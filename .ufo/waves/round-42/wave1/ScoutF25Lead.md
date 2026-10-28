# ScoutF25Lead — round-42 wave-1 receipt: F25 lead screen + S064 capture

Seat spec: pick exactly ONE machine-readable vulnerability-data standard not held by the lane (leads: OSV schema, CVE Record Format, one found alternate), verify no lane/sibling coverage, capture it as S064 with 3 located Gate quotes, and record ≥1 fetched reject with URL/date/quote/reason/flip (closes D-r41-2). F24/RFC 9116 parked — not screened.

## Verdict

**PICK = CVE Record Format** (CVE JSON record format; CVEProject/cve-schema `CVE_Record_Format_bundled.json`, JSON Schema draft-07, `$id` cveproject.github.io/cve-schema/schema/CVE_Record_Format.json).
Criteria ranking, all candidates measured first: (i) primary first-party — CVE Program's own schema repo, equal-best with OSV(OSSF)/NVD(NIST); (ii) normative — the served artifact IS the bundled JSON Schema, machine-validatable, vs OSV's HTML page about a schema published separately; (iii) disjoint — zero hits lane+all-siblings, vs OSV adjacent (kaidoku S015 holds an OSV *record* instance, family-adjacent not identical — concurred with ScribeC2Gate-2's independent screen).

## Deliverables (landable bytes; sha256 + lines)

| file | lines | sha256 |
|---|---|---|
| ScoutF25Lead.facts.txt | 41 | 8fe4737189fd1e7b50a599049058eab199bb8550ff53b09285a44aa48ab903ef |
| ScoutF25Lead.S064.txt | 3545 | b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa |
| ScoutF25Lead.manifest-record.json | 63 | a6778644ac7aabf0fcae3fe555db928c299b54d935824c7175d2d7921a7e835a |
| ScoutF25Lead.reject-record.txt | 22 | 17a297725e910eb3bbfa3e3d774b3a0d601e84886522316e5b87b9773c6bd64c |

Landing map: `ScoutF25Lead.S064.txt` -> `corpus/source-snapshots/round-42/S064.txt`; `ScoutF25Lead.manifest-record.json` -> `corpus/source-snapshots/round-42/manifest.json` (complete file, single S064 record); facts+reject feed SOURCES.md row S064 (mined) + S065/S066 (rejected, R=2 suggested) and the lesson Gate block. S064 row source-cell URL and manifest `url` are byte-equal per capture-binding rule B5.

## Evidence — commands run with actual output

No-overlap (lane): `grep -liE 'osv|cve.?record.?format|cve.schema|CVE_Record|ghsa|nvd' corpus/SOURCES.md corpus/README.md corpus/knowledge/*.md` -> only incidental record-instance mentions (CWE methodology quotes, CISA CVD stage, S031.txt rule 5.2 naming the format once); no row/entry/capture holds any candidate spec. Siblings: `find $d/corpus -name '*.md' -o -name '*.txt' | grep -iE 'knowledge|SOURCE|registry' | xargs grep -liE 'osv.dev|...|nvd api'` -> kaidoku SOURCES.md S015 (OSV record instance, adjacent); mori SOURCES.md S012 + userspace entry (GHSA advisory page, adjacent); nothing else.

Fetches (UA kasegi-shokunin/1.0, -sS -L --max-time 90, UTC stamped):
- cve  `2026-10-28T11:06:45Z` HTTP 200, 133616 B, raw sha256 44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f
- osv  `2026-10-28T11:06:45Z` HTTP 200, 228890 B, raw sha256 8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8
- nvd-page `2026-10-28T11:06:45Z` HTTP 200, 2092 B — Angular shell + Cloudflare challenge, no document text; rejected-candidate evidence instead quotes the same family's normative artifact:
- nvd-schema `2026-10-28T11:08:16Z` HTTP 200, 10394 B, sha256 2b9c4e8ab7e6e42aa17ea787f58167beff47c119c6f291405f86ac19c6149e01

Capture verification: `python3 corpus/instruments/capture-source.py --id S064 --url <cve url> --out <scratch>/S064-instr.txt --kind text` -> `S064 status=200 fetched_bytes=133616 snapshot_bytes=84520 sha256=b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa utc=2026-10-28T11:09:10Z`; `cmp` vs my curl collapse -> BYTE-IDENTICAL. Manifest validation: `python3 corpus/instruments/source-recheck.py --manifest <scratch>/mf/manifest.json --source S064` -> `S064:sha256 OK; S064:Q1 OK occurrences=1 anchor=5-ok; S064:Q2 OK occurrences=1 anchor=3466-ok; S064:Q3 OK occurrences=1 anchor=3510-ok`, exit 0.

Gate quotes (capture lines in ScoutF25Lead.S064.txt, ≤25 words, unique): Q1 L5; Q2 L3466; Q3 L3510 — full text in facts.txt/manifest-record.

Rejects recorded (reject-record.txt): R1 OSV schema — reason: disjointness tie-break (kaidoku S015 OSV-record adjacency; HTML-about-schema vs bundled-schema), flip: re-open if S064 withdrawn or OSV range semantics needed. R2 NVD API 2.0 schema 2.2.4 — reason: downstream NVD-enriched view (evaluator*/cisa* fields), not the canonical record; flip: NVD-enrichment/API-contract frontier. Quote pins: OSV normalized L9 (14w); NVD schema served L96 (10w).

F25 row suggestion (for landing): "CVE Record Format 5.x (CVE JSON record format) — canonical machine-readable CVE record: dataType/dataVersion/cveMetadata/containers, one 'cna' + optional 'adp' containers, PUBLISHED/REJECTED states" — disjoint from F07 (CNA assignment rules, not record shape).

## Hygiene

- Scratch: `/fast/scratch/hyaku/kasegi-r42/ScoutF25Lead` — removed before yield (rm -rf; verified gone).
- No lane/fleet/sibling writes outside `.ufo/waves/round-42/wave1/ScoutF25Lead.*`; no git mutations; disk guard green at start (27% used on /fast/scratch/hyaku).
- Tool installs: none (curl, python3, coreutils already present; RULES.md read; pacman not touched).
- Peers: pick summary sent to ScribeC2Gate-2 for the Gate block.

Confidence: high on pick + capture (instrument-verified, byte-identical refetch). Remaining unknowns: none blocking wave-1 landing; NVD doc-page is JS-gated, noted honestly in R2.
