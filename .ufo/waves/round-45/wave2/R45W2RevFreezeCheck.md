VERDICT: BROKEN

# R45W2RevFreezeCheck: attack on corpus/instruments/freeze-check.py (export of 6662a4276b6f7bd61e23e12058414e09dd71b9e4)

## Scope and setup
- Export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/exp`. The lane working tree was not used.
- Attacked file sha256 (re-run): `a38d8dc1319ff0bdab1bc557643b192cf201312fe0f7d681e430c40817305888  .../exp/corpus/instruments/freeze-check.py` (364 lines). Matches the assignment.
- Base: export of the round base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`. Its `corpus/README.md` has 26 table-aware `admitted` rows (`admitted_rows` = 26). A plain `grep -cE '^\| F[0-9]+ \| admitted \|'` on the same file prints `0`, the round-44 defect.
- Tool-root: a copy of that base README (26 rows). Fixtures: `altbase` (same README, 0 admitted rows), `moving` (27 rows, not the frozen base), `base-b` (fresh copy for mutation).
- Claim files were generated in scratch and replayed with the exported tool: `python3 exp/corpus/instruments/freeze-check.py --claims <c>.json --tool-root <tool> --base <base> --work <w> --timeout 60`.
- Own selftest, control run: `freeze-check.py --selftest --work <w> --base <base>` printed `selftest cases=20 failures=0` (rc=0). The selftest does not cover any construction below.
- Counter used for the honest reading (H): `cd {tree} && awk -F'|' '$2 ~ /^ *F[0-9]+ *$/ && $4 ~ /^ *admitted *$/ {n++} END{print "admitted=" n+0}' corpus/README.md`. It prints `admitted=26` on base, `admitted=0` on altbase, `admitted=27` on moving.

## Controls (discrimination)
- C0 honest H on real base, `expect_before=admitted=26`: `claim X base_read=admitted=26 verdict=ok` / `freeze-check claims=1 base_ok=1 exit=0`. Honest passes.
- C1 honest H on altbase, same claim: `claim X base_read=admitted=0 verdict=FAIL` / `finding X FC-NO-MATCH no output line equals expect_before 'admitted=26'; rc=0` / `freeze-check claims=1 base_ok=0 exit=1`. The check does react to the base.
- C2 honest H on moving base with the frozen claim: `FC-NO-MATCH` and `FC-AFTER-AT-BASE`, exit 1.
- C3 do-nothing `echo 'admitted=26'` with no tree mention: `finding X FC-NO-TREE counter_cmd reads neither {tree} nor {base}`, exit 1.

## Findings (all exit 0 with `base_ok=1`, i.e. the defect passes the gate)

### F1 (High): a matching line beside a contradicting line passes. freeze-check.py:164, :169, :167-168
- Claim: `counter_cmd` = `echo 'admitted=0'; cd {tree} && <H>`; `expect_before=admitted=0`; `expect_after=admitted=27`; base = real frozen base.
- Raw counter output at base (`bash -c`, tree=base): `admitted=0` / `admitted=26`.
- Freeze-check output:
  ```
  claim X base_read=admitted=0 verdict=ok
  freeze-check claims=1 base_ok=1 exit=0
  ```
- Mechanism: `matched = next(ln for ln in stripped if ln == eb)` returns the first equal line; no other output line is checked against the claim, and `read = matched` reports the stale line. The base actually reads 26.

### F2 (High): base mutation check compares size+mtime_ns, not bytes. freeze-check.py:51-65 (snapshot, `(st.st_size, st.st_mtime_ns)`), :158-161; docstring :24-26 says "byte-for-byte untouched"
- Counter (K2) flips one byte of `{tree}/corpus/README.md` (`a`->`A`), then `os.utime(p, ns=(st_atime_ns, st_mtime_ns))` restores the timestamps. It prints `admitted=26`.
- Evidence: `cmp -l` on base vs mutated copy: `4 141 101` (byte 4: `a` -> `A`). sha256 pre `f5e7bd2572af7f8440cc2210ffd410e9713e9099add1b93b2b14072c1b28edea`, post `cf6d3b30770beae3f31d99809abd696132811d3a51dd2fc22b34c010e94e7b44`. Size 61225 and mtime_ns 1793220479000000000 are identical in both.
- Freeze-check output: `claim X base_read=admitted=26 verdict=ok` / `freeze-check claims=1 base_ok=1 exit=0`. No `FC-BASE-MUTATED`.
- Control K2-size (same counter but appending one byte): `finding X FC-BASE-MUTATED counter changed the base tree: corpus/README.md`, exit 1. So the blind spot is precisely same-size with restored mtime.
- Persistent corruption of the frozen base therefore passes the gate.
- Transient variant K2b (edit then restore the original bytes, mtime restored): passes, and the bytes are identical afterwards (`sha256 before==after-run: True`). This one is harmless to the result; it is a limitation, not a second defect.

### F3 (High): the `{tree}` requirement is a substring mention, not a use. freeze-check.py:146-147, :235-236 (the selftest helper prepends `: {tree}; `)
- K3 `echo 'admitted=26' #{tree}` and K3b `: {tree}; echo 'admitted=26'`, base = altbase (0 rows, honest reads 0). Both print:
  ```
  claim X base_read=admitted=26 verdict=ok
  freeze-check claims=1 base_ok=1 exit=0
  ```
- Raw K3 output with tree=altbase: `admitted=26`. The counter never reads the tree; the constant is accepted. Control C1 shows the honest counter fails on the same base.

### F4 (High): a relative path reads the tool-root, not the base, and the gate still passes. freeze-check.py:74 (`cwd=tool_root`), :146-147
- K4 counter `: {tree}; awk ... corpus/README.md` (no `cd`), tool-root holds 26 rows, base altbase holds 0.
- Raw output (cwd=tool-root, tree=altbase): `admitted=26`. Honest `cd {tree}` reading on the same base: `admitted=0`.
- Freeze-check: `claim X base_read=admitted=26 verdict=ok` / `freeze-check claims=1 base_ok=1 exit=0`.
- This is the same shape as the round-44 counter (`grep ... corpus/README.md` relative); a `{tree}` mention elsewhere satisfies the check.

### F5 (High): `--base` is never tied to `FROZEN_BASE_REV`. freeze-check.py:48 (constant), :195-197 (used only in `locate_readme`, i.e. selftest); `check()` :101-179 never compares the base to it
- K5 counter H on the moving base (27 rows), claim `expect_before=admitted=27`, `expect_after=admitted=28`:
  ```
  claim X base_read=admitted=27 verdict=ok
  freeze-check claims=1 base_ok=1 exit=0
  ```
- A claim replayed against a non-frozen tree is accepted as "replayed at the freeze". Control C2 (frozen claim on moving base) fails, so the difference is only the claim value, not a base check.

### F6 (Medium): env branch. freeze-check.py:70-72 sets `R45_FREEZE_CHECK=1` for the child
- K6 counter: `if [ -n "$R45_FREEZE_CHECK" ]; then echo 'admitted=26'; else <H>; fi`, base = altbase.
- Raw under the checker env: `admitted=26`. Raw with env unset (the lane's real use): `admitted=0`.
- Freeze-check: `claim X base_read=admitted=26 verdict=ok` / exit 0. The replayed counter is not the counter the lane runs. Requires deliberate branching, so the threat model is an adversarial or careless author.

### F7 (Low): missing base is silently accepted. freeze-check.py:151-153 (`snapshot(base) if os.path.isdir(base) else {}`)
- K9 `echo 'admitted=26'; : {tree}` with `--base <nonexistent>`: `claim X base_read=admitted=26 verdict=ok` / `freeze-check claims=1 base_ok=1 exit=0`. The base directory is not required to exist.

## Held (no defect found)
- Exact-line equality holds. K7 `echo 'admitted=260'; echo 'admitted=2'` with `expect_before=admitted=26`: `finding X FC-NO-MATCH no output line equals expect_before 'admitted=26'; rc=0`, exit 1 (prefix rejected). K8 zero-width space inside the line (`printf 'admitted=26\xe2\x80\x8b'`): `claim X base_read=admitted=26​ verdict=FAIL` / `FC-NO-MATCH`, exit 1.
- A do-nothing counter with no tree mention is rejected (C3, `FC-NO-TREE`). The `--base`-changing honest counter is correctly rejected (C1, C2).
- Counter timeouts, the crash case and the schema/dup-id/field checks are exercised by the author's selftest (20/20 pass on re-run); I did not find a bypass there.

## Verdict summary
The gate certifies counters that print constants, read the wrong tree, contradict themselves while containing the expected line, or mutate the base in a same-size, mtime-preserving way. The only real guarantee is the exact-line match and the `FC-NO-TREE`/`FC-BASE-MUTATED` checks for the simplest cases. The docstring's "byte-for-byte" claim is overstated. Suggested minimum fixes (not applied; L1 owns edits): hash contents not size+mtime (F2); require the base to be a directory and to equal `FROZEN_BASE_REV` or a supplied rev (F5, F7); require every output line to be consistent (or require the expected value to be the sole numeric output) (F1); require the counter to read the tree (e.g. run with cwd=`{tree}`, or fail when a relative path resolves under tool-root) (F3, F4); and remove or document the env flag (F6).

## Limitations
- Threat model: the author writes the claims and counters. F3/F6 require deliberate or careless constructions, though F1, F2 and F4 can arise from honest mistakes (e.g. a debug `echo`, a relative path).
- I did not re-run the real round-45 counters (`r45-routed-defects.py`, `r45-c2-gate.py`) through freeze-check; I only read the frozen `claims.json` (commit 8cf62c8) to confirm the `{tool}`/`{tree}` argument style. Whether those counters read the base is not established here.
- Tested on this host's `/fast` filesystem; nanosecond mtime preservation was observed (F2), not assumed for other filesystems.
- No edits to the lane tree, the base export, or any git state. No tool installs. Scratch removed on exit.
