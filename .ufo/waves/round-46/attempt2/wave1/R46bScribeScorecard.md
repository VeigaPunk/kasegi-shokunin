VERDICT: DRAFT-READY

# R46bScribeScorecard — round 46 (attempt 2), kasegi lane

Seat scope (single item): draft the `## Round 46 (attempt 2) result` table rows, the
`### Planned evidence gates for round 47` block, and the saturation line for
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md`, following the round-45 result-block
shape. Draft only.

Deliverable: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/scorecard.md`
(337 lines, sha256 `5bf0d124891f0aad22ec7db0ef95c88403408998b1ba2f4a8a3f3a99c0c3accc`), with two raw
receipts beside it in `R46bScribeScorecard.draft/receipts/`. Nothing tracked was edited; no commit, no
push, no mutating git/jj call. Scratch root
`/fast/scratch/hyaku/kasegi-r46/R46bScribeScorecard/` was removed on exit. No tooling was installed or
upgraded (`git`, `tar`, `sed`, `grep`, `awk`, `bash`, `python3` were already present; no `pacman`
transaction).

## What the draft says, and why

**All three axes are stated as held.** The draft reads the promotion criteria out of the Scorecard's
own `## Distance-to-next-score` section (`SCORECARD.md:1532`, `depth:verifiability, 4 → 5` at `:1536`,
`coverage, 7 → 8` at `:1547`) rather than inventing a criterion, and neither written promotion limb
moved:

- depth:verifiability limb 1 wants `gated=0`; this seat measured `executes=43 gated=22 broken=0` at the
  base export **and** at the live tip, so 22 gated lines remain. Limb 2 (the score-5 audit bar,
  `SCORECARD.md:331`) is untouched and only a non-author closure can grade it. Attempt 2's C1 works the
  counters' **mutation coverage**, not the gated recheck lines, so the axis number does not move.
- coverage has **no written 8 → 9 criterion** (`SCORECARD.md:1547` carries only `### coverage, 7 → 8`).
  The r22 ratio stays 1.000 (29 admitted of 29, queued registry rows 0), so F29 is an expansion count,
  not a ratio move. Same reading as the attempt-1 row at `SCORECARD.md:1789`.
- depth:density is a non-target guard: `density.py` is byte-identical base → tip.

## Findings

### F1 — the frozen C1 before-value reproduces at the base export (built: the draft's C1 row's control)

Built the base export with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d | tar -x -C <scratch>`, copied the frozen PURE export (`/fast/scratch/hyaku/kasegi-r46/L1/pure2`) to `<scratch>/pure` without editing it, then ran the claim's own counter command:

```
$ python3 corpus/instruments/r46-mutbat.py --root <base-export> --pure <pure-copy> --work <scratch> --counter both --jobs 8
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=8 verdict=caught
mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught
BATEXIT=124
```

`diff <(head -3 .ufo/waves/round-46/attempt2/controls/mutbat-before.txt) <(head -3 my run)` → **IDENTICAL
(3/3 lines)**; receipt digest `sha256sum` = `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`,
matching `freeze.txt`. `BATEXIT=124` is my own 2400-second wall clock on the run, **not** a counter
verdict — each mutant re-runs the whole selftest suite, and 20 c1 + 21 c2 mutants do not fit. The
committed receipt's summary lines (`mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7
baseline_failures=0` / `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13
baseline_failures=0`, `BATEXIT=1`) are therefore cited for the full before-value and my partial replay
is cited for the reproduction.

### F2 — both frozen selftest baselines re-run at the base export (built: the C1 plain measures)

```
$ python3 corpus/instruments/r46-counters-selftest-c1.py --pure <pure-copy> --work <scratch> --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
exit=0

$ python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure-copy>
selftest cases=137 failures=0
exit=0
```

Matches `controls/selftest-baselines.txt` (`cases=76 failures=0`, `cases=137 failures=0`).

### F3 — the C2 gate discriminates red at base and freeze, green on a projection of the wave-1 drafts (built: the C2 row's evidence)

```
$ python3 corpus/instruments/r46-f29-gate.py --root <base-export>
f29-gate fixed=1/7 exit=1
$ python3 corpus/instruments/r46-f29-gate.py --root <freeze-export-fe0f56b7>
f29-gate fixed=2/7 exit=1
$ python3 corpus/instruments/r46-f29-gate.py --root <projection>
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=10 xrefs=6/6 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=28 located=28 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

Do-nothing controls on the same fixture builder and the same gate: `--mode junk` → `fixed=6/7 exit=1`
(H5 `spans=7 located=2 failed=5`); `--mode fabricated` → `fixed=6/7 exit=1` (H5 `spans=7 located=5
failed=2`). The base export reproduces `controls/f29-gate-at-base.txt` exactly (`fixed=1/7 exit=1`).

The **projection** is a scratch tree: the freeze export plus the wave-1 drafts (entry draft A, the
S074 row from rows draft A, admission block (a), and the `knowledge-expected.txt` insert). It is not
the landed tree — the draft says so in three places and marks every tip-side value `<AT-LANDING: …>`.

### F4 — the coverage counters and plain counts, base vs projection (built: the C2 row's secondary and plain measures)

```
$ python3 corpus/instruments/r44-frontier-count.py --root <base-export> --expect 29
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1
$ python3 corpus/instruments/r44-frontier-count.py --root <projection> --expect 29
frontier rows=29 admitted=29
exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <base-export>
records=60 bound=60 unbound=0
$ python3 corpus/instruments/capture-binding-check.py --root <projection>
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
records=61 bound=61 unbound=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
…
S074:Q9 OK occurrences=1 anchor=38-ok
exit=0

$ python3 corpus/instruments/frontier-recheck-count.py --root <base-export>
entries=31 pass=31 exit=0
$ python3 corpus/instruments/frontier-recheck-count.py --root <projection>
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S074           exit=0
entries=32 pass=32 exit=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <base-export>/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	<base-export>/corpus/SOURCES.md
exit=0
```

Plain counts (base → projection): frontier rows 28 → 29; SOURCES rows 73 → 74; knowledge entries 65 → 66;
absence sweep files 2 → 4. The base sweep's two files are the F28 entry's scope-out notes and the S068
rejected-row search-log context — neither answers the maintainer-side lifecycle question.

### F5 — the promotion limb that did not move (built: the depth:verifiability row's "held" verdict)

```
$ python3 corpus/instruments/recheck-audit.py --root <base-export> --quiet
strict pass=1/65 cdroot_fail=64 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=65 missing=0 unexpected=0 exit=1
exit=1
$ python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
exit=0
$ python3 corpus/instruments/score-gap.py
gap: 22 of 65 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

Base and tip read the **same** `gated=22`. That is the discrimination for the held verdict: the
attempt-2 C1 surface (the counters' mutation coverage) is not the surface the 4 → 5 limb measures.
The base export's `exit=1` is an export artifact — its recheck lines `cd` into the live lane path, so
`cdroot_fail=64` on any export; the lane tree itself reads `strict pass=65/65 … exit=0`.

### F6 — non-target guard and no-harm diff (built: the depth:density row)

```
$ cmp <base-export>/corpus/instruments/density.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/density.py
$ echo $?
0
$ python3 corpus/instruments/density.py <base-export>/SKILL.md --label base | tail -3
| | **mean dens** | | | | | | | | | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.
$ python3 corpus/instruments/density.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md --label tip | tail -3
| | **mean dens** | | | | | | | | | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.

$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat 04af9bc9 HEAD
 20 files changed, 3309 insertions(+)
$ git -C … diff --numstat 04af9bc9 HEAD | awk '$2>0 {print}'
(no output; deletion-line-count=0)
```

`SKILL.md` is byte-identical base → tip at the freeze (`cmp` silent, exit 0); the wave's registry-block
append will move the mean at landing and is not credited as depth.

### F7 — the claim's own C1 plain counter cannot discriminate (finding for the L1; erratum-class)

The frozen claim's third C1 plain command is
`grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py`
("the case-count move behind the tallies"). Run at the base export and at the freeze tree it prints:

```
$ grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py
corpus/instruments/r46-counters-selftest-c1.py:0
corpus/instruments/r46-counters-selftest-c2.py:0
exit=1
```

**0 for both files**, because the cases are not `def case_` functions: c1 registers them in a
module-level `CASES = [` list (`corpus/instruments/r46-counters-selftest-c1.py:457`) and c2 builds them
as `Case(...)` constructions into `C: list[Case] = []`
(`corpus/instruments/r46-counters-selftest-c2.py:363`). The command therefore reads **0 → 0** across the
round and cannot discriminate the case-count move it is cited for. The counting command that does
discriminate is the selftest's own last line, `selftest cases=<n> failures=<f>` — which this seat
re-ran at the base export and got `cases=76 failures=0` (c1) and `cases=137 failures=0` (c2), matching
`controls/selftest-baselines.txt`. The claims file is read-only for every seat (amendments happen only
at L1 integration as logged errata), so this seat does not edit it: the draft cites the selftest's own
tally instead of the `grep` counter and records the defect as an erratum-class item.

### F8 — the attempt-1 counter goes red on the attempt-2 tree (finding for the L1; the draft records it, it does not score it)

```
$ python3 corpus/instruments/r46-c2-gate.py --root <base-export>
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
…
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
c2-gate fixed=7/7 exit=0

$ python3 corpus/instruments/r46-c2-gate.py --root <projection>
gate G1 pass=0 read=rows=29 admitted=29 dup=0
…
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
```

Cause, from the committed source: `corpus/instruments/r46-c2-gate.py:178`
(`if len(rows) != 28 or adm != 28 or dup:`) and `:347`
(`return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized), …`). The
attempt-1 counter pins the attempt-1 tree's counts; the attempt-2 claims freeze that counter unedited
(`.ufo/waves/round-46/attempt2/claims.json`, top-level `note`), and `.ufo/waves/round-46/attempt2/counter-errata.md`
classifies this round's instrument changes as errata with E3 **conditional** and separate. So the red is
an erratum-class item, not a defect in the attempt-2 work and not a score move. The draft carries it as
an explicit no-harm note under the counting commands and as a round-47 gate (a counter that pins the
previous round's counts must be re-based or its expected red recorded before the landing commit).

## Limitations

- **Draft only; nothing committed.** The only writes were
  `.ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/` (this draft + two receipts) and this
  Report file. No tracked file was edited, no commit, no push, no mutating git/jj call, no
  `MANIFEST.json` / `.ufo/state` / `LOG.md` / `SCORECARD.md` / `SHONEN.md` touch, no sibling lane, no
  `~/Projects/shokuknow` write.
- **The after-values are not yet measured.** At this seat's time the wave-1 build had not landed: lane
  tip `ee03806`; `corpus/README.md` has no `F29` row; `corpus/SOURCES.md` no `S074` row;
  `corpus/knowledge/github-repository-security-advisories.md` absent; `r46-counters-selftest-c1.py` still
  reads `cases=76`. Every tip-side number in the draft is an `<AT-LANDING: cmd>` slot (9 slots) with
  the producing command inline; the green readings quoted above are on a scratch projection of the
  wave-1 drafts, labelled as such.
- **C1's after-value was not re-run.** It needs the wave's extended selftests, which are drafts
  (`R46bExecSelftestC1.draft/r46-counters-selftest-c1.py`). What this seat re-derived is the **before**
  side: three c1 mutant lines identical to the frozen receipt, plus both selftest baselines reproduced
  at the base export.
- **The base battery re-run hit my own 2400 s cap** (`BATEXIT=124`) after 3 of 20 c1 mutants; 20 + 21
  mutants × a full selftest each do not fit in one seat's budget. Time limit of the re-run, not a
  counter verdict.
- **The `r46-mutbat.py` v1.1 `--counter f29` mode is the wave's E1 and is not committed**, so the f29
  battery mode was not exercised by this seat; the f29 gate itself was.
- **Live-target testing refused.** The S074 page was not re-fetched; every quote check is against the
  frozen capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256
  `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, matching `freeze.txt`) and its
  manifest; `source-recheck.py` printed `S074:sha256 OK` plus nine located quotes, exit 0.
- **Moving target.** The wave's drafts changed while this seat worked (the admission draft, the entry
  and rows drafts, the extended selftest draft all appeared during the seat). The draft's wording is
  written against the freeze `fe0f56b7`, `counter-errata.md`, and the drafts as read; the L1 re-reads
  them at integration.
- **Tooling:** none installed or upgraded. `git`, `tar`, `sed`, `grep`, `awk`, `bash`, `python3` were
  already present. No `pacman`, `uv tool`, `cargo` or `npm` transaction was run.
