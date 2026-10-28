# Google Cloud VRP: customer-resource boundary

source: S069 — https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules — Rules of Engagement: Disqualifying Actions & Boundaries, “Do Not Test Customer Projects & Resources”; captured through the official article API at `corpus/source-snapshots/round-44/S069.txt`.
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069 # 180d

## Scope and decision rule

This entry records the Google Cloud Vulnerability Reward Program's own terms; it is not a rule for Google's other programs or a general authorization opinion. In its Cloud VRP scope section the policy states: “product or web service that handles reasonably sensitive user data is intended to be in scope” (`S069.txt:10-11`, manifest Q5). Read that as a program scope statement, not permission to test an arbitrary Google-branded or customer-owned service.

The Cloud VRP's explicit boundary is: “The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services” (`S069.txt:61-62`). Its next sentence says: “To protect customer data and privacy, testing customer resources is strictly prohibited” (`S069.txt:62-63`). The rule identifies `*.bc.googleusercontent.com` and `*.appspot.com` as examples of customer-owned domains (`S069.txt:68-69`); the suffix alone is a reason to inspect the program's ownership boundary, not proof that a target is Google-owned.

| Observed question | Cloud VRP text | Package consequence |
|---|---|---|
| Does a Google Cloud product fall within the described program scope? | The policy states that a “product or web service that handles reasonably sensitive user data is intended to be in scope” (`S069.txt:10-11`, Q5). | Record the exact product and the program rule; do not generalize this to Google Workspace or other programs. |
| Does the tested resource belong to a Cloud customer? | The policy prohibits customer-resource testing and names example customer domains (`S069.txt:61-69`). | Do not represent customer-hosted resources as authorized Cloud VRP targets. |
| Did a report's finding or verification touch customer resources? | “the report is ineligible for a reward if finding or verifying it involved testing or accessing customer resources” (`S069.txt:70-72`). | Record reward-ineligibility separately from the technical validity of a finding; do not erase the finding or imply permission. |
| Would proving impact risk another tenant? | The policy says not to test unsafe multi-tenant escapes live and instead submit technical analysis with local reproduction (`S069.txt:78-86`). | Keep the package's evidence bounded to the local reproduction and analysis; do not test a live shared tenant. |

## Limits

This is one vendor's Cloud VRP rule, not general law, a statement about all Google programs, or proof of authorization for any action. Customer authorization and Cloud VRP reward eligibility are separate: the Cloud VRP says testing of customer resources without written authorization is prohibited and separately says reports involving such testing are ineligible (`S069.txt:65-72`). The entry documents program text only; it instructs no target testing, scanning, account access, or submission.

## Round-44 novel rule and rejected over-generalization (appended)

This entry does not claim novelty for the general rules already held: F03 distinguishes policy scope from a safe-harbor badge (`corpus/knowledge/authorization-safe-harbor-and-scope.md:8`), F09 says a platform cannot supply a third-party customer's consent (`corpus/knowledge/statutory-authorization-and-unauthorized-access.md:46`), F13 records a program's own asset-control boundary (`corpus/knowledge/program-severity-ladders-and-reward-scales.md:16`), and F01 separates technical score from program eligibility and reward (`corpus/knowledge/cvss-v4-severity-and-vector.md:34`). Those are shared principles, not F26's expansion.

The Cloud VRP adds a program-specific, previously uncovered restriction: “Finding a Google-owned asset inside a customer IP block during a broad scan is still considered unauthorized testing within customer space” (`S069.txt:76-77`, 21 words). It also says unsafe multi-tenant escapes should not be tested live and directs researchers to submit technical analysis with local reproduction (`S069.txt:78-87`). These are the new F26 ground: customer IP-range ownership remains the boundary even when an individual asset is Google-owned, and an unsafe shared-tenant reproduction is local, not live.

**Falsifiable package rule:** when a report claims a Cloud VRP target is eligible, check the program's customer-IP-range and tenant boundary in addition to product ownership; if the observed address range belongs to a customer, do not treat a Google-owned asset inside it as permission to scan or test.

**Rejected over-generalization:** “A Google-owned asset is in scope even when it lies inside a customer IP range.” Rejected because S069 says the broad-scan discovery “is still considered unauthorized testing within customer space” (`S069.txt:76-77`). Re-open only if Google's Cloud VRP rule changes or supplies a narrower explicit exception for that customer-range case.

## Source-ID namespace note (appended)

`S069` here means the row in this lane's `corpus/SOURCES.md` and its Google Cloud VRP capture. Round-35 lessons also use `S069` inside the separate external absent-defect-register namespace for a Chinese national-standard PDF (`corpus/lessons/round-35.md:124,136-139`). The identical token does not identify the same document across those namespaces; use the URL and capture digest above to resolve this entry's source.
