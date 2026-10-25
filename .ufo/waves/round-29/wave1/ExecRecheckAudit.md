# ExecRecheckAudit — expected-list regeneration for the recheck audit (round 29, wave 1)

Seat: `ExecRecheckAudit` (executor; axes depth:verifiability + coverage). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Run answering model: `inception/mercury-3`
(workstation default; this item performs no model-dependent generation, so no config route
table was consulted).

## Scope

Regenerate `corpus/instruments/knowledge-expected.txt` so `recheck-audit.py` passes after the
F13 entry landed, proving the stale list fails first. Only two files were touched:
`corpus/instruments/knowledge-expected.txt` (regenerated) and this report. No other file was
written; no other seat's file was edited.

## RED-BEFORE — proof that the old list fails (run 1)

State at run time:

- Tree: 41 `corpus/knowledge/*.md` entries, including the landed F13 entry
  `program-severity-ladders-and-reward-scales.md` (sha256
  `e461057c0b93a401a1e84651aba17d5b4caceee4e82d59e5d7e93ab1c5fd60ec`; captures S043/S044/S045
  and `manifest.json` present, sha256 `79b32d50…5da7f`).
- `corpus/instruments/knowledge-expected.txt` unchanged at the round-28 regenerated state:
  **42 lines = 40 entries + 2 comment lines** (header `— round 28`), sha256
  `8d96a4eae9058960c0239ce0cac16cd2e82392c678d40a1feeba530a3f81c16b` (git HEAD bytes; working
  tree was clean before this seat's write).

Command (from the lane root):

```
python3 corpus/instruments/recheck-audit.py
```

Result (red, captured verbatim):

```
unexpected=corpus/knowledge/program-severity-ladders-and-reward-scales.md
strict pass=41/41 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=17 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=40 missing=0 unexpected=1 exit=1
AUDIT_EXIT=1
```

Every one of the 41 entry lines passed the frozen and strict limbs (`strict pass=41/41`), so
the sole red driver was the stale expected list: `unexpected=1`, `exit=1` — exactly the
predicted failure. The F13 entry itself executed (lane=0 foreign=0), i.e. its `recheck:` line
ran cleanly from both cwds at capture time.

## Regeneration (write)

Expected list regenerated from the tree with the round-28 header convention (round marker
updated, sorted one-entry-per-line, `#` comment lines preserved):

- Old: 42 lines = 40 entries + 2 comments; sha256 `8d96a4ae…81c16b`.
- New: 43 lines = 41 entries + 2 comments; sha256 `6d26f6d5a290eb6039a3783b55246a7800c346e0c416d970750553346458989a`.
- New entry added: `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (inserted
  in sort order between `program-quirks.md` and `repo-git-state.md`).

## AFTER — re-run until green (run 2)

```
python3 corpus/instruments/recheck-audit.py
```

```
strict pass=41/41 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=17 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=41 total=41 pass=41 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=41 missing=0 unexpected=0 exit=0
AUDIT_EXIT=0
```

Green on the first re-run; `wc -l` → 43, `grep -vc '^#'` → 41 confirm the expected shapes.
A repeat run (run 3) produced byte-identical summary lines and exit 0 (deterministic).

## Files changed

- `corpus/instruments/knowledge-expected.txt` — regenerated (40 → 41 entries; 42 → 43 lines;
  header `round 28` → `round 29`).
- `.ufo/waves/round-29/wave1/ExecRecheckAudit.md` — this report.

Nothing else touched. Bounds respected: no fleet-root writes, no git/jj commands on the lane,
no edits to any other seat's files.

## Risks / notes

- RED-BEFORE was captured while the C2 chain was still settling (ExecCapS043 replaced the
  initial S043 "JavaScript disabled" stub with the raw JSON capture; ExecEntryF13 reported
  manifest Q2/Q4 corrections to ExecManifestC2). The audit run itself executed the F13
  `recheck:` line cleanly (exit 0 from both cwds) at capture time, so the stale-list proof is
  uncontaminated by any manifest churn.
- No PRE-STATE number is compared to an after column: run 1 is the red proof against the
  unmodified round-28 list; runs 2–3 are the green state after regeneration.

## Addendum — re-verification on the final C2 bytes (appended, never in-place)

After this report was first written, ExecCapS043 replaced S043.txt with the record-scoped final
snapshot (204 lines / 7,298 B, sha256 `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199`)
and the manifest/entry were refreshed (entry sha256 `5d056f60a5421828f3f6e295697e271edae669d3da6ff693260155d970e2d331`,
manifest sha256 `54a36f4f3602221f71a52a42106cbf28502bffe2e06d39b0ca6cfe55076b8854`). A fresh audit
run on these final bytes (same command, lane root):

```
strict pass=41/41 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=25 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=41 total=41 pass=41 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=41 missing=0 unexpected=0 exit=0
AUDIT_EXIT=0
```

Green holds on the final bytes: `expected=41 missing=0 unexpected=0 exit=0`. The F13 entry's
`recheck:` line is `gated` (fails closed on the current capture chain) but passes all frozen and
strict limbs (`PASS` per entry, 41/41). The expected-list regeneration itself is byte-final and
unchanged by the capture refresh.
