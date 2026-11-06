# FORGED — true provenance, inverted meaning

source: S115 — https://google.github.io/osv.dev/get-v1-importfindings/
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115

## Claim 1 — c

"Given a specific OSV.dev source, report any records that are failing import-time quality checks." (S115.txt:25). The endpoint reports every record a source publishes, whether the checks pass or fail.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:25.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

## Claim 2 — c

"It is targeted to operators of home databases that OSV.dev imports from." (S115.txt:32). It is a public feed for consumer-side scanners, not a report for data publishers.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:32.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

## Claim 3 — c

"a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported)." (S115.txt:34). A record below the bar is repaired and imported, so absence from OSV.dev means nothing.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:34.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

## Claim 4 — c

"The only parameter you need for this API call is the source, in order to construct the URL." (S115.txt:36). The call takes a JSON body naming a package, a version and a source.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:36.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

## Claim 5 — c

"https://api.osv.dev/v1experimental/importfindings/{source}" (S115.txt:37). The source may also be sent as a query-string parameter on the stable v1 prefix.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:37.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

## Claim 6 — c

"The source value is the same as the name value in source.yaml" (S115.txt:38). The source value is the record-id prefix of the source's own advisories.

Falsifiable rule: a reader who expects the opposite behaviour from this sentence has misread S115.txt:38.

Rejected over-generalization, not a page sentence: the sentence is broader than the one deployment it describes.

