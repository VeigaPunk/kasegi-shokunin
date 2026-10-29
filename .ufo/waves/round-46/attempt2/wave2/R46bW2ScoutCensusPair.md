VERDICT: HOLDS

Seat: R46bW2ScoutCensusPair (leaf, read-only; no commits, no pushes, no git/jj/index mutation; scratch deleted on exit).
Tree facts established first (read-only): `git cat-file -t fe0f56b…` = commit; `git log --oneline -3` on /home/vgpnk/Projects/shokunin/kasegi-shokunin prints, newest first:
- `96379ae round-46 (attempt 2): wave-1 integration — F29 entry + S074 row + admission blocks + ledger dispositions; …`
- `ee03806 round-46 (attempt 2): wave a2w1 spec (64 seats, v2) …`
- `fe0f56b round-46 (attempt 2): freeze claims C1 counter-mutation coverage + C2 frontier F29, counters v1 (mutbat, f29-gate), S074 capture + manifest-a2, R50 receipt, controls`
So fe0f56b is the FREEZE commit, not the wave-1 integration (HEAD 96379ae is). `corpus/SOURCES.md` is byte-identical (sha256 `d7c3df3b650521544dab896dcd0e6f80258b5780fcf9a8b1cc5e11fb810e89a9`, 162 lines) at base 04af9bc9 and at freeze fe0f56b — no S074 row there; the S074 row and the two draft-scaffold blocks below exist only at the integration tree (worktree == HEAD, sha256 `e3bdefcfaad97e093a2950af37e62430635f130d9ea2d43fb1585db988077a6c`, 185 lines; `git status --porcelain` shows only `.ufo/` files dirty). Both trees were checked; nothing below depends on which one "the tree under attack" names.

## Finding 1 — census pair re-run: exit 0, byte-identical to the before-receipt (HOLDS)
Attacked: `.ufo/waves/round-46/attempt2/controls/sources-census-before.txt` and live `corpus/SOURCES.md`.
Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
Quoted output (exit 0):
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```
`diff -u controls/sources-census-before.txt <live output>` → empty (byte-identical). Re-runs on scratch exports of base and freeze (`validate --file`): same three W04 lines, `ok`, exit 0 (the freeze --file run additionally storms E11 only because I exported `corpus/SOURCES.md` without its knowledge tree — used-by resolution is relative to the export root; the full-corpus base export grades clean, and the freeze registry is byte-identical to base). attempt2/freeze.txt:9 itself records the control as "controls/sources-census-before.txt (exit 0, three W04 warnings, census-before)" — consistent.

## Finding 2 — no new W04; S074 shares its URL with no held row (HOLDS)
Attacked: the three W04 warnings and the S074 row's URL.
Command: census-normalized URL extraction over all 74 live rows (first `https?://[^\s|]+` of the source cell, scheme stripped, host lowercased, trailing `/` and fragment stripped).
Quoted output: `rows: 74`; `S074 url occurrences among 74 rows: 1`; duplicated urls exactly:
```
  2x bughunters.google.com/about/rules/about-this-section -> ['S070', 'S072']
  2x cyclonedx.org/docs/1.7/json -> ['S059', 'S060']
  2x docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq -> ['S006', 'S028']
  2x eur-lex.europa.eu/eli/reg/2024/2847/oj/eng -> ['S024', 'S029']
```
S074's URL occurs once; S073's URL differs in path (`…/how-tos/report-and-fix-vulnerabilities/report-privately`). The printed W04 set is exactly the three pre-existing pairs. The fourth duplicate pair S059/S060 (same `cyclonedx.org/docs/1.7/json`, same scope cell) prints nothing because the census's W04 keys on url+scope and its E04 exempts a scope whose earlier same-URL row is rejected (S059 rejected → S060 mined passes silently); this pair pre-exists at base and is by-design census behavior, not a wave-1 artifact.

## Finding 3 — S074 row-shape guards pass; the item's census-gap premise is only true for compensated mutations (HOLDS, premise corrected)
Attacked: `corpus/SOURCES.md:80` (the S074 row) and the claim that the census does not check 11 cells / escaped pipes.
Direct measurement: `awk -F'|' 'NR==80{print "NF="NF" cells="NF-2 …}'` → `NF=13 cells=11`; backslash scan over the row → `0` (no escaped pipes anywhere); row starts and ends with `|`. The census script's own grammar (scripts/sources-census.sh E01: `if (NF!=13) printf "…E01\t%s fields=%d\n",lane,id,NF-2`) enforces exactly NF==13 for every `|`-leading row inside `## Registry`, and any `\|` inside a cell inflates NF — so single-fault violations of either named guard ARE census-checked (E01, exit 1).
Discrimination fixtures (scratch; census `validate --file`, do-nothing control vs mutants built from the byte-exact row):
```
F0 exact S074 row, lane layout          -> file	ok	…/fix2/corpus/SOURCES.md        exit=0
F1 drop used-by cell (10 cells)         -> file	E01	S074 fields=10                 exit=1
F2 inject ` \| ` into teaches           -> file	E01	S074 fields=12                 exit=1
F4 add a 12th cell                      -> file	E01	S074 fields=12 (+E11)          exit=1
F3 compensated: drop trailing pipe + ` \| x` (NF stays 13)
                                        -> file	E11	S074 missing used-by …md  \    exit=1
```
F0 (do-nothing) grades clean; every single-fault mutant is caught by E01. The residual gap the item gestures at exists only for the compensated case (F3): NF==13 is the census's ONLY row-shape invariant, so a dropped-pipe + escaped-pipe pair passes shape checks — in this concrete instance it still trips E11 on the corrupted used-by string (`…advisories.md  \`), but that is path existence, not a shape guard. The S074 row itself passes both named guards outright.

## Finding 4 — F29 Search-log bullet: every countable claim re-derives (HOLDS)
Attacked: the bullet text at `corpus/SOURCES.md:122` (inside the committed draft fence :121–:123; identical text in `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/rows.md:76`).
Re-runs on the base export (`git archive 04af9bc9… corpus`):
- `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md` → exactly `corpus/knowledge/github-private-vulnerability-reporting.md` and `corpus/SOURCES.md`, exit 0 (claimed "2 files … exited 0").
- `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `65` (claimed "over 65 knowledge files").
- `grep -ciE 'repository securit. advisor|GHSA' corpus/README.md` → `0`, exit 1 (claimed).
- `grep -rn 'S074' corpus/SOURCES.md corpus/README.md` → no output, exit 1 (claimed).
- Line-level `grep -rniE …` → exactly 4 hits: `SOURCES.md:74` (id S068, the rejected Advisory-Database row), `SOURCES.md:157` (the round-43 "Public disclosed advisory pair … identified 5 candidates, screened 5, included 1, excluded 4. GHSA-v…" bullet), and the F28 entry at `:40` and `:43` — the exact four the bullet names.
- `S073.txt:563` = "If you have admin or security permissions … create a draft security advisory directly. See Creating a repository security advisory." — the link-text-only exclusion reason checks out (`:561` likewise carries "Configuring private vulnerability reporting for a repository").
- PRISMA arithmetic: identified 4 units = primary page + F28 entry + S068 row + round-43 bullet; screened 4; included 1 (page → S074); excluded 3 (F28 entry counted once despite its two line-hits — the bullet's own phrasing). Consistent.
- On the landed tree the same `-rliE` command now prints 4 files (adds `corpus/knowledge/github-repository-security-advisories.md` and `corpus/README.md`): the bullet's "same command on the live lane printing the same 2 files" is a dated pre-integration PRE-STATE claim, true at authoring time, not reproducible on the integration tree (same class the round-35 correction bullets document). Not a count error.

## Finding 5 — S074 Registry-changes bullets: snapshot, manifest, locators, rows, sha pins all verify (HOLDS)
Attacked: the draft bullets at `corpus/SOURCES.md:183-184` (inside fence :182–:185) and the landed row :80.
- Snapshot: `sha256sum corpus/source-snapshots/round-46-a2/S074.txt` → `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`; `wc -l -c` → `42 7087`. Both match row + bullet + attempt2/freeze.txt:6.
- Manifest `round-46-a2/manifest.json` S074 record: `http.status 200`, `final_url` equals the row URL, `fetched_utc 2026-10-29T20:19:30Z`, `bytes 582877`, `snapshot_bytes 7087`, `lines 42`, exactly 9 quotes with anchors Q1:10, Q2:13, Q3:17, Q4:24, Q5:25, Q6:25, Q7:26, Q8:31, Q9:38.
- All 14 anchor locators land on the labeled content: L2 heading `## Repository security advisories`; L3 one-line purpose; L10 privately-discuss-and-fix; L12 draft advisory; L13 temporary private fork; L14 publish-on-patch; L17 credit; L24 GitHub-is-CNA; L25 CVE request + 72-hour review; L26 other-CNA boundary; L30-L31 publication visibility; L33 URL stability; L35-L36 Dependabot alerts; L37-L38 fix-version duty.
- Gate quote: S074.txt:25 contains exactly "Requesting a CVE identification number doesn't make your security advisory public." — 11 words, as the bullet says.
- Row bookkeeping: S-row counts base 73 / freeze 73 / live 74 ("Registry rows 73 → 74"); `git diff fe0f56b HEAD -- corpus/SOURCES.md` shows the table hunk adds exactly the S074 row and touches no pre-existing row (R8 claim holds).
- Capture-directory note: attempt-1 manifest sha256 `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` identical at base, HEAD and worktree; a2 manifest sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f` verified; pinned at attempt2/freeze.txt:7 (`manifest-a2-sha256`), recorded at `.ufo/waves/round-46/freeze.txt:7` and `wave1/R46SentinelContent.md:13`; `git diff --name-status 04af9bc9 HEAD -- corpus/source-snapshots/` → exactly `A round-46-a2/S074.txt` + `A round-46-a2/manifest.json`.

## Finding 6 — structural, for the L1 (INFO, not a count falsification)
The F29 Search-log bullet and both S074 Registry-changes bullets are NOT landed as real section bullets anywhere in the tree under attack. The live Search log's real bullets end at the F28 bullet (:111; round-44 at :109); `grep -n '^- S074 row added' corpus/SOURCES.md` hits only :183, inside the closing draft fence. The integration commit 96379ae added 23 lines: the S074 table row (+1) and two committed draft-scaffold blocks ("The `## Search log` bullet to append" :113–123, "`## Registry changes` bullets to append" :177–185, +22). The scaffold prose's line references (:90–:111, F28 at :110, Leads at :112, Registry changes at :118, file ends at :162) are exact for the 162-line freeze file and stale by +1/+13/+23 in the 185-line live file — the blocks were authored at freeze state and committed without executing the appends they describe. Whether that placement is what wave 1 intended is a scribe/integration question outside this seat; the counts inside the un-landed bullets are, per Findings 4–5, all correct.

## Limitations
- No live-target contact (bounds): the primary page is verified through the committed snapshot + manifest record only; "final URL equals the row URL" rests on the manifest's http record.
- The freeze `validate --file` E11 storm is an artifact of exporting SOURCES.md without its knowledge tree; the clean freeze-equivalent evidence is the byte-identical base registry's full-corpus run (Finding 1).
- The environment's `grep` prints a wrapped summary line ("grep: 4 matches in 2 files"); the underlying hits/lines/exit codes quoted above are as measured.
- The census fixtures live in scratch and were deleted on exit; their outputs are quoted verbatim in Finding 3 but the fixtures are not preserved (recipes reproducible from the quoted mutations).
- I did not audit the scribe's own receipts (sweep-receipts.txt, a2w1-results.json) as evidence — every number above is re-derived from the base export, the snapshot, the manifest, and git objects directly.

Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2ScoutCensusPair/` removed after this report was written. No tool installs were needed or performed. Files written: this report only.
