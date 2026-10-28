# kasegi-shokunin — Promotion checklist

> Current pointers: the round-35 paragraphs appended at the end of this file are the boxes' current
> evidence. The four paragraphs immediately below are the round-34 state, retained as history.
> All four boxes remain `[~]`.

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 34, base `014ee2d7`; `SKILL.md` byte-unchanged this round:
      `git diff --numstat 014ee2d7 -- SKILL.md` empty and `sha256sum SKILL.md` still
      `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`, 1090 lines): the round-34
      no-harm sweep re-measured those bytes — `density.py SKILL.md` mean dens **201.7** over 25 blocks
      and 710 path-citation instances (the round-33 value reproduced), exit 0; `anchorcheck.py SKILL.md`
      `12 in-range cite instances, 0 bad`, `LOST-RECORDED=306`, `PIN-BROKEN=0`, exit 0; and
      `git diff 014ee2d -- SKILL.md PROVINCE.md | grep -cE '^-[^-]'` = 0
      (`.ufo/waves/round-34/wave1/RevNoHarm.md` §A/§B/§C; same figures in
      `.ufo/waves/round-34/wave1/ScribeSkillGate.md` §3). Open, not closed: `ScribeSkillGate.md`
      §4b's conditional obligation fired when `capture-binding-check.py` was hardened — the round-33
      re-verify row (`SKILL.md:1090`) still pins `target b4182665…`, 492 lines, `selftest cases=11`
      against the landed `3d9e5e0ddbaaccf9…`, 892 lines, `selftest cases=23`
      (`.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md` §Commands, §Addendum); the append-only
      EOF correction is not yet in `SKILL.md`. Box stays `[~]`.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 34): **no new end-to-end domain task ran this round.** `grep -c '^## Round 34'
      LOG.md` = 0 and the newest heading is `## Round 33` at `:1597` (1599 lines). Correcting the
      round-33 text in this box: it said no `## Round 33` heading existed — true at `9f98488`
      (`git show 9f98488:LOG.md | grep -c '^## Round 33'` = 0, 1595 lines) but false at HEAD, where
      the closure commit `5b7a039` appended it at `:1597`. The closest executed measurement remains
      the capture-binding check — round 33 `records=40 bound=40 unbound=0` exit 0 twice,
      `selftest cases=11 failures=0` (`.ufo/waves/round-33/wave1/ExecRegressionC1.md` §1/§2.1-2.2);
      round 34 hardened that same instrument to `records=41 bound=41 unbound=0` exit 0 (`bound=records`;
      erratum 1 `.ufo/waves/round-34/claims-erratum-1.md` supersedes the frozen `40` literal) and
      `selftest cases=23 failures=0` (`.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md` §Addendum)
      — instrument work, not a domain task. Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 34, measured 2026-10-26T06:03:13Z): the F17 entry
      `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` is the 46th
      `corpus/knowledge/*.md` entry and carries exactly one `recheck:` command; on the landed tree
      `python3 corpus/instruments/recheck-audit.py --quiet` prints `strict pass=46/46 cdroot_fail=0
      instrument_fail=0 own_fail=0`, but its expectation limb is open — `expect=present expected=45
      missing=0 unexpected=1 exit=1`, because `corpus/instruments/knowledge-expected.txt` (sha256
      `3f68b9a2…ab81ceb`) still lists 45 entries and no round-34 seat owns that sync. The new
      instruments' selftests all pass (receipts under `.ufo/waves/round-34/wave1/`):
      `r-defect-closure.sh --selftest` → `selftest cases=9 failures=0`, exit 0
      (`ExecRDefectClosureSuite.md` §4; plain run `closed=9/9 exit=0` §3, base tree `closed=0/9
      exit=1` §5); `capture-binding-check.py --selftest` → `selftest cases=23 failures=0`, exit 0
      (`ExecCaptureBindingHarden.md` §Commands); `kill-rule-check.py` → `mutants=3 killed=3
      survivors=0 invalid=0`, `survivors=0`, `exit=0` (`ExecKillRuleCheck.md` §3, with §9b
      disclosing one unpinned `parse_round` mutant shape); `frontier-recheck-count.py` →
      `entries=20 pass=20 exit=0` incl. `PASS F17
      knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051 exit=0`
      (`ExecHarnessAfter.md` §4). Round-33's `source-recheck.py` S049/S050 exits 0 stand
      (`round-33/wave1/ExecHarnessC2.md` §C2.[8]/[9]). Box stays `[~]` on the expectation limb.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 34, base `014ee2d7`): `PROVINCE.md` is untouched this round —
      `git diff --numstat 014ee2d7 -- PROVINCE.md` empty, 74 lines, sha256
      `b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679`. F17 sits inside this
      province (core paragraph "program rules, claim packages"; the F13/F14 severity-ladder
      precedent), so no re-scope is claimed; the append-only frontier amendment is **owed and not
      applied** — the appended list stops at F16 (`PROVINCE.md:74`), and
      `.ufo/waves/round-34/wave1/ScribeSkillGate.md` §4a proposes the exact 2-line/216 B append
      (append sha256 `33f769be3bc6038afd0961d0d20868fbf096f6430d322df07287875b46fafa47`) with a
      prefix-identical rehearsal. Sibling sweep: `.ufo/waves/round-34/wave1/ConnSibling.md` §1 rules
      "Contested scope: none" over seven tokens × 20 sibling corpora + `SKILL.md` + fleet root
      (corroborated by `ScoutSiblingSweep.md` §1-§2); the single `Immunefi` hit is kotoba's
      citation-routing mirror of kasegi's own `SKILL.md:130`, and kake's `PROVINCE.md:284-286`
      explicitly excludes "bounty and policy operation". Nothing absorbed; box stays `[~]`.

---

**L1 integration note (appended 2026-10-26, after the boxes above were drafted):** the L1
landed the two "owed and not applied" items the boxes name, both as end-of-file appends — the
`PROVINCE.md` F17 frontier amendment (now at `PROVINCE.md:75`, `sha256 33f769be…` prefixed
per the `ScribeSkillGate` rehearsal) and the `SKILL.md` round-34 re-verify correction
(`SKILL.md:1091`, pins `sha256sum` target `3d9e5e0d…`, 892 lines, `selftest cases=23`), so
box 1's "byte-unchanged" sentence describes the base-to-tip no-harm state before this append and
box 4's "owed" sentence is now applied. `corpus/instruments/knowledge-expected.txt` was synced
to 46 entries (F17), so `recheck-audit.py` prints `strict pass=46/46` and
`expect=present expected=46 missing=0 unexpected=0 exit=0`. Post-append no-harm re-measurement:
`density.py SKILL.md` mean **201.2** (base 201.7; the append is a factual correction, no score
move claimed), `anchorcheck.py SKILL.md` exit 0 with the same failure classes (0 bad). All four
boxes stay `[~]` with these pointers.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 35, base `3266c99`; integration commits `aa6ad99` / `0aee0ef`, tip `5a25337`):
      the Gates & probes registry home now carries the round-34 instruments' rows at
      `SKILL.md:1097` (`r-defect-closure.sh`) and `:1098` (`kill-rule-check.py`), each with name /
      gate|probe / entry command / verdict map / selftest spelling / pinned-value path / write
      scope / owner (spotcheck D3; receipt `.ufo/waves/round-35/wave1/ExecD3SkillRegistry.md`).
      `git diff --numstat 3266c99 -- SKILL.md` = `13 0` (end-of-file append only, 1104 lines,
      sha256 `daeff71b…`). No-harm receipt `.ufo/waves/round-35/wave1/ExecNoHarmFinal.md` §1–§2:
      the base limb `3266c99:SKILL.md` (`ba5ebe5d…`, 1091 lines, 25 blocks, 711 cites) still reads
      mean **201.2**, while the landed bytes read mean **220.9** (26 blocks, 742 cites — the one new
      high-density block); `anchorcheck.py SKILL.md` exits 0 with `LOST-RECORDED=306 PIN-BROKEN=0
      ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, `16 in-range cite instances, 0 bad`. The independent
      `RevNoHarm.md` §A–§C reproduces both limbs and the 0-deletion diff, and discloses one transient
      mid-write `BASE-ABSENT` read that is not reproducible on the pinned bytes. `SCORECARD.md` now
      carries two round-35 depth:density records: the integration stub at `:1269` still says “no-harm
      guard mean ≈ 201.2”, while the receipt-grounded section's guard row at `:1314` binds both
      figures — base `ba5ebe5d…` 201.2 / 25 blocks / 711 cites, landed `daeff71b…` 220.9 / 26 blocks
      / 742 cites — and discloses the stub cell as contradicted, the closing commit being the
      reconciliation point. Box stays `[~]`; no non-author has checked it.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 35): **no new end-to-end domain task ran this round.** `LOG.md` carries the
      committed round heading `## Round 35` at `:1651` (1659 lines), and it logs instruments and an
      admission, not a hunt-to-claim task; the wave spec has no domain-task seat. The KEV work is a
      measurement, not a domain hunt: `.ufo/waves/round-35/wave1/ExecC2Capture.md` §1–§6 captures one
      document (`status=200`, 1,479,694 bytes / 27,870 lines, sha256 `d69349e8…`, exit 0),
      `source-recheck.py --manifest …/round-35/manifest.json --source S052` prints Q1–Q5 each
      `occurrences=1` with `sha256 OK`, exit 0, and the CSV alternative is measured then discarded.
      The closest executed end-to-end work remains instrument closure: `r35-defect-closure.sh` plain
      run `closed=7/7 exit=0` and `--selftest` `cases=7 failures=0` (this seat, §Measurement state).
      Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 35, measured 2026-10-26T07:02Z): the F18 entry
      `corpus/knowledge/cisa-kev-catalog.md` (91 lines, sha256 `e9de994d…`) is the 47th
      `corpus/knowledge/*.md` entry, and `corpus/instruments/knowledge-expected.txt` is synced to it
      (49 lines, sha256 `d2e99ca6…`). `python3 corpus/instruments/recheck-audit.py` prints
      `strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0` and
      `expect=present expected=47 missing=0 unexpected=0 exit=0` (double run in
      `.ufo/waves/round-35/wave1/ExecExpectedListSync.md` §4; this seat's `--quiet` run exit 0). The
      new suite is executable end to end on the landed tree: `bash corpus/instruments/r35-
      defect-closure.sh` → `D1–D7 … open=0`, `closed=7/7 exit=0`, and `--selftest` →
      `selftest cases=7 failures=0`, exit 0 with seven `live=pass fixture=rejected` case lines and
      the forged-summary / forged-caselines / short-report / fake-suite / fake-plain judges all
      rejecting (this seat's post-fix runs; corpus receipts `ExecClosureSuite.md` §5–§6,
      `ExecSelftestFixtures.md` §3, `RevClosureSuite.md` §4). Box stays `[~]`.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 35, base `3266c99`): `PROVINCE.md` is unchanged at this seat's read — 75
      lines, sha256 `b4bb5fee…`, `git diff --numstat 3266c99 -- PROVINCE.md` empty; `RevNoHarm.md`
      §A records it as PASS (`git diff --stat … -- PROVINCE.md` empty, exit 0). F18 sits inside the
      province (core "program rules, claim packages"; the F13/F16/F17 severity-scope precedent).
      `ScoutSiblingSweep.md` and `ConnSibling-ruling-draft.md` rule **“F18 / S052 is uncontested by
      any sibling corpus; no report-to-lane item arises this round”** across 20 sibling lanes — the
      only CISA hits are kake's rejection record of the BOD 20-01 VDP template (VDP publication
      path, not exploitation-status prioritization) and shokuknow's doctrine row assigning
      `cisa.gov` to kasegi (affirmative ratification). The append-only F18 frontier amendment is
      **owed and not applied** at this read: `grep -c 'F18' PROVINCE.md` = 0 and the appended list
      stops at F17 (`PROVINCE.md:75`); its form is a one-line end-of-file append under R6. Box stays
      `[~]`.

**Round-35 measurement state (ScribeShonen, 2026-10-26T07:02Z; tip re-read at 07:06Z).** Live tree HEAD `5a25337` (integration `0aee0ef`, C1 integration `aa6ad99`), base `3266c993…`. Digests read at this seat's
measurement: `SKILL.md` `daeff71b…` (1104 lines), `SCORECARD.md` `ed6e931f…` (1404 lines, the blob
committed in `48e6053`; this seat's first pass read `085cffd6…` / 1282 lines and an intermediate
append read `5ea6f459…` / 1404 lines — the committed blob is the binding),
`corpus/QUALITY.md` `d4f83bb1…` (250 lines), `corpus/README.md` `277f04ce…` (396 lines),
`corpus/SOURCES.md` `0f95a132…` (112 lines), F18 entry `e9de994d…` (91 lines),
`knowledge-expected.txt` `d2e99ca6…` (49 lines), `r35-defect-closure.sh` `0ae4b484…` (834 lines),
`PROVINCE.md` `b4bb5fee…` (75 lines). An intervening run at ~06:58Z read `closed=6/7 exit=1`: the
round-35 SCORECARD append had reintroduced the `filled by the L1` placeholder at `:1271` (D1 class);
commit `8ce6fb4` reworded that sentence, and the plain and `--selftest` runs after it are 7/7 and
`cases=7 failures=0` (exit 0). All four boxes stay `[~]`: a wave seat is the lane and cannot write
a checked box; promotion needs a named non-author verifier.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 36): Gates & probes registry now registers `r35-defect-closure.sh` and `r36-closure.sh` by exact basename (E3); `anchorcheck.py SKILL.md` exit 0; suite `r36-closure.sh --selftest` cases=9 failures=0 at the final head. Box stays `[~]`; no non-author check.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 36): no new end-to-end domain hunt ran; closest executed measurement: F19 EPSS live capture + source-recheck S053 + the r36 closure suite (C1/C2). Box stays `[~]`.
- [~] Instructions executable by an agent without oral context
      — evidence (round 36): `recheck-audit.py` strict pass=48/48 expected=48 exit=0; frontier harness entries=22 pass=22 exit=0 incl. PASS F19 ids=S053; r36 suite `--export-ref <final>` closed=9/9 exit=0; census exit 0. Box stays `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 36): PROVINCE.md amended with F18 (round 35 admission, previously owed) and F19; sibling sweep over 20 lanes finds no EPSS ground (ConnSibling ruling); S053/F19 uncontested. Box stays `[~]`.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 37, final lane head aa88877bf921d952137817b91ca76234b206da65): the Gates & probes registry now carries the r37-closure.sh row plus the D5-corrected single-choice r36-closure.sh row (E13); `anchorcheck.py SKILL.md` exit 0; density/anchor post-append re-measurement (density mean 225.3→post-append re-measurement in RevNoHarm; anchorcheck exit 0). Box stays `[~]`; no non-author check.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 37): no new end-to-end domain hunt ran; closest executed measurement: C1 suite + C2 SSVC capture/harness. Box stays `[~]`.
- [~] Instructions executable by an agent without oral context
      — evidence (round 37): `recheck-audit.py` strict pass=49/49 expected=49 exit=0; frontier harness entries=23 pass=23 exit=0 incl. PASS F20 ids=S054; source-recheck S054 exit 0; capture-binding records=44 bound=44; census exit 0; r37 suite `--selftest` cases=14 failures=0 and `--export-ref aa88877bf921d952137817b91ca76234b206da65` closed=14/14 exit=0 (raw transcript committed at .ufo/waves/round-37/final-gates/all-gates.txt). Box stays `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 37): PROVINCE.md F20 amendment appended; F20/S054 uncontested across 20 sibling lanes (ConnSibling/ScoutF20Sibling ruling); junk twin rejected. Box stays `[~]`.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 38): the Gates & probes registry gains the `r38-closure.sh` row (single-choice type `gate`, verdict map incl. exit 2) appended at EOF; every base line byte-identical; `anchorcheck.py SKILL.md` exit 0. Box stays `[~]`; no non-author check.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 38): no end-to-end domain task ran this round; the closest executed work is the F21 capture + harness run and the r38 suite run. Box stays `[~]`.
- [~] Instructions executable by an agent without oral context
      — evidence (round 38): `frontier-recheck-count.py` entries=24 pass=24 exit=0 incl. PASS F21 ids=S055; `source-recheck --source S055` exit 0; `capture-binding-check.py` records=45 bound=45; `recheck-audit.py --quiet` expected=50 unexpected=0 exit=0; census exit 0; r38 suite run + selftest over the judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt (raw transcript committed there). Box stays `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 38): PROVINCE.md carries a `Correction (round 38)` line marking the round-37 scaffolding L81-L152 as not part of the province (D-A), then the F21 amendment; CSAF/VEX ground uncontested across 20 sibling lanes, kake's security.txt `CSAF` extension mention ruled adjacent (`wave1/ConnSibling.md`). Box stays `[~]`.


Correction (round 39): box 3's round-38 evidence line ("r38 suite run + selftest over the judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt (raw transcript committed there)") overstates what that transcript carries. The receipt's `export-ref` is the judged head J = `66703acaaff50529a35be49aa8759d04140720ad`, and its run over J is `export-ref-run: closed=7/8 exit=1` (G2 `receipt=0`); the committed `closed=8/8 exit=0` and `selftest cases=8 failures=0` are over `run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e`. Read the line as: run + selftest committed over the receipt's run-ref, with the run over J red on G2 alone. Box 3 stays `[~]` (non-author verifier `corpus/lessons/round-38-verifier-spotcheck.md` §5 R2).


- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 39): Gates & probes registry gains the `r39-closure.sh` row (single-choice gate, verdict map incl. exit 2) appended at EOF; every base line byte-identical; `anchorcheck.py SKILL.md` exit 0; suite `--selftest` graded cases=8 failures=0 at the verification ref. Box stays `[~]`; no non-author check.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 39): no end-to-end domain hunt ran; the closest executed work is the F22 capture + harness run and the r39 suite run. Box stays `[~]`.
- [~] Instructions executable by an agent without oral context
      — evidence (round 39): `frontier-recheck-count.py` entries=25 pass=25 exit=0 incl. PASS F22 ids=S057; `source-recheck --source S057` exit 0; `capture-binding-check.py` records=46 bound=46; `recheck-audit.py --quiet` expected=51 missing=0 unexpected=0 exit=0; census exit 0; r39 suite run + graded selftest at the verification ref Y (all-gates.txt). Box stays `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 39): PROVINCE.md carries the `[r39 Frontier amendment]` F22 line; F22/S057 uncontested across 20 sibling lanes + shokuknow (ScoutSiblingF22 ruling); junk twin rejected. Box stays `[~]`.

Round-39 measured state: judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt (claims-erratum-1.md E4).
Correction (round 39): the round-39 suite's recorded 8/8 receipt is not independently reproducible as committed proof: G2 accepts mutated payload values and G6 depends on scratch-root state (`wave2/CritG2Exploit.md`, `wave2/CritC1Kill.md`). Its green isolated-clone/selftest evidence is reported with those limits; box 3 remains `[~]`, not independently verified.

## BLOCK SHONEN.md

Correction (round 40): the round-39 box 3 evidence line ("suite `--selftest` graded cases=8 failures=0 at the verification ref") is contradicted by the committed receipt at Y `8371e7ac9f32cae5ed72f8c28205634603f836fa`, which records `closed=7/8 exit=1` and `selftest failures=1` (`selftest cases=8 failures=1`, `selftest-exit=1`, `G2 positive=fail`; all-gates v5, sha256 8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471).
Correction (round 40): read the line as: the suite ran, seven of eight checks close, and the graded selftest carries one failing case; the 8/8 exists only in the discarded attempt-1 receipt at `5006097a` (`run-utc=2026-10-26T21:35:00Z`, after its containing commit), and the two green limbs are not independent — G2 accepts forged payload values (mut-f/g/h/j/k, `wave2/CritG2Exploit.md`), G6 depends on a scratch root the seats populate (`wave2/CritC1Kill.md`) — so box 3 stays `[~]`, not independently verified. Verifier R2's ask, quoted: "Append `Correction (round 40)` lines naming the final receipt values in each record."

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 40): Gates & probes registry row `r40-closure.sh` appended; density instrument byte-identical to base (H10 payload `density=1`); no density move claimed; `anchorcheck.py SKILL.md` exit 0. Box stays `[~]`; no non-author check.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 40): no live domain hunt ran (refused); closest executed work: the claim-package exemplar built from a public disclosed report (considerthese 2026-10-26 proposal 2) and the C1 suite run. Box stays `[~]`.
- [~] Instructions executable by an agent without oral context
      — evidence (round 40): r40-closure.sh suite at Y `closed=10/10 exit=0` and graded `--selftest cases=10 failures=0`; harness `entries=26 pass=26 exit=0`; binding `records=54 bound=54`; census exit 0; audit `expected=59 unexpected=0 exit=0`. Box stays `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 40): PROVINCE.md carries the `[r40 Frontier amendment]` F23 line; sibling sweep found no F23 ground (ScoutSiblingFinal/ConnPatterns); junk twin rejected. Box stays `[~]`.

Correction (round 40): the final round-40 receipt values are recorded in `.ufo/waves/round-40/final-gates/all-gates.txt` at Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5`: `closed=10/10 exit=0`, graded `selftest cases=10 failures=0`, suite sha256 `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`, `time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`. Box 3 stays `[~]` — no non-author verifier this round.

Correction (round 41): box 3's evidence line ("r40-closure.sh suite at Y `closed=10/10 exit=0` and graded `--selftest cases=10 failures=0`") grades round-40 C1 verified when it is not verified on the frozen counter (NOT verified): `wave2/RevC1Counters.defeats.txt` T2/T4/T7/T13/T14, `wave2/CritKillRule.md`'s eight committed escape states F1–F8 (`wave2/CritKillRule.h6-escapes.sh`) and `wave2/MutH6H10.md` D2 (leaf-capped green base) each show a check passing while its defect is present.
Correction (round 41): read the line as: the receipt committed at Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5` (`.ufo/waves/round-40/final-gates/all-gates.txt`, sha256 7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b) records `closed=10/10 exit=0` with H1–H10 all `closed=1` over `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd` (`time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`), and a green suite run is not claim admission when the frozen kill rule fires; box 3 stays `[~]`, not independently verified.
Correction (round 41): the `--selftest cases=10 failures=0` half, also quoted by the round-40 correction above, carries no committed transcript (round-40 verifier D2) — the Y receipt holds no `selftest` line and the only graded tally is over scratch Y′ (`wave2/RevC1Counters.md` R7, report-only); the round-41 receipt tees the selftest transcript beside the run transcript (I2), so this class cannot recur.

## Round 41 evidence

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — evidence: r40/r41 closure rows appended in a contiguous registry block and density.py unchanged; C1 suite's I7 row check passes, but no non-author final green closure.
- [~] At least one end-to-end domain task executed and logged in LOG.md — evidence: no live target-domain hunt ran; the round curated RFC 9116 as format knowledge, not an authorized domain task. Box remains `[~]`.
- [~] Instructions executable by an agent without oral context — evidence: C2 source-recheck/frontier/binding/audit/census counters pass; C1 final receipt run is `closed=10/12 exit=1` and graded selftest has 6 failures, so the round does not verify the closure suite. Box remains `[~]`.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — evidence: F24 was appended, but wave 2 found shared RFC 9116 fields/scope/expiry/non-authorization material in kake's existing `security-txt-publishing.md`; L0 scope ruling requested, no coverage credit claimed. Box remains `[~]`.

## Round 42 evidence

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 42, base `5053a7f46de35784cff4b56756906e9014a38276`; lane docs byte-unchanged
      base → claims freeze `0566bd66e93d429b2df8b6751cf10cbdc391e79b`): `SKILL.md` 1129 lines, sha256
      `f8e7a5d3be74699329162635b26731e0ce156483dc17bd29a3323eef15413e00`; `density.py SKILL.md` mean
      **237.1** over 29 blocks, 780 path-citation instances, exit 0; `anchorcheck.py SKILL.md`
      `16 in-range cite instances, 0 bad; 16 distinct anchors` plus
      `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0. The round's
      registry move is the `r42-closure.sh` row appended in one well-formed Gates & probes block,
      with the D-r41-3 residue repaired (the round-40 block whose header/separator/row are split by
      a blank line, and the duplicated `r40-closure.sh` row): the repair, the post-append density
      re-measurement and the `anchorcheck` re-run are measured at the round's judged head: J3 `tables=18,rows=73,r42-rows=1,r40-rows=1,r40-split=0,bare=0,lead=0`; `density.py SKILL.md` mean **234.2** over 30 blocks (1134 lines, 782 path-citation instances); `anchorcheck.py SKILL.md` `16 in-range cite instances, 0 bad` (J3 /
      F-TABLE; `density.py` byte-identical to base sha256
      `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` under J12). Box stays
      `[~]`; no non-author check.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 42): **no end-to-end domain hunt ran this round.** The wave-1 dispatch is 64
      build seats — executor 19, scout 11, critic 8, reviewer 8, scribe 7, mutation-tester 5,
      connector 2, sentinel 2, simplifier 1, revenger 1 (`.ufo/waves/round-42/wave1-dispatch.json`,
      64 members) — and none is a hunt-to-claim seat; `grep -c '^## Round 42' LOG.md` = 0 at the
      claims freeze (1750 lines). The closest executed work is measurement, not a domain hunt: the
      F25 lead screen, the S064 capture with its `source-recheck` quote checks and harness
      admission, and the C1 suite run itself. Box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 42, base `5053a7f46de35784cff4b56756906e9014a38276`): the counters run from
      committed bytes with no oral context. Base controls (measured): the
      `.ufo/waves/round-42/c1-controls/do-nothing.txt` control records the r42 suite absent at base —
      `bash corpus/instruments/r42-closure.sh` exits 127 there and cannot print `closed=13/13` — and
      the r41 suite at `closed=8/12 exit=1` with `selftest cases=12 failures=8`;
      `.ufo/waves/round-42/c2-controls/before.txt` records frontier 24, registry 63, knowledge 60,
      `entries=27 pass=27`, `records=55 bound=55 unbound=0`, `expected=60`. After-state at Y: `bash corpus/instruments/r42-closure.sh --export-ref <Y>` → `closed=13/13 exit=0`;
      `--selftest --export-ref <Y>` → `selftest cases=13 failures=0` with thirteen graded
      `selftest case=J<n> … positive=pass … verdict=pass` lines; a plain run refuses exit 2; the base
      `5053a7f4…` and round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` exports print
      `closed<13/13 exit=1`; an unresolvable `--export-ref` prints its distinct ref-not-found red;
      the receipt `.ufo/waves/round-42/final-gates/all-gates.txt` tees both transcripts. C2 at Y: frontier 25, registry 64+R, knowledge 61, `entries=28 pass=28` incl. `PASS F25`,
      `records=56 bound=56 unbound=0`, `expected=61`, census exit 0, measure 45/45 = 1.000. Box stays
      `[~]`; no non-author check.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 42, base `5053a7f46de35784cff4b56756906e9014a38276`): `PROVINCE.md` is 163
      lines, sha256 `5b88bc43a5a5c64ec7710882c7af1268ef8de94f4b360492ab989e9e21e2ea9a`, unchanged
      base → claims freeze; the round's only province move is one `[r42 Frontier amendment]` F25
      line appended at end of file, present at the judged head. F25's topic is a
      machine-readable vulnerability-data standard (the lead class the freeze names: the OSV schema
      or the CVE Record Format) — the data-standard layer under the claim-package and triage
      province that F18/F19/F20/F21/F23 already sit in — and the scout's no-overlap check against
      existing lane rows and entries is recorded in `wave1/ScoutC2Screen.md`. F24 (RFC 9116) stays PARKED: the round-41 L0
      scope question on shared security.txt ground with kake is unanswered at freeze time, so it is
      neither re-mined nor referenced as a candidate. Sibling scan recorded in `wave1/ScoutC2Screen.md` (no sibling lane holds the CVE Record Format). Box stays `[~]`.

