# Round 72 — lesson (kasegi, attempt 1)

Round: kasegi r72 attempt 1. Frozen claims `.ufo/waves/round-72/claims.json` (freeze `a34ce4c`). Attack wave `w1` (11 seats, one v1 wave, band 8–16). Report `.ufo/reports/round-72/kasegi.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M72-1 | unmeasured narrowing: a round-71 repair turned a deny-everywhere default for write roots into deny-where-listed, and the frozen round-71 predicate measured only the enumerated rows, so the population-wide guarantee was never a predicate row | `.ufo/waves/round-72/controls/c1-census-donothing-r72.txt` (19 `READMITTED-ROW` lines, `READMITTED=19`, base gate `182f4ef7…`); `.ufo/waves/round-71/w2/SentinelC1.md` §4 R1 and row 23 (22,012 files written under `--work`) | `corpus/instruments/derive-head-census.py` (round 72, C1): the census reads every instrument's `add_argument` literals against the gate's tables | Round 72 denies `--work` and `--scratch` globally (`corpus/instruments/figure-audit.py`, `PY_DENIED_ANY`) and pins four cases (`python-work-global-refused` and three siblings) | red: base `READMITTED=19`, measured; green: candidate `READMITTED=0` (`.ufo/waves/round-72/controls/`, `K72ExecSweep`); the candidate is also refused on the round-71 row-22/23 derives (`K72ExecProbe`) |
| M72-2 | identity by spelling: the policy key was the basename of the argv spelling while containment used the realpath of the same token, so one token could name two files | base `corpus/instruments/figure-audit.py:493` (`script = os.path.basename(parts[1]…)`) against `:501-505` (realpath containment); `.ufo/waves/round-71/w2/SentinelC1.md` §3 rows 28-29 (`out/alias.json`, 2,595 B, written through `ok.py`→`gate-quote-audit.py`) | none at round 71 | Round 72 keys the policy on `os.path.basename(os.path.realpath(…))` (`python_head_ok`) | red: census `ALIAS-PROBE verdict=admitted rc=1` on base; `K72ExecSweep` alias row admitted on base (rc=1) and refused on candidate (rc=2); green: `ALIAS-PROBE verdict=refused rc=2` |
| M72-3 | count quoted without its predicate: "23 censused heads" (sentinel) and "43 / 26" (spot-check) and "19" (census) are three different sets, and the round-71 report and lesson reused one phrase for them | `.ufo/waves/round-71/controls/` spot-check `corpus/lessons/round-71-verifier-spotcheck.md:38-39` (K71-A), `:77-80` (43 / 26); `SentinelC1.md:108` (23); the census receipt `:27` (19 heads, 19 pairs: 15 `--work`, 4 `--scratch`) | none (no round-71 row or criterion measures a harm count with its predicate) | This lesson states each count with its predicate. The correction to the round-71 harm note is routed (R-4 below). | a count without a predicate cannot be re-derived; each figure here names its command or receipt |
| M72-4 | a positive row whose direct command exits nonzero is reported as "stale" and passes: the counter's negative branch is the passing branch | round-71 spot-check `:66-68` (the `direct_rc != 0 → stale` branch of `.ufo/waves/round-71/controls/c1-probe-run-r71.py`), `:71-73` (R8 compares `"" == ""`) | none | Not fixed in round 72 (K71-C, residual 6). The counter is frozen; the change needs its own freeze next round. | red: spot-check R5–R8 exit 1 yet pass (read from bytes, not re-run this round) |
| M72-5 | a frozen target clause written before its source was opened: C2's target named an `api_key` requirement, and the freeze (`a34ce4c`) preceded the S107 capture (2026-11-05T03:49:50Z). The clause is absent from the page (zero `api_key` / `API key` / `authentication` lines in `corpus/source-snapshots/round-72/S107.txt`) | `.ufo/waves/round-72/claims.json` (C2 `target`, freeze `a34ce4c`); `K72AttackF50` §4 (grep evidence), §5 verdict `C2 attack: FALSIFIED on frozen wording` | none: the claims rules require counters to be re-derivable, not that each named element be checked against a source before freezing | The C2 entry records the absence as a measured limit (`corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` Limits) and does not invent an api_key sentence. The frozen target is NOT rewritten after a seat has scored it; the report states the falsified clause for the operator. Next round: a source row is opened before the claim that names its content is frozen (CORPUS.md rule 1). | red: `K72AttackF50` grep (`api_key|API key|authentication` → no sentence); green: the entry's Limits section names the absence; the counters are unchanged by the entry |

Process note (not a mistake class): the first probe expectations in `K72ExecProbe` were set from the round-71 "intended fix" column rather than the measured base, so three rows (20, 21, 29) were recorded as DIFFERENT when the base already admitted them. The seat reported the base rc, and no regression follows.

## Gate

- URL: https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html
- Access date: 2026-11-05 (`corpus/source-snapshots/round-72/manifest.json`, `fetched_utc` 2026-11-05T03:49:50Z, HTTP 200).
- Capture: `corpus/source-snapshots/round-72/S107.txt`, sha256 `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652`, 1176 lines.
- Located quote (capture line 33, 13 words):
  "The REST API for creating, changing, and getting the details of bugs."
- Every quoted fragment in `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` was checked against the capture by substring (30 fragments, all located; the one measured-absence word was reworded so no unlocated quote remains). The 17 pinned quotes pass `source-recheck.py` with `anchor=…-ok`.

## Routed defects

Each item names the evidence and the next owner. None is closed by round 72.

- **R-1 · `--json` and `--root` are outside the census's write-class set.** `derive-head-census.py` counts only `("--out","--output","--work","--scratch","--url")`. The candidate denies `--json` for seven heads and `--root` for four, per script. `K72AttackCensus` §3: 8 heads declare `--json`; seven are denied and `claim-package-check.py` is admitted as the intended stdout flag. The frozen set does not change this round. Owner: next round.
- **R-2 · `freeze-check.py` runs `bash -c` on the claims file's `counter_cmd`.** Sentinel row 33 (marker `pwned-from-claims`). The candidate's `PY_HEAD_REFUSED` lists only `frontier-recheck-count.py`. Round 72 excludes it (`claims.json` non-claims). `K72ExecProbe` row 33: ADMITTED on both gates, shell marker executed. Owner: next round, with its own census row.
- **R-3 · `sort -T` / `--temporary-directory` create and unlink files outside the root.** Sentinel rows 14, 15, 18. `K72ExecProbe` rows 14, 15, 18: admitted on both gates. `sort` is not a census head, so no row covers it. Owner: next round.
- **R-4 · the round-71 harm note.** The spot-check asks for a correction to M71-4 and the SCORECARD harm note. Correct figures by predicate: 19 heads re-admitting a write-class flag (census, round 72); 23 heads re-admitting any base-denied name including `--root` (sentinel); 43 / 26 (spot-check, ast over the r71 tables). The correction is appended to the round-71 SCORECARD move-log row in this round's SCORECARD section; the round-71 spot-check file is not edited.
- **R-5 · a realpath-resolved alias to a census head is admitted under a non-census name.** `K72ExecProbe` row 10: `censusf.py → capture-source.py`: base rc=2, candidate rc=1. The flags are still policed against the true head (row 28 refused), so the new admission reads a census head under its real name. It is a documented consequence of the realpath key, not a bypass, and no frozen predicate pins it. Owner: next round decides whether a census row must name realpath semantics.
- **R-6 · a regular file named like a fixture head is keyed by name.** `PY_SELFTEST_FIXTURE_HEADS` (`ok.py`, …) admits by basename, and a regular file of that name inside `corpus/instruments/` gets `PY_DENIED_ANY` only. The realpath fix covers symlinks, not regular files. `K72ExecSweep` measured the symlink case only. Inference for the regular-file case, not measured. Owner: next round.
- **R-7 · `capture-binding-check.py --root .` is admitted on base and candidate.** `K72ExecProbe` row 20 (not refused). The round-71 probe expected it refused; the base never refused it. Unchanged by round 72; recorded so the census's `--root` coverage is not overstated.

## Residuals

1. `freeze-check.py` `bash -c` exec (R-2): outside the frozen claims; needs its own gate change and census row.
2. `sort -T` temp-directory writes (R-3): no census row for `sort`.
3. `--json` and `--root` outside `WRITE_CLASS` (R-1): changing the frozen write-class set is a next-round decision.
4. Regular file named as a fixture head (R-6): measured only in inference.
5. Per-script default-allow for `--json`, `--root`, `--url` (K71-B): inverting to a global deny-minus-allowlist is a larger repair than round 72's claims.
6. A positive row whose direct command exits nonzero reads as "stale" (K71-C, M72-4): `c1-probe-run-r71.py` is frozen and unchanged.
7. Probe-doc drift in `c1-probe-run-r71.py` (K71-F): docstring-only.
8. Missing erratum for the base prefix `39cde8a…` (K71-D): an L1 filing action.
9. Wave role split against the template (K71-E): round 72's wave has 11 items, roles executor×3, mutation-tester, reviewer×2, critic, scout, scribe×2, connector; the L1 holds the planner seat.
10. Driver relaunch with a live prior process (K71-G): operator or driver work.
11. Harm-count predicates (R-4, M72-3): corrected by predicate, not by replacing the round-71 record.
12. Argparse abbreviations and dash-spelling: measured for `--wor`, `--js`, `--o`, `--ou`, `--ro` (`K72AttackCensus` §4); the one admitted abbreviation resolves to `--root` on a head that does not deny it.
13. Stdin inheritance and absolute-path reads (sentinel residual 6): read confinement is outside C1.
14. `-- --selftest` admission (sentinel residual 2; V71-9/V71-10): outside the frozen set.
15. Unpinned PATH and argv[0] resolution (sentinel residual 9): host-boundary statement, unmeasured.
16. Green values for C1 and C2: pinned in the report, measured on the final bytes.
17. The api_key clause of C2's frozen target (M72-5): the operator rules; the entry does not supply it from another source. A second source would be a new claim, not a repair of this one.

## Registry changes (old → new)

- S107 (Bugzilla REST API core v1 bug endpoints): **none → mined**. Opened 2026-11-05; recheck **none → 90d**; used-by **none → corpus/knowledge/bugzilla-rest-api-bug-endpoints.md**. No row was rejected or superseded this round.
- Census before → after: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 before (`kasegi ok`), exit 0 after (`kasegi ok`); W04 duplicate-URL warnings are inherited, unchanged by this round.

## Sourced claim

C2 rests on S107 (opened this round): the entry `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` cites S107 for every routed claim; the registry row is S107 with `used-by` set to that entry.

## Assimilation and considerthese

Assimilation: none (`merge/kasegi/` was not used this round; the census of the staged package is routed to a later round). `considerthese/` was read by `K72Connector` (section 4): no unimplemented Bugzilla or bug-report proposal is pending, so no proposal was taken.
