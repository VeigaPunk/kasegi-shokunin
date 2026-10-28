VERDICT: DRAFT-READY

Scope: C1/R1 registry rows (SOURCES.md S071 and S072) plus the C2 F27 source row, drafted at `.ufo/waves/round-45/wave1/R45ScribeRowsA.draft/rows.md`. Nothing was appended to `corpus/SOURCES.md`, nothing was committed, and no git/jj mutation ran. The only write is the draft file and this report. No tool was installed or upgraded.

## Findings

### F1. Source pins match the seat spec
Command: `sha256sum corpus/source-snapshots/round-45/S071.txt corpus/source-snapshots/round-45/S072.txt; wc -c -l corpus/source-snapshots/round-45/S071.txt corpus/source-snapshots/round-45/S072.txt`
Output:
```
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  corpus/source-snapshots/round-45/S071.txt
364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025  corpus/source-snapshots/round-45/S072.txt
  372 20152 corpus/source-snapshots/round-45/S071.txt
  312 10032 corpus/source-snapshots/round-45/S072.txt
```
Command: `jq -r '.body | length' .ufo/waves/round-45/source-recon/S072.json` → `10029`
Manifest `corpus/source-snapshots/round-45/manifest.json`: S071 `fetched_utc` `2026-10-28T20:52:44Z`, `bytes` 20152, `lines` 372; S072 `fetched_utc` `2026-10-28T20:53:00Z`, `bytes` 10032, `lines` 312. Headers record `last-modified: Sun, 09 Aug 2026 21:57:49 GMT` (`.ufo/waves/round-45/source-recon/S071.headers.txt`).

### F2. S071 teaches is grounded in the capture
Read with `cat -n corpus/source-snapshots/round-45/S071.txt`:
- L20-21: "with no version indication, your report / will not be processed." (manifest Q5 anchor 20 confirmed)
- L17-18 and L22-23: a stable commit ID or exact version is required.
- L112-113: "send it directly to the affected subsystem's maintainers and Cc: the Linux kernel security team."
- L308-315: "postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days if it is agreed..."
- Manifest quote anchors Q1 310, Q2 95, Q3 39, Q4 41, Q5 20 each land on the quoted text (checked with `cat -n`).
- Headings in the anchor cell all exist: lines 10, 73, 109, 174, 254, 299, 329, 359, 368 (`grep -n -E '^(=+|-+)$' -B1` output shows them).

### F3. S072 scope and the S069 restatement are grounded
`cat -n corpus/source-snapshots/round-45/S072.txt`: section headings at L17 (Android & Friends), L57 (Chrome & Friends), L107 (Google & Friends), L171 (Open Source), L249 (Other). Cloud VRP row L146-152, scope line L148-149: "Security issues affecting any Google Cloud product or web service that / handles reasonably sensitive user data".
Command: `sed -n 9,11p corpus/source-snapshots/round-44/S069.txt`
Output: "In principle, any [Google Cloud](...) / product or web service that handles reasonably sensitive user data is intended / to be in scope."
Same sentence in substance: the restatement claim holds (not verbatim).
Every program row links its `(rules)` page, so the table is a secondary routing summary to the primary rules pages. This is the basis for tier B.

### F4. Row shape: 11 cells, NF=13, no inner pipes
Command (after the rewrite): `grep -n -E '^\| S07[0-2] ' <appended SOURCES.md> | awk -F'|' '{print $1 $2 "NF=" NF}'`
Output:
```
76: S070 NF=13
77: S071 NF=13
78: S072 NF=13
```
Both new rows sit inside the Registry table after S070. `readable` appears twice in the S072 teaches cell.

### F5. Self-caught defect, fixed
The first draft had no closing ` |` after `used-by`. The census caught it:
```
file	E01	S071 fields=10
file	E01	S072 fields=10
```
Fix: the draft was rewritten with a trailing `|` on both rows. E01 is gone (see F7). The mutant M2 below reproduces the same class.

### F6. Do-nothing control: unmodified live registry
Setup: `cp -r corpus` into a scratch root, so existing `used-by` paths resolve. A first attempt that copied only `SOURCES.md` produced E11 on roughly 60 existing rows. That was a harness artifact and was discarded. `--file` resolves paths against the parent of the file's directory, so the full tree is required.
Command: `bash scripts/sources-census.sh validate --file <scratch>/base-full/corpus/SOURCES.md --today 2026-10-28`
Output:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	<scratch>/base-full/corpus/SOURCES.md
exit=0
```
The W04 lines are pre-existing and do not affect status.

### F7. Validator on the appended registry (the drafted rows)
Command: `bash scripts/sources-census.sh validate --file <scratch>/app-full/corpus/SOURCES.md --today 2026-10-28`
Output:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
exit=1
```
Reading: the only new finding is E11 for S071, and the path does not exist because its knowledge entry is not written yet. This is the separate, expected missing-path error the seat anticipated. There are no E01 to E10 or E12 findings, and S072 raises no W02 (its teaches is long). The W04 lines are the same as the control.

### F8. Falsification: mutants on scratch copies of the appended tree
Each mutant changes one property of the appended rows. Each probe fired its own code, and only the expected finding changed.
- M0: stub file at `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (scratch only). Output `file	ok	…/m0/corpus/SOURCES.md`, `exit=0`. E11 clears, so it is exactly the missing entry.
- M1: stray `|` inside S072 teaches. Output `file	E01	S072 fields=12`, `exit=1`.
- M2: trailing pipe removed from S071. Output `file	E01	S071 fields=10`, `exit=1`.
- M3: duplicate S072 row. Output `file	E03	S072 duplicate id`, `exit=1`.
- M4: S071 `opened` set to 2026-10-29. Output `file	E08	S071 opened=2026-10-29`, `exit=1`.
- M5: S072 tier `Z`. Output `file	E06	S072 tier=Z`, `exit=1`.
- M6: S072 teaches replaced with ` thin `. Output `file	W02	S072 thin reject reason`, `exit=1`. W02 fires only under 8 characters, so the first probe (`too short`, 9 characters) was a mis-set probe and was not counted.
- M7: S071 kind `community` at tier A. Output `file	E10	S071 community-at-A`, `exit=1`.

### F9. Frozen C2 gate: G3 and G7 on the scratch tree
Command: loaded `corpus/instruments/r45-c2-gate.py` and called `g3(root)` and `g7(root)` only. Other gates need the F27 frontier row and entry, which belong to other seats.
Output on the appended tree: `G3 (False, 'bad=used-by')`, `G7 (False, 'census-rc=1')`.
Output with the M0 stub: `G7 (True, 'census-rc=0')`; `G3` still `bad=used-by`.
Reading: G3's bad list contains only `used-by`. The 11-cell count, tier A, status mined, `opened` 2026-10-28, URL in the source cell, and full sha in the anchor all pass. The `used-by` failure is caused by `entry_path()` needing an F27 frontier row in `corpus/README.md` that names an existing knowledge file. `grep -n -E '^\| F27 ' corpus/README.md` prints nothing, so that row is not in the lane yet. This is a cross-seat dependency, not a defect in the drafted rows.

### F10. Knowledge path absent
Command: `ls corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`
Output: `ls: cannot access 'corpus/knowledge/linux-kernel-security-bugs-reporting-process.md': No such file or directory`

### F11. Contract conflict on `REJECTED:` (for L1 decision)
The seat spec says `REJECTED:` is not needed because status carries it. CORPUS.md (SOURCES.md contract, `teaches`) says rejected rows read `REJECTED: <reason>; flip: <what would change the verdict>`. The live rows S026, S027, S028, S070 all follow the contract. The draft S072 teaches therefore keeps `REJECTED:` and `flip:`, and opens with `supersedes S070 —` as Rule 2 requires. L1 should confirm which reading governs.

## Draft rows (as written to `.ufo/waves/round-45/wave1/R45ScribeRowsA.draft/rows.md`)
- S071: source Linux kernel security-bugs reporting process (`https://docs.kernel.org/process/security-bugs.html`); kind docs; tier A; scope the kernel security team's own intake and embargo rules only; anchor headings, RST source, last-modified 2026-08-09, capture path, fetched 2026-10-28T20:52:44Z, sha256 0918dcfa…346f40, 20152 bytes, 372 lines; teaches: address the report to maintainers, state an exact version or commit ID, and expect a fix embargo of at most 7 calendar days, extendable to 14 by agreement; status mined; opened 2026-10-28; recheck 180d; used-by `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`.
- S072: source Google Bug Hunters Rules directory, readable article-API capture (API URL as specified); kind docs; tier B; scope the directory's overview table; anchor section line numbers, capture path, sha256 364166c4…a025, raw JSON with body 10029 characters, fetched 2026-10-28T20:53:00Z; teaches `supersedes S070 — REJECTED:` with the readable body reason, the S069 Q5 restatement and a `flip:` clause; status rejected; opened 2026-10-28; recheck 180d; used-by `—`.

## Hand-off
- L1 appends the two rows after the S070 line (validated position: after line 76, giving lines 77 and 78).
- L1 or the F27 entry seat writes `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`, and the F27 frontier row must name that same path. Then E11 clears (M0) and G3 can pass.
- The round lesson `## Gate` must record, for S071, the URL, the access date, and a quote of at most 25 words with its location (CORPUS rule 1). This is not drafted here.
- Before the frozen C2 gate G7 can exit 0, E11 must clear.

## Limitations
- Sources were verified from pinned captures and the manifest only. No network fetch ran, so the captures were not re-fetched.
- S070's claim that the HTML directory body is a JavaScript shell was not re-verified. The lane holds no capture for S070; `corpus/source-snapshots/round-44/` contains only S069. The S072 supersession is therefore scoped to the article-API route, which I did verify.
- Tier B for S072 is a judgment: a Google-authored overview that restates the linked per-program rules pages is secondary to them. A tier C reading would also pass validation.
- The S072 source cell uses the API URL, as specified. The S070 row uses the HTML URL. Both are recorded, and the row does not dedupe as a duplicate URL.
- The scratch root and the `--today` date were set explicitly (`--today 2026-10-28`) so that E08 is judged against the seat date.
- I did not run `r45-routed-defects.py` (C1) or the other gates of `r45-c2-gate.py`; those belong to other seats. I ran only G3 and G7 because they read my rows.
- Scratch under `/fast/scratch/hyaku/kasegi-r45/R45ScribeRowsA` was removed. Output above is quoted from the run; no `/tmp` path is cited as evidence.
