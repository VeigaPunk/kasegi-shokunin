# MutManifestC2 — mutation probe: Q9 stem/sha binding (round-28 manifest)

Seat: MutManifestC2 (FSD mutation tester, wave 1, C2 lane)
Probe state: **POST-LANDING** — `corpus/source-snapshots/round-28/{manifest.json,S041.txt,S042.txt}` existed at probe time; all runs used byte-exact scratch copies under `.ufo/waves/round-28/wave1/MutManifestC2/` (pristine/, m1/, m2/, m3/, m3b/). No production file was touched.
Detector: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest <dir>/manifest.json [--source ID]`
Date: 2026-10-25 (UTC)

## Baseline (pristine scratch copies, conclusive)

`pristine/` exit **0**: `S041:sha256 OK` + 6× `Q# OK occurrences=1`; `S042:sha256 OK` + 6× `Q# OK occurrences=1`. Per-source `--source S041` / `--source S042` runs also exit 0. Pre-probe hashes:

| file | sha256 |
|---|---|
| live manifest.json | `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d` |
| live S041.txt | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (== manifest pin) |
| live S042.txt | `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` (== manifest pin) |

## Mutants

| # | mutation (smallest behavior-bearing point) | expected | observed output | exit | verdict |
|---|---|---|---|---|---|
| M1 | S042 record `"path": "S042.txt"` → `"S042b.txt"`; scratch file renamed `S042.txt`→`S042b.txt` (stem≠id, same bytes) | non-zero | `S042:sha256 OK` + all 6 quotes `OK occurrences=1`; full-manifest and `--source S042` identical | **0** | **SURVIVED — live mutation** |
| M2 | S041 record `"sha256"` → S042's digest `b432…6966` (path/id bound to wrong bytes) | non-zero | `S041:sha256 MISMATCH expected=b432… actual=e18a…` | **1** | killed |
| M3 | both records `"path"` → `"S041.txt"` (shas/quotes untouched) | non-zero | `S042:sha256 MISMATCH expected=b432… actual=e18a…` | **1** | killed |
| M3b (extra probe) | both records → `"S041.txt"` AND S042 sha → `e18a…` (fully self-consistent duplicate path) | non-zero | `S042:sha256 OK`, then `S042:Q1..Q6 MISMATCH reason=quote-not-found` ×6 | **1** | killed — only via the quote layer; no dedup/path check fired |

## Live mutation named

**M1 survives: `source-recheck.py` does not bind `Path(path).stem == record["id"]`.** `check_source()` validates path shape, containment under the manifest dir, sha256 equality, and quote presence — the filename stem is never compared to the id. A capture renamed to `S042b.txt` (or `anything.txt`) still verifies clean under id `S042`, exit 0, in both full-manifest and `--source` modes. Grep over `corpus/instruments/` (source-recheck.py, capture-source.py, recheck-audit.py, frontier-recheck-count.py, anchorcheck.py, test_resolve.py) shows **no stem==id enforcement anywhere** — the "path stem equals id" limb of the C2 predicate lives only in manifest.json's self-documenting `purpose` string and review convention, not in the gate. This is a coverage finding (the contract is unchanged; nothing in this probe licenses editing it). M3b narrows the exposure further: even a *self-consistent* duplicate-path manifest fails only because quote bytes differ — sha/path dedup across records is likewise unchecked.

## Restoration evidence

All four scratch dirs re-synced to pristine bytes post-probe; `m1/S042b.txt` deleted. Post-probe `sha256sum` of every scratch file: manifest `e62ddad1…`, S041 `e18acbf9…`, S042 `b432ec16…` — identical to pre-probe. Pristine re-run after probes: exit 0. Live production files re-hashed post-probe: byte-identical to pre-probe (`e62ddad1…` / `e18acbf9…` / `b432ec16…`); `git status --porcelain corpus/source-snapshots/` shows only the wave's pre-existing `?? corpus/source-snapshots/round-28/` (untracked by my seat).

## Re-run command (L1, any state)

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json
```

Scratch fixture dirs retained at `.ufo/waves/round-28/wave1/MutManifestC2/{pristine,m1,m2,m3,m3b}/` for audit. Tooling: none installed.
