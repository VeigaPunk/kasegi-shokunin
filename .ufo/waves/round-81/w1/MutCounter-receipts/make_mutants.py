#!/usr/bin/env python3
"""Generate single-transform mutants of the frozen r81 mutbat.py in scratch."""
import hashlib
import json
import os
import sys

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "mutbat-pristine.py")

MUTANTS = [
    ("V1-drop-killcases-filter", "verdict(): count every FAIL as on-target",
     "    on_target = [exc for case, exc in fails if case in kill_cases]\n",
     "    on_target = [exc for case, exc in fails]\n"),
    ("V2-miskilled-as-killed", "battery(): MISKILLED counts toward the kill tally",
     '        counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")\n',
     '        counts = v == "KILLED" or v == "MISKILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")\n'),
    ("V3-exc-any", "verdict(): all(on_target) -> any(on_target) in exception branch",
     "    if all(on_target):\n",
     "    if any(on_target):\n"),
    ("V4-exc-class-unguarded", "battery(): EXCEPTION-KILL counts for assertion rows too",
     '        counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")\n',
     '        counts = v == "KILLED" or v == "EXCEPTION-KILL"\n'),
    ("P1-drop-nofail-conjunct", "clean_pass(): drop the no-FAIL-line conjunct",
     '    return rc == 0 and exact and not fail_lines(out) and "Traceback" not in out\n',
     '    return rc == 0 and exact and "Traceback" not in out\n'),
    ("P2-drop-exact-line", "clean_pass(): drop the exact summary-line anchor",
     '    exact = re.search(r"^selftest cases=%d failures=0$" % expect_cases, out, re.M) is not None\n',
     "    exact = True\n"),
    ("P3-drop-traceback", "clean_pass(): drop the Traceback test",
     '    return rc == 0 and exact and not fail_lines(out) and "Traceback" not in out\n',
     '    return rc == 0 and exact and not fail_lines(out)\n'),
    ("B1-neutral-broken-as-ok", "battery(): every neutral row ticks neutral_ok",
     '            if ok_n:\n                tally["neutral_ok"] += 1\n',
     '            tally["neutral_ok"] += 1\n'),
    ("B2-drop-nneutral", "battery(): ok drops the n_neutral > 0 requirement",
     '    ok = (baseline and n_kill > 0 and n_neutral > 0 and tally["killed"] == n_kill\n',
     '    ok = (baseline and n_kill > 0 and tally["killed"] == n_kill\n'),
    ("B3-drop-nkill", "battery(): ok drops the n_kill > 0 requirement",
     '    ok = (baseline and n_kill > 0 and n_neutral > 0 and tally["killed"] == n_kill\n',
     '    ok = (baseline and n_neutral > 0 and tally["killed"] == n_kill\n'),
    ("B4-neutral-in-place", "battery(): neutral rows run the target in place, not from a copy",
     '        mpath = os.path.join(mdir, os.path.basename(target))\n',
     '        mpath = target if row["class"] == "neutral" else os.path.join(mdir, os.path.basename(target))\n'),
    ("R1-drop-killcases-validation", "validate_rows(): drop the kill_cases check",
     '            kc = row.get("kill_cases")\n'
     '            if not (isinstance(kc, list) and kc and all(isinstance(c, str) and c for c in kc)):\n'
     '                return "row %s lacks kill_cases" % row["id"]\n',
     '            pass\n'),
    ("F1-failline-drop-caret", "FAIL_LINE_RE: drop the start-of-line anchor",
     'FAIL_LINE_RE = re.compile(r"^selftest case=(\\S+) FAIL(?: (.*))?$", re.M)\n',
     'FAIL_LINE_RE = re.compile(r"selftest case=(\\S+) FAIL(?: (.*))?$", re.M)\n'),
    ("F2b-exc-substring", "fail_lines(): exception detail matched by substring, not prefix",
     '    return [(m.group(1), (m.group(2) or "").startswith("exception="))\n',
     '    return [(m.group(1), "exception=" in (m.group(2) or ""))\n'),
    ("F2-failline-drop-detail", "FAIL_LINE_RE: drop the exception-detail capture",
     'FAIL_LINE_RE = re.compile(r"^selftest case=(\\S+) FAIL(?: (.*))?$", re.M)\n',
     'FAIL_LINE_RE = re.compile(r"^selftest case=(\\S+) FAIL(?: .*)?$", re.M)\n'),
]


def main():
    src = open(SRC, encoding="utf-8").read()
    out = []
    os.makedirs(os.path.join(S, "mutants"), exist_ok=True)
    for mid, desc, anchor, repl in MUTANTS:
        n = src.count(anchor)
        rec = {"id": mid, "desc": desc, "anchor": anchor, "occurrences": n}
        if n != 1:
            rec["status"] = "ANCHOR-MISS"
            out.append(rec)
            continue
        mut = src.replace(anchor, repl, 1)
        path = os.path.join(S, "mutants", mid + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(mut)
        rec.update({"status": "derived", "path": path,
                    "sha256": hashlib.sha256(mut.encode("utf-8")).hexdigest(),
                    "diff_bytes": len(mut) - len(src)})
        out.append(rec)
    json.dump(out, open(os.path.join(S, "mutants.json"), "w"), indent=1)
    print(json.dumps([{k: r[k] for k in ("id", "status", "sha256", "diff_bytes")} for r in out], indent=1))
    print("pristine_sha256", hashlib.sha256(src.encode("utf-8")).hexdigest(), "mutants", len(out))
    return 0 if all(r["status"] == "derived" for r in out) else 1


if __name__ == "__main__":
    sys.exit(main())
