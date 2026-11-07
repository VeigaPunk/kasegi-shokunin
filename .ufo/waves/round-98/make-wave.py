#!/usr/bin/env python3
"""Build the kasegi round-98 w1 wave spec (13 seats, one v1 wave).

Usage: python3 -B .ufo/waves/round-98/make-wave.py --base <rev> --freeze <rev> \
         --c1 <rev> --c2 <rev> --census-rev <rev> --out .ufo/waves/round-98/w1-spec.json
"""
import argparse
import json

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"


def context(a):
    return """# Goal
Kasegi round 98, attempt 1, ONE v1 wave of 13 seats. Two frozen claims, both already landed before this wave was dispatched. Base `%s`, freeze `%s`, C1 landing `%s`, C2 landing `%s`. Frozen statements, predicates, kill rules, sha256 pins and every executed pre-freeze control: `%s/.ufo/waves/round-98/claims.json` and `%s/.ufo/waves/round-98/controls/`.

C1 `depth:verifiability` (lowest axis, score 4) — the citation census of record becomes a reading of a named revision. `corpus/instruments/census-at-rev.py` extracts `git archive REV`, runs the extract's own `corpus/instruments/resolve.py`, and `--check` re-measures the revision the census file's `measured-at:` line names. The regenerated census records `measured-at: %s`, pinned (INTERNAL-only) SKILL 162/732, corpus 2550/7556, lane 2588/7958, host-owned 78, and the host-inclusive SKILL 166/732. Before: the committed census recorded SKILL 132/701 with no revision and a 224-file scope.

C2 `coverage` (score 8 held; capability extension `capture-secret-scan`) — four further S140 rules (`gitlab-ci-build-token` S140:293, `gitlab-iam-refresh-token` S140:480, `gitlab-iam-authorization-code` S140:497, `gitlab-session-cookie` S140:549-551) and S140's own punct/space/EOL right boundary for the five round-97 shapes that refused a real token followed by `_` or `-`; selftest 148 -> 170; every plant value generated from the rule grammar, not copied from the selftest.

# Absolute paths (seat tools start at the fleet root)
Lane repo: `%s` — every lane path below is relative to it. Every `Report:` trailer path is relative to `%s` — write it at `%s/<that path>`.

# Scratch discipline
`S=/fast/scratch/hyaku/kasegi-r98/<YourSeatName>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`. Every clone, mirror, work tree and fixture lives under `$S`; one live clone per seat (`git clone --shared` or `git archive`), never a full mirror; never write under `/tmp` (files under 50 MB only); remove your scratch dir before you yield, receipts first copied into your Report dir.

# Bounds
You are a read-only attacker/verifier: never commit, push, or run a mutating git/jj command in the lane repo; never write the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, or `MANIFEST.json`. Write only your Report file and its `-receipts/` directory under `%s/.ufo/waves/round-98/w1/`. Any fixture repo is created with `D=$(mktemp -d)` and every git call names `-C "$D"`; assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never pass an empty or unchecked variable to `git -C`.

# Tooling
You may install or upgrade tools that help the task (read `/home/vgpnk/.omp/agent/RULES.md` first: official channels, update-safety gate; record tool/version/channel/reason in your report). **pacman transactions are PAUSED host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question. Never mutate host sysctls.

# Depth
An executor seat may spawn one read-only `labrat` probe for a falsifiable hypothesis; every other role is a leaf and runs no swarm.

# Output
Your report is the evidence: every claim about the code carries the command you ran and its observed output (or the exact `file:line`). Never fabricate; an unrun check has not passed. End with one `VERDICT:` line per item you were asked to judge.
""" % (a.base, a.freeze, a.c1, a.c2, LANE, LANE, a.census_rev, LANE, LANE, LANE, LANE)


def seat(name, body):
    return (GODSPEED + "\nScratch S=/fast/scratch/hyaku/kasegi-r98/" + name +
            "; mkdir -p $S; trap 'rm -rf -- \"$S\"' EXIT. cd " + LANE + ".\n\n" + body)


def items(a):
    return [
        ("CriticClaimsC1", "critic", seat("CriticClaimsC1", """Attack C1's frozen predicate P1-P3 at the C1 landing `%s`. Re-run `python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work $S/w` in a fresh `git clone --shared` of the lane at the landing; then try to make it pass while the census is wrong: (a) a census whose pinned line matches but whose body was hand-edited; (b) a census whose `measured-at` is a revision the file was not generated from; (c) a `measured-at` that is not an ancestor of the branch tip; (d) a census generated from a tree with one knowledge file removed. For each: what the check prints, and whether P1/P3 still holds. Report STANDS or DOES-NOT-STAND per limb with the exact output.""" % a.c1)),

        ("CriticClaimsC2", "critic", seat("CriticClaimsC2", """Attack C2's frozen predicate K1-K7 at the C2 landing `%s`. Re-run `.ufo/waves/round-98/c2/capability-check.py --lane . --rev <landing> --work $S/w --instrument-sha256 <pin> --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` with your own seed, twice. Then attack the independence claim: build a literal-locked matcher that accepts only the instrument's own selftest literals and run K3's plants against it; build a matcher that drops the session-cookie context requirement and see whether K3's n10 negative kills it. Report which limbs are real and which are passable by a wrong instrument.""" % a.c2)),

        ("CriticHarm", "critic", seat("CriticHarm", """Harm audit for the round: base `%s` -> C1 `%s` and C2 `%s`. Check that `SKILL.md`, `PROVINCE.md`, `SHONEN.md` and `AGENTS.md` are byte-identical base->landing; that `capture-secret-scan.py` loses no earlier shape (compare `patterns()` at base and landing); that the round-94 receipt redaction preserves line count and every other byte; that the census numbers are not gamed (the pinned numerator is INTERNAL only, and no knowledge file was edited to move it); and that no earlier knowledge entry's citation of `capture-secret-scan.py:N` is now out of range. Report HARM or NO HARM with the commands.""" % (a.base, a.c1, a.c2))),

        ("ReviewC1Census", "reviewer", seat("ReviewC1Census", """Review `corpus/instruments/census-at-rev.py` at the C1 landing `%s` line by line. Independently re-derive the pinned numbers with your own script over a `git archive %s` extract (do not import the lane's instrument): count distinct backticked path-like citations per scope and the INTERNAL-only numerator, and compare with the census header. Check: the cache cannot mask a wrong measurement (a cache entry for a revision must not be reusable for another revision); the body is resolve.py's own output (compare against a fresh resolve.py run on the same extract); the host-owned line is a count of RESOLVES+MIRROR-EQUIVALENT distinct citations. Report the numbers you got and every discrepancy.""" % (a.c1, a.census_rev))),

        ("ReviewC2Scanner", "reviewer", seat("ReviewC2Scanner", """Review the C2 landing `%s` of `corpus/instruments/capture-secret-scan.py` against `corpus/source-snapshots/round-94/S140.txt` lines 291-294, 478-481, 495-498 and 547-551, and against S140's right boundary class `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)`. For each of the four new shapes check alphabet, exact length, separator and boundary character by character; for each of the five widened shapes check that `(?![A-Za-z0-9])` is exactly S140's class. Then check no earlier shape regressed (run the selftest and compare the case list at base and landing). Report APPROVE or REQUEST-CHANGES with findings F1..Fn.""" % a.c2)),

        ("MutC1Counter", "mutation-tester", seat("MutC1Counter", """Mutation-test the round-98 C1 control set. Build at least ten single-point mutants of `corpus/instruments/census-at-rev.py` (drop the `measured-at` regex, accept any revision, drop the pinned-line comparison, compare only SKILL, drop the host-owned line, accept a missing pinned line, key the cache by lane instead of revision, read the body from the live lane, accept a 12-character revision, ignore the resolve.py exit code). Run the frozen control harness `.ufo/waves/round-98/controls/c1-controls-r98.py` against each mutant (copy the mutant into a fixture clone; never edit the lane). Report killed/survivors with the limb each mutant escapes, and name any survivor as a routed gap.""" )),

        ("MutC2Counter", "mutation-tester", seat("MutC2Counter", """Mutation-test the round-98 C2 shapes and gate. Build at least ten single-point mutants of the landed `corpus/instruments/capture-secret-scan.py` (drop each of the four new shapes, narrow each of the five widened boundaries back to `(?![A-Za-z0-9_-])`, drop the session-cookie context requirement, change a `{43}` to `{42}`, drop the `_` separator in the ci-build grammar, widen the session hex to `[0-9a-fA-F]`). Run the instrument's `--selftest` and the gate's K3 plants against each mutant in a fixture clone. Report killed/survivors; a mutant the selftest kills but K3 does not (or vice versa) is a coverage gap to name.""" )),

        ("SentinelShapes", "sentinel", seat("SentinelShapes", """Security review of the nine shapes at the C2 landing `%s`, read as an attacker who wants a real token to pass unseen. Build a matrix of at least 120 payloads across the four new shapes and the five widened ones: separators (`_`, `-`, `.`, `;`, `&`, `%%26`, `\\u0026`, `&#x26;`), contexts (JSON value, header, cookie, URL query, markdown cell, log line, git remote), case variants, one-character length over/under, boundary characters, and the session-cookie context at line start/after a quote. Run each through the landed `scan_bytes` and a faithful translation of the cited S140 regexes. Report MUST-FIX findings (a real token the scanner misses that S140 detects) separately from routed qualifiers.""" % a.c2)),

        ("ExecC1Indep", "executor", seat("ExecC1Indep", """Independent re-derivation of C1's numbers, without importing the lane's instrument. (1) Write your own census of distinct backticked path-like tokens in `SKILL.md` + `corpus/**/*.md` (excluding `corpus/instruments/citation-survival.md`) over a `git archive %s` extract, classify lane-relative tokens that exist in the extract as INTERNAL, and print the per-scope totals. (2) Compare with the census header's pinned line. (3) Re-run the lane's `census-at-rev.py --check` and report both readings side by side. Report AGREE or DISAGREE with the delta.""" % a.census_rev)),

        ("ExecC2Probe", "executor", seat("ExecC2Probe", """Independent probe of the nine shapes at the C2 landing `%s`. Write your own fixture generator (not the gate's) that builds 21 positives (four new shapes x 3 variants, five widened shapes x 2 boundary variants) and 21 boundary negatives, in a scratch git repo with nonce-derived paths, and run the landed `capture-secret-scan.py --files` over them. Report the exact hit set, every miss and every extra hit. Then run the round-97 instrument at `a9a53608` over the same files and report which of the nine shapes it misses (the before state).""" % a.c2)),

        ("ScoutSources", "scout", seat("ScoutSources", """Source reconnaissance for the round. (1) Re-open S140: fetch `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/raw/59ada1f4ca53d5a69fafb9cb0f10bb893720ce39/rules/mit/gitlab/gitlab.toml` (record HTTP status, bytes, sha256) and compare the four cited lines (291-294, 478-481, 495-498, 547-551) with the committed capture `corpus/source-snapshots/round-94/S140.txt`; report the line offset between the live file and the capture (the round-97 spot-check's routed defect 5). (2) Re-open S144 `https://docs.gitlab.com/security/tokens/` (status, bytes, sha256) and confirm the `glcbt-` and `_gitlab_session=` rows. (3) Report whether any new row is warranted (a page that states the IAM token formats); do not write SOURCES.md.""" )),

        ("ConnectorOverlap", "connector", seat("ConnectorOverlap", """Sibling-overlap scan (read-only). Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/` (kagi, chousa, kengaku, kotoba, kumitate, tamesa, tsukuroi, mori, kama — whichever exist) for the four new shape ids (`gitlab-ci-build-token`, `gitlab-iam-refresh-token`, `gitlab-iam-authorization-code`, `gitlab-session-cookie`), for `census-at-rev`, and for the S140/S144 source ids. Report every hit with path:line and say whether it is a duplicate implementation, a citation, or a contested-scope claim. Write nothing outside your report.""" )),

        ("ScribeGate", "scribe", seat("ScribeGate", """Draft the round-98 lesson's `## Gate` block and verify the integration text. Read `.ufo/waves/round-98/claims.json`, the control receipts under `.ufo/waves/round-98/controls/`, `corpus/SOURCES.md` rows S140 and S144, `corpus/QUALITY.md` (the round-97 additions R153/R154), and `SCORECARD.md`'s capability row. Check: every number in the draft Gate block is re-derivable from a receipt you ran or read; the S140/S144 `used-by` cells list the two new knowledge entries; the lesson's `## Mistakes` rows each carry class, evidence pointer, captured-by and fix; and no `PENDING-L1`/`TBD`/`TODO` marker sits in the Gate body (R133). Write your draft as `%s/.ufo/waves/round-98/w1/ScribeGate.md` with a `GATE-DRAFT:` block the L1 can paste, and list every discrepancy you found.""" % LANE)),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--c1", required=True)
    ap.add_argument("--c2", required=True)
    ap.add_argument("--census-rev", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = {
        "wave": "kasegi-r98-w1",
        "milestone": "round-98 attempt 1: C1 revision-pinned citation census (measured-at %s, pinned SKILL 162/732) and C2 four further S140 shapes plus five widened boundaries (selftest 148 -> 170); attack, verify, draft" % a.census_rev,
        "reportDir": ".ufo/waves/round-98/w1",
        "maxLanes": 16,
        "axes": ["depth:verifiability", "coverage"],
        "context": context(a),
        "items": [{"name": n, "role": r, "prompt": p} for n, r, p in items(a)],
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1)
    print("wrote %s items=%d" % (a.out, len(spec["items"])))


if __name__ == "__main__":
    main()
