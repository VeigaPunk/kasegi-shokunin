#!/usr/bin/env python3
"""Builds .ufo/waves/round-46/attempt2/wave2-spec.json (34 seats, policy v1). Falsify wave: attacks the integrated tree."""
import json
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = L + "/.ufo/waves/round-46/attempt2"
INTEG = "AT-INTEGRATION"       # patched by the L1 before validation
FREEZE = "AT-FREEZE"
BASE = "04af9bc92229232ea5cce8b32bfe59dd969eb26d"
PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure2"
SNAP = L + "/corpus/source-snapshots/round-46-a2/S074.txt"
MAN = L + "/corpus/source-snapshots/round-46-a2/manifest.json"
GATE = L + "/corpus/instruments/r46-f29-gate.py"
MUTBAT = L + "/corpus/instruments/r46-mutbat.py"
ST1 = L + "/corpus/instruments/r46-counters-selftest-c1.py"
ST2 = L + "/corpus/instruments/r46-counters-selftest-c2.py"
STF = L + "/corpus/instruments/r46-selftest-f29.py"
CLAIMS = W + "/claims.json"
BATTERY_BEFORE = W + "/controls/mutbat-before.txt"

context = (
    "Round 46 (attempt 2) kasegi FALSIFY wave — the tree under attack is lane commit " + INTEG + " (integration of wave 1). Frozen claims: " + CLAIMS +
    " (freeze " + FREEZE + ", base " + BASE + "; before-value receipt " + BATTERY_BEFORE + "; R50 receipt " + W + "/controls/f29-r50-receipt.txt). "
    "Every item names what it attacks. Re-run, do not trust: every counting command in the claims file, the battery, the selftests, the entry's quotes against " + SNAP + " and the live page, and every new instrument. "
    "The L1 holds the planner seat and the only writer role; seats return findings (and scratch-built counterexample trees as recipes), never commits. Read-only seats edit nothing. "
    "Every `Report:` trailer path is relative to " + L + " — write it at " + L + "/<that path>. Absolute paths only under " + L + ". "
    "Never commit/push/mutate git-jj-index anywhere; never touch the fleet repo, sibling lanes, MANIFEST.json, .ufo/state, ~/Projects/shokuknow (read-only ok). "
    "Scratch: $HYAKU_SCRATCH/kasegi-r46/<YourSeatName>/ (default /fast/scratch/hyaku; mkdir -p; explicit TMPDIR; /tmp < 50 MB only); exports via `git -C " + L + " archive <rev> <paths> | tar -x -C <scratch>`; "
    "delete your scratch before yielding (trap rm -rf); a /tmp path is never citable evidence. "
    "Tooling authorization (operator, 2026-10-19) applies; read /home/vgpnk/.omp/agent/RULES.md first; pacman PAUSED (uv/npx/official binary only). "
    "No credentials, no live-target testing. Report format: first line `VERDICT: <HOLDS|BROKEN|DRAFT-READY|BLOCKED|INFO>`; findings each naming the exact artifact attacked, the command, the quoted output; then limitations. "
    "An unrun check has not passed."
)
template = (
    "/skill:godspeed\n\nYou are a leaf lane in kasegi round 46 attempt 2 wave 2; no delegation or background work (an executor may spawn one read-only labrat probe). "
    "Your single item: {{item}}. Attack what the item names; discriminate against a do-nothing control; quote exact outputs. "
    "Do not commit, push, mutate git/jj/index, or touch shared production files. Remove scratch on exit. Return concise structured findings."
)

items = []


def add(name, role, item):
    items.append({"name": "R46bW2" + name, "role": role, "item": item})


# re-run every counting command (3 executors)
add("ExecRerunC1", "executor",
    "re-run the C1 counting chain at " + INTEG + " vs base " + BASE + " exports (git archive both): `python3 " + MUTBAT + " --root <integ export> --pure " + PURE + " --work <scratch> --counter c1 --jobs 8` (expect uncaught=0), the c2 twin (expect uncaught=0), the extended " + ST1 + " and " + ST2 + " baselines (expect failures=0 at the integration tree), and the plain lines: `grep -cE '^\\| F[0-9]+ \\|'`, SOURCES rows, knowledge files, absence sweep. Quote every line; any value off the claim's after-state is BROKEN.")
add("ExecRerunC2", "executor",
    "re-run the C2 counting chain at the integration export: `python3 " + GATE + " --root <integ>` (expect 7/7), `python3 " + L + "/corpus/instruments/r44-frontier-count.py --root <integ> --expect 29`, `python3 " + L + "/corpus/instruments/source-recheck.py --manifest " + MAN + " --source S074` (expect exit 0), `python3 " + L + "/corpus/instruments/capture-binding-check.py --root <integ>` (expect unbound=0), census `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <integ>/corpus/SOURCES.md` (exit 0), and the prior-attempt instruments on the SAME export: " + L + "/corpus/instruments/r46-c1-gate.py --root <integ> --baseline <base export> (expect 7/7) and r46-c2-gate.py --root <integ> (expect 7/7 — its v1.3 amendment if landed). Quote every line.")
add("ExecRerunLive", "executor",
    "re-run the selftest/battery suite on the LIVE lane (not an export): " + ST1 + " --pure " + PURE + " --work <scratch> --jobs 8; " + ST2 + " --pure " + PURE + "; " + STF + " if landed; `python3 " + MUTBAT + " --root " + L + " --pure " + PURE + " --work <scratch> --counter both --jobs 8 | grep mutbat`; `python3 " + GATE + " --root " + L + "`. Expect the claim after-values. Then the export-vs-live delta: any value that differs between the integration export and the live tree is a finding (uncommitted drift).")
# source re-open (1 scout)
add("ScoutS074Live", "scout",
    "re-open https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories live (record HTTP status + final URL), then locate every quoted span of the LANDED entry " + L + "/corpus/knowledge/github-repository-security-advisories.md in the LIVE page (normalise whitespace; the pinned capture " + SNAP + " is the fallback): report any quote the live page no longer holds (drift = BROKEN for C2's kill rule), and any entry statement the page does not support (overclaim = M46-3 class).")
# entry + registry attacks (4 reviewers)
add("RevEntryClaims", "reviewer", "attack the landed entry " + L + "/corpus/knowledge/github-repository-security-advisories.md against " + SNAP + " line by line: every quote located (<= 25 words, range holds it); every claimed contrast with F28/F07 actually stated by the sources; the decision rule actionable; Limits honest about the sibling pages. One finding per defect with entry line + capture line.")
add("RevRegistryText", "reviewer", "attack the registry surface: the S074 row in " + L + "/corpus/SOURCES.md (11 cells, tier/kind/status/opened/recheck/used-by/anchor correct vs " + MAN + "), the README admission block (row shape, status third cell, 29/29 count line), the PROVINCE F29 line (scope limit present), knowledge-expected.txt (+1), the instruments README + SKILL.md registry rows (commands actually run). Quote each defect.")
add("RevClaimC1", "reviewer", "attack the C1 verdict end-to-end: replay " + BATTERY_BEFORE + " (before) against the integration values; audit the equivalence entries used for the formerly-uncaught mutants (read the committed proof map; falsify one proof by constructing the input class it claims impossible — if any constructible input flips a verdict under the mutant, the equivalence is false and C1 is BROKEN).")
add("RevClaimC2", "reviewer", "attack the C2 verdict: the frontier row admits F29 with status third-cell; the entry cites five frozen cores inside located live spans (re-locate each yourself); the census exits 0; the claim's after-values hold; the target (29/66) was not narrowed post-freeze (diff " + CLAIMS + " against the freeze commit). Any gap = BROKEN.")
# mutation-testers (8)
add("MutGate1", "mutation-tester", "single-edit mutants (>= 10, your own, not the R50 set) of " + GATE + " against the landed tree export: every mutant that keeps the marker must flip the gate red on the LANDED tree (the landed tree is a positive). Survivors = false-green class = finding with recipe.")
add("MutGate2", "mutation-tester", "independent: >= 10 further own mutants of " + GATE + " (target H4/H5/H6 — the quote and pin machinery: tolerance windows, span limits, word counts, anchor parsing). Report survivors.")
add("MutSelfF29", "mutation-tester", "mutation-test the landed " + STF + ": for >= 8 of its cases, remove or invert the case's core assertion in a scratch copy — the selftest must then report failures>0 (a case that cannot fail is dead weight masking a limb). Report per-case.")
add("MutSelfC1", "mutation-tester", "run the landed battery --counter c1 against the landed tree; then verify each formerly-uncaught mutant is now caught: for M06,M07,M08,M11,M12,M13,M14,M17,M18,M19 quote the extended selftest's per-mutant failure lines (or the equivalence proof ids). Any mutant still failures=0 without an equivalence id = C1 BROKEN.")
add("MutSelfC2", "mutation-tester", "same for --counter c2's formerly-uncaught set (read " + BATTERY_BEFORE + " for the uncaught list): quote the extended selftest's lines proving each is now caught or equivalence-proven.")
add("MutBattery2", "mutation-tester", "verify the battery v1.1's f29 mode end-to-end: run `python3 " + MUTBAT + " --root <integ export> --pure " + PURE + " --work <scratch> --counter f29` and reconcile its per-mutant lines against the R50 receipt " + W + "/controls/f29-r50-receipt.txt (11 flips must read caught; the 9 disclosed must read equivalent-or-caught after the selftest landed). Mismatch = finding.")
add("MutLanding", "mutation-tester", "mutation-test the landing gate " + L + "/corpus/instruments/r46-landing-gate.py (or its attempt-2 successor): >= 6 single-edit mutants (drop the cleanliness check, drop the ls-remote equality, accept two SHONEN headings) — each must flip the gate red on a fixture pair built in scratch (D=$(mktemp -d -p $SCRATCH) && git -C \"$D\" init -q; never elsewhere). Report per-mutant.")
add("MutPinAmend", "mutation-tester", "if the r46-c2-gate.py v1.3 ledger exemption landed: verify with mutants — a shrunk ledger, a stubbed ledger, a swapped-name ledger must each still turn G6 red (name-pinned non-shrink holds), AND the v1.2 bytes at eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7 still read 7/7 on their era export (history intact). If v1.3 did not land, verify the ledger row was NOT appended (G6 green at the tip) and say which deferral the report must carry.")
# critics (6)
add("CritVerdictC1", "critic", "final C1 audit: is the after-value the value the committed receipts print (re-derive ONE of them yourself)? Is the axis named by the surface the round changed (instrument soundness = depth:verifiability, not coverage)? Could a do-nothing control have reached uncaught=0 (the before-value receipt says otherwise — check its base replay is honest)? Name the weakest link in the chain freeze->before->after.")
add("CritVerdictC2", "critic", "final C2 audit: name the surface moved (a new source class on the lane's frontier — maintainer-side advisory lifecycle) and the command that would show it unmoved at the base. Re-run the absence sweep at both exports. Is any admission limb satisfied only by the L1's own reading (unverified by machine or seat)? Name it.")
add("CritNovelty2", "critic", "re-run the novelty test on the LANDED corpus: name >= 8 practitioner questions the corpus now answers that it could not at " + BASE + " (git -C " + L + " grep at both revisions). Fewer than 8 = the frontier move is thin — say so.")
add("CritCalib2", "critic", "calibration re-scan at the integration tree: SCORECARD/SHONEN/LOG self-assessment cells vs the observed state (run the cheap commands). Name mismatches with path:line; include the round's own new rows.")
add("CritScope", "critic", "province-fit audit: the landed F29 ground vs " + L + "/PROVINCE.md (bounty/security research, program rules, claim packages); the reporter/maintainer boundary vs F28's scope-out sentence; the CNA boundary vs F07; live-target testing absent (documentation only). Any bleed or absorbed sibling ground = finding.")
add("CritErrata2", "critic", "errata audit: every counter/instrument change this round (mutbat v1.1, selftest extensions, any v1.3 gate amendment) must be logged as errata with a plain re-derivation that does not use the changed instrument (read " + L + "/.ufo/waves/round-46/attempt2/ counter-errata file when landed). Is the claims.json byte-identical to the freeze? (`diff <(git -C " + L + " show " + FREEZE + ":.ufo/waves/round-46/attempt2/claims.json) " + CLAIMS + "`). Name any unlogged change.")
# sentinel / revenger / connector / simplifier / scout-exec (4)
add("SentFinal", "sentinel", "final integrity pass on the landed tree: every new instrument read-only on its --root; no tree-supplied execution outside the allow-listed shapes; no hardcoded scratch paths in committed files (grep corpus/instruments for /fast/ and /tmp/ — the two known dead PURE defaults must be fixed or named as errata); no credentials/session material in the wave dir.")
add("RevengerW2", "revenger", "rebuild the prior attempt's wave-2 attacks against the landed tree: from " + L + "/.ufo/waves/round-46/wave2/R46W2MutSelftestC1.md take probes P1/P2/P3 recipes and re-run them against the LANDED counter+entry state — the counter must still reject each (the entries' anchors are the same bytes). Any acceptance = regression.")
add("ConnW2", "connector", "cross-seat scan (run LAST): read " + W + "/wave2/*.md reports; name (1) findings confirmed by >= 2 seats, (2) contradictions, (3) the three findings the L1 must fix before the report, ranked. Quote seat + line.")
add("SimplW2", "simplifier", "dead-weight pass over the landed instruments: duplicated logic between " + STF + " and the fixture builders, unreachable branches added by the extensions, docstring drift. Findings only, with identical-behavior arguments.")
add("RevSelftestW2", "reviewer", "diff-audit the extended selftests at the integration tree vs their committed drafts (" + W + "/wave1/R46bExecSelftestC1.draft/, R46bExecSelftestC2.draft/ when present): every case the L1 changed or dropped during integration is a finding unless the accompanying receipt shows it failing identically; run the extended baselines once more and quote the tallies.")
add("RevLessonGate", "reviewer", "attack the lesson's Gate block (corpus/lessons/round-46.md attempt-2 section, if landed): every <= 25-word quote must sit on its manifest anchor line in " + MAN + " and in " + SNAP + " (`sed -n 'Np'`); every reject/flip entry must carry a reason + flip condition; the admit must cite S074 with the pinned sha. Quote each defect.")
add("ScoutCensusPair", "scout", "re-run the census pair and the registry guards: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` now (expect exit 0; compare against " + W + "/controls/sources-census-before.txt — same three W04 warnings plus any new one, which must be explained: does S074 share a URL with a held row?), the SOURCES row-shape guards the census does not check (11 cells, no escaped pipes) on the S074 row, and the registry Search-log/Registry-changes bullets' counts against the real sweeps.")
add("MutPlain", "mutation-tester", "mutation-test the plain-measure script " + W + "/wave1/R46bExecPlain.draft/plain-measure2.sh (or its landed successor): >= 5 single-edit mutants (drop the absence sweep, count knowledge files recursively, unquote a grep) — each must change a printed value on the landed tree so a verifier can detect the tampering. Report per-mutant.")
add("MutNoHarm", "mutation-tester", "mutation-test the no-harm script " + W + "/wave1/R46bExecNoharm.draft/noharm.sh: >= 4 mutants (drop the numstat exclusion inversion so wave files hide, drop the density line, mis-set the base rev) — each must be detectable in its output (a wrong base rev prints a diff the receipt's base hash contradicts). Report per-mutant.")
add("CritHonestStop", "critic", "honest-stop audit of the round's claims: for every limb of both claims, name the check that verifies it and WHO ran it (L1, seat, or nobody). Any limb whose only support is an unrun check or a placeholder = the honest-stop list the report must carry. Read the claims file, the wave receipts, and the integration commit; quote the gap per limb or state none.")

for it in items:
    it["axes"] = ["depth:verifiability"] if any(k in it["name"] for k in ("C1", "SelfC1", "SelfF29", "Battery", "Landing", "PinAmend", "Errata")) else ["coverage"]
    it["milestone"] = "one wave item, spec in task text"

spec = {
    "reportDir": ".ufo/waves/round-46/attempt2/wave2",
    "context": context,
    "template": template,
    "items": items,
}
roles = Counter(i["role"] for i in items)
attack = sum(v for k, v in roles.items() if k in ("reviewer", "critic", "mutation-tester"))
print(json.dumps(dict(roles), sort_keys=True))
print("seats=%d attack=%d (%.1f%%)" % (len(items), attack, 100.0 * attack / len(items)))
out = W + "/wave2-spec.json"
json.dump(spec, open(out, "w", encoding="utf-8"), indent=1)
print("wrote", out)
