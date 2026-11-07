# Round 87 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Closure of lane-round kasegi r87. Report `.ufo/reports/round-87/kasegi.md` (fleet repo); dispatched
prompt `.ufo/prompts/kasegi-round-87.md`. Lane base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`,
freeze `afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69`, tip `4d007eb1cbde0c3c4cc9d16464e316f0159bfbc5`.
Driver digest (copied from the mutable `.ufo/watchdog.log`):

    2026-11-06T22:51:24-03:00 launch kasegi round=87 pgid=676283 driver=hyaku-inline attempt=1
    2026-11-07T00:22:05-03:00 complete kasegi round=87; hyaku-inline attempt=1

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-87/kasegi.md` (fleet) | `kasegi-shokunin kasegi@shokunin.local 11c5927e8c2411e8707bfa8d8499c38c18cbe7b8 2026-11-07 00:21:43 -0300` | pass (filed after lane tip 00:20:39, before `complete` 00:22:05) |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` report; `git show 4d007eb1:SHONEN.md \| grep -cE '^- \['` | 1 heading; 4 report lines for 4 boxes, all `[~]` | pass |
| Cited hashes are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `cd1f568a`, `afb13a88`, `d87b1b55`, `132e16c5`, `d7888107`, `4d007eb1`, `252df0c9`, `a48fe8b9`, `e73c1f94`, `b079a106` | all `anc` | pass |
| Pushed, nothing left over | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=4d007eb1… ahead=0 behind=0 tracked=0 untracked=0`; `0`; `4d007eb1…` | pass |
| Prompt carries template contract | `diff <(grep -E '^## [1-5]' templates/round-prompt.md) <(grep -E '^## [1-5]' .ufo/prompts/kasegi-round-87.md)` | identical (§1, §2, §2b, §3, §4, §5) plus hyaku addendum §6, §7 | pass |
| Prompt committed by lane identity | `git log -- .ufo/prompts/kasegi-round-87.md` | `0c3ba472…` 2026-11-06 22:51:20 (before launch line) | pass |

No conformance defect at step 1.

## 2. Claims — re-check

### C1 — depth:verifiability (knowledge tranche 2, 83 keys, meter 596/1720 → 678/1719)

Frozen kill rule (`claims.json` at `4d007eb1`): any of P1–P3 false at the landing → NOT VERIFIED.

- **P3 re-measured:** `git diff --name-only afb13a88 d87b1b55` prints 8 paths: the 5 knowledge files
  plus `.ufo/waves/round-87/w1-dispatch.json`, `w1-spec.json`, `w1/swarm-registry.json`. P3 is
  **false**, as the lane reported. The committed R139 check agrees:
  `LANDING-SCOPE from=afb13a88 to=d87b1b55 changed=8 outside=3 verdict=FAIL exit=1`
  (`.ufo/waves/round-87/l1/r139-check-r87.txt`).
- **Repoint re-measured (plain git + regex over committed bytes, my own script):** map
  `.ufo/waves/round-87/c1/repair-map.json` sha256 `7db928c7…eaa` (= frozen), 83 keys
  (S102 ×70, S069 ×10, S029, S040, S100 ×1). At `d87b1b55`: 83/83 target paths exist in the tree,
  83/83 basenames unique under `corpus/source-snapshots/`, 83/83 anchors within file length;
  full-path occurrences of the 83 targets in `corpus/knowledge/*.md` 2 (base) → 100 (landing);
  bare-key occurrences 107 → 9, and the 9 residues are 8 regex artefacts (anchored `S040.txt:58`,
  `:185-193` are not the bare key `S040.txt`) plus 1 unbackticked prose mention
  `the API description at S102.txt:13` in `openssf-scorecard-api-contract.md`, which the meter does
  not classify as a citation (the two backticked mentions of the same key were repointed).
- **Meter value evidence-verified, not re-executed:** `.ufo/waves/round-87/l1/c1-landing-r87.txt`
  records `KNOWLEDGE-METER base=596/1720 after=678/1719 … keys=83`, M1–M7 pass,
  `KNOWLEDGE-METER-RESULT pass rc=0`, `P2 pins=13 bad=0`. P2 spot re-measured: sha256 of
  `knowledge-meter.py` (`949f0625…`), `resolve.py` (`db5e0767…`) at the landing match the frozen pins.
- **Ruling:** the repoint is real and correct, but the frozen predicate P3 fails, so C1 is
  **NOT VERIFIED**. Axis `depth:verifiability` graded `unchanged` (score 4 held, as declared; the
  claim does not verify).

### C2 — coverage (capability `capture-secret-scan`)

- **P2 re-measured:** at `132e16c5`, `corpus/instruments/capture-secret-scan.py` sha256 `b2bf9d65…`
  and `capture-secret-allow.tsv` `f9fbd7e7…` are byte-equal to the frozen candidates under
  `.ufo/waves/round-87/c2/candidate/`; `claim-package-check.py` `8b6f8493…` and the counter
  `capability-check.py` `4fba0cbe…` match their pins. Neither instrument file exists at base
  (`git ls-tree -r cd1f568a corpus/instruments | grep -c capture-secret` → 0).
- **K2 oracle re-measured:** `git grep -lE 'X-Amz-Security-Token=[A-Za-z0-9%/+=_-]{40,}' 252df0c9`
  → exactly 2 files (`.ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json`,
  `corpus/source-snapshots/round-86/S122.txt`), matching `K2 … sts_files=2 oracle=2`. Same grep at
  `132e16c5` and `4d007eb1` → 0 files (consistent with K3 `hits=0`).
- **Key-id literals at tip:** `git grep -ohE '\b(AKIA|ASIA)[A-Z0-9]{16}\b' 4d007eb1 | sort | uniq -c`
  → only `AKIAIOSFODNN7EXAMPLE` ×37 (AWS's documented example, S124:409) and planted fixtures
  (`AKIAZZZ…`, `ASIAPLANTEDFIXTURE01`, `ASIAQGYBPQ6EXAMPLE12`, `ASIAZZZZYYYY…`). No real key id.
- **K5 re-measured:** `git diff cd1f568a 4d007eb1 -- SCORECARD.md` adds the `capture-secret-scan`
  capabilities row (round 87).
- **K1/K3/K4 evidence-verified, not executed** (lane-owned gate, §Gate standard Closure
  consequence): `.ufo/waves/round-87/l1/c2-landing-r87.txt` records `K1 pass selftest_rc=0`,
  `K3 pass rc=0 summary=scanned=1319,hits=0,files=0,allowed=18,unused_allow=0`,
  `K4 pass rc=1 missing=none extra=none sts_allow_rc=2`, `CAPABILITY-CHECK-RESULT pass rc=0`,
  measured against revision `132e16c588a2424c06b5ca15ea01fce1ee9a396d`.
- **Ruling:** C2 **VERIFIED**. Axis `coverage` graded `improved` (new capability row with an
  exercised round demonstration). The scanner's known gaps (ReviewC2Scanner: `corpus/practice/*/evidence/`
  out of scope, HAR/percent-encoding gaps, `--files` untested by the counter; 5 surviving
  scanner mutants) are qualifiers routed below, not a re-score.

### Harm check

- `git diff --stat cd1f568a 4d007eb1 -- SKILL.md PROVINCE.md SHONEN.md corpus/README.md` → empty;
  `corpus/QUALITY.md` +2 lines (R138, R139 appended, nothing rewritten). `depth:density`
  `unchanged` (SKILL.md untouched; lane value 273.2 → 273.2).
- `git diff --name-only --diff-filter=D cd1f568a 4d007eb1 | wc -l` → 0 deletions.
- Non-`.ufo` paths touched: LOG, SCORECARD, QUALITY, SOURCES, 2 instruments, 6 knowledge files,
  lesson, 3 round-87 snapshot files — all inside the lane's own repo. The P3 breach swept 3
  wave-scaffold files into a landing commit; that is a scope/process defect, not harm to an owned axis.
  No axis harmed.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | unchanged | C1 NOT VERIFIED on frozen P3; score 4 held as declared |
| coverage | improved | C2 VERIFIED; capability `capture-secret-scan` enters |
| depth:density | unchanged | SKILL.md untouched |

## 4. Discernment spot-check (`corpus/lessons/round-87.md` § Gate)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S124 — AWS IAM, Create a signed AWS API request (SigV4) | admit (mined) | `curl -sSL https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html` → 200, 57,201 B; tag-stripped text contains the 20-word quote; capture `corpus/source-snapshots/round-87/S124.txt:83-85` holds it, `:409` holds `AKIAIOSFODNN7EXAMPLE` | agree | First-party AWS page stating exactly the rule the scanner enforces (session token in `X-Amz-Security-Token`), tier A scoped to AWS only |
| S125 — AWS IAM, IAM identifiers | admit (mined) | `curl -sSL https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html` → 200, 47,977 B; live text reads "ASIA Temporary (AWS STS) access key IDs use this prefix, but are unique only in combination with the secret access key and the session token"; capture `S125.txt:330-332` matches | agree | Authoritative prefix table backing the AKIA/ASIA classifier; row scope correctly excludes secret-key formats |
| Amazon S3 API, "Authenticating Requests: Using Query Parameters (SigV4)" | reject | `curl -sSI` → `302` to `https://docs.aws.amazon.com/AmazonS3/latest/API/`; `curl -sSL` → 200, 2,343 B, `http-equiv="refresh" content="0;URL=Welcome.html"`, zero `X-Amz-Security-Token` mentions | agree | No capturable text, so no located quote is possible; S124 carries the same rule. Note: the lesson says HTTP 200 for the URL itself; today it answers 302 then serves the 2,343-byte shell — same outcome, minor wording drift |

`corpus/SOURCES.md` row re-open: S124 (line 136) names snapshot lines 83-85 and 409 and capture
`corpus/source-snapshots/round-87/S124.txt`; `sed -n '83,85p'` prints the quoted sentence; the quote
is 20 words (≤25). Row count `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`:
123 at `cd1f568a` → 125 at `4d007eb1` (matches report).

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → 6 inherited
W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085), `kasegi ok …/corpus/SOURCES.md`, rc 0.

## 5. Trend verdicts

- **expansion: improved.** Two tier-A AWS sources mined (SOURCES 123 → 125), one admitted knowledge
  entry citing them, and a new instrument class (capture credential screening) with a SCORECARD row.
- **quality: unprovable-but-better.** Gains: the r86 STS-leak class is now detected by a committed,
  mutation-attacked check (K2 reproduces the 2-file oracle), 83 repointed citations resolve
  (re-measured), QUALITY R138/R139 added with R139 shown able to fail. Against: C1's landing mixed
  scope, and the scanner has named scope/encoding gaps. Non-author reviewer: this closure judges the
  net change better on the re-measurements above.
- **discernment: improved.** C1 reported NOT VERIFIED on its own P3 instead of reframed; a forgery
  control exposed a pipe deadlock before the freeze; my admit ×2 / reject ×1 sample all agree.

## 6. Routed defects (lane fixes next round)

1. **P3 scope breach (M87-2):** wire `.ufo/waves/round-87/l1/landing-scope-check.py` (R139) into the
   landing procedure so a landing commit is refused when `outside>0`, and record its pass line in the
   landing receipt.
2. **Scanner scope/detection gaps (ReviewC2Scanner):** add `corpus/practice/*/evidence/` to scope,
   cover percent-encoded/HAR/non-text captures, and add a counter limb exercising `--files`; kill the
   5 surviving scanner mutants (MutC2Scanner) and the 7 surviving counter mutants (MutC2Counter).
3. **Intake gate:** call the scanner from `capture-source.py` before a snapshot is written
   (`considerthese/2026-10-24.md:49-52`; CriticClaims F6).
4. **Manifest anchor erratum D-1:** `S125:Q01-prefix-intro` declared at line 303, sentence on 304;
   correct via an appended record and add a `source-recheck.py` test proving the anchor tolerance.
5. **Lesson wording:** the rejected S3 URL now answers 302 before the 2,343-byte shell; record the
   redirect in the next lesson's rejection row (outcome unchanged).
6. **Unbackticked residue:** `openssf-scorecard-api-contract.md` still carries one prose
   `S102.txt:13`; repoint it or record why the meter excludes prose mentions.
7. **Open L0:** expired HackerOne STS token in history `a48fe8b9`..`e73c1f94` (2 paths) stays
   operator-owned.

## 7. Operator notes

- All four SHONEN boxes are reported `[~]` with pointers (round-47 spot-check, the curl-ibb practice
  report, PROVINCE.md); a non-author can check them against those artifacts — promotion review is
  operator-owned.
- Verdict for the closure entry: `admitted=false`, `rejected-honest-stop` (C1 fails its frozen P3,
  reported honestly; no axis harmed).
