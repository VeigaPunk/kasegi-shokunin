# ScribeF46 — round 68 w1, C2 corpus landing (F46 / S102)

**Verdict: LANDED — C2 frozen after-counts all met in this seat (uncommitted working tree), with FINDINGS F1–F4 below.**

Nothing was committed, staged or pushed. The only lane files I wrote are the four this seat names, plus this report and
its receipts under `.ufo/waves/round-68/w1/ScribeF46/`. Scratch was `/fast/scratch/hyaku/kasegi-r68/ScribeF46/`
(TMPDIR and HYAKU_SCRATCH pointed there). I removed it before yielding. I installed no tools.

## Files written (sha256 after; receipt `ScribeF46/sha256-after.txt`, diff `ScribeF46/lane-diff.txt`)

| file | change | sha256 after |
|---|---|---|
| `corpus/knowledge/openssf-scorecard-api-contract.md` | new, 173 lines | `36b5e242…046b83c` |
| `corpus/README.md` | appended only: `## Round-68 admission — Frontier F46` section (2 header lines, 1 source-basis sentence, table header, F46 row); 10 lines added, none changed | `d101ab54…0dfb04b6` |
| `corpus/SOURCES.md` | +1 registry row S102 after S101 (NF=13, 11 columns); −2 lines in `## Leads (unopened)` | `8336a2e5…10174fb5` |
| `corpus/instruments/knowledge-expected.txt` | +1 entry path in sorted position; 1 pre-existing out-of-order line moved (F2) | `160fb0f3…2b50addf7` |

### Entry shape
I followed `cve-services-publication-api.md` (F30) and `first-psirt-services-framework.md` (F44). The header has `source:` / `verified-at:` / `recheck:` / `ground:`. The body has these parts:
- a scope and decision rule with five numbered, line-anchored facts;
- a result-object table;
- a G1–G8 ground table;
- "What the document does NOT say", with measured zeros;
- overlap with F35/S086 and F30;
- a `## Gate — S102` block giving the URL, my access date and 13 located quotes;
- Limits, including the recorded refusal of the served-instance candidate.

The frozen claim's coverage minimum is fully covered: info.version 1.1.0 (L15); host api.scorecard.dev (L17); the GET on `/projects/{platform}/{org}/{repo}` (L19, L24) with its `commit` query parameter (L30–32) and 40-hex pattern (L28); the `publish` body parameter (L97) with `VerifiedScorecardResult` (L101, L387–403); `/version` (L234–244); ScorecardResult date/repo/scorecard/score "Aggregate score of the repository"/checks (L336–361, plus `metadata` L365); Repo name/commit (L281–292); ScorecardCheck name/score/reason/documentation.url+short/details (L297–330); and Error code/message (L268–276).

### Refused and recorded (things the capture does not support)
- Score range, weighting and check meaning: `minimum` 0, `maximum` 0, `weight` 0.
- Check-name enumeration: the only `"enum"` in the document is the badge style.
- An auth scheme: `securityDefinitions` 0 and `security` 0; "OIDC" appears once, at L93.
- A date format: `"format"` 0.
- Meanings for metadata, details, branch and result.
- An error-code catalogue.
- Whether api.scorecard.dev and api.securityscorecards.dev serve the same data.
- Any served instance value: the round's `/projects/github.com/ossf/scorecard` refusal is restated in Limits.

## Gate: my re-open (receipt `ScribeF46/reopen.txt`)
```
$ date -u; curl -sS -D hdr.txt -o swagger.json -w 'http=%{http_code} size=%{size_download} final=%{url_effective}\n' https://api.securityscorecards.dev/swagger.json; date -u
2026-11-04T21:53:23Z
http=200 size=11802 final=https://api.securityscorecards.dev/swagger.json
2026-11-04T21:53:23Z
d526f3274a6dbcb1ba6632bf3ee1e9a642dc2106b18a1354cc0c8a26104c8af4  swagger.json      (raw, 428 lines, 11802 bytes)
content-type: application/json / date: Wed, 04 Nov 2026 21:53:23 GMT / x-cache: HIT, HIT / age: 37
$ sed -E 's/^[[:space:]]+//; s/[[:space:]]+$//; s/[[:space:]]+/ /g' swagger.json | grep -v '^$' > norm.txt
429 norm.txt
6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0  norm.txt
diff -q norm.txt corpus/source-snapshots/round-68/S102.txt  -> identical (exit 0)
```
The capture reproduces exactly: same snapshot digest, same 429 lines. Access date: **2026-11-04**.

I checked all 13 Gate quotes at their stated line and across the whole capture. Each one is present exactly once at its own line, and each stated word count matches `wc -w`. Quote → line, word count:

| quote | line | words |
|---|---|---|
| API to interact with a project's published Scorecard result | L13 | 9 |
| OpenSSF Scorecard API | L14 | 3 |
| Get a repository's ScorecardResult | L24 | 4 |
| SHA1 commit hash expressed in hexadecimal format | L30 | 7 |
| A JSON object of the repository's ScorecardResult | L37 | 7 |
| Publish a repository's OIDC verified ScorecardResult | L93 | 6 |
| Successfully updated ScorecardResult | L107 | 3 |
| Reports the scorecard-infra release and commit this server was built from, and the workflow parser that verifies uploads. | L236 | 18 |
| Get the build this server is running | L240 | 7 |
| respository that was analyzed | L285 | 4 |
| SHA1 value of the analyzed commit expressed as hexadecimal | L290 | 9 |
| Aggregate score of the repository | L353 | 5 |
| Scorecard version used for this analysis | L375 | 6 |

I also checked every inline `"…" (S102.txt:N)` anchor in the body against its line. All matched, with one exception: three matched only after collapsing whitespace, because the Markdown line-wrap splits the quote. Those three are L93, L107 and L236.

## Verification (every line from this seat; receipts in `ScribeF46/`)

`frontier-recheck-count.txt`:
```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0 registry=102
FRONTIER-PASS F46 ids=S102
PASS     F46  knowledge/openssf-scorecard-api-contract.md          ids=S102           exit=0
entries=49 pass=49 exit=0
exit=0
```
(The other 45 FRONTIER-PASS rows and the 48 other PASS rows are in the receipt. There is no FAIL line.)

`capture-binding-check.txt`:
```
MANIFEST round-68 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=82 with_url=82 with_fetched_utc=44 with_archival=38 snapshot_dirs=41 manifest_dirs=41 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=82 bound=82 unbound=0
exit=0
```

`sources-census-validate.txt`:
```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
kasegi	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
kasegi	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```
(All six W04 warnings are on pre-existing rows. None names S102.)

`knowledge-expected.txt`, final state:
```
$ wc -l .../corpus/instruments/knowledge-expected.txt      -> 86
$ grep -vc '^#' .../knowledge-expected.txt                  -> 84
$ env LC_ALL=C sort -c .../knowledge-expected.txt           -> (silent) exit=0
```

`source-recheck-S102.txt`:
```
$ python3 .../corpus/instruments/source-recheck.py --manifest .../corpus/source-snapshots/round-68/manifest.json --source S102
S102:sha256 OK
S102:Q01-description OK occurrences=1 anchor=13-ok
S102:Q02-title OK occurrences=1 anchor=14-ok
S102:Q04-operation OK occurrences=1 anchor=24-ok
S102:Q05-commit-parameter OK occurrences=1 anchor=30-ok
S102:Q06-200-schema OK occurrences=1 anchor=37-ok
S102:Q07-repo-name OK occurrences=1 anchor=285-ok
S102:Q08-repo-commit OK occurrences=1 anchor=290-ok
S102:Q09-aggregate-score OK occurrences=1 anchor=353-ok
exit=0
```

Compared with the frozen C2 after-target (rows=46 registry=102 entries=49 capture=82 knowledge=84 (86 lines) census exit=0), every value matches.

## SOURCES.md changes, old → new
- Registry: 101 → 102 rows (`grep -c '^| S[0-9]'` = 102). The new row is S102: kind `docs`, tier `A`, status `mined`, opened `2026-11-04`, recheck `2027-05-03`, used-by `corpus/knowledge/openssf-scorecard-api-contract.md`.
  - The recheck is an ISO date, as the seat spec asks. It equals opened + 180 days, the lane's tier-A docs cadence.
  - The source cell holds exactly one `https://` token, equal to the manifest `url`, so capture-binding B4/B5 hold.
  - The evidence cell holds the capture path, sha256, line count and the located quote "Aggregate score of the repository" (L353, 5 words).
  - No cell contains a literal `|` (NF=13).
  - No existing row changed.
- Leads (unopened), old:
  ```
  - Fuzzilli project's primary documentation at https://github.com/googleprojectzero/fuzzilli — unopened; defer unless its tool-technique ground clears PROVINCE and sibling ownership.

  - OpenSSF Scorecard aggregate-score/API documentation — unopened portion only; S086 already holds the check documentation, not a general scorecard.dev API contract.
  ```
  new: the Fuzzilli line only. I removed the OpenSSF lead line and its preceding blank line (old L163–164).

## Findings / residuals
- **F1, Registry-changes bullet not written.** Every earlier admission appended an audit bullet under `## Registry changes` (for example the round-67 S100/S101 lines). The seat spec names only the row and the Leads edit, so I did not add one. If the lane wants a round-68 history bullet (S102 added; the OpenSSF lead retired as opened), the L1 integrator should decide and write it.
- **F2, the base list was not sort-clean; I moved one line.** At base `d0f48405` and at HEAD, `LC_ALL=C sort -c` on knowledge-expected.txt failed with `disorder: corpus/knowledge/first-psirt-maturity-document.md` (line 85). Round 67 had appended F45 at the end. To meet the spec's "must stay sort-clean", I moved that line to its sorted spot before `first-psirt-services-framework.md`.
  - old: line 85 at EOF; new: line 36.
  - The file is still 86 lines / 84 entries, and `sort -c` now exits 0.
  - The L1 should accept or revert this move. It changes the order only, not the set.
- **F3, recheck-audit.py exits 1, and it did at base too (not in the C2 predicate).** I ran `recheck-audit.py --root <lane>` after the edit. It printed `expect=present expected=84 missing=0 unexpected=0` and listed the new entry as `PASS`. It exits 1 on nine pre-existing `cwd_fail` entries: cisa-vulnrichment ×2, github-…-rest-api, nvd-api ×2, openssf-scorecard-checks, osv-affected-range-events and project-zero ×2.
  - The same nine FAIL at a `git archive d0f48405` export: `lines=83 … cwd_fail=9 … exit=1`, receipt `ScribeF46/recheck-audit-base.txt`.
  - So this is a pre-existing residual. This round did not introduce it.
- **F4, manifest quote ids skip Q03.** The manifest pins 8 quotes with ids Q01, Q02 and Q04–Q09. My entry's recheck comment names them that way. Five Gate quotes (L93, L107, L236, L240, L375) are not manifest-pinned. I verified them with `grep -F` at their lines in this seat; `source-recheck` does not cover them. I did not touch the manifest because it is not one of my files.
- **Out of scope / untouched:**
  - The working-tree modifications to `corpus/knowledge/first-psirt-maturity-document.md` and `.ufo/waves/round-67/controls/driver-pins.json`.
  - The untracked `corpus/lessons/round-68.md`.
  - These belong to another writer, and I did not read them as my own.
  - C1 is not this seat's work.
