# ScoutStandingRefusals receipt — round 36 (package standing refusals re-confirmation)

Read-only on `/home/vgpnk/Projects/shokuknow/merge/kasegi/` and on the lane. No package tool run, no network call, no subagent, no tool installed, no scratch dir created (nothing to clean). Baseline: `corpus/lessons/round-35.md` § "Standing refusals" (lines 155–169) and `.ufo/waves/round-35/wave1/ScoutPackageThemes.md` § 1–3. Reads at 2026-10-26T15:3xZ, lane HEAD `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`.

## Verdict

**Assimilation: none.** The package is byte-identical to round 35, every one of the seven reasons is unchanged, and **no flip condition cleared**. All seven staged entries stay refused.

## 1. Package byte-identity (sha256sum, `find -type f`, `stat`)

70 files (67 knowledge + `SOURCES.append.md` + `MERGE-REPORT.md` + `MERGE-REPORT.json`) — same count as round 35. Every file mtime is `2026-10-24 23:33:20 -0300`; `find $P -type f -newer .ufo/waves/round-35/claims.json` → empty.

| file | sha256 (current) | equals round-35 receipt? |
|---|---|---|
| `SOURCES.append.md` | `4fe049cb…73eb` | yes |
| `MERGE-REPORT.json` | `8a42a910…bf5b` | yes |
| `MERGE-REPORT.md` | `0e6759b4…106df` | yes |
| `program-scope-rules-and-asset-boundaries.md` | `120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8` | yes |
| `claim-packaging-and-report-quality.md` | `6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc` | yes |
| `cn-crowdsourced-testing-roles-and-conduct.md` | `a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813` | yes |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | `6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f` | yes |
| `chinese-criminal-thresholds-and-authorisation.md` | `1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae` | yes |
| `chinese-program-severity-instrument.md` | `442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c` | yes |
| `program-severity-ladders-and-reward-scales.md` (staged) | `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87` | yes |

Lane same-name `corpus/knowledge/program-severity-ladders-and-reward-scales.md` → `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6` (unchanged; still ≠ staged `35de5f8b…`).

## 2. Lane state versus the flip conditions (what changed since round 35)

Lane registry now has **52 rows (S001–S052)** — S052 (CISA KEV, round-35 C2) has landed; `S053` not yet present (`grep -c '| S053 ' corpus/SOURCES.md` → 0); README frontier tops out at **F18**; `corpus/knowledge/` has 47 files. Staged ids vs lane ids: staged 94 rows (S031–S124), **22 collisions S031..S052** (was 21 at round 35; +1 from lane S052). The round-36 C2 row S053 will extend this to 23: staged `S053` is a different document (METI 経済産業省告示第19号 脆弱性関連情報取扱規程 `meti.go.jp/policy/netsecurity/vul_notification.pdf`) from the lane's planned S053 (FIRST EPSS). `grep -rliE 'epss|first\.org|exploit prediction'` over the package → 0 files, and none of the seven entries cites S052/S053, so neither the S052 landing nor the F19 admission can unblock any refused entry.

| staged entry | flip condition (round-35 table) | met now? | evidence this round |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries` | located quote + executable recheck + non-colliding frontier id | **No** | `txt:\d+` locators in body → 0; no recheck; `ground: F09` = lane F09 "Authorisation outside the platform" (different item, admitted) |
| `claim-packaging-and-report-quality` | S036 row + capture | **No** | body cites S034/S035/S036; lane `S036` is the Cybozu policy (different doc), BILISRC V1.7 (`security.bilibili.com/static/docs/BILISRC_V1.7.pdf`) in no row and no snapshot; only non-lesson `corpus/` hit of "BILISRC" is the do-not-adopt prose in `knowledge/program-severity-ladders-and-reward-scales.md:64` |
| `cn-crowdsourced-testing-roles-and-conduct` | entry shape + S081/S082 rows | **No** | H1 count 0; S081/S082 only in `corpus/SOURCES.md:76-77` prose recording the refusal, not as registry rows |
| `chinese-crowd-testing-national-standard-2026-10-23` | three rows + a real frontier id | **No** | S077/S078/S079 registry rows absent (only `kill-rule-check.py` fixture strings `S077.txt`); `ground: F24` — lane frontier ends F18 |
| `chinese-criminal-thresholds-and-authorisation` | three rows + renumber map | **No** | court.gov.cn / czt.ln.gov.cn / nj.jsjc.gov.cn → 0 hits anywhere in `corpus/` (lessons excluded); staged S044/S045/S046 still collide with lane rows of other documents |
| `chinese-program-severity-instrument` | row + locatable anchor | **No** | `sse.com.cn` → 0 hits; `newsType_6` → 0 in `corpus/source-snapshots/round-32/S049.txt`, `newsType_21` → 1 |
| `program-severity-ladders-and-reward-scales` | byte-identity or supersedes row | **No** | lane `6c05c98f…` vs staged `35de5f8b…`; S036 half still unregistered |

## 3. Observation (additive, not a changed verdict)

The staged `ground:` ids of four more entries name lane F-ids that are already admitted for *different* items: `claim-packaging…` `F11` (lane F11 = ISO/IEC 29147/30111 division of labour), `chinese-criminal-thresholds…` `F12` (lane F12 = Japanese state-coordinated disclosure), `chinese-program-severity-instrument` and `program-severity-ladders…` `F10` (lane F10 = vendor disclosure policies; the latter's `ground: F10 (...)` and the instrument's `F10 (extends F01)` are staged-numbering). Round 35 recorded this collision only for `program-scope…`; for these four it is a further, already-implied reason a renumber/regrounding step would be needed before any adoption. The refusal reasons themselves are unchanged.

## 4. Unmet-flip summary

Seven of seven refusals stand. Package byte-identical: **yes**. Same reasons: **yes**. Cleared flip conditions: **0 of 7**. Only delta since round 35: registry collision span widened S031..S051 → S031..S052 (22) by the lane's own S052 row, and will widen to S053 (23) when the round-36 C2 row lands.
