# RevC1Instrument — round 30, wave 1 (C1 instrument conformance review)

Seat: `RevC1Instrument-2` (L2 reviewer, leaf — no subagents dispatched, no tools installed).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `a94871315caf…`; claims freeze `3c5573541300…`.
All commands run from the lane root; every write this seat made is this report file (mutant scratch lived in `/tmp/r30rev`, deleted after use).

## Bytes measured (sha256, bound before and after every run)

| file | base (frozen) | measured this review |
|---|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` | **`aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`** (stable across all my runs; pre- and post-run hashes equal) |
| `corpus/instruments/source-recheck.py` | `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | **`33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`** (pre- and post-run hashes equal) |

Drift observed during the wave: `source-recheck.py` went `9fe6a4a0…` (freeze) → `0b841d5d…` (18:50:40, per `c1-controls/mutants/digest-poll.log`) → `72f411b0…` (on disk at my first pass; my first four-counter run at those bytes) → `33602a9d…` (my bound pass). **Counter outputs were byte-identical at `72f411b0…` and `33602a9d…`.** Both instruments are still uncommitted (`git status`: ` M` on both, plus `corpus/instruments/knowledge-expected.txt`); the committed-digest conjunct of the kill rule can only close at `ExecPostCommitRecheck` (owed). Freeze copies in `c1-controls/mutants/` hash-match the base digests exactly — the do-nothing control bytes are authentic.

## Verdict — **conditional agree** with the C1 claim receipt

- The landed instruments **do implement all four C1 semantics**; A1, A2, B1 predicates hold exactly as written, verified by reading the code and by re-running the committed counters.
- **B2 holds only on its exit-code + "a failure reason" clauses.** The committed B2 counter produces `reason=stem-mismatch`, **not** the predicate sentence's `reason=occurrence-not-unique`, and the claims' own mutants clause ("mutant-B2 … must make B2 exit 0") is **false on the committed fixture** (measured: mutant-B2 still exits 1 via the stem limb). The receipt is not receivable until the B2 fixture/counter pair is corrected (fix below lands as an appended claims correction — `claims.json` stays frozen).

## 1. C1 semantics — verified by reading the landed sources

- **A1 named-row fail-closed**: `entry_contract()` now returns `None` when the entry exists under neither `root/<entry_path>` nor `root/corpus/<entry_path>`; `evaluate()` turns `None` into `problems=["missing-entry"]` (row id printed in the record line); `main()`'s `fail_closed = duplicate is not None or not records or passed != len(records)` → exit 1. No `open()` of an absent file remains on that path — the base bytes' uncaught `FileNotFoundError` is unreachable through `entry_contract`.
- **A2 duplicate realpath rejection**: after evaluation, `main()` builds `seen_realpath` over `record["realpath"]` (`os.path.realpath` of the resolved entry file); the first repeat prints `DUPLICATE-ENTRY <rowA>,<rowB> <entry>` and sets `duplicate`, feeding `fail_closed` → exit 1. Realpath canonicalization means alias spellings collide, as intended.
- **B1 stem==id fail-closed**: `check_source()` rejects before any sha256/quote work: `if Path(path).stem != source_id: emit(... "MISMATCH", "reason=stem-mismatch"); return 1`. Exit-1 propagates through `recheck()`'s status merge.
- **B2 non-unique-without-anchor fail-closed**: `anchor_verdict()` classifies `missing`/`out-of-range`/`broken`; `check_source()` fails any assertion with `occurrences > 1 and verdict != "ok"`, emitting `reason=occurrence-not-unique` / `anchor-out-of-range` / `anchor-broken`, `status = 1`. Anchored non-unique quotes still pass when the anchor verifies (`anchor=N-ok` window check). Unique quotes need no anchor. `--selftest` covers the whole matrix: `selftest cases=9 failures=0` (clean, corrupt, missing-source, missing-manifest, stem-mismatch, double-occurrence, double-anchored, out-of-range, broken).

## 2. The four counts — re-run by this seat at the bound digests

| counter | measured output | exit | predicate/kill clause |
|---|---|---|---|
| A1 `--root …/harness-root-a1` | `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry` / `entries=1 pass=0 exit=1` | **1** | ✓ names row F98, no traceback |
| A2 `--root …/harness-root-a2` | two `PASS` rows then `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md` / `entries=2 pass=2 exit=1` | **1** | ✓ names the duplicate entry |
| B1 `--manifest …/q9/manifest-b1.json --source S043` | `S043:manifest MISMATCH reason=stem-mismatch` | **1** | ✓ `reason=stem-mismatch` |
| B2 `--manifest …/q9/manifest-b2.json --source S045` | `S045:manifest MISMATCH reason=stem-mismatch` | **1** | ✗ named reason is B1's, **not** `reason=occurrence-not-unique`; exit+reason clauses hold, isolation does not |

Fixture integrity checked: `manifest-b1.json`/`manifest-b2.json` in the tree hash-equal to the claims-freeze commit (`d2e09c89…`, `3a13e5c3…`); `B2.txt` hashes to its manifest's `55124b0e…` and the quote occurs exactly 2× — the fixture is self-consistent with the *base* semantics it was frozen under, but its `id S045`/`path B2.txt` mismatch now short-circuits at the new stem limb (`Path("B2.txt").stem == "B2" != "S045"`), so the occurrence limb is unreachable on it.

## 3. Mutant isolation — independently reproduced (my own mutants, built in `/tmp`, deleted after)

Each mutant = landed bytes with exactly one limb removed (string-patch asserted to differ from landed source):

| mutant | limb removed | target fixture | measured | isolating? |
|---|---|---|---|---|
| mutant-A1 (missing-entry `return None` dropped → base crash restored) | A1 | harness-root-a1 | exit 1, `FileNotFoundError` traceback, no `F98` anywhere | ✓ flips |
| mutant-A2 (`DUPLICATE-ENTRY` block + `duplicate` term removed) | A2 | harness-root-a2 | exit 0, `entries=2 pass=2 exit=0` | ✓ flips |
| mutant-B1 (`stem != source_id` branch disabled) | B1 | manifest-b1 | exit 0 (`sha256 OK`, `Q1 OK normalized=markup-whitespace occurrences=1`) | ✓ flips |
| mutant-B2 (`occurrences > 1 … != "ok"` branch disabled) | B2 | manifest-b2 (committed) | **exit 1, `reason=stem-mismatch`** | **✗ does not flip** |
| mutant-B2 | B2 | **corrected isolating fixture** (id `S045`, path `S045.txt` = same double-occurrence bytes, same sha) | exit 0, `occurrences=2 anchor=MISSING` | ✓ flips on a clean fixture |
| live instrument | — | corrected fixture | exit 1, `S045:Q1 MISMATCH reason=occurrence-not-unique` | — limb proven present and load-bearing |
| mutant-B1 | B1 | corrected fixture | exit 1, `reason=occurrence-not-unique` | — B1/B2 orthogonal on the right fixtures |

Consequence: an implementation omitting the entire B2 occurrence branch passes every element of C1's kill rule as currently written — B2 counter (fires via stem), A1/A2/B1 counters, and all real-manifest rechecks. This matches the independent CritC1Kill receipt (`.ufo/waves/round-30/wave1/CritC1Kill.md` §3–§4); my runs above are my own, not imports.

## 4. Real-corpus regression clause — green at the measured bytes

- **Lane harness**: `python3 corpus/instruments/frontier-recheck-count.py` → **`entries=17 pass=17 exit=0`**, including `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0` (F14 landed between my first pass, when the entry was still absent per CritC1Kill's `entries=17 pass=16`, and this run). The assignment's 16/16 baseline set is a subset; every row passes.
- **Every real manifest recheck that passed at base still passes**: swept all 7 snapshot manifests × every listed id (round-23 S018/S029/S030/S031; round-24 S001–S015 + S032–S035; round-25 S036–S040; round-26 S041; round-28 S041/S042; round-29 S043/S044/S045; round-30 S046/S047/S041) under **both** the landed instrument and the freeze-copy base instrument: **37/37 exit 0 on both** — the new stem/anchor limbs reject nothing that base accepted, and base-passing set == current-passing set.
- Do-nothing control reproduced first-hand at freeze bytes (freeze copies hash-equal to base): A1 exit 1 with traceback and no named row; A2 exit 0 `pass=2`; B1 exit 0; B2 exit 0 `occurrences=2 anchor=MISSING` — identical to `c1-controls/before.txt` and `before-run-2.txt`. Control cannot meet the target.

## Findings by severity

1. **HIGH — receipt-blocking: the B2 counter/fixture pair is not an isolating measurement.** Committed `manifest-b2.json` (id `S045`, path `B2.txt`) trips the B1 stem limb before the occurrence limb; predicate's `reason=occurrence-not-unique` never appears; mutant-B2 does not flip. Smallest safe correction: (a) align the fixture (id `S045` + path `S045.txt` holding the double-occurrence bytes `55124b0e…`, or id `B2` + path `B2.txt`) — the first shape is the isolating one; (b) tighten the B2 kill clause from "lacks a failure reason" to "lacks `reason=occurrence-not-unique`"; (c) re-run counter B2 + the mutant-B2 flip. Land as an appended claims-correction file; do not edit the frozen `claims.json`.
2. **MEDIUM — instrument byte drift across the wave with stale poll evidence.** `source-recheck.py` moved through ≥4 digests (`9fe6a4a0` → `0b841d5d` → `72f411b0` → `33602a9d`); `digest-poll.log`'s last entry (18:50:40) pins `0b841d5d`, which is no longer on disk. My counter evidence is identical across the last two states and bound by pre/post hashes here, but any receipt citing an earlier digest describes bytes that no longer exist. Instruments are uncommitted; the committed-digest conjunct closes only at the post-commit recheck.
3. **LOW — harness row-filter is silent about malformed row ids.** `read_frontier` drops any row whose id cell fails `F\d+`; a fully renamed frontier would report `entries=0` → generic exit 1 with no named-row diagnostic. Outside the four counters' scope; no action claimed this round.

## Residual risk / verification gaps

- The regression clause is judged **as of my measured bytes** (`aa60b581…` + `33602a9d…`); if either instrument moves again before integration, this review does not cover the moved bytes. Final-state binding is `ExecPostCommitRecheck`'s owed job (harness + four counters + committed digests at the integration commit).
- I did not re-verify the round-30 C2 counters (F14 counts, registry rows 45→47) — outside this seat's assignment; the lane harness PASS F14 line and round-30 manifest rechecks measured above are the only C2-adjacent evidence I hold.
- Mutant receipts published under `wave1/CritC1Kill-attack/` were cross-checked for agreement, not re-run file-by-file; my §3 table is from my own mutants.

## Compliance

No write outside the lane repo except this report's path; no writes to `.ufo/state`, `MANIFEST.json`, git/jj state (read-only `git show`/`git status`/`git rev-parse` only), fleet root, sibling lanes, or `/home/vgpnk/Projects/shokuknow`. No live target contacted — every command ran local bytes. No tools installed (none needed). Answering route: operator's global role map; no model was passed.
