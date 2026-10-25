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
| lane tip | `HEAD` = `953c278` |
| audit wall clock | 2026-10-25 06:36–06:44 **UTC** (03:36–03:44 local, host TZ `-03`) |
| `8bf9807`→`HEAD` diff for assigned paths | `9 files changed, 1618 insertions(+), 1 deletion(-)` |
| scratch | `/tmp/kasegi-r23-falsify-inherited/` |

Three distinct states of the C1 bytes exist and must not be conflated:
**(a) committed `953c278`** — resolver `ed9a9dae…`, 13-case matrix `5e61a33e…`;
**(b) live at 06:40Z** — resolver `9e0b5751…`, same 13-case matrix;
**(c) live at 06:43Z (close of audit)** — resolver `8dd45bc8…`, 17-case matrix
`5c64e014…`, changed `mirror-containment-check.py` `53742c8d…`. The C1 receipt
`c1-fixed.json` pins (a) only.

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

**Explicitly unchanged since the checkpoint** (so nothing in them was repaired):
`corpus/knowledge/multiparty-vulnerability-coordination.md`,
`corpus/SOURCES.md`, `corpus/instruments/source-recheck.py`,
`corpus/source-snapshots/round-23/{S018,S029,S030}.txt`,
`.ufo/waves/round-23/{claims.json,before-instruments.json,opened-source-snapshots.json,source-open-transcript.json,build/**}`.

Cited-by files changed at `HEAD` but outside the assigned path list (evidence is
presented through them, so they are in scope as *presentation*): `corpus/README.md`
(3/3, the F06–F08 flip), `corpus/lessons/round-23.md` (167/0, attempt-2 section),
`SCORECARD.md` (34/0, round-23 result row).

### 2a. Uncommitted drift observed *during* this audit

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
| `.ufo/waves/round-23/c1-fixed.json` (new) | escape 6/6, controls 7/7, 13/13 | **Matched the bytes it pinned — and is now stale** (§4, F1). |
| `corpus/source-snapshots/round-23/manifest.json` (new, +46) | 19 quote assertions + 3 digests | **All 19 quotes are literal substrings** (`TOTAL quotes 19 MISSES 0`); the three digests equal `sha256sum` of the `.txt` files; `source-recheck.py` exits 0 for S018/S029/S030 with the claimed line counts (7/7/8). This repairs the inherited "recheck exits 2" defect. |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` (1/1) | Article 71 quote corrected | **Repairs a genuine misquote.** Inherited row (`git show 8bf9807:…:50`) quoted “It shall apply from 11 December 2027.”; `grep -c` of that string in `S029.txt` = **0**, of “This Regulation shall apply from 11 December 2027.” = **1**. The repaired entry quote is now an exact substring. |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` (+5) | Quote-fidelity note for `4.1.9` `<u>` markup | **Accurate disclosure, not a quote correction.** `S030.txt:165` carries `are <u>Independently Fixable</u>`; the entry table quotes the rendered form, which is *not* a substring (`OUT` in my per-doc check). The note states exactly this and points at the manifest, which asserts the literal bytes. Consistent, and the divergence is markup only. |
| `.ufo/waves/round-23/falsify-spec.json`, `falsify/refusal-1.json`, `falsify/swarm-registry.json` (new) | 36-seat wave, refused at dispatch, no replacement | **Counts check out.** `falsify-spec.json` items = 36, `maxLanes` 64; registry members = 36 with role tally `critic 9, reviewer 7, executor 7, scout 4, mutation-tester 3, sentinel 2, revenger 2, connector 1, scribe 1` — identical to the lesson's prose. `refusal-1.json` records `refused:true`, `seats:36`, job-limit error. |
| `corpus/knowledge/multiparty-vulnerability-coordination.md` | **unchanged** | Nothing repaired — F06 rests entirely on inherited bytes. My check: all **6** quoted sentences are literal substrings of `S018.txt`; no defect found in the entry's quotes. |
| `corpus/SOURCES.md`, `source-recheck.py`, `S018/S029/S030.txt` | **unchanged** | Registry census reproduces the lesson exactly: 30 rows, tier `A=28 C=2`, status `mined 18 / queued 9 / rejected 3`, `used-by` non-empty on 18; S029 "supersedes S024", S030 "supersedes S022". |
| `corpus/README.md` (3/3) | F06–F08 queued→admitted | **Reproduces:** `grep -cE '^\| F0[6-8] .*\| admitted \|'` → **3**; `grep -cE '^\| F0[1-8] .*\| admitted \|'` → **8**; each `entry` path exists. |
| `corpus/lessons/round-23.md` (167/0) | attempt-2 lesson | **Wave and census arithmetic reproduces** (§ above). One blanket sentence is not covered — F6. |

## 4. Findings

### F1 (high, falsifiable) — the C1 receipt is bound to bytes the tree no longer has, and the live delta is an unpinned classification change

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
controls 10/10, exit 0, `matrix_sha256=5c64e014…`)**. So the defect is *evidence
binding and unpinned scope*, not a false matrix result. Minimal closure: either revert
the ternary hunk before commit, or add a bare-root fixture (pin whichever class is
intended), regenerate `c1-fixed.json` against the final resolver+matrix pair, and
record the GONE→MIRROR-EQUIVALENT decision against the 23 citations. Do not rely on
either live receipt until it is regenerated after the tree stops moving.

### F2 (high) — the repo's own regression fixture is green on the inherited unsound bytes

`corpus/instruments/README.md:120` documents `python3 corpus/instruments/test_resolve.py`
as "the regression fixture". `test_resolve.py` was **not touched** by this attempt
(absent from the `8bf9807..HEAD` name-status). Running its copies in `/tmp`:

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

### F3 (medium) — the committed entry `recheck:` lines are not verbatim-executable outside the lane root

The committed (`953c278`) `recheck:` fields are:
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

### F4 (medium) — `corpus/instruments/README.md` documents the pre-fix classifier as current

Unchanged since the checkpoint, and now wrong about the code it indexes:

- `README.md:105`: "Bounty, relative and other-root classification is **untouched**; the four classes remain …" — the whole point of the landed change is that bounty and relative classification moved.
- `README.md:107–110`: "**Realpath confinement.** Newly mapped **explicit** hits must stay under the realpath of `mirror_root`" — confinement is now applied to the bounty and relative fallbacks too, and the exact-root bounty boundary (`bounty_suffix`) is documented nowhere.
- `README.md:11` still summarises `resolve.py` with no mention of confinement at all.

This is the instrument's own index page, not a historical round note, so it is
presented as current documentation. `corpus/lessons/round-23.md` records the code
change but no doc-update, and the file is absent from the change set.

### F5 (medium) — the wave's "source-open transcript" contains none of the round's opens

`.ufo/waves/round-23/source-open-transcript.json` (unchanged) contains `S001`–`S015`
only. Counts for the rows the lesson's Gate says were "opened this round":

```
S018 in transcript: 0    S022: 0    S024: 0    S028: 0    S029: 0    S030: 0
```

The opens are instead asserted by a *different* inherited file,
`opened-source-snapshots.json` (S018/S029/S030, `"opened": "2026-10-20"`), and for
**S028 there is no open record at all** (not in the transcript, not in
`opened-source-snapshots.json`; only the `SOURCES.md` row's own `where` cell claims
it was opened). The transcript is not marked as partial or superseded, and the lesson
cites the wave directory as the open record. C2's admission criterion ("only after
official text opens") is therefore backed, for three rows, by a file whose sibling
transcript denies covering them — and for the fourth by self-assertion only.

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

### F8 (low) — two sha256 authorities over the same snapshots, still unchecked

`opened-source-snapshots.json` and `manifest.json` each pin `sha256` for
`S018/S029/S030.txt`. They **agree today** (d366bf…, 825144…, 673526…), and
`source-recheck.py` has **no reference to `opened-source-snapshots`** (grep → "NO
reference"), so nothing enforces the agreement. `build/Q1Executable.md` #6 named this
class; the landing minted the second authority without a cross-check. Not currently a
divergence — a latent one.

## 5. Confirmed-as-sound (so the next seat does not re-derive it)

- **Matrix reproducibility and control validity.** Committed `c1-baseline.json` and
  `c1-fixed.json` reproduce case-for-case on independent runs of the committed
  resolver+matrix pair; the baseline is byte-identical to the checkpoint resolver;
  `matrix_sha256` equals the fixtures' digest in all receipts. The live 17-case
  expansion also passes on the live resolver (17/17, exit 0) — but see F1: that run is
  not the receipt of record and pins no bare-root case.
- **The C1 fix itself.** All six declared escapes (seven in the live matrix) are GONE
  on committed and live bytes; all controls keep their pinned class. The confinement is
  real, not a blanket ban.
- **Quote pins.** 19/19 manifest quotes are literal substrings; per-entry checks give
  F06 6/6, F08 6/6, F07 6/7 exact with the one disclosed markup case; max quote length 20 words (Q3's ≤25).
- **C2 counters.** 3/3 and 8/8 as claimed; SOURCES census (30 rows, A=28/C=2,
  mined 18/queued 9/rejected 3, used-by 18) as claimed; `mirror=0` vacuity disclosed.
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
git diff --numstat 8bf9807 HEAD -- corpus/knowledge/multiparty-vulnerability-coordination.md \
  corpus/knowledge/cna-assignment-and-vulnerability-rules.md \
  corpus/knowledge/cra-manufacturer-reporting-duties.md corpus/SOURCES.md \
  corpus/source-snapshots/round-23 corpus/instruments/source-recheck.py .ufo/waves/round-23
git show 8bf9807:corpus/instruments/resolve.py > /tmp/kasegi-r23-falsify-inherited/inherit_resolve.py
diff /tmp/kasegi-r23-falsify-inherited/inherit_resolve.py .ufo/waves/round-23/c1-baseline-resolver.py   # empty
# pin the live state first; these bytes moved 3× during the audit
git status --porcelain=v1; git diff --stat HEAD -- corpus/instruments/; sha256sum corpus/instruments/resolve.py
git stash list >/dev/null   # not used: no tree mutation by this seat
python3 corpus/instruments/mirror-containment-check.py --json /tmp/…/rerun-fixed.json                   # 13/13 exit 0 on committed pair
python3 corpus/instruments/mirror-containment-check.py \
  --resolver .ufo/waves/round-23/c1-baseline-resolver.py --json /tmp/…/rerun-baseline.json              # 7/13 exit 1
for s in S018 S029 S030; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source $s; done                            # exit 0 ×3, 7/7/8 lines
cp corpus/instruments/*.py /tmp/kasegi-r23-falsify-inherited/instr/   # run tests on copies only
cd /tmp/kasegi-r23-falsify-inherited/instr && python3 test_resolve.py                                    # 10 tests OK
KASEGI_RESOLVER_UNDER_TEST=baseline.py python3 test_resolve.py                                           # 10 tests OK  ← F2
sh -c 'python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018'  # from /tmp: EXIT=2  ← F3
sha256sum corpus/instruments/resolve.py   # ed9a9dae… == c1-fixed.json at 06:37Z; 9e0b5751… 06:40Z; 8dd45bc8… 06:43Z  ← F1
```

Per-doc quote check and the bare-root probe are in
`/tmp/kasegi-r23-falsify-inherited/docquotes.py` and the `rootcase/` + `run-{head,inherit,live,live43}/`
fixtures (`SKILL.md` cites `~/Projects/bounties`, `~/Projects/bounties/`,
`~/Projects/bounties//etc/hostname`; `HOME` and `KASEGI_MIRROR` are fixture dirs so the
mirror is present). The bare-root probe is the only way to see F1's class change; the
committed 13-case and live 17-case matrices both omit that citation.

## 7. Scope limits and confidence

- **Confidence: high** for F1's hash divergence, the bare-root probe, the unit-suite
  blindness (F2), the `/tmp` verbatim failure (F3), F4's README lines, F5's zero
  counts, F7's timestamps, and every "confirmed-as-sound" item — each is a direct
  command output above.
- **Confidence: medium** for F6's severity: whether a bulk reuse sentence must carry
  per-report supersession is a documentation-policy call, not a mechanical fact; the
  premise contradictions themselves are mechanical.
- **Not assessed:** `corpus/instruments/test_resolve.py` behaviour under the *live*
  bytes beyond the matrix (the unit suite is byte-blind to the relevant branch, so it
  tells nothing either way about the F1 ternary change); `anchorcheck.py` over the
  three entries' line-anchored claims; whether the uncommitted edits were L1's or a
  seat's; `SCORECARD.md`'s score semantics beyond reading its C1/C2 evidence pointers.
- **Concurrency caveat:** the tree moved during the audit — three distinct resolver
  hashes and two matrix configurations were observed between 06:36Z and 06:43Z
  (§2a). Everything in §2a, and F1's "live" half, describes those snapshots and must
  be re-pinned before any admission decision. All scratch used by this seat is
  `/tmp/kasegi-r23-falsify-inherited/` (not `.ufo/waves/*/scratch/`); no production
  file, index, or lane tree was modified by this seat.
- **No installs or updates** were performed (no pacman, uv, cargo, or npm), so the
  tooling-record requirement is vacuous. No network access, no credential operation,
  no live-target traffic; only local authorized fixtures under `/tmp`.
- This seat makes no admission call and claims no score movement.
