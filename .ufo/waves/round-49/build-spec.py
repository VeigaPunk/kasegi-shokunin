#!/usr/bin/env python3
"""Build the round-49 wave-1 spec (one v2 wave, 64 seats).

The L1 is the integration owner; seats are read-only on production files and
return findings in their own report file.  This script only writes the spec
JSON; it never touches the lane tree.
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = "/fast/scratch/hyaku/kasegi-r49"
WAVE_DIR = ".ufo/waves/round-49/wave1"
BASE = "9b1662a2fa0e7c7b0ad6c4d45cb7786f27bdd03b"
FREEZE = "1954022d91c2063d0ce25bb5551778bc0b3e70f3"
CLASS_JSON = LANE + "/.ufo/waves/round-49/controls/class-before.json"
CLAIMS = LANE + "/.ufo/waves/round-49/claims.json"
COUNTER = LANE + "/corpus/instruments/citation-ground-check.py"
CAPTURE = LANE + "/corpus/source-snapshots/round-49/S078.txt"
MANIFEST = LANE + "/corpus/source-snapshots/round-49/manifest.json"

CONTEXT = (
    "Round 49 kasegi only. Lane root {lane}; fleet root {fleet}; sole integration owner KasegiR49. "
    "Frozen claims: {claims} (base {base}, freeze commit {freeze}). "
    "C1 depth:verifiability — every citation in the lane's own files that names an existing file but is "
    "written so the resolver cannot open it is re-grounded to a path that opens, recorded in the committed "
    "ledger corpus/instruments/citation-reground-ledger.md; the frozen counter {counter} must read "
    "'unresolved-class=0' at the measured revision (it reads 68 at the base). "
    "C2 coverage — one new frontier row F30 for the CVE Services API publication surface, backed by the "
    "tier-A first-party capture {capture} (sha256 1403e607cf2c5be529b9d34bad5f1ebe6b72c7673fb1de2fda79431bf1684472, "
    "282553 bytes, 8374 lines), a knowledge entry, a registry row and a manifest {manifest}; the frozen "
    "counter corpus/instruments/frontier-recheck-count.py must read "
    "'FRONTIER-CENSUS rows=30 admitted=30 closed=30 problem-rows=0 registry=78'. "
    "The authoritative list of the 68 class members (with every occurrence site) is {class_json}; read it, "
    "do not re-derive it. "
    "Every 'Report:' trailer path is relative to {lane} — write your report at {lane}/<that path>. "
    "Absolute paths are required for every read and write. "
    "You may write ONLY your own report file and your own scratch fixtures. Never edit production files "
    "(SKILL.md, PROVINCE.md, SCORECARD.md, LOG.md, corpus/**), never touch the fleet repo, sibling lanes, "
    "domain trees, the git or jj index or state, never run a mutating git/jj command, never commit, never "
    "push, never delegate, never start a background job. "
    "Scratch: create {scratch}/<your-seat-name>/ yourself and delete it before you yield; /tmp is only for "
    "files under 50 MB; the reaper may delete anything idle for 45 minutes, so copy every receipt you want "
    "to cite into the lane's wave directory or your report. "
    "Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps your item, "
    "reading /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate) and recording "
    "tool/version/channel/reason in your report; pacman stays PAUSED host-wide for this campaign — install "
    "via uv tool, npx or an official binary in ~/.local/bin, or file an L0 question; never run a pacman "
    "transaction, never restart a host service. "
    "Report the exact commands you ran and their observed output; never write an output you did not observe, "
    "and say plainly when a check could not be run."
).format(lane=LANE, fleet=FLEET, claims=CLAIMS, base=BASE, freeze=FREEZE, counter=COUNTER,
         capture=CAPTURE, manifest=MANIFEST, class_json=CLASS_JSON, scratch=SCRATCH)

TEMPLATE = (
    "/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim — let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. "
    "Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. "
    "Act directly via tool calls.\n\n{{item}}"
)

items = []


def add(name, role, item):
    items.append({"name": name, "role": role, "item": item})


# ---------------------------------------------------------------- C1 executors
EXEC_SCOPES = [
    ("R49Exec01", "corpus/README.md lines 1-51 (the coverage-map table)"),
    ("R49Exec02", "corpus/README.md lines 52-197 (Known gaps and Interactive cutover evidence)"),
    ("R49Exec03", "corpus/README.md lines 198-300 (the Frontier table and the round-28/29/30 blocks)"),
    ("R49Exec04", "corpus/README.md lines 301-425 (the round-31..round-38 admission blocks)"),
    ("R49Exec05", "corpus/README.md lines 426-560 (the round-39..round-42 admission blocks)"),
    ("R49Exec06", "corpus/README.md lines 561-702 (the round-43..round-47 blocks)"),
    ("R49Exec07", "corpus/QUALITY.md"),
    ("R49Exec08", "corpus/SOURCES.md"),
    ("R49Exec09", "corpus/knowledge/japanese-domestic-disclosure-workflow.md, corpus/knowledge/vendor-third-party-finding-coordination.md and corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md"),
    ("R49Exec10", "corpus/lessons/round-3.md, round-5.md, round-6.md, round-7.md, round-8.md and round-9.md"),
    ("R49Exec11", "corpus/lessons/round-15.md, round-17-mirror-relocation.md, round-20-recensus.md, round-21-routing-blocked.md, round-23.md and round-26.md"),
    ("R49Exec12", "corpus/lessons/round-28.md, round-29.md, round-31.md, round-34.md, round-35.md and round-38.md"),
    ("R49Exec13", "corpus/instruments/README.md"),
    ("R49Exec14", "corpus/knowledge/considerthese-proposals-ledger.md"),
    ("R49Exec15", "the fleet-relative members only: the PROTOCOL.md / MISSION.md / scripts/ / templates/ / .ufo/state / .ufo/watchdog.log / kake-shokunin / kumitate-shokunin references in corpus/lessons/round-20-recensus.md, round-28.md, round-38.md, corpus/knowledge/root-loss-2026-10-12.md, corpus/SOURCES.md and corpus/QUALITY.md"),
]
for name, scope in EXEC_SCOPES:
    add(name, "executor",
        "C1 ledger rows for {scope}. Read the class-before list at {class_json} and keep only the members "
        "whose occurrences are inside your scope. For each member: read the citing sentence in full, open the "
        "file the repaired path names, and decide whether that file really is the referent the sentence means "
        "(a same-named file elsewhere is NOT the referent). Then write, for every member you keep, one ledger "
        "row exactly in this shape: "
        "| `OLD-TOKEN` | `NEW-TOKEN` | `lane-bare` or `fleet-relative` | `file:line,file:line` | `referent note` | "
        "where OLD-TOKEN is the token as written today, NEW-TOKEN is the full path that opens (for a lane-bare "
        "member: `corpus/<old>` with the line anchor kept; for a fleet-relative member: the absolute fleet "
        "path {fleet}/<old> with the line anchor kept), the sites column lists EVERY occurrence you found for "
        "that token, and the referent note says in one clause why the new path is the same referent. Report "
        "the rows you propose in your report file, each with the file:line you verified the referent at, and "
        "name every member you deliberately refused with the reason (ambiguous referent, wrong referent, "
        "gloss not a path). Do not edit any file.".format(scope=scope, class_json=CLASS_JSON, fleet=FLEET))

add("R49Exec16", "executor",
    "C1 completeness sweep, independent method. Do NOT trust the class-before list: re-derive the class "
    "members of {lane} with your own scan (walk SKILL.md and corpus/**/*.md yourself, extract backticked "
    "tokens, keep the path-like ones, and ask which name a file that exists under {lane}/corpus/ or under "
    "{fleet} but do not open from the lane root). Report every member the frozen list misses, and every member "
    "it lists that you cannot reproduce, each with file:line. A difference is a finding, not an error to "
    "paper over: state which method you trust and why. Do not edit any file.".format(lane=LANE, fleet=FLEET))

# ------------------------------------------------------- C1 mutation-testers
MUTS = [
    ("R49Mut01", "mutate the frozen counter so that a glob token (`corpus/knowledge/*.md`) counts as a class "
     "member, in a scratch copy only, and show that the selftest case `glob-token-is-not-a-class-member` then "
     "fails. Never edit the committed instrument."),
    ("R49Mut02", "mutate a scratch copy of the counter so that an occurrence in a protected file "
     "(corpus/lessons/round-1-verifier-spotcheck.md) counts as an owned member, and show that the selftest "
     "case `protected-occurrence-is-blocked-not-owned` then fails."),
    ("R49Mut03", "mutate a scratch copy of the counter so that the site check compares substrings instead of "
     "whole tokens, and show that the selftest case `repaired-lane-bare-reads-clean` then fails (the old "
     "token `knowledge/entry.md` is a substring of `corpus/knowledge/entry.md`)."),
    ("R49Mut04", "mutate a scratch copy of the counter so that a ledger row whose new path does not exist is "
     "accepted, and show that the selftest case `ledger-row-pointing-at-missing-file-reads-red` then fails."),
    ("R49Mut05", "mutate a scratch copy of the counter so that a ledger row pointing into a lost tree "
     "(~/Projects/bounties/claims/x.md) is accepted, and show that the selftest case "
     "`ledger-row-into-lost-tree-reads-red` then fails."),
    ("R49Mut06", "mutate a scratch copy of the counter so that a ledger row whose old token is still present "
     "at one of its sites is accepted, and show that the selftest case "
     "`ledger-row-with-old-token-still-present-reads-red` then fails."),
    ("R49Mut07", "mutate a scratch copy of the counter so that a ledger row whose new token is absent at its "
     "site is accepted, and show that the selftest case that must catch it fails or is missing; report "
     "precisely which of the ten selftest cases covers that limb and which does not."),
    ("R49Mut08", "mutate a scratch copy of the counter so that the ledger file itself is scanned for class "
     "members, and show the consequence: every ledger row's recorded old token becomes a class member. Report "
     "what the selftest shows and whether any case covers it."),
    ("R49Mut09", "mutate a scratch copy of the counter so that the fleet root is never derived (fleet "
     "relative members never fire), and show that the selftest case "
     "`planted-fleet-relative-reads-red` then fails."),
    ("R49Mut10", "check whether the frozen counter can mutate the tree it measures: run it against a scratch "
     "export of the lane, compare the export's file list, sizes and mtimes before and after, and report "
     "whether anything moved. A counter that writes into the tree it grades is a defect of the counter "
     "(freeze-check's FC-BASE-MUTATED limb)."),
    ("R49Mut11", "build a scratch tree with a fabricated ledger (rows that name files which exist but whose "
     "sites are invented) and show that the counter reads red; then build a scratch tree with a ledger whose "
     "rows are correct but whose class members are still open, and show that it also reads red. Report both "
     "outputs."),
    ("R49Mut12", "check the counter's extraction rule against an independent reimplementation: write your own "
     "backtick-token path-like extractor in your scratch, run it over SKILL.md and corpus/**/*.md, and report "
     "how many class members each method finds and where they disagree. The counter imports resolve.py's rule "
     "so the two cannot drift; your job is to check that the imported rule is the rule the axis census "
     "actually uses."),
]
for name, item in MUTS:
    add(name, "mutation-tester", "C1 counter mutation. " + item + " Scratch: {s}/<your-seat-name>/; delete it "
        "before you yield.".format(s=SCRATCH))

# ------------------------------------------------------------- C1 reviewers
add("R49Rev01", "reviewer",
    "Replay the frozen C1 counter at the base tree: export the base commit {base} with "
    "`git -C {lane} archive {base} | tar -x -C <your scratch>` (git read-only only), then run "
    "`python3 {counter} --root <your scratch> --fleet-root {fleet} --ledger <your scratch>/corpus/instruments/"
    "citation-reground-ledger.md` and report the printed values. They must read unresolved-class=68, "
    "class-lane-bare=57, class-fleet-relative=11, class-total=147, class-protected-blocked=79, ledger-rows=0. "
    "Also re-run `python3 {lane}/corpus/instruments/freeze-check.py --claims {claims} --tool-root {lane} "
    "--base <your scratch> --work <your scratch>/work --timeout 900` and report its verdict. Do not edit any "
    "file.".format(base=BASE, lane=LANE, fleet=FLEET, counter=COUNTER, claims=CLAIMS))

add("R49Rev02", "reviewer",
    "C1 referent audit, batch 1: take the ledger rows whose sites are in corpus/README.md (coverage map, "
    "known gaps, frontier table) from the class-before list at {class_json}; for each row, open the file the "
    "repaired path names and read the citing sentence in full, then state PASS or FAIL per row with the "
    "file:line you read at. A row whose repaired file exists but is NOT what the sentence cites is a FAIL "
    "(referent swap) and must be named as such. Report the rows you judged and the failures with evidence. "
    "Do not edit any file.".format(class_json=CLASS_JSON))

add("R49Rev03", "reviewer",
    "C1 referent audit, batch 2: the same audit over the ledger rows whose sites are in corpus/lessons/"
    "round-{3,5,6,7,8,9,15,17,20,21,23,26}.md. PASS or FAIL per row with the file:line you read at; name "
    "every referent swap. Do not edit any file.")

add("R49Rev04", "reviewer",
    "C1 referent audit, batch 3: the same audit over the ledger rows whose sites are in corpus/lessons/"
    "round-{28,29,31,34,35,38}.md, corpus/QUALITY.md and corpus/SOURCES.md. PASS or FAIL per row with the "
    "file:line you read at; name every referent swap. Do not edit any file.")

add("R49Rev05", "reviewer",
    "C1 referent audit, batch 4: the same audit over the ledger rows whose sites are in corpus/knowledge/"
    "(japanese-domestic-disclosure-workflow.md, vendor-third-party-finding-coordination.md, "
    "chinese-crowdsourced-testing-scope-and-rewards.md), corpus/instruments/README.md and "
    "corpus/knowledge/considerthese-proposals-ledger.md. PASS or FAIL per row with the file:line you read at; "
    "name every referent swap. Do not edit any file.")

add("R49Rev06", "reviewer",
    "C1 site completeness audit: for every member in {class_json}, check that the sites list is complete — "
    "grep the whole lane for the old token and count the occurrences yourself; a site that does not exist or a "
    "missing occurrence is a finding. Report every member whose occurrence count differs from the list, with "
    "the grep command you ran. Do not edit any file.".format(class_json=CLASS_JSON))

add("R49Rev07", "reviewer",
    "C1 axis-metric replay: export the base commit and the current lane HEAD into two scratch trees with "
    "`git -C {lane} archive <rev> | tar -x -C <scratch>` (read-only git), then run "
    "`python3 <tree>/corpus/instruments/resolve.py <tree>` in each and report the three rate lines "
    "(SKILL.md, corpus, lane total) and the class table from both runs. The lane rate must be higher after the "
    "repair and the numerator must not be lower; report the exact numbers and the distinct-citation counts. "
    "Note that resolve.py rewrites corpus/instruments/citation-survival.md inside the tree it measures, which "
    "is why you measure in scratch copies, never in the lane. Do not edit any file.".format(lane=LANE))

add("R49Rev08", "reviewer",
    "C1 referent-swap hunt, independent of the per-row audit: pick the 12 class members whose repaired path "
    "names a file with a common name (PROTOCOL.md, MISSION.md, QUALITY.md, SOURCES.md, README.md, scripts/, "
    "templates/, .ufo/state, the sibling-lane paths) and decide, from the citing sentence alone, which file "
    "the sentence means; then check whether the proposed repair points at that file or at another file with "
    "the same name (for example the canonical protocol checkout "
    "~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md is a different vintage from the fleet "
    "root's PROTOCOL.md). Report each decision and any row whose proposed repair points at the wrong copy. "
    "Do not edit any file.")

add("R49Rev09", "reviewer",
    "C2 capture binding audit: verify the capture {capture} against the manifest {manifest} — digest, byte "
    "count, line count, and each declared quote located at its anchor line — and verify the registry row for "
    "S078 in corpus/SOURCES.md binds to the same URL and capture. Then run "
    "`python3 {lane}/corpus/instruments/source-recheck.py --manifest {manifest} --source S078` and "
    "`python3 {lane}/corpus/instruments/capture-binding-check.py --root {lane}` and report their exits and "
    "outputs. A quote that is not located at its anchor is a FAIL and must be named.".format(
        capture=CAPTURE, manifest=MANIFEST, lane=LANE))

add("R49Rev10", "reviewer",
    "C2 novelty audit: read the 29 admitted frontier rows of {lane}/corpus/README.md and the F25 and F07 "
    "knowledge entries (corpus/knowledge/cve-json-record-format.md, "
    "corpus/knowledge/cna-assignment-and-vulnerability-rules.md), then decide whether the proposed F30 surface "
    "(the CVE Services API publication endpoints) is a NEW surface or a duplicate of an admitted row. Argue "
    "both sides from the admitted rows' own text, then give your verdict with the rows you compared. A "
    "duplicate verdict means C2 fails and must be reported, not argued away. Do not edit any file.".format(
        lane=LANE))

add("R49Rev11", "reviewer",
    "Freeze integrity audit: confirm that the committed bytes of {counter} still hash to the digest recorded "
    "in {lane}/.ufo/waves/round-49/freeze.txt, that {claims} still hashes to its recorded digest, and that "
    "neither file was changed after the freeze commit {freeze} (compare `git -C {lane} show {freeze}:<path>` "
    "with the working tree). Also confirm the do-nothing control receipt at "
    "{lane}/.ufo/waves/round-49/controls/do-nothing.txt prints the declared before-values. Report every "
    "mismatch. Do not edit any file.".format(counter=COUNTER, lane=LANE, claims=CLAIMS, freeze=FREEZE))

add("R49Rev12", "reviewer",
    "C1 claim-honesty audit: read {claims} (C1) and the frozen counter, then answer these with evidence: does "
    "the counter's verdict depend on anything a do-nothing tree could satisfy; is any before-value quoted in "
    "the claim a value the claim's own counter prints; is the 'protected-file residue' exclusion a scope dodge "
    "or a real write-scope limit; and does the claim text promise a rate move the counter cannot deliver. "
    "Report each answer with the command or file:line you checked. Do not edit any file.".format(claims=CLAIMS))

add("R49Rev13", "reviewer",
    "C2 entry audit: read the round-49 knowledge entry for the CVE Services surface and its coverage-map and "
    "frontier rows, and check every factual sentence against the captured bytes {capture} — each quoted "
    "fragment must occur at the cited line, and each paraphrase must be supported by the text. Report every "
    "sentence you could not support, with the line you expected it at. Do not edit any file.".format(
        capture=CAPTURE))

add("R49Rev14", "reviewer",
    "L2 floor and role-mix audit: check the wave-1 dispatch file at {lane}/.ufo/waves/round-49/wave1-dispatch.json "
    "against the round contract — one wave, seat count, role counts, and the attack share (reviewer + critic + "
    "mutation-tester + labrat seats over the total). Report the counts you derived and whether the contract's "
    "minimum role split is met (the validator rejects `planner`, so the L1 holds the planner seat — say whether "
    "the dispatch reflects that). Do not edit any file.".format(lane=LANE))

# --------------------------------------------------------------- C1 critics
CRITICS = [
    ("R49Crit01", "Falsify C1: construct a tree where the frozen counter reads clean (unresolved-class=0, "
     "findings=0) while a citation in the lane is still unopenable by the reader — for example a citation "
     "whose repaired path resolves but whose line anchor is past EOF, or a citation written in a form the "
     "extractor never sees (a plain-text path outside backticks), or a ledger row whose new token is present "
     "at its site but in a comment. Report whether you succeeded and, if you did, whether the claim as frozen "
     "is still true. Do not edit any file."),
    ("R49Crit02", "Falsify C2: argue that the proposed F30 surface duplicates an admitted row (the round-47 "
     "ZDI precedent rejected a row because it duplicated F02's discipline), or that the captured OpenAPI file "
     "is an application shell rather than the document's content, or that the entry would claim a workflow the "
     "spec does not state. Read the admitted rows' own text and the capture before arguing. Report your "
     "verdict with evidence. Do not edit any file."),
    ("R49Crit03", "Attack the claim sizing: is the frozen C1 target (68 members, 0 remaining) reachable by a "
     "do-nothing baseline? Build the cheapest control that skips the claimed work — apply nothing but the "
     "ledger file — score it with the frozen counter, and report the score. If a do-nothing tree can satisfy "
     "the predicate, say so with the command output; that voids the claim as frozen. Do not edit any file."),
    ("R49Crit04", "Attack the round's honesty: which of the three trend verdicts (expansion, quality, "
     "discernment) would be wrong if C1 and C2 both land, and which claim in this round could turn out to be a "
     "trade rather than an improvement? Name the specific evidence that would be needed for each verdict and "
     "the specific observation that would flip it. Do not edit any file."),
    ("R49Crit05", "Attack the scope exclusion: 79 class members sit in protected files (round-*-verifier-"
     "spotcheck.md, round-*-aggregator-*.md). Decide whether excluding them from the frozen target is the "
     "protocol's write-scope limit or a dodge, using the protocol text in "
     "~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md and the round prompt's inherited-state "
     "rule. Report your verdict and what a reader would still be unable to open after this round. Do not "
     "edit any file."),
]
for name, item in CRITICS:
    add(name, "critic", item)

# ------------------------------------------------------------- C2 connectors
CONNECTORS = [
    ("R49Conn01", "Cross-claim overlap scan: C1 re-grounds citations and C2 adds a knowledge entry, a "
     "registry row, a manifest and frontier text. Find every place where the two collide — a new C2 citation "
     "that C1 would have to repair, a C1 repair that would touch a file C2 writes, an id or filename used by "
     "both (the manifest id S078, the snapshot path corpus/source-snapshots/round-49/, the entry slug). Report "
     "each collision and its resolution order. Do not edit any file."),
    ("R49Conn02", "Cross-lane pattern finding: look at how the sibling lanes under {fleet} record citation "
     "bases and repair logs (for example kake-shokunin, kumitate-shokunin, kotoba-shokunin, kengaku-shokunin, "
     "mori-shokunin) and report the pattern the kasegi lane's new ledger and counter should follow or "
     "deliberately differ from, with one file:line per sibling. Report only what you actually read. Do not "
     "edit any file."),
    ("R49Conn03", "Cross-surface pattern finding inside the lane: find every place the lane already records a "
     "citation-repair decision (corpus/knowledge/citation-bases.md, the round-12 and round-13 citation audits "
     "recorded in corpus/README.md, corpus/lessons/round-{12,13,18,19,20}.md) and report the pattern the new "
     "ledger must honour to stay consistent with them — naming the file:line of each precedent. Do not edit "
     "any file."),
]
for name, item in CONNECTORS:
    add(name, "connector", item)

# ---------------------------------------------------------------- C2 scouts
SCOUTS = [
    ("R49Scout01", "Independent reconnaissance of the class members: pick the 20 members you consider the "
     "riskiest repairs (ambiguous referents, common file names, tokens with many occurrences) and report, for "
     "each, the sentence that cites it, the file the repair would point at, and your judgement whether the "
     "sentence means that file. Prioritise the fleet-relative ones. Do not edit any file."),
    ("R49Scout02", "Protected-file residue dossier: for the 79 class members the counter reports as blocked "
     "by protected files, group them by file and count them with one command, and report the per-file counts "
     "plus the three largest groups. This dossier is the operator-facing note for the next round; write it as "
     "a table you can paste, not as prose. Do not edit any file."),
    ("R49Scout03", "Frontier lead screen for the NEXT round (no admission): screen three candidate surfaces "
     "for the lane's frontier that are not F01-F30 — for example a first-party bug-bounty platform's "
     "researcher-side report and dispute flow, a second CNA's publication interface, or a national CERT's "
     "disclosure-intake service. For each: the URL, whether the fetch returns the document's content or an "
     "application shell (show the extracted text length and a located fragment), the tier it would carry and "
     "the admitted row it would duplicate, if any. Open nothing that is not public. Do not admit anything and "
     "do not edit any file."),
    ("R49Scout04", "Mistake mining sweep for the round lesson: search the lane's lessons and the fleet's "
     "round-47/48 verification files for a mistake class that this round's work touches — especially anything "
     "about citation bases, relative paths, false-green counters, do-nothing controls, or quotes that were "
     "counted by hand rather than measured. Report the best two candidates with their file:line and the rule "
     "that should have caught them; paste the grep commands you ran. Do not edit any file."),
    ("R49Scout05", "Search-log sweep: read the Search log section of {lane}/corpus/SOURCES.md and report what "
     "the lane searched, what it included and excluded, and which query of THIS round (the CVE Services API "
     "capture, the citation-base audit) is missing from it. Give the exact prose bullet the lane should append, "
     "with the counts you can support. Do not edit any file.".format(lane=LANE)),
]
for name, item in SCOUTS:
    add(name, "scout", item)

# ---------------------------------------------------------------- C2 scribes
SCRIBES = [
    ("R49Write01", "Draft the SOURCES.md registry row for S078 (the CVE Services API OpenAPI capture). Use the "
     "shape of the existing rows in {lane}/corpus/SOURCES.md: id, source title + canonical URL, kind, tier, "
     "scope, anchor (the capture path plus the line ranges you cite), teaches, status, opened, recheck, "
     "used-by. The anchor must name the capture file and the lines you actually read; the teaches cell must "
     "state one grounded learner benefit, not a summary of the document. Give the row as text plus the list of "
     "quote ids and their anchor lines you used. Do not edit any file.".format(lane=LANE)),
    ("R49Write02", "Draft the knowledge entry for the CVE Services publication surface. The entry must open "
     "with the provenance trio (source:, verified-at:, recheck: — the recheck line must be a "
     "`source-recheck.py --manifest corpus/source-snapshots/round-49/manifest.json --source S078` invocation "
     "that the frontier counter can run), then a scope and decision rule paragraph, then a question/ground "
     "table whose every quoted fragment is located at a line of the capture {capture}, then an overlap and "
     "novelty section that states what F25 (the CVE record format) and F07 (the CNA rules) hold and what this "
     "entry holds instead. Quote only text you can locate in the capture. Give the draft as text. Do not edit "
     "any file.".format(capture=CAPTURE)),
    ("R49Write03", "Draft the three README/PROVINCE edits the round needs, as text, in the lane's append-only "
     "style (never edit a line in place; append an end-of-file block that names what it appends): (a) the "
     "coverage-map row for the new entry, (b) the Frontier row for F30 in the six-cell frontier table shape, "
     "with a `next` cell that says how to read the surface rather than what it is, (c) the PROVINCE.md frontier "
     "amendment sentence naming F30 and its entry path. Copy the wording style of the round-46/47 rows you can "
     "read in {lane}/corpus/README.md. Give the three blocks as text. Do not edit any file.".format(lane=LANE)),
    ("R49Write04", "Draft the round-49 lesson file (corpus/lessons/round-49.md): a `## Gate` section (the "
     "candidates considered, the admitted, the rejected with reasons, the spot-check result) and a `## "
     "Mistakes` section (one row per mistake: class, evidence pointer, captured-by, fix), following the shape "
     "of corpus/lessons/round-48.md. Ground every claim in a file:line or a command output that exists. Name "
     "the two candidate mistakes your own sweep found (from R49Scout04's report if it is available; otherwise "
     "your own). Give the draft as text. Do not edit any file."),
]
for name, item in SCRIBES:
    add(name, "scribe", item)

# ----------------------------------------------------------------- sentinel
add("R49Sent01", "sentinel",
    "Provenance and scope review of everything this round proposes to write: the ledger rows (no secret, "
    "session token, cookie or `op://` reference anywhere — corpus/QUALITY.md's credential rule), the S078 "
    "capture and manifest (no credential material in the captured bytes; the manifest's url, digest and "
    "fetched_utc must match the bytes on disk), the knowledge entry (no quote that is not located in the "
    "capture; no sentence that asserts a workflow the spec does not state), and the lesson (no claim without a "
    "pointer). Read the capture {capture} for anything that must not be copied into the corpus (a key, a "
    "token, an internal hostname). Report every finding with the file:line.".format(capture=CAPTURE))

# ------------------------------------------------------------------- labrats
add("R49Lab01", "executor",
    "Labrat-role probe (a bounded falsifiable probe; the wave validator has no labrat role, so this seat is an executor running one): build a scratch copy of the lane tree (use `git -C {lane} archive <rev> | tar -x -C "
    "<scratch>` — read-only git), plant one unresolvable class member in it (a backticked "
    "`knowledge/<a file that does not exist>.md` citation in corpus/README.md), run the frozen counter "
    "`python3 <scratch>/corpus/instruments/citation-ground-check.py --root <scratch> --fleet-root {fleet}` — "
    "copy the instrument into the scratch tree first — and report the printed values and the exit code. The "
    "probe succeeds when the counter reads the planted member as a class member (unresolved-class increases by "
    "1 and the finding names the planted token). Report the exact output; delete your scratch when done."
    .format(lane=LANE, fleet=FLEET))

add("R49Lab02", "executor",
    "Labrat-role probe (bounded falsifiable probe; the wave validator has no labrat role, so this seat is an executor running one) on the counter's honest limit: build a scratch tree in which one ledger row points at a "
    "file that EXISTS but is not the referent the citing sentence means (a different file with the same name "
    "elsewhere, or a file whose content does not support the sentence). Run the frozen counter and report what "
    "it reads. The probe succeeds when the counter reads GREEN on that tree: that is the documented mechanical "
    "limit of the counter (it grades path resolvability, not referent truth), and your report is the evidence "
    "the round's report must disclose. Also state what a non-mechanical check would have to do to catch it. "
    "Do not edit any file.")

# ------------------------------------------------------------------ revenger
add("R49Rev15", "revenger",
    "Recover the intent behind the repair: find where the lane's LANE citation-base rule came from "
    "(corpus/knowledge/citation-bases.md and the round-16/18 lessons), what it was written to prevent, and "
    "whether any earlier round already attempted to re-ground bare citations and abandoned it. Search "
    "corpus/lessons/*.md, corpus/README.md and LOG.md for the earlier attempt (terms: bare cite, lane root, "
    "GONE, relative path, re-ground, citation base). Report what the earlier round found, what it did not try, "
    "and the one constraint the original rule states that a repair must respect. Paste the grep commands. Do "
    "not edit any file.")

# ---------------------------------------------------------------- simplifier
add("R49Simp01", "simplifier",
    "YAGNI review of the two artifacts this round adds to the lane: the frozen counter "
    "corpus/instruments/citation-ground-check.py and the ledger shape "
    "corpus/instruments/citation-reground-ledger.md. For each, name the parts that carry no verdict (unused "
    "options, dead branches, redundant fields, a column nobody reads) and say what a reader of the round "
    "report would lose if it were deleted. Do not propose deleting a self-test case or a kill-rule limb. Do "
    "not edit any file.")

spec = {
    "wave": "kasegi-r49-citation-ground-and-cve-services",
    "reportDir": WAVE_DIR,
    "maxLanes": 128,
    "axes": ["depth:verifiability", "coverage"],
    "milestone": "One frozen citation-grounding repair (68 members to 0) and one frozen frontier admission "
                 "(F30, the CVE Services publication surface), attacked by 33 review/critic/mutation/labrat "
                 "seats",
    "context": CONTEXT,
    "template": TEMPLATE,
    "items": items,
}

out = os.path.join(LANE, ".ufo/waves/round-49/wave1-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
roles = {}
for it in items:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("wrote", out, "items", len(items))
print("roles", roles)
attack = sum(roles.get(r, 0) for r in ("reviewer", "critic", "mutation-tester", "labrat"))
print("attack seats", attack, "share %.1f%%" % (100.0 * attack / len(items)))
