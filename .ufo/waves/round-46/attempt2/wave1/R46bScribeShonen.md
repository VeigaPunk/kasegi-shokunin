VERDICT: DRAFT-READY

# R46bScribeShonen — SHONEN.md round-46 (attempt 2) evidence bullets (DRAFT)

Seat: scribe (builder seat). Scope: draft only. Draft deliverable:
`.ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.draft/shonen.md` (the proposed append-only
`## Round 46 (attempt 2) evidence` block for `SHONEN.md`, four `- [~]` bullets, one per box, in the
shape of the round-46 attempt-1 block at `SHONEN.md:304-316`).

Nothing tracked was edited by this seat. No git or jj mutation was performed anywhere. Scratch
`/fast/scratch/hyaku/kasegi-r46/R46bScribeShonen/` was removed on exit; the receipt values quoted
below are in this Report and in the draft file, not in `/tmp`.

## Behaviour

Drafted the four SHONEN.md evidence bullets for round 46 attempt 2 and ran every command the bullets
cite, pasting each command's printed output into the draft. All four boxes stay `[~]`; `[x]` is
operator-owned.

## Gates (command → printed output)

All runs used absolute paths under the lane; the base and tip trees are `git archive` exports of
committed revisions (`git -C <lane> archive <rev> | tar -x -C <scratch>`); `TMPDIR` was set explicitly
to the scratch root. The **projection** tree is the tip export plus this wave's real drafts (entry
draft A, the S074 row draft, admission block (a), the `knowledge-expected.txt` insert) — a scratch
tree, not the landed tree.

### Box 1 — SKILL.md decision tables / cited sources

```
$ git -C <lane> rev-parse 04af9bc92229232ea5cce8b32bfe59dd969eb26d:SKILL.md ee03806b6b54a2822045e96641a77fa76984b410:SKILL.md
b659e3ec6911d362355c042943211c4a24c9fa7d
b659e3ec6911d362355c042943211c4a24c9fa7d

$ python3 corpus/instruments/density.py SKILL.md --label r46b-scribe-tip     # tip export
| **mean dens** | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.
exit=0

$ python3 corpus/instruments/density.py SKILL.md --label r46b-scribe-base     # base export
| **mean dens** | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.
exit=0

$ python3 corpus/instruments/anchorcheck.py SKILL.md
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
$ diff <base-export anchorcheck output> <tip-export anchorcheck output>
IDENTICAL
```

### Box 2 — end-to-end domain task

None new: no target testing, probing or submission was performed (documentation-only round). The
closest executed work is the captured-page gate and the source recheck:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074   # projection
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
…
S074:Q9 OK occurrences=1 anchor=38-ok
exit=0
```

### Box 3 — instructions executable without oral context

```
$ python3 corpus/instruments/r46-f29-gate.py --root <base export>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1
# byte-identical to the frozen receipt controls/f29-gate-at-base.txt

$ python3 corpus/instruments/r46-f29-gate.py --root <tip export>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
…
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
…
gate H7 pass=1 read=census-rc=0 ok-line=1
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

Do-nothing controls re-run by this seat on the round's committed fixtures (same gate, same command):

```
$ python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk --dir <scratch>/fix-junk --lane <lane>
$ python3 corpus/instruments/r46-f29-gate.py --root <scratch>/fix-junk
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1

$ python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode fabricated --dir <scratch>/fix-fabricated --lane <lane>
$ python3 corpus/instruments/r46-f29-gate.py --root <scratch>/fix-fabricated
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=6/7 exit=1
```

So the gate discriminates: base export 1/7 red, tip export 2/7 red, junk tree 6/7 red, fabricated tree
6/7 red, projection 7/7 green. The frozen R50 receipt
`controls/f29-r50-receipt.txt` records the same control shape ("Positive tree reads `f29-gate
fixed=7/7 exit=0`; junk tree `fixed=3/7` … fabricated tree `fixed=3/7`" — under the R50 receipt's own
21-mutant defect-tree harness, a different fixture from the two-limb count the plain fixture modes
produce here).

Secondary and standing counters:

```
$ python3 corpus/instruments/r44-frontier-count.py --root <tip export> --expect 29
frontier rows=28 admitted=28
frontier expected=29 admitted=28 verdict=SHORT exit=1

$ python3 corpus/instruments/r44-frontier-count.py --root <projection> --expect 29
frontier rows=29 admitted=29
exit=0

$ python3 corpus/instruments/recheck-audit.py --root <lane> --quiet            # LIVE lane
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
exit=0

$ python3 corpus/instruments/recheck-audit.py --root <export> --quiet           # export, no --cdroot
strict pass=1/65 cdroot_fail=64 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=65 missing=0 unexpected=0 exit=1
exit=1

$ python3 corpus/instruments/recheck-audit.py --root <export> --cdroot <lane> --quiet
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
exit=0
```

The export's `cdroot_fail=64` is an **export artifact** (the exported `recheck:` lines `cd` into the
live lane path); the lane tree reads `strict pass=65/65 … exit=0`. The figure that carries the
promotion-limb distance is `gated=22`, identical at base and tip.

```
$ python3 corpus/instruments/frontier-recheck-count.py --root <tip export>
FRONTIER-CENSUS rows=28 admitted=28 closed=28 problem-rows=0 registry=73
entries=31 pass=31 exit=0

$ python3 corpus/instruments/frontier-recheck-count.py --root <projection>
FRONTIER-CENSUS rows=29 admitted=29 closed=29 problem-rows=0 registry=74
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S074           exit=0
entries=32 pass=32 exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <base export>
records=60 bound=60 unbound=0
exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <tip export>
FAIL rule=no-row record=S074 dir=round-46-a2
records=61 bound=60 unbound=1
exit=1

$ python3 corpus/instruments/capture-binding-check.py --root <projection>
records=61 bound=61 unbound=0
exit=0

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <tree>/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	<tree>/corpus/SOURCES.md
exit=0
# the same three W04 warnings and exit 0 at the base export, the tip export and the projection

$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <tree>/corpus/SOURCES.md
file	rows	73      # base export and tip export
file	rows	74      # projection
exit=0

$ bash corpus/instruments/r46-plain-measure.sh <tree>
c1a=21 c1b=22 c2a=28 c2b=73 c2c=65 c2d=3     # base export and tip export
c1a=21 c1b=22 c2a=29 c2b=74 c2c=66 c2d=3     # projection
```

C1 battery (the depth:verifiability counter):

```
$ python3 corpus/instruments/r46-mutbat.py --root <tip export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch> --counter both --jobs 8
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
BATEXIT=143
```

This seat's run printed that first line — byte-identical to line 1 of the frozen receipt
`controls/mutbat-before.txt` — and was then stopped by this seat (exit 143 = SIGTERM) once the c1/c2
selftest baselines had been re-run; a first attempt over the base export hit the tool's 1200-second
cap after printing `error: interrupted`. The host was under a load average above 200 with many sibling
seats running the same battery concurrently. The tip export's counters and selftests are byte-identical
to the base export's (`git diff --name-status 04af9bc9 ee03806 -- corpus/` adds only `r46-f29-gate.py`,
`r46-mutbat.py` and the round-46-a2 capture/manifest), so the M01 reading is the base export's M01
reading. The frozen receipt's summary lines are what the draft quotes, not a completed run of this
seat's:

```
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
BATEXIT=1
```

Selftest baselines re-run by this seat at the tip export (the extended selftests are not landed yet,
so these are the unchanged baselines):

```
$ python3 corpus/instruments/r46-counters-selftest-c1.py --pure <pure> --work <scratch> --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
exit=0
# 76 `case ` lines; identical to controls/selftest-baselines.txt (`selftest cases=76 failures=0`, `c1-exit=0`)

$ python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure>
selftest cases=137 failures=0
exit=0
# 137 `case `/`ok `/`probe ` lines; identical to controls/selftest-baselines.txt (`selftest cases=137 failures=0`, `c2-exit=0`)
```

### Box 4 — no cross-domain bleed (PROVINCE.md still accurate)

```
$ git -C <lane> rev-parse 04af9bc92229232ea5cce8b32bfe59dd969eb26d:PROVINCE.md ee03806b6b54a2822045e96641a77fa76984b410:PROVINCE.md
e22cdf9b5b80ae717acec15ebc48579e9c609ed0
e22cdf9b5b80ae717acec15ebc48579e9c609ed0

$ grep -c 'F29' PROVINCE.md
0
$ grep -c 'F28' PROVINCE.md
1
$ grep -c 'F29' corpus/README.md
0
$ grep -c 'S074' corpus/SOURCES.md
0
$ ls corpus/knowledge/github-repository-security-advisories.md
ls: cannot access '.../corpus/knowledge/github-repository-security-advisories.md': No such file or directory

$ grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l
2      # base export and tip export
4      # projection (entry, SOURCES, README, F28 entry)
```

The F29 province amendment is **owed and not applied** at this read; the wave drafts it as an
end-of-file append with a scope limit (`R46bScribeAdmission.draft/appends.md` block (b)). The sibling
sweep `.ufo/waves/round-46/attempt2/wave1/R46bScoutAdjacent.md` (VERDICT: DRAFT-READY) rules F29
uncontested across 20 sibling corpora plus `shokuknow`, naming the only sibling GHSA holdings (mori
S012 — a published advisory used for patch-state facts, self-ruled "adjacency only"; kaidoku's OSV
JSON; tabi's GitHub Docs nav chrome) and sixteen clean zeros, and naming the F28 sentences the new
entry must contrast rather than absorb (`corpus/knowledge/github-private-vulnerability-reporting.md:9`,
`:13`, `:40`, `:43`).

## Touched surfaces

- Written: `.ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.draft/shonen.md` (the draft) and this
  Report `.ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.md`. Nothing else.
- Read-only: the lane repo (`git log` / `git diff` / `git rev-parse` / `git archive` / `git ls-tree`
  only), the fleet `scripts/sources-census.sh`, and the sibling wave-1 reports.
- Scratch: `/fast/scratch/hyaku/kasegi-r46/R46bScribeShonen/` (base, tip and projection exports,
  work dirs, receipts) — **removed on exit**. `/fast/scratch/hyaku/kasegi-r46/L1/pure2` was read only
  (`find … -newermt '2026-10-29 18:30' -type f` printed nothing; no file under it was written).

## Out of scope

- No edit to `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `corpus/**`, `SCORECARD.md`, `LOG.md` or the lesson
  file: this seat drafts the SHONEN text; the L1 integrates and commits.
- No commit, push, or mutating git/jj command anywhere; no `MANIFEST.json`, `.ufo/state` or
  `~/Projects/shokuknow` write.
- No live-target testing (refused for this corpus).

## Findings

1. **The round tip does not exist yet.** The lane HEAD at this seat's read is `ee03806` (the wave-1
   *spec* commit): `git diff --name-status 04af9bc9 ee03806 -- corpus/` prints `A
   corpus/instruments/r46-f29-gate.py`, `A corpus/instruments/r46-mutbat.py`, `A
   corpus/source-snapshots/round-46-a2/S074.txt`, `A corpus/source-snapshots/round-46-a2/manifest.json`
   — no corpus content change. Every value that exists only after the wave-1 integration is an
   `<AT-LANDING: cmd>` slot in the draft, using the sibling scorecard seat's convention.
2. **The projection reads green where the tip reads red, and the draft says so.** `r46-f29-gate.py` reads
   `fixed=1/7` at base, `fixed=2/7` at the tip export, `fixed=7/7` on the projection. The draft marks the
   `7/7` as a projection reading and leaves the landing value as a slot.
3. **`capture-binding-check.py` is red at the tip export** (`FAIL rule=no-row record=S074 dir=round-46-a2`,
   `records=61 bound=60 unbound=1`, exit 1) because the freeze commit added the S074 capture and its
   manifest without the S074 registry row. The projection reads `records=61 bound=61 unbound=0` (exit 0).
   The draft quotes both; the L1 should expect this counter to be red until the S074 row lands.
4. **The `recheck-audit.py --root <export>` red is an export artifact, not a lane defect.** Every
   knowledge entry's `recheck:` line begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`
   (64 lines), so an export's `--root` is not the cd target and the strict `cdroot` limb fails 64/65.
   Passing `--cdroot <lane>` makes the same export read `strict pass=65/65 … exit=0`. The draft cites the
   lane reading (`exit=0`) and states the export reading and its cause.
5. **The wave's registry block for the three new instruments will move the SKILL.md density mean.** The
   draft records the measured 258.7 at base and tip and leaves the landing mean as a slot, with the
   round-45 precedent noted (an appended block is not credited as depth).
6. **The battery run was stopped, not completed** (see Limitations). The c1/c2 summary lines in the draft
   are the frozen receipt's, explicitly attributed.
7. **Both selftest baselines were reproduced** at the tip export: `selftest cases=76 failures=0` (exit 0,
   76 case lines) and `selftest cases=137 failures=0` (exit 0, 137 case/ok/probe lines), identical to
   `controls/selftest-baselines.txt` (`c1-exit=0`, `c2-exit=0`). The extended selftests' own tallies
   (`n` > 76 / `n` > 137) exist only after the wave's selftest extension lands and are `<AT-LANDING: …>`
   slots in the draft.

## Limitations

- The c2 selftest re-run (`r46-counters-selftest-c2.py --pure <pure>`) completed: `selftest cases=137
  failures=0`, exit 0, identical to the frozen receipt `controls/selftest-baselines.txt` (`c2-exit=0`).
  It took roughly 40 minutes of wall clock under the host load; the c1 selftest completed at
  `selftest cases=76 failures=0`, exit 0.
- The battery (`r46-mutbat.py --counter both --jobs 8`) was stopped by this seat (exit 143 = SIGTERM)
  after printing its first mutant line, identical to the frozen receipt's line 1; a first attempt over
  the base export hit the tool's 1200-second cap after printing `error: interrupted`. The host was under
  a load average above 200 with many sibling seats running the same battery concurrently. No summary
  line of this seat's is claimed.
- The projection tree applies one entry draft of six competing drafts; the L1's landing measurement, and
  the landing of a different entry draft, replace every projection reading in the draft.
- No non-author verifier has judged any box; the wave-2 critics are internal, not non-author verifiers.
- No tool was installed or upgraded; `pacman` was not invoked (the operator's tooling directive at
  `/home/vgpnk/.omp/agent/RULES.md` was read; the host-wide pacman guard made an install unnecessary —
  every command used here is stock `python3` / `bash` / `grep` / `git` / `ls` / `wc` / `diff` / `cmp`).

## Artifact paths

- Draft: `.ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.draft/shonen.md`
- This Report: `.ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.md`
