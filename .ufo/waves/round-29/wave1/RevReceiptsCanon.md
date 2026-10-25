# RevReceiptsCanon — canonical receipts review (round 29, wave 1)

Seat: `RevReceiptsCanon` (reviewer, leaf). Scope: the canonical receipt set —
`ExecCanonC1` / `ExecCanonC2` (+ `ExecPostCommitRecheck`), the assembled
`c1-receipt-index.txt` / `receipt-index.txt`, and the C1/C2 controls. UTC review
window: 2026-10-25T18:20Z–18:35Z. Answering model: `inception/mercury-3`
(workstation route; no model passed by me). No tool installed/upgraded (nothing
needed; pacman untouched). All checks below are read-only re-runs over the lane
working tree; `git status --porcelain` count stayed 15 → 16 (README F13 row
landed mid-review), i.e. my review runs mutated nothing.

## Verdict

The canonical receipts are **substantively truthful and M28-1-compliant**: the
C2 receipt is honestly labelled PRE-STATE with the exact re-run named; the C1
receipt index reports numbers I reproduce byte-for-byte at the same bytes; exit
codes are recorded everywhere; and both receipts’ measured lane-hash is the tip.
One material caveat: the C1 index calls its state “C1 AFTER … at the landed
production bytes” and its kill-rule table marks the instrument digest “matching
committed digest PASS” — but at review time no committed blob carries that
digest (tip `46e07f6…` still has anchorcheck.py `23818c…`). The digest matches
only the uncommitted working-tree file. Both seats disclosed this nuance in
prose; it is a labeling/timing overstatement, not a fabricated number.

## Verification performed (independent, read-only)

Lane commits (git rev-parse/log): tip `46e07f6ae8f23debb10034164252e7027b4d9091`
(wave-1 dispatch), freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`, base
`7a6591c1eb8a14f427297980a96fa8bb339f29ee` — all three match claims.json and
both receipts’ measured-hash statements.

C1 frozen counters re-run at the current working tree:
- `python3 corpus/instruments/anchorcheck.py --selftest` →
  `selftest cases=12 failures=0` / `limbs=9 covered=9`, exit 0.
- `python3 corpus/instruments/anchorcheck.py --selftest | grep -E 'selftest cases=|limbs='` → same two lines, exit 0.
- Frozen counter 3 (git-free PATH): `T=$(mktemp -d) && ln -s "$(command -v python3)" "$T/python3" && env -i "PATH=$T" "$T/python3" corpus/instruments/anchorcheck.py --selftest >/dev/null 2>&1; E=$?; ...` → `nogit_exit=0` (clean skip, no traceback).
- `anchorcheck.py SKILL.md` → 7 in-range, 0 bad, LOST-RECORDED=306, PIN-BROKEN=0, ORIGIN=0, OUTSIDE-BASE=0, BASE-ABSENT=0, exit 0.
- Digests: working-tree `sha256sum corpus/instruments/anchorcheck.py` = `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` (561 lines) = the `c1-receipt-index.txt` `instrument_sha256` line. `git show HEAD:corpus/instruments/anchorcheck.py | sha256sum` = `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396` = base blob at `7a6591c1…` = claims.json do-nothing-control pin. `git diff --stat HEAD -- corpus/instruments/anchorcheck.py`: 1 file, +78/−42.

C2 frozen counters re-run at review time (post-landing):
- frontier admitted = **13** (`awk` over corpus/README.md; F13 row at README:264)
- entries citing `^source: S04[3-5] ` = **1**
- S043+S044+S045 registry rows = **3** (SOURCES.md:49-51; registry total 42 → 45)
- `sources-census.sh validate` exit **0** (W04 S028/S029 only)
- `frontier-recheck-count.py` → `entries=16 pass=16 exit=0` (F13 PASS line binds entry ids=S043,S044,S045)
- `source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043|S044|S045` → exit **0** each; S044/S045 all assertions `occurrences=1`; S043 Q1/Q2/Q4 `occurrences=12` (Q1 anchor=1-ok; Q2/Q4 anchor=MISSING), Q3 `occurrences=1`.
- Snapshot digests recomputed and matching the manifest pins: S043 `02ecb500…`, S044 `8adfca61…`, S045 `f583a396…`; `manifest.json` present.

Controls: `wave1/c1-controls/before.txt` (instrument sha256 `23818c…`, selftest cases=9/exits 0, limb-assert grep = 0, `nogit_exit=1` + FileNotFoundError 'git' traceback), `base-control-grep.txt`, `base-control-selftest.txt`, `round-29/c2-controls/before.txt` (12 / 0 / 42 / harness 15-15) — all match the claims `do_nothing_control` expectations.

## Findings by severity

**H1 — medium: C1 index labels an uncommitted state as AFTER.** `c1-receipt-index.txt`
header is “C1 AFTER … at the landed production bytes”; `ExecCanonC1.md` kill-rule row
marks “instrument_sha256 line matching committed digest | PASS”. At review time the
lane tip `46e07f6…` still commits anchorcheck.py at `23818c…`; `68e1bdc…` exists only
in the working tree (`M corpus/instruments/anchorcheck.py`, +78/−42). The claim’s kill
rule is conditioned on the **committed** digest, so the PASS row is premature until the
integration commit preserves these bytes and `ExecPostCommitRecheck` re-hashes at that
commit. The seat’s own “Notes / risks” says exactly this; the index/table rows just
outrun it. This is a labeling/timing overstatement, not a fabricated number — every
figure is reproducible at the same bytes. Close-out requirement: integration commit must
land anchorcheck.py unchanged; `ExecPostCommitRecheck` must record `git rev-parse master`
and re-hash; the index’s `instrument_sha256` line must then equal the committed digest
(or the index must be regenerated at that revision).

**H2 — low / informational: git-free run counts a skipped limb as covered.** In the
`--selftest` code the pin-broken case, when git is absent, prints `SKIP pin-broken (git
not found)` and is appended to `executed`, so `covered=9` includes a limb that did not
actually run in that environment. For the no-git predicate this is the declared clean-skip
behavior (exit 0, no traceback) and the receipt shows the SKIP line; but the predicate
“every declared verdict limb has an isolating failing fixture” is only demonstrated in a
git-present run. State this in the receipt text to keep the coverage claim exact.

**H3 — low / verifiability gap: C2 kill-rule wording vs instrument behavior on S043.**
The frozen kill rule says “any manifest assertion not occurrences=1”, yet the landed S043
manifest (minified one-line JSON capture) reports `occurrences=12` for Q1/Q2/Q4 while
`source-recheck.py` exits 0 (Q9 semantics: non-unique quotes are observable, not fatal;
Q2/Q4 print `anchor=MISSING`). Literally read, the rule would fail the very capture the
round admits; the entry §Limits documents this. Class: same as M28-3 (frozen wording vs
instrument). Recommended: the after-run receipt must record the observed occurrences
verbatim (the C2 re-run block already does), and the L1 should decide whether to accept
“assertions check OK” or append a claims correction stating S043 exactly-once is
impossible under whole-file normalization.

**H4 — positive strengths.** ExecCanonC2 is the model M28-1 receipt: PRE-STATE label,
every counter row with expected vs measured, named exact re-run commands, express ban on
comparing pre-state to after. Exit codes are present in every receipt
(`selftest_exit`, `nogit_exit`, `skill_exit`, `census_exit`, `harness_exit`,
`recheck_exit`). Indexes carry the exact frozen counter text (grep -E 'selftest
cases=|limbs=' verbatim). Measured commit hash equals the lane tip at measurement time in
both receipts. Snapshot digests match the real files (independently recomputed). Base
controls match claims.json exactly.

## Residual risk / gaps

- `ExecPostCommitRecheck.md` exists but **`post-commit-recheck.txt` has not been
  produced**: it correctly refuses to run counters before the L1 integration-landing
  message and specifies the exact final-run steps. Outstanding deliverable, not a defect.
- **No C2 after-receipt exists yet**: the interim after-state I measure (13/1/3/45/
  16-16/0) has not been recorded by any seat; the canonical C2 re-run is still owed at
  the integration commit.
- `receipt-index.txt` (generated 18:19:59Z) is already stale: several seats filed after
  generation (e.g. ScribeSourcesGate, CritC1Kill, CritMeta, LabInstrumentProbe,
  ScribeQuarantine, SimplyBloat), so its ok=28 undercounts; regenerate at assembly time
  (ExecAssembleReceipts seat).
- C1 controls were captured at base bytes (correct); they remain the only before-record
  for C1 and are not claimed as after.

## Close-out checklist for L1

1. Integration commit: include anchorcheck.py (561 lines) unchanged; verify final
   `sha256sum corpus/instruments/anchorcheck.py` = `68e1bdc…`.
2. `ExecPostCommitRecheck`: record `git rev-parse master`, run both frozen counter sets
   at that revision, capture exits, update `post-commit-recheck.txt` and re-check
   `c1-receipt-index.txt` digest line against the committed blob.
3. Record the C2 after-run (frontier 13, rows 45, harness 16/16, recheck exit 0,
   per-id occurrences as measured above) at the integration commit.
4. Regenerate `receipt-index.txt` after all seats have filed.
