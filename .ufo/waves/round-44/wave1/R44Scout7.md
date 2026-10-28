# R44Scout7 — one disclosure format outside F01–F25

Axes: depth:verifiability, coverage. Read-only. No production or shared-file edit. No git/jj mutation. No tool install. Pacman not invoked. `RULES.md` read.

Format: **Open Source Vulnerability (OSV) schema v1.9.2**, the OpenSSF interchange format for vulnerabilities in open source packages. It is not an admitted frontier row. At commit `66314015122b9aa32dc40f2f1815df56624c26d1`, `corpus/README.md` F01–F25 are the admitted rows; F25 is the CVE JSON record format (S064). OSV appears only as rejected source row S065.

## Date

| Source | Date |
|---|---|
| Pinned prose, `docs/schema.md` line 11 at tag `v1.9.2` | `Version 1.9.2 (October 13, 2026)` |
| `CHANGELOG.md` line 50 at the same tag | `2026-10-13 Released version 1.9.2.` |
| GitHub release `v1.9.2` | `published_at` `2026-10-13T23:37:11Z`; commit `c8a57bdc5b0bc54646e140cabbb7834bd0b5aec9`; committer `2026-10-13T23:35:17Z`; subject `feat: release v1.9.2 (#635)` |
| This seat's fetch | HTTP `Date: Wed, 28 Oct 2026 19:00:06 GMT` for the tag files; site `Date: Wed, 28 Oct 2026 19:00:07 GMT` |

## Official source opened

- Public page: `https://ossf.github.io/osv-schema/` — HTTP 200, 228890 bytes, sha256 `8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8`. Byte-identical to the raw hash already recorded on committed S065. Version string is on `site.html` line 288. Root `schema.md` at the tag is only the pointer `Moved to <https://ossf.github.io/osv-schema>.` (46 bytes).
- Pinned prose (quotes below): `https://raw.githubusercontent.com/ossf/osv-schema/v1.9.2/docs/schema.md` — HTTP 200, 93945 bytes, 2010 lines, sha256 `96d82f03d763fb408bc344d01fc271f761a81cc225f6f6a42d318e3ed21cebff`.
- Pinned validator: `https://raw.githubusercontent.com/ossf/osv-schema/v1.9.2/validation/schema.json` — HTTP 200, 16868 bytes, 584 lines, sha256 `15b10dbb4c4e31c7aae11d22cdd991a9a374758db7c8389e62b3cc37cac92653`. `$schema` is JSON Schema draft 2020-12. Its `$id` still names `main`, not the tag.

Checked with preinstalled `jsonschema` 4.25.1 (`Draft202012Validator`). Not installed this seat.

## Quotes (pinned `docs/schema.md`)

Each of these occurs once in that file.

1. Lines 18–20. "This document defines a standard interchange format for describing vulnerabilities in open source packages."
2. Lines 106–107. "For serving, only the JSON encoding format is allowed, not a transliteration into any other encoding."
3. Lines 109–111. "Overall, the approach of this schema is to define only the fields that absolutely must be shared between databases, leaving customizations to the "ecosystem_specific" and "database_specific" blocks (see below)"
4. Lines 721–722. "The `id` and `modified` fields are required. For schema versions above 1.0.0, the `schema_version` field is also required."
5. Lines 167–168. "Do not encode mutable vulnerability metadata: IDs must not describe the vulnerability type or weakness (e.g. `SQLI`, `RCE`), package or component name (e.g. `LOG4J`), or severity rating (e.g. `CRITICAL`, `HIGH`)."
6. Lines 771–775. "Aliases should **not** be used to refer to vulnerabilities in packages upstream or downstream in a software supply chain from the given OSV record's affected package(s)."
7. Lines 1159–1161. "Only **a single type** (either `introduced`, `fixed`, `last_affected`, `limit`) is allowed in each event object. For instance, `{"introduced": "1.0.0", "fixed": "1.0.2"}` is **invalid**."
8. Lines 1163–1164. "Entries in the `events` array may be "last_affected" or "fixed" events, but not both."
9. Line 1182. "There must be at least one `introduced` object in the `events` array."
10. Lines 1204–1209. "The meaning of the values within the object is entirely defined by the database and beyond the scope of this document." Then: "Values in this field have no effect on the evaluation algorithm."

The same sentences are in the fetched HTML: purpose starts at line 298; the single-type rule at lines 1646–1648; "but not both" at line 1651; the introduced requirement at line 1669; "have no effect on the evaluation algorithm" at line 1696.

## Boundaries the source draws

- **What it is.** A JSON interchange format for open-source package vulnerabilities. A database may store another encoding; consumers are served JSON only (quotes 1–2).
- **What leaves the format.** Anything not shared by every database sits in `ecosystem_specific` or `database_specific` (quote 3). On a range, `database_specific` is defined by the database, is "beyond the scope of this document", and "have no effect on the evaluation algorithm" (quote 10). Top-level `database_specific` (lines 1527–1536) is the same kind of extension for the whole record.
- **Identity.** `id` is `<DB>-<ENTRYID>`, or `x_` for a local database not aggregated by OSV.dev (lines 143–150). New IDs should be semantically neutral (quote 5). `aliases` are the same vulnerability, symmetric and transitive, and are not the supply-chain link; that link is `upstream`, which is transitive and not symmetric (lines 758–797). `related` is what fails those two definitions (lines 807–812).
- **Required record fields, prose versus validator.** Prose requires `id`, `modified`, and `schema_version` above 1.0.0 (quote 4). The v1.9.2 validator's root `required` is only `id` and `modified` (lines 368–371). A document with those two fields and no `schema_version` validates. Root `additionalProperties` is `false` (line 583): an extra root key does not validate.
- **Affected ranges.** `ranges[].type` is the enum `GIT`, `SEMVER`, `ECOSYSTEM` (validator lines 89–93). `type` and `events` are required (lines 273–276). Each event object is one of `introduced`, `fixed`, `last_affected`, `limit` (quote 7; validator title at line 99: "events must contain an introduced object and may contain fixed, last_affected or limit objects"). `last_affected` and `fixed` cannot both appear (quote 8; validator title at line 246). At least one `introduced` is required (quote 9). `introduced` of `"0"` sorts before every version; a missing `limit` is an implicit `{ "limit": "*" }` (lines 1151–1155). `GIT` requires `repo` (prose line 1198; validator title line 163, "GIT ranges require a repo") and full-length commit hashes (title line 178, pattern `^(0|[a-f0-9]{40}|[a-f0-9]{64})$`).
- **Severity is someone else's score.** `severity[].type` is `CVSS_V2`, `CVSS_V3`, `CVSS_V4`, or `Ubuntu` (prose lines 861–866; validator lines 480–485). If any package-level `severity` is set, top-level `severity` must not be set (prose lines 1070–1073). The validator encodes that as package `severity` type `null` when top-level `severity` is present (lines 372–391).
- **Withdrawn is a timestamp, not a record state.** Missing `withdrawn` means the entry has not been withdrawn (lines 745–748).

Validator results against the tag file, `jsonschema` 4.25.1: `{id, modified}` valid; missing `id` invalid; extra root key invalid; omitted `schema_version` valid; one event object holding both `introduced` and `fixed` invalid; `fixed` together with `last_affected` invalid; events with only `fixed` invalid; `introduced` alone valid; `introduced` plus an unknown key `foo` **valid** (the prose single-type sentence is stricter than the validator, which does not set `additionalProperties: false` on an event object); range type `CPE` invalid; `GIT` without `repo` invalid; `GIT` `introduced` of `abc` invalid; 40-hex `introduced` with `repo` valid; top-level and package `severity` together invalid; a non-vector `CVSS_V4` score invalid.

`main`'s `validation/schema.json` is not the tag file (sha256 `ec09a74d4c4f7bafd57ee76781f2104f873fc1113b3eb82f047b5a09ab651afb`, 16915 bytes). First differing line is 439. The difference is the ecosystem `Raspberry Pi OS` and the id prefix `RPI`. Lines 1–438, which hold the event, repo, required-field, and severity rules above, are identical.

## Not F01–F25, and not a new admission

Committed counter, `git show HEAD:corpus/README.md`:

- do-nothing regex `^\| F[0-9]+ \| .* \| admitted \|` → **25**
- claims.json regex `^\| F[0-9]+ \| admitted \|` → **0**
- `^\| F26 \|` → **0**

The 25 is real under the control file's regex. The counter string in `claims.json` does not see those rows, because `admitted` is the third cell (`| F25 | <topic> | admitted |`), not the second. A do-nothing replay of the claims.json string cannot show the frozen before-count of 25. This seat did not change either file.

Committed S065 (`corpus/SOURCES.md`, the S065 row) is `rejected`, opened 2026-10-28, used-by `—`. Its own text says there is no lane capture and no manifest anchor. The flip it records is OSV range semantics (`affected[].ranges[].events`, or `database_specific` `extracted_events`) that the CVE format cannot express. Quotes 7–10 are that event boundary. They were not pinned on S065, which quotes only the purpose sentence. This seat still does not admit a row: the reject stands, and there is still no lane capture.

Sibling boundary, not a scope claim: `kaidoku-shokunin/corpus/SOURCES.md` line 21, S015, is one OSV **record** (`https://api.osv.dev/v1/vulns/CVE-2025-55305`), and the field it names is `affected[].ranges[].database_specific.extracted_events`. Quote 10 says values in that field do not affect OSV evaluation. `chousa-shokunin`, `kake-shokunin`, and `kengaku-shokunin` `corpus/SOURCES.md` have no match for `osv.dev`, `osv-schema`, `OpenVEX`, `SPDX 3`, or `csaf_security_advisory`.

F25's committed schema describes a third version status. `corpus/source-snapshots/round-42/S064.txt` line 129: "The status 'unknown' indicates that it is unknown or unspecified whether the given version is affected." OSV's `IsVulnerable` pseudocode (docs lines 1248–1255) returns true or false. That contrast is a reading of the two texts, not a sentence either document writes about the other.

## Do-nothing

Opening these URLs and writing this report does not add an F row, a knowledge entry, or a source capture. HEAD remains 25 admitted rows under the control regex. C1's eight routed defects were not re-counted here.

Worktree, not HEAD: `git status --short` showed `M corpus/README.md` and `M corpus/SOURCES.md` before this report existed. The worktree README matched the do-nothing regex **26** times. Those modifications are not this seat's, and they are not committed evidence. The visible extra row was a program-scope policy (Google Cloud VRP), not this format.

## Limitations

- Scratch was `/fast/scratch/hyaku/kasegi-r44/R44Scout7` because `HYAKU_SCRATCH` was unset in this process. Round-42 used `/fast/scratch/hyaku`. Deleted on exit; removal result is in the trailer.
- The published HTML matches the 2026-10-28 S065 hash, so the page did not move today. The tag prose is the line-stable copy. `main`'s validator has already added one ecosystem past v1.9.2.
- No lane snapshot or manifest was written. Hashes above are the re-fetch pins.
- C1 was not tested.

## Commands

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
# 66314015122b9aa32dc40f2f1815df56624c26d1

git -C ... show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| .* \| admitted \|'   # 25
git -C ... show HEAD:corpus/README.md | grep -cE '^\| F[0-9]+ \| admitted \|'         # 0
git -C ... show HEAD:corpus/README.md | grep -cE '^\| F26 \|'                         # 0

curl -sS -L -A kasegi-shokunin/r44-R44Scout7 -o docs-schema.md \
  https://raw.githubusercontent.com/ossf/osv-schema/v1.9.2/docs/schema.md
# http=200 bytes=93945 sha256=96d82f03d763fb408bc344d01fc271f761a81cc225f6f6a42d318e3ed21cebff

curl -sS -L -A kasegi-shokunin/r44-R44Scout7 -o validation-schema.json \
  https://raw.githubusercontent.com/ossf/osv-schema/v1.9.2/validation/schema.json
# http=200 bytes=16868 sha256=15b10dbb4c4e31c7aae11d22cdd991a9a374758db7c8389e62b3cc37cac92653

curl -sS -L -A kasegi-shokunin/r44-R44Scout7 -o site.html https://ossf.github.io/osv-schema/
# http=200 bytes=228890 sha256=8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8
```

Release and tag metadata: `GET https://api.github.com/repos/ossf/osv-schema/releases/tags/v1.9.2` and `.../git/refs/tags/v1.9.2`, both HTTP 200.

## Report trailer

- scope: read-only research; one report file; scratch removed
- path: `.ufo/waves/round-44/wave1/R44Scout7.md`
- committed lane HEAD read: `66314015122b9aa32dc40f2f1815df56624c26d1`
- tool install/update: none. `jsonschema` 4.25.1 was already installed and was used. Pacman not invoked.
- scratch: `/fast/scratch/hyaku/kasegi-r44/R44Scout7` (`HYAKU_SCRATCH` unset). `rm -rf` completed; the seat directory was absent afterward. The parent `kasegi-r44` was left in place.
