# C2S036Quote — S036 capture re-opened, all entry quotes exactly-once + located (wave 2)

Seat: `L1Kasegi25.C2S036Quote` (read-only reviewer). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. No file outside this report was
written; no VCS operation; no tool install/upgrade (nothing installed — pacman
paused, nothing needed).

## Verdict

**CONFIRMED.** Every S036 quote asserted by the round-25 manifest is byte-exact,
occurs **exactly once** in `corpus/source-snapshots/round-25/S036.txt`, and sits on
the capture line its `location` field claims. Both knowledge entries quote S036
only through those same strings. Wave-1 receipts (`EntryJapanVendors.md`,
`RevQuotesJP.md`, `EntryCiscoCrosswalk.md` union) are accurate; no correction needed.

## Capture integrity

`sha256sum` of the committed capture matches both the manifest's `sha256` field and
`.ufo/waves/round-25/capture-log.txt` (fetched `2026-10-25T08:14:25Z`, status=200):

```
S036.txt sha256 = 022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950   (match ×3)
87 content lines, UTF-8, no U+00A0/U+202F/non-ASCII spaces anywhere in the file.
```

## Exact-once + located — measured

Byte-exact substring count over the whole file (`txt.count(q)`), line hits, and the
line number parsed from each manifest `location` field:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036
S036:sha256 OK
S036:Q1..Q8 OK occurrences=1        exit=0
```

| id | occurrences in S036.txt | hit line | claimed line | section in `location` matches capture | verdict |
|----|------------------------|----------|--------------|----------------------------------------|---------|
| Q1 | 1 | 19 | 19 | 情報収集 header at L17 | OK |
| Q2 | 1 | 14 | 14 | 対象範囲 header at L13 | OK |
| Q3 | 1 | 28 | 28 | 公開 対象範囲 at L26-27 | OK |
| Q4 | 1 | 30 | 30 | same block | OK |
| Q5 | 1 | 22 | 22 | 影響の確認 at L20-21 | OK |
| Q6 | 1 | 21 | 21 | same | OK |
| Q7 | 1 | 44 | 44 | JVNでの公開 at L43 | OK |
| Q8 | 1 | 19 | 19 | substring of Q1, same line — location says so | OK |

Q8 (`脆弱性報奨金制度を含む外部からの報告`) is an exact substring of Q1's line-19
sentence; the manifest `location` states "(substring of Q1)" — no hidden double
count. Q1 and Q8 are the only quotes sharing a line.

## Entry-side check — every S036 string an entry shows is one of these eight

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` — all 8 quotes
  appear **once each** as `> ` blockquotes (lines 23, 35, 40, 45, 53, 56, 64, plus
  attribution lines L24/36/41/46/54/57/65 naming `S036.txt:` with the correct line
  numbers). Verified mechanically: each blockquote occurs exactly once in the
  capture and on the line its attribution cites.
- `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` — cites
  S036 Q2/Q4/Q5/Q7/Q8 inline (L54-58, one occurrence each); all five strings are
  byte-identical to the capture. No S036 string appears in either entry that is
  absent from the manifest record (the union discipline wave 1 reported holds).
- Manifest S036 record is byte-identical to the wave-1 authored list
  `.ufo/waves/round-25/wave1/quotes-vendor-jp.json` — 8/8 ids, 8/8 strings equal.

## Commands run (exact)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/source-snapshots/round-25/S036.txt        # 022ca4f4…ceb950
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036
   -> 9 OK lines, exit 0
python3 - <<…   # txt.count(quote), per-line hits, location parse (table above)
grep -nF '> '  entries; cross-checked every S036-cited blockquote
grep -n 'S036' corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

## Residual risk / gaps

- **Line-range headers are prose, not manifest assertions.** The JP entry header
  cites `S036.txt:14-44` and the crosswalk cites `(L13-L15)`, `(L16-L25)`,
  `(L27-L30)`, `(L43-L44)`. All were spot-checked and correct (対象範囲 header L13
  → bullets L14-15; flow L16-25; 公開 対象範囲 L27-30; JVN L43-44). These ranges
  are not instrument-verified; only the quote lines are.
- Snapshot fidelity to the live cybozu.co.jp page rests on the wave-1 fetch
  (`status=200`, capture-log); I did not re-fetch (out of scope, read-only).
- Untracked files: `corpus/source-snapshots/round-25/` and both entries are `??`
  in `git status` — committed to the worktree but not yet to the index. The
  sha256 evidence above is on the working-tree bytes, which are the bytes of record.

No actionable finding against the wave-1 S036 result; smallest correction is none.
