# R44W2Scout02 — registry recon (`corpus/SOURCES.md`, `5ab3a60` → `8063547`)

- seat: `R44W2Scout02` (scout, read-only); lane: kasegi; round 44 attempt 2, wave 2 (falsify)
- item: diff `corpus/SOURCES.md` between frozen base `5ab3a60` and commit `8063547`; report every row added or changed, the per-line diff, and the row count before and after. Expected shape: S069 added, S070 added, one used-by line added, and no pre-existing status/recheck/used-by cell modified.
- frozen base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (ancestor of the target; `git merge-base --is-ancestor` exit 0)
- target: `8063547d0ce647d6f9eafc3c8d0a502616685218` (`git rev-parse HEAD` in `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)
- parent of the target: `66314015122b9aa32dc40f2f1815df56624c26d1`
- blobs: base and parent both `corpus/SOURCES.md` = `c491c1270870485a76cdbca1bea2462f9cc1a7e7`; target = `b577281010f4082dfac075b4ad86c5951472ec2c`
- content sha256 (`git show` bytes): base `fd96d38b03585db8952740958e87db6aa0a4b54f0abb30d9ca3f9a7a1b60c358`; target `84cf5e2e4c5d41f073ce7bb09730ad27d59660dfe694154765b38111e7dc4e91`
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44W2Scout02/` (created with `mkdir -p`; removed before yield)
- edits: this report only. No production file, no other seat's file, no git/jj mutation.
- tooling: no install. Census used stock `git` 2.56.0 and `python3` 3.14.8 already on the host. `RULES.md` was not applied because nothing was installed.
- section 6 of `corpus/lessons/round-43-verifier-spotcheck.md` was read (eight routed defects). This item does not re-grade them and does not score C1 or C2.

## Result

**Registry rows: the expected shape holds.** From `5ab3a60` to `8063547`, `corpus/SOURCES.md` adds `S069` and `S070` and no other registry row. The C2 row pattern goes from 68 to 70. All 68 pre-existing rows stay on the same lines (7–74) and are byte-identical, so no pre-existing status, recheck, or used-by cell is modified. No row is deleted.

**Whole-file diff: seven insertions, zero deletions — more than two rows plus one used-by line.** The single new used-by line is the `## Paths` bullet at line 86, which cites `S069`. The same patch also appends a Search log bullet (line 105), a Registry changes bullet (line 154), and two blank lines (106 and 153). Those four lines are not registry rows and do not edit a pre-existing cell. `claims.json` does not say the patch contains only three lines; this seat does not turn the extra log lines into a C1 or C2 failure.

Nothing here falsifies the row constraint. A claim that this commit's `SOURCES.md` diff is only `S069`, `S070`, and one path line would be false, because of the two log bullets and two blank lines.

## Row count

| census | `5ab3a60` | `8063547` |
|---|---:|---:|
| `wc -l` on `git show <rev>:corpus/SOURCES.md` | 147 | 154 |
| C2 source-row grep (command in Commands) | 68 | 70 |
| lines that start with a pipe (header + separator + data rows) | 70 | 72 |
| registry data rows `^\\| S[0-9]+ \\|` | 68 | 70 |

`git diff --numstat 5ab3a60 8063547 -- corpus/SOURCES.md` → `7	0	corpus/SOURCES.md`.

Only one commit in `5ab3a60..8063547` touches the file:

```
8063547d0ce647d6f9eafc3c8d0a502616685218 round-44: land the eight routed round-43 defects, the fail-closed C1 counter, the C2 frontier counter and the wave registry emitter
```

The parent blob equals the base blob, so the whole range diff is exactly that commit. Working tree matches the target for this path: `git status --porcelain -- corpus/SOURCES.md` is empty and `git diff --exit-code 8063547 -- corpus/SOURCES.md` exits 0.

Id order of `S001`–`S068` is unchanged, including the pre-existing inversion where `S057` (line 62) precedes `S056` (line 63). Added ids, in order, are only `S069` (line 75) and `S070` (line 76). Removed ids: none. Rows whose full line text differs: none. Rows whose line number moved: none.

Lines 1–74 of the two blobs are identical. Every base line still occurs in the target at least as many times (lines with a decreased count: none). Blank-line count 15 → 17 (delta 2).

## Per-line diff

`git diff -U0 --no-color 5ab3a60 8063547 -- corpus/SOURCES.md` is four pure-insertion hunks. Lengths below are the line text without the trailing newline. No `-` body line exists.

| new line | git hunk | section in the target | what | chars |
|---:|---|---|---|---:|
| 75 | `@@ -74,0 +75,2 @@` | `## Registry` | S069 | 996 |
| 76 | `@@ -74,0 +75,2 @@` | `## Registry` | S070 | 656 |
| 86 | `@@ -83,0 +86 @@` | `## Paths` | bullet | 239 |
| 105 | `@@ -101,0 +105,2 @@` | `## Search log` | bullet | 1099 |
| 106 | `@@ -101,0 +105,2 @@` | `## Search log` | blank | 0 |
| 153 | `@@ -147,0 +153,2 @@` | `## Registry changes` | blank | 0 |
| 154 | `@@ -147,0 +153,2 @@` | `## Registry changes` | bullet | 857 |

Hunk headers as git printed them (the text after `@@` is git's function-line context, not a changed line):

- `@@ -74,0 +75,2 @@` — 2 added line(s), first new line 75
- `@@ -83,0 +86 @@` — 1 added line, first new line 86
- `@@ -101,0 +105,2 @@` — 2 added line(s), first new line 105
- `@@ -147,0 +153,2 @@` — 2 added lines, first new line 153. After the header git prints function context, truncated at `policy_ve`, from the pre-existing S043 change-log line (`corpus/SOURCES.md:120` in the target). That context is not a diff body line. The S043 sentence is byte-identical at base and target.

### Added lines

#### target line 75 (996 chars) under `## Registry`

```
| S069 | Google Cloud Vulnerability Reward Program Rules — https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules | docs | A | Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule | Rules of Engagement: Disqualifying Actions & Boundaries; “Do Not Test Customer Projects & Resources”; official article API capture at corpus/source-snapshots/round-44/S069.txt, fetched 2026-10-28T18:53:38Z; sha256 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2; Q1–Q3 lines 61–72, Q4 lines 76–77, Q5 lines 9–11; capture body extracted from preserved API JSON via `jq -r '.body'` | Google states its Cloud VRP is limited to Google-owned infrastructure, prohibits customer-resource testing, and makes reports ineligible for rewards when finding or verifying involved customer resources | mined | 2026-10-28 | 180d | corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md |
```


#### target line 76 (656 chars) under `## Registry`

```
| S070 | Google Bug Hunters Rules directory — https://bughunters.google.com/about/rules/about-this-section | docs | C | Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata | meta description, opened 2026-10-28: “Welcome to Google's Bug Hunting community, learn more about hunting & reporting bugs you’ve found in Google products.” | REJECTED: the page's accessible body is a JavaScript shell and its metadata is a directory welcome, not an operative program rule; flip: the page itself exposes a located, program-specific rule absent from the linked policy text. | rejected | 2026-10-28 | 180d | — |
```


#### target line 86 (239 chars) under `## Paths`

```
- Google Cloud VRP customer-resource boundary — S069: read this program's stated product scope before its customer-resource prohibition and reward-ineligibility rule; do not generalize the program text into authorization for other targets.
```


#### target line 105 (1099 chars) under `## Search log`

```
- Google Cloud VRP customer-resource boundary sweep (round 44); question: does a first-party program distinguish Google-owned infrastructure from customer-owned Cloud resources and specify reward eligibility for testing those resources? Where: the official Cloud VRP rules page at `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`, its first-party article API `https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules` captured to `corpus/source-snapshots/round-44/S069.txt`, and the general Rules directory page at `https://bughunters.google.com/about/rules/about-this-section`; date 2026-10-28. Identified 2, screened 2, included 1 as S069 and rejected 1 as S070. The source capture contains the located customer-resource prohibition and reward-ineligibility text; the directory page exposes only navigation/metadata, so it is not admitted as an operative rule. Stop: the direct Cloud VRP rules and capture answer the bounded program-scope question; no target-facing testing was attempted.
```


#### target line 106 (0 chars) under `## Search log`

Empty line.

#### target line 153 (0 chars) under `## Registry changes`

Empty line.

#### target line 154 (857 chars) under `## Registry changes`

```
- Round 44 source/frontier addition: S069 is the tier-A, mined Google Cloud VRP rules page; S070 is the tier-C rejected directory page. S069's canonical source URL remains the row URL; the manifest records the article API separately as `capture_url`/`http.final_url`. Its pinned text was extracted from the preserved raw API JSON by `jq -r '.body' .ufo/waves/round-44/source-recon/S069.txt > corpus/source-snapshots/round-44/S069.txt`; `source-recheck.py` resolves Q1–Q5 in the pinned text. The cited snapshot has sha256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2` (45,681 bytes, 1,132 lines). The live API later returned formatting differences; the digest is the dated capture, not a claim of byte-stable live responses. Registry rows 68→70; F26 is the sole new admitted frontier. No pre-existing status/recheck/used-by cell changed.
```


### Blank-line alignment

The two empty additions are real (blank count 15 → 17) but one of them sits next to a pre-existing empty line, so two diff algorithms name different line numbers for that one blank:

- `git diff` (the per-line diff above): after base line 101, new line 105 is the Search log bullet and new line 106 is empty. New line 104 is the old blank that followed the RFC 9116 bullet, shifted by the three earlier insertions.
- `difflib.SequenceMatcher` (autojunk off), insert line numbers: 75, 76, 86, 104, 105, 153, 154. It treats new line 104 as the inserted blank and new line 106 as the old blank.

The committed bytes are the same either way: line 103 is the unchanged RFC 9116 bullet, line 104 is empty, line 105 is the new Search log bullet, line 106 is empty, line 107 is `## Leads (unopened)`. Non-blank additions are lines 75, 76, 86, 105, and 154 in both alignments.

The end-of-file blank is not ambiguous. Base line 147 is the round-43 registry bullet and the file ends there. Target lines 153 (empty) and 154 (round-44 bullet) are both new. The target still ends with that bullet plus a single newline, not an extra trailing blank (`tail` bytes end `changed.\n`).

## New rows, cell by cell

Header is target line 5, unchanged, 11 cells: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`. Both new rows split into 11 cells (no extra `|` inside a cell).

### S069 — `corpus/SOURCES.md:75`

| cell | value |
|---|---|
| id | S069 |
| source | Google Cloud Vulnerability Reward Program Rules — https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules |
| kind | docs |
| tier | A |
| scope | Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule |
| anchor | Rules of Engagement: Disqualifying Actions & Boundaries; “Do Not Test Customer Projects & Resources”; official article API capture at corpus/source-snapshots/round-44/S069.txt, fetched 2026-10-28T18:53:38Z; sha256 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2; Q1–Q3 lines 61–72, Q4 lines 76–77, Q5 lines 9–11; capture body extracted from preserved API JSON via `jq -r '.body'` |
| teaches | Google states its Cloud VRP is limited to Google-owned infrastructure, prohibits customer-resource testing, and makes reports ineligible for rewards when finding or verifying involved customer resources |
| status | mined |
| opened | 2026-10-28 |
| recheck | 180d |
| used-by | corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md |

### S070 — `corpus/SOURCES.md:76`

| cell | value |
|---|---|
| id | S070 |
| source | Google Bug Hunters Rules directory — https://bughunters.google.com/about/rules/about-this-section |
| kind | docs |
| tier | C |
| scope | Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata |
| anchor | meta description, opened 2026-10-28: “Welcome to Google's Bug Hunting community, learn more about hunting & reporting bugs you’ve found in Google products.” |
| teaches | REJECTED: the page's accessible body is a JavaScript shell and its metadata is a directory welcome, not an operative program rule; flip: the page itself exposes a located, program-specific rule absent from the linked policy text. |
| status | rejected |
| opened | 2026-10-28 |
| recheck | 180d |
| used-by | — |

`S069` is tier A, status `mined`, recheck `180d`, opened `2026-10-28`, used-by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`.

`S070` is tier C, status `rejected`, recheck `180d`, opened `2026-10-28`, used-by `—` (one em dash, not a knowledge path).

## Pre-existing status / recheck / used-by

No pre-existing cell was modified. Proof is stronger than a three-column check: for each of `S001`–`S068`, the entire registry line is byte-identical at the same line number in both blobs (lines 7–74). Status (column 8), recheck (column 10), and used-by (column 11) therefore cannot have changed, and neither can kind, tier, scope, anchor, teaches, or opened.

The one new used-by line in the sense of the expected checklist is the Paths bullet at line 86. It names `S069` only. It does not append a path onto any older row. `S070` adds no used-by path.

The new Registry changes bullet (line 154) says "Registry rows 68→70" and "No pre-existing status/recheck/used-by cell changed." The independent census agrees with that sentence. Agreement is not extra evidence about the Google capture; it only means the log line matches the row diff.

## Expectation check

| expected | result |
|---|---|
| S069 added | yes, line 75, one row, not present at base |
| S070 added | yes, line 76, one row, not present at base |
| one used-by line added | yes, if this means the new Paths bullet (line 86). No pre-existing used-by cell was edited. `S069`'s used-by cell is part of the new row, not a separate line. |
| no pre-existing status/recheck/used-by cell modified | confirmed, all 68 prior rows, all 11 cells |

Not named by that checklist, and present anyway: Search log bullet line 105 (1099 chars), Registry changes bullet line 154 (857 chars), empty lines 106 and 153.

## Commands

Run from a shell whose `git -C` target was `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (`git rev-parse --show-toplevel` printed that path). Reads only.

```
git rev-parse HEAD
git rev-parse 5ab3a60^{commit}
git rev-parse 8063547^{commit}
git merge-base --is-ancestor 5ab3a60 8063547
git log --format='%H %s' 5ab3a60..8063547 -- corpus/SOURCES.md
git rev-parse 5ab3a60:corpus/SOURCES.md
git rev-parse 66314015122b9aa32dc40f2f1815df56624c26d1:corpus/SOURCES.md
git rev-parse 8063547:corpus/SOURCES.md
git diff --numstat 5ab3a60 8063547 -- corpus/SOURCES.md
git diff -U0 --no-color 5ab3a60 8063547 -- corpus/SOURCES.md
git show 5ab3a60:corpus/SOURCES.md | wc -l
git show 8063547:corpus/SOURCES.md | wc -l
git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
git status --porcelain -- corpus/SOURCES.md
git diff --exit-code 8063547 -- corpus/SOURCES.md
```

Observed: HEAD `8063547d0ce647d6f9eafc3c8d0a502616685218`; ancestor check exit 0; numstat `7	0	corpus/SOURCES.md`; `wc -l` 147 and 154; C2 grep 68 and 70; status porcelain empty; worktree diff exit 0. Blob ids are in the header of this report.

The row-identity check was a Python 3 comparison of the two `git show` blobs: regex `^\| (S\d+) \|`, full-line equality, and `difflib.SequenceMatcher(..., autojunk=False)`. No package was installed.

## Limitations

- Did not fetch the Google URLs, hash `corpus/source-snapshots/round-44/S069.txt`, or run `source-recheck.py`. Row text is what the commit contains; this item does not re-verify the capture.
- Did not run `corpus/instruments/r44-routed-defects.py`, `r44-frontier-count.py`, or `wave-registry.py`, and did not score C1 or C2.
- Did not re-grade the eight routed defects in `corpus/lessons/round-43-verifier-spotcheck.md` §6. They were read so this recon would not wander into them.
- Which of the two adjacent empty lines in the Search log is "the" inserted blank depends on the diff algorithm. Non-blank line numbers and the row census do not.
- Pipe-splitting was used only to describe the two new rows. The no-edit result for `S001`–`S068` does not depend on splitting, because the full lines match.
