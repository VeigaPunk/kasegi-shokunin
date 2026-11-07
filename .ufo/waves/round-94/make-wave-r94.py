#!/usr/bin/env python3
"""Build the round-94 w1 spec (one v1 wave, 13 seats). Values are placeholders
filled from argv: BASE FREEZE C1LANDING C2LANDING
Usage: make-wave-r94.py BASE FREEZE C1LAND C2LAND > .ufo/waves/round-94/w1-spec.json
"""
import json
import sys

BASE, FREEZE, C1LAND, C2LAND = sys.argv[1:5]

GOD = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

"""

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
WAVE = ".ufo/waves/round-94/w1"

CONTEXT = f"""# Goal
Kasegi round 94, attempt 1, ONE v1 wave of 13 seats (count from this spec's items; state no other number). Two frozen claims, both already landed before this wave was dispatched; base {BASE}, freeze {FREEZE}, C1 landing {C1LAND}, C2 landing {C2LAND}. Frozen statements, predicates, kill rules, sha256 pins and every executed pre-freeze control: {LANE}/.ufo/waves/round-94/claims.json and {LANE}/.ufo/waves/round-94/controls/.

Claims in one line each: C1 depth:verifiability (lowest axis, score 4) — tranche 9 applies the 19 token-level repoints the round-94 non-author labels name (triage-thresholds.md 17 sites, considerthese-proposals-ledger.md 1 site with two occurrences) under a successor counter that walks every labelled file including one outside corpus/knowledge, binds lane-root tokens embedded in a cell-repair replacement, and prints the measured revision; 10 label rows needing a prose reword stay EXCLUDED with reasons; measured knowledge meter 1008/1999 -> 1009/2000. C2 coverage (score 8 held, capability extension of capture-secret-scan) — three GitLab shapes from the vendor's own rules file (S140): the PAT custom instance prefix, the runner authentication token (glrt-/glrtr-, optional t1_/t2_/t3_) and the deploy token (gldt-); the round-93 glrt- known limit is retired; every planted path and basename is relocated at run time; K9 is a new previous-landing regression limb.

# Rules
- Working dir for every command: {LANE} (absolute paths only). Your own scratch S=/fast/scratch/hyaku/kasegi-r94/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT and pass TMPDIR=$S explicitly; nothing of yours may outlive the seat. Files under 50 MB only outside that scratch.
- Read-only on the lane's git/jj state: never git add/commit/push/checkout/reset/stash and never a mutating jj command anywhere. Seats return findings and files only; the L1 commits. Never edit MANIFEST.json, the fleet repo, sibling lanes, .ufo/state, .scratch, or any file outside your wave report/receipt paths.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Fixture repos: D=$(mktemp -d) && git -C "$D" init -q; assert git -C "$D" rev-parse --show-toplevel equals $D before the first commit; never run a mutating git command with an empty or unchecked variable.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool/npx/an official binary in ~/.local/bin, or name the need in your report. Never run -Sy/-Syu/-U/-R, never downgrade, never restart a host service, never mutate host sysctls.
- Never call the `ask` tool; never message agent://all; never spawn subagents. Leaf seat: no delegation except an executor's single read-only labrat probe (not needed this round).
- Every claim is judged on its frozen predicate only. A finding that does not re-score a claim is a routed defect/qualifier, not a verdict change.
- Output: one report file at the path your item names, with a `## Verdict` line and a `## Receipts` list of the commands you ran and their observed rc/lines (no credential values, no fabricated numbers). Say `AGREE`/`STANDS` only when you re-derived it yourself.

# Evidence already committed at the freeze
- claims.json, the C1 counter/map/labels, the C2 counter and candidate scanner/row, the executed control receipts (c1-controls-r94.txt 12/12, c2-controls-r94.txt 10/10), the S140 capture+manifest (example values redacted, line numbering kept), the redaction and intake receipts, the census receipts.
- The S140 capture is redacted because GitHub push protection refuses the published example values; the three quoted regex lines keep their anchors (4, 114, 255) and source-recheck passes.

# Godspeed lead (verbatim)
{GOD}"""


def item(name, role, body, report=None):
    report = report or f"{WAVE}/{name}.md"
    return {
        "name": name,
        "role": role,
        "prompt": GOD + body + f"\n\nReport: {report}\nReceipts: {WAVE}/{name}-receipts/ (create it; every command output you cite goes there).\n",
    }


ITEMS = [
    item("CriticClaimsC1", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/CriticClaimsC1; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C1's frozen predicate P1-P4 at the C1 landing {C1LAND}: re-run the frozen counter yourself from committed bytes in a fresh `git clone --shared` of the landing (`python3 -B .ufo/waves/round-94/c1/knowledge-meter.py --lane <clone> --base-rev {BASE} --after-rev {C1LAND} --map .ufo/waves/round-94/c1/repair-map.tsv --labels-rev {FREEZE} --base-target 1008/1999 --target 1009/2000 --map-sha256 11de45a74337b945b5179645e18e0f710a2f9ec54935450806a0e4bda7a78847 --work $S`), verify the freeze commit precedes the landing and every control receipt is a freeze blob, and test at least four forgery variants of your own (an unlabelled in-scope edit; an out-of-scope edit; a map row whose `new` text differs from the label; a label whose anchor is out of range; a cell-repair row whose lane-root token is past EOF). Verify the ten EXCLUDED pairs are genuinely unmapped and that M3 compares a labelled file outside corpus/knowledge (build a fixture like the shipped control). State STANDS or DOES-NOT-STAND on the frozen predicate only, with the exact limb output for each attack, and list qualifiers separately."""),
    item("CriticClaimsC2", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/CriticClaimsC2; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C2's frozen predicate P1-P4 at the C2 landing {C2LAND}: re-run the frozen counter in a fresh `git clone --shared` of the landing at three seeds (the printed run-time one, 1 and 9191) with `--instrument-sha256 22ba32d145f90f7759caf16d3ee524eb1779153d3f2a33611675a93a4667beaf --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`; verify the landed scanner sha256 equals the pin and the landing diff is exactly two paths; verify the landed SCORECARD row equals the frozen candidate row byte-for-byte. Then attack the counter's own guards: a path-shape-keyed scanner (hardcode `round-1/` and `S0NN.txt` shapes), a harness-gated scanner, a scanner with `gldt-` accepted at any length, and a scanner that drops `github-token`; each must be rejected by a limb. Report which limb rejects each or SURVIVOR with the run output. State STANDS or DOES-NOT-STAND on the frozen predicate only; qualifiers separately."""),
    item("ReviewC1Labels", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ReviewC1Labels; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Hand-read the 19 landed repoints at {C1LAND} against the cited bytes, one row each, with the cited line quoted: triage-thresholds.md lines 143, 151, 153, 220, 267, 310-313, 355, 374, 390, 394, 397 (two tokens), 446, 459, 460 and considerthese-proposals-ledger.md:156 (both occurrences). For each say CORRECT / PARTIAL / WRONG with the reason (does the new anchor line state what the citing cell says?). Then read the ten EXCLUDED rows and say whether each exclusion is right or whether a token repoint alone would have stayed true. Finally write the next tranche's non-author labels (5-column TSV `line key label fix evidence`, same schema as .ufo/waves/round-94/c1/labels.tsv) for every remaining wrong-but-token-fixable citation you can prove, to {WAVE}/ReviewC1Labels-receipts/round95-labels.tsv, and a verify script + output that re-derives each row from the cited bytes."""),
    item("ReviewC2Scanner", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ReviewC2Scanner; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Read the landed scanner at {C2LAND} and the S140 capture corpus/source-snapshots/round-94/S140.txt. Check clause by clause against the frozen C2 statement: the three new shape regexes against S140 lines 4, 114 and 255 (quote them from the capture), the custom-prefix alphabet bound, the optional t1_/t2_/t3_ partition, the right boundary, that the three quoted lines are unredacted and the 18 redacted lines carry the fixed marker, and that no round-87..93 sentence became false. Verify the docstring's known-limits list and the citation line numbers against the capture. Enumerate the knowledge entries that cite capture-secret-scan.py by line (`grep -rlE 'capture-secret-scan\\.py:[0-9]' corpus/knowledge`) and list every citation whose line numbers the landing shifted, with old and new bounds. Report clause-by-clause and write the re-anchor list (if any) to a receipt."""),
    item("MutC1Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/MutC1Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutate the frozen round-94 C1 counter at the freeze commit {FREEZE} (read it with `git show {FREEZE}:.ufo/waves/round-94/c1/knowledge-meter.py` into your scratch) one change at a time and run every mutant against the landed state ({C1LAND}) and against the control fixtures you can rebuild from .ufo/waves/round-94/controls/c1-controls-r94.txt (at least 12 mutants). Targets: `lane_specs` (a comma-combined value, an out-of-range part, a malformed part), the M5 lane-root loop, the M3 replace-all and the per-site edit list, the EXCLUDED set, the M3 labelled-file union, the M10 completeness on (site,key), the `after_rev` print. For each mutant record: killed by which limb/control, or SURVIVOR with the exact input that proves it. Survivors are routed defects for round 95, not claim re-scores."""),
    item("MutC2Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/MutC2Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Forge the frozen round-94 C2 counter at the landed state ({C2LAND}): the counter relocates every plant path and basename and adds K9. Build at least six forgeries of your own beyond the shipped controls: (1) a detector keyed on the relocated path *shape* (`source-snapshots/r<8hex>/<12hex>.txt`), (2) a detector that returns clean when its own path contains the counter's work-dir prefix, (3) a detector that drops one old shape, (4) `gldt-` at any length, (5) `glpat-` with any 3+ tail, (6) a detector that reads the K4 plant literals from its own source. Run each through the frozen counter pinned and unpinned, at two seeds, in a fresh clone. Record which limb rejects each, or SURVIVOR with the run output. Also probe K9: can a scanner lose an old shape and still pass? Prove your answer."""),
    item("SentinelShapes", "sentinel", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/SentinelShapes; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Adversarial probe of the landed scanner at {C2LAND} (run a copy beside that rev's claim-package-check.py and capture-secret-allow.tsv). Fixtures are one file each, generated in your scratch, never real values. Measure and tabulate: (a) the three new shapes in at least eight encodings (JSON \\t/\\u0020/\\u0026, %20/%26, HTML entities, line start, after `=`, in a URL, in a cookie header, quoted JSON value) with DETECTED/MISSED and the reason; (b) the custom-prefix boundary class: 1-, 20- and 21-character prefixes, a prefix with `_`, `-glpat-` at line start, `xglpat-`, a prefix with a dot; (c) false positives: prose mentioning `gldt-`, documentation placeholders, a 21-character tail, a token followed by `-`, an acronym like `gldt-` inside a word; (d) ReDoS timing on a 1 MB worst-case line for each new pattern. Do not widen anything yourself. Every miss/false positive becomes a routed defect with the exact fixture and observed output."""),
    item("ScoutGitLabRules", "scout", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ScoutGitLabRules; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Per-surface reconnaissance on the GitLab source, frozen: do NOT edit corpus/. Re-fetch the S140 rules file (the API raw URL pinned to commit 59ada1f4 is in corpus/source-snapshots/round-94/manifest.json) and compare its bytes with the committed capture, reporting the 18 redacted line numbers and the sha of the fetched bytes. Then enumerate the next leads with URL, HTTP status, whether the page states the shape, and a located quote: the `glcbt-eyJ…`/`glsat-eyJ…`/`gliamat-eyJ…` JWT forms, `glagent-` 50, `glsoat-` 20, `glffct-` 20, `gloas-` 64, the routable/versioned forms, and GitHub's `ghr_` 76 refresh token (rules/mit/github/github.toml). Rank them for round 95 and say which one source row grounds which shape. Record every page you opened, including rejections with the reason."""),
    item("ConnectorOverlap", "connector", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ConnectorOverlap; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Sibling-overlap scan across the fleet: read (read-only) the other lanes' committed instruments and gates that touch secret scanning or citation verification — list them with paths and hashes — and report every overlap with kasegi's C1/C2 surfaces: a sibling scanner that already covers a shape this lane claims, a sibling gate that already verifies citation anchors, or a sibling capability row that duplicates `capture-secret-scan`. For each overlap say whether it is duplication (report it, do not absorb) or a distinct scope, with the command and line numbers that prove it. Do not edit any sibling repo. Also check the lane's own two counters for a duplicated limb (M3 vs M4 vs M5 can each catch the same forgery) and report which limbs are sole guards."""),
    item("CriticHarm", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/CriticHarm; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Harm check across the lane's axes at {BASE} -> {C2LAND} + the C1 landing and the freeze: `git diff --stat` for SKILL.md, PROVINCE.md, SHENEN/AGENTS, corpus/README.md; confirm SKILL.md bytes are identical base->tip; count the full-path scanner citations in corpus/knowledge at base and at each landing (`git grep -oE 'capture-secret-scan\\.py:[0-9]+' <rev> -- corpus/knowledge | wc -l`) and every out-of-range one; recount the knowledge meter rate at base and at the C1 landing independently (your own extractor, no counter code) and explain the 1008/1999 -> 1009/2000 arithmetic token by token; check that the S140 redaction did not change the SOURCES row's tier/status cells or drop a cell; check that the ten EXCLUDED rows still cite their old anchors. Report no-harm or a named harm with the exact command; a disclosed qualifier is not a harm."""),
    item("ExecC1Indep", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ExecC1Indep; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent byte check of C1 at {C1LAND}, importing no counter code: build the base and after trees with `git archive` into $S, then for each of the 19 map rows in .ufo/waves/round-94/c1/repair-map.tsv reconstruct the expected line edit yourself from the row and compare with the after tree's line. Report: per-row `line key expected==after`, the exact set of changed lines between base and after (should be 18 lines: 17 in triage-thresholds.md, where line 397 carries two edits, and line 156 in considerthese-proposals-ledger.md), that every old token occurs at least once on its base line, that every new value's anchor lies inside SKILL.md, and that no other line in either file changed. Also count the occurrences of the ledger key on its base line and of its replacement in the after line."""),
    item("ExecC2Probe", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ExecC2Probe; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent probe of the landed scanner at {C2LAND}, not importing the counter and not reusing its fixtures: copy `corpus/instruments/capture-secret-scan.py` and the gate beside it from {C2LAND} (`git show {C2LAND}:...`) into your scratch, then build your own fixture files and measure: `acme-glpat-<20>`, `glpat-<20>`, `glrt-<20>`, `glrtr-t1_<20>`, `gldt-<20>`, `acme-glrt-<20>`, `acme-gldt-<20>`; negatives `xglpat-<20>`, `gldt-<19>`, `gldt-<21>`, `glrt-<21>`, `glrtr-t4_<20>` (24-char tail), `GLD T-<20>`, a 21-character custom prefix. Run `--selftest` and report `SELFTEST-RESULT`; run `--files` on your fixtures and report the exact HIT set. Also scan the S140 capture itself and report hits/allowed."""),
    item("ScribeGate", "scribe", f"""Scratch S=/fast/scratch/hyaku/kasegi-r94/ScribeGate; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Draft (do not commit) the round-94 lesson's `## Gate` block and `## Mistakes` rows from the committed evidence at {FREEZE} and {C1LAND}: for S140 record the URL, access date 2026-11-07, the three ≤25-word located quotes (lines 4, 114, 255), the tier/scope reasoning, the redaction and the intake refusal; for the mistake rows use (i) M93-4 (the round-93 nonce left basenames and the `round-1` segment, so a path-shape-keyed detector passed) and (ii) M93-5 (the counter's M3 union crashed on a labelled non-knowledge file) with class, evidence pointer, captured-by and fix; show each fix can fail by pointing at the committed control lines. Also verify the SOURCES S140 row and the two round-94 bullets against `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (exit code and row count). Write the draft to {WAVE}/ScribeGate-draft.md with a `## Gate`, `## Mistakes` and `## Census` section; the L1 owns the final lesson."""),
]


def main():
    spec = {
        "wave": "kasegi-r94-w1",
        "milestone": "round-94 attempt 1: C1 tranche 9 (19 label-named repoints, M3 union + cell-repair M5 + revision print, meter 1008/1999 -> 1009/2000) and C2 capture-secret-scan GitLab custom prefix + runner + deploy shapes (S140) with relocated plants and K9; attack, verify, draft",
        "reportDir": WAVE,
        "maxLanes": 16,
        "axes": ["depth:verifiability", "coverage"],
        "context": CONTEXT,
        "items": ITEMS,
    }
    json.dump(spec, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
