# ScoutMergePackage — shokuknow merge package probe for F22 (round 39, wave 2)

Seat: scout (attack/falsify), leaf, read-only on `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`$P`) and on the lane
(`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37`, claims-freeze `dcd3170`,
base `480b1a5`). Probe time 2026-10-26T20:14Z–20:15Z. No package tool run, no network fetch, no write outside the wave dir and
scratch `/fast/scratch/hyaku/kasegi-r39/ScoutMergePackage` (removed on exit).

## Verdict

- Package byte-identical to rounds 35–38: **yes** (70 files, one mtime, `SOURCES.append.md` sha256 matches).
- Staged entry competing with F22 (CISA When-to-Issue VEX): **none** — 0 package files mention VEX / issuance / reaffirm / CISA.
- Staged row colliding by *document* with lane S057 (or S056/S058/S059): **none**. Staged S055–S059 are five *different* documents
  than lane S055–S059; they collide by *id* only.
- Id-collision re-derivation at lane HEAD: registry **59**, staged **94**, collisions **29** (S031–S059), the predicted 25 + 4.
- Frozen C2 predicates not falsified by this probe; one non-falsifying observation (§6).

## 1. Byte identity (commands: `find`, `sha256sum`, `wc`)

```
find $P -type f | wc -l                         -> 70   (SOURCES.append.md, MERGE-REPORT.md, MERGE-REPORT.json + 67 knowledge)
ls $P/knowledge/corpus/knowledge | wc -l        -> 67
mtimes (find -printf '%TY-%Tm-%Td %TH:%TM:%TS') -> 70 files, single value 2026-10-24 23:33:20
find $P -type f -newer <lane>/.ufo/waves/round-39/claims.json | wc -l -> 0
wc -lc SOURCES.append.md                        -> 100 lines, 89718 bytes
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  SOURCES.append.md
0e6759b47595f1bce5fbf49bf0422838ff89a394b2f424d17fb17d96a09106df  MERGE-REPORT.md
8a42a9109c8c95bc55e818f0ad97e7923cbfe5a9e7792c72c59b5aaa3aecbf5b  MERGE-REPORT.json
```

`SOURCES.append.md` digest equals the spec value (`4fe049cb…73eb`) and the r38 `ScoutStandingRefusals`/`ExecIdCollision` value;
`MERGE-REPORT.md` and `.json` digests equal the r38 `ScoutStandingRefusals` §1 values (`0e6759b4…`, `8a42a910…`).

## 2. Competing-ground search (case-insensitive `grep -rliE` over all 70 files; hits = files / lines)

| term | files | lines |
|---|---|---|
| `when-issue`, `when-to-issue`, `when to issue` | 0 | 0 |
| `VEX` | 0 | 0 |
| `reaffirm` | 0 | 0 |
| `inheritance` | 0 | 0 |
| `issuance` | 0 | 0 |
| `cisa\.gov`, `csaf`, `openvex`, `cyclonedx`, `not_affected`, `minimum requirements` | 0 each | 0 |
| `ssvc`, `epss`, `kev|known exploited`, `sbom`, `software bill`, `downstream`, `upstream` | 0 each | 0 |
| `inherit` (substring) | 2 | 2 |
| `lifecycle` | 2 | 3 |
| `supplier` | 1 | 1 |
| `timestamp` | 2 | 3 |
| `affected` | 4 | 5 |
| `advisory|advisories` | 10 | 23 |
| `exploitab` | 7 | 15 |
| `MERGE-REPORT.md/.json` for `vex|cisa` | 0 | 0 |

Every non-zero hit read in context; none is VEX/issuance ground:
- `inherit`/`lifecycle`: `vendor-cvd-policy-crosswalk-2026-10-23.md:16,46` (Cisco policy "product lifecycle" scope boundary),
  `chinese-grading-standard-draft-2026-10-23.md:40` (draft "inherits the 2020 edition's three core dimensions"),
  `gb30279-2020-edition-provenance.md:23` (inherited vocabularies of a GB standard), `SOURCES.append.md:13` (S037 "lifecycle dates" of
  a Chinese standard catalogue entry).
- `timestamp`: `program-scope-rules-and-asset-boundaries.md:8` (HackerOne policy-version record timestamp recheck).
- `affected`/`supplier`: JP/CN disclosure-coordination prose (`vendor-third-party-finding-coordination…:22,30`, `authorization-safe-harbor-and-scope-2026-10-23-amendment.md:49`, `cnvd-canonical-advisory-cross-references…:20`, `japanese-severity-vocabulary…:46`).
- `advisory`: all in the JP/CN disclosure and CNVD/IPA lines (e.g. `cnvd-canonical-advisory-cross-references-2026-10-23.md`, `japanese-disclosure-legal-framework.md:30`); none is a status-lifecycle document.

URL level: `cisa.gov`, `openvex`, `cyclonedx.org`, `docs.oasis-open.org/csaf` — 0 hits across the package.

Staged `ground:` frontier ids (grep of all entries): F09, F12, F14, F20, F21, F24 and numbered round-ledger items; **no staged entry grounds
F22**. `F24` (`chinese-crowd-testing-national-standard-2026-10-23.md:9`) is not a lane F-id (`grep -cE '\bF24\b' corpus/README.md` → 0;
lane frontier tops at F22). Staged `ground: F20`/`F21` (`vendor-cvd-policy-crosswalk…`, `vendor-third-party-finding-coordination…`,
`chinese-grading-annexes-transcribed…`) name lane F-ids already admitted for different items (lane F20 = SSVC, F21 = OASIS CSAF; staged
F20/F21 = vendor disclosure policies / revised Chinese grading standard) — a re-grounding step the standing refusals already require; not
F22 competition.

**Competing staged entry: none (as expected).**

## 3. Staged rows that share an id with the new lane rows (by document: all different)

| id | staged document (URL) | lane document (URL) | same doc? |
|---|---|---|---|
| S055 | cybozu.co.jp/company/security-policy/ (Cybozu handling policy; duplicate of lane **S036**) | docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html (CSAF 2.0) | no |
| S056 | cybozu.co.jp/products/bug-bounty/faq/ (duplicate of lane **S037**) | cisa.gov/…/minimum-requirements-vulnerability-exploitability-exchange-vex (rejected row) | no |
| **S057** | pepabo.com/contact/vulnerability-reporting/ (duplicate of lane **S038**) | **cisa.gov/resources-tools/resources/when-issue-vex-information** (F22) | **no** |
| S058 | ipa.go.jp/security/todokede/vuln/uketsuke.html | github.com/openvex/spec/blob/main/OPENVEX-SPEC.md (rejected row) | no |
| S059 | phic.org.cn/…/P020260909380470895113.pdf (CNVD weekly 2026.8.24–8.30) | cyclonedx.org/docs/1.7/json/ (rejected row) | no |

Staged **entries** that cite S055–S059 as `source:` lines (textual id-collision hazard only, since their S-numbers mean the staged
documents): `program-quirks-2026-10-23-amendment.md` (S055, S056, S057), `japanese-vendor-disclosure-policies-2026-10-23.md` (S055, S056,
S057), `authorization-safe-harbor-and-scope-2026-10-23-amendment.md` (S057, S058), `chinese-national-grading-applied-2026-10-23.md` (S059).
Adopting any of these verbatim would make `source: S057` in the lane resolve to the CISA row (F22 entry `cisa-when-to-issue-vex.md`
is the lane's only `^source: S057` file: `grep -rlE '^source: S057' corpus/knowledge | wc -l` → 1) while the entry's body means Pepabo. No
adoption is proposed, so this is a standing hazard, not a defect in the landed work. Staged-S057 → document-level duplicate of lane S038.

## 4. Re-derived id lists (0–3-space extractor) at lane HEAD `5006097`

```
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
grep -oE "$PAT" <lane>/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE "$PAT" $P/SOURCES.append.md     | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
 59 reg-ids       (S001..S059, 59 unique, 295 bytes)
 94 staged-ids    (S031..S124, 94 unique, 470 bytes)
 29 collisions    (S031..S059, 145 bytes)
b698a2460f64e9a247954e1f9eec005bf4c59058446ae609806362808173ea2f  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
5b959cc58fc5c6a25c60713b090e30839043a9ec14f1b507c2378dd8e86ae9d0  collisions
collision list: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059
```

- `staged-ids` sha256 `550a0129…6948019f` is the same value in r31, r34, r38 and r39 wave 1 — package stable.
- Consistency with wave 1 (`wave1/ExecAssimilationIds.md`, run at base-registry 55): reg-ids 55 → 25 collisions (S031–S055), sha `cd5ee2d9…`/`0875ecb4…`.
  At HEAD with S056–S059 landed: 59 → 29, i.e. exactly +4 ids, each a new collision (S056–S059 all ≥ S031 and ≤ S124). Consistent.
- Column-zero variant (`^\|[[:space:]]*S[0-9]{3,}`): staged 94, registry 59 — equal to the 0–3-space extractor on both files (no
  indented rows). `grep -cE '^ {4,}\|'` → 0 on both files: the 4+-space blind spot remains empty.
- Registry count form: claim form `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **59** at HEAD — the E1
  after-count (59), not the as-frozen 58. Frontier rows `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 22; `ls corpus/knowledge/*.md | wc -l` → 51;
  `source: S057` entries → 1.
- Document-level duplicates (per-row first URL, lane map vs staged map): **21** staged rows carry a URL already in the lane registry (same
  count as r38, 19 distinct URLs shared); **0** of them map to lane S055–S059 (their lane ids are S032–S050 and S036/S037/S038 for staged
  S055/S056/S057). So the new rows added no document-level overlap with the package; same-id-same-document stays at 1 (S042).

```
staged->lane (dup docs): S031->S043 S032->S044 S033->S045 S034->S049 S035->S050 S039->S033 S040->S034 S041->S035 S042->S042 S043->S041
S049->S046 S050->S047 S055->S036 S056->S037 S057->S038 S060->S039 S064->S041 S068->S040 S076->S041 S080->S048 S123->S032
```

## 5. Quarantine slice

Four same-name entries exist in both trees at HEAD: `authorised-testing-rules-of-engagement.md` (lane `5533fc87…` vs staged
`bf40409e…`), `japanese-domestic-disclosure-workflow.md` (`a22d2321…` vs `ee667c2f…`), `japanese-severity-vocabulary-and-impact-model.md`
(`f584f06c…` vs `d7fdd31f…`), `program-severity-ladders-and-reward-scales.md` (`6c05c98f…` vs `35de5f8b…`) — all DIFF; none concerns VEX,
issuance, or CISA. (Only the last is on the r38 seven-row standing-refusal table; the other three are older lane entries, last commits
2026-10-25, with different bytes from the staged copies; not a round-39 flip.) Nothing here is an adoptable F22 competitor.

## 6. Observations (non-falsifying)

- `claims.json` `frozen_at_utc` reads `2026-10-26T20:30:00Z`, but the claims-freeze commit `dcd3170` is dated `2026-10-26T16:26:41-03:00`
  (= 19:26:41Z) and this probe ran at 20:14Z. The field is later than the freeze commit and the then-wall-clock; it is a nominal stamp, not
  a gate input. No predicate depends on it.
- The frozen C2 counting command `registry -> 58` is superseded by E1 (59); measured 59 at HEAD.
- Package-wide, there is no package ground for the VEX layer at all (F20 SSVC, F21 CSAF and F22 are all live-capture admissions): the
  r38 observation stands and extends to F22.

## 7. Falsification attempts and outcomes

| attempt | outcome |
|---|---|
| package changed since r38 (digest, file count, mtime) | no — identical |
| any staged entry/row covers CISA issuance/lifecycle/reaffirmation/inheritance | no — 0 hits on 15 direct terms |
| staged row for the same document as S057 under another id | no — staged docs for ids S055–S059 are Cybozu×2, Pepabo, IPA, CNVD weekly; none is CISA/OpenVEX/CycloneDX/CSAF |
| id intersection differs from predicted 25→29 | no — 29 measured |
| F22 re-used as a staged `ground:` | no — 0 staged F22 grounds |
| indented (4+) row hiding a collision | no — 0 rows |

Deliverable: this file. Scratch removed before yield.
