# Round 68 — program-execution flags refused in the derive gate (C1) and the OpenSSF Scorecard API contract (C2)

Two claims, one v1 wave of 12 seats. C1 works the lowest depth:verifiability (4) and is nominal under
QUALITY R58 (the axis's citation-resolution metric is not read by this gate: score 4 → 4). C2 is the
coverage frontier admission (8 held). Base `d0f48405e7fe44a53a28305785dc4d881a414194`; pre-freeze
controls `3dfe6f162c9cec8fdbb629738b36fc53a7ce6128`; frozen claims
`.ufo/waves/round-68/claims.json` at `7c4f9f7ec096298b1edd1912249e5864ee73d985`; C1 implementation
`82b3b7d4704e914eb224e7bb24e57aa9cbd8603f` (gate sha256
`10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8`).

## Gate

**S102 — OpenSSF Scorecard API, swagger 2.0 contract.** https://api.securityscorecards.dev/swagger.json
opened 2026-11-04 (HTTP 200, 11802 fetched bytes, normalized snapshot 7595 bytes / 429 lines,
sha256 `6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0`, fetched
2026-11-04T21:49:46Z). Located quote (≤25 words, L13): "API to interact with a project's published
Scorecard result" — admitted for the route family, the `ScorecardResult`/`ScorecardCheck`/`Repo`/
`Error` definitions and the aggregate-score field as the machine interface to the scorecard data;
refused for anything the served contract does not declare (no check semantics, no scoring formula, no
served values, no freshness claim).

**Refused candidate (recorded, not adopted).** The live project result
`https://api.securityscorecards.dev/projects/github.com/ossf/scorecard` was opened the same instant
(HTTP 200, 13259 bytes) and refused as an entry source: the served JSON is a single line, so no
located line anchor exists, and its values (date, aggregate score, per-check scores) are instance
data that change with every analysis. Both URLs' facts are in
`corpus/source-snapshots/round-68/manifest.json`.

**Refused quote.** The version literal `1.1.0` (S102.txt:15) was pinned as a quote in the first
manifest draft and refused by `source-recheck.py` with `reason=quote-too-short-to-be-evidence`
(7 characters is not evidence); the manifest carries eight quotes, maximum 9 words.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M68-1 | candidate residual was not observable | `git show <rev>:big.txt <rev>:missing.txt \| head -n 1` returns 128 on every attempt (git resolves revisions before writing), so the gate already read `stale`; the "git head SIGPIPE masking" residual named by SentinelMultiHead (round 67, F1) does not reproduce | L1 empirical probe before the freeze (three repeats, `stderr` carried the missing-path fatal) | dropped that candidate; chose the two *measured* program-execution flags instead |
| M68-2 | claim observable chosen on the wrong axis of the gate's output | at base `sort --compress-program=… -S 1K big.txt \| head -n 1` already read `stale` (`derive-upstream-signal-13`) while the compressor really ran 18288 times: the verdict hid the execution | base no-work control `controls/c1-base-donothing-r68.txt` | the predicate measures parse refusal (`rc=2`, `reason=derive-not-read-only`) plus marker runs `=0`, never the verdict alone |
| M68-3 | a pinned quote below the evidence bar | `source-recheck.py --source S102` printed `S102:Q03-version UNAVAILABLE reason=quote-too-short-to-be-evidence` | the lane's own recheck instrument, before commit | quote dropped from the manifest; the version is cited in prose, not as a quote |
| M68-4 | capture form made anchors impossible | the live project-result JSON normalizes to one 13259-byte line, so every quote would be occurrence-only | `capture-source.py` output (`wc -l` = 1) | the source was refused as an entry source and recorded as such in the manifest note |
| M68-5 | two earlier attempts of this round ended with no report | `.ufo/watchdog.log` `lane-dead-no-report kasegi round=68` at 18:36:33 and 18:42:43 (attempts 1 and 2); the lane repo was byte-clean at `d0f48405` when attempt 3 started, so nothing was inherited | the watchdog log, read at round start | attempt 3 committed the freeze and the C1 implementation before dispatch, wrote every receipt to a committed path as it was produced, and dispatched the wave from a validated spec in one handoff |

## Round shape

One v1 wave, 12 seats (spec `.ufo/waves/round-68/w1-spec.json`, dispatch `w1-dispatch.json`):
reviewer ×2 (ReviewC1, ReviewC2), scribe ×2 (ScribeF46, ScribeRound), executor ×2 (ExecC2Counters,
ExecHarness), critic (CriticC1), mutation-tester (MutationC1), sentinel (SentinelGate), revenger
(RevengerC1), scout (ScoutS102), connector (ScopeF46). Attack seats 5 of 12 (42 %), one connector.
L1 `KasegiR68a3` holds the planner seat (the validator rejects a planner role).

## Wave verdicts and adjudication

One v1 wave, 12 seats, all settled (WAVE-DONE received; `w1-results.json`). No dead seat, no
replacement, no residual call.

| seat | role | verdict | effect on the round |
|---|---|---|---|
| ReviewC1 | reviewer | VERIFIED (frozen predicate 8/8 from a `git archive` export at `82b3b7d4`) + FINDINGS | the abbreviation spellings and default-textconv class named below |
| CriticC1 | critic | DEFEATED as a *class* repair; frozen predicate passes | named open, escalated to round 69 |
| MutationC1 | mutation-tester | `killed=5/5 survivors=none equivalents=2 invalid=1` | the four new selftest cases are load-bearing |
| SentinelGate | sentinel | FINDINGS (F1 HIGH: prefix abbreviations; F2/F3 pre-existing) | admission parity shows no widening |
| RevengerC1 | revenger | FINDINGS (ranked execution-surface table) | supplies the round-69 candidate list |
| ScoutS102 | scout | AGREE (independent re-capture byte-identical; 8/8 quotes on their anchors; max 9 words) | confirms the Gate |
| ScopeF46 | connector | SCOPE CLEAR (no held row or sibling province holds the swagger ground) | confirms the admission |
| ScribeF46 | scribe | LANDED (entry + F46 row + S102 row + expected list) | C2's counts met |
| ExecC2Counters | executor | before-state from the freeze export (rows=45, registry=101, entries=48) | independent copy of the before values |
| ReviewC2 | reviewer | VERIFIED (capture chain); one condition open at its run (the S102 row had not landed) | re-measured by the L1 after landing |
| ExecHarness | executor | VERIFIED (both ends reproduced from clean exports, byte-identical to the committed receipts) | second copy of C1's before/after |
| ScribeRound | scribe | DRAFTS + three calibration findings | drafts used, numbers re-measured by the L1 |

**C1 adjudication.** The frozen predicate is met (`VERIFY measurements=8 failures=0`, exit 0, gate
sha256 `10c87100…74fee8`, receipt `controls/final-verification-r68.txt`). The claim's declared
spelling set — `--compress-program` written with `=`, as a separate token, quoted, or after another
option, and the exact token `--textconv` — is refused and neither program runs. The critic's
class-level defeat is accepted and recorded, not hidden: the refusal is spelling-exact and three
classes stay open on the same committed gate, each with a seat receipt under `w1/`:

- unique long-option prefixes of `--compress-program` (`--compress-prog=`, `--compress=`, `--co=`)
  are admitted by this host's uutils sort and run the compressor (CriticC1: 18288 runs each;
  SentinelGate: 9144 runs, verdict green);
- `git show <commit>` runs a config-declared textconv driver through `.gitattributes` with **no
  flag at all** (CriticC1 marker 2/3/5), so `--textconv` refusal covers the blob-form spelling only;
- `git cat-file --textconv` / `--filters` and `git show -c/--cc/-m` on merges still execute
  (CriticC1, RevengerC1).

**C2 adjudication.** Verified: `FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0
registry=102`, `FRONTIER-PASS F46 ids=S102`, `entries=49 pass=49 exit=0`, capture
`records=82 bound=82 unbound=0`, `knowledge-expected.txt` 86 lines / 84 entries with
`LC_ALL=C sort -c` exit 0, census exit 0 (`controls/c2-after-counters-r68.txt`).

## Round-67 routed defects — disposition

| routed | disposition |
|---|---|
| V67-1 (stale quote count `54/54` vs 58) | fixed as an appended correction with the counting command in `corpus/knowledge/first-psirt-maturity-document.md` § Corrections |
| V67-2 (bare `knowledge/...` cells, citation-ground findings) | fixed: `citation-ground-check.py --root .` findings 10 → 6 and `class-lane-bare` 5 → 1 (the remaining one is a `corpus/lessons/round-57.md:5` registry line, left as history) |
| V67-3 (C15 area list ends L463) | fixed as an appended correction naming L462/L463 |
| V67-4 (driver-pins note names pre-erratum digests) | fixed: the note now names `07dfa36c` / `ea31d439`, the values the file pins |
| V67-5 (inherited `recheck-audit.py` exit 1, `citation-ground-check.py` findings) | partially reduced (V67-2); `recheck-audit.py` still exits 1 with 9 pre-existing `cwd_fail` and 22 fail-closed lost-base entries — recorded, not fixed |
| V67-6 (`.ufo/state/kasegi.round` stale at 17) | untouched: operator-owned driver state |

## Residuals named, not claimed

- The program-execution class as a whole (the three open classes above), plus the gate's own
  standing "not a sandbox" boundary.
- `knowledge-expected.txt` was **not** sort-clean at base: round 67 appended the F45 path at the end
  and `LC_ALL=C sort -c` failed on it (ScribeF46 F2). The round-68 landing moved that one line to its
  sorted position; the base failure is recorded here rather than silently repaired.
- The round-68 manifest pins 8 quotes; the entry's Gate block cites 13 located quotes, five of which
  are line-verified by the scribe seat's own receipt and not manifest-pinned (ScribeF46 F4).
