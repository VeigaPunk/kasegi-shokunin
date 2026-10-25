# ScribeSourcesGate — round 29 wave 1

Seat: `ScribeSourcesGate-2` (leaf scribe). Scope: `corpus/SOURCES.md` only. Axes: `depth:verifiability`, `coverage`. Lane base: `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; claims freeze: `f28ff5d26b29270f93163117e7255e24f0b1d947`.

## Behavior and gate

Waited for the prerequisite scratch-mirror gate. `ExecCensusDry-2` reported PASS: planned S043/S044/S045 rows and the F13 used-by target were installed in the scratch mirror, `sources-census.sh validate --file <scratch>/corpus/SOURCES.md` exited 0 with only the pre-existing W04 warnings for S028/S029, and scratch census reported 45 rows. The executor receipt is `.ufo/waves/round-29/wave1/ExecCensusDry.md`. Only after that PASS did I append the live rows.

Appended exactly three registry rows after S042 and before `## Paths`: S043 HackerOne policy record 3787452, S044 Bugcrowd VRT README, and S045 Bugcrowd VRT CWE mapping dataset. All are tier A, status `mined`, opened `2026-10-25`, recheck `90d`, and `used-by` exactly `corpus/knowledge/program-severity-ladders-and-reward-scales.md`. No cell contains a pipe delimiter internally. Anchors describe the round-29 captures, not staged prose: S043 describes the policy API capture and manifest-pinned policy sections; S044 points to captured README lines 9–11, 26–33 and 32–38; S045 points to the JSON capture's metadata, category, idor/CWE-932 and null-node lines. Capture evidence is under `corpus/source-snapshots/round-29/`; the capture seat's receipt `ExecCapS043.md` records S043's JSON/API fallback and digest, and `ExecCapS045.md` records S045's captured JSON and digest. The manifest is `corpus/source-snapshots/round-29/manifest.json`.

The rows use staged S031/S032/S033 as document/name provenance only; the adopted lane ids continue from S042. Each row's `opened` cell changed from staged `2026-10-23` to actual opened date `2026-10-25`, `anchor` was rewritten from the captures, and `used-by` was narrowed to the single F13 entry. Each is a new row, so old→new applies to each new row's cells; no existing registry row was altered. The appended `## Registry changes` note records these changes and explicitly records S041/S042 as untouched.

## Exact commands and outcomes

Before append:

- `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/SOURCES.md` → `e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`.
- `grep -cE '^\\|[[:space:]]*S[0-9]{3}[[:space:]]*\\|' corpus/SOURCES.md` → `42`.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0; W04 S028/S029 and `ok` row only.

After append, exact command:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/SOURCES.md && grep -cE '^\\|[[:space:]]*S[0-9]{3}[[:space:]]*\\|' corpus/SOURCES.md && grep -cE '^\\|[[:space:]]*S04[3-5][[:space:]]*\\|' corpus/SOURCES.md && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
```

Observed: digest `fa54ba528eadc032e3cf0cbc6f431e683b2d0d5e7bc1123dd5bb874ac92d1836`; registry rows `45`; S043–S045 rows `3`; census output W04 S028/S029 plus `kasegi ok`; `census_exit=0`. Only the pre-existing W04 warnings remain. After-hash was independently obtained with `sha256sum` and Python `hashlib.sha256` over the registry bytes, with identical digest.

## Touched surfaces, limits, exclusions

Changed `corpus/SOURCES.md` only: appended rows S043–S045 and added Registry-changes bullets. Receipt written at `.ufo/waves/round-29/wave1/ScribeSourcesGate.md`. No edits to the F13 knowledge entry, capture files, manifest, claims, scorecard, lesson, judge or other product files. No package files were written; `/home/vgpnk/Projects/shokuknow/merge/kasegi/` was read-only. No tool installation, git/jj command, commit, push, build, lint or test was performed. I did not run the other C2 counters; their receipts are separate evidence. The assignment's requested post-append census is the only C2 command reported here.

Model provenance: no model-dependent source judgment or generated content was used for the registry edit; the row facts and anchors derive from lane captures and the census gate. Seat's runtime route was not queried, so no model identity is asserted.
