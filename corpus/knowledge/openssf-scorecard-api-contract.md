# OpenSSF Scorecard API: the machine contract for a published scorecard result

source: S102 — https://api.securityscorecards.dev/swagger.json — "OpenSSF Scorecard API", swagger 2.0, info.version 1.1.0, declared host api.scorecard.dev; capture corpus/source-snapshots/round-68/S102.txt (sha256 6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0, 429 lines, 7595 snapshot bytes over 11802 fetched bytes): the API description at S102.txt:13, the result route at S102.txt:19-37, the publish route at S102.txt:93-107, the version route at S102.txt:234-244, the Error/Repo/ScorecardCheck/ScorecardResult definitions at S102.txt:268-370
verified-at: 2026-11-04
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-68/manifest.json --source S102   # 8 pinned quotes (Q01, Q02, Q04-Q09), each exactly-once at its anchor; the route and definition inventory below is read from the captured swagger document, not from a fresh network fetch
ground: F46 — the OpenSSF Scorecard project's machine interface to its published results: the route family, the ScorecardResult / ScorecardCheck / Repo / Error definitions and the aggregate-score field. The check taxonomy and risk tiers stay with F35/S086; served project results are instance data and are not ground here.

## Scope and decision rule

This entry records the **interface** through which a published Scorecard result is read and written: the
routes, their parameters, and the shape of the object a reader receives. The source is the Scorecard API's own
swagger 2.0 document, captured as one file; every quoted fragment below is located at a line of that capture
(`S102.txt:LINE`). The capture keeps the served line structure with whitespace collapsed, so each JSON member
sits on its own line.

The document names itself and its purpose: `"title": "OpenSSF Scorecard API"` (`corpus/source-snapshots/round-68/S102.txt:14`), described as
"API to interact with a project's published Scorecard result" (`corpus/source-snapshots/round-68/S102.txt:13`). It declares `"swagger": "2.0"`
(`corpus/source-snapshots/round-68/S102.txt:11`), `"version": "1.1.0"` (`corpus/source-snapshots/round-68/S102.txt:15`), `"host": "api.scorecard.dev"` (`corpus/source-snapshots/round-68/S102.txt:17`) and the
single scheme `"https"` (`corpus/source-snapshots/round-68/S102.txt:9`).

Decision rule for "what does a Scorecard API result carry, and how is it addressed?" — read the contract, not a
served instance:

1. **A result is addressed by platform, owner and repository.** The path is
   `/projects/{platform}/{org}/{repo}` (`corpus/source-snapshots/round-68/S102.txt:19`); its three path parameters are described as
   "VCS platform. eg. github.com" (`corpus/source-snapshots/round-68/S102.txt:139`), "Name of the owner/organization of the repository"
   (`corpus/source-snapshots/round-68/S102.txt:146`) and "Name of the repository" (`corpus/source-snapshots/round-68/S102.txt:153`), each `"required": true` (`corpus/source-snapshots/round-68/S102.txt:142`,
   `:149`, `:156`).
2. **Reading is a GET that may pin a commit.** The GET's summary is "Get a repository's ScorecardResult"
   (`corpus/source-snapshots/round-68/S102.txt:24`), operationId `getResult` (`corpus/source-snapshots/round-68/S102.txt:25`). Its one query parameter is `commit`
   (`corpus/source-snapshots/round-68/S102.txt:31-32`), "SHA1 commit hash expressed in hexadecimal format" (`corpus/source-snapshots/round-68/S102.txt:30`), constrained by
   `"pattern": "^[0-9a-fA-F]{40}$"` (`corpus/source-snapshots/round-68/S102.txt:28`) — exactly 40 hex digits. The document does not mark
   `commit` as required. A 200 returns "A JSON object of the repository's ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:37`)
   with `$ref` to `ScorecardResult`; a 400 is "The request provided to the server was invalid" (`corpus/source-snapshots/round-68/S102.txt:53`)
   with an `Error` schema; a 404 is "The content requested could not be found" (`corpus/source-snapshots/round-68/S102.txt:69`) and declares no
   body schema.
3. **Writing is a separate POST on the same path, and it is OIDC-verified.** The POST's summary is "Publish a
   repository's OIDC verified ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:93`), operationId `postResult` (`corpus/source-snapshots/round-68/S102.txt:94`). Its
   one parameter is the body parameter `publish` (`corpus/source-snapshots/round-68/S102.txt:97`), `"required": true` (`corpus/source-snapshots/round-68/S102.txt:99`), whose
   schema is `#/definitions/VerifiedScorecardResult` (`corpus/source-snapshots/round-68/S102.txt:101`). The 201 response is "Successfully
   updated ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:107`). `VerifiedScorecardResult` (`corpus/source-snapshots/round-68/S102.txt:387`) has four properties:
   `result` (string, `corpus/source-snapshots/round-68/S102.txt:390-391`), `branch` (string, `corpus/source-snapshots/round-68/S102.txt:394-395`), `accessToken` (string,
   `corpus/source-snapshots/round-68/S102.txt:398-399`) and `tlogIndex` (integer, `corpus/source-snapshots/round-68/S102.txt:402-403`).
4. **The server reports its own build on `/version`.** The route `/version` (`corpus/source-snapshots/round-68/S102.txt:234`) is summarized
   "Get the build this server is running" (`corpus/source-snapshots/round-68/S102.txt:240`), operationId `getVersion` (`corpus/source-snapshots/round-68/S102.txt:241`), and
   described as "Reports the scorecard-infra release and commit this server was built from, and the workflow
   parser that verifies uploads." (`corpus/source-snapshots/round-68/S102.txt:236`). Its 200 is "The server's build information"
   (`corpus/source-snapshots/round-68/S102.txt:244`), a `VersionInfo` (`corpus/source-snapshots/round-68/S102.txt:408`) whose properties `version`, `commit` and `parser` are
   described at `corpus/source-snapshots/round-68/S102.txt:412`, `:417` and `:422`.
5. **A badge route exists beside the result route.** `/projects/{platform}/{org}/{repo}/badge`
   (`corpus/source-snapshots/round-68/S102.txt:160`), "Get a repository's Scorecard badge" (`corpus/source-snapshots/round-68/S102.txt:168`), takes a `style` query parameter
   (`corpus/source-snapshots/round-68/S102.txt:181-183`) and answers 302 "Scorecard badge for the repository" (`corpus/source-snapshots/round-68/S102.txt:209`). These three
   paths are the document's entire `paths` object (measured: `grep -c '^"/' S102.txt` = 3).

### The result object

`ScorecardResult` (`corpus/source-snapshots/round-68/S102.txt:336`) has six properties, in the document's own `x-order`:

| property | type in the contract | location |
|---|---|---|
| `date` | string; no `format` is declared | `corpus/source-snapshots/round-68/S102.txt:339-340` |
| `repo` | `$ref` `#/definitions/Repo` | `corpus/source-snapshots/round-68/S102.txt:343-345` |
| `scorecard` | object, `$ref` `#/definitions/ScorecardVersion` | `corpus/source-snapshots/round-68/S102.txt:347-350` |
| `score` | number, "Aggregate score of the repository", `"x-omitempty": false` | `corpus/source-snapshots/round-68/S102.txt:352-355` |
| `checks` | array of `#/definitions/ScorecardCheck` | `corpus/source-snapshots/round-68/S102.txt:358-361` |
| `metadata` | string | `corpus/source-snapshots/round-68/S102.txt:365-366` |

`Repo` (`corpus/source-snapshots/round-68/S102.txt:281`) has `name` — "respository that was analyzed" (`corpus/source-snapshots/round-68/S102.txt:285`, the source's own
spelling) — and `commit` — "SHA1 value of the analyzed commit expressed as hexadecimal" (`corpus/source-snapshots/round-68/S102.txt:290`), with
the same 40-hex pattern (`corpus/source-snapshots/round-68/S102.txt:292`). `ScorecardVersion` (`corpus/source-snapshots/round-68/S102.txt:371`) carries the analysing tool's
`version`, "Scorecard version used for this analysis" (`corpus/source-snapshots/round-68/S102.txt:375`), and its `commit`, "SHA1 value of the
Scorecard commit used for analysis" (`corpus/source-snapshots/round-68/S102.txt:380`).

`ScorecardCheck` (`corpus/source-snapshots/round-68/S102.txt:297`) has `name` (string, `corpus/source-snapshots/round-68/S102.txt:300-301`), `score` (**integer**,
`corpus/source-snapshots/round-68/S102.txt:304-305`, `"x-omitempty": false` at `corpus/source-snapshots/round-68/S102.txt:306`), `reason` (string, `corpus/source-snapshots/round-68/S102.txt:309-310`),
`documentation` (object, `corpus/source-snapshots/round-68/S102.txt:313-314`) whose properties are `url` (string, `corpus/source-snapshots/round-68/S102.txt:316-317`) and
`short` (string, `corpus/source-snapshots/round-68/S102.txt:320-321`), and `details` (array of strings, `corpus/source-snapshots/round-68/S102.txt:327-330`). The aggregate
`score` on the result is typed `number` (`corpus/source-snapshots/round-68/S102.txt:354`) while each check's `score` is typed `integer`
(`corpus/source-snapshots/round-68/S102.txt:305`); the contract states the types and states nothing more about either value.

`Error` (`corpus/source-snapshots/round-68/S102.txt:268`) has two properties and no descriptions: `code` (integer, `corpus/source-snapshots/round-68/S102.txt:271-272`) and
`message` (string, `corpus/source-snapshots/round-68/S102.txt:275-276`).

| id | observed question | ground |
|---|---|---|
| G1 | What is this API for? | "API to interact with a project's published Scorecard result" (`corpus/source-snapshots/round-68/S102.txt:13`) |
| G2 | What does the result route return? | "Get a repository's ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:24`); "A JSON object of the repository's ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:37`) |
| G3 | How is a specific commit's result selected? | "SHA1 commit hash expressed in hexadecimal format" (`corpus/source-snapshots/round-68/S102.txt:30`), pattern `^[0-9a-fA-F]{40}$` (`corpus/source-snapshots/round-68/S102.txt:28`) |
| G4 | Which commit did a result analyse? | "SHA1 value of the analyzed commit expressed as hexadecimal" (`corpus/source-snapshots/round-68/S102.txt:290`) |
| G5 | Which field is the repository-level score? | "Aggregate score of the repository" (`corpus/source-snapshots/round-68/S102.txt:353`) |
| G6 | How is a result published? | "Publish a repository's OIDC verified ScorecardResult" (`corpus/source-snapshots/round-68/S102.txt:93`) |
| G7 | How does a reader learn the server's build? | "Get the build this server is running" (`corpus/source-snapshots/round-68/S102.txt:240`) |
| G8 | Which tool version produced a result? | "Scorecard version used for this analysis" (`corpus/source-snapshots/round-68/S102.txt:375`) |

## What the document does NOT say

Each item was checked against the capture; a zero is a measured `grep -c -F` over S102.txt on 2026-11-04.

- **No score range or computation.** The capture carries no `minimum` or `maximum` (0 and 0) and no weighting
  vocabulary (`weight` 0). The document does not say the aggregate is 0-10, how it is computed from the
  checks, or what a check `score` of any particular value means. Score semantics, risk tiers and the check
  list stay with F35/S086 (`corpus/knowledge/openssf-scorecard-checks.md`); this entry claims none of them.
- **No check-name enumeration.** `ScorecardCheck.name` is a bare string (`corpus/source-snapshots/round-68/S102.txt:300-301`); the only `enum`
  in the document is the badge `style` list (`grep -c -F '"enum"'` = 1, at the badge route).
- **No authentication scheme.** The document declares no `securityDefinitions` and no `security` member (0 and
  0). The POST's summary says "OIDC verified" (`corpus/source-snapshots/round-68/S102.txt:93`, the only `OIDC` occurrence), and the body names
  an `accessToken` and a `tlogIndex`; the document does not say which token, which transparency log, or how
  verification is performed.
- **No date format.** `ScorecardResult.date` is typed string with no `format` member (`"format"` 0).
- **No meaning for `metadata`, `details`, `branch` or `result`.** They carry a type and no description.
- **No error-code catalogue.** `Error.code` is an integer with no description and no enumerated values.
- **Host mismatch is the document's, not the capture's.** The bytes were served at
  api.securityscorecards.dev while the document declares `"host": "api.scorecard.dev"` (`corpus/source-snapshots/round-68/S102.txt:17`). The
  document does not say whether the two hosts serve the same data; no such claim is made here.

## Overlap and novelty

Contrast with **F35**, the OpenSSF Scorecard check documentation
(`corpus/knowledge/openssf-scorecard-checks.md`, source S086). F35 holds the *program's check contract*: which
checks exist, the risk tier each carries and what each tests. This entry holds the *machine interface* that
serves a result: the route a reader calls, the commit pin, the publish path, and the object shape — including
the field that carries the aggregate score, which F35's check documentation does not define as a wire field. A
reader with only F35 cannot say which URL returns a result or what JSON keys it has; a reader with only this
entry cannot say what any check measures or what its score means.

Contrast with **F30**, the CVE Services publication API (`corpus/knowledge/cve-services-publication-api.md`):
both are first-party machine contracts, but F30 is the write path for CVE records and its actor split, while
this entry is a repository-health scoring service. Neither holds the other's ground.

## Gate — S102 (OpenSSF Scorecard API swagger 2.0 contract)

- **URL:** https://api.securityscorecards.dev/swagger.json (HTTP 200, final URL equal to the requested URL, no
  redirect; `content-type: application/json`).
- **Access date:** 2026-11-04. The committed capture's `fetched_utc` is 2026-11-04T21:49:46Z
  (`corpus/source-snapshots/round-68/manifest.json`). Seat ScribeF46 re-opened the URL with curl at
  2026-11-04T21:53:23Z (server `date: Wed, 04 Nov 2026 21:53:23 GMT`): 11802 bytes, raw sha256
  `d526f3274a6dbcb1ba6632bf3ee1e9a642dc2106b18a1354cc0c8a26104c8af4`; collapsing each line's whitespace and
  dropping empty lines gave 429 lines with sha256
  `6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0`, byte-identical to S102.txt
  (`diff -q` silent). Receipt: `.ufo/waves/round-68/w1/ScribeF46/reopen.txt`.
- **Edition:** the document's own `"version": "1.1.0"` (`corpus/source-snapshots/round-68/S102.txt:15`); it states no publication date.
- **Located quotes (≤25 words each, verbatim at the anchor, word counts by `wc -w`):**
  1. "API to interact with a project's published Scorecard result" (L13, 9 words).
  2. "OpenSSF Scorecard API" (L14, 3 words).
  3. "Get a repository's ScorecardResult" (L24, 4 words).
  4. "SHA1 commit hash expressed in hexadecimal format" (L30, 7 words).
  5. "A JSON object of the repository's ScorecardResult" (L37, 7 words).
  6. "Publish a repository's OIDC verified ScorecardResult" (L93, 6 words).
  7. "Successfully updated ScorecardResult" (L107, 3 words).
  8. "Reports the scorecard-infra release and commit this server was built from, and the workflow parser that verifies uploads." (L236, 18 words).
  9. "Get the build this server is running" (L240, 7 words).
  10. "respository that was analyzed" (L285, 4 words).
  11. "SHA1 value of the analyzed commit expressed as hexadecimal" (L290, 9 words).
  12. "Aggregate score of the repository" (L353, 5 words).
  13. "Scorecard version used for this analysis" (L375, 6 words).
- Quotes 1-5, 10-12 are the manifest's pinned Q01, Q02, Q04-Q09 and are re-verified by the `recheck:` line;
  quotes 6-9 and 13, and every JSON member cited above by line, are verified by `grep -n -F` over the pinned
  capture in this seat's receipt, not by the manifest.

## Limits

- The capture is the swagger document of one API version (`info.version` 1.1.0, `swagger` 2.0) as served on
  2026-11-04; the recheck verifies the pinned bytes and the located quotes, not that the live service still
  serves this contract or behaves as it declares.
- Refused and recorded: a live project result (`/projects/github.com/ossf/scorecard`) was opened by the round's
  capture pass and refused as an entry source (one 13259-byte line, no line anchors, instance values that
  change per analysis; recorded in the round-68 manifest note). No served score, date or check value appears
  in this entry.
- The entry reads the contract's routes, parameters and definitions only. It does not claim response
  latency, caching behaviour beyond the declared header names, rate limits, or the meaning of any score.
- No credential material appears in this entry: `accessToken` is a property *name* in the contract; no token,
  key or session value was captured or used. Documentation only: nothing here instructs calling the publish
  route, probing the service, or contacting any project.
