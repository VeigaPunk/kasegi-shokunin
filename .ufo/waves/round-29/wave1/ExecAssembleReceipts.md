# ExecAssembleReceipts — round-29 wave-1 receipt rollup

Seat: `ExecAssembleReceipts` (executor, leaf — no subagents, no labrat, no background jobs).
Round 29, wave 1 (build+attack, 64 seats, hyaku run 7). Lane: kasegi-shokunin.
Scope: only `.ufo/waves/round-29/wave1/` (this report, `receipts/`, `receipt-index.txt`,
`assemble-receipts.py`).
Answering model: `inception/mercury-3` (session default per workstation context; the task is a
deterministic file assembly — no route-table lookup was needed, no model was passed).

## What was produced

| artifact | path | notes |
|---|---|---|
| seat report copies | `.ufo/waves/round-29/wave1/receipts/NN_<Seat>.txt` | flat, numbered by registry order (01–64); refresh from `<Seat>.md` |
| index | `.ufo/waves/round-29/wave1/receipt-index.txt` | `seat | role | file | status` for all 64 seats; status = ok / missing / empty |
| assembler | `.ufo/waves/round-29/wave1/assemble-receipts.py` | idempotent; re-runnable by the L1 post-integration to fold in stragglers |

Seat list and roles come from `swarm-registry.json` (64 members; registry order; 20 executor, 13
scribe, 11 reviewer, 5 scout, 4 critic, 4 mutation-tester, 3 connector, 2 simplifier, 1 sentinel,
1 revenger). Numbered copies are byte-identical to their source reports (verified with `cmp` on
every copy; all `MISMATCH` count = 0). Seat-authored unnumbered files already inside `receipts/`
(e.g. `ExecCanonC2.txt`) were left untouched.

## Snapshot state (final run)

- **ok = 60**, **empty = 0**, **missing = 4** of 64 (after this report lands; see index).
- Missing at snapshot — **pending, not classified dead** (no error text is visible anywhere:
  `.ufo/waves/round-29/wave1-run.err` is 0 bytes; agent roster shows these seats parked/idle/running,
  none failed):
  - `ExecHarnessC2` (executor)
  - `ScribeScorecard` (scribe)
  - `RevNoHarmC1` (reviewer)
  - `RevKillTry` (reviewer)
- Reported before 2026-10-25T18:21Z (see receipt-index.txt `# generated at`). The four seats above
  may land after this snapshot; re-run `python3 .ufo/waves/round-29/wave1/assemble-receipts.py`
  to refresh `receipts/` + `receipt-index.txt` without touching any seat report.

## Production state cross-check (what the rollup covers)

C1 subject landed: `corpus/instruments/anchorcheck.py` sha256
`68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` (ExecImplC1 report + canonical
`wave1/c1-receipt-index.txt` present, `selftest cases=12 failures=0`, `limbs=9 covered=9`,
`nogit_exit=0`, digest line matching).
C2 subject landed: `corpus/knowledge/program-severity-ladders-and-reward-scales.md` exists (7,583 B),
`corpus/SOURCES.md` has 3 rows `S043/S044/S045`, frontier admitted count = 13 (awk counter),
`corpus/source-snapshots/round-29/manifest.json` exists.
These are the claims' subject files; the counters themselves are other seats' scope.

## Bounds compliance

- Writes: only the five paths listed above, all under the lane repo.
- No tools installed (stdlib python only); no pacman transaction; no git fixtures created; no
  subagents/labrat spawned; no peer broadcast.
- Peer coordination: answered `RevC2Entry`'s query (F13 entry/report absent at that time) via
  `write agent://RevC2Entry`.

## Risks / notes

- The 4 missing seats are a timing artifact of assembling mid-wave, not a verdict; the L1 should
  re-run the assembler after integration (R14: receipts are regenerable artifacts).
- If any of the four never lands, they are the seats to classify dead with error text; none is
  visible in the harness log at snapshot time.
