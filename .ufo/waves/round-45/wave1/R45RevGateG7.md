VERDICT: BROKEN

Seat: R45RevGateG7 (read-only reviewer; C2 gate attack on G7). No edits to any repo; all fixtures in scratch (removed on exit).

## Attacked

- `corpus/instruments/r45-c2-gate.py:197-199` (`def g7`):
  ```
  def g7(root: str) -> tuple[bool, str]:
      rc, out = run(["bash", CENSUS, "validate", "--file", os.path.join(root, "corpus/SOURCES.md")], root)
      return rc == 0, f"census-rc={rc}"
  ```
  Frozen predicate (docstring line 27): "`sources-census.sh validate --file <root>/corpus/SOURCES.md` exits 0."
  `CENSUS` (line 46) defaults to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, a fleet-shared script outside the lane and outside the frozen base; overridable by env `SOURCES_CENSUS`.
- Census validate exit logic, `scripts/sources-census.sh:737-746, 803-806`: only `E[0-9]+` findings set `findings=1`; `W[0-9]+` lines are printed but never fail. Row checks cover shape/enums/dates/duplicate-URL/used-by-existence only (`:634-674`, `:538-571`). Nothing checks the anchor sha256, the source URL against the canonical form, the snapshot, the used-by entry content, or the tier/status against capture evidence.
- Claims: `.ufo/waves/round-45/claims.json` C2 `expect_before` = `c2-gate fixed=1/7 exit=1`.

Counter copy used: `corpus/instruments/r45-c2-gate.py` from the lane working tree, copied to scratch; sha256 prefix `5e0796168cfe09f1` on both (not in the frozen base rev dc5bb8c6, which lacks the counter).

## Finding 1 (the cheapest construction): zero edits. G7 passes on the frozen base

Command (scratch copy of `/fast/scratch/hyaku/kasegi-r45/L1/pure`, byte-identical `corpus/SOURCES.md` to `git show dc5bb8c6…:corpus/SOURCES.md`):
```
TMPDIR=<scratch>/tmp python3 <scratch>/gate.py --root <scratch>/base
```
Printed:
```
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=F27-rows=0
gate G6 pass=0 read=knowledge=63
gate G7 pass=1 read=census-rc=0
c2-gate fixed=1/7 exit=1
```
The real defect is present (no F27 row, no S071, 26 rows, 63 entries). G7 is green regardless. This matches `expect_before` and means the single "fixed" limb on the do-nothing control is G7.

Direct census on base:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	…/base/corpus/SOURCES.md
census-rc=0
```

## Finding 2: "registry that parses clean but lies" constructions, each G7 pass=1

All fixtures add one `S071` row (11 cells, NF=13) inside `## Registry`. Results from the gate run on each tree.

| # | Construction (what the registry lies about) | G7 line | Census output | Other limbs that catch the lie |
|---|---|---|---|---|
| T2 | mined tier-A row, anchor `sha256 000…0`, used-by `—` | `gate G7 pass=1 read=census-rc=0` | `W03 S071 mined but unused`, `ok` | G3 fail |
| T3 | source URL `https://example.org/security` (non-canonical), used-by existing `corpus/README.md` | `gate G7 pass=1 read=census-rc=0` | `ok` | G3 fail |
| T4 | S071 reuses S001's URL and scope; teaches begins `supersedes S001:` (E04 exempted by `teaches !~ /supersedes S[0-9]{3}/`, line 648) | `gate G7 pass=1 read=census-rc=0` (requires the used-by target to exist, else E11 → RED) | `ok` | G3/G5 fail |
| T5 | tier-A row with status `queued`, used-by `—` | `gate G7 pass=1 read=census-rc=0` | `ok` | G3 fail |
| T6 | row indented 4 spaces (census ignores as code) | `gate G7 pass=1 read=census-rc=0` | `ok` (row silently dropped) | G3 `row-S071=absent-or-malformed` |
| T7 | full lane snapshot dir copied in (S071.txt, S072.txt, manifest.json), anchor sha zeros, used-by existing placeholder entry | `gate G7 pass=1 read=census-rc=0` | `ok` | G3 `bad=used-by,anchor-sha` |
| E1 | `SOURCES_CENSUS` env → stub `exit 0` script (no registry read) | `gate G7 pass=1 read=census-rc=0` | n/a | none |

T7 is the strongest: the registry lies about the anchor digest and G7 still prints pass=1, the same as on the empty base. G7 cannot distinguish T7 (lying S071) from the do-nothing base. Full T7 gate:
```
gate G3 pass=0 read=bad=used-by,anchor-sha
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G7 pass=1 read=census-rc=0
c2-gate fixed=3/7 exit=1
```
(G4 and G6 pass there only because of the lane snapshot and my placeholder knowledge file; they are not evidence about the lane's real content.)

Also silently accepted by validate: recheck `every 90 days` (E09 regex accepts digits after a letter). `overdue` then classifies it as a non-judged cadence while `90d` is flagged:
```
fr-F1-recheck-every-90-days overdue@2027-12-01: (1, ['file\tcadence\tS071 recheck=every 90 days opened=2026-10-28']) | validate: 0
fr-F11-recheck-90d-control overdue@2027-12-01: (1, ['file\tcadence\tS071 recheck=90d opened=2026-10-28', 'file\toverdue\tS071 309d recheck=90d opened=2026-10-28']) | validate: 0
```

## Finding 3: can G7 false-RED on a correct landing? Yes

Baseline correct-looking row (tier A, kind docs, opened 2026-10-28, recheck on-release, used-by an existing entry path): census rc=0, G7 pass=1. Variants of that row, each printed by census:

- CRLF line endings on the whole file (valid content): `file	E12	S001 row outside Registry section` for every row, because `## Registry\r` is not recognised (`trim` strips only space/tab, `:580-582`). Gate: `gate G7 pass=0 read=census-rc=1`.
- GFM-escaped pipe `\|` inside a cell (valid GFM): `file	E01	S071 fields=12`.
- used-by written as a code span `` `corpus/knowledge/….md` ``: `file	E11	S071 missing used-by ` + "`corpus/knowledge/…md`".
- recheck `90 d`: `file	E09	S071 recheck=90 d`.
- recheck `on-release (quarterly)`: `file	E09	S071 recheck=on-release (quarterly)`.
- opened with a time `2026-10-28T20:52Z`: `file	E08	S071 opened=2026-10-28T20:52Z`.
- kind `advisory` (outside closed enum; contract-consistent rejection): `file	E05	S071 kind=advisory`.

Strict-by-contract rejections (kind enum, ISO date, `NNd`) are defensible; the CRLF and escaped-pipe cases are not contract-inconsistent and are genuine false REDs.

## Discriminating control

Do-nothing base (Finding 1) grades G7 = pass=1; lying trees T2–T7 grade G7 = pass=1. G7 has zero discriminating power for the F27 defect.

## Verdict rationale

G7 as written is an always-pass on the frozen base and passes every construction above. Its failure modes are asymmetric: it accepts any W-only registry (including lying rows) and it reds on valid GFM/CRLF content. The C2 `before` count therefore starts at 1/7 with no work done.

## Limitations

- Did not run the census `selftest` or the lane's real final revision (not available in my scope). Used the lane working-tree counter copy (sha prefix matched).
- Fixtures use placeholder knowledge entries; no real F27 entry was built.
- G7 depends on the fleet-shared `scripts/sources-census.sh` (read only, not modified, not run in selftest). A change to that script changes G7 without any lane change.
- E08 compares `opened` with the system UTC date; not tested with a clock change.
- All results are from runs I performed in scratch; scratch removed on exit.

## Suggested disposition (for L1; no edit made)

- Either make G7 assert that the S071 row itself is clean (exit 0 and no W-line for S071) or drop G7 from the 7-limb count, because it carries no F27 evidence. Changing the predicate after scoring must be logged as a counter erratum per claims.json C2 kill rule, so L1 decides.
- Fix census CRLF and escaped-pipe handling only in the fleet script owner's lane.
