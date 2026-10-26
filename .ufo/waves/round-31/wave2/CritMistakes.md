# CritMistakes — attack on the round-31 mistake-mining (wave 2)

Seat `CritMistakes` (leaf; no delegation, no background jobs, no swarm). Round kasegi-shokunin 31, wave 2.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`.
Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (runtime route table; this seat passed no model).
Tools installed or upgraded: **none** (no pacman transaction — host-wide pause respected; no uv/npx/binary download).
Writes: this receipt only. All attack work ran in `tempfile.mkdtemp` scratch roots (`/tmp/critmist-_b_q2tmu`,
`/tmp/critmistB-xxpv89ho`, `/tmp/critmistC-hijtypqh`, plus one `/tmp/critmist-…` from a cell that failed on its own regex
translation and wrote nothing into the lane); all four deleted at exit (`ls -d /tmp/critmist-* /tmp/critmistB-* /tmp/critmistC-*`
after deletion → `No such file or directory`).
No git/jj mutation: read-only `git show`, `git status --porcelain`, `git -C . rev-parse` only. No network fetch.

## 0. Bottom line

| Item | Verdict |
|---|---|
| (1) M31-1 fix "shown able to fail" | **Reproduced for the three states the item names** (base copy → exit 1, current → exit 0, erratum block deleted → exit 1). The claim holds as stated, **but the able-to-fail demonstration covers only erratum-removal**: two other mutants are green on this check (§2, §3), and the erratum's own cited output is superseded on landed bytes (§4). |
| (2) wave-1 sweep for `BLOCKED`/`DEFECT`/`survivor`/`FAIL`/`traceback`/`PRE-STATE` | Six mistake classes the wave hit are **absent** from `ScribeGateDraft.md`'s M31 list (O1-O6, §5.1), one of them the round's central C1 event. No hidden hard `BLOCKED:` exists. |
| (3) `QUALITY.md` R16/R17 | R17 carries an executable able-to-fail check and its cites resolve. **R16 carries no runnable check in the corpus, its criterion contradicts its only specimen, and both rows cite `corpus/lessons/round-31.md` — a file that does not exist in the tree** (§6). |

## 1. Quiescence of the subjects measured here

```
$ sha256sum SCORECARD.md LOG.md corpus/QUALITY.md corpus/instruments/recheck-audit.py \
            corpus/instruments/source-recheck.py corpus/instruments/frontier-recheck-count.py
5fa41aef7c8e795e0fb2efac8989ca5df1727aa35cb8b3da079e329b5e660dc7  SCORECARD.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
96b71caad96979b42422bd7dfc362c94913d54ffc63d2cf2dc0aac62ef2e6b2d  corpus/QUALITY.md
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
```

Each digest was recomputed after the last measurement of the corresponding block; every pair was equal. `SCORECARD.md`
and `LOG.md` are byte-identical to the wave-1 after receipts (`5fa41aef…`, `864deb7d…`), so §2/§3 compare like with like
(bound 6). `corpus/QUALITY.md` is byte-identical to the wave-1 digest cited by `ScribeGateDraft.md` (`96b71caa…`).
`recheck-audit.py` is **not** at the base digest (`3fc0d751…`): the C1 limb work changed it to `5d4842da…`, which is the
trigger condition the SCORECARD erratum itself names (§4).

## 2. Item (1) — re-run of `ExecErratumCheck`'s CHECK A, verbatim

The shipped check was copied out of `.ufo/waves/round-31/wave1/ExecErratumCheck.md` §1 unchanged, into
`$D/checkA.sh`, and run as `bash $D/checkA.sh <file>`; the script `cd`s to the lane root itself, so the argument is the
file under test and a `/tmp` copy is admissible:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
f=${1:-SCORECARD.md}
n=$(grep -c 'recheck-audit open item' "$f")
l=$(grep -nE '(([Rr]31)|([Rr]ound[- ]31))[[:space:]]+[Ee]rrata?' "$f" | head -1 | cut -d: -f1)
c=0
if [ -n "$l" ] && tail -n +"$l" "$f" | grep -q 'recheck-audit open item' \
   && tail -n +"$l" "$f" | grep -q 'strict pass=43/43'; then c=1; fi
printf 'file=%s stale_paragraphs=%s erratum_anchor=%s names_item_and_cites_corrected_audit=%s\n' "$f" "$n" "${l:-none}" "$c"
if [ "$n" -eq 0 ] || [ "$c" -eq 1 ]; then echo "erratum_closure=closed"; exit 0; else echo "erratum_closure=open"; exit 1; fi
```

`git show b374febb…:SCORECARD.md > $D/sc-base.md` → 80608 B, `sha256 cac64dbd…` — the same digest the red-before receipt
records, so the "copy from base" is the right blob.

```
=== BASE-b374febb exit=1
file=/tmp/critmist-_b_q2tmu/sc-base.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
=== CURRENT exit=0
file=/home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1
erratum_closure=closed
=== MUT2-erratum-block(837-EOF)-deleted exit=1
file=/tmp/critmist-_b_q2tmu/mut-block-deleted.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=open
```

All three states the item names reproduce exactly, and they match the filed receipts line for line —
`ExecErratumCheck-before.txt:45-46` (`erratum_closure=open` / `EXIT CODE: 1`), `ExecErratumCheck-after.txt:30-31`
(`closed` / `EXIT CODE: 0`), `ExecErratumCheck-after.txt:62-64` (mutant `open`). Two further mutants were run because
"deleting the erratum line" is ambiguous:

```
=== MUT1-erratum-heading-line-only-deleted (line 837 removed) exit=0
file=/tmp/critmist-_b_q2tmu/mut-anchor-deleted.md stale_paragraphs=2 erratum_anchor=838 names_item_and_cites_corrected_audit=1
erratum_closure=closed
=== MUT3-strict-pass-43/43-line-deleted exit=1
file=/tmp/critmist-_b_q2tmu/mut-strict-line-deleted.md stale_paragraphs=1 erratum_anchor=837 names_item_and_cites_corrected_audit=0
erratum_closure=open
```

The anchor search finds a **second** anchor on `SCORECARD.md:839` (`r31 erratum: the paragraph …`), so removing the
heading alone cannot fail the check; only removing the block (or the literal) can. That is consistent with the check's
documented shape, not a defect by itself.

### 2.1 Able-to-fail hole H1 — the check is green when the stale paragraph is deleted

```
=== BASE-with-filed-paragraph-(813-819)-DELETED, no erratum anywhere exit=0
file=/tmp/critmistC-hijtypqh/sc-base-para-deleted.md stale_paragraphs=0 erratum_anchor=none names_item_and_cites_corrected_audit=0
erratum_closure=closed
=== CURRENT-with-filed-paragraph-(813-819)-DELETED, erratum intact exit=0
file=/tmp/critmistC-hijtypqh/sc-cur-para-deleted.md stale_paragraphs=1 erratum_anchor=830 names_item_and_cites_corrected_audit=1
erratum_closure=closed
```

The first case is decisive: **base bytes minus the stale paragraph, with no erratum at all, read `erratum_closure=closed`
and exit 0**, because the shipped condition is `[ "$n" -eq 0 ] || [ "$c" -eq 1 ]`. R16's own sentence forbids exactly
this: "a check that turns green because the stale sentence was reworded or deleted has closed nothing"
(`corpus/QUALITY.md:95`). Note the disclosure state, because it changes the size of the finding: **the hole is already
recorded inside R16's row** — "Limit measured here: on the base bytes reworded once with no erratum the same check printed
`erratum_closure=closed` and exited 0 (`stale_paragraphs=0`), so only the naming-erratum branch is closure under this
criterion" — so the wave *measured* it. What it did not do is list it as a mistake, or change the check. Consequence:
`ExecErratumCheck.md` §R-1 and R16 both register a criterion that **no shipped specimen satisfies**.

## 3. Item (1) continued — CHECK B, same shape, a second hole

CHECK B copied out of `ExecErratumCheck.md` §2 unchanged (`bash $D/checkB.sh <file>`):

```
=== BASE-b374febb exit=1
file=/tmp/critmistB-xxpv89ho/log-base.md round30_h2_headings=0 round30_h2_or_h3_headings=0
log_closure=open
=== CURRENT exit=0
file=/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md round30_h2_headings=1 round30_h2_or_h3_headings=2
log_closure=closed
=== MUT-h2-entry-body-deleted_keep-h3 exit=0
file=/tmp/critmistB-xxpv89ho/mut-h2body-deleted.md round30_h2_headings=0 round30_h2_or_h3_headings=1
log_closure=closed
=== MUT-h3-subsection-deleted exit=0
file=/tmp/critmistB-xxpv89ho/mut-h3-deleted.md round30_h2_headings=1 round30_h2_or_h3_headings=1
log_closure=closed
```

The third row is the hole: deleting the round-30 entry body (lines 1469-1549) while keeping the round-31 h3 sub-section
at `LOG.md:1550` (`### Round-30 checks re-run for this append (round 31, quiescent committed bytes)`) still prints
`log_closure=closed`, exit 0, because closure is `[ "$h23" -ge 1 ]`. The h3 tolerance is disclosed as `ExecErratumCheck.md`
§R-2 ("an h3 sub-section whose first token is 30 … satisfying the entry"), but the *consequence* — a year's missing round-30
entry can be satisfied by a round-31 appendix about it — is not measured anywhere in wave 1, and the required mutant
(`head -n 1468`) removes **both** headings, so it never exercised the branch. Ditto the current LOG state:
`round30_h2_or_h3_headings=2` means one of the two counted headings is the round-31 h3, not a round-30 entry.

## 4. The erratum's own cited output is superseded on landed bytes (and the check pins it)

```
$ python3 corpus/instruments/recheck-audit.py --quiet; echo exit=$?
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
exit=0
```

`SCORECARD.md:839` states "the audit **now** prints `strict pass=43/43 …`" and `:852` files `strict pass=43/43` under
"Live re-run … Measured 2026-10-25T23:33:27Z, exit 0". The erratum then adds its own trigger: "If `recheck-audit.py`
bytes change later this round (the C1 limb work), re-run and label any new value with its date." **The trigger fired** —
`corpus/instruments/recheck-audit.py` is now `5d4842da…` (base `3fc0d751…`) — and no label was appended:

```
$ grep -c '44/44' SCORECARD.md
0
$ grep -n 'strict pass=43/43' SCORECARD.md
839:r31 erratum: …  841:Pointers: …  852:strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
```

Mitigation, stated so the finding is not overstated: the block carries its timestamp and the digest it measured, so a
careful reader can see it is historical. The un-timestamped sentence at `:839` ("now prints 43/43") cannot be read that
way, and CHECK A cannot see the staleness — it *requires* the `43/43` literal after the anchor, so the historical literal
is load-bearing while the corrected one is invisible. Measured: a scratch copy with the literal updated to the live value

```
=== MUT-corrected-to-live-44/44 exit=1
file=/tmp/critmistB-xxpv89ho/sc-44.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=0
erratum_closure=open
```

(This copy rewrites rather than appends, which R9 forbids anyway — the point is that the check's notion of "cites the
corrected output" is bound to a fixed string, not to the live run at the time it is read.)

## 5. Item (2) — wave-1 sweep, commands and counts

```
$ cd .ufo/waves/round-31/wave1
$ for w in BLOCKED DEFECT survivor FAIL traceback PRE-STATE; do
    printf '%s files=%s hits=%s\n' "$w" \
      "$(grep -rlF "$w" --include='*.md' --include='*.txt' . | wc -l)" \
      "$(grep -roF "$w" --include='*.md' --include='*.txt' . | wc -l)"; done
BLOCKED files=8 hits=17
DEFECT files=1 hits=2
survivor files=21 hits=280
FAIL files=13 hits=70
traceback files=5 hits=31
PRE-STATE files=24 hits=47
$ ls *.md *.txt | wc -l
40
```

Case-insensitive, fixed-string, for comparability with `ScribeGateDraft.md`'s `grep -n -i -E 'BLOCKED|DEFECT|survivor'`:

```
$ for w in BLOCKED DEFECT survivor FAIL traceback PRE-STATE; do
    printf 'ci %s files/hits: %s %s\n' "$w" \
      "$(grep -rilF "$w" --include='*.md' --include='*.txt' . | wc -l)" \
      "$(grep -roiF "$w" --include='*.md' --include='*.txt' . | wc -l)"; done
ci BLOCKED files/hits: 13 25
ci DEFECT files/hits: 15 65
ci survivor files/hits: 21 294
ci FAIL files/hits: 38 458
ci traceback files/hits: 5 34
ci PRE-STATE files/hits: 26 65
```

`ci FAIL` is inflated by the substring `fail-closed` inside pasted audit output; the uppercase-only count (70 hits / 13
files) is the usable one. Per-file distribution of the three words the draft's sweep omitted:

```
$ grep -rcF "FAIL" … | grep -v ':0$'      -> MutRAExisting 18, ExecRALimbs 20, MutSRExisting 8, MutFRExisting 8,
                                            ExecFRLimbs 4, ScoutRALimbMap 3, RevClaimsFreeze 2, ExecSRLimbs 2,
                                            ExecErratumCheck 1, ExecErratumCheck-before.txt 1, ConnSibling 1,
                                            ExecLedgerMerge 1, ExecSRLimbs-scratch/proof.txt 1
$ grep -rciF "traceback" … | grep -v ':0$' -> CritC1Kill 23, ExecFRLimbs 5, MutFRExisting 2, ExecLedgerMerge 2,
                                            ScoutRALimbMap 1
$ grep -rcF "PRE-STATE" … | grep -v ':0$'  -> 24 files (ExecExpectedList 5, ExecFRLimbs 4, ScribeSkillGate 4,
                                            ExecScoreGap 3, ExecErratumCheck-before.txt 3, CritC1Kill 3, …)
```

Classification of every hit I opened (no hidden hard blocker was found):

- `CritC1Kill.md` ×23 `traceback`: mutant-design table (`A3` import-crash, `A6` gutted module) — deliberate, not crashes.
- `ExecFRLimbs.md:148,192-193` and `MutFRExisting.md:99`: a *simulated* traceback proving an exit-code-only kill would
  accept a crash — deliberate fixture.
- `ScoutRALimbMap.md:77`, `ExecFRLimbs.md:60,159`, `MutFRExisting.md:33,60`: fixture stdout (`FAIL F98 … problems=missing-entry`).
- `RevClaimsFreeze.md:196,206`: harness `FAIL F15 … problems=no-source-line,no-recheck-line,…` — these are its **Case 3a/3b
  junk fixtures**, not the live entry (the receipt's own `Case 3a`/`Case 3b` headings bracket them).
- `ExecSRLimbs.md:184`, `ExecSRLimbs-scratch/proof.txt:15`: the pre-fix `selftest cases=10 failures=1` for the new
  `quote-absent` case — expected, closed by the same receipt.
- The eight `BLOCKED` files hold only negative forms ("`BLOCKED:` is not used", "BLOCKED: none"); **no seat hit a hard blocker**.

### 5.1 Mistake classes the wave hit that `ScribeGateDraft.md`'s M31 list omits

| # | Omitted mistake | Evidence (receipt command/output) | Why it belongs in M31 |
|---|---|---|---|
| **O1 (headline)** | **The first landed C1 counter satisfied the frozen predicate with 13 non-load-bearing limbs.** Nine of 13 mutants were behavior-equivalent comment patches ("the instrument's own honest `--selftest` stdout **and** stderr are byte-identical to the unmutated run (`d2adb51f86997c2c`)"), four were `NameError` imports that `py_compile` accepts, and four "kills" came from a second-invocation state effect — printing the target lines byte-exactly at exit 0. | `CritC1Kill.md:25-47` (§0 Verdict), `§3.1` (title: "The landed counter at `eb9b87ff…` accepts the degenerate ledger (the target lines, exit 0)"), `§3.3`, `§3.4` (calibration: honest kills do discriminate). | `ScribeGateDraft.md` cites `CritC1Kill.md` only as corroboration (`:331`, `:392`, `:426`) and never records the defect. This is the round's central verifiability event and the exact reason R17's bar exists; a reader of the draft's Gate would conclude C1's predicate bound the limbs from the start. |
| **O2** | **Five counter digest states inside one wave** (`eb9b87ff…` → `cde7c2b6…` → `67db4a20…` → `bd18c244…` → `c660a95f…`), each closed one attack route; the counter's own selftest went to `cases=20`. | `CritC1Kill.md` §3.1, §3.6, §3.8, §3.9 headings; live digest `c660a95f…` measured twice here (§1). | M31-2 records digest churn for the *F15 entry* only. The M30-2 class ("instrument digest drift during implementation") recurred on the round's headline instrument, five times, and the draft does not say so — so a re-run of any C1 number by a later reader has no digest table to bind to. |
| **O3** | **The M31-1 closure check is green on deletion of the filed paragraph** (§2.1) — measured by `ScribeQuality` and written into R16's limit, but not into M31-1, whose mutant control is erratum-removal only. | This receipt §2.1; `corpus/QUALITY.md:95` "Limit measured here …". | M31-1's claim is "the fix shown able to fail". The demonstration covers one mutant class; the class the criterion forbids (delete rather than errata) is green. A mistake entry must name the weaker demonstration. |
| **O4** | **The round-30 `LOG.md` closure can be satisfied by the round-31 h3 sub-section** (§3): delete the entry body, keep `LOG.md:1550`, check still exits 0. | This receipt §3. | The receipt discloses the tolerance (`§R-2`) but not that the entry itself is optional; the required mutant (`head -n 1468`) removes both headings, so the filed evidence never tests the admitted branch. |
| **O5** | **The erratum's own "the audit now prints `strict pass=43/43`" is superseded on landed bytes (`44/44`, `executes=20`, `lines=44`), and the erratum's own re-label instruction fired without a label being appended.** | §4 above; `ExecExpectedList.md:134` already recorded `43/43 -> 44/44`, `ExecErratumCheck-after.txt:81` recorded `44/44`. | This is M31-1's own class — stale premise — recurring inside the fix, one round later, in the same file. The draft's M31-1 records the timestamp but closes the item. |
| **O6** | **ScribeGateDraft's own sweep is not reproducible from its artifact**: it swept only `BLOCKED|DEFECT|survivor` (row 13 of its table defers to "the sweep output in this seat's run", which is not in the file), and it omitted `FAIL`/`traceback`/`PRE-STATE` entirely. | §5 counts; the draft's own sweep command and row 13. | A sweep is evidence only if its command and output are in the receipt; here 70 `FAIL` hits / 31 `traceback` hits / 47 `PRE-STATE` hits were outside the sweep, and the one row that needed the output points at nothing. |

Not omitted, checked and confirmed: M31-3 (anchor drift), M31-4 (`corpus/QUALITY.md:77` `cases=4` still present —
`grep -c 'cases=4' corpus/QUALITY.md` → `1`), M31-5 (survivor discipline; live instrument prints **18** `selftest …`
case lines and **no** `cases=|failures=` summary, so M31-4's replacement number must not be "cases=18 failures=0" without
re-measurement, and the closed SR survivor now reads `selftest cases=10 failures=0 exit=0`), M31-6 (scratch/commit
hygiene; measured here: `git status --porcelain | grep -c '^??'` → **13** untracked entries — git folds the scratch trees
under directory entries such as `?? .ufo/waves/round-31/wave2/`, so 13 *entries* is not 13 *files* and does not contradict
`SentScopeW1.md`'s 126 touched paths — and exactly **1** modified entry, ` M corpus/instruments/limb-mutation-check.py`,
i.e. the C1 counter itself is uncommitted working-tree state whose digest (`c660a95f…`) was stable across this seat's run).

## 6. Item (3) — R16 / R17 in `corpus/QUALITY.md` (sha `96b71caa…`)

| Requirement | R16 (`:95`) | R17 (`:96`) |
|---|---|---|
| cites the lesson section | **Dangling.** `corpus/lessons/round-31.md` § Mistakes M31-1 — `ls corpus/lessons/round-31.md` → `No such file or directory` at the digest above. Its other cites resolve: `corpus/lessons/round-30.md:110` `## Close-out erratum — final integration state`, and `corpus/lessons/round-30-verifier-spotcheck.md:69-70` §5 items 3 and 4. | **Dangling for the round-31 half and coarse.** `corpus/lessons/round-31.md` § Mistakes (no M-id) — same absent file. Its other cites resolve: `R13`; `corpus/lessons/round-30.md:70` `## Mistakes (M30-*)` → `:74` `**M30-1 — B2 fixture fails to isolate its claimed limb**`. |
| carries an able-to-fail check | **No runnable check in the corpus.** The row states the required exits and cites `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` → `-after.txt` as the specimen; the command itself exists only in that wave receipt (and in §2 here). Its disclosed limit says the specimen does **not** meet the criterion's deletion clause. | **Yes.** It names the exact replay: `corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json`, plus the three controls it must reject. Executed here on quiescent bytes (`c660a95f…` / `c042adf6…` before and after, stable): `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` / `counter_exit=0`, including `CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y` — so "rejected" really means "verdict equals expect", as `ConnClaims.md` §3 warns. |

Reading: **R16 as landed is a criterion with no conforming specimen** — it requires that a check *not* turn green on
rewording or deletion, and the only check it points at does exactly that (§2.1). The row is honest about it, which is
better than hiding it, but a bar admitted in that state either (a) needs the check fixed, or (b) needs the criterion
narrowed to what the specimen proves ("closure is the naming-erratum branch; deletion-closure is a known non-closure").
As written, a later reader can cite R16 and be told the opposite of what its specimen does. R17 is executable and
non-vacuous; its only gap is scope — it governs *claimed* limbs, so the two behaviour-bearing FR mutants
(`ExecFRLimbs.md` §Risks 2, `MutFRExisting.md:52-53,117-120`) are outside it and neither admitted nor refused.

## 7. Impacted axes, and the smallest safe correction

Impacted axes: `depth:verifiability` (M31-1's able-to-fail demonstration, R16's criterion/specimen, the 43/43 → 44/44
stale literal); `coverage` (R16/R17's dangling lesson cite; the wave-1 sweep's omitted word set).

Smallest safe corrections, in order of cost:

1. **CHECK A — close the deletion branch.** Replace
   `if [ "$n" -eq 0 ] || [ "$c" -eq 1 ]` with a closure that requires the filed paragraph present *and* the naming
   erratum: `if [ "$n" -ge 2 ] && [ "$c" -eq 1 ]`. Add the missing mutant row to `ExecErratumCheck`: "filed paragraph
   (813-819) deleted, no erratum" must be **exit 1** (today it is exit 0). Measured criterion for the fix: §2.1's first
   case flips 0 → 1 and §2's three cases keep 1/0/1.
2. **CHECK B — drop the h3 substitution or require the h2 entry.** `if [ "$h2" -ge 1 ]` (canonical level), keeping both
   counts printed. Add the mutant "entry body (1469-1549) deleted, h3 retained" as a required exit-1 case (today exit 0).
3. **SCORECARD — append the label the erratum asked for**: an r31 erratum line naming the `strict pass=43/43` block at
   `:852` and citing the landed run (`strict pass=44/44`, `executes=20`, `lines=44 total=44`, instrument
   `recheck-audit.py 5d4842da…`). Append-only; the filed bytes stay identical.
4. **QUALITY R16** — either attach the runnable check (`bash -n`-parseable) and the required mutant list to the row, or
   restate the criterion to the naming-erratum branch and reword the "deleted has closed nothing" clause as the
   `n -ge 2` rule the check must adopt. Keep the disclosed limit sentence either way — it is the row's best feature.
5. **Lesson/QUALITY sequencing** — land `corpus/lessons/round-31.md` with headings `## Mistakes (M31-*)` and the M-ids
   `ScribeGateDraft` already uses (M31-1 … M31-6, plus O1-O5 above), so R16's "§ Mistakes M31-1" and R17's "§ Mistakes"
   resolve; R17's cite should name M31-5 instead of "(the round-31 survivor/limb entries)".
6. **Mistake list** — add O1-O6 to `corpus/lessons/round-31.md` § Mistakes; O1 and O2 in particular are the round's
   verifiability story and belong beside M31-5, not only inside a critic's receipt.

## 8. What this seat did not do

- No judgement of C1/C2 admission, no instrument edit, no entry/registry/README/SCORECARD/QUALITY/lesson write, no
  delegation, no background job, no peer broadcast (no message was needed; no colleague was addressed).
- No verification run of the C1 *mutant battery* (owned by the wave-2 mutation seats); the one counter invocation above
  is cited only as the state of R17's executable check, on bytes that held identical before and after it.
- The `.ufo/waves/round-31/wave1/ExecErratumCheck-*` receipts were read, never modified; the `.txt` receipts are
  `.ufo/` evidence outside the corpus, which is why R16's pointer to them is not a corpus-side check.
- No campaign-package access, no live bounty contact, no credential material, no lane git/jj mutation, no write outside
  the lane.
