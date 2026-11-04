# Round-68 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r68 (attempt 3) · base `d0f48405e7fe44a53a28305785dc4d881a414194` · final lane hash
`b0b9fb871e3cf45a51febd7671e2331c4f54637a` · measured implementation
`82b3b7d4704e914eb224e7bb24e57aa9cbd8603f` · report `.ufo/reports/round-68/kasegi.md` (fleet commit
`f71d44ebf3868f1b90adba91cb23a099ac240b40`, 2026-11-04 19:06:49 -0300, by `kasegi-shokunin`,
15123 bytes) · prompt `.ufo/prompts/kasegi-round-68.md` (828 lines, last committed `56884e92`
18:42:43 by `kasegi-shokunin`).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-04T18:27:42-03:00 launch kasegi round=68 pgid=816980 driver=hyaku-inline attempt=1
2026-11-04T18:36:33-03:00 lane-dead-no-report kasegi round=68; retry same round (hyaku-inline attempt=1: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-68/kasegi.md)
2026-11-04T18:36:35-03:00 launch kasegi round=68 pgid=958339 driver=hyaku-inline attempt=2
2026-11-04T18:42:43-03:00 lane-dead-no-report kasegi round=68; retry same round (hyaku-inline attempt=2: L1 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-68/kasegi.md)
2026-11-04T18:42:45-03:00 launch kasegi round=68 pgid=1254127 driver=hyaku-inline attempt=3
2026-11-04T19:07:18-03:00 complete kasegi round=68; hyaku-inline attempt=3
```

## Conformance (step 1)

- **Attribution.** `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-68/kasegi.md` →
  `kasegi-shokunin <kasegi@shokunin.local> f71d44eb… 2026-11-04 19:06:49 -0300`, after the lane tip
  `b0b9fb87` (19:06:25) which it cites. All five round commits carry `kasegi-shokunin
  <kasegi@shokunin.local>` as author and committer; none touches `.ufo/state/` or
  `.ufo/watchdog.log` (`git log --name-only d0f48405..b0b9fb87 | grep -cE '^\.ufo/(state|watchdog)'` = 0).
- **SHONEN heading.** `grep -c '^## SHONEN'` = 1; four box lines (`[~]`, `[ ]`, `[~]`, `[~]`) for the
  four boxes of `SHONEN.md` (`grep -c '^- \['` = 4). No `[x]` written by the report or by this reviewer.
- **Ancestry.** Base and all five cited commits exist (`git cat-file -e`) and
  `git merge-base --is-ancestor <h> refs/heads/master` holds for each (git HEAD is detached; tested
  against the branch ref): `d0f48405`, `3dfe6f16`, `7c4f9f7e`, `82b3b7d4`, `29f1ff59`, `b0b9fb87`.
- **Lane state.** `jj-lane.sh state` → `branch=master local=b0b9fb87… remote=b0b9fb87… ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin
  refs/heads/master` → `b0b9fb871e3cf45a51febd7671e2331c4f54637a`. No uncommitted round work.
- **Prompt fidelity.** `diff <(sed -n 1,140p .ufo/prompts/kasegi-round-68.md) templates/round-prompt.md`
  shows only the `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` macro substitutions (l.1, 5–6, 46,
  61, 65, 69, 101, 133, 135, 139); the §6 hyaku addendum starts at l.141, appended. Template contract
  carried.
- **Marker check.** Substantive report: two declared claims, five landed commits tied to LOG round-68
  bullets, committed receipts under `.ufo/waves/round-68/`. Status `ok`. Attempts 1–2 left no lane
  bytes (base byte-clean when attempt 3 started, per the report and the commit range).
- **Timestamp defect (status-neutral).** `claims.json` (`git log` → only commit `7c4f9f7e`, committer
  date 18:50:37 -0300) carries `"frozen_at": "2026-11-04T21:52:00Z"` = 18:52:00 -0300, 83 s *after*
  the commit that ships it and 66 s after the implementation commit `82b3b7d4` (18:50:54). Commit
  order (freeze before implementation) is correct; the declared freeze time is future-dated
  (§Evidence standard). Routed V68-1.

## Claim re-checks

C1 is a **gate claim**: per PROTOCOL §Gate standard ("Closure consequence") its committed evidence was
verified and the lane's gate and C1 counter were **never executed** by this reviewer. C2 is countable
and was **re-measured** over committed bytes with plain counts plus the lane's read-only census
counters.

### C1 — depth:verifiability, 4 → 4, delta 0, nominal R58

```
$ git show <rev>:corpus/instruments/figure-audit.py | sha256sum
d0f48405  8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247
7c4f9f7e  8147350c…   (freeze commit: gate bytes unchanged — no implementation landed before freeze)
82b3b7d4  10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8
b0b9fb87  10c87100…   (tip identical to the measured revision)
$ sha256sum controls/c1-probe-run-r68.py controls/base-gate-d0f48405.py ; git show 3dfe6f16:…/c1-probe-run-r68.py | sha256sum
785e38fd1393f345226fbd34e3a2310eed597bb7b95997478066db158c496b4b   (= claims.json pins.counter_sha256, unchanged since 3dfe6f16)
8147350c…                                                           (= pins.base_gate_sha256)
```

`claims.json` pins `candidate_trial_gate_sha256 = 10c87100…`, the exact landed gate. Committed receipts
(read, not re-run):

```
controls/final-verification-r68.txt (b0b9fb87)   VERIFY measurements=8 failures=0 gate_sha256=10c87100… mode=candidate
   sort-compress-refused ok rc=2 marker_runs=0 · git-textconv-refused ok rc=2 marker_runs=0 · controls=5 failed=0
   selftest cases=77 failures=0 · mutbat killed=5/5 · FIGURE-AUDIT figures=35 ok=35 · red-fixture rc=1 · fixture_changed=0 marker_runs=0
controls/c1-base-donothing-r68.txt (3dfe6f16)    VERIFY measurements=8 failures=4 gate_sha256=8147350c… mode=base
   sort-compress-refused FAIL marker_runs=18288 · git-textconv-refused FAIL marker_runs=1
   selftest FAIL selftest cases=73 · no-write-side-effect FAIL marker_runs=18289
controls/seat-reproduction-r68.txt               runs A/B from git-archive exports and C/D from clean clones at d0f48405 / 82b3b7d4
                                                 reproduce both ends byte-identically (exit 1 / exit 0)
```

Static delta (`git diff d0f48405 82b3b7d4 -- corpus/instruments/figure-audit.py`, 18+/4−): `DENIED_FLAGS`
gains `--compress-program` (sort) and `--textconv` (git show), `EXPECTED_CASES` 73 → 77, four selftest
cases (equals, space, quoted sort spellings; `git show --textconv HEAD`), docstring and an R68 comment.
Nothing in the allow-list widened.

Verdict: **claim verified on its frozen predicate.** The frozen target names the equals/space/quoted
spellings; the wave's attack seats (`w1/CriticC1.md` l.6, l.26, l.41–42, l.58–61) show the class is
open — unique long-option prefixes (`--compress-p=`, `--co=`) still run the compressor 18288 times at
both gates, plain `git show <commit>` runs the textconv driver with no flag, and `git cat-file
--textconv/--filters` execute — all *identically at base*, so nothing was widened; the report names
them as round-69 residuals rather than hiding them. Routed V68-3.

Report transcription defect: report l.119 quotes the base line as `MEASURE selftest ok selftest
cases=73`, but the committed receipt (and the seat reproduction) reads `MEASURE selftest FAIL selftest
cases=73`; as transcribed, the block shows three FAIL lines under `failures=4`. Routed V68-2.

### C2 — coverage, 8 → 8, score held

```
$ git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'      101 -> 102
$ … kind histogram (col 4)          docs=70 -> docs=71 (dataset 3, community 1, spec 19, paper 1, code 3, own-work 4 unchanged)
$ git ls-tree -r --name-only <rev> corpus/knowledge/ | wc -l                                 83 -> 84
$ git show <rev>:corpus/README.md | grep -oE '^\|[[:space:]]*F[0-9]+' | tr -d '| ' | sort -u | wc -l   45 -> 46
$ git show <rev>:corpus/instruments/knowledge-expected.txt | wc -l ; grep -vc '^#'        85/83 -> 86/84
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt                               exit 0
$ python3 -B corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0 registry=102
FRONTIER-PASS F46 ids=S102            entries=49 pass=49 exit=0
$ python3 -B corpus/instruments/capture-binding-check.py                                    records=82 bound=82 unbound=0
$ python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-68/manifest.json --source S102   rc=0 (8 quotes Q01,Q02,Q04–Q09 OK)
$ sha256sum corpus/source-snapshots/round-68/S102.txt ; wc -l                               6ebb8552…c2caa0, 429 lines, 7595 bytes
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
six W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085 — inherited, none names S102); kasegi ok …/corpus/SOURCES.md; exit 0
```

Every frozen after-value reproduces. `git status --porcelain` stayed empty after the counters. Verdict:
**claim verified (re-measured).**

V67 dispositions re-measured: `citation-ground-check.py --root .` → `findings=6`, `class-lane-bare=1`
(the report's 10 → 6 and 5 → 1 after-values reproduce; the remaining items are inherited).

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability (lowest, 4) | **improved** | Base control executes both named programs (18288 + 1 runs, `failures=4`); the measured gate `10c87100` refuses them at parse time with `failures=0`, selftest 73 → 77, no widening. Score held at 4 nominally per R58 (the axis metric is not read by this gate); class-level residuals are open and routed, not claimed. |
| coverage (8) | **improved** | F46 admitted on S102 (registry 101 → 102, knowledge 83 → 84, frontier 45 → 46, capture 81 → 82, census exit 0), all re-measured; score held at 8. |
| depth:density (9) | **unchanged** | Not targeted; SKILL gains a registry-pin update and one amendment; no credit taken. |

No owned axis is harmed: `git diff --numstat d0f48405 b0b9fb87` shows `SCORECARD.md` +29/−0,
`LOG.md` +14/−0, `PROVINCE.md` and `SHONEN.md` unchanged, no knowledge entry superseded (the F45 entry
gains +5/−0 appended corrections). The in-place deletions are the SKILL registry row (pin 73 → 77),
README bare-path fixes (V67-2, 12 lines), the SOURCES lead retirement, and a re-indent of a closed
round-67 receipt (see V68-4).

## Discernment spot-check (non-author)

| # | Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|---|
| 1 | S102 admit (OpenSSF Scorecard API swagger 2.0) | admit, tier A docs, mined | `curl https://api.securityscorecards.dev/swagger.json` 2026-11-04 → HTTP 200, 11802 bytes, 429 lines; committed `S102.txt` | **agree** | Live body with leading whitespace stripped equals `S102.txt` except the final newline; L13 "API to interact with a project's published Scorecard result", L15 `1.1.0`, L17 host `api.scorecard.dev`, L353 "Aggregate score of the repository" and the `^[0-9a-fA-F]{40}$` commit pattern / "OIDC verified" publish POST all sit where the row says. It is the API's own contract, distinct from S086's check docs. |
| 2 | Reject the live project instance as an entry source | reject | `curl https://api.securityscorecards.dev/projects/github.com/ossf/scorecard` → HTTP 200, 13259 bytes, 1 line; `.date` 2026-11-03T06:28:58Z, `.score` 8.8, 18 checks | **agree** | Same byte count the lesson recorded; a single-line JSON gives no line anchor, and date/score are per-analysis instance values that will drift. Refusing it as ground is correct. |
| 3 | Reject the `1.1.0` version literal as a pinned quote | reject (too short) | `corpus/source-snapshots/round-68/manifest.json` (quote ids Q01, Q02, Q04–Q09 — the Q03 gap) | **agree** | A 5-character literal does not identify its location; the version is still recorded as an anchor (L15) in the row, not as a quote. |
| 4 | New registry row S102 | row written as claimed | `corpus/SOURCES.md:114` | **agree** | 13 `|`-fields (11 columns), next unused id, tier A / docs / mined / opened 2026-11-04 / recheck 2027-05-03 / used-by path exists; Gate quote "Aggregate score of the repository" is 5 words (≤25) at L353, verified live. |

## Trend verdicts

- **Expansion — improved.** F46 admitted on ground no held row covered (the retired lead line at
  base `corpus/SOURCES.md:164` said S086 "not a general scorecard.dev API contract"); registry, knowledge,
  frontier and capture counts all +1, re-measured above.
- **Quality — improved.** Admitted entry F45 had a false count (54 vs 58 pinned quotes) and a wrong
  anchor (L463 vs L462) routed as V67-1/V67-3; both are now marked by appended corrections, and
  citation-ground findings fell 10 → 6 (re-measured). No admitted entry fails its re-check; the
  ledger still re-derives 35/35.
- **Discernment — improved.** This spot-check agrees with the gate on the sampled admit and both
  sampled rejects; the wave's attack seats defeated the repair as a class and the receipts were
  landed and named as residuals rather than narrowed into a pass.

## Routed defects and notes

1. **V68-1 (lane, minor, evidence standard).** `.ufo/waves/round-68/claims.json` `frozen_at`
   `2026-11-04T21:52:00Z` is later than its own commit `7c4f9f7e` (21:50:37Z) and the implementation
   commit `82b3b7d4` (21:50:54Z). Record an appended correction naming the actual freeze time.
2. **V68-2 (lane, minor, report transcription).** Report l.119 prints the base selftest line as `ok`;
   `controls/c1-base-donothing-r68.txt` says `FAIL`. Note it in the next report/LOG as a correction.
3. **V68-3 (lane, substantive residual).** Derive-gate program-execution class still open at the
   measured gate: sort long-option prefixes (`--co=`, `--compress-p=`; also `--outp=` for `--output`),
   default textconv on plain `git show <commit>`, `git cat-file --textconv/--filters`, merge-diff
   forms (`w1/CriticC1.md` R69-a..d). Also: the four new selftest cases assert exit code only, not
   `reason=` (CriticC1 (c)).
4. **V68-4 (lane, minor, append-only receipts).** `.ufo/waves/round-67/controls/driver-pins.json` was
   rewritten in place (39+/39−; `git diff -w` shows one semantic line, the V67-4 note, the rest is
   re-indentation). A closed round's pinned receipt should take an appended correction, not a
   reformat that changes its digest.
5. **V68-5 (lane, minor, receipt prose).** `controls/seat-reproduction-r68.txt` header names "GNU
   coreutils sort 9.12", but this host's `sort --version` prints `sort 0.8.0` (uutils), as the report
   itself says; the counter docstring says "six" read-only controls while it runs five; the R68
   gate comment and SKILL amendment say a "420 KB fixture" while the receipt measures 480000 bytes.
6. **Inherited.** V67-5 (`recheck-audit.py` exit 1, 9 `cwd_fail`) and V67-6 (`.ufo/state/kasegi.round`
   stale at 17, operator-owned) stand.
7. **Operator note (promotion, operator-owned).** SHONEN boxes 1, 3 and 4 are `[~]` author-asserted
   and checkable by a non-author against committed bytes; box 2 stays `[ ]` (no authorized
   end-to-end domain task). No box was marked here.

No lane-authored file was edited by this reviewer; this file is the only artifact written in the lane.
