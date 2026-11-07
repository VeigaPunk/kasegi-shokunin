# junk entry (CriticClaims r84 attack: six vacuous claims)

source: S118 — a junk entry that states nothing falsifiable
verified-at: 2026-11-06
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-84/manifest.json --source S118

## Claim 1 — filler

"This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at gs://osv-vulnerabilities/all.zip." (S118.txt:102).

Falsifiable rule: a bucket holds records and vulnerabilities on the page, as S118.txt:102 states plainly for any reader of it.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

## Claim 2 — filler

"Individual vulnerability records can be found at gs://osv-vulnerabilities/<ECOSYSTEM>/<ID>.json." (S118.txt:104).

Falsifiable rule: a record identifier for a vulnerability lives at a path on the page, as S118.txt:104 states for any reader of it.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

## Claim 3 — filler

"Vulnerabilities without an ecosystem (typically withdrawn ones) are exported to the gs://osv-vulnerabilities/[EMPTY]/ directory." (S118.txt:104).

Falsifiable rule: a directory holds exported records for no ecosystem, as S118.txt:104 states for a reader of the page.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

## Claim 4 — filler

"The per-ecosystem files omit the <ecosystem_dir>/ prefix." (S118.txt:114).

Falsifiable rule: a file may omit a directory prefix, as S118.txt:114 states for a reader of this page.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

## Claim 5 — filler

"the data dump will always contain an ecosystem directory without the :.* suffix (e.g. Alpine)." (S118.txt:121).

Falsifiable rule: a dump directory always contains an ecosystem, as S118.txt:121 states for a reader of this page.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

## Claim 6 — filler

"OSV.dev has stopped exporting entries for ecosystems with prefixes (e.g. All Alpine:.*)." (S118.txt:123).

Falsifiable rule: an export of ecosystem entries stopped, as S118.txt:123 states for a reader of this page.

Rejected over-generalization: this rejection sentence is filler text, and it says nothing about the page at all.

