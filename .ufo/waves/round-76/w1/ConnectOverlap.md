# ConnectOverlap — round 76, attempt 1, wave w1

Seat: ConnectOverlap (leaf, read-only). Lane HEAD read: `5da54cd` (freeze commit; base `a788021`).
Scope: (1) cross-lane OSV overlap scan for C2, (2) considerthese sweep with dispositions, (3) assimilation id collision re-derivation.
Writes: this report, `assimilation-ids/` (three id files), and scratch `/fast/scratch/hyaku/kasegi-r76/ConnectOverlap/` (removed before yield). No git mutation, no network, no edits to `/home/vgpnk/Projects/shokuknow`.

## Summary

- **Sibling overlap (C2): DISTINCT for all 21 sibling corpora.** No sibling holds the OSV.dev API-surface overview ground (six request types, rate-limit statement, OpenAPI download). Closest sibling is kaidoku-shokunin S015, a single OSV record, not the overview.
- **Within-lane overlap risk for C2 (new, not in the claim text):** the six endpoint *paths* appear only as page navigation at `S111.txt:4-9`, outside the claimed anchor range 21-36, and the same nav list already sits in the held S108 capture at `S108.txt:5-9`. The six request *types* are located at `S111.txt:28-34`. See §1b.
- **considerthese: 47 proposals across 8 files (2026-10-19 … 2026-10-26).** Dispositions in §2. The lane's own ledger (`corpus/knowledge/considerthese-proposals-ledger.md`) covers only the 2026-10-25 and 2026-10-26 proposals; the 2026-10-19 … 2026-10-24 proposals have no ledger row. **No still-unimplemented proposal fits this round** (reasons in §2c).
- **Assimilation collisions: reg-ids 110, staged-ids 94, collisions 80** (nonempty). Adoption stays closed; the L0 routing item stands.
- **New collision finding for C2:** the id `S111` that C2 assigns to the OSV overview is already staged in `shokuknow/merge/kasegi/SOURCES.append.md:87` (a Chinese NCSC weekly-report row). Landing C2 with S111 would raise collisions from 80 to 81 (simulated, §3). The L1 must resolve this id before integration.

## 1. Sibling overlap scan (C2 distinctness, step 1)

### 1a. Commands and counts

| # | command | result | exit |
|---|---|---|---|
| 1 | `grep -ril -i 'osv' /home/vgpnk/Projects/shokunin/*/corpus 2>/dev/null` | 270 files across the 21 corpus dirs (binary and substring hits included) | 0 (count via `… \| wc -l`, exit 0) |
| 2 | `ls -d /home/vgpnk/Projects/shokunin/*/corpus \| wc -l` | 21 corpus dirs | 0 |
| 3 | `grep -rIil -i 'osv' <corpus>` per repo (text files only) and `grep -rIil -w -i 'osv\(\.dev\)\?'` (word match) | per-repo counts in the table below | 0 |
| 4 | `grep -rIin -o '.{0,90}osv.{0,90}'` over the non-kasegi siblings, `grep -rIil -E 'google.github.io/osv\|osv.dev/api\|querybatch\|determineversion\|importfindings\|binary-to-source\|v1experimental\|rate.limit\|v1/vulns\|api.osv.dev\|osv\.dev'` over all siblings | the marker search below | 0 |

### 1b. Verdicts per sibling

| sibling | text hits / word hits | verdict | what the hit is |
|---|---|---|---|
| audio-shokunin | 66 / 0 | DISTINCT | Substring `R83OSV` (a media-name test marker), e.g. `corpus/fixtures/measure_audio.py:17405`. No OSV content. |
| chousa-shokunin | 1 / 0 | DISTINCT | Base64 substring inside `corpus/captures/e84bfe97808591d23fe3266f.raw:35`. |
| game-dev-2d-shokunin | 2 / 0 | DISTINCT | `uid://…46osv` Godot UID substring; `.x86_64` binaries. |
| game-dev-3d-shokunin | 0 / 0 | DISTINCT | Hits only inside a binary `pybullet…so` vendor file. |
| kaidoku-shokunin | 4 / 3 | DISTINCT for overview ground (record-level overlap only) | `corpus/SOURCES.md:21` S015 is one OSV **record** (`https://api.osv.dev/v1/vulns/CVE-2025-55305`, the `details`/`extracted_events`/`references` fields); `corpus/lessons/round-13.md:42,59` restates it; `corpus/evidence/round-30/c1/pypi-uv-0.13.0.json` holds osv.dev record links. None of these name the six request types, the rate-limit statement or the OpenAPI download. It shares only the `GET /v1/vulns/{id}` endpoint class; its S015 row must not be cited for overview ground. |
| kengaku-shokunin | 1 / 0 | DISTINCT | `osv` substring inside a fetched GitHub-API JSON (`evidence/round53/fetched/C1PriceScoutC-ghapi-issues-242.json:2`). |
| kotodama-shokunin | 1 / 1 | DISTINCT | Name collision: OSV = Object-Subject-Verb word order (`corpus/knowledge/linguistics/syntax-typology.md:11,32`). |
| mori-shokunin | 4 / 0 | DISTINCT | Substring `nosve` in kernel-parameter text (`arm64.nosve`). |
| revenger-shokunin | 1 / 0 | DISTINCT | `OSVersion 4.0` PE header comment (`corpus/fixtures/managed-r76/generator.py:138`). |
| tabi-shokunin | 11 / 0 | DISTINCT | Base64 substrings in bidi/bfcache transcripts and a vendored `playwright-core` bundle (`node_modules`). |
| kagi, kake, kama, kotoba, kumitate-shokunin, lore, mado, souji, tameshi, tsukuroi | 0 / 0 | DISTINCT | No hits. |

Marker search (command 4) over all siblings: `google.github.io/osv`, `osv.dev/api`, `querybatch`, `determineversion`, `importfindings`, `binary-to-source`, `v1experimental`, `v1/vulns`, `api.osv.dev` match **only** kasegi-shokunin files. The `rate.limit` hits in other siblings are unrelated (no OSV). **Sibling verdict: DISTINCT for all eleven hit-bearing siblings; no OVERLAP.**

### 1c. Within-lane check of the C2 entry (kasegi, for the L1)

Commands: `grep -n -E 'six different|no limits|OpenAPI|API \(1.0\)|rate limited' corpus/source-snapshots/round-73/S108.txt` → no match (exit 1). `sed -n '25,38p' corpus/source-snapshots/round-76/S111.txt` and `grep -n -E 'querybatch|determineversion|importfindings|binary-to-source|v1experimental' …/S108.txt`.

- S111 line map (verified): 21-24 = `API (1.0)`, `Download the OpenAPI specification`, `Download Here`, `OSV API`; 28 = "There are six different types of requests…"; 29-34 = the six type descriptions (31-33 marked Experimental); 35 = "Is the API rate limited?"; 36 = "Currently there are no limits on the API."; 38 = the 32 MiB sentence.
- S108 (round-73 POST /v1/query page) contains the endpoint navigation list at lines 5-9 (same six paths as S111:4-9) and the 32 MiB sentence at line 148, which is the same text as S111:38. It does **not** contain the six-types sentence, the rate-limit Q/A, or the OpenAPI download.
- **Finding for B6/QUALITY R114:** the endpoint *paths* in the claim text (`POST /v1/query`, …, `POST /v1experimental/ubuntu/binary-to-source`) are located only at S111:4-9 (nav chrome, outside the claimed range 21-36), and the same paths are already held as nav at S108:5-9. The claimed ground that is **new** and located in 21-36 is the six-types sentence (28), the six type descriptions (29-34), the rate-limit Q/A (35-36) and the API 1.0 / OpenAPI lines (21-22). The entry should claim those and cite the endpoint paths as page navigation, not as located ground. The claim text itself is not reworded here (claims are frozen).

## 2. considerthese sweep (step 2)

### 2a. Inputs

`ls /home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese | wc -l` → 8 (exit 0); last file `2026-10-26.md`. No file after 2026-10-26 (10 days at 2026-11-05). Proposals counted per file: 10-19: 7; 10-20: 6; 10-21: 6; 10-22: 5; 10-23: 5; 10-24: 5; 10-25: 6; 10-26: 7; total 47.

Status keys: LANDED (committed lane record verified by me or cited ledger row); PARTIAL; OPEN-OP (operator-owned); OPEN-BOT (lives in the bot's local store, not in the repo, not verifiable from the lane); SUPERSEDED.

Verification commands used: `ls corpus/instruments/test_*` (only `test_resolve.py`, exit 0); `grep -n -E '^\| (Q7|Q9|R7|R8|R9) ' corpus/QUALITY.md` (Q7 :48, R7 :49, R8 :50, R9 :51, Q9 :64; exit 0); `grep -c -E '^ {0,3}\|[[:space:]]*S031 ' corpus/SOURCES.md` → 1 (exit 0); `grep -n -E '^\| (F06|F07|F08|F13|F18) ' corpus/README.md` → F06 :207, F07 :208 (S031), F08 :209, F13 :264, F18 :388 (exit 0); `grep -n F18 PROVINCE.md` → :77 `[r36 Frontier amendment …] F18` (exit 0); `grep -n -E '^## Saturation|9/10|N = 3' SCORECARD.md` → §Saturation at :309, 9/10 and N = 3 at :313-314 (exit 0); `sed -n '7p' SHONEN.md` → `- [ ] At least one end-to-end domain task executed and logged in LOG.md` (exit 0); `ls corpus/instruments/ | grep -E 'closure|score-gap|claim-package|source-recheck|recheck-audit'` (r35-r43 closure scripts, score-gap.py, claim-package-check.py, source-recheck.py, recheck-audit.py present, exit 0); `git for-each-ref --format='%(refname)' | grep -c cursor` → 0 (exit 0 on grep count); `git ls-files | wc -l` → 14447 and `git ls-files | grep -c '^\.ufo/'` → 13799 (exit 0).

### 2b. Dispositions

**2026-10-19**
1. anchorcheck prefix regression test (`test_anchorcheck.py`) — SUPERSEDED. The file does not exist; anchorcheck fail-closed plus nine selftest cases landed r28 (`corpus/lessons/round-28-verifier-spotcheck.md:84`).
2. Calibrate claim-package review rubric (bot store) — OPEN-BOT. The lane gate `claim-package-check.py` is committed (r43, per ledger §Round-46).
3. Severity language grounded in HackerOne/Bugcrowd/Intigriti — LANDED r29 as F13 program severity ladders (`corpus/README.md:264`, S043–S045).
4. Pre-draft Saturation line and window N — LANDED r22 (`SCORECARD.md:309-314`: 9/10 per owned axis, N = 3).
5. Decide draft PR #1 — OPEN-OP. No `cursor/*` refs in the lane clone (command above → 0).
6. Craft-vs-meta ratio report — OPEN-BOT.
7. Change-driven (push-listener) reflections — OPEN-OP.

**2026-10-20**
1. Become the live-source rechecker (daily re-fetch) — PARTIAL. Snapshot rechecker landed (`source-recheck.py`, `recheck-audit.py` present); a scheduled live re-fetch has no committed artefact → OPEN.
2. Fold Frontier table into the bot rubric — OPEN-BOT.
3. Owed-corrections ledger — LANDED in form: R15 (`QUALITY.md`), `r35-defect-closure.sh` through `r43-closure.sh` (ledger §Round-46 row 3-5).
4. Pre-screen queued Frontier sources S018/S022/S024 — LANDED r23: F06–F08 admitted (`corpus/README.md:207-209`), S029/S030 superseded by S031.
5. Redefine coverage denominator (20 Core+Frontier)/25 — OPEN-OP; the frozen C2 text says the denominator is operator-owned.
6. Carry-overs (anchorcheck test, PR #1) — item 1 SUPERSEDED; PR #1 OPEN-OP.

**2026-10-21**
1. Run every `recheck:` line daily — PARTIAL. `recheck-audit.py` committed; the daily schedule is bot-side → OPEN-BOT.
2. Check quotes against snapshots before admission — LANDED r23 (`source-recheck.py` quote-not-found) and Q9 exactly-once (`QUALITY.md:64`).
3. Fold CNA 4.2.0 and CRA Art. 14 into the rubric — repo side LANDED (F07 at S031 rule 4.2.6, F08 admitted `README.md:209`); rubric lens OPEN-BOT.
4. Second reviewer for the resolver fix (C1) — LANDED r23: mirror containment 12/12 GONE (`corpus/lessons/round-23-verifier-spotcheck.md:34-41`; `mirror-containment-check.py` present).
5. Track rounds blocked by infrastructure — OPEN-BOT.
6. Carry-overs — as 2026-10-20 item 6.

**2026-10-22**
1. Single-seat "close r23" dossier — LANDED r23 (F06–F08 admitted, `README.md:207-209`).
2. Scan all branches; eight `cursor/*` README branches — not present in the lane clone (`git for-each-ref … | grep -c cursor` → 0). Remote state not inspected → OPEN-OP (prune decision).
3. Wall-clock idleness counter — OPEN-BOT.
4. CVSS v4 → platform-severity lens — repo side LANDED (F01 CVSS v4 admitted r22; F13 r29); rubric lens OPEN-BOT.
5. Reflect on events, not a timer — OPEN-OP.

**2026-10-23**
1. Quote uniqueness plus location in the rechecker — LANDED r24: Q9 exactly-once or anchored (`QUALITY.md:64`).
2. Close-r23 dossier with exact diffs — LANDED r23 (same evidence as 2026-10-22 item 1).
3. Run quote check on F06/F07 before admission — LANDED r23: F07 rewritten to S031 (rule 4.2.6, `SOURCES.md` S031 row present), F06 admitted.
4. Downshift cadence while idle — OPEN-OP.
5. Decide 8 README branches and draft PR #1 — OPEN-OP.

**2026-10-24**
1. Normalise `<u>` markup and pin exactly-once — LANDED: Q8 names the `<u>…</u>` strip declaration (`QUALITY.md:57`); Q9 exactly-once (`:64`).
2. Re-capture snapshots as clean text — PARTIAL. S031 is the normalised capture (landed r23). The render/raw-sha256 debt is recorded in `corpus/lessons/round-25.md:213-214` (cited by the 10-25 reflection, not re-verified here).
3. Close-r23 dossier with all three bodies measured — LANDED r23 (as 2026-10-22 item 1).
4. Downshift cadence — OPEN-OP.
5. Decide PR #1 and README branches — OPEN-OP.

**2026-10-25** (ledger rows and §Round-46/§Round-62 are the lane's own dispositions)
1. Cap wave-evidence bloat — criterion LANDED r28 (`QUALITY.md:83`, R14). Bloat itself OPEN-OP. Measured now: `git ls-files | wc -l` → 14447; `git ls-files | grep -c '^\.ufo/'` → 13799 (95.5 %), exit 0. (Ledger round-46 measured 9342 at `ee03806`.)
2. Track distance to the next score — LANDED r31 (`score-gap.py`) and r39 criteria (`SCORECARD.md:1532`, per ledger). Re-run: `python3 -B corpus/instruments/score-gap.py` → exit 0, prints `gap: 22 of 91 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`. (Ledger's round-46 figure `22 of 65` is superseded by this run.)
3. Bounty craft and SHONEN box 2 — PARTIAL. F13 (r29), exemplar package (r40), claim gate (r43) landed; SHONEN.md:7 is still `[ ]`; the domain task itself is OPEN.
4. Proposal-status ledger — LANDED r30 (`corpus/knowledge/considerthese-proposals-ledger.md`, 172 lines).
5. Open-defects ledger with runnable closure checks — LANDED r29 (R15) and closure scripts r35–r43 (verified present).
6. Event-driven reflections — OPEN-OP (ledger §Round-46 row 6 analogue).

**2026-10-26** (ledger §Round-46 rows 1-7)
1. Make "distance to next score" explicit — LANDED r39 (`SCORECARD.md:1532`, per ledger).
2. Run one end-to-end domain task round — PARTIAL (r40 exemplar, r43 gate); domain task OPEN (SHONEN.md:7 `[ ]`).
3. Quiescence gate before `complete` — LANDED: placeholder half `r35-defect-closure.sh` (present); porcelain half `r36-closure.sh` E9(b); `r46-landing-gate.py` (ledger §Round-46 row 3, per ledger).
4. Cap or externalise wave evidence — OPEN-OP (as 2026-10-25 item 1).
5. Land the owed F18 PROVINCE amendment — LANDED r36 (`PROVINCE.md:77`, verified).
6. Re-tune cadence and depth — OPEN-OP.
7. Keep a proposal-status ledger — LANDED r30 (as 2026-10-25 item 4).

**Ledger gap (for the L1):** `corpus/knowledge/considerthese-proposals-ledger.md` line 3 names only `considerthese/2026-10-25.md` as its source. The 2026-10-19 … 2026-10-24 proposals (34 items) have no ledger row. Their dispositions above are my reading of the repo; the L1 may want to file them.

### 2c. The round's considerthese item: none fits this round

Candidates still OPEN in the lane's own records, checked against the lane bar (`corpus/QUALITY.md`, `SHONEN.md`, `PROVINCE.md`) and this round's bounds:

- **End-to-end domain task (SHONEN box 2).** Does not fit. It needs an authorised target or a public disclosed report executed end-to-end, and this round refuses live-target access (only one documentation page is allowed). SHONEN.md:7 stays `[ ]`, and ledger §Round-62 records that no authorisation or real bounty execution is inferred. PROVINCE's domain (bounty and security research, claim packages) does cover it, so it stays open for a round that carries authorisation.
- **Evidence externalisation (2026-10-25 #1 / 10-26 #4).** Does not fit as a seat item. The criterion is landed (R14) and the keep-or-externalise decision is operator-owned (ledger). The freeze discipline (controls committed at the freeze, `claims.json`) also requires committed receipts, so a seat cannot choose this.
- **Cadence / event-driven reflection (10-22 #5, 10-23 #4, 10-26 #6).** Operator-owned; not a lane-bar item.

Result: **none fit this round.** The lane's bar is not moved by any of them this round.

## 3. Assimilation collision re-derivation (step 3, §6 commands)

Commands (exit codes from each step; `S=/home/vgpnk/Projects/shokuknow`, `A=/fast/scratch/hyaku/kasegi-r76/ConnectOverlap/assimilation`):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"        # exit 0
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"  # exit 0
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"                                                                          # exit 0
```

| file | lines | unique | id range |
|---|---|---|---|
| reg-ids (registry `corpus/SOURCES.md`) | 110 | 110 | S001–S110 |
| staged-ids (`shokuknow/merge/kasegi/SOURCES.append.md`, 89718 bytes, read only) | 94 | 94 | S031–S124 |
| collisions (`comm -12`) | 80 | 80 | S031–S110 |

- Staged ids not in the registry (`comm -23`): S111–S124 (14 ids).
- Collision file: `/fast/scratch/hyaku/kasegi-r76/ConnectOverlap/assimilation/collisions`; copies under `.ufo/waves/round-76/w1/assimilation-ids/` (`reg-ids`, `staged-ids`, `collisions`; `cmp` identical, exit 0).
- **Verdict: collisions nonempty (80), so adoption stays closed. The L0 routing item stands** (r70/r71 questions).

**New finding for C2:** `SOURCES.append.md:87` stages `S111` as a Chinese NCSC weekly-report row. The registry has no S111 today (`grep -c` on `SOURCES.md` for `^ {0,3}\|[[:space:]]*S111[[:space:]]*\|` → 0, exit 1). Simulation (scratch only, lane not touched): `(cat reg-ids; echo S111) | sort` → 111 lines; `comm -12` with staged-ids → **81 collisions**, the 81st being `S111`. Landing C2 with its frozen id S111 adds a collision that the L1 must resolve before integration. I do not choose the id here.

## 4. Verification ledger

| check | command (abridged) | exit | result |
|---|---|---|---|
| sibling OSV grep | `grep -ril -i 'osv' /home/vgpnk/Projects/shokunin/*/corpus \| wc -l` | 0 | 270 files (binary included) |
| corpus dirs | `ls -d /home/vgpnk/Projects/shokunin/*/corpus \| wc -l` | 0 | 21 |
| marker search | `grep -rIil -E 'google.github.io/osv\|…\|osv\.dev'` over siblings | 0 | kasegi-only for OSV API markers |
| S108 overview phrases | `grep -n -E 'six different\|no limits\|OpenAPI\|rate limited' round-73/S108.txt` | 1 | no match |
| S111 hash | `sha256sum corpus/source-snapshots/round-76/S111.txt` | 0 | `6f92e5b7…5581ab`, 48 lines (matches claim) |
| considerthese count | `ls considerthese \| wc -l` | 0 | 8 files; last 2026-10-26 |
| ledger table lines | `grep -c '^\| ' …considerthese-proposals-ledger.md` (includes header and separator rows) | 0 | 54 lines across all sections |
| score gap | `python3 -B corpus/instruments/score-gap.py` | 0 | `gap: 22 of 91 rechecks still gated` |
| F18 / SHONEN | `grep -n F18 PROVINCE.md`; `sed -n '7p' SHONEN.md` | 0 | :77 present; `- [ ]` |
| cursor refs | `git for-each-ref --format='%(refname)' \| grep -c cursor` | 0 | 0 |
| tracked files | `git ls-files \| wc -l`; `… \| grep -c '^\.ufo/'` | 0 | 14447; 13799 |
| assimilation counts | `wc -l` on reg-ids, staged-ids, collisions | 0 | 110, 94, 80 |
| S111 simulation | `(cat reg-ids; echo S111) \| sort \| comm -12 … staged-ids \| wc -l` | 0 | 81 |

Not run: no build, no lane recheck, no snapshot fetch (no network targets allowed to this seat).

## 5. Hand-off notes for the L1

1. C2 S111: resolve the staged-id collision before landing (§3).
2. C2 B6: cite S111:28-36 and 21-22 as located ground; treat the endpoint paths as nav-only (S111:4-9, same as S108:5-9) (§1c).
3. Ledger: add rows for the 2026-10-19 … 2026-10-24 proposals or record that they are out of scope (§2b).
4. Tool installs: none by this seat. Background job `bg_4285` (a `grep` over game-dev-3d) was started by a shell command and is only a read.
