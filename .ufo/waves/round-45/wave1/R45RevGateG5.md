VERDICT: BROKEN

# R45RevGateG5 — C2 gate attack on G5 (`def g5`, corpus/instruments/r45-c2-gate.py:169-188)

Scope: read-only attack on G5 only. No commit, no git mutation, no shared file touched. Scratch (`/fast/scratch/hyaku/kasegi-r45/R45RevGateG5/`, TMPDIR explicit) removed on exit. Counter script sha256 `5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082`; pinned snapshot S071.txt sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` (matches manifest.json). Snapshot has 372 lines by `wc -l` and by Python `splitlines()`; 0 CR, 0 form-feed, 0 NUL, no U+2028/U+0085, so line numbers agree between grep, sed and G5.

## What G5 actually checks (code read)
- Span regex, corpus/instruments/r45-c2-gate.py:175: `“([^”]+)”\s*\(`?S071\.txt:(\d+)(?:-(\d+))?`?` — only a curly-quoted span immediately followed by `(` and `S071.txt:N[-M]` is examined. Anything else is dropped silently (no `failed` increment).
- Window, line 180: `norm(" ".join(snap[a-1:b]))`, unbounded width; no check that the cited range is tight.
- Substring test + word cap, line 182: `nq in window` and `len(nq.split()) <= 25` (per span, not per quote).
- Cores, lines 186-187: each core regex must match *some* passed span; `ok = failed==0 and len(passed)>=4 and cores==4`. Nothing checks prose outside spans, presence of stitch markers, or distinctness of spans.
- Docstring lines 7-8 say the gate exists so that "an entry that quotes text the source does not hold cannot satisfy" its limbs; G5 only enforces that for the one shape in line 175.

## Attack results (every row = a tree I built and ran; G5 line copied from stdout)

Driver: `python3 corpus/instruments/r45-c2-gate.py --root <tree>`; each tree = README F27 row + one knowledge entry + byte-copied S071.txt. Four verbatim cores were always included (verified against the snapshot: L1 310-311, L2 95-96, L3 39-40, L4 41-43). Fabricated text used: `Reporters have 48 hours to disclose AI-found bugs.` (not in S071; `grep -c` 0).

Controls (must behave):
- T0_do_nothing (empty tree): `gate G5 pass=0 read=F27-rows=0`
- T1_honest_control (4 correct cited spans): `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`
- T2_cited_fabricated_control (fabricated curly quote with canonical `(`S071.txt:95-96`)` shape): `gate G5 pass=0 read=spans=5 located=4 failed=1 cores=4/4`  — G5 does catch shape-correct fabrication.
- A7c_unsplit_control (66-word verbatim passage, one span): `gate G5 pass=0 read=spans=5 located=4 failed=1 cores=4/4`
- A8c_single_span_stitch_control (`“Binary-only executables are not accepted. If you resorted to AI assistance, you must treat it as public”`, cite 39-96): `gate G5 pass=0 read=spans=5 located=4 failed=1 cores=4/4`

Constructions that pass (defect present, G5 green):
- A1 straight-quote fabrication: body `"Reporters have 48 hours to disclose AI-found bugs." (`S071.txt:95-96`)` plus the 4 honest spans → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`. (Line 175 only matches curly quotes; the fabricated span is never seen.)
- A2 uncited curly fabrication: `“Reporters have 48 hours to disclose AI-found bugs.”` with no citation → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`. Contradicts the docstring purpose (lines 7-8).
- A3 non-canonical citation shape: `“Reporters have 48 hours to disclose AI-found bugs.” (see `S071.txt:95-96`)` → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4` (`(see ` breaks the `\(` `` `? `` S071 pattern).
- A4 guillemet fabrication: `«Reporters have 48 hours to disclose AI-found bugs.» (`S071.txt:95-96`)` → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`.
- A5 other-capture fabrication (attributed to the Google page): `“Reporters have 48 hours to disclose AI-found bugs.” (`S072.txt:1`)` → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4` (G5 never looks at S072).
- A6 mislocated / over-broad citation: honest spans with L2 cited `(`S071.txt:20-100`)` though the quote is at 95-96 → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`. Citation is wrong about where the text is; G5 only tests containment in a window.
- A7 over-long quote split into three chunks of 22 words, each cited `(`S071.txt:308-312`)` → `gate G5 pass=1 read=spans=7 located=7 failed=0 cores=4/4` (unsplit 66-word version fails: A7c above).
- A8 stitched by ellipsis: `“Binary-only executables are not accepted.” (`S071.txt:39-40`) … “you must treat it as public” (`S071.txt:95-96`)` presented as one sentence → `gate G5 pass=1 read=spans=6 located=6 failed=0 cores=4/4`.

Cheapest recipe (3 files, reproduced by hand in a fresh `mktemp -d` and printed in full):
```
corpus/README.md:  | F27 | Linux kernel security-bugs reporting process | admitted | `knowledge/linux-kernel-security-bugs.md` | S071 |
corpus/source-snapshots/round-45/S071.txt:  (cp of the pinned file)
corpus/knowledge/linux-kernel-security-bugs.md:
  “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (`S071.txt:310-311`)
  “If you resorted to AI assistance to identify a bug, you must treat it as public” (`S071.txt:95-96`)
  “Binary-only executables are not accepted.” (`S071.txt:39-40`)
  “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.” (`S071.txt:41-43`)
  “Reporters have 48 hours to disclose AI-found bugs.”
```
Printed:
```
gate G1 pass=0 read=rows=1 admitted=1 dup=0
gate G2 pass=0 read=source=0 verified-at=0 recheck=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4
gate G6 pass=0 read=knowledge=1
gate G7 pass=0 read=census-rc=2
c2-gate fixed=1/7 exit=1
```
Empty-tree control run in the same way printed `gate G5 pass=0 read=F27-rows=0`.

So the fabricated, uncited, non-canonically cited, guillemet and other-capture quotes (A1-A5), the widened citation (A6), the chunked over-long passage (A7) and the ellipsis stitch (A8) each turn G5 green while the entry contains text the source does not hold, cites it to the wrong place, or joins non-adjacent source text as one claim. Five-plus distinct constructions satisfied: A1, A2, A3, A4, A5, A6, A7, A8. The honest-control and fabricated-cited controls show G5 is discriminating only for the canonical shape.

Note: G5 green alone does not give `c2-gate fixed=7/7`; G1-G4, G6, G7 must also pass. I did not build a full 7/7 tree (not requested); the bypass is demonstrated at G5.

## False-RED on correct landings (G5 rejects; all printed)
- R1 anchor-style single-line citations (`(`S071.txt:310`)`, `:95`, `:39`, `:41`) → `gate G5 pass=0 read=spans=4 located=0 failed=4 cores=0/4`. Every correct quote here spans 2-3 lines (Q1 310-311, Q2 95-96, Q3 39-40, Q4 41-43), so a one-line cite fails. This is the same convention as the manifest's `anchor` field (manifest.json: 310, 95, 39, 41, 20). source-recheck.py:110-113 reads `anchor..anchor+3`, so G4-style anchors pass recheck while G5 rejects them: the two gates disagree on the same source.
- R2 repo-path citation (`(`corpus/source-snapshots/round-45/S071.txt:310-311`)`) → `gate G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`. The regex needs `(` directly before `S071`.
- R3 en-dash range (`S071.txt:310–311`) → `gate G5 pass=0 read=spans=4 located=0 failed=4 cores=0/4` (only ASCII `-` is parsed; en-dash drops the end line).
- R4 elided correct quote (`“for up to 7 calendar days … with an exceptional extension to 14 calendar days”`) → `gate G5 pass=0 read=spans=4 located=3 failed=1 cores=3/4`. Elision is a correct convention; it is rejected.
- R5 bracket-editorial correct quote (`“[T]he reporter …”`) → `gate G5 pass=0 read=spans=4 located=3 failed=1 cores=3/4`.
- By design, not tested: any verbatim quote over 25 words (e.g. the full 66-word paragraph) is RED even if exact (line 182).
- Passing as expected: verbatim mid-sentence fragments (`if an issue cannot be reproduced …`) → `gate G5 pass=1 read=spans=4 located=4 failed=0 cores=4/4`.

## Limitations
- Only the S071 snapshot in the lane was used; the lane's README has no F27 row yet (`grep '^| F2[5-7]' corpus/README.md` shows F25, F26 only), so I did not run G5 against a real landing.
- Did not run G1-G4, G6, G7 against the constructions beyond the printed lines; G7 uses `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (not invoked on lane content).
- Did not test the frozen controls file directly (not in my assignment).
- A6 "mislocation" is an over-broad citation range, not a wrong quote; it is labelled as such.
- Python `str.split()` / `re` behaviour on exotic Unicode whitespace was not exercised beyond the snapshot's actual bytes.
- Recommendation for the L1 (not applied by me): require the cited span's start and end lines to be tight (e.g. the quote must occur in `snap[a-1:b]` *and* not in `snap[a:b]` for a multi-line span), reject any curly/straight/guillemet quote-like span without a canonical citation, and count non-matching quote-like spans as failures.
