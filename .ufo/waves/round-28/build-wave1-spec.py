#!/usr/bin/env python3
"""Build wave-1 spec for kasegi round 28 (one v2 wave, 69 seats)."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SHOKU = "/home/vgpnk/Projects/shokuknow"
BASE = "c9f8b115a098c65356e4b3b6048af45a37ab8395"
W1 = ".ufo/waves/round-28/wave1"
R28 = ".ufo/waves/round-28"

CONTEXT = f"""# Round
kasegi-shokunin round 28, wave 1 (build+attack, single v2 wave), dispatched by the L1 (parent omp session).
Fleet root {FLEET}. Lane repo {LANE} — your only write scope. Lane base revision {BASE} (claims freeze commit).
Read before your item (absolute paths):
- {LANE}/.ufo/waves/round-28/claims.json (FROZEN claims C1/C2, predicates, counters, kill rules — do
  not edit; corrections land as separate appended files)
- {LANE}/SCORECARD.md (axes, saturation, round-27 carry-forward)
- {LANE}/corpus/QUALITY.md (entry bar Q1-Q10, record bar R1-R13)
- {LANE}/corpus/README.md (coverage map, frontier F01-F11)
- {LANE}/corpus/SOURCES.md (registry; S001-S041; S041 row)
- {LANE}/corpus/lessons/round-27.md (carry-forward items 1-4, M27-1/M27-2)
- {LANE}/corpus/instruments/anchorcheck.py (the C1 instrument; digest c2a9e6c6... pre-change)
- {LANE}/corpus/instruments/capture-source.py (--kind html|pdf|text), source-recheck.py,
  frontier-recheck-count.py, recheck-audit.py
- {SHOKU}/merge/kasegi/ (READ-ONLY assimilation package: MERGE-REPORT.md, SOURCES.append.md,
  knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md)

# The two frozen claims (do not widen, do not re-word; counter commands execute from the lane root)
C1 depth:verifiability (lowest non-retired axis, score 4 held) — anchorcheck.py gate soundness:
(a) exit 1 on unverifiable verdicts (MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT,
BOUNTIES-ABSENT); (b) CITE gains a ~/Projects/bounties/ arm → BOUNTIES-ABSENT; (c) --selftest runs one
isolating fixture per limb, prints `selftest cases=N failures=0`, receipt at the landed sha256;
(d) no-harm: SKILL.md live run exit 0, bad=0, verdict classes unchanged (LOST-RECORDED=306).
Corpus disclosure (frozen): 4 corpus marked bounties citations (claim-gates.md, intake-and-finalize.md,
mission-control.md, source-tree-loss-2026-09-28.md) newly classify LOST-RECORDED after the arm.
Implementation notes (round-27 lesson carry-forward 2): FAIL_CLASSES as above; LOST-RECORDED stays
recorded-not-fail; derive the bounties root like MIRROR/ORIGIN ($KASEGI_BOUNTIES override + canonical
~/Projects/bounties); selftest fixtures must isolate limbs under the absent-bases host (env-override a
temp mirror root to reach MISSING-FILE; PAST-EOF needs a real temp file).
C2 coverage (score 7 held) — F12 Japanese state-coordinated disclosure workflow: captures of the IPA
intake-process page (new row S042) + a round-28 re-capture of the JPCERT/CC 2026 P-guideline (row S041)
under corpus/source-snapshots/round-28/, manifest.json with Q9-bound quote assertions, entry
knowledge/japanese-domestic-disclosure-workflow.md (source: S041 + source: S042 headers, one executable
cwd-independent recheck line), corpus/README.md F12 row admitted, S042 registry row (tier A, mined,
opened 2026-10-25, used-by exactly the entry), S041 used-by gains the entry (old→new logged), census
exit 0, harness entries 14→15 pass 15. Assimilation Gate: >=1 admit + >=1 reject with inline <=25-word
quotes. considerthese/2026-10-25.md proposal 1 lands as QUALITY.md R14 and is practiced in-round.

# Ownership map — production files have exactly ONE writer; do not touch any other production file
- corpus/instruments/anchorcheck.py -> ExecImplC1 ONLY (all other C1 seats: scratch copies under
  {R28}/wave1/<YourSeat>/ only, never the live file)
- corpus/instruments/README.md -> ExecInstrReadme ONLY
- SKILL.md -> ScribeSkillGate ONLY (append at end per R6; never shift lines)
- corpus/source-snapshots/round-28/S042.txt -> ExecCaptureS042 ONLY
- corpus/source-snapshots/round-28/S041.txt -> ExecCaptureS041 ONLY
- corpus/source-snapshots/round-28/manifest.json -> ExecManifest ONLY
- corpus/knowledge/japanese-domestic-disclosure-workflow.md -> ScribeEntryC2 ONLY
- corpus/SOURCES.md -> ScribeRegistryC2 ONLY
- corpus/README.md -> ScribeReadmeC2 ONLY
- corpus/QUALITY.md -> ScribeR14 ONLY
- corpus/lessons/round-28.md -> ScribeLesson ONLY
- LOG.md -> ScribeLog ONLY; SCORECARD.md -> ScribeScorecard ONLY
- {R28}/assimilation/ scratch -> ScoutAssimilation ONLY
- Per-seat receipts: {R28}/receipts/<SeatName>.txt (or .json) — write only your own file.

# Hard rules (every seat)
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Use absolute
  paths in every command.
- You are a leaf: spawn nothing, start no background job, run no swarm of your own.
- Timing: seats run concurrently. If a file your item depends on is not yet updated (e.g. the
  instrument still has pre-change digest c2a9e6c6...), do NOT wait or poll: run your attack against
  scratch copies / the pre-change bytes, label your receipt PRE-STATE, and name the exact re-run
  command the L1 must execute post-change. An unrun check has not passed.
- Write ONLY your owned paths (named above and in your item). A read-only seat makes NO production edit.
- Never write {FLEET} (fleet root), any sibling lane, {SHOKU} (READ-ONLY: no writes, never run
  renumber-staged.py / merge-plan.py / quote-lint.py / absent-defect-register.py there),
  {FLEET}/.ufo/state, {FLEET}/.scratch, MANIFEST.json, templates/ or fleet scripts/.
- Never run in the lane repo: git add/commit/push/checkout/switch/stash/reset/pull, any mutating jj
  command (commit/new/describe/squash/rebase/abandon/bookmark/undo/op restore), or any other VCS write.
  Read-only git (log/show/diff/status/ls-files/rev-parse) and `jj --ignore-working-copy` are fine.
  The L1 commits through the lane helper; you never do. Git fixtures: mktemp -d + git -C "$D" init.
- Tooling: you may install or upgrade tools that help your item — read /home/vgpnk/.omp/agent/RULES.md
  first, official channels only, record tool/version/channel/reason in your report. ALL pacman
  transactions are PAUSED host-wide: use `uv tool` / `npx` / an official binary in ~/.local/bin only;
  never `pacman -S`, `-Sy`, `-Syu`, `-U`, `-R`.
- Honesty: an unrun check has not passed; never fabricate a verdict, a quote, a count or an exit code.
  Quote failures verbatim. If your item cannot be completed, report the exact blocker.
- Never edit claims.json, the round-27 lesson(s), or any prior round's wave receipts.
- No credential material, session or private URLs in anything you write (CORPUS.md rule 6).
- Today is 2026-10-25. Use UTC in timestamps. Access dates in Gate blocks must be today.
"""

ITEMS = {}

def add(name, agent, task):
    assert name not in ITEMS, name
    ITEMS[name] = {"name": name, "agent": agent, "task": "/skill:godspeed\n\n" + task}

# ---------------- scouts (5) ----------------
add("ScoutDatawalk", "scout", f"""This seat carries the L1 planner's bounded data-walk. Verify and report:
1. The frozen counters run from the lane root and their BEFORE values hold at base {BASE}:
   bad-fixture exit (expect 0, BASE-ABSENT=1), bounties-fixture BOUNTIES lines (expect 0),
   `python3 corpus/instruments/frontier-recheck-count.py` (expect entries=14 pass=14 exit=0),
   `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {{n++}} END{{print n+0}}' corpus/README.md`
   (expect 11), sources census exit 0 / 41 rows.
2. `git ls-files corpus/knowledge/*.md | wc -l` (expect 41) and confirm no untracked knowledge files.
3. Read {LANE}/.ufo/waves/round-28/claims.json and confirm it matches commit {BASE} byte-exact
   (`git show {BASE}:.ufo/waves/round-28/claims.json | sha256sum` vs the worktree file).
4. Confirm the 4 disclosed corpus bounties-marked citations exist as claimed (grep the 4 named files).
5. Run `python3 corpus/instruments/recheck-audit.py` and record the summary line (expected-list basis
   for carry-forward 4 reconciliation).
Report: {W1}/ScoutDatawalk.md (facts only, no edits).""")

add("ScoutIpaRecon", "scout", f"""Reconnaissance for the S042 capture (C2). Open the live source
https://www.ipa.go.jp/security/todokede/vuln/process.html (instrument UA:
`curl -sSL -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"`):
1. Record HTTP code, final URL, content-type, and whether the page carries the
   脆弱性関連情報の取扱いプロセス steps 1-10 and the ウェブアプリケーションの取扱いプロセス steps 1-6.
2. Locate step 5 起算日の連絡 in the rendered text and record a <=25-word verbatim quote with the line
   context you found it in (this quote seeds the registry row and the lesson Gate).
3. Note any markup quirks capture-source.py --kind html must handle (encode, nav boilerplate).
4. Confirm the staged row's anchor claim (staged S042: 'step 5 起算日の連絡') against the live page.
Do NOT write the snapshot (ExecCaptureS042 owns S042.txt); do NOT edit SOURCES.md.
Report: {W1}/ScoutIpaRecon.md (include the exact curl command, exit, and your located quote).""")

add("ScoutJpcertRecon", "scout", f"""Reconnaissance for the S041 re-capture (C2). Probe
https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf with the instrument UA (curl -sSIL): record
code, content-type, content-length, last-modified. Compare the live bytes' sha256 against the round-26
committed capture {LANE}/corpus/source-snapshots/round-26/S041.txt (sha256
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47): if identical, say so with the
command output; if different, diff the first divergence and report it. Confirm the edition stamp
2026年10月 and the PDF digital-signature date 2026.09.29 are still what the document carries. Report
whether a fresh capture is byte-identical, and locate the 起算日 footnote-4 sentence in the current
capture text, quoting <=25 words. Do NOT write the snapshot (ExecCaptureS041 owns S041.txt).
Report: {W1}/ScoutJpcertRecon.md.""")

add("ScoutAssimilation", "scout", f"""Run the assimilation pre-checks in scratch you own ({R28}/assimilation/):
1. Id-collision check exactly per the round prompt: extract lane registry ids and staged ids with the
   0-3-space-tolerant pattern, `comm -12` into {R28}/assimilation/collisions. Non-empty is EXPECTED
   (staged S031-S043+ collide with lane S031-S041 by number but differ by document) — record the count
   and paste both id lists.
2. Prove the guard once: a scratch registry file with an indented `  | S002 |` row colliding with a
   staged id must produce a non-empty collisions file (write the fixture, run the pattern, paste output).
3. By-document mapping: for the rows this round adopts, map staged S042 (IPA process page URL) -> lane
   S042 (free; verify no lane row carries that URL: grep the lane registry), and staged S043 (JPCERT
   guideline URL) -> lane S041 (verify SAME URL by document, not by number).
4. Quarantine slice: read /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
   (READ-ONLY), extract the kasegi slice (awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/
   && $4 ~ /S[0-9]+/' ...), record every row's class cell; confirm none of the adopted rows (S042 by
   document) appears; record the verdict list for the report (rows NOT adopted stay quarantined).
5. Staged-row schema survey: inspect staged S042/S043 rows for census-schema conformance (11 columns,
   no literal or escaped pipes in cells, recheck cell is ISO date / NNn / symbolic cadence — NOT prose;
   flag the staged S042 teaches cell per the round-27 lesson note).
Write scratch only under {R28}/assimilation/. Report: {W1}/ScoutAssimilation.md + the scratch files.""")

add("ScoutGateRegistry", "scout", f"""Reconnaissance for the C1 SKILL.md gate-registry update. Read
{LANE}/SKILL.md and {LANE}/corpus/instruments/README.md:
1. Find every existing gate|probe registry row/table naming anchorcheck.py (quote it with its line
   number) and record its current verdict map and exit-code wording.
2. Find where the instruments README documents anchorcheck's verdict classes and exit behavior
   (quote lines).
3. Confirm appending ONE new row at the end of the existing registry table shifts no existing line
   (R6): record the table's last-row line number and the byte offset where an append would land.
4. Report the exact append strategy for ScribeSkillGate and ExecInstrReadme (same-line suffix vs new
   row; cite R6).
Report: {W1}/ScoutGateRegistry.md (no edits).""")

# ---------------- connectors (3) ----------------
add("ConnOverlap", "connector", f"""Sibling-overlap scan for F12 ground. Read the sibling lanes' corpus
indexes (READ-ONLY): {FLEET}/kengaku-shokunin/corpus/README.md, {FLEET}/chousa-shokunin/corpus/README.md,
{FLEET}/kotoba-shokunin/corpus/README.md, {FLEET}/kake-shokunin/corpus/README.md. Question: does any
sibling already hold the Japanese state-coordinated disclosure workflow ground (IPA/JPCERT process,
起算日, coordinator-mediated flow)? Check for entries naming IPA, JPCERT, 起算日, 情報処理推進機構.
Name what you found with paths; if nothing, paste the sweep commands and outputs (negative claim
carries its sweep). Conclude: is F12 uncovered coverage-map ground for kasegi?
Report: {W1}/ConnOverlap.md (no edits).""")

add("ConnClaims", "connector", f"""Cross-claim pattern check. The round's two claims share one pattern:
fail-closed receipts (C1: instrument exits nonzero; C2: manifest quote assertions). Read the frozen
claims.json, then check consistency: (1) both claims' kill rules demand a failing control — name each
control and its receipt path; (2) C1 counter (c) and C2 counter (3) both bind a receipt to a sha256 —
confirm the binding sentence is the same shape in both (paste both); (3) flag any asymmetry the L1
must reconcile before the canonical receipts land. Also scan {LANE}/corpus/lessons/round-25.md and
round-26.md for the same pattern's prior defects (R25-2 receipt cross-reference, defect 4 canonical
receipt) and confirm this round's dispatch_requirements close them; cite the lesson lines.
Report: {W1}/ConnClaims.md (no edits).""")

add("ConnStagedCensus", "connector", f"""Census of the staged package vs the lane registry by document.
From {SHOKU}/merge/kasegi/SOURCES.append.md (READ-ONLY): extract every staged row's id + canonical URL;
from {LANE}/corpus/SOURCES.md extract every lane row's id + URL. Join by URL: (1) which staged rows
are already lane rows under DIFFERENT ids (staged S043 == lane S041 is known — verify and find all
others); (2) which staged rows are genuinely absent from the lane registry (count them); (3) verify the
r27 lesson's claim 'staged S042 is free in the lane registry' by URL. Report the join table (id_staged,
url, id_lane|none). This is the adoption map future rounds use; it also proves this round appends
exactly one row.
Report: {W1}/ConnStagedCensus.md (no edits).""")

# ---------------- executors (19) ----------------
add("ExecImplC1", "executor", f"""Implement the frozen C1 change in {LANE}/corpus/instruments/anchorcheck.py
(you own this file; no other seat may edit it). Requirements (claims.json C1, round-27 carry-forward 2):
1. FAIL_CLASSES = MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT; the
   tool exits 1 when any fail-class count > 0, else 0. LOST-RECORDED stays recorded-not-fail.
2. CITE gains a `~/Projects/bounties/` arm: regex alternative for `~/Projects/bounties/<path>:<line>`
   with the SAME realpath confinement as MIRROR/ORIGIN (escapes classify OUTSIDE-BASE against the
   bounties root); absent root -> BOUNTIES-ABSENT. Derive the root like MIRROR/ORIGIN:
   $KASEGI_BOUNTIES override else canonical ~/Projects/bounties; BOUNTIES_ABSENT flag like the others.
3. `--selftest`: one isolating fixture per limb, run in temp dirs (env-overrides KASEGI_MIRROR /
   KASEGI_BOUNTIES to reach MISSING-FILE / BOUNTIES-ABSENT; a real temp file for PAST-EOF; a fake git
   pin object id for PIN-BROKEN; a path escape for OUTSIDE-BASE). Print `selftest cases=N failures=0`
   and exit 0; any fixture failing prints the failing case and exits 1.
4. Update the module docstring: new verdict class, exit semantics, --selftest, the bounties arm, and
   keep the existing verdict classes/separation intact.
5. After editing, run: the two r27 fixtures (bad-fixture must exit 1 with BASE-ABSENT printed;
   bounties-fixture must print exactly 1 BOUNTIES-ABSENT line); `--selftest` (exit 0, cases=N
   failures=0); the SKILL.md live run (exit 0, bad=0, LOST-RECORDED=306, BASE-ABSENT=0 — verdict
   classes UNCHANGED); and anchorcheck over corpus/knowledge/*.md (report the 4 disclosed bounties
   citations now classifying LOST-RECORDED). Paste ALL outputs into your receipt.
Also write {W1}/ExecImplC1.diff (unified diff of your change, produced with `git diff -- corpus/instruments/anchorcheck.py`
plus `sha256sum` of the new file) so reviewers can review without touching the live file.
Receipts: {R28}/receipts/ExecImplC1.txt and {W1}/ExecImplC1.diff.""")

add("ExecInstrReadme", "executor", f"""You own {LANE}/corpus/instruments/README.md ONLY. Update the
anchorcheck.py section to document: the fail-closed exit semantics (exit 1 on any fail class), the
BOUNTIES-ABSENT verdict class, the derived $KASEGI_BOUNTIES root, the --selftest spelling, and the
corpus disclosure (4 marked bounties citations now LOST-RECORDED). Append at the end of the anchorcheck
section (R6: never shift existing lines); if the section is mid-file, add a same-line-suffix-free new
paragraph at the file end naming the round-28 amendment instead. Wait for ScoutGateRegistry's report
({W1}/ScoutGateRegistry.md) to see the current wording — if it is not yet written, proceed against the
current bytes and note that. Receipt: {R28}/receipts/ExecInstrReadme.txt with before/after sha256.""")

add("ExecCaptureS042", "executor", f"""You own {LANE}/corpus/source-snapshots/round-28/S042.txt ONLY.
Capture the IPA intake-process page:
`cd {LANE} && python3 corpus/instruments/capture-source.py --id S042 --url
https://www.ipa.go.jp/security/todokede/vuln/process.html --kind html --out
corpus/source-snapshots/round-28/S042.txt`
Record exit, byte count, sha256, and fetch timestamp (UTC). Then grep the snapshot for 起算日 and for
取扱いプロセス, recording every hit line number + first 100 chars. Verify the snapshot contains the
10-step product flow and the 6-step web-application flow; paste the step headings you found. If the
fetch fails or the page structure blocks the instrument, report the exact failure and stop (do NOT hand-
scrape into the snapshot). Receipt: {R28}/receipts/ExecCaptureS042.txt.""")

add("ExecCaptureS041", "executor", f"""You own {LANE}/corpus/source-snapshots/round-28/S041.txt ONLY.
Re-capture the JPCERT/CC 2026 partnership guideline:
`cd {LANE} && python3 corpus/instruments/capture-source.py --id S041 --url
https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out
corpus/source-snapshots/round-28/S041.txt`
Record exit, byte count, sha256, fetch timestamp. Compare byte-for-byte with the round-26 capture
{LANE}/corpus/source-snapshots/round-26/S041.txt (`cmp` + sha256 of both): identical or not, paste the
result (ScoutJpcertRecon may already have probed this — your comparison is the authoritative one on the
committed bytes). Grep for 起算日 and record hit lines; verify the edition stamp 2026年10月 appears.
Receipt: {R28}/receipts/ExecCaptureS041.txt.""")

add("ExecManifest", "executor", f"""You own {LANE}/corpus/source-snapshots/round-28/manifest.json ONLY.
Build it AFTER both captures land (if absent when you start, do the parts you can and re-check once;
if still absent, report the blocker — do NOT invent captures). Schema follows round-26's manifest
(schema_version 1, purpose, sources[]): records S042.txt (new capture, path stem == id) and S041.txt
(round-28 re-capture) with sha256 pins and quote assertions. Quote assertions: Q9-conformant — every
quote exactly-once in its capture OR carries an `anchor` line number; `location` is documentation the
instrument does not read; each quote <= 25 words, copied from the capture bytes (never retyped from
memory); include at least: for S042, the step-5 起算日の連絡 quote ScoutIpaRecon located; for S041, the
起算日 footnote-4 definition and the 図1 flow statement. Run
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json`
(full run) and paste the output (expect exit 0, every assertion passing). Receipt:
{R28}/receipts/ExecManifest.txt with the manifest sha256 before and after any fix.""")

add("ExecHarnessC2", "executor", f"""Run and receipt the C2 instruments (no production edits):
1. `cd {LANE} && python3 corpus/instruments/source-recheck.py --manifest
   corpus/source-snapshots/round-28/manifest.json --source S042` and `--source S041` — both must exit 0;
   paste outputs. If the manifest is not yet present, run against the round-26 manifest for S041 as a
   PRE-STATE receipt and say so.
2. After the entry + README row land: `python3 corpus/instruments/frontier-recheck-count.py` — expect
   entries=15 pass=15 exit=0; paste output. PRE-STATE (before entry lands): expect entries=14 — record
   both if you can, else the one that exists.
3. Run the entry's own recheck line exactly as written, from a FOREIGN cwd (cd /tmp first) — Q10
   cwd-independence; paste output.
Receipt: {R28}/receipts/ExecHarnessC2.txt.""")

add("ExecCensusDry", "executor", f"""Pre-landing census dry-run in scratch (no production edits). Build a
scratch mirror: copy {LANE}/corpus/ to a temp dir, apply ScribeRegistryC2's planned registry edit (read
their draft receipt {R28}/receipts/ScribeRegistryC2.txt if present; else construct the expected S042 row
+ S041 used-by change from claims.json yourself and say which), then run:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`
Expect exit 0 (warnings allowed). Paste the full output. This gates the real append: E03/E04 findings
mean refuse/supersede, never append past. Receipt: {R28}/receipts/ExecCensusDry.txt.""")

add("ExecExpectedList", "executor", f"""Reconcile the recheck-audit expected-list count basis (round-27
carry-forward 4). Run `cd {LANE} && python3 corpus/instruments/recheck-audit.py` and record its
`lines=`/`total=` summary; count `git ls-files corpus/knowledge/*.md | wc -l`; determine whether the
expected-list regeneration after the F12 entry lands should produce N or N+1 and WHY (read the
instrument's expected-list logic, quote the code lines). Do NOT regenerate the list (the entry may not
have landed yet); produce the exact command the L1 must run post-landing and the expected before/after
values. Receipt: {R28}/receipts/ExecExpectedList.txt.""")

add("ExecNoHarmC1", "executor", f"""Run the C1 no-harm measurements (no production edits):
1. `cd {LANE} && python3 corpus/instruments/anchorcheck.py SKILL.md` — record exit, the summary line,
   and the full verdict-class counts (LOST-RECORDED, PIN-BROKEN, ORIGIN, OUTSIDE-BASE, BASE-ABSENT,
   bad). Compare against the frozen before (exit 0, bad=0, LOST-RECORDED=306). If the instrument is
   still pre-change (digest c2a9e6c6...), run anyway and label PRE-STATE.
2. `cd {LANE} && python3 corpus/instruments/density.py SKILL.md --label r28-noharm` — record the mean,
   block count, and path-citation instances; compare against 154.0 / 19 blocks / 652 (round-25/24
   receipts). SKILL.md must be byte-identical to base {BASE} for this guard (`git diff {BASE} -- SKILL.md`
   must be empty unless ScribeSkillGate has landed — check and name what you see).
Receipt: {R28}/receipts/ExecNoHarmC1.txt.""")

add("ExecFixtureRun", "executor", f"""Re-run the frozen C1 counters against the live instrument and
receipt them exactly (no production edits):
1. bad-fixture: `python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md
   >/dev/null 2>&1; echo $?` — paste exit + the printed summary line.
2. bounties-fixture: `python3 corpus/instruments/anchorcheck.py
   .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT` — paste count.
3. selftest: `python3 corpus/instruments/anchorcheck.py --selftest` — paste full output + exit.
Label each receipt with the instrument sha256 you ran against (`sha256sum corpus/instruments/anchorcheck.py`).
If the instrument is still pre-change, label all three PRE-STATE. Receipt: {R28}/receipts/ExecFixtureRun.txt.""")

add("ExecC2Counters", "executor", f"""Re-run the frozen C2 counters (no production edits), labeling
PRE-STATE where the artifact has not landed:
1. `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {{n++}} END{{print n+0}}' corpus/README.md`
2. `grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l`
3. `grep -cE '^\\|[[:space:]]*S042[[:space:]]*\\|' corpus/SOURCES.md`
4. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo exit=$?`
5. `python3 corpus/instruments/frontier-recheck-count.py`
Paste every output with the UTC timestamp of each run. Receipt: {R28}/receipts/ExecC2Counters.txt.""")

add("ExecRecheckAuditR28", "executor", f"""Run the recheck-audit instrument over the corpus after all
knowledge/ lands (if the new entry is absent when you run, produce a PRE-STATE receipt and stop):
`cd {LANE} && python3 corpus/instruments/recheck-audit.py` — record the summary line. Then run the new
F12 entry's recheck line standalone from a foreign cwd and from the lane root; both must exit 0; paste.
Receipt: {R28}/receipts/ExecRecheckAuditR28.txt.""")

add("ExecScopeSweep", "executor", f"""Write-scope sweep after the wave's edits land (best effort at your
run time; label what was checked):
1. `git -C {FLEET} status --porcelain` (fleet root) — any untracked file whose content names kasegi or
   round-28 is a MISROOT: copy it byte-exact into the same relative path under {LANE}, `cmp` to verify,
   then DELETE the fleet copy; record each action. Never touch files naming other lanes, .ufo/state,
   .scratch, MANIFEST.json, templates/ or fleet scripts/.
2. `git -C {LANE} status --porcelain` — every modified path must be in the ownership map or under
   .ufo/waves/round-28/ or the named receipts; list any violation.
3. Confirm no seat wrote under {SHOKU} (`git -C {SHOKU} status --porcelain` empty — read-only).
Receipt: {R28}/receipts/ExecScopeSweep.txt.""")

add("ExecReceiptCanonC1", "executor", f"""Draft the canonical C1 receipt index content (a TEXT block, not
the final file — the L1 assembles the canonical file post-commit). Collect from the wave receipts:
instrument sha256 (post-change), bad-fixture exit + summary, bounties-fixture count, selftest output,
SKILL.md no-harm line, and the corpus disclosure count. Emit the exact lines the canonical
{R28}/c1-receipt-index.txt should contain, each labeled with its source receipt path. Write your draft
to {R28}/receipts/ExecReceiptCanonC1.txt. Do NOT create {R28}/c1-receipt-index.txt (defect 4: one
canonical receipt, assembled by the L1 at the landed digest).""")

add("ExecReceiptCanonC2", "executor", f"""Draft the canonical C2 receipt block (same rules as
ExecReceiptCanonC1): frontier count before/after, entries-citing-S042 before/after, registry rows
before/after, census exit, harness line, manifest sha256, source-recheck S041/S042 exits. Write the
exact canonical lines with source-receipt pointers to {R28}/receipts/ExecReceiptCanonC2.txt. Do NOT
create any canonical file under {R28}/ root.""")

add("ExecSkillGateSupport", "executor", f"""Support measurement for the SKILL.md gate row (no edits):
run `cd {LANE} && grep -nE 'gate\\|probe|anchorcheck' SKILL.md | head -20` and record the registry
table shape; compute the line number where an appended row would land and confirm appending there
shifts no existing anchor (count SKILL.md lines; R6). Also run
`python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | tail -1` and record the summary (it
is the post-impl no-harm input if the impl has landed; label PRE-STATE otherwise).
Receipt: {R28}/receipts/ExecSkillGateSupport.txt.""")

# ---------------- scribes (15) ----------------
add("ScribeEntryC2", "scribe", f"""You own {LANE}/corpus/knowledge/japanese-domestic-disclosure-workflow.md ONLY.
Draft the F12 entry, re-grounded on THIS ROUND's captures (never on the staged package bytes as
authority). Structure: H1 title; directly under it the Q1 trio: `source: S041 — <url> — <anchor>` and
`source: S042 — <url> — <anchor>` header lines (both; mirror the two-source F09/F10/F11 entry format:
read one first, e.g. knowledge/iso-29147-and-30111-division-of-labour.md, and copy its header shape),
`verified-at: 2026-10-25`, `recheck:` ONE executable cwd-independent command of the form
`cd <lane-root> && python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-28/manifest.json --source S041 --source S042` (Q10: parseable by bash -n,
carries its own cd prefix). Body: the state-coordinated flow (10-step product path + 6-step web-app
path), 起算日 as the disclosure-clock anchor (first attempted contact — quote it from the captures,
<=25 words each, with capture line numbers), the one-year withdrawal rule, the web-app lighter path,
and a 'Why it matters' paragraph naming 起算日 as the transferable artefact for coordinator-timeline
comparisons (F02 linkage). Q4: attribute positions to IPA/JPCERT/CC, never universalize. Q5: name one
falsifiable rule and one rejected over-generalization. Q6: documentation-only. Every load-bearing claim
carries a capture-anchored quote: cite S042.txt:LINE and S041.txt:LINE. Read the staged package entry
{SHOKU}/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md for its claim
skeleton, but every quote must be re-located in the round-28 captures (RevengerC2 traces this).
Receipt: {R28}/receipts/ScribeEntryC2.txt (quote list + line anchors).""")

add("ScribeRegistryC2", "scribe", f"""You own {LANE}/corpus/SOURCES.md ONLY. Two edits, both logged:
1. Append ONE row for S042: 11 columns, no literal or escaped pipes in any cell; normalized to the
   lane's fleet schema (NOT the staged bytes as-is): id S042; source `IPA 脆弱性関連情報の届出受付業務における
   取扱いプロセス — https://www.ipa.go.jp/security/todokede/vuln/process.html`; kind docs; tier A;
   scope = IPA/JPCERT/CC intake-process for that page's coverage; anchor = the 10-step flow + step 5
   起算日の連絡, verified against the round-28 capture; teaches = ONE grounded learner benefit
   (coordinator-mediated flow; the finder is told 起算日 and the detail-information date); status mined;
   opened 2026-10-25; recheck `180d`; used-by exactly `corpus/knowledge/japanese-domestic-disclosure-workflow.md`.
   The staged row's prose-flavored cells (per the r27 lesson note) must be rewritten in this normalized
   shape — never appended as-is (§10 scratch transformation rule).
2. S041 used-by: append the entry path to the existing S041 row's used-by cell, keeping every other
   cell byte-identical (R8: log old -> new in your receipt and in the lesson).
Also append the change log lines at the registry's change-log section per the round-26 precedent
(r26 logged the S041 recheck-cell restore at the file's log area — mirror that shape). Then run the
census CLI yourself: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` — exit must be 0 (only pre-existing W04 warnings allowed); paste.
Receipt: {R28}/receipts/ScribeRegistryC2.txt (old/new cells + census output).""")

add("ScribeReadmeC2", "scribe", f"""You own {LANE}/corpus/README.md ONLY. Two appends (R6 — never shift
existing lines; both go at the end of their sections or as end-of-file amendments):
1. Frontier table: append row F12 (id F12 | topic 'Japanese state-coordinated disclosure workflow' |
status admitted | entry knowledge/japanese-domestic-disclosure-workflow.md | sources S041, S042 |
next-step cell naming the 起算日 column for future coordinator-timeline comparisons). Mirror an existing
row's exact column shape. Update the admitted-count sentence (the paragraph after the table that names
'11/11 admitted at round 26; F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26')
to record F12 at round 28 and 12/12 — same-line suffix or an appended amendment line, never rewriting
the historical sentence (R9).
2. Coverage map / expected-list note: append the round-28 reconciliation note naming the new entry and
   pointing at ExecExpectedList's receipt for the count basis.
Do not touch the 0/18 lost-domain sentences. Receipt: {R28}/receipts/ScribeReadmeC2.txt.""")

add("ScribeR14", "scribe", f"""You own {LANE}/corpus/QUALITY.md ONLY. Append the round-25/26-era section
shape: `## Round-28 additions — wave-evidence economy` with one criterion:
| R14 | Wave evidence is receipts and digests in git: a control/fixture tree larger than a few hundred
kilobytes is committed as one content-addressed tarball (sha256 in the receipt) or regenerated from
`git archive <rev>` plus a named mutation script, never as a full corpus copy; per-round repo growth is
measurable from committed bytes. | considerthese/2026-10-25.md proposal 1 (2026-10-25); round-25
verifier spotcheck §bloat finding (98261eb +850,085 lines; ~65 MB under .ufo/waves/round-25/) |
Append at the end of the file (R6). Practice note: cite this round's own receipts/ layout (digests +
receipts, no full-corpus fixture copies) as the exercised instance in your receipt.
Receipt: {R28}/receipts/ScribeR14.txt.""")

add("ScribeSkillGate", "scribe", f"""You own {LANE}/SKILL.md ONLY. After ExecImplC1 lands (check
{W1}/ExecImplC1.diff; if absent, draft against the frozen predicate and label PRE-STATE), append ONE
row to the existing gate|probe registry table for anchorcheck.py recording the round-28 semantics:
fail-closed exit (exit 1 on MISSING-FILE/PAST-EOF/OUTSIDE-BASE/PIN-BROKEN/BASE-ABSENT/BOUNTIES-ABSENT),
the --selftest spelling, the $KASEGI_BOUNTIES root, and the owner. Append at the END of the table only
(R6); record the table's prior last line number and the new row's line number in your receipt. Also
append a same-round note (end of file or end of section) that the 4 corpus bounties citations now
classify LOST-RECORDED — one sentence, anchored to the disclosure. Keep every existing byte anchored:
verify with `python3 corpus/instruments/anchorcheck.py SKILL.md` BEFORE and AFTER your edit — the
cited-line output for pre-existing anchors must be unchanged except your appended material (paste both
summaries). Receipt: {R28}/receipts/ScribeSkillGate.txt.""")

add("ScribeStagedCompare", "scribe", f"""Read-only comparison (no production edits): diff the staged
entry {SHOKU}/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md against
the lane's existing F11 entries ({LANE}/corpus/knowledge/iso-29147-and-30111-division-of-labour.md and
iso-29147-divergence-and-clause-crosswalk.md) and against F02
({LANE}/corpus/knowledge/coordinated-disclosure-timelines.md). Produce the overlap map: which staged
claims duplicate F11 ground (e.g. 29147/30111 division — the staged entry's S043 anchor names the
guideline, not the division itself; be precise), which are new (起算日 workflow, one-year withdrawal,
web-app parallel path). Output the overlap map as {W1}/ScribeStagedCompare.md — ScribeEntryC2 and
RevengerC2 consume it to keep F12 distinct from F11.""")

add("ScribeLessonGate", "scribe", f"""You own the Gate section draft (final assembly by ScribeLesson):
write {W1}/ScribeLessonGate.md containing the round-28 `## Gate` section per LEARNING.md/CORPUS.md:
- The assimilation set: staged package rows/entries read this round; >=1 ADMIT (the workflow entry +
  S042 by document; staged S043 == lane S041 cited not re-registered) and >=1 REJECT with reason+flip.
  Reject candidates to evaluate: (a) the standing chinese-criminal-thresholds refusal — re-confirm or
  lift with evidence; (b) vendor-third-party-finding-coordination-2026-10-23.md — its `ground: F20`
  names no lane frontier row (verify against corpus/README.md). Verdicts must cite package paths.
- Every NEW SOURCES row: URL, access date 2026-10-25, and a <=25-word located quote INLINE (round-26
  routed defect 3 — no pointer-only gates). For S042 use ScoutIpaRecon's/ExecCaptureS042's located quote.
- Every status/recheck/used-by change: old -> new inline (S041 used-by).
- The quarantine-slice verdict list from ScoutAssimilation (7 kasegi rows, none adopted; each row's
  register class recorded).
Gate shape follows round-26's lesson Gate (read it first: {LANE}/corpus/lessons/round-26.md).""")

add("ScribeLesson", "scribe", f"""You own {LANE}/corpus/lessons/round-28.md ONLY. Assemble the full lesson
from the wave receipts after the work lands (read every {W1}/*.md and {R28}/receipts/*.txt that exists
when you run; label anything missing as not-landed): H1 round-28 header; the frozen-claims recap with
final verdicts (filled from ExecC2Counters/ExecFixtureRun — if those show PRE-STATE, mark the lesson
DRAFT and say the L1 finalizes after close); `## Gate` — paste ScribeLessonGate's draft, reconciled
with what actually landed; `## Mistakes` — at least one row: class, evidence pointer, captured-by,
fix (candidates: any seat's PRE-STATE receipt that reveals a timing hazard; the staged-row prose-cell
defect the normalization fixed; anything SentinelScope finds); `## Compliance` (freeze discipline,
census before/after, no pacman). Claim and honest wording throughout. If claims land mid-wave while you
write, record both receipt states with timestamps. Receipt: {R28}/receipts/ScribeLesson.txt.""")

add("ScribeLog", "scribe", f"""You own {LANE}/LOG.md ONLY. Append the round-28 entry at the END (never
rewrite history; R9). Content: freeze commit {BASE}; the two claims with their final measured
before->after values (re-run the frozen counter commands yourself from the committed bytes at your run
time — do not transcribe another seat's numbers; if an artifact has not landed, write 'pending at
<UTC>' and the L1 appends the final value at close); census before (exit 0, 41 rows) and after
(ScribeRegistryC2's run; expect 42); wave shape (one v2 wave, 69 seats, role mix from the spec);
receipt pointers. One line per claim plus a census line and a wave line. Receipt:
{R28}/receipts/ScribeLog.txt with the exact LOG.md diff.""")

add("ScribeScorecard", "scribe", f"""You own {LANE}/SCORECARD.md ONLY. Append `## Round 28 — frozen
claims C1/C2 (2026-10-25)` at the end (never edit prior rows). Table rows: C1 depth:verifiability
before (bad-fixture exit 0; bounties 0 lines; selftest absent; SKILL exit 0 bad=0 LOST=306) -> after
(the measured values you re-run yourself: bad-fixture exit 1; bounties 1 line; selftest cases=N
failures=0 at instrument sha256; SKILL exit 0 bad=0 LOST=306) with verdict + evidence pointers
(receipts paths); C2 coverage before (frontier 11; entries 0; rows 41; harness 14/14) -> after
(frontier 12; entries 1; rows 42 census exit 0; harness 15/15); depth:density 9 held with the
ExecNoHarmC1 density numbers (SKILL.md byte-diff vs base named). Capabilities: add NO row unless a
capability actually demonstrated this round (none is planned — say so). Saturation paragraph unchanged.
If measurements are PRE-STATE when you run, write the row with 'pending' cells and the L1 completes at
close. Receipt: {R28}/receipts/ScribeScorecard.txt.""")

add("ScribeSourcesGate", "scribe", f"""Draft the SOURCES-anchored evidence block for the report (no
production edits): for every source opened this round (IPA page, JPCERT PDF, staged package files),
write: the S-row it becomes or cites, URL, access date 2026-10-25, <=25-word located quote, and the
knowledge path citing it. This block is the report's Sources & frontier raw material and the §2b
'at least one sourced claim' evidence (C2 rests on S042 opened this round). Write it to
{W1}/ScribeSourcesGate.md. Confirm the census row count for S042 lands at exactly 42 total rows
(re-run the row-count command yourself).""")

add("ScribeReportDigest", "scribe", f"""Draft the report skeleton evidence digest (no production edits):
read the frozen claims.json and every receipt in {R28}/receipts/ that exists at your run time; produce
{W1}/ScribeReportDigest.md containing, per report section (Work performed / Landed changes /
Before-after measurements / Sources & frontier / Trend verdicts / SHONEN), the bullet points with
evidence pointers the L1 needs. Trend verdicts: draft a proposed verdict per trend with its evidence
(expansion: F12; quality: C1 fail-closed + captures re-grounded; discernment: the Gate admits/rejects
+ disclosure) — the L1 owns the final call. SHONEN: four boxes, all [~] with refreshed pointers, no
self-written [x]. Label PRE-STATE items as such. Receipt: {R28}/receipts/ScribeReportDigest.txt.""")

add("ScribeReceiptsC2", "scribe", f"""Assemble the C2 receipt bundle index (no canonical file — write
{R28}/receipts/ScribeReceiptsC2.txt): list every C2-related receipt file with one-line summaries
(capture sha256s, manifest sha256, census output hash, harness lines, counter values with timestamps).
Cross-check that every frozen C2 counter has at least one receipt covering it; name any gap.
This is the digest the canonical receipt and the report cite.""")

add("ScribeFrontierNote", "scribe", f"""Draft the frontier-continuity note (no production edits): read
corpus/README.md's Frontier section and the F02/F11 entries; write {W1}/ScribeFrontierNote.md
proposing the F12 'next' cell wording (how 起算日 becomes the Japanese column in future coordinator-
timeline comparisons) and checking the F12 topic string does not collide with any existing F-row
topic. Also verify the coverage-map paragraph's denominator wording stays consistent with the
11/12 admitted public-practice frontier (never the 0/18 lost-domain figure). ScribeReadmeC2 consumes.""")

add("ScribeQualityCross", "scribe", f"""Cross-check the C2 entry draft against QUALITY.md Q1-Q10 BEFORE
it lands (no production edits): read ScribeEntryC2's file as it exists when you run (if absent, check
against the staged skeleton and label PRE-STATE); produce a criterion-by-criterion table
(Q1..Q10, R1..R6 where applicable) with PASS/FAIL and the entry line evidence for each; any FAIL gets
a concrete fix suggestion. Write {W1}/ScribeQualityCross.md. This is the entry's independent bar check
before admission. Receipt: {R28}/receipts/ScribeQualityCross.txt.""")


add("ExecInstrSelftest", "executor", f"""Selftest instrumentation run (no production edits): after ExecImplC1
lands (check sha256), run `python3 corpus/instruments/anchorcheck.py --selftest` and capture the FULL
output verbatim including the `selftest cases=N failures=0` line and exit code; then run it a second
time to confirm determinism (identical output). Record the instrument sha256 with each run. If the
impl has not landed, run against pre-change bytes, record the FileNotFoundError as PRE-STATE, and stop.
Receipt: {R28}/receipts/ExecInstrSelftest.txt.""")

add("ScribeCensusNote", "scribe", f"""Draft the census-section note for the lesson (no production edits):
read {R28}/census-before.txt (exit 0, 41 rows) and run the round-end census yourself when the registry
lands (or record PRE-STATE): paste the full validation output, the row count before->after (41->42),
the tier/status histogram delta (one new tier-A mined row), and the W04 status (pre-existing, S028/S029).
Write it to {W1}/ScribeCensusNote.md — ScribeLesson consumes it as the Compliance census block.""")

add("ExecGateLog", "executor", f"""Emit the gate/verdict inventory for the report (no production edits):
list every instrument gate run this round with its exit code — anchorcheck.py (before/after, fixtures,
selftest, SKILL.md, corpus sweep), density.py, recheck-audit.py, source-recheck.py,
frontier-recheck-count.py, capture-source.py x2, sources-census.sh xN — each with receipt path and the
sha256 of the instrument or manifest it ran against. Produce {W1}/ExecGateLog.md (the report's
evidence-pointer index).""")
# ---------------- reviewers (12) ----------------
add("RevImplC1", "reviewer", f"""Review the C1 implementation against the frozen predicate. Source:
{W1}/ExecImplC1.diff (if absent, review the live file against base with
`git diff {BASE} -- corpus/instruments/anchorcheck.py`; if that is empty too, label PRE-STATE and
review the pre-change bytes against the predicate, listing what must change). Check line by line:
(1) every FAIL_CLASS actually triggers exit 1 and no IN-RANGE class does; (2) the bounties arm is
realpath-confined exactly like MIRROR (quote the confinement code from both arms and compare); (3)
--selftest fixtures are isolating — each fails exactly one limb (read the fixture code; run it if the
impl has landed); (4) LOST-RECORDED is untouched; (5) no behavior change outside the fail-class/exit/
arm/selftest scope (flag any drive-by edit). Verdict: APPROVE or CHANGES-REQUIRED with file:line
evidence. Receipt: {W1}/RevImplC1.md.""")

add("RevFixturesC1", "reviewer", f"""Review the --selftest fixtures for isolation and completeness
(claims.json kill rule: a limb with no failing fixture, or a fixture failing another limb, kills C1).
Read the selftest code in the landed instrument (or {W1}/ExecImplC1.diff). For EACH fixture: which
limb it targets, why it fails that limb and no other (trace the code path), and its expected output
line. Check completeness: one fixture per FAIL_CLASS limb (MISSING-FILE, PAST-EOF, OUTSIDE-BASE,
PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT) + a clean-case control. Also verify fixtures run in temp
dirs and never touch the live tree. Run the selftest if the impl has landed and paste the output.
Receipt: {W1}/RevFixturesC1.md.""")

add("RevNoHarmC1", "reviewer", f"""Independent no-harm verification (claims.json C1(d)): after the impl
lands (check the instrument digest; PRE-STATE if unchanged), run `python3 corpus/instruments/anchorcheck.py
SKILL.md` and diff the FULL verdict-class set against the frozen before (exit 0; bad=0; LOST-RECORDED=306;
PIN-BROKEN=0; ORIGIN=0; OUTSIDE-BASE=0; BASE-ABSENT=0; in-range=7). Then run over corpus/knowledge/*.md
and corpus/*.md: produce the corpus-wide delta table (which files gained LOST-RECORDED lines; expect
exactly the 4 disclosed bounties citations and no other class movement). Any OTHER movement is a no-harm
violation — name it. Receipt: {W1}/RevNoHarmC1.md.""")

add("RevEntryC2", "reviewer", f"""Bar-check the F12 entry against QUALITY.md. Read
{LANE}/corpus/knowledge/japanese-domestic-disclosure-workflow.md as it exists when you run (PRE-STATE:
check the staged skeleton against the bar instead, and say what the real entry must still prove).
Criterion table Q1-Q10 + Q4 attribution + Q5 falsifiable-rule-and-rejection, each with entry line
evidence; then verify three load-bearing claims END-TO-END: open the round-28 captures at the entry's
cited line anchors and confirm the quoted text is there verbatim (paste capture line + entry quote);
run the entry's recheck line from a foreign cwd; confirm both source: headers' ids equal the recheck's
--source ids (R12). Verdict: ADMIT-BAR-MET or list exact failures. Receipt: {W1}/RevEntryC2.md.""")

add("RevRegistryC2", "reviewer", f"""Review the registry edit (corpus/SOURCES.md) after ScribeRegistryC2
lands (PRE-STATE if untouched): run the FULL frozen census grammar yourself — 11 columns on the new
row (awk NF check), no literal/escaped pipes in cells, kind enum `docs`, tier A scoped, status mined,
used-by exactly the one entry and the path exists, S042 id not reused anywhere (dup check), S041's
other cells byte-identical to base ({BASE}) except used-by (`git diff {BASE} -- corpus/SOURCES.md`
must show exactly: one added row + one used-by cell change + any log lines). Then run the census CLI
and paste. Any extra drift is a defect — name it. Receipt: {W1}/RevRegistryC2.md.""")

add("RevManifestC2", "reviewer", f"""Q9 review of the round-28 manifest after ExecManifest lands
(PRE-STATE if absent): (1) every record's path stem equals its id; (2) every sha256 matches the on-disk
capture (sha256sum both); (3) every quote occurs exactly once in its capture OR carries an `anchor`
line number — re-run each assertion yourself with grep -c (paste counts); (4) quotes are <=25 words;
(5) run source-recheck.py on both sources and paste exits. Any quote found twice with no anchor is a
Q9 failure — name it. Receipt: {W1}/RevManifestC2.md.""")

add("RevCounters1", "reviewer", f"""Independent counter re-run (C1): after the impl lands, re-run all
four frozen C1 counter commands from the lane root yourself (do not trust seat receipts): paste each
command, its output, its exit, and the UTC timestamp; compare each against the frozen after-values in
claims.json (bad-fixture exit 1; bounties 1 line; selftest receipt conditions; SKILL exit 0 bad=0
LOST=306). State PASS/FAIL per counter. If PRE-STATE, run anyway against the pre-change bytes, record
the observed before-values, and say the after re-run is owed at close. Receipt: {W1}/RevCounters1.md.""")

add("RevCounters2", "reviewer", f"""Independent counter re-run (C2): after the C2 artifacts land, re-run
all four frozen C2 counter commands yourself: frontier awk (expect 12), entries-citing-S042 (expect 1),
S042 row count (expect 1) + census CLI exit 0, harness (expect entries=15 pass=15 exit=0). Paste
commands/outputs/timestamps; PASS/FAIL each. PRE-STATE: run against current bytes, record observed
values, name the owed re-runs. Receipt: {W1}/RevCounters2.md.""")

add("RevCensusEnd", "reviewer", f"""Round-end census verification: run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
after the registry lands; paste the FULL output and exit code. Also run the seven frozen manual census
commands from CORPUS.md §Census (rows, malformed=0, tier histogram, status histogram, dup ids empty,
enum/tier-inflation empty, mined used-by paths exist) against corpus/SOURCES.md and paste each output.
Report rows before (41) vs after (expect 42) with the counting command. Any non-zero malformed or a new
E-code is a conformance defect — name it. Receipt: {W1}/RevCensusEnd.md.""")

add("RevDensityGuard", "reviewer", f"""Guard the density axis (score 9): run `python3 corpus/instruments/density.py
SKILL.md --label r28-guard` after ALL lands; compare mean / blocks / path-citation instances against
the frozen before (154.0 / 19 / 652 — verify against the round-25 committed receipt if numbers differ;
the instrument is unchanged so the comparison is valid). Also `git diff {BASE} --stat -- SKILL.md
corpus/knowledge/ corpus/README.md` — name every touched file; SKILL.md changes must be append-only
(R6). Any density drop or non-append SKILL.md edit is a harm — name it. Receipt: {W1}/RevDensityGuard.md.""")

add("RevReceiptsCanon", "reviewer", f"""Receipt completeness review: after the wave settles, list every
frozen counter/kill-rule/claim condition and map each to the receipt(s) covering it ({R28}/receipts/
and {W1}/). Name every gap. Confirm defect-4 conformance: NO file named c1-receipt-index.txt or any
canonical receipt exists yet under {R28}/ root (only the L1 creates it at close, at the landed digest).
Confirm every receipt carries its instrument/artifact sha256 and UTC timestamp. Receipt:
{W1}/RevReceiptsCanon.md.""")

add("RevCloseCheck", "reviewer", f"""Final close-out checklist against the round contract: (1) every
production change maps to the ownership map and to a wave receipt; (2) the four routed dispatch
requirements from claims.json are each evidenced (reviewer seats in THIS wave — count them; inline Gate
quotes in the lesson; one canonical receipt still owed at close; expected-list reconciliation);
(3) misroot sweep evidence exists (ExecScopeSweep); (4) no fleet-root writes; (5) lesson Gate has
>=1 admit and >=1 reject with quotes; (6) do-nothing receipts exist (r27+ r28 before receipts).
Produce the go/no-go list with pointers. Receipt: {W1}/RevCloseCheck.md.""")

# ---------------- critics (5) ----------------
add("CritC1Vacuity", "critic", f"""Vacuity attack on C1: can any after-value be reached WITHOUT the
claimed work? Build the do-nothing control explicitly: the pre-change instrument (digest
c2a9e6c6...) on both fixtures reaches exit 0 / 0 lines (re-run and paste) — already known; now attack
the selftest: could `--selftest` print `selftest cases=N failures=0` with ZERO real fixtures
(degenerate: cases=0, or fixtures that assert nothing)? Read the impl (or diff) and try to construct
a vacuous pass; if you cannot, state the blocking code with line evidence. Also attack exit-code
reachability: is there any path where exit 1 comes from something OTHER than a fail-class verdict
(e.g. a parse error masquerading)? Receipt: {W1}/CritC1Vacuity.md.""")

add("CritC1Kill", "critic", f"""Kill-rule attack on C1: the kill rule fires on non-isolating fixtures.
Attempt to PROVE a fixture non-isolating: for each selftest fixture in the landed impl (or diff),
trace whether it can fail for a reason in ANOTHER limb (e.g. the MISSING-FILE fixture failing because
of the absent bounties root rather than the mirror override). Run the selftest with deliberate
env perturbations (KASEGI_MIRROR set/unset, KASEGI_BOUNTIES set) and record which cases flip.
Any cross-limb flippage is a kill — name the fixture and the perturbation. Receipt: {W1}/CritC1Kill.md.""")

add("CritC2Admission", "critic", f"""Admission attack on C2: argue the STRONGEST case that F12 should
NOT be admitted: (a) is the entry's core claim (起算日 as coordinator-told disclosure clock) actually
supported by BOTH captures, or does one capture not contain it? (b) does F12 duplicate F11 ground
(use ScribeStagedCompare's map)? (c) is S042 tier-A justified for this scope or is a process page
only tier-B? (d) does the staged entry's claim skeleton contain any claim the re-grounded entry
dropped silently? Read the captures at the cited anchors and paste what you find. Verdict: the
admission survives or dies on these points — say which with evidence. Receipt: {W1}/CritC2Admission.md.""")

add("CritC2Kill", "critic", f"""Kill-rule attack on C2: attempt to violate each kill-rule clause without
doing the work: (1) can the frontier awk count reach 12 by editing an EXISTING row's status instead of
admitting F12? (2) can entries-citing-S042 reach 1 with a stub entry failing Q1? (3) can the census
stay exit 0 with a malformed appended row (test the 0-3-space indented-row blind spot on a scratch
copy of the registry — a row indented 4+ spaces is ignored by the census; is that reachable here?)?
(4) can the harness pass 15/15 with the entry's recheck pointing at the wrong manifest (R12)? Each
attempt: describe, test in scratch, report the outcome. Receipt: {W1}/CritC2Kill.md.""")

add("CritGlobal", "critic", f"""Whole-claim falsification pass: read the final (or in-flight) state of
both claims' artifacts and argue each claim FAILED or is unprovable-as-stated: are the before-values
honest (re-run one before counter yourself from base {BASE} via git archive or the committed r27/r28
before receipts)? Is any after-value measured against mutable bytes instead of committed bytes (R3)?
Is any claim a re-score of an existing rule on new inputs rather than a surface move (§9 naming
rule)? Is 'no axis harmed' true anywhere outside SKILL.md (the corpus LOST-RECORDED growth — is it
harmed or disclosed)? Produce the strongest honest counter-case; the L1 answers each point in the
report. Receipt: {W1}/CritGlobal.md.""")

# ---------------- mutation-testers (5) ----------------
add("MutExitC1", "mutation-tester", f"""Mutation-test the exit-code limb: on a SCRATCH copy of the
landed instrument (or pre-change bytes if the impl has not landed — label it), create mutants:
M1 remove the exit-1 (always exit 0); M2 exit 1 unconditionally; M3 drop BASE-ABSENT from the fail
set; M4 drop PIN-BROKEN from the fail set. Run each mutant against: the bad-fixture, the bounties
fixture, the selftest, and SKILL.md. Expected: M1 fails bad-fixture (still exit 0), M2 fails SKILL.md
(exit nonzero on clean input), M3 fails the selftest BASE-ABSENT limb, M4 fails the PIN-BROKEN limb.
Paste a table: mutant x test -> score. Any mutant passing everything is a live mutation — name it.
Work ONLY in {R28}/wave1/MutExitC1/ (copy the instrument there; never edit the live file).
Receipt: {W1}/MutExitC1.md.""")

add("MutArmC1", "mutation-tester", f"""Mutation-test the bounties arm: scratch copy. Mutants: M1 remove
the bounties alternative from CITE entirely (bounties cite becomes invisible again); M2 remove the
realpath confinement for the bounties arm only (escapes would classify in-range instead of
OUTSIDE-BASE); M3 point the bounties root at the mirror candidates by mistake. Score each against the
bounties fixture + an escape fixture you write (`~/Projects/bounties/../etc/passwd:1`-shaped, in
scratch text) + SKILL.md (no new movement allowed). Expected kills: M1 -> 0 BOUNTIES lines; M2 ->
escape not OUTSIDE-BASE; M3 -> wrong absence verdict. Paste the table. Receipt: {W1}/MutArmC1.md.""")

add("MutSelftestC1", "mutation-tester", f"""Mutation-test the selftest completeness: scratch copy.
Mutants: M1 report `selftest cases=0 failures=0` (skip all fixtures); M2 drop one fixture silently
while keeping the count accurate (does the count drop get noticed? the frozen predicate binds cases=N
— what N is frozen? If none, completeness is the only guard — attack it); M3 make one fixture assert a
trivially-true condition. Score each against the frozen counter (c): does the receipt-line condition
catch it? The kill rule says a limb with no failing fixture kills C1 — demonstrate the catch or name
the gap. Paste the table with the exact outputs. Receipt: {W1}/MutSelftestC1.md.""")

add("MutQuoteC2", "mutation-tester", f"""Mutation-test the manifest quote binding: scratch copy of the
manifest + captures ({R28}/wave1/MutQuoteC2/). Mutants: M1 change one quote's final character; M2
swap two quotes between S041 and S042 records; M3 set one quote to a string occurring twice (remove
its anchor). Run source-recheck.py against each mutant. Expected: all three exit non-zero naming the
failing assertion. Any mutant exiting 0 is a live mutation — name it and the assertion it fooled.
Receipt: {W1}/MutQuoteC2.md.""")

add("MutManifestC2", "mutation-tester", f"""Mutation-test the Q9 stem/sha binding: scratch copy.
Mutants: M1 rename S042.txt to S042b.txt in the manifest path (stem != id); M2 set S041's sha256 to
S042's (path/id bound to wrong bytes); M3 point both records at the same capture file. Run
source-recheck.py on each. Expected: all exit non-zero. Any pass is a live mutation — name it.
Receipt: {W1}/MutManifestC2.md.""")

# ---------------- revengers (2) ----------------
add("RevengerC1", "revenger", f"""Reverse-engineer the C1 change's fidelity to original intent: read the
anchorcheck.py git history (`git log --oneline -- corpus/instruments/anchorcheck.py` + the r15/r18/r19
commits' versions) and the round-15..27 lessons' instrument requirements; enumerate the documented
behaviors the round-28 change must PRESERVE (verdict-class separation, LOST-RECORDED semantics, pin
handling, LANE_DIRS resolution order, derived roots, printed line format for semantic review).
Then diff the landed impl (or {W1}/ExecImplC1.diff) against that list: any documented behavior lost,
weakened, or silently changed? The printed per-line and summary formats are consumed by other
receipts/grep patterns — check the new output still matches the frozen counter sed/grep shapes in
claims.json (the `== ... bad;` and `LOST-RECORDED=` summary forms). Receipt: {W1}/RevengerC1.md.""")

add("RevengerC2", "revenger", f"""Trace the staged entry to ground: for EVERY claim in the landed
knowledge/japanese-domestic-disclosure-workflow.md (or the staged skeleton if not yet landed), find
its origin in the staged package bytes and its re-grounded anchor in the round-28 captures. Produce
the claim-traceability table: claim -> staged line -> capture file:line -> quote match (yes/no with
grep output). Any claim present in the staged entry but ABSENT or unsupported in the re-grounded entry
must be named (silent drops are defects); any NEW claim in the re-grounded entry without a capture
anchor is unsupported — name it. Receipt: {W1}/RevengerC2.md.""")

# ---------------- sentinels (2) ----------------
add("SentinelScope", "sentinel", f"""Scope and safety sweep of the wave's writes (run at your best
time; re-check after any late edit you notice): (1) `git -C {LANE} status --porcelain` — every
modified/untracked path must be in the ownership map or under .ufo/waves/round-28/ or receipts/;
(2) grep every new/changed file under corpus/ and .ufo/waves/round-28/ for credential patterns
(secret/token/cookie/op://, BEGIN PRIVATE KEY) — must be empty; (3) confirm no writes to {FLEET}
root, {SHOKU}, .ufo/state, .scratch, MANIFEST.json, templates/, fleet scripts/; (4) confirm the two
capture fetches used only the instrument UA on public URLs (read ExecCaptureS042/S041 receipts);
(5) confirm no fixture or test probed any live target (Q6 class check). Name any violation with its
path. Receipt: {W1}/SentinelScope.md.""")

add("SentinelQuality", "sentinel", f"""Quality-bar sentinel: independently sample-verify the admission
bar on the F12 entry (read the landed entry; if absent, PRE-STATE against the staged skeleton): pick
THREE load-bearing claims at random (seed from your own read), open the capture at each cited anchor,
and confirm the quote verbatim. Check the entry for universalized attribution (Q4 violations:
'Japan requires...' vs 'the IPA process page states...'), memory-typed numbers (any numeric claim must
match a capture line), and the Q6 documentation-only rule. Also verify the SKILL.md append is
append-only (`git diff {BASE} -- SKILL.md` shows only added lines at the end). Receipt:
{W1}/SentinelQuality.md.""")

# ---------------- simplifier (1) ----------------
add("SimplBloat", "simplifier", f"""Wave-evidence economy sweep (R14 practice): measure the byte size
of everything under .ufo/waves/round-28/ as it exists when you run (`du -sb` + `find -type f | wc -l`).
Flag any single artifact over 256 KiB that is NOT a capture snapshot or instrument (receipts should be
text, kilobytes at most). If ScribeLesson/others produced oversized control trees, recommend the R14
remedy (content-addressed tarball with sha256 in the receipt, or git-archive regeneration note) with
the exact commands. Confirm no full-corpus fixture copies were committed this round (compare against
the round-25 mistake: c1-after-35 was a full corpus copy). Receipt: {W1}/SimplBloat.md.""")

AXES = {
    "ScoutDatawalk": ["depth:verifiability", "coverage"], "ScoutIpaRecon": ["coverage"],
    "ScoutJpcertRecon": ["coverage"], "ScoutAssimilation": ["coverage"],
    "ScoutGateRegistry": ["depth:verifiability"],
    "ConnOverlap": ["coverage"], "ConnClaims": ["depth:verifiability", "coverage"],
    "ConnStagedCensus": ["coverage"],
    "ExecImplC1": ["depth:verifiability"], "ExecInstrReadme": ["depth:verifiability"],
    "ExecCaptureS042": ["coverage"], "ExecCaptureS041": ["coverage"],
    "ExecManifest": ["coverage"], "ExecHarnessC2": ["coverage"],
    "ExecCensusDry": ["coverage"], "ExecExpectedList": ["depth:verifiability"],
    "ExecNoHarmC1": ["depth:verifiability"], "ExecFixtureRun": ["depth:verifiability"],
    "ExecC2Counters": ["coverage"], "ExecRecheckAuditR28": ["depth:verifiability"],
    "ExecScopeSweep": ["depth:verifiability", "coverage"],
    "ExecReceiptCanonC1": ["depth:verifiability"], "ExecReceiptCanonC2": ["coverage"],
    "ExecSkillGateSupport": ["depth:verifiability"], "ExecInstrSelftest": ["depth:verifiability"],
    "ExecGateLog": ["depth:verifiability", "coverage"],
    "ScribeEntryC2": ["coverage"], "ScribeRegistryC2": ["coverage"],
    "ScribeReadmeC2": ["coverage"], "ScribeR14": ["depth:verifiability"],
    "ScribeSkillGate": ["depth:verifiability"], "ScribeStagedCompare": ["coverage"],
    "ScribeLessonGate": ["coverage"], "ScribeLesson": ["depth:verifiability", "coverage"],
    "ScribeLog": ["depth:verifiability", "coverage"], "ScribeScorecard": ["depth:verifiability", "coverage"],
    "ScribeSourcesGate": ["coverage"], "ScribeReportDigest": ["depth:verifiability", "coverage"],
    "ScribeReceiptsC2": ["coverage"], "ScribeFrontierNote": ["coverage"],
    "ScribeQualityCross": ["coverage"], "ScribeCensusNote": ["coverage"],
    "RevImplC1": ["depth:verifiability"], "RevFixturesC1": ["depth:verifiability"],
    "RevNoHarmC1": ["depth:verifiability"],
    "RevEntryC2": ["coverage"], "RevRegistryC2": ["coverage"], "RevManifestC2": ["coverage"],
    "RevCounters1": ["depth:verifiability"], "RevCounters2": ["coverage"],
    "RevCensusEnd": ["coverage"], "RevDensityGuard": ["depth:verifiability", "coverage"],
    "RevReceiptsCanon": ["depth:verifiability", "coverage"], "RevCloseCheck": ["depth:verifiability", "coverage"],
    "CritC1Vacuity": ["depth:verifiability"], "CritC1Kill": ["depth:verifiability"],
    "CritC2Admission": ["coverage"], "CritC2Kill": ["coverage"],
    "CritGlobal": ["depth:verifiability", "coverage"],
    "MutExitC1": ["depth:verifiability"], "MutArmC1": ["depth:verifiability"],
    "MutSelftestC1": ["depth:verifiability"], "MutQuoteC2": ["coverage"],
    "MutManifestC2": ["coverage"],
    "RevengerC1": ["depth:verifiability"], "RevengerC2": ["coverage"],
    "SentinelScope": ["depth:verifiability", "coverage"], "SentinelQuality": ["coverage"],
    "SimplBloat": ["depth:verifiability"],
}
spec = {
    "wave": "kasegi-r28-build",
    "context": CONTEXT,
    "reportDir": W1,
    "maxLanes": 128,
    "axes": ["depth:verifiability", "coverage"],
    "milestone": "round-28 build+attack wave: C1 anchorcheck fail-closed + C2 F12 assimilation",
    "items": [{"name": it["name"], "role": it["agent"], "axes": AXES[it["name"]],
               "milestone": "round-28", "prompt": it["task"]} for it in ITEMS.values()],
}
out = os.path.join(LANE, R28, "wave1-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(i["agent"] for i in ITEMS.values())
total = sum(c.values())
flash = sum(v for k, v in c.items() if k in ("executor", "scribe", "labrat", "sonic", "simplifier"))
attack = sum(v for k, v in c.items() if k in ("reviewer", "critic", "mutation-tester", "labrat"))
print("total", total, dict(c))
print("m_flash", flash, f"{flash*100//total}%", "attack", attack, f"{attack*100//total}%")
print("wrote", out)
