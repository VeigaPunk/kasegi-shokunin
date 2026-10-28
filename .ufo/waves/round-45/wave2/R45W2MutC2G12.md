VERDICT: BROKEN

Seat R45W2MutC2G12 — mutation test of `corpus/instruments/r45-c2-gate.py` v1.1, gates G1 and G2 only.
Subject: lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6), exported with
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/export`.
The export was never edited; each mutant ran on a fresh copy of `export/corpus/`. Counter bytes were
checked before and after every run: sha256 `639a038a99bdd19d1ae612b45cff63a5631b4b2e5fc7e727e9e5f78339c205f2`,
`counter-sha-ok=1` on every mutant.

Baseline (do-nothing control, unmutated export), command
`python3 corpus/instruments/r45-c2-gate.py --root <export>`:
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=13 xrefs=5/5
... G3-G7 pass=1 ...
c2-gate fixed=7/7 exit=0
```

Method: `rejected=1` = counter exit non-zero. Each mutant is one edit; a rendered-markdown probe
(markdown-it-py 4.2.0, `commonmark` + `table`) asserts the defect is actually present before the counter runs
(`defect-present=1` on every row below). Recipe run: `R45_SCRATCH=<scratch> TMPDIR=<scratch>/tmp venv/bin/python recipe.py`.

## Survivors (counter green while the defect is present)

### S1 — G2 accepts the provenance trio inside an HTML comment (survives)
- Attacked: `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` lines 3-5 (`source:`, `verified-at:`, `recheck:`). Edit: insert `<!--` before line 3 and `-->` after line 5. Nothing else changed.
- Root cause: G2 reads the raw body, `head = body.splitlines()[:8]` (`r45-c2-gate.py:178`), and never strips comments (`live_lines`, L108-118, is applied only to frontier/registry rows, L124 and L133).
- Output: `mutant=g2-trio-in-html-comment rejected=0` / `target=G2 defect-present=1 probe: trio-visible=False` / `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=13 xrefs=5/5` / `exit=0`.
- Impact: the rendered entry shows no provenance header; the only check of the header passes.

### S2 — G2 accepts the `## Limits` section heading inside a code fence (survives)
- Attacked: line 45 `## Limits`. Edit: replace the line with three lines: "```", "## Limits", "```".
- Root cause: section check is a raw regex, `re.search("^" + sct + r"\s*$", body, re.M)` (`r45-c2-gate.py:182`), blind to fences.
- Output: `mutant=g2-limits-heading-in-fence rejected=0` / `defect-present=1 probe: rendered-h2=['Scope and decision rule', 'Overlap and novelty', 'Falsifiable package rule', 'Rejected over-generalizations']` / `gate G2 pass=1 read=... sections=4/4 ...`.
- Impact: a required section is shown as code text; the counter reports 4/4.

### S3 — G2 accepts the evidence table hidden in an HTML comment (survives)
- Attacked: the 13-row table at lines 15-29. Edit: insert `<!--` before line 15 and `-->` after line 29.
- Root cause: the table count is over raw lines, `tbl = len([ln for ln in body.splitlines() if re.match(r"^\|[^|]+\|[^|]+\|[^|]+\|\s*$", ln)]) - 2` (`r45-c2-gate.py:183`).
- Output: `mutant=g2-table-in-html-comment rejected=0` / `defect-present=1 probe: rendered-tables=0 raw-table-rows=13` / `gate G2 pass=1 ... table-rows=13 ...`.

### S4 — G2 cross-reference check only tests that the cited line number exists (survives)
- Attacked: line 36 citation `corpus/knowledge/ai-assisted-finding-validation.md:7-8,15`, changed to `...ai-assisted-finding-validation.md:1` (line 1 is the title).
- Root cause: `refok` counts a reference when `1 <= int(ln) <= len(t.splitlines())` (`r45-c2-gate.py:186-189`, `:192`). The content at the cited line is never compared to the claim, and the regex keeps only the first number of a range (L184).
- Output: `mutant=g2-xref-cites-line-1 rejected=0` / `defect-present=1 probe: cited-line-1='# AI-Assisted Finding Validation'` / `gate G2 pass=1 ... xrefs=5/5`.

### S5 — G2 recheck-line check is a substring test; `--source S071X` passes (survives)
- Attacked: line 5 `recheck:` line, `--source S071 # 180d` changed to `--source S071X # 180d`.
- Root cause: `"--source S071" in h` (`r45-c2-gate.py:181`). The recheck command text is never parsed; G4 runs the real recheck but does not check that this line names the same command.
- Output: `mutant=g2-recheck-source-substring rejected=0` / `defect-present=1 probe: --source token=S071X` / `gate G2 pass=1 ...`.

### S6 — G1 counts "27 admitted" by status cell only; an admitted row with no entry passes (survives)
- Attacked: `corpus/README.md` line 264, F13 row: entry cell `knowledge/program-severity-ladders-and-reward-scales.md` replaced by `none`; status still `admitted`.
- Root cause: `adm = sum(1 for r in rows if ... r[2] == "admitted")` (`r45-c2-gate.py:162`). Entry checks (L166-170) apply to F27 only. The same status-only count is in the round-44 counter (`corpus/instruments/r44-frontier-count.py:68-69`, `cells[2] == "admitted"`), so the weakness is inherited.
- Output: `mutant=g1-f13-entry-blank rejected=0` / `defect-present=1 probe: admitted-rows-without-entry=['F13']` / `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`.

### S7 — G1 row regex misses a rendered frontier row with a leading space (survives)
- Attacked: `corpus/README.md`, one line inserted after the F27 row (line 651): ` | F28 | Junk admitted row | admitted | knowledge/cvss-v4-severity-and-vector.md | S001 | x |` (one leading space).
- Root cause: rows are selected by `re.match(r"^\| F\d+ \|", ln)` (`r45-c2-gate.py:125`), which requires column 0.
- Output: `mutant=g1-leading-space-row rejected=0` / `defect-present=1 probe: rendered-admitted-F28-rows=1 rendered-rows=28` / `gate G1 pass=1 read=rows=27 admitted=27 ...`.

### S8 — G1 row regex misses a rendered frontier row with compact pipes (survives)
- Attacked: one line inserted after the F27 row: `|F28|Junk admitted row|admitted|knowledge/cvss-v4-severity-and-vector.md|S001|x|` (no spaces).
- Same root cause as S7 (`r45-c2-gate.py:125` requires `| F\d+ |` with spaces).
- Output: `mutant=g1-compact-pipe-row rejected=0` / `defect-present=1 probe: rendered-admitted-F28-rows=1 rendered-rows=28` / `gate G1 pass=1 read=rows=27 admitted=27 ...`.

### S9 — G1 does not require the frontier ids to be F01..F27; renumbering F26 to F28 passes (survives)
- Attacked: `corpus/README.md` line for `| F26 |`: id changed to `| F28 |`. The table keeps 27 rows and 27 admitted.
- Root cause: the predicate checks length, admitted count and duplicates only (`r45-c2-gate.py:164`: `if len(rows) != 27 or adm != 27 or dup`). It does not check that the ids are the contiguous set F01..F27.
- Output: `mutant=g1-renumber-f26-to-f28 rejected=0` / `defect-present=1 probe: F26-rendered=False F28-rendered=True rows=27` / `gate G1 pass=1 read=rows=27 admitted=27 ...`.

## Gate-local survivor (G1 green, overall caught elsewhere)

### S10 — G1 binds F27's entry cell to any existing, unshared file, not to the F27 entry (caught by G2/G3/G5/G6)
- Attacked: F27 row entry cell changed to `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` (an existing knowledge file that no README row mentions).
- Output: `mutant=g1-f27-entry-unrelated rejected=1` / `gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` / `gate G2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 ...` / `gate G3 pass=0 read=bad=used-by` / `gate G5 pass=0 read=spans=0 ...` / `gate G6 pass=0 read=knowledge=64 base-names-intact=0 ...`.
- Reading: G1 alone does not show the F27 entry is the S071 entry; the failure is caught by G2, G3, G5 and G6, not G1.

## Discrimination (controls)
- do-nothing: `mutant=control-do-nothing rejected=0` (exit 0; green baseline).
- positive, G1: `mutant=control-delete-f27-row rejected=1` / `gate G1 pass=0 read=rows=26 admitted=26 dup=0`.
- positive, G2: `mutant=control-header-past-window rejected=1` (six blank lines pushed the trio past line 8) / `gate G2 pass=0 read=source=0 verified-at=0 recheck=0 ...`.
So the counter does reject a missing F27 row and a header outside its window; the survivors above are not a harness that never fails.

## Dropped candidate (not claimed)
- A `    ```` indented fence token placed before an inserted F28 row was tried, expecting the counter to skip the row. markdown-it renders the row outside the table (`venv/bin/python rendercheck.py readme-m01.md` printed `F25|admitted`, `F26|admitted`, `F27|admitted` only), so there is no rendered 28th row and no claim is made.

## Pins and scope
- None of the mutants touched the pinned bytes (`S071.txt`, `manifest.json`, base knowledge names); G3 and G4 stay green on S1-S9. The pins make byte forgeries of the capture moot, which is why the survivors are all in unpinned surfaces: the entry body, README rows, and the recheck line.
- Only G1 and G2 were mutated. G3-G7 were not mutated and no claim is made about them.

## Limitations
- The renderer is markdown-it-py 4.2.0 (`commonmark` + `table`), not GitHub's renderer. Statements that GitHub renders S7/S8 the same way are [INFERENCE].
- Each mutant is one edit (a "wrap" is two inserted lines; "fence wrap" is one line replaced by three). The mutants are single defects, not exhaustive.
- S5 is textual: G4 still runs the real recheck, so the substring survivor concerns only the text of the line.
- Round-44 counters share the status-only count (S6). Not tested beyond the source line cited.

## Tooling record (RULES.md; no PATH or system changes)
- markdown-it-py 4.2.0, channel `uv pip install` (uv 0.13.0) into a scratch venv, reason: render probes for the table and fence checks. Nothing installed into ~/.local/bin or any PATH directory; no pacman transaction.

## Restoration
- Export and copies were scratch-only. The lane tree, the commit, the index and shared production files were not touched. Scratch removed on exit.
