# ConnectorOverlap — round 77, attempt 1, wave w1 (read-only scan)

Seat: `ConnectorOverlap-16` (connector, leaf). Freeze HEAD read: `539a438` (round-77 freeze). Base: `2e53fc7`.
Scope: overlap + assimilation scan only. No claim work, no edits, no commits. Receipts: `ConnectorOverlap.collisions.txt`, `ConnectorOverlap.reg-ids.txt`, `ConnectorOverlap.staged-ids.txt` (this dir).

## Summary

- **Assimilation collisions: 82** (registry 112 rows, staged 94 ids). Spec expected ~80 and "S112 adds none". Both are off: the new S112 **does** add one collision, and S111 (landed r76) adds one more. See §1.
- **Verdict (assimilation): none this round.** Nothing appended to `corpus/SOURCES.md`; the merge package stays L0-routed. Not absorbed.
- **considerthese: nothing new landed since 2026-10-26.** No file after `considerthese/2026-10-26.md` (last commit `e86afb8`). None of the seven 2026-10-26 proposals fits either frozen claim (C1 census counter, C2 F54 OSV querybatch). Two dispositions in the lane's own records are stale (see §2).
- **Sibling OSV/querybatch overlap: no contest to F54.** `querybatch` appears only in kasegi-shokunin. Adjacency hits are listed in §3, not absorbed.
- **Cross-claim: no other lane touches OSV or batch-query ground in round-70..79 lessons.** Only kasegi rounds 73–76 do.

## 1. Assimilation disposition recount (step 1)

Commands (run from scratch dir `/fast/scratch/hyaku/kasegi-r77/ConnectorOverlap-16/`):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

| measure | value | evidence |
|---|---:|---|
| registry rows (unique ids) | 112 | `reg-ids` = 112 lines, 112 unique; tail `S110 S111 S112` (`corpus/SOURCES.md:123-124`, S112 row at `:124`) |
| staged ids (unique) | 94 | `staged-ids` = 94 lines, 94 unique (matches `merge/kasegi/MERGE-REPORT.md` "proposed rows accepted: 94") |
| staged id range | S031 … S124 | staged ids > S094: 30 (S095–S124). **The staged set is not S001–S094.** |
| collisions | **82** | `collisions` = 82 lines, range S031 … S112 |
| collisions with id > S094 | 18 | S095–S112 |
| staged S112 present? | yes | `merge/kasegi/SOURCES.append.md:88` |

Collision delta against r76 (80 at 110 rows, `round-76.md:13`, `w1/ConnectOverlap.md:12`):
- **+S111**: registry row `corpus/SOURCES.md:123` (landed r76) against staged `S111` at `SOURCES.append.md:87` (NCSC weekly report). The r76 finding (`w1/ConnectOverlap.md:13`, lesson R-D `round-76.md:40`) said the L1 must resolve this id before integration. It was not resolved; the registry row landed with the collision still open.
- **+S112**: registry row `corpus/SOURCES.md:124` (OSV querybatch, freeze `539a438`) against staged `S112` at `SOURCES.append.md:88` (TC260 suggestion route, different document).

Finding (routed, not fixed here): the spec premise "the new S112 is outside S001-S094 so it adds none" is false. The staged package spans S031–S124. A merge of the 94 staged rows as-is would fail on 82 ids, and the merge needs renumbering or refusal for every colliding row, not just S112. Ids collide, not contents: the staged and registry rows for S111/S112 describe different documents (same id, different source).

Verdict: **assimilation none this round** (nothing appended; L0 question routed, same status as r76 R-D). No named adoptable theme.

Receipts: `ConnectorOverlap.collisions.txt` (82 ids), `ConnectorOverlap.reg-ids.txt` (112), `ConnectorOverlap.staged-ids.txt` (94).

## 2. considerthese — per-item verdicts (step 2)

Latest file: `considerthese/2026-10-26.md` (`git log -- considerthese` head `e86afb8`). Nothing newer exists; the 2026-10-26 window is the last one. "Fits r77?" is against C1 (census counter amendment) and C2 (F54 OSV querybatch admission).

Disposition source: `corpus/knowledge/considerthese-proposals-ledger.md` (latest section `## Round-62 dispositions`, `:168`), plus lessons and repo bytes I checked directly.

| # | proposal (2026-10-26) | status now | evidence | fits r77 claims? |
|---|---|---|---|---|
| 1 | distance to next score explicit | **landed** (r31 measure, r39 criteria) | `SCORECARD.md:1532` (`## Distance-to-next-score`); `corpus/instruments/score-gap.py` present (`ls corpus/instruments`); ledger `:101` | no — C1 is a counter amendment, not a gap report |
| 2 | run one end-to-end domain task | **partially landed**; SHONEN box 2 still open | gate `corpus/instruments/claim-package-check.py` landed `5b4a850` (r43); r74 non-claim documentation trial, `claimable: false` (`LOG.md:2795`); `SHONEN.md:7` is `[ ]`; ledger `:139`, r62 `:168` ("partially landed / domain task open") | no — no authorised target; C1/C2 are instrument and source work |
| 3 | quiescence gate before `complete` | **landed** | `corpus/QUALITY.md:534` (R110); `corpus/instruments/r35-defect-closure.sh` (placeholder half); `corpus/QUALITY.md:292` (R33, closure order) | no — gate already in closure order; not a claim |
| 4 | cap or externalise wave evidence | **open, operator-owned** | `git ls-tree -r -l 539a438`: 14,568 tracked files, 193,346,415 bytes; `.ufo/`: 13,916 files, 180,601,625 bytes (≈93%). No `.gitattributes`. Keep-or-externalise is an operator decision (`round-75.md:43`, R75-8) | no — freeze discipline requires committed receipts |
| 5 | land the owed F18 `PROVINCE.md` amendment | **landed** r36 | `PROVINCE.md:77` (`[r36 Frontier amendment …] F18`); `grep -c F18 PROVINCE.md` = 6 | no |
| 6 | re-tune cadence / depth | **landed as QUALITY R23; ledger row stale** | `corpus/QUALITY.md:227` (R23, event-driven reflection cadence); `corpus/lessons/round-34.md:345-346` ("mined → landed"). Ledger rows `:59`, `:86`, `:106`, `:128`, `:143` still say "open (operator-owned)" | no |
| 7 | proposal-status ledger | **landed** r30, filled r37–r41 | `corpus/knowledge/considerthese-proposals-ledger.md` (172 lines); `corpus/QUALITY.md:278` (R31) | no |

Findings on the lane's own records (routed, not edited here):
- **F-CT1 (stale ledger, P2).** Ledger §Round-43 (`:139`) says `claim-package-check.py` is absent at base `ab98fac9`. It was added later (`5b4a850`, 2026-10-28). The ledger does not record the landing. The r62 row (`:168`) still reads "partially landed". No later ledger section covers r74 or r75.
- **F-CT2 (P2 overstated in r75).** `corpus/lessons/round-75.md:16` says "P2 completed r74". The r74 trial is documentation-only and `claimable: false` (`LOG.md:2795`), and `SHONEN.md:7` remains `[ ]`. The accurate status is "partially landed", as the ledger says.
- **F-CT3 (P6 stale ledger).** `round-75.md:16` says P6 was mined r34; `QUALITY.md:227` (R23) confirms that. The ledger's later rows still say "open". Not a claim issue; the ledger lags R23.
- **F-CT4 (ledger upkeep gap).** R31 (`QUALITY.md:278`) wants a disposition in the lesson and the ledger each round. Ledger sections exist for r37–r46 and r62; `round-74.md`, `round-75.md` and `round-76.md` do not have matching ledger sections (verified by `grep -n '^## ' considerthese-proposals-ledger.md`).

Result: **no still-unimplemented 2026-10-26 proposal fits round 77.** This agrees with `round-76.md:12` and `w1/ConnectOverlap.md` §2c.

## 3. Sibling overlap with OSV / querybatch / API-contract ground (step 3)

Command: `grep -rliE 'osv|querybatch|api[- ]contract' */corpus/knowledge/` over the 21 sibling `corpus/knowledge/` trees, and `grep -rniE 'querybatch|osv\.dev|/v1/query' */corpus/knowledge/`.

Results (adjacency only, not absorbed):

| file | line(s) | what it touches | contests F54? |
|---|---|---|---|
| `kasegi-shokunin/corpus/knowledge/osv-post-v1-query-contract.md` | `:75` | F51 entry explicitly defers `POST /v1/querybatch` ("listed, not described") | no — defers the batch endpoint to a successor, which is F54's place |
| same | `:71` | rate limits and quotas not stated on `/v1/query` | no |
| `kasegi-shokunin/corpus/knowledge/osv-affected-range-events.md` | `:18` | OSV record events outside the bytes; per-database statements | no (record format, F31 / S080) |
| `kasegi-shokunin/corpus/knowledge/github-advisory-database-curation-semantics.md` | `:75`, `:120` | cites the OSV format statement (S105.txt:567); says the OSV schema stays with S080 | no |
| `kasegi-shokunin/corpus/knowledge/openssf-scorecard-checks.md` | `:35`, `:83` | osv.dev as a consumer of scorecard data | no |
| `kasegi-shokunin/corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` | `:79` | "F31 / S080 unrelated" | no |
| `kaidoku-shokunin/corpus/knowledge/2026-10-13-r3-node-addons.md` | `:67` | ASAR / native fringe line matched on the generic term | no (false match) |
| `souji-shokunin/corpus/knowledge/quarantine-origin-record-fields-r24.md` | `:19` | "write-side API contract" (gio trash, S112 of souji's own numbering) | no (different domain; same id text, not OSV) |
| `kotodama-shokunin/corpus/knowledge/linguistics/syntax-typology.md` | `:32` | "OSV" = object-subject-verb word order | no (false match) |

- `querybatch` appears in fleet corpora only under `kasegi-shokunin/` (`corpus/SOURCES.md`, `corpus/knowledge/osv-post-v1-query-contract.md`, `corpus/lessons/round-76-verifier-spotcheck.md`, `corpus/source-snapshots/round-73/S108.txt`, `…/round-76/S111.txt`, `…/round-77/S112.txt`, `…/round-77/manifest.json`).
- The r76 draft entry `osv-api-surface-and-limits.md` is not in any `corpus/knowledge/` tree.
- Scope note: this seat grepped the knowledge trees only (as the spec names). The r76 scan covered all 21 corpus dirs (270 files, `w1/ConnectOverlap.md` §1a). I did not rerun that wider scan.

Result: **no sibling contests F54.** Adjacency is the F51 deferral at `osv-post-v1-query-contract.md:75` and the OSV-format pointers above.

## 4. Cross-claim pattern (step 4)

Command: `grep -rliE 'osv|querybatch|/v1/query' */corpus/lessons/round-7[0-9].md` (and the `-n` form).

- Hits: **kasegi-shokunin only.** `corpus/lessons/round-73.md:16,37,42,49`; `round-74.md:13-26`; `round-75.md:12,18`; `round-76.md:7-9,39`.
- No other lane's round-70..79 lesson mentions OSV, querybatch or `/v1/query`.
- Conclusion: no cross-claim collision on OSV ground. The only OSV thread is kasegi's own F51 → F53/F54 sequence.

## 5. Checks not run and limits

- `score-gap.py` and the closure scripts were **not executed** by this seat (read-only scan; the reporter runs subprocesses). Their status is cited from committed files and ledger text, not re-measured.
- No `git` mutation. Read-only only: `git log`, `git show`, `git ls-tree`, `git rev-parse`, `git count-objects`.
- Tools installed: none.
- Sibling corpora were read from working-tree bytes (`*/corpus/knowledge/`); no sibling git state was checked.

## Routed items for the L1

1. **R-D (persisting, r76):** assimilation collisions 82, not 80; S111 and S112 both now collide with the staged package. Resolve ids at merge time; the package cannot apply as-is.
2. **F-CT1 to F-CT4:** ledger upkeep (landing record for `claim-package-check.py`, P6 R23 row, r74–r76 disposition sections; P2 status wording in `round-75.md:16`).
