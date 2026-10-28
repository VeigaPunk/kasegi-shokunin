# ScribeC2Gate — round-42 lesson `## Gate` block (C2, F25/S064 admission + screened rejects)

Seat: scribe (leaf, no subagent dispatch). Round 42, wave 1, lane `kasegi-shokunin`.
Base `5053a7f46de35784cff4b56756906e9014a38276`; frozen claims read first from
`.ufo/waves/round-42/claims.json` (not edited). No mutating git/jj command run; no file outside the
seat's write scope written.

Deliverable: `.ufo/waves/round-42/wave1/ScribeC2Gate.gate-block.txt` — the landable `## Gate` markdown
the round-42 lesson carries in place of ScribeLesson's placeholder. Text only: no validation tables, no
notes, no headings outside the landed block.

## 1. What the block records

- `### Admitted — F25 / S064 (CVE Record Format)` with, in the round-41 Gate's shape: lead screen and
  no-overlap evidence, the S064 row cells, source URL + 2026-10-28 access date + fetch ledger, the
  capture path with lines/bytes/sha256, three ≤25-word located quotes, the knowledge entry and its
  provenance trio, the frontier admission 24 -> 25, and a limit paragraph.
- `### Rejected — the screened floor (closes D-r41-2)` with two rejects (S065 OSV schema, S066 NVD
  Vulnerability Data API 2.2.4 schema), each carrying URL, 2026-10-28 access date, upstream fetch
  ledger, a located ≤25-word quote, an honest reason on a named criterion, and a flip condition; plus
  the two candidates dropped before a fetch (GHSA, FIRST VIN) and a closing sentence naming D-r41-2.

## 2. Commands run (actual output)

Disk guard (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`) is green —
`/fast/scratch/hyaku 28% 580.4G free`, `/tmp 5% 122.1G free`. This seat ran no heavy pass: file reads,
`grep`/`sed`, and three `curl` fetches (candidate ledger, ~373 KB total).

```
$ cd .../kasegi-shokunin && grep -n '"predicate"\|"kill_rule"\|"id"' .ufo/waves/round-42/claims.json
23:   "id": "C1",
27:   "predicate": "The committed instrument `corpus/instruments/r42-closure.sh` ...
44:   "id": "C2",
48:   "predicate": "One new frontier topic F25 is admitted 24->25 ...
49:   "kill_rule": "Any of: no F25 frontier row or its status cell not `admitted`; ...

$ cat .ufo/waves/round-42/c2-controls/before.txt
frontier rows: 24 / F25 rows: 0 / registry rows: 63 / S064+ rows: 0 / knowledge files: 60
entries citing S064+: 0 / harness: entries=27 pass=27 exit=0 / binding: records=55 bound=55 unbound=0
audit: expect=present expected=60 missing=0 unexpected=0 exit=0

$ sed -n '120,165p' corpus/lessons/round-41-verifier-spotcheck.md
... 2. **D-r41-2 (discernment protocol).** The round-41 Gate recorded no reject; the outside spot-check
    had nothing to sample in the reject direction. Round 42 should screen >=1 candidate and record a
    reject with reason + flip (a lead-level rejection suffices).

$ awk '/^## Gate/,0' corpus/lessons/round-41.md        # format reference (Admitted block shape)
$ sed -n '120,165p' corpus/lessons/round-40.md          # format reference (Rejected block shape)
```

Lane + sibling no-overlap screen (each command run from the lane root; sibling loop over every
`/home/vgpnk/Projects/shokunin/*-shokunin`, kasegi excluded):

```
$ grep -rin 'cve record format\|cve-record-format\|CVE_Record_Format\|cve-schema' \
    corpus/knowledge/*.md corpus/SOURCES.md corpus/README.md PROVINCE.md
(no output)
$ grep -rli 'osv' corpus/SOURCES.md corpus/README.md corpus/knowledge/*.md
(no output)
$ for L in /home/vgpnk/Projects/shokunin/*-shokunin; do [ kasegi ] && continue;
    grep -ril 'CVE_Record_Format\|cve-schema\|cveSchema' "$L/corpus/knowledge" "$L/corpus/SOURCES.md" "$L/SKILL.md"; done
(no output from any lane)
$ grep -ril 'osv' ...same sibling loop...
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
$ grep -n 'S015' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
21:| S015 | OSV CVE-2025-55305 record — https://api.osv.dev/v1/vulns/CVE-2025-55305 | dataset | A | ...
```

The lane does hold near-references to the term, which the block states precisely instead of claiming
zero: `grep -o 'CVE Record Format' corpus/source-snapshots/round-23/S031.txt | wc -l` -> `7`
(L102 §4.5.5, L112 x2 §5.1.12-§5.1.13, L114 x3 §5.2, L116 §5.2.11), and no capture of the format.

Fetch ledger (both re-run by this seat, independently of ScoutF25Lead):

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o cand_307815a0.bin -w '%{http_code}' \
    https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json
HTTP=200 BYTES=133616 SHA=44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f UTC=2026-10-28T11:02:52Z
$ ... https://ossf.github.io/osv-schema/
HTTP=200 BYTES=228890 SHA=8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8 UTC=2026-10-28T11:02:52Z
$ ... https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema
HTTP=200 BYTES=10394 SHA=2b9c4e8ab7e6e42aa17ea787f58167beff47c119c6f291405f86ac19c6149e01 UTC=2026-10-28T11:11:09Z
```

## 3. Evidence verification (every claim in the block is checked against bytes)

Capture binding (ScoutF25Lead.S064.txt, read from the wave-1 dir):

```
$ wc -l ScoutF25Lead.S064.txt ; sha256sum ; stat -c%s
3545 ; b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa ; 84520
```

Quote validation (whitespace-collapsed matcher — Gate lines wrap, so the matcher joins lines before
matching, the same matcher RevC2Entry documented for the entry bar):

| quote | capture line | words | in capture line | occurrences in capture | in Gate block |
|---|---|---|---|---|---|
| Q1 "cve-schema specifies ... set of JSON data" | L5 | 18 | yes | 1 | yes |
| Q2 "When a CNA populates ... as a CVE Record" | L3466 | 15 | yes | 1 | yes |
| Q3 "A Rejected CVE Record ... when it is invalid." | L3510 | 18 | yes | 1 | yes |

Structural claims behind the quote glosses, re-read at the cited lines: `$schema` L2, `$id` L3,
title L4/description L5; root `oneOf` L3463, `Published` title L3465 / description L3466, required list
L3500-L3505 (`dataType`, `dataVersion`, `cveMetadata`, `containers`), `containers` L3478-L3498
(`cna` required L3494-L3496, `adp` optional), `Rejected` title L3509 / description L3510,
`dataVersion` pattern L482 and `default` `5.2.0` L483.

Reject quotes:

| reject | quote source | words | located | in Gate block |
|---|---|---|---|---|
| S065 OSV | page normalized by `capture-source.py --kind text`, L9-L10 | 14 | `This document defines a standard interchange format for describing` at L9 (own normalization reproduced L9 verbatim), sentence completes L10 | yes |
| S066 NVD | served schema L96, `metrics.description` | 9 | `Metric scores for a vulnerability as found on NVD.` at L96 of the fetched 10394-byte file | yes |

Own re-derivation of the OSV location: this seat normalized the fetched HTML with the same collapse
(`<script|style|svg|noscript>` stripped, tags to newlines, whitespace runs collapsed, blank lines
dropped) and got `Purpose` at L8, the quote line at L9, `vulnerabilities in open source packages.` at
L10, `This format is stable, but further backwards compatible changes may still be made.` at L17 —
matching the scout's reject-record anchors.

Correction to the scout's facts: `ScoutF25Lead.facts.txt` says S031 mentions "CVE Record Format" once
in rule 5.2. Re-measured: 7 occurrences (L102, L112 x2, L114 x3, L116). The no-overlap conclusion is
unchanged (no capture of the format document), and the block records the corrected figure. Reported to
ScoutF25Lead.

## 4. Consistency with the artifacts the L1 will land

Read, not guessed, before the block was written:

- `ScoutF25Lead.S064.txt` (capture), `ScoutF25Lead.manifest-record.json` (S064: url, fetched 200,
  133616 raw bytes, 3545 lines, 84520 B, both sha256s, quotes Q1-Q3 with anchors 5/3466/3510),
  `ScoutF25Lead.reject-record.txt` (R1/R2 URL, date, quote, reason, flip).
- `ScribeC2Entry.entry.md`: header `source: S064 ... capture corpus/source-snapshots/round-42/S064.txt
  (3,545 lines, 84,520 bytes; sha256 b90a51f7...`, `verified-at: 2026-10-28`, `ground: F25`, `recheck:`
  executable; the entry's pinned anchors include `S064.txt:L5`, `L3466`, `L3510`.
- `ExecC2Rows.registry-rows.txt`: row S064 `| spec | A | ... | mined | 2026-10-28 | on-release |
  corpus/knowledge/cve-json-record-format.md |`; reject rows S065 (OSV) and S066 (NVD) both end
  `... | rejected | 2026-10-28 | on-release | — |`.
- `ExecC2Rows.readme-row.txt` contains exactly one appended `| F25 | ...` frontier line (the 24 -> 25
  row) and `ExecC2Rows.province-amendment.txt` carries the `[r42 Frontier amendment, appended
  2026-10-28...]` F25 line.
- Entry filename confirmed by ScribeC2Entry-3 (message): `corpus/knowledge/cve-json-record-format.md`.
  S065/S066 ids confirmed from the landed registry-rows deliverable.

## 5. Deliverable facts

- Path: `.ufo/waves/round-42/wave1/ScribeC2Gate.gate-block.txt`
- Lines / bytes / sha256: **92** / **7751** /
  **`d601dcc94bbf939167ae936f8b4918294e0f91d941c9be4456762c3ee5c28173`** — measured on the copied
  bytes; `cmp` of the scratch draft and the copied file exits 0. No tabs, no CR bytes, no trailing
  whitespace, final newline present; headings are exactly `## Gate`,
  `### Admitted — F25 / S064 (CVE Record Format)`,
  `### Rejected — the screened floor (closes D-r41-2)`.
- Tooling installed: none (no pacman transaction, no `uv tool install`, no binary fetched; `curl`,
  `python3`, `grep`, `sed`, `sha256sum` only).

## 6. Scratch

`S=/fast/scratch/hyaku/kasegi-r42/ScribeC2Gate/` held the candidate fetches, the normalized OSV text,
the NVD schema and the Gate draft. Copied into the wave-1 dir, then removed (`rm -rf`). No scratch
survives.

## 7. Limits of this seat

- The Gate block is text the L1 lands; it does not itself write `corpus/lessons/round-42.md`,
  `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`, the manifest or the entry.
- No lane gate/instrument was run: this seat verified quotes against bytes (grep/matcher), not the
  suite. `r42-closure.sh` and the C2 instruments are other seats' work; the frozen counts (25 frontier,
  64+R registry, 28/28 harness, 56/56 binding, expected=61) are the L1's to re-derive after landing.
- The S065/S066 reject rows are ExecC2Rows' bytes; the block quotes the scout's reject-record and the
  served documents, and this seat re-verified both quotes at their locations.
