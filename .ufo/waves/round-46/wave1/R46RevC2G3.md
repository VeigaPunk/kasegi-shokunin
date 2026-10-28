VERDICT: BROKEN

# R46RevC2G3 — attack on C2 gate G3 (`def g3`, SOURCES row S073)

Seat: R46RevC2G3 (reviewer, leaf, read-only except this report). Target: `corpus/instruments/r46-c2-gate.py` (sha256 `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`, equal to `c2-gate-sha256` in `.ufo/waves/round-46/freeze.txt` and to the worktree copy). Attacked the frozen predicate only. Frozen tree = `git archive 9f23aab corpus` into scratch; no repo, index, or git state was mutated.

## What G3 checks (the frozen predicate)

`corpus/instruments/r46-c2-gate.py:209-234` (`def g3`):
- `hits` = live registry lines matching `^ {0,3}\|\s*S073\s*\|`; exactly one hit, split into cells, must have **11** cells (line 215).
- `row[3] == "A"` (tier), `row[7] == "mined"` (status), `row[8] == "2026-10-28"` (opened), `URL in row[1]` (source, substring), `p in row[10]` (used-by = README F28 entry path, substring), `snap_sha in row[5]` (anchor, substring) (lines 228-233).
- `PINS["S073-row"]` is `None` (line 60), so the row bytes are not pinned. The docstring says so explicitly (lines 33-34: "the F28 / S073 row bytes are NOT pinned").
- `registry_lines` (136-145) counts every line after any `## Registry...` heading (regex `^ {0,3}## Registry\b`, so `## Registry changes` also matches) and stops only at the next `## ` heading. `# ` and `### ` headings do not end the section. `live_lines` (112-124) drops fenced and HTML-commented lines.
- Cells read by G3: 1, 3, 5, 7, 8, 10. Cells 2 (kind), 4 (scope), 6 (teaches), 9 (recheck) are never read. The anchor cell is checked only for containing the sha; the locator text is not checked.

Cell map from the live header `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (`corpus/SOURCES.md:5`).

## Finding 1 (BROKEN): a row with empty scope/teaches and a bare-sha anchor passes G3

Recipe (scratch, all committed bytes except the row and the empty entry):
1. `corpus/source-snapshots/round-46/S073.txt` copied from the freeze (sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`).
2. `corpus/README.md` holds one F28 line: `| F28 | GitHub private vulnerability reporting, reporter flow | admitted | \`corpus/knowledge/github-private-vulnerability-reporting.md\` | S073 | Decision rule for the reporter. |`
3. `corpus/knowledge/github-private-vulnerability-reporting.md` is 0 bytes (`wc -c` printed `0`).
4. `corpus/SOURCES.md` is a `## Registry` heading, the table header, and this one row:

   `| S073 | https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately | docs | A |  | 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 |  | mined | 2026-10-28 | 90d | corpus/knowledge/github-private-vulnerability-reporting.md |`

Command: `TMPDIR=$S python3 $S/freeze/corpus/instruments/r46-c2-gate.py --root $S/fx-min` (`$S` = scratch root). Printed:
```
gate G1 pass=0 read=rows=1 admitted=1 dup=0
gate G2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 table-rows=-2 xrefs=0/0
gate G3 pass=1 read=row-S073=ok
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate G6 pass=0 read=knowledge=1 base-names-intact=0 entry-bytes-ok=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=2/7 exit=1
```

Same row inside the full frozen corpus (`fx-C1`: frozen `corpus/` plus the F28 line appended to README, plus the row inserted after the S072 row, plus the empty entry). Command: `python3 $S/freeze/corpus/instruments/r46-c2-gate.py --root $S/fx-C1`. Printed:
```
gate G3 pass=1 read=row-S073=ok
c2-gate fixed=4/7 exit=1
```
and `bash scripts/sources-census.sh validate --file $S/fx-C1/corpus/SOURCES.md` printed `file	ok	…/corpus/SOURCES.md` (census exit 0, W04 warnings only). So census G7 also passes the empty scope/teaches row. Census rules (`scripts/sources-census.sh:24-28`) check kind, tier, status, opened, recheck and field count only, not scope, teaches or anchor locator.

Variants that also pass G3 (`=1`):
- Scope and teaches filled with `x`, otherwise identical (`C5`): `gate G3 pass=1 read=row-S073=ok`, G7 pass=1.
- Row placed under a `### Notes` heading inside the Registry section (`C4`): G3 pass=1, census ok, G7 pass=1.
- Row placed under `## Registry changes`, the changelog section (`C2`, full-tree): G3 pass=1, but census prints `file	E12	S073 row outside Registry section`, so G7 pass=0. G3 still passes it.
- Row placed under a `# Scratch` H1 inside the Registry section (`C3`): G3 pass=1, census E12, G7 pass=0.
- Kind and recheck cells empty, dash filler in scope and teaches (`V1`, `V1b`): G3 pass=1, census `E05 S073 kind=` and `E09 S073 recheck=`, G7 pass=0.
- Genuine full row with real scope, teaches and anchor text (`V2`, control): G3 pass=1. G3 cannot tell junk from genuine content.

Frozen-control confirmation: `.ufo/waves/round-46/controls/freeze-controls.txt`, block `c2 junk-row`, prints `gate G3 pass=1 read=row-S073=ok` and then `c2-gate fixed=4/7 exit=1`. The control's row (`controls/freeze-controls.py:113-114`) has scope `reporter flow`, teaches `teaches x`, and the anchor cell is `sha256 66c9…1930`. The frozen control therefore already passes G3 on a filler row. The control goes red only through G2, G5 and G6 (the entry), never through G3.

Kill-rule reading: C2's kill rule is about a control grading 7/7 or a fixed count below 7/7 at the final revision. Neither is triggered by this finding. What it does show is that the row-level junk control is not caught by its own named gate.

## Finding 2 (INFO): G3 does fail alone, and the controls that should be red are red

Discriminating controls (same fixture as Finding 1, one field changed each; G1, G4 and G7 stay at 1 in each, so G3 is the only changed gate):
```
A1 tier B                  gate G3 pass=0 read=bad=tier                 G1=1 G4=1 G7=1
A2 sha in scope cell        gate G3 pass=0 read=bad=anchor-sha           G1=1 G4=1 G7=1
A3 used-by empty            gate G3 pass=0 read=bad=used-by              G1=1 G4=1 G7=1
A4 used-by other path       gate G3 pass=0 read=bad=used-by              G1=1 G4=1 G7=1
A5 source without URL       gate G3 pass=0 read=bad=url                  G1=1 G4=1 G7=1
A6 status rejected          gate G3 pass=0 read=bad=status               G1=1 G4=1 G7=1
A7 anchor cell empty        gate G3 pass=0 read=bad=anchor-sha           G1=1 G4=1 G7=1
A8 snapshot tampered        gate G3 pass=0 read=snapshot-not-the-pinned-capture   (also G4=0)
A9 no README F28 row        gate G3 pass=0 read=bad=used-by              (also G1=0)
```
Opened `2026-10-27` gives `bad=opened`. A second S073 row gives `row-S073=absent-or-malformed`. A 10-cell row gives `row-S073=absent-or-malformed`.

Do-nothing control, frozen tree: `python3 $S/freeze/corpus/instruments/r46-c2-gate.py --root $S/freeze` printed `gate G3 pass=0 read=row-S073=absent-or-malformed` and `c2-gate fixed=2/7 exit=1`.

Placement controls (row inside a fence, inside an HTML comment, or under `## Leads (unopened)`): each printed `gate G3 pass=0 read=row-S073=absent-or-malformed`.

So G3 can fail alone (A1–A7). It catches a wrong tier, status or date, a wrong or missing used-by, a missing sha in the anchor cell, a moved sha, a source without the URL, and out-of-section placement in the fence, comment or Leads cases. It does not catch empty or filler scope, teaches or anchor locator, and it does not catch placement under the changelog or sub-heading sections (those are caught only by census E12 for H1 and changelog placement, and not at all for the H3 case).

## Constructions tally

Constructions with G3 pass=1 (genuine, distinct; the constructions are different placements or contents):
1. Registry table, scope/teaches empty, anchor = sha only (Finding 1, `C1`). G3 1, census 0.
2. Registry table, scope/teaches = `x` (`C5`). G3 1, census 0.
3. Registry table, kind and recheck empty, dash filler (`V1b`). G3 1, census 1 (E05/E09).
4. Row under `### Notes` inside Registry (`C4`). G3 1, census 0.
5. Row under `## Registry changes` (`C2`). G3 1, census 1 (E12).
6. Row under `# Scratch` inside Registry (`C3`). G3 1, census 1 (E12).
7. Genuine full row (`V2`), control for the content blindness.

Controls with G3 pass=0: no row, fence, HTML comment, Leads heading, two rows, 10 cells, tier B, sha in wrong cell, opened wrong, used-by empty, used-by other path, URL absent, status rejected, anchor empty, snapshot tampered, no F28 row.

## Recommendation (not applied; the counter is frozen)

Changing `r46-c2-gate.py` changes its frozen sha (`0ee958…`). That is a decision for the L1 and the operator, not this seat. Options, in order of strength:
- Pin the row bytes: fill `PINS["S073-row"]` after the L1 writes the row (the mechanism exists at lines 60 and 217-218). This is the only option that removes the filler gap completely; it trades away the docstring's "row bytes not pinned" design.
- Or extend G3: require non-empty kind, scope, teaches and recheck cells; require scope and teaches to be more than a single token; require the anchor cell to contain the sha and `S073.txt:<N>`; restrict `registry_lines` to the exact `## Registry` heading and reset on any heading of any level (`^#{1,6} `).
- Until then the only defence against the filler row is the non-author closure, which the counter does not run.

## Limitations

- Attacked the frozen predicate, not the L1's real S073 row, which has not been written yet. Any L1-written row with the same cells gets the same G3 result.
- Fixtures use an empty entry file; G3 does not read entry content, so this does not affect the G3 result. G2, G5 and G6 are red in every fixture, as at freeze.
- Census validation was run with the fleet-root `scripts/sources-census.sh` (read-only, constant from the counter).
- Did not test the C1 gate, the F28 entry, or the fixed count on a real build. The F28 entry and C1 re-grounds were not my item.
- Scratch dir `/fast/scratch/hyaku/kasegi-r46/R46RevC2G3/` removed on exit. Nothing committed; no git or jj mutation; no file in the repo or the fleet root touched except this report.
- No tools installed.
