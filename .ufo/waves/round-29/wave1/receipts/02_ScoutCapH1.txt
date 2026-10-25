# ScoutCapH1 — Recon receipt: S043 capture (C2 F13), HackerOne standard program policy

Role: scout (leaf), round 29 wave 1. Item: reconnaissance for the S043 capture —
live source https://hackerone.com/security/policy_versions.

## 1. Fetch metadata (instrument UA, 2026-10-25T18:16Z–18:23Z)

| item | value |
|---|---|
| URL | `https://hackerone.com/security/policy_versions` |
| HTTP code | 200 (HTTP/2; `cf-cache-status: DYNAMIC`, cloudflare) |
| Final URL | identical (0 redirects) |
| Content-Type | `application/json; charset=utf-8` |
| Body bytes (curl) | 1,220,741 |
| sha256 (body) | `02ecb50086eefcf3d82bb4b3542b93010eda51448874de8d4c63ef5b9db4dfc6` |
| ETag | `W/"02ecb50086eefcf3d82bb4b3542b9301"` (first 32 hex chars of body sha256) |
| `Vary: Accept` | present — server content-negotiates (see §3) |
| Reproducibility | 3 independent fetches (curl) → identical sha256 |

The landed snapshot `corpus/source-snapshots/round-29/S043.txt` (1,220,741 B,
0 newlines, sha256 `02ecb500…`) is byte-identical to this body. JSON API
document confirmed: top-level JSON array of **153 policy records**.

## 2. Record shape and standard-policy fields

Each record (object) has keys: `id`, `new_policy` (markdown string),
`target_signal` (null for the newest record), `previous_target_signal`,
`has_open_scope`, `pays_within_one_month`,
`protected_by_gold_standard_safe_harbor`, `protected_by_ai_safe_harbor`,
`disclosure_declaration`, `introduction`, `platform_standards_exclusions`,
`exemplary_standards_exclusions`, `scope_exclusions` (JSON-string list),
`timestamp`.

The newest record (index 0, max timestamp) is:

- record id **3787452**, timestamp **2026-10-16T15:34:59.854Z** —
  the staged S031 anchor **is present** (id 1×, timestamp 1× in the document; it is the newest record).
- `new_policy` = 205 markdown lines (§ headings: `## Program Scope and Assets`
  L27, `### In Scope` L29, `### Out of Scope` L38, `### DoS Reward` L168,
  `## 🚫 Denial-of-Service (DoS) Policy` L155).

## 3. Content-negotiation quirk (capture step MUST handle)

`capture-source.py` fetches via `urllib` with **no `Accept` header** → the
server returns the `text/html` JS-disabled stub (3,592 B; html→text snapshot
= 128 B: "HackerOne … It looks like your JavaScript is disabled …").
Verified by actually running the instrument (`--kind html`, `--kind text`):
both produced the stub (3,592 B fetched).

`curl` (default `Accept: */*`) or explicit `Accept: application/json` → the
JSON API (1,220,741 B). Conclusion: the S043 capture requires the **plain
fetch fallback** (curl with instrument UA; or urllib with an explicit
`Accept: application/json` header) — `capture-source.py --kind html` cannot
produce it as-configured.

Additional quirks:

- The raw JSON is a **single line** (0 real newlines). `source-recheck.py`
  `raw_lines` = 1, so only `anchor: 1` is in-range; the anchor window covers
  the whole document — **anchor=1 is vacuous** on this snapshot (any quote
  present passes `anchor=1-ok`; probe confirmed `anchor=2` → OUT-OF-RANGE).
- JSON escapes are literal (`\n`, `\u003c`…). `normalize()` collapses
  whitespace and strips `<u>/</u>` only; multi-line markdown spans do NOT
  match unless the quote is written with literal `\n` sequences. Single-line
  quotes match verbatim (all candidates below are single markdown lines).

## 4. Candidate verbatim quotes (record 3787452), with occurrence counts

Normalization = `source-recheck.py` `normalized=markup-whitespace`. For each
quote: doc-occurrences (whole 153-record array) / record-occurrences
(3787452's `new_policy` alone).

| quote | words | doc occ | record occ | record line |
|---|---|---|---|---|
| "Issues affecting assets under HackerOne's control are in scope." | 9 | 12 | 1 | L31 |
| "Third-party assets outside HackerOne's control are not authorized for testing because HackerOne cannot grant permission to test infrastructure it does not host or operate." | 24 | 12 | 1 | L40 |
| "Eligible Denial of Service (DoS) findings are capped at the **Medium** severity bounty rate for the affected asset." | 18 | **1** | 1 | L170 |
| "| `www.hackerone.com` | **$1,000** |" | 5 | 12 | 1 | L174 |
| "| `hackerone.com` | **$1,500** |" | 5 | 12 | 1 | L175 |
| "Reports that include prohibited testing methods or actions are **not eligible** for a reward." | 14 | 12 | 1 | L177 |
| "Using multiple approved proof-of-concept reports to demonstrate the same issue does **not** increase the severity or reward of a finding." | 20 | 12 | 1 | L92 |

Policy content coverage (item 2 of the assignment):

- what a program may authorise → `new_policy` "Program Scope and Assets"
  section (In Scope/Out of Scope), plus the flags
  `has_open_scope`/`protected_by_gold_standard_safe_harbor`/
  `protected_by_ai_safe_harbor`/`disclosure_declaration: "Standard"`.
- per-asset/per-finding severity caps → DoS Reward section (per-asset bounty
  table L172-175; DoS findings capped at **Medium** severity bounty rate for
  the affected asset, L170; prohibited-method exclusion L177; PoC-stacking
  severity/reward no-bump L92).
- "program can only place assets it controls in scope" → L31 (in scope =
  assets under HackerOne's control) + L40 (third-party assets outside
  HackerOne's control are not authorized because HackerOne cannot grant
  permission to test infrastructure it does not host or operate).

## 5. Kill-rule-relevant finding (flag for Main/executor)

C2's frozen kill rule includes "any manifest assertion not occurrences=1". The
**landed round-29 manifest** currently pins S043 Q1/Q2/Q4 against the raw
whole-document JSON → `source-recheck.py` reports `occurrences=12` for each
(anchor=1-ok; exit still 0). Under a literal reading of the kill rule, those
assertions fail the `occurrences=1` clause.

Remedies (both verified by running the instrument):

1. **Record-scoped capture** — commit the newest record's `new_policy` text
   as the snapshot (205 lines; sha256
   `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199`,
   7,298 B). All quotes above become occurrences=1 with real line anchors
   (L31/L40/L170/L174/L175/L177/L92) — all pass `source-recheck.py` exit 0.
2. Keep the raw JSON snapshot and assert only whole-document-unique quotes —
   currently only the DoS cap sentence (L170) and the id/timestamp markers are
   unique; the scope/per-asset quotes would be lost (reduces F13 coverage).

## 6. Model note

Answering model for this item: `inception/mercury-3` (operator session; no
model passed by me).

## 7. Files touched

- This receipt: `.ufo/waves/round-29/wave1/ScoutCapH1.md`.
- Read-only: live URL, `claims.json`, `corpus/source-snapshots/round-29/S043.txt`,
  `manifest.json`, `corpus/instruments/source-recheck.py`, `capture-source.py`,
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/…` (staged S031 row).
- No production edits; no sibling-owned files modified. Scratch probes under
  `/tmp` only (not part of the repo).
