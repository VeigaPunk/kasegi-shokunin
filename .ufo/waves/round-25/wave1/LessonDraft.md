# LessonDraft — round-25 § Mistakes + § Gate draft (kasegi, wave 1)

Seat: `L1Kasegi25.LessonDraft` (scribe). Lane `kasegi-shokunin`, base revision
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Written 2026-10-25.
Mode: read-only outside my two owned paths. No commit, no push, no VCS write, no background
job, no subagent, no tool install (nothing was needed; no `pacman`/`uv`/`npx` transaction ran).

## Behavior

I drafted the two sections the L1 needs for `corpus/lessons/round-25.md` and wrote them as a
draft, not as product prose:

- `.ufo/waves/round-25/wave1/lesson-mistakes.md` — `## Mistakes` (M25-1 … M25-4),
  `## Gate` (5 admit rows S036–S040 + 1 reject with failing criteria and flip condition),
  `## Fixes that can fail` (5 fixes, each with its control).
- This report.

Every mistake candidate in the ticket was re-verified by me against committed bytes before
it was written; one candidate was replaced by a stronger, measured variant (see Findings 3),
and the misroot candidate resolved to "none found" with the scan recorded as a control.

## Gates (what I actually ran)

| Gate | Command | Observed |
|---|---|---|
| committed-bytes basis | `git archive HEAD corpus \| tar -x -C /tmp/kasegi-head-25` at HEAD `b49948f` | extraction used for every "committed bytes" number |
| parse limb, HEAD | per-file `bash -n` on each of the 35 `recheck:` values from `/tmp/kasegi-head-25` | `recheck_lines 35 parse_fail 23`; leading-token census of the failing set `{'on-restoration': 23}` |
| cwd limb, HEAD | each parse-OK value run with `cwd=/tmp/kasegi-head-25` and `cwd=/`, comparing exit status **and** sha256 of combined stdout+stderr | `cwd_diff 6`, `same_both_cwds 6` (the six named in the draft) |
| independent reproduction of the frozen counter | my own two-limb run above vs `.ufo/waves/round-25/c1-before.txt` | identical totals: `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` |
| cd-prefix census | `grep -h '^recheck: cd ' corpus/knowledge/*.md \| wc -l` | `5` (files: `authorised-testing-rules-of-engagement`, `cna-assignment-and-vulnerability-rules`, `cra-manufacturer-reporting-duties`, `multiparty-vulnerability-coordination`, `statutory-authorization-and-unauthorized-access`) |
| legacy-set cross-tab | files containing `## Provenance (round-22 correction, appended)` (25) vs the 23 parse-fail files | 23 of 23 parse-fail files are legacy; 25 legacy blocks in total |
| D24-5 quoted verbatim | `grep -n 'D24-5' corpus/lessons/round-24-verifier-spotcheck.md` | line 208, text quoted in the draft |
| count divergence at HEAD | manifest self-count vs the three prose copies | manifest `19 76`; README `:174` "62"; SCORECARD `:510` "77"; lesson `:77` "77"; report `:31` "76" |
| mutant claim at HEAD | `ResolverAttack.md` M4 row vs the four restatements | M4 measured "4/8, identical receipt" on baseline `690153ad…`; restatements at README `:159`, SCORECARD `:500`, QUALITY `:65`, report `:159`/`:227` |
| no mutant of landed bytes | `grep -rl db5e0767`, `ls .ufo/waves/round-24/wave2/` | only fixed-resolver receipts, README, lessons, spotcheck; wave2 holds `swarm-registry.json` only |
| quote occurrence, 5 captures | `grep -Fo '<quote>' S0NN.txt \| wc -l` in `corpus/source-snapshots/round-25/` | 1, 1, 1, 1, 1 (S036:30, S037:109, S038:17, S039:519, S040:58); each quote also present verbatim in the draft (`q in draft` = True for all five, plus the S038 line-20 half-sentence) |
| capture integrity | `sha256sum` + `wc -c` on the five snapshots vs the log's instrument output | byte counts and sha256 match for S036–S040 |
| frontier state at HEAD | `git show HEAD:corpus/README.md` parsed by row | admitted rows = 9 (F01–F09); `F10` rows = 0; `F20` rows = 0 |
| staged-row identity | S068 row URL vs capture-log S040 URL | byte-identical Cisco URL; `S068` occurrences in `HEAD:corpus/SOURCES.md` = 0 |
| reject criterion 1 | `bash -n` on the crosswalk's `recheck:` value (staged line 6) | exit 2, `syntax error near unexpected token '('` |
| misroot, first scan | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | 22 entries, all driver/operator state |
| misroot, final scan (after my writes) | same command | 23 entries; the addition is `?? .ufo/reports/round-44/mori.md` (mori lane's round-44 report) |

## Touched surfaces

- Written by me: `.ufo/waves/round-25/wave1/lesson-mistakes.md` (draft) and this report.
- Read only: `corpus/knowledge/*.md` (HEAD bytes + live tree), `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `corpus/lessons/round-24.md`,
  `corpus/lessons/round-24-verifier-spotcheck.md`, `corpus/instruments/README.md`,
  `corpus/source-snapshots/round-24/manifest.json`, `corpus/source-snapshots/round-25/*.txt`,
  `.ufo/waves/round-24/wave1/ResolverAttack.md`, `.ufo/waves/round-25/{claims.json,capture-log.txt,c1-before.txt,c1-instrument-digest.txt,assimilation/ids/*}`,
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md`,
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/**` (READ-ONLY, nothing executed there).
- No production file, judge, contract, or VCS state was modified.

## Out of scope / left to the L1

- Composing `corpus/lessons/round-25.md`; the draft's `## Gate` rows carry `L1 to fill:
  tier / status / recheck command / used-by` markers on purpose — I did not invent registry
  field values.
- The C1 fix itself and its counter run (`recheck-audit.py` is another seat's instrument; I
  reproduced its before-verdict with my own two-limb script instead of re-running it).
- The S040/S068 single-owner decision, and whether the Cisco row is admitted (see Conflict).

## Findings

1. **The ticket's first candidate is confirmed, and its captured-by is sharper than stated.**
   23 of 35 `recheck:` values begin with the token `on-restoration` and fail `bash -n` on
   committed bytes; the 23 are a subset of the 25 legacy entries. Q7 exists at
   `corpus/QUALITY.md:48` (HEAD) and was written for new entries. The stronger capture is
   `SCORECARD.md:327` (HEAD), which asserts "`recheck:` lines runnable **0/25 → 25/25**" — a
   self-description (R2) that no command backed, because running the field as written is a
   parse error, not the "exit 1, base absent" the row claims.
2. **The ticket's D24-5 candidate is confirmed with a corrected count.** D24-5 implies 30
   non-prefixed lines are cwd-dependent. Measured: 5 prefixed + 23 unparseable + 6
   cwd-dependent + 1 cwd-stable-unprefixed (`root-loss-2026-10-12`, `test ! -e ~/...`). So
   non-conforming = 29, and the 23 are a different class (never runs) from the 6.
3. **The ticket's third candidate needed the HEAD-bytes reading, because the live tree is
   already fixed.** At HEAD: README says 62 assertions, SCORECARD and the round-24 lesson say
   77, the manifest measures 76, the report says 76, and no counting command sits beside the
   lane numbers. In the live tree a seat has already replaced the README figure with 76 and
   added the command — that is a live-tree change, not a committed-bytes fact, and I recorded
   both sides rather than reporting the fix as the before state.
4. **The live tree is a moving target.** Two consecutive runs of the same per-file `bash -n`
   loop gave `parse_fail 23` (start of work) and then `parse_fail 0` minutes later, because
   wave-1 seats landed the `cd … &&` + `#` comment rewrite in between. All "before" numbers
   in the draft therefore come from `git archive HEAD`, and the fix shape is cited as a live
   diff, not as a completed fix.
5. **The round-25 captures are internally consistent.** The five snapshot sha256 and byte
   counts match `capture-log.txt` verbatim, and each of my five chosen quotes occurs exactly
   once in its capture. Japanese quotes are reported by character count, not by a whitespace
   word count that would be a tokenizer artefact.
6. **Misroot: none attributable to a kasegi round-25 seat.** The fleet-root status holds
   driver/operator state; a transient 23rd entry mid-work was a sibling lane's report
   (`.ufo/reports/round-44/mori.md`) in the intended report directory, which that lane then
   committed at `86166ec7`, returning the status to the same 22 entries. `.scratch/goal-…md`
   self-declares orchestrator ownership and its mtime (05:23:08) is after the lane dispatch.

7. **Two live-tree entries overlap under the same frontier row.** While I worked, two
   untracked entries appeared for the same set:
   `vendor-disclosure-policies-as-corpus-objects.md` (sources S036–S039) and
   `vendor-disclosure-policy-commitments-crosswalk.md` (S036, S038, S039, S040), both
   `ground: F10`, overlap 3 ids. Both recheck lines are `cd`-prefixed and their `--source`
   selections cover their header ids (R12 shape), and both name
   `corpus/source-snapshots/round-25/manifest.json`, which exists (5 records, 33 quotes,
   ids S036–S040). The draft records the overlap as a decision for the L1 rather than
   resolving it, because one object per document set is the L1's call.

## Conflict reported verbatim (for the canonical judge)

`claims.json` → `assimilation.planned_reject`:
`"vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy unreachable this round)"`.

`capture-log.txt` →
`S040 status=200 fetched_bytes=94027 snapshot_bytes=33463 sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c utc=2026-10-25T08:14:28Z out=corpus/source-snapshots/round-25/S040.txt`,
and the file at that path hashes to that sha256 (my `sha256sum`). The reachability ground for
the planned reject is contradicted by committed bytes; the draft's reject block therefore
stands on three criteria I measured directly (Q7 parse failure, `ground: F20` absent from the
frontier table, and S068 being the same document as S040), and says so.

## Artifact paths

- Draft: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/wave1/lesson-mistakes.md`
- This report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/wave1/LessonDraft.md`
- Committed-bytes extraction used for measurement (outside the repo):
  `/tmp/kasegi-head-25/` (from `git archive HEAD corpus`)

## Checks the L1 should run after composition

1. `grep -c '^recheck: on-restoration' corpus/knowledge/*.md` → 0 on the composed tree, and
   the frozen counter prints `lines=35 pass=35 exit=0`.
2. `python3 -c "import json;m=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in m['sources']))"` → one number, and that number appears in `corpus/instruments/README.md`, `SCORECARD.md` and `corpus/lessons/round-24.md` with the command adjacent.
3. `grep -n '62 assertions\|77 assertions'` over those three files → 0 hits.
4. `git -C /home/vgpnk/Projects/shokunin status --porcelain` at round close → only
   driver/operator paths; any lane artefact there is the fail signal.
5. Re-run my quote check on the composed lesson:
   `cd corpus/source-snapshots/round-25 && grep -Fo '<each gate quote>' S0NN.txt | wc -l` → 1.

## Known limits

- Authorship of fleet-root files is inferred from content and mtime; the fleet root keeps no
  per-file write log for untracked files.
- The cwd leg was run from the `git archive` extraction rather than the lane root, because
  the lane root was mid-edit; the extraction contains the same committed bytes, but a
  path-dependent command that resolved against untracked live files would read differently
  there. No line in the measured set named an untracked path.
- I did not re-run `corpus/instruments/recheck-audit.py` (another seat owns the C1 counter);
  my reproduction is an independent two-limb script, and it agrees with the frozen receipt on
  the totals.
