# AttackC1 — entry quality audit: `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`

Round 26, wave 2 (falsify + integration closure). Seat: L1Kasegi26.AttackC1 (read-only, leaf).
Scope: audit the division-of-labour knowledge entry against Q1–Q9 (QUALITY.md), the S041 capture,
and the README F11 row. Verdict: **PASS** — no defect found in scope.

## What was checked and how

- Entry bytes: `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (54 lines, matches the
  round-26 lesson's record).
- Captures: `corpus/source-snapshots/round-26/S041.txt` (2,354 lines, sha256
  `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` = manifest binding),
  `corpus/source-snapshots/round-25/S039.txt`, `corpus/source-snapshots/round-25/S040.txt`.
- Manifest: `corpus/source-snapshots/round-26/manifest.json` (7 S041 assertions).
- Executed the entry's own `recheck:` command: exit **0**, `S041:sha256 OK`, all manifest quotes
  `occurrences=1` or `anchor=…-ok` (Q2a anchor-verified).
- All quote presence/length/occurrence checks and the edition-rule counts were run against the
  capture bytes (exact commands below).

## Q1 — headers

Line 2 `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録6 §2 p.45,
division paragraph L1667-1672 and 図1 L1676-1678 (capture corpus/source-snapshots/round-26/S041.txt)`:
row id S041 + URL + exact anchor, capture path named. ✓
Line 3 `verified-at: 2026-10-25` — ISO date, matches the capture date (2026-10-25T12:34:17Z). ✓
Line 4 `recheck:` is a single runnable command with `cd <lane-root> &&` prefix and the
`--manifest corpus/source-snapshots/round-26/manifest.json --source S041` path; it fails closed when
the capture is absent (sha256 is checked). Ran it: exit 0. ✓

## Q3/Q8/Q9 — quotes present, verbatim, ≤70 chars, correct line refs

All 11 table quotes verified verbatim in their captures; all ≤70 characters (max 60); all S041
quotes at exactly the cited line numbers.

| quote id | location cited | verified |
|---|---|---|
| jpcert-29147-subject | S041.txt:1667 | present, occurrences=1, len 34 |
| jpcert-outward-exchanges | S041.txt:1669 | present, occurrences=1, len 8 |
| jpcert-outward-enum | S041.txt:1670 | present, occurrences=1, len 35 (starts at the wrapped word 弱性; L1669 ends 脆) |
| jpcert-30111-half1 | S041.txt:1671 | present, occurrences=1, len 33 (= manifest Q1a) |
| jpcert-30111-half2 | S041.txt:1672 | present, occurrences=1, len 34 (= manifest Q1b) |
| jpcert-fig1-title | S041.txt:1677 | present, occurrences=1, len 33 |
| jpcert-fig1-caption | S041.txt:1678 | present, occurrences=**5** — anchor documented and exact: repeat lines are 1777/1867/1908/1974, all verified |
| hitachi-step1-29147 | S039.txt:497 | verbatim (the `...` is inside the capture line itself), len 50 |
| hitachi-step2-30111 | S039.txt:498 | verbatim, len 49 |
| hitachi-step3-29147 | S039.txt:499 | verbatim, len 49 |
| cisco-iso-29147-2018 | S040.txt:58 | verbatim, len 60 |

Q9 binding: exactly-once quotes are exactly-once (verified counts); the sole repeating quote (fig1
caption) carries the anchor line and its repeat locations in the entry. ✓

## Thesis grounded / no invented claims

- Division sentence (L1667-1672): 29147 = ソフトウエア製品に係る事業者 (製品開発者, オンラインサービス事業者,
  中間ベンダ) and 社外とのやりとり (外部からの脆弱性に関する情報の受領、ユーザに対する脆弱性対策のアドバイザリ配布等);
  30111 = 社内での脆弱性取扱いのプロセス (脆弱性の検証、脆弱性対策の開発等) の指針を提供. All load-bearing
  clauses map to the captured text at L1667-1672. ✓
- Figure claim (L1676-1678): 図 1 title + caption （出所：ISO/IEC 29147:2014 を元に作成） →
  "drawn based on ISO/IEC 29147:2014" is an accurate rendering of the caption. ✓
- Edition rule (Q5 falsifiable rules): `29147:2014` occurs **24×** in S041.txt and `29147:2018`
  occurs **1×** in S040.txt — both counts reproduced exactly as printed in the entry. ✓
- Hitachi corroboration: L497-499 map step 1 (入手) and step 3 (情報公開) to 29147 and step 2
  (調査ならびに対策) to 30111; the entry's reading ("the internal investigation phase — not receipt or
  announcement — is the 30111 piece") matches. ✓
- No fabricated or unverifiable assertion found anywhere in the entry.

## No staged F19/F20 ground leak

- The entry contains no `F19`/`F20` text and no reference to un-admitted staged ids (S076/S064/S068)
  or to the rejected `vendor-cvd-policy-crosswalk-2026-10-23.md` candidate.
- The only staged-file mention is the `ground:` adoption note (line 5): "adopts the staged entry
  iso-29147-and-30111-division-of-labour-2026-10-23.md, re-grounded on the round-26 capture … (S041,
  付録6 §2)" — this matches claims.json C2's `staged_entries` and is a disclosure, not a leak; the
  entry's content is fully re-grounded on S041 (verified above). ✓

## Title/scope vs README F11 row

- Title: "Division of labour between ISO/IEC 29147:2014 and ISO/IEC 30111:2013" — matches the F11
  row topic ("ISO/IEC 29147/30111 division-of-labour meta") and the row's "Treat 29147 as the
  vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the
  edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018)". ✓
- The F11 row's entry cell names the actual unsuffixed filename (M26-3 fix landed); the entry is
  listed in `corpus/instruments/knowledge-expected.txt` (39 entries). ✓

## Verification commands (all run on 2026-10-25 UTC, from the lane root)

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041   # exit 0
# quote presence/occurrence/length + caption repeat lines + edition counts (python, inline):
#   S041 quotes: all present at cited lines, occurrences=1 except caption (5: 1678/1777/1867/1908/1974)
#   all 11 quote lengths <=70 (max 60)
#   '29147:2014' in S041.txt = 24; '29147:2018' in S040.txt = 1
#   S039.txt:497-499 verbatim lines confirmed
grep -nE 'F19|F20|staged|2026-10-23|S076|S064|S068|vendor-cvd' corpus/knowledge/iso-29147-and-30111-division-of-labour.md   # only line 5 (ground adoption note)
```

## Verdict

**PASS.** All Q1–Q9 criteria audited hold; every quote is present verbatim at its cited capture line
with correct occurrence binding; thesis and falsifiable rules are grounded in the captured bytes; no
invented claims; no staged F19/F20 ground leak; title/scope consistent with the README F11 row. No
defect in scope. Residual note (not a defect): the fig1 caption quote is repeated 5× and is
documented as anchored at L1678; the manifest pins only Q1a/Q1b (the two half-quotes used by this
entry), the other five S041 quotes being exactly-once and verified directly.
