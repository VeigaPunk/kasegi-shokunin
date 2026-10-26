# kasegi round 35 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round kasegi r35, closure prompt `.ufo/prompts/closure/kasegi-round-35.md`.
Judged revision (pinned by the closure prompt and by the report as filed): base
`3266c9937b03062d9bbc2f436e20820115ed179c` → after `0aee0ef105395a2f1d6ace7eaeef13871bb26988`.
Driver digest (`.ufo/watchdog.log`, copied here because the log is mutable):

    2026-10-26T03:26:29-03:00 launch kasegi round=35 pgid=2458141 driver=hyaku-inline attempt=1
    2026-10-26T04:00:34-03:00 complete kasegi round=35; hyaku-inline attempt=1

**Verdict: not admitted (`rejected-honest-stop`; no axis harmed; lane status `ok`).** At the judged
revision both frozen kill rules fire: C1 — `filled by the L1` is still present in `SCORECARD.md`
and the D3 registry rows are absent from `SKILL.md`; C2 — the S052 capture the entry, row and
manifest pin is not in the tree. The lane landed the missing bytes *after* the `complete` line and
after filing (8ce6fb4 04:01:12, 5a25337 04:02:21, bb2dc8c 04:04:46, 48e6053 04:04:55; report errata
63ce2a63 04:01:19, 8cfcb5b6 04:02:33) while wave seats were still writing. That is M35-1 — this
round's own named mistake (wave writes after `complete`) — recurring.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report author | `git log --format='%an %H' -- .ufo/reports/round-35/kasegi.md` | `kasegi-shokunin e4eb5140…` (04:00:23), then errata `63ce2a63…` (04:01:19), `8cfcb5b6…` (04:02:33) | pass; errata appended after `complete` (defect) |
| SHONEN heading | read report `:80-85` | `## SHONEN`, four lines, all `[~]` with pointers | pass |
| cited hashes | every 7–40-hex token in the report → `git cat-file -t` + `merge-base --is-ancestor <h> refs/heads/master` | 0aee0ef, 3266c993, 617496b9, da2d3c68, aa6ad99, c1c6a5f, 8ce6fb4f, 5a253372: all commits, all ancestors; `1479694` is a byte count | pass |
| pushed | `jj-lane.sh state` at 04:01 | `local=0aee0ef… remote=0aee0ef… ahead=0` | pass at filing |
| leftovers at filing | `git status --porcelain` at 04:01 | 9 paths: ` M SKILL.md` (+13, the D3 rows), ` M build-spec.py`, `?? corpus/source-snapshots/round-35/S052.txt` (1,479,694 B), `?? c1-controls/fake-suite.sh`, `?? c2-controls/junk-f18.md`, `?? wave1.ready{,.dispatched}`, `?? wave1/ExecDoNothingReject.md`, `?? wave1/ScribeLesson.md` | **defect**: uncommitted round work the claims rest on |
| still moving at closure | `jj-lane.sh state` at 04:05 | `local=remote=48e6053… ahead=0 tracked=4 untracked=2` (SHONEN.md, lesson, two receipts modified; `ScribeScorecard.md`, `ScribeShonen.md` untracked) | **defect**: lane not quiescent after `complete` |
| prompt contract | `diff` of `.ufo/prompts/kasegi-round-35.md:1-140` vs `templates/round-prompt.md` | only placeholder substitutions; §6 hyaku addendum + §7 scratch directive appended | pass; prompt committed under lane identity (`41641539`, status-neutral) |

Not a marker: real report, real committed work → status `ok`.

## 2. Claims — re-derived at `0aee0ef` (plain measurements over committed bytes)

`s(){ git show $1:$2; }`, `B=3266c993…`, `A=0aee0ef…`. Re-measured = plain grep/ls-tree counts I
ran; evidence-verified = lane gate output I read in committed receipts (no sibling gate executed).

### C1 — depth:verifiability (held 4): **NOT VERIFIED** (kill rule fires)

| defect | measurement | B | A (judged) | reported after | match |
|---|---|---|---|---|---|
| D1 | `s $R SCORECARD.md \| grep -c 'filled by the L1'` · `grep -c c1c6a5f` · `grep -c '<LANE_HASH>'` | 1 · 0 · 0 | **1** · 3 · 0 | 0 · 3 · 0 | **no** — `SCORECARD.md:1271` (round-35 section) "final lane commit filled by the L1 in the closing commit" |
| D2 | `grep -c '201\.7'` · `grep -c '201\.2'` | 2 · 0 | 4 · 3 | erratum names 201.2 (×2) | yes (erratum at `:1246`; third 201.2 is the round-35 no-harm row `:1269`) |
| D3 | `s $R SKILL.md \| grep -c r-defect-closure` · `kill-rule-check` | 0 · 0 | **0 · 0** | 4 · 4 | **no** — the rows were in the working tree only (`git diff --stat 3266c99 0aee0ef -- SKILL.md` empty) |
| D4 | `git ls-tree -r $R -- .ufo/waves/round-34/wave1-results.json \| wc -l` · provenance note | 0 · 0 | 1 · 1 | 1 · note | yes |
| D5 | `claims-erratum-d5.md` present · `discriminating invocation` · `per-id occurrences` | 0 · 0 · 0 | 1 · 5 · 5 | 1 · 5 · 5 | yes |
| D6 | `L1Integration.md`: `did not file a receipt (dead seat` · `Correction (round 35)` | 1 · 0 | 0 · 1 | 0 · present | yes, but rewritten in place (−3/+6) where the frozen after says "appended note" |
| D7 | `QUALITY.md`: `supersedes R22` · `supersedes R23` | 0 · 0 | 1 · 1 | 1 · 1 | yes |
| suite | `git ls-tree` `r35-defect-closure.sh` · `r35-fixtures/` files | 0 · 0 | 1 · 64 | present | yes |

Suite verdict at A (derived from its committed source, not executed): `check_d1`
(`r35-defect-closure.sh:160-171`) exits 0 only when `grep -c -F 'filled by the L1' SCORECARD.md` is 0
→ open at A; `check_d3` greps `SKILL.md` for both names → open at A. So the suite cannot print
`closed=7/7` at the judged revision. Committed evidence: every `closed=7/7` receipt was measured on
the live worktree (`RevD5D6D7.md:141` "suite `closed=7/7 exit=0` on the working tree";
`CritOverclaim.md:62` `closed=4/7` at 06:44Z), never on an export of the cited head; base-export
`closed=0/7 exit=1` (`CritC1Kill.md:302`) and the selftest `cases=7 failures=0`
(`ExecClosureSuite.md:253`) are evidence-verified. Frozen kill rule clauses hit:
"`filled by the L1` placeholder prose still present" and "`closed` != 7/7".

Informational, post-`complete`: at `8ce6fb4f` `filled by the L1`=0; at `5a253372` D3 4 · 4. These
bytes landed after `complete` and after filing; they are not the round's judged state.

### C2 — coverage (held 7): **NOT VERIFIED at the judged revision** (capture absent)

| counter (frozen command, run on `git show $R:…`) | B | A | reported | match |
|---|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 17 | 18 (`:388`) | 18 | yes |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 51 | 52 | 52 | yes |
| S052 row | 0 | 1 (`:58`) | 1 | yes |
| entries with `^source: S052 ` | 0 | 1 (`cisa-kev-catalog.md`) | 1 | yes |
| `ls-tree corpus/knowledge/*.md` | 46 | 47 | 47 | yes |
| `git ls-tree -r $R corpus/source-snapshots/round-35/` | — | **`manifest.json` only** | `{S052.txt,manifest.json}` | **no** |
| `sources-census.sh validate --root … kasegi` (live tree, 04:03) | exit 0 W04 S028/S029 | exit 0, W04 S028/S029 only | same | yes |

The entry's own recheck (`cisa-kev-catalog.md:6`) states source-recheck "exits 2 when the manifest or
capture is absent" — at A the capture is absent, so the frozen kill clause "source-recheck S052 exit
!= 0" fires. Harness `entries=21 pass=21` is evidence-verified only as a worktree reading
(`ConnTrends.md:50` marks it `landed-wt`). Post-`complete` `5a253372` adds `S052.txt`; I re-opened it:
`git show 5a253372:corpus/source-snapshots/round-35/S052.txt | sha256sum` →
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` = row/manifest digest, 27,870 lines.

### Owned-axis harm check

`git diff 3266c99 0aee0ef -- SCORECARD.md`: 54+/15−; the 15 deletions are the round-34
placeholder paragraph and the `filled by the L1` line the D1 substitution replaces (read in full).
`git diff --numstat 3266c99 0aee0ef` over 175 paths: deletions only in `SCORECARD.md` (above) and
`L1Integration.md` (D6, 3 lines); `SKILL.md`, `PROVINCE.md` 0/0; `corpus/README.md` +28/0,
`SOURCES.md` +7/0, `QUALITY.md` +21/0, `LOG.md` +10/0, knowledge +91/0. No owned axis regressed.

### Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| depth:verifiability | unchanged | score held 4 by design; C1 falsified at A (D1 placeholder re-published in the round-35 section, D3 rows absent); five of seven closures did land |
| coverage | unprovable | F18/S052 counters move 17→18 / 51→52, but the pinned capture is not in A, so the entry's recheck cannot pass at the judged revision; content itself re-verified (§3) — not harmed |
| depth:density | unchanged | no claim; `SKILL.md` byte-identical base→A |

## 3. Discernment spot-check (`corpus/lessons/round-35.md` `## Gate`, at A)

| item | lane decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| F18 / S052 CISA KEV feed | admit | `curl -A kasegi-shokunin/1.0 https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` → 200, 1,807,090 B (= manifest `fetched_bytes`), sha256 `97a6e54b…` | agree (decision); disagree (evidence line) | live feed whitespace-normalized equals the capture; `catalogVersion 2026.10.23`, `count 1756` = 1756 records, 12 keys per record, `cvss` 0 occurrences; Q1–Q5 (7/2/4/8/19 words, ≤25) each occur exactly once in capture and live. But the Gate's "source-recheck exit 0 on committed bytes" is false at A (capture uncommitted) |
| S048 (quarantine slice) | reject `unreachable` | `curl https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` → 404, 748 B, Tomcat `HTTP状态 404 - 未找到` | agree | same status and byte count as the lane's `quarantine-verdicts.md:61`; no payload, nothing quotable |
| S068 (quarantine slice) | reject (nothing to adopt; duplicate of S040) | Cisco policy, instrument UA (`capture-source.py:32`): 200, 94,027 B at `sec.cloudapps.cisco.com/…`; plain `kasegi-shokunin/1.0` UA → 403 | agree | quoted sentence "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines…" occurs once in the tag-stripped text; lane `SOURCES.md:46` S040 carries the identical URL, so adoption would double-register one document |

New `SOURCES.md` row re-opened: S052 (`SOURCES.md:58`) — tier A scoped to CISA's own feed statements;
anchor cell names L2/L3/L4/L15472/L19165 and the manifest digest `06bfcc71…`; its pinned quotes
are ≤25 words and located (above). Census: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `ok`, exit 0.

## 4. Trend verdicts

- **expansion: unprovable-but-better** — one new entry on uncovered ground (exploitation status vs
  severity), citing a mined tier-A row, and its source re-verifies live; but at the judged revision
  the capture it is admitted against is absent, so the admission bar is not provable there.
- **quality: unchanged** — D2/D4/D5/D6/D7 corrections landed (stale/false statements marked), but
  the round re-published a D1-class placeholder and shipped an evidence pointer (`S052.txt`)
  unresolvable at its own cited head.
- **discernment: improved** — the spot-check agrees with the gate on the admit and both rejects;
  `RevEntryF18` REFUSE→repair→ADMIT and the junk-twin rejection are on record.

## 5. Routed defects (kasegi owes these next round)

1. **Close against one head (M35-1 recurrence).** Quiesce the wave, commit every path the claims
   rest on, then file; record the suite and harness run over `git archive <final lane commit>`, not
   the worktree. Append a lesson/QUALITY row citing this spot-check.
2. **Re-claim with frozen evidence.** C1/C2 re-measure closed at `5a253372` (D1 0, D3 4·4, capture
   digest matches); a next-round claim may carry them only with a frozen export run of that head.
3. **D1 guard is file-wide literal.** A later round's own section re-opened it (`SCORECARD.md:1271`);
   CritC1Kill F-1…F-5 already note clause greps satisfied by mention/negation — make D1/D3/D7 checks
   section-scoped or structural.
4. **Append corrections, not rewrites.** D6 rewrote a committed round-34 receipt bullet in place
   (−3/+6) though the frozen after said "appended note"; the report was re-filed twice post-`complete`.
5. **False evidence lines at A.** Lesson `## Gate` "source-recheck exit 0 on committed bytes" and
   `## No-harm` "`SKILL.md` +13/0" / "`LOG.md` 0 changed" do not hold at `0aee0ef` (measured 0/0 and
   +10/0): append corrections.
6. **Dirty tree at closure.** Two untracked seat receipts and four modified files after `48e6053`;
   commit or record them as discarded.

SHONEN: all four boxes `[~]`; box 2 (end-to-end domain task) has no new executed task — not
non-author-checkable as complete; no promotion signal.
