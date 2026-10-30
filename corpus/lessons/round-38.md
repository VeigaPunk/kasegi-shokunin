
# Round 38 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims-freeze commit
`9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; wave spec/dispatch commit `700153593eb586c70a6499c8ca225ee4d673bc9b`.
judged head: export-ref of `.ufo/waves/round-38/final-gates/all-gates.txt` (QUALITY R33 — this file cannot name the
commit that contains it; the report names it).

Shape: **one v2 wave** `kasegi-r38-build`, **73 seats** — executor 21, scribe 15, reviewer 11, critic 7,
mutation-tester 6, scout 6, connector 3, sentinel 2, simplifier 2; attack seats (reviewer + critic +
mutation-tester) 24/73 = 32.9 %; m_flash-routed roles (executor, scribe, critic, sentinel, simplifier) 47/73 =
64.4 %. Validated under policy v2 (`.ufo/waves/round-38/wave1-dispatch.json`, 73 tasks). The L1 held the
planner seat (the validator rejects `planner`). Integration: the L1 landed seat deliverables byte-exact from
their `wave1/<Seat>.<suffix>` files (deliverable discipline against D-A), except where a non-author grade
corrected them (named below).

## Frozen claims — before → after

| Claim | Axis | Before (frozen control at base) | After (integrated tree = judged head content) |
|---|---|---|---|
| **C1** | depth:verifiability (4, held) | `r38-closure.sh` absent; D-A..D-F open as listed in `.ufo/waves/round-38/c1-controls/before.txt` (no `Correction (round 38)` lines; README fence open at EOF from L426; no declared-blocks/all-gates; 7 pending-marker lines in the round-37 lesson; r37 judged head without its results file; 1 `Final lane commit:` label in the round-37 SCORECARD section; `kasegi-r37/build-spec.py` left in scratch; empty ledger section) | suite landed (sha256 `85d33ea9…`, 1473 lines); `closed=8/8 exit=0` and `selftest cases=8 failures=0` over the judged head are the receipt `.ufo/waves/round-38/final-gates/all-gates.txt`; base and r37 reviewed-head reds in `final-gates/reds.txt` |
| **C2** | coverage (7, held) | frontier 20; registry 54; S055 rows 0; knowledge 49; harness `entries=23 pass=23`; binding `records=44 bound=44`; audit `expected=49` | frontier 21; registry 55; one entry cites `source: S055`; knowledge 50; harness `entries=24 pass=24 exit=0` incl. `PASS F21 … ids=S055`; `source-recheck --source S055` exit 0 (Q1–Q4 `occurrences=1`); binding `records=45 bound=45 unbound=0`; audit `expected=50 missing=0 unexpected=0 exit=0`; census exit 0 (W04 S028/S029 only); junk twin rejected (`.ufo/waves/round-38/c2-controls/junk-f21-recheck.txt`, 4× `quote-not-found`, exit 1) |
| depth:density | 9 | `SKILL.md` 1113 lines | one EOF registry row appended (1114 lines); base lines byte-identical; no move claimed |

Capture note (C2): the CSAF page is served behind Cloudflare. `capture-source.py`'s urllib fetch received
415,225 raw bytes (sha256 `0fbc5857…`), curl received 414,858 (sha256 `fad0c60d…`); the difference is one
injected `<script … beacon.min.js …>` element, which `html_to_text()` removes, so both normalize to the same
`S055.txt` (sha256 `63c8ad52…`, 272,441 bytes, 5146 lines — measured by the L1 and by ExecC2Capture
independently). The manifest records the curl fetch; the snapshot hash is the binding.

## Gate

### Admitted — F21 / S055 (OASIS CSAF v2.0, the VEX profile's product status and justification flags)

- **Row.** `corpus/SOURCES.md`, inserted immediately after the `S054` row (base `:60`) as new line 61, i.e. the last row of the `## Registry` table and not a new section: `awk -F'|'` → `NF=13` (11 cells), id `S055`, kind `spec`, tier `A`, status `mined`, opened `2026-10-26`, recheck `180d`, used-by `corpus/knowledge/csaf-vex-product-status-and-justifications.md`, one `https://` token in the source cell equal to the manifest `url`. The landed line is byte-identical to the row deliverable `wave1/ScribeRowS055.row.md` (1 line, 1,713 bytes, sha256 `901309af744b32383f3c8fe4c8023a960201baa65028600f0b9c31da59ff96cc`). Position is enforced, not stylistic: a row appended after `## Paths` validates as `file E12 S055 row outside Registry section` exit 1 (`wave1/ExecC2Census.md` §6). Landing order is enforced too: the row without the entry prints `file E11 S055 missing used-by corpus/knowledge/csaf-vex-product-status-and-justifications.md` exit 1, so row and entry land in one commit (`wave1/ScribeRowS055.md` §4).
- **Three row drafts existed; one landed.** Besides the landed scribe row, `wave1/ExecC2Census.md` §DELIVERABLE (818 bytes, sha256 `caa476c1…cee82c`, prose anchors) and `wave1/ExecCsafStatus.md` §DELIVERABLE (a 318-byte scope cell, sha256 `0d7892e5…de1e2`) drafted the same slot, and the `corpus/SOURCES.md ## Registry changes` bullet in `wave1/ScribeSourcesLog.blocks.md` stated recheck `on-release` where the landed row says `180d`. Both cadences are legal under census E09 (`on-release` is a symbolic cadence carried by 15 existing rows) and every draft validated `NF=13`, so the difference was a choice, not a defect — resolved in favour of the scribe row. A spot-check reads the landed row, not a draft.
- **URL.** `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`. This seat's own fetch, `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, 2026-10-26T18:31:17Z: HTTP 200, `text/html`, 0 redirects, requested URL == effective URL, 414,858 raw bytes, sha256 `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b`; served `Date: Mon, 26 Oct 2026 18:31:18 GMT`, `last-modified: Sun, 05 Apr 2026 13:17:09 GMT`, `server: cloudflare`. Normalized with the lane's own `corpus/instruments/capture-source.py` `html_to_text`: 272,441 bytes, 5,146 lines, sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, `cmp`-identical to the landed capture at `corpus/source-snapshots/round-38/S055.txt`.
- **Access date:** `2026-10-26`; `fetched_utc` `2026-10-26T18:31:17Z`, within the same second as the served `Date` header.
- **Quotes (each ≤25 words, located, `occurrences=1`, `anchor=N-ok`).** Line numbers are 1-based lines of the `63c8ad52…` snapshot and were read by this seat, not copied:
  - Q1 — 24 words, `S055.txt:2135`: `The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability.` (second sentence of `4.5 Profile 5: VEX`, heading L2134; purpose).
  - Q2 — 25 words, `S055.txt:2844`: `For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status.` (`6.1.27.7 VEX Product Status`, heading L2843; the machine-checkable test form, not the profile requirement).
  - Q3 — 23 words, `S055.txt:2151-2152`: `For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.` (L2151 ends on `For each item in`, so the pin is a two-line block; `source-recheck` reports it as `normalized=markup-whitespace` because the manifest pins the joined reading).
  - Q4 — 19 words, `S055.txt:1767`: `vulnerable_code_not_in_execute_path: The affected code is not reachable through the execution of the code, including non-anticipated states of the product.` (definition item of the flag `label` enum, section `3.2.3.5 Vulnerabilities Property - Flags`, heading L1729).
  - Supporting located facts, each read in the same bytes: the eight `product_status` properties named in one sentence at `S055.txt:1855` and defined at L1885–L1894 (`first_affected` L1885, `first_fixed` L1886, `fixed` L1887, `known_affected` L1888, `known_not_affected` L1890, `last_affected` L1892, `recommended` L1893, `under_investigation` L1894); the five justification labels as an enum at L1757–L1761 with the sentence `The given values reflect the VEX not affected justifications.` at L1762 and per-label MUST-uses at L1763–L1769; the disjointness rule at `S055.txt:2329` (`The sets formed by the contradicting groups within one vulnerability item MUST be pairwise disjoint.`, section `6.1.6 Contradicting Product Status`, heading L2328).
- **Kind and tier reasoning.** Kind `spec`: the artifact is normative prose plus conformance tests — 194 `MUST`, 54 `SHALL`, 74 `MUST be tested`, and 88 lines that open a `6.1.*` heading (66 at the `6.1.N` level, 22 nested) — and its scope statement is a requirements statement, not commentary. Tier `A`: the URL is the producing Technical Committee's own OASIS Standard artifact served from OASIS's `docs.oasis-open.org` (`Technical Committee: OASIS Common Security Advisory Framework (CSAF) TC`, L18; `OASIS Standard`, L3; `18 November 2022`, L4), with no secondary host, summary or vendor restatement in between. This is not a vendor execution claim: the standard says nothing about which vendors publish conforming VEX documents, and `All examples in this document are informative only.` (L498).
- **Stage facts recorded rather than smoothed.** The v2.0 header's own `Latest stage` block (L13–L16) points at `https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html`, which serves Errata 01 bytes (this seat: HTTP 200, 25,631 bytes, 2026-10-26T18:33:34Z, sha256 `05ce174d…f51de`; normalized head `Common Security Advisory Framework Version 2.0 Errata 01`, `OASIS Approved Errata`, `26 January 2024`). That erratum says of itself that `There are no changes to the published CSAF document. Changes have been made only to the included Aggregator JSON schema.` and that `The conformance requirements stated in the OASIS Standard … are not changed in any way by the publication of this Errata document.`, so the four pins above are unaffected by it and the row is bound to the `csaf-v2.0-os.html` stage, never to the latest-stage URL.
- **Entry as landed.** `corpus/knowledge/csaf-vex-product-status-and-justifications.md`, 137 lines, 22,887 bytes, sha256 `0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`, byte-identical to `wave1/ScribeEntryF21.entry.md`: `source: S055 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html — capture corpus/source-snapshots/round-38/S055.txt (5,146 lines, 272,441 bytes; sha256 63c8ad52…)`, `verified-at: 2026-10-26`, `ground: F21`, and an executable `recheck:` line selecting `--manifest corpus/source-snapshots/round-38/manifest.json --source S055` from a `cd`-prefixed lane root. Its citation set is inside the bytes this seat read (L394, L498, L502, L1855, L1887–L1894, L2069–L2075, L2135, L2152, L2156, L2844). Two earlier revisions wore different digests (`545303c7…`, and `96899762…` in the row seat's mirror), so any census or audit claim must name the bytes it read; at this head the landed entry and the wave-1 deliverable are the same bytes.
- **Frontier row as landed.** `corpus/README.md`, 1 line, 1,267 bytes, sha256 `17743c05a1451d2cf5c505deb71a66f86c7131d0556638a4d5ba7245d0c8488f`, `awk -F'|'` → `NF=8`, the shape of F19/F20 and the `## Frontier` header at `corpus/README.md:200`. It cites `S055.txt:2135`, `:2844` and `:2152`; the L2135 and L2152 quotations are verbatim, while the L2844 clause is condensed to `every vulnerability item MUST carry at least one of fixed, known_affected, known_not_affected or under_investigation in product_status` — a faithful paraphrase of the test sentence, but the entry, not the row, carries the verbatim form.
- **Recheck, measured at the committed paths.** `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055` prints `S055:sha256 OK`, `S055:Q1 OK occurrences=1 anchor=2135-ok`, `S055:Q2 OK occurrences=1 anchor=2844-ok`, `S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok`, `S055:Q4 OK occurrences=1 anchor=1767-ok`, exit 0. The manifest's `path` field is `S055.txt`, so manifest and capture live in one directory; a manifest left beside a capture named anything else reports `S055:source UNAVAILABLE reason=missing` exit 2 (observed against the wave-1 filenames before landing).
- **Harness reading, and its live-lane caveat.** `frontier-recheck-count.py` prints `entries=24 pass=24 exit=0` with `PASS F21 knowledge/csaf-vex-product-status-and-justifications.md ids=S055 exit=0` (23 → 24 measured on the same tree at base). With the F21 files in a mirror, each cut limb reds exactly one row: no entry → `problems=missing-entry`; no manifest → `manifest-unreadable`; no capture → `recheck-exit-2`; a swapped `--source S054` selection or a self-consistent S054 binding → rejected; citing S054 in prose while the binding stays S055 → still `PASS` (`wave1/ExecC2Harness.md` §§4–5). Every committed frontier row's `recheck:` line carries a lane-root `cd`, so the counter re-executes against the lane and an export-only reading cannot rederive `24/24`.

### Rejected

- **`c2-controls/junk-f21.md` — the negative twin (fabricated CSAF claims).** 23 lines, 983 bytes, sha256 `6742705ec69537cfd949b1a7df506fe8446267c712aaec8b7e714d6cbdaa1630`, four invented sentences: a mandatory CVSS v4.0 score, a justification-free `known_not_affected`, CSAF maintained by FIRST, and mandated SSVC decision points. Measured by this seat against the pinned capture with the lane's own instrument: a manifest naming `S055.txt` (sha256 `63c8ad52…`) and carrying the four claims prints `S055:sha256 OK` then one `S055:J1` through `S055:J4` `MISMATCH reason=quote-not-found`, one per claim, exit 1; the round's own artifact `c2-controls/junk-f21-recheck.txt` records the same four lines from the same instrument. The rejection is content-specific, not manifest-specific: the same manifest shape carrying Q1 verbatim prints `S055:Q1 OK occurrences=1 anchor=2135-ok` exit 0, and a one-word paraphrase of Q1 (`product` → `component`) at the same anchor prints `S055:P1 MISMATCH reason=quote-not-found` exit 1 — so no anchor repair can rescue the twin.
- **The capture's own bounds, recorded so the entry cannot overreach.** `CVSS` occurs 73 times (the standard carries CVSS vectors, scoring of fixed products and invalid-CVSS tests), so the "distinct from CVSS severity" claim rests on `product_status` being a per-product affect assertion with its own disjointness test, never on CVSS being absent; `KEV` 0, `EPSS` 0, `SSVC` 0; `FIRST` 3, all in reference entries for the CVSS specifications (L435, L437) and a TLP sentence (L1305); `product_status` 79, `known_not_affected` 18. The twin's fourth claim has no anchor anywhere in the admitted bytes, where `SSVC` occurs not at all; any KEV, EPSS or SSVC definition must come from S052, S053 or S054, never from S055.

### Candidates considered and not taken this round

- **CSAF v2.1 (not an OASIS Standard yet).** `https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html` (this seat: HTTP 200, 1,231,332 bytes, 2026-10-26T18:32:50Z; normalized head `Common Security Advisory Framework Version 2.1`, `Committee Specification Draft 04`, `21 October 2026`), while `https://docs.oasis-open.org/csaf/csaf/v2.1/os/` returns HTTP 404 (41,334 bytes, same minute). A Committee Specification Draft is work in progress: CSD 04 was opened for a 15-day public review running 23 October–6 November 2026 (`wave1/ExecCsafStatus.md` §4, review metadata page), so its normative text can still change. Admission waits for an `os/` artifact; **flip condition:** when a v2.1 OASIS Standard exists, its VEX section becomes the current normative text and needs its own capture and row (a new stage binding; the S055 row keeps its 18 November 2022 stage, amended by a supersedes note rather than rewritten).
- **CSAF v2.0 Errata 01 (26 January 2024).** A separate OASIS Approved Errata whose only change is the aggregator JSON schema, with conformance requirements explicitly unchanged (quoted in the Admitted block). It is not a registry front and does not displace the OS pins. **Flip condition:** an erratum that amends the `4.5 Profile 5: VEX` or `3.2.3.5`/`3.2.3.9` prose — then the row's scope must bind the amended stage and the capture must be re-taken.
- **CISA, Minimum Requirements for Vulnerability Exploitability eXchange (VEX).** `https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex` (this seat: HTTP 200, 49,253 bytes, 2026-10-26T18:32:30Z; normalized 115 lines; publish date `April 21, 2023`; the resource is a PDF of 1,023.41 KB). Its own scope sentence reads `These elements are derived from, but may not fully conform to, existing VEX documentation and implementations`. It is format-neutral minimum-elements guidance: it does not define `product_status` lists or bind the justification labels to a schema, so it cannot ground F21's machine-readable layer, and the round opened one source. **Flip condition:** a round that needs the consumer-side question — what a downstream consumer minimally needs from a VEX document, and whether a given document clears that bar — which is a `docs`-tier front of its own, captured from the PDF rather than its landing page.

### Standing assimilation refusals — seven staged entries, no flip cleared

Reasons and flip conditions are unchanged from the round-35 table (`corpus/lessons/round-35.md:155-169`), carried by the round-37 Gate and re-measured this round: the package is byte-identical to rounds 35–37 (70 files, every mtime `2026-10-24 23:33:20`, `SOURCES.append.md` sha256 `4fe049cb…73eb`), two flip conditions were sampled and both remain unmet (`program-severity-ladders-and-reward-scales.md` is `6c05c98f…` in the lane against `35de5f8b…` staged, so no byte-identity and no supersedes row; `newsType_6` is still absent from `corpus/source-snapshots/round-32/S049.txt`, where `newsType_21` occurs once), and `grep -c sse.com.cn corpus/SOURCES.md` → 0 keeps `S047` unregistered (`wave1/ScribeAssimilation.block.md`).

| staged entry | reason it stays refused | flip condition (still unmet) |
|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | 0 located quotes, no executable recheck, `ground: F09` collides with admitted lane F09 | a located quote + executable recheck + a non-colliding frontier id |
| `claim-packaging-and-report-quality.md` | body cites S036 (BILISRC V1.7) in no lane row and no capture | an S036 row + capture |
| `cn-crowdsourced-testing-roles-and-conduct.md` | H1 count 0; S081/S082 in no row/capture | an entry shape + the two rows |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | S077/S078/S079 unregistered; `ground: F24` is not a lane F-id | three rows + a real frontier id |
| `chinese-criminal-thresholds-and-authorisation.md` | three PRC legal sources in no row/capture; staged ids collide with different lane rows | three rows + a renumber map |
| `chinese-program-severity-instrument.md` | S047 (`sse.com.cn`) unregistered; anchor `newsType_6` → 0 in `round-32/S049.txt` | the row + a locatable anchor |
| `program-severity-ladders-and-reward-scales.md` | same-name lane file differs (`6c05c98f…` vs `35de5f8b…`); S036 half unregistered | byte-identity or a supersedes row |

The package names no CSAF or VEX ground at all (`csaf`/`vex` → 0 hits over its 94 staged rows), so no staged row competes for F21; and the staged row numbered `S055` — the Cybozu vulnerability-handling policy, which is lane `S036`'s document under a second number — must not be renumbered into the id this round uses (`wave1/ScribeAssimilation.block.md`, id-collision paragraph).

### Contested scope — kake's security.txt `CSAF` mention: adjacent, reported not absorbed

- **The hit.** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` reads: "New fields are IANA-registered, optional by definition, and unknown ones must be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079)." This seat's sweep over the 20 sibling lanes (`grep -rliE '\bCSAF\b|Common Security Advisory Framework' --include=*.md`, excluding `.ufo`/`.git`) returns exactly one file — that line — and the shokuknow merge tree returns zero; the lane's own tree returned zero at base.
- **Why adjacent, not F21 ground.** The sentence names CSAF only as an extension label registered for a security.txt file, sourced to `S079` (securitytxt.org). It carries no `product_status` category, no justification label, no document structure and no CSAF specification source; kake's own registry holds no CSAF row. F21's claimed layer — a per-product affect assertion with machine-readable not-affected justifications — is absent from it, so there is no duplicate-ground conflict and no absorption owed.
- **Ruling stated, not left silent.** Reported not absorbed: kake keeps its security.txt entry, kasegi holds the CSAF ground, and the seam is a citation rather than a move — if kake's security.txt entry ever needs the extension's semantics, `S055` is the row it would cite, and that is a kake write. The widened controls found no second site: the extra hits were `vex` as an English/Old-Norse dictionary and OCR word in kotodama, `existsSyncSafe` in kumitate scripts, and a `ScoutDocsAfter33` filename inside chousa's binary tree-state index, so the zero is measured, not a pattern artefact (`wave1/ScoutF21Sibling.md`; `wave1/ScribeSourcesLog.blocks.md` search-log bullet).

### Spot-check readiness (what a non-author can re-derive from committed bytes)

1. **Capture identity.** `sha256sum corpus/source-snapshots/round-38/S055.txt` → `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`, 5,146 lines, 272,441 bytes; the manifest's `sha256`, `lines` and `snapshot_bytes` agree. Re-normalizing a fresh fetch with `corpus/instruments/capture-source.py` reproduces that digest from either client: two seats' raw bodies differ by a Cloudflare-injected script block (414,858 vs 415,225 bytes) that the instrument strips, so pin the snapshot digest and never a `Content-Length`.
2. **Quote pins.** `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055` → `sha256 OK` plus four `OK occurrences=1 anchor=N-ok` lines, exit 0 (measured at the committed paths above).
3. **Row and registry.** `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 55; `awk -F'|' '/^\| S055 \|/{print NF}'` → 13; the source cell holds exactly one `https://` token equal to the manifest `url`; the landed line hashes to the row deliverable's `901309af…f96cc`.
4. **Frontier row.** `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 21 and `awk -F'|' '/^\| F21 \|/{print NF}'` → 8; the row's three line cites resolve in `S055.txt` to L2135, L2844 and L2152; the landed row hashes to `17743c05…d0c8488f`.
5. **Harness.** `python3 corpus/instruments/frontier-recheck-count.py` → `entries=24 pass=24 exit=0` with a `PASS F21 … ids=S055 exit=0` line, run in the lane with the entry, row, capture and manifest present in the tree (it re-executes each row's `cd`-prefixed recheck line, so an export cannot substitute).
6. **Binding, audit, census.** `capture-binding-check.py` → `records=45 bound=45 unbound=0` exit 0 with a `MANIFEST round-38 records=1 url_bound=1 fetched=1` line; that instrument binds URL, provenance and file accounting only — deleting the capture leaves it at 45/45 exit 0 (`wave1/ExecC2Binding.md` M2), so capture content is `source-recheck`'s job. `recheck-audit.py --quiet` → `expected=50 missing=0 unexpected=0 exit=0`, which requires the C-locale-correct list insertion at line 16 of `corpus/instruments/knowledge-expected.txt` (between `cra-manufacturer-reporting-duties.md` and `cvss-v4-severity-and-vector.md`). `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 with only `W04 S028` and `W04 S029`.
7. **Junk red.** A manifest naming the four twin claims against `S055.txt` → four `MISMATCH reason=quote-not-found` lines, exit 1; the same shape with Q1 → `OK occurrences=1 anchor=2135-ok`, exit 0; the round's own transcript sits at `c2-controls/junk-f21-recheck.txt`.
8. **C1 receipts at the judged head.** `bash corpus/instruments/r38-closure.sh` plain → exit 2; `--export-ref J` → `closed=8/8 exit=0`; `--selftest --export-ref J` → `selftest cases=8 failures=0`; base `a173b0c2` and r37 judged head `2387dcf6` exports → `closed<8/8 exit=1`; `.ufo/waves/round-38/final-gates/all-gates.txt` differs from J by itself only (`git diff --name-only J Y`), carries `all-gates v2`, an `export-ref` that is REF or an ancestor of REF, `suite-sha256` equal to the executing bytes, eight `G1`–`G8` payload lines ending `closed=1` and eight selftest case lines; G8's `closed=14/14` needs the live HEAD at the exported ref and a clean tree (qualification 1). These are the receipt's values (the receipt and `final-gates/reds.txt` carry the runs); at the integration head this seat measured the three `Correction (round 38)` lines, the closed fence state at EOF in both front-door files, and the two declared-block digests matching their file tails.
9. **Quiescence and cleanliness.** no directory under `/fast/scratch/hyaku/kasegi-r36`, `kasegi-r37` or `kasegi-r38` except each seat's own live work, and `git -C kasegi-shokunin status --porcelain` empty at filing; the ledger's `## Round-37 dispositions` section carries 7 proposal rows under its filled heading, and `corpus/lessons/round-38.md` carries none of the suite's placeholder vocabulary.

## Assimilation: none adopted

Id-collision rerun (this seat, read-only, the guard's own 0–3-space extractor
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` applied to both sides, ids intersected with
`comm -12`): lane `corpus/SOURCES.md` at HEAD `70015359` — the same blob as base `a173b0c2` —
holds **54** rows and **54** ids, unique, `S001`–`S054`; staged
`shokuknow/merge/kasegi/SOURCES.append.md` (`sha256 4fe049cb…73eb`, 100 lines, 89,718 B, mtime
`2026-10-24 23:33:20 −03:00`) holds **94** ids, unique, `S031`–`S124`. `comm -12` → **24**
collisions: `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046
S047 S048 S049 S050 S051 S052 S053 S054`. Artifact digests: `reg-ids`
`ea4dfaaa459dcb0ba8a648a11896a166a101b39a970b667cae02fc867c385047`, `staged-ids`
`550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f`, `collisions`
`3f3799a4d918288c122c7c0c062b7d1aa4ee6acb44a412637a1540309d64c492` — byte-equal to
`wave1/ExecIdCollision.{reg-ids,staged-ids,collisions}`, re-derived independently by this seat.

Three facts keep the number honest:

- **It is head-relative.** 24 is the registry-54 reading. C2 lands `S055` after this measurement;
  adding `S055` to the lane id list and re-running `comm -12` against the unchanged staged list
  prints **25** (`S031`–`S055`), so the lesson must state the registry size it read, never the
  figure alone.
- **Id collisions are not document collisions.** Of the 34 cited ids that are also lane rows and
  carry a URL, exactly **1** names the same host as its lane row (staged `S042` =
  `https://www.ipa.go.jp/security/todokede/vuln/process.html` = lane `S042`); **33** name a
  different host (staged `S047` = `sse.com.cn` vs lane `S047` = `ipa.go.jp`; staged `S048` =
  `std.samr.gov.cn` vs lane `S048` = `microsoft.com`; staged `S053` = `meti.go.jp` vs lane
  `S053` = `first.org`). A registered number is not a registered document.
- **The incoming row is already taken twice over.** Staged `S055` is the Cybozu
  vulnerability-handling policy (`cybozu.co.jp/company/security-policy/`), which is lane `S036`'s
  document under a second number, and `S055` is the id C2 needs for CSAF. It must not be
  renumbered into `S055`.

Guard proof (`wave1/ExecIdCollision.md` §1 holds the same fixture; re-run here): on
`| S001 | x |` + `  | S002 | y |` against `| S002 | y |`, extractor A reports
`collisions=[S002] count=1`, while the column-zero-only pattern `grep -oE '^\|…'` reports
`count=0` on the same bytes. An indent sweep (`1`–`5` leading spaces on one `S099` row) matches at
1, 2 and 3 and misses at 4 and 5 — the 0–3-space tolerance is load-bearing and 4+ spaces is the
guard's blind spot. Neither real input carries an `S`-row indented four or more spaces, so the
count above is unaffected.

Quarantine slice: the read-only register
`shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (`sha256
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, 83,621 B) yields
7 kasegi rows under the frozen awk
`awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`
(lines 99, 100, 322–326) — 7 lines, 417 B, `sha256
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`, `cmp`-identical to
`.ufo/waves/round-37/assimilation/quarantine-slice`. **0 adopted.** Three rows were re-measured
live this round (UA `kasegi-shokunin/1.0`, 2026-10-26T18:32:3xZ); four are carried from round 37
on a byte-identical register and an unchanged package:

| id (staged) | register class | verdict | basis |
|---|---|---|---|
| S037 | `payload-absent` | present-and-located, quote defective (stitched) | `openstd.samr.gov.cn` 200, 24,131 B at 18:32:45Z; the contiguous register quote occurs **0** times in the tag-stripped, whitespace-collapsed page, while `标准状态：现行`, `2020-11-19`, `2021-06-01` and `网络安全漏洞分类分级指南` each occur **1** time — the quote splices separate fields |
| S054 | `payload-absent` | present-and-located, quote defective (elided) | IPA request PDF 200, 513,648 B at 18:32:36Z (`pdftotext`); live text reads `（ア）脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`, so the contiguous register quote occurs **0** times and the embedded parenthetical is dropped from it |
| S048 | unreachable | unreachable as cited | `std.samr.gov.cn/gb/search/gbDetailed?id=3B865A…` 404, 748 B, `sha256 95cd25d8…` at 18:32:35Z — byte-identical to the r36/r37 probe |
| S065, S068, S069, S070 | unreachable | present-and-located (carried, round 37) | not re-fetched this round; r37 located each quote (NPC catalogue PDF p. break; Cisco hop to `sec.cloudapps.cisco.com`; draft standard §6.3.2 p.25; drafting note 1.2 p.1) and register + package are byte-stable |

The measured slice is **0 fabrication-class, 1 unreachable (S048), 6 present-and-located** — the
register's class column is a candidate list, not a verdict. The quarantine ids are package ids:
quarantine `S054` is the IPA request PDF, not the round-37 SSVC source, and quarantine `S037` is
the GB/T 30279-2020 catalogue record while lane `S037` is the Cybozu bounty FAQ.

Standing refusals — the two flips the round-37 verifier sampled re-measured, still unmet:
`program-severity-ladders-and-reward-scales.md` is `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6`
(67 lines) in the lane against `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87`
(50 lines) staged, so there is no byte-identity and no supersedes row;
`grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → **0** (`newsType_21` → 1), so the
`chinese-program-severity-instrument.md` anchor is still absent; `grep -c sse.com.cn
corpus/SOURCES.md` → **0**, so `S047` is still unregistered. The package is byte-identical to
rounds 35–37 (70 files, every mtime `2026-10-24 23:33:20`, `SOURCES.append.md 4fe049cb…`), so all
seven reasons in `corpus/lessons/round-35.md:155-169` stand and **0 of 7 flip conditions is met**.

Assimilation set — the package's 67 `knowledge/` entries against the lane's 49, measured against
`corpus/QUALITY.md` Q1–Q10:

- **4 shared basenames, all divergent bytes** — `authorised-testing-rules-of-engagement.md`
  (`5533fc87…` vs `bf40409e…`), `japanese-domestic-disclosure-workflow.md` (`a22d2321…` vs
  `ee667c2f…`), `japanese-severity-vocabulary-and-impact-model.md` (`f584f06c…` vs `d7fdd31f…`)
  and `program-severity-ladders-and-reward-scales.md` (above): copying any of them overwrites lane
  text, so each is **rejected as an overwrite hazard**, not a flip.
- **Registration and binding:** 67 of 67 carry a `source:` line; **12** cite only ids that exist in
  the lane registry, **52** cite zero registered ids, **3** are mixed
  (`authorization-safe-harbor-and-scope-2026-10-23-amendment.md`,
  `chinese-criminal-case-law-2026-10-23.md`, `chinese-national-grading-applied-2026-10-23.md`), so
  **55 of 67** cite at least one unregistered id (Q1/Q2 red). **0 of 67** reference a lane capture
  under `corpus/source-snapshots/` (Q9 unbound), **0 of 67** carry a `cd`-prefixed executable
  `recheck:` line (Q10 red), and **11 of 67** carry no quoted sentence at all (Q3 red).
- **`ground:` collides with live lane ids:** 27 of 67 write a `ground: F##` that is also an
  admitted lane frontier id but means something else — e.g. `program-scope-rules-and-asset-boundaries.md`
  says `ground: F09 (new frontier item; extends F03…)` while lane F09 is *authorisation outside the
  platform*, and `japanese-domestic-disclosure-workflow.md` says `ground: F13 (new frontier item…)`
  while lane F13 is *program severity ladders*.
- **Admit: none.** The nearest candidate is `japanese-domestic-disclosure-workflow.md`: its `S042`
  is the lane's own IPA process page, but `S043` in that entry is `jpcert.or.jp/vh/…` while lane
  `S043` is HackerOne, its bytes differ from the same-name lane entry, it references no capture, and
  its `recheck:` is a prose sentence plus a backticked `curl` (Q10). It fails on four counts.
- **Rejects recorded, with their reasons:** `chinese-program-severity-instrument.md` (S047
  unregistered, `newsType_6` absent — the standing flip stays unmet);
  `program-severity-ladders-and-reward-scales.md` (same-name bytes unequal, S036 half
  unregistered); `chinese-crowd-testing-national-standard-2026-10-23.md` (cites S077/S078/S079,
  none of which is a lane row); staged `S055` (duplicate-by-document of lane `S036`, and the id C2
  needs).

Assimilation result: **none adopted** — no staged entry passes `PROVINCE.md`/`corpus/QUALITY.md`
admission at this head, no id-collision row is free to reuse, and no refusal flip condition is met.

## considerthese 2026-10-26 dispositions

Ledger: `corpus/knowledge/considerthese-proposals-ledger.md`. The seven are the items under
`considerthese/2026-10-26.md` § Self-improvement suggestions. Round 38 mines proposal 3 and leaves 1, 2,
4, 5, 6 as the ledger records them. The ledger's round-37 section
(`## Round-37 dispositions (appended 2026-10-26, R31 home)`, L37) landed as an empty heading at the
claims-freeze head `9a10b02f` — the L1-found defect D-F — and this round fills it under G7 with one row
per proposal, so each old → new below is the lesson half of an R31 disposition and that section the
durable half. The tracked path is also where the round-37 two-path conflict resolves: the freeze names
`corpus/knowledge/considerthese-proposals-ledger.md`, and `corpus/considerthese-ledger.md` is in no tree
(`git cat-file -e 9a10b02f:corpus/considerthese-ledger.md` → fatal, absent).

1. **Distance-to-next-score thresholds** — `open`, unchanged (the round-37 dispositions row for proposal
   1). Round 37 recorded the gap line (`gap: 24 of 47 rechecks still gated on a lost base; score 5 needs
   0 gated unsupported claims`); the static read this round is
   `grep -c 'Threshold for 8' SCORECARD.md` → `0` at `9a10b02f`, so §Saturation (`SCORECARD.md:309`)
   still declares the 9/10 line and no promotion threshold for either axis.
2. **End-to-end domain task round** — `open`, unchanged (row 2). `SHONEN.md:173-174` keeps box 2 at
   `[~]` with "no new end-to-end domain hunt ran"; this round again spends its work on a closure suite
   and one coverage admit, not on a priced claim package.
3. **Quiescence gate before `complete`** — `mined` round 36 → `mined` round 38, same class, wider check
   (row 3). What the proposal points at, opened this round: round 35 is `rejected-honest-stop` with both
   frozen kill rules firing at the judged revision and the missing bytes landed after `complete kasegi
   round=35` (04:00:34) and after filing — `8ce6fb4` 04:01:12, `5a25337` 04:02:21, `bb2dc8c` 04:04:46,
   `48e6053` 04:04:55 (`corpus/lessons/round-35-verifier-spotcheck.md:10-20`), which that spot-check
   names M35-1, wave writes after `complete`. Round 36 routes the same order again: `complete` 13:02:47,
   lane commit `c20300df` 13:41:37, erratum `1c43fd8f` 13:41:38
   (`corpus/lessons/round-36-verifier-spotcheck.md` §5 D3). Round 37 again: `complete` 15:02:47, lane
   commit `83975acc` 15:03:15 (`corpus/lessons/round-37-verifier-spotcheck.md` §5 D3), and §5 D-E finds
   `/fast/scratch/hyaku/kasegi-r37/build-spec.py` still present.

   Round 36 had landed the criterion (QUALITY R28) and a suite limb (`r36-closure.sh:93-108`, E9); round
   37 rewrote E9 fail-closed, added E14 to shape-check that the fail-closed status read stays in the
   committed bytes, and added E10 to bind the committed positive run. Both routed defects recurred
   anyway. Two faces were unchecked. E9 counted leftover *seat directories* — the read is
   `find "$sroot" -mindepth 1 -maxdepth 1 -type d` (`r36-closure.sh:475`) — so a leftover file reads
   quiescent. And nothing read the order, so a lane that is quiescent when the suite runs can commit
   afterwards.

   Round 38 puts both faces in the closure suite. G4: every `.ufo/waves/round-38/*-dispatch.json` in the
   export has a tracked sibling `*-results.json` that parses as JSON and lists exactly as many seats as
   the dispatch's `taskCall.tasks`, so the wave results are in the judged head before the report (D3,
   M38-4). G6: live scratch quiescence with the any-entry rule — `kasegi-r36` and `kasegi-r37` hold
   zero entries or are absent, and `kasegi-r38` holds nothing but the suite's own `--work` dir (D-E,
   M38-6). QUALITY **R33** (round-38 append-only block) records the criterion: the judged head carries
   every round artifact including the wave results, lane files name the judged head by reference to the
   gate receipt rather than by a hash they cannot contain, and the report is filed after the last lane
   commit. The status stays `mined`: a check binds the next round's evidence, not the intent of the lane
   that writes it.
4. **Cap or externalise wave evidence** — `open` (operator-owned), unchanged (row 4). Measured at
   `9a10b02f`: 7,352 tracked files, 7,069 of them under `.ufo/` (96.2 %); 121,114,796 tracked blob
   bytes, 115,132,709 under `.ufo/` (95.1 %); `.gitattributes` carries no LFS rule
   (`grep -c filter=lfs` → `0`). The round adds wave evidence; nothing in it externalises or prunes.
5. **Land the owed F18 `PROVINCE.md` amendment** — `mined`, unchanged (row 5): `PROVINCE.md:77`
   carries the F18 amendment appended in round 36 for the round-35 admission.
6. **Re-tune cadence and depth** — `open`, unchanged (row 6): no change is recorded for it in this
   lesson or in the ledger section the round fills.
7. **Proposal-status ledger** — `mined` at round 37 (QUALITY R31 plus the ledger itself), row 7. What
   round 37 left incomplete is the row set — the empty heading above — and G7 is its fill, not a new
   proposal.

## Census

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
— before (base, `.ufo/waves/round-38/census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0; after (integrated
tree with the S055 row): `W04 S028`, `W04 S029`, `ok`, exit 0. Registry 54 → 55 rows; tier A +1; rows touched
old→new: none (S055 is a new row; the `## Registry changes` bullet logs it).

## Mistakes

Six rows, minted this round from the six defects routed by the round-37 verifier spot-check — D-A, D-B,
D-C, D3 and D-E from `corpus/lessons/round-37-verifier-spotcheck.md` §5, plus the L1-found D-F. Every
evidence cell was measured read-only against the revision it names, with the commands and their outputs
in `.ufo/waves/round-38/wave1/ScribeMistakes.md` §2; the G-checks in the fix column are this round's
closure limbs, and this seat ran none of them. Placeholder tokens are named in prose rather than
reproduced, so this lesson cannot satisfy the vocabulary its own G3 hunts.

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M38-1 | landing / deliverable-bleed | The round-37 scribe receipt's scaffolding was landed as the front-door append. `PROVINCE.md` grew 78 → 152 lines where the declared block is 2 lines / 295 B, and `corpus/README.md` grew 398 → 454 lines where the declared block is 27 lines / 2947 B. The landed text carries the receipt's own section headings (`PROVINCE.md:90` `## 3. Deliverable B — corpus/README.md end-of-file block`, `:134` `## 4. Validation on a scratch mirror`), its property tables, and a duplicated F20 frontier row; the README append opens a fence at `:426` that never closes and never states its `## Round-37 admission` heading. Where the pasted table asserts its own green, the landed bytes contradict it: `corpus/README.md:448` records the section-header check as `1`, and the same bytes read `0`. | at `2387dcf6` and at base `a173b0c2`: `wc -l` `PROVINCE.md` 152 (base 78), `corpus/README.md` 454 (base 398); receipt-section headings in `PROVINCE.md` 2; fence lines `PROVINCE.md` `:81`, `:96`, `:124` (3, EOF state open) and `corpus/README.md` `:426` (1, open); anchored heading read 0 against the pasted 1 at `:448`; declared blocks recorded at `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md:56` (295 B, 2 lines) and `:99` (2947 B, 27 lines) | none — the r37 placeholder limb reads `SCORECARD.md` only, against two fixed spellings (`corpus/instruments/r37-closure.sh:59-64`), and no check compared an append with the block declared before landing | G1 (D-A): one appended `Correction (round 38)` line per front-door file, appended-block equality against the declared blocks, and fenced-code state closed at EOF; QUALITY R32 | base export `a173b0c2` is red on G1 (2 receipt sections, 3 fences odd in `PROVINCE.md`, 0 correction lines); J green; a declared-vs-landed line-count or digest mismatch stays red |
| M38-2 | stale-premise / label-drift | Three round-37 artifacts name three different heads as final, and only the one with the committed run is an ancestor of the other two. The gate receipt pins `export-ref=9492c776…` (`.ufo/waves/round-37/final-gates/all-gates.txt:2`); `SCORECARD.md:1505` and `SHONEN.md:172,176` name `aa88877b…` as the final lane head; the filed report's C1 section names `2387dcf6…`. No transcript of a run over `aa88877b` or `2387dcf6` is committed, so the two heads the round files call final are the two nothing measured. | `git merge-base --is-ancestor` `9492c776` → `aa88877b` → `2387dcf6` all exit 0; commit stamps 14:59:49, 15:00:25, 15:01:28 −03:00; `git diff --name-only 9492c776 2387dcf6` → `all-gates.txt`, `SCORECARD.md`, `SHONEN.md` only, i.e. exactly the files whose values the later heads change | R19 for figures only (it binds a literal to the command that prints it, not a label to one head); r37 E1 checks that a named hash resolves and is an ancestor inside the SCORECARD round-37 block, never that one head is named everywhere | G2 (D-B): the gate receipt binds the suite digest and grades the judged head through its `export-ref`; `SCORECARD.md` and `SHONEN.md` name that head by reference to the receipt, never by a hash; the diff from the judged head to the graded ref is the receipt file alone; QUALITY R33 | the r37 bytes are red under G2 (three heads, and the graded head is an ancestor of both heads named final); a lane hash written on the judged head's own line is red, since a commit cannot contain its own hash |
| M38-3 | evidence-record / placeholder-bleed | The round-37 lesson shipped unresolved pending-markers: 7 of them, at lines 10, 90, 95, 216, 265, 300 and 320 — the final-commit line, the entry-state line, the harness transcript, the gate-review pointer, the considerthese block, the census after-state and the No-harm measurement. `corpus/lessons/round-37.md:85` still says the SSVC entry is **not landed** while that entry is committed in the same head, so one marker also carried a stale sentence past the placeholder sweep. | at `2387dcf6`: `grep -c` pending-markers on `corpus/lessons/round-37.md` → 7 at the lines above; `sed -n '83,87p'` shows the not-landed sentence; the placeholder limb's documented scope at `corpus/instruments/r37-closure.sh:59-64` is two spellings in `SCORECARD.md`, so `SHONEN.md` and the lesson were never read; the same head's `SCORECARD.md:1505` and `SHONEN.md:172` carry template head tokens the two-spelling vocabulary does not name | E1 placeholder limb — too narrow by both file set and vocabulary; G3 widens both this round | G3 (D-C): a pending-marker resolutions section in this lesson, and zero widened placeholder tokens in the lines added from base to the judged head | the round-37 lesson is red on G3 at its own head (7 markers) and one widened token in an added line keeps a round red |
| M38-4 | landing / closure-order | The round-37 lane committed wave results after the round had completed, for the third round running (r36 M36-1, r37 D3, this row). `83975acc` (2026-10-26T15:03:15−03:00, `.ufo/waves/round-37/kasegi-r37-build-results.json`, 392 insertions in 1 file) landed 28 s after the dispatcher's `complete kasegi round=37` at 15:02:47, so the judged head carried the dispatch but not its results file. | `git log -1 --format=%cI 83975acc` → 2026-10-26T15:03:15−03:00; `git show --stat 83975acc` → 1 file changed, 392 insertions; `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1537` → complete at 2026-10-26T15:02:47−03:00; `git cat-file -e 2387dcf6:.ufo/waves/round-37/kasegi-r37-build-results.json` → exit 128, and the same read at `83975acc` → exit 0 | none — R4 binds a work commit to a round and M36-1's fix read only the pre-report direction; no committed check reads dispatch-to-results pairing or the position of the results commit | G4 (D3): every round-38 dispatch file has a tracked results file with an equal seat count, and the report is filed after the wave result lands, so no lane commit follows `complete`; QUALITY R33 | the r37 judged head is red on G4 (dispatch tracked, results file absent there and present only at `83975acc`); a dispatch whose results file never lands stays red |
| M38-5 | evidence-record / empty-section | The proposal ledger's round-37 section shipped as a bare heading: `corpus/knowledge/considerthese-proposals-ledger.md:37` is the section header, the next heading follows at `:41`, and no table row sits between them — 0 rows for the round, against the report's statement that the round landed an 18-row disposition table. | at `a173b0c2` and `2387dcf6`: `grep -n '^## Round-37 dispositions'` → `:37`; row count after that heading → 0; section spans 7 lines; the claim is at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:25` | none — R31 requires a disposition per touched proposal, but no check reads a row count, so an empty section reads exactly like a filled one | G7 (D-F): the round-38 ledger section carries 7 proposal rows | `a173b0c2` is red on G7 (heading present, rows 0); a section carrying fewer rows than the proposals the round touched stays red |
| M38-6 | scratch-discipline | The round-37 round left a scratch entry behind and reported scratch empty: `/fast/scratch/hyaku/kasegi-r37/build-spec.py` was still present when the closure run ran. The quiescence limb counted only first-level directories at the lane's scratch prefix, so a file sitting at that prefix passed the sweep it should have failed. | `corpus/instruments/r37-closure.sh` quiescence limb counts `find "$sroot" -mindepth 1 -maxdepth 1 -type d`, so a file at the prefix is outside the read; `corpus/lessons/round-37-verifier-spotcheck.md` §5 D-E records the surviving path; the path is absent today (`ls /fast/scratch/hyaku/kasegi-r37` → No such file or directory, measured this round), so the red is the r37 observation, not a current one | E9 seat-dir limb only — the `-type d` filter drops files, and R28's wording ("no leftover scratch seat dirs") matches the limb's shape, so nothing caught a surviving file | G6 (D-E): quiescence for `kasegi-r36`, `kasegi-r37` and `kasegi-r38` reads any entry at the lane prefix, file or directory | a single file at the lane prefix keeps G6 red — r37's `build-spec.py` would have — and an empty prefix is green |
| M38-7 | scope / misroot | Wave seat ExecNoHarm's fixture driver wrote relative paths before `cd` while its cwd was the fleet root (2026-10-26T15:29:11−03:00): it truncated the fleet-root `LOG.md`/`SCORECARD.md` and created `PROVINCE.md`, `SHONEN.md`, `SKILL.md` and `corpus/*` there. The seat restored the fleet files from fleet HEAD blobs; the orchestrator verified the fleet ledgers byte-equal to HEAD (no loss). | orchestrator notice to the L1 (round 38, in-session); `git -C /home/vgpnk/Projects/shokunin status --porcelain` at the L1 misroot sweep shows no kasegi file | none — the wave context forbade fleet writes and required absolute paths, but nothing enforced it inside a seat's own fixture driver | wave contexts from round 39 require every fixture driver to `cd "$S"` (its scratch) before any relative write and to assert `pwd` is under `$S`; `ExecNoHarm.sh` itself (`--repo`) is not re-run from the fleet root | a driver that writes before `cd` reproduces the misroot in a scratch fixture whose cwd is a throwaway git repo |

## Instrument attack findings — routed to round 39 (not fixed after scoring)

The wave attacked the landed suite (`85d33ea9…`) after seats had scored it, so the suite was not rewritten
this round (a rule changed after scoring is not the claim's rule). Findings, each with its receipt:

- G1: a declaration may cover only part of the appended tail; a `Correction (round 38)` line inside a fence
  still counts; `~~~` fences are not modelled; a declaration path is not confined to the export
  (`wave1/CritC1Kill.md` K2, `wave1/RevSuiteDesign.md` G1-H1..H4). On the landed bytes none of these is used:
  declared lines equal the appended lines (README 486−454 = 32, PROVINCE 156−152 = 4), both corrections sit
  outside fences (fence walk `closed` before and after them), and both declared paths are lane-relative.
- G2: the selftest case lines are counted, not graded `positive=pass … verdict=pass` (`wave1/RevSuiteDesign.md`
  G2-H2; `wave1/CritC1Kill.md` K3); the landed receipt's case lines are all `positive=pass` / `verdict=pass`.
- G4: counts, not seat identities; a zero-task dispatch is vacuously green (`RevSuiteDesign.md` G4-H1/H2).
- Selftest coverage, measured by source mutation of the landed suite: G1/G2 — 19 surviving one-limb mutants (e.g. deleting the fence-state conjuncts or the lane-relative path guard leaves `--selftest` at `failures=0`; `wave1/MutG1G2.md`); G3/G4 — G3-M3 (vocabulary gutted to one token) and G3-M4 (fail-closed diff read defaulted) survive (`wave1/MutG3G4.md`); G5–G8 — four survivors (`wave1/MutG5G8.md` F-G5, F-G6, F-G7, F-G8). The suite's own mutants are all rejected (the frozen selftest predicate), but its fixtures do not pin every conjunct: the verdicts at the judged head stand on the payload values in the receipt, which a reader re-derives with plain greps.
- G8 runs the export's own `r37-closure.sh`, whose bytes the judged head controls (`wave1/CritC1Export.md`).
- C2 census: a tier A→C downgrade survives with `W01` and exit 0 (`wave1/MutC2Row.md` F1) — a census property,
  not a lane instrument; recorded, not changed (fleet `/home/vgpnk/Projects/shokunin/scripts/` is out of write scope).

Planned for round 39: an r39 suite carrying these as fixtures and tightened limbs (SCORECARD `## Planned`).

Correction (round 39): two C1 lines above overstate the result at the judged head. The frozen C1 row (`:21`, "`closed=8/8 exit=0` and `selftest cases=8 failures=0` over the judged head are the receipt") and Gate readiness item 8 (`:94`, "`--export-ref J` → `closed=8/8 exit=0`; `--selftest --export-ref J` → `selftest cases=8 failures=0`") both contradict the committed receipt `.ufo/waves/round-38/final-gates/all-gates.txt`: its `export-ref` (`:2`) is the judged head J = `66703acaaff50529a35be49aa8759d04140720ad`; its run over J prints `export-ref-run: G2 payload=receipt=0,… closed=0` (`:8`) and `export-ref-run: closed=7/8 exit=1` (`:15`); and the `closed=8/8 exit=0` run (`:26`) with the `selftest cases=8 failures=0` tally (`:73`) is over `run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e` (`:4`, `:17`, `:29`), the bootstrap commit that is J plus a receipt, not J itself. Read both lines as: the suite closes all eight checks over the receipt's `run-ref`, and the run over J is 7/8, red on G2 alone, because G2 requires the receipt inside the export while the judged-head rule makes J the receipt's own `export-ref` — a commit cannot contain the receipt that names it (receipt header `:5`). The two lines are retained as history; this line is the correction (non-author verifier `corpus/lessons/round-38-verifier-spotcheck.md` §5 R2).
