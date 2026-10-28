#!/usr/bin/env python3
"""Build wave-2 (falsify) spec for kasegi round 42. Emits .ufo/waves/round-42/wave2-spec.json.
Run AFTER wave-1 integration: fills J/Y into the context."""
import json, os, sys

R = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = ".ufo/waves/round-42"
J = sys.argv[1] if len(sys.argv) > 1 else "<J-hash>"
Y = sys.argv[2] if len(sys.argv) > 2 else "<Y-hash>"

CTX = f"""# Round
kasegi-shokunin round 42 FALSIFY wave, dispatched by the L1 (agent KasegiR42) via the inline spawn handoff (hyaku run 10). Lane repo /home/vgpnk/Projects/shokunin/kasegi-shokunin is the ONLY lane repo. The fleet root /home/vgpnk/Projects/shokunin is read-only to you — never write there. /home/vgpnk/Projects/shokuknow is read-only — never write there, never run its campaign tools. Base commit 5053a7f46de35784cff4b56756906e9014a38276; frozen claims at /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/claims.json (read first; do not edit). Wave 1 (build) has landed; judged head J = {J}; verification ref Y = {Y} (J + receipt only).

Frozen claims (summary; claims.json is authoritative):
- C1 depth:verifiability (4 held): corpus/instruments/r42-closure.sh export-mode only; at Y prints closed=13/13 exit=0 with J1-J13 payload lines; --selftest --export-ref Y prints thirteen graded `selftest case=J<n> ... verdict=pass` lines + `selftest cases=13 failures=0`; base and r41 judged head exports print closed<13/13 exit=1; plain run exit 2; unresolvable ref = distinct ref-not-found red. Kill rule: any committed artifact at Z shows the CURRENT suite bytes accepting an input within one of the seven named repair families F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP; receipt must be the teed transcript of one observed run+selftest at its named ref.
- C2 coverage (8 held): F25 admitted 24->25; S064 mined + >=1 rejected screened row; capture + manifest record + entry with provenance trio; harness entries=28 pass=28 incl PASS F25; binding 56/56; audit expected=61; census exit 0; measure 45/45 = 1.000.

Your job is falsification, not repair: attack the frozen predicates, replay every committed defeat, re-run every counting command on the integrated tree, and report FIRES / DEFENDED / ROUTED per item. Read your item fully before acting. Leaf seat — no subagent spawning. No placeholders: report commands you ran with their actual output.

Write scope. Your ONLY writes are your receipt + deliverable files under /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/wave2/<SEATNAME>.<suffix>. Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin. Never edit any other file anywhere; never run a mutating git/jj command.

Scratch. S=/fast/scratch/hyaku/kasegi-r42/<SEATNAME>/; mkdir -p; bind TMPDIR=$S and every --work dir there; remove the dir before you yield (trap/finally). Disk guard before heavy passes: bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status.

Tooling. You may install/upgrade tools that help (official channels only, read /home/vgpnk/.omp/agent/RULES.md first; record tool/version/channel/reason). pacman is PAUSED host-wide — never run it. Network fetches: curl -sS -L --max-time 90 -A kasegi-shokunin/1.0; record status/bytes/UTC.

Rules. Keep moves that improve an axis and harm none. No agent://all. No own swarms. A finding that names what it attacks is evidence; a finding without a reproducer is a note, not a defeat.
"""

def it(name, role, prompt):
    directive = "You are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n4. **Don't aim — let the frontier walk itself.**\n\n## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + directive + "\n\n" + prompt}

CJ = "Read /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42/claims.json first (frozen claims; do not edit). "
W42 = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-42"

items = [
it("RevC1Counters","reviewer",
   CJ+f"Re-run every frozen C1 counting command at Y={Y}: suite run (closed=13/13 exit=0), graded selftest (cases=13 failures=0, thirteen case lines), base export red, r41 judged head 1f7464612ac4c44e39886b82e812610d3c039b13 red, plain run exit 2, unresolvable ref distinct red. Private --work/--scratch-root inside your scratch. File `RevC1Counters.md` with full transcripts."),
it("CritC1KillRule","critic",
   CJ+"Attack the C1 kill rule against the LANDED tree: replay EVERY committed r41 defeat artifact (wave1 seat ScoutDefeatsR41 catalog + "+W42+"/wave1 receipts): the I1 union-evidence mutant, I3 closed=10/100 token mutant, MutSkillTablePipes variants, CritDeclarationCoverage probes, MutScratchTiming outside-root stray, capture-binding missing-path/URL variants, frontier status-flip probe. Each replay MUST be against the CURRENT committed suite — a green acceptance inside a named family KILLS C1. File `CritC1KillRule.md` per-artifact verdicts."),
it("MutSuite","mutation-tester",
   CJ+"Mutation-test the landed r42 suite: at least 12 byte-level mutants across J1-J13 limbs (weakened regex -> substring, dropped per-record guard, literal-prefix-only scan, fence blindness, missing-path acceptance, silent row-drop, union aggregation). Each mutant applied to a scratch copy, executed, verdict: detected (selftest red) / survives (kill). File `MutSuite.md` + `MutSuite.findings.txt`."),
it("RevReceipt","reviewer",
   CJ+f"Verify the receipt at Y={Y}: (1) byte-identical to a freshly teed run at the same ref (reproduce in scratch, diff); (2) run-utc equals the ref committer instant (git show -s --format=%cI {J}) and time-basis=ref-commit; (3) carries BOTH run payload lines and selftest case lines; (4) recorded payload values equal re-derived values (forgery check). File `RevReceipt.md`."),
it("CritC2Live","critic",
   CJ+"Re-open S064 live: fetch the S064 URL recorded in corpus/SOURCES.md (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0; record status/bytes/sha256/UTC); compare sha256 to corpus/source-snapshots/round-42/S064.txt; locate all three Gate quotes in LIVE bytes (whitespace-normalized). Locate the REJECTED row's quote live too. File `CritC2Live.md`."),
it("MutC2Chain","mutation-tester",
   CJ+"Mutation-test the C2 instrument chain on scratch mirrors of the landed tree: (a) F25 row status flipped -> harness must FAIL it (this is the r41 blind spot — verify the J7 repair holds); (b) entry source: removed -> recheck-audit fails; (c) capture sha256 corrupted -> binding/source-recheck red; (d) manifest url mutated -> binding red (J6); (e) knowledge file lacking provenance trio. File `MutC2Chain.md`."),
it("RevC2Numbers","reviewer",
   CJ+"Re-measure every C2 counter at the lane tip with the frozen commands: frontier 25, registry (expected 64+R — count mined vs rejected), S064 mined cell, entries citing S064, knowledge 61, harness 28/28 incl PASS F25, binding 56/56, audit expected=61, census exit 0, measure 45/45. File `RevC2Numbers.md`."),
it("CritProvince","critic",
   CJ+"Boundary attack on the F25 pick: re-derive the scout's no-overlap claim — grep kasegi corpus (SOURCES.md, knowledge/, README.md) AND sibling lanes' corpus/knowledge/*.md + corpus/SOURCES.md for the chosen doc's URL stems and vocabulary. Substantive shared ground = C2 NOT VERIFIED (the r41 RFC-9116 precedent). File `CritProvinceBoundary.md`."),
it("CritGate","critic",
   CJ+"Review the round-42 Gate record in corpus/lessons/round-42.md draft (wave1 ScribeC2Gate + L1 integration): >=1 admit AND >=1 reject each with URL + 2026-10-28 access date + <=25-word located quote (D-r41-2 closure); verify each quote is <=25 words and located. Missing reject = defect. File `CritGate.md`."),
it("MutJ1Evidence","mutation-tester",
   CJ+"Mutate J1 (F-EVID) beyond the committed union mutant: (a) evidence named but verdict phrase absent; (b) verdict present but evidence ids missing in ONE record only; (c) union across FILES (SCORECARD has evidence, LOG doesn't); (d) correction grading the WRONG overclaim; (e) evidence ids present but inside a fence. Each on a scratch copy; suite must reject. File `MutJ1Evidence.md`."),
it("MutJ2Token","mutation-tester",
   CJ+"Mutate J2 (F-TOKEN) beyond closed=10/100: `closed = 13/13`, `closed:13/13`, `closed=13/130`, `failures=10`, `closed=1/13`, `xclosed=13/13x`, `13/13` bare, `closed=13.5/13`, `closed=013/013`, HTML entity variants, unicode digits. Each must be rejected. File `MutJ2Token.md`."),
it("MutJ3Table","mutation-tester",
   CJ+"Mutate J3 (F-TABLE): (a) blank line inside table body; (b) leading-whitespace first cell; (c) bare internal pipe in a cell; (d) escaped \\| that looks like a cell boundary; (e) basename mentioned but not as a row; (f) two rows same instrument; (g) row outside header scope. File `MutJ3Table.md`."),
it("MutJ4Decl","mutation-tester",
   CJ+"Mutate J4 (F-DECL): (a) symlinked declared path escaping the export; (b) `..` path components; (c) absolute path declaration; (d) undeclared-path read probe; (e) declared-but-never-read entries (over-declaration); (f) declared path present but a sibling undeclared file also read. File `MutJ4Decl.md`."),
it("MutJ5Scan","mutation-tester",
   CJ+"Mutate J5 (F-SCAN): (a) stray under kasegi-r39/; (b) stray kasegi-r41/SeatX; (c) stray kasegi-r42/OtherSeat (sibling seat in SAME round prefix); (d) outside-configured-root stray at the parent level; (e) dot-prefixed stray dir; (f) case variant KASEGI-R42; (g) symlinked stray. File `MutJ5Scan.md`."),
it("MutJ6Bind","mutation-tester",
   CJ+"Mutate J6 (F-BIND) per MutBind's battery: missing capture path, url trailing slash, http->https variant, sha256 of different file, record for absent source id, extra unbound record, valid-JSON-wrong-schema manifest, duplicate record, case-variant url. File `MutJ6Bind.md`."),
it("MutJ7Flip","mutation-tester",
   CJ+"Mutate J7 (F-FLIP): (a) admitted row missing PASS line; (b) status flipped to queued/explored/rejected; (c) ids cell missing the new source; (d) recheck exit nonzero counted as pass; (e) frontier row with malformed status cell; (f) row present but entry path dangling. File `MutJ7Flip.md`."),
it("CritJ8Forge","critic",
   CJ+"Attack J8 receipt integrity: fabricate a receipt with (a) correct shape wrong payload values; (b) real transcript different ref; (c) run-utc != committer instant; (d) summary-only lines; (e) edited tee (post-hoc line). Verify each is rejected. Also probe: can a receipt be produced WITHOUT a run (tee of nothing)? File `CritJ8Forge.md`."),
it("CritJ9Neg","critic",
   CJ+"Attack J9: (a) does base export REALLY print closed<13/13 (which J checks fail there — enumerate); (b) r41 head export red for the right reasons; (c) unresolvable ref prints ref-not-found (not a silent green); (d) does the suite hang or exit on a truncated archive? File `CritJ9Neg.md`."),
it("CritJ10Iso","critic",
   CJ+"Attack J10 selftest isolation: run the selftest twice CONCURRENTLY in the same scratch root — do cases leak state? Does a leftover fixture from a killed case contaminate the next? File `CritJ10Iso.md`."),
it("CritJ11Corr","critic",
   CJ+"Attack J11 dedup semantics: (a) does the check catch duplicates ACROSS files (same correction text in SCORECARD and LOG — legitimate or dup?); (b) whitespace-normalized dup (trailing-space variant); (c) does the dedup marker requirement itself tolerate a forged marker? File `CritJ11Corr.md`."),
it("RevReplay","reviewer",
   CJ+"Verify every J1-J7 REPLAY limb exists in the landed suite and actually re-executes its committed artifact (not a stub asserting a name): read the suite, extract each replay limb, run each over its artifact; a limb that doesn't replay = kill per frozen kill rule. File `RevReplay.md`."),
it("CritUnionDesign","critic",
   CJ+"Design attack on the J-check set itself: which J can green while its family defect persists through a DIFFERENT channel (e.g. J1 checks records but a new file type carries corrections; J6 checks manifests but a second manifest dir)? File `CritUnionDesign.md`."),
it("ScoutLiveVerify","scout",
   CJ+"Receipt-only: live re-verification sweep of the round-42 additions — re-fetch the S064 URL AND the rejected row's URL; byte-compare; locate Gate quotes in live text. Also re-check S062/S061 flips did not fire. File `ScoutLiveVerify.md`."),
it("ConnPostmortem","connector",
   CJ+"Deliverable `ConnPostmortem.txt` + receipt. Cross-attack synthesis: read EVERY wave-2 receipt as it lands; group findings by family; produce the routed-defects list for the next round (each: family, artifact, verdict) and name any in-family green that kills C1."),
it("ConnPattern","connector",
   CJ+"Deliverable `ConnPattern.txt` + receipt. Cross-wave pattern scan: which escape classes recurred across r39/r40/r41 wave-2s AND appear again in r42 wave-2 — the meta-pattern (e.g. count-relative checks always exploitable)? Names the QUALITY criterion family each maps to."),
it("RevScorecard","reviewer",
   CJ+"Verify SCORECARD.md round-42 section + corrections: dedup marker present; `Correction (round 41)` occurrences consistent with J11 semantics; r41 standings recorded honestly; no verbatim block duplicated. File `RevScorecard.md`."),
it("CritDensity","critic",
   CJ+"Non-target guard: verify corpus/instruments/density.py byte-identical to base (sha256 ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710); SKILL.md diff vs base is append-only; PROVINCE.md amendment appended not rewritten; zero tracked deletions in corpus paths (git diff --name-status base..tip). File `CritDensity.md`."),
it("MutKnowledge","mutation-tester",
   CJ+"Mutate the new knowledge entry on a scratch copy: (a) provenance trio key renamed; (b) recheck line non-executable; (c) a limb anchor pointing outside the capture; (d) entry teaching a claim the source does not support (pick one limb, corrupt it). Which instrument catches each? File `MutKnowledge.md`."),
it("CritAssimilation","critic",
   CJ+"Verify the assimilation verdict: re-run the id-collision extraction (0-3-space tolerant) and the quarantine slice; check ScoutAssimilation/ExecAssimilation verdicts per row; an adoptable row marked quarantined (or reverse) is a finding. File `CritAssimilation.md`."),
it("RevShonen","reviewer",
   CJ+"Review the SHONEN.md round-42 append: every `[~]` line carries a resolvable evidence pointer; no `[x]` self-attested; box 2 honestly states no end-to-end domain hunt. File `RevShonen.md`."),
it("CritReport","critic",
   CJ+"Pre-attack the report's claim language (wave1 ScribeReport + L1 drafts if present): hunt overclaim patterns from r40/r41 — 'verified' without transcript, tallies quoted without committed evidence, J named by hash inside a lane file. File `CritReport.md`."),
it("SentinelWave2","sentinel",
   CJ+"Scope/misroot watch for wave 2: `git -C /home/vgpnk/Projects/shokunin status --porcelain` + ls of wave2 dir every ~10 min; flag any write outside the wave dir shape. File `SentinelWave2.md`."),
it("LabratR41Limb","scout",
   CJ+"Receipt-only probe: on scratch copies run the r41 suite's I1/I3 mutants against the r42 suite's J1/J2 limbs DIRECTLY (extract limbs to scratch harness) — does the r42 check reject what r41 accepted? Transcripts required. File `LabratR41Limb.md`."),
it("CritClosure","critic",
   CJ+"Meta-attack on the round design: does the round-42 kill-rule design (families + replay) still let a kill-class finding slip (a committed artifact showing CURRENT suite accepting an in-family input)? Try to construct one: pick the family you believe weakest and demonstrate or fail. File `CritClosure.md`."),
it("MutDeclared","mutation-tester",
   CJ+"Mutate declared-blocks.txt on a scratch copy: (a) drop one entry the suite reads; (b) add an entry pointing outside the export; (c) corrupt a sha256 cell; (d) reorder; (e) add a duplicate. Which must J4 reject? File `MutDeclared.md`."),
it("RevWaveMix","reviewer",
   CJ+"Verify wave bookkeeping for the report: count seats, roles, attack share from wave1-dispatch.json + wave2-dispatch.json; count dead seats from results.json files; wave-2 has connector seats this round (D-r41-5). File `RevWaveMix.md`."),
]

spec = {
 "wave": "kasegi-r42-falsify",
 "reportDir": ".ufo/waves/round-42/wave2",
 "maxLanes": 64,
 "axes": ["depth:verifiability", "coverage"],
 "milestone": "round-42 falsify wave 2: re-run frozen counters, replay every committed defeat against the landed suite, mutation-test J1-J13 limbs, live re-open S064 + reject row, receipt forgery attacks, boundary/gate review",
 "context": CTX,
 "items": items,
}
out = os.path.join(R, W, "wave2-spec.json")
with open(out, "w") as f:
    json.dump(spec, f, indent=1, ensure_ascii=False)
print("wrote", out, "items:", len(items))
import collections
print(collections.Counter(i["role"] for i in items))
