#!/usr/bin/env python3
import json
import os
import re

WAVE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/MutC1Hunt"
S = "/fast/scratch/hyaku/kasegi-r80/MutC1Hunt"
res = json.load(open(os.path.join(WAVE, "results.json")))
probes = json.load(open(os.path.join(WAVE, "probes.json")))
rows = {r["id"]: r for r in res["results"]}

CLASS = {
 "H27": ("real gap", "`true` in place of the fresh-cwd fixture keeps every bucket count; composed probe: pristine+cwd-inheritance FAILs prefix-census (rc1) while H27+cwd-inheritance passes (rc0) - the fixture's strength is unasserted"),
 "S01": ("real gap", "entry `cd <lane>NONSENSE && true` counted prefixed; main ret 1->0"),
 "S02": ("real gap", "entry `cd <lane> &&false` counted prefixed (noprefix 1->0)"),
 "S03": ("real gap", "ENTRY order follows readdir (a,b,c -> c,a,b); output determinism unpinned"),
 "S04": ("real gap", "census whose only defect is a foreign exit 2 becomes conformant (ret 1->0)"),
 "S05": ("real gap", "census whose only defect is a no-header entry becomes conformant (ret 1->0)"),
 "S06": ("real gap", "with only --root the default lane is the fleet root: conformant fixture ret 0->1; DEFAULT_LANE unexercised"),
 "S07": ("real gap", "ENTRY lines appear without --verbose (0->1)"),
 "S08": ("real gap", "gate_consume_ok(1,[True]) false->true (bool/int identity edge untested)"),
 "S09": ("real gap", "gate_consume_ok(True,[True,False]) false->true (extra log entries accepted)"),
 "S10": ("real gap", "both_headers_ok(True,True,0) false->true (falsiness replaces `is False`)"),
 "S11": ("real gap", "predicates_ok([('a','b')],1) false->true (elements compared by truthiness)"),
 "S12": ("real gap", "predicates_ok with 2 rows against expect=1 false->true (row count is a lower bound)"),
 "S13": ("real gap", "gate_checkids_ok(['a'],['a'],[[False,True]]) false->true (membership, not exact log)"),
 "S14": ("real gap", "check(\"gate-consume\", True and gate_consume_ok(x)): pristine F1, mutant silent; no BoolOp fixture"),
 "S15": ("real gap", "gate_consume_ok(0, log): pristine F4, mutant silent; F4 narrowed to Constant True"),
 "S16": ("real gap", "check(\"x\", False or True): pristine F1, mutant silent; operand quantifier not pinned"),
 "S18": ("real gap", "check(\"gate-consume\", consumed(x)): pristine F2, mutant raises IndexError; arity guard untested"),
 "S19": ("real gap", "RESTORATION-ONLY line vanishes while counts stay right; marker text unpinned"),
 "S20": ("real gap", "NORECHECK line vanishes; marker text unpinned"),
 "S21": ("real gap", "every ENTRY line vanishes; detail output unpinned"),
 "S22": ("real gap", "prefixed exit-2 entry loses its ENTRY line; `code == 2` clause unpinned"),
 "S23": ("equivalent", "indented header is contract-invalid (header must start the line); probe differs only on `   recheck:`, whose value is also mis-sliced; no corpus-valid entry changes"),
 "S24": ("real gap", "selftest leaves a recheck-cwd-selftest-* dir under TMPDIR (leftover>0)"),
 "S25": ("real gap", "TMPDIR unset: pristine rc0, mutant TypeError traceback (None guard untested)"),
 "S27": ("equivalent", "`not xs` == (`xs == []`) for every list; probe identical on [], [x], [x,y]; every call site passes a list"),
 "S28": ("equivalent", "noprefix is a non-negative counter, so `== 0` == `<= 0`; probe identical on conformant, noprefix-only and norecheck-only censuses"),
 "S29": ("real gap", "summary line reworded (`entries=%d` -> `entries = %d`); format unpinned"),
 "S30": ("real gap", "unknown argument exits 0 instead of 2 (usage path untested)"),
 "S31": ("real gap", "empty root: pristine raises SystemExit, mutant prints conformant and exits 0; missing-corpus guard untested"),
 "S32": ("real gap", "scratch-cleanup limb is constant: composed probe (mutant + cleanup removed) rc0/scratch ok while (pristine + cleanup removed) rc1"),
 "S33": ("real gap", "capture() stops restoring stdout: selftest exits 0 with 0 stdout chars; the summary line is unasserted"),
 "S34": ("equivalent", "shipped path: main() guards TMPDIR before selftest() is reachable, so `--selftest` with a bad TMPDIR exits 2 in both; probe differs only through a direct in-process selftest() call (inner guard redundant)"),
 "S35": ("equivalent", "/bin/sh -> /usr/bin/bash 5.3.20 on this host; probe counts identical and the selftest passes, so no observable difference for bash/sh-common values here (portability-only risk on dash hosts)"),
 "S36": ("real gap", "unreadable own source: pristine gate-wiring FAIL rc1, mutant rc0 (F0 fallback untested)"),
 "S37": ("real gap", "`restoration-note:` counted restoration_only (exact-header test unexercised)"),
 "S38": ("real gap", "TMPDIR unset: pristine rc0, mutant tmpdir-parent FAIL rc1 (None-parent limb untested)"),
 "S39": ("real gap", "--lane distinct from --root is ignored: conformant fixture ret 0->1 (argument never varied)"),
 "S40": ("real gap", "gate_negpolarity_ok(False,0) false->true (int identity edge)"),
 "S41": ("real gap", "both_headers_ok(True,1,False) false->true (int identity edge)"),
 "S42": ("equivalent", "valid candidate source has string-literal labels; difference only for `check(42, ...)`, an invalid call"),
 "S43": ("real gap", "GATE_CONSUME_OK accepted as the predicate: pristine F2, mutant silent (case-insensitive matching)"),
}

def failing_cases(rid):
    path = os.path.join(WAVE, "logs", rid + ".out")
    out = open(path, encoding="utf-8").read()
    return [m.group(1) for m in re.finditer(r"^selftest case=(\S+) FAIL", out, re.M)]

def probe_cell(rid):
    p = probes.get(rid)
    if not p:
        return "-"
    key = [k for k in ("ret", "noprefix", "entry_lines", "conformant", "findings", "order",
                       "restoration_only", "norecheck", "marker", "cases", "rc", "leftover_selftest_dirs",
                       "pristine_plus_cwd_inherit_rc", "mutant_plus_cwd_inherit_rc",
                       "mutant_plus_cleanup_removed_rc", "pristine_plus_cleanup_removed_rc") if k in p["pristine"] or k in p["mutant"]]
    def fmt(d):
        bits = []
        for k in key:
            v = d.get(k, "<absent>")
            if isinstance(v, list):
                v = "[" + ",".join(str(x) for x in v) + "]"
            bits.append("%s=%s" % (k, v))
        return "; ".join(bits)
    return "pristine {%s} -> mutant {%s}" % (fmt(p["pristine"]), fmt(p["mutant"]))

lines = []
A = lines.append
A("# MutC1Hunt - round-80 C1 mutant hunt (attempt 1, wave 1, seat MutC1Hunt)")
A("")
A("Scope: single transforms of the frozen r80 C1 candidate that are **outside** the frozen")
A("28-row table (`mutant-table.json` sha256 `08d7f3ce...e418`), applied one literal")
A("replacement at a time to an exact scratch copy, then run as")
A("`TMPDIR=$S/t python3 -B <mutant> --selftest`. Every row is a single transform; anchors")
A("occur exactly once in the frozen bytes (71/71 derived, 0 NOT-DERIVED).")
A("")
A("Frozen candidate: `.ufo/waves/round-80/c1/recheck-cwd-census.py`")
A("sha256 `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698`.")
A("Baseline: rc=0, `selftest cases=15 failures=0`; same sha256 after every run")
A("(`BASELINE rc=0 ok=True`, `FROZEN_AFTER 420151fd...5698`).")
A("")
A("Detector (frozen-counter-shaped, mutbat.py semantics): rc 0 = SURVIVED; rc != 0 with a")
A("`selftest case=... FAIL` line and no Traceback = KILLED; traceback or no FAIL = DIRTY;")
A("`exception=` FAIL detail = EXCEPTION-KILL. A baseline failure would be inconclusive; none")
A("occurred. For every SURVIVED row an R128 normalized-output diff against the baseline was")
A("computed (scratch paths normalized), plus a crafted probe run against pristine and mutant.")
A("")
A("## Totals")
A("")
A("| rows | killed | survived | dirty | not-derived | survivors real-gap | survivors equivalent |")
A("|---|---|---|---|---|---|---|")
A("| 71 | 29 | 42 | 0 | 0 | 36 | 6 |")
A("")
A("No exact `(anchor, replacement)` pair collides with the frozen 28-row table. Two rows")
A("share an anchor with a frozen row but use a different mechanism: H08 (same anchor as N21,")
A("folds `exit_other` into `exit2_foreign` rather than `exit1_foreign`) and S27 (same anchor")
A("as K-N1, rewrites `wiring_ok` as truthiness rather than to a constant).")
A("")
A("R128: 41 of the 42 survivors produce selftest output identical to the baseline after")
A("normalization; only S33 differs (0 stdout chars). Survival is therefore not output noise -")
A("the frozen selftest is silent on all 36 real-gap behaviours below. Survivors are routed")
A("findings for round 81; **no frozen verdict changes** and no frozen byte is edited.")
A("")
A("## Rows")
A("")
A("| id | transform | verdict | rc | class | probe / killing evidence |")
A("|---|---|---|---|---|---|")
for r in res["results"]:
    rid = r["id"]
    if r["verdict"] == "KILLED":
        cls = "detector"
        ev = "FAIL " + ", ".join(failing_cases(rid))
    elif r["verdict"] == "SURVIVED":
        cls, note = CLASS[rid]
        ev = note
        if r.get("probe") and not r.get("probe_differs"):
            ev += " [probe identical]"
    else:
        cls, ev = "detector", r.get("verdict")
    A("| %s | %s | %s | %s | %s | %s |" % (rid, r["desc"], r["verdict"], r.get("rc", "-"), cls, ev))
A("")
A("Killed-row failing-case lists are the selftest's own FAIL lines from `logs/<id>.out`.")
A("Survivor probes are re-runnable: `probes.json` holds the full pristine/mutant observations,")
A("`survivors/<id>.py` holds each surviving mutant source, and `logs/<id>.out` holds its run.")
A("")
A("## Routed findings for round 81 (survivors, by theme)")
A("")
A("1. **Product path / census core** - S01, S02 (prefix literal accepts `cd <lane>NONSENSE`"),
A("   and `cd <lane> &&false`); S03 (unsorted glob changes stdout order); S04, S05 (conform")
A("   drops the `exit2_foreign` / `norecheck` conjuncts, so those are not required for")
A("   `RECHECK-CWD-RESULT conformant`); S06 (DEFAULT_LANE); S07 (verbose default); S37")
A("   (restoration header prefix broadened); S29 (summary format); S30 (usage exit 0); S31")
A("   (missing-corpus guard); S39 (main passes `root` where `lane` belongs).")
A("2. **Unasserted output lines** - S19, S20, S21, S22 (RESTORATION-ONLY / NORECHECK /")
A("   ENTRY lines can vanish entirely); S33 (capture() can silence the whole selftest summary")
A("   while rc stays 0).")
A("3. **Predicate edge inputs** - S08, S09, S10, S11, S12, S13, S40, S41: bool/int identity")
A("   (`is` -> `==`), truncated limb logs, truthiness coercion, `>=` row counts, log membership")
A("   instead of exact logs. Every probe input is a value the predicate's documented contract")
A("   rejects and the mutant accepts.")
A("4. **Gate-wiring scanner limbs** - S14 (F1 BoolOp limb), S15 (F4 non-True constants),")
A("   S16 (BoolOp `any` -> `all`), S18 (`consumed()` arity -> crash), S36 (F0 unreadable-source")
A("   fallback), S43 (case-insensitive predicate match).")
A("5. **Environment / harness self-protection** - H27 (fixture neutralisation undetected;")
A("   composed with cwd inheritance it survives where pristine fails); S24 (selftest scratch")
A("   dir leaks); S25, S38 (TMPDIR-unset paths: crash / tmpdir-parent FAIL); S32")
A("   (scratch-cleanup `leftover` limb constant).")
A("")
A("## Equivalent survivors (not routed as gaps)")
A("")
A("| id | why equivalent |")
A("|---|---|")
for rid in ("S23", "S27", "S28", "S34", "S35", "S42"):
    A("| %s | %s |" % (rid, CLASS[rid][1]))
A("")
A("## Restoration evidence")
A("")
A("Frozen bytes hashed before and after the hunt (`frozen-before.txt` / `frozen-after.txt`):")
A("candidate `420151fd...5698`, counter `b47276d1...d450`, table `08d7f3ce...e418`, builder")
A("`e0a8c714...e0ef3`, manifest `85cd2f26...ba1`, snapshot S114 `e1ccfb9b...88d2`, claims")
A("`c9343d81...5204`; the ten control files are listed with their hashes. Both hash lists are")
A("identical; no frozen byte, no instrument, no lane file outside this wave directory was")
A("written. No git/jj mutation was issued; no tool was installed. Scratch root")
A("`/fast/scratch/hyaku/kasegi-r80/MutC1Hunt` was deleted after outputs were copied here.")
A("")
A("## Reproduce")
A("")
A("```")
A("S=/fast/scratch/hyaku/kasegi-r80/MutC1Hunt; mkdir -p $S/t")
A("TMPDIR=$S/t python3 -B driver.py        # 71 rows, ~12 s")
A("```")
A("`driver.py` is copied beside this report; output dirs `logs/`, `survivors/`, `results.json`,")
A("`probes.json`, `baseline.out`.")

open(os.path.join(os.path.dirname(WAVE), "MutC1Hunt.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("wrote", os.path.join(os.path.dirname(WAVE), "MutC1Hunt.md"))
