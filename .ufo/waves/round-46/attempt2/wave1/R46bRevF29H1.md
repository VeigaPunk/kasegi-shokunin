# Seat R46bRevF29H1 — attack on r46-f29-gate.py limb H1 (frontier table)

VERDICT: BROKEN

Limb attacked: `corpus/instruments/r46-f29-gate.py` H1 (lines 159–179), on positive
fixture trees built by `.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive`.
Every attack tree is byte-identical to the positive tree except `corpus/README.md`
(H1's only input — verified with `diff -rq positive <tree>` for all 9 trees), so all
other limbs stay green by construction and a green H1 line means the full gate reads
`f29-gate fixed=7/7 exit=0`.

Baseline (do-nothing control, re-run by me):

    $ python3 corpus/instruments/r46-f29-gate.py --root .../positive
    gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
    ...
    f29-gate fixed=7/7 exit=0

## Findings (false-greens: tree carries an H1 defect, gate prints pass=1)

### F1 — duplicate admitted rows in an appended amendment block (whole 29-row frontier duplicated)
Recipe: append after the frontier table a heading `### Amendment 2026-10-29 — re-affirmed frontier`
plus a second copy of all 29 admitted rows, each prefixed with ONE space
(`" " + row`). `frontier()` (`r46-f29-gate.py:137-146`) only matches `re.match(r"^\| F\d+ \|", ln)`
on un-stripped lines, so leading-space rows are invisible to it; `live_lines()` keeps them
(its `<!--` skip at line 123 does not apply). Human-visible admitted F-rows: 58; gate-seen: 29.

    tree a2-indented-dup-block:
    gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
    f29-gate fixed=7/7 exit=0

### F2 — id collision: `F2 9` ghost row (also `f29` lowercase, also `F29`+ZERO WIDTH SPACE)
Recipe: append `| F2 9 | ghost duplicate of the F29 frontier row | admitted | corpus/knowledge/ghost-holder.md | S074 | collision probe |`.
The id cell `F2 9` fails `^\| F\d+ \|` (space between digits) and fails the raw
`^\| F29 \|` one-line recount, so it is never in `rows`, never in `dup` (exact-string `set()`),
and never in `raw` — yet renders as a distinct admitted frontier row in the README.

    tree a3-id-collision-f2-space-9:
    gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
    f29-gate fixed=7/7 exit=0

Variant recipes, same green line (`gate H1 pass=1 read=rows=29 admitted=29 F29=admitted`,
`f29-gate fixed=7/7 exit=0`):
- tree a8-lowercase-id: append `| f29 | ghost duplicate ... | admitted | ...` (case-fold blind;
  the regex has no re.IGNORECASE).
- tree a9-zwsp-id: append `| F29\u200b | ...` (id cell repr verified `' F29\u200b '`;
  `\u200b` breaks the `\d+ \|` boundary so the row is invisible while printing as `F29`).

### F3 — entry-cell aliasing (substring vs "names exactly ENTRY")
Recipe: rewrite the live F29 row's entry cell from
`corpus/knowledge/github-repository-security-advisories.md` to
`corpus/knowledge/github-repository-security-advisories.md (mirror entry: corpus/knowledge/github-private-vulnerability-reporting.md)`.
H1 checks only `ENTRY not in f29[0][3]` (`r46-f29-gate.py:172`) — a substring test — so a cell
that names ENTRY **and** a second (here nonexistent) mirror path passes. The gate docstring
(H1 spec) says "its entry cell names exactly ENTRY"; the code does not enforce exactness, and
the `shared` guard at line 174 exempts the F29 row itself.

    tree a5-entry-cell-aliasing:
    gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
    f29-gate fixed=7/7 exit=0

### F4 — a second F29 row inside a one-line HTML comment
Recipe: append `<!-- | F29 | ghost row smuggled inside a one-line HTML comment | admitted | corpus/knowledge/ghost.md | S074 | -->`.
`live_lines()` (line 123) drops any line whose *stripped* form starts with `<!--`, so the
ghost row never enters `rows` and never enters the `raw` recount (`r46-f29-gate.py:176-178`,
`len(raw) != 1`); the README bytes contain two `| F29 |` table lines, the gate sees one.

    tree a6-comment-oneline-f29:
    gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
    f29-gate fixed=7/7 exit=0

## Caught controls (naive variants the gate DOES catch — discrimination evidence)

- tree a1-naive-dup-control (append the unmodified F29 row again — this is the receipt's
  known `duprow` class):
  `gate H1 pass=0 read=rows=30 admitted=30 dup=1` / `f29-gate fixed=6/7 exit=1`
- tree a4-unicode-digits-control (append `| F２９ | ...` fullwidth digits — caught by the
  row count, NOT by `dup`, since `\d` matches Unicode decimal digits and `２９` is a distinct string):
  `gate H1 pass=0 read=rows=30 admitted=30 dup=0` / `f29-gate fixed=6/7 exit=1`
- tree a7-comment-multiline-control (row on its own line inside a `<!-- ... -->` block —
  the interior line is treated as LIVE, so it trips counts and dup):
  `gate H1 pass=0 read=rows=30 admitted=30 dup=1` / `f29-gate fixed=6/7 exit=1`

Discrimination: the do-nothing positive re-run reads 7/7; the three naive mutations flip H1 red;
only the regex-evasion mutations stay green. The green results are therefore attributable to the
H1 blind spots, not to harness noise.

## What the R50 receipt does not list

`controls/f29-r50-receipt.txt` covers exactly three H1 mutants — H1a counts-loose, H1b raw-loose,
H1c src-boundary — and its H1 defects are only `duprow` and `fencedf29` (both matching-regex
variants, disclosed NOT-SHOWN as shadowed). It lists NO tree for: indented/amendment-block
duplicates, id normalization (case fold, internal space, zero-width space), Unicode-lookalike
evasion, entry-cell substring aliasing, or one-line-comment smuggling. Findings F1–F4 are outside
the receipt's mutant set; F2/F3/F4 are not "shadowed" clauses but full bypasses of the dup,
entry-cell and one-live-row checks respectively.

## Limitations

- All trees are synthetic README mutations on the fixture's positive tree; I did not touch the
  lane repo (read-only seat) and did not test against the fleet README.
- The blind spots are coverage gaps in H1 as specified; whether indented table rows "count" as a
  rendered amendment is a markdown-rendering judgment (CommonMark accepts ≤3 leading spaces as a
  table row). The gate's own docstring treats the README table as the frontier of record, so a
  human-visible duplicate admitted row is a defect in the record even if some renderer folds it.
- F3's mirror path was chosen nonexistent to keep H6 name pins green; an existing mirror path
  would also pass H1 but was not needed to show the substring/aliasing gap.
- I ran the gate as `python3 <gate> --root <tree>` (no --work); H1 takes no scratch.
- No new tools installed; none needed (python3 stdlib only).
