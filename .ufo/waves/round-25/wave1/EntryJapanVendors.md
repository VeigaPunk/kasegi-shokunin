# EntryJapanVendors — round-25 wave-1 receipt (C2)

Seat: `L1Kasegi25.EntryJapanVendors` (scribe). Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base revision `b49948f` (read-only `git rev-parse --short HEAD`). No VCS write, no background job of my
own, no subagent, no tool install (nothing installed or upgraded this seat).

## Behaviour

Wrote one new corpus entry re-grounded from this round's four Japanese vendor-policy captures
(S036 Cybozu policy, S037 Cybozu bounty FAQ, S038 GMO Pepabo, S039 Hitachi HIRT-PUB10008), plus the
machine-readable quote list that the L1 turns into `corpus/source-snapshots/round-25/manifest.json`.
The staged package
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-vendor-disclosure-policies-2026-10-23.md`
was read for shape only; no text was copied and none of its ids (staged S055/S056/S057/S060) appear
in the entry — every claim is re-grounded on the four round-25 captures.

Entry shape: H1, four `source:` lines (one per lane row id, each with URL, exact section headings and
capture path:line range), `verified-at: 2026-10-25`, one `recheck:` line, `ground: F10`. Then seven
claims, each with verbatim quotes at section + capture line; four falsifiable rules (FR-1..FR-4); five
rejected over-generalizations with reasons; a scope/limits section stating the capture-only limit and
the Q6 documentation-only posture.

Final state: **211 lines / 13961 B**; quote list **30 quotes over 4 records** (175 lines / 8546 B).
Two external edits landed inside my files afterwards and were verified byte-for-byte: the L1
re-serialized the JSON to 1-space indent (05:49) and, in the entry, widened the S038 Q1 blockquote
from the conditional fragment to the whole sentence plus an annotation "(quoted whole: the fragment
omits the subject, 当社システムへの侵入または侵入の試みが)" — a fair call, since the fragment had no
subject. I re-verified afterwards: 30/30 quotes exactly-once in their captures, all present in the
entry, JSON/manifest in agreement.

## Touched surfaces (my write scope only)

| path | state |
|---|---|
| `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` | new, untracked — 211 lines; the L1 widened its S038 Q1 blockquote at 05:49 (annotation in the entry), I re-verified |
| `.ufo/waves/round-25/wave1/quotes-vendor-jp.json` | new, untracked — 30 quotes, 4 records |
| `.ufo/waves/round-25/wave1/EntryJapanVendors.md` | this report |

No other lane file was created or modified by this seat. `git status --porcelain` also shows
`M corpus/knowledge/*.md` (29 files, the `FixRecheckLines` seat) and
`?? corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (the `EntryCiscoCrosswalk`
seat) — not mine.

## L1 corrections (IRC, applied before finishing)

| # | correction | action | evidence |
|---|---|---|---|
| 1 | Drop "invitation-only"; the capture supports an お申込み-gated reporting site (S037 L99-101) | Rewrote Claim 5: "account-gated (S037:99) and account issuance runs through an application form (S037:101)", plus a sentence stating no capture supports an invitation regime; added S037 Q6 as a quote and added rejected over-generalization #5 | `grep -c '招待'` = 0,0,0,0 over S036–S039; `grep -nF '報告用サイトアカウントお申し込みフォームからお申込みください。'` → L101 |
| 2 | `ground:` must be F10, not F09 | Already F10 (`ground: F10 — vendor-side disclosure policies as corpus objects; admits the four round-25 captures S036–S039`) | `grep -n '^ground:'` → line 9 |
| 3 | Rejected over-generalization with reason; name what a programme has that these policies lack | Rejection #1 rewritten to name "a reward ladder and a submission form", Pepabo's no-reward line, and where Cybozu's reward terms actually live | `grep -c '招待\|invitation'` on the entry = 0; rejection text at lines 176-182 |
| 4 | Lane ids only (S036–S039); staged ids never in header `source:` lines | Entry contains no S05x/S060 string at all | `grep -nE 'S05[5-7]\|S060'` → no match (exit 1) |
| 5 | `recheck:` → round-25 manifest, all four `--source` ids, quotes byte-identical and exactly-once | Line carries four chained invocations; 30/30 quotes exactly-once; rehearsal exits 0 ×4 | gates (b) and (c) below |

Note on correction 1's provenance: L1's message cited the 報奨金 line as S038.txt L21; the committed
capture has it at **L20** (`grep -nF` → 20; `sed -n '18,21p'` shows it as the third of those lines).
The entry, the JSON and this report use L20. The Cisco seat independently confirmed L20; there is no
open disagreement.

## Gates (acceptance a–e)

### a) file exists, header order, ≥2 new-row `source:` lines

```
head -8 <entry> | grep -nE '^#|^source:|^verified-at:|^recheck:|^ground:'
  1:# Japanese vendor disclosure pages carry separable objects, not one programme
  3:source: S036 — …   4:source: S037 — …   5:source: S038 — …   6:source: S039 — …
  7:verified-at: 2026-10-25
  8:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …
grep -c '^source: S03[6-9]' <entry>   -> 4
```

Ticket deviation, stated plainly: the item asks that "`head -3` shows H1 + `source:`/`verified-at:`/
`recheck:` in that order", but the same item requires one `source:` line per row id (four rows) and
acceptance (a) requires `grep -c '^source: S03[6-9]' >= 2`. With four `source:` lines, `head -3` is
H1 + two `source:` lines; the required order holds inside `head -8`. I did not collapse four rows onto
one line to make `head -3` literal.

### b) every JSON quote occurs exactly once (grep -c per quote, 1 expected)

Measured per quote: `grep -cF <quote> corpus/source-snapshots/round-25/<src>.txt` (fixed-string,
because quotes contain `(`, `)`, `.`, `※`), plus exact-substring count, `normalize()`-aware count
(whitespace collapse + `<u>` strip), in-entry count and the line hits. **quotes=30 failures=0.**

| src | id | chars | entry | cap | norm | grep | location |
|---|---|---|---|---|---|---|---|
| S036 | Q1 | 52 | 1 | 1 | 1 | 1 | 脆弱性対応フロー 1. 情報収集; :19 |
| S036 | Q2 | 20 | 1 | 1 | 1 | 1 | 脆弱性対応 対象範囲; :14 |
| S036 | Q3 | 25 | 1 | 1 | 1 | 1 | 脆弱性情報の公開 対象範囲; :28 |
| S036 | Q4 | 42 | 1 | 1 | 1 | 1 | 脆弱性情報の公開 対象範囲; :30 |
| S036 | Q5 | 36 | 1 | 1 | 1 | 1 | 脆弱性対応フロー 2. 影響の確認; :22 |
| S036 | Q6 | 36 | 1 | 1 | 1 | 1 | 脆弱性対応フロー 2. 影響の確認; :21 |
| S036 | Q7 | 45 | 1 | 1 | 1 | 1 | 公開フロー 2. JVNでの公開; :44 |
| S036 | Q8 | 18 | 1 | 1 | 1 | 1 | 1. 情報収集 (substring of Q1); :19 |
| S037 | Q1 | 27 | 1 | 1 | 1 | 1 | FAQ Q「Webサイトの脆弱性…」; :109 |
| S037 | Q2 | 18 | 1 | 1 | 1 | 1 | FAQ Q「報告したいのですが…」; :99 |
| S037 | Q3 | 25 | 1 | 1 | 1 | 1 | FAQ Q「受け取り方法」; :111 |
| S037 | Q4 | 40 | 1 | 1 | 1 | 1 | FAQ Q「いつ支払われますか」; :115 |
| S037 | Q5 | 24 | 1 | 1 | 1 | 1 | FAQ Q「報告用サイトで検証…」; :123 |
| S037 | Q6 | 31 | 1 | 1 | 1 | 1 | FAQ Q「アカウントが欲しいです」; :101 |
| S038 | Q1 | 72 | 1 | 1 | 1 | 1 | 脆弱性報告制度 opening (whole sentence; L1 widened); :17 |
| S038 | Q2 | 23 | 1 | 1 | 1 | 1 | 脆弱性の評価について; :19 |
| S038 | Q3 | 18 | 1 | 1 | 1 | 1 | 脆弱性の評価について; :20 |
| S038 | Q4 | 20 | 1 | 1 | 1 | 1 | 禁止行為 1; :24 |
| S038 | Q5 | 36 | 1 | 1 | 1 | 1 | 禁止行為 2; :25 |
| S038 | Q6 | 28 | 1 | 1 | 1 | 1 | opening paragraph (substring of Q1); :17 |
| S038 | Q7 | 18 | 1 | 1 | 1 | 1 | 禁止行為 1 (substring of Q4); :24 |
| S039 | Q1 | 42 | 1 | 1 | 1 | 1 | intro 4つのIRT; :491 |
| S039 | Q2 | 41 | 1 | 1 | 1 | 1 | 1.2 入手, 製品開発工程; :506 |
| S039 | Q3 | 16 | 1 | 1 | 1 | 1 | 1.2 入手, same paragraph; :506 |
| S039 | Q4 | 43 | 1 | 1 | 1 | 1 | 1.2 入手, パートナーシップからの通知; :510 |
| S039 | Q5 | 60 | 1 | 1 | 1 | 1 | 1.3 調査ならびに対策; :519 |
| S039 | Q6 | 25 | 1 | 1 | 1 | 1 | 1.3 調査ならびに対策; :519 |
| S039 | Q7 | 50 | 1 | 1 | 1 | 1 | 1.1 概要, ステップ１; :497 |
| S039 | Q8 | 36 | 1 | 1 | 1 | 1 | 1.3 調査ならびに対策, CERT/CC; :520 |
| S039 | Q9 | 35 | 1 | 1 | 1 | 1 | 1.5 CVE採番と公開プロセス; :557 |

Every quote is single-line in its capture, so the `grep -c` line count equals the substring count;
no quote needed an `anchor`. Two pairs share a line (S039 Q2/Q3 on 506, S039 Q5/Q6 on 519) but each
string is unique. Max length 60 chars (S039 Q5, a full Japanese sentence — ~15 文節, inside Q3's
≤25-word bound). `entry=1` for S036 Q8 / S038 Q6 / S038 Q7 means the string occurs once inside a
longer blockquote, which their JSON `location` states.

### c) one cwd-prefixed recheck line

```
grep -c '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ' <entry>   -> 1
```

The line (528 chars) chains one `source-recheck.py` invocation per id against
`corpus/source-snapshots/round-25/manifest.json` — see finding F-1 on repeated `--source`. Form and
verdict limbs, measured against the **second** landed manifest (11451 B, sha256 `4d632090…`, built
05:51 after the alias dedupe; sources S036–S040):

```
bash -n -c "<line>"        -> exit 0
lane root run              -> exit 0, sha256 b15f167f937a2fa0727a5060bb650f587ccc79f887609b512c0c93519c779aca
run from foreign cwd `/`   -> exit 0, sha256 b15f167f937a2fa0727a5060bb650f587ccc79f887609b512c0c93519c779aca
output                     -> 4x "<id>:sha256 OK" + 30x "<id>:Qn OK occurrences=1" (34 OK lines)
```

Identical exit status (0) and identical combined stdout+stderr digest from both cwds (C1 limb b).
History, measured at each state: before the manifest existed the line exited 2 from both cwds with
digest `ed7d0ed1…` (`manifest UNAVAILABLE reason=missing`, i.e. fails closed); against the first
manifest (12119 B, `f50f9b59…`, with the three S039 aliases) it exited 0 with digest `ace345fe…` —
the digest changed only because the printed assertion set did. `recheck-audit.py` reports this entry
as `frozen=111 strict=1111111 lane=0 foreign=0 passing PASS`.

### d) quote JSON parses

```
python3 -c 'import json;json.load(open(".ufo/waves/round-25/wave1/quotes-vendor-jp.json"))'   # exit 0
```

Shape exactly `{"entry": …, "records": [{"source", "quotes": [{"id", "quote", "location"}]}]}`;
4 records, 30 quotes, ids unique per record (asserted in the verification script); `entry` equals the
entry path verbatim.

### e) Q6 self-check — no line instructs testing, scanning or contacting

```
grep -nEi 'curl|wget|nmap|scan|probe|submi|contact|login|log in|検証し|スキャン|送信|アクセスし|攻撃し|実行し' <entry>
```

Four hits, all benign and read in full: `:5` the S038 public policy URL in a `source:` header;
`:178` and `:180` my own rejection text ("a submission form" as the thing these pages lack);
`:210` the entry's negative statement "It instructs no probing, scanning, login or submission
against any target". Pepabo's two prohibition items are quoted as that vendor's policy text. No
credential material, session, or private URL; the only URLs are the four public policy pages.

## Coordination with EntryCiscoCrosswalk (one manifest, no duplicate source)

That seat's crosswalk cites S036/S038/S039 alongside S040, so a manifest that listed S036 twice — or
listed it without both entries' strings — would break both rechecks. Resolution: **I own the
S036–S039 records and carry the union; the Cisco seat keeps S040 only.** Its eight strings are now in
my records (S036 Q8, S038 Q6/Q7, S039 Q5/Q7/Q8/Q9), byte-identical and exactly-once. Two of mine
changed shape to meet theirs: S039 Q5 is now their full sentence (my shorter fragment was removed),
and three of theirs are recorded as substrings of my longer quotes with `location` naming the
crosswalk entry. My entry gained three real citations (S039 Q7/Q8/Q9: the ISO/IEC-mapped step, the
CERT/CC–JPCERT/CC coordination bodies, and CVE-ID assignment since 2022-06). The Cisco seat
confirmed the union and added a mapping line from its row labels to these manifest ids.

The landed manifest carries my 30 quotes byte-identically: first build 05:41 (12119 B, `f50f9b59…`,
with three S039 aliases), rebuilt 05:51 after the dedupe (11451 B, `4d632090…`; `S036` 8, `S037` 6,
`S038` 7 — Q1 now the whole sentence, `S039` 9 of my 9, `S040` 9). A record-by-record comparison
against `quotes-vendor-jp.json` shows no missing and no altered string. The dropped aliases came
from `.ufo/waves/round-25/wave1/quotes-crosswalk-s039.json` (865 B, 05:41, `entry` = the crosswalk)
— an L1-authored file, not the crosswalk seat's JSON, which holds S040 only; see F-7.

## Instrument rehearsal (evidence the recheck passes once the manifest exists)

No round-25 manifest exists yet, so I rehearsed the exact build from `quotes-vendor-jp.json` in a
throwaway `mktemp -d /tmp/r25jp2.XXXXXX` (captures copied in, `manifest.json` with their real sha256),
then removed it:

```
python3 corpus/instruments/source-recheck.py --manifest "$T/manifest.json" --source S0NN   # for S036..S039
-> "<id>:sha256 OK" + "<id>:Qn OK occurrences=1" for all 30 quotes; S036 exit=0, S037 exit=0, S038 exit=0, S039 exit=0
control (S036 Q1 replaced by a fabricated sentence) -> "S036:Q1 MISMATCH reason=quote-not-found", exit=1
```

sha256 of the captures matches the ticket: S036 `022ca4f4…`, S037 `b204aa7f…`, S038 `09e077d3…`,
S039 `657e7b4c…` (`sha256sum corpus/source-snapshots/round-25/S03{6,7,8,9}.txt`).

## Findings for the L1

1. **F-1 — repeated `--source` silently checks only the last id.** The ticket's suggested form
   (`--source S036 --source S037 --source S038 --source S039` in one invocation) is a single-value
   argparse option, so only S039 is verified. Measured on committed bytes:
   `source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S001 --source S002`
   prints S002 lines only, exit 0. My line chains four invocations instead; the Cisco seat's line
   does the same. If the single-invocation form is preferred, `source-recheck.py` needs
   `action="append"` first.
2. **F-2 — C1's `lines=` denominator moved 35 → 37.** Before the two new entries,
   `recheck-audit.py` printed `lines=35`. With this entry and the crosswalk entry it now prints
   `lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`
   (`strict pass=37/37 cdroot_fail=0 instrument_fail=0 artifact_fail=0 own_fail=0`). C1's frozen
   target is written `lines=35 pass=35 exit=0`; the receipt must state which denominator it reports
   (35 at freeze, 37 at measurement) or the claim reads as unmet when it is exceeded.
   Intermediate state worth recording: while the manifest was absent the same counter printed
   `lines=36 pass=35 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=1 exit=1`, and my entry was
   the only failure (`parse,cwd,paths=110`) — the manifest is what flips that limb.
3. **F-3 — manifest location constraint (satisfied).** source-recheck rejects an absolute `path`
   and any source path outside the manifest's own directory (`reason=invalid-path` /
   `reason=outside-manifest-directory`), and Q9 requires `path` stems equal to ids. The landed
   `corpus/source-snapshots/round-25/manifest.json` (rebuilt 05:51, sha256 `4d632090…`) meets both:
   sources S036–S040, `path` values `S036.txt`…`S040.txt`, all 30 of my quotes byte-identical to my
   JSON (record-by-record). My line exits 0 from lane root and from `/`.
4. **F-4 — `head -3` in the ticket is unsatisfiable with per-row `source:` lines** (gate a).
5. **F-5 — C2's census limb is not mine.** `corpus/SOURCES.md` still has no S036–S039 rows
   (`grep -n 'S03[5-9]\|S040' corpus/SOURCES.md` returns only the pre-existing S035 line) and the
   frontier count is the `RowsScratch` seat's surface. This entry supplies the ids they must cite; it
   does not register the rows.
6. **F-6 — one string, two entries.** S039 Q5 is the full 基本方針 sentence because the crosswalk
   entry quotes it; my earlier shorter fragment was removed rather than kept alongside, so the
   manifest carries one assertion where two would have overlapped.
7. **F-7 — three S039 strings were asserted twice in the first manifest; resolved in the rebuild.**
   The 05:41 manifest (`f50f9b59…`) listed my `S039 Q7/Q8/Q9` and, under `hitachi-29147-2014`,
   `hitachi-coordination`, `hitachi-cna`, byte-identical text (step/ISO-IEC L497, CERT/CC L520, CVE
   L557). Provenance, measured: those ids lived in
   `.ufo/waves/round-25/wave1/quotes-crosswalk-s039.json` (865 B, 05:41, `entry` = the crosswalk), not
   in the crosswalk seat's `quotes-vendor-cisco.json`, which holds `['S040']` with 9 quotes — the
   Cisco seat confirmed this in reply. The L1's rebuild at 05:51 (`4d632090…`) already dropped them:
   `S039` now shows 9 quotes, all `occurrences=1`. Recorded here because the crosswalk's mapping line
   names my ids — the removal is clean, no entry loses a binding.
8. **F-8 — `recheck-audit.py` changed under the round.** My first run printed the frozen 8-column
   form (`lines=36 pass=35 … paths_fail=1 exit=1`); a later run prints extra `frozen=`/`strict=`
   columns and `total=`, `strict pass=…`, `cdroot_fail=`, `instrument_fail=`, `artifact_fail=`,
   `own_fail=`. Current digest `8ab4dff70b578268bb2ff625dff99168d17e24629856180c30f8b9f5204f1475`.
   C1's receipt must name the instrument digest it measured with (QUALITY R11: a counter's instrument
   is part of the claim), otherwise before/after numbers come from two different detectors.

## Out of scope (deliberately not done)

- No edit to `corpus/SOURCES.md`, `corpus/README.md`, `SCORECARD.md`, lessons/logs, other knowledge
  entries, instruments, or the round-25 manifest.
- No network fetch: all quotes come from the committed captures; the entry says so and claims no live
  verification.
- No probing, scanning, contacting or submitting against any target; no write outside my two owned
  paths (rehearsals used `mktemp -d` scratch dirs, removed before this report).
- S040/Cisco content is not cited in my entry — only the crosswalk seat's record carries it.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/wave1/quotes-vendor-jp.json`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/wave1/EntryJapanVendors.md`
