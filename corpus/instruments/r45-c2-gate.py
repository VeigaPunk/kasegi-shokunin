#!/usr/bin/env python3
"""r45-c2-gate.py — round-45 C2 counter (coverage), v1.1 (hardened after the wave-1 falsification).

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

    VERSION 1.1 (erratum E1, predicate and gate names unchanged; v1 digest 5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082).
    Wave 1 falsified v1 (`.ufo/waves/round-45/wave1/R45RevGate*`, `R45Mut*`, `R45CritKillC2.md`): G1 accepted an existing unrelated or empty
    entry and rows inside comments/fences, G2 accepted a header-only stub and a URL suffix, G3 accepted a self-pinned empty snapshot, G4 ran a
    tree-supplied source-recheck against a tree-supplied manifest, G5 accepted uncited and fabricated-capture quotes, G6 accepted padding,
    G7 honored an env-overridden census.  v1.1: rows are read only from the real tables (no comments/fences), the F27 entry must be a unique
    regular file with the required sections and located cross-references, the frozen captures and the manifest are pinned by sha256, source-recheck.py
    runs from THIS script's own lane, every curly-quoted span in the entry must be a located S071 citation, the knowledge dir must equal the 63
    base names plus exactly the F27 entry, and the census path is a constant.

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
import json
import os
import re
import subprocess
import sys

CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PINS = {
    "S071.txt": "0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40",
    "manifest.json": "125339d9ec21bfdc7a07a164fd2e7023c1f4976daa1f34e18aaba4edba05f459",
    "base-knowledge-names": "a93599be6ca5784d5fbcdc6340d14b6cfc7409ab392ab7399bc934a873c66bed",
}
if os.environ.get("R45_PINS_OVERRIDE"):  # selftests only: the grader's environment, never the graded tree's
    PINS.update(json.load(open(os.environ["R45_PINS_OVERRIDE"])))
SECTIONS = ["## Scope and decision rule", "## Overlap and novelty", "## Limits", "## Falsifiable package rule"]
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


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def live_lines(t: str) -> list[str]:
    """Lines outside HTML comments and fenced code blocks."""
    t = re.sub(r"(?s)<!--.*?-->", "", t)
    out, fence = [], False
    for ln in t.splitlines():
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    return out


def frontier(root: str) -> tuple[list[list[str]], str]:
    t = txt(root, "corpus/README.md") or ""
    rows = []
    for ln in live_lines(t):
        if re.match(r"^\| F\d+ \|", ln):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows, t


def registry_lines(root: str) -> list[str]:
    t = txt(root, "corpus/SOURCES.md") or ""
    out, inreg = [], False
    for ln in live_lines(t):
        if re.match(r"^ {0,3}## ", ln):
            inreg = bool(re.match(r"^ {0,3}## Registry\b", ln))
            continue
        if inreg:
            out.append(ln)
    return out


def entry_path(root: str) -> tuple[str | None, str]:
    rows, _ = frontier(root)
    f27 = [r for r in rows if r[0] == "F27"]
    if len(f27) != 1 or len(f27[0]) < 4:
        return None, "F27-rows=%d" % len(f27)
    m = re.findall(r"knowledge/[A-Za-z0-9._-]+\.md", f27[0][3])
    if len(m) != 1:
        return None, "F27-entry-cell-paths=%d" % len(m)
    full = os.path.join("corpus", m[0])
    fp = os.path.join(root, full)
    if os.path.islink(fp) or not os.path.isfile(fp):
        return None, "F27-entry-not-a-regular-file"
    if any(m[0] in r[3] for r in rows if r[0] != "F27" and len(r) > 3):
        return None, "F27-entry-shared-with-another-row"
    return full, "entry=" + full


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
    body = txt(root, p) or ""
    head = body.splitlines()[:8]
    ok_s = any(h.startswith("source: S071 — " + URL + " — ") for h in head)
    ok_v = any(h == "verified-at: 2026-10-28" for h in head)
    ok_r = any(h.startswith("recheck: ") and "source-recheck.py" in h and "--source S071" in h for h in head)
    secs = sum(1 for sct in SECTIONS if re.search("^" + re.escape(sct) + r"\s*$", body, re.M))
    tbl = len([ln for ln in body.splitlines() if re.match(r"^\|[^|]+\|[^|]+\|[^|]+\|\s*$", ln)]) - 2
    refs = re.findall(r"corpus/knowledge/([A-Za-z0-9._-]+\.md):(\d+)", body)
    refok = 0
    for fn, ln in refs:
        t = txt(root, "corpus/knowledge/" + fn)
        if t is not None and 1 <= int(ln) <= len(t.splitlines()):
            refok += 1
    need = {"coordinated-disclosure-timelines.md", "ai-assisted-finding-validation.md"}
    have = {fn for fn, ln in refs}
    ok_x = need <= have and refok == len(refs)
    good = ok_s and ok_v and ok_r and secs == len(SECTIONS) and tbl >= 6 and ok_x
    return good, f"source={int(ok_s)} verified-at={int(ok_v)} recheck={int(ok_r)} sections={secs}/{len(SECTIONS)} table-rows={tbl} xrefs={refok}/{len(refs)}"


def g3(root: str) -> tuple[bool, str]:
    p, _ = entry_path(root)
    row = None
    hits = [ln for ln in registry_lines(root) if re.match(r"^ {0,3}\|\s*S071\s*\|", ln)]
    if len(hits) == 1:
        c = [x.strip() for x in hits[0].strip().strip("|").split("|")]
        if len(c) == 11:
            row = c
    if row is None:
        return False, "row-S071=absent-or-malformed"
    try:
        snap_sha = sha(open(os.path.join(root, "corpus/source-snapshots/round-45/S071.txt"), "rb").read())
    except OSError:
        return False, "snapshot-absent"
    if snap_sha != PINS["S071.txt"]:
        return False, "snapshot-not-the-pinned-capture"
    bad = []
    if row[3] != "A": bad.append("tier")
    if row[7] != "mined": bad.append("status")
    if row[8] != "2026-10-28": bad.append("opened")
    if URL not in row[1]: bad.append("url")
    if p is None or p not in row[10]: bad.append("used-by")
    if snap_sha not in row[5]: bad.append("anchor-sha")
    return (not bad), ("row-S071=ok" if not bad else "bad=" + ",".join(bad))


def g4(root: str) -> tuple[bool, str]:
    man = os.path.join(root, "corpus/source-snapshots/round-45/manifest.json")
    if not os.path.isfile(man):
        return False, "manifest-absent"
    if sha(open(man, "rb").read()) != PINS["manifest.json"]:
        return False, "manifest-not-the-pinned-bytes"
    rc, out = run([sys.executable, os.path.join(TOOL_ROOT, "corpus/instruments/source-recheck.py"), "--manifest", man,
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
    allcurly = re.findall("\u201c([^\u201d]+)\u201d", body)
    spans = re.findall("\u201c([^\u201d]+)\u201d\\s*\\(`?S071\\.txt:(\\d+)(?:-(\\d+))?`?", body)
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
    uncited = len(allcurly) - len(spans)
    ok = failed == 0 and uncited == 0 and len(passed) >= 4 and len(cores) == len(CORES)
    return ok, f"spans={len(spans)} located={len(passed)} failed={failed} uncited={uncited} cores={len(cores)}/{len(CORES)}"


def g6(root: str) -> tuple[bool, str]:
    d = os.path.join(root, "corpus/knowledge")
    names = sorted(f for f in os.listdir(d) if f.endswith(".md")) if os.path.isdir(d) else []
    p, why = entry_path(root)
    base_like = [n for n in names if p is None or "corpus/knowledge/" + n != p]
    base_ok = sha(("\n".join(base_like) + "\n").encode()) == PINS["base-knowledge-names"]
    sized = p is not None and os.path.getsize(os.path.join(root, p)) >= 3000
    return (len(names) == 64 and base_ok and sized), f"knowledge={len(names)} base-names-intact={int(base_ok)} entry-bytes-ok={int(sized)}"


def g7(root: str) -> tuple[bool, str]:
    rc, out = run(["bash", CENSUS, "validate", "--file", os.path.join(root, "corpus/SOURCES.md")], root)
    ok_line = bool(re.search(r"^\S+\tok\t", out, re.M))
    return rc == 0 and ok_line, f"census-rc={rc} ok-line={int(ok_line)}"


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
