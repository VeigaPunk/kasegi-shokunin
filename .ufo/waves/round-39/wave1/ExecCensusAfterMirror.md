# ExecCensusAfterMirror — after-state mirror metrics (round 39, wave 1)

Seat: ExecCensusAfterMirror (leaf). Item: compose a scratch mirror of the intended round-39
after-state and run the after-metrics on it. Judged axis: depth:verifiability. Date: 2026-10-26.

## Axes named

- depth:verifiability (the seat's judged axis): the after-metrics are pre-measured on a composed
  after-state mirror, so the claim's counting commands are known-green before landing.
- coverage: F22 / S057 / harness / binding / knowledge counters measured on the composition.

## What was run (all writes under `/fast/scratch/hyaku/kasegi-r39/ExecCensusAfterMirror`, `TMPDIR=$S`)

Mirror construction (scripts `build-mirror.sh`, `build-variant.sh` in scratch):

    git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 480b1a505a2dfc14a4f718d16d63808247214d0a | tar -x -C mirror-base
    git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 7beae6098f58cba99b0a9d1ac387edc664c0abe4 | tar -x -C mirror-after

`mirror-after` (lane HEAD at measure time = base + claims freeze + wave-1 spec/dispatch + claims
erratum 1) with the wave-1 deliverables applied: `corpus/source-snapshots/round-39/{S057.txt,
manifest.json}`; S056/S057/S058/S059 registry rows after the S055 row; the search-log bullet before
`## Leads (unopened)`; the registry-changes bullets at EOF; the `corpus/README.md` EOF append;
`corpus/knowledge/cisa-when-to-issue-vex.md`; the sorted insert into
`corpus/instruments/knowledge-expected.txt`; the `PROVINCE.md` EOF append.

`mirror-after-cd` is a measurement variant: every knowledge entry's `recheck:` line has its
`cd <lane>` prefix retargeted onto the mirror root (recheck lines only). Reason: `recheck-audit.py`
limbs (b)/(d) and `frontier-recheck-count.py` execute the line with `cwd=<root>`; the line's own
`cd` overrides it, so the landed-byte form binds execution to the real lane. The variant is a
shape check; the authoritative lane-root run happens after the L1 lands the same bytes.

## After-metric results

| metric | command | target | baseline (mirror-base / BASE) | measured after |
|---|---|---|---|---|
| census | `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` | exit 0, only W04 S028/S029 | exit 0, W04 S028/S029 | exit 0, W04 S028/S029 (both mirror forms) |
| frontier | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 22 | 21 | 22 |
| registry | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 59 (erratum E1) | 55 | 59 |
| knowledge | `ls corpus/knowledge/*.md \| wc -l` | 51 | 50 | 51 |
| S057 citation | `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | 1 | 0 | 1 |
| harness | `python3 corpus/instruments/frontier-recheck-count.py --root <mirror>` | entries=25 pass=25 exit=0 | 24/24 exit=0 | 25/25 exit=0 on mirror-after-cd (`PASS F22 ... ids=S057 exit=0`); 24/25 exit=1 on mirror-after (`FAIL F22 ... exit=2 problems=recheck-exit-2`, lane-root binding only) |
| audit | `python3 corpus/instruments/recheck-audit.py --root <mirror> --quiet` | expected=51 missing=0 unexpected=0 exit=0 | exit=1 on mirror (cdroot), exit=0 at lane root expected=50 | exit=0, `lines=51 total=51 pass=51`, `strict pass=51/51 cdroot_fail=0`, `expected=51 missing=0 unexpected=0` on mirror-after-cd; exit=1 on mirror-after (cdroot_fail=50, lane-root binding only) |
| binding | `python3 corpus/instruments/capture-binding-check.py --root <mirror>` | records=46 bound=46 unbound=0 | 45/45/0 | 46/46/0 (both forms) |

Additional shape evidence on the mirror: `source-recheck.py --manifest
corpus/source-snapshots/round-39/manifest.json --source S057` -> `S057:sha256 OK` and
`Q1..Q4 OK occurrences=1 anchor=N-ok`, exit 0; all 22 block-quotes in the entry occur verbatim
in the pinned capture under Unicode/whitespace normalization (0 missing); the four appended rows
pipe-split to NF=13 with `status` mined (S057) / rejected (S056, S058, S059), `opened 2026-10-26`,
`used-by —` for the three rejected rows; the F22 frontier row is `admitted` on
`knowledge/cisa-when-to-issue-vex.md` with `sources S057`.

Raw commands and output: `ExecCensusAfterMirror.mirror-metrics.txt` (280 lines,
sha256 `d90a6abba1769fd24eb769d5dc21cdf9f13d4b968518a3187cb2e7e0d0049a48`).

## Findings

1. **Registry after-count is 59, not the as-frozen 58** (F1, corroborates `claims-erratum-1.md`
   E1). Base is 55 rows (S001–S055); the claim appends four rows — S057 + S056/S058/S059 — so
   55+4 = 59. Measured 59 on the composed after-mirror. Erratum E1 already fixes the measurement
   value; no claim edit is needed beyond citing it.
2. **Lane-root-bound instruments cannot go green on a mirror that keeps the landed `cd <lane>`
   prefixes.** `recheck-audit.py`'s cdroot limb and the harness's line execution both bind to the
   real lane; on `mirror-after` they report `cdroot_fail=50` / `FAIL F22 exit=2`. The
   retargeted variant clears them (`strict pass=51/51`, `entries=25 pass=25`), which is the shape
   prediction; the authoritative after-run must be at the lane root once the bytes are landed.
3. **Suite deliverable absent at measure time.** `wave1/ExecSuiteBuild.r39-closure.sh` did not
   exist in the wave1 listings at 2026-10-26T19:38Z and 2026-10-26T19:42Z, so the mirror was built without
   `corpus/instruments/r39-closure.sh`. No after-metric in this seat's item reads that file; the
   mirror carries no digest for a file it does not hold.
4. **Mirror base is lane HEAD (7beae60), not BASE.** HEAD already carries the claims freeze,
   controls, wave-1 spec and erratum 1; using it keeps the mirror a faithful after-state
   approximation. The before-control uses the BASE archive and reproduces `c2-controls/before.txt`
   exactly (frontier 21, registry 55, knowledge 50, harness 24/24, binding 45/45, census W04 only).
5. **Positional assumptions.** The search-log bullet is composed before `## Leads (unopened)`
   (ScribeSearchLog.md's landing line); the registry-changes bullets at SOURCES.md EOF. Census
   validate is insensitive to both positions (exit 0, W04 only).

## Risks / blockers

- The harness/audit after-values are proven on the retargeted variant, not on the landed-byte
  form; a landing that changes an entry's `cd` prefix or the manifest path would move them.
  Re-run `recheck-audit.py --quiet` and `frontier-recheck-count.py` at the lane root after landing.
- The mirror contains only the artifacts present in wave1 at build time; later scribe appends
  (SCORECARD/SHONEN/LOG/lesson/considerthese ledger) are outside this seat's metric set and are
  not represented.
- Frozen claim text 58 vs erratum 59: closure must cite erratum E1, otherwise the C2 counting
  command reads red on a correct lane.

## Scope discipline

Wrote only (1) this receipt, (2) `ExecCensusAfterMirror.mirror-metrics.txt` beside it, (3) scratch
under `/fast/scratch/hyaku/kasegi-r39/ExecCensusAfterMirror/` (removed before yield). No lane,
fleet, sibling-repo or source-tree file was modified; no git/jj mutation was run; no network fetch
was made; no tool was installed (tooling record: none needed, none installed).

Report: `.ufo/waves/round-39/wave1/ExecCensusAfterMirror.md`
