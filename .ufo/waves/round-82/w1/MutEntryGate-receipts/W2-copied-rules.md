# t

source: S116 — u
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-82/manifest.json --source S116

## Claim 1 — c

"Describe the “good enough” OSV record that will be imported by OSV.dev" (S116.txt:25). x

Falsifiable rule: a caller that uses this endpoint to look up vulnerabilities affecting a package has the wrong endpoint; the page's summary names records of a source that fail import-time quality checks, not affected packages (S116.txt:25). A reader checks it by reading the page's one-line summary.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

## Claim 2 — c

"a record passes JSON Schema validation for the version of the OSV Schema it declares itself to comply with in the schema_version field" (S116.txt:36). x

Falsifiable rule: a bounty hunter or a scanner author is not the audience the page names; a plan that treats this endpoint as a consumer-side vulnerability feed contradicts S116.txt:36. A reader checks it by reading the second sentence of the Experimental endpoint paragraph.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

## Claim 3 — c

"Package-level precision is the minimum standard." (S116.txt:41). x

Falsifiable rule: reading the absence of an advisory from OSV.dev as proof that the home database never published it contradicts S116.txt:41, which describes published records that were not imported because they failed the quality bar. A reader checks it by reading the Purpose paragraph.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

## Claim 4 — c

"introduced and fixed versions or commits can’t be the same" (S116.txt:44). x

Falsifiable rule: a request that sends a JSON body with a package or a version to this endpoint carries parameters the page does not name; the page states the source is the only parameter and that it builds the URL (S116.txt:44). A reader checks it by reading the Parameters paragraph.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

## Claim 5 — c

"for commit (GIT) ranges the commits exist in the specified repo (i.e. they are not from another GitHub fork)" (S116.txt:47). x

Falsifiable rule: a call to the importfindings template is not the template the page gives; the template carries v1experimental (S116.txt:47). A reader checks it by reading the line after the Parameters sentence.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

## Claim 6 — c

"reference URLs return a 2xx or 3xx response at the time of publication" (S116.txt:51). x

Falsifiable rule: an operator who passes the display name of its project, or a record-id prefix it does not use as its source.yaml name, is not passing the value S116.txt:51 names. A reader checks it by reading the sentence after the URL template.

Rejected over-generalization: Rejected over-generalization, not a page sentence: the endpoint reports every record a source publishes, with a pass or fail mark. The summary says otherwise (S116.txt:25).

