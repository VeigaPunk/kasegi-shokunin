# round-54 routed-defect corrections — D53-1 and D53-2 (appended file; no filed byte edited)

Filed by round 54 against base `32782bd6b564f80454af853b38868603a4140e79`, addressing the round-53
non-author closure's routed defects (`corpus/lessons/round-53-verifier-spotcheck.md` section 6).
R9 form: a numerical erratum naming its base and changed-file scope, appended as a NEW file — the
corrected records' bytes are never rewritten (receipts are the unedited tees of one observed run,
R39; registry rows are append-only, R8). Before-state receipt with the filed literals and the
sha256 pins as they stood at the round's start: `.ufo/waves/round-54/controls/d53-base-greps-r54.txt`.

## D53-1 — receipt trailer number drift (34 vs 33)

- Filed literal: `.ufo/waves/round-53/controls/c2-counter-final-r53.txt:9` reads
  `C2_COUNTER_FINAL_EXIT=1 (counter exit stays 1 on the 34 inherited recheck-exit-1 entry records — ...)`.
- Measured value: the SAME receipt's `:8` class-check line prints
  `FAIL_entry_records=33 not_recheck-exit-1=0 ...`, and 33 = entries 37 − pass 4. Re-derived again
  at the round-54 base (`.ufo/waves/round-54/controls/do-nothing-c2-r54.txt`: FAIL-entry records 33)
  and, after the round's C2 admission, 38 − 5 = 33 — the figure is invariant across the round's own
  declared after-state, so the correction cannot be invalidated by the round's data.
- Disposition: the `:9` trailer literal "34" is **superseded by 33**. The receipt's bytes stay
  byte-identical (sha256 `be69ece74fcd5498dd23e14c9ec1aa862a579bbb46f2df22c1692409f42bf3ab`, pinned
  in the before-state receipt and in the closure check below) — a receipt is never edited or
  appended to after its run.
- Class: receipt trailer prose composed from the superseded draft-run figure; the load-bearing lines
  (`:8`) were correct. Fix: `corpus/instruments/figure-audit.py` + `figure-audit-ledger.json` (round
  54 C1) — ledger entry `fail-entry-records` re-derives 33 from the live counter and its `record`
  cell names the superseded 34; mined in `corpus/lessons/round-54.md` § Mistakes.

## D53-2 — capture metadata line-count drift (543 vs 542)

- Filed literals (three places): `corpus/source-snapshots/round-53/manifest.json` `"lines": 543`;
  the `corpus/SOURCES.md` S085 row anchor cell "…7590 bytes, 543 lines;…"; the
  `corpus/knowledge/nvd-api-2.0-response-schema.md` source: line "(543 lines, 7590 bytes; …)".
- Measured value: `wc -l < corpus/source-snapshots/round-53/S085.txt` → **542** (7590 bytes =
  7589 content bytes + 1 trailing newline; `awk 'END{print NR}'` agrees). The load-bearing figures —
  sha256 `4d1c4e7732e128750a00557b0f16e69f021d2d5d25e2f55dfe8a9d5faa9a44d2`, 7590 snapshot bytes,
  10394 raw bytes — are correct and unchanged.
- Disposition: all three "543" literals are **superseded by 542**. The three files stay
  byte-identical as of this correction's commit (sha256 pins in the before-state receipt:
  manifest `eb6ffa6047d2e6e7edc19b4708d1b7bb39b322c77e7f4c146d5a3f341c5f475e`, capture
  `4d1c4e77…`, SOURCES `06c92e6ae60470553caf8d0c1bb0754f28559d1591a50c8418b4d9406f5b5fd2`,
  entry `15eb2d05e88d8e08a4de9939e7996307481899c659c35536fbe286ea1324b201`; the capture and the
  round-53 manifest are additionally pinned by the closure check below, since committed capture
  provenance must never move). The manifest is committed capture provenance (R20) and is never
  rewritten; a registry row's cells are append-only (R8) and a corrected `lines` count does not
  merit a superseding row; the entry header is a filed assertion corrected here, not in place.
- Class: metadata figures hand-derived at capture time, not command-derived — the same family as
  the R56 quote word-count rule. Fix: figure-audit ledger entries `capture-lines-s085` (want 542)
  and `capture-bytes-s085` (want 7590) re-derive both figures from the committed bytes at
  `32782bd`; mined in `corpus/lessons/round-54.md` § Mistakes.

## D53-3 — prompt-template omission (operator-side; recorded, not actionable lane-side)

The round-53 closure's D53-3 (the dispatched prompt omits the MISSION.md §L2-concurrency embed) is
operator-side and standing; routed via `.ufo/l0-questions.md` (kasegi round-54 row appended this
round; the same-substance host question stands as kaidoku round-53). Nothing lane-side changes; the
lane keeps disclosing the absence of the AgentSwarm surface every round.

## Closure check (bash -n parseable; run from the lane root)

```sh
cd "$(git rev-parse --show-toplevel)" || exit 9
c=.ufo/waves/round-54/controls/routed-d53-corrections.md
r=.ufo/waves/round-53/controls/c2-counter-final-r53.txt
cap=corpus/source-snapshots/round-53/S085.txt
man=corpus/source-snapshots/round-53/manifest.json
ok=1
grep -q 'D53-1' "$c" && grep -q 'D53-2' "$c" || ok=0
grep -q 'superseded by 33' "$c" || ok=0
grep -q 'superseded by 542' "$c" || ok=0
[ "$(grep -c '34 inherited' "$r")" -eq 1 ] || ok=0
[ "$(grep -c 'FAIL_entry_records=33' "$r")" -eq 1 ] || ok=0
[ "$(wc -l < "$cap")" -eq 542 ] || ok=0
[ "$(sha256sum "$r" | cut -d' ' -f1)" = be69ece74fcd5498dd23e14c9ec1aa862a579bbb46f2df22c1692409f42bf3ab ] || ok=0
[ "$(sha256sum "$cap" | cut -d' ' -f1)" = 4d1c4e7732e128750a00557b0f16e69f021d2d5d25e2f55dfe8a9d5faa9a44d2 ] || ok=0
[ "$(sha256sum "$man" | cut -d' ' -f1)" = eb6ffa6047d2e6e7edc19b4708d1b7bb39b322c77e7f4c146d5a3f341c5f475e ] || ok=0
[ "$ok" -eq 1 ] && { echo "d53-corrections=closed"; exit 0; }
echo "d53-corrections=open"; exit 1
```

Exit 0 only when both corrections are named with their measured values AND the filed receipt bytes,
the capture and the round-53 manifest are unchanged; non-zero while any limb fails.
