# ExecManifestRecheck — round-26 wave-1 manifest + quote recheck report

- Seat: `L1Kasegi26.ExecManifestRecheck` (leaf executor, sole owner of the round-26 snapshot manifest)
- Date: 2026-10-25 (UTC)
- Scope: build `corpus/source-snapshots/round-26/manifest.json`, then run `source-recheck.py --source S041`.
- Milestone: manifest + quote recheck — COMPLETE, all quotes PASS, exit 0.

## Files changed (owned paths only)

1. `corpus/source-snapshots/round-26/manifest.json` — created (schema_version 1; S041 entry with 7 quote assertions; S040 skipped).
2. `.ufo/waves/round-26/wave1/e6-recheck-results.txt` — created (verbatim output, per-quote verdicts, final exit status).
3. `.ufo/waves/round-26/wave1/ExecManifestRecheck.md` — this report.

## Manifest

- Schema: read `corpus/source-snapshots/round-25/manifest.json` first; matched its shape (`schema_version`, `purpose`, `sources[]` with `id`/`path`/`sha256`/`quotes[]` of `id`/`quote`/`location`), per `source-recheck.py` (SCHEMA_VERSION 1, ID regex, sha256 regex, quote min 12 normalized chars, anchor support).
- S041 entry: `path: "S041.txt"`, `sha256: e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`.
  - sha256 source: capture log line in `ExecCaptureS041.md` (`sha256=e18acbf…`); re-verified on disk with `sha256sum` — identical bytes.
  - Snapshot facts: 2354 lines, 147267 bytes, fetched 2026-10-25T12:34:17Z.
- S040 entry: SKIPPED. `corpus/source-snapshots/round-26/S040-live.txt` is absent (ScoutS040Probe fetch not landed; the only S040.txt in the tree is the round-25 snapshot). Noted in manifest `purpose`; no fabricated S040 row.

## Quote recheck

Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041` (from lane root).

Result: exit 0; every assertion OK:

```
S041:sha256 OK
S041:Q1a OK occurrences=1
S041:Q1b OK occurrences=1
S041:Q2a OK occurrences=2 anchor=1874-ok
S041:Q2b OK occurrences=1
S041:Q3 OK occurrences=1
S041:Q4 OK occurrences=1
S041:Q5 OK occurrences=1
```

## Corrections applied (reported per assignment)

1. **Q1** — requested quote "ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱いのプロセス（脆弱性の検証、脆弱性対策の開発等）の指針を提供します。" does **not** exist as contiguous bytes: the PDF text wrap splits the word 取扱/い (L1671 ends `…脆弱性取扱`, L1672 starts `いのプロセス…`). Corrected to two contiguous fragments:
   - Q1a `ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱` (L1671)
   - Q1b `いのプロセス（脆弱性の検証、脆弱性対策の開発等）の指針を提供します。` (L1672)
2. **Q2** — requested quote "脆弱性公開ポリシーには、ベンダへの連絡方法、セキュアな通信オプション" does **not** exist as contiguous bytes: the word セキュアな通信オプション is split mid-word at L1708→L1709 (`通信オ`+`プション、…`) and L1874→L1875 (`通信オプショ`+`ン、…`). Corrected to:
   - Q2a `脆弱性公開ポリシーには、ベンダへの連絡方法、` (occurs at L1708 and L1874; anchor=1874 verified as `anchor=1874-ok`)
   - Q2b `b）セキュアな通信オプション` (contiguous list element at L1851)
3. Q3, Q4, Q5 matched exactly as requested (L1868, L1916, L1813 respectively — single occurrences).

No quote failed in the final run; snapshot S041.txt was not edited.

## Risks / notes

- S040 has no round-26 snapshot; if ScoutS040Probe's `S040-live.txt` lands later in this wave, a follow-up manifest append (and re-run of the census/recheck) would be needed — out of scope for this seat, which froze the manifest at S041-only.
- No tool installs/updates were needed (python3 + source-recheck.py already present; no pacman transactions).
- No VCS writes; no claims.json/lessons edits; no edits to S041.txt.
