# ScribeEntryF18 — F18 knowledge entry draft (CISA KEV catalog)

Seat: ScribeEntryF18, round 35, wave 1, leaf (no subagents). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base `3266c993`; claims freeze `617496b9`. No jj/git mutation run; no commit made.

Deliverable (working copy, L1 commits): `corpus/knowledge/cisa-kev-catalog.md` — 88 lines, 13,308 bytes, sha256 `da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf`.

## Report

### R1 — inputs read (paths, not summaries)

- `corpus/source-snapshots/round-35/S052.txt` — 1,479,694 bytes, 27,870 lines, sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`.
- `corpus/source-snapshots/round-35/manifest.json` — sha256 `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`; record S052 pins path `S052.txt`, the same digest, url `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`, `fetched_utc: 2026-10-26T06:32:40Z`, assertions Q1 anchor 2, Q2 anchor 3, Q3 anchor 4, Q4 anchor 15472, Q5 anchor 19165.
- `corpus/QUALITY.md` (Q1–Q10, R1–R25), `corpus/SOURCES.md` (no S052 row yet at read time), `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (round-34 F17 form), `corpus/instruments/source-recheck.py` lines 1–260 (Q9/B1/B2 and occurrence/anchor semantics), `corpus/instruments/capture-source.py` (`--kind text` vs default `html`), `corpus/README.md:344-370` (F17 admission shape). `corpus/lessons/round-34*.md`, `SCORECARD.md`, `corpus/README.md` full reads were not needed for this seat's item and were not performed beyond the cited ranges.

### R2 — recheck run (the entry's own `recheck:` line, verbatim execution)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit=0
```

`bash -n` on the exact `recheck:` line (comment included): `exit=0`. The line carries the `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` prefix (measured by `grep -m1 '^recheck:' | cut -c1-120`).

### R3 — quote inventory in the entry (normalized occurrence counts on the landed capture)

| entry line | quote (trimmed) | words | occurrences |
|---|---|---|---|
| 14 | `"title": "CISA Catalog of Known Exploited Vulnerabilities",` | 7 | 1 |
| 16 | `"dateReleased": "2026-10-23T19:30:18.9209Z", "count": 1756,` | 4 | 1 |
| 22 | Q4 record tail (dueDate/knownRansomwareCampaignUse/forensicTriage/notes, CVE-2022-29499) | 8 | 1 |
| 24 | Q5 record lines (dateAdded/shortDescription/requiredAction/dueDate, CVE-2019-12989) | 19 | 1 |
| 36 | `"The KEV due date refers to the deadline by which FCEB agencies are expected to review"` | 16 | 2 |
| 38 | `"Apply mitigations per vendor instructions, follow applicable BOD 22-01 guidance for cloud services, or discontinue use of the product if mitigations are unavailable."` | 23 | 327 |

All six are verbatim substrings of the capture; four are exactly-once (and are the manifest assertions Q1/Q2/Q4/Q5 plus Q3's cross-line form). Two cannot be exactly-once, so they are anchored in the entry (L5423, L2246) and counted by FC-9/FC-10 rather than added to the manifest — adding them would make the frozen C2 literal "every assertion `occurrences=1`" false. The entry states this trade-off in its Scope section.

### R4 — falsifiable checks, executed as written (output is what the entry prints)

```
FC-1 keys 5 count 1756 records 1756
FC-2 ids 1756 of 1756
FC-3 keysets 1 keys 12
FC-4 {'Unknown': 1395, 'Known': 361} {'Yes': 91, 'No': 1665}
FC-5 forward 1756 of 1756 [(21, 1025), (14, 280), (181, 238)]
FC-6 bod22 340 bod26 139 both 0 neither 1277
FC-7 distinct 46 top [('Apply updates per vendor instructions.', 893)]
FC-8 cvss=0 base score=0 risk rating=0 reward=0 bounty=0 severity+score=3
FC-9 2
FC-10 327
FC-11 11954
```

### R5 — Q1–Q10 mapping for the drafted entry

- Q1: H1 on line 1; line 3 `source: S052 — <feed URL>` with capture path, digest and line anchors (L2, L3, L4-L5, L7-L22 fields, L5423, L15465-L15475, L19161-L19168); line 4 `verified-at: 2026-10-26`; line 5 `ground: F18` (F17 precedent); line 6 one `recheck:` command.
- Q2: all load-bearing claims cite S052, the only source in the capture; no tier-C row used.
- Q3: six located verbatim quotes, 4–23 words (table R3); every number is printed by an FC command or the manifest assertion.
- Q4: attribution section states the catalog is CISA's and that the definition sentence is not in S052; the FCEB/BOD sentences are quoted as CISA field text, not as universal rules.
- Q5: one explicit falsifiable rule (five named failure conditions) plus six rejected over-generalizations.
- Q6: documentation only; no credential/session/private-URL text; quotes only public feed bytes.
- Q7: recheck is a command, not prose; output names `sha256 OK` and per-assertion `occurrences`; a missing manifest/capture returns exit 2 (observed at freeze for this manifest path before it landed), a moved quote exit 1.
- Q8: the entry declares the whitespace normalization for Q3/Q4/Q5 (`normalized=markup-whitespace`), and each cross-line assertion states the lines it joins.
- Q9: path stem `S052` equals record id; every manifest assertion is exactly-once with a verified anchor; the instrument prints the occurrence count.
- Q10: `bash -n` exit 0; `cd` prefix present; human note after `#`.

### R6 — findings: the capture contradicts three hints in the F18 seat prompt (recorded, not silently smoothed)

1. **URL.** `https://www.cisa.gov/known-exploited-vulnerabilities.json` returns **HTTP 404** (46,916-byte HTML error page; measured independently with the instrument UA). The live feed is `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` (HTTP 200, `application/json`, 1,807,090 bytes, requested == effective URL). The entry, the manifest and ExecC2Capture's receipt all use the feed URL; the 404 belongs in the search log, not the header.
2. **Count.** The capture's `count` field is **1,756** (L5), equal to `len(vulnerabilities)` and to the distinct `cveID` count — not the prompt's "~1,300". Catalog version `2026.10.23`, released `2026-10-23T19:30:18.9209Z`.
3. **Fields.** Records carry **12** keys, not nine: the prompt's nine plus `forensicTriage`, `notes`, `cwes`. One key set across all 1,756 records (FC-3). No field encodes exploitation evidence, an actor, or an exploited/not-exploited status; the only status flags are `knownRansomwareCampaignUse` (Known 361 / Unknown 1,395) and `forensicTriage` (Yes 91 / No 1,665).
4. **Directive.** The prompt's "dueDate clock binds BOD 22-01 for federal agencies" is only partly what the bytes say. Per record: BOD 22-01 in 340 `requiredAction` values, BOD 26-04 in 139 (138 of those records also in `notes`), both 0, neither 1,277 (FC-6). The only sentence stating an addressee is the KEV deadline sentence at L5423/L5439: "The KEV due date refers to the deadline by which FCEB agencies are expected to review and begin implementing the guidance outlined in Emergency Directive (ED) 25-03" (2 occurrences). The entry states the clock as per-record, names both directives with counts, and explicitly does not assert the directives' addressees or legal force because their text is absent.
5. **Definition.** The feed has no prose definition of "known exploited"; its only descriptive text is the title (L2). The entry does not attribute a definition sentence to S052 and records this as an honest limit.
6. **Not a severity or reward ladder (measured absences).** `cvss` 0, `base score` 0, `risk rating` 0, `reward` 0, `bounty` 0; `severity` twice (L5135, L11629 — URL slugs in `notes`) and `score` once (L23592 — prose in a `shortDescription`); the single `$` is the Java identifier `UserResource$UriData` (L11954). So the entry says "no severity field", not "no severity token".

### R7 — cross-seat count reconciliation (both peers were told the measured numbers)

- `ScribeSOURCESRow-2` reported "341 records mention BOD 22-01 in notes/requiredAction". Measured: **340**, all in `requiredAction`, 0 in `notes`, 0 in any other string field (`any-field` count 340; `requiredAction` 340).
- `ExecRegistryAppend-3` reported "277 name BOD 26-04". Measured: **139 rows** by `requiredAction`, of which **138** also carry it in `notes` — 277 is the field-hit count (139 + 138), not the row count. No record carries both directives (0).
- The discrepancy does not affect the entry: it states the row counts 340 / 139 / 1,277 and the 46 distinct `requiredAction` values, each printed by FC-6/FC-7.

### R8 — out of scope / not performed (L1 owns these)

- The S052 row insert into `corpus/SOURCES.md` (ExecRegistryAppend-3 holds the frozen block; row `05c4310a…`, blocks `c47f1a4d…`) — the entry's header already names `S052` and the feed URL so the row and entry agree.
- The `corpus/README.md` F18 frontier row (frontier 17 → 18), the harness `entries=21 pass=21` including `PASS F18 ids=S052`, the census run, and the junk-twin rejection — none of these were run or edited by this seat.
- Any jj/git mutation or commit; any write outside the lane; any network capture (the capture and manifest are ExecC2Capture's bytes; this seat only read them, plus one independent 404/200 URL probe whose bodies stayed in scratch and were deleted).

### R9 — limits of this receipt

- I did not re-fetch the feed to test freshness beyond the one README-level 404/200 probe; `verified-at` in the entry is the writing date, not the fetch instant (the manifest's `fetched_utc` is).
- The entry has not been reviewed by RevEntryF18 or mutation-tested by MutC2Entry-2 at the time this receipt was written; I notified both that the bytes are final at the path above.
- The Q1–Q10 mapping above is my own reading; the non-author reviewer's verdict is the one that counts for admission.

### R10 — scratch and tooling

- Scratch root: `/fast/scratch/hyaku/kasegi-r35/ScribeEntryF18/` — created, used for two independent feed fetches (JSON/CSV probes), the local capture simulations and the verification script; **removed before this receipt was filed** (`rm -rf --` executed; `ls` of the parent afterwards showed no seat directory).
- No tool installed or upgraded; no pacman transaction attempted.

### R11 — post-filing note (appended after the row landed; R8 item 1 superseded)

`ScribeSOURCESRow-2` and `ExecRegistryAppend-3` landed the S052 row while this seat was closing: `corpus/SOURCES.md:58` now reads `| S052 | CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | dataset | A | …`, and `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` prints `52`. The row URL is byte-identical to the entry's `source:` URL (`sed -n '3p' corpus/knowledge/cisa-kev-catalog.md`), so the entry/row pair agrees; R8 item 1 above is therefore closed by other seats, not by this one, and the frontier row, harness, census and junk-twin items remain out of scope.

The 341 → 340 reconciliation is explained by `ScribeSOURCESRow-2`: a bare-token `grep '22-01'` also matches inside `CVE-2022-0185` (the id string contains `22-01`), whose `requiredAction` carries no directive. The reusable trap for the lesson scribe: count `BOD 22-01`, never the bare token `22-01`; the row and this entry both use 340 records / 139 records, and neither cites 341 or 277 as a row count.

### R12 — L1 steer implemented: BOD 26-04 as current, BOD 22-01 revoked (entry bytes changed)

Steer received after the first filing: cite BOD 26-04 as the current directive binding the KEV remediation clock and state that BOD 22-01 is revoked, verified on the live page with a ≤25-word located quote.

Live-page read (2026-10-26, instrument UA, no capture committed):

```
$ curl -sS -L -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' -o bod2604.html https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk
status=200 final=https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk bytes=84350 type=text/html; charset=utf-8
```

Text extraction (script tags removed, block tags to newlines, entities decoded, 242 lines) located the following, each quoted verbatim and each `occurrences=1` in the normalized live text:

| entry location | quote | words | live line/section |
|---|---|---|---|
| Claim 4b | `A Binding Operational Directive is a compulsory direction to federal, executive branch, departments, and agencies` | 15 | L92, page introduction |
| Claim 4b | `BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked)` | 11 | L208, "Related Directives" |
| Claim 4b | `The text “& forensic triage” means that the agency must complete remediation or mitigation action within the timeline (three days)` | 20 | L179, "Appendix A: Vulnerability Response Timeline" |
| Claim 4b | `The timelines defined in Table 1 begin when either (1) CISA adds the vulnerability to the KEV Catalog` | 18 | L181, Appendix A |
| Claim 4b prose | `shall remediate vulnerabilities based on the timelines detailed in Table 1` | 11 | L169, Appendix A |
| Claim 4b prose | `Asset Exposure: Is the vulnerable asset publicly exposed?` | 8 | L98, the four risk variables |
| Claim 4b prose | `is similar to the Common Vulnerability Scoring System (CVSS) base score’s concept` | 12 | L171, Appendix A |

The four risk variables are quoted/named at L98-L101 (Asset Exposure, KEV Status, Exploit Automation, Technical Impact); KEV status is stated as one input, not the whole ranking, and the three-day figure is attributed only to the "& forensic triage" case (L179), not to every KEV record. `BOD 22-01` is stated as revoked (L208), and Claim 4 was amended so the 340 capture rows naming it are labelled legacy field text.

Re-check added as **FC-12** (a network command, unlike the pinned S052 assertions), tested today:

```
$ curl -sSL -A 'kasegi-shokunin/1.0 (documentation capture)' <page> | python3 -c '<extract+collapse>'
revoked 1 compulsory 1 three_days 1 evolves 1
```

Re-verified after the edit: `source-recheck --source S052` still prints `sha256 OK` + Q1-Q5 `occurrences=1` (anchors 2/3/4/15472/19165), exit 0; `bash -n` on the `recheck:` line exit 0; entry now 117 lines, 16,995 bytes, sha256 `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74`.

**Provenance gap, stated rather than hidden.** The BOD 26-04 page is CISA tier A but has **no registry row** (registry is frozen at 52, C2 kill rule `registry rows != 52`) and **no `corpus/source-snapshots/` capture**; its quotes are therefore located by section heading plus extraction line and re-checked live by FC-12, not pinned by `source-recheck`. The entry's Scope section says exactly this. Minimal repair for a later round: register one row for the directive page and capture it under that row, then move Claim 4b's quotes into a manifest record — doing it this round would break the frozen C2 registry literal, which is the L1's call, not this seat's. Header Q1 trio remains S052-only and unchanged; the directive URL appears only in Claim 4b's body provenance.

### R13 — mutation report received; M3 anchor gap closed at the entry's evidence layer (entry bytes changed again)

`MutC2Entry-2` reported six mutants on the steered bytes: M1 (drop `source: S052`) KILLED by the harness (`problems=no-source-line`), M2a (paraphrase the manifest Q1 quote) KILLED by both detectors, M4 (unregistered `--source S051`) KILLED by three harness limbs; **M3 SURVIVED** (Q4 anchor retargeted 15472 → 19165, `source-recheck` exits 0 because its anchor limb is fatal only when `occurrences>1`), **M2b SURVIVED** (paraphrase of the entry's rendered pinned quote — no detector compares entry text with the manifest), **M2c SURVIVED** (Claim 4b live-page quote paraphrase, the disclosed gap, not counted against the pinned tier).

Action taken in scope: **FC-13** added to the entry (anchor-verification check) and tested — pristine `anchors_ok 5 of 5`; a simulated M3 manifest (Q4 anchor → 19165) prints `anchors_ok 4 of 5`, so the entry now carries a check that fails on the mutant the instrument misses. The entry is 118 lines, 17,643 bytes, sha256 `e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730`; `source-recheck --source S052` exit 0, `bash -n` exit 0, FC-13 `anchors_ok 5 of 5`.

Not fixed here, because it is a lane-instrument change rather than an entry edit: **M2b** (nothing compares an entry's rendered quotes to its manifest) and **M3's instrument form** (`source-recheck` anchor limb unexercised on all-exactly-once manifests). Both are regression-test findings for the instrument owner/L1; FC-13 only closes M3 at this entry's evidence layer. **M2c** stays a disclosed provenance gap with the R12 repair (a row + capture for the directive page).

Re-run confirmation from `MutC2Entry-2` on the final digest `e3f233c0…`: FC-13 prints `anchors_ok 5 of 5` pristine, `4 of 5` on the M3 manifest and `4 of 5` on the M2a (paraphrase) manifest — so the check is redundant against both mutants, while `source-recheck` and the harness still exit 0 on M3 as recorded. M1/M2a/M4 killed; M2b/M2c survive at every automated layer (M2c disclosed). The tester measured the lane digests identical before and after its run.

### R14 — non-author reviewer REFUSED on Q2; Claim 4b demoted per their option (2)

`RevEntryF18` refused admission on Q2 only: Claim 4b's live-page quotes had no registry row and no pinned bytes in the lane, so the load-bearing dependency (Claim 4's tail) rested on an unregistered source. They offered two repairs: (1) register a tier-A row plus capture this round and bind the 4b assertions; (2) demote 4b to a Scope note and reword Claim 4 to what S052 alone supports. They also flagged two minors: header "first record L8-L21" should be L7-L22 (braces at L7/L22), and the old Scope phrasing "is tier A but has no registry row" was self-contradictory.

Applied repair (2), because repair (1) is not this seat's to make: a new registry row would take `corpus/SOURCES.md` from 52 to 53 rows and fail the frozen C2 literal `registry rows != 52`; the row block is ExecRegistryAppend-3's, and any row addition needs an L1 claim erratum, not a scribe edit. Changes:

- Removed the `## Claim 4b` section (header, provenance paragraph, four blockquotes, closing analysis).
- Claim 4 now ends on S052 alone: 340 `requiredAction` values cite BOD 22-01, 139 cite BOD 26-04, "these bytes establish neither directive's status nor its force, and no claim in this entry depends on one."
- The directive status moved to a single Scope bullet explicitly labelled **not an admitted claim (Q2)**, carrying the page URL, read date, HTTP/size, section headings and extraction lines L208 (BOD 22-01 revoked), L92 (compulsory direction), L179 (three days, "& forensic triage" case only), and the sentence "**no claim above rests on them**"; the bullet names the row+capture repair that would let a later round admit it.
- FC-12 reworded to point at the Scope note, not "Claim 4b"; FC-13 and all other checks unchanged.
- Header L3 fixed to `first record L7-L22`; the self-contradictory phrasing removed with the old bullet.

Verification after the edit: entry **91 lines, 15,831 bytes, sha256 `e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761`**; `source-recheck --source S052` exit 0 (`sha256 OK`, Q1-Q5 `occurrences=1`, anchors 2/3/4/15472/19165); `bash -n` on the recheck line exit 0; S052 quote counts unchanged (title 1, count 1, Q4 1, Q5 1, FCEB 2, BOD 22-01 327); the three Scope-note quotes re-measured on a fresh live read (HTTP 200, 84,350 bytes) at `occurrences=1` each. No `Claim 4b` reference remains (`grep -n '4b'` exit 1). L1 notified that the L1 steer's content now lives as a labelled note rather than an admitted claim, and that making it a claim requires the row+capture plus a C2 erratum they own.

**Reviewer verdict on the repaired bytes: ADMIT.** `RevEntryF18` re-verified digest `e9de994d…` (91 lines, 15,831 B): `grep '4b'` exit 1; Q2 PASS because the dependency is severed and every claim rests on tier-A S052; the Scope note at L89 is correctly labelled with "no claim above rests on them" and the row+capture repair named; L3 `first record L7-L22` byte-exact and agrees with the row; six blockquotes re-counted 1/1/1/1 (three via declared whitespace normalization), FCEB=2 anchored, BOD=327 anchored; `recheck` exit 0 in-lane and from a foreign cwd; Q6 sweep clean. Their receipt §7 carries the full re-check log, and they endorsed the frozen-C2-registry=52 reasoning for the lesson if the L1 wants it.


