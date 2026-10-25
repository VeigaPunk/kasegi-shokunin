# ExecCaptureS041 — S041 capture report (wave 1, round 26)

- Seat: `L1Kasegi26.ExecCaptureS041`
- Date: 2026-10-25 (UTC)
- Scope: capture JPCERT/CC 2026 partnership guideline as S041; sole owner of
  `corpus/source-snapshots/round-26/S041.txt`. No manifest written (e6 owns it).

## Command executed

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-26/S041.txt
```

## Capture log line (verbatim)

```
S041 status=200 fetched_bytes=1338665 snapshot_bytes=147267 sha256=e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47 utc=2026-10-25T12:34:17Z out=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-26/S041.txt
```

## Recorded metrics

| Field | Value |
|---|---|
| exit code | 0 |
| HTTP status | 200 |
| sha256 (log) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` |
| sha256 (on-disk `sha256sum`) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (matches) |
| fetched_bytes | 1338665 |
| snapshot_bytes | 147267 |
| utc | 2026-10-25T12:34:17Z |
| snapshot path | `corpus/source-snapshots/round-26/S041.txt` |
| snapshot lines | 2354 |

Toolchain: `pdftotext` 26.08.0 (`/usr/bin/pdftotext`, present before run; no
install needed, no pacman transaction). Instrument: `corpus/instruments/capture-source.py`.

## Content verification (grep hits)

- Division-of-labour paragraph — `社内での脆弱性取扱`:
  - line 1671: `を規定しています。一方、ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱`
  - Context: the paragraph spans lines 1669–1673 (section "2. 国際標準の概要",
    ISO/IEC 29147:2014 external handling vs ISO/IEC 30111:2013 in-house
    process), preamble "これらの関係を次の図に示します。" at line 1673.
- 図1 caption — `出所：ISO/IEC 29147:2014 を元に作成`:
  - line 1678, immediately following "図 1" (line 1676) and title
    "ISO/IEC 29147 と ISO/IEC 30111 の対応" (line 1677).
  - Same caption string also appears at lines 1777, 1867, 1908, 1974 (other
    figures in 付録６); line 1678 is the 図1 caption.

## Files changed

- `corpus/source-snapshots/round-26/S041.txt` (created, sole owner).
- `.ufo/waves/round-26/wave1/ExecCaptureS041.md` (this report).

## Risks / blockers

- None. Capture succeeded, digest matches on disk, both required strings present.
- Not touched: no manifest file (e6 owns it), no claims.json, no SOURCES.md row
  (parent-side), no VCS writes.
