author: hyaku closure (non-author integrator, @m_opus)
round: kasegi 33
lane HEAD before: 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
lane HEAD after: 7963976e60b2564860553c6ab4838128d5ca06ea
date: 2026-10-26

# Round 33 — non-author verifier spot-check

Dispatch digest copied from mutable `.ufo/watchdog.log` (lines 1468/1471 at closure time):

```
2026-10-26T01:10:54-03:00 launch kasegi round=33 pgid=99020 driver=hyaku-inline attempt=1
2026-10-26T02:04:22-03:00 complete kasegi round=33; hyaku-inline attempt=1
```

Scope: closure of one lane-round. This file is the only path the closure writes in the lane.
Two read-only seats dispatched by the closure (not by the lane) re-checked C1 (critic) and the
F16 entry (reviewer); their findings are folded in below and named as such. No lane instrument
(`corpus/instruments/*.py`) was executed by this closure (PROTOCOL §Gate standard, Closure
consequence): those verdicts are **evidence-verified** from committed receipts; every count in
§2 marked *re-measured* was produced by plain `git show`/`grep`/`awk`/`jq`/Python over committed
bytes at `7963976e`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-33/kasegi.md` (fleet) | `kasegi-shokunin 521b11c68480c9f62780b1d1d3806592cea1c34a`, committer time `2026-10-26T02:03:51-03:00` (after lane tip `7963976e` at 02:03:32, before the 02:04:22 completion line) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN; `grep -n '^\s*- \[' SHONEN.md` | 4 report lines, 4 boxes (`SHONEN.md:5,15,24,36`), all `[~]`; `grep -c '\[x\]' SHONEN.md` → 0 | pass |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> master` | `690b69da`, `6e55c8d`, `a6a5023`, `53bfa59`, `9f98488`, `5b7a039`, `7963976e` all resolve, all `anc=0` | pass |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=7963976e… remote=7963976e… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `7963976e60b2564860553c6ab4838128d5ca06ea` | pass |
| Prompt carries the template contract | every non-blank line of `kimi-shokunin/templates/round-prompt.md` (116) checked against `.ufo/prompts/kasegi-round-33.md`; placeholder prefixes checked; unrendered `{UPPER}` tokens | 0 missing literal lines, 0 missing placeholder prefixes, 0 unrendered tokens; §6 hyaku addendum + §7 scratch directive present; no L2 route map quoted (route table deferred to host) | pass |
| Wave settled | `wave1-spec.json` names vs `wave1/*.md` receipts; `jq '.results|length' wave1-results.json` | 64 spec names, 64 receipts, 0 missing; 64 results | pass |

Status: **ok** (real committed round work; not a marker).

## 2. Claims

### C1 — depth:verifiability (measured; lowest non-retired axis, score 4 held)

Re-measured (plain Python over `git show <rev>:` bytes; per-record: own-id row in `corpus/SOURCES.md`
unique, record `url` a substring of that row, `fetched_utc` for round ≥ 32, `archival: true` or
`fetched_utc` below):

```
690b69da rows=48 dirs=9 missing=['corpus/source-snapshots/round-32'] records=38 url=0 fetched=0 archival=0 bound=0
7963976e rows=50 dirs=9 missing=[] records=40 url=40 fetched=2 archival=38 bound=40 multi_row_url_records=2
```

Matches the reported before (`TOTAL records=38 with_url=0 with_fetched_utc=0`, round-32 manifest
absent) and after (`records=40 bound=40 unbound=0`; `AUDIT … with_fetched_utc=2 with_archival=38
… missing_manifest=0 multi_row_url=2`). `multi_row_url=2` = S029 (shares URL with S024) and S006
(shares with S028): `git show 7963976e:corpus/SOURCES.md | grep -cF <url>` → 2 each (closure critic seat).

Evidence-verified (not executed): instrument `git show 7963976e:corpus/instruments/capture-binding-check.py | sha256sum`
→ `b4182665ba5cf544…b6d0b7f9`, identical at `9f98488`; CASES list length 11; `--selftest`
`cases=11 failures=0 exit 0` at that digest (`wave1/RevC1Instrument.md:81-86`, `wave1/ExecCaptureBinding.md`);
determinism two runs byte-identical stdout `1861fec8…` (`wave1/ExecDeterminism.md` §2); base bytes
fail closed `records=38 bound=0 unbound=38`, `bind_base_exit=1`, `FAIL rule=missing-manifest dir=round-32`
(`wave1/ExecRegressionC1.md:124-132`); fake checker `records=38 bound=38 unbound=0 fake_exit=0`
rejected by the base-bytes clause (`c1-controls/fake-checker-receipt.txt`); capability row
`capture-binding-check` present (`git show 7963976e:SCORECARD.md | grep -n capture-binding-check` → 1071, 1078, 1084).
`git diff --stat 9f98488 7963976e` touches no instrument, manifest, or `SOURCES.md` (receipts,
`LOG.md`, `SCORECARD.md`, `SHONEN.md`, lesson only), so the measured revision equals the tip for every C1 input.

Rule-B erratum 1 (`53bfa59`, committer 01:18:36): ruled **acceptable**. The literal frozen wording
("`url` matches exactly one registry-row URL"; kill-rule parenthetical "zero or two+") was
unsatisfiable at freeze — two record URLs each sit in two R8-immutable rows — so it reads
`bound=38` under any instrument. The erratum was committed before any scoring seat's receipt
(earliest C1 verdict receipts `MutCtrFetchMissing` 01:21:04, `MutCtrUnbound` 01:21:09; only
`ScoutManifestAudit` 01:18:08, the hazard report the erratum answers, is earlier — critic seat,
committer times + receipt mtimes, since author stamps are jj-rewritten and do not order commits),
and its relaxation is disclosed on every surface that reads it (SCORECARD round-33 section,
lesson open item 8, `multi_row_url=2` printed). It is a supersession of an unreachable clause,
not a rescue of a failing measurement; the freeze itself is a lane defect (R2 below).

Mutant obligation (`mutants_of_the_counter`): **3 of 4 under the frozen kill-rule text**, not
"all killed" as report lines 41/49 say. accept-url-not-in-registry and skip-fetched_utc are killed
by the selftest clause; accept-record-without-url survives the plain run (`MutCtrUnbound.md:232`
headlines **SURVIVOR**) and is killed only by the selftest clause; skip-selftest prints
`selftest cases=0 failures=0` exit 0 (`MutCtrSelftestSkip.md:63-64`), which the frozen clause
("`--selftest` prints any failure or exits non-zero") does not catch (`RevClaimsFreeze.md:66-73`
F-5 "NOT caught"); `MutCtrSelftestSkip.md:84` kills it only under the dispatcher's sharpened
clause ("failures=0 lines printed from real cases"), which is in `wave1-dispatch.json`, not
`claims.json`. Ruling: the claim's predicate sentence and its measured after-value verify — the
genuine selftest's 11 case-backed lines are in committed receipts and its CASES count is 11 in
the committed bytes, so the forged-summary mutant does not describe the landed instrument. The
unmet attack obligation is a counter-strength defect, routed (R4), status- and admission-neutral
(round-31 precedent: unmet counter-mutant clause disclosed, admitted).

**C1 verdict: verifies → depth:verifiability `improved`** (score held 4; the measured surface
moved absent/0-of-38 → 40/40 with manifest provenance).

### C2 — coverage (measured, sourced; score 7 held)

Re-measured:

```
== 690b69da  frontier_admitted=15  rows=48 S049=0 S050=0  entries_citing S049=0 S050=0  knowledge_md=44
== 7963976e  frontier_admitted=16  rows=50 S049=1 S050=1  entries_citing S049=1 S050=1  knowledge_md=45
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
  kasegi W04 S028 duplicate url docs.hackerone.com/…   kasegi W04 S029 duplicate url eur-lex.europa.eu/…
  kasegi ok …/corpus/SOURCES.md   census_exit=0
contract census at tip: malformed=0  tier A=47 B=1 C=2  dups=∅  enum/tier-inflation=∅  missing used-by=∅
git diff 690b69da 7963976e -- corpus/SOURCES.md: additions only (rows S049, S050; 1 Search-log bullet; 3 R8 lines)
sha256sum round-32/S049.txt S050.txt → 962a451a…9cb8, 2f9c6406…8888 = manifest pins
```

Evidence-verified (not executed): harness `entries=19 pass=19 exit=0` with
`PASS F16 knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050`
(`wave1/ExecHarnessC2.md`); `source-recheck` S049 Q1–Q8 / S050 Q1–Q6 `occurrences=1`, `sha256 OK`,
exit 0. Closure reviewer seat independently byte-checked all 14 manifest quotes and 16 further
attributed strings at their cited lines (30/30 found; one declared PDF-wrap string matches only
whitespace-free, as the entry states) and judged the entry **ADMIT**, Q1–Q10 all pass on the landed
bytes `1f7ac0a2…` (Q4 per-platform attribution held; Q6 credential block located, not reproduced;
Q10 `bash -n` on the recheck line OK). New ground: `git grep -iE 'CNVD|360SRC|众测|zc\.cnvd|security\.360' 690b69da -- corpus/knowledge corpus/README.md`
→ 1 hit, F13's own "not adopted" refusal note; 0 hits of the F16 probe strings in the four refused staged entries.

**C2 verdict: verifies → coverage `improved`** (frontier 15 → 16 on new ground; score held 7).

### Owned axis not claimed — depth:density

`git diff 690b69da 7963976e -- SCORECARD.md` is append-only (+111 / 0); `git diff --numstat` →
`SKILL.md 19 0`, `PROVINCE.md 2 0`, `QUALITY.md 55 0`, `corpus/README.md 26 0`, all manifests
additions only. Reported density 191.5 → 201.7 and anchorcheck failure classes unchanged
(evidence-verified, `wave1/ExecNoHarmFinal.md` §3–§4). **`unchanged`, no harm.**

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | C1 re-measured + evidence-verified |
| coverage | improved | C2 re-measured + evidence-verified + closure reviewer ADMIT |
| depth:density | unchanged | append-only diffs; no score move claimed |

## 3. Discernment spot-check (LEARNING.md §Discernment is checked from outside)

Sample from `corpus/lessons/round-33.md` `## Gate`: 2 admits, 2 rejects, 1 new registry row.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S049 / F16 — CNVD 众测 helpList | admit, tier A, mined | `curl -A 'Mozilla/5.0' https://zc.cnvd.org.cn/news/helpList` → HTTP 200, 56674 B (2026-10-26 ≈05:20Z); `grep -c` on the live body: 「众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。」 → 1, 「测试项目范围以外的系统不在客户的授权范围内」 → 1; capture `S049.txt:214` / `:410` hold the same strings | agree | Platform-owned help page stating its own scope rule; quotes exactly-once live and in the capture at the cited lines; tier A scoped to CNVD's own statements is correct. |
| S050 / F16 — 360SRC 外部漏洞处理和评分标准 V2.0 | admit, tier A, mined | `curl https://security.360.cn/Reward/rules` → HTTP 200, 427391 B, `application/pdf`, 21 pp; `pdftotext -layout` + whitespace-free match: 「未纳入安全服务的资产一般情况下不收录相关漏洞」 → 1, 「本标准适用于360集团发布的产品和业务」 → 1; capture `S050.txt:591`, `:70` | agree | Publisher's own versioned standard; both quotes present live and in the capture. |
| `program-severity-ladders-and-reward-scales.md` (staged) | REFUSED / do-not-copy | `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md`: `sha256 35de5f8b…`, 50 lines vs lane file `6c05c98f…`, 67 lines; staged `source:` lines cite S032/S033/S034/S036, while lane rows S032/S033/S036 name NIST SP 800-115 / e-Gov 不正アクセス禁止法 / Cybozu policy; `grep -c bilibili corpus/SOURCES.md` → 0 | agree | Same-name overwrite hazard with colliding staged ids naming different documents; BILISRC has no lane row. |
| `chinese-program-severity-instrument.md` (staged) | REFUSED as an entry | staged file `sha256 442e0f2b…`; `grep -c newsType_6` → 1 in staged, 0 in `S049.txt` (`newsType_21` → 1); `grep -c sse.com.cn corpus/SOURCES.md` → 0 | agree | Its anchor is absent from the capture and its second source is unregistered; reusing only its S049-verified facts with line locators is the right disposition. |
| New `corpus/SOURCES.md` row S050 (`:56`) — ≤25-word quote | Gate quote 「未纳入安全服务的资产一般情况下不收录相关漏洞」 at `S050.txt:591` | capture line 591 and live PDF (above) | agree | Present at the cited line, 22 characters (one clause, well under the bar); the lesson's printed "23 characters" is a miscount (R7). |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0,
W04 S028/S029 only (same pair as `census-before.txt`), no E finding.

## 4. Trend verdicts

- **expansion: `improved`** — one admitted knowledge entry (F16) on ground the coverage map did not
  hold, each `source:` on a `mined` tier-A row (S049/S050); capability `capture-binding-check`
  enters the SCORECARD table; frontier 15 → 16.
- **quality: `improved`** — all 40 capture-manifest records now bind to their registry row and carry
  provenance (0/38 → 40/40); the round-32 captures gained their manifest (D5 closed); live re-opens
  of S049/S050 still carry every gate quote; no admitted entry failed a re-check (harness 19/19,
  recheck-audit 45/45, evidence-verified).
- **discernment: `improved`** — the outside spot-check agrees with the gate on 2/2 admits and 2/2
  rejects; the new criteria R20/R21 each cite a lesson (M33-1; round-31 open item 4). Against
  (routed, not harming the trend): a frozen clause unsatisfiable at freeze, R20 restating the
  superseded global reading, and the report's "all mutants killed" overstatement.

## 5. Routed defects — the lane fixes these next round (append-only corrections)

- **R1** `SCORECARD.md:988` and `:1087` still carry `<LANE_HASH>` ("the L1 replaces this marker");
  the final lane commit is `7963976e60b2564860553c6ab4838128d5ca06ea`. Append a correction naming it.
- **R2** Frozen C1 predicate/kill-rule text ("exactly one registry-row URL", "zero or two+")
  literally reads `bound=38`; erratum 1 supersedes it. Append erratum 2 restating the parenthetical
  per-id, and add a pre-freeze step that evaluates each literal predicate against base bytes for
  satisfiability.
- **R3** `corpus/QUALITY.md:169` (R20, new this round) says a record's `url` must match "exactly one
  `corpus/SOURCES.md` registry-row URL" — the global reading erratum 1 rejected and the landed
  bytes violate (S029, S006). Amend by appended note (Evidence standard: corrections sweep every mention).
- **R4** C1 counter mutants 3/4 under the frozen kill rule: skip-selftest survives (`RevClaimsFreeze.md`
  F-5), accept-record-without-url survives the plain run. Report lines 41/49 ("all killed") overstate.
  Tighten the kill rule to require `cases>=11` with one `selftest case=` verdict line per case; correct the report claim in the next report.
- **R5** Selftest case name `url-matching-two-rows` now builds a dup-id fixture; rename to match content.
- **R6** `corpus/source-snapshots/round-26/S040-live.txt` has no manifest record and the round-26
  manifest `purpose` text is now false; rule A is dir-level only (`CritC1Kill.md:113`). Land the
  per-file binding (CritC1Kill D1/rule D) or record the orphan.
- **R7** Citation/count slips: fleet report line 61 cites `S050.txt:69` for the applicability
  sentence (heading at L69, sentence at L70); `corpus/lessons/round-33.md:31-32` print "19 characters"
  (actual 31) and "23 characters" (actual 22) with no producing command.
- **R8** Round-32 manifest `fetched_utc` holds `2026-10-25T23:14:00-03:00` — a local-offset capture-commit
  time in a `_utc` field, not a fetch instant (disclosed in SCORECARD). Normalize or rename the field.
- **R9** Open instrument gaps carried from the receipts: C1 blind spots H4–H8 (`CritC1Kill.md`),
  C2 junk construction passing every counter but the reviewer clause (`CritC2Kill.md` §5) with no
  committed junk-twin control under `c2-controls/`, harness rule A one-directional (`MutEntryF16.md`).

## 6. Operator notes

SHONEN: all four boxes `[~]`; boxes 1, 3 and 4 cite resolvable committed evidence a non-author
could check; box 2 has no non-author replay. This closure verified none of them as boxes and writes
no `[x]`; promotion is operator-owned. The kasegi round-32 L0 question (re-dispatch vs L1-only
landing) remains open.
