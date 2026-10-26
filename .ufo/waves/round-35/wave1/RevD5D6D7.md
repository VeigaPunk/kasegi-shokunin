# RevD5D6D7 — D5/D6/D7 fix review (round 35, wave 1)

Seat: `RevD5D6D7` (reviewer, L2 leaf of the kasegi round-35 wave). Item: review the D5/D6/D7 fixes —
(1) `claims-erratum-d5.md` exists with both required literals (`discriminating invocation`, `per-id occurrences`);
(2) `L1Integration.md` stale dead-seat sentence gone + `Correction (round 35)` note appended;
(3) `QUALITY.md` appended supersedes-R22 / supersedes-R23 rows with correct grounding (M34-3 for R22; round-34 lesson for R23);
(4) appends discipline. Verdict with evidence.

- Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`; HEAD at review start `da2d3c687f82a9814ee71c91c930cb733050d37c`; L1 integration commit observed during review `aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b` ("round-35: L1 integration — C1 D4/D6/D7 lands …").
- Method: read-only (git status/show/cat-file/diff/hash-object, fixed-string grep counts, sha256sum, suite runs, scratch fixture re-runs). No tooling installed (nothing needed beyond coreutils/python3/jq already present; pacman paused host-wide, no package transaction ran). No subagents, no git/jj mutation, no writes outside the lane.

## Report

### 0. Before state (measured at review start, HEAD `da2d3c68`)

| check | command | observed | exit |
|---|---|---|---|
| D5 erratum file | `ls .ufo/waves/round-35/claims-erratum-d5.md` | absent at first check; landed during this review (seat `ScribeErratumD5`), then revised to final bytes (trail in §1) | 0 after landing |
| D6 stale sentence | `grep -c -F 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md` | `1` (line 30; bullet spans :30-32) | 0 |
| D6 correction note | `grep -c -F 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md` | `0` | 1 |
| D7 rows | `grep -c -F 'supersedes R22' corpus/QUALITY.md` / `'supersedes R23'` | `0` / `0` | 1 / 1 |
| L1Integration.md | `wc -l` + `sha256sum` | 37 lines, `5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5` | 0 |
| QUALITY.md | `wc -lc` + `sha256sum` | 229 lines / 30,889 B, `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` (matches ScribeQualityDraft's before-read) | 0 |

Suite timeline across this review: `closed=3/7` (ScribeQualityDraft §3 before-read, D5 absent) → `closed=4/7` (this seat, D5 landed) → `closed=6/7` (D6+D7 landed, D4 untracked) → **`closed=7/7 exit=0`** (final, after the L1's commit `aa6ad99` tracked `wave1-results.json`).

D6 premise verified first-hand: `.ufo/waves/round-34/wave1/ExecRegressionC1.md` IS committed — `git cat-file -e 617496b…:.ufo/waves/round-34/wave1/ExecRegressionC1.md` → yes; same at `c1c6a5f…` → yes; working-tree sha `6b3604cb6d5aca94e68f2b2a66aaaaee5ed9c3e2856ba9f7c5c13cd32b06de83` (matches round-34-verifier-spotcheck §1's "sha back to `6b3604cb`"). Per spotcheck §2, `git diff --stat 4b0a9f2 c1c6a5f` touches `ExecRegressionC1.md` — the receipt landed between the integration commit and the round-34 tip, after the note was written, so the note's dead-seat claim is stale at tip. Exactly D6.

### 1. D5 — **closed, verified**

File `.ufo/waves/round-35/claims-erratum-d5.md`, final bytes **`eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6`**, 262 lines / 13,086 B (stable across the last three reads; still untracked at HEAD `aa6ad99` — pending the L1's closing commit, see §4).

Literals (this seat's measurement, `grep -c -F`): `discriminating invocation` → **5** (lines 70, 75, 77, 199, 239); `per-id occurrences` → **5** (lines 140, 163, 183, 202, 241). Suite: `D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0`.

Content vs the D5 fix (round-34-verifier-spotcheck.md:189-194, verified at :189): §2 records the two non-discriminating routes (the twin's own `recheck:` line re-checks the real manifest → exit 0; the instrument pointed at the twin `.md` → exit 2 for any non-manifest); §3 restates clause 1 with the discriminating invocation (the twin's fabricated sentence pinned in a manifest against the committed capture → `MISMATCH reason=quote-not-found`, exit != 0, with a present-quote control at exit 0); §4 restates clause 2 as per-id occurrences (16×`occurrences=1`, Q9/Q17 `occurrences=2` anchored 77/96; unanchored non-unique fails `occurrence-not-unique`; broken anchor fails `anchor-broken`); §6 states the forward rule (future twins carry only absent sentences) with measured counts; §5 discloses the verbatim recurrence in round-35's frozen C2 without editing the freeze; §8 states non-effects (no score change, no adjudication, no round-35 after-state claims).

**Independent re-verification (this seat, scratch fixtures — every measured claim in the erratum reproduced):**

| run | expected (erratum) | measured | exit |
|---|---|---|---|
| committed round-34 capture digest | `4fd8ed98…b325a5` | `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` | — |
| A1: real-manifest recheck (twin's own recheck target) | 18 assertion lines, Q9/Q17 `occurrences=2` anchored, exit 0 | identical listing | 0 |
| A2: instrument pointed at the twin `.md` | `manifest UNAVAILABLE reason=unreadable-or-invalid` | same | 2 |
| B1: fabricated quote `five severity levels for smart-contract exploits` | `S051:J1 MISMATCH reason=quote-not-found` | same | 1 |
| B2 control: real quote, anchor 46 | `S051:Q1 OK occurrences=1 anchor=46-ok` | same | 0 |
| C1: `Permanent freezing of funds` anchor 77 | `S051:Q9 OK occurrences=2 anchor=77-ok` | same | 0 |
| C2: same, no anchor | `S051:Q9 MISMATCH reason=occurrence-not-unique` | same | 1 |
| C3: same, anchor 1 | `S051:Q9 MISMATCH reason=anchor-broken` | same | 1 |
| `source-recheck.py --selftest` | `cases=10 failures=0` (incl. all four double-occurrence limbs) | same | 0 |
| round-35 S052 capture digest (§5) | `d69349e8…8826` | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` | — |
| §6 normalized counts (S051 real/fabricated; S052 both) | 1 / 0 / 0 / 0 | 1 / 0 / 0 / 0 | — |

Frozen-quote fidelity verified against both frozen files (`grep -c` → 1 each): round-34 C2 predicate span "source-recheck S051 prints every assertion occurrences=1, sha256 OK, exit 0; census exit 0 (W04 S028/S029 only); the junk F17 twin (c2-controls/junk-f17.md) is rejected by the admission gate."; "source-recheck exit != 0; reviewer REFUSE"; "junk twin rejected: source-recheck exit != 0 and non-author reviewer REFUSE on record"; "junk twin passes source-recheck or is admitted"; round-35 "source-recheck S052 prints every assertion occurrences=1" and the same after[6] sentence.

**Attribution table verified per-field** (jq over `.ufo/waves/round-34/claims.json`): C2.`predicate` ✓, C2.`after[6]` ✓, **C1.`after[10]`** ✓ (the "(source-recheck exit != 0; reviewer REFUSE) (R9)" sentence lives in C1's after-list, not C2 — the seat corrected the erratum's original C2 attribution mid-review and the correction is right; no before/predicate/kill_rule hit for that sentence), C2.`kill_rule` ✓.

**Post-review fixes by `ScribeErratumD5`, all verified on the final bytes:** (a) §2's original "byte-identical" claim removed (`grep -c 'byte-identical'` → 0) and replaced with the accurate difference statement ("targets the same manifest and `--source S051` as the admitted entry's line …; the only differences are the entry's `cd <lane-root> &&` prefix and its trailing comment" — measured: twin `junk-f17.md:11` has neither; entry `:6` has both, identical at `c1c6a5f` and `617496b`); (b) §3's reproduction scratch path genericized to `S="$(mktemp -d)/S051"` (`kasegi-d5` count 0); (c) §3's kill-rule phrasing made exact ("is the rejection the frozen kill rule presupposes" — the kill rule keys on the twin *passing*); (d) §5 "repeats the same phrasings verbatim" (three fields, two phrase classes). The seat's receipt §8 pins the final digest with the revision trail (`ScribeErratumD5.md:251,254-259`).

Appends: new appended correction file; neither frozen `claims.json` touched (`git status` shows no claims.json modification at any point).

### 2. D6 — **closed, verified** (shape nuance recorded for the L1)

Landed and committed (blob `557957a4b359ed25c79c91c829065c084fae0bf2` in HEAD `aa6ad99`; working copy clean). File now 40 lines / 3,714 B, sha `76f190a003931aee3bfbab7fec10aa657c0d64584d0cc0c7fd88b02b3679dc2d`.

| clause | command | observed |
|---|---|---|
| stale sentence gone | `grep -c -F 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md` | `0` |
| correction note present | `grep -c -F 'Correction (round 35)' …` | `1` (line 34) |
| suite | `bash corpus/instruments/r35-defect-closure.sh` | `D6 check=dead-seat-sentence=0,correction-round-35=1 open=0` |

Diff vs freeze `617496b` (`git diff --numstat`): **6 additions / 3 deletions**. The three deleted lines are exactly the stale bullet (`:30-32`). The landed replacement, quoted from the diff:

```
- The round-33 summary `ExecRegressionC1` filed its receipt, committed in `c1c6a5f`
  (round-34 closure); the regression battery is covered by that receipt plus this L1
  re-run and `wave1/ExecRDefectClosureSuite.md` §5 (base `closed=0/9`, exit 1).

- Correction (round 35): the bullet above was corrected in place — the dead-seat claim
  was false; the `ExecRegressionC1` receipt is committed in `c1c6a5f` (round-34 closure).
```

Replacement content verified: the receipt IS committed in `c1c6a5f` (and the freeze `617496b`) — `git cat-file -e` yes at both.

**Shape nuance (flagged for the L1, not a defect verdict):** the fix is an **in-place correction of the stale bullet plus an adjacent disclosure note** — 3 deletions, and the note sits after the corrected bullet (mid-file, `:34-35`), not at EOF. This shape is forced by the suite's own D6 clause (`dead-seat-sentence == 0`: leaving the sentence and only appending a note would read `open=1` → `closed=6/7` → a C1 kill), and it is disclosed, not silent — the note itself says "corrected in place", which is the R9-compliant pattern (R9 forbids *silently* rewriting filed assertions; the same replace+disclose pattern is D1's assigned fix). The note also avoids the trap this seat flagged pre-landing: it paraphrases ("the dead-seat claim was false") and does not quote the literal `did not file a receipt (dead seat`, so the suite's `D6:+dead-seat-sentence` mutant condition (r35-defect-closure.sh:389-392) is not tripped — `stale_count=0` with the note present proves it. If the L1 reads the item's "All must be appends" as zero-deletion/EOF-only, D6's 3 deletions and mid-file placement are the deviation to rule on; under the suite's clause and the claims.json after-list ("corrected by an appended note") the landed shape is the intended one.

### 3. D7 — **closed, verified**

Landed and committed (blob `4b675483f2cec11a6c983702b1cc5053e5731be2` in HEAD `aa6ad99`; working copy clean). File now 250 lines / 33,731 B, sha `d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69`.

| clause | command | observed |
|---|---|---|
| rows present | `grep -c -F 'supersedes R22' corpus/QUALITY.md` / `'supersedes R23'` | `1` / `1` (rows at :249, :250) |
| pure append | `git diff --numstat 617496b -- corpus/QUALITY.md` | `21  0` — additions only, zero deletions |
| byte-prefix proof | `head -c 30889 corpus/QUALITY.md \| sha256sum` | `807cc714…b74a8` — byte-identical to the pre-append file |
| draft applied verbatim | `tail -c 2842 corpus/QUALITY.md \| sha256sum` | `e3aa99a16b725335ceac2928f61d2d65ff1cc4e105c9c150fe51f2985eaa6918` — equals ScribeQualityDraft §1's declared block hash (independently extracted and hashed by this seat before landing) |
| suite | `bash corpus/instruments/r35-defect-closure.sh` | `D7 check=supersedes-R22=1,supersedes-R23=1 open=0` |

Grounding text verified against ground truth (every cited span re-opened by this seat):

- **R26 row (:249) — supersedes R22.** States R22's Grounded-in column cites M34-2; that M34-2 is the SCORECARD unfilled-placeholder defect (R1 class — round-34 lesson :254-257 confirms M34-2 is the `<LANE_HASH>` placeholder mistake); and that the correct mistake is **M34-3**, the freeze-satisfiability row minted at `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` (round-34 lesson open item 10, `:482-485`, which states verbatim that `QUALITY.md:226` cites M34-2 "while M34-2 is the marker defect … the correct grounding is M34-3"). ✓ matches the item's "M34-3 for R22". The row also carries the new distance-to-next-score criterion (grounded in `considerthese/2026-10-25.md` proposal 2, verified at :53-57) with the runnable form citing the `score-gap.py` command rather than a volatile figure (R19-compliant) — satisfying the non-claim frontier item "proposal 2 mined into QUALITY R26" without an id collision.
- **R27 row (:250) — supersedes R23.** States R23's Grounded-in column cites `considerthese/2026-10-25.md:76` proposal 6 alone (verified accurate at :76) and that the landed grounding is the round-34 lesson's own §considerthese disposition (`corpus/lessons/round-34.md:343-358`: proposal 6 "mined → landed" as R23, including the recorded narrowing against the draft's block). ✓ matches the item's "round-34 lesson for R23". R23's criterion text is restated unchanged ("R23's criterion is unchanged by this row"); the narrowed disposition limb is deliberately not restored (ScribeQualityDraft F5 — a bar decision the L1 owns, outside this item's scope).
- Block preamble: quotes spotcheck :199-203 (D7 — verified at :199) and mistakes-erratum-1.md:18-20 (the "Captured by: `none` at freeze time — `QUALITY.md` R22 … had no planned-state limb" lines — verified) verbatim; declares the byte-prefix proof it then satisfies.

### 4. Final suite state, commit state, digest stability

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
```

Commit state at review end: HEAD `aa6ad99` (L1 integration) contains L1Integration.md (blob `557957a4`) and QUALITY.md (blob `4b675483`) — both working-copy clean, i.e. the verified bytes are the committed bytes — and tracks `wave1-results.json` (`git ls-files … | wc -l` → 1, closing D4's tracked limb). **`claims-erratum-d5.md` is still untracked** (`??`) — its D5 clause passes on the working tree the suite measures, but a post-closing-commit re-run of the suite needs the erratum inside the closing commit; the L1's closing commit must include it (the round-34 pattern committed its erratum with the round).

Erratum digest stable across the last three reads: `eee0bb57…` (262 ln / 13,086 B); `ScribeErratumD5.md` §8 pins the same digest with the revision trail.

### 5. Findings for the L1

- **F1 — RESOLVED during review.** The erratum §2 originally claimed the twin's `recheck:` line was "byte-identical" to the admitted entry's line; measured not byte-identical at any revision (twin `junk-f17.md:11` = `recheck: python3 … --source S051`; entry `:6` adds the `cd … &&` prefix and a trailing comment; identical at `c1c6a5f` and `617496b`). Flagged to `ScribeErratumD5`; fixed and verified on the final bytes (`byte-identical` count 0). The operative claim (same manifest+source → exit 0 → non-discriminating) was verified throughout.
- **F2 — trap avoided (verified).** The suite greps the whole L1Integration.md for `did not file a receipt (dead seat`; the landed Correction note paraphrases and does not quote the literal — `stale_count=0` with the note present proves it.
- **F3 — RESOLVED during review.** Erratum §3's documented reproduction scratch path (`/fast/scratch/kasegi-d5/S051`, outside the round's `/fast/scratch/hyaku/kasegi-r35/<seat>/` convention) genericized to `S="$(mktemp -d)/S051"` — verified on the final bytes.
- **F4 — RESOLVED.** Digest bookkeeping: the erratum dropped its in-file self-digest (correct design — "a digest written inside the file it measures is stale the moment it is typed") and the seat's receipt §8 pins the final digest with a revision trail naming this seat's verification of the intermediate `2f4fae0a…` bytes.
- **F5 — attribution correction verified.** Erratum §1 now attributes the "(source-recheck exit != 0; reviewer REFUSE) (R9)" sentence to **C1 `after[10]`**, not C2 — verified by jq (exactly `C1.after[10]`; no other field hit). Note: round-34-verifier-spotcheck.md §6 D5 itself called it a "C2 junk-twin phrase"; the erratum's correction is the accurate reading and explains the routing.
- **F6 — D6 shape nuance (L1's call if it reads "appends" strictly).** See §2: in-place correction + adjacent disclosed note (6+/3− vs freeze), forced by the suite's D6 clause; D5 (new file) and D7 (21+/0−, byte-prefix proven) are pure appends.
- **F7 — erratum tracking (action for the closing commit).** `claims-erratum-d5.md` is untracked at HEAD `aa6ad99`; the closing commit must include it so the D5 clause holds on the committed tree (see §4).

## Verdict

**All three fixes: closed and verified.**

- **D5 — PASS.** `claims-erratum-d5.md` exists at `.ufo/waves/round-35/claims-erratum-d5.md` (final bytes `eee0bb57…`, 262 ln / 13,086 B) and contains both required literals (`discriminating invocation` ×5, `per-id occurrences` ×5). Every measured claim in it reproduced first-hand (capture digests `4fd8ed98…`/`d69349e8…`; A1/A2/B1/B2/C1/C2/C3 fixture runs matching §2-§4 exactly; `--selftest` `cases=10 failures=0`; §6 counts 1/0/0/0). Frozen-quote fidelity and the §1 attribution table verified against both frozen claims.json files. Suite: `D5 … open=0`. Untracked at HEAD — closing commit must include it (F7).
- **D6 — PASS** (shape nuance recorded, §2/F6). Stale dead-seat sentence gone (`grep -c` → 0; bullet corrected in place to factually-verified content), `Correction (round 35)` note present (×1, `:34`), suite `D6 … open=0`. Disclosed, not silent (R9-compliant); avoids the literal-quoting trap. Committed in `aa6ad99` (blob `557957a4`).
- **D7 — PASS.** QUALITY.md carries the appended `## Round-35 supersession` block with `supersedes R22` (:249) and `supersedes R23` (:250) rows; grounding text correct (M34-3 for R22 — mistakes-erratum-1.md:9-29 / lesson open item 10 :482-485; round-34 lesson §considerthese :343-358 for R23); pure append proven three ways (numstat 21+/0−; byte-prefix sha `807cc714…` unchanged; landed block hash == draft block hash `e3aa99a1…`). Suite: `D7 … open=0`. Committed in `aa6ad99` (blob `4b675483`).
- **Appends discipline:** D5 and D7 are pure appends; D6 is the suite-required removal paired with a disclosed appended note (reasoning in §2). Neither frozen `claims.json` was touched by any of the three fixes.

Residual (outside this item): suite `closed=7/7 exit=0` on the working tree; the erratum awaits the closing commit (F7).

### Scratch cleanup

`rm -rf -- /fast/scratch/hyaku/kasegi-r35/RevD5D6D7` executed before yield; `test -e` → rc 1 (gone). The seat's verification scripts and fixtures lived only there; every evidence value is quoted above.

Report: .ufo/waves/round-35/wave1/RevD5D6D7.md
