# K72AttackF50 — attack on C2 (frontier F50, Bugzilla REST API core v1 on S107)

Round 72 w1, read-only seat. No git/jj mutation run anywhere; no writes outside this
report and scratch `/fast/scratch/hyaku/kasegi-r72/K72AttackF50` (created with
`mkdir -p`, nothing cited from it). No tool installs (operator tooling authorization
not exercised). No network fetch performed: my item names no URL to open, and the
frozen capture bytes are the object under test.

Frozen wording under attack: `.ufo/waves/round-72/claims.json` C2 — target
"frontier F50: the Bugzilla REST API core v1 bug endpoints — the report channel's
machine interface (create/update a bug, add a comment, the api_key and
mandatory-field contract, the security-group restriction that keeps a report
private)", `sourced_claim` "C2 rests on S107, opened and captured this round".

## 1) Capture identity and git status

```
sha256sum corpus/source-snapshots/round-72/S107.txt
-> 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652   (matches the item pin)
wc -l  corpus/source-snapshots/round-72/S107.txt -> 1176
grep -c '' corpus/source-snapshots/round-72/S107.txt -> 1176          (newline-agnostic recount: same)
```

`manifest.json` is present beside the capture (2417 B) with one record S107
(url https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html, HTTP 200,
fetched_utc 2026-11-05T03:49:50Z, same sha256, lines 1176) and 8 pinned quotes
Q01–Q08. All 8 anchors verified at their stated lines by `grep -n` on the capture:
Q01 :645, Q02 :648, Q03 :649, Q04 :660, Q05 :666, Q06 :726, Q07 :797, Q08 :886.

Git status (all read-only):

```
git -C kasegi-shokunin rev-parse HEAD
-> a34ce4c146b669ea8038da32ba47d7ca3b36ea43        (lane is at the freeze commit)
git -C kasegi-shokunin status --porcelain -- corpus/source-snapshots/round-72/
-> ?? corpus/source-snapshots/round-72/            (whole dir untracked)
git -C kasegi-shokunin ls-files -- corpus/source-snapshots/round-72/
-> (empty)
git -C kasegi-shokunin show a34ce4c:corpus/source-snapshots/round-72/S107.txt
-> fatal: path ... exists on disk, but not in 'a34ce4c'
```

So the capture (and manifest) are NOT in the freeze commit; the sha I verified is the
working-tree bytes. This matches the claim's own wording ("opened and captured this
round"), and QUALITY.md R105 (:528) requires capture + manifest to land in the same
commit at admission — both files are present together in the untracked dir, so the
R105 precondition can still be met at integration. Residual, not a defect today.

## 2) Province scope — verdict: INSIDE

PROVINCE.md, line 3 (the sentence I rely on):

> `**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages`

Supported by :29-30 ("The line-3 domain comprises program rules, scopes, and claim
packages; the core also covers triage and claim gates, and submission/disclosure
packaging.") and :52 ("Live-target testing is refused; this corpus is documentation
only."). Adjacent siblings, :47-49: chousa — research method and source hierarchy;
kagi — secrets and vault handling; kake — web properties.

Reasoning: the S107 page is the machine interface a receiving team's bug tracker
exposes to file and update bug reports — the report channel's interface ground, the
same ground class the frontier already admits as F27 (kernel e-mail report channel),
F30 (CVE Services write path), F36/F47 (GitHub advisories REST interfaces). The
capture is documentation, not a live Bugzilla instance (no kake web property is
touched), asserts no research method (not chousa), and carries no secret-handling
material (not kagi — indeed the api_key clause is exactly the part with no capture
ground, §4). Not a reporting-channel policy: the capture contains no eligibility,
timeline, severity or reward language; it states methods, paths, parameters and
response objects.

## 3) Overlap with F26, F28, F29, F36, F47, F48 — verdict: NONE

Row locations measured in `corpus/README.md` (`grep -n '^\| F(26|28|29|36|47|48) |'`):
F26 :628, F28 :666, F29 :691, F36 :869, F47 :1087, F48 :1097.

- F26 :628 — Google Cloud VRP program scope and customer-resource testing boundary:
  a bounty-program policy, no tracker or API contract.
- F28 :666 — GitHub private vulnerability reporting, reporter flow (GitHub web flow,
  form fields): not a REST contract, not Bugzilla.
- F29 :691 — GitHub repository security advisories, maintainer-side lifecycle; the
  row/PROVINCE scope limit (:178) explicitly keeps "the REST API for repository
  security advisories" out of F29.
- F36 :869 — GitHub repository security advisories REST API: the nearest sibling
  (a create/update REST pair), but bound to GitHub advisory objects and its own
  twelve-endpoint route family; Bugzilla bug CRUD is a different product and surface.
- F47 :1087 — GitHub global security advisories REST API: read-only interface over
  the GitHub Advisory Database.
- F48 :1097 — GitHub Advisory Database curation semantics: database admission
  classes, no tracker interface.

Named list: none. Measured checks:

```
grep -ri 'bugzilla' corpus/knowledge/        -> no matches (0 files)
grep -ri 'bug.tracker|tracker.{0,40}REST|REST.{0,40}tracker' corpus/knowledge/ -> no matches
grep -ri 'tracker|bugzilla' over the six entries cited above   -> no matches
```

No sentence in any cited entry covers Bugzilla or a generic bug-tracker REST API;
C2's "new primary source, new surface" is not contradicted by the cited rows.

## 4) Interface (REST contract), not policy — what the capture actually states

All quotes located by `grep -n` on `corpus/source-snapshots/round-72/S107.txt`
(capture line numbers; each quote under 25 words):

| Element | Located quote | Lines |
|---|---|---|
| Page subject | "The REST API for creating, changing, and getting the details of bugs." | :33 |
| Create endpoint | "To create a new bug in Bugzilla." + "POST /rest/bug" | :648-649 |
| Required-field mechanism | "Some params must be set, or an error will be thrown. These params are marked in bold." | :660-661 |
| Required vs defaulted | "Bugzillas should always set both the params marked required and those marked (defaulted)" | :666-667 |
| Required set (four non-(defaulted) rows) | product :674-676, component :677-679, summary :680-682, version :683-685 — no "(defaulted)" tag; first defaulted row is description :686ff | :674-685 |
| api_key requirement | **NOT STATED — zero occurrences** (evidence below) | — |
| Group restriction, create | "An array of group names to put this bug into." | :726 (+ :729-733 default-groups / empty-array rule) |
| Restriction semantics, read side | "even if they are not in the groups the bug is restricted to." | :222-223 and :237-238; response `groups` field :214-215 |
| Update endpoint | "PUT /rest/bug/(id_or_alias)" | :797 |
| Groups on update | "add (array) The names of groups to add." | :941-944 |
| Add a comment (update) | "A comment on the change. The object may contain" | :886-887; body :888-889; "is_private (boolean) Whether the comment is private" :892-895 |
| Description privacy (create) | "If set to true, the description is private" | :720-723 |
| Stability caveat | "anything undocumented here may likely change in the future." | :645-646 |

api_key evidence (measured):

```
grep -in 'api_key|API key|api key' S107.txt -> no matches
grep -in 'api|[Kk]ey|auth|token'   S107.txt -> only: nav headings :8-10/:29-30, the two
  "REST API" sentences :33-34, keywords/key fields (:106,:239-241,:801,:844,:949-965,
  :1122,:1157-1158), and update_token :295-300
```

The only credential-adjacent item in the capture is `update_token` (:295-300, "The
token that you would have to pass to the process_bug.cgi page") — a per-bug update
token, not an API key, and not an authentication requirement. The page's own nav
lists "6.1.1. General" (:10), where Bugzilla documents api_key authentication; that
page's content is NOT in this capture.

Caveats for the entry writer: (a) the required-field marking is typographic (bold)
and bold is stripped by the text capture, so the capture grounds the requirement
mechanism (:660-661) plus the four non-(defaulted) rows (:674-685), not the bold
marks themselves; (b) "keeps a report private" is the claim's gloss — the page's own
located words are group restriction (:222-223, :237-238) and per-comment/description
privacy (:720-723, :892-895); the entry must quote the page's words.

## 5) Verdict

`C2 attack: FALSIFIED on frozen wording`

- Single falsifier: the frozen C2 target clause "the api_key and mandatory-field
  contract" (`.ufo/waves/round-72/claims.json`, C2.target). S107 states no api_key
  requirement anywhere (0 occurrences, §4). Since `sourced_claim` says "C2 rests on
  S107" (singular source), an F50 entry grounding that clause in S107 cannot locate
  the quote, tripping C2's own kill_rule ("if any quote in the entry is not located
  in the capture"). The clause has no ground in the frozen source set.
- Scope limb: holds — INSIDE the province (§2).
- Overlap limb: holds — NONE with F26/F28/F29/F36/F47/F48 or their entries (§3).
- Ground limb: holds for the create endpoint and its required-field contract
  (:648-649, :660-669, :674-685), the group/security-restriction field
  (:214-215, :222-223, :237-238, :726-733, :941-944), the update endpoint (:797) and
  add-a-comment (:886-895); fails only for the api_key clause.
- Repair path (recommendation only — the planner seat's call, not mine): narrow the
  frozen target by dropping the api_key clause — every other named element is
  grounded in S107 — or admit the Bugzilla "6.1.1 General" page as a second source
  before entry-writing.

## Residual risk and verification gaps

- The capture and manifest are untracked at a34ce4c; my verification is against the
  working-tree bytes whose sha matches the item pin. At integration, capture +
  manifest must land in the admission commit (QUALITY.md R105, :528), or the frozen
  hash is the only pin on those bytes.
- No live re-open of the URL was performed this seat (my item names no fetch; the
  manifest's HTTP 200 record of 2026-11-05T03:49:50Z is taken as recorded). Capture
  fidelity vs. the live page is unverified by me.
- The bold marking loss (§4 caveat a) is a property of `--kind html` text
  normalization; whether the round's rules accept "required set = the non-(defaulted)
  rows" as grounding is a gate/judge question I do not decide.
