VERDICT: BROKEN

# R46MutC1c — C1 mutation probe of `corpus/instruments/r46-c1-gate.py` (limbs L6, L7, check_row / section_rows)

Subject: `corpus/instruments/r46-c1-gate.py`, sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` (matches the freeze pin in `.ufo/waves/round-46/freeze.txt`). Read-only; the lane file is unchanged (re-checked: same sha, empty `git status` for the counter and both C1 entries).

## Method

- Fixture: the pure base export (`/fast/scratch/hyaku/kasegi-r46/L1/pure`, copied) as BASE. TREE = BASE plus `claim-gates.md` and `claim-package-contract.md` re-grounded with six rows each over 2–3 committed anchor files (`corpus/instruments/anchorcheck.py`, `recheck-audit.py`, `freeze-check.py`, `source-recheck.py`), the counter copy at `corpus/instruments/r46-c1-gate.py` as the tree's own tool, and a symlinked directory `corpus/instruments/kdir -> ../knowledge`. The fixture also has one probe body line in `claim-gates.md` (line 127, `Fixture probe: the entry’s own text is the anchor.`) so a normalisation-only self-anchor exists. Claim wording is fixture text, not a re-ground deliverable.
- Each mutant = one row or one line edit on a fresh copy of TREE. The oracle is an unmodified copy of the lane counter, run as `python3 -I <oracle> --root <mutant> --baseline <BASE> --work <scratch>`. `rejected=1` means exit non-zero.
- Recipe: scratch-only at `/fast/scratch/hyaku/kasegi-r46/R46MutC1c/recipe.py` (removed on exit). Final run: `R46SCR=… TMPDIR=…/tmp python3 recipe.py`, wall time 96.99 s, exit 0.

## Controls

```
mutant=control-satisfied(unmutated) rejected=0
  gates: L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1  exit=0
c1-gate fixed=7/7 exit=0
mutant=do-nothing(tree=base) rejected=1
  gates: L1=0 L2=0 L3=0 L4=0 L5=0 L6=0 L7=1  exit=1
```

The satisfied fixture passes all seven limbs and the do-nothing tree is rejected, so the probe discriminates.

## Survivors (rejected=0): six of ten mutants are accepted

**S1 — `mutant=M1-selfanchor-symlink-normalized-token rejected=0`.** Self-verification through a symlinked directory.
- Attacked: `check_row` line 110 (`rel == entry_rel`, a string compare) and line 113 (`os.path.islink` checks only the final component; `realpath` stays inside the root). Docstring lines 24–26 promise "every anchor a regular non-symlink file … (never the entry itself)".
- Exact edit, `corpus/knowledge/claim-gates.md`, row G5:
  `| G5 | The check reads current bytes and does not establish tracking. | \`corpus/instruments/anchorcheck.py:45\` | \`the check reads current bytes\` |`
  → `| G5 | The check reads current bytes and does not establish tracking. | \`corpus/instruments/kdir/claim-gates.md:127\` | \`entry's own text is the anchor\` |`
  (line 127 = the probe line; its apostrophe is U+2019, so the ASCII token matches only after `norm()`).
- Printed: `gates: L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1  exit=0`; per-entry on the same tree: `row G5 ok=1 read=token-located` and `reground entry=claim-gates.md rows=6 ok=6 files=3 exit=0`.
- Why it survives: L6 blanks only the raw token, so the normalised match is not removed from the anchor line; the row is then "killed" by erasing the entry's own probe line. L6 therefore reports this self-anchor as load-bearing.

**S2 — `mutant=M2-alias-path-counted-distinct rejected=0`.** The "≥2 distinct anchor files" rule counts strings, not files (`files.add(f)` line 142, `len(files) >= 2` line 143).
- Exact edit, `claim-gates.md` row G6: `corpus/instruments/recheck-audit.py:1` → `corpus/instruments/./anchorcheck.py:1` (token `python3`, present in both).
- Printed: `reground entry=claim-gates.md rows=6 ok=6 files=2 exit=0`. Real distinct anchor files: 1.

**S3 — `mutant=M5-indented-row-hidden rejected=0`.** The row parser drops any row with leading whitespace (`section_rows` line 96, `^\|\s*G\d+\s*\|`).
- Exact edit, `claim-gates.md`: appended after G6 a line `  | G7 | Fabricated claim with no anchor. | \`corpus/instruments/anchorcheck.py:45\` | \`this phrase is absent from the file\` |`
- Printed: `reground entry=claim-gates.md rows=6 ok=6 files=2 exit=0` for a seven-row table; the G7 token is absent from the anchor file.
- [INFERENCE] CommonMark/GFM allow up to three leading spaces before a table row, so this would render as a row. I did not render it.

**S4 — `mutant=M7-dash-divider-token rejected=0`.** The token rule (`len(tok) < 6`, line 115) accepts a comment divider as evidence.
- Exact edit, `claim-package-contract.md` row G5: `corpus/instruments/freeze-check.py:12` / `freeze-check.py --claims PATH` → `corpus/instruments/anchorcheck.py:206` / `------` (line 206 is `# ---- round-29 selftest: one isolating fixture per fail limb ----…`).
- Printed: `reground entry=claim-package-contract.md rows=6 ok=6 files=3 exit=0`; `row G5 ok=1 read=token-located`.

**S5 — `mutant=M8-claim-text-unbound rejected=0`.** The claim column is never read. `check_row` uses only `row[2]` and `row[3]`; `entry_mode` uses only `r[0]`.
- Exact edit, `claim-package-contract.md` row G1: claim `The counter replays each claim against the frozen base.` → `The gate verdict is always green, unconditionally.`; anchor and token unchanged.
- Printed: `row G1 ok=1 read=token-located`; `gates: … L7=1  exit=0`.

**S6 — `mutant=M3-L7-trailing-space rejected=0`.** L7 compares `.strip()`ed recheck text (`recheck_line` line 82; L7 line 238), while the docstring (line 36) promises "byte-identical".
- Exact edit, still-gated `citation-bases.md`: its `recheck:` line + two trailing spaces.
- Printed: `gate L7 pass=1 read=still-gated=22 changed=none`; `rejected=0`.

## Controls that are caught (rejected=1)

- **M4-L7-command-comment**: `citation-bases.md` recheck line + ` # relaxed`. Printed `gate L7 pass=0 read=still-gated=22 changed=citation-bases.md`, `rejected=1`.
- **M9-token-five-chars**: G1 token `replay a kasegi-round-claims-v2 file` → `repla`. Per-entry: `row G1 ok=0 read=token-or-range-bad`, `exit=1`, `rejected=1`.
- **M10-range-41-lines**: G1 anchor `anchorcheck.py:29` → `anchorcheck.py:29-69`. Per-entry: `row G1 ok=0 read=token-or-range-bad`, `exit=1`, `rejected=1`.
- **M6-L6-token-absent**: G2 token `LOST-RECORDED stays recorded-not-fail` → `…recorded-not-passed`. Per-entry: `row G2 ok=0 read=token-not-in-lines`; gate `L6 pass=1 read=mutants=6 survivors=none`. L6 is silent here: once the entry is red, every blank "kills" every row. The rejection comes from L4, L1, L2 and L7, not from L6.
- **D1-selfanchor-symlink-raw-token** (diagnostic, not counted): same self-anchor as M1 but with a raw-identical token (`custodian-receipts.json`, line 10). Printed `rejected=1`, `gate L6 pass=0 read=mutants=12 survivors=claim-gates.md:G5`, while per-entry is green (`row G5 ok=1 read=token-located`, `exit=0`). The rejection is right for the wrong reason. The raw blank rewrites the row's own token cell as well as line 10, so the row still matches after blanking and L6 flags it. `check_row` does not reject it.

## Full summary (final run, verbatim)

```
M1-selfanchor-symlink-normalized-token rejected=0 expected=survive MATCH
M2-alias-path-counted-distinct rejected=0 expected=survive MATCH
M3-L7-trailing-space rejected=0 expected=survive MATCH
M5-indented-row-hidden rejected=0 expected=survive MATCH
M7-dash-divider-token rejected=0 expected=survive MATCH
M8-claim-text-unbound rejected=0 expected=survive MATCH
M10-range-41-lines rejected=1 expected=reject MATCH
M4-L7-command-comment rejected=1 expected=reject MATCH
M6-L6-token-absent rejected=1 expected=reject MATCH
M9-token-five-chars rejected=1 expected=reject MATCH
D1-selfanchor-symlink-raw-token rejected=1 (diagnostic, not counted)
controls: satisfied rejected=0 (want 0); do-nothing rejected=1 (want 1)
survivors=6 of 10 mutants
```

Earlier runs of the same recipe (v1, v2) gave the same result for every shared mutant (M2, M3, M5, M7, M8 survived in both). v2 introduced the normalised self-anchor (M1); v3 added the per-entry probe output quoted above.

## Limitations

- The fixture is hand-built on the pure base export, not the live lane. The probe line (claim-gates.md:127) was added to the control, because neither entry currently contains a curly quote or double space (grep found none). In the live lane, S1 needs one body line with such a character, which is a single-line authoring step.
- `rejected` is the whole-gate exit status. Limb-level evidence is the `gates:` line and the per-entry `row` output quoted above.
- Not tested: L6 on rows of entries that are not regrounded (L6 iterates `reg` only, line 205); a second `recheck:` line in a still-gated entry (`recheck_line` reads the first match only, lines 79–82); L3/L5 variants; side effects of the lane's own recheck commands (classify runs 64 of them).
- Survivors are demonstrated on the fixture only. Each survivor is a fixed defect class, not a claim about the C1 lane's current entries.
- Not done: the F28 entry and the C1 re-grounds, which are milestone items outside this seat's single item (C1 mutation probe).
- Tools: none installed; python3 3.14.8 standard library only. Nothing committed, pushed, or mutated in git; no lane file written.
