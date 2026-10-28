# R44Critic10 — attack: can a dummy F26 row or an unrelated new source meet the C2 counter?

seat: critic (leaf, read-only) · lane: kasegi round 44 · item: mutation-minded attack on C2's counter
measurement base: committed bytes at `HEAD=66314015122b9aa32dc40f2f1815df56624c26d1` (`git rev-parse HEAD`), plus one
clean export `git archive HEAD … | tar -x -C $SCRATCH` and a deliberately mutated copy of that export.
No lane file was edited; the only file written is this report. No commit, push, git/jj/index mutation, no instrument install.

## Answer

**Yes — three times over.** A dummy F26 row, an unrelated (or fabricated) new source row, and an empty knowledge
file each move the frozen C2 counter to its after-value with no content. Two independent defects make the counter
unusable as written even for honest work: its first command cannot print `26` at all, and all three commands read the
**live working tree**, which at 16:00–16:06 today already read `26 / 70 / 63` with **zero** commits.

## E1 — the frozen counter's first command cannot measure its own baseline (blocking)

`claims.json:23` (C2 `counter`) starts with `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`.
The frontier table's status cell is the **third** column, not the second — `corpus/README.md:200`
`| id | topic | status | entry | sources | next |` — so the regex demands a row of shape `| F01 | admitted | …`.

```
$ cd <clean export of HEAD>
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md ; echo rc=$?
0
rc=1
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md ; echo rc=$?
25
rc=0
```

The frozen control uses the **second** form and recorded 25 (`.ufo/waves/round-44/controls/do-nothing.txt:10`).
So counter and control measure different things, and the counter reports `0` before *and* after: landing F26 in the
existing schema still yields `0`, i.e. C2 fails by its own frozen counter, or the lane silently substitutes an
unfrozen command (provenance defect, the same class as round-43 defect 1 — an unbacked summary figure).
`grep -c` also exits 1 on a zero count, so any runner with `set -e` aborts on the first leg.

## E2 — the counter reads the working tree, so uncommitted drafts already reach the after-state (blocking)

```
$ date -Is ; git rev-parse --short HEAD ; git status --porcelain --untracked-files=all -- corpus/
2026-10-28T16:06:03-03:00
6631401
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/knowledge-expected.txt
?? corpus/instruments/r44-routed-defects.py
?? corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
?? corpus/source-snapshots/round-44/S069.txt
?? corpus/source-snapshots/round-44/manifest.json

live (working tree) : frontier_control=26  sources=70  knowledge=63
committed (HEAD)    : frontier_control=25  sources=68  knowledge=62
```

`git show HEAD:…` for the same three quantities reproduces the freeze values exactly (25 / 68 / 62), so committed
bytes still discriminate; the **live** tree does not. A do-nothing replay executed in this tree today would print
`26 / 70 / 63` — the frozen after-state on all three legs — while nothing is committed. The do-nothing control's own
recorded `68` and `62` no longer reproduce against the tree it was measured in, so the control cannot be re-run as
written. (The uncommitted drafts are sibling work, not a defect of theirs; the defect is the counter's measurement base.)

## E3 — a dummy F26 row and an unrelated source satisfy the counter, on committed bytes

Clean export of HEAD, three dummy edits, then the frozen control's commands:

```
dummy README row : | F26 | placeholder topic (dummy) | admitted | knowledge/does-not-exist.md |  |  |
dummy SOURCES row: | S999 | Unrelated vendor homepage — https://example.com/ | docs | B | unrelated | none | … | rejected | …
dummy knowledge  : corpus/knowledge/dummy-unrelated-note.md  (one line, no source:, no recheck:)

CLEAN(committed)  frontier(claims)=0  frontier(control)=25  sources=68  knowledge=62
DUMMY             frontier(claims)=0  frontier(control)=26  sources=69  knowledge=63
```

`26 / 69 / 63` is exactly C2's after-state, produced by a row pointing at a non-existent entry, a source that is
unrelated and **rejected**, and a knowledge file with no content. The first grep is line-based over the whole file, so a
row that is not even in a table counts:

```
$ (append to README)  ```\n| F26 | dummy row inside a fenced example | admitted | knowledge/nope.md | | |\n```
fenced-block dummy row -> counter = 26 rc= 0
line: 615:| F26 | dummy row inside a fenced example | admitted | knowledge/nope.md | | |
```

## E4 — the source leg does not measure "newly opened tier-A", and nothing rejects a fabricated row

Committed status/tier split of `corpus/SOURCES.md` (`awk -F'|'` over `S[0-9]{3,}` rows):

```
A/mined 54   A/rejected 8   B/mined 1   B/rejected 3   C/rejected 2   = 68
```

The counter counts **any** `S###` row, so 13 already-`rejected` rows are inside the 68 and one more rejected tier-B row
is all it takes (my S999 → 69). Worse, a fabricated `A/mined` row with no capture passes every committed instrument:

```
$ append to export/corpus/SOURCES.md:
  | S998 | Fabricated tier-A source with no capture — https://example.invalid/nothing | docs | A | invented scope | none | nothing | mined | 2026-10-28 | none | none |
frozen counter now: 69
$ python3 corpus/instruments/capture-binding-check.py --root $PWD
AUDIT records=57 with_url=57 … snapshot_dirs=19 missing_manifest=0 digest_unpinned=0 orphans=1
records=57 bound=57 unbound=0
rc=0
```

`capture-binding-check.py` binds records→rows (rule B: `no-row`, `dup-id`, `rejected-row-anchor`); `grep -rn
'no-capture|missing-capture|unbound-row' corpus/instruments/*.py` → no hits, i.e. there is **no** rows→records rule, so
the "its captured source" half of C2's kill rule has no instrument behind it except the frontier entry's own recheck line.

## E5 — the discriminating instruments already exist and reject every dummy shape

`frontier-recheck-count.py --root <mini>` (read-only, no network in these fixtures):

```
mini-dummy-only       FRONTIER-FAIL F26 status=admitted ids=- problems=missing-pass-line
                      FAIL F26 knowledge/does-not-exist.md problems=missing-entry            rc=1
mini-borrowed-entry   FRONTIER-FAIL F25,F26 …  DUPLICATE-ENTRY F25,F26 knowledge/cve-json-record-format.md   rc=1
mini-not-admitted     FRONTIER-FAIL F26 status=staged problems=status-not-admitted             rc=1
mini-fenced (row only inside ```)  FRONTIER-FAIL F26 … problems=missing-entry                 rc=1
--selftest            selftest cases=6 failures=0                                            rc=0
```

`recheck-audit.py --selftest` shows the expected-list limb that kills a dummy knowledge file once the committed list
(62 at HEAD) is pinned: `selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok`.
And frontier Rule B ("the named manifest must exist, be schema-valid, and list every one of those ids") forces the new
source to be captured and re-verifiable, which is the leg the frozen grep lacks.

## Residual limitation — do not overclaim from the harness either

A **byte-clone** entry under a new filename is not caught; `DUPLICATE-ENTRY` fires on identical realpath only:

```
mini-cloned-entry  a.md and b.md byte-identical: True
                   rc=1  DUPLICATE-ENTRY present: False
```

So even the hardened counter cannot prove a *topical* new move; that stays with the non-author admit/reject spot-check
that C2's kill rule already names. C2's **kill rule** is therefore sound as written; its **counter** line is not.

## Impacted axes

- `coverage` (C2) — direct: the frozen counter cannot reach `26` (E1) and is satisfied by dummies (E3/E4); the after-state
  is unprovable by the artifact the claim names.
- `depth:verifiability` (C1) — indirect: C2's counter is the round's frozen evidence instrument; an instrument that prints
  a superseded literal is the round-43 defect-1 class recurring in a new file.

## Smallest safe correction (append-only; no frozen predicate widened)

1. **Freeze erratum** under `.ufo/waves/round-44/` naming `claims.json:23`'s first regex as a literal that measures `0`
   on the committed table, and `controls/do-nothing.txt:10`'s regex as the one that measured `25`; record both values
   with `git show HEAD:corpus/README.md | grep -cE …` so the erratum is reproducible from committed bytes.
2. **Pin the base**: all three legs run against a clean export (`git archive HEAD | tar -x -C <export>`), never the live
   tree — E2 shows the live tree drifts to the after-value with zero commits.
3. **Make the counter the existing gates** over that export, instead of three greps:
   `frontier-recheck-count.py --root <export>` (exit 0 ⇒ every admitted row owns a passing, source-bound entry),
   `recheck-audit.py --root <export>` (expected-list equality ⇒ no extra/dummy `.md`), and the source leg as an
   `A/mined` **id-set diff** against the baseline (54 at HEAD), not a raw row count.
4. If the counter must stay shell-only, the minimum added predicates are: the F26 entry cell resolves to an existing
   file unique by realpath, and the new `S` id appears in that entry's `source:` line and in the row's `used-by` cell.

## Do-nothing discrimination

Committed bytes at `HEAD=6631401` still print `25 / 68 / 62`, identical to the freeze at `5ab3a60` — do-nothing at a
pinned base cannot reach F26, so the control's *intent* holds. It fails only if the replay runs against the live tree
(E2). The controls were not re-executed here beyond the three greps; `sources-census.sh` was not run (its committed
exit-0 with the S028/S029 duplicate warnings is cited from `do-nothing.txt`, not re-measured).

## Limitations

- Findings are about the **counter and controls**, not about sibling content; I did not grade the drafted F26 row or the
  drafted knowledge entry, only used their presence as a measurement-base witness.
- `frontier-recheck-count.py` and `recheck-audit.py` were exercised through their self-tests and miniature fixture
  lanes; I did **not** run either against the real lane (it would execute 25 live recheck lines and would run a
  sibling's gate, contrary to the closure rule).
- `capture-binding-check.py` was run on a clean export (records=57, exit 0) and on the export plus a fabricated row;
  that is the only real-lane-sized instrument run in this seat.
- Scratch `$HYAKU_SCRATCH` was unset, so scratch was created under the lane's ignored tree at
  `kasegi-shokunin/.ufo/scratch/kasegi-r44/R44Critic10/` and deleted on exit (see the lane's scratch-removal note).
- No tool was installed or updated in this seat.
