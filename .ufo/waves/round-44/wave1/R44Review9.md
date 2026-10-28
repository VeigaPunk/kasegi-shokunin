# R44Review9 — Adversarial C1 count/predicate

## Finding

**No evidence that the frozen C1 count/predicate can be satisfied by do-nothing or mere post-hoc edits.** The canonical frozen claims define C1 as the same eight numbered routed defects from round-43 §6, all corrected append-only, with at least one red-before control for each changed gate; the kill rule explicitly fails if a do-nothing replay reports all eight fixed or any remains unresolved (`.ufo/waves/round-44/claims.json:9-15`). The frozen do-nothing receipt records base `5ab3a60a…`, count 8, no R44 correction/counter, and says target 0 unresolved cannot be reached (`.ufo/waves/round-44/controls/do-nothing.txt:2-7`). The source defects are enumerated 1–8 at `corpus/lessons/round-43-verifier-spotcheck.md:97-108`.

Adversarial concern: **post-hoc editability is not itself ruled out by append-only form.** An appended correction can alter the reported interpretation without changing historical bytes. The frozen predicate does constrain this by fixing identity of the list before implementation, requiring *all eight same defects* unresolved→resolved and a red-before control per changed gate (`claims.json:11-13`); simply appending a blanket assertion or changing the count is not satisfaction. However, I cannot affirm the eventual counter rejects such gaming: at inspected HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`, `corpus/instruments/r44-routed-defects.py` is absent (read returned not found), and no wave1 report/instrument was present in the accessible tree. Therefore counter soundness against post-hoc reinterpretation remains unverified, not a proven defect.

## Exact evidence / commands

- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `66314015122b9aa32dc40f2f1815df56624c26d1`.
- `git -C ... status --short` → pre-existing `?? .ufo/waves/round-44/controls/census-invocation-error.txt` and `?? .ufo/waves/round-44/wave1.ready.partial`; I did not touch them.
- Read `claims.json:9-15`, `controls/do-nothing.txt:1-7`, and frozen defect source `round-43-verifier-spotcheck.md:97-108`.
- `read .../corpus/instruments/r44-routed-defects.py` → `Path ... not found`.
- Scratch attempt `mkdir -p "$HYAKU_SCRATCH/kasegi-r44/R44Review9"` failed `Permission denied`; `HYAKU_SCRATCH` was empty. No scratch created, therefore nothing to clean. No tools installed.

## Limitations

This is a frozen-base/predicate adversarial check only; I did not inspect a later integrated revision or execute any instrument. No semantic LSP device was available in this environment, so no caller/definition diagnostics were obtained. No runtime verdict offered.