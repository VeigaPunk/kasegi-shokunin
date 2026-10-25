# C2RowSchema — round 25 wave 2: census re-run on the scratch mirror + five-row schema audit

Seat: `L1Kasegi25.C2RowSchema`. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Attacked item: wave-1 `RowsScratch.md` claims (a–d) — the `--file` census on
`.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md`, the pipe audit of
`SOURCES.append.block.md`, and the schema/normalization of the five new rows S036–S040.
Read-only: no production file edited; no tool installs needed (bash, gawk, coreutils, diff, git all present).

## Verdict

**CONFIRMED — the wave-1 result stands.** The mirror validates exit 0 with only the two
pre-existing W04s, both discrimination mutants are still killed (E03/E04, exit 1), all five
rows are NF=13 with a conforming `180d` NNd cadence (no prose, no ISO-date), no cell carries
a literal or escaped pipe, and every `used-by` path resolves. No correction required.

One scope observation beyond the receipt: the mirror is now **byte-identical to the live
`corpus/SOURCES.md`** — the append landed after wave 1 (file shows ` M` in git status), so
the mirror result now also describes the production file.

## Commands, outputs, exits (all run from lane root)

### 1. Validate on the scratch mirror — wave-1 said exit 0, W04 ×2 only

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md
exit=0
```
Matches `wave1/RowsScratch.md:99-103` and `wave1/LogDraft.md:42` exactly.

### 2. Census mode on the mirror — wave-1 said rows 40 / tier.A 37 / mined 28

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file .ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md
file	rows	40
file	tier.A	37
file	tier.B	1
file	tier.C	2
file	status.mined	28
file	status.queued	9
file	status.rejected	3
FLEET	missing	0   (+ FLEET aggregates, all consistent)
exit=0
```
Matches `RowsScratch.md:109-110` (35+5 rows, 32+5 tier A, 23+5 mined).

### 3. Discrimination mutants still kill — exit was not vacuous

```
$ …/sources-census.sh validate --file …/validate/corpus/SOURCES.mutant-dup-id.md
file	E03	S038 duplicate id     exit=1
$ …/sources-census.sh validate --file …/validate/corpus/SOURCES.mutant-dup-url.md
file	E04	S037 duplicate url cybozu.co.jp/company/security-policy within scope …   exit=1
```
Matches `RowsScratch.md:115-121`.

### 4. Mirror ↔ live file ↔ block identity

```
$ diff .ufo/…/validate/corpus/SOURCES.md corpus/SOURCES.md        → IDENTICAL (exit 0)
$ diff <(grep '^| S0' SOURCES.append.block.md) \
       <(grep -E '^\| S0(3[6-9]|40) ' …/validate/corpus/SOURCES.md) → IDENTICAL (exit 0)
$ wc -l corpus/SOURCES.md …/validate/corpus/SOURCES.md            → 69 / 69
$ git status --porcelain corpus/SOURCES.md                        → " M corpus/SOURCES.md"
```
The five mirror rows are byte-identical to the block rows and to the rows now sitting in the
live file. Wave-1 said the rows were "not appended this round" (`SOURCES.append.block.md:3`);
they have since been appended in the worktree — the mirror prediction held byte-for-byte.

### 5. Five-row schema inspection (lines 42–46 of the mirror)

```
$ awk -F'|' '/^\| S0(3[6-9]|40) /{print NR": NF="NF" id="$2" recheck="$(NF-2)" status="$(NF-4)" opened="$(NF-3)}' …/SOURCES.md
42: NF=13 id= S036  recheck= 180d  status= mined  opened= 2026-10-25
43: NF=13 id= S037  recheck= 180d  status= mined  opened= 2026-10-25
44: NF=13 id= S038  recheck= 180d  status= mined  opened= 2026-10-25
45: NF=13 id= S039  recheck= 180d  status= mined  opened= 2026-10-25
46: NF=13 id= S040  recheck= 180d  status= mined  opened= 2026-10-25
```
- **Prose cadence:** none. `180d` satisfies `recheck ~ /^[0-9]+d$/` at
  `scripts/sources-census.sh:665` — E09 cannot fire. A whole-file scan for non-conforming
  recheck cells (not ISO date / `NNd` / symbolic) over all 40 rows returns zero suspects.
  `overdue --today 2026-10-25` prints `cadence` lines for all five (`S036…S040 recheck=180d`),
  no `overdue` lines, exit 0. (Note: `:676-677` emits `cadence` for `NNd` *and* symbolic
  values — the header comment at `:36` underspecifies this; doc-only, no defect.)
- **Escaped pipes:** `grep -cF '\|'` over the five rows → 0; over `SOURCES.append.block.md`
  → 0 (8 lines total: 3 comments + 5 rows). Disguised-pipe scan (`&#124;`, `&vert;`,
  `&#x7C;`, full-width `｜`) → 0. Each row carries exactly 12 pipe chars (5 lines × 12 = 60,
  reproducing `RowsScratch.md:77-85`). NF=13 on every row means no cell contains an unescaped
  `|` — one would push NF to 14 and trip E01, which validate did not report.
- **Whole-file shape:** `awk 'NF>1 && NF!=13'` over the mirror → no output (header, separator
  and all 40 data rows well-formed); no line contains a pipe without starting with `|`
  outside the registry section other than none found.
- **used-by:** cells name `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
  and `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md`; both `test -e`
  pass from lane root (E11 clean), consistent with the `corpus/knowledge` symlink the mirror
  carries for `--file` resolution (`RowsScratch.md` risk 2).

### 6. Live-lane counters (bonus — mirror == live, so these must match)

```
$ …/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 …   kasegi	W04	S029 …   kasegi	ok	…/corpus/SOURCES.md   exit=0
$ …/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
rows 40, tier.A 37, tier.B 1, tier.C 2, mined 28, queued 9, rejected 3, missing 0   exit=0
```
Identical to the mirror numbers — the predicted post-append state of `RowsScratch.md` risk 3.

## Residual risk / gaps

- Escaped-pipe disguises are enumerable but not exhaustive (e.g. a cell could hold
  prose-with-semicolons masquerading as two cells — a content judgment, not schema; NF=13
  already excludes any `|`-based disguise).
- The `overdue` header comment (`:34-37`) understates that `cadence` lines cover `NNd` too;
  cosmetic, no verdict impact.
- `grep -c` returning 0 exits 1 — counts above report the count, not failure.

## Evidence anchors

- `.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md:42-46` — the five rows.
- `.ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md:4-8` — byte-identical block.
- `scripts/sources-census.sh:665` (E09 `NNd` acceptance), `:676-685` (cadence/overdue split).
- `wave1/RowsScratch.md:95-124` — claims reproduced 1:1.
