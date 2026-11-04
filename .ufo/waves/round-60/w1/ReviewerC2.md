VERIFIED — all nine frozen C2 counting commands reproduce their wants at 7f7dd267283d2a16ca38d4cb05bed92165cb35cd (re-run identically at current lane HEAD 228118a8cfba679c1d97841aa3af38e5ec83d84a), the base-side counters match `controls/do-nothing-c2-r60.txt`, the pure-append files have 0 deletions, corpus/SOURCES.md's only deleted line is the declared lead bullet with S001–S092 id/URL cells untouched, and the F41 entry's recheck line has no absolute `cd` and passes from the clone root and from a `.git`-less archive export. No failing frozen number.

# Seat / scope

C2 review of round 60 (frontier F41 on S093), lane `kasegi`. Read-only on the lane; the only lane file written is this one. Assigned implementation commit `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`; claims frozen at `66e6241cd7afd6184273ce7df1dcd5328c187367`; counting command 8's want is 2 per `.ufo/waves/round-60/claims-erratum-1.md`. Scratch root `S=/fast/scratch/hyaku/kasegi-r60/ReviewerC2`; `TMPDIR=$S` on every command; all paths absolute.

Lane state at first read: `git -C L rev-parse HEAD` = `b8c77fb9fa13710f46d8f564a00af640de5108cd`; `git -C L status --porcelain` listed only `??` entries (round-57/58/59/60 wave files), no modified tracked path. During the wave the lane advanced to `228118a8cfba679c1d97841aa3af38e5ec83d84a` (commits `fb6a928`, `228118a`); the C2-relevant paths are unchanged between `7f7dd26` and that HEAD (E10).

# E1 — head clone identity (the tree every head-side number below was measured in)

```
$ S=/fast/scratch/hyaku/kasegi-r60/ReviewerC2; D=$(mktemp -d -p "$S") && echo "D=$D" && git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$D/clone" && git -C "$D/clone" checkout -q 7f7dd267283d2a16ca38d4cb05bed92165cb35cd && git -C "$D/clone" rev-parse HEAD && git -C "$D/clone" rev-parse --show-toplevel
D=/fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.vutWSGVVsD
7f7dd267283d2a16ca38d4cb05bed92165cb35cd
/fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.vutWSGVVsD/clone
```
exit 0. Every command E2–E7 ran with `cd` into `/fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.vutWSGVVsD/clone`.

# E2 — C2 counting command 1 (frontier counter)

```
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F41|entries='
FRONTIER-CENSUS rows=41 admitted=41 closed=41 problem-rows=0 registry=93
FRONTIER-PASS F41 ids=S093
entries=44 pass=44 exit=0
EXIT1=0
```
Want: `rows=41 admitted=41 closed=41 problem-rows=0 registry=93`; `FRONTIER-PASS F41 ids=S093`; `entries=44 pass=44 exit=0`; exit 0. **Match on all values.**

Supporting line and counts (same clone root):

```
$ python3 corpus/instruments/frontier-recheck-count.py | grep 'F41'
FRONTIER-PASS F41 ids=S093
PASS     F41  knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md ids=S093           exit=0

$ python3 corpus/instruments/frontier-recheck-count.py > $S/counter-head.out 2>&1; echo "COUNTER-EXIT=$?"
COUNTER-EXIT=0
$ grep -c '^PASS ' $S/counter-head.out ; grep -c '^FAIL ' $S/counter-head.out ; grep -c '^FRONTIER-PASS ' $S/counter-head.out
44
0
41
```
exit 0 for the run; 44 `PASS` lines, 0 `FAIL` lines, 41 `FRONTIER-PASS` lines. So `entries=44 pass=44` is backed by 44 executed entries and F41 by a PASS line naming the new entry and `ids=S093`.

# E3 — C2 counting command 2 (source-recheck, S093)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S093
S093:sha256 OK
S093:Q1 OK occurrences=2 anchor=12-ok
S093:Q10 OK occurrences=1 anchor=82-ok
S093:Q11 OK occurrences=1 anchor=88-ok
S093:Q12 OK occurrences=1 anchor=16-ok
S093:Q13 OK occurrences=1 anchor=16-ok
S093:Q14 OK occurrences=1 anchor=281-ok
S093:Q15 OK occurrences=1 anchor=281-ok
S093:Q2 OK occurrences=1 anchor=16-ok
S093:Q3 OK occurrences=1 anchor=40-ok
S093:Q4 OK occurrences=1 anchor=51-ok
S093:Q5 OK occurrences=1 anchor=61-ok
S093:Q6 OK occurrences=1 anchor=65-ok
S093:Q7 OK occurrences=1 anchor=68-ok
S093:Q8 OK occurrences=1 anchor=71-ok
S093:Q9 OK occurrences=1 anchor=74-ok
EXIT2=0
```
Want: `sha256 OK` plus 15 Q-OK lines, each with `occurrences=` and an `anchor=` verification. **Match:** one `sha256 OK` line, 15 `Qn OK` lines; Q1 is the only `occurrences=2` line and it carries `anchor=12-ok`, i.e. anchor-verified, exactly the want's "occurrences=1 or anchor-verified". Line count checked independently: `... | grep -c 'OK occurrences='` = `15`.

# E4 — C2 counting command 3 (capture binding)

```
$ python3 corpus/instruments/capture-binding-check.py | tail -1
records=76 bound=76 unbound=0
EXIT3=0
```
Want: `records=76 bound=76 unbound=0`, exit 0. **Match.** The record that makes it 76 is the round-60 manifest (same run, grep view):

```
$ python3 corpus/instruments/capture-binding-check.py | grep -E 'round-60|AUDIT|records=76'
MANIFEST round-60 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=76 with_url=76 with_fetched_utc=38 with_archival=38 snapshot_dirs=36 manifest_dirs=36 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=76 bound=76 unbound=0
```

# E5 — C2 counting commands 4–6 (knowledge files, expected list, sort)

```
$ ls corpus/knowledge/*.md | wc -l
79
$ grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt
79
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
EXIT6=0
```
Want: 79, 79, exit 0. **Match.** (The file has 81 physical lines at head: 79 entry lines plus two `#` header lines; `wc -l` of the file is therefore not the count the command measures.) The only added entry line:

```
$ git -C L diff -U0 cdeea55... 7f7dd26... -- corpus/instruments/knowledge-expected.txt
@@ -61,0 +62 @@ corpus/knowledge/program-severity-ladders-and-reward-scales.md
+corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
```
One insertion, zero deletions, at the C-sorted position — consistent with `sort -c` above.

# E6 — C2 counting commands 7–9 (README row, lead bullet, census)

```
$ grep -cE '^\| F41 ' corpus/README.md
1
$ grep -c 'the tracker is opened as S092' corpus/SOURCES.md
2
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
... (5 more pre-existing W04 duplicate-url warnings, unchanged base→head, see E8) ...
file	ok	/fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.vutWSGVVsD/clone/corpus/SOURCES.md
EXIT9=0
```
- Command 7 want 1: **match** (prints `1`, exit 0).
- Command 8: frozen text says `want: 1`; **`.ufo/waves/round-60/claims-erratum-1.md` supersedes it to 2** (both occurrences are the declared lead correction: SOURCES.md:142 under `## Leads (unopened)` and SOURCES.md:221 under `## Registry changes`, E9). Measured `2`, exit 0 → **match to the erratum's value.** Base-side control: `git -C L show cdeea55:corpus/SOURCES.md | grep -c 'the tracker is opened as S092'` = `0` (so the correction, not a pre-existing phrase, produces both lines).
- Command 9 want exit 0: **match** (exit 0). The six `W04 duplicate url` warnings are pre-existing: the base census output is byte-identical after normalising the root path (E8).

# E7 — frozen capture digest and manifest shape

```
$ sha256sum corpus/source-snapshots/round-60/S093.txt
46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96  corpus/source-snapshots/round-60/S093.txt
$ wc -lc corpus/source-snapshots/round-60/S093.txt
    283  40649 corpus/source-snapshots/round-60/S093.txt
```
Frozen want `46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96`: **match.** The entry and registry row state "40649 snapshot bytes over 283 lines": **match**.

Manifest (`corpus/source-snapshots/round-60/manifest.json`) read with `python3 -c`:

```
id = S093
url = https://projectzero.google/2026/10/fuzzing-v-AI.html
capture_url = https://projectzero.google/2026/10/fuzzing-v-AI.html
http = {'status': 200, 'final_url': 'https://projectzero.google/2026/10/fuzzing-v-AI.html'}
bytes = 64812
snapshot_bytes = 40649
lines = 283
sha256 = 46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96
fetched_utc = 2026-11-04T13:29:52Z
quotes: 15   (Q1..Q15)
```
"15 pinned quotes": **match** (15 entries under `sources[0].quotes`, anchors 12/16/40/51/61/65/68/71/74/82/88/16/16/281/281).

# E8 — base side at cdeea55bea09ed08765d3c3d3a56f23db44e66f4 versus `controls/do-nothing-c2-r60.txt`

Second clone: `B=$(mktemp -d -p "$S"); git clone -q --shared L "$B/base"; git -C "$B/base" checkout -q cdeea55...`; `git -C "$B/base" rev-parse HEAD` = `cdeea55bea09ed08765d3c3d3a56f23db44e66f4`, toplevel `/fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.Qmitat2R7b/base`.

```
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|entries='
FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92
entries=43 pass=43 exit=0
BASE-FRONTIER-EXIT=0
$ python3 corpus/instruments/capture-binding-check.py | tail -1
records=75 bound=75 unbound=0
BASE-BINDING-EXIT=0
$ grep -cE '^\| F40 ' corpus/README.md        # 1
$ grep -cE '^\| F41 ' corpus/README.md        # 0   (grep exit 1)
$ ls corpus/knowledge/*.md | wc -l            # 78
$ grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt   # 78
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt ; echo "EXIT=$?"   # EXIT=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md >/dev/null 2>&1 ; echo "EXIT=$?"   # EXIT=0
```

| control `do-nothing-c2-r60.txt` | measured at base | match |
|---|---|---|
| `FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92` | same | yes |
| `entries=43 pass=43 exit=0` | same | yes |
| `frontier-exit=0` | 0 | yes |
| F40/F41 rows `1` / `0` | 1 / 0 | yes |
| knowledge counts `78` / `78` | 78 / 78 | yes |
| `sort-exit=0` | 0 | yes |
| `records=75 bound=75 unbound=0` | same | yes |
| `binding-exit=0` | 0 | yes |
| `census-file-exit=0` | 0 | yes |

Census output comparison, root path normalised: `diff base-census.norm head-census.norm` → **exit 0** (identical text, same six `W04 duplicate url` warnings and the same `file ok` line).

# E9 — pure-append rule and corpus/SOURCES.md diff classification

```
$ git -C L diff --numstat cdeea55bea09ed08765d3c3d3a56f23db44e66f4 7f7dd267283d2a16ca38d4cb05bed92165cb35cd -- corpus/README.md PROVINCE.md corpus/instruments/knowledge-expected.txt
2	0	PROVINCE.md
21	0	corpus/README.md
1	0	corpus/instruments/knowledge-expected.txt
```
**Deletions 0 in all three.** Insertion positions against base lengths (base `git show cdeea55:<file> | wc -l`: README 988, PROVINCE 207, knowledge-expected 80 = 78 entries + 2 header lines; head `wc -l`: 1009, 209, 81):

```
$ git -C L diff -U0 cdeea55... 7f7dd26... -- corpus/README.md PROVINCE.md | grep '^@@'
@@ -207,0 +208,2 @@ RECEIPT-STORE-LOST stays corpus-attested-only and nothing in this province re-gr
@@ -988,0 +989,21 @@ outside it.
```
README and PROVINCE additions are end-of-file appends (base length + 1). `knowledge-expected` is `@@ -61,0 +62 @@` — a sorted-position insertion, not EOF; deletions are still 0 and `LC_ALL=C sort -c` passes (E5), so the append rule "deletions 0" holds while the sort invariant is preserved.

`corpus/SOURCES.md` numstat and hunks:

```
$ git -C L diff --numstat cdeea55... 7f7dd26... -- corpus/SOURCES.md
6	1	corpus/SOURCES.md
$ git -C L diff -U0 cdeea55... 7f7dd26... -- corpus/SOURCES.md | grep -E '^@@|^-'
@@ -99,0 +100 @@
@@ -141 +142 @@
-- Google Big Sleep reporting beyond the tracker linked by Project Zero; the first candidate DeepMind blog URL tried in …
@@ -216,0 +218,4 @@ Change cell old → new: the S043 anchor originally described the raw `policy_ve
```

**Classification: 3 hunks, 6 additions, 1 deletion.**
1. `+100` — one added registry row, cells read with `sed -n '100p' corpus/SOURCES.md | awk -F'|' '{for(i=2;i<=NF-1;i++){v=$i; gsub(/^[ \t]+|[ \t]+$/,"",v); printf "[%d] %s\n", i-1, v}}'`:

```
[1] S093
[2] Project Zero, Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines (2026-Oct-27) — https://projectzero.google/2026/10/fuzzing-v-AI.html
[3] docs
[4] A
[5] Project Zero's own dated comparison of two production automated vulnerability-discovery pipelines on V8 — …
[6] capture corpus/source-snapshots/round-60/S093.txt (40649 bytes, 283 lines, sha256 46f69d32cd237d0c…39076347d96): title/date/byline L12-L14 (Q1); production numbers L16 (Q2) and L40 (Q3); production overlap L51 (Q4) …
[7] Read an LLM agent's production output against a coverage-guided fuzzer as a tie on actionable Type-Vuln counts with a ~25% overlap, …
[8] mined
[9] 2026-11-04
[10] 90d
[11] corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
```
   (<https://projectzero.google/2026/10/fuzzing-v-AI.html> in cell 2 equals the entry's `source:` URL and the manifest's `url`/`capture_url`, E7.)
2. `-141/+142` — **the only modified line**: the old lead bullet is deleted and the corrected bullet added; the deletion count 1 is exactly this declared correction.
3. `+218..+221` — 4 added lines under `## Registry changes` (blank, `- S093 row added (round 60): …`, blank, `- Leads bullet corrected old → new (round 60, … defect 8): …`); heading at SOURCES.md:151, bullets at 219 and 221.

S001–S092 id/URL cells untouched — per-row `id|source-cell` extraction from each revision, then diff:

```
$ git -C L show <rev>:corpus/SOURCES.md | awk -F'|' '/^\| S[0-9][0-9][0-9] /{id=$2; src=$3; gsub(/^[ \t]+|[ \t]+$/,"",id); gsub(/^[ \t]+|[ \t]+$/,"",src); print id "|" src}'   # run once per rev, output to base-rows.txt / head-rows.txt
base-rows=92 head-rows=93
$ diff base-rows.txt head-rows.txt
92a93
> S093|Project Zero, Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines (2026-Oct-27) — https://projectzero.google/2026/10/fuzzing-v-AI.html
DIFF-EXIT=1
$ diff base-urls.txt head-urls.txt          # URL-only extraction, same rows
92a93
> https://projectzero.google/2026/10/fuzzing-v-AI.html
URL-DIFF-EXIT=1
```
Only an append of S093; no S001–S092 id or URL cell changed. `grep -c '^| S093 ' corpus/SOURCES.md` = `1` (no duplicate id).

README F41 row (README.md:1005, inside the appended round-60 block at 989–1009), cells read with the same awk form on `corpus/README.md` line 1005:

```
[1] F41
[2] Project Zero Fuzzilli-vs-BigSleep comparison — the publisher's own dated comparison of an LLM bug-finding agent against a coverage-guided JavaScript-engine fuzzer on V8: the six-month production window's actionable Type-Vuln counts and ~25% overlap, the 112-bug re-discovery experiment at 25 attempts per commit, and the post's "run both" recommendation to vendors
[3] admitted
[4] knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md
[5] S093
[6] Read the 45-vs-37 pair as actionable Type-Vuln reports, not raw reports (the post's own 316/441 counts narrow to 178/95 then 45/37) and as a tie rather than agent superiority; …
```
`sources` cell `S093`, `status` cell `admitted`, entry cell the new file. PROVINCE addition: PROVINCE.md:208–209, blank plus `[r60 Frontier amendment, appended 2026-11-04, end-of-file append per R6] F41 — Project Zero's Fuzzilli-vs-BigSleep comparison … admitted round 60; entry corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md (source S093; capture corpus/source-snapshots/round-60/S093.txt); scope limit: one first-party research post on Google's own two systems and one target only …`.

# E10 — the F41 entry's recheck line: no absolute `cd`, clone-root pass, export pass, fail-closed

Entry `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md` (43 lines). Recheck line is line 6; its executable prefix (comment stripped, the way the counter executes it) is:

```
$ sed -n '6p' <entry> | sed 's/^recheck:[[:space:]]*//; s/[[:space:]]*#.*$//' > $S/recheck-cmd.txt
$ cat $S/recheck-cmd.txt
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-60/manifest.json --source S093
$ grep -cE '(^|[[:space:];&|(])cd([[:space:]]|$)' $S/recheck-cmd.txt
0
grep-exit=1
$ grep -cE '/home/|/fast/|/tmp/|^cd' $S/recheck-cmd.txt
0
grep-exit=1
```
No `cd` token and no absolute path in the executed command — the entry carries no absolute `cd` (the word `cd` appears only inside the trailing comment's parenthetical "no absolute `cd` is baked in").

Clone-root run:

```
$ cd /fast/scratch/hyaku/kasegi-r60/ReviewerC2/tmp.vutWSGVVsD/clone && bash -c "$(cat $S/recheck-cmd.txt)" | tail -3
S093:Q7 OK occurrences=1 anchor=68-ok
S093:Q8 OK occurrences=1 anchor=71-ok
S093:Q9 OK occurrences=1 anchor=74-ok
RUN-EXIT=0
```
Passes, exit 0.

Export replay (the ExportReplay class round 58/59 named) — `git archive` of the commit into a third path with **no `.git`**, then the same line:

```
$ git -C L archive 7f7dd267283d2a16ca38d4cb05bed92165cb35cd | tar -x -C $S/export
$ cd $S/export && bash -c "$(cat $S/recheck-cmd.txt)" | tail -2
S093:Q8 OK occurrences=1 anchor=71-ok
S093:Q9 OK occurrences=1 anchor=74-ok
EXPORT-RUN-EXIT=0
$ ls $S/export/.git
ls: cannot access '.../export/.git': No such file or directory
```
**State: this entry fixes the ExportReplay cd-prefix class for itself** — its recheck line is root-relative and passes in a plain exported tree at a third absolute path. For contrast, a pre-round-60 entry still bakes the absolute lane path (`corpus/knowledge/google-big-sleep-findings-tracker.md:6`: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092 …`); that class is explicitly a non-claim this round and is unchanged.

Fail-closed semantics stated on the recheck line, exercised in the export (scratch only; restored afterwards):

```
$ cd $S/export
$ printf 'x' >> corpus/source-snapshots/round-60/S093.txt
$ bash -c "$(cat $S/recheck-cmd.txt)"; echo "TAMPER-EXIT=$?"
S093:sha256 MISMATCH expected=46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96 actual=9999c9d6005343468bbad04bd75337bd80aee7c4da26fcdbe908841e1d0beb20
TAMPER-EXIT=1
$ mv corpus/source-snapshots/round-60/manifest.json $S/manifest.bak
$ bash -c "$(cat $S/recheck-cmd.txt)"; echo "NOMANIFEST-EXIT=$?"
manifest UNAVAILABLE reason=missing
NOMANIFEST-EXIT=2
$ mv $S/manifest.bak corpus/source-snapshots/round-60/manifest.json
$ bash -c "$(cat $S/recheck-cmd.txt)" | tail -1; echo "RESTORED-EXIT=${PIPESTATUS[0]}"
S093:Q9 OK occurrences=1 anchor=74-ok
RESTORED-EXIT=0
$ sha256sum corpus/source-snapshots/round-60/S093.txt
46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96  corpus/source-snapshots/round-60/S093.txt
```
Digest-differs → exit 1; manifest absent → exit 2; restored → exit 0, matching the line's stated failure mode.

# E11 — the F41 PASS is causally tied to the capture (counter sensitivity)

In the export, tampering only the capture and re-running the frontier counter:

```
$ printf 'x' >> corpus/source-snapshots/round-60/S093.txt
$ python3 corpus/instruments/frontier-recheck-count.py > $S/counter-tamper.out 2>&1; echo COUNTER-EXIT=$?
COUNTER-EXIT=1
$ grep -E 'F41|FRONTIER-CENSUS|entries=' $S/counter-tamper.out
FRONTIER-CENSUS rows=41 admitted=41 closed=40 problem-rows=1 registry=93
FRONTIER-FAIL F41 status=admitted ids=S093 problems=missing-pass-line
FAIL     F41  knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md ids=S093           exit=1    problems=recheck-exit-1
entries=44 pass=43 exit=1
```
Restored capture digest `46f69d32…39076347d96`, and returning to E2 gives `pass=44` again. So the PASS line is not a rubber stamp: it depends on the F41 entry's recheck succeeding against the pinned capture.

# E12 — content support for the admitted frontier (spot checks, exact anchors)

The claim is a coverage claim; the entry's numbers were checked against the capture it pins:

```
$ F=corpus/source-snapshots/round-60/S093.txt
$ grep -nE '^Fuzzilli: 316|^BigSleep: 441|^Fuzzilli: 178|^BigSleep: 95|45 vs\. 37|roughly 25% \(20 out of a total of 81\)|final number of 112|25 attempts|re-discover ~62%|knowledge cutoff date is March 2026|5 attempts per bug|~70%|~84%|overlap was around 60%' "$F"
30:Fuzzilli: 316
31:BigSleep: 441
33:Fuzzilli: 178
34:BigSleep: 95
40:So in terms of vulnerabilities, it’s roughly a tie (small advantage BigSleep) at the moment: 45 vs. 37.
51:… we see an overlap of roughly 25% (20 out of a total of 81) …
61:… This leaves us with a final number of 112 bugs.
65:We now run the agent for 25 attempts on each commit. …
68:… re-discover ~62% … another ~12% of commits. On around 26% of the commits it failed to find any bugs.
71:For the model used in this experiment (Gemini 3.6 flash), the knowledge cutoff date is March 2026. … there seems to be no statistically significant amount of memorization pre-2026.
82:Running these two experiments with only 5 attempts per bug … 10 additional bugs in total: 8 from the different starting points and 7 with the rephrased prompt …
84:… the share of “correct” bugs found climbs to ~70%, and we find some kind of bug for ~84% of starting points. …
88:In our experiment, overlap was around 60% of historic Fuzzilli bugs (70% with additional runs that used different prompts).
281:… the two approaches remain complementary, and specialized fuzzing continues to provide value by finding bugs quickly …
```
Title/date/byline at 12/13/14, scope sentence at 22, target sentence at 23, six-month sentence ("We limit our analysis to the six months from April to September 2026") at 26, hotlist queries at 27/28, reverse-direction sentence at 53, difficulty sentence at 74, JIT-component sentence at 91 — each cited at those exact lines in the entry (`sed -n 'Np'` on each). `grep -c 'the six months from April to September 2026'` = `1`; `grep -c 'statistically significant'` = `2` (line 71 memorization and line 74 difficulty).

All 15 manifest quotes, exact-line scan (`python3` scan of `manifest.json` quotes against `S093.txt`, one line per quote):

```
Q1 anchor=12 exact_line_hits=[1, 12]   Q2 16 [16]   Q3 40 [40]   Q4 51 [51]
Q5 61 [61]   Q6 65 [65]   Q7 68 [68]   Q8 71 [71]   Q9 74 [74]   Q10 82 [82]
Q11 88 [88]  Q12 16 [16]  Q13 16 [16]  Q14 281 [281] Q15 281 [281]
```
Every anchor is the quote's exact line (Q1 is non-unique — also the HTML `<title>` at line 1 — and its anchor 12 selects the body title, hence the instrument's `occurrences=2 anchor=12-ok`).

# E13 — current lane HEAD cross-check

`git -C L rev-parse HEAD` = `228118a8cfba679c1d97841aa3af38e5ec83d84a`; `git -C L diff --numstat 7f7dd267283d2a16ca38d4cb05bed92165cb35cd 228118a8cfba679c1d97841aa3af38e5ec83d84a`:

```
207	0	.ufo/waves/round-60/build-spec.py
100	0	.ufo/waves/round-60/controls/neighbor-screen-r60.txt
251	0	.ufo/waves/round-60/w1-dispatch.json
67	0	.ufo/waves/round-60/w1-plan.json
78	0	.ufo/waves/round-60/w1-spec.json
13	0	LOG.md
37	0	SCORECARD.md
4	1	SHONEN.md
69	0	corpus/lessons/round-60.md
```
No C2-relevant path (SOURCES.md, README.md, PROVINCE.md, knowledge-expected.txt, the F41 entry, the capture, the manifest, the instruments) is in that set. Third clone at `228118a` (`.../tmp.vCZ4qTeWR8/head`, `rev-parse HEAD` verified) re-ran the nine commands:

```
CMD1: FRONTIER-CENSUS rows=41 admitted=41 closed=41 problem-rows=0 registry=93 ; FRONTIER-PASS F41 ids=S093 ; entries=44 pass=44 exit=0 ; EXIT1=0
CMD2: 15 Q-OK lines incl. S093:Q1 OK occurrences=2 anchor=12-ok ; EXIT2=0
CMD3: records=76 bound=76 unbound=0 ; EXIT3=0
CMD4/5/6: files=79 expected=79 SORT-EXIT=0
CMD7/8: 1 / 2
CMD9: CENSUS-EXIT=0
sha256sum …/S093.txt: 46f69d32cd237d0c14755ba3ce5cbaee0999219e82c806a78e5aa39076347d96
```
Identical to E2–E7. (The lane-after receipt `controls/c2-lane-after-r60.txt` measured working-tree bytes at lane-tip `66e6241`; E2–E7 measure the committed bytes at `7f7dd26` and match, so the receipt's working-tree measurement is reproduced from the committed tree.)

# Findings (severity order)

- **Blocking:** none. No frozen C2 number failed; every kill-rule item the item names was checked and passed (frontier counter values + exit, source-recheck Q lines + exit, capture-binding values + exit, S093 digest, knowledge 79 = 79 + sort, lead bullet present, F41 README row present, S001–S092 id/URL untouched).
- **Major:** none.
- **Minor:** none in C2's predicate.
- **Observations (non-findings; pre-existing or out-of-scope, recorded so they are not mistaken for C2 gaps):**
  1. Lane HEAD moved during the wave (`b8c77fb` → `228118a`) while the item names `7f7dd26` as lane HEAD. C2-relevant paths are unchanged and all nine commands were re-run at `228118a` with identical output (E13).
  2. `source-recheck.py`'s anchor verdict is a 4-line window (`window = " ".join(raw_lines[max(0, anchor - 1):anchor + 3])`, `corpus/instruments/source-recheck.py:110`), so `anchor=N-ok` alone proves the quote lies in lines N..N+3. For this manifest I closed the gap independently: every one of the 15 quotes is exactly on its anchored line (E12). Instrument behaviour is pre-existing and unchanged this round; the claim's phrase "anchor-verified" is satisfied by the instrument's own contract.
  3. `capture-binding` AUDIT still reports `orphans=1 orphan=S040-live.txt` at both base and head; C2 does not predicate on orphans and the count of records/bound is as claimed.
  4. `corpus/instruments/knowledge-expected.txt`'s header comment still says "round 30". The file is append-only this round (`1	0`), so the header was not touched; updating it would have broken the deletions-0 rule. Pre-existing, not a C2 defect.
  5. The frozen `claims.json` command 8 text still reads `# want: 1`; the erratum's 2 is the operative value and the measured value is 2 with a base value of 0 (E6). Editing claims.json is prohibited, so this is the correct handling, not a defect.
  6. `corpus/SOURCES.md` `## Registry changes` bullets sit at lines 219 and 221; the `## Leads (unopened)` bullet is at 142. Both phrase occurrences are the declared correction (erratum statement confirmed).

# Residual risk and verification gaps

- **No live re-fetch.** The capture's provenance fields (`http.status=200`, `bytes=64812`, `fetched_utc=2026-11-04T13:29:52Z`, "independent curl open … same text") are the manifest's self-record; I verified the pinned snapshot's bytes (40649/283), its frozen digest, and all 15 quote anchors against that snapshot. Upstream state is not re-verified, which matches the claim's own "pinned-capture comparison, not a fresh network check" scope. `64812` is read from the manifest, not re-measured over the network.
- **Execution is `bash -c`, not a sandbox.** The counter runs each entry's `recheck:` line with `cwd=root` (`frontier-recheck-count.py:269`), which is why the entry's root-relative line is the right shape; it is still arbitrary shell execution. This is the lane's named-open derive/gate boundary, outside C2's predicate.
- **ExportReplay class remains for pre-r60 entries** (their recheck lines `cd` to the absolute lane path; e.g. the F40 entry at line 6). This entry fixes it for itself (E10); repairing old entries is a declared non-claim.
- **Not audited by this seat:** post-implementation report/lesson files added in `fb6a928`/`228118a` (`corpus/lessons/round-60.md`, SCORECARD/LOG/SHONEN); none is read by any of the nine C2 commands, and they are outside the item's target list.
- **Anchor window:** as E12/Observation 2 — closed for this manifest by the exact-line scan; the instrument-level weakness would matter for a future manifest whose anchors are only window-accurate.

# Tooling

No installs or upgrades were needed or performed. Tools used, all pre-existing on the host: `python3` 3.14.8, `git` 2.56.0. No `pacman` transaction was run (host-wide pause respected); no tool was written to `~/.local/bin` or any other PATH directory.

# Scratch

All fixtures lived under `S=/fast/scratch/hyaku/kasegi-r60/ReviewerC2` (`tmp.vutWSGVVsD/clone`, `tmp.Qmitat2R7b/base`, `tmp.vCZ4qTeWR8/head`, `export/`, and the small `.out`/`.txt` files cited above), with `TMPDIR=$S`. The directory is removed with `rm -rf -- "$S"` before this seat yields; nothing is left behind, and no lane file other than this evidence file was written.
