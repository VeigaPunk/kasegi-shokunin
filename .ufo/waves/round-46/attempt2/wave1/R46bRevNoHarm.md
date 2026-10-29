# R46bRevNoHarm — no-harm review, round 46 attempt 2 freeze payload

VERDICT: HOLDS, with one transient red (capture-binding-check) that the wave itself is committed to clearing.

Scope: diff `04af9bc92229232ea5cce8b32bfe59dd969eb26d`..`HEAD` (live lane, tip `ee03806`) restricted to paths OUTSIDE `.ufo/waves/round-46/attempt2`; for each, name the prior receipt that watches it and re-verify the cheap ones. All commands run by this seat against exports at `/fast/scratch/hyaku/kasegi-r46/R46bRevNoHarm/{base,live}` (git-archive exports of the frozen base and of HEAD; receipts copied to `R46bRevNoHarm.draft/` before scratch removal).

## The committed surface outside attempt2

`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat 04af9bc92229232ea5cce8b32bfe59dd969eb26d HEAD` (re-run by this seat) prints, outside `.ufo/waves/round-46/attempt2/**`, exactly:

| path | kind | watchers |
|---|---|---|
| `.ufo/waves/round-46/a2w1.ready` | +1 line (dispatch state) | no prior receipt watches wave ready-files |
| `corpus/instruments/r46-f29-gate.py` | new, 367 lines | none prior (instrument set is not enumerated by any gate; see §4) |
| `corpus/instruments/r46-mutbat.py` | new, 184 lines | none prior |
| `corpus/source-snapshots/round-46-a2/S074.txt` | new, 42 lines | capture-binding-check (round-32 C1 predicate); source-recheck (C2 claim) |
| `corpus/source-snapshots/round-46-a2/manifest.json` | new, 68 lines | capture-binding-check (round-32 C1 predicate) |

Everything the attempt-1 receipts pin is byte-untouched by the freeze commit:

- `git diff 04af9bc9..HEAD -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py corpus/knowledge corpus/README.md corpus/SOURCES.md LOG.md SCORECARD.md SHONEN.md corpus/lessons` prints nothing (re-run by this seat, exit 0).
- `sha256sum corpus/source-snapshots/round-46/manifest.json` → `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` (attempt-1 freeze pin MATCH).
- `sha256sum corpus/source-snapshots/round-46/S073.txt` → `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` (attempt-1 freeze pin MATCH).
- `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `65` (attempt-1 pinned 65-entry dir MATCH).
- SCORECARD.md / LOG.md: no diff entries between base and HEAD (append-only receipts unaffected).

## Finding 1 (MEDIUM, transient): the new S074 manifest breaks the round-32 capture-binding predicate at HEAD

Attack: run the round-32 C1 counter over the live export. The counter walks EVERY `corpus/source-snapshots/**` directory (capture-binding-check.py docstring lines 9-13, 271-278; snapshot dirs are defined by holding a `manifest.json`), and `round-46-a2/manifest.json` is committed at HEAD while its S074 registry row is not (the wave lands the row as C2's after-state).

Command and output (this seat, live export):

```
$ python3 $S/live/corpus/instruments/capture-binding-check.py --root $S/live
...
MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=61 with_url=61 with_fetched_utc=23 with_archival=38 snapshot_dirs=23 manifest_dirs=23 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S074 dir=round-46-a2
records=61 bound=60 unbound=1
exit=1
```

Do-nothing control (base export, same environment):

```
$ python3 $S/base/corpus/instruments/capture-binding-check.py --root $S/base
...
records=60 bound=60 unbound=0
exit=0
```

The round-32 C1 predicate sentence (`.ufo/waves/round-32/claims.json`, re-asserted as a live capability every round since) requires `records=R bound=R unbound=0` and exit 0. At the current HEAD that predicate reads `bound=60 unbound=1`, exit 1 — the freeze commit alone turned the r32 capability counter red. Watching receipt: round-32 claims.json C1 `predicate_sentence` + kill rule ("the checker ... exits non-zero").

Mitigations observed (why this is transient, not structural): (a) the failure is exactly `rule=no-row` — the S074 manifest record itself is well-formed (`fetched_utc` strict UTC, `url` present, sha256 pin good: `sha256sum S074.txt` → `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, matching the freeze pin and the manifest record); `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` prints `S074:sha256 OK` + `S074:Q1..Q9 OK` (9/9 quotes located), exit 0. (b) The record's `url` equals the URL the C2 wave will register (docs.github.com repository-security-advisories), so once the S074 SOURCES row lands, binding returns to `unbound=0`. If the wave were abandoned at HEAD, the lane would ship with the r32 capability counter red — the L1 should treat landing the S074 row as blocking.

## Finding 2 (no-harm verified): counters and census are unmoved

- r46-c2-gate on the live export reproduces the attempt-1 landed verdict exactly:

```
$ python3 $S/live/corpus/instruments/r46-c2-gate.py --root $S/live
gate G1 pass=1 ... gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```

(identical on the base export — the freeze commit moved nothing G1-G7 watch, including G6 `knowledge=65 entries=65` and G7 census.)

- r46-c1-gate, live-vs-base against the do-nothing control, byte-identical readings (this seat; full output in `R46bRevNoHarm.draft/c1-gate-base-vs-live.txt`):

```
=== C1-GATE base-vs-base (do-nothing control) ===   === C1-GATE live-vs-base ===
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65   gate L1 pass=1 read=gated=22 broken=0 lines=65/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0           gate L2 pass=0 read=base-gated=22 regrounded=0
...(L3-L6 identical)...                                  ...(L3-L6 identical)...
gate L7 pass=1 read=still-gated=22 changed=none          gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=2/7 exit=1                                 c1-gate fixed=2/7 exit=1
```

(2/7 is the correct do-nothing reading at this base — root and baseline carry the same post-attempt-1 bytes, so `regrounded=0`; the attempt-1 7/7 required baseline `914ca0b`. The discrimination point is live == control byte-for-byte.)

- Census on the live export reproduces the attempt-2 before-receipt (`.ufo/waves/round-46/attempt2/controls/sources-census-before.txt`) exactly:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/live/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	$ S/live/corpus/SOURCES.md
exit=0
```

- `python3 corpus/instruments/r44-frontier-count.py --root $S/live --expect 28` → `frontier rows=28 admitted=28`, exit 0 (README untouched).
- The F28 entry's own recheck stays green: `source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` → all quotes OK, exit 0.

## Finding 3 (INFO): the new instruments are inert for every prior receipt

No committed instrument enumerates `corpus/instruments/` (grep over the instruments dir for `iterdir|listdir|glob(|rglob|scandir`: hits are per-file logic, fixtures, knowledge-dir walks, and `/proc` only). recheck-audit counts recheck lines in `corpus/knowledge/*.md` only; resolve.py's citation census walks `corpus/**/*.md` (the additions are `.py`/`.txt`/`.json`); the limb ledgers are static JSON naming pre-existing paths. `r46-f29-gate.py` and `r46-mutbat.py` cannot be reached by any prior counter — confirmed operationally by findings 2's identical base/live readings.

Hygiene observation (not a defect): `.ufo/waves/round-31/wave1/ExecCensusDry/validate/**/corpus/instruments` are symlinks to `../../../../../../../corpus/instruments`, so the two new .py files are visible inside those historical fixtures; nothing re-executes them and receipts over the fixtures are historical.

## Limitations

- I verified committed bytes only; the working tree carries other seats' in-flight draft edits under `.ufo/waves/round-46/attempt2/` (uncommitted, outside my scope; `git status --porcelain` shows them under attempt2 plus untracked `a2w1.ready.dispatched`).
- I did not re-run `freeze-check.py` for the attempt-1 claims (needs a full `914ca0b` export; the four prescribed cheap checks plus pinned-sha verification cover the named receipts). The attempt-1 `claims.json` itself is untouched by the freeze commit (no diff entry).
- capture-binding-check's `--live` network mode was not run (live-target testing is refused); the finding rests on the offline predicate, which is the committed counter.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevNoHarm` removed after receipts were copied into the draft dir; every command above was run by this seat against the named exports.
