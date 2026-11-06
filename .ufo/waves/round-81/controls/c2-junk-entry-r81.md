# junk: six pinned quotes, no claims

source: S115 — https://google.github.io/osv.dev/get-v1-importfindings/
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115

"Given a specific OSV.dev source, report any records that are failing import-time quality checks." (S115.txt:25)

"It is targeted to operators of home databases that OSV.dev imports from." (S115.txt:32)

"a machine-readable way to reason about records they have published that do not meet OSV.dev’s quality bar (and therefore have not been imported)." (S115.txt:34)

"The only parameter you need for this API call is the source, in order to construct the URL." (S115.txt:36)

"https://api.osv.dev/v1experimental/importfindings/{source}" (S115.txt:37)

"The source value is the same as the name value in source.yaml" (S115.txt:38)

