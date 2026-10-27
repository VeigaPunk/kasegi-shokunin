# ScoutRfc9116 — receipt (round 41, wave 1)

Seat: ScoutRfc9116 (leaf scout, no subagent dispatch). Item: open RFC 9116 live from source, record quotable facts with line numbers, verify lane-coverage absence. Deliverable: `.ufo/waves/round-41/wave1/ScoutRfc9116.facts.txt` (59 lines, 9087 bytes, sha256 ad70cd054edcee77bb290d587b2726841ef8a5a3ab3d7eb3338cf9d0e8a8311a).

All quotes in the deliverable were re-located in the fetched bytes below with line numbers from the fetched capture itself (verified with `awk NR>=...` and `grep -n`, transcripts in scratch session). Nothing is quoted from memory.

## Fetch transcript 1 — rfc-editor text

Command:
`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -w '\nHTTP_STATUS=%{http_code} SIZE=%{size_download} CONTENT_TYPE=%{content_type}\n' -o rfc9116.txt https://www.rfc-editor.org/rfc/rfc9116.txt`

Actual output:
```
HTTP_STATUS=200 SIZE=45129 CONTENT_TYPE=text/plain;charset=utf-8
```
UTC fetch time: 2026-10-27T08:18:37Z (date -u at completion).
`wc -c rfc9116.txt` → 45129; `sha256sum rfc9116.txt` → `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`.

## Fetch transcript 2 — datatracker page

Command:
`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -w '\nHTTP_STATUS=%{http_code} SIZE=%{size_download} CONTENT_TYPE=%{content_type}\n' -o rfc9116-datatracker.html https://datatracker.ietf.org/doc/rfc9116/`

Actual output:
```
HTTP_STATUS=200 SIZE=80220 CONTENT_TYPE=text/html; charset=utf-8
```
UTC fetch time: 2026-10-27T08:18:38Z.
`wc -c rfc9116-datatracker.html` → 80220; `sha256sum` → `dacfed24ebf0ebb625667fd56d984b9d7c789a509d9321b2dfb2362268d59aff`.

Datatracker metadata (HTML stripped to text, lines 85-119 of the stripped view): title "A File Format to Aid in Security Vulnerability Disclosure", "RFC 9116", "Type RFC - Informational (April 2022)", "Was draft-foudil-securitytxt (individual in sec area)", authors E. Foudil / Y. Shafranovich, "RFC stream: Internet Engineering Task Force (IETF)", responsible AD Benjamin Kaduk, last updated 2026-05-20.

## Key cross-checks against the fetched text (all verified on the capture bytes)

- Status: capture lines 7 and 25-26 — "Category: Informational" / "This document is not an Internet Standards Track specification; it is published for informational purposes." (So NOT Standards Track / NOT Proposed Standard; frozen-claim phrase "kind spec, tier A" refers to the registry row's kind field; the RFC's own category is Informational.)
- Well-known sentence: capture lines 439-441.
- Default field optionality: capture line 237.
- Contact MUST: lines 290-291; Expires MUST + one-year RECOMMENDED: lines 347-351; Encryption "Keys MUST NOT appear...": lines 316-319; Preferred-Languages MUST-NOT-more-than-once: line 388.
- Security considerations: 5.1 lines 686, 688-689; 5.3 lines 721, 726-728; 5.4 lines 737, 743-745 (32 KB / 2048 chars / 1000 lines).
- IANA: 6 (line 836), 6.1 (line 842, security.txt permanent), 6.2 (line 852, eight initial field rows lines 878-950).

## Coverage verdict

`grep -rni 'security\.txt\|rfc 9116\|rfc9116\|9116' corpus/ SKILL.md` (run at lane root 2026-10-27): only the expected pre-r15 operational stub mentions — corpus/knowledge/policy-access-playbook.md:12; corpus/knowledge/retirement-autopsies.md:19,127; corpus/knowledge/submitted-registry.md:90; SKILL.md:131,453,486 — plus in-passing citations inside other sources' captures (round-24 S003.txt:173-178, S011.txt:685; round-25 S040.txt:81-82; round-26 S040-live.txt:81-82; round-38 S055.txt:470-471,3853-3861; round-40 S021.txt:357-358). corpus/knowledge/rfc-9116-security-txt.md does not exist; registry has 62 rows ending at S062; frontier ends at F23. VERDICT: RFC 9116 not covered anywhere in the lane as ground; S063 and F24 are free for the L1 to land.

## Tooling / environment

- No installs or upgrades performed (curl, grep, awk, python3, sha256sum, wc already present on host). No pacman use. Nothing written outside the wave dir and scratch.
- Disk guard checked green before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` (root/tmp usage low, /fast/scratch 25%).
- Scratch: /fast/scratch/hyaku/kasegi-r41/ScoutRfc9116 (fetch artifacts + session). Removed at yield per seat guard.
- Read-only lane access only; no git/jj mutations anywhere. Fleet root and shokuknow untouched.

## Hand-off

Deliverable is landable as-is for the L1's C2 artifacts: F24 coverage-map row + PROVINCE amendment, registry row S063 (kind spec, tier A — note the RFC category itself is Informational), capture corpus/source-snapshots/round-41/S063.txt byte-identical to the 45129-byte / sha256 79d19ce7... fetch above, manifest.json record, knowledge entry corpus/knowledge/rfc-9116-security-txt.md (provenance trio: rfc-editor URL + datatracker URL + fetch ledger; `source: S063`). All quotes carry capture line numbers for the source-recheck and capture-binding gates.
