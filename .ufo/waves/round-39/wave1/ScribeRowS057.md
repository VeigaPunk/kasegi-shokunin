# ScribeRowS057 — SOURCES registry row for S057 (CISA, When to Issue VEX Information)

Seat: `ScribeRowS057` (scribe, axes: coverage). Round 39, kasegi-shokunin lane, base `480b1a505a2dfc14a4f718d16d63808247214d0a`. Report path: `.ufo/waves/round-39/wave1/ScribeRowS057.md`. Writes made: the row deliverable `wave1/ScribeRowS057.row.md` and this receipt, plus scratch under `/fast/scratch/hyaku/kasegi-r39/ScribeRowS057/` (removed before yielding). No lane file, fleet file, sibling repo, tooling install, or git mutation.

## 0. What this seat delivered

| artifact | bytes | lines | sha256 | shape |
|---|---|---|---|---|
| `wave1/ScribeRowS057.row.md` | 948 | 1 | `176762ea6a22ecffcd28e926ae026044bbbf59c40c530cf53a00c741e5d3c8d9` | `awk -F'|'` → `NF=13` (11 cells), 12 `|` characters, trailing bytes `20 7c 0a` (`\|` + LF) |

Measured on the delivered file:

```
$ awk -F'|' 'NR==1{print "NF="NF; print "pipes="gsub(/\|/,"|")}' ScribeRowS057.row.md
NF=13
pipes=12
$ awk -F'|' '{for(i=2;i<NF;i++){gsub(/^ +| +$/,"",$i); printf "c%d=%d ", i-1, length($i)}; print ""}'
c1=4 c2=111 c3=4 c4=1 c5=143 c6=296 c7=289 c8=5 c9=10 c10=4 c11=42
$ awk -F'|' '{n=gsub(/https:\/\//,"&",$3); print "source_https_tokens="n}' ScribeRowS057.row.md
source_https_tokens=1
```

Cells 1-5 and 7-11 are byte-identical to the cells the L1 specified (checked per cell against the dispatch text: `1 SAME 2 SAME 3 SAME 4 SAME 5 SAME 6 DIFF 7 SAME 8 SAME 9 SAME 10 SAME 11 SAME`). Cell 6 (anchor) is the one deliberate change, documented in §3.

## 1. Source opened, and what the row binds to

- **Registry URL (the row's only `https://` token):** `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`. This seat's own fetch, `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, **2026-10-26T19:30:38Z**: HTTP **200**, 54,453 bytes, sha256 `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d`. The same digest is in the round-38 scout fetch ledger and in this round's `wave1/ExecFrontierCapture.manifest.json` (`landing_page.raw_sha256`).
- **The committed capture is the 508c PDF the page links, not the page.** `https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf`, fetched **2026-10-26T19:30:47Z**: HTTP **200**, `application/pdf`, 235,270 bytes, sha256 `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` (identical to the round-38 ledger), served `last-modified: Mon, 06 Nov 2023 15:43:40 GMT`. Normalized with the lane's own `corpus/instruments/capture-source.py` `pdf_to_text` (`pdftotext -enc UTF-8` then `collapse()`): **17,971 bytes, 275 lines, sha256 `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`**.
- **Independent reproduction.** Ran the same instrument path from this seat's own PDF bytes into `S057.independent.txt` and compared with the seat-owner deliverable `wave1/ExecFrontierCapture.S057.txt`: `cmp … && echo "cmp: byte-identical exit 0"` → `cmp: byte-identical exit 0`, 275 lines. Two seats, two fetches, one digest.
- **Access date:** **2026-10-26**. Publication: the landing page carries `November 06, 2023` (HTML match) and the capture's own line 3 reads `Publication date: November 2023`; the served PDF `last-modified` is 2023-11-06.

## 2. Gate — F22 / S057 (CISA, When to Issue VEX Information)

URL: `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information` (HTTP 200, 54,453 bytes, sha256 `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d`). Access date **2026-10-26**. All line numbers below are 1-based lines of the committed capture `S057.txt` (275 lines, sha256 `11c8d6d6…5d64f2f`), read by this seat in those bytes; `occurrences=1` for every quote under `source-recheck.py`'s `normalize()`.

- **Q1 — 25 words, `S057.txt:12-14`** (`Whether,` closes L12; opening of the Introduction's scoping paragraph): `Whether, and when, to issue VEX information is a business decision for most suppliers and possibly a more individual decision for independent open source developers.`
- **Q2 — 20 words, `S057.txt:79-81`** (under the heading `When VEX information could be issued`, L78): `The decisions and timing around providing VEX information are primarily business decisions and are not determined by a strict protocol.` — the sentence that makes the document guidance rather than a conformance standard, and the one the round's negative twin `c2-controls/junk-f22.md` claim 1 contradicts.
- **Q3 — 13 words, `S057.txt:132-133`** (body of `Status changes`, heading L131): `Ideally, when a new vulnerability is disclosed, an “under_investigation” status should be issued.`
  - Companion, same region, 19 words, `S057.txt:133-135`: `When the investigation has concluded, status should be updated, for example, noting that the product is “affected” or “not_affected.”`
  - Companion, 22-word exact sub-span (`S057.txt:137-138`; the full sentence is 26 words and ends `…at the present time.`): `By updating a timestamp but not changing status or other information, a VEX issuer can reaffirm that the current status remains accurate`
- **Q4 — 20 words, `S057.txt:184-185`** (`Status inheritance` under `Software supply chain considerations`, L179-181): `Strictly speaking, consumers should not assume the status of an upstream component applies to a product that uses the component.`
  - Companion, the exception, 14 words, `S057.txt:188-190`: `a VEX status of “not_affected” with justification “component_not_present” or “vulnerable_code_not_present” could be inherited downstream`

Q1-Q4 satisfy the ≤25-word bar (25/20/13/20); the two companions exist because the row's anchor claims three regions and the lifecyle/reaffirmation pair cannot be a single ≤25-word quote (13 + 19 words as separate sentences) and the full reaffirmation sentence runs 26 words.

- **Kind `docs`, tier `A` — measured, not asserted.** Case-sensitive normative keywords in the whole capture: `MUST` 0, `SHALL` 0, `SHOULD` 0, `MAY` 0, `REQUIRED` 0; case-insensitive lowercase `must` 0, `shall` 0, `should` 15, `may` 14 — advisory prose throughout, with no conformance test, schema or requirement list, and the document's own statement (Q2) that the decisions are not determined by a strict protocol. That is `docs`, not `spec`. Tier `A`: cisa.gov serves CISA's own guidance about its own VEX programme; no secondary host, summary or vendor restatement intervenes.
- **The layer is genuinely beyond S055, measured in S055's own bytes.** Against `corpus/source-snapshots/round-38/S055.txt` (5,146 lines): `business decision` 0, `reaffirm` 0, `issuance` 0, `when to issue` 0; `inherit` 6, and all six are CSAF role-permission sentences (`Author: inherits Registered permissions…` L4322 through `Administrator: inherits Manager permissions…` L4327), not vulnerability-status inheritance; `under_investigation` 12, all status-value uses. So the row's `teaches` cell ("the issuance-trigger, lifecycle, reaffirmation and inheritance layer the CSAF VEX profile (S055) does not carry") is grounded in a zero, not in an impression.
- **Recheck against the committed manifest and capture** (scratch mirror: lane `SOURCES.md` copy + my row appended, `ExecFrontierCapture.S057.txt` → `corpus/source-snapshots/round-39/S057.txt`, `ExecFrontierCapture.manifest.json` → `corpus/source-snapshots/round-39/manifest.json`):

```
$ python3 corpus/instruments/source-recheck.py --manifest mirror/corpus/source-snapshots/round-39/manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
exit=0
```

  The manifest's four quotes are 25/22/42/34 words; the Gate block above is the ≤25-word reading of the same passages, and its line numbers agree with the manifest anchors (12, 132, 136, 184).
- **Binding (rule B), with the row present.** `capture-binding-check.py --root mirror` → `MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0`, `AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0`, `records=1 bound=1 unbound=0`, **exit 0**. Rule B5 requires the record's `url` to byte-equal the row's token; the manifest satisfies it with `url` = the page URL and a separate `capture_url` = the PDF, which is the only split that keeps the registry URL meaningful while the committed bytes are the PDF's text. `multi_row_url=0`: the page URL occurs in no other row, so landing the row adds no `W04` duplicate-URL warning (census before-state stays `S028`/`S029`).

## 3. Finding — the dispatched anchor cell's line numbers do not address the committed capture

The dispatched cell 6 read:

```
capture corpus/source-snapshots/round-39/S057.txt: business-decision sentences (PDF L19-20, L129), under_investigation lifecycle + timestamp reaffirmation (L205-213), inheritance caution (L287-294); publication page November 6, 2023
```

Those numbers are real, but they are lines of a **different extraction of the same PDF**, not of the file the cell names. Measured three ways from the same 235,270-byte PDF:

| basis | non-empty lines | Q1 | Q2 | Q3 | Q3-companion | reaffirmation | Q4 | Q4-exception |
|---|---|---|---|---|---|---|---|---|
| `pdftotext -layout`, raw (blank lines kept) | 401 | L19 | L129 | L206 | L206-208 | L212 | L287 | L293 |
| `pdftotext -layout` + `collapse()` | 278 | L18-20 | L128-130 | L205-206 | L206-208 | L211-212 | L287-288 | L292-294 |
| **`capture-source.py pdf_to_text` (the committed capture)** | **275** | **L12-14** | **L79-81** | **L132-133** | **L133-135** | **L137-138** | **L184-185** | **L188-190** |

`L287-294` is past the end of a 275-line file, so the dispatched cell would have sent a reader to nothing in the committed capture. The cause is traceable: the round-38 scout that first opened this PDF recorded it as "400 text lines" (`wave1/ScoutVexLeads.md:41`) and pinned quotes as `L19-20`, `L129`, `L205-212`, `L287-294`, and those layout numbers were carried into the round-39 dispatch. The seat that owns the capture (`ExecFrontierCapture`) reached the same conclusion independently and messaged this seat mid-work: *"the planned numbers (L19-L20, L129, L205-L213, L287-L294) are `pdftotext -layout` line numbers; the committed capture is default-mode + collapsed (275 lines), so L287+ is out of range there … Do not cite layout numbers alone."*

**Move taken:** cell 6 keeps every dispatched locator group and adds the committed-capture numbers ahead of them, so the cell addresses the named file and the layout numbering remains verifiable from the PDF:

```
capture corpus/source-snapshots/round-39/S057.txt: business-decision sentences (L12-14, L79-81; pdftotext -layout L19-20, L129), under_investigation lifecycle + timestamp reaffirmation (L132-138; layout L205-213), inheritance caution (L184-191; layout L287-294); publication page November 6, 2023
```

This is the only cell this seat changed (spec 232 chars → landed 296 chars). It harms no axis: `NF=13`, one `https://` token, no `|` inside the cell, no claim remade. If the L1 prefers the literal dispatch text, reverting is a one-cell paste of the block quoted above; it will then cite lines that do not exist in the committed capture, and the round's own Gate reading (this receipt) is the only place that says so.

## 4. Finding — the frozen C2 counting command is off by one against its own rows

`claims.json` C2 `counting_commands` pins `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58`, and the `after` cell says `registry 58 (S057 mined + S056/S058/S059 rejected)`. Measured: `corpus/SOURCES.md` holds **55** rows at base (the frozen `c2-controls/before.txt` agrees), the highest id is `S055`, `S056` and `S057` are both `0`; four rows landing (`S056`, `S057`, `S058`, `S059`) give **59**, and the scratch mirror with only this seat's row gives 56. 55 + 4 = 59 ≠ 58.

The kill rule does not test the registry count ("S057 row absent or NF != 13; S056/S058/S059 rows absent as rejected rows; …"), so this is a counting-command/reporting delta, not a sourcing defect — but a verifier who runs the pinned command at the judged head will read 59 and call it a miss unless the receipt says why. Recorded verbatim rather than smoothed; the fix belongs to whichever seat owns the C2 report numbers.

## 5. Touched surfaces and blast radius

- Written: `wave1/ScribeRowS057.row.md` (deliverable), `wave1/ScribeRowS057.md` (this receipt), `/fast/scratch/hyaku/kasegi-r39/ScribeRowS057/` (removed).
- Read only: lane `corpus/SOURCES.md`, `corpus/source-snapshots/round-38/S055.txt`, `corpus/instruments/{capture-source,source-recheck,capture-binding-check}.py`, `.ufo/waves/round-39/{claims.json,c2-controls/*,census-before.txt,wave1/*}`, `.ufo/waves/round-38/wave1/{ScoutVexLeads.md,ScribeRowS055.row.md}`. Fetched (network): the CISA page and its 508c PDF, both recorded above.
- Not touched: `corpus/knowledge/` (entry is another seat's), `corpus/README.md` (frontier row), `corpus/instruments/*` (no edit, no new instrument), the harness/binding/audit/census after-values, `recheck-audit` expected list, `.ufo/state/`, any fleet-root or shokuknow file, any sibling lane.
- Out of scope by construction: rejected rows `S056`/`S058`/`S059` (owned by the rejection scribe), the knowledge entry `corpus/knowledge/cisa-when-to-issue-vex.md`, the F22 frontier row, `c2-controls/junk-f22.md` handling (the junk recheck seat owns the transcript), and every C1 (depth:verifiability) artifact.

## 6. Limits of what this receipt claims

- No claim that `SOURCES.md` now holds the row: it does not; the L1 lands it. All row measurements above are of the deliverable file, and the binding/recheck runs were against a scratch mirror of the lane's registry copy plus this row, not the live tree.
- No claim about the entry's QUALITY answers, the harness count, the audit expectation, or the census exit — those move only when other seats land their files, and this seat did not run them against the live lane.
- The row's `status: mined` asserts a capture exists and is bound; at filing the capture lives at `wave1/ExecFrontierCapture.S057.txt` with its manifest, and the row's `capture` cell names the path the L1 must copy it to (`corpus/source-snapshots/round-39/S057.txt`). If the L1 lands the row without that copy, `recheck-audit` and `source-recheck` go red on a missing capture — that is a landing order, not a sourcing question.
- Tooling: nothing installed or upgraded this seat; no `pacman` invocation. Scratch: `/fast/scratch/hyaku/kasegi-r39/ScribeRowS057/` created with `mkdir -p`, used for both fetches, the mirror tree and the reproduction, and removed with `rm -rf` before this report was filed.
