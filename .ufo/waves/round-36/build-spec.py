import json, textwrap

LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE="cc692008b0cfd58d18275aa6c4aed79620120799"
FREEZE="b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6"
R35BASE="3266c9937b03062d9bbc2f436e20820115ed179c"
R35HEAD="0aee0ef105395a2f1d6ace7eaeef13871bb26988"

CTX = f"""# Round
kasegi-shokunin round 36, dispatched by the L1 (agent KasegiR36) via the inline spawn handoff (hyaku run 9). Lane repo {LANE} is the ONLY lane repo. The fleet root /home/vgpnk/Projects/shokunin is read-only to you — never write there. /home/vgpnk/Projects/shokuknow (shokuknow campaign) is read-only — never write there, never run its campaign tools. Base commit {BASE}; claims-freeze commit {FREEZE}; frozen claims at {LANE}/.ufo/waves/round-36/claims.json (do not edit; corrections land as separate appended files).

Frozen claims:
- C1 depth:verifiability (score 4, held): a committed instrument corpus/instruments/r36-closure.sh runs over a `git archive` export of a named lane head (--export-ref <hash>) and prints closed=9/9 exit=0 on the round-36 final lane head; --selftest prints cases=9 failures=0. Checks E1-E9 close the round-35 verifier spot-check's routed defects and the closure-order defects: E1 structural placeholder/hash binding (no 'filled by the L1' / '<LANE_HASH>' tokens; the Final lane commit line's hash exists and is an ancestor), E2 round-34 depth:density erratum present, E3 SKILL.md Gates & probes registry rows for exact basenames r35-defect-closure.sh AND r36-closure.sh, E4 round-35 wave1-results.json tracked with provenance note, E5 claims-erratum-d5.md present, E6 L1Integration.md has 'Correction (round 35)', E7 QUALITY.md supersedes-R22/R23 rows present, E8 false-evidence-line correction recorded in the round-36 lesson, E9 quiescence (git status --porcelain empty; no leftover /fast/scratch/hyaku/kasegi-r36 seat dirs). Suite must fail on the r35 base export {R35BASE} (closed=0/9) and on the r35 judged head export {R35HEAD} (closed<9/9).
- C2 coverage (score 7, held): Frontier F19 (FIRST EPSS, exploitation-likelihood scoring) admitted 18->19; registry row S053 added (tier A, mined, opened 2026-10-26); knowledge entry corpus/knowledge/epss-exploit-prediction-scoring.md cites `source: S053`; harness entries=22 pass=22 exit=0 incl. PASS F19 ids=S053; source-recheck S053 exit 0; census exit 0; knowledge 47->48; junk twin c2-controls/junk-f19.md rejected.
- Non-claim frontier items: quarantine slice re-derived + id-collision rerun (Assimilation: none); considerthese 2026-10-26 proposals 3 and 5 adopted; mistakes M36-1..M36-4 minted in the round-36 lesson.

Read your item spec below fully before acting. You are a leaf seat (no subagent spawning except one read-only labrat probe allowed for executors). Work only your item. No output placeholder/plan text - land real evidence.

Write scope. Your ONLY allowed writes are (1) your receipt at {LANE}/.ufo/waves/round-36/wave1/<SEATNAME>.md (write it last), and (2) scratch files under your scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit any file in the lane repo, the fleet repo, sibling lane repos, or source trees (/home/vgpnk/Projects/shokuknow, ~/Projects/*). Never run a mutating git/jj command (no commit/add/reset/checkout/switch/push/fetch/stash/init except inside a `D=$(mktemp -d) && git -C "$D" init -q` fixture whose toplevel you verified equals $D). Read-only git (log/show/diff/status/rev-parse/ls-tree/ls-files/archive/cat-file/merge-base) is fine.

Scratch. HYAKU_SCRATCH defaults to /fast/scratch/hyaku. Create /fast/scratch/hyaku/kasegi-r36/<SEATNAME>/ with mkdir -p and bind ALL scratch/work copies there; never let it rely on an inherited TMPDIR; /tmp is only for files under 50 MB. Remove your scratch dir before you yield (trap 'rm -rf -- "$S"' EXIT in shell; finally: shutil.rmtree in Python), after copying receipts into the wave dir.

Tooling. Tooling authorization (operator 2026-10-19): you may install/upgrade tools that help the task, after reading /home/vgpnk/.omp/agent/RULES.md (official channels only; record tool/version/channel/reason in your receipt). pacman transactions are PAUSED host-wide — never run pacman; use `uv tool install`, `npx`, or an official binary into ~/.local/bin instead. Never edit ~/.omp/agent/config.yml or ~/.omp/agent/mcp.json (operator-owned).

Rules. Keep moves that improve an axis and harm none. Do not message agent://all. Do not run your own swarm. A seat keeps the route chain it captured at spawn."""

def item(name, role, axes, task):
    return {"name": name, "role": role, "axes": axes, "milestone": "round-36", "prompt": CTX + "\n\nYour item — " + name + " (" + role + "):\n" + task}

items = []

# ---------------- EXECUTORS (18) ----------------
items.append(item("ExecC1SuiteBuild","executor",["depth:verifiability"],"""
Write the committed instrument `corpus/instruments/r36-closure.sh` (as a DRAFT in your scratch; the L1 lands it). Requirements:
- Bash, `bash -n`-clean, every path absolute os under a `cd {LANE}` prefix; honours TMPDIR; never writes /tmp hardcoded (accept --work dir).
- Runs in EXPORT MODE: `--export-ref <hash>` extracts the lane tree via `git -C {LANE} archive <hash>` into a scratch dir and runs every check against THAT export (never the live worktree). Plain run (no --export-ref) must refuse with exit 2 and an explicit message.
- Nine checks E1..E9 per the frozen claim (see context): E1 placeholder/hash binding (grep -cF 'filled by the L1' and '<LANE_HASH>' over SCORECARD.md from the export must be 0; and the `Final lane commit:` line's 40-hex value must satisfy `git -C {LANE} cat-file -e <hash>` AND `git -C {LANE} merge-base --is-ancestor <hash> <exported-ref>`), E2 grep -c '201.2' SCORECARD.md >=1, E3 grep -cF 'r35-defect-closure.sh' SKILL.md >=1 AND grep -cF 'r36-closure.sh' SKILL.md >=1, E4 `git ls-files .ufo/waves/round-35/wave1-results.json` = 1 AND a provenance note file exists beside it, E5 test -e .ufo/waves/round-35/claims-erratum-d5.md, E6 grep -cF 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md >=1 (find exact path from `git ls-tree -r --name-only <export>`), E7 grep -cF 'supersedes R22' corpus/QUALITY.md >=1 AND 'supersedes R23' >=1, E8 grep -cF 'M36' corpus/lessons/round-36.md >=1 AND grep -cF 'source-recheck exit 0 on committed bytes' corpus/lessons/round-35.md == 0 (the stale line must be gone; if it exists, E8 fails), E9 `git -C {LANE} status --porcelain` empty AND `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d` empty.
- Prints one line `closed=K/9 exit=E` plus per-check `E<n> ...` payload lines. `--selftest` prints at least 9 `selftest case=<name>` verdict lines with `failures=0` and exit 0; summary-only forgery (cases=0 failures=0) must not satisfy it.
- Do NOT create the file in the lane: put the complete script text in your receipt (plus in scratch). Include the sha256 of your draft. State `bash -n` result.
"""))
items.append(item("ExecC1Fixtures","executor",["depth:verifiability"],"""
Build a fixture set proving each of E1..E9 can fail (red) and pass (green). In scratch, create a mini lane snapshot (git archive of BASE or a synthetic tree) and produce:
- per-check red fixture: a tree where exactly that defect is present; run your draft r36-closure.sh (from ExecC1SuiteBuild's scratch or your own draft if absent) against it and record the failing check (exit 1, `closed<9/9`).
- per-check green fixture: the same tree with the defect fixed → check passes.
- one `--selftest` case per check showing it can fail.
Record in your receipt: fixture inventory, each red/green exit, and a matrix check->red_exit->green_exit. Prove the matrix is not vacuous: every red fixture must fail at least its own check.
"""))
items.append(item("ExecC1ExportMode","executor",["depth:verifiability"],"""
Prove the export-mode discipline: build or reuse ExecC1SuiteBuild's draft suite; verify (1) `--export-ref` runs extract via `git archive` and no check reads the live worktree (e.g., temporarily break a live file in a scratch COPY of the lane env and show the suite output unchanged, or show the suite's checks all stat under the export root); (2) a run without --export-ref exits 2; (3) the suite does not create or modify anything under the lane (run with a clean lane and confirm `git status --porcelain` stays empty). Record commands + outputs.
"""))
items.append(item("ExecC1BaseFail","executor",["depth:verifiability"],"""
With the draft r36-closure.sh, run: `--export-ref {R35BASE}` (round-35 base) → expect `closed=0/9 exit=1` with E1/E3/E5/E6/E7/E8 open at least; and `--export-ref {R35HEAD}` (round-35 judged head) → expect `closed<9/9 exit=1` (E1 or E3 or E8 open). Record full stdout. If your draft can't run, record the blocker precisely (missing file etc.) and note it - do not fake output.
"""))
items.append(item("ExecC2Capture","executor",["coverage"],"""
Fetch the primary source for F19: the FIRST EPSS documentation page `https://www.first.org/epss/` using the instrument UA `kasegi-shokunin/1.0`. Follow redirects; record final URL, HTTP status, content-type, served bytes. Normalize the capture: strip markup (like the <u> example), collapse whitespace, keep UTF-8. Produce in scratch:
- S053.txt (normalized text capture),
- manifest.json for corpus/source-snapshots/round-36/: records array with {url (exact registry URL), fetched_utc (strict ISO8601 UTC), fetched_bytes, sha256, lines, normalized} plus pinned quote entries Q1..Q4: {quote (<=25 words), line/occurrence anchor} chosen from the page text (recommend: Q1 the model definition sentence 'EPSS is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.'; Q2 the 0-1 probability/percentiles sentence; Q3 the 'every day for every CVE' + free/open CSV/API sentence; Q4 the SIG/maintained sentence).
- verify each quote occurs exactly once in the normalized capture (use grep -cF and print counts).
Put the full manifest JSON and S053.txt content into your receipt (or a copy path under scratch). Do NOT write to the lane.
"""))
items.append(item("ExecC2Harness","executor",["coverage"],"""
In scratch, assemble the proposed round-36 tree state: `git archive` of BASE + (a) the drafted entry corpus/knowledge/epss-exploit-prediction-scoring.md (from ScribeEntryF19's receipt), (b) the drafted S053 row + search-log bullet (from ScribeRowS053), (c) knowledge-expected.txt with the entry appended (47->48). Then run from that tree:
- `python3 corpus/instruments/frontier-recheck-count.py` → expect entries=22 pass=22 exit=0 incl. `PASS F19 ... ids=S053`.
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` → exit 0 with occurrences=1 per quote.
- `python3 corpus/instruments/recheck-audit.py` → strict pass=48/48, expect=present expected=48 missing=0 unexpected=0 exit=0.
- `python3 corpus/instruments/capture-binding-check.py` → exit 0 (records bound).
Record every command and its full output. If a draft is missing, note it explicitly and run what exists; do not invent outputs.
"""))
items.append(item("ExecC2JunkControl","executor",["coverage"],"""
Build the junk twin control `c2-controls/junk-f19.md` content (in scratch; L1 lands it): a fake knowledge entry that mimics the real F19 entry header (source: S053) but carries a fabricated quote sentence that does NOT occur in the normalized capture (e.g., 'EPSS guarantees exploitation within 30 days'). Then demonstrate:
- `grep -cF '<fabricated sentence>'` over S053.txt → 0 (the discriminating invocation),
- running the harness/source-recheck selection with the junk entry's recheck line → must fail (quote-not-found / non-admission),
Record both as the discriminating control evidence. Also attempt an alternate twin: one whose quote DOES occur but whose `source:` is wrong (--source S052) → must fail.
"""))
items.append(item("ExecScoreGap","executor",["depth:verifiability","calibration"],"""
Compute the distance-to-next-score for depth:verifiability (4->5) and coverage (7->8) using the lane's score-gap instrument if possible: run `python3 corpus/instruments/score-gap.py` (if it exists; else implement the read-only computation in scratch enumerating the recorded next-score thresholds from SCORECARD.md §Saturation and PROVINCE/QUALITY). Record: current values, the concrete gaps, and any threshold that is undefined (state it). Output a short table in your receipt. Do not modify lane files.
"""))
items.append(item("ExecInstrumentsSynopsis","executor",["depth:verifiability","freshness"],"""
Run EVERY committed instrument's selftest/plain gate on the current base tree (read-only) and record results: density.py (SKILL.md), resolve.py, anchorcheck.py SKILL.md, mirror-containment-check.py, source-recheck.py (selftest + a known S row, e.g., S051/S052), capture-binding-check.py (selftest + plain), frontier-recheck-count.py, recheck-audit.py, kill-rule-check.py, r-defect-closure.sh, r35-defect-closure.sh, limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json. Table: instrument -> command -> exit -> key output line. Flag any failure/red (that is the no-harm baseline). 
"""))
items.append(item("ExecRegressionBase","executor",["depth:verifiability","coverage"],"""
Replay the before controls at the base commit (read-only): reproduce the values in .ufo/waves/round-36/c1-controls/before.txt and c2-controls/before.txt (frontier 18, registry 52, S053 0, entries citing 0, knowledge 47, harness 21/21, suite missing, r35 registry exact basename 0, worktree clean, scratch 0) and confirm each matches. Also verify claims.json literals are satisfiable at base (e.g., 'filled by the L1' count 0, '201.2' presence, 'Correction (round 35)' presence, supersedes R22/R23 presence, round-35 results tracked). Record a MATCH/DIFF table.
"""))
items.append(item("ExecQuiescenceProbe","executor",["depth:verifiability"],"""
Implement E9's quiescence check as a standalone reusable command (draft) and prove it can fail: (1) on the real lane now (`git status --porcelain | wc -l` and `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l`) → record; (2) in a scratch sandbox, create a fake dirty tree (touch a file) and a fake leftover scratch dir and show the E9 gate exits 1 (red); (3) clean state → exit 0 (green). Record red/green outputs.
"""))
items.append(item("ExecAncestry","executor",["depth:verifiability"],"""
Verify the ancestry requirement for E1: for each 40-hex token that appears in SCORECARD.md 'Final lane commit:' paragraphs (use `grep -oE '[0-9a-f]{40}' SCORECARD.md`), run `git -C {LANE} cat-file -e <h>` (exists) and `git -C {LANE} merge-base --is-ancestor <h> master` (ancestor). Produce a table of token -> exists -> ancestor. Also confirm the current branch tip hash and print `git rev-parse master`. Do not modify anything.
"""))
items.append(item("ExecC2QuoteOnce","executor",["coverage"],"""
Independently verify the F19 quote anchoring: with the normalized S053.txt (from ExecC2Capture), for each pinned quote Q1..Q4 (and the junk sentence), print `grep -cF '<quote>'` occurrence counts (must be 1 for pinned, 0 for junk). Also verify the entry's recheck command line (from ScribeEntryF19) is `bash -n`-parseable and carries `cd {LANE} &&` and `--source S053`. Record all outputs.
"""))
items.append(item("ExecDatawalk","executor",["depth:verifiability","calibration"],"""
Walk the round-35 verifier spot-check's §5 routed defects 1-6 against the base tree and produce an open/closed matrix with the exact command + output for each: (1) close-against-one-head (suite runs on git archive export - test the current r35-defect-closure.sh has no export mode), (2) re-claim with frozen evidence, (3) D1 file-wide literal (show `grep -cF 'filled by the L1' SCORECARD.md` = 0 but also that a section-scoped grep would be needed for r35 section), (4) append-not-rewrite (mark the D6 rewrite location), (5) false evidence lines (grep 'source-recheck exit 0 on committed bytes' corpus/lessons/round-35.md). (6) dirty tree at closure (git status now). This matrix grounds C1's E1-E9 selection. Record as a table.
"""))
items.append(item("ExecCensusReplay","executor",["coverage"],"""
Run the census command twice and record outputs and exit codes: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (expect exit 0, W04 S028/S029 only). Also run the three frozen census greps (rows, tier histogram, status histogram, duplicate ids, enum violations, mined used-by existence) and record. This is the before census evidence.
"""))
items.append(item("ExecManifestChecks","executor",["coverage"],"""
Validate the proposed round-36 capture manifest schema (from ExecC2Capture): fields url/fetched_utc/fetched_bytes/sha256/lines/normalized on every record; url must equal the registry row URL exactly; fetched_utc must be strict ISO8601 with Z. Run `python3 corpus/instruments/capture-binding-check.py` logic manually against the scratch manifest (or the instrument with --manifest pointing at scratch) and report bound/unbound counts. Record outputs.
"""))
items.append(item("ExecSiblingSweep","executor",["adjacency","coverage"],"""
Read-only sweep of sibling lane corpora for EPSS/exploitation-likelihood ground: grep -rilE 'EPSS|exploit prediction|exploitation likelihood|probability.*exploit|percentile' /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md (exclude kasegi-shokunin). Also check /home/vgpnk/Projects/shokuknow/doctrine/ for a host/channel assignment touching first.org. Produce a hit table (lane, file, line, token) and a ruling: contested/ratified. This grounds the adjacency report.
"""))
items.append(item("ExecGateReviewPrep","executor",["depth:verifiability"],"""
Prepare the post-integration gate run script (draft, in scratch): a bash script that after integration will (1) run `bash {LANE}/corpus/instruments/r36-closure.sh --export-ref <hash>` on the final lane hash, (2) run the three C2 counters, (3) census validate, (4) `git -C {LANE} status --porcelain`. Print a template receipt with placeholders. Also verify the script itself is bash -n clean and does not write to the lane.
"""))

# ---------------- SCRIBES (12) ----------------
items.append(item("ScribeEntryF19","scribe",["coverage"],"""
Draft the full knowledge entry `corpus/knowledge/epss-exploit-prediction-scoring.md` (text goes in your receipt only; L1 lands it). It must satisfy QUALITY Q1-Q10: Q1 three header lines (source: S053 + URL + anchor; verified-at: 2026-10-26; recheck: one executable command with `cd {LANE} &&`, `--manifest corpus/source-snapshots/round-36/manifest.json --source S053`, bash -n-parseable, plus `#` note). Q2 load-bearing claims rest on tier A row S053. Q3 every claim carries a <=25-word verbatim quote with exact location (line anchors into S053.txt as pinned by ExecC2Capture Q1..Q4). Q4 attribution: FIRST's own statements; never generalize to universal rules. Q5 at least one falsifiable rule (e.g., 'EPSS output is a probability in [0,1] with per-CVE daily updates and the entry's recheck must print occurrences=1 for each pinned quote') and one rejected over-generalization with reason (e.g., NOT 'EPSS predicts exploitation' - it estimates probability; EPSS should not be used as a severity/reward scaler without policy grounding). Q6 documentation-only, no credential material, no instructions to probe anything. Use the content from S053.txt (the actual page text). Build the entry around: what EPSS is (model definition), its output (0-1 probability + percentiles), cadence/free access (CSV/API/github), and how it differs from CVSS severity and KEV catalog status (distinct axes), plus the observed page text only - do not add claims not in the capture.
"""))
items.append(item("ScribeRowS053","scribe",["coverage"],"""
Draft the SOURCES.md row for S053, the Search-log bullet, and the Paths update snippet. Row must match contract v1: 11 columns, no `|` inside any cell, id S053, source `FIRST EPSS documentation page — https://www.first.org/epss/`, kind docs, tier A scoped to FIRST's own EPSS statements, anchor = the S053.txt capture line numbers of Q1 (e.g., 'capture corpus/source-snapshots/round-36/S053.txt: <line> (sha256 <full>)'), teaches = one grounded learner benefit (e.g., 'EPSS estimates the probability a published CVE will be exploited in the wild within 30 days; treat it as a likelihood signal distinct from CVSS severity and KEV catalog status'), status mined, opened 2026-10-26, recheck 90d, used-by corpus/knowledge/epss-exploit-prediction-scoring.md. Search-log bullet: question/query/where (the fixed FIRST EPSS page), date 2026-10-26, identified/screened/included/excluded counts, stop rationale, and the negative sweep command output (grep across lane knowledge for EPSS/exploitation-likelihood = 0 hits). Paths: append a study path line `Exploitation likelihood — S053 → S052 → S001 → S002: ...`. Provide the exact lines in your receipt.
"""))
items.append(item("ScribeGateLesson","scribe",["depth:verifiability","coverage"],"""
Draft the round-36 lesson `corpus/lessons/round-36.md` (text in receipt) with a `## Gate` section containing: candidates considered (S053/EPSS entry; assimilation package staged entries; junk twin), admitted (F19 entry + S053 row with URL/access-date/<=25-word located quote), rejected (junk-f19 with reason; any staged entry that still fails its flip conditions; standing refusals), quarantine slice verdicts (from ScoutQuarantine), id-collision numbers (from ScoutIdCollisions), considerthese dispositions (proposal 3 and 5 adopted; 1 computed; 2/4/6/7 reasons), and the spot-check result placeholder. Also include the `## Mistakes` anchor text for M36-1..M36-4 to be filled by ScribeMistakes. Keep it as a complete draft a non-author can re-open.
"""))
items.append(item("ScribeMistakes","scribe",["depth:verifiability","calibration"],"""
Draft the `## Mistakes` rows M36-1..M36-4 for the round-36 lesson using the kaika §5 class vocabulary (landing, closure-order, stale-premise, counter-discrimination, number-drift, reference-drift, scope, attribution, provider):
- M36-1: recurrence of M35-1 (wave/closure ordering) — class landing/closure-order — evidence: round-35 verifier spot-check §5.1 and the watchdog complete-vs-commit timestamps — captured-by: none (new) — fix: the E9 quiescence gate + export-bound suite (r36-closure.sh) — shown able to fail: fake dirty tree red vs clean green.
- M36-2: false evidence lines at A (round-35 lesson Gate claimed 'source-recheck exit 0 on committed bytes' while the capture was uncommitted) — class stale-premise — evidence: verifier spot-check §5.5 — captured-by: R16 (result paragraph closure) — fix: E8 check + appended correction — able to fail: grep finds the stale line before, 0 after.
- M36-3: the r35 D3 registry row never landed (exact basename r35-defect-closure.sh absent; the near-name r-defect-closure satisfied the old literal) — class counter-discrimination — evidence: `grep -cF 'r35-defect-closure.sh' SKILL.md` = 0 at base — captured-by: R17 limb / R11 (discrimination) — fix: E3 exact-basename registry rows + mutant — able to fail: red fixture with only near-name row.
- M36-4: the report was re-filed/errataed after `complete` (verifier §5.4) — class landing — captured-by: R4 (landed = committed and pushed) — fix: full integration before the one report commit; report lands last — able to fail: check that report commit is after the final lane commit.
Each row: class · evidence pointer (command + output) · captured-by · fix · able-to-fail red/green. Put the complete table in your receipt.
"""))
items.append(item("ScribeScorecard","scribe",["depth:verifiability","coverage"],"""
Draft the round-36 SCORECARD.md section (text in receipt): a `## Round 36` block with (1) claims table C1/C2 with before (frozen controls) → after (expected) and verdicts pending measurement; (2) measurement state paragraph template (base/freeze hashes, suite digest, harness counts); (3) move-log rows for depth:verifiability and coverage; (4) saturation line + lowest non-retired axis restatement; (5) capabilities: no row enters (statement). Follow the round-34/35 section style. Keep every line anchor-stable for appending (R6).
"""))
items.append(item("ScribeShonen","scribe",["calibration"],"""
Draft the round-36 SHONEN.md box updates (text in receipt; L1 integrates): for each of the four boxes, keep `[~]` and write an evidence paragraph citing THIS round's intended artifacts (suite r36-closure.sh + selftest, census exit 0, harness 22/22, knowledge-expected sync, PROVINCE amendments F18/F19, LOG entry, lesson). Explicitly state what is still owed (non-author verification). Also include the fact that box 2 (end-to-end domain task) still has no new executed task.
"""))
items.append(item("ScribeLOG","scribe",["depth:verifiability","coverage"],"""
Draft the LOG.md round-36 entry (text in receipt): heading `## Round 36`, claims C1/C2 with summary, frontiers F18/F19 amendments, instruments added (r36-closure.sh), assimilation: none, considerthese proposals adopted, mistakes M36-1..4, wave shape. Keep it consistent with the scorecard and lesson drafts.
"""))
items.append(item("ScribeSOURCSCorrection","scribe",["depth:verifiability"],"""
Draft the R9-style appended correction for the S052 search-log bullet (M35-6 at `corpus/SOURCES.md:79`): a new Search-log paragraph stating the old bullet's digest abbreviation `d69349e8…77e8826` is wrong (should be `…e8826`) and its '7 SOURCES rows' count is wrong (the registry has 5 rows mentioning CISA: S003 S008 S021 S023 S026; 7 counted two `## Search log` bullets). Provide the exact appended text lines in your receipt (never edit `:79`).
"""))
items.append(item("ScribeQualityRows","scribe",["depth:verifiability","calibration"],"""
Draft two QUALITY.md additions (text in receipt):
- R28 (quiescence/head-closure criterion): a round's claims rest on committed paths at the quoted head; the counter/harness runs are recorded over `git archive <final lane commit>` exports; the lane is quiescent (`git status --porcelain` empty, no leftover scratch seat dirs) before filing. Grounded in: round-35 verifier spot-check §5.1 (§ M35-1 recurrence) + considerthese/2026-10-26.md proposal 3.
- R29 (exact-basename registration): an instrument is registered in SKILL.md Gates & probes by its exact basename (a near-name sibling does not satisfy the registry literal). Grounded in: M36-3.
Each row: id | criterion | grounded in. Follow the append-only table style (R6).
"""))
items.append(item("ScribeAssimilationGate","scribe",["coverage","adjacency"],"""
Draft the assimilation Gate block for the round-36 lesson: 'Assimilation: none' with (1) id-collision numbers from ScoutIdCollisions (registry vs staged ids, collision count, guard-proof), (2) quarantine slice verdicts from ScoutQuarantine (rows, per-row verdict, none adopted), (3) standing refusals re-confirmation from ScoutStandingRefusals (the seven staged entries with flip conditions still unmet). Keep the exact counts placeholders to fill from the scout receipts (complete them in the final draft; if a scout receipt is missing, mark the cell missing - never invent).
"""))
items.append(item("ScribeConsiderthese","scribe",["calibration"],"""
Write the disposition table for considerthese/2026-10-26.md proposals: proposal 1 (distance-to-next-score) → computed via ExecScoreGap, cited in scorecard; proposal 2 (end-to-end domain task round) → not this round (recorded; SHONEN box 2 remains open); proposal 3 (quiescence gate) → adopted as R28 + E9; proposal 4 (cap/externalise wave evidence) → not this round (needs operator/LFS decision); proposal 5 (F18 PROVINCE amendment) → adopted this round (plus F19); proposal 6 (cadence/depth) → recorded as reflection, no change; proposal 7 (proposal-status ledger) → recorded, not started. Cite file + date. Draft in your receipt.
"""))
items.append(item("ScribeReportDraft","scribe",["depth:verifiability","coverage"],"""
Draft the round-36 report skeleton (text in receipt) with all required sections in order: Work performed (naming claims C1/C2 and axes), Landed changes (bullets tied to LOG.md and commit hashes), Before → after measurements (one per claim, with counting commands and measured commits), Sources & frontier (rows before/after, added by tier, touched old→new, frontier advanced), Trend verdicts (expansion/quality/discernment + evidence), SHONEN (one line per box), plus the Stale-lane line, tooling installs line, and open L0 questions line. Fill in values from the other scribes where known; mark unknowns as `[MEASURE]` (the L1 fills after measurement). Ensure the SHONEN heading count is exactly one.
"""))

# ---------------- REVIEWERS (10) ----------------
items.append(item("RevClaimsFreeze","reviewer",["depth:verifiability","calibration"],"""
Review the frozen claims at {LANE}/.ufo/waves/round-36/claims.json: for every literal constant in predicates/kill rules/counters, check satisfiability against the base tree (run each grep/command): e.g., 'filled by the L1'=0, '<LANE_HASH>'=0, '201.2' >=1, 'Correction (round 35)' >=1, 'supersedes R22'/'R23' >=1, wave1-results tracked, frontier=18, registry=52, S053=0, knowledge=47, harness 21/21, suite missing. Produce a satisfy/fail table. Also verify the do-nothing control cannot meet the targets (run the control greps on the untouched base and show they equal the before values). Verdict: freeze OK or list defects.
"""))
items.append(item("RevC1Suite","reviewer",["depth:verifiability"],"""
Review the drafted r36-closure.sh (from ExecC1SuiteBuild) against: correctness of export-mode (no worktree reads), structural (not file-wide literal) E1/E3/E7 checks, bash -n cleanliness, cd-prefix, absence of hardcoded /tmp, TMPDIR honouring, kill-rule clauses (no count-zero escape). Run `bash -n` and the plain run's refusal path on a scratch copy (do not modify lane). Produce a defect list (severity) + verdict (ADMIT / REFUSE with repair paths).
"""))
items.append(item("RevC1Fixtures","reviewer",["depth:verifiability"],"""
Review ExecC1Fixtures' matrix: every fixture isolates exactly one limb (mutating only that limb), red fixtures fail only their own check, green pass, no shared mutation, counts per check. Reproduce two fixtures of your choice and report.
"""))
items.append(item("RevC1Selftest","reviewer",["depth:verifiability"],"""
Run the drafted suite's `--selftest` (from scratch) and verify: >=9 case lines, each prints `selftest case=<name>` verdict line, failures=0, exit 0; a summary-only forgery (cases=0 failures=0) is rejected (prove by constructing a forgery that prints only the summary). Report outputs.
"""))
items.append(item("RevEntryF19","reviewer",["coverage"],"""
Review the drafted F19 entry (from ScribeEntryF19) against QUALITY Q1-Q10 with the capture S053.txt (from ExecC2Capture) in hand: header trio, quotes <=25 words and exactly-once (verify by grep), attribution, falsifiable rule + rejected over-generalization, no credential/probe content, Q7 executable recheck (bash -n, cd prefix), Q9 three-way binding. Verdict ADMIT/REFUSE with repair paths. If the capture is missing, say so.
"""))
items.append(item("RevRowS053","reviewer",["coverage"],"""
Review the drafted S053 row + search-log bullet (from ScribeRowS053): 11 columns (NF=13), no `|` inside any cell, id order, tier/status/kind enums, opened/recheck forms, used-by exact paths exist in the proposed tree, search-log bullet has all counts, negative sweep evidence present. Also verify the row URL matches the manifest url in ExecC2Capture's manifest. Verdict: matches / list fixes.
"""))
items.append(item("RevSourceRecheck","reviewer",["coverage"],"""
Verify the F19 entry's recheck command line (per Q10): one executable command, bash -n parseable, carries `cd {LANE} &&`, `--manifest corpus/source-snapshots/round-36/manifest.json --source S053`, human note after `#`. Also verify it would fail-closed on a missing capture (exit 2). Run the bash -n checks in scratch. Report.
"""))
items.append(item("RevHarnessSync","reviewer",["depth:verifiability","coverage"],"""
Review the planned knowledge-expected.txt sync: entries count 47->48, comment lines kept, recheck-audit expectation `expected=48`, and the frontier harness entry addition. Verify the recheck-audit.py logic will count the new entry (read the instrument source). Report any risk (e.g., duplicate counting).
"""))
items.append(item("RevNoHarm","reviewer",["depth:verifiability"],"""
Assess planned round-36 changes for no-harm: compare the set of proposed file writes (entries, rows, lesson, scorecard append, PROVINCE append, SHONEN append, LOG append, QUALITY append, SKILL registry append, instruments) against base and verify no deletions/rewrites of existing lines, line anchors preserved per R6 (appends at EOF), and no core text edits. Use git archive exports. Report PASS/defects.
"""))
items.append(item("RevSpotCheckReadiness","reviewer",["calibration","depth:verifiability"],"""
Formulate the non-author spot-check sample plan for this round: at least one admit (F19 entry + S053 row) and one reject (junk-f19, quarantine verdicts) that a fresh reviewer should re-open, plus the census and suite rerun commands. Check that the drafted lesson Gate will contain all required blocks (URLs, access dates, <=25-word quotes). Report the plan and any gaps in the draft.
"""))

# ---------------- CRITICS (6) ----------------
items.append(item("CritC1Kill","critic",["depth:verifiability"],"""
Attack the drafted r36-closure.sh: attempt to make each E-check pass while its defect is present (e.g., E1 by removing the Final-lane-commit line or using a hash string in prose that satisfies grep while being a repudiation; E3 by a near-name row; E8 by a different phrase; E9 by deleting the check). Also test the kill-rule clauses: count-zero escapes, summary-only selftest, worktree fallback. Produce an attack matrix: attack -> survives/killed -> evidence. Verdict: which limits remain (report honestly; 'proved by its own selftest' is not accepted as proof - bind counters to bytes).
"""))
items.append(item("CritC1Export","critic",["depth:verifiability"],"""
Attack the export-mode discipline: try to make the suite read the live worktree (symlink, missing set -e, path traversal, unset --export-ref default), or pass with a tampered export (e.g., run against an export of a tree where a defect is fixed but claim it is the lane head). Also check the suite does not leave files behind. Report findings.
"""))
items.append(item("CritC2Kill","critic",["coverage"],"""
Attack C2: (1) fabricate S053 row without capture — census/counters must still fail (verify by grep/commands); (2) fabricate an entry with quote from the live page but no capture; (3) manifest with mismatched URL (must be caught by capture-binding-check); (4) junk twin acceptance (run source-recheck with the junk recheck line and show it must fail); (5) harness over-count (entry pass without row). Produce an attack matrix with commands + outcomes.
"""))
items.append(item("CritC2Claim","critic",["coverage"],"""
Verify causal separability of C2 counters: show that moving each counter alone (e.g., only the frontier row; only the row; only the entry; only harness) leaves the others at before values (run on a scratch tree). Also confirm the do-nothing control (untouched base export) scores all before values and thus cannot meet the after target.
"""))
items.append(item("CritMotivation","critic",["calibration"],"""
Check that the claims are not reachable by a do-nothing control: run all C1 and C2 counters on an untouched base export (git archive base) and show none meet the after targets (C1: suite missing, closed<9/9; C2: frontier 18, registry 52, entry count 0). Also confirm the claims are not already satisfied at base. Record.
"""))
items.append(item("CritBoundary","critic",["scope"],"""
Sweep every draft/plan in the wave (receipts under {LANE}/.ufo/waves/round-36/wave1/ once they appear; plus scan the wave dir .ufo/waves/round-36/) for: fleet-root writes (paths under /home/vgpnk/Projects/shokunin outside the lane), sibling lane writes, shokuknow writes, credential material (tokens/keys/private URLs/op://), and any instructions to mutate git/jj. Report each violation with file+line or state none. Also scan for a seat writing another seat's receipt.
"""))

# ---------------- MUTATION-TESTERS (5) ----------------
items.append(item("MutC1Suite","mutation-tester",["depth:verifiability"],"""
Mutation-test the drafted r36-closure.sh (from ExecC1SuiteBuild): for each of E1..E9, produce a one-limb mutant (exact-once find/replace over the suite bytes, still bash -n parseable) that removes/weakens that check; confirm the mutant's output differs from the unmutated run (kill command differs) and the mutant makes the suite report open/red for that check. Use the limb-mutation-check.py ledger pattern (corpus/instruments/limb-ledger.json). Report per-limb killed/survivor; a survivor is a defect (strengthen or report, never relabel).
"""))
items.append(item("MutC1Fixtures","mutation-tester",["depth:verifiability"],"""
Mutation-test the fixtures (from ExecC1Fixtures): flip each red fixture to green (fix the defect) and confirm the check then passes; flip a green to red and confirm it fails. Also add a vacuous fixture (asserting nothing) and confirm it is detected as vacuous. Report.
"""))
items.append(item("MutC2Entry","mutation-tester",["coverage"],"""
Mutate the drafted F19 entry: M1 drop `source:` line → harness must print no-source-line/exit 1; M2 paraphrase a pinned quote → quote-not-found; M3 wrong `--source` (S052) → exit 1; M4 remove recheck line → recheck-audit fails closed. Run each mutant against the scratch tree and record exit codes.
"""))
items.append(item("MutC2Row","mutation-tester",["coverage"],"""
Mutate the drafted S053 row: broken column count (12/14), embedded `|` in a cell, wrong status enum, duplicate id S053, wrong tier A->B (allowed? check enum only), URL mismatch vs manifest. For each, run the census validator on a scratch SOURCES.md and record exit codes (E03/E04 etc.). Report which mutations are caught.
"""))
items.append(item("MutJunkTwin","mutation-tester",["coverage"],"""
Verify the junk twin control discriminates: variants (a) junk with fabricated quote → source-recheck exit 1 quote-not-found; (b) junk with real quote but wrong source → exit 1; (c) junk with real quote and real source (i.e., the real entry) → exit 0 only for the real one. Confirm each variant's result. Report.
"""))

# ---------------- SCOUTS (6) ----------------
items.append(item("ScoutF19Open","scout",["coverage","freshness"],"""
Re-open the FIRST EPSS documentation page live: `curl -sSL -A 'kasegi-shokunin/1.0' https://www.first.org/epss/ -o <scratch>/S053-live.html`; record time, status, bytes, sha256; normalize (strip tags, collapse ws) and compare to the planned capture (from ExecC2Capture scratch) — report differing lines count. Locate Q1..Q4 sentences with line numbers in the normalized live text and confirm each is <=25 words. Also run the negative sweep: grep -rilE 'EPSS|exploit prediction|exploitation likelihood' {LANE}/corpus/knowledge {LANE}/corpus/README.md {LANE}/corpus/SOURCES.md {LANE}/SKILL.md → expect 0 hits (uncovered ground). Report.
"""))
items.append(item("ScoutF19Sibling","scout",["adjacency"],"""
Sweep sibling lanes for EPSS ground (read-only): grep -rilE 'EPSS|exploit prediction|exploitation' /home/vgpnk/Projects/shokunin/*-shokunin (excluding kasegi-shokunin) and /home/vgpnk/Projects/shokuknow/doctrine/ (read-only). Produce a hit table and a verdict: contested/ratified for F19/S053.
"""))
items.append(item("ScoutQuarantine","scout",["coverage"],"""
Re-derive the kasegi quarantine slice from the read-only register /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md using the frozen awk (rows where lane cell matches `kasegi` and round cell matches roundNN and id cell matches S\d+), print id+class per row. Then live-fetch each row's cited source (exactly one fetch per row, instrument UA, max 30s each): record status/bytes/verdict (present-and-located with located quote, prose-class-unverifiable, unreachable, absent). Produce the verdict table. Do not adopt anything.
"""))
items.append(item("ScoutIdCollisions","scout",["coverage"],"""
Run the assimilation id-collision check per the frozen commands: extract registry ids from {LANE}/corpus/SOURCES.md (0-3-space tolerant), staged ids from /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md, `comm -12` → collisions. Also run the guard proof on a scratch fixture: indented collision row caught by 0-3-space pattern, column-0-only pattern false-greens it, missing registry path exits 2 (fails closed). Report both id lists counts, collision count, and guard proof output. (Do not renumber anything.)
"""))
items.append(item("ScoutStandingRefusals","scout",["coverage"],"""
Re-confirm the seven standing refusal rows against the read-only package /home/vgpnk/Projects/shokuknow/merge/kasegi/ (compare digests with the round-35 lesson's table: program-scope-rules-and-asset-boundaries.md, claim-packaging-and-report-quality.md, cn-crowdsourced-testing-roles-and-conduct.md, chinese-crowd-testing-national-standard-2026-10-23.md, chinese-criminal-thresholds-and-authorisation.md, chinese-program-severity-instrument.md, program-severity-ladders-and-reward-scales.md). Report which flip conditions remain unmet (byte-identical package? same reasons?).
"""))
items.append(item("ScoutCaptureAvailability","scout",["coverage","freshness"],"""
Verify the capture prerequisites for the round: re-fetch the EPSS page with a plain UA AND the instrument UA (record both statuses), confirm the instrument UA gets 200, record length/sha256. Also confirm the manifest url equals https://www.first.org/epss/ exactly, and that the pinned quotes exist in the live feed (occurrences). This is freshness evidence for the S053 row.
"""))

# ---------------- CONNECTORS (3) ----------------
items.append(item("ConnC1C2","connector",["depth:verifiability","coverage"],"""
Map cross-claim coupling between C1 and C2: shared files (SOURCES.md, knowledge-expected.txt, lesson, scorecard), orderings (entry must land before harness re-run; suite E8 depends on lesson), risks (a shared append breaking the other's counter). Produce a dependency table and integration ordering recommendation. Report.
"""))
items.append(item("ConnPatterns","connector",["depth:verifiability","calibration"],"""
Correlate this round's defects with the kaika fleet mistake taxonomy and prior rounds: which classes repeat (closure-order, stale-premise, counter-discrimination, line-number drift); which QUALITY criteria would have caught each; propose the wording for R28/R29 (feed to ScribeQualityRows). Verify the proposals don't duplicate existing criteria (grep QUALITY.md). Report.
"""))
items.append(item("ConnSibling","connector",["adjacency"],"""
Consolidate the sibling-overlap scan outcomes (from ScoutF19Sibling and ExecSiblingSweep) into a ruling: is F19/S053 contested by any sibling? Does the doctrine assign first.org to this lane? State the PROVINCE adjacency handling (report, don't absorb). Produce the final ruling text for the lesson.
"""))

# ---------------- SENTINELS (2) ----------------
items.append(item("SentScope","sentinel",["scope"],"""
Verify all planned round-36 writes stay inside the lane wave dir and scratch: scan the wave dir {LANE}/.ufo/waves/round-36/, and the drafts (receipts) as they appear, for any path outside {LANE} or under /home/vgpnk/Projects/shokunin (fleet), /home/vgpnk/Projects/shokuknow, ~/Projects; flag any. Also check no receipt instructs mutating git/jj or editing another lane. Report violations or 'none'.
"""))
items.append(item("SentSecrets","sentinel",["scope"],"""
Scan every draft receipt and proposed file content in the wave dir for credential material: tokens, API keys, session cookies, private URLs (op://, vault refs), account identifiers. Report matches with file+line or 'none'. Also check the proposed entry/rows carry no instructions to probe/scan/log-in to anything.
"""))

# ---------------- SIMPLIFIERS (2) ----------------
items.append(item("SimplC1","simplifier",["depth:verifiability"],"""
Review the drafted r36-closure.sh for YAGNI/dead surface: unused variables/functions, duplicated greps, comments that lie, extra ops that add no check value. Propose a minimal diff (list of deletions) that keeps E1-E9 + selftest intact. Verify the minimal version still runs (bash -n + selftest in scratch). Report.
"""))
items.append(item("SimplReport","simplifier",["calibration"],"""
Review the drafted lesson/scorecard/report for redundancy and drift: duplicate statements, placeholders left, counts that don't match the receipts, sections out of order. Produce a corrections list (not edits). Confirm the report will satisfy required sections in order (Work performed, Landed changes, Before/after, Sources & frontier, Trend verdicts, SHONEN).
"""))

spec = {
  "wave": "kasegi-r36-build",
  "reportDir": ".ufo/waves/round-36/wave1",
  "maxLanes": 128,
  "axes": ["depth:verifiability", "coverage", "calibration"],
  "milestone": "round-36 build wave: C1 r36-closure head-closure suite; C2 F19 EPSS admission",
  "context": CTX,
  "items": items,
}
assert len(items)==64, len(items)
names=[i["name"] for i in items]
assert len(set(names))==64, "dup names"
json.dump(spec, open(".ufo/waves/round-36/wave1-spec.json","w"), indent=1)
print("items:", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
