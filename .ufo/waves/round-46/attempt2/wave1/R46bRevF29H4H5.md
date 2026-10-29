VERDICT: HOLDS

Seat R46bRevF29H4H5 — attack on `corpus/instruments/r46-f29-gate.py` limbs H4+H5 only, round 46
attempt 2. All trees were built in scratch
(`/fast/scratch/hyaku/kasegi-r46/R46bRevF29H4H5/`, removed after the run) from read-only
`git archive` exports of the freeze commit fe0f56b (corpus) and base 04af9bc9, plus the L1's own
committed fixture harness `.ufo/waves/round-46/attempt2/controls/f29-fixture.py`. Receipts for
every command below are committed in `R46bRevF29H4H5.draft/` beside this report. No tools were
installed or upgraded (stdlib only, no installs needed).

## Do-nothing controls (calibration)

- `$ python3 <freeze>/corpus/instruments/r46-f29-gate.py --root <base export 04af9bc9>`
  printed `f29-gate fixed=1/7 exit=1` (H7 only) — matches the frozen before-value
  (`controls/f29-gate-at-base.txt`, `claims.json` C2 expect_before). Receipt: `receipts-E1-controls.txt` E1a.
- Same command on the freeze export printed `f29-gate fixed=2/7 exit=1` with
  `gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0` — matches the frozen
  freeze-tree reading in `claims.json`. Receipt E1b.
- Positive fixture tree (the L1's `f29-fixture.py --mode positive`) printed
  `f29-gate fixed=7/7 exit=0` (all seven limbs green). Receipt E1c. Junk and fabricated
  fixture modes both printed `fixed=6/7 exit=1` with H5 red (`junk`: `spans=7 located=2 failed=5
  uncited=0 cores=0/5`; `fabricated`: `spans=7 located=5 failed=2 uncited=0 cores=4/5`). Receipts E1d/E1e.
  None of the three named kill-rule controls (do-nothing base, junk, fabricated) grades 7/7.

## Findings (severity order)

### F1 — LOW (residual seam, H5): a quotation stitched across a paragraph boundary locates and grades 7/7

Thing attacked: H5 located-ness is normalized-substring containment in the cited window
(`h5`, r46-f29-gate.py ~lines 315-324: `window = norm(" ".join(snap[max(a - 1, 0):b]))` …
`nq in window`), so a "quote" formed by joining the tail of snapshot line 25 with the head of
line 26 — two verbatim sentences from two different paragraphs — is indistinguishable from a
continuous quote.

Tree `att3` = positive tree + one extra cited span in the Limits section:
“Anyone with admin permissions to a security advisory can request a CVE identification number.
If you already have a CVE you want to use” (`S074.txt:25-26`) — 24 words, span 25-26.

Command: `python3 <freeze>/r46-f29-gate.py --root att3`
Output (quoted): `gate H5 pass=1 read=spans=8 located=8 failed=0 uncited=0 cores=5/5` and
`f29-gate fixed=7/7 exit=0`. Receipt: `receipts-E2-E7-attacks.txt` att3.

Mitigations that keep this LOW: the 25-word cap (my first 26-word stitch was rejected,
`failed=1` — observed before trimming) and the 12-line span cap bound it; both stitched halves
are verbatim held text, so the gate's stated contract ("an entry quoting text the source does
not hold cannot satisfy") is not violated; and norm() strips markup symmetrically, so I could
not construct any non-held text that locates. No false claim can be smuggled, only a
presentation-level stitch of held sentences.

### F2 — LOW (residual seam, H5): a frozen core quoted inside a mid-line HTML comment counts as "live text" — 7/7

Thing attacked: `live_lines` (r46-f29-gate.py ~lines 104-114) drops only whole lines that
start with `<!--`; fences and line-leading comments are stripped, a comment mid-line is not.

- `att4` (core-2 span “Privately collaborate to fix the vulnerability in a temporary private
  fork.” moved into a fenced block): `gate H5 pass=0 … cores=4/5` — correctly red.
- `att5a` (same span on a line starting with `<!--`): `gate H5 pass=0 … cores=4/5` — correctly red.
- `att5b` (same span inside a MID-LINE `Note: <!-- … --> (verified).` line): printed
  `gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5` and
  `f29-gate fixed=7/7 exit=0`. Receipts att4/att5a/att5b.

Severity LOW: the span is still located and verbatim-held; the core is present in the raw
markdown (visible to anyone reading the entry source, invisible only in rendered HTML). This is
the "CORES matched inside note fields" recipe — it reads GREEN for mid-line note fields,
RED for fences and line-leading comments. Not one of the claim's named kill-rule controls.

### F3 — LOW (residual seam, H5): citation ranges are not tight — a quote cited 3 lines above its true line locates; 7/7

Thing attacked: same containment check as F1. `att7` = positive tree with G4's cite padded from
`S074.txt:25` to `S074.txt:22-25` (the quoted text sits on line 25 only; the 22-25 window is a
superset). Command: `python3 r46-f29-gate.py --root att7`.
Output: `gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5`,
`f29-gate fixed=7/7 exit=0`. Receipt att7. Bounded by the 12-line span budget (R50 defect
"widespan" 1-42 is caught by `b - a <= 11`; the H5a mutant flipped that defect red).

### F4 — RECIPE RESISTS (H4): a snapshot whose sha matches but whose quotes moved lines cannot be built — sha pin closes the class

Thing attacked: the "anchor tolerance abuse" half of recipe 1. `att1` = positive tree with
snapshot lines 13 and 40 swapped (the "temporary private fork" sentence moved off line 13;
42 lines kept). Command: `python3 r46-f29-gate.py --root att1`. Output:
`gate H3 pass=0 read=snapshot-not-the-pinned-capture`,
`gate H4 pass=0 read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0`,
`gate H5 pass=0 read=spans=7 located=6 failed=1 uncited=0 cores=4/5`,
`f29-gate fixed=4/7 exit=1`. Direct recheck:
`S074:sha256 MISMATCH expected=1296528d…c278039 actual=94ead00e…ff5a2`. Receipt E2.
Any snapshot edit breaks the manifest-recorded sha before recheck's 4-line anchor window
(`source-recheck.py` `anchor_verdict`, window = lines anchor..anchor+3) is ever reachable at
gate level. H5 independently red: the moved quote fell out of its cited window.

### F5 — RECIPE RESISTS at gate level (defect disclosed at the recheck layer): anchor tolerance exists in source-recheck but is neutralized by H4's manifest pin

Direct recheck probes (manifest + pinned snapshot in scratch):
- `probeA` — quote truly on line 13, anchor declared 10 (3 high; window covers lines 10-13):
  `S074:Q1 OK occurrences=1 anchor=10-ok`, exit 0. Receipt E4 probeA.
- `probeB` — unique quote, anchor declared 4 (outside any window):
  `S074:Q1 OK occurrences=1 anchor=4-BROKEN`, exit 0 — recheck still prints OK for a
  definitively wrong anchor when the quote is unique. Receipt E4 probeB.

Gate consequence, tested with the real gate code (importlib, manifest pin monkey-satisfied so
the quote logic past the pin is exercised): `h4(anchor+3 manifest)` returned
`pass=0 read=recheck-rc=0 quotes-ok=1 frozen-cores-missing=0` — the OK line WAS counted
(`quotes-ok=1`), so the tolerance would feed `oks`, but the `oks >= 8` floor and the
frozen-cores floor reject a 1-quote manifest; and any `*-BROKEN` note trips h4's
`"BROKEN" not in out` guard (probeB). On the actual pinned manifest all nine anchors hold
exactly (verified line-by-line against the capture: Q1@10, Q2@13, Q3@17, Q4@24, Q5@25, Q6@25,
Q7@26, Q8@31, Q9@38). Receipts `receipts-E3b-E4b-clauses.txt`, `evidence-snapshot-boundary-lines.txt`.

### F6 — RECIPE RESISTS (H4): a manifest with 8 identical quotes is rejected twice

`att2` = positive tree with the manifest replaced by one whose S074 record keeps the pinned
snapshot sha but carries 8 identical quotes
("GitHub usually reviews the request within 72 hours." x8, anchor 25 each). Gate:
`gate H4 pass=0 read=manifest-not-the-pinned-bytes`, `f29-gate fixed=6/7 exit=1`. Receipt E3.
The raw recheck on the same fabricated manifest prints
`S074:sha256 OK` + `S074:Q1..Q8 OK occurrences=1 anchor=25-ok`, exit 0 — the recheck layer
alone is fooled (it counts source occurrences, not manifest distinctness). Layer 2 (h4's
distinctness clause, computed with the real gate code on the fabricated manifest):
`distinct=False set=1 qs=8`. Receipts E3/E3b. The manifest-byte pin (h4,
r46-f29-gate.py ~lines 283-285) plus the distinct clause close the recipe.

### F7 — RECIPE RESISTS (H4): CORES matched inside manifest note fields do not count

h4 builds its core haystack only from `q["quote"]` fields
(`mt = norm(" ".join(q["quote"] for q in qs))`, r46-f29-gate.py ~line 295); a "note" field on a
quote record is never read. Verified with the real gate code on the att2 fabricated manifest
(cores missing=4 with only decoy quote text) and by code reading; additionally the manifest-byte
pin makes any such edit red at H4 before the clause is reached. Receipt `receipts-E3b-E4b-clauses.txt`.

### F8 — INFO for L1: the R50 receipt's junk/fabricated fixed totals do not reproduce at the freeze export

`controls/f29-r50-receipt.txt` states junk/fabricated trees grade `fixed=3/7` with "H2/H5 red".
Re-running the committed fixture against the freeze export today gives `fixed=6/7 exit=1` for
both (H2 green in both), while the H5 limb readings reproduce exactly: junk
`located=2 … cores=0/5` (receipt: "2/7 quotes located, 0/5 cores"), fabricated
`located=5 … cores=4/5` (receipt: "5/7 located, 4/5 cores"). The security-relevant limb
readings match; the older fixed totals and the "H2 red" note look stale relative to the
committed fixture. No gate or fixture edit is proposed from this seat (read-only); flagged for
L1 adjudication. Receipts E1d/E1e.

## Limitations

- The honest 7/7 baseline is the L1's own fixture entry (`f29-fixture.py --mode positive`), not
  the wave's final landing entry; the wave's entry may quote differently, but every H4/H5
  attack here is a single-mutation delta off that baseline, and the do-nothing base/freeze
  controls reproduce the frozen receipts exactly, so the discriminations stand.
- Only H4/H5 were in scope; H1/H2/H3/H6/H7 went green in the attack trees as a side effect of
  reusing the positive fixture and are reported only as readings.
- Live-target testing is refused by the lane rules; all located-ness claims are against the
  pinned capture S074.txt only.
- The pin-lifted h4 computation in F5 used the committed gate code with `PINS["manifest.json"]`
  monkey-patched in memory; no file was modified. It isolates the layer behavior; the shipped
  gate always applies the real pin first.
- Scratch directory `/fast/scratch/hyaku/kasegi-r46/R46bRevF29H4H5/` was removed after receipts
  were copied into this draft directory. No commit, push, or git/jj mutation was performed
  anywhere; the lane repo was touched only to create this report and the draft receipts.
