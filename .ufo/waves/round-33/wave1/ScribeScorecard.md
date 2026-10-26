# ScribeScorecard — round-33 C1/C2 section and capability row (append-only)

- Seat: `ScribeScorecard` (scribe, leaf; no delegation, no background jobs).
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — the **only** write scope.
- Round 33 / wave 1, hyaku run 8. Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`,
  claims-freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; wave-1 integration commit
  `9f9848816503aa0cd566fc2efdc5e69ea501a253` (read-only `git log`/`rev-parse`).
- Answering model I actually ran on: `opencode-go/deepseek-v4.1-flash` (host project
  context; the config route table decided; no model passed by this seat).
- Owned path: `SCORECARD.md` (append-only). This receipt. Nothing else.
- Tools installed/upgraded: **none** (nothing needed; `pacman` never invoked).
- Scratch: no clone/mirror/work tree/fixture was created by this seat — the item is a
  synthesis append, so rule 12 has no tree to remove; nothing was written to `/tmp`.

## 1. Gate — poll to the assigned condition, 45-minute cap

Item condition: `{WD}/ExecRegressionC1.md`, `{WD}/ExecHarnessC2.md`,
`{WD}/ExecCensusAfter.md` and at least 10 wave receipts. `ExecNoHarmFinal.md` was added to the
gate because the item names it as a density source.

```
$ cd .ufo/waves/round-33/wave1 && while [ $SECONDS -lt $DL ]; do n=$(ls -1 | grep -v swarm-registry | wc -l);
    ok=1; for f in ExecRegressionC1.md ExecHarnessC2.md ExecCensusAfter.md ExecNoHarmFinal.md; do
    [ -s "$W/$f" ] || ok=0; done; echo "$(date -u +%TZ) receipts=$n gate=$ok"; ...
04:17:56Z receipts=4 gate=0
…
04:46:57Z receipts=58 gate=1
GATE_MET
```

Gate met at `2026-10-26T04:46:57Z`, 30 min after the first poll, inside the cap. At write time
`ls -1 .ufo/waves/round-33/wave1/*.md | wc -l` = **55** seat receipts (58 entries including
`ExecCaptureBinding/`, `ExecRegressionC1/` evidence dirs and `swarm-registry.json`), far above
the assigned 10.

## 2. Receipts read (the only sources for the appended numbers)

| receipt | what the append takes from it |
|---|---|
| `c1-controls/before.txt` (frozen at claims time) | instrument absent `ls_exit=2`; `TOTAL records=38 with_url=0 with_fetched_utc=0`; `round-32/` = `S049.txt`/`S050.txt`; `recheck_exit=2` |
| `c1-controls/fake-checker-receipt.txt` | `records=38 bound=38 unbound=0`, `fake_exit=0` |
| `c2-controls/before.txt`, `census-before.txt` | frontier 15; `S049=0`/`S050=0`; rows 0/0; `total_rows=48`; census `W04 S028`+`W04 S029`+`ok`, exit 0; harness `entries=18 pass=18`; `recheck_exit=2` |
| `wave1/ExecRegressionC1.md` §1–§2, §4 | `records=40 bound=40 unbound=0` twice byte-identical (`1861fec8…`); the `AUDIT` line; `selftest cases=11 failures=0`; base-byte `unbound=38` exit 1 + `FAIL rule=missing-manifest dir=round-32`; fake rejection; `strict pass=45/45`, `expected=45`; `source-recheck --selftest cases=10`; harness `entries=19 pass=19`; anchorcheck `12 in-range … 0 bad`; density 191.5/689/24 → 201.7/710/25; append-only `19 0 SKILL.md`, `2 0 PROVINCE.md`, 0 deletions; D-R33-1, D-R33-2 |
| `wave1/ExecHarnessC2.md` §1–§3 | the nine C2 counter outputs (16 / 1 / 1 / 1 / 1 / 50 / census / harness / recheck), 14 quote assertions `occurrences=1`, entry `recheck:` exit 0 from lane root, `/`, `/tmp` |
| `wave1/ExecCensusAfter.md` §1–§3 | census exit 0 with exactly the three lines; six contract commands (`rows=50`, `tier=A=47 B=1 C=2`, `status=mined=38 queued=9 rejected=3`, `dups=`, `enum_violations=0`, `missing_usedby=0`); `diff -u` deltas `+2`/`+2`/`+2`; `S049`/`S050` row count 1 each |
| `wave1/ExecNoHarmFinal.md` §1, §3–§4, §7 | measured-file digests; density 191.5 → 201.7 with 24 → 25 blocks and 689 → 710 cites; anchorcheck classes; the final `capture-binding-check.py` run; the 57 unowned evidence-dir observation (not mine to file) |
| `wave1/RevC1Instrument.md` §1–§9 | Q1–Q6 answers; §9 verdict `lands` |
| `wave1/CritC1Kill.md` Verdict 1–4, `Measured matrix`, `Disclosures` | fake-checker clause; erratum load-bearing; H1–H8 blind spots; 40 `:sha256 OK` byte arm; `fetched_utc` = commit timestamp |
| `wave1/RevEntryF16.md` §1–§7 | Q1–Q10 table; `**ADMIT.**`; three below-bar findings; reviewed digest `53c48b3b…` |
| `wave1/RevRowS049.md` §8, `wave1/RevRowS050.md` §3 | `ADMIT-ROW` ×2 and their grounds |
| `wave1/MutEntryF16.md` §digest history, §Verdict | final digest `1f7ac0a2…`; the narrow-delta sentence; `SURVIVOR (coverage finding)` scoped to the harness |
| `wave1/RevQuoteSweep.md` §6 | the quote finding closed on `1f7ac0a2…` |
| `wave1/RevTranslation.md` | review at `1f7ac0a2…` |
| `wave1/CritC2Kill.md` §5, §6 item 3, §10 | junk-twin all-pass measurement; uncommitted twin control; the reported residual defect |
| `wave1/ExecDeterminism.md` | per-command determinism table over the same digests |
| `.ufo/waves/round-33/claims.json`, `claims-erratum-1.md`, `census-before.txt` | frozen predicates, erratum ruling, before-capture |

Every number in the appended section was copied from one of these files (or from `claims.json`
for the frozen targets); none was retyped from memory.

## 3. Append landing (append-only, `SCORECARD.md`)

```
$ sha256sum SCORECARD.md ; wc -l SCORECARD.md                      # before
6224ab877044896fc07320fc7e2434f1b5bad1d5f2f748c7e49502f02634a624  SCORECARD.md
980 SCORECARD.md
$ grep -c 'capture-binding-check' SCORECARD.md                     # before: no such row
0
$ grep -n '^## ' SCORECARD.md | tail -3                            # before: no Round-32 section
862:## Round 31 — frozen claims C1/C2 (2026-10-25)
931:## Round-31 capabilities
```

Anchor used: the last line of the file (line 980, the round-31 wave-4 addendum's closing
sentence). Appended after it, nothing rewritten, no existing byte changed:

```
$ sha256sum SCORECARD.md ; wc -l SCORECARD.md                      # after
e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3  SCORECARD.md
1091 SCORECARD.md
$ grep -n '^## Round 33\|^## Round-33 capabilities\|^### Round-33 move-log' SCORECARD.md
982:## Round 33 — frozen claims C1/C2 (2026-10-26)
1074:## Round-33 capabilities
1080:### Round-33 move-log rows
$ grep -c 'LANE_HASH' SCORECARD.md
2
$ git status --porcelain -- SCORECARD.md
 M SCORECARD.md
```

Net +111 lines: the C1/C2/density table, five prose paragraphs (erratum, C1 blind spots, C2
reviewer posture, measurement state, capabilities clause, saturation), the
`## Round-33 capabilities` table with one `capture-binding-check` row, two round-33 move-log
rows, and **two** `<LANE_HASH>` markers — one in the section preamble and one closing line —
for the L1 to replace with the final lane commit.

## 4. Shape decisions (round-31 parity)

- Table columns exactly as round 31: `Claim | Axis | Before | After | Verdict and evidence |
  Last change`. C1 axis cell `depth:verifiability (lowest non-retired, 4)`, C2 `coverage (7)`,
  third row `depth:density` with `Last change` = `r15 (held r33)`.
- Verdict cells state the score outcome (C1 `Verified, score held 4`; C2 `Verified on all nine
  frozen counters, score held 7`; density `Unchanged (held 9), no harm`) and then disclose
  every deviation, exactly as round 31 recorded its counter-mutant repair.
- The capability row enters as a **separate** `## Round-33 capabilities` subsection, the
  round-24/25/26/31 pattern, because this seat is append-only and does not edit the master
  `## Capabilities` table (line 301) in place — stated in the section itself.
- Saturation line kept at `9/10 per owned axis, window N = 3`, with the capability entry noted
  as restarting the window (previous entry round 31).

## 5. Disclosures (recorded, not resolved — none of these is a seat write)

1. **This file had no round-32 section at base.** `grep -n '^## ' SCORECARD.md` shows round 31
   as the last round heading; the appended section says so and keeps C2's `Last change` at 31
   instead of inventing a round-32 row.
2. **C1's capability clause is landed here.** `wave1/ExecRegressionC1.md` D-R33-2 records that
   the `capture-binding-check` row was unobservable at 04:33Z and that the L1 must re-check
   after this seat lands. The row is appended; no counter in section 3 changes as a result.
3. **C2's entry clause rests on an ADMIT of an earlier revision.** `RevEntryF16` reviewed
   `53c48b3b…`; the final bytes are `1f7ac0a2…` (306 lines, 24539 B, `sha256sum` read by this
   seat). The delta is disclosed in section 3 as a Claim 1 question stem with the
   quote/translation limbs re-measured on the final bytes; the section does not claim a second
   full Q1–Q10 review.
4. **`MutEntryF16` SURVIVOR is reported, not charged to C2.** The receipt scopes it as an
   instrument coverage finding on `frontier-recheck-count.py` rule A and states the frozen
   counter #2 covers the mutant; the section repeats that scope rather than filing it as an
   entry defect.
5. **The critic's junk-twin control is unapplied.** `CritC2Kill` §6 item 3 asks for the twin and
   its all-pass output to be committed under `c2-controls/`; `ls .ufo/waves/round-33/c2-controls/`
   = `before.txt` only. `c2-controls/` is not this seat's path, so it is recorded, not created.
6. **One reported residual defect does not reproduce on final bytes — measured here, once.**
   `CritC2Kill` §10 reported that `entry:280`'s scoped `grep` prints a stale literal. This seat
   ran that line's own command once on committed `1f7ac0a2…`:

   ```
   $ awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md \
       | grep -c -E 'CVSS|0.85|时效评价|利用代码'      → 1
   $ grep -c -E 'CVSS|0.85|时效评价|利用代码' corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   → 3
   ```

   The entry's printed literal is the scoped value, so the defect was fixed with the revision
   that followed it. The section records this as this seat's own single read of committed
   bytes, explicitly **not** a re-review and not a seat receipt.
7. **`ExecNoHarmFinal` §1 reports 57 unowned evidence files (392K) under `wave1/<Seat>/`.** The
   FILE OWNERSHIP list grants only `wave1/<YourName>.md`. This seat wrote exactly one file in
   that directory (this receipt) and no evidence subdirectory, so it contributes nothing to
   that class; the item is named here for the L1, not filed as mine.
8. **`anchorcheck.py` in-range 7 → 12** (`D-R33-1`) is carried in the density row and the C1
   verdict as a count change with every failure class identical; it is not presented as new
   resolvable evidence, and no score move is claimed for it.

## 6. Bounds and hygiene

- Wrote: `SCORECARD.md` (append) and this receipt. No other lane path, no fleet root, no
  sibling lane, no `/home/vgpnk/Projects/shokuknow`, no `templates/`, `scripts/`, `.ufo/state/`,
  `.ufo/watchdog.log`, `MANIFEST.json`, `/home/vgpnk/Projects/shokunin/.scratch/`.
- No git/jj mutation: only read-only `git log`, `git rev-parse`, `git status --porcelain`.
  The L1 commits.
- No fetch, no live bounty target contacted, no credential material read or reproduced
  (`SentCred`/`SentScopeFinal` receipts untouched beyond being listed; the S049 credential
  ranges were never opened by this seat — only the entry's non-reproduction sentence was read
  in `RevEntryF16`'s quotation).
- No quotation longer than 25 words; each quote carries its file and section/line.
- No tool install or upgrade; no `pacman` transaction; no host service touched.

## 7. Files

- Written by this seat: `SCORECARD.md` (+111 lines, `6224ab87…` → `e03fbefa…`); this receipt.
- Read only: the receipts and control files in §2, `claims.json`, `claims-erratum-1.md`,
  `census-before.txt`, and (for the one-command check in §5.6) the committed F16 entry.
