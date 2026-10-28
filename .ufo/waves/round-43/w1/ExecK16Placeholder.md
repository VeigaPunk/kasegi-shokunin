# ExecK16Placeholder — round 43, K16 placeholder-section promise check (RD42-4 class)

Seat: `ExecK16Placeholder` (leaf executor, kasegi-shokunin round 43). Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Scratch `S=/fast/scratch/hyaku/kasegi-r43/ExecK16Placeholder/` (removed before yield; disk guard read
before the pass: `/fast/scratch/hyaku` 25% used, 607.3G free). No tool installs, no network fetch, no writes outside
`$S` and this wave dir, no mutating git (only `git archive`, `rev-parse`).

## Deliverables

| path (relative to `kasegi-shokunin/`) | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK16Placeholder.sh` | 213 | `d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb` |
| `.ufo/waves/round-43/w1/ExecK16Placeholder.transcript.txt` | 147 | `0afd034c21c72b8e1251f17efc79883bd43a634d216e3969cd0d074c39de5d7c` |

The `.sh` is one sourceable function, `check_k16 <export-root>`: it prints exactly one stdout line
`payload=sections=<n>,promises=<p>,fenced=<k>,unresolved=<u> closed=0|1` and returns 0 (closed) or 1 (open).
`K16_VERBOSE=1` adds `K16 unresolved file=<rel> line=<n> heading=<text> clause=<name>` lines on stderr only.
It reads no file outside the root it is given and writes nothing.

## Shape (as landed in the limb header)

Scan `corpus/lessons/*.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`. A *section* is `^## ` outside a fenced block,
body to the next `^# ` or `^## ` outside a fence. A section *promises* when its **opening stanza** (first non-blank
body lines to the first blank line, fenced lines excluded) carries a promise clause:

- `schedule` — `when the <subject> reports`, subject 1–60 chars with no `; : , .` `"` `'` backtick bracket or pipe
- `to-be-filled` — `to be filled`
- `tbd` — `TBD` as a whole token
- `pending-wave` — `pending the <subject> wave` (same subject rule)
- `placeholder` — `the|this section|subsection|entry|block is|remains|stays a|an placeholder|stub`

Backticked and double-quoted spans are stripped before the clause test (a quoted clause is evidence *about* a
promise, never the promise). Fenced lines are never headings and never promises; promise vocabulary there increments
`fenced` and is ignored. A promise is *resolved* only when a later line **in the same file**, outside a fence,
carries the literal `Correction (round 43)` and names the heading (`heading text after "## "` as a raw substring, so
`## X`, `X` and `` `## X` `` all name it). `closed=1` requires `sections>0 ∧ promises>0 ∧ unresolved=0`, so erasing
the promise does not close the check.

## Evidence (one `set -x` tee, in the transcript)

Command: `bash $S/driver.sh > $S/transcript.raw 2>&1` after `. ./ExecK16Placeholder.sh`; trees are
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x`
into `$S/trees/<case>`, each mutated by one append only.

| case | tree mutation | payload | rc |
|---|---|---|---|
| base | none (real base export) | `payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0` | 1 |
| corrected | correction line appended to `corpus/lessons/round-42.md` | `payload=sections=491,promises=1,fenced=0,unresolved=0 closed=1` | 0 |
| fenced | corrected + new `round-43-fixture.md` whose promise line sits inside a fenced block | `payload=sections=494,promises=1,fenced=1,unresolved=0 closed=1` | 0 |
| wrongname | correction names `## Wave-3 falsification` | `…,unresolved=1 closed=0` | 1 |
| fencedcorr | correction itself wrapped in a fence | `…,unresolved=1 closed=0` | 1 |
| erased | the promise stanza deleted, correction kept | `payload=sections=491,promises=0,fenced=0,unresolved=0 closed=0` | 1 |
| echo | unquoted echo of the promise in a *later* stanza of another file | `payload=sections=493,promises=1,fenced=0,unresolved=0 closed=1` | 0 |
| early | correction placed **before** the heading | `…,unresolved=1 closed=0` | 1 |
| crossfile | correction in `SCORECARD.md`, not in the lesson file | `…,unresolved=1 closed=0` | 1 |

Base detail line, verbatim: `K16 unresolved file=corpus/lessons/round-42.md line=52 heading=Wave-2 falsification clause=schedule`.
Environment recorded in the transcript: `Python 3.14.8`, `GNU bash, version 5.3.20(1)-release`, base resolves to
`ab98fac9dce87130bc4f66de89e30650d63943dc`, limb sha256 `d7c33c9e…a74cb` (the driver re-hashes the file it runs).
Determinism: two consecutive runs over `$S/trees/base` from `/` printed byte-identical payloads, rc=1 both; a green
run prints exactly one stdout line.

## What the L1 needs to land

1. Wire `check_k16 <export>` as K16 in `r43-closure.sh` and print `K16 payload=… closed=<0|1>`; at base this is the
   required red and it names `corpus/lessons/round-42.md:52` / `Wave-2 falsification`.
2. Land the correction as **one line appended after line 52 in `corpus/lessons/round-42.md`, outside any fence**,
   carrying `Correction (round 43)` and the heading text — the shape the limb grades:

   ```
   Correction (round 43): the `## Wave-2 falsification` section above promised per-claim verdicts, attack tallies and per-family replay status `when the round-42 falsify wave reports`; no round-42 falsify wave was dispatched and no `.ufo/waves/round-42/wave2-results.json` exists, so the promise is withdrawn: the round-42 record stands at the thirteen-check closure and the r43 narrative-evidence checks K14-K19 grade the statement instead of the promise.
   ```

   That exact line is what the `corrected`/`fenced`/`echo` trees carry and what makes K16 print `closed=1`.
3. The three graded selftest limbs are the `base` (red), `corrected` (green) and `fenced` (green with `fenced=1`)
   trees above; the five mutants (`wrongname`, `fencedcorr`, `erased`, `early`, `crossfile`) fail as listed, so the
   limb is not a constant.
4. The whole check is one `python3 -` heredoc inside `check_k16` (`K16_PY` … `K16_PY`); the bash outside it is only
   the `local root` / payload / exit-code plumbing. If the r43 engine is the r42-style `exec python3 - <<'R43_ENGINE_PY'`
   form, lift that heredoc verbatim and have its `main()` return the same payload and 0/1; if it is limb-sourced,
   `. ExecK16Placeholder.sh` and call the function.

## Named limits

- Only the opening stanza is graded: a promise parked mid-section is invisible by design (the shape is "the section
  announces it will be filled later"), and that is what keeps a narrative echo of the defect from reddening the
  check — the `echo` case measures exactly that.
- The `placeholder` clause requires a copula about the section (`the section is a placeholder`); bare prose uses of
  the token (`placeholder row only`, `the placeholder token no longer occurs`) are deliberately not promises — at
  base they are 30+ lines across the four scanned targets and every one is discussion, not a promise.
- Resolution is a single literal line; a correction whose `Correction (round 43)` marker and heading name are split
  across two lines does not resolve. That is the frozen wording ("a line carrying … that names that section
  heading") and the landing shape above is one line.

## Residual state

Scratch `$S` removed; nothing written outside `.ufo/waves/round-43/w1/ExecK16Placeholder.{sh,transcript.txt}` and this
receipt; no lane source file touched; no installs recorded because none were made.
