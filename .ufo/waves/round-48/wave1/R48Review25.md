# R48Review25 — Source census: S077-only delta, immutable cells preserved

- Seat: R48Review25 (reviewer, leaf — no subagent dispatch)
- Round: 48, kasegi lane; lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Frozen claim: `.ufo/waves/round-48/claims.json`; assignment header pins commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` ("round-48: freeze canonical checklist restoration and controls", verified ancestor of HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031`); on-disk file sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` equals `.ufo/waves/round-48/freeze.txt` `claims-sha256`. freeze.txt `base: 903d47e13058982460f0d90c1c2b9c7c02680646`.
- Census control (before): `.ufo/waves/round-48/controls/census-before.txt` — output of `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` at freeze time.
- Census instrument: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (fleet root; read-only validator; modes `census|validate|overdue|shared|selftest`; contract SOURCES-CONTRACT-v1: 11 columns ⇒ NF=13, statuses queued|mined|rejected).
- Registry: `corpus/SOURCES.md` — live sha256 `f0a3a3e96501545fb8457f303f005fa676830d844dea6b72b133ac49c280d613`; base-commit (903d47e1) copy sha256 `2d3d1d15eeffc10f6803500dbf1535cec05a0423ae6b468c269337e3e1f257b8`.
- Round-47 verifier routes R1/R2: R1 = canonical-form drift, R2 = prose-sensitive count (`corpus/lessons/round-48.md` Mistakes table, citing `round-47-verifier-spotcheck.md`). R1 is SHONEN-side, not census-side. R2 is registry-adjacent and directly informs this seat: row-shape anchoring must discriminate a real registry row from narrative prose. Both are context, not separate census counters.

## Task

Run source census on the current registry and compare before; verify S077 only added row and existing immutable cells preserved.

## Observed commands and output

1. Live source-census gate, compared byte-for-byte against the frozen before-control:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

`diff .ufo/waves/round-48/controls/census-before.txt <live output>` → `DIFF_EXIT=0` (byte-identical: same 4 pre-existing by-design W04 warnings, same order, same ok line, same exit 0). S077 introduced zero new validator findings and removed none.

2. Census counts, before vs after:

| metric | before (base 903d47e1 registry copy, `census --file`, EXIT=0) | after (live, `census --root /home/vgpnk/Projects/shokunin kasegi`, EXIT=0) |
|---|---|---|
| rows | 76 | 77 |
| tier.A | 69 | 70 |
| tier.B | 4 | 4 |
| tier.C | 3 | 3 |
| status.mined | 61 | 62 |
| status.rejected | 15 | 15 |
| status.queued | 0 | 0 |
| tier.invalid / status.invalid / missing | 0 / 0 / 0 | 0 / 0 / 0 |

Delta = exactly +1 row, +1 tier.A, +1 mined = the S077 row (`own-work`, tier A, `mined`). Every other count identical.

3. Only-added-row / immutable-cells proof (git, read-only):

```
$ git diff --numstat 903d47e13058982460f0d90c1c2b9c7c02680646 -- corpus/SOURCES.md
2	0	corpus/SOURCES.md
$ git diff --numstat 3546f7089c224ac6c8adc68208b1e648bbf3e6a5 -- corpus/SOURCES.md
2	0	corpus/SOURCES.md
$ git diff 903d47e1... -- corpus/SOURCES.md | grep -c '^-[^-]'
0
```

2 insertions, 0 deletions against both the claims base and the freeze commit; zero deletion lines. The two inserted lines and only these:
- line 83: the `| S077 | … |` registry row;
- line 119: one Round-48 bounded-protocol-repair narrative bullet in the `## Paths` search-log section.

All pre-existing rows — including the immutable id/anchor cells of S001–S076 — are byte-identical between base, freeze, and worktree; any mutated cell would appear as a deletion+addition pair and none does.

4. S077 row contract conformance (from the live validate run — no E-codes emitted, and direct checks):

- NF=13 (11 columns) on the S077 row; all 77 registry rows NF=13 (`awk` scan: 0 malformed).
- id `S077` matches `S[0-9]{3,}`, no duplicate id (no E02/E03).
- URL `.ufo/waves/round-48/controls/protocol-source.txt` unique across scopes (no W04/E04).
- kind `own-work` in enum (no E05); tier A non-community (no E06/E10); status `mined` (no E07).
- opened `2026-10-30` = today, a past/present ISO date (no E08); recheck `on-release` symbolic cadence (no E09).
- used-by `corpus/lessons/round-48.md` exists on disk (2744 bytes; no E11; census `missing=0`) and cites S077 at its line 14, closing the used-by loop.
- Row content matches the S077 source snapshot: `controls/protocol-source.txt:439` `## File contract per shokunin repo` and the verbatim canonical four-box SHONEN seed immediately following it.

## Expected vs observed

| Check | Expected | Observed | Match |
|---|---|---|---|
| Live `validate` vs frozen `census-before.txt` | byte-identical, exit 0 | byte-identical (`DIFF_EXIT=0`), exit 0 | yes |
| Registry delta vs base 903d47e1 | S077 row only added | 2 insertions / 0 deletions (S077 row + 1 narrative bullet) | yes |
| Registry delta vs freeze 3546f70 | unchanged since freeze | 2 insertions / 0 deletions — identical delta | yes |
| Census counts before→after | +1 row, +1 tier.A, +1 mined, else identical | exactly that | yes |
| Existing immutable cells | preserved byte-for-byte | 0 deletion lines; numstat `2 0` both refs | yes |
| S077 row well-formedness | NF=13, no E-codes, used-by exists | confirmed (see §4) | yes |

## R1/R2 interaction

R2's lesson (prose-sensitive count; row-shape anchoring) is honored by this delta: the S077 change is one row-shaped registry row plus one clearly narrative bullet, both pure insertions — no existing row's cells were edited, and the validator's row/prose discrimination is unchanged (same 4 W04 by-design findings before and after). R1 (canonical-form drift) is SHONEN-side; the census gate does not read SHONEN.md, so no census interaction. Neither route is a separate census counter.

## Scope and hygiene

- Read-only probes only: `sources-census.sh validate/census` against the live registry and a scratch copy of the base-commit registry; `git diff/show/merge-base/log` for byte-level comparison. No production files, fleet files, sibling trees, or git/jj state edited; no commit/push; no delegation; no background jobs.
- `git status` at the lane root shows pre-existing worktree state (`M SKILL.md`, `M corpus/QUALITY.md`, SHONEN.md restored, sibling wave reports) authored by the integration owner/candidate, none by this seat.
- Probe artifact note: running `validate --file` on the scratch base copy emits E11 used-by noise because used-by paths resolve relative to CWD; that is a fixture-location artifact, not a registry defect. The authoritative before/after comparison uses the identical frozen command (`validate --root /home/vgpnk/Projects/shokunin kasegi`) whose outputs are byte-identical.
- No tool installs were needed or performed this wave (pacman untouched).

## Verdict

Source-census review passes: the live registry census gate is byte-identical to the frozen before-control (exit 0, same four by-design W04 warnings); the before→after census delta is exactly the S077 row (+1 row, +1 tier.A, +1 mined, all other counts unchanged); and the registry diff against both the claims base and the freeze commit is purely additive (`2 0`, zero deletion lines), so every pre-existing immutable cell is preserved. S077 conforms to SOURCES-CONTRACT-v1 (NF=13, valid enums, unique URL, existing used-by that cites it). No census-side defect observed; nothing to repair.
