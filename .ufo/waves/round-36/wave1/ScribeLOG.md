# ScribeLOG — round-36 `LOG.md` entry draft (scribe, text only)

Lane head at drafting: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (claims freeze), working tree
clean apart from the untracked `.ufo/waves/round-36/*` wave files. Judged axes: depth:verifiability,
coverage. This seat wrote **only this receipt**; no lane file, no fleet file, no scratch survivor, no
git/jj mutation, no tool install.

## 1. Item and deliverable

Item (as dispatched): *Draft the LOG.md round-36 entry (text in receipt): heading `## Round 36`,
claims C1/C2 with summary, frontiers F18/F19 amendments, instruments added (r36-closure.sh),
assimilation: none, considerthese proposals adopted, mistakes M36-1..4, wave shape. Keep it consistent
with the scorecard and lesson drafts.*

Delivered: the entry text in §7 — 15 lines / 9,541 bytes, every requested block present in
the order the item lists. Land by appending at EOF of `LOG.md` after integration (R6 append-only): the
file is 1659 lines with the last heading `## Round 35` at `:1651`, so the append adds the blank
separator plus these lines and changes no existing line.

## 2. Measurements this seat ran (read-only, `git show`/`grep`/`ls-tree`)

`HEAD` is the freeze commit; `n/m` = not measured by this seat and therefore **not asserted** in the
entry.

| probe | command | r35 base `3266c993` | r35 judged head `0aee0ef` | freeze `b47f2cd` |
|---|---|---|---|---|
| E1 placeholder phrase | `git show <ref>:SCORECARD.md \| grep -cF 'filled by the L1'` | **1** (`:1240`) | **1** (`:1271`) | **0** |
| E1 angle-bracket marker | `… \| grep -cF '<LANE_HASH>'` | 0 | 0 | 0 |
| E2 density erratum | `… \| grep -c '201\.2'` | **0** | n/m | **6** (`:1246,:1250,:1269,:1307,:1312,:1314`) |
| E3 exact r35 basename | `git show <ref>:SKILL.md \| grep -cF 'r35-defect-closure.sh'` | n/m | **0** | **0** |
| E3 exact r36 basename | `… \| grep -cF 'r36-closure.sh'` | n/m | n/m | **0** |
| E3 near-name | `… \| grep -cF 'r-defect-closure'` / `grep -oF \| wc -l` | n/m | n/m | **stem 4 lines / 9 occurrences**; `.sh` form 3 lines / 8 occurrences; row `:1097` |
| E4 results tracked | `git ls-tree -r <ref> -- .ufo/waves/round-35/wave1-results.json` | n/m | **0** | **1** |
| E4 provenance note | `git ls-tree -r <ref> --name-only -- .ufo/waves/round-35/ \| grep -c provenance` | n/m | n/m | **0** |
| E5 erratum file | `git ls-tree -r <ref> -- .ufo/waves/round-35/claims-erratum-d5.md` | n/m | **1** | **1** |
| E6 file | `git ls-tree -r <ref> -- .ufo/waves/round-34/wave1/L1Integration.md` | **1** | **1** | **1** |
| E6 phrase | `git show <ref>:…/L1Integration.md \| grep -cF 'Correction (round 35)'` | **0** | n/m | **1** |
| E7 supersession rows | `… corpus/QUALITY.md \| grep -c 'supersedes R22'` / `R23` | n/m | n/m | **1 / 1** |
| E8 stale evidence line | `git show <ref>:corpus/lessons/round-35.md \| grep -cF 'source-recheck exit 0 on committed bytes'` | n/m | **1** | **0** |
| C2 frontier rows | `git show <ref>:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | **17** | n/m | **18** |
| C2 registry rows | `… corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | **51** | n/m | **52** |
| C2 knowledge entries | `git ls-tree -r <ref> --name-only -- corpus/knowledge/ \| grep -c '\.md$'` | **46** | n/m | **47** |
| suite present | `git ls-tree -r <ref> -- corpus/instruments/r36-closure.sh` | n/m | n/m | **0** |
| cited commits exist | `git cat-file -t` on `cc69200…`, `b47f2cd…`, `3266c993…`, `0aee0ef…` | `commit` ×4 | — | — |
| freeze descends from base | `git merge-base --is-ancestor cc69200 b47f2cd` | exit 0 | — | — |

The E1 mechanism is visible in the table: the placeholder phrase is present in both round-35 exports
(`SCORECARD.md:1240` in the round-34 section, `:1271` in the round-35 section) and absent at freeze, so
E1's red at `3266c993`/`0aee0ef` is exactly the round-35 placeholder class the suite binds — measured,
not inferred.

## 3. Figures carried from sibling receipts (their measurement; I read, did not re-run)

- **Capture (C2):** `.ufo/waves/round-36/wave1/ScoutCaptureAvailability.md` §1 — HTTP 200, 0 redirects,
  26804 raw bytes, raw sha256 `66fece52…117868`; normalized 8448 bytes / 244 lines, sha256
  `4ec61c59…83e9`; `fetched_utc 2026-10-26T15:35:10Z`; page `last-modified` 2026-07-30T13:48:13Z.
- **Id collisions:** `wave1/ScoutIdCollisions.md` — registry 52 × staged 94 → **22** standing collisions
  (S031–S052), 23 predicted after lane S053 lands against a different staged S053 (METI
  平成29年経済産業省告示第19号); guard load-bearing and fail-closed (exit 2 on a missing registry path).
- **Quarantine slice:** `wave1/ScoutQuarantine.md` §2–§3 — the same 7 rows, byte-equal to the round-35
  slice; verdicts 1 present-and-located (S068 = lane S040) / 2 absent (S037, S054) / 4 unreachable
  (S048 404; S065 timeout at 9.1 % of bytes; S069–S070 verified-TLS failure, 0 B); 0 adopted;
  S065/S069/S070 differ from the round-35 labels by transport only.
- **Negative sweep + adjacency ruling:** `wave1/ScoutF19Open.md` (`EPSS|exploit prediction` → 0 hits
  before admission; the broad `exploitation likelihood` alternative already hits the F17 Immunefi entry
  once), `wave1/ScoutF19Sibling.md` (uncontested; nearest neighbour a kagi retained NVD/SSVC probe).
- **M36-1…M36-4 gists:** `wave1/ScribeMistakes.md` rows + that seat's IRC messages; the entry follows
  their wording and the class vocabulary.
- **Score gap:** `wave1/ScribeConsiderthese.md` quoting `python3 corpus/instruments/score-gap.py --root .`
  — `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
- **Before controls:** `.ufo/waves/round-36/c1-controls/before.txt`, `c2-controls/before.txt`,
  `census-before.txt` — read for the entry's before-values, not re-executed.

## 4. Contract-only figures (frozen claims; this seat measured none of them)

`closed=9/9 exit=0`, `cases=9 failures=0`, `closed=0/9 exit=1` at `3266c993`, `closed<9/9 exit=1` at
`0aee0ef`, the plain-run refusal (exit 2), frontier 19, registry 53, knowledge 48, harness
`entries=22 pass=22`, `source-recheck --source S053` exit 0, census exit 0, the junk-twin rejection,
QUALITY R28/R29 landing, the F18/F19 PROVINCE amendments, and `wave1-results.json` finalisation.

The entry states this in its own words: *"The round-36 after-state figures are the frozen claims'
contract values; the instrument's own run at the final head and the round report are the evidence of
record, and a deviation lands as an appended erratum, never as an edit."* Do not append the entry
before the post-integration gate prints those values.

Measured by this seat and therefore stated plainly: the seat census (`wave1-spec.json`: 64 items, roles
18/12/10/6/6/5/3/2/2), the before-value triples (17/51/46 at the r35 base; 18/52/47 at freeze), and
every E-probe cell in §2.

## 5. Consistency with sibling drafts

- **ScribeScorecard** (`wave1/ScribeScorecard.md`): same before-values and the same E-probe set; the
  entry repeats its `suite_missing=1` premise and its R28/R29 and `depth:density` no-move expectation
  (the entry claims no density row). Its near-name cell reads `r-defect-closure.sh` **3** (exact-basename
  lines); the entry states both readings — `.sh` form 3 lines, stem 4 lines / 9 occurrences.
- **ScribeMistakes**: the four gists follow its rows and its `captured-by` framing (E9/export-bound
  suite, E8 + correction, E3 exact basenames, single report last). The near-name count drifted in its
  first draft (8 vs 9 occurrences) and was settled by independent measurement before integration; that
  seat's canonical wording, which the entry now uses: *4 `SKILL.md` lines; 9 occurrences of the stem
  `r-defect-closure`, 8 of the `.sh` form.*
- **ScribeConsiderthese**: proposal 1 is written as *partially landed* per that seat's finding F-1 (gap
  computed; the criteria-in-§Saturation plank not landed); proposals 3 and 5 are *adopted* and tied to
  the landings this entry records, so do not append the entry if either landing is absent.
- **ScribeShonen**: no overlap (separate file, no shared counts).

## 6. Writes, scratch, tooling

- Writes: this receipt only, at the path below; scratch `/fast/scratch/hyaku/kasegi-r36/ScribeLOG/`
  (entry draft `round-36-entry.md`, this builder script) removed at exit.
- Tooling: none installed, nothing upgraded, no pacman transaction attempted (host-wide pause).

## 7. The entry text (verbatim, ready to append)

```markdown
## Round 36 — 2026-10-26 — C1 head-closure suite E1–E9 over `git archive` exports + C2 F19 FIRST EPSS admitted (one v2 wave, 64 seats)

Claims frozen in `.ufo/waves/round-36/claims.json` before dispatch (base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims-freeze commit `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`, before-controls `c1-controls/before.txt` / `c2-controls/before.txt`, `census-before.txt`). Wave-1 spec/dispatch (64 seats, v2 policy) and the integration commit are named in the round report; a commit cannot carry its own hash. The suite's red anchors are the round-35 pair the non-author spot-check judged — base `3266c9937b03062d9bbc2f436e20820115ed179c`, judged head `0aee0ef105395a2f1d6ace7eaeef13871bb26988`; both resolve as commits (`git cat-file -t`).

- **C1 depth:verifiability (4 held) — head-closure suite over exports.** Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`. `--export-ref <commit>` extracts the lane with `git -C … archive <commit>` into a scratch root and runs every check against that export; a plain run without the flag refuses (exit 2) instead of reading the worktree. Nine checks E1–E9 print one payload line each plus `closed=K/9 exit=E`: `closed=9/9 exit=0` at the round-36 final lane head, `selftest case=<name>` verdict lines with `cases=9 failures=0` under `--selftest` (a summary-only forgery does not satisfy it), and the required reds — round-35 base export `closed=0/9 exit=1`, round-35 judged head export `closed<9/9 exit=1`. What the checks bind, re-measured by this seat on committed bytes at freeze `b47f2cd` against both round-35 refs: E1 placeholder/hash binding — `filled by the L1` **1** at each r35 export (`SCORECARD.md:1240` at the base, `:1271` at the judged head) and **0** at freeze, the angle-bracket lane-hash marker 0 in all three revisions, and the `Final lane commit:` line's 40-hex hash must resolve and be an ancestor of the exported ref; E2 round-34 depth:density erratum — `201.2` **0** at the r35 base vs **6** lines at freeze; E3 exact-basename registry rows — `r35-defect-closure.sh` **0** and `r36-closure.sh` **0** in `SKILL.md` at freeze, both still owed (the near-name `r-defect-closure.sh` occupies 3 `SKILL.md` lines, the stem `r-defect-closure` 4 lines / 9 occurrences, so the round-35 literal was satisfied by a sibling name — M36-3); E4 `.ufo/waves/round-35/wave1-results.json` tracked **1** at freeze (0 at the judged head) with a provenance note beside it (**0** at freeze — this round's add); E5 `.ufo/waves/round-35/claims-erratum-d5.md` present **1**; E6 `Correction (round 35)` in `.ufo/waves/round-34/wave1/L1Integration.md` **1** at freeze, **0** at the r35 base (file present in both); E7 `supersedes R22` / `supersedes R23` rows in `corpus/QUALITY.md` **1 / 1**; E8 the round-35 lesson's false evidence lines (`source-recheck exit 0 on committed bytes`, `SKILL.md +13/0`, `LOG.md 0 changed`) — **1** stale line at the judged head, **0** at freeze, correction recorded in `corpus/lessons/round-36.md`; E9 quiescence — `git status --porcelain` empty and no leftover `/fast/scratch/hyaku/kasegi-r36` seat dirs at filing. `corpus/QUALITY.md` gains **R28** (a round's claims rest on committed paths at the quoted head; counters run over exports; the lane is quiescent before filing — considerthese 2026-10-26 proposal 3) and **R29** (an instrument is registered in `SKILL.md` by its exact basename; a near-name sibling does not satisfy the registry literal — M36-3). The round-36 after-state figures are the frozen claims' contract values; the instrument's own run at the final head and the round report are the evidence of record, and a deviation lands as an appended erratum, never as an edit.

- **C2 coverage (7 held) — F19 FIRST EPSS admitted.** Frontier 18→19: `corpus/knowledge/epss-exploit-prediction-scoring.md` (`ground: F19`, `source: S053`) built from a live capture of `https://www.first.org/epss/` under the instrument UA — 200, no redirect, 26804 raw bytes (sha256 `66fece52…117868`), normalized to 8448 bytes / 244 lines (sha256 `4ec61c59…83e9`), fetched 2026-10-26T15:35:10Z, page `last-modified` 2026-07-30T13:48:13Z. Registry 52→53 (`S053`, tier A, status mined, opened 2026-10-26, used-by the entry); knowledge 47→48; harness `entries=22 pass=22 exit=0` incl. `PASS F19 … ids=S053`; `source-recheck --manifest corpus/source-snapshots/round-36/manifest.json --source S053` exit 0 with each pinned quote `occurrences=1`; census exit 0 (W04 S028/S029 only — the two standing duplicate-URL rows). The entry's teaching point is the separability the corpus lacked: EPSS is an exploitation-likelihood probability (0–1 per CVE, refreshed daily), not a severity score (CVSS) and not a status (KEV catalog listing). The declared junk twin `c2-controls/junk-f19.md` is rejected — fabricated sentence, `source-recheck` quote-not-found / harness non-admission — and the discriminating invocation is recorded. Negative sweep before admission: `EPSS|exploit prediction` → 0 hits across `corpus/knowledge`, `corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md`; the broader `exploitation likelihood` alternative already matches one pre-existing line in the Immunefi entry (F17), so the uncovered-ground assertion rests on the strict anchors only.

- **Frontier items.** `PROVINCE.md` takes two end-of-file amendments: **F18** — CISA Known Exploited Vulnerabilities catalog, admitted round 35 and owing its amendment since then (considerthese 2026-10-26 proposal 5) — and **F19** — FIRST EPSS, admitted this round. Adjacency: the EPSS sweep over the sibling lanes is **uncontested** (nearest neighbour is a retained kagi NVD/SSVC probe — the SSVC *Exploitation* decision point, a different framework; reported, not absorbed). Assimilation: **none adopted** — id-collision rerun registry **52** × staged **94** → **22** standing collisions (S031–S052, contiguous, no new ones; 23 predicted once lane S053 lands against the staged S053, which is a different source — METI 平成29年経済産業省告示第19号 — so the collision is the standing scratch-side renumber class, not a lane defect), the guard proven load-bearing (0–3-space-tolerant pattern catches the indented collision a column-0 pattern false-greens) and fail-closed (exit 2 on a missing registry path); quarantine slice re-derived from the read-only register — the same 7 rows, byte-equal to the round-35 slice, verdicts **1** present-and-located (S068, duplicate of lane S040) / **2** absent (S037, S054) / **4** unreachable (S048 404; S065 30 s timeout at 9.1 % of bytes; S069–S070 verified-TLS failure, 0 B), **0 adopted**, with S065/S069/S070 differing from the round-35 labels by transport only; standing refusals re-measured, no flip cleared. considerthese/2026-10-26: proposal **3** adopted (quiescence gate → QUALITY R28 + E9); proposal **5** adopted (F18 + F19 PROVINCE amendments); proposal **1** partially landed — the distance-to-next-score is computed (`corpus/instruments/score-gap.py`: `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`) and cited in the scorecard, while its write-the-criteria-into-§Saturation plank is not landed; proposals **2 / 4 / 6 / 7** recorded with reasons (2 — SHONEN box 2 still has no executed end-to-end task; 4 — capping or externalising wave evidence needs an operator/LFS decision; 6 — cadence recorded, no change; 7 — proposal-status ledger not started).

- **Mistakes M36-1…M36-4** minted in `corpus/lessons/round-36.md` from the round-35 spot-check's routed defects. **M36-1** (landing/closure-order) — round-35 lanes kept writing and committing after `complete kasegi round=35` at 04:00:34: `8ce6fb4` 04:01:12, `5a25337` 04:02:21, `bb2dc8c` 04:04:46, `48e6053` 04:04:55, and `wave1-results.json` only at `980aa3d` 04:19:52 — the M35-1 class recurring. **M36-2** (stale-premise) — the round-35 lesson `## Gate` line "source-recheck exit 0 on committed bytes" is false at `0aee0ef` (the S052 capture is absent there; the instrument prints `S052:source UNAVAILABLE reason=missing`), and the same `## No-harm` bullets measure 0/0 (`SKILL.md`) and +10/0 (`LOG.md`) at the judged head. **M36-3** (counter-discrimination) — the r35 suite's own D3 registry row never landed: `grep -cF 'r35-defect-closure.sh' SKILL.md` → 0 at freeze while the near-name `r-defect-closure.sh` occupies 3 `SKILL.md` lines (stem `r-defect-closure`: 4 lines / 9 occurrences; registry row at `:1097`), so the loose literal scored the defect closed. **M36-4** (landing) — the round-35 report was re-filed three times after `complete` (errata `63ce2a63` 04:01:19, `8cfcb5b6` 04:02:33, `375f9514` 04:20:03) instead of landing once, last, after full integration. The four fixes: E9's gate and export-bound suite (M36-1), E8 plus the appended correction (M36-2), E3's exact-basename rows and a red fixture (M36-3), one report commit after integration (M36-4).

- **Wave.** One v2 wave, 64 seats (executor 18, scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2); adversarial seats 23/64 = 35.9 % (reviewer 10 + critic 6 + mutation-tester 5 + sentinel 2 — the round-35 entry's 31.2 % counted the same set without sentinel). Receipts under `.ufo/waves/round-36/wave1/`; `wave1-results.json` is finalised by the dispatcher once the last seat settles.

- **Tooling.** No installs; no pacman transactions (host-wide pause).
```

## 8. Limits / open items for the L1

1. The entry quotes the placeholder phrase once (`filled by the L1`) because that is the measured defect
   string. E1's grep is `SCORECARD.md`-scoped, so the LOG occurrence does not fire it, and the round-35
   entry did the same; if a future gate greps `LOG.md` for the phrase, paraphrase the clause. This
   receipt also carries the angle-bracket lane-hash marker once, as the argument of the E1 probe in §2 —
   it is documentation of the check, not placeholder prose (the frozen `claims.json` and `build-spec.py`
   in the same wave dir carry both tokens, and E1's own grep is `SCORECARD.md`-scoped).
2. The wave-1 spec/dispatch and integration hashes are deferred to the round report ("a commit cannot
   carry its own hash", round-31/35 precedent). Adding the real hashes when appending is fine; adding a
   placeholder token is not.
3. `wave1-results.json` is described as dispatcher-finalised. If it is already finalised at append time,
   state the settled count (round 35: 64/64) instead.
4. The entry starts at `## Round 36` and ends on the Tooling bullet; the round report and any post-entry
   note land separately, as in rounds 34 and 35.
