#!/usr/bin/env python3
"""H-mutant table for r46-f29-gate.py, derived by analogy with the committed C2 battery
(r46-mutbat.py C2_MUTANTS G1a..G7c): the same clause-weakening shape, retargeted at the
f29 gate's own literals (29 rows / S074 / 2026-10-29 / 11 cells / 66 entries / 25 words).
Each entry asserts the old substring occurs EXACTLY ONCE in the gate."""
import json, os, sys

GATE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py"

MUTANTS = [
 ("H1a-counts-loose",
  'if len(rows) != 29 or adm != 29 or dup:',
  'if len(rows) < 29 or adm < 29:'),
 ("H1b-raw-loose",
  'if len(raw) != 1:',
  'if len(raw) < 1:'),
 ("H1c-src-boundary",
  'not re.search(r"\\bS074\\b", f29[0][4])',
  'not re.search(r"S074", f29[0][4])'),
 ("H2a-verified-loose",
  'ok_v = any(h == "verified-at: " + VERIFIED_AT for h in head)',
  'ok_v = any(h.startswith("verified-at: " + VERIFIED_AT) for h in head)'),
 ("H2b-wordfloor-low",
  '(12 if sct.startswith("## Falsifiable") else 25)',
  '(1 if sct.startswith("## Falsifiable") else 5)'),
 ("H2c-need-empty",
  'need = {"github-private-vulnerability-reporting.md", "cna-assignment-and-vulnerability-rules.md"}',
  'need = set()'),
 ("H3a-cells-loose",
  'if len(c) == 11:',
  'if len(c) >= 9:'),
 ("H3b-scope-low",
  'if len(re.findall(r"\\w+", row[4])) < 8: bad.append("scope-words")',
  'if len(re.findall(r"\\w+", row[4])) < 2: bad.append("scope-words")'),
 ("H3c-kind-dead",
  'if row[2] != "docs": bad.append("kind")',
  'if row[2] != "Docs": bad.append("kind")'),
 ("H4a-manifest-unpinned",
  'if sha(open(man, "rb").read()) != PINS["manifest.json"]:',
  'if False:'),
 ("H4b-quotes-low",
  'oks >= 8 and not miss',
  'oks >= 1 and not miss'),
 ("H4c-distinct-dropped",
  'and "BROKEN" not in out and distinct',
  'and "BROKEN" not in out'),
 ("H5a-span-wide",
  'b - a <= 11',
  'b - a <= 110'),
 ("H5b-words-wide",
  'len(nq.split()) <= 25',
  'len(nq.split()) <= 250'),
 ("H5c-pass-low",
  'len(passed) >= 4',
  'len(passed) >= 1'),
 ("H6a-counts-loose",
  'len(names) == 66 and len(everything) == 66 and nested == 66 and base_ok and sized and not links',
  'base_ok and sized and not links'),
 ("H6b-pin-dropped",
  'base_ok = base_ok and cont == PINS["base-knowledge-content"] and ledger_ok',
  'base_ok = base_ok and ledger_ok'),
 ("H6c-size-low",
  'os.path.getsize(os.path.join(root, p)) >= 3000',
  'os.path.getsize(os.path.join(root, p)) >= 3'),
 ("H7a-verdict-or",
  'return p.returncode == 0 and ok_line,',
  'return p.returncode == 0 or ok_line,'),
 ("H7b-symlink-dead",
  'return False, "census-input-is-a-symlink"',
  'pass  # mutant H7b'),
 ("H7c-okline-loose",
  're.search(r"^\\S+\\tok\\t", p.stdout, re.M)',
  're.search(r"^\\S+\\tok", p.stdout, re.M)'),
]

def main():
    text = open(GATE, encoding="utf-8").read()
    out = {}
    for mid, old, new in MUTANTS:
        n = text.count(old)
        if n != 1:
            print("DRIFT %s: old substring occurs %d times" % (mid, n)); sys.exit(2)
        out[mid] = (old, new)
    json.dump(out, open(os.path.join(sys.argv[1], "mutants.json"), "w"), indent=1)
    print("mutants=%d all-old-substrings-unique" % len(out))

main()
