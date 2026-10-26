# ScribeScorecard — round-36 SCORECARD.md section draft

seat: `ScribeScorecard` (scribe, leaf — no subagent dispatch)
issue: draft the `## Round 36` SCORECARD.md block (claims table with frozen before → expected after,
verdicts pending measurement; measurement-state template; move-log rows for depth:verifiability and
coverage; saturation + lowest non-retired axis; capabilities: no row). Text only, in this receipt.
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — read-only for this seat.
writes: this receipt only. No lane byte, no fleet byte, no source tree touched; no git/jj mutation
(`git log/show/ls-tree/ls-files/rev-parse/status` and `git archive`-free reads only). No tool installed.

## Report

### 1. Behavior

Read the round-34 and round-35 sections (`SCORECARD.md:1121-1262`, `:1263-1404`) and reproduced their
structure: preamble binding the freeze artefacts by digest, a six-column claims table
(`Claim | Axis | Before | After | Verdict and evidence | Last change`), a measurement-state paragraph
whose values are all digest- or count-bound, per-axis move-log rows, capabilities, saturation. Measured
the frozen `Before` surface myself on the freeze blob (read-only) so no before-cell is quoted from
another seat's receipt; every `After` cell is labelled **expected** and every verdict **pending
measurement**, because `corpus/instruments/r36-closure.sh` does not exist at this read and none of the
round-36 counters have moved.

### 2. Drafted text (append at EOF; lands after `SCORECARD.md:1404`)

Every paragraph is self-contained and ends at a blank line; no line carries a total that a later append
must rewrite, no angle-bracket token and no occurrence of the round-34 placeholder literal appear
anywhere in the block, and the block deliberately contains **no** lane-commit anchor line (see F2).

````markdown
## Round 36 — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-36/claims.json` (sha256 `a6405e71…`, `frozen_at_utc`
`2026-10-26T15:33:19Z`, attempt 1; base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims-freeze commit
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`), together with the frozen before-controls
(`c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…`) and `census-before.txt`
`920e6fd4…` (three lines: `W04 S028`, `W04 S029`, `ok`). No do-nothing control pair was committed at this
freeze: `c1-controls/` carries `before.txt` only, and the round-36 junk twin `c2-controls/junk-f19.md` is a
claim output rather than a base artefact, so the two frozen before-files are the entire control surface.
Receipts land under `.ufo/waves/round-36/` (`c1-controls/`, `c2-controls/`, `census-before.txt`,
`assimilation/`, `wave1/`); `wave1-spec.json` dispatches 64 items. The last round heading at this round's
base is round 35, so C1's and C2's last-change column stays 35 and every before-column below is the frozen
control measured at this round's base bytes. The round-36 subject is instrument-soundness closure for the
routed defects of the round-35 verifier spot-check (§5, six items) plus the standing closure-order defects
(C1), and frontier F19 / FIRST EPSS exploitation-likelihood scoring (C2).

| Claim | Axis | Before (frozen control) | After (expected) | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | suite absent (`suite_missing=1`); `SKILL.md` Gates & probes exact basenames `r35-defect-closure.sh` **0** and `r36-closure.sh` **0** (`r-defect-closure.sh` **3**); round-35 `wave1-results.json` tracked **1** with a beside-provenance note **0**; `claims-erratum-d5.md` present **1**; `L1Integration.md` `Correction (round 35)` **1** and the dead-seat sentence **0**; `QUALITY.md` `supersedes R22` **1** / `supersedes R23` **1**; round-34 depth:density erratum `201.2` **6** and its heading **1**; round-36 lesson absent (`git ls-tree` **0**); placeholder-token greps **0 / 0** (`placeholder_filled=0`, `placeholder_angle=0`); `worktree_clean=0`, `scratch_leftovers=0` | **expected:** `corpus/instruments/r36-closure.sh` committed, run over a `git archive` export of the round-36 lane head (`--export-ref`), printing `closed=9/9 exit=0`, with `--selftest cases=9 failures=0`; round-35 base export `3266c993…` `closed=0/9 exit=1`; round-35 judged head export `0aee0ef…` `closed<9/9 exit=1`; E3 registers both exact basenames; E4 adds the provenance note beside the round-35 results; E5/E6/E7 retained; E8 records the false-evidence-line correction in `corpus/lessons/round-36.md`; E9 quiescent at filing | **pending measurement.** The suite is absent at this seat's read (`git ls-tree -r --name-only b47f2cd -- corpus/instruments/r36-closure.sh` returned 0 paths), so no after value is measured here; the deciding commands are listed under § Verdict state | 35 |
| C2 | coverage (7) | frontier admitted **18** (`corpus/README.md` F-rows, last F18); registry rows **52** (last S052 at `:58`), `S053` rows **0**, entries citing `source: S053` **0**; harness `entries=21 pass=21 exit=0`; `corpus/knowledge/*.md` **47**, no EPSS entry on disk; census exit 0 with `W04 S028` + `W04 S029` only; `junk_present=1` as the frozen control states it | **expected:** frontier **19** (F19 row); registry **53** with the `S053` row; entries citing `source: S053` **1** (`corpus/knowledge/epss-exploit-prediction-scoring.md`); harness `entries=22 pass=22 exit=0` including `PASS F19 ids=S053`; `source-recheck S053` exit 0 against the round-36 manifest; `capture-binding-check.py` exit 0 with the S053 record bound; census exit 0 with the two base warnings only; knowledge **48**; the junk twin `c2-controls/junk-f19.md` rejected (quote-not-found / non-admission) | **pending measurement.** At this read the counters still print the before values (18 / 52 / 47 / 21-21), so every after value is the frozen contract's expected state | 35 |
| depth:density | 9 | mean **220.9**, 26 blocks, 742 path-citation instances (`SKILL.md` `daeff71b…`, 1104 lines; `PROVINCE.md` `b4bb5fee…`, 75 lines) | **expected no move:** any `SKILL.md` change is an EOF-appended Gates & probes block (E3's two registrations), every existing line byte-identical, `PROVINCE.md` unchanged | **no move claimed; no-harm guard pending measurement** on the same committed `density.py` (`ee803726…`) and the same definition | 35 |

**Verdict state.** Every after-cell above is the frozen contract's expected state, not a measurement: at
this seat's read `r36-closure.sh` is absent, the harness prints `entries=21 pass=21 exit=0`, and the three
coverage counters print 18 / 52 / 47. The commands that decide the verdicts, one per line, so closure
appends verdict lines instead of rewriting the table:

    bash corpus/instruments/r36-closure.sh --export-ref "$ROUND36_HEAD"           -> closed=9/9 exit=0
    bash corpus/instruments/r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c -> closed=0/9 exit=1
    bash corpus/instruments/r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -> closed<9/9 exit=1
    bash corpus/instruments/r36-closure.sh --selftest                          -> cases=9 failures=0
    grep -cE '^\| F[0-9]+ \|' corpus/README.md                                 -> 19
    grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md       -> 53
    python3 corpus/instruments/frontier-recheck-count.py                       -> entries=22 pass=22 exit=0
    python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053 -> exit 0
    python3 corpus/instruments/capture-binding-check.py                        -> exit 0
    ls corpus/knowledge/*.md | wc -l                                           -> 48

**Measurement state (round-36 template, values re-read at this draft).** Base `cc692008…`; claims-freeze
commit `b47f2cd…`; `wave1-spec.json` / `wave1-dispatch.json` are the freeze worktree's untracked files, so
no spec/dispatch commit hash is asserted; the wave-1 integration commit, the `r36-closure.sh` digest and
line count, and the round-36 lane-commit anchor are recorded by appended lines at closure, not here.
Harness at this draft: `entries=21 pass=21 exit=0`; expected after: `entries=22 pass=22 exit=0`. Digests on
the freeze bytes: `corpus/SOURCES.md` `0f95a132…` (112 lines, 52 rows), `corpus/README.md` `277f04ce…`
(396 lines, 18 F-rows), `corpus/QUALITY.md` `d4f83bb1…` (250 lines), `SKILL.md` `daeff71b…` (1104 lines),
`PROVINCE.md` `b4bb5fee…` (75 lines), `corpus/instruments/r35-defect-closure.sh` `0ae4b484…` (834 lines),
`capture-binding-check.py` `3d9e5e0d…`, `source-recheck.py` `fd2e01e8…`,
`frontier-recheck-count.py` `1be79af6…`, `knowledge-expected.txt` `d2e99ca6…`, `density.py` `ee803726…`,
`claims.json` `a6405e71…`, `c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…`,
`census-before.txt` `920e6fd4…`; `SCORECARD.md` 1404 lines at this draft. Supersessions, if the wave
produces any, are recorded as appended lines naming both digests rather than compared.

**Capabilities: no row enters this round.** `r36-closure.sh` is a closure counter — it demonstrates nine
named defects closed on an exported head — not a new thing the lane can do to the domain. The master
`## Capabilities` table and the round-33 row are unchanged, and the capability window is not restarted
(last entry round 33).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. No capability entry enters this round,
so the capability window does not restart. The lowest non-retired axis remains **depth:verifiability (4)**;
the round's own distance-to-next-score reading is the L1's to file, and with C1 held 4 by design that
obligation stays active after this round.

### Round-36 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 36 | depth:verifiability | 4 (suite absent; E3 both registrations absent; E4 provenance note absent; E8 lesson absent; E2/E5/E6/E7 already present as guards; placeholder greps 0/0 at base) | 4 held — **expected** (`closed=9/9 exit=0` on the round-36 lane-head export, `--selftest cases=9 failures=0`, round-35 base export `closed=0/9`, round-35 judged head export `closed<9/9`; two registry rows; provenance note; lesson correction; quiescence) — **pending measurement** | `corpus/instruments/r36-closure.sh`, `SKILL.md` Gates & probes registry, `.ufo/waves/round-35/wave1-results.json` + provenance note, `corpus/lessons/round-36.md` |
| 36 | coverage | 7 (frontier 18, registry 52, S053 rows 0, knowledge 47, harness 21/21) | 7 held — **expected** (frontier 19, registry 53, one entry citing S053, harness 22/22 incl. `PASS F19`, recheck and binding exit 0, census exit 0, knowledge 48, junk twin rejected) — **pending measurement** | `corpus/README.md` F19 row, `corpus/SOURCES.md` S053 row, `corpus/knowledge/epss-exploit-prediction-scoring.md`, `corpus/source-snapshots/round-36/{S053.txt,manifest.json}`, `.ufo/waves/round-36/c2-controls/junk-f19.md` |

**Contract risks recorded at draft time (not filed as failures).** Three structural points the closure
seat and the suite author must settle, each measured on the freeze blob: (i) the quiescence check closes on
any export if it reads live-lane status alone — `git status --porcelain` is empty at `b47f2cd` and no
round-36 scratch seat dir exists before dispatch — so the frozen base-export limb `closed=0/9` requires an
E9 leg that is false at `3266c993…`, e.g. binding the exported ref to the lane head recorded at filing or
requiring the export to carry the round-36 lesson; (ii) a lane-commit anchor line cannot cite the commit
that contains it, so the round-36 anchor must name the integration commit or an earlier ancestor (verified
with `git cat-file -e` and `git merge-base --is-ancestor`) and is appended at closure — this block therefore
asserts no closing commit; (iii) `E3` reads exact basenames, and the freeze `SKILL.md` registers
`r-defect-closure.sh` only, so the older suite needs its own `r35-defect-closure.sh` row, not a reworded
`r-defect-closure.sh` row.

**The closing lane commit is not known at this seat's read and is not asserted here.** Every value in this
section was measured on the claims-freeze bytes digested under § Measurement state; the closure may add
seat receipts, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-36.md` and this section itself, none of which
any counter above reads.
````

The command block inside the draft uses the shell variable `$ROUND36_HEAD` for the round-36 lane head so
the block carries no angle-bracket placeholder at all; closure substitutes the 40-hex value when the
verdict line is appended.

### 3. Before-column measurements (mine, read-only, on `b47f2cd`)

| surface | command | value |
|---|---|---|
| suite presence | `git ls-tree -r --name-only b47f2cd -- corpus/instruments/r36-closure.sh` | 0 paths (`suite_missing=1`) |
| E1 placeholder limbs | `git show b47f2cd:SCORECARD.md \| grep -c 'filled by the L1'` · `… \| grep -c '<LANE_HASH>'` | 0 · 0 |
| E1 anchor lines | `git show b47f2cd:SCORECARD.md \| grep -n 'Final lane commit'` | 2 (`:987`, `:1129`) |
| E2 | `… \| grep -c '201\.2'` · `… \| grep -c 'Erratum (round 35)'` | 6 · 1 |
| E3 | `git show b47f2cd:SKILL.md \| grep -c 'r35-defect-closure\.sh'` · `'r36-closure\.sh'` · `'r-defect-closure\.sh'` | 0 · 0 · 3 |
| E4 | `git ls-tree -r b47f2cd -- .ufo/waves/round-35/wave1-results.json \| wc -l` · `git ls-tree -r --name-only b47f2cd -- .ufo/waves/ \| grep -ci provenance` | 1 · 1 (only `.ufo/waves/round-34/wave1-results.json.provenance.md`) |
| E5 | `git ls-tree -r b47f2cd -- .ufo/waves/round-35/claims-erratum-d5.md \| wc -l` | 1 |
| E6 | `git show b47f2cd:.ufo/waves/round-34/wave1/L1Integration.md \| grep -c 'Correction (round 35)'` · `grep -c 'did not file a receipt (dead seat'` | 1 · 0 |
| E7 | `git show b47f2cd:corpus/QUALITY.md \| grep -c 'supersedes R22'` · `'supersedes R23'` | 1 · 1 |
| E8 | `git ls-tree -r b47f2cd --name-only corpus/lessons/ \| grep -c round-36` | 0 |
| E9 | `git status --porcelain \| wc -l` · `ls -d /fast/scratch/hyaku/kasegi-r36` | 9 (wave scaffolding, live) · present (live wave) |
| C2 frontier | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 18 (last F18 at `:388`) |
| C2 registry | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 52 (last S052 at `:58`) |
| C2 S053 rows / citing entries | same greps for `S053` · `grep -rlE '^source: S053 ' corpus/knowledge \| wc -l` | 0 · 0 |
| C2 knowledge | `ls corpus/knowledge/*.md \| wc -l` | 47 (no EPSS entry) |
| C2 harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=21 pass=21 exit=0` |
| C2 census | `.ufo/waves/round-36/census-before.txt` | `W04 S028`, `W04 S029`, `ok` (exit 0) |
| density | `python3 corpus/instruments/density.py SKILL.md` | mean 220.9, 26 blocks, 742 cites, exit 0 |

Digests measured: `SKILL.md` `daeff71b…`, `PROVINCE.md` `b4bb5fee…`, `corpus/QUALITY.md` `d4f83bb1…`,
`corpus/README.md` `277f04ce…`, `corpus/SOURCES.md` `0f95a132…`, `r35-defect-closure.sh` `0ae4b484…`,
`source-recheck.py` `fd2e01e8…`, `frontier-recheck-count.py` `1be79af6…`, `capture-binding-check.py`
`3d9e5e0d…`, `knowledge-expected.txt` `d2e99ca6…`, `density.py` `ee803726…`, `claims.json` `a6405e71…`,
`c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…`, `census-before.txt`
`920e6fd4…`. Frozen control replay on the freeze bytes: 5/7 `c1` keys and 6/7 `c2` keys reproduce now
(`worktree_clean`, `scratch_leftovers` and `junk_present` are time- or control-defined at the freeze and
are quoted, not reinterpreted).

### 4. Findings (reported, not filed as failures)

- **F1 — E9 export semantics vs the frozen `closed=0/9` base limb.** At the freeze blob the quiescence
  clauses are already satisfied (`git status --porcelain` empty at `b47f2cd`; no round-36 seat dirs before
  dispatch), so an E9 defined on live-lane status alone closes on *any* export, including `3266c993…`;
  the frozen base-export value is `closed=0/9`. The suite's committed E9 must therefore contain a leg that
  is false at the round-35 base and at the round-35 judged head (e.g. exporting ref must equal the lane head
  recorded at filing, or the export must carry the round-36 lesson). Not measurable by me — the suite did
  not exist at my read. Smallest safe correction: state E9's definition in the suite header and ship one
  red/green fixture per limb.
- **F2 — anchor ordering and wrapped lines.** The anchor phrase in the freeze `SCORECARD.md` ends a source
  line twice (`:987`, `:1129`) with the 40-hex hash on the **next** line, so a same-line parser extracts no
  hash; E1 must join the wrapped paragraph. Separately, a lane-commit line inside the round-36 section
  cannot cite the commit that contains it — the anchor must be the integration commit or an earlier
  ancestor. My draft therefore carries no lane-commit line and says so; closure appends one only with a
  `git cat-file -e` + `git merge-base --is-ancestor`-verified hash.
- **F3 — E3 exact basenames.** Freeze `SKILL.md` registers `r-defect-closure.sh` (3 occurrences) but neither
  `r35-defect-closure.sh` nor `r36-closure.sh` (0 / 0). A round-36 registry block that reuses the
  `r-defect-closure.sh` spelling for the older suite will not close E3.
- **F4 — E4 note filename.** The only beside-note in the tree is
  `.ufo/waves/round-34/wave1-results.json.provenance.md`, i.e. `<results file>.provenance.md` beside the
  JSON. Round-35's results file is tracked with no such sibling; E4 needs that convention named in the
  suite so the note is discoverable.
- **F5 — `junk_present=1` is undefined in the freeze artefacts.** `c2-controls/` holds `before.txt` only
  and `c2-controls/junk-f19.md` does not exist at the freeze; the two committed twins are the round-34
  `junk-f17.md` and round-35 `junk-f18.md`. I quote the key verbatim and do not interpret it.
- **F6 — spec/dispatch not committed.** `wave1-spec.json` and `wave1-dispatch.json` are untracked at the
  freeze, so the round-35-style measurement-state line naming a spec/dispatch commit cannot be filled from
  a commit; the draft says so instead of citing a hash.
- **F7 — the frozen predicate's "five routed defects" counts six.** `corpus/lessons/round-35-verifier-spotcheck.md`
  §5 routes six items (close-against-one-head; re-claim with frozen evidence; D1 guard file-wide;
  append-don't-rewrite; false evidence lines; dirty tree). The nine checks cover all six (E1 ← items 1-3,
  E2/E8 ← item 5, E3 ← item 3, E4 ← item 1, E5/E6/E7 ← item 4, E9 ← items 1, 6), so no routed item is
  unrouted; the number in the frozen sentence is the only mismatch. The draft preamble says "routed
  defects … (§5, six items)" rather than repeating the count, so the block stays true either way.

### 5. Out-of-scope / not done

- No `SCORECARD.md` edit (this seat is append-only and its only lane write is this receipt); the block
  above is text for the L1's integration commit.
- No suite run, no harness run against round-36 bytes, no export of any ref — the suite does not exist and
  re-running counters would not decorate a draft.
- No score change proposed; C1/C2 stay `held` per the freeze until the decided commands run on the final
  head.
- No installs or upgrades.

### 6. Scratch

`/fast/scratch/hyaku/kasegi-r36/ScribeScorecard/` created empty and removed before yield (no scratch copy
was needed: every read was a `git show`/`git ls-tree` against the lane).

Report: .ufo/waves/round-36/wave1/ScribeScorecard.md
