# ConnSibling — contested-scope ruling draft, sibling-overlap synthesis (F17 ground)

Seat: ConnSibling · round 34 · lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c` · claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.
kasegi HEAD read at ruling time: `206e5108f1190e61b3e2622d21cab8a5d921650c`.
Source scan synthesized: `.ufo/waves/round-34/wave1/ScoutSiblingSweep.md` (sha256 `2810a7ed…281ab2`), independently re-verified by the spot-checks in `## Report`.
Read-only across the fleet; writes: this receipt only. No scratch tree created (no fixtures); nothing installed. No lane git/jj mutation.

## Verdict

**Contested scope: none.** No sibling corpus holds, stages, or claims the F17 ground (Immunefi Vulnerability Severity Classification System v2.2 — Web3/smart-contract bounty severity classification). The round-34 admission (`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, header `source: S051`, `ground: F17`) is unambiguously inside kasegi's province (`PROVINCE.md:3` — "bounty & security research — program rules, claim packages"). Nothing is absorbed from a sibling because no sibling ground exists; nothing is reported to another lane because no sibling contests it. PROVINCE adjacency upheld in both directions.

## Per-hit rulings (every nonzero sweep cell)

Token set swept by ScoutSiblingSweep: `Immunefi`, `VSCS`, `severity classification`, `smart contract` (regex `smart.contract`), `Web3`, `blockchain`, `bounty`; scope: 20 sibling `corpus/` + `SKILL.md`, fleet root files, per-lane `considerthese/`. Counts table and method: ScoutSiblingSweep §1–§2. Ruling per hit family:

| hit | location (path:line) | what it is | ruling |
|---|---|---|---|
| `Immunefi` ×1 | `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json:651` | Verbatim mirror of **kasegi's own** `SKILL.md:130` (byte-compared in `## Report`), carried in kotoba's citation-routing audit of kasegi. Citation of kasegi, not a sibling claim. | **no contested scope** |
| `bounty` ×34 (chousa, 25 files) | e.g. `corpus/knowledge/scope-refusal-r12.md:21` — "`bug bounty` … `claim package(s)`, `kasegi` → `SCOPE_BOUNTY_ABSORBED` → kasegi"; `SKILL.md:3,10,57,152`; `PROVINCE.md:10`; evidence demo logs | chousa's declared-scope refusal machinery: bounty-program scope is **refused** by chousa and routed to kasegi. Boundary enforcement in kasegi's favor. | **no contested scope** |
| `bounty` ×14 (kengaku, 7 files) | `corpus/evidence/round9-fleet/sibling-overlap.md:11,13,23,25`; `round11-fleet/r11-connector.md:15,24`; `round12-fleet/r12-connector.md:74,78,93`; `round14-fleet/INTEGRATOR-NOTES.md:29`, `r14-connector.md:45`, `r14-scout-surfaces.md:137,147`; `r12-report-final.md:208` | Fleet sibling-overlap / route-telemetry / ledger-absence notes that **name kasegi as owner** of the bounty domain. | **no contested scope** |
| `bounty` ×36 (kotoba, 7 files) | `sibling-citation-routing-round16.json:500,637,651,1905,1906,2744,2750,2757,2758`; `sibling-description-rewrites-round8.md:259–326,376,418–444`; `sibling-overlap-census-round49.md:77`; `sibling-overlap-census-round74.md:61,92`; `lessons/round-16.md:22,25`; `lessons/round-49-verifier-spotcheck.md:171` | kotoba's audits of kasegi's SKILL description and sibling-overlap censuses — routing/citation text only. | **no contested scope** |
| `bounty` ×3 (kake) | `corpus/knowledge/origin-repos.md:49` (repo-name glob `veigapunk-bounty-audit-*`); `corpus/lessons/round-35.md:50` (security.txt example row quoting GitHub's served file, `Policy: https://bounty.github.com` — GitHub's program page, **not** Immunefi/VSCS); `corpus/README.md:465` | kake's province explicitly **excludes** the ground: `PROVINCE.md:284–286` "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, **bounty and policy operation** … are not kake's". Severity classification is triage. | **no contested scope** (adjacent, self-disclaimed) |
| `bounty` ×2 (kama) | `corpus/knowledge/cross-lane-scope.md:43,51` — "kama retains endpoint identity and kasegi retains bounty/target-scope research" | Cross-lane routing note naming kasegi as owner. | **no contested scope** |
| `bounty` ×1 (kagi) | `corpus/lessons/round-11.md:184` — mentions kasegi's `ops/claim-check.mjs` | Tool cross-reference. | **no contested scope** |
| `bounty` ×1 (tabi) | `corpus/knowledge/csrf-defense-shape-boundary.md:19` — "fleet roster's bounty/security-research lane" | Own-scope provenance line naming the roster assignment. | **no contested scope** |
| `bounty` ×1 (kumitate) | `corpus/knowledge/ops-watchers.md:30` — "Refires stale bounty-hunt UFOs" | Orchestration watcher vocabulary, not a content holding. | **no contested scope** |
| `bounty` ×1 (kotodama) | `corpus/knowledge/civilizations/arabia-pre-islamic.md:137` — Qur'an 2:198 "seeking bounty" (trade) | Unrelated lexical accident in a historical text. | **no contested scope** |
| `bounty` (fleet root) | `MANIFEST.json:9,2314,4430`; `MISSION.md:23`; `README.md:112`; `ROADMAP.md:7`; `shokunin.conf:46` | Roster/scope declarations assigning the domain to kasegi. The other six tokens: **0 hits** in every swept root file, `research/`, `templates/`, `scripts/`, `.ufo/{scopes,prompts,state,gates,l0-questions.md}`. | **no contested scope** |
| whole-lane noise (mori, souji, kotoba, kaidoku `.ufo`/`.scratch`) | `mori-shokunin/.scratch/r48-ScoutQuarantineS262/roma.txt:1379,1381`; `souji-shokunin/census/round-26/.../fixture-src-*/real-home*.md`; `kotoba .ufo/round-44/evidence/omp-live-18.12.2-strings.txt:523413,1320853,1320854` | Paper-text/tool-string noise outside `corpus/` holdings. | **no contested scope** (not corpus content) |
| per-lane `considerthese/` (16 siblings) | — | 0 hits on all seven tokens. | nothing to rule |

Zero-hit siblings on all seven tokens: audio, game-dev-2d, game-dev-3d, kaidoku, lore, mado, mori, revenger, souji, tameshi, tsukuroi (11).

### Adjacent, but not contested (kept distinct for the lesson)

1. **kaidoku / revenger — EVM bytecode.** `kaidoku-shokunin/PROVINCE.md:54` (`inspect-evm-interface`), `:91` ("EVM bytecode (extended)" Frontier). Byte/selector recovery layer, zero severity/claim wording. Prior fleet ruling on the same ground pair: `revenger-shokunin/.ufo/waves/round-61/build/ConnectorKasegiEvm.md:66` — "kasegi owns the *claim/package* layer, revenger C09 … the *byte-offset* layer … report both counter-examples to kasegi and never cite kasegi for a byte claim". F17 is severity/claim classification — claim layer, kasegi-owned; the prior ruling stands and points the same direction. `revenger/reports/round-62/claims.md:75` ("REA producers, blockchain calls …") is an exclusion clause, i.e. revenger **refuses** blockchain calls. Ruling: **no contested scope**.
2. **kake — security.txt publishing.** `kake-shokunin/PROVINCE.md:202–292` (RFC 9116, S078–S085) serves a vulnerability-reporting pointer; the boundary at `:284–286` excludes triage/bounty-policy, which is where severity classification lives. Ruling: **no contested scope**.

### Report-to-lane triggers

None this round. Standing rule unchanged (kasegi `PROVINCE.md` "Refuses" line): any future sibling staging of Immunefi/VSCS/Web3-severity ground is **reported to the lane, not absorbed**; conversely kasegi absorbs nothing sibling-owned.

Boundary note: staged `merge/kasegi/` entries in the shokuknow campaign are not sibling corpora; their standing-refusal/flip-condition verdicts are the assimilation Gate's instrument (ScoutPackageThemes → ScribeAssimilationGate; claims.json non-claim item records "Assimilation: none" this round). This ruling covers sibling corpora + fleet themes only.

## Ruling draft for the lesson (adjacency paragraph — for ScribeLesson integration)

> **Adjacency / contested scope (connector ruling).** Sibling sweep of the F17 ground (ScoutSiblingSweep, corroborated by ConnSibling spot-checks): seven tokens × 20 sibling corpora + SKILL.md + fleet root + per-lane considerthese — no sibling holds, stages, or claims the Immunefi/VSCS/Web3-severity ground. The single `Immunefi` hit is a kotoba citation-routing mirror of kasegi's own `SKILL.md:130`; every `bounty` hit is routing/refusal text naming kasegi as owner (chousa `SCOPE_BOUNTY_ABSORBED`; kake's explicit exclusion of "bounty and policy operation" at `PROVINCE.md:284–286`), a cross-reference, or unrelated lexical noise. Adjacent-but-not-contested: kaidoku/revenger own the EVM byte-offset layer (prior fleet ruling revenger r61 keeps them byte-scoped; kasegi keeps the claim/package layer — the layer F17 sits in); kake owns security.txt publishing and excludes triage. Ruling: **no contested scope** — F17 is kasegi-owned under `PROVINCE.md:3`; PROVINCE Adjacent (chousa, kagi, kake, kengaku) re-confirmed as route-or-disclaim, none absorbing; nothing reported to another lane this round.

## Report

Commands run (cwd `/home/vgpnk/Projects/shokunin` unless noted; all grep/sed pipelines completed; `grep` exits 1 on a no-match lane, which is the expected zero-hit signal in per-lane loops — the printed hit lists are the output):

1. Primary sweep, sibling `corpus/SKILL.md` only —
   `for d in /home/vgpnk/Projects/shokunin/*-shokunin; do … [ "$name" = kasegi-shokunin ] && continue; grep -inE 'immunefi|vscs|severity classification|smart[- ]?contract|web3|blockchain|bounty' "$d/corpus/SKILL.md"; done`
   Output: `=== <each of 20 siblings> : NO corpus/SKILL.md ===` — **no sibling lane has a `corpus/SKILL.md` at all**; exit 0 for the loop body per iteration (file-missing branch printed the marker). Zero-hit by construction at that exact path; ScoutSiblingSweep's scope (`corpus/` + root `SKILL.md`) is the authoritative one and is used below.
2. Recursive sibling sweep, all corpora content, excluding `.ufo/waves/` —
   `grep -rinE 'immunefi|vscs|severity classification|smart[- ]?contract|web3|blockchain|bounty' <sibling> --include='*.md' --include='*.txt' --include='*.json' -l | grep -v '/.ufo/waves/'`
   Output: hit families exactly as tabled above (chousa 16 files incl. evidence logs; kagi 1; kaidoku 1; kake 4; kama 2; kengaku 10; kotoba 18; kotodama 4; kumitate 1; mori 2; revenger 1; souji 6 fixture files; tabi 1) + `DONE-RECURSIVE-SWEEP`. Corroborates ScoutSiblingSweep §2/§3 (which also swept `.ufo` via `-uu` and found only the same noise classes). Lanes printing nothing = grep exit 1 (no match), expected.
3. Fleet `merge/` + `considerthese/` at root —
   `ls /home/vgpnk/Projects/shokunin/merge /home/vgpnk/Projects/shokunin/considerthese` → **neither directory exists at fleet root** (exit 2 from ls, recorded); `grep -rinE '<tokens>' merge/ considerthese/` → no such dir, nothing swept there. Scout concurs (§6); per-lane `*/considerthese/` (16 lanes) swept by scout: 0 hits on all seven tokens.
4. Spot-checks of the scout's load-bearing lines (all exit 0, output shown):
   - `sed -n '130p' kasegi-shokunin/SKILL.md` → the `| Immunefi/Cantina/HackenProof | …` capture row (kasegi's own prior-art mention of Immunefi as a bounty-platform page).
   - `grep -n 'Immunefi/Cantina/HackenProof' kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json` → `:651`, byte-identical row text (mirror confirmed).
   - `sed -n '21p' chousa-shokunin/corpus/knowledge/scope-refusal-r12.md` → "`bug bounty`, `bounty program(s)`, …, `kasegi` | `SCOPE_BOUNTY_ABSORBED` | kasegi".
   - `sed -n '284,286p' kake-shokunin/PROVINCE.md` → "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, bounty and policy operation … are not kake's".
   - `sed -n '54p;91p' kaidoku-shokunin/PROVINCE.md` → EVM interface core row; "EVM bytecode (extended)" Frontier line.
   - `sed -n '66p' revenger-shokunin/.ufo/waves/round-61/build/ConnectorKasegiEvm.md` → "VERDICT: Overlap is one proposition, not a method — keep C09 byte-scoped … report both counter-examples to kasegi and never cite kasegi for a byte claim".
5. Sibling `corpus/knowledge` ground check —
   `for d in …/*-shokunin; do … grep -rinE 'immunefi|vscs' "$d/corpus/knowledge"; done`
   Output: exactly **one** hit — the kotoba citation-routing mirror at `:651`. No sibling knowledge entry names Immunefi or VSCS. (grep exit 1 on all other lanes = zero hits, expected.)
6. kasegi own-tree anchors —
   `ls corpus/knowledge | grep -i immunefi` → `immunefi-vscs-v2-2-smart-contract-severity.md`; header shows `source: S051 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ …`, `verified-at: 2026-10-26`, `ground: F17`.
   `git rev-parse HEAD` → `206e5108f1190e61b3e2622d21cab8a5d921650c` (matches scout's sweep-time HEAD).

Digests (sha256) at ruling time:
- `.ufo/waves/round-34/wave1/ScoutSiblingSweep.md` — `2810a7ed569aeec467a123941ad80bf50a2e5e1ff9403edacc5695e3d6281ab2`
- `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` — `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`
- `PROVINCE.md` (kasegi) — `b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679`
- `SKILL.md` (kasegi) — `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`
- `chousa-shokunin/corpus/knowledge/scope-refusal-r12.md` — `393470188506d7eb97b334103e5cc89b06687677cf4bf56155aa926e52af1c46`
- `kake-shokunin/PROVINCE.md` — `5cc33b015f2691d7b387b60a41cd27cf943513f979143d3bbf2a28947956f7e3`
- `kaidoku-shokunin/PROVINCE.md` — `ecfa491fa315047a6797bd660b239f29e5e1d9c548e38e943e398a9eb0a8d242`
- `revenger-shokunin/.ufo/waves/round-61/build/ConnectorKasegiEvm.md` — `f844dbb6a161616fd9e536773256b4250d9fe67f5fffe068c085f14344240551`
- `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json` — `6674dca126e5be915f759b32005600788337de0ad470fa26473814d0bf408882`
- `MANIFEST.json` (fleet root) — `33ab3ce11e3fa1b5aaadbd6a0d21b20a87dd82c8c522aa7db33f3cf0fe9b257c`

Limits: sibling working copies read as-on-disk (HEADs unpinned); the `merge/kasegi/` staged-entry verdicts belong to the assimilation Gate, not this ruling; scout's scoped `corpus/`+`SKILL.md` counts are uncapped and authoritative, my recursive pass corroborates the hit families and adds no new class of hit. Installs: none. Scratch: none created, none left. Writes: this receipt only. No git/jj mutation.
