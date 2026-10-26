# ScoutDatawalk receipt (round 33, wave 1) — planner data-walk of the frozen BEFORE values

Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Freeze commit 6e55c8d58a3e63efe11c0df47068bfc479bfc8e0. Base 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4.
Read-only seat: no lane writes except this receipt. Runs used `PYTHONDONTWRITEBYTECODE=1`. Scratch `$HYAKU_SCRATCH/kasegi-r33/ScoutDatawalk/` (a `git archive` of the freeze commit) was removed before yield (`ls /fast/scratch/hyaku/kasegi-r33` no longer lists it).
Model: not asserted (config route table decides).

## 0. Quiescence / identity

```
$ git rev-parse master            -> a6a502351bb90c8cd6d9b8f45f55109b7848e0d1
$ git rev-parse 6e55c8d^{commit}  -> 6e55c8d58a3e63efe11c0df47068bfc479bfc8e0
$ git rev-parse 690b69d^{commit}  -> 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
$ git merge-base --is-ancestor 6e55c8d HEAD ; echo $?   -> 0
$ git diff --name-only 6e55c8d HEAD
.ufo/waves/round-33/build-spec.py
.ufo/waves/round-33/wave1-dispatch.json
.ufo/waves/round-33/wave1-plan.err
.ufo/waves/round-33/wave1-plan.out
.ufo/waves/round-33/wave1-run.err
.ufo/waves/round-33/wave1-spec.json
$ git diff --name-only (tracked-modified in working tree) | wc -l -> 0
```

FINDING N1: `master` is `a6a5023` ("round-33: wave-1 spec ... dispatch"), a child of the freeze commit `6e55c8d`, not `6e55c8d` itself. The diff 6e55c8d..a6a5023 touches only `.ufo/waves/round-33/*` wave-1 spec files — no `corpus/`, `SKILL.md`, `LOG.md`, instruments. So every corpus counter below is the same on `master` and on `6e55c8d`. Counters were run on a `git archive 6e55c8d` tree (quiescent, M30-3) and, where the instrument is path-sensitive (recheck-audit), on the live lane, which had zero tracked modifications at run time.

## 1. C1 BEFORE values

### 1a. Instrument absent
```
$ ls corpus/instruments/capture-binding-check.py
ls: cannot access 'corpus/instruments/capture-binding-check.py': No such file or directory
ls_exit=2
```
Agrees with `.ufo/waves/round-33/c1-controls/before.txt` (`ls_exit=2`).

### 1b. Manifest audit (claims.json counter command 3 on the freeze tree)
```
corpus/source-snapshots/round-23/manifest.json records= 4 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-24/manifest.json records= 19 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-25/manifest.json records= 5 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-26/manifest.json records= 1 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-28/manifest.json records= 2 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-29/manifest.json records= 3 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-30/manifest.json records= 3 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-31/manifest.json records= 1 url= 0 fetched= 0 archival= 0
corpus/source-snapshots/round-32/manifest.json -> FileNotFoundError (no manifest)
TOTAL records=38 with_url=0 with_fetched_utc=0
```
MATCHES the frozen `records=38 with_url=0 with_fetched_utc=0`. Record key set of all 38 records: `('id','path','quotes','sha256')` (38/38) — no `url`, no `fetched_utc`, no `archival` key. Manifest top-level keys: `schema_version, purpose, sources`.

### 1c. Round-32 snapshot dir has no manifest
```
$ ls corpus/source-snapshots/round-32
S049.txt
S050.txt
(no manifest.json)
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
manifest UNAVAILABLE reason=missing
recheck49_exit=2
```
MATCHES the frozen control. Snapshot-dir inventory at freeze (files / manifest): round-23 5/y, round-24 20/y, round-25 6/y, round-26 3/y, round-28 3/y, round-29 4/y, round-30 4/y, round-31 2/y, round-32 2/**n**. So Rule A has exactly one failing directory at base (round-32). Dir names present: round-23..26, 28..32 (no round-27).

### 1d. recheck-audit
First run on the `git archive` tree (path differs from the lane root, so the `cd <lane> &&` limb (d) fails by construction — PRE-STATE/non-comparative, not a defect):
```
strict pass=1/44 cdroot_fail=43 ... exit=1   (archive tree, wrong root; NON-COMPARATIVE)
```
Authoritative run on the live lane root (zero tracked modifications):
```
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
```
MATCHES the expected strict pass=44/44 exit 0. NOTE: this value moves when the F16 entry lands (a 45th `recheck:` line / `knowledge-expected.txt` 46 -> 47 lines; currently 44 entries in corpus/knowledge, 46 lines in knowledge-expected.txt — the expectation file also holds non-entry lines; not asserted here). Any after-column must be a fresh run on landed bytes, not this one.

### 1e. Frontier harness (BEFORE)
```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -1
entries=18 pass=18 exit=0
harness_exit=0
```
MATCHES entries=18 pass=18. (Last rows: `PASS F14 ... ids=S041,S046,S047`, `PASS F15 ... ids=S048`.) Full 18-row listing is frozen in `c2-controls/before.txt`.

## 2. C2 BEFORE values (claims.json counter commands, freeze tree)
```
frontier admitted (awk on corpus/README.md)         15
echo -n 'S049='; grep -lE '^source: S049 ' knowledge/*.md | wc -l   S049=0
echo -n 'S050='; ...                                                S050=0
grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md      0
grep -cE '^\|[[:space:]]*S050[[:space:]]*\|' corpus/SOURCES.md      0
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md 48
```
MATCH `c2-controls/before.txt` (15 / 0 / 0 / 0 / 0 / 48). Sanity on the `source: Sxxx ` pattern: `grep -lE '^source: S048 '` returns 1 (the F15 entry), whose line reads `source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "..."`, so the pattern with trailing space is valid for the F16 entry as long as it uses the same `source: S049 — <url> — section ...` shape.

### Census
```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi   (live lane)
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```
(archive tree via `--file corpus/SOURCES.md kasegi`: identical two W04 lines, exit 0.) MATCHES `census-before.txt`.

## 3. Predicate sentences vs counter commands — agreement check

C1:
- "prints `records=40 bound=40 unbound=0` exit 0" <-> counter 1: agrees with the interface contract (38 base + 2 = 40).
- "`--selftest` failures=0, exit 0" <-> counter 2: agrees.
- "38 pre-round-32 records carry `archival: true`", "round-32 records carry `fetched_utc`" <-> counter 3 counts `'archival' in s` and `'fetched_utc' in s` (KEY PRESENCE, not value). Agreement holds only if round-32 records do NOT carry an `archival` key at all. The contract text for the round-32 records reads `"archival": false-freezed` (garbled). If ExecManifest32 writes `"archival": false`, counter 3 would print `archival= 2` on the round-32 manifest while the predicate wants 38 `archival: true` — a counter/predicate divergence. Recommendation: round-32 records omit `archival` entirely (counter 3 then shows round-32 `fetched=2 archival=0`; total archival=38).
- Counter 3 prints per-manifest lines only (no grand total) and has no `id->SOURCES.md` check; the predicate's "url matches exactly one registry-row URL" is verified only by the instrument (counter 1), not by counter 3.

C2: predicate sentence items (15 -> 16; 1 entry per S049/S050; 1 row each; 48 -> 50; census W04 only; harness 19/19 incl. PASS F16 ids=S049,S050; source-recheck exit 0 for both) correspond one-to-one to the nine counter commands. No divergence found.

## 4. FINDING N2 (affects the C1 predicate; decision for the L1) — Rule B literal reading yields bound=38, not 40

Rule B (contract): "`url` must match EXACTLY ONE `corpus/SOURCES.md` registry-row URL (... 0 or 2+ matches = failure, name the record id)". Dry-run on the freeze `SOURCES.md` (substring match of the record's row URL against registry rows):

```
$ grep -nF 'https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq' corpus/SOURCES.md
12:| S006 | HackerOne Safe Harbor Overview and FAQ — https://docs.hackerone.com/en/...        (mined)
34:| S028 | HackerOne Safe Harbor Overview and FAQ, duplicate-row proposal — https://docs...  (REJECTED row)
-> 2 rows
$ grep -nF 'https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng' corpus/SOURCES.md
30:| S024 | Regulation (EU) 2024/2847, Cyber Resilience Act — https://eur-lex...             (mined)
35:| S029 | Regulation (EU) 2024/2847, CRA manufacturer reporting clocks — https://eur-lex...  (mined, "supersedes S024")
-> 2 rows
```
All 38 other legacy records match exactly 1 row. Records affected: round-24 `S006` and round-23 `S029` (the two census W04 duplicate-URL pairs). Under the literal "exactly one row URL" rule these two records are unbound, so the checker would print `records=40 bound=38 unbound=2` exit 1 and the predicate `bound=40` could not be met. Resolutions the L1 / ExecCaptureBinding must pick (this seat does not pick for them): (i) Rule B counts matches among rows whose id equals the record `id` (record id's own row must carry the URL, exactly once) — satisfies S006/S029 and still fails a record whose id's row lacks the URL; (ii) keep a global-uniqueness rule but exempt rows that are `rejected` or superseded (S028 rejected; S024 superseded by S029) — then S029's row itself still has to be distinguished from S024. Option (i) is the smaller change; the fake/mutant `accept-url-not-in-registry` still fails under it. The same duplicate pair is why census W04 S028/S029 remains in the "no new E/W" baseline — it is unaffected.

Other data points for Rule B/C implementers:
- Registry URL is written `Title — https://...` in the row's second cell (col 1 after id), no backticks, so a regex `https?://[^\s|`<>)\]]+` over the source cell recovers it byte-exactly for all 38 legacy ids (every record id has a row; no NOROW).
- `S041` appears as a record in three manifests (round-26, round-28, round-30) with one registry row — no within-manifest duplicate ids (checked), so duplicates are cross-round only; summary `records=40` counts them separately (38 + 2).
- No round-32 row exists yet in SOURCES.md (S049/S050 absent), so Rule B for the round-32 records can only pass after ExecRegistryAppend lands; the checker run for citation must be on quiescent landed bytes.
- Capture commit `288ea9ac17a78dce644388af35b89aa96b7994da`: author time and committer time both `2026-10-25T23:14:00-03:00` (`git log -1 --format='%H %aI %cI'`), matching the contract's `fetched_utc` source (note: that is -03:00 local; UTC is 2026-10-26T02:14:00Z — ExecManifest32 must pick one explicit form and the checker should not require a particular zone).

## 5. do-nothing / fake-checker controls re-read
`c1-controls/fake-checker-receipt.txt`: `records=38 bound=38 unbound=0 fake_exit=0` (fake). The real checker on base bytes must exit 1 and name unbound records (all 38 lack url/provenance; round-32 dir lacks a manifest). Verified inputs support that: with_url=0, with_fetched_utc=0, no archival key anywhere, round-32 has no manifest.

## 6. `git status --porcelain --untracked-files=all` (untracked entries)
Two samples (the tree was filling with wave-1 receipts as seats started):
```
?? .ufo/waves/round-33/l1-ref/sid-url.tsv
?? .ufo/waves/round-33/wave1.ready
?? .ufo/waves/round-33/wave1/swarm-registry.json
```
then
```
?? .ufo/waves/round-33/l1-ref/sid-url.tsv
?? .ufo/waves/round-33/wave1.ready
?? .ufo/waves/round-33/wave1.ready.dispatched      (content: 2026-10-26T01:16:32)
?? .ufo/waves/round-33/wave1/swarm-registry.json
```
(plus `.ufo/waves/round-33/wave1/*.md` seat receipts as they appear, incl. this one). No tracked file modified; no untracked file under `corpus/`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `SCORECARD.md`. Pre-existing untracked path `.ufo/waves/round-33/l1-ref/sid-url.tsv` is the L1's reference file (not mine).

## 7. Scratch / tooling
No tool installed. Scratch dir removed (confirmed by `ls /fast/scratch/hyaku/kasegi-r33` after `rm -rf`, no `ScoutDatawalk` entry). No git/jj mutation run; read-only `git rev-parse/diff/log/show/status/ls-files/merge-base` only.
