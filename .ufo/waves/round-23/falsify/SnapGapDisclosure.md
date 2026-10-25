# SnapGapDisclosure — claims the pinned recheck cannot verify, and whether each entry says so

Seat: `L1Kasegi23.SnapGapDisclosure-2` (leaf, read-only). Lane: round-23 FALSIFY.
Attack surface: the three C2 entries against their pinned captures and
`corpus/source-snapshots/round-23/manifest.json`, plus the recheck the entries cite.

Production files, git/jj state, sibling lanes and the fleet repo were not touched. The only
write is this report. Scratch: `/tmp/kasegi-r23-falsify-SnapGap/`.

Question asked of every sentence: **does it read as established because a local digest
matched, when the digest cannot reach what the sentence asserts?**

## Working-tree state (concurrent landing, reconciled)

The three entries and the manifest changed **while this review was running** — mtimes
`03:39:18` (F06, F07), `03:39:50` (F08), `03:40:08` (manifest); I read the pre-change bytes and
re-verified every citation below against the post-change bytes at `03:41`.

```
git diff --stat -- corpus/knowledge corpus/source-snapshots/round-23/manifest.json corpus/instruments/resolve.py
 corpus/knowledge/cna-assignment-and-vulnerability-rules.md |  2 +-
 corpus/knowledge/cra-manufacturer-reporting-duties.md      | 14 ++++++++++++--
 corpus/knowledge/multiparty-vulnerability-coordination.md  |  9 ++++++++-
 corpus/source-snapshots/round-23/manifest.json             |  2 +-
 corpus/instruments/resolve.py                              |  8 ++++----
```

The landing added: a `Capture gap (disclosed)` paragraph to F06 (lines 56-61); the OJ-date
disclosure to F08 (lines 79-81); an ambiguity paragraph to F08 (lines 52-56); a
`Clock (paraphrase; exact wording in the quotes table)` header to F08 (line 27); a
location-binding ceiling sentence to `manifest.json.purpose`; and an absolute `cd` prefix on
the three `recheck:` lines. Two findings below were **partially** answered by that landing; they
are marked as such, and the surviving defect is stated. `corpus/instruments/source-recheck.py`
is unmodified (`git diff --stat` empty for it), so every blindness experiment still applies to
the current instrument.

## Verdict

| id | Finding | Class | Severity |
|---|---|---|---|
| S-1 | `cna-assignment-and-vulnerability-rules.md` cites `page 7` twice (`:25-26`) and `pages 9–10` once (`:33`). The capture has **no page markers 3–7 at all**, and 3.2.4.2 sits wholly before the `Page 10` marker; deleting every page marker leaves the recheck at rc=0. The new manifest ceiling says location binding is not machine-checked — but the entry's own note still does not, and two citations are contradicted by the capture, which no ceiling note repairs. | official-byte fidelity / location | **Medium** |
| S-2 | The F07 quote-fidelity note (`:39-42`) answers a fidelity challenge with the manifest digest, but the "literal bytes" it invokes are a `markit` PDF conversion (`S030.txt:1-4`); conversion provenance is disclosed nowhere, and the new ceiling covers location binding, not conversion. | official-byte fidelity | **Medium** |
| S-3 | F08 rows for Article 14(4)(a) (`:32`) and 14(4)(b) (`:33`) are pinned by **no** manifest quote, while the header now promises "exact wording in the quotes table". Mutating 14(4)(a)'s 24-hour clock to 30 days leaves the published recheck at 22/22 OK, rc=0. | coverage / verifiability | **Medium** |
| S-4 | Two disclosures name a base that carries only part of their claim: F08 `:79-81` ("rests on the ELI URL") for `OJ 20.11.2024`, and F06 `:58-59` ("rests on the opened URL segment (`…/guidelines-v1.1`)") for "version 1.1, **Spring 2020**". An ELI path carries no publication date; a version slug carries no season/year. | false/partial provenance inside a disclosure | **Medium** |
| S-5 | F07 `:14-17` asserts the 4.1.0→4.2.0 section move (4.1.10 → 4.1.9). No S022 capture exists, the S022 registry row is `queued` with no used-by, and the named recheck cannot fail on it. | version currency / provenance | **Medium** |
| S-6 | The manifest carries no `url`, `retrieved_at` or HTTP status; injecting `https://example.invalid/…`, `1999-01-01`, `599` into a scratch manifest leaves 22/22 OK, rc=0. Header claims of the form "URL", "opened 2026-10-20" sit beside a recheck blind to them. | freshness / provenance | **Medium** |
| S-7 | F06 `:21` and its new disclosure `:59` both say the page was "opened 2026-10-20"; `SOURCES.md:24` records `opened` = `2026-10-19`. No capture arbitrates. | freshness | **Low** |
| S-8 | All three `recheck:` lines carry a command only, no cadence/date, although QUALITY.md Q1 asks for "date or cadence plus the runnable command"; the cadence lives only in `SOURCES.md` (S018 `180d`; S029/S030 `on-release`). | freshness mechanism | **Low** |

Nothing above contradicts a quoted string. All 19 manifest quotes and all 3 digests pass
(`22/22 OK`) when the published commands run; the defects are in what the pin and the prose
cover, not in quote exactness.

## Baseline reproduced (not taken from the L1 claim)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/source-snapshots/round-23/S018.txt corpus/source-snapshots/round-23/S029.txt \
          corpus/source-snapshots/round-23/S030.txt
d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  S018.txt
82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  S029.txt
673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019  S030.txt

python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018  # rc=0, 7 OK lines
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029  # rc=0, 7 OK lines
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S030  # rc=0, 8 OK lines
```

Sizes: S018 86 lines / 8372 B; S029 145 lines / 19900 B; S030 248 lines / 26660 B.

What the instrument asserts, read from `corpus/instruments/source-recheck.py:27-143`:
`schema_version`, unique ids, a relative `path` confined to the manifest directory, a 64-hex
`sha256`, non-empty unique `quotes`, digest equality, and `quote in source_text`. It reads no
URL, date, HTTP status, page marker, or `verified-at` field:

```
python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-23/manifest.json'));print(sorted(m));print(sorted(m['sources'][0]))"
['purpose', 'schema_version', 'sources']
['id', 'path', 'quotes', 'sha256']
```

## S-1 — page citations no pinned byte supports (F07)

`cna-assignment-and-vulnerability-rules.md:25-26` cite `3.1.1, page 7` and `3.1.4, page 7`;
`:33` cites `section 3.2.4.2, pages 9–10`.

```
grep -n '<!-- Page' corpus/source-snapshots/round-23/S030.txt
8:<!-- Page 1 -->   20:<!-- Page 2 -->   76:<!-- Page 8 -->   95:<!-- Page 9 -->
112:<!-- Page 10 --> 134:<!-- Page 11 --> 155:<!-- Page 12 --> 168:<!-- Page 13 -->
186:<!-- Page 14 --> 209:<!-- Page 15 --> 227:<!-- Page 16 --> 242:<!-- Page 17 -->

grep -c '<!-- Page [3-7] -->' corpus/source-snapshots/round-23/S030.txt   # 0
grep -n '^3\.1\.1 CNAs MUST' …/S030.txt                                   # 64:…
grep -n '3\.1\.4 For Scope Definitions' …/S030.txt                        # 73:…
grep -n '3\.2\.4\.2 A CNA MUST provide' …/S030.txt                         # 110:…
```

The converter's marker sequence jumps `Page 2` → `Page 8`; `3.1.1` (line 64) and `3.1.4`
(line 73) both fall inside that unmarked gap, so "page 7" is not derivable from the capture. It
can only come from the real PDF's pagination, which is not under test. `3.2.4.2` at line 110
precedes the `Page 10` marker at line 112, so the capture places it on page 9 only — not
"pages 9–10".

Blindness proof (scratch copy, digest recomputed):

```
rewrite of /tmp/kasegi-r23-falsify-SnapGap/mut-pages/S030.txt removing all
`<!-- Page N -->` markers: 12 -> 0; manifest sha256 recomputed
python3 corpus/instruments/source-recheck.py --manifest …/mut-pages/manifest.json --source S030
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
… (all 8 lines OK)
rc=0
```

Control that the instrument is not weak everywhere — mutate quoted text, recompute the digest,
and it fails closed:

```
mutate 3.1.1 "CNAs MUST develop" -> "CNAs SHOULD develop"; digest recomputed
S030:sha256 OK
S030:rule-3-1-1-scope-definition MISMATCH reason=quote-not-found
… rc=1
```

The manifest's new ceiling sentence now says this in general terms: *"quote-to-location binding
is human-verified and is not machine-checked, so exit 0 does not prove a sentence sits at the
article or rule the entry names."* That is a genuine improvement and it lowers the severity of
the *generic* form of this class. What survives: the ceiling lives in the manifest, not in the
entry beside the failing citations; it does not say any specific citation is wrong; and the
`3.2.4.2, pages 9–10` span is contradicted by the capture rather than merely unchecked. A
reader who runs the entry's own command sees `OK` eight times and no warning.

**Smallest safe correction:** replace the page column with capture-relative locations
(`S030.txt:64`, `S030.txt:73`, `S030.txt:110`), or drop the page column; and append the
manifest ceiling's first clause to the entry's quote-fidelity note so the warning travels with
the table.

## S-2 — a fidelity note that settles fidelity with the digest, over a conversion (F07)

`cna-assignment-and-vulnerability-rules.md:39-42`:

> Quote-fidelity note: the captured 4.1.9 line marks its final term with `<u>` emphasis
> (`are <u>Independently Fixable</u>.`). The table above quotes the rendered text;
> `corpus/source-snapshots/round-23/manifest.json` asserts the excerpt's literal bytes, which
> is what the recheck compares.

The note is accurate about what it says and still leaves the decisive layer unnamed:

```
head -4 corpus/source-snapshots/round-23/S030.txt
URL: https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf
Content-Type: application/pdf
Method: markit
Notes: Converted with markit
```

The "literal bytes" are a `markit` rendering. `<u>` is a converter annotation, not PDF content;
the page markers are converter pagination; and any character dropped or reordered by conversion
is preserved by the digest rather than detected by it. A reader who sees `sha256 OK` plus this
note reasonably concludes the quote's fidelity to the PDF has been checked. Capture stability
was checked. The new purpose ceiling does not cover this either — it bounds *location* binding,
not conversion fidelity.

`multiparty-vulnerability-coordination.md` has the same unstated layer with more cover: S018
has no provenance banner (`head -c 300` begins at `## Definitions`), yet it is a rendering —
`S018.txt:3` carries a rewritten footnote anchor `[3](#fn-3)` and the body a site-absolute image
path `![Stakeholder roles and communication paths](/global/sigs/…figure-1.jpg)`. The new
`Capture gap (disclosed)` paragraph (`:56-61`) fixes the *boundary* question but not the
*rendering* question: it says the capture has no title/version/date and is cut at the end of
`Use coordinators when appropriate`, and names neither conversion nor retained format.

**Smallest safe correction:** append to the note — "S030 is a `markit` conversion of the PDF;
the digest proves capture stability, not PDF-byte equality, and `<u>` markers and
`<!-- Page N -->` breaks are converter artifacts." For F06, add one clause to `:56-61`:
"its bracketed footnote anchors and image path show a rendering, not verbatim bytes."

## S-3 — the track table's incident rows are pinned by nothing (F08)

`:32-33` assert the distinction the entry exists for:

```
| Trigger and actor | Stage | Clock (paraphrase; exact wording in the quotes table) | Located support |
| Manufacturer becomes aware of a severe incident … | Early warning | … within 24 hours of awareness | Article 14(4)(a) |
| Same incident | Incident notification | … within 72 hours … | Article 14(4)(b) |
```

The manifest pins `art14-2a`, `art14-2b`, `art14-2c`, `art14-4c`,
`art71-article-14-start`, `art71-general-application` — nothing covers 14(4)(a) or 14(4)(b):

```
python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-23/manifest.json'));print([q['id'] for s in m['sources'] if s['id']=='S029' for q in s['quotes']])"
['art14-2a-early-warning', 'art14-2b-vulnerability-notification', 'art14-2c-final-report',
 'art14-4c-incident-final-report', 'art71-article-14-start', 'art71-general-application']
grep -n '^| Article 14(4)' corpus/knowledge/cra-manufacturer-reporting-duties.md
48:| Article 14(4)(c) | “within one month after the submission of the incident notification under point (b)” |
```

The quotes table therefore has no 14(4)(a) or 14(4)(b) row, so the header's promise —
"exact wording in the quotes table" — is true for four rows and false for the two incident
clock rows. Mutation proof (scratch copy, digest recomputed):

```
14(4)(a): "…within 24 hours" -> "within 30 days"; manifest sha256 recomputed
python3 corpus/instruments/source-recheck.py --manifest …/mut-14-4a/manifest.json --source S029
S029:sha256 OK
S029:art14-2a-early-warning OK
… (all 7 lines OK)
rc=0
```

A second-order effect: `art14-2a`'s quote is `within 24 hours of the manufacturer becoming
aware of it`, which occurs at both `S029.txt:10` (14(2)(a)) and `S029.txt:20` (14(4)(a)), so
even a borrowed pin could not bind the incident row. The entry already discloses the
duplicate-substring limitation (`:52-56`) — honest, and not sufficient: the incident track has
no assertion at all, and the paraphrase header now implies it does.

**Smallest safe correction:** add two manifest ids with track-distinguishing wording —
`art14-4a-severe-incident-early-warning` = `a severe incident having an impact on the security
of the product with digital elements, without undue delay and in any event within 24 hours`,
`art14-4b-severe-incident-notification` = `an incident notification, without undue delay and in
any event within 72 hours of the manufacturer becoming aware of the incident` — and tighten
`art14-2a` to include `of an actively exploited vulnerability` so the tracks cannot satisfy each
other. Then the header's promise is true for all six rows.

## S-4 — disclosures that name a base which carries only part of the claim

**F08 `:79-81`:**

> The captured excerpt carries no OJ date line: the `OJ 20.11.2024` attribution in this
> entry's `source:` header rests on the ELI URL (`/eli/reg/2024/2847/oj/eng`) and the
> 2026-10-20 opening, not on the excerpt bytes.

First clause verified: `20.11.2024` count 0 in `S029.txt`; the only `Official Journal` line is
`S029.txt:120`, the generic entry-into-force sentence. Second clause is not: an ELI of the form
`reg/2024/2847/oj/eng` encodes year and regulation number, not an OJ publication date, so it
cannot ground `20.11.2024`. Once that clause fails, the date rests on nothing local but the
authored header. (Sibling `S029Quotes.md` reaches the same byte fact with the same "carried only
by the ELI URL" phrasing, so the same misattribution exists twice; fixing this entry is
independent of the sibling report.)

**F06 `:56-59`**, the newly added paragraph:

> Capture gap (disclosed): the pinned excerpt begins at `## Definitions` and carries no title,
> version banner or date, so its own bytes cannot confirm “version 1.1, Spring 2020”. That
> attribution rests on the opened URL segment (`…/guidelines-v1.1`) and the 2026-10-20 page
> opening; …

Boundary claim verified — `tail -3 S018.txt` ends with the last bullet of `Use coordinators
when appropriate`, exactly as described. Base claim partly false: `…/guidelines-v1.1` carries
`1.1` only; **no local byte anywhere carries "Spring 2020"**. The registry row (`SOURCES.md:24`,
anchor column) is the sole holder, and the sentence does not name it. This is the same defect
shape as F08's, in the opposite direction: a disclosure that suppresses a gap it just opened.

**Smallest safe correction:** F08 — delete "rests on the ELI URL (`/eli/reg/2024/2847/oj/eng`)
and", keep "rests on the 2026-10-20 opening and the registry row, not on the excerpt bytes".
F06 — replace "the opened URL segment (`…/guidelines-v1.1`)" with "the URL's version slug for
`1.1` and the registry anchor for `Spring 2020`". One clause each.

## S-5 — a comparative version claim whose earlier half has no base (F07)

`:14-17`:

> The public document's current version opened this round is 4.2.0. S022 preserves the earlier
> 4.1.0 source and must not silently become a claim about 4.2.0. The new S030 row records the
> successor. Never reuse old section numbers blindly: independently fixable guidance moved from
> 4.1.10 in 4.1.0 to 4.1.9 in 4.2.0.

The 4.2.0 half is attested (`S030.txt:12-16`: `Version: 4.2.0`, `Approved date:
2026-August-20`, `Effective date: 2026-August-25`; 4.1.9 at `S030.txt:165`). The 4.1.0 half is
not:

```
ls -1 corpus/source-snapshots/            # round-23   (only)
ls -1 corpus/source-snapshots/round-23/   # S018.txt S029.txt S030.txt manifest.json
grep -rln 'CNA_Rules_v4.1.0\|4\.1\.0' corpus/source-snapshots/   # no hits
grep -n '| S022 ' corpus/SOURCES.md       # status queued | opened 2026-10-19 | on-release | used-by —
```

No S022 snapshot, no manifest record, no quotes; the entry's `recheck:` argument is `--source
S030`. `SOURCES.md:53` records that CNA 4.1.0 was opened live on 2026-10-20, so the claim is not
invented — it is unretained, and the executable check beside it cannot fail on `4.1.10`. The
entry never says so.

**Smallest safe correction:** add an S022 capture + manifest record with a
`rule-4-1-10-independently-fixable` quote, or downgrade the sentence to "the 4.1.0 numbering is
reported by the registry row and is not rechecked here". The second is one line and harms no
axis.

## S-6 — provenance fields the pin cannot see

The manifest records `id`, `path`, `sha256`, `quotes`. The entry headers assert a URL, an open
date, and (F06) a version label. Demonstration on a scratch copy with source bytes unchanged:

```
inject into /tmp/kasegi-r23-falsify-SnapGap/manifest.json, per record:
  "url": "https://example.invalid/fabricated-<id>"
  "retrieved_at": "1999-01-01T00:00:00Z"
  "http_status": 599
python3 corpus/instruments/source-recheck.py --manifest …/manifest.json
S018:sha256 OK … S030:rule-4-2-12-uncertainty OK     (22 OK lines)
rc=0
```

Per-entry disclosure of the residue:

| Entry | Claim the pin cannot reach | Disclosed? |
|---|---|---|
| F06 `:2`, `:21` | URL identity; "opened 2026-10-20" | **Partial.** `:56-61` discloses that the bytes carry no title/version/date and that the attribution rests on URL + opening. It does not say the *opening* is unattested, and it names a partial base for "Spring 2020" (S-4). |
| F07 `:2`, `:21` | URL identity; "opened 2026-10-20"; "current version" at the open event | **Partial.** `:64-66` covers rule change and "not current online freshness"; the open-event assertion itself is unattested. |
| F08 `:2`, `:16-17` | URL identity; "opened the original official text on 2026-10-20" | **Partial.** `:16-18` bounds law/jurisdiction/product applicability; `:84-86` bounds platform/law/excerpt. "Opened … the original official text" remains an author assertion, and `S029.txt` carries no URL/Content-Type/Method header (`head -c 400` is a blank line then `Article 14`). |

**Smallest safe correction:** make the field non-optional and fail-closed — require non-empty
`url` and `retrieved_at` per record and emit `UNAVAILABLE reason=missing-provenance` when
absent. Local, offline, no network traffic; it moves the headers' provenance from untested to
structurally attested.

## S-7 — S018 open date: entries say 2026-10-20, registry says 2026-10-19

`:21` — "All quotes below are from S018, version 1.1, opened 2026-10-20"; the new `:59` repeats
"the 2026-10-20 page opening". `SOURCES.md:24`, by column: `status=mined`,
`opened=2026-10-19`, `recheck=180d`. `SOURCES.md:48` (the 2026-10-19 sweep) records FIRST v1.1
as opened and included; `:53` names FIRST v1.1 inside the 2026-10-20 follow-up — so a re-open on
2026-10-20 is possible, and `QUALITY.md:14` defines `verified-at:` as "the author re-opened it".
The defect is the bare word "opened", twice, restating the registry's `opened` field with a
different value. F07/F08 match their rows (2026-10-20); this inconsistency is F06's alone.

**Smallest safe correction:** "re-opened 2026-10-20 (first opened 2026-10-19; `SOURCES.md:24`)"
— in both places.

## S-8 — recheck lines with no cadence

```
grep -n '^recheck:' corpus/knowledge/*.md | grep -E 'multiparty|cna-assignment|cra-manufacturer'
…:4:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 … --source S0NN
```

QUALITY.md Q1 asks for "date or cadence plus the runnable command". All three carry the command
only; the cadence that would eventually force the freshness re-open each Limits promises lives
only in the registry (`SOURCES.md:24` `180d`; `:35,:36` `on-release`). No entry states when its
pinned capture expires as evidence.

**Smallest safe correction:** append the registry cadence — `; cadence 180d` / `; cadence
on-release`. Two words per entry.

## Sentences that read as verified because a local digest matched

Ranked by how much a reader is likely to over-infer:

1. **F07 `:39-42`** — "manifest.json asserts the excerpt's literal bytes, which is what the
   recheck compares." Offered as the answer to a quote-fidelity question; the answer is scoped
   to a converter's output the note never mentions (S-2), and the same table block cites page
   numbers the digest cannot reach (S-1). Clearest instance.
2. **F06 `:21`** — "All quotes below are from S018, version 1.1, opened 2026-10-20:" immediately
   above six `OK` rows. The landing added a disclosure at `:56-61`, which mitigates this — but
   the claim still stands unqualified where the reader evaluates it, it repeats a date the
   registry contradicts (S-7), and its "Spring 2020" base is partial (S-4).
3. **F08 `:16-17`** — "This entry opened the original official text on 2026-10-20; it does not
   claim a complete review of later implementing acts, consolidated amendments, jurisdiction, or
   product applicability." The disclaimer is real; "opened the original official text" is an
   identity claim about a capture with no retrieval headers and a demonstrable cut boundary
   (`sed -n '2p' S029.txt` → `Article 14`; `tail -c 120 … | od -c` → `) P o s i t i o`). Excerpt
   status is disclosed at `:84`; official fidelity is not.
4. **F08 `:27`** — "Clock (paraphrase; exact wording in the quotes table)" is a verification
   pointer, not a claim; it is listed because it points at a table that is missing exactly the
   two rows it is invoked for (S-3).
5. **F08 `:79-81`** — a disclosure whose form ("rests on the ELI URL") is precisely what a
   careful reader looks for, which misdirects while appearing to disclose (S-4).

## Claims that are correctly disclosed (kept, not attacked further)

- **Freshness, F06** `:50-52`: "not whether FIRST has changed since the capture. A future
  revision needs an official-source re-open and a new snapshot/expected baseline."
- **Freshness/currency, F07** `:64-66`: "Rules can change and exceptions exist. The executable
  recheck proves captured-source support only, not current online freshness…".
- **Jurisdiction/authority, F06** `:15-17`: "not a universal legal deadline, a mandate to
  contact anyone, or authorization to test an asset… remain operator-owned".
- **Jurisdiction/attribution, F07** `:12`, `:36-37`, `:51`: "CVE Program rules for CNAs, not
  universal bounty eligibility criteria"; "does not treat first refusal as unconditional or
  instruct any external contact".
- **Jurisdiction, F08** `:17-18`; **platform operation, F08** `:38-39` and `:86`: "not a claim
  that a particular platform is currently operating"; "cannot certify … operation of the
  reporting platform".
- **Location-binding ceiling, `manifest.json.purpose`** (landed 03:40): "quote-to-location
  binding is human-verified and is not machine-checked, so exit 0 does not prove a sentence sits
  at the article or rule the entry names." Accurate, and the strongest disclosure in the set
  for S-1/S-3 — it simply does not propagate into the entries.
- **Capture boundary, F06** `:56-57`, `:59-61`: begins at `## Definitions`, ends at `Use
  coordinators when appropriate`, later cross-referenced sections absent. Verified against
  `head`/`tail` of `S018.txt`.
- **Track ambiguity, F08** `:52-56`: discloses that the 24-hour phrase is non-unique and that a
  substring recheck cannot distinguish the rows. Accurate — S-3 is the narrower, still-open gap.

## Scope limits

- Read-only, no network fetch, no re-open of FIRST, cve.org or EUR-Lex: this report says nothing
  about whether any source has actually changed, and does not fault an entry for being
  unrefreshed.
- I did not verify the cited page numbers against the real PDF. That is the point of S-1: they
  are unverifiable from the artifact under test, and I make no claim about which page they
  actually fall on.
- Not adjudicated: C1 (`resolve.py` / mirror-containment) artifacts, the frontier denominator,
  or any sibling finding beyond the two cross-checks named (S018Quotes.md Q8, S029Quotes.md OJ
  date). Overlapping byte-level results are cited as corroboration, not re-filed.
- Findings reflect the working tree at `03:41` on 2026-10-25, after the concurrent landing
  described above; later edits to these files can invalidate a line pointer without invalidating
  the quoted sentence, which is reproduced verbatim in each finding.
- No admission, score movement, integration, or self-credit is claimed.

## Tooling

No installs or updates; no package transactions (the pacman pause was not touched). Only
`python3`, `grep`, `sha256sum`, `wc`, `od`, `tail`, `head`, `sed -n` from the existing system.
Scratch confined to `/tmp/kasegi-r23-falsify-SnapGap/{,mut-pages/,mut-quote/,mut-14-4a/}`. Every
mutation above was applied to a copy under that scratch tree with the copy's manifest digest
recomputed; `corpus/source-snapshots/round-23/` was never written.

Durability: this report cites **no** path under any `.ufo/waves/*/scratch/` tree, and no finding
depends on the `/tmp` scratch tree surviving — each mutation is stated as the byte edit made,
the digest recomputation, the command, and its output lines, so a reader can replay it from the
production tree without the copies. At observation `03:43` the scratch tree held 16 files across
the three mutation directories; it is `/tmp` and therefore expected to be ephemeral.
