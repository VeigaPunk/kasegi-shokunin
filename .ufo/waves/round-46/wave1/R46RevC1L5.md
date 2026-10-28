VERDICT: BROKEN

# R46RevC1L5 — C1 limb attack on L5 (append-only)

Target: `corpus/instruments/r46-c1-gate.py` `gate_list()` L5, lines 196-202, read with the frozen sentence in `claims.json` C1 `after` ("every BASE line kept (append-only)").

L5 as written: for each re-grounded entry `e`, `b` = BASE lines minus every line matching `^recheck:`, `t` = TREE lines minus the same filter; fail unless `t[:len(b)] == b and len(t) > len(b)`. Also `bool(reg)` is required, where `reg = gated(BASE) - gated(TREE)`.

Consequence: every line starting with `recheck:` is invisible to L5 in both files, in any position, and any count. L3/L4 read only `recheck_line()` (first match, line 78-83) and only check `~/`/`$HOME` and the `--entry` substring in the CD-stripped command, so the trailing `# comment` of a re-grounded entry's recheck line is read by no limb. L7 protects that comment only for still-gated entries (line 238).

## Method

Base: copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` (read-only use). Counter copied into `corpus/instruments/` of each tree. Aggregate run each time:
`python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <pure> --work <scratch>`
Honest control = both entries (`claim-gates.md`, `claim-package-contract.md`) re-grounded with >=6 rows over 2 anchor files (`corpus/instruments/claim-package-check.py`, `corpus/instruments/r46-c1-gate.py`), recheck replaced by `--entry`. Scratch removed on exit.

## Controls

1. Do-nothing (pure base as tree):
```
gate L5 pass=0 read=append-only=0
c1-gate fixed=1/7 exit=1
```
2. Honest re-ground of both entries (anchors located in committed bytes):
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

## Findings (what L5 accepts)

F1 — Recheck-line comment carries a claim; rewriting it passes all seven limbs (full green, the strongest result).
Edit: from the honest control, the trailing comment of `claim-gates.md`'s recheck line is changed from `# round-46 re-ground; prior gate was the lost-tree anchorcheck line` to `# on-restoration: base restored and re-verified 2026-10-28; entry no longer lost-tree; re-scope closed` (same for `claim-package-contract.md`). Diff vs honest for that entry is exactly that one line.
Output:
```
gate L5 pass=1 read=append-only=2
c1-gate fixed=7/7 exit=0
```
Claim changed: BASE line 125 of `claim-gates.md` says `base absent since 2026-09-28; not re-verifiable`. Host check, read-only: `test -d ~/Projects/bounties && echo PRESENT || echo ABSENT` printed `ABSENT (test -d ~/Projects/bounties rc=1)`, so the new "base restored and re-verified" status is false, and the counter reads 7/7 regardless.

F2 — Cheapest tree making L5 read pass=1 with the same claim rewrite (two edits: recheck line replaced by `true` with the rewritten comment, one blank line appended).
Recipe: in `corpus/knowledge/claim-gates.md`, replace the last line (BASE line 125) with
`recheck: true  # on-restoration: base restored and re-verified 2026-10-28; entry no longer lost-tree; re-scope closed`
and append one empty line. Run:
```
gate L5 pass=1 read=append-only=1
c1-gate fixed=2/7 exit=1
```
L5 needs one appended line (`or len(t) == len(b)`) and at least one un-gated entry (`bool(reg)`); `true` provides the second. L1-L4 and L6 go red, so this is the L5-only reading, not the full-green tree.

F3 — Rendered claim removed by filtered lines (no BASE line changed, no recheck line touched in its command).
Edit: honest tree; the first `recheck:` line moved to the top (kept as the gate line); two filtered lines `recheck: <!--` and `recheck: -->` inserted around BASE line 5 (`` `OK` only when zero errors. ``).
Output of counter: `gate L5 pass=1 read=append-only=2`, `c1-gate fixed=7/7 exit=0`.
Rendered with CommonMark reference `cmark`: `grep -c 'only when zero errors'` prints `1` on BASE HTML and `0` on tree HTML; tree HTML contains `<p>recheck: <!-- raw HTML omitted --></p>` as an artifact. Raw text still contains the claim; the rendered entry does not.

F4 — Appended retraction contradicts a BASE claim; L5 accepts because appends are allowed by design.
Edit: append `Correction (round 46): the OK gate above is retracted; claim-check reports OK while errors remain.` before the recheck line in `claim-gates.md`. Output: `gate L5 pass=1 read=append-only=2`, `c1-gate fixed=7/7 exit=0`. Not a rewrite of BASE bytes; it is a semantic contradiction only a non-author reading can see (kill_rule clause 3).

F5 — Second `recheck:` line shadows the gate (first-match in `recheck_line`); the BASE gated line stays byte-identical at EOF.
Edit: honest `--entry` line placed first, BASE line 125 kept at EOF. Output: `gate L5 pass=1 read=append-only=2`, `c1-gate fixed=7/7 exit=0`. L7 does not see it (only still-gated entries are byte-checked).

F6 — Position of recheck line moved to top and a prose-neutral second `recheck:` line inserted mid-prose. Output: `gate L5 pass=1 read=append-only=2`. Claims unchanged; this shows L5 is blind to recheck position/count (control for F1-F5, not a defect by itself).

## Constructions where L5 correctly fails (limb can fail alone)

With all other limbs green (honest control base), each of these reads `c1-gate fixed=6/7` with only L5 red:
- A1 prose rewrite of BASE line 5: `` `OK` only when zero errors. `` -> `` `OK` even when errors remain. `` :
```
gate L5 pass=0 read=bad=claim-gates.md
c1-gate fixed=6/7 exit=1
```
- A2 trailing space on BASE line 1 (title): `gate L5 pass=0 read=bad=claim-gates.md`, fixed=6/7.
- A3 change of BASE line 4 date `2026-09-28` -> `2026-10-28` (the same token recurs at BASE `verified-at: 2026-09-28`): `gate L5 pass=0 read=bad=claim-gates.md`, fixed=6/7. Recurrence does not help; L5 is index-based.
- A4b move one blank line across the Provenance heading: `gate L5 pass=0 read=bad=claim-gates.md`, fixed=6/7.
Do-nothing control: `gate L5 pass=0 read=append-only=0` (no regrounded entry).

## Constructions with no claim change (L5 pass, claims identical)

- A4 swap two identical blank lines: file sha256 prefix `beb600ab46f65612` identical to honest control; no-op.
- A10 CRLF on the whole re-grounded entry: `gate L5 pass=1 read=append-only=2`, fixed=7/7. Universal-newline `read()` erases line endings; harmless, but it is a whitespace-only pass.
- F6 above.

## Verdict basis

Five+ distinct genuine constructions pass L5 while a claim changes or is contradicted: F1 (comment rewrite, full green), F2 (cheapest, L5-only), F3 (rendered hide, full green), F4 (appended retraction, full green), F5 (shadowed recheck, full green), plus F6/A10 as position/line-ending exemptions. L5 is therefore not load-bearing for the recheck-comment channel. L5 does fail alone on prose edits (A1, A2, A3, A4b), so it is load-bearing for BASE prose lines.

## Suggested minimal fixes (not applied; L1 owns the tree)

- Require exactly one `recheck:` line per entry, and that it is the last line (closes F5 and the mid-prose filter in F3).
- For re-grounded entries, require the recheck line to equal the exact `--entry` command with no trailing text (closes F1 and F2), or fold the recheck line into the append-only comparison as a suffix rule.
- Fail on any `<!--` or `-->` in appended or filtered lines (closes F3 at the text level).
- F4 needs a non-author reading (kill_rule clause 3); no counter fix.

## Limitations

- Renderer: CommonMark reference `cmark` only; GitHub rendering of `recheck: <!--` was not checked.
- Re-ground rows in the honest control were written only to satisfy the per-entry checks; their semantic adequacy was not judged.
- Only `claim-gates.md` and `claim-package-contract.md` were tested; the other 22 gated entries were not varied.
- F1's false status claim is judged against the host's `~/Projects/bounties` (absent); the entry's own BASE text is the judged claim.
- The tree used is the pure base export, not the freeze commit; the freeze controls describe the same base reading.
- No commits, pushes, or git mutation; no fleet/sibling/MANIFEST/.ufo/state touched; scratch removed on exit.
