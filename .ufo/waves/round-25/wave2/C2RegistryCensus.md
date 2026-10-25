# C2RegistryCensus — wave-2 falsification of the round-25 registry census

Seat: `C2RegistryCensus` (reviewer, read-only). Attacked item: the registry-census limb of
claim C2 — the wave-1 prediction in `wave1/ScoutCensusWarnings.md` (and the
`frontier_step.census_before` baseline in `claims.json`) that after appending the five
normalized rows the lane census reads `rows 40`, schema clean, exactly the two pre-existing
W04s (S028, S029), `exit 0`.

Run at 2026-10-25T08:59Z against the live lane tree (round-25 work present but **uncommitted**:
`git status` shows `corpus/SOURCES.md` modified, HEAD still `b49948f`). The census script reads
the working file, so the figures below are the post-append state.

## Verdict: CONFIRMED — every limb of the wave-1 census prediction reproduces exactly. No correction needed.

| limb | wave-1 predicted | wave-2 measured | match |
|---|---|---|---|
| rows | 40 | 40 | yes |
| schema | clean, NF=13, no E-codes | 40/40 rows NF=13, zero E-codes, zero duplicate ids | yes |
| W04s | exactly {S028, S029}, pre-existing | exactly {S028, S029}, no W04 on S036–S040 | yes |
| exit | 0 | 0 | yes |
| tier/status | A=37 B=1 C=2, mined=28 queued=9 rejected=3 | identical | yes |

## Commands, output, exits (verbatim)

### Canonical counter (the `claims.json` frontier_step census command)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

E-code count in that output: `grep -cE 'E[0-9]{2}'` → **0**. W04 count → **2**.

### Census mode (row/tier/status totals)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin
kasegi	rows	40
kasegi	tier.A	37
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	28
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	2899
FLEET	tier.A	2395
FLEET	tier.B	395
FLEET	tier.C	109
FLEET	tier.invalid	0
FLEET	status.queued	295
FLEET	status.mined	2404
FLEET	status.rejected	200
FLEET	status.invalid	0
FLEET	missing	0
EXIT=0
```

### Independent schema/row checks (outside the script)

```
$ awk -F'|' '/^\| S[0-9]/{n++; if(NF!=13) print "BAD"} END{print n}' corpus/SOURCES.md
rows=40          # zero BAD lines → all 40 rows NF=13 (11 columns + 2 edge fields)

$ awk -F'|' '/^\| S[0-9]/{print $2}' corpus/SOURCES.md | tr -d ' ' | sort | uniq -d
(empty)          # no duplicate ids; ids run S001–S040 contiguous

$ git diff corpus/SOURCES.md
@@ -39,6 +39,11 @@        # pure append: +5 lines (S036–S040), zero context edits
corpus/SOURCES.md | 5 +++++
```

`git show HEAD:corpus/SOURCES.md` last row = S035 (35 rows committed) — so the five new rows
are S036–S040, exactly the `RowsScratch`/`CollisionGuard` id mapping.

### used-by resolution (the wave-1 E11 sequencing risk — discharged)

All five new rows are `status=mined`, so E11 inspects their `used-by` cells:

| row | used-by | target on disk? |
|---|---|---|
| S036 | vendor-disclosure-policies-as-corpus-objects.md, vendor-disclosure-policy-commitments-crosswalk.md | both exist |
| S037 | vendor-disclosure-policies-as-corpus-objects.md | exists |
| S038 | both | both exist |
| S039 | both | both exist |
| S040 | vendor-disclosure-policy-commitments-crosswalk.md | exists |

```
$ ls -la corpus/knowledge/vendor-disclosure-*.md
-rw-r--r-- 13961 Oct 25 05:49 corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
-rw-r--r-- 16211 Oct 25 05:43 corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

Both prerequisite entries landed before/with the append → validate exit 0, not the 5×E11
failure mode `ScoutCensusWarnings.md` §c warned about.

## W04 provenance (the "pre-existing" limb)

Both warnings name rows opened **2026-10-20** (`corpus/SOURCES.md:34` S028, `:35` S029), five
days before the round-25 rows (opened 2026-10-25). They duplicate URLs held by S006
(docs.hackerone.com safe-harbor FAQ) and S024 (eur-lex CRA OJ) — both older rows. None of the
five new URLs (cybozu.co.jp ×2 distinct paths, pepabo.com, hitachi.co.jp, cisco.com) collides
with any existing row, matching `ScoutCensusWarnings.md` §d's URL-overlap analysis: W04
compares normalized host+path, so the two cybozu.co.jp rows cannot fire it.

## File:line evidence

- `corpus/SOURCES.md:3` — `## Registry` heading; table header at lines 5–6; rows S001–S040
  span lines 7–46; `## Paths` section resumes at line 48. All 40 row-shaped lines are inside
  the Registry section (no E12 surface).
- `corpus/SOURCES.md:42-46` — the five appended rows S036–S040.
- `corpus/SOURCES.md:34,35` — S028 and S029, the two W04 rows.
- `scripts/sources-census.sh:24-33` — E01–E12/W01–W04 code definitions; exit contract at
  lines 16-18 (W-codes never change exit; clean lane → `ok` + exit 0).
- `.ufo/waves/round-25/claims.json:39` — frozen `census_before` (rows 35, W04 x2 S028,S029)
  is consistent: 35 committed rows + 5 appended = 40 measured.
- `.ufo/waves/round-25/wave1/ScoutCensusWarnings.md:112` — predicted `rows 40 / tier.A 37 /
  status.mined 28`; line 111 predicted unchanged warning set. Both reproduce verbatim.

## Residual risk / gaps

- Scope: this seat verified the **registry census limb** only. The other C2 limbs
  (`frontier=10` in `corpus/README.md`, entries citing S036+ headers) and the manifest
  (5 sources / 39 quotes) belong to sibling seats and were not re-run here.
- The round-25 mutations are still uncommitted in the working tree; the census result is
  correct for the bytes on disk now. A later edit to `SOURCES.md` invalidates these figures.
- The `sources-census.sh` header documents `validate` exit 0 as "clean **or warnings**" —
  exit 0 alone does not prove zero warnings; the two W04s were confirmed by parsing stdout,
  not inferred from the exit code.
- `E04` (duplicate URL *within* a scope) was checked implicitly: validate exit 0 with zero
  E-codes means none of the five new rows shares normalized URL+scope with an existing row.

## Tooling

None installed or updated. Used only `bash`, `gawk`, `git`, `ls`, `grep` — all pre-existing.
No pacman/uv/cargo/npm transactions.

## Verdict

**Wave-1 census result CONFIRMED.** Re-running the canonical command on the post-append tree
yields rows=40, zero E-codes, exactly {W04 S028, W04 S029}, exit 0 — matching both the
`ScoutCensusWarnings.md` prediction and the `claims.json` `frontier_step` accounting. The
smallest correction is: none.
