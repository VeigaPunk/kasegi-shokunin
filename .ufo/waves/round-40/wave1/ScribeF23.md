# ScribeF23 — round-40 wave 1 receipt (F23 admission package)

Seat: ScribeF23 (scribe, leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` only.
Base `a7af2ce63bce153757d39bf66b366a96caf30c13`; claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`.
No subagent dispatched. No lane file outside this seat's write scope was written; no mutating
git/jj command run anywhere; fleet root and `/home/vgpnk/Projects/shokuknow` untouched.
Tooling: nothing installed or upgraded (none needed). Scratch `/fast/scratch/hyaku/kasegi-r40/ScribeF23`
removed at exit; disk guard read green (`bash scripts/hyaku/disk-guard.sh status` ->
`/fast/scratch/hyaku 26% use, 598.9G free`), and this seat ran no heavy pass.

## 1. Deliverables (byte-exact, landable)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-40/wave1/ScribeF23.entry.md` | 322 | 22993 | `5a549e312237372a639931cc980ea697f60d383999790b9d48d5df4bd5d1978c` |
| `.ufo/waves/round-40/wave1/ScribeF23.readme-row.txt` | 28 | 2734 | `d6a9f3c1306525f91ddad82afc96e47b77043208ce42a115a0290db43cc9e15b` |
| `.ufo/waves/round-40/wave1/ScribeF23.province.txt` | 2 | 324 | `c445324c0f6d197f4c1b94f9509f86e3afd2af467d294dcb5bcac4e15c177408` |

- **Entry** lands at `corpus/knowledge/cyclonedx-analysis-subtree.md` (the path the H9 example block
  already names, adopted to avoid a cross-seat byte mismatch; my provisional longer name was dropped).
  H1 + four header lines in the corpus order `source:` / `verified-at:` / `ground: F23` / `recheck:`.
- **readme-row.txt** is the whole appended block: separator blank line, `## Round-40 admission — coverage
  map row and Frontier F23 (appended 2026-10-26)`, the R6 paragraph, the 3-cell coverage-map row, the
  6-cell F23 frontier row, and the `[r40 amendment, appended 2026-10-26]` count line naming 23/23.
- **province.txt** is the 2-line end-of-file append: separator blank line + the
  `[r40 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F23 — … (source S060)` line.
- Byte hygiene on all three: 0 tabs, 0 CR, 0 trailing-space lines, final newline present
  (`grep -cP '\t'` = 0, `grep -c $'\r'` = 0, `grep -cE ' +$'` = 0, `tail -c1 | od` = `\n`).

## 2. Provenance of the capture this entry rests on

The capture is ScoutF23Lead's deliverable, not mine; I verified it independently rather than trusting
the manifest.

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o cdx17.json.html \
    -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective} time=%{time_total}\n' \
    https://cyclonedx.org/docs/1.7/json/
status=200 bytes=6419901 url=https://cyclonedx.org/docs/1.7/json/ time=0.280503
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T21:17:47Z
$ sha256sum cdx17.json.html
02298a919ab2212c3554edea4e4ccb9d827f1436b407fcdd59ca5a85fa776040  cdx17.json.html
```

That raw digest differs from the scout's (`4d9c10da…`) at the same 6,419,901 bytes — the Cloudflare
mail-obfuscation rewrite the scout's manifest already discloses. Reproduction was therefore taken at
the normalized level, with the lane's own instrument imported read-only:

```
$ python3  # capture-source.py html_to_text() + collapse() over the fetched HTML
lines 22794 bytes 1041903
$ sha256sum page.txt
ffe8c0b6c155dab46098754e7ee757c441f230810fd353135fb2bd149f5ba7f4  page.txt
manifest full_text_sha256 ffe8c0b6c155dab46098754e7ee757c441f230810fd353135fb2bd149f5ba7f4   match True

$ python3  # title line + page-text L16060..L16169, joined with newlines
repro slice lines 111 bytes 4889 sha256 d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779
capture identical: True
```

So an independent third fetch reproduces ScoutF23Lead's committed slice byte for byte, and the page's
normalized full text matches the manifest's `full_text_sha256`. Capture facts as landed:
`ScoutF23Lead.capture.txt`, 111 lines, 4,889 bytes, sha256
`d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`, HTTP 200, final URL
`https://cyclonedx.org/docs/1.7/json/`, 0 redirects, fetched 2026-10-26T21:16:18Z, raw 6,419,901 bytes;
mapping capture line k ≥ 2 = page-text line 16058 + k.

## 3. Entry validation

### 3.1 Quotes are verbatim, unique, on their declared lines

Every quoted span in the entry was re-checked against the capture under whitespace collapse, with its
declared anchor:

```
anchored=12 ok=12 maxwords=21
```

Per span (`occ` = occurrences in the collapsed capture, `on` = capture line holding it):

| decl | words | occ | on | verdict |
|---|---|---|---|---|
| L4 | 10 | 1 | 4 | ok |
| L7 | 15 | 1 | 7 | ok |
| L18 | 10 | 1 | 18 | ok |
| L32 (response description) | 18 | 1 | 32 | ok |
| L32 ("More than one response is allowed.") | 6 | 1 | 32 | ok |
| L32 ("Responses are strongly encouraged…") | 12 | 1 | 32 | ok |
| L44 | 21 | 1 | 44 | ok |
| L47 | 11 | 1 | 47 | ok |
| L50 | 11 | 1 | 50 | ok |
| L53 | 10 | 1 | 53 | ok |
| L71 | 9 | 1 | 71 | ok |
| L106 | 10 | 1 | 106 | ok |

The table cells' quoted descriptions of the six `state` values (L10-L15) and three version `status`
values (L109-L111) resolve under the same collapse. Quoted spans in the entry that are not from S060 are
only the S055 quotation attributed to `S055.txt:L2151-L2152` and the rejected over-generalization labels
(text a reader might assert, marked as rejections).

### 3.2 The FC figures printed in the entry are measured, not remembered

```
SHALL 0        MUST 0        should 2 (L15, L44)
VEX 0          CSAF 0        CVSS 0        severity 0     score 0
product_status 0   known_affected 0   known_not_affected 0   under_investigation 0
component_not_present 0   vulnerable_code_not_present 0   vulnerable_code_not_in_execute_path 0
vulnerable_code_cannot_be_controlled_by_adversary 0   inline_mitigations_already_exist 0
(lane counts, grep -oiF) state=3 justification=2 response=3 analysis=6 detail=1 affects=1
                         firstIssued=1 lastUpdated=1
enum sizes: state 6 (L10-L15) justification 9 (L21-L29) response 5 (L37-L41) status 3 (L109-L111)
rare states once each: false_positive 1 (L14) in_triage 1 (L13) resolved_with_pedigree 1 (L11)
grep -n 'Default' → L105 only
```

### 3.3 Recheck line is a runnable command that binds the entry to its source

```
$ bash -n <the recheck command>            -> bash -n OK (exit 0)
$ head -c ... rc.sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-40/manifest.json --source S060
```

Q10 shape satisfied (`cd <lane-root> &&` prefix, human note after `#`), one `--source S060` equal to the
entry's single declared id (frontier harness rule A, both directions), and the declaration is exactly one
header `source:` line (`grep -c '^source:'` = 1). No line of the entry begins with `- S0` or `S0\d\d `
(other than the header/recheck lines), so S055/S057 stay prose citations and are not read as declarations.

Executed against a scratch mirror that carries the record as a manifest:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S060
S060:sha256 OK
S060:Q1 OK occurrences=1 anchor=7-ok
S060:Q2 OK occurrences=1 anchor=15-ok
S060:Q3 OK occurrences=1 anchor=50-ok
exit=0
```
(The manifest is scratch — built from `ScoutF23Lead.manifest-record.json` as `sources:[record]`, mirror
only. Assembly of the lane's `corpus/source-snapshots/round-40/manifest.json` is not this seat's scope;
until it exists the landed recheck line exits 2, which is its declared fail-closed behaviour.)

### 3.4 The C2 harness accepts the F23 entry (mirror run)

A `git archive HEAD PROVINCE.md corpus` export into scratch, then only scratch copies mutated: entry
copied in, capture copied to `corpus/source-snapshots/round-40/S060.txt`, scratch manifest written,
ScribeNewRows' three registry rows inserted, my two blocks appended, and the mirror entry's `recheck`
`cd` target repointed at the mirror (so the line exercises the mirror copy):

```
PASS     F23  knowledge/cyclonedx-analysis-subtree.md              ids=S060           exit=0
entries=26 pass=26 exit=0
```

That is the claim's `entries=26 pass=26` line with `PASS F23 ids=S060`, produced by the lane's own
`corpus/instruments/frontier-recheck-count.py`. The repointed `cd` is the only difference from the landed
bytes; on the lane the same line runs against the lane root.

## 4. README / PROVINCE append validation (mirror)

```
$ git -C <lane> show HEAD:PROVINCE.md > orig.province; diff orig.province mirror/PROVINCE.md
PROVINCE deleted=0 added=2
$ git -C <lane> show HEAD:corpus/README.md > orig.readme; diff orig.readme mirror/corpus/README.md
README deleted=0 added=28
$ wc -l mirror/PROVINCE.md mirror/corpus/README.md
160 / 542            (158+2 / 514+28 — matches the H9 seat's expected totals)

$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                 -> 23   (target 23)
$ grep -c '^## Round-40 admission' corpus/README.md          -> 1
$ grep -c '^\[r40 Frontier amendment' PROVINCE.md            -> 1
$ awk -F'|' '/^\| F23 \|/ {print NF-2}' corpus/README.md     -> 6 cells
$ awk -F'|' '/^\| Vulnerability analysis decisions in a CycloneDX BOM \(round 40\)/ {print NF-2}' -> 3 cells
$ grep -rlE '^source: S06[0-9]' corpus/knowledge | wc -l     -> 1  (corpus/knowledge/cyclonedx-analysis-subtree.md)
$ grep -c '⟨pending' corpus/knowledge/cyclonedx-analysis-subtree.md -> 0
```

F20-F22 comparison rows measured for shape: existing `F22` row `NF-2` = 6, existing round-39 coverage
row = 3 — the new rows match. The F23 `next` cell carries the comparison to S055's flag obligation and to
S057's issuance layer, the `false_positive`-has-no-CSAF-twin point, and the `Default: "affected"` trap,
all with `S060.txt:L<n>` anchors; it contains no `|`.

## 5. Findings

1. **Entry path is the H9 draft path, deliberately.** `ExecH9DeclaredBlocks` had already published example
   blocks and expected totals naming `knowledge/cyclonedx-analysis-subtree.md`; I adopted it and dropped
   my provisional `cyclonedx-vulnerability-analysis-states-and-justifications.md`. I sent that seat the
   final tails (PROVINCE 2 lines / 324 B / `c445324c…`; README 28 lines / 2734 B / `d6a9f3c1…`) and the
   unchanged 160/542 line counts, so its example digests can be refreshed from my files rather than retyped.
2. **Hard dependency outside this seat: the round-40 manifest.** The entry's `recheck:` names
   `corpus/source-snapshots/round-40/manifest.json` and `--source S060`; the record
   (`ScoutF23Lead.manifest-record.json`) and the capture must both be landed there by the integrator. I
   proved the pass on a scratch manifest; on the lane the line exits 2 (fail-closed) until it exists.
3. **Raw-page digest is not stable; the normalized capture is.** Three fetches (scout's two, mine) gave the
   same 6,419,901 bytes with differing raw digests but identical normalized text (`ffe8c0b6…f4`) and an
   identical 111-line slice. The entry discloses this in `verified-at:` and `## Honest limit` rather than
   claiming a byte-stable raw page.
4. **The slice carries no edition or normative-prose line.** It has no date, no ECMA number, no status
   line, and `MUST`/`SHALL` occur zero times. The entry therefore claims field definitions only and
   explicitly refuses the "v1.7 is the ratified edition" claim, which belongs to the overview/standards
   page. This is the honest-limit cost of a scoped capture and is stated, not hidden.
5. **`false_positive` is the load-bearing difference from S055.** CycloneDX's `state` can allege the
   finding does not belong to the component (L14); CSAF's four mandatory `product_status` categories have
   no such meaning, and the entry's `next` cell and claim 2 both say so with anchors.
6. **`Default: "affected"` (L105) inverts the tempting reading.** A version entry that omits its status
   asserts affectedness. The entry makes this a rejected over-generalization and a usage rule.

## 6. Out of scope (other seats)

- `corpus/SOURCES.md` S060 row — ScribeNewRows (landed in `ScribeNewRows.txt`; my simulation used it
  verbatim and the harness passed with `ids=S060`).
- Assembling `corpus/source-snapshots/round-40/{manifest.json,S060.txt}` and landing the entry/README/
  PROVINCE bytes — L1 / integrator.
- `corpus/instruments/knowledge-expected.txt` — ExecHarnessUpdate.
- Census, audit expected counts, binding increments, the nine-row decisions and the lesson/criteria
  corrections — their owning seats.
- No commit, push, or landing was performed; the lane working tree holds only my three deliverables plus
  the wave's other seats' files.

## 7. Report path

`.ufo/waves/round-40/wave1/ScribeF23.md` (this file).
