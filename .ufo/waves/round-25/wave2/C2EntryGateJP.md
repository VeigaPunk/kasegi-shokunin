# C2EntryGateJP — falsification of the JP entry (vendor-disclosure-policies-as-corpus-objects.md)

Seat: `L1Kasegi25.C2EntryGateJP` (critic, wave 2). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; read-only; no VCS write, no installs. Target: falsify
the JP entry Q1–Q6/Q9 (sources, dates, quotes, reject, attribution, documentation-only).

## Verdict

**Not falsified wholesale — the entry is largely sound, but three defects are found**, one of which
violates the wave-1 reviewer's own binding limit (U1). All claims, quotes, sources and dates are real;
none of the defects changes the C1/C2 numbers (the entry's recheck passes, the manifest validates, the
frontier/census hold). Smallest corrections below require no production edit.

| gate | verdict | evidence |
|---|---|---|
| Q1 header order | PASS | H1 at line 1; `source:` L3–6, `verified-at:` L7, `recheck:` L8, `ground:` L9. Order holds. |
| Q1 exact anchor | **minor defect** | S039 header says `(capture … S039.txt:491-519)` and names only 4-IRT intro / 1.2 / 1.3, but the entry quotes L520 (1.3) and L557 (1.5). Header under-covers. |
| Q2 tier-A source | PASS | S036–S039 all tier A (`corpus/SOURCES.md:42-45`), admitted this round (rows dated 2026-10-25). |
| Q3 verbatim quotes | **one gap** | 27/27 blockquotes verified verbatim + exactly-once at cited lines. But Claim 2's "plus third-party products it uses" conjunct has no quote and no citation (S036.txt:15 never appears). |
| Q4 attribution | PASS | claims are vendor-scoped; first-party labels; three vendors named; no universal rule. `「招待」` count 0/0/0/0. |
| Q5 falsifiable + rejected | PASS | FR-1..FR-4 present; five rejected over-generalizations with reasons. |
| Q6 documentation-only | PASS | grep of actionable verbs only hits the public URL in a header (L5) and the entry's own negative statement (L210). |
| Q9 capture assertions | PASS | path stem = id for all five records; all 30 S036–S039 manifest quotes occur exactly once in raw captures and appear in the entry; recheck exit 0 from both cwds with identical digest. |

## Commands, outputs, exits

```
# all 27 blockquotes vs cited capture lines (script, see below)
total_quotes=27 failures=0
# 招待 counts
S036 招待=0  S037 招待=0  S038 招待=0  S039 招待=0
# Q6 pattern scan (curl|wget|nmap|scan|probe|submi|contact|login|検証し|スキャン|送信|アクセスし|攻撃し|実行し)
hit lines: 5 (S038 public URL in header), 178/180 (rejection prose), 210 (negative statement)   exit=0
# recheck line (S036..S039 chained), bash -n
bash -n -> exit 0
lane root -> exit 0; foreign cwd / -> exit 0; digest b15f167f937a2fa0727a5060bb650f587ccc79f887609b512c0c93519c779aca (identical both)
# manifest: 5 sources; paths S036.txt..S040.txt stem = id; S036=8 S037=6 S038=7 S039=9 S040=9 quotes
# C2 counter
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md -> 10
grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md | wc -l -> 2
# capture-log sha256 matches files: S036 022ca4f4… S037 b204aa7f… S038 09e077d3… S039 657e7b4c…
# fetch time: log utc=2026-10-25T08:14:25/26Z == entry ground "fetched 2026-10-25T08:14Z"
# 更新日: S039.txt:487 = 更新日：2026年10月14日 == header
```

## Finding 1 (substantive) — Claim 6 equates un-enumerated conditions with the prohibition list

Entry `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:119-121`:

> Pepabo's page is a reporting channel plus a conditional statement about legal action plus a case-by-case
> publication decision, with no reward. The three are decided separately, **and the non-litigation
> statement is conditional on the two listed prohibitions**.

Capture S038.txt:17: `…が以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。`
— the policy names "the conditions shown below"; L18–22 between the sentence and the prohibition list carry
`脆弱性の評価について` / `報告方法` content, and the list has its own heading `禁止行為` (L23). The capture
**never enumerates** the conditions; the two prohibitions (L24–25) are a separate, distinctly headed list.

This is precisely the wave-1 reviewer limit `wave1/RevQuotesJP.md` U1:

> The reference dangles. An entry may say the policy is conditioned on compliance with conditions stated on
> the page; it may **not** enumerate or characterise those conditions.

Wave-1's U1 verdict was "yes (policy only)" for the quoted sentence — the *entry* then crossed the limit by
identifying the conditions with the prohibitions. The claim that protection is bounded by the prohibition
list is practically sensible, but as written it asserts a binding the bytes do not prove.

**Smallest correction**: split the sentence into the two supported facts — (a) the no-legal-action statement
is conditional on conditions stated on the page (not enumerated), (b) verification is separately bounded by
the two prohibited acts (S038.txt:24–25). Fix is in the entry's prose only; no quote/manifest change.

## Finding 2 (Q3 gap) — Claim 2's third-party conjunct has no quote

`vendor-disclosure-policies-as-corpus-objects.md:33`:

> Handling scope covers everything Cybozu develops, plus third-party products it uses:

Only S036.txt:14 is quoted beneath it. The "plus third-party products it uses" conjunct is load-bearing
(the second half of the scope claim, and the *disclosure*-vs-*handling* contrast at FR-1 depends on the
distinction). S036.txt:15 (`当社が利用しているサードパーティー製品`) is never quoted and never cited —
`grep -n 'S036.txt:15|サードパーティー製品' <entry>` → no match (exit 1) — and the manifest's S036 record
has no L15 quote. Both U2's row table and U5's caution treat L14/L15 as two separately supportable bullets.

**Smallest correction**: add the L15 verbatim quote with its citation (`> 当社が利用しているサードパーティー製品` / `> — 脆弱性対応 対象範囲, capture S036.txt:15`) and, to keep Q9/R12 whole, add the string to the S036 manifest record (quote id, e.g. Q9) so the recheck asserts it too.

## Finding 3 (Q1 anchor, minor) — S039 header under-covers the entry's own citations

`vendor-disclosure-policies-as-corpus-objects.md:6`:

> source: S039 — … — HIRT-PUB10008 (更新日 2026年10月14日), the 4 IRT model intro, 1.2 脆弱性情報の入手 and
> 1.3 調査ならびに対策 (capture corpus/source-snapshots/round-25/S039.txt:491-519)

The entry quotes from L497 (1.1 概要), L520 (1.3), and L557 (1.5 CVE採番). Two are outside the declared
range, and sections 1.1 and 1.5 are unnamed. Q1 asks for "an exact anchor"; the header is under-specific for
what the body relies on.

**Smallest correction**: extend the header to `S039.txt:491-557` and name `1.1 概要` and `1.5 CVE採番と公開プロセス` (or state the range as 491–520 + 557).

## Soft notes (not defects, recorded for the judge)

- Claim 1's "state-coordinated partnership" (L26–27) describes the 情報セキュリティ早期警戒パートナーシップ; the
  quoted S036 line does not say "state-coordinated". The phrase is defensible (S039.txt:571 describes it as
  `官民の連携体制`), but as written it is an interpretive gloss on a quote that does not carry it.
- Claim 3's "not to the reporter's scoring" (L60) is an interpretive contrast beyond the quoted S036.txt:21;
  the quote supports assignment to PSIRT, not the negative clause.

## Why the remaining axes hold

- **Sources**: URLs match SOURCES.md rows S036–S039; all tier A; all opened this round (Q2).
- **Dates**: `verified-at: 2026-10-25` matches the run date; "fetched 2026-10-25T08:14Z" matches
  capture-log `utc=2026-10-25T08:14:25/26Z`; S039's `更新日 2026年10月14日` matches capture L487.
- **Reject**: rejected over-generalizations 1–5 each name the capture line that defeats the reading; the
  招待=0 check is reproduced (0/0/0/0) and the S037 account-gate reading is directly quoted (L99/L101).
- **Attribution**: every claim names its vendor; Claim 7 explicitly ("Hitachi describing Hitachi"), and the
  scope/limits block limits the entry to captured pages.
- **Doc-only**: the Q6 scan's four hits are the public source URL, rejection prose about what the pages
  lack, and the entry's own negative statement; no credentials, no session, no private URL, no instruction.

Kept strictly to the asked gates: no production edits; this report is the only write.
