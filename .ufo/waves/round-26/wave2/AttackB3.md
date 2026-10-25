# Attack B3 — F11 frontier harness re-run (C2 integration; M26-3 fix check)

Seat: `L1Kasegi26.AttackB3` (leaf, read-only; no subagent dispatch, no installs — python3 already present, so no tooling-directive record).
Item: run `python3 corpus/instruments/frontier-recheck-count.py --root <lane>`, record per-row lines + exit (expect 14/14 exit 0, F11 twice with ids=S041); verify the F11 entry-cell names equal the two real unsuffixed filenames and that both files exist.
Attacks: the wave-1 claim that the F11 row's entry cell was aligned to the actual entry names (M26-3 fix, §Fixes 6) and that the frontier harness passes on the live map.

## 1. Frontier harness run (lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

Command: `python3 corpus/instruments/frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin`
Run: 2026-10-25 UTC, `cwd` = lane root. Per-row output verbatim:

```
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
entries=14 pass=14 exit=0
```

Shell exit code: `EXIT=0`.

Expected outcome met exactly: **14/14 PASS, exit 0**, F11 contributes two rows, both with `ids=S041` and `exit=0`. No `FileNotFoundError`, no `harness UNAVAILABLE`, no FAIL row — the M26-3 crash (staged suffixed names in the F11 cell) is not present on the live tree.

## 2. F11 entry-cell names vs real unsuffixed filenames

`corpus/README.md` F11 row (line 212), entry cell (col 4):
`knowledge/iso-29147-and-30111-division-of-labour.md, knowledge/iso-29147-divergence-and-clause-crosswalk.md`

- Cell names equal the two **real unsuffixed** filenames: no `-2026-10-23` staged suffix on either.
- Both files exist: `corpus/knowledge/` holds exactly the two `iso-29147*` entries (`iso-29147-and-30111-division-of-labour.md`, `iso-29147-divergence-and-clause-crosswalk.md`); each is also present in the committed expected list `corpus/instruments/knowledge-expected.txt` (39 entries, both listed) and in `c1-live.json`'s `expected_entries` (both listed, `missing=0 unexpected=0`).

## Verdict

The attacked claim holds: the frontier harness re-runs clean on the live lane (14/14 exit 0; F11 twice, ids=S041), and the F11 entry cell names match the two real unsuffixed knowledge files, both of which exist. No actionable defect found in scope.

## Residual risk / verification gaps

- Instrument scope: `frontier-recheck-count.py` measures recheck coverage (A–D contract + exit 0) only; it does not attest that the entries' body quotes assert what the entries claim, nor that S041's manifest pins hold upstream — those are other seats' items (source-recheck / manifest), not this attack.
- Here F11's `S041` id is verified present on both rows and the recheck invocations exited 0; the underlying `source-recheck.py --source S041` success is evidenced by those exits (the harness runs the exact `recheck:` line from the lane root).
- Read-only: no production edit made; the only writes are this report at `.ufo/waves/round-26/wave2/AttackB3.md` (mirrored at `b3.md`).
