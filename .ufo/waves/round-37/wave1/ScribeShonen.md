# ScribeShonen — round-37 SHONEN box lines (draft)

Seat: ScribeShonen (scribe, leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`).
Axis owned: calibration. Milestone: round-37. Receipt path: `.ufo/waves/round-37/wave1/ScribeShonen.md`.

This seat wrote only this receipt and scratch under `/fast/scratch/hyaku/kasegi-r37/ScribeShonen/`
(removed before yielding). `SHONEN.md` was **not** edited — the L1 appends the block. No lane file,
fleet file, sibling repo or source tree was written; no mutating git command was run (read-only
`log`/`rev-parse`/`status`/`ls` only); no tool was installed or upgraded; no network fetch.

---

## 1. Calibration boundary — what this seat measured (HEAD `b362068`, detached)

All values below were produced by this seat at 2026-10-26T17:05–17:10Z, from the lane root, on the
bytes at HEAD (three commits past base by design: `224df74` freeze, `f324655` wave evidence,
`b362068` claims-erratum-1; `git rev-parse 224df74^` = `b56a4168` per `ExecQuiescenceProbe.md` §1).

| quantity | measured value | command |
|---|---|---|
| `SKILL.md` | sha256 `2ddb1bc72872a54a87f2b3655d6612c4b5bae86ea154a612aa42cfc5fcc1fd8f`, 1111 lines | `sha256sum SKILL.md`, `wc -l < SKILL.md` |
| density of `SKILL.md` | mean **225.3**, 27 blocks, 751 path-citation instances | `python3 corpus/instruments/density.py SKILL.md` |
| anchors of `SKILL.md` | `16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 | `python3 corpus/instruments/anchorcheck.py SKILL.md` |
| D5 defect state | `grep -cF 'gate\|probe' SKILL.md` = **6** (lines 1064, 1077, 1097, 1098, 1110, 1111); `r36-closure.sh` row at `SKILL.md:1111` has type cell `gate\|probe` | `grep -nF 'gate\|probe' SKILL.md` |
| r37 suite absent | `grep -c 'r37-closure.sh' SKILL.md` = 0; `ls corpus/instruments/r37-closure.sh` → No such file | same |
| LOG state | `grep -c '^## Round 37' LOG.md` = **0**; `grep -c '^## Round 36'` = 1; 1675 lines | `grep -c`, `wc -l` |
| recheck-audit | `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0`; `expect=present expected=48 missing=0 unexpected=0 exit=0` | `python3 corpus/instruments/recheck-audit.py --quiet` |
| frontier harness | `entries=22 pass=22 exit=0` (F18/S052, F19/S053) | `python3 corpus/instruments/frontier-recheck-count.py` |
| census | exit **0**, only `W04 S028`, `W04 S029` | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` |
| knowledge entries | 48 files; `knowledge-expected.txt` 50 lines (2 `#` + 48 entries) | `ls corpus/knowledge/*.md \| wc -l` |
| capture binding | `records=43 bound=43 unbound=0` (plus pre-existing `orphans=1 orphan=S040-live.txt`, `multi_row_url=2`) | `python3 corpus/instruments/capture-binding-check.py` |
| frontier rows | **19** | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` |
| registry rows | **53**; `S054` hits **0**; entries citing `source: S054` **0** | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, `grep -c 'S054'` |
| `PROVINCE.md` | 78 lines, sha256 `b0e91a611feadeeae38df7fd7fa55d8efe56039721cc35a024ca8af81108b5a9`; EOF amendment list ends at F19 (line `F19` present); `grep -c 'F20' PROVINCE.md` = **0** | `wc -l`, `sha256sum`, `grep`, `tail -6` |
| quiescence now | `git status --porcelain` = 6 lines, all `?? .ufo/waves/round-37/…`; 0 outside the wave dir (`ExecQuiescenceProbe.md` §2 corroborates) | `git status --porcelain` |
| `final-gates/` | `.ufo/waves/round-37/final-gates/` **absent** at this read (E10 artifact not yet produced) | `ls` |

Everything else appearing in the four lines below is either (a) a **frozen-claim contract value**
(`.ufo/waves/round-37/claims.json` after `claims-erratum-1.md`), or (b) a **seat mirror measurement**
whose receipt is named in the pointer table (§3). No contract value is presented as this seat's
observation.

---

## 2. The four box lines (append-ready)

```markdown
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 37, base `b56a4168`; claims-freeze `224df74d`; final lane head
      `<r37-final-lane-hash>`): the Gates & probes registry keeps the exact-basename rows the r37 suite's
      E3 reads (`r35-defect-closure.sh`, `r36-closure.sh`) and registers the new suite in the same table
      (`r37-closure.sh`, export-mode only); the `r36-closure.sh` row's type cell is a single choice
      instead of the literal `gate\|probe`, and its verdict map gains exit `2` → `could-not-evaluate`
      (E13, closing spot-check D5 — `corpus/lessons/round-36-verifier-spotcheck.md` §5). At this seat's
      base read (`b362068`) `SKILL.md` is sha256 `2ddb1bc7…`, 1111 lines, `grep -cF 'gate\|probe'
      SKILL.md` = 6 with the r36 row at `:1111`, `grep -c 'r37-closure.sh' SKILL.md` = 0 and
      `corpus/instruments/r37-closure.sh` absent; on those bytes `density.py SKILL.md` reads mean
      **225.3** over 27 blocks / 751 path-citations and `anchorcheck.py SKILL.md` reads `16 in-range cite
      instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0.
      Post-append re-measurement <fill: mean/blocks/cites and `git diff --numstat <base> -- SKILL.md` from
      `.ufo/waves/round-37/wave1/RevNoHarm.md`>; the change is one appended registry row plus one
      in-place type-cell correction — a registration and D5 correction, no score move claimed. Pointers:
      `.ufo/waves/round-37/wave1/ExecC1SuiteBuild.md` (suite text and the `E3`/`E13` limb bytes),
      `RevC1Suite.md` (per-check false-green review), `RevNoHarm.md` (base/after no-harm reads),
      `ExecC1BaseFail.md` §2 (base suite state). Box stays `[~]`; no non-author check yet.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 37): **no new end-to-end domain task ran this round.** At this seat's read
      `grep -c '^## Round 37' LOG.md` = 0 (1675 lines; newest heading `## Round 36`), and the round-37
      block (draft `.ufo/waves/round-37/wave1/ScribeLOG.md`) logs instruments and an admission, not a
      hunt-to-claim task; the wave spec (`.ufo/waves/round-37/wave1-spec.json`, 64 seats) contains no
      domain-task seat. The closest executed measurements remain instrument and admission work:
      C1 — the r36 suite's red controls were re-measured this round,
      `r36-closure.sh --export-ref cc692008…` → `closed=4/9 exit=1` (open E1/E3/E4/E8/E9) and the r36
      judged head `a23dc478…` → `closed=8/9 exit=1` with only the live E9 limb open
      (`.ufo/waves/round-37/wave1/ExecC1BaseFail.md` §2), while the r37 suite's own reds are
      <fill: `closed<14/14 exit=1` at `cc692008…` and `a23dc478…` from `ExecC1BaseFail.md`/
      `ExecC1JudgedHeadFail.md`>; C2 — the S054 capture (`ExecC2Capture.md`, `S054.txt` + `manifest.json`)
      and the frontier harness `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054`
      (`ExecC2Harness.md`). Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 37, base measured 2026-10-26T17:10Z at `b362068`): `recheck-audit.py` prints
      `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0` and
      `expect=present expected=48 missing=0 unexpected=0 exit=0`; `frontier-recheck-count.py` prints
      `entries=22 pass=22 exit=0`; `sources-census.sh validate --root <fleet> kasegi` exits 0 with only
      `W04 S028`/`W04 S029`; the tree carries 48 `corpus/knowledge/*.md` and
      `capture-binding-check.py` `records=43 bound=43 unbound=0`. The round-37 after-state:
      `strict pass=49/49` / `expected=49` (`.ufo/waves/round-37/wave1/ExecExpectedListSync.md` §2–§3
      mirrors it, and the no-sync control `unexpected=1 exit=1` proves the sync load-bearing),
      `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054`,
      `source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` exit 0,
      `records=44 bound=44 unbound=0`, census exit 0 (`ExecCensusReplay.md` §2–§3), and the new suite
      `bash corpus/instruments/r37-closure.sh --selftest` → `selftest cases=14 failures=0` with the
      `--export-ref <r37-final-lane-hash>` run → `closed=14/14 exit=0`, whose raw transcript is the
      committed `.ufo/waves/round-37/final-gates/all-gates.txt` (digest header
      `suite-sha256=<sha>`, fourteen `E<n> payload=` lines, fourteen `selftest case=` lines, E10).
      Final-head values <fill from `ExecExpectedListSync.md`, `ExecC2Harness.md`/`RevHarnessSync.md`,
      `RevSourceRecheck.md`, `ExecManifestChecks.md`, `ExecC1SuiteBuild.md`/`RevC1Selftest.md`>. Box stays `[~]`.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 37, base `b56a4168`): `PROVINCE.md` is 78 lines, sha256 `b0e91a61…` at this read,
      its appended frontier list ending at F19; `grep -c 'F20' PROVINCE.md` = 0, so the round-37 F20
      amendment is owed at this read and lands as a one-line end-of-file append under R6
      (draft `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`), in the F16–F19 form. F20 sits
      inside the province (core "program rules, claim packages"; the F13/F17/F18/F19 severity- and
      prioritization-scope precedent). F20/S054 is uncontested: the 20-lane sweep and the combined
      ruling (`ExecSiblingSweep.md`, `ScoutF20Sibling.md`, `ConnSibling.md`) find no sibling ground —
      nearest neighbour is kagi's retained NVD/SSVC probe (the SSVC Exploitation decision point, a
      different framework), reported and not absorbed <fill: the ruling's verbatim
      "uncontested" sentence>. The junk twin is rejected (`ExecC2JunkControl.md`, `MutJunkTwin.md`).
      At this read frontier rows = 19 (`grep -cE '^\| F[0-9]+ \|' corpus/README.md`) and `S054` registry
      rows = 0; after, frontier 20 and registry 54. Box stays `[~]`; no non-author check.

**Round-37 measurement state (ScribeShonen, 2026-10-26T17:10Z; HEAD `b362068`, detached).** Base at
spawn `b56a4168`; HEAD is three commits past it (`224df74` claims freeze, `f324655` wave evidence,
`b362068` claims-erratum-1), all the round's own. Values marked with a command in §1 are this seat's
reads on the HEAD bytes; every "after" value above is frozen-claim contract or a named seat's mirror
measurement until the final-head run, and nothing in this block is claimed as a final-head run by this
seat. `<fill …>` placeholders are for the L1/integrator: the r37 final lane hash, the post-append
density/anchor pair and `git diff --numstat`, the r37 suite's two red counts, and the sibling-ruling
phrase. `git status --porcelain` at this read = 6 lines, all `?? .ufo/waves/round-37/…` (0 outside the
wave dir); quiescence is a filing-time property reached at integration, not at this read, and
`.ufo/waves/round-37/final-gates/` does not exist yet. All four boxes stay `[~]`: a wave seat is the
lane and cannot write a checked box; promotion needs a named non-author verifier.
```

---

## 3. Pointer status at this read (17:10Z)

`landed` = file present in `.ufo/waves/round-37/wave1/` when this receipt was written; `pending` = the
draft names the wave receipt the L1 will have at append time. The L1 should confirm every `pending`
pointer exists before appending the block.

| receipt | status | what the line takes from it |
|---|---|---|
| `ExecC1BaseFail.md` | landed | r36 base `closed=4/9 exit=1`; r36 judged head `closed=8/9 exit=1`; r37 suite absent at base/live head (§ Blocker) |
| `ExecC2JunkControl.md` | landed | junk-f20 twin content + rejection discriminating control |
| `ExecC2QuoteOnce.md` | landed | S054 quote occurrence counts/anchors (supports box 3's source-recheck pointer) |
| `ExecCensusReplay.md` | landed | census base exit 0 + W04 S028/S029; mirror-with-S054 exit 0; row must sit inside `## Registry`; row+entry land together |
| `ExecExpectedListSync.md` | landed | mirror `strict pass=49/49`, `expected=49`; no-sync control `unexpected=1 exit=1` |
| `ExecManifestChecks.md` | landed | base `records=43 bound=43 unbound=0`; selftest `cases=23 failures=0`; rule A/B/C definitions |
| `ExecQuiescenceProbe.md` | landed | pre-seat quiescence `0`, base binding via `224df74^`, 6 untracked wave artifacts |
| `ExecRegressionBase.md` | landed | base transcript of every existing instrument |
| `ExecC1SuiteBuild.md` | pending | r37 suite text, `E3`/`E13` limbs, `selftest cases=14 failures=0` |
| `ExecC1JudgedHeadFail.md` | pending | r37 suite red at `a23dc478…` |
| `ExecC2Capture.md` | pending | S054 capture + manifest (URL per `claims-erratum-1.md`) |
| `ExecC2Harness.md` | pending | `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054` |
| `ExecSiblingSweep.md`, `ScoutF20Sibling.md`, `ConnSibling.md` | pending | 20-lane sweep hits + uncontested/province ruling |
| `RevC1Suite.md`, `RevC1Selftest.md` | pending | per-check false-green review; selftest acceptance bar |
| `RevHarnessSync.md`, `RevSourceRecheck.md`, `RevNoHarm.md` | pending | independent harness delta; S054 recheck contract; base/after density+anchor and diffstat |
| `MutJunkTwin.md` | pending | near-miss/duplicate-quote twin rejections |
| `ScribeLOG.md`, `ScribeFrontierAmendments.md` | pending | round-37 LOG block; PROVINCE F20 amendment line |
| `.ufo/waves/round-37/final-gates/all-gates.txt` | pending | E10 raw transcript (digest header, 14 payload lines, `closed=14/14 exit=0`, 14 case lines, `cases=14 failures=0`) |

---

## 4. Findings and calibration notes

1. **The r36 suite's red is not the r37 suite's red.** `ExecC1BaseFail.md` measured the *r36*
   instrument (`r36-closure.sh`, sha256 `4db1ae70…`, 9 checks) at the r36 base; the frozen C1 predicate
   needs the *r37* instrument's 14-check red at the same refs. That seat states the blocker verbatim:
   "`corpus/instruments/r37-closure.sh` is absent at both the r36 base and the live lane head
   `b362068…`". The draft therefore labels the r36 numbers as this round's re-measurement and leaves the
   r37 reds as `<fill>` — the frozen claim's after-state is contract until that run exists.
2. **E13 vs the no-harm expectation (report, not adjudicate).** E13 requires the `r36-closure.sh`
   registry row's type cell to be a single choice, i.e. an **in-place edit** of `SKILL.md:1111`
   (`gate\|probe` → one choice) and an added exit-2 verdict cell, while the `RevNoHarm` seat prompt
   prepares an append-only reading ("after must be append-only for SKILL.md/… (zero deletions; existing
   line numbers preserved)"; "only appended registry rows after :1106"). Both cannot hold literally.
   The draft words box 1 as "one appended registry row plus one in-place type-cell correction" so the
   no-harm report must be read that way; the L1/judge decides whether the no-harm contract is amended.
3. **F20 amendment is owed at this read, not applied.** `grep -c 'F20' PROVINCE.md` = 0 and the EOF
   list ends at F19; box 4 says "owed at this read and lands as a one-line end-of-file append", matching
   the F16–F19 form, rather than claiming it was already appended.
4. **URL literal.** The C2 capture URL is the erratum-1 value
   `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`, not the frozen home-page literal
   `https://certcc.github.io/SSVC/`; the draft cites no URL literal in the boxes, so an erratum change
   cannot make a box line false, and `ExecCensusReplay.md` §3 confirms the mirror row uses the tutorial
   URL.
5. **Base binding.** `git rev-parse master` is not `b56a4168` at this read (it is HEAD `b362068`); the
   honest assertion is `git rev-parse 224df74^` = `b56a4168`, which `ExecQuiescenceProbe.md` §1 supplies
   and this seat mirrors in the measurement-state paragraph. HEAD is detached.
6. **Quiescence is not yet true and the draft does not say it is.** 6 untracked entries, all the wave's
   own `.ufo/waves/round-37/` paths; the E9 quiescence limb can only close after integration commits
   them. `final-gates/` is likewise absent.
7. **Box 2 stays `[~]` with "none new",** consistent with the round-35/36 pattern and with the
   round-36 spot-check's promotion note (`corpus/lessons/round-36-verifier-spotcheck.md` closing
   paragraph: box 2 "remains `[~]` with 'none new', so the checklist is not fully checkable by a
   non-author this round").
8. **Box 1's registration is not a live-green claim.** The registry rows are registration; the suite
   runs that turn them green are the final-head `--export-ref` and `--selftest` runs named in box 3.
9. **No non-author check exists for any box.** Each line ends with the `[~]` reason; nothing here
   upgrades a box.

---

## 5. Write scope, tooling, scratch

- Writes: this receipt only. `SHONEN.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`,
  `corpus/**` and `.ufo/waves/round-37/{claims.json,claims-erratum-1.md,c1-controls,c2-controls,
  census-before.txt,wave1-spec.json,wave1-dispatch.json}` were read, never written.
- Scratch: `/fast/scratch/hyaku/kasegi-r37/ScribeShonen/` created and removed before yielding; no
  `/tmp` use; no inherited `TMPDIR` reliance.
- Tooling: none installed or upgraded (pacman paused host-wide; not invoked).
- Network: none.
- Mutating git: none. Read-only `git log`/`rev-parse`/`status` only.

Report: .ufo/waves/round-37/wave1/ScribeShonen.md
