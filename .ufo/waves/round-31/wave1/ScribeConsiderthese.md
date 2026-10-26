# ScribeConsiderthese — round 31 receipt

Seat `ScribeConsiderthese`, item: append the round-31 status-flip section to
`corpus/knowledge/considerthese-proposals-ledger.md` (append-only), keep its `recheck:` line
byte-identical, wait for `ExecScoreGap.md`, cite the reporter's real output line, and re-run
`recheck-audit.py --quiet`.

- Answering model actually run: `devin/deepseek-v4-1-flash` (config route table decides; no model passed).
- Write scope used: `corpus/knowledge/considerthese-proposals-ledger.md` (owned) + this receipt. Nothing else.
- Lane base `b374febb…`; claims-freeze `738a7799…`. No git/jj mutation, no tool install, no pacman, no network fetch.

## 1. Baseline before the append

```
$ sha256sum corpus/knowledge/considerthese-proposals-ledger.md
d91889e5f7d77c3695c366521c348569b4f29269632e0bfc927105600a6c250d  corpus/knowledge/considerthese-proposals-ledger.md
$ wc -l corpus/knowledge/considerthese-proposals-ledger.md
20 corpus/knowledge/considerthese-proposals-ledger.md
$ grep -n "^recheck:" corpus/knowledge/considerthese-proposals-ledger.md
5:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/density.py corpus/knowledge/considerthese-proposals-ledger.md --label proposal-ledger
```

The whole-file digest `d91889e5…` equals the round-30 close-out erratum's corrected ledger
sha256, so the starting bytes are the audited ones.

Audit baseline at the start of this seat, before `ExecExpectedList`'s F15 line landed — PRE-STATE
for the 43-vs-44 count, not comparable to §5 (no UTC stamp was captured for this run; it precedes
the 23:40:12Z wait):

```
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
… exit=0
```

## 2. Waiting for the score-gap receipt

```
$ until [ -s .ufo/waves/round-31/wave1/ExecScoreGap.md ]; do sleep 20; done
ARRIVED 2026-10-25T23:40:12Z      # draft: §6 FINAL run = PENDING
$ until ! grep -q '^PENDING$' .ufo/waves/round-31/wave1/ExecScoreGap.md; do sleep 20; done
FINAL_READY 2026-10-25T23:45:48Z  # §6 FINAL run filled in
```

`ExecScoreGap.md` §6 is the quiescent-byte run (its own gate: `recheck-audit.py --quiet` →
`lines=44 total=44 pass=44 … exit=0`, `expected=44 missing=0 unexpected=0`). The line cited in
the ledger:

```
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
```

Independent re-measurement by this seat at 2026-10-25T23:46Z (read-only; the reporter writes
nothing):

```
$ cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/score-gap.py
…
recheck: lines=44 executes=20 gated=24 broken=0 exit=0
gap: 24 of 44 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
$ echo $?
0
```

Identical to the receipt's §6 lines (same four `source:` digests, same five fields).

## 3. The append

Section `## Round-31 status flips (appended 2026-10-25)` appended after `## Limits` (the file's
last section). Proposal 2 flips `open` → `mined round 31 → corpus/instruments/score-gap.py`,
stated as a read-only reporter asserting no score move, with the `gap:` line above as evidence.
Proposals 1, 3, 4, 5, 6 are stated `unchanged`, each with the consulted evidence:

| proposal | unchanged because |
|---|---|
| 1 | mined round 28 → `corpus/QUALITY.md:83` R14; `corpus/lessons/round-29.md:221`, `corpus/lessons/round-30.md:82` restate it, no later landing/decline |
| 3 | still partially landed (F13/S043–S045); round-30 verifier records all four SHONEN boxes `[~]` (`corpus/lessons/round-30-verifier-spotcheck.md:12`); box 2 open per `corpus/lessons/round-29.md:221` |
| 4 | mined round 30 into this file (`corpus/lessons/round-30.md:82`); no later note revises it |
| 5 | mined round 29 → `corpus/QUALITY.md:89` R15 (`corpus/lessons/round-29.md:219`); restated at `corpus/lessons/round-30.md:82` |
| 6 | no round-28..30 lesson records a landing/decline; lane-wide `grep -rn 'event-driven\|push listener'` over `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md` → 0 matches (this seat, round 31) |

Nothing in the pre-existing table, the `Limits` section or the header was edited.

## 4. Additions-only verification

```
$ git show HEAD:corpus/knowledge/considerthese-proposals-ledger.md | sha256sum
d91889e5f7d77c3695c366521c348569b4f29269632e0bfc927105600a6c250d  -
$ head -20 corpus/knowledge/considerthese-proposals-ledger.md | sha256sum
d91889e5f7d77c3695c366521c348569b4f29269632e0bfc927105600a6c250d  -
$ git show HEAD:corpus/knowledge/considerthese-proposals-ledger.md | grep "^recheck:" | sha256sum
ac0fbac1a1e4d2862e2e9eb0139a9d32aa5950cd2c7a5b204bbf4bf8e4127771  -
$ grep "^recheck:" corpus/knowledge/considerthese-proposals-ledger.md | sha256sum
ac0fbac1a1e4d2862e2e9eb0139a9d32aa5950cd2c7a5b204bbf4bf8e4127771  -
$ sha256sum corpus/knowledge/considerthese-proposals-ledger.md ; wc -l …
c354ca0242bf7da44589e45c464deba0714dc083e2bf480a6c855ec30a1629c2  corpus/knowledge/considerthese-proposals-ledger.md
35 corpus/knowledge/considerthese-proposals-ledger.md
```

The committed 20 lines are byte-identical to the working file's first 20 lines, and the
`recheck:` line hash is identical on both sides (append-only proven at the byte level).

## 5. Post-append gates

```
$ eval "$(grep '^recheck:' corpus/knowledge/considerthese-proposals-ledger.md | sed 's/^recheck: //')"
# Density census — proposal-ledger (35 lines, 2 blocks)
| 1 | Limits | 4 | 2 | … | 0.0 |
| 2 | Round-31 status flips (appended 2026-10-25) | 14 | 11 | 23 | 7 | 13 | 2 | 45 | 409.1 |
| | **mean dens** | | | | | | | | **204.5** |
density_exit=0
```

```
$ python3 corpus/instruments/recheck-audit.py --quiet      # 23:48:22Z, after the append
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
```

`bash -n` on the extracted recheck line → exit 0. Before the append at 44 lines the audit was
also `strict pass=44/44 … exit=0` (run in the same batch as the 23:46Z re-measurement), so the
append changed neither the pass count nor the exit. The count moved 43 → 44 earlier in the wave because a sibling landing
(`ExecExpectedList` adding the F15 entry) changed the audited set — disclosed, not attributed to
this seat.

Density moved from mean `0.0` (1 block, 20 lines) to mean `204.5` (2 blocks, 35 lines) because
the appended section is dense in paths/numerics. That is a measurement change from the append,
not a score claim; the recheck's exit is 0 in both states.

## 6. Scope and limits

- Only `corpus/knowledge/considerthese-proposals-ledger.md` is modified (`git status --porcelain`
  shows exactly ` M corpus/knowledge/considerthese-proposals-ledger.md` for the paths this seat
  checked). `considerthese/` is untouched: `git status --porcelain considerthese/` → 0 lines;
  `sha256sum considerthese/2026-10-25.md` → `6adc24d64e3c04884d029d380278bb49b50f8e6e9c7bdc1951f56a38c027052e`.
- No write outside the lane; no `pacman`; no tool installed or upgraded; no fetch (the only
  network-dependent inputs were read from committed bytes).
- Limits: the audit figure is at 23:48Z on a wave still landing; later landings can move
  `lines=` and the canonical figure is the L1's post-commit recheck. The `gated=24 of 44` figure
  is timestamped at 23:46Z and moves if a gated recheck's base returns — that movement is the
  reporter's point, not a defect. Proposal-2 status records a landed instrument; it asserts no
  score move and does not decide whether any of the 24 gated rechecks is "unsupported".
