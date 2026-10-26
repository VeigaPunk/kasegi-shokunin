# RevManifestR32 — review of the normalized round-32 manifest (R8)

Seat: reviewer, leaf of the round-34 L2 wave (hyaku run 8). Read-only review seat:
no lane file edited, no git/jj mutation, no subagent, no fleet/shokuknow write.
Item: verify the normalized `corpus/source-snapshots/round-32/manifest.json` —
(1) `fetched_utc` values are strict UTC instants; (2) the `purpose` note states
they are verification re-opens of byte-equal content; (3) no other cell changed
(diff against the round-33 landed manifest); (4) source-recheck S049/S050 still
exit 0. Verdict with evidence below.

## Report

### 1. Diff base and provenance

The round-33 landed manifest was extracted read-only from lane history at both
the lane base and the claims-freeze commit; the two are byte-identical, so the
normalization happened after the freeze, in the round-34 working tree
(`git status --porcelain corpus/source-snapshots/round-32/` →
` M corpus/source-snapshots/round-32/manifest.json`; the L1 commits).

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git show 014ee2d7aa8c3c095ff57ae51097606a9906228c:corpus/source-snapshots/round-32/manifest.json > $S/manifest.r33landed.json
$ git show 29f606dbdd28aff6fd4573ab4b90788bbb90af13:corpus/source-snapshots/round-32/manifest.json > $S/manifest.freeze.json
$ sha256sum $S/manifest.r33landed.json $S/manifest.freeze.json corpus/source-snapshots/round-32/manifest.json \
    corpus/source-snapshots/round-32/S049.txt corpus/source-snapshots/round-32/S050.txt corpus/instruments/source-recheck.py
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  $S/manifest.r33landed.json
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  $S/manifest.freeze.json
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  corpus/source-snapshots/round-32/S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  corpus/source-snapshots/round-32/S050.txt
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
```

($S = /fast/scratch/hyaku/kasegi-r34/RevManifestR32.) The old digest `6e4e719a…`
matches the pre-state quoted in `.ufo/waves/round-34/wave1/ExecManifestR32Normalize.md`
§1; the current digest `72ab4e68…` matches that receipt's post-state §2. Capture
digests equal the manifest's own `sha256` pins and the fresh-fetch sha256s in
`.ufo/waves/round-33/wave1/ScoutLiveDrift.md` (commands block). Current size:
`wc -lc` → `94 6138` (old: 94 5753); JSON parses, `records=2 quotes=14`.

### 2. Assertion 1 — fetched_utc values are strict UTC instants: PASS

Structural walk over `json.load` of the round-33 landed bytes vs the working tree:

```
structural_changes:
  ('/purpose', 'VALUE', <old purpose text>, <new purpose text>)
  ('/sources[0]/fetched_utc', 'VALUE', '2026-10-25T23:14:00-03:00', '2026-10-26T04:16:06Z')
  ('/sources[1]/fetched_utc', 'VALUE', '2026-10-25T23:14:00-03:00', '2026-10-26T04:16:16Z')
total_changes = 3
old fetched_utc: [('S049', '2026-10-25T23:14:00-03:00'), ('S050', '2026-10-25T23:14:00-03:00')]
new fetched_utc: [('S049', '2026-10-26T04:16:06Z'), ('S050', '2026-10-26T04:16:16Z')]
all_strict_utc = True          # fullmatch r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$' on both
  2026-10-26T04:16:06Z parses as UTC instant -> 2026-10-26T04:16:06+00:00
  2026-10-26T04:16:16Z parses as UTC instant -> 2026-10-26T04:16:16+00:00
matches_ScoutLiveDrift = True  # vs .ufo/waves/round-33/wave1/ScoutLiveDrift.md lines 8/10
```

Ground truth for the instants is the round-33 drift seat's own measured stamps
(`ScoutLiveDrift.md:8` `utc=2026-10-26T04:16:06Z`, `:10` `utc=2026-10-26T04:16:16Z`,
both `status=200`), not a retyped prompt value. Offset audit on the new file:

```
$ grep -c -- '-03:00' corpus/source-snapshots/round-32/manifest.json
1
$ grep -o '"fetched_utc": "[^"]*-03:00"' corpus/source-snapshots/round-32/manifest.json | wc -l
0
```

The single remaining `-03:00` literal is the capture-commit author time kept as
history in the `purpose` first sentence — the R8-scoped reading (the
`fetched_utc` fields, not the whole file) is the one that passes. The in-flight
C1 suite's own R8 limb is built the same way (`corpus/instruments/r-defect-closure.sh:299-340`,
`check_r8`: strict regex + no-offset over `fetched_utc` fields only; its selftest
mutant re-injects `2026-10-25T23:14:00-03:00`, `:515-529`). That suite is
untracked/in flight (`?? corpus/instruments/r-defect-closure.sh`), so this seat
did not run it; the C1 seat owns its run.

### 3. Assertion 2 — purpose note states verification re-open of byte-equal content: PASS

The full `purpose` line (`:raw:3-3` of the manifest) states, verbatim:

> … each record carries its registry `url` and a strict-UTC (Z-suffix) `fetched_utc`
> that is a 2026-10-26 verification re-open instant of byte-equal content, not the
> original fetch: S049 2026-10-26T04:16:06Z and S050 2026-10-26T04:16:16Z, each
> HTTP 200 with 0 differing lines (round-33 lesson; `wave1/ScoutLiveDrift.md`).
> The capture commit's author time above (02:14Z) is a local-offset commit
> instant, not a measured HTTP fetch, and is recorded here as history rather than
> in a `_utc` field (R8).

Grounding, measured: `ScoutLiveDrift.md` comparison table shows both rows
`diff -u rc 0`, `differing lines 0`, fresh sha256 identical to the committed
pins; `corpus/lessons/round-33.md:31-32` records the same two re-open instants
with 0 differing lines; `:133` records the bound (post-conversion text equality
does not prove raw HTML/PDF-body equality). The note's "byte-equal content" is
therefore accurate at the frame the manifest actually pins — the converted-text
captures its `sha256` fields bind — and it does not claim raw-body equality. The
old semantics ("its `fetched_utc` from the capture commit (C1 rule B/C)") is
exactly what R8 flagged, and the note now records the commit time as history
outside the `_utc` field, matching the defect's "Normalize or rename the field"
(`corpus/lessons/round-33-verifier-spotcheck.md:184-185`).

Minor, pre-existing: the purpose cites `wave1/ScoutLiveDrift.md` without the
`.ufo/waves/round-33/` prefix; the old purpose line used the same bare form, so
this edit changed nothing about citation convention (resolvable in-lane).

### 4. Assertion 3 — no other cell changed: PASS

Two independent proofs:

(a) Structural walk (§2): `total_changes = 3` — exactly `/purpose`,
`/sources[0]/fetched_utc`, `/sources[1]/fetched_utc`. No `KEYS` or `LEN` entries,
so object key order and array lengths are unchanged; every `id`, `path`,
`sha256`, `url`, `quotes[].id/quote/location` and `schema_version` cell is
identical (`records=2 quotes=14`, `schema_version 1` both sides).

(b) Line-level diff against the round-33 landed base:

```
$ git diff --numstat 014ee2d7aa8c3c095ff57ae51097606a9906228c -- corpus/source-snapshots/round-32/manifest.json
3	3	corpus/source-snapshots/round-32/manifest.json
```

Unified diff: two hunks (`@@ -1,13 +1,13 @@` covering the `purpose` line and
S049's `fetched_utc`; `@@ -56,7 +56,7 @@` covering S050's `fetched_utc`), each
changed line replaced in place — `- "fetched_utc": "2026-10-25T23:14:00-03:00",`
→ `+ "fetched_utc": "2026-10-26T04:16:06Z",` / `…04:16:16Z`, plus the one
`purpose` line. No line added or removed beyond the 3/3 replacement.

Scope check: `git status --porcelain corpus/source-snapshots/round-32/` shows
only the manifest modified — the captures are untouched and their digests still
equal the manifest pins (§1).

### 5. Assertion 4 — source-recheck S049/S050 still exit 0: PASS

Instrument of record `corpus/instruments/source-recheck.py`, digest
`fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` (same bytes
the normalizer quoted). The instrument never reads `fetched_utc`, so "still"
holds by construction; measured anyway on the final bytes:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
S049:sha256 OK
S049:Q1 OK occurrences=1
… (Q2–Q7 identical)
S049:Q8 OK occurrences=1
recheck_S049_exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
S050:sha256 OK
S050:Q1 OK occurrences=1
… (Q2–Q5 identical)
S050:Q6 OK occurrences=1
recheck_S050_exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json
(16 assertion lines: 2 × sha256 OK + 14 × Q OK occurrences=1)
recheck_all_exit=0
```

Every assertion `occurrences=1`, both per-source runs and the full run exit 0.

### 6. Corroboration

- Frozen C1 kill-rule clause "round-32 manifest still carrying a non-UTC
  fetched_utc" (`.ufo/waves/round-34/claims.json`, C1) is now false on the
  working tree → R8 is closed on this file.
- The C1 suite's R8 limb exists and reads only the `fetched_utc` fields
  (`r-defect-closure.sh:61-62,299-340`), consistent with the scoped reading; its
  run belongs to the C1 seat (file untracked at my run time, 2026-10-26).

### 7. Adjacent findings for the L1 (outside my item's file; not edited by this seat)

The normalization makes four production-file mentions stale; each needs an
appended correction per the lane's corrections convention (frozen round-33
receipts under `.ufo/waves/round-33/` carrying the old digest/value are history
and correctly untouched):

1. `corpus/instruments/README.md:604` — digest table row still
   `| round-32 | 6e4e719a… |`; actual is now `72ab4e68…`.
2. `corpus/instruments/README.md` known-limit bullet (Known limits section,
   after `:606`): "`fetched_utc` is the capture commit instant for the round-32
   records, not a measured HTTP instant" — first clause now false.
3. `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:290-291`
   — binds the manifest by the old digest `6e4e719a…`.
4. `SCORECARD.md` (~`:1045-1046`, C1-blind-spots section): "rule C's
   `fetched_utc` is the capture-commit timestamp (round-32 manifest `purpose`),
   not a fetch instant" — first clause now false. (File is ` M` in flight by the
   R1 seat at my run time.)

### 8. Tooling

No tool installed or upgraded; system `python3`, coreutils and read-only `git`
only. No tooling entry to record.

### 9. Verdict

**PASS on all four assertions.** The normalized round-32 manifest carries only
strict-UTC `fetched_utc` instants equal to the round-33 drift seat's measured
stamps; the purpose note states the verification re-open of byte-equal pinned
content and keeps the capture-commit time as history outside the `_utc` field;
the change is exactly three cells (structural walk + `3 3` numstat agree); and
source-recheck S049/S050 (and the full manifest) exit 0 with every assertion
`occurrences=1`. R8 is closed on `corpus/source-snapshots/round-32/manifest.json`.
Residual for the L1: the four stale cross-file mentions in §7 and the C1 suite
run (in flight, not this seat's).

### 10. Scratch

`/fast/scratch/hyaku/kasegi-r34/RevManifestR32/` held the two extracted
landed-manifest copies only; removed before this seat yielded and verified
absent. No scratch tree remains on disk.
