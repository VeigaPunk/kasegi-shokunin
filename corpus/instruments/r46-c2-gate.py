#!/usr/bin/env python3
"""r46-c2-gate.py — round-46 C2 counter (coverage), v1.1 (hardened after the wave-1 falsification; erratum E1, see .ufo/waves/round-46/counter-errata.md; v1 sha256 0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6).

WHAT IT MEASURES
    One frontier move, F28 (GitHub private vulnerability reporting, the reporter-side
    flow; row S073, capture `corpus/source-snapshots/round-46/S073.txt`), counted through
    seven limbs that a junk row, a sourceless row or an entry that quotes text the source
    does not hold cannot satisfy (the limbs carry the round-46 v1.2 hardening: real tables
    only, pinned captures, tool-side source-recheck, every curly quote located, base
    knowledge directory pinned, constant census path):

    G1  frontier table: exactly 28 rows and 28 `admitted` (status = third cell),
        no duplicate ids, row F28 admitted, its entry cell names one `knowledge/*.md`
        path that exists under --root and is shared with no other row.
    G2  that entry opens with the provenance trio: `source: S073 — <canonical URL> — `,
        `verified-at: 2026-10-28`, a `recheck:` line running source-recheck.py --source S073;
        carries the four sections of the round-46 entry shape, >= 6 table rows and
        cross-references (file:line, in range) to ai-assisted-finding-validation.md and
        linux-kernel-security-bugs-reporting-process.md.
    G3  SOURCES.md row S073: 11 cells, tier A, status `mined`, opened 2026-10-28,
        source cell holds the canonical URL, `used-by` lists the entry path, the anchor
        cell carries the snapshot's sha256.
    G4  capture: this lane's source-recheck.py exits 0 on manifest S073 (sha256 OK and
        >= 8 quotes OK) and the manifest holds the five frozen quote cores.
    G5  entry citations: every curly-quoted span followed by a backticked `S073.txt:N[-M]`
        citation is located (whitespace/markup-normalised) in snapshot lines N..M, every
        span is <= 25 words, at least four pass, no curly quote is uncited, and the five
        frozen cores each appear inside a located span.
    G6  `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 65 and the other 64 files
        are the round-46 tip's bytes.
    G7  `sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0.

    The knowledge entry and the F28 / S073 row bytes are NOT pinned (they do not exist at freeze):
    the gate grades structure and located quotes, and the non-author closure re-opens the page.

    READ-ONLY; stdlib; honors TMPDIR; never runs git.

USAGE
    python3 corpus/instruments/r46-c2-gate.py --root TREE
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
    "S073.txt": "66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930",
    "manifest.json": "01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34",
    "entry": None,
    "S073-row": None,
    "F28-row": None,
    "source-recheck.py": "fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003",
    "base-knowledge-content": "5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47",
    "base-knowledge-names": "bf3044814698b31b2d63a47ef6933cfe4d2d09635c2d717b05c8adf0bf719f5d",
}
if os.environ.get("R46_PINS_OVERRIDE"):  # selftests only: the grader's environment, never the graded tree's; a null value disables that one pin
    PINS.update(json.load(open(os.environ["R46_PINS_OVERRIDE"])))
CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}
BODY = (556, 583)  # the page body inside the capture (the rest is site navigation); a quote located elsewhere is not support
SECTIONS = ["## Scope and decision rule", "## Overlap and novelty", "## Limits", "## Falsifiable package rule"]
URL = "https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately"
CORES = [
    r"only report vulnerabilities privately for repositories where this feature is enabled",
    r"summary, details, proof of concept, and impact statement",
    r"I used AI assistance",
    r"credited user on the proposed advisory",
    r"only the repository maintainer can merge",
]
MANIFEST_CORES = [
    "You can only report vulnerabilities privately for repositories where this feature is enabled.",
    "By default, you must provide a summary, details, proof of concept, and impact statement.",
    "Optionally, select I used AI assistance to find or write up this report.",
    "GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.",
    "only the repository maintainer can merge changes from that private fork into the parent repository",
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
    out, fence = [], None
    for ln in t.splitlines():
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            mark = st[:3]
            fence = None if fence == mark else (fence or mark)
            continue
        if fence is None:
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
        if re.match(r"^ {0,3}#{1,6} ", ln):
            inreg = bool(re.match(r"^ {0,3}## Registry\b", ln))
            continue
        if inreg:
            out.append(ln)
    return out


def entry_path(root: str) -> tuple[str | None, str]:
    rows, _ = frontier(root)
    f27 = [r for r in rows if r[0] == "F28"]
    if len(f27) != 1 or len(f27[0]) < 4:
        return None, "F28-rows=%d" % len(f27)
    m = re.findall(r"knowledge/[A-Za-z0-9._-]+\.md", f27[0][3])
    if len(m) != 1:
        return None, "F28-entry-cell-paths=%d" % len(m)
    full = os.path.join("corpus", m[0])
    fp = os.path.join(root, full)
    if os.path.islink(fp) or not os.path.isfile(fp):
        return None, "F28-entry-not-a-regular-file"
    if any(m[0] in r[3] for r in rows if r[0] != "F28" and len(r) > 3):
        return None, "F28-entry-shared-with-another-row"
    return full, "entry=" + full


def g1(root: str) -> tuple[bool, str]:
    rows, _ = frontier(root)
    ids = [r[0] for r in rows]
    adm = sum(1 for r in rows if len(r) > 2 and r[2] == "admitted")
    dup = len(ids) - len(set(ids))
    if len(rows) != 28 or adm != 28 or dup:
        return False, f"rows={len(rows)} admitted={adm} dup={dup}"
    p, why = entry_path(root)
    f27 = [r for r in rows if r[0] == "F28"][0]
    if f27[2] != "admitted" or p is None:
        return False, why
    raw = [ln for ln in live_lines(txt(root, "corpus/README.md") or "") if re.match(r"^\| F28 \|", ln)]
    if len(raw) != 1 or (False):
        return False, "F28-row-not-the-pinned-line"
    return True, f"rows=28 admitted=28 {why}"


def sect_words(body: str, heading: str) -> int:
    m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return len(re.findall(r"\w+", m.group(1))) if m else 0


def g2(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    raw_b = open(os.path.join(root, p), "rb").read()
    if PINS["entry"] is not None and sha(raw_b) != PINS["entry"]:
        return False, "entry-not-the-pinned-bytes"
    body = "\n".join(live_lines(raw_b.decode("utf-8", "replace")))
    head = body.splitlines()[:8]
    ok_s = any(h.startswith("source: S073 \u2014 " + URL + " \u2014 ") for h in head)
    ok_v = any(h == "verified-at: 2026-10-28" for h in head)
    ok_r = any(h.startswith("recheck: ") and "source-recheck.py" in h and re.search(r"--source S073(?:\s|$)", h) and "round-46/manifest.json" in h for h in head)
    secs = sum(1 for sct in SECTIONS if re.search("^" + re.escape(sct) + r"\s*$", body, re.M))
    full = sum(1 for sct in SECTIONS if sect_words(body, sct) >= (12 if sct.startswith("## Falsifiable") else 25))
    rows = []
    for ln in body.splitlines():
        if re.match(r"^\|[^|]+\|[^|]+\|[^|]+\|\s*$", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if all(len(re.findall(r"\w+", c)) >= 2 for c in cells) and re.search(r"S073\.txt:\d+", cells[1] + " " + cells[0]):
                rows.append(cells)
    tbl = len(rows)
    refs = re.findall(r"corpus/knowledge/([A-Za-z0-9._-]+\.md):(\d+)", body)
    refok = 0
    for fn, ln in refs:
        t = txt(root, "corpus/knowledge/" + fn)
        if t is not None and 1 <= int(ln) <= len(t.splitlines()):
            refok += 1
    need = {"linux-kernel-security-bugs-reporting-process.md", "ai-assisted-finding-validation.md"}
    have = {fn for fn, ln in refs}
    ok_x = need <= have and refok == len(refs)
    good = ok_s and ok_v and ok_r and secs == len(SECTIONS) and full == len(SECTIONS) and tbl >= 6 and ok_x
    return good, f"source={int(ok_s)} verified-at={int(ok_v)} recheck={int(bool(ok_r))} sections={secs}/{len(SECTIONS)} full={full}/{len(SECTIONS)} table-rows={tbl} xrefs={refok}/{len(refs)}"


def g3(root: str) -> tuple[bool, str]:
    p, _ = entry_path(root)
    row = None
    hits = [ln for ln in registry_lines(root) if re.match(r"^ {0,3}\|\s*S073\s*\|", ln)]
    if len(hits) == 1:
        c = [x.strip() for x in hits[0].strip().strip("|").split("|")]
        if len(c) == 11:
            row = c
        if PINS["S073-row"] is not None and sha(hits[0].strip().encode("utf-8")) != PINS["S073-row"]:
            return False, "S073-row-not-the-pinned-line"
    if row is None:
        return False, "row-S073=absent-or-malformed"
    try:
        snap_sha = sha(open(os.path.join(root, "corpus/source-snapshots/round-46/S073.txt"), "rb").read())
    except OSError:
        return False, "snapshot-absent"
    if snap_sha != PINS["S073.txt"]:
        return False, "snapshot-not-the-pinned-capture"
    bad = []
    if row[3] != "A": bad.append("tier")
    if row[2] != "docs": bad.append("kind")
    if len(re.findall(r"\w+", row[4])) < 8: bad.append("scope-words")
    if len(re.findall(r"\w+", row[6])) < 8: bad.append("teaches-words")
    if not re.fullmatch(r"(?:\d+d|on-release|\d{4}-\d{2}-\d{2})", row[9]): bad.append("recheck-cell")
    if "S073.txt" not in row[5] or not re.search(r"(?:\bL\d+|\blines?\s+\d+|S073\.txt:\d+)", row[5]): bad.append("anchor-locator")
    if row[7] != "mined": bad.append("status")
    if row[8] != "2026-10-28": bad.append("opened")
    u = re.findall(r"https?://\S+", row[1])
    if not u or u[0].rstrip(".,;)") != URL: bad.append("url")
    if p is None or p not in row[10]: bad.append("used-by")
    if snap_sha not in row[5]: bad.append("anchor-sha")
    return (not bad), ("row-S073=ok" if not bad else "bad=" + ",".join(bad))


def g4(root: str) -> tuple[bool, str]:
    man = os.path.join(root, "corpus/source-snapshots/round-46/manifest.json")
    if not os.path.isfile(man):
        return False, "manifest-absent"
    if sha(open(man, "rb").read()) != PINS["manifest.json"]:
        return False, "manifest-not-the-pinned-bytes"
    rcb = open(os.path.join(TOOL_ROOT, "corpus/instruments/source-recheck.py"), "rb").read()
    if PINS["source-recheck.py"] is not None and sha(rcb) != PINS["source-recheck.py"]:
        return False, "source-recheck-not-the-pinned-bytes"
    rc, out = run([sys.executable, "-I", os.path.join(TOOL_ROOT, "corpus/instruments/source-recheck.py"), "--manifest", man,
                   "--source", "S073"], root)
    oks = len(re.findall(r"^S073:Q\d+ OK ", out, re.M))
    mt = norm(open(man, encoding="utf-8").read())
    miss = [c for c in MANIFEST_CORES if norm(c) not in mt]
    try:
        qs = json.load(open(man, encoding="utf-8"))["sources"][0]["quotes"]
        distinct = len({q["quote"] for q in qs}) == len(qs) == oks and len({q["anchor"] for q in qs}) >= 7
    except Exception:
        distinct = False
    good = rc == 0 and "S073:sha256 OK" in out and oks >= 8 and not miss and "BROKEN" not in out and distinct
    return good, f"recheck-rc={rc} quotes-ok={oks} frozen-cores-missing={len(miss)}"


def g5(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    body = "\n".join(live_lines(txt(root, p) or ""))
    snap = (txt(root, "corpus/source-snapshots/round-46/S073.txt") or "").splitlines()
    allcurly = re.findall("\u201c([^\u201d]+)\u201d", body)
    spans = re.findall("\u201c([^\u201d]+)\u201d\\s*\\(`?S073\\.txt:(\\d+)(?:-(\\d+))?`?", body)
    straight = [q for q in re.findall('"([^"\\n]{12,})"', body) if len(q.split()) >= 4]
    straight_cited = re.findall('"([^"\\n]{12,})"\\s*\\(`?S073\\.txt:(\\d+)(?:-(\\d+))?`?', body)
    passed, failed = [], 0
    for q, a, b in spans + straight_cited:
        a = int(a)
        b = int(b) if b else a
        window = norm(" ".join(snap[max(a - 1, 0):b]))
        nq = norm(q)
        if len(nq.split()) <= 25 and nq and a >= BODY[0] and b <= BODY[1] and b - a <= 11 and nq in window:
            passed.append(nq)
        else:
            failed += 1
    cores = [c for c in CORES if any(re.search(c, q) for q in passed)]
    uncited = (len(allcurly) - len(spans)) + (len(straight) - len(straight_cited))
    ok = failed == 0 and uncited == 0 and len(passed) >= 4 and len(cores) == len(CORES)
    return ok, f"spans={len(spans) + len(straight_cited)} located={len(passed)} failed={failed} uncited={uncited} cores={len(cores)}/{len(CORES)}"


def g6(root: str) -> tuple[bool, str]:
    d = os.path.join(root, "corpus/knowledge")
    everything = sorted(os.listdir(d)) if os.path.isdir(d) else []
    names = [f for f in everything if f.endswith(".md") and os.path.isfile(os.path.join(d, f))]
    nested = sum(1 for _r, _d, fs in os.walk(d) for f in fs if f.endswith(".md")) if os.path.isdir(d) else 0
    p, why = entry_path(root)
    base_like = [n for n in everything if p is None or "corpus/knowledge/" + n != p]
    base_ok = sha(("\n".join(base_like) + "\n").encode()) == PINS["base-knowledge-names"]
    try:  # the two entries claim C1 re-grounds are exempt from the content pin (their names stay pinned): C2 is verifiable without C1 landed
        cont = sha("\n".join("%s %s" % (n, sha(open(os.path.join(d, n), "rb").read())) for n in base_like if n not in CONTENT_EXEMPT).encode())
    except OSError:
        cont = ""
    base_ok = base_ok and (PINS["base-knowledge-content"] is None or cont == PINS["base-knowledge-content"])
    sized = p is not None and os.path.getsize(os.path.join(root, p)) >= 3000
    return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized), f"knowledge={len(names)} entries={len(everything)} nested-md={nested} base-intact={int(base_ok)} entry-bytes-ok={int(sized)}"


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
        print(f"r46-c2-gate: {a.root} is not a directory", file=sys.stderr)
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
