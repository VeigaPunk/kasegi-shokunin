#!/usr/bin/env python3
"""Build the round-34 v2 wave spec (64 seats) for kasegi.

Run from the lane root; writes wave1-spec.json. The spec is then validated and
rendered by ufo-swarm-wave.mjs, and the dispatch JSON is handed to the
orchestrator via wave1.ready.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SHOKUKNOW = "/home/vgpnk/Projects/shokuknow"
BASE = "014ee2d7aa8c3c095ff57ae51097606a9906228c"
FREEZE = "29f606dbdd28aff6fd4573ab4b90788bbb90af13"
SCRATCH = "/fast/scratch/hyaku/kasegi-r34"
RD = ".ufo/waves/round-34/wave1"  # lane-relative report dir
C1 = ".ufo/waves/round-34/c1-controls"
C2 = ".ufo/waves/round-34/c2-controls"

HEAD = (
    "# Round\n"
    "kasegi-shokunin round 34, dispatched by the L1 (agent KasegiR34) via the inline spawn handoff "
    "(hyaku run 8). Lane repo %s is your ONLY write scope. Lane base %s; claims-freeze commit %s. "
    "The fleet root %s is read-only to you; %s (shokuknow campaign) is read-only — never write there, "
    "never run its campaign tools (renumber-staged.py, merge-plan.py, quote-lint.py, "
    "absent-defect-register.py all write into it).\n\n"
    "Frozen claims (do not edit; corrections land as separate appended files): %s/.ufo/waves/round-34/claims.json\n"
    "- C1 depth:verifiability (score 4, held): the nine round-33 verifier-routed defects R1–R9 land with "
    "runnable closure checks: `corpus/instruments/r-defect-closure.sh` prints `closed=9/9 exit=0` and "
    "`--selftest` prints `cases=9 failures=0`; `corpus/instruments/capture-binding-check.py --selftest` "
    "prints `selftest cases=N failures=0` with N>=19 (per-file binding, nested dir, strict-UTC, dup-record, "
    "dual-https row, rejected anchor, summary-only rejection); `corpus/instruments/kill-rule-check.py` prints "
    "`survivors=0`; SCORECARD.md carries 0 `<LANE_HASH>` markers; round-32 manifest carries only strict-UTC "
    "fetched_utc; S040-live.txt has a manifest record or orphan listing; erratum 2 + pre-freeze satisfiability "
    "step recorded; QUALITY R20 has the appended per-id note; round-33 lesson carries the R7 erratum; "
    "frontier-recheck-count.py rule A enforces both directions; junk twin committed under c2-controls/ and rejected.\n"
    "- C2 coverage (score 7, held): Frontier F17 admitted 16 -> 17 (Immunefi Vulnerability Severity Classification "
    "System v2.2 — Web3/smart-contract bounty severity classification; row S051, registry 50 -> 51, opened "
    "2026-10-26), one knowledge entry citing `source: S051`, harness entries=20 pass=20 exit=0 incl. "
    "`PASS F17 ids=S051`, source-recheck S051 exit 0, census exit 0 (W04 S028/S029 only).\n"
    "- Non-claim frontier items: assimilation (id-collision check + quarantine slice re-derived; no staged "
    "entry has fully-met flips — Assimilation: none, verdicts in the lesson Gate); considerthese proposal 6 "
    "(event-driven reflections) mined into QUALITY R23; mistakes M34-1 (round-33 'all mutants killed' "
    "overstatement, R4) and M34-2 (<LANE_HASH> markers filed, R1).\n\n"
    "Read as your item requires (absolute paths): %s/corpus/QUALITY.md (entry bar Q1–Q10, record R1–R23); "
    "%s/corpus/SOURCES.md; %s/corpus/README.md; %s/corpus/lessons/round-33.md and round-33-verifier-spotcheck.md "
    "(R1–R9 source); %s/SCORECARD.md; %s/corpus/instruments/README.md; %s/.ufo/waves/round-34/claims.json."
    % (LANE, BASE, FREEZE, FLEET, SHOKUKNOW, LANE, LANE, LANE, LANE, LANE, LANE, LANE, LANE)
)

TAIL = (
    "\n\nWork and reporting rules:\n"
    "- Every seat writes its receipt at %s/<seat-name>.md with a `## Report` section (commands + output + "
    "exit codes + file digests). Receipts are the evidence; quote named locations, never summarize blindly.\n"
    "- The lane repo is jj-colocated: NEVER run git add/commit/push or jj mutations; the L1 commits. "
    "Never touch the fleet repo, sibling lanes, /home/vgpnk/Projects/bounties, or shokuknow.\n"
    "- Every `Report:` trailer path is relative to %s — write it at %s/<that path>.\n"
    "- Scratch: all work trees/fixtures live under %s/<seat-name>/ (create with mkdir -p; NEVER rely on "
    "inherited TMPDIR; /tmp only for files under 50 MB; delete your scratch dir before yielding: "
    "`trap 'rm -rf -- \"$S\"' EXIT` in shell, `finally: shutil.rmtree` in Python; receipts first copied into "
    "the wave dir). A seat that ends with its tree still on disk reports that as a defect.\n"
    "- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task — "
    "read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record "
    "tool/version/channel/reason in the report). pacman transactions are PAUSED host-wide: install via "
    "`uv tool`/`npx`/an official binary in ~/.local/bin only; never `pacman -S` variants.\n"
    "- Do NOT spawn subagents, do NOT dispatch waves, never `agent://all`; message only your known peer "
    "seats by id (visible in the roster). Do not write outside your lane write scope.\n"
    "- The seat is a leaf of an L2 wave of a shokunin round: report findings/verdicts in your receipt; "
    "the L1 integrates and decides. You are not a judge of the round.\n" % (RD, LANE, LANE, SCRATCH)
)

def item(name, role, prompt, axes=("depth:verifiability", "coverage"), ms="round-34"):
    return {"name": name, "role": role, "axes": list(axes),
            "milestone": ms, "prompt": prompt}

ITEMS = []

def add(name, role, prompt, axes=("depth:verifiability", "coverage")):
    ITEMS.append(item(name, role, prompt, axes))

# ---------------------------------------------------------------- executors
add("ExecCaptureBindingHarden", "executor", HEAD + """
Implement the capture-binding-check.py hardening for C1 (all in ONE landing, then verify):
1. Rule C strict-UTC: `fetched_utc` must parse as ISO-8601 with 'Z' or '+00:00' suffix; reject `"pending"`,
   reject any timezone-offset value (e.g. `-03:00`), reject malformed. Add selftest cases
   `fetched-utc-pending-rejected` and `fetched-utc-local-offset-rejected`.
2. Rule A per-file binding: every captured source file in a snapshot dir (non-manifest files under
   corpus/source-snapshots/<round>/) must appear in >=1 manifest record, or the audit line lists it as an
   orphan (`orphan=<file>`). Add cases `per-file-orphan-detected` and `per-file-orphan-listed`.
3. Nested snapshot dirs: walk snapshot dirs recursively (a nested snapshot dir is also audited). Add case
   `nested-snapshot-dir`.
4. Duplicate records inside one manifest fail (`dup-record-in-manifest` case).
5. A registry row with two `https://` tokens in the source cell fails (`double-https-row` case).
6. A `rejected` registry row cannot anchor a record (`rejected-row-anchor` case).
7. Rename selftest case `url-matching-two-rows` to `shared-url-between-two-records` (content unchanged: two
   records sharing one URL across distinct rows is informational multi_row_url, not dup-id).
8. The selftest runner must require one `selftest case=<name> exit=... want=... verdict=pass` line per case
   AND the summary `selftest cases=N failures=0`; a summary-only output (forged) is a failure
   (`summary-only-selftest-rejected` case).
Keep the existing outputs: `records=40 bound=40 unbound=0` exit 0 on the landed corpus; `--selftest`
failures=0; 11 existing cases stay passing. Run: `python3 corpus/instruments/capture-binding-check.py --selftest`
-> `selftest cases=N failures=0` with N>=19, exit 0; plus the live audit `records=40 bound=40 unbound=0`.
Write your receipt with before/after digests (sha256) of the instrument and the selftest line counts.
""" + TAIL)

add("ExecRDefectClosureSuite", "executor", HEAD + """
Build `corpus/instruments/r-defect-closure.sh` (committed, read-only, bash -n-parseable, every check
`cd %s &&`-prefixed) — the C1 counter. It contains exactly NINE check functions, one per round-33 verifier
routed defect (round-33-verifier-spotcheck.md §5):
- R1: SCORECARD.md carries 0 `<LANE_HASH>` AND an appended correction naming 7963976e…/014ee2d… exists.
- R2: an appended "erratum 2" paragraph in the SCORECARD round-33 section restates the kill-rule
  parenthetical per-id AND a pre-freeze satisfiability step is recorded (QUALITY R22 row exists).
- R3: QUALITY.md carries an appended note below the R20 row stating the per-id reading supersedes
  "exactly one" registry-row URL.
- R4: the tightened kill-rule requirement is recorded (QUALITY R22/R24 or the scorecard section) AND the
  round-33 lesson carries an appended erratum correcting the "all mutants killed" overstatement to the
  measured 3-of-4-under-frozen-rule figure.
- R5: capture-binding-check.py selftest case list contains no name `url-matching-two-rows`.
- R6: corpus/source-snapshots/round-26/manifest.json has a record for S040-live.txt (path match) or the
  audit lists `orphan=S040-live.txt`; the manifest `purpose` text is corrected.
- R7: round-33 lesson contains the appended R7 erratum (char counts 31 and 22; S050.txt:70 sentence cite).
- R8: round-32 manifest fetched_utc values all match strict UTC (`^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$`)
  and contain no '-' offset (+00:00 or Z only).
- R9: capture-binding-check.py has the named H4–H8 cases (nested dir, pending-UTC, dup-record, dual-https,
  rejected anchor) AND frontier-recheck-count.py rule A is bidirectional AND c2-controls/junk-f17.md exists.
EACH check must exit nonzero while its defect is open (that is the closure semantics). Plain run:
`bash corpus/instruments/r-defect-closure.sh` -> `closed=K/9 exit=0|1`. `--selftest` mode: run each check
against a deliberately-broken fixture copy (a scratch tree where that one defect is reintroduced); it must
print `cases=9 failures=0` only if every check fails on its broken fixture and passes on the live tree.
Also print per-check lines `R1 check=... open=0|1`. Prove the do-nothing control is rejected: the fake
suite (c1-controls/fake-suite.sh) prints `closed=9/9 exit=0` but its --selftest prints no real case lines —
your suite's selftest must be the discriminator (document it). Receipt with the full outputs and digests.
""" % LANE + TAIL)

add("ExecKillRuleCheck", "executor", HEAD + """
Build `corpus/instruments/kill-rule-check.py` (committed) — C1's survivor-mutant counter. It replays the
three named mutants against a COPY of the landed `corpus/instruments/capture-binding-check.py` bytes:
1. skip-selftest summary mutant (replaces the selftest section with a forged summary `selftest cases=0
   failures=0` exit 0) — must now be KILLED (the landed runner rejects summary-only output).
2. accept-record-without-url mutant (drops rule B's url-required limb; prints `records=2 bound=2 unbound=0`
   exit 0 on a url-less fixture) — must now be KILLED.
3. per-file-binding-removal mutant (drops rule A's per-file orphan detection) — must now be KILLED.
Each mutant is an exactly-once textual patch over the instrument bytes (like QUALITY R17). Print one line per
mutant: `mutant=<name> killed=0|1`. Summary `survivors=K`; exit 0 only when K=0. Controls: accept a
no-op patch (must NOT be a kill), a non-compiling patch, and the fake runner c1-controls/fake-killrule.py
(prints survivors=0 without replay) — the real tool must differ. Receipt with mutant diffs, outputs, digests.
""" + TAIL)

add("ExecFrontierBidirectional", "executor", HEAD + """
Patch `corpus/instruments/frontier-recheck-count.py` rule A to be bidirectional (closes R9's one-directional
gap): currently the header `source:` ids must be covered by the entry's recheck `--source` selections
(declared ⊄ recheck_ids fails). Add the reverse: every `--source` id in the recheck line must ALSO appear in
the entry's header `source:` ids (a recheck line pointing at a source the entry does not cite fails). Keep all
existing behavior: `PASS F16 … ids=S049,S050`, `entries=K pass=K exit=0`; add selftest coverage of the
reverse direction (a fixture entry with an extra `--source` in its recheck line must fail). The F16/F17/F15
entries must still pass (entries=20 pass=20 once F17 lands). Receipt: before/after digests, selftest output,
a demonstration that dropping `--source S050` from the F16 entry now fails.
""" + TAIL)

add("ExecManifestR32Normalize", "executor", HEAD + """
Normalize `corpus/source-snapshots/round-32/manifest.json` for R8: the two `fetched_utc` values are
`2026-10-25T23:14:00-03:00` — a local-offset capture-commit time in a `_utc` field. The record's captured
bytes were verified live under the same URLs on 2026-10-26 (`S049` at 04:16:06Z, `S050` at 04:16:16Z,
HTTP 200, 0 differing lines — see round-33 lesson / ScoutLiveDrift). Set `fetched_utc` to those strict-UTC
instants and add a `purpose` note stating they are verification re-open instants of byte-equal content, not
the original fetch. Do NOT edit any other cell. Then verify: `python3 corpus/instruments/source-recheck.py
--manifest corpus/source-snapshots/round-32/manifest.json --source S049` and `--source S050` still print all
assertions `occurrences=1` and `sha256 OK`, exit 0; `python3 corpus/instruments/capture-binding-check.py`
still prints `records=40 bound=40 unbound=0` exit 0. Receipt with old/new manifest digests and outputs.
""" + TAIL)

add("ExecS040Orphan", "executor", HEAD + """
Resolve R6's orphan: `corpus/source-snapshots/round-26/S040-live.txt` exists but the round-26 manifest
(records: S041.txt only) has no record for it, and its `purpose` text is now false. Decide and land one of:
(a) add a manifest record for S040-live.txt (path, sha256 computed from the file, `archival: true`, `url`
matching its registry row if one exists — S040's row URL is the Cisco policy page; note this file is a live
capture of that page, so the URL matches S040), or (b) leave it as an explicitly listed orphan — but then the
manifest must carry an `orphan` list naming it. Either way the instrument's audit must show the file bound or
listed as orphan, and the manifest `purpose`/notes text must be corrected to describe what the manifest
actually covers. Verify: `python3 corpus/instruments/capture-binding-check.py` exit 0 with
`missing_manifest=0` and no unbound file; source-recheck unaffected. Receipt with old/new manifest digests
and capture-binding-check output.
""" + TAIL)

add("ExecScorecardMarkers", "executor", HEAD + """
Fix R1: SCORECARD.md carries two `<LANE_HASH>` markers (lines ~988 and ~1087). The round-33 final lane
commit was `7963976e60b2564860553c6ab4838128d5ca06ea` (the tip is `014ee2d7…` after the verifier spot-check
commit). Replace BOTH markers with `7963976e…` (the measured round-33 integration/tip hash) and append one
correction line at the end of the round-33 section stating: "Correction (round 34): the two <LANE_HASH>
placeholders above were replaced with the round-33 final hash 7963976e… (lane tip 014ee2d… after the verifier
commit)." Then `grep -c '<LANE_HASH>' SCORECARD.md` -> 0. The R1 closure check in r-defect-closure.sh
depends on both facts. Receipt: before/after grep counts, the appended line, file digest.
""" + TAIL)

add("ExecErratum2", "executor", HEAD + """
Land R2: append to the SCORECARD.md round-33 section (end of the Rule-B erratum paragraph area) an
"erratum 2" block that (a) restates the frozen kill-rule parenthetical per-id: "0 or 2+ matches = failure"
applies within a single record's own id scope — a URL shared by two different rows is informational
(multi_row_url=N) and does not fail rule B; two rows with the same id fail as `dup-id`; and (b) records the
pre-freeze satisfiability step: before freezing any claim, evaluate each literal predicate against base bytes
(see QUALITY R22). Append-only: do not edit existing paragraphs. Receipt: appended block text, file digest.
""" + TAIL)

add("ExecQualityAppends", "executor", HEAD + """
Append the QUALITY.md amendments (append-only, below the existing rows, R6 style):
- R3 note: below the R20 row add: "Note (round 34): R20's 'exactly one registry-row URL' reading is
  superseded by the C1 erratum-2 per-id reading — a URL shared by two different registry rows is
  informational `multi_row_url=N`, not a failure (SCORECARD round-33 section, erratum 2)."
- R22 (new criterion, grounded in R2/M34-2): "A frozen claim predicate is checked for satisfiability
  against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run
  against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze
  erratum. Grounded in: round-33 verifier R2; M34-2."
- R23 (new criterion, grounded in considerthese/2026-10-25.md proposal 6): "A lane records an event-driven
  reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing
  the considerthese file and date. Grounded in: considerthese/2026-10-25.md proposal 6."
Each grounded in its lesson. Receipt: appended rows, diff numstat (append-only), file digest.
""" + TAIL)

add("ExecLessonErrata", "executor", HEAD + """
Land R7 + M33-3 errata (append-only):
- Append to corpus/lessons/round-33.md an "Erratum (round 34)" block correcting: (a) the F16/S050 quote
  character counts "19 characters" -> 31 and "23 characters" -> 22 (with the command that counts:
  `printf '…' | wc -m`), and (b) the report/lesson citation of the S050 applicability sentence: the
  sentence is at `S050.txt:70` (the heading is at L69) — any citation of ":69" for the sentence is
  corrected to ":70".
- Append to corpus/lessons/round-29.md an erratum noting the SOURCES.md anchor drift (M33-3): the
  registry/appendix line numbers cited from round-29 grew by +7 since round-33's 6-line append (SOURCES.md
  `## Registry changes` block); cite the current line numbers.
Do not edit existing lines. Receipt: appended blocks + digests.
""" + TAIL)

add("ExecSnapshotR34", "executor", HEAD + """
Create the C2 capture: capture the Immunefi Vulnerability Severity Classification System v2.2 page at
https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ using
`python3 corpus/instruments/capture-source.py <url> --out corpus/source-snapshots/round-34/S051.txt`
(instrument UA; the page is Next.js SSR — verify the text body containing the Smart Contracts level table is
present, lines with the five levels and impact bullets). Build `corpus/source-snapshots/round-34/manifest.json`
(record S051: path, sha256, url, fetched_utc in strict UTC) including the exact quotes the F17 entry will
use, each with line anchors, asserting `occurrences=1`. Candidate quotes (≤25 words each, located):
- from the Smart Contracts table: severity5. Critical — Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield" (verify exact wording/case against the capture).
- a sentence naming the classification focus (e.g. "Classification focuses on the consequences of a successful exploit" — locate verbatim).
Self-check: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` -> every assertion `occurrences=1`, `sha256 OK`, exit 0. Receipt with fetch stats, sha256, line numbers, manifest digest.
""" + TAIL)

add("ExecRegistryAppend", "executor", HEAD + """
Append the S051 row to `corpus/SOURCES.md` (registry), plus one `## Search log` bullet for the round-34
Immunefi sweep, plus the `## Registry changes` R8 lines (old→new), exactly per the ScribeSOURCESRow draft
(coordinate via agent message when it is written; do not proceed with a different shape). Row schema: 11
columns, NF=13, no `|` inside cells, id S051, kind docs, tier A scoped to Immunefi's own VSCS v2.2
statements, status mined, opened 2026-10-26, recheck 90d, used-by the F17 entry path, anchor pinned to the
round-34 capture with line locators, teaches a grounded learner benefit naming Immunefi as the stating party
(Q4). Do not touch any other row. Verify census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kasegi` -> exit 0 with only W04 S028/S029; `grep -cE
'^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` -> 51; malformed=0. Receipt with the appended
lines and census output.
""" + TAIL)

add("ExecCensusAfter", "executor", HEAD + """
Run the round-end census and contract commands on the landed bytes and save the receipt:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
(expect exit 0, W04 S028/S029 only); the six contract commands: rows (51), malformed (0), tier histogram
(A=48 B=1 C=2), status histogram (mined=39 queued=9 rejected=3), duplicate ids (empty), enum/tier-inflation
(empty), missing used-by (empty); `grep -cE '^\\| F[0-9]+ \\|' corpus/README.md` -> 17. Write all outputs to
your receipt. This is the C2 census after-state, measured at quiescent tip bytes.
""" + TAIL)

add("ExecHarnessAfter", "executor", HEAD + """
Run the C2 harness on the landed bytes: `python3 corpus/instruments/frontier-recheck-count.py` — expect
`PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051` (or the exact entry basename)
and `entries=20 pass=20 exit=0`. Also confirm the junk twin is NOT counted as an entry (it lives under
c2-controls/, not corpus/knowledge/). If any F-row fails, report the failing line verbatim. Receipt with the
full output.
""" + TAIL)

add("ExecBeforeReceipts", "executor", HEAD + """
Replay the frozen before-controls at the freeze commit to prove they are reproducible: from a scratch export
of `git archive 29f606db` (the freeze commit), run the commands recorded in
`c1-controls/before.txt` (ls_exit=2 for r-defect-closure.sh, capture-binding-check selftest cases=11,
grep -c <LANE_HASH> = 2, manifest fetched_utc values, phishing S040-live orphan, QUALITY 'exactly one'=1,
census lines, frontier=16, rows=50, S051=0, harness entries=19 pass=19, source-recheck exit 2). Confirm each
matches the stored receipt. Also confirm claims.json at the freeze commit still hashes to the committed
bytes (`git show 29f606db:.ufo/waves/round-34/claims.json | sha256sum`). Receipt: per-line match report.
""" + TAIL)

add("ExecDoNothingReject", "executor", HEAD + """
Demonstrate the do-nothing controls are rejected by the real instruments:
1. `bash corpus/instruments/r-defect-closure.sh --selftest` -> `cases=9 failures=0` exit 0; and the fake
   suite (c1-controls/fake-suite.sh) lacks real per-case lines — show its `--selftest` output cannot satisfy
   the real suite's own selftest discriminator (document the comparison).
2. `python3 corpus/instruments/kill-rule-check.py` -> `survivors=0`; the fake runner
   (c1-controls/fake-killrule.py) is rejected because it prints survivors=0 without replaying mutants —
   document the difference.
3. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json
   --source S051` -> exit 0 on the real entry, exit != 0 on the junk twin (c2-controls/junk-f17.md's
   fabricated quote); show both outputs.
Receipt with all outputs.
""" + TAIL)

add("ExecNoHarmFinal", "executor", HEAD + """
No-harm sweep on the landed bytes (read-only): (1) `python3 corpus/instruments/density.py SKILL.md` -> mean
and block/citation counts — compare to the round-33 recorded 201.7 (25 blocks, 710 cites); (2) `python3
corpus/instruments/anchorcheck.py SKILL.md` -> failure classes 0 (LOST-RECORDED=306, PIN-BROKEN=0,
ORIGIN=0, OUTSIDE-BASE=0, BASE-ABSENT=0), exit 0; (3) `git diff --numstat <base> -- SKILL.md PROVINCE.md
corpus/README.md corpus/SOURCES.md corpus/QUALITY.md SCORECARD.md LOG.md` — append-only (0 deletions);
(4) `git status --porcelain` in the lane — no stray files outside the wave/known receipts; (5) confirm no
fleet-root misroot files authored by this round's seats: run `git -C /home/vgpnk/Projects/shokunin status
--porcelain` and list any untracked file a seat wrote (name check) — report them (the L1 sweeps). Receipt.
""" + TAIL)

add("ExecRegressionC1", "executor", HEAD + """
Final C1 regression at quiescent tip bytes: run every C1 counting command from claims.json verbatim:
`bash corpus/instruments/r-defect-closure.sh` (closed=9/9 exit=0), `bash corpus/instruments/r-defect-closure.sh
--selftest` (cases=9 failures=0), `python3 corpus/instruments/capture-binding-check.py --selftest`
(cases=N>=19 failures=0), `python3 corpus/instruments/kill-rule-check.py` (survivors=0), `grep -c
'<LANE_HASH>' SCORECARD.md` (0), `python3 corpus/instruments/capture-binding-check.py` (records=40 bound=40
unbound=0 exit=0). Record outputs verbatim; compare to the after-values; report matches/mismatches.
""" + TAIL)

add("ExecRegressionC2", "executor", HEAD + """
Final C2 regression at quiescent tip bytes: run every C2 counting command from claims.json verbatim:
`grep -cE '^\\| F[0-9]+ \\|' corpus/README.md` (17), `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'
corpus/SOURCES.md` (51), `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` (1), `grep -lE
'^source: S051 ' corpus/knowledge/*.md | wc -l` (1), `python3 corpus/instruments/frontier-recheck-count.py`
(entries=20 pass=20 exit=0), `python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-34/manifest.json --source S051` (all occurrences=1, sha256 OK, exit 0), census
validate (exit 0). Record outputs verbatim; compare to after-values; report matches/mismatches.
""" + TAIL)

# ---------------------------------------------------------------- scribes
add("ScribeEntryF17", "scribe", HEAD + """
Draft the F17 knowledge entry at `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`
(place it at the path; the L1 commits). It must pass Q1–Q10 (corpus/QUALITY.md): H1 title; header trio
`source: S051 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/` with an
exact anchor (capture line), `verified-at: 2026-10-26`, `recheck:` as one executable command
(`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json
--source S051`); every load-bearing claim rests on the tier-A row S051 with a verbatim ≤25-word located
quote; attribution stays Immunefi's (Q4); at least one falsifiable rule and one rejected over-generalization
(Q5); documentation-only, no credentials (Q6). Content: the VSCS v2.2 five severity levels for Smart
Contracts (Critical 5 → None 1), the impact-bullet semantics (theft/permanent freezing/MEV/insolvency,
etc.), the focus on exploit consequences and the downgrade/rejection carve-outs, and the note that programs
specify which version applies (v2.2 vs v2.3). Read the capture `corpus/source-snapshots/round-34/S051.txt`
first; every quote must be exactly-once in it (verify with grep). Keep Total ≤ 120 lines. Do NOT cite or
quote anything not in the capture.
""" + TAIL)

add("ScribeSOURCESRow", "scribe", HEAD + """
Draft the exact S051 registry row (11 columns, NF=13, no `|` in any cell), the round-34 `## Search log`
bullet (PRISMA-shaped: question / where searched / date / identified/screened/included/excluded counts /
stop rationale), and the `## Registry changes` R8 lines (old→new, e.g. "Registry 50 rows pre-append → 51
post-append", "No status/recheck/used-by cell changed on pre-existing rows; S001–S050 untouched (logged)").
Place the draft at `.ufo/waves/round-34/wave1/ScribeSOURCESRow.md`; message ExecRegistryAppend when ready —
it applies exactly this text.
""" + TAIL)

add("ScribeLesson", "scribe", HEAD + """
Compose `corpus/lessons/round-34.md` (the round lesson; the L1 commits). Required sections, all backed by
wave receipts (cite `.ufo/waves/round-34/wave1/<seat>.md` paths):
- Header: revisions (base 014ee2d…, freeze 29f606db…, wave-1 dispatch commit, final integration hash as
  placeholders the L1 fills), shape (one v2 wave, seat count, role mix), answering-model note per receipt.
- `## Frozen claims — before → after`: table with C1/C2 before (frozen controls), after (named receipts),
  verdict/boundary.
- `## Gate`: assimilation (≥1 admit + ≥1 reject requirement: this round's set is the quarantine slice and
  standing refusals — record each verdict with reason and flip; State Assimilation: none adopted with the
  reason), F17/S051 admittance (URL, access date, ≤25-word located quote), any rejects with reasons.
- `## Mistakes` (M34-1, M34-2, and any further mined from receipts): class · evidence pointer · captured-by
  · fix; every fix shown able to fail.
- `## considerthese`: proposal 6 mined → R23; other proposals unchanged with reasons.
- `## Census before → after`: both census outputs + exit codes.
- `## No-harm` table (density, anchorcheck, diff numstat, unowned writes).
- `## Open items / unverified`: list honestly.
Do not fabricate; if a receipt is missing for a claim, say so.
""" + TAIL)

add("ScribeScorecard", "scribe", HEAD + """
Compose the round-34 SCORECARD.md section (append at the end; the L1 commits): "## Round 34 — frozen
claims C1/C2 (2026-10-26)" with the claims table (C1 depth:verifiability 4 held; C2 coverage 7 held;
depth:density unchanged guard row), measurement state (digests), capabilities note (no new capability row:
capture-binding-check already entered round 33), move-log rows for round 34, saturation unchanged, and the
pointers to receipts. Follow the round-33 section's exact shape. Use only values from the receipts;
placeholders for the final lane commit are the L1's to fill.
""" + TAIL)

add("ScribeShonen", "scribe", HEAD + """
Update `SHONEN.md` (the lane's promotion checklist): the four boxes stay `[~]` unless a named non-author
verifier checks one (a wave seat is the lane, so it cannot write `[x]`). Refresh each box's evidence pointer
to round-34 receipts/commits: box 1 (decision tables/checklists — SKILL.md unchanged; cite the no-harm
receipt + instrument receipts), box 2 (end-to-end domain task executed and logged — round 33's
capture-binding-check measurement is the closest; state if no new E2E task ran), box 3 (instructions
executable without oral context — cite recheck-audit 46/46 after the F17 entry and the new instruments'
selftests), box 4 (no cross-domain bleed — PROVINCE.md diff append-only). Do not claim `[x]`.
""" + TAIL)

add("ScribeReportDraft", "scribe", HEAD + """
Draft the round report body at `.ufo/waves/round-34/wave1/ScribeReportDraft.md` using the wave receipts:
Work performed (claims named), Landed changes (each tied to LOG.md entry + commit hash placeholders),
Before → after measurements (commands + outputs), Sources & frontier (SOURCES rows before→after, rows added
by tier, rows touched old→new, frontier advanced), Trend verdicts (expansion/quality/discernment with
evidence), SHONEN lines. Leave `<LANE_HASH>` placeholders for the L1. This draft is the input to the final
report; do not write the fleet repo.
""" + TAIL)

add("ScribeSearchLog", "scribe", HEAD + """
Draft the round-34 `## Search log` bullet for the Immunefi VSCS sweep (for ScribeSOURCESRow), PRISMA-shaped:
question ("does the lane hold a Web3/smart-contract bounty severity-classification source?"), where searched
(Immunefi's own site, official VSCS v2.2 URL; negative sweep over the lane corpus for 'Immunefi', 'VSCS',
'smart contract', 'Web3', 'blockchain'), date 2026-10-26, identified/screened/included/excluded counts,
exclusion reasons, stop rationale. Place at `.ufo/waves/round-34/wave1/ScribeSearchLog.md`.
""" + TAIL)

add("ScribeAssimilationGate", "scribe", HEAD + """
Draft the assimilation Gate block for the lesson: (1) re-derived quarantine slice for kasegi from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (awk filter: lane
cell kasegi, round cell, id cell) with per-row verdicts (payload-present/absent, unreachable) — the slice
must carry an S-id on every line; (2) id-collision check re-run (registry ids vs staged ids, comm -12,
0–3-space pattern); (3) standing refusals re-confirmed with flip conditions (from round-33 lesson). Verdict:
Assimilation: none adopted this round (flips unmet — name each). Place at
`.ufo/waves/round-34/wave1/ScribeAssimilationGate.md`.
""" + TAIL)

add("ScribeSkillGate", "scribe", HEAD + """
Record the SKILL.md/PROVINCE.md conformance gate for the lesson: diff the base vs landed bytes for both
files (`git diff --numstat 014ee2d -- SKILL.md PROVINCE.md`), confirm an-only (0 deletions), and record
whether any skill/province update was needed this round (expected: none beyond this round's no-harm check;
F17 sits inside the province's frontier — report if a PROVINCE amendment is warranted and propose its exact
append-only text). Place at `.ufo/waves/round-34/wave1/ScribeSkillGate.md`.
""" + TAIL)

add("ScribeQualityDraft", "scribe", HEAD + """
Draft the exact QUALITY.md amendment text for R3 note, R22 and R23 (see ExecQualityAppends for the required
content; you supply final wording with the grounded-in citations). Also draft the R24 row if the wave's
mutations surface a new criterion (e.g. selftest summary-runner strictness). Place at
`.ufo/waves/round-34/wave1/ScribeQualityDraft.md`; message ExecQualityAppends when ready.
""" + TAIL)

# ---------------------------------------------------------------- reviewers
add("RevEntryF17", "reviewer", HEAD + """
Non-author review of the final F17 entry bytes (read `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`
from the tip): Q1–Q10 verdict table (QUALITY.md), plus re-open `corpus/source-snapshots/round-34/S051.txt`
and verify every quoted string is exactly-once at its cited line (`grep -c`). Verdict ADMIT / REFUSE with
reasons. If REFUSE, list the exact failing criterion and line. You did not author the entry.
""" + TAIL)

add("RevRowS051", "reviewer", HEAD + """
Review the S051 registry row: 11 columns/NF=13; no `|` inside cells; tier A scoped to Immunefi's own VSCS
v2.2 statements; anchor pinned to the round-34 capture with line locators; quote ≤25 words located in the
capture; `opened 2026-10-26`; `recheck 90d`; `used-by` exactly the F17 entry; kind docs; status mined.
Also confirm the round-34 Search-log bullet and Registry-changes R8 lines are present and truthful. Verdict
`matches|differs` with specifics.
""" + TAIL)

add("RevC1BeforeAfter", "reviewer", HEAD + """
Independent before→after verification of C1: re-derive every C1 counter from claims.json with its own
command at the tip (r-defect-closure.sh, its --selftest, capture-binding-check --selftest, kill-rule-check,
grep <LANE_HASH>, capture-binding-check audit) and compare to the frozen before receipt and the after-values.
Report matches/differences with exact outputs. You did not author the changes.
""" + TAIL)

add("RevC2BeforeAfter", "reviewer", HEAD + """
Independent before→after verification of C2: re-derive every C2 counter (frontier count, registry rows, S051
row, entries citing S051, harness, source-recheck S051, census) from claims.json with its own command at the
tip. Report matches/differences with exact outputs. You did not author the changes.
""" + TAIL)

add("RevRSuite", "reviewer", HEAD + """
Review `corpus/instruments/r-defect-closure.sh`: exactly nine checks R1–R9; every check `bash -n`-parseable,
`cd`-prefixed, read-only; every check exits nonzero while its defect is open (test by running the suite on
a scratch copy of the base tree where all defects are open → `closed=0/9`; and on the tip → `closed=9/9`);
the `--selftest` mode genuinely runs each check against a broken fixture; no vacuous `echo` check can pass
the selftest. Verdict with evidence.
""" + TAIL)

add("RevKillRule", "reviewer", HEAD + """
Review `corpus/instruments/kill-rule-check.py`: the three mutants are exactly-once textual patches over the
landed capture-binding-check.py bytes, each still compiles, each flips the relevant limb; the tool prints one
line per mutant and `survivors=K`; controls (no-op, non-compiling, fake runner) are rejected; the fake runner
c1-controls/fake-killrule.py does not satisfy the output contract. Verdict with evidence.
""" + TAIL)

add("RevManifestR32", "reviewer", HEAD + """
Review the normalized round-32 manifest: fetched_utc values are strict UTC instants; the purpose note states
they are verification re-opens of byte-equal content; no other cell changed (diff against the round-33
landed manifest); source-recheck S049/S050 still exit 0. Verdict with evidence.
""" + TAIL)

add("RevOrphan", "reviewer", HEAD + """
Review the R6 orphan resolution: round-26 manifest now has a record for S040-live.txt (or an explicit orphan
list); the record's sha256 matches the file bytes; the manifest purpose text is truthful; capture-binding-check
exit 0 with missing_manifest=0. Verdict with evidence.
""" + TAIL)

add("RevNoHarm", "reviewer", HEAD + """
Independent no-harm review: `git diff --numstat 014ee2d --` over the lane's production files (SKILL.md,
PROVINCE.md, corpus/*, SCORECARD.md, LOG.md) — append-only (0 deletions); `python3 corpus/instruments/anchorcheck.py
SKILL.md` failure classes 0; density mean not below the round-33 201.7 by more than noise (report actual);
no new lost-base/misroot files at the fleet root authored by this round. Verdict.
""" + TAIL)

add("RevErrata", "reviewer", HEAD + """
Review the appended errata: R1 correction + marker replacement (grep <LANE_HASH> = 0 and the correction line
names 7963976e…); erratum 2 present in the round-33 section with the per-id restatement and the pre-freeze
step; QUALITY R20 note present below the R20 row; round-33 lesson R7 erratum present (31/22 counts, S050.txt:70);
round-29 lesson anchor-drift erratum present. All must be appends (no in-place edits). Verdict with evidence.
""" + TAIL)

add("RevClaimsFreeze", "reviewer", HEAD + """
Verify the claim freeze: claims.json at the freeze commit 29f606db hashes identically to the tip version; the
predicate sentences in the wave context match claims.json verbatim; every counting command in claims.json is
runnable and the after-values match the receipts; the kill rules are the same sentences as in the plan and
the counter code. Report any divergence.
""" + TAIL)

add("RevJunkTwin", "reviewer", HEAD + """
Verify the junk-twin control: `c2-controls/junk-f17.md` is committed; its shape counters pass
(junk-checker.py prints shape_counters=3/3); the admission gate rejects it: source-recheck on it exits != 0
(manifest missing / quote absent) and the F17 entry review (RevEntryF17) does not admit the junk bytes.
Explicitly run the source-recheck against the junk twin's fabricated quote and record the failure. Verdict.
""" + TAIL)

add("RevCensus", "reviewer", HEAD + """
Verify the final census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` -> exit 0 with exactly W04 S028 + W04 S029 + ok; the six contract
commands (rows=51, malformed=0, tier A=48 B=1 C=2, status mined=39 queued=9 rejected=3, dups empty, enum
violations empty, missing used-by empty); registry rows 50→51; frontier 16→17. Verdict.
""" + TAIL)

# ---------------------------------------------------------------- mutation-testers
add("MutCaptureBindingLimbs", "mutation-tester", HEAD + """
Mutation-test the landed capture-binding-check.py: for each NEW selftest case (per-file-orphan-detected,
per-file-orphan-listed, nested-snapshot-dir, fetched-utc-pending-rejected, fetched-utc-local-offset-rejected,
dup-record-in-manifest, double-https-row, rejected-row-anchor, summary-only-selftest-rejected, shared-url-between-two-records)
build a one-limb mutant that removes/disables that case's guard and show the selftest run changes (case fails
or the guard's fixture passes) — each case is load-bearing. Controls: no-op patch, non-compiling patch, and
a semantically equivalent patch must NOT be treated as kills. Every mutant is an exact-once find/replace over
the instrument bytes in a scratch copy; run `--selftest` against each mutant copy. Receipt with mutant list,
diffs, outcomes.
""" + TAIL)

add("MutRSuiteChecks", "mutation-tester", HEAD + """
Mutation-test r-defect-closure.sh: for each of the nine checks R1–R9, build a mutant that makes the check
vacuous (always exit 0) — the suite's `--selftest` must then fail (the check no longer fails on its broken
fixture); and a mutant that deletes the check — the plain run must print closed<9/9. Controls: no-op and
non-compiling mutants rejected. Receipt with per-check outcomes.
""" + TAIL)

add("MutKillRuleMutants", "mutation-tester", HEAD + """
Verify kill-rule-check.py's killer behavior: run it at the tip (expect survivors=0); then introduce a
non-killed mutant (e.g. rule-B url-limb removal with a different wording the tool misses) and confirm the
tool reports it as a survivor (this is the red-before for the obligation). Also confirm the three named
mutants are genuinely killed. Receipt.
""" + TAIL)

add("MutFrontierRuleA", "mutation-tester", HEAD + """
Mutation-test the bidirectional rule A in frontier-recheck-count.py: (1) remove the reverse direction → a
fixture entry with an extra `--source` in its recheck line passes (this must now fail on the landed tool);
(2) remove the forward direction → a fixture entry whose header cites a source its recheck line omits passes
(must fail); (3) controls: no-op patch rejected. Run on scratch copies with fixture entries. Receipt.
""" + TAIL)

add("MutSelftestSummary", "mutation-tester", HEAD + """
Forge-summary mutant against the landed capture-binding-check.py selftest runner: replace the per-case lines
with only `selftest cases=0 failures=0` (exit 0) — the landed runner must reject it (exit != 0,
`summary-only-selftest-rejected`). Also forge `cases=19 failures=0` with no per-case lines — must be
rejected. Demonstrate both against the landed bytes in scratch. Receipt.
""" + TAIL)

add("MutManifestField", "mutation-tester", HEAD + """
Field mutants against the landed capture-binding-check.py: build scratch manifest fixtures exercising (1)
fetched_utc="pending", (2) fetched_utc="2026-10-25T23:14:00-03:00", (3) a nested snapshot dir hiding two
records, (4) duplicate records in one manifest, (5) a source cell with two https:// tokens, (6) a rejected-row
anchor, (7) a captured file with no manifest record — each must fail (exit 1/2) with the named failure.
Controls: the clean round-32/round-34 manifests pass. Receipt with outputs.
""" + TAIL)

add("MutC2Entry", "mutation-tester", HEAD + """
Mutation-test the F17 entry + harness binding: mutants (1) drop the `source: S051` header line, (2) change
a quote's wording (paraphrase), (3) point the anchor at the wrong line, (4) add an unregistered `--source`
to the recheck line — each must fail source-recheck or the harness (exit != 0). The pristine entry must pass.
Receipt with outputs.
""" + TAIL)

# ---------------------------------------------------------------- scouts
add("ScoutImmunefiLive", "scout", HEAD + """
Live re-open of the C2 source: fetch https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/
under the instrument UA; note HTTP status/bytes; extract the text body; compare with `corpus/source-snapshots/round-34/S051.txt`
(normalized, whitespace-collapsed): 0 differing lines expected; verify the two gate quotes occur live exactly-once
(`grep -c`); record access date 2026-10-26. Also confirm the page identifies the version (v2.2) and that
the 'severity-classification-systems' index lists v2.2 and v2.3 as both in use. Receipt.
""" + TAIL)

add("ScoutDatawalk", "scout", HEAD + """
Planner data-walk (the L1 holds the canonical planner seat; this item is its permitted data-walk ride). From
the freeze commit 29f606db verify the frozen BEFORE values: replay the c1-controls/before.txt commands and
confirm each value (ls_exit=2; selftest cases=11; <LANE_HASH>=2; manifest fetched_utc values; S040-live
orphan; QUALITY 'exactly one'=1; census lines; frontier=16; rows=50; S051_rows=0; harness entries=19 pass=19;
source-recheck exit 2). Confirm claims.json predicate sentences agree with the counters and the kill rules
are identical strings in claims.json and in the wave context. Receipt.
""" + TAIL)

add("ScoutQuarantine", "scout", HEAD + """
Re-derive the kasegi quarantine slice from the shokuknow absent-defect-register (read-only):
`awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Every line must
carry an S-id. For each row, probe reachability (read-only, instrument UA) of the cited source and record
found/absent/unreachable. Verdict per row (refuse/unreachable/verifiable) into the assimilation Gate draft.
Also re-run the id-collision check: registry ids vs `merge/kasegi/SOURCES.append.md` staged ids with the
0–3-space pattern; print both lists, the collision count, and confirm no adopted row this round.
""" + TAIL)

add("ScoutPackageThemes", "scout", HEAD + """
Re-confirm the merge/kasegi/ package standing refusals and their flip conditions (read-only) using the
round-33 lesson Gate as the baseline: for each refused staged entry (program-scope-rules-and-asset-boundaries,
claim-packaging-and-report-quality, cn-crowdsourced-testing-roles-and-conduct,
chinese-crowd-testing-national-standard-2026-10-23, chinese-criminal-thresholds-and-authorisation,
chinese-program-severity-instrument, program-severity-ladders-and-reward-scales) state whether ANY flip
condition cleared this round (e.g. S036/BILISRC row now registered? S081/S082/S077/S078/S079?) by checking
the current lane registry and captures. Deliver the "Assimilation: none" verdict with per-entry reasons.
""" + TAIL)

add("ScoutSiblingSweep", "scout", HEAD + """
Negative sweep across sibling lanes for the C2 ground: search /home/vgpnk/Projects/shokunin/*-shokunin/
(except kasegi) corpora/SKILL.md for 'Immunefi', 'VSCS', 'severity classification', 'smart contract', 'Web3',
'blockchain', 'bounty' — report per-sibling hits (path:line) or zero-hits, so the connector can rule on
contested scope. Also check the fleet root's merge/considerthese themes for the same tokens. Receipt.
""" + TAIL)

# ---------------------------------------------------------------- critics
add("CritC1Kill", "critic", HEAD + """
Falsify C1 as declared: attempt to construct states that satisfy the after-predicate while violating the
kill rule: (1) an r-defect-closure.sh printing closed=9/9 with nine vacuous checks (does the --selftest
discriminator catch it?); (2) capture-binding-check --selftest with N>=19 trivial cases that don't exercise
the named guards; (3) kill-rule-check.py printing survivors=0 while a mutant survives (forge one); (4) a
round-32 manifest passing strict-UTC regex while the value is still not a real fetch instant; (5) the
per-file binding satisfied by listing every file as orphan without binding. For each, state whether the
landed instruments catch it (pass) or not (gap -> record). Verdict.
""" + TAIL)

add("CritC2Kill", "critic", HEAD + """
Falsify C2 as declared: build junk constructions that pass the shape counters (frontier=17, rows=51, S051
row present, harness entries=20 pass=20) without a real capture or a real admission: (1) an entry quoting a
fabricated string with a fake manifest record (can source-recheck detect it? run it); (2) a row with no
opened source; (3) an entry citing S051 without ever opening the page. State which landed checks catch each
and which do not (record the residual gaps). Verdict.
""" + TAIL)

add("CritOverclaim", "critic", HEAD + """
Check C1/C2 before/after statements against the receipts and the frozen controls: every after-value must have
a measured command output; no universal clause beyond what the counting command enumerates; no claim that a
check 'verifies' while its receipt is missing; the report and lesson must not overstate mutant kills or
closure counts beyond measured figures. Report every overclaim or unmeasured value with its location.
""" + TAIL)

add("CritBoundary", "critic", HEAD + """
Scope-guard critique: scan this round's wave receipts and the tip tree for files a seat wrote outside the
lane write scope (check the fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for
untracked files naming kasegi/round-34; check no sibling repo or shokuknow was touched; check no lane git/jj
state was mutated by seats). Also check every seat used the scratch root under `/fast/scratch/hyaku/kasegi-r34`
and deleted its tree (report any leftover). Verdict.
""" + TAIL)

add("CritMistakes", "critic", HEAD + """
Critique the lesson's Mistakes rows (M34-1, M34-2 and any others): each row must have a real evidence pointer,
a captured-by (or `none`), a fix, and the fix shown able to fail (a red-before run). Flag any mistake row
that is prose without a reproducible check. Verdict.
""" + TAIL)

# ---------------------------------------------------------------- connectors
add("ConnClaims", "connector", HEAD + """
Cross-index the nine routed defects R1–R9 to their landed fixes: for each defect name the fix artifact
(file/line), the closure check in r-defect-closure.sh, and the receipt that proves it; produce a coverage
table (R1..R9 all 9 mapped). Flag any defect with no fix, no check, or no receipt. Also connect R2/R3/R7 to
the appended errata and confirm the pre-freeze satisfiability step is recorded.
""" + TAIL)

add("ConnSibling", "connector", HEAD + """
Synthesize the sibling-overlap scan (ScoutSiblingSweep) into a contested-scope ruling draft for the lesson
and report: any sibling corpus holding Immunefi/VSCS/Web3-severity ground is reported, not absorbed
(PROVINCE adjacency). State the ruling (no contested scope / report-to-lane) for each hit.
""" + TAIL)

add("ConnCrossCheck", "connector", HEAD + """
Cross-check the source chains end to end: for S051 verify registry row ↔ capture file ↔ manifest record ↔
entry header `source:` ↔ harness `PASS F17` ↔ source-recheck assertion ids all agree (ids, URLs, sha256);
for the round-32 and round-26 manifests verify manifest records ↔ files ↔ registry rows. Report any dangling
link. Also confirm census W04 pair is unchanged and no new warnings appeared.
""" + TAIL)

# ---------------------------------------------------------------- sentinels
add("SentCred", "sentinel", HEAD + """
Credential/secret scan of every new artifact this round: captures, manifests, the F17 entry, receipts, the
new instruments and suite. Scan for session tokens, cookies, private URLs, `op://` refs, passwords, API
keys, personal data. The Immunefi capture must contain no credential material (flag the login/member areas
of the page if present — the VSCS page should be public text; if the capture contains a login prompt or
session-bearing content, refuse it and report). Verdict clean/flag with locations.
""" + TAIL)

add("SentScopeFinal", "sentinel", HEAD + """
Final scope audit: (1) verify no seat wrote outside the lane repo (check the fleet root status for untracked
round-34-named files: `git -C /home/vgpnk/Projects/shokunin status --porcelain` and name any hit; the L1
sweeps them); (2) verify no lane git/jj mutation was done by seats (read-only git only); (3) verify the
shokuknow tree is untouched (`git -C /home/vgpnk/Projects/shokuknow status --porcelain` read-only); (4)
verify scratch discipline: no `/fast/scratch/hyaku/kasegi-r34/<seat>` leftover for this round's seats
(except the L1's own). Verdict.
""" + TAIL)

# ---------------------------------------------------------------- simplifier
add("SimplifierCleanup", "simplifier", HEAD + """
YAGNI sweep of the new instruments: (1) r-defect-closure.sh — every check loads a distinct defect; no two
checks test the same fact; no dead or duplicate code; (2) kill-rule-check.py — the mutant set is minimal and
each mutant is load-bearing; (3) capture-binding-check.py additions — no dead cases, no unreachable branches;
(4) the mixed17 entry — no filler, no redundant claims; (5) the wave's receipts — no duplicate artifacts.
Propose deletions only where behavior is provably preserved (run the counters before/after your proposal and
paste both outputs). Receipt.
""" + TAIL)

# ---------------------------------------------------------------- assemble
seen = set()
for it in ITEMS:
    if it["name"] in seen:
        raise SystemExit("duplicate name %s" % it["name"])
    seen.add(it["name"])
if not (64 <= len(ITEMS) <= 128):
    raise SystemExit("seat count %d outside v2 band" % len(ITEMS))
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("roles:", roles, "total:", len(ITEMS))
attack = roles.get("reviewer", 0) + roles.get("critic", 0) + roles.get("mutation-tester", 0) + roles.get("labrat", 0)
print("attack share: %d/%d = %.1f%%" % (attack, len(ITEMS), 100.0 * attack / len(ITEMS)))

spec = {
    "wave": "kasegi-r34-build",
    "reportDir": RD,
    "maxLanes": 128,
    "axes": ["depth:density", "depth:verifiability", "coverage"],
    "milestone": "round-34 build wave: C1 R1-R9 instrument-soundness closure; C2 F17 Immunefi VSCS v2.2 admission",
    "context": HEAD + TAIL,
    "items": ITEMS,
}
out = ".ufo/waves/round-34/wave1-spec.json"
with open(out, "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
print("wrote", out, len(json.dumps(spec)))
