#!/usr/bin/env python3
"""R46bMutF29b — independent mutant battery for r46-f29-gate.py (round-46 attempt 2, seat R46bMutF29b).

Own mutant set (single-line edits of the frozen gate), graded against the positive tree and the
defect trees shipped in .ufo/waves/round-46/attempt2/controls/.  The lane's committed gate is never
written: every mutant is a scratch copy.  The original file's sha256 is printed before and after.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r46/R46bMutF29b"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
GATE_REL = "corpus/instruments/r46-f29-gate.py"
RECHECK_REL = "corpus/instruments/source-recheck.py"

DEFECTS = ["duprow", "fencedf29", "vjunk", "thinsection", "badnames", "row9cells",
           "thinscope", "kindcase", "manws", "fewquotes", "dupquote", "widespan",
           "longquote", "fewspans", "nestedmd", "entrymutant", "symlink"]
EXTRA = ["junk", "fabricated"]
TREES = ["positive"] + DEFECTS + EXTRA

# (id, limb, one-line old, one-line new, intent)
MUTANTS = [
    # ---- H1: frontier table -------------------------------------------------
    ("A1-live-lines-fence-dropped", "H1",
     '        if fence or not st or st.startswith("<!--"):',
     '        if not st or st.startswith("<!--"):',
     "drop the fence conjunct of live_lines: fenced content becomes live text"),
    ("A2-entry-cell-dropped", "H1",
     "    if ENTRY not in f29[0][3]:",
     "    if False:",
     "drop the F29 entry-cell conjunct"),
    ("A3-entry-shared-dropped", "H1",
     "    if shared:",
     "    if False:",
     "drop the entry-shared-with-other-rows clause"),
    ("A4-one-live-row-loosened", "H1",
     "    if len(raw) != 1:",
     "    if len(raw) < 1:",
     "loosen the one-live-F29-row clause to >= 0"),
    ("A5-s074-boundary-widened", "H1",
     're.search(r"\\bS074\\b", f29[0][4])',
     're.search(r"\\bS074\\d?\\b", f29[0][4])',
     "widen the F29 sources-cell regex to also accept S0740"),
    # ---- H2: entry shape ----------------------------------------------------
    ("B1-verified-at-prefix", "H2",
     '    ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)',
     '    ok_v = any(h.startswith("verified-at: " + VERIFIED_AT) for h in head)',
     "relax verified-at from exact equality to prefix"),
    ("B2-xref-need-dropped", "H2",
     "    ok_x = need <= have and refok == len(refs)",
     "    ok_x = refok == len(refs)",
     "drop the required-xref-name conjunct"),
    ("B3-table-rows-floor", "H2",
     "and len(rows) >= 6 and ok_x and anchored",
     "and len(rows) >= 5 and ok_x and anchored",
     "lower the >=6-row table floor to 5"),
    ("B4-recheck-count-loosened", "H2",
     'ok_r = sum(1 for ln in body.splitlines() if ln.startswith("recheck:")) == 1 and any(RECHECK_LINE.match(h) for h in head)',
     'ok_r = sum(1 for ln in body.splitlines() if ln.startswith("recheck:")) >= 1 and any(RECHECK_LINE.match(h) for h in head)',
     "loosen exactly-one-recheck-line to at-least-one"),
    ("B5-cell-word-floor", "H2",
     'if all(len(re.findall(r"\\w+", c)) >= 2 for c in cells[1:])',
     'if all(len(re.findall(r"\\w+", c)) >= 1 for c in cells[1:])',
     "lower the per-cell word floor from 2 to 1"),
    # ---- H3: SOURCES.md registry row ---------------------------------------
    ("C1-scope-words-floor", "H3",
     'if len(re.findall(r"\\w+", row[4])) < 8: bad.append("scope-words")',
     'if len(re.findall(r"\\w+", row[4])) < 3: bad.append("scope-words")',
     "lower the scope-cell word floor from 8 to 3"),
    ("C2-kind-literal-case", "H3",
     'if row[2] != "docs": bad.append("kind")',
     'if row[2] != "Docs": bad.append("kind")',
     "swap the kind literal to the wrong case"),
    ("C3-tier-literal", "H3",
     'if row[3] != "A": bad.append("tier")',
     'if row[3] != "B": bad.append("tier")',
     "swap the tier literal"),
    ("C4-url-equality-dropped", "H3",
     'if not u or u[0].rstrip(".,;)") != URL: bad.append("url")',
     'if not u: bad.append("url")',
     "drop the URL equality check"),
    ("C5-anchor-locator-range", "H3",
     "not (BODY[0] <= int(loc.group(1)) <= int(loc.group(2)) <= SNAP_LINES)",
     "not (BODY[0] <= int(loc.group(1)) <= int(loc.group(2)))",
     "drop the upper bound of the anchor line locator"),
    # ---- H4: capture / manifest --------------------------------------------
    ("D1-manifest-pin-dropped", "H4",
     'if sha(open(man, "rb").read()) != PINS["manifest.json"]:',
     "if False:",
     "drop the manifest bytes pin"),
    ("D2-recheck-pin-dropped", "H4",
     'if sha(rcb) != PINS["source-recheck.py"]:',
     "if False:",
     "drop the source-recheck.py bytes pin"),
    ("D3-quote-count-floor", "H4",
     'good = rc == 0 and "S074:sha256 OK" in out and oks >= 8 and not miss',
     'good = rc == 0 and "S074:sha256 OK" in out and oks >= 1 and not miss',
     "lower the >=8 verified-quote floor to 1"),
    ("D4-sha-ok-conjunct-dropped", "H4",
     'good = rc == 0 and "S074:sha256 OK" in out and oks >= 8 and not miss and "BROKEN" not in out and distinct',
     'good = rc == 0 and oks >= 8 and not miss and "BROKEN" not in out and distinct',
     "drop the S074:sha256 OK conjunct"),
    # ---- H5: entry citations ------------------------------------------------
    ("E1-span-width", "H5",
     "and b - a <= 11 and nq in window",
     "and b - a <= 41 and nq in window",
     "widen the cited-span width from 12 to 42 lines"),
    ("E2-word-cap", "H5",
     "if len(nq.split()) <= 25 and nq and",
     "if len(nq.split()) <= 250 and nq and",
     "widen the 25-word quote cap"),
    ("E3-core-count", "H5",
     "len(passed) >= 4 and len(cores) == len(CORES)",
     "len(passed) >= 4 and len(cores) >= len(CORES) - 1",
     "allow one of the five frozen cores to be missing"),
    ("E4-passed-floor", "H5",
     "and len(passed) >= 4 and len(cores) == len(CORES)",
     "and len(passed) >= 1 and len(cores) == len(CORES)",
     "lower the >=4 located-span floor to 1"),
    ("E5-uncited-tolerance", "H5",
     "ok = failed == 0 and uncited <= 0 and",
     "ok = failed == 0 and uncited <= 2 and",
     "tolerate two uncited quotes"),
    # ---- H6: knowledge directory -------------------------------------------
    ("F1-entry-size-floor", "H6",
     'sized = os.path.getsize(os.path.join(root, p)) >= 3000',
     'sized = os.path.getsize(os.path.join(root, p)) >= 100',
     "lower the entry size floor from 3000 to 100 bytes"),
    ("F2-content-pin-dropped", "H6",
     'base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok',
     "base_ok = base_ok and ledger_ok",
     "drop the pinned-content hash conjunct"),
    ("F3-nested-count", "H6",
     "and len(everything) == 66 and nested == 66 and base_ok",
     "and len(everything) == 66 and nested >= 66 and base_ok",
     "loosen the nested-md count to >= 66"),
    ("F4-symlink-clause-dropped", "H6",
     "and sized and not links,",
     "and sized and True,",
     "drop the no-symlinks conjunct of H6"),
    # ---- H7: census ---------------------------------------------------------
    ("G1-symlink-guard-dropped", "H7",
     'if os.path.islink(os.path.join(root, "corpus")) or os.path.islink(os.path.join(root, "corpus/SOURCES.md")):',
     "if False:",
     "drop the census-input symlink guard"),
    ("G2-ok-line-tab-dropped", "H7",
     'ok_line = bool(re.search(r"^\\S+\\tok\\t", p.stdout, re.M))',
     'ok_line = bool(re.search(r"^\\S+\\tok", p.stdout, re.M))',
     "drop the trailing tab from the census ok-line pattern"),
    ("G3-verdict-or", "H7",
     'return p.returncode == 0 and ok_line, "census-rc=%d ok-line=%d"',
     'return p.returncode == 0 or ok_line, "census-rc=%d ok-line=%d"',
     "swap and->or in the census verdict"),
    # ---- controls -----------------------------------------------------------
    ("Z0-do-nothing-whitespace", "H1",
     "    if len(raw) != 1:",
     "    if len(raw) != 1 :",
     "CONTROL: whitespace-only edit, must be behaviour-identical"),
    ("Z1-do-nothing-comment", "H6",
     'LEDGER = "considerthese-proposals-ledger.md"',
     'LEDGER = "considerthese-proposals-ledger.md"  # control',
     "CONTROL: comment-only edit, must be behaviour-identical"),
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_gate(gate: str, tree: str) -> tuple[str, str, str]:
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(S, "tmp")
    p = subprocess.run([sys.executable, gate, "--root", os.path.join(S, "trees", tree),
                        "--work", os.path.join(S, "work")],
                       capture_output=True, text=True, env=env, timeout=600)
    return p.stdout, p.stderr, p.returncode


def limbs(out: str) -> dict:
    d = {}
    for m in re.finditer(r"^gate (H\d) pass=(\d) read=(.*)$", out, re.M):
        d[m.group(1)] = (int(m.group(2)), m.group(3))
    fixed = re.search(r"f29-gate fixed=(\d+)/7 exit=(\d+)", out)
    d["fixed"] = int(fixed.group(1)) if fixed else -1
    return d


def build_src0740() -> None:
    """Rebuild the defect tree the R50 receipt pairs with its H1 mutant (src0740), which the
    shipped controls/f29-defects.py cannot build."""
    dst = os.path.join(S, "trees", "src0740")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(S, "trees", "positive"), dst, symlinks=True)
    p = os.path.join(dst, "corpus/README.md")
    lines = open(p, encoding="utf-8").read().splitlines(keepends=True)
    for i, ln in enumerate(lines):
        if ln.startswith("| F29 |"):
            lines[i] = ln.replace("| S074 |", "| S0740 |", 1)
            break
    else:
        raise SystemExit("F29 row not found in src0740 build")
    open(p, "w", encoding="utf-8").write("".join(lines))


def main() -> int:
    os.makedirs(os.path.join(S, "mutants"), exist_ok=True)
    os.makedirs(os.path.join(S, "runs"), exist_ok=True)
    os.makedirs(os.path.join(S, "tmp"), exist_ok=True)
    os.makedirs(os.path.join(S, "work"), exist_ok=True)
    src = os.path.join(LANE, GATE_REL)
    pristine = open(src, "rb").read()
    base_sha = sha(pristine)
    print("# original gate sha256 (before) = %s" % base_sha)
    print("# original gate path = %s" % src)

    build_src0740()
    trees = TREES + ["src0740"]

    # baseline run (pristine copy, do-nothing control)
    bdir = os.path.join(S, "mutants", "BASE")
    os.makedirs(bdir, exist_ok=True)
    shutil.copy(src, os.path.join(bdir, "r46-f29-gate.py"))
    shutil.copy(os.path.join(LANE, RECHECK_REL), os.path.join(bdir, "source-recheck.py"))
    base = {}
    for t in trees:
        out, err, rc = run_gate(os.path.join(bdir, "r46-f29-gate.py"), t)
        base[t] = limbs(out)
        if err.strip():
            print("# BASE %s stderr: %s" % (t, err.strip()[:200]))
    print("# BASE positive read: %s" % (base["positive"].get("H1", (0, ""))[1],))
    for t in trees:
        print("# BASE %-12s fixed=%d %s" % (t, base[t]["fixed"],
              " ".join("%s=%d" % (h, base[t][h][0]) for h in ["H%d" % i for i in range(1, 8)])))

    results = []
    for mid, limb, old, new, intent in MUTANTS:
        d = os.path.join(S, "mutants", mid)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        text = pristine.decode()
        n = text.count(old)
        if n != 1:
            print("MUTANT %s ABORT: old string occurs %d times" % (mid, n))
            results.append((mid, limb, intent, None))
            continue
        mutated = text.replace(old, new, 1)
        gpath = os.path.join(d, "r46-f29-gate.py")
        open(gpath, "w", encoding="utf-8").write(mutated)
        shutil.copy(os.path.join(LANE, RECHECK_REL), os.path.join(d, "source-recheck.py"))
        m_sha = sha(open(gpath, "rb").read())
        row = {"id": mid, "limb": limb, "intent": intent, "sha": m_sha, "trees": {},
               "stderr": {}, "rc": {}}
        for t in trees:
            out, err, rc = run_gate(gpath, t)
            row["trees"][t] = limbs(out)
            if err.strip():
                row["stderr"][t] = err.strip()[:300]
        results.append(row)
        # classify
        pos = row["trees"]["positive"]["fixed"]
        flips = []
        full = []
        for t in trees:
            if t == "positive":
                continue
            b, m = base[t], row["trees"][t]
            f = [h for h in ["H%d" % i for i in range(1, 8)] if b[h][0] == 0 and m[h][0] == 1]
            if f:
                flips.append((t, ",".join(f)))
            if b["fixed"] < 7 and m["fixed"] == 7:
                full.append(t)
        print("MUTANT %-32s limb=%s sha=%s pos=%d/7 flips=%s full_false_green=%s"
              % (mid, limb, m_sha[:12], pos, flips if flips else "-", full if full else "-"))
        for t, e in row["stderr"].items():
            print("   stderr %s: %s" % (t, e))

    with open(os.path.join(S, "runs", "mutants.tsv"), "w", encoding="utf-8") as fh:
        for mid, limb, old, new, intent in MUTANTS:
            fh.write("%s\t%s\t%s\t%s\n" % (mid, limb, old.replace("\n", "\\n"), new.replace("\n", "\\n")))

    after = sha(open(src, "rb").read())
    print("# original gate sha256 (after)  = %s" % after)
    print("# original gate unchanged = %s" % (after == base_sha))
    print("# baseline tree fixed counts: %s" % ", ".join("%s=%d" % (t, base[t]["fixed"]) for t in trees))
    return 0


if __name__ == "__main__":
    sys.exit(main())
