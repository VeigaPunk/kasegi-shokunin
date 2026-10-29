#!/usr/bin/env python3
"""r46-c2-gate.py — round-46 C2 counter (coverage), v1.3 (attempt-2 erratum E3: the considerthese ledger joins the
content-exempt set — its name stays pinned, its bytes may grow never shrink; v1.2's hardening (errata E1 and E2, see
.ufo/waves/round-46/counter-errata.md) is unchanged; v1 sha256 0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6).

WHAT IT MEASURES
    One frontier move, F28 (GitHub private vulnerability reporting, the reporter-side flow; row S073, capture
    `corpus/source-snapshots/round-46/S073.txt`), counted through seven limbs that a junk row, a sourceless row or an
    entry that quotes text the source does not hold cannot satisfy. The entry and row bytes are NOT pinned (they did
    not exist at freeze); the limbs grade structure and located quotes, and the non-author closure re-opens the page.

    G1  frontier table: exactly 28 rows and 28 `admitted` (status = third cell), no duplicate ids, row F28 admitted,
        its sources cell names S073, its entry cell names one `knowledge/*.md` path that exists under --root and is
        shared with no other row.
    G2  that entry opens with the provenance trio (`source: S073 — <canonical URL> — `, `verified-at: 2026-10-28`,
        and exactly one `recheck:` line of the exact form `cd <lane> && python3 corpus/instruments/source-recheck.py
        --manifest corpus/source-snapshots/round-46/manifest.json --source S073` plus an optional ` # comment`);
        carries the four sections of the round-45 entry shape, each with real content (>= 25 words, the package rule
        >= 12; Scope cites S073.txt, Overlap holds >= 2 corpus/knowledge file:line references, Limits cites S073.txt
        or a backticked sweep command, the package rule cites S073.txt); a >= 6-row table whose cells each hold >= 2
        words and whose cites lie inside the page body (lines 556-583); cross-references corpus/knowledge/<f>.md:N[-M]
        in range to linux-kernel-security-bugs-reporting-process.md and ai-assisted-finding-validation.md.
    G3  SOURCES.md row S073 under `## Registry` only: 11 cells, kind docs, tier A, status `mined`, opened 2026-10-28,
        the FIRST URL of the source cell is the canonical URL, scope and teaches >= 8 words, a cadence or date in the
        recheck cell, an anchor cell naming the capture, a line locator inside lines 556-589 and the snapshot sha256,
        `used-by` naming the entry.
    G4  capture: this lane's source-recheck.py exits 0 on manifest S073 (sha256 OK and >= 8 quotes OK), the S073
        record's quote texts are pairwise distinct with >= 7 distinct anchors, and the five frozen cores sit inside
        those quote records (not in a note field).
    G5  entry citations: every quoted span anywhere in the file (curly, or ASCII/single-curly of >= 4 words, comments
        and fences included) is followed by a backticked `S073.txt:N[-M]` citation located (whitespace/markup-normalised)
        in snapshot lines N..M, inside the page body (556-583), spanning <= 12 lines and <= 25 words; at least four pass
        and the five frozen cores each appear inside a located span that is live text.
    G6  `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 65, the directory holds nothing else (no non-md file,
        no nested .md, no symlink) and the other 64 names are the round-45 tip's; 61 of them are pinned byte for byte, and
        three entries are exempt from the byte pin (names pinned, size may grow never shrink): the two entries claim C1
        re-grounds, and the considerthese ledger, which the round-46 attempt-2 wave appends the dispositions to. So C2 is
        verifiable without C1 landed, without the ledger append, and the reverse.
    G7  `sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0 (corpus/ and SOURCES.md are not symlinks).
        The census script lives at the fleet root, outside the lane: this limb depends on it.

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
    "base-knowledge-content": "2c4ccfb65fdb5b727a3bc0c2465f6091b535663abd81126b81e76fdaae83a9a7",
    "base-knowledge-names": "bf3044814698b31b2d63a47ef6933cfe4d2d09635c2d717b05c8adf0bf719f5d",
}
if os.environ.get("R46_PINS_OVERRIDE"):  # selftests only: the grader's environment, never the graded tree's; a null value disables that one pin
    PINS.update(json.load(open(os.environ["R46_PINS_OVERRIDE"])))
CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md", "considerthese-proposals-ledger.md"}
EXEMPT_BASE_SIZE = {'claim-gates.md': 6742, 'claim-package-contract.md': 5169, 'considerthese-proposals-ledger.md': 30696}  # the exempt entries may grow (C1 appends; the round-46 attempt-2 wave appends the ledger dispositions) but never shrink: a gutted entry is red
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
RECHECK_LINE = re.compile(r"^recheck: cd " + re.escape(LANE) + r" && python3 corpus/instruments/source-recheck\.py --manifest corpus/source-snapshots/round-46/manifest\.json --source S073(?: +#.*)?$")
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
    if len(f27) < 5 or not re.search(r"\bS073\b", f27[4]):
        return False, "F28-sources-cell-lacks-S073"
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
    ok_r = sum(1 for ln in body.splitlines() if ln.startswith("recheck:")) == 1 and any(RECHECK_LINE.match(h) for h in head)
    secs = sum(1 for sct in SECTIONS if re.search("^" + re.escape(sct) + r"\s*$", body, re.M))
    full = sum(1 for sct in SECTIONS if sect_words(body, sct) >= (12 if sct.startswith("## Falsifiable") else 25))
    rows = []
    table_lines = 0
    for ln in body.splitlines():
        if re.match(r"^\s*\|", ln) and ln.count("|") >= 2:
            table_lines += 1
        if re.match(r"^\|[^|]+\|[^|]+\|[^|]+\|\s*$", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            cites = [int(x) for x in re.findall(r"S073\.txt:(\d+)", cells[1] + " " + cells[0])]
            if all(len(re.findall(r"\w+", c)) >= 2 for c in cells) and cites and all(BODY[0] <= x <= BODY[1] for x in cites):
                rows.append(cells)
    # every table-shaped line must be a header, a separator, or a counted row: a junk filler row is a defect even when
    # the real rows still clear the >=6 floor (the attempt-2 regression finding: v1.1 made junk rows not count but left them tolerated)
    accounted = 2 + len(rows)  # header + separator + counted rows
    junk = table_lines - accounted
    tbl = len(rows)
    refs = re.findall(r"corpus/knowledge/([A-Za-z0-9._-]+\.md):(\d+)(?:-(\d+))?", body)
    refok = 0
    for fn, ln, ln2 in [(r[0], r[1], r[2] or r[1]) for r in refs]:
        t = txt(root, "corpus/knowledge/" + fn)
        if t is not None and 1 <= int(ln) <= int(ln2) <= len(t.splitlines()):
            refok += 1
    refs = [(r[0], r[1]) for r in refs]
    need = {"linux-kernel-security-bugs-reporting-process.md", "ai-assisted-finding-validation.md"}
    have = {fn for fn, ln in refs}
    ok_x = need <= have and refok == len(refs)
    def sect(heading):
        m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
        return m.group(1) if m else ""
    anchored = (re.search(r"S073\.txt:\d+", sect(SECTIONS[0])) is not None
                and len(re.findall(r"corpus/knowledge/[A-Za-z0-9._-]+\.md:\d+", sect(SECTIONS[1]))) >= 2
                and re.search(r"S073\.txt:\d+|`(?:grep|sed) ", sect(SECTIONS[2])) is not None
                and re.search(r"S073\.txt:\d+", sect(SECTIONS[3])) is not None)
    good = ok_s and ok_v and ok_r and secs == len(SECTIONS) and full == len(SECTIONS) and tbl >= 6 and junk == 0 and ok_x and anchored
    return good, f"source={int(ok_s)} verified-at={int(ok_v)} recheck={int(bool(ok_r))} sections={secs}/{len(SECTIONS)} full={full}/{len(SECTIONS)} anchored={int(anchored)} table-rows={tbl} xrefs={refok}/{len(refs)}"


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
    loc = re.search(r"(?:lines?|\bL)\s*(\d+)\s*[-\u2013]\s*L?(\d+)", row[5])
    if "S073.txt" not in row[5] or not loc or not (BODY[0] <= int(loc.group(1)) <= int(loc.group(2)) <= 589): bad.append("anchor-locator")
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
    try:
        rec = [x for x in json.load(open(man, encoding="utf-8"))["sources"] if x.get("id") == "S073"]
        qs = rec[0]["quotes"] if len(rec) == 1 else []
        mt = norm(" ".join(q["quote"] for q in qs))
        distinct = len({q["quote"] for q in qs}) == len(qs) == oks and len({q["anchor"] for q in qs}) >= 7
    except Exception:
        mt, distinct = "", False
    miss = [c for c in MANIFEST_CORES if norm(c) not in mt]
    good = rc == 0 and "S073:sha256 OK" in out and oks >= 8 and not miss and "BROKEN" not in out and distinct
    return good, f"recheck-rc={rc} quotes-ok={oks} frozen-cores-missing={len(miss)}"


def g5(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    raw = txt(root, p) or ""
    live = "\n".join(live_lines(raw))
    snap = (txt(root, "corpus/source-snapshots/round-46/S073.txt") or "").splitlines()
    cite = "\\s*\\(`?S073\\.txt:(\\d+)(?:-(\\d+))?`?"
    curly = "\u201c([^\u201d]+)\u201d"
    # every quoted span anywhere in the raw file (comments and fences included) must be cited and located
    spans = re.findall(curly + cite, raw) + re.findall('"([^"]+)"' + cite, raw, re.S)
    single = re.findall("\u2018([^\u2019]+)\u2019", raw)
    quoted = re.findall(curly, raw) + [q for q in re.findall('"([^"]+)"', raw, re.S) if len(q.split()) >= 4] + [q for q in single if len(q.split()) >= 4]
    passed, failed = [], 0
    for q, a, b in spans:
        a = int(a)
        b = int(b) if b else a
        window = norm(" ".join(snap[max(a - 1, 0):b]))
        nq = norm(q)
        if len(nq.split()) <= 25 and nq and a >= BODY[0] and b <= BODY[1] and b - a <= 11 and nq in window:
            passed.append(nq)
        else:
            failed += 1
    live_spans = {norm(q) for q, _a, _b in re.findall(curly + cite, live)}
    cores = [c for c in CORES if any(re.search(c, q) for q in passed if q in live_spans)]
    uncited = len(quoted) - len(spans)
    ok = failed == 0 and uncited <= 0 and len(passed) >= 4 and len(cores) == len(CORES)
    return ok, f"spans={len(spans)} located={len(passed)} failed={failed} uncited={max(uncited, 0)} cores={len(cores)}/{len(CORES)}"


def g6(root: str) -> tuple[bool, str]:
    d = os.path.join(root, "corpus/knowledge")
    everything = sorted(os.listdir(d)) if os.path.isdir(d) else []
    names = [f for f in everything if f.endswith(".md") and os.path.isfile(os.path.join(d, f))]
    nested = sum(1 for _r, _d, fs in os.walk(d) for f in fs if f.endswith(".md")) if os.path.isdir(d) else 0
    p, why = entry_path(root)
    base_like = [n for n in everything if p is None or "corpus/knowledge/" + n != p]
    base_ok = sha(("\n".join(base_like) + "\n").encode()) == PINS["base-knowledge-names"]
    try:  # the three exempt entries (the two entries claim C1 re-grounds and the considerthese ledger the attempt-2 wave appends to) are exempt from the content pin (their names stay pinned): C2 is verifiable without C1 landed and without the ledger append
        cont = sha("\n".join("%s %s" % (n, sha(open(os.path.join(d, n), "rb").read())) for n in base_like if n not in CONTENT_EXEMPT).encode())
    except OSError:
        cont = ""
    base_ok = base_ok and (PINS["base-knowledge-content"] is None or cont == PINS["base-knowledge-content"])
    sized = p is not None and os.path.getsize(os.path.join(root, p)) >= 3000
    links = [x for x in (os.path.join(root, "corpus"), d) if os.path.islink(x)] + [n for n in everything if os.path.islink(os.path.join(d, n))]
    grown = all(os.path.isfile(os.path.join(d, n)) and os.path.getsize(os.path.join(d, n)) >= sz for n, sz in EXEMPT_BASE_SIZE.items())
    if links or not grown:
        return False, f"symlinks={len(links)} exempt-entries-not-shrunk={int(grown)}"
    return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized), f"knowledge={len(names)} entries={len(everything)} nested-md={nested} base-intact={int(base_ok)} entry-bytes-ok={int(sized)}"


def g7(root: str) -> tuple[bool, str]:
    if os.path.islink(os.path.join(root, "corpus")) or os.path.islink(os.path.join(root, "corpus/SOURCES.md")):
        return False, "census-input-is-a-symlink"
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
