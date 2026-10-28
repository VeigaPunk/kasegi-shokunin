# Round-44 non-author spot-check packet — kasegi (for the closure, not for the lane)

This packet hands the closure the two decisions the round-44 C2 claim rests
on: one **admit** and one **reject** from the source set opened this round. A
seat dispatched by this lane is still the lane (LEARNING.md), so the
adjudication belongs to the non-author closure; the lane prepares the packet
and does not grade itself.

Every line below is re-grounded by this lane on 2026-10-28 — the URL, the
access date, the located quote and the pinned bytes are the lane's own, taken
from the round-44 capture, not from a campaign record.

## Decision 1 — ADMIT: S069 (tier A, `mined`) → F26

- registry row: `corpus/SOURCES.md`, id `S069`
- url: `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`
- accessed: 2026-10-28 (official article API fetch; `http.final_url` recorded in
  `corpus/source-snapshots/round-44/manifest.json`)
- pinned bytes: `corpus/source-snapshots/round-44/S069.txt` — 45 681 bytes,
  1 132 lines, sha256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`
- located quote (≤25 words): "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services." — `corpus/source-snapshots/round-44/S069.txt:61`
- supporting anchors: customer-resource testing prohibited (`:62-63`); reward
  ineligible when finding or verifying involved customer resources (`:70-72`);
  a Google-owned asset inside a customer IP range is still unauthorized testing
  (`:76-77`); a service handling reasonably sensitive user data is in scope
  (`:10-11`)
- admitted as: frontier row `F26` in `corpus/README.md`, knowledge entry
  `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`
- the question for the non-author: does the entry stay inside the program
  boundary (no general authorization rule), and does the rejected
  overgeneralization (a Google-owned asset inside a customer IP range is not
  thereby authorized) actually appear in the entry?

## Decision 2 — REJECT: S070 (tier C, `rejected`)

- registry row: `corpus/SOURCES.md`, id `S070`
- url: `https://bughunters.google.com/about/rules/about-this-section`
- accessed: 2026-10-28
- located text: the accessible body is a JavaScript shell; the metadata is a
  directory welcome only — there is no quotable rule text to anchor a knowledge
  entry
- reason for rejection: a directory shell carries no rule that could support a
  boundary entry; nothing is admitted from it
- flip condition: a readable, dated copy of the rules directory that carries a
  quotable rule text
- the question for the non-author: is the rejection right, and is the flip
  condition specific enough to be re-checked?

## How to run the spot-check

1. Re-open both URLs (live) and locate the quotes above; a quote that cannot
   be located refutes the admit.
2. Read `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` and
   decide admit / reject for the F26 entry, naming the reason.
3. Re-check the SOURCES rows: `python3 corpus/instruments/recheck-audit.py`
   (expects `63/63`), `python3 corpus/instruments/source-recheck.py --manifest
   corpus/source-snapshots/round-44/manifest.json --source S069` (expects Q1–Q5
   pass), `python3 corpus/instruments/frontier-recheck-count.py` (expects
   `entries=29 pass=29`).
4. Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
   --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 (the two `W04`
   duplicate-URL warnings are pre-existing).

The lane's own receipts for the same checks are under
`.ufo/waves/round-44/controls/`; they are the lane's claim, not the verdict.
