#!/usr/bin/env python3
"""r46-f29-gate.py — round-46 (attempt 2) C2 counter (coverage), v1.

WHAT IT MEASURES
    One frontier move, F29 (GitHub repository security advisories — the maintainer-side
    advisory lifecycle: draft advisory, private fork, CVE request through GitHub as CNA,
    credit, publication and fix-version duty; row S074, capture
    `corpus/source-snapshots/round-46-a2/S074.txt`), counted through seven limbs that a
    junk row, a sourceless row or an entry quoting text the source does not hold cannot
    satisfy. The entry and row bytes are NOT pinned (they do not exist at freeze); the
    limbs grade structure and located quotes, and the non-author closure re-opens the page.
    The reporter-side flow stays F28 (`github-private-vulnerability-reporting.md`); this
    gate requires the entry to state that contrast, not absorb it.

    H1  frontier table: exactly 29 rows and 29 `admitted` (status = third cell), no
        duplicate ids, row F29 admitted, its sources cell names S074, its entry cell names
        exactly ENTRY and that path exists under --root, shared with no other row.
    H2  that entry opens with the provenance trio (`source: S074 — <canonical URL> — `,
        `verified-at: 2026-10-29`, and exactly one `recheck:` line of the exact form
        `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
        corpus/source-snapshots/round-46-a2/manifest.json --source S074`); carries the four
        sections of the round-45 entry shape (## Scope and decision rule, ## Overlap and
        novelty, ## Limits, ## Falsifiable package rule), each with real content (>= 25
        words, the package rule >= 12); a >= 6-row table whose cells each hold >= 2 words
        and whose cites lie inside the snapshot body (lines 1-42); cross-references
        corpus/knowledge/github-private-vulnerability-reporting.md and
        corpus/knowledge/cna-assignment-and-vulnerability-rules.md in range.
    H3  SOURCES.md row S074 under `## Registry` only: 11 cells, kind docs, tier A, status
        `mined`, opened 2026-10-29, the FIRST URL of the source cell is the canonical URL,
        scope and teaches >= 8 words, a cadence or date in the recheck cell, an anchor cell
        naming the capture, its sha256, and a line locator inside lines 1-42, `used-by`
        naming the entry.
    H4  capture: this lane's source-recheck.py exits 0 on manifest S074 (sha256 OK and
        >= 8 quotes OK), the S074 record's quote texts are pairwise distinct with >= 7
        distinct anchors, and the five frozen cores sit inside those quote records.
    H5  entry citations: every quoted span anywhere in the file (curly, or ASCII/
        single-curly of >= 4 words, comments and fences included) is followed by a
        backticked `S074.txt:N[-M]` citation located (whitespace/markup-normalised) in
        snapshot lines N..M, inside the body (1-42), spanning <= 12 lines and <= 25 words;
        at least four pass and the five frozen cores each appear inside a located span
        that is live text.
    H6  `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 66, the directory holds
        nothing else (no non-md file, no nested .md, no symlink); the other 65 names are
        the freeze tip's; 64 of them are pinned byte for byte — the considerthese ledger is
        exempt from the content pin (its name is pinned, its size may grow never shrink, so
        the ledger dispositions append does not couple with this claim).
    H7  `sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0 (corpus/ and
        SOURCES.md are not symlinks). The census script lives at the fleet root, outside
        the lane: this limb depends on it.

    READ-ONLY on --root; scratch under --work / TMPDIR; never runs git; stdlib only.

USAGE
    python3 corpus/instruments/r46-f29-gate.py --root TREE [--work DIR]
OUTPUT
    one `gate H<n> pass=0|1 read=<token>` line each, then
    `f29-gate fixed=<k>/7 exit=0|1`
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

SELF = os.path.realpath(__file__)
INSTRUMENTS = os.path.dirname(SELF)
LANE_CD = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
URL = "https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories"
VERIFIED_AT = "2026-10-29"
ENTRY = "corpus/knowledge/github-repository-security-advisories.md"
SNAP_REL = "corpus/source-snapshots/round-46-a2/S074.txt"
MAN_REL = "corpus/source-snapshots/round-46-a2/manifest.json"
BODY = (1, 42)
SNAP_LINES = 42
LEDGER = "considerthese-proposals-ledger.md"
LEDGER_MIN_BYTES = 30696  # the ledger's byte size at the freeze tip; it may grow, never shrink

PINS = {
    "S074.txt": "1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039",
    "manifest.json": "46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f",
    "source-recheck.py": "fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003",
    "base-knowledge-names": "b8facde108c5adb61b1cca7d561e87811e85c5220670fdced4ae0ca660b94057",
    "base-knowledge-content": "4db2b6a5a2d58a0818285a97e8ad7dad288ec44ffe20568323122630f86ad273",
}

RECHECK_LINE = re.compile(
    r"^recheck: cd " + re.escape(LANE_CD) + r" && python3 corpus/instruments/source-recheck\.py --manifest "
    + re.escape(MAN_REL) + r" --source S074(?: +#[ 0-9A-Za-z./_-]+)?$")  # the comment is a cadence note only: no shell metacharacters
SECTIONS = ["## Scope and decision rule", "## Overlap and novelty", "## Limits", "## Falsifiable package rule"]
CORES = [
    r"privately discuss and fix a security vulnerability",
    r"temporary private fork",
    r"authorized to assign CVE identification numbers",
    r"reviews the request within 72 hours",
    r"add a fix version to a security advisory prior to publishing",
]
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(s: str) -> str:
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def live_lines(text: str) -> list[str]:
    out = []
    fence = False
    for ln in text.splitlines():
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence or not st:
            continue
        clean = re.sub(r"<!--.*?-->", " ", ln)  # mid-line HTML comments are not rendered text
        clean = clean.strip()
        if not clean or clean.startswith("<!--"):
            continue
        out.append(clean)
    return out


def txt(root: str, rel: str) -> str | None:
    p = os.path.join(root, rel)
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def frontier(root: str) -> list[list[str]]:
    rows = []
    for ln in live_lines(txt(root, "corpus/README.md") or ""):
        st = ln.lstrip()
        if re.match(r"^\| F\d+ \|", st):
            cells = [c.strip() for c in st.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def frontier_anywhere(root: str) -> int:
    """Lines anywhere in the README bytes (fence-stripped, zero-width chars removed) that look like an F-row.
    The strict parsed count must equal this: a duplicate, indented, commented or zero-width-disguised row is a defect."""
    n = 0
    for ln in live_lines(txt(root, "corpus/README.md") or ""):
        clean = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", ln)
        if re.search(r"\| *F\d+ *\|", clean):
            n += 1
    return n


def entry_path(root: str) -> tuple[str | None, str]:
    if os.path.isfile(os.path.join(root, ENTRY)):
        return ENTRY, "entry-present"
    hits = [n for n in sorted(os.listdir(os.path.join(root, "corpus/knowledge")))
            if n.endswith(".md") and n != LEDGER and "advisor" in n] if os.path.isdir(os.path.join(root, "corpus/knowledge")) else []
    return None, "entry-absent advisor-named=%s" % ",".join(hits)


def sect_words(body: str, heading: str) -> int:
    m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return len(re.findall(r"\w+", m.group(1))) if m else 0


def h1(root: str) -> tuple[bool, str]:
    rows = frontier(root)
    ids = [r[0] for r in rows]
    adm = sum(1 for r in rows if len(r) > 2 and r[2] == "admitted")
    dup = len(ids) - len(set(ids))
    if len(rows) != 29 or adm != 29 or dup:
        return False, "rows=%d admitted=%d dup=%d" % (len(rows), adm, dup)
    p, why = entry_path(root)
    f29 = [r for r in rows if r[0] == "F29"]
    if not f29 or f29[0][2] != "admitted" or p is None:
        return False, "F29-row-or-entry-missing %s" % why
    if len(f29[0]) < 5 or not re.search(r"\bS074\b", f29[0][4]):
        return False, "F29-sources-cell-lacks-S074"
    if ENTRY not in f29[0][3] or f29[0][3].strip().strip("`") != ENTRY:
        return False, "F29-entry-cell-not-exactly-ENTRY"  # backticks are the lane's row decoration; the cell must name exactly this path
    shared = [r[0] for r in rows if len(r) > 3 and ENTRY in r[3] and r[0] != "F29"]
    if shared:
        return False, "entry-shared-with=%s" % ",".join(shared)
    raw = [ln for ln in live_lines(txt(root, "corpus/README.md") or "") if re.match(r"^\| F29 \|", ln.lstrip())]
    if len(raw) != 1:
        return False, "F29-row-not-one-live-line"
    anywhere = frontier_anywhere(root)
    if anywhere != len(rows):
        return False, "F-rows-visible=%d parsed=%d (duplicate, commented, indented or zero-width ghost rows)" % (anywhere, len(rows))
    return True, "rows=29 admitted=29 F29=admitted"


def h2(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    body = "\n".join(live_lines(txt(root, p) or ""))
    head = body.splitlines()[:8]
    ok_s = any(h.startswith("source: S074 \u2014 " + URL + " \u2014 ") for h in head)
    ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)
    ok_r = sum(1 for ln in body.splitlines() if ln.startswith("recheck:")) == 1 and any(RECHECK_LINE.match(h) for h in head)
    secs = sum(1 for sct in SECTIONS if re.search("^" + re.escape(sct) + r"\s*$", body, re.M))
    full = sum(1 for sct in SECTIONS if sect_words(body, sct) >= (12 if sct.startswith("## Falsifiable") else 25))
    rows = []
    for ln in body.splitlines():
        if re.match(r"^\|[^|]+\|[^|]+\|[^|]+\|\s*$", ln):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            cites = [int(x) for x in re.findall(r"S074\.txt:(\d+)", ln)]
            if all(len(re.findall(r"\w+", c)) >= 2 for c in cells[1:]) and cites and all(BODY[0] <= x <= BODY[1] for x in cites):
                rows.append(cells)
    refs = re.findall(r"corpus/knowledge/([A-Za-z0-9._-]+\.md):(\d+)(?:-(\d+))?", body)
    refok = 0
    for fn, ln, ln2 in [(r[0], r[1], r[2] or r[1]) for r in refs]:
        t = txt(root, "corpus/knowledge/" + fn)
        if t is not None and 1 <= int(ln) <= int(ln2) <= len(t.splitlines()):
            refok += 1
    need = {"github-private-vulnerability-reporting.md", "cna-assignment-and-vulnerability-rules.md"}
    have = {r[0] for r in refs}
    ok_x = need <= have and refok == len(refs)

    def sect(heading: str) -> str:
        m = re.search("^" + re.escape(heading) + r"\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
        return m.group(1) if m else ""

    anchored = (re.search(r"S074\.txt:\d+", sect(SECTIONS[0])) is not None
                and len(re.findall(r"corpus/knowledge/[A-Za-z0-9._-]+\.md:\d+", sect(SECTIONS[1]))) >= 2
                and re.search(r"S074\.txt:\d+|`(?:grep|sed) ", sect(SECTIONS[2])) is not None
                and re.search(r"S074\.txt:\d+", sect(SECTIONS[3])) is not None)
    good = ok_s and ok_v and ok_r and secs == len(SECTIONS) and full == len(SECTIONS) and len(rows) >= 6 and ok_x and anchored
    return good, ("source=%d verified-at=%d recheck=%d sections=%d/%d full=%d/%d table-rows=%d xrefs=%d/%d anchored=%d"
                  % (ok_s, ok_v, ok_r, secs, len(SECTIONS), full, len(SECTIONS), len(rows), refok, len(refs), anchored))


def h3(root: str) -> tuple[bool, str]:
    p, _ = entry_path(root)
    row = None
    hits = [ln for ln in live_lines(txt(root, "corpus/SOURCES.md") or "") if re.match(r"^ {0,3}\|\s*S074\s*\|", ln)]
    if len(hits) == 1:
        c = [x.strip() for x in hits[0].strip().strip("|").split("|")]
        if len(c) == 11:
            row = c
    if row is None:
        return False, "row-S074=absent-or-malformed-or-not-registry-only hits=%d" % len(hits)
    try:
        snap_sha = sha(open(os.path.join(root, SNAP_REL), "rb").read())
    except OSError:
        return False, "snapshot-absent"
    if snap_sha != PINS["S074.txt"]:
        return False, "snapshot-not-the-pinned-capture"
    bad = []
    if row[3] != "A": bad.append("tier")
    if row[2] != "docs": bad.append("kind")
    if len(re.findall(r"\w+", row[4])) < 8: bad.append("scope-words")
    if len(re.findall(r"\w+", row[6])) < 8: bad.append("teaches-words")
    if not re.fullmatch(r"(?:\d+d|on-release|\d{4}-\d{2}-\d{2})", row[9]): bad.append("recheck-cell")
    locs = re.finditer(r"(?:lines?|\bL)\s*(\d+)\s*[-\u2013]\s*L?(\d+)\s+of\s+(\S+)", row[5])
    ok_loc = any(m.group(3).rstrip(".,;)'\"") == SNAP_REL and BODY[0] <= int(m.group(1)) <= int(m.group(2)) <= SNAP_LINES
                 for m in locs)
    if SNAP_REL not in row[5] or not ok_loc: bad.append("anchor-locator")  # the locator must be bound to THIS capture's path
    if row[7] != "mined": bad.append("status")
    if row[8] != VERIFIED_AT: bad.append("opened")
    urls = [x.rstrip(".,;)") for x in re.findall(r"https?://\S+", row[1])]
    if not urls or any(x != URL for x in urls): bad.append("url")  # every URL in the source cell is the canonical one: no redirector wrap
    if p is None or p not in row[10]: bad.append("used-by")
    if snap_sha not in row[5]: bad.append("anchor-sha")
    return (not bad), ("row-S074=ok" if not bad else "bad=" + ",".join(bad))


def h4(root: str) -> tuple[bool, str]:
    man = os.path.join(root, MAN_REL)
    if not os.path.isfile(man):
        return False, "manifest-absent"
    if sha(open(man, "rb").read()) != PINS["manifest.json"]:
        return False, "manifest-not-the-pinned-bytes"
    rcb = open(os.path.join(INSTRUMENTS, "source-recheck.py"), "rb").read()
    if sha(rcb) != PINS["source-recheck.py"]:
        return False, "source-recheck-not-the-pinned-bytes"
    p2 = subprocess.run([sys.executable, "-I", os.path.join(INSTRUMENTS, "source-recheck.py"),
                         "--manifest", man, "--source", "S074"], capture_output=True, text=True, timeout=120)
    rc, out = p2.returncode, p2.stdout
    oks = len(re.findall(r"^S074:Q\d+ OK ", out, re.M))
    try:
        rec = [x for x in json.load(open(man, encoding="utf-8"))["sources"] if x.get("id") == "S074"]
        qs = rec[0]["quotes"] if len(rec) == 1 else []
        mt = norm(" ".join(q["quote"] for q in qs))
        distinct = len({q["quote"] for q in qs}) == len(qs) == oks and len({q["anchor"] for q in qs}) >= 7
    except Exception:
        mt, distinct = "", False
    miss = [c for c in CORES if not re.search(c, mt)]
    good = rc == 0 and "S074:sha256 OK" in out and oks >= 8 and not miss and "BROKEN" not in out and distinct
    return good, "recheck-rc=%d quotes-ok=%d frozen-cores-missing=%d" % (rc, oks, len(miss))


def h5(root: str) -> tuple[bool, str]:
    p, why = entry_path(root)
    if p is None:
        return False, why
    raw = txt(root, p) or ""
    live = "\n".join(live_lines(raw))
    snap = (txt(root, SNAP_REL) or "").splitlines()
    cite = r"\s*\(`?S074\.txt:(\d+)(?:-(\d+))?`?"
    curly = "\u201c([^\u201d]+)\u201d"
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
    return ok, "spans=%d located=%d failed=%d uncited=%d cores=%d/%d" % (len(spans), len(passed), failed, max(uncited, 0), len(cores), len(CORES))


def h6(root: str) -> tuple[bool, str]:
    d = os.path.join(root, "corpus/knowledge")
    everything = sorted(os.listdir(d)) if os.path.isdir(d) else []
    names = [f for f in everything if f.endswith(".md") and os.path.isfile(os.path.join(d, f))]
    nested = sum(1 for _r, _d, fs in os.walk(d) for f in fs if f.endswith(".md")) if os.path.isdir(d) else 0
    p, why = entry_path(root)
    if p is None:
        return False, why
    base_like = sorted(n for n in names if "corpus/knowledge/" + n != ENTRY)
    base_ok = sha(("\n".join(base_like) + "\n").encode()) == PINS["base-knowledge-names"]
    try:
        cont = sha("\n".join("%s %s" % (n, sha(open(os.path.join(d, n), "rb").read())) for n in base_like if n != LEDGER).encode())
        ledger_ok = os.path.getsize(os.path.join(d, LEDGER)) >= LEDGER_MIN_BYTES
    except OSError:
        cont, ledger_ok = "", False
    base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok
    sized = os.path.getsize(os.path.join(root, p)) >= 3000
    links = [x for x in (os.path.join(root, "corpus"), d) if os.path.islink(x)] + [n for n in everything if os.path.islink(os.path.join(d, n))]
    return (len(names) == 66 and len(everything) == 66 and nested == 66 and base_ok and sized and not links,
            "knowledge=%d entries=%d nested-md=%d base-intact=%d entry-bytes-ok=%d symlinks=%d" %
            (len(names), len(everything), nested, base_ok, sized, len(links)))


def h7(root: str) -> tuple[bool, str]:
    if os.path.islink(os.path.join(root, "corpus")) or os.path.islink(os.path.join(root, "corpus/SOURCES.md")):
        return False, "census-input-is-a-symlink"
    reg = sum(1 for ln in (txt(root, "corpus/SOURCES.md") or "").splitlines() if ln.strip() == "## Registry")
    if reg != 1:
        return False, "registry-sections=%d (exactly one expected; a duplicated Registry section is a structural corruption the census does not see)" % reg
    p = subprocess.run(["bash", CENSUS, "validate", "--file", os.path.join(root, "corpus/SOURCES.md")],
                       capture_output=True, text=True, timeout=120)
    ok_line = bool(re.search(r"^\S+\tok\t", p.stdout, re.M))
    return p.returncode == 0 and ok_line, "census-rc=%d ok-line=%d" % (p.returncode, int(ok_line))


GATES = [("H1", h1), ("H2", h2), ("H3", h3), ("H4", h4), ("H5", h5), ("H6", h6), ("H7", h7)]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if not os.path.isdir(a.root):
        print("f29-gate fixed=0/7 exit=1 (root-missing)")
        return 1
    fixed = 0
    for name, fn in GATES:
        try:
            ok, read = fn(a.root)
        except Exception as exc:  # a limb that raises is red, never green
            ok, read = False, "limb-error=%s" % type(exc).__name__
        print("gate %s pass=%d read=%s" % (name, int(bool(ok)), read))
        fixed += int(bool(ok))
    print("f29-gate fixed=%d/7 exit=%d" % (fixed, 0 if fixed == 7 else 1))
    return 0 if fixed == 7 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
