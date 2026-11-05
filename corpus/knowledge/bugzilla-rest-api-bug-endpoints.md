# Bugzilla REST API core v1 bug endpoints: the machine interface for getting, creating and updating a bug

source: S107 — https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html — capture corpus/source-snapshots/round-72/S107.txt (1176 lines, 31435 snapshot bytes, sha256 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652, fetched 2026-11-05T03:49:50Z, HTTP 200; manifest corpus/source-snapshots/round-72/manifest.json)
verified-at: 2026-11-05
ground: F50 — the Bugzilla REST API core v1 bug endpoints: the route and method of get, create and update; the create parameter contract; the update comment object; and the access sentences on CC-list members and the reporter.
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-72/manifest.json --source S107

## Attribution

This is one tracker's own reference for its REST API bug endpoints (the Bugzilla project's documentation of core v1). Every statement below is the page's declared contract. This entry is documentation only: it instructs no call against any Bugzilla instance, and it does not say what any receiving team does with a report. The page introduces the section: "The REST API for creating, changing, and getting the details of bugs." (S107.txt:33).

## Claim 1 — three routes on one resource, and the method that names each

The page's create request is "To create a new bug in Bugzilla." (S107.txt:648), written as "POST /rest/bug" (S107.txt:649). The update request is "PUT /rest/bug/(id_or_alias)" (S107.txt:797). Falsifiable rule: a create is a POST to the collection path `/rest/bug`; an update is a PUT to the single-bug path. A get route is also named in the section; the create and update routes are the two write routes this entry covers.

## Claim 2 — create: the page states a required-parameter mechanism and a defaulted-parameter mechanism

The page states "Some params must be set, or an error will be thrown. These params are" (S107.txt:660) and then marks them in bold. The bold marking is lost in the tag-stripped capture, so this entry does not list which create parameters are required. It states the mechanism only. The page also advises "Bugzillas should always set both the params marked required and those" (S107.txt:666), continued by "marked (defaulted), because some Bugzillas may not have defaults set" in the same paragraph. Falsifiable rule: a client that sets both the required and the defaulted parameters is the page's own recommended form.

A successful create returns the new bug's id: "This is the ID of the newly-filed bug." (S107.txt:791).

## Claim 3 — update: the comment object is a field of the update request

The update's comment field is "A comment on the change. The object may contain" (S107.txt:886). Falsifiable rule: the only comment-write surface this page states is the `comment` object of the update request (S107.txt:886–895). The page refers to a "Create Comments" route by name (S107.txt:890) and states no method or fields for it on this page.

The response of an update does not report every write: "Currently, some fields are not tracked in changes: comment," (S107.txt:1166), continued "comment_is_private, and work_time. This means that they will not" (S107.txt:1167), and "show up in the return value even if they were successfully updated." (S107.txt:1168). Falsifiable rule: a comment written through an update is not echoed in the update's response.

## Claim 4 — groups and access: the page states per-field sentences, not a security-group rule

The create groups field: "An array of group names to put this bug into. You" (S107.txt:726). A bug is "added into all the groups that are set as being" (S107.txt:731) defaults for the product. The CC list may reach a bug "Whether or not users in the CC list are allowed" (S107.txt:881) to access it "to access the bug, even if they aren’t in a group" (S107.txt:882), "that can normally access the bug." (S107.txt:883). The reporter is covered by the parallel sentence: "Whether or not the bug’s reporter is allowed" (S107.txt:1002), "to access the bug, even if they aren’t in a group" (S107.txt:1003).

Falsifiable rule: the page's access sentences let a CC-list member or the reporter reach a bug "even if they aren’t in a group" that can normally access it. They state no key requirement.

## Claim 5 — the page's own stability caveat

"anything undocumented here may likely change in the" (S107.txt:645), continued "future." (S107.txt:646). Falsifiable rule: any field not named on this page is outside the contract this entry records.

## Distinctness

- F36 / S087 (GitHub repository security advisories REST API): a different tracker's routes, permission sets and status codes. No route, field or permission of this page is GitHub's.
- F47 / S103 (GitHub global security advisories REST API): a read interface over an advisory database. This page is a write-and-read interface over one bug tracker's bugs.
- F26, F28, F29, F48: policies, reporting channels and database curation. No overlap with the endpoint contract recorded here.

## Limits

The page does not establish, and this entry does not claim:

- an authentication or API-key requirement. Measured on the capture: `grep -n -i 'api_key\|api key\|authentication' S107.txt` returns no sentence stating either; the only token statement is the per-bug update token, "The token that you would have to pass to the" (S107.txt:297), tied to "process_bug.cgi page in order to update this" (S107.txt:298). That is a per-bug token on the web form, not an API credential, and the page does not state a key rule for the REST routes. The api_key clause of this round's frozen C2 target is therefore not grounded in S107 (see the round-72 report).
- a security-group rule that keeps a report private. The capture has no sentence naming security (`grep -n -i secur S107.txt` returns nothing). The access sentences are the ones in Claim 4.
- a receiving team's triage, acceptance, or response policy. The only assignment sentence is a parameter description: "A user to assign this bug to, if you don’t want it" (S107.txt:715), continued "to be assigned to the component owner." (S107.txt:716).
- which create parameters are required (Claim 2): the bold marking is absent from the tag-stripped capture.
- the body of the page's "Comments" section, which the table of contents lists but the capture does not reproduce. The Create Comments and Get Comments routes are not described here.
- the state of any live Bugzilla instance or its default configuration. The page says "Some parameters can have defaults set in Bugzilla, by the administrator." (S107.txt:662) and gives no default value.
- stability across rounds. The URL sits on the `latest` documentation track; the pinned sha256 is the round-72 authority. A changed page re-fails the capture rather than silently changing the entry.
