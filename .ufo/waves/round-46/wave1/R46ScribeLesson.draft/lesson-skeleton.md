# Round 46 — Kasegi

DRAFT SKELETON (seat R46ScribeLesson). Not the lesson. The L1 integrates and commits `corpus/lessons/round-46.md`. Every `[[FILL-BY-L1: …]]` must be replaced; none may survive into the committed file.

Lane: `kasegi`; attempt [[FILL-BY-L1: attempt number and L1 seat name]]. Round-open base: `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`. Freeze commit: `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` (`.ufo/waves/round-46/claims.json`, sha256 `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`; `freeze.txt`; `r46-c1-gate.py` sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`; `r46-c2-gate.py` sha256 `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`; `S073.txt` sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`; manifest sha256 `01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`). Lane tip: [[FILL-BY-L1: lane commit hash, after `git ls-remote` shows it]].

C1 (`depth:verifiability`): gated `recheck:` lines 24 → ≤22 by re-grounding at least two gated entries (intended pair `claim-package-contract.md`, `claim-gates.md`) on committed bytes. C2 (`coverage`): frontier F28, GitHub private vulnerability reporting (reporter flow), source S073, entry `corpus/knowledge/github-private-vulnerability-reporting.md`.

Frozen-tree readings, measured by the seat (`python3 -I <freeze-counter> --root <tree>`, trees from `git archive`):
- do-nothing, base tree: `c1-gate fixed=1/7 exit=1`; `c2-gate fixed=1/7 exit=1`.
- freeze tree (full export of `9f23aab`): `c1-gate fixed=1/7 exit=1`; `c2-gate fixed=2/7 exit=1`.
- tip reading: [[FILL-BY-L1: `c1-gate` and `c2-gate` at the lane tip, with the printed last line]].

Routed defects: `corpus/lessons/round-45-verifier-spotcheck.md` §6 items 1–5 (`:95`, `:96`, `:97`, `:98`, `:99`), answered below in `## Routed defects`.

## Mistakes

Round-45 spot-check disposition (`corpus/lessons/round-45-verifier-spotcheck.md` §6): item 1 is mined here as M46-1 (class `landing`); items 2–5 are answered in `## Routed defects` and are not mined mistakes. [[FILL-BY-L1: any mistake found by wave 2 (M46-2 …), or the statement "wave 2 found no further mined mistake" with the wave-2 seat ids that checked]].

| ID | Class | Error | Evidence pointer | Captured by | Fix | Evidence the fix can fail |
|---|---|---|---|---|---|---|
| M46-1 | landing | The round-45 closure records that the lane's report names its own report commit `a1f7761` (dated 19:30:06 -0300) earlier than the lane commit `2998baa` it cites as final (dated 19:36:30 -0300), and calls this status-neutral. The lane repository does not hold the cited report commit: `git -C <lane> cat-file -t a1f7761` printed `fatal: Not a valid object name a1f7761`, and `git log --format='%h %ad %s' --date=iso -- .ufo/reports/round-45/kasegi.md` printed nothing, so the ordering cannot be shown from the lane's own history. | `corpus/lessons/round-45-verifier-spotcheck.md:22` (§1 defect (a)); `:95` (§6 item 1); its §1 check row at `:13`. Lane re-run: `git log -1 --format='%h %ad %s' --date=iso 2998baa` → `2998baa 2026-10-28 19:36:30 -0300 round-45: wave 2 results, final measurement, errata, lesson, LOG, SCORECARD`; `git merge-base --is-ancestor 2998baa 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba` → ancestor. | none (`corpus/lessons/round-45.md` `## Mistakes` rows M45-1 to M45-7 carry no ordering or landing-order row) | `corpus/instruments/r46-landing-gate.py` [[FILL-BY-L1: committed path and commit; absent at freeze `9f23aab`]]; QUALITY R50 [[FILL-BY-L1: the R50 row text and its line number; at base `corpus/QUALITY.md` R49 is the last `| R` row (`:382`) and `grep -c R50` prints `0`]]. The fix counts only once its red-before receipt on the round-45 pair is committed: [[FILL-BY-L1: receipt path, the command, and its printed output]]. | The gate must read the report's cited hashes against the lane's history and turn red when a cited hash is absent or is not an ancestor of the report's own commit. A passing run on a tree that lacks the report bytes is the vacuous case: a red-before must exist on the round-45 pair itself, not only on a fixture. [[FILL-BY-L1: where the round-45 report bytes are committed, or a fixture labelled as a fixture]]. [INFERENCE, not run: considerthese proposal 3's landed checks (`corpus/instruments/r35-defect-closure.sh` D1 placeholder grep; `r36-closure.sh` E9(b) porcelain half) do not read a report's cited hashes.] |
| M46-2 | [[FILL-BY-L1: class]] | [[FILL-BY-L1: error, or delete this row if no M46-2 is found]] | [[FILL-BY-L1]] | [[FILL-BY-L1]] | [[FILL-BY-L1]] | [[FILL-BY-L1]] |

## Gate — frontier, source, and rejection

Candidates: [[FILL-BY-L1: every candidate considered this round, with its origin (seat id or considerthese line)]].

Admitted: F28, GitHub private vulnerability reporting (reporter flow), source S073, entry `corpus/knowledge/github-private-vulnerability-reporting.md` [[FILL-BY-L1: entry commit hash; README F28 row line number (`corpus/README.md`; the F27 row is at `:651` at base)]].

Rejected: [[FILL-BY-L1: each rejected candidate with its reason and its flip condition, or the statement "none rejected" with the seat that checked]].

Assimilation: none. Id-collision guard: [[FILL-BY-L1: command and printed output of the guard run against `merge/kasegi/` (`comm -12` on lane ids and staged ids, with the indented-row fixture)]].

considerthese pointer: `considerthese/2026-10-26.md:31` (proposal 3, "Add a quiescence gate before `complete`"). Ledger disposition, old → new (R31): `corpus/knowledge/considerthese-proposals-ledger.md:140` reads `landed — unchanged` (the `## Round-42 dispositions` block starts at `:134`). New: [[FILL-BY-L1: the new disposition wording, citing the M46-1 fix status; the ledger row is the L1's to write]]. The ledger's own numbering note (`:73`) says the same label names different proposals in different tables; the row here is the 2026-10-26 proposal.

New source row S073 (tier A, `mined`, kind `docs`, opened 2026-10-28, used-by the F28 entry): URL `https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately` (`capture_url` and `http.final_url` are the same; HTTP 200 per `manifest.json`); access (UTC capture) `2026-10-28T22:56:49Z`; capture `corpus/source-snapshots/round-46/S073.txt` (589 lines, 15568 bytes per `wc`), committed at freeze `9f23aab`.

Quote block, ≤25 words each, verbatim from the manifest. The seat located each at its anchor line (whitespace-normalised, anchor ±2 lines). `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` (run from a `git archive 9f23aab` export) printed `S073:sha256 OK`, `S073:Q1 OK occurrences=1 anchor=560-ok` through `S073:Q8 OK occurrences=1 anchor=578-ok`, and exited 0:

- Q1 `S073.txt:560` (10 words): “Anyone can privately report a security vulnerability to repository maintainers.”
- Q2 `S073.txt:563` (6 words): “create a draft security advisory directly”
- Q3 `S073.txt:564` (13 words): “You can only report vulnerabilities privately for repositories where this feature is enabled.”
- Q4 `S073.txt:566` (18 words): “you need to initiate the reporting process by following the instructions in the security policy for the repository”
- Q5 `S073.txt:573` (14 words): “By default, you must provide a summary, details, proof of concept, and impact statement.”
- Q6 `S073.txt:574` (13 words): “Optionally, select I used AI assistance to find or write up this report.”
- Q7 `S073.txt:577` (20 words): “GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.”
- Q8 `S073.txt:578` (15 words): “only the repository maintainer can merge changes from that private fork into the parent repository”

Non-author closure slots (the closure fills these; the L1 does not fill them with its own judgment):
- [[FILL-BY-L1: slot 1, S073 re-open: the URL re-fetched by a non-author, Q1–Q8 located in the live page or the capture, verdict]].
- [[FILL-BY-L1: slot 2, F28 entry: does the entry state a reporter decision rule (the claims kill rule: "a decision rule a reporter can act on"), verdict]].
- [[FILL-BY-L1: slot 3, counter reading: the non-author's own `c1-gate` and `c2-gate` run on the tip export, printed last lines]].

Frontier and census counts (base measured by the seat; tip to be filled): SOURCES rows 72 → [[FILL-BY-L1: tip count, expected ≥73]]; frontier rows 27 → [[FILL-BY-L1: tip count, expected 28]]; knowledge entries 64 → [[FILL-BY-L1: tip count, expected 65]]; census: [[FILL-BY-L1: `scripts/sources-census.sh validate --root <tree> kasegi` last line and exit code]].

## SOURCES log

Status, recheck and used-by changes (old → new):

- Existing rows: [[FILL-BY-L1: expected none; confirm with `git diff <base> <lane-tip> -- corpus/SOURCES.md` and the printed hunks for pre-existing row ids, or list each changed cell as old → new]]. At freeze `9f23aab` the diff over `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md` and `corpus/knowledge` is empty (`git diff --stat 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 -- corpus/SOURCES.md corpus/README.md corpus/QUALITY.md corpus/knowledge` printed nothing).
- New row: S073 — [[FILL-BY-L1: the full `corpus/SOURCES.md` row as landed, including the recheck cell]].
- S070 / S072 supersede pair (spot-check §6 item 4): at base, `corpus/SOURCES.md:76` (S070) and `:78` (S072) are the only row lines for those ids; the round-44 note at `:156` names S070 as rejected, and no registry note records that S072 supersedes S070. Recorded: [[FILL-BY-L1: the note line added at the tip, its wording, and the grep that prints it]]. The census `W04` duplicate-URL warning for S072 and S070 is expected from the round-45 closure; [[FILL-BY-L1: confirm the census output line at the tip]].

## Routed defects

Answers to `corpus/lessons/round-45-verifier-spotcheck.md` §6, one item each.

1. **Report/commit ordering: landing gate (§6 item 1).** Carried as M46-1 in `## Mistakes`. Status: [[FILL-BY-L1: open, or fixed at <commit> with the red-before receipt at <path>]]. At freeze `9f23aab`, `git ls-tree -r --name-only 9f23aab | grep -i landing` lists two files, both under `.ufo/waves/round-34` and `.ufo/waves/round-41`, and no landing gate in `corpus/instruments/`; the fix is not yet in the tree.

2. **Counter classification, decided in-round (§6 item 2).** Decision for the round-46 counters, erratum or changed rule: [[FILL-BY-L1: decision, taken before closure, with (a) the diff between the prose predicate in `claims.json` `after` and each counter limb sentence, and (b) the plain re-derivation of item 3 below, which does not use the counter]]. Measured by the seat: `.ufo/waves/round-46/counter-errata.md` does not exist at freeze (`git ls-tree -r --name-only 9f23aab .ufo/waves/round-46 | grep -i errata` printed nothing). The counter files in the `9f23aab` export hash to the digests in `freeze.txt` (`sha256sum` printed `b0c730c8…2294` for `r46-c1-gate.py` and `0ee95857…c6f3` for `r46-c2-gate.py`).

3. **Plain measures beside each counter (§6 item 3).** Base values, from plain commands over a base export (`git archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba corpus SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md`), run by the seat:
   - C1: `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` → `23` (target ≤21).
   - C1: `python3 corpus/instruments/recheck-audit.py --root . --quiet | grep '^executes='` → `executes=40 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)`; the same run's last line is `exit=1`.
   - C1: `python3 corpus/instruments/score-gap.py | grep '^gap:'` → `gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
   - C2: `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `27`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `72`; `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → `64`; `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → no output (exit 1).
   - Tip values: [[FILL-BY-L1: the same commands at the lane tip, with their printed output]].

4. **S072 / S070 pair in the registry (§6 item 4).** Recorded at: [[FILL-BY-L1: `corpus/SOURCES.md` note line and wording]]. See the `## SOURCES log` bullet above for the base reading.

5. **Per-held-axis next promotion limb (§6 item 5).** Held this round: `depth:verifiability` at 4 and `coverage` at 8 [[FILL-BY-L1: confirm the held values at the tip, with the `SCORECARD.md` round-46 result line]]. `depth:density` (9) is not claimed in round 46 and is not listed.
   - `depth:verifiability` 4 → 5: `SCORECARD.md:1536` (`### depth:verifiability, 4 → 5`). Limb 1 is zero gated rechecks (`recheck-audit.py` `gated=0`); the base reads `gated=24` (item 3). C1 targets `gated ≤22`, so limb 1 stays unmet after C1 [[FILL-BY-L1: confirm at the tip]]. Limb 2 is the score-5 audit bar at `SCORECARD.md:331` ("a non-author audit passing 25/25 source chains and 0 unsupported current claims"), which only a non-author closure can grade. [[FILL-BY-L1: name the limb the next round's claim targets]].
   - `coverage` 8: the only coverage promotion heading in `SCORECARD.md` is `### coverage, 7 → 8` at `:1547`; `grep -n '^### coverage' SCORECARD.md` printed only that line, and no 8 → 9 criterion is written. [[FILL-BY-L1: either define the 8 → 9 criterion with its base value, or state that none is defined and coverage is held without a promotion limb]].
