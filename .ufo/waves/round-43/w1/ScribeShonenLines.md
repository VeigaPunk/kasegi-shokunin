# ScribeShonenLines — round 43 receipt

Seat: `ScribeShonenLines` (scribe, leaf — no subagent dispatch, no swarm).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` · round 43 · base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Measured at lane HEAD `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (the round-43 freeze commit) on 2026-10-28,
16:38–16:47Z. Frozen claims read first and not edited: `.ufo/waves/round-43/claims.json`
(sha256 `a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`, matching `freeze.txt`'s
`claims-sha256=`).

## Deliverable

| item | value |
|---|---|
| path | `.ufo/waves/round-43/w1/ScribeShonenLines.append.md` |
| lines | **8** (4 box lines + 4 evidence lines) |
| sha256 | **`fc13ac07d944f1c96912ffd6da9d16c37188f6791b5569d5cf0044e10b6071aa`** |
| form | no `## Round 43 evidence` heading; one indented `— evidence (...)` line per box; four `[~]`; zero `[x]`; zero `<pending>` token (appendable verbatim) |
| append target | `SHONEN.md` (285 lines, ends `\n\n`; the landable block begins on line 286 after the existing blank line) |

Rehearsal (scratch copy, lane file untouched): `cp SHONEN.md $S/SHONEN.final.rehearsal.md && cat …append.md >> …`
→ `293` lines (`285 + 8`); `grep -c '^## Round 43'` = `0`; `grep -c '^- \[~\]'` = `40` (36 existing + 4 new);
`grep -c '^- \[x\]'` = `0`; `grep -c '^- \[ \]'` = `0`; pairing check over the 8 appended lines prints
`block lines=8` with no `BAD box` / `BAD evidence` line (odd lines match `^- \[~\] `, even lines match
`^      — evidence \(`).

## Measurements — commands and real output

All from the lane root unless noted; every corpus counter ran read-only against committed bytes.

| # | command | observed (true shell exit captured separately, not a pipeline tail) |
|---|---|---|
| 1 | `git rev-parse HEAD` | `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` |
| 2 | `git log --oneline -6` | `4cb6d4a round-43: frozen claims C1 … C2 … v2 wave spec and dispatch (73 seats)`; parent `ab98fac round-42 verifier spot-check …` |
| 3 | `git status --porcelain` | only `?? .ufo/waves/round-43/w1-REGISTRY.txt`, `?? …/w1.ready`, `?? …/w1.ready.partial`, `?? …/w1/` — no tracked modification, no lane byte of mine among them |
| 4 | `wc -l PROVINCE.md SKILL.md SHONEN.md` | `165 PROVINCE.md` / `1134 SKILL.md` / `285 SHONEN.md` |
| 5 | `sha256sum PROVINCE.md SKILL.md` | `8deea5ea1c58457341aa58252639de2156a3c3b92b7b395de3b9c75609e7ccc2  PROVINCE.md`; `9eef84d163173c8e840732458d70b5c14050289cbf0c4f0d2414780a74f92b57  SKILL.md` |
| 6 | `git diff --numstat ab98fac9 -- PROVINCE.md SKILL.md SHONEN.md` | empty (all three byte-identical base→freeze) |
| 7 | `git diff --stat ab98fac9 HEAD` | 9 files, 2004 insertions — the round-43 freeze record, spec, dispatch and controls only |
| 8 | `python3 corpus/instruments/density.py SKILL.md` | `# Density census — SKILL.md (1134 lines, 30 blocks)` … mean **234.2** … `Total path-citation instances: 782 across 30 blocks.` — exit 0 |
| 9 | `python3 corpus/instruments/anchorcheck.py SKILL.md` | `== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` — exit 0 |
| 10 | `python3 corpus/instruments/capture-binding-check.py` | `records=56 bound=56 unbound=0` (AUDIT line: `records=56 with_url=56 with_fetched_utc=18 with_archival=38 … orphans=1 orphan=S040-live.txt`) — exit 0 |
| 11 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=28 pass=28 exit=0` — true exit 0 |
| 12 | `python3 corpus/instruments/recheck-audit.py --quiet` | `lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; `expect=present expected=61 missing=0 unexpected=0 exit=0` — true exit 0 |
| 13 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi W04 S028 duplicate url …`, `kasegi W04 S029 duplicate url …`, `kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md` — true exit 0 |
| 14 | `ls corpus/knowledge/*.md \| wc -l`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | `61`; `66`; `0` — identical to `.ufo/waves/round-43/c2-controls/before.txt` (measured 16:34:15Z) |
| 15 | `grep -c 'r43-closure\|claim-package-check' SKILL.md` | `0` (no Gates & probes row for either new instrument in the freeze bytes) |
| 16 | `grep -n "claim packages\|Sibling lanes are reported" PROVINCE.md` | `3:**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages`; `9:…`; `29:The line-3 domain comprises program rules, scopes, and claim packages; the`; `45:Sibling lanes are reported, not absorbed:` (`sed -n '29,30p;45p'` confirms `:30` = `core also covers triage and claim gates, and submission/disclosure packaging.`) |
| 17 | `bash corpus/instruments/r43-closure.sh; echo exit=$?` | `bash: corpus/instruments/r43-closure.sh: No such file or directory`, `r43-run-exit=127` |
| 18 | `ls corpus/instruments/r43-closure.sh; echo ls-exit=$?` | `No such file or directory`, `ls-exit=2` |

### Base-control reading (disclosure, not a defect)

`.ufo/waves/round-43/c1-controls/do-nothing.txt` §A records the absent suite with `exit=2`; `claims.json`'s C1
`before` cell says `exit 127`. Both are right for different commands: `ls` exits 2 (row 18), the `bash`
invocation exits 127 (row 17). Box 3's evidence line names this so no reader takes the control's `2` as the
run's code.

The control's §B (the r42 stand-in over the base export, run at `run-utc=2026-10-28T16:27:52Z`) prints
`closed=12/13 exit=1` with `J8 … closed=0` and `J1`–`J7`, `J9`–`J13` `closed=1`. Box 3 cites it as the
committed control's recording, not as this seat's run.

### S067 capture — re-verified by this seat

`sha256sum .ufo/waves/round-43/w1/ExecSourceCapture.S067.txt` → `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b`;
`wc -l` → `131`; `sed -n '69p;99p;112p;113p;126p'` returns the five manifest quotes verbatim (`Project curl
Security Advisory, October 11 2023 Permalink` … `This issue was reported to the curl project on September 30,
2023. We contacted distros@openwall on October 3, 2023.`), matching anchors Q1/Q2/Q3/Q4/Q5.
Provenance (`w1/ExecSourceCapture.provenance.txt`): `https://curl.se/docs/CVE-2023-38545.html`, `HTTP status: 200`,
`13940 bytes served`, `UTC fetch: … 2026-10-28T16:39:59Z`, `redirects=0`. Box 2 quotes these.

### K19 limb transcript — read, not re-run

`w1/ExecK19Freeze.transcript.txt` records `K19 payload=freeze=present,order=ok,sha=match closed=1` `rc=0` for the
live round-43 commit, `K19 … closed=0` `rc=1` for base `ab98fac9`, and red for seven mutants (`m-early`,
`m-late-baddigest`, `m-dupe-measured`, `m-offset`, `m-missing-line`, `m-label-drift`, `m-max-drift`) plus the
no-argument case. Box 3 cites that file; this seat did not re-execute the limb.

## Findings and L1 actions

1. **The block carries no `<pending>` token — the L1 can append it verbatim.** Two limbs are stated as
   self-contained conditions instead: box 1 says both density/anchor figures describe the *pre-append* bytes
   and that any Gates & probes row for `r43-closure.sh` / `claim-package-check.py` is an L1 landing append not
   covered by them (no dispatched seat owns a `SKILL.md` edit — the dispatch sweep for `SKILL.md` /
   `Gates & probes` yields only `CritProvinceScope`, a receipt-only seat); box 4 points the province-fit /
   non-authorization ruling at this round's `w1/CritProvinceScope.md` without asserting its content. If the L1
   does append the registry rows, the density mean moves off **234.2** and `SKILL.md`'s line count and sha256
   move with it — re-measure before quoting either figure in a later record.
2. **If `ExecExemplarPackage` or `ExecGateSelftest` does not land**, boxes 2 and 3's exemplar clause must be
   dropped before appending; the S067 capture clause stands on its own (it is re-verified above). The
   `expects` tokens in boxes 2/3 come from the frozen `claims.json` after-state
   (`rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`, `selftest cases=10 failures=0`, `closed=19/19 exit=0`,
   `selftest cases=19 failures=0`), not from any run this seat observed.
3. **Report consistency risk.** `w1/ScribeReportSkeleton.report.md` §SHONEN box 1 lists "the `r43-closure.sh`
   registry row" as evidence. While that row is absent from the freeze bytes (row 15 = 0), the report sentence
   and this block agree only if the L1 lands that row; otherwise the report's box 1 is a K14-class narrative
   mismatch against `SKILL.md`.
4. **After-state counters are not yet observable.** At the freeze commit the corpus reads `61` knowledge files,
   `66` registry rows, `records=56`, `expected=61`, `entries=28` — the frozen C2 `before` values. Box 3 quotes
   these as freeze-commit values and does not claim the `68/57/62` after-state.
5. **Out-of-scope message answered.** `W1ScribeLessonGate` reported an unescaped pipe in souji's
   `corpus/SOURCES.md:189` (S242, `NF=14`, validator `rc=1`). Not a kasegi file and not in my write scope; I
   replied that it must route to the souji lane owner. No edit made anywhere.
6. **No product edit, no commit, no judge.** Read-only git only (`rev-parse`, `log`, `status`, `diff`,
   `--numstat`, `--stat`). No `add`/`commit`/`push`/`checkout`/`stash`/`branch`/`tag`/`worktree`. No fixture git
   repo was created. No fleet-root or shokuknow write.

## Tooling

None installed or upgraded: no `pacman` transaction (host-wide pause), no `uv tool install`, `npx` package or
release binary. No config file touched.

## Scope and cleanup

Writes: only `.ufo/waves/round-43/w1/ScribeShonenLines.append.md` and this receipt, both under the wave dir,
plus scratch in `/fast/scratch/hyaku/kasegi-r43/ScribeShonenLines/` (disk guard checked before the pass).
`SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `corpus/**` and every sibling lane are untouched by this seat. Scratch
removed at seat close.
