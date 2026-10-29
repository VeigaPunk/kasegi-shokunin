# Round 46 (attempt 2) — `## Status, recheck and used-by changes (old → new)` DRAFT

DRAFT by seat `R46bScribeLesson` for the L1's append to `corpus/lessons/round-46.md`
(section `## Attempt 2 (2026-10-29, L1 KasegiR46)`).

---

## Status, recheck and used-by changes (old → new)

### Registry diff (additive only)

Command run by this seat (base export on the left, a scratch copy carrying the draft S074 row on the
right; the scratch copy is a copy of the base file with the single draft row inserted after the S073 row
at line 79, it is not the landed file):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ diff <(git show 04af9bc92229232ea5cce8b32bfe59dd969eb26d:corpus/SOURCES.md) \
       /fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/SOURCES.new.md
79a80
> | S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's ...
```

Counted over the same diff: **1 line added, 0 lines removed** (`grep -c '^>'` → 1, `grep -c '^<'` → 0).
The same run on `corpus/README.md` with the draft F29 row and its section header appended:

```
$ diff <(git show 04af9bc92229232ea5cce8b32bfe59dd969eb26d:corpus/README.md) \
       /fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/README.new.md
668a669,674
>
> ## Round-46 (attempt 2) admission — Frontier F29 (appended 2026-10-29)
>
> | id | topic | status | entry | sources | next |
> |---|---|---|---|---|---|
> | F29 | GitHub repository security advisories, maintainer flow: private discussion and fix of a vulnerability, the tem...
```

**Only additive hunks are expected.** Every hunk in the attempt-2 landing of `corpus/SOURCES.md` and
`corpus/README.md` must be an addition (`>`), never a rewrite of an existing line: no pre-existing row's
`status`, `recheck` or `used-by` cell changes in this round, and the frontier table is appended, not
edited in place (the attempt-1 precedent in `corpus/lessons/round-46.md` §Status).

### Per-cell statement

- **status:** no pre-existing row changes. The new row S074 is `mined` (the row is authored and applied
  in this one round step, so it has no old → new transition; a later correction lands as its own appended
  statement, per the round-41/43 precedent recorded in `corpus/SOURCES.md` §Registry changes).
- **recheck:** no pre-existing row's cadence changes. S074's recheck cell is `180d`, matching the
  tier-A GitHub Docs rows of the same round family (S073 `180d`); the entry carries exactly one
  `recheck:` line, of the exact form the C2 counter grades:
  `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`
  (that command run by this seat: `S074:sha256 OK`, nine `S074:Qn OK` lines, `RC=0` — see
  `gate-block.md`).
- **used-by:** no pre-existing row's `used-by` cell changes. S074's `used-by` cell names the new entry
  `corpus/knowledge/github-repository-security-advisories.md`; the new entry's own cross-references
  (`github-private-vulnerability-reporting.md`, `cna-assignment-and-vulnerability-rules.md`) are read-only
  reads of pinned files and change no cell.

### The row and the entry must land together (census coupling)

The census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <root>/corpus/SOURCES.md`)
resolves a row's `used-by` cell **relative to the tree that contains the registry file**. Run by this
seat on the scratch tree that carries the draft S074 row:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
   (exit 1)
```

and, with the entry file present in the same tree:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeLesson/tree/corpus/SOURCES.md
RC=0
```

So a row-only landing makes the census exit 1 (`E11`) and therefore the C2 counter's H7 limb red
(`gate H7 pass=0 read=census-rc=1 ok-line=0`, observed on the row-only tree); the entry and the row must
land in the same commit. The census's other readings are unchanged: the three `W04` warnings
(`S028`, `S029`, `S072`) are the same ones recorded in
`.ufo/waves/round-46/attempt2/controls/sources-census-before.txt`, and the lane line reads `kasegi ok`.

### Capture binding

At the current tip the S074 capture is committed before its registry row, and the binding check says so:

```
$ python3 corpus/instruments/capture-binding-check.py --root .
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=61 with_url=61 with_fetched_utc=23 with_archival=38 snapshot_dirs=23 manifest_dirs=23 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S074 dir=round-46-a2
records=61 bound=60 unbound=1
```

With the draft S074 row landed in the same tree (and its entry present), the same check reads:

```
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
records=61 bound=61 unbound=0
```

This is the attempt-1 precedent for S073 (`corpus/lessons/round-46.md` §Census: the freeze tree read
`records=60 bound=59 unbound=1` and it went green once the S073 row landed): the expected after-value for
attempt 2 is `records=61 bound=61 unbound=0`, and the `FAIL rule=no-row record=S074 dir=round-46-a2` line
must be gone.

### Counts the landing must reach

| measure | base `04af9bc9` | expected after attempt 2 |
|---|---|---|
| frontier rows in `corpus/README.md` (`grep -cE '^\| F[0-9]+ \|'`) | 28 | 29 (all admitted) |
| SOURCES registry rows | 73 | ≥ 74 (S074 mined) |
| knowledge entries (`find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l`) | 65 | 66 |
| absence sweep `grep -rliE 'repository securit. advisor\|GHSA' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l` | 2 — the files are `corpus/knowledge/github-private-vulnerability-reporting.md` (F28's scope-out note) and `corpus/SOURCES.md` (the S068 rejected-database row's search-log context) | 4 (the two base files plus `corpus/README.md` and the new entry `corpus/knowledge/github-repository-security-advisories.md`) |
| `r46-f29-gate.py --root <tree>` | `fixed=1/7 exit=1` at the base export; `fixed=2/7 exit=1` at the freeze tree | `fixed=7/7 exit=0` |

<!-- END OF (c) DRAFT -->
