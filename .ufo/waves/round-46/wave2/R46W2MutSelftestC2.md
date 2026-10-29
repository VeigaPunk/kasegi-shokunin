VERDICT: BROKEN

# R46W2MutSelftestC2 — mutation probe of the C2 selftest against the C2 counter (round 46, wave 2)

Scope: `corpus/instruments/r46-counters-selftest-c2.py` (selftest) against mutants of `corpus/instruments/r46-c2-gate.py` (counter v1.1), at the integrated tree 5437afeaf9b642c267bba3c31f00ae701e49da68 (exported with `git archive`; the lane HEAD is 0d121a2, a spec commit on top of 5437af; `git diff --quiet HEAD -- corpus/instruments/r46-c2-gate.py corpus/instruments/r46-counters-selftest-c2.py` printed nothing, so the two C2 files are byte-identical at HEAD). Read-only on the lane; all work in scratch, removed on exit. Nothing committed, nothing staged.

Pins observed in the export: `r46-c2-gate.py` sha256 b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621 (matches errata); `r46-counters-selftest-c2.py` sha256 ac9f638ae342916f8e1fb03f8d1e28b7eeb49750eada0e5999abec929b153656; `S073.txt` 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930; `manifest.json` 01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34; `source-recheck.py` fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003.

## 1. The committed selftest does not pass against the committed counter (finding, HIGH)

Command (selftest run unmodified, `--lane` = the 5437af export, `--pure` = the pure base):
```
HYAKU_SCRATCH=<scratch>/hs TMPDIR=<scratch>/tmp python3 corpus/instruments/r46-counters-selftest-c2.py --lane <export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure
```
Printed (last line): `selftest cases=95 failures=62`. Sample:
```
FAIL control ctl-complete-tree fixed=6/7 failing=['G2']  <- control-not-7/7 failing=['G2']
       gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=3/4 table-rows=7 xrefs=2/2
```
Every one of the 62 failures is G2 (the `collateral-unexpected=['G2']` / `control-not-7/7 failing=['G2']` reason). Cause: counter v1.1 requires each entry section to carry >= 25 words (`r46-c2-gate.py:202`, `sect_words(body, sct) >= (12 if ... else 25)`), but the selftest fixture's `## Limits` section counts 22 words, and the selftest was not updated with that errata (C2-E1). So the selftest's own 11 controls (`ctl-*`) cannot read 7/7 on the committed counter, and every mutant "fails" for the wrong reason. A selftest that fails 62/95 on the tree it certifies cannot discriminate any mutant; the mutant verdicts below are therefore taken against a scratch-only fixture fix (section 2).

## 2. Scratch-only fixture fix and the residual baseline

Scratch copy of the selftest (`selftest-patched.py`), one line added to `entry_text()` (the `## Limits` bullets) and nothing else (`diff` output):
```
166a167
>         "- The page is one platform's wording at one capture date, so the row must be re-read before reuse.",
```
Baseline on that copy against the unmutated counter:
```
FAIL mutant  mut-fabricated-quote-in-fenced-block fixed=7/7 failing=[]  <- ACCEPTED-targeted-gate-passes=['G5']; tree read 7/7
FAIL mutant  mut-census-bad-kind fixed=5/7 failing=['G3', 'G7']  <- collateral-unexpected=['G3']
selftest cases=95 failures=2
```
Both residual failures are selftest-side expectations, not counter gaps:
- `mut-fabricated-quote-in-fenced-block` (selftest line 365) expects G5 to reject a fabricated quote inside a fenced code block; the counter's `live_lines()` (`r46-c2-gate.py:114-126`) excludes fences by design (docstring: "live lines only (no HTML comment, no fence)"). The case contradicts the counter's own stated design.
- `mut-census-bad-kind` (selftest line 440) declares `allow` for G7 only; the kind change also trips G3 (`r46-c2-gate.py:243`, `row[2] != "docs"`), which is correct behaviour.

Do-nothing discriminator (`--do-nothing-control`, stub that prints 7/7): `selftest cases=95 failures=84` (83 mutant cases + the null case FAIL; all 11 controls pass, as the do-nothing stub intends). So the selftest does discriminate a do-nothing counter.

## 3. Mutant battery (24 counter mutants + do-nothing), run against the patched copy

Each mutant is one exact-string substitution of `r46-c2-gate.py` (asserted to occur once; generator in scratch), placed in a copy of `corpus/instruments/` so `TOOL_ROOT` still resolves `source-recheck.py`; each mutant then ran the full 95-case selftest with `--counter`. `caught=1` iff the mutant run has at least one FAIL line that is not in the baseline FAIL set (`mut-census-bad-kind`, `mut-fabricated-quote-in-fenced-block`). Printed lines (from `summarize`/`final-lines`):
```
mutant=flip-28-row-count-to-27 selftest-failures=78 caught=1
mutant=flip-28-row-count-to-29 selftest-failures=78 caught=1
mutant=drop-located-quote-test selftest-failures=7 caught=1
mutant=drop-body-lines-window selftest-failures=2 caught=0
mutant=drop-distinct-quote-test selftest-failures=2 caught=0
mutant=drop-exempt-entry-handling selftest-failures=76 caught=1
mutant=accept-straight-quotes-uncited selftest-failures=2 caught=0
mutant=accept-straight-quotes-unlocated selftest-failures=2 caught=0
mutant=skip-census-g7 selftest-failures=6 caught=1
mutant=range-width-unbounded selftest-failures=2 caught=0
mutant=word-cap-25-to-40 selftest-failures=4 caught=1
mutant=table-rows-6-to-5 selftest-failures=3 caught=1
mutant=g3-tier-check-removed selftest-failures=3 caught=1
mutant=g4-quote-count-8-to-7 selftest-failures=2 caught=0
mutant=g1-duplicate-id-check-removed selftest-failures=3 caught=1
mutant=g6-nested-md-check-removed selftest-failures=2 caught=0
mutant=g3-used-by-check-removed selftest-failures=4 caught=1
mutant=g2-xref-check-removed selftest-failures=7 caught=1
mutant=g5-uncited-curly-not-counted selftest-failures=3 caught=1
mutant=g5-cores-4-of-5 selftest-failures=5 caught=1
mutant=g6-content-pin-removed selftest-failures=3 caught=1
mutant=g2-verified-at-unchecked selftest-failures=3 caught=1
mutant=g2-section-words-25-to-1 selftest-failures=2 caught=0
mutant=g3-scope-words-8-to-1 selftest-failures=2 caught=0
control=do-nothing selftest-failures=84 caught=1
```
Caveat on "caught": flip-28 (both), drop-exempt, skip-census and several others are caught only through controls or unrelated cases (e.g. flip-28 fails `ctl-complete-tree`); they show the counter is exercised, not that the specific rule has its own case. 15 of 24 counter mutants are caught; 9 are not.

## 4. Uncaught counter mutants — what is and is not covered (each re-run; quoted)

**(a) drop-body-lines-window** (`r46-c2-gate.py:296`, `a >= BODY[0] and b <= BODY[1]`). No counted case. The window is exercised only by a probe, and the probe flips under the mutant:
```
baseline:  probe       probe-core-quote-from-page-chrome-line fixed=6/7 failing=['G5'] (rejected) -- a located quote from non-article page chrome
mutant:    probe       probe-core-quote-from-page-chrome-line fixed=7/7 failing=[] (ACCEPTED) -- a located quote from non-article page chrome
```
Coverage gap: a located quote outside lines 556-583 is accepted if the probe is not counted.

**(b) accept-straight-quotes-uncited** (`r46-c2-gate.py:288`, `straight = []`). No counted case. Probe `probe-straight-quoted-fabrication` is rejected by the real counter and ACCEPTED under the mutant, so the probe's own note ("straight-quoted fabricated text is invisible to G5") is stale for v1.1; the counter does reject it. Gap: uncited straight-quoted prose is untested as a counted case.

**(c) accept-straight-quotes-unlocated** (`r46-c2-gate.py:296` with straight cited spans passing unlocated). Re-run on a fixture (entry bullet `- The page says "GitHub guarantees a response within 24 hours" (`S073.txt:577`).`, built by importing the patched selftest's own `build()`):
```
counter v1.1:  gate G5 pass=0 read=spans=8 located=7 failed=1 uncited=0 cores=5/5
mutant:        gate G5 pass=1 read=spans=8 located=8 failed=0 uncited=0 cores=5/5
```
Gap: no counted case has a fabricated cited straight quote.

**(d) range-width-unbounded** (`r46-c2-gate.py:296`, `b - a <= 11`). Re-run with the anyone quote cited `S073.txt:560-575` (15 lines, inside the body window):
```
counter v1.1:  gate G5 pass=0 read=spans=7 located=6 failed=1 uncited=0 cores=5/5
mutant:        gate G5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
```
Gap: the <=12-line citation rule (errata C2-E4) has no counted boundary case.

**(e) g2-section-words-25-to-1** (`r46-c2-gate.py:202`). Re-run, Limits section reduced to 24 words, then 25 words (word counts from the gate's own `sect_words`):
```
24 words  counter: gate G2 pass=0 read=... sections=4/4 full=3/4 ...   c2-gate fixed=6/7 exit=1
24 words  mutant:  gate G2 pass=1 read=... sections=4/4 full=4/4 ...   c2-gate fixed=7/7 exit=0
25 words  counter: gate G2 pass=1 read=... full=4/4 ...                c2-gate fixed=7/7 exit=0
```
The 25-word threshold is the rule the selftest itself failed on (section 1); after the fixture fix nothing tests its boundary. Gap: no 24/25-word control or mutant.

**(f) g3-scope-words-8-to-1** (`r46-c2-gate.py:244`). Re-run with the S073 scope cell cut to `Reporter-side flow only` (4 words):
```
counter v1.1:  gate G3 pass=0 read=bad=scope-words
mutant:        gate G3 pass=1 read=row-S073=ok
```
Gap: no counted case for the scope-words floor.

**(g) g4-quote-count-8-to-7 and drop-distinct-quote-test** (`r46-c2-gate.py:261-276`). These are EQUIVALENT under the real manifest pin: the manifest sha check (`:261`) returns before the count and distinctness rules run, and any manifest that passes the pin is the pinned one (8 distinct quotes). Re-run with the manifest pin relaxed to each variant's own sha (env `R46_PINS_OVERRIDE`, the selftest-only mechanism), which isolates the rules:
```
drop Q1 (7 quotes):   counter G4 pass=0 read=recheck-rc=0 quotes-ok=7 ...   mutant G4 pass=1 read=recheck-rc=0 quotes-ok=7 ...
duplicate Q2 as Q9:   counter G4 pass=0 read=recheck-rc=0 quotes-ok=9 ...   mutant G4 pass=1 read=recheck-rc=0 quotes-ok=9 ...
```
With the real pin both variants read `G4 pass=0 read=manifest-not-the-pinned-bytes` (counter and mutant alike). So the rules are unreachable under the shipped pins; they are live gaps only if the pin is relaxed, and no counted case tests them either way.

**(h) g6-nested-md-check-removed** (`r46-c2-gate.py:320`). EQUIVALENT. With names==65 and everything==65 (both required by `:320`), no subdirectory can exist at depth 1, so no nested `.md` can exist; `len(everything)==65` alone rejects any subdirectory. Re-run with `corpus/knowledge/sub/x.md` added:
```
counter v1.1:  gate G6 pass=0 read=knowledge=65 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
mutant:        gate G6 pass=0 read=knowledge=65 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
```
The probe note "G6 counts only maxdepth-1" (selftest line 452) is stale: the counter rejects the subdirectory file (`probe-extra-knowledge-subdir-file ... (rejected)`).

## 5. Harness and doc defects found while running (for the L1 to route)

- `r46-c2-gate.py:66` comment says "a null value disables that one pin". True for `base-knowledge-content`, `S073-row`, `entry`, `source-recheck.py` (guarded by `is not None`), false for `manifest.json` (`:261`, plain `!=`) and `S073.txt` (`:239`, plain `!=`). Re-run:
```
R46_PINS_OVERRIDE={"manifest.json": null}  ->  gate G4 pass=0 read=manifest-not-the-pinned-bytes
R46_PINS_OVERRIDE={"manifest.json": <sha of the same file>}  ->  gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
```
- `r46-c2-gate.py:179` `if len(raw) != 1 or (False):` is dead code.
- Selftest `:276` hardcodes the scratch dir name `kasegi-r46/R46ExecSelftestC2` (another seat's name). I ran it with `HYAKU_SCRATCH` pointed inside my own scratch so nothing was written under that name.
- Probe notes at selftest lines 447-466 are partly stale against v1.1 (straight-quote probe, subdir probe; see 4b, 4h).
- The counter's G7 calls the fleet-level `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`r46-c2-gate.py:54`); this is outside the lane and was run read-only.

## 6. Summary of gaps for the L1

Selftest coverage is missing for: body window (4a), uncited straight-quoted prose (4b), fabricated cited straight quotes (4c), citation range width (4d), section-word threshold boundary (4e), scope-words floor (4f). Quote-count and distinctness (4g) are unreachable under the pin and untested even when the pin is relaxed. Nested-md (4h) is redundant. Fixing the selftest fixture for C2-E1 (section >= 25 words) is a prerequisite: at 5437af the selftest reports 62 failures.

## Limitations

- Mutants are single exact-string substitutions (24 counter mutants, one do-nothing). The battery is not exhaustive over the counter; a surviving mutant is only a surviving mutant of these 24 edits.
- The patched selftest (section 2) is a scratch-only copy with one fixture line added; it is not a proposed fix to the lane file. Probe verdicts printed by the patched copy are as the copy computes them.
- The verification fixtures in section 4 were built by importing the patched selftest's own `build()`/`entry_text()`, then editing single bytes; they are my edits, not the selftest's cases.
- Counter and selftest were exercised at the 5437af export, not at lane HEAD 0d121a2 (C2 files unchanged between them).
- `caught` is a set difference against the baseline FAIL set; a mutant caught only through controls (flip-28, drop-exempt, skip-census in part) is caught for coarse reasons.
- No pacman, no installs, no git mutation; scratch under $HYAKU_SCRATCH/kasegi-r46/R46W2MutSelftestC2 removed on exit.
