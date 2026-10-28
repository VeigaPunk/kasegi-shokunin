#!/usr/bin/env python3
"""r45-c2-gate.py — round-45 C2 counter (coverage), v1.

WHAT IT MEASURES
    One frontier move, F27 (Linux kernel security-bugs reporting process; row
    S071, capture `corpus/source-snapshots/round-45/S071.txt`), counted through
    seven limbs that a junk row, a sourceless row or an entry that quotes text
    the source does not hold cannot satisfy:

    G1  frontier table: exactly 27 rows and 27 `admitted` (status = third cell),
        no duplicate ids, row F27 admitted, its entry cell names a
        `knowledge/*.md` path that exists under --root.
    G2  that entry opens with the provenance trio: `source: S071 — https://docs.kernel.org/process/security-bugs.html`,
        `verified-at: 2026-10-28`, a `recheck:` line.
    G3  SOURCES.md row S071: 11 cells, tier A, status `mined`, opened 2026-10-28,
        source cell holds the canonical URL, `used-by` lists the entry path, and
        the anchor cell carries the snapshot's sha256.
    G4  capture: source-recheck.py exits 0 on manifest S071 (sha256 OK and five
        quotes OK) and the manifest holds the five frozen quote cores.
    G5  entry citations: every curly-quoted span followed by a backticked
        `S071.txt:N[-M]` citation is located (whitespace/markup-normalised) in
        snapshot lines N..M, every span is <= 25 words, at least four spans
        pass, and the four frozen cores (7-day embargo ceiling, AI treated as
        public, binary-only refusal, unreproducible is not exploitable) each
        appear inside a located span.
    G6  `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 64.
    G7  `sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0.

    READ-ONLY; stdlib; honors TMPDIR; never runs git.

USAGE
    python3 corpus/instruments/r45-c2-gate.py --root TREE
OUTPUT
    one `gate G<n> pass=0|1 read=<token>` line each, then
    `c2-gate fixed=<k>/7 exit=0|1`
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys

CENSUS = os.environ.get("SOURCES_CENSUS", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")
URL = "https://docs.kernel.org/process/security-bugs.html"
CORES = [
    r"up to 7 calendar days",
    r"treat it as public",
    r"Binary-only executables are not accepted",
    r"cannot be reproduced, it is not exploitable",
]
MANIFEST_CORES = [
    "for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days",
    "If you resorted to AI assistance to identify a bug, you must treat it as public",
    "Binary-only executables are not accepted.",
    "By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.",
    "with no version indication, your report will not be processed",
]


def norm(s: str) -> str:
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(s.split())


def txt(root: str, rel: str) -> str | None:
    try:
        with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def run(cmd: list[str], cwd: str) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.SubprocessError) as exc:
        return 99, f"run-error {exc}"
    return p.returncode, p.stdout + p.stderr


def frontier(root: str) -> tuple[list[list[str]], str]:
    t = txt(root, "corpus/README.md") or ""
    rows = []
    for ln in t.splitlines():
        if re.match(r"^\| F\d+ \|", ln):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows, t


def entry_path(root: str) -> tuple[str | None, str]:
    rows, _ = frontier(root)
    f27 = [r for r in rows if r[0] == "F27"]
    if len(f27) != 1 or len(f27[0]) < 4:
        return None, "F27-rows=%d" % len(f27)
    m = re.findall(r"knowledge/[A-Za-z0-9._-]+\.md", f27[0][3])
    for p in m:
        full = os.path.join("corpus", p)
        if os.path.isfile(os.path.join(root, full)):
            return full, "entry=" + full
    return None, "F27-entry-missing"


def g1(root: str) -> tuple[bool, str]:
    rows, _ = frontier(root)
    ids = [r[0] for r in rows]
    adm = sum(1 for r in rows if len(r) > 2 and r[2] == "admitted")
    dup = len(ids) - len(set(ids))
    if len(rows) != 27 or adm != 27 or dup:
        return False, f"rows={len(rows)} admitted={adm} dup={dup}"
    p, why = entry_path(root)
    f27 = [r for r in rows if r[0] == "F27"][0]
    if f27[2] != "admitted" or p is None:
        return False, why
    return True, f"rows=27 admitted=27 {why}"


def g2(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    head = (txt(root, p) or "").splitlines()[:8]
    ok_s = any(h.startswith("source: S071 — " + URL) for h in head)
    ok_v = any(h == "verified-at: 2026-10-28" for h in head)
    ok_r = any(h.startswith("recheck:") and len(h) > 10 for h in head)
    return (ok_s and ok_v and ok_r), f"source={int(ok_s)} verified-at={int(ok_v)} recheck={int(ok_r)}"


def g3(root: str) -> tuple[bool, str]:
    p, _ = entry_path(root)
    row = None
    for ln in (txt(root, "corpus/SOURCES.md") or "").splitlines():
        if re.match(r"^ {0,3}\|\s*S071\s*\|", ln):
            c = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(c) == 11:
                row = c
    if row is None:
        return False, "row-S071=absent-or-malformed"
    try:
        sha = hashlib.sha256(open(os.path.join(root, "corpus/source-snapshots/round-45/S071.txt"), "rb").read()).hexdigest()
    except OSError:
        return False, "snapshot-absent"
    bad = []
    if row[3] != "A": bad.append("tier")
    if row[7] != "mined": bad.append("status")
    if row[8] != "2026-10-28": bad.append("opened")
    if URL not in row[1]: bad.append("url")
    if p is None or p not in row[10]: bad.append("used-by")
    if sha not in row[5]: bad.append("anchor-sha")
    return (not bad), ("row-S071=ok" if not bad else "bad=" + ",".join(bad))


def g4(root: str) -> tuple[bool, str]:
    man = os.path.join(root, "corpus/source-snapshots/round-45/manifest.json")
    if not os.path.isfile(man):
        return False, "manifest-absent"
    rc, out = run([sys.executable, os.path.join(root, "corpus/instruments/source-recheck.py"), "--manifest", man,
                   "--source", "S071"], root)
    oks = len(re.findall(r"^S071:Q\d+ OK ", out, re.M))
    mt = norm(open(man, encoding="utf-8").read())
    miss = [c for c in MANIFEST_CORES if norm(c) not in mt]
    good = rc == 0 and "S071:sha256 OK" in out and oks >= 5 and not miss and "BROKEN" not in out
    return good, f"recheck-rc={rc} quotes-ok={oks} frozen-cores-missing={len(miss)}"


def g5(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    body = txt(root, p) or ""
    snap = (txt(root, "corpus/source-snapshots/round-45/S071.txt") or "").splitlines()
    spans = re.findall(r"“([^”]+)”\s*\(`?S071\.txt:(\d+)(?:-(\d+))?`?", body)
    passed, failed = [], 0
    for q, a, b in spans:
        a = int(a)
        b = int(b) if b else a
        window = norm(" ".join(snap[max(a - 1, 0):b]))
        nq = norm(q)
        if len(nq.split()) <= 25 and nq and nq in window:
            passed.append(nq)
        else:
            failed += 1
    cores = [c for c in CORES if any(re.search(c, q) for q in passed)]
    ok = failed == 0 and len(passed) >= 4 and len(cores) == len(CORES)
    return ok, f"spans={len(spans)} located={len(passed)} failed={failed} cores={len(cores)}/{len(CORES)}"


def g6(root: str) -> tuple[bool, str]:
    d = os.path.join(root, "corpus/knowledge")
    n = len([f for f in os.listdir(d) if f.endswith(".md") and os.path.isfile(os.path.join(d, f))]) if os.path.isdir(d) else -1
    return n == 64, f"knowledge={n}"


def g7(root: str) -> tuple[bool, str]:
    rc, out = run(["bash", CENSUS, "validate", "--file", os.path.join(root, "corpus/SOURCES.md")], root)
    return rc == 0, f"census-rc={rc}"


GATES = [("G1", g1), ("G2", g2), ("G3", g3), ("G4", g4), ("G5", g5), ("G6", g6), ("G7", g7)]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    a = ap.parse_args(argv)
    if not os.path.isdir(a.root):
        print(f"r45-c2-gate: {a.root} is not a directory", file=sys.stderr)
        return 2
    root = os.path.abspath(a.root)
    fixed = 0
    for gid, fn in GATES:
        try:
            ok, read = fn(root)
        except Exception as exc:
            ok, read = False, f"exception-{type(exc).__name__}"
        fixed += 1 if ok else 0
        print(f"gate {gid} pass={1 if ok else 0} read={read}")
    code = 0 if fixed == len(GATES) else 1
    print(f"c2-gate fixed={fixed}/{len(GATES)} exit={code}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
