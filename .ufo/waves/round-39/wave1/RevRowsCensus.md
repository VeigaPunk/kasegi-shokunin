# RevRowsCensus — round-39 receipt

Seat: `RevRowsCensus` (reviewer, leaf, no subagent dispatch). Round: kasegi-shokunin 39, judged on depth:verifiability. Item: validate the four row deliverables (`ScribeRowS057` row + `ScribeRowsRejected` x3) against the census schema, run `sources-census.sh validate --file` on a scratch mirror containing the rows, verdict + findings. Read-only against the lane except this receipt. Lane read at `d65d823` (wave1 spec/dispatch; rows unlanded — validated as deliverable bytes). Tools installed or upgraded: none. Scratch `/fast/scratch/hyaku/kasegi-r39/RevRowsCensus/` removed before yield. Disk guard green at start (25% /fast/scratch, 609.8G free). All times UTC 2026-10-26.

## 0. Verdict

**PASS.** All four row deliverables conform to the census schema (`SOURCES-CONTRACT-v1`, 11 cells, NF=13) and validate clean in a scratch mirror: `sources-census.sh validate --file` over the mirror prints exit 0 with exactly the two pre-existing warnings (`W04 S028`, `W04 S029`) and no new E/W code. Two findings recorded (F1 frozen-count arithmetic — cross-claim, not row-defect; F2 the S057 anchor's justified deviation from the dispatched text), neither blocks the rows.

## 1. Deliverables validated (sha256 measured on the landed bytes)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `wave1/ScribeRowS057.row.md` | 1 | 948 | `176762ea6a22ecffcd28e926ae026044bbbf59c40c530cf53a00c741e5d3c8d9` |
| `wave1/ScribeRowsRejected.S056.row.md` | 1 | 1281 | `e3b789f2f7c249c82a71b498ef498cdf8afa43407a3eae59895ad0da86a69ceb` |
| `wave1/ScribeRowsRejected.S058.row.md` | 1 | 1202 | `57f1ab24f58bc512301226d7fe8e8e48ca4bd759474db249c90d6909ea3f87bb` |
| `wave1/ScribeRowsRejected.S059.row.md` | 1 | 1044 | `faf60f0194690c91a6db77d8c6523e4f71034e886426619059ff3b0b80d5cb47` |

Note: `ScribeRowS057.row.md` was revised mid-wave (1023 B @16:34 → 948 B @16:35, anchor tightened); every check below is on the final 948-byte bytes.

## 2. Per-row schema checks (my checker, `check_rows.py`, over the delivered bytes)

```
S057  PASS one-line lines=1 | NF=13 | id=S057 | no-pipe-in-cells | no-escaped-pipe
      kind=docs | tier=A | status=mined | opened=2026-10-26 | recheck=180d
      one-https-token tokens=1 | url==manifest | usedby=corpus/knowledge/cisa-when-to-issue-vex.md
S056  PASS one-line lines=1 | NF=13 | id=S056 | no-pipe-in-cells | no-escaped-pipe
      kind=docs | tier=A | status=rejected | opened=2026-10-26 | recheck=on-release
      one-https-token tokens=1 | teaches-REJECTED | teaches-flip | usedby=—
S058  PASS one-line lines=1 | NF=13 | id=S058 | no-pipe-in-cells | no-escaped-pipe
      kind=docs | tier=B | status=rejected | opened=2026-10-26 | recheck=180d
      one-https-token tokens=1 | teaches-REJECTED | teaches-flip | usedby=—
S059  PASS one-line lines=1 | NF=13 | id=S059 | no-pipe-in-cells | no-escaped-pipe
      kind=spec | tier=A | status=rejected | opened=2026-10-26 | recheck=on-release
      one-https-token tokens=1 | teaches-REJECTED | teaches-flip | usedby=—
SUMMARY fails=0
```

Cross-checked with the census parser's own semantics: `awk -F'|'` prints `NF=13` for all four files; `grep -cF '\'` prints 0 for all four (no escaped pipes anywhere — an earlier `escaped_pipe=1` reading was my own awk regex bug, `/\\|/` being alternation with an empty match, not a file defect). Enum domains per the census awk: kind `docs|spec` inside the E05 enum; tier `A|B` inside E06; status `mined|rejected` inside E07; opened `2026-10-26` passes E08 (past/present ISO); recheck `180d` (NNd) and `on-release` (symbolic `^[A-Za-z][A-Za-z0-9 _-]*$`) both pass E09.

- **S057 source cell vs manifest:** exactly one `https://` token, `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`, byte-equal to `ExecFrontierCapture.manifest.json` `sources[0].url` (the manifest's `capture_url` is the PDF, `landing_page.url` the same page URL — the split the binding rule B5 accepts).
- **S057 teaches/scope/source/kind/tier/status/opened/recheck/used-by:** byte-equal to the dispatched mandate (extracted from `wave1-spec.json` item `ScribeRowS057` and compared per cell: 9 of 10 cells BYTE-EQUAL; anchor is the one deviation, see F2).
- **Rejected rows' teaches:** all three start `REJECTED:` and carry `; flip:`; all three used-by cells are `—` (precedent S026–S028); W02 (thin reject) cannot fire (teaches 256/266/256 chars).
- **Rejected rows' anchor digests:** all six 64-hex tokens (`67bafe17…`, `1e73325c…` S056; `9375415c…`, `1dd123a8…` S058; `afb22b46…`, `ff875e45…` S059) occur verbatim in the round-38 fetch ledger `.ufo/waves/round-38/wave1/ScoutVexLeads.md` §1 (ledger rows #1/#2, #6/#7, #10/#9). Nothing invented.

## 3. Mirror run — census validate --file (the item's required run)

Mirror at `<scratch>/mirror/lane/`: lane `corpus/SOURCES.md` bytes with the four rows inserted into the `## Registry` table immediately after the S055 row (S057, then S056, S058, S059 → 59 registry rows); `corpus/knowledge/` copied from the lane plus the F22 entry deliverable landed at its used-by path `corpus/knowledge/cisa-when-to-issue-vex.md` (from `wave1/ScribeEntryF22.entry.md`); capture + manifest copied to `corpus/source-snapshots/round-39/`.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file <scratch>/mirror/lane/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	<scratch>/mirror/lane/corpus/SOURCES.md
exit=0
```

Exactly the expected result: exit 0, only W04 S028/S029 (the two pre-existing warnings; census-before.txt agrees), no new E/W code from any of the four rows.

**Mirror-read proof** (the checker read the mirror, not the real lane): same mirror with a probe row `| S900 | … | Z | … |` appended inside the Registry table and the S057 id mutated to `S057X`:

```
file	W04	S028 …
file	W04	S029 …
file	E02	S057X
file	E06	S900 tier=Z
probe-exit=1
```

**Placement checks on the mirror:**
- S057 sits at mirror line 62, immediately after S055 (line 61), inside `## Registry` (line 3), before `## Paths` (line 67) — the item's "inside the ## Registry table (after S055), not in ## Paths".
- E12 negative control: the same mirror with the S057 row moved under `## Paths` prints `file	E12	S057 row outside Registry section`, exit 1 — the instrument enforces the placement the item requires.

## 4. Independent instrument runs over the mirror (row present)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <mirror>/lane
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=1 bound=1 unbound=0
exit=0
```

`multi_row_url=0` confirms the S057 URL collides with no other registry row (checked independently: normalized new-row URLs — `www.cisa.gov/.../when-issue-vex-information`, `www.cisa.gov/.../minimum-requirements-vulnerability-exploitability-exchange-vex`, `github.com/openvex/spec/blob/main/OPENVEX-SPEC.md`, `cyclonedx.org/docs/1.7/json` — have no collision among the 55 existing rows), so the append cannot add a W04.

**Teaches-cell grounding, measured in S055's own capture** (`corpus/source-snapshots/round-38/S055.txt`, 5146 lines): `business decision` 0, `reaffirm` 0, `when to issue` 0, `issuance` 0; `inherit` 6 hits, all CSAF role-permission sentences (L4322–L4327), none vulnerability-status inheritance. The S057 teaches claim ("the layer the CSAF VEX profile (S055) does not carry") rests on zeros, not impressions.

**S057 anchor locators resolve in the committed capture** (`ExecFrontierCapture.S057.txt`, 275 lines, sha256 `11c8d6d6…5d64f2f` = manifest `sha256`): L12–14 business-decision sentence ✓, L79–81 "not determined by a strict protocol" ✓, L132–138 under_investigation lifecycle + timestamp reaffirmation ✓, L184–191 inheritance caution + exception ✓.

## 5. Findings

- **F1 (HIGH, cross-claim arithmetic; not a row defect; not resolvable in my write scope).** Frozen C2 `counting_commands` pins `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58` while the same claim's kill rule requires all four rows to land; measured pre-append count is 55 (`c2-controls/before.txt` agrees), so landing all four gives **59**, not 58. `ScribeRowsRejected.md` §5 F1 and `ScribeRowS057.md` §4 found the same independently; I confirm it from the delivered bytes. The rows themselves are consistent with the kill rule; the pinned counting command is unsatisfiable at the same time. The L1 owns the C2 report numbers; a wave-2 verifier running the pinned command at the judged head will read 59.
- **F2 (deviation from dispatch, justified, verified harmless).** The dispatched S057 anchor cell cited `pdftotext -layout` locators (L19-20, L129, L205-213, L287-294) that do not address the committed capture — L287-294 is past the end of the 275-line file (measured: capture L19-20 is a footnote line, L129 a KEV sentence, L205-213 trust-policy text). The landed anchor leads with capture-true lines (all four ranges verified to resolve, §4) and keeps the layout numbers as labeled parentheticals (`pdftotext -layout L19-20, L129` / `layout L205-213` / `layout L287-294`). Anchor is the only non-byte-equal cell (232 → 296 chars); every other cell matches the mandate exactly. This improves depth:verifiability (locators now resolve in the named file) and harms none; `ScribeRowS057.md` §3 documents the same deviation with a three-basis line-number table.
- **F3 (note).** Recheck cells: S057/S058 carry `180d`; S056/S059 carry `on-release`. My item's parenthetical names `180d` as the cadence example; the binding census check (E09) accepts both forms, and `on-release` matches the round-38 scout draft rows for these exact ids (ScoutVexLeads.md §4: S056/S057/S059 `on-release`, S058 `180d`). Recorded, not flagged as a defect.
- **F4 (note).** The S056 anchor carries the round-38 ledger's own `18:36:0xZ` timestamp placeholder verbatim — an honest citation of the ledger rather than inflated precision.

## 6. Out of scope / not claimed

No claim that the lane tree now holds the rows (the L1 lands them; validated as deliverable bytes over a mirror). No census-after claim on the live lane beyond the before-state rerun (`exit 0`, W04 S028/S029 — matches census-before.txt). No entry-QUALITY, harness, binding-on-live-tree, or audit claims. No lane/fleet/sibling/source-tree file written except this receipt; no mutating git command; no tooling installed (nothing needed: bash, gawk, python3 present).

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r39/RevRowsCensus/` (checker, mirror trees, probe copies, spec extracts) removed before yield; no `/tmp` residue.
