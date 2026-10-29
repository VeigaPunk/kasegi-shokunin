# R46bScribeScorecard — round 46 (attempt 2) SCORECARD block (DRAFT, for L1 integration)

**Status: DRAFT.** Nothing here is committed. This is the proposed append-only text for
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md`, following the round-45 result-block shape
(`SCORECARD.md:1741-1774`). Every number in this draft is either (a) a value this seat re-ran and
quotes with its command, or (b) an explicit `<AT-LANDING: …>` slot the L1 fills from the landing
measurement — never an unrun check presented as passed.

**Slot convention.** `<AT-LANDING: cmd>` marks a value that only exists after the wave-1 integration
commit lands; the command inside the slot is the one that produces it. The L1 substitutes the printed
value and deletes the slot. Where this seat could already measure the value (the base export, the
freeze tree, and a scratch projection of the wave-1 drafts) the measured value is given in full.

---

## Round 46 (attempt 2) result

Frozen at `.ufo/waves/round-46/attempt2/claims.json` (freeze commit `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`,
base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; claims sha256 `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`
— verified by `sha256sum` against `.ufo/waves/round-46/attempt2/freeze.txt`). The attempt-1 counters
`corpus/instruments/r46-c1-gate.py` / `r46-c2-gate.py` and their selftests are **byte-identical at the
freeze** to the base (`git show 04af9bc9:<path> | sha256sum` vs `git show fe0f56b7:<path> | sha256sum`:
`r46-c1-gate.py` `95f2eb7933841d6c`, `r46-c2-gate.py` `647bd5b7b6268551`, `r46-counters-selftest-c1.py`
`8b17164aadbd9c69`, `r46-counters-selftest-c2.py` `ff7104cfc8910071` — all four unchanged); the round's
surface is their **selftests**, the battery `r46-mutbat.py` (v1 sha256 `f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8`),
the new gate `r46-f29-gate.py` (v1 sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`)
and one frontier admission. Errata file: `.ufo/waves/round-46/attempt2/counter-errata.md`
(E1 battery `v1 → v1.1`, E2 selftest extensions, E3 **conditional** `r46-c2-gate.py` `v1.2 → v1.3` ledger
exemption). Before-value receipt `controls/mutbat-before.txt` (sha256 `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`);
R50 pre-freeze receipt `controls/f29-r50-receipt.txt` (21 mutants, 11 defect-tree flips, 10 disclosed).

| Axis | Score before r46a2 | Score after r46a2 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4 held — measured (counter mutation coverage closed; no promotion limb moved)** | C1 `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure <pure> --work <scratch> --counter both --jobs 8`: base `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0` and `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0` (receipt `controls/mutbat-before.txt`, re-derived by this seat at the base export); after `<AT-LANDING: same command on the landing export>` → `mutbat counter=c1 … uncaught=0 baseline_failures=0` and `mutbat counter=c2 … uncaught=0 baseline_failures=0`, with the extended selftests green (`selftest cases=<n> failures=0` for both, `n` > 76 / > 137). **The 4 → 5 promotion limb did not move**: `## Distance-to-next-score` (`SCORECARD.md:1536`) limb 1 wants `gated=0` and this seat measured `executes=43 gated=22 broken=0` at the base export and at the live tip (`recheck-audit.py --root <tree> --quiet`), so 22 gated lines remain; limb 2 (the score-5 audit bar, `SCORECARD.md:331`) is untouched and only a non-author closure can grade it. | r46a2 (held) |
| coverage | 8 | **8 held — measured (+1 admitted frontier row F29; not a coverage-ratio move)** | C2 `python3 corpus/instruments/r46-f29-gate.py --root <tree>`: base `f29-gate fixed=1/7 exit=1` (re-derived by this seat at the `04af9bc9` export — matches `controls/f29-gate-at-base.txt`), freeze tree `f29-gate fixed=2/7 exit=1`, after `<AT-LANDING: same command on the landing export>` → `f29-gate fixed=7/7 exit=0`. Secondary `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 29`: base `frontier rows=28 admitted=28` / `frontier expected=29 admitted=28 verdict=SHORT exit=1`; after `<AT-LANDING: …>` → `frontier rows=29 admitted=29` exit 0. Plain: frontier rows 28 → 29, SOURCES rows 73 → 74 (S074 `mined`), knowledge entries 65 → 66, absence sweep 2 → 4 files. **No 8 → 9 criterion exists** (`## Distance-to-next-score`, `SCORECARD.md:1547`, carries only `### coverage, 7 → 8`), so the r22 ratio `(20 + F_admitted)/(20 + F_total)` stays **1.000** (29 admitted of 29, queued registry rows 0) — an expansion count, not a ratio move; none is invented here. | r46a2 (held) |
| depth:density | 9 | **9 held — non-target guard** | `corpus/instruments/density.py` is **byte-identical** base → tip (`cmp` on the base-export copy and the live copy prints nothing; exit 0). SKILL.md mean `<AT-LANDING: python3 corpus/instruments/density.py SKILL.md --label r46a2>` — the wave's appended Gates & probes registry block moves the mean, which is **not credited as depth** (same reading as round 45's row, `SCORECARD.md:1749`). | r46a2 (held) |

### Round-46 (attempt 2) move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 46a2 | depth:verifiability | 20 c1 battery mutants with **7 uncaught** (M06-L3-home-dropped, M07-L3-home-no-abs, M13-L6-control-dropped, M14-L6-exit-ignored, M18-anchor-dirs-wide, M19-L2-eq-relaxed, M20-syntax-ignored); 21 c2 battery mutants with **13 uncaught** (G1c-src-boundary, G2a-verified-prefix, G2b-wordfloor-low, G2c-need-empty, G3a-cells-loose, G4b-quotes-low, G5c-pass-low, G6a-guards-dead, G6b-integrity-loose, G6c-size-low, G7a-verdict-or, G7b-symlink-dead, G7c-okline-loose); selftest baselines `cases=76 failures=0` / `cases=137 failures=0` | `<AT-LANDING: mutbat counter=c1 … uncaught=0>` and `<AT-LANDING: mutbat counter=c2 … uncaught=0>`, `baseline_failures=0` both; extended selftests `cases=<n> failures=0` with `n` > 76 / > 137; every `equivalent` verdict must name a committed proof file (`--equivalent` map) that a reviewer can falsify by constructing an input class where the mutated clause changes a verdict | `corpus/instruments/r46-mutbat.py`; `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`; `.ufo/waves/round-46/attempt2/counter-errata.md` (E1, E2) |
| 46a2 | coverage | 28 admitted frontier rows (F01–F28), 73 SOURCES rows, 65 knowledge entries; the maintainer-side advisory lifecycle held nowhere (absence sweep `repository securit. advisor\|GHSA` → 2 files, both non-answering: the F28 entry's scope-out notes and the S068 rejected-row search-log context) | 29 admitted rows (F29 = GitHub repository security advisories, the maintainer-side lifecycle; the reporter flow stays F28), SOURCES 74 (S074 tier A `mined`, sha-pinned capture `corpus/source-snapshots/round-46-a2/S074.txt` sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, 42 lines, nine located manifest quotes), 66 knowledge entries, absence sweep 2 → 4 files | `corpus/README.md` Round-46 (attempt 2) admission block; `corpus/knowledge/github-repository-security-advisories.md`; `corpus/SOURCES.md` S074; `corpus/source-snapshots/round-46-a2/manifest.json`; `corpus/instruments/r46-f29-gate.py`; `controls/f29-r50-receipt.txt` |

Counting commands, one per claim (re-runnable on an export):

- **C1** — `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure <pure> --work <scratch> --counter both --jobs 8` → `mutbat counter=c1 mutants=20 caught=<k> equivalent=<e> uncaught=<u> baseline_failures=0` and `mutbat counter=c2 mutants=21 caught=<k> equivalent=<e> uncaught=<u> baseline_failures=0`; before (base export `04af9bc9`) `c1 caught=13 equivalent=0 uncaught=7`, `c2 caught=8 equivalent=0 uncaught=13`, `BATEXIT=1`; after `<AT-LANDING: …>` `uncaught=0` on both counters, `baseline_failures=0` on both. Plain second measures: `python3 corpus/instruments/r46-counters-selftest-c1.py --pure <pure> --work <scratch> --jobs 8 | tail -1` → `selftest cases=<n> failures=0` (base `cases=76 failures=0`); `python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1` → `selftest cases=<n> failures=0` (base `cases=137 failures=0`).
- **C2** — `python3 corpus/instruments/r46-f29-gate.py --root <tree>` → `f29-gate fixed=<k>/7 exit=<c>`; before (base export) `fixed=1/7 exit=1`, freeze tree `fixed=2/7 exit=1`, after `<AT-LANDING: …>` `fixed=7/7 exit=0`; secondary `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 29` → base `frontier rows=28 admitted=28` exit 1, after `<AT-LANDING: …>` `frontier rows=29 admitted=29` exit 0. Plain: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` 28 → 29; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` 73 → 74; `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` 65 → 66; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` → `S074:sha256 OK` + nine `S074:Qn OK occurrences=1 anchor=N-ok` lines, exit 0 (already true at the freeze tree, re-run by this seat); `grep -rliE 'repository securit. advisor\|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l` 2 → 4.

**Plain-counter defect the L1 must record, not hide.** The claim's third C1 plain command —
`grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py`
("the case-count move behind the tallies") — prints **0** for both files at the base export *and* at the
freeze tree, because the cases are not `def case_` functions: c1 registers them in a module-level
`CASES = [` list (`corpus/instruments/r46-counters-selftest-c1.py:457`) and c2 builds them as
`Case(...)` constructions into `C: list[Case] = []` (`corpus/instruments/r46-counters-selftest-c2.py:363`).
The command therefore reads 0 → 0 across the round and **cannot discriminate** the case-count move it is
cited for; the counting command that does is the selftest's own last line (`selftest cases=<n>
failures=<f>`). The claims file is read-only for every seat and amendments happen only at L1 integration
as logged errata, so this is an erratum-class item for the L1, not an edit this seat may make. This
draft cites the selftest's own tally in the C1 row instead of the `grep` counter.

**No-harm note the L1 must record, not hide.** The attempt-1 counter `r46-c2-gate.py` (v1.2, **not** edited by this round
per the claims note) hard-codes the attempt-1 tree's counts — `len(rows) != 28 or adm != 28`
(`corpus/instruments/r46-c2-gate.py:178`) and `len(names) == 65 and len(everything) == 65 and nested == 65`
(`:347`). On a scratch projection of the wave-1 drafts (freeze export + the S074 row + the F29 README
block + the entry file) this seat measured `gate G1 pass=0 read=rows=29 admitted=29 dup=0` and
`gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1`, i.e.
`c2-gate fixed=5/7 exit=1` at the attempt-2 tree, against `c2-gate fixed=7/7 exit=0` at the attempt-1
tip. That red is the attempt-1 counter pinning the attempt-1 tree, not a defect in the attempt-2 work;
it is an erratum-class item (`counter-errata.md` E3 is the adjacent, separate ledger-exemption
amendment and is **conditional**). The attempt-2 C2 counter is `r46-f29-gate.py`, which reads
`fixed=7/7 exit=0` on the same projection. The L1 decides the disposition; this row states the
measurement, not a verdict.

### Round-46 (attempt 2) capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| `<L1: capability row — the L1's decision, not this section's claim>` | The attempt-2 surface is instruments (battery `v1 → v1.1` with the `F29_MUTANTS` table and `--counter f29`; the extended `r46-counters-selftest-c1.py` / `-c2.py`; the new `r46-selftest-f29.py`), and per the lane's own reading of `AXES.md` §Capabilities a counter or a selftest extension is **not** a new thing the lane can do to the domain — the same reading as rounds 35, 36, 38, 41, 42 and round 46 attempt 1 (`SCORECARD.md:1805`). If the L1 reads the mutation-battery discipline as a capability, the row enters here and the stagnation window restarts. | — | 46a2 (L1's call) |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. The lowest non-retired axis stays
**depth:verifiability (4)**, which C1 worked. The attempt-2 work moved no axis's number: the
`## Distance-to-next-score` promotion limb for depth:verifiability (`SCORECARD.md:1536`) is unmoved
(`gated=22` of 65 lines still fail closed — 22 to go — and the score-5 audit bar is untouched), and the
coverage axis has **no written 8 → 9 criterion** to move against (`SCORECARD.md:1547`). The operator
half of coverage (0/18 domain surfaces present) is unchanged. No axis retired; none split.

### Planned evidence gates for round 47

*(This block supersedes the round-46 attempt-1 round-47 gates at `SCORECARD.md:1807-1810`; that text
is kept as history. Where the two differ, this one is the operative plan.)*

- `depth:verifiability`: state each claim's before-value per start tree and run `capture-binding-check.py --root` and the census **BEFORE** dispatching a wave (round 46 attempt 2 read `records=61 bound=60 unbound=1` with `FAIL rule=no-row record=S074 dir=round-46-a2` at the freeze tree — the capture landed one commit ahead of its registry row); a new counter is **freeze-ready only after** its own mutation battery runs against it and reaches `uncaught=0` with each `equivalent` verdict naming a committed proof file that a reviewer can falsify by constructing an input class (QUALITY R50, carried from the attempt-1 round-47 gate and now discharged by `controls/mutbat-before.txt`); a battery mutant that the gate level cannot isolate must be **disclosed in the claim** and graded by the selftest instead — the R50 receipt's ten NOT-SHOWN mutants (disclosures (a)–(f)) are the precedent; a re-ground names who read its rows side by side.
- `coverage`: obtain a non-author admit/reject spot-check of **S074** (not S073 — S074 is the row this round admitted) before any coverage statement beyond +1 row; append the considerthese ledger row with the pin amendment (the ledger is byte-pinned by C2 G6); keep rejected-row captures outside `corpus/source-snapshots/`; a counter that pins the previous round's row or entry counts must be re-based or its expected red recorded as an erratum before the landing commit, so the next round's no-harm reading is not a surprise (the attempt-1 `r46-c2-gate.py` reads `fixed=5/7 exit=1` on the attempt-2 tree for exactly this reason).

---

## Evidence this seat produced (commands and printed output)

All commands were run by this seat from absolute paths; the base export was built with
`git -C <lane> archive 04af9bc9 | tar -x -C <scratch>` and the freeze export with
`git -C <lane> archive fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 | tar -x -C <scratch>`.
Scratch root `$HYAKU_SCRATCH/kasegi-r46/R46bScribeScorecard/` (`HYAKU_SCRATCH` unset → `/fast/scratch/hyaku`),
`TMPDIR` set explicitly; removed on exit.

### E1 — the frozen before-value reproduces at the base export (C1's control)

```
$ python3 corpus/instruments/r46-mutbat.py --root <base-export> --pure <pure2-copy> --work <scratch> --counter both --jobs 8
mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=8 verdict=caught
mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught
BATEXIT=124
```

`diff <(head -3 controls/mutbat-before.txt) <(head -3 my-run)` → **IDENTICAL (3/3 lines)**. `BATEXIT=124`
is my own 2400-second wall-clock cap on the run, not a counter verdict; the frozen receipt's own
summary lines (`mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0`,
`mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0`, `BATEXIT=1`) are
the committed before-value, and this seat re-derived the first three mutant lines plus both selftest
baselines at the base export.

### E2 — both selftest baselines re-run at the base export

```
$ python3 corpus/instruments/r46-counters-selftest-c1.py --pure <pure2-copy> --work <scratch> --jobs 8
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
exit=0

$ python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure2-copy>
selftest cases=137 failures=0
exit=0
```

Matches `controls/selftest-baselines.txt` (`cases=76 failures=0`, `cases=137 failures=0`).

### E3 — the C2 gate reads red at the base and at the freeze tree, green on a projection of the wave-1 drafts

```
$ python3 corpus/instruments/r46-f29-gate.py --root <base-export>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=entry-absent advisor-named=
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=0 read=manifest-absent
gate H5 pass=0 read=entry-absent advisor-named=
gate H6 pass=0 read=entry-absent advisor-named=
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=1/7 exit=1

$ python3 corpus/instruments/r46-f29-gate.py --root <freeze-export>
gate H1 pass=0 read=rows=28 admitted=28 dup=0
…
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
…
f29-gate fixed=2/7 exit=1

$ python3 corpus/instruments/r46-f29-gate.py --root <projection: freeze export + wave-1 drafts>
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=10 xrefs=6/6 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=28 located=28 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

Do-nothing controls on the same fixture builder, same gate, same command:

```
$ python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk --dir <scratch> --lane <lane>
$ python3 corpus/instruments/r46-f29-gate.py --root <junk-tree>
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1

$ python3 .ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode fabricated --dir <scratch> --lane <lane>
$ python3 corpus/instruments/r46-f29-gate.py --root <fabricated-tree>
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```

So the gate discriminates: base 1/7 red, freeze 2/7 red, junk 6/7 red, fabricated 6/7 red, projected
landing 7/7 green. **The projection is a scratch tree assembled from the wave-1 drafts (entry draft A,
the S074 row from rows draft A, admission block (a) from the admission draft, and the
`knowledge-expected.txt` insert), not the landed tree** — the L1's landing measurement replaces it.

### E4 — coverage counters and plain counts, base vs projection

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
… (Q2..Q8)
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
absence sweep files 2 → 4 (`corpus/knowledge/github-private-vulnerability-reporting.md`,
`corpus/SOURCES.md` at base — the F28 scope-out note and the S068 rejected-row search-log context, both
non-answering; the projection adds the README frontier block and the entry).

### E5 — the promotion limb that did not move (depth:verifiability)

```
$ python3 corpus/instruments/recheck-audit.py --root <base-export> --quiet
strict pass=1/65 cdroot_fail=64 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=65 missing=0 unexpected=0 exit=1
exit=1
$ python3 corpus/instruments/recheck-audit.py --root <lane> --quiet
strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=43 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=65 missing=0 unexpected=0 exit=0
exit=0
$ python3 corpus/instruments/score-gap.py
gap: 22 of 65 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

The base export and the live tip read the **same** `gated=22` — attempt 2's C1 works the counters'
mutation coverage, not the gated recheck lines, so the 4 → 5 limb 1 (`gated=0`) has 22 to go and limb 2
(the non-author audit bar) is untouched. Coverage has no 8 → 9 criterion to move against
(`SCORECARD.md:1547`), and the r22 ratio stays 1.000 (29 admitted of 29, queued registry rows 0).
Hence all three axes **held**.

(The base export's `exit=1` is an artifact of the export, not of the lane: the exported tree's recheck
lines `cd` into the live lane path, so `cdroot_fail=64` on an export — the same reading the base export
gives for every other round's census. The lane tree itself reads `strict pass=65/65 … exit=0`. The
figure that carries the promotion-limb distance is `gated=22`, identical in both, and it is that
figure, not the export's cwd exit, that the 4 → 5 limb measures.)

### E6 — non-target guard (depth:density) and no-harm diff

```
$ cmp <base-export>/corpus/instruments/density.py <lane>/corpus/instruments/density.py
$ echo $?
0
$ python3 corpus/instruments/density.py <base-export>/SKILL.md --label base | tail -3
| | **mean dens** | | | | | | | | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.
$ python3 corpus/instruments/density.py <lane>/SKILL.md --label tip | tail -3
| | **mean dens** | | | | | | | | | | | | | | | | **258.7** |
Total path-citation instances: 839 across 33 blocks.

$ git -C <lane> diff --stat 04af9bc9 HEAD
 20 files changed, 3309 insertions(+)
$ git -C <lane> diff --numstat 04af9bc9 HEAD | awk '$2>0 {print}'
(no lines — zero deletions anywhere)
```

The freeze commit adds files only; it deletes nothing. `SKILL.md` is byte-identical base → tip at the
freeze (`cmp` silent, exit 0); the wave's registry-block append will move the mean at landing and is
not credited as depth.

### E7 — the attempt-1 counter goes red on the attempt-2 tree (no-harm item for the L1)

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
(`return (len(names) == 65 and len(everything) == 65 and nested == 65 and base_ok and sized), …`).
The attempt-1 counter pins the attempt-1 tree's counts; attempt 2's claims freeze that counter
unedited. Recorded as an erratum-class item, not as a defect in the attempt-2 work and not as a score
move.

---

## Limitations of this draft

- **Draft only.** Nothing was committed, pushed, or mutated in git/jj; no tracked file was edited; the
  only writes were this seat's draft directory and this seat's Report file. The scratch root was
  removed on exit.
- **The after-values are not yet measured.** The wave-1 build had not landed at this seat's time
  (`git log` tip `ee03806`; `corpus/README.md` has no `F29` row, `corpus/SOURCES.md` no `S074` row,
  `corpus/knowledge/github-repository-security-advisories.md` absent). Every tip-side number is an
  `<AT-LANDING: …>` slot; the values shown green in E3/E4 are on a **scratch projection** of the
  wave-1 drafts, not on the landed tree.
- **C1's after-value was not re-run.** The battery needs the wave's extended selftests, which are
  drafts at this seat's time (`corpus/instruments/r46-counters-selftest-c1.py` still reads `cases=76`).
  This seat re-derived the **before** value at the base export (first three c1 mutant lines identical
  to the frozen receipt; both selftest baselines reproduced) — the after-side claim is the L1's
  landing measurement.
- **The base battery run hit my own 2400 s wall clock** (`BATEXIT=124`) after three of twenty c1
  mutants; each mutant re-runs the whole selftest suite. This is a time limit of this seat's re-run,
  not a counter verdict, and it is why the frozen receipt — not my run — is cited for the full
  before-value.
- **Not re-derived:** the claim's own `frozen_tree_reading` for C2 (`fixed=2/7 exit=1` at the freeze
  tree) — I did re-run it and got `fixed=2/7 exit=1`, so it agrees; and the `r46-mutbat.py` v1.1
  `--counter f29` mode, which is the wave's E1 and not yet committed.
- **Live-target testing refused.** The S074 page was not re-fetched; every quote check is against the
  frozen capture `corpus/source-snapshots/round-46-a2/S074.txt` (sha256
  `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, matching `freeze.txt`) and its
  manifest.
- **Tooling:** none installed or upgraded — `git`, `tar`, `sed`, `grep`, `awk`, `bash` and `python3`
  were already present. No `pacman` transaction was run.
