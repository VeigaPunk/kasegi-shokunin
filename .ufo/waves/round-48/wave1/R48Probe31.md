# R48Probe31 — bounded grammar probe: box-3 removal on canonical SHONEN.md

- Seat: R48Probe31 (leaf; no subagent dispatch, no delegation, no background jobs)
- Round: 48, wave 1, lane kasegi-shokunin
- Claim probed: C1 (routed-defect-closure) — `SHONEN.md` conforms to the canonical
  four-box author-assessment grammar; frozen counter
  `python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`
- Judged axis: depth:verifiability
- Verifier revision observed: `corpus/instruments/shonen-form.py` as present at frozen
  claim `.ufo/waves/round-48/claims.json` sha 3546f7089c224ac6c8adc68208b1e648bbf3e6a5
  (checker source untouched by this seat; report-only).

## Scope and bounds honored

- All probes ran against scratch copies under
  `/fast/scratch/hyaku/kasegi-r48/R48Probe31/` only. No production file, fleet file,
  sibling tree, domain tree, or git/jj index/state was edited by this seat.
- `--root` stayed pointed at the production tree
  (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`) exactly as the seat spec and the
  checker's pointer-resolution contract require; only `--file` named a scratch path.
- Scratch dir was explicitly created at start and removed on exit after receipts were
  saved into this report. No `/tmp` clones.
- Tool installs: none required, none performed (python3 from host, no version change).
- Predicates/bytes frozen: reported observed-vs-expected as-is; nothing silently fixed.

## Transformation

Scratch copies of canonical `SHONEN.md` (sha256
`b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` for both copies at
copy time) were made; on the mutant copy, box 3 only — the checklist line
`- [~] Instructions executable by an agent without oral context` and its evidence line
`Evidence: corpus/lessons/round-47-verifier-spotcheck.md — ...` — was deleted.
Boxes 1, 2, and 4 left byte-identical.

Diff evidence (positive vs mutant):

```
9,10d8
< - [~] Instructions executable by an agent without oral context
<       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
diff_exit=1
```

Mutant sha256 after edit: `512f058e8e134b8d954b68662cd9ba99840a4d115f848e9eb9f8c984e9383242`.

## Exact commands and full observed output

Working directory for all probe runs: `/fast/scratch/hyaku/kasegi-r48/R48Probe31`.

```
PY=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin

=== POSITIVE (unmodified copy) ===
$ python3 "$PY" --root "$ROOT" --file SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0

=== MUTANT box3-removed run 1 ===
$ python3 "$PY" --root "$ROOT" --file SHONEN.box3-removed.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1

=== MUTANT box3-removed run 2 (stability) ===
$ python3 "$PY" --root "$ROOT" --file SHONEN.box3-removed.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

## Expected vs observed

| Case | Expected | Observed | Verdict |
|---|---|---|---|
| Positive (unmodified copy) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` (process exit 0) | MATCH |
| Mutant, box 3 removed, run 1 | nonclean, stable SF finding | `canonical=0 finding=SF-BOX exit=1` (process exit 1) | MATCH |
| Mutant, box 3 removed, run 2 | same finding as run 1 | `canonical=0 finding=SF-BOX exit=1` (process exit 1) | MATCH — stable across both runs |

## Mechanism of the finding

With box 3's checklist line removed, the checker's label loop compares
`LABELS[2]` (`Instructions executable by an agent without oral context`) against the
line now sitting in that position — box 4's
`- [~] No cross-domain bleed (PROVINCE.md still accurate)`. The `re.fullmatch` on the
box-3 pattern fails, yielding `SF-BOX`, exit 1. The checker does not silently resync or
pass a three-box checklist; the four-box grammar is enforced positionally.

## Semantically permitted?

No — the transformation is a genuine grammar violation, not a permitted alternative
form. The promotion gate (protocol-source.txt, "Promotion gates") requires all four
`SHONEN.md` boxes, and the frozen checker's preamble contract enumerates exactly four
labels. A checklist missing box 3 is noncanonical author-side form. The observed
`SF-BOX` is the checker defeating the mutant as designed; no defect was fabricated and
no defect in the checker was observed.

## Production-tree untouched evidence

`git status --porcelain` in the lane root after the probe shows `SHONEN.md` absent
from the modification list (pre-existing entries belong to the integrator and sibling
seats: `SKILL.md`, other `R48Probe*.md` reports, `.ufo/waves/round-48/` state files).
This seat's only writes were the two scratch fixtures and this report.

## Receipts / cleanup

- Scratch fixtures hashed and diffed above; full command outputs reproduced verbatim.
- Scratch directory `/fast/scratch/hyaku/kasegi-r48/R48Probe31/` removed on exit after
  this report was written.

## Risks / blockers

- None. Probe bounded to the assigned grammar case; no other boxes, predicates, or
  rounds touched.
