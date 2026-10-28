VERDICT: DRAFT-READY

Scope: C1/R2 drafter. Deliverable is a draft only: `.ufo/waves/round-45/wave1/R45ScribeQuality.draft/quality-append.md` (4601 bytes, 1 `## Round-45 additions` heading, header row, rows R47, R48, R49). Nothing was appended to `corpus/QUALITY.md`; no commit, no git mutation, no edit to any tracked file. Installs: none.

## Finding 1 — base hash, size and line count the R6 line cites (measured at draft time)

Commands and printed output:
- `wc -c corpus/QUALITY.md` → `78651 corpus/QUALITY.md`
- `head -c 78651 corpus/QUALITY.md | sha256sum` → `dd753497f7138c395230df48443d3d356ca0d67c3d8a8cd24d9989103dd43d03  -`
- `wc -l corpus/QUALITY.md` → `372 corpus/QUALITY.md`
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat dc5bb8c HEAD -- corpus/QUALITY.md corpus/lessons/round-44.md` → (no output), exit 0; base and HEAD `QUALITY.md` are identical.
- Row lines in base (`grep -n -o '^| R[0-9][0-9] |'`): R22=226 … R38=337, R39=351, R40=352, R41=353, R42=354, R43=369, R44=370, R45=371, R46=372. These are the numbers the R6 paragraph lists.

## Finding 2 — the draft is shaped for the counter's R2 limb, and the limb grades it

Counter: `corpus/instruments/r45-routed-defects.py`, limb R2 (`limb_r2`). Each replay ran `python3 <root>/corpus/instruments/r45-routed-defects.py --root <root> --baseline /fast/scratch/hyaku/kasegi-r45/L1/pure` on a scratch copy of `git archive HEAD` (5242db6), with only `corpus/QUALITY.md` swapped per case.

Controls and draft:
- Do-nothing control (pure base as root, nothing appended): `limb R2 fixed=0 read=quality-not-append-only-or-unchanged`; `routed-defects total=5 fixed=0 unresolved=5 exit=1`.
- Draft appended, `corpus/instruments/freeze-check.py` absent: `limb R2 fixed=0 read=R47-enforced-by-missing-corpus/instruments/freeze-check.py`.
- Draft appended plus a TEST-ONLY stub `freeze-check.py` (a two-line scratch file, not the instrument; used only to test the string match): `limb R2 fixed=1 read=criteria=3`.

Mutants (each one applied to the draft text, stub present; the real draft restored and byte-compared afterwards with `cmp` → identical, 83246 bytes with base):
- M1 `do-nothing` removed everywhere → `limb R2 fixed=0 read=R47-missing-do-nothing`
- M1b `before data` removed (case-insensitive) → `limb R2 fixed=0 read=R47-missing-before data`
- M2 `presence-only` removed → `limb R2 fixed=0 read=R48-missing-presence-only`
- M3 `capture method` → `capture-method` → `limb R2 fixed=0 read=R49-missing-capture method`
- M4 second `## Round-45 additions` heading → `limb R2 fixed=0 read=round-45-heading!=1`
- M5 `|` inserted into the R47 criterion → `limb R2 fixed=0 read=R47-cells=4`
- M6 R49 grounded cell without `corpus/lessons/round-44.md` → `limb R2 fixed=0 read=R49-ungrounded`
- M7 R48 `enforced-by` path typo → `limb R2 fixed=0 read=R48-enforced-by-missing-corpus/instruments/r45-routed-defect.py`
- M8 R48 row renamed to `R48x` → `limb R2 fixed=0 read=R48-rows=0`
- M9 `reject` removed everywhere → `limb R2 fixed=0 read=R49-missing-reject`

Table-shape check of the real draft: `awk` over the three rows printed `| R47  pipes=4`, `| R48  pipes=4`, `| R49  pipes=4` (four pipes = three cells, no `|` inside a cell). `grep -c '^## Round-45 additions'` → `1`. Last byte of the draft is `\n`.

## Finding 3 — each row's content is grounded in the cited bytes (quoted from the files)

R47 (do-nothing replay before data; r44 mine = frozen C2 grep printed 0/0):
- `.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt` prints `base 5ab3a60 stdout:` then `0`, `68`, `62`, then `worktree stdout:` then `0`, `70`, `63`, then `The F-count result is 0 in both states; this is not the 25→26 target.`
- `.ufo/waves/round-44/controls/c2-do-nothing.txt` line 3: `Correct diagnostic counts at base: admitted frontier 25; SOURCES registry rows 68; ...`
- `corpus/lessons/round-44.md:126` (M44-8): the corrected counter is red at base `(frontier rows=25 admitted=25, --expect 26 → exit 1)`.
- `corpus/lessons/round-44.md:15` (M44-3): the frozen regex "prints 0 in base and after".

R48 (presence-only; r44 mines M44-4/M44-7/M44-10 and `wave2/R44W2Rev09.md`):
- `corpus/lessons/round-44.md:189` (M44-10): "accepted a fully fabricated evidence tree (`fixed=8 unresolved=0` with no repair performed) and several presence-only predicates accepted denials, stubs and rewrites."
- `corpus/lessons/round-44.md:16` (M44-4): "accepted marker-only evidence and reported all 8 fixed".
- `corpus/lessons/round-44.md:125` (M44-7): "a prose correction with no committed artifact behind it made the counter print `fixed=8 unresolved=0`".
- `corpus/lessons/round-44.md:167`: "Presence-only predicates accepted denials (D4), filename mentions instead of registry rows (D7), a nonfunctional emitter stub and fabricated seat names (D5), ..." grounded in `wave2/R44W2Rev09.md`; that file exists (71 lines, `.ufo/waves/round-44/wave2/R44W2Rev09.md`).

R49 (capture method for admit and reject; r44 S070 mine):
- `corpus/lessons/round-44.md:131`: S070 "the accessible body is a JavaScript shell and the metadata is a directory welcome with no quotable rule."
- `corpus/lessons/round-44.md:24`: "S069 was fetched 2026-10-28T18:53:38Z via the official article API".
- `corpus/lessons/round-44-verifier-spotcheck.md:65`: S069 "the HTML page is a metadata shell for a plain fetch, so I re-opened the same document through `…/rest/v1/articles/about/rules/google-friends/...` (HTTP 200, 48 657 B)".
- `corpus/lessons/round-44-verifier-spotcheck.md:66`: S070 re-read through `…/rest/v1/articles/about/rules/about-this-section` (HTTP 200, 10 029-char body) — "agree on the decision, disagree with the stated reason".
- `corpus/source-snapshots/round-45/manifest.json` S072 `capture_url`: `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section`.

Lesson quotes above are read from the committed base bytes in this session; they were not re-opened through any capture method beyond `sed -n` and `grep -n` on the files named.

## Finding 4 — a counter weakness the draft cannot fix

The R2 needle check is keyword presence, not criterion structure. `r45-routed-defects.py` runs `re.search(nd, crit, re.I)` on the criterion cell only (lines 160-166). The R47 criterion cell contains `do-nothing` three times: `cheapest do-nothing control`, `on the do-nothing control printed`, and the path `.ufo/waves/round-44/controls/c2-do-nothing.txt`. Replay with one occurrence changed (`cheapest do-nothing control` → `cheapest control`, single replacement):
- `do-nothing occurrences in R47 criterion cell: 3`
- `limb R2 fixed=1 read=criteria=3`
So the R2 limb passes a criterion whose class word survives only in an incidental place. This is the same presence-only defect class R48 names. The fix belongs to the counter's owner (L1), not this draft: the limb should key on the row's own sentence or require the word inside the ruled clause. I did not edit the counter.

## Limitations

- `corpus/instruments/freeze-check.py` does not exist at base or at HEAD 5242db6 (`ls corpus/instruments/freeze-check.py` → "No such file or directory"; `git ls-files` for that path printed nothing). R47's `enforced-by:` path therefore makes R2 red until L1 lands the instrument. The stub used above only tests the string match; it is evidence about the counter, not about the instrument.
- The R2 result `fixed=1` above is with the stub present; with the other limbs (R1, R3, R4, R5) still red, the counter's total is `fixed=1 unresolved=4 exit=1`, as printed. Those limbs are other drafters' work and were not touched.
- The R6 numbers (78651 bytes, `dd753497…`, 372 lines) were measured at draft time. The landing commit must re-run both commands immediately before writing; any earlier append in the round would move them.
- I did not replay the round-45 C2 gate or the round-45 claims file; that belongs to the C2/freeze seats, not to this drafter.
- Scratch root `$HYAKU_SCRATCH/kasegi-r45/R45ScribeQuality` (default `/fast/scratch/hyaku/...`) held the archive copy and the mutant fixtures and is removed on exit. The pure base export at `/fast/scratch/hyaku/kasegi-r45/L1/pure` was read only; it was not edited.
