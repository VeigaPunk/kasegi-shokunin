#!/usr/bin/env python3
"""Build the round-30 wave-1 spec (v2 policy, 64 seats) for kasegi-shokunin."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "a94871315cafa368f79c17d8c62d71fddd967986"
FREEZE = "3c5573541300ba0fd3d89372dda3d841172eaa3f"
REPORTS = ".ufo/waves/round-30/wave1"
LANE_ABS = " /home/vgpnk/Projects/shokunin/kasegi-shokunin"

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# kasegi-shokunin round 30, wave 1 (one v2 wave, 64 seats) — hyaku run 7 inline spawn

You are an L2 seat dispatched by the kasegi L1 (KasegiR30) through the orchestrator session. Fleet root /home/vgpnk/Projects/shokunin — you NEVER write there.

Lane repo (your ONLY write scope): {LANE}. Lane base revision {BASE}; claims-freeze commit {FREEZE}.

Read before your item (absolute paths):
- {LANE}/.ufo/waves/round-30/claims.json — FROZEN claims C1/C2 (predicates, counter commands, kill rules; do not edit; corrections land as separate appended files).
- {LANE}/.ufo/waves/round-30/c1-controls/before.txt, c2-controls/before.txt, census-before.txt — committed before receipts.
- {LANE}/SCORECARD.md, corpus/README.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/lessons/round-29.md, corpus/lessons/round-29-verifier-spotcheck.md.
- /home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md and SOURCES.append.md (read-only package; NEVER write inside /home/vgpnk/Projects/shokuknow).
- /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (read-only).

Hard bounds:
- Write ONLY inside {LANE}. Never write to the fleet root (/home/vgpnk/Projects/shokunin), sibling lanes, /home/vgpnk/Projects/shokuknow, the lane's git/jj state (no `git`/`jj` mutations; working-tree files only), `.ufo/state`, or MANIFEST.json. No command may contact a live bounty target; corpus entries are documentation-only (QUALITY Q6).
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your report file is your ownership marker; put your final evidence there.
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task — first read /home/vgpnk/.omp/agent/RULES.md (official channels: uv tool / official release binary / cargo / npm -g; NEVER sudo pacman: all pacman transactions are PAUSED host-wide; never run pacman -Sy/-Syu/-U/-R; no partial upgrades). Record any install (tool/version/channel/reason) in your report.
- Your route is set by the operator's global role map; never pass a model.
- Godspeed posture: name the axes; iterate cheap and in parallel; keep moves that improve any axis and harm none; never stall in clarifying-question loops; act via tool calls, don't ask.
- If an artifact you depend on is not yet on disk, poll (sleep 30s loops) up to your seat ceiling, then proceed against current bytes and label exactly which bytes you measured (sha256); never fabricate output and never claim a check you did not run.
- You are a leaf: do not dispatch tasks or spawn subagents (one read-only labrat probe is permitted only for an executor testing a falsifiable hypothesis).
- Your final answer = your report file content (Markdown) that the L1 will integrate."""

def seat(name, role, axes, prompt):
    return {"name": name, "role": role, "axes": axes,
            "milestone": "round-30", "prompt": "/skill:godspeed\n\n" + GODSPEED + "\n\n" + prompt}

S = []
def add(name, role, axes, prompt):
    S.append(seat(name, role, axes, prompt))

C1AX = ["depth:verifiability"]
C2AX = ["coverage"]
BOTHAX = ["depth:verifiability", "coverage"]

# ---------------- scouts ----------------
add("ScoutDatawalk", "scout", BOTHAX, f"""This seat carries the L1 planner's bounded data-walk (the L1 holds the canonical planner seat; this item is the permitted data-walk ride). Verify and report:
1. The frozen counters run from the lane root and their BEFORE values hold at the freeze commit {FREEZE} (`git -C {LANE} show {FREEZE}:.ufo/waves/round-30/c1-controls/before.txt` etc. — run the actual commands from claims.json against the working tree for an identical record).
2. `git -C {LANE} status --porcelain` state; the lane must contain no pre-existing production drift beyond the wave's own files.
3. Confirmation that the round-30 claims target the lane's lowest non-retired axis (depth:verifiability 4) and a second distinct axis (coverage 7) per SCORECARD.md.
4. Confirm no earlier round-30 attempt artifacts exist except the committed freeze files.
Report: {REPORTS}/ScoutDatawalk.md (with all command outputs, exit codes, and sha256 of the two instruments at {FREEZE}).""")

add("ScoutAssimPackage", "scout", C2AX, f"""Read the assimilation package (read-only) for the F14 theme "Japanese severity vocabulary and the handling-priority model":
- /home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.md
- /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md rows staged S049 (IPA JVN activity report PDF) and S050 (IPA JVN quarterly registration report) and S043 (JPCERT/CC guideline, maps to lane S041)
- staged entry /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md

Report the exact staged cell bytes (URL, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by) for S049/S050, the staged entry's header/source lines, and every schema hazard (cells containing `|`, prose recheck cells, non-ISO opened dates) that the lane append must normalize. Confirm the two URLs are absent from the lane registry (grep). Also read the lane's S041 row and round-28 capture path to state what S041 contributes. Report: {REPORTS}/ScoutAssimPackage.md.""")

add("ScoutQuarantineSlice", "scout", C2AX, f"""Extract this lane's quarantine slice from the read-only absent-defect register:
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
A={LANE}/.ufo/waves/round-30/assimilation; mkdir -p "$A"
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {{print $4, $5}}' "$R" > "$A/quarantine-slice"
Every line must carry an S-id; print the full table (id + register cell text) and mark which rows carry truncated URLs vs full locators. Record the slice count. Do NOT fetch yet (ExecQuarantineFetch does). Report: {REPORTS}/ScoutQuarantineSlice.md.""")

add("ScoutInstrumentBaseline", "scout", C1AX, f"""Re-read the two instruments fully: corpus/instruments/frontier-recheck-count.py and corpus/instruments/source-recheck.py. Reproduce the four before probes from claims.json C1 (A1/A2/B1/B2) against the working tree at the freeze commit and confirm every value in .ufo/waves/round-30/c1-controls/before.txt still reproduces (run each command, capture stdout/stderr/exit, sha256 both instrument files). Explain in your report WHY each baseline behavior is a conformance gap for claims C1 (missing named-row error; duplicate target passes; stem mismatch passes; double-occurrence passes). Report: {REPORTS}/ScoutInstrumentBaseline.md.""")

add("ScoutMapExpected", "scout", C2AX, f"""Study corpus/instruments/knowledge-expected.txt and corpus/instruments/recheck-audit.py: what entries/lines does the expected list hold today (counts at the freeze commit), how is it regenerated, and what must change when exactly one new knowledge entry (corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md) lands? Verify the round-28/29 notes: expected=40 entries/42 lines pre-r28 → 41/43 after F12; r29: 43? Measure exactly. Also confirm the README append-only convention (R6) and the exact table shapes used for the F13 coverage-map/frontier appendix rows so the F14 appendix matches byte-for-byte in shape. Report: {REPORTS}/ScoutMapExpected.md.""")

add("ScoutAdjacency", "scout", BOTHAX, f"""Scan /home/vgpnk/Projects/shokunin/MISSION.md, AXES.md and every sibling PROVINCE.md (chousa, kake, kagi, kengaku, kumitate, kotoba, kama, souji, tabi, kaidoku, tsukuroi, mado, tameshi, mori, revenger, kotodama): does any sibling lane hold the ground of "Japanese severity vocabulary and JVN handling-priority model" (IPA JVN reports, CVSS→深刻度 mapping, quarterly statistics) or of the C1 harness/Q9 checker instruments? Report each scan with evidence; report adjacency findings, absorb nothing. Report: {REPORTS}/ScoutAdjacency.md.""")

# ---------------- connectors ----------------
add("ConnClaims", "connector", BOTHAX, f"""Reconcile the frozen claims: for each claim in {LANE}/.ufo/waves/round-30/claims.json, produce a claim chain showing predicate sentence → counter command → kill rule → before receipt file → expected after file. Verify the counter commands exactly match the predicate and that the kill rules are executable by the L1 (paste the command list). Flag any counter that cannot emit the number its kill rule watches (M29-2 class). Confirm C1/C2 are causally separable (C1 fixtures touch only .ufo/waves/round-30/c1-controls and the two instruments; C2 touches corpus/SOURCES.md, corpus/README.md, corpus/knowledge/<F14 entry>, corpus/source-snapshots/round-30/, corpus/instruments/knowledge-expected.txt). Report: {REPORTS}/ConnClaims.md.""")

add("ConnStagedCensus", "connector", C2AX, f"""Run the assimilation id-collision check (addendum §10) with scratch committed as wave evidence:
S=/home/vgpnk/Projects/shokuknow
A={LANE}/.ufo/waves/round-30/assimilation; mkdir -p "$A"
grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' {LANE}/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
Also PROVE the guard's discrimination: create a scratch registry fixture with an indented `  | S002 |` row and show the 0–3-space-tolerant pattern catches it (nonempty collisions) while `^\\|` misses it. Then produce the adopted-id map by document (URL equality): staged S049→lane S046, staged S050→lane S047; verify both URLs are absent from the lane registry pre-append and the ids are free. Paste both id lists, the collision count and the renumber map. Report: {REPORTS}/ConnStagedCensus.md.""")

add("ConnQuarantine", "connector", C2AX, f"""Cross-source pattern join: read {LANE}/.ufo/waves/round-30/assimilation/quarantine-slice (from ScoutQuarantineSlice) and the package's staged rows S049/S050/S043. For each slice row, note whether the document's publisher/lineage overlaps the F14 sources (IPA/JPCERT/CC) — mark `related-to-F14` vs `unrelated`. This join feeds the lesson Gate, so verdicts are consistent. Also report which slice rows, if adopted, would need which lane ids (never arithmetic: document identity decides). Report: {REPORTS}/ConnQuarantine.md.""")

add("ConnHarm", "connector", BOTHAX, f"""Cross-claim interference analysis: C1 hardens frontier-recheck-count.py and source-recheck.py; C2 lands a new frontier row + entry + rows that must pass the hardened harness (17/17) and the hardened checker (exit 0). Enumerate every ordering hazard: manifest before captures; harness after entry/row; census after rows; Entry before registry/README; expected-list after entry. For each dependent seat, state the wait-gate file (the artifact that must exist on disk before the seat proceeds) and a sane poll ceiling. Also check C1's regression clause does not forbid the C2 additions (the F14 recheck line must satisfy the stricter checker). Output a dependency table. Report: {REPORTS}/ConnHarm.md.""")

# ---------------- executors ----------------
add("ExecImplFrontierHarness", "executor", C1AX, f"""Implement C1 limbs A1+A2 in corpus/instruments/frontier-recheck-count.py (single owner):
- A1: when an admitted frontier row names an entry path that does not exist, fail with a message that names the row id and path (exit 1), instead of an uncaught FileNotFoundError traceback.
- A2: when two admitted rows resolve to the same entry realpath, fail naming the duplicate (exit 1).
Preserve every existing behavior and CLI flag (--root, --json). Update the module docstring to state the new fail-closed behaviors. Do not touch any other file. Show the diff (`git -C {LANE} diff corpus/instruments/frontier-recheck-count.py`) and the new sha256 in your report. Then run the A1/A2 fixtures from .ufo/waves/round-30/c1-controls/ to demonstrate the new behavior (expected: a1 exit 1 naming F98; a2 exit 1 naming the duplicate). Report: {REPORTS}/ExecImplFrontierHarness.md.""")

add("ExecImplSourceRecheck", "executor", C1AX, f"""Implement C1 limbs B1+B2 in corpus/instruments/source-recheck.py (single owner):
- B1: in check_source, verify record["id"] == Path(record["path"]).stem; on mismatch emit `reason=stem-mismatch` and return 1.
- B2: an assertion whose normalized quote occurs more than once passes ONLY if its anchor verifies (anchor_verdict anchor=N-ok); MISSING/OUT-OF-RANGE/BROKEN anchors become failures (emit the reason and set status=1).
Preserve all existing behaviors, flags and exit conventions; update the module docstring and selftest to cover the two new limbs (add selftest cases for stem mismatch and double occurrence). Run `python3 corpus/instruments/source-recheck.py --selftest` — it must print `selftest cases=… failures=0` and exit 0. Show diff + sha256. Report: {REPORTS}/ExecImplSourceRecheck.md.""")

add("ExecControlC1", "executor", C1AX, f"""Run the canonical C1 control matrix (single owner of .ufo/waves/round-30/c1-controls/*.txt):
1. BEFORE: re-run the four frozen probes exactly as in claims.json C1 counter_commands at the freeze commit bytes (git show {FREEZE}:corpus/instruments/frontier-recheck-count.py etc. into scratch if the working tree has changed) and write before-run-2.txt reproducing before.txt.
2. Poll until the working-tree digests of both instruments differ from the freeze digests (or 45 min), then AFTER: run the same four probes against the landed bytes and write c1-after.txt.
3. Regression: `python3 corpus/instruments/frontier-recheck-count.py` on the real corpus and each real manifest source-recheck that passed at base must still pass (prove unchanged).
Print a before/after table with exit codes and the key output lines. Report: {REPORTS}/ExecControlC1.md.""")

add("ExecMutantsC1", "executor", C1AX, f"""After the instruments are updated (poll digests; ceiling 60 min), create four mutant copies under .ufo/waves/round-30/c1-controls/mutants/:
- mutant-a1.py: frontier-recheck-count.py with the A1 named-row limb removed (revert to uncaught open()).
- mutant-a2.py: with the A2 duplicate detection removed.
- mutant-b1.py: source-recheck.py with the B1 stem check removed.
- mutant-b2.py: with the B2 occurrence check removed.
Run the corresponding fixture against each mutant: each mutant must FLIP the fixed behavior (mutant-a1: A1 exits 1 with traceback/no named-row marker; mutant-a2: A2 exits 0; mutant-b1: B1 exits 0; mutant-b2: B2 exits 0). Also re-run the four probes from the freeze-commit bytes (via `git -C {LANE} show {FREEZE}:…`) as the do-nothing control — none may meet the targets. Record outputs and sha256 of each mutant. Report: {REPORTS}/ExecMutantsC1.md.""")

add("ExecDensityNoHarm", "executor", BOTHAX, f"""No-harm measurement (do not edit any production file): run `python3 corpus/instruments/density.py SKILL.md --label r30-before` and `python3 corpus/instruments/anchorcheck.py SKILL.md` and `python3 corpus/instruments/recheck-audit.py` at the current tree; record SKILL.md sha256 and PROVINCE.md sha256. Then AFTER the wave's production changes land (poll for the F14 entry and new instrument digests; ceiling 60 min), re-run all three and record. Report the before/after numbers, verdict-class movement (must be none beyond documented appends), and confirm no owned axis score changes (depth:density 9, depth:verifiability 4 held, coverage 7 held). Report: {REPORTS}/ExecDensityNoHarm.md.""")

add("ExecCaptureAssim", "executor", C2AX, f"""Single owner of corpus/source-snapshots/round-30/ (captures + manifest.json):
1. S046: capture the IPA JVN activity report PDF — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf — with `python3 corpus/instruments/capture-source.py --kind pdf` (pdftotext -enc UTF-8); name the snapshot S046.txt.
2. S047: capture the IPA JVN quarterly registration report — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html — with `python3 corpus/instruments/capture-source.py --kind html`; name S047.txt.
3. Also copy the existing S041 capture into this dir (corpus/source-snapshots/round-28/S041.txt → S041.txt) so the manifest is self-contained.
4. Build manifest.json (schema_version 1, sources list): records S046, S047, S041 with path, sha256 (real file hashes), and quotes arrays: for each record pick 3-6 assertions from the actual capture text (normalized length ≥12 chars, exactly-once occurrences, correct stem == id, optional anchors). Verify with `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046` (and S047, S041) — all must exit 0 with `occurrences=1` (or verified anchors) — and `source-recheck.py --selftest` still green. Report the chosen quotes, occurrence counts, hashes and the manifest bytes digest. If capture-source.py fails on a source (e.g., bot gate), use the documented curl fallback (instrument UA) and say so (M29-5 class). Report: {REPORTS}/ExecCaptureAssim.md.""")

add("ExecEntryF14", "executor", C2AX, f"""Sole writer of corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md (the F14 entry). Requirements (QUALITY Q1-Q10, R-rules):
- Opens with `source: S046 — <URL> — <anchor>`, `source: S047 — <URL> — <anchor>`, `source: S041 — <URL> — <anchor>` (anchors from the actual captures), `verified-at: 2026-10-25`, `ground: F14`, and one executable `recheck:` line: a single command chain running source-recheck.py for S046, S047, S041 (each `--source` invocation, `&&`-chained), prefixed `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`, with a `#` human note after the command (Q10).
- Use the captured quotes (read corpus/source-snapshots/round-30/S046.txt, S047.txt, S041.txt) for every load-bearing claim: JVN has no native severity scale and maps CVSS base scores (v2 and v3) onto the Japanese 深刻度 labels; the quarterly report publishes the distribution (cite the exact percentages you find in S047.txt); the guideline's 付録4 (S041) frames the impact-model thinking. Attribute everything to IPA/JPCERT's own reports (Q4); include at least one falsifiable rule and one rejected over-generalization (Q5). No live-target instructions; documentation-only (Q6).
- Body must mention S046, S047, S041 ids (the harness's cited-ids check reads S-ids in the body).
Report the final file bytes (sha256, line count) and how each Q/R criterion is met. Do NOT edit SOURCES.md, README.md, or the manifests yourself. Report: {REPORTS}/ExecEntryF14.md.""")

add("ExecRegistryAppend", "executor", C2AX, f"""Sole writer of the corpus/SOURCES.md registry appends for this round:
1. Append two new rows after the last registry row (S045): S046 (source: IPA JVN activity report — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf; kind docs; tier A; scope: JVN's own severity vocabulary, CVSS-to-深刻度 band definitions; anchor: from the round-30 capture S046.txt, the 注1)/注2) definitions; teaches: JVN has no native severity scale — it maps CVSS base scores onto Japanese labels keeping legacy v2 bands; status mined; opened 2026-10-25; recheck 180d; used-by corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md) and S047 (IPA JVN quarterly registration report — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html; kind docs; tier A; scope: JVN quarterly severity distribution; anchor: from S047.txt, 2-2 深刻度別割合/図2-2,図2-3; teaches: Japan's national database carries CVSS-derived severities at scale; status mined; opened 2026-10-25; recheck 90d; used-by same entry). No `|` inside any cell; exactly 11 columns.
2. Append the "Registry changes" lines: S046+S047 rows added (old → new), plus any status/recheck/used-by cell change observed this round (log old→new each, R8).
Do not modify any existing row. Verify with the census row-count command (rows=47) and `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 (W04 S028/S029 warnings allowed). Report the final registry tail bytes + sha256. Report: {REPORTS}/ExecRegistryAppend.md.""")

add("ExecReadmeF14", "executor", C2AX, f"""Sole writer of corpus/README.md appends: after the last line, append (R6 — never edit existing lines):
1. A coverage-map appendix row: | Japanese severity vocabulary and handling-priority model (round 30) | `knowledge/japanese-severity-vocabulary-and-impact-model.md` | S046, S047 (S041) — public primary, opened 2026-10-25 | (same shape as the F13 appendix row).
2. An F14 frontier row: | F14 | Japanese severity vocabulary and the handling-priority model | admitted | knowledge/japanese-severity-vocabulary-and-impact-model.md | S046, S047, S041 | <next note> | (same shape as F13's row in its appendix table).
3. A short appended amendment paragraph recording "at round 30 the frontier stands at 14/14 admitted" (historical note appended, never rewriting earlier text).
Verify `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {{n++}} END{{print n+0}}' corpus/README.md` → 14 and head bytes unchanged. Report final tail + sha256. Report: {REPORTS}/ExecReadmeF14.md.""")

add("ExecExpectedList", "executor", C2AX, f"""After the F14 entry lands (poll for corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md; ceiling 45 min): regenerate/append corpus/instruments/knowledge-expected.txt exactly as recheck-audit.py expects (one line per corpus/knowledge/*.md entry, comments preserved), then run `python3 corpus/instruments/recheck-audit.py` — it must print expected=<n> missing=0 unexpected=0 exit=0. Show the old vs new expected-list line counts and the recheck-audit output. Report: {REPORTS}/ExecExpectedList.md.""")

add("ExecCensusAfter", "executor", C2AX, f"""After S046/S047 rows and the F14 entry exist (poll SOURCES row count 47; ceiling 60 min): run the full census suite and write .ufo/waves/round-30/c2-after.txt:
- `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' corpus/SOURCES.md` → 47
- tier histogram, status histogram, malformed count (0), duplicate ids (none), enum violations (none), mined used-by paths exist (none missing)
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0
Print all outputs. Report: {REPORTS}/ExecCensusAfter.md.""")

add("ExecHarnessAfter", "executor", C2AX, f"""After the F14 row, entry, rows and round-30 manifest all exist (poll for corpus/README.md F14 row AND entry AND manifest; ceiling 60 min): run `python3 corpus/instruments/frontier-recheck-count.py` → expect `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S046,S047,S041 exit=0` and `entries=17 pass=17 exit=0`; then `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046 && … --source S047 && … --source S041` → exit 0. Save outputs to .ufo/waves/round-30/harness-after.txt. Report: {REPORTS}/ExecHarnessAfter.md.""")

add("ExecSelftestProbe", "executor", C1AX, f"""Probe every instrument and every new/edited artifact:
- `python3 corpus/instruments/source-recheck.py --selftest` → `selftest cases=… failures=0` exit 0 (post-B1/B2 implementation).
- `bash -n` on every `recheck:` line in the F14 entry and any changed corpus entry (must parse).
- Run the F14 entry's recheck line from a foreign cwd (/tmp) — must still exit 0 (cwd-independence).
- `python3 corpus/instruments/recheck-audit.py` exit 0.
Record all outputs and exit codes. Report: {REPORTS}/ExecSelftestProbe.md.""")

add("ExecQuarantineFetch", "executor", C2AX, f"""Hand-check every row of {LANE}/.ufo/waves/round-30/assimilation/quarantine-slice: for each S-id, fetch the cited source (instrument UA; use the full staged URL when the register URL is truncated) and try to locate the quote the register/proposal names. Classify each row: `reachable-quote-located` (fetch 200 + quote found), `fetched-no-quote` (fetch 200 + no located quote), `unfetchable` (404/TLS/failure), `already-mined-by-document` (URL byte-equal to an existing lane row). Verdicts close the row: none is appendable until hand-checked; a row that is not cited by an admitted entry is not appended regardless. Do NOT write into the register or the package. Produce the verdicts table (id, verdict, evidence, quote-or-reason). Report: {REPORTS}/ExecQuarantineFetch.md.""")

add("ExecConsiderthese", "executor", BOTHAX, f"""Mine considerthese proposal 4 ("Give my own proposals a status ledger") from /home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md (read-only; never edit that file). Land it as corpus/knowledge/considerthese-proposals-ledger.md: a status ledger table for proposals 1-6 (columns: proposal, status, round, path/evidence, note), marking 1 mined→R14, 2 open, 3 partially landed, 4 mined→this round (this file), 5 mined→R15, 6 open. Opens with provenance trio (source: considerthese/2026-10-25.md — own-work path, verified-at: 2026-10-25, recheck: 180d), meets Q1-Q6 (documentation-only, no universal claims). Report file sha256. Report: {REPORTS}/ExecConsiderthese.md.""")

add("ExecScopeSweep", "executor", BOTHAX, f"""During and after the wave, scan for out-of-bounds writes: list files under the fleet root /home/vgpnk/Projects/shokunin (excluding .ufo/state, .scratch, .ufo/reports, .ufo/prompts, .ufo/watchdog.log — orchestrator-owned) modified since the wave start whose content mentions `kasegi` + `round-30`; also confirm nothing was written into /home/vgpnk/Projects/shokuknow or sibling lane repos. Do NOT delete or edit anything; report findings (paths + mtimes + first line) or a clean sweep. Also verify the lane has no writes outside .ufo/waves/round-30/, corpus/ (sanctioned files), SCORECARD.md, LOG.md, SKILL.md (if appended). Report: {REPORTS}/ExecScopeSweep.md.""")

add("ExecPostCommitRecheck", "executor", BOTHAX, f"""Write the canonical post-integration recheck script at .ufo/waves/round-30/post-commit-recheck.sh that, run from the lane root after the L1's final commit, re-runs every C1 and C2 counter from claims.json plus the census and prints a summary (a1/a2/b1/b2 exits, frontier 14, entries citing S046/047 =1, rows 47, census exit, harness 17/17, recheck exit). Dry-run it on the current working tree and record its output. The L1 will run it at the final commit. The script must be bash -n clean. Report: {REPORTS}/ExecPostCommitRecheck.md.""")

add("ExecBeforeVerify", "executor", BOTHAX, f"""Verify the freeze receipts are intact at the freeze commit:
- `git -C {LANE} show {FREEZE}:.ufo/waves/round-30/claims.json` parses and matches the working copy.
- `git -C {LANE} show {FREEZE}:.ufo/waves/round-30/c1-controls/before.txt` reproduces the four probes (run them) — same outputs.
- census-before.txt values reproduce (census exit 0, rows 45, frontier 13, entries citing S046/047 0, harness 16/16).
Produce a freeze-authenticity receipt (digests + outputs). Report: {REPORTS}/ExecBeforeVerify.md.""")

# ---------------- scribes ----------------
add("ScribeLesson", "scribe", BOTHAX, f"""Sole writer of corpus/lessons/round-30.md. Assemble the full round lesson in the round-29 lesson's structure: revisions (base, freeze commit, dispatch commit, landed), wave shape/seat-role mix (from the spec/registry), frozen claims before→after table (from claims.json + c1/c2 receipts), Gate section (admitted F14 entry + S046/S047 rows; refused package candidates with reasons + flip; quarantine slice verdicts), Registry changes old→new, Mistakes (M30-*) from ScribeMistakes, considerthese, census before/after, compliance/ownership (single writers per file), tooling, close-out ledger. Poll until the required seat report files exist under .ufo/waves/round-30/wave1/ (ceiling 90 min); never fabricate a value you cannot point to. Report (the lesson itself): {REPORTS}/ScribeLesson.md plus the lesson at corpus/lessons/round-30.md.""")

add("ScribeLessonGate", "scribe", C2AX, f"""Draft the Gate block for the assimilation set (for ScribeLesson): admitted items (F14 entry; rows S046/S047) with per-item evidence (capture anchor, exactly-once quote, Q1-Q10 compliance) and ≤25-word located quotes with access date 2026-10-25; rejected candidates from the package (name at least one reject with reason + flip, e.g. `chinese-criminal-thresholds-and-authorisation.md` standing refusal or any candidate whose sources are not lane-registered); and the quarantine-slice verdict summary. Write {REPORTS}/ScribeLessonGate.md as your draft (ScribeLesson integrates). Report: {REPORTS}/ScribeLessonGate.md.""")

add("ScribeLog", "scribe", BOTHAX, f"""Sole writer of LOG.md's round-30 entry (append only): lane, round 30, date 2026-10-25, claims C1/C2 (axes), wave shape (one v2 wave 64 seats), key evidence pointers (claims.json, before/after receipts, wave spec/dispatch), and the planned commit references. Do not embed final commit hashes you cannot know; leave that to the report. Verify the entry is appended at the end (head unchanged, R6). Report: {REPORTS}/ScribeLog.md.""")

add("ScribeScorecard", "scribe", BOTHAX, f"""Sole writer of SCORECARD.md's round-30 result section (append at end): before→after tables for C1 (depth:verifiability 4 held — instrument conformance, evidence c1-controls) and C2 (coverage 7 held — F14, registry 45→47, harness 16/16→17/17), depth:density unchanged 9 (density numbers disclosed, not a score move), capabilities (none added this round), saturation unchanged (line 9/10, window N=3), and the move-log row. Poll receipts (ceiling 60 min). Keep all existing text untouched. Report: {REPORTS}/ScribeScorecard.md.""")

add("ScribeSkillGate", "scribe", C1AX, f"""If the hardened instruments (frontier-recheck-count.py, source-recheck.py) warrant a row in SKILL.md's Gates & probes table, append it at the end of the table (R6 append-only; head unchanged). Otherwise state no-op. Then run `python3 corpus/instruments/density.py SKILL.md --label r30-post-scribe` and `python3 corpus/instruments/anchorcheck.py SKILL.md` to confirm the append caused no verdict-class movement, and report density mean before/after. Report: {REPORTS}/ScribeSkillGate.md.""")

add("ScribeReport", "scribe", BOTHAX, f"""Draft the round report (for the L1 to finalize at /home/vgpnk/Projects/shokunin/.ufo/reports/round-30/kasegi.md) with exactly these literal sections in order: **Work performed** (names claims C1/C2 + axes; one bullet per item with evidence pointer), **Landed changes** (each tied to a LOG.md entry and later the commit hash), **Before → after measurements** (one per claim with counting command + commit), **Sources & frontier** (SOURCES rows before→after, census command/output, rows added by tier, rows touched old→new, frontier rows advanced, assimilation theme + considerthese), **Trend verdicts** (expansion/quality/discernment verdicts with evidence), **SHONEN** (one line per box: `[x]` only with a named non-author verifier; `[~]` with a resolvable evidence pointer; `[ ]` if untouched — the lane has 4 boxes in SHONEN.md), plus a **Stale-lane** line and any tool installs. Write your draft at {REPORTS}/draft-report.md. Report: {REPORTS}/ScribeReport.md.""")

add("ScribeQuarantine", "scribe", C2AX, f"""Finalize the quarantine verdicts table for the lesson: read ExecQuarantineFetch verdicts and ConnQuarantine joins; produce one row per slice id (id, verdict, evidence, note). Verify each verdict has a matching evidence line. Report: {REPORTS}/ScribeQuarantine.md.""")

add("ScribeAssim", "scribe", C2AX, f"""Build the assimilation evidence pack under .ufo/waves/round-30/assimilation/: copies of reg-ids, staged-ids, collisions (from ConnStagedCensus), the adopted-id map (staged S049→S046, S050→S047) with URL-equality proof, the gate-quote compliance check (each quoted ≤25 words, located), and the normalization notes (staged cells → lane schema). Confirm nog staged row is appended as-is (schema/census-safe). Report: {REPORTS}/ScribeAssim.md.""")

add("ScribeMistakes", "scribe", BOTHAX, f"""Mine this round's mistakes into rows (class · evidence pointer · captured-by · fix). Sources: the round-29 verifier routed defects (uncommitted leftovers at closure — committed via cleanup; report conformance items; S043 residual anchor cell deferred under R8), any wave findings you observe, and M29-3/M29-4 recurrences. Each fix must be shown able to fail before it counts (e.g., run the pre-fix instrument against the fixture). If you find none beyond the routed ones, paste the sweep that found none. Write {REPORTS}/ScribeMistakes.md. Report: {REPORTS}/ScribeMistakes.md.""")

add("ScribeFrontier", "scribe", C2AX, f"""Verify the frontier sheet: read corpus/README.md frontier rows and confirm F01-F14 rows (13 pre-round → 14 after F14); record the F14 row bytes and its entry/sources binding; compose the frontier section snippet for the lesson/report (rows before 13 → after 14, F14 admitted, denominator 14/14). Report: {REPORTS}/ScribeFrontier.md.""")

add("ScribeDigest", "scribe", BOTHAX, f"""Track instrument digests across stages: record sha256 of frontier-recheck-count.py and source-recheck.py at freeze ({FREEZE}), at implementation (poll), and at the end (landed bytes); catch and report mid-wave digest drift (M29-6 class) — if a receipt's digest does not match the file it cites, flag it. Produce a digest ledger table. Report: {REPORTS}/ScribeDigest.md.""")

add("ScribeSpot", "scribe", BOTHAX, f"""Collect the non-author seat spot-check agreements/disagreements (from RevC2Entry, RevC2Registry, RevQuarantineInd, RevC1Instrument and other reviewers) into the lesson's Spot-check result section: table of item, gate decision, re-opened by, agree/disagree, reason. Poll those reports (ceiling 60 min). Report: {REPORTS}/ScribeSpot.md.""")

add("ScribeCloseOut", "scribe", BOTHAX, f"""Maintain the close-out ledger: what the L1 still owes after the wave (post-commit recheck run at final commit; misroot sweep; report landing via fleet-commit; proof of census exit 0 at round end; final harness re-run). Each item carries the command that closes it. Report: {REPORTS}/ScribeCloseOut.md.""")

# ---------------- reviewers ----------------
add("RevC1Instrument", "reviewer", C1AX, f"""After the instruments change (poll digests; ceiling 60 min), independently re-read frontier-recheck-count.py and source-recheck.py and verify the C1 semantics (A1 named-row fail-closed; A2 duplicate realpath rejection; B1 stem==id fail-closed; B2 non-unique-without-anchor fail-closed). Re-run the four counts yourself; verify the real-corpus regression clause (harness 16/16 and every real manifest recheck that passed at base still passes). Verdict: agree/disagree with the claim receipt, with reasons. Report: {REPORTS}/RevC1Instrument.md.""")

add("RevC1Controls", "reviewer", C1AX, f"""Audit the C1 fixture matrix (c1-controls/): each fixture must isolate exactly one limb (A1/A2/B1/B2); run all four against base bytes (git show {FREEZE}:…) and against the landed bytes; confirm the do-nothing control cannot meet the targets and each mutant flips exactly one fixture. Flag any fixture that is not discriminating. Verdict with reasons. Report: {REPORTS}/RevC1Controls.md.""")

add("RevC2Entry", "reviewer", C2AX, f"""Bar-check the F14 entry (single re-open, non-author seat): read corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md and the round-30 captures (S046.txt/S047.txt/S041.txt) + manifest.json. Check Q1-Q10: provenance trio, source-id equality with the recheck `--source` set, bash -n + cwd-independence + `#` note (Q10), attribution (Q4), falsifiability (Q5), documentation-only (Q6), exactly-once quotes with stems==ids (Q9), normalization declared (Q8). Verdict admit/reject with reasons; record agree/disagree on the gate. Report: {REPORTS}/RevC2Entry.md.""")

add("RevC2Registry", "reviewer", C2AX, f"""Independently re-verify the registry changes: parse corpus/SOURCES.md rows S046/S047 (11 columns, no pipes in cells, enums valid, no duplicate ids, used-by paths exist), confirm census exit 0, and audit the "Registry changes" changelog for complete old→new logging (R8). Confirm no existing row was modified. Report: {REPORTS}/RevC2Registry.md.""")

add("RevC2Manifest", "reviewer", C2AX, f"""Re-run the round-30 manifest assertions: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046` (and S047, S041) — all assertions occurrences=1 raw and normalized, stems==ids, anchors in range; verify each capture file's sha256 matches the manifest pin; verify source-recheck selftest still green. Verdict with reasons. Report: {REPORTS}/RevC2Manifest.md.""")

add("RevClaimsOverall", "reviewer", BOTHAX, f"""End-to-end claim admission review: regenerate the before→after table for C1 and C2 from committed receipts and working-tree bytes; check each kill rule; confirm causal separability (C1 verifiable without C2 and vice versa) and that no claim's target is reachable by a do-nothing control. Produce the final verdicts (improved / held) with evidence. Report: {REPORTS}/RevClaimsOverall.md.""")

add("RevNoHarm", "reviewer", BOTHAX, f"""Verify no owned axis is harmed: compare SKILL.md and PROVINCE.md bytes before/after (allowed appends only, head unchanged); confirm SCORECARD scores hold (density 9, verifiability 4, coverage 7) with no in-place edits of history; confirm no claim traded one axis for another; density/anchorcheck verdict classes unmoved. Report: {REPORTS}/RevNoHarm.md.""")

add("RevScope", "reviewer", BOTHAX, f"""Scan all seat reports and the filesystem for out-of-bounds writes: nothing under the fleet root, sibling lanes, /home/vgpnk/Projects/shokuknow, lane git/jj state, .ufo/state, or MANIFEST.json should be touched; confirm no `git`/`jj` mutation by any seat; confirm no pacman transaction. Report any violation with the seat name and path. Report: {REPORTS}/RevScope.md.""")

add("RevQuarantineInd", "reviewer", C2AX, f"""Independently re-open a sample (≥3) of the quarantine-slice verdicts from ExecQuarantineFetch: re-fetch or check the evidence and record agree/disagree with reasons for each sampled row. Report: {REPORTS}/RevQuarantineInd.md.""")

add("RevConsiderthese", "reviewer", BOTHAX, f"""Verify the proposals ledger (corpus/knowledge/considerthese-proposals-ledger.md) against /home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-25.md: proposal numbers, statuses, round numbers, paths. Confirm the considerthese/ file was never modified (read-only; sha256 before/after). Verdict with reasons. Report: {REPORTS}/RevConsiderthese.md.""")

add("RevReadme", "reviewer", C2AX, f"""Verify corpus/README.md: head bytes unchanged (R6), F14 frontier row + coverage-map appendix row present with correct shapes, expected-list/recheck-audit alignment, and `awk …` frontier count = 14; harness 17/17 passes against the appendix. Report: {REPORTS}/RevReadme.md.""")

# ---------------- critics ----------------
add("CritC1Kill", "critic", C1AX, f"""Attack C1: try to satisfy the four counters without the claimed work — e.g., a printer that emits the expected lines, exit-code manipulation, degenerate fixtures, hardcoded messages, or reusing unrelated entries. Also check the mutants flip exactly one limb and the do-nothing control stays failing. Publish every bypass attempt with its outcome and the exact counter command it targets. Verdict: is the claim's kill rule robust? Report: {REPORTS}/CritC1Kill.md.""")

add("CritC2Kill", "critic", C2AX, f"""Attack C2: try to reach frontier 14 + entries citing S046/047 =1 + rows 47 + census 0 + harness 17/17 + recheck 0 WITHOUT a real entry or captures — e.g., an empty/stub/wrong entry, a row-only append, a duplicate source row, pointing the entry at an existing capture, or counting rows a sourceless fixture also counts. Publish each attempt and outcome. Verdict: is the claim's kill rule robust? Report: {REPORTS}/CritC2Kill.md.""")

add("CritGlobal", "critic", BOTHAX, f"""Global vacuity/overclaim audit across both claims: scores held correctly (no scalar rise claimed), measurement-vs-intent honesty (what the counters actually prove), no hidden trade anywhere, report markers absent, and the round's admission readiness. Also check the round's wave composition satisfies run-7 (64 seats, connector present, m_flash majority, attack ≥25%). Report: {REPORTS}/CritGlobal.md.""")

add("CritMeta", "critic", BOTHAX, f"""Wave-level meta-review: after results land, verify the results registry (wave1-results.json) matches the spec's seat roster (no missing/dead seats, no extra), seat counts vs spec, and whether any seat's report is contentless or a marker. Check that every seat whose output feeds a claim actually ran (dead seats stay dead in evidence). Report: {REPORTS}/CritMeta.md.""")

# ---------------- mutation-testers ----------------
add("MutC1A1", "mutation-tester", C1AX, f"""After the instrument update (poll digest; ceiling 60 min): create mutant-a1 (frontier-recheck-count.py with the A1 named-row limb removed, i.e. no catch around open()) in .ufo/waves/round-30/c1-controls/mutants/, run the A1 fixture against it, and show the behavior FLIPS (exit 1 traceback, no F98 marker). Record the mutant sha256 and output. Report: {REPORTS}/MutC1A1.md.""")

add("MutC1A2", "mutation-tester", C1AX, f"""After the instrument update (poll digest; ceiling 60 min): create mutant-a2 (A2 duplicate detection removed), run the A2 fixture against it, show it exits 0 (pass=2) — the flip. Record sha256 and output. Report: {REPORTS}/MutC1A2.md.""")

add("MutC1B1", "mutation-tester", C1AX, f"""After the instrument update (poll digest; ceiling 60 min): create mutant-b1 (source-recheck.py B1 stem check removed), run the B1 fixture, show exit 0 — the flip. Record sha256 and output. Report: {REPORTS}/MutC1B1.md.""")

add("MutC1B2", "mutation-tester", C1AX, f"""After the instrument update (poll digest; ceiling 60 min): create mutant-b2 (B2 occurrence check removed), run the B2 fixture, show exit 0 with occurrences=2 — the flip. Record sha256 and output. Report: {REPORTS}/MutC1B2.md.""")

# ---------------- sentinel ----------------
add("SentScope", "sentinel", BOTHAX, f"""Watch the wave live: periodically (every ~10 min, up to 90 min) scan for out-of-bounds writes — files under /home/vgpnk/Projects/shokunin (fleet root), siblings, /home/vgpnk/Projects/shokuknow — that mention kasegi round 30 or were modified after wave start; record findings with timestamps; never modify anything. Also confirm no seat ran git/jj mutations or pacman. Report: {REPORTS}/SentScope.md.""")

add("SentSecretScan", "sentinel", BOTHAX, f"""Scan every new/edited production file this round (F14 entry, SOURCES rows, lesson, ledger, manifests, instruments) for credential material, session/private URLs, `op://` references, and any live-target instruction (Q6). Also grep seat reports for banned tool usage claims (pacman). Report pass/fail per file with evidence. Report: {REPORTS}/SentSecretScan.md.""")

# ---------------- revenger ----------------
add("RevEngIntent", "revenger", C1AX, f"""Reverse-engineer the intent behind C1's targets: read corpus/lessons/round-24.md (M24), round-29.md (M29-3/M29-4) and the round-24/25/28 verifier spotchecks; trace each new limb (A1/A2/B1/B2) to the recorded incident it fixes; verify the fixes address the original failure modes by replaying the original repros; report residue gaps not yet covered (e.g. cross-entry credit, manifest path handling) as findings, without editing. Report: {REPORTS}/RevEngIntent.md.""")

# ---------------- simplifier ----------------
add("SimplWave", "simplifier", BOTHAX, f"""YAGNI pass over the wave's outputs before integration: list files under .ufo/waves/round-30/wave1/ and .ufo/waves/round-30/c1-controls/ that are redundant, superseded, or scaffolding not needed by the claims or lesson (e.g., duplicate receipts, scratch copies), and recommend exclusions from the final commit. Verify nothing needed is excluded (cross-check claims.json counters, kill rules, lesson structure). Also check that no bulk corpus copies were introduced (R14: use tarballs/git archive instead). Report: {REPORTS}/SimplWave.md.""")

assert len(S) == 64, len(S)
spec = {
    "wave": "kasegi-r30-build",
    "context": CONTEXT,
    "reportDir": REPORTS,
    "maxLanes": 128,
    "axes": ["depth:verifiability", "coverage"],
    "milestone": "round-30 build+attack wave: C1 harness/Q9 conformance + C2 F14 Japanese severity vocabulary assimilation",
    "items": S,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wave1-spec.json")
out = os.path.normpath(out)
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
from collections import Counter
print("items:", len(S), dict(Counter(i["role"] for i in S)))
print("wrote", out)
