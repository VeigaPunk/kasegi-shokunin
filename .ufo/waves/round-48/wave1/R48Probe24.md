# R48Probe24 — bounded grammar probe: HTML-comment wrap of SHONEN box 2

Seat: `R48Probe24` (leaf, no subagent dispatch, no background jobs). Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Frozen claim: `.ufo/waves/round-48/claims.json` at `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`.

## Scope and outcome

Probe: on a scratch copy of canonical `SHONEN.md`, wrap **box 2 only** (checkbox line plus its evidence line) in an HTML comment; keep the other three boxes byte-identical; run the frozen detector `corpus/instruments/shonen-form.py`. Also run the unmodified positive control.

Result: the mutant is **nonclean** with stable finding `SF-BOX`, exit `1`, matching the expected detector (two identical runs). The pristine control is `SF-CLEAN`, exit `0`. No defeat was found. No production bytes were modified.

Verdict on semantics: the transformation is **not** semantically permitted by the canonical form. The protocol requires the `SHONEN.md` seed to diff byte-identical modulo `<name>`, with marks confined to the box character plus one indented evidence line per box and no other prose (`PROTOCOL.md` §File contract, "Canonical form"). An HTML comment is extra prose, and it also hides box 2 from rendered markdown. The `SF-BOX` finding is therefore a correct form defect, not a fabricated one.

## Frozen predicate (read, not modified)

`corpus/instruments/shonen-form.py` (`grade()`): for each label in order it requires `lines[i]` to fullmatch `- \[([ ~x])\] <label>`, else returns `SF-BOX`. Box 2's checkbox line is at index 8, after the box 1 evidence line. With `<!--` at that position, the fullmatch fails and the detector returns `SF-BOX` before any evidence check. Exit mapping: `0` clean, `1` noncanonical, `2` unreadable.

Frozen hashes at probe time (read-only):

- `SHONEN.md` (production, working copy and HEAD `3d7e042` blob): `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`
- `corpus/instruments/shonen-form.py`: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`

## Commands and observed output

Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Probe24/` (created with `mkdir -p`, removed on exit).

Setup and before-hashes:

```
$ cp SHONEN.md .../R48Probe24/SHONEN.pristine.md; cp SHONEN.md .../R48Probe24/SHONEN.mutated.md
$ sha256sum SHONEN.md corpus/instruments/shonen-form.py SHONEN.pristine.md SHONEN.mutated.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.md
0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  corpus/instruments/shonen-form.py
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.pristine.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.mutated.md
```

Mutation (box 2 only; `edit` on the scratch copy, lines 7–10 of the mutant):

```
<!--
- [ ] At least one end-to-end domain task executed and logged in LOG.md
      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
-->
```

Diff, pristine vs mutant:

```
$ diff SHONEN.pristine.md SHONEN.mutated.md; echo DIFF_EXIT=$?
6a7
> <!--
8a10
> -->
DIFF_EXIT=1
```

Mutant, two runs (expected `SF-BOX`, exit 1):

```
$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe24/SHONEN.mutated.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT_MUTATED_RUN1=1
$ (same command, second run)
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT_MUTATED_RUN2=1
```

Unmodified positive control (expected `SF-CLEAN`, exit 0):

```
$ python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe24/SHONEN.pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT_PRISTINE=0
```

Note: the printed `canonical=1` is `int(code == 0)`, so `1` is the clean value. The `exit` field is the process exit code.

Additional distinct variants (same detector, each one edit, boxes 1/3/4 unchanged):

| Variant | Edit | Expected | Observed |
|---|---|---|---|
| A | box 2 checkbox line only as one-line `<!-- … -->` | `SF-BOX` exit 1 | `shonen-form canonical=0 finding=SF-BOX exit=1` |
| B | box 2 evidence line only wrapped in `<!--` … `-->` | `SF-BOX` exit 1 (box 3 label meets the comment line) | `shonen-form canonical=0 finding=SF-BOX exit=1` |
| C | preamble heading line wrapped as `<!-- # kasegi-shokunin — Promotion checklist -->` | `SF-PREAMBLE` exit 1 | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` |

Variant C agrees with the frozen selftest's persisted mapping `'commented': 'SF-PREAMBLE'` (`corpus/instruments/shonen-form-selftest.py` lines 12–20, fixture hash checked by that script). I did not run the selftest; this is a read of its expected table only.

Production bytes after probe (read-only verification):

```
$ git rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git status --porcelain -- SHONEN.md        (empty: no change vs HEAD)
$ sha256sum SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.md
$ git rev-parse HEAD
3d7e042ecbb1f17662f5042e8d3da3290722c031
$ git show HEAD:SHONEN.md | sha256sum
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  -
```

Only read-only git subcommands (`rev-parse`, `status --porcelain`, `show`, `log`) were used; no mutating git/jj.

## Round-47 route context (R1/R2)

- **R1 (SHONEN canonical-form drift, 13 accumulated blocks)** — superseded, not live at this HEAD. `git log -- SHONEN.md` shows `3d7e042 round-48: restore canonical checklist and dispatch 64 probes` after `29c02f9`. Production `SHONEN.md` is the 12-line / 761-byte canonical seed, with no `Round 4` headings. The positive control above therefore runs against the restored canonical bytes.
- **R2 (plain-target phrasing for `supersedes S074`)** — not in this probe's scope; I did not run or evaluate it.

## Limits and what was not verified

- One mutation family (HTML comment wrap) was exercised at box 2 and at the preamble, plus one single-line variant of box 2. Milestone "64 distinct bounded probes" is a fleet-level count across seats; this seat delivered **five** distinct executed runs (mutant ×2, pristine, variants A/B/C), so it does not claim 64.
- The detector is form-only. A `SF-CLEAN` verdict is not promotion, not independent verification, and not semantic truth of any box.
- No build, lint or selftest run was performed (not assigned). The selftest mapping was read, not executed.
- The frozen counter/predicate was not modified; no defeat was found, so none is reported as a fix.

## Tool installs

None. No tool was installed or updated by this seat.

## Scratch cleanup

Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe24/` holds the pristine, mutant and variant fixtures. Receipts are inline above; scratch removed on exit. No `/tmp` clones, no fleet/sibling/domain writes, no commit/push, no background jobs.
