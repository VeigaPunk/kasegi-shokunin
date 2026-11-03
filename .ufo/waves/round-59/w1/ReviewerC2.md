VERIFIED — every frozen C2 "after" number reproduced at tip 472737847ff31d1255bf1a0745822a5e878e9622 in a fresh clone; base 69de8d3 "before" numbers also reproduced; pure-append rule and lead-line sha hold. One caveat recorded in §4 (entry recheck line cds to an absolute lane path; run in clone with clone manifest instead, as directed).

Seat: ReviewerC2 (C2 frontier F40 re-open). Lane HEAD checked: 472737847ff31d1255bf1a0745822a5e878e9622 (`git -C L rev-parse HEAD`).
Scratch: /fast/scratch/hyaku/kasegi-r59/ReviewerC2 (removed before yield; see §8).
Tool installs: none (all commands used system python3 3.14 and git; nothing installed or upgraded).

## 0. Setup

Command:
```
S=/fast/scratch/hyaku/kasegi-r59/ReviewerC2; L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; export TMPDIR=$S
D=$(mktemp -d -p "$S"); git clone -q --shared "$L" "$D/clone"; git -C "$D/clone" checkout -q 472737847ff31d1255bf1a0745822a5e878e9622
git -C "$D/clone" rev-parse --show-toplevel; git -C "$D/clone" rev-parse HEAD; git -C "$D/clone" status --short | wc -l
```
Output:
```
/fast/scratch/hyaku/kasegi-r59/ReviewerC2/tmp.ZKaAeFp9cV/clone
472737847ff31d1255bf1a0745822a5e878e9622
0
```
Exit 0. Clone root = /fast/scratch/hyaku/kasegi-r59/ReviewerC2/tmp.ZKaAeFp9cV/clone (HEAD matches, clean tree).

Base clone (for "before" numbers):
```
D2=$(mktemp -d -p "$TMPDIR"); git clone -q --shared "$L" "$D2/base"; git -C "$D2/base" checkout -q 69de8d363b2193fdb37d03fd3e235bceeb1c2daa
git -C "$D2/base" rev-parse HEAD
```
Output: `69de8d363b2193fdb37d03fd3e235bceeb1c2daa`; root /fast/scratch/hyaku/kasegi-r59/ReviewerC2/tmp.FGPZ5R4iqT/base.

Frozen command text was read with `python3 -c "import json; ... claims[1]"` from L/.ufo/waves/round-59/claims.json (claim C2, kill_rule and before/after strings).

## 1. Counting commands (frozen C2 counting_commands), run in the clone root

1a. `python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F40|entries='`
```
exit=0
FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92
FRONTIER-PASS F40 ids=S092
entries=43 pass=43 exit=0
```
Full output file also shows `PASS     F40  knowledge/google-big-sleep-findings-tracker.md       ids=S092           exit=0`. Want: rows=40 admitted=40 closed=40 problem-rows=0 registry=92 / FRONTIER-PASS F40 ids=S092 / entries=43 pass=43 exit=0. **Reproduced.**

1b. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092`
```
S092:sha256 OK
S092:Q1 OK occurrences=1 anchor=2-ok
S092:Q10 OK occurrences=1 anchor=2-ok
S092:Q2 OK occurrences=1 anchor=2-ok
... (Q3–Q9 each occurrences=1 anchor=2-ok)
exit=0
```
10 Q lines (Q1–Q10), each occurrences=1. **Reproduced.**

1c. `python3 corpus/instruments/capture-binding-check.py | tail -1`
```
records=75 bound=75 unbound=0
exit=0
```
**Reproduced.**

1d. `ls corpus/knowledge/*.md | wc -l` → `78`, exit 0 (pipefail variant `set -o pipefail; ... ; echo exit=$?` → `78`, exit=0). **Reproduced.**

1e. `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` → `78`, exit 0. **Reproduced.** Entry on line 38 of knowledge-expected.txt: `corpus/knowledge/google-big-sleep-findings-tracker.md`.

1f. `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` → no output, exit 0. **Reproduced.**

1g. `grep -cE '^\| F40 ' corpus/README.md` → `1`, exit 0. (The row is README.md:984; block header at :970.) **Reproduced.**

1h. `grep 'Google Big Sleep reporting beyond the tracker' corpus/SOURCES.md | sha256sum` → `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432  -`, exit 0. **Reproduced** (matches frozen 3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432).

1i. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` (run in clone)
exit=0; final line `file	ok	/fast/scratch/hyaku/kasegi-r59/ReviewerC2/tmp.ZKaAeFp9cV/clone/corpus/SOURCES.md`. Preceding lines are four `W04` duplicate-url warnings (S072, S076, S080, S085) — pre-existing: base and tip outputs are byte-identical after path substitution (`diff` exit 0, 7 lines each). **Reproduced** (exit 0). Note: the script is a fleet-root tool, invoked read-only.

## 2. Kill-rule counters (C2 kill_rule)

- S092 capture sha256: `sha256sum corpus/source-snapshots/round-59/S092.txt` → `048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38  corpus/source-snapshots/round-59/S092.txt`, exit 0. Matches frozen 048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38. Capture size `wc -c` = 6371 bytes (matches entry header).
- Lead-line sha at base: `git -C L show 69de8d3:corpus/SOURCES.md | grep 'Google Big Sleep reporting beyond the tracker' | sha256sum` → `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432  -`, exit 0.
- Lead-line sha at tip: same command on `472737847:corpus/SOURCES.md` → `3ed4f54df244a57ffbc82d9c1ce1cd909d5d7ab70be807a1a6d1d978e652a432  -`, exit 0. Unchanged.
- Working-tree L lead-line sha → same value.
- Knowledge-expected entries 78 = knowledge files 78; LC_ALL=C sorted. OK.

## 3. Pure-append rule (step 2)

Command: `git -C L diff --numstat 69de8d363b2193fdb37d03fd3e235bceeb1c2daa 472737847ff31d1255bf1a0745822a5e878e9622 -- corpus/README.md PROVINCE.md corpus/instruments/knowledge-expected.txt corpus/SOURCES.md`
```
2	0	PROVINCE.md
20	0	corpus/README.md
1	0	corpus/SOURCES.md
1	0	corpus/instruments/knowledge-expected.txt
```
exit 0. Deletions = 0 in all four files. SOURCES adds exactly one line. The SOURCES diff hunk is `@@ -96,6 +96,7 @@`, a single `+| S092 | Google Issue Tracker, [Big Sleep] README (issue 430375499) ...` after the S091 row; S001–S091 lines unchanged (no `-` lines). **Reproduced / rule holds.**

## 4. Recheck-line caveat (step 1 instruction)

- The frontier counter (`corpus/instruments/frontier-recheck-count.py`) derives its root from `__file__` (lines 494, 504: `--root` defaults to the script's parent-of-parent), so the in-clone run measured the clone, not L. The grep for `cd /` in the counter output found nothing; the counter itself does not cd.
- The entry's own recheck line (corpus/knowledge/google-big-sleep-findings-tracker.md:6) is `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092 ...`. It names the absolute lane root, so run literally it would read L's working tree, not the clone. Per the directive I ran the same source-recheck with the clone's manifest in the clone root (§1b). This is the caveat ExportReplay PARTIAL named; it remains open, not claimed here.

## 5. Base "before" values (reproduced at 69de8d3)

Command (in base clone): `python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|entries='`
```
FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91
entries=42 pass=42 exit=0
```
Also `python3 corpus/instruments/capture-binding-check.py | tail -1` → `records=74 bound=74 unbound=0` (exit 0); `ls corpus/knowledge/*.md | wc -l` → 77; `grep -cE '^\| F40 ' corpus/README.md` → 0 (grep exit 1, no match); census exit 0. All match the frozen "before" line.

## 6. Entry claims vs. the capture (frozen sentence content)

Capture: L/corpus/source-snapshots/round-59/S092.txt (6371 bytes, sha256 048937…).
Command: `python3 -c "import json; ... manifest['sources'] S092 quotes"` (manifest quotes Q1–Q10) and `grep -o -- <pattern> S092.txt | wc -l`:
```
goo.gle/bigsleep: 5
savedsearches/7155917: 0
industry standard: 2
disclosure trial: 2
Project Zero: 4
Product: 1
Reported: 1
Fixed: 1
Impact: 2
```
Pinned quotes (all verified by source-recheck, §1b): Q1 '[Big Sleep] README'; Q2 'research. Findings from the project will be publicly disclosed following [Google'; Q3 'All issues reported by the project so far can be found [here](https://goo.gle/bigsleep)'; Q4 'Impact of the vulnerability'; Q5 'Software product the vulnerability was found in'; Q6 'Date when the bug was reported'; Q7 '["High","Medium","Low","None"]' (four-value Impact enum); Q8 'Date when the bug was fixed'; Q9 'null,"2025-07-08",[[null,"7/8/2025"]]'; Q10 '[Project Naptime: …]'. The "industry standard" and "disclosure trial" hits are the Q2 link text and its Project Zero 2025 reporting-transparency context (capture contains `googleprojectzero.blogspot.com/2025/07/reporting-transparency.html`). **Reproduced.**

Not re-verified by me: `savedsearches/7155917` does not occur in the capture (0 hits). The frozen sentence's "goo.gle/bigsleep resolves to the saved search savedsearches/7155917" rests on the pre-freeze control L/.ufo/waves/round-59/controls/s092-opens-r59.txt:64 (`code=200 final=https://issuetracker.google.com/savedsearches/7155917`), and on round-35 L/.ufo/waves/round-35/wave1/ScoutLeads.md:19. I did not re-fetch the network; this is a recorded control, not a seat-reproduced number.

Entry header (corpus/knowledge/google-big-sleep-findings-tracker.md:4–6) carries `source: S092 — https://issuetracker.google.com/issues/430375499 — capture corpus/source-snapshots/round-59/S092.txt …` and `ground: F40`. The kill-rule requirement ("entry header cites S092 with 'ground: F40'") holds.

## 7. Scope audit (tip commit 472737847 file list)

`git -C L show --stat 472737847` lists 10 files: README.md, PROVINCE.md, SKILL.md, SOURCES.md, knowledge-expected.txt, knowledge/google-big-sleep-findings-tracker.md, figure-audit.py (C1 territory, not this seat), and round-59 controls. No C2-relevant file outside the frozen set. The frontier census reads `registry=92` = 91 base rows + S092.

## 8. Cleanup

Scratch removed at yield: /fast/scratch/hyaku/kasegi-r59/ReviewerC2 (contains the two clones tmp.ZKaAeFp9cV/clone and tmp.FGPZ5R4iqT/base and output files). Nothing written to L except this evidence file. No git mutation against L; no commits; no pacman; no installs.

## 9. Findings / residual

- No C2 number fails. No new defects in the F40 admission found within scope.
- Residual (not claimed, recorded): the entry recheck line's absolute `cd` path (§4); the `savedsearches/7155917` resolution is a pre-freeze control, not re-fetched here (§6).
- The census "W04" duplicate-url warnings are pre-existing (identical at base), not introduced by S092.
