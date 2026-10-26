# ScribeRowS055 — S055 registry row for corpus/SOURCES.md

Axis: coverage. Milestone: round-38. Leaf seat, no dispatch.

## Behavior

Drafted the S055 row for the lane registry (`corpus/SOURCES.md`, table header at `:5`,
S054 as the model at `:60`) and wrote the single row line byte-exact to
`.ufo/waves/round-38/wave1/ScribeRowS055.row.md`. Line numbers in the `anchor` cell come
from my own `corpus/instruments/capture-source.py` normalization of the live page, and
that normalization is byte-identical to the sibling capture deliverable
`.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt` (proof below).

## Deliverable

- Path: `.ufo/waves/round-38/wave1/ScribeRowS055.row.md`
- 1 line, 1713 bytes, sha256 `901309af744b32383f3c8fe4c8023a960201baa65028600f0b9c31da59ff96cc`
- Shape: `awk -F'|'` → `NF=13` (11 cells), no `|` and no `\|` in any cell, cells:
  `S055` · source (`Common Security Advisory Framework Version 2.0 (OASIS Standard) — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`) ·
  `spec` · `A` · scope · anchor · teaches · `mined` · `2026-10-26` · `180d` ·
  `corpus/knowledge/csaf-vex-product-status-and-justifications.md`
- Cell check: `cells 11 / id S055 / kind spec tier A status mined opened 2026-10-26 recheck 180d / usedby corpus/knowledge/csaf-vex-product-status-and-justifications.md / url_in_source True`
- Landing note (not part of the deliverable): insert at **line 61** of
  `corpus/SOURCES.md`, i.e. immediately after the S054 row at `:60` and before the blank
  line that precedes `## Paths` (`:62`). Appending at EOF fails census `E12` (see Findings).

## Evidence

### 1. Scratch and fetch

```
S=/fast/scratch/hyaku/kasegi-r38/ScribeRowS055   (mkdir -p, TMPDIR=$S for every step)
curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o $S/live.html \
  -w 'http=%{http_code} bytes=%{size_download} ct=%{content_type} utc=%{time_starttransfer}\n' \
  https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
→ http=200 bytes=414858 ct=text/html utc=0.043514
date -u +%Y-%m-%dT%H:%M:%SZ → 2026-10-26T18:27:35Z
sha256sum $S/live.html → fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b
```

### 2. Normalization with the committed instrument

```
python3 corpus/instruments/capture-source.py --id S055 \
  --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html --out $S/snap/S055.txt
→ S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 \
  sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 \
  utc=2026-10-26T18:27:35Z out=/fast/scratch/hyaku/kasegi-r38/ScribeRowS055/snap/S055.txt
wc -l $S/snap/S055.txt → 5146
```

Byte agreement with the sibling capture deliverable (the file the L1 lands at
`corpus/source-snapshots/round-38/S055.txt`):

```
sha256sum .ufo/waves/round-38/wave1/ExecC2Capture.S055.txt $S/snap/S055.txt
→ 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  .ufo/waves/round-38/wave1/ExecC2Capture.S055.txt
→ 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  .../snap/S055.txt
wc -l  (both) → 5146 / 5146
cmp .ufo/waves/round-38/wave1/ExecC2Capture.S055.txt $S/snap/S055.txt → IDENTICAL
```

### 3. Anchor lines verified in the normalized capture (line → text head)

```
1854  3.2.3.9 Vulnerabilities Property - Product Status
1855  Product status (product_status) of value type object with 1 or more properties contains different lists of product_ids which provide details on the st…
1885  First affected (first_affected) of value type Products (products_t) represents that these are the first versions of the releases known to be affected…
1890  Known not affected (known_not_affected) of value type Products (products_t) represents that these versions are known not to be affected by the vulnera…
1891  This could for instance be because the code referenced in the vulnerability is not present, not exposed, compensating controls exist, or other factors…
1729  3.2.3.5 Vulnerabilities Property - Flags
1737  Every Flag item of value type object with the mandatory property Label (label) contains product specific information in regard to this vulnerability a…
1756  Label of the flag (label) of value type string and enum specifies the machine readable label. Valid enum values are:
1762  The given values reflect the VEX not affected justifications. See [VEX-Justification] for more details. The values MUST be used as follows:
1763  component_not_present: The software is not affected because the vulnerable component is not in the product.
1769  inline_mitigations_already_exist: Built-in inline controls or mitigations prevent an adversary from leveraging the vulnerability.
2843  6.1.27.7 VEX Product Status
2844  For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigatio…
2876  6.1.27.9 Impact Statement
2877  For each item in /vulnerabilities[]/product_status/known_not_affected it MUST be tested that a corresponding impact statement exist in /vulnerabilitie…
2328  6.1.6 Contradicting Product Status
2329  For each item in /vulnerabilities it MUST be tested that the same Product ID is not member of contradicting product status groups. The sets formed by …
2134  4.5 Profile 5: VEX
2135  This profile SHOULD be used to provide information of the "Vulnerability Exploitability eXchange". The main purpose of the VEX format is to state that…
2152  /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human …
```

Other anchor facts used in the row: labels `component_not_present` L1757,
`inline_mitigations_already_exist` L1758, `vulnerable_code_cannot_be_controlled_by_adversary`
L1759, `vulnerable_code_not_in_execute_path` L1760, `vulnerable_code_not_present` L1761;
eight-status JSON skeleton L1856-L1884; VEX SHALL list L2136-L2146 (`fixed`,
`known_affected`, `known_not_affected`, `under_investigation`) and L2151-L2156;
6.1.6 group sets L2330-L2341 (`Affected`/`Not affected`/`Fixed`/`Under investigation`);
revision date lines `L3 OASIS Standard`, `L4 18 November 2022`.

### 4. Census validation in the scratch mirror — exit 0

Mirror = `cp -a corpus $S/mirror/corpus` (lane `corpus/` at HEAD `7001535`), the
deliverable row inserted at the post-S054 position, and the sibling entry deliverable
copied byte-exact (sha256 `96899762d9d565ce32753ee3b4c80394aa64342b19c8bbe81e303fe15734f129`)
to `$S/mirror/corpus/knowledge/csaf-vex-product-status-and-justifications.md`.

```
diff <(cat ScribeRowS055.row.md) <(grep '^| S055 ' $S/mirror/corpus/SOURCES.md) → ROW_BYTE_IDENTICAL_IN_MIRROR
awk -F'|' '/^\| S055 \|/{print "NF="NF}' → NF=13
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $S/mirror/corpus/SOURCES.md → 55
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
→ file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
→ file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
→ file	ok	/fast/scratch/hyaku/kasegi-r38/ScribeRowS055/mirror/corpus/SOURCES.md
exit=0
```

Only the two pre-existing W04 warnings fire; both are present in the round-38
before-control `.ufo/waves/round-38/census-before.txt:1-2` verbatim, so the row adds no
warning and no error.

Census counts, same mirror:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file $S/mirror/corpus/SOURCES.md
→ file rows 55 / tier.A 52 / tier.B 1 / tier.C 2 / status.mined 43 / status.queued 9 / status.rejected 3 ; FLEET rows 55
bash .../sources-census.sh census --file corpus/SOURCES.md | head -1                    → file rows 54   (lane head, no S055)
bash .../sources-census.sh census --file $S/mirror/corpus/SOURCES.norow.md | head -1    → file rows 54   (mirror with the row removed)
```

### 5. Mutant controls (the row is load-bearing, not decorative)

Each mutant is the validated mirror with one cell edited, validated from inside
`$S/mirror/corpus` (so used-by resolution keeps its real root):

```
escaped_pipe (pairwise \| disjoint)  → file E01 S055 fields=12   exit=1
kind        (framework)              → file E05 S055 kind=framework exit=1
tier        (AAA)                    → file E06 S055 tier=AAA exit=1
status      (watched)                → file E07 S055 status=watched exit=1
usedby      (absent.md)              → file E11 S055 missing used-by corpus/knowledge/absent.md exit=1
norow       (S055 line deleted)      → file ok ... exit=0 (rows 54)
```

`E01 fields=12` is the concrete reason the item forbids a `\|`: awk counts an escaped pipe
as a separator, so a 11-cell row with one escaped pipe reads as 12 cells.

### 6. Pre-landing state of the lane (no lane edit by this seat)

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD → 700153593eb586c70a6499c8ca225ee4d673bc9b
git -C ... status --porcelain → ?? .ufo/waves/round-38/wave1.ready / wave1.ready.partial / wave1/
grep -n 'S055' corpus/SOURCES.md → no lines (id unused; no E03 duplicate)
grep -c 'csaf' corpus/SOURCES.md → 0 (URL+scope pair absent; no E04 duplicate)
```

## Gates / criteria touched

- Registry row count 54 → 55 on validation (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).
- `sources-census.sh validate` exit 0 in the mirror with S055 present and exit 0 with it
  removed — the row is the thing that moves rows 54 → 55 and it introduces no E-code.
- Row carries every C2 field the frozen claim names: id `S055`, tier `A`, kind `spec`,
  status `mined`, opened `2026-10-26`, recheck `180d`, used-by the F21 entry.

## Touched surfaces

- Wrote: `.ufo/waves/round-38/wave1/ScribeRowS055.row.md` (deliverable) and this receipt.
- Wrote: `$S` scratch only (`/fast/scratch/hyaku/kasegi-r38/ScribeRowS055/`), removed
  before yielding.
- Read-only: lane `corpus/` tree (copied to the mirror), `.ufo/waves/round-38/claims.json`,
  `wave1-dispatch.json`, `census-before.txt`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
  `corpus/instruments/capture-source.py`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
  `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`,
  `.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt`, `ScribeEntryF21.entry.md`.
- No lane file other than the deliverable and the receipt; no fleet-root, shokuknow, or
  sibling-lane write; no mutating git command; no tool install (nothing needed —
  python 3.14.8, gawk 5.4.1, bash 5.3.20 were already present).

## Findings

1. **Insert at line 61, never at EOF (landing trap).** Appending the row at end of file
   (after `## Paths`) validates as `file E12 S055 row outside Registry section`, exit 1.
   Observed directly on a first-draft mirror. The row must go immediately after the S054
   row at `corpus/SOURCES.md:60`.
2. **E11 is a landing-order dependency, not a row defect.** Before
   `corpus/knowledge/csaf-vex-product-status-and-justifications.md` exists in the lane,
   the same mirror prints `file E11 S055 missing used-by corpus/knowledge/csaf-vex-product-status-and-justifications.md`
   and exits 1. My exit-0 run therefore used the sibling's byte-exact entry deliverable
   (`ScribeEntryF21.entry.md`, sha256 `96899762…34f129`) at the used-by path; if the L1
   lands the row without the entry, census goes red on E11 with no change to the row.
3. **Anchor range corrected during drafting.** The per-status definition block starts at
   L1885 (`First affected (first_affected)`), not L1886 (`First fixed`); the row cites
   L1885-L1894 and names L1890-L1891 for `known_not_affected`.
4. **Revision binding added for contract compliance.** `SOURCES-CONTRACT-v1.md` requires
   the anchor to carry a revision; the row's anchor now names `OASIS Standard, 18 November
   2022, L3-L4` alongside the capture path and section/line anchors. Line numbers bind the
   exact bytes that will land: `cmp` says the sibling capture and my normalization are
   identical (sha256 `63c8ad52…e11cd42`, 5146 lines, 272441 bytes).
5. **No recency claim in scope**, per item: the scope cell says "no claim about how current
   or widely deployed the standard is"; the page itself is a dated 18 November 2022 OASIS
   Standard, not a rolling advisory feed.
6. **Overlap with the sibling entry's citation set** is consistent, not duplicated: the
   entry cites L1/L3/L4, L42, L394, L502, L510/L515/L516, L521-527, L1729/L1737/L1738,
   L1757-1769, L1855/L1887/L1888/L1890/L1891/L1894, L2069-2078, L2134/L2135/L2152-L2156,
   L2844/L2861, L2877, L2933, L3096/L3097; every line my row cites is inside that set, and
   the row adds the 6.1.6 contradiction-group test (L2328-L2341) that the entry does not use.

## Artifact paths (lane-relative)

- `.ufo/waves/round-38/wave1/ScribeRowS055.row.md` — the landable row (1 line, 1713 bytes,
  sha256 `901309af744b32383f3c8fe4c8023a960201baa65028600f0b9c31da59ff96cc`)
- `.ufo/waves/round-38/wave1/ScribeRowS055.md` — this receipt
- Scratch `/fast/scratch/hyaku/kasegi-r38/ScribeRowS055/` — removed before yield (nothing
  under it is referenced above except as historical command output).
