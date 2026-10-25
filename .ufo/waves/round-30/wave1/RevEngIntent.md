# RevEngIntent — C1 target intent reconstruction and fix verification (round 30 wave 1)

Seat: `RevEngIntent` (revenger, L2 leaf). Mandate: reconstruct the intent behind C1's four
limbs (A1/A2/B1/B2), trace each to the recorded incident it fixes, verify the fixes against the
original failure modes by replaying the original repros, and report residue gaps as findings —
**without editing any production file**.

Measurement discipline: every claim below was re-run by me at labelled bytes. Instrument digests:
`frontier-recheck-count.py` base `c8a62888…` (freeze copy, matches claims freeze) / landed
`aa60b581…`; `source-recheck.py` base `9fe6a4a0…` / landed `33602a9d…`. All runs local, no live
target contacted (QUALITY Q6). No tool installed; no pacman attempted. No git/jj mutation; only
working-tree reads plus scratch fixtures under `.ufo/waves/round-30/wave1/RevEngIntent-scratch/`
(lane-internal wave evidence).

## 1. What C1's targets are (from the frozen predicate)

| Limb | Frozen predicate clause | What the instrument must do |
|---|---|---|
| A1 | a frontier row naming a missing entry makes the harness exit 1 with a message naming the row, not a `FileNotFoundError` traceback | fail closed with a named-row `missing-entry` problem |
| A2 | two admitted rows naming the same entry realpath make the harness exit 1 naming the duplicate | pairwise duplicate detection on `realpath` |
| B1 | a source-recheck manifest record whose `id != capture file stem` exits 1 (reason=stem-mismatch) | reject stem mismatch before any matching |
| B2 | a quote occurring twice without a verified anchor exits 1 (reason=occurrence-not-unique) | reject non-unique quotes unless the anchor verifies |

## 2. Incident chain each limb traces to

- **A1 ← M28-5 → M29-4 (first mode).** Round-28 verifier spotcheck routed defect 5:
  "`frontier-recheck-count.py` crashes on an absent entry — fail with a named row". Round-29
  lesson M29-4 confirms it was carried unfixed: "raises an uncaught `FileNotFoundError` when an
  admitted row's entry is absent … Fix: fail with a named row instead of a traceback".
- **A2 ← M29-4 (second mode).** "can pass pointing at an unrelated entry … a row whose entry
  cell names the existing F12 entry passes `entries=16 pass=16 exit=0` with zero new content …
  reject duplicate entry targets across admitted rows (same realpath twice)".
- **B1/B2 ← M28-8 → M29-3.** Round-28 spotcheck routed defect: "C2 Q9 stem check is not
  instrumented (hand-run receipts) — promote `check_q9.py`". Round-29 M29-3: "Q9's
  occurrence/stem binding is still not enforced by the committed instrument … `source-recheck.py`
  prints `OK occurrences=12 anchor=MISSING` and exits 0 for a record whose stem ≠ id
  (S043→S045.txt) … the C2 kill-rule clause was tripped mid-wave by the first manifest".
  QUALITY Q9 (round 24) is the normative text: "the record's `path` stem equals its `id`; the
  quote is exactly-once … (or carries an `anchor` line number the instrument verifies)".
- The B1 fixture mirrors the M29-3 repro shape exactly (record id `S043`, capture `S045.txt`);
  the B2 fixture mirrors the `occurrences=2 anchor=MISSING` observation.

## 3. Verification: baseline vs landed, replayed

Baseline replay at **freeze bytes** (do-nothing control; matches committed `c1-controls/before.txt`
and `before-run-2.txt`):

| Fixture | Freeze bytes | Observed | Verdict |
|---|---|---|---|
| A1 (`harness-root-a1`) | freeze harness `c8a62888…` | `FileNotFoundError` traceback, exit 1, no named-row marker | control cannot meet target |
| A2 (`harness-root-a2`) | freeze harness | `PASS F98/PASS F97`, `entries=2 pass=2 exit=0` | control cannot meet target |
| B1 (`q9/manifest-b1.json`) | freeze source-recheck `9fe6a4a0…` | `S043:Q1 OK… occurrences=1`, exit 0 (stem mismatch passes) | control cannot meet target |
| B2 (`q9/manifest-b2.json`) | freeze source-recheck | `S045:Q1 OK occurrences=2 anchor=MISSING`, exit 0 | control cannot meet target |

Landed bytes replay (same fixtures, current instruments):

| Fixture | Observed (current bytes) | Kill-rule clause |
|---|---|---|
| A1 | `FAIL F98 knowledge/zz-missing.md problems=missing-entry`, `entries=1 pass=0 exit=1`, no traceback | ✓ a1_exit=1, names F98 |
| A2 | `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1` | ✓ a2_exit=1, names duplicate |
| B1 | `S043:manifest MISMATCH reason=stem-mismatch`, exit 1 | ✓ b1_exit=1, reason present |
| B2 | `S045:manifest MISMATCH reason=stem-mismatch`, exit 1 | ✓ exit 1 + a failure reason, **but not the stated `occurrence-not-unique` — see F1** |

`source-recheck.py --selftest` at landed bytes: `selftest cases=9 failures=0`, exit 0 (clean,
corrupt, missing-source, missing-manifest, stem-mismatch, double-occurrence, double-occurrence-
anchored, out-of-range, broken).

Real corpus at current bytes: harness `entries=17 pass=17 exit=0` incl. `PASS F14 … ids=S041,S046,S047`;
per-id source-recheck on the round-30 manifest (`dfc8835750…`) — S046 Q1–Q4 all `occurrences=1`;
S047 Q1 occ=3 anchor=123-ok, Q3 occ=2 anchor=130-ok, others occ=1; S041 Q1–Q3 occ=1 — all exit 0.
(The F14 entry `japanese-severity-vocabulary-and-impact-model.md` landed mid-session, `f584f06c…`,
7096 B, 15:52Z; before it landed the harness was red on F14 `missing-entry` — the fail-closed
limb firing on the live row; that transient is sequencing (M29-1 class), not a regression.)

Mutant isolation probes (scratch copies only; each drop flips exactly its fixture):

| Mutant | Fixture | Observed | Conclusion |
|---|---|---|---|
| drop stem check | committed B1 | exit 0 | B1 limb load-bearing, isolating |
| drop occurrence block | isolated B2 (`S045.txt`, same `55124b0e…` capture) | `OK occurrences=2 anchor=MISSING`, exit 0 | B2 limb load-bearing when isolated |
| drop duplicate detection | committed A2 | `entries=2 pass=2 exit=0` | A2 limb load-bearing |
| A1 mutant = freeze bytes (uncaught open) | committed A1 | traceback, exit 1, no marker | A1 limb load-bearing |
| spelling-variant duplicate (`knowledge/../knowledge/dup-entry.md`) | H5 scratch | `DUPLICATE-ENTRY F98,F97`, exit 1 | realpath normalization works |

## 4. Findings — residue gaps (no edits made)

- **F1 (confirmed, medium): the committed B2 fixture is non-isolating.** `manifest-b2.json`
  pins `path: "B2.txt"` while the record id is `S045`; the B1 stem check fires first, so the
  frozen counter can never observe `reason=occurrence-not-unique`, and mutant-B2 ("drop
  occurrence check must make B2 exit 0") cannot be killed by it (mutant run still exits 1 via
  stem). The described reason never appears on the frozen fixture — the limb is demonstrable only
  via selftest. This violates R13's isolating-fixture requirement. Correction (future claims
  fix, not made here): name the capture `S045.txt` (same bytes/hash) so B2 is exercised alone.
- **F2 (confirmed, medium-high): single-row pointer to an existing entry still passes — M29-4's
  "zero new content" mode is only partly closed.** A2 catches pairwise duplicates among *admitted*
  rows; a lone admitted row whose entry cell points at an existing conforming entry passes
  (`P-H1`: `entries=1 pass=1 exit=0` using the harness's own dup-entry fixture). No
  ownership/novelty binding exists (the harness cannot know the entry is new this round or unique
  to the frontier). A row naming an existing non-frontier entry — or an entry whose owning row is
  not `admitted` — passes with zero new content.
- **F3 (confirmed, low-medium): manifest path handling is unsupervised.** The harness trusts
  whatever `--manifest <token>` the entry names: it does not require the manifest under
  `corpus/source-snapshots/`, nor bind it to the current round (an older round's manifest whose
  ids are listed would satisfy contract B). Also `RECHECK_MANIFEST` only matches the
  `--manifest value` spelling; `--manifest=value` (accepted by argparse) is flagged
  `no-manifest` — fail-closed, but asymmetric with the tool it gates.
- **F4 (observed, low):** the harness evaluates only `status="admitted"` rows (main filters on
  `r[2]`); the README currently holds only admitted rows, so this is consistent with the claim's
  semantics, but a non-admitted row with a bad entry is invisible to the harness.
- **F5 (observed):** the harness runs the recheck line via `bash -c` with `cwd=root`; a line
  carrying `cd /home/…/kasegi-shokunin &&` escapes the root in fixture runs (production lines do
  this by design and resolve to the lane root — the fixture entries therefore omit the `cd`
  prefix). Fixture-hygiene note, not a production defect.
- **F6 (observed, C2-adjacent):** mid-wave red window — the harness is exit 1 whenever the
  newest admitted entry file has not landed yet (the round-30 F14 gap; M29-1 sequencing-hazard
  class). Converged green at measurement time; a dispatcher-level depends-on between the C2 entry
  seat and this counter would remove the transient.

## 5. Confidence

- A1/A2/B1: **high** — baseline (freeze bytes) and fixed behavior both replayed; each limb flips
  its fixture under an isolating mutant; real corpus green 17/17 at current bytes.
- B2: **high that the limb exists** (isolated probe + selftest), **limited at claim level** by
  F1 (frozen fixture non-isolating).
- F2/F3: demonstrated on in-lane scratch fixtures; presented as residue, no production change.
