# ExecC2Census — round 38 (C2 census mechanics)

Item: run the fleet census at base; mirror `corpus/SOURCES.md` into scratch, append a candidate
`S055` row at the end of the registry table, validate the mirror (exit 0, no new W/E), and
establish what the census requires of `used-by` paths (must they exist?). Receipt only.

Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat).
Lane head observed at work time: `700153593eb586c70a6499c8ca225ee4d673bc9b`
(`round-38: wave1 spec + validated dispatch (73 seats, v2)`); claims base `a173b0c2…`.
Registry under test: `corpus/SOURCES.md` (118 lines, sha256
`ead94cc69c09afc2da890c7124f09852b4da26880de193e782dfba03eaf6e671`, 54 registry rows).
Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecC2Census` (removed before yield).
No lane/fleet/shokuknow file was written; no network fetch; no tool install; no mutating git.

## 1. Base census (real registry, real lane dir)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Byte-identical to `.ufo/waves/round-38/census-before.txt` (same two W04 rows, same `ok` line,
same `exit=0`); expected shape confirmed — no E codes.

## 2. Mirror setup

```
$ mkdir -p $S/mirror/corpus && cp -a <lane>/corpus/. $S/mirror/corpus/
$ sha256sum <lane>/corpus/SOURCES.md $S/mirror/corpus/SOURCES.md
ead94cc6…f6e671  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
ead94cc6…f6e671  /fast/scratch/hyaku/kasegi-r38/ExecC2Census/mirror/corpus/SOURCES.md
files=270      # same file count as the lane corpus tree
```

Mirror baseline with the unmodified registry (entry file not yet involved):

```
$ bash …/sources-census.sh validate --file $S/mirror/corpus/SOURCES.base.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r38/ExecC2Census/mirror/corpus/SOURCES.base.md
exit=0
```

The `--file` path is a full tree mirror, not a lone registry: `E11` resolves every mined row's
`used-by` against the mirror root, so the mirror must carry `corpus/knowledge/*`,
`corpus/source-snapshots/*` etc. (270 files). Measured: holding the registry outside that tree
(so the resolved root has no `corpus/`) yields `47` `E11` lines over `23` distinct `used-by`
paths (rows naming several paths emit one line each) and `exit=1`.

## 3. Candidate S055 row appended at the end of the registry table

Placement: inserted immediately after `S054` (base line 60), i.e. as new line 61, before the blank
line and `## Paths` (base line 62). This is the last row of the `## Registry` table, not a new
section.

```
$ awk 'NR==60{print; print row; next} {print}' SOURCES.md > SOURCES.with-row.md
59: | S053 | FIRST EPSS documentation page — https://www.first.org/epss/ | docs | A | …
60: | S054 | SSVC: Stakeholder-Specific Vulnerability Categorization — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ | docs | A | …
61: | S055 | OASIS CSAF v2.0 (Common Security Advisory Framework) — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html | spec | A | …
62: 
63: ## Paths
S055 NF=13
base rows=54   with-row rows=55
```

Field map (NF=13 ↔ 11 columns): `S055` · source+URL · `spec` · `A` · scope · anchor · teaches ·
`mined` · `2026-10-26` · `180d` · `corpus/knowledge/csaf-vex-product-status-and-justifications.md`.
No duplicate id, no duplicate URL+scope (no `E03`/`E04` fired), `opened` not future (`E08` clean).

## 4. Validate without the entry file (E11 fires)

```
$ ls $S/mirror/corpus/knowledge/csaf-vex-product-status-and-justifications.md
ls: cannot access '…/csaf-vex-product-status-and-justifications.md': No such file or directory
$ bash …/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S055 missing used-by corpus/knowledge/csaf-vex-product-status-and-justifications.md
exit=1
```

## 5. Validate with the entry file present (clean)

Entry stubbed in scratch only (48 bytes) to test resolution; content is the C2 seat's deliverable,
not this seat's:

```
$ bash …/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/hyaku/kasegi-r38/ExecC2Census/mirror/corpus/SOURCES.md
exit=0
```

Only the two pre-existing `W04` rows (S028, S029); **no new W or E code**; `S055` is not a
duplicate URL. Row count in the validated registry: 55.

## 6. Negative control — row outside `## Registry`

Row inserted after `## Paths` (line 67 of the mirror) instead of at the table end:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E12	S055 row outside Registry section
exit=1
```

So the "place the row where the registry table ends" instruction is enforced, not stylistic.

## 7. What the census requires of `used-by`

Resolver (`usedby_findings`, `sources-census.sh:538-574`): for every row inside `## Registry` whose
status is `mined`, split cell 11 on `,`, trim each path, skip empty/`—`, and require
`[ -e "$dir/$path" ]` where `dir` is the **registry root** (for `--file <X>/corpus/SOURCES.md`,
`dir` = `<X>`); a miss emits `E11 <id> missing used-by <path>`. Observed matrix:

| probe | registry `used-by` | disk state | result |
|---|---|---|---|
| A | `corpus/knowledge/x.md` | file at `<root>/corpus/knowledge/x.md` | `ok`, exit 0 |
| B | `corpus/knowledge/x.md` | file moved to `<root>/knowledge/x.md` | `E11` exit 1 |
| C2 | `corpus/knowledge/x.md, corpus/knowledge/missing.md` | first present, second absent | `E11 … missing.md` only, exit 1 |
| D | `corpus/knowledge/x.md` | registry file itself moved one dir up (root = grandparent) | `E11` exit 1 |
| E | `—` (mined) | n/a | `W03 S055 mined but unused`, exit 0 |
| F | `corpus/knowledge/adir` | directory exists | `ok`, exit 0 |
| 6b/6c | path named, status `queued` | entry file absent | `ok`, exit 0 (no `E11`) |

Answers: **yes — a named `used-by` path must exist on disk**, checked with `-e` (a directory
passes, a file passes, a symlink to an existing target passes). The path is repo-relative (it
contains the `corpus/` prefix) and is resolved against the registry root, i.e. the parent of the
directory holding the registry, not against `corpus/`. Multiple comma-separated paths are each
checked and each miss reported separately. `E11` applies **only to `mined`** rows: `queued` and
`rejected` rows are not checked (6b, 6c). `—` is the "nothing consumed this yet" escape for a
mined row and downgrades the requirement to warning `W03` (exit stays 0), so a mined row with a
dangling path fails the gate while a mined row with no path at all only warns.

## 8. Landing consequence

- Land the S055 row and `corpus/knowledge/csaf-vex-product-status-and-justifications.md` **in the
  same commit**: the row alone makes `validate` exit 1 with `E11 S055`.
- Post-landing re-run of the real command (`--root /home/vgpnk/Projects/shokunin kasegi`) should
  still print exactly `W04 S028`, `W04 S029`, `ok`, `exit=0`; any `E11 S055` means the entry file
  is missing or renamed, any `E12` means the row drifted out of `## Registry`.

## DELIVERABLE

```markdown
| S055 | OASIS CSAF v2.0 (Common Security Advisory Framework) — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html | spec | A | The VEX profile's product_status categories a vendor publishes per product (first_affected, known_affected, fixed, known_not_affected, under_investigation, last_affected, recommended) and the machine-readable flags for not-affected products | the product_status definition and the not-affected flags table at the OASIS Standard; capture corpus/source-snapshots/round-38/S055.txt | CSAF VEX product_status is a per-product advisory state with justification flags for not-affected products — distinct from CVSS severity, KEV status, EPSS likelihood and SSVC stakeholder decisions | mined | 2026-10-26 | 180d | corpus/knowledge/csaf-vex-product-status-and-justifications.md |
```

Deliverable: 1 line, 818 bytes with its newline (817 bytes without), NF=13,
sha256 `caa476c1d44aaf49f05bf9b039018ecd9612e684ed42fc4ba2c5ae09edcee82c`.
Insertion point: after the `S054` row (registry-table end), before the blank line that precedes
`## Paths` — one added line, no other registry edit.

## Risks

- The candidate row's `anchor`/`teaches` prose is this seat's wording shaped from the C2 claim;
  if the C2 entry lands different emphasis the L1 may reword the two middle cells. Shape
  (NF=13, enums, dates, path) is validated as above and must not change.
- `used-by` is existence-checked with `-e` only; content, citation or the entry's own
  `source: S055` binding are not census concerns and were not validated here.
- The scratch stub written for probe 5 is not the entry; the real entry must be non-empty and
  pass the QUALITY gate owned by the C2 seat.
