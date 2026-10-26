# CritC2Kill — adversarial critique of C2's kill rule and the F16 candidate (round 33)

Role: critic (attack the approach, not the owner). No delegation, no lane writes except this
receipt. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD `53bfa59`, base `690b69da`.
Model recorded: `opencode-go/deepseek-v4.1-flash` (config route table decided; no model passed).

**State labels (bound 6).** The F16 entry (`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`,
21,938 B, mtime 01:21) and the round-32 manifest (5,753 B, mtime 01:18) landed **during** this
seat. `corpus/SOURCES.md` S049/S050 rows and the `corpus/README.md` F16 row had **not** landed at
my last observation (01:26): `frontier=15`, `registry_rows=48`. Therefore C2 counters 1, 3, 4, 5
are **PRE-STATE** here and are not compared to the C2 target; the re-run after quiescence is the
L1's `frontier admitted=16 / rows=50` pass. Everything below about the entry's **content** is
read from landed bytes; counters 2, 7, 8 (entries citing S049/S050 = 1/1; harness; source-recheck)
were run on those landed bytes.

## Verdicts (one line each)

1. **Expansion credit — holds**, but only on a reading of the kill rule that its own wording
   contradicts; two overlap lines must be named and one refused-ground overlap is undeclared (§1).
2. **Q4 attribution — satisfied**, to a higher standard than the kill rule asks; one sentence at
   entry:143 crosses into a cross-market analogy and should be re-cut (§2).
3. **Live pages — zero drift.** Both pages still carry every quoted sentence; the first-pass
   "20 absent lines" is a capture *converter* artifact, not page drift; that artifact is itself a
   hole in C2's "source-recheck exit 0 ⇒ verbatim quote" inference (§3).
4. **Two sources are enough for Q2** (each claim is single-document and attributed), provided the
   round-33 fresh open is carried as its own evidence; the entry must refuse one more construction
   it currently leaves open — cross-platform price comparison (§4).
5. **A junk construction passes every C2 counter, measured** — frontier 16, 1/1 citing files,
   1/1 rows, 50 registry rows, census exit 0, harness `entries=19 pass=19`, source-recheck exit 0
   with `occurrences=1` — while its body is a restatement. Only the reviewer clause fires (§5).

## 1. Expansion credit — does F16 stand on ground the map did not hold?

### 1a. Base-ground measurement (taken before the entry landed)

```
cd …/kasegi-shokunin && for t in 众测 'zc\.cnvd\.org\.cn' 'security\.360\.cn' 360SRC 安全币 报告质量 'GB/T 43741'; do
  echo -n "[$t] "; grep -rlE "$t" corpus/knowledge/ corpus/README.md corpus/SOURCES.md SKILL.md | tr '\n' ' '; echo; done
[众测] corpus/knowledge/program-severity-ladders-and-reward-scales.md
[zc\.cnvd\.org\.cn]            (none)
[security\.360\.cn]           (none)
[360SRC]                      (none)
[安全币]                      (none)
[报告质量]                    (none)
[GB/T 43741]                  (none)
```
`grep -nE 'zc\.cnvd|360\.cn|security\.360' corpus/SOURCES.md` → no rows. The single `众测` hit is
F13's own refusal note (`program-severity-ladders-and-reward-scales.md:64`: staged CNVD/BILISRC
ladders "not adopted this round"). So the lane held **no** platform-scope or reward-rule ground
before this entry, and F13 declares the ground outside its own scope. Expansion credit is real.

### 1b. The two overlap lines that must be named (and are defensible)

- **F13's override rule** — `program-severity-ladders-and-reward-scales.md:32` quotes Bugcrowd's
  "application complexity, bounty brief restrictions or unusual impact" override. F16 `Claim 2`
  (entry:54) leads with "severity … follow the project's rules rather than a platform-wide
  scale", which is the same *class* of rule. The residual is real but not stated: Bugcrowd's
  override moves a taxonomy rating **before** submission from the brief; S049's adjustment is the
  platform and enterprise re-rating a finding **after** submission (S049.txt:208). The entry
  should say that difference rather than let a reviewer find the overlap first.
- **F14/F15** — Japanese severity vocabulary (S046/S047) and MSRC's intake routes (S048) share no
  claim with F16. No line to name.

### 1c. The refused-ground clause is what almost kills F16 — and it is mis-worded

Three refused staged entries held this ground, and the kill rule's clause ("or repeats ground …
that a refused staged entry held") read literally condemns F16:

| refused file (package `knowledge/corpus/knowledge/`) | what it held | refusal |
|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | staged S034 (`zc.cnvd.org.cn`) + S035 (`security.360.cn`) scope claims | round 29/30/31, form/registration + Q4 universalisation |
| `claim-packaging-and-report-quality.md` | staged S034/S035/S036 reporting rules | round 30/31, same class |
| `chinese-program-severity-instrument.md` | S034 CVSS 3.0 metric set **and** the multiplicative reward formula in prose | round 29/30 set, unregistered |

The round-29 refusal of the first file states the flip condition in words F16 executes —
"register S034+S035 as lane rows with captures + exactly-once quotes; add a named lane frontier
row" (`corpus/lessons/round-29.md:137` area; verifier agrees at
`round-29-verifier-spotcheck.md:69`). A kill rule that forbids what the refusal's own flip
condition orders is self-defeating: no refused ground could ever be recovered.

**Is the overlap with `chinese-program-severity-instrument.md` real?** Partly. F16 quotes the same
formula sentence (S049.txt:132) but does **not** re-claim that entry's thesis: measured,
`grep -n 'CVSS\|0\.85\|时效评价\|利用代码'` on the entry returns **one** line, the quoted
seven-aspect sentence at entry:78 — no coefficient table, no temporal metric set, no CVSS
derivation. The refused entry's headline (the platform grades on CVSS 3.0 with temporal metrics)
is absent from F16. That residual is what the reviewer must be shown, and the entry does not
declare it: "What this adds beyond F13 and F15" (entry:234) names F13 and F15 only.

Also measured: the kill rule and the claims name the refused file as
`chinese-crowdsourced-testing…`; `find /home/vgpnk/Projects/shokuknow/merge/kasegi -name
'chinese-crowdsourced*'` → no output. The real file is `cn-crowdsourced-testing-roles-and-conduct.md`
(`ScoutF16Sweep.md` §2 records the same correction). A literal filename check on the clause is
unrunnable as written.

## 2. Q4 attribution

Every platform claim is stated as its publisher's. Spot-audited: Claim 1 "the CNVD 众测 manual
states", Claim 3/5 "the 360SRC standard states", and the entry separates the 众测 platform from the
CNVD 漏洞共享平台 (Claim 1; S049.txt:214) — the identity confusion my seat exists to hunt is
already refused in the text (Rejected #2). The `source:` lines name the stating party beyond what
the kill rule asks: footer "国家计算机网络应急技术处理协调中心" as rights holder and
"北京数字观星科技有限公司" as technical supporter (S049.txt:425-426, verified at those lines),
"编写人 360 安全应急响应中心" (S050.txt:2-3).

**One crossing.** entry:143 — "…which is the same shape the CNVD manual states at S049.txt:208
from the other side of the market." "Same shape … from the other side of the market" is an
analogy that generalizes two platforms into one market pattern; it is the only place the entry
stops attributing and starts comparing. Q4 does not require deleting it, but a reviewer will
name it, and the fix is cheaper than the argument.

**Kill-rule wording defect.** The clause "does not name CNVD and 360SRC as the stating parties"
understates the party: the helpList page is the 网络安全众测平台 manual whose operator is
CNCERT/CC, published on a CNVD subdomain; "CNVD" alone can be read as the 漏洞共享平台 the same
page redirects away to. The clause should name the page + operator, since the entry already does.

## 3. Do the live pages still say the quoted sentences?

Opened 2026-10-26 with the instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`:

```
curl -sS -L -A '<UA>' https://zc.cnvd.org.cn/news/helpList      → http=200 bytes=56674
curl -sS -L -A '<UA>' https://security.360.cn/Reward/rules       → http=200 bytes=427391 (PDF, 21 pages)
```

Drift, measured by normalized whitespace-collapsed substring (NFKC + `\s+`→''), capture vs live:

| capture | lines | absent in live text | live page identity |
|---|---|---|---|
| `round-32/S049.txt` | 426 | **0** | HTML; footer `版权所有 © 2018-2026 国家计算机网络应急技术处理协调中心`, `京ICP备10012421号` |
| `round-32/S050.txt` | 630 | **0** | PDF; `pdfinfo` CreationDate/ModDate 2023-03-01, 21 pages, Title `360SRC 外部漏洞处理和评分标准 V2.0` |

Entry quotes re-checked one by one against today's live text: **15 block quotes, 15 present**
(14 exactly once; `漏洞安全币（安全币 ：RMB=1 : 5）` 7×, which the entry itself discloses at
S050.txt:129 + `L159, 189, 219, 249, 274, 304`). Cited capture line numbers re-measured: every one
correct (S049 132/208/211/212/214/359/408/410/419/425-426; S050 62/68/70/71/99/112/113/129/418/558-560/591-597/601/607/611).
The entry's own falsifiable counts all reproduce on the captures: FC-1 1/1; FC-2 `授权`=2, two other
counts 1/1; FC-3 1/1; FC-4 1 and `不予收录`=6; FC-5 `安全币` 0 (S049) vs 32 (S050), `奖金`=12;
FC-6 `免责|安全港` 0/0, `授权测试`=0 (S050), legal-action sentence=1; `附加分`=1.

**False-drift trap, recorded so nobody re-runs it as a finding.** A naive line-by-line compare
reports 20 of 426 S049 lines "absent" (e.g. `评价要素取值系数`, the CVSS coefficient rows). They
are **converter artifacts**: the capture joins table cells that the live page emits as separate
`<td>`/`<th>` elements (`grep -c '不改变（U）' live html` → 1; the header is three `<th>` cells
`评价要素`/`取值`/`系数`). After whitespace collapse the count is 0 absent.

**That artifact is a live hole in C2's inference chain.** `评价要素取值系数` is reproducible by the
capture instrument, passes `source-recheck.py` (it is a capture substring), and is *not* a sentence
on the page — `grep -c '评价要素取值系数'` on the live HTML → 0. So "source-recheck exit 0" proves
capture binding, never verbatim sentencehood. Today's entry is clean (all 15 quotes are live
prose), but the kill rule should not accept instrument exit 0 as Q3 evidence for table-derived
strings.

## 4. Is a two-source (S049/S050) entry enough for Q2 — and what must it refuse?

**Enough, on one condition.** Q2 is per-claim and needs ≥1 tier-A/B row "opened in the admitting
round". Every load-bearing claim in the entry is single-document and attributed (Claim 1 and 2 →
S049; Claims 3-6 → S050); no claim spans both documents. The condition is freshness: the captures
were committed in round 32 (commit `288ea9ac`, author time `2026-10-25T23:14:00-03:00` =
`2026-10-26T02:14Z`), so `verified-at: 2026-10-26` is satisfiable either from the capture instant
or from a round-33 re-open. The round-33 re-open exists — `wave1/ScoutLiveDrift.md` (04:16Z,
`0 differing lines`, sha256 identical on both) and my independent open above — but the entry does
not cite it; its `recheck:` note honestly says "a captured-source comparison, not a fresh network
verification" (Q7-compliant). One appended Limits line naming the 2026-10-26T04:16Z fresh fetch
would make `verified-at` unambiguous.

**What the entry must refuse (measured against its Rejected list, entry:206-233).** Held: universal
Chinese-platform rule; S050-as-asset-list; either document as authorization/safe harbor; grade-as-
payout; 安全币 formula read into CNVD. **Not held, and it should be:** cross-platform price
comparison — CNVD 众奖 settles by bank transfer with a per-withdrawal floor (`下限为每笔提现申请不低于200元`,
S049.txt:356) while 360SRC pegs 1 安全币 = 5 RMB (S050.txt:129); nothing in either document makes
the two reward instruments commensurable, and the entry's FC-5 asserts only that they are different,
not that they cannot be compared.

## 5. Which junk construction meets every C2 counter except the reviewer clause — measured

Built in `/fast/scratch/hyaku/kasegi-r33/CritC2Kill/junk-lane` from `git archive HEAD` (base
bytes `53bfa59`), with: two shape-valid registry rows citing the two URLs; a *junk entry* whose
body is the restatement (`Chinese crowdsourced-testing platforms score a finding by multiplying
factors … Each platform's ladder is its own suggested baseline`) plus a vacuous falsifiable rule;
two manifest records whose quotes are real, exactly-once capture substrings that do **not** assert
the entry's claim (`平台目前仅支持银行卡转账的方式来发放奖金` S049.txt:352;
`漏洞奖励=业务系数*基础安全币` S050.txt:112); one appended frontier row; one expected-list line.

Result — every measurable C2 counter passes:

```
frontier=16
S049files=1
S050files=1
S049rows=1
S050rows=1
registry_rows=50
S049:q1 OK occurrences=1
recheck49_exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050  exit=0
entries=19 pass=19 exit=0
file	W04	S028 duplicate url …safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url …reg/2024/2847/oj/eng across scopes
file	ok	…/junk-lane/corpus/SOURCES.md
census_exit=0
```

So the counter set discriminates **shape**, not content: novelty, Q3 quote-to-claim fit and Q4
attribution are carried entirely by the reviewer clause, which has no committed control. The C2
kill rule therefore rests on one unmeasured limb (R13/R17 by analogy: a limb with no isolating
fixture is a survivor).

## 6. Smallest safe corrections to the C2 kill rule (for the L1; I do not edit claims)

1. **Refused-ground clause.** Replace "repeats ground … that a refused staged entry held" with a
   test: *the clause fires only when the entry claims ground a refusal declared absent or
   unopenable; a refusal for delivery defects (Q1/Q2/Q3/Q4/Q7/Q10, id collision, unregistered
   source) consumes nothing — the entry passes this clause when it meets that refusal's own flip
   condition.* Name the files exactly (`cn-crowdsourced-testing-roles-and-conduct.md`,
   `chinese-crowd-testing-national-standard-2026-10-23.md`, and the three that held S034/S035:
   `program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md`,
   `chinese-program-severity-instrument.md`).
2. **Stating-party clause.** Name the page and operator (网络安全众测平台 help manual, CNCERT/CC;
   360 安全应急响应中心), not the acronym pair.
3. **Reviewer clause needs a control.** Commit §5's junk twin bytes + its all-pass output under
   `c2-controls/`, and require the reviewer verdict *on the twin* (reject) beside the verdict on the
   candidate. Optionally add one mechanical counter for the known universalisation shapes
   (`Chinese … platforms? (all|every|universally)`) — cheap, and it kills the twin's worst sentence.
4. **Quote-verbatim conjunct.** Require that any quote used as Q3 evidence appear in the
   live-page text of a round-current fetch, or be drawn from prose lines only — `source-recheck`
   exit 0 must not be cited as proof of sentencehood (§3 artifact).
5. **Owner attribution on failure.** `source-recheck` reads `corpus/source-snapshots/round-32/manifest.json`
   (ExecManifest32) and counters 3-5 read `SOURCES.md` (ExecRegistryAppend); the C2 receipt should
   name the owning seat for each failing limb so a C1-owned byte defect is not filed as a C2 kill.
6. **Counter 2 brittleness.** `grep -lE '^source: S049 '` needs a trailing space and counts files,
   not header lines; restrict it to the Q1 header block (first 8 lines) so a body mention cannot
   satisfy it and `source: S049,S050` is a named failure rather than a silent zero.

## 7. Minimal fixes handed to ExecEntryF16 (messaged by id)

1. entry:143 — cut the cross-market clause; state the mechanism difference (S049 re-rates after
   submission, S050's 初评级 clock at S050.txt:99) instead of "the same shape".
2. entry:54 — re-cut the Claim 2 headline so it does not read as F13's override restated; the
   novel claim is "no per-severity money table; payout = enterprise rating + project rules".
3. entry:234 — add one sentence distinguishing F13:32's pre-submission taxonomy override from
   S049's post-submission re-rating, and declare that the S049 formula quote was previously staged
   in the refused `chinese-program-severity-instrument.md` while the CVSS metric set is not
   re-claimed here.
4. entry:206-233 — add Rejected #7: the two reward instruments are not commensurable (S049.txt:356
   bank-transfer floor; S050.txt:129 peg).
5. entry Limits — append the round-33 fresh open (2026-10-26T04:16Z, 0 differing lines) so
   `verified-at: 2026-10-26` is evidence, not a restated capture instant; and add the
   `grep -c` count beside the one hand-measured quote that carries none (`360SRC 根据业务的重要程度…`,
   S050.txt:113, measured `1`).

None of these is a kill: C2's counters 2/7/8 pass on the landed bytes and the content defects above
are one-sentence fixes.

## 8. Tooling, scratch, cleanup

- Installs: none. `curl`, `pdftotext`, `python3` (stdlib only) were already present; `pacman`
  untouched per the host ruling.
- Scratch: `/fast/scratch/hyaku/kasegi-r33/CritC2Kill` (live fetches, junk-lane clone via
  `git archive`, junk registry/entry/manifest fixtures, `junk-twin-counters.txt`). Removed with
  `rm -rf` before yielding; every number above is reproduced in this receipt, so nothing had to be
  preserved.
- No lane git/jj mutation; no lane file written but this receipt; `/home/vgpnk/Projects/shokuknow`
  read only; no live bounty target contacted (two public documentation URLs only); no credential
  material quoted — the S049 credential-adjacent ranges (L202-205, L398-406) are named, never
  reproduced.

## 9. Uncertainties I am not allowed to resolve

- The frontier/registry counters were PRE-STATE (15/48) at my last look; the L1's post-quiescence
  run (`16 / 50 / harness 19/19`) is the authoritative reading, not this receipt.
- Whether the L1 accepts `ScoutLiveDrift.md` as the round-33 open for Q2 is a ruling, not a
  measurement; my own UA fetch agrees with it (http 200, all quotes present).

## 10. Post-state addendum (appended after the owner applied the five fixes)

§0 and §9 filed the frontier/registry counters as PRE-STATE (15/48). Appended here, leaving those
paragraphs byte-identical, per R9: the registry rows and the `README.md` F16 row landed after those paragraphs were written,
and the whole C2 counter set now passes on quiescent bytes — measured at this seat's re-run:

```
S049files=1  S050files=1  S049rows=1  S050rows=1  registry_rows=50
frontier=16
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050  exit=0
entries=19 pass=19 exit=0                                   (frontier-recheck-count.py --root .)
kasegi  W04 S028 duplicate url …safe-harbor-overview-faq
kasegi  W04 S029 duplicate url …reg/2024/2847/oj/eng
kasegi  ok  …/kasegi-shokunin/corpus/SOURCES.md             (census_exit=0)
recheck_exit=0                                              (14/14 assertions, landed bytes)
```

Entry digest after the owner's fixes: `eebd5ea572b3359f012e9c7ef9975969ffcbd3e5b06e31d40ac56a6a7d15910b`
(305 lines) — matches the digest ExecEntryF16 reported. All five §7 fixes are present on those
bytes (cross-market clause gone; Claim 2 headline re-cut; overlap paragraph at :277-281; Rejected
#7 at :236; Limits drift bullet at :293), and C2's measurable kill clause is met.

**One residual defect, introduced by fix 3.** Entry:280 prints `grep -c -E 'CVSS|0.85|时效评价|利用代码'`
on this entry → `1`. On the final bytes that command yields **3**, because the declaration
paragraph itself says "its CVSS 3.0 metric set" (:278) and the command string sits at :280 — the
count is self-referential and the printed literal is stale (R19). The substance is unaffected: all
three hits are meta-mentions, and scoping the count to the claim body reproduces the intended value
(`head -200 | grep -c …` → 1). Smallest fix: print the scoped command with its `1`, or print the
measured `3` and dispose of each hit. Reported to ExecEntryF16 by id.

## 11. Final-bytes confirmation (appended, §10 paragraph left byte-identical)

The residual in §10 is closed on the entry's final bytes — digest
`53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48` (306 lines, 24,492 B),
verified at this seat:

```
awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' <entry> | grep -c -E 'CVSS|0.85|时效评价|利用代码'  → 1
grep -c -E 'CVSS|0.85|时效评价|利用代码' <entry>                                                          → 3
python3 corpus/instruments/source-recheck.py --manifest …/round-32/manifest.json                        → exit 0
python3 corpus/instruments/frontier-recheck-count.py --root .   → PASS F16 … ids=S049,S050; entries=19 pass=19 exit=0
```

The scope is section-bounded (`## Attribution` → `## What this adds`), so the printed `1` no longer
depends on a numeric window and the command string sits outside its own scope. R19 closed; C2's
measurable clause stays met on the final bytes.

## 12. Digest supersession (appended; §10/§11 hashes superseded)

After §11 the owner applied a citation-stem correction (RevQuoteSweep: the 使用手册 question stem
was retyped `漏洞提交时` where `S049.txt:210` reads `提交漏洞时` — a copied source string, not a
manifest quote). Any gate citing this receipt should use the live hash, verified at this seat:

```
entry sha256 1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1   306 lines, 24,539 B
grep -c '提交漏洞时' round-32/S049.txt → 2      grep -c '漏洞提交时' … → 0
entry:3, entry:48 cite the stem as 提交漏洞时 with question L210 / answer L211
source-recheck --manifest round-32/manifest.json → exit 0
frontier-recheck-count.py --root . → PASS F16 … ids=S049,S050; entries=19 pass=19 exit=0
```

§10's `eebd5ea5…` and §11's `53c48b3b…` are historical readings, not the delivered bytes. Nothing
in §1-§9 changes: the five fixes, the section-scoped counter and the C2 counter set all still hold
on this digest.
