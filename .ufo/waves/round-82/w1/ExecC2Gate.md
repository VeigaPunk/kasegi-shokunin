# ExecC2Gate — round-82 attempt 1, C2 gate predicates (B0, B4–B8)

Seat: `ExecC2Gate` (leaf). Wave: round-82 attempt 1, one v1 wave of 12 seats. Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch:
`/fast/scratch/hyaku/kasegi-r82/ExecC2Gate` (deleted on exit; all gate/counter output written
under the wave dir, never `/tmp`).

Frozen inputs exercised (read-only; no lane file edited):

| input | digest / identity |
|---|---|
| `corpus/knowledge/osv-high-quality-record-import-bar.md` (uncommitted worktree draft) | 1100997162fdd64b4282cd9b2afbe00f6549981733010e56cf6f39d2b1a30cac |
| `corpus/source-snapshots/round-82/manifest.json` | S116, 6 quotes, anchors 25/36/41/44/47/51 |
| `corpus/source-snapshots/round-82/S116.txt` | sha256 `2198d329bf6a8711ac28ae9221351162d61679699c0b45acb8ebb95cadce9ca0`, 87 lines, 6586 bytes |
| `.ufo/waves/round-82/c2/entry-gate.py` (B8, G1–G4 + new G5) | 10330 bytes, mtime 18:01 |
| `.ufo/waves/round-81/c2/entry-gate.py` (predecessor) | 7237 bytes |

**Verdict: the draft entry passes every C2 gate predicate (B0, B4, B5, B6, B7, B8 rc 0). One
routed defect: a Limits bullet carries a receipt that does not reproduce (D1 below). The
candidate fix is in the wave dir and still passes B8.**

## 1. B0 — recheck of S116 against the frozen manifest

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-82/manifest.json --source S116
S116:sha256 OK
S116:Q01-purpose OK occurrences=1 anchor=25-ok
S116:Q02-valid-prerequisite OK occurrences=1 anchor=36-ok
S116:Q03-package-level-minimum OK occurrences=1 anchor=41-ok
S116:Q04-distinct-ranges OK occurrences=1 anchor=44-ok
S116:Q05-git-commits-in-repo OK occurrences=1 anchor=47-ok
S116:Q06-reference-urls OK occurrences=1 anchor=51-ok
RC=0
```

Receipt: `ExecC2Gate-receipts/B0-source-recheck.txt`.

## 2. B5 — the entry's `recheck:` value runs from a foreign cwd

Value extracted from entry line 5; run with `bash -c` from
`/fast/scratch/hyaku/kasegi-r82/ExecC2Gate/foreign-cwd` (not the lane, not the fleet root):

```
VALUE=cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-82/manifest.json --source S116
B0CMD=cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-82/manifest.json --source S116
EQUAL=yes (byte-identical to the B0 command)
S116:sha256 OK
S116:Q01-purpose OK occurrences=1 anchor=25-ok
... (six pin lines, identical to B0)
RC=0
```

The value is byte-identical to the B0 command behind `cd <lane> && `; the cwd-independent
`cd` prefix is what makes it reproduce. Receipt: `ExecC2Gate-receipts/B5-recheck-foreign-cwd.txt`.

## 3. B6 — literal sweep of the six manifest quotes over the other knowledge entries

95 files swept (`corpus/knowledge/*.md` minus the draft entry), literal substring, both
case-sensitive and case-insensitive:

| quote | files (cs) | files (ci) |
|---|---|---|
| Q01-purpose | 0 | 0 |
| Q02-valid-prerequisite | 0 | 0 |
| Q03-package-level-minimum | 0 | 0 |
| Q04-distinct-ranges | 0 | 0 |
| Q05-git-commits-in-repo | 0 | 0 |
| Q06-reference-urls | 0 | 0 |

`all_zero=True`. This reproduces the entry's Distinctness sweep claim. Receipt:
`ExecC2Gate-receipts/B6-quote-sweep.txt`; the same result was obtained independently with the
`grep` tool (six "No matches found" calls).

## 4. B4 — capture binding

```
$ python3 corpus/instruments/capture-binding-check.py | tail -2
records=96 bound=96 unbound=0
RC=0
```
(Full first line: `AUDIT records=96 with_url=96 with_fetched_utc=58 with_archival=38
snapshot_dirs=55 manifest_dirs=55 missing_manifest=0 multi_row_url=7 digest_unpinned=0
orphans=1 orphan=S040-live.txt`.) Receipt: `ExecC2Gate-receipts/B4-capture-binding-check.txt`.

## 5. B7 — sources census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi | tail
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
kasegi	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
kasegi	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
RC=0
```

W04 warnings are pre-existing duplicate-URL notices across scopes, not errors; the final
`ok` line and rc 0 are the validator's verdict. Receipt:
`ExecC2Gate-receipts/B7-sources-census.txt`.

## 6. B8 — the r82 gate, its selftest and its controls

```
# selftest
entry-gate selftest ok got={'good': True, 'dump': False, 'moved': False, 'norule': False,
 'labelled': False, 'copied': False, 'snapline': False, 'nocite': False, 'shortrej': False}
RC=0

# draft entry, r82 manifest, S116
ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
ENTRY-GATE-RESULT pass
RC=0

# junk-labelled.md (r81 CriticClaims fixture) under the r82 gate, r81 manifest, S115
ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=6 header=ok
ENTRY-GATE-RESULT fail
RC=1

# same fixture under the r81 gate (predecessor)
ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok
ENTRY-GATE-RESULT pass
RC=0
```

The G5 limb is the only behavioural delta between the gates (`diff -u` shows the docstring,
`MIN_WORDS`, `label_text`, `drawn_from_source`, `content_ok` and the `ruleless` counter added;
nothing removed). The labelled six-quote dump flips pass→fail exactly as the round-81
CriticClaims (d) / MutEntryGate finding requires, and the selftest's `labelled`, `copied`,
`snapline`, `nocite`, `shortrej` cases pin each G5 sub-check. Receipt:
`ExecC2Gate-receipts/B8-entry-gate.txt`.

## 7. Calibration — r82 gate over every admitted entry with a matching round manifest

Mapping: entry `source: S###` header → every `corpus/source-snapshots/round-*/manifest.json`
holding that sid (55 manifests, 93 sids); where a sid appears in several manifests the one
named in the entry's own text was used (S041 → round-26/round-28 per entry; S112 → round-78).
70 of 96 knowledge files carry a sid with a manifest; the other 26 are lane-process entries
with no `source:` header.

| entry | sid | result |
|---|---|---|
| ai-assisted-finding-validation.md | S009 | fail |
| aisi-autonomous-cyber-capability-progress-rate.md | S091 | fail |
| anthropic-cvd-provenance-and-pacing.md | S016 | fail |
| authorised-testing-rules-of-engagement.md | S032 | fail |
| authorization-safe-harbor-and-scope.md | S006 | fail |
| bugzilla-rest-api-bug-endpoints.md | S107 | fail |
| cert-guide-cvd-phases-and-validation.md | S095 | fail |
| chinese-crowdsourced-testing-scope-and-rewards.md | S049 | fail |
| cisa-bod-20-01-vdp-minimums.md | S021 | fail |
| cisa-cvd-program-stages.md | S023 | fail |
| cisa-kev-catalog.md | S052 | fail |
| cisa-vulnrichment-adp-enrichment.md | S081 | fail |
| cisa-vulnrichment-record-list.md | S088 | fail |
| cisa-when-to-issue-vex.md | S057 | fail |
| claim-package-gate.md | S067 | fail |
| cna-assignment-and-vulnerability-rules.md | S031 | fail |
| coordinated-disclosure-timelines.md | S003 | fail |
| cra-manufacturer-reporting-duties.md | S029 | fail |
| csaf-vex-product-status-and-justifications.md | S055 | fail |
| cve-bench-agent-exploitation-benchmark.md | S025 | fail |
| cve-json-record-format.md | S064 | fail |
| cve-services-publication-api.md | S078 | fail |
| cvss-v4-severity-and-vector.md | S001 | fail |
| cwe-top25-2025-methodology.md | S013 | fail |
| cyclonedx-analysis-subtree.md | S060 | fail |
| doj-vdp-framework-scope-and-authorization.md | S020 | fail |
| epss-exploit-prediction-scoring.md | S053 | fail |
| first-psirt-maturity-document.md | S100 | fail |
| first-psirt-services-framework.md | S098 | fail |
| fuzzilli-js-engine-fuzzing-framework.md | S109 | fail |
| fuzzilli-ndss2023-jit-fuzzing-paper.md | S110 | fail |
| github-advisory-database-curation-semantics.md | S105 | fail |
| github-global-security-advisories-rest-api.md | S103 | fail |
| github-private-vulnerability-reporting.md | S073 | fail |
| github-repository-security-advisories-rest-api.md | S087 | fail |
| github-repository-security-advisories.md | S076 | fail |
| google-big-sleep-findings-tracker.md | S092 | fail |
| google-cloud-vrp-customer-resource-boundary.md | S069 | fail |
| immunefi-vscs-v2-2-smart-contract-severity.md | S051 | fail |
| iso-29147-30111-standard-records.md | S089 | fail |
| iso-29147-and-30111-division-of-labour.md | S041 | fail |
| iso-29147-divergence-and-clause-crosswalk.md | S041 | fail |
| japanese-domestic-disclosure-workflow.md | S041 | fail |
| japanese-severity-vocabulary-and-impact-model.md | S046 | fail |
| linux-kernel-security-bugs-reporting-process.md | S071 | fail |
| multiparty-vulnerability-coordination.md | S018 | fail |
| nist-sp800-216-vdp-framework.md | S019 | fail |
| nvd-api-2.0-response-schema.md | S085 | fail |
| nvd-api-2.0-retrieval-interface.md | S083 | fail |
| openssf-scorecard-api-contract.md | S102 | fail |
| openssf-scorecard-checks.md | S086 | fail |
| osv-affected-range-events.md | S080 | fail |
| osv-determineversion-cc-library-versioning.md | S113 | pass |
| osv-high-quality-record-import-bar.md | S116 | pass |
| osv-importfindings-record-quality-feedback.md | S115 | pass |
| osv-post-batch-query-contract.md | S112 | fail |
| osv-post-v1-query-contract.md | S108 | fail |
| osv-ubuntu-binary-to-source-mapping.md | S114 | pass |
| program-severity-ladders-and-reward-scales.md | S043 | fail |
| project-zero-big-sleep-sqlite-variant-analysis.md | S094 | fail |
| project-zero-fuzzilli-vs-bigsleep-comparison.md | S093 | fail |
| pz-reporting-transparency-trial.md | S017 | fail |
| rfc-9116-security-txt.md | S063 | fail |
| ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | fail |
| statutory-authorization-and-unauthorized-access.md | S033 | fail |
| vendor-disclosure-policies-as-corpus-objects.md | S036 | fail |
| vendor-disclosure-policy-commitments-crosswalk.md | S040 | fail |
| vendor-third-party-finding-coordination.md | S048 | fail |
| zdi-disclosure-policy.md | S075 | fail |
| zdi-disclosure-process-and-vendor-coordination.md | S106 | fail |

**TOTAL=70 PASS=4 FAIL=66.** The four passes are exactly the four entries written in the
current format: S113 (round-79), S114 (round-80), S115 (round-81), S116 (round-82, this draft).

Failure-cause distribution over the gate's own fields: `header=bad` 53/66; `claims != want`
65/66; `claimless`/`unpinned`/`ruleless` co-occur with the claim-count mismatch. The single
failure with `claims == want` is `ssvc-stakeholder-specific-vulnerability-categorization.md`
(S054, claims=4 want=4, spans=0, claimless=4, header=bad).

**Calibration caveat (bound on what "pass" means here).** This gate encodes the round-79+
entry format; the 66 failures are format-era mismatches, not quality regressions. Two
concrete limits visible in the data:
- G3 requires `len(claims) == len(quotes)`. `osv-post-batch-query-contract.md` (S112) fails
  only that: `claims=5 want=7 spans=10 ... unpinned=0 ruleless=0 header=ok` — all seven quotes
  are pinned inside claim sections, but two quotes share a claim. Same shape in
  `osv-post-v1-query-contract.md` (S108, claims=6 want=31, unpinned=10). A grouped-quote entry
  is rejected by the equality even when every quote is pinned.
- G1 requires the `recheck:` line byte-identical to
  `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest <manifest-rel-to-lane>
  --source <SID>`; 53 entries predate that form.

Full per-entry gate lines (all fields, rc) are in
`ExecC2Gate-receipts/B7x-calibration.txt`.

## 8. Routed defect D1 — the draft entry's Limits receipt does not reproduce

Entry line 92 (`## Limits`, first bullet) states:

> `grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt` prints
> nothing and exits 1.

Against the pinned capture (the same bytes B0 verifies, sha256 `2198d329…`):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt
7:GET /v1experimental/importfindings
RC=0
```

The snapshot carries `GET /v1experimental/importfindings` in the page's navigation block
(S116.txt:7), so the command prints one line and exits 0. The bullet's *substantive* limit
(the page states no enforcement rule and names no import finding) still holds — line 7 is a
nav link, not a statement — but the receipt as written is false, and a reader who runs it gets
the opposite result. B8 does not catch this: G5 reads only Claim-section rule/rejection text,
never `## Limits`.

Minimal fix (candidate bytes in the wave dir, one line changed, nothing else):
`.ufo/waves/round-82/w1/ExecC2Gate-candidate-osv-high-quality-record-import-bar.md`

```
- how OSV.dev enforces each property or which import finding a failure produces: the capture
  carries the word only in the navigation link `GET /v1experimental/importfindings`
  (S116.txt:7) and states no enforcement rule; `grep -n -i -E 'IMPORT_FINDING|finding'
  corpus/source-snapshots/round-82/S116.txt` prints that one navigation line and exits 0.
```

`diff -u` against the draft shows this is the only changed line; the r82 gate over the
candidate still prints `ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0
claimless=0 unpinned=0 ruleless=0 header=ok` / `pass` / rc 0. Receipt:
`ExecC2Gate-receipts/B8x-candidate.txt`. The L1 integrates; this seat did not touch `corpus/`.

## 9. Other verifiability checks on the draft entry (all reproduce)

| entry claim | check | result |
|---|---|---|
| sha256, 87 lines, 6586 bytes | `sha256sum` / `wc -c -l` on S116.txt | match |
| served page 24473 raw bytes | manifest `fetch_method` | match |
| word counts 12/23/6/10/19/13 | `len(quote.split())` over the six manifest quotes | match |
| six anchors 25/36/41/44/47/51 | S116.txt lines read | match, each quote verbatim on its line |
| `S116.txt:21` heading, `:22-23` version, `:27` out-of-scope, `:28` deferred, `:64` Gemini, `:86` exclusivity | S116.txt lines read | match |
| "third bullet" (:44), "sixth bullet" (:47), "last bullet" (:51) | bullet ordinal count under Precise (42,43,44,45,46,47,48,49,50,51) | match |
| F57 link text at `S115.txt:14` | S115.txt line 14 | match ("Properties of a High Quality OSV Record") |
| F31 exclusivity `S080.txt:760-761`, fixed-over-last_affected `S080.txt:762-766` | S080.txt lines read | match |
| recheck receipt in `controls/c2-prefreeze-r82.txt` | file read | match (same six pin lines, rc=0, plus the same B6 zeros and B8 pass) |

## 10. Coverage note (C2, F58 on S116)

The page's Precise section lists ten bullets (S116.txt:42–51). The entry claims three of them
(:44 distinct range ends, :47 GIT commits in the named repo, :51 reference URLs at publication)
plus the package-level-minimum paragraph (:41), the purpose (:25) and the schema-validation
prerequisite (:36). Seven Precise bullets are explicitly unclaimed (:42, :43, :45, :46, :48,
:49, :50); :43 is held by F31, the other six have no other corpus holder named in the entry
(`grep -rn "canonically\|introduced is defined\|versions exist in the" corpus/knowledge` returns
only this entry's own Not-claimed line; purl coverage exists only in `cve-json-record-format.md`
and `osv-post-v1-query-contract.md` for different pages). The entry states the limit and the
scope sentence, so this is a declared v1 boundary rather than a silent gap — but a successor
entry on :42/:45/:46/:48–:50 (introduced defined, ordering, ecosystem existence, canonical
name, purl conformance) is the uncovered remainder of this page.

## 11. Gate residuals observed (no action taken; evidence only)

- G5 checks that the rule text exists, is the entry's own words and cites `S<sid>.txt:<n>`; it
  does not check that the cited line supports the rule, nor that the rule follows from the
  quote. The docstring says so; the S116 draft's citations happen to be accurate (section 9).
- `drawn_from_source` is a substring test: a rule that is a near copy of a snapshot line with
  one word changed passes. Not exercised here (the item's controls are the named ones).
- G5 is scoped to `## Claim` sections; `## Limits`, `## Distinctness` and `## Gate` receipts are
  unchecked — which is why D1 passes B8.

## 12. Files written

- `.ufo/waves/round-82/w1/ExecC2Gate.md` (this report)
- `.ufo/waves/round-82/w1/ExecC2Gate-candidate-osv-high-quality-record-import-bar.md` (D1 fix, candidate bytes for L1 integration)
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B0-source-recheck.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B4-capture-binding-check.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B5-recheck-foreign-cwd.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B6-quote-sweep.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B7-sources-census.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B7x-calibration.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B8-entry-gate.txt`
- `.ufo/waves/round-82/w1/ExecC2Gate-receipts/B8x-candidate.txt`

No lane file outside the wave dir was modified; no git/jj write was issued; no tool was
installed. Scratch `/fast/scratch/hyaku/kasegi-r82/ExecC2Gate` removed before yield.
