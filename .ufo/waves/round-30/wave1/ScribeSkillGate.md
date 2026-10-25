# ScribeSkillGate-3 — round-30 wave-1 gate scribe (SKILL.md Gates & probes registry)

Seat: `ScribeSkillGate-3` (L2 scribe, leaf). Lane: `kasegi-shokunin`. Date: 2026-10-25.
Answering model: `inception/mercury-3` (config route table; no model passed). No tool installed by this seat (RULES.md read; no pacman/uv/cargo/npm action needed).

## Behavior

1. **Warrant decision: YES — a row is warranted.** The hardened instruments `frontier-recheck-count.py` and `source-recheck.py` are the round-30 C1 counter instruments (and the C2 harness counter uses the frontier harness), yet `SKILL.md`'s Gates & probes registry lists neither (`grep -n 'frontier-recheck\|source-recheck' SKILL.md` → 0 matches; registry rows exist only for `recheck-audit.py` and `anchorcheck.py`). The round-30 claims harden exactly these instruments (M29-3/M29-4 fixes: named-row missing-entry, duplicate realpath, stem==id, occurrence-not-unique), so the registry was incomplete relative to the load-bearing gate surface. Append made (R6: appended at file end; head and all prior lines unchanged at their numbers).
2. **Append content** (SKILL.md tail, new section `## Round-30 Gates & probes registry addition (appended 2026-10-25)`): two rows, one per instrument, with entry command, verdict map (exit 0/1/2 semantics read from the committed instrument code), self-test column (frontier harness: no built-in `--selftest`, discrimination via the committed C1 control fixtures; source-recheck: `--selftest` 9-case matrix incl. stem-mismatch and double-occurrence variants), pinned-value path `.ufo/waves/round-30/c1-controls/before.txt`, write scope, owner `kasegi`; followed by an honest measurement note for the working-tree bytes at append time (digests, A1/A2/B1/B2 counter smoke, selftest result).
3. **No-verdict-movement confirmation** (run after the append, same instruments, same SKILL.md file):
   - `python3 corpus/instruments/density.py SKILL.md --label r30-post-scribe` → mean **171.1**, 23 blocks, 662 path-citation instances (before append, `--label r30-pre-scribe`: mean **167.5**, 22 blocks, 659 cites). Density change disclosed, not claimed (same posture as round 29: measurement change from the append, not a score claim).
   - `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0, verdict classes identical before/after append: 7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0. **No verdict-class movement.**
   - `sha256sum`: SKILL.md `82bdced5d5c46b6847a169f5ce6bec172dbf0c57d51bc5ec5361e2bd4731ee70` → `a05c1b47afd4498b107ff962497d0c9d7e938a6feca88fa4f0cbddd749599cfc` (1047 → 1057 lines; +10 appended lines; head byte-identical).

## Gates

- R6 (append-only; no existing line moved): satisfied — append at file end; anchorcheck before/after prints the same cited source lines and verdict counts.
- No verdict-class movement: satisfied (anchor exit 0; classes identical).
- Read-only bounds: no writes to fleet root, sibling lanes, `/home/vgpnk/Projects/shokuknow`, lane git/jj state, `.ufo/state`, `MANIFEST.json`. Writes: `SKILL.md` (append) and this report only.
- No live target contacted (all runs local; Q6 documentation-only posture).

## Touched surfaces

- `SKILL.md` — appended lines 1048–1057 (Round-30 Gates & probes registry addition section, 2 table rows + measurement note). 1047 prior lines unchanged.

## Findings (measured at current working-tree bytes)

- Working-tree instrument digests at measurement time: `frontier-recheck-count.py` `bab0d321f75f1b79c5ed839b92b29164f5c2139d61af9d63cca1c904592b8d36`; `source-recheck.py` `0b841d5ddb80f96f0e802eec1e67a0b9ba0606609282d8991759db72ac71a243` (committed base analogues in `c1-controls/before.txt`: `c8a62888…` / `9fe6a4a0…`). Instrument bytes are mid-wave (executors still landing the fix).
- C1 counter smoke at those bytes: A1 exit 1 with named-row `FAIL F98 knowledge/zz-missing.md problems=missing-entry` ✓ (claim predicate met); A2 exit 1 **via `NameError: name 'cited' is not defined` traceback** (frontier harness line 83, `entry_contract`) — duplicate-realpath limb not yet landing cleanly; B1 exit 1 `reason=stem-mismatch` ✓; B2 exit 1 `reason=stem-mismatch` (current `manifest-b2.json` capture stem precedes the occurrence limb); `source-recheck.py --selftest` → `cases=9 failures=1` (the `stem-mismatch` selftest case observes exit 0, so its own fixture does not yet produce the mismatch). These are mid-wave observations; the rows' verdict-map cells record the contract the landed fix must satisfy, and post-integration re-runs belong to `ExecPostCommitRecheck`.

## Out-of-scope items

- No edits to instrument code (owned by executors), claims.json, SCORECARD.md, lessons, or anything outside `SKILL.md` + this report.
- No subagent/task dispatch (leaf).
- Round-30 C1/C2 kill-rule verdicts and receipt re-runs are other seats' scope (recorded here only as measured observations at append time).

## Artifact paths

- Report: `.ufo/waves/round-30/wave1/ScribeSkillGate.md` (this file).
- Edited file: `SKILL.md` (append at tail).
- Measured inputs: `.ufo/waves/round-30/c1-controls/before.txt`, `before-run-2.txt`, `mutants/control-b1.out`, `control-b2.out`, `c2-controls/before.txt`, `census-before.txt`, `claims.json`, `wave1-spec.json`.
- Read-only package: `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` (+ `MERGE-REPORT.json`); `SOURCES.append.md` exists at the package root (the assignment's `SOURCESUR.append.md` path was a typo; read the package directory listing).
