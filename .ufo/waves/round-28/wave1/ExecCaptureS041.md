# ExecCaptureS041 — round-28 re-capture of S041 (JPCERT/CC 2026 P-guideline)

- Seat: `ExecCaptureS041` (round 28, wave 1, build+attack)
- Date: 2026-10-25 (UTC)
- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base c9f8b115a098c65356e4b3b6048af45a37ab8395)
- Claim served: C2 (coverage) — re-grounding the S041 capture for the F12 entry
- Sole write scope: `corpus/source-snapshots/round-28/S041.txt` (plus this report and my
  own receipt). No other production file touched; no manifest, no SOURCES.md, no VCS write.

## Command executed (verbatim, cwd = lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf --out corpus/source-snapshots/round-28/S041.txt
```

State note: this item depends on **no** in-flight production file. `capture-source.py` is not
being edited this round; the run used the present committed bytes,
`sha256sum corpus/instruments/capture-source.py` =
`e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`.
No PRE-STATE label is owed here and no post-change re-run is required for the capture itself.
Re-verified after the run: same digest `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`,
so the capture was produced and stays bound to the bytes named in this report.

## Capture log line (verbatim stdout) and exit

```
S041 status=200 fetched_bytes=1338665 snapshot_bytes=147267 sha256=e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47 utc=2026-10-25T17:22:12Z out=corpus/source-snapshots/round-28/S041.txt
capture_exit=0
```

## Recorded metrics

| Field | Value |
|---|---|
| exit code | 0 |
| HTTP status | 200 |
| fetch timestamp (UTC) | `2026-10-25T17:22:12Z` |
| sha256 (log) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` |
| sha256 (on-disk `sha256sum`) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` — matches the log |
| fetched (PDF) bytes | 1338665 |
| snapshot bytes | 147267 |
| snapshot lines | 2354 |
| snapshot path | `corpus/source-snapshots/round-28/S041.txt` |
| instrument | `corpus/instruments/capture-source.py` sha256 `e18318888…633dc18` |
| toolchain | `pdftotext` 26.08.0 (`/usr/bin/pdftotext`, pre-existing; no install, no pacman) |

Upstream corroboration (independent `curl -sI`, same UA, 2026-10-25):

```
HTTP/2 200
content-type: application/pdf
content-length: 1338665
last-modified: Thu, 01 Oct 2026 00:49:04 GMT
etag: "146d29-65cbcc8478000"
```

`content-length: 1338665` equals the instrument's `fetched_bytes`, so the body size is
corroborated outside the instrument. `last-modified` 2026-10-01 postdates the PDF signature
stamp (2026-09-29 18:01:10 +09:00, snapshot line 7).

## Byte-for-byte comparison with the round-26 capture (authoritative, on committed bytes)

```
$ sha256sum corpus/source-snapshots/round-26/S041.txt corpus/source-snapshots/round-28/S041.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-26/S041.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-28/S041.txt

$ wc -c corpus/source-snapshots/round-26/S041.txt corpus/source-snapshots/round-28/S041.txt
147267 corpus/source-snapshots/round-26/S041.txt
147267 corpus/source-snapshots/round-28/S041.txt
294534 total

$ cmp corpus/source-snapshots/round-26/S041.txt corpus/source-snapshots/round-28/S041.txt ; echo cmp_exit=$?
cmp_exit=0
```

**Verdict: IDENTICAL.** `cmp` exit 0, equal digests, equal byte counts (147267). The upstream
PDF served at 2026-10-25T17:22:12Z extracts to the same bytes as the round-26 capture taken at
2026-10-25T12:34:17Z, and the upstream body length is unchanged (1338665 both times).
Honest scope of the claim: this proves snapshot-text identity plus equal upstream body size;
it does not by itself prove PDF-body identity against a hypothetical equal-length different
PDF, which is implausible here and is not claimed.

## Content verification

### `起算日` grep hits — 9 lines (round-28 bytes)

```
$ grep -n '起算日' corpus/source-snapshots/round-28/S041.txt
305:なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、
340:本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。
430:IPA は、起算日から 1 年以上経過した届出について、発見者から情報非開示依
648:みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、
786:日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。公表に更なる時
1170:起算日の連絡
1171:起算日の連絡
1186:5 起算日の連絡
1211:5起算日の連絡
```

Reading of the hits (context lines cited from the same capture):

- **L340 is the operative definition**, under the 注釈 4 list (L338–L339 are the numeral
  lines `4`/`5`): `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。`
  followed by `具体的には、` (L341) — i.e. the clock for the 45-day publication estimate starts
  at the first contact attempt under Ⅳ.4.2).
- L305 / L430 — the >1-year rule: the finder may request withdrawal of a non-disclosure
  request once 1 year has elapsed from `起算日` (L305 finder side, L430 IPA side).
- L648 (Ⅳ.3, IPA handling) and L786 (Ⅳ.5, product developer handling) — the 45-day
  post-`起算日` publication target, both with the cross-reference `起算日、２．注釈 4 を参照`.
- L1170, L1171, L1186, L1211 — 付録2 flowchart labels (`起算日の連絡`) and the section heading
  `5 起算日の連絡`; these are diagram/heading text, not additional normative statements.

### Edition stamp

```
$ grep -n '2026 年 10 月' corpus/source-snapshots/round-28/S041.txt
10:2026 年 10 月
```

One hit, at L10, in the cover block directly under the title (L8 `情報セキュリティ早期警戒`,
L9 `パートナーシップガイドライン`). The signature block at L2–L7 pins the document build:
`日付 : 2026.09.29 18:01:10 +09'00'`. **Edition stamp 2026年10月 confirmed.**

## Cross-check for ExecManifest (informational — `manifest.json` is not my file)

The round-26 manifest quote assertions still resolve against the round-28 bytes at the same
line numbers (expected, given the byte identity; measured rather than assumed):

| Quote | count | lines |
|---|---|---|
| Q1a | 1 | 1671 |
| Q1b | 1 | 1672 |
| Q2a | 2 | 1708, 1874 (anchor 1874 as pinned in round 26) |
| Q2b | 1 | 1851 |
| Q3 | 1 | 1868 |
| Q4 | 1 | 1916 |
| Q5 | 1 | 1813 |

Q2a is the only non-unique assertion; it is the documented two-occurrence case, not a new
anchor defect. This table is evidence handed to ExecManifest, not a manifest verdict.

## Files written

- `corpus/source-snapshots/round-28/S041.txt` (created; my sole production scope)
- `.ufo/waves/round-28/receipts/ExecCaptureS041.txt` (my own receipt)
- `.ufo/waves/round-28/wave1/ExecCaptureS041.md` (this report)

## Not run / deferred to L1

- `source-recheck.py` over the round-28 manifest cannot run yet: `corpus/source-snapshots/round-28/manifest.json`
  does not exist at my run time (owned by `ExecManifest`). Post-landing command for the L1:

  ```
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
  ```

  It must exit 0 and report the pinned sha256 as `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
  if the manifest is built from these bytes. **Unrun ⇒ not passed**; this seat asserts only the
  capture, the comparison, and the greps above.

## Risks / blockers

- None for this item. Capture exit 0, on-disk digest matches the log, `cmp` against round-26 is
  byte-identical, both required strings present.
- Concurrency observation, not a conflict: `corpus/source-snapshots/round-28/S042.txt`
  (60508 bytes) was present when I listed the directory. I did not write or verify it;
  `ExecCaptureS042` owns it.
- No tool installs or upgrades were performed (no pacman transaction attempted; host policy is
  paused anyway).
- Did not touch: `claims.json`, `manifest.json`, `SOURCES.md`, `README.md`, `QUALITY.md`,
  `SKILL.md`, `LOG.md`, `SCORECARD.md`, any round-27 artifact, any VCS state.
