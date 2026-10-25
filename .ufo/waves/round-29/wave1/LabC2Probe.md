# LabC2Probe — C2 capture reproducibility probe (round 29 wave 1)

Seat: `LabC2Probe` (scout, leaf; no subagents). Lane: kasegi-shokunin.
UTC window: 2026-10-25T18:16–18:21Z. Lane HEAD read: `46e07f6ae8f23debb10034164252e7027b4d9091` (wave-1 dispatch commit).
Answering model: session default `inception/mercury-3` (no config route table consulted; the item is deterministic HTTP probing, no model-dependent step).

Instrument UA (exact): `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`.

## 1. Determinism — each capture URL fetched twice with the instrument UA (curl, `-L`)

| id | URL | run1 | run2 | identical? | SHA-256 (raw body) |
|---|---|---|---|---|---|
| S043 | `https://hackerone.com/security/policy_versions` | HTTP 200, 1,220,741 B | HTTP 200, 1,220,741 B | **YES** | `02ecb50086eefcf3d82bb4b3542b93010eda51448874de8d4c63ef5b9db4dfc6` |
| S044 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | HTTP 200, 8,881 B | HTTP 200, 8,881 B | **YES** | `72576250dfff95344cdda7e2af00b3d4843a5785cef9e2af0ab1e251c69ec022` |
| S045 | `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json` | HTTP 200, 28,482 B | HTTP 200, 28,482 B | **YES** | `3de912588d845cd57e49dca40e3273b13290c3775b1d6e69b6787efb342ff364` |

All three: no `Last-Modified` header today (ETag served instead: S043 `W/"02ecb500…"`; S044 `"19b012d7…"`; S045 `"86f97732…"`).

## 2. Redirect chain

- All three https URLs: **0 redirects** (`num_redirects=0`, final URL = requested URL).
- Redirect edge tested: `http://` variant of each → **301 Moved Permanently → https** (single hop) for all three. No multi-hop chain today.

## 3. UA-403 edge

| URL | browser UA | no UA (curl default) | edge result |
|---|---|---|---|
| S043 | HTTP 200, identical 1,220,741 B JSON | HTTP 200, identical 1,220,741 B JSON | **no 403** — same bytes with/without instrument UA |
| S044 | n/a (raw.githubusercontent) | HTTP 200, 8,881 B | no 403 |
| S045 | n/a (raw.githubusercontent) | HTTP 200, 28,482 B | no 403 |

The S040-style browser-UA-403 pattern is **not reproduced** on any of the three round-29 URLs today; all serve identical bytes regardless of UA.

## 4. Committed-capture reproducibility

| id | committed snapshot (on disk, sha256) | fresh instrument run (`capture-source.py` at 18:17:41Z) | reproducible today? |
|---|---|---|---|
| S044 | `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` (8,187 B) | `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` (8,187 B) | **YES** — byte-identical |
| S045 | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` (14,575 B) | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` (14,575 B) | **YES** — byte-identical |
| S043 | `02ecb50086eefcf3d82bb4b3542b9301…` (1,220,741 B — raw JSON API body) | `40c96a43e79df162223433a44ec93a09…` (**128 B — "JavaScript is disabled" stub**) | **NO via `capture-source.py`** |

**S043 caveat (important):** the committed S043.txt is the raw JSON API response (1,220,741 B, matches the curl fetch byte-for-byte), but re-running the committed instrument `capture-source.py --kind html` today does **not** reproduce it — the instrument's `urllib` fetch returns a 128-byte "It looks like your JavaScript is disabled…" stub (fetched 3,592 B → snapshot 128 B), because Cloudflare serves the JSON only to HTTP/2-ish clients, not to the instrument's `urllib` request. Raw-fetch reproducibility holds (two curl runs identical), but instrument-based reproducibility does not. The manifest pins the raw-JSON sha, so the pin is fetchable — just not by the documented capture instrument.

## 5. Quote locations

Ran the gate recheck (`source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043|S044|S045`):

| id | sha256 | Q1 | Q2 | Q3 | Q4 | exit |
|---|---|---|---|---|---|---|
| S043 | OK | OK occurrences=**12** anchor=MISSING | OK occurrences=**12** anchor=MISSING | OK occurrences=1 | OK occurrences=**12** anchor=MISSING | 0 |
| S044 | OK | OK occurrences=1 | OK occurrences=1 | OK occurrences=1 | OK occurrences=1 | 0 |
| S045 | OK | OK occurrences=1 | OK occurrences=1 | OK occurrences=1 | OK occurrences=1 | 0 |

**Quote-location findings:**
- S044/S045: all quotes exactly-once; locations hold, S044 Q3 still at line 33; S045 Q1 `idor`→`CWE-932` at JSON path `$.content[4].children[2]` etc. **No shift.**
- S043: Q1/Q2/Q4 each occur **12×** in the raw JSON (the standard-policy sentences repeat across the 153 policy records), the manifest declares **no anchor**, so source-recheck prints `anchor=MISSING`; and the manifest's `location` prose (e.g. "line 31/40/170/177") is uncheckable because S043.txt is a single-line JSON body (0 newlines) — those line numbers do not exist as file lines. **Q9 binding fails for S043 as pinned** (occurrences ≠ 1, no anchor), even though source-recheck exits 0.

## 6. Verdict for the C2 recheck gate

- Committed S044/S045 **are reproducible today** (byte-identical through the instrument, quotes exactly-once, no location shift).
- Committed S043 **is fetch-reproducible but not instrument-reproducible**, and its three non-unique quotes (12× each, no anchor) do not satisfy the `occurrences=1` kill rule as currently pinned. The C2 `source-recheck` exit 0 is not a Q9 pass for S043 (R12/Q9: exit code alone does not bind the quote).

## Bounds compliance

- Writes: only this report (under lane repo). No writes to fleet root, sibling lanes, git/jj state, `~/Projects/shokuknow`, or any tool substrate; fetches are read-only public GETs.
- No pacman transaction; no tool installed (curl present, 8.23.0; `capture-source.py` stdlib-only). No subagents/background jobs/labrat.

## Risks / notes

- S043's capture-pipeline divergence (urllib vs curl) means the round-29 manifest's S043 pin depends on an ad-hoc fetch, not on the committed instrument; if the F13 entry rechecks via `capture-source.py`, it will produce the stub, not the pinned JSON.
- The S043 `.occurrences=12` + missing-anchor state is a manifest-level defect (Q9) that the C2 counter (`source-recheck` exit 0) does not surface — recommend the F13 gate treat S043 quotes as needing anchors or a per-record capture before relying on `occurrences=1`.
