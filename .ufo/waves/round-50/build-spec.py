#!/usr/bin/env python3
"""Build the round-50 wave-1 spec (one v1 wave, 32 seats, policy v1 band 32-48)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = "/fast/scratch/hyaku/kasegi-r50"
WAVE_DIR = ".ufo/waves/round-50/wave1"
BASE = "c5e36360f5226c97d28f1937961b15c90e58827f"
FREEZE = "a2de23b025d8f1600c6a4387f22794dfc5ba2b88"
CLAIMS = LANE + "/.ufo/waves/round-50/claims.json"
EXPORT = SCRATCH + "/base-export"

GODSPEED = (
    "/skill:godspeed\n"
    "You are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n"
    "2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. "
    "Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. "
    "Act directly via tool calls.\n\n"
)

CONTEXT = (
    "Round 50 kasegi only. Lane root {lane}; fleet root {fleet}; sole integration owner is the L1 agent id "
    "KasegiR50 (message ONLY KasegiR50; never agent://all). Frozen claims: {claims} (base {base}, freeze "
    "commit {freeze}).\n"
    "WRITE BOUNDS: you may write only (a) under your scratch dir {scratch}/<your-seat-name>/ and (b) your "
    "report file at {lane}/" + WAVE_DIR + "/<your-seat-name>.md plus, when your item says so, draft files "
    "under {lane}/" + WAVE_DIR + "/ only. Every `Report:` trailer path is relative to the lane root \u2014 write it "
    "at {lane}/<that path>. Do NOT write into corpus/, do NOT edit corpus/SOURCES.md, SCORECARD.md, LOG.md, "
    "SKILL.md or PROVINCE.md (the L1 integrates); do NOT commit, push, or run any mutating git/jj command "
    "anywhere; do NOT touch the fleet repo, sibling lanes, .ufo/state, {fleet}/templates/ or {fleet}/scripts/. "
    "A read-only base export of the freeze base exists at {export} \u2014 shared, read-only, do not modify or "
    "delete it.\n"
    "SCRATCH: everything you clone/run heavy under {scratch}/<your-seat-name>/ (mkdir -p first); /tmp is for "
    "files under 50 MB only; honour TMPDIR; delete your scratch dir before you yield (trap/finally) after "
    "copying receipts into your report; one live clone per seat (git worktree/git archive/git clone --shared).\n"
    "TOOLING: you may install/upgrade tools that help \u2014 read /home/vgpnk/.omp/agent/RULES.md first (official "
    "channels, update-safety gate) and record tool/version/channel/reason in your report. PACMAN GUARD: all "
    "pacman transactions are PAUSED host-wide \u2014 never pacman -S/-Sy/-Syu/-U/-R, never restart host services; "
    "install via uv tool / npx / an official binary in ~/.local/bin only.\n"
    "ROUTING: never pass `model`; the host route table decides. You are a leaf: do not call task yourself. "
    "An unrun check has not passed; ground every claim in your report with a command output or file:line."
).format(lane=LANE, fleet=FLEET, claims=CLAIMS, base=BASE, freeze=FREEZE, scratch=SCRATCH, export=EXPORT)

CONTEXT = CONTEXT  # (shared context string built above)

items = []


def add(name, role, item):
    item = item + ("\n\nYou are seat {n}. Your report file: {wd}/{n}.md "
                   "(absolute: {lane}/{wd}/{n}.md). Write it before you yield."
                   .format(n=name, wd=WAVE_DIR, lane=LANE))
    items.append({"name": name, "role": role, "item": item})


TEMPLATE = GODSPEED + CONTEXT + "\n\n# Seat assignment\n{{item}}"


# ---------------------------------------------------------------- connectors
add("R50Conn1", "connector",
    "Sibling-overlap scan for C2. grep -ri 'epss' across {fleet}/*-shokunin/corpus (exclude this lane) and "
    "report per lane: which hold EPSS material, at what depth (row/entry/mention). Then answer: does a kasegi "
    "F31 (EPSS exploit-prediction scoring) duplicate ground a sibling lane already holds? Cross-lane overlap is "
    "your only question; do not judge kasegi's internal novelty (that is R50Rev2).".format(fleet=FLEET))

add("R50Conn2", "connector",
    "Pattern scan across the fleet and this lane's own history for census-freshness/staleness gates: grep for "
    "'citation-survival', 'stale census', 'freshness' in {fleet}/*-shokunin/corpus/instruments and this lane's "
    "lessons. Report which patterns exist, which lane holds them, and what kasegi's planned gate "
    "(claims.json C1) could reuse or must deliberately not copy.".format(fleet=FLEET))

# ----------------------------------------------------------------- executors
add("R50Exec1", "executor",
    "BUILD the C1 gate draft. Read the frozen sentence for C1 in {claims} and the interfaces of "
    "{lane}/corpus/instruments/resolve.py (run `python3 resolve.py --help`). Implement "
    "census-freshness-check.py: stdlib-only; runs resolve.py over the tree (subprocess or import), generates "
    "citation-survival.md and .tsv into a scratch dir, byte-compares them to the committed files; prints "
    "CENSUS-FRESH=ok and exits 0 only on byte equality; otherwise prints a unified diff summary "
    "(CENSUS-FRESH=stale plus the differing line count) and exits 1; honours TMPDIR/--scratch; never writes "
    "/tmp. Also write a selftest that builds two mutant fixtures (one stale census md with one number changed; "
    "one tampered tsv with a row dropped), runs the gate logic against them, and asserts exit 1 on both plus "
    "exit 0 on a fresh pair. Deliver BOTH files as drafts R50Exec1-gate.py and R50Exec1-selftest.py under "
    "{lane}/" + WAVE_DIR + "/ plus your report. Do NOT write into corpus/.".format(claims=CLAIMS, lane=LANE))

add("R50Exec2", "executor",
    "DETERMINISM probe for C1. resolve.py must be byte-deterministic over identical trees or the C1 gate is "
    "void. Run {lane}/corpus/instruments/resolve.py twice over the shared base export {export} into two "
    "scratch output dirs and `cmp` the generated citation-survival.md and .tsv pairwise; then once over the "
    "live tree. For every difference, name the cause (dict ordering, walk order, timestamps, embedded absolute "
    "paths). Also read resolve.py source and list every input that could vary between runs (env vars, locale, "
    "readdir order). Conclude DETERMINISTIC/NOT with evidence.".format(lane=LANE, export=EXPORT))

add("R50Exec3", "executor",
    "S080 CAPTURE. The scout seat R50Scout1 chooses the capture URL; if its report is not yet written when you "
    "start, use https://www.first.org/epss/ as the capture URL. Study the round-49 capture pattern first: "
    "{lane}/corpus/source-snapshots/round-49/manifest.json, {lane}/corpus/instruments/capture-source.py and "
    "source-recheck.py interfaces (read them). Fetch the capture with a plain UA, record bytes + sha256 + line "
    "count, and write a manifest with >=4 assertions, each a located quote <=25 words with a numeric line "
    "anchor that source-recheck.py can verify (quote exactly-once). Ground the teaches cell: probability of "
    "exploitation semantics, percentile, model version/data sources, API access. Deliver S080.txt and "
    "manifest.json drafts under {lane}/" + WAVE_DIR + "/ plus your report.".format(lane=LANE))

add("R50Exec4", "executor",
    "Round-49 routed-defect-5 receipts (evidence hygiene). The round-49 spotcheck says non-target-guard outputs "
    "were quoted without committed receipts. Produce receipt files under {lane}/" + WAVE_DIR + "/receipts/: "
    "run anchorcheck.py SKILL.md, density.py SKILL.md --label SKILL, recheck-audit.py (read each instrument's "
    "interface first), saving full stdout+stderr, the exact command line and the exit code into one file per "
    "run (anchorcheck-SKILL.receipt.txt, density-SKILL.receipt.txt, recheck-audit.receipt.txt). These are what "
    "the round report may cite.".format(lane=LANE))

add("R50Exec5", "executor",
    "Shokuknow re-screen (assimilation duty). Re-run the id-collision screen exactly as the round prompt "
    "\u00a710 specifies: extract lane registry ids with the 0-3-space pattern from {lane}/corpus/SOURCES.md and the "
    "staged ids from /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md, comm -12 them, and diff "
    "the package's registry baseline against the lane registry to characterize the mass id drift. Then read "
    "the package's MERGE-REPORT.md and answer: does the package hold any ground C1 or C2 needs this round? "
    "Deliver reg-ids, staged-ids, collisions, the drift summary and an ADOPT-this-round / REFUSE-with-reason "
    "verdict under {lane}/" + WAVE_DIR + "/assimilation/. Never write into /home/vgpnk/Projects/shokuknow.".format(lane=LANE))

add("R50Exec6", "executor",
    "SCORECARD correction drafts for the four round-49 routed SCORECARD defects (read "
    "{lane}/corpus/lessons/round-49-verifier-spotcheck.md \u00a75 items 2-4): (a) the r49 depth:density row's false "
    "'SKILL.md was not edited' claim; (b) the C2 cells quoting registry=78 vs the committed 79; (c) the "
    "'Planned for round 50' row citing a scout seat report that never ran; (d) the report's misnamed ledger "
    "pointer (that one is a fleet-repo report erratum \u2014 draft the erratum text too). Draft exact APPEND-ONLY "
    "entries (entry headers, before/after wording) as one markdown file under {lane}/" + WAVE_DIR + "/ — the "
    "lane's append-only style keeps superseded text in place. Do not edit SCORECARD.md or the report.".format(lane=LANE))

add("R50Exec7", "executor",
    "Frozen-claims replay + LOG skeleton. (1) Read {lane}/corpus/instruments/freeze-check.py's interface; if it "
    "can replay {claims} against an export, run it against {export} and report the output; if it cannot, say "
    "so and state what it checks instead. (2) Draft the LOG.md round-50 entry skeleton (sections: claims "
    "frozen, wave, C1 landing, C2 landing, measurements, census before/after) with placeholder markers, as a "
    "markdown file under {lane}/" + WAVE_DIR + "/. Do not edit LOG.md.".format(claims=CLAIMS, export=EXPORT, lane=LANE))

# ------------------------------------------------------------------- scribes
add("R50Scribe1", "scribe",
    "Draft corpus/lessons/round-50.md \u00a7 Mistakes. Read {lane}/corpus/lessons/round-49.md and "
    "round-49-verifier-spotcheck.md \u00a75; from the round-50 evidence already committed (freeze.txt, controls/) "
    "and the routed defects, draft the mistakes table rows (class | evidence pointer | captured-by | fix) for: "
    "the r49 evidence-hygiene defect now becoming a receipts duty, and any stale-number class you can evidence "
    "(e.g. the live resolve.py run at the base tree reading 4771 distinct citations / 202 files vs the "
    "committed census 4758 / 201 \u2014 verify that from the L1's wave-dir note r50-live-resolve.txt if present). "
    "Deliver the draft under {lane}/" + WAVE_DIR + "/. Do not edit corpus/lessons/.".format(lane=LANE))

add("R50Scribe2", "scribe",
    "Draft the registry/frontier rows for C2. Read the S078 registry row in {lane}/corpus/SOURCES.md, the F30 "
    "row and r49 amendment in {lane}/corpus/README.md, and the F30 amendment in {lane}/PROVINCE.md. Draft: "
    "(1) the S080 registry row in the identical 11-column schema (id S080; kind docs or spec as the capture "
    "warrants; tier A scoped to FIRST's own EPSS model documentation; status mined; opened 2026-10-30; recheck "
    "90d; used-by corpus/knowledge/epss-exploit-prediction-scoring.md) with teaches/anchor cells as TBD "
    "markers to fill from the capture manifest; (2) the F31 frontier row in the README table's exact shape; "
    "(3) the one-line PROVINCE.md end-of-file F31 amendment. No cell may contain a literal or escaped pipe. "
    "Deliver all three drafts under {lane}/" + WAVE_DIR + "/.".format(lane=LANE))

add("R50Scribe3", "scribe",
    "Draft the F31 knowledge entry skeleton: {lane}/corpus/knowledge/epss-exploit-prediction-scoring.md "
    "following the round-49 entry pattern (read {lane}/corpus/knowledge/cve-services-publication-api.md): "
    "front matter with source: S080, the capture sha/bytes TBD, verified-at 2026-10-30, and a recheck: line "
    "naming `source-recheck.py --manifest corpus/source-snapshots/round-50/manifest.json --source S080`; "
    "section stubs for probability-vs-severity (distinction from F01), data sources and model version, API "
    "access, non-combination-with-CVSS guidance, and a Limits section. Deliver the draft under {lane}/" +
    WAVE_DIR + "/.".format(lane=LANE))

# -------------------------------------------------------------------- scouts
add("R50Scout1", "scout",
    "SOURCE OPENING for S080. Open https://www.first.org/epss/ and its linked model/data/API documentation "
    "pages (fetch with a plain UA; record HTTP status, byte size, sha256 for each). Decide which single "
    "first-party URL is the best S080 capture: it must carry the scoring semantics (EPSS probability 0-1, "
    "percentile, current model version and training-data provenance, API access path). Record the located "
    "quotes (<=25 words each, with line anchors in the final capture text) that ground those four facts, and "
    "hand the capture choice + quotes to {lane}/" + WAVE_DIR + "/R50Scout1-capture-choice.md for R50Exec3. If "
    "www.first.org/epss/ carries JS-only content with no semantics in raw bytes, say so and pick the linked "
    "spec/data page that does.")

add("R50Scout2", "scout",
    "EPSS limits recon. Fetch https://api.first.org/data/v1/epss?cve=CVE-2024-3094 (or another recent CVE) "
    "and compare the live API response's model version/date against the documentation page's. Record what a "
    "documentation capture will NOT cover (live per-CVE scores, bulk data, schema fields only in the API) so "
    "the entry's Limits section is accurate. Deliver notes in your report.")

add("R50Scout3", "scout",
    "considerthese mining. Read {lane}/considerthese/2026-10-26.md proposal 1 (make distance-to-next-score "
    "explicit). Read {lane}/corpus/instruments/score-gap.py and report exactly what it already encodes for the "
    "verifiability 4->5 gap (the 22 gated rechecks) and whether any coverage saturation criterion exists "
    "anywhere in SCORECARD.md. Deliver a grounded verdict: does the proposal add anything beyond score-gap.py, "
    "and if yes, the exact QUALITY.md criterion text (id R65) the L1 could add. This is the round's single "
    "considerthese item.".format(lane=LANE))

# ------------------------------------------------------------------ reviewers
add("R50Rev1", "reviewer",
    "ATTACK C1's frozen sentence (read {claims} C1). Enumerate every implementation route that prints "
    "CENSUS-FRESH=ok while the committed census is actually stale: e.g. the gate regenerating into the repo "
    "and comparing a file to itself; resolve.py invoked with a different scope than the census of record; only "
    "the .md compared and not the .tsv; a gate that regenerates, then overwrites the committed file, then "
    "compares. For each route, name the exact self-test fixture case that must exist to kill it. Deliver the "
    "attack list under {lane}/" + WAVE_DIR + "/.".format(claims=CLAIMS, lane=LANE))

add("R50Rev2", "reviewer",
    "ATTACK C2's novelty. Read the F01, F05, F13 and F18 frontier rows and their entries in {lane}/corpus. "
    "Write the strongest possible case that EPSS duplicates existing ground (CVSS severity semantics, CWE "
    "ranking methodology, platform reward ladders, KEV presence). Then verdict: does the F31 distinction as "
    "frozen in {claims} C2 survive your strongest case? Be honest either way; the L1 lands what survives.".format(lane=LANE, claims=CLAIMS))

add("R50Rev3", "reviewer",
    "REVIEW the C1 gate draft (R50Exec1-gate.py and R50Exec1-selftest.py under {lane}/" + WAVE_DIR + "/ once "
    "present; if absent, review the frozen sentence against resolve.py's actual interface and predict the "
    "defects). Check: scope equality (the gate must generate over the same file set the committed census "
    "describes), byte comparison (not normalized), exit-code discipline (verdict map: unreadable input -> "
    "mapped exit per R59), no /tmp writes, TMPDIR honoured. Findings by severity with file:line.".format(lane=LANE))

add("R50Rev4", "reviewer",
    "COUNTER-SOUNDNESS review for C2. Read {lane}/corpus/instruments/frontier-recheck-count.py docstring rules "
    "A-G and {lane}/corpus/instruments/source-recheck.py. Name every hole a fraudulent F31 admission could "
    "slide through (e.g. teaches cell copied from F01; capture sha truncated; manifest quotes that exist "
    "twice), and state for each whether the round's evidence (capture + manifest + recheck exit 0) closes it "
    "or the L1 must hand-check it.".format(lane=LANE))

add("R50Rev5", "reviewer",
    "ROUND RECEIPTS. Re-run every counting command the round will cite, at the current tree, and record full "
    "outputs + exit codes in your report: grep -cE '^\| F[0-9]+ \|' {lane}/corpus/README.md; grep -cE "
    "'^\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\|' {lane}/corpus/SOURCES.md; bash "
    "{fleet}/scripts/sources-census.sh validate --file {lane}/corpus/SOURCES.md; python3 "
    "{lane}/corpus/instruments/score-gap.py. These are the only numbers the report may cite from your seat.".format(lane=LANE, fleet=FLEET))

add("R50Rev6", "reviewer",
    "SCHEMA review of the C2 drafts (R50Scribe2's three drafts + R50Exec3's manifest, under {lane}/" + WAVE_DIR +
    "/ once present). Verify: 11-column registry row shape; zero literal or escaped pipes in any cell; recheck "
    "cell is a valid ISO date / NN d / symbolic cadence; used-by exact path; README frontier row cells match "
    "the existing table; PROVINCE amendment is one line. Report every violation with the exact draft line.".format(lane=LANE))

# ------------------------------------------------------------------- critics
add("R50Crit1", "critic",
    "FALSIFY C1. Strongest position: the census-freshness gate is the wrong fix for the round-49 stale-census "
    "mistake \u2014 the real fix is protocol (regenerate the census every round), and a gate that compares committed "
    "bytes to a live regeneration is gamed by the round itself committing the regeneration before running the "
    "gate. Write the falsification in full; then verdict: does the frozen sentence survive it as a CAPABILITY "
    "claim (a fail-closed tripwire against the stale class), even if it cannot prove the census is TRUE? "
    "Distinguish freshness (bytes match the instrument on this tree) from truth (the instrument measures what "
    "the axis says).")

add("R50Crit2", "critic",
    "FALSIFY C2. Argue EPSS is not coverage ground the lane lacks: FIRST already sources S001/S002/S018, "
    "scoring semantics live in F01, and a probability score is severity-adjacent. Then verdict: does the F31 "
    "admission as frozen survive? Consider what would make it honest even if thin: a stated, checkable "
    "distinction and an accurate Limits section.")

add("R50Crit3", "critic",
    "ATTACK THE KILL RULES. For each claim in {claims}: construct one scenario where the kill rule fires but "
    "the claim is actually fine (false kill), and one where the claim passes while the kill rule stays silent "
    "(false pass). Conclude whether each kill rule is load-bearing or decorative, and what single amendment "
    "would make it load-bearing if decorative.".format(claims=CLAIMS))

add("R50Crit4", "critic",
    "ADVERSARIAL READ of the do-nothing controls ({lane}/.ufo/waves/round-50/controls/do-nothing-c1.txt and "
    "do-nothing-c2.txt). Could a do-nothing control reach either expect_after in {claims} \u2014 e.g. does the C2 "
    "counter at base print anything near rows=31/registry=80, and could the C1 counter's absence at base be "
    "misread as success by a careless judge? State exactly what the closure judge must check so a do-nothing "
    "round cannot pass.".format(lane=LANE, claims=CLAIMS))

# ----------------------------------------------------------- mutation-testers
add("R50Mut1", "mutation-tester",
    "MUTATE the C1 gate. Once R50Exec1's drafts exist under {lane}/" + WAVE_DIR + "/, copy them to your scratch "
    "and apply >=6 mutants: exit-0-always; compare only the .md; normalize away whitespace before comparing; "
    "regenerate into the repo dir and compare the file to itself; skip the .tsv entirely; invert the "
    "comparison order. Run R50Exec1's selftest against every mutant. Report a table: mutant | caught by "
    "selftest (which case) | slipped through. Any slip names a fixture case the L1 must add before landing.".format(lane=LANE))

add("R50Mut2", "mutation-tester",
    "MUTATE the C2 surface. Shipped positive controls: the F30 row + S078 row ({lane}/corpus). In scratch "
    "copies, demonstrate >=5 mutants of an F31/S080 pair that frontier-recheck-count.py would NOT catch (e.g. "
    "teaches cell copied from F01; capture sha truncated to 8 chars; manifest quote located twice; registry "
    "row used-by pointing at a nonexistent entry; status cell `mined ` with trailing space). For each: does "
    "sources-census.sh or a byte check catch it instead? Deliver the mutant table and the hand-check list the "
    "L1 owns.".format(lane=LANE))

# --------------------------------------------------------------------- labrat
add("R50Lab1", "executor",
    "PROBE: is the committed census stale at base? Run {lane}/corpus/instruments/resolve.py over the shared "
    "base export {export} into your scratch (takes ~5 minutes), and `diff` the generated citation-survival.md "
    "against {export}/corpus/instruments/citation-survival.md. Report FRESH or STALE with the differing "
    "totals line (distinct citations, scope file count). This decides whether the C1 landing MUST include "
    "regenerating the census (it must, if stale). Note: a live-tree run by the L1 already read 4771 distinct / "
    "202 files vs the committed 4758 / 201 \u2014 confirm or refute that on the export.".format(lane=LANE, export=EXPORT))

# ------------------------------------------------------------------- revenger
add("R50Revgr1", "revenger",
    "REVERSE-ENGINEER resolve.py ({lane}/corpus/instruments/resolve.py): enumerate every input that could "
    "vary between two runs over byte-identical trees \u2014 dict/set iteration order, os.walk/readdir order, locale, "
    "environment variables read, absolute-path embedding, timestamps. For each, state with source file:line "
    "evidence whether it can change the output bytes. Conclude with the exact conditions under which the C1 "
    "gate's byte comparison is sound.".format(lane=LANE))

# ------------------------------------------------------------------- sentinel
add("R50Sent1", "sentinel",
    "SECURITY review of the files this round will add or change: the gate instrument (R50Exec1 drafts), the "
    "S080 capture + manifest (R50Exec3), the F31 entry and registry/frontier rows (scribes' drafts), all under "
    "{lane}/. Can any write outside the repo, follow a symlink out, execute fetched content, or phone home? "
    "Read capture-source.py and source-recheck.py for the fetch path (SSRF, redirects, file:// handling). "
    "Report findings by severity with file:line.".format(lane=LANE))

# ----------------------------------------------------------------- simplifier
add("R50Simp1", "simplifier",
    "SMALLEST GATE. Read resolve.py's interface and the frozen C1 sentence in {claims}. Propose the smallest "
    "gate design that satisfies the sentence (budget <=120 lines including the freshness print). When "
    "R50Exec1's draft appears under {lane}/" + WAVE_DIR + "/, review it against the budget and report what to "
    "cut (boring design beats needless abstraction; no normalized comparisons, no extra modes).".format(claims=CLAIMS, lane=LANE))

# ------------------------------------------------------------------ distiller
add("R50Dist1", "scribe",
    "DISTILL the attack surface into a one-page checklist. Read {lane}/corpus/lessons/round-49.md, "
    "round-49-verifier-spotcheck.md \u00a75, and corpus/QUALITY.md R50-R64. Produce the 12 most likely defect "
    "classes for this round's two claims (e.g. stale-census self-certification, F31 teaches-cell duplication, "
    "registry-row pipe violation, kill-rule decoration) as a numbered checklist with the R-criterion or lesson "
    "that grounds each, and deliver it under {lane}/" + WAVE_DIR + "/R50Dist1-checklist.md for the review "
    "seats.".format(lane=LANE))

spec = {
    "wave": "kasegi-r50-census-freshness-and-epss",
    "reportDir": WAVE_DIR,
    "maxLanes": 48,
    "axes": ["depth:verifiability", "coverage"],
    "milestone": "One frozen census-freshness gate capability (C1, depth:verifiability) and one frozen frontier admission (C2, F31 EPSS), attacked by 14 review/critic/mutation/labrat/sentinel seats",
    "context": CONTEXT,
    "template": TEMPLATE,
    "items": items,
}

out = os.path.join(LANE, ".ufo/waves/round-50/wave1-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
roles = {}
for it in items:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("wrote", out, "items", len(items))
print("roles", roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat", "sentinel"))
print("attack seats", attack, "share %.1f%%" % (100.0 * attack / len(items)))
