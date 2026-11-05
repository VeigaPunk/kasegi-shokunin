# Round 73 — lesson (kasegi, attempt 1)

Round: kasegi r73 attempt 1. Frozen claims `.ufo/waves/round-73/claims.json` (freeze commit `3b53ff83`, base `fdf17413`). Attack/build wave `w1` (10 seats, one v1 wave, band 8–16; results `.ufo/waves/round-73/w1-results.json`). Report `.ufo/reports/round-73/kasegi.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M73-1 | the Q10 recheck rule (`cd <lane-root> && ` prefix, runnable from any cwd) was stated in QUALITY.md but enforced by no counter, so entries added in later rounds shipped prefix-less relative recheck lines: 11 entries had no prefix, and 10 of them exit 2 from a foreign cwd | `.ufo/waves/round-73/controls/c1-donothing-r73.txt` (census at base `fdf17413`: `entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22`, `RECHECK-CWD-RESULT nonconformant`, exit 1); names of the 11 in `.ufo/waves/round-73/w1/K73ExecRecheck.md` §1 | none (no census read the recheck cwd; QUALITY Q10 was text only) | `corpus/instruments/recheck-cwd-census.py` counts `noprefix` and `exit2_foreign` per entry; the 11 first recheck lines gain the prefix (`.ufo/waves/round-73/w1/K73ExecRecheck.U3.patch`, prefix-only per `K73ExecRecheck.md` §3) | red: the base run above exits 1 and names the 11 and the 10; the selftest fixture asserts `noprefix=2 exit2_foreign=1` on a three-entry tree (`selftest cases=1 failures=0`, exit 0) |
| M73-2 | the baseline census was run in this session before the freeze commit `3b53ff83` was written; the claim text and the do-nothing receipts therefore followed a look at the data. The receipts were committed with the freeze, but the order was not protocol order | the session order is recorded here, not in a receipt; the freeze commit carries the receipts `controls/c1-donothing-r73.txt` and `controls/c2-donothing-r73.txt` | none (the freeze step has no check that the first measurement follows the freeze commit) | disclosed in the report; the next round runs `freeze-check`-style replay before any measurement | the receipts are re-derivable from `fdf17413` (K73Falsify re-derived the C1 base values from a scratch export, `K73Falsify-ev-c1-base-rederived-verbose.txt`, equal to the receipt) |

Process note: the C2 draft's Limits section stated "The only limit sentences are …" and an authority timestamp that the capture does not carry. Both were found by `K73AttackC2` (findings F-1 and F-2) before landing and corrected in the landed entry (line 149 is a third limit sentence, "time limit"; the fetch instant sits in the manifest only). That is a near-miss, not a registered mistake, because it was caught in the wave.

## Gate

- URL: https://google.github.io/osv.dev/post-v1-query/
- Access date: 2026-11-05 (manifest `fetched_utc` 2026-11-05T07:40:48Z, HTTP 200; a re-run of the instrument by `K73ScoutCapture` reproduced the sha256 and the 6563 snapshot bytes and `cmp` exit 0).
- Capture: `corpus/source-snapshots/round-73/S108.txt`, sha256 `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9`, 150 lines.
- Located quote (capture line 24, 14 words): "Lists vulnerabilities for given package and version. May also be queried by commit hash."
- All 31 pinned quotes in `corpus/source-snapshots/round-73/manifest.json` pass `source-recheck.py` (anchors checked by the entry's recheck, `S108:Q01…Q31 OK`, exit 0 from a foreign cwd). No quote is over 25 words.

## Routed defects (not closed by round 73)

- **RC-1 (counter, found by mutation).** `recheck-cwd-census.py --selftest` does not call `main()`, so a forced `RECHECK-CWD-RESULT conformant` (M4) survives both the selftest and the base census. Owner: next round, a frozen-counter amendment with a case that runs `main()`. Evidence: `.ufo/waves/round-73/w1/K73MutateCounter.md` row M4.
- **RC-2 (counter).** A hard-coded `/tmp` scratch parent (M5) and a scratch that is not removed (M6) both survive the selftest; `K73MutateCounter` caught them by a fixture and a leak count, not by the shipped selftest. Owner: next round, same amendment.
- **RC-3 (counter).** `first_recheck` and a last-line reader are indistinguishable on the base tree (M7), because every base entry has one `recheck:` line. Proposed fixture: an entry with two `recheck:` lines. Owner: next round.
- **RC-4 (claim text, falsified).** The C1 non-claim "every recheck replays the pinned capture" is false: 27 of 88 first recheck lines are not capture replays (`K73Falsify` item 7). The claim is frozen; the statement is recorded here, not rewritten.
- **RC-5 (claim text, weakened).** The C1 kill clause "from any cwd" is measured from one foreign tempdir; the two `restoration-recheck:` lines are uncounted by the first-line rule (`K73Falsify` items 6, 9).
- **RC-6 (tree scope, falsified).** C1's `tree_scope` clause says the C2 entry does not move the C1 predicate. On the merged tree the census prints `entries=89 exit0_foreign=67` (C1 alone: `entries=88 exit0_foreign=66`); the C1 predicate holds on both, but the printed line is not the C1 after-line on the merged tree. Recorded as falsified as written.
- **RC-7 (seat, dead).** `K73AttackC1` (reviewer) returned an empty result with no report file. Its prefix-only attack is covered by `K73ExecRecheck` §3 (prefix-only proof, 11 files, exit 0) and its counter-discrimination by `K73MutateCounter`. The M-A and M-C mutants of the original plan were not run by a live attack seat.
- **RC-8 (sentinel residual, pre-existing).** Every first `recheck:` value runs through `bash -c` with the operator's environment and privileges (`K73SentinelCounter` finding 1, medium, unchanged by the repair). Owner: operator decision on whether knowledge recheck lines may run in the counter.
- **Carried from round 72:** R-1 (`--json`/`--root` outside the census WRITE_CLASS), R-2 (`freeze-check.py` `bash -c`), R-3 (`sort -T`), R-5 (realpath alias semantics), R-6 (regular-file fixture keying), R-7 (`capture-binding-check.py --root .`), L72-2/L72-3 (counter self-test and counter-internal mutants), L72-8 and L72-11. None touched this round.

## Residuals

1. The 22 fail-closed exit-1 entries (lost bases, `[lost-base]`) stay as they are by design (Q1: fail closed when the base is absent).
2. The OSV overview page (`api/`) is not captured; its rate-limit and response-size statements are not claimed.
3. The F51 entry states no rate limit and no API-key rule because the captured page states none; a reader must not supply one from another source.

## Registry changes (old → new)

- S108 (OSV.dev POST /v1/query reference): **none → mined**. Opened 2026-11-05; recheck **none → 90d**; used-by **none → corpus/knowledge/osv-post-v1-query-contract.md**. No row rejected or superseded.
- Knowledge recheck headers (C1, 11 files, prefix only; old → new; the check text is unchanged): old `recheck: <check>` → new `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && <check>` for `bugzilla-rest-api-bug-endpoints`, `cisa-vulnrichment-adp-enrichment`, `cisa-vulnrichment-record-list`, `github-repository-security-advisories-rest-api`, `nvd-api-2.0-response-schema`, `nvd-api-2.0-retrieval-interface`, `openssf-scorecard-checks`, `osv-affected-range-events`, `project-zero-big-sleep-sqlite-variant-analysis`, `project-zero-fuzzilli-vs-bigsleep-comparison`, `root-loss-2026-10-12`. The exact old and new lines are in `.ufo/waves/round-73/w1/K73ExecRecheck.U3.patch`.
- Census before → after: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 before (`kasegi ok`) and exit 0 after (`kasegi ok`); the W04 duplicate-URL warnings are inherited and unchanged.
- `corpus/instruments/knowledge-expected.txt`: 90 lines / 88 rows → 91 lines / 89 rows, `LC_ALL=C sort -c` clean.

## Sourced claim

C2 rests on S108, opened and captured this round: the entry `corpus/knowledge/osv-post-v1-query-contract.md` cites S108 for every routed claim, and the registry row S108 names that entry in `used-by`.

## Assimilation and considerthese

Assimilation: none (`merge/kasegi/` was not used this round). `considerthese/` was not mined for an OSV or query-API proposal: `K73ConnectSiblings` §4 reports the grep and its result, recorded in `.ufo/waves/round-73/w1/K73ConnectSiblings.md`.

## Seats (wave w1, 10 seats; roles executor×1, scribe×2, scout×1, connector×1, reviewer×2, critic×1, mutation-tester×1, sentinel×1; attack share 5/10)

- Reported: `K73ExecRecheck` (C1 candidate, predicate met), `K73ScribeEntry`, `K73ScribeLesson`, `K73ScoutCapture` (S108 reproduces byte-identically), `K73ConnectSiblings`, `K73AttackC2` (WEAKENED on the Limits clause, corrected), `K73Falsify`, `K73MutateCounter` (4 killed, 4 survived), `K73SentinelCounter`.
- Dead: `K73AttackC1` (empty result, no report).
