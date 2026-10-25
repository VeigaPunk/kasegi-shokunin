# S030 quote assertions — falsification report (seat L1Kasegi23.S030Quotes-2)

Date: 2026-10-25. Mode: read-only attack on landed working-tree bytes. Repo root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (all paths below relative to it).
No repo file was modified; the only writes were `/tmp/kasegi-r23-falsify-S030Quotes-2/*`
and this report. No package installs (python3, grep/awk/sha256sum, and the already-present
`curl` + poppler `pdftotext` were used).

## Subject bytes measured

| object | sha256 | size | mtime |
|---|---|---|---|
| `corpus/source-snapshots/round-23/S030.txt` | `673526db…c5ab019` | 26660 | 2026-10-20 18:38 |
| `corpus/source-snapshots/round-23/manifest.json` | (not hashed by manifest) | 3541 | 2026-10-25 03:30 |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | `44016013b6b0c6053a4f2a22add62dfef0a3b1e5cd3fe36b11cf5f5e3d5221c4` | 4691 | 2026-10-25 03:39 |

Snapshot digest equals the manifest's `sha256` for S030. Replay:

```
$ python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-23/manifest.json --source S030
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
exit=0
```

## F1 — Manifest assertions: 7/7 exact substrings, one occurrence each (HIGH confidence, survives)

`manifest.json` L32 `"id": "S030"`, assertion rows L36–L42. Method: byte substring
`quote in open(S030.txt,'rb').read().decode('utf-8')` (UTF-8, exact bytes).

| manifest line | assertion id | exact? | S030.txt line(s) | len |
|---|---|---|---|---|
| 36 | rule-3-1-1-scope-definition | **yes** | 64 | 66 |
| 37 | rule-3-1-4-covered-products | **yes** | 73 | 101 |
| 38 | rule-4-1-2-security-impact | **yes** | 147 | 109 |
| 39 | rule-4-1-9-independently-fixable | **yes** (with markup, see F2) | 165 | 82 |
| 40 | rule-4-2-1-1-first-opportunity | **yes** | 179 | 100 |
| 41 | rule-4-2-11-separate-ids | **yes** | 211 | 89 |
| 42 | rule-4-2-12-uncertainty | **yes** | 212 | 111 |

No assertion occurs twice in the excerpt; each hit is a single line. Manifest L3 states
the ceiling correctly: the instrument asserts containment only, and quote-to-location
binding is human-verified and not machine-checked.

## F2 — Entry quote rows: 6/7 byte-literal; the single divergence is disclosed (HIGH confidence)

`corpus/knowledge/cna-assignment-and-vulnerability-rules.md` rows L25–L31 (table header L23
claims "Exact quote (at most 25 words)"; max observed 20 words, so the limit holds).

| entry line | rule | page claim | literal substring of excerpt? | in upstream PDF (ws-normalised)? |
|---|---|---|---|---|
| 25 | 3.1.1 | 7 | **yes** | yes |
| 26 | 3.1.4 | 7 | **yes** | yes |
| 27 | 4.1.2 | 11 | **yes** | yes |
| 28 | 4.1.9 | 12 | **NO** — excerpt has `<u>Independently Fixable</u>` | yes |
| 29 | 4.2.1.1 | 13 | **yes** | yes |
| 30 | 4.2.11 | 15 | **yes** | yes |
| 31 | 4.2.12 | 15 | **yes** | yes |

Exactly one rendered quote differs from the excerpt bytes: row L28 drops the capture's
`<u>`/`</u>` underline markup present at `S030.txt:165`
(`…the Vulnerabilities are <u>Independently Fixable</u>.`). The outer `“…”` in the table
are the entry's own typographic delimiters and are not part of the quoted text; no other
byte-level difference exists (no NBSP, no differing punctuation, no reflow inside any cell).

**Disclosure:** entry L39–L42 ("Quote-fidelity note") states the difference, reproduces the
differing bytes (`are <u>Independently Fixable</u>.` — verified as an exact substring of
`S030.txt:165`), says the table quotes rendered text, and says the manifest/recheck compare
literal excerpt bytes. All three claims are true:

- `corpus/instruments/source-recheck.py:129` is `if assertion["quote"] in source_text:`
  with `source_text` read from the snapshot (`:120`); the instrument never reads the
  knowledge entry. So "which is what the recheck compares" is exactly right.
- Synthetic replay in `/tmp/kasegi-r23-falsify-S030Quotes-2/` (copy of `S030.txt` + a
  manifest whose 4.1.9 assertion was replaced by the entry's rendered text):

```
$ python3 corpus/instruments/source-recheck.py --manifest manifest.json --source S030
…
S030:rule-4-1-9-independently-fixable MISMATCH reason=quote-not-found
exit=1
```

  i.e. the parenthetical is load-bearing, not cosmetic: quoting only the rendered form in
  the manifest would fail closed.

- Supplementary fidelity check (beyond the assigned question): all seven rendered entry
  quotes are exact substrings of the **upstream PDF** text after whitespace normalisation
  (`curl` → `/tmp/S030.pdf`, `pdfinfo`: 27 pages, title "… Version 4.2.0";
  `pdftotext` → `/tmp/S030-pdf.txt`). The rendered form is therefore faithful to the
  document; the `<u>` is purely a markit conversion artifact (the PDF contains no `<u>`).

Nit only: L39 calls `<u>` "emphasis"; it is underline markup. The example itself is
byte-exact, so this does not misdescribe the difference.

## F3 — Two of seven page attributions are not verifiable from the pinned excerpt (HIGH confidence on the gap; entry is nonetheless correct upstream)

`S030.txt` page markers are `1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17`
(lines 8, 20, 76, 95, 112, 134, 155, 168, 186, 209, 227, 242); pages 3–7 are absent.
Therefore the section-3 text (lines 57–75) carries no page marker of its own: it falls under
`<!-- Page 2 -->` (L20) and the next marker is `<!-- Page 8 -->` (L76). Checks:

- rows L25/L26 claim "page 7", but nothing in the pinned bytes assigns page 7 to 3.1.1/3.1.4;
  they are only bounded above by the page-8 marker.
- upstream PDF (fetched 2026-10-25) puts both on page 7 — so the entry is **correct**, and
  the gap is in the capture, not the entry.
- the other five page claims are reproducible from the markers: 4.1.2→11 (L147 after marker
  L134), 4.1.9→12 (L165 after L155), 4.2.1.1→13 (L179 after L168), 4.2.11/4.2.12→15
  (L211/212 after L209). All five match the PDF.

Assessment: not a false claim, but a disclosure gap local to the entry — the entry's only
offered mechanical check (frontmatter L4 recheck) verifies quote containment, never pages,
and the entry does not say that two of its page numbers depend on bytes the pinned excerpt
does not contain. `manifest.json:3` does disclose the general ceiling ("quote-to-location
binding is human-verified and is not machine-checked"), which partly covers this at the
manifest level; the entry does not repeat it.

## F4 — Falsified page claim: "section 3.2.4.2, pages 9–10" (HIGH confidence)

Entry L33 says `Version 4.2.0 section 3.2.4.2, pages 9–10`. The rule is wholly on page 9:

- excerpt: `3.2.4.2 …` is L110, and the `<!-- Page 10 -->` marker is L112; nothing of
  3.2.4.2 follows the marker.
- upstream PDF: page 9 ends with the rule's final sentence
  (`…assign directly if the requester is a CNA with appropriate scope.` then the page
  footer `CNA Operational Rules 4.2.0 9`); page 10 begins directly with `3.2.4.3`.

So the two-page span overstates by one page. Low impact (prose, not a quoted rule; the
seven quoted rows are unaffected) but it is an undisclosed page error in the target file,
failing against both the pinned excerpt and the PDF.

## F5 — Adjacent verifiable claims in the same entry that hold (HIGH confidence)

| entry line | claim | evidence |
|---|---|---|
| L14 | 4.2.0 current; approved 2026-08-20; effective 2026-08-25 | `S030.txt:12,14,16` (`#### Version: 4.2.0`, `#### Approved date: 2026-August-20`, `#### Effective date: 2026-August-25`) |
| L17 | independently-fixable guidance moved 4.1.10 (4.1.0) → 4.1.9 (4.2.0) | `S030.txt:165` is 4.1.9 and contains it; fetched 4.1.0 PDF has the identical sentence at 4.1.10, page 12 |
| L48 | 4.1.10 uses the integer-overflow→buffer-overflow case as one vulnerability | `S030.txt:166` |
| L56 | 4.1.11: updating dependencies is not a vulnerability | `S030.txt:170` |
| L57 | 4.2.7 distinguishes vulnerabilities from fixes | `S030.txt:204` |
| L57 | 4.2.13(1): not more than one ID when products share vulnerable code | `S030.txt:213` (rule) / `:214` (item 1) |

## F6 — "S022 preserves the earlier 4.1.0 source" is not byte-verifiable (HIGH confidence on absence, MEDIUM on intent)

Entry L14. `corpus/SOURCES.md:28` records S022 as the 4.1.0 URL with status `queued` and
artifact path `—`; `find . -iname "*S022*"` returns nothing, and no file under
`corpus/source-snapshots/` contains 4.1.0 bytes (only `round-23/` exists, with S018/S029/S030).
The only 4.1.0 artifact is a single quoted row at `corpus/lessons/round-22.md:98`.
If "preserves" is read as preserving source bytes locally, the claim is false; if it means
"the registry row keeps the superseded source identified", it is unverifiable and
untestable by the entry's own recheck (which selects S030 only). Worth tightening, because
the entry's rule text depends on not confusing the two versions.

## Mid-run working-tree change (recorded, not a defect)

The entry changed during this seat's run: size 4639 → 4691 bytes (+52), mtime
`2026-10-25 03:39:18`. The +52 delta equals exactly `len("cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ")`,
and the only observed change is frontmatter L4 gaining that `cd` prefix. Quote rows
(L25–L31), the 3.2.4.2 prose (L33) and the disclosure (L39–L42) are byte-identical and at
unchanged line numbers. Every check above was re-run on the current sha
`44016013…5221c4`; none of the findings depends on the pre-change bytes.

## Verdict on the assigned question

- Seven manifest assertions: all exact substrings of the pinned excerpt (L64, 73, 147, 165,
  179, 211, 212); digest matches; recheck 8/8 OK.
- Seven entry quote rows: one byte-level divergence from the excerpt (4.1.9, underline
  markup) and it is disclosed at L39–L42 with byte-accurate reproduction; the disclosure's
  mechanism claim is confirmed by instrument source and by a failing /tmp replay.
- Residual defects found outside the quote axis: the 3.2.4.2 "pages 9–10" span is wrong
  (page 9 only), the page-7 attribution for 3.1.1/3.1.4 is not reproducible from the pinned
  excerpt (correct upstream), and the S022 "preserves" provenance claim has no bytes behind it.

## Scope limits

- The pinned excerpt is curated, not the full document: markers present are pages 1, 2 and
  8–17; pages 3–6 and 18–27 are absent. No claim about content outside the captured pages
  is tested here.
- Upstream PDFs (`CNA_Rules_v4.2.0.pdf`, `CNA_Rules_v4.1.0.pdf`) were fetched once on
  2026-10-25 from the public `cve.org` URLs for page/rule-numbering cross-checks only
  (public documentation read). This says nothing about freshness after that date, and the
  recheck still proves captured bytes only.
- I exercised the recheck's pass path and one synthetic MISMATCH on the rendered form. I did
  not test digest-mismatch/fail-closed semantics (other seats: BaselineFalsify, ControlsRerun).
- No score or admission claim is made.
