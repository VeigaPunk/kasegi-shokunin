#!/usr/bin/env python3
"""Build the round-35 v2 wave spec (64 seats) for kasegi.

One v2 wave (policy v2, band 64-128), C1 D1-D7 closure suite + C2 F18 CISA KEV
admission. L1 holds the canonical planner seat; the planner data-walk rides the
ScoutDatawalk item (orchestrator ruling 2026-10-19).
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SHOKUKNOW = "/home/vgpnk/Projects/shokuknow"
BASE = "3266c9937b03062d9bbc2f436e20820115ed179c"
FREEZE = "617496b9c6e92bc671e7e78b83df69a04470d0e9"
SCRATCH = "/fast/scratch/hyaku/kasegi-r35"
RD = ".ufo/waves/round-35/wave1"  # lane-relative report dir
C1 = ".ufo/waves/round-35/c1-controls"
C2 = ".ufo/waves/round-35/c2-controls"

HEAD = (
    "# Round\n"
    "kasegi-shokunin round 35, dispatched by the L1 (agent KasegiR35) via the inline spawn handoff "
    "(hyaku run 8). Lane repo %s is your ONLY write scope. Lane base %s; claims-freeze commit %s. "
    "The fleet root %s is read-only to you; %s (shokuknow campaign) is read-only — never write there, "
    "never run its campaign tools (renumber-staged.py, merge-plan.py, quote-lint.py, "
    "absent-defect-register.py all write into it).\n\n"
    "Frozen claims (do not edit; corrections land as separate appended files): %s/.ufo/waves/round-35/claims.json\n"
    "- C1 depth:verifiability (score 4, held): the seven round-34 verifier-routed defects D1–D7 land with "
    "runnable closure checks: `corpus/instruments/r35-defect-closure.sh` prints `closed=7/7 exit=0` and "
    "`--selftest` prints `cases=7 failures=0`; SCORECARD.md `filled by the L1` count 0 with an appended "
    "correction naming c1c6a5f; an appended round-34 depth:density-row erratum naming the corrected mean "
    "201.2; SKILL.md Gates & probes registry registers r-defect-closure.sh + kill-rule-check.py; "
    "wave1-results.json tracked with a provenance note beside it; claims-erratum-d5.md carries the "
    "discriminating-invocation and per-id occurrences statements; L1Integration.md stale dead-seat sentence "
    "corrected; QUALITY supersedes-R22/R23 rows present.\n"
    "- C2 coverage (score 7, held): Frontier F18 admitted 17 -> 18 (CISA Known Exploited Vulnerabilities "
    "catalog — exploitation-status-based prioritization distinct from CVSS severity; row S052, registry "
    "51 -> 52, opened 2026-10-26), one knowledge entry citing `source: S052`, harness entries=21 pass=21 "
    "exit=0 incl. `PASS F18 ids=S052`, source-recheck S052 exit 0, census exit 0 (W04 S028/S029 only).\n"
    "- Non-claim frontier items: assimilation (id-collision check + quarantine slice re-derived; no staged "
    "entry has fully-met flips — Assimilation: none, verdicts in the lesson Gate); considerthese proposal 2 "
    "(distance to the next score) mined into QUALITY R26; mistakes M35-1+ minted in the lesson.\n\n"
    "Read as your item requires (absolute paths): %s/corpus/QUALITY.md (entry bar Q1–Q10, record R1–R26); "
    "%s/corpus/SOURCES.md; %s/corpus/README.md; %s/corpus/lessons/round-34.md and round-34-verifier-spotcheck.md "
    "(D1–D7 source); %s/SCORECARD.md; %s/corpus/instruments/README.md; %s/.ufo/waves/round-35/claims.json."
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

def item(name, role, prompt, axes=("depth:verifiability", "coverage"), ms="round-35"):
    return {"name": name, "role": role, "axes": list(axes),
            "milestone": ms, "prompt": prompt}

ITEMS = []

def add(name, role, prompt, axes=("depth:verifiability", "coverage")):
    ITEMS.append(item(name, role, prompt, axes))

# ---------------------------------------------------------------- executors
add("ExecD1Markers", "executor", HEAD + """
Land D1 (round-34-verifier-spotcheck.md §6 D1): the SCORECARD.md round-34 section carries placeholder
prose `**Round-34 final lane commit: filled by the L1 in the closing commit.**` (and any sibling
`Final lane commit: the L1 fills this line…` lines). Replace those lines with the actual round-34 final
lane hash `c1c6a5f826d2425446347173de527c42991b78b0` and append one correction line at the end of the
round-34 section: "Correction (round 35): the 'filled by the L1' placeholders above were replaced with the
round-34 final lane hash c1c6a5f… (the round-34 lane tip at its non-author closure)." Append-only for all
other content: do not edit any other paragraph. Then `grep -c 'filled by the L1' SCORECARD.md` -> 0 and
`grep -c 'c1c6a5f' SCORECARD.md` -> >= 1. Receipt: before/after grep counts, the appended line, file digest.
""" + TAIL)

add("ExecD2DensityRow", "executor", HEAD + """
Land D2 (spotcheck D2): the SCORECARD.md round-34 depth:density row (the row that reads `density.py SKILL.md`
mean 201.7 over 25 blocks / 710 cites and `git diff --numstat` 0 changed lines) is stale at the tip: each of
SKILL.md and PROVINCE.md gained +1 appended line (R6 corrections) and the measured mean is 201.2
(wave1/L1Integration.md). Append an erratum at the end of the round-34 section: "Erratum (round 35): the
round-34 depth:density row measured 0 changed SKILL/PROVINCE lines and mean 201.7; at the tip each file had
+1 appended correction line and the measured density mean is 201.2 (unchanged instrument, same definition)."
Do NOT edit the stale row in place (append-only). Verify: `grep -c 'round-34 depth:density row' SCORECARD.md`
-> >= 1 and `grep -c '201.2' SCORECARD.md` -> >= 1, and the stale row bytes are untouched
(`git diff <base> -- SCORECARD.md` shows 0 deletions in the round-34 section). Receipt.
""" + TAIL)

add("ExecD3SkillRegistry", "executor", HEAD + """
Land D3 (spotcheck D3): the SKILL.md Gates & probes registry has no rows for `corpus/instruments/r-defect-closure.sh`
or `corpus/instruments/kill-rule-check.py`. Locate the existing registry section (`grep -ni 'gate' SKILL.md`
and find the table; if no registry table exists, add a new `## Gates & probes registry` section at the end of
the file) and append one row per instrument with all of: name, gate|probe, entry command (the exact run
command), verdict map (exit codes/printed verdicts), selftest spelling (the `--selftest` output shape),
pinned-value path (which committed file holds the pinned expected values), write scope (read-only instrument;
never mutates the lane), owner (kasegi-shokunin). Append rows only (R6); do not insert mid-table. Verify:
`grep -c 'r-defect-closure' SKILL.md` -> >= 1 and `grep -c 'kill-rule-check' SKILL.md` -> >= 1, and each
row carries the eight fields. Receipt with the appended rows.
""" + TAIL)

add("ExecD4ResultsTrack", "executor", HEAD + """
Land D4 (spotcheck D4): the round-34 dispatcher wrote `.ufo/waves/round-34/wave1-results.json`
(312874 B, sha256 `3afa3581afb14aba…`, written 2026-10-26 06:23:19Z) after the `complete` line, and it
remains untracked. The L1 commits it during integration; your job is to prepare the provenance note and
verify identity: (1) compute `sha256sum` of the file now and pin it; (2) write
`.ufo/waves/round-34/wave1-results.json.provenance.md` stating: what the file is (65 seat results from the
round-34 v2 wave), when it was written (06:23:19Z, after the closure line — the D4 defect), its sha256, and
that committing it with this note closes D4; (3) confirm the git index does not yet track it
(`git ls-files .ufo/waves/round-34/wave1-results.json` empty — expected before the L1 integration commit).
Receipt: sha256, note text, ls-files state.
""" + TAIL)

add("ExecClosureSuite", "executor", HEAD + """
Build `corpus/instruments/r35-defect-closure.sh` (committed, read-only, `bash -n`-parseable, every check
`cd %s &&`-prefixed) — the C1 counter. It contains exactly SEVEN check functions, one per round-34 verifier
routed defect (round-34-verifier-spotcheck.md §6):
- D1: SCORECARD.md carries 0 `filled by the L1` placeholder lines AND an appended correction naming c1c6a5f
  exists (`grep -c 'c1c6a5f'` >= 1).
- D2: SCORECARD.md carries an appended round-34 depth:density-row erratum: `grep -c 'round-34 depth:density row'`
  >= 1 AND `grep -c '201.2'` >= 1 (and the stale row's own bytes untouched — diff shows 0 deletions).
- D3: SKILL.md Gates & probes registry registers both instruments: `grep -c 'r-defect-closure'` >= 1 AND
  `grep -c 'kill-rule-check'` >= 1.
- D4: the results file is tracked: `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` == 1 AND
  the provenance note `.ufo/waves/round-34/wave1-results.json.provenance.md` exists.
- D5: the claims erratum exists and carries both required statements: `.ufo/waves/round-35/claims-erratum-d5.md`
  exists AND `grep -c 'discriminating invocation'` >= 1 AND `grep -c 'per-id occurrences'` >= 1.
- D6: L1Integration.md's stale dead-seat sentence is corrected: `grep -c 'did not file a receipt (dead seat'`
  == 0 AND `grep -c 'Correction (round 35)'` >= 1 in that file.
- D7: QUALITY.md carries appended supersession rows: `grep -c 'supersedes R22'` >= 1 AND
  `grep -c 'supersedes R23'` >= 1.
EACH check must exit nonzero while its defect is open (that is the closure semantics). Plain run:
`bash corpus/instruments/r35-defect-closure.sh` -> `closed=K/7 exit=0|1` plus per-check lines `D<i> check=... open=0|1`.
`--selftest` mode: run each check against a deliberately-broken fixture copy (corpus/instruments/r35-fixtures/D<i>
where that one defect is reintroduced); print `cases=7 failures=0` only if every check fails on its broken
fixture and passes on the live tree. Prove the do-nothing control is rejected: the fake suite
(c1-controls/fake-suite.sh) prints `closed=7/7 exit=0` but its --selftest prints no real case lines — your
suite's selftest must be the discriminator (document it). Also run the suite on a scratch git-archive export
of the base tree: `closed=0/7` exit 1 expected. Receipt with the full outputs and digests.
""" % LANE + TAIL)

add("ExecSelftestFixtures", "executor", HEAD + """
Create the broken-fixture set for the C1 suite's `--selftest` under `corpus/instruments/r35-fixtures/`:
one subdir per defect D1–D7 (`r35-fixtures/D1/`, …, `D7/`), each a minimal scratch tree (copies of the
relevant files) where exactly that defect is present and all others are fixed. Fixture rules: D1 = a copy of
SCORECARD.md still carrying `filled by the L1` and no c1c6a5f citation; D2 = a copy carrying the stale row
and no '201.2' erratum; D3 = a SKILL.md copy with no registry rows; D4 = an untracked results file (simulate
with a scratch git repo or report `git ls-files` on a scratch clone) and no provenance note; D5 = a scratch
directory with a claims-erratum-d5.md missing one of the two required literals; D6 = an L1Integration.md copy
still carrying the dead-seat sentence and no correction; D7 = a QUALITY.md copy with no supersedes-R22/R23
rows. Each fixture must make exactly ONE check fail (isolate the limb). Verify: running the suite with
`--selftest` over the fixture set yields `cases=7 failures=0`; and a fixture with two defects reintroduced
fails two checks (document). Receipt: fixture file list, per-fixture run outputs, digests.
""" + TAIL)

add("ExecC2Capture", "executor", HEAD + """
Create the C2 capture: capture the CISA Known Exploited Vulnerabilities catalog CSV at
https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv using
`python3 corpus/instruments/capture-source.py <url> --out corpus/source-snapshots/round-35/S052.txt`
(instrument UA). Follow redirects; record the final URL. Note for the search log: the JSON endpoint
https://www.cisa.gov/known-exploited-vulnerabilities.json returns HTTP 404 (measured 2026-10-26), so the
official CSV distribution is the primary data source. Verify the body is the catalog CSV (header row
`cveID,vendorProject,product,vulnerabilityName,dateAdded,shortDescription,requiredAction,dueDate,knownRansomwareCampaignUse`
with the record rows below it). Build `corpus/source-snapshots/round-35/manifest.json`
(record S052: path, sha256, url (the final URL), fetched_utc in strict UTC) including the exact quotes the
F18 entry will use, each with line anchors (line numbers in the captured text file), asserting
`occurrences=1`. Candidate quotes (≤25 words each, located, from the CSV): the header row itself (the nine
field names), one full catalog record line (a concrete `cveID` row with its `dateAdded` and `dueDate`
values), and a second record demonstrating a `knownRansomwareCampaignUse` value. Each quote must occur
exactly once in the capture (a full record line quoted verbatim occurs once). Self-check:
`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json
--source S052` -> every assertion `occurrences=1`, `sha256 OK`, exit 0. Report the capture size (expected
well below 10 MiB). Receipt with fetch stats, final URL, sha256, size, line numbers, manifest digest.
""" + TAIL)

add("ExecRegistryAppend", "executor", HEAD + """
Append the S052 row to `corpus/SOURCES.md` (registry), plus one `## Search log` bullet for the round-35 CISA
KEV sweep, plus the `## Registry changes` R8 lines (old→new), exactly per the ScribeSOURCESRow draft
(coordinate via agent message when it is written; do not proceed with a different shape). Row schema: 11
columns, NF=13, no `|` inside cells, id S052, kind dataset, tier A scoped to CISA's own Known Exploited
Vulnerabilities catalog statements, status mined, opened 2026-10-26, recheck 90d, used-by the F18 entry path,
anchor pinned to the round-35 capture with line locators, teaches a grounded learner benefit naming CISA as
the stating party (Q4). Do not touch any other row. Verify census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kasegi` -> exit 0 with only W04 S028/S029; `grep -cE
'^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md` -> 52; malformed=0. Receipt with the appended
lines and census output.
""" + TAIL)

add("ExecExpectedListSync", "executor", HEAD + """
Sync the recheck-audit expectation limb for the new F18 entry: `corpus/instruments/knowledge-expected.txt`
currently lists 46 knowledge entries (the F17-era sync). After the F18 entry lands, regenerate the list to 47
entries (same shape/selection rules as the existing file: one row per expected entry, comments preserved).
Then run `python3 corpus/instruments/recheck-audit.py` — it must print `expect=present expected=47 missing=0
unexpected=0 exit=0` and `strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0` (or the instrument's
exact successful shape). Receipt with the diff of the expected file and the audit output.
""" + TAIL)

add("ExecCensusAfter", "executor", HEAD + """
Run the round-end census and contract commands on the landed bytes and save the receipt:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
(expect exit 0, W04 S028/S029 only); the six contract commands: rows (52), malformed (0), tier histogram,
status histogram, duplicate ids (empty), enum/tier-inflation (empty), missing used-by (empty);
`grep -cE '^\\| F[0-9]+ \\|' corpus/README.md` -> 18. Write all outputs to your receipt. This is the C2
census after-state, measured at quiescent tip bytes.
""" + TAIL)

add("ExecBeforeReceipts", "executor", HEAD + """
Replay the frozen before-controls at the freeze commit to prove they are reproducible: from a scratch export
of `git archive 617496b9` (the freeze commit), run the commands recorded in
`c1-controls/before.txt` (ls_exit=2 for r35-defect-closure.sh, `grep -c 'filled by the L1'` = 1,
`grep -c 'c1c6a5f'` = 0, `grep -c '201.7'` = 2, `grep -c '201.2'` = 0, SKILL.md registry greps = 0,
`git ls-files` results = 0, D5/D6/D7 greps) and `c2-controls/before.txt` (frontier=17, rows=51, S052=0,
entries citing S052=0, harness entries=20 pass=20, knowledge entries=46). Confirm each matches the stored
receipt. Also confirm claims.json at the freeze commit still hashes to the committed bytes
(`git show 617496b9:.ufo/waves/round-35/claims.json | sha256sum`). Receipt: per-line match report.
""" + TAIL)

add("ExecDoNothingReject", "executor", HEAD + """
Demonstrate the do-nothing controls are rejected by the real instruments:
1. `bash corpus/instruments/r35-defect-closure.sh --selftest` -> `cases=7 failures=0` exit 0; and the fake
   suite (c1-controls/fake-suite.sh) lacks real per-case lines — show its `--selftest` output cannot satisfy
   the real suite's own selftest discriminator (document the comparison).
2. Run the C2 counters on a scratch `git archive 617496b9` export (no F18 work applied): frontier=17,
   rows=51, S052=0, entries citing S052=0, harness entries=20 pass=20, source-recheck S052 exit 2 — the
   target is unreachable by a do-nothing control.
3. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json
   --source S052` -> exit 0 on the real entry, exit != 0 on the junk twin (c2-controls/junk-f18.md's
   fabricated quote); show both outputs.
Receipt with all outputs.
""" + TAIL)

add("ExecNoHarmFinal", "executor", HEAD + """
No-harm sweep on the landed bytes (read-only): (1) `python3 corpus/instruments/density.py SKILL.md` -> mean
and block/citation counts — compare to the round-34 recorded 201.2; (2) `python3
corpus/instruments/anchorcheck.py SKILL.md` -> failure classes 0 (LOST-RECORDED=306, PIN-BROKEN=0,
ORIGIN=0, OUTSIDE-BASE=0, BASE-ABSENT=0), exit 0; (3) `git diff --numstat <base> -- SKILL.md PROVINCE.md
corpus/README.md corpus/SOURCES.md corpus/QUALITY.md SCORECARD.md LOG.md` — append-only (0 deletions);
(4) `git status --porcelain` in the lane — no stray files outside the wave/known receipts; (5) confirm no
fleet-root misroot files authored by this round's seats: run `git -C /home/vgpnk/Projects/shokunin status
--porcelain` and list any untracked file a seat wrote (name check) — report them (the L1 sweeps). Receipt.
""" + TAIL)

add("ExecRegressionC1", "executor", HEAD + """
Final C1 regression at quiescent tip bytes: run every C1 counting command from claims.json verbatim:
`bash corpus/instruments/r35-defect-closure.sh` (closed=7/7 exit=0), `bash corpus/instruments/r35-defect-closure.sh
--selftest` (cases=7 failures=0), `grep -c 'filled by the L1' SCORECARD.md` (0), `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'
corpus/SOURCES.md` (52), `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` (1). Record outputs
verbatim; compare to the after-values; report matches/mismatches.
""" + TAIL)

add("ExecRegressionC2", "executor", HEAD + """
Final C2 regression at quiescent tip bytes: run every C2 counting command from claims.json verbatim:
`grep -cE '^\\| F[0-9]+ \\|' corpus/README.md` (18), `grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'
corpus/SOURCES.md` (52), `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` (1), `grep -lE
'^source: S052 ' corpus/knowledge/*.md | wc -l` (1), `python3 corpus/instruments/frontier-recheck-count.py`
(entries=21 pass=21 exit=0), `python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-35/manifest.json --source S052` (all occurrences=1, sha256 OK, exit 0), census
validate (exit 0). Record outputs verbatim; compare to after-values; report matches/mismatches.
""" + TAIL)

add("ExecScoreGap", "executor", HEAD + """
considerthese/2026-10-25.md proposal 2 (distance to the next score, not just 'improved, held') — mine it as
a read-only computation. Produce a gap report at `.ufo/waves/round-35/wave1/ExecScoreGap.md` with: (1) the
score-5 threshold definition for depth:verifiability as recorded in SCORECARD.md (the round-22-era threshold:
a non-author audit passing all source chains with 0 unsupported current claims); (2) the measured current
facts against it — run `python3 corpus/instruments/anchorcheck.py SKILL.md` and count current unsupported
claims (entries whose `recheck:` cannot currently pass, lost-base gated entries, and any entry failing its
own recheck), plus `python3 corpus/instruments/resolve.py <lane>` summary if runnable; (3) the explicit gap
statement ("the score-relevant number today is X; the score-5 bar is Y; gap = Z"). This is a measurement,
not a score move: no axis score changes. Do NOT edit QUALITY.md; draft only. Receipt.
""" + TAIL)

add("ExecQuarantineSlice", "executor", HEAD + """
Derive the kasegi quarantine slice from the shokuknow absent-defect-register (read-only) and land verdicts:
`A=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-35/assimilation; mkdir -p "$A"`
`R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
`awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > "$A/quarantine-slice"`
Every line must carry an S-id (if any line lacks one, report it). For each row, fetch the cited source
(read-only, instrument UA) and locate the quote if possible; record per-row verdict: present-and-located /
absent (refuse, fabrication class) / unreachable / prose-class-unverifiable. Write the verdicts table to
`$A/quarantine-verdicts.md`. No row is adopted this round (wave-4 quarantine-first for the package; the lane
adopts nothing until a row is hand-checked present). Receipt.
""" + TAIL)

add("ExecIdCollisions", "executor", HEAD + """
Run the assimilation id-collision check in scratch and prove the guard once:
`S=/home/vgpnk/Projects/shokuknow; A=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-35/assimilation; mkdir -p "$A"`
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"`
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"`
`comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"`
Prove the guard once before any append: a scratch registry with an INDENTED row (0-3 leading spaces) that the
staged set collides with must produce a nonempty `collisions` — if it does not, the guard is broken and
nothing appends (report). Paste both id lists, the collision count and the renumber map into the report.
Given S031-S047 staged collisions are standing (round-34 rerun: 21), a nonempty collisions file is expected;
fix nothing in the lane (append-only registry; renumbering is scratch-side only). Receipt.
""" + TAIL)

# ---------------------------------------------------------------- scribes
add("ScribeEntryF18", "scribe", HEAD + """
Draft the F18 knowledge entry at `corpus/knowledge/cisa-kev-catalog.md`
(place it at the path; the L1 commits). It must pass Q1–Q10 (corpus/QUALITY.md): H1 title; header trio
`source: S052 — https://www.cisa.gov/known-exploited-vulnerabilities.json` with an exact anchor (capture
line), `verified-at: 2026-10-26`, `recheck:` as one executable command
(`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json
--source S052`); every load-bearing claim rests on the tier-A row S052 with a verbatim ≤25-word located
quote; attribution stays CISA's (Q4); at least one falsifiable rule and one rejected over-generalization
(Q5); documentation-only, no credentials (Q6). Content: the KEV catalog is CISA's list of known-exploited
vulnerabilities (with `cveID`, `vendorProject`, `product`, `vulnerabilityName`, `dateAdded`, `shortDescription`,
`requiredAction`, `dueDate`, `knownRansomwareCampaignUse` fields); it is a remediation-priority list keyed to
known in-the-wild exploitation — distinct from CVSS severity and from bounty reward ladders (F13/F17), so a
high-severity score is not the same signal as a KEV listing; the `dueDate` remediation clock binds CISA's
binding directive (BOD 22-01) for federal agencies; ~1,300 records (record the exact count from the capture).
Read the capture `corpus/source-snapshots/round-35/S052.txt` first; every quote must be exactly-once in it
(verify with grep). Keep total ≤ 120 lines. Do NOT cite or quote anything not in the capture.
""" + TAIL)

add("ScribeSOURCESRow", "scribe", HEAD + """
Draft the exact S052 registry row (11 columns, NF=13, no `|` in any cell), the round-35 `## Search log`
bullet (PRISMA-shaped: question / where searched / date / identified/screened/included/excluded counts /
stop rationale), and the `## Registry changes` R8 lines (old→new, e.g. "Registry 51 rows pre-append → 52
post-append", "No status/recheck/used-by cell changed on pre-existing rows; S001–S051 untouched (logged)").
Place the draft at `.ufo/waves/round-35/wave1/ScribeSOURCESRow.md`; message ExecRegistryAppend when ready —
it applies exactly this text.
""" + TAIL)

add("ScribeLesson", "scribe", HEAD + """
Compose `corpus/lessons/round-35.md` (the round lesson; the L1 commits). Required sections, all backed by
wave receipts (cite `.ufo/waves/round-35/wave1/<seat>.md` paths):
- Header: revisions (base 3266c993…, freeze 617496b9…, wave-1 dispatch commit, final integration hash as
  placeholders the L1 fills), shape (one v2 wave, seat count, role mix), answering-model note per receipt.
- `## Frozen claims — before → after`: table with C1/C2 before (frozen controls), after (named receipts),
  verdict/boundary.
- `## Gate`: assimilation (≥1 admit + ≥1 reject requirement: this round's set is the quarantine slice and
  standing refusals — record each verdict with reason and flip; state Assimilation: none adopted with the
  reason), F18/S052 admittance (URL, access date, ≤25-word located quote), any rejects with reasons.
- `## Mistakes` (M35-1 D4 results-after-complete, and any further mined from receipts): class · evidence
  pointer · captured-by · fix; every fix shown able to fail.
- `## considerthese`: proposal 2 mined → R26; other proposals unchanged with reasons.
- `## Census before → after`: both census outputs + exit codes.
- `## No-harm` table (density, anchorcheck, diff numstat, unowned writes).
- `## Open items / unverified`: list honestly.
Do not fabricate; if a receipt is missing for a claim, say so.
""" + TAIL)

add("ScribeScorecard", "scribe", HEAD + """
Compose the round-35 SCORECARD.md section (append at the end; the L1 commits): "## Round 35 — frozen claims
C1/C2 (2026-10-26)" with the claims table (C1 depth:verifiability 4 held; C2 coverage 7 held; depth:density
unchanged guard row), measurement state (digests), capabilities note (no new capability row), move-log rows
for round 35, saturation unchanged, and pointers to receipts. Follow the round-34 section's exact shape. Use
only values from the receipts; placeholders for the final lane commit are the L1's to fill.
""" + TAIL)

add("ScribeShonen", "scribe", HEAD + """
Update `SHONEN.md` (the lane's promotion checklist): the four boxes stay `[~]` unless a named non-author
verifier checks one (a wave seat is the lane, so it cannot write `[x]`). Refresh each box's evidence pointer
to round-35 receipts/commits: box 1 (decision tables/checklists — SKILL.md registry rows + no-harm receipt),
box 2 (end-to-end domain task executed and logged — the KEV capture + source-recheck is a measurement, not a
domain hunt; state if no new E2E domain task ran), box 3 (instructions executable without oral context — cite
recheck-audit 47/47 after the F18 entry and the r35 suite's selftest), box 4 (no cross-domain bleed —
PROVINCE.md diff append-only). Do not claim `[x]`.
""" + TAIL)

add("ScribeReportDraft", "scribe", HEAD + """
Draft the round report body at `.ufo/waves/round-35/wave1/ScribeReportDraft.md` using the wave receipts:
Work performed (claims named), Landed changes (each tied to LOG.md entry + commit hash placeholders),
Before → after measurements (commands + outputs), Sources & frontier (SOURCES rows before→after, rows added
by tier, rows touched old→new, frontier advanced), Trend verdicts (expansion/quality/discernment with
evidence), SHONEN lines. Leave `<LANE_HASH>` placeholders for the L1. This draft is the input to the final
report; do not write the fleet repo.
""" + TAIL)

add("ScribeErratumD5", "scribe", HEAD + """
Draft the D5 claims erratum at `.ufo/waves/round-35/claims-erratum-d5.md` (the L1 commits). It addresses the
round-34 C2 frozen-predicate wording defect (round-34-verifier-spotcheck.md §6 D5): (1) the junk-twin phrase
"source-recheck exit != 0; reviewer REFUSE" is not executable as written — the erratum restates it with a
discriminating invocation: the twin's own fabricated quote must be checked against the capture
(`source-recheck` on a capture that does not contain the quote exits != 0) — the sentence must contain the
exact literal `discriminating invocation`; (2) the phrase "every assertion occurrences=1" is literally false
when an assertion anchors a repeated quote — the erratum restates it per-id: per-assertion `occurrences`
are reported and anchored, and an unanchored non-unique quote fails — the sentence must contain the exact
literal `per-id occurrences`. Also note that future twins should carry only absent sentences. Verify the two
literals are present: `grep -c 'discriminating invocation'` >= 1 and `grep -c 'per-id occurrences'` >= 1.
Receipt.
""" + TAIL)

add("ScribeQualityDraft", "scribe", HEAD + """
Draft the exact QUALITY.md amendment text (append-only):
- D7 supersessions: a "## Round-35 supersession" block with two rows: one row beginning
  `| R26 | ... supersedes R22` stating R22's grounding is corrected (the grounded-in column cites M34-2;
  the correct mistake is M34-3 — round-34 lesson open item 10 / `mistakes-erratum-1.md`), and one row
  beginning `| R27 | ... supersedes R23` stating R23's grounded-in column must cite the round-34 lesson
  §considerthese rather than the considerthese file alone.
- R26 (new criterion, grounded in considerthese/2026-10-25.md proposal 2): "A round reports the distance to
  the next score, not only 'improved, held': a read-only gap computation against the recorded next-score
  threshold, cited in the round lesson." (place as the supersedes-R22 row or as its own R26 row per shape
  consistency with the existing table).
Draft at `.ufo/waves/round-35/wave1/ScribeQualityDraft.md`; the L1 applies your exact text.
""" + TAIL)

add("ScribeMistakesDraft", "scribe", HEAD + """
Mine the round's mistakes from the receipts into `corpus/lessons/round-35.md` `## Mistakes` (draft rows;
the L1 integrates). Minimum rows: M35-1 (D4 — wave writes landed after the `complete` line; class
landing/closure-order; captured-by R4's landed-means-committed reading not applied to the results file; fix =
commit results with provenance and quiesce before the final commit). Sweep every receipt for further defects
(rejected verdicts, overclaims, boundary violations, unverified claims) and add rows: class · evidence
pointer (receipt path:line) · captured-by (criterion or `none`) · fix (shown able to fail where possible).
Found no further mistakes? Paste the sweep command and output that found none. Draft at
`.ufo/waves/round-35/wave1/ScribeMistakesDraft.md`.
""" + TAIL)

add("ScribeGateAssimilation", "scribe", HEAD + """
Draft the assimilation Gate block for the lesson from the scout/executor receipts: quarantine slice rows with
per-row verdicts (`ExecQuarantineSlice.md`), the id-collision lists and count (`ExecIdCollisions.md`), and
standing refusals with flip conditions (`ScoutPackageThemes.md`). State "Assimilation: none adopted" with the
reasons; record ≥1 admit and ≥1 reject from the assimilation set for the non-author closure to spot-check
(e.g. reject rows with reason+flip; if any row was hand-checked present, note it as a candidate for a later
round, not adopted). Place at `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md`.
""" + TAIL)

add("ScribeSearchLog", "scribe", HEAD + """
Draft the round-35 `## Search log` bullet for the CISA KEV sweep (for ScribeSOURCESRow), PRISMA-shaped:
question ("does the lane hold a known-exploited-vulnerabilities prioritization source, distinct from severity
ladders?"), where searched (CISA's own KEV catalog JSON and the BOD 22-01 directive page; negative sweep over
the lane corpus for 'KEV', 'known exploited', 'CISA', 'exploited vulnerabilities', 'BOD 22-01'), date
2026-10-26, identified/screened/included/excluded counts, exclusion reasons, stop rationale. Place at
`.ufo/waves/round-35/wave1/ScribeSearchLog.md`.
""" + TAIL)

add("ScribeIntegrationNotes", "scribe", HEAD + """
Draft the `LOG.md` round-35 entry (append at the end; the L1 commits) and the D4 provenance-note template
(`.ufo/waves/round-34/wave1-results.json.provenance.md` content per ExecD4ResultsTrack). The LOG entry
follows the round-34 entry's shape: claims C1/C2 with before→after, wave shape and role mix, frontier items
(assimilation / considerthese / mistakes), verifier close-out placeholders, tooling line. Place the draft at
`.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md`.
""" + TAIL)

# ---------------------------------------------------------------- reviewers
add("RevC1BeforeAfter", "reviewer", HEAD + """
Independent before→after verification of C1: re-derive every C1 counter from claims.json with its own
command at the tip (r35-defect-closure.sh, its --selftest, grep 'filled by the L1', grep S-rows, git
ls-files results) and compare to the frozen before receipt and the after-values. Report matches/differences
with exact outputs. You did not author the changes.
""" + TAIL)

add("RevC2BeforeAfter", "reviewer", HEAD + """
Independent before→after verification of C2: re-derive every C2 counter (frontier count, registry rows, S052
row, entries citing S052, harness, source-recheck S052, census, knowledge-entry count) from claims.json with
its own command at the tip. Report matches/differences with exact outputs. You did not author the changes.
""" + TAIL)

add("RevClosureSuite", "reviewer", HEAD + """
Review `corpus/instruments/r35-defect-closure.sh`: exactly seven checks D1–D7; every check `bash -n`-parseable,
`cd`-prefixed, read-only; every check exits nonzero while its defect is open (test by running the suite on
a scratch copy of the base tree where all defects are open → `closed=0/7`; and on the tip → `closed=7/7`);
the `--selftest` mode genuinely runs each check against a broken fixture (r35-fixtures/D1..D7); no vacuous
`echo` check can pass the selftest. Verdict with evidence.
""" + TAIL)

add("RevSelftestFixtures", "reviewer", HEAD + """
Review `corpus/instruments/r35-fixtures/`: each of D1–D7 has a fixture where exactly that defect is present
and the other six are fixed; running the suite's `--selftest` over the set yields `cases=7 failures=0`; a
fixture with two defects reintroduced fails exactly two checks; no fixture is vacuous (each truly changes the
check's verdict). Verdict with evidence.
""" + TAIL)

add("RevD1D2", "reviewer", HEAD + """
Review the SCORECARD.md corrections: `grep -c 'filled by the L1'` -> 0; the appended correction line names
c1c6a5f and is appended (0 deletions in the round-34 section per `git diff --numstat`); the round-34
depth:density-row erratum is appended with the corrected mean 201.2 while the stale row's bytes are untouched
(0 deletions). Verdict with evidence.
""" + TAIL)

add("RevD3D4", "reviewer", HEAD + """
Review the D3/D4 fixes: SKILL.md Gates & probes registry rows for r-defect-closure.sh and kill-rule-check.py
exist and carry all eight fields (name, gate|probe, entry command, verdict map, selftest spelling,
pinned-value path, write scope, owner); `.ufo/waves/round-34/wave1-results.json` is tracked
(`git ls-files` -> 1) and the provenance note exists beside it with the file's sha256. Verdict with evidence.
""" + TAIL)

add("RevD5D6D7", "reviewer", HEAD + """
Review the D5/D6/D7 fixes: `claims-erratum-d5.md` exists and contains both required literals
(`discriminating invocation`, `per-id occurrences`); L1Integration.md's stale dead-seat sentence is gone and
a `Correction (round 35)` note is appended; QUALITY.md carries appended supersedes-R22 and supersedes-R23
rows whose grounding text is correct (M34-3 for R22; round-34 lesson for R23). All must be appends. Verdict
with evidence.
""" + TAIL)

add("RevEntryF18", "reviewer", HEAD + """
Non-author review of the final F18 entry bytes (read `corpus/knowledge/cisa-kev-catalog.md`
from the tip): Q1–Q10 verdict table (QUALITY.md), plus re-open `corpus/source-snapshots/round-35/S052.txt`
and verify every quoted string is exactly-once at its cited line (`grep -c`). Verdict ADMIT / REFUSE with
reasons. If REFUSE, list the exact failing criterion and line. You did not author the entry.
""" + TAIL)

add("RevRowS052", "reviewer", HEAD + """
Review the S052 registry row: 11 columns/NF=13; no `|` inside cells; tier A scoped to CISA's own KEV
catalog statements; anchor pinned to the round-35 capture with line locators; quote ≤25 words located in the
capture; `opened 2026-10-26`; `recheck 90d`; `used-by` exactly the F18 entry; kind dataset; status mined.
Also confirm the round-35 Search-log bullet and Registry-changes R8 lines are present and truthful. Verdict
`matches|differs` with specifics.
""" + TAIL)

add("RevNoHarm", "reviewer", HEAD + """
Independent no-harm review: `git diff --numstat 3266c993 --` over the lane's production files (SKILL.md,
PROVINCE.md, corpus/*, SCORECARD.md, LOG.md) — append-only (0 deletions); `python3 corpus/instruments/anchorcheck.py
SKILL.md` failure classes 0; density mean not below the round-34 201.2 by more than noise (report actual);
no new lost-base/misroot files at the fleet root authored by this round. Verdict.
""" + TAIL)

# ---------------------------------------------------------------- mutation-testers
add("MutClosureSuite", "mutation-tester", HEAD + """
Mutation-test r35-defect-closure.sh: for each of the seven checks D1–D7, build a mutant that makes the check
vacuous (always exit 0) — the suite's `--selftest` must then fail (the check no longer fails on its broken
fixture); and a mutant that deletes the check — the plain run must print closed<7/7. Controls: no-op and
non-compiling mutants rejected. Receipt with per-check outcomes.
""" + TAIL)

add("MutFixturesLimbs", "mutation-tester", HEAD + """
One-limb fixture mutants: for each D1–D7, take the fixture for that defect and mutate it so the defect is
absent (the fix applied) — the check must then pass on that mutant fixture (and still fail on the original);
and a mutant adding an unrelated second defect — the check must still fail for its own defect. This proves
each fixture isolates exactly one limb. Receipt with outcomes.
""" + TAIL)

add("MutC2Entry", "mutation-tester", HEAD + """
Mutation-test the F18 entry + harness binding: mutants (1) drop the `source: S052` header line, (2) change
a quote's wording (paraphrase), (3) point the anchor at the wrong line, (4) add an unregistered `--source`
to the recheck line — each must fail source-recheck or the harness (exit != 0). The pristine entry must pass.
Receipt with outputs.
""" + TAIL)

add("MutJunkTwin", "mutation-tester", HEAD + """
Attack the D5 and junk-twin controls: (1) forge a claims-erratum-d5.md that has the right filename but omits
one required literal (`discriminating invocation` or `per-id occurrences`) — the suite's D5 check must fail
on it (red-before for the check); (2) forge a junk-twin F18 candidate carrying a REAL sentence from the KEV
capture (present in S052.txt) as its only quote — the admission gate must still reject it (it is not the
drafted entry; source-recheck on a twin not listed in the manifest must exit != 0); (3) forge a twin with an
absent/fabricated sentence — source-recheck must reject it (quote not found). Receipt with outputs.
""" + TAIL)

add("MutCounterBase", "mutation-tester", HEAD + """
Prove the C2 counters cannot be met by a do-nothing control on base bytes: export `git archive 617496b9`
to scratch and run all five C2 counting commands there (frontier, registry rows, S052 row, entries citing
S052, harness) plus source-recheck S052 (exit 2, manifest absent). Each must print the BEFORE values (17 /
51 / 0 / 0 / entries=20 pass=20) — i.e. the after-state is unreachable without the claimed work. Receipt
with all outputs.
""" + TAIL)

# ---------------------------------------------------------------- scouts
add("ScoutKEVLive", "scout", HEAD + """
Live re-open of the C2 source: fetch https://www.cisa.gov/known-exploited-vulnerabilities.json under the
instrument UA; note HTTP status/bytes/final URL; extract the text and compare with
`corpus/source-snapshots/round-35/S052.txt` (normalized, whitespace-collapsed): 0 differing lines expected;
verify the gate quotes occur live exactly-once (`grep -c`); record access date 2026-10-26. Also fetch the
BOD 22-01 directive page (https://www.cisa.gov/binding-operational-directive-22-01) and note how it binds the
KEV `dueDate` clock (quote ≤25 words, located). Receipt.
""" + TAIL)

add("ScoutDatawalk", "scout", HEAD + """
Planner data-walk (the L1 holds the canonical planner seat; this item is its permitted data-walk ride). From
the freeze commit 617496b9 verify the frozen BEFORE values: replay the c1-controls/before.txt and
c2-controls/before.txt commands and confirm each value (ls_exit=2; 'filled by the L1'=1; c1c6a5f=0;
201.7=2; 201.2=0; SKILL registry greps=0; ls-files results=0; D5/D6/D7 greps; frontier=17; rows=51; S052=0;
entries citing S052=0; harness entries=20 pass=20; knowledge entries=46). Confirm claims.json predicate
sentences agree with the counters and the kill rules are identical strings in claims.json and in the wave
context. Receipt.
""" + TAIL)

add("ScoutQuarantine", "scout", HEAD + """
Independently re-derive the kasegi quarantine slice (read-only) to cross-check ExecQuarantineSlice:
`awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Confirm the slice
and verdicts (present-and-located / absent / unreachable / prose-class-unverifiable) match the executor's;
discrepancies are findings. Receive no adoption. Receipt.
""" + TAIL)

add("ScoutPackageThemes", "scout", HEAD + """
Re-confirm the merge/kasegi/ package standing refusals and their flip conditions (read-only) using the
round-34 lesson Gate as the baseline: for each refused staged entry (program-scope-rules-and-asset-boundaries,
claim-packaging-and-report-quality, cn-crowdsourced-testing-roles-and-conduct,
chinese-crowd-testing-national-standard-2026-10-23, chinese-criminal-thresholds-and-authorisation,
chinese-program-severity-instrument, program-severity-ladders-and-reward-scales) state whether ANY flip
condition cleared this round (e.g. S036/BILISRC row now registered? S081/S082/S077/S078/S079?) by checking
the current lane registry and captures. Deliver the "Assimilation: none" verdict with per-entry reasons.
""" + TAIL)

add("ScoutSiblingSweep", "scout", HEAD + """
Negative sweep across sibling lanes for the C2 ground: search /home/vgpnk/Projects/shokunin/*-shokunin/
(except kasegi) corpora/SKILL.md for 'CISA', 'KEV', 'known exploited', 'BOD 22-01', 'exploited
vulnerabilities', 'remediation deadline' — report per-sibling hits (path:line) or zero-hits, so the connector
can rule on contested scope. Also check the fleet root's merge/considerthese themes for the same tokens.
Receipt.
""" + TAIL)

add("ScoutLeads", "scout", HEAD + """
Verify the three standing leads (corpus/SOURCES.md `## Leads (unopened)`) remain unopened and record their
state: (1) Google Big Sleep reporting tracker at https://goo.gle/bigsleep; (2) ISO/IEC 29147/30111 standard
records at https://www.iso.org/standard/72311.html and https://www.iso.org/standard/69725.html; (3) UK AI
Security Institute report at https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing.
For each: probe read-only (instrument UA), record HTTP status and whether it is a substantive new source this
round could have used; none is adopted this round (the leads stay leads). Receipt.
""" + TAIL)

# ---------------------------------------------------------------- critics
add("CritC1Kill", "critic", HEAD + """
Falsify C1 as declared: attempt to construct states that satisfy the after-predicate while violating the
kill rule: (1) an r35-defect-closure.sh printing closed=7/7 with seven vacuous checks (does the --selftest
discriminator catch it?); (2) a D5 erratum carrying both literals but not actually fixing the wording defect;
(3) a D4 delta where results.json is tracked but the file is a placeholder (identity vs the dispatcher's
bytes); (4) a D1 state where the prose is gone but the correction names a wrong hash; (5) a D7 row that
mentions supersedes-R22 without correcting the grounding. For each, state whether the landed check catches it
(pass) or not (gap -> record). Verdict.
""" + TAIL)

add("CritC2Kill", "critic", HEAD + """
Falsify C2 as declared: build junk constructions that pass the shape counters (frontier=18, rows=52, S052
row present, harness entries=21 pass=21) without a real capture or a real admission: (1) an entry quoting a
fabricated string with a fake manifest record (can source-recheck detect it? run it); (2) a row with no
opened source; (3) an entry citing S052 without ever opening the KEV JSON; (4) a KEV capture that is an HTML
error page renamed to .txt with a self-consistent manifest. State which landed checks catch each and which do
not (record the residual gaps). Verdict.
""" + TAIL)

add("CritOverclaim", "critic", HEAD + """
Check C1/C2 before/after statements against the receipts and the frozen controls: every after-value must have
a measured command output; no universal clause beyond what the counting command enumerates; no claim that a
check 'verifies' while its receipt is missing; the report and lesson must not overstate closure counts beyond
measured figures. Report every overclaim or unmeasured value with its location.
""" + TAIL)

add("CritBoundary", "critic", HEAD + """
Scope-guard critique: scan this round's wave receipts and the tip tree for files a seat wrote outside the
lane write scope (check the fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` for
untracked files naming kasegi/round-35; check no sibling repo or shokuknow was touched; check no lane git/jj
state was mutated by seats). Also check every seat used the scratch root under `/fast/scratch/hyaku/kasegi-r35`
and deleted its tree (report any leftover). Verdict.
""" + TAIL)

add("CritMistakes", "critic", HEAD + """
Critique the lesson's Mistakes rows (M35-1 and any others): each row must have a real evidence pointer, a
captured-by (or `none`), a fix, and the fix shown able to fail (a red-before run). Flag any mistake row that
is prose without a reproducible check. Verdict.
""" + TAIL)

# ---------------------------------------------------------------- connectors
add("ConnClaims", "connector", HEAD + """
Cross-index the seven routed defects D1–D7 to their landed fixes: for each defect name the fix artifact
(file/line), the closure check in r35-defect-closure.sh, and the receipt that proves it; produce a coverage
table (D1..D7 all 7 mapped). Flag any defect with no fix, no check, or no receipt. Also connect D5/D7 to the
appended erratum/supersession artifacts and confirm the fit-freeze satisfiability step is recorded.
""" + TAIL)

add("ConnSibling", "connector", HEAD + """
Synthesize the sibling-overlap scan (ScoutSiblingSweep) into a contested-scope ruling draft for the lesson
and report: any sibling corpus holding CISA/KEV/known-exploited ground is reported, not absorbed
(PROVINCE adjacency). State the ruling (no contested scope / report-to-lane) for each hit.
""" + TAIL)

add("ConnCrossCheck", "connector", HEAD + """
Cross-check the source chains end to end: for S052 verify registry row ↔ capture file ↔ manifest record ↔
entry header `source:` ↔ harness `PASS F18` ↔ source-recheck assertion ids all agree (ids, URLs, sha256);
for the round-35 manifest verify manifest records ↔ files ↔ registry rows. Report any dangling link. Also
confirm census W04 pair is unchanged and no new warnings appeared.
""" + TAIL)

add("ConnTrends", "connector", HEAD + """
Map the three learning trends to the round's evidence: expansion (F18 admitted on uncovered coverage-map
ground, entry citing mined S052; capability rows none), quality (D1–D7 closures + suite; recheck-audit
47/47; no admitted entry failed re-check), discernment (gate decisions vs the non-author spot-check; any
disagreement becomes a lesson-backed criterion). Produce the evidence table the report's Trend verdicts
section will cite; do not decide the verdicts (the L1 does).
""" + TAIL)

# ---------------------------------------------------------------- sentinels
add("SentCred", "sentinel", HEAD + """
Credential/secret scan of every new artifact this round: the S052 capture (KEV JSON is public federal data);
the F18 entry; manifests; receipts; the new suite and fixtures. Scan for session tokens, cookies, private
URLs, `op://` refs, passwords, API keys, personal data. The KEV capture must contain no credential material
(it should be pure JSON); if it does, refuse it and report the location. Verdict clean/flag with locations.
""" + TAIL)

add("SentScopeFinal", "sentinel", HEAD + """
Final scope audit: (1) verify no seat wrote outside the lane repo (check the fleet root status for untracked
round-35-named files: `git -C /home/vgpnk/Projects/shokunin status --porcelain` and name any hit; the L1
sweeps them); (2) verify no lane git/jj mutation was done by seats (read-only git only); (3) verify the
shokuknow tree is untouched (`git -C /home/vgpnk/Projects/shokuknow status --porcelain` read-only); (4)
verify scratch discipline: no `/fast/scratch/hyaku/kasegi-r35/<seat>` leftover for this round's seats
(except the L1's own). Verdict.
""" + TAIL)

# ---------------------------------------------------------------- simplifiers
add("SimplifierCleanup", "simplifier", HEAD + """
YAGNI sweep of the new instruments: (1) r35-defect-closure.sh — every check loads a distinct defect; no two
checks test the same fact; no dead or duplicate code; (2) the r35-fixtures set — no redundant fixtures; (3)
the F18 entry — no filler, no redundant claims; (4) the wave's receipts — no duplicate artifacts. Propose
deletions only where behavior is provably preserved (run the counters before/after your proposal and paste
both outputs). Receipt.
""" + TAIL)

add("SimplifierDocs", "simplifier", HEAD + """
YAGNI/minimality review of the drafted docs (read .ufo/waves/round-35/wave1/Scribe*.md drafts): the report
draft, lesson draft, scorecard draft and SHONEN edits must each carry only evidence-backed statements; flag
filler, repetition, or placeholder prose that will not be filled; propose deletions where content is
non-load-bearing (preserve the contract-required sections). You edit nothing; propose in your receipt.
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
flash = roles.get("executor", 0) + roles.get("scribe", 0) + roles.get("critic", 0) + roles.get("simplifier", 0) + roles.get("sentinel", 0)
print("m_flash roles share: %d/%d = %.1f%%" % (flash, len(ITEMS), 100.0 * flash / len(ITEMS)))

spec = {
    "wave": "kasegi-r35-build",
    "reportDir": RD,
    "maxLanes": 128,
    "axes": ["depth:density", "depth:verifiability", "coverage"],
    "milestone": "round-35 build wave: C1 D1-D7 closure suite; C2 F18 CISA KEV admission",
    "context": HEAD + TAIL,
    "items": ITEMS,
}
out = ".ufo/waves/round-35/wave1-spec.json"
with open(out, "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
print("wrote", out, len(json.dumps(spec)))
