#!/usr/bin/env python3
"""Build MutC1Hunt-rows.json from the frozen r84 candidate, asserting every anchor is unique."""
import json
import sys

TARGET = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/c1/recheck-cwd-census.py"
OUT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/w1/MutC1Hunt-rows.json"

# (id, anchor, replacement, class, kill_cases, expect)
ROWS = [
    ("X01-LK-runforeign",
     '            globals()["run_foreign"] = real_run\n',
     '            pass\n',
     "assertion", ["entry-set"],
     "state leak: the case-31 finally no longer restores run_foreign; a no-op mutation of the "
     "restoration line leaves the -1 stub installed for every later in-process census, yet the "
     "33-case suite still prints cases=33 failures=0. Fix: add "
     "`globals()[\"run_foreign\"] is real_run` to the entry-set check."),
    ("X02-LK-selftest",
     '            globals()["selftest"] = real_selftest\n',
     '            pass\n',
     "assertion", ["argv-values"],
     "state leak: the case-29 finally no longer restores the selftest global; after selftest() "
     "returns, main([..., '--selftest']) returns the 77 stub instead of running. Suite still "
     "green. Fix: add `globals()[\"selftest\"] is real_selftest` to argv-values."),
    ("X03-LK-chdir",
     '            os.chdir(here29)\n',
     '            pass\n',
     "assertion", ["argv-values"],
     "state leak: the case-29 finally no longer restores the process cwd; selftest() leaves the "
     "caller in the (deleted) case-29 fixture. Every later case uses absolute roots, so the suite "
     "stays green. Fix: add `os.getcwd() == here29` to argv-values."),
    ("X04-LK-timeout",
     '            globals()["TIMEOUT"] = saved_timeout17\n',
     '            pass\n',
     "assertion", ["timeout-bucket"],
     "state leak: the case-17 finally no longer restores TIMEOUT; after selftest() the module "
     "runs with TIMEOUT=1 for the rest of the process. Fast fixtures keep the suite green. Fix: "
     "add `TIMEOUT == saved_timeout17` to timeout-bucket."),
    ("X05-LK-mkdtemp",
     '            tempfile.mkdtemp = real_mkdtemp\n',
     '            pass\n',
     "assertion", ["scratch-cleanup"],
     "state leak: the cases-3/4 finally no longer restores tempfile.mkdtemp; every later mkdtemp "
     "in the process is the recording wrapper holding a growing list. The wrapper delegates, so "
     "the suite stays green. Fix: add `tempfile.mkdtemp is real_mkdtemp` to scratch-cleanup."),
    ("X06-ENV-tmp-unset",
     '    env_tmp = os.environ.get("TMPDIR") or None\n',
     '    env_tmp = os.environ["TMPDIR"]\n',
     "assertion", ["tmpdir-unset"],
     "census() now requires TMPDIR; with TMPDIR unset (cron/CI) the census raises KeyError instead "
     "of using the tempfile default. tmpdir-unset only calls tmpdir_refused(), never census(). Fix: "
     "run census(root1, lane1) inside the TMPDIR-unset block and assert got18 == got1."),
    ("X07-REST-substr",
     '            if line.startswith("restoration-recheck:"):\n',
     '            if "restoration-recheck:" in line:\n',
     "assertion", ["relabel-detection"],
     "has_restoration_recheck() matches the header anywhere in a line; a doc that documents the "
     "convention (`- write \\`restoration-recheck:\\` ...`) becomes restoration_only and is never "
     "executed. Latent (no current corpus line triggers it); no fixture has a mid-line mention. "
     "Fix: add a mid-line mention to case-8 n-neither.md and keep norecheck=1."),
    ("X08-NOPREFIX-in",
     '        noprefix = not value.startswith(prefix)\n',
     '        noprefix = prefix not in value\n',
     "assertion", ["prefix-literal"],
     "the prefix may now appear anywhere; `recheck: true && cd <LANE> && true` is reported "
     "prefixed although it does not carry its own cd prefix (contract: 'does not start with'). "
     "Latent on the current corpus; no fixture has a mid-value prefix. Fix: add a d-mid.md fixture "
     "to case 14 and bump noprefix=3/exit0=3."),
    ("X09-SUM-noprefix-slot",
     '          % (counts["entries"], counts["noprefix"], counts["exit2_foreign"],\n',
     '          % (counts["entries"], counts["norecheck"], counts["exit2_foreign"],\n',
     "assertion", ["prefix-census"],
     "the printed summary reports norecheck in the noprefix slot; case 27's fixture has both "
     "values 0, so the six new checks never see a nonzero noprefix. Fix: assert case-1's exact "
     "summary line (entries=6 noprefix=5 exit2_foreign=1 ...) in prefix-census."),
    ("X10-SUM-exit2-zero",
     '          % (counts["entries"], counts["noprefix"], counts["exit2_foreign"],\n',
     '          % (counts["entries"], counts["noprefix"], 0,\n',
     "assertion", ["prefix-census"],
     "the summary always prints exit2_foreign=0; case 27's fixture has exit2_foreign=0, so no "
     "six-check fixture pins a nonzero gating bucket. Fix: same case-1 summary assertion (its "
     "fixture has exit2_foreign=1)."),
    ("X11-ENTRY-exit1",
     '        if verbose or noprefix or code == 2:\n',
     '        if verbose or noprefix or code in (1, 2):\n',
     "assertion", ["bucket-sum"],
     "default mode also prints ENTRY for prefixed exit-1 entries; entry-set pins exit-0/exit-7 "
     "only, and case-1's d-exit1 is prefix-less (it prints anyway), so no case asserts the exit-1 "
     "arm. Case 21's default out21 has the prefixed exit-1 entry osv-b and no ENTRY line. Fix: "
     "add `\"ENTRY osv-b.md\" not in out21` to bucket-sum."),
    ("X12-TIMEOUT-sentinel",
     '            return -1\n',
     '            return -2\n',
     "assertion", ["timeout-bucket"],
     "a timed-out recheck now renders foreign_exit=-2 (docstring: counted as -1); timeout-bucket "
     "asserts only the exit_other bucket, and entry-set forces -1 by patching run_foreign, so the "
     "real timeout path's sentinel is never pinned. Fix: capture case 17 verbosely and assert "
     "`ENTRY h-hang.md noprefix=0 foreign_exit=-1` (no extra run)."),
    ("X13-MAIN-argv-slice",
     '    sys.exit(main(sys.argv))\n',
     '    sys.exit(main(sys.argv[1:]))\n',
     "assertion", ["usage-guards"],
     "the __main__ guard drops argv[0]; --selftest still works (membership test), but every "
     "documented CLI run (`--root D --lane D`) starts parsing at the root value and exits 2 with "
     "usage. No check ever executes the script as a subprocess. Fix: run the candidate e2e via "
     "subprocess in usage-guards and assert RESULT conformant + rc 0."),
    ("X14-MAIN-defroot",
     '    root, lane, verbose = ".", DEFAULT_LANE, False\n',
     '    root, lane, verbose = "..", DEFAULT_LANE, False\n',
     "assertion", ["usage-guards"],
     "the default root moves off cwd; the documented bare invocation now censuses the parent. No "
     "case calls main() with zero flags (every call passes --root). Fix: chdir into a fixture "
     "with an empty corpus/knowledge and assert main([prog]) prints entries=0 and exits 0."),
    ("X15-TIMEOUT-default",
     'TIMEOUT = 120\n',
     'TIMEOUT = 1\n',
     "assertion", ["timeout-bucket"],
     "the default timeout drops to 1 s; any legitimate recheck that takes 1-120 s moves into the "
     "non-gating exit_other bucket, so a tree with unverifiable rechecks stays conformant. The "
     "suite only exercises the patched TIMEOUT=1 path. Fix: pin TIMEOUT == 120 (a behaviour test "
     "needs a sleep fixture and adds ~2 s per run)."),
    ("X16-FIRST-errors",
     'def first_recheck(path):\n    with open(path, encoding="utf-8", errors="replace") as fh:\n',
     'def first_recheck(path):\n    with open(path, encoding="utf-8") as fh:\n',
     "assertion", ["first-line"],
     "a knowledge doc with one non-UTF-8 byte now raises UnicodeDecodeError out of census() "
     "(traceback, exit 1) instead of being scanned with replacement chars. Every fixture is "
     "UTF-8. Fix: add a bytes fixture (b'# caf\\xe9\\nrecheck: cd ...') to first-line and assert "
     "entries=1/exit0_foreign=1 with no exception."),
    ("X17-STRIP-space",
     '                return line[len("recheck:"):].strip()\n',
     '                return line[len("recheck:"):].strip(" ")\n',
     "assertion", ["prefix-census"],
     "equivalent: strip(' ') keeps the trailing newline, which is inert -- the prefix test only "
     "uses startswith on the same leading bytes and bash -c ignores trailing whitespace, so every "
     "output is byte-identical. Not a gap."),
    ("X18-SUM-restoration-adds-noprefix",
     '             counts["norecheck"], counts["restoration_only"]))\n',
     '             counts["norecheck"], counts["restoration_only"] + counts["noprefix"]))\n',
     "assertion", ["prefix-census"],
     "the summary's restoration_only slot prints restoration_only + noprefix; case 27 has both "
     "values 0, so the six new checks never see a nonzero restoration_only (case 6 does not assert "
     "its summary). Fix: extend summary-fields with an all-slots-nonzero fixture (entries=8 "
     "noprefix=1 exit2=1 exit0=2 exit1=2 other=1 norecheck=1 restoration=1)."),
    ("X24-CONFORM-sum-add-noprefix",
     '               + counts["exit_other"] + counts["norecheck"] + counts["restoration_only"])\n',
     '               + counts["exit_other"] + counts["norecheck"] + counts["restoration_only"] + counts["noprefix"])\n',
     "assertion", ["bucket-sum"],
     "equivalent on every reachable census output: noprefix>0 already fails the noprefix limb, so "
     "conform_ok is False either way, and noprefix=0 adds zero. A negative-noprefix hand-built "
     "dict is the only divergence. Not a gap."),
    ("X25-USAGE-except-breadth",
     '            except Exception as exc_:  # a crash is a finding, not a harness error\n',
     '            except SystemExit as exc_:  # a crash is a finding, not a harness error\n',
     "assertion", ["argv-values"],
     "equivalent on the frozen bytes: main() returns ints and never raises on the usage_run "
     "inputs, so the guard's breadth is unobservable. Latent harness weakness (a future main() "
     "raising would crash the suite instead of a FAIL line, the r80 F4 shape), not a defect now."),
    ("X19-SUM-entries-slot",
     '          % (counts["entries"], counts["noprefix"], counts["exit2_foreign"],\n',
     '          % (counts["noprefix"], counts["noprefix"], counts["exit2_foreign"],\n',
     "assertion", ["summary-fields"],
     "control: the entries slot prints noprefix; case 27 wants entries=4 on a noprefix=0 tree, so "
     "the six-check summary-fields fixture kills it. Shows the battery does catch summary slot "
     "defects -- X09/X10 survive only because that fixture's nonzero slots are all zero."),
    ("X20-ENTRY-drop-exit2",
     '        if verbose or noprefix or code == 2:\n',
     '        if verbose or noprefix:\n',
     "assertion", ["output-lines"],
     "control: exit-2 entries no longer print by default; output-lines expects "
     "'ENTRY x-exit2.md noprefix=0 foreign_exit=2' in out15e, so it is killed. Shows the exit-2 "
     "arm is pinned while X11's exit-1 arm is not."),
    ("X21-CONFORM-couple-norecheck-restoration",
     '            and counts["norecheck"] == 0 and counts["restoration_only"] == 0\n',
     '            and counts["norecheck"] == counts["restoration_only"]\n',
     "assertion", ["conform-limbs"],
     "conform_ok couples two independent limbs: a tree with one no-header entry AND one "
     "restoration-only entry (both nonzero, equal) is declared conformant. No fixture has both "
     "defects at once, so no case fails. Fix: add a hand-built dict with "
     "norecheck=1/restoration_only=1 to conform-limbs and assert False."),
    ("X22-CONFORM-exit2-le-noprefix",
     '    return (counts["noprefix"] == 0 and counts["exit2_foreign"] == 0\n',
     '    return (counts["noprefix"] == 0 and counts["exit2_foreign"] <= counts["noprefix"]\n',
     "assertion", ["conform-limbs"],
     "equivalent: the same predicate pins noprefix == 0, so exit2 <= noprefix forces exit2 == 0 "
     "for non-negative counts. No reachable tree changes verdict. Not a gap."),
    ("X23-NEUTRAL-comment",
     'def conform_ok(counts):\n',
     'def conform_ok(counts):  # conformance predicate\n',
     "neutral", None,
     "neutral control: a trailing comment on the predicate's def line; must pass exactly like the "
     "baseline (NEUTRAL-OK)."),
]


def main():
    with open(TARGET, encoding="utf-8") as fh:
        src = fh.read()
    rows = []
    bad = []
    for rid, anchor, repl, cls, kc, expect in ROWS:
        n = src.count(anchor)
        if n != 1:
            bad.append("%s anchor occurrences=%d" % (rid, n))
            continue
        if anchor == repl:
            bad.append("%s replacement equals anchor" % rid)
            continue
        row = {"id": rid, "anchor": anchor, "replacement": repl, "class": cls, "expect": expect}
        if kc:
            row["kill_cases"] = kc
        rows.append(row)
    if bad:
        print("BAD:\n" + "\n".join(bad))
        return 1
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2)
        fh.write("\n")
    print("rows=%d out=%s" % (len(rows), OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
