#!/usr/bin/env python3
"""MutC1Hunt — beyond-table mutation hunt on the r79 C1 candidate (read-only on the lane).

Detector (same bounded behavioral detector for pristine, mutants, composites, r78 receipt):
    TMPDIR=<scratch> python3 -B <file> --selftest
Verdicts per seat spec: KILLED (rc != 0, FAIL line, no Traceback) / DIRTY / SURVIVED (rc 0).
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
TARGET = LANE + "/.ufo/waves/round-79/c1/recheck-cwd-census.py"
TABLE = LANE + "/.ufo/waves/round-79/c1/mutant-table.json"
OUT = LANE + "/.ufo/waves/round-79/w1/MutC1Hunt"
S = "/fast/scratch/hyaku/kasegi-r79/MutC1Hunt"
R78 = LANE + "/.ufo/waves/round-78/w1/successor/recheck-cwd-census.py"
R78_KX2 = LANE + "/.ufo/waves/round-78/w1/successor/mutants/K-X2.py"
EXPECT_SHA = "eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f"

FAIL_RE = re.compile(r"^selftest case=\S+ FAIL", re.M)
EXC_RE = re.compile(r"^selftest case=\S+ FAIL .*exception", re.M)

# (id, anchor, replacement, area, hypothesis)
MUTANTS = [
    ("N01-gatedict-drop-checkids",
     '    "gate-checkids": "gate_checkids_ok",\n', "",
     "GATE_PREDICATES dict entry removed",
     "predicate registration removal may be invisible to the self-referential scanner -> SURVIVE?"),
    ("N02-gatedict-wiring-wrong",
     '    "gate-wiring": "wiring_ok",\n', '    "gate-wiring": "wiring_findings",\n',
     "GATE_PREDICATES dict value points at the wrong function",
     "gate-wiring check would not call its mapped predicate -> F2/F3 kill"),
    ("N03-f1-append-pass",
     '            findings.append("F1:%s:%d" % (name, node.lineno))\n', "            pass\n",
     "wiring_findings F1 branch",
     "bad_src loses F1:gate-consume:1 -> gate-predicates rows mismatch"),
    ("N04-f2-cond-invert",
     "        elif not (isinstance(ok, ast.Constant) and ok.value is False):\n",
     "        elif (isinstance(ok, ast.Constant) and ok.value is False):\n",
     "wiring_findings F2 branch",
     "constant-True ok no longer reported F2 -> gate-predicates rows mismatch"),
    ("N05-f3-extend-pass",
     '    findings.extend("F3:%s" % name for name in GATE_PREDICATES if name not in wired)\n',
     "    pass\n",
     "wiring_findings F3 branch",
     "unwired gates drop out of bad_src findings -> gate-predicates rows mismatch"),
    ("N06-label-int",
     '        if not (isinstance(label, ast.Constant) and isinstance(label.value, str)):\n',
     '        if not (isinstance(label, ast.Constant) and isinstance(label.value, int)):\n',
     "wiring_findings label filter",
     "every check() label is skipped -> all gates unwired -> gate-wiring FAIL"),
    ("N07-walk-body",
     "    for node in ast.walk(ast.parse(source)):\n", "    for node in ast.parse(source).body:\n",
     "wiring_findings traversal",
     "own check() calls live inside selftest() -> all gates unwired -> gate-wiring FAIL"),
    ("N08-check-arity3",
     '                and node.func.id == "check" and len(node.args) >= 2):\n',
     '                and node.func.id == "check" and len(node.args) >= 3):\n',
     "wiring_findings check() arity gate",
     "all check() calls carry 3 args -> no observable change -> SURVIVE (equivalent?)"),
    ("N09-consumed-arity",
     '        if node.func.id == "consumed" and len(node.args) == 2:\n',
     '        if node.func.id == "consumed" and len(node.args) >= 2:\n',
     "_calls consumed() arity",
     "consumed() takes exactly 2 args -> no observable change -> SURVIVE (equivalent?)"),
    ("N10-calls-recurse-true",
     "            return _calls(node.args[1], name)\n", "            return True\n",
     "_calls recursion through consumed()",
     "consumed(log, <anything>) starts counting as wired -> SURVIVE?"),
    ("N11-rows-drop-empty",
     "            (predicates_ok([]), False),\n", "",
     "gate-predicates rows table",
     "a passing row is deleted; no registration tracks rows -> SURVIVE?"),
    ("N12-rows-flip",
     "(predicates_ok([(True, False)]), False),",
     "(predicates_ok([(True, False)]), True),",
     "gate-predicates rows table",
     "row polarity flipped -> gate-predicates FAIL"),
    ("N13-sidelog-drop-third",
     "        side_logs = [relabel_log, wiring_log, [predicates_ok([(True, False)]) is False]]\n",
     "        side_logs = [relabel_log, wiring_log]\n",
     "gate-checkids side_logs",
     "third limb duplicates rows[14]; removal is unobservable -> SURVIVE (equivalent?)"),
    ("N14-required-drop-wiring",
     '"tmpdir-refusal",\n        "gate-predicates", "gate-wiring"))',
     '"tmpdir-refusal",\n        "gate-predicates"))',
     "REQUIRED_CHECKS",
     "done has gate-wiring, required does not -> gate-checkids extra -> FAIL"),
    ("N15-required-add-phantom",
     '"gate-predicates", "gate-wiring"))',
     '"gate-predicates", "gate-wiring", "phantom-check"))',
     "REQUIRED_CHECKS",
     "required has phantom-check, done does not -> gate-checkids missing -> FAIL"),
    ("N16-main-refusal-rc0",
     "def main(argv):\n    if tmpdir_refused():\n        return 2\n",
     "def main(argv):\n    if tmpdir_refused():\n        return 0\n",
     "case-13 guard (main refusal rc)",
     "case 13 sees ret=0 -> tmpdir-refusal FAIL"),
    ("N17-case13-existing-tmpdir",
     '        bogus13 = os.path.join(scratch, "no-such-tmpdir")\n',
     "        bogus13 = scratch\n",
     "case-13 guard (guard not triggered)",
     "TMPDIR becomes a real dir -> no refusal -> tmpdir-refusal FAIL"),
    ("N18-census-exit2-to-3",
     "        if code == 2:\n", "        if code == 3:\n",
     "census() exit-code bucket",
     "exit-2 rechecks land in exit_other -> prefix-census FAIL"),
    ("N19-census-noprefix-invert",
     "        noprefix = not value.startswith(prefix)\n",
     "        noprefix = value.startswith(prefix)\n",
     "census() noprefix test",
     "prefix census inverts -> prefix-census FAIL"),
    ("N20-restoration-reader-false",
     '            if line.startswith("restoration-recheck:"):\n                return True\n',
     '            if line.startswith("restoration-recheck:"):\n                return False\n',
     "has_restoration_recheck",
     "r.md loses its tag -> restoration-only bucket empty -> FAIL"),
    ("N21-census-exitother-to-exit1",
     '        else:\n            counts["exit_other"] += 1\n',
     '        else:\n            counts["exit1_foreign"] += 1\n',
     "census() exit_other bucket",
     "no fixture yields a code outside {0,1,2} -> SURVIVE?"),
    ("N22-consumed-noappend",
     "        sink.append(value)\n", "        pass\n",
     "consumed()",
     "relabel_log/wiring_log stay empty -> gate-checkids side_logs -> FAIL"),
    ("N23-consumed-return-true",
     "    def consumed(sink, value):\n        sink.append(value)\n        return value\n",
     "    def consumed(sink, value):\n        sink.append(value)\n        return True\n",
     "consumed() return limb",
     "gate-wiring ignores wiring_ok(wfind) -> SURVIVE? (masks X2b class)"),
    ("N24-check-done-pass",
     "        done.append(case)\n", "        pass\n",
     "check() registration",
     "done stays empty -> gate-checkids missing -> FAIL"),
    ("N25-gatecheckids-firstsidelog",
     "all(log == [True] for log in side_logs)",
     "all(log == [True] for log in side_logs[:1])",
     "gate_checkids_ok side_logs limb",
     "rows falsify only side_logs[0]; later logs unasserted -> SURVIVE?"),
    ("N26-gatecheckids-superset",
     "    return set(done) == set(required) and all(log == [True] for log in side_logs)\n",
     "    return set(done) >= set(required) and all(log == [True] for log in side_logs)\n",
     "gate_checkids_ok",
     "no row tests done superset of required -> SURVIVE?"),
    ("N27-case7-drop-rest-flag",
     "              all(got7[k] == v for k, v in want7.items()) and first7 and not rest7,\n",
     "              all(got7[k] == v for k, v in want7.items()) and first7,\n",
     "case-7 both-headers guard",
     "restoration marker for the both-header entry is unasserted -> SURVIVE?"),
    ("N28-census-restoration-bucket",
     '            if has_restoration_recheck(path):\n                counts["restoration_only"] += 1\n',
     '            if has_restoration_recheck(path):\n                counts["norecheck"] += 1\n',
     "census() restoration-only bucket",
     "case 6 counts move -> restoration-only FAIL"),
    ("N29-gatedict-rename-consume",
     '    "gate-consume": "gate_consume_ok",\n',
     '    "gate-consume-x": "gate_consume_ok",\n',
     "GATE_PREDICATES key rename",
     "gate-consume drops out of the gate set -> SURVIVE?"),
    ("N30-runforeign-cwd-inherit",
     '            proc = subprocess.run(["bash", "-c", value], cwd=scratch, env=env,\n',
     '            proc = subprocess.run(["bash", "-c", value], cwd=None, env=env,\n',
     "run_foreign cwd",
     "relative rechecks still fail from the caller cwd -> SURVIVE? (foreign-cwd unasserted)"),
]

COMPOSITES = [
    ("X1-K-W2+K-C1", ["K-W2", "K-C1"]),
    ("X2-K-P2+K-C1", ["K-P2", "K-C1"]),
    ("X3-K-N1+K-P1", ["K-N1", "K-P1"]),
    ("X4-K-X2b+K-N1", ["K-X2b", "K-N1"]),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(path):
    env = dict(os.environ)
    env["TMPDIR"] = S
    p = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                       stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       timeout=600, cwd=OUT)
    return p.returncode, p.stdout + p.stderr


def verdict(rc, out):
    fails = FAIL_RE.findall(out)
    if rc == 0:
        return "SURVIVED", len(fails)
    if "Traceback" in out:
        return "DIRTY", len(fails)
    if not fails:
        return "DIRTY", len(fails)
    return "KILLED", len(fails)


def normalize(text):
    text = text.replace(S, "<SCRATCH>")
    return re.sub(r"recheck-cwd-selftest-[A-Za-z0-9_]+", "recheck-cwd-selftest-<RAND>", text)


def write_diff(path, src, mut, label):
    diff = "".join(difflib.unified_diff(src.splitlines(True), mut.splitlines(True),
                                        "pristine", label, n=2))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(diff)


def main():
    os.makedirs(OUT + "/mutants", exist_ok=True)
    os.makedirs(OUT + "/out", exist_ok=True)
    os.makedirs(OUT + "/composites", exist_ok=True)
    os.makedirs(OUT + "/r78", exist_ok=True)
    with open(TARGET, encoding="utf-8") as fh:
        src = fh.read()
    h0 = sha(TARGET)
    if h0 != EXPECT_SHA:
        print("TARGET SHA MISMATCH %s" % h0)
        return 2
    with open(TABLE, encoding="utf-8") as fh:
        table = json.load(fh)
    table_pairs = {(r["anchor"], r["replacement"]) for r in table}

    base_rc, base_out = run(TARGET)
    base_ok = base_rc == 0 and "selftest cases=15 failures=0" in base_out
    with open(OUT + "/out/_baseline-pristine.out", "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s" % (base_rc, base_out))
    print("BASELINE rc=%d ok=%s sha256=%s" % (base_rc, base_ok, h0))
    if not base_ok:
        return 2

    results = []
    for mid, anchor, repl, area, hypo in MUTANTS:
        n = src.count(anchor)
        rec = {"id": mid, "area": area, "hypothesis": hypo, "occurrences": n,
               "anchor": anchor, "replacement": repl}
        if (anchor, repl) in table_pairs:
            rec["verdict"] = "TABLE-DUPLICATE"
            results.append(rec)
            print("MUTANT %s TABLE-DUPLICATE" % mid)
            continue
        if n != 1:
            rec["verdict"] = "NOT-DERIVED"
            results.append(rec)
            print("MUTANT %s NOT-DERIVED occurrences=%d" % (mid, n))
            continue
        mut = src.replace(anchor, repl, 1)
        mpath = "%s/mutants/%s.py" % (OUT, mid)
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mut)
        write_diff("%s/mutants/%s.diff" % (OUT, mid), src, mut, mid)
        rc, out = run(mpath)
        v, fails = verdict(rc, out)
        with open("%s/out/%s.out" % (OUT, mid), "w", encoding="utf-8") as fh:
            fh.write("rc=%d\n%s" % (rc, out))
        fail_lines = [ln for ln in out.splitlines() if ln.startswith("selftest case=") and " FAIL " in ln]
        rec.update({"verdict": v, "rc": rc, "fails": fails,
                    "exception_detail": bool(EXC_RE.search(out)),
                    "fail_cases": [ln.split()[1] for ln in fail_lines],
                    "mutant_sha256": sha(mpath), "mutant_path": mpath})
        results.append(rec)
        print("MUTANT %s area=%r verdict=%s rc=%d fails=%d cases=%s"
              % (mid, area, v, rc, fails, ",".join(rec["fail_cases"])))

    # composites of frozen-table rows (out of frozen scope; routed only)
    comp_results = []
    for cid, ids in COMPOSITES:
        rows = {r["id"]: r for r in table}
        text = src
        ok = True
        for rid in ids:
            row = rows[rid]
            cnt = text.count(row["anchor"])
            if cnt != 1:
                ok = False
                comp_results.append({"id": cid, "rows": ids, "verdict": "NOT-DERIVED",
                                     "detail": "%s occurrences=%d" % (rid, cnt)})
                print("COMPOSITE %s NOT-DERIVED %s occurrences=%d" % (cid, rid, cnt))
                break
            text = text.replace(row["anchor"], row["replacement"], 1)
        if not ok:
            continue
        cpath = "%s/composites/%s.py" % (OUT, cid)
        with open(cpath, "w", encoding="utf-8") as fh:
            fh.write(text)
        write_diff("%s/composites/%s.diff" % (OUT, cid), src, text, cid)
        rc, out = run(cpath)
        v, fails = verdict(rc, out)
        with open("%s/out/%s.out" % (OUT, cid), "w", encoding="utf-8") as fh:
            fh.write("rc=%d\n%s" % (rc, out))
        fail_cases = [ln.split()[1] for ln in out.splitlines()
                      if ln.startswith("selftest case=") and " FAIL " in ln]
        comp_results.append({"id": cid, "rows": ids, "verdict": v, "rc": rc,
                             "fails": fails, "fail_cases": fail_cases,
                             "mutant_sha256": sha(cpath)})
        print("COMPOSITE %s rows=%s verdict=%s rc=%d fails=%d cases=%s"
              % (cid, "+".join(ids), v, rc, fails, ",".join(fail_cases)))

    # r78 K-X2 equivalence receipt
    r78 = {}
    files = {"candidate": R78, "kx2": R78_KX2}
    outs = {}
    for key, path in files.items():
        h_before = sha(path)
        rc, out = run(path)
        h_after = sha(path)
        with open("%s/r78/%s.raw.out" % (OUT, key), "w", encoding="utf-8") as fh:
            fh.write("rc=%d\n%s" % (rc, out))
        norm = normalize(out)
        with open("%s/r78/%s.norm.out" % (OUT, key), "w", encoding="utf-8") as fh:
            fh.write("rc=%d\n%s" % (rc, norm))
        outs[key] = (rc, norm)
        r78[key] = {"path": path, "rc": rc, "sha_before": h_before, "sha_after": h_after}
        print("R78 %s rc=%d sha=%s" % (key, rc, h_before))
    a, b = outs["candidate"], outs["kx2"]
    identical = a[0] == b[0] and a[1] == b[1]
    diff = "".join(difflib.unified_diff(a[1].splitlines(True), b[1].splitlines(True),
                                        "r78-candidate", "r78-K-X2", n=3))
    with open(OUT + "/r78/normalized.diff", "w", encoding="utf-8") as fh:
        fh.write(diff if diff else "")
    r78["identical"] = identical
    r78["diff_nonempty"] = bool(diff)
    print("R78 identical=%s rc_pair=%d/%d" % (identical, a[0], b[0]))

    # restoration evidence: pristine bytes and output again after all runs
    h1 = sha(TARGET)
    rest_rc, rest_out = run(TARGET)
    base_norm, rest_norm = normalize(base_out), normalize(rest_out)
    restored_ok = (h1 == h0 and rest_rc == base_rc and rest_norm == base_norm)
    with open(OUT + "/out/_baseline-restored.out", "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s" % (rest_rc, rest_norm))
    with open(OUT + "/out/_baseline-restored.raw.out", "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s" % (rest_rc, rest_out))
    with open(OUT + "/out/_baseline-pristine.norm.out", "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s" % (base_rc, base_norm))
    print("RESTORED sha_before=%s sha_after=%s normalized_output_identical=%s raw_identical=%s"
          % (h0, h1, rest_norm == base_norm, rest_out == base_out))

    summary = {"target": TARGET, "target_sha256": h0, "target_sha256_after": h1,
               "detector": "TMPDIR=%s python3 -B <file> --selftest" % S,
               "baseline_rc": base_rc, "baseline_case_line": "selftest cases=15 failures=0" in base_out,
               "restored_identical": restored_ok,
               "table_rows": len(table), "table_pair_duplicates":
                   [r["id"] for r in results if r.get("verdict") == "TABLE-DUPLICATE"],
               "mutants": results, "composites": comp_results, "r78": r78}
    with open(OUT + "/summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    tally = {}
    for r in results:
        tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
    print("HUNT mutants=%d tally=%s restored=%s" % (len(results), tally, restored_ok))
    return 0


if __name__ == "__main__":
    sys.exit(main())
