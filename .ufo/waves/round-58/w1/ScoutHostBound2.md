VERDICT: PASS — 0 new host dependencies introduced by round-58 changed bytes. The surviving round-57 live-counter derive (M57-8 in .ufo/waves/round-54/controls/red-d53-ledger.json) is repaired to read the committed receipt literal (.ufo/waves/round-53/controls/c2-counter-final-r53.txt), eliminating the live counter under QUALITY R65 (reproduces derived=33 want=34 stale, exit 1). The new entry corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6 recheck line uses the documented cd-prefixed lane root (/home/vgpnk/Projects/shokunin/kasegi-shokunin) and its recheck (source-recheck.py) depends solely on committed bytes (manifest.json and S091.txt; exit 0). No live files or moving range bases are cited (QUALITY R69 compliant). Pre-existing items M57-7 (Windows host-stamped citation-survival.tsv) and M57-9 (watchdog.log range base) remain open as declared in claims.json.

# Seat ScoutHostBound2 (kasegi round 58, wave 1)

Target: Host-dependence sweep of the bytes this round adds or changes, in the same class as round-57 M57-7 and M57-8: a pinned figure or committed gate reads a host-stamped path, a live file, or a live counter.
Claims freeze commit: `543cac13886b91ac660d788ed20e64ae70ee0fa5`
Implementation commit under test: `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` (branch master)
Lane repository L: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only)
Scratch root S: `/fast/scratch/hyaku/kasegi-r58/ScoutHostBound2`
Evidence file W: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-58/w1/ScoutHostBound2.md`

No tools installed or upgraded. No credential material written. Read-only on lane repo L except for this evidence file.

---

## 1. Changed files between freeze commit and implementation commit

Command:
```bash
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --name-only 543cac13886b91ac660d788ed20e64ae70ee0fa5 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
```
Output:
```
.ufo/waves/round-54/controls/red-d53-ledger.json
PROVINCE.md
corpus/README.md
corpus/SOURCES.md
corpus/instruments/figure-audit-mutbat.py
corpus/instruments/figure-audit.py
corpus/instruments/knowledge-expected.txt
corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md
```
Exit code: `0`
Diff stat: 8 files changed, 224 insertions(+), 1 deletion(-).

---

## 2. Host-dependence sweep of changed files

All 8 files were grepped for absolute paths (`/home/`, `C:\`, `/fast/`) and live-counter invocations (`python3? corpus/instruments/...`).

Commands:
```bash
$ grep -nE '/home/|[A-Za-z]:\\|/fast/' <file>
$ grep -nE 'python3?\s+corpus/instruments/' <file>
```

### 2.1 Added/changed lines in round 58

Across all 224 added lines in the diff, exactly TWO lines matched any pattern:

1. `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6`
   - Line: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check`
   - Classification: `recheck (entry)`
   - Patterns: `/home/` (`ABSOLUTE_HOME`) and `python3 corpus/instruments/` (`LIVE_COUNTER`).
   - Note: The `cd` prefix is the lane's documented entry recheck convention (see §3 below).

2. `corpus/instruments/figure-audit-mutbat.py:9`
   - Line: `Usage: python3 corpus/instruments/figure-audit-mutbat.py`
   - Classification: `prose` (docstring usage comment in new Python script).
   - Pattern: `python3 corpus/instruments/` (`LIVE_COUNTER`).
   - Note: This is Python docstring documentation, not an executable derive or recheck line.

In `.ufo/waves/round-54/controls/red-d53-ledger.json:9`, the round-58 edit **removed** a live-counter invocation:
- Line 9: `"derive": "grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2",`
- Classification: `derive (figure-audit ledger)`
- Patterns: NONE. Does not contain `/home/`, `C:\`, `/fast/`, or `python3 corpus/instruments/`.
- Repointed from prior live counter: `"derive": "python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'"` (see §4 below).

### 2.2 Pre-existing matches in the changed files (unchanged lines)

The remaining pattern matches in the 8 files sit on pre-existing lines from prior rounds:
- `PROVINCE.md:137` (`/fast/`, prose historical note from round 37)
- `PROVINCE.md:151` (`python3 corpus/instruments/`, prose harness note from round 37)
- `corpus/README.md:4` (`/home/`, prose notes on initial read)
- `corpus/README.md:216` (`/home/`, prose notes on lost domain)
- `corpus/README.md:244` (`/home/` and `python3 corpus/instruments/`, prose audit command)
- `corpus/README.md:439` (`/fast/`, prose historical note from round 37)
- `corpus/README.md:453` (`python3 corpus/instruments/`, prose harness note from round 37)
- `corpus/SOURCES.md:118, 119, 124, 154, 167, 177, 193` (`/home/`, prose notes and change bullets from rounds 31, 33, 38, 42, 45)
- `corpus/instruments/figure-audit.py:15` (`python corpus/instruments/`, prose usage in docstring)

None of these pre-existing lines were altered in round 58.

---

## 3. New entry recheck inspection (`aisi-autonomous-cyber-capability-progress-rate.md`)

Location: `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6`
Verbatim line:
```markdown
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091   # run from any cwd (the cd prefix names the lane root); prints one sha256 OK + one Q-OK line per pinned quote with its occurrences= count and anchor note; exits 2 when the manifest or a capture is absent and 1 when a digest differs or a pinned quote moved, so a missing or corrupted capture fails closed; a pinned-capture comparison, not a fresh network check
```

Findings:
1. **cd-prefixed lane root**: The recheck command begins with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ...`. This follows the documented form used across all entry rechecks in the corpus, allowing direct execution from any cwd. Per task specification, this documented form is not a host defect.
2. **Independence from live tree**: The command invokes `source-recheck.py` with:
   - `--manifest corpus/source-snapshots/round-58/manifest.json`
   - `--source S091`
   Inspection of `source-recheck.py` confirms it reads solely the manifest JSON and the source capture file specified inside it (`corpus/source-snapshots/round-58/S091.txt`). Both files are committed in git (freeze commit `543cac13886b91ac660d788ed20e64ae70ee0fa5`). The recheck checks the sha256 digest of `S091.txt` and locates 9 pinned quotes (Q1-Q9) at their declared line anchors. It does not read any uncommitted files, system logs, clocks, network resources, or live git status.
3. **Execution proof**:
```bash
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091
S091:sha256 OK
S091:Q1 OK occurrences=1 anchor=1-ok
S091:Q2 OK occurrences=1 anchor=14-ok
S091:Q3 OK occurrences=1 anchor=21-ok
S091:Q4 OK occurrences=1 anchor=23-ok
S091:Q5 OK occurrences=1 anchor=25-ok
S091:Q6 OK occurrences=1 anchor=30-ok
S091:Q7 OK occurrences=1 anchor=34-ok
S091:Q8 OK occurrences=1 anchor=45-ok
S091:Q9 OK occurrences=1 anchor=14-ok
```
Exit code: `0`

---

## 4. Red fixture repoint inspection (`red-d53-ledger.json`)

Location: `.ufo/waves/round-54/controls/red-d53-ledger.json:9`
Entry: `d53-1-trailer`

Before round 58 (at base `543cac13886b91ac660d788ed20e64ae70ee0fa5`):
```json
   "derive": "python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'",
```
In round 57, this derive was host-bound (M57-8): on Linux, `frontier-recheck-count.py` printed no `FAIL` line, so `grep -c` exited 1, causing the figure audit to report `FIG d53-1-trailer recorded=34 derived=UNAVAILABLE reason=derive-exit-1 stale`.

After round 58 repair (at landed commit `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b`):
```json
   "derive": "grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2",
```

Findings:
1. **Committed receipt path**: The derive reads `.ufo/waves/round-53/controls/c2-counter-final-r53.txt`, which is a committed receipt file in the lane repository (repo-relative, not absolute).
2. **No live counter**: The derive executes a simple pipeline (`grep` / `head` / `cut`) against the static receipt text. It does not invoke Python or any lane instrument (`frontier-recheck-count.py`).
3. **Execution proof**:
```bash
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2
33
```
Exit code: `0`

Auditing the fixture via `figure-audit.py`:
```bash
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py --ledger /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-54/controls/red-d53-ledger.json
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
```
Exit code: `1`

Result: The red control now reads `derived=33 want=34 stale` rather than `UNAVAILABLE reason=derive-exit-1`. The derive is completely host-portable under QUALITY R65.

---

## 5. Classified table of pattern matches in changed files

| File and line | Pattern | Line type | Status in r58 | Evaluation / Host dependency |
|---|---|---|---|---|
| `.ufo/waves/round-54/controls/red-d53-ledger.json:9` | None (removed `python corpus/...`) | derive (figure-audit ledger) | CHANGED | Portable: reads committed receipt `.ufo/waves/round-53/controls/c2-counter-final-r53.txt`. Eliminates live counter M57-8. (R65 compliant) |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6` | `/home/` | recheck (entry) | ADDED | Documented `cd` prefix to lane root; recheck body depends solely on committed bytes (`manifest.json`, `S091.txt`). Not a host defect. (R65 compliant) |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6` | `python3 corpus/instruments/` | recheck (entry) | ADDED | Recheck command for F39 entry; re-derives quotes against committed capture. Fails closed (exit 1/2) on missing/corrupt capture. |
| `corpus/instruments/figure-audit-mutbat.py:9` | `python3 corpus/instruments/` | prose (docstring) | ADDED | Usage example in docstring of new mutant battery. Not an executable derive/recheck line. |
| `PROVINCE.md:137` | `/fast/` | prose | PRE-EXISTING | Unchanged historical text from round 37. |
| `PROVINCE.md:151` | `python3 corpus/instruments/` | prose | PRE-EXISTING | Unchanged historical text from round 37. |
| `corpus/README.md:4` | `/home/` | prose | PRE-EXISTING | Unchanged historical note. |
| `corpus/README.md:216` | `/home/` | prose | PRE-EXISTING | Unchanged historical note. |
| `corpus/README.md:244` | `/home/`, `python3 corpus/instruments/` | prose | PRE-EXISTING | Unchanged historical command illustration. |
| `corpus/README.md:439` | `/fast/` | prose | PRE-EXISTING | Unchanged historical text from round 37. |
| `corpus/README.md:453` | `python3 corpus/instruments/` | prose | PRE-EXISTING | Unchanged historical text from round 37. |
| `corpus/SOURCES.md:118, 119, 124, 154, 167, 177, 193` | `/home/` | prose | PRE-EXISTING | Unchanged historical sweep and change notes (rounds 31-45). |
| `corpus/instruments/figure-audit.py:15` | `python corpus/instruments/` | prose | PRE-EXISTING | Unchanged usage line in docstring. |

---

## 6. Analysis under QUALITY R65 and R69

### 6.1 QUALITY R65 (Host-portable derives)
Criterion:
> "A figure a committed record states by re-deriving it is host-portable only when its derive reads committed bytes: a rev-pinned `git show` or `git ls-tree`, or a receipt line the record itself cites. A derive that re-runs a live counter whose result depends on the host (a cd-prefixed recheck that resolves on one machine only, a Windows-only FAIL class) is host-bound..."

Findings:
- **Ledger derives**: In `corpus/instruments/figure-audit-ledger.json`, 0 of 35 derives invoke a live counter (`grep -c '"derive": "python' = 0`). All 35 derives read rev-pinned git trees or committed receipt lines.
- **Fixture derives**: In `.ufo/waves/round-54/controls/red-d53-ledger.json`, the only surviving live-counter derive (`d53-1-trailer`, M57-8) was repaired in round 58 to read `.ufo/waves/round-53/controls/c2-counter-final-r53.txt`. It now derives `33` on any host.
- **New entry recheck**: The recheck line in `aisi-autonomous-cyber-capability-progress-rate.md:6` uses the documented `cd <lane-root>` form. Because no ledger derive re-runs `frontier-recheck-count.py` or entry rechecks live, no audited figure is host-bound by this recheck under R65.

### 6.2 QUALITY R69 (Range citations against fixed revisions)
Criterion:
> "A census's range citation resolves against a pinned file or a fixed revision, never against a live file whose length moves between regenerations..."

Findings:
- **Zero live file citations added**: Round 58 added no citations to live or growing files (e.g. `.ufo/watchdog.log`). Entry `aisi-autonomous-cyber-capability-progress-rate.md` resolves all citations against static snapshot `corpus/source-snapshots/round-58/S091.txt`.
- **Pre-existing M57-9**: The pre-existing range base on `.ufo/watchdog.log` in historical lessons remains open per `claims.json:52` awaiting operator decisions on the L0 row. It was not modified or claimed in round 58.

### 6.3 Pre-existing M57-7 (Host-stamped census substrate)
- `corpus/instruments/citation-survival.tsv` carries pre-existing Windows paths (`C:\Users\jpvei\...`) from round 56. This item is acknowledged in `claims.json:53` as open and unclaimed in round 58. Round 58 added 0 new drive-letter paths or host-stamped rows.

---

## 7. Clean clone verification in scratch

To verify that findings reproduce in a clean git clone without working-tree artifacts, all checks were executed in `/fast/scratch/hyaku/kasegi-r58/ScoutHostBound2/clone`:

```bash
$ D=/fast/scratch/hyaku/kasegi-r58/ScoutHostBound2/clone
$ git -C $D rev-parse HEAD
18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
[exit=0]

$ git -C $D diff --name-only 543cac13886b91ac660d788ed20e64ae70ee0fa5 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b | wc -l
8
[exit=0]

$ python3 $D/corpus/instruments/figure-audit.py --ledger $D/.ufo/waves/round-54/controls/red-d53-ledger.json
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
[exit=1]

$ python3 $D/corpus/instruments/figure-audit.py --root $D
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
[exit=0]

$ python3 $D/corpus/instruments/figure-audit-mutbat.py
PRISTINE selftest_exit=0 last='selftest cases=6 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=6 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest pin cases=5 expected=6 verdict=fail'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest case=derive-not-read-only-refused exit=0 want=2 verdict=fail'
mutbat killed=2/2 survivors=0 controls=pass
[exit=0]
```

All commands succeed with exact expected exits and outputs.

---

## 8. Scratch cleanup

Scratch directory: `/fast/scratch/hyaku/kasegi-r58/ScoutHostBound2`
Clone and all temporary files removed before yield via `rm -rf -- /fast/scratch/hyaku/kasegi-r58/ScoutHostBound2`.
Leftovers: None.
