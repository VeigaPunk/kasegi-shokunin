# Falsify — F06/F07/F08 sources-cell binding (C2 coverage)

Seat: `L1Kasegi23.FrontierSources-2` · lane: round-23 falsify · read-only attack on landed bytes.
Assigned item: "Verify each admitted F06-F08 row's sources cell matches the entry's own source header
and current registry rows." Plus the brief's "report a mismatch anywhere, including a row citing a
superseded id (S022/S024) as if it were the current authority."

All paths are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Verdict

| # | Claim attacked | Result | Confidence |
|---|---|---|---|
| A | `corpus/README.md:200-202` **sources cell** ↔ each entry's `source:` header (id **and** URL) | **holds 3/3** — ids identical, URLs byte-identical to the registry row | high (scripted extraction) |
| B | README sources cell ↔ `corpus/SOURCES.md` **`used-by`** cell | **holds 3/3** — `used-by` == `corpus/<entry>` for S018/S029/S030, each status `mined` | high |
| C | Any of the three cells holding a superseded id out as the **current** authority | **holds 3/3** — cells read `S030 (supersedes S022)` / `S029 (supersedes S024)`; neither S022 nor S024 is presented as current | high (full live-doc sweep below) |
| D | F07 `source:` header anchor is an *exact* anchor (QUALITY Q1) and matches the registry anchor | **FAILS** — header says `3.2.4`, registry and the entry's own body say `3.2.4.2` (F2) | high |
| E | The README index carries a **Coverage-map row** for each newly admitted entry ("every disk file earns a row") | **FAILS 0/3** — 30 Coverage-map rows vs 33 knowledge files; the three missing are exactly the round-23 entries (F1) | high (section-scoped census) |

The assigned comparison itself is **clean**. The defects below are in the same index/provenance
chain, not in the three sources cells.

## Bytes under test (pinned 2026-10-25T06:40:36Z)

| file | sha256 | vs HEAD `953c278` |
|---|---|---|
| `corpus/README.md` | `2d3e9f4b59aacd3f54a773c786fb50a28bacf05cd7d3c88bcd2232fea81a0ac5` | unmodified |
| `corpus/SOURCES.md` | `32a19dc403c1a1de470607b75a1477c2b129e14213be4c6afed3d8f5bd672b4c` | unmodified |
| `corpus/knowledge/multiparty-vulnerability-coordination.md` | `258648095adc219f329f0a030434f7beb4734cdeab4303dd58f78b35a1a60094` | modified (peer edits, see Gaps) |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | `44016013b6b0c6053a4f2a22add62dfef0a3b1e5cd3fe36b11cf5f5e3d5221c4` | modified (peer edits) |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | `b33afa37dfe4f97d8cd92673aa98f9d02f51aa5fceb2eebe34d2d1f5d95684a8` | modified (peer edits) |
| `corpus/source-snapshots/round-23/manifest.json` | `d1020fee34e0674553cd40187704cd226c14d2db2eef622a19367c1cc88abc3a` | modified (peer edits) |

The three `source:` lines are **identical at HEAD and in the working tree**; the uncommitted diffs
touch only `recheck:` lines, disclosure prose and the manifest purpose string (`git diff -- corpus/`
= 4 files, +22/−5).

## Findings

### F1 — MEDIUM — README Coverage map has no row for any of the three entries it just admitted

`corpus/README.md:7-44` ("## Coverage map", the index's only per-entry `Source basis` table) lists
30 `knowledge/*.md` rows. `corpus/knowledge/` holds 33 files. The three absent rows are exactly the
round-23 entries — i.e. the index cannot answer which sources support F06/F07/F08 from its own
coverage map (only the separate Frontier table at `README.md:191-202` carries that binding).

```
$ LC_ALL=C comm -13 <(awk 'NR>=7 && NR<=44' corpus/README.md \
    | grep -oE 'knowledge/[a-z0-9-]+\.md' | sort -u) \
  <(ls corpus/knowledge/*.md | sed 's|^corpus/||' | sort -u)
knowledge/cna-assignment-and-vulnerability-rules.md
knowledge/cra-manufacturer-reporting-duties.md
knowledge/multiparty-vulnerability-coordination.md
# rows=30  disk=33   (F06-F08's own F01-F05 rows are present at README.md:37-41)
```

The round-23 README diff changed **only** the three Frontier rows; no Coverage-map row was added:

```
$ git --no-optional-locks show 953c278 -- corpus/README.md | grep '^[+-]|' | cut -c1-60
-| F06 | Multi-party CVD — FIRST guidelines v1.1 | queued
-| F07 | CVE CNA operational rules | queued | — | S022 | O
-| F08 | EU Cyber Resilience Act reporting duties | queued |
+| F06 | Multi-party CVD — FIRST guidelines v1.1 | admitte
+| F07 | CVE CNA operational rules | admitted | knowledge/cn
+| F08 | EU Cyber Resilience Act reporting duties | admitted
```

This is the lane's own recorded defect class, graded MAJOR when it last occurred:

- `corpus/lessons/round-4-aggregator-audit.md:41-43` — "**Missing index row** (`README.md`): coverage
  map has no row for `knowledge/program-quirks.md` … CORPUS.md: *an index row is a claim* — every
  disk file earns a row."
- `corpus/lessons/round-6-aggregator-audit.md:84` — "**MAJOR — index-vs-disk**: `program-quirks.md`
  has no row (routed round-4). `corpus/README.md` coverage map rows (19) vs `corpus/knowledge/*.md` (20)".

Graded MEDIUM, not MAJOR, because the mitigating fact is real: unlike the round-4 case, each file
*does* have a row in the README (the Frontier row), with the correct sources cell, and F1's fix is a
three-row append whose content is already fixed by `README.md:200-202`.

**Command-sensitivity disclosure (verifiability).** The census command *as recorded* in the round-4
lesson greps the whole README, and would now pass, because the Frontier table also names the three
paths:

```
$ comm -13 <(grep -oE 'knowledge/[a-z0-9-]+\.md' corpus/README.md | sort -u) \
           <(ls corpus/knowledge/*.md | sed 's|^corpus/||' | sort -u) | wc -l
0
```

An instrument that passes while the finding stands must scope to the section it names. Suggested
gate: `awk 'NR>=7 && NR<=44'` (Coverage map) as above, or compare row count 30 vs disk 33.

### F2 — LOW — F07 `source:` anchor is the parent heading, not the exact subsection its body relies on

```
corpus/knowledge/cna-assignment-and-vulnerability-rules.md:2
source: S030 — …/CNA_Rules_v4.2.0.pdf — CNA Operational Rules 4.2.0, … effective 2026-08-25; sections 3.1, 3.2.4, 4.1 and 4.2
corpus/SOURCES.md:36  (anchor cell)
Approved 2026-08-20, effective 2026-08-25; sections 3.1, 3.2.4.2, 4.1 and 4.2, especially 4.2.11 page 15
corpus/knowledge/cna-assignment-and-vulnerability-rules.md:33
Version 4.2.0 section 3.2.4.2, pages 9–10, also adds a requirement for an assignment
```

QUALITY Q1 requires the `source:` line to carry "an exact anchor" (`corpus/QUALITY.md:14`). The header
names `3.2.4` where the registry row and the entry's own body name `3.2.4.2`. Both headings exist in
the pinned capture (`S030.txt:108` = `3.2.4 Availability and Responsiveness`, `S030.txt:110` =
`3.2.4.2`), so the anchor is not dangling — it is one level imprecise. Caps severity at LOW; no claim
breaks, and the load-bearing sentence at entry line 33 already carries the exact subsection.

Detection gap: nothing in the automated path checks anchors. `corpus/instruments/source-recheck.py`
docstring (`:3-6`) and manifest purpose assert **substring containment of quotes only** — a wrong or
imprecise section number is invisible to it. Recommend normalising the header to `3.2.4.2` (or
`3.2.4(.2)`), which is a same-line edit under R6.

### F3 — LOW — README front-matter still bounds the public-source set at "five … F01–F05"

`corpus/README.md:5`:

> `[r22 correction: this holds for the 25 legacy entries only; the five round-22 entries (Frontier F01–F05) were read from public sources S001–S015 on 2026-10-19 — see SOURCES.md]`

Current state: 8 admitted frontier rows (`grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md`
→ `8`), 33 knowledge files = 25 legacy + 8 public-source entries, and the round-23 three were read
from `S018`/`S030`/`S029` on 2026-10-20 (`README.md:200-202`, `SOURCES.md:24,35,36`). The bracket is
labelled an r22 correction, so it can be read as dated history; but it is the file's only statement
of which entries are public-sourced, and it now under-enumerates by three. Fix: extend the note (or
append a same-line r23 suffix) rather than rewrite it.

### F4 — INFO — `SCORECARD.md:178` still names S022/S024 as the round-23 admission sources

```
SCORECARD.md:178
2. **coverage** — admit F06–F08 (multi-party CVD S018, CNA rules S022, EU CRA S024) …
```

Mitigating: `SCORECARD.md:176` frames the paragraph as a plan, and `SCORECARD.md:404` records the
result with the correct `S018/S029/S030`. Nothing marks the **source list** in the plan superseded,
though, and `SCORECARD.md:363` ("Round 23 — frozen claims") claims to replace only "the r22
next-plan's stale-cell reconciliation". A reader executing line 178's command would admit CNA 4.1.0
and the S024 row. This is the only live document (outside historical lessons/`considerthese/`) that
presents S022/S024 as the authority; an appended erratum naming S030/S029 closes it and respects R9
(append, do not rewrite filed assertions).

## Non-findings (checked, clean)

1. **Three-way binding, scripted** — cell ids, header id, header URL vs registry URL, `used-by`, status:

```
F06: cell_ids=['S018']        header_id=S018 header_url_eq_registry=True usedby_eq=True status=mined
F07: cell_ids=['S030','S022'] header_id=S030 header_url_eq_registry=True usedby_eq=True status=mined
F08: cell_ids=['S029','S024'] header_id=S029 header_url_eq_registry=True usedby_eq=True status=mined
```

2. **Base→tip direction is correct.** `git show 922a4dde:corpus/README.md` lines 200-202 carry
   `S022`/`S024` in the sources cell; `953c278` replaces them with `S030 (supersedes S022)` /
   `S029 (supersedes S024)`. The superseded ids appear only as supersession pointers.
3. **Superseded rows are honest, not laundered.** `SOURCES.md:28` (S022) and `:30` (S024) stay
   `queued`, `used-by = —`, and the transition is logged
   (`corpus/lessons/round-23.md:203`: "S022, S024 | status | queued | queued (unchanged; historical,
   not rewritten)"). S029/S030's `teaches` cells begin `supersedes S024 —` / `supersedes S022 —`.
4. **Every section the F07 body cites exists in the pinned capture** — `3.1.1` (:64), `3.1.4` (:73),
   `4.1.10` (:166), `4.1.11` (:170), `4.2.1.1` (:179), `4.2.7` (:204), `4.2.11` (:211), `4.2.12`
   (:212), `4.2.13` (:213). No fabricated section number.
5. **F06 header anchor headings exist** — `S018.txt:1` `## Definitions`, `S018.txt:21`
   `## Guiding Concepts and Best Current Practices`. Header is a superset of the registry anchor
   (which omits "Definitions"), not a contradiction.
6. **F08 header anchor is a superset, not a contradiction** — registry anchor
   `Articles 14(1)-(4), 15, 16 and 71` covers the header's `Articles 14, 15, 16 and 71`; the entry's
   new Limits paragraph (working tree) discloses that the `OJ 20.11.2024` date is not in the excerpt
   bytes and rests on the ELI URL + opening date. Self-disclosed, not a hidden overclaim.
7. **Entry paths resolve** — all three `entry` cells name files present on disk; `used-by` paths
   resolve to the same files.
8. **Admitted count reproduces** — `grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md` → `3`.

## Residual risk / verification gaps

- **No LSP device in this seat.** `read xd://lsp` → `No such tool: xd://lsp` (mounted devices listed:
  ast_edit, debug, aseprite/blender/godot/tripo/unity MCP tools). Markdown corpus has no language
  server anyway; every check above is an explicit text/CLI command, and none is presented as semantic
  proof. Definitions/references/diagnostics checks were not possible — recorded as unavailable, not as
  absence.
- **Bytes are moving.** Four corpus files were uncommitted-modified during this run (peer seats adding
  `cd …&&` recheck prefixes and disclosure paragraphs; one edit landed between my first read and my
  digest pin). Findings F1/F3 rest on `README.md`, and F2 on an unchanged `source:` line; the digests
  above are the exact bytes I read. Re-run `sha256sum` before acting.
- **Command sensitivity** for F1 is disclosed above: the lane's recorded census command passes while
  the section-scoped census fails 0/3. A future gate should name the section, per R3's "an instrument
  verdict names its matcher".
- **Snapshots are normalized reader excerpts**, not raw HTTP; `OJ 20.11.2024` and "Spring 2020" are not
  byte-supported (now disclosed in-entry). No network verification was attempted or claimed.
- No mutation of `README.md`/`SOURCES.md` was performed (read-only seat); the coverage-map and
  front-matter defects are proven by content, not by flipping them.

## Scope limits

- C1 (`resolve.py`, mirror matrix, receipts, c1-fixed.json) — **out of scope**, other seats.
- Lessons-row staleness (`README.md:36,44` "25 files" vs 27 files on disk incl. `round-23.md`) — **not
  claimed here**; `LessonGateRows` owns it.
- Admission judgement, score movement, integration, commit — **not claimed**; this seat emits findings only.
- No tools were installed or updated in this run (nothing was needed).
