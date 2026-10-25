# InheritedReuse — checkpoint-vs-worktree inheritance audit (round 23, C1/C2)

Axes in scope: **depth:verifiability** (do the landed C1/C2 counter-artifacts still
describe the bytes the tree now has?) and **coverage** (which of the reused
artifacts' load-bearing premises the current tree contradicts). Read-only seat: the
only write is this file. Executor rule followed — every run of code under test used
copies in `/tmp/kasegi-r23-falsify-inherited/`, never the lane tree.

## 0. Reconstructed contract of the artifacts under test

Frozen claims (`.ufo/waves/round-23/claims.json`, unchanged since the checkpoint):

- **C1** `depth:verifiability` — "Make MIRROR-EQUIVALENT sound: bounty-prefixed and
  relative mirror fallback paths cannot credit parent traversal or symlink escapes
  outside the selected mirror. Preserve valid confined mirror and missing-file
  controls; reject sibling-root prefix confusion." Detector = `corpus/instruments/resolve.py`
  `classify` plus copied real CLI TSV. Evidence designated by `after`: "All declared
  mirror-escape and prefix-confusion fixtures classify GONE".
- **C2** `coverage` — admit F06/F07/F08 "only after official text opens, exact
  located quotes and executable local rechecks"; `count` = admitted rows in
  `corpus/README.md`, frontier 5/8 → 8/8.
- `admission`: independent non-author closure only; L1 holds the planner seat.
- Note on later scope: `SCORECARD.md`'s round-23 errata re-scopes the axis move as
  **mirror-fallback soundness, not "detector soundness"** (the lane-relative
  `INTERNAL` branch stays unconfined, the bounty literal hit is reported as written).
  Neither the claim text nor `claims.json` changed; the errata is a reading.

What the inherited attempt (checkpoint `8bf9807`, "policy-paused, unadmitted, no task
resumption") left in the tree: the three F06–F08 knowledge entries, the six
`SOURCES.md` rows, the three pinned snapshots, `source-recheck.py`, the 64-seat
wave-1 registry and 44 seat reports — but **no** C1 code change (`resolve.py` was
byte-identical at `922a4dde` and `8bf9807`) and **no** manifest (so every entry
`recheck:` exited 2).

## 1. Pins (tree moved during this audit — see §2)

| object | identity |
|---|---|
| checkpoint under test | `8bf9807` = `8bf980721554d2d24bcc83e2e0996e0c27684a06` |
| lane tip at audit start | `953c278` |
| lane tip at audit close | **`f6966d4`** — six unpredicted commits landed mid-audit: `2712c99`, `4d9231e`, `12edac4`, `8acb255`, `bf9ce02`, `f6966d4` |
| audit wall clock | 2026-10-25 06:36–06:53 **UTC** (03:36–03:53 local, host TZ `-03`) |
| `8bf9807`→`953c278` diff for assigned paths | `9 files changed, 1618 insertions(+), 1 deletion(-)` |
| scratch | `/tmp/kasegi-r23-falsify-inherited/` |

The C1 counter went through **five** generations inside this audit. Any sentence
about "the matrix" is meaningless without the generation:

| generation | resolver sha256 | matrix cases / sha256 | where it lived |
|---|---|---|---|
| G13 | `ed9a9dae…` | 13 / `5e61a33e…` | committed `953c278`; receipt `c1-fixed.json` |
| G17 | `8dd45bc8…`(a) | 17 / `5c64e014…` | worktree 06:43Z |
| G20 | `fce5b84b…` | 20 / `4e39f65c…` | worktree 06:47Z |
| G22 | `fce5b84b…` | 22 / `158a423c…` | worktree 06:48:20Z |
| G23 | `fce5b84b…` | 23 / `332a5fe9…` | committed `4d9231e` + dirty receipts at 06:48:42Z |
| **G24** | **`690153ad…`** | **24 / `d05b1e0c…`** | committed `f6966d4`, 06:53Z — the ladder was still moving when this report closed |

(a) G17/G20 also carried `9e0b5751…` for a window (see §2a–2b). Findings below are
labelled with the generation they hold for; §4.0 is the status board.

## 2. Every file changed since the checkpoint, in the assigned scope

`git diff --numstat 8bf9807 HEAD -- corpus/knowledge/multiparty-vulnerability-coordination.md corpus/knowledge/cna-assignment-and-vulnerability-rules.md corpus/knowledge/cra-manufacturer-reporting-duties.md corpus/SOURCES.md corpus/source-snapshots/round-23 corpus/instruments/source-recheck.py .ufo/waves/round-23`

```
561  0  .ufo/waves/round-23/c1-baseline-resolver.py
185  0  .ufo/waves/round-23/c1-baseline.json
185  0  .ufo/waves/round-23/c1-fixed.json
229  0  .ufo/waves/round-23/falsify-spec.json
  1  0  .ufo/waves/round-23/falsify/refusal-1.json
405  0  .ufo/waves/round-23/falsify/swarm-registry.json
  5  0  corpus/knowledge/cna-assignment-and-vulnerability-rules.md
  1  1  corpus/knowledge/cra-manufacturer-reporting-duties.md
 46  0  corpus/source-snapshots/round-23/manifest.json
```

**Unchanged from the checkpoint to `953c278`** (nothing repaired in the first landing; see §2a for the post-audit commits, which touched three of these):
`corpus/knowledge/multiparty-vulnerability-coordination.md` (now +8/−1),
`corpus/SOURCES.md` (now +1: S031), `corpus/instruments/source-recheck.py` (now +11),
`corpus/source-snapshots/round-23/{S018,S029,S030}.txt` (still untouched),
`.ufo/waves/round-23/{claims.json,before-instruments.json,opened-source-snapshots.json,source-open-transcript.json,build/**}`.

Cited-by files changed at `953c278` but outside the assigned path list (evidence is
presented through them, so they are in scope as *presentation*): `corpus/README.md`
(3/3, the F06–F08 flip), `corpus/lessons/round-23.md` (167/0, attempt-2 section),
`SCORECARD.md` (34/0, round-23 result row).

### 2a. Post-audit commits (not present when the audit began)

Four commits landed between 06:44Z and 06:50Z, so the table above is the **first
landing only**. At close (`HEAD` = `8acb255`, 06:50:29Z) the assigned-path delta is
much larger:

```
2712c99 round-23: post-attack repairs; F07 to current CNA 4.2.6 (S031); 20-case containment matrix; c2 receipts
4d9231e round-23: log the post-attack repairs and final C1/C2 measurements
12edac4 round-23 seal: 23-case matrix with ordering/prefix pins, declared recheck normalization, Q8/R10, final receipts
8acb255 round-23: record the failing Q7/Q8 control exits beside the clean runs
bf9ce02 round-23 rescue: 24-case matrix, docstring truth fixes, supplementary Gate rows for S018/S031, corrected census
f6966d4 round-23: receipts carry per-case method/domain; baseline-vs-landed routing visible
```

`git diff --numstat 953c278 HEAD -- corpus/ SCORECARD.md LOG.md`:

```
 70   0  LOG.md                                             31   0  SCORECARD.md
  7   0  corpus/QUALITY.md                                   9   3  corpus/README.md
  1   0  corpus/SOURCES.md                                 145  55  corpus/instruments/mirror-containment-check.py
171  19  corpus/instruments/mirror-containment-fixtures.json 22  10  corpus/instruments/resolve.py
 11   0  corpus/instruments/source-recheck.py                43  29  corpus/knowledge/cna-assignment-and-vulnerability-rules.md
 14   2  corpus/knowledge/cra-manufacturer-reporting-duties.md 8   1  corpus/knowledge/multiparty-vulnerability-coordination.md
 60   0  corpus/lessons/round-23.md                        136   0  corpus/source-snapshots/round-23/S031.txt
136  20  corpus/source-snapshots/round-23/manifest.json
```

New in the wave directory: `c2-controls.txt` and `c2-recheck-{S018,S029,S030,S031}.txt`
(receipts for the failing controls and the clean runs), plus ~30 `falsify/*.md`
seat reports. State at close: `HEAD`=`8acb255`, clean except ten `falsify/*.md`
(including this report), so the production bytes I measured are the committed ones.

What the four commits change materially:

- **F07 authority moved to `S031`** (CNA Operational Rules 4.2.6, approved
  2026-10-14, effective 2026-10-20; 136-line normalized `S031.txt`). `README.md`
  F07 now cites S031; `SOURCES.md` gained row S031 ("supersedes S030"); the cna
  entry was rewritten (43/29) and its `source:`/`recheck:` now name S031.
- **C2 pins grew from 19 to 32 assertions** across four snapshots
  (`S018 6, S029 9, S030 7, S031 10`), still with **0 misses** (`TOTAL quotes 32
  MISSES 0`), and four rechecks exit 0: `S018` 7 lines, `S029` 10, `S030` 8,
  `S031` 11 — counts consistent with digest+quotes for each.
- **The matrix grew 13 → 17 → 20 → 22 → 23 cases.** Final: 11 escapes, 12 controls,
  `matrix_sha256=332a5fe9…`, baseline `922a4dd` bytes **0/11 escape GONE** and
  controls 12/12 (12/23 pass), landed `fce5b84b…` **23/23**. The two cases
  `relative-priority-lane-first-control` and `mirror-root-prefix-sibling-escape`
  were added because mutation seats showed the earlier matrix could not see them
  (`SCORECARD.md` errata, round-23 append-only block).
- **`resolve.py` root-only bounty citations were taken back to their pre-round
  verdict.** The G17/G20 ternary that mapped `~/Projects/bounties` to the mirror
  root is gone; the final bytes carry the comment "Root-only bounty citations keep
  their pre-r23 verdict" and my probe returns `GONE` for both
  `~/Projects/bounties` and `~/Projects/bounties/` (§4.0).

### 2b. Byte-level drift observed *during* this audit

The working tree changed between 06:36Z and 06:43Z UTC while I was reading it. The
first `git status --porcelain` (06:36Z) showed only ` M LOG.md`; by 06:40Z it showed
five modified files plus ~19 new `falsify/*.md`, and by 06:43Z the resolver, the
fixture matrix and the checker had all moved. `resolve.py` alone changed twice:

| time (UTC) | `corpus/instruments/resolve.py` sha256 | matrix `cases` / sha256 | evidence |
|---|---|---|---|
| ~06:36–06:37 | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` | 13 / `5e61a33e…b5e76a9` | `sha256sum`; matrix printed the same `resolver_sha256` twice |
| 06:40:53 | `9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde` | 13 / `5e61a33e…b5e76a9` | `sha256sum`; matrix printed the same `resolver_sha256` |
| 06:43:23 | `8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848` | **17** / `5c64e014…cbed73e6e` | matrix `cases=17 escape=7 controls=10 pass=17 fail=0`; `mirror-containment-check.py` also moved (`53742c8d…`) |
| — | git blob `83905b2` vs `HEAD` blob `490b19d` | fixtures blob `504c8c9` vs `HEAD` `4ede1bc` | `git diff HEAD -- corpus/instruments/` |

The three-entry and manifest edits are likewise uncommitted (` M` in `git status`).
I attribute no authorship: the contract forbids me from editing production, and the
drift may be L1 integration. But **the report below distinguishes "committed
`953c278` bytes" from "live worktree bytes at 06:43Z"**, because they differ.

## 3. Repair verdict per changed file (independently reproduced)

| file | claim of change | my verdict and evidence |
|---|---|---|
| `corpus/instruments/resolve.py` (+29/−8) | exact-root bounty boundary + `under_mirror()` on bounty and relative fallbacks | **Repairs a real defect, verified causally.** Inherited bytes at `8bf9807` have `if base.startswith(BOUNTY_PREFIXES)` (a tuple prefix test) and `rel = base.split("/Projects/bounties", 1)[1].lstrip("/")` with `if m:` and no confinement; committed bytes replace both with `bounty_suffix()` + `if m and under_mirror(p, mirror_root)`. Independent replay (`--resolver` = inherited bytes) gives **0/6 escape GONE, 7/13, exit 1**; committed bytes give **6/6 GONE, 13/13, exit 0**. |
| `corpus/instruments/mirror-containment-fixtures.json` (new; 13 cases committed, 17 live at 06:43Z) | frozen matrix, escapes pin GONE | **Sound as an instrument, sensitive to both defects.** Case-level results on the two byte sets differ on exactly the 6 escape cases and on zero controls. Two cases (escape + control) share the same citation `~/Projects/bounties-legacy/README.md:1`; the fixture `note` explains the discrimination, so this is not a duplicate-case error. The four live-added cases (two literal-present carve-out controls, one absolute-form fallback control, one absolute prefix-sibling escape) all pass on the live resolver — but none of them pins a bare-root citation (F1). |
| `corpus/instruments/mirror-containment-check.py` (new; committed `1bc2db10…`, live `53742c8d…`) | copied-CLI replay | **Reproducible.** My three runs (committed bytes ×2, inherited bytes ×1) reproduced the committed receipts case-for-case (`fixed identical: True`, `baseline identical: True`); `matrix_sha256=5e61a33e…b5e76a9` equals `sha256sum` of the committed fixtures file. The checker itself changed in the worktree, so the committed receipts cannot have been produced by the current checker+matrix pair. |
| `.ufo/waves/round-23/c1-baseline-resolver.py` (new) | "do-nothing" control = `git show 922a4dd:resolve.py` | **Correct.** `diff <(git show 8bf9807:corpus/instruments/resolve.py) c1-baseline-resolver.py` → no output; `git diff --stat 922a4dde 8bf9807 -- corpus/instruments/resolve.py` → no output. Recorded `resolver_sha256` matches the file. |
| `.ufo/waves/round-23/c1-baseline.json` (new) | escape 0/6, controls 7/7, 7/13 | **Matches my rerun** (`baseline identical: True`). |
| `.ufo/waves/round-23/c1-fixed.json` (new) | escape 6/6, controls 7/7, 13/13 | G13 receipt: matched the bytes it pinned, then went stale mid-audit, then was **regenerated at G23** (23 cases, `332a5fe9…`, `fce5b84b…`). See §4.0/F1. |
| `corpus/source-snapshots/round-23/manifest.json` (new, +46) | 19 quote assertions + 3 digests | **All 19 quotes are literal substrings** (`TOTAL quotes 19 MISSES 0`); the three digests equal `sha256sum` of the `.txt` files; `source-recheck.py` exits 0 for S018/S029/S030 with the claimed line counts (7/7/8). This repairs the inherited "recheck exits 2" defect. |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` (1/1) | Article 71 quote corrected | **Repairs a genuine misquote.** Inherited row (`git show 8bf9807:…:50`) quoted “It shall apply from 11 December 2027.”; `grep -c` of that string in `S029.txt` = **0**, of “This Regulation shall apply from 11 December 2027.” = **1**. The repaired entry quote is now an exact substring. |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (+5) | Quote-fidelity note for `4.1.9` `<u>` markup | **Accurate disclosure, not a quote correction.** `S030.txt:165` carries `are <u>Independently Fixable</u>`; the entry table quotes the rendered form, which is *not* a substring (`OUT` in my per-doc check). The note states exactly this and points at the manifest, which asserts the literal bytes. Consistent, and the divergence is markup only. |
| `.ufo/waves/round-23/falsify-spec.json`, `falsify/refusal-1.json`, `falsify/swarm-registry.json` (new) | 36-seat wave, refused at dispatch, no replacement | **Counts check out.** `falsify-spec.json` items = 36, `maxLanes` 64; registry members = 36 with role tally `critic 9, reviewer 7, executor 7, scout 4, mutation-tester 3, sentinel 2, revenger 2, connector 1, scribe 1` — identical to the lesson's prose. `refusal-1.json` records `refused:true`, `seats:36`, job-limit error. |
| `corpus/knowledge/multiparty-vulnerability-coordination.md` | unchanged at `953c278`; +8/−1 at `8acb255` | At the first landing nothing was repaired — F06 rested entirely on inherited bytes, and all **6** quoted sentences are literal substrings of `S018.txt`. The post-audit commit adds the `cd …` recheck prefix (F3) and a *Capture gap* disclosure that I verified: `S018.txt` starts at `## Definitions`, contains no "Spring 2020", and ends at the `Use coordinators` lead line. |
| `corpus/SOURCES.md`, `source-recheck.py`, `S018/S029/S030.txt` | unchanged at `953c278`; SOURCES +1 row and `source-recheck.py` +11 at `8acb255` | At the first landing the census reproduced the lesson exactly: 30 rows, tier `A=28 C=2`, status `mined 18 / queued 9 / rejected 3`, `used-by` 18; S029 "supersedes S024", S030 "supersedes S022". At close: **31 rows, A=29 C=2, mined 19 / queued 9 / rejected 3, used-by 19** — the deltas are S031 and the S030 double-attribution in F10. |
| `corpus/README.md` (3/3 at `953c278`; 9/3 by `8acb255`) | F06–F08 queued→admitted; F07 sources cell later S030→S031 | **Reproduces:** `grep -cE '^\| F0[6-8] .*\| admitted \|'` → **3**; `grep -cE '^\| F0[1-8] .*\| admitted \|'` → **8**; each `entry` path exists. |
| `corpus/lessons/round-23.md` (167/0 at `953c278`; +60 more by `8acb255`) | attempt-2 lesson + post-attack repair log | **Wave and census arithmetic reproduces** (§ above). One blanket sentence is not covered — F6. |

## 4. Findings

### 4.0 Status board (committed state `8acb255`, 06:50:29Z; G24 addendum below)

| finding | first observed | status at close | why |
|---|---|---|---|
| F1a receipt ↔ bytes binding | G13 / live G17 | **CLOSED** | `c1-fixed.json` regenerated and re-regenerated: G23 = 23 cases / `332a5fe9…` / `fce5b84b…`; G24 = 24 cases / `d05b1e0c…` / `690153ad…`, each equal to the live file (`sha256sum`) |
| F1b bare-root class change | G17/G20 | **CLOSED by reversal** | final `resolve.py` keeps root-only bounty citations at `GONE` (comment + probe below) |
| F2 unit suite blind to the defect | G13 | **OPEN** | `test_resolve.py` untouched by all six commits; still `10 tests OK` on both fixed and baseline bytes |
| F3 `recheck:` cwd dependence | G13 | **CLOSED** | all three entries (and the new F07→S031 form) now begin `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 …` |
| F4 instruments README stale | G13 | **OPEN** | `git diff --stat 953c278 HEAD -- corpus/instruments/README.md` is empty |
| F5 open-record transcript gaps | G13 | **OPEN, wider** | transcript still has none of S018/S029/S030/S031; `opened-source-snapshots.json` has S018/S029/S030 but **no S031**, which is now F07's admitted authority |
| F6 bulk-reuse of contradicted reports | G13 | **OPEN** | reuse sentence unchanged; three of its reports' premises remain falsified by the landing |
| F7 refusal timestamp mislabelled | G13 | **OPEN** | `refusal-1.json` still `"at":"2026-10-25T03:34Z"` (local `-03`) |
| F8 dual sha authority unchecked | G13 | **OPEN, asymmetric** | S031 is pinned in `manifest.json` only; no open-record copy exists to disagree with |
| F9 a declared escape case was non-discriminating | G22 | **CLOSED** | `glob-expansion-escape` passed on the baseline at G22 and was redefined at G23 (see F9) |
| F10 superseded registry row still claims current use | G23 | **OPEN** | `SOURCES.md` S030 is `mined`, teaches "use current 4.2.0 requirements", and still lists the cna entry under `used-by` although that entry now sources S031 |

**G24 addendum (06:53:04Z, `HEAD`=`f6966d4`).** The ladder did not stop at `8acb255`: a
rescue commit `bf9ce02` and `f6966d4` took the matrix to **24 cases / 12 escapes**
(`matrix_sha256=d05b1e0c…`, resolver `690153ad…`), and the receipts were regenerated
again — baseline **0/12 escapes GONE**, landed **24/24**; a new escape case
`bounty-root-underscore-sibling` appears. Every **OPEN** finding in the board above was
re-checked against these newest bytes and is **unchanged**: `test_resolve.py` still
absent from `953c278..HEAD`; `instruments/README.md` still untouched; open records still
`['S018','S029','S030']` with an empty transcript; `refusal-1.json` still
`"at":"2026-10-25T03:34Z"`; SOURCES S030 still `mined` with the cna entry in `used-by`.
Bare-root citations are still **absent from all 24 cases**, so the G17/G20 class change
and its reversal remain unpinned by any fixture. F1/F3 and F9 stay closed.
Treat every number in this report as **state-pinned**; the primary sources are the
receipts and the commits, not this prose.

### F1 (high; **closed** by 2712c99/12edac4) — the C1 receipt was bound to bytes the tree no longer had, and a live delta was an unpinned classification change

**Status: both halves closed.** The binding half was repaired by regenerating the
receipts (final `c1-fixed.json`: 23 cases, `matrix_sha256=332a5fe9…`,
`resolver_sha256=fce5b84b…`, equal to the live file and to
`sha256sum corpus/instruments/mirror-containment-fixtures.json`). The class half was
repaired by reversal: the final `resolve.py` carries "Root-only bounty citations keep
their pre-r23 verdict" and my probe on `fce5b84b…` returns `GONE` for
`~/Projects/bounties`, `~/Projects/bounties/`, and `~/Projects/bounties//etc/hostname`
— identical to the committed `953c278` result. The body below is the record of the
window in which it was not closed, because the evidence was already being cited as
current while it drifted.

Original observation (G13):

`c1-fixed.json` records `"resolver": ".../corpus/instruments/resolve.py"` and
`"resolver_sha256": "ed9a9dae…40e9"`. That identifies the **committed** `953c278`
bytes and nothing later:

| state | resolver sha256 | matrix | receipt still identifies it? |
|---|---|---|---|
| committed `953c278` | `ed9a9dae…` | 13 cases / `5e61a33e…` | yes |
| live 06:40:53Z | `9e0b5751…` | 13 cases / `5e61a33e…` | **no** (resolver moved) |
| live 06:43:23Z | `8dd45bc8…` | **17 cases / `5c64e014…`**, checker `53742c8d…` | **no** (resolver, matrix and checker all moved) |

The lesson, `SCORECARD.md` C1 row and `LOG.md` all present `c1-fixed.json` as the
receipt for "the landed bytes". Under a literal reading it no longer identifies any
bytes in the working tree, and the matrix no longer matches the receipt's own
`matrix_sha256` either.

The delta is not cosmetic. `git diff HEAD -- corpus/instruments/resolve.py` (3 hunks):

- `bounty_suffix`: `return base[len(root) + 1:]` → `.lstrip("/")`
- bounty fallback: `exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)` → `exists_any(os.path.join(mirror_root, suffix) if suffix else mirror_root)`
- census: `max(...)` → `max((...), default=0)`

The second hunk changes a **published class**. Scratch probe, identical inputs, three
byte sets (`SKILL.md` citing three tokens; `HOME` and `KASEGI_MIRROR` are fixture
dirs, mirror present):

```
--- HEAD bytes (ed9a9dae…):   ~/Projects/bounties          GONE
                              ~/Projects/bounties/         GONE
--- live 06:40 (9e0b5751…):   ~/Projects/bounties          MIRROR-EQUIVALENT  <resolved>=<mirror root> literal bounty
                              ~/Projects/bounties/         MIRROR-EQUIVALENT  <resolved>=<mirror root> literal bounty
--- live 06:43 (8dd45bc8…):   ~/Projects/bounties          MIRROR-EQUIVALENT  <resolved>=<mirror root> literal bounty
                              ~/Projects/bounties/         MIRROR-EQUIVALENT  <resolved>=<mirror root> literal bounty
--- inherited bytes:          both GONE
```

Why this matters rather than being a tidy consistency fix:

1. **No fixture covers it — even after the live matrix grew to 17.** Neither the
   committed 13-case set nor the live 17-case set contains a bare-root citation.
   The four cases added live (`bounty-literal-present-traversal`,
   `bounty-literal-symlink-present`, `absolute-bounty-fallback-control`,
   `absolute-prefix-sibling-confusion`) cover literal-present carve-outs and the
   `/home/vgpnk/...` absolute prefix, not the exact-root suffix `""`. So neither the
   13/13 nor the 17/17 receipt certifies this path.
2. **It moves the numerator.** `SKILL.md` + `corpus/` contain **23** bare-root
   citations (`21 × \`~/Projects/bounties\``, `2 × \`~/Projects/bounties/\``), and
   `corpus/instruments/citation-survival.md:191` currently lists the bare root as
   GONE with 12 occurrences. On any host where the mirror exists, the live edit flips
   up to 23 distinct citations GONE → `MIRROR-EQUIVALENT`, i.e. into the
   availability numerator — the exact "availability growth without restoration"
   risk that `claims.json` C1 `after` disclaims.
3. **It contradicts the lane's own written state.** `SKILL.md:813` — "`~/Projects/bounties`
   is GONE — removed"; `corpus/knowledge/ev-model.md:5` repeats it.
4. **The no-harm guard cannot see it.** `mirror=0` on this host (disclosed in the
   lesson), so the frozen-corpus diff is vacuous by construction and cannot arbitrate
   a mirror-present class change.

The escape/control claim itself survives on every byte set I ran: committed bytes
**13/13**, live 06:40 bytes **13/13**, live 06:43 bytes **17/17 (escape 7/7,
controls 10/10)**, live 06:47 bytes **20/20**, and final `fce5b84b…` bytes
**23/23 (escape 11/11, controls 12/12, `matrix_sha256=332a5fe9…`, exit 0)** against a
baseline of **12/23 with 0/11 escapes GONE**. So the defect was *evidence binding and
unpinned scope*, never a false matrix result — and the bare-root decision was
ultimately made the other way (root-only stays `GONE`), which also restores
`SKILL.md:813`'s statement. Two things the closure did **not** do: add a bare-root
fixture (still none at 23 cases, so the decision remains unpinned and could flip again
silently) and wire the matrix into any test runner (F2).

### F2 (high) — the repo's own regression fixture is green on the inherited unsound bytes

`corpus/instruments/README.md:120` documents `python3 corpus/instruments/test_resolve.py`
as "the regression fixture". `test_resolve.py` was **not touched** by this attempt
(absent from the `8bf9807..953c278` name-status) and **still untouched at `8acb255`**
(`git log 953c278..HEAD --name-only` names no `test_resolve`), although the resolver it
tests gained two guards and the matrix grew to 23 cases. Running its copies in `/tmp`:

```
default (committed resolver):                 Ran 10 tests … OK   EXIT=0
KASEGI_RESOLVER_UNDER_TEST=<c1-baseline-resolver.py>  Ran 10 tests … OK   EXIT=0
```

The suite cannot distinguish the unsound inherited resolver from the fixed one: it
has no bounty-fallback escape case, no `bounties-x` sibling case, and no
relative-fallback escape case (its confinement tests use canonical-alias tokens,
`test_resolve.py:255–279`, which hit the branch that was already guarded). The only
detector for the C1 defect is the new standalone matrix, and nothing wires it into a
test runner or CI (`grep -rn "mirror-containment-check"` hits only
`mirror-containment-check.py`, `corpus/lessons/round-23.md:111,114`, and the wave
specs). Consequence: a future edit that deletes `bounty_suffix()`'s boundary or either
`under_mirror()` call leaves `test_resolve.py` green. R7 asks that instrument claims
change and exercise the actual detector; the unit fixture still does not exercise it.

### F3 (medium; **closed** at `8acb255`) — the committed entry `recheck:` lines were not verbatim-executable outside the lane root

**Status: closed.** All four entry `recheck:` lines (F06, F07→S031, F08) now begin
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 …` at `HEAD`, so the
command is cwd-independent. The defect below held for `953c278` only.

The committed (`953c278`) `recheck:` fields were:
`recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0NN`.
Executed verbatim from `/tmp`:

```
$ sh -c 'python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018'
python3: can't open file '/tmp/corpus/instruments/source-recheck.py': [Errno 2] No such file or directory
EXIT=2
```

Q7's predicate is "contains a command … executable", and the exit integer 2 is also
the tool's legitimate `UNAVAILABLE` code — so the committed form is indistinguishable
from a fail-closed `UNAVAILABLE` for a verifier who is not already standing in the lane
root. The live worktree has begun repairing this (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 …`
in all three entries, uncommitted at 06:41Z); the committed bytes still carry the
defect, and no receipt records the fix.

### F4 (medium; **OPEN at `8acb255`**) — `corpus/instruments/README.md` documents the pre-fix classifier as current

Unchanged since the checkpoint, and now wrong about the code it indexes:

- `README.md:105`: "Bounty, relative and other-root classification is **untouched**; the four classes remain …" — the whole point of the landed change is that bounty and relative classification moved.
- `README.md:107–110`: "**Realpath confinement.** Newly mapped **explicit** hits must stay under the realpath of `mirror_root`" — confinement is now applied to the bounty and relative fallbacks too, and the exact-root bounty boundary (`bounty_suffix`) is documented nowhere.
- `README.md:11` still summarises `resolve.py` with no mention of confinement at all.

This is the instrument's own index page, not a historical round note, so it is
presented as current documentation. The lesson records the code change but no
doc-update, and `git diff --stat 953c278 HEAD -- corpus/instruments/README.md` is
still empty after all four post-audit commits: the file has not moved since the
checkpoint.

### F5 (medium; **OPEN and wider at `8acb255`**) — the wave's open records do not cover the authorities it admits

`.ufo/waves/round-23/source-open-transcript.json` (unchanged through all four
commits) contains `S001`–`S015` only. Counts for the rows the lesson's Gate says were
"opened this round", re-measured at close:

```
S018 in transcript: 0    S022: 0    S024: 0    S028: 0    S029: 0    S030: 0    S031: 0
opened-source-snapshots.json ids: ['S018', 'S029', 'S030']        # no S031
manifest.json ids:               ['S018', 'S029', 'S030', 'S031']
```

The opens are instead asserted by a *different* inherited file,
`opened-source-snapshots.json` (S018/S029/S030, `"opened": "2026-10-20"`). Since
`2712c99`, **F07's admitted authority is `S031`, which appears in the manifest but in
neither open record** — no open date, no URL, no byte pin, no transcript line. S028
(rejected) likewise has no open record at all; only its `SOURCES.md` `where` cell
claims it was opened. The transcript is not marked partial or superseded, and the
lesson cites the wave directory as the open record. C2's criterion ("only after
official text opens") is therefore backed for three rows by a file whose sibling
transcript denies covering them, self-asserted for the fourth, and — for the source
F07 now rests on — backed by the *manifest alone*, which is a byte pin, not an open.

### F6 (low) — the bulk reuse statement covers reports whose premises the tree now contradicts

`corpus/lessons/round-23.md:81–82` reuses "the 44 inherited seat reports under
`.ufo/waves/round-23/build/` (author-side evidence, never admission)" wholesale as
"reused after re-verification". The 44 count is exact (`ls build/*.md | wc -l` → 44)
and wave-1's registry does have 64 members, of which exactly 20 have no report. But
at least three of those reused reports rest on premises the landing falsifies, with no
supersession marker in the reuse sentence:

- `build/Q1Executable.md` #4 — "`corpus/source-snapshots/round-23/` contains … but **no manifest.json** … exit=2". Manifest now present; rechecks exit 0.
- `build/CoverageDenom.md` Finding 1 — "**neither** `source-recheck.py` **nor** `manifest.json` exists in the tree". Both exist at the checkpoint already (`source-recheck.py`) / now (`manifest.json`).
- `build/RecheckSources.md` — "No … `--selftest` run was performed" for the tool that is now the C2 evidence.

The same lesson's M11 records the manifest minting, so a careful reader can reconcile
them; the reuse sentence itself does not, and the reports remain unmarked in the tree
as the current author-side record of wave 1.

### F7 (low) — `falsify/refusal-1.json`'s `at` field is local time labelled `Z`

```
refusal-1.json                 "at":"2026-10-25T03:34Z"
falsify/swarm-registry.json    "createdAt":"2026-10-25T06:33:42.832Z"
host                           03:33:42 -0300 = 06:33:42 UTC  (date; date -u)
```

Read literally, the refusal is stamped **3 hours before** the registry of the wave it
refused was created. The registry's timestamp is correct UTC; the refusal's is local
`-03` time carrying a `Z` suffix. Wave-conformance evidence for "refused at dispatch"
should not carry a timestamp that inverts the ordering.

### F8 (low; **OPEN, now asymmetric**) — two sha256 authorities, one of which no longer covers the admitted set

`opened-source-snapshots.json` and `manifest.json` each pin `sha256` for
`S018/S029/S030.txt`. They **agree today** (d366bf…, 825144…, 673526…), and
`source-recheck.py` has **no reference to `opened-source-snapshots`** (grep → "NO
reference"), so nothing enforces the agreement. Since `2712c99` the manifest also pins
**S031**, which the other file does not carry at all — the two authorities now cover
different sets, and the newer one is the only pin for F07's authority. `build/Q1Executable.md`
#6 named this class; the landing extended the second authority without a cross-check or
a set-equality assertion.

### F9 (low; **CLOSED at G23**) — a declared escape case was non-discriminating for one generation

At generation **G22** (22 cases, `matrix_sha256=158a423c…`, resolver `fce5b84b…`) the
regenerated do-nothing receipt recorded:

```
c1-baseline.json: cases 22  escape 10  fail 9  pass 13
  PASS  escape  glob-expansion-escape  GONE -> GONE
```

i.e. one of the ten declared escape fixtures **already classified GONE on the
inherited bytes**, so it could not testify to the fix — the counter would have shown
"escape 9/10" and still reported the matrix as exercising ten escapes. At G23 the case
was redefined (`~/Projects/bounties/<name>/../../outside-vault/x.md:1`) and now fails
on the baseline (`0/11`), so the class is closed. The record matters because the
SCORECARD errata describes only the two *added* cases as mutation-driven; the
non-discriminating state itself existed in a committed-then-replaced receipt and is
visible only by comparing the two generations.

### F10 (medium; **OPEN at `8acb255`**) — a superseded registry row still claims current use

`corpus/SOURCES.md` rows S030 and S031 (abbreviated to the load-bearing cells; status and `used-by` are the last two columns):

```
| S030 | … CNA Operational Rules v4.2.0 … | spec | A | … version 4.2.0 | … | supersedes S022 — use current 4.2.0 requirements and section numbering; … | mined | … | corpus/knowledge/cna-assignment-and-vulnerability-rules.md |
| S031 | … CNA Operational Rules v4.2.6 … | spec | A | … current version 4.2.6 | … | supersedes S030 — current 4.2.6 makes independent-fixability ID separation a MUST; S030's 4.2.0 SHOULD is historical. | mined | … | corpus/knowledge/cna-assignment-and-vulnerability-rules.md |
```

Both rows are `mined` and both claim `used-by` the same entry, while that entry's
`source:` is **S031 only**. So S030 simultaneously (a) tells a reader to "use current
4.2.0 requirements", (b) is declared historical by S031's own cell, and (c) claims a
`used-by` relation the entry does not have. `corpus/lessons/round-23.md:252` states
the intent — "S030/S022 kept as historical rows" — and the SCORECARD errata corrects
the *entry and README* cells, but the registry row itself was not updated and no
old→new status/`used-by` change is logged (R8 requires exactly that log). Census at
close: 31 rows, tier `A=29 C=2`, status `mined 19 / queued 9 / rejected 3`, `used-by`
non-empty on 19 — the two extra `mined`/`used-by` counts relative to `953c278`
(30 / 28 / 18) are S031 plus this double-attribution.

## 5. Confirmed-as-sound (so the next seat does not re-derive it)

- **Matrix reproducibility and control validity (final generation).** At `8acb255` the
  receipts match the tree: 23 cases, `matrix_sha256=332a5fe9…` = `sha256sum` of the
  fixtures file; `c1-fixed.json` 23/23 with `resolver_sha256=fce5b84b…` = the live
  file; `c1-baseline.json` 12/23 with **0/11** escapes GONE and controls 12/12. My
  independent runs reproduced G13 (13/13), G17 (17/17), G20 (20/20) and G23 (23/23),
  and the inherited baseline (7/13 at G13; 12/23 at G23).
- **The C1 fix itself.** All eleven declared escapes are GONE on the final bytes; all
  twelve controls keep their pinned class; the baseline fails every escape. The
  confinement is real, not a blanket ban, and the two carve-outs (lane-relative
  `INTERNAL`, bounty literal hit) are pinned as controls and named in the docstring.
- **Quote pins (final).** 32/32 manifest quotes are literal substrings across four
  snapshots; per-entry checks give F06 6/6 against S018, F08 8/8 against S029, and F07
  7/8 against S031 — the single non-literal string is `4.2.0 is the current CNA rule
  set.`, which sits in F07's **Rejected** block as the rejected claim, so it is
  correctly absent from the source. Max quote length 20 words (Q3's ≤25).
- **C2 counters and rechecks (final).** 3/3 and 8/8 as claimed; four rechecks exit 0
  (`S018` 7 lines, `S029` 10, `S030` 8, `S031` 11 — digest+quotes each); SOURCES
  census reproduces the 31/29/2/19 numbers above; `mirror=0` vacuity disclosed.
- **F07's currentness correction is real and material.** `S031.txt` is a 49,350-byte
  normalized capture whose 10 assertions all verify, and the entry now records that
  4.2.6 turns independent-fixability ID separation into a MUST where 4.2.0 said SHOULD.
  The inherited F07 admitted on 4.2.0 was out of date on the day it was opened.
- **Entry headers.** All three entries carry the Q1 triad (`source:`, `verified-at: 2026-10-20`,
  `recheck:`) directly under the H1 — the working tree did not need to add them; my
  earlier suspicion that they were missing was a grep-pattern artefact, corrected here.
- **Live sibling disclosures are true.** `S029.txt:20` is the Article 14(4)(a) early
  warning and the 24-hour phrase occurs twice (lines 10 and 20); `S018.txt` starts at
  `## Definitions`, contains no "Spring 2020", and ends at the `Use coordinators` lead
  line; `S029.txt` contains no `20.11.2024`.

## 6. Reproduction

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git log --format='%h %s' 953c278..HEAD          # four post-audit commits, HEAD 8acb255
git diff --numstat 953c278 HEAD -- corpus/ SCORECARD.md LOG.md
git diff --numstat 8bf9807 HEAD -- corpus/knowledge/multiparty-vulnerability-coordination.md \
  corpus/knowledge/cna-assignment-and-vulnerability-rules.md \
  corpus/knowledge/cra-manufacturer-reporting-duties.md corpus/SOURCES.md \
  corpus/source-snapshots/round-23 corpus/instruments/source-recheck.py .ufo/waves/round-23
git show 8bf9807:corpus/instruments/resolve.py > /tmp/kasegi-r23-falsify-inherited/inherit_resolve.py
diff /tmp/kasegi-r23-falsify-inherited/inherit_resolve.py .ufo/waves/round-23/c1-baseline-resolver.py   # empty
# pin the state first: the tree changed five matrix generations during this audit
git status --porcelain=v1; sha256sum corpus/instruments/{resolve.py,mirror-containment-fixtures.json}
python3 corpus/instruments/mirror-containment-check.py --json /tmp/…/rerun-fixed.json                   # 23/23 exit 0
python3 corpus/instruments/mirror-containment-check.py \
  --resolver .ufo/waves/round-23/c1-baseline-resolver.py --json /tmp/…/rerun-baseline.json              # 12/23, escape 0/11, exit 1
for s in S018 S029 S030 S031; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source $s; done                            # exit 0 ×4, 7/10/8/11 lines
cp corpus/instruments/*.py /tmp/kasegi-r23-falsify-inherited/instr2/   # run tests on copies only
cd /tmp/kasegi-r23-falsify-inherited/instr2 && python3 test_resolve.py                                   # 10 tests OK
KASEGI_RESOLVER_UNDER_TEST=baseline.py python3 test_resolve.py                                           # 10 tests OK  ← F2, still open
sh -c 'python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018'  # from /tmp: EXIT=2 on 953c278 text; fixed at HEAD  ← F3
sha256sum corpus/instruments/resolve.py   # ed9a9dae… 06:37Z; 9e0b5751… 06:40Z; 8dd45bc8… 06:43Z; fce5b84b… 06:47Z onward  ← F1
```

Per-doc quote check and the bare-root probe are in
`/tmp/kasegi-r23-falsify-inherited/{docquotes.py,docquotes2.py}` and the `rootcase/` +
`run-{head,inherit,live,live43,final,close}/` fixtures (`SKILL.md` cites
`~/Projects/bounties`, `~/Projects/bounties/`, `~/Projects/bounties//etc/hostname`;
`HOME` and `KASEGI_MIRROR` are fixture dirs so the mirror is present). The bare-root
probe is the only way to see the G17/G20 class change and its reversal; **no matrix
generation — 13, 17, 20, 22 or 23 cases — contains a bare-root citation**.

## 7. Scope limits and confidence

- **Confidence: high** for every hash/timestamp/class divergence above (F1's ladder,
  the bare-root probe and its reversal, F2's identical `10 tests OK` on both byte sets,
  F3's `/tmp` exit 2 on the `953c278` text, F4's untouched README, F5's zero counts and
  the missing S031 open record, F7's timestamps, F9's two-generation receipt pair,
  F10's S030 row) — each is a direct command output quoted in place.
- **Confidence: medium** for F6's severity: whether a bulk reuse sentence must carry
  per-report supersession is a documentation-policy call, not a mechanical fact; the
  premise contradictions themselves are mechanical.
- **Not assessed:** `test_resolve.py` behaviour beyond the two byte sets (the suite is
  byte-blind to the relevant branch, so it says nothing about either guard);
  `anchorcheck.py` over the entries' line-anchored claims; `SCORECARD.md`'s score
  semantics beyond its C1/C2 evidence pointers; whether the mid-audit uncommitted
  edits and the four commits were L1's integration or seat work (authorship is not
  observable from the tree, and this seat made no production edit).
- **Concurrency caveat:** the tree moved continuously during this audit — **four
  commits** (`2712c99`, `4d9231e`, `12edac4`, `8acb255`) and **five matrix
  generations** (13→17→20→22→23 cases) between 06:36Z and 06:50Z. §2a–2b pins each
  state; §4.0 states which finding survives at `8acb255`. A reader must re-pin before
  using any number here: F1 and F3 are closed *by later bytes*, not by the bytes they
  were found on. All scratch used by this seat is `/tmp/kasegi-r23-falsify-inherited/`
  (not `.ufo/waves/*/scratch/`); no production file, index, or lane tree was modified
  by this seat.
- **No installs or updates** were performed (no pacman, uv, cargo, or npm), so the
  tooling-record requirement is vacuous. No network access, no credential operation,
  no live-target traffic; only local authorized fixtures under `/tmp`.
- This seat makes no admission call and claims no score movement.
