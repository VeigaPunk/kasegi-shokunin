VERDICT: INFO

The article-API URL for S072 avoids a within-scope duplicate-URL error (E04) against S070. Repeating S070's own page URL in that same scope also avoids E04, because S070 is `rejected` and E04 does not arm off a rejected row. A used-by path that is not on disk is an error only when the row's status is `mined`: census prints E11 and exits 1. The same missing path on a `rejected` or `queued` row is not an error.

## Setup

Scratch copy: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 8cf62c879e6e6b031e67412f8fac1fba0bd378cf | tar -x` into `/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree` (`TMPDIR` set to that scratch's `tmp`). Commit subject printed by `git log -1`: `8cf62c879e6e6b031e67412f8fac1fba0bd378cf round-45: freeze claims C1/C2, counters, controls, S071/S072 captures`.

`corpus/SOURCES.md` sha256 `84cf5e2e4c5d41f073ce7bb09730ad27d59660dfe694154765b38111e7dc4e91` is identical for the archive, `git show 8cf62c87:corpus/SOURCES.md`, and the lane worktree. Registry rows in that file: 70, last row S070 at `corpus/SOURCES.md:76`. Appended probes were inserted immediately before `## Paths` (`corpus/SOURCES.md:78`), still inside `## Registry`. Every appended line splits to 13 `|` fields (11 cells). Host UTC date during the runs: `2026-10-28`. The census command was the seat command, with no `--today`. Stderr was empty on every run. The archive tree's `corpus/SOURCES.md` inode and sha256 were unchanged after the probes.

S070 source cell, first URL `https://bughunters.google.com/about/rules/about-this-section`. Scope cell: `Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata`. Status cell: `rejected`. Tier cell: `C`. Used-by cell: `—` (U+2014). S069 is `mined`, tier A, first URL `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`.

Path check in that tree:

```
ls -l /fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
-rw-r--r-- 21 vgpnk vgpnk 5843 Oct 28 17:55 /fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
```

```
ls -l /fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
ls: cannot access '/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/knowledge/linux-kernel-security-bugs-reporting-process.md': No such file or directory
```

(`echo $?` after that `ls` printed `2`.)

Census URL key is the first `http(s)` URL in the source cell only (`scripts/sources-census.sh:600-605`). Anchor text is not the key. Below, "page URL" means S070's directory URL and "article-API URL" means `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section`.

## Do-nothing control

Unmodified archive registry. Command:

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/SOURCES.md`

Exit 0. Stdout:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/tree/corpus/SOURCES.md
```

Those two W04 bodies are the same two lines already recorded in `.ufo/waves/round-45/controls/sources-census-before.txt` (that file's lane column is `kasegi` and its ok-path is the lane worktree; this run's lane column is `file` because `--file` sets the lane name in `scripts/sources-census.sh:500-503`). Every probe below keeps both W04 lines. A shape "matches control" when its stdout is those two lines plus `file	ok	<that file>` and exit 0.

## Plausible S071 (tier A, mined) + S072 (tier B, rejected, article-API URL)

Appended lines (11 cells each):

```
| S071 | Linux kernel security-bugs — https://docs.kernel.org/process/security-bugs.html | docs | A | the kernel security team's own report-intake and embargo rules only | Reporting security bugs; capture corpus/source-snapshots/round-45/S071.txt fetched 2026-10-28T20:52:44Z sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40 20152 bytes 372 lines | the kernel security team's own report-intake and embargo rules | mined | 2026-10-28 | 180d | corpus/knowledge/linux-kernel-security-bugs-reporting-process.md |
| S072 | Google Bug Hunters Rules directory — https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section | docs | B | Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata | article API capture corpus/source-snapshots/round-45/S072.txt fetched 2026-10-28T20:53:00Z sha256 364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025 10032 bytes 312 lines | supersedes S070 — the body is readable through the article API and is an overview table, not an operative rule beyond the linked program text | rejected | 2026-10-28 | 180d | — |
```

Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/plausible/corpus/SOURCES.md`

Exit 1. Stdout:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
```

Delta against the control: the `ok` line is gone, exit goes 0 to 1, and one new line appears: E11 on S071. No E03, no E04, no new W04. S072 (new id, article-API URL, same scope as S070, `rejected`, teaches begins `supersedes S070`, used-by `—`) adds no finding.

## What each shape added

`—` below means the stdout matched the control (two pre-existing W04 lines, `ok`, exit 0). New lines are the only lines beyond that pair.

| shape | row under test | new finding | exit |
|---|---|---|---|
| control | none | — | 0 |
| plausible | S071 A mined, kernel URL, missing used-by; S072 B rejected, article-API URL, S070 scope, `supersedes S070` | `E11 S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` | 1 |
| api-mined-samescope | S072 B mined, article-API URL, S070 scope, teaches has no `supersedes`, used-by exists | — | 0 |
| html-mined-samescope | S072 B mined, page URL, S070 scope, no `supersedes`, used-by exists | — | 0 |
| html-rejected-samescope | S072 B rejected, page URL, S070 scope, no `supersedes` | — | 0 |
| html-queued-samescope | S072 B queued, page URL, S070 scope, no `supersedes` | — | 0 |
| html-mined-samescope-supersedes | S072 B mined, page URL, S070 scope, teaches `supersedes S070 — corrected directory reject while repeating the page url` | — | 0 |
| html-mined-diffscope | S072 B mined, page URL, scope `rules-directory overview table only` | `W04 S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes` | 0 |
| api-mined-diffscope | S072 B mined, article-API URL, that other scope | — | 0 |
| pos-e04-s069 | S072 B mined, S069's URL and S069's scope, no `supersedes` | `E04 S072 duplicate url bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules within scope Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule` | 1 |
| pair-html-then-html | S071 A mined then S072 B mined, both page URL and S070 scope, no `supersedes` | `E04 S072 duplicate url bughunters.google.com/about/rules/about-this-section within scope Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata` (no E04 on S071) | 1 |
| pair-html-then-api | same S071 mined page-URL holder, then S072 B mined article-API URL, S070 scope | — | 0 |
| pair-html-then-html-supersedes | same mined page-URL holder, then S072 B mined page URL whose teaches is `supersedes S070 — second mined row repeating the page url` | — | 0 |
| dup-id | two mined rows both id S071, different URLs, used-by exists | `E03 S071 duplicate id` | 1 |
| mined-missing | S071 A mined, kernel URL, missing used-by | `E11 S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` | 1 |
| mined-exists | S071 A mined, kernel URL, used-by the existing Google Cloud VRP entry | — | 0 |
| rejected-missing | S072 B rejected, article-API URL, used-by the missing kernel path | — | 0 |
| queued-missing | S071 A queued, kernel URL, used-by the missing kernel path | — | 0 |
| mined-emdash | S071 A mined, kernel URL, used-by `—` | `W03 S071 mined but unused` | 0 |
| s069-url-first | S072 B mined, S069 scope; source cell lists S069's URL first and the article-API URL second | same E04 as pos-e04-s069 | 1 |
| api-url-first-s069-later | S072 B mined, S069 scope; source cell lists the article-API URL first and S069's URL second | — | 0 |

E03 does not fire for a first use of S071 or S072 (they are absent from the 70-row registry). E04 against S070's page URL does not fire for a mined, queued, or rejected S072 in S070's scope. It fires once a prior non-rejected row holds that same URL and scope (`pair-html-then-html`: S071 is that prior; S070 is not). In that armed case the article-API URL still produces no E04 (`pair-html-then-api`), and a teaches cell matching `supersedes S070` also suppresses E04 (`pair-html-then-html-supersedes`). W04 fires for the page URL only when the scope string differs, and that warning still exits 0 (`html-mined-diffscope` prints `ok`). The article-API URL does not trip W04 against S070 in either scope.

A missing used-by path is an error for `mined` (E11, exit 1, no `ok` line) and is not an error for `rejected` or `queued`. A mined row whose used-by is `—` warns W03 and still exits 0. The plausible pair therefore fails census only because S071 is `mined` before `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` exists. The same S071 row with an existing used-by path exits 0.

The census keys the first URL in the source cell. Listing the article-API URL second does not avoid a duplicate that the first URL triggers (`s069-url-first` vs `api-url-first-s069-later`, armed against mined S069 because rejected S070 cannot arm E04).

Predicate the runs are discriminating, not a substitute for them (`scripts/sources-census.sh:641-654`, `:559-567`, `:737-745`, `:803-806`): E03 is a repeated id; W04 is the same normalized URL in a new scope and does not set the failure bit; E04 requires the same URL and scope, a prior non-rejected holder, this row not `rejected`, and teaches not matching `supersedes S` plus three digits; E11 is `status = mined` and `[ ! -e "$dir/$path" ]`. Header at `scripts/sources-census.sh:16-18` says exit 0 covers warnings and exit 1 covers E-findings. The runs match that: W03 and W04 exit 0; E03, E04, and E11 exit 1.

## Exact stdout

Paths below are `/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/<shape>/corpus/SOURCES.md`. Command for each: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <that path>`. Control path is the `tree` path quoted above.

api-mined-samescope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/api-mined-samescope/corpus/SOURCES.md
```

html-mined-samescope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/html-mined-samescope/corpus/SOURCES.md
```

html-rejected-samescope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/html-rejected-samescope/corpus/SOURCES.md
```

html-queued-samescope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/html-queued-samescope/corpus/SOURCES.md
```

html-mined-samescope-supersedes, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/html-mined-samescope-supersedes/corpus/SOURCES.md
```

html-mined-diffscope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/html-mined-diffscope/corpus/SOURCES.md
```

api-mined-diffscope, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/api-mined-diffscope/corpus/SOURCES.md
```

pos-e04-s069, exit 1:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E04	S072 duplicate url bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules within scope Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule
```

pair-html-then-html, exit 1:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E04	S072 duplicate url bughunters.google.com/about/rules/about-this-section within scope Whether the general rules directory itself supplies operative scope rules beyond its navigation and metadata
```

pair-html-then-api, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/pair-html-then-api/corpus/SOURCES.md
```

pair-html-then-html-supersedes, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/pair-html-then-html-supersedes/corpus/SOURCES.md
```

dup-id, exit 1:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E03	S071 duplicate id
```

mined-missing, exit 1:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S071 missing used-by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
```

mined-exists, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/mined-exists/corpus/SOURCES.md
```

rejected-missing, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/rejected-missing/corpus/SOURCES.md
```

queued-missing, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/queued-missing/corpus/SOURCES.md
```

mined-emdash, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W03	S071 mined but unused
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/mined-emdash/corpus/SOURCES.md
```

s069-url-first, exit 1:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E04	S072 duplicate url bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules within scope Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule
```

api-url-first-s069-later, exit 0:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus/v/api-url-first-s069-later/corpus/SOURCES.md
```

## Limitations

The E04 line names the new row, the normalized URL, and the scope. It does not name the prior id. "Against S070" is the case where S070 is the only earlier row with that URL and scope (`html-mined-samescope` and the other single-row page-URL shapes). The armed case is a separate appended mined row (`pair-html-then-html`), not an in-place edit of S070.

Probes did not vary trailing slash, fragment, or host case. They did not run `sources-census.sh` in fleet-roster mode. `--file` labels the lane `file`. Opened dates are `2026-10-28`, equal to the host UTC date of these runs; the seat command does not pass `--today`.

Scratch `/fast/scratch/hyaku/kasegi-r45/R45ScoutCensus` was removed after these outputs were copied here. No lane file other than this report was written. No git or jj mutation.
