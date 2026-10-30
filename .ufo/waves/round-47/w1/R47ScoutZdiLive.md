# R47ScoutZdiLive — S075 live re-open

Axes: depth:verifiability (independent live fetch/digest/quote evidence); coverage (all ten S075 manifest quotes).

## Observed findings

**Zero normalized-capture drift, high confidence.** Two independent concurrent fetches returned HTTP 200 at `2026-10-30T11:42:53Z`, each fetching 25,321 HTML bytes and producing 4,701 snapshot bytes / 60 lines. Both snapshots equal the committed S075 snapshot byte-for-byte, SHA-256:

`9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`

The manifest pins this digest at `corpus/source-snapshots/round-47/manifest.json:16`. All ten quotes locate exactly once in **both live snapshots**, at their unchanged manifest anchors:

| Quote | Live line, both fetches | Manifest record line |
|---|---:|---:|
| Q1 | 21 | 26–28 |
| Q2 | 23 | 31–33 |
| Q3 | 24 | 36–38 |
| Q4 | 24 | 41–43 |
| Q5 | 24 | 46–48 |
| Q6 | 24 | 51–53 |
| Q7 | 25 | 56–58 |
| Q8 | 25 | 61–63 |
| Q9 | 25 | 66–68 |
| Q10 | 26 | 71–73 |

**Page-visible revision date:** none identified in either normalized capture. The only calendar date is the footer `©2026 TrendAI™ Zero Day Initiative™ (ZDI).` at line 39; this is a copyright year, not a policy revision date. Policy text occupies lines 20–27.

## Commands and receipts

Working directory for all Python commands: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

Executed twice, substituting `N=1` and `N=2`:

```sh
python3 corpus/instruments/capture-source.py --id S075 --url https://www.zerodayinitiative.com/advisories/disclosure_policy/ --out /fast/scratch/hyaku/kasegi-r47/R47ScoutZdiLive/S075-live-N.txt --kind html
```

Both exit 0, no stderr. Printed receipts:

```text
S075 status=200 fetched_bytes=25321 snapshot_bytes=4701 sha256=9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1 utc=2026-10-30T11:42:53Z out=/fast/scratch/hyaku/kasegi-r47/R47ScoutZdiLive/S075-live-1.txt
S075 status=200 fetched_bytes=25321 snapshot_bytes=4701 sha256=9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1 utc=2026-10-30T11:42:53Z out=/fast/scratch/hyaku/kasegi-r47/R47ScoutZdiLive/S075-live-2.txt
```

Independent digest/byte comparison and exact per-line quote lookup used Python `hashlib.sha256`, byte equality, and each manifest quote as a literal substring of each live line. Both printed `equals_committed=True`; each Q1–Q10 printed its single line above and `anchor_exact=True`.

Required committed-source recheck:

```sh
python3 corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-47/manifest.json --source S075
```

Exit 0, no stderr:

```text
S075:sha256 OK
S075:Q1 OK occurrences=1 anchor=21-ok
S075:Q10 OK occurrences=1 anchor=26-ok
S075:Q2 OK occurrences=1 anchor=23-ok
S075:Q3 OK occurrences=1 anchor=24-ok
S075:Q4 OK occurrences=1 anchor=24-ok
S075:Q5 OK occurrences=1 anchor=24-ok
S075:Q6 OK occurrences=1 anchor=24-ok
S075:Q7 OK occurrences=1 anchor=25-ok
S075:Q8 OK occurrences=1 anchor=25-ok
S075:Q9 OK occurrences=1 anchor=25-ok
```

## Control, inference, and limitations

**Do-nothing control:** rechecking only the existing committed S075 snapshot produces the preceding success receipt without accessing the live page: `source-recheck.py:156–174` reads and hashes the manifest-relative local file. Thus that receipt alone cannot establish live freshness. This seat discriminates against that control with two actual URL fetches, HTTP receipts, independent live hashes/byte comparison, and live quote location. No C1/C2 counter or full mutant battery was run; no claim is made about the disclosed survivors.

The capture tool removes script/style and HTML tags, unescapes entities, and collapses whitespace (`capture-source.py:39–53,82–96`). Therefore zero drift applies to normalized text, **not proven identical raw HTML**, headers, images, or rendered-only content. Two same-second fetches establish current observations, not temporal stability or future freshness. No browser-rendered revision-date inspection was performed. No exported contract was changed or investigated; no semantic/LSP assertion is made.

The disk guard command `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` printed `/fast/scratch/hyaku 54% 376.3G` free before these small fetches; it subsequently timed out after 30 seconds while listing consumers. No ENOSPC occurred. The explicit seat scratch directory was removed in Python `finally` after evidence collection (`SCRATCH_REMOVED /fast/scratch/hyaku/kasegi-r47/R47ScoutZdiLive`). No tools installed or upgraded; no git/jj mutations or production-file changes.

Report: `.ufo/waves/round-47/w1/R47ScoutZdiLive.md`
