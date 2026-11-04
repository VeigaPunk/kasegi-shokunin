# Round 68 — program-execution flags refused in the derive gate (C1) and the OpenSSF Scorecard API contract F46 (C2)

Two claims, one v1 wave of 12 seats. C1 works the lowest depth:verifiability (4), nominal under
QUALITY R58 (the axis's citation-resolution metric is not read by this gate: 4 → 4, delta 0). C2 is
the coverage frontier admission (8 held). Base `d0f48405e7fe44a53a28305785dc4d881a414194`;
pre-freeze controls `3dfe6f162c9cec8fdbb629738b36fc53a7ce6128`; frozen claims
`.ufo/waves/round-68/claims.json` at `7c4f9f7ec096298b1edd1912249e5864ee73d985`; C1 implementation
`82b3b7d4704e914eb224e7bb24e57aa9cbd8603f` (gate sha256
`10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8`).

<!-- DRAFT by seat ScribeRound. Every number below was produced by a command this seat ran; receipts in
.ufo/waves/round-68/w1/ScribeRound/. Values the L1 must still measure on committed bytes are marked
NOT MEASURED BY THIS SEAT. -->

## Gate

**S102 — OpenSSF Scorecard API, swagger 2.0 contract.** https://api.securityscorecards.dev/swagger.json
opened by this seat 2026-11-04T21:53:35Z (HTTP 200, 11802 fetched bytes, raw sha256
`d526f3274a6dbcb1ba6632bf3ee1e9a642dc2106b18a1354cc0c8a26104c8af4`). Stripping per-line leading/trailing
whitespace and adding the final newline reproduces the committed capture
`corpus/source-snapshots/round-68/S102.txt` exactly: sha256
`6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0`, 429 lines (receipt
`w1/ScribeRound/s102-fetch-scribe.txt`). The capture's own fetch is 2026-11-04T21:49:46Z (manifest);
the served bytes did not drift between the two fetches.

Located quote (≤25 words, 9 words, `S102.txt:13`, manifest Q01): "API to interact with a project's
published Scorecard result".

Admitted for: the machine interface to the scorecard data — `swagger: "2.0"` (L11), `info.version`
`1.1.0` (L15), `host` `api.scorecard.dev` (L17), the route family `/projects/{platform}/{org}/{repo}`
(L19), `/projects/{platform}/{org}/{repo}/badge` (L160) and `/version` (L234), the
ScorecardResult/ScorecardCheck/Repo/Error definitions and the aggregate-score field ("Aggregate score
of the repository", L353).

Refused for: what any check measures or how it is scored (that is the check documentation the lane
already holds as F35/S086), and any served instance value. The live result
https://api.securityscorecards.dev/projects/github.com/ossf/scorecard, re-opened by this seat (HTTP 200,
13259 bytes, 1 line, `date` 2026-11-03T06:28:58Z, `score` 8.8), carries no located line anchor and its
values change per analysis; it is refused as an entry source, as recorded in the round-68 manifest note.

**Own-work diagnostics (not domain sources).** The base gate bytes
`controls/base-gate-d0f48405.py` (sha256 `8147350c…`), the frozen counter
`controls/c1-probe-run-r68.py` (sha256 `785e38fd…`) and its receipts are own-work evidence for a local
instrument, not new domain ground and not a frontier admission.

## Mistakes

Only rows whose evidence this seat re-ran or re-read are listed.

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M68-1 | allow-listed head admits a program-execution flag | Base gate, frozen counter re-run by this seat: `python3 -B …/c1-probe-run-r68.py --gate …/base-gate-d0f48405.py --work /fast/scratch/hyaku/kasegi-r68/ScribeRound/workb --mode base` → `MEASURE sort-compress-refused FAIL rc=1 marker_runs=18288`, `MEASURE git-textconv-refused FAIL rc=1 marker_runs=1`, `VERIFY measurements=8 failures=4 … mode=base` exit 1 (`w1/ScribeRound/c1-base-scribe.txt`). Originally measured as a pre-existing class in `.ufo/waves/round-67/w1/SentinelMultiHead.md` §3 (re-read: "**68 217** (base) / **68 222** (candidate) compressor invocations", "**1** driver run") | round-67 SentinelMultiHead §3; round-68 L1 no-work control `controls/c1-base-donothing-r68.txt` | `82b3b7d4`: `--compress-program` added to sort's denied flags and `--textconv` to `git show`'s; four selftest cases (73 → 77). Same counter on the committed gate: `VERIFY measurements=8 failures=0 gate_sha256=10c87100… mode=candidate` exit 0 (`w1/ScribeRound/c1-candidate-scribe.txt`) |
| M68-2 | committed receipt labelled with a revision whose bytes it did not measure | `controls/c2-base-counters-r68.txt` header reads `revision d0f48405…` but its capture line is `records=82 bound=81 unbound=1`; this seat's run on `git archive d0f48405` gives `records=81 bound=81 unbound=0 exit=0` (`w1/ScribeRound/c2-base-d0f48405-scribe.txt`). `git ls-tree -r --name-only d0f48405 corpus/source-snapshots/round-68` prints nothing: the round-68 manifest is not in d0f48405. `claims.json` C2 `do_nothing_control` quotes `records=81 bound=81 unbound=0` and cites this receipt, which shows 82/81/1 | ScribeRound (this seat), re-measurement; the receipt's own trailing note discloses that the manifest was committed before the freeze | Draft for L1: relabel the receipt as measured on the tree with the round-68 capture input (`3dfe6f16`), and record the true-d0f48405 value beside it in an erratum; the frozen file is not rewritten |
| M68-3 | lane is red between the capture commit and the registry row | At C1 implementation `82b3b7d4` (git archive) this seat ran `python3 -B corpus/instruments/capture-binding-check.py` → `records=82 bound=81 unbound=1`, exit 1 (`w1/ScribeRound/c2-counters-scribe.txt`) | ScribeRound (this seat) | Expected interim state of a capture-first round; closes only when the S102 registry row is committed. Draft rule: commit the capture input and its registry row together, or name the interim red in the controls receipt |
| M68-4 | counter measurement reads the live lane, not committed bytes | Same frozen counter, committed gate, `--lane` pointed at a `git archive 82b3b7d4` export (no `.git`): `MEASURE real-ledger FAIL FIGURE-AUDIT figures=35 ok=11 stale=24 exit=1 rc=1`, `VERIFY measurements=8 failures=1` exit 1 (selftest 77/0 and mutbat 5/5 still pass there); with the default `--lane` (the live lane repo) the same measurement reads `figures=35 ok=35 stale=0` (`w1/ScribeRound/c1-candidate-archive-lane-scribe.txt` vs `c1-candidate-scribe.txt`). The gate run directly on the export prints `FIG frontier-rows … derived=UNAVAILABLE reason=derive-exit-1 stale` | ScribeRound (this seat) | Not a defeat: the frozen counting command uses the default lane. Record that measurement 6 (real ledger) derives against the live lane repo's git history and worktree, so a "from committed bytes" reproduction needs a git checkout at the revision, not an archive export |

## Round shape

One v1 wave, 12 seats (`w1-spec.json` items = 12; `w1-dispatch.json` `counts` spawn=12 resume=0
total=12, band 8–16): ReviewC1 and ReviewC2 (reviewer ×2), CriticC1 (critic), MutationC1
(mutation-tester), SentinelGate (sentinel), RevengerC1 (revenger), ScoutS102 (scout), ScopeF46
(connector), ScribeF46 and ScribeRound (scribe ×2), ExecC2Counters and ExecHarness (executor ×2).
L1 `KasegiR68a3` holds the planner seat (the validator rejects a planner role) and is the sole
production integrator. Attack seats: reviewer ×2, critic, mutation-tester, sentinel, revenger = 6 of 12.
Seat settlement, dead seats and residual calls: NOT MEASURED BY THIS SEAT (no `w1-results.json` and
only four seat directories existed when this draft was written).

## Final measurement

- C1, frozen counter on the committed gate (this seat, export of `82b3b7d4`, default lane):
  `VERIFY measurements=8 failures=0 gate_sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 mode=candidate`, exit 0.
- C2 after-state on committed bytes: NOT MEASURED BY THIS SEAT (the S102 registry row, F46 entry and
  knowledge-expected line were uncommitted ScribeF46 worktree edits over HEAD `82b3b7d4`). The same
  commands on that uncommitted worktree at 2026-11-04T21:58:53Z (`w1/ScribeRound/c2-live-worktree-scribe.txt`):
  `FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0 registry=102`, `FRONTIER-PASS F46 ids=S102`,
  `entries=49 pass=49 exit=0`, `records=82 bound=82 unbound=0` (exit 0), knowledge-expected 86 lines /
  84 entries, census exit 0 — equal to the frozen after-target, pending the L1's commit and re-run.
  Before at `d0f48405` (this seat): `FRONTIER-CENSUS rows=45 admitted=45 closed=45 problem-rows=0 registry=101`,
  `entries=48 pass=48 exit=0`, `records=81 bound=81 unbound=0`, knowledge-expected 85 lines / 83 entries.

## Open boundaries

The remaining program-execution surface of allow-listed heads beyond the two measured flags (prefix
abbreviations, other heads' flags, environment-driven execution) is a named residual, not claimed and not
measured by this seat. Sandbox, authenticity and pipefail readings, source restoration and the
operator-owned R15/R57/R59/R60/R67/R69 decisions are untouched. Scores 4/8/9 held.
