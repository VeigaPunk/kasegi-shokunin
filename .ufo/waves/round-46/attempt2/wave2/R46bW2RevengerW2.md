VERDICT: HOLDS

# R46bW2RevengerW2 — re-run of attempt-1 wave-2 probes P1/P2/P3 against the landed tree (round 46, attempt 2)

Tree under attack: `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (attempt-2 freeze / wave-1 integration), exported read-only with `git archive | tar -x` to scratch; the export is what was run.
Counter under test: `corpus/instruments/r46-c1-gate.py` v1.2 at fe0f56b, `sha256 95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7` (the report at .ufo/waves/round-46/wave2/R46W2MutSelftestC1.md records this hash as the live-HEAD v1.2; the attempt-1 pinned v1.1 was `99e0ee55…`).
Baseline: `914ca0b` ("round-45 verifier spot-check") — the same pure base the prior attempt used (`git diff 914ca0b fe0f56b -- corpus/instruments/claim-package-check.py corpus/instruments/fixtures corpus/knowledge/triage-thresholds.md` prints nothing; the entries' anchors are the same bytes).

## 0. What "landed counter+entry state" means here

The landed tree already IS the re-grounded tip: `git show fe0f56b:corpus/knowledge/claim-gates.md` and `…/claim-package-contract.md` each carry one `recheck:` line (the r46-c1-gate entry line), one `restoration-recheck:` line (the pure base's line verbatim), and a `## Re-ground (round 46)` section (25 and 21 G-rows; L6 counts mutants=46). So the P1/P2/P3 edits were applied to mutated copies of the REAL landed entries, not to a re-synthesized tip — a strictly stronger re-run than attempt-1's synthetic one.

## 1. Sanity + do-nothing control

P0, unmutated landed export vs pure (proves the limbs discriminate on this baseline):
```
$ python3 landed/corpus/instruments/r46-c1-gate.py --root landed --baseline pure --work work/p0
gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-exact=2
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
CONTROL, tree = baseline = pure:
```
$ python3 landed/corpus/instruments/r46-c1-gate.py --root pure --baseline pure --work work/ctl
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L3 pass=0 read=recheck-lines-exact=0
gate L4 pass=0 read=entry-mode-green-anchors-unchanged=0
gate L5 pass=0 read=append-only-restoration-kept=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
```
Identical to the attempt-1 control reading (`1/7`, L7 alone green).

## 2. Probes (recipes re-derived from .ufo/waves/round-46/wave2/R46W2MutSelftestC1.md §5)

Each probe is a copy of the landed tree with one edit; run `python3 <counter> --root trees/<P> --baseline pure --work <w>`. Each is also run under the matching single-line mutant counter (M08/M12/M18 rebuilt from the v1.1 recipes — M08 drops `and read(bp) == read(tp)` at l.280, M12 drops `or rest_ok != [want]` at l.297, M18 adds `"corpus/knowledge/"` to ANCHOR_DIRS at l.63 — the same mutation points exist verbatim in v1.2) so every acceptance is attributed to the mutation, not a malformed attack.

```
PROBE P1-anchor-file-bytes-changed   (landed claim-package-check.py +1 appended comment line, 802->803 lines; every token still located)
   v1.2-landed                       fixed=6/7 red=gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md   exit=1
   M08-L4-byte-identity-dropped      fixed=7/7 red=none                                                               exit=0

PROBE P2-restoration-line-deleted    (claim-gates.md l.126 `restoration-recheck: …` deleted; recheck line, rows, bytes untouched)
   v1.2-landed                       fixed=6/7 red=gate L5 pass=0 read=bad=claim-gates.md                              exit=1
   M12-L5-restoration-dropped        fixed=7/7 red=none                                                               exit=0

PROBE P3-row-anchored-in-knowledge-prose  (contract row G1 re-anchored on `corpus/knowledge/triage-thresholds.md:4` token `all read in full 2026-09-28`, a real line-4 substring)
   v1.2-landed                       fixed=4/7 red=gate L1 pass=0 read=gated=23 …;gate L2 pass=0 read=…regrounded=1 claim-gates.md;gate L7 pass=0 read=still-gated=23 changed=claim-package-contract.md   exit=1
   M18-anchor-dirs-add-knowledge     fixed=7/7 red=none                                                               exit=0
```

Landed v1.2 verbatim outputs (P3 red limbs):
```
gate L1 pass=0 read=gated=23 broken=0 lines=65/base=64
gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md
gate L7 pass=0 read=still-gated=23 changed=claim-package-contract.md
c1-gate fixed=4/7 exit=1
```

## 3. Result

All three probes are still rejected by the landed v1.2 counter against the landed entries, on the same limbs as attempt-1's v1.1 readings (L4 for P1, L5 for P2, L1+L2+L7 for P3; fixed counts 6/7, 6/7, 4/7 — identical). No acceptance on the landed state: no regression. Each rebuilt mutant accepts its own attack tree (7/7), so the rejections discriminate: the attacked clause is the thing that kills each tree.

## 4. Limitations and notes

- The P3 anchor in the original recipe named `triage-thresholds.md:1` with "a token copied from a line of that file" — line 1 (`# Triage thresholds — …`) carries no clean ≥8-char/alnum≥6 substring without `-`. First build anchored `:3`; the token `all read in full 2026-09-28` actually sits on line 4, so under M18 the row read `token-not-in-lines` and the mutant also rejected (attack input malformed, not evidence). Corrected to `:4`; both legs re-run: v1.2 red at L1/L2/L7 (4/7), M18 green (7/7). The off-by-one and the fix are the only deviation from the recipe, and it cannot produce a false "still rejected" (a bad token would only weaken the attack).
- The counter was run from the tree exports (`TOOL_LANE` = the export), so `classify()` executes the export's own instrument copies — matching attempt-1's protocol where each probe tree carried its counter copy.
- Scope: only P1/P2/P3 (the attempt-1 probes that were confirmed REAL holes with direct probes). M17 and M13 were "not probed" in attempt-1 either; not re-run here.
- Host: `~/Projects/bounties` absent → the L2/HOME discrimination is exercised by the selftest's home-cases, not here; grader HOME cannot flip L2 on this host either way.
- Tooling: nothing installed. Read-only git (`archive`, `show`, `diff`, `log`, `cat-file`, `ls-tree`). No commit/push/index/lane mutation. Scratch `/fast/scratch/hyaku/kasegi-r46/R46bW2RevengerW2` removed at exit.
