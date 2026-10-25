# CritC1Kill — C1 kill-rule attack review (round 30, wave 1)

Reviewer: CritC1Kill (L2 leaf). Scope: C1 (depth:verifiability, held 4).
All measurements run in the lane repo (cwd = `kasegi-shokunin`) against the
frozen fixtures. Bytes measured: live instruments at run time
`frontier-recheck-count.py` sha256 `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`,
`source-recheck.py` sha256 `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`
(both differ from the frozen base digests `c8a62888…` / `9fe6a4a0…` — the landed work).

## Verdict

Kill rule is **NOT fully robust**. A1, A2, B1 counters isolate their limbs and
the do-nothing control stays failing. **The B2 counter is structurally incapable
of exercising the occurrence limb**: the committed `manifest-b2.json` trips the
B1 stem check first, so the counter passes for the wrong reason and cannot detect
a build that omits the entire B2 occurrence check (proof: the claim's own
mutant-B2 does not flip on the committed fixture).

## 1. Counter command verification (exact commands from claims.json)

| Counter | Command (verbatim) | Measured result |
|---|---|---|
| A1 | `python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1; echo "a1_exit=$?"` | exit 1; stdout `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry` + `entries=1 pass=0 exit=1`; no traceback (stderr empty) |
| A2 | `... --root .ufo/waves/round-30/c1-controls/harness-root-a2; echo "a2_exit=$?"` | exit 1; stdout `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md` after two PASS rows; `entries=2 pass=2 exit=1` |
| B1 | `python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043; echo "b1_exit=$?"` | exit 1; stdout `S043:manifest MISMATCH reason=stem-mismatch` |
| B2 | `python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045; echo "b2_exit=$?"` | exit 1; stdout `S045:manifest MISMATCH reason=stem-mismatch` — **NOT reason=occurrence-not-unique** |

All four counters pass as executed (exit 1), so the claim's measurements are
true as stated. Finding is that B2's exit-1 is produced by the **B1 stem limb**,
not the B2 occurrence limb (see §4).

## 2. Do-nothing control (base bytes) — stays failing ✓

Ran the two freeze copies (digests `c8a62888…` / `9fe6a4a0…`, sha-matched to the
committed base) against the four fixtures. Reproduces `before.txt` /
`before-run-2.txt` exactly:

- A1 base: exit 1, `FileNotFoundError` traceback, **no** named-row marker (0 hits for `F98` in stdout/stderr).
- A2 base: exit 0, `entries=2 pass=2 exit=0` on duplicate target.
- B1 base: exit 0 (`S043:sha256 OK; Q1 OK` — stem mismatch passes).
- B2 base: exit 0 (`occurrences=2 anchor=MISSING`).

Control cannot meet the target — confirmed at base bytes.

## 3. Mutants flip exactly one limb — A1/A2/B1 ✓, B2 ✗

Mutants built from the live landed instruments (generator `wave1/CritC1Kill-attack/make-mutants.py`,
copies in `.../mutants/`), each removing exactly one new limb:

| Mutant | Limb dropped | Target (claim) | Measured | Flip? |
|---|---|---|---|---|
| mutant-A1 | isfile guard → `open()` crash restored | A1 exits without named-row marker | exit 1, `FileNotFoundError` traceback, 0× `F98` | ✓ |
| mutant-A2 | duplicate realpath detection + its fail_closed term | A2 exits 0 | exit 0, `entries=2 pass=2 exit=0`, no `DUPLICATE` line | ✓ |
| mutant-B1 | stem-mismatch branch | B1 exits 0 | exit 0 (`sha256 OK`, `Q1 OK normalized=markup-whitespace occurrences=1`) | ✓ |
| mutant-B2 | non-unique occurrence fail branch | B2 exits 0 | **exit 1 — `reason=stem-mismatch`** | ✗ |

The claimed mutant-B2 flip is FALSE on the committed fixture. The B2 fixture
cannot distinguish presence from absence of the occurrence limb.

## 4. Root cause: B2 fixture is self-inconsistent (id/path mismatch)

`manifest-b2.json`: id `S045`, path `B2.txt` (sha `55124b0e…`, verified = actual
`B2.txt` bytes; quote `vulnerability rating taxonomy crosswalk node` occurs
exactly 2× in `B2.txt`, double anchor). In `check_source()` the B1 stem check
(`Path(path).stem != source_id`) runs **before** sha256/quote logic:
`Path("B2.txt").stem == "B2" != "S045"` → early `return 1` with
`reason=stem-mismatch`. The occurrence limb is unreachable on this fixture.

Proof the limb itself is implemented correctly: a corrected isolating fixture
(stem OK — id `S045`, path `S045.txt`, file = same double-occurrence bytes, same
sha) makes the **live** instrument exit 1 with `S045:Q1 MISMATCH
reason=occurrence-not-unique`; the same corrected fixture makes mutant-B2 exit 0
with `occurrences=2 anchor=MISSING`. Limb exists and works; the committed
counter/fixture just never reaches it.

Regression-leg consequence: an implementation silently omitting the whole B2
occurrence branch passes **every** element of C1's kill rule — B2 counter (via
stem), A1/A2/B1 counters, and all real-manifest rechecks (`mutant-B2` with the
live instrument exits 0 on all 7 manifests: rounds 23–30, including S047's
multi-occurrence anchored quotes `occurrences=3 anchor=123-ok`, `occurrences=2
anchor=130-ok`).

## 5. Bypass attempt log (each tied to its counter command)

- **A1 hardcoded-printer simulation** → name: renamed row id `F98`→`F99` in a
  scratch root; live harness output names `F99` (`FAIL F99 knowledge/zz-missing.md
  … problems=missing-entry`, exit 1). The named-row marker is data-driven (row
  id parsed from the README), not hardcoded. A generic unconditional-fail printer
  would still satisfy A1, but is caught by the regression leg (harness must pass
  every admitted row of the real lane at final state).
- **A2 hardcoded-duplicate simulation** → failed: renamed F98/F97→F91/F92; live
  harness emits `DUPLICATE-ENTRY F91,F92 knowledge/dup-entry.md`. Also verified
  realpath canonicalization catches alias spellings (`knowledge/sub/../dup-entry.md`
  vs `knowledge/dup-entry.md` → still duplicate, exit 1).
- **Exit-code manipulation** → B: A1/A2/B1/B2 exit codes come from genuine
  fail-closed paths (verified by mutant flips and conditional probes). No
  synthetic exit-code route found.
- **B1 unconditional-fail printer** → failed: with stem OK (id `S045`, path
  `S045.txt`) and file present, live instrument exits 0 (`sha256 OK`, quote OK) —
  the `reason=stem-mismatch` emission is conditional on an actual stem mismatch.
- **Degenerate/stem-dodge fixture** → failed for B1: `Path(path).stem` cannot be
  made equal to id while the file differs (trailing slash stripped by `Path`;
  extension-bearing id forces mismatch). No dodge found.
- **B2 degenerate fixture (the real hole)** → succeeded: the committed B2
  fixture's id/path mismatch means the counter passes via B1, so removing the
  occurrence limb is invisible (§3–§4). This is the one successful "satisfy the
  counter without the claimed work" route.
- **Reusing unrelated entries (M29-4 shape)** → out of C1's four counters' scope:
  the A–D entry-level binds (round-24 limbs) still allow an entry to cite extra
  ids in its body and select them on its recheck line; that is pre-existing
  semantics and is not what the four counters measure. Flagged as observation, not
  a kill.
- **Minor robustness note**: `read_frontier` silently drops rows whose id fails
  `F\d+` (a renamed row `G01` vanished; `entries=0` → generic exit 1). Not one of
  the four counters; no action claimed.

## 6. Regression-leg measurements (kill-rule OR clause)

- Real-manifest rechecks: live `source-recheck.py` exits 0 on all seven snapshots
  (rounds 23–30), including round-30 S046/S047/S041. Base-passing rechecks
  preserved.
- Lane harness at measurement time: exit 1 (`entries=17 pass=16`), because C2's
  F14 entry `knowledge/japanese-severity-vocabulary-and-impact-model.md` is not
  yet on disk (mid-wave state — C2 not landed). The C1 regression leg can only be
  finally judged at the round's final state; as of this review it cannot yet be
  confirmed, and the current failure is attributable to C2 in-flight work, not to
  the C1 instruments.

## 7. Smallest safe correction

1. Fix `manifest-b2.json` so B1 passes and B2 is reachable — either
   - id `B2`, path `B2.txt` (keeps sha `55124b0e…` and the double-occurrence
     content), or
   - id `S045`, path `S045.txt` where `S045.txt` = the double-occurrence bytes
     (sha `55124b0e…`) — note this is a *new* capture file, not the existing q9
     `S045.txt` (which does not contain the quote) — then re-run counter B2 and
     the mutant-B2 flip (`mutant-B2` on the corrected fixture must exit 0).
2. Tighten the B2 kill-rule clause from "output lacks a failure reason" to
   "output lacks `reason=occurrence-not-unique`" (and correspondingly the A1/A2
   clauses already name F98/duplicate). Without this, any unrelated reason string
   would also satisfy the counter.
3. Re-run the full four-counter battery + the four mutant flips + regression legs
   at the round's final state once C2 has landed.

## Evidence artifacts

- `wave1/CritC1Kill-attack/` — per-counter outputs (`a1.out`, `a2.out`, `b1.out`,
  `b2.out`, stderr files), `digests-before.txt`, `lane-harness.out`, mutant
  copies, probe roots, generator script, digest sweep outputs.
- Baseline receipts cross-checked: `.ufo/waves/round-30/c1-controls/before.txt`,
  `before-run-2.txt`.
