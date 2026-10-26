# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 33, integration commit `9f98488` over base `690b69da`; `SKILL.md` sha256
      `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`, 1090 lines, appended
      only: `git diff --numstat 690b69da -- SKILL.md` = `19	0`): `density.py SKILL.md`
      prints mean dens 201.7 over 25 blocks and 710 path-citation instances, `density_exit=0`,
      against the base re-measured on the same bytes at 191.5 / 24 blocks / 689 citations;
      `anchorcheck.py SKILL.md` prints `12 in-range cite instances, 0 bad`, `LOST-RECORDED=306`,
      `PIN-BROKEN=0`, `anchor_exit=0` (`.ufo/waves/round-33/wave1/ExecRegressionC1.md` §2.8/§2.9,
      raws `anchor.txt`/`density-final.txt`); the round-33 SKILL row carries the instrument gate.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 33): `LOG.md` newest entry is `## Round 32` at `:1593`, appended in the
      freeze commit `6e55c8d` by the L1 (routed defect D1), and it records an honest stop, not a
      task; `## Round 31` (`:1584`) is the last end-to-end entry and no `## Round 33` heading
      exists (`grep -c '^## Round 33' LOG.md` = 0; `git diff --numstat 690b69da 9f98488 -- LOG.md` = `4	0`; 1595 lines).
      Round 33's end-to-end measurement is executed but unlogged: `capture-binding-check.py`
      prints `records=40 bound=40 unbound=0` exit 0 twice, `selftest cases=11 failures=0` exit 0
      (`.ufo/waves/round-33/wave1/ExecRegressionC1.md` §1/§2.1-2.2); the box stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 33, integration commit `9f98488` over base `690b69da`): each of the 45
      `corpus/knowledge/*.md` entries carries one `recheck:` command; `recheck-audit.py --quiet`
      prints `strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0` and
      `expect=present expected=45 missing=0 unexpected=0`, `recheck_exit=0`, over
      `knowledge-expected.txt` sha256 `3f68b9a2…ab81ceb` (44 → 45 entries)
      (`.ufo/waves/round-33/wave1/ExecRegressionC1.md` §2.5; `ExecExpectedList.md` §3);
      `frontier-recheck-count.py` prints `PASS F16 … ids=S049,S050` and
      `entries=19 pass=19 exit=0` (`ExecHarnessC2.md` §C2.[7]); `source-recheck.py` exits 0
      on the round-32 manifest for S049 (`sha256 OK`, `Q1`-`Q8` `OK occurrences=1`) and S050
      (`sha256 OK`, `Q1`-`Q6`), `recheck49_exit=0 recheck50_exit=0` (`ExecHarnessC2.md` §C2.[8]/[9]).

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 33, integration commit `9f98488`): `PROVINCE.md` gained only the end-of-file
      F16 amendment — `git diff --numstat 690b69da -- PROVINCE.md` = `2	0`, `grep -c '^-[^-]'` = 0,
      74 lines, sha256 `b57de5d9…abd679` (`.ufo/waves/round-33/wave1/ScribeProvince.md` §5) — and F16 sits
      inside this province: the round-33 six-lane sweep found zero hits for CNVD, 360SRC, 众测,
      `zc.cnvd.org.cn`, `security.360.cn`, `crowdsourced` (`wave1/ConnSibling.md` §1/Findings), which
      records `kake-shokunin/corpus/README.md:464-465` refusing vulnerability handling; nothing absorbed.
