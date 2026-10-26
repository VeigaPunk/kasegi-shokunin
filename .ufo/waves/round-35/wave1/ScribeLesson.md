# ScribeLesson — round-35 lesson (`corpus/lessons/round-35.md`)

Seat: `ScribeLesson` (scribe, leaf; no subagents, no `agent://all`, no write outside the lane). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `3266c9937b03062d9bbc2f436e20820115ed179c`,
claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`, wave-1 dispatch `da2d3c68…`.
Composition window: `2026-10-26T06:32Z`–`06:59Z` while the wave was still landing.
Production path written: **`corpus/lessons/round-35.md` only** (`76eb3204…`, 533 lines, 48,016 B).
No git/jj mutation; no commit; no package or network tool run.

## Report

### 1. Composition snapshot (`2026-10-26T06:50:44Z`, worktree)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ   -> 2026-10-26T06:50:44Z
$ git rev-parse HEAD            -> da2d3c687f82a9814ee71c91c930cb733050d37c
```

Lane state at that instant (`git status --porcelain`): ` M .ufo/waves/round-35/build-spec.py`,
` M SCORECARD.md`, ` M SKILL.md`, and untracked: `.ufo/waves/round-34/wave1-results.json{,.provenance.md}`,
`.ufo/waves/round-35/{assimilation/,c1-controls/fake-suite.sh,c2-controls/junk-f18.md,claims-erratum-d5.md,wave1.ready,wave1.ready.dispatched,wave1/}`,
`corpus/instruments/r35-defect-closure.sh`, `corpus/instruments/r35-fixtures/`,
`corpus/knowledge/cisa-kev-catalog.md`, `corpus/source-snapshots/round-35/`.

Wave shape (read, not assumed):

```
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-35/wave1-dispatch.json'));print(d['counts'],d['policy']['maxLanes'])"
{'spawn': 64, 'resume': 0, 'total': 64} 128
$ python3 -c "...Counter(i['role'] for i in spec['items'])"
executor 18, scribe 12, reviewer 10, scout 6, mutation-tester 5, critic 5, connector 4, sentinel 2, simplifier 2
```

### 2. Before-controls replay (independent of the seats that own it)

```
$ git archive 617496b9c6e92bc671e7e78b83df69a04470d0e9 | tar -x -C $S/base   # exit 0
$ cd $S/base
$ ls corpus/instruments/r35-defect-closure.sh            -> No such file or directory; ls_exit=2
$ grep -c 'filled by the L1' SCORECARD.md                -> 1
$ grep -c 'c1c6a5f' SCORECARD.md                         -> 0
$ grep -c '201\.7' SCORECARD.md; grep -c '201\.2' ...    -> 2 / 0
$ grep -c 'r-defect-closure' SKILL.md; ... kill-rule-check -> 0 / 0
$ grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md -> 1
$ grep -c 'Correction (round 35)' <same file>            -> 0
$ grep -c 'supersedes R22' corpus/QUALITY.md; R23        -> 0 / 0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md             -> 17
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' ...       -> 0
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l -> 0
$ ls corpus/knowledge/*.md | wc -l                       -> 46
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l -> 0
```

All 18 values match `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`.

### 3. After-side measurements (each command run by this seat, exit code recorded)

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1                                                   exit=1

$ bash corpus/instruments/r35-defect-closure.sh --selftest
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest judge=forged-summary rejected=1 / forged-caselines rejected=1 / short-report rejected=1
selftest judge=fake-suite rejected=1 / fake-plain rejected=1
selftest problem=self-report status=1                               exit=1
  (failures=3 = D4/D6/D7 live limbs open on the uncommitted tree; green target proven reachable)

$ grep -c 'filled by the L1' SCORECARD.md                -> 0
$ grep -c 'the L1 fills this line' SCORECARD.md          -> 0   (the prose spelling D1's check cannot see)
$ grep -c 'c1c6a5f' SCORECARD.md                         -> 3
$ grep -c '201\.7' SCORECARD.md                          -> 4  (2 stale + 2 in the erratum)
$ grep -c '201\.2' SCORECARD.md                          -> 2
$ grep -c -F 'r35-defect-closure' SKILL.md               -> 0  (the round's own gate unregistered)
$ grep -c -F 'r-defect-closure' SKILL.md                 -> 4
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md             -> 18
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md      -> 1
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l            -> 1
$ ls corpus/knowledge/*.md | wc -l                                   -> 47
$ python3 corpus/instruments/frontier-recheck-count.py               -> entries=21 pass=21 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK / S052:Q1..Q5 OK occurrences=1 anchor={2,3,4,15472,19165}-ok      exit=0
$ python3 corpus/instruments/recheck-audit.py
strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0
expect=present expected=47 missing=0 unexpected=0                exit=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi W04 S028 … / kasegi W04 S029 … / kasegi ok …/corpus/SOURCES.md
census_exit=0
```

No-harm (this seat, `06:48–06:50Z`):

```
$ python3 corpus/instruments/density.py <freeze SKILL.md>  -> mean 201.2, 25 blocks, 711 cites, 1091 lines
$ python3 corpus/instruments/density.py SKILL.md           -> mean 220.9, 26 blocks, 742 cites, 1104 lines
$ python3 corpus/instruments/anchorcheck.py SKILL.md       -> 16 in-range, 0 bad, BASE-ABSENT=0, exit 0
   (base export, same instrument: 12 in-range, 0 bad, BASE-ABSENT=0, exit 0)
$ python3 corpus/instruments/anchorcheck.py PROVINCE.md    -> 0 in-range, 0 bad, exit 0 (both sides)
$ git diff --numstat 3266c993…                             -> SCORECARD.md 33 15; SKILL.md 13 0;
   corpus/README.md 28 0; corpus/SOURCES.md 7 0; knowledge-expected.txt 1 0;
   PROVINCE.md / LOG.md / corpus/QUALITY.md absent
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -ci 'kasegi\|round-35' -> 0
```

Caveat this seat hit and corrected rather than reported as a finding: `anchorcheck.py` on a copy of
`SKILL.md` outside the lane resolves the root differently and prints `BASE-ABSENT=12` with
`0 in-range`; the valid before-measurement is the one run **inside** the extracted tree (above).

### 4. Receipt coverage at composition

```
$ python3 - <<'PY'  # spec names vs wave1/*.md stems
filed 57 of 64; missing: ExecCensusAfter ExecDoNothingReject ExecRegressionC1 ScribeLesson
                          ScribeScorecard ScribeShonen SentScopeFinal
PY
$ ls .ufo/waves/round-35/wave1/*.md | wc -l        -> 58 (57 spec-named + ConnSibling-ruling-draft.md)
$ cat .ufo/waves/round-35/wave1/*.md | wc -l       -> 16,166
$ du -sb .ufo/waves/round-35 | cut -f1             -> 2,461,510
$ du -sb .ufo/waves/round-35/wave1 | cut -f1       -> 1,253,805
```

Answering-model scan over the receipts: `grep -inE 'answering model|opencode-go/|anthropic/[a-z0-9.-]+|deepseek-v|claude-[a-z0-9-]+' *.md`
→ three files, of which only one self-identifies (`wave1/ScoutPackageThemes.md:3`,
`anthropic/claude-sonnet-5-5`); the other two are a `⟨FILL⟩` prompt and a note that attribution is not
a criterion.

### 5. Lesson digests and section map

| path | bytes | lines | sha256 |
|---|---|---|---|
| `corpus/lessons/round-35.md` (this seat's only production write) | 48016 | 533 | `76eb320445a3d4be1fe1a36e34653adacb057a3f4c5eff07623dc9407e657ff2` |
| `.ufo/waves/round-35/wave1/ScribeLesson.md` (this receipt) | — | — | not self-pinned |

Sections in order: header (revisions/shape/model note) → `## Frozen claims — before → after` →
`## Gate` (F18 admittance · rejects/entry review · quarantine slice · id-collision · standing refusals ·
assimilation none · contested scope none) → `## Mistakes` (M35-1 + provisional M35-2…M35-10) →
`## considerthese` (proposal 2 → R26, plus R27 and five dispositions) → `## Census before → after` →
`## No-harm` → `## Open items / unverified` (17 items) → `## Touched surfaces and provenance`.

### 6. Cross-check of lesson claims against receipts

Every receipt citation in the lesson was opened by this seat. Mechanical cross-check:

```
$ python3 …  # extract wave1/<name> tokens from the lesson, compare to the file set and to § Touched surfaces
cited-not-existing: L1Integration (round-34 path), ScribeLesson (this seat)   — both explained in text
cited-not-listed:   ConnSibling (marked "this seat did not open" in the text),
                    L1Integration, ScribeLesson                                — as above
```

Two student-visible corrections made during composition rather than shipped:

1. `wave1/RevD5D6D7.md:78` reads `pending — finalized in §4/§Verdict when D6/D7 land`; an earlier draft
   of the C1 row cited it as certifying D5. Replaced with `wave1/ScribeErratumD5.md` + this seat's own
   count of the two literals in `claims-erratum-d5.md` (`×5`/`×5`).
2. `wave1/ScribeMistakesDraft.md` M35-7 states the CISA count as 5 against a bullet saying 7; measured
   here: **5** registry rows and **7** whole-file lines (two are search-log bullets). The lesson prints
   both and adopts neither as a single figure (Open item 15).

### 7. Peer coordination

- `ScribeEntryDiscordHeaders` (IRC, mid-composition) asked this seat to add an S117 gate line to
  `corpus/lessons/round-30.md` §Gate. Declined in writing: this seat owns `round-35.md` only, S117 is
  not in round-35's frozen claims, and R6 forbids moving cited lines in a historical lesson. The seat
  was told to route the request to the round-30 owner or the L1.
- No other peer message sent or received.

### 8. Scratch and tooling

- Scratch root used: `/fast/scratch/hyaku/kasegi-r35/ScribeLesson/` (a freeze export, two measurement
  logs, a suite selftest log and a `util/` scratch base for the instrument's `KASEGI_SCRATCH`).
  Removed with `rm -rf --`; verified:

```
$ test -d /fast/scratch/hyaku/kasegi-r35/ScribeLesson && echo PRESENT || echo scratch-absent
scratch-absent
$ ls /fast/scratch/hyaku/kasegi-r35
ExecCensusAfter  ExecDoNothingReject  ExecRegressionC1  SentScopeFinal
```

  The four remaining directories belong to seats that had not filed a receipt at composition
  (`§ 4`); this seat wrote none of them and deleted none of them.
- Tools installed/upgraded: **none**. Commands used were host `bash`, `git` (read-only), `python3 3.14.8`,
  `sha256sum`, `grep`, `awk`, `du`, `wc`. No `pacman`/`uv`/`npx`/`cargo` transaction; no network fetch.

Report: .ufo/waves/round-35/wave1/ScribeLesson.md
