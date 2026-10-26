# CritExpansion — expansion-credit attack on F16 (round 33)

Seat: critic (leaf). Scope: does any existing lane entry — F13, F15, the refused staged package
entries, SKILL.md — already say what F16 says? Read-only on the lane; the only write is this
receipt. No network, no subagents, no background jobs, no scratch tree, no installs, no git/jj
mutation. Answering model (rule 10, read from the harness project context, not passed by me):
`opencode-go/deepseek-v4.1-flash`.

Bytes reviewed (quiescent: the entry sha printed identical twice, 6 s apart, before writing):

```
eebd5ea572b3359f012e9c7ef9975969ffcbd3e5b06e31d40ac56a6a7d15910b  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md  (305 lines)
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  corpus/source-snapshots/round-32/S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  corpus/source-snapshots/round-32/S050.txt
```

The entry landed mid-round (01:21Z) and was revised in flight: the first read was
`d9b2acf2…` (278 lines), the writer then applied CritC2Kill's fixes, and **this review was
re-run on `eebd5ea5…` (M30-3: in-flight bytes are non-comparative)**. Every line reference below
is measured on `eebd5ea5…`; the `recheck:` was re-executed on those bytes (`S049` exit 0, `S050`
exit 0). `corpus/SOURCES.md` S049/S050 rows and the README F16 row were **not yet landed** when
this receipt was written (`registry_rows=48`, `grep -c F16 corpus/README.md` → 0); nothing here
depends on them because this review measures the **entry against existing ground**, not the C2
counters.

## VERDICT: `partial`

**Overlap is real and named; residual is real and named. `restatement` does not fire on the entry
as a whole. It still fires on one self-named addition (item 1) and on the headline of item 3; the
entry has already conceded the formula overlap at `entry:271-282`.** The admission stands; the
remaining defect is the scope half of the adds-section (§6).

Three grounds must be conceded in the entry:

1. **The CNVD 众测 project-scope rule is refused ground, stated twice in the package.**
   `program-scope-rules-and-asset-boundaries.md:20-22` and
   `chinese-crowd-testing-national-standard-2026-10-23.md:30-31` both already say it. **Not yet
   conceded anywhere in the entry.**
2. **The CNVD 众测 internet-intake refusal is refused ground.**
   `chinese-criminal-thresholds-and-authorisation.md:50` holds it. **Not yet conceded.**
3. **The CNVD 众测 multiplicative score and "severity ≠ payout" argument is refused ground.**
   The staged F13 package entry (`program-severity-ladders-and-reward-scales.md:21, 29-35`) holds
   both the formula and the worked 12/10/7/4-point example; the lane's own F13 entry records that
   ground as **not adopted** (`program-severity-ladders-and-reward-scales.md:64`). **Conceded at
   `entry:276-282`** ("The S049 scoring formula quoted here was also held by the refused package
   entry `chinese-program-severity-instrument.md`"), and Claim 2's heading was re-cut to "publishes
   no per-severity money table" (`entry:54`) — the correct narrower claim.

What survives as expansion is §4: the target-list disclaimer, the CNVD payout source and
settlement, 360SRC's investee/joint-venture applicability and separate asset list, its
security-service coverage filter, its reward formula/peg/grades/clock, and its report-hygiene
forfeiture rules. That residual is substantive and is absent from the base tree and from every
refused/staged entry (§1, §4).

## §1 The sweep (base tree, so the new entry cannot supply its own hits)

### 1a. Lane at base `690b69da` — before F16 existed

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ for t in CNVD 360SRC 'zc\.cnvd\.org\.cn' 'security\.360\.cn' '众测' 'crowdsourc' 'crowd-test' \
           '客户授权' '授权测试范围' '互联网漏洞' '安全服务' '基础安全币' '业务系数'; do
    printf '### %s\n' "$t"
    git grep -n -E -- "$t" 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- \
      corpus/knowledge corpus/README.md SKILL.md PROVINCE.md | head -6
  done
### CNVD
690b69dae…:corpus/knowledge/program-severity-ladders-and-reward-scales.md:64:- The staged package entry also included CNVD 众测 and BILISRC ladders and a worked CNVD score example. They are **not adopted this round**…
### 360SRC            (none)
### zc\.cnvd\.org\.cn  (none)
### security\.360\.cn  (none)
### 众测
690b69dae…:corpus/knowledge/program-severity-ladders-and-reward-scales.md:64: (same line)
### crowdsourc        (none)
### crowd-test        (none)
### 客户授权          (none)
### 授权测试范围      (none)
### 互联网漏洞        (none)
### 安全服务          (none)
### 基础安全币        (none)
### 业务系数          (none)
```

So at base the lane held **one** line on this ground: F13's own disclaimer that the CNVD 众测
ladder and worked score example were **not adopted**. SKILL.md, PROVINCE.md and README are 0-hit.
F15 is 0-hit on every term.

### 1b. On the landed tree, every residual-term hit is the new entry itself

```
$ for t in '客户授权' '互联网漏洞' '目标列表' '安全服务' '业务系数' '基础安全币' '安全币' '子公司' '合资'; do
    echo "### $t"; grep -rlE -- "$t" corpus/knowledge corpus/README.md corpus/SOURCES.md \
      corpus/QUALITY.md SKILL.md PROVINCE.md; done
### each of the nine terms
corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

No other lane file carries any of them. This is the measurement that makes the residual credit
real and, equally, that shows the entry is the only holder of it.

### 1c. Refused / staged package — the ground the entry's headline claims also restates

Package root `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/` (read-only).

```
$ for t in '不接受互联网漏洞|互联网漏洞' '投资的公司|子公司|合资公司' '基础安全币|业务系数' \
           '未纳入安全服务|安全服务' '测试范围' '安全币' '云存储|对象存储|公开披露'; do
    printf '### %s\n' "$t"; grep -rnE -- "$t" *.md; done
### 不接受互联网漏洞|互联网漏洞
chinese-criminal-thresholds-and-authorisation.md:50: …and the exclusion of 互联网漏洞 by the 众测 platform
### 投资的公司|子公司|合资公司      (none)
### 基础安全币|业务系数            (none)
### 未纳入安全服务|安全服务        (none)
### 测试范围                       (none)
### 安全币
program-severity-ladders-and-reward-scales.md:22:| BILISRC / 360SRC 安全币 | 严重 / 高危 / 中危 / 低危 / 忽略 + 经验值 | the vendor SRC | reward is money, scaled by business tier |
### 云存储|对象存储|公开披露        (iso-29147-divergence…:42 only — public-disclosure clause, unrelated platform)
```

Refusal status (lane lessons, read-only): `program-scope-rules-and-asset-boundaries.md` refused
rounds 29–31 (`round-29.md:137,166`; `round-29-verifier-spotcheck.md:69`; `round-31.md:62`);
`claim-packaging-and-report-quality.md` refused rounds 29–31 (`round-30.md:45`;
`round-31-verifier-spotcheck.md:89`); `cn-crowdsourced-testing-roles-and-conduct.md` and
`chinese-crowd-testing-national-standard-2026-10-23.md` refused round 31 (`round-31.md:64-65`);
`chinese-criminal-thresholds-and-authorisation.md` standing refusal (`round-31.md:67`).
`chinese-program-severity-instrument.md` has **no gate record in any lane lesson** — it is staged
and never lane-resident; I do not call it refused.

The flip condition the round-29 gate wrote for the first file is, word for word, what this round
does: "register S034+S035 as lane rows with captures + exactly-once quotes; add a named lane
frontier row" (`round-29.md:137`, concurred at `round-29-verifier-spotcheck.md:69`). That makes
the reuse legitimate, but it also means the entry is a **flip of refused ground**, not ground no
refusal ever touched — the distinction the adds-section concedes for the formula (`entry:276-282`)
but not for the scope rule.

## §2 What each neighbour already says — quote, exact location, gap

| # | file / line | overlapping text (≤25 words) | what it holds | what it does not hold |
|---|---|---|---|---|
| 1 | refused `program-scope-rules-and-asset-boundaries.md:20-22` | "systems outside the test project's scope are not within the customer's authorization and are strictly not permitted" | F16 Claim 1's second rule (S049.txt:410), in English prose | the located quote, the lane row, the target-list disclaimer |
| 2 | refused `chinese-crowd-testing-national-standard-2026-10-23.md:30-31` | "the rule that out-of-project systems are outside the customer's authorization" | the same rule, plus "the seven-factor score" as already-recorded mechanics | any quote, any source row, the security-service filter |
| 3 | refused `chinese-criminal-thresholds-and-authorisation.md:50` | "the exclusion of 互联网漏洞 by the 众测 platform" | F16 Claim 1's first rule (S049.txt:214) — internet-wide findings are refused | the redirect to CNVD 漏洞共享平台, the intake wording |
| 4 | staged `program-severity-ladders-and-reward-scales.md:21,29-35` | "CNVD 众测 points \| multiplicative formula over 7 factors"; "A maximum-CVSS finding pays 4 points or 12 points depending on who was tested." | F16 Claim 2's formula (S049.txt:132) and the whole "severity ≠ payout" argument | lane rows, quotes, the "no 安全币 table" negative |
| 5 | staged `program-severity-ladders-and-reward-scales.md:22` | "reward is money, scaled by business tier" | that 360SRC/BILISRC reward is tier-scaled money | the coefficient formula, the 1:5 peg, the five grades, the clock |
| 6 | refused `claim-packaging-and-report-quality.md:16-18` | "仅从理论层面说明漏洞的存在而无利用和复现过程将不予收录" | 360SRC's proof-of-exploitation refusal (a **different** rule from F16 Claim 6) | the cloud-storage and pre-fix-disclosure forfeiture rules |
| 7 | lane F13 `program-severity-ladders-and-reward-scales.md:64` | "They are **not adopted this round**" | the lane's own record that items 4/5's ground was declined | — |
| 8 | lane F09 `statutory-authorization-and-unauthorized-access.md:46` | "the platform's text cannot supply that third party's consent" | the *principle* behind F16 addition 1 and its honest limit | any Chinese platform instance |
| 9 | F13 entry (whole) | English ladders only (S043–S045) | HackerOne/Bugcrowd suggested baselines | Chinese platform scope or reward — F13 says so itself |
| 10 | F15 entry (whole) | MSVR's three intake routes (S048) | vendor-as-finder direction | nothing on any Chinese platform |
| 11 | SKILL.md / README / PROVINCE | 0 hits for `CNVD|360SRC|众测|zc.cnvd.org.cn|security.360.cn` | the general rule "a badge does not expand scope" (F03) | all platform-specific content |

Entry line references used below: Claim 1 `:21`, Claim 2 `:54`, Claim 3 `:94`, Claim 4 `:111`,
Claim 5 `:124`, Claim 6 `:147`, adds-section `:242-282` (items at `:252`, `:258`, `:263`; the
concession paragraph at `:271-282`).

## §3 Counterexamples: two self-named "additions" are refused ground, one survives

### 3a. Addition 1 (`entry:252`) — the scope object

> "A scope object that is a customer authorization, not a taxonomy or an asset list."

The *instance* is new to the lane; the *claim* is not new to the package. Rows 1–3 of §2 say the
same thing in the refused set, and row 8 (F09) states the principle for statutory consent: a
platform's text cannot supply a third party's consent. What is actually not held anywhere is the
**target-list disclaimer** ("the submission page's target list is not the scope document",
`entry:254`; S049.txt:211-212) and the **redirect**: internet findings go to the national sharing
platform. The redirect is closely held by row 3's ground (the exclusion), so the clean residual is
the disclaimer. Addition 1 as written therefore overstates by two of its three components — and
unlike addition 3, it has **no** concession paragraph: `grep -n 'program-scope-rules\|chinese-crowd-testing-national-standard\|chinese-criminal-thresholds'` on the entry → no hits.

The counter-check that the entry does *not* restate the other refused entry:
`grep -c '众测需求方\|众测组织方\|授权测试方\|众测审计方\|不得因为漏洞信息私自联系厂商'` on the entry → `0`.
F16 does not re-claim the four-role GB/T 43741 arrangement or S081's conduct rule, so
`cn-crowdsourced-testing-roles-and-conduct.md` is **not** restated (shared text: the platform URL
only; longest common word run 6 = `https zc cnvd org cn news`).

### 3b. Addition 3 (`entry:263`) — the reward instruments

> "Two reward instruments that do not reduce to a severity ladder." … "the enterprise's rating
> plus project rules set the reward" … "安全币 never appears"

The staged F13 entry already contains the entire argument that CVSS severity does not fix payout:
the multiplicative formula row (`:21`) and the worked example in which a CVSS 10.0 RCE pays 4, 7,
10 or 12 points by enterprise size and report quality (`:29-35`). F16 re-states the formula
(S049.txt:132) and the per-project adjustment (S049.txt:208) — **and the entry now concedes
exactly that** at `entry:276-282`: "The S049 scoring formula quoted here was also held by the
refused package entry `chinese-program-severity-instrument.md`", with the CVSS 3.0 metric set
declined. The remaining defect is only the item-3 headline: "do not reduce to a severity ladder"
still claims the class, while the genuinely new facts are narrower — the manual prints **no**
per-severity money table (`安全币` count on S049 = 0; `奖金` = 12), and payout follows the
enterprise's rating plus project rules (S049.txt:419). On the 360SRC side the tier-scaled-money
ground is row 5; the new facts are the formula, the peg and the grade list (`entry:124-146`).

### 3c. Addition 2 (`entry:258`) survives as written

The security-service coverage filter is absent from the base tree and from every refused/staged
file (`未纳入安全服务|安全服务` → 0 hits), and it is not derivable from F13's asset paragraph or
F15's intake routes. This is the strongest single piece of new ground in the entry.

## §4 Residual, named precisely (falsifiable)

*What this entry adds to the lane that no admitted entry and no refused/staged entry held:*

1. **The submission page's target list is not the project scope agreement** — S049.txt:211-212
   ("并不是项目的测试范围约定"; `注：请严格按照项目测试范围进行测试。`), each exactly once.
2. **CNVD 众测 payout is not a platform-wide table** — the enterprise's rating plus project rules
   set the reward (S049.txt:419); settlement happens at project close (S049.txt:359); `安全币`
   never appears on the page (0 occurrences).
3. **360SRC's applicability names investees, subsidiaries and joint ventures, and defers the
   list** — S050.txt:70-71; the enumeration is the separate `/Product/product` page.
4. **360SRC's collection is filtered by security-service coverage** — S050.txt:591-593
   ("未纳入安全服务的资产一般情况下不收录相关漏洞"), with the major-harm exception.
5. **360SRC's reward is a coefficient formula over three business tiers, pegged 1 安全币 = 5 RMB,
   with five grades and a seven-working-day final-grading clock** — S050.txt:112, 113, 129, 418,
   99.
6. **360SRC's report-hygiene forfeiture rules** — no report on open cloud services/shared docs
   (S050.txt:595), no publication or leak before the fix (S050.txt:597-598).

Checkable in both directions: the base-tree sweep (§1a) is 0-hit on every term; the refused/staged
sweep (§1c) is 0-hit on 3–5's distinctive strings and holds only item 2's class and item 1's rule
class in other words. A package that states items 1–6 from F13+F15+the refused entries alone is
not constructible from them.

## §5 Verdict against C2's kill rule, and the axes

- Kill-rule clause **"repeats ground the coverage map already holds"**: **passes**. The coverage
  map held nothing (F13 disclaims it at `:64`); rows 9–11 of §2 show F13/F15/SKILL hold none of it.
- Kill-rule clause **"or that a refused staged entry held"**: **passes only on the narrow reading**,
  i.e. the entry is not a restatement as a whole because items 1–6 of §4 are absent from every
  refusal. Read literally ("repeats ground … that a refused staged entry held"), the clause is
  **self-defeating**: rows 1–5 are refused ground, and the round-29 flip condition orders exactly
  the recovery this round performs. I therefore do not fire it, and I record the tension for the
  L1 rather than pretend it away.
- Kill-rule clause **"reviewer must show F16 is not a restatement … with the sweep command"**:
  satisfied by §1a+§1c+§4, with the concession that addition 1 must be re-cut and the item-3 headline narrowed to the entry's own concession at `:276` (§6).
- **Q4**: satisfied. Every platform claim is headed "the CNVD 众测 manual states" / "the 360SRC
  standard states"; the two intakes are separated (S049.txt:214; Rejected #2), and the refused
  entry's universalisation ("every platform's scope list is…") is not reproduced.
- **Axes impacted**: `coverage` — expansion credit is **partial**, carried by §4 items 1–6, not by
  the adds-section's item 1 as written; no score move asserted (held at 7). `depth:verifiability`
  — untouched by this review; the entry's `recheck:` was executed and passes
  (`S049` Q1–Q8, `S050` Q1–Q6, all `occurrences=1`, both exit 0).

## §6 Smallest safe correction (owner: ExecEntryF16; the L1 routes it)

No new source, no new row, no re-quote. Three items: one is already applied by the writer, two remain open:

1. **Already applied (verified on `eebd5ea5…`).** Claim 2's heading is now the narrow claim
   (`entry:54`), and the paragraph at `entry:271-282` names F13:32's pre-submission override and
   concedes that the S049 formula was held by the refused `chinese-program-severity-instrument.md`
   while declining its CVSS 3.0 metric set. Nothing further is needed on the formula.
2. **`entry:250-257` — scope the claim and re-cut addition 1 (still open).** After "Three things
   here are not in either", add one sentence: the scope half was held by refused package entries
   (`program-scope-rules-and-asset-boundaries.md:20-22`, `chinese-crowd-testing-national-standard-2026-10-23.md:30-31`,
   and the internet-intake exclusion at `chinese-criminal-thresholds-and-authorisation.md:50`),
   refused for delivery defects whose flip conditions are the lane rows and the frontier row this
   entry supplies — so that ground is re-stated with evidence, not invented. Then drop "a scope
   object that is a customer authorization" as the headline and lead with what is not held: the
   submission page's target list is not the scope agreement (S049.txt:211-212).
3. **`entry:263` — one clause on the item-3 headline.** "Two reward instruments that do not reduce
   to a severity ladder" overstates against the conceded formula; write instead "neither rewards a
   severity label on its own" and let the following sentence point back to the concession.

Optional, not required: the F13:32 override distinction CritC2Kill §1b asked for is already in the
entry at `entry:271-274`.

I do **not** recommend: editing F13 or the README, adding a source, or withdrawing the entry. The
entry's own text concedes "Neither can be read as 'severity X pays Y'" (`entry:268-270`), which is
the right claim; only the scope-side novelty framing is still overstated.

## §7 Reproduce

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
B=690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
for t in CNVD 360SRC '众测' 'zc\.cnvd\.org\.cn' 'security\.360\.cn' '客户授权' '互联网漏洞' '安全服务'; do
  printf '### %s\n' "$t"; git grep -n -E -- "$t" "$B" -- corpus/knowledge corpus/README.md SKILL.md PROVINCE.md; done
cd /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge
grep -nE 'systems outside the test project|out-of-project systems|exclusion of 互联网漏洞' \
  program-scope-rules-and-asset-boundaries.md chinese-crowd-testing-national-standard-2026-10-23.md \
  chinese-criminal-thresholds-and-authorisation.md
grep -nE 'multiplicative formula over 7 factors|pays 4 points or 12 points|reward is money, scaled by business tier' \
  program-severity-ladders-and-reward-scales.md
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sed -n '64p' corpus/knowledge/program-severity-ladders-and-reward-scales.md
sed -n '46p' corpus/knowledge/statutory-authorization-and-unauthorized-access.md
sed -n '242,282p' corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
grep -c '众测需求方\|众测组织方\|授权测试方\|众测审计方\|不得因为漏洞信息私自联系厂商' \
  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md    # 0
grep -n 'program-scope-rules\|chinese-crowd-testing-national-standard\|chinese-criminal-thresholds' \
  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md    # no hits (undeclared scope overlap)
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
```

## §8 Peer receipts read, and where I differ

- `wave1/ScoutF16Sweep.md` — read. Its §1 sweep agrees with §1a here. **Disagreement**: its §2c
  lists the refused `program-scope-rules-and-asset-boundaries.md` correctly but then, in §3,
  calls the platforms' scope statements "not held by either refused named entry" and F16's
  addition 1 "new". Rows 1–3 of §2 falsify that: the CNVD scope rule and the internet-intake
  refusal are both in refused package entries. Its "restatement risks" list is otherwise sound.
- `wave1/ConnSibling.md` — read. Zero sibling hits on all six scoped terms; the province verdict
  (F16 inside kasegi's Core) is not in dispute here.
- `wave1/CritC2Kill.md` — read. Agrees on the three package entries holding S034/S035 ground and
  on the refused-ground clause being self-defeating if read literally. **Disagreements**: (a) it
  names only F13's override as the overlap and concludes expansion "holds" without the
  `chinese-criminal-thresholds` and `chinese-crowd-testing-national-standard` lines that make
  addition 1 refused ground; (b) it does not name the staged F13 worked 12/10/7/4 example, so its
  treatment of addition 3 is gentler than the bytes support; (c) it calls
  `chinese-program-severity-instrument.md` refused ("round 29/30 set") where I find **no gate
  record** in any lane lesson — I classify it staged-and-never-lane-resident.
- `wave1/ExecEntryF16.md` — read (landed 01:26, 16,732 B). It pins the same final digest as this
  review (`eebd5ea5…`, 305 lines, 24,318 B) and records a longer revision chain than I saw in
  flight (my two reads were `d9b2acf2…` → `eebd5ea5…`; its §6 lists `8d4b1489…` → `8d209995…` →
  `eebd5ea5…`) and the CritC2Kill corrections it applied. It does **not** claim to have addressed
  the scope-side refused ground, which is the open item in §6 here — so the two receipts agree on
  the bytes and differ only on whether that overlap needed a concession (it did not add one).

## §9 Bounds observed

- Writes: this receipt only. No lane git/jj mutation; `/home/vgpnk/Projects/shokuknow` read-only;
  no fleet-root write; no scratch tree created (nothing to clean up).
- No live target contacted; no fetch at all in this seat; the S049 credential-adjacent ranges
  (L202-205, L398-406) are named only, never reproduced (Q6).
- No tool installed; `pacman` untouched per the host ruling.
- Quotes are ≤25 words with file:line; every count above was produced by the command shown.
