#!/usr/bin/env python3
import json, sys
sys.path.insert(0, '/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39')
import items1

LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET="/home/vgpnk/Projects/shokunin"
W=f"{LANE}/.ufo/waves/round-39"
BASE="480b1a505a2dfc14a4f718d16d63808247214d0a"
FREEZE="dcd31701720a6a4929a32471a62011ed87103421"

CONTEXT = f"""# Round
kasegi-shokunin round 39, dispatched by the L1 (agent KasegiR39) via the inline spawn handoff (hyaku run 9). Lane repo {LANE} is the ONLY lane repo. The fleet root {FLEET} is read-only to you — never write there. /home/vgpnk/Projects/shokuknow is read-only — never write there, never run its campaign tools. Base commit {BASE}; claims-freeze commit {FREEZE}; frozen claims at {W}/claims.json (read it first; do not edit). Before-controls: {W}/c1-controls/before.txt, c2-controls/before.txt, c2-controls/junk-f22.md, census-before.txt.

Frozen claims (summary; claims.json is authoritative):
- C1 depth:verifiability (score 4, held): new committed suite corpus/instruments/r39-closure.sh, export mode only (`--export-ref <hash>` -> `git -C <lane> archive <hash> | tar -x` into a work dir outside the lane; plain run exit 2; `--selftest` with GRADED case lines), prints `closed=8/8 exit=0` on the round-39 judged head J and `selftest cases=8 failures=0` with every case line `positive=pass ... verdict=pass`; base {BASE} and r38 judged head 66703aca50529a35be49aa8759d04140720ad exports print closed<8/8 exit=1. Checks: G1 whole-tail declared blocks = added lines, backtick+tilde fence walk, corrections only outside fences, declared paths exist in export; G2 all-gates v3 receipt with export-ref J, diff J..REF only the receipt, digest bound, exactly eight graded selftest case lines, no summary-only line counts; G3 every quoted `--export-ref <hash> -> closed=K/K` result in lane files has a committed transcript or is labeled report-only; G4 results.json seat identities distinct and == task count, zero-task dispatch RED; G5 no `Final lane commit:` line in round-39 section, judged head by reference only; G6 scratch quiescence live (kasegi-r37/r38 empty-or-absent; r39 holds only its own --work); G7 considerthese ledger round-39 dispositions section filled; G8 pinned r37-closure.sh bytes at 2387dcf6 (git show), 14/14 green, export copy must hash to pinned digest.
- C2 coverage (score 7, held): frontier F22 = CISA, When to Issue VEX Information (issuance/lifecycle/reaffirmation/inheritance layer beyond the CSAF VEX profile); registry S057 (https://www.cisa.gov/resources-tools/resources/when-issue-vex-information, tier A, kind docs, mined, opened 2026-10-26, NF=13, capture corpus/source-snapshots/round-39/S057.txt + manifest.json); rejected rows S056 (CISA Minimum Requirements), S058 (OpenVEX v0.2.0), S059 (CycloneDX v1.7 analysis) with reason+flip; entry corpus/knowledge/cisa-when-to-issue-vex.md (`source: S057`); harness entries=25 pass=25 incl PASS F22 ids=S057; binding 46/46; recheck-audit expected=51; census exit 0 (W04 S028/S029 only); knowledge 50->51; junk twin c2-controls/junk-f22.md rejected by source-recheck (exit 1).

Read your item spec below fully before acting. You are a leaf seat (no subagent spawning, except one read-only labrat probe allowed for executors). Work only your item. No placeholders or plan text — land real evidence: commands you ran with their actual output.

Write scope. Your ONLY allowed writes are (1) your receipt at {W}/wave1/<SEATNAME>.md (write it last), (2) byte-exact deliverable files your item names, written beside the receipt as {W}/wave1/<SEATNAME>.<suffix> (for example `ExecSuiteBuild.r39-closure.sh`), and (3) scratch under your scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit any other file in the lane repo, the fleet repo, sibling lane repos, or source trees (/home/vgpnk/Projects/shokuknow, ~/Projects/*). Never run a mutating git/jj command anywhere (no add/commit/push/checkout/reset/stash, no jj commit/new/describe/squash/rebase/abandon/bookmark/undo); read-only git is fine. Never edit MANIFEST.json, templates/, scripts/ (fleet), .ufo/state/, .ufo/watchdog.log, .scratch/, or any sibling repo.

Deliverable discipline (round-37 defect D-A: a scribe receipt's scaffolding was pasted into PROVINCE.md/README.md). When your item delivers text the L1 will land, put ONLY the landable bytes in the deliverable file (or, if your item says receipt-only, inside ONE fenced block headed `## DELIVERABLE`) — no validation tables, no notes, no headings that are not part of the landed text. Put validation evidence in the receipt, outside the deliverable. Give the deliverable's line count and sha256.

Scratch. Create S=/fast/scratch/hyaku/kasegi-r39/<SEATNAME>/ with mkdir -p and bind ALL scratch/work copies there (TMPDIR=$S, --work under $S); never rely on an inherited TMPDIR; /tmp only for files under 50 MB. Remove your scratch dir before you yield (`trap 'rm -rf -- "$S"' EXIT` in shell; `finally: shutil.rmtree` in Python), after copying receipts/deliverables into the wave dir. A seat whose scratch dir survives is a round-39 defect (G6 checks it live). Do not run a heavy pass while the disk guard is not green: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`.

Tooling. Tooling authorization (operator 2026-10-19): you may install/upgrade tools that help the task, after reading /home/vgpnk/.omp/agent/RULES.md (official channels only; record tool/version/channel/reason in your receipt). pacman transactions are PAUSED host-wide — never run pacman (no -S/-Sy/-Syu/-U/-R); use `uv tool install`, `npx`, or an official binary into ~/.local/bin instead; if pacman were ever needed, `pacman -Sp --print-format '%n %v' <pkgs>` dry-run first and only for not-installed packages. Never edit ~/.omp/agent/config.yml or ~/.omp/agent/mcp.json (operator-owned). Never restart a host service.

Host guard (SEAT_GUARD). Your tools start at the fleet root: cd to your scratch first and use absolute paths for every read/write. If you build a git fixture, create it as D=$(mktemp -d) && git -C "$D" init -q and verify `git -C "$D" rev-parse --show-toplevel` equals "$D" before any commit; never use a throwaway git identity anywhere else. Never write to any PATH directory (~/.local/bin, /usr/bin). Never write fleet-root tracked files (LOG.md, SCORECARD.md, PROVINCE.md, SHONEN.md, SKILL.md, corpus/*, MANIFEST.json at the fleet root).

Rules. Keep moves that improve an axis and harm none. Do not message agent://all. Do not run your own swarm. A seat keeps the route chain it captured at spawn. Network fetches: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; record HTTP status, bytes and the UTC fetch time. Godspeed posture governs your work: name the axes, iterate cheap in parallel, keep moves that improve any axis and harm none, never stall in clarifying-question loops."""

items = []
for it in items1.ITEMS:
    body = it["body"].replace("{W}", W)
    items.append({"name": it["name"], "role": it["role"],
                  "axes": ["depth:verifiability"] if it["role"] in ("executor","reviewer","critic","mutation-tester") else (["coverage"] if it["role"]=="scribe" else ["depth:verifiability","coverage"]),
                  "milestone": "round-39", "prompt": CONTEXT + "\n\n" + body})

spec = {"wave":"kasegi-r39-build","reportDir":".ufo/waves/round-39/wave1","maxLanes":64,
        "axes":["depth:verifiability","coverage"],
        "milestone":"round-39 build wave 1: C1 r39 suite + C2 F22 S057 capture/rows/entry; controls and corrections",
        "context":CONTEXT, "items":items}
json.dump(spec, open(f"{W}/wave1-spec.json","w"), indent=1)
print("spec items:", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
