# ExecConsiderthese — round 39 receipt (proposal 1: make distance-to-next-score explicit)

Seat: `ExecConsiderthese` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Item: mine `considerthese/2026-10-26.md` proposal 1 — measure the current gap and compose the
`SCORECARD.md` § Saturation addendum that states the concrete criteria for depth:verifiability 5
and coverage 8, plus the ledger row. Judged axis touched: depth:verifiability (measurement, no
score claimed). Round-39 base `480b1a505a2dfc14a4f718d16d63808247214d0a`; measured worktree
`7beae6098f58cba99b0a9d1ac387edc664c0abe4`.

## 1. Deliverables (byte-exact, beside this receipt)

| file | lines | bytes | sha256 |
|---|---:|---:|---|
| `ExecConsiderthese.scorecard.append.md` | 26 | 4897 | `a8c7af5293dc801a35fe46443f4f5b1bb6c757f2826d544b35db62f39398d707` |
| `ExecConsiderthese.ledger-row.md` | 1 | 1038 | `eb8d957dcf9295c691bee2db96a79184eabdb91c48aa52a8b960997159b00a3d` |

The scorecard file holds only landable bytes: one `##` block (`## Distance-to-next-score (round 39,
mined from considerthese 2026-10-26 proposal 1)`) with two `###` criteria subsections and the
`gap@r39:` line. No validation table, no scaffolding. Recommended landing slot: immediately after
`SCORECARD.md:321` (end of the § Saturation round-22 declaration, before `## Round 22` at `:323`);
an end-of-file append per R6 leaves the bytes valid. The ledger file is one 4-column row
(`proposal | status before | status after round 39 | evidence`) for the round-39 dispositions
section of `corpus/knowledge/considerthese-proposals-ledger.md`; the file's newest section uses a
5-column shape (`| status after round 37 | status after round 38 |`), so the L1 may prepend a
`round 38` cell without touching the row's text.

## 2. What the block states

- **depth:verifiability 4 → 5** — two limbs, both must read at the judged head: (1) `gated=0` in
  the `recheck-audit.py` breakdown (`executes=<n> gated=0 broken=0` with
  `parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`), a gated line being one that runs and fails
  closed on an absent base or a `LOST-RECORDED` anchor; (2) the `SCORECARD.md:331` bar,
  "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current
  claims", restated by dispositions row `corpus/knowledge/considerthese-proposals-ledger.md:54`.
  Measured distance: **24 gated of 50**.
- **coverage 7 → 8** — the r22 measure `(20 + F_admitted)/(20 + F_total) = 1.000` with `F_total`
  = frontier rows **plus** queued registry rows (`SCORECARD.md:332`; planned adoption at `:178`,
  never adopted — `corpus/lessons/round-23.md:173-177`). Measured: `41/50 = 0.820` strict,
  `41/41 = 1.000` frontier-only, `0/18` under the adopted r15 denominator. Distance: **9 queued
  rows to 0**, plus the operator-owned r15 re-base.
- No score move is asserted anywhere; the block says so in its first paragraph and in its
  `gap@r39:` line.

## 3. Measurements (commands run from the lane root, outputs verbatim)

### 3.1 Instruments

`…` marks output lines elided from a transcript; every line shown is verbatim.

```
$ python3 -B corpus/instruments/recheck-audit.py --root .
...
strict pass=50/50 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=26 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=50 missing=0 unexpected=0 exit=0        # EXIT=0

$ python3 -B corpus/instruments/score-gap.py
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=50 executes=26 gated=24 broken=0 exit=0
[2] anchors
anchorcheck: in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
census-lane: 134/1480 = 9.05%      census-skill: 32/506 = 6.32%
[4] score-5 threshold
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 50 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims   # EXIT=0
```

Instrument identity: `score-gap.py` sha256 `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf`
(554 lines), `recheck-audit.py` sha256 `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`.

### 3.2 Gated partition (the 24)

24 entries print `gated` in the recheck-audit table. Classifying each entry's own `recheck:` line:

```
23  test -d ~/Projects/... guard
 1  anchorcheck-only (citation-bases.md)
```

Entries naming each absent base (one recheck line per entry):

```
entries_naming_bounties=23   entries_naming_tbh=6   entries_naming_origin=1
```

`citation-bases.md` is the one non-guard: `python3 -B corpus/instruments/anchorcheck.py
corpus/knowledge/citation-bases.md` → `LOST-RECORDED md:52`, `BASE-ABSENT md:31`, **EXIT=1**.
The block therefore says the 24th fails on a `LOST-RECORDED` anchor and a `BASE-ABSENT` anchor,
and that `score-gap.py`'s phrase "gated on a lost base" over-covers that entry by exactly one.

### 3.3 Coverage counters

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                   -> 21
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md -> 21
$ # non-admitted frontier rows: 0
$ python3 -B corpus/instruments/frontier-recheck-count.py | tail -1             -> entries=24 pass=24 exit=0
$ python3 -B - <<'EOF'   # parse corpus/SOURCES.md registry rows, count status cell
...                        -> rows 55: mined 43, queued 9, rejected 3
queued ids: S016 S017 S019 S020 S021 S022 S023 S024 S025
```

Arithmetic in the block: `(20+21)/(20+30) = 41/50 = 0.820` (strict), `(20+21)/(20+21) = 41/41 =
1.000` (frontier-only). The Core constant 20 is the r22 proposal's own term and has no per-item
derivation in the lane: `git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/`
returns one line, `SCORECARD.md:332`.

Registry at base is 55 rows / 43 mined / 9 queued / 3 rejected (`.ufo/waves/round-39/claims-erratum-1.md`
E1 fixes the post-round count to 59, which the block does not assert).

### 3.4 Base equivalence of the measured bytes

```
$ git diff --name-only 480b1a505a2dfc14a4f718d16d63808247214d0a HEAD | grep -vc '^\.ufo/waves/round-39/'
0
$ git status --porcelain -- corpus SKILL.md SCORECARD.md PROVINCE.md considerthese/
(no output)
```

So every figure the block labels "measured at base `480b1a5`" is the value of the base bytes.

### 3.5 Block self-check (every backticked command in the deliverable re-run)

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                         -> 21
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {…}' …      -> 21
$ python3 corpus/instruments/frontier-recheck-count.py               -> entries=24 pass=24 exit=0
$ git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/ -> SCORECARD.md:332 only
$ python3 corpus/instruments/recheck-audit.py --root .               -> gated=24 of lines=50, exit=0
```

Citations used and checked: `SCORECARD.md:331` (threshold), `SCORECARD.md:332` (r22 measure),
`SCORECARD.md:178` (planned adoption), `corpus/lessons/round-23.md:173-177` (adoption declined),
`corpus/knowledge/considerthese-proposals-ledger.md:54` (round-37 dispositions row for proposal 1),
`PROVINCE.md:5-19` (root-loss annotation), `PROVINCE.md:121-122` and `corpus/README.md:55-56`
(`0/18`), `.ufo/waves/round-23/build/CoverageDenom.md` § Finding 4 (queued rows are uncovered
surfaces).

## 4. Risks / limits of the landed text

1. **The coverage denominator is a judgment, stated explicitly.** The r22 text reads "Frontier
   topics"; taken literally today it yields `41/41 = 1.000`, which cannot discriminate 7 from 8
   (numerator and denominator grow together). The block uses the r23 audit's own objection
   (unmined queued rows are uncovered surfaces) to widen `total`, and prints the frontier-only
   reading beside the strict one so a reader can reject the choice without re-deriving it.
2. **The Core term "20" is prose-only.** No committed command counts Core items; the block says
   so and holds C constant. A verifier who refuses an underived constant can still re-run both
   moving terms (frontier rows, queued rows) and the harness.
3. **`score-gap.py`'s gap sentence over-covers by one** (absent-base phrase vs
   `citation-bases.md`'s `LOST-RECORDED` anchor). Quoted verbatim as the instrument prints it,
   with the one-entry correction stated in the same subsection.
4. **Post-round numbers differ from the measured ones.** C2 lands F22/S057–S059, so frontier
   becomes 22 and registry 59 while queued stays 9; the block asserts only base values and the
   structural property that admitted topics grow both terms.
5. **The ledger row says `mined round 39`** and names the SCORECARD heading as the landing. If
   the L1 lands the block under a different heading or drops it, that row must be re-stated, not
   edited (append-only, R6/R9).

## 5. Cross-seat overlap (L1 decision needed, not a blocker)

Sibling seat `ExecConsidertheseLedger` delivers the whole round-39 dispositions section
(`ExecConsidertheseLedger.ledger.append.md`, 27 lines / sha256
`8becfdf77c472af27234fb783f7612ad1a7b767140ff0270175bb2eac3fe3c70`), whose row 1 covers the
same proposal in a 3-column shape (`proposal | status | evidence`). Two consequences:

1. **Shape collision.** My `ExecConsiderthese.ledger-row.md` is 4 columns (`proposal | status
   before | status after round 39 | evidence`). Landing both would break the table; the L1 lands
   one. If the sibling section lands, my row is redundant and must not also land; if my row lands,
   the sibling's row 1 is the duplicate.
2. **Stale digest — resolved, not carried.** An earlier revision of that block quoted my
   scorecard block as sha256 `3a67156951…d95d8e50`. I corrected one citation in my block
   (`PROVINCE.md:8-18` → `PROVINCE.md:5-19`; still 26 lines / 4897 bytes; current digest
   `a8c7af5293dc801a35fe46443f4f5b1bb6c757f2826d544b35db62f39398d707`) and messaged the seat; the
   final sibling block names the path and the exact heading and pins no digest. Measured by this
   seat on the final file: `grep -c '3a671569'` → `0`, `grep -c 'a8c7af52'` → `0`. Neither file
   carries a stale digest now.

No blockers. No score move claimed by this seat. No tool installed or upgraded. Scratch
`/fast/scratch/hyaku/kasegi-r39/ExecConsiderthese/` removed before yield; the only lane writes
are the two deliverables above and this receipt.
