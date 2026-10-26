# ScoutSiblingSweep — negative sibling sweep for the C2 ground (F17, Immunefi VSCS v2.2)

Seat: ScoutSiblingSweep · round 34 · lane base `014ee2d7…` · kasegi HEAD read at sweep time `206e5108f1190e61b3e2622d21cab8a5d921650c`. Read-only; no lane file touched except this receipt. No scratch dir was created (nothing to clean). No installs.

## Verdict (for the connector)

**No sibling lane claims the C2 ground.** Seven tokens × 20 siblings (all `*-shokunin` except kasegi), scope `corpus/` + `SKILL.md`:

- `Immunefi`: 1 hit (kotoba), and it is a verbatim mirror of **kasegi's own** `SKILL.md:130` — not a competing claim.
- `VSCS`, `severity classification`, `smart contract` (regex `smart.contract`), `Web3`, `blockchain`: **0 hits in every sibling's corpus/SKILL.md.**
- `bounty`: hits in 9 siblings, **all** routing/refusal/cross-reference text pointing AT kasegi (no sibling hosts bounty content of its own; kotodama's one hit is an unrelated Qur'an translation, "seeking bounty").
- Fleet root: bounty/security is declared kasegi's only (`MANIFEST.json:9`, `MISSION.md:23`, `README.md:112`, `ROADMAP.md:7`, `shokunin.conf:46`); the other six tokens have 0 hits at root files, `research/`, `templates/`, `scripts/`, `.ufo/{scopes,prompts,state,gates,l0-questions.md}`.

Nearest adjacent (adjacent ≠ contested) grounds a connector might be asked about:
1. **kaidoku / revenger** — EVM *bytecode* (selectors, opcodes). Byte layer, not severity/claim layer. See §4.
2. **kake** — `security.txt` publishing (RFC 9116). Explicitly excludes triage/bounty/policy. See §5.

Contested scope: none found. F17 (bounty-severity classification) is unambiguously inside kasegi PROVINCE.md:3 "bounty & security research".

## 1. Method

Commands (cwd `/home/vgpnk/Projects/shokunin`; `rg` 15.x at `/home/vgpnk/.local/bin/rg`, case-insensitive `-i`):

```
for d in *-shokunin; do [ $d = kasegi-shokunin ] && continue
  for t in 'Immunefi' 'VSCS' 'severity classification' 'smart.contract' 'Web3' 'blockchain' 'bounty'; do
    rg -i -c --no-messages -- "$t" $d/corpus $d/SKILL.md ; done ; done          # exit 0
rg -i -n --no-messages 'bounty|Immunefi' <each sibling hit-lane>/corpus <lane>/SKILL.md   # line listing
rg -i -uu -n -g '!.git/**' 'Immunefi|VSCS|severity classification|smart.contract|Web3|blockchain' -- <lane>   # whole-lane wide sweep (incl. .ufo, .scratch)
rg -i -n -H '…|\bEVM\b|Solidity|bounty' */{PROVINCE,README,AGENTS,MINT,SHONEN,SKILL}.md   # top-level docs
rg -i -n  '…|bounty' */considerthese                                           # considerthese dirs
rg -i -n  '…|bounty' <fleet-root md/json + research templates scripts .ufo/…>   # fleet root
```

Layout facts (observed): all 20 siblings (every `*-shokunin` except kasegi) have `corpus/`; `audio-shokunin` and `game-dev-2d-shokunin` have **no `SKILL.md`** (corpus only, so only their `corpus/` was swept). `souji-shokunin` has no README.md. Largest corpora: game-dev-3d 121 039 files, game-dev-2d 54 559, audio 49 569 (all swept; zero hits for the six non-bounty tokens).

## 2. Per-sibling table (corpus/ + SKILL.md; counts are matching lines)

| sibling | Immunefi | VSCS | severity classification | smart contract | Web3 | blockchain | bounty |
|---|---|---|---|---|---|---|---|
| audio | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| chousa | 0 | 0 | 0 | 0 | 0 | 0 | 34 (25 files) |
| game-dev-2d | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| game-dev-3d | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kagi | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| kaidoku | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kake | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| kama | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| kengaku | 0 | 0 | 0 | 0 | 0 | 0 | 14 (7 files) |
| kotoba | **1** | 0 | 0 | 0 | 0 | 0 | 36 (7 files) |
| kotodama | 0 | 0 | 0 | 0 | 0 | 0 | 1 (unrelated) |
| kumitate | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| lore | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mado | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mori | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| revenger | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| souji | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tabi | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| tameshi | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tsukuroi | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Zero-hit siblings on **all seven** tokens: audio, game-dev-2d, game-dev-3d, kaidoku, lore, mado, mori, revenger, souji, tameshi, tsukuroi (11). (kaidoku/revenger do carry EVM-bytecode text — a token outside the assigned seven; §4.)

## 3. Hit locations (path:line), every nonzero cell

**Immunefi (1):**
- `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json:651` — row `| Immunefi/Cantina/HackenProof | Public bounty pages with contract scope …`. This is the verbatim text of **kasegi-shokunin/SKILL.md:130** (same row, confirmed by `rg 'Immunefi/Cantina/HackenProof' kasegi-shokunin/corpus kasegi-shokunin/SKILL.md` → `SKILL.md:130`), carried in kotoba's citation-routing audit of kasegi. Citation of kasegi, not a sibling claim.

**bounty — chousa** (refusal/scope-screen text; chousa REFUSES bounty scope → kasegi): `corpus/knowledge/fenced-heading-r17.md:14`; `hardening-r10.md:447`; `scope-phrase-gap-r18.md:28`; `scope-refusal-r12.md:21,26,31,50`; `corpus/README.md:657,660,737`; `SKILL.md:3,10,57,152`; plus 21 `corpus/evidence/*` logs/READMEs (`…-selftest.log:86 ok-case 86 scope-fail-bounty exit=1`, `fence-r17…demo.log:7`, `verify-r20…demo.log:7`, `README.md:961,1003`). Line 21 of scope-refusal-r12.md: "`bug bounty`, `bounty program(s)`, `bounty hunt(ing)`, `bounty scope`, `claim package(s)`, `kasegi` → `SCOPE_BOUNTY_ABSORBED` → kasegi".
**bounty — kagi:** `corpus/lessons/round-11.md:184` (mentions kasegi's `ops/claim-check.mjs`).
**bounty — kake:** `corpus/knowledge/origin-repos.md:49` (a repo-name glob `veigapunk-bounty-audit-*`); `corpus/lessons/round-35.md:50` (security.txt example row, GitHub's served file); `corpus/README.md:465` (kake excludes "bounty and policy operation").
**bounty — kama:** `corpus/knowledge/cross-lane-scope.md:43,51` ("kama retains endpoint identity and kasegi retains bounty/target-scope research").
**bounty — kengaku:** `corpus/evidence/round11-fleet/r11-connector.md:15,24`; `round12-fleet/r12-connector.md:74,78,93`; `round12-fleet/r12-report-final.md:208`; `round14-fleet/INTEGRATOR-NOTES.md:29`; `round14-fleet/r14-connector.md:45`; `round14-fleet/r14-scout-surfaces.md:137,147`; `round9-fleet/sibling-overlap.md:11,13,23,25` — all fleet sibling-overlap/route-telemetry/ledger-absence notes that name kasegi as owner.
**bounty — kotoba:** `corpus/knowledge/sibling-description-rewrites-round8.md:259–326,376,418–444`; `sibling-citation-routing-round16.json:500,637,651,1905,1906,2744,2750,2757,2758`; `sibling-citation-routing-round16.md:102`; `sibling-overlap-census-round49.md:77`; `sibling-overlap-census-round74.md:61,92`; `lessons/round-16.md:22,25`; `lessons/round-49-verifier-spotcheck.md:171` — kotoba audits kasegi's SKILL.md description; routing/census text only.
**bounty — kotodama:** `corpus/knowledge/civilizations/arabia-pre-islamic.md:137` — Qur'an 2:198 "seeking bounty" (trade); unrelated.
**bounty — kumitate:** `corpus/knowledge/ops-watchers.md:30` ("Refires stale bounty-hunt UFOs and steers under-filled missions").
**bounty — tabi:** `corpus/knowledge/csrf-defense-shape-boundary.md:19` ("fleet roster's bounty/security-research lane"; the entry's own scope line records provenance).

Top-level docs (PROVINCE/README/AGENTS/MINT/SHONEN/SKILL), bounty only, all pointers to kasegi: `chousa PROVINCE.md:10, README.md:6, MINT.md:14,22,27, SKILL.md:3,10,57,152`; `kake PROVINCE.md:285`; `kama MINT.md:38`; `kengaku PROVINCE.md:29,74,79,142,159`; `kotoba PROVINCE.md:64`. No sibling PROVINCE/SKILL carries Immunefi, VSCS, severity classification, smart contract, Web3 or blockchain.

**considerthese dirs** (16 siblings have one — audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama, kengaku, kotoba, kumitate, lore, mado, mori, revenger, tameshi, tsukuroi; kaidoku, kotodama, souji, tabi have none; kasegi excluded): **0 hits** on all seven tokens.

## 4. Adjacent but not contested: EVM bytecode (kaidoku, revenger)

Not in the assigned token list; reported because a connector could ask "who else speaks about smart contracts".
- `kaidoku-shokunin/PROVINCE.md:54` (Core row `inspect-evm-interface`), `:91` ("EVM bytecode (extended)" Frontier, selector-name resolution rounds 25/28/29), `:318`; `kaidoku-shokunin/SKILL.md:54,78,286,301`. Byte/selector recovery with REA; no severity, bounty-program or claim wording (token sweep: 0 for Immunefi/VSCS/severity classification/smart.contract/Web3/blockchain in kaidoku corpus+SKILL).
- `revenger-shokunin/.ufo/waves/round-61/build/ConnectorKasegiEvm.md` (sha256 `f844dbb6a161616fd9e536773256b4250d9fe67f5fffe068c085f14344240551`, `:11`): prior fleet ruling "No method overlap; one real ground overlap, at a single proposition … kasegi owns the *claim/package* layer, revenger C09 would own the *byte-offset* layer"; `:44` "Deployed-bytecode identity versus source pins, program scope and claimability are kasegi-shokunin's ground"; verdict `:66`: byte-scoped, "report both counter-examples to kasegi and never cite kasegi for a byte claim". It also records kasegi's own smart-contract hits (`target-checkouts.md:54`, `intake-surface.md:22`, `claim-anatomy-sample.md:44`) as claim-layer. This is prior-art ruling in the same direction as F17.
- `revenger-shokunin/reports/round-62/claims.md:75` ("REA producers, blockchain calls, intrusive reproduction or offensive workflows" — an exclusion clause, i.e. revenger refuses blockchain calls).
- Prior fleet scan of the same ground: `kaidoku-shokunin/.ufo/waves/round-25/a2/w1-spec.json:170` ("Sibling-overlap scan for EVM and smart-contract ground … whether kaidoku's C2 would absorb contested scope"); its result artifact is not on disk (only `swarm-registry.json` in `w1/`), so no ruling to cite from it.
- Wide (`-uu`, `.ufo`/scratch included) sweep hits for the six non-bounty tokens, all non-ground: kaidoku `.ufo/waves/arc3-loop1-round1/seats/RV-1.md:105` (`web3`/`ethers` missing-package note), `…round7/claims/c2/EX-4|EX-5/evidence/vyper-help.txt:11` ("Pythonic Smart Contract Language for the EVM", tool help text), `round-25/a2/w1-spec.json:90,170`; mori `.scratch/r48-ScoutQuarantineS262/roma.txt:1379,1381`, `…S268/roma_ua.txt:1379,1381` (paper-text noise "blockchain technology"); kotoba `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:523413,1320853,1320854` (string dump of the OMP binary); revenger `reports/round-62/claims.md:75`, `.ufo/waves/round-61/build/ConnectorKasegiEvm.md:11,13`, `…/build-spec.json:9`, `…/build-dispatch.json:725` (copies of the above prompts), `.ufo/waves/round-62/build-spec.json:8`; kama `.ufo/waves/round-36/w3/out/RevQualBytes/seat.log:372` ("Severity classification:" — one line inside a tool log, not a corpus entry; not read further); `VSCS`/`vscs` case-insensitive hits elsewhere (kaidoku patches, kake `…S074.txt` / `round-41/…json` / `round-42/…py`, kotodama chronicle text "Vscslav", mado `round-26/controls/K2LabelKeyed.py`, tabi strace `tmp_obj_VScsuw`, tsukuroi `round-33/a3w1/R2MutHomeTz/m3.jsonl:5`) are **false positives** from base64/hash/name substrings; with `\bVSCS\b` the whole-lane sweep of tameshi and tsukuroi returned only the tsukuroi base64 line. Also kake `.ufo/waves/round-34/sources/S074.txt:1` (Telegram Bot API page text) matched the case-insensitive token by substring only.
  - Caveat: the wide sweep's per-lane output was capped at 15 lines for earlier-alphabet lanes (`head -15`); the corpus/SKILL.md scoped counts in §2 are uncapped and authoritative.

## 5. Adjacent but not contested: kake `security.txt` publishing

`kake-shokunin/PROVINCE.md:202–292` (round-35 "security.txt publishing frontier step"; `corpus/knowledge/security-txt-publishing.md`; RFC 9116, S078–S085). Subject is serving a vulnerability-reporting pointer from a Pages site. Explicit boundary at `PROVINCE.md:284–286`: "Vulnerability handling itself stays out of province: report intake, triage, remediation, disclosure timing, bounty and policy operation, and whether any named contact channel works, are not kake's ground". Mirrored at `kake-shokunin/corpus/README.md:465–467`. Severity classification is "triage" — kake disclaims it. No Immunefi/VSCS/severity-classification/smart-contract tokens in kake.

## 6. Fleet root (read-only)

- Files swept: `AGENTS.md AXES.md CORPUS.md LEARNING.md LOG.md MANIFEST.json MISSION.md PROTOCOL-APPENDIX.md PROTOCOL.md README.md ROADMAP.md SCORECARD.md shokunin.conf`, dirs `research/ templates/ scripts/`, and `.ufo/{scopes,prompts,state,gates}` + `.ufo/l0-questions.md`.
- Seven tokens: only `bounty` hits, all roster/scope declarations: `MANIFEST.json:9` (`"domain": "bounty & security research"` for kasegi), `MANIFEST.json:2314` (chousa admission note: "kasegi does program-specific bounty research only"), `MANIFEST.json:4430` (chousa r12 note, SCOPE_BOUNTY_ABSORBED), `MISSION.md:23` (`kasegi: … "depth + coverage (bounty/security research)"`), `README.md:112`, `ROADMAP.md:7`, `shokunin.conf:46` (`kasegi|kasegi-shokunin|depth + coverage (bounty and security research)`). `Immunefi`, `VSCS`, `severity classification`, `smart contract`, `Web3`, `blockchain` → **0 hits** in all of the above (the `.ufo/prompts|scopes|state|gates|l0-questions.md` rg returned no lines; the shell wrapper emitted a "temporary shell" notice for that call, so its empty result is recorded as "no lines emitted", re-confirmed by the MANIFEST/MISSION/README/ROADMAP/shokunin.conf results above, which print their hits normally).
- No fleet-root `considerthese/` or `merge` theme directory exists (`ls` of root shows none; `find . -maxdepth 3 -iname '*merge*'` found only per-lane `.git/MERGE_RR`/`AUTO_MERGE` git internals and `souji-shokunin/tools/cand-merge-selftest.sh`, a candidate-merge self-test unrelated to these tokens). Per-lane `*/considerthese/` dirs (16, kasegi excluded) → 0 hits on all seven tokens, including `bounty`.
- Lane domain lines (`sed -n 3p */PROVINCE.md`): only kasegi declares "bounty & security research"; kagi = secrets & vault ops, kake = web properties & publishing, tabi = browser & web-interaction craft, kaidoku/revenger = reverse engineering, chousa = deep-research method; none declares security triage, severity, smart contracts or bounty severity.

## 7. Open items / limits

- `rg` honours `.gitignore` in the scoped counts (§2); the whole-lane `-uu` pass in §4 disables ignore filters, so a hit hidden by `.gitignore` in `corpus/` would have shown there; none did beyond those listed.
- Sibling lanes carrying uncommitted or unpushed work at sweep time were read as on disk (working copy), not at a pinned rev; sibling HEADs are not recorded here.
- kaidoku round-25 scan result artifact (for the same type of question) is absent on disk — only the prompt survives; flagged, not inferred.
- The connector's contested-scope ruling is the connector's; evidence above supports "uncontested; kasegi-owned".

## Report

Commands run: the `rg` pipelines above (exit 0 for every counting run; `rg` returned exit 2 only for deliberate glob expansions over non-lane root files, e.g. `AGENTS.md/PROVINCE.md: Not a directory`, which were noise from `*/PROVINCE.md` globs hitting root files and `154.0.8037.97`/`156.0.8078.47`/`ok`/`research`/`scripts`/`templates` directories — the results for real lanes are unaffected).
Digests (sha256) of cited sibling/fleet files at sweep time:
- `kaidoku-shokunin/PROVINCE.md` `ecfa491fa315047a6797bd660b239f29e5e1d9c548e38e943e398a9eb0a8d242`
- `kotoba-shokunin/corpus/knowledge/sibling-citation-routing-round16.json` `6674dca126e5be915f759b32005600788337de0ad470fa26473814d0bf408882`
- `kasegi-shokunin/SKILL.md` `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`
- `revenger-shokunin/.ufo/waves/round-61/build/ConnectorKasegiEvm.md` `f844dbb6a161616fd9e536773256b4250d9fe67f5fffe068c085f14344240551`
- `MANIFEST.json` (fleet root) `33ab3ce11e3fa1b5aaadbd6a0d21b20a87dd82c8c522aa7db33f3cf0fe9b257c`
Scratch: none created; none left on disk. Installs: none. Writes: this file only.
