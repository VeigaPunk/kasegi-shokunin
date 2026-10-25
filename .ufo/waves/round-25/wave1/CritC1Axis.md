# CritC1Axis — is C1 depth:verifiability, and can it move the score?

Seat: `L1Kasegi25.CritC1Axis` (UFO-FSD critic, round 25 wave 1). Read-only: this file is my only
output; no production path was edited. Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.

Evidence base: frozen receipts `.ufo/waves/round-25/c1-before.json` / `c1-before.txt`, base bytes
read through `git show b49948f:corpus/knowledge/*.md`, `AXES.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-24-verifier-spotcheck.md`, and one live read of the working tree (labelled
below; it is a moving target, not a receipt).

## 1. Verifiability or operability?

**Both limbs are present, and they belong to different axes — the label is defensible only for the
smaller limb.** `AXES.md:11` defines depth as "Verifiable technical detail — decision tables with
real thresholds, named error signatures, cited sources", signal "A reader can act on SKILL.md alone;
no filler"; `AXES.md:13` defines operability as "Runnable artifacts: checklists that are executable,
commands that exist, scripts that run", signal "A checklist item can be run and produces the stated
outcome". The cwd limb (b) is verifiability: a line that exits 0 at the lane root and 2 from `/`
*does run* — it runs only under ambient state the entry never states, so the recorded evidence is
not re-derivable from the artifact alone. The parse limb (a) and the path limb (c) are operability
in its own words — "commands that exist" — and are the entry bar already written down as `QUALITY.md`
Q7 ("An executable recheck field contains a command, not prose beginning 'On each'"). The split is
not academic in this receipt: of the 29 failing lines at base, **23 fail only the operability limb
(`parse_fail=23`, all 23 being `recheck: on-restoration — <cmd> (fails closed …)` prose hybrids,
verified against base bytes) and only 6 fail the verifiability limb (`cwd_fail=6`)**; the 6 base
passes are exactly the 5 lines that already carried `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`
plus `root-loss-2026-10-12.md`, whose `test ! -e …` needs no cwd. So ~79 % of the claimed move is
entry-bar conformance, not evidence re-derivability. This matters structurally because the lane does
not score operability at all: `SCORECARD.md:4-5` — "The other four axes (operability, freshness,
calibration, adjacency) are worked by their owning lanes" — so the 23-line parse repair has no
scoring home here, and the fleet already treats portability this way (`revenger-shokunin/SCORECARD.md:84`:
"operability — not an assigned scoring axis … Portable replay is counted only under the declared
criterion, not as a second gain"). Keeping C1 on `depth:verifiability` is therefore acceptable *for
the cwd limb*, but the claim cannot present the 23 parse repairs as verifiability gain.

## 2. Does D24-5 already concede verifiability?

**Yes for the cwd limb, and its own fix menu is the proof; no for the score.** `corpus/lessons/round-24-verifier-spotcheck.md:208`
(D24-5) reads: "Residual cwd dependence: … 5 of 35 `recheck:` lines carry it, so a cold run from
another cwd still exits 2 (**the harness pins cwd, which masks it**)", fix: "Prefix the remaining
lines **or make the harness's cwd pin explicit in each entry's recheck text**". Two things follow.
First, the defect is stated as the *entry's* evidence being reproducible only under a condition the
entry does not carry — that is the verifiability question, not the operability one, and the second
fix option (document the pin, change nothing about execution) is only a fix if the axis is disclosure
of the evidence's preconditions. Second, "the harness pins cwd, which masks it" concedes something
the score must absorb: the round-24 C1 receipt was measuring a property the entry does not have, so
the harness — not the entry — supplied the ambient state. That is an instrument-honesty concession
(calibration of the receipt), and it is why re-measuring the same field with cwd unpinned is a
*correction*, not a new axis move. I confirmed the figure independently at base:
`git grep -h '^recheck: ' b49948f -- corpus/knowledge | grep -c '^recheck: cd '` → **5**, total
**35**, `^recheck: on-restoration` → **23**, matching `c1-before.json` exactly.

## 3. Score 4 → 5, or 4 held?

**4 held — the count 6 → 35 is the axis's *surface*, not its numerator, and the frozen counter does
not yet measure what a score move would need.** Three measured reasons. (i) *No registered detector
moved.* `corpus/QUALITY.md:49` (R7) states the lane's own bar and its ground: "A provenance/header
count cannot stand in for citation resolution; instrument-correctness claims must change and exercise
the actual detector … r22 C1 rejected because `resolve.py` and `anchorcheck.py` were unchanged." C1
edits 35 entry lines and adds `recheck-audit.py`; `resolve.py`, `anchorcheck.py` and
`source-recheck.py` bytes are untouched, and the verifiability score has been defined by those
detectors since r15 (`SCORECARD.md:33`, the `resolve.py` census of record). (ii) *The counter admits
degenerate passes.* I evaluated four lines against the audit's own three limbs (importing
`audit_entry`'s helpers, `root` = lane, `foreign` = `/`):

| degenerate line (fails R12 / proves nothing) | limbs parse,cwd,paths | exits lane/foreign | audit verdict |
|---|---|---|---|
| `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest … --source S999` (invalid id) | T,T,T | 2 / 2 | **PASS** |
| `cd /home/vgpnk/Projects/nonexistent-lane && python3 corpus/instruments/anchorcheck.py corpus/knowledge/ev-model.md` | T,T,T | 1 / 1 | **PASS** |
| `cd <lane> && true corpus/knowledge/ev-model.md` (R12: "a line pointing at … `true` … is not a recheck") | T,T,T | 0 / 0 | **PASS** |
| `cd <lane> && python3 … --source S018 corpus/knowledge/cvss-v4-severity-and-vector.md` (another entry's capture) | T,T,T | 2 / 2 | **PASS** |

The cwd limb compares two digests, so it is satisfied by *uniform brokenness*; and the path limb
accepts any `corpus/…` token that exists, so a command that names a real file and does nothing passes.
`pass=35` is therefore reachable with 35 `true`-shaped lines, which `QUALITY.md:66` (R12) forbids and
`QUALITY.md:65` (R11) requires the round to publish discrimination against. (iii) *23 of the 35
"passes" are consistent-failure receipts, not re-derivations*: at my live read of the working tree the
audit already printed `lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`
(siblings mid-edit; not a receipt) — 12 lines actually re-derive evidence, 23 exit 1 from both cwds
because the bases are absent. That is the claim's declared design (fail-closed lines count), but it
means the number cannot carry a score. Why 6 → 35 is nonetheless the axis's surface: `claims.json`
C1 names the surface as "the `recheck:` line of every corpus/knowledge/*.md entry (35 lines) as the
entry's own verifiability instrument", and the 35-line set is exactly the entry-granularity instance
of the axis's question ("can a reader open/redo what the entry asserts"). Repairing that surface
raises the *floor* of re-derivability — every entry now states its own location instead of relying on
the harness's cwd pin — while leaving the *ceiling* (do the cited sources open) at the unchanged
`resolve.py`/`anchorcheck.py` census. Surface repaired ≠ score moved: the lane has now held 4 through
r18, r19, r22 (headers 0/25 → 25/25, rechecks runnable 0/25 → 25/25 — the r22 verifier's
REJECTED-HONEST-STOP), r23 and r24, all with detectors moving or not, and `SCORECARD.md:71-77` already
records the split's rule that the score follows the detector, not the form.

**If the L1 nevertheless wants a mover, the predicate must be** `lines=35 pass=35 exit=0` under a
*binding* audit: each line's `--source` ids cover that entry's header `source:` ids (R12), the 12
non-fail-closed entries' lane run exits 0 and prints the capture it checked, and three degenerate
controls (`true <existing path>`, `--source S999`, nonexistent `cd`) **fail**; plus the round must
disclose that the verifiability detectors are unchanged and why that is credit anyway. Even then I
would record "improved, score held" — R7's ground is the detector, and the honest move after it is a
detector change.

## Impacted axes and smallest safe correction

- `depth:verifiability`: surface repaired (35/35 self-locating, guards preserved as `#` comments — the
  kill rule's "prefix, do not delete the fail-closed test" is satisfied). Score **held 4**.
- `operability` (not a kasegi-scored axis): the 23 parse repairs are entry-bar conformance (Q7);
  report them, do not score them here.
- `calibration`: D24-5's "the harness pins cwd, which masks it" must appear in the round's own
  receipt, or the round repeats the r24 masking.
- Regression risk introduced by the fix, disclosed not hidden: 34 of 35 lines now hardcode
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. If the lane is relocated, all 34 fail identically
  and the audit stays **green** (row 2 of the table above is that exact case). Smallest safe
  correction: add the three degenerate controls to `recheck-audit.py`'s `selftest()` and require them
  to FAIL, and add R12 header-vs-`--source` cover to `audit_entry`; then `pass=N` means something a
  reader can re-derive.

**Recommendation: `score 4 held`** — record C1 as an improved *surface precondition* on
`depth:verifiability` (35/35 self-locating recheck lines, 23 fail-closed preserved, detectors
unchanged), not as detector-defined depth credit; the 6 → 35 count is the axis's 35-line surface,
whose score remains the `resolve.py`/`anchorcheck.py` census.
