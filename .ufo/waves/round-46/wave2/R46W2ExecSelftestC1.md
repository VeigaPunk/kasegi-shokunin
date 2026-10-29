VERDICT: DRAFT-READY

Seat R46W2ExecSelftestC1 - C1 counter selftest updated to counter v1.1 (draft only; the lane was not edited).
Draft: `.ufo/waves/round-46/wave2/R46W2ExecSelftestC1.draft/r46-counters-selftest-c1.py` (sha256 `87e478563df7c547080c7fc142d9cff282c877bafd5fb477a4eef75d5f2bd2ae`; copy of `corpus/instruments/r46-counters-selftest-c1.py`, then edited). L1 integrates it over `corpus/instruments/r46-counters-selftest-c1.py`.

Inputs: tip export = `git archive 5437afeaf9b642c267bba3c31f00ae701e49da68` (counter `corpus/instruments/r46-c1-gate.py` sha256 `99e0ee555b68e5177f33e49e8024469608297a412171b190f66b1bba189475cc`, equal to counter-errata.md:16); base export `/fast/scratch/hyaku/kasegi-r46/L1/pure`; v1 counter = `git show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:corpus/instruments/r46-c1-gate.py` (sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`, equal to counter-errata.md:3).

## Pre-change reading (the wave-1 selftest against v1.1; it "read partly red")
`python3 <old selftest> --lane <tip export> --pure <pure>` last line: `selftest cases=47 failures=16`; first lines: `case TIP-7of7 ... L5=0 ... fixed=6/7 exit=1 ... verdict=UNEXPECTED` (the synthetic tip had no `restoration-recheck:` line, so L5 read `bad=claim-gates.md,claim-package-contract.md`); the nine `+stubbed-gate-copy` cases read `L1=0 L2=0 ... L4=1 ... verdict=UNEXPECTED` (v1.1 runs every instrument from the grader's own lane, so the tree's stubbed copy no longer matters); `L6-token-blanking-is-a-noop`, `X-anchor-self-via-symlinked-dir` read on other limbs; `X-rows-inside-code-fence`, `P-*` and `X-stubbed-gate-copy-alone` read UNEXPECTED because L5 was red.

## What changed in the draft
- Synthetic tip = v1.1 shape: recheck line is the one exact shape; `restoration-recheck: <BASE recheck command>` line (`rest_line()`, built from the pure export's `recheck:` line, exactly as r46-c1-gate.py:255-258 compares); anchored files untouched (byte-identical to BASE).
- Eight v1 false-greens, each now a named case that must read red on the named limb (all `L3=0` or `L4=0` or `L5=0` in the v1.1 run below): `L3-gate-incantation-in-comment` (comment trick), `L3-cd-tilde-home-target` (`cd ~/Projects/bounties && python3 ... r46-c1-gate.py --entry ...`), `L3-true-hash-gate-name` (`true # r46-c1-gate.py --entry ...`), `L3-shadow-recheck-line-above` and `-below` (+ `L3-base-line-kept-as-second-recheck`), `L3-dotslash-spelling-true-claim-red` (`./corpus/...` spelling = the same gate, red by the one-exact-shape rule), `L4-planted-new-anchor-hash-noop`, `L4-planted-anchor-in-place-edit`, `L4-tautological-anchor-file`, `L4-anchor-self-via-symlinked-dir` (planted anchors), `L5-restoration-recheck-dropped` (+ `-comment-rewritten`, `-twice`), `L5-hollow-gutted-entry`.
- New cases asked for: hostile lines in an UNRELATED entry (7 cases: `touch`, `; touch`, `$(touch ...)` argument to an allow-listed instrument, `env > marker`, `python3 -c`, a gated unrelated entry `recheck: touch <marker>`, `mkdir -p ~/Projects/bounties` under a scratch grader HOME); kind `hostile` asserts marker absent AND `L1=0` AND `broken>=1`. HOME override: `HOME-bounties-do-nothing` and `HOME-bounties-tip` run the counter with `HOME=<scratch>/Projects/bounties` present and assert `L2=0`, `fixed<7`. Duplicate (anchor, range): `L4-duplicate-anchor-range` (+ `L4-duplicate-token`). Token < 8 chars: `L4-token-shorter-than-8` (`MAX_SCA`, located in its line). Extra: `L6-overlapping-tokens-not-isolated` (token prefix of a sibling's token: blanking either reds both rows).
- Row-level cases keep their `+stubbed-gate-copy` twins but now target `L1,L2` (v1.1 ignores the tree copy of the gate).
- New kind `residual`: known mechanical limits stay visible instead of silently passing: `R-rows-inside-code-fence` (wave-1 F8; the counter's row reader is not markdown-aware; read 7/7) and `R-claim-text-unrelated-to-anchor` (claim cell swapped for an unrelated sentence, anchor and token kept; read 7/7). They print `verdict=RESIDUAL-FALSE-GREEN`, are listed in a `residual-false-greens=2 (...)` line, and are NOT counted in `failures`. If a later counter rejects them they print `RESIDUAL-NOW-RED`.
- Positive controls: `P-exactly-six-rows`, `P-prose-after-table`, `P-trailing-comment-on-recheck-line` (new), `X-stubbed-gate-copy-alone`.
- The harness never writes the real HOME: the only `mkdir ~/...` case runs with `HOME=<scratch>/fakehome-mkdirhome`. After both runs `ls ~/Projects/bounties` printed `ls: cannot access '/home/vgpnk/Projects/bounties': No such file or directory`.

## Run 1 - v1.1 counter on the committed tip export (re-run by me)
Command: `TMPDIR=<scratch>/w1 python3 st.py --lane <tip export> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/w1 --jobs 6` (st.py = the draft, sha256 equal, checked with sha256sum).
Last lines, exact:
```
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=2 (disclosed mechanical limits, not counted as failures: R-rows-inside-code-fence,R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
rc=0
```
Key lines of that run: `case TIP-7of7 L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 verdict=OK`; `case CONTROL-do-nothing L1=0 L2=0 L3=0 L4=0 L5=0 L6=0 L7=1 fixed=1/7 exit=1 verdict=OK`; `case HOME-bounties-do-nothing L1=1 L2=0 ... fixed=2/7 exit=1 targets=L2 verdict=OK`; `case HOME-bounties-tip L1=1 L2=0 ... fixed=2/7 exit=1 targets=L2 verdict=OK`; `case L3-cd-tilde-home-target ... L3=0 ... fixed=6/7`; `case L3-true-hash-gate-name ... L3=0 ... fixed=5/7`; `case L3-shadow-recheck-line-above ... L3=0`; `case L3-dotslash-spelling-true-claim-red ... L3=0`; `case L4-planted-anchor-in-place-edit ... L4=0 ... fixed=6/7`; `case L4-duplicate-anchor-range ... L1=0 L2=0 ... fixed=4/7`; `case L5-hollow-gutted-entry ... L5=0 ... fixed=6/7`; `case L5-restoration-recheck-dropped ... L5=0 ... fixed=6/7`; `case L6-overlapping-tokens-not-isolated ... L6=0 ... fixed=6/7`; `case H-hostile-touch-in-executing-entry L1=0 ... fixed=6/7 exit=1 targets=L1+broken verdict=OK` (same for the six other hostile cases; none prints `MARKER-CREATED`).

## Run 2 - frozen v1 counter (can the harness fail?) (re-run by me)
Command: same, plus `--counter <scratch>/v1/r46-c1-gate-v1.py` (the v1 bytes from `git show 9f23aab...`).
Last lines, exact:
```
residual-false-greens=2 (disclosed mechanical limits, not counted as failures: R-rows-inside-code-fence,R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=40
rc=1
```
Failing cases (`verdict` in the second column):
- FALSE-GREEN (v1 prints 7/7): `L3-gate-incantation-in-comment`, `L3-true-hash-gate-name`, `L3-gate-verdict-discarded-or-true`, `L3-gate-verdict-discarded-semicolon`, `L3-gate-only-echoed`, `L3-cd-target-not-the-lane`, `L3-cd-tilde-home-target`, `L3-root-override-absolute`, `L3-shadow-recheck-line-below`, `L3-base-line-kept-as-second-recheck`, `L4-duplicate-anchor-range` (+`+stubbed-gate-copy`), `L4-duplicate-token` (+stub), `L4-token-shorter-than-8` (+stub), `L4-planted-anchor-in-place-edit`, `L4-tautological-anchor-file`, `L5-restoration-recheck-dropped`, `L5-restoration-comment-rewritten`, `L5-restoration-recheck-twice`, `L6-overlapping-tokens-not-isolated`.
- UNEXPECTED (v1 rejects but on another limb): the eight `L4-*+stubbed-gate-copy` row cases and `X-section-heading-twice+stubbed-gate-copy` (v1 targets L4 only with the tree copy stubbed; v1.1 reads L1/L2), `L4-planted-new-anchor-hash-noop` (`L6=0`, L4 green), `L4-anchor-self-via-symlinked-dir` (`L6=0`, L4 green).
- EXECUTED (v1 runs the hostile line, `MARKER-CREATED:` printed): `H-hostile-touch-in-executing-entry`, `H-hostile-semicolon-in-executing-entry`, `H-hostile-cmdsubst-argument`, `H-hostile-env-dump`, `H-hostile-inline-python`, `H-hostile-in-gated-entry`, `H-hostile-mkdir-home-bounties` (the last under the scratch HOME: `marker=bounties`).
- Do-nothing discrimination: the same run prints `case TIP-7of7 ... fixed=7/7`, `case CONTROL-do-nothing ... fixed=1/7`, and the `P-*`/HOME cases OK, so v1's failures are the mutants, not the setup.
Cases that do NOT discriminate v1 from v1.1 (v1 already red): `L3-shadow-recheck-line-above`, `L5-hollow-gutted-entry`, `L5-body-line-*`, `L1-*`, the `L3-line-*` family. They still guard v1.1 against regression.

## Limitations
- Synthetic tip, not the real lane tip: rows/anchors are the harness's own (8 + 7 rows over `claim-package-check.py` and the exemplar fixture), the restoration lines come from the pure export. The 25/21 real rows and the real F28 entry are not exercised here.
- One run of each; v1.1 wall time about 4.5-5 min at `--jobs 6` on a loaded host (user time is large: every case re-runs L6's ~15 mutants). No flakiness repeat.
- `HOME-bounties-tip` reads `L1=1 L2=0 ... fixed=2/7` under a HOME that has `Projects/bounties`; the harness asserts only `L2=0` and `fixed<7`, not the whole limb vector.
- Two residual false-greens remain by design (disclosed in the errata: "v1.1 is still a mechanical grader"): a fenced table (F8) and a claim cell the counter cannot read. They are not failures here; L1 must decide whether to leave them as `residual` (my draft) or have the counter fixed.
- Hostile coverage is the shapes listed; `allowed()` accepts `python3 corpus/instruments/<x>.py <plain args>` and an allow-listed instrument that itself writes a file named by a plain argument would not be caught by this check (not tested; no such instrument was looked for).
- Tools installed: none. Git/jj: read-only (`git archive`, `git show`). Lane edited: no (draft + this report only). Scratch `/fast/scratch/hyaku/kasegi-r46/R46W2ExecSelftestC1` removed on exit.
