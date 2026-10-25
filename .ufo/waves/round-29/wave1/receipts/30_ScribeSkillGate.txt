# ScribeSkillGate — round 29 wave 1

Seat: `ScribeSkillGate-2` (scribe). Owns `SKILL.md` only (R6, append-only — never shift existing lines).
UTC: 2026-10-25 (wave window). Answering model recorded from environment/project context: `inception/mercury-3`
(the config route table decides; no model was passed by this seat).

## Task

After `ExecImplC1` and `ExecEntryF13` land, append to `SKILL.md`:
1. a Gates & probes registry row for anchorcheck.py noting round-29 selftest completeness (limbs=9 covered=9, cases=12) and hermetic git-free behavior;
2. a frontier note line for F13 (program severity ladders and reward scales; entry path; sources S043–S045).
Keep every existing line at its number; record old/new line counts and before/after sha256; confirm `head -N` byte-identical for all unchanged lines.

## Dependencies (waited, then verified)

- **ExecImplC1** (pinger `ExecImplC1-2`): landed. I re-measured at the landed bytes (POST-STATE, not PRE-STATE):
  - `corpus/instruments/anchorcheck.py` sha256 `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` (561 lines; git baseline `23818c1204…ee7396` at 7a6591c1/f28ff5d/46e07f6).
  - `python3 corpus/instruments/anchorcheck.py --selftest` → prints `limbs=9 covered=9` and `selftest cases=12 failures=0`, exit **0** (`selftest_exit=0`).
  - `grep -E 'selftest cases=|limbs='` → found; exit 0.
  - git-free PATH run (frozen counter-3 shape: `env -i PATH=$T` with a python3-only dir) → **nogit_exit=0** (clean skip, no traceback; code/docstring: PIN-BROKEN case skips with `SKIP pin-broken (git not found)`).
- **ExecEntryF13** (pinger `ExecEntryF13`): landed. Verified the landed entry:
  - `corpus/knowledge/program-severity-ladders-and-reward-scales.md` sha256 `6beeedd7d2b2cb5ff3ecb5383041dbee63b9be54d9be50e282352b1b41a39ed4`; header `source: S043` / `source: S044` / `source: S045`, `verified-at: 2026-10-25`, `ground: F13`; recheck chains three `source-recheck.py --source` invocations from the lane-root `cd` (per ExecEntryF13 receipt, each exits 0 at the final bytes; manifest `79b32d50146116685df0d94db601e979c92dc4c50d7479d44c733dfab6f5da7f`).

## Edit performed (append at end-of-file, lines 1036+)

Appended 12 lines to `SKILL.md` (no line moved):
- `## Round-29 Gates & probes registry addition (appended 2026-10-25)` — one anchorcheck.py registry row (same 8-column shape as the round-28 row) carrying the round-29 self-test cell: `limbs=9 covered=9`, `selftest cases=12 failures=0`, exit 0, and hermetic git-free behavior (clean skip, no traceback); pinned-value path `.ufo/waves/round-29/c1-receipt-index.txt`. A one-line annotation states it records the round-29 state of the same instrument (R6) and supersedes the row above's self-test cell for this measurement.
- `## Round-29 frontier note (appended 2026-10-25)` — one F13 note line: topic, admission date, entry path, sources S043/S044/S045, captures pinned in `corpus/source-snapshots/round-29/manifest.json`.

Why end-of-file: an in-table insertion would shift every later line and break R6; the append keeps all existing line numbers (verified below).

## Measurements

| metric | before | after |
|---|---|---|
| `SKILL.md` lines | 1035 | 1047 (+12) |
| `SKILL.md` sha256 | `125be37d85ffe6be30a3c372b52d96d8074e3c4d7f4baf835d0f5aed5f56cca6` | `82bdced5d5c46b6847a169f5ce6bec172dbf0c57d51bc5ec5361e2bd4731ee70` |
| `head -n 1035` vs old bytes | — | `cmp` exit 0 → **byte-identical** for all unchanged lines |

No-harm checkpoint after the append: `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0, `7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`. (The only grep hit of fail-class tokens in the run text is the new row's prose mention, not a verdict.)

## Touched surfaces

- Written: `SKILL.md` (append only); this receipt `.ufo/waves/round-29/wave1/ScribeSkillGate.md`.
- Read-only: `claims.json`, `SCORECARD.md`, `corpus/{QUALITY.md,SOURCES.md,README.md}`, `corpus/lessons/round-28.md`, `corpus/lessons/round-28-verifier-spotcheck.md`, `considerthese/2026-10-25.md`, `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (MERGE-REPORT.md, SOURCES.append.md, staged F13 entry), `corpus/instruments/README.md`, `anchorcheck.py`, `wave1-spec.json`, `wave1/README.md`, `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`.
- Out of scope (intentionally untouched): `corpus/README.md` (ScribeReadmeC2), `corpus/SOURCES.md` (ScribeSourcesGate), `corpus/QUALITY.md` (ScribeQuality), `corpus/instruments/*` (ExecImplC1), `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (ExecEntryF13), git index/jj state, fleet root, `~/Projects/shokuknow`.
- No tool installs (RULES.md read; nothing installed — no pacman invoked).

## Findings

- C1 landed instrument satisfies the frozen predicate at the measured digest: limbs=9 covered=9, cases=12 failures=0, exit 0, git-free exit 0 (all re-measured by this seat).
- F13 landed entry exists at the claimed path with source ids S043/S044/S045 and ground F13; per-id source rechecks exit 0 (per ExecEntryF13 receipt; S043 occurrence counts >1 disclosed there due to one-line JSON capture).
- R6 append verified byte-identical for all pre-existing lines (head -1035 cmp), so anchors into SKILL.md (e.g., `SKILL.md:1000`, resolve-dispatch-fixtures) remain valid; the previously routed M28-6 pointer issue does not recur.

## Artifacts

- `SKILL.md` (modified), `.ufo/waves/round-29/wave1/ScribeSkillGate.md` (this receipt).
- Peers' receipts referenced: `.ufo/waves/round-29/wave1/ExecImplC1.md`, `ExecCanonC1.md`, `c1-receipt-index.txt`, `ExecEntryF13.md`, `ExecManifestC2.md`.
- Scratch: `/tmp/skill-old-r29.md` (pre-edit copy, sha256 `125be37d…`), `/tmp/skill-postcheck.txt` (post-append anchorcheck output).
