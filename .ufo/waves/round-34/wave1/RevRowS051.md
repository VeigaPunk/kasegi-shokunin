# RevRowS051 — round-34 review of the S051 registry row, Search-log bullet and R8 lines

Seat: RevRowS051 (reviewer, L2 leaf, kasegi-shokunin round 34, hyaku run 8). Item: review the landed
S051 registry row in `corpus/SOURCES.md` (11 columns/NF=13; no `|` inside cells; tier A scoped to
Immunefi's own VSCS v2.2 statements; anchor pinned to the round-34 capture with line locators; quote
≤25 words located in the capture; `opened 2026-10-26`; `recheck 90d`; `used-by` exactly the F17
entry; kind docs; status mined) and confirm the round-34 `## Search log` bullet and
`## Registry changes` R8 lines are present and truthful.

## Verdict: **matches**

Every criterion holds on the landed bytes (`corpus/SOURCES.md` sha256 `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6`,
105 lines / 58 561 B). Two prose-only observations for the L1 (§ Findings), neither a corpus defect.

## Report

### 0. Timing (why the review ran late)

At first check `corpus/SOURCES.md` was still the round-33 tree (50 rows, sha256 `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`,
100 lines, `S051_rows=0`): the S051 append had not landed. I messaged `ExecRegistryAppend` (turned
out to be the parked round-33 seat — its S049/S050 append is committed and out of my scope) and then
`ExecRegistryAppend-2`, who confirmed ownership of the round-34 S051 append and pinged me at landing.
All capture-side, manifest-side and draft-truthfulness checks below were run **before** the landing;
the row checks were run **after** it, on the landed bytes.

### 1. The landed row — `corpus/SOURCES.md:57` (verbatim, one physical line)

```
| S051 | Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ | docs | A | Immunefi's own Web3 severity classification system v2.2 as this page states it: the five levels Critical to None and the impact bullets each level lists for the Smart Contracts table, which is this row's subject | capture corpus/source-snapshots/round-34/S051.txt (sha256 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5, 175 lines): H1 L45 names v2.2; L46 the five-level sentence; L52 the factors-versus-impact sentence; L53-L56 the consequence-of-a-successful-exploit paragraph with the downgrade-or-reject caveat; L72 Smart Contracts heading; L73 LevelImpact; L74-L83 Critical bullets (direct theft of user funds and of NFTs, permanent freezing of funds and of NFTs, miner-extractable value, unauthorised NFT minting, predictable RNG, unintended NFT-representation alteration, protocol insolvency); L84-L89 High; L90-L94 Medium; L95 Low; L96 None | Immunefi's VSCS v2.2 places Web3 bugs on a five-level scale, decides the level mainly by the impact a successful exploit causes, and may downgrade or reject that level when exploiting it needs elevated privileges or uncommon user interaction, so read the Smart Contracts bullets as v2.2's impact vocabulary rather than as CVSS scores, a program's payout ladder or an authorisation to test | mined | 2026-10-26 | 90d | corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md |
```

Per-criterion verdicts:

| criterion | landed evidence | verdict |
|---|---|---|
| 11 columns / NF=13 | `sed -n '57p' \| awk -F'\|'` → `NF=13`, `row_pipes=12`; header row `:5` also `NF=13` (11 columns: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by); cells 01–11 all non-empty | **matches** |
| no `\|` inside cells | NF=13 with 11 cells ⟺ 12 boundary pipes; whole-file `grep -cF '\|' corpus/SOURCES.md` → `0` | **matches** |
| tier A scoped to Immunefi's own VSCS v2.2 statements | cell04 `A`; cell05 opens "Immunefi's own Web3 severity classification system v2.2 as this page states it" and bounds the row to the Smart Contracts table ("which is this row's subject") — Q4 attribution kept, no generalization | **matches** |
| anchor pinned to the round-34 capture with line locators | cell06 pins `corpus/source-snapshots/round-34/S051.txt` with its sha256 and 175-line count, then L45/L46/L52/L53-L56/L72/L73/L74-L83/L84-L89/L90-L94/L95/L96 — every locator re-opened against the capture (§2) | **matches** |
| quote ≤25 words located in the capture | the row files no verbatim quote (lane row shape — S049/S050 rows carry none either); the round's S051 quotes of record are manifest Q1–Q18 (max 20 words; 16 exactly-once, Q9/Q17 `occurrences=2` with anchors 77/96 per QUALITY Q9) and the entry's capture quotes; the gate quote of record is Q8 "Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield" — 14 words, `S051.txt:75`, exactly-once, also live-verified by `wave1/ScoutImmunefiLive.md` (live grep 1 / snapshot grep 1) | **matches** |
| `opened 2026-10-26` | cell09 | **matches** |
| `recheck 90d` | cell10 (cadence form, same as S006/S007/S043/S044/S045/S047/S049) | **matches** |
| `used-by` exactly the F17 entry | cell11 is the single path `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`; the entry exists (113 lines, sha256 `948b202e…c1d8a`) and its `:3` reads `source: S051 — https://immunefi.com/…`; `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` → `1` | **matches** |
| kind docs | cell03 `docs` | **matches** |
| status mined | cell08 `mined` | **matches** |

Row position: `:56` S050, `:57` S051, `:58` blank, `:59` `## Paths` — last row of the `## Registry`
table, exactly the draft's apply point 1.

### 2. Anchor locators re-opened against the capture

Capture `corpus/source-snapshots/round-34/S051.txt`, 175 lines / 8 502 B, sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`.
Independently re-fetched live with the lane instrument before the row landed:

```
$ python3 corpus/instruments/capture-source.py --id S051 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ --out $S/S051-live-recheck.txt
S051 status=200 fetched_bytes=219383 snapshot_bytes=8502 sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 utc=2026-10-26T05:33:38Z   (exit 0)
$ diff corpus/source-snapshots/round-34/S051.txt $S/S051-live-recheck.txt && echo DIFF_IDENTICAL
DIFF_IDENTICAL   (exit 0)
```

Locator map verified line-by-line (`awk 'NR>=45 && NR<=56'`, `NR>=72 && NR<=96` on the capture):

- L45 H1 `Immunefi Vulnerability Severity Classification System - v2.2` — "names v2.2" ✓
- L46 `At Immunefi, we classify bugs on a simplified 5-level scale:` ✓; L47–51 the five level names ✓
- L52 the factors-versus-impact sentence ✓; L53–L56 the consequence paragraph ending "…downgraded to reflect that or rejected." ✓ (wraps L53→L54, L55→L56)
- L72 `Smart Contracts` heading ✓; L73 `LevelImpact` ✓
- L74 `5. Critical- Any governance voting result manipulation`; L75 the funds-theft bullet; L76 NFT-theft; L77–L78 permanent freezing (funds/NFTs); L79 MEV; L80 unauthorized minting; L81 predictable RNG; L82 NFT-representation alteration; L83 `Protocol insolvency` — the anchor cell's parenthetical paraphrases each ✓ (its "unauthorised NFT minting" is a paraphrase of L80's "Unauthorized minting of NFTs", a description, not a quote)
- L84 `4. High- Theft of unclaimed yield` + L85–L89 bullets ✓; L90 `3. Medium- …` + L91–L94 ✓; L95 `2. Low- …` ✓; L96 `1. None- Best practices` ✓

Teaches-cell negatives grounded: `grep -icF CVSS` → 0; payout/dollar-amount grep → 0; the only
`authoriz|Safe Harbor` tokens are the product-nav item (L16, L37) and the impact label "Unauthorized
minting" (L80) — no authorization-to-test statement exists in the capture ✓.

### 3. Manifest and recheck (the row's captured-source binding)

`corpus/source-snapshots/round-34/manifest.json` sha256 `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`
(final revision after the entry author objected to converter-joined spans; the earlier `3e726d84…`
version was superseded mid-wave). Record: id `S051`, path `S051.txt`, sha256 = the capture's sha256,
`url` byte-equal to the row's source-cell URL token, `fetched_utc 2026-10-26T05:31:10Z` (strict UTC,
no offset — R20/R21 conformant).

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok          (… Q2–Q8, Q10–Q16, Q18 occurrences=1 …)
S051:Q9 OK occurrences=2 anchor=77-ok
S051:Q17 OK occurrences=2 anchor=96-ok
recheck_exit=0
```

My own independent check (not the instrument): every quote ≤25 words (max 20, Q3), every quote
exactly-once under the declared markup-whitespace normalization except Q9/Q17 (2×, each with a
verified anchor line holding the quote head), Q2 (five level names, L47–L51) carries no anchor and
relies on normalized uniqueness — the manifest's `purpose` declares exactly that exception. 18/18.

```
$ python3 corpus/instruments/capture-binding-check.py   (tail)
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
binding_exit=0
```

The pre-landing `FAIL rule=no-row record=S051` cleared when the row landed. `orphans=1
orphan=S040-live.txt` is the known round-33 R6 item (ExecS040Orphan's lane, not mine).

### 4. Search-log bullet — `corpus/SOURCES.md:77` — present and truthful

Present: one bullet appended as the last `## Search log` bullet (section now `:66`, bullet `:77`),
byte-identical to the final scribe draft (`cmp` draft:41 ↔ sources:77 → exit 0). PRISMA fields all
present (question / where / date 2026-10-26 / identified 8, screened 3, included 1, excluded 7 / stop
rationale). Truthfulness, each load-bearing claim re-verified by me:

- **identified 8**: my own fetch of the live index HTML (`https://immunefi.com/severity-classification-systems/`, 149 274 B) → exactly 7 version links + the index: Currently in Use v2.3, v2.2; Being Phased Out v2.1, v2, **v1.2** (anchor text "…System v1.2", slug `severity-system-comprehensive`), "Updated" (`severity-updated`), plain (`severity-system`). The bullet's "files v2.1, v2, v1.2, the 'Updated' system and the plain system" names them by document title — truthful. Arithmetic 1+7=8 ✓.
- **screened 3 / excluded 7**: index + v2.2 + v2.3 read in full; five version pages title-screened; 3+5=8 ✓.
- **"the v2.3 page states a four-level scale"**: my own v2.3 re-fetch → L46 `At Immunefi, we classify bugs on a simplified 4-level scale:` ✓.
- **"the index itself carries no level or impact"**: index text `Critical`=0; the only level/impact words are the Rewards-by-Threat-Level pointer (L48) and the Help Desk explainer pointer (L58–59) — which the bullet itself discloses as "deliberately left unscreened" ✓.
- **"a guessed bare-slug URL (…-system/) returned 404"**: my own curl with the instrument UA → `bare_slug_http=404` ✓.
- **eight-term negative sweep**: my own POST-STATE re-run reproduces the scribe's numbers exactly — Immunefi 7 knowledge files / 2 README lines / 2 SKILL lines; VSCS 1; "smart contract" 1; "smart-contract" 3; web3 7; blockchain 1; Solidity 0; "bug bounty" 2; knowledge files 45 → 46 after the F17 entry ✓. The bullet labels its knowledge counts PRE-STATE and states the 46-after figure — honest.
- **capture stats in the bullet** (status 200, 8502 bytes, 175 lines, sha256 `4fd8ed98…b325a5`): all verified by my own live re-fetch (byte-identical) ✓.
- **"2 README lines in the lost-tree note"**: the two README Immunefi lines are `:175`/`:177`, inside the Known-gaps bullet about lost-tree artifacts (`portal-reconciliation-2026-09-11.json`/`final-audit.json`, keeper `html_sha256` telemetry) — characterization fair ✓.

### 5. Registry-changes R8 lines — `corpus/SOURCES.md:103-105` — present and truthful

Present: three bullets appended at file end (section now `:85`, lines `:103`–`:105`), byte-identical
to the final scribe draft (`cmp` draft:49/50/51 ↔ sources:103/104/105 → exit 0 each). Truthfulness:

- **":103 S051 row added…"** — every cell it names matches the landed row (id/kind/tier/scope
  summary/status/opened/recheck/used-by; anchor digest + the same locator list I verified in §2) ✓.
- **":103 Live-capture admission, not a staged row: an `immunefi`/`vscs` grep over
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/` returns no files"** — my own read-only grep → `0`
  files (exit 0) ✓. No staged row, no staged-cell rewrite — consistent with the shokuknow package.
- **":104 no cell says `latest` or `current`"** — `sed -n '57p' | grep -icF latest` → 0 and
  `… current` → 0 ✓; the no-recency-claim scoping (v2.3 and v2.2 both "Currently in Use" per the
  index; v2.3 four-level) matches my own index/v2.3 reads ✓.
- **":105 No status/recheck/used-by cell changed on any pre-existing row; S001–S050 untouched
  (logged). Registry 50 rows pre-append → 51 post-append (R8)."** — `git diff HEAD --numstat --
  corpus/SOURCES.md` → `5 0`; the five insertions are exactly the row + bullet + three R8 lines;
  deletions `grep -c '^-[^-]'` → 0. My pre-append baseline (measured before the landing):
  `S_rows=50`, sha256 `b22c7f01…4d13b`; post: `S_rows=51`, `S051_rows=1`, sha256 `4c85ff86…77b6`.
  Zero pre-existing lines touched at all — stronger than the claim ✓. "(R8)" is the QUALITY record-R8
  logging criterion (`corpus/QUALITY.md:50`), not the round-33 verifier defect R8.

### 6. Landed-tree cross-checks (claims C2 counters, read-only)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        → 51
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md              → 1
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                  → 17
$ grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l                     → 1
$ python3 corpus/instruments/frontier-recheck-count.py   (tail)
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0                                              (harness_exit=0)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0        (identical before and after the append; no new W, no E line)
```

README F17 row `:361` (section "## Round-34 admission … (appended 2026-10-26)" at `:344`) names the
same entry path and `S051`; its four capture cites (`S051.txt:52`, `:55-56`, `:75`, `:88`) all
verified in the capture ✓.

### 7. Findings for the L1 (none a corpus defect)

1. **Scribe-receipt prose defect (prose-only, census-neutral).** The final draft
   `.ufo/waves/round-34/wave1/ScribeSOURCESRow.md` (sha256 `94deb84a…d5b1d`) §4 check-table still
   claims "R8 block 1, the escaped `\|` inside the backticked `immunefi\|vscs` grep pattern", but the
   landed R8 block — and the whole landed `corpus/SOURCES.md` — contains no `\|` anywhere
   (`grep -cF '\|' corpus/SOURCES.md` → `0`); the R8 line says "an `immunefi`/`vscs` grep" in prose
   with no command. `ExecRegistryAppend`'s receipt flags the same. Class: stale receipt-internal
   claim (M33-4-adjacent); no corpus byte affected; the landed blocks are clean.
2. **Anchor drift, M33-3 class, recurring (routed to lessons, not this row's defect).** The 5-line
   append moves `## Paths` 58→59, `## Search log` 65→66, `## Leads` 77→79, `## Registry changes`
   83→85; the stale `SOURCES.md:83` citation trail (`corpus/lessons/round-29.md:214`,
   `round-29-verifier-spotcheck.md:74`, already +7) deepens by +2.
3. **Residual gap outside my row scope:** the round-34 lesson (which will file the S051 Gate quote)
   had not landed at my check time (`ls corpus/lessons/ | grep round-34` → none). The ≤25-word quote
   of record is verified at manifest Q8 + entry level; the lesson Gate quote should be checked when
   `ScribeLesson` lands (expected: Q8's 14-word funds-theft sentence at `S051.txt:75`).

### 8. File digests (measured this seat)

```
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md                 (105 lines / 58561 B; pre-append b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b, 100 lines)
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt   (175 lines / 8502 B; live re-fetch byte-identical)
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md  (113 lines)
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
94deb84a4507ced156d2e3e78c1dc1e1f8f5b4907b4ffba6e8f6cb3b3d8d5b1d  .ufo/waves/round-34/wave1/ScribeSOURCESRow.md  (landed blocks byte-identical: cmp draft:32/41/49/50/51 ↔ sources:57/77/103/104/105, all exit 0)
```

### 9. Tooling and scratch

- No tool installed or upgraded (no `pacman`, `uv`, `npx`, or binary fetch); only lane instruments,
  `curl`, `python3`, coreutils.
- Scratch `/fast/scratch/hyaku/kasegi-r34/RevRowS051/` (census-before.txt, census-after.txt,
  S051-live-recheck.txt, IDX.txt, V23.txt, idx.html) — deleted before yielding; receipt first copied
  into the wave dir. Scratch-left-on-disk: **none**.
- Write scope respected: only this receipt under `.ufo/waves/round-34/wave1/`; no jj/git mutations;
  shokuknow and the fleet root read-only (one read-only grep over `shokuknow/merge/kasegi/`).
