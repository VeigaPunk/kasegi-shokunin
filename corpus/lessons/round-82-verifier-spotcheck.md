# Round 82 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_zfl)

Scope: lane-round kasegi r82. Base `1a50638edabb9bd1a4a4784774fc984cb5f2360f`, freeze `b9589300810a477f4d6794bfabc24b22fb50b846`, landing / lane HEAD `4576a88e85d0ee67197cf36f9f2b533040b840dd`. Report `.ufo/reports/round-82/kasegi.md` (fleet repo, commit `0132796c5e226d692a7d07bcf6b8a73bc815316b`). Dispatched prompt `.ufo/prompts/kasegi-round-82.md` (fleet commit `78a71038`).

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```
2026-11-06T17:51:17-03:00 launch kasegi round=82 pgid=340246 driver=hyaku-inline attempt=1
2026-11-06T18:38:44-03:00 complete kasegi round=82; hyaku-inline attempt=1
```

Every measurement below is a read over committed bytes (`git show`, `git diff`, `git ls-tree`, `jq`, `grep`, `sha256sum`), the fleet census, or a live re-open of S116. No lane gate, selftest, counter or entry gate was executed (§Gate standard, Closure consequence); those are evidence-verified from committed receipts.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report author | `git log --format='%an %ae %H %ci' -- .ufo/reports/round-82/kasegi.md` | `kasegi-shokunin kasegi@shokunin.local 0132796c… 2026-11-06 18:38:18 -0300` | lane identity; filed after the landing commit (18:37:27) |
| SHONEN heading | report `## SHONEN` | one heading, 4 lines (`[~]`, `[ ]`, `[~]`, `[~]`) | conformant |
| cited commits + ancestry | `git merge-base --is-ancestor <h> master` for 1a50638e, b9589300, 4576a88e | `anc-ok` ×3 | conformant |
| pushed, clean | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain` | `branch=master local=4576a88e… remote=4576a88e… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | conformant |
| remote tip | `git ls-remote origin refs/heads/master` | `4576a88e85d0ee67197cf36f9f2b533040b840dd` | matches report |
| lane commits in range | `git log 1a50638e..4576a88e` | 2 commits (freeze, landing), both `kasegi-shokunin <kasegi@shokunin.local>` | conformant |
| prompt contract | headings of `.ufo/prompts/kasegi-round-82.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (SHONEN rule `:118`), §5 commit/push/L0, §6 hyaku addendum, §7 scratch | template contract carried |
| freeze integrity | `git diff --stat b9589300 4576a88e -- .ufo/waves/round-82/{claims.json,c1,c2,controls}` | empty; landing receipt `l1/L1-landing-r82.txt` prints `FROZEN-OK` ×9 | frozen bytes unchanged at landing |
| evidence timestamps | `l1/L1-landing-r82.txt:1` `2026-11-06T21:34:31Z` vs landing commit `18:37:27 -0300` (21:37:27Z) | receipt precedes commit | conformant |

Defects: none bearing on status.

## Per-claim re-check

### C1 — depth:verifiability — partly re-measured, counter evidence-verified

Re-measured (plain reads):

- Landed bytes: `git show <r>:corpus/instruments/recheck-cwd-census.py | sha256sum` → base `1a50638e` and freeze `b9589300` both `a3b58aa5…6dbec0`; landing `4576a88e` → `81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050`, equal to the frozen candidate `git show b9589300:.ufo/waves/round-82/c1/recheck-cwd-census.py | sha256sum`.
- Selftest 22 → 24: docstring `selftest cases=22` at base (`:36`, `:264`) and `cases=24` at landing (`:39`, `:284`). `diff` of sorted `check("<id>"` sets base vs landing adds exactly `bucket-sum` and `main-default`. `conform_ok` defined at `:258` and used by `main()` at `:795`; base blob has no `conform_ok`.
- Counter/table: `sha256sum` mutbat.py → `a7d4db43…ac55c`, table → `045edc07…5f26a` (match the report). `jq length` → `63`; classes `assertion 59, exception 1, neutral 3`; ids `S04 S05 J1 S07M B1 B2` present.

Evidence-verified (committed receipts, not executed):

- `controls/c1-donothing-r82.txt:66-67`: r81 bytes `a3b58aa5…` → `baseline=bad rows=63 killed=54 survived=2 … notderived=4 neutral_ok=0/3 decoy=broken`, `rc=1`; `:62-63` J1 and S07M `SURVIVED`.
- `controls/c1-candidate-r82.txt:81-82`: candidate `81677e9d…` → `baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60`, `rc=0`; counter selftest ok; candidate `selftest cases=24 failures=0`.
- `controls/c1-junkedit-r82.txt`: r81 junk edit `conformant rc=0`; J1-edited r82 `nonconformant rc=1`.
- `controls/c1-forgeries-r82.txt:7-12`: F6/F7 `rc=0` under counter r81 and `rc=1 decoy=broken` under counter r82; F8 `rc=0` under both (declared limit).
- `l1/L1-landing-r82.txt`: P1–P9 printed as frozen; P5 `RECHECK-CWD-RESULT conformant`, P6 `nonconformant rc=1`.

Before → after agrees with the report. Limit I accept as true from committed receipts: the claim's prose "F8 is the declared limit" is not the only residual — `w1/CriticClaims-receipts/mutbat-pathforge-table.txt:71-72` scores a path-reading forgery (`287c05ba…`) `killed=60 … rc=0` under the frozen r82 counter, because mutant temp dirs carry the row id (`c1/mutbat.py:221`, `prefix="mutbat-%s-" % row["id"]`). The report discloses this (CriticClaims F1, M82-2) and `l1/M82-2-constprefix-r82.txt:18-22` shows the constant-prefix fix rejecting it (`killed=0 rc=1`) while the candidate still passes (`rc=0`). This falsifies prose, not a frozen predicate.

### C2 — coverage — re-measured

| measure | base 1a50638e | freeze b9589300 | landing 4576a88e | report |
|---|---|---|---|---|
| `git ls-tree -r --name-only <r> corpus/knowledge \| grep -c '\.md$'` | 95 | 95 | 96 | 95 → 96 ✓ |
| registry rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 115 | 116 | 116 | 115 → 116 ✓ |
| S116 status / used-by (cells 9, 12) | absent | `queued` / `—` | `mined` / `corpus/knowledge/osv-high-quality-record-import-bar.md` | ✓ |
| `git diff b9589300 4576a88e -- corpus/SOURCES.md` row changes | — | — | one `-`/`+` pair, S116 only | ✓ |
| README Frontier rows `grep -cE '^\| *F[0-9]+'` | 59 | 59 | 60 (+F58 at `corpus/README.md:1257`) | F57 → F58 ✓ |
| snapshot `sha256sum corpus/source-snapshots/round-82/S116.txt` | — | — | `2198d329…ce9ca0` | ✓ |
| entry header | — | — | `source: S116 — https://google.github.io/osv.dev/data_quality.html`, `verified-at: 2026-11-06`, `recheck: … source-recheck.py --manifest … --source S116` | ✓ |

FRONTIER-CENSUS (`rows=58 admitted=58 closed=58 problem-rows=0 registry=116`, `FRONTIER-PASS F58 ids=S116`) and ENTRY-GATE (`S116 … ruleless=0 … pass rc=0`; labelled dump `ruleless=6 fail rc=1`) are evidence-verified from `l1/L1-landing-r82.txt:65-82`; the r81-gate side (dump `pass rc=0`) from `controls/c2-b8-controls-r82.txt` as quoted in `corpus/lessons/round-82.md:198-205`.

### Harm check

- `git diff --numstat 1a50638e 4576a88e`: `SCORECARD.md 22/0`, `LOG.md 12/0`, `PROVINCE.md 2/0`, `corpus/QUALITY.md 1/0`, `osv-determineversion-cc-library-versioning.md 4/0` (additions only); `SKILL.md 1/1` (the recheck-cwd pin row). SCORECARD diff adds only `## Round 82`.
- Density mean `272.8` before and after is evidence-verified (`l1/L1-landing-r82.txt:83-85`).
- R133 check by me: `awk '/^## Gate/{f=1} /^## Mistakes/{f=0} f' corpus/lessons/round-82.md | grep -ciE 'PENDING|TODO|TBD'` → `0`.
- Census (run by me): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok`, six inherited `W04` (S028 S029 S072 S076 S080 S085), `rc=0`.

## Discernment spot-check (LEARNING.md)

Live re-open: `curl -sSL https://google.github.io/osv.dev/data_quality.html` → `200`, final URL unchanged; HTML tags stripped, entities decoded, whitespace collapsed, each quote counted. Five of six quotes count 1 with tags replaced by spaces; Q05 counts 0 that way (inline markup around `GIT`) and 1 with tags removed without a space — present.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| cl2 valid prerequisite, "a record passes JSON Schema validation for the version of the OSV Schema it declares itself to comply with in the schema_version field" (S116.txt:36, 23 words) | admit | live page (count 1) + snapshot `:36` | agree | a stated import prerequisite, verbatim on the cited line; the entry rightly notes the `or 1.0.0 if it does not` fallback lives on the same line |
| cl5 GIT commits in repo, "for commit (GIT) ranges the commits exist in the specified repo (i.e. they are not from another GitHub fork)" (S116.txt:47, 19 words) | admit | live page (count 1, markup-insensitive) + snapshot `:47` | agree | a checkable record property on the cited line; not held by F31 (S080 defines range events, not repo existence) |
| S116.txt:43 prefer `fixed` over `last_affected` | reject (held) | snapshot `:43`; `corpus/source-snapshots/round-50/S080.txt:760-766`; `corpus/knowledge/osv-affected-range-events.md:56-63` (F31 Claim 3, cites S080.txt:762-766) | agree | the preference and its false-negative reason are already admitted under F31 |
| S116.txt:63-86 Appendix A schema summary | reject | live page: "(As at version 1.6.3, generated by Gemini from the OSV JSON schema)"; snapshot `:64` | agree | a generated restatement of the schema, not the project's rule text; its fixed/last_affected exclusivity is held at source (S080.txt:760-761) |

New registry row re-opened: S116 (`corpus/SOURCES.md:128`), tier A `docs`, opened 2026-11-06, `teaches` "what OSV.dev requires of a record before import…". Its ≤25-word quotes live in `corpus/source-snapshots/round-82/manifest.json`: `jq` gives word counts `12 23 6 10 19 13` at anchors `25 36 41 44 47 51`, all ≤25, each found once on its anchor line (`grep -c -F` → `1` ×6). `teaches` is grounded by Q01 + Q02.

Predecessor routing: r81 routed defect 1 became the appended correction in `osv-determineversion-cc-library-versioning.md` (round-82 section); defect 6 became QUALITY R133 grounded in M82-1; defects 2–4 are answered by the decoy limb, the bucket-sum conjunct and the G5 `ruleless` limb; defect 5's S07M row landed (killed by `main-default`).

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | improved | landed instrument strictly stronger: selftest 22 → 24 checks and bucket-sum wired into `main()` (re-measured); case-matched kills 54 → 60, neutral 0/3 → 3/3, J1 and S07M now killed, F6/F7 rejected by the r82 decoy limb (evidence-verified); score 4 → 4 nominal per R58 |
| coverage | improved | F58 admitted, knowledge 95 → 96, S116 `queued → mined`, frontier rows 59 → 60 (re-measured) |
| depth:density | unchanged | one-token SKILL.md pin edit; mean 272.8 both sides (evidence-verified) |

## Trend verdicts

- **expansion: improved** — one new entry on uncovered ground (OSV.dev's import bar for a record), citing a `mined` row; frontier F57 → F58; quotes re-found on the live page.
- **quality: improved** — the recheck-cwd gate kills 60/60 rows plus both decoys on the landing bytes against 54 and `decoy=broken` on the base; the r82 counter rejects two forgeries the r81 counter accepted; r81's stale cite received an appended correction; census `rc=0`. Carried limits are recorded and routed, not hidden.
- **discernment: improved** — this spot-check agrees on 2/2 admits and 2/2 rejects; the r81 spot-check's routed defects 1 and 6 became an appended correction and QUALITY R133 grounded in M82-1.

## Routed defects (lane fixes next round)

1. Path-label leak: `c1/mutbat.py:221` names mutant dirs after the row id, so a path-reading forgery scores `rc=0` under the frozen r82 counter (`w1/CriticClaims-receipts/mutbat-pathforge-table.txt:71-72`). Land the constant-prefix counter (M82-2; `l1/M82-2-constprefix-r82.txt`).
2. Decoys are unkeyed (ReviewC1 Major 1, `[INFERENCE]` simulation only); add a per-run secret and a committed forgery control that shows it failing and passing.
3. G5 is lexical: 8/14 G5 mutants survive (MutEntryGate); add a limb tying each rule to its cited line.
4. MutC1Hunt G1–G4 real gaps remain open; P1/P5/P6/P8 are stub-satisfiable (CriticClaims F2).
5. M82-3's stated-output check is a wave script (`l1/stated-output-check.py`), not a registered lane instrument; register it at the registry home (`SKILL.md`) or record why not.
6. Minor: the claims' parenthetical "six pins at lines 25 36 41 44 47 51" names snapshot anchors, not manifest lines (`corpus/lessons/round-82.md:181`); word it as snapshot anchors in future claims.
7. Carried from r81: the MutC1Hunt r81 survivors outside the r82 table and r81 defect 7 (`:32` rejection support) — no landed answer found this round; re-confirm or close in r83.

SHONEN: no box is fully checkable by a non-author this round (box 2, an end-to-end domain task in LOG.md, stays untouched).
