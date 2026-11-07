#!/usr/bin/env python3
"""Build the round-93 w1 spec (one v1 wave, 13 seats). Values are placeholders
filled from argv: BASE FREEZE C1LANDING C2LANDING
Usage: make-wave-r93.py BASE FREEZE C1LANDING C2LANDING > .ufo/waves/round-93/w1-spec.json
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

CONTEXT = f"""# Goal
Kasegi round 93, attempt 1, ONE v1 wave of 13 seats (count from this spec's items; state no other number). Two frozen claims, both already landed before this wave was dispatched; base {BASE}, freeze {FREEZE}, C1 landing {C1LAND}, C2 landing {C2LAND}. Frozen statements, predicates, kill rules, sha256 pins and every executed pre-freeze control: {LANE}/.ufo/waves/round-93/claims.json and {LANE}/.ufo/waves/round-93/controls/.

Claims in one line each: C1 depth:verifiability (lowest axis, score 4) — tranche 8 closes the last five GONE bare-key sites in corpus/knowledge/triage-thresholds.md (2 whole-cell errata repairs, the 454 second-token repoint, the 58/144 surviving SKILL.md:117 ties) under a successor counter with `cell-repair` and lane-root `SKILL.md:N[-M]` kinds and an M3 that walks every labelled file; measured knowledge meter 1007/2001 -> 1009/2000. C2 coverage (score 8 held, capability extension of capture-secret-scan) — new `gitlab-pat` shape (`glpat-` + 20 characters, S139) and the escape-terminator left boundary for `github-token` (round-92 SentinelGitHub P1), verified by a successor counter that plants every value under a run-time nonce directory and carries U1-U6 boundary negatives.

# Rules
- Working dir for every command: {LANE} (absolute paths only). Your own scratch S=/fast/scratch/hyaku/kasegi-r93/<your seat name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT and pass TMPDIR=$S explicitly; nothing of yours may outlive the seat. Files under 50 MB only outside that scratch.
- Read-only on the lane's git/jj state: never git add/commit/push/checkout/reset/stash and never a mutating jj command anywhere. Seats return findings and files only; the L1 commits. Never edit MANIFEST.json, the fleet repo, sibling lanes, .ufo/state, .scratch, or any file outside your wave report/receipt paths.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Fixture repos: D=$(mktemp -d) && git -C "$D" init -q; assert git -C "$D" rev-parse --show-toplevel equals $D before the first commit; never run a mutating git command with an empty or unchecked variable.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide; install via uv tool/npx/an official binary in ~/.local/bin, or name the need in your report. Never run -Sy/-Syu/-U/-R, never downgrade, never restart a host service, never mutate host sysctls.
- Never call the `ask` tool; never message agent://all; never spawn subagents. Leaf seat: no delegation except an executor's single read-only labrat probe (not needed this round).
- Every claim is judged on its frozen predicate only. A finding that does not re-score a claim is a routed defect/qualifier, not a verdict change.
- Output: one report file at the path your item names, with a `## Verdict` line and a `## Receipts` list of the commands you ran and their observed rc/lines (no credential values, no fabricated numbers). Say `AGREE`/`STANDS` only when you re-derived it yourself.

# Godspeed lead (verbatim)
{GOD}"""


def item(name, role, body, report):
    return {
        "name": name,
        "role": role,
        "prompt": GOD + body + f"\n\nReport: {report}\nReceipts: .ufo/waves/round-93/w1/{name}-receipts/ (create it; every command output you cite goes there).\n",
    }

ITEMS = [
    item("CriticClaimsC1", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/CriticClaimsC1; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C1's frozen predicate P1-P3 at the C1 landing {C1LAND}: re-run the frozen counter yourself from committed bytes in a fresh `git clone --shared` of the landing (`python3 -B .ufo/waves/round-93/c1/knowledge-meter.py --lane <clone> --base-rev {BASE} --after-rev {C1LAND} --map .ufo/waves/round-93/c1/repair-map.tsv --labels-rev {FREEZE} --base-target 1007/2001 --target 1009/2000 --map-sha256 7ab66a7fc8a90cf92d026d0ba1abaa23461b10a3bbd79d003ee4a33961eb3b76 --work $S`), verify the freeze commit precedes the landing and every control receipt is a freeze blob, and test at least four forgery variants of your own (an unlabelled in-scope edit; an out-of-scope edit; a map row whose `new` text differs from the label; a label whose anchor is out of range). State for each whether the frozen limbs kill it and name the limb. Check the frozen target arithmetic against the printed base and after rates; check P3's one-path claim with `git diff-tree --no-commit-id --name-only -r {C1LAND}`. Verdict: C1 STANDS or FALSIFIED on the frozen predicate."""),

    item("CriticClaimsC2", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/CriticClaimsC2; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Attack C2's frozen predicate P1-P3 at the C2 landing {C2LAND}: re-run the frozen counter in a fresh `git clone --shared` of the landing at three seeds (the printed run-time one, 1 and 9191) with `--instrument-sha256 7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5 --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`; verify the landed scanner sha256 equals the pin and the landing diff is exactly two paths; verify the landed SCORECARD row equals the frozen candidate row byte-for-byte. Then test the counter's new guards yourself: a path-keyed forgery (hardcode the round-92 plant paths), an instrument that detects `glpat-` plus any 3+ characters, and a JWT-segment floor of 1; each must be rejected by a limb, and you name which. Report any clause of the frozen statement the counter does not bind. Verdict: C2 STANDS or FALSIFIED on the frozen predicate."""),

    item("ExecC1Indep", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ExecC1Indep; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent byte check of C1 at {C1LAND}, importing no counter code: build the base and after trees with `git archive` into $S, then for each of the 8 label rows in .ufo/waves/round-93/c1/labels.tsv reconstruct the expected line edit yourself from the label (kind, key, label text) and compare with the after tree's line. Report: per-row `line key kind expected==after`, the exact set of changed lines between base and after (should be 5), that the 3 no-edit rows are unchanged, that every old token occurs exactly once on its base line, and that no other line changed. Also independently recount the knowledge meter's class sets (resolved vs GONE distinct backticked tokens over corpus/knowledge) by your own extractor over the two trees and say whether the printed 1007/2001 and 1009/2000 hold. Verdict AGREE or DISAGREE with the arithmetic and the byte set."""),

    item("ReviewC1Labels", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ReviewC1Labels; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Hand-read the 8 round-93 label rows and the 5 landed edits at {C1LAND} against the cited bytes. For each landed row say CORRECT / PARTIAL / WRONG with the cited line quoted and the reason: 437 and 438 whole-cell repairs (does the new cell keep the errata sentence true at the anchor it names? open corpus/knowledge/intake-surface.md:89-93 and mission-control.md:55-57), 454's second token (does SKILL.md:827-848 hold the EV formula and the UNKNOWN fail-closed sentence, and is SKILL.md:494-506 really the park-disposition text?), and 58/144 (is SKILL.md:191 the only attempts statement; does `MAX_ATTEMPTS` occur 0 times in SKILL.md?). For the 3 no-edit pairs say whether leaving them bare is right. Then write the next tranche's non-author labels to .ufo/waves/round-93/w1/ReviewC1Labels-receipts/round94-labels.tsv (same 5-column schema: line, key, label, fix, evidence) for any still-stale lane-root `SKILL.md:N` ties you find in corpus/knowledge, or a file that records zero findings. Verdict: X CORRECT / Y PARTIAL / Z WRONG."""),

    item("ReviewC2Scanner", "reviewer", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ReviewC2Scanner; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Read the landed scanner at {C2LAND} and the source capture corpus/source-snapshots/round-93/S139.txt. Check clause by clause against the frozen C2 statement: the `glpat-` + exactly 20 [A-Za-z0-9_-] value, both boundaries, the escape-terminator family list, the two new known-limit lines (encoded separators, other GitLab prefixes), and that no round-87..92 sentence became false. Verify the S139 quote at line 87 really states the 20-character length and that the page states no alphabet (quote the line). Enumerate the knowledge entries that cite capture-secret-scan.py by line (`grep -rlE 'capture-secret-scan\\.py:[0-9]' corpus/knowledge`), and list every citation whose line numbers the landing shifted, with old and new bounds. Write a machine-readable reanchor table to .ufo/waves/round-93/w1/ReviewC2Scanner-receipts/reanchor-r93.tsv (columns: path, old, new, quote). Verdict: APPROVE / REQUEST-CHANGES with each defect numbered."""),

    item("MutC1Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/MutC1Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Mutate the frozen round-93 C1 counter {FREEZE}:../.ufo/waves/round-93/c1/knowledge-meter.py (use {LANE}/.ufo/waves/round-93/c1/knowledge-meter.py) one change at a time and run every mutant against the landed state ({C1LAND}) and against each control variant you can rebuild from .ufo/waves/round-93/controls/c1-controls-r93.txt (the counter's own selftest style: at least 12 mutants). Targets: the new `cell-repair` old/new derivation; the lane-root value binding (M4) and range check (M5); the M3 labelled-file union; M10 pair completeness; the EXCLUDED empty set; the M6 pin. For each mutant record: killed by which limb/control, or SURVIVOR with the exact input that proves it. Survivors are routed defects for round 94, not claim re-scores. Write the mutant table to .ufo/waves/round-93/w1/MutC1Counter-receipts/mutants.tsv and a proposed-controls list for the survivors. Verdict: killed=X survivors=Y."""),

    item("MutC2Counter", "mutation-tester", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/MutC2Counter; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Forge the frozen round-93 C2 counter at the landed state ({C2LAND}): the counter plants values under a run-time nonce and carries U1-U6; try to make it pass with an instrument that does not really detect the two new classes. Build at least six forgeries of your own: (1) a path-keyed table over the round-92 fixed paths, (2) a detector gated on a harness marker (its own tempdir/work names), (3) `glpat-` + any 3 characters, (4) `ghp_` after an escape but with a 3-character tail, (5) a detector that reads the K4 plant literals from its own source, (6) the candidate scanner with its selftest sabotaged. Run each through the frozen counter pinned and unpinned, at two seeds, in a fresh clone. Record which limb rejects each, or SURVIVOR with the run output. Also probe the counter's own nondeterminism: does the nonce reach every plant path (grep the run output), and is the seed printed. Verdict: forged=X rejected=Y survivors=Z."""),

    item("SentinelEscape", "sentinel", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/SentinelEscape; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Adversarial probe of the landed scanner at {C2LAND} (run a copy beside that rev's claim-package-check.py and capture-secret-allow.tsv). Fixtures are one file each, generated in your scratch, never real values. Measure and tabulate: (a) at least 12 encodings around `glpat-` (JSON \\t/\\u0020/\\u0026, %20/%3A/%2F/%26, HTML entities, BOM, CRLF, YAML/JSON keys, .git-credentials form, double-encoded separator) and say DETECTED/MISSED with the reason; (b) the escape-terminator family for `github-token` including the r92 P1 eleven; (c) false positives: documentation example values, the S139 page text, a 20-character run after a bare `glpat-` in prose, and a 21-character value; (d) ReDoS timing on a 1 MB worst-case line. Do not widen anything yourself. Every miss that the frozen statement does not name is a routed defect for round 94; name the closest remediation you measured, without editing the instrument. Write the probe table to .ufo/waves/round-93/w1/SentinelEscape-receipts/probes.tsv. Verdict: probe count, DETECTED/MISSED/FP counts, timing."""),

    item("ScoutGitLab", "scout", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ScoutGitLab; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Per-surface reconnaissance on the GitLab source, frozen: do NOT edit corpus/. Re-fetch https://docs.gitlab.com/user/application_security/secret_detection/detected_secrets/ and compare its bytes with the committed capture corpus/source-snapshots/round-93/S139.txt (report whether the fetched text equals the capture; if it differs, quote the differing lines). Find every statement on the page about the `glpat-` format and the 20 characters, list the page's own line numbers, and say whether it states an alphabet or a total length. Open at least two other first-party GitLab pages that might state the format (secret detection rules, personal access tokens, token prefixes) and record for each: URL, HTTP status, whether `glpat` and a length statement occur, and a located quote or the absence. Also record GitLab's other token prefixes mentioned on the detection page. Deliver a ranked lead list for round 94 with the exact quote each lead rests on. Verdict: capture-equal=yes/no, new leads=N."""),

    item("ConnectorOverlap", "connector", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ConnectorOverlap; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Sibling-overlap scan, read-only, across /home/vgpnk/Projects/shokunin/*-shokunin: find every credential scanner or pattern list in the sibling lanes (kagi, kengaku, chousa, tabi, souji, and any other lane with a scanner) and record for each whether it detects (a) `glpat-` with a length bound, (b) a GitHub token after an escape terminator, (c) the round-92 GitHub shapes. Within kasegi, check whether `capture-source.py`'s intake gate inherits the two new shapes through `patterns()` at the landing. The report names each lane, file:line (absolute), the pattern text, and the gap class. This is adjacency evidence, not a score move. Verdict: lanes scanned=N, glpat detectors=M, escape-aware=K."""),

    item("CriticHarm", "critic", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/CriticHarm; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
No-harm audit of both landings ({C1LAND}, {C2LAND}) across the other axes and the old capabilities. Measure: (1) depth:density — `python3 corpus/instruments/density.py SKILL.md --label r93` and confirm SKILL.md is byte-identical between {BASE} and the tip; (2) false positives — run the landed scanner `--rev {C2LAND}` and `--files` over every knowledge entry and source snapshot, report hits/allowed/unused; (3) ReDoS — time the landed scanner on a 1 MB line of near-miss prefixes (glpat- + 19 chars, ghp_ + 35 chars) and report ms/MB; (4) old capabilities — run the round-92 C2 counter (frozen bytes at {FREEZE}:.ufo/waves/round-92/c2/capability-check.py) against the landed state and report K limbs; (5) C1 class movement — count GONE/resolving distinct tokens in corpus/knowledge at base and landing and say whether the repair lost any resolving citation; (6) the intake gate still refuses a planted github token and a planted glpat token through capture-source.py (use a scratch out path and the committed allowlist). Verdict: NO HARM / HARM with each item numbered."""),

    item("ScribeEntry", "scribe", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ScribeEntry; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Draft (do not commit) the round-93 evidence prose the L1 will integrate, checked against committed bytes: (1) the S139 SOURCES row and the row-change bullet already at {FREEZE} — verify every cell against the capture (URL, kind, tier, scope, anchor line numbers, quote, status, used-by) and list any cell that does not match; (2) the C2 capability-row text at {C2LAND} — verify it names `gitlab-pat`, the escape boundary, S139, and keeps first-working round 87; (3) a `## Gate` block for corpus/lessons/round-93.md in the lane's form: S139 URL, access date 2026-11-07, the located quote at S139.txt:87 with its word count, capture sha256, the row change queued->mined/used-by, and one rejected candidate with its reason (the PAT profile page: no `glpat` occurrence). (4) a LOG.md Round 93 bullet set in the lane's existing style. Write all four to .ufo/waves/round-93/w1/ScribeEntry-receipts/drafts.md with a per-item PASS/DEFECT line. Verdict: drafts=4 defects=N."""),

    item("ExecC2Probe", "executor", f"""Scratch S=/fast/scratch/hyaku/kasegi-r93/ExecC2Probe; mkdir -p $S; trap 'rm -rf -- "$S"' EXIT. cd {LANE}.
Independent end-to-end probe of the landed scanner at {C2LAND}, no counter import. Build a fresh fixture repo in $S (assert its toplevel) with: one `glpat-` value in prose, one in JSON, one after a \\t escape, one after %20; plus negatives (19 chars, 21 chars, glrt-, bare prefix, letter-prefixed, post-escape with a trailing `_`); run `--rev HEAD` and `--files` on the same files and report the exact HIT lines and summary; confirm the 4 S139 allowlist rows bind only the exact matched values by re-scanning corpus/source-snapshots/round-93/S139.txt with the committed allowlist and again with the rows removed (scratch copy of the allowlist); run `--selftest` and report the case count and result. Also confirm the intake gate refuses a planted `glpat-` capture through capture-source.py with the committed allowlist (scratch out path). Verdict: rev_hits=.. files_hits=.. selftest=.. intake=refused/allowed."""),
]

spec = {
    "wave": "kasegi-r93-w1",
    "milestone": "round-93 attempt 1: C1 tranche 8 (5 label-named edits, cell-repair + lane-root kinds, meter 1007/2001 -> 1009/2000) and C2 capture-secret-scan gitlab-pat + escape boundary (S139); attack, verify, draft",
    "reportDir": ".ufo/waves/round-93/w1",
    "maxLanes": 16,
    "axes": ["depth:verifiability", "coverage"],
    "context": CONTEXT,
    "items": ITEMS,
}
print(json.dumps(spec, indent=1, ensure_ascii=False))
