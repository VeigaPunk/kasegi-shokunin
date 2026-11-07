# CriticClaimsC1 — round-95 w1, C1 critic (depth:verifiability)

Seat: CriticClaimsC1. Round 95 attempt 1, wave 1, 2026-11-07.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`,
freeze `347519f21524d2bc13eb6c91cf3550930a4265b3`, C1 landing `53ec479d71d25cf5be052db794a548a5904564b8`.
Read-only on the lane's git state; all fixtures are `git clone --shared` copies in scratch; scratch removed after the seat.

## Verdict

**C1 STANDS** on the frozen predicate P1–P3 at the landing `53ec479d71d25cf5be052db794a548a5904564b8`.

Observed limb values, from a fresh shared clone of the landing (not the live worktree):

- `KNOWLEDGE-METER-RESULT pass rc=0`
- M0 base=`1007/1998`; M1 after=`1008/1994`; M3 `same_files=True bad_lines=0 old_not_once=0 dup_rows=0`
- M4 `bad=none`; M5 `out_of_range=none`; M9 `rows=16 unbound=none`
- M10 `labelled=16 want=16 mapped=16 kinds=cell-repair=4,part=5,range=7 unknown=none` (EXCLUDED set is empty, see §5.1)
- M6 `sha256=8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6`; `after_rev=53ec479…`
- P2: counter `c0799f4c…`, map `8545eba2…`, labels `cf739497…` — all equal the pins at freeze, landing and live worktree.
- P3: the landing commit (parent = the freeze) changes exactly `corpus/knowledge/triage-thresholds.md` and
  `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (`5/5` and `9/9` insertions/deletions; 14
  changed physical lines), nothing else.
- Controls: re-run against a clone of the landing, 15/15 reproduce (`C1-CONTROLS-RESULT pass controls=15`, rc 0);
  every CONTROL line and every LIMB line is identical to the committed receipt — only the
  `candidate=<rev> work=<dir>` header differs.

The strongest counterexamples I could construct are recorded in §4 and §5. They expose the frozen counter's
semantic blindness and its scope boundary, but none is a limb FAIL, none changes P2/P3, and no control fails to
reproduce. Where the claim's *statement* makes a semantic assertion beyond the predicate ("new text is true of
the anchor they cite"), I re-read all sixteen new texts against their anchors myself; the result is in §5.

## 1. P1 — frozen counter, re-run independently

Fresh clone (`git clone --shared -q . $S/lane`, toplevel asserted = the clone dir; base/freeze/landing all
`commit`), then the exact frozen invocation:

```
TMPDIR=$S/work python3 -B .ufo/waves/round-95/c1/knowledge-meter.py \
  --lane $S/lane \
  --base-rev 9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10 \
  --after-rev 53ec479d71d25cf5be052db794a548a5904564b8 \
  --map .ufo/waves/round-95/c1/repair-map.tsv \
  --labels-rev 347519f21524d2bc13eb6c91cf3550930a4265b3 \
  --base-target 1007/1998 --target 1008/1994 \
  --map-sha256 8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6 \
  --work $S/work
```

rc `0`. Full output in `01-counter-run.txt`. The header prints `after_rev=53ec479d71d25cf5be052db794a548a5904564b8`,
`mirror_absent=True`, `pinned=archive`; every recorded value matches P1, including the M10 kind tally
`cell-repair=4,part=5,range=7` and the frozen map sha.

Independent cross-check of the composition (not via the counter): for both files I applied each map row's
old→new to the base line and compared with the landing line — 14 changed physical lines, exactly the 14 mapped
site lines (9 in `triage-thresholds.md`: 88, 89, 90, 356, 396, 433, 434, 435, 436; 5 in
`iso-29147-divergence-and-clause-crosswalk.md`: 13, 34, 43, 54, 64), `mismatches 0` (`06-line-map.txt`).

## 2. P2 / P3

Blob sha256 at the freeze and at the landing (`git show <rev>:<path> | sha256sum`):

| file | freeze | landing | pin |
|---|---|---|---|
| `knowledge-meter.py` | `c0799f4c…8db8` | `c0799f4c…8db8` | same |
| `repair-map.tsv` | `8545eba2…beb6` | `8545eba2…beb6` | same |
| `labels.tsv` | `cf739497…79d0` | `cf739497…79d0` | same |

`git show --name-status --format= 53ec479d…` → exactly the two `M` lines; `git rev-list --parents -n1` →
parent `347519f21…`; `git diff --numstat 347519f… 53ec479d…` → `5 5` and `9 9`. P3 holds as a commit-level
statement (the landing commit against its parent); the two files are the only paths it touches.

## 3. Controls reproduce after the landing (round-94 defect 1)

```
TMPDIR=$S/work python3 -B .ufo/waves/round-95/controls/c1-controls-r95.py \
  $S/lane .ufo/waves/round-93/c1/knowledge-meter.py $S/work $S/out
```

rc `0`; `C1-CONTROLS-RESULT pass controls=15`. Observed CONTROL lines: `candidate rc=0`; `do-nothing rc=1`;
`partial-row-dropped`, `extra-unlisted-edit`, `wrong-new`, `m5-out-of-range`, `snapshot-missing`,
`wrong-map-sha`, `unlabelled-row`, `part-as-cell`, `cell-repair-lane-root`, `two-cells-one-line` all rc 1;
`missing-labels rc=2`; `union-applied rc=0` and `union-applied-before-r93 rc=1` with `Traceback`. All named
limbs appear in the expected controls (M10, M3, M9, M5, M4, M6). Diff against the committed receipt: CONTROL
lines identical except the candidate rev/work path header; all LIMB lines byte-identical (`03-…diff.txt`).

Round-94 defect 1 (before-fixture reading the mutable lane) is repaired in the harness as built: every
invocation passes `--base-rev BASE` (harness line 110), and the counter's before reading is
`git archive <base-rev>` from the clone, so the before state is the pinned base in every control; the fixtures
are clones of the candidate clone by commit, not the live worktree. The committed receipt's
`candidate=4ef12a2f…` is a pre-landing clone rev (not an object in this repo); re-running at `53ec479d…`
prints the same limbs, which is what this seat verified.

Residual non-hermeticity (benign, routed): the harness reads `MAP` from the live-lane path for `real_sha` and
for control #5's template, and the candidate control uses that path rather than the clone's map. The map is
hash-identical (`8545eba2…`) and M6 would fail on drift, so this cannot silently pass.

## 4. Four forgeries of my own (fixtures cloned from the landing; full logs in `10-forgeries.txt`)

| # | Forgery | Observed | Reading |
|---|---|---|---|
| F1 | `356` cell rewritten to `MATCHES: SKILL.md:999 (the parking-invisibility sentence; …)` — in range, false of the anchor, same token set | rc `0`, all limbs pass | the counter cannot judge prose truth; M5 is range-only and M9 binds the row to the (forged) label |
| F2 | `90` part edit to `` `SKILL.md:182-184,255-257` (term omitted) `` — the old premise "(term omitted)" survives | rc `0`, all limbs pass | M9 checks the edit the label names, never that the old premise was removed |
| F3 | the same cell plus a bare `` `S041.txt` `` token | rc `1`, `M1 FAIL after=1008/1995` | a re-added bare capture token inside the measured scope is caught by the exact rate target |
| F4 | a new row at `143` repointing `` `SKILL.md:251-253` ``, while the same token still stands on line `151` (in scope) | rc `0`, 17 rows/labels, rate unchanged | a per-site repoint cannot remove a token cited twice; the map is per-site and the rate is token-membership, so the survivor is not flagged |

F1/F2 show the predicate's ceiling, not a landing defect: the actual sixteen new texts were authored under the
frozen labels and I read them against their anchors (§5); F3 shows the rate target is a real guard; F4 is the
shape of the two landed rows whose old text also occurs outside the meter's scope (§5.3).

## 5. Semantic limb, scope and wording — read, not inferred

### 5.1 M10 "excluded=0" is a state, not a printed field

The frozen counter has `EXCLUDED = {}` (line 106) and its M10 print line carries
`labelled=… want=… mapped=… kinds=… unknown=… unapplied=… unlabelled=…` with no `excluded=` field
(`09-harness-pins.txt`). The empty set is verified from the pinned source and from the tally (no `excluded`
kind); M10's `set(EXCLUDED) <= set(kinds)` is vacuous. A predicate read as a literal substring test for
`excluded=0` would not be met by the printed line; a read on the values is met. This is a wording mismatch in
the frozen predicate, not a limb failure.

### 5.2 Anchor truth of the sixteen new texts

I read each new text against the cited anchor at the landing (`07-anchors.txt`):

- **Five S041 repoints** — `corpus/source-snapshots/round-30/S041.txt` exists (2354 lines), sha256
  `e18acbf9…ab47`, byte-identical to the round-26 capture the entry's header cites; the ranges in the new texts
  (1868-1870, 1792-1867, 1996-2079, 1868) are all inside the file, and 1868-1870 is the policy-divergence
  sentence the cells quote. No false provenance.
- **356** — `SKILL.md:999` is the program-record schema bullet (`~/Projects/bounties/bounty-map/schema.json —
  program record schema …`); `SKILL.md` contains no required-key enumeration (`grep` for the key list returns
  nothing), so the cell's parenthetical is supported.
- **396** — `SKILL.md:335-338` states the `gitMutationBlocker` fail-closed rule; the cell keeps
  `ops-invariants.md:24` for the marker/code list.
- **436** — `corpus/knowledge/mission-control.md:21-27` completes the negative-EV/`ev_note` substance that the
  old 21-23 range cut at "the negative-EV dispatches carry an".
- **435** — the `EV ordering` phrasing is 0× in `SKILL.md`; `SKILL.md:182-184` puts `curated` third
  (`priority > continue > curated`).
- **88 / 89 / 90 / 433 / 434** — the `SKILL.md:182-184` anchor states the five-term ordering including
  `reward.min×1000` and `is_live(1)`; `255-257` (cited by 88, 90 and 433) states the curated-boolean correction.

Strongest counterexample: in these last rows the cited `SKILL.md:182-184` stops one line before the correction
clause completes — line 184 ends `(round-13 correction: earlier`, and `text omitted is_live(1)`)` is on line
185. Two of them (89, 434) additionally assert "the earlier text wrote `reward.min`", which is a historical
claim about the superseded text and is not stated by the anchor (the anchor's correction note names only
`is_live(1)`). The anchors do contain the operative current-form claims (`reward.min×1000`, five terms,
curated boolean, curated third), so this is a one-line under-citation / historical aside, not a falsity of the
anchor's content. If the judge reads "true of the anchor" as requiring the full quoted clause inside the
range, these four cells (88 part 1, 89, 90, 434) cite a clause the anchor does not fully contain — 88 and 90
stop one line short of the `is_live(1)` correction, and 89/434 assert an earlier-text `reward.min` that the
anchor never states; the package and landing are frozen and
the kill rule forbids re-labelling after landing, so that is a next-tranche precision fix only.

### 5.3 Scope boundary of the meter

The meter's scope is `corpus/knowledge/*.md`. Two landed rows remove a token that still survives outside that
scope: `SKILL.md:245-247` (row 396) also stands in `corpus/instruments/citation-survival.md`, and bare
`S041.txt` (row 64) also stands in `corpus/lessons/round-26-verifier-spotcheck.md`,
`corpus/lessons/round-30-verifier-spotcheck.md` and `corpus/lessons/round-30.md` (`08-dup-old-scan.txt`). The
crosswalk file itself still cites the capture bare at lines 23-28 (ranged forms other than the five repointed);
line 3 carries the full `corpus/source-snapshots/round-26/S041.txt` path (INTERNAL), while line 47 is a
backticked shell command (`grep -cF …`), not a path citation. The claim is scope-local ("the citation meter
reads …") and the five rows are precisely the round-94 rows, so this is not a claim violation; it does mean the
reading must not be quoted as a repo-wide "old anchors gone".

Independent arithmetic (`05-token-diff.txt`): base (1007, 1998), after (1008, 1994); 12 tokens removed (5 GONE
bare `S041.txt*` + 7 INTERNAL old anchors), 8 added (all INTERNAL: `SKILL.md:182-184`, `SKILL.md:255-257`,
`SKILL.md:335-338`, `mission-control.md:21-27`, and four `round-30/S041.txt:*` paths), 0 status changes. So the
+1 numerator is +4 from the four new snapshot tokens minus 3 from the anchor swaps; the −4 denominator is
12 removed − 8 added. The movement is honest and attributable to the 14 mapped lines (M3 and my independent
line-map agree).

## 6. Impacted axes

- `depth:verifiability` (C1, score 4): supported — eleven deferred rows closed, the successor counter has an
  empty EXCLUDED set, every fixture clones commits (pinned base readings), the meter moves exactly 1007/1998 →
  1008/1994, and all controls reproduce at the landing. No score increase is claimed by C1 and none is implied
  here.
- `coverage`: not touched by C1; I did not judge C2.

## 7. Smallest safe correction

None is permitted in-round: the predicate, map, labels and landing are frozen, and the kill rule forbids
re-labelling. For the next tranche, if the semantic limb is read strictly, the smallest fix is to cite
`SKILL.md:182-185` (or reword the historical `reward.min` aside) in the four cells noted in §5.2, and to have
the M10 line print `excluded=<n>` so the frozen predicate's wording is literal. Neither is a defect that
changes this round's verdict.

## Receipts

All under `.ufo/waves/round-95/w1/CriticClaimsC1-receipts/` (outputs copied verbatim; scratch removed after
the seat). No tool installs; no git/jj mutation of the lane; fixture clones only (clone/commit/checkout inside
the seat's scratch clones, toplevel asserted before commits).

- `01-counter-run.txt` — clone (`git clone --shared -q . $S/lane`; `rev-parse --show-toplevel` = `$S/lane`;
  `cat-file -t` base/freeze/landing = `commit`), then the frozen counter invocation above; rc `0`, output as
  quoted in §1.
- `02-controls-landing.txt` — full harness log for the re-run at the landing clone; rc `0`;
  `C1-CONTROLS-RESULT pass controls=15`; all CONTROL and LIMB lines.
- `03-controls-vs-committed.diff.txt` — CONTROL-line diff vs the committed
  `.ufo/waves/round-95/controls/c1-controls-r95.txt` (only the `candidate=… work=…` header differs; `diff_rc=1`);
  LIMB-line diff (`limb_diff_rc=0`, no output).
- `04-p2-p3.txt` — blob sha256 at freeze and landing (all equal the pins); `git show --name-status` = exactly
  the two `M` files; parent = freeze; `git diff --numstat` = `5 5` / `9 9`.
- `05-token-diff.txt` — base (1007, 1998), after (1008, 1994); 12 removed (5 GONE + 7 INTERNAL), 8 added (all
  INTERNAL), 0 status changes.
- `06-line-map.txt` — per-file base/after line counts, changed-line set = mapped site set, per-line composition
  `match True`, `mismatches 0`.
- `07-anchors.txt` — SKILL.md 182-186 / 255-257 / 335-338 / 999, mission-control 21-27, the five crosswalk
  lines; `sha256` of round-30 and round-26 S041 (equal), `cmp` rc 0, 2354 lines, 1868-1870 text; `EV ordering`
  0× and `curated-EV` 0× in SKILL.md; the required-key list absent from SKILL.md.
- `08-dup-old-scan.txt` — per-row old-text occurrences across `corpus/`: row 396 also in
  `corpus/instruments/citation-survival.md`; row 64 also in three `corpus/lessons/` files; all other rows
  single-occurrence.
- `09-harness-pins.txt` — harness `--base-rev BASE` (line 110), `clone(cand)` (line 65), `EXCLUDED = {}`
  (counter line 106), M10 limb/detail at lines 447-450 (the detail string has no `excluded` field);
  `git cat-file -t 4ef12a2f…` → `fatal: could not get object info`, rc `128` (the committed controls receipt's
  candidate rev is a scratch fixture clone, not an object in this repo); bare `S041.txt` lines in the landing
  crosswalk = 23-28 only.
- `10-forgeries.txt` — the four fixture logs (F1 rc 0, F2 rc 0, F3 rc 1 `M1 FAIL after=1008/1995`, F4 rc 0,
  17 labels/rows) with fixture revisions.
- `11-fx-driver.py` — the fixture driver (four attacks, each a shared clone of the landing commit).
