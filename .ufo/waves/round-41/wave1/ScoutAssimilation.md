# ScoutAssimilation — round 41 wave 1 receipt

Seat spec: sample exactly three staged knowledge entries from `/home/vgpnk/Projects/shokuknow/merge/kasegi/` whose target paths the lane already holds; compare staged content ground vs lane live entry; verdict additive/redundant/superseded; adopt-one-theme recommendation.

Deliverable: `.ufo/waves/round-41/wave1/ScoutAssimilation.txt` — 31 lines, sha256 `abd8bb37654aeb36b7b68e91f4629d54426378fa0c8fcff4550ebaaf93ae3c06`.

## Reads performed

- `.ufo/waves/round-41/claims.json` (frozen claims, read first, unmodified).
- `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md` (full): 94 accepted rows, 67 entries, first staged id S031, lane held 30 rows at staging; adopt checklist item 5 references an `amendments/` directory.
- `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.json` via python3: keys `{lane, accepted=94, refused=[], entries=67, existing_rows=30, renumbered=[], first_id}` — all 67 entries marked `new-file`; no duplicate-target flag field exists.
- `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` head + id sweep: staged range S031–S124, 94 rows (`grep -cE '^\| S[0-9]{3,}'` → 94; first S031, last S124).
- `find .../merge/kasegi/knowledge -type f` → 67 flat files under `knowledge/corpus/knowledge/`; **no `amendments/` directory exists** — amendments are staged as `*-amendment.md` new-file paths (packaging vs checklist inconsistency, noted in deliverable).
- Full reads: lane+staged `japanese-domestic-disclosure-workflow.md`, `program-severity-ladders-and-reward-scales.md`; lane `authorization-safe-harbor-and-scope.md`; both staged `authorization-safe-harbor-and-scope-2026-10-23{,-r4}-amendment.md`; heads of lane+staged `japanese-severity-vocabulary-and-impact-model.md`, `authorised-testing-rules-of-engagement.md`.

## Key evidence (commands run, observed output)

- Exact-name collisions staged-vs-lane (bytes): `japanese-domestic-disclosure-workflow` 3617/18544, `program-severity-ladders-and-reward-scales` 3187/8095, `japanese-severity-vocabulary-and-impact-model` 3666/7096, `authorised-testing-rules-of-engagement` 4180/5296 — lane larger in all four; four collisions total exist, spec capped the sample at three.
- Lane `japanese-domestic-disclosure-workflow.md` `ground:` line declares adoption of the staged entry re-grounded on round-28 captures; Limits record the staged draft's "six-step" web path vs captures' seven steps. Staged→lane id remap: staged S043 (JPCERT guideline) = lane S041; staged S042 (IPA) = lane S042.
- Lane `program-severity-ladders-...md` Limits: "staged package entry also included CNVD 众测 and BILISRC … not adopted this round"; id map staged S032→lane S044, S033→S045, S031→S043. CNVD/360SRC ground lives in `chinese-crowdsourced-testing-scope-and-rewards.md` (lane S049/S050, opened 2026-10-26). `grep -c bilibili corpus/SOURCES.md` → 0 (BILISRC is the residual additive doc).
- Lane `SOURCES.md` row count 62; knowledge files 59. Lane S041–S045 all `mined 2026-10-25` (independent re-registration, not package appends — different documents than staged same-ids).
- Amendment absorption check: `grep -l '経済産業省告示|内閣府|meti.go.jp|vul_notification|request_to_ipa|msrc/bounty-guidelines|pentest-rules-of-engagement|Washington Criminal Code| CFAA|Computer Fraud and Abuse'` over `corpus/knowledge/*.md corpus/SOURCES.md` → only `doj-vdp-framework-scope-and-authorization.md` (CFAA in a DOJ context, unrelated). METI notice / IPA 留意事項 / Cabinet Office 要請 / both MSRC docs absent from lane registry. Pepabo IS lane S038 (used-by `vendor-disclosure-policies-as-corpus-objects.md`, `vendor-disclosure-policy-commitments-crosswalk.md`) — present, but never cited by the safe-harbor entry.
- 受付機関/調整機関/公表判定委員会 grep hits in vendor-policy entries are Hitachi-policy vocabulary, not the METI notice — amendment ground confirmed absent.
- Lane S063 absent at read time (C2 lands it this round); staged S063 is a Gazette case — same id, different doc: the collision will exist once C2 lands.

## Verdict (per sample + package)

1. `japanese-domestic-disclosure-workflow.md` — SUPERSEDED (lane adopted, corrected, capture-pinned).
2. `program-severity-ladders-and-reward-scales.md` — SUPERSEDED except BILISRC residue (additive, unlanded).
3. `authorization-safe-harbor-and-scope.md` target — staged amendments ADDITIVE (5 of 6 documents absent from lane registry); Pepabo slice redundant.
4. Package: SUPERSEDED-at-collisions + unlandable-as-written — staged id range S031–S124 collides with committed lane S031–S062 on every shared id (32 collisions, different documents); verbatim `SOURCES.append.md` append corrupts the registry.

## Recommendation

Adopt one theme — "safe harbour and authorization beyond platform policy" — by landing the two amendments' documents as a dated lane amendment to the existing entry, re-captured under fresh lane ids (S064+). Reject wholesale adoption: it would overwrite two better entries, restore a corrected error, duplicate ≥4 documents, and collide the id space.

## Conduct

- Writes: only the two wave1 files above plus scratch dir (created `/fast/scratch/hyaku/kasegi-r41/ScoutAssimilation`, removed after use — verified gone). No git mutations, no fleet/shokuknow writes, no network fetches, no tool installs.
- Disk guard checked green before work; no heavy pass run anyway (read-only assignment).
- Remaining unknowns: whether other staged-only themes (Chinese criminal case law, GB/T 30279 revision chain) are also partially absorbed — outside the three-entry sample; id-collision count stated as the full overlap (32) since ranges are contiguous.
