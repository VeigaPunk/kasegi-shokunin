# R46RevC2G2 — attack on C2 gate G2 (entry provenance trio, sections, table, cross-references)

VERDICT: BROKEN

Scope: `corpus/instruments/r46-c2-gate.py` `def g2` (lines 182-206) and its docstring predicate (lines 15-19). Counter run from the freeze-commit export (`git archive 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 corpus`) into scratch; `--root` pointed at each fixture tree. No repo file was edited; nothing committed; no git mutation. Read-only git used: `cat-file -t`, `diff --stat`, `archive`.

## What G2 actually tests (read from code)

- `g2` line 191-193: trio test is `h.startswith("source: S073 — " + URL + " — ")`, `h == "verified-at: 2026-10-28"`, and `h.startswith("recheck: ") and "source-recheck.py" in h and "--source S073" in h`, over the first 8 live lines.
- Line 194: four `SECTIONS` headings must appear as `^## ...\s*$` anywhere in the body; no content is required under them.
- Line 195: `tbl = len([lines matching ^\|[^|]+\|[^|]+\|[^|]+\|\s*$]) - 2`; needs `tbl >= 6`. Each cell only needs one non-pipe character, so `| — | — | — |` counts.
- Lines 196-204: every `corpus/knowledge/<f>.md:<n>` must point at an existing file and an in-range line, and both `linux-kernel-security-bugs-reporting-process.md` and `ai-assisted-finding-validation.md` must be cited. The cited line's content is never read.
- The recheck line is never executed by the counter. G4 (line 246) runs `source-recheck.py` on the manifest, not on the entry's recheck line. Entry bytes are unpinned (`PINS["entry"] is None`, line 59).

## Controls (re-run by me)

1. Do-nothing (freeze-commit `corpus` on the pure base tree, `--root base`):
   `gate G2 pass=0 read=F28-rows=0` / `c2-gate fixed=1/7 exit=1`. Matches controls file line 53-59.
2. Freeze tree (`--root frz`): `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`, `gate G7 pass=1 read=census-rc=0 ok-line=1`, `c2-gate fixed=2/7 exit=1`. Matches claims.json C2 `freeze_tree_reading`.

## Finding 1 — G2 passes the pasted skeleton (the defect asked for)

Recipe, cheapest tree that makes G2 print pass=1 (fixture `v0`, 745-byte entry plus two 1-line stubs):

- `corpus/README.md`: one row, `| F28 | GitHub private vulnerability reporting (reporter flow) | admitted | \`knowledge/github-private-vulnerability-reporting.md\` | S073 | Reporter flow only. |`
- `corpus/knowledge/github-private-vulnerability-reporting.md`: H1; `source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — section anchors: none`; `verified-at: 2026-10-28`; `recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d`; the four `## ` headings with a one-character body (`—`); a table of header, separator and six `| — | — | — |` rows; one sentence citing `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:1` and `corpus/knowledge/ai-assisted-finding-validation.md:1`.
- `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` and `ai-assisted-finding-validation.md`: one-line stubs (`# stub`). The xref targets must exist; without them G2 reads `xrefs=0/2` and fails (measured).

Command: `TMPDIR=<scratch> python3 r46-c2-gate.py --root <v0>` printed:

```
gate G1 pass=0 read=rows=1 admitted=1 dup=0
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2
gate G3 pass=0 read=row-S073=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate G6 pass=0 read=knowledge=3 base-names-intact=0 entry-bytes-ok=0
gate G7 pass=0 read=census-rc=2 ok-line=0
c2-gate fixed=1/7 exit=1
```

Same skeleton inside a full tree (`v1` = freeze corpus + F28 README row + a correctly formed S073 row, 11 cells, sha-pinned anchor) printed:

```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate G6 pass=0 read=knowledge=65 base-names-intact=1 entry-bytes-ok=0
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=5/7 exit=1
```

So the real defect is caught by G5 (no located quotes) and G6 (under 3000 bytes), not by G2. Discrimination: G2 is not a pass-through; the ablations below show it red for each structural break.

Distinct constructions that make G2 pass (≥5, all printed `gate G2 pass=1`):

1. minimal skeleton, 745 bytes, two stub xref targets (fixture v0) — `table-rows=6 xrefs=2/2`.
2. same skeleton inside the full tree (v1) — G2 pass, c2 fixed 5/7.
3. recheck line whose command is decorative: `recheck: true echo source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d` (fixture vD and x3) — `recheck=1`; x3 ran at 7/7 (see Finding 3).
4. recheck with substring `--source S0730` (fixture x4) — `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`. The check is `"--source S073" in h`, a substring match.
5. a verbatim restatement with the five frozen cores quoted and cited, trio, four headings and a 6-row table whose decision column is `see the page` (fixture v2, 5223 bytes; section 'Scope' quotes `S073.txt:564,573,574,577,578`) — G2 pass=1, and the whole counter prints `c2-gate fixed=7/7 exit=0`.

## Finding 2 — G2 can fail alone (discrimination)

Ablations on the v0/v2 family, each printed one `gate G2` line:

- no `source:` line (vA): `gate G2 pass=0 read=source=0 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`
- no `verified-at:` line (vB): `gate G2 pass=0 read=source=1 verified-at=0 ...`
- `--source S072` in recheck (vC): `gate G2 pass=0 read=source=1 verified-at=1 recheck=0 ...`
- `## Limits` removed (vE): `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=3/4 table-rows=6 xrefs=2/2`
- one table row removed, five rows (vF): `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=5 xrefs=2/2`
- both xrefs removed (vG): `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=0/0`
- xref line set to 9999 (vH): `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=0/2`
- wrong canonical URL (vJ): `gate G2 pass=0 read=source=0 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`
- table inside a fenced code block (vL): `gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=-2 xrefs=2/2`

G2 fails alone: fixture x1 is v2 with `## Limits` renamed to `## Limitations`. Printed:

```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=0 read=source=1 verified-at=1 recheck=1 sections=3/4 table-rows=6 xrefs=2/2
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=6/7 exit=1
```

Fixture x2 (v2 with the AI cross-reference's `:1` citation replaced by prose) prints `gate G2 pass=0 read=... xrefs=1/1` and `c2-gate fixed=6/7`, again G2 alone red. So G2 can fail alone, and its structural checks do bite; the gap is in what they cannot see.

## Finding 3 — the full counter can be 7/7 with a restatement-only entry (outside G2, reaches the C2 kill rule)

Fixture v2 (entry text in `v2src/entry.md`, 5223 bytes) prints:

```
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```

The entry's decision column is `see the page` on all six rows and its 'Falsifiable package rule' section restates the page. C2's kill rule says the entry must not restate the page without a decision rule; no gate checks for that, and the freeze controls contain no restatement control, so this passes 7/7. Only the non-author closure can catch it.

Also: fixture x3 (recheck line `true echo source-recheck.py …`) prints `c2-gate fixed=7/7 exit=0`, so the entry's recheck line can be decorative and still pass the counter.

## Limitations

- Only G2 was attacked; G1, G3–G7 were exercised only as they appear in the printed runs above. The C1 counter and the other frozen controls (junk-row, fabricated-quote, uncited-filler) were not re-run by me, only the do-nothing and freeze readings.
- The v2 prose is my fixture text, not a draft for corpus/knowledge; its quotes are copied from the committed capture `corpus/source-snapshots/round-46/S073.txt` (lines 564, 573, 574, 577, 578). No live GitHub fetch was made.
- The counter run used the freeze-commit export of `corpus/` (identical to the lane's freeze commit by `git archive`), not the lane working tree. Its `TOOL_ROOT` is the export.
- `R46_PINS_OVERRIDE` (counter line 66-67) can disable pins by environment variable; not exercised, read from code only.
- Pins: the entry pin is `None` by design (docstring lines 33-34), so G2 never binds to bytes; this is why Findings 1 and 3 are reachable.

Scratch removed on exit. No files written outside this report.
