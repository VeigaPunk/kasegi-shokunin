# R45W2CritKillC2v11 — C2 re-falsification of counter v1.1 (export of 6662a4276b6f7bd61e23e12058414e09dd71b9e4)

VERDICT: BROKEN

Scope: C2 only (frontier F27 / S071 / knowledge entry / r45-c2-gate.py v1.1). Export made with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>`; the lane working tree was not read or written. Nothing committed, nothing mutated in git, no fleet-root file touched, no install. Scratch removed on exit.

Summary: the integrated tree does reach `c2-gate fixed=7/7 exit=0`, and the coverage is real (F27 is a topic absent from the base). But the v1.1 counter is a presence-and-count instrument, not a support checker. I reached 7/7 with (i) straight-quoted fabricated text, (ii) an inverted claim behind a wrong cross-reference, (iii) a frontier row whose topic is unrelated, (iv) an emptied Limits section, (v) uncited contradictions, and (vi) a tree-supplied source-recheck stub. Only one class of probe (a fabricated curly-quoted span) is caught.

## F1 — the shipped tree meets the numeric claim (re-run)

Command: `python3 corpus/instruments/r45-c2-gate.py --root <export>`
Output (verbatim):
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=13 xrefs=5/5
gate G3 pass=1 read=row-S071=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=24 located=24 failed=0 uncited=0 cores=4/4
gate G6 pass=1 read=knowledge=64 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```
Do-nothing control (base dc5bb8c6 exported, graded by the same v1.1 counter): `c2-gate fixed=1/7 exit=1` (G1 `rows=26 admitted=26`, G6 `knowledge=63 ... entry-bytes-ok=0`, G7 the only pass). Matches the frozen controls file line for do-nothing-base.
Coverage check: `grep -rliE 'security-bugs|linux kernel|kernel\.org' corpus/knowledge corpus/SOURCES.md corpus/README.md` on base → no output, rc=1. On export → the three landed files (knowledge entry, SOURCES.md, README.md). So the topic is new to the corpus.
Secondary: `r44-frontier-count.py --root <export> --expect 27` → `frontier rows=27 admitted=27`, rc=0.
Cross-references I checked by hand are accurate: F02 `coordinated-disclosure-timelines.md:7-17` (Rule), `:22` (CERT/CC 45 days), `:24-25` (Project Zero 30/14); F04 `ai-assisted-finding-validation.md:7-8,15`; F15 `vendor-third-party-finding-coordination.md:91-96` and `corpus/README.md:309`. Every curly quote I checked against `corpus/source-snapshots/round-45/S071.txt` at its cited lines is present. The capture sha256 `0918dcfa…346f40` and the manifest pin `125339d9…f459` match the counter's PINS.

So the claim as numerically written holds for this tree. The falsification below is about what the 7/7 does and does not certify.

## F2 — the counter reaches 7/7 on landings that the claim text rejects

Method: copies of the export in scratch, one edit per mutant, graded by the export's own `r45-c2-gate.py --root <copy>`. Each edit described exactly; the printed last line is quoted. Full gate lines were captured; only the summaries are repeated here.

| id | edit to the shipped entry / tree | printed result |
|---|---|---|
| M0 | none (control) | `c2-gate fixed=7/7 exit=0` |
| M1 | appended `“The kernel security team pays 10000 dollars for each accepted report” (`S071.txt:300`).` (curly) | `G5 pass=0 read=spans=25 located=24 failed=1 …`; `c2-gate fixed=6/7 exit=1` |
| M2 | same sentence, straight quotes `"…"` | `G5 pass=1 read=spans=24 located=24 failed=0 uncited=0 cores=4/4`; `c2-gate fixed=7/7 exit=0` |
| M3 | F04 cross-reference changed to `ai-assisted-finding-validation.md:1` and claim changed from "stays a candidate until reproduction and an independent reviewer" to "is confirmed once a reproducer has run once" (F04 line 7 says the opposite) | `G2 … xrefs=5/5`; `c2-gate fixed=7/7 exit=0` |
| M4 | appended "The page permits a 21-day kernel embargo: “for up to 7 calendar days from the start of the release process” (`S071.txt:1-372`)." | `G5 pass=1 read=spans=25 located=25 …`; `c2-gate fixed=7/7 exit=0` |
| M5 | README F27 row rewritten to "Bug bounty payout tables for an unrelated vendor" (entry path unchanged) | `G1 pass=1 read=rows=27 admitted=27 …`; `c2-gate fixed=7/7 exit=0` |
| M6 | inserted 3 sentences of uncited generic prose and 8 three-column filler rows before `## Limits` | `G2 … table-rows=23 …`; `c2-gate fixed=7/7 exit=0` |
| M7 | stripped curly marks from every span except the four cores (4 curly spans left); appended uncited "The clock starts at the report date…" | `G5 pass=1 read=spans=4 located=4 failed=0 uncited=0 cores=4/4`; `c2-gate fixed=7/7 exit=0` |
| M8 | deleted the body of `## Limits`, kept the header | `G2 pass=1 read=sections=4/4 …`; `c2-gate fixed=7/7 exit=0` |
| M9 | appended two cross-references to line 1 of F02 and F04 | `G2 … xrefs=7/7`; `c2-gate fixed=7/7 exit=0` |
| M10 | `corpus/instruments/source-recheck.py` in the tree replaced by a stub printing `S071:sha256 OK` and `S071:Q1..Q5 OK`, exit 0 | `G4 pass=1 read=recheck-rc=0 quotes-ok=5 …`; `c2-gate fixed=7/7 exit=0` |
| M11 | combined: M3 + M5 + M7 + M8 + M2 + uncited contradiction | `G5 … spans=4 located=4 …`; `c2-gate fixed=7/7 exit=0` |

Mechanisms, from the counter source (`corpus/instruments/r45-c2-gate.py`):
- G5 regex is `“([^”]+)”` only (line 244); straight quotes are never seen. Verified by M2.
- G5 requires at least four located spans and the four cores; it never requires that a claim sentence be a span (M7, M11).
- G5 window is `snap[a-1:b]` with no width cap; a citation `S071.txt:1-372` locates any snapshot sentence (M4).
- G2 checks only that the first number after `corpus/knowledge/…md:` is within file length (line 186-189); it does not check that the cited line supports the sentence, and it does not check the span of `-N` (M3, M9).
- G2 checks that `## Limits` header exists, not its body (M8). Table rows are counted only by a three-cell pattern (line 183), so filler rows count (M6).
- G1 counts 27 rows and 27 `admitted`; the F27 row's topic is never read (M5).
- G6 `sized` floor is 3000 bytes; the shipped entry is 10707 bytes, so the floor binds nothing.
- G4 runs `TOOL_ROOT/corpus/instruments/source-recheck.py` (line 229). When the counter is run in place, TOOL_ROOT is the graded tree, so the recheck is tree-supplied. The manifest pin (`manifest.json` sha) does not cover the recheck script. M10 confirms.

Discriminator: M1 (a fabricated curly-quoted span) is the only probe in the table that the gate fails. M2 shows the same fabrication with straight quotes passes.

## F3 — text in the shipped entry that the source does not support (not gate-visible)

These are present in the exported tree, not constructed. Each is verifiable by reading the cited lines.

1. Entry line 42 (What is new, item 2): "The page requires … a fix tested before reporting (`S071.txt:195-196`, `S071.txt:213-217`; the MUST list at `S071.txt:239-245`)." The MUST list at `S071.txt:239-245` has two items: a plain-text report with the four items (241-245) and a recipients section (246-250). It has no fix duty. Lines 213-217 say "Please ask your tool to propose a fix and **test it** before reporting" — a request, not a requirement. The word "requires" overstates the source.
2. Entry line 26 (deferral reason): the quote stops at "the logistics of QA" (`S071.txt:312-314`), and the gloss reads "Record QA **or** large-scale rollout coordination". The source (`S071.txt:313-315`) reads "the logistics of QA **and** large scale rollouts which require release coordination". The gloss turns a conjunction into a disjunction and drops the truncation without an ellipsis.
3. Entry line 43 calls the 7-day ceiling "the maintainer's own ceiling, not a researcher deadline." The source (`S071.txt:309-311`) says the postponement is "at the request of the reporter or an affected party", so the ceiling caps a reporter-requested deferral. Line 58 of the entry says so; line 43 contradicts it.
4. SOURCES.md row S071 (line 77) scope cell reads: "The kernel security team's own report-intake and embargo rules only; its CVE and linux-distros statements are outside this row." The entry relies on exactly those statements at line 27 (linux-distros, `S071.txt:350`) and line 29 (CVE, `S071.txt:362-363`). The registry scope limit and the entry's use disagree.
5. corpus/README.md F27 row (line 651): "the AI-found, binary-only and unreproducible refusal rules". S071 contains no refusal of AI-found reports. It says such bugs must be treated as public (`S071.txt:95-96`) and that a reproducer is shared on request (`S071.txt:99`, `210-211`). "Refusal" is the row author's word, and the entry itself does not use it.
6. Entry Limits (line 48): "The assignment labels the page as versioned 7.3.0 at capture". This cites an assignment that a reader of the corpus cannot open. Not a source claim; a process leak into a knowledge entry. `grep '7\.3' S071.txt` returns no match (rc=1), so the entry is right not to rely on it.
7. Novelty / overlap is incomplete. Overlap (lines 33-37) names only F02, F04 and F15. The corpus contains `knowledge/cisa-bod-20-01-vdp-minimums.md` (required policy elements for an intake floor, which the entry's "What is new" item 1 claims is absent elsewhere) and `knowledge/vendor-disclosure-policies-as-corpus-objects.md:174` (FR-4: "A package stating a fixed embargo length … is unsupported"), which is the same falsifiable rule as the entry's Falsifiable package rule (lines 52-54). Neither is cited, so the "new" claims are not compared against them.

Items 1-5 are text errors that the counter cannot see; item 7 is a coverage-novelty omission. None blocks 7/7.

## F4 — the non-author closure clause: what network access can and cannot satisfy

Claim kill rule: "or if the non-author closure re-opening S071 does not locate the cited quotes."

Re-run with network only (public documentation GET, read-only, no credentials):
- `curl -sS -o live-S071.rst.txt -w 'http=%{http_code} bytes=%{size_download}\n' https://docs.kernel.org/_sources/process/security-bugs.rst.txt` → `http=200 bytes=20152`; `sha256sum` → `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, identical to the pinned capture.
- `curl … https://docs.kernel.org/process/security-bugs.html` → `html http=200 bytes=33621`; after tag stripping and whitespace normalisation the six quotes checked (the five manifest quotes and the "The only valid reason…logistics of QA" span) all print `HIT`.

So a network-only closer can: fetch the RST capture and confirm the pinned sha256, and locate the quotes in either the RST or the cited HTML. That part of the clause is satisfiable today.

What network access cannot satisfy:
- The counter does not perform the closure. G4 reads the local capture and the local manifest; the counter contains no fetch and no identity check (grep: no `author`, no `reviewer`, no `git`). "Non-author" is a process statement with no record, so nothing gates it.
- The pins are point-in-time. The RST's last-modified is 2026-08-09 (SOURCES.md row S071). If the live page changes, G3/G4 fail on `snapshot-not-the-pinned-capture` / `manifest-not-the-pinned-bytes`. The PIN override exists only for selftests (`R45_PINS_OVERRIDE`, line 63), so a non-author cannot re-pin the gate against a newer page without editing the tree.
- The cited source URL in the entry (the HTML page) and the pinned capture (the RST source) are different artifacts. The quote check runs on the RST bytes, not on the HTML the entry cites. The HTML currently carries the same quotes (above), so this is not a present falsity, but the gate does not test the URL it reports.

Answer to the question: a person with network access only can satisfy the quote-location part of the non-author closure for the current bytes, by hand. They cannot satisfy it through the counter, and nothing in the artifacts records that the closure was done by a non-author.

## F5 — what remains un-gated (complete list of what the 7/7 does not certify)

1. Straight-quoted text (M2).
2. Any uncited prose, including contradictions of the source (M6, M7, M11).
3. Whether a cross-reference line supports its sentence, and whether the span after `-` exists (M3, M9).
4. Whether the frontier row's topic matches the entry (M5).
5. The body of any section; only the `##` header is checked (M8).
6. Quote minimum: four located curly spans are enough; the other 20 quotes could be unmarked (M7).
7. The recheck script in G4 is tree-supplied when run in place (M10).
8. The census in G7 is a fleet-root constant (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, 35466 bytes, mtime Oct 19) and is not hash-pinned; the gate depends on it without a pin.
9. The 3000-byte floor (G6) binds nothing at 10707 bytes.
10. Novelty against existing entries (F3 item 7).
11. Non-author closure (F4).
12. The text errors in F3 items 1-5.

## Controls and limitations

- Controls. The frozen controls file (`.ufo/waves/round-45/controls/freeze-controls.txt`) records `c2-junk-row … fixed=4/7` and `c2-fabricated-quote … fixed=5/7`. Those fixtures are not in the export and I did not re-run them; I cite the file's printed values, not a re-run. The do-nothing control I did re-run (1/7).
- Mutants were built from the export copy by string edits in scratch; the export and the lane working tree were not modified. Each mutant's printed result is from a re-run I performed.
- The gate's G7 and the census path are out of the tree; I ran the census on the export's SOURCES.md and it printed `file	ok	…` with rc=0.
- Live fetches were two read-only GETs of public documentation. No live system was tested.
- I did not audit QUALITY R47-R49, the round-44 correction, SKILL.md, or the freeze-check/ selftest artifacts; they are outside C2.
- Nothing was installed; no tool versions to record.
