# ExecRegressionBase — base regression transcript of every existing lane instrument (round 37)

Seat: `ExecRegressionBase` (executor, leaf). Judged axes: `depth:verifiability`, `coverage`.
Milestone: round-37. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only; the only lane
write is this receipt). Base commit `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze commit
`224df74db2a46d627ae1475a72ca48796bbd177c`; lane HEAD at my runs = `b362068195d5489aa94b31e6ec8f880c367e0ba0`.
Measured 2026-10-26 (UTC clock read mid-run: `2026-10-26T17:03:13Z`). Python `3.14.8`.

## 1. Method and base anchoring

All six instruments were run **from the lane root**, read-only, with stdout+stderr captured together:

```
python3 corpus/instruments/recheck-audit.py --quiet
python3 corpus/instruments/capture-binding-check.py
python3 corpus/instruments/frontier-recheck-count.py
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
python3 corpus/instruments/score-gap.py
```

Base equivalence of the measured bytes (the lane moved only in `.ufo/waves/round-37` after the base):

| anchor | value |
|---|---|
| `git diff --stat b56a4168…..HEAD -- corpus scripts .ufo/waves/round-36` | **empty** |
| `git rev-parse b56a4168…:corpus` | `b6d08dfe56690df501d0e4ece4c5a7c9ad8488a4` |
| `git rev-parse HEAD:corpus` (before *and* after the runs) | `b6d08dfe56690df501d0e4ece4c5a7c9ad8488a4` |
| `git status --porcelain corpus scripts SKILL.md SCORECARD.md` (after the runs) | empty |

So every number below is the **base** number for `corpus/`, not a reading of a partially-edited wave
tree. `git status --porcelain` (whole lane) was the same six untracked `.ufo/waves/round-37` paths
(`assimilation/`, `wave1-plan.err`, `wave1-run.err`, `wave1.ready`, `wave1.ready.partial`, `wave1/`)
before and after the runs — no instrument wrote into the lane.

Determinism: `recheck-audit.py --quiet`, `capture-binding-check.py` and `frontier-recheck-count.py` were
each run **twice**; `cmp` reports the two outputs byte-identical for all three.

Byte binding of the files the round-37 after-state is allowed to change (blob ids at `b56a4168…`, so
"the instrument changed" is distinguishable from "the corpus grew"):

| file | base blob | base sha256 |
|---|---|---|
| `corpus/instruments/recheck-audit.py` | — | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/capture-binding-check.py` | — | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| `corpus/instruments/frontier-recheck-count.py` | — | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` |
| `corpus/instruments/source-recheck.py` | — | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/instruments/score-gap.py` | — | `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf` |
| `corpus/instruments/knowledge-expected.txt` | `ca41196e283ea771d8f65560ea4176327ca48561` | `f0d4bb0dcc12c2f3492d117a651264aa1c38638e57dd365de4655d87a46e4321` (50 lines, 48 non-comment) |
| `corpus/SOURCES.md` | `77ff68482a1c64016651ff1f53a2043408540df7` | — |
| `corpus/README.md` | `18c09ce102cdb1e57be7c9adcaba1d53ac17706b` | — |
| `corpus/QUALITY.md` | `29fc6c11e24405ce6b5a0a2a5731a25cf63d09bd` | — |
| `SCORECARD.md` | `9d867fed162f6fed8e182262b0873e87fe9b1cfd` | — |
| `SKILL.md` | `cefd579b1bcaaff40050f2381490e6c539e75f7b` | — |
| `LOG.md` | `4b4f586e2d96ede72162e9141aeeb0a2b9670c81` | — |

Cross-check that the bytes are the ones `score-gap.py` binds internally: it prints
`source: corpus/instruments/recheck-audit.py sha256=5d4842da…f09`, identical to my `sha256sum`.

## 2. Transcript table

| # | instrument | exit | baseline line (verbatim, see §3 for the full output) | expected by the item | verdict |
|---|---|---|---|---|---|
| 1 | `recheck-audit.py --quiet` | **0** | `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0` / `expect=present expected=48 missing=0 unexpected=0 exit=0` | strict 48/48, expected=48, unexpected=0, exit 0 | **MATCH** |
| 2 | `capture-binding-check.py` | **0** | `records=43 bound=43 unbound=0` | 43/43/0, exit 0 | **MATCH** |
| 3 | `frontier-recheck-count.py` | **0** | `entries=22 pass=22 exit=0` | 22/22, exit 0 | **MATCH** |
| 4 | `source-recheck.py --manifest …/round-36/manifest.json --source S053` | **0** | `S053:sha256 OK` + 4 quote rows OK | exit 0 | **MATCH** |
| 5 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **0** | `kasegi W04 S028 duplicate url …` / `kasegi W04 S029 duplicate url …` / `kasegi ok …/corpus/SOURCES.md` | exit 0, W04 S028/S029 | **MATCH** |
| 6 | `score-gap.py` | **0** | `gap: 24 of 48 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` | read-only, no score move | **MATCH** |

Frozen base counters read alongside (same tree, same run window), for the C2 before-state:
`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **19**; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **53**;
`grep -rlE '^source: S054 ' corpus/knowledge | wc -l` → **0**; `ls corpus/knowledge/*.md | wc -l` → **48**;
`corpus/source-snapshots/round-37/` → absent; 12 snapshot manifests.

## 3. Verbatim outputs (stdout+stderr merged) with file digests

### 3.1 `recheck-audit.py --quiet` — exit 0 — sha256 `d030938123a2fe54db14f87be66ad2cc169b0fb56ae2fb0b84164d7037584686`

```
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
```

### 3.2 `capture-binding-check.py` — exit 0 — sha256 `14c43839451b3066edc73693c0869578ef06712822184d3ce30f5579ae134559`

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=43 with_url=43 with_fetched_utc=5 with_archival=38 snapshot_dirs=12 manifest_dirs=12 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=43 bound=43 unbound=0
```

### 3.3 `frontier-recheck-count.py` — exit 0 — sha256 `b4c4806777da1930f62a5bf25aed5b7d378ca7b42b80a8ff0de6f573d988825c`

```
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0   
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0   
entries=22 pass=22 exit=0
```

(22 `PASS` rows over 19 frontier rows: F09/F10/F11 each have two knowledge rows. This is the harness
shape the round must keep — after F20 is admitted the only change allowed is one more `PASS F20  … ids=S054`
row and `entries=23 pass=23 exit=0`.)

### 3.4 `source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` — exit 0 — sha256 `45df116405570ed3969c28da4b0d01a6d1a7845ec3175eae43a2fff92d965796`

```
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
```

### 3.5 `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` — exit 0 — sha256 `920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499`

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

(TSV, tabs preserved on replay. `validate` is read-only: `emit`/`out_sink` write to stdout unless
`--out` is passed, and none was.)

### 3.6 `score-gap.py` — exit 0 — sha256 `2c82496c9aa1c20c3fbd6ed76471f7175e7e91b72f00f50ad4ac1e531c149faa`

```
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=2ddb1bc72872a54a87f2b3655d6612c4b5bae86ea154a612aa42cfc5fcc1fd8f
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=1e2788c6a7f577f17dd5ce46ec69e6debe7b883caea374b46f240e1754d84e6e
[1] rechecks
cmd: python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
recheck: lines=48 executes=24 gated=24 broken=0 exit=0
[2] anchors
cmd: python3 corpus/instruments/anchorcheck.py SKILL.md (cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin)
anchorcheck: in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
cmd: grep -nE '^Numerator = |^- lane total \(SKILL\.md \+ corpus\): |^- SKILL\.md alone: ' corpus/instruments/citation-survival.md
census-definition: Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct citations appearing in that scope (a citation in both scopes enters both denominators).
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
cmd: grep -nE 'Threshold for 5:.*unsupported current claims' SCORECARD.md
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 48 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

`score-gap.py` also runs `anchorcheck.py` in-tree as limb [2] (`in-range=16 bad=0`) and is explicitly
not a claim; its exit 0 asserts only that it could measure.

## 4. Post-wave delta map — the only lines allowed to differ

From the frozen counting commands (`.ufo/waves/round-37/claims.json`):

| counter | base (this transcript) | round-37 planned after-state | claim |
|---|---|---|---|
| `recheck-audit --quiet` | `strict pass=48/48 … expected=48 missing=0 unexpected=0 exit=0` | `strict pass=49/49 … expected=49 missing=0 unexpected=0 exit=0` | C2 counting_commands[6] |
| `capture-binding-check` | `records=43 bound=43 unbound=0` (12 manifests, `with_fetched_utc=5`) | `records=44 bound=44 unbound=0` (13 manifests incl. round-37, `with_fetched_utc=6` — [INFERENCE] from the claim's `fetched_utc` requirement; only `records/bound/unbound` are pinned by the claim) | C2 counting_commands[5] |
| `frontier-recheck-count` | `entries=22 pass=22 exit=0` | `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054` | C2 counting_commands[3] |
| `ls corpus/knowledge/*.md \| wc -l` | `48` | `49` | C2 counting_commands[7] |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `19` | `20` | C2 counting_commands[0] |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `53` | `54` | C2 counting_commands[1] |
| `source-recheck … S054` | n/a (no round-37 manifest at base) | exit 0 | C2 counting_commands[4] |
| `source-recheck --round-36 --source S053` | exit 0, sha+Q1-Q4 OK | **unchanged, still exit 0** | no-regression |
| census `validate … kasegi` | exit 0, exactly W04 S028/S029 + ok line | **unchanged: exit 0, still W04 S028/S029 only** (claim says "census exit 0 (W04 S028/S029 only)") | no-regression |
| `score-gap.py` | exit 0, `gap: 24 of 48 …` | exit 0; the gated count follows `lines`/`gated` after the 49th entry — the gap sentence is **expected** to move and must be re-measured, not pinned | read-only |

Everything else in §3 is a **no-regression invariant**: byte-identical instrument files (§1 sha256),
the 12 pre-round-37 `MANIFEST` lines unchanged, and the same front 22 harness rows with the same ids.

## 5. Agreement with the committed before-controls (independent reproduction)

I did not read these before running; they were compared afterwards, and every overlapping value matches:

| source | value in committed control | my base reading |
|---|---|---|
| `.ufo/waves/round-37/c1-controls/before.txt` | `git status --porcelain \| wc -l` = 0 (measured at freeze, before the wave scaffolding existed) | 6 paths, **all untracked `.ufo/waves/round-37` wave scaffolding**, 0 tracked-dirty; the count rose from the control only because the wave ran after it was taken — no tracked file changed |
| same | `grep -c '<LANE_HASH>' SCORECARD.md` = 0 | not re-run (not my item) |
| `.ufo/waves/round-37/c2-controls/before.txt` | `entries=22 pass=22 exit=0` | `entries=22 pass=22 exit=0` |
| same | `records=43 bound=43 unbound=0` | `records=43 bound=43 unbound=0` |
| same | `strict pass=48/48`, `expected=48 unexpected=0 exit=0` | identical |
| same | registry 53, knowledge 48, frontier 19, S054 citing 0, round-37 snapshot absent | 53 / 48 / 19 / 0 / absent |
| `.ufo/waves/round-37/census-before.txt` | W04 S028, W04 S029, `ok`, exit 0 | the same three lines, exit 0 |

No divergence to report: the base transcript is a second, independent measurement of the same base state.

## 6. Verification performed / not performed

Performed: six read-only instrument runs from the lane root with merged stdout+stderr and exit codes
captured; three of them re-run for determinism (`cmp` byte-identical); base-tree equivalence proven by
empty `git diff` for `corpus/`+`scripts/`+`.ufo/waves/round-36` and equal `corpus` tree ids at
`b56a4168…` and `HEAD` before and after the runs; `git status --porcelain` clean for
`corpus/ scripts SKILL.md SCORECARD.md` after the runs; sha256 binding of five instrument files plus
`knowledge-expected.txt`; blob ids for the seven corpus/root files the wave may edit; frozen count
regexes re-derived (19/53/0/48); cross-check of `score-gap.py`'s internal `recheck-audit.py` digest
against `sha256sum`; post-hoc comparison against the three committed before-controls.

Not performed, deliberately: **no** build/lint/test/suite run and no `r37-closure.sh` run (the suite does
not exist at base; the parent owns the after-state gate); no write inside the lane repo other than this
receipt; no mutating git; no pacman (host paused) and no tool install (nothing was needed — python3 3.14.8,
bash and the committed scripts sufficed); no subagent and no labrat probe (no external fact required).

Evidence: scratch `/fast/scratch/hyaku/kasegi-r37/ExecRegressionBase/` held the six `.out` logs plus three
`.2.out` determinism logs; §3 reproduces every line of them with per-file sha256. The directory is
removed after this receipt was written, leaving no `kasegi-r37/ExecRegressionBase` residue for E9.

## Report

Base transcript recorded for all six existing instruments, **6/6 MATCH** the assigned baseline with exit
0 each: audit `strict pass=48/48 expected=48 unexpected=0` (48 lines, 24 gated, 24 executes),
capture-binding `records=43 bound=43 unbound=0` over 12 manifests, harness `entries=22 pass=22`, S053
source-recheck `sha256 OK` + `Q1-Q4 OK`, census `exit 0` with exactly `W04 S028`/`W04 S029`, and
`score-gap` read-only with `gap: 24 of 48 rechecks still gated`. The measured bytes are the base bytes
(`git diff b56a4168…..HEAD -- corpus scripts` empty; `corpus` tree `b6d08dfe…` at both refs, unchanged
after the runs), the three counters are deterministic across reruns, and the numbers match the committed
`c1-controls`/`c2-controls`/`census-before` controls independently. Allowed after-state deltas and their
frozen targets are tabulated (§4) so the parent can diff one screen: audit 49/49, binding 44/44,
harness 23/23, knowledge 49, frontier 20, registry 54, round-37 manifest present — everything else must
stay byte-identical. No lane file was written except this receipt; no tooling installed; scratch removed.
