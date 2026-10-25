# ScribeReadmeC2 — round-29 wave1 receipt

Seat: `ScribeReadmeC2-2` (scribe, leaf: no subagent dispatch, no background jobs).

Scope: `corpus/README.md` ONLY (append-only, R6). No other lane file edited.

## What was done

After `ExecEntryF13` confirmed the F13 entry existed (messaged
`agent://ExecEntryF13`, readiness reply received; entry verified on disk with
`source: S043` / `source: S044` / `source: S045` header lines and
`ground: F13`), appended one appended section to `corpus/README.md` (file end,
lines 246–264; every pre-existing line 1–245 unshifted):

1. Coverage-map row (line 260):
   `| Program severity ladders and reward scales (round 29) | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 — public primary, opened 2026-10-25 |`
2. Frontier row F13 (line 264):
   `| F13 | Program severity ladders and reward scales | admitted | knowledge/program-severity-ladders-and-reward-scales.md | S043, S044, S045 | Keep each platform's ladder as its own suggested baseline — distinct from CVSS-B and from other programs' reward ceilings; do not generalize a payout scale across programs. |`

Both rows were appended at file end (R6) rather than inserted into the existing
tables, so every existing line number is preserved; this matches the round-28
amendment precedent in the same file.

## Gates

- C2 counter (frozen, `claims.json`): `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → **13** (before: 12). PASS.
- Before sha256: `5f458a7a26b8dfc2dd2ee2e46e11380d5697e51e77213772bce7b59253363180`.
- After sha256: `67d94e80d7253edcb1988f204a5176434b12cac93afd43db058b4c80a3a2c860`.
- Append-only: `git diff`-class line check performed via read — lines 1–245 byte-identical to before-state read; the only change is the appended block.
- F13 entry exists at `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (created by ExecEntryF13; verified directly, source headers S043/S044/S045 present).

## Touched surfaces

- `corpus/README.md` — appended section only (246–264).
- `.ufo/waves/round-29/wave1/ScribeReadmeC2.md` — this receipt.
- No other lane file read/written. No writes outside the lane repo; no git commands run; no jj touched.

## Provenance / out-of-scope notes

- Captures `corpus/source-snapshots/round-29/S043.txt`, `S044.txt`, `S045.txt` exist (sha256: S043 `40c96a43…`, S044 `8adfca61…`, S045 `f583a396…`). `manifest.json` was absent at my edit time; per `ExecEntryF13`'s message, the manifest is being corrected by `ExecManifestC2` (S043 Q2/Q4 `occurrences=12 anchor=MISSING` reported). That is the entry/manifest seat's scope, not this seat's; the README rows are unaffected and do not depend on the manifest.
- I did not run any counter that belongs to another seat (source-recheck, frontier-recheck-count, sources-census) — those are C2 verification receiver for the L1/verifier, not this scribe seat.
- Answering model: this seat performed no model-dependent inference; every appended string is transcribed from committed repo bytes (entry header, registry rows, existing README table shapes). No model was passed or invoked.

## Findings

- `frontier-recheck-count.py` reads any `| F\d+ |` row regardless of table position (regex `^\|\s*(F\d+)\s*\|…`), so the appended F13 row is counted and will be harness-reachable once the manifest lands.
- No defects observed in the README append; awk count 12 → 13 exactly.
