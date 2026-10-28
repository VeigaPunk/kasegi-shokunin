# ScribeC2Entry — round 42 wave 1 receipt (C2 coverage: F25 = CVE JSON record format, S064 capture, knowledge entry)

Seat: `ScribeC2Entry` (leaf, no subagent dispatch). Item: deliver the byte-exact knowledge entry for the
F25 topic picked by `ScoutF25Lead` (with `ExecC2Rows`), after their pick is filed. Scratch:
`/fast/scratch/hyaku/kasegi-r42/ScribeC2Entry/` (removed before yield). No network fetch, no tool install,
no mutating git/jj, no write outside this seat's wave-1 receipt/deliverable and that scratch dir.

Pick (scout's, verified by me against the filed bytes): **CVE Record Format** — the CVE Program's bundled
JSON Schema at
`https://raw.githubusercontent.com/CVEProject/cve-schema/main/schema/docs/CVE_Record_Format_bundled.json`,
captured by the scout as `ScoutF25Lead.S064.txt` (3,545 lines / 84,520 bytes /
`b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa`). Rejected candidates in the scout's
record: OSV schema (R1), NVD API 2.0 CVE response schema (R2); GHSA API and FIRST VIN screened-not-fetched.

## 1. Deliverable

`.ufo/waves/round-42/wave1/ScribeC2Entry.entry.md` — **161 lines, 23,793 bytes, sha256
`7cd4f14c598f62eabcfc130e172a09d24595e32cfd2d5f575d3f6e9826ead61f`** (`wc -lc` and `sha256sum` on the filed
file; `cmp` against the scratch copy → identical). The L1 copies it **byte-exact** to
`corpus/knowledge/cve-json-record-format.md`; it contains only landable entry text — no splice markers, no
validation tables, no headings that are not part of the entry.

Structure (measured on the filed bytes): H1 line 1; blank line 2; header lines 3-6 in the lane order
`source:` → `verified-at:` → `ground: F25` → `recheck:`; 13 `##` sections; 18 blockquote lines (17
S064-anchored claims + 1 S031 seam quote); exactly one `source:` line, one `recheck:` line, one `ground:` line.
No BOM (`head -c 8` → `23 20 43 56 45 20 4a 53`), final byte `\n`, zero lines with trailing whitespace
(`grep -cE ' +$'` → 0).

Title carries no version number, per `ExecC2Rows`' coordination note; the version evidence lives in Claim 1
(`dataVersion` pattern `^5\.(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))?$` at L482, `default: "5.2.0"` at L483).

The `recheck:` line as landed (one line, `bash -n` rc 0):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json --source S064   # prints S064:sha256 OK then one S064:Q<n> OK line per pinned quote with its occurrences= count and anchor=N-ok note; exits 2 when the manifest or capture is absent and 1 when the digest differs or a pinned quote moved — a pinned-capture comparison, not a fresh network check
```

The `#` note contains no `--source` for another id and no `--selftest` (the two harness traps in
`RevC2Entry` A4).

## 2. Inputs read

| path | use |
|---|---|
| `.ufo/waves/round-42/claims.json` | frozen C2 predicate, kill rule, counting commands |
| `.ufo/waves/round-42/c2-controls/before.txt` | before-state (frontier 24, registry 63, knowledge 60, harness 27/27, binding 55/55, audit expected=60) |
| `.ufo/waves/round-42/wave1/ScoutF25Lead.S064.txt` | **the capture bytes the entry anchors to** (byte-identical to `ScoutF25Lead/cve.collapsed` by `cmp` before the scout's scratch removal) |
| `.ufo/waves/round-42/wave1/ScoutF25Lead.manifest-record.json` | the Gate pins Q1 L5 / Q2 L3466 / Q3 L3510, url, fetch facts |
| `.ufo/waves/round-42/wave1/ScoutF25Lead.reject-record.txt`, `ScoutF25Lead.facts.txt` | screen result and fetch ledger |
| `corpus/knowledge/cyclonedx-analysis-subtree.md`, `corpus/knowledge/rfc-9116-security-txt.md` | model entries (trio, Claims, FC block, rejected list, honest limit) |
| `corpus/QUALITY.md` (Q1-Q6), `corpus/instruments/{source-recheck,frontier-recheck-count,recheck-audit,capture-binding-check}.py` | admission bar and the exact limbs the entry must satisfy |
| `.ufo/waves/round-42/wave1/RevC2Entry.md` | reviewer's acceptance checklist A-L (used as the test plan) |
| `corpus/source-snapshots/round-23/S031.txt`, `round-38/S055.txt`, `round-40/S060.txt` | the three cross-references the entry cites (each opened at the cited lines) |

## 3. Provenance and network

**This seat made no network request.** The capture is the scout's filed artifact; its fetch ledger, from the
scout's manifest record and facts, is:

```
2026-10-28T11:06:45Z  HTTP 200  133,616 raw bytes  3,545 raw lines
  sha256(raw)      44c703322b1fcc532bc1c93f3993a0ba042c1a2831aae8cf39c4fbb707d03c8f
  snapshot         3,545 lines / 84,520 bytes  sha256 b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa
2026-10-28T11:09:10Z  instrument refetch  HTTP 200  133,616 bytes, snapshot sha256 identical, cmp of the two capture files exit 0
```

I re-measured the filed capture myself: `wc -lc` → `3545 84520`, `sha256sum` → `b90a51f7…`, `cmp` against the
scout's collapsed body → identical. The entry's `source:` line copies those numbers and the manifest URL
byte-for-byte (checked by the fixture's binding run, §4.3).

## 4. Validation actually run (all in scratch; nothing written into the lane corpus)

Scratch: `S=/fast/scratch/hyaku/kasegi-r42/ScribeC2Entry`. Disk guard read first:
`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → green (`/tmp` 5%, `/var/tmp` 36%,
`/fast/scratch/hyaku` 27%).

### 4.1 Quote, anchor and header validator (`$S/validate.py`, written for this seat)

```
$ python3 validate.py --entry entry.md --capture S064.txt --sid S064 --ground F25
note: anchors not in ascending document order
entry_lines=161 quoted_spans>=4w=17 anchored=17 skipped=9 max_words=24
skipped_spans=[(84, 0, 'MUST meet any requirements set by any ap'), (92, 0, 'SHALL exist as machine readable flag'), (145, 0, "The CNA Rules define the CVE Record's fi"), (146, 0, 'A CVE Record has a severity.'), (147, 0, '`status: unaffected` is a VEX not-affect'), (148, 0, 'An omitted version status means the vers'), (149, 0, 'A rejected CVE ID is deleted.'), (150, 0, '`state` records investigation status or '), (151, 0, 'This document specifies CVE Record Forma')]
citation_lines=[16, 20, 26, 30, 34, 36, 40, 46, 52, 56, 62, 70, 74, 78, 96, 98, 100, 116, 131, 137, 139]
anchors=[5, 480, 129, 344, 354, 421, 449, 3479, 809, 693, 3466, 1077, 1082, 3190, 778, 790, 3510]
problems=0
```

What the numbers mean:

- 17 S064-anchored quoted spans, each verbatim under the instrument's own normalization
  (`" ".join(MARKUP_RE.sub("", text).split())`), each occurring **exactly once**, each ≤25 words (max 24), and
  each declared line holding its own quote within the instrument's 4-line window.
- 21 entry lines cite `S064` outside the declaration lines (`frontier-recheck-count` rule A's citation limb).
- The 9 skipped spans are not S064 quotes: 2 are the foreign citations (`S031.txt:L112` blockquote and the
  inline `S055.txt:L2151` span, both verified in their own captures — §4.5), and 7 are the rejected
  over-generalization labels, which are assertions a reader might make, not source text (the F23 precedent).
- Anchors are not in ascending document order. That is deliberate: the claims follow the schema's own
  narrative (top-level description → definitions → root branches), not line order, and no lane instrument
  requires ascending anchors; the prior round's ascending rule existed only for placeholder splicing, which
  this entry does not use.

### 4.2 `source-recheck.py` against the scout's manifest record (exit 0)

```
$ cp ScoutF25Lead.S064.txt $S/rc/S064.txt
$ cp ScoutF25Lead.manifest-record.json $S/rc/manifest.json
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/source-recheck.py --manifest $S/rc/manifest.json --source S064
S064:sha256 OK
S064:Q1 OK occurrences=1 anchor=5-ok
S064:Q2 OK occurrences=1 anchor=3466-ok
S064:Q3 OK occurrences=1 anchor=3510-ok
EXIT=0
```

All three Gate pins are inside the entry, verbatim, in three different limbs: Q1 on entry line 16 (Claim 1),
Q2 on line 62 (Claim 4), Q3 on line 100 (Claim 7) — so the manifest's own assertions exercise three limbs,
not one.

### 4.3 Fixture lane: the three integration instruments

`mkfix.sh` copies the lane's `corpus/` into `$S/fix`, places `S064.txt` + `manifest.json` at
`corpus/source-snapshots/round-42/`, the entry at `corpus/knowledge/cve-json-record-format.md` (its `cd`
rewritten to the fixture **in the fixture copy only**), one synthesized 13-cell S064 row (spec / A / mined /
2026-10-28 / on-release / `used-by corpus/knowledge/cve-json-record-format.md` / the manifest URL), one F25
README row, and the `knowledge-expected.txt` line.

```
$ cd $S/fix && python3 corpus/instruments/frontier-recheck-count.py --root .
... PASS F24 ... PASS F25 knowledge/cve-json-record-format.md ids=S064 exit=0
entries=28 pass=28 exit=0                                    # rc 0

$ python3 corpus/instruments/capture-binding-check.py --root .
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
... records=56 bound=56 unbound=0                            # rc 0

$ python3 corpus/instruments/recheck-audit.py --root . --json $S/audit.json --quiet   # per-entry, my line
# JSON record for cve-json-record-format.md:
#   limbs {parse:true, cwd:true, paths:true}
#   strict {parse:true, cwd:true, paths:true, cdroot:true, instrument:true, own:true}
#   lane_exit=0 foreign_exit=0
#   lane_output_sha256 = foreign_output_sha256 = 894e3d7744eae96a1fd1a5954bf3743f9f5a42222756e95711be0c1bf267bf70
```

Global audit behaviour on the fixture, stated precisely because the fixture is not the lane:

- First run, only my entry's `cd` rewritten → `strict pass=2/61 cdroot_fail=59` — the 59 are the other
  entries still cd-ing to the real lane root, i.e. a fixture artifact. That run is used only for my entry's
  per-line record above (all six strict limbs true).
- Second run after rewriting every entry's `cd` to the fixture → `lines=61 total=61 pass=61 fail-closed=24
  parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`, `strict pass=61/61 cdroot_fail=0 instrument_fail=0
  own_fail=0`, `expect=present expected=61 missing=0 unexpected=0 exit=0`.

So the entry adds a 61st knowledge file that passes the strict audit, and the fixture reproduces the frozen
`entries=28 pass=28`, `records=56 bound=56`, `expected=61` shapes. The landed tree needs no fixture edits;
the lane's own entries already `cd` to the lane root.

### 4.4 Grammar and parked-topic checks on the filed deliverable

```
$ grep -c "9116\|F24\|S063\|security.txt" ScribeC2Entry.entry.md      -> 0
$ grep -nE '^([-*]|[0-9]+[.)]) +`?S[0-9]{3}' ScribeC2Entry.entry.md    -> (no lines)
$ grep -c '^source:'  -> 1 ; grep -c '^recheck:' -> 1 ; grep -c '^ground: F25' -> 1
$ grep -cE ' +$' -> 0 ; wc -l -> 161 ; head -c 8 | xxd -> 2320 4356 4520 4a53  ("# CVE JS")
```

F24 / RFC 9116 is parked and the entry never names it, its source id or its document (0 hits). No list item
starts with an S-id, so harness rule A cannot mistake a cross-reference for a declaration.

### 4.5 Counted numbers behind the entry's claims (commands and outputs)

On `S064.txt`:

```
$ for w in MUST "MUST NOT" SHALL SHOULD should MAY may VEX product_status known_affected \
           not_affected under_investigation justification CSAF CycloneDX SBOM severity score CVSS adp cna PUBLISHED REJECTED; do
    printf '%-22s %s\n' "$w" "$(grep -oF -- "$w" S064.txt | wc -l)"; done
MUST 2          MUST NOT 1      SHALL 0        SHOULD 0       should 10
MAY 0           may 10          VEX 0          product_status 0
known_affected 0  not_affected 0  under_investigation 0  justification 0
CSAF 0          CycloneDX 0     SBOM 0         severity 11    score 17
CVSS 14         adp 9           cna 17         PUBLISHED 9    REJECTED 9

enum sizes (lines between "enum": [ and ]):  tags 19 (L51-L69)  status 3 (L132-L134)
  dataType 1 (L476)  published state 1 (L531)  rejected state 1 (L579)
required sets: root 4 (L3500-L3505, L3536-L3541); cveMetadata 3 (L488-L492, L540-L544);
  cnaPublished 4 (L765-L769); cnaRejected 2 (L798-L801); providerMetadata 1 (L606-L608);
  adpContainer providerMetadata + minProperties 2 (L877-L880)
severity occurrences = 3 severityType definitions (L1592, L2152, L2832) + 7 `$ref`s (L1634, L2343,
  L2358, L2397, L2898, L2913, L2952) + 1 credits sentence (L3305) = 11
Rejected containers block L3522-L3534: `"adp": {` count 0
```

Cross-capture checks (each cited line opened before use):

```
corpus/source-snapshots/round-40/S060.txt L5-L15   6 analysis states (resolved, resolved_with_pedigree,
  exploitable, in_triage, false_positive, not_affected); L16-L29 9 justification values;
  L15 "Justification should be specified for all not_affected cases."; L105 `Type: enum (of string) Default: "affected"`
corpus/source-snapshots/round-38/S055.txt L2151    impact-statement flag sentence, occurrences=1
corpus/source-snapshots/round-23/S031.txt L112     "MUST meet any requirements set by any approved formats..."
  occurrences=1; L102 rejection-formats sentence, occurrences=1
```

Foreign-quote counts were checked in their own captures (S031 span 18 words, count 1; S055 span 9 words,
count 1), so the two non-S064 quotations are pinned the same way S064's are.

## 5. QUALITY compliance (the parts this seat controls)

| id | how the entry meets it |
|---|---|
| Q1 | lines 3-6 directly under the H1: `source: S064 — <URL> — capture corpus/source-snapshots/round-42/S064.txt (lines, bytes; sha256)`, `verified-at: 2026-10-28 (...)`, `ground: F25`, one-line `recheck:` |
| Q2 | one tier-A row (the CVE Program's own bundled schema), opened this round; no tier-C support |
| Q3 | 17 anchored spans, verbatim, ≤25 words (max 24), each exactly once; every number copied from a command output in §4.5, none retyped from memory |
| Q4 | every rule attributed to the document ("the schema", "this schema"), never generalized; the captures' non-CNA practice is not asserted |
| Q5 | `**Falsifiable rule.**` with limbs (a)-(f) and FC-1…FC-7 checks; 7 numbered rejected over-generalizations, each falsifiable against a line cite or a zero-count |
| Q6 | documentation only: no probing/scanning/login/submission instruction, no credential, session, private URL or op-scheme reference |
| Q7 / Q10 | `recheck:` is one `bash -n`-parseable command whose output names what it checked; exit 2 (absent) / exit 1 (digest or moved quote) are stated; `cd <lane-root> &&` prefix |
| Q9 | all S064 spans unique; the anchor form `— S064.txt:L<n>` is used, not a backticked `path:NN` |
| R12 | `--source S064` equals the entry's only declared id |

## 6. `RevC2Entry` checklist mapping (A-L)

| item | status |
|---|---|
| A1-A3 | H1 line 1; four header lines 3-6; `source:` starts `S064`; numbers copied from `wc`/`sha256sum`; `verified-at` gives the 2026-10-28 fetch facts (HTTP 200, 133,616 raw bytes, sha256 `44c703…`) |
| A4-A5 | one `recheck:` line, `cd` prefix, `source-recheck.py --manifest … --source S064`, note free of foreign `--source` and `--selftest`; no second `source:` line; no list item starts with an S-id |
| A6 | 21 lines cite S064 outside the declaration lines |
| B1 | 7 claim limbs + Attribution + comparison + usage + checks + rejected + limit; every claim limb has ≥1 blockquote |
| B2 | §4.1: 17/17 unique, ≤25 words, declared line holds the quote |
| B3 | the manifest's Q1/Q2/Q3 land in three different limbs (entry lines 16, 62, 100); no Q-id is decorative |
| B4 | counted numbers with commands in §4.5 and in the entry's FC-3/FC-4 |
| B5 | verb census in FC-1 (`MUST` 2, `MUST NOT` 1, `SHALL`/`SHOULD`/`MAY` 0, `should` 10, `may` 10) and every claim names its verb |
| B6 | lane readings are labelled "Lane reading, not a quote:" |
| B7 | attributed to the CVE Program's schema, not to "vulnerability data" in general |
| C1 | no-overlap command and result recorded in §10 below |
| C2 | F07 line drawn in Claim 6 and rejected over-generalization 1; F21/F23 lines drawn in Claim 7 and the comparison table |
| C3 | 0 mentions of F24 / RFC 9116 / S063 (grep in §4.4) |
| C4 | exactly one entry path for F25 |
| D1-D3 | 7 numbered rejections, each with a line cite or zero-count; falsifiable rule (a)-(f) plus FC-1…FC-7 |
| E1-E3 | `## Honest limit` covers full-document scope, schema-not-prose, no edition line, raw-vs-snapshot digests, no producer practice, conformance level; final sentence is the documentation-only form |
| F1-F2 | 7 numbered researcher uses, each line-cited, item 6 states what the document does not let a reader conclude; comparison table cites S055/S060 lines opened first |
| G2/G5 | slug `cve-json-record-format`; `knowledge-expected.txt` insertion point measured (§7) |
| H1 | `verified-at: 2026-10-28` matches the Gate access date; the Gate quotes are the manifest's |

## 7. What must land around this entry (not this seat's writes)

1. `corpus/knowledge/cve-json-record-format.md` ← this deliverable, byte-exact.
2. `corpus/SOURCES.md` S064 row (ExecC2Rows): kind `spec`, tier `A`, status `mined`, opened `2026-10-28`,
   recheck `on-release`, `used-by` **exactly** `corpus/knowledge/cve-json-record-format.md`, source cell one
   `https://` token byte-equal to the manifest `url` (capture-binding B4/B5; the fixture run proves it).
3. `corpus/README.md` F25 row with entry cell `knowledge/cve-json-record-format.md` (fixture: 25 rows,
   `entries=28 pass=28`).
4. `PROVINCE.md` F25 amendment (ExecC2Rows/ScribeC2Gate).
5. `corpus/instruments/knowledge-expected.txt`: insert `corpus/knowledge/cve-json-record-format.md` between
   line 21 (`corpus/knowledge/cve-bench-agent-exploitation-benchmark.md`) and line 22
   (`corpus/knowledge/cvss-v4-severity-and-vector.md`) — measured with `bisect` over the current 60 entry
   lines: index 19. Without it `recheck-audit.py` prints `unexpected=cve-json-record-format.md`.
6. `corpus/source-snapshots/round-42/S064.txt` = `ScoutF25Lead.S064.txt` and `manifest.json` =
   `ScoutF25Lead.manifest-record.json`, unchanged (the fixture's 56/56 binding and the entry's recheck were
   both run against exactly those bytes).
7. Census E11 path-exists: the row's `used-by` target must exist at census time, so land 1 before/with 2.

## 10. No-overlap check (the claim the entry makes about lane coverage)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -rniE 'osv\.dev|OSV schema|CVE Record Format|cve-schema|CVE JSON 5|cveMetadata' \
    corpus/knowledge corpus/SOURCES.md corpus/README.md PROVINCE.md corpus/source-snapshots/*/manifest.json | wc -l
0
$ grep -liE 'osv|CVE Record Format|cve-schema' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/*.md | wc -l
0
```

The scout's facts additionally record the only adjacent artifacts (kaidoku S015 OSV record instance, mori
S012 GHSA page) and the single incidental "CVE Record Format" mention inside S031's CNA-rules prose — none of
which is a document capture of this format.

## 8. Limits of this seat's evidence

- **No network fetch by this seat.** The capture is the scout's artifact; I verified its bytes (`wc`, `sha256sum`,
  `cmp`) but did not re-fetch the URL. A URL that changes after 2026-10-28T11:06:45Z cannot be detected by
  this entry; `recheck:` compares the pinned capture only, as its note says.
- **Fixture runs are not lane runs.** §4.3 proves the entry, the capture, the manifest record and the row shape
  satisfy `frontier-recheck-count`, `capture-binding-check` and `recheck-audit` on a corpus copy. The global
  `61/61 exit 0` required rewriting 59 entries' `cd` targets to the fixture; the landed tree needs no such
  rewrite, but the L1's own integrated run is what counts.
- **Rows, README, PROVINCE and manifest are other seats' deliverables.** The fixture used one synthesized
  13-cell S064 row and one F25 row to test the seam; if `ExecC2Rows` lands different cell text, the shape is
  still fine but the binding/census verdicts must be re-read from its files.
- **Foreign citations are limited to what the entry needs:** S031 L112/L102, S055 L2151, S060 L5-L29/L15/L105.
  Each line was opened before citing; no other lane source is claimed.
- **The entry is 161 lines** — longer than F24 (53), shorter than F23 (322). The extra length is the seam
  claim (Claim 6) and the counted-required-set checks; no section repeats another.

## 9. Tooling and scratch

- No install or upgrade; no `pacman` (host pause respected); no writes to any PATH directory.
- No mutating git/jj anywhere; no fixture git repo was needed for this item.
- Scratch `/fast/scratch/hyaku/kasegi-r42/ScribeC2Entry/` held `validate.py`, `mkfix.sh`, `entry.md`,
  `S064.txt`, `rc/`, `fix/`, `audit.json`; it is removed at yield (`rm -rf`), after the deliverable and this
  receipt were copied into the wave dir.
- Files written this seat: `.ufo/waves/round-42/wave1/ScribeC2Entry.entry.md` and this receipt. Nothing else in
  the lane, the fleet root, sibling lanes or source trees was touched.
