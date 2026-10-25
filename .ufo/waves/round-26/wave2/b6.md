# AttackB6 — manifest quote recheck re-run (S041)

- Seat: `L1Kasegi26.AttackB6` (UFO-FSD reviewer, read-only)
- Round: kasegi-shokunin round 26, wave 2 (falsify)
- Item: milestone "manifest quote recheck re-run" — run `source-recheck.py --source S041`, record per-quote verdicts + exit (expect 0), confirm quotes ≤70 chars and locatable.
- UTC: 2026-10-25
- Verdict: **PASS — C2 S041 source-side binding holds; exit 0; all 7 quotes ≤70 chars and locatable in the pinned snapshot.**

## Command run

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041
echo "EXIT_CODE=$?"
```

## Instrument output (verbatim) and exit

```
S041:sha256 OK
S041:Q1a OK occurrences=1
S041:Q1b OK occurrences=1
S041:Q2a OK occurrences=2 anchor=1874-ok
S041:Q2b OK occurrences=1
S041:Q3 OK occurrences=1
S041:Q4 OK occurrences=1
S041:Q5 OK occurrences=1
EXIT_CODE=0
```

Exit 0 as expected. sha256 of `S041.txt` binds the snapshot bytes (`e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` matches manifest).

## Per-quote verdicts

| quote | verdict | evidence |
|---|---|---|
| Q1a | OK, occurrences=1, unique | no anchor needed (Q9) |
| Q1b | OK, occurrences=1, unique | no anchor needed |
| Q2a | OK, occurrences=2, anchor=1874-ok | non-unique; anchor verified against raw snapshot (Q9) |
| Q2b | OK, occurrences=1, unique | no anchor needed |
| Q3 | OK, occurrences=1, unique | no anchor needed |
| Q4 | OK, occurrences=1, unique | no anchor needed |
| Q5 | OK, occurrences=1, unique | no anchor needed |

## Quote length check (≤70 chars)

Measured with Python `len()` on the manifest quote strings:

| quote | length | ≤70 |
|---|---|---|
| Q1a | 33 | yes |
| Q1b | 34 | yes |
| Q2a | 22 | yes |
| Q2b | 14 | yes |
| Q3 | 35 | yes |
| Q4 | 28 | yes |
| Q5 | 26 | yes |

All ≤70 chars (also all ≤25 words, satisfying Q3's word bound).

## Locatability check (manual, against pinned S041.txt)

Read the cited snapshot lines; every quote text is present at the exact lines named in the manifest `location` fields:

| quote | manifest location | snapshot line read | found |
|---|---|---|---|
| Q1a | 付録6 §2 p.45 L1671 | 1671 ends `…ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱` | yes |
| Q1b | 付録6 §2 p.45 L1672 | 1672 starts `いのプロセス（脆弱性の検証、脆弱性対策の開発等）の指針を提供します。` | yes |
| Q2a | 付録6 §4 p.46-47 L1708 and L1874 | 1708 contains `脆弱性公開ポリシーには、ベンダへの連絡方法、セキュアな通信オ`; 1874 contains `・脆弱性公開ポリシーには、ベンダへの連絡方法、セキュアな通信オプショ` | yes, both |
| Q2b | 付録6 §4 p.46-47 L1851 | 1851 exact `b）セキュアな通信オプション` | yes |
| Q3 | 付録6 §4 p.46 L1868 | 1868 exact `P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません` | yes |
| Q4 | 付録6 §4 p.46-47 L1916 | 1916 contains `…受信した旨を 7 日以内に返信することが必要となります。` | yes |
| Q5 | 付録6 English section L1813 | 1813 exact `6.2 Minimum policy aspects` | yes |

Non-unique Q2a's two occurrences match the manifest's two cited line numbers (1708, 1874); the instrument additionally verified anchor 1874 holds the quote (window check), so the Q9 binding (exactly-once or anchored) is satisfied for every quote.

## Notes

- No tools installed (none required; `python3` already present). No VCS mutations, no edits outside `.ufo/waves/round-26/wave2/`.
- This run is a local pinned-capture check (Q7: captured-source comparison, not fresh network verification); it does not re-fetch the JPCERT/CC PDF.
- S041 is the only source in the round-26 manifest (S040 skipped per manifest note); `--source S041` selected it and the run covered all 7 quotes.
