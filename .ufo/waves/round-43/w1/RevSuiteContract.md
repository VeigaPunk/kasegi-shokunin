# RevSuiteContract — review of `ExecSuiteSkeleton.r43-closure.sh` against the r42 harness and the recorded conventions

Seat: `RevSuiteContract` (reviewer, leaf, receipt-only). Round 43, wave 1. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Judged on: `depth:verifiability`, `coverage`. I wrote no lane file except this receipt; no deliverable file (receiver-only item) so no line/sha pair to record here.

## 0. Artifacts under review

| artifact | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecSuiteSkeleton.r43-closure.sh` (reviewed bytes, frozen copy in my scratch) | 2339 | `5a38d32c159c563e369fc18fbd1d80e8da5531686202f4082b2493201b2b1fce` |
| `corpus/instruments/r42-closure.sh` (proven harness, reference) | 2186 | `fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7f8df7f6d6b` |

Convention sources: `ScoutInstrumentInventory.md` (27538 bytes, `§1` shape, `§1.5` selftest grammar, `§1.6` cells, `§2` carried conventions, `§4` `/tmp` class), `ExecNegCtlReceipt.spec.txt` ("ROUND-43 RECEIPT CONTRACT (v3) — normative grammar for K8", landed 14:33), and `.ufo/waves/round-42/wave1/ExecJ8Receipt.spec.txt` + `ExecSuiteCore.md` (the r42 harness records).

Method: exact-text diff of the two committed scripts (`diff -u`), then execution of the reviewed bytes at base and at the round-41 head with `TMPDIR` and `--work`/`--scratch-root` bound to my scratch. No `lsp` device exists in my toolset, so callers/definitions were checked by exact-token diff over both scripts, not by a semantic index; that is a recorded limitation, not a semantic proof.

## 1. Verified faithful to the r42 harness (measured, not inferred)

Commands run with `S=/fast/scratch/hyaku/kasegi-r43/RevSuiteContract`, `final.sh` = the reviewed bytes:

```
$ bash final.sh                       -> two stderr lines, exit 2
r43-closure: a plain run is refused (export mode only)
r43-closure: usage: r43-closure.sh --export-ref <hash> [options]
$ bash final.sh --export-ref          -> r43-closure: --export-ref needs a value ; exit 2
$ TMPDIR= bash final.sh --export-ref deadbeef… (no --work/--scratch-root)
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1 ; exit 1
$ git log -1 --format='%ct %cI' ab98fac9… -> 1793204872 2026-10-28T13:27:52-03:00 ; run-utc=2026-10-28T16:27:52Z
$ bash final.sh --export-ref ab98fac9… --work $S/fA/w --scratch-root $S/fA --receipt-out $S/fA/receipt.txt
  -> 19 payload lines K1..K19 numeric order, closed=13/19 exit=1, exit 1, open set = K14 K15 K16 K17 K18 K19 only
$ bash final.sh --selftest --export-ref ab98fac9… -> 19 graded lines + summary, selftest cases=19 failures=6, exit 1
$ bash final.sh --export-ref 1f74646… -> closed=5/19 exit=1
$ diff -q <(head -25 $S/fA/receipt.txt) $S/A.out -> identical ; wc -l $S/fA/receipt.txt -> 45
```

* Export root: `git -C <lane> archive <resolved> | tar -x -C "$WORK/export"` after `rm -rf`, `$WORK` defaulting to `<scratch>/r43-<ref12>/work`; ref resolved with `rev-parse --verify --quiet "${EXPORT_REF}^{commit}"` (final L85; export L119-L126) — identical mechanism to r42 L68, L74-L92.
* `run-utc` is the ref's committer instant, not a wall clock (matches `%ct` above).
* Five header lines, one payload line per check in numeric order, `closed=<n>/19 exit=<0|1>`; exit 0 only at 19/19.
* `--receipt-out` is one unedited tee: **45 lines, and lines 1-25 are byte-identical to the run's stdout** (measured with `diff -q`); order header/payload/closed/selftest/summary.
* `--selftest` stdout is the graded block only (20 lines: 19 cases + summary).
* `--leaf`: `K9 payload=…deferred…closed=0`, `K10 …fixture=skipped closed=0`, tally `closed=11/19 exit=1`, and no receipt written even with `--receipt-out` (measured).
* **Carried checks are genuinely carried.** At base, K1-K7, K9, K11-K13 payload strings are byte-identical to the r42 suite's J1-J13 at the same export; K8 differs only in the receipt path/source/`diff` fact and the `18/18` denominator (19−1); K10 differs only `13`→`19`. Measured by parsing both transcripts:
  `SAME J1/K1 … SAME J7/K7, DIFF J8/K8 (expected), SAME J9/K9, DIFF J10/K10 (expected), SAME J11/K11 … SAME J13/K13`.
* Constants that must **not** move are correctly held: `ROUND=42`, `DECLARED_REL=.ufo/waves/round-42/declared-blocks.txt`, `PRIOR_RECEIPT_REL=…round-41…`, `BASE_REF=5053a7f…`, `DENSITY_SHA` (final L168-L180). Moving them as `ScoutInstrumentInventory` §1 suggests ("round-scoped constants that must move") would make K1/K4 red at Y and destroy the frozen base figure (13 carried closed); the deliverable's choice is the one consistent with the carried-payload identity above. The scout contract is wrong on that point; do not adopt it.
* `-h` prints the comment block only; it now stops before code (r42 L40 `sed -n '2,30p'` leaked `set -uo pipefail`, which the scout measured; final L46 uses `2,32p` and the last printed line is `in --selftest mode); 1 when any is open; 2 on a usage error.`).
* No `${TMPDIR:-/tmp}` fallback remains: final L91-L104 uses the `--work` parent, then `TMPDIR`, else exit 2. This closes the scout's `§4` defect class for this instrument.

## 2. Divergences that change semantics (r42 line → r43 line, effect, judgment)

| # | dimension | r42 | r43 (reviewed bytes) | effect | judgment |
|---|---|---|---|---|---|
| S1 | selftest grammar | L1422-L1424 `^selftest case=(J\d+) mutants=(\d+)/(\d+) positive=(pass\|fail) payload-match=([01]) verdict=(pass\|fail)$`; emitted L2088-L2092 | L1458-L1459 `^selftest case=(K\d+) positive=(pass\|fail) mutants=(\d+)/(\d+) verdict=(pass\|fail)$`; emitted L2209-L2210 | field order swapped and the `payload-match` cell **removed from the line** | **Not cosmetic.** The verdict predicate still folds payload identity (`pm == 1`, L2205-L2208), so no case is weakened, but the machine-readable bit is gone and an r42-shaped consumer parses **zero** graded lines. It also contradicts the recorded round-43 contract of record (`ExecNegCtlReceipt.spec.txt` §5 mandates exactly the r42 order *with* `payload-match=<0\|1>`). Either the suite or the contract must move; shipping both makes the receipt's own selftest block non-conforming to the contract it is supposed to satisfy. |
| S2 | selftest verdict floor | L2086 `(total == 0 or good == total)` | L2205-L2208 `total >= 1 and good == total` | a case with an empty battery can no longer pass | **Strengthening**, and it is what the scout §1.5 and the v3 contract §5(b) require. Keep. |
| S3 | K8 receipt subject | L136 `…/round-42/final-gates/all-gates.txt`; fallback root `…/round-42` L1498 | L171 `…/round-43/final-gates/all-gates.txt`; fallback root `…/round-43` L1533 | K8 grades the round-43 receipt | **Required** (otherwise no ref can reach 19/19); K1-K13 keep grading the round-42 closure, which is what "carried" means here. |
| S4 | K8 `digest` fact | L1606 `bool(now) and info["suite"] == now` | L1662 `info["suite"] == (now or "none")` | accepts `suite-sha256=none` only when the export carries no suite | **Safe but semantic**: the `none` branch is unreachable whenever the suite is present (a forged `none` against a present suite still reds). Needed for the base probe; v3 §2 says a *receipt* line 3 is 64 hex, so this is a canonical-mode-only relaxation. |
| S5 | K8 `closed-line` fact | L1626 `info["closed"] == (N,N,0)` | L1682-L1691: canonical mode accepts `closed == derived_closed(info)`; committed mode keeps `(N,N,0) and derived == info["closed"]` | a receiptless probe is graded on "the tally agrees with its own lines", not "claims full closure" | **Required** for the frozen base figure (without it K8 is red at base and the base tally would be 12/19). Still catches an inflated tally (derived ≠ claimed). |
| S6 | K9 dependent reds | L1703-L1704 `(J1,J2,J3,J4,J8,J11)` | L1759-L1761 `(K1,K2,K3,K4,K8,K11,K14..K19)` | the two nested controls accept a child whose tree-reds are the new narrative checks | **Required** by the frozen base figure: at base K1-K13 are all closed (measured, `closed=13/19` with only K14-K19 open), so the r42 set yields zero tree-reds and K9 would red, breaking "exactly K14-K19 open". It contradicts `ScoutInstrumentInventory` §1.6 verbatim ("at least two reds among K1, K2, K3, K4, K8, K11"); the scout's rule is unsatisfiable at base in r43. Caveat: while K14-K19 are stubs, K9's base greenness is *entailed by the stubs* and proves nothing (see F1). |
| S7 | scratch root default | L74-L76 `SCRATCH_ROOT="${TMPDIR:-/tmp}"` | L91-L104 work-parent → `TMPDIR` → exit 2 | no write root can ever be literal `/tmp`; with both `--work` and `TMPDIR` given, the work parent wins | **Improvement**, matches the scout §4 class. Behavioural but not weakening. |
| S8 | lane containment | none; `WORK` accepted anywhere | L111-L118 realpath `$WORK` and refuse `work` under the lane with exit 2 | a work tree inside the lane is refused | **Improvement**, but see F3: the `mkdir` precedes the guard, and only `WORK` is guarded. |
| S9 | `--only` | absent | L56, L70-L78, L2266-L2281: `--only K<n>` for K1..K7, K11..K19 (K8/K9/K10 refused exit 2); prints `only=K<n> closed=<0\|1>/1 exit=<0\|1>` or `selftest cases=1 failures=<k>` | a new invocation surface outside the frozen counting commands | **Not a forgery surface** (it can never print `closed=19/19`, and it writes no receipt), but it is not in the frozen `counting_commands` and must never be quoted as suite evidence; its `selftest cases=1` summary uses the same word as the real summary. |
| S10 | K8 forgery battery | L1534-L1582: six classes (payload value, closed bit, tally, summary, selftest verdict, run-utc) | L1589-L1634: same six, ids renamed, v1 payload text `forged-value,r43` | unchanged | **Weaker than the round-43 contract of record**: `ExecNegCtlReceipt.spec.txt` §7 defines **eight** classes and requires `composed-of-two-runs`, `summary-only`, `nonexistent-ref`, `foreign-ref` (with `tree-bind`), `future-dated` (`not-future`), and `selftest-match` in the bundle. Verified absent from the reviewed bytes: `grep -n 'one-run\|composed\|not-future\|tree-bind\|selftest-match\|summary-only\|nonexistent-ref\|foreign-ref'` → no hits; `grep -c 'out.append(rejects'` → 6. |
| S11 | K8 bundle cells | L1641-L1685: `receipt,source,sentinel,lines,ref,digest,time-basis,utc,ancestor,diff,run-lines,selftest-lines,verdicts,summary,closed-line,no-stray,payload-match,forged,payload-match=<m>/<n>,forged=<k>/6` | same, ids renamed | carries `source=canonical\|committed` and `receipt=(canonical)` | **Contradicts v3 §6 explicitly**: "the constant receipt path (never `(canonical)`)" and "no `source=` cell", because the source label flips when the receipt lands (the recorded r41 bootstrap defect). At base the reviewed bytes print `receipt=(canonical),source=canonical,…` (measured). This is the one divergence I would not accept silently: it re-introduces a defect the contract was written to prevent. |

## 3. Cosmetic divergences (no semantic change)

* `J`→`K` in ids, headers, docstrings; `r42`→`r43` in the program name, messages, `SUITE_REL`, `RECEIPT_REL`, `SUITE_SCRATCH`, and the `R42_*`→`R43_*` env prefix; fixture directories `j5-fixture`→`k5-fixture`, `j6`→`k6`, `j7`→`k7`, replay dirs `j1..j4`→`k1..k4`; canary token `CANARY-R42-7f3a91`→`CANARY-R43-7f3a91`.
* `usage()` range `2,30`→`2,32` with a longer header; the off-by-one that leaked `set -uo pipefail` is fixed.
* `K2`'s ten `BOUNDARY_PROBES` still carry the literal `closed=13/13` / `failures=6` / `cases=13` probe text — correct: those are tokenizer probes, not the round's tally (scout §1.6 agrees).
* `DETERMINISTIC` rewritten as "all but K8" (L166) — same set the r42 list had (K9 included), now expressed so it tracks `NCHECKS`; K8's denominator is `18/18` as the scout predicted.
* `PREV_ROUND=41` is still used only for the pre-round scan (L472), not in any payload cell.

## 4. Findings, by severity

**F1 (high, state — not repairable in this file). K14-K19 are stubs, so C1 cannot be satisfied and the base red is vacuous.** `LIMB_STUB = ("stub", False)` (L1802); `check_k14..check_k19` return it (L1805-L1826). Measured: base prints `K14..K19 payload=stub closed=0` and the selftest prints `selftest case=K14 positive=fail mutants=0/0 verdict=fail` (…K19), `failures=6`. The frozen kill rule requires each new check to *see its own committed defect* at base; a stub is closed=0 for the wrong reason and proves nothing. It also means K9's base greenness rests on stub reds (S6). The L1 must not read `closed=13/19` as evidence that the six new checks work, and the receipt must say the six limbs were not exercised. The deliverable's own comment (L1793-L1799) says exactly this; the risk is that the number gets quoted as a result.

**F2 (high, interface). The six limb deliverables do not fit the seam.** The seam is a Python `check_k<n>(_tree) -> (payload, ok)` plus `limb_mutants(_check_id, _root)` (L1829-L1837, documented in `ExecSuiteSkeleton.usage.txt` "LIMB INTEGRATION"). The landed K19 limb is a **bash** function `check_k19 <export-root> [<commit-utc>]` printing a complete line `K19 payload=freeze=…,order=…,sha=… closed=<0|1>` (`ExecK19Freeze.sh` L1-L40; transcript lines 43-97). Consequences: (a) the bodies must be ported to Python, not dropped in; (b) a `source`-and-parse adapter would emit `K19 payload=K19 payload=… closed=1 closed=<n>` (double prefix) and would lose the two-argument form's commit-utc; (c) `limb_mutants` has no counterpart in the limb. The L1 needs one owner to port all six consistently, and the port must preserve each limb's measured base-red.

**F3 (medium). The lane-containment guard runs after the write, and covers only one of the two roots.** Measured: `--work <lane>/.ufo/tmpwork …` is refused with exit 2 but the directory was created first (`mkdir -p -- "$WORK"` at L111 precedes the realpath guard at L113-L118). And although the header says "both the work tree and the scratch root must resolve outside the lane" (L12), `--scratch-root <lane>/.ufo/scratchprobe` was **accepted** and the run created `<lane>/.ufo/scratchprobe/r43-ab98fac9dce8/`. I removed both probe directories immediately (`rm -rf -- .ufo/scratchprobe .ufo/tmpwork`; `ls` confirms absent). The suite therefore can write inside the lane on a caller's flag and on its own refusal path — the exact scratch-discipline class the round is closing. Fix: resolve/validate both roots before any `mkdir`, or refuse a lane-internal scratch root too.

**F4 (medium). `check_k8` receives the live selftest and ignores it.** `def check_k8(tree, payloads, selftest_lines, summary, provisional)` (L1636) never reads `selftest_lines` or `summary`; in canonical mode it builds `selftest cases=19 failures=0` unconditionally (L1643-L1644). Measured instance: at base, run mode prints `K8 … closed=1` while `--selftest` at the same ref reports `failures=6`. So at a receiptless ref the run tally can be 19/19 with a failing selftest. This cannot survive into Y (the committed receipt's `summary` and `verdicts` facts are strict, L1650-L1652), but it means the J-side green is not a statement about the live battery. Inherited from r42 (same dead parameters there); worth fixing while the seam is open.

**F5 (low, latent fail-open).** `run_lines_from` defaults a missing id to `("pending", True)` (L1475) and the tally defaults to `("", True)` (L2333). Today every id is populated (`CHEAP` = K1-K7,K11-K13 + `LIMB_SLOTS`, L2247-L2248; `--leaf` sets K9/K10), so it is unreachable. A future slot dropped from `CHEAP` would print `payload=pending closed=1` and inflate the tally. Fail-closed (`False`) costs nothing.

**F6 (low, contract).** `ref-not-found` prints `closed=0 exit=1` (L81 lane form, L87 ref form), carried from r42 L64/L70. v3 §11 says the red carries "NO `closed=<n>/<m>` tally line". No denominator is present, so no tally regex matches; it is compliant by the letter and ambiguous by the look. Dropping the token removes the argument.

## 5. Integration state I observed (out of my write scope; for the L1)

The lane already carries a **different** suite and a non-green receipt; the reviewed deliverable is not what is in the tree:

```
corpus/instruments/r43-closure.sh           471478efc762f53d93118079fd906dc224e5e6d5ceea4dc769fa989db3fad758  511 lines (clean at 0a24364)
git cat-file -p 6c360f4:corpus/instruments/r43-closure.sh | sha256sum -> 0e782d5e3208a82b60880a53937d61d9b66293417ba7e3ce89b8437ffbe9946d  (511 lines)
.ufo/waves/round-43/final-gates/all-gates.txt: 39 lines, export-ref=6c360f4c…, suite-sha256=0e782d5e…, closed=10/19 exit=1, selftest cases=19 failures=9
```

That receipt is not the 45-line shape, its graded lines read `selftest case=K1 positive=fail mutants=carried:0 verdict=fail` — a **third** grammar that matches neither r42's nor the reviewed deliverable's `SELFTEST_RX` (`mutants=(\d+)/(\d+)`) nor v3 §5 — and its K8 line is `source=absent,header=0,…,forged=0/0 … closed=0`. C1 requires `closed=19/19 exit=0` and `selftest cases=19 failures=0`; the landed receipt satisfies neither, and a suite whose K10 requires 19 well-formed graded lines would count that block as 0. Three implementations currently define three K8/selftest grammars; one of them must be declared canonical before Y, and it should be the v3 contract, not whichever file happens to land.

## 6. Residual risk and verification gaps

* All measurements are at base `ab98fac9…` and the round-41 head `1f74646…`; **no Y exists**, so `closed=19/19 exit=0` and a *committed*-receipt K8 (`source=committed`, `diff`, `ancestor`, strict `summary`/`verdicts`) are untested here. The writer's 45-line tee and its first-25-line identity to stdout are measured; the K8 committed path is not.
* I did not run the reviewed bytes twice at base for byte-identical output (determinism). Two runs at base on two byte-different snapshots (pre- and post-K8-synth fix) agreed on every payload except the K8 fix, which is not the same as a double run of the final.
* K8's `selftest_lines`/`summary` dead parameters (F4) mean K8 grades a synthetic block at a receiptless ref; the Y-side gate is real, the J-side claim is not.
* `--only` output is not covered by any frozen counting command; do not cite it.
* No language server in my toolset: caller/definition checks are exact-text, not semantic. A grep hit or miss here is evidence about bytes, not about reachability.

## 7. Housekeeping

Scratch `S=/fast/scratch/hyaku/kasegi-r43/RevSuiteContract`, removed after this receipt was written; `TMPDIR` bound to it for every run; no writes outside `S` except the two probe directories the suite itself created inside the lane (F3), removed immediately; no tool installed (none needed), no network fetch, no `pacman`, no mutating git command (only `log`, `cat-file`, `archive`, `rev-parse`, `status --porcelain`); `~/.omp/agent/config.yml` and `mcp.json` untouched; no fleet-root or sibling-lane writes.
