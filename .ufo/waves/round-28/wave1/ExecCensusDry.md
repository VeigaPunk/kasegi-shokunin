# ExecCensusDry — round-28 pre-landing census dry-run

Scope: build a scratch mirror of the lane corpus, apply the planned C2 registry edit
(S042 append + S041 used-by gain), run `sources-census.sh validate --file`, paste the
output, and state whether the real append is safe. Scratch only — no production edit,
no commit, no spawn.

## Verdict

**Modelled append: GATE PASS** — `exit 0`, rows 41 → 42, no `E0x`, warnings only (the two pre-existing
`W04`). The registry row itself is safe to append.

**Live registry, as of the end of this seat's run: GATE FAIL (`exit 1`, two `E11`).** While the dry run was
in progress, ScribeRegistryC2 landed the real edit; ScribeEntryC2's entry has not landed. Live
`validate --file corpus/SOURCES.md` reports `E11 S041 missing used-by
corpus/knowledge/japanese-domestic-disclosure-workflow.md` and the same for `S042`, `exit=1`; the claim's
own `validate --root … kasegi` counter gives the same two findings, `census_exit=1`. C2's "census exits 0"
is **currently unmet**. No registry change is implied — the landed row produced no `E01/E03/E04/E08/E09`;
only the entry file is missing. Re-run after the entry lands (commands below).

Two conditions are not gate-visible and must be carried by the claim counters, not by the census:
the entry file must exist in the same commit as the S042 row (proved below: E11 ×2 otherwise), and the
"cite S041, do not re-register the guideline" decision (proved below: a re-registered JPCERT row is only
`W04`, exit 0).

## What was modelled, and on whose authority

`ScribeRegistryC2`'s draft receipt did not exist when this seat read
`.ufo/waves/round-28/receipts/` (empty at run start), so the row was **constructed**, not copied from a
draft: wording verbatim from the read-only assimilation package
(`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`, staged S042), `opened` normalized
`2026-10-23 → 2026-10-25` per `claims.json` C2, `used-by` set to exactly
`corpus/knowledge/japanese-domestic-disclosure-workflow.md`. S041's used-by cell gained the same entry.
Both edits were applied to a `/tmp` copy only.

Entry stand-in: the staged entry bytes copied verbatim (sha256 `ee667c2f…572ec`) into the mirror at the
claim path. Census `E11` reads only path existence, so the stand-in is faithful for this gate; it is
**not** a proposal for the lane entry content (ScribeEntryC2 owns that, with `S041`+`S042` headers).

## Evidence

| # | state | output | exit |
|---|---|---|---|
| B0 | unmodified mirror (control) | 2×`W04`, `ok`, rows 41 | 0 |
| B1 | registry edit, entry absent | 2×`W04`, `E11 S041`, `E11 S042` | **1** |
| B2 | **gate**: registry edit + entry present | 2×`W04`, `ok`, rows 42 | **0** |
| M1 | duplicate `S042` id | `E03 S042 duplicate id` | 1 |
| M2 | same URL **and** same scope, no supersedes | `E04 S043 duplicate url www.ipa.go.jp/…/process.html within scope …` | 1 |
| M3 | staged S043 re-registered beside S041 (same URL, different scope) | `W04 S043 duplicate url www.jpcert.or.jp/…` + `ok` | **0** |
| B6 | `sources-census.sh selftest` | 95 `killed` lines, `selftest ok` | 0 |
| L1 | **live** registry after the sibling's landing, entry absent | 2×`W04`, `E11 S041`, `E11 S042` | **1** |

L1 detail: production `corpus/SOURCES.md` sha256 `79c4ae7a…d693e` (`git diff --stat`: 4 insertions,
1 deletion), S042 present at line 48 with `NF=13`, rows 42, S041's used-by cell carrying the new entry,
`corpus/knowledge/japanese-domestic-disclosure-workflow.md` absent.

B0 reproduces the committed `.ufo/waves/round-28/census-before.txt` exactly except for the `--file` lane
label (`file`) and the registry path — same findings, same exit. Full verbatim output (gate, B1, all
mutants) is in `.ufo/waves/round-28/receipts/ExecCensusDry.txt`.

Facts checked on the appended row: `NF=13` (E01-clean), URL appears nowhere else in the lane registry
today (`grep` on the production file returned nothing), 42 registry rows after the edit.

## Landing conditions (from the runs, not from reading the intent)

1. `corpus/knowledge/japanese-domestic-disclosure-workflow.md` must land **with or before** the row — B1
   shows two `E11` findings and `exit 1` if it does not.
2. The S042 row must be inside the `## Registry` table; a row below `## Paths` is `E12`.
3. No `|` inside any cell, `NF=13`, `recheck` `180d`, `opened` `2026-10-25`.
   Note the census **cannot** check the claim's `opened` value: `2026-10-23` also passes `E08`.
4. S041's used-by gain is invisible to the census (E11 only proves that paths a row *does* list exist;
   no check requires a row to list a given entry). The claim counter must carry it.
5. Re-registering the JPCERT guideline as a second row passes the census (`W04`, exit 0, M3) — the
   "cited, not re-registered" clause is a human/claim check.

## Exact post-change re-runs (for the L1; unrun ≠ passed)

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md; echo exit=$?
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' \
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md   # expect 1
```

## Bounds kept

No production file touched by this seat. Production `corpus/SOURCES.md` was `fe148213…384481b` when the
mirror was taken and is `79c4ae7a…d693e` now — that delta is ScribeRegistryC2's landing, not this seat's
(`git status` on `corpus/` shows the sibling's edits only). Mirror lived in `/tmp/census-dry-r28.XKHc2x`
(ephemeral, 2.7M); nothing bulky was written under the lane (R14). No tool install. No VCS write. Lane
HEAD at run time `94f387c` (dispatch) over claims freeze `c9f8b11`.

Risk: `/tmp` is shared with the other wave-1 seats — an earlier mutant tree at the generic path
`/tmp/mutants` was removed by a sibling mid-run; all reported runs above were made after moving to the
seat-specific path and were re-verified in one pass.
