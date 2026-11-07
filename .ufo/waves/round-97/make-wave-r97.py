#!/usr/bin/env python3
"""Build the round-97 w1 spec (one v1 wave, 14 seats).
Usage: make-wave-r97.py BASE FREEZE C1LAND C2LAND > .ufo/waves/round-97/w1-spec.json
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
WAVE = ".ufo/waves/round-97/w1"
C1SHA = "a56198d00505cb81cb971b959aa32f4c917c74c48bf1f482521d7c50e8bb57da"
MAPSHA = "f4ed7387ca08146e1426e22d7ad3a3c60082a53ae77b9556351ffaade0783c0c"
LABSHA = "5155959d4cea88bde7f44c0590f007731700a3072faa93f8ecbbd16410ffc853"
INSTR = "59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92"
GATE = "8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6"

CONTEXT = f"""# Goal
Kasegi round 97, attempt 1, ONE v1 wave of 14 seats (count from this spec's items). Two frozen claims, both already landed before this wave was dispatched; base {BASE}, freeze {FREEZE}, C1 landing {C1LAND}, C2 landing {C2LAND}. Frozen statements, predicates, kill rules, sha256 pins and every executed pre-freeze control: {LANE}/.ufo/waves/round-97/claims.json and {LANE}/.ufo/waves/round-97/controls/.

C1 depth:verifiability (lowest axis, score 4) — tranche 12 qualifies 33 bare lane-instrument basenames to their tracked `corpus/instruments/` paths across 16 `corpus/knowledge/*.md` files: `resolve.py`, `anchorcheck.py`, `capture-source.py`, `source-recheck.py`, `density.py`, `capture-secret-scan.py`, `claim-package-check.py`, `r35-defect-closure.sh`, `r36-closure.sh` (nine distinct tokens). The round-97 counter adds the `qualify-lane` label kind: the written value must be a tracked, non-.ufo path at the after revision that classifies INTERNAL, the key must be a bare basename, and the edit is exactly `key` -> `label`. The meter reads 1040/2041 at the base and 1043/2035 at the landing (three of the nine qualified tokens are new to the scope; six already existed, so those rows shrink the denominator instead). The control set ships thirteen attribution fixtures: each negative fixture's failing-limb set equals the set declared in the harness.

C2 coverage (score 8 held, capability extension of capture-secret-scan) — the ten remaining GitLab families the round-96 known-limits list named, all published in S140: the runner registration token (`GR1348941` + 20, line 101), the `feed_token=` query form (line 160), `gloas-` + 64 (line 174), `glft-` + 20 (line 190), the plain `glagent-` 50-character form (line 213, the round-96 spot-check's routed defect 1), `glimt-` + 20-25 lower-case with the optional instance prefix (line 229), `glsoat-` + 20 (line 278), the `gitlab+deploy-token-<N>:<token>@` URL form (line 341), `glffct-` + 20 (line 392) and `glrct-` + 20 (line 412). Selftest 128 -> 148 cases; the known-limits list keeps only the path-dependent `glft-` 64-hex form, the `t1_` legacy partition token and the `/trigger/pipeline` URL form.

# Rules
- Working dir for every command: {LANE} (absolute paths only). Scratch S=/fast/scratch/hyaku/kasegi-r97/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT and pass TMPDIR=$S explicitly; nothing of yours may outlive the seat. `/tmp` is for files under 50 MB only.
- Read-only on the lane's git/jj state: never git add/commit/push/checkout/reset/stash and never a mutating jj command anywhere. Seats return findings and files only; the L1 commits. Never edit MANIFEST.json, the fleet repo, sibling lanes, .ufo/state, .scratch, /boot, /etc, /usr, /var, /efi, other users' homes, or any file outside your wave report/receipt paths. Host paths are read-only inputs; never run a binary-editing tool with a host path as its input. Never mutate host sysctls.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Fixture repos: D=$(mktemp -d) && git -C "$D" init -q; assert git -C "$D" rev-parse --show-toplevel equals $D before any mutating git command; never pass an empty or unchecked variable to `git -C`.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool/npx/an official binary in ~/.local/bin, or name the need in your report. Never run -Sy/-Syu/-U/-R, never downgrade, never restart a host service.
- Never call the `ask` tool; never message agent://all; never spawn subagents. Leaf seat.
- Every claim is judged on its frozen predicate only. A finding that does not re-score a claim is a routed defect/qualifier, not a verdict change.
- Output: one report file at the path your item names, with a `## Verdict` line and a `## Receipts` list of the commands you ran and their observed rc/lines (no credential values, no fabricated numbers). Say `AGREE`/`STANDS` only when you re-derived it yourself.

# Evidence already committed at the freeze
- claims.json; C1 counter (sha256 {C1SHA}), map ({MAPSHA}), labels ({LABSHA}), generator; the control harness and its receipt (14 controls, ATTRIBUTION pass fixtures=13).
- C2 capability gate, candidate scanner (sha256 {INSTR}), the extended SCORECARD row; the pre-freeze K1-K6 pass at the scratch candidate 72fa2fa1.
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
    item("CriticClaimsC1", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/CriticClaimsC1; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C1's frozen predicate P1-P4 at the C1 landing {C1LAND}. Re-run the frozen counter yourself in a fresh `git clone --shared` of the landing: `python3 -B .ufo/waves/round-97/c1/knowledge-meter.py --lane <clone> --base-rev {BASE} --after-rev {C1LAND} --map .ufo/waves/round-97/c1/repair-map.tsv --labels-rev {FREEZE} --base-target 1040/2041 --target 1043/2035 --map-sha256 {MAPSHA} --work $S`. Re-derive every limb value independently where you can (M0/M1 by an independent resolver census over corpus/knowledge at both revisions; M3 by applying the map yourself; M9/M10 by reading the 33 labels). Re-run the control harness `.ufo/waves/round-97/controls/c1-controls-r97.py <clone of the landing> {FREEZE} .ufo/waves/round-96/c1/knowledge-meter.py $S/ctl $S/out` and check every CONTROL line's limbs= equals its declared=. Then attack the claim's semantic core: is each of the nine bare tokens really the LANE'S instrument at its site (not a lost-tree path or a quoted field), and does every qualified path exist at the landing? P1-P4 are in claims.json; report STANDS / NOT-VERIFIED per limb with your own numbers, and route (do not re-score) anything you cannot bind."""),
    item("CriticClaimsC2", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/CriticClaimsC2; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C2's frozen predicate K1-K6 at the C2 landing {C2LAND}. Re-run `.ufo/waves/round-97/c2/capability-check.py --lane <clone of the landing> --rev {C2LAND} --work $S --instrument-sha256 {INSTR} --gate-sha256 {GATE}` at three seeds of your own. Independently test each of the ten shapes against S140's published regexes (corpus/source-snapshots/round-94/S140.txt lines 101, 160, 174, 190, 213, 229, 278, 341, 392, 412): the exact lengths (20, 64, 20, 20-25, 20, 20, 50), the lower-case-only alphabet of `glimt-`, the `@` terminator of the deploy-token URL form, the `glagent-` 50 right boundary (a following dot is allowed only when not followed by a lower-case alphanumeric), and whether any new shape swallows a plain token of the same family. Check K4 (the round-96 instrument misses all ten) and K6 (no earlier shape lost). Report STANDS / NOT-VERIFIED per limb with your own numbers; route anything you cannot bind."""),
    item("CriticHarm", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/CriticHarm; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Harm audit for the round, base {BASE} -> C1 {C1LAND} and C2 {C2LAND}. Check: (1) SKILL.md blob identical base->tip (density guard) and PROVINCE.md/SHONEN.md/AGENTS.md untouched; (2) every `corpus/knowledge/*.md` citation token the C1 landing did not touch is byte-unchanged, and no citation lost resolution (count with corpus/instruments/resolve.py at base and tip, report both); (3) the C2 scanner change cannot mask an earlier shape: run the landed scanner and the round-96 scanner over the same sample you build and diff the (path, shape) sets; (4) the allowlist is unchanged this round and the landed scanner's `--rev {C2LAND}` run is clean. One `HARM` or `NO HARM` line per item with numbers; anything wrong is a routed defect, and say whether it re-scores a claim."""),
    item("ReviewC1Sites", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ReviewC1Sites; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Read every one of the 33 C1 map rows (`.ufo/waves/round-97/c1/repair-map.tsv`, landing {C1LAND}) against the committed bytes of its line. For each row output CORRECT / PARTIAL / WRONG with the anchor line quoted and, for a PARTIAL/WRONG, the exact defect. The truth test: the bare token names the LANE'S instrument (not the lost tree's copy, not a manifest field value), the qualified path is the tracked file at the landing, and the sentence still reads true with the path substituted. Flag any site where the qualification changes what the sentence asserts (e.g. a quoted manifest `path` field, a directory listing, a lost-tree path). Also write the round-98 label set for any site you find wrong (a TSV with line/key/label/fix/evidence, the round-96 label shape) and a `round98-labels.tsv` header-only file if none."""),
    item("ReviewC2Scanner", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ReviewC2Scanner; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Review the landed scanner at {C2LAND} against the frozen statement: read the diff of corpus/instruments/capture-secret-scan.py from {BASE} and check each clause against S140's published regexes. Verify: the left boundary and optional custom prefix on each shape (and that the shapes whose rule has NO prefix do not accept one); the exact lengths; the `glimt-` lower-case alphabet; the `gitlab+deploy-token-<N>:` URL form's digits and `@`; the `glagent-` 50-character form's right boundary (dot allowed only when not followed by a lower-case alphanumeric, or at end); and that no new shape fires on a plain 20-character token of the same family. Run `--selftest` and `--rev {C2LAND}`. Output APPROVE / REQUEST-CHANGES with numbered findings; each finding names the line and the S140 line it violates."""),
    item("MutC1Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/MutC1Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutation-test the round-97 C1 control set. Build at least ten single-point mutants of the round-97 counter (drop the tracked/INTERNAL check on a qualify-lane target; allow a key with a separator; accept `new != label`; drop the old==`key` check; accept a `.ufo/` target; drop M3's old_not_once; drop M10's unapplied set; drop M9's new comparison; drop M6; make M10 accept an unknown kind) and run the frozen harness `.ufo/waves/round-97/controls/c1-controls-r97.py` against each (parameterise only the counter path; a copy of the harness in your scratch is the probe, the frozen file is read-only). Report, per mutant: killed by which control, or survived and why. Also try at least two forgeries of the harness itself (a declared set that hides a real FAIL; a fixture that edits the meter) and say what catches them."""),
    item("MutC2Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/MutC2Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutation-test the round-97 C2 shapes and gate. Build at least ten single-point mutants of the landed scanner (drop the `glagent-` 50 right boundary; accept 49 or 51; widen `glimt-` to upper-case; drop the `@` on the deploy-token URL form; accept 19 or 21 on one 20-length shape; accept a 63-character `gloas-`; let `glft-` accept 21; drop the left boundary on one shape; make `glsoat-` accept a custom prefix; make `feed_token=` case-insensitive) and run the frozen gate `.ufo/waves/round-97/c2/capability-check.py` against each (K1's sha pin will refuse a mutated instrument: record that as the guard, then run the gate with the pin omitted to see which behavioural limb catches each mutant). Report killed/survived per mutant with the limb that caught it. Also try at least two forgeries of the gate itself and say what catches them."""),
    item("SentinelShapes", "sentinel", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/SentinelShapes; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Security review of the ten new shapes at {C2LAND}, read as an attacker who wants a real token to pass unseen. For each shape, list the bypass classes you can construct: escape contexts the left boundary does not cover (`&#x26;` without semicolon, `\\x26`, double-encoded), a token split across a line wrap, a token embedded in a longer alphanumeric run, a token with a trailing `_`, a token inside a URL query, a token with a percent-encoded separator, and a custom instance prefix longer than 20 characters. Run each against the landed scanner and report HIT/MISS with the exact bytes (never a real credential: build synthetic values). Report MUST-FIX items separately from routed ones; state whether any finding re-scores K1-K6."""),
    item("ExecC1Indep", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ExecC1Indep; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent re-derivation of C1's numbers, without importing the lane's counter. (1) Write your own census of distinct backticked path-like tokens over `corpus/knowledge/*.md` at {BASE} and {C1LAND} (state your extraction and classification rules) and compare the denominator change and numerator delta with the meter's 1040/2041 -> 1043/2035. (2) Apply `.ufo/waves/round-97/c1/repair-map.tsv` to a `git archive {BASE}` extract yourself and diff the result against `git archive {C1LAND}` for the twelve files: they must be byte-identical. (3) Count the changed lines with `git diff --numstat {BASE} {C1LAND} -- corpus/knowledge` and check the claim's "33 rows on 30 lines" reading. Report AGREE or DISAGREE per item with your numbers."""),
    item("ExecC2Probe", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ExecC2Probe; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent probe of the ten new shapes at {C2LAND}: write your own fixture generator (not the gate's) that builds, for each shape, three positives (bare, inside JSON, after an escape) and three negatives (one character short, one character long, wrong case in the tail where the rule has a case), run the landed scanner `--files` over them, and report the (fixture, expected, observed) table. Then run the round-96 scanner (at {BASE}) over the same positives and confirm it misses all of them. Report PASS/FAIL per shape with the exact fixture bytes."""),
    item("ExecC2Counter", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ExecC2Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent re-derivation of C2's gate numbers. (1) Re-run the frozen gate at {C2LAND} at three seeds of your own and report every K limb's detail line. (2) Re-derive K1's selftest count with an AST count over the committed instrument (cases + paths + checks) and compare with `cases=148`. (3) Re-derive K5 independently: `git show {C2LAND}:SCORECARD.md`, split the `capture-secret-scan` row into cells, check exactly one row, the last cell `87`, and that all ten new shape ids appear in the "what it can now do" cell. (4) Re-derive K6 at the round-86 freeze and name every shape the landed scanner reports there. Report AGREE/DISAGREE per item with numbers."""),
    item("ScoutSources", "scout", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ScoutSources; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Source reconnaissance for the round's Gate (read-only; the L1 writes the rows). Three jobs. (1) Re-open S140's live source (GitLab secret-detection rules `gitlab.toml` at commit 59ada1f4) and confirm the ten rules the round used are still at lines 101, 160, 174, 190, 213, 229, 278, 341, 392, 412 of the committed capture, quoting each regex line (redact any example value). (2) Open ONE candidate new source that states GitLab's token prefixes with their lengths in prose (the GitLab docs token-overview page or the API authentication page): record URL, access date, HTTP status, the exact section heading and a <=25-word located quote, and say whether it is tier A or B for the scope "GitLab token prefix and length". (3) Open ONE candidate you expect to REJECT and record why with the absence sweep that grounds it. Never write outside your report/receipts."""),
    item("ConnectorOverlap", "connector", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ConnectorOverlap; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Sibling-overlap scan for the round's two claims. (1) Search the sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for any instrument that (a) measures citation resolution or knowledge-scope token rates, (b) implements GitLab token shapes, or (c) ships single-defect attribution fixtures for a counter. Report lane, path, and whether kasegi's work duplicates or should defer. (2) Read `considerthese/` (operator-authored, read-only) and name at most one still-unimplemented proposal that fits either claim, with the file and line; if none fits, say so. (3) Check whether any sibling lane already cites S140 or the same GitLab rules file, and whether the lane's new shapes would belong to another lane's province (report, do not absorb)."""),
    item("ScribeGate", "scribe", f"""Scratch S=/fast/scratch/hyaku/kasegi-r97/ScribeGate; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Draft (do not land) the round-97 lesson's Gate block and the SOURCES rows the L1 will verify. Read `corpus/SOURCES.md` (contract v1 shape), `corpus/lessons/round-96.md` (its Gate form and the routed defects the closure listed) and the round-97 claims. Produce: (a) a `## Gate` block in the round-96 shape that records, for each new row, the URL, the access date and a <=25-word located quote, plus at least one reject with its reason and flip; (b) a draft `## Mistakes` table with at least three rows in the class / evidence pointer / captured-by / fix form, mined from this round's own work (the two qualify-lane attribution couplings and the SCORECARD shape-id requirement are the obvious candidates); (c) a draft knowledge entry `corpus/knowledge/gitlab-remaining-token-families.md` (Q1-Q6 compliant: source/verified-at/recheck header, per-shape S140 line, a verbatim <=25-word quote each, one falsifiable rule and one rejected over-generalization, documentation-only) — write it under your scratch, never into corpus/. Report the drafts' paths and the Q1-Q6 self-check."""),
]

SPEC = {
    "wave": "kasegi-r97-w1",
    "milestone": "round-97 attempt 1: C1 tranche 12 (33 qualify-lane rows, nine bare lane-instrument basenames, meter 1040/2041 -> 1043/2035) and C2 capture-secret-scan ten remaining GitLab families (S140) with selftest 128 -> 148; attack, verify, draft",
    "reportDir": WAVE,
    "maxLanes": 16,
    "axes": ["depth:verifiability", "coverage"],
    "context": CONTEXT,
    "items": ITEMS,
}

json.dump(SPEC, sys.stdout, indent=1)
