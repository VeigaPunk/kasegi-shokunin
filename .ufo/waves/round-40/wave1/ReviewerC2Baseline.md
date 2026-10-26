# ReviewerC2Baseline — receipt (round 40, hyaku run 9)

Seat: leaf reviewer, C2 baseline re-derivation on the claims-freeze commit.
Date: 2026-10-26. No tools installed (none needed); no network fetches (no HTTP calls made; nothing to record). No git/jj mutation anywhere — only read-only git (`cat-file`, `show`, `diff --name-only`, `status --porcelain`, `archive | tar -x` into scratch). Disk guard green before work: `/fast/scratch/hyaku` at 26% use, 602.0G free.

## What was verified, with observed output

1. Freeze commit exists and is HEAD of the lane:
   `5e985b74075dd3813a63d7750966bf8abf693465 2026-10-26 18:10:32 -0300 round-40: freeze claims C1/C2 + control receipts`.
   `git diff --name-only base..freeze` lists exactly five `.ufo/waves/round-40` control files (c1-controls/before.txt, c2-controls/before.txt, c2-controls/junk-decisions.md, census-before.txt, claims.json) — the corpus at freeze is identical to base a7af2ce63bce153757d39bf66b366a96caf30c13.
2. Freeze tree exported read-only via `git archive 5e985b74… | tar -x` into scratch (`$S/freeze`); `cmp` confirms the export's `corpus/SOURCES.md` and `corpus/README.md` are byte-identical to the lane working tree; `git status --porcelain` shows no tracked modifications (untracked `.ufo/waves/round-40` round files only). The derived baseline is therefore also the live working-tree baseline.
3. Queued among the nine: **9** (claims counting command verbatim). Exhaustive queued-id sweep over the whole registry returns exactly `S016 S017 S019 S020 S021 S022 S023 S024 S025` — matches claims.json, no extra queued row.
4. Statuses of the nine: all `queued`; mined among the nine: **0**; knowledge entries citing any of the nine: **0**; S060+ rows: **0**.
5. Registry total: **59** (`grep -cE '^\|[[:space:]]*S[0-9]+[[:space:]]*\|' corpus/SOURCES.md`).
6. Frontier: **22** rows in `corpus/README.md` § Frontier; status-cell census `22 admitted, 0 non-admitted`.
7. Harness inside the freeze export: `python3 corpus/instruments/frontier-recheck-count.py` → `entries=25 pass=25 exit=0`. Full listing observed:
   ```
   PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
   PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
   PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
   PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
   PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
   PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
   PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
   PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
   PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
   PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
   PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
   PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
   PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
   PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
   PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
   PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
   PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
   PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
   PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
   PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
   PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
   PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
   PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0
   PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
   PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0
   entries=25 pass=25 exit=0
   ```
   (Trailing padding spaces from the instrument were trimmed in this receipt block only; the deliverable quotes the counted summary line.)
8. Supersession: S030 row read at freeze — status `mined`, teaches cell "supersedes S022 — use current 4.2.0 requirements and section numbering…", CNA Rules v4.2.0 (approved 2026-08-20) replacing S022's v4.1.0; bound to `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (same entry the harness F07 line cites, via S031 the current 4.2.6). S029 row read at freeze — status `mined`, teaches cell "supersedes S024 — official Article 14 text distinguishes vulnerability and incident reporting clocks; Article 71 applies Article 14 from 11 September 2026", bound to `corpus/knowledge/cra-manufacturer-reporting-duties.md` (harness F08 ids=S029). Both are genuine mined supersessions, matching claims.json. Context: S031 (v4.2.6, opened 2026-10-25) in turn supersedes S030 — consistent chain, no contradiction.
9. Junk control: `c2-controls/junk-decisions.md` fabricates all nine as `rejected`/evidence "none"; the frozen counter's mined-among-nine over its fabricated status column = 0 < 4 → rejected, as c2-controls/before.txt requires.
10. r22 measure re-derived from the lane's own SCORECARD.md criterion (F_total = frontier rows + queued registry rows; F_admitted = frontier rows with status `admitted`): 22 + 9 = 31; (20+22)/(20+31) = 42/51 = 0.8235 ≈ 0.824 — matches c2-controls/before.txt. (Fleet-level only in appearance; the criterion is fully lane-derivable, so no component was taken on faith.)
11. Census control: `census-before.txt` records `sources-census.sh validate … kasegi` → exit 0 with W04 S028/S029 only — matches claims.json C2.

## Discrepancy verdict

**No discrepancy with claims.json.** All eight C2 before-values reproduce at the freeze commit (queued 9 with exact ids; mined among nine 0; entries citing nine 0; S060+ 0; frontier 22; harness 25/25; registry 59; measure 42/51 = 0.824), and both supersession claims are confirmed by the S030/S029 rows. Data collection may proceed on this baseline.

## Deliverable

- Path: `.ufo/waves/round-40/wave1/ReviewerC2Baseline.txt`
- Lines: 66; sha256: `bb65893517d9d3c2dc248c0eca12d102097d195122344c30f1db11dcb30127ba`
- Contains only the re-derivation record (commands + outputs + verdict); validation evidence lives in this receipt.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ReviewerC2Baseline/` (freeze export + working files) removed before yield; nothing written outside the seat's allowed paths (wave1 deliverable + receipt, scratch).
