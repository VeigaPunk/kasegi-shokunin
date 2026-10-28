VERDICT: DRAFT-READY

Scope: C2 registry drafter B (independent). Draft file: `.ufo/waves/round-46/wave1/R46ScribeRowsB.draft/rows.md` (sections (a) S073 row, (b) Registry changes bullets, (c) Search-log bullet). No registry file, knowledge entry, manifest, or git state was touched; scratch removed on exit.

Landing constraint (the one thing the L1 must respect): the S073 row's used-by path `corpus/knowledge/github-private-vulnerability-reporting.md` does not exist yet. The row must land in the same commit as that entry. Alone, it fails the census (E11, exit 1) and drops the frozen C2 counter from 2/7 to 1/7 (findings 4 and 6).

## 1. S073 row shape: 11 cells, no `|` inside any cell
Command: `grep -m1 '^| S073 |' <draft rows.md> > s073.row; awk -F'|' '{print NF}' s073.row`
Output: `13` (13 fields from splitting on `|` = 11 cells plus two empty edges). Re-run on the final draft bytes: `final-row-NF=13`; `cmp` of the final draft row against the row that was validated printed `row-bytes-identical-to-validated`.

## 2. Anchor and quotes (S073 capture)
Command: `sha256sum .../freeze/corpus/source-snapshots/round-46/S073.txt; wc -lc`
Output: `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` and `589 15568` (matches the pinned sha256 in the brief and `manifest.json`).
Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` (run in the freeze export, 9f23aab)
Output: `S073:sha256 OK`, then `S073:Q1 OK occurrences=1 anchor=560-ok` through `S073:Q8 OK occurrences=1 anchor=578-ok`; exit 0.
Line check: `sed -n` on lines 556 (`Privately reporting a security vulnerability`), 560 (`Anyone can privately report...`), 583 (`YesNo`). Line 583 is the feedback widget, inside the brief's range 556-583; the row keeps the brief's range.

## 3. Redirect of the legacy URL
Command: `curl -sIL -A '<UA>' 'https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability' | grep -iE '^(HTTP|location)'`
Output: `HTTP/2 301` / `location: /en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately` / `HTTP/2 200`.
Command: `curl -sL -o /dev/null -w '%{http_code} %{url_effective} hops=%{num_redirects}\n' <legacy URL>`
Output: `200 https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately hops=1`. Canonical URL alone: `200 ... hops=0`. The redirect claim in the anchor cell is verified by these two live re-runs (2026-10-28), not by a committed capture; no source-recon file exists for it (`.ufo/waves/round-46/source-recon/` is empty).

## 4. Census validate on a scratch copy (the requested command)
Setup: scratch `$S/base` = `git -C <lane> archive 914ca0b... corpus SKILL.md ... | tar -x`; `$S/final` = that base with the final S073 row inserted after line 78 (the S072 row); line 79 blank in base.
Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/final/corpus/SOURCES.md; echo rc=$?`
Output (verbatim):
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S073 missing used-by corpus/knowledge/github-private-vulnerability-reporting.md
rc=1
```
What the census says about the used-by path: `E11 ... missing used-by corpus/knowledge/github-private-vulnerability-reporting.md`. The census checks `$dir/$path` for every mined row; `--file` sets `dir` to the file's grandparent (`$S/final`), so it is the scratch tree that is checked, and the path does not exist there. This is the expected state until the entry lands; E11 is the only error line.

Do-nothing control, same command on the base registry without the row: `file W04 S028 ...`, `file W04 S029 ...`, `file W04 S072 ...`, `file ok <base>/corpus/SOURCES.md`, `rc=0`. The row is what turns the validation red (E11), and the census still discriminates: an inserted junk row with an extra cell returns `file	E01	S073 fields=12`, `rc=1` (the row's `NF=14` case), so the E01 check is live.

## 5. Supersede-pair note (spot-check item 4): S072 supersedes S070, W04 is expected
Evidence: S072's teaches cell opens `supersedes S070 —` (`corpus/SOURCES.md`, the S072 row), and both S070 and S072 carry `https://bughunters.google.com/about/rules/about-this-section` (S070 `rejected`, tier C; S072 `rejected`, tier A, not mined). Census output line: `file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes`, printed on the base control with no S073 row (rc=0), so W04 is pre-existing and independent of the new row. It is a warning and does not affect validation. No E04 is raised because S072 is rejected (E04 applies to non-rejected rows only). The brief said "S072 mined"; the registry says `rejected`, and the bullet records the registry's status.

## 6. Frozen C2 counter on the freeze tree, with and without the row
Command: `python3 corpus/instruments/r46-c2-gate.py --root <freeze export>` (9f23aab)
Output (verbatim): `gate G3 pass=0 read=row-S073=absent-or-malformed`, `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`, `gate G7 pass=1 read=census-rc=0 ok-line=1`, `c2-gate fixed=2/7 exit=1` (matches the claims' stated freeze reading 2/7).
Command: same counter on a copy of the freeze tree with the final S073 row substituted into `corpus/SOURCES.md`.
Output: `gate G3 pass=0 read=bad=used-by`, `gate G4 pass=1 ... quotes-ok=8`, `gate G7 pass=0 read=census-rc=1 ok-line=0`, `c2-gate fixed=1/7 exit=1`.
So the row alone moves the counter the wrong way (2/7 to 1/7): G3 fails on the used-by path and G7 fails on the census. The row and the entry must land together, and the counter's G3 then needs the entry's path to exist.

## 7. Registry counts and the Registry changes bullet
Command: `census --file <base>/corpus/SOURCES.md` → `rows 72`, `status.mined 57`, `status.rejected 15`. Command on the row tree → `rows 73`, `status.mined 58`, `status.rejected 15`. These numbers are in the (b) bullet (72 → 73, mined 57 → 58).

## 8. Search-log sweep and the held rows
Command (cwd = base export): `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md; echo sweep-rc=$?` → `sweep-rc=1`, no lines (0 identified at base 914ca0b).
Same command at the freeze export → `sweep-rc=1`, no lines.
Held adjacent rows, read from the registry cells: S065 `rejected` (teaches: "screened out on the disjointness tie-break, not on quality"); S068 `rejected` (teaches: "screened out on primary-of-record and record completeness"). These are the exclusions in the (c) bullet (identified 3, screened 3, included 1 S073, excluded 2 S065 and S068).

## 9. Drafting notes and discrepancies with the brief
- "Pattern of the S071 bullet": no S071 bullet exists in `## Registry changes`. `grep -n "S071" corpus/SOURCES.md` returns only the table row (line 77). I used the S052 / S055 `row added` bullet pattern instead.
- S072 is `rejected`, not mined (registry row 78). The supersede note records that.
- The `|` in the (c) bullet appears only inside the grep pattern `private vulnerability reporting|privately report`, which is outside any registry cell. No registry cell contains `|` (row NF=13).

## Limitations
- Scope: I drafted only my single item (S073 row, Registry changes bullets, search-log bullet). The F28 knowledge entry and the C1 re-grounds named in the lane milestone are other seats' items; I did not build or counter-test them.
- The `E11` line is the expected missing-entry state, so the census result is red by design until the entry lands; I did not create the entry (outside my item).
- The census used a scratch tree from the base export (`corpus` plus root files). Mined rows other than S073 were checked against that export, not against the lane's live tree.
- The redirect and quotes were re-run on 2026-10-28; live docs.github.com pages are not byte-stable, and the captured digest (66c96a…1930) is the pinned evidence for the body text.
- The row's teaches cell is one benefit grounded in S073 lines 564-566 and 567-569 (the form steps); I did not run a non-author closure.
- Line 583 of the snapshot is the feedback widget text inside the brief's 556-583 range.
- No installs or upgrades were made. Nothing was committed or pushed. Scratch `$HYAKU_SCRATCH/kasegi-r46/R46ScribeRowsB` was removed on exit.

## Checks for the main agent after landing
1. `bash scripts/sources-census.sh validate --file corpus/SOURCES.md` must exit 0 and print no `E` line (only the W04 warnings for S028, S029, S072).
2. `python3 corpus/instruments/r46-c2-gate.py --root <lane tree>` after the entry lands (G3 and G7 should then read ok).
3. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` (already run here: Q1–Q8 OK).
