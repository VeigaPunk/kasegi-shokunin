# Round 74 — ConnectorSweep (cross-claim, cross-lane and considerthese scan)

Seat: ConnectorSweep (leaf; read-only; no lane writes, no git mutation, no subagents).
Frozen reference: freeze commit `847b53792d2d29d161cad7d21a33c89df9e52e8d` (controls `654d877`, base `ccd6a54`). Every lane file below was read from that commit via `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 847b537… | tar -x -C <scratch>/tree` (read-only export into scratch), or `git show 847b537…:<path>`. The live lane working tree was consulted only where marked.
Tools installed or upgraded: none.

## Result summary

| item | verdict | evidence (command → exit) |
|---|---|---|
| (2) Sibling overlap, Fuzzilli | **no sibling holds Fuzzilli ground**; distinctness of F52 vs siblings certified for the Fuzzilli-specific ground | `_grep (?i)fuzzilli` over 20 sibling repos → 1 file (chousa round-80 receipt quoting kasegi's own lead line) |
| (2) Sibling overlap, recheck-cwd / claim-package | no sibling holds the instrument or the contract; all hits cite kasegi-owned files | `_grep (?i)recheck-cwd\|recheck-cwd-census\|claim-package-check` and `(?i)recheck-cwd\|claim-package` over 20 siblings → citations only |
| (2) **Wording defect in the screen** | `distinctness_screen.siblings` says "none holds fuzzer tool documentation". Literally false: revenger holds other fuzzer-tool documentation (DecFuzzer, mishegos). Distinctness of F52 still holds. Reported, not reworded (claims.json binding). | `_grep (?i)fuzzer…` over sibling `corpus/` → revenger `corpus/SOURCES.md:132` (S117 DecFuzzer README), `:411` (S396 mishegos README) |
| (3) considerthese 2026-10-26, proposal 1 (distance to next score) | **implemented (round 39)** | `grep -n '^## Distance' SCORECARD.md` on frozen tree → `1532`, exit 0 |
| (3) proposal 2 (end-to-end claim-package trial) | **partially landed; domain task open** (checker landed r43; SHONEN box 2 unchecked) | `python3 corpus/instruments/claim-package-check.py …/exemplar` → `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`; `--selftest` → `selftest cases=10 failures=0`, exit 0; `SHONEN.md:7` `- [ ]`, exit 0 |
| (4) L0 rows for kasegi r57–r60, r70–r73 | r57–r60 and r70–r72 are not claimed this round; r73 (RC-8) routed around, and C1 kill rule (d) enforces it. **None blocks round 74**; several remain unanswered (see §4). | `grep -n -i kasegi .ufo/l0-questions.md` → rows at lines 269, 273, 279, 293, 307, 308, 313, 315, exit 0 |
| (5) Lead overlap | C2 consumes the **only** `## Leads (unopened)` bullet (Fuzzilli). C1 shares no surface with any lead. Next-round candidates: NDSS 2023 paper (named in S109, not a lead); OpenSSF aggregate-score computation (undefined in two held entries, no lead line). | `awk '/^## Leads/' SOURCES.md` on HEAD → 1 bullet, exit 0 |

## 1. Scope read

- `claims.json` read in full (`.ufo/waves/round-74/claims.json`). C1 = counter amendment on `corpus/instruments/recheck-cwd-census.py` (depth:verifiability, 4 → 4). C2 = admit F52 on S109 (coverage, 8 → 8). Non-claim work: end-to-end trial (SHONEN box 2 / considerthese proposal 2), R73-V1/V2/V4/V6.
- Frozen-tree facts consumed here: `ls corpus/knowledge/*.md | wc -l` → 89 (matches base); `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 51 (matches base); `grep -c '^|' corpus/SOURCES.md` → 110 table lines; the registry tail at HEAD is S106, S107, S108 (`grep -n -E '^\| *S1[0-9]{2}' SOURCES.head.md` → lines 118–120), so S109 is free in the registry.
- S109 capture: `git show 847b537…:corpus/source-snapshots/round-74/S109.txt > <scratch>/S109.txt` → `sha256sum` = `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`, `wc -l` = 375. Matches the claim's pinned digest and line count.

## 2. Sibling-overlap scan (certifies `distinctness_screen.siblings`)

Scope: all 20 sibling lane repos present under `/home/vgpnk/Projects/shokunin/` (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi). kasegi excluded.

Commands and results (`_grep`, case-insensitive; no file-level pagination was returned):

1. `(?i)fuzzilli` over the 20 sibling roots → one file: `chousa-shokunin/.ufo/waves/round-80/w1/R80ConnectorA/kasegi-search.txt` (receipt quoting kasegi's own `## Leads` Fuzzilli line and the registry arithmetic). chousa holds a copy of kasegi text; it holds no Fuzzilli documentation ground.
2. `(?i)recheck-cwd|recheck-cwd-census|claim-package-check` over the 20 roots → hits only in files that **cite** kasegi paths or quote kasegi output: chousa round-80 receipts (`kasegi--corpus__QUALITY.md`, `kasegi-narrow.txt`), kake round-92 `ConnectorScope/receipts/query-*.txt`, tameshi round-58 `T58W1ConnSib-receipts/sweep.json`, kagi round-28 `build/ConnKasegi.md` (documentation of kasegi's contract; states no executable exists in `corpus/instruments/`). No sibling holds `recheck-cwd-census.py`, `claim-package-check.py`, or the claim-package contract.
3. `(?i)fuzzer|libfuzzer|afl\+\+|honggfuzz|jazzer` over the 20 sibling `corpus/` trees → hits:
   - revenger `corpus/SOURCES.md:132` S117 DecFuzzer ISSTA'20 artifact README; `:411` S396 trailofbits/mishegos x86-decoder differential fuzzer README; `:131` S116 ISSTA 2020 decompiler tester paper. **These are fuzzer-tool documentation grounds, held by a sibling.** Different tools, different domain (decompilers, x86 decoders), not Fuzzilli, not JS engines.
   - revenger `knowledge/claude-red-re-bridge.md:20,32` (generic "fuzzer primary docs" routing rule; no tool doc held).
   - kengaku `corpus/evidence/round53/fetched/*.html` (arXiv KernelBench paper text: "fuzzer" = input generator in an LLM-kernel benchmark). Not tool documentation.
   - mori `corpus/evidence/sources-r55|r61` and tabi `corpus/evidence/round-29/release-pins/…content_switches.cc` (kernel parameter docs; Chromium IPC-fuzzer switches). Not fuzzer-tool documentation of Fuzzilli's kind.

Conclusion (Fuzzilli-specific ground): **distinct**. No sibling holds the Fuzzilli project's documentation, its FuzzIL/REPRL/tree-hierarchy descriptions, or the S109 source. The literal phrase "none holds fuzzer tool documentation" in `distinctness_screen.siblings` is **overbroad** (revenger holds S117/S396). Not reworded here; flagged for L1 to narrow in the report text, not in the frozen predicate.

Frozen-tree check on the F52 neighbourhood (`grep -rln -i ndss corpus/` in the export, cwd = scratch tree): only `corpus/source-snapshots/round-74/S109.txt`. No NDSS row or lead exists yet. The live working tree was not searched for this item.

## 3. considerthese mining

Files: `considerthese/2026-10-19.md` … `2026-10-26.md` (8 files, `ls` exit 0). Latest: `2026-10-26.md`, 35 lines, seven numbered self-improvement suggestions.

- **Proposal 1 — "Make 'distance to next score' explicit": implemented (round 39).**
  Evidence: frozen tree `grep -n -E '^## Distance-to-next-score|^### (depth|coverage)' SCORECARD.md` → `1532 ## Distance-to-next-score (round 39, mined from considerthese 2026-10-26 proposal 1)`, `1536 ### depth:verifiability, 4 → 5`, `1547 ### coverage, 7 → 8`; exit 0. The section states the two promotion bars and the measured distance at round-39 base. `corpus/instruments/score-gap.py` present (554 lines by `grep -c ''`, exit 0). **Not re-run** in this seat: it executes `recheck-audit.py`, which runs recheck values through `bash -c` (RC-8 surface); running it from a sweep seat would exercise that surface. The most recent gated count in the lane's text (working-tree `SCORECARD.md:2541`, read by grep, not frozen-tree verified) is "22 of 81 rechecks still gated"; recorded as text, not as a measurement here.
- **Proposal 2 — "Run one end-to-end domain task round": partially landed; domain task open.**
  Landed: `corpus/instruments/claim-package-check.py` and `claim-package-selftest.py` (both present in the frozen tree), fixtures `corpus/instruments/fixtures/claim-package/{exemplar,defect-1..9}`.
  - `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` (cwd = frozen-tree export) → `package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.
  - `python3 corpus/instruments/claim-package-check.py --selftest` → `selftest cases=10 failures=0`, exit 0.
  - exemplar `status.json` line 6: `"claimable": false` (grep exit 0). The exemplar fixture is parked; no live domain package is evidenced in the frozen tree.
  - `SHONEN.md:7`: `- [ ] At least one end-to-end domain task executed and logged in LOG.md` (grep exit 0). Box 2 remains unchecked.
  - Ledger status: `corpus/knowledge/considerthese-proposals-ledger.md` round-62 section (`## Round-62 dispositions`, last section) = "partially landed / domain task open". **Stale text in the ledger:** rows at round-41 (`:124`) and round-43 (`:139`) say "claim-checker remainder still absent / no `corpus/instruments/` basename contains `claim`"; that is no longer true (the checker is committed and passes its own selftest). Recorded here; the ledger is not edited by this seat.
- Proposals 3–7 (quiescence gate, evidence externalisation, F18 PROVINCE amendment, cadence, proposal ledger): dispositions per the ledger (landed r36–r38 for 3 and 5; open/operator-owned for 4 and 6; landed for 7). **Ledger-cited, not re-verified in this seat.**

## 4. L0 sweep (`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, 318 lines)

`grep -n -i kasegi .ufo/l0-questions.md` → kasegi rows for rounds 12, 15, 16, 17, 32, 41, 46, 48, 49, 50, 54, 57, 58, 59, 60, 70, 71, 72, 73. The file has no answered/unanswered column; "unanswered" below means no reply row exists in the file.

| row | question | status vs round 74 |
|---|---|---|
| r57 (line 269) | authorise counter amendment for body-substance (stub entry body admitted by the frontier counter) and pinned-range rule for census bases | **routed around**: round 74 adds no body-substance limb. C2's entry is substantive, but the FRONTIER-PASS counter still cannot reject a stub. Unanswered. Blocks nothing in round 74. |
| r58 (line 273) | re-ask of r57 (a) and (b); figure-audit selftest kills 7 of 15 | **routed around**: no figure-audit or census-range claim. Unanswered. Blocks nothing. |
| r59 (line 279) | figure-audit derive gate security boundary (operator decision) | **blocks nothing**: round 74 touches the recheck-cwd census and the frontier counter, not the derive gate. |
| r60 (line 293) | figure-audit write-flag spellings (decoded bash forms) | **blocks nothing**: same as r59. |
| r70 (line 307) / r71 (line 308) | assimilation drift: staged `merge/kasegi/SOURCES.append.md` ids collide with registry | **routed around**: adoption stays closed; no staged row is adopted by C2. See §5 for a new id-collision fact. Unanswered. |
| r72 (line 313) | C2 `api_key` amendment (`claims-amendment-c2.json`) awaiting accept/reject | **blocks nothing**: round 74 claims do not touch S107. Unanswered. |
| r73 (line 315) | may the first recheck value run through `bash -c` in a counter (RC-8) | **routed around, enforced**: C1 explicitly does not expand the surface. Base counter has exactly one `bash -c` call site: `grep -n -E 'bash|subprocess' corpus/instruments/recheck-cwd-census.py` (frozen tree) → line 51 `subprocess.run(["bash", "-c", value], …)`; `grep -c 'bash -c'` → 1, exit 0. C1 kill rule (d) requires the count to stay at one. Unanswered; blocks nothing if (d) holds. |

## 5. Cross-source pattern and next-round candidates

- `awk '/^## Leads/' corpus/SOURCES.md` on HEAD `847b537` → `## Leads (unopened)` has **one** bullet: `- Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.` (exit 0).
  - C2 consumes exactly this bullet's surface. The claim's registry predicate does not name the Leads line. The round-68 precedent (`SOURCES.md` Registry-changes bullet: "lead line removed, row S102 added") retires a lead as a changelog entry, not a registry cell. L1 should retire the Fuzzilli bullet the same way, as an appended changelog bullet, to keep "every pre-existing row unchanged" true.
  - C1 shares no surface with any lead.
- **Candidate, NDSS 2023 Fuzzilli paper.** Named in S109 at `S109.txt:243` ("A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers."). Not a registry row; not opened. C2 scope excludes its content (existence and name only). A next-round lead; needs its own capture and source id.
- **Candidate, OpenSSF aggregate-score computation.** The API lead was retired as opened (S102, round 68). The aggregate 0–10 score is named as undefined in held entries: `corpus/knowledge/openssf-scorecard-checks.md:91` ("The aggregate 0-10 score computation, the risk-based weights …") and `corpus/knowledge/openssf-scorecard-api-contract.md:100,122`. No `## Leads` line carries it at HEAD (`grep -n -i aggregate` over `corpus/SOURCES.md`: only S086/S102 rows and the round-61 narrowing note). Next-round lead, to be screened against S086 and S102 before opening, so as not to re-admit the check taxonomy.
- **Id-collision fact (new, for L1).** The staged assimilation package `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` carries `S109` = "GB/T 30279-2020 征求意见稿" (`grep -n -E '\bS109\b'` → line 85, exit 0). Adoption stays closed (r70/r71), so no current registry collision exists; C2's S109 is lane-local. If the staged package is ever re-staged by id, S109 must be re-id'd. Staged package has 94 `S`-id rows (`grep -c -E '^\| *S[0-9]{3,}'` → 94, exit 0).

## 6. Verification commands (all run by this seat)

| command | cwd | exit |
|---|---|---|
| `S=/fast/scratch/hyaku/kasegi-r74/ConnectorSweep; mkdir -p "$S"` | — | 0 |
| `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 847b537… \| tar -x -C $S/tree` | — | 0 |
| `git -C … rev-parse HEAD` → `847b53792d2d29d161cad7d21a33c89df9e52e8d` | — | 0 |
| `git -C … rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kasegi-shokunin` | — | 0 |
| `git -C … show 847b537…:corpus/SOURCES.md > $S/SOURCES.head.md` | — | 0 |
| `git -C … show 847b537…:corpus/source-snapshots/round-74/S109.txt > $S/S109.txt`; `sha256sum` → `c9a7adfb…568d486`; `wc -l` → 375 | — | 0 |
| `ls corpus/knowledge/*.md \| wc -l` → 89 | `$S/tree` | 0 |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 51 | `$S/tree` | 0 |
| `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` → `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` | `$S/tree` | 0 |
| `python3 corpus/instruments/claim-package-check.py --selftest` → `selftest cases=10 failures=0` | `$S/tree` | 0 |
| `grep -n -E '^## Distance-to-next-score\|^### (depth\|coverage)' SCORECARD.md` → 1532/1536/1547 | `$S/tree` | 0 |
| `grep -n -E '^- \[' SHONEN.md` → `:7` `- [ ]` | `$S/tree` | 0 |
| `grep -n -E 'bash\|subprocess' corpus/instruments/recheck-cwd-census.py` → 9, 28, 51, 52, 55; `grep -c 'bash -c'` → 1 | `$S/tree` | 0 |
| `grep -rln -i ndss corpus/` → `corpus/source-snapshots/round-74/S109.txt` | `$S/tree` | 0 |
| `grep -n -i kasegi /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` → kasegi rows, lines 1–315 | — | 0 |
| `_grep` sibling scans (three patterns, 20 roots) | — | returned as cited in §2 |
| `grep -n -E '\bS109\b' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` → 85 | — | 0 |

Not run, by design: `score-gap.py` and `recheck-audit.py` (executes recheck values through `bash -c`; RC-8 surface), and any live fetch (no network calls made).

## 7. Risks and open items for L1

1. `distinctness_screen.siblings` wording is overbroad (revenger S117/S396). Distinctness of F52 holds; wording should be narrowed in the report, not the predicate.
2. Fuzzilli lead bullet retirement must be a changelog bullet (round-68 precedent), not a registry-cell edit.
3. Ledger rows at `considerthese-proposals-ledger.md:124` and `:139` are stale about the claim-checker's absence; a future ledger append should correct them (not in this round's claims).
4. The staged package's S109 (GB/T draft) collides with C2's S109 if the package is ever re-staged by id.
5. RC-8: C1 kill rule (d) must be checked against the single `bash -c` line at `recheck-cwd-census.py:51` (count = 1 at base).

Scratch: `/fast/scratch/hyaku/kasegi-r74/ConnectorSweep` (export tree, S109 copy, SOURCES copy, two gate outputs) is removed before yield; no evidence file was written outside this report.
