# ExecRegistryAppend — kasegi-shokunin round 34 (wave 1)

Seat: `ExecRegistryAppend` (executor, leaf). Scope: append the S051 registry row, the round-34 Immunefi
`## Search log` bullet and the `## Registry changes` R8 lines to `corpus/SOURCES.md`, exactly per the
ScribeSOURCESRow draft, then verify the census. No other file was written; no git/jj mutation was run; the
fleet repo, sibling lanes, `/home/vgpnk/Projects/bounties` and `/home/vgpnk/Projects/shokuknow` were never
written.

## Report

### 1. Inputs and their digests (all read-only)

```
$ sha256sum .ufo/waves/round-34/wave1/ScribeSOURCESRow.md
94deb84a4507ced156d2e3e78c1dc1e1f8f5b4907b4ffba6e8f6cb3b3d8d5b1d  .ufo/waves/round-34/wave1/ScribeSOURCESRow.md
   (16874 B; the scribe's declared FINAL revision, messaged at 02:37)
$ sha256sum corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
   175 lines, 8502 B
$ sha256sum corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
e71fbcd985379fdd54cd2b65da5fd2eaebc5b29119f022a4915e66e827849ea7  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
   113 lines, 11206 B; line 6 selects `--source S051` against corpus/source-snapshots/round-34/manifest.json
$ sha256sum corpus/source-snapshots/round-34/manifest.json   (18 assertions Q1-Q18, record id S051,
   url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/, fetched_utc
   2026-10-26T05:31:10Z)
```

Pre-append `corpus/SOURCES.md` at the lane base `014ee2d` (`git show 014ee2d7:corpus/SOURCES.md` copied to
scratch), digest `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b` — byte-identical to the
digest ScribeSearchLog recorded, so the file was untouched between its measurement and my append.

### 2. Pre-append baseline (measured before any write)

```
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 50
```

Negative-sweep reproduction over the 45-file pre-entry tree (verifying the bullet's own numbers before
landing them):

```
Immunefi | knowledge_files=6 README=2 SKILL=2 SOURCES=0
VSCS | knowledge_files=0 … ; smart contract | 0 ; smart-contract | 2 ; web3 | 6 (SKILL 1)
blockchain | 0 ; Solidity | 0 ; bug bounty | 2 (SOURCES 1)
```

### 3. Applied blocks — verbatim, byte-identical

Three guarded edits, each diffed against the draft's own fenced bytes after writing:

```
$ awk 'NR==57' corpus/SOURCES.md > landed_row.txt
$ cmp -s row.txt landed_row.txt ; echo cmp_exit=$?
cmp_exit=0
$ awk 'NR==77' corpus/SOURCES.md > landed_bullet.txt
$ cmp -s searchlog.txt landed_bullet.txt ; echo cmp_exit=$?
cmp_exit=0
$ awk 'NR>=103 && NR<=105' corpus/SOURCES.md > landed_r8.txt
$ cmp -s r8.txt landed_r8.txt ; echo cmp_exit=$?
cmp_exit=0
```

`row.txt` / `searchlog.txt` / `r8.txt` were extracted from the draft with
`re.findall(r"```\n(.*?)\n```", draft)` (blocks 1-3 of 7; blocks 4-7 are the scribe's command/evidence
examples). Landed positions:

- `corpus/SOURCES.md:57` — registry row, immediately after `S050` (now :56) and before the blank line at
  :58 / `## Paths` (:59).
- `corpus/SOURCES.md:77` — Search-log bullet, immediately after the round-33 CN bullet (:76) and before the
  blank line at :78 / `## Leads (unopened)` (:79).
- `corpus/SOURCES.md:103-105` — the three R8 bullets, after the round-33 tally line (:102, the former :100).

Landed row (one physical line, `|` field count 13):

```
| S051 | Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ | docs | A | Immunefi's own Web3 severity classification system v2.2 as this page states it: the five levels Critical to None and the impact bullets each level lists for the Smart Contracts table, which is this row's subject | capture corpus/source-snapshots/round-34/S051.txt (sha256 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5, 175 lines): H1 L45 names v2.2; L46 the five-level sentence; L52 the factors-versus-impact sentence; L53-L56 the consequence-of-a-successful-exploit paragraph with the downgrade-or-reject caveat; L72 Smart Contracts heading; L73 LevelImpact; L74-L83 Critical bullets (direct theft of user funds and of NFTs, permanent freezing of funds and of NFTs, miner-extractable value, unauthorised NFT minting, predictable RNG, unintended NFT-representation alteration, protocol insolvency); L84-L89 High; L90-L94 Medium; L95 Low; L96 None | Immunefi's VSCS v2.2 places Web3 bugs on a five-level scale, decides the level mainly by the impact a successful exploit causes, and may downgrade or reject that level when exploiting it needs elevated privileges or uncommon user interaction, so read the Smart Contracts bullets as v2.2's impact vocabulary rather than as CVSS scores, a program's payout ladder or an authorisation to test | mined | 2026-10-26 | 90d | corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md |
```

Landed Search-log bullet: `corpus/SOURCES.md:77`, 2656 B, PRISMA-shaped in one physical line — `question:`
the lane holds no Web3/smart-contract severity-classification source and v2.2 adds impact-level ground the
F13/F16 ladders do not; `where:` Immunefi's severity-classification index and every version page it lists,
v2.2 captured under the instrument UA into `corpus/source-snapshots/round-34/S051.txt` (status 200, 8502 B,
175 lines, sha256 `4fd8ed98…b325a5`), v2.3 opened alongside; an eight-term negative sweep (Immunefi, VSCS,
"smart contract", "smart-contract", web3, blockchain, Solidity, "bug bounty") over `corpus/knowledge/*.md`
(45 files, PRE-STATE; 46 after), `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`; `date: 2026-10-26`;
`identified 8, screened 3 …, included 1 (v2.2 → S051), excluded 7` with the index/v2.3 exclusion reasons,
the 404 bare-slug probe and the unscreened Help Desk explainer named, and a stop rationale (Immunefi's own
index closes the version set).

Landed R8 lines: `corpus/SOURCES.md:103` S051 row-added entry (kind/tier/scope/status/opened/recheck/used-by,
anchor pinned to the round-34 capture with sha256 and L45-L96 locators, live-capture admission because the
`immunefi`/`vscs` grep over the campaign package returns no files); `:104` the no-recency-claim statement
(v2.3 and v2.2 both Currently in Use in the index fetch, carried as a recheck item, no cell claim resting on
it); `:105` `No status/recheck/used-by cell changed on any pre-existing row; S001–S050 untouched (logged).
Registry 50 rows pre-append → 51 post-append (R8).`

### 4. Mandated verification (post-append)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
51
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md
1
$ ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi ; echo census_exit=$?
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Malformed rows counted independently of the script (every `|`-leading line inside `## Registry` must split
into 13 fields):

```
registry_lines=53 malformed=0 []
   (53 = header + separator + 51 rows; no E01 in the census output either)
```

Row-shape checker over the landed bytes (stdlib-only; run from scratch, deleted with it):

```
registry_rows=51
S051 line=57 NF=13
url: https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/
PASS row-shape        check_exit=0
```

It asserts: 11 non-empty cells; id `S051`; https URL present; kind in {docs,spec,dataset,paper,community};
tier in {A,B,C} and not community-at-A; status in {queued,mined,rejected}; opened `2026-10-26` ISO;
recheck `90d`; used-by `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` present on disk
(census E11); anchor names `round-34/S051.txt` with `L` locators; no duplicated row bytes.

Files changed: `corpus/SOURCES.md` only. Post-append digest and shape:

```
$ sha256sum corpus/SOURCES.md
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
$ wc -lc corpus/SOURCES.md
105 58561 corpus/SOURCES.md
$ diff base_SOURCES.md corpus/SOURCES.md | cut -c1-90
56a57   > | S051 | Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi
75a77   > - Immunefi severity-classification sweep (round 34); question: does the lane already hol
100a103,105 > - S051 row added: … / > - S051 scope recorded without a recency claim: … /
             > - No status/recheck/used-by cell changed on any pre-existing row; S001–S050 untouched …
```

Five added lines, zero deletions, zero in-place modifications: no pre-existing row cell was touched (R8).

### 5. Read-only cross-evidence for the L1 (not my claim to make)

My row is what `capture-binding-check.py` rule B binds the round-34 record to, so I ran both instruments
after the append:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1..Q18 OK  (each occurrences=1 or anchor-ok; Q2/Q5/Q6 normalized=markup-whitespace; Q9/Q17 occurrences=2 anchored)
sourcerecheck_exit=0
$ python3 corpus/instruments/capture-binding-check.py
… MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10
      missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
binding_exit=0
```

Context at the same moment (other seats' writes, reported not claimed): `corpus/README.md` frontier rows = 17,
`corpus/knowledge/*.md` = 46, `corpus/source-snapshots/round-34/` holds `S051.txt` + `manifest.json`.

### 6. Findings

1. **Draft revision history (the count defect was closed before landing, not by me).** The first draft I
   extracted (sha256 `9f485e62…`, 2125 B bullet) said "nine-term negative sweep" while enumerating seven
   terms and measuring eight in its own §4 table. I refused to invent a ninth term and asked the scribe to
   settle it; it revised (`923441a8…`, still nine-term, PRISMA 1/1/1/0) and then froze at `94deb84a…` with
   **eight-term**, the terms enumerated inline, and PRISMA `8/3/1/7` reconciled with ScribeSearchLog. The
   landed bytes carry the corrected text; my only edits were insertions of that text.
2. **Draft pipe claim — correction, and where my earlier note applied.** The superseded 9175 B revision
   (`923441a8…`) claimed the R8 block carried 0 `|`; the **frozen** draft (`94deb84a…`) already corrected it:
   `.ufo/waves/round-34/wave1/ScribeSOURCESRow.md:64` reads "Search-log line 0; R8 block 1, the escaped `\|`
   inside the backticked `immunefi\|vscs` grep pattern (prose, outside the registry table; census E12 fires
   only on row-shaped lines)", which matches my own measurement (landed R8 bullet 1, one escaped `\|`). The
   scribe's freeze note (artifact line 11) records the same. So the correction was the author's, made before
   the freeze; my note to that effect applied only to the revision I had first read, and the landed bytes are
   consistent with the frozen draft's own claim.
3. **Anchor locators verified line by line against the committed capture**, not against the manifest text:
   L45 `… System - v2.2`, L46 five-level sentence, L52 factors-versus-impact, L53-L56 consequence paragraph,
   L72 `Smart Contracts`, L73 `LevelImpact`, L74-L83 Critical (L83 `Protocol insolvency`), L84-L89 High
   (L89 `Temporary freezing NFTs`), L90-L94 Medium, L95 Low, L96 None. `source-recheck` confirms all 18
   assertions (exit 0).
4. **Ordering constraint worth recording:** capture-binding rule B requires the manifest record's id to name
   a registry row, so the round-34 manifest could not bind until this row landed. Post-append
   `round-34 records=1 url_bound=1` is the observable close of that dependency.
5. **No other row touched.** S001–S050 byte-identical to the base blob (diff shows five insertions only).

### 7. Limits

- I did not fetch the Immunefi pages myself; the bullet's `where:` facts (status 200, 8 502 B, 175 lines,
  the eight version pages, v2.3's four-level scale) are ScribeSearchLog/ScribeSOURCESRow measurements, and I
  reproduced only the lane-side sweep counts and the capture digests.
- The row's anchor cell asserts nothing about other Immunefi systems and no recency claim; v2.3 is present
  only as an observation with no committed capture, per the R8 line at `:104`.
- Census was run at `--root /home/vgpnk/Projects/shokunin` with the single lane argument `kasegi`, as the
  assignment specifies; I did not run the fleet-wide census.

### 8. Scratch, tooling, cleanliness

Scratch `/fast/scratch/hyaku/kasegi-r34/ExecRegistryAppend/` held `scribe-spec.txt`, the extracted
`row.txt` / `searchlog.txt` / `r8.txt`, the landed copies, `base_SOURCES.md` and `check_row.py`; it was
deleted with `rm -rf` after these numbers were transcribed (verification of removal is in the transcript
line that follows the receipt write). No tools were installed or upgraded (no pacman, no uv, no npx); only
host `bash`, `grep`, `awk`, `diff`, `cmp`, `sha256sum`, `git show` (read-only) and `python3` stdlib.
