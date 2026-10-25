# ExecCapS045 — Bugcrowd VRT CWE mapping dataset capture

Seat: `ExecCapS045` (executor, leaf). Round 29 wave 1 (hyaku run 7). Lane: kasegi-shokunin.
Scope: **only** `corpus/source-snapshots/round-29/S045.txt` + this receipt.
Model note: this seat's execution model is the session default `inception/mercury-3`
(workstation project context); no config route table was consulted because the item is a
deterministic instrument run — no model-dependent step exists.

## Command (exact)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S045 --url https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json --kind html --out corpus/source-snapshots/round-29/S045.txt
```

Instrument reader: `corpus/instruments/capture-source.py` (committed round 24; `--kind html`
strips tags/entities then collapses whitespace — for a JSON body the tag steps are identity, so
the snapshot is the fetched text normalized per line).

## Capture record

| field | value |
|---|---|
| exit | **0** |
| status | 200 |
| fetched_bytes | 28,482 |
| snapshot_bytes | 14,575 |
| sha256 | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` |
| utc | `2026-10-25T18:16:10Z` |
| out | `corpus/source-snapshots/round-29/S045.txt` (1,363 lines) |

Re-hash of the on-disk bytes after the run (read-only check) matches the printed digest exactly,
so the receipt line and the committed file agree (M28-12 rule).

## Content verification (the two required patterns)

1. **`idor` → CWE-932 row — PRESENT.** `S045.txt:91-94`: `"id": "idor"` / `"cwe": ["CWE-932"]`,
   under parent `broken_access_control` (`S045.txt:73`). Occurrence count of the literal
   `"CWE-932"` in the snapshot: **1** (exactly-once, Q9).
2. **`cwe: null` gap pattern — PRESENT.** Both shapes:
   - root `metadata.default` is `null` (`S045.txt:3`);
   - nodes carry `"cwe": null`: literal `"cwe": null` occurs **69** times in the snapshot; 62 of
     184 leaf nodes have a null `cwe`, e.g. `ai_application_security` (`S045.txt:8`),
     `algorithmic_biases`/children (`S045.txt:12,16,20`), `automotive_security_misconfiguration`
     and children (`S045.txt:32,36,40,…`), `excessive_jwt_lifetime` (`S045.txt:171`).

## Extra checks (same capture, support the staged F13 entry's claims)

- Top-level `content` categories: **36** (matches staged `program-severity-ladders-and-reward-scales.md`
  "36 top-level categories").
- `authentication_bypass` → `["CWE-287"]` (`S045.txt:117-120`).
- `privilege_escalation` → `["CWE-269"]` (`S045.txt:97-100`).
- Snapshot parses as JSON (`json.load` ok); 184 leaf nodes total, 122 with a CWE list, 62 null.

## Bounds compliance

- Writes: only `corpus/source-snapshots/round-29/S045.txt` (created; dir did not exist before) and
  this receipt — both under the lane repo. Nothing written to fleet root, sibling lanes, git/jj
  state, `~/Projects/shokuknow`, or any MCP/tool substrate.
- No pacman transaction, no tool installed (none needed; `capture-source.py` is stdlib-only).
- No subagents, no background jobs, no labrat spawned (single leaf task, no probe needed).
- No counter runs; this seat produces the subject capture itself, so no PRE-STATE/after pairing
  applies. The C2 counters (`source-recheck.py` etc.) are other seats' runs on the round-29
  manifest, which this seat does not write.
- Answering model recorded above (no route table invoked by this seat).

## Risks / notes

- The snapshot is what the host served at 2026-10-25T18:16:10Z; the instrument cannot certify the
  host serves identical bytes again (documented instrument limit) — the manifest pin will bind it.
- The `--kind html` normalization is identity for this JSON body (no tags/entities); Q8's
  `normalized=markup-whitespace` still applies to any later quote matching.
- Line numbers here are from the head `S045.txt`; they hold while the file is unchanged — the
  round-29 manifest quotes will re-verify them.
