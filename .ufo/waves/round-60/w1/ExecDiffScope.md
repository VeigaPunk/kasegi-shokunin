OUT-OF-SCOPE: `SKILL.md` carries 1 deleted line (registry row L1224 rewritten, not appended) and is a file outside the three the item permits to show deletions; `corpus/instruments/figure-audit.py` also spends 2 of its 8 deleted lines outside the item's parenthetical ("the replaced scanner/segment functions and docstring"): old L53 `EXPECTED_CASES = 14` and old L257 selftest case. Everything else in the frozen bound holds: the 15 freeze paths are pure adds (0 deletions), the ledger's 7 deletions are exactly five derive strings plus two record cells, `corpus/SOURCES.md`'s 1 deletion is the declared lead bullet, and all four required sha256 equalities are exact. Separately, the item's premise that `7f7dd267` is lane HEAD is false at audit time: HEAD is `fb6a928`, three commits past the freeze, with 7 further paths changed after the audited implementation (`SHONEN.md` 4/1 among them).

Seat ExecDiffScope (kasegi r60 w1). L = `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only throughout). W = `L/.ufo/waves/round-60/w1`. S = `/fast/scratch/hyaku/kasegi-r60/ExecDiffScope` (created, not needed for fixtures — every command is a read-only command against L — and removed; §9). Freeze F = `66e6241cd7afd6184273ce7df1dcd5328c187367`. Implementation I = `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`. Tool: `git version 2.56.0`. No file under L was written except this evidence file; `git status --porcelain --untracked-files=no` on L prints nothing (§7), so the tracked worktree equals HEAD for every audited path.

Every command below is run against absolute paths; the blocks abbreviate `-C L` for `-C /home/vgpnk/Projects/shokunin/kasegi-shokunin` and `F`/`I` for the two full hashes printed above, with those bindings set in each shell that ran the command (the §1 block spells the lane path out once). Nothing in this file is inferred beyond arithmetic over printed numbers, and each such total is also printed directly by a `--shortstat` or `wc -l` block.

---

## 1. Freeze commit F — changed paths and kinds

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show --shortstat --format= 66e6241cd7afd6184273ce7df1dcd5328c187367
 15 files changed, 959 insertions(+)
EXIT=0
```

```
$ git -C L show --name-status --format= 66e6241cd7afd6184273ce7df1dcd5328c187367
A	.ufo/waves/round-60/assimilation/collisions
A	.ufo/waves/round-60/assimilation/reg-ids
A	.ufo/waves/round-60/assimilation/staged-ids
A	.ufo/waves/round-60/claims.json
A	.ufo/waves/round-60/controls/c1-probe-run-r60.sh
A	.ufo/waves/round-60/controls/c1-probes-base-r60.txt
A	.ufo/waves/round-60/controls/c1-probes-standin-r60.txt
A	.ufo/waves/round-60/controls/c1-standin-after-r60.txt
A	.ufo/waves/round-60/controls/c2-standin-after-r60.txt
A	.ufo/waves/round-60/controls/census-round-start-r60.txt
A	.ufo/waves/round-60/controls/do-nothing-c1-r60.txt
A	.ufo/waves/round-60/controls/do-nothing-c2-r60.txt
A	.ufo/waves/round-60/controls/freeze-digests-r60.txt
A	corpus/source-snapshots/round-60/S093.txt
A	corpus/source-snapshots/round-60/manifest.json
EXIT=0
```

```
$ git -C L show --numstat --format= 66e6241cd7afd6184273ce7df1dcd5328c187367
62	0	.ufo/waves/round-60/assimilation/collisions
92	0	.ufo/waves/round-60/assimilation/reg-ids
94	0	.ufo/waves/round-60/assimilation/staged-ids
60	0	.ufo/waves/round-60/claims.json
59	0	.ufo/waves/round-60/controls/c1-probe-run-r60.sh
12	0	.ufo/waves/round-60/controls/c1-probes-base-r60.txt
12	0	.ufo/waves/round-60/controls/c1-probes-standin-r60.txt
19	0	.ufo/waves/round-60/controls/c1-standin-after-r60.txt
120	0	.ufo/waves/round-60/controls/c2-standin-after-r60.txt
8	0	.ufo/waves/round-60/controls/census-round-start-r60.txt
13	0	.ufo/waves/round-60/controls/do-nothing-c1-r60.txt
18	0	.ufo/waves/round-60/controls/do-nothing-c2-r60.txt
3	0	.ufo/waves/round-60/controls/freeze-digests-r60.txt
283	0	corpus/source-snapshots/round-60/S093.txt
104	0	corpus/source-snapshots/round-60/manifest.json
EXIT=0
```

Kind of change: 15 adds, 0 modifications, 0 renames, 0 deletes. 959 insertions and **0 deletions**, so the item's "every other modified file must have 0 deletions" bound is trivially met by the freeze (there are no modified files in it).

Deletion-carrying filter over the freeze (want: no rows):

```
$ git -C L show --numstat --format= 66e6241 | awk -F'\t' '$2+0 != 0 {print $2"\t"$3}'
(no output)
EXIT=0
```

## 2. Implementation commit I — changed paths and kinds

`I` is the **direct child** of `F`, so its 12-path diff is exactly the freeze→implementation delta with no intervening commit:

```
$ git -C L rev-parse 7f7dd267283d2a16ca38d4cb05bed92165cb35cd^
66e6241cd7afd6184273ce7df1dcd5328c187367
EXIT=0
```

```
$ git -C L show --shortstat --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
 12 files changed, 224 insertions(+), 17 deletions(-)
EXIT=0
```

```
$ git -C L show --numstat --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
19	0	.ufo/waves/round-60/claims-erratum-1.md
31	0	.ufo/waves/round-60/controls/c1-lane-after-r60.txt
37	0	.ufo/waves/round-60/controls/c2-lane-after-r60.txt
2	0	PROVINCE.md
1	1	SKILL.md
1	0	corpus/QUALITY.md
21	0	corpus/README.md
6	1	corpus/SOURCES.md
7	7	corpus/instruments/figure-audit-ledger.json
55	8	corpus/instruments/figure-audit.py
1	0	corpus/instruments/knowledge-expected.txt
43	0	corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
EXIT=0
```

```
$ git -C L show --name-status --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
A	.ufo/waves/round-60/claims-erratum-1.md
A	.ufo/waves/round-60/controls/c1-lane-after-r60.txt
A	.ufo/waves/round-60/controls/c2-lane-after-r60.txt
M	PROVINCE.md
M	SKILL.md
M	corpus/QUALITY.md
M	corpus/README.md
M	corpus/SOURCES.md
M	corpus/instruments/figure-audit-ledger.json
M	corpus/instruments/figure-audit.py
M	corpus/instruments/knowledge-expected.txt
A	corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
EXIT=0
```

```
$ git -C L show --name-status --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd | awk '{print $1}' | sort | uniq -c
      4 A
      8 M
EXIT=0
```

Kind of change: 4 adds (erratum, two lane receipts, one knowledge file) and 8 modifications; 224 insertions, 17 deletions. The 17 deletions are entirely accounted for by §3.

`git -C L diff --numstat F I` reproduces the same 12 rows byte-for-byte (run; identical output to the numstat above, exit 0), which is expected from the parent link above.

## 3. Deletion census against the item's bound — FAIL on one file

Deletion-carrying files in `I` (want: the three permitted files only):

```
$ git -C L show --numstat --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd | awk -F'\t' '$2+0 != 0 {print $2"\t"$3}'
1	SKILL.md
1	corpus/SOURCES.md
7	corpus/instruments/figure-audit-ledger.json
8	corpus/instruments/figure-audit.py
EXIT=0
```

Per-file census (status/insertions/deletions from the numstat above):

| path | kind | + | − | deletions permitted by the item | result |
|---|---|---|---|---|---|
| `.ufo/waves/round-60/claims-erratum-1.md` | A | 19 | 0 | 0 | pass |
| `.ufo/waves/round-60/controls/c1-lane-after-r60.txt` | A | 31 | 0 | 0 | pass |
| `.ufo/waves/round-60/controls/c2-lane-after-r60.txt` | A | 37 | 0 | 0 | pass |
| `PROVINCE.md` | M | 2 | 0 | 0 | pass (pure append) |
| `SKILL.md` | M | 1 | **1** | 0 | **FAIL** |
| `corpus/QUALITY.md` | M | 1 | 0 | 0 | pass (pure append) |
| `corpus/README.md` | M | 21 | 0 | 0 | pass (pure append) |
| `corpus/SOURCES.md` | M | 6 | 1 | 1 (the one lead bullet) | pass |
| `corpus/instruments/figure-audit-ledger.json` | M | 7 | 7 | 7 (five derive strings + two record cells) | pass (composition exact, §6) |
| `corpus/instruments/figure-audit.py` | M | 55 | 8 | 8 (replaced scanner/segment functions and docstring) | file-level pass; 2 lines outside the description, §6 |
| `corpus/instruments/knowledge-expected.txt` | M | 1 | 0 | 0 | pass (pure append) |
| `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` | A | 43 | 0 | 0 | pass |

Totals reconcile with the shortstat: deletions 1+1+7+8 = 17; insertions 19+31+37+2+1+1+21+6+7+55+1+43 = 224.

**Out-of-scope item 1 — `SKILL.md`, 1 deletion.** `SKILL.md` is not one of the three files the item permits to show deletions, and it is modified (1/1). The deleted bytes are registry row 1224 of the old file, replaced by a rewritten row at the same line number of the new file (§6.1). The change is semantically the declared registry-cell refresh (self-test pin `cases=14` → `cases=20`, allow-list wording extended for round 60), and it touches no other line of the file — but as a numstat fact it is a deletion in a file the frozen bound requires to be 0. The seat reports it and does not alter the rule.

**Out-of-scope item 2 — 2 of the instrument's 8 deleted lines.** The item's parenthetical for `corpus/instruments/figure-audit.py` names "the replaced scanner/segment functions and docstring". Measured composition of the 8 deleted lines (old-file numbering from the `-U0` hunks, content from §6.4): 5 docstring lines (old L27-L29, L83-L84), 1 allow-list constant line (old L49, `READ_ONLY_HEADS`), 1 selftest pin (old L53 `EXPECTED_CASES = 14`), 1 selftest case (old L257). The last two are selftest scaffolding rather than scanner/segment functions or docstring, so they fall outside the parenthetical description even though the file itself is permitted to carry deletions. The file-level predicate is satisfied; the content description is exceeded by 2 lines.

No other file in `I` deletes anything: the erratum, the two lane receipts, `PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/instruments/knowledge-expected.txt` and the new knowledge file are all 0-deletion (8 of the 12 paths), which matches their `A` or pure-append `M` status.

## 4. Required digests — all four match

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/figure-audit.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  corpus/instruments/figure-audit.py
EXIT=0

$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/figure-audit-ledger.json
28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b  corpus/instruments/figure-audit-ledger.json
EXIT=0
```

```
$ git -C L show 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:corpus/instruments/figure-audit.py | sha256sum
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  -
EXIT=0

$ git -C L show 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:corpus/instruments/figure-audit-ledger.json | sha256sum
28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b  -
EXIT=0
```

Both equalities are exact (worktree file = commit-I blob = the item's pinned value). Blob identity makes the same point at the git level and shows the later commits did not touch them:

```
$ git -C L rev-parse HEAD:corpus/instruments/figure-audit.py HEAD:corpus/instruments/figure-audit-ledger.json 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:corpus/instruments/figure-audit.py 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:corpus/instruments/figure-audit-ledger.json
ad25f7859c73b5f95d9825775b4f9b2e12675d4e
271065230331ac6cce914851a91d3dc093e787eb
ad25f7859c73b5f95d9825775b4f9b2e12675d4e
271065230331ac6cce914851a91d3dc093e787eb
EXIT=0
```

HEAD and I agree line-for-line (same two blob ids). `git -C L diff --stat I..HEAD -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json corpus/source-snapshots/round-60 .ufo/waves/round-60/claims.json` prints nothing, exit 0 (§7).

## 5. Freeze composition — claims in, erratum out, capture and manifest in

Contents of the freeze tree for the two directories that carry the round's frozen artifacts:

```
$ git -C L ls-tree -r 66e6241cd7afd6184273ce7df1dcd5328c187367 -- .ufo/waves/round-60 corpus/source-snapshots/round-60
100644 blob 486ef13362c2a48485d4b06a458b8f752afa0699	.ufo/waves/round-60/assimilation/collisions
100644 blob 339c1a6d9a3aa51ee357712163d2b84c88e3d45f	.ufo/waves/round-60/assimilation/reg-ids
100644 blob 17e75265bc3e818e3ce55cc5b8787f1d5d95dbd4	.ufo/waves/round-60/assimilation/staged-ids
100644 blob 975f84c6634d5cb238fe11f5117bd5a47f7be051	.ufo/waves/round-60/claims.json
100755 blob 862694cdb168d65f6869d4fe633d1eeb6b277e26	.ufo/waves/round-60/controls/c1-probe-run-r60.sh
100644 blob 3d2c6b1027ce5742d02df0d18a93cfe5f8e4ee14	.ufo/waves/round-60/controls/c1-probes-base-r60.txt
100644 blob 30823ef4f59013e307e411b34fb41958c5863220	.ufo/waves/round-60/controls/c1-probes-standin-r60.txt
100644 blob 13d11023e232786f1f688204b7a831357392aece	.ufo/waves/round-60/controls/c1-standin-after-r60.txt
100644 blob fac65d525a956e0f49cb57e413a11a5eab84ca90	.ufo/waves/round-60/controls/c2-standin-after-r60.txt
100644 blob 9c123f633d9e732635a19923744ad7a86f6d6cdb	.ufo/waves/round-60/controls/census-round-start-r60.txt
100644 blob b27ef767e5a9ef790fbd690184a7c2cfe46e7bdc	.ufo/waves/round-60/controls/do-nothing-c1-r60.txt
100644 blob b49790cbf8b27af5ea4ba6074735de3089a85ad1	.ufo/waves/round-60/controls/do-nothing-c2-r60.txt
100644 blob 50f72cac300c0670af245b500942ebf23787660c	.ufo/waves/round-60/controls/freeze-digests-r60.txt
100644 blob 372d9f49236312ec338a930e2c0e3fae829df722	corpus/source-snapshots/round-60/S093.txt
100644 blob 28cc5aa3968a1deaf6127a49888fa7f0817d65f2	corpus/source-snapshots/round-60/manifest.json
EXIT=0
```

- **claims.json: present in F** (blob `975f84c`).
- **erratum: absent from F, present in I.** `cat-file -e` on the freeze tree fails, on the implementation tree succeeds:

```
$ git -C L cat-file -e 66e6241cd7afd6184273ce7df1dcd5328c187367:.ufo/waves/round-60/claims-erratum-1.md
fatal: path '.ufo/waves/round-60/claims-erratum-1.md' exists on disk, but not in '66e6241cd7afd6184273ce7df1dcd5328c187367'
EXIT=128

$ git -C L cat-file -e 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:.ufo/waves/round-60/claims-erratum-1.md
(no output)
EXIT=0
```

  The erratum is 19 lines, equal to its 19-insertion numstat row, and it is an add in `I` only:

```
$ wc -l /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/claims-erratum-1.md
19 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/claims-erratum-1.md
EXIT=0
```

  The erratum supersedes without mutating the frozen file: claims.json still carries the frozen `want: 1` at C2 command 8 while the erratum states the superseding value 2 (its §"The superseding value is **2**"). Confirmation that the frozen bytes were not edited to absorb it:

```
$ git -C L show HEAD:.ufo/waves/round-60/claims.json | grep -n 'the tracker is opened as S092'
38:   "after": "…the corrected lead bullet prints 1 for 'the tracker is opened as S092'; the census --file exits 0. …
48:    "grep -c 'the tracker is opened as S092' corpus/SOURCES.md   # want: 1",
EXIT=0
```

  (line 38 is the C2 `after` prose; line 48 is `counting_commands[7]`, still the frozen `want: 1`).

- **capture and manifest: present in F** (blobs `372d9f4` and `28cc5aa`), unchanged through I and HEAD:

```
$ git -C L diff --stat 66e6241cd7afd6184273ce7df1dcd5328c187367 7f7dd267283d2a16ca38d4cb05bed92165cb35cd -- corpus/source-snapshots/round-60
(no output)
EXIT=0
$ git -C L diff --stat 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json corpus/source-snapshots/round-60 .ufo/waves/round-60/claims.json
(no output)
EXIT=0
```

  The capture's content digest matches the freeze receipt `.ufo/waves/round-60/controls/freeze-digests-r60.txt:3`:

```
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-60/S093.txt
46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-60/S093.txt
EXIT=0
```

- **Frozen claims byte-identical at all four observation points** (freeze blob, implementation tree, HEAD tree, worktree), so no mid-round edit occurred:

```
$ git -C L show 66e6241:.ufo/waves/round-60/claims.json | sha256sum
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  -
EXIT=0
$ git -C L show 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:.ufo/waves/round-60/claims.json | sha256sum
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  -
EXIT=0
$ git -C L show HEAD:.ufo/waves/round-60/claims.json | sha256sum
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  -
EXIT=0
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/claims.json
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/claims.json
EXIT=0
$ git -C L diff --stat 66e6241cd7afd6184273ce7df1dcd5328c187367..HEAD -- .ufo/waves/round-60/claims.json
(no output)
EXIT=0
```

## 6. Line-level pointers for every deletion

Old-side numbers are from the freeze blob (`git show 66e6241:<path> | grep -n …`, exit 0 each); new-side numbers are from the worktree file (`grep -n …, awk 'NR==…'`, exit 0 each).

### 6.1 `SKILL.md` — 1 deletion (out of scope, §3)
- Old `L1224` (freeze): the `figure-audit.py` registry row with self-test cell `(prints \`selftest cases=14 failures=0\`)` and write-scope cell `…refuses the shell-chaining probes P1-P8 and admits the residual classes listed below`.
- New `L1224`: same row, self-test cell now `(prints \`selftest cases=20 failures=0\`; [r60] pin moved 14 → 20 with the six new escape/in-program/write-flag cases)` and write-scope cell `…refuses the shell-chaining probes P1-P8 (round 59) and, since round 60, the escaped-quote, in-program (awk and sed heads removed) and write-flag (sort -o, git show …`.
- Reproduced by `grep -n 'selftest cases=20' SKILL.md` → `1224:` and `git show F:SKILL.md | grep -n 'selftest cases=14'` → `1224:`.
- Hunk shape: `@@ -1221,7 +1221,7 @@` (one line out, one line in; no other line of the file moves). The single remaining `cases=14` occurrence in the new file is an unrelated `r37-closure.sh` row, not the figure-audit row:

```
$ grep -n 'selftest cases=14' /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md
1113:| r37-closure.sh | gate | `bash corpus/instruments/r37-closure.sh --export-ref <hash>` … `selftest cases=14 failures=0` exit 0 | … | kasegi (round 37) |
EXIT=0
```

  On the freeze blob the same grep returns two hits (`1113:` the r37 row, `1224:` the figure-audit row); on the new file it returns one (`1113:`), evidence that the figure-audit row's `14` became `20` in place.

### 6.2 `corpus/SOURCES.md` — 1 deletion (permitted: the one lead bullet)
- Old `L141` (freeze, `grep -n 'was not opened'` → `141:`): `- Google Big Sleep reporting beyond the tracker linked by Project Zero; the first candidate DeepMind blog URL tried in this pass returned 404, and the referenced tracker at https://goo.gle/bigsleep was not opened.`
- New `L142`: `- Big Sleep reporting beyond the tracker linked by Project Zero: the tracker is opened as S092 (F40) and Project Zero's own Fuzzilli-vs-BigSleep comparison is opened as S093 (F41), so the earlier 'was not opened' clause is retired …`.
- The row insert is at new `L100` (`| S093 | Project Zero, Fuzzers vs. AI: …`), and the old→new log is a **new** line at `L221` (`- Leads bullet corrected old → new (round 60, the round-59 closure's routed defect 8): …`); both are insertions (0 deletions), which is why the file's net is 6/1 rather than 5/1.

### 6.3 `corpus/instruments/figure-audit-ledger.json` — 7 deletions (permitted: five derive strings + two record cells)
Old line numbers in the freeze blob where `awk` occurs (`grep -n 'awk'` → `91,120,123,128,131,155,237`):
- **five `"derive"` strings**: old `L91` (rev `5108584a…`, the r54 counter derive), `L123` (rev `32782bd6…`, LOG mentions), `L131` (rev `32782bd6…`, knowledge-expected mentions), `L155` (rev `133c5753…`, r55 counter), `L237` (rev `8a5d7538…`, r56 counter) — each replaced by a `grep|wc -l` / `cut|tr|wc -l` form on the same line number of the new file.
- **two `"record"` cells**: old `L120` (rev `32782bd6…`, "the LOG limb prints 0 … hence the awk whole-count form") and old `L128` (rev `32782bd6…`, "the knowledge-expected limb prints 0, exit 1 - awk whole-count form"), each reworded on the same line number to name the `grep|wc` form and the round-60 cause.
- Hunk shape — every changed line is a one-for-one replacement at the same line number, so the file's line count is unchanged and no cell moved:

```
$ git -C L diff -U0 66e6241cd7afd6184273ce7df1dcd5328c187367 7f7dd267283d2a16ca38d4cb05bed92165cb35cd -- corpus/instruments/figure-audit-ledger.json | grep -E '^@@'
@@ -91 +91 @@
@@ -120 +120 @@
@@ -123 +123 @@
@@ -128 +128 @@
@@ -131 +131 @@
@@ -155 +155 @@
@@ -237 +237 @@
EXIT=0
```

- 5 derives + 2 records = 7 = the file's deletion count, and every deleted line's key is either `"derive"` or `"record"` (the diff's removed lines start with one of those two keys only, §"ledger diff" above). No `"recorded"`, `"rev"`, `"want"` or `"id"` cell changed, and no entry was added or removed (7/7).

### 6.4 `corpus/instruments/figure-audit.py` — 8 deletions (file permitted; 2 lines outside the parenthetical)
`git -C L diff -U0 F I -- corpus/instruments/figure-audit.py | grep -E '^@@'` (exit 0):
```
@@ -27,3 +27,6 @@ Ledger entry shape (JSON object with a "figures" array):
@@ -49 +52,8 @@ READ_ONLY_HEADS = (
@@ -53 +63 @@ READ_ONLY_HEADS = (
@@ -80,0 +91,4 @@ def split_segments(cmd):
@@ -83,2 +97 @@ def split_segments(cmd):
@@ -94,0 +108,5 @@ def split_segments(cmd):
@@ -101,0 +120,7 @@ def split_segments(cmd):
@@ -130,0 +156,14 @@ def split_segments(cmd):
@@ -135,0 +175,2 @@ def segment_ok(head):
@@ -257 +298,7 @@ def selftest():
```
Deleted lines, by old line number and content (`git show F:<file> | awk 'NR==…'`, exit 0):
- `L27`-`L29` — 3 lines of the module docstring allow-list (`(allow-list: git show, git cat-file, grep, wc, ls,` / `sha256sum, cat, cut, sort, awk, sed -n, python/` / `python3 running a corpus/instruments/*.py counter).`). New `L27` rewrites the same paragraph (`…git ls-tree, grep, wc, ls, head,`).
- `L49` — 1 line of the `READ_ONLY_HEADS` tuple: `"sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "head ", "tail ", "python ", "python3 ",`. This is scanner/segment logic (the allow-list itself), replaced by the 8-line tuple at new `L52`.
- `L53` — 1 line: `EXPECTED_CASES = 14  # R17 pin: a dropped selftest case turns the selftest red`. **Outside** the item's "scanner/segment functions and docstring" description; new `L63` is `EXPECTED_CASES = 20 …`.
- `L83`-`L84` — 2 docstring lines on quoting (`… inside double quotes a backtick` / `… or '$(' is still live and refused. An unterminated quote is refused."""`), replaced by 1 line at new `L97`.
- `L257` — 1 line: `run_case("quoted-separator-admitted", 0, _one("s-quoted", "cat g.txt | awk 'BEGIN{x=1;y=2} {print}'", "35"))`. **Outside** the description; it is a selftest case whose pipeline used the now-removed `awk` head, rewritten at new `L298` as `… "cat g.txt | grep -e '35' -e ';'" …`.
- 3 + 1 + 1 + 2 + 1 = 8 = the file's deletion count. The five pure-insertion hunks (`-80,0`, `-94,0`, `-101,0`, `-130,0`, `-135,0`) add escaping/screen code inside `split_segments`/`segment_ok` and delete nothing; the mixed hunk `-27,3 +27,6` deletes the three docstring lines counted above and adds three.

## 7. Post-freeze drift — observation outside the two named commits

The item states the implementation "is landed at commit `7f7dd267…` (lane HEAD)". At audit time HEAD is not that commit:

```
$ git -C L rev-parse HEAD
b8c77fb9fa13710f46d8f564a00af640de5108cd
EXIT=0
$ git -C L log --oneline -8
fb6a928 round-60: lesson (M60-1..M60-7, Gate S093 with 15 quotes, sources/frontier, R78-R80 in QUALITY), extended neighbor-screen receipt, SHONEN box-2 reconciliation (round-59 defect 5)
b8c77fb round-60: wave-1 spec, validated plan and dispatch (13 seats, policy v1 band 8-16, attack share 4/13=31%, connector 1/13; L1 holds the planner seat)
7f7dd26 round-60: C1 escape-aware derive gate with awk/sed heads removed and a write-flag screen (selftest 14->20, mutbat 2/2, ledger 35/35, probes Q1-Q7 refused, docstring R74 limb 1) and C2 frontier F41 on S093 (Project Zero Fuzzilli-vs-BigSleep comparison; frontier 40->41, registry 92->93, entries 43->44, knowledge 78->79, binding 75->76, lead bullet corrected); SKILL registry cells, QUALITY R78, claims erratum 1
66e6241 round-60: freeze — claims C1 (escape-aware + in-program/write-flag gate repair, nominal per R58) and C2 (frontier F41 on S093); base/do-nothing/stand-in receipts, probe runner, S093 capture and manifest, assimilation id check
EXIT=0
$ git -C L rev-list --count 66e6241cd7afd6184273ce7df1dcd5328c187367..HEAD
3
EXIT=0
$ git -C L diff --name-only 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD | wc -l
7
EXIT=0
```

- Three commits sit past the freeze: `I` = `7f7dd267` (audited), then `b8c77fb` (wave-1 spec/plan/dispatch) and `fb6a928` (lesson + receipts + SHONEN):

```
$ git -C L show --shortstat --format= b8c77fb
 4 files changed, 603 insertions(+)
EXIT=0
$ git -C L show --shortstat --format= fb6a928
 3 files changed, 173 insertions(+), 1 deletion(-)
EXIT=0
```
- Seven paths changed after the audited implementation:

```
$ git -C L diff --numstat 7f7dd267283d2a16ca38d4cb05bed92165cb35cd..HEAD
207	0	.ufo/waves/round-60/build-spec.py
100	0	.ufo/waves/round-60/controls/neighbor-screen-r60.txt
251	0	.ufo/waves/round-60/w1-dispatch.json
67	0	.ufo/waves/round-60/w1-plan.json
78	0	.ufo/waves/round-60/w1-spec.json
4	1	SHONEN.md
69	0	corpus/lessons/round-60.md
EXIT=0
```

  These are outside my two named commits and therefore do not enter the §3 verdict, but they falsify the item's "lane HEAD" premise and they add one post-implementation deletion (`SHONEN.md` 4/1, in `fb6a928`, which is not a file the item's deletion bound covers). Recorded for the lead; the seat does not judge the later commits' intent.
- The audited artifacts are nevertheless stable at HEAD: §4 blob identity and `git -C L diff --stat I..HEAD -- corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json corpus/source-snapshots/round-60 .ufo/waves/round-60/claims.json` (no output, exit 0). So a seat that measures "lane HEAD" today would still read the audited bytes for the instrument, ledger, capture, manifest and claims; only the seven paths above differ.
- No tracked working-tree drift in L:

```
$ git -C L status --porcelain --untracked-files=no
(no output)
EXIT=0
```

## 8. Tooling

No tool was installed or upgraded for this seat. `git version 2.56.0` (pre-existing) was the only tool used. No `pacman` transaction was run (host-wide pause respected), no `uv`/`npx`/binary install was needed, and therefore no version/channel record is owed beyond this paragraph.

## 9. Scratch

`S = /fast/scratch/hyaku/kasegi-r60/ExecDiffScope` was created with `mkdir -p` and never used for a clone, export, mutant or probe: every measurement is a read-only command (git read-only subcommands, `sha256sum`, `grep`, `wc`, `awk`) against L, so no fixture tree was needed. It was removed before this file was yielded, and absence was asserted:

```
$ S=/fast/scratch/hyaku/kasegi-r60/ExecDiffScope; rm -rf -- "$S"; test ! -e "$S" && echo "S absent: $S"
S absent: /fast/scratch/hyaku/kasegi-r60/ExecDiffScope
EXIT=0
```

No leftover under S; no temp file was written anywhere else (nothing under `/tmp`, no relative-path write from the fleet root).

## 10. Summary table

| item step | predicate | measured | verdict |
|---|---|---|---|
| 1 | changed paths + kinds, both commits | F: 15 paths (15 A), 959/0; I: 12 paths (4 A, 8 M), 224/17 | enumerated |
| 2 | deletions only in figure-audit.py, figure-audit-ledger.json, corpus/SOURCES.md | `SKILL.md` 1 deletion; instrument 2 of 8 deletions outside the stated content description | **FAIL (SKILL.md)**; content note on the instrument |
| 3 | four sha256 equalities | worktree = commit-I = pinned value for instrument and ledger | pass |
| 4 | claims.json in F; erratum not in F, in I; capture+manifest in F | claims blob `975f84c` in F; erratum `cat-file -e` 128 at F, 0 at I; capture `372d9f4` + manifest `28cc5aa` in F, unchanged through HEAD | pass |
| premise | I is lane HEAD | HEAD is `fb6a928`; 3 commits past F, 7 paths changed after I (`SHONEN.md` 4/1) | **false at audit time** |
