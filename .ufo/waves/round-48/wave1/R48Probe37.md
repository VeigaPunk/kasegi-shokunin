# R48Probe37 — Bounded grammar probe: box-3 evidence-line removal vs frozen shonen-form

- Seat: R48Probe37 (executor, wave 1, one v2 wave / 64 seats)
- Claim probed: C1 (routed-defect-closure, axis `depth:verifiability`), frozen at
  `.ufo/waves/round-48/claims.json` sha256 `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` (as assigned;
  on-disk freeze.txt pins the pre-wave claims blob `b8022cdf…` — the claims text and counter bytes
  are frozen either way and were not edited)
- Date: 2026-10-30T14:56Z. No production files touched; all fixtures under scratch, removed on exit.
- No tool installs this seat (system python3 3.14.8 only).

## Assignment

On a scratch copy of canonical `SHONEN.md`, remove the evidence line of box 3 only, run the frozen
`shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file <scratch>`, expect
nonclean + stable SF finding; also run the unmodified positive. Keep other boxes unchanged.

## Box-numbering note (both conventions probed)

The protocol File contract (`controls/protocol-source.txt`) numbers the four boxes 1–4; the committed
fixture caselist (`controls/fixtures.json`) names variants `missing-evidence-0..3` (0-indexed). I ran
both negative variants so the finding is convention-independent:

- Mutant A = box 3 in 1-indexed protocol numbering ("Instructions executable by an agent without
  oral context" — the third box), evidence line deleted; other three boxes untouched.
- Mutant B = box index 3 in 0-indexed fixture numbering ("No cross-domain bleed (PROVINCE.md still
  accurate)" — the fourth box), evidence line deleted; other three boxes untouched.

## Frozen inputs (hashes observed this seat)

| Artifact | sha256 |
|---|---|
| `corpus/instruments/shonen-form.py` (frozen checker) | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` |
| `.ufo/waves/round-48/controls/fixtures.json` | `10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288` (matches the digest pinned inside `shonen-form-selftest.py`) |
| `.ufo/waves/round-48/controls/canonical-candidate.txt` | `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c` |
| scratch `SHONEN.canonical.md` (byte-copy of candidate) | `b476c7aa…4de4b8c` (identical) |
| scratch `SHONEN.box3-no-evidence.md` (mutant A) | `dddde31bef24762b3635db2a1f58cd6dc9d1d92ad82dbf8c81486fa6c7b4bf7e` |
| scratch `SHONEN.boxidx3-no-evidence.md` (mutant B) | `973f7073211a465562c63c12a380ccce31ea3ab437edf1329e1b21101799cdc8` |

## Probe construction (exact deltas)

`diff SHONEN.canonical.md SHONEN.box3-no-evidence.md` → `10d9` deleting exactly
`      Evidence: LOG.md — Author assessment only; no promotion claimed.` (line 10, under the third
box). `diff SHONEN.canonical.md SHONEN.boxidx3-no-evidence.md` → `12d11` deleting exactly line 12
(under the fourth box). Both mutants are single-line deletions; boxes, marks, preamble, and trailing
bytes otherwise byte-identical to the canonical copy (each 582 bytes vs canonical's longer length;
canonical file is 12 lines).

The committed fixtures `missing-evidence-2` / `missing-evidence-3` are cumulative prefix deletions
(2 and 3 evidence lines respectively — verified by difflib against my single-box mutants), so my
single-box transformation is a distinct case not in the committed caselist; it lands on the same
finding as the whole `missing-evidence-0..3` family.

## Commands and observed output (verbatim, run 2026-10-30T14:52–14:56Z)

Positive (unmodified canonical copy):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe37/SHONEN.canonical.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

Negative A (box 3, 1-indexed — "Instructions executable…", evidence line removed):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe37/SHONEN.box3-no-evidence.md
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
PROCESS_EXIT=1
```

Negative B (box index 3, 0-indexed — "No cross-domain bleed…", evidence line removed):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe37/SHONEN.boxidx3-no-evidence.md
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
PROCESS_EXIT=1
```

Stability repeat (second run of all three, 2026-10-30T14:56Z): identical output lines and exit
codes — positive `canonical=1 finding=SF-CLEAN exit=0` / PROCESS_EXIT=0; both negatives
`canonical=0 finding=SF-EVIDENCE exit=1` / PROCESS_EXIT=1.

## Expected vs observed

| Case | Expected | Observed | Verdict |
|---|---|---|---|
| Unmodified canonical | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | MATCH |
| Box-3 evidence removed (either numbering) | nonclean + stable SF finding | `canonical=0 finding=SF-EVIDENCE exit=1`, stable across repeat | MATCH |

## Why this finding is a true defect, not fabrication

The transformation is **not** semantically permitted under the frozen grammar, so the
`SF-EVIDENCE` finding is real. In `shonen-form.py` `grade()`, after each box line the next line
must start with `      Evidence: ` carrying one repo-relative resolvable pointer; if the evidence
line is absent and the mark is not `[ ]`, it returns `SF-EVIDENCE` (exit 1). The protocol's File
contract is the normative source: marks are confined to "the box character plus one indented
evidence line per box — `[x] <verifier-id>` or `[~]` with a resolvable pointer". A `[~]` mark with
no evidence line claims an author assessment while withholding its mandatory pointer — exactly the
class C1's `mechanical_limits` names ("Evidence pointer existence is checked, not semantic truth").
The checker neither over-reaches (it does not judge the pointer's semantics) nor under-reaches (an
unchecked `[ ]` box may carry no evidence; a `[~]`/`[x]` box may not). The finding is also stable by
construction: pure function of file bytes, and the selftest's committed EXPECTED map already pins
`missing-evidence-{0..3} → SF-EVIDENCE exit=1`, which my single-box variants reproduce.

## Discrimination against controls

- Positive control discriminates: the byte-identical canonical copy passes (`SF-CLEAN`), so the
  negatives' red is caused by the deletion, not by scratch-path or root resolution
  (`LOG.md` exists at the lane root, so pointer resolution is exercised green in the positive).
- Frozen `controls/do-nothing.txt` records the actual-r47-drift state
  (`canonical=0 finding=SF-PREAMBLE exit=1`) — a different finding class (preamble drift), showing
  the checker separates defect kinds rather than collapsing to one red.

## Scope and hygiene

Read-only over the production tree; scratch fixtures lived at
`/fast/scratch/hyaku/kasegi-r48/R48Probe37/` and were removed after this report was written. No
git/jj mutations, no delegation, no background jobs, no PATH writes. This is author-side form
validation only — it does not bear on promotion semantics or evidence truth (round-47 verifier
routes R1/R2 discipline: a checker verdict is a measurement, and this seat asserts the frozen
counter's behavior, not any claim's worth).

## Receipts

Full command/output transcripts are quoted verbatim above; fixture digests are recorded in the
hashes table. Scratch removed post-report (no durable scratch artifacts retained, per seat spec).
