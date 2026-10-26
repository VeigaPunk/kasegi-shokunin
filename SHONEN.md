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
