# ScribeSearchLog — round-39 receipt

Seat: ScribeSearchLog (scribe, leaf, no subagent dispatch). Round: kasegi-shokunin 39, claim C2 (coverage), frontier F22 (CISA, When to Issue VEX Information). Deliverable: `.ufo/waves/round-39/wave1/ScribeSearchLog.searchlog.append.md` — one prose `## Search log` bullet in the shape of the round-38 CSAF/VEX bullet (`corpus/SOURCES.md:86`, 2451 chars). Reads are read-only against the lane; the only lane writes are this receipt and the deliverable. All times UTC, 2026-10-26. Fetches: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`.

## 0. Result

The round-39 VEX-issuance search-log bullet is drafted, one line, no table and no heading (landable as-is): question, where, date, `identified 4, screened 4, included 1, excluded 3`, the inclusion (CISA When to Issue VEX Information → F22/S057) with its four measured quote anchors, the three rejections with reason and flip (S056/S058/S059, flip wording aligned to the `ScribeRowsRejected` item spec), and a `Stop:` clause. Landable bytes: **1 line, 3937 bytes, sha256 `400d393392d0dfb9e155acd5885a8714ab4269661119380ec270cb8a2b74222e`**.

Every figure in the bullet is from a command run this round, recorded below: six live fetches (HTTP 200, 0 redirects, effective URL == requested), one five-term negative sweep over the lane's own text (50 knowledge files, the pre-F22 state), and downstream measurements of the fetched bytes (`pdftotext` line counts, `grep` quote locators, enum token counts).

## 1. Lane state at read time

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git log --oneline -3 && git rev-parse HEAD
d65d823 round-39: wave1 spec/dispatch
dcd3170 round-39: claims freeze C1/C2 + controls
480b1a5 round-38 verifier spot-check (integrator, hyaku): non-author admit/reject
d65d823e7c84813c192b20ee757a8761f878a61f
$ git status --porcelain | grep -vc '^??'      -> 0     (tracked tree clean; only untracked .ufo/waves/round-39/*)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 55
$ grep -nE '^\| (S056|S057|S058|S059) ' corpus/SOURCES.md               -> no lines
$ ls corpus/knowledge/*.md | wc -l             -> 50
$ ls corpus/knowledge/cisa-when-to-issue-vex.md -> No such file or directory
$ sha256sum corpus/SOURCES.md; wc -l corpus/SOURCES.md
88bcd8c6bfbdca2180a113a60f0c7c3869ace3fd331d8118b65a39cbbf29ae61  corpus/SOURCES.md
122 corpus/SOURCES.md
$ ls corpus/source-snapshots/round-39/          -> No such file or directory
$ cat .ufo/waves/round-39/c2-controls/before.txt -> frontier 21; registry 55; S057 0; knowledge 50; harness 24/24; binding 45/45; audit expected=50
```

`## Search log` spans `corpus/SOURCES.md:71-86`; the round-38 bullet is the last line of the section (line 86), `## Leads (unopened)` starts at line 87. Landing anchor for the deliverable: append after line 86.

## 2. Live fetch ledger (instrument UA, 2026-10-26T19:30:58Z)

All six fetches: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o <file> -w '%{http_code} %{size_download} %{content_type}'`. A second pass measured `%{num_redirects} %{url_effective}` for each: **200, redirects=0, effective URL == requested URL** in all six cases.

| # | URL | HTTP | bytes | content-type | sha256 | local lines |
|---|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/resources-tools/resources/when-issue-vex-information | 200 | 54453 | text/html; charset=utf-8 | `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d` | 1684 |
| 2 | https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf | 200 | 235270 | application/pdf | `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` | 1457 raw / **400** pdftotext |
| 3 | https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex | 200 | 49253 | text/html; charset=utf-8 | `67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8` | 1472 |
| 4 | https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf | 200 | 1047967 | application/pdf | `1e73325c674aa55c5665e3d2b647201acc46ee1fa9c8ee8bf88e4ff044f975c8` | 4259 raw / **812** pdftotext |
| 5 | https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md | 200 | 30580 | text/plain; charset=utf-8 | `9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884` | 671 |
| 6 | https://cyclonedx.org/docs/1.7/json/ | 200 | 6419901 | text/html; charset=utf-8 | `85c1f8ec534c551fa8269f6201156bb770413e950822bfb72d256d17d5d90587` | 897 |

Digest stability against the round-38 scout (`ScoutVexLeads.md` §1): #1 `4e6aa483…`, #2 `cbcbd77a…`, #3 `67bafe17…`, #4 `1e73325c…`, #5 `9375415c…` are byte-identical to the round-38 fetch. #6 changed: round-38 recorded `afb22b46d49ad68a648cfb1b9ec3f0f47028cc6170a8ad133603fac30e88f3f9` at the same 6419901-byte length; this round it is `85c1f8ec…`. That live drift is the measured ground for the S059 rejection ("needs a scoped capture of the `analysis` subtree before any quote can be pinned") and is stated in the bullet.

`pdftotext -layout` was run only to locate quotes; the committed capture is ExecFrontierCapture's normalized PDF text for `corpus/source-snapshots/round-39/S057.txt`, not these scratch extractions.

## 3. Content checks (scratch extractions, this round's bytes)

- **S057 / When to Issue**, `pdftotext -layout` of #2, 400 lines, front matter `TLP:CLEAR` (L1) and `Publication date: November 2023` (L6); page carries `datetime="2023-11-06T12:00:00Z"` exactly once (grep of #1).
  - L19-20: "Whether, and when, to issue VEX information is a business decision for most suppliers and possibly a more individual decision for independent open source developers." — bullet quotes "a business decision for most suppliers".
  - L129-130: "The decisions and timing around providing VEX information are primarily business decisions and are not determined by a strict protocol." — bullet quotes "determined by a strict protocol".
  - L204-206: "Ideally, when a new vulnerability is disclosed, an “under_investigation” status should be issued. When the investigation has concluded, status should be updated, for example, noting that the product is “affected” or “not_affected.”" — lifecycle layer.
  - L209-211: "By updating a timestamp but not changing status or other information, a VEX issuer can reaffirm that the current status remains accurate at the present time." — bullet quotes "the current status remains accurate".
  - L286-288: "VEX consumers should carefully evaluate if it is valid to inherit status from upstream components. Strictly speaking, consumers should not assume the status of an upstream component applies to a product that uses the component." — bullet quotes "should not assume the status of an upstream component applies".
- **S056 / Minimum Requirements** (#3/#4): PDF L24 "derived from, but may not fully conform to, existing VEX documentation and implementations"; statuses at L410-413 (`Not affected` / `Affected` / `Fixed` / `Under investigation`); justifications from L435-439 including `Vulnerable_code_not_present`. Same four statuses and five labels the bullet says S055 already mirrors.
- **S058 / OpenVEX** (#5): L1 `# OpenVEX Specification v0.2.0`; L205-219 the justification/impact_statement note and the "issuers SHOULD use the machine readable justification labels and optionally enrich the statement" recommendation the flip names; statuses L343-356. Digest identical to round-38, so no re-reading was needed beyond confirming H1 and the note.
- **S059 / CycloneDX** (#6): token counts in the fetched page — `code_not_present` 1, `code_not_reachable` 1, `requires_configuration` 1, `requires_dependency` 1, `requires_environment` 1, `protected_by_compiler` 1, `protected_at_runtime` 1, `protected_at_perimeter` 1, `protected_by_mitigating_control` 1, `in_triage` 1, `false_positive` 1, `resolved_with_pedigree` 1 (nine justifications, and the six-state set the bullet cites). The page is minified (897 lines over 6419901 bytes), one occurrence per token — a scoped extraction is required before quoting, as the bullet says.

## 4. Negative sweep (lane ground, pre-F22)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ for t in "reaffirm" "when to issue" "issuance" "inherit" "under_investigation"; do
    n=$(grep -rniF -- "$t" corpus/knowledge/ corpus/README.md corpus/SOURCES.md SKILL.md 2>/dev/null | wc -l); echo "$t -> $n"; done
reaffirm -> 0
inherit -> 9
when to issue -> 0
issuance -> 1
under_investigation -> 7
$ ls corpus/knowledge/*.md | wc -l   -> 50
```

Categorization (from the hit lines): `issuance` — 1, `vendor-disclosure-policies-as-corpus-objects.md:94` "account issuance" (account provisioning, unrelated). `inherit` — 9: `mission-control.md:165` (inherited accounting), `submitted-registry.md:133` (registry exclusion inheritance), `ufo-archive-2026.md:160` (archive junk verdict), `statutory-authorization-and-unauthorized-access.md:33,64,87` ("次号において同じ" statutory cross-reference), `corpus/README.md:190,191` (lessons-row descriptions), `corpus/SOURCES.md:39` (S033 row). `under_investigation` — 7: five in `csaf-vex-product-status-and-justifications.md` (L30, 32, 39, 88, 109), one in `corpus/README.md:477` (the F21 frontier row) and one in `corpus/SOURCES.md:61` (the S055 row). All seven are S055's CSAF product-status vocabulary; none states issuance, lifecycle, reaffirmation or inheritance. The bullet states exactly this.

## 5. Deliverable

- Path: `.ufo/waves/round-39/wave1/ScribeSearchLog.searchlog.append.md`
- Content: one `- ` prose bullet; no heading, no table, no leading/trailing scaffold; 0 `|` characters.
- Size: 1 line, 3937 bytes; sha256 `400d393392d0dfb9e155acd5885a8714ab4269661119380ec270cb8a2b74222e` (command output in §6). The exclusion clause reads `Excluded as rejected rows, with reason:` so the bullet names the three rows' status, not only their verdict.
- Abbreviated digests inside the bullet were verified as true prefix/suffix of the full digests: `67bafe17`/`05a8eab8`, `1e73325c`/`044f975c8`, `9375415c`/`5519f884`, `85c1f8ec`/`d5d90587`, `afb22b46` prefix-only — all `True` against the round-38/full values (the SOURCES.md:120 correction duty).
- Capture binding, checked after the sibling landed it: `.ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt` (17971 bytes, sha256 `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`, opening `TLP:CLEAR` / `When to Issue VEX Information` / `Publication date: November 2023`) and `ExecFrontierCapture.manifest.json` records `raw_bytes 235270`, `raw_sha256 cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99`, `fetched_utc 2026-10-26T19:30:55Z` — the same PDF bytes this seat measured three seconds later, and the page digest `4e6aa483…` matches too. The bullet's "captured as the PDF's converted text … page digest recorded in `manifest.json`" is therefore verified against the landed file, not just the capture item spec.
- Landing: append after `corpus/SOURCES.md:86` (last line of `## Search log`, before `## Leads (unopened)` at line 87). The round-38 bullet's shape is matched clause for clause: `- <topic> sweep (round 39); question: …; where: …; date: 2026-10-26; identified 4, screened 4, included 1, excluded 3. Included: … Excluded as rejected rows, with reason: … Stop: …`.

## 6. Digest and shape verification output

```
$ cd .ufo/waves/round-39/wave1 && wc -l -c ScribeSearchLog.searchlog.append.md && sha256sum ScribeSearchLog.searchlog.append.md && grep -c '|' ScribeSearchLog.searchlog.append.md
   1 3937 ScribeSearchLog.searchlog.append.md
400d393392d0dfb9e155acd5885a8714ab4269661119380ec270cb8a2b74222e  ScribeSearchLog.searchlog.append.md
0
$ python3 (prefix/suffix check against the five full digests) -> 67bafe17 05a8eab8 True True / 1e73325c 044f975c8 True True / 9375415c 5519f884 True True / 85c1f8ec d5d90587 True True / afb22b46 None True
```

(The `grep -c` exits 1 with output `0`, as grep does on zero matches; the newline count `wc -l` = 1 means one bullet line plus the final LF.)

## 7. Out of scope and known limits

- No corpus, registry, frontier, knowledge or capture file was written: `corpus/SOURCES.md` is untouched at `88bcd8c6…`; the bullet and this receipt are the only lane writes. `corpus/source-snapshots/round-39/` did not exist at read time, so the bullet names the capture path the C2 capture seat lands; it does not quote a capture digest.
- NF=13, the S057 anchor cell and the `teaches` cell belong to the `ScribeRowS057` item and were not measured here; the bullet asserts only the row's identity fields from `claims.json` (tier A, kind docs, status mined, opened 2026-10-26).
- The capture's normalization is verified, not assumed: `ExecFrontierCapture.S057.txt` is the PDF's converted text and its manifest carries the page digest (see §5). No caveat remains for the bullet's capture clause.
- The bullet says "admitted as Frontier F22 with new row S057"; the frontier/F21→F22 row edits land with the L1's corpus integration, not with this seat.
- Rejections' flip wording is taken from the `ScribeRowsRejected` item spec so the bullet and the row files agree; no row file was edited.
- Tooling: nothing installed or upgraded (curl 8.23.0, pdftotext 26.08.0, Python 3.14.8 already present). No pacman, no PATH writes, no host service touched.
- Disk guard checked green before the fetches (`/tmp` 3%, `/var/tmp` 35%, `/fast/scratch/hyaku` 25%, 609.7G free); the largest scratch file was the 6.4 MB CycloneDX page.
- Scratch `/fast/scratch/hyaku/kasegi-r39/ScribeSearchLog/` removed before yield; nothing under `/tmp` was created by this seat.
