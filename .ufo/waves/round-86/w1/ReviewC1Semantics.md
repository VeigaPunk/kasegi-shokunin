# ReviewC1Semantics — round-86 w1, C1 semantic review

Freeze 252df0c90c066d83d229e3107811a6bc05e8feed. Method: `git clone --shared` of the lane into
`/fast/scratch/hyaku/kasegi-r86/ReviewC1Semantics/land`, checkout of the freeze commit, applied
`.ufo/waves/round-86/c1/apply-map.py --root <clone> --map <clone>/.ufo/waves/round-86/c1/repair-map.json`
→ `APPLY files_changed=14 keys=203`. Read the full `git diff -- corpus/knowledge/` (292 insertions /
292 deletions, 14 files; receipt `ReviewC1Semantics-receipts/c1-knowledge.diff`), every changed line,
plus 98 sampled backticked full-path citations opened against snapshot text across 12 distinct
knowledge files and all 15 repointed snapshot ids (~54 anchored lines verified verbatim; receipt
`ReviewC1Semantics-receipts/anchor-sample.txt`). Machine cross-checks (digest binding, map
self-consistency, basename census, excluded count): `ReviewC1Semantics-receipts/manifest-and-excluded-checks.txt`.

## Finding 1 — WRONG (4 keys): the map rewrites a quoted manifest-record field, not a citation

Four knowledge files bind their pin to the round-40 manifest record and enumerate that record's own
field values: `…bound by the round-40 manifest record (id `S0xx`, path `S0xx.txt`, same digest, …)`.
The round-40 manifest records for S016/S020/S021/S023/S025 store `path` as the **bare basename**
(`path='S021.txt'` etc.; same convention in every round's manifest: round-45/46/47/49/57/69/70/71 all
store bare basenames). The map repointed exactly that quoted field value to the full lane path,
so the post-map sentence now asserts the manifest record's `path` field is
`corpus/source-snapshots/round-40/S0xx.txt` — false, and falsifiable by the very procedure the line
prescribes (read the record; the value differs). A manifest-field quotation is a quoted value, not a
snapshot citation — same class as the executed rule-B exclusion ("a command string is not a
citation"); the correct C1 move for these four keys was exclusion, not repoint. These are the only
changed line in each of the four files, so each file's entire diff is the defect:

| file:post-map line | key | evidence |
|---|---|---|
| cisa-bod-20-01-vdp-minimums.md:159 | `S021.txt` → `corpus/source-snapshots/round-40/S021.txt` | manifest round-40 record S021 `path='S021.txt'`; pin sha256 `72dbba…30e329` matches both |
| cisa-cvd-program-stages.md:131 | `S023.txt` → `…/round-40/S023.txt` | record S023 `path='S023.txt'` |
| cve-bench-agent-exploitation-benchmark.md:138 | `S025.txt` → `…/round-40/S025.txt` | record S025 `path='S025.txt'` |
| doj-vdp-framework-scope-and-authorization.md:136 | `S020.txt` → `…/round-40/S020.txt` | record S020 `path='S020.txt'` |

Re-run (prints the mismatch the four lines now deny):
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B -c "import json;print([ (r['id'],r['path']) for r in json.load(open('corpus/source-snapshots/round-40/manifest.json')) if r['id'] in ('S020','S021','S023','S025')])" && sed -n '159p' corpus/knowledge/cisa-bod-20-01-vdp-minimums.md | cut -c1-260
```
(Working-tree paths; same lines in the freeze clone — receipts hold the applied diff.) Note S016's
anthropic file escapes this class: its single changed line cites the capture for quote matching, not
a manifest field.

## Per-file verdicts (all 14 changed files)

- anthropic-cvd-provenance-and-pacing.md — CORRECT. 1 line; FC-1's "matched … against" now names the round-40 capture; `S016.txt:Lnn` template and the `grep -n 'Last updated' S016.txt` command string correctly untouched.
- cisa-bod-20-01-vdp-minimums.md — WRONG (Finding 1, key `S021.txt`).
- cisa-cvd-program-stages.md — WRONG (Finding 1, key `S023.txt`).
- cve-bench-agent-exploitation-benchmark.md — WRONG (Finding 1, key `S025.txt`).
- cve-services-publication-api.md — CORRECT. 16 repoints, all round-49; anchors 6/125/1368/1480/1594/1798/5285/6354 (x2 tables) verified verbatim against S078.txt (e.g. L125 "Reserves CVE IDs for the organization provided in the short_name query parameter…").
- doj-vdp-framework-scope-and-authorization.md — WRONG (Finding 1, key `S020.txt`).
- github-advisory-database-curation-semantics.md — CORRECT. 43 lines, all round-70; anchors 567/569/570/571/572/573/573-582/584/585/586-597/589/597/598/599/600/601/602/603/604/605/606/607/611-616/621/622/623/623-627/628/639/639-640/640/642/643 sampled against S105.txt and all support (e.g. L607 "Our malware advisories are mostly about substitution attacks…", L623-627 the four CVSS Section 5 bands). Untouched bare prose `(S103.txt:275-276)` at the 101-hunk is unbackticked — out of the map's backticked scope, consistent.
- github-global-security-advisories-rest-api.md — CORRECT. 35 lines, all round-69; anchors 13/273/274/275/276/282/283/289-290/291-294/293/294/295-299/300-302/303-305/306-307/308-311/312-320/321-326/323/327-341/345-346/349/356/357/358-456/360/365-430/457/458/465/471/475-476/486/487 sampled and support (e.g. L13 "API Version: 2026-03-10 (latest)", L297-299 the 13-ecosystem list, L365-430 example keys). The `S103.txt:LINE` placeholder is correctly not a key.
- github-private-vulnerability-reporting.md — CORRECT. 18 lines, all round-46; anchors 560/561/563/564/566/567/568/569/573/574/575/577/578/579 sampled and support (e.g. L561 "Owners and administrators of public repositories…", L575 "GitHub will display a message letting you know that maintainers have been notified…"). Unbackticked prose "body prose is S073.txt:556-579" left bare — out of scope, consistent.
- github-repository-security-advisories.md — CORRECT. 45 lines, all round-47; anchors 558/559/561/568/570/571/572/573/574/575/577/578/581/582/583/584/589/590/591/592/594/596/598/599/600 sampled and support (e.g. L558 the three-phase summary, L577 dual-sentence line, L589 credits-public line). Unbackticked `S076.txt:558-600` style refs left bare — consistent.
- iso-29147-30111-standard-records.md — CORRECT. 3 lines; S089→round-57, S090→round-57, matching the rows' anchor cells; anchors 1/52/53/54/59/97/103/105/107 (S089) and 1/52/53/54/59/90/96/98/100 (S090) verified (e.g. L1 titles, L54 "Edition 2", L105 "ISO/IEC JTC 1/SC 27"). Unbackticked `S089.txt:84 Q2` refs left bare — consistent.
- linux-kernel-security-bugs-reporting-process.md — CORRECT. 25 lines, all round-45; anchors 17-18/20-21/20-47/21-22/22-23/23-24/37-39/39-40/41-43/84-87/92-93/95-96/96/96-98/99/117/201/208-209/210-211/213-219/232-237/239-250/257/271-276/305/305-306/309-312/313-315/329-357/332/333-334/359-366/371-372 sampled and support (e.g. L309-310 postponement-at-request, L332 "solely focuses on getting bugs fixed", L239-250 the AI MUST list).
- zdi-disclosure-policy.md — CORRECT. 17 lines, all round-47, matching the S075 row's anchor cell "lines 20-27 of corpus/source-snapshots/round-47/S075.txt"; anchors 20-27/22/23/24/25/26 verified (e.g. L24 "four months (120 days) to address the vulnerability").
- zdi-disclosure-process-and-vendor-coordination.md — CORRECT. 85 lines; S106→round-71 (matches the S106 row's Q01-Q15 anchor cells) and the cross-row `S075.txt:25` → round-47; anchors 28/31/47/49/51/52/60/61/62/69/70/72 sampled and support (e.g. L70 carries all three window statements on one line as the entry says).

Machine cross-checks that back the verdicts: every map value's basename id equals the key's id and
carries the anchor through unchanged (203/203 consistent); all 15 repointed rounds match the
SOURCES.md anchor-cell rounds (round-40 ×5 for the pre-convention rows, whose pin digests I
recomputed against the round-40 files and manifest: 5/5 match — so same S-id, same capture); file
sha256 == manifest digest for all five round-40 pins.

## excluded.json — exclusion right in rule, conservative in fact; 2 routed candidates

`build-map.py` computes basename uniqueness over **all** tracked files at the rev (`git ls-tree -r`),
so `.ufo/waves/**` receipt/fixture copies collide with the real snapshots: at freeze S029 has 41
tracked same-basename files (1 under corpus/source-snapshots/round-23 + 40 wave copies), S040 33/1,
S041 23/3 (three *distinct* captures: rounds 26, 28, 30), S069 3/1 (round-44), S100 3/1 (round-67),
S102 2/1 (round-68). 89 tokens excluded, count confirmed.

- **Exclusion was right as executed** (mechanical, context-free, and the frozen claim's own wording
  "basename is not unique" matches the implementation); no frozen-map change is proposed.
- **Routed candidate 1 (later round, not C1):** S029/S040/S069/S100/S102 tokens are unambiguous from
  context — exactly one real snapshot each under corpus/source-snapshots/, held by the used-by file
  that cites them (cra-manufacturer-reporting-duties.md → S029 round-23;
  vendor-disclosure-policy-commitments-crosswalk.md → S040 round-25;
  google-cloud-vrp-customer-resource-boundary.md → S069 round-44;
  first-psirt-maturity-document.md → S100 round-67; openssf-scorecard-api-contract.md → S102
  round-68); the colliding paths are .ufo fixture copies of the same captures. A future round can
  either scope the uniqueness limb to corpus/source-snapshots/ (as the claim sentence's alternative
  parse reads) or adjudicate these ~86 tokens with the same M5 anchor-range check.
- **Routed candidate 2:** S041 exclusion is genuinely right — three distinct tracked captures
  (round-26/28/30; the corpus already cites round-26 in iso-29147-and-30111-division-of-labour.md:23
  and round-30 in japanese-severity-vocabulary-and-impact-model.md:5), and the deep anchors
  (:1680-1681 … :1996-2079) can differ per capture; repointing needs per-token anchor checks against
  each candidate, not a blanket map.

## Residual risk / verification gaps

- I verified ~54 anchored lines by content, not all 203 keys' anchors; the frozen meter's M5 limb is
  the exhaustive in-range check and other seats re-run it.
- The four Finding-1 keys still pass every frozen limb (M1-M6), so P1 does not catch them; the
  defect is semantic only (false attribution inside a verification-bearing "Scope and limits" line).
- No C2 files touched by this review.

**CHANGES-REQUESTED** — Finding 1: exclude the four manifest-field-quotation keys (`S020.txt`,
`S021.txt`, `S023.txt`, `S025.txt` in doj/cisa-bod/cisa-cvd/cve-bench) from the map (or route them
with the round-85 distinct-wording lesson); with that single map delta the remaining 199 repoints
are semantically correct on every sampled line.
