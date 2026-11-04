# ScoutS102 — round-68 C2 source re-open (S102)

**Verdict: AGREE.** The served swagger.json today normalizes byte-for-byte to the committed `S102.txt`. There is no drift. All 8 pinned quotes sit on their anchor lines, once each. The longest quote is 9 words, so it is well under the 25-word cap. The decision to refuse the live project result as an entry source is supported. The API root serves only a Swagger UI JS shell.

Scratch: `/fast/scratch/hyaku/kasegi-r68/ScoutS102/` (TMPDIR and cwd point at it). Raw receipts are copied beside this report under `w1/ScoutS102/`: `S102.txt`, `swagger.raw`, `project.raw`, `root.raw`. No tools were installed. I made no lane writes except this report and its receipts.

## (1) Independent re-capture
```
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S102 --url https://api.securityscorecards.dev/swagger.json --out /fast/scratch/hyaku/kasegi-r68/ScoutS102/S102.txt --kind text
-> S102 status=200 fetched_bytes=11802 snapshot_bytes=7595 sha256=6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0 utc=2026-11-04T21:52:46Z  (exit 0)

curl -sS -L -o .../swagger.raw -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' https://api.securityscorecards.dev/swagger.json
-> 200 11802 application/json https://api.securityscorecards.dev/swagger.json
```
- Committed `S102.txt` has sha256 `6ebb8552…c2caa0`, 7595 bytes and 429 lines. My snapshot has the same sha256, 7595 bytes and 429 lines, and the comparison returned `identical True`.
- The raw served bytes (11802) have sha256 `d526f3274a6dbcb1ba6632bf3ee1e9a642dc2106b18a1354cc0c8a26104c8af4`.
- No lines drifted.
- I parsed the served document to check the manifest note. It reports `swagger 2.0`, `info.version 1.1.0` and `host api.scorecard.dev`.
  - paths: `/projects/{platform}/{org}/{repo}`, `/projects/{platform}/{org}/{repo}/badge`, `/version`
  - definitions: `Error, Repo, ScorecardCheck, ScorecardResult, ScorecardVersion, VerifiedScorecardResult, VersionInfo`

  This matches the note.
- Manifest `bytes: 11802` is the fetched byte count, not the snapshot size (7595). That follows the lane's existing convention. In earlier manifests:
  - S098: field 229255, file 170137
  - S100: field 82978, file 59068
  - S101: field 644190, file 58889

  This is not a defect.

## (2) Pinned quotes (checked against the committed capture)
Method: for each quote, check that it is a substring of the anchor line, count occurrences in the whole file, list every line that contains it, and count words with whitespace split.

| id | anchor | on anchor | lines containing | occurrences | words |
|---|---|---|---|---|---|
| Q01-description | 13 | True | [13] | 1 | 9 |
| Q02-title | 14 | True | [14] | 1 | 3 |
| Q04-operation | 24 | True | [24] | 1 | 4 |
| Q05-commit-parameter | 30 | True | [30] | 1 | 7 |
| Q06-200-schema | 37 | True | [37] | 1 | 7 |
| Q07-repo-name | 285 | True | [285] | 1 | 4 |
| Q08-repo-commit | 290 | True | [290] | 1 | 9 |
| Q09-aggregate-score | 353 | True | [353] | 1 | 5 |

The maximum is **9 words**, against a cap of 25. Two notes:
- Q07 reproduces the source's own typo, "respository". It is faithful to the served text.
- The quote ids skip Q03. That is cosmetic only: there are 8 quotes, matching the frozen "8 pinned quotes".

## (3) Refused candidate: the live project result
```
curl ... https://api.securityscorecards.dev/projects/github.com/ossf/scorecard
-> 200 13259 application/json
```
- The response has 13259 bytes and a single `\n`, so it is one line. Both facts match the manifest note ("one 13259-byte line").
- Top-level keys are `date, repo, scorecard, score, checks`. Their values:
  - `date`: `2026-11-03T06:28:58Z`
  - `repo`: `{name: github.com/ossf/scorecard, commit: ab792da5…}`
  - `scorecard`: `{version: v5.6.0, commit: 61e84743…}`
  - `score`: `8.8`
  - `checks`: a list of 18 entries
- Every value is instance data and changes with each analysis run.
- Because the response is a single line, no quote could carry a meaningful line anchor.

Refusing it as an entry source was right. The contract document (S102) is the stable, line-anchorable ground. The live result is a moving instance of that contract.

## (4) API root
```
curl ... https://api.securityscorecards.dev/  -> 200 741 text/html
```
- The body is the static Swagger UI distribution shell: `<div id="swagger-ui">` plus `swagger-ui-bundle.js`, `swagger-ui-standalone-preset.js` and `swagger-initializer.js`.
- It contains no contract text.

So the JSON contract at `/swagger.json` is the correct capturable ground, not the shell.

## Residuals and disagreements
- None against C2's capture input.
- **Not checked by this seat** (outside my assignment): the frozen after-counts (FRONTIER-CENSUS rows=46, FRONTIER-PASS F46, entries=49, capture records=82, knowledge-expected 86/84). Those are the integrator's to show.
- Live-source caveat: agreement was observed at 2026-11-04T21:52:46Z, 3 minutes after the committed fetch. Later drift of the live source is not ruled out.
