# MutC2Counter — round-91 C2 counter mutation test

Seat: mutation-tester (leaf). Round 91, attempt 1, wave 1. Scope: the frozen C2 counter
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-91/c2/capability-check.py`
(sha256 `39deae670c72f52641b98a8a4dd1c877a4f1747ed6fe9138963ece3d1e37b6f0`), tested
against the C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70` and the nine control
variants rebuilt from `.ufo/waves/round-91/controls/c2-controls-r91.sh` with the
forgeries from `c2-forgeries.py`.

Frozen inputs used read-only: counter above; C2 candidate instrument
`89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7`; gate
`8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`; base
`bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`; frozen controls receipt
`c2-controls-r91.txt`. No lane, frozen, instrument or state file was modified; no git/jj
write was made outside the scratch clone.

## Method

- Scratch `S=/fast/scratch/hyaku/kasegi-r91/MutC2Counter` (deleted before yield). Shared
  clone `S/c2clone` (`git clone --shared` of the lane, toplevel asserted); all commits
  under test were made only in that clone.
- Variants rebuilt exactly as `c2-controls-r91.sh` does it: `git -C clone checkout
  --detach $BASE`, instrument replaced (no-work keeps the base instrument), the frozen
  candidate SCORECARD row substituted, one commit per variant. Revs in
  `MutC2Counter-receipts/variant-revs.tsv`.
- Baseline first: the unmodified counter against the landing (pinned, seeds 9191 and 1;
  unpinned seed 9191; and once with `--lane` = the real lane) and against each rebuilt
  control (unpinned, seed 9191). Landing passes, all nine controls fail, per-limb
  outcomes identical to the frozen controls receipt (K3 `scanned=1734` at the landing vs
  `1731` at the base-derived variants; K8 clause lists and K1 `selftest_rc=1` on every
  forgery match line for line).
- 35 single-limb mutants (>=20 required) generated from the frozen counter by
  count==1 exact replacements, every replacement asserted exactly once, every mutant
  syntax-checked and byte-distinct from the frozen counter. Names + sha256:
  `MutC2Counter-receipts/mutant-index.tsv`.
- Matrix: each mutant x {landing pinned seed 9191; the 9 rebuilt controls unpinned seed
  9191} = 350 runs, plus each mutant on the landing at seed 1 = 35 runs. Verdicts:
  `MutC2Counter-receipts/matrix.tsv`.
- Classification: a mutant fails the landing -> **killed by landing** (the landing's
  positive checks detect the counter change); a mutant passes any control -> **killed by
  control** (that limb was the sole guard for that control); otherwise **survivor**
  (redundant limb: the mutation is invisible to the whole control set).

## Result

**35 mutants: 3 killed by the landing, 0 killed by any control, 32 survivors.**
At seed 1 the same 3 fail and the same 32 pass.

No single-limb counter mutation makes the counter accept any forgery or the no-work
variant. Every control is rejected by at least two limbs, and every forgery is rejected
by K1's `--selftest` in addition to K4/K7/K8 (see Finding 1). The frozen receipt already
shows this: `LIMB K1 FAIL selftest_rc=1` on F1-F8.

### Killed by the landing (the only mutants the control set can see)

| mutant | landing limb(s) FAIL | why |
| --- | --- | --- |
| M23-K4-drop-E4-plant-only | K4 `missing=...E4.json`, K8 clause 6 | plant dropped but the clause and the expected hit kept: K4's exact set sees the miss, K8's `p not in PLANTS` linkage sees the inconsistency |
| M24-K8-flip-S016 | K8 clause 7 | clause flag inverted; K8 fails on the true landing |
| M25-K8-flip-S019 | K8 clause 9 | same |

Evidence: `MutC2Counter-receipts/killed-by-landing.txt` (seed 9191) and
`seed1-sweep.txt` (seed 1). The landing pins flag direction and clause/plant linkage;
it cannot pin the removal of a check (all removal mutants pass).

### Survivor classes (32)

| class | mutants | what each removes |
| --- | --- | --- |
| limb ablations | M01 K1-selftest, M02 K2, M03 K3, M04 K4, M05 K5, M06 K6, M07 K7, M08 K8 | the limb can no longer fail |
| K1 pins | M09 instrument sha, M10 gate sha | sha comparison |
| K2 sub-checks | M11 `rc==1`, M12 `oracle==HISTORY_EXPECTED` | return code / oracle pin |
| K3 sub-check | M13 `unused_allow==0` | stale-allow check |
| K4 sub-checks | M14 `rc==1`, M15 bad-allow `rc2==2`, M16 `--files` sub-run (fok) | each K4 sub-check |
| K4/CLAUSES plants | M17 S014, M18 live-f, M19 S022, M20 S021, M21 E4, M22 report3 | one plant (+ its expect entry and clause) |
| K8 arm | M26 negative-clause flags ignored | the hit-set comparison for negative clauses |
| K6 sub-checks | M27 `bhits<=PLANT_EXPECT`, M28 `caught=bhits&NEW_EXPECT` | base-discrimination checks |
| K7 sub-checks/plants | M29 `rc==1`, M30 n6, M31 n7, M32 n4+n5, M33 g6 | return code / one generated negative or positive |
| K5 sub-checks | M34 `need` tokens, M35 `87` last cell | scorecard-row checks |

Per-mutant x case verdicts: `MutC2Counter-receipts/matrix.tsv`.

## Per-control guard sets (unmodified counter)

| control | limbs that FAIL | k1 selftest |
| --- | --- | --- |
| no-work (base instrument) | K4, K7, K8 | pass |
| F1 cookie-only (skdutid window reverted) | K1, K4, K7, K8 | FAIL rc=1 |
| F2 skdutid-only (cookie shape removed) | K1, K4, K7, K8 | FAIL rc=1 |
| F3 no-floor | K1, K3, K4, K7, K8 | FAIL rc=1 |
| F4 case-insensitive | K1, K4, K7, K8 | FAIL rc=1 |
| F5 overbroad-names | K1, K4, K7, K8 | FAIL rc=1 |
| F6 no-lookbehind | K1, K4, K7, K8 | FAIL rc=1 |
| F7 literal-keyed | K1, K4, K7, K8 | FAIL rc=1 |
| F8 no-json-newline | K1, K4, K8 (K7 passes) | FAIL rc=1 |

## Per round-91 conjunct: guard set and single-limb answer

"Single limb that guards it" — **none for any of the 13 conjuncts**. Each violating
control fails at least two limbs; the matrix confirms it behaviourally: no single-limb
mutant accepts any control, so no limb is a single point of failure and no limb's
individual rejection power is exercised. The joint guard sets below are observed
(receipt `counter-baseline.txt`) and, for clauses 1/2 and 6, proven exact by the
union-ablation probes.

| # | conjunct (CLAUSES key) | violating control | limbs that fail | joint guard set (counter-side checks) |
| --- | --- | --- | --- | --- |
| 1 | azure: skdutid between sv and sig | F1 | K1,K4,K7,K8 | K1 selftest; K4 S014 expected hit; K7 g6 generated positive; K8 clause |
| 2 | azure: skdutid between sig and sv, JSON `\u0026` | F1 | K1,K4,K7,K8 | K1; K4 live-f expected hit; K7 g6; K8 clause |
| 3 | azure: 8-letter name ends the window | F5 | K1,K4,K7,K8 | K1; K4 S018 absence; K7 n7 negative; K8 clause |
| 4 | cookie: Set-Cookie header | F2 | K1,K4,K7,K8 | K1; K4 S015; K7 g4; K8 clause |
| 5 | cookie: Cookie request header | F2 | K1,K4,K7,K8 | K1; K4 live-h; K7 g5; K8 clause |
| 6 | cookie: JSON-escaped newline between Set-Cookie values | F2, F8 | F2: K1,K4,K7,K8; F8: K1,K4,K8 | K1; K4 E4; K8 clause (K7 has no such case; P1) |
| 7 | cookie: 28-char documentation example is not a hit | F3 | K1,K3,K4,K8 | K1; K3 lane hit (round-90 `round91-leads.txt:65` quotes the example); K4 S016 absence; K8 clause |
| 8 | cookie: prose placeholder is not a hit | F3 | K1,K4,K8 | K1; K4 S017 absence; K8 clause |
| 9 | cookie: name case-sensitive | F4 | K1,K4,K7,K8 | K1; K4 S019 absence; K7 n4; K8 clause |
| 10 | cookie: name preceded by `-` never starts a match | F6 | K1,K4,K7,K8 | K1; K4 S020 absence; K7 n5; K8 clause |
| 11 | cookie: 39-char value below the floor | F3 | K1,K4,K7,K8 | K1; K4 S021 absence; K7 n6; K8 clause |
| 12 | cookie: 40-char value meets the floor | F2, F7 | F7: K1,K4,K7,K8 | K1; K4 S022 expected hit; K7 g4/g5; K8 clause |
| 13 | cookie: capture scope only (practice report is not a capture) | **none** | — | **no control**: K4 report3.md absence and K8 clause are never exercised (M22 survives) |

K7 passes F8 (no JSON-newline case); K3 rejects F3 only because the lane tree contains a
round-90 receipt quoting the 28-char example, so clause 7's K3 guard is incidental lane
content, not a counter fixture.

## Attribution probes (necessity, not just observation)

Two union-ablation probes were built on top of the counter (probe sha256 in
`MutC2Counter-receipts/attribution-probes.txt`); both pass the landing, so they are
faithful to the counter's positive behaviour.

| probe | composition | landing | targeted control | verdict |
| --- | --- | --- | --- | --- |
| P1 `97b98ac6…` | K1 selftest ablated + E4 plant/clause removed from K4/K8 (`K8 clauses=12`) | pass | F8 -> **pass** (K1 det `selftest_rc=1`) | clause 6 guard set is exactly {K1-selftest, K4-E4, K8-clause-6}; removing all three makes the counter accept F8, while any two still reject |
| P2 `7164072b…` | K1 selftest ablated + S014/live-f/g6 removed (`K8 clauses=11`) | pass | F1 -> **pass** | clauses 1/2 guard set is exactly {K1, K4-S014, K4-live-f, K7-g6, K8-c1, K8-c2}; removing all makes the counter accept F1 |

Individual redundancy inside those sets is also measured: M17 (S014) alone, M18
(live-f) alone, M21 (E4) alone and M33 (g6) alone all survive — another limb catches
each. The counter is deliberately redundant; the cost is that the control set validates
only joint rejection.

## Findings (routed defects/qualifiers; the frozen predicate is not re-scored)

1. **Every forgery is caught by the instrument's own `--selftest` before any counter
   behavioural limb can be a sole guard.** `c2-controls-r91.sh` says unpinned forgeries
   are judged "only [by] the behavioural limbs (K2-K8)", but K1 runs `--selftest`, which
   is behavioural and fails on F1-F8 (`selftest_rc=1` in the frozen receipt and in every
   rebuilt variant). Consequence: 32/35 single-limb mutants survive; the 3 kills come
   from the landing, not from a forgery. To test a behavioural limb in isolation, a
   forgery must preserve `--selftest` (patch the regex and the matching selftest case
   together). Re-run: `bash .ufo/waves/round-91/controls/c2-controls-r91.sh <lane> <scratch>`
   (the frozen rebuild), then add such a selftest-preserving forgery.
2. **K6 is a counter-fixture self-check that no scanner variant can pin.** K6 reads the
   BASE_REV instrument from git, not the variant under test, and the no-work control's
   base instrument finds zero NEW_EXPECT members, so K6 passes on every control. M06
   (K6 ablated), M27 and M28 survive. Its only failure mode is a counter fixture in
   which a NEW_EXPECT plant is base-detectable (e.g., an E1-class plant moved into
   NEW_EXPECT). Re-run: same frozen controls; note `LIMB K6 pass` on no-work.
3. **K5 has no negative control.** `c2-controls-r91.sh` substitutes the frozen candidate
   SCORECARD row into every variant, including no-work, so K5 passes on all nine. M05,
   M34 (need tokens dropped) and M35 (`87` cell dropped) survive. Re-run: build a
   variant with the candidate instrument and the round-89 row (no
   `cloudfront-signed-cookie-signature` / `skdutid` tokens) — K5 must fail and no other
   limb should.
4. **Conjunct 13 (capture scope) is not covered by any control.** No forgery touches
   `is_capture_path`; M22 (report3.md plant + clause dropped) survives, so a counter
   that stopped checking that a practice report is out of capture scope is
   indistinguishable. Re-run: add a forgery that makes the cookie shape match under
   `corpus/practice/*/report*.md`; K4's exact set (and K8 clause 13) must fail (unless
   the instrument's scope selftest also fails first).
5. **K7 lacks a JSON-newline negative.** F8 passes K7 in the frozen receipt and in
   every rebuilt run; K7's cookie negatives cover case (n4), prefix (n5) and the 39-char
   floor (n6) only. Clause 6 therefore rests on K1+K4+K8 (P1 proves the set). Re-run:
   the F8 variant; `LIMB K7 pass` is the evidence.
6. **Paired sub-checks with no negative control.** K4 `rc==1` (M14), bad-allowlist
   `rc2==2` (M15), the `--files` sub-run (M16); K7 `rc==1` (M29); K2 `rc==1` (M11) and
   the `HISTORY_EXPECTED` pin (M12); K1's two sha pins (M09/M10); K3 `unused_allow`
   (M13). Each removes cleanly and every control still fails, so none is pinned by the
   control set, only positively by the landing. These are robustness margins, not
   defects; routed as control-coverage gaps for round 92.
7. **Design qualifier (not a defect):** the counter's exact-set K4 + clause K8 + the
   instrument selftest are three independent guards per positive conjunct. Single-limb
   defects are masked by construction, which is good for false negatives but means the
   r90 finding repeats in a stronger form: in round 91 *all eight* forgeries are
   multi-caught (no forgery isolates one limb), not merely most. The only single-guard
   exposure found is clause 13, and it has zero control coverage.

C2 itself is not re-scored: at the landing the frozen predicate passes, K1-K8 pass at
seeds 9191 and 1, and P3's path set is unchanged; these findings are qualifiers on the
control set's discriminative power, not on the claim.

## Receipts

All under `.ufo/waves/round-91/w1/MutC2Counter-receipts/`:

- `counter-baseline.txt` — frozen counter sha256; frozen command on the real lane;
  landing pinned (seeds 9191, 1), landing unpinned, and all nine rebuilt controls with
  the counter's own LIMB/verdict lines.
- `variant-revs.tsv` — the nine variant commit ids in this seat's clone.
- `mutant-index.tsv` — the 35 mutants and their sha256.
- `matrix.tsv` — 350 rows: mutant, case, counter rc, pass/fail, failing limbs.
- `killed-by-landing.txt`, `seed1-sweep.txt` — the three landing kills at both seeds.
- `attribution-probes.txt` — probe sha256 and the four probe runs (landing + targeted
  control for P1/P2).

## Cleanup / tooling

- Scratch `/fast/scratch/hyaku/kasegi-r91/MutC2Counter` removed before yield; no scratch
  files remain. No tool was installed or upgraded. No credential-shaped value was
  written to any wave file; receipts carry only sha256 digests, lane paths and the
  counter's LIMB/summary lines.
