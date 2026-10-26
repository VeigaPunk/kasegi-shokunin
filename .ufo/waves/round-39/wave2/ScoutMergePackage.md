# ScoutMergePackage receipt — round 39 wave 2 (falsify), leaf scout

Deliverable (byte-exact beside this receipt): `.ufo/waves/round-39/wave2/ScoutMergePackage.package.md` (full evidence).

Lane HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37`; claims-freeze `dcd3170`; base `480b1a5`. Probe 2026-10-26T20:14Z. I did not author any
C1/C2 deliverable; read-only probe of `/home/vgpnk/Projects/shokuknow/merge/kasegi/`. No tool installed, no network fetch, no git mutation,
no writes outside this dir and scratch `/fast/scratch/hyaku/kasegi-r39/ScoutMergePackage` (removed).

## Findings (all measured this session)

1. Package byte-identical to r35–r38: 70 files, all mtime `2026-10-24 23:33:20`, 0 newer than `claims.json`; `SOURCES.append.md`
   sha256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` (100 lines / 89718 B); `MERGE-REPORT.md` `0e6759b4…`,
   `MERGE-REPORT.json` `8a42a910…` (equal to r38 values).
2. Competing ground: grep over all 70 files for `when-issue`, `when to issue`, `VEX`, `reaffirm`, `inheritance`, `issuance`, `cisa.gov`,
   `csaf`, `openvex`, `cyclonedx`, `not_affected`, `ssvc`, `sbom`, `downstream`, `upstream` → 0 files each. Substring hits (`inherit` 2,
   `lifecycle` 2, `timestamp` 2, `supplier` 1, `affected` 4, `advisory` 10 files) all read in context: JP/CN disclosure, Cisco policy
   lifecycle, GB-standard inheritance, HackerOne policy timestamp — none VEX/issuance. **Staged entry competing with F22: none.**
3. Document collision with S057: **none.** Staged S055–S059 = Cybozu policy, Cybozu bounty FAQ, Pepabo (staged S057), IPA uketsuke, CNVD
   weekly; lane S055–S059 = CSAF, CISA Min Req, **CISA When to Issue (S057)**, OpenVEX, CycloneDX. Collision is by id only; 0 staged URLs
   match cisa.gov/openvex/cyclonedx/oasis. Hazard (not a defect): 4 staged entries carry `source: S055..S059` lines meaning other documents.
4. Id intersection (0–3-space extractor): registry **59** (S001–S059, sha `b698a246…`), staged **94** (S031–S124, sha `550a0129…`, byte-equal to
   r31/r34/r38/r39 wave 1), collisions **29** (S031–S059, sha `5b959cc5…`) = wave-1's 25 at registry 55 + the four new rows S056–S059.
   No 4+-space-indented rows in either file. Document-level duplicates 21 (same as r38), 0 onto S055–S059; same-id-same-doc 1 (S042).
5. No staged `ground: F22`; staged grounds F20/F21/F24 collide with or lie outside lane F-ids (pre-existing re-grounding requirement).
6. Landed-count cross-check at HEAD: registry claim-form 59 (E1), frontier rows 22, knowledge 51, `source: S057` entries 1.
7. Non-falsifying observation: `claims.json` `frozen_at_utc` `20:30Z` is later than the freeze commit (`dcd3170` = 19:26:41Z); nominal.

## Verdict

C2 coverage claim not falsified by the package probe; assimilation expectation "none adopted" holds (nothing staged competes with or
duplicates F22/S057). C1 not touched by this seat.
