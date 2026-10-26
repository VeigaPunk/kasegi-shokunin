# L1 integration verification — kasegi round 34 (KasegiR34a2)

This is the L1's own re-run of the frozen counters on the integrated bytes,
captured at `2026-10-26` (UTC) after all production edits and before the round
commit. Raw full output (including `anchorcheck.py` per-cite listing) is in
`L1Integration.raw` in this directory; the summary lines are reproduced below.

| Frozen counter | Output at integrated tree | Exit |
|---|---|---|
| `bash corpus/instruments/r-defect-closure.sh` | `closed=9/9 exit=0` | 0 |
| `bash corpus/instruments/r-defect-closure.sh --selftest` | `selftest cases=9 failures=0` | 0 |
| `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=23 failures=0` | 0 |
| `python3 corpus/instruments/capture-binding-check.py` | `records=41 bound=41 unbound=0` (erratum 1 reading) | 0 |
| `python3 corpus/instruments/kill-rule-check.py` | `mutants=3 killed=3 survivors=0 invalid=0`; `gates=7 failed=0`; `survivors=0` | 0 |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` | 0 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` | 0 |
| `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `1` | 0 |
| `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `1` | 0 |
| `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` incl. `PASS F17 ... ids=S051` | 0 |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | 18 assertions OK, Q9/Q17 `occurrences=2` anchored (77-ok/96-ok), `sha256 OK` | 0 |
| `grep -c '<LANE_HASH>' SCORECARD.md` | `0` (grep exit 1) | 1 |
| `python3 corpus/instruments/recheck-audit.py` | `strict pass=46/46 cdroot_fail=0 instrument_fail=0 own_fail=0`; `expect=present expected=46 missing=0 unexpected=0 exit=0` | 0 |
| `python3 corpus/instruments/density.py SKILL.md --label r34` | mean dens **201.2** (base 014ee2d: 201.7; the 1-line EOF correction is a factual re-verify update, no score move claimed) | 0 |
| `python3 corpus/instruments/anchorcheck.py SKILL.md` | 12 in-range, 0 bad, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `ORIGIN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0` | 0 |
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | W04 S028/S029 only, `kasegi ok .../corpus/SOURCES.md` | 0 |
| Do-nothing control C1 (`c1-controls/fake-suite.sh`) | prints `closed=9/9 exit=0`; rejected by the suite judge (`selftest judge=forged-summary rejected=1`), fake kill rule `CTL-fake-killrule` rejected (`opaque`, `differs=1`) | — |
| Do-nothing control C2 (`c2-controls/junk-checker.py` + `junk-f17.md`) | shape counters pass `3/3` by design; fabricated sentence at `junk-f17.md:15` fails `source-recheck` against the capture (`MISMATCH reason=quote-not-found`, exit 1) | — |

Notes:
- The round-33 summary `ExecRegressionC1` filed its receipt, committed in `c1c6a5f`
  (round-34 closure); the regression battery is covered by that receipt plus this L1
  re-run and `wave1/ExecRDefectClosureSuite.md` §5 (base `closed=0/9`, exit 1).

- Correction (round 35): the bullet above was corrected in place — the dead-seat claim
  was false; the `ExecRegressionC1` receipt is committed in `c1c6a5f` (round-34 closure).
- The junk-twin rejection limb is recorded with its dispute (`wave1/RevJunkTwin.md` holds;
  `wave1/CritOverclaim.md` F1/F1b, `wave1/CritC2Kill.md` G5, `wave1/ScoutDatawalk.md`
  F-1/F-1b dispute the as-frozen phrasing); the executable fact the round lands is that the
  fabricated **sentence** is rejected against the committed capture by three independent runs
  (`ExecDoNothingReject.md` §3, `RevJunkTwin.md` §3, `RevC2BeforeAfter.md` §8).
