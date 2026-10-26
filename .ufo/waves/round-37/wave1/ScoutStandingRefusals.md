# ScoutStandingRefusals receipt — round 37 (package standing refusals re-measurement)

Read-only on `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`$S` = `/home/vgpnk/Projects/shokuknow`, so `$S/merge/kasegi/MERGE-REPORT.md`) and on the lane. No package tool run, no network call, no subagent, no tool installed, no scratch dir created (nothing to clean). Reads 2026-10-26, lane HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0` (tracked tree clean; only untracked round-37 wave artefacts). Baselines: `corpus/lessons/round-35.md` § "Standing refusals" (the seven-row reason/flip table), `corpus/lessons/round-36.md` Gate line 20 ("7 staged package entries unchanged, flip conditions unmet"), `.ufo/waves/round-36/wave1/ScoutStandingRefusals.md` (digests + flip evidence).

## Verdict

**Assimilation: none adopted.** All seven refusals stand: every reason is unchanged and **0 of 7 flip conditions triggered**. The package is byte-identical to rounds 35/36.

Note on source wording: `MERGE-REPORT.md` itself says `refused: 0` and lists 67 knowledge entries — it carries no per-entry refusal rows. The seven *standing refusals* are the lane's own decision (round-35 lesson table, re-confirmed round 36), made against the package; the report's only refusal instruction is adopt-checklist item 8 ("Do not touch rows marked refused until the stated reason is cleared"). Package header numbers unchanged: accepted 94, refused 0, entries 67, existing_rows 30, renumbered 0, first_id S031 (`MERGE-REPORT.json`).

## 1. Package byte-identity

- 70 files (67 knowledge + `SOURCES.append.md` + `MERGE-REPORT.md` + `MERGE-REPORT.json`) — same count as r36. All mtimes `2026-10-24 23:33:20 -0300`; `find -newer .ufo/waves/round-37/claims.json` → 0 files.
- `SOURCES.append.md` `4fe049cb…73eb`, `MERGE-REPORT.json` `8a42a910…bf5b`, `MERGE-REPORT.md` `0e6759b4…106df` — equal to the r36 receipt.
- Staged knowledge files live under `$S/merge/kasegi/knowledge/corpus/knowledge/` (67 files). Seven entries' sha256, all equal to the r36 receipt:

| staged entry | sha256 |
|---|---|
| program-scope-rules-and-asset-boundaries | `120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8` |
| claim-packaging-and-report-quality | `6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc` |
| cn-crowdsourced-testing-roles-and-conduct | `a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813` |
| chinese-crowd-testing-national-standard-2026-10-23 | `6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f` |
| chinese-criminal-thresholds-and-authorisation | `1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae` |
| chinese-program-severity-instrument | `442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c` |
| program-severity-ladders-and-reward-scales | `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87` |

- Lane same-name `corpus/knowledge/program-severity-ladders-and-reward-scales.md` → `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6` (last touched `0ab8929`, 2026-10-25; unchanged since r36; still ≠ staged `35de5f8b…`). The other six staged names have no lane file (`git ls-files --error-unmatch` fails for each).

## 2. Seven-row status table

| # | staged entry | reason it stays refused (re-measured r37) | flip condition (unchanged) | met? | r37 evidence |
|---|---|---|---|---|---|
| 1 | `program-scope-rules-and-asset-boundaries` | 0 located quotes; no executable recheck; `ground: F09` collides with admitted lane F09 | located quote + executable recheck + non-colliding frontier id | **No — refused stands** | `txt:\d+` locators in body → 0; cites S031/S034/S035 whose staged ids collide with lane rows of different documents; `ground: F09` = lane F09 (authorisation outside the platform, `PROVINCE.md:38`); no lane file |
| 2 | `claim-packaging-and-report-quality` | body cites S036 (BILISRC V1.7) which is in no lane row and no capture | an S036 row + capture | **No — refused stands** | lane `S036` = Cybozu policy (different doc); `grep -rlE 'BILISRC_V1\.7\|security\.bilibili\.com/static' corpus` outside lessons → 0 files; `txt:` locators 0; `ground: F11` = lane F11 (ISO 29147/30111, `PROVINCE.md:41`) |
| 3 | `cn-crowdsourced-testing-roles-and-conduct` | H1 count 0 (no entry shape); S081/S082 in no row/capture | an entry shape + the two rows | **No — refused stands** | H1 count 0; `S081`/`S082` absent as registry rows (`corpus/SOURCES.md` hits only prose lines 78–79, the r31/r33 sweep notes, not rows — grep `S08[12]` shows no `\| S08x \|` row); staged `ground:` is a ledger-item sentence, not an F-id |
| 4 | `chinese-crowd-testing-national-standard-2026-10-23` | S077/S078/S079 unregistered; `ground: F24` is not a lane F-id | three rows + a real frontier id | **No — refused stands** | `\| S077/78/79 \|` rows in lane → 0 each; `F24` appears nowhere in `PROVINCE.md`/`README.md`; lane frontier tops at F19 in tracked HEAD (F20 is this round's in-flight C2, SSVC, unrelated to crowd testing) |
| 5 | `chinese-criminal-thresholds-and-authorisation` | three PRC legal sources in no row/capture; staged S044/S045/S046 ids collide with different lane rows | three rows + a renumber map | **No — refused stands** | `court.gov.cn`/`czt.ln.gov.cn`/`nj.jsjc.gov.cn` → 0 files in `corpus/` outside lessons; lane S044/S045/S046 = Bugcrowd README / Bugcrowd CWE mapping / JVN activity report (different docs); `renumbered: 0` in `MERGE-REPORT.json` (no map supplied); `ground: F12` = lane F12 (Japanese state-coordinated disclosure) |
| 6 | `chinese-program-severity-instrument` | S047 (sse.com.cn) unregistered; anchor `newsType_6` not locatable in `round-32/S049.txt` | the row + a locatable anchor | **No — refused stands** | `sse.com.cn` → 0 files outside lessons; lane `S047` = IPA JVN quarterly report (different doc); `grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → 0 (`newsType_21` → 1); `ground: F10 (extends F01)` = staged numbering, lane F10 is vendor disclosure policies |
| 7 | `program-severity-ladders-and-reward-scales` | same-name lane file differs (`6c05c98f…` vs `35de5f8b…`); S036 half unregistered | byte-identity or a supersedes row | **No — refused stands** | digests as in §1 (unequal); no supersedes row for it (`corpus/QUALITY.md` R8 is the only supersedes rule row; no registry row begins "supersedes" for this file); S036 BILISRC still unregistered (row 2) |

## 3. Lane state since r36 (what moved; none of it is a flip)

- Lane registry **53 rows (S001–S053)** — S053 (FIRST EPSS) landed in r36; **S054 not yet in the tracked registry** (`grep -c '^| S054 ' corpus/SOURCES.md` → 0; this round's C2 row is in flight). `knowledge/` tracked files 48 (49 after F20 entry).
- Round-37 id-collision rerun artefacts re-derived by me: `reg-ids` (53) equals the lane registry ids exactly; `comm -12 reg-ids staged-ids` → **23** = `collisions` file lines (S031–S053 contiguous). It was 22 at r36; +1 is the lane's own S053 (EPSS) landing against staged `S053` (METI vulnerability-handling rule — a different document), exactly the prediction in the r36 lesson. None of the seven entries cites S053 or S052.
- Forward note (not a flip): when lane `S054` (SSVC, https://certcc.github.io/SSVC/) lands this round the collision span becomes S031–S054 (24); staged `S054` is the IPA 要請 PDF (`.../request_to_ipa.pdf`), a different document. Package-wide greps for `ssvc|certcc|stakeholder-specific` → 0 files (also 0 for `epss|first.org` and `known exploited|cisa.gov`), so the package adds no ground for F18/F19/F20 and none of the seven cite them. Adoption remains by document, not by number.
- `quarantine-slice` (7 rows) is a separate item (ScoutQuarantine/round-37 slice), not these seven; its S037/S054 `payload-absent` and S048/S065/S068/S069/S070 unreachable verdicts do not touch any of the seven refusals.
- Observation carried from r36 §3 (additive, unchanged): `ground:` ids F10/F11/F12 of entries 2, 5, 6, 7 name lane F-ids already admitted for different items — a further implied reason a regrounding step would precede any adoption.

## 4. Summary

Seven of seven refusals stand. Package byte-identical: **yes**. Same reasons: **yes**. Cleared flip conditions: **0 of 7**. Only delta since r36: collision span S031–S052 → S031–S053 (22 → 23) from lane S053; 24 predicted when S054 lands.
