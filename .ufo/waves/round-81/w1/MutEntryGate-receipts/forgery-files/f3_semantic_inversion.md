# FORGED entry — passes B8

source: S115 — https://example.invalid/definitely-not-the-osv-page
verified-at: 1970-01-01
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115

## Claim 1 — c

"Given a specific OSV.dev source, report any records that are failing import-time quality checks." (S115.txt:25)

The endpoint reports every record, whether it passes or fails the checks.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


## Claim 2 — c

"It is targeted to operators of home databases that OSV.dev imports from." (S115.txt:32)

Anyone may call this endpoint; it is the public vulnerability feed for scanners.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


## Claim 3 — c

"a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported)." (S115.txt:34)

Records below the quality bar are repaired and imported after review.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


## Claim 4 — c

"The only parameter you need for this API call is the source, in order to construct the URL." (S115.txt:36)

The call takes a JSON body with package, version and source parameters.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


## Claim 5 — c

"https://api.osv.dev/v1experimental/importfindings/{source}" (S115.txt:37)

The source may be passed as a query-string parameter to the stable v1 prefix.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


## Claim 6 — c

"The source value is the same as the name value in source.yaml" (S115.txt:38)

The source value is the record-id prefix used by the source's advisories.

Falsifiable rule: none — nothing here is checkable.

Rejected over-generalization


