# ReviewC1Sites — round-97 C1 tranche 12: the 33 qualify-lane rows

Seat: `ReviewC1Sites` (leaf). Slice: every row of `.ufo/waves/round-97/c1/repair-map.tsv` read against the committed bytes of its line at the C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`; truth-test each substitution; flag any site whose qualification changes what the sentence asserts; emit the round-98 label set for any wrong site.

Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`; freeze `daf7fc6a627d615178c27594110e956e592e4cd9`; C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`; C2 landing `a9a53608dce6aea07d298bb9d5133532078eb1dd` (not in this slice).

## Verdict

C1 STANDS on the 33-row site review: **33 CORRECT, 0 PARTIAL, 0 WRONG**. No qualification changes what its sentence asserts. P1 re-derived pass rc=0 (M0 `1040/2041`, M1 `1043/2035`, M3 `same_files=True bad_lines=0 old_not_once=0 dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M6 the frozen map sha, M9 `rows=33 unbound=none`, M10 `labelled=33 want=33 mapped=33 kinds=qualify-lane=33`). P3 re-derived pass (exactly the sixteen `corpus/knowledge` files; `SKILL.md` byte-identical base..landing). Two claim-text qualifiers, neither re-scores C1: `claims.json` C1.surface says "12 corpus/knowledge files" where the statement, map and landing say sixteen; and the meter-arithmetic parenthetical mis-attributes the −6 denominator. P2: the 14-control harness re-run against the landing prints `ATTRIBUTION pass fixtures=13` and `C1-CONTROLS-RESULT pass controls=14` (receipt 21); the committed pre-freeze receipt (receipt 20) is the candidate-side evidence.

## Method

For each of the 33 rows: extract the base and landing line; assert the base line contains the map's `old` exactly once; apply every edit the map names for that line; compare the result to the landing line byte-for-byte; assert the label equals the map's `new` and the `fix` is `Qualify to <path>`; assert no bare token of the nine remains on the edited line; assert the target is tracked at the landing and classifies INTERNAL through the pinned `resolve.py` (the meter's own `reading()`); quote the anchor line. Truth test per row: (a) the bare token names the lane's own instrument — not the lost tree's copy, not a manifest field value; (b) the qualified path is the tracked file at the landing; (c) the sentence still reads true with the path substituted.

Result of the mechanical checks: 33 rows on 30 lines in 16 files; `old` occurs exactly once in every base line; every multi-edit line reproduces byte-for-byte after all its edits; `old == "`"+key+"`"` and `new == "`"+label+"`"` for all 33; zero bare tokens of the nine remain on any edited line; all nine targets are tracked at the landing and INTERNAL (receipts 09, 18, 06).

## Row verdicts

All anchors are quoted from the landing bytes. `…` marks omitted text; nothing inside a quote is altered. The table quotes the clause containing each substitution; the complete base and landing line for every row is in receipt 04, and the surrounding context in receipt 05.

| # | site | key | verdict | anchor (landing bytes) | note |
|---|---|---|---|---|---|
| 1 | capture-intake-gate.md:5 | capture-secret-scan.py | CORRECT | `` `git show 643ddb43…:corpus/instruments/capture-source.py \| sha256sum` and the same for `corpus/instruments/capture-secret-scan.py` print the two digests above `` | "the same for X" is the same `git show <rev>:X \| sha256sum`; X is the lane's tracked instrument and the digests above are those paths' digests |
| 2 | capture-intake-gate.md:11 | capture-source.py | CORRECT | `` `corpus/instruments/capture-source.py` and `corpus/instruments/capture-secret-scan.py` are the lane's own instruments: every sentence about the gate's order, refusal line, exit code, allowlist and limits is about those bytes at `643ddb43…` `` | the sentence itself says "the lane's own instruments"; the path is that instrument |
| 3 | capture-intake-gate.md:11 | capture-secret-scan.py | CORRECT | same line as row 2 | second key on the same line; both substituted, both true |
| 4 | capture-intake-gate.md:105 | capture-source.py | CORRECT | `` the gate inherits each through `patterns()` without a change to `corpus/instruments/capture-source.py` `` | the instrument that owns `patterns()` is the tracked file |
| 5 | capture-intake-gate.md:178 | anchorcheck.py | CORRECT | `` `corpus/instruments/anchorcheck.py` prints `0 bad` on this draft (FC-6) `` | command subject is the lane's instrument |
| 6 | capture-intake-gate.md:262 | source-recheck.py | CORRECT | `` S131 was re-read from its committed snapshot through `corpus/instruments/source-recheck.py` `` | the re-read tool is the tracked instrument |
| 7 | chinese-crowdsourced-testing-scope-and-rewards.md:300 | source-recheck.py | CORRECT | `` under `corpus/instruments/source-recheck.py`'s declared normalization `` | normalization defined by the tracked instrument |
| 8 | cisa-bod-20-01-vdp-minimums.md:4 | capture-source.py | CORRECT | `` then normalized by the lane's `corpus/instruments/capture-source.py` `` | "the lane's" + tracked path; no anachronism (added at that path round-24, before the 2026-10-26 capture) |
| 9 | cisa-cvd-program-stages.md:4 | capture-source.py | CORRECT | `` then normalized by the lane's `corpus/instruments/capture-source.py` `` | same sentence shape as row 8 |
| 10 | citation-bases.md:64 | anchorcheck.py | CORRECT | `` `LOST-RECORDED` under `corpus/instruments/anchorcheck.py`, GONE+synthetic under `` | the classifier is the lane's instrument; the lost-base anchors are the object, not the instrument |
| 11 | citation-bases.md:65 | resolve.py | CORRECT | `` `corpus/instruments/resolve.py`, never counts as verified). `ufo-fsd-alpha` is NOT a lost base — `` | the resolver is the lane's instrument |
| 12 | citation-bases.md:74 | anchorcheck.py | CORRECT | `` Machine-readable pin declaration for `corpus/instruments/anchorcheck.py` (plain HTML comment, never backticked) `` | the declaration is the `<!-- pin: … -->` comment anchorcheck.py parses; its literal content (`pin: SKILL.md fc6d398`) is unchanged, so the assertion about the declaration form is untouched |
| 13 | cloud-signed-url-credentials-in-captured-evidence.md:69 | claim-package-check.py | CORRECT | `` The claim-package gate's `SECRET_PATTERNS`, imported from `corpus/instruments/claim-package-check.py` beside the instrument so the two never drift `` | the imported module is the tracked file beside the scanner |
| 14 | considerthese-proposals-ledger.md:125 | r35-defect-closure.sh | CORRECT | `` Placeholder half live: `corpus/instruments/r35-defect-closure.sh` prints `closed=7/7 exit=0` at round-42 base `` | the script existed at this path from round 35, before the round-42 base |
| 15 | considerthese-proposals-ledger.md:125 | r36-closure.sh | CORRECT | `` porcelain half in `corpus/instruments/r36-closure.sh` E9(b), r38 G4/G6, r39 G2/G5/G6 + `corpus/QUALITY.md:292` (R33) `` | second key on the same line; the round labels `r38 G4/G6` are not path tokens and were correctly left alone |
| 16 | considerthese-proposals-ledger.md:140 | r36-closure.sh | CORRECT | `` Porcelain half remains `corpus/instruments/r36-closure.sh` E9(b), r38 G4/G6, r39 G2/G5/G6, and `corpus/QUALITY.md:292` (R33) `` | this line already carried the qualified `bash corpus/instruments/r35-defect-closure.sh`; the qualification makes the pair consistent |
| 17 | first-psirt-maturity-document.md:11 | source-recheck.py | CORRECT | `` re-checked by the production instrument: `corpus/instruments/source-recheck.py` reports 54/54 OK (S100 44, S101 10), exit 0 `` | the count is superseded by V67-1, but the instrument identity is right and the qualification does not touch the count |
| 18 | first-psirt-maturity-document.md:68 | source-recheck.py | CORRECT | `` The attributed-claim-table preamble above says "`corpus/instruments/source-recheck.py` reports 54/54 OK (S100 44, S101 10)" `` | a present-tense quote of line 11; line 11 was edited in the same commit, so the quote still matches its target. The superseded element (the count) is unchanged |
| 19 | first-psirt-services-framework.md:41 | capture-source.py | CORRECT | `` L1 opened the page with `corpus/instruments/capture-source.py` (HTTP 200, 229255 fetched bytes, 170137 snapshot bytes, `fetched_utc` 2026-11-04T19:26:27Z) `` | the fetch tool is the tracked instrument |
| 20 | immunefi-vscs-v2-2-smart-contract-severity.md:111 | source-recheck.py | CORRECT | `` so `corpus/instruments/source-recheck.py` prints `occurrences=2 anchor=N-ok` `` | the reporting tool is the tracked instrument |
| 21 | japanese-domestic-disclosure-workflow.md:101 | source-recheck.py | CORRECT | `` `corpus/instruments/source-recheck.py` accepts one `--source` per invocation (`corpus/instruments/source-recheck.py:275`) `` | the line already anchored the qualified path at `:275`; the bare name and the anchor now agree |
| 22 | presigned-url-credentials-in-captured-evidence.md:92 | source-recheck.py | CORRECT | `` `corpus/instruments/source-recheck.py` prints `S124:sha256 OK` then `S124:Q01-session-token OK occurrences=1 anchor=84-ok` `` | the reporting tool is the tracked instrument |
| 23 | program-severity-ladders-and-reward-scales.md:66 | source-recheck.py | CORRECT | `` `corpus/instruments/source-recheck.py` counts normalized substrings across the whole capture `` | the counting tool is the tracked instrument |
| 24 | root-loss-2026-10-12.md:54 | anchorcheck.py | CORRECT | `` **Instruments:** `corpus/instruments/anchorcheck.py` and `corpus/instruments/resolve.py` now DERIVE their roots `` | the sentence is explicitly about the lane's instruments |
| 25 | root-loss-2026-10-12.md:54 | resolve.py | CORRECT | same line as row 24 | second key on the same line |
| 26 | root-loss-2026-10-12.md:56 | anchorcheck.py | CORRECT | `` never hardcode; `corpus/instruments/anchorcheck.py` reports `BASE-ABSENT` as its own verdict for citations into an absent base that were not yet marked `` | the verdict printer is the tracked instrument |
| 27 | source-tree-loss-2026-09-28.md:321 | density.py | CORRECT | `` \| `corpus/instruments/density.py` file mean over `SKILL.md` (18 blocks) \| 142.5 \| **152.9** \| `` | the table header is `\| instrument \| before r15 \| after r15 \|`; the cell names the instrument that produced the measurement |
| 28 | source-tree-loss-2026-09-28.md:322 | density.py | CORRECT | `` \| `corpus/instruments/density.py` path-citation instances \| 376 \| **623** \| `` | same table, same instrument |
| 29 | source-tree-loss-2026-09-28.md:327 | resolve.py | CORRECT | `` \| `corpus/instruments/resolve.py` SKILL.md resolvability \| 47/289 = 16.26 % \| **222/486 = 45.68 %** \| `` | same table, instrument column |
| 30 | source-tree-loss-2026-09-28.md:328 | resolve.py | CORRECT | `` \| `corpus/instruments/resolve.py` corpus resolvability \| 129/971 = 13.29 % \| **396/1297 = 30.53 %** \| `` | same table, instrument column |
| 31 | source-tree-loss-2026-09-28.md:329 | resolve.py | CORRECT | `` \| `corpus/instruments/resolve.py` lane total \| 156/1107 = 14.09 % \| **410/1437 = 28.53 %** \| `` | same table, instrument column |
| 32 | source-tree-loss-2026-09-28.md:330 | anchorcheck.py | CORRECT | `` \| `corpus/instruments/anchorcheck.py` over `SKILL.md` \| n/a \| 194 in-range mirror cite instances, **0 past-EOF**; 47 MISSING-FILE are the expected lost-tree and package-relative anchors (`docs/*`, `claims/*`, `status.json`, `INGESTION.md`, `fleets/*`) `` | the instrument is the lane's; the lost-tree paths in the same cell are untouched and remain the object of the sentence |
| 33 | vendor-third-party-finding-coordination.md:168 | source-recheck.py | CORRECT | `` `corpus/instruments/source-recheck.py`'s declared normalization (capture markup stripped, whitespace `` | normalization defined by the tracked instrument |

## Assertion-change flags

None. I checked the three named traps explicitly:

- **Manifest `path` field values** — no row is a manifest field. The only manifest-adjacent rows are 20 and 22, where the sentence names the instrument that *reports against* a manifest (`occurrences=2 anchor=N-ok`, `S124:sha256 OK`); the manifest path itself is elsewhere on those lines and was not edited.
- **Directory listings** — no row is a listing. Rows 27-32 are table cells under an `instrument` column, not a listing of files.
- **Lost-tree paths** — no row qualifies a lost-tree path. Rows 10-11, 24-26 and 27-32 are about the lane's own instruments classifying or measuring lost-tree/lost-base anchors; the lost-tree paths in those sentences (`docs/*`, `claims/*`, `status.json`, `INGESTION.md`, `fleets/*`, the `[lost-base]`/`[lost-tree]` prefixes) are untouched. The instruments were never in the lost tree.

Two rows deserve a note even though they are CORRECT:

- Row 18 quotes line 11 in the present tense ("the preamble above says"). Line 11 was edited in the same commit, so the quote still matches its target; the superseded element (the 54/54 count) is unchanged. If a later tranche edits line 11 without line 68, the quote would drift — not a current defect.
- Row 12's declaration content is `pin: SKILL.md fc6d398`, which the qualification does not touch; the parenthetical "(plain HTML comment, never backticked)" describes the declaration, not the instrument name.

## Qualifiers (routed; no verdict change)

**Q1 — `claims.json` C1.surface says 12 files, the claim says sixteen.** C1.surface reads "33 bare lane-instrument basenames in 12 corpus/knowledge files"; the statement says "sixteen corpus/knowledge files"; the map names sixteen distinct files; the landing stat is 16 files changed. The predicate does not read the surface field, so this does not re-score C1. Routed defect: surface text should say sixteen.

**Q2 — the meter-arithmetic parenthetical mis-attributes the −6 denominator.** The statement says "three of the nine qualified tokens are new to the scope (+3 numerator, +3 denominator) and six already existed in the scope (-6 denominator, numerator unchanged)". Measured decomposition (receipt 06): the base scope holds 2041 distinct tokens = 2032 common + nine bare GONE tokens; the landing scope holds 2035 = 2032 common + three new INTERNAL qualified paths; zero class changes among the 2032 common tokens. So: nine bare rows leave (−9 denominator), three qualified paths are new (+3 numerator, +3 denominator), six qualified paths already existed as INTERNAL (0 change). Net +3 numerator, −6 denominator — the net numbers (1043/2035) are right, but the −6 is not contributed by the six pre-existing paths, which contribute nothing. The orchestrator's paraphrase ("six already existed, so those rows shrink the denominator instead") repeats the mis-attribution. Routed qualifier: the explanatory clause should read "nine bare rows leave (−9); three qualified paths are new (+3/+3); six qualified paths were already INTERNAL (0)".

## Round-98 label set

No wrong site, so `.ufo/waves/round-97/w1/round98-labels.tsv` is header-only, matching the round-96 shape: `line	key	label	fix	evidence`.

## Residual risk and verification gaps

- **P2 candidate-side replay.** The committed controls receipt pins `candidate=f410e91f0aaa43310866f4fddae31f13470a83d1` and `freeze=2059fcbade2fddfa9be6430d15a401a5165dfd0a`; both are scratch-clone objects and are absent from the lane object store (`git cat-file -e` → rc=1 for both; receipt 22), so the exact pre-freeze candidate run cannot be replayed. I re-ran the same 14 controls against a clone of the landing (receipt 21); that is the reproducible half of P2. The C1 artifacts are byte-identical at the freeze and the landing (receipt 23), so the landing's labels/map/counter are the frozen ones.
- **C2 is out of this slice.** I did not review the capture-secret-scan families, the selftest 128→148, or the SCORECARD row.
- **Scope of the meter.** The meter's scope is `corpus/knowledge/*.md` only; bare tokens elsewhere in the lane are outside this tranche and are not claimed.
- **Row 12 label evidence.** The evidence column says "the instrument whose header comment is quoted"; the sentence actually states the pin-declaration form rather than quoting a header comment. The instrument identity is right; cosmetic only.
- **No host-path or binary-editing exposure.** All reads were `git show`/`git ls-tree`/`git log` on the lane and the meter's own `git archive` extracts in scratch; no host path was passed to a binary-editing tool.

## Receipts

All under `.ufo/waves/round-97/w1/ReviewC1Sites-receipts/`.

| # | command | observed | file |
|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-97/c1/knowledge-meter.py --lane <lane> --base-rev b06af5e --after-rev 75a4718 --map .ufo/waves/round-97/c1/repair-map.tsv --labels-rev daf7fc6a --base-target 1040/2041 --target 1043/2035 --map-sha256 f4ed7387… --work <scratch>` | rc=0; 12 output lines; `KNOWLEDGE-METER-RESULT pass`; M0 1040/2041, M1 1043/2035, M3 same_files=True bad_lines=0 old_not_once=0 dup_rows=0, M4 bad=none, M5 out_of_range=none, M9 rows=33 unbound=none, M10 labelled=33 want=33 mapped=33 kinds=qualify-lane=33, M6 the frozen sha | `01-p1-meter.txt` |
| 2 | same, stderr | 0 bytes | `02-p1-meter-stderr.txt` |
| 3 | `git show 75a4718 --unified=0 -- corpus/knowledge` | 155 lines; 25 hunks; 16 files | `03-c1-landing.diff` |
| 4 | base/after line dump per map row with `old`/`new` occurrence counts | 33 rows, 164 lines; `base_old_count=1`, `after_old_count=0` on every row | `04-map-rows-base-after.txt` |
| 5 | per-row context windows around the substituted path | 33 rows, 98 lines | `05-row-context-windows.txt` |
| 6 | token-scope diff base vs landing via the meter's own `reading()` | base (1040, 2041), after (1043, 2035); 9 base-only bare GONE, 3 after-only qualified INTERNAL, 0 class changes, 2032 common | `06-token-scope-diff.txt` |
| 7 | `git diff --name-only b06af5e 75a4718 -- corpus/knowledge`; `git diff --quiet … -- SKILL.md`; non-knowledge path count | 16 files; SKILL.md rc=0 (identical); 59 non-knowledge paths in the base..landing diff (wave artifacts committed between the base and the landing: round-87..97 receipts, round-97 freeze/c1/c2 files), outside P3's scope | `07-p3-fileset.txt` |
| 8 | `sha256sum` map/labels/counter vs frozen pins | all three match: map `f4ed7387…`, labels `5155959d…`, counter `a56198d0…` | `08-sha256-pins.txt` |
| 9 | byte-exactness / label-map / bare-remains / strict `old`==`key` and `new`==`label` check | 33 rows, 30 lines, 16 files, 0 defects; strict map-column check 0 defects | `09-map-label-bytecheck.txt` |
| 10 | `git log --diff-filter=A --name-status` for the nine instruments | all nine added (`A`) at `corpus/instruments/<name>`: eb5b590, d3614a2, 8bf9807, 132e16c, 5b4a850, 0aee0ef, caa3146 — no rename into the path, so no anachronism | `10-instrument-add-paths.txt` |
| 11 | `git show 75a4718:corpus/knowledge/<file> \| awk 'NR>=a&&NR<=b'` for the five risky regions | context for rows 1-6, 10-12, 17-18, 24-26, 27-32 | `11-context-*.txt` |
| 12 | labels `fix` and `evidence` columns | 33 rows each | `13-labels-fix.txt`, `14-labels-evidence.txt` |
| 13 | `git ls-tree -r --name-only 75a4718` for the nine targets | all nine tracked at the landing | `18-nine-tracked-at-landing.txt` |
| 14 | `head -1 .ufo/waves/round-97/c1/labels.tsv`; `wc -l` | header `line	key	label	fix	evidence`; 34 lines (33 rows + header) | `19-labels-header.txt` |
| 15 | committed controls receipt (read-only input) | 148 lines; `ATTRIBUTION pass fixtures=13`; `C1-CONTROLS-RESULT pass controls=14`; `candidate=f410e91f`, `freeze=2059fcba` | `20-committed-controls-receipt.txt` |
| 16 | `python3 -B .ufo/waves/round-97/controls/c1-controls-r97.py <landing-clone> 75a4718 <lane>/.ufo/waves/round-96/c1/knowledge-meter.py <work> <out>` | rc=0; `CONTROL …` lines all PASS with their declared limb sets; `ATTRIBUTION pass fixtures=13`; `C1-CONTROLS-RESULT pass controls=14` | `21-controls-rerun-at-landing.txt` |
| 17 | `git cat-file -e f410e91f…`; `git cat-file -e 2059fcba…` | rc=1, rc=1 (both absent from the lane object store) | `22-scratch-pins-absent.txt` |
| 18 | `git diff --quiet daf7fc6a 75a4718 -- c1/{labels.tsv,repair-map.tsv,knowledge-meter.py}`; sha256 at both revs | rc=0; labels `5155959d…`, map `f4ed7387…`, counter `a56198d0…` at both revs | `23-freeze-vs-landing-c1-artifacts.txt` |
| 19 | `git show --stat 75a4718` | 16 files changed, 30 insertions(+), 30 deletions(-) | `17-landing-stat.txt` |
