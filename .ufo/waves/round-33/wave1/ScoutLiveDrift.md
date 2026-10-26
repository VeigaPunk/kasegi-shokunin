# ScoutLiveDrift — S049/S050 live drift check (round 33)

Model: anthropic/claude-sonnet-5-5 (config route). Tooling installed: none.

## Commands and output
```
python3 corpus/instruments/capture-source.py --id S049 --url https://zc.cnvd.org.cn/news/helpList --kind html --out $S/S049-now.txt
S049 status=200 fetched_bytes=56674 snapshot_bytes=20272 sha256=962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8 utc=2026-10-26T04:16:06Z
python3 corpus/instruments/capture-source.py --id S050 --url https://security.360.cn/Reward/rules --kind pdf --out $S/S050-now.txt
S050 status=200 fetched_bytes=427391 snapshot_bytes=31016 sha256=2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888 utc=2026-10-26T04:16:16Z
```
($S = /fast/scratch/hyaku/kasegi-r33/ScoutLiveDrift; UA = instrument default.)

## Comparison against committed round-32 captures
| id | HTTP | fetched bytes | fresh text bytes / lines | fresh sha256 | committed sha256 | diff -u rc | differing lines |
|---|---|---|---|---|---|---|---|
| S049 | 200 | 56674 | 20272 / 426 | 962a451a...1cb8 | 962a451a...1cb8 (identical) | 0 | 0 |
| S050 | 200 | 427391 | 31016 / 630 | 2f9c6406...6888 | 2f9c6406...6888 (identical) | 0 | 0 |

Full sha256 values are in the output above; `sha256sum` of the committed files and the fresh files matched byte for byte, line counts 426/426 and 630/630, `diff -u` produced empty output for both.

## Quote text
Zero lines differ, so no candidate quote text from S049/S050 changed on the live pages. (Entry `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` had not landed when I checked, so I did not test individual quotes; with identical bytes every quote that appears in the committed capture also appears in the fresh text.)

## Bounds on what this proves (Q7)
- Fresh network read at 2026-10-26T04:16Z (S049) / 04:16:16Z (S050), ~2h02m after the capture commit 288ea9ac (author time 2026-10-25T23:14:00-03:00 = 02:14Z). This is a short-interval drift check only; it says nothing about the pages' content before the capture or after this fetch.
- The pinned snapshot is a text conversion captured at one instant. `source-recheck.py` on the pinned capture is NOT a fresh network verification; only this drift run is, and only for these two URLs at this time.
- Identical post-conversion text does not prove the raw HTML/PDF is byte-identical (fetched byte counts of the round-32 raw bodies are not recorded in the repo, so raw-body equality was not checked); it proves the extracted text the quotes are anchored to is unchanged.
- S049 page contains platform-issued tester VPN credential instructions; none quoted or reproduced here.

## Cleanup
Scratch dir $S removed at end of seat (diffs were empty; nothing to preserve).
