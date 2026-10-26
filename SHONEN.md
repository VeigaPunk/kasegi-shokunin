# kasegi-shokunin — Promotion checklist

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
