VERDICT: BROKEN

# R45W2MutC2G34 — mutation test of C2 gates G3 and G4 (r45-c2-gate.py v1.1)

Scope: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (extracted with `git archive | tar -x` into scratch; the lane working tree was not read). Counter bytes unchanged: `sha256sum corpus/instruments/r45-c2-gate.py` = `639a038a99bdd19d1ae612b45cff63a5631b4b2e5fc7e727e9e5f78339c205f2`. Each mutant copies only the export's `corpus/` tree into a fresh scratch root (counter TOOL_ROOT = that copy), applies one edit to the copy, and runs the unmodified counter with `--root`. Pristine export never written.

Result of the do-nothing control on the tip export (all green, so the mutants start from a fully green tree):

```
mutant=control-do-nothing rejected=0 target=G3+G4 G3=1 G4=1 exit=0
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=13 xrefs=5/5
gate G3 pass=1 read=row-S071=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=24 located=24 failed=0 uncited=0 cores=4/4
gate G6 pass=1 read=knowledge=64 base-names-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
```

## Survivors (counter green while the defect is present) — listed first

### F1. G4 accepts a stubbed recheck tool: `mutant=g4-tool-stub-all-ok rejected=0 target=G4 target_pass=1`
- Edit: `corpus/instruments/source-recheck.py` replaced in full by a 6-line stub: prints `S071:sha256 OK`, prints `S071:Q1 OK occurrences=1` … `S071:Q5 OK occurrences=1`, `sys.exit(0)`. Reads nothing.
- Printed: `gate G3 pass=1 read=row-S071=ok` / `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0` / `gate G7 pass=1 read=census-rc=0 ok-line=1` / `c2-gate fixed=7/7 exit=0`.
- Why: G4 executes the tree's own tool (`r45-c2-gate.py:57` TOOL_ROOT, `:229-230` run). `PINS` (`:58-62`) cover only `S071.txt`, `manifest.json` and the base knowledge names; the tool's bytes are not pinned. G4's pass is therefore whatever the tree's tool prints. The defect "capture not actually re-verified" is fully reintroduced.

### F2. G3 accepts the S071 row when it sits only inside a `~~~` fence: `mutant=g3-row-in-tilde-fence rejected=0 target=G3 target_pass=1`
- Edit: `corpus/SOURCES.md` line 77 (the S071 row) wrapped as lines 77 `~~~`, 78 the unchanged row, 79 `~~~`. No other change; the row is no longer a rendered table row.
- Printed: `gate G3 pass=1 read=row-S071=ok`; `gate G7 pass=1 read=census-rc=0 ok-line=1`; `c2-gate fixed=7/7 exit=0`.
- Why: `live_lines` (`r45-c2-gate.py:108-118`) strips fenced blocks only when `ln.strip().startswith("```")` (`:113`); `~~~` fences are not stripped, so `registry_lines` (`:130-139`) and G3 treat the fenced row as live. The fleet census used by G7 has no fence handling either (`grep -n '~~~\|```\|fence' scripts/sources-census.sh` printed nothing), so the same defect passes G7. [INFERENCE from CommonMark, not executed here: `~~~` opens a code block, so the row would not render as a table row.]

### F3. G3 anchor check is substring-only: `mutant=g3-anchor-wrong-digest rejected=0 target=G3 target_pass=1`
- Edit: `corpus/SOURCES.md` line 77, anchor cell (cell 5) — the pinned sha `0918dcfa…9346f40` replaced by `9a9a9a9a0918dcfa…9346f40` (a 72-hex run whose tail is the pinned digest). The probe printed the resulting run: `['9a9a9a9a0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40']`.
- Printed: `gate G3 pass=1 read=row-S071=ok`; `c2-gate fixed=7/7 exit=0`.
- Why: `r45-c2-gate.py:219` `if snap_sha not in row[5]` is a substring test; it does not require the cell to hold a 64-hex sha256 equal to the pinned one. The snapshot file itself is pinned (`:211-212`), so the wrong digest in the row is the only thing left unchecked.

### F4. G3 source-URL check is substring-only: `mutant=g3-source-url-lookalike rejected=0 target=G3 target_pass=1`
- Edit: `corpus/SOURCES.md` line 77, source cell (cell 1): `https://docs.kernel.org/process/security-bugs.html` → `https://docs.kernel.org/process/security-bugs.html.mirror.example`.
- Printed: `gate G3 pass=1 read=row-S071=ok`; `c2-gate fixed=7/7 exit=0`.
- Why: `r45-c2-gate.py:217` `if URL not in row[1]` accepts any cell containing the canonical string, including a host-suffix lookalike. The canonical-URL requirement is not an equality check.

### F5 (composition, not one of the ten single edits). G4 is blind once the tool's sha check is removed and the snapshot changes; only G3's pin catches it
- Command: `python3 probe.py` (scratch; output pasted here). Probe 1 = snapshot tamper only (append `forged trailing line` to S071.txt). Probe 2 = same tamper plus `corpus/instruments/source-recheck.py:` `if actual != expected:` → `if False:`.
- Printed for probe 1: `probe=probe-snapshot-tamper-only rejected=1 exit=1` / `gate G3 pass=0 read=snapshot-not-the-pinned-capture` / `gate G4 pass=0 read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0` / `c2-gate fixed=5/7 exit=1`.
- Printed for probe 2: `probe=probe-snapshot-tamper+g4-sha-unchecked rejected=1 exit=1` / `gate G3 pass=0 read=snapshot-not-the-pinned-capture` / `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0` / `c2-gate fixed=6/7 exit=1`.
- So G4 contributes no independent sha detection: it passes the tampered snapshot when the tool's check is off (`r45-c2-gate.py:211-212` pin is the only catch).

### F6 (single edit, survives G4 only when the tool sha check is off; equivalent under the tip pins). `mutant=g4-tool-sha-unchecked rejected=0 target=G4 target_pass=1`
- Edit: `source-recheck.py` `if actual != expected:` → `if False:`. Output identical on the pinned tip, so the mutant is observable only through F5.

## Masked by another gate (G3 accepts; a different gate rejects)
- `g3-usedby-dangling-suffix`: `corpus/SOURCES.md` line 77 used-by cell gets `.orig` appended. Printed: `gate G3 pass=1 read=row-S071=ok` and `gate G7 pass=0 read=census-rc=1 ok-line=0`. G3's used-by check is `p not in row[10]` (`r45-c2-gate.py:218`), a substring test; the census, not G3, kills it.
- `g3-registry-heading-retired`: line 3 `## Registry` → `## Registry (retired 2026-10-01)`. Printed: `gate G3 pass=1`, `gate G7 pass=0 read=census-rc=1`. G3's section regex `^ {0,3}## Registry\b` (`:134-135`) accepts the retired heading; the census kills it.

## Controls (killed as expected)
- `g3-tier-B-control`: `corpus/SOURCES.md` cell 3 `A`→`B`. Printed: `mutant=g3-tier-B-control rejected=1 target=G3 target_pass=0 exit=1`, `gate G3 pass=0 read=bad=tier`.
- `g4-tool-check-source-silent`: `return 0` inserted at top of `check_source`. Printed: `mutant=g4-tool-check-source-silent rejected=1 target=G4 target_pass=0 exit=1`, `gate G4 pass=0 read=recheck-rc=0 quotes-ok=0`.
- `g4-tool-rc1-all-ok`: `return status` → `return 1` in `recheck`; quote lines unchanged. Printed: `mutant=g4-tool-rc1-all-ok rejected=1 target=G4 target_pass=0 exit=1`, `gate G4 pass=0 read=recheck-rc=1 quotes-ok=5 frozen-cores-missing=0`.

## Mutant table (10 single edits + control; every line from `python3 recipe.py`)

| mutant | target | rejected | target_pass | what killed it |
|---|---|---|---|---|
| g3-tier-B-control | G3 | 1 | 0 | G3 |
| g3-anchor-wrong-digest | G3 | 0 | 1 | survives (F3) |
| g3-source-url-lookalike | G3 | 0 | 1 | survives (F4) |
| g3-usedby-dangling-suffix | G3 | 1 | 1 | G7 only |
| g3-row-in-tilde-fence | G3 | 0 | 1 | survives (F2) |
| g3-registry-heading-retired | G3 | 1 | 1 | G7 only |
| g4-tool-stub-all-ok | G4 | 0 | 1 | survives (F1) |
| g4-tool-check-source-silent | G4 | 1 | 0 | G4 |
| g4-tool-rc1-all-ok | G4 | 1 | 0 | G4 |
| g4-tool-sha-unchecked | G4 | 0 | 1 | survives under pins (F6; F5 shows the composition) |

Counts: 4 survivors (F1-F4) plus F6 (pin-equivalent) and F5 (composition probe); 2 masked by G7; 3 controls killed by their own gate.

## Limitations
- Only G3 and G4 were mutated, one edit per mutant, as assigned; G1, G2, G5, G6 and G7 were not mutated (G7 only observed as the census verdict that masks two G3 mutants).
- The pins were treated as given (`PINS` values unchanged); I did not test whether the pinned values themselves are correct.
- G7 calls the fleet census at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (`r45-c2-gate.py:56`), which lies outside this lane; I only read it (grep). Its verdict is not pinned by the counter.
- Untested idea: `source-recheck.py` is run as `python3 <TOOL_ROOT>/corpus/instruments/source-recheck.py`, so `sys.path[0]` is `corpus/instruments/`; a module there could shadow a stdlib import. Not executed.
- G3 reads row cells by position (`:202-219`) and does not read the header; header relabelling was not tested.
- `live_lines` treats only ``` fences (`:113`); the CommonMark claim in F2 is inference, not rendered.
- No commit, push, git or index mutation; the lane tree was not written; scratch directory removed after this report.

## Suggested direction (not implemented)
- Pin `source-recheck.py` bytes (or inline the quote check into the counter) and remove the tree-supplied tool from G4's trust path.
- G3: compare the anchor cell to `^[0-9a-f]{64}$` exactly; compare the source cell for URL equality; strip `~~~` fences in `live_lines`; match `## Registry` exactly.
