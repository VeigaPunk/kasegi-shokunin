# ConnectorOverlap receipts — index

All paths under /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ConnectorOverlap-receipts/.
Scratch: /fast/scratch/hyaku/kasegi-r86/ConnectorOverlap (deleted before yield). Nothing outside this
directory and scratch was written; all lane/fleet/shokuknow reads were read-only.

| file | what it shows | how to reproduce |
|---|---|---|
| sibling-scan.txt | 20 sibling lanes grepped for the C2 subject tokens and for a knowledge-scope repoint instrument; only 2 incidental (non-source) '1997312' hits; no sibling holds S122/S123, the IBB subject or CVE-2023-28319; no sibling has corpus/instruments/resolve.py or a knowledge meter | grep -rlF over /home/vgpnk/Projects/shokunin/*-shokunin/corpus/ (commands in the file) |
| assimilation/reg.ids | 123 registry ids from corpus/SOURCES.md (pattern ^ {0,3}\|[[:space:]]*S[0-9]{3,}) | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md \| grep -oE 'S[0-9]+' \| sort -u |
| assimilation/staged.ids | 94 staged ids from /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | same pattern on the staged file |
| assimilation/collisions.txt | 93 ids in both (comm -12) | comm -12 reg.ids staged.ids |
| assimilation/guard/ | guard proof: an indented "  | S002 |" row is found by the 0-3-space pattern (collisions nonempty) and silently dropped by a naive ^\| pattern (collisions empty) | cat guard/registry-guard.md; the two extractions are in kasegi-merge-detail.txt §6 |
| kasegi-merge-detail.txt | 93/93 colliding ids hold *different* sources (0 identical), S124 free, S120 malformed (12 fields); union dry-run through the fleet census: E03 92 / E01 1 / E09 43 / E04 4 vs control 0; C1 map basenames inside the colliding range; fleet table summary | file lists the exact commands |
| union-validate-inside.txt | census validate over registry+staged union inserted inside ## Registry: rc 1, 92 E03 duplicate id, 1 E01 S120 fields=12 | bash scripts/sources-census.sh validate --root $S/census-root $S/census-root/kasegi-shokunin |
| union-validate-control.txt | same scratch root, unmodified registry: rc 1, 106 E11 (scratch root holds only SOURCES.md) + 6 W04, no E03/E01/E09/E04/W01 | same command on the control root |
| union-append-at-eof.txt | same append placed after ## Registry: E12 x94 "row outside Registry section", E03 0 — the duplicate-id check does not see out-of-section rows | same command, rows appended at EOF |
| fleet-merge-collision.tsv | 21 lanes: staged/registered/common/row-differs/identical/staged-only counts; every lane with common ids has 0 identical rows | python3 -B script (command line in the file header) |
| root-witness.txt | C1 root probe: base 398/1721 (scratch parent) vs 399/1721 (fleet-root-like parent); after 596/1716 pass vs 597/1716 M1 FAIL; map bytes and excluded bytes identical in both roots; 0/406 key+value classification flips; only ../MISSION.md:49-56 flips | commands in the file; clone --shared + frozen instruments |
| rebuilt-map.json, rebuilt-excl.json | the frozen builder re-run at base rev: repair-map sha dd40455a... (203 keys), excluded sha 920641e6... (89 tokens), byte-identical to the frozen files; two runs identical | python3 -B c1/build-map.py --lane $S/land --rev d7296645... --out ... --excluded ... --work ... |

Note: no S<digits>.txt file was copied into the wave dir; snapshots are cited by path and sha256 only.
