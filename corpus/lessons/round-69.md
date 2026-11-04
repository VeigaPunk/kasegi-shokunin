# Round 69 — the derive gate refuses the eight measured program-execution/write shapes (C1) and the GitHub global security advisories REST API (C2)

Two claims, one v1 wave of 12 seats. C1 works the lowest depth:verifiability (4) and is nominal under
QUALITY R58 (the axis's citation-resolution metric is not read by this gate: score 4 → 4). C2 is the
coverage frontier admission (8 held) and the round's sourced claim (S103, opened this round). Base
`656272cf6b753fab7ce249f286b824c87677fdf3`; pre-freeze controls `4d91dcd3f3cfdb3bad0324ac20c30bce489eee61`;
frozen claims `.ufo/waves/round-69/claims.json` at `9b877fd916308e948b865c44ebc76e6ad322d6a7`; C1
implementation `1bd01ee1e6558925e23d3d27a4bb12b88f502656` (gate sha256
`c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde`); C2 landing
`981115648e4108e1adf5aec010edadac285a0c78`.

## Gate

**S103 — GitHub Docs, REST API endpoints for global security advisories.**
https://docs.github.com/en/rest/security-advisories/global-advisories opened 2026-11-04 by the L1
(`capture-source.py --kind html`, HTTP 200, 329039 fetched bytes, snapshot 15500 bytes / 585 lines, sha256
`c531c1e9b3eb9b4443e9851edc479e137eff772fb41dca3db16d697ac514344f`, fetched 2026-11-04T22:17:58Z). Located
quote (17 words, `S103.txt:275`): "If no other parameters are defined, the request will return only
GitHub-reviewed advisories that are not malware." Admitted for the two endpoints, the list filters with their
enumerated values and defaults, pagination/sort controls and the unauthenticated-public statement; refused for
anything the page does not state (no response schema in the capture, no database curation semantics, no
numeric rate limit). Thirteen quotes pinned in `corpus/source-snapshots/round-69/manifest.json`
(`source-recheck.py --source S103` rc 0, 13/13 OK).

**Refused candidate (opened, not admitted).** ENISA EUVD API documentation,
https://euvd.enisa.europa.eu/apidoc, opened 2026-11-04: the static HTML is a 3062-byte single-page-application
shell with zero occurrences of any endpoint name; the documentation text exists only in a 544337-byte minified
bundle and after JavaScript rendering, so the lane's capture instrument cannot produce a line-anchored
snapshot (`.ufo/waves/round-69/controls/euvd-refusal-r69.txt`). Flip: a statically served or line-anchorable
rendering of the same documentation. SOURCES.md status changes: S103 new row (mined); no existing row's
status, recheck or used-by cell changed.

**Assimilation:** none this round (no `merge/kasegi/` theme or `considerthese/` proposal fits the two claims).

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M69-1 | tool identity measured through the wrong binary | round 68's report, `w1/RevengerC1.md` and `w1/CriticC1.md` call the host sort "uutils sort 0.8.0", while the gate's `subprocess.Popen(["sort", …])` runs `/usr/bin/sort` = GNU coreutils 9.12 (`.ufo/waves/round-69/controls/c1-base-donothing-r69.txt` HOST line); the omp bash tool's bare `sort` is a shell builtin (`type -a sort` → "sort is a shell builtin", then `/usr/bin/sort`) | the round-68 closure V68-5 (non-author) noticed the contradiction; nothing in the lane captured it | the round-69 counter prints a `HOST` line resolved the way the gate resolves argv[0] (from Python, not from the shell), and the wave context tells seats to call `/usr/bin/sort` explicitly; this fails visibly if a future receipt's HOST line disagrees with a seat's claim |
| M69-2 | frozen count did not budget a contract-required rejected row | `/home/vgpnk/Projects/shokunin/CORPUS.md:101-104` keeps rejected sources as registry rows (`status` `rejected`, `teaches` `REJECTED: …; flip: …`), but the C2 freeze (`claims.json` C2 predicate `registry=103`) counted only the admitted row; the EUVD rejection was therefore recorded in the Search log and the manifest note, not as a registry row | none at freeze time (found while landing, before any seat scored) | the frozen predicate is kept unchanged (no post-freeze rule change); the EUVD row is owed to the registry in a later round whose freeze counts it. A future C2 freeze states `registry = before + admitted + rejected`; the census count would then fail a freeze that forgot the rejected row |
| M69-3 | hand-typed freeze timestamp (inherited, V68-1) | round-68 `claims.json` `frozen_at` 21:52:00Z vs freeze commit 21:50:37Z | round-68 non-author closure | round-69 `claims.json` names no clock time and defers to the freeze commit's committer date; the round-68 correction is appended in `.ufo/waves/round-68/claims-erratum-r69.md` (the closed `claims.json` bytes are unchanged) |
| M69-4 | lost shell variables in a backgrounded compound command | the first forgery/trial run wrote to `/trial.out` and `/forg.out` (Permission denied) because the variables set before `&` were not visible in the subshells as composed; 127 s lost, nothing written in the lane or fleet | the redirect error itself | rerun with literal absolute paths (receipts `controls/c1-forgery-blanket-r69.txt`, `controls/c1-candidate-trial-r69.txt`); scratch paths in later commands are literal |
| M69-5 | untested refusal limbs | `.ufo/waves/round-69/controls/l1-mutation-r69.txt`: one-limb mutants M9 (drop `"--" in parts[2:]`) and M10 (drop `or not operands`) survive the 86-case selftest | L1 mutation pass after the measured commit (no non-author mutation seat survived) | QUALITY R103; the two cases (`git show` with no operand, `git show HEAD:g.txt -- g.txt`) are owed to the next gate change — adding them now would move the frozen pin `cases=86` after measurement |

## Round shape

One v1 wave, 12 seats (spec `.ufo/waves/round-69/w1-spec.json`, dispatch `w1-dispatch.json`, spawn=12):
reviewer ×2 (ReviewC1, ReviewC2), critic ×2 (CriticC1, CriticC2), mutation-tester ×2 (MutationC1,
MutationCounter), sentinel (SentinelGate), revenger (RevengerHosts), scout (ScoutS103), connector (ScopeF47),
executor (ExecHarness), scribe (ScribeRound). Attack seats 6 of 12 (50 %), one connector. L1 `KasegiR69`
holds the planner seat (the validator rejects a planner role).

## Wave verdicts and adjudication

WAVE-DONE received (`.ufo/waves/round-69/w1-results.json`, seats=12). **Two seats settled, ten died.** The
orchestrator observed (message 2026-11-04, not inferred) that CriticC1-6, MutationC1-6, MutationCounter-5,
SentinelGate-2, RevengerHosts, ScoutS103, ScopeF47, CriticC2, ExecHarness-3 and ScribeRound-4 each ended on
one terminal error: `[commandcode/deepseek/deepseek-v4.1-flash] 401 Invalid 'Authorization' header or token.
(type=authentication_error param=UNAUTHORIZED)`, with no fallback walk; they wrote no report or scratch.
They stay dead in the evidence and were not replaced (orchestrator instruction); no residual call.

| seat | role | verdict | effect on the round |
|---|---|---|---|
| ReviewC1 | reviewer | VERIFIED — frozen predicate `VERIFY measurements=13 failures=0` reproduced from a `git archive` export at `1bd01ee1`; base `failures=10`; freeze precedes implementation and `git diff 4d91dcd3 9b877fd9 -- corpus/instruments/figure-audit.py` is empty (`w1/ReviewC1.md`, receipts `w1/ReviewC1/01-06`) | non-author reproduction of C1 |
| ReviewC2 | reviewer | VERIFIED — every frozen before/after C2 value MATCH on base and landing exports; S103 row 11 columns, next id, quote 17 words at L275; census exit 0 (`w1/ReviewC2.md`) | non-author re-measurement of C2 |
| ten seats | critic ×2, mutation-tester ×2, sentinel, revenger, scout, connector, executor, scribe | DEAD (401 above) | no class attack, no independent source re-capture, no sibling-overlap scan, no clean-clone harness |

Because every attack seat died, the round carries only **author** attack evidence, labelled as such:
`controls/l1-mutation-r69.txt` (9/11 one-limb mutants killed, two survivors → M69-5/R103),
`controls/l1-residual-probes-r69.txt` (range spellings carrying `:` are admitted but resolve to a git error,
no driver run), `controls/c1-strace-candidate-r69.txt` (11105 execve over the frozen counter run, zero of the
three marker programs), and the pre-freeze blanket-refusal forgery (`controls/c1-forgery-blanket-r69.txt`,
failures=4). None of these is a non-author verdict.

**C1 adjudication.** Verified on its frozen predicate (`controls/final-verification-r69.txt`, ReviewC1). The
claim is the enumerated set P1..P8, not the class; residuals stay named: python counters with `--root`/`--out`
(round-68 RevengerC1 rows 2 and 7), `sort -T` temp writes, environment variables, host-file reads, and the two
untested limbs (M69-5).

**C2 adjudication.** Verified (`controls/c2-after-counters-r69.txt`, ReviewC2). The sibling-overlap scan and the
independent re-capture did not run (dead seats); the L1's own screen is the Search log entry in
`corpus/SOURCES.md` and the F36 entry's own pointer at `corpus/knowledge/github-repository-security-advisories-rest-api.md:45-46`.

## Round-68 routed defects — disposition

| routed | disposition |
|---|---|
| V68-1 (future-dated `frozen_at`) | appended correction `.ufo/waves/round-68/claims-erratum-r69.md` (closed `claims.json` unchanged); round-69 `claims.json` names no clock time (M69-3) |
| V68-2 (report printed base selftest `ok`) | recorded in the same erratum; the receipt is authoritative |
| V68-3 (program-execution class open) | worked as C1: the eight measured shapes refused; the remaining residuals are listed above |
| V68-4 (closed receipt re-indented in place) | not reversible without a second in-place edit; recorded here, and round 69 wrote its round-68 correction as a new file rather than editing a closed receipt |
| V68-5 (sort identity, counter docstring six/five, 420 KB) | settled by M69-1/R101 (the gate runs GNU coreutils 9.12); docstring and size noted in the erratum; the gate comment now says 480000-byte |
| V67-5/V67-6 (inherited) | `recheck-audit.py` still exit 1 with 9 `cwd_fail` (`controls/lane-health-r69.txt`); `.ufo/state` untouched |

## Residuals named, not claimed

- EUVD (ENISA) API documentation is owed a `rejected` registry row (M69-2) once a round's freeze counts it.
- The two untested `git_show_operands_ok` limbs (M69-5).
- The derive gate is not a sandbox: counters, `sort -T`, environment variables and host-file reads stay open.

