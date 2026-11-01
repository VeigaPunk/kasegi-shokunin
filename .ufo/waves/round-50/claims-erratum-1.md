# Round-50 claims erratum 1 — the round-50 freeze is superseded (2026-11-01)

Freeze of record moves from `.ufo/waves/round-50/claims.json` (commit `a2de23b025d8f1600c6a4387f22794dfc5ba2b88`,
base `c5e36360f5226c97d28f1937961b15c90e58827f`) to `.ufo/waves/round-50/claims.v2.json`. The original
claims.json stays byte-identical in history; this erratum is the correction of record (R9: append, do not
rewrite filed assertions). Three defects force the supersession; the first is disqualifying on its own.

## D1 — the frozen C2 surface is already admitted: F31=EPSS duplicates F19

The frozen C2 sentence admits "frontier row F31 — EPSS exploit-prediction scoring (probability of
exploitation in the wild ...)" with used-by `corpus/knowledge/epss-exploit-prediction-sco...` — the same
entry file the lane already admitted. The lane's own province already holds this surface:

- `PROVINCE.md` line 78 (r36 amendment): "F19 — FIRST Exploit Prediction Scoring System (EPSS)
  (exploitation-likelihood scoring, 0–1 probability) — admitted round 36; entry
  `corpus/knowledge/epss-exploit-prediction-scoring.md` (source S053)".
- The entry exists and is the F19 row's entry: `corpus/knowledge/epss-exploit-prediction-scoring.md`
  (`ground: F19`, source S053, capture `corpus/source-snapshots/round-36/S053.txt`).
- The frozen sentence names its distinctions against F01/F05/F13/F18 and never against F19 — the one row it
  collides with. The frontier counter's own duplicate guards (DUPLICATE-ENTRY on shared entry realpath;
  rule G) would fire once the second F31=EPSS row and entry landed: two admitted rows cannot own one entry.
- The committed wave-1 spec itself asks a reviewer seat "does a kasegi F31 (EPSS exploit-prediction
  scoring) duplicate ..." — the duplication question was scheduled for AFTER the freeze (a pre-freeze
  satisfiability defect, the round-34 class).

Landing C2 as frozen would be a fabricated new admission. C2 is superseded by C2' (OSV affected-range
events, F31), which is a genuinely new surface reached by re-opening the round-42 S065 screen under its own
recorded flip condition.

## D2 — the frozen predicates are unsatisfiable on the host that committed them

Every frozen counter command in claims.json names `python3` and the root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. This host (Windows workspace, round-50 session) has no
`/home/vgpnk` (`ls /home/` → No such file or directory) and its `python3` is the Microsoft Store alias stub
("Python was not found"); the working interpreter is `python` (3.13.15). All 67 committed entry recheck
lines share the same two host bindings (`grep -h "^recheck:" corpus/knowledge/*.md | grep -c "cd /home/vgpnk"`
= 67), so the frozen C2 expect_after — `entries=34 pass=34 exit=0` — is unreachable here regardless of any
lane work, and even C1's counter command names the dead root. The claims contract adapts, not re-hosts: the
superseding claims carry host-portable commands (`python`, lane-root argument or repo-root cwd) and
predicates measured on THIS host, with the inherited-failure taxonomy disclosed in the claim itself.

## D3 — the committed do-nothing control for C2 was not produced by a run on this host

`.ufo/waves/round-50/controls/do-nothing-c2.txt` prints `FRONTIER-CENSUS rows=30 admitted=30 closed=30
problem-rows=0 registry=79`, thirty `FRONTIER-PASS` rows and `entries=33 pass=33 exit=0` for a base export
at `/fast/scratch/hyaku/kasegi-r50/base-export`. No run on this host can print that: the 30 base rows'
recheck lines `cd /home/vgpnk/...` (absent), so the counter here reads every inherited row
`recheck-exit-1` — the actual base-export run on this host (committed as
`controls/do-nothing-c2-winhost.txt`) prints `rows=30 admitted=30 closed=0 problem-rows=30 registry=79`,
`entries=33 pass=0 exit=1`, zero `F31` lines. The file sits beside a control that clearly WAS produced here
(`do-nothing-c1.txt` carries a Windows CPython error string for a `/fast/...` path). do-nothing-c2.txt is
therefore evidence of record for the D3 mistake (round-50 lesson, M3) — an evidence file whose provenance is
not what it implies — and it is superseded as a control by `controls/do-nothing-c2-winhost.txt`. It is kept
byte-identical: deleting it would destroy the mistake's evidence.

## What survives unchanged

- C1's substance survives with a host-portable command: same instrument, same self-test duty, same
  `CENSUS-FRESH=ok` predicate, measured at this round's final tip. The C1 do-nothing control
  (`controls/do-nothing-c1.txt`) is genuine (instrument absent at base export → exit 2) and stays.
- The non-targets stand: depth:density guard only; no axis retired or split; no SCORECARD score asserted by
  the lane.
- The committed wave-1 spec (`wave1-spec.json`, 32 seats) is the prior session's record: its CONTEXT names
  the Linux-only roots and several seats attack the superseded C2=EPSS freeze. This round claims no
  falsification credit from it; no seat ran on this host.

## Superseding claims

`claims.v2.json` — C1' (depth:verifiability, capability-acquisition, host-portable gate command) and C2'
(coverage, frontier-admission F31 = OSV affected-range events on S080, with a host-honest predicate naming
the inherited recheck-exit-1 taxonomy). Digests in `freeze-v2.txt`.
