# ScribeSOURCESRow — round-34 SOURCES.md draft (S051 row, Search-log bullet, R8 lines)

Seat: ScribeSOURCESRow (L2 leaf, kasegi-shokunin round 34). Draft only: the L1 commits, ExecRegistryAppend
applies. Every byte below is measured against the landed capture
`corpus/source-snapshots/round-34/S051.txt` (sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`,
8 502 bytes, 175 lines) and against `corpus/SOURCES.md` at draft time (100 lines; last registry row S050 at
line 56; `## Search log` 65-75; `## Leads (unopened)` 77-81; `## Registry changes` 83-100).

Revision note: v2 of this draft supersedes v1 (sha256 `9f485e62…f489`, read by ExecRegistryAppend). Changes:
the Search-log bullet's PRISMA counts move to the version-index accounting (8/3/1/7) with the sweep named as
eight terms after a second-seat reproduction, and §4's pipe claim is corrected (the R8 block carries one
escaped `|` inside a backticked `grep` pattern).

## Apply points (ExecRegistryAppend)

1. **Registry row** — insert as a new line immediately after `| S050 | …` (current line 56): last row of the
   `## Registry` table, before the blank line that precedes `## Paths`.
2. **Search-log bullet** — append as the last bullet of `## Search log`, after the round-33
   "Chinese crowdsourced-testing platform scope and reward rules sweep" bullet (current line 75), before the
   blank line that precedes `## Leads (unopened)`.
3. **Registry-changes lines** — append at the end of the file, after the current last line
   `- No status/recheck/used-by cell changed on any pre-existing row; S001–S048 untouched (logged). Registry 48 rows pre-append → 50 post-append (R8).`
   (current line 100). Append exactly three bullets, in the order given.

Do not reflow, wrap, or re-order anything else; the row is one physical line.

---

## 1. Registry row — verbatim (one line)

```
| S051 | Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ | docs | A | Immunefi's own Web3 severity classification system v2.2 as this page states it: the five levels Critical to None and the impact bullets each level lists for the Smart Contracts table, which is this row's subject | capture corpus/source-snapshots/round-34/S051.txt (sha256 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5, 175 lines): H1 L45 names v2.2; L46 the five-level sentence; L52 the factors-versus-impact sentence; L53-L56 the consequence-of-a-successful-exploit paragraph with the downgrade-or-reject caveat; L72 Smart Contracts heading; L73 LevelImpact; L74-L83 Critical bullets (direct theft of user funds and of NFTs, permanent freezing of funds and of NFTs, miner-extractable value, unauthorised NFT minting, predictable RNG, unintended NFT-representation alteration, protocol insolvency); L84-L89 High; L90-L94 Medium; L95 Low; L96 None | Immunefi's VSCS v2.2 places Web3 bugs on a five-level scale, decides the level mainly by the impact a successful exploit causes, and may downgrade or reject that level when exploiting it needs elevated privileges or uncommon user interaction, so read the Smart Contracts bullets as v2.2's impact vocabulary rather than as CVSS scores, a program's payout ladder or an authorisation to test | mined | 2026-10-26 | 90d | corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md |
```

Cell check (measured, §4): 11 cells, `awk -F'|'` NF=13, no `|` inside any cell, status `mined`, kind `docs`,
tier `A`, opened `2026-10-26` (past date), recheck `90d` (cadence form), used-by a lane path.

## 2. Search-log bullet — verbatim (one line)

```
- Immunefi severity-classification sweep (round 34); question: does the lane already hold a Web3 or smart-contract bounty severity-classification source, and does Immunefi's own Vulnerability Severity Classification System v2.2 add impact-level ground that the F13 and F16 platform ladders (S043, S044, S049, S050) do not; where: Immunefi's own site — the severity-classification index at https://immunefi.com/severity-classification-systems/ and every version page it lists, with https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ captured under the instrument UA into corpus/source-snapshots/round-34/S051.txt (status 200, 8502 bytes, 175 lines, sha256 4fd8ed98…b325a5) and v2.3 opened alongside it; plus an eight-term negative sweep (Immunefi, VSCS, "smart contract", "smart-contract", web3, blockchain, Solidity, "bug bounty") over the lane's own corpus/knowledge/*.md (45 files at measurement time, before this round's F17 entry landed — PRE-STATE; 46 after), corpus/README.md, corpus/SOURCES.md and SKILL.md; date: 2026-10-26; identified 8, screened 3 (the index, v2.2 and v2.3 read in full; five further version pages title-screened), included 1 (v2.2 → S051), excluded 7: the index names v2.3 and v2.2 under Currently in Use and files v2.1, v2, v1.2, the "Updated" system and the plain system under Being Phased Out, so those five pages were excluded at title level, the index itself carries no level or impact, and the v2.3 page states a four-level scale — a concurrent instrument whose bullets are not read as v2.2's. The negative sweep found Immunefi only as a platform or workspace name: 6 knowledge files (parked-claim rows, intake-surface datasets, workspace and archive ledgers), 2 README lines in the lost-tree note and 2 SKILL.md platform-table lines, with VSCS, "smart contract" unhyphenated, blockchain and Solidity in 0 files, "smart-contract" in 2 files that cite a parked claim id and a checkout rule, web3 in 6 files only as a dataset or source-kind label, and "bug bounty" in 2 files. No lane entry carried a smart-contract impact-level ladder: S043/S044 are platform ladders and S049/S050 are CN reward rules. Stop: Immunefi's own index closes the version set, one opened authority answers the bounded question, and the index's secondary Help Desk explainer of the v2.3 impacts was deliberately left unscreened; a guessed bare-slug URL (…-system/) returned 404 and was dropped before screening. The index and v2.3 findings are fetch observations with no committed capture, so no row cell or entry claim rests on them, and S051's `90d` recheck cell is a cadence rather than a recency claim.
```

PRISMA fields present: question, where, date, identified/screened/included/excluded with reasons, stop rule.

## 3. Registry-changes lines — verbatim (three bullets)

```
- S051 row added: new row (id `S051`, kind `docs`, tier A scoped to Immunefi's own VSCS v2.2 statements and anchored to its Smart Contracts impact bullets, status mined, opened 2026-10-26, recheck `90d`, used-by `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`), anchor pinned to the round-34 capture `corpus/source-snapshots/round-34/S051.txt` (sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`, 175 lines: H1 L45 names v2.2, five-level sentence L46, factors-versus-impact sentence L52, consequence-of-a-successful-exploit paragraph L53-L56, Smart Contracts heading L72, levels L74-L83, L84-L89, L90-L94, L95, L96). Live-capture admission, not a staged row: an `immunefi`/`vscs` grep over `/home/vgpnk/Projects/shokuknow/merge/kasegi/` returns no files, so no staged `SOURCES.append.md` row exists for this document and no staged cell was rewritten.
- S051 scope recorded without a recency claim: no cell says `latest` or `current`, because the index fetch of 2026-10-26 (no committed capture; observation only) marks v2.3 and v2.2 both Currently in Use; S051 therefore states v2.2 and carries a `90d` cadence rather than a recency claim, and no other cell or entry claim rests on that observation.
- No status/recheck/used-by cell changed on any pre-existing row; S001–S050 untouched (logged). Registry 50 rows pre-append → 51 post-append (R8).
```

R8 reading: one row added; one provenance statement (live capture, no staged row); one scoping statement (no
recency claim, the index observation logged here only); the 50 → 51 tally; and an explicit statement that no
pre-existing cell changed.

## 4. Local checks run on the draft

| check | command | result |
|---|---|---|
| captured bytes match the landed file | `sha256sum corpus/source-snapshots/round-34/S051.txt` | `4fd8ed98…b325a5` — the same digest my scratch capture printed; `wc -lc` = 175 lines, 8 502 bytes |
| row cell count | `awk -F'|' '{print NF}'` on the row line | `NF=13`, `pipes=12` |
| pipes in the prose blocks | `grep -c '|'` per line | Search-log line 0; R8 block 1, the escaped `\|` inside the backticked `immunefi\|vscs` grep pattern (prose, outside the registry table; census E12 fires only on row-shaped lines) |
| PRE-STATE sweep (45 knowledge files) | eight-term loop, §2 | Immunefi 6 files / README 2 / SKILL 2 / SOURCES 0; VSCS 0; "smart contract" 0; "smart-contract" 2; web3 6 / SKILL 1; blockchain 0; Solidity 0; "bug bounty" 2 / SOURCES 1 |
| POST-STATE re-run (46 files, F17 entry landed) | same loop | Immunefi 7 / VSCS 1 / "smart contract" 1 / "smart-contract" 3 / web3 7 / blockchain 1 / Solidity 0 / "bug bounty" 2 — the new entry accounts for the delta, which is why the bullet carries the PRE-STATE label |
| index grouping and version links | ordered extraction of `severity-classification-systems` HTML | Currently in Use: v2.3, v2.2 · Being Phased Out: v2.1, v2, v1.2, "Updated", plain — 7 version links + the index = 8 identified |
| v2.3 scale | `capture-source.py` of the v2.3 URL (scratch) | `At Immunefi, we classify bugs on a simplified 4-level scale:` — four levels Critical/High/Medium/Low |
| staged package | grep over `…/shokuknow/merge/kasegi/` | 0 files |
| registry anchors unchanged | `grep -n` for S049/S050 and section heads | S050 still line 56; `## Search log` 65; last bullet 75; `## Registry changes` 83; file 100 lines |

## 5. Non-claims and limits

- This seat writes no product file: ExecRegistryAppend applies the row; ExecSnapshotR34 owns the capture and
  manifest; ScribeEntryF17 owns the entry. Census E11 needs the `used-by` path on disk, so the append waits
  on that file, as ExecRegistryAppend already stated.
- Nothing outside the capture is asserted by the row: no VSCS-to-CVSS mapping, no payout, no claim that v2.2
  is the only or newest Immunefi system.
- The index and v2.3 findings are fetch observations (uncommitted, no digest pinned in the lane). They justify
  the exclusion reasons and the "no recency claim" scoping only; promoting them to corpus ground needs their
  own captures and rows, which this draft does not create.
- Line numbers hold only while the capture bytes hold; a re-capture that changes the snapshot invalidates
  L45-L96 and the anchor cell must be re-pinned in the same commit.

## Report

Seat: ScribeSOURCESRow. Deliverable: the three SOURCES.md blocks in §1-§3, ready for verbatim append.

### Commands and outputs (all exit 0 unless stated)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
$ wc -lc corpus/source-snapshots/round-34/S051.txt
175 8502 corpus/source-snapshots/round-34/S051.txt
$ row=$(grep -m1 '^| S051 |' .ufo/waves/round-34/wave1/ScribeSOURCESRow.md); printf '%s\n' "$row" | awk -F'|' '{print "NF="NF; print "pipes="gsub(/\|/,"|")}'
NF=13
pipes=12
$ ls corpus/knowledge/*.md | wc -l            # before the F17 entry landed
45
$ for t in Immunefi VSCS "smart contract" "smart-contract" web3 blockchain Solidity "bug bounty"; do
    printf '%s | knowledge_files=%s README=%s SOURCES=%s SKILL=%s\n' "$t" \
      "$(grep -rilF -- "$t" corpus/knowledge/*.md | wc -l)" \
      "$(grep -icF -- "$t" corpus/README.md)" "$(grep -icF -- "$t" corpus/SOURCES.md)" \
      "$(grep -icF -- "$t" SKILL.md)"; done
Immunefi | knowledge_files=6 README=2 SOURCES=0 SKILL=2
VSCS | knowledge_files=0 README=0 SOURCES=0 SKILL=0
smart contract | knowledge_files=0 README=0 SOURCES=0 SKILL=0
smart-contract | knowledge_files=2 README=0 SOURCES=0 SKILL=0
web3 | knowledge_files=6 README=0 SOURCES=0 SKILL=1
blockchain | knowledge_files=0 README=0 SOURCES=0 SKILL=0
Solidity | knowledge_files=0 README=0 SOURCES=0 SKILL=0
bug bounty | knowledge_files=2 README=0 SOURCES=1 SKILL=0
$ grep -ril 'immunefi\|vscs' /home/vgpnk/Projects/shokuknow/merge/kasegi/ | wc -l
0
$ grep -n "^## Search log\|^## Leads\|^## Registry changes" corpus/SOURCES.md
65:## Search log
77:## Leads (unopened)
83:## Registry changes
$ grep -n "^| S050 " corpus/SOURCES.md | cut -c1-20
56:| S050 | 360SRC
```

Live reads (read-only HTTP, my own instrument run into scratch; the lane capture landed afterwards with the
same digest):

```
$ python3 corpus/instruments/capture-source.py --id S051 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ --out $S/S051.txt
S051 status=200 fetched_bytes=219383 snapshot_bytes=8502 sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 utc=2026-10-26T05:31:15Z
$ python3 corpus/instruments/capture-source.py --id IDX --url https://immunefi.com/severity-classification-systems/ --out $S/IDX.txt
IDX status=200 fetched_bytes=149273 snapshot_bytes=4122 sha256=2ca35aee10bd7923c0900b8a4502cdd542a24a08cf30c298a047708d42010469
$ python3 corpus/instruments/capture-source.py --id V23 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3/ --out $S/V23.txt
V23 status=200 fetched_bytes=230877 snapshot_bytes=12895 sha256=f669160df3e367abaa2aaaf819f26c1b248062e68190ba30389981085a2a979a utc=2026-10-26T05:36:12Z
$ curl -s -o /dev/null -w '%{http_code}\n' -A '<instrument UA>' https://immunefi.com/immunefi-vulnerability-severity-classification-system/
404
```

Ordered index extraction (my own HTML fetch, `probe_41e36345.html`, 149 273 B):

```
### Currently in Use
immunefi-vulnerability-severity-classification-system-v2-3
immunefi-vulnerability-severity-classification-system-v2-2
### Being Phased Out
immunefi-vulnerability-severity-classification-system-v2-1
immunefi-vulnerability-severity-classification-system-v2
severity-system-comprehensive
severity-updated
severity-system
```

### File digests at handoff

```
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
```

Row line and bullet digests are reported to ExecRegistryAppend with the handoff message (a file's own digest
changes on every edit, so it is not quoted inside the file being edited).

### Findings for the L1

1. **F17's version framing needs a qualifier.** Immunefi's own index marks **v2.3 and v2.2 both "Currently in
   Use"**, and the v2.3 page states a **four-level** scale, not v2.2's five. The row therefore attributes the
   five-level scale to v2.2 explicitly, and the R8 line records the observation. Any round-34 text saying
   "Immunefi's five-level system" without the v2.2 qualifier would be an overstatement — the entry
   (`ScribeEntryF17`) and the F17 README row are the places to check this.
2. **v2.3 is a candidate F18, not a defect.** It is a distinct concurrent document; admitting it needs its own
   capture, row and entry. This draft does not create them (the claim names v2.2).
3. **Provenance is live-capture, not campaign-package.** No staged `SOURCES.append.md` row exists for this
   document, so no staged-cell rewrite applies; the row lands from the round-34 capture only.
4. **The append is gated on the entry file** (census E11). ExecRegistryAppend holds until
   `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` exists; the entry landed while this draft
   was being finished, so the gate is now open.
5. **Rule-B binding measured, not assumed.** `corpus/source-snapshots/round-34/manifest.json` now carries the
   S051 record (`url` = the v2.2 URL with its trailing slash, `fetched_utc` `2026-10-26T05:31:10Z`, sha256
   `4fd8ed98…b325a5`, 18 quotes at L46-L99). Applying the checker's own tokenizer
   (`URL_TOKEN = re.compile(r"https?://[^\s|]+")`, trailing `.,;:` stripped) to the drafted source cell yields
   exactly `['https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/']`, equal to
   the record's `url`, so rule B binds once the row is appended; before the append the instrument reports
   `FAIL rule=no-row record=S051` by design. The row's anchor locators overlap the manifest's quote locators
   (L46, L52-L56, L72-L96) and cite nothing the manifest does not cover.

### Scratch

`/fast/scratch/hyaku/kasegi-r34/ScribeSOURCESRow/` held `S051.txt`, `IDX.txt`, `V23.txt`, `page.html` and
three probe HTML files; removed with `rm -rf` after the readings above were transcribed. No tool was
installed or upgraded (no `pacman`, `uv`, `npx`, or binary fetch).
