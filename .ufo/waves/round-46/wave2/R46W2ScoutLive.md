VERDICT: HOLDS
seat: R46W2ScoutLive — S073 live drift, second look (kasegi round-46 wave 2, lane kasegi-shokunin)

Scope: re-capture the S073 page live, diff against the pinned capture, re-run the gated recheck on the committed bytes, and fetch the enablement page the F28 entry does not use to test for contradictions with entry sentences. Read-only seat: no edits anywhere except this Report file and scratch (scratch removed before yield).

# Findings

## F1 — S073 live re-capture is byte-identical to the pinned capture: zero drift on all 589 lines

Thing attacked: the pinned capture `corpus/source-snapshots/round-46/S073.txt` (manifest sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, 589 lines) as a live-fidelity claim, ~58 minutes after the pin.

Command:
```
TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S073 --url 'https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately' --out /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073.live.txt --kind html
```
Output (verbatim):
```
S073 status=200 fetched_bytes=577188 snapshot_bytes=15568 sha256=66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 utc=2026-10-28T23:54:27Z out=/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073.live.txt
```
Independent comparison (not trusting the receipt):
```
sha256sum /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073.live.txt /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt && wc -l -c <both files> && cmp <live> <committed> && echo CMP: byte-identical
```
Output (verbatim):
```
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073.live.txt
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt
  589 15568 /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073.live.txt
  589 15568 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt
 1178 31136 total
CMP: byte-identical
```
Drift: none — sha256, byte count, and line count all equal; `cmp` found no differing byte, so there are no drifted lines to name. Manifest `fetched_utc` was `2026-10-28T22:56:49Z`; re-capture `2026-10-28T23:54:27Z` (same UA/instrument).

Wave-2 tree binding: lane HEAD is `0d121a2` ("round-46: wave 2 spec (33 seats, policy v1) and dispatch"); `git merge-base --is-ancestor 5437afeaf9b642c267bba3c31f00ae701e49da68 HEAD` → ancestor (echoed `ANCESTRY: 5437afe-is-ancestor-of-HEAD`); `git show 5437afeaf9b642c267bba3c31f00ae701e49da68:corpus/source-snapshots/round-46/S073.txt | sha256sum` → `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  -`. Working-tree, wave-2-integrated-tree, and live bytes are all the same blob. `git status --porcelain=v1` over the three F28 files printed nothing (0 lines, clean).

## F2 — Gated recheck passes on the committed capture (exit 0, 8/8 anchored quotes)

Thing attacked: the entry's `recheck:` line (github-private-vulnerability-reporting.md:6).

Command:
```
TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/manifest.json --source S073
```
Output (verbatim):
```
S073:sha256 OK
S073:Q1 OK occurrences=1 anchor=560-ok
S073:Q2 OK occurrences=1 anchor=563-ok
S073:Q3 OK occurrences=1 anchor=564-ok
S073:Q4 OK occurrences=1 anchor=566-ok
S073:Q5 OK occurrences=1 anchor=573-ok
S073:Q6 OK occurrences=1 anchor=574-ok
S073:Q7 OK occurrences=1 anchor=577-ok
S073:Q8 OK occurrences=1 anchor=578-ok
```
`echo "exit=$?"` printed `exit=0`.

## F3 — Do-nothing control: the pipeline discriminates (one flipped byte is caught)

Thing built: proof that F1/F2 results are true negatives, not a vacuous pass. Control = copy of manifest + S073.txt in scratch with a single byte overwritten (`printf 'X' | dd of=control/S073.txt bs=1 seek=10000 conv=notrunc status=none`).

Output (verbatim):
```
--- cmp committed vs corrupted:
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/control/S073.txt differ: char 10001, line 454
--- recheck on corrupted copy:
S073:sha256 MISMATCH expected=66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 actual=9d9f4315d2f9e1e475a9a08caa9f0a9566ae9f6b1a7c0d7916895c81a0e6e156
exit=1
```
The identical comparator flags a 1-byte drift at line 454 and recheck exits 1; the committed capture passing is therefore informative.

## F4 — The not-used enablement page: captured live; no sentence of the F28 entry is contradicted

Thing attacked: the F28 entry's claim set vs the body of the page linked at `S073.txt:561`, resolved from the live page's own href (`/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository`).

Command:
```
TMPDIR=/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S073CFG --url 'https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository' --out /fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073CFG.live.txt --kind html
```
Output (verbatim):
```
S073CFG status=200 fetched_bytes=648322 snapshot_bytes=19831 sha256=7be8d5660bb2ea0d253df0d45cd9a2ed2b56b38abdc3d5aaa5a156e5813b8f5a utc=2026-10-28T23:56:10Z out=/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/S073CFG.live.txt
```
664 lines. Located quotes below are from MY capture `S073CFG.live.txt` (all ≤25 words; since scratch is removed per seat spec, the quoted lines are embedded here as the durable record):

- `S073CFG.live.txt:559` — "Owners and administrators of public repositories can allow security researchers to report vulnerabilities securely in the repository by enabling private vulnerability reporting." (21 words)
- `S073CFG.live.txt:562` — "Repository owners, organization owners, security managers, and users with the admin role" (12 words)
- `S073CFG.live.txt:569` — "The instructions in this article refer to enablement at repository level." (11 words) [same line continues: "For information about enabling the feature at organization level, see Creating a custom security configuration."]
- `S073CFG.live.txt:575` — "security researchers see a Report a vulnerability button on the repository's 'Advisories' page" (13 words)
- `S073CFG.live.txt:576` — "The built-in default form is not enforced for API submissions." (10 words) [same line opens: "Security researchers can also use the REST API to privately report security vulnerabilities."]
- `S073CFG.live.txt:579` — "By default, the private vulnerability reporting form requires reporters to provide a summary, details, proof of concept, and impact statement." (20 words)

Contradiction sweep (entry sentence vs my capture):

| Entry sentence (path) | My capture | Verdict |
|---|---|---|
| Enabling condition "Owners and administrators of public repositories can enable …" (entry :11, S073.txt:561) | :559 near-verbatim; :562 sharpens roles to "Repository owners, organization owners, security managers, and users with the admin role" | No contradiction — role list is a sharpening of "owners and administrators", not a denial |
| Reporter path begins at "Security and quality" then "Report a vulnerability" (entry :41, S073.txt:568-569) | :575 locates the button "on the repository's 'Advisories' page" | No contradiction — both pages are live and each reports its own UI wording; the entry's sentence is about what S073 says, which re-verified byte-identically today (F1). Cross-page divergence in UI-path naming noted for the L1 |
| Default form fields + "Maintainers can customize the form" (entry :20, S073.txt:573) | :579 confirms the four default fields; :580 customization via `VULNERABILITY_REPORT.yml` in `.github` (repo or owner-level) | No contradiction — confirms and mechanizes the entry's row |
| Automatic collaborator + credited user on submission (entry :22, S073.txt:577); maintainer-only merge (entry :23, S073.txt:578) | Page is silent on both (maintainer/enablement-side page) | No contradiction |
| "The enablement sentence names public repositories … The page says nothing about private repositories." (entry :42, about S073.txt:561) | Body of config page likewise names only public repositories (:559). The string "Private repository enablement" at my capture :446 is inside the support-topics navigation (between "C# compiler failing" and "Analysis takes too long"), not article content | No contradiction; entry :42 remains accurate about the S073 page |
| Recipient class "Anyone can privately report …" (entry :32, S073.txt:560) | `grep -n -E '^(Anyone|anyone)' S073CFG.live.txt` printed nothing; page's noun for submitters is "security researchers" (:559, :575, :576); its "Who can use this feature?" box (:562) is about configuring | No contradiction — audience framing, not an access denial; S073 remains the access statement |

Two scope notes the L1 may want (extensions, NOT contradictions; entry Limits bullet 1 already disclaims "not GitHub's full policy"):
1. Org-level enablement exists: :569 points to "Creating a custom security configuration" for organization-level enablement. The entry's decision rule requires "the target repository's enablement" to be recorded; an org-level custom security configuration is a second way the precondition can be satisfied that the entry's model does not name.
2. REST API submission channel: :576 "Security researchers can also use the REST API to privately report security vulnerabilities" and "The built-in default form is not enforced for API submissions." A package recording "the four default fields" for an API-submitted report would over-record; the entry's field row (:20) is web-form-scoped (S073.txt:573 sits in the web form steps).

## F5 — Defect found (minor, coverage): the entry's Limits undercounts the S073 body's linked pages, omitting exactly this enablement page

Entry :43 says "Three linked pages appear only as link text in the capture" and names S073.txt:563, :566, :579. Command: `grep -n ' See ' corpus/source-snapshots/round-46/S073.txt` — output (verbatim):
```
561:Owners and administrators of public repositories can enable private vulnerability reporting on their repositories. See Configuring private vulnerability reporting for a repository.
563:If you have admin or security permissions for a public repository, you don’t need to submit a vulnerability report. Instead, create a draft security advisory directly. See Creating a repository security advisory.
566:If the repository doesn't have private vulnerability reporting enabled, you need to initiate the reporting process by following the instructions in the security policy for the repository, or by creating an issue asking the maintainers for a preferred security contact. See Coordinated disclosure of security vulnerabilities.
579:The next steps depend on the action taken by the repository maintainer. See Managing privately reported security vulnerabilities.
585:All Docs are open source. See something that's wrong or unclear? Submit a pull request.
```
Four in-body doc links (561/563/566/579; :585 is page boilerplate, not a doc link). The census "Three linked pages" is 3 of 4; the omitted one is `Configuring private vulnerability reporting for a repository` at S073.txt:561 — the page whose body this seat fetched (F4). Suggest the L1 amend that Limits bullet (L1 is the only writer). This does not touch any gated claim; `recheck:` still passes (F2).

# Limitations

- Captures are point-in-time (2026-10-28T23:54:27Z and 23:56:10Z, instrument UA `kasegi-shokunin/1.0`). Scratch (`/fast/scratch/hyaku/kasegi-r46/R46W2ScoutLive/`) is removed before yield per seat spec; the receipt lines and located quotes embedded above are the durable evidence, and every command is reproducible as written.
- Config-page line numbers refer to my 664-line scratch capture `S073CFG.live.txt`, preserved only via the quotes embedded in F4; it is not a committed snapshot, so its line anchors are not machine-recheckable after this session (that would be an L1 decision to pin it, if wanted).
- Contradiction sweep covered the config page's body text and did not follow its outbound links (e.g., "Creating a custom security configuration"); the org-level and REST-API notes are recorded as pointers, not verified further.
- The href for the config page was resolved via a content-negotiation markdown read of the live S073 URL; all citable captures used the corpus instrument only.
- No tool installs were needed (nothing added under the 2026-10-19 tooling authorization). No commits, pushes, or mutations anywhere; only this Report file and scratch were written.
