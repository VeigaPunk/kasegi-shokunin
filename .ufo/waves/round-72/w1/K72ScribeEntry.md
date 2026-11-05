# K72ScribeEntry — round-72 F50 drafts (scribe, leaf)

Status: drafts complete. Nothing written into the lane; no git/jj run; no gate run (not assigned to this seat); no tools installed. Scratch `/fast/scratch/hyaku/kasegi-r72/K72ScribeEntry` created for the quote-locator run and removed before yield.

## 1. Measured facts (commands and observed output)

- `sha256sum corpus/source-snapshots/round-72/S107.txt; wc -l …` → `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652` and `1176`. Digest matches the seat's `0b944ea1…` prefix.
- `corpus/source-snapshots/round-72/manifest.json` S107 entry: url and capture_url `https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html`; `http.status` 200; `fetched_utc` `2026-11-05T03:49:50Z`; `bytes` 31435; `lines` 1176; `fetch_method` "capture-source.py --kind html, … (tags stripped, entities decoded, whitespace collapsed per line)". Pins Q01–Q08 at anchors 645, 648, 649, 660, 666, 726, 797, 886.
- `grep -n -i 'api' S107.txt` → lines 8, 9, 29, 30, 33, 34 — generic "API" heading and "REST API" text only.
- `grep -n -i 'key' S107.txt` → 21 lines (106, 156, 169, 188, 239, 241, 266, 801, 844, 900, 949, 951, 953, 955, 957, 959, 961, 963, 1122, 1157, 1158), all "keys", "keyword(s)" or "two keys". No `api_key`, no `api key`.
- `grep -n -i 'secur' S107.txt` → no output (exit 1). No "security" and no "security group" line.
- `grep -n -i -E 'auth|login|token' S107.txt` → no `auth` line. Hits are "login name" fields (151, 163, 183, 261, 341, 370, 374, 460, 524, 538, 616, 777, 847, 999, 1105) and `update_token` (295, 297, 299).
- `grep -c '\*\*' S107.txt` → 0. The capture carries no bold markup, consistent with the tag-stripped fetch method.
- `grep -n -i 'group' S107.txt` → group sentences at 724–734 (create), 936–948 and 985–991 (update, product move), 882/1003 ("aren’t in a group"). No "security group".
- `grep -n -i 'comment' S107.txt` → 21 (`6.1.7. Comments` in the TOC), 720–723 (create `comment_is_private`), 884–910 (update `comment` and `comment_is_private` objects), 1151, 1166–1167 (fields not tracked in `changes`).
- `grep -ri 'bugzilla'` over `corpus/knowledge`, `corpus/README.md`, `corpus/SOURCES.md` (case-insensitive) → one hit: `corpus/SOURCES.md:211` (a Mozilla advisory note, "Bugzilla id"). No Bugzilla knowledge entry exists in the lane.
- `grep -n 'S107' corpus/SOURCES.md` / `'| S107 |' in SOURCES.md` → False. S107 is not yet a registry id.
- `corpus/instruments/source-recheck.py` exists (True).
- `PROVINCE.md` (repo root, not `corpus/`): 29968 bytes; last non-empty line 215 is the `[r71 Frontier amendment, appended 2026-11-05] F49 - …` line; file ends with a newline; 216 `split` pieces with the empty last one.
- Quote locator (Python, read-only, against `S107.txt`): 98 fragments checked in three runs (65 + 13 + 20). All 98 located at the stated line with `frag in lines[n-1]`; none ≥ 25 words (longest 17); 0 misses. The table in §3.2 lists the 71 fragments the drafts use.

## 2. Findings

- **F-1 — the `api_key` and security-group statements the seat asked for do not exist in S107.** The capture has no `api_key`, `api key`, `security` or `authentication` sentence (§1 greps). The entry records this as a scope limit (Limits, bullet 4 and 5) and does not invent one. The only token statement is `update_token` (S107.txt:297–299), which the page ties to `process_bug.cgi`, not to the REST route.
- **F-2 — the create required set cannot be established from this capture.** The page says "Some params must be set, or an error will be thrown. These params are" / "marked in bold." (S107.txt:660–661). The capture is tag-stripped (manifest `fetch_method`) and has zero bold markers, so the entry states no required set. The frontier row's `next` cell routes this to the L1 or to a rendered capture.
- **F-3 — no add-comment route is in the capture.** The TOC lists `6.1.7. Comments` (S107.txt:21), but the capture holds no body for that section. The update's comment object refers to "Create Comments" (S107.txt:890) and "Get Comments" (S107.txt:903) by name only. The entry states the `comment` object of the update request as the only comment-write surface the page states.
- **F-4 — the manifest pins only 8 of the 71 fragments the entry uses.** The recheck command verifies only pinned quotes. Pins needed for the recheck to cover the entry: every fragment in §3.2. The L1 adds them to `manifest.json` before running `source-recheck.py`.
- **F-5 — PROVINCE bracket form diverges from r71.** I used the seat's literal bracket `[r72 Frontier amendment, appended 2026-11-05, end-of-file append per R6]` with an em dash. The r71 line reads `[r71 Frontier amendment, appended 2026-11-05] F49 - …` (hyphen, no "end-of-file" token). The L1 chooses the form; the draft follows the seat's literal.
- **F-6 — recheck tier is my judgment.** I set the registry `recheck` to `90d`. The URL sits on the `latest` track, which is the rationale the S087 entry gives for its 90d row. The seat did not fix the value.
- **F-7 — live URL.** The capture's own heading reads "6.1.3. Bugs — Bugzilla 5.2+ documentation" (S107.txt:1). The `latest` track may move; the pinned sha256 is the round-72 authority, and a changed page re-fails the capture.
- **F-8 — no lane change needed beyond the L1's copy.** I wrote only this report. The drafts below are for the L1 to copy into the lane.

## 3. Drafts

### 3.1 Knowledge entry — `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md`

```markdown
# Bugzilla REST API core v1 bug endpoints — the machine interface contract for getting, creating and updating a bug, and the comment object of the update request, with the page's own scope limit

source: S107 — https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html — capture corpus/source-snapshots/round-72/S107.txt (1176 lines, 31435 bytes; sha256 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652; recorded fetch 2026-11-05T03:49:50Z, HTTP 200, tags stripped by capture-source.py --kind html); manifest corpus/source-snapshots/round-72/manifest.json (pins Q01-Q08 at this draft; the L1 pins every further quote this entry cites before the recheck runs)
verified-at: 2026-11-05 (opened this round; the URL sits on Bugzilla's `latest` documentation track, so the 90d row recheck re-fetches and a changed sha re-fails the capture; the pinned sha256 is the round-72 authority, not the URL's stability)
ground: F50
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-72/manifest.json --source S107

## Attribution

This is Bugzilla's own REST API reference for the core v1 bug endpoints, speaking as one tracker's machine-interface contract: the route, the method, the parameter contract and the response of get, create and update. Every statement here is the page's declared contract, and this entry is documentation-only: it instructs no call against any Bugzilla instance. The capture's heading reads "6.1.3. Bugs — Bugzilla 5.2+ documentation" (S107.txt:1). The page's own disclaimer is "anything undocumented here may likely change in the" (S107.txt:645), continued "future." (S107.txt:646). The GitHub repository-advisories REST API of F36 is a different tracker's contract and is not this page.

## Claim 1 — the bug section names three routes on one resource: get, create and update

The section opens "The REST API for creating, changing, and getting the details of bugs." (S107.txt:33). Get is `GET /rest/bug/(id_or_alias)` (S107.txt:40), whose parameter is typed `mixed` (S107.txt:48) and described "An integer bug ID or a bug alias string." (S107.txt:49). Create is `POST /rest/bug` (S107.txt:649), introduced "To create a new bug in Bugzilla." (S107.txt:648). Update is `PUT /rest/bug/(id_or_alias)` (S107.txt:797), described "Allows you to update the fields of a bug. Automatically sends emails" (S107.txt:793), continued "out about the changes." (S107.txt:794).

Falsifiable rule: a create request is a POST to the collection route `/rest/bug`; an update request is a PUT to the single-bug route, and the bug may be named in the path, in the `ids` parameter, or both: "either in the URL path and/or in the ids param. You can use both and they" (S107.txt:807). Rejected over-generalization: the page states no authentication or key requirement on any route (see Limits).

## Claim 2 — create: the page names required and defaulted parameters, and the capture cannot show which are required

The contract is stated as "Some params must be set, or an error will be thrown. These params are" (S107.txt:660), continued "marked in bold." (S107.txt:661). Defaults are stated as "Some parameters can have defaults set in Bugzilla, by the administrator." (S107.txt:662) and "If these parameters have defaults set, you can omit them. These parameters" (S107.txt:663), continued "are marked (defaulted)." (S107.txt:664). The page advises "Bugzillas should always set both the params marked required and those" (S107.txt:666).

The parameters the page describes, quoted as written:
- product: "The name of the product the bug is being filed" / "against." (S107.txt:675–676)
- component: "The name of a component in the product above." (S107.txt:679)
- summary: "A brief description of the bug being filed." (S107.txt:682)
- version: "A version of the product above; the version the" / "bug was found in." (S107.txt:685–686)
- description: "(defaulted) The initial description for this bug." (S107.txt:689)
- op_sys: "(defaulted) The operating system the bug was" (S107.txt:694)
- priority: "(defaulted) What order the bug will be fixed in by" (S107.txt:702)
- severity: "(defaulted) How severe the bug is." (S107.txt:707)

Falsifiable rule: the page makes omission of a (defaulted) parameter conditional on an administrator's default: "If these parameters have defaults set, you can omit them. These parameters" (S107.txt:663). Unknown or disallowed fields are handled as stated: "If you specify any fields you are not allowed to set, they will just be" (S107.txt:641), continued "set to their defaults or ignored." (S107.txt:642).

The response is `{ "id" : 12345 }` (S107.txt:784), with "This is the ID of the newly-filed bug." (S107.txt:791). Required set: the page marks it in bold (S107.txt:660–661); the capture is tag-stripped and holds no bold markup, so this entry states no required set (see Limits).

## Claim 3 — update: the PUT body carries the field set, a comment object and a privacy object, and the response does not track comments

The request modifies "The IDs or aliases of the bugs that you want to modify." (S107.txt:817). "All following fields specify the values you want to set on the bugs you are" (S107.txt:818), continued "updating." (S107.txt:819).

The comment object is "A comment on the change. The object may contain" (S107.txt:886), with "body (string) The actual text of the" (S107.txt:888), "is_private (boolean) Whether the comment is" (S107.txt:892) and "private or not. If you try to make a comment" (S107.txt:893), continued "and you don’t have the permission to," (S107.txt:894) and "an error will be thrown." (S107.txt:895). Privacy of comments already on the bug is a separate object: "This is how you update the privacy of comments" (S107.txt:898), keyed "where the keys are the int ID of comments" (S107.txt:900).

The response reports changes for tracked fields only: "Currently, some fields are not tracked in changes: comment," (S107.txt:1166), continued "comment_is_private, and work_time. This means that they will not" (S107.txt:1167) and "show up in the return value even if they were successfully updated." (S107.txt:1168).

Falsifiable rule: a comment written by an update does not appear in the response, even when the write succeeded (S107.txt:1166–1168).

## Claim 4 — add comment: no standalone comment route is stated; the comment is a field of the update request

The table of contents lists "6.1.7. Comments" (S107.txt:21), but the capture holds no body for that section; its last section is the update-bug section, followed by the page footer. The comment object names a separate route only by reference: "to Create Comments, you can also call" (S107.txt:890). The privacy object refers to comment IDs "as returned by" / "Get Comments and the value is a" (S107.txt:902–903).

Falsifiable rule: the only comment-write surface this page states is the `comment` object of the update request (S107.txt:886–895); a comment added through this page is part of a PUT to `/rest/bug/(id_or_alias)` (S107.txt:797). Rejected over-generalization: the Create Comments route, its method and its fields are named here only in a cross-reference and are not in the capture; no add-comment route, method or required field is stated.

## Claim 5 — access and groups: the page states per-field group and access sentences; it states no security-group or api_key sentence

The create groups field reads "An array of group names to put this bug into. You" (S107.txt:726), continued "can see valid group names on the Permissions tab of" (S107.txt:727). The default is stated "added into all the groups that are set as being" (S107.txt:731), continued "“Default” for this product. (If you want to avoid" (S107.txt:732), "that, you should specify groups as an empty" (S107.txt:733) and "array.)" (S107.txt:734). The update's groups object takes an add list: "add (array) The names of groups to add." (S107.txt:941).

The access flags: for the CC list, "Whether or not users in the CC list are allowed" (S107.txt:881), "to access the bug, even if they aren’t in a group" (S107.txt:882), "that can normally access the bug." (S107.txt:883). For the reporter, "Whether or not the bug’s reporter is allowed" (S107.txt:1002), "to access the bug, even if they aren’t in a group" (S107.txt:1003), "that can normally access the bug." (S107.txt:1004).

Falsifiable rule: the access sentences state that a CC-list member or the reporter may reach a bug "even if they aren’t in a group" that can normally access it. They state no key requirement and no security-group requirement.

## Distinctness

- vs F36/S087 (GitHub repository security advisories REST API): a different tracker's routes, permission sets and status codes; no route or field of this page is GitHub's.
- vs F48/S105 (GitHub Advisory Database curation): an advisory database's semantics, not an API surface; no claim overlaps.

## Limits

The page does not establish, and this entry does not claim:

- a receiving team's triage, acceptance or response policy. The capture has no such sentence; the only assignment statement is a parameter description: "A user to assign this bug to, if you don’t want it" (S107.txt:715), continued "to be assigned to the component owner." (S107.txt:716).
- any Bugzilla instance's configuration, or Bugzilla's default configuration: "Some parameters can have defaults set in Bugzilla, by the administrator." (S107.txt:662); "Some Bugzillas may treat your arguments case-sensitively, depending" (S107.txt:504), continued "on what database system they are using. Most commonly, though, Bugzilla is" (S107.txt:505). The page gives no default value for any named parameter.
- which create parameters are required (Claim 2): the page marks them in bold (S107.txt:660–661), and the tag-stripped capture carries no bold markup.
- an api_key or authentication statement. A case-insensitive search of the capture finds no "api_key", "api key", "security" or "authentication" sentence. The only token statement concerns `update_token`, which the page ties to the process_bug.cgi page: "The token that you would have to pass to the" (S107.txt:297), continued "process_bug.cgi page in order to update this" (S107.txt:298) and "bug. This changes every time the bug is updated." (S107.txt:299).
- a security-group statement. The capture has none; the group sentences are those in Claim 5.
- the body of the Comments section (S107.txt:21). It is not in the capture, so the Create Comments and Get Comments routes are not described here.
- stability: "anything undocumented here may likely change in the" (S107.txt:645), continued "future." (S107.txt:646). The URL is the `latest` track, so cross-round stability is not asserted; the 90d row recheck re-fetches.
```

### 3.2 Quote-line table (every fragment the drafts use, located in S107.txt)

Each fragment is a byte-exact substring of the named line. Multi-line sentences list each segment; "/" marks a line break in the capture, not a character in the quote. Max fragment length 17 words (measured).

```
L1     6.1.3. Bugs — Bugzilla 5.2+ documentation
L21    6.1.7. Comments
L33    The REST API for creating, changing, and getting the details of bugs.
L40    GET /rest/bug/(id_or_alias)
L48    mixed
L49    An integer bug ID or a bug alias string.
L504   Some Bugzillas may treat your arguments case-sensitively, depending
L505   on what database system they are using. Most commonly, though, Bugzilla is
L641   If you specify any fields you are not allowed to set, they will just be
L642   set to their defaults or ignored.
L645   anything undocumented here may likely change in the   (substring of L645 "here, but realize that anything undocumented here may likely change in the")
L646   future.
L648   To create a new bug in Bugzilla.
L649   POST /rest/bug
L660   Some params must be set, or an error will be thrown. These params are
L661   marked in bold.
L662   Some parameters can have defaults set in Bugzilla, by the administrator.
L663   If these parameters have defaults set, you can omit them. These parameters
L664   are marked (defaulted).
L666   Bugzillas should always set both the params marked required and those
L675   The name of the product the bug is being filed / L676 against.
L679   The name of a component in the product above.
L682   A brief description of the bug being filed.
L685   A version of the product above; the version the / L686 bug was found in.
L689   (defaulted) The initial description for this bug.
L694   (defaulted) The operating system the bug was
L702   (defaulted) What order the bug will be fixed in by
L707   (defaulted) How severe the bug is.
L715   A user to assign this bug to, if you don’t want it / L716 to be assigned to the component owner.
L726   An array of group names to put this bug into. You / L727 can see valid group names on the Permissions tab of
L731   added into all the groups that are set as being / L732 “Default” for this product. (If you want to avoid / L733 that, you should specify groups as an empty / L734 array.)
L784   "id" : 12345
L791   This is the ID of the newly-filed bug.
L793   Allows you to update the fields of a bug. Automatically sends emails / L794 out about the changes.
L797   PUT /rest/bug/(id_or_alias)
L807   either in the URL path and/or in the ids param. You can use both and they
L817   The IDs or aliases of the bugs that you want to modify.
L818   All following fields specify the values you want to set on the bugs you are / L819 updating.
L881   Whether or not users in the CC list are allowed / L882 to access the bug, even if they aren’t in a group / L883 that can normally access the bug.
L886   A comment on the change. The object may contain
L888   body (string) The actual text of the
L890   to Create Comments, you can also call
L892   is_private (boolean) Whether the comment is / L893 private or not. If you try to make a comment / L894 and you don’t have the permission to, / L895 an error will be thrown.
L898   This is how you update the privacy of comments
L900   where the keys are the int ID of comments
L902   their globally-unique ID, as returned by / L903 Get Comments and the value is a
L941   add (array) The names of groups to add.
L1002  Whether or not the bug’s reporter is allowed / L1003 to access the bug, even if they aren’t in a group / L1004 that can normally access the bug.
L1166  Currently, some fields are not tracked in changes: comment, / L1167 comment_is_private, and work_time. This means that they will not / L1168 show up in the return value even if they were successfully updated.
L297   The token that you would have to pass to the / L298 process_bug.cgi page in order to update this / L299 bug. This changes every time the bug is updated.
```

### 3.3 SOURCES registry row (11 columns; appended at the end of the Registry table, after the S106 row)

```
| S107 | Bugzilla 5.2+ documentation, REST API: Bugs (core v1), 6.1.3 (Bugzilla project) — https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html | docs | A | Bugzilla's own core v1 REST interface for getting, creating and updating a bug: the create parameter contract with its defaulted parameters, the groups, cc, access and comment fields of the create and update requests, and the comment object of the update request; not a receiving team's policy, not any installation's configuration, and not the Comments section body, which the capture does not hold | capture corpus/source-snapshots/round-72/S107.txt (sha256 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652, 1176 lines, 31435 bytes, fetched 2026-11-05T03:49:50Z, HTTP 200, tags stripped; manifest corpus/source-snapshots/round-72/manifest.json pins Q01-Q08 at anchors 645, 648, 649, 660, 666, 726, 797, 886) | Read a create request's required set from the page's bold markup, which the tag-stripped capture cannot show, and treat the comment object of the update request as the page's only comment-write statement | mined | 2026-11-05 | 90d | corpus/knowledge/bugzilla-rest-api-bug-endpoints.md |
```

Cell check: 11 cells; no literal or escaped pipe in any cell (the only `|` characters are the column separators).

### 3.4 README block — `corpus/README.md`, appended after the Round-71 block (after line 1133)

```markdown
## Round-72 admission — coverage map row and Frontier F50 (2026-11-05)

Appended amendment (R6): the round-72 entry `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` (Frontier F50, source S107) rests on Bugzilla's own "6.1.3. Bugs" page at https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html, captured `corpus/source-snapshots/round-72/S107.txt` (sha256 0b944ea1...4652, 1176 lines), manifest `corpus/source-snapshots/round-72/manifest.json`. The coverage map above is not edited in place (R6); the coverage-map row is appended here rather than inserted into the map, and the F50 frontier row is listed here on the same six-cell table shape as F48 and F49.

| Area | Entry | Source basis |
|---|---|---|
| Bugzilla REST API core v1 bug endpoints: get, create and update of a bug, and the comment object of the update request (round 72) | knowledge/bugzilla-rest-api-bug-endpoints.md | S107, Bugzilla's own bug-section statements, opened 2026-11-05 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F50 | Bugzilla's own REST API core v1 bug endpoints — GET /rest/bug/(id_or_alias), POST /rest/bug and PUT /rest/bug/(id_or_alias), the create parameter contract with its (defaulted) parameters, the groups, cc, access and comment fields of the create and update requests, and the comment object of the update request as the page's only comment-write statement | admitted | knowledge/bugzilla-rest-api-bug-endpoints.md | S107 | Read the create contract's required set from the page's bold markup only where a rendered capture carries it: the tag-stripped S107 capture does not (S107.txt:660-661 names the bold markers); the update's comment object sits at S107.txt:886-895, and no standalone add-comment route is in the capture. |

F50 adds Bugzilla's own statements on the core v1 bug endpoints, which the lane did not hold: a case-insensitive search of the knowledge set, the registry and this README finds no Bugzilla entry (the only match is a Mozilla advisory's "Bugzilla id" in the registry notes, SOURCES.md:211). The GitHub repository-advisories REST API of F36 is a different tracker's contract and is not affected. The page's bug-endpoint sentences are the admission basis; the create required set and the add-comment route are not established by the capture and are listed under the entry's Limits.
```

### 3.5 PROVINCE.md frontier amendment — append at end of file (after line 215, one blank line between)

```
[r72 Frontier amendment, appended 2026-11-05, end-of-file append per R6] F50 — Bugzilla's own REST API core v1 bug endpoints on its "6.1.3. Bugs" page (S107, https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html): GET /rest/bug/(id_or_alias), POST /rest/bug and PUT /rest/bug/(id_or_alias), the create parameter contract with its (defaulted) parameters, the groups, cc, access and comment fields, and the comment object of the update request; admitted on source S107 in corpus/knowledge/bugzilla-rest-api-bug-endpoints.md. Scope limit: one tracker's documented interface contract — not a receiving team's triage or response policy, not any Bugzilla instance's configuration, and not Bugzilla's default configuration; the capture cannot show which create parameters are required (its bold markup is stripped), states no api_key or security-group wording, and holds no body for the Comments section.
```

## 4. Items for the L1 (not done by this seat)

1. Copy §3.1 to `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md`, §3.3 into `corpus/SOURCES.md` after the S106 row, §3.4 after the Round-71 block at the end of `corpus/README.md`, §3.5 at the end of the repo-root `PROVINCE.md` (F-5 for the bracket form).
2. Extend `corpus/source-snapshots/round-72/manifest.json` to pin every fragment in §3.2 (F-4) before `source-recheck.py --source S107` is run.
3. The registry `recheck` value `90d` is my judgment (F-6).
4. Attack seats should check the Limits list against the capture: the absence claims in Limits and §1 are measured greps, not reading.
