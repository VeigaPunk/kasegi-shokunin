#!/usr/bin/env python3
"""Q9 binding table (round-29 reviewer instrument, RevC2Manifest).

Re-runs the QUALITY Q9 binding over a source-snapshot manifest:
  1. the record's `path` stem equals its `id`;
  2. each quote is exactly-once in the capture (raw AND normalized), or carries
     an `anchor` line the instrument's window rule verifies;
  3. the observed occurrence counts (raw and normalized) are printed per row.

Exit is a verdict: 0 = every row passes, 1 = any row FAILs, 2 = structural
(manifest unreadable/invalid). --require-exactly-once additionally FAILs rows
that only pass via the anchor fallback (the frozen C2 kill-rule bar
"any manifest assertion not occurrences=1").

Read-only over its inputs; stdlib only; deterministic.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 1
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
MARKUP_RE = re.compile(r"</?u>")


def normalize(text):
    return " ".join(MARKUP_RE.sub("", text).split())


def anchor_note(assertion, raw_lines, n_normalized):
    """Mirror corpus/instruments/source-recheck.py anchor_verdict()."""
    anchor = assertion.get("anchor")
    if anchor is None:
        return "" if n_normalized <= 1 else " anchor=MISSING"
    if not (isinstance(anchor, int) and 1 <= anchor <= len(raw_lines)):
        return " anchor=OUT-OF-RANGE"
    window = " ".join(raw_lines[max(0, anchor - 1):anchor + 3])
    expected = normalize(assertion["quote"])
    if expected and expected in normalize(window):
        return " anchor=%d-ok" % anchor
    return " anchor=%d-BROKEN" % anchor


def main(argv=None):
    parser = argparse.ArgumentParser(description="QUALITY Q9 binding table for a snapshot manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--require-exactly-once", action="store_true",
                        help="FAIL anchor-fallback rows too (C2 kill rule: occurrences=1)")
    args = parser.parse_args(argv)

    mpath = Path(args.manifest).resolve(strict=True) if Path(args.manifest).exists() else None
    if mpath is None:
        print("q9 manifest UNAVAILABLE reason=missing")
        return 2
    try:
        data = json.loads(mpath.read_bytes().decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("q9 manifest UNAVAILABLE reason=unreadable-or-invalid")
        return 2
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION or not isinstance(data.get("sources"), list):
        print("q9 manifest UNAVAILABLE reason=unsupported-schema")
        return 2

    base = mpath.parent
    rows = []
    failed = once = anchored = 0
    for record in sorted(data["sources"], key=lambda r: r.get("id") or ""):
        sid = record.get("id")
        path = record.get("path")
        stem = Path(path).stem if isinstance(path, str) and path else None
        stem_ok = isinstance(sid, str) and ID_RE.fullmatch(sid) is not None and stem == sid
        capture = base / path if isinstance(path, str) and path and not Path(path).is_absolute() else None
        text = None
        sha_ok = False
        raw_lines = []
        if capture is not None:
            try:
                resolved = (base / path).resolve(strict=True)
                if str(resolved).startswith(str(base.resolve(strict=True))):
                    raw = resolved.read_bytes()
                    sha_ok = hashlib.sha256(raw).hexdigest() == record.get("sha256")
                    text = raw.decode("utf-8")
                    raw_lines = text.splitlines()
            except (OSError, RuntimeError, ValueError, UnicodeError):
                text = None
        nsrc = normalize(text) if text is not None else ""
        for assertion in sorted(record.get("quotes") or [], key=lambda q: q.get("id") or ""):
            qid = assertion.get("id")
            quote = assertion.get("quote") or ""
            raw_n = text.count(quote) if text is not None else 0
            nq = normalize(quote)
            norm_n = nsrc.count(nq) if text is not None else 0
            note = anchor_note(assertion, raw_lines, norm_n) if text is not None else " anchor=n/a"
            anchor_declared_invalid = note.endswith("-BROKEN") or note.endswith("OUT-OF-RANGE")
            if raw_n == 1 and norm_n == 1 and not anchor_declared_invalid:
                bind = "once"
            elif anchor_declared_invalid:
                bind = "anchor-broken"
            elif note.endswith("-ok"):
                bind = "anchored"
            elif raw_n == 0 and norm_n == 0:
                bind = "not-found"
            elif note.endswith("MISSING"):
                bind = "unanchored-multi"
            else:
                bind = "anchor-broken"
            verdict = "PASS"
            reason = ""
            if not stem_ok:
                verdict, reason = "FAIL", " stem!=id"
            elif not sha_ok:
                verdict, reason = "FAIL", " sha-mismatch"
            elif anchor_declared_invalid:
                # A declared anchor the instrument disproves fails the row even
                # when the quote itself is exactly-once (probe P3).
                verdict, reason = "FAIL", " " + bind
            elif bind == "once":
                pass
            elif bind == "anchored":
                if args.require_exactly_once:
                    verdict, reason = "FAIL", " not-exactly-once(c2-bar)"
            else:
                verdict, reason = "FAIL", " " + bind
            if verdict == "PASS":
                if bind == "once":
                    once += 1
                else:
                    anchored += 1
            else:
                failed += 1
            rows.append(f"{sid}:{qid} stem={'ok' if stem_ok else 'MISMATCH'} sha={'ok' if sha_ok else 'MISMATCH'} "
                        f"raw={raw_n} norm={norm_n} bind={bind}{note} verdict={verdict}{reason}")
    digest = hashlib.sha256(mpath.read_bytes()).hexdigest()
    for row in rows:
        print(row)
    total = once + anchored + failed
    print(f"q9-binding manifest={digest[:12]} sources={len(data['sources'])} assertions={total} "
          f"exactly-once={once} anchored-ok={anchored} failed={failed} exit={0 if failed == 0 else 1}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
