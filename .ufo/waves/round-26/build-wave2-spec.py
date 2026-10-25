#!/usr/bin/env python3
"""Build wave-2 (falsify + integration closure) spec for kasegi round 26."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
SHOKU = "/home/vgpnk/Projects/shokuknow"
R26 = ".ufo/waves/round-26"
W2 = ".ufo/waves/round-26/wave2"

CONTEXT = f"""# Round
kasegi-shokunin round 26, wave 2 (falsify + integration closure), dispatched by the L1 after wave 1
landed. Fleet root {FLEET}. Lane repo {LANE} — your only write scope. Current lane state: wave-1
build has landed (claims C1/C2 implemented; S041 capture + manifest + SOURCES row + F11 row + two
knowledge entries + regenerated receipts + cadence-only recheck cells + expected list 39). The L1
integrated the four blockers found by wave 1 (README/SCORECARD F11 names aligned to actual
unsuffixed filenames; S040/S041 recheck cells restored to bare `180d` with prose recorded under
`## Registry changes`; knowledge-expected.txt regenerated to 39 entries; c1-receipt-index.txt +
c1-instrument-digest.txt regenerated at landed instrument digest 3fc0d751… with selftest cases=15).
Measured at integration time: census exit 0; frontier-recheck-count 14/14 exit 0; live audit 39/39
exit 0 expect=present; deletion fixture exit 1 missing=<name>; registry grep 1; selftest receipt line
1; fix-control restated BRE 0; awk frontier 11; precise S041-citing entries 2.

Read before your item (absolute paths):
- {LANE}/.ufo/waves/round-26/claims.json (FROZEN; do not edit)
- {LANE}/SCORECARD.md (axes, round-26 result rows)
- {LANE}/corpus/QUALITY.md (Q1-Q9, R1-R12)
- {LANE}/corpus/README.md (frontier F11 row)
- {LANE}/corpus/SOURCES.md (S040/S041 rows + Registry changes note)
- {LANE}/corpus/lessons/round-26.md (lesson incl open-items block)
- {LANE}/corpus/instruments/recheck-audit.py (landed --expect version, digest 3fc0d751…)
- {LANE}/corpus/instruments/knowledge-expected.txt (39 entries)
- {LANE}/.ufo/waves/round-26/c1-receipt-index.txt, c1-instrument-digest.txt, c1-live.json
- {LANE}/.ufo/waves/round-26/c1-controls/ (wave-1 control receipts)
- {LANE}/corpus/source-snapshots/round-26/ (S041.txt, S040-live.txt, manifest.json)
- {LANE}/corpus/knowledge/iso-29147-and-30111-division-of-labour.md and
  iso-29147-divergence-and-clause-crosswalk.md

# Hard rules (every seat)
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- You are a leaf: spawn nothing, start no background job, run no swarm of your own.
- Write ONLY your owned paths. A read-only seat makes NO production edit; its output is its report
  file (and, where the item says so, files under {W2}/ or {R26}/c1-controls/). The one production
  writer this wave is the scribe amend seat (ScribeLessonAmend, sole owner of
  corpus/lessons/round-26.md). All other seats are read-only.
- Never write {FLEET} (fleet root), any sibling lane, {SHOKU} (READ-ONLY), {FLEET}/.ufo/state,
  {FLEET}/.scratch, MANIFEST.json, templates/ or fleet scripts/.
- Never run VCS mutations in the lane. Read-only git is fine.
- Tooling: pacman transactions PAUSED host-wide; uv tool/npx/official binary only; read
  /home/vgpnk/.omp/agent/RULES.md before installing; record installs in report.
- Honesty: an unrun check has not passed; never fabricate a verdict, quote, count or exit code.
- Never edit claims.json or round-25 files. Today is 2026-10-25; use UTC.

# Attack items (falsify the claimed AFTER states; each report names what it attacks and its verdict)
"""

ITEMS = {
  "a1": dict(role="reviewer", axes=["depth:verifiability"], milestone="C1a registry row counter",
    task=f"""Attack C1 counter (a): run `grep -cE '^\\| [^|]+\\| gate\\|probe ' SKILL.md` (expect 1)
and also grep for a row whose THIRD field begins with literal `gate|probe `; verify the row content
against the Gate-standard fields (name, type, entry command, verdict map, self-test spelling
--selftest, pinned-value path, write scope, owner). Report whether the counter could be satisfied by a
decorative row under the current bytes, and whether the landed row is complete. Output:
{W2}/a1.md (read-only)."""),
  "a2": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="C1b counter gameability",
    task=f"""Attack C1 counter (b): the selftest line grep `grep -cE 'selftest cases=' {R26}/c1-receipt-index.txt`
returns 1. On a scratch COPY of the receipt, produce a misleading line `selftest cases=15 failures=0
exit=0` without any run and confirm the counter still returns 1 (document). Also confirm the real
receipt's selftest line is backed by a true 15-case run (see e1-selftest-live.txt and the index's
regeneration note). Output {W2}/a2.md; scratch only."""),
  "a3": dict(role="reviewer", axes=["depth:verifiability"], milestone="C1 receipt-digest equality",
    task=f"""Verify the receipt index digest binding: read {R26}/c1-receipt-index.txt and
{R26}/c1-instrument-digest.txt; compute `sha256sum corpus/instruments/recheck-audit.py`; assert all
three match the landed instrument (3fc0d751…) and that base_sha256_control equals the round-25 pinned
digest c3c19adc… (pre-change control). Report the three values. Also confirm c1-live.json instrument
hash equals the same. Output {W2}/a3.md (read-only)."""),
  "a4": dict(role="reviewer", axes=["depth:verifiability"], milestone="C1c fix-control semantics",
    task=f"""Attack C1 counter (c): run the restated fix-control in BOTH spellings from the lane root:
(a) the frozen spelling with `-E` and `\\|` (GNU grep on this host treats `\\|` as literal — record
output), (b) the BRE alternation without `-E`: `grep -rnE '62 assertions|77 assertions'
corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' |
wc -l` (expect 0) and without the exclusion (expect 1, the retained historical line). Report both,
plus the exact retained line text. Output {W2}/a4.md (read-only)."""),
  "a5": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="C1d deletion mutants on landed bytes",
    task=f"""Re-run the deletion-mutant suite on the LANDED instrument (digest 3fc0d751…), each fixture
being a scratch copy of corpus/ WITH the committed knowledge-expected.txt present:
A) delete whole entry (e.g. multiparty-vulnerability-coordination.md) → expect exit 1 +
`missing=…`; B) delete the recheck line from one entry → expect exit 1 (completeness); C) rename a
knowledge file → expect exit 1 + `missing=… unexpected=…`; D) add stray extra file without recheck →
expect exit 1 + `unexpected=…`; E) clean copy → expect exit 0 + `expect=present expected=39`.
Record every verbatim tail line (lines/total/exit/expect/missing/unexpected). Also verify a copy
WITHOUT the expected list (expect=absent) reproduces the old green pass for mutant A (document the
fallback). Output {W2}/a5.md + {R26}/c1-controls/a5-*.txt (scratch fixtures under /tmp)."""),
  "a6": dict(role="reviewer", axes=["depth:verifiability"], milestone="expected-list parity",
    task=f"""Verify `corpus/instruments/knowledge-expected.txt`: (1) sorted, one relative path per line,
comments only in the 2-line header; (2) non-comment set == `ls corpus/knowledge/*.md | sort`
(39 entries); (3) no blank/duplicate/CR; (4) every name exists; (5) report the exact count. Also cross
check that `git status --porcelain corpus/knowledge/` shows exactly the two new untracked entries.
Output {W2}/a6.md (read-only)."""),
  "a7": dict(role="reviewer", axes=["depth:verifiability"], milestone="instrument diff review",
    task=f"""Review the landed `recheck-audit.py` changes (git diff vs base 1b076fa7): --expect
argument + default resolution, expected-list reading (skip blank/#), set comparison, missing/unexpected
receipt fields, exit semantics (0 clean/1 failed), expect=present/absent behavior, docstring updated,
selftest count 15. Flag any path by which a deletion could still pass (e.g. expected file deleted
together with an entry — compare against claims' kill rules). Output {W2}/a7.md (read-only)."""),
  "a8": dict(role="reviewer", axes=["depth:verifiability"], milestone="selftest truth",
    task=f"""Run `python3 corpus/instruments/recheck-audit.py --selftest` from the lane root; count the
lines matching `selftest … ok` (expect 15), confirm `failures=0` and final exit 0, list each case name.
Cross-check the receipt's `selftest cases=15 failures=0 exit=0` line against the observed run. Output
{W2}/a8.md (read-only)."""),
  "a9": dict(role="critic", axes=["depth:verifiability"], milestone="registry row conformance",
    task=f"""Apply the Gate-standard registry field checklist to the SKILL.md row: name, type
(gate|probe), entry command, verdict map (0 clean / 1 failed / undeclared nonzero ->
could-not-evaluate), self-test command, spelling `--selftest`, pinned-value path, write scope, owner.
Quote the landed row; report each field present/absent; note the unescaped `gate|probe` rendering
trade-off. Output {W2}/a9.md (read-only)."""),
  "b1": dict(role="reviewer", axes=["coverage"], milestone="census exit re-measure",
    task=f"""Re-run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` and record exit (expect 0; W04 S028/S029 pre-existing). Also
run against an explicit lane dir. Confirm no E09/E11. Output {W2}/b1.md (read-only)."""),
  "b2": dict(role="reviewer", axes=["coverage"], milestone="registry R9 row citation coverage",
    task=f"""Scan corpus/SOURCES.md rows and corpus/knowledge/*.md `source:` headers: report any row with
no citing entry (R9 violation) and any citing id not present in the registry. Verify S041 is cited by
exactly the two new F11 entries and S040 still by the F10 crosswalk. Output {W2}/b2.md (read-only)."""),
  "b3": dict(role="reviewer", axes=["coverage"], milestone="frontier harness re-run",
    task=f"""Run `python3 corpus/instruments/frontier-recheck-count.py --root <lane>` and record per-row
lines + exit (expect 14/14 exit 0, F11 twice with ids=S041). Also verify the F11 entry-cell names
equal the two real unsuffixed filenames and that both files exist. Output {W2}/b3.md (read-only)."""),
  "b4": dict(role="reviewer", axes=["coverage"], milestone="README variant sanity",
    task=f"""Check corpus/README.md: F11 row exactly once; awk frontier counter = 11; entry cell paths
exist; sources cell = S041; no stray F12; other rows untouched (compare F01-F10 with round-25 map).
Also note header/count mentions (37→39) consistency. Output {W2}/b4.md (read-only)."""),
  "b5": dict(role="reviewer", axes=["coverage"], milestone="S041 capture pinning",
    task=f"""Verify S041 pinning: file `corpus/source-snapshots/round-26/S041.txt` sha256 equals the
capture log `(e18acbf9…)`, equals manifest's sha256, and the capture log line exists in wave1
ExecCaptureS041.md. Grep the snapshot for the division-of-labour paragraph line ~1670-1673 and the
図1 caption line 1678. Output {W2}/b5.md (read-only)."""),
  "b6": dict(role="reviewer", axes=["coverage"], milestone="manifest quote recheck re-run",
    task=f"""Run `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json
--source S041` and record per-quote verdicts + exit (expect exit 0). Confirm quote texts are ≤70
chars and locatable. Output {W2}/b6.md (read-only)."""),
  "b7": dict(role="reviewer", axes=["coverage"], milestone="precise C2 counter",
    task=f"""Run the precise round-26 counter: `grep -lE '^source: S041 ' corpus/knowledge/*.md | wc -l`
(expect 2) and the frozen overmatch `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l`
(expect 3: round-25 S040 + the two S041). Explain why the frozen 'before 0' is stale (round-25 S040)
and why the precise S041-only measure is the honest one for 'first registered this round'. Output
{W2}/b7.md (read-only)."""),
  "b8": dict(role="critic", axes=["coverage"], milestone="C2 vacuity re-probe",
    task=f"""Re-attack C2 counters on final bytes: (1) could the two entries be renamed/emptied while all
counters stay green? Check the entries' bodies have real quoted content (report presence of quotes and
source headers); (2) simulate removing the S041 row → which checks fail (census/frontier)? (3)
simulate F11 row → status staged → awk count 10 (confirm filtering). Report verdicts. Output
{W2}/b8.md (scratch only)."""),
  "c1": dict(role="reviewer", axes=["coverage"], milestone="entry division-of-labour quality audit",
    task=f"""Audit `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` against Q1-Q9: headers
(source S041 / verified-at 2026-10-25 / recheck command with --manifest path), every quote present in
the captured S041.txt with correct line refs and ≤70 chars, thesis grounded, no invented claims, no
staged F19/F20 ground leak, title/scope consistent with the README F11 row. Report the verdict and any
defect. Output {W2}/c1.md (read-only)."""),
  "c2": dict(role="reviewer", axes=["coverage"], milestone="entry crosswalk quality audit",
    task=f"""Audit `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` similarly: quotes
(divergence sentence, 7-day, 6.2/6.3, 参考1) with line refs and ≤70 chars against S041.txt, Cisco
edition claim against S040-live.txt line 58, no duplication of F10 coverage without added value.
Report verdict + defects. Output {W2}/c2.md (read-only)."""),
  "c3": dict(role="connector", axes=["coverage"], milestone="duplication scan",
    task=f"""Compare the two new F11 entries against F10 entries (vendor-disclosure-policies-as-corpus-objects.md,
vendor-disclosure-policy-commitments-crosswalk.md) for duplicated quotes/themes; report overlap verdicts
and any unique content each adds (mirror the round-25 verifier's duplication rule). Output {W2}/c3.md
(read-only)."""),
  "d1": dict(role="reviewer", axes=["depth:verifiability","coverage"], milestone="lesson integrity audit",
    task=f"""Audit `corpus/lessons/round-26.md`: Gate block (admits/rejects/quarantine verdicts) matches
the wave-1 data (reject reasons + flips; seven quarantine verdicts); kill-rule status matches final
state; fix-control #3 restated text + recorded 0; no fabricated outputs; counters table matches final
measured values; access-date evidence today. Report any stale statement (especially any 'open item'
that the L1 has since closed). Output {W2}/d1.md (read-only)."""),
  "d2": dict(role="reviewer", axes=["depth:verifiability"], milestone="scorecard consistency",
    task=f"""Verify SCORECARD.md round-26 rows against evidence pointers: C1 row's evidence file
(c1-receipt-index.txt) exists and matches current receipt; C2 row's names match actual filenames;
capability row source-capture-pdf evidence exists; r27 planned row is plan-only and not marked done.
Report drift, if any. Output {W2}/d2.md (read-only)."""),
  "d3": dict(role="reviewer", axes=["coverage"], milestone="LOG/PROVINCE accuracy",
    task=f"""Spot-check LOG.md round-26 entry and PROVINCE.md F11 sentence for factual consistency with the
final state (frontier 11, S041 row, census 0, receipt digest). Quote any discrepancy. Output
{W2}/d3.md (read-only)."""),
  "e1": dict(role="revenger", axes=["depth:verifiability"], milestone="R25 lineage re-confirm",
    task=f"""Re-derive the round-25 digest lineage from git (read-only): confirm the round-25 tip
instrument sha equals c3c19adc…, the committed receipt index has no selftest line at :4, and the new
round-26 receipt (at 3fc0d751…) fixes the cross-reference with its note line. Quote the old line 4 and
the new selftest line. Output {W2}/e1.md (read-only)."""),
  "e2": dict(role="revenger", axes=["depth:verifiability"], milestone="S040 fingerprint + final URL",
    task=f"""Combine the wave-1 s2 probe with the round-25 verifier note into one fingerprint: canonical URL
→ 301 → final URL → 200 under instrument UA; browser UA 403; S040-live.txt sha256 b7f7b55f… equals
round-25 snapshot; the S040 recheck cell now bare `180d`, with final URL/UA recorded in `## Registry
changes`. Output {W2}/e2.md (read-only)."""),
  "f1": dict(role="sentinel", axes=["depth:verifiability"], milestone="final scope sweep",
    task=f"""Final read-only sweep: (1) working tree changes since base 1b076fa7 ⊆ owned paths (reuse
wave1/c4-ownership.txt; allow wave2 reports + the lesson amend + c1-controls additions); (2) no fleet
root / shokuknow / sibling writes; (3) claims.json byte-equal freeze commit (sha 343e568e…); (4) HEAD
still at base (no VCS write by any seat). Output {W2}/f1.md (read-only; run LAST)."""),
  "g1": dict(role="sentinel", axes=["coverage"], milestone="contract deliverables checklist",
    task=f"""Check final deliverables presence: two knowledge entries, SOURCES S041 row + bare recheck
cells, README F11 (names aligned), lesson round-26 with Gate/fixes/appendix, SCORECARD rows,
knowledge-expected.txt (39), c1-receipt-index.txt + c1-instrument-digest.txt + c1-live.json, manifest.json,
S041.txt, S040-live.txt, c1-controls/, c2-controls/, wave1 & wave2 reports. For each: exists + non-empty.
Report gaps only. Output {W2}/g1.md (read-only)."""),
  "h1": dict(role="executor", axes=["depth:verifiability"], milestone="live audit receipt regen check",
    task=f"""Re-run the live audit `python3 corpus/instruments/recheck-audit.py --json
{R26}/c1-live.json` and record exit + summary (expect lines=39 total=39 pass=39 exit=0
expect=present expected=39 missing=0 unexpected=0). Note any deviation. Output {W2}/h1.md; writes only
its report (the JSON receipt is owned by the L1's receipt file — do not overwrite unless identical)."""),
  "i1": dict(role="critic", axes=["depth:verifiability"], milestone="kill-rule recheck",
    task=f"""Re-evaluate the frozen kill rules against the final state: C1 (all four counters green after
regeneration); C2 (census exit 0; every new row cited; precise counter ≥1). State explicitly which kill
rule would fire for each known failure mode (deletion pass, census E09, orphan row, counter overmatch)
and confirm none fires now. Output {W2}/i1.md (read-only)."""),
  "i2": dict(role="mutation-tester", axes=["coverage"], milestone="row-deletion sensitivity",
    task=f"""On scratch copies, test that removing (1) the S041 row from SOURCES, (2) one F11 entry from
knowledge/, (3) the F11 row from README, each individually causes at least one gate red (census exit
or frontier exit or awk count). Record which gate fires for which removal and that the committed state
has none missing. Output {W2}/i2.md (scratch only)."""),
  "j1": dict(role="scout", axes=["coverage"], milestone="staged rejects presence",
    task=f"""Re-confirm the two reject candidates remain in the staged package with their documented
grounds (vendor-cvd-policy-crosswalk-2026-10-23.md ground F20; chinese-criminal-thresholds-and-authorisation.md
ground F12) and that the lane corpus contains no F12/F19/F20 frontier rows; report the reject reasons +
flip conditions carried by the lesson. Output {W2}/j1.md (read-only)."""),
  "k1": dict(role="reviewer", axes=["depth:verifiability"], milestone="old receipts untouched",
    task=f"""Confirm no round-25 or earlier file changed: `git diff 1b076fa7 --stat` shows only the
round-26 files; specifically `.ufo/waves/round-25/` untouched and `corpus/lessons/round-25*.md`
untouched. Output {W2}/k1.md (read-only)."""),
  "l1": dict(role="scout", axes=["depth:verifiability"], milestone="git log freeze visibility",
    task=f"""Show `git log --oneline -3` and confirm the claims-freeze commit (1b076fa7 "round-26:
freeze claims.json …") is the parent of the build state, with no post-freeze edit of claims.json
(byte-equal). Output {W2}/l1.md (read-only)."""),
  "m1": dict(role="mutation-tester", axes=["depth:verifiability"], milestone="receipt line mutants",
    task=f"""Probe the regenerated c1-receipt-index.txt counter determinism: (1) delete the selftest line
→ grep 0; (2) change `failures=0` → `failures=1` → grep still 1 (document counter blind spot); (3)
change digest → grep still 1. Note any hardening suggestion for wave3/report. Output {W2}/m1.md
(scratch only)."""),
}

DEFERRED = {
  "z1": dict(role="connector", axes=["coverage"], milestone="used-by edge map (deferred)",
    task=f"""Complete the wave-1 failed seat: compute used-by edges for S039/S040/S041 from
corpus/knowledge/*.md `source:` headers; assert S041 used-by = the two F11 entries, S040 = the F10
crosswalk, S039 = both F10 entries + none of the F11 entries; confirm no orphan rows (R9). Output
{W2}/z1.md (read-only)."""),
  "z2": dict(role="scribe", axes=["coverage"], milestone="lesson open-items closure (deferred)",
    task=f"""Amend `corpus/lessons/round-26.md` (SOLE OWNER; append a dated `## Integration closure
(2026-10-25)` block): record the four wave-1 open items and their resolution — (1) receipt index
regenerated at landed digest 3fc0d751… with `selftest cases=15 failures=0 exit=0`; (2) census E09/E11
cleared by cadence-only recheck cells (S040/S041) with final-URL/UA prose moved to `## Registry
changes`; (3) README/SCORECARD F11 entry names aligned to actual filenames; (4) knowledge-expected.txt
regenerated to 39 entries. Append the final measured counter table (C1a 1; C1b 1; C1c BRE 0; C1d
deletion exit 1 + missing=<name>; C2 awk 11; precise S041-citing 2; census exit 0; frontier 14/14
exit 0). Do not alter earlier blocks. Report appended lines. Output {W2}/z2.md."""),
}

if __name__ == "__main__":
    spec = {
      "wave": "kasegi-r26-falsify",
      "context": CONTEXT,
      "reportDir": W2,
      "maxLanes": 64,
      "axes": ["depth:verifiability", "coverage"],
      "milestone": "round-26 falsify wave: attack the claimed AFTER states + integration closure",
      "items": [],
    }
    order = ["a1","a2","a3","a4","a5","a6","a7","a8","a9",
             "b1","b2","b3","b4","b5","b6","b7","b8",
             "c1","c2","c3","d1","d2","d3","e1","e2",
             "f1","g1","h1","i1","i2","j1","k1","l1","m1",
             "z1","z2"]
    camels = {"z2":"ScribeLessonAmend"}
    for key in order:
        it = ITEMS.get(key) or DEFERRED.get(key)
        spec["items"].append({
          "name": camels.get(key, "Attack" + key[0].upper() + key[1:]),
          "role": it["role"],
          "axes": it["axes"],
          "milestone": it["milestone"],
          "prompt": it["task"],
        })
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave2-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, ensure_ascii=False, indent=1)
    print("wrote", out, "items:", len(spec["items"]))
