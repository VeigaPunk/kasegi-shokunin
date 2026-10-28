VERDICT: BROKEN

Scope: limb R5 (receipt wording) of the round-45 C1 counter v1.1 against the integration tree, lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (exported with `git archive` to scratch; never the moving working tree). Round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd. Tip c950fa3 exported separately for the re-run.

The refiled body is genuine: a re-run at c950fa3 reproduces lines 4-24 byte-for-byte. The receipt as a file, however, carries hand-written header lines that QUALITY R37 (line 323: "with no hand-written header") and R39 (line 351) forbid, and the counter's R5 predicate does not bind those lines, so R5 accepts them. Three counter mutants survive.

---

## F1 — BROKEN: refiled receipt carries hand-written header lines (R37/R39)

Attacked: `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` lines 1-2 in the 6662a42 export.

Command: `cat -n .../final-attempt3-refiled.txt` (excerpt)
```
     1	# refile of the selftest invocation of final-attempt3.txt (round 45; one observed run; the bare call without --root that printed an argparse usage error there is not repeated)
     2	# tip export c950fa3
     3	$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>
    ...
    24	selftest cases=20 failures=0
    25	exit=0
```
Command: `grep -n "^#" .../final-attempt3-refiled.txt` → `1:# refile ...` and `2:# tip export c950fa3`.

The instrument prints no `#` line. Re-run stdout (below) is 21 lines, stderr 0 bytes; it contains no `$` line, no header and no `exit=` line. So lines 1-2 (hand-typed), line 3 (hand-typed command echo with placeholders `<tip>`/`<scratch>`, not the executed argument values) and line 25 (`exit=0`, typed by the wrapper) are outside the instrument's bytes. QUALITY R37 (line 323): "a receipt is only the unedited tee of one observed run: its bytes are that invocation's stdout+stderr as written, with no hand-written header, no edited tally …". R39 (line 351) restates it: a receipt "with one whose header line its instrument does not print … is not a receipt".

Answer to the seat question: yes. R39 does not use the words "no hand-written header"; that phrase is in R37 (line 323), which R39 specializes and leaves in force. The `#` header lines 1-2 are exactly the header lines the instrument does not print. The original `final-attempt3.txt` carries the same pattern (its lines 1, 30, 37, 38 are `#` prose), so the repo convention predates this refile; the refiled file is still non-compliant under R37 as written.

Counter consequence: see F2-F4 (R5 does not check these lines).

## F2 — counter survivor: a hand-written header line passes R5

Attacked: `corpus/instruments/r45-routed-defects.py` `limb_r5` (lines ~293-318). The predicate hashes only `body = lines[inv[0]+1 : end[0]]`; nothing before the invocation line or after `exit=0` is bound.

Mutant `M2-hand-header-line-added`: `# notes: re-ran on my laptop, all green` prepended to the refiled file; then
`python3 corpus/instruments/r45-routed-defects.py --root <mutant> --baseline <base>` →
`limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`

## F3 — counter survivor: a line appended after the receipt's end passes R5

Mutant `M3-line-appended-after-exit0`: `# edited after the run: all green` appended after `exit=0` → `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`. R37/R39: "nothing appends to it or edits it afterwards". Survives.

## F4 — counter survivor: the failed bare call restated in a header passes item 5

Spot-check item 5 (`corpus/lessons/round-44-verifier-spotcheck.md:83`): "re-file the selftest invocation line without the failed call". The R5 usage check is `^(usage:|.*error:)`.

Mutant `M4-failed-call-described-in-header`: `# bare call printed: argparse: the following arguments are required: --root (exit 2)` prepended → `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`. The regex misses "arguments are required", so the failed call survives in the receipt while R5 reads fixed.

## F5 — VERIFIED OK: the body is a reproducible run at c950fa3

Command (run in the `git archive c950fa3` export, cwd there):
`TMPDIR=$S python3 corpus/instruments/r44-routed-defects.py --root $S/c950 --selftest --work $S/work` → rc=0, stderr 0 bytes, 21 stdout lines; last line `selftest cases=20 failures=0`.
`sed -n '4,24p' final-attempt3-refiled.txt | cmp - rerun.out` → no output, byte-identical (`BODY_BYTE_IDENTICAL`).
Second independent run at c950fa3: `diff rerun.out run2.out` → no output (identical).
Body sha256 (`\n`-joined, no trailing newline) = `03fe3af53006dc7561b6080b5bd923312569a5a2b8ca3d7b6ad3722da9f226c0`, equal to the counter's `refiled-body` pin (`r45-routed-defects.py:72`).
Ancestry: `git merge-base --is-ancestor c950fa3 6662a42…` → ancestor; `… c950fa3 dc5bb8c…` → ancestor.
The r44 counter is the pinned bytes at both trees (`sha256 d5438c67befaefadf46e44474330771d5d5b7b3b8f0c5ec3df11ef422ca7ba90` at c950fa3 and in the integ tree).

Discrimination: the same invocation against the integ tip gives `selftest case=POSITIVE verdict=fail fixed=7 unresolved=1` and `selftest cases=20 failures=1` (rc=1; D4 reads unresolved, as SKILL.md records). The receipt is therefore tied to c950fa3, as its header says, and cannot be re-attributed to the tip.

## F6 — VERIFIED OK: the original receipt is unchanged

`cmp .ufo/waves/round-44/controls/final-attempt3.txt` (integ export) vs the dc5bb8c export → IDENTICAL; `git show dc5bb8c…:<path> | cmp - <export file>` → IDENTICAL_BLOB. sha256 `91eddf5c064f522aec1173f74bcae397b8f1d61ec858a178ddd2de60ed44cec7` in both. `git diff --stat dc5bb8c 6662a42 -- <original>` → empty. `git log` lists only `5e4d6bf` for the original and only `6662a42` for the refiled file.

## F7 — VERIFIED OK: spot-check item 5 wording is satisfied by the body; R5 rejects the do-nothing and copy controls

- Body (lines 4-24) has no `usage:` or `error:` line; `grep -n -i "usage\|error"` on the refiled file matches only line 1 (the narrative mention).
- Do-nothing control, base export (`--root dc5bb8c export`): `limb R5 fixed=0 read=refiled-absent`.
- Copy-the-original control (`M1`, original file copied verbatim as the refiled file): `limb R5 fixed=0 read=usage-or-error-line-present`.
- Lane export (unchanged): `limb R5 fixed=1 read=refiled=pinned-run-output original=unchanged`; full counter on the integ tree: `routed-defects total=5 fixed=5 unresolved=0 exit=0`.
- Mutants that break the body or the envelope are rejected: body count edited (`M5`) → `receipt-body-not-the-pinned-run-output`; body line dropped (`M8`) → same; invocation with real paths (`M6`) → `invocation-lines=0`; exit line removed (`M7`) → `exit0-line-absent`; second run appended (`M9`) → `invocation-lines=2`.

## F8 — finding (timing and attribution): no execution instant; the pin is self-referential

- `grep -n -E "[0-9]{4}-[0-9]{2}-[0-9]{2}T|run-utc"` on the refiled file → none. The instrument prints no instant either, so the header's "one observed run" cannot be checked from the bytes. R39 (line 351) says a receipt with no printed instant must have its timing labelled `report-only`; the R5 record does not label it.
- The counter's pin proves the bytes are unchanged since pinning. It does not prove a single invocation. Only the independent re-run (F5) establishes the body's content.
- Line 3 uses the placeholders `<tip>`/`<scratch>`; R5 requires that exact string, so the echoed command cannot be checked against the executed command. Limitation, not a defect of the body.

---

## Fix (not applied; L1 owns the tree)

1. Move the header prose out of the receipt into a sidecar the counter pins (or drop it); the receipt must start at the invocation line and end at `exit=0`, with no other lines.
2. In `limb_r5`, reject any line before the invocation and any line after `exit=0`; pin the whole-file sha256 as well as the body sha.
3. Widen the failed-call check to the argparse text (`the following arguments are required`), not only `^(usage:|.*error:)`.
With (1)-(3), mutants M2, M3 and M4 are rejected; F5, F6 and F7 stay as they are.

## Verification gaps

- The "one observed run" claim is not verified from the bytes (F8); only the body's reproducibility is.
- The re-run used the `git archive` export of c950fa3 (not the original worktree) and two runs, not a timing-bound observation.
- Mutants are single-edit probes of R5 only; I did not run the other counter limbs beyond the full-counter run cited in F7.
- The scratch tree was removed at exit; no install was made; nothing was committed or mutated.
