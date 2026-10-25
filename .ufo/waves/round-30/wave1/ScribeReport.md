# ScribeReport-2 — round-30 wave-1 scoped findings

Role: UFO-FSD scribe (ScribeReport). Scope: compile the round draft report from measured bytes; no product edits, no judge/commit actions.

## Bytes measured (sha256, worktree at 2026-10-25T18:53:21Z; HEAD `002e92ce07ed398334ef7cd8ca08d3fd99631351`)

- `corpus/instruments/frontier-recheck-count.py` `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` (base `c8a62888…`)
- `corpus/instruments/source-recheck.py` `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` (base `9fe6a4a0…`)
- `corpus/source-snapshots/round-30/manifest.json` `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6`
- `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32`
- `corpus/SOURCES.md` `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` (47 rows)
- `corpus/README.md` `df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f` (frontier admitted=14)
- `corpus/knowledge/considerthese-proposals-ledger.md` `7574b776e431363427c66a7bcf725aa6843354689dff834e83c8f6a4c04d2bd3` (per ExecConsiderthese)

## Commands run (all from lane root; outputs in `ScribeReport-canonical.txt`)

- C1 A1: `python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1` → exit 1, `FAIL F98 knowledge/zz-missing.md … problems=missing-entry`
- C1 A2: `… --root …/harness-root-a2` → exit 1, `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`
- C1 B1: `python3 corpus/instruments/source-recheck.py --manifest …/q9/manifest-b1.json --source S043` → exit 1, `reason=stem-mismatch`
- C1 B2: `… --manifest …/q9/manifest-b2.json --source S045` → exit 1 (finding F-1 below)
- Real corpus: `python3 corpus/instruments/frontier-recheck-count.py` → `entries=17 pass=17 exit=0`
- Selftest: `python3 corpus/instruments/source-recheck.py --selftest` → `selftest cases=9 failures=0`, exit 0
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0, W04 S028/S029 only
- C2 per-id rechecks on round-30 manifest: S046/S047/S041 each exit 0 (12 assertions OK; S047 Q1/Q3 anchored `anchor=123-ok`/`anchor=130-ok`)
- C2 counts: `awk … admitted` → 14; `grep -lE '^source: S04[6-7] '` → 1; `grep -cE '^\|…S04[6-7]…'` → 2; registry rows → 47
- `recheck-audit.py` → `expect=present expected=41 missing=0 unexpected=2 exit=1` (expected list not yet regenerated for the two new knowledge files)

## Findings

- **F-1 (B2 fixture confounded by stem check).** The frozen B2 fixture `q9/manifest-b2.json` records id `S045` with path `B2.txt`; the new B1 limb therefore fires first and the counter prints `reason=stem-mismatch` (exit 1) rather than the predicate's `reason=occurrence-not-unique`. The kill rule's literal (`b2_exit != 1 or output lacks a failure reason`) is satisfied, and the occurrence limb is independently exercised by the selftest `double-occurrence` case (exit 1, `reason=occurrence-not-unique`). Flagged for RevC1Controls / mutant-B2 definition: dropping the occurrence check alone would NOT flip the committed B2 fixture (stem check would still exit 1); the mutant-B2 isolation test must use a stem-correct fixture with double occurrence.
- **F-2 (mid-wave manifest drift, M29-6 class).** An earlier measurement (18:52Z) saw a different `manifest.json` digest and a transient `S046:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`; the final manifest digest `dfc88357…` at 18:53:21Z passes all per-id rechecks. Snapshots label the final bytes; any earlier digest must not be cited as final.
- **F-3 (expected-list regen owed).** `recheck-audit.py` reports `unexpected=2` (`considerthese-proposals-ledger.md`, `japanese-severity-vocabulary-and-impact-model.md`); `knowledge-expected.txt` must be regenerated (41 → 43 entries) before close-out. Not a frozen C2 counter, but blocks the green audit gate.
- **F-4 (harness F14 id order).** Harness prints `PASS F14 … ids=S041,S046,S047`; claims.json's sentence writes `S046,S047,S041`. Set is identical; kill rule unaffected. Noted for literal-minded readers.
- **C2 manifest note.** S047 Q1/Q3 are non-unique occurrences (3 and 2) made acceptable by verified anchors (`occurrences=3 anchor=123-ok`, `occurrences=2 anchor=130-ok`) — Q9 anchor path, consistent with the claim's "exactly-once (occurrences=1) with stem == id" only where no anchor exists; the anchored path is the permitted exception per Q9.

## Boundary compliance

- Writes only inside the lane repo (this report + `draft-report.md` + `ScribeReport-canonical.txt` under `.ufo/waves/round-30/wave1/`). No write to fleet root, sibling lanes, `/home/vgpnk/Projects/shokuknow`, git/jj state, `.ufo/state`, or MANIFEST.json.
- No live target contacted; all commands local and read-only.
- No tools installed; no pacman transaction attempted.

## Handoff to L1

Run `ScribeReport-canonical.txt`'s post-commit recheck at the integration commit; regenerate the expected list; assemble the lesson (Gate verdicts, quarantine, M30-*). Integrate `draft-report.md` into `.ufo/reports/round-30/kasegi.md` with the commit hash filled in.
