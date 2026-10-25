# Frontier admission form — F06–F08 against the F01–F05 convention

Seat: FrontierAdmitForm-2 (critic). Read-only. No production file, lane tree, index
or sibling lane was modified; the only writes are this report and scratch files under
`/tmp/kasegi-r23-falsify-FrontierAdmitForm-*`.

Target: `corpus/README.md` § Frontier (lines 191–204) and the three entries those rows
link. Landing commit `953c278` (round-23 work commit), parent `922a4dd…` per
`.ufo/waves/round-23/claims.json` `base`.

Verdict summary, per asked cell:

| Row | evidence cell (entry) | sources cell | next cell | F01–F05 consistent? |
|---|---|---|---|---|
| F06 (`README.md:200`) | exists, header `source: S018` | `S018` | constraint | entry/sources yes; coverage-map row **missing** |
| F07 (`README.md:201`) | exists, header `source: S030` | `S030 (supersedes S022)` | constraint | annotation has no F01–F05 precedent and contradicts registry status |
| F08 (`README.md:202`) | exists, header `source: S029` | `S029 (supersedes S024)` | constraint + dated fact | same annotation defect |
| closing (`README.md:204`) | — | — | — | sentence does not describe frontier state |

Raw rows, verbatim:

```
$ nl -ba corpus/README.md | sed -n '200,204p'
200  | F06 | Multi-party CVD — FIRST guidelines v1.1 | admitted | knowledge/multiparty-vulnerability-coordination.md | S018 | Record each party's role and relationship; an upstream fix is not downstream evidence. |
201  | F07 | CVE CNA operational rules | admitted | knowledge/cna-assignment-and-vulnerability-rules.md | S030 (supersedes S022) | Separate technical impact, assignment scope and identifier count; do not reuse 4.1.0 section numbers. |
202  | F08 | EU Cyber Resilience Act reporting duties | admitted | knowledge/cra-manufacturer-reporting-duties.md | S029 (supersedes S024) | Distinguish manufacturer statutory tracks from researcher disclosure; Article 14 applies from 2026-09-11. |
203
204  The original domain-root map is exhausted: 0/18 surfaces are present.
```

Evidence-cell check (all three paths resolve and their header source id equals the
`sources` cell):

```
$ sed -n '2p' corpus/knowledge/multiparty-vulnerability-coordination.md
source: S018 — https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1 — version 1.1, Spring 2020; …
$ sed -n '2p' corpus/knowledge/cna-assignment-and-vulnerability-rules.md
source: S030 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf — CNA Operational Rules 4.2.0, approved 2026-08-20, effective 2026-08-25; …
$ sed -n '2p' corpus/knowledge/cra-manufacturer-reporting-duties.md
source: S029 — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng — Regulation (EU) 2024/2847, OJ 20.11.2024; Articles 14, 15, 16 and 71
```

Each entry also carries `verified-at:` and an executable `recheck:` command
(`source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source
S018|S029|S030`), satisfying the Q1 header form; the manifest lists all three ids
(`python3 -c "import json;print([s['id'] for s in json.load(open('corpus/source-snapshots/round-23/manifest.json'))['sources']])"`
→ `['S018', 'S029', 'S030']`, exactly those three). I did not execute the recheck (no
freshness claim made).

## Finding F1 — fixable defect (coverage): the three admissions have no Coverage map row, unlike 5/5 earlier frontier admissions and 30/30 prior entries

Evidence — the convention is uniform before r23 and breaks exactly at the three new
entries:

```
$ start=$(grep -n '^## Coverage map' corpus/README.md | cut -d: -f1); end=$(grep -n '^## Known gaps' corpus/README.md | cut -d: -f1)
$ for f in corpus/knowledge/*.md; do b=$(basename "$f"); sed -n "${start},${end}p" corpus/README.md | grep -q "$b" || echo "NO COVERAGE-MAP ROW: $b"; done
NO COVERAGE-MAP ROW: cna-assignment-and-vulnerability-rules.md
NO COVERAGE-MAP ROW: cra-manufacturer-reporting-duties.md
NO COVERAGE-MAP ROW: multiparty-vulnerability-coordination.md
```

`covered=30 of 33` knowledge files appear in the Coverage map section; the three missing
are precisely F06–F08. F01–F05 each have one, `README.md:37–41`:

```
37 | CVSS v4.0 severity and vector semantics | knowledge/cvss-v4-severity-and-vector.md | S001, S002 — public primary, opened 2026-10-19 |
38 | Coordinated-disclosure timelines | ... | S003, S004, S005 — public primary, opened 2026-10-19 |
39 | Authorization, safe harbor, and scope | ... | S006, S007, S008 — public primary, opened 2026-10-19 |
40 | AI-assisted finding validation | ... | S009, S010, S011, S012 — public primary, opened 2026-10-19 |
41 | CWE Top 25 2025 methodology | ... | S013, S014, S015 — public primary, opened 2026-10-19 |
```

The lane's own metric records this convention as admission evidence for r22 —
`SCORECARD.md:328`: "Coverage-map rows **25 → 33**" — and `SCORECARD.md:344` defines the
counter. The same command is flat across the r23 admission:

```
$ awk '/^## Coverage map/{f=1;next}/^## /{f=0} f&&/^\| /{n++} END{print n-2}' corpus/README.md   # now
33
$ git show c8b719d:corpus/README.md | awk '/^## Coverage map/{f=1;next}/^## /{f=0} f&&/^\| /{n++} END{print n-2}'
33
```

Also: the three paths occur only in the Frontier rows —
`grep -nE 'knowledge/(multiparty-vulnerability-coordination|cna-assignment-and-vulnerability-rules|cra-manufacturer-reporting-duties)\.md' corpus/README.md`
→ lines 200, 201, 202 only (count 3). The r22 admission added eight Coverage-map rows —
the five frontier entries plus `citation-bases`, the QUALITY/SOURCES row and the r22
lessons row (`git diff c8b719d^ c8b719d -- corpus/README.md | grep '^+| '`, first eight
added rows, taking the count 25→33 per `SCORECARD.md:328`); the r23 admission added 0
for 3 new entries.

Counterexample tested: "a Coverage map row is not an admission requirement, so this is a
design choice." Rejected on three local facts: (a) 30/30 prior entries have one; (b) the
r22 round record (`SCORECARD.md:328`, the C2 receipt) reports the map-row delta as
coverage evidence; (c) the README's own section is titled a coverage map and its rows are
keyed by entry path. The omission is a form break, not a deliberate scope.
Not scored as a C2 falsifier: the frozen C2 count greps `^\| F0[6-8] .*\| admitted \|`
only, so 3/3 and 8/8 remain literally true. This is index-completeness debt, not a false
admission count.

Smallest safe correction: **append-only**. Inserting the three rows at line 42 would
renumber `corpus/README.md` lines 42–204, and README is cited by line from
`corpus/lessons/round-6-aggregator-audit.md:28` (`corpus/README.md:82`) and `:64`
(`corpus/README.md:49`) — the same shift class as R6/M17. Append a new section after
line 204 (README ends at 204):

```
## Coverage map — round-23 addendum

| Area | Entry | Source basis |
|---|---|---|
| Multi-party CVD — FIRST guidelines v1.1 | knowledge/multiparty-vulnerability-coordination.md | S018 — public primary, opened 2026-10-19 |
| CVE CNA operational rules | knowledge/cna-assignment-and-vulnerability-rules.md | S030 — public primary, opened 2026-10-20 |
| EU Cyber Resilience Act reporting duties | knowledge/cra-manufacturer-reporting-duties.md | S029 — public primary, opened 2026-10-20 |
```

Opened dates taken from `corpus/SOURCES.md` S018/S029/S030 `opened` cells. If the C2
counter must include them, it needs a second term; changing the r22 counter in place
would rewrite a filed receipt, which R9 forbids.

## Finding F2 — fixable defect (form + registry state): `(supersedes S022/S024)` has no F01–F05 precedent and asserts a state the registry does not hold

F01–F05 sources cells are bare comma lists (`S001, S002`, …, `S013, S014, S015`); no
annotation anywhere in `README.md:195–199`. F07/F08 introduce a parenthetical.

The asserted state is not recorded where the sources cell tells the reader to resolve it:

```
$ grep -E '^\| S02[24] ' corpus/SOURCES.md | awk -F'|' '{gsub(/ /,"",$2); gsub(/^ | $/,"",$9); gsub(/^ | $/,"",$12); print $2" status=["$9"] used-by=["$12"]"}'
S022 status=[queued] used-by=[—]
S024 status=[queued] used-by=[—]
```

Both superseded rows still read `queued` with `used-by=—`, and their `teaches` columns
still address the reader in the future tense — S022 "Define who has assignment
authority…" (`SOURCES.md:28`), S024 "mine Article 14's reporting clock only after reading
it in the official text" (`SOURCES.md:30`). A reader resolving `S030 (supersedes S022)`
therefore finds a row still queued for the work the supersede claims is done; a future
sweep would satisfy S022/S024 a second time.

Placement detail: the supersede marker that R8 names lives at the head of the *teaches*
cell, not at the row start — `grep '^| S030 ' corpus/SOURCES.md | cut -d'|' -f8` →
`supersedes S022 — use current 4.2.0 requirements and section numbering; …` (same form
for S029 → S024). Under R8's literal wording ("a new row beginning 'supersedes S### —'")
the landed marker does not sit at the row beginning; that registry question belongs to
the registry seat and is flagged here, not claimed.

Smallest safe correction, two options (choose one, not both):
1. Drop the parentheticals at `README.md:201–202`; the registry's `teaches` cell already
   carries "supersedes S0xx —", so the README copy is a second authority for the same
   fact. Cheapest and does not touch filed registry bytes.
2. Keep the parentheticals and set S022/S024 to a non-pending status with a logged
   old→new change per R8. This is registry work, not mine.

## Finding F3 — pass: `next` states review constraints, not pending actions (one accepted deviation)

All eight admitted `next` cells are constraints; the r22 pending-action forms ("Open the
public guideline and record its coordination roles." at `c8b719d:corpus/README.md:200`)
are gone:

```
$ grep -E '^\| F0[1-8] \|' corpus/README.md | cut -d'|' -f7 | grep -nE 'Open |Read |Fetch |Locate |Mine |then ' || echo none
none
```

Two deviations that are tradeoffs, not defects:
- F08 (`README.md:202`) appends a dated scope fact, "Article 14 applies from
  2026-09-11". It is not a pending action; it matches S029's `teaches` ("Article 71
  applies Article 14 from 11 September 2026") and the entry body
  (`corpus/knowledge/cra-manufacturer-reporting-duties.md:15`). Accepted; no fix. It is
  the only `next` cell carrying a date, so a reviewer comparing rows will notice it, but
  the statement is sourced and stable.
- F06 (`README.md:200`) cites a single source where F01–F05 cite 2–5. Q2 requires ≥1
  tier-A/B row per claim scope, so this is permitted; S018 is the sole authority for the
  FIRST surface and is `mined`/`used-by` set in `SOURCES.md`. No fix; do not inflate.

## Finding F4 — the closing sentence is true about a different denominator, but after three admissions it no longer describes the frontier

`README.md:204` is byte-identical to the r22 line (it was not edited by `953c278`):

```
$ git show c8b719d:corpus/README.md | tail -1 > /tmp/…-r22.txt; sed -n '204p' corpus/README.md > /tmp/…-now.txt; cmp /tmp/…-r22.txt /tmp/…-now.txt && echo IDENTICAL
IDENTICAL
```

Its referent is the lost-tree denominator, defined in
`corpus/knowledge/source-tree-loss-2026-09-28.md:64–79` (`claims/`, `evidence/`,
`ledger/`, `bounty-map/`, `docs/`, `ops/`, … "18 items — **0 of 18 present**"), restated
at `README.md:47–49`. So the sentence is not false after three admissions. It is also
not a frontier statement: § Frontier's denominator is eight public-practice surfaces,
all eight now admitted (`README.md:195–202`), and the round record separates the two —
`corpus/lessons/round-23.md:176`: "Score held at **7**: the r15 domain-root denominator
is untouched by public-practice entries."

Falsification test: change any frontier row's status and re-run — the sentence cannot
change, because it contains no frontier term. It is therefore non-descriptive of the
state asked about, and as the only prose after eight "admitted" rows it invites the
reader to read "0/18" as frontier coverage — an understatement in one direction and a
denominator conflation in the other.

Smallest safe correction: append one sentence after line 204 (nothing follows it, so no
line is renumbered), e.g. "Frontier coverage uses a separate denominator: 8/8
public-practice surfaces admitted (F01–F08); the r15 lost-root denominator remains 0/18."
Leave line 204 intact; R6.

## Finding F5 — adjacent staleness caused by the same three admissions (lower severity, likely another seat's file)

`README.md:5` still scopes provenance as "this holds for the 25 legacy entries only; the
five round-22 entries (Frontier F01–F05) were read from public sources S001–S015 on
2026-10-19". After the three admissions the preamble classifies 30 of 33 entries; F06–F08
fall outside both clauses (not legacy, not the five). Same-line suffix keeps the line
number (R6): extend with "and the three round-23 entries (F06–F08) were read from
S018/S029/S030 on 2026-10-20." Also `README.md:43` describes QUALITY/SOURCES as the
"Round-22 admission and source-registry contract" while `corpus/QUALITY.md` now carries
the round-23 criteria Q7/R7–R9. Reported, not claimed; I did not establish whether the
preamble or the QUALITY row is owned by another falsify seat.

## Impacted axes

- coverage (C2): F1 is index-completeness debt inside the axis' own artifact; it does not
  falsify the frozen counts (3/3, 8/8). F2 affects provenance resolution of two of the
  three admitted rows.
- depth:verifiability (C1): no impact found — I did not read or exercise `resolve.py`,
  the fixture matrix, or the recheck manifest, so I make no claim about them.

## Scope limits

- Captured bytes only: I did not open FIRST, cve.org or EUR-Lex; freshness of S018/S029/
  S030 is unverified here (the manifest's own purpose line says it verifies captured
  bytes, not upstream freshness).
- Quote/excerpt correctness for the three entries belongs to the S018/S029/S030 quote
  seats; registry status vocabulary intent belongs to the registry seat.
- No mutation testing was required for a documentation form question; no scratch copy of
  README was mutated. All git reads were `git show`/`git log`/`git diff` (no index write).
- Tooling: nothing installed or upgraded during this seat.

## Reproduction log (exact commands, all read-only)

```
grep -nE '^\| F0[1-8] \|' corpus/README.md | awk -F'|' '{print $2, $6, $7}'          # cells
for f in corpus/knowledge/*.md; do … sed -n "${start},${end}p" corpus/README.md …   # F1
awk '/^## Coverage map/{f=1;next}/^## /{f=0} f&&/^\| /{n++} END{print n-2}' corpus/README.md
git show c8b719d:corpus/README.md | awk '…same…'
grep -E '^\| S02[24] ' corpus/SOURCES.md | awk -F'|' '{print $2,$9,$12}'            # F2
git show c8b719d:corpus/README.md | tail -1 | cmp - <(sed -n '204p' corpus/README.md) # F4
sed -n '64,79p' corpus/knowledge/source-tree-loss-2026-09-28.md                     # F4 referent
```
