# R46bScribeShonen — SHONEN.md round-46 (attempt 2) evidence block (DRAFT, for L1 integration)

**Status: DRAFT.** Nothing here is committed. This is the proposed append-only text for
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md`, in the shape of the round-46 attempt-1
block at `SHONEN.md:304-316` (`## Round 46 evidence`, four `- [~]` bullets, one per box, each with the
exact counting command, the value it printed, and the no-non-author-verifier note).

**Slot convention** (same as the sibling seat `R46bScribeScorecard`'s draft
`.ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/scorecard.md` §"Slot convention"):
`<AT-LANDING: cmd>` marks a value that only exists after the wave-1 integration commit lands; the
command inside the slot is the one that produces it, and the L1 substitutes the printed value and
deletes the slot. Every number not in a slot was printed by a run this seat performed; the command
that produced it is quoted inline with its output.

**Measurement basis.** Base export = `git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d | tar -x -C <scratch>`.
Tip export = `git -C <lane> archive ee03806b6b54a2822045e96641a77fa76984b410 | tar -x -C <scratch>`
(lane HEAD at this seat's read; the wave-1 integration commit does not exist yet).
Projection = the tip export plus this wave's real drafts (entry draft A
`R46bScribeEntryA.draft/github-repository-security-advisories.md`, the S074 row from
`R46bScribeRowsA.draft/rows.md`, admission block (a) from `R46bScribeAdmission.draft/appends.md`, and
the `knowledge-expected.txt` insert) — a scratch tree, **not** the landed tree. The L1's landing
measurement replaces every projection reading. Scratch root
`/fast/scratch/hyaku/kasegi-r46/R46bScribeShonen/` (`HYAKU_SCRATCH` unset → `/fast/scratch/hyaku`),
`TMPDIR` set explicitly; removed on exit.

---

## Round 46 (attempt 2) evidence

All four boxes stay `[~]`; `[x]` is operator-owned and no non-author verifier has judged this round yet.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 46 attempt 2, base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, lane HEAD
      `ee03806b6b54a2822045e96641a77fa76984b410`): `SKILL.md` is byte-identical base → tip
      (`git rev-parse 04af9bc9:SKILL.md ee03806:SKILL.md` prints `b659e3ec6911d362355c042943211c4a24c9fa7d`
      twice; 1166 lines, sha256 `0ac062d3e8a82f16d60214551ae37ca5c35614f7e61cef8eb228d6015b1894eb`);
      `python3 corpus/instruments/density.py SKILL.md --label r46b-scribe-tip` prints
      `| **mean dens** | | | | | | | | | **258.7** |` and `Total path-citation instances: 839 across 33 blocks.`
      (exit 0) — identical to the base export's `--label r46b-scribe-base` reading
      (`258.7`, `839 across 33 blocks`, exit 0), the two labels being the only difference;
      `python3 corpus/instruments/anchorcheck.py SKILL.md` prints
      `== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
      (exit 0) and `diff` of the base export's and the tip export's full anchorcheck output prints
      nothing (identical). The wave's registry block for the three new instruments
      (`r46-mutbat.py`, `r46-f29-gate.py`, `r46-selftest-f29.py`) is an L1 landing append, so the
      density mean it produces is `<AT-LANDING: python3 corpus/instruments/density.py SKILL.md --label r46a2>`
      and the appended block is **not** credited as depth (same reading as round 45's row,
      `SCORECARD.md:1749`: "SKILL.md mean 237.4 → 248.4 from an appended registry block, not credited
      as depth"). Box stays `[~]`; no non-author verifier.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 46 attempt 2): **none new.** No target testing, probing or submission was
      performed; the round is documentation-only (the wave brief in
      `.ufo/waves/round-46/attempt2/wave1-spec.json`: "Live-target testing is refused: this corpus is
      documentation only"). The closest executed work is the S074
      capture and the counter/gate runs above: `python3 corpus/instruments/source-recheck.py --manifest
      corpus/source-snapshots/round-46-a2/manifest.json --source S074` prints
      `S074:sha256 OK` then `S074:Q1 OK occurrences=1 anchor=10-ok` … `S074:Q9 OK occurrences=1 anchor=38-ok`
      (exit 0) on the projection tree, and `python3 corpus/instruments/r46-f29-gate.py --root <projection>`
      prints `f29-gate fixed=7/7 exit=0` — a gate over a captured page, not a domain task. No package was
      submitted and no submission is claimable. The box stays `[~]` until the operator authorizes a domain
      task.

- [~] Instructions executable by an agent without oral context
      — evidence (round 46 attempt 2): every counting command runs from a committed export and prints
      its reading. **C1 (depth:verifiability)** — `python3 corpus/instruments/r46-mutbat.py --root <tree>
      --pure <pure> --work <scratch> --counter both --jobs 8`: the frozen before-value at the base export
      is `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0` and
      `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0` (`BATEXIT=1`,
      receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`, sha256
      `13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd`); this seat's re-run of the same
      command over the **tip export** printed the first line
      `mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught` — byte-identical to
      the frozen receipt's line 1 — and was then stopped by this seat (exit 143, SIGTERM; see
      Limitations); the tip export's counters and selftests are byte-identical to the base export's
      (`git diff --name-status 04af9bc9 ee03806 -- corpus/` adds only `r46-f29-gate.py`, `r46-mutbat.py`
      and the round-46-a2 capture/manifest), so this reading is the base export's M01 reading;
      the after-value is `<AT-LANDING: the same command on the landing export>` → `mutbat counter=c1 …
      uncaught=0 baseline_failures=0` and `mutbat counter=c2 … uncaught=0 baseline_failures=0`, with the
      extended selftests green (`<AT-LANDING: python3 corpus/instruments/r46-counters-selftest-c1.py --pure
      <pure> --work <scratch> --jobs 8 | tail -1>` → `selftest cases=<n> failures=0` with `n` > 76, and
      `python3 corpus/instruments/r46-counters-selftest-c2.py --pure <pure> | tail -1` → `selftest cases=<n>
      failures=0` with `n` > 137). The **unchanged** selftest baselines were re-run by this seat at the tip
      export: `r46-counters-selftest-c1.py --pure <pure> --work <scratch> --jobs 8` printed
      `residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)`
      and `selftest cases=76 failures=0` (exit 0; 76 `case ` lines) — identical to the frozen receipt
      `controls/selftest-baselines.txt` (`selftest cases=76 failures=0`, `c1-exit=0`) — and
      `r46-counters-selftest-c2.py --pure <pure>` printed
      `selftest cases=137 failures=0` (exit 0; 137 `case `/`ok `/`probe ` lines) — identical to the frozen
      receipt's `selftest cases=137 failures=0` / `c2-exit=0`; the extended selftests' own tallies are
      `<AT-LANDING: …>` (`n` > 76 and `n` > 137 respectively).
      **C2 (coverage)** — `python3 corpus/instruments/r46-f29-gate.py --root <tree>`: the base export prints
      `f29-gate fixed=1/7 exit=1` (H4 `manifest-absent`; byte-identical to the frozen receipt
      `controls/f29-gate-at-base.txt`), the tip export prints `f29-gate fixed=2/7 exit=1`
      (`gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`, `gate H7 pass=1 read=census-rc=0 ok-line=1`),
      and the projection of the wave-1 drafts prints `f29-gate fixed=7/7 exit=0` (all seven limbs `pass=1`,
      `gate H1 pass=1 read=rows=29 admitted=29 F29=admitted`, `gate H5 pass=1 read=spans=28 located=28 failed=0 uncited=0 cores=5/5`,
      `gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0`);
      the after-value is `<AT-LANDING: the same command on the landing export>` → `f29-gate fixed=7/7 exit=0`.
      Do-nothing controls re-run by this seat on the round's committed fixtures
      (`.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode junk|fabricated`, same gate, same
      command): the junk tree prints `gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5`
      and `f29-gate fixed=6/7 exit=1`, the fabricated tree prints
      `gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5` and `f29-gate fixed=6/7 exit=1`
      — so the projection's `7/7` is not what a counter prints on a tree that does not answer.
      Secondary `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 29`: the tip export
      prints `frontier rows=28 admitted=28` / `frontier expected=29 admitted=28 verdict=SHORT exit=1`, the
      projection prints `frontier rows=29 admitted=29` (exit 0). **Standing counters** —
      `python3 corpus/instruments/recheck-audit.py --root <lane> --quiet` prints
      `strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0` and
      `executes=43 gated=22 broken=0` and `lines=65 total=65 pass=65 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`
      and `expect=present expected=65 missing=0 unexpected=0 exit=0` (exit 0) on the live lane; the same
      command over an export prints `strict pass=1/65 cdroot_fail=64` and `exit=1` **only** because the
      exported `recheck:` lines `cd` into the live lane path — with `--cdroot <lane>` added the export reads
      `strict pass=65/65 cdroot_fail=0 instrument_fail=0 own_fail=0` … `expect=present expected=65 missing=0 unexpected=0 exit=0`
      (exit 0), so the export's red is an artifact of the export and not a lane reading;
      `python3 corpus/instruments/frontier-recheck-count.py --root <tree>` prints
      `FRONTIER-CENSUS rows=28 admitted=28 closed=28 problem-rows=0 registry=73` and `entries=31 pass=31 exit=0`
      at the tip export, and on the projection `FRONTIER-CENSUS rows=29 admitted=29 closed=29 problem-rows=0 registry=74`
      and `entries=32 pass=32 exit=0` (incl. `PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S074           exit=0`);
      `python3 corpus/instruments/capture-binding-check.py --root <tree>` prints at the base export
      `records=60 bound=60 unbound=0` (exit 0), at the tip export `FAIL rule=no-row record=S074 dir=round-46-a2`
      and `records=61 bound=60 unbound=1` (exit 1 — the committed S074 capture has no registry row yet, the
      very defect the wave's S074 row closes), and on the projection `records=61 bound=61 unbound=0` (exit 0);
      `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <tree>/corpus/SOURCES.md`
      prints the three pre-existing `file W04 …` warnings and `file ok …` (exit 0) at the base export, at the
      tip export and on the projection, and `census --file …` prints `file rows 73` (base, tip) and
      `file rows 74` (projection). Plain counts (`bash corpus/instruments/r46-plain-measure.sh <tree>`):
      `c1a=21 c1b=22 c2a=28 c2b=73 c2c=65 c2d=3` at both the base and the tip export, and
      `c1a=21 c1b=22 c2a=29 c2b=74 c2c=66 c2d=3` on the projection. Box stays `[~]`; no non-author verifier.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 46 attempt 2, base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`): `PROVINCE.md` is
      byte-unchanged base → tip (`git rev-parse 04af9bc9:PROVINCE.md ee03806:PROVINCE.md` prints
      `e22cdf9b5b80ae717acec15ebc48579e9c609ed0` twice; 171 lines, sha256
      `d3642efc158a934e16f34969d50d81e9d69be71805770cc2a7acc32c41e9e6aa`), and the F29 province amendment is
      **owed and not applied** at this read (`grep -c 'F29' PROVINCE.md` prints `0`; the appended list stops
      at F28, `PROVINCE.md:171`: "[r46 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F28 — GitHub private vulnerability reporting, reporter flow …"). The amendment the wave drafts is an end-of-file append
      with a scope limit (`R46bScribeAdmission.draft/appends.md` block (b)): "F29 — GitHub repository security
      advisories, maintainer-side lifecycle … scope limit: maintainer-side advisory lifecycle only — the
      reporter flow stays F28, and advisory editing, the REST API for repository security advisories and
      GitHub Advisory Database edits stay out" — the same shape as F28's line and the same hold-out of the
      reporter-side ground F28 already holds. The sibling sweep
      `.ufo/waves/round-46/attempt2/wave1/R46bScoutAdjacent.md` (VERDICT: DRAFT-READY) walked all 20 sibling
      corpora plus `shokuknow` and rules F29 uncontested: the only sibling GHSA holdings are a published
      advisory used for patch-state facts (mori S012, self-ruled "adjacency only"), consumer-side advisory
      records (kaidoku's OSV JSON) and GitHub Docs nav chrome (tabi), while sixteen corpora print a clean zero;
      its §4 names the F28 sentences the new entry must contrast (`corpus/knowledge/github-private-vulnerability-reporting.md:9`,
      `:13`, `:40`, `:43`) rather than absorb, and the F28 entry holds that ground out at `:9`
      ("The entry does not record the maintainer-side flow"). The absence sweep
      `grep -rliE 'repository securit. advisor|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md`
      prints `2` files at the base export and at the tip export and `4` on the projection (the entry, the
      SOURCES row, the README F29 row and the F28 entry) — the entry does not yet exist at the tip
      (`ls corpus/knowledge/github-repository-security-advisories.md` → `No such file or directory`;
      `grep -c 'F29' corpus/README.md` = 0; `grep -c 'S074' corpus/SOURCES.md` = 0). Box stays `[~]`;
      no non-author verifier.

---

## Limitations of this draft (the L1 must read these before landing)

1. **The round tip does not exist yet.** Every `<AT-LANDING: …>` slot is a value that only the wave-1
   integration commit produces; this seat did not and could not run any command against it. The measured
   values in the bullets are the base export, the tip export `ee03806` (the wave-1 *spec* commit — it adds
   only `.ufo/waves/round-46/attempt2/` files, no corpus change: `git diff --name-status 04af9bc9 ee03806 --
   corpus/` prints `A corpus/instruments/r46-f29-gate.py`, `A corpus/instruments/r46-mutbat.py`,
   `A corpus/source-snapshots/round-46-a2/S074.txt`, `A corpus/source-snapshots/round-46-a2/manifest.json`)
   and the projection of the wave's drafts.
2. **The projection is not the landed tree.** It applies one entry draft (draft A of six competing drafts),
   one SOURCES row draft, one admission block and one `knowledge-expected.txt` insert. If the L1 lands a
   different entry draft, the projection readings (`f29-gate fixed=7/7 exit=0`, `entries=32 pass=32`,
   `records=61 bound=61 unbound=0`, `frontier rows=29 admitted=29`) change; the L1's own landing measurement
   is the binding value.
3. **The battery run was stopped, not completed.** This seat's
   `python3 corpus/instruments/r46-mutbat.py --root <tip export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
   --work <scratch> --counter both --jobs 8` printed the first mutant line
   `mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught` (byte-identical to the
   frozen receipt `controls/mutbat-before.txt` line 1) and was then stopped by this seat (`BATEXIT=143`,
   SIGTERM) once the c1/c2 selftest baselines had been re-run; a first attempt over the base export hit
   the tool's 1200-second cap after printing `error: interrupted`. The host was under a load average above
   200 with many sibling seats running the same battery concurrently. The c1/c2 summary lines quoted in
   bullet 3 are therefore **the frozen receipt's** values (`controls/mutbat-before.txt`), not this seat's
   own completed run. The sibling seat `R46bScribeScorecard` reports the same cap (`BATEXIT=124`) on its
   base replay. The L1's landing measurement supplies the after-value.
4. **Both selftest baselines were re-run by this seat at the tip export and both reproduce.** The c1
   selftest printed `selftest cases=76 failures=0` (exit 0) and the c2 selftest printed
   `selftest cases=137 failures=0` (exit 0) — identical to `controls/selftest-baselines.txt`
   (`c1-exit=0`, `c2-exit=0`). What this seat did **not** run to completion is the battery
   (Limitation 3); the extended selftests' own tallies (`n` > 76 / `n` > 137) exist only after the
   wave's selftest extension lands and are `<AT-LANDING: …>` slots.
5. **No non-author verifier has judged any of this.** The four boxes are `[~]`; `[x]` is operator-owned
   (`corpus/lessons/round-45-verifier-spotcheck.md` §7). The wave-2 seats `R46bW2CritVerdictC1` /
   `R46bW2CritVerdictC2` are the round's internal critics, not non-author verifiers.
6. **No file outside this seat's draft directory and this seat's Report was written.** No git or jj
   mutation was performed; `git log` / `git diff` / `git rev-parse` / `git archive` (read-only) were the only
   git commands run. No tool was installed or upgraded; `pacman` was not invoked (the operator's tooling
   directive at `/home/vgpnk/.omp/agent/RULES.md` was read; the host-wide pacman guard made an install
   unnecessary — every command used here is stock `python3` / `bash` / `grep` / `git`).
