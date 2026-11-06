#!/usr/bin/env python3
"""build-table.py — round-81 C1 mutant table for the frozen candidate.

The 28 round-80 rows are carried with the same anchor, replacement and class; each gains
`kill_cases`, the selftest case named after the arrow in its frozen round-80 `expect` prose
(declared there before any round-80 seat scored; never read off an observed run). 28 rows are
new: the round-80 routed real-gap survivors (ReviewC1 M1/M2; MutC1Hunt S01 S02 S04 S05 S07
S08 S09 S10 S11 S12 S13 S14 S15 S16 S19 S20 S21 S22 S25 S30 S31 S37 S39 S40 S41 S43), each
with the round-81 check meant to kill it. Three rows are neutral (semantics-preserving).
Every row's anchor must occur exactly once in the candidate (checked here, exit 1 if not).
Usage: python3 build-table.py <candidate.py> <out.json>
"""
import json
import sys

OLD = ".ufo/waves/round-80/c1/mutant-table.json"
OLD_KILL = {
    "K-M1": ["gate-regs"], "K-M2": ["gate-negpolarity"], "K-M3": ["gate-consume"],
    "K-M4": ["gate-predicates", "gate-negpolarity"], "K-M5": ["gate-checkids"],
    "K-X1": ["gate-consume"], "K-X2a": ["gate-predicates"], "K-X2b": ["gate-wiring"],
    "K-M8": ["gate-wiring", "gate-checkids"], "K-W1": ["gate-predicates"],
    "K-W2": ["gate-checkids"], "K-N1": ["gate-predicates"], "K-P1": ["gate-checkids"],
    "K-P2": ["gate-wiring"], "K-G1": ["gate-predicates"], "K-C1": ["gate-wiring"],
    "K-NP": ["gate-wiring"], "K-CL": ["gate-predicates"], "K-T1": ["tmpdir-refusal"],
    "N10": ["gate-predicates"], "N11": ["gate-predicates"], "N21": ["prefix-census"],
    "N25": ["gate-predicates"], "N26": ["gate-predicates"], "N27": ["gate-predicates"],
    "N30": ["prefix-census"], "T1": ["gate-wiring"], "T2": ["gate-negpolarity"],
}
BOOLOP = ("        if (isinstance(ok, ast.Constant) and ok.value is True) or (\n"
          "                isinstance(ok, ast.BoolOp)\n"
          "                and any(isinstance(v, ast.Constant) and v.value is True for v in ok.values)):\n")
NEW = [
    ("M1", "if tmp is not None and not os.path.isdir(tmp):",
     "if tmp is not None and not os.path.exists(tmp):", "tmpdir-file",
     "regular-file TMPDIR accepted by the guard -> tmpdir-file FAIL"),
    ("M2", "            return -1\n", "            return 0\n", "timeout-bucket",
     "timeout counted as exit 0 -> timeout-bucket FAIL"),
    ("S01", 'prefix = "cd %s && " % lane', 'prefix = "cd %s" % lane', "prefix-literal",
     "prefix loses its ' && ' -> prefix-literal FAIL"),
    ("S02", 'prefix = "cd %s && " % lane', 'prefix = "cd %s &&" % lane', "prefix-literal",
     "prefix loses its trailing space -> prefix-literal FAIL"),
    ("S04", 'conform = (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n               and',
     'conform = (counts["noprefix"] == 0\n               and', "conform-limbs",
     "conform drops the exit2_foreign conjunct -> conform-limbs FAIL"),
    ("S05", '               and counts["norecheck"] == 0 and counts["restoration_only"] == 0)',
     '               and counts["restoration_only"] == 0)', "conform-limbs",
     "conform drops the norecheck conjunct -> conform-limbs FAIL"),
    ("S37", '            if line.startswith("restoration-recheck:"):',
     '            if line.startswith("restoration"):', "conform-limbs",
     "restoration header prefix broadened -> conform-limbs FAIL"),
    ("S07", "def census(root, lane, verbose=False):", "def census(root, lane, verbose=True):",
     "output-lines", "census verbose by default -> output-lines FAIL"),
    ("S19", '                print("RESTORATION-ONLY %s" % name)\n', "                pass\n",
     "output-lines", "RESTORATION-ONLY line deleted -> output-lines FAIL"),
    ("S20", '                print("NORECHECK %s" % name)\n', "                pass\n",
     "output-lines", "NORECHECK line deleted -> output-lines FAIL"),
    ("S21", '            print("ENTRY %s noprefix=%d foreign_exit=%d" % (name, int(noprefix), code))\n',
     "            pass\n", "output-lines", "ENTRY line deleted -> output-lines FAIL"),
    ("S22", "        if verbose or noprefix or code == 2:\n", "        if verbose or noprefix:\n",
     "output-lines", "ENTRY drops the code == 2 clause -> output-lines FAIL"),
    ("S08", "    return clean_ok is True and limb_log == [True]\n",
     "    return clean_ok == True and limb_log == [True]\n", "gate-predicates",
     "gate_consume_ok identity -> equality -> gate-predicates FAIL"),
    ("S09", "    return clean_ok is True and limb_log == [True]\n",
     "    return clean_ok is True and limb_log[:1] == [True]\n", "gate-predicates",
     "limb_log truncated to its first element -> gate-predicates FAIL"),
    ("S10", "first_ran is True and rest_ran is False", "first_ran is True and not rest_ran",
     "gate-predicates", "both_headers rest_ran falsiness -> gate-predicates FAIL"),
    ("S41", "counts_match is True and first_ran is True and",
     "counts_match is True and first_ran == True and", "gate-predicates",
     "both_headers first_ran identity -> equality -> gate-predicates FAIL"),
    ("S40", "    return neg_ok is False and neg_ret_ok is False\n",
     "    return neg_ok is False and neg_ret_ok == False\n", "gate-predicates",
     "neg_ret_ok identity -> equality -> gate-predicates FAIL"),
    ("S11", "all(got == want for got, want in rows)",
     "all(bool(got) == bool(want) for got, want in rows)", "gate-predicates",
     "predicates_ok elements compared by truthiness -> gate-predicates FAIL"),
    ("S12", "bool(rows) and len(rows) == expect and", "bool(rows) and len(rows) >= expect and",
     "gate-predicates", "predicates_ok row count a lower bound -> gate-predicates FAIL"),
    ("S13", "    return set(done) == set(required) and all(log == [True] for log in side_logs)\n",
     "    return set(done) == set(required) and all(True in log for log in side_logs)\n",
     "gate-predicates", "side log membership instead of exact log -> gate-predicates FAIL"),
    ("S14", BOOLOP, "        if (isinstance(ok, ast.Constant) and ok.value is True):\n",
     "gate-predicates", "F1 BoolOp limb deleted -> gate-predicates FAIL"),
    ("S16", "and any(isinstance(v, ast.Constant) and v.value is True for v in ok.values)",
     "and all(isinstance(v, ast.Constant) and v.value is True for v in ok.values)",
     "gate-predicates", "F1 BoolOp operand quantifier any -> all -> gate-predicates FAIL"),
    ("S15", "if any(isinstance(a, ast.Constant) for a in call.args):",
     "if any(isinstance(a, ast.Constant) and a.value is True for a in call.args):",
     "gate-predicates", "F4 narrowed to constant True -> gate-predicates FAIL"),
    ("S43", "        if node.func.id == name:\n", "        if node.func.id.lower() == name.lower():\n",
     "gate-predicates", "case-insensitive predicate match -> gate-predicates FAIL"),
    ("S25", "if tmp is not None and not os.path.isdir(tmp):", "if not os.path.isdir(tmp):",
     "tmpdir-unset", "None guard dropped (TypeError on unset TMPDIR) -> tmpdir-unset FAIL"),
    ("S30", "                  file=sys.stderr)\n            return 2\n",
     "                  file=sys.stderr)\n            return 0\n", "usage-guards",
     "usage error exits 0 -> usage-guards FAIL"),
    ("S31", '        raise SystemExit("recheck-cwd: no corpus/knowledge under %s" % root)',
     '        print("recheck-cwd: no corpus/knowledge under %s" % root)', "usage-guards",
     "missing-corpus guard prints instead of exiting -> usage-guards FAIL"),
    ("S39", "    counts = census(os.path.abspath(root), lane, verbose)",
     "    counts = census(os.path.abspath(root), root, verbose)", "usage-guards",
     "main passes root where lane belongs -> usage-guards FAIL"),
]
NEUTRAL = [
    ("NT1", "#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n# mutbat neutral row: a comment line\n",
     "comment line after the shebang (moves every later line by one)"),
    ("NT2", '    def counts_str(counts, want):\n        return ",".join("%s=%d" % (k, counts[k]) for k in sorted(want))',
     '    def counts_str(cnt, want):\n        return ",".join("%s=%d" % (k, cnt[k]) for k in sorted(want))',
     "local parameter renamed counts -> cnt (AST changes, behaviour does not)"),
    ("NT3", "TIMEOUT = 120\n", "TIMEOUT = 120  # seconds\n", "trailing comment on a constant"),
]


def main(argv):
    src = open(argv[1], encoding="utf-8").read()
    rows = []
    for r in json.load(open(OLD, encoding="utf-8")):
        rows.append({"id": r["id"], "anchor": r["anchor"], "replacement": r["replacement"],
                     "class": r["class"], "kill_cases": OLD_KILL[r["id"]], "expect": r["expect"]})
    for rid, a, rep, case, exp in NEW:
        rows.append({"id": rid, "anchor": a, "replacement": rep, "class": "assertion",
                     "kill_cases": [case], "expect": exp})
    for rid, a, rep, exp in NEUTRAL:
        rows.append({"id": rid, "anchor": a, "replacement": rep, "class": "neutral", "expect": exp})
    bad = [r["id"] for r in rows if src.count(r["anchor"]) != 1]
    with open(argv[2], "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
        fh.write("\n")
    print("TABLE rows=%d neutral=%d not_unique=%s" % (len(rows), len(NEUTRAL), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
