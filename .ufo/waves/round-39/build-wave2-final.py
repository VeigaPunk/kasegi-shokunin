#!/usr/bin/env python3
import json, sys
sys.path.insert(0, '/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39')
import items2

LANE="/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET="/home/vgpnk/Projects/shokunin"
W=f"{LANE}/.ufo/waves/round-39"
BASE="480b1a505a2dfc14a4f718d16d63808247214d0a"
FREEZE="dcd31701720a6a4929a32471a62011ed87103421"

CONTEXT = f"""# Round
kasegi-shokunin round 39, wave 2 (falsify), dispatched by the L1 (agent KasegiR39) via the inline spawn handoff (hyaku run 9). Lane repo {LANE} is the ONLY lane repo. The fleet root {FLEET} is read-only to you — never write there. /home/vgpnk/Projects/shokuknow is read-only — never write there, never run its campaign tools. Base commit {BASE}; claims-freeze commit {FREEZE}; frozen claims at {W}/claims.json (read it first; do not edit) and claims-erratum-1.md (E1 registry after-count 59; E2 r38 judged head full hash; E4 verification ref Y = J + receipt; E5 non-vacuous measurement semantics). Wave 1 landed the C1 suite and the C2 artifacts; your attack targets are the LANDED bytes in the lane tree (read them at HEAD) plus the frozen predicates in claims.json. You are an ATTACK seat: your job is to falsify the claims as frozen, find defects in the landed work, and verify the do-nothing controls; you are NOT the author of the work (a seat that wrote the deliverable under attack must say so and focus on a different item).

Frozen claims (summary; claims.json is authoritative):
- C1 depth:verifiability (4, held): r39-closure.sh suite prints `closed=8/8 exit=0` at J and graded `selftest cases=8 failures=0`; base/r38-head reds; G1 whole-tail, G2 graded receipt, G3 committed-run truth, G4 seat identity, G5 no-final-label, G6 scratch quiescence, G7 ledger fill, G8 pinned r37 bytes.
- C2 coverage (7, held): F22 S057 admission counters (frontier 22, registry 58, knowledge 51, harness 25/25, binding 46/46, audit expected=51, census exit 0, junk-f22 rejected).

Read your item spec below fully before acting. You are a leaf seat (no subagent spawning). Work only your item. No placeholders or plan text — land real evidence: commands you ran with their actual output.

Write scope. Your ONLY allowed writes are (1) your receipt at {W}/wave2/<SEATNAME>.md (write it last), (2) byte-exact deliverable files your item names, written beside the receipt as {W}/wave2/<SEATNAME>.<suffix>, and (3) scratch under your scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit any other file in the lane repo, the fleet repo, sibling lane repos, or source trees. Never run a mutating git/jj command anywhere (no add/commit/push/checkout/reset/stash, no jj mutations); read-only git is fine. Never edit MANIFEST.json, templates/, scripts/ (fleet), .ufo/state/, .ufo/watchdog.log, .scratch/, or any sibling repo.

Scratch. Create S=/fast/scratch/hyaku/kasegi-r39/<SEATNAME>/ with mkdir -p; bind ALL scratch/work copies there (TMPDIR=$S, --work under $S); never rely on an inherited TMPDIR; /tmp only for files under 50 MB. Remove your scratch dir before you yield (`trap 'rm -rf -- "$S"' EXIT`), after copying receipts/deliverables into the wave dir. Do not run a heavy pass while the disk guard is not green.

Tooling. Tooling authorization (operator 2026-10-19): you may install/upgrade tools that help the task, after reading /home/vgpnk/.omp/agent/RULES.md (official channels only; record tool/version/channel/reason in your receipt). pacman transactions are PAUSED host-wide — never run pacman; use `uv tool install`, `npx`, or an official binary into ~/.local/bin instead. Never edit ~/.omp/agent/config.yml or mcp.json. Never restart a host service.

Host guard (SEAT_GUARD). Your tools start at the fleet root: cd to your scratch first and use absolute paths for every read/write. If you build a git fixture, create it as D=$(mktemp -d) && git -C "$D" init -q and verify `git -C "$D" rev-parse --show-toplevel` equals "$D" before any commit; never use a throwaway git identity anywhere else. Never write to any PATH directory. Never write fleet-root tracked files.

Rules. Keep moves that improve an axis and harm none. Do not message agent://all. Do not run your own swarm. A seat keeps the route chain it captured at spawn. Network fetches: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; record HTTP status, bytes and the UTC fetch time. Godspeed posture governs your work: name the axes, iterate cheap in parallel, keep moves that improve any axis and harm none, never stall in clarifying-question loops."""

items = []
for it in items2.ITEMS:
    body = it["body"].replace("{W}", W)
    items.append({"name": it["name"], "role": it["role"],
                  "axes": ["depth:verifiability"] if it["role"] in ("reviewer","critic","mutation-tester") else (["coverage"] if it["role"]=="scribe" else ["depth:verifiability","coverage"]),
                  "milestone": "round-39", "prompt": CONTEXT + "\n\n" + body})

spec = {"wave":"kasegi-r39-falsify","reportDir":".ufo/waves/round-39/wave2","maxLanes":64,
        "axes":["depth:verifiability","coverage"],
        "milestone":"round-39 falsify wave 2: attack C1/C2 as frozen; verify controls; hunt defects",
        "context":CONTEXT, "items":items}
json.dump(spec, open(f"{W}/wave2-spec.json","w"), indent=1)
print("wave2 spec items:", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
