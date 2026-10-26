# ScoutS017Chk receipt — cross-check of ScoutS017's S017 capture (round 40)

Seat: ScoutS017Chk (leaf, no subagents). Scope: verify ScoutS017's capture for registry row S017 (https://projectzero.google/2025/07/reporting-transparency.html) and assess mined vs rejected per QUALITY.md Q1-Q6 and corpus/README.md. I did not edit SOURCES.md, any knowledge file, or any other lane file; my only lane writes are this receipt and `ScoutS017Chk.txt`.

## Verdict recommendation

**MINED** — one line in `ScoutS017Chk.txt` (1 line, 2537 bytes, sha256 e2bd779d8594c4f461ba33c0eabffe71c90951f6d357be4737fade5582f8889b). My agreement is independent of ScoutS017's own run: fresh fetch, fresh normalization, fresh greps, fresh source-recheck.

## 1. Capture integrity (re-opened bytes)

`ScoutS017.capture.txt`: 5058 bytes (`wc -c`), 39 lines (`wc -l`), sha256 `3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe` (`sha256sum`) — all three equal the manifest record's `size_bytes`/`snapshot_bytes`/`lines`/`sha256`. Manifest record `status` 200 and `size_bytes` 5058 match live behavior (below). Record `path` `S017.txt` stem = id (source-recheck B1 passes).

## 2. Live re-fetch (independent)

`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0` at 2026-10-26T21:18:13Z: HTTP 200, 0 redirects, final URL unchanged, 14764 bytes, `content-type: text/html`, `content-length: 14764`, `server: sffe`, no `last-modified`, `cache-control: no-cache, must-revalidate` — matches the manifest record's http block. Raw sha256 `f2b272f98e710115bac4562ada5f6701421f4464457bbde7594b080f4f059599` differs from ScoutS017's recorded `raw_sha256` `4bd7186c…`; a second consecutive fetch gave `e535b361…` with 110 differing bytes (`cmp -l | wc -l`), confirming the receipt's per-request CSP-nonce explanation. The nonce does not reach the snapshot (next check).

## 3. Snapshot reproducibility

`python3 corpus/instruments/capture-source.py --id S017 --url … --out $S/S017-refetch.txt --kind html` at 2026-10-26T21:18:20Z printed:
```
S017 status=200 fetched_bytes=14764 snapshot_bytes=5058 sha256=3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe utc=2026-10-26T21:18:20Z
```
and `cmp` against `ScoutS017.capture.txt` → **byte-identical**. The committed capture is reproducible from a live fetch despite the nonce.

## 4. Quote occurrence and anchors (grep -c >= 1)

- Q1 `within approximately one week of reporting a vulnerability to a vendor, we will publicly share that a vulnerability was discovered.` → grep -c = **1**, at capture **L23**, under heading L21 `The Trial: Reporting Transparency` (20 words, ≤25 ✓).
- Q2 `no technical details, proof-of-concept code, or information that we believe would materially assist discovery will be released until the deadline.` → grep -c = **1**, at **L34**, under heading L33 `Will this help attackers?` (20 words).
- Q3 `Reporting Transparency is an alert, not a blueprint for attackers.` → grep -c = **1**, at **L34**.

Independent `source-recheck.py` run (record wrapped as `{schema_version:1, sources:[record]}` with the capture copied beside it):
```
S017:sha256 OK
S017:Q1 OK occurrences=1 anchor=23-ok
S017:Q2 OK occurrences=1 anchor=34-ok
S017:Q3 OK occurrences=1 anchor=34-ok
rc=0
```
Cross-check finding: the round-22 Gate row (`corpus/lessons/round-22.md:93`) places the Q2 quote under "The Trial: Reporting Transparency", but it actually sits at L34 under "Will this help attackers?" (L33) — ScoutS017's manifest anchors are the correct ones; the round-22 location column is the stale one.

## 5. New-ground check (independent greps)

- `grep -ri 'reporting transparency|upstream patch gap|patch gap|big sleep' corpus/knowledge/` → **0 hits**.
- Project Zero mentions in knowledge/ are only `coordinated-disclosure-timelines.md` (S005: 90-day deadline/30-day uptake/14-day grace) and `ai-assisted-finding-validation.md:39` (S010 Naptime benchmark caveat) — neither holds the reporting-transparency trial.
- `grep -rl S017` over corpus (*.md/*.txt/*.tsv/*.json, excluding source-snapshots) → exactly `corpus/SOURCES.md:23` (status `queued`) and `corpus/lessons/round-22.md:93` (quote-only Gate row; no knowledge entry, no capture). No supersession: no other registry row covers this URL (grep `reporting-transparency` in SOURCES.md → only S017).
- Frontier F01-F22 (corpus/README.md): F02 holds S003/S004/S005 clocks; F06 holds S018's upstream/downstream roles ("an upstream fix is not downstream evidence"); F10 holds vendor-side policies; F21/F22 hold CSAF/VEX. None holds a researcher-side policy that publicly pre-announces a report's existence within ~1 week. S017 adds: the notice step (vendor/project, product, report date, deadline expiry — L24-26), the upstream-patch-gap concept (L17), and the no-technical-detail limit (L34). Fits as an extension of F02/F06, attributed first-party.

## 6. Q1-Q6 assessment

- Q1: capture + manifest record + recheck command exist; `source-recheck.py` is the runnable recheck and passes. ✓
- Q2: S017 is a tier-A docs row opened this round; entry would rest on it. ✓
- Q3: verbatim ≤25-word quotes with exact line/section anchors, verified occurring in the capture. ✓
- Q4: capture is Project Zero's own first-party trial post ("we're announcing a new trial policy" L20; "This is a trial" L37); entry must state it as PZ's position and carry the as-of 2025-07-29 date — the capture supports that framing; unknown trial outcome after the post is a qualification, not a rejection ground. ✓
- Q5: falsifiable rule available ("no technical details, proof-of-concept code, or information that we believe would materially assist discovery will be released until the deadline" — checkable against any issued notice); over-generalization to reject available (treating the notice as universal researcher practice, or as an attacker blueprint — the post itself rejects the latter). ✓
- Q6: documentation-only policy post; no probing instructions, credentials, or private URLs. ✓

No Q1-Q6 failure and no covered/superseded ground → **mined** is supported; rejection would be wrong.

## Tooling

No installs or upgrades (operator 2026-10-19 rule read; nothing needed beyond lane instruments + curl). No git/jj mutations anywhere. No writes outside `wave1/ScoutS017Chk.{txt,md}` and scratch.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ScoutS017Chk/` (held refetch.html, refetch2.html, headers.txt, S017-refetch.txt, recheck/{manifest.json,S017.txt}) — removed before yield; deliverable + receipt copied into the wave dir first. Disk guard checked green before the pass (/fast 27% used, 593G free).
