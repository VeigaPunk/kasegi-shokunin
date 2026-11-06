# Round 80 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r80. Base `58905f2bbc52db6b1634566cc1be9c92cdddebfb`, freeze `4ab545865f747fca8456370b5927fe51236fe579`, landing `0039d6708158f26655ee4fad2af4893a5f6c1cb7`, wave results / lane HEAD `7629cc563dee8ad7f48b7eaaebdb860e5ddb9252`. Report `.ufo/reports/round-80/kasegi.md` (fleet repo). Dispatch digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T16:37:34-03:00 launch kasegi round=80 pgid=628805 driver=hyaku-inline attempt=1
2026-11-06T17:04:00-03:00 complete kasegi round=80; hyaku-inline attempt=1
```

All re-measurements below ran over `git archive <rev>` extracts of base, freeze, landing and HEAD into a private scratch tree; nothing ran in the lane worktree. No lane gate was executed (§Gate standard, Closure consequence).

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-80/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> e263e108f0e04f16d75806e892a986fc64267759 2026-11-06T17:03:33-03:00` (after HEAD `7629cc56`, before the 17:04:00 completion line) | ok |
| `SHONEN` heading, one line per box | read of report § SHONEN | 4 lines: `[~]`, `[ ]`, `[~]`, `[~]` | ok |
| cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for `58905f2b…`, `4ab54586…`, `0039d670…`, `7629cc56…` | all `commit`, all ancestors | ok |
| lane pushed, clean | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain` | `branch=master local=7629cc56… remote=7629cc56… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | ok |
| lane commits by lane identity | `git log --format='%h %an %ae %s' 58905f2..master` | 3 commits (`4ab5458`, `0039d67`, `7629cc5`), all `kasegi-shokunin kasegi@shokunin.local` | ok |
| prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/kasegi-round-80.md) templates/round-prompt.md` | differs only in rendered placeholders (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`); §1–§5 headings identical; §6 hyaku addendum and §7 follow | ok |
| wave receipts | `jq` over `.ufo/waves/round-80/w1-results.json` | `seats 12`, `results 12` | ok |

Not a marker report: three lane commits, 13 non-`.ufo` lane files changed (`git diff --name-status 58905f2 7629cc5`).

## Per-claim re-check

### C1 — depth:verifiability — evidence-verified (lane-owned gate and wave counter; not executed)

| what | command | observed |
|---|---|---|
| landed bytes = frozen candidate | `git show <rev>:corpus/instruments/recheck-cwd-census.py \| sha256sum` at base/freeze/HEAD; `sha256sum .ufo/waves/round-80/c1/recheck-cwd-census.py` at freeze and HEAD | base and freeze `e666ae11…a21a`; HEAD `420151fd…5698`; frozen candidate `420151fd…5698` at freeze and HEAD (P2 holds) |
| counter and table unchanged after freeze | `sha256sum c1/mutbat.py c1/mutant-table.json` at `4ab54586` and `7629cc56` | `b47276d1…d450`, `08d7f3ce…a418` at both — match the lesson's pins |
| table composition | `jq` over `c1/mutant-table.json` | 28 rows; 27 `assertion`, 1 `exception` (`K-M3`); includes `N10 N11 N21 N25 N26 N27 N30 T1 T2` (the nine r79 routed survivors) |
| R129 classifier | `grep -n 'EXC_RE\|counts = ' c1/mutbat.py` | `42:EXC_RE = re.compile(r"^selftest case=\S+ FAIL exception=", re.M)`; `95: counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row.get("class") == "exception")` — keyed on the prefix, not a free-text substring (the r79 defect) |
| scored battery (frozen run) | `grep MUTBAT w1/ExecC1Battery.md l1/L1-landing-r80.txt` | `MUTBAT target_sha256=420151fd…5698 baseline=ok rows=28 killed=28 survived=0 dirty=0 notderived=0` (twice in ExecC1Battery, once in the L1 landing receipt, rc 0) |
| controls | `grep -h 'MUTBAT\|rc=' controls/c1-*.txt` | base `e666ae11` `baseline=bad killed=0 survived=2 dirty=1 notderived=25` rc 1; r79 `eda49d32` `killed=13 survived=6 notderived=9` rc 1; print-stub `7b0c488a` `killed=0 survived=28` rc 1; R129 selftest rc 0 |
| selftest pin | `git diff -U0 58905f2 7629cc5 -- SKILL.md corpus/instruments/README.md` | exactly `cases=6` → `cases=15` in each file (1+/1− each); L1 receipt P1 `selftest cases=15 failures=0` rc 0 |
| TMPDIR refusal | L1 receipt P4 | `rc=2`, `recheck-cwd: TMPDIR /nonexistent-kasegi-r80 is not a directory`, Traceback count 0 (base control: `FileNotFoundError`, rc 1) |
| revision measured | MUTBAT `target_sha256` | `420151fd…` = the landed bytes, measured on the landing tree `0039d670` |

Matches the report. Lane-acknowledged limit, carried: CriticClaims (a) — forgeries reach `killed=28` under this counter, so only P2's byte pin excludes them; MutClassifier `P3DEL`/`P3RAISE` land as `EXCEPTION-KILL counted=no`. Both are outside the frozen table and routed by the lane to r81; neither changes the frozen verdict. Axis: **improved** (score 4 → 4 nominal per R58, but the landed instrument measurably supersedes the base: 0 → 28/28 frozen kills, selftest 6 → 15 cases, M77-3 TMPDIR crash closed).

### C2 — coverage — re-measured

Command at each revision: `python3 -B corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-(CENSUS|PASS F56)'; ls corpus/knowledge/*.md | wc -l; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && NF!=13' corpus/SOURCES.md | wc -l`

| rev | FRONTIER-CENSUS | F56 pass | knowledge | registry | malformed rows |
|---|---|---|---|---|---|
| 58905f2b (base) | `rows=55 admitted=55 closed=55 problem-rows=0 registry=113` | — | 93 | 113 | 0 |
| 4ab54586 (freeze) | `rows=55 admitted=55 closed=55 problem-rows=0 registry=114` | — | 93 | 114 | 0 |
| 0039d670 (landing) | `rows=56 admitted=56 closed=56 problem-rows=0 registry=114` | `FRONTIER-PASS F56 ids=S114` | 94 | 114 | 0 |
| 7629cc56 (HEAD) | `rows=56 admitted=56 closed=56 problem-rows=0 registry=114` | `FRONTIER-PASS F56 ids=S114` | 94 | 114 | 0 |

Matches the report (55→56, 93→94, 113→114 across the round). Further checks:
- S114 row at freeze vs HEAD (cells 9 and 12): `queued`→`mined`, `—`→`corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md`; other cells unchanged.
- Snapshot `corpus/source-snapshots/round-80/S114.txt`: sha256 `e1ccfb9b…88d2`, 73 lines — matches manifest and row.
- Every `"quote" (S114.txt:<n>)` span in the F56 entry occurs on its cited snapshot line: `ok 6 bad 0`; the six claim-table quotes each occur once in the snapshot, word counts 11/16/14/9/12/20 (all ≤25) equal the declared counts.
- Entry opens with `source:` (S114 + URL), `verified-at: 2026-11-06`, `recheck:` — provenance trio present.
- New ground: `grep -rli ubuntu corpus/knowledge | wc -l` = 0 at base, 1 at HEAD.
- The entry cites F54's ordering sentence at `osv-post-batch-query-contract.md:21` (`grep -n guaranteed` prints 19 heading, 21 sentence) — correct.

Axis: **improved** (frontier 55→56, knowledge 93→94; score held at 8, denominator operator-owned).

### Harm check

`git diff --numstat 58905f2 7629cc5`: `SCORECARD.md 22/0`, `LOG.md 12/0`, `corpus/QUALITY.md 7/0`, `corpus/lessons/round-79.md 5/0` (appended corrections, never in place), `PROVINCE.md 2/0`, `corpus/README.md 14/0`, `corpus/SOURCES.md 2/0`, `SKILL.md 1/1` and `corpus/instruments/README.md 1/1` (the `cases=` token only). SCORECARD diff is additions only; depth:density **unchanged** (one-token SKILL edit; lane receipt mean 272.8 before/after). No owned axis harmed.

QUALITY rows R130 and R131 exist (`corpus/QUALITY.md:587-588`) and cite `corpus/lessons/round-80.md` § Mistakes M80-1 / M80-2 — grounded criteria.

## Discernment spot-check (LEARNING.md)

| # | item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|---|
| 1 | cl2 Q02 source-name indexing, "Ubuntu vulnerability advisories in OSV are indexed by source package name rather than binary package name." (S114.txt:35) | admit | live `curl https://google.github.io/osv.dev/post-v1-ubuntu-binary-to-source/` → HTTP 200, 18769 bytes (= manifest raw size); tag-stripped text contains the quote once; also on snapshot line 35 | **agree** | A contract-level statement from the endpoint's own reference page; absent from the 93 prior entries (base `grep -rli ubuntu` = 0); 16 words. |
| 2 | S114.txt:33 experimental-status paragraph | reject | snapshot line 33 ("This API endpoint is still considered experimental. …"); `sed -n 75p corpus/knowledge/osv-post-v1-query-contract.md` | **agree** | F51:75 already lists the experimental endpoints ("…and the experimental endpoints, S108.txt:5-9. They are listed, not described."); a status sentence is not a contract clause. |
| 3 | S114.txt:58 leading ordering clause ("The response results array is guaranteed to match the ordering of the input binary_names") | reject | live page (clause present once); `grep -n guaranteed corpus/knowledge/osv-post-batch-query-contract.md` → `19:` heading, `21:` "The response ordering will be guaranteed to match the input." | **agree** | Same input-ordering rule-shape is held by F54:21; pinning only the empty-object half of :58 avoids a restatement. |

SOURCES row re-open: S114 (`corpus/SOURCES.md:126`, new this round). The row carries no inline quote; its anchor names "binary-to-source page, lines 25-58" and the manifest's six pins. Quotes checked against the live page: Q01 (11 words), Q02 (16), Q03 (14), Q05 (12), Q07 (20) each occur once in the tag-stripped live text; Q04 (9 words) is present live with `<code>` spans splitting the punctuation (`Ubuntu:24.04 , Ubuntu:24.04:LTS , …`) — an extraction artefact, not an absence. All ≤25 words. The row's note that the experimental-path URL returns 404 re-checks: `curl …/osv.dev/v1experimental/ubuntu/binary-to-source/` → `404`.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, the six inherited W04 warnings (S028 S029 S072 S076 S080 S085), rc 0.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability (C1) | improved | evidence-verified: landed `420151fd…` = frozen candidate; frozen battery 28/28 kills vs base 0; selftest 6→15; TMPDIR rc 2 |
| coverage (C2) | improved | re-measured: frontier 55→56, knowledge 93→94, S114 `queued`→`mined` |
| depth:density | unchanged | one-token SKILL.md edit; lane receipt 272.8 before/after |

## Trend verdicts

- **expansion: improved** — F56 is new ground (no knowledge entry mentioned Ubuntu at base; 1 at HEAD), citing the `mined` S114 row; frontier 55→56.
- **quality: improved** — a weaker instrument is superseded by a stronger one (base killed 0/28 → 28/28 on frozen bytes, selftest 6→15 cases, TMPDIR traceback closed); no admitted entry fails re-check (`FRONTIER-CENSUS problem-rows=0`, census `kasegi ok`).
- **discernment: improved** — this spot-check agrees with the gate on the sampled admit and both sampled rejects; the r79 spot-check disagreement (false Q12 correction) became M80-1 with grounded R130, and the r79 D1 cite defect became M80-2 with R131.

## Routed defects (lane fixes next round)

1. **Stale F54 line cite in the lesson.** `corpus/lessons/round-80.md` cites `osv-post-batch-query-contract.md:19` three times (lines 88, 160, 162) for the ordering sentence, which is at `:21` (`:19` is the heading). The lesson self-flags it at line 14; append a named correction (R131 class), never in place.
2. **Reject count.** `corpus/lessons/round-80.md` § Learning says "Six admits and four rejects" while § Gate lists three reject bullets (:33, :58 ordering, skeleton+samples); state the counting rule or correct by appended note.
3. **Counter independence (carried from the lane's own routing).** CriticClaims (a): forgeries reach `killed=28`; only P2's byte pin excludes them. MutClassifier `P3DEL`/`P3RAISE` score `EXCEPTION-KILL counted=no`. ReviewC1 M1/M2 survivors. The next C1 successor should make the kill tally a limb independent of the byte pin.

SHONEN: box 2 (end-to-end domain task) is `[ ]`; boxes are not fully checkable by a non-author — no promotion signal for the operator.
