#!/usr/bin/env python3
"""Capture a public source into a committed, re-verifiable text snapshot.

Usage:
  python3 corpus/instruments/capture-source.py --id S001 --url URL \
      --out corpus/source-snapshots/round-24/S001.txt [--kind html|pdf|text] [--allow TSV]
  python3 corpus/instruments/capture-source.py --selftest

The snapshot is the bytes `source-recheck.py` hashes and searches: the fetched
body converted to UTF-8 text (HTML tags stripped and entities decoded, PDF text
via `pdftotext -enc UTF-8`, plain text kept as served), each line whitespace
collapsed. The script prints the sha256 of the written snapshot, the fetched
byte count and the UTC fetch time so the manifest record can be bound to it.

This instrument captures evidence of what a source said at one instant. It does
not establish that the source is current today, that the quote asserts what the
entry claims, or that the host will serve the same bytes again — the manifest
sha256 binds the snapshot, the round's Gate block records the reading.

Intake gate (round 90). Before the snapshot file is opened, its bytes are
scanned with capture-secret-scan.py beside this file (its patterns(),
load_allow() and scan_bytes(), imported, never copied) under the snapshot's
lane-relative path. A hit refuses the capture: nothing is written (an existing
file at --out is left byte-for-byte as it was), one INTAKE-REFUSED line per
shape names the shape and line only (never the matched value), exit 3. A
scanner or allowlist that cannot be loaded refuses the same way (fail closed).
An allowlist row (path, shape, sha256 of the matched bytes, reason) lets one
documented value through at one path, as a push-protection bypass carries a
reason. Design source: S131, GitHub's push protection "blocks pushes that
contain secrets before they reach your repository" (S131.txt:570); round 86
committed a live STS token in a capture (lesson M86-2) because nothing scanned
a capture before it was written.
"""
import argparse
import datetime
import hashlib
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(HERE))
REFUSED_RC = 3

UA = "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"
MAX_FETCH_BYTES = 32 * 1024 * 1024
SCRIPT_RE = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")
BLANK_RE = re.compile(r"[ \t\u00a0]+")


def collapse(text):
    lines = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = BLANK_RE.sub(" ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines) + "\n"


def html_to_text(raw):
    text = SCRIPT_RE.sub(" ", raw)
    text = re.sub(r"</(p|div|li|tr|h[1-6]|section|article|br)>", "\n", text, flags=re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = TAG_RE.sub("", text)
    return collapse(html.unescape(text))


def pdf_to_text(raw):
    tool = shutil.which("pdftotext")
    if not tool:
        raise SystemExit("pdftotext not found; install poppler-utils from an official binary")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
        fh.write(raw)
        tmp = fh.name
    try:
        proc = subprocess.run([tool, "-enc", "UTF-8", tmp, "-"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
        if proc.returncode != 0:
            raise SystemExit("pdftotext failed rc=%d: %s" % (proc.returncode, proc.stderr[:200]))
        return collapse(proc.stdout.decode("utf-8", "replace"))
    finally:
        os.unlink(tmp)


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read(MAX_FETCH_BYTES + 1)
        if len(body) > MAX_FETCH_BYTES:
            raise SystemExit("response exceeds %d bytes" % MAX_FETCH_BYTES)
        return body, response.status


def load_scanner():
    path = os.path.join(HERE, "capture-secret-scan.py")
    spec = importlib.util.spec_from_file_location("capture_secret_scan", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lane_rel(out):
    p = os.path.abspath(out)
    rel = os.path.relpath(p, LANE)
    return p if rel.startswith("..") else rel


def intake_gate(data, out, allow_path):
    """Return [(shape, line)] that refuse these bytes at --out; [("gate-error", 0)] if the scanner cannot run."""
    try:
        scan = load_scanner()
        allow = scan.load_allow(allow_path or os.path.join(HERE, "capture-secret-allow.tsv"))
        found, _ = scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)
        return found
    except Exception as e:  # fail closed: a gate that cannot run refuses
        return [("gate-error:%s" % type(e).__name__, 0)]


def capture(source_id, url, out, kind, allow_path=None):
    raw, status = fetch(url)
    if kind == "pdf":
        text = pdf_to_text(raw)
    elif kind == "text":
        text = collapse(raw.decode("utf-8", "replace"))
    else:
        text = html_to_text(raw.decode("utf-8", "replace"))
    data = text.encode("utf-8")
    found = intake_gate(data, out, allow_path)
    if found:
        for shape, line in found:
            print("INTAKE-REFUSED %s shape=%s line=%d out=%s written=no" % (source_id, shape, line, out))
        return None
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as fh:
        fh.write(data)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("%s status=%d fetched_bytes=%d snapshot_bytes=%d sha256=%s utc=%s out=%s" % (
        source_id, status, len(raw), len(data), hashlib.sha256(data).hexdigest(), stamp, out))
    return hashlib.sha256(data).hexdigest()


def selftest():
    """Prove the capture pipeline is deterministic and the digest binds bytes."""
    directory = tempfile.mkdtemp(prefix="capture-source-selftest-")
    try:
        sample = "<html><head><style>x{}</style></head><body><p>Alpha&nbsp; beta</p><u>gamma</u></body></html>"
        raw = os.path.join(directory, "in.html")
        with open(raw, "w", encoding="utf-8") as fh:
            fh.write(sample)
        text = html_to_text(open(raw, encoding="utf-8").read())
        once = hashlib.sha256(text.encode("utf-8")).hexdigest()
        text2 = html_to_text(open(raw, encoding="utf-8").read())
        twice = hashlib.sha256(text2.encode("utf-8")).hexdigest()
        ok_text = text == "Alpha beta\ngamma\n"
        print("selftest normalize=%s deterministic=%s" % ("ok" if ok_text else "FAIL",
                                                          "ok" if once == twice else "FAIL"))
        token = "IQoJb3JpZ2luX2VjEXAMPLEFAKESESSIONTOKENVALUE0123456789abcdefABCDEF"
        planted = os.path.join(directory, "planted.html")
        with open(planted, "w", encoding="utf-8") as fh:
            fh.write("<p>u?X-Amz-Security-Token=%s&amp;X-Amz-Signature=1</p>" % token)
        out = os.path.join(directory, "out.txt")
        with open(out, "wb") as fh:
            fh.write(b"previous\n")
        refused = capture("SELFTEST", "file://" + planted, out, "html") is None
        kept = open(out, "rb").read() == b"previous\n"
        print("selftest intake-refuse=%s existing-kept=%s" % ("ok" if refused else "FAIL", "ok" if kept else "FAIL"))
        return 0 if ok_text and once == twice and refused and kept else 1
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--id")
    parser.add_argument("--url")
    parser.add_argument("--out")
    parser.add_argument("--kind", choices=("html", "pdf", "text"), default="html")
    parser.add_argument("--allow")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.id and args.url and args.out):
        parser.error("--id, --url and --out are required unless --selftest")
    if capture(args.id, args.url, args.out, args.kind, args.allow) is None:
        return REFUSED_RC
    return 0


if __name__ == "__main__":
    sys.exit(main())
