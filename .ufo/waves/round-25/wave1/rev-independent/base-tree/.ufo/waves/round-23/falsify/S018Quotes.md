# Falsify — S018 six-quote binding (C2 coverage F06)

Seat: `L1Kasegi23.S018Quotes-2` · lane: round-23 falsify · read-only attack on landed bytes.
Target under test: `corpus/source-snapshots/round-23/S018.txt` vs the six Evidence rows in
`corpus/knowledge/multiparty-vulnerability-coordination.md` (lines 25-30) and the S018 block of
`corpus/source-snapshots/round-23/manifest.json`.

All paths absolute below are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Verdict

| # | Claim attacked | Result | Confidence |
|---|---|---|---|
| Q1-Q6 | Each of the six quotes is an exact substring of the pinned excerpt at the stated heading | **holds** — 6/6, one occurrence each, single line each | high (byte-level) |
| Q7 | The entry's "Located source" heading text names the excerpt's actual heading | **holds** — 6/6, with two cosmetic notes (B1, B2) | high |
| Q8 | The entry's "version 1.1, Spring 2020" (md:2, md:21) / SOURCES.md:24 "released Spring 2020" is a statement of the excerpt | **unsupported by pinned bytes** — the excerpt carries no title, no URL, no version and no date statement at all | high (absence verified); "Spring 2020" has zero local support anywhere in the snapshot dir |

Nothing in the six quotes fails. The single falsifiable defect is provenance of the version
attribution, not the quoting.

## Evidence — quote binding

Snapshot digest matches the manifest, so the bytes checked are the pinned bytes:

```
$ sha256sum corpus/source-snapshots/round-23/S018.txt
d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  corpus/source-snapshots/round-23/S018.txt
# manifest S018.sha256 == d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
```

Programmatic substring test (md quote extracted from the row, curly delimiters U+201C/U+201D
stripped, counted against snapshot lines):

```
LOC='Definitions — Coordinator' words=14 exact_line_hits=[6] in_doc=True
LOC='Definitions — Upstream Vendor' words=11 exact_line_hits=[15] in_doc=True
LOC='Maintain clear and consistent communications — Prior to disclosure' words=12 exact_line_hits=[36] in_doc=True
LOC='Maintain clear and consistent communications — Prior to disclosure' words=11 exact_line_hits=[40] in_doc=True
LOC='Minimize exposure for stakeholders' words=20 exact_line_hits=[72] in_doc=True
LOC='Use coordinators when appropriate' words=15 exact_line_hits=[85] in_doc=True
```

Occurrence counts (rules out "matched a different occurrence"): every manifest quote has
`count= 1` in `S018.txt`. Word counts are 11-20, all within the entry's stated 25-word ceiling.
The md quotes and the manifest `quotes[].quote` strings are byte-identical for all six (no drift
between the assertion store and the prose entry).

Excerpt heading structure, for the heading-match axis:

```
$ grep -n -E "^#{1,4} |^\*\*" corpus/source-snapshots/round-23/S018.txt
1:## Definitions
21:## Guiding Concepts and Best Current Practices
25:### Establish a strong foundation of processes and relationships
32:### Maintain clear and consistent communications
34:**Prior to disclosure**
44:**After disclosure**
53:### Build and maintain trust
61:### Minimize exposure for stakeholders
74:### Respond quickly to early disclosure
80:### Use coordinators when appropriate
```

## Evidence — typographic apostrophe (line 72)

The apostrophe in "other vendors’ components" is U+2019, in both the snapshot and the entry:

```
$ sed -n '72p' corpus/source-snapshots/round-23/S018.txt | hexdump -C | grep "e2 80 99"
00000070  20 76 65 6e 64 6f 72 73  e2 80 99 20 63 6f 6d 70  | vendors... comp|
# per-character: ['0x2019', '0x20']  -> 'vendors’ components.'
$ sed -n '29p' corpus/knowledge/multiparty-vulnerability-coordination.md : apostrophe codepoint 0x2019, U+2019 present = True
```

Byte offset of the line-72 quote: 7240, length 133 bytes; line 72 confirmed by newline count.

This matters because it removes the "normalization artifact" escape: the excerpt preserves
typography at three independent points, so a non-ASCII character surviving into the entry is
evidence of a byte-faithful copy, not of a lossy transcription.

Non-ASCII inventory of the whole snapshot (only 4 characters, all typographic):

```
16 0x2019  - **Downstream Vendor:** ... downstream vendor’s product ...
37 0x201c  - ... such as security@ email addresses and “slash security” (/security) web pages.
72 0x2019  - Vendors should be aware ... vendors’ components.
```

(Line 37 also supplies the matching 0x201d.) Corollary: nothing in the excerpt was ASCII-folded,
so no quote could be accidentally "exact" by normalization.

## Evidence — the excerpt's own version statement: there is none

```
$ head -1 corpus/source-snapshots/round-23/S018.txt
## Definitions
$ grep -n -i -E "version|v1|spring|20[0-9][0-9]|first\.org|guidelines" corpus/source-snapshots/round-23/S018.txt
3:Within the context of this document, the following definitions apply. Definitions that are available in ISO/IEC 29147:2014[3](#fn-3) are used with minimal modification.
```

That single hit is a normative reference to another standard, not a statement about this
document. The file begins directly at `## Definitions` (no BOM: first bytes `23 23 20 44 65 66 69 6e 69 74 69 6f 6e 73`), is 86 lines / 8372 bytes,
and contains no title, no "Version:", no date, and no self-URL.

```
$ grep -rn -E "Spring|2020" corpus/source-snapshots/round-23/
corpus/source-snapshots/round-23/S030.txt:172: ... CVE-2020-2761 ... CVE-2020-5229 ... CVE-2020-29380 ...
```

No "Spring" anywhere in the snapshot directory; the only "2020" hits are CVE identifiers in the
unrelated S030 capture.

Contrast with the sibling capture, which shows the format *does* record version headers when the
captured text carries them — so the absence in S018 is a property of this capture, not of the
snapshot schema:

```
$ for f in S018 S029 S030; do printf "%s: " "$f"; grep -c "^URL:" corpus/source-snapshots/round-23/$f.txt; done
S018: 0
S029: 0
S030: 1
$ grep -n -m3 -E "4\.2\.0|Version" corpus/source-snapshots/round-23/S030.txt
1:URL: https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf
12:#### Version: 4.2.0
18:#### CNA Operational Rules 4.2.0
```

Manifest schema: `sources[].keys == ['id', 'path', 'sha256', 'quotes']`; the manifest has no
`version`/`title`/`retrieved_from` field, and its own purpose string scopes it to "pinned
excerpt … verifies captured bytes, not current upstream freshness". `source-recheck.py` validates
only `schema_version`, digest and quote substrings (no version/title handling: grep shows
`SCHEMA_VERSION` only). Therefore no corpus artifact asserts "1.1" except:

- the URL path segment `guidelines-v1.1` written by the entry itself (md:2), which is a
  URL-name inference and not an excerpt statement;
- the prose "version 1.1, Spring 2020" (md:2), "version 1.1" (md:21), and SOURCES.md:24
  "version 1.1, released Spring 2020".

**Falsifier (restated so it can be run against a future artifact):** if a reader treats the
entry's version/date as a statement of S018, they cannot confirm it from the pinned bytes. The
"v1.1" half has at least a URL-text basis; **"Spring 2020" has no basis in any round-23 artifact**.

## Evidence — excerpt is truncated mid-document, without an elision marker

- Line 23 (`## Guiding Concepts and Best Current Practices` prose) reads: "…the cases, variants,
  responses, and preventions discussed later in the section on Multi-Party Disclosure Use Cases."
  That section is not in the file; the file ends at line 85 with the last bullet of
  `### Use coordinators when appropriate` (line 86 is empty).
- `grep -n -E "\[…\]|\[\.\.\.\]|\.\.\.|\(cut\)|trimmed|excerpt"` over `S018.txt` → **NO MARKERS**.

The entry's scope label "Definitions and Guiding Concepts and Best Current Practices" (md:2) is
accurate for what the excerpt contains, and md "## Limits" does say "captured public-source
excerpt", so no written claim is contradicted. The residual gap is that no artifact records the
cut point, so any future instruction to verify an S018 statement from the use-cases section would
be unanswerable from pinned bytes while looking answerable.

## Cosmetic / precision notes (no claim fails)

- **B1** — `Maintain clear and consistent communications — Prior to disclosure`: the excerpt has
  one `###` heading and `**Prior to disclosure**` as a bold pseudo-heading (line 34), not a heading
  level. The entry's composite "heading — sub-label" is accurate in text and level-agnostic; no
  fix needed, but "heading" in the column header slightly overstates the structure.
- **B2** — `Definitions — Coordinator` / `Definitions — Upstream Vendor`: no excerpt heading reads
  "Definitions — Coordinator"; the pattern is `## Definitions` + a bold lead-in term
  (`- **Coordinator:**`, `- **Upstream Vendor:**`, lines 6 and 15). Composite label, correct.

## Scope limits (what I did not and cannot establish)

1. Captured bytes only. I did not re-open `https://www.first.org/…/guidelines-v1.1` (network
   re-open is out of scope for this seat and live external fetch was not attempted). Absence of a
   version banner in `S018.txt` does not prove the live page lacks one — the capture plainly starts
   at the `## Definitions` heading, so a page header/title banner could exist above the cut.
2. The recheck proves digest + quote containment, not that the excerpt is a complete or faithful
   rendering of the upstream page (no upstream comparison was made).
3. I did not evaluate the entry's Rule/Rejected/Falsifiable-check prose for correctness of
   interpretation — only the six quotes, their locations, and the metadata claims named in the
   assignment.
4. No mutation testing performed here (other seats own the mutate lanes); no production file was
   edited; only this report was written.
5. No tool install or update was performed for this seat (nothing needed beyond coreutils/python3).

## Remaining unknowns

- Whether FIRST's page carries a visible "v1.1 / Spring 2020" banner above `## Definitions`, which
  would make the entry's version attribution reproducible on a future re-capture.
- Recorded cut provenance for `S018.txt` (why the capture begins at `## Definitions` and ends at
  `## Use coordinators when appropriate`); nothing in the round-23 directory states it.
