# RevF22Quotes — round-39 wave-2 falsify receipt (S057 quote pins)

Seat: RevF22Quotes, leaf attack seat (no subagents, no swarm). Item: re-derive the
four S057 quote pins directly from the committed capture
`corpus/source-snapshots/round-39/S057.txt` — locate each quote, count occurrences
(must be 1 for the pin region), confirm ≤25 words by whitespace split, confirm the
manifest's anchor lines point at them, list any discrepancy with the entry/row
citations, confirm the capture sha256 equals the manifest `snapshot_sha256`, and
confirm the live re-fetch (ScoutReopenS057) is byte-identical.

Read first, unmodified: `.ufo/waves/round-39/claims.json` and
`.ufo/waves/round-39/claims-erratum-1.md` (E1–E5 noted; E5's measurement semantics
do not touch quote pins). All attacked bytes read at lane HEAD `5006097`
("round-39: receipt Y (all-gates v3)"); tracked worktree clean at read time
(`git status --porcelain` → 0 modified/staged tracked files; only untracked wave-2
dispatch files). I authored none of the bytes under attack (capture, manifest,
entry, row, lesson are wave-1 seats' deliverables). Receipt only — no other lane
writes, no mutating git/jj anywhere, read-only git only.

## 1. Capture sha binding — PASS

```
$ sha256sum corpus/source-snapshots/round-39/S057.txt
11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f  S057.txt
$ wc -c -l -w corpus/source-snapshots/round-39/S057.txt
275 lines, 2483 words, 17971 bytes
```

manifest.json S057 record: `sha256` = `snapshot_sha256` =
`11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`,
`snapshot_bytes` = 17971, `lines` = 275 — all four match the committed bytes.
Supplementary: `python3 corpus/instruments/capture-binding-check.py` →
`MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0` …
`records=46 bound=46 unbound=0`, exit 0 — the record is url-bound and fetched.

## 2. Live re-fetch byte-identity — PASS (verified directly, not only transitively)

My fetch, `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, 2026-10-26T20:17:02Z:

```
pdf  http=200 bytes=235270 final=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
page http=200 bytes=54453 final=https://www.cisa.gov/resources-tools/resources/when-issue-vex-information
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  S057.pdf
4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d  S057-page.html
```

Raw PDF sha256 == manifest `raw_sha256`/`raw_bytes` (235270) ✓; landing-page sha ==
manifest `landing_page.raw_sha256`/`raw_bytes` (54453) ✓ — source unchanged since
the recorded 2026-10-26T19:30:55Z capture. Normalized through the lane's own
`capture-source.py pdf_to_text()` (scratch driver imports the module, no
reimplementation):

```
$ python3 normalize_pdf.py S057.pdf > S057.normalized.txt
$ cmp S057.normalized.txt <lane>/corpus/source-snapshots/round-39/S057.txt
cmp exit 0: BYTE-IDENTICAL   (sha256 11c8d6d6…)
```

ScoutReopenS057's chain, closed: their normalized re-fetch sha256 `11c8d6d6…` ==
committed capture sha; their cmp target
`.ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt` is byte-identical to the
committed capture (my `cmp` exit 0, same sha); their deliverable
`wave1/ScoutReopenS057.reopen.txt` hashes to `278e76d6…` as their receipt records.
Their own l1_note asked for exactly this re-check against the landed file — done,
and upgraded to a direct fetch+normalize+cmp.

## 3. The four pins re-derived (independent script; whitespace-join semantics)

Method: capture lines joined with single spaces keeping a char→line map; each
manifest quote whitespace-collapsed and searched; occurrences counted over the
whole capture and over the manifest-declared L-range; occurrence span lines
compared to the declared range; start line compared to `anchor`; word count =
whitespace split. Script + raw output in scratch (removed at yield); results:

| pin | anchor | actual span | declared | occ full | occ region | words | ≤25 | verdict |
|---|---|---|---|---|---|---|---|---|
| Q1 | 12 | L12–L14 | L12–L14 | 1 | 1 | 25 | yes | PASS |
| Q2 | 132 | L132–L134 | L132–L134 | 1 | 1 | 22 | yes | PASS |
| Q3 | 136 | L136–L138 | L136–L138 | 1 | 1 | **42** | **no** | **FAIL words** |
| Q4 | 184 | L184–L186 | L184–L186 | 1 | 1 | **34** | **no** | **FAIL words** |

Every pin is verbatim under whitespace collapse, occurs exactly once in the whole
capture AND exactly once inside its declared pin region, its span lines equal the
declared range exactly, and the quote **starts on its anchor line** — stricter than
the lane instrument, whose `anchor_verdict` only requires the quote inside
`[anchor, anchor+3]` (`source-recheck.py:100-104`). Location sub-claims verified:
L12 closes with `Whether,`; L131 is the `Status changes` heading; L134–L135 carry
the `for example, noting that the product is` continuation; L179–L181 carry
`Software supply chain considerations` + `Status inheritance`; L189 carries both
`component_not_present` and `vulnerable_code_not_present`. Lane instrument
agreement: `python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-39/manifest.json --source S057` →
`S057:sha256 OK` + four `S057:Q<n> OK normalized=markup-whitespace occurrences=1
anchor=N-ok` lines, exit 0.

## 4. Entry citations (corpus/knowledge/cisa-when-to-issue-vex.md) — PASS

The entry tiles all four pin regions with 10 verbatim spans; every one is ≤25
words, occurs, and its declared range intersects its occurrence (script-verified):
Claim1a 25w L12-14; Claim1b 20w L79-81; Claim3a 13w L132-133; Claim3b 19w L134-135;
Claim4a 16w L136-137; Claim4b 22w L137-138; Claim6a 15w L183-184; Claim6b 20w
L184-185; Claim6c 14w L185-186; Claim6d 18w L189-191. The entry header's line refs
for the pin regions (business-decision L12-14, lifecycle L132-135, reaffirmation
L136-138, caution L183-186, allowance L187-191) all point at the claimed content.
The entry satisfies QUALITY Q3 by splitting; its FC-1 `words_max=25` holds for the
pin-region subset re-derived here (10 of its 22 spans — the other 12 spans are
outside this item's four-pin scope and were not exercised).

## 5. Row citations (corpus/SOURCES.md:62) — PASS with imprecision

Capture-line refs all verified against the capture: L12-14, L79-81, L132-138,
L184-191 point at the claimed content. The `pdftotext -layout` refs were
re-derived from my fresh fetch of the recorded PDF (§2), `pdftotext -layout`:
L205-213 is exact for lifecycle+reaffirmation (content L205-212); but **L19-20
misses the first business-decision sentence's first word** (`Whether,` sits on
layout L18); **L129 is the middle line** of the L128-130 sentence; **L287-294
starts mid-caution** (the sentence head "VEX consumers should carefully evaluate…"
is on L285-286) **and ends before the allowance's last word** (`downstream.` on
L295). All point inside the cited content; none is a full-span pointer. Also the
row's `inheritance caution (L184-191)` starts one line after the entry's
caution-sentence start (L183) — consistent with the manifest pin (anchor 184) but
divergent from the entry.

## 6. Findings

**D1 (medium) — manifest Q3/Q4 pin fields exceed the ≤25-word quote bound: 42 and
34 words.** Evidence: §3 table (script `check_pins.py`, whitespace split). This
fails the item-specified ≤25-word check for 2 of the 4 pins. Corroboration:
(a) the round-39 lesson Gate `corpus/lessons/round-39.md:24-27` asserts
"**Quotes (each ≤25 words, located in the capture):**" and lists Q3 `:136-138` and
Q4 `:183-186` — the very regions the manifest pins occupy — and the pins living
there are 42/34 words, so under the pin reading the lesson's assertion is false;
(b) lane convention: every manifest quote pin from r30 through r38 is ≤25 words
(per-record max: r30 14, r31 23, r32 13, r34 20, r35 19, r36 25, r37 17, r38 25);
the only prior over-25 pins are r23 S029 (26, 37) and r29 S044 (35) — r39 is the
first manifest since r30 to break the bound; (c) no instrument enforces the bound
on manifest pins: `source-recheck.py` carries `MIN_QUOTE_CHARS = 12` (a floor
only) and checks sha/occurrences/anchor-window, so the over-long pins pass
silently (§3 instrument run, exit 0). Materiality is contained: the pins are
verbatim, unique, correctly anchored, and the entry's own quotes all comply (§4);
the defect is the over-long manifest pin fields plus the lesson's
false-under-the-pin-reading "each ≤25 words". Repair (not mine to execute): split
manifest Q3/Q4 the way the entry already splits them (Q3 → L136-137 + L137-138;
Q4 → L184-185 + L185-186), or append an R9-class erratum to the lesson scoping the
"each ≤25 words" claim — never a silent rewrite.

**D2 (low) — lesson Gate Q-labels collide with the manifest's pin ids.**
`corpus/lessons/round-39.md:24-27` lists "Q2 `:79-81`" (the strict-protocol
quote) — the manifest's Q2 is anchor 132 (under_investigation lifecycle,
L132-134) and the manifest has no pin at L79-81; lesson Q4 `:183-186` vs manifest
Q4 anchor 184 (L184-186). A reader cross-referencing "Q2" from the lesson to the
manifest lands on the wrong quote. The Gate's Q3/Q4 entries also carry
location+description only (no verbatim quote text), so the "each ≤25 words"
heading is unverifiable from the Gate block alone for those two. Every line range
the lesson cites does contain the described content (verified §3/§5), so this is a
citation-hygiene defect, not a fabrication.

**D3 (minor) — row layout-citation imprecision** (§5): layout L19-20 / L129 /
L287-294 are inside-the-content pointers rather than exact spans; the row's
capture-line refs are exact.

**No kill-rule trigger.** claims.json C2's predicate and kill rule bind row
counts, NF=13, harness/binding/audit/census counters, junk rejection, and
"capture or manifest absent or unbound" — the capture and manifest are present,
sha-bound (§1), url-bound and fetched (capture-binding-check exit 0), so C2 stands
as frozen. The ≤25-word pin bound is not a frozen C2 predicate: it lives in
QUALITY Q3 (entries — satisfied, §4) and in the lesson Gate's prose (falsified
under the pin reading, D1). C1 is untouched by this item.

## 7. Method notes

- Scratch: `/fast/scratch/hyaku/kasegi-r39/RevF22Quotes/` (check_pins.py,
  normalize_pdf.py, fetched PDF/page bytes, normalized + layout texts); removed
  before yield; nothing written outside scratch and this receipt.
- No tools installed: `pdftotext` pre-existing at `/usr/bin/pdftotext`; no
  pacman/uv/npx/cargo installs, no config edits, no service restarts.
- Network: two GETs, 2026-10-26T20:17:02Z, UA `kasegi-shokunin/1.0`, HTTP 200
  both, 235270 + 54453 bytes (§2).
- Wave-2 dir already held `swarm-registry.json` (not mine); this receipt is the
  only file I add there.
