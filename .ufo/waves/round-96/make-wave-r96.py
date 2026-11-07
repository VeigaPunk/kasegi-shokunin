#!/usr/bin/env python3
"""Build the round-96 w1 spec (one v1 wave, 13 seats).
Usage: make-wave-r96.py BASE FREEZE C1LAND C2LAND > .ufo/waves/round-96/w1-spec.json
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
WAVE = ".ufo/waves/round-96/w1"

CONTEXT = f"""# Goal
Kasegi round 96, attempt 1, ONE v1 wave of 13 seats (count from this spec's items). Two frozen claims, both already landed before this wave was dispatched; base {BASE}, freeze {FREEZE}, C1 landing {C1LAND}, C2 landing {C2LAND}. Frozen statements, predicates, kill rules, sha256 pins and every executed pre-freeze control: {LANE}/.ufo/waves/round-96/claims.json and {LANE}/.ufo/waves/round-96/controls/.

C1 depth:verifiability (lowest axis, score 4) — tranche 11 lands the five round-95 non-author labels: `SKILL.md:182-184` -> `SKILL.md:182-185` on triage-thresholds.md:88 and inside `SKILL.md:182-184,255-257` on :90; the last bare `S041.txt:1680-1681` becomes its committed capture path at iso-29147-divergence-and-clause-crosswalk.md:13; and the two prose pointers on iso-29147:36 narrow to `(L1832-1833)` and `e) ... (L1834)`. The round-96 counter adds the prose-pointer `part` binding in M4 (the edited substring is exactly the key and only its `(L...)` numbers change). The control set ships eleven attribution fixtures: each negative fixture's failing-limb set equals the set declared in the harness (the round-95 mutation campaign left 10 of 18 mutants alive because no negative fixture isolated its rule). Meter 1030/2027 -> 1032/2028.

C2 coverage (score 8 held, capability extension of capture-secret-scan) — seven GitLab shapes S140 publishes and the round-95 scanner could not express: the routable and versioned-routable forms of `glpat-` (lines 30, 51), `glrtr-` (136), `gldt-` (324), `glagent-` (358) and `glwt-` (375), plus `glptt-` (line 73, exactly 20 or exactly 40 characters). Selftest 115 -> 128 cases; the docstring's known-limits list drops the six families this round detects.

# Rules
- Working dir for every command: {LANE} (absolute paths only). Scratch S=/fast/scratch/hyaku/kasegi-r96/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT and pass TMPDIR=$S explicitly; nothing of yours may outlive the seat. `/tmp` is for files under 50 MB only.
- Read-only on the lane's git/jj state: never git add/commit/push/checkout/reset/stash and never a mutating jj command anywhere. Seats return findings and files only; the L1 commits. Never edit MANIFEST.json, the fleet repo, sibling lanes, .ufo/state, .scratch, /boot, /etc, /usr, /var, /efi, other users' homes, or any file outside your wave report/receipt paths. Host paths are read-only inputs; never run a binary-editing tool with a host path as its input.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Fixture repos: D=$(mktemp -d) && git -C "$D" init -q; assert git -C "$D" rev-parse --show-toplevel equals $D before any mutating git command; never pass an empty or unchecked variable to `git -C`.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool/npx/an official binary in ~/.local/bin, or name the need in your report. Never run -Sy/-Syu/-U/-R, never downgrade, never restart a host service, never mutate host sysctls.
- Never call the `ask` tool; never message agent://all; never spawn subagents. Leaf seat.
- Every claim is judged on its frozen predicate only. A finding that does not re-score a claim is a routed defect/qualifier, not a verdict change.
- Output: one report file at the path your item names, with a `## Verdict` line and a `## Receipts` list of the commands you ran and their observed rc/lines (no credential values, no fabricated numbers). Say `AGREE`/`STANDS` only when you re-derived it yourself.

# Evidence already committed at the freeze
- claims.json; C1 counter (sha256 fadd0ede47392ce0f15596377728415d8e5cc7906874debe1229ee17c8ad36db), map (7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f), labels, generator; the control harness and its receipt (12 controls, ATTRIBUTION pass fixtures=11).
- C2 capability gate, candidate scanner (sha256 71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9), candidate row; the pre-freeze K1-K6 pass at the scratch candidate b31227ca.
- S140 is GitLab's `gitlab.toml` at commit 59ada1f4 under corpus/source-snapshots/round-94/ (example values structurally redacted, line numbering preserved).

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
    item("CriticClaimsC1", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/CriticClaimsC1; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C1's frozen predicate P1-P4 at the C1 landing {C1LAND}. Re-run the frozen counter yourself in a fresh `git clone --shared` of the landing: `python3 -B .ufo/waves/round-96/c1/knowledge-meter.py --lane <clone> --base-rev {BASE} --after-rev {C1LAND} --map .ufo/waves/round-96/c1/repair-map.tsv --labels-rev {FREEZE} --base-target 1030/2027 --target 1032/2028 --map-sha256 7d9bb49f366a594df3cd13e5651a6db4aabef1ab4b5a7081d89fd5f8c68b1d0f --work $S`. Re-derive every limb value independently where you can (M0/M1 by an independent resolver census over corpus/knowledge at both revisions; M3 by applying the map yourself; M9/M10 by reading the labels). Re-run the control harness `.ufo/waves/round-96/controls/c1-controls-r96.py <clone of the landing> {FREEZE} .ufo/waves/round-95/c1/knowledge-meter.py $S/work $S/out` and check every control reproduces AFTER the landing, that each fixture's FAIL set equals its declared set, and that the do-nothing control cannot reach the target. Attack the prose-pointer M4 branch: can a row satisfy it while editing text outside its own pointer, or while introducing a citation through a non-backticked form? Verdict line: C1 STANDS / NOT VERIFIED on <limb>, with the limb values you measured."""),
    item("CriticClaimsC2", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/CriticClaimsC2; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C2's frozen predicate K1-K6 at the C2 landing {C2LAND}. Re-run `.ufo/waves/round-96/c2/capability-check.py --lane <clone of the landing> --rev {C2LAND} --work $S --instrument-sha256 71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9 --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` at three seeds of your own. Independently test each of the seven shapes against S140's published regexes: the 27-character head floor, the 2+7 and 2+2+7 tails, the case of each segment, the right boundary after the tail, the optional custom instance prefix, `glptt-` 20 vs 40 vs 39, and whether any new shape swallows a plain 20-character token of the same family. Check K4's claim that the base instrument misses all seven, and that no earlier shape is lost. Verdict line: C2 STANDS / NOT VERIFIED on <limb>."""),
    item("CriticHarm", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/CriticHarm; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Harm audit for the round, base {BASE} -> C1 {C1LAND} and C2 {C2LAND}. Check: (1) SKILL.md blob identical base->tip (density guard) and PROVINCE.md/SHONEN.md/AGENTS.md untouched; (2) every `corpus/knowledge/*.md` citation token the C1 landing did not touch is byte-unchanged, and no citation lost resolution (count with corpus/instruments/resolve.py at base and tip, report both); (3) the C2 scanner change cannot mask an earlier shape: run the landed scanner and the round-95 scanner over the same sample you build and diff the (path, shape) sets; (4) the allowlist is unchanged this round and the landed scanner's `--rev {C2LAND}` run is clean. One `HARM` or `NO HARM` line per item with numbers; anything wrong is a routed defect, and say whether it re-scores a claim."""),
    item("ReviewC1Sites", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ReviewC1Sites; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Read each of the five C1 edits (map `.ufo/waves/round-96/c1/repair-map.tsv`, landing {C1LAND}) against the committed bytes of its anchor. For each row output CORRECT / PARTIAL / WRONG with the anchor line quoted and, for a PARTIAL, the exact defect. Focus on truth of the NEW text: `SKILL.md:182-185` must carry the completed round-13 correction (the `is_live(1)` omission sentence ends on 185), `SKILL.md:182-185,255-257` must be true of both ranges, `corpus/source-snapshots/round-30/S041.txt:1680-1681` must be in range and carry the quoted no-contradiction sentence, and the two `(L...)` pointers must land on the d) and e) items of the minimum-policy list (S041 1832-1834 and 1835). Also write the round-97 label set for any site you find wrong (a TSV with line/key/label/fix/evidence) into your receipts. Output a table plus the label file path."""),
    item("ReviewC2Scanner", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ReviewC2Scanner; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Review the landed scanner at {C2LAND} against the frozen statement: read the diff of corpus/instruments/capture-secret-scan.py from {BASE} and check each clause against S140's published regexes (corpus/source-snapshots/round-94/S140.txt lines 30, 51, 73, 136, 324, 358, 375). Verify: the left boundary and optional custom prefix on each shape; the 27-300 head; the routable tail `.` + 2 + 7 and the versioned tail `.` + 2 + `.` + 2 + 7; that the routable shape cannot match a versioned token and vice versa; that `glptt-` 20 and 40 are exact and 39 is not a hit; that no new shape fires on a plain 20-character `glpat-`/`gldt-` token. Run `--selftest` and `--rev {C2LAND}`. Output APPROVE / REQUEST-CHANGES with numbered findings; each finding names the line and the command."""),
    item("MutC1Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/MutC1Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutation-test the round-96 C1 control set. Reconstruct the ten surviving mutants the round-95 campaign recorded (`.ufo/waves/round-95/w1/MutC1Counter.md` names each: m06_cell_multi_value_forbidden, s01_old_absent_accepted, s02_m9_ignores_new, s03_missing_label_no_edit, s04_snapshot_existence_dropped, s05_unknown_kind_allowed, s06_unlabelled_ignored, s07_unapplied_ignored, s08_part_any_old, s09_skip_absent_label) as single-point edits of the round-96 counter, and run the frozen harness `.ufo/waves/round-96/controls/c1-controls-r96.py` against each mutant (parameterise only the counter path; a copy of the harness in your scratch is the probe, the frozen file is read-only). Report, per mutant: killed by which control, or survived and why; and whether the round-96 attribution fixtures change the round-95 outcome. Do not modify the frozen counter, harness, map or labels. Output the kill table plus the manifest of your diffs."""),
    item("MutC2Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/MutC2Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutation-test the round-96 C2 shapes and gate. Build at least eight single-point mutants of the landed scanner (drop the 27-head floor; widen the routable tail to 1+7; accept uppercase in the tail; drop the right boundary; make `glptt-` accept 21-39; drop the custom instance prefix on one shape; make the versioned shape accept a 1-character middle; make `gitlab-pat-routable` also match the versioned form) and run the frozen gate `.ufo/waves/round-96/c2/capability-check.py` against each (K1's sha pin will refuse a mutated instrument: record that as the guard, then run the gate with the pin omitted to see which behavioural limb catches each mutant). Report killed/survived per mutant with the limb that caught it. Also try at least two forgeries of the gate itself (a plant outside the scan scope; a fixture-literal detector) and say whether the digest pin is the only guard."""),
    item("SentinelShapes", "sentinel", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/SentinelShapes; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Security review of the seven new shapes at {C2LAND}, read as an attacker who wants a real token to pass unseen. For each shape, list the bypass classes you can construct: escape contexts the left boundary does not cover (`&#x26;` without semicolon, `\\x26`, HTML entity decimal, double-encoded), a token split across a line wrap, a token embedded in a longer alphanumeric run, a token with a trailing `_`, a token inside a URL query, a token with a percent-encoded `.` separator, and a custom instance prefix longer than 20 characters. Run each against the landed scanner and report HIT/MISS with the exact bytes (never a real credential: build synthetic values). Report MUST-FIX items separately from routed ones; state whether any finding re-scores K1-K6."""),
    item("ExecC1Indep", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ExecC1Indep; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent re-derivation of C1's numbers, without importing the lane's counter. (1) Write your own census of distinct backticked path-like tokens over `corpus/knowledge/*.md` at {BASE} and {C1LAND} (state your extraction and classification rules) and compare the denominator change and numerator delta with the meter's 1030/2027 -> 1032/2028. (2) Apply `.ufo/waves/round-96/c1/repair-map.tsv` to a `git archive {BASE}` extract yourself and diff the result against `git archive {C1LAND}` for the two files: they must be byte-identical. (3) Count the changed lines with `git diff --numstat {BASE} {C1LAND} -- corpus/knowledge` and check the claim's "five edits" reading. Report AGREE or DISAGREE per item with your numbers."""),
    item("ExecC2Probe", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ExecC2Probe; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent probe of the seven new shapes at {C2LAND}: write your own fixture generator (not the gate's) that builds, for each shape, three positives (bare, inside JSON, after an escape) and three negatives (one character short, one character long, wrong case in the tail), run the landed scanner `--files` over them, and report the (fixture, expected, observed) table. Then run the round-95 scanner (at {BASE}) over the same positives and confirm it misses all of them. Report PASS/FAIL per shape with the exact fixture bytes."""),
    item("ScoutSources", "scout", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ScoutSources; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Source reconnaissance for the round's Gate (read-only; the L1 writes the rows). Three jobs. (1) Re-open S140's live source (GitLab secret-detection rules `gitlab.toml` at commit 59ada1f4) and confirm the seven rules the round used are still at lines 30, 51, 73, 136, 324, 358, 375 of the committed capture, quoting each regex line (redact any example value). (2) Find and open ONE candidate new source that states GitLab's token prefixes with their lengths in prose (the GitLab docs token-overview page or the API authentication page): record URL, access date, HTTP status, the exact section heading and a <=25-word located quote, and say whether it is tier A or B for the scope "GitLab token prefix and length". (3) Find and open ONE candidate you expect to REJECT (e.g. a blog or a marketing page about token scanning): record the same fields and the reason it fails the lane's bar. Write every URL, date and quote into your receipts; never paste a credential-shaped example value."""),
    item("ConnectorOverlap", "connector", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ConnectorOverlap; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Sibling-overlap scan for the round's two claims. (1) Search the sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for any instrument that (a) measures citation resolution or knowledge-scope token rates, (b) implements GitLab token shapes, or (c) ships single-defect attribution fixtures for a counter. Report lane, path, and whether kasegi's work duplicates or should defer. (2) Read `considerthese/` (operator-authored, read-only) and name at most one still-unimplemented proposal that fits either claim, with the file and line; if none fits, say so. (3) Check whether any sibling lane already cites S140 or the same GitLab rules file, and whether the lane's new shapes would belong to another lane's province (report, do not absorb)."""),
    item("ScribeGate", "scribe", f"""Scratch S=/fast/scratch/hyaku/kasegi-r96/ScribeGate; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Draft (do not land) the round-96 lesson's Gate block and the two SOURCES rows the L1 will verify. Read `corpus/SOURCES.md` (contract v1 shape), `corpus/lessons/round-95.md` (its Gate form and the six routed defects the closure listed) and the round-96 claims. Produce: (a) a `## Gate` block in the round-95 shape that records, for each new row, the URL, the access date and a <=25-word located quote, plus at least one reject with its reason and flip; (b) a draft `## Mistakes` table with at least three rows in the class / evidence pointer / captured-by / fix form, mined from this round's own work (the two fixture defects the harness caught pre-freeze are the obvious ones); (c) a draft knowledge entry `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` opening with `source:`, `verified-at:` and `recheck:`, stating the seven shapes with their S140 line cites and the boundaries the scanner enforces, and carrying no sentence the landed docstring contradicts. Write all three as files under your receipts and name their paths."""),
]

SPEC = {
    "wave": "kasegi-r96-w1",
    "milestone": "round-96 attempt 1: C1 tranche 11 (5 label rows, prose-pointer M4, 11 attribution fixtures, meter 1030/2027 -> 1032/2028) and C2 capture-secret-scan routable/versioned/glptt shapes (S140) with selftest 115 -> 128; attack, verify, draft",
    "reportDir": WAVE,
    "maxLanes": 16,
    "axes": ["depth:verifiability", "coverage"],
    "context": CONTEXT,
    "items": ITEMS,
}

json.dump(SPEC, sys.stdout, indent=1)
