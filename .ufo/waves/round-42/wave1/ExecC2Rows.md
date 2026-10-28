# ExecC2Rows — round-42 wave-1 receipt (C2 landable rows: S064/S065/S066, F25 frontier row, PROVINCE amendment, manifest record, knowledge-expected)

Seat: `ExecC2Rows` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` only; the fleet
root `/home/vgpnk/Projects/shokunin` and `/home/vgpnk/Projects/shokuknow` were read-only to me and were
not written. No subagent, labrat probe, background job, swarm or second runtime was used. No mutating
git/jj command was run anywhere (read-only `git log`, `git show`, `git archive`, `git rev-parse` only).
Scratch `S=/fast/scratch/hyaku/kasegi-r42/ExecC2Rows` (removed at exit). Tooling: nothing installed or
upgraded — none needed. Disk guard read before the work: `/fast/scratch/hyaku 27% use, 592.6G free` —
green.

Inputs consumed (all read-only): `ScoutF25Lead.facts.txt`, `ScoutF25Lead.S064.txt`,
`ScoutF25Lead.manifest-record.json`, `ScoutF25Lead.reject-record.txt` (the scout's filed facts), and
`ScribeC2Entry.entry.md` (the entry's filed bytes, used only to validate my rows against the entry they
bind). `claims.json` and `claims-erratum-1.md` were read, not edited.

## 1. Deliverables (byte-exact landable bytes)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecC2Rows.registry-rows.txt` | 3 | 5081 | `3cad4cfdb3c6b47dc002819a3ed5d0397b81eb9b570adefc4fb2c3c43c70ee05` |
| `.ufo/waves/round-42/wave1/ExecC2Rows.readme-row.txt` | 28 | 2944 | `66519653dade76a909dc73ad2f34871aeef02eea38fd0640a8a9e5d7cea333c1` |
| `.ufo/waves/round-42/wave1/ExecC2Rows.province-amendment.txt` | 2 | 395 | `d8b0f16625ee7f0eb2f02d8c54c6459f9cd2e055992dfc1ed06ab22ddecf3b65` |
| `.ufo/waves/round-42/wave1/ExecC2Rows.manifest-record.json` | 71 | 4662 | `32145af1563dc32ceaaaf97a47ff3cca1c6c29f0a5cab4ccb2a4506c09a5fb8e` |
| `.ufo/waves/round-42/wave1/ExecC2Rows.knowledge-expected.txt` | 63 | 3122 | `b095a0ba0ab3196cb9aecea1b8f2c387b6a92e87ea80d80b98c666c2570bbcba` |

Byte hygiene on all five (asserted in the build): 0 tabs, 0 CR bytes, 0 lines with trailing whitespace,
final `\n` present. No literal `|` inside any cell of the three registry rows (each row splits into
exactly 13 awk fields = the census's `NF=13`, so census `E01` cannot fire). (This receipt's own census
evidence blocks contain literal tabs — they are the census tool's own TSV output, transcribed
verbatim.)

### What each file contains

- **registry-rows.txt** — three one-line `corpus/SOURCES.md` registry rows in the lane's 11-column
  grammar (`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`):
  - `S064` — **mined**, kind `spec`, tier `A`, opened `2026-10-28`, recheck `on-release`, used-by
    `corpus/knowledge/cve-json-record-format.md`.
  - `S065` — **rejected** (OSV schema), used-by `—`, teaches starts `REJECTED:` and carries `flip:`.
  - `S066` — **rejected** (NVD API 2.0 CVE response schema 2.2.4), used-by `—`, same grammar.
- **readme-row.txt** — the whole `## Round-42 admission` block in the round-41 shape: the R6
  not-edited-in-place paragraph, the 3-cell coverage-map row, the 6-cell `F25` frontier row
  (`admitted`, `knowledge/cve-json-record-format.md`, `S064`), and the `[r42 amendment, appended
  2026-10-28]` count line reading **25/25 admitted**.
- **province-amendment.txt** — 2 lines: a blank separator and the
  `[r42 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F25 — …` line, prefix- and
  form-identical to the F22/F23/F24 amendments already in `PROVINCE.md` (no backticks around the entry
  path, matching the two most recent amendments).
- **manifest-record.json** — the complete `corpus/source-snapshots/round-42/manifest.json` bytes:
  `schema_version` 1, a `purpose` line, and **one** `sources` record for `S064` with the scout's
  `path`/`url`/`fetched_utc`/`sha256`/`http` block and **four** pinned quotes `Q1`–`Q4`.
- **knowledge-expected.txt** — the committed `corpus/instruments/knowledge-expected.txt` with exactly
  **one** added line, `corpus/knowledge/cve-json-record-format.md`, inserted at the sorted seam between
  `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` and
  `corpus/knowledge/cvss-v4-severity-and-vector.md`. Every other committed byte is preserved — see §5.

## 2. Capture facts — re-derived, not taken on trust

I fetched the picked document myself rather than only accepting the scout's numbers, and the capture I
produced is byte-identical to the scout's filed capture:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-28T11:03:05Z
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o <raw> \
    -w 'HTTP %{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json
HTTP 200 bytes=133616 url=https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json
$ sha256sum <raw>
44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f  <raw>
```

Normalised with the lane's own instrument (`capture-source.py` `collapse()`):

```
lines 3545 bytes 84520 sha256 b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa
$ cmp <my capture> wave1/ScoutF25Lead.S064.txt && echo IDENTICAL-TO-SIBLING-CAPTURE
IDENTICAL-TO-SIBLING-CAPTURE
```

So the sha256/lines/bytes in my `S064` row's anchor cell and in the manifest record are the bytes that
will land, and they are reproducible from the published URL.

Both **rejected** candidates were re-fetched and re-verified independently as well (this is the D-r41-2
evidence the claim names):

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-28T11:23:08Z
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o osv-schema.raw \
    -w 'HTTP %{http_code} bytes=%{size_download} final=%{url_effective}\n' https://ossf.github.io/osv-schema/
HTTP 200 bytes=228890 final=https://ossf.github.io/osv-schema/
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o cve_api_json_2.0.schema.raw \
    -w 'HTTP %{http_code} bytes=%{size_download} final=%{url_effective}\n' \
    https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema
HTTP 200 bytes=10394 final=https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema
$ sha256sum osv-schema.raw cve_api_json_2.0.schema.raw
8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8  osv-schema.raw
2b9c4e8ab7e6e42aa17ea787f58167beff47c119c6f291405f86ac19c6149e01  cve_api_json_2.0.schema.raw
```

Both digests equal the scout's fetch ledger byte-for-byte. The two reject quotes are located and
unique in their own documents:

```
OSV  quote "This document defines a standard interchange format for describing"
      occ=1  at normalized page-text line 9  (sentence completes on line 10)
NVD  quote "Metric scores for a vulnerability as found on NVD."
      occ=1  at served line 96  (the metrics.description field)
```

Every line number I cite in the rows was re-opened in the capture and printed before landing; the
`S064` anchor cell names `$schema` L2, `$id` L3, title L4, description L5, `dataType` L472-L477,
`dataVersion` L479-L484, `cveMetadataPublished` L485, `cveMetadataRejected` L537, `providerMetadata` L589,
status enum L128-L136, `defaultStatus` L344, `versions` L355-L386, `changes` L419-L446, `packageURL`
L448-L449, `cnaPublishedContainer` L693, `adpContainer` L809, and the root `oneOf` L3463-L3544
(Published L3464-L3507, Rejected L3508-L3543). Spot checks, verbatim:

```
  L472  "dataType": {
  L476  "CVE_RECORD"
  L480  "description": "The version of the CVE schema used for validating this record. Used to support multiple versions of this format.",
  L482  "pattern": "^5\\.(0|[1-9][0-9]*)(\\.(0|[1-9][0-9]*))?$",
  L483  "default": "5.2.0"
  L3500 "required": [
  L3536 "required": [
```

## 3. The four pinned quotes (Q1-Q4) re-run against the capture

`source-recheck.py` over a scratch manifest holding the landed capture:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json --source S064
S064:sha256 OK
S064:Q1 OK occurrences=1 anchor=5-ok
S064:Q2 OK occurrences=1 anchor=3466-ok
S064:Q3 OK occurrences=1 anchor=3510-ok
S064:Q4 OK occurrences=1 anchor=480-ok
exit=0
```

`Q1`-`Q3` are the scout's three quotes, unchanged (same text, same anchor, same `location`). `Q4` is
mine: the `dataVersion` description at L480 — the version-in-record quote, chosen because it is the
fourth thing the entry's Claim 1 asserts and it is unique (`occurrences=1`, `anchor=480-ok`). Each
quote is ≤25 words (18 / 15 / 18 / 19), matching the claim's Gate rule.

## 4. Validation on a scratch mirror (my bytes landed, not simulated)

Mirror = `git archive HEAD corpus PROVINCE.md SKILL.md` extracted into scratch, then my three appends
applied with the landing recipe of §5, plus the siblings' already-delivered stand-ins
(`ScoutF25Lead.S064.txt` → `corpus/source-snapshots/round-42/S064.txt`, my manifest record →
`corpus/source-snapshots/round-42/manifest.json`, `ScribeC2Entry.entry.md` →
`corpus/knowledge/cve-json-record-format.md`, and my `knowledge-expected.txt`). One difference from the
landed bytes: the entry's `recheck:` line `cd`s the real lane, which has no `round-42` yet, so the
**mirror copy** of that one `cd` target was repointed at the mirror — the same measurement the round-41
seat made. It is disclosed here and in §7.

### 4.1 The claim's counting commands (mirror)

```
frontier rows (24 -> 25)                       25
registry rows (63 -> 66 per erratum E1)        66
S064 mined rows (0 -> 1)                       1
entries citing S064 (0 -> 1)                   1
knowledge files (60 -> 61)                     61
```

`registry rows = 66` matches **claims-erratum-1 E1** (63 + S064 mined + S065 + S066 rejected), which
repairs the frozen `63 -> 64` contradiction in the C2 counting command. The mined-status probe still
reads `1` — only `S064` is `mined`.

### 4.2 The instruments (mirror)

```
$ python3 corpus/instruments/frontier-recheck-count.py --root <mirror>
PASS     F24  knowledge/rfc-9116-security-txt.md                  ids=S063  exit=0
PASS     F25  knowledge/cve-json-record-format.md                 ids=S064  exit=0
entries=28 pass=28 exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <mirror>
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=56 with_url=56 with_fetched_utc=18 with_archival=38 snapshot_dirs=18 manifest_dirs=18 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=56 bound=56 unbound=0
exit=0   (0 FAIL lines)

$ python3 corpus/instruments/recheck-audit.py --root <mirror> --quiet
lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0
expect=present expected=61 missing=0 unexpected=0
```

The recheck-audit's **strict** `cdroot` limb reads `strict pass=2/61 cdroot_fail=59` on the mirror and
the exit is 1. That is a **mirror artifact, not a defect in these bytes**: the strict limb requires each
line's `cd <path>` to equal the *audited* root, and the 59 pre-existing entries `cd` the real lane
while the audited root is the scratch mirror. Two controls settle it:

```
# control A — the real, unmodified lane (nothing of mine landed yet):
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=60/60 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0

# control B — the mirror with every entry's cd target repointed at the mirror:
strict pass=61/61 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=61 missing=0 unexpected=0 exit=0
```

Control B is the decisive one: with the `cd` targets agreeing with the audited root, all **61/61**
entries pass every strict limb including my new one, and the audit exits 0 with `expected=61
missing=0 unexpected=0` — the three numbers the C2 kill rule names. The frozen limbs (a)-(c) already
read `pass=61/61` on the mirror without any repointing.

### 4.3 Sources census (scratch fleet root with a `kasegi` conf row)

```
$ bash scripts/sources-census.sh validate --root <fleet> --today 2026-10-28 kasegi
kasegi	unlisted	<fleet>/kasegi-shokunin
kasegi	W04	S028 duplicate url docs.hackerone.com/… across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/… across scopes
kasegi	ok	<fleet>/kasegi-shokunin/corpus/SOURCES.md
validate exit=0

$ bash scripts/sources-census.sh census --root <fleet> --today 2026-10-28 kasegi
kasegi	rows	66
kasegi	tier.A	61   tier.B	3   tier.C	2
kasegi	status.mined	54   status.rejected	12
FLEET	rows	66   FLEET	missing	0
census exit=0
```

`ok`, exit 0, and the **only** warnings are the two standing W04s (S028, S029) — no new W or E code.
No E-code fired: `NF=13` on all three rows, kind `spec`, tier `A`, status `mined`/`rejected`, opened
`2026-10-28` (not future), recheck `on-release` (a symbolic cadence), used-by path present for the
mined row, `—` for the rejected rows. The three new rows' URLs are distinct from every existing
registry row's URL after census normalisation, so no new W04 fires.

### 4.4 Pure addition, zero deletions

```
corpus/README.md removed/added                 0 / 28
PROVINCE.md removed/added                      0 / 2
corpus/SOURCES.md removed/added                0 / 3
```

No tracked line is deleted or reworded anywhere — the claim's "any tracked deletion in corpus paths" kill
clause cannot fire on these bytes.

## 5. Landing recipe — measured on the round-41 landed bytes, not assumed

The round-41 integration commit `03ca614` is the reference. Re-derived from the committed bytes:

```
== the round-41 reference landing (commit 03ca614) ==
-- corpus/README.md
   landed == prev + deliverable                : False
   landed == prev.rstrip(\n) + \n + deliv + \n : True
-- PROVINCE.md
   landed == prev + deliverable                : True
   landed == prev.rstrip(\n) + \n + deliv + \n : False
```

So the recipes are:

- `corpus/README.md`:
  `landed = prev.rstrip(b"\n") + b"\n" + <readme-row.txt> + b"\n"`
  (the deliverable itself starts with `\n`, so the block is separated by exactly one blank line, and the
  file ends with one trailing newline — matching the committed file's current shape)
- `PROVINCE.md`: `landed = prev + <province-amendment.txt>` (the deliverable starts with `\n`, giving one
  blank separator line)
- `corpus/SOURCES.md`: the three rows are inserted **immediately after the `| S063 |` row** (line 69),
  which is the last row of the `## Registry` section (`## Registry` starts at line 3, `## Paths` at line
  71), so census `E12` ("row-shaped source outside the Registry section") cannot fire.

Both recipes apply cleanly to my bytes (checked in `landing_recipe.py`):

```
README: recipe applies cleanly, result 58225 bytes, ends b' stays outside it.\n\n'
README: the applied block starts with b'\n## Round-42 admission \xe2\x80\x94 coverage map '
PROVINCE: recipe applies cleanly, result 13140 bytes, ends b'at.md (source S064)\n'
SOURCES: insertion point after line 69 (| S063 | RFC); next non-blank line is ''
SOURCES: the ## Registry section spans line 3..69 (## Paths at 71)
```

**Insertion order (E11).** `used-by corpus/knowledge/cve-json-record-format.md` must exist on disk when
the census runs, so `S064`'s row and the entry must land in the same step; a row-only landing fires
census `E11`. My `knowledge-expected.txt` deliverable carries the matching entry line, so the three land
together.

**`knowledge-expected.txt` is a pure one-line insertion.** Verified by diff against the committed file:

```
added/removed lines                            1 / 0
added line                                     corpus/knowledge/cve-json-record-format.md
```

I deliberately did **not** re-sort the file. The committed `knowledge-expected.txt` is not globally
sorted (`rfc-9116-security-txt.md` sits one line above its sorted position, before
`retirement-autopsies.md`), and the audit compares the expected list to the tree **as a set**
(`recheck-audit.py`: "set equality between the listed entries and the audited tree's actual
`corpus/knowledge/*.md` entries"). Re-sorting would move an unrelated committed line for no measurement
gain; my insertion adds exactly one line and preserves every other byte. The `ScribeC2Entry` seat
measured the same seam independently (index 19 of the 60 entry lines) and asked for exactly this
pure-insertion form.

## 6. Content decisions, and the two corrections I made to the scout's suggestion

1. **No `5.x` in the topic cell.** The scout's facts proposed a frontier topic reading "CVE Record
   Format 5.x". The capture says otherwise in a way worth being precise about: `dataVersion` (L479-L484)
   has a `pattern` accepting any `5.x` (L482) and a `default` of `5.2.0` (L483), so the schema *names a
   version family and one default*, not a fixed edition. My `F25` topic cell therefore says "CVE JSON
   record format (CVE Record Format)" — the schema's own `title` (L4) — and no version number appears
   in it. The `5.x`/`5.2.0` facts live in the `S064` anchor and teaches cells and in the entry's Claim 1,
   where the pattern and the default are both pinned. I told the `ScribeC2Entry` seat the same thing
   before it filed, and its entry title carries no version number.
2. **No `adp` claim overstated.** The `adp` array belongs to the **Published** branch only: the
   Published branch's `containers` has `cna` (L3482-L3483) and `adp` (L3485-L3492) and requires `cna`
   (L3494-L3496), while the Rejected branch's `containers` has `cna` only (L3526-L3527), requires `cna`
   (L3530-L3532) and closes with `additionalProperties: false` (L3533) — no `adp` property at all. My
   row's scope cell says "exactly one `cna` container plus optional `adp` containers" and the anchor
   names both root branches (Published L3464-L3507, Rejected L3508-L3543), so the qualification is
   carried by the anchor rather than asserted loosely; the `F25` next cell states the same split and
   cites each half (`S064.txt:L3494-L3496`, `S064.txt:L3530-L3532`, `S064.txt:L3485-L3492`).
3. **`kind = spec`, `tier = A` for all three rows.** The picked document is a normative JSON Schema
   (draft-07) published by the CVE Program itself — primary first-party, so tier `A`, and `spec` is in
   the census's kind enum. The two rejected rows are also `spec`/`A`: they are *rejected on scope
   grounds*, not on quality, and the row's `teaches` cell says so explicitly (the OSV schema is itself
   "a primary first-party normative spec" per the scout's screen). Marking a rejected-but-primary row
   `spec`/`A` keeps the tier a statement about the document's standing rather than about the lane's
   decision — the `status` cell carries the decision.
4. **recheck `on-release` for S064.** The schema is versioned (`dataVersion` 5.x, default 5.2.0) and the
   lane already uses `on-release` for the two other versioned normative captures it holds (`S055` CSAF
   2.0, `S063` RFC 9116). The rejected rows carry `on-release` as well, matching `S056`/`S059`
   (rejected rows with a versioned upstream).
5. **Both rejects land as rows, not only in the Gate.** The scout filed two rejects; `claims-erratum-1`
   E1 fixes the concrete registry after-value at 66, i.e. `S064 + S065 + S066`. My `S065`/`S066` rows
   carry the reject's URL, access date, a located ≤25-word quote, the honest reason and the flip
   condition in the `teaches` cell, so the D-r41-2 evidence exists in the registry as well as in the
   lesson's Gate block. Neither rejected row gets a manifest record — capture-binding rule **B3**
   (`rejected-row-anchor`) fails a capture that tries to anchor a rejected row, so the manifest holds
   the `S064` record only and binding stays `records=56 bound=56 unbound=0`.

## 7. Risks, dependencies and observations for the L1

1. **Landing order (census E11).** `S064`'s `used-by` path must exist on disk when the census runs. Land
   the `S064` row, the entry and the `knowledge-expected.txt` line in the same step.
2. **Entry/`cd` seam.** The entry's `recheck:` line `cd`s the real lane. It exits 0 once
   `corpus/source-snapshots/round-42/manifest.json` and `S064.txt` are landed; before that it fails
   closed with exit 2 (absent). The mirror measurement in §4.2 repointed only that `cd`; the real-lane
   behaviour is the fail-closed one until the capture lands.
3. **`knowledge-expected.txt` insertion point.** One line, at the sorted seam between
   `cve-bench-agent-exploitation-benchmark.md` and `cvss-v4-severity-and-vector.md`. The file's existing
   order is preserved (§5) — including the pre-existing `rfc-9116-security-txt.md` off-by-one that is
   outside both my item and the scribe's.
4. **SOURCES.md line shift.** Inserting three rows after `S063` shifts `## Paths` and everything below
   by three lines. `corpus/lessons/*.md` cite `corpus/SOURCES.md:NN` in several places (r25, r28, r29,
   r31); round 40 inserted three rows the same way without re-basing them, so this is the established
   pattern, but it is a real number shift. Nothing I deliver cites `SOURCES.md` by line.
5. **The F25 frontier row is one `F`-row, but the README's `## Frontier` table also needs the row.** My
   `readme-row.txt` is the whole appended `## Round-42 admission` block, matching the round-40/41 shape
   byte-for-byte in structure (heading, R6 paragraph, coverage-map row, frontier row, count line). It
   contains exactly one `| F25 |` row, so `grep -cE '^\| F[0-9]+ \|' corpus/README.md` reads 25 and the
   harness's `FRONTIER_ROW` regex reads the row from the appended block (the same place F13-F24 live).
6. **The `F25` next cell is 108 words**, matching F23's 109-word cell (F24's is 123) — the file's
   established style. It quotes only spans I re-opened in the capture and cites them by
   `S064.txt:L<n>`, the citation form the neighbouring rows use. Every one of its seven line
   citations was re-opened and prints the construct it names (L3500/L3536 the two root `required`
   arrays, L472 `dataType`, L479 `dataVersion`, L3494/L3530 the two `cna` `required` arrays, L3485 the
   `adp` property, L3510 the Rejected branch's description).
7. **The claim's `63 -> 64` registry counting command is superseded by `claims-erratum-1` E1** (`66`).
   My rows implement the erratum's concrete after-value; the mined-status probe (`0 -> 1`) is
   unaffected. Flagging it so the L1 does not read 66 as a drift against the frozen command.
8. **`F24`/RFC 9116 is untouched and unreferenced** by my bytes — it is neither a candidate, a comparison
   nor a flip target in any cell I wrote.

## 8. Report path

`.ufo/waves/round-42/wave1/ExecC2Rows.md` (this file). Deliverables beside it:
`ExecC2Rows.registry-rows.txt`, `ExecC2Rows.readme-row.txt`, `ExecC2Rows.province-amendment.txt`,
`ExecC2Rows.manifest-record.json`, `ExecC2Rows.knowledge-expected.txt`.
