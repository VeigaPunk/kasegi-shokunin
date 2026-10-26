# ScribeProvinceF22 — round-39 receipt

Seat: ScribeProvinceF22 (scribe, leaf) · role: province amendment scribe · axes touched: coverage (C2 F22)
Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin · lane HEAD at drafting: `d65d823e7c84813c192b20ee757a8761f878a61f` ("round-39: wave1 spec/dispatch")
Base: `480b1a505a2dfc14a4f718d16d63808247214d0a` · claims freeze: `dcd31701720a6a4929a32471a62011ed87103421`
Dispatch provenance: `git log --oneline -8` shows `480b1a5` is an ancestor of HEAD (`git merge-base --is-ancestor` → true) and `dcd3170` is a commit object (`git cat-file -t` → `commit`), matching the frozen round.

## Item

Draft the PROVINCE.md frontier amendment line for F22 as a deliverable-only file, one line, R6 end-of-file append per precedent, for the L1 to land. Deliverable only — no lane file was edited.

## Behavior

Wrote exactly one line to the deliverable, byte-identical to the mandate carried in the L1's own seat spec (`wave1-spec.json`, seat `ScribeProvinceF22`), and validated by simulating the append on a scratch copy of PROVINCE.md.

- Deliverable: `.ufo/waves/round-39/wave1/ScribeProvinceF22.province.append.md`
- Line count: **1** (single line, LF-terminated, no blank line, no fence, no heading)
- Bytes: **262** (257 characters + `\n`)
- sha256 (file): `bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d`
- sha256 (line text, no newline): `780e33c82498fde9a6cfcfeea039923a2fec881d81b25e91c9a615b912a6f883`
- Expected final PROVINCE.md line count after the L1's append: **156 + 1 = 157**

## Gates — commands and actual output

`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` — green before any work:
```
root                             use%     free
/fast/scratch/hyaku               25%   610.1G
```
No heavy pass was run (single-line deliverable; no export, no build).

Baseline of the target file (unmodified before and after this seat):
```
$ wc -l PROVINCE.md
156 PROVINCE.md
$ sha256sum PROVINCE.md
030be330a9989202165f743c8565360b8221159e465729da449e613bb78f8dea  PROVINCE.md
$ awk 'END{print NR}' orig.md        # copied to scratch
156
$ tail -c1 orig.md                   # end-of-file state
trailing newline present
```
Last existing line is the round-38 amendment (`F21 — OASIS CSAF v2.0 …`, L156); the r39 line therefore appends at L157.

Deliverable shape:
```
$ wc -l -c ScribeProvinceF22.province.append.md
  1 262 ScribeProvinceF22.province.append.md
$ sha256sum ScribeProvinceF22.province.append.md
bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d  …province.append.md
$ grep -c '[^[:space:]]' <deliverable>
1
$ tail -c1 <deliverable> | od -An -c
  \n
$ grep -c '```\|~~~' <deliverable> ; grep -cE '^#' <deliverable> ; grep -c '^|' <deliverable>
0
0
0
```

Byte-exactness against the spec mandate (`spec==deliverable: True`), non-ASCII audit:
```
bytes: 262
byte-identical to mandated text: True
chars: 258 em_dashes: 2 non_ascii: ['—']
backticks: 0
sha256: bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d
line_length_chars: 257
spec sha256(line): 780e33c82498fde9a6cfcfeea039923a2fec881d81b25e91c9a615b912a6f883
deliv sha256(line): 780e33c82498fde9a6cfcfeea039923a2fec881d81b25e91c9a615b912a6f883
```

Simulated R6 append on a scratch copy (`new.md` = `orig.md` + deliverable), which is exactly what the L1's append must produce:
```
lines: 157                # expected: 157
diff orig.md new.md | grep -c '^<'   -> 0        # pure addition, zero deletions
diff orig.md new.md | grep -c '^>'   -> 1        # exactly one added line
tail -n 1 new.md == deliverable line -> IDENTICAL
^\[r37 Frontier amendment -> 1
^\[r38 Frontier amendment -> 1
^\[r39 Frontier amendment -> 1
F22 occurrences in new.md -> 1
sha256sum new.md -> 5a5b70dabdc0e56ec135c665a09cc934829954c7b3d191dbdcc253b41320d692
```
Pre-append the lane carried zero `F22` and zero `r39` markers (`grep -c` → `0` each), so the append introduces exactly one new frontier line and cannot duplicate an existing amendment.

## Touched surfaces

- Wrote: `.ufo/waves/round-39/wave1/ScribeProvinceF22.province.append.md` (deliverable) and this receipt `.ufo/waves/round-39/wave1/ScribeProvinceF22.md`.
- Scratch: `/fast/scratch/hyaku/kasegi-r39/ScribeProvinceF22/` (created, used for baseline copy + append simulation, removed before yield).
- Not touched: `PROVINCE.md` (sha unchanged `030be330…`), `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`, any `.ufo/waves/round-39/` file other than my two outputs, fleet root, `shokuknow`.
- Git: read-only only (`log`, `ls-tree`, `merge-base`, `cat-file`, `status`). No add/commit/checkout/reset/stash, no jj.
- Tooling: no installs, no upgrades, no network fetches (nothing was needed; all inputs local). No PATH writes.

## Findings

1. **F-1 (conditional deliverable).** At drafting HEAD `d65d823`, the artifacts the amendment line references do not exist yet, because they are C2's to land at J:
   - `corpus/knowledge/cisa-when-to-issue-vex.md` → `ls` fails, `git ls-tree -r --name-only HEAD | grep -c cisa-when-to-issue-vex` → `0`; `corpus/knowledge` at HEAD holds 50 files (frozen before-state).
   - `corpus/README.md` frontier rows → `grep -cE '^\| F[0-9]+ \|'` → `21` (frozen before 21; target 22).
   - `corpus/SOURCES.md` → `S057` rows `0`, `S056/S058/S059` rows `0` (registry at the frozen before-state, 55 rows).
   - `corpus/source-snapshots/round-39/` → absent.
   The line must therefore be landed **only together with C2's landed artifacts**; if C2 is rejected at integration, this line must not be appended. This receipt is a draft, not evidence that F22 is admitted.
2. **F-2 (formatting delta, cosmetic).** Precedent lines F19 (L78), F20 (L80), F21 (L156) each carry exactly 2 backticks (the entry path is wrapped in a code span). The mandated r39 line carries **0** backticks (`backticks: 0`, confirmed against the spec bytes). I delivered the mandated bytes verbatim rather than adding backticks. If the L1 wants precedent styling at landing, wrapping `corpus/knowledge/cisa-when-to-issue-vex.md` in backticks changes the line to 259 characters and the file sha256 to something other than `bd8dbc09…`; the mandated text itself should otherwise stay untouched.
3. **F-3 (wording condensation is mandated, not paraphrase).** The frozen C2 predicate describes "the issuance, lifecycle, timestamp-reaffirmation and upstream-inheritance layer of VEX publishing"; the amendment line says "(VEX issuance/lifecycle/reaffirmation/inheritance guidance)". The shorter form is the L1's mandated line text (`spec==deliverable: True`), so it is not a scribe edit — recorded here so a reviewer comparing line vs claim sees the difference is intentional.
4. **F-4 (D-A discipline).** The deliverable contains no fences, headings, tables, notes or validation text (all four counters `0`); every validation artifact in this receipt lives outside the deliverable.
5. **F-5 (append safety).** Appending at EOF does not disturb the round-38 correction line at L154 (which declares the r37 scaffolding at L81–L152 as not part of the province) or any count line: after the simulated append the r37/r38/r39 amendment prefixes each match exactly once, and total lines are 157 as expected.
6. **F-6 (scratch state at my yield).** `/fast/scratch/hyaku/kasegi-r39/ScribeProvinceF22` is removed (`ls` → "No such file or directory"). At 16:31 UTC the shared `/fast/scratch/hyaku/kasegi-r39/` still held 44 live sibling seat dirs (e.g. `ExecScoreGap`, `ScribeFrontierF22`, `CritDesignReview`), i.e. peers were still running when this seat finished. G6 must therefore be evaluated after the wave drains, not from this snapshot; this seat contributes no surviving entry.

## Out of scope

Registry rows S057/S056/S058/S059, the knowledge entry, the `corpus/README.md` frontier row and count line, the S057 capture/manifest, harness/binding/audit/census counting, the C1 suite and all-gates receipt, lesson/LOG/SCORECARD updates, and the commit itself. No `Final lane commit:` line was produced; judged head J is named by reference only.

## Artifacts

- Deliverable: `.ufo/waves/round-39/wave1/ScribeProvinceF22.province.append.md` — 1 line, 262 bytes, sha256 `bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d`
- Receipt: `.ufo/waves/round-39/wave1/ScribeProvinceF22.md` (this file)

## CLAIMS

```
artifact=.ufo/waves/round-39/wave1/ScribeProvinceF22.province.append.md lines=1 bytes=262 sha256=bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d
province_baseline_lines=156 province_baseline_sha256=030be330a9989202165f743c8565360b8221159e465729da449e613bb78f8dea
expected_final_lines=157 simulated_append_lines=157 simulated_deletions=0 simulated_additions=1 simulated_sha256=5a5b70dabdc0e56ec135c665a09cc934829954c7b3d191dbdcc253b41320d692
spec_byte_identical=true spec_line_sha256=780e33c82498fde9a6cfcfeea039923a2fec881d81b25e91c9a615b912a6f883 backticks=0 em_dashes=2
lane_edits=0 scratch_removed=true network_fetches=0 tool_installs=0
```
