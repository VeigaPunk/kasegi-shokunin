# Round 79 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r79. Base `d16d2124fd5262f5a8088aa598f1e628f897d3ab`, freeze `9d0b1eb0709e47c3c6decc09138b5012a8968924`, landing `cdade13cc65c84073922bd01c2fc1ff17b4c4b29`. Report `.ufo/reports/round-79/kasegi.md` (fleet repo). Dispatch digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T15:39:22-03:00 launch kasegi round=79 pgid=1083054 driver=hyaku-inline attempt=1
2026-11-06T16:06:46-03:00 complete kasegi round=79; hyaku-inline attempt=1
```

All re-measurements below ran over `git archive <rev>` extracts of the three revisions into a private scratch tree; nothing ran in the lane worktree.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-79/kasegi.md` | `kasegi-shokunin cfe0e4cc5408cd494c1ac4c6f3ee82afe8c5c5b6 2026-11-06 16:06:18 -0300` (after landing commit 16:05:29) | ok |
| `SHONEN` heading, one line per box | read of report § SHONEN | 4 lines: `[~]`, `[ ]`, `[~]`, `[~]` | ok |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `cdade13c…`, `9d0b1eb0…`, `d16d2124…` | all `commit`, all ancestors | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain` | `branch=master local=cdade13c… remote=cdade13c… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `cdade13c…` | ok |
| prompt carries template contract | `diff <(head -140 .ufo/prompts/kasegi-round-79.md) templates/round-prompt.md` | differs only in rendered placeholders (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §1–§5 headings identical; §6 hyaku addendum follows | ok |
| wave receipts | `.ufo/waves/round-79/w1-results.json` | `seats 13`, `results 13` | ok |

Not a marker report: two lane commits, 11 non-`.ufo` files changed (`git diff --stat d16d2124 cdade13c -- . ':!.ufo'`).

Conformance defects (status-neutral):
- D1. Citation off by one: the report (line 25), `corpus/lessons/round-79.md:53` and `corpus/QUALITY.md` R129 cite the classifier as `.ufo/waves/round-79/c1/mutbat.py:41`; the committed bytes put `EXC_RE` at line 40 (line 41 is blank).
- D2. `corpus/lessons/round-79.md:37` (appended correction) carries a false measurement — see spot-check item 3.

## Per-claim re-check

### C1 — depth:verifiability — evidence-verified (lane-owned counter; not executed per §Gate standard, Closure consequence)

| what | command | observed |
|---|---|---|
| frozen bytes | `sha256sum c1/recheck-cwd-census.py c1/mutbat.py c1/mutant-table.json` at `cdade13c` | `eda49d32…091f2f`, `735d2336…3ea9`, `0cb50dc8…31e2` — match the lesson's pins |
| scored battery | `grep MUTBAT w1/ExecC1Battery.md l1/L1-battery-r79.txt` | three identical lines `baseline=ok rows=19 killed=18 survived=0 dirty=1 notderived=0` against target `killed=19`, rc 0 |
| the short row | `grep -n FAIL w1/ExecC1Battery-mutants/K-T1.out` | `selftest case=tmpdir-refusal FAIL ret=-99 stdout="exception=FileNotFoundError(2, …)"`; counting rule `mutbat.py:93` `counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row.get("class") == "exception")`; row K-T1 `class: assertion` → `counted=no` |
| controls | `grep -h MUTBAT controls/*` | base `e666ae11` `killed=0 notderived=18`; forgery `dd5b192e` `survived=8`; r78 `f6849971` `killed=6` |
| not landed | `sha256sum corpus/instruments/recheck-cwd-census.py` at d16d2124, 9d0b1eb0, cdade13c | `e666ae11…a21a` at all three |
| frozen-run revision | MUTBAT `target_sha256` | `eda49d32…` = the frozen candidate, measured at freeze `9d0b1eb0` |

The lane's NOT VERIFIED is correct: the target count is not met under the frozen kill rule and no amendment followed scoring. Axis: **unchanged** (score 4 → 4, instrument byte-identical).

### C2 — coverage — re-measured

Command at each revision: `python3 -B corpus/instruments/frontier-recheck-count.py | grep FRONTIER-CENSUS; ls corpus/knowledge/*.md | wc -l; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`

| rev | FRONTIER-CENSUS | knowledge | registry rows |
|---|---|---|---|
| d16d2124 (base) | `rows=54 admitted=54 closed=54 problem-rows=0 registry=112` | 92 | 112 |
| 9d0b1eb0 (freeze) | `rows=54 admitted=54 closed=54 problem-rows=0 registry=113` | 92 | 113 |
| cdade13c (landing) | `rows=55 admitted=55 closed=55 problem-rows=0 registry=113` | 93 | 113 |

Matches the report (54→55, 92→93, 113→113; 112→113 across the whole round). Further checks:
- `git diff 9d0b1eb0 cdade13c -- corpus/SOURCES.md`: S113 `queued`→`mined`, used-by `—`→ the F55 entry; malformed rows (`NF!=13` census) 0.
- Snapshot `corpus/source-snapshots/round-79/S113.txt`: sha256 `f4bce053…8ebf`, 127 lines — matches the manifest pin.
- Every quoted span in the F55 entry that cites `S113.txt:<n>` (10 spans, regex scan) occurs on its cited line: `ok 10 bad 0`.
- Entry opens with `source:` (S113 + URL), `verified-at: 2026-11-06`, `recheck:` — provenance trio present.
- `grep -c F55 PROVINCE.md corpus/README.md` → 1, 4.
- R128 and R129 cite `corpus/lessons/round-79.md` § Mistakes M79-1 / M79-2 (grounded criteria).

Axis: **improved** (measurable: frontier 54→55, knowledge 92→93; score held at 8 pending the operator denominator).

### Axis harm check

`git diff d16d2124 cdade13c -- SCORECARD.md` appends only `## Round 79`; no axis score lowered; depth:density 9→9 (no `SKILL.md` diff). No owned axis harmed.

| axis | verdict |
|---|---|
| depth:verifiability | unchanged |
| coverage | improved |
| depth:density | unchanged |

Round admission: **not admitted** — C1 did not verify (honest stop: reported NOT VERIFIED, candidate not landed).

## Discernment spot-check

Sources re-opened live: `curl -sSL https://google.github.io/osv.dev/post-v1-determineversion/` → `200 30242` bytes, final URL unchanged (tag-stripped, whitespace-normalized text used for containment).

| # | item · decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| 1 | Q06 ranked versions · admit | live page + `S113.txt:55` | agree | "The API will return a number of possible versions for your package, ranked by how well the version matched your local copy." occurs once live (22 words) and on S113.txt:55; no admitted entry holds the determineversion response contract (literal sweep 0/8 recorded by the lane; F51/F54 scope query endpoints only). |
| 2 | S113.txt:64 case sensitivity · reject (restates F51:31) | live page + `S113.txt:64`; `corpus/knowledge/osv-post-v1-query-contract.md:31` | agree | Live page has "Case Sensitivity: API requests are case-sensitive." once; F51:31 already quotes the identical sentence from S108.txt:53. Restatement of held ground. |
| 3 | appended correction to r78 Q12 reject reason (`corpus/lessons/round-79.md:37`) | `grep -n -i 'threading\|vary' corpus/knowledge/osv-post-v1-query-contract.md` at `cdade13c` and `d16d2124` | **disagree** | The grep matches line 47: "The page size can vary slightly because of threading and may change in the future." (S108.txt:136). The sentence has been in F51 since round 73 (`git log -S'vary slightly because of threading'` → `6582d14`). So the r78 reject reason ("restates ground F51 already holds at :47") was right, the r78 closure's disagreement (its spot-check item 4, built on a "no matches" grep) was itself a false measurement, and the r79 correction propagated it. Fault originates in the r78 closure; the lane accepted the routed item without re-running the grep. |

SOURCES row re-open: S113 (new this round, `corpus/SOURCES.md:125`). Row anchor "lines 25-85", 8 pins; quotes checked: Q01 "Given the source code hashes of C/C++ libraries, this endpoint attempts to find the closest upstream library and version." (19 words, ≤25, once live, S113.txt:25); Q08 "the MD5 hash bytes encoded in base64." (7 words, once live, S113.txt:62). Tier A `docs` for the project's own endpoint reference — appropriate.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, six inherited W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085), rc 0.

Summary: admits agree, rejects agree; one disagreement on the round's discernment-specific move (item 3).

## Trend verdicts

- **expansion: improved** — one admitted entry (F55) on ground the coverage map did not hold, `source:` citing `mined` S113; frontier 54→55 re-measured above.
- **quality: unchanged** — no entry superseded or re-verified; the C1 instrument did not land (sha256 unchanged).
- **discernment: unchanged** — the r79 gate's sampled admit and reject agree, but the round's one discernment move (the appended Q12 correction) rests on a false grep (item 3), so no improvement is credited; not `harmed`, because the error was induced by the r78 closure's routed item and is newly found here, not left unlearned. The lane's self-assessed `unprovable-but-better` is not endorsed.

## Routed defects (lane fixes next round)

1. **Retract the Q12 correction.** Append a correction to `corpus/lessons/round-79.md:37` (never in place): `grep -n -i 'threading\|vary'` over F51 matches line 47 (S108.txt:136); the r78 reject reason stands. The r78 verifier spot-check item 4 and its routed item 1 are withdrawn by this closure. Optionally note that S112.txt:170 ("These numbers can vary…") qualifies Q10/Q11 for querybatch — a successor-entry refinement, not a defect.
2. **D1 line cite.** Correct `mutbat.py:41` → `:40` by appended correction in the lesson and a superseding QUALITY row or note for R129's evidence cell.
3. **C1 successor** (carried): R129-keyed classifier, MutC1Hunt real-gap survivors (N10, N11, N21, N25, N26, N27, N30) and ReviewEquiv half-B survivors in the frozen table, P7 as a code-literal check. M77-3 (TMPDIR crash) stays open on the lane tree.
4. **Before acting on a routed reason, re-run its command.** A routed defect from a closure is evidence to re-measure, not a verdict to transcribe.

SHONEN: box 2 (end-to-end domain task) is `[ ]`; boxes are not fully checkable by a non-author — no promotion signal for the operator.
