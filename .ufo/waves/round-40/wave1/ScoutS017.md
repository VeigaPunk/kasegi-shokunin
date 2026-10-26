# ScoutS017 receipt — S017 decision input (round 40)

Verdict: **MINE (reachable, substantive, new ground).** The L1/ScribeRows decide the row status; I did not write SOURCES.

## Fetch facts (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0)
Three fetches of https://projectzero.google/2025/07/reporting-transparency.html, all HTTP 200, text/html, 0 redirects, 14764 raw bytes each:
| UTC | purpose | raw sha256 |
|---|---|---|
| 2026-10-26T21:15:47Z | first probe | 80f2f7ffc08295cc73dd2278fcf9b247e5761a31105df4b1b246d0e13c9708d6 |
| 2026-10-26T21:16:06Z | `corpus/instruments/capture-source.py --id S017 --kind html` (printed: `S017 status=200 fetched_bytes=14764 snapshot_bytes=5058 sha256=3b6aaf1f…83fe utc=2026-10-26T21:16:06Z`) | not printed by tool |
| 2026-10-26T21:16:32Z | header-bearing fetch (`-D`), the manifest record's fetch | 4bd7186ccb950a56d466833c242f31d4507c010f7694cfa711363d9bf00857d0 |

Raw sha256 differs per fetch because the page embeds a per-request CSP nonce; the converted snapshot is stable: capture-source.py's `html_to_text()` on the 21:15:47Z and 21:16:32Z bodies both give sha256 3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe, equal to the tool's own output. Response headers: `content-type: text/html`, `content-length: 14764`, `server: sffe`, no `last-modified`, `cache-control: no-cache`.

Snapshot: 5058 bytes, 39 lines, sha256 3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe.

## (a) Reachable and substantive?
Yes. Title "Policy and Disclosure: 2025 Edition - Project Zero" (L1), dated 2025-Jul-29 (L13), by Tim Willis (L14-15). Full article text is in the static HTML (no JS shell): trial policy (L20-28), rationale (L29-32), attacker-risk limits (L33-37). The "90+30" model and the "upstream patch gap" are defined (L16-17).

## (b) Does it teach ground the lane does not hold?
Yes. Checks run: grep of corpus/**/*.md excluding source-snapshots for `reporting transparency|upstream patch gap|patch gap|90\+30|project zero|big sleep`, and of the S017 id.
- Only mentions of Project Zero: `knowledge/coordinated-disclosure-timelines.md` (S005 only: the 90-day deadline, the 30 days after a fix, the 14-day grace), `knowledge/ai-assisted-finding-validation.md:39` (S010 Naptime), QUALITY.md Q4 (attribution). No hit anywhere in knowledge/ for "Reporting Transparency", "patch gap" or "upstream patch gap".
- S017 appears only in `corpus/SOURCES.md:23` (status `queued`) and `corpus/lessons/round-22.md:93` (a Gate row: quote, no knowledge entry, no capture). `grep -l S017` over corpus *.md/*.txt/*.tsv/*.json outside `.ufo/waves` returns exactly those two files.
- Frontier rows F01-F22 (corpus/README.md): F02 timelines hold S003/S004/S005; F06 holds upstream/downstream roles from FIRST (S018: "an upstream fix is not downstream evidence"); none holds a researcher-side policy that publicly pre-announces a report's existence. F06's S018 gives the roles; S017 adds the first-party Project Zero trial: public notice within ~1 week naming vendor/project, product, report date and deadline expiry, with the 90+30 clock unchanged (L22-27), and the "upstream patch gap" framing (L17), which is an earlier delay than the user-side patch gap.
- Candidate entry shape: attributed to Project Zero's trial, not general practice; notice discloses no technical detail (L34); "trial" status (L20, L37) so no universal claim (QUALITY Q4). It extends F02 (a clock-start/notice event beyond the report) or F06 (downstream awareness) rather than needing a new frontier row.
- Unknown: whether Project Zero ended the trial after 2025-07-29; this capture does not say, so any entry must say "as of the 2025-07-29 post".

## (c) Located quote (≤25 words)
Q1 (20 words), **L23** of the capture, section "The Trial: Reporting Transparency" (heading L21):
“within approximately one week of reporting a vulnerability to a vendor, we will publicly share that a vulnerability was discovered.”
Also pinned: Q2 (L34, "Will this help attackers?"): “no technical details, proof-of-concept code, or information that we believe would materially assist discovery will be released until the deadline.” (20 words, matches the round-22 Gate row quote); Q3 (L34): “Reporting Transparency is an alert, not a blueprint for attackers.”

## Validation
Scratch manifest `{schema_version:1, sources:[record]}` run through `python3 corpus/instruments/source-recheck.py --manifest man.json --source S017`, rc=0:
```
S017:sha256 OK
S017:Q1 OK occurrences=1 anchor=23-ok
S017:Q2 OK occurrences=1 anchor=34-ok
S017:Q3 OK occurrences=1 anchor=34-ok
```

## Deliverables (beside this receipt)
- `ScoutS017.capture.txt` — byte-identical to capture-source.py output; 39 lines; sha256 3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe. The landed path should be `corpus/source-snapshots/round-40/S017.txt` (record `path` is `S017.txt`, the bare name, as in the r38/r39 manifests).
- `ScoutS017.manifest-record.json` — one `sources[]` record in the round-38 html shape (fields id, path, url, fetched_utc, fetched_bytes, snapshot_bytes, lines, sha256, normalized, raw_sha256, http, quotes), plus the fields the spec names: `files` ["S017.txt"], `status` 200, `size_bytes` 5058. 49 lines; sha256 138622e28f118cb313691276fc4d143c8f8da385bc7fe92458373e3a3c796917. Its `fetched_utc` is 2026-10-26T21:16:32Z, the header-bearing fetch whose raw_sha256 it records; the snapshot sha is identical to the 21:16:06Z tool run. `last_modified` is null (header absent). `files`, `status`, `size_bytes` are not fields of the existing committed records (they use `http.status` and `snapshot_bytes`): the L1 may drop them when landing if the binding check rejects unknown keys.

## Tooling
No installs. Read-only repo access only; no git mutations. Scratch `/fast/scratch/hyaku/kasegi-r40/ScoutS017/` removed before yield. Disk guard checked (`/fast/scratch/hyaku` 27% used) before the pass.
