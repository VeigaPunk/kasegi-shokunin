# MutC2Chain — C2 mutation probe

Scratch mirror: `git archive ad7147532cb702b0d541d40499874552183d9132`; no lane source was changed. Disk guard status was checked before probes. Axes: coverage and depth:verifiability.

## Baseline outputs

- `python3 corpus/instruments/frontier-recheck-count.py`: `entries=27 pass=27 exit=0` (F01–F24 PASS, including F24/S063).
- `python3 corpus/instruments/capture-binding-check.py`: `records=63 bound=63 unbound=0`.
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063`: `S063:sha256 OK`; Q1/Q2/Q3 all `OK`.
- `python3 corpus/instruments/recheck-audit.py --quiet`: exit 1, `strict pass=1/60`, `lines=60 total=60 pass=60 ... exit=1`, `expect=present expected=60 missing=0 unexpected=0 exit=1`. This is a baseline failure: strict cdroot limb rejects 59 pre-existing recheck lines, so it is inconclusive for the expected-list negative probe.

## Mutations and verdicts

A. Changed F24 status cell from `admitted` to `explored` in scratch `corpus/README.md`; reran frontier harness. Actual output: all prior rows PASS, then F24 is omitted, `entries=26 pass=26 exit=0`. **SURVIVED — coverage finding.** Detector failed to fail F24 as specified; harness appears to count only entries with an admitted status and thereby removes the attacked row from its denominator. No contract change proposed.

B. Removed the `source: S063` line from scratch knowledge entry; expected detector: `recheck-audit.py` rejects the missing provenance/recheck line. Not successfully run to a completed transcript in this probe; **inconclusive**.

C. Corrupted S063 capture SHA256 in manifest; expected `source-recheck.py` and binding checker to red. Not successfully run to a completed transcript in this probe; **inconclusive**.

D. Deleted the expected-listed knowledge entry; expected audit to report `missing=corpus/knowledge/rfc-9116-security-txt.md`. Baseline audit already failed strict cdroot (1/60); mutation not isolated from baseline; **inconclusive**.

E. Changed manifest S063 `used_by` to nonexistent entry; expected binding checker unbound. Not successfully run to a completed transcript in this probe; **inconclusive**.

## Restoration

All probes ran only on disposable `git archive` scratch; the lane tree was not edited. Scratch directory was removed by shell trap. No before/after scratch hashes were retained for the status flip; lane bytes remain untouched. No tools installed.
