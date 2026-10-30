# R48Probe44 — Bounded grammar probe: box-4 HTML-comment wrap mutant vs frozen shonen-form.py

- Seat: R48Probe44 (mutation-tester, wave 1, round 48, kasegi lane)
- Axis: depth:verifiability
- Target claim: C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- Probe class: negative mutant on a scratch copy — wrap box 4 (box line + its `Evidence:` line) in an HTML comment; boxes 1–3 and the preamble byte-unchanged
- Round/wave: 48 / wave1 (one v2 wave, 64 seats); lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Date: 2026-10-30
- Production edits: none. The mutant exists only in seat scratch, removed after these receipts were embedded.

## Godspeed axes

1. **Axes named:** (a) mutant killed/not (detector flips on the defect), (b) finding stability (same SF code + exit across re-runs), (c) blast radius (boxes 1–3 and production bytes untouched), (d) restoration evidence (pristine == production hashes before and after).
2. **Cheap parallel iterations:** all four detector runs executed in one bounded batch against the frozen checker.
3. **Kept moves:** exact-command logging, hash identity chain, diff proof of single-box scope.
4. **Frontier walk:** verdict follows the detector bytes; no predicate amended.

## Frozen identity

- Frozen claim: `.ufo/waves/round-48/claims.json` at freeze commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`; observed file sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` (matches `freeze.txt` `claims-sha256` recorded by sibling seats).
- Frozen counter: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (unmodified; no checker amendment, per the C1 kill rule).
- Canonical target: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md`, sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`.
- Round-47 verifier routes read: **R1** (`corpus/lessons/round-47-verifier-spotcheck.md:85`) — canonical form = seed verbatim + marks confined to the box character + one indented evidence line per box, no other prose; this is the basis of C1 and directly governs this probe. **R2** (`:86`, frozen plain-target phrasing) read; not exercised by this grammar probe.
- Scope: author-side form only — not promotion, not semantic truth, no target testing.
- Tooling: no tools installed or updated this seat; host `python3` with stdlib only. All pacman transactions remain paused; nothing touched.

## Scratch fixtures

Scratch (created, then removed after receipts): `/fast/scratch/hyaku/kasegi-r48/R48Probe44/`

```sh
mkdir -p /fast/scratch/hyaku/kasegi-r48/R48Probe44 && cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md && sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md && wc -c /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md
```
Output:
```text
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md
761 /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md
```

Mutant `SHONEN.mutant.box4-htmlcomment.md` (770 bytes, sha256 `82a654a898288cc119e92c72ff85dd9d69ae958b473fc4c21383a8a1dc174c0b`) — full diff against the pristine copy (only the two comment-delimiter lines are added; box 4's bytes and boxes 1–3 are untouched):

```text
--- /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md	2026-10-30 11:57:52.429577663 -0300
+++ /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.mutant.box4-htmlcomment.md	2026-10-30 12:00:24.951926727 -0300
@@ -8,5 +8,7 @@
       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
+<!--
 - [~] No cross-domain bleed (PROVINCE.md still accurate)
       Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
+-->
DIFF_EXIT=1
```

## Expected vs observed

| Run | Fixture | Expected (from frozen grammar) | Observed | Verdict |
|---|---|---|---|---|
| 1 | pristine copy (positive) | `canonical=1 finding=SF-CLEAN exit=0` | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH |
| 2 | mutant, box 4 in HTML comment | nonclean, stable single SF finding, exit=1 → `SF-BOX` at the box-4 line | `shonen-form canonical=0 finding=SF-BOX exit=1`, shell exit 1 | MATCH — mutant killed |
| 3 | mutant, stability re-run | identical to run 2 | byte-identical output, exit 1 | MATCH (stable) |
| 4 | production `SHONEN.md`, default `--file` (read-only control) | `canonical=1 finding=SF-CLEAN exit=0` (C1 `expect_after` at current tree) | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, shell exit 0 | MATCH |

## Full observed commands and output

```text
== RUN 1: positive, pristine scratch copy ==
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0

== RUN 2: mutant, box 4 wrapped in HTML comment ==
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.mutant.box4-htmlcomment.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1

== RUN 3: stability re-run of mutant ==
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe44/SHONEN.mutant.box4-htmlcomment.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1

== RUN 4: production SHONEN.md via default --file (read-only control) ==
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

## Verdict and reasoning

**Mutant killed.** The frozen checker parses line-by-line: after boxes 1–3 consume lines 5–10, it applies `re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), lines[i])` with box 4's label at the line where the mutant has `<!--`. The fullmatch fails and `grade()` returns `SF-BOX` (exit 1) — a nonclean, single, deterministic finding, exactly as the seat spec expects. No state, no time dependence; the stability re-run reproduced it byte-for-byte.

**The transformation is not semantically permitted.** Wrapping box 4 in an HTML comment is a real defect, not a checker false positive. In raw bytes the box text survives, but under the lane's own R1 route a canonical box must be a live `- [ ]`/`[~]`/`[x]` list line followed by its indented `Evidence:` line; a commented-out box is neither. In rendered Markdown an HTML comment is invisible, so the rendered document would present a three-box checklist while claiming "all of" four requirements — box 4 ("No cross-domain bleed") silently disappears from every rendered reading. Hiding a mandatory gate line is precisely the class of drift C1's grammar exists to reject, so `SF-BOX` is the correct verdict against both the frozen bytes and the rendered semantics. (Contrast with the round-47 counter errata: those survivors were false greens in *that* counter; this checker's rejection here is a true kill, and no counter bytes were amended to obtain it.)

## Restoration evidence

- Production `SHONEN.md` before the probe: `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`; after RUN 4 (which reads it via the frozen default invocation) and at teardown: same sha256 — untouched. Run 4 itself demonstrates the live tree still grades clean.
- Pristine scratch copy retained byte-identical to production throughout (`b1352168…` at setup and at the identity-hash block after all runs).
- Checker sha256 before and after: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` — frozen bytes never amended.
- Scratch removal (receipts embedded above first, then removal per seat spec):
  ```sh
  cd /fast/scratch/hyaku/kasegi-r48 && rm -rf R48Probe44 && ls /fast/scratch/hyaku/kasegi-r48/ | grep -c R48Probe44; echo "scratch_gone_check_exit=$?"
  ```
  Expected: `0` (no remaining entry named R48Probe44).

No installs, no git/jj mutations, no background jobs, no delegation, no sibling/production writes. Findings are author-side form observations only; C1's promotion and semantic judgments remain independently held.
