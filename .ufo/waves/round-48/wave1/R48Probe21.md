# R48Probe21 — Bounded grammar probe: box-2 removal mutant vs frozen shonen-form.py

- Seat: R48Probe21 (executor, wave 1, round 48, kasegi lane)
- Axis: depth:verifiability
- Claim probed: C1 (routed-defect-closure) — frozen predicate: `shonen-form canonical=1 finding=SF-CLEAN exit=0` at the measured revision; frozen counter `python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`.
- Round-47 routes read: R1 (SHONEN.md canonical-form drift — basis of C1), R2 (frozen plain-target phrasing — not exercised by this probe).
- Production edits: none. All mutations live on scratch fixtures, removed after this report landed.
- Tooling: no tools installed or updated for this seat. Host `python3 3.14.8`, stdlib only (`argparse`, `pathlib`, `re`).

## Frozen inputs (hashes recorded at probe time)

```
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  corpus/instruments/shonen-form.py          (frozen counter)
b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c  .ufo/waves/round-48/controls/canonical-candidate.txt  (controls canonical snapshot)
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.md                                   (production, read-only control and probe base)
b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2b345  .ufo/waves/round-48/claims.json            (== freeze.txt claims-sha256, verified)
```

Canonical base note: the seat's "canonical SHONEN.md" was probed as the production `SHONEN.md` (the live integrated candidate, sha256 `b1352168…`, byte-identical to my positive fixture). It differs from `controls/canonical-candidate.txt` only in evidence-line prose and box 2's mark (`[ ]` vs `[~]`); both bases are canonical-form conformant and behave identically under a box-2 removal, because the finding fires on the box-line mismatch, not on evidence text. The claim C1 `after` state is defined against the production tree, so production is the correct base.

## Transformation

Scratch copies of canonical SHONEN.md under `/fast/scratch/hyaku/kasegi-r48/R48Probe21/`:

- `SHONEN.positive.md` — byte copy of production (sha256 `b1352168…`, confirmed equal).
- `SHONEN.no-box2.md` — single bounded mutation, box 2 only: the box-2 checklist line and its evidence line were both removed (a "box" is the checklist line plus its one optional indented evidence line per the file contract). Boxes 1, 3, 4 and all other lines are unchanged. Diff:

```
7,8d6
< - [ ] At least one end-to-end domain task executed and logged in LOG.md
<       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
```

Mutant sha256: `aa54418f0bd1d66783d8f2a645a762280f8de9e96c2045a8973f2d235aac91ae`.

This transformation is **not** semantically permitted: the protocol file contract fixes the seed verbatim — "no other prose, added boxes, or removed boxes" — so deleting a required checklist box is exactly the drift the frozen counter exists to catch. The defect is real; none was fabricated.

## Exact commands and full observed output

```
cd /fast/scratch/hyaku/kasegi-r48/R48Probe21
TOOL=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin

== RUN 1: positive (unmodified canonical copy) ==
$ python3 "$TOOL" --root "$ROOT" --file /fast/scratch/hyaku/kasegi-r48/R48Probe21/SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0

== RUN 2: mutant, box 2 removed ==
$ python3 "$TOOL" --root "$ROOT" --file /fast/scratch/hyaku/kasegi-r48/R48Probe21/SHONEN.no-box2.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1

== RUN 3: mutant, box 2 removed (stability re-run) ==
$ python3 "$TOOL" --root "$ROOT" --file /fast/scratch/hyaku/kasegi-r48/R48Probe21/SHONEN.no-box2.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1

== RUN 4: production SHONEN.md via default --file (read-only control) ==
$ python3 "$TOOL" --root "$ROOT"
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

Fixture digests at run time:

```
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.positive.md
aa54418f0bd1d66783d8f2a645a762280f8de9e96c2045a8973f2d235aac91ae  SHONEN.no-box2.md
```

## Expected vs observed

| Run | Input | Expected | Observed | Verdict |
|---|---|---|---|---|
| 1 | positive (canonical copy, unmodified) | canonical=1 SF-CLEAN exit=0 | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH |
| 2 | mutant, box 2 removed | nonclean, stable single SF finding, exit=1 | `shonen-form canonical=0 finding=SF-BOX exit=1`, shell exit 1 | MATCH |
| 3 | mutant re-run (stability) | identical to RUN 2 | identical byte-for-byte output and exit | MATCH (stable) |
| 4 | production SHONEN.md (claim C1 "after" control) | canonical=1 SF-CLEAN exit=0 | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH — supports C1's `after` predicate at the measured tree |

## Why SF-BOX is the correct, stable finding for box-2 removal

Walking `grade()` on the mutant: the preamble (4 lines) and box 1 (mark `~`, evidence pointer `SKILL.md` resolves under root) consume lines 1–6. The grader then expects box 2's label at line 7 and applies `re.fullmatch(r'- \[([ ~x])\] ' + box2_label, lines[6])`. With box 2 deleted, line 7 is box 3's line (`- [~] Instructions executable by an agent without oral context`), which cannot fullmatch box 2's label, so the grader returns `SF-BOX` immediately — before pointer checks on later lines and before the trailing-length check. The exit code is the declared `1` = noncanonical per the counter's docstring and the Gate standard verdict map (`0` clean, `1` failed; no other code occurred). The function is pure (no time, no randomness, no I/O beyond the fixture read), and the mutation shifts every later box up by exactly two lines without altering their content, so the finding id is deterministic across runs — demonstrated by RUN 2 vs RUN 3 byte-identical output.

## Conclusions

- The frozen counter rejects a box-2 removal with a stable, single `SF-BOX` finding at exit 1; the unmodified canonical positive passes with `SF-CLEAN` at exit 0. Both seat-spec expectations hold.
- Production `SHONEN.md` at the measured tree grades `canonical=1 SF-CLEAN exit=0`, consistent with claim C1's declared `after` state; no evidence against the frozen predicate was observed.
- No counter defeat observed; nothing for the kill rule to act on. No production, fleet, or sibling files were written; scratch fixtures were removed after this report was saved.
