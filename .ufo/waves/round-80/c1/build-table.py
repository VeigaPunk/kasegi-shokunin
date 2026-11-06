#!/usr/bin/env python3
"""build-table.py — round-80 C1 mutant table (28 rows) for the frozen candidate.

The nineteen round-79 rows are carried with the same transform on the round-80 bytes
(seven re-anchored where the round-80 edits changed the anchor text: K-M4, K-M5, K-W1,
K-P1, K-P2, K-NP, K-CL); nine rows are new — the round-79 routed real-gap survivors
(MutC1Hunt N10, N11, N21, N25, N26, N27, N30; ReviewEquiv half-B T1, T2).
Every row's anchor must occur exactly once in the candidate (checked here, exit 1 if not).
Usage: python3 build-table.py <candidate.py> <out.json>
"""
import json
import sys

OLD = ".ufo/waves/round-79/c1/mutant-table.json"
REANCHOR = {
    "K-M4": ("    return neg_ok is False and neg_ret_ok is False\n",
             "    return neg_ok is True and neg_ret_ok is False\n",
             "negpolarity predicate inverted -> gate-predicates and gate-negpolarity FAIL"),
    "K-M5": ('        check("both-headers", both_headers_ok(match7, first7, rest7),\n'
             '              "got=%s want=%s first_ran=%s restoration_ran=%s"\n'
             '              % (counts_str(got7, want7), counts_str(want7, want7), first7, rest7))\n',
             "", "both-headers check deleted -> gate-checkids FAIL missing"),
    "K-W1": ('def wiring_findings(source):\n    """Findings over every check("<name>", <ok>, ...) call in source; [] means wired.\n',
             'def wiring_findings(source):\n    return []\n    """Findings over every check("<name>", <ok>, ...) call in source; [] means wired.\n',
             "wiring scanner neutered -> gate-predicates FAIL"),
    "K-P1": ("def predicates_ok(rows, expect):\n    return bool(rows) and len(rows) == expect and all(got == want for got, want in rows)",
             "def predicates_ok(rows, expect):\n    return True",
             "predicates_ok neutered -> gate-checkids FAIL side_logs"),
    "K-P2": ('check("gate-predicates", predicates_ok(rows, GATE_ROWS),',
             'check("gate-predicates", True,',
             "gate-predicates call neutered -> gate-wiring FAIL"),
    "K-NP": ('check("gate-negpolarity", gate_negpolarity_ok(neg_ok, neg_ret_ok),',
             'check("gate-negpolarity", True,',
             "gate-negpolarity call neutered -> gate-wiring FAIL"),
    "K-CL": ('def _pred_call(node, name):\n    """The call node when node is name(...) or consumed(<log>, name(...)); else None."""\n',
             'def _pred_call(node, name):\n    return node if isinstance(node, ast.Call) else None\n    """The call node when node is name(...) or consumed(<log>, name(...)); else None."""\n',
             "_pred_call neutered (any call is the predicate call) -> gate-predicates FAIL"),
}
NEW = [
    ("N10", "            return _pred_call(node.args[1], name)\n", "            return node\n",
     "consumed() recursion accepts any wrapped call -> gate-predicates FAIL (wrong_src row)"),
    ("N11", "            (predicates_ok([], 0), False), (predicates_ok([(True, True)], 2), False),\n",
     "            (predicates_ok([], 0), False),\n",
     "a gate-predicates row deleted -> gate-predicates FAIL rows=27 expect=28"),
    ("N21", '            counts["exit_other"] += 1\n', '            counts["exit1_foreign"] += 1\n',
     "exit_other bucket folded into exit1_foreign -> prefix-census FAIL"),
    ("N25", "all(log == [True] for log in side_logs)", "all(log == [True] for log in side_logs[:1])",
     "only the first side log consulted -> gate-predicates FAIL"),
    ("N26", "    return set(done) == set(required) and", "    return set(done) >= set(required) and",
     "done-superset accepted -> gate-predicates FAIL"),
    ("N27", "first_ran is True and rest_ran is False", "first_ran is True",
     "both-headers restoration limb dropped -> gate-predicates FAIL"),
    ("N30", "cwd=scratch, env=env,", "cwd=None, env=env,",
     "foreign cwd inherited -> prefix-census FAIL (fresh-cwd entry exits 1)"),
    ("T1", "gate_consume_ok(clean_ok, limb_log),", "gate_consume_ok(True, limb_log),",
     "gate-consume predicate argument neutered to a constant -> gate-wiring FAIL F4"),
    ("T2", '            ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)',
     '            True and "RECHECK-CWD-RESULT nonconformant" in out)',
     "RESULT limb ret conjunct neutered -> gate-negpolarity FAIL neg_ret_ok=True"),
]


def main(argv):
    src = open(argv[1], encoding="utf-8").read()
    rows = []
    for r in json.load(open(OLD, encoding="utf-8")):
        if r["id"] in REANCHOR:
            a, rep, exp = REANCHOR[r["id"]]
            r = {"id": r["id"], "anchor": a, "replacement": rep, "class": r["class"], "expect": exp}
        rows.append(r)
    for rid, a, rep, exp in NEW:
        rows.append({"id": rid, "anchor": a, "replacement": rep, "class": "assertion", "expect": exp})
    bad = [r["id"] for r in rows if src.count(r["anchor"]) != 1]
    with open(argv[2], "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
        fh.write("\n")
    print("TABLE rows=%d not_unique=%s" % (len(rows), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
