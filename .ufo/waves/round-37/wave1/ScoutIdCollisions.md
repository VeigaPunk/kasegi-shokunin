# ScoutIdCollisions — round 37 id-collision guard proof + real rerun

Seat: ScoutIdCollisions (scout, coverage). Receipt only; no lane/fleet/shokuknow writes. Scratch `/fast/scratch/hyaku/kasegi-r37/ScoutIdCollisions/` removed after this receipt.
Tooling installed: none.

## Inputs (read-only, hashed)

| input | path | sha256 |
|---|---|---|
| lane registry | `corpus/SOURCES.md` at lane HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0` (clean tracked tree; untracked round-37 evidence only) | `2ff7818ad2179c1f8ecf89262e3f8a84a585dfb4f64bbc1fa0e7dbc3be2465fe` |
| staged set | `$S/merge/kasegi/SOURCES.append.md` with `$S=/home/vgpnk/Projects/shokuknow` (same file r36 hashed as `4fe049cbe4ba`) | `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` |

Guard (the 0–3-space "wide" extractor): `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort`, then `comm -12 reg staged`.

## 1. Guard proof — indented-row fixture (GUARD WORKS)

Fixture `fx-reg.md` (5 lines): `| S001 |` (col 0), `  | S002 |` (2-space indent), `   | S003 |` (3-space), `    | S004 |` (4 spaces = code block, deliberately not a row), `| S010 |`.
Fixture `fx-staged.md`: `  | S002 | …` (indented), `| S099 | …`.

- reg ids (wide extractor): `S001 S002 S003 S010` (4) — S004 correctly excluded.
- staged ids (wide): `S002 S099` (2).
- `comm -12` → **collisions = 1: `S002`** — nonempty, so the guard is NOT broken; the indented row is caught.
- Negative control (col-0-only pattern `^\|[[:space:]]*S[0-9]{3,}`): reg ids 2, staged ids 2, **collisions = 0** → col-0-only extraction would have missed this collision; the 0–3-space widening is what catches it.
- Cross-check via the committed script `.ufo/waves/round-35/assimilation/collide-check.sh`: fixture `wide` → `reg_ids=4 staged_ids=2 collisions=1 ids=S002`; fixture `col0` → `collisions=0`.

## 2. Real rerun — registry 53 × staged 94

Counts: registry ids = **53** (unique 53), staged ids = **94** (unique 94), collisions = **23**. (Expected "23: S031–S052-ish"; actual range is **S031–S053**, contiguous, 23 ids.)
Any-indent row census (`^[[:space:]]*\|[[:space:]]*S[0-9]`): registry 53, staged 94 — no 4+-space-indented rows hiding outside the guard; staged has 96 `^|` lines = 94 rows + header + separator.

Registry id list (53): `S001 … S053` contiguous:
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053

Staged id list (94): `S031 … S124` contiguous:
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120 S121 S122 S123 S124

Collision file (`comm -12`, 23 lines):
```
S031
S032
S033
S034
S035
S036
S037
S038
S039
S040
S041
S042
S043
S044
S045
S046
S047
S048
S049
S050
S051
S052
S053
```
`cmp` of my regenerated `reg-ids`, `staged-ids`, `collisions` against the L1-prepared `.ufo/waves/round-37/assimilation/{reg-ids,staged-ids,collisions}`: all three byte-identical.
`collide-check.sh` on the real inputs: `kind=wide reg_ids=53 staged_ids=94 collisions=23 ids=S031…S053`; `kind=col0` identical (23) — no real row is indented, so both widths agree on the real data.

Verdict: every staged id S031–S053 collides with a different lane row (e.g. lane S053 = FIRST EPSS documentation page; staged S053 = METI 脆弱性関連情報取扱規程) → the 23 staged rows colliding by id cannot be appended as-is; S054–S124 (71 ids) do not collide with the 53-row registry at lane HEAD b362068.

## 3. Forward-looking flag (not in the item's claim, found while rerunning)

Lane HEAD registry has no S054. The frozen C2 claim adds lane row **S054 = SSVC** (https://certcc.github.io/SSVC/). Staged S054 is a different document (IPA 重要電子計算機… 要請, ipa.go.jp). After C2 lands, the same guard would report **24 collisions (S031–S054)** and staged S054 is likewise a collision, not an adoptable row. The id-collision gate text for the round-37 lesson should state the count at the head it is evaluated against (23 at b362068 pre-S054; 24 once S054 is in the registry) so the figure is not read as stale. No staged row is adopted either way.
