# ExecH4GateRows — round-40 located-source blocks for rejected rows S056/S058/S059

- Seat `ExecH4GateRows` (executor, leaf); lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only this seat: no lane file edited, no git/jj mutation).
- Axes: `depth:verifiability`, `coverage`; milestone round-40 build wave 1; item: round-39 lesson `## Gate` / `### Rejected` additions carrying URL + access date + a ≤25-word located quote for S056, S058, S059.
- Status: **delivered** — one deliverable with three landable append blocks, all quotes fetched live and re-located in the fetched bytes.
- Disk guard at start (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`): `/tmp 3% 125.2G free`, `/var/tmp 35% 585.3G`, `/fast/scratch/hyaku 26% 597.4G` — green.

## 1. Deliverable

| file | lines | bytes | sha256 |
|---|---:|---:|---|
| `.ufo/waves/round-40/wave1/ExecH4GateRows.txt` | 3 | 1151 | `cc5d6ee9116208fbc53b6e3dd05f118c5c6b8624dd202b6ea56dd266fbc3f90b` |

Measured:

```
$ cd .ufo/waves/round-40/wave1 && f=ExecH4GateRows.txt && \
    printf 'lines=%s bytes=%s sha256=%s\n' "$(wc -l < $f)" "$(stat -c%s $f)" "$(sha256sum $f | cut -d' ' -f1)"
lines=3 bytes=1151 sha256=cc5d6ee9116208fbc53b6e3dd05f118c5c6b8624dd202b6ea56dd266fbc3f90b
```

The file contains exactly three list-item blocks (one per row), no heading, no note, no table. Each block names
its row id, quotes the item-specified URL, carries the ISO access date `2026-10-26`, a locator (line number
and/or section anchor) and one verbatim sentence in double quotes followed by its word count.

**Landing point (append-only):** immediately after `corpus/lessons/round-39.md:42` — the second line of the
existing S059 `### Rejected` bullet (`  scoped capture; flip: a CycloneDX-vs-CSAF entry with scoped
analysis-subtree capture.`) — inside `### Rejected` (heading at `:36`), before the blank line at `:43` and
`### Candidates considered and not taken` at `:44`. The three blocks are additional bullets in the same list;
the pre-existing three bullets are untouched. Read at the frozen claims head, the section reads:

```
36:### Rejected
37:- S056 (CISA Minimum Requirements for VEX) — REJECTED: vocabulary already mirrored by S055; flip: a round that
38:  needs the consumer-side minimum-elements phrasing or tool-neutral metadata rules.
39:- S058 (OpenVEX v0.2.0) — REJECTED: same labels; community spec at mutable `main`, no release date; flip: pinned
40:  commit + release date + a ground needing its label-over-free-text recommendation.
41:- S059 (CycloneDX v1.7 analysis) — REJECTED: different vocabulary is a separate frontier; 6.4MB reference needs a
42:  scoped capture; flip: a CycloneDX-vs-CSAF entry with scoped analysis-subtree capture.
43:
44:### Candidates considered and not taken
```

## 2. Live fetch ledger (curl, `-A kasegi-shokunin/1.0`, `--max-time 90`)

Work dir `S=/fast/scratch/hyaku/kasegi-r40/ExecH4GateRows`; `TMPDIR` was not inherited, all artifacts bound under `$S`.

```
$ for spec in \
   "S056|https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex|s056.html" \
   "S058|https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md|s058.md" \
   "S059|https://cyclonedx.org/docs/1.7/json/|s059.html" ; do
    id=${spec%%|*}; rest=${spec#*|}; url=${rest%%|*}; out=${rest##*|}
    t=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    code=$(curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' -o "$out" -w '%{http_code}' "$url")
    bytes=$(stat -c %s "$out"); sha=$(sha256sum "$out" | cut -d' ' -f1)
    echo "$id $url code=$code bytes=$bytes sha256=$sha utc=$t"
  done
S056 https://www.cisa.gov/resources-tools/resources/minimum-requirements-vulnerability-exploitability-exchange-vex code=200 bytes=49253 sha256=67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8 utc=2026-10-26T21:14:50Z
S058 https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md code=200 bytes=30580 sha256=9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884 utc=2026-10-26T21:14:50Z
S059 https://cyclonedx.org/docs/1.7/json/ code=200 bytes=6419901 sha256=c5384e398bcce3e0815646b1e3ef3fdddacfedbc90ead9939e77288ed648bd72 utc=2026-10-26T21:14:50Z
```

Second S059 fetch (determinism probe):

```
$ curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0' -o s059.b.html -w '%{http_code}' https://cyclonedx.org/docs/1.7/json/
S059-refetch code=200 bytes=6419901 sha256=ccbf7e690edb677a8582efcc6a2d85ec874855210d7dbf260a4aa6e53c691dab utc=2026-10-26T21:16:44Z
```

Digest comparison with the row's recorded round-38/39 fetches: S056 and S058 are byte-identical to the
recorded digests (`67bafe17…a8eab8`, `9375415c…19f884`). S059 is not: the round-38 ledger records
`afb22b46d49ad68a648cfb1b9ec3f0f47028cc6170a8ad133603fac30e88f3f9` at the same 6,419,901 bytes, and two
fetches this seat differ from it and from each other at the same length. `cmp -l` shows 3,967 differing
bytes in 62-byte runs spread across the page (first at byte 74,040, last ending at 6,190,932), none
overlapping the quoted sentence at bytes 4,189,124–4,189,223. The page is dynamically generated; the stable
evidence is the section anchor plus the quote, not a page digest. See §4.

## 3. Located quotes, re-verified in the fetched bytes

| row | source (fetched bytes) | locator | quote | words | occurrences in fetched bytes |
|---|---|---|---|---:|---:|
| S056 | `s056.html`, 49,253 B, sha256 `67bafe17…a8eab8` | publication-page summary paragraph, raw HTML L1146 (byte offset 36,986; same paragraph is normalized visible-text line 107); the page's `Publish Date` is April 21, 2023 and it links `minimum-requirements-for-vex-508c.pdf` (1,023.41 KB) | `These elements are derived from, but may not fully conform to, existing VEX documentation and implementations.` | 16 | 1 |
| S058 | `s058.md`, 30,580 B (671 lines), sha256 `9375415c…19f884` | `OPENVEX-SPEC.md:373`, section `### Status Justifications` (heading L362), table row `component_not_present` | `The product is not affected by the vulnerability because the component is not included.` | 14 | 1 |
| S059 | `s059.html`, 6,419,901 B, sha256 `c5384e39…48bd72` | section `vulnerabilities[].analysis.state`, anchor `#vulnerabilities_items_analysis_state` (raw HTML L770; normalized rendered text L24567; byte offset 4,189,124) | `Declares the current state of an occurrence of a vulnerability, after automated or manual analysis.` | 15 | 1 (also 1 in the second fetch) |

Verification command and output:

```
$ python3 - <<'PY'
checks=[
 ('S056','s056.html','These elements are derived from, but may not fully conform to, existing VEX documentation and implementations.'),
 ('S058','s058.md','The product is not affected by the vulnerability because the component is not included.'),
 ('S059','s059.html','Declares the current state of an occurrence of a vulnerability, after automated or manual analysis.'),
]
for sid,f,q in checks:
    b=open(f,'rb').read(); print(f'{sid} occurrence={b.count(q.encode())} words={len(q.split())} source_bytes={len(b)}')
PY
S056 occurrence=1 words=16 source_bytes=49253
S058 occurrence=1 words=14 source_bytes=30580
S059 occurrence=1 words=15 source_bytes=6419901
```

S058 row read verbatim at the pinned line:

```
$ sed -n '373p' s058.md | cut -c1-140
| `component_not_present` | The product is not affected by the vulnerability because the component is not included. The status justification
```

S059 anchors present in the fetched bytes:

```
$ grep -c 'id="vulnerabilities_items_analysis_state"' s059.html
1
```

Word counts are whitespace-split counts of the quoted spans only (16, 14, 15 — all ≤25). Access date in all
three blocks is the fetch date `2026-10-26` (UTC fetches above). URLs are the item-specified URLs, byte-exact
in the blocks. S056's quote is CISA's own summary of the v1.0.0 document on the fetched page; the page also
carries the linked 508c PDF.

## 4. Risks / notes

- **S059 page is not byte-stable.** Same length, different digest on every fetch (3,967 bytes in 62-byte runs).
  A future verifier should re-check the quote at the `#vulnerabilities_items_analysis_state` anchor, not a
  page sha256. The deliverable itself carries no digest so it cannot be invalidated by page churn; the digest
  above only pins the bytes this seat read at 2026-10-26T21:14:50Z.
- **S058 URL is the mutable `main` ref** (the row already records this as the reason for rejection). The
  quote/digest pair is valid at fetch time; a later commit can move the line numbers.
- **S056 page digest equals the round-38/39 recorded digest**, so the quote location (raw HTML L1146) is
  reproducible against those recorded bytes.
- H4's wording is "each carry a URL, an access date and a <=25-word located quote": each block starts with
  the exact row id, contains exactly one `https://` URL, one ISO date, one locator and one quoted span with
  its word count. If the suite slices the `### Rejected` list, the blocks are inside it at the stated landing
  point; if it greps the whole lesson, the row ids disambiguate without a heading.

## 5. Scope and hygiene

- Writes: only `wave1/ExecH4GateRows.txt`, `wave1/ExecH4GateRows.md` (this receipt) and scratch under
  `$S`. No lane/ tracked file, fleet-root file, sibling repo, `~/.local/bin`, config or service touched.
- No tool installation; no package manager run; no git/jj mutation; no subagent dispatch.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/ExecH4GateRows` removed before yield (`trap 'rm -rf -- "$S"' EXIT`);
  the fetched sources are not copied into the lane.
