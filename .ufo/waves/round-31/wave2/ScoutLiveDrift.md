# ScoutLiveDrift — S048 live drift check (wave 2, read-only)

Scratch: /tmp/tmp.5fErkyKMNN (outside lane). Instrument UA only. Fetch time 2026-10-26T00:24Z (UTC). No lane file other than this receipt was written.

## Commands and output
1. `curl -A <instrument UA> https://www.microsoft.com/en-us/msrc/msvr` -> `http=200 bytes=81802`
2. `python3 corpus/instruments/capture-source.py --id S048 --url https://www.microsoft.com/en-us/msrc/msvr --kind html --out <scratch>/S048-now.txt`
   -> `S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=b5f0feb57ea4b2d0d967dba153f8c3ff1e3ff05bab25fc74a07c1ea34aaa2f14`
3. Same command again (S048-now2.txt) -> `sha256=64fd56ab4fab1ed32cc809f6cbff361363157e32cbc66a712892e2b3d89bf6a4` (same fetched_bytes=81802, snapshot_bytes=3755)
4. Pinned snapshot corpus/source-snapshots/round-31/S048.txt sha256 = `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55` (matches manifest pin); 97 lines. now and now2 are also 97 lines.

## diff -u pinned vs now (1 hunk, 1 line differs)
```
-This is the Trace Id: f97e6b1cb578f714d23850f80f018bb3
+This is the Trace Id: cb2370175b56ae471125fde8a080149f
```
diff -u now vs now2 (back-to-back, <1 s apart): the same single line differs (`cb23...` vs `d274bb00ad1d209e56d24710281a0dd5`).

## Findings
- Differing lines pinned vs live: **1 of 97** (snapshot line 2, the per-request Trace Id). No nav, date, or body-text change. Pinned and live are otherwise byte-identical.
- **No manifest assertion text changed.** Re-counted Q1-Q8 (normalized via source-recheck.py `normalize()`, imported read-only): each occurs exactly once in the pinned snapshot, S048-now.txt and S048-now2.txt.
- **Determinism: capture-to-capture sha256 is NOT equal**, even for two consecutive captures. Cause is one source only: the Trace Id (32 hex, new value each request). Fixing line 2 gives identical bytes (the diff proves this). So the whole-file sha pin is reproducible only for the committed file, never from a re-fetch; manifest purpose text already names this quirk and relies on quote assertions, not re-fetch hash equality. A re-fetch hash comparison would false-alarm every time.
- Raw HTML (not the snapshot) also varies between requests (same 81802 bytes, different sha256 each time): beyond the Trace Id, the CVToken / `window.mscv` / `window.msservercv` values (`CASMicrosoftCV<hex>.N`) change per request, in about 12 `>`-split fragments. These sit in head/script content that html_to_text drops (scripts stripped) or that never reaches the text, so they do not affect the snapshot.
- Q7 bound: the committed capture is a pinned record of what the page said at its capture time (2026-10-25 20:29 -03 file mtime). This live check shows it equal to the page about 55 minutes later (observed once, 3 fetches, 1 host). It is NOT a fresh network verification: `source-recheck.py S048` re-reads the committed file and says nothing about today's page. This drift check is a separate, single-instant observation and should be cited that way, not as ongoing currency. Page staleness over weeks/months is unmeasured [INFERENCE: stable marketing page, low churn, but unobserved].
- Suggested hardening for the L1 to route (not applied): a drift tool that masks `Trace Id: [0-9a-f]{32}` before comparing would make re-fetch comparison deterministic; capture-source.py today has no such mask.

Tooling: nothing installed. Model/config: not model-dependent.
