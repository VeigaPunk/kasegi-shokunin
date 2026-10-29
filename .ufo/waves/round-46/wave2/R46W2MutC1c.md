VERDICT: BROKEN

# R46W2MutC1c — C1 counter `corpus/instruments/r46-c1-gate.py` (v1.1), limbs L6-L7, row parser `section_rows`/`check_row`

Scope: mutation test of the committed tip 5437afeaf9b642c267bba3c31f00ae701e49da68 (export copy, lane instruments, aggregate `--baseline` = pure base export 914ca0b6). Twelve single-edit mutants plus three controls. The counter and the lane were not edited. Nothing was committed. No tool was installed.

## Method

- Tip export extracted with `git archive 5437afeaf9b642c267bba3c31f00ae701e49da68` into a scratch dir. Each mutant is a `cp -al` hard-link copy of that tree with exactly one file replaced through a new inode (no write through the link).
- Grading command for every case (counter run from the lane path, so its instruments are the lane's):
  `TMPDIR=<scratch>/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --root <case> --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/work`
- `rejected` = aggregate exit != 0. Per-entry mode (`--entry corpus/knowledge/<e>.md --root <case>`) is printed too.
- Base export and tip tree hashed before and after the run (tree-hash, symlinks skipped): tip `b9e8a8680e7ffdb1` before and after; base `6cd1c401edd5a2f1` before and after. Base unchanged.

## Do-nothing control (must be accepted)

```
mutant=ctl-do-nothing-tip rejected=0 expected=0 aggregate-exit=0 failing=none
   gate L1 pass=1 read=gated=22 broken=0 lines=65/base=64
   gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
   gate L3 pass=1 read=recheck-lines-exact=2
   gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
   gate L5 pass=1 read=append-only-restoration-kept=2
   gate L6 pass=1 read=mutants=46 survivors=none
   gate L7 pass=1 read=still-gated=22 changed=none
   c1-gate fixed=7/7 exit=0
```

## SURVIVORS (rejected=0 while the defect is present) — listed first

The printed survivor lines, verbatim from the run:

```
mutant=m05-trivial-token-hyphens rejected=0 defect=generic 8-char token (a comment rule) grounds an unrelated row
mutant=m06-section-in-code-fence rejected=0 defect=fence handling: whole Re-ground section inside a code fence (not rendered as a table)
mutant=m07-section-in-html-comment rejected=0 defect=comment handling: whole Re-ground section inside an HTML comment (not rendered)
mutant=m09-lowercase-id-hidden-row rejected=0 defect=row parser: a table row whose id is not `G<digits>` is never read or checked
mutant=m11-L7-crlf-of-still-gated rejected=0 defect=L7 claims byte-identical; text-mode read hides CRLF/LF conversion
```

### S1 — m11: CRLF conversion of a still-gated entry passes L7 (defect: L7 is not byte-identical)
- Edit (tip -> mutant): every `\n` of `corpus/knowledge/citation-bases.md` (a base-gated, still-gated entry, 126 lines) replaced by `\r\n`. Nothing else.
- Printed: `mutant=m11-L7-crlf-of-still-gated rejected=0 expected=1 aggregate-exit=0 failing=none`; `gate L7 pass=1 read=still-gated=22 changed=none`; `c1-gate fixed=7/7 exit=0`.
- Evidence the defect is present (command run): `sha256sum tip/.../citation-bases.md mut/.../citation-bases.md` printed `2eda5eab…fc1da8` and `11de8124…4bb5`; `grep -c $'\r'` printed `tip=0 mut=126`; Python text-mode read vs byte compare printed `text-mode read equal: True | bytes equal: False`.
- Cause (code read, lines of `r46-c1-gate.py`): `read()` opens with `open(path, "r", encoding="utf-8")` (line 102), so universal newlines hide `\r\n` vs `\n`; L7 compares `read()` outputs (line 305). The byte-identity sentence in L7 is therefore not what the code does.
- Same blindness reaches L4 by code reading only (not run): L4 compares anchors with `read(bp) == read(tp)` (line 244), so a CRLF change to an anchored file would also pass there.

### S2 — m09: a row whose id is lowercase is silently never read (defect: row parser skips it)
- Edit: after the G25 row of `corpus/knowledge/claim-gates.md` insert `| g26 | probe: lowercase id, absent token | \`corpus/instruments/claim-package-check.py:1-5\` | \`zzz_absent_token_probe\` |`.
- Printed: `mutant=m09-lowercase-id-hidden-row rejected=0 expected=1 aggregate-exit=0 failing=none`; `per-entry exit=0`; `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0` (the file has 26 table rows; the parser reports 25).
- Cause: row regex `^\|\s*G\d+\s*\|` (line 126) is case-sensitive and needs a capital G followed by digits.
- Discriminating control `ctl-uppercase-bogus-row` (identical row, id `G26`): `mutant=ctl-uppercase-bogus-row rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7`; `row G26 ok=0 read=token-not-in-lines`; `reground entry=claim-gates.md rows=26 ok=25`. So the only difference is the id regex, and the rejection is real once the row is read.

### S3 — m06: whole Re-ground section inside a fenced code block still counts (defect: section not rendered)
- Edit: a line ```` ```markdown ```` inserted before `## Re-ground (round 46)` (claim-gates.md line 128) and a line ```` ``` ```` inserted after row G25 (new line 160). Nothing else.
- Printed: `mutant=m06-section-in-code-fence rejected=0 expected=1 aggregate-exit=0 failing=none`; `per-entry exit=0`; `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`.
- Cause: `section_rows` matches the heading by `ln.strip() == SECTION` (line 119) and reads rows until the next `#` heading (lines 122-127); no fence state is tracked.

### S4 — m07: whole Re-ground section inside an HTML comment still counts
- Edit: a line `<!--` before the heading (new line 128) and `-->` after row G25 (new line 160).
- Printed: `mutant=m07-section-in-html-comment rejected=0 expected=1 aggregate-exit=0 failing=none`; `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`.
- Cause: same as S3; no comment state is tracked in `section_rows`.

### S5 — m05: a generic 8-char token (a comment rule) grounds an unrelated row (defect: specificity; the counter checks only a length floor)
- Edit: row G1 of `claim-gates.md` changed from anchor `corpus/instruments/claim-package-check.py:101-108` + token `'custodian-receipts.json',` to anchor `corpus/instruments/claim-package-check.py:299-301` + token `--------`. Line 300 of that file is `# ---- R-MANIFEST ----…`.
- Printed: `mutant=m05-trivial-token-hyphens rejected=0 expected=1 aggregate-exit=0 failing=none`; `gate L6 pass=1 read=mutants=46 survivors=none`; `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`.
- Discriminating control `ctl-token-8-hyphens-off-range` (same token `--------`, anchor `:101-108` where no hyphen run exists): `mutant=ctl-token-8-hyphens-off-range rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7`; `row G1 ok=0 read=token-not-in-lines`. So the survival is about where the token sits, and the length check (line 145) does not judge whether the token is specific.
- Note: the 8-char floor is the stated rule (`MIN_TOKEN = 8`), so this is a gap between the rule and the defect it is meant to prevent, not a broken check. It belongs to the non-author reading, which the C1 kill rule already assigns.

## REJECTED mutants (7 of 12 rejected; attribution as printed)

```
mutant=m01-dup-row-same-anchor-token rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   reground entry=claim-gates.md rows=26 ok=26 files=3 distinct=0 exit=1
mutant=m02-same-range-other-token rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   reground entry=claim-gates.md rows=26 ok=26 files=3 distinct=0 exit=1
mutant=m03-token-7-chars rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   row G1 ok=0 read=token-or-range-bad
   reground entry=claim-gates.md rows=25 ok=24 files=3 distinct=1 exit=1
mutant=m04-range-41-lines rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   row G1 ok=0 read=token-or-range-bad
   reground entry=claim-gates.md rows=25 ok=24 files=3 distinct=1 exit=1
mutant=m08-second-heading-in-fence rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=2
mutant=m10-L7-prose-edit-of-still-gated rejected=1 expected=1 aggregate-exit=1 failing=L7
   gate L7 pass=0 read=still-gated=22 changed=citation-bases.md
mutant=m12-dup-id-distinct-range rejected=1 expected=1 aggregate-exit=1 failing=L1,L2,L7
   reground entry=claim-gates.md rows=26 ok=26 files=3 distinct=1 exit=1
```

Edits: m01 duplicate of G1 as G26 (same anchor and token); m02 G26 on the G1 range with token `'provenance.json',`; m03 G1 token `'custodian-receipts.json',` -> `'report` (7 chars); m04 G1 anchor `:101-108` -> `:101-141`; m08 a second copy of the heading appended at EOF inside a fence; m10 one prose line appended to still-gated `citation-bases.md`; m12 G7 duplicate id on a fresh range `:300-310` with token `manifest.get('schema_version')`.

Attribution: m03/m04 are rejected by the per-entry token/range check (line 145); m08 by `section-count` (line 119-120); m10 by L7 alone; m01/m02 by the `distinct` check (line 177); m12 by elimination, since the per-entry line shows `ok=26 distinct=1` and only the id-uniqueness conjunct (line 178) is left failing.

**Observation (cascade):** for m01-m04, m12 and the two controls, the entry's own recheck goes red, so the entry leaves the re-grounded set R; L2 then fails, and L1 and L7 follow. L6 is the rejecting limb for none of the 12 mutants. The rejections are right, but the aggregate's diagnosis for a row-level defect is "L1,L2,L7", not the row-level limb.

## Supplementary probe (not one of the 12): L6 rejects an honest row

- Edit: row G26 `| G26 | probe: token wrapped across lines 69-70 and raw at 72 | \`corpus/instruments/README.md:69-93\` | \`file mean\` |` after G25 of claim-gates.md. README lines 69-70 wrap `file` / `mean`; line 72 contains `file mean` raw.
- Printed: `mutant=s1-L6-wrapped-duplicate-token rejected=1 aggregate-exit=1 failing=L6`; `gate L6 pass=0 read=mutants=47 survivors=claim-gates.md:G26`; `per-entry exit=0`; `reground entry=claim-gates.md rows=26 ok=26 files=4 distinct=1 exit=0`.
- Reading: the row is grounded (per-entry green), yet L6 flags it, because L6 blanks only the raw single-line hit (lines 287-290) and the wrapped copy survives the blanking. L6's sentence ("blanking that row's token inside its anchored lines turns per-entry mode red") is then false for this row. This is a precision defect (honest rows can be rejected), not a survivor.

## Limitations

- 12 mutants, one edit each, chosen to hit the named surfaces. Not exhaustive; no fuzzing; the counter itself was not mutated.
- `rejected` is the aggregate exit code. Limb attribution comes from the printed `gate` lines and the per-entry lines, not from separate runs of each limb.
- Each case ran under the grader's inherited HOME/PATH/TMPDIR. The counter's own docstring says a host change moves both readings. Not re-run under another HOME.
- L4's CRLF blindness is from reading lines 102 and 244 only; not executed.
- The base export was read, never written (hash before and after unchanged).
- The 58 symlinks inside the tip export (all under `.ufo/waves/round-25|28|29|31`) were preserved as symlinks by `cp -al`; none sits under `corpus/`.
- Scratch removed on exit. The mutant edits are fully described above; the recipe itself is not committed anywhere.
