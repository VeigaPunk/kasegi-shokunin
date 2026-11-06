# CriticClaims — kasegi round 79, attempt 1 (run-15 fresh start), wave 1

Seat: critic (attack only, read-only). Wave 1 of round 79 is **13 seats** (spec items count).
Freeze commit `9d0b1eb0709e47c3c6decc09138b5012a8968924` (base `d16d2124fd5262f5a8088aa598f1e628f897d3ab`);
lane HEAD measured at the freeze commit; frozen claims `.ufo/waves/round-79/claims.json`
(`frozen_at 2026-11-06T18:49:41Z`). C2 integration was landing in the worktree while this review ran
(`git status`: `M PROVINCE.md`, `M corpus/README.md`, `M corpus/SOURCES.md`,
`M corpus/instruments/knowledge-expected.txt`, `?? corpus/knowledge/osv-determineversion-cc-library-versioning.md`);
all freeze-tree measurements below were taken with `git show 9d0b1eb…:<path>` / `git grep 9d0b1eb…`, not the moving worktree.

Artefacts under attack (hashes re-derived, not trusted):

| artefact | sha256 |
|---|---|
| `.ufo/waves/round-79/c1/recheck-cwd-census.py` (candidate) | `eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f` (P2 ✓) |
| `.ufo/waves/round-79/c1/mutbat.py` (frozen counter) | `735d2336550850a0c72c6049e5d7ee1f92dd345332b624578a8b627bcfba3ea9` |
| `corpus/instruments/recheck-cwd-census.py` at freeze (base bytes) | `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` |
| `.ufo/waves/round-79/controls/c1-forgery-stub.py` | `dd5b192e2174f16f55706a64ba62bdfeef86c88aa7172733d58473df6c6f10cf` |
| `corpus/source-snapshots/round-79/S113.txt` | `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf` |

Scratch root `/fast/scratch/hyaku/kasegi-r79/CriticClaims` (TMPDIR passed explicitly; removed before yield).
Raw receipts: `.ufo/waves/round-79/w1/CriticClaims-receipts/`. No tool installed; no git/jj write; no lane-file edit.

---

## (a) Can a do-nothing or forged candidate reach either target under the frozen counters?

**Committed controls — reproduce exactly, rc included.**

```
$ python3 -B .ufo/waves/round-79/c1/mutbat.py --target <base bytes e666ae11> \
    --table .ufo/waves/round-79/c1/mutant-table.json --expect-cases 15 --work <scratch>
MUTBAT target_sha256=e666ae11…2a21a baseline=bad rows=19 killed=0 survived=0 dirty=1 notderived=18
rc=1
```
```
$ … --target .ufo/waves/round-79/controls/c1-forgery-stub.py …
MUTBAT target_sha256=dd5b192e…6f10cf baseline=ok rows=19 killed=0 survived=8 dirty=0 notderived=11
rc=1
```
Both match `controls/c1-donothing-r79.txt` and `controls/c1-forgery-r79.txt` field for field
(`killed/survived/dirty/notderived` and `rc`). The naive forgery is refused; the do-nothing base cannot reach either target.
C2's do-nothing receipt (`controls/c2-donothing-counters-r79.txt`) also holds: knowledge 92, frontier rows 54
(registry 112 in the pre-row control transcript; 113 at the freeze commit with S113 `queued`) — B1/B2/B3 unmet.

**But the counter is forgeable in class.** A forgery whose executed `selftest()` is only a self-integrity gate —
the real selftest body renamed `_dead_selftest()` and never called, every anchor left byte-intact so every row is derived —
prints its own FAIL line on any byte change and the green line on the untouched bytes:

```
$ python3 -B …/mutbat.py --target CriticClaims-receipts/F-selfhash-forgery.py …
MUTBAT target_sha256=c8bc3b1b…23205e baseline=ok rows=19 killed=19 survived=0 dirty=0 notderived=0
rc=0
```
(`F-selfhash-forgery.py`, sha256 `c8bc3b1bc7ad22b722d9cfaca684f1c11b54a4541a984a9d99317867e823205e`;
receipt `selfhash-forgery-run.txt`.) **No assertion is executed for any mutant**, yet P3's exact target string is met.
The committed forgery control (a print-stub replacement) does not enumerate this class; the counter cannot distinguish
"the mutated limb's assertion fired" from "the file's bytes changed".

**Verdict: holds for the two committed control receipts; breaks as a counter property.** P2 (the sha256 pin to the
frozen candidate) is the only thing that keeps such a forgery out of the landing — the 19/19 number itself is not proof
that the assertions are load-bearing. This is a routed defect, not a verdict change for the frozen candidate.

## (b) Does mutbat's KILLED rule accept a kill that is not an assertion?

**Yes, and the converse too — the classifier is a free-text rule.** `verdict()` is decided by the literal substring
`"Traceback"` and by `EXC_RE = re.compile(r"^selftest case=\S+ FAIL .*exception")` (`mutbat.py:40,56-64`):

```
Traceback+SyntaxError          verdict=DIRTY            (correct: a syntax-error mutant cannot fake a kill)
FAIL detail names exception    verdict=EXCEPTION-KILL
FAIL detail names KeyError     verdict=KILLED           ← runtime exception counts as an assertion kill
FAIL plain assertion           verdict=KILLED
```
(`CriticClaims-receipts/classifier-demo.txt`.) The same runtime-exception kill flips verdict on the class *name*: only
details containing the word `exception` are demoted. This is the r76 V-A defect (a NameError kill counted) returning
through a different string.

The frozen candidate demonstrates both directions in one row. `K-T1` removes the TMPDIR refusal; `main()` then raises
`FileNotFoundError`, which the case catches and prints as `stdout="exception=FileNotFoundError(…)"`
(candidate `:428`), so the genuine assertion failure (`ret13 != 2`) is classified **EXCEPTION-KILL** and, being tabled
`class:"assertion"`, is **not counted**:

```
MUTANT K-T1 verdict=EXCEPTION-KILL rc=1 fails=1 counted=no
MUTBAT target_sha256=eda49d32…091f2f baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0   rc=1
```
(`CriticClaims-receipts/p3-candidate-run.txt`, `mutants-p3/K-T1.out`.)

**P3 is therefore false at the frozen bytes**: expected `killed=19 survived=0 dirty=0 notderived=0`, exit 0; observed
`killed=18 … dirty=1`, exit 1. The claims' own kill rule — "…or EXCEPTION-KILL on an assertion-class row = NOT VERIFIED" —
fires. The table row is self-contradictory: `class:"assertion"` with `expect:"…(exception caught as ret=-99)"`.

The mirror attack proves the count is wording-driven, not assertion-driven: changing **only** the diagnostic string
`"exception=%r"` → `"err=%r"` at `:428` (no assertion touched) makes the frozen counter print
`killed=19 survived=0 dirty=0 notderived=0`, rc 0 (`CriticClaims-receipts/wording-variant-run.txt`,
`C-wording-err.py` sha256 `ac076450…1c40`). A one-word edit reaches the declared target; the declared target therefore
does not measure the property the claim states.

**Hang path:** `run_selftest` uses `subprocess.run(..., timeout=900)` (`mutbat.py:50`) with no `except` anywhere between
`battery` (`:86`, `:174`) and `main` (the only `try` in `main` wraps the table read). An out-of-table mutant that hangs
raises an uncaught `subprocess.TimeoutExpired`, aborting the whole battery with a traceback and **no MUTBAT line**
(code path read at `mutbat.py:50/86/174`; a 1 s `subprocess.run(timeout=1)` demo shows `TimeoutExpired` escaping as a
traceback, rc 1). A hang is not classified DIRTY; it destroys the run. A SyntaxError mutant
is correctly DIRTY (traceback), so it cannot fake a kill.

**Verdict: breaks** (the rule is a text rule; K-T1 is misclassified by the candidate's own wording, and an
exception-detail row can be counted or not by string choice). Impact: depth:verifiability / calibration.

## (c) Is the 19-row table a fair successor to the r78 eight? Is the K-X2 split a narrowing or a widening?

r78's table (`.ufo/waves/round-78/c1-mutant-transforms.md`) had 8 rows: K-M1…K-M5, K-X1, K-X2, K-M8 —
7 assertion + 1 exception (K-M3). r79 has 19: 18 tabled `assertion` + 1 `exception` (K-M3), effectively 17 assertion
kills + K-T1 (observed exception) + K-M3.

- All eight r78 ids survive with re-derived anchors; no r78 transform was dropped or weakened.
- r78 `K-X2` replaced the condition `clean_ok is True` with `True` at the check call. In the r79 candidate that
  expression moved inside `gate_consume_ok`; `K-X2a` applies the *same expression transform* inside the predicate
  (`return clean_ok is True and limb_log == [True]` → `return True and limb_log == [True]`) and is killed by
  `gate-predicates FAIL rows=17 bad=[1]` — the r78 survivor class is now killed **by an assertion**.
  `K-X2b` additionally replaces the whole call-site argument (`check("gate-consume", True,`) and is killed by
  `gate-wiring F1/F2/F3`.
- Therefore the split is a **widening**: the r78 transform survives verbatim as K-X2a and a second, stronger structural
  form is added. The 11 net-new rows track the new predicates/wiring scanner one-for-one.

Fairness is otherwise sound; the single table defect is K-T1's class column (above), which contradicts the row's own
`expect` text — not a difficulty narrowing.

**Verdict: holds (widening), with K-T1's class as the count-breaking defect.**

## (d) Is C1 honestly labelled nominal (QUALITY R58)? Is C2 a coverage move on uncovered ground?

**C1 — holds.** R58: "A lowest-axis claim must move a metric that the axis counter itself reads… labelled nominal and
its score is held, with the non-moving metric named" (`corpus/QUALITY.md:415`). The depth:verifiability metric is the
`resolve.py` citation census over `SKILL.md` + `corpus/**/*.md` (`SCORECARD.md:33` and the axis rows); the
`recheck-cwd-census.py` verdicts are not read by it. C1's only `.md` edits are the case count in two **pre-existing**
pin rows (`SKILL.md:982`, `corpus/instruments/README.md:354`, both currently `cases=6`), which adds no citation token.
The claim names the non-moving metric ("the scored citation census is not read by this counter") and holds 4. Honest.

**C2 — holds on ground, with a scope limit.** At the freeze tree: 92 knowledge entries; `git grep -i determineversion
9d0b1eb… -- corpus/knowledge/` → no hits (rc 1); `git grep -i 'file_hashes\|MD5'` → one hit in
`source-tree-loss-2026-09-28.md:172`, a digest string (`md5 ab25833e…`), not the determineversion clause; the eight
pinned quotes return **0/8** literal hits over the 92 base entries. F51 lists the endpoint only as listed-not-described
ground (the draft cites `corpus/knowledge/osv-post-v1-query-contract.md:75`), so the eight clauses are a new
endpoint/operation class — coverage, not a re-score of a held rule. The eight quotes are exact on their declared
snapshot lines (25, 41, 41, 55, 61, 62, 66, 85), occur once each, and are 7–22 words (all ≤25), verified by a plain
script over the committed bytes.

Limit (routed, not a mislabel): B0–B7 verify capture fidelity and admission bookkeeping, not the entry's clause prose.
An entry that pins the eight quotes with no claims would satisfy B0–B7. [INFERENCE from the predicate definitions;
a stub was not written into the lane.] The draft is not a stub: it states eight falsifiable rules with a Gate table.

**Verdict: holds; C1 nominal is honest, C2 is coverage on uncovered ground.**

## (e) Causal separability of C1 and C2

**Holds.** Disjoint write sets: C1 → `corpus/instruments/recheck-cwd-census.py` + the two pin rows; C2 → the new
entry, `corpus/SOURCES.md` S113 row, `corpus/instruments/knowledge-expected.txt`, `corpus/README.md` F55/coverage
rows, `PROVINCE.md` amendment. The in-flight integration diff touches only the C2 set.
The one measurement coupling is benign and dynamic: C1's P5 compares `entries` to `ls corpus/knowledge/*.md | wc -l`
at the landing tree, so it is conformant at 92 (C2 absent) or 93 (C2 landed); C2's B2 counts knowledge files and does
not read the C1 instrument. ExecC1RealTree already flags that P5 must be re-run at the landing commit if C2 lands —
a re-run, not an interdependence.

**Verdict: holds.**

## (f) Universal clauses a predicate's counter does not enumerate

1. **C1 statement, "every assertion-neutering-to-True transform on the gate checks (K-X2b, K-M8, K-W2, K-P2, K-C1, K-NP)"** —
   the list names 5 gate checks plus K-M8 (a non-gate `relabel-detection` check); `gate-regs` has **no row**. The
   constant-True form on `gate-regs` *is* killed structurally (`gate-wiring F1:gate-regs:475`), so the class is closed
   by the scanner for that form — but not enumerated by the 19 rows. The **input-constant** form is neither
   enumerated nor caught:
   `check("gate-consume", gate_consume_ok(True, limb_log), …)` — F2 passes (the predicate is called) and the selftest
   stays green (`B-consume-input-True-selftest.txt`: `cases=15 failures=0`). Composite with a real neuter,
   `clean_ok = not limb(out6, ret6)` + the constant input, also stays green (`E-input-neuter-plus-inversion-selftest.txt`):
   the case-6 RESULT assertion can be inverted while the selftest reports `failures=0`. Per the frozen kill rule these
   are routed findings (new transforms/composites), not verdict changes — but they falsify the statement's universal
   and violate §9 ("no universal clauses… unless the counting command enumerates the full set").
2. **"the equivalence class closed"** — no definition and no counter; unenumerable as written.
3. **C1 P7, "no string literal path under /tmp"** — the candidate's module docstring contains `/tmp` in prose (`:25`,
   "no path is hard-coded under /tmp"). A literal `grep '/tmp'` = 1, not 0; the intent holds but the predicate's
   enumeration must be anchored (e.g. a quote-anchored grep).
4. **C2 B6, "excluding the new entry"** — at freeze the literal count is 0/8 as claimed, but at the landing commit a
   plain `grep -F -l` over `corpus/knowledge/*.md` hits the new entry 8/8; the exclusion must be in the command for
   the value to be re-derivable with one command.
5. C2's "eight pinned clauses" and "a claimed clause not on its declared line" are fully enumerated (8 manifest quotes,
   each verified exact-on-line) — no defect. C1's "all nineteen" is enumerated by P3, and P3 is false (b).

**Verdict: breaks for C1's universal clause (surviving input-constant transform); wording defects in P7/B6.**

---

## Verdict summary

| attack | verdict | decisive evidence |
|---|---|---|
| (a) do-nothing / forgery | controls **hold**; counter **breaks** in class | base `killed=0` rc1, stub `killed=0 survived=8` rc1 reproduce; self-hash forgery `killed=19` rc0 with no assertion executed |
| (b) KILLED accepts non-assertion | **breaks** | K-T1 `EXCEPTION-KILL counted=no` from the candidate's own `exception=` wording; wording-only variant reaches 19/19; `KeyError` detail counts as KILLED; hang aborts the battery (uncaught `TimeoutExpired`) |
| (c) 19-row successor / K-X2 split | **holds** (widening) | r78 K-X2 preserved as K-X2a (killed by `gate-predicates bad=[1]`), K-X2b adds the call-site form; no r78 row dropped |
| (d) nominal / coverage labels | **holds** | R58 label names the non-moving census; C2 ground 0/8 literals, no `determineversion` in 92 entries, quotes exact-on-line |
| (e) C1/C2 separability | **holds** | disjoint write sets; P5 dynamic over the knowledge count |
| (f) universals vs enumeration | **breaks** (C1) | `gate_consume_ok(True, limb_log)` survives; `gate-regs` row absent; "equivalence class closed" uncounted; P7/B6 command forms |

**C1 is NOT VERIFIED at the frozen bytes**, by its own P3 and kill rule: `killed=18`, not 19. Everything else in C1's
predicate set that is verifiable pre-landing passes: P1 `selftest cases=15 failures=0` rc0; P2 sha `eda49d32…`; P4
`TMPDIR=/nonexistent-kasegi-r79 … --root <lane> --lane <lane>` → rc2, stderr `recheck-cwd: TMPDIR … is not a directory`,
0 `Traceback` on both streams; P7 exec surface one `subprocess.run(`, one `"bash", "-c"` (`:81`). P5 is ExecC1RealTree's
(92 entries pre-C2, 93 after); P6 is landing-only (pins currently `cases=6`).

**Smallest safe corrections (routed; frozen bytes are not edited):**
1. Do not land this candidate with a `killed=19` claim: land it and write C1 NOT VERIFIED, or re-freeze a successor with
   the repairs below.
2. Counter classifier: stop inferring the kill class from free text. Either the target prints a dedicated marker the
   harness owns, or the harness requires the FAIL line's case to be the row's `expect` case (the `expect` field is
   currently never read). Without this, a one-word diagnostic edit (C-wording-err) buys 19/19.
3. Table: `K-T1` is a caught-exception FAIL and must be classed `exception`, or the case must assert the refusal
   without routing the exception text into the detail; either way the class must match the observed verdict before
   freeze.
4. Add the consume-input transform (`gate_consume_ok(True, limb_log)`) as a row, or drop "every … transform" and
   "the equivalence class closed" from the statement (§9 universal rule).
5. Catch `subprocess.TimeoutExpired` in `run_selftest` and classify it DIRTY so a hang cannot abort the battery.
6. Make P7 and C2-B6 one-command-re-derivable (anchored `/tmp` grep; explicit `--exclude` of the new entry).
7. C2: re-run B3/B4/P5 at the landing commit after the in-flight integration settles; the predicates are otherwise met
   on the bytes checked here.

## Files written by this seat

- `.ufo/waves/round-79/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-79/w1/CriticClaims-receipts/` — `p3-candidate-run.txt`, `p3-rc.txt`, `mutants-p3/` (19 verdict outputs),
  `base-donothing-run.txt`, `forgery-control-run.txt`, `wording-variant-run.txt`, `selfhash-forgery-run.txt`,
  `classifier-demo.txt`, `A-gate-regs-True-selftest.txt`, `B-consume-input-True-selftest.txt`,
  `E-input-neuter-plus-inversion-selftest.txt`, `p4.out`, `p4.err`, the four variant sources, `base-bytes.py`,
  `variant-hashes.txt`, `mutants-wording/`.

No lane file outside `.ufo/waves/round-79/w1/` was created or modified; no git/jj write was issued; no tool was
installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r79/CriticClaims` removed before yield.
