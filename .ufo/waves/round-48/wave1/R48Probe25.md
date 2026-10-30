# R48Probe25 — Bounded grammar probe: box-2 code-indent mutant vs frozen shonen-form.py

- Seat: R48Probe25 (executor, wave 1, round 48, kasegi lane)
- Axis: depth:verifiability
- Claim probed: C1 (routed-defect-closure) — frozen predicate: `shonen-form canonical=1 finding=SF-CLEAN exit=0` at the measured revision; frozen counter `python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`.
- Frozen claim: `.ufo/waves/round-48/claims.json` @ commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` — verified read-only: `git cat-file -t` → `commit`; `git log --oneline -1` → `3546f70 round-48: freeze canonical checklist restoration and controls`; blob at that commit and working-tree file both sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matching `freeze.txt` (`claims-sha256: b8022cdf...`).
- Round-47 routes read: R1 (SHONEN.md canonical-form drift — basis of C1; `corpus/lessons/round-47-verifier-spotcheck.md` L85), R2 (frozen plain-target phrasing — not exercised by this probe; L86).
- Production edits: none. All mutations live on scratch fixtures, removed after this report landed.

## Frozen inputs (hashes recorded at probe time)

```
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  corpus/instruments/shonen-form.py          (frozen counter)
b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c  .ufo/waves/round-48/controls/canonical-candidate.txt  (canonical SHONEN.md)
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.md                                   (production, read-only control)
```

No tools installed or updated for this seat (python3 from host, Python 3.14.8 stdlib only). No packages touched; pacman untouched.

## Transformation

Scratch copy of the canonical SHONEN.md (byte-identical to `controls/canonical-candidate.txt`, sha256 confirmed equal). Single bounded mutation, box 2 only: the box-2 checklist line was indented by 4 spaces, rendering it a Markdown code block per CommonMark (the canonical grammar requires the box line to begin at column 0 with `- [<mark>] `). The box-2 evidence line and boxes 1, 3, 4 are unchanged. Diff (only changed line shown):

```
7c7
< - [~] At least one end-to-end domain task executed and logged in LOG.md
---
>     - [~] At least one end-to-end domain task executed and logged in LOG.md
```

Mutant sha256: `05805dea4f780bae4a2263f74c7a6f7037dce33d8d1572a46ed907594bd15237`.

This transformation is **not** semantically permitted: the file contract (`controls/protocol-source.txt` L446, File-contract row for `SHONEN.md`) requires the seed verbatim with "marks … confined to the box character plus one indented evidence line per box — … no other prose, added boxes, or removed boxes". A 4-space-indented box line is a code block, i.e. added prose/structure, not a mark. The defect is real; none was fabricated.

## Exact commands and full observed output

```
cd /fast/scratch/hyaku/kasegi-r48/R48Probe25
TOOL=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin

== RUN 1: positive (unmodified canonical copy) ==
$ python3 "$TOOL" --root "$ROOT" --file SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0

== RUN 2: mutant, box 2 indented as code (first pass) ==
$ python3 "$TOOL" --root "$ROOT" --file SHONEN.box2-code-indented.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1

== RUN 3: mutant, box 2 indented as code (stability re-run) ==
$ python3 "$TOOL" --root "$ROOT" --file SHONEN.box2-code-indented.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1

== RUN 4: production SHONEN.md via default --file (read-only control) ==
$ python3 "$TOOL" --root "$ROOT"
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

## Expected vs observed

| Run | Input | Expected | Observed | Verdict |
|---|---|---|---|---|
| 1 | positive (canonical copy, unmodified) | canonical=1 SF-CLEAN exit=0 | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH |
| 2 | mutant, box 2 as code | nonclean, stable single SF finding, exit=1 | `shonen-form canonical=0 finding=SF-BOX exit=1`, shell exit 1 | MATCH |
| 3 | mutant re-run (stability) | identical to RUN 2 | identical byte-for-byte output and exit | MATCH (stable) |
| 4 | production SHONEN.md (claim C1 "after" control) | canonical=1 SF-CLEAN exit=0 | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH — supports C1's `after` predicate at the measured tree |

## Why SF-BOX is the correct, stable finding

The frozen checker grades each box with `re.fullmatch(r'- \[([ ~x])\] ' + label, lines[i])` — `fullmatch` anchors both ends, so leading whitespace on the box line fails the match and the grader returns `SF-BOX` immediately, before any later line (including that box's unchanged evidence line) is consulted. Concretely: preamble consumes lines 1–4 (`i=4`); box 1 at line 5 matches and its evidence line 6 passes the pointer check (`i=7`); box 2 is then read at line 7 (`    - [~] At least one end-to-end domain task …`), where the 4-space indent breaks the `fullmatch` → `SF-BOX`. The mutant changes exactly one line (the box-2 line) and nothing downstream differs, so the finding id is deterministic across runs (demonstrated by RUN 2 vs RUN 3 byte-identical output). The exit code is the declared `1` = noncanonical per the counter's own docstring (`0 clean; 1 noncanonical; 2 unreadable input`); no other code occurred.

## Conclusions

- The frozen counter rejects a code-indented box 2 with a stable, single `SF-BOX` finding at exit 1; the unmodified canonical positive passes with `SF-CLEAN` at exit 0. Both expectations from the seat spec hold.
- Production `SHONEN.md` at the measured tree grades `canonical=1 SF-CLEAN exit=0`, consistent with claim C1's declared `after` state; no evidence against the frozen predicate was observed.
- No counter defeat observed; nothing for the kill rule to act on. No production, fleet, or sibling files were written; scratch fixtures were removed after this report was saved.
