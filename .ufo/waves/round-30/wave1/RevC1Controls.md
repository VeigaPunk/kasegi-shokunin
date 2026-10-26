# RevC1Controls — C1 fixture matrix audit (round 30, wave 1)

Seat: `RevC1Controls-2` (reviewer, L2 leaf). Scope: the four C1 fixtures in `.ufo/waves/round-30/c1-controls/` — one-limb isolation, base-vs-landed runs, do-nothing control, mutant single-flip. Every number below is my own run at the lane root (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`), not an import; sibling receipts are cited only as convergence.

## 0. Bytes measured (sha256, stable across this audit — hashed at start and re-hashed after all runs)

| object | sha256 | note |
|---|---|---|
| landed `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | working tree |
| landed `corpus/instruments/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | working tree |
| base bytes `git show 3c557354:…` (both instruments) | `c8a62888…` / `9fe6a4a0…` | byte-equal to `git show a94871315:…` and to `mutants/freeze-*.py` — "base" is identical at both cited commits |
| mutants a1/a2/b1/b2 | `013dd1e5…` / `5028f09e…` / `99073b11…` / `e12c8c75…` | single-hunk removals, verified by `diff` (a1: `77a78,79` inverse; a2: `203c203,214` inverse; b1: `122a123,126` inverse; b2: `189a190,200` inverse) |
| all 7 fixture files (q9/*, both harness-root READMEs, dup-entry.md) | FROZEN-OK | byte-identical to claims-freeze commit `3c557354` |

Digest-drift note: `mutants/digest-poll.log` row 2 (`0b841d5d…`, 15:50:40Z) is a transient pre-settlement digest; `source-recheck.py` settled at `33602a9d…` (mtime 15:51:26Z). Every receipt I audited (controls, mutants, ExecMutantsC1) pins the settled bytes; nothing cites `0b841d5d` as final.

## 1. Fixture isolation — does each fixture exercise exactly one limb?

- **A1** (`harness-root-a1`): one admitted row `F98 → knowledge/zz-missing.md` (file absent). Single row ⇒ duplicate limb (F) impossible; missing file ⇒ no recheck line is ever read or executed. Only the E limb (named-row missing-entry) can fire. **Isolating.**
- **A2** (`harness-root-a2`): two admitted rows `F98`/`F97 → knowledge/dup-entry.md`; the entry is contract-clean — under landed bytes each row prints `PASS … exit=0` with no problems, and under base bytes I ran the row's recheck target directly (`S003:sha256 OK / S003:Q1 OK occurrences=1`, exit 0). So the landed run's `exit=1` is attributable **solely** to the F limb (`passed == len(records)`; only `duplicate is not None` closes it). **Isolating.**
- **B1** (`q9/manifest-b1.json`): id `S043`, path `S045.txt` (stem mismatch, intentional); otherwise clean — under base bytes: `S043:sha256 OK`, quote `normalized=markup-whitespace occurrences=1` (I verified the normalized quote occurs exactly 1× in `q9/S045.txt`, sha `f583a396…` matching the pin). Only the stem limb fails. **Isolating.**
- **B2** (`q9/manifest-b2.json`): id `S045`, path `B2.txt`, quote occurs exactly 2×, no anchor — but `Path("B2.txt").stem == "B2" != "S045"`, so the **B1 stem limb fires first** and the occurrence limb is unreachable. **NOT isolating** — see Finding 1.

## 2. Measured matrix (first-hand runs)

### 2a. Do-nothing control — base bytes (freeze copies, hash-equal to `3c557354` and `a94871315`)

| probe | exit | output | meets target? |
|---|---|---|---|
| A1 | 1 | uncaught `FileNotFoundError` traceback at `entry_contract` `open(full…)`; grep for `F98` in stdout+stderr: **0 lines** | NO — target needs a named-row message, not a traceback |
| A2 | 0 | `PASS F98 / PASS F97 / entries=2 pass=2 exit=0` | NO — duplicate target passes |
| B1 | 0 | `S043:sha256 OK / S043:Q1 OK normalized=markup-whitespace occurrences=1` | NO |
| B2 | 0 | `S045:sha256 OK / S045:Q1 OK occurrences=2 anchor=MISSING` | NO |

Reproduces `c1-controls/before.txt` and `before-run-2.txt` line-for-line. **The receipts are genuine and the control cannot meet any of the four targets.**

### 2b. Landed bytes

| probe | exit | key output | verdict |
|---|---|---|---|
| A1 | 1 | `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry` / `entries=1 pass=0 exit=1`, no traceback | ✓ named row, kill-rule A1 clause met |
| A2 | 1 | both rows `PASS` + `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md` | ✓ names duplicate rows and entry |
| B1 | 1 | `S043:manifest MISMATCH reason=stem-mismatch` | ✓ |
| B2 | 1 | `S045:manifest MISMATCH reason=stem-mismatch` | ✗ wrong reason — predicate says `reason=occurrence-not-unique`; the stem limb answers instead |

### 2c. Mutants — own limb and cross cells (each cell run by me)

| mutant | on A1 | on A2 | on B1 | on B2 (committed q9) | on B2′ (corrected `b2iso/`) | flips exactly one? |
|---|---|---|---|---|---|---|
| mutant-a1 | **FLIP**: exit 1 traceback, zero `F98` lines | no flip: still `DUPLICATE-ENTRY…exit=1` | n/a (B commands never invoke the frontier harness) | n/a | n/a | ✓ |
| mutant-a2 | no flip: still `FAIL F98 … problems=missing-entry` | **FLIP**: exit 0, `pass=2` | n/a | n/a | n/a | ✓ |
| mutant-b1 | n/a | n/a | **FLIP**: exit 0 | reason-only change (`stem-mismatch`→`occurrence-not-unique`), exit stays 1 — **no flip** | no flip: exit 1 | ✓ (B1 only) |
| mutant-b2 | n/a | n/a | no flip: still exit 1 `stem-mismatch` | **NO FLIP**: still exit 1 `stem-mismatch` | **FLIP**: exit 0 `occurrences=2 anchor=MISSING` | ✗ on committed fixture / ✓ on corrected fixture |

Cross-effects of the source-recheck mutants on the A fixtures are structurally excluded: the A2 row's recheck line invokes the lane instrument by absolute path, and A1 never reaches a subprocess; I additionally confirmed A2's row outcome is generation-insensitive (exit 0 under both base and landed source-recheck).

### 2d. Kill-rule non-regression limb (real corpus)

- Landed harness on the real lane: **`entries=17 pass=17 exit=0`** (F01–F14, incl. F14 `ids=S041,S046,S047`) — every real recheck that passed at base still passes; no missing/duplicate regression.
- Landed `source-recheck.py --selftest`: `selftest cases=9 failures=0`, exit 0 (clean/corrupt/missing-source/missing-manifest/stem-mismatch/double-occurrence/double-anchored/out-of-range/broken).

## 3. Findings by severity

### F1 — HIGH (receipt-blocking for the B2 clause only): committed B2 fixture is not discriminating
`q9/manifest-b2.json` (id `S045`, path `B2.txt`, frozen sha `3a13e5c3…`) trips the B1 stem limb before the occurrence limb under landed bytes. Measured consequences: (a) the frozen counter command emits `reason=stem-mismatch`, never the predicate's `reason=occurrence-not-unique`; (b) claims' mutants clause "mutant-B2 … must make B2 exit 0" is **false as measured** (exit 1); (c) worst case: an implementation deleting the entire B2 occurrence branch passes **every** element of C1's kill rule as written — B2's clause only demands "a failure reason", which the stem limb supplies. The limb itself is load-bearing and fails closed exactly as claimed once the stem matches: on the same-stem isolation fixture `mutants/b2iso/` (manifest `0180394b…`, capture `55124b0e…` = the `B2.txt` bytes renamed `S045.txt`), landed → exit 1 `reason=occurrence-not-unique`; mutant-b2 → exit 0; base → exit 0; mutant-b1 → exit 1. **Correction (appended claims-correction file; `claims.json` stays frozen): adopt the same-stem fixture shape for the B2 counter (id `S045`, path `S045.txt`, double-occurrence capture `55124b0e…`) and tighten the B2 kill clause from "lacks a failure reason" to "lacks `reason=occurrence-not-unique`"; then re-run counter B2 and the mutant-B2 flip.** Converges independently with `ExecMutantsC1.md` §4, `MutC1B2.md`, `RevC1Instrument.md` (HIGH), `CritC1Kill.md`.

### F2 — LOW (fixture hygiene, no effect on this round's conclusions)
`harness-root-a2/corpus/knowledge/dup-entry.md` embeds the lane instrument by absolute path in its `recheck:` line, so the base-bytes A2 control executed the **landed** source-recheck inside the row subprocesses (only the frontier harness was base bytes). Immaterial here — I verified the row exits 0 under both instrument generations — but future fixtures should vendor the row instrument (or pin a digest) so "base bytes" is closure-complete.

### F3 — INFO
`digest-poll.log` row 2 records a transient landed digest `0b841d5d…` (superseded within a minute by settled `33602a9d…`, M29-6-style drift). All audited receipts pin settled bytes; no action beyond the note in §0.

## 4. Verdict

- **A1, A2, B1 fixtures: VALID.** Each isolates exactly one limb, is discriminating (flips under exactly its own mutant, including both cross-cells), and the control fails all three targets for the right reason. Reproduces the committed receipts byte-for-byte.
- **Do-nothing control: CONFIRMED unable to meet any target** (A1 exit 1 but traceback without the named row; A2/B1/B2 exit 0) at bytes identical across `a94871315` and `3c557354`.
- **Non-regression limb: HELD** (real lane 17/17 under landed bytes; selftest 9/9).
- **B2 fixture as committed: NOT discriminating — flag and block the B2 clause** until the appended claims correction lands (same-stem fixture + tightened clause). No instrument defect: the occurrence limb is proven by the in-wave isolation fixture. No other fixture flagged.

## 5. Verification log (all commands run at lane root, 2026-10-25)

Base/landed/mutant/cross/b2iso cells per §2 (commands = frozen counter-command paths, with the instrument swapped for freeze/mutant copies); `git show <commit>:<instrument> | sha256sum` for base digests; `sha256sum` before and after all runs (identical); fixture-vs-freeze `git show | sha256sum` comparisons (7/7 FROZEN-OK); `diff mutant-*.py <landed>` single-hunk confirmation (4/4); real-lane harness and `--selftest` per §2d. No tool installed or upgraded (none needed). Writes: this report only.
