# ExecHarnessC2 — round 28 wave 1 seat report

Read-only seat: ran and receipted the C2 instruments. **No production file was edited.**
Receipt with full pasted outputs: `.ufo/waves/round-28/receipts/ExecHarnessC2.txt`.
Measured 2026-10-25T17:20–17:28Z; lane HEAD `94f387cbee71a532a51ce075f01701a557231e85`.
The F12 entry landed mid-measurement (~17:27Z), so both the pre- and post-entry states below are
observed, not forecast.

## Assigned items — all three met on landed bytes

| item | result |
|---|---|
| 1. `source-recheck.py` on the round-28 manifest, `--source S042` / `--source S041` | **both exit 0**; 12/12 assertions `OK occurrences=1`; manifest `e62ddad1…4f291d` |
| 2. `frontier-recheck-count.py` | **`entries=15 pass=15 exit=0`**, row `PASS F12 … ids=S041,S042 exit=0` (PRE-STATE was `entries=14 pass=14 exit=0`; README admitted rows 11 → 12) |
| 3. entry's own recheck line from a foreign cwd | **`bash_n_exit=0`, `foreign_cwd_exit=0`** from `/tmp`; both ids rechecked, exit 0 |

## A. Item 1 — post-state

`S042:sha256 OK` + `Q1..Q6 OK occurrences=1`; `S041:sha256 OK` + `Q1..Q6 OK occurrences=1`; exit 0
for both. S041's round-28 digest `e18acbf9…2f5ab47` is byte-identical to its round-26 digest, so
F11's two round-26-anchored entries are unaffected by this round's capture.

**A defect the run caught before it reached the gate.** On the manifest's first landed bytes,
`--source S042` was **exit 2**: `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence` — Q1 was
the heading `5.起算日の連絡`, 8 chars after normalization, under `MIN_QUOTE_CHARS=12`, so the r24
forge-route guard rejected it before any match. ExecManifest rebuilt with the step-5 body line
(verbatim L145); S041 was clean on both byte versions. I edited nothing in that file.

## B. Item 2 — post-state, plus a harness robustness finding from the mid-wave run

Before the entry existed the README row was already `admitted`, and in that state the harness does
not fail gracefully:

```
FileNotFoundError: [Errno 2] No such file or directory: '…/corpus/knowledge/japanese-domestic-disclosure-workflow.md'
harness_exit=1
```

after printing the 14 existing PASS rows — no `entries=` line, no `problems=` code.
`entry_contract()` falls back once to `corpus/<cell>` then opens **unconditionally**; there is no
`isfile` guard on that second path. Same shape as the round-24/25 `--json` crash. Not a false pass,
but a mid-wave run of this counter cannot be read as a count, so `entries=14` should not be quoted
as a round-28 result either. Once the entry landed: `entries=15 pass=15 exit=0`, `harness_exit=0`.

## C. Item 3 — Q10, and why only this seat binds it

`frontier-recheck-count.py:127` runs the line as `subprocess.run(["bash","-c",recheck], cwd=root)` —
from the lane root — so **a cwd-dependent `recheck:` line still PASSes the harness**. The foreign-cwd
run is the discriminating measurement. Landed line, run from `/tmp`:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
```

(shown wrapped only by the display; the file holds it as one line — `\n` before `&&` would be a bash
syntax error, and `bash -n` on the extracted line exits 0)

`bash -n` parses (exit 0); from `/tmp` it resolves through its own `cd … &&` prefix and exits 0 with
both ids at `occurrences=1`. It is two chained invocations rather than one call with two `--source`
flags; the id set `{S041, S042}` still equals the entry's two header `source:` ids, which is what the
harness binds, and both point at the same round-28 manifest. Corpus-wide corroboration:
`recheck-audit.py` reports `lines=40 … cwd_fail=0 paths_fail=0 parse_fail=0`.

## D. The exit code is not the Q9 counter (measured, both directions)

`source-recheck.py` exits **0** for all three states C2's kill rule names. Probe
`wave1/ExecHarnessC2/probe_q9_discrimination.py`, fixtures confined to this seat's scratch dir:

| probe | exit | printed |
|---|---|---|
| P1 `id=S042 path=capture-S041.txt` (stem ≠ id, Q9 c1) | **0** | `S042:Q1 OK occurrences=1` |
| P2 quote twice, no anchor (Q9 c2) | **0** | `… occurrences=2 anchor=MISSING` |
| P3 `anchor=4` does not hold the quote | **0** | `… occurrences=1 anchor=4-BROKEN` |
| P4 quote normalizes to 2 chars (control) | 2 | `reason=quote-too-short-to-be-evidence` |
| P5 path escapes manifest dir (control) | 2 | `reason=outside-manifest-directory` |

So neither a green `--source` run nor a green harness row proves "path stem equals id" or
"exactly-once or holding anchor" — the printed `occurrences=`/`anchor=` notes must be read.
`wave1/ExecHarnessC2/check_q9.py` is that reader: `PASS` on the landed manifest (`S041`,`S042`,
assertions=7 each, `anchor_defects=0`), `FAIL` on each of the three unpinned scratch states with the
failing conjunct named, and `PASS` on the round-26 control. Not always-PASS/always-FAIL (R11).

## E. Gates outside my assignment

- **Census: green post-entry.** Pre-entry it was exit 1 with `E11 S041/S042 missing used-by`; now
  `census_exit=0`, only the pre-existing W04 S028/S029 pair remains.
- **Expected-list basis: still RED — the one live gate at 17:28Z.** `knowledge-expected.txt` holds 39
  entries (41 lines = 39 + 2 comments) while the tree now holds 40, so:
  `expect=present expected=39 missing=0 unexpected=1 exit=1` (`lines=40 pass=40 cwd_fail=0
  parse_fail=0 broken=0`). The exit is purely `unexpected=1`. There is no regeneration flag —
  `--expect` only points at a list, and the only writer of that file in `recheck-audit.py` is inside
  the `--selftest` fixture builder — so the fix is a manual sorted insertion of
  `corpus/knowledge/japanese-domestic-disclosure-workflow.md` between
  `iso-29147-divergence-and-clause-crosswalk.md` and `mission-control.md`, then re-run
  `python3 corpus/instruments/recheck-audit.py` for `expected=40 … unexpected=0 exit=0`.
  `corpus/README.md:234` names `.ufo/waves/round-28/receipts/ExecExpectedList.txt` as the
  reconciliation receipt, but no seat of that name is in the wave-1 roster I can see — both the
  edit and that receipt appear outstanding, and r27 carry-forward 4 is not yet closed.

## F. Scope / integrity

- Production edits: none. Files written: this report, `receipts/ExecHarnessC2.txt`,
  `wave1/ExecHarnessC2/{probe_q9_discrimination.py, check_q9.py, note-to-ExecManifest.txt}` plus
  scratch fixtures (`m1–m4`, `sub/m5`, `capture-S04{1,2}.txt`, synthetic probe text).
- One peer message to ExecManifest (the S042 Q1 short-quote blocker) — it had already fixed it and
  confirmed `e62ddad1…`.
- No tool installed, no pacman transaction, no VCS write, no subagent, no background job left running.
