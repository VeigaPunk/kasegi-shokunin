#!/usr/bin/env python3
"""r47-mutbat.py — round-47 mutation-battery runner (QUALITY R50/R53 pre-freeze falsification).

WHAT IT DOES
    Applies a frozen set of single-edit mutants to scratch copies of the round-47
    counters (`r47-routed-defects.py` c1, `r47-f30-gate.py` c2), runs the round-47
    selftest (`r47-counters-selftest.py`) against each mutant through `--gate`, and
    grades each mutant:

        caught      the selftest reports failures > 0 under the mutant while the
                    unmutated counter reads failures = 0 (baseline must be clean);
        equivalent  the mutant id carries a committed proof in --equivalent;
        uncaught    neither (a hole in the selftest's coverage — R50 requires this
                    to be 0 at the freeze, or the survivor is disclosed).

    Each mutant is a (id, old-substring, new-substring) triple; the edit is asserted
    to occur EXACTLY ONCE in the counter copy, so a drifted counter fails loudly
    instead of mutating the wrong line. The mutant copy lives in a scratch copy of
    the whole `corpus/instruments` dir so its sibling-instrument reads
    (`source-recheck.py`) keep resolving. Never runs git; stdlib only; scratch
    under --work (TMPDIR honoured).

    The selftest's fixture trees are the R53 tree-level false-green probes (markers
    kept, bound content removed, disguised or displaced); this battery adds the R50
    counter-mutant class. Receipts from both classes are committed under
    `.ufo/waves/round-47/controls/`.

USAGE
    python3 corpus/instruments/r47-mutbat.py --root TREE --base PURE_EXPORT \
        --work DIR [--counter c1|c2|both] [--equivalent MAP.json] [--list]
OUTPUT
    one `mutant=<id> baseline_failures=0 mutant_failures=<m> verdict=<v>` line per mutant, then
    `mutbat counter=<c> mutants=<n> caught=<k> equivalent=<e> uncaught=<u> baseline_failures=0 exit=0|1`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SELF = os.path.realpath(__file__)
INSTRUMENTS = os.path.dirname(SELF)
SELFTEST = "r47-counters-selftest.py"

# --- c1 mutant table: r47-routed-defects.py, >= 3 single-line edits per limb ------
C1_MUTANTS = [
    ("L1a-phrase0-only",   "hits = [p for p in SCAFFOLD_PHRASES if p in t]",  "hits = [p for p in SCAFFOLD_PHRASES[:1] if p in t]"),
    ("L1b-always-true",    'return not hits, ("scaffold-phrases=%d" % len(hits)) if hits else "scaffold-phrases=0"', 'return True, "scaffold-phrases=0"'),
    ("L1c-wrong-file",     '    t = txt(root, SOURCES) or ""\n    hits =',    '    t = txt(root, ENTRY) or ""\n    hits ='),
    ("L2a-fences-ignored", 'if fences:\n        bad.append("fence-markers=%d" % fences)', 'if False:\n        bad.append("fence-markers=%d" % fences)'),
    ("L2b-slbullet-loose", 'r"^- Repository security advisory lifecycle sweep \\(round 46 attempt 2, frontier F29\\); question:"', 'r"^- XXX"'),
    ("L2c-regbullet-loose", 'if not re.search(r"^- S074 row added: new row", reg, re.M):', 'if False:'),
    ("L2d-notebullet-loose", 'if not re.search(r"^- Capture directory note: `corpus/source-snapshots/round-46-a2/` exists beside", reg, re.M):', 'if False:'),
    ("L3b-content-true",   'ok = ("SOURCES.md" in tail) and ("fence" in tail) and ("Search log" in tail or "Registry changes" in tail)', 'ok = True'),
    ("L3c-third-clip-dropped", 'ok = ("SOURCES.md" in tail) and ("fence" in tail) and ("Search log" in tail or "Registry changes" in tail)', 'ok = ("SOURCES.md" in tail) and ("fence" in tail)'),
    ("L3d-return-true",    'return ok, "corrections-section-present content=%d" % int(ok)', 'return True, "corrections-section-present"'),
    ("L4a-phrases-empty",  'bad = [p for p in FALSE_PHRASES[:2] if p in t]',  'bad = []'),
    ("L4b-chrome-ignored", 'if not re.search(r"\\bchrome\\b", t):',             'if False:'),
    ("L4c-phrase1-only",   'bad = [p for p in FALSE_PHRASES[:2] if p in t]',  'bad = [p for p in FALSE_PHRASES[1:2] if p in t]'),
    ("L5a-order-ignored",  'if FALSE_PHRASES[2] in t:\n        return False, "order-phrase-still-present"', 'if False:\n        return False, "order-phrase-still-present"'),
    ("L5b-corrected-loose", 'if "CVE request before the fix-version" not in t:', 'if False:'),
    ("L5c-order-inverted", 'if FALSE_PHRASES[2] in t:\n        return False, "order-phrase-still-present"', 'if FALSE_PHRASES[2] not in t:\n        return False, "order-phrase-still-present"'),
    ("L6a-threecase-loose", 'if re.search(r"three cases[^.]*let a maintainer publish", t):', 'if False:'),
    ("L6b-twocase-loose",  'if "two cases" not in t:',                        'if False:'),
    ("L6c-forbid-loose",   'if "wait to disclose the issue when the fix is ready" not in t:', 'if False:'),
    ("L7a-one-name-only",  'if "R46bW2RevEntryClaims" in t and "R46bConnPatterns" in t and re.search(r"dropped|not carried|erratum", t, re.I):', 'if "R46bW2RevEntryClaims" in t and re.search(r"dropped|not carried|erratum", t, re.I):'),
    ("L7b-keyword-loose",  're.search(r"dropped|not carried|erratum", t, re.I)', 're.search(r".", t)'),
    ("L7c-keyword-invert", 're.search(r"dropped|not carried|erratum", t, re.I)', 're.search(r"XYZNOPE", t)'),
    ("L8a-supersede-loose", 'if not c[6].startswith("supersedes S074"):',     'if False:'),
    ("L8b-sha-loose",      'if "round-47/S076.txt" not in c[5] or "9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38" not in c[5]:', 'if "round-47/S076.txt" not in c[5]:'),
    ("L8c-recheck-ignored", 'if p2.returncode != 0 or "S076:sha256 OK" not in p2.stdout:', 'if False:'),
    ("L8d-cells-loose",    "if len(c) != 11:",                                "if len(c) < 9:"),
    ("L9a-oldcite-ignored", 'old = t.count("S074.txt:")\n    if old:',        'old = 0\n    if old:'),
    ("L9b-range-loose",    'if len(nq.split()) <= 25 and nq and rng[0] <= a <= b <= rng[1] and b - a <= 11 and nq in window:', 'if len(nq.split()) <= 25 and nq and nq in window:'),
    ("L9c-pass-low",       'ok = failed == 0 and uncited <= 0 and passed >= 20', 'ok = failed == 0'),
    ("L10a-url-loose",     'and "docs.github.com/en/rest/security-advisories" in ln]', 'and "docs.github.com" in ln]'),
    ("L10b-bullet-loose",  'if ln.lstrip().startswith("- ")',                 'if True'),
    ("L10c-url-invert",    'and "docs.github.com/en/rest/security-advisories" in ln]', 'and "docs.github.com/en/rest/security-advisories" not in ln]'),
    ("L11a-zdi-only",      'a = "ZDI" in t and "reservation" in t',           'a = "ZDI" in t'),
    ("L11b-precision-only", 'b = "S068" in t and "one GHSA advisory entry" in t', 'b = "S068" in t'),
    ("L11c-or-verdict",    'return a and b, "zdi-reservation=%d s068-precision=%d" % (int(a), int(b))', 'return a or b, "zdi-reservation=%d s068-precision=%d" % (int(a), int(b))'),
]

# --- c2 mutant table: r47-f30-gate.py, 3 per limb H1-H7 ---------------------------
C2_MUTANTS = [
    ("H1a-counts-loose",    "if len(rows) != 30 or adm != 30 or dup:",                        "if len(rows) < 30 or adm < 30 or dup:"),
    ("H1b-raw-loose",       "if len(raw) != 1:",                                              "if len(raw) > 1:"),
    ("H1c-src-boundary",    're.search(r"\\bS075\\b", f30[0][4])',                             're.search(r"S075", f30[0][4])'),
    ("H2a-verified-loose",  'ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)',    'ok_v = any(h.startswith("verified-at: " + VERIFIED_AT) for h in head)'),
    ("H2b-wordfloor-low",   '(12 if sct.startswith("## Falsifiable") else 25)',                '(1 if sct.startswith("## Falsifiable") else 5)'),
    ("H2c-need-empty",      'need = {"coordinated-disclosure-timelines.md", "vendor-third-party-finding-coordination.md"}', "need = set()"),
    ("H3a-cells-loose",     "if len(c) == 11:",                                               "if len(c) >= 9:"),
    ("H3b-scope-low",       'if len(re.findall(r"\\w+", row[4])) < 8: bad.append("scope-words")', 'if len(re.findall(r"\\w+", row[4])) < 2: bad.append("scope-words")'),
    ("H3c-kind-dead",       'if row[2] != "docs": bad.append("kind")',                         'if row[2] not in ("docs", "Docs"): bad.append("kind")'),
    ("H4a-manifest-unpinned", 'if sha(open(man, "rb").read()) != PINS["manifest.json"]:', "if False:"),
    ("H4b-quotes-low",      "oks >= 8 and not miss",                                          "oks >= 1 and not miss"),
    ("H4c-distinct-dropped", 'and \"BROKEN\" not in out and distinct',                         "and \"BROKEN\" not in out"),
    ("H5a-span-wide",       "b - a <= 11",                                                    "b - a <= 110"),
    ("H5b-words-wide",      "len(nq.split()) <= 25",                                          "len(nq.split()) <= 250"),
    ("H5c-pass-low",        "len(passed) >= 4",                                               "len(passed) >= 1"),
    ("H6a-counts-loose",    "len(names) == 67 and len(everything) == 67 and nested == 67",     "len(names) == 67 and len(everything) >= 67 and nested >= 67"),
    ("H6b-pin-dropped",     'base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok', "base_ok = base_ok and ledger_ok"),
    ("H6c-size-low",        'os.path.getsize(os.path.join(root, p)) >= 3000',                  'os.path.getsize(os.path.join(root, p)) >= 3'),
    ("H7a-verdict-or",      "p.returncode == 0 and ok_line",                                  "p.returncode == 0 or ok_line"),
    ("H7b-symlink-dead",    'return False, "census-input-is-a-symlink"',                       "pass  # mutant H7b"),
    ("H7c-okline-loose",    're.search(r"^\\S+\\tok\\t", p.stdout, re.M)',                     're.search(r"^\\S+\\tok", p.stdout, re.M)'),
]

COUNTER = {"c1": ("r47-routed-defects.py", C1_MUTANTS),
           "c2": ("r47-f30-gate.py", C2_MUTANTS)}


def run_selftest(pure: str, work: str, which: str, gate: str | None) -> tuple[int, str]:
    st = os.path.join(INSTRUMENTS, SELFTEST)
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-I", st, "--base", pure, "--work", work, "--counter", which]
    if gate:
        cmd += ["--gate", gate]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, cwd=work)
    m = re.findall(r"failures=(\d+)", p.stdout)
    return (int(m[-1]) if m else -1), p.stdout[-3000:]


def apply_mutant(src_counter: str, triple: tuple[str, str, str], dst_dir: str) -> str:
    mid, old, new = triple
    text = open(src_counter, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        raise SystemExit("mutant=%s old-substring occurs %d times (expected 1) — battery vs counter drift" % (mid, n))
    # the mutant copy lives in a scratch instruments dir so sibling reads keep resolving
    dst_inst = os.path.join(dst_dir, "instruments")
    shutil.copytree(INSTRUMENTS, dst_inst, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "r46-mutant-equivalents"))
    dst_counter = os.path.join(dst_inst, os.path.basename(src_counter))
    open(dst_counter, "w", encoding="utf-8").write(text.replace(old, new, 1))
    return dst_counter


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", required=True, help="PURE base export the selftest builds fixtures from")
    ap.add_argument("--work", required=True, help="scratch dir (mutant copies and selftest scratch live here)")
    ap.add_argument("--counter", default="both", choices=["c1", "c2", "both"])
    ap.add_argument("--equivalent", default=os.path.join(INSTRUMENTS, "r47-mutant-equivalents.json"),
                    help="JSON file mapping mutant id -> proof path")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        for which in ("c1", "c2"):
            for mid, old, new in COUNTER[which][1]:
                print("%s %s | %s => %s" % (which, mid, old[:60], new[:60]))
        return 0
    eq = {}
    if os.path.isfile(a.equivalent):
        eq = json.load(open(a.equivalent, encoding="utf-8"))
    os.makedirs(a.work, exist_ok=True)
    bad = 0
    for which in ("c1", "c2"):
        if a.counter not in ("both", which):
            continue
        cname, mutants = COUNTER[which]
        src_counter = os.path.join(INSTRUMENTS, cname)
        baseline, tail = run_selftest(a.base, os.path.join(a.work, "base-" + which), which, None)
        if baseline != 0:
            print("mutbat counter=%s BASELINE-DIRTY baseline_failures=%d" % (which, baseline))
            print(tail)
            bad += 1
            continue
        caught = equivalent = uncaught = 0
        for mid, old, new in mutants:
            mdir = tempfile.mkdtemp(prefix="mutbat-%s-" % which, dir=a.work)
            try:
                dst = apply_mutant(src_counter, (mid, old, new), mdir)
                mf, _ = run_selftest(a.base, os.path.join(mdir, "run"), which, dst)
            finally:
                shutil.rmtree(mdir, ignore_errors=True)
            if mf >= 1:
                caught += 1
                verdict = "caught"
            elif mid in eq and os.path.isfile(str(eq[mid])):
                equivalent += 1
                verdict = "equivalent"
            else:
                uncaught += 1
                verdict = "uncaught"
            print("mutant=%s baseline_failures=0 mutant_failures=%d verdict=%s" % (mid, mf, verdict))
        print("mutbat counter=%s mutants=%d caught=%d equivalent=%d uncaught=%d baseline_failures=0 exit=%d" %
              (which, len(mutants), caught, equivalent, uncaught, 0 if uncaught == 0 else 1))
        if uncaught:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
