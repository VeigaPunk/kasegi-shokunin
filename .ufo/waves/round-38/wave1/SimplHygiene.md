# SimplHygiene — round-38 audit hygiene (evidence weight, scratch, /tmp, duplication)

Seat: simplifier, round 38, wave 1. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD at work time
`700153593eb586c70a6499c8ca225ee4d673bc9b` (base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`).
Item: audit hygiene — wave-evidence size (round-37 and planned round-38), any file >1 MiB without
being named, S055 capture size, scratch leftovers under `/fast/scratch/hyaku/kasegi-r38`, `/tmp` use
by lane instruments (prompt §7 rule 4), duplicate-content risk (r37 scaffolding duplicated the F20 row).
Deliverable: **receipt only** — no landable text was produced, so no `## DELIVERABLE` block and no
beside-receipt deliverable file. This file is the only lane write; nothing was committed.

Scratch `S=/fast/scratch/hyaku/kasegi-r38/SimplHygiene`, created with `mkdir -p`, all fixtures under
`$S/land/`; `TMPDIR=$S` for every instrument call; removed at the end of the run (see §7).

Method: read-only `git ls-files`/`ls-tree`/`rev-parse`/`status`, `du`/`stat`/`sha256sum`/`find`,
`grep`, and one Python pass over the tracked tree (7355 files) hashing every file ≥4 KiB to group
byte-identical copies. No lane gate was re-run; the only instrument executed was the wave-1
`ExecFenceWalk.sh` deliverable (state mode, writes nothing), over copies in `$S`.

---

## 1. Wave-evidence size

### 1.1 Trees

```
$ du -sb .ufo/waves/round-37   -> 3082296      (83 files)
$ du -sb .ufo/waves/round-38   -> 2313363      (74 files, wave1 still filling at 18:39:02Z)
```

Round-37 breakdown (`du -sb` per entry, descending):

| bytes | entry |
|---:|---|
| 1 333 922 | `wave1/` (64 seat receipts) |
| 473 712 | `wave1-dispatch.json` |
| 472 985 | `wave1-plan.out` |
| 449 103 | `wave1-spec.json` |
| 326 389 | `kasegi-r37-build-results.json` |
| 9 238 | `final-gates/` |

Round-38 breakdown at 18:39:02Z: `wave1/` 1 114 407, `wave1-dispatch.json` 606 497,
`wave1-spec.json` 577 124, `claims.json` 9 133, `c1-controls/` 1 744, `c2-controls/` 1 384,
`census-before.txt` 276, `wave1.ready*` 2 798.

### 1.2 Planned round-38 bytes

Landable deliverables already in `wave1/` (the set that will be copied into the lane), measured:

```
$ stat -c'%s %n' wave1/ExecC2Capture.S055.txt wave1/ExecC2Capture.manifest.json \
    wave1/ScribeEntryF21.entry.md wave1/ScribeFrontierBlocks.{province-eof,readme-eof}.md \
    wave1/Scribe{Scorecard.section,Scorecard.correction,RowS055.row,SourcesLog.blocks,\
Mistakes.block,LOG.block,PendingResolutions.block,Assimilation.block,Considerthese.block,\
QualityRows.block,SkillRegistry.row}.md
TOTAL 357118 bytes
```

Largest single landed item: `ExecC2Capture.S055.txt` 272 441 B (76 % of the landing set). `r38-closure.sh`
is not yet delivered at read time (`ls wave1/ExecSuiteBuild.r38-closure.sh` → No such file); its size
class is the r37 predecessor, `corpus/instruments/r37-closure.sh` = 73 132 B (r36 39 022, r35 35 391).

**Projection.** round-38 wave on disk 2 313 363 B + landing set 357 118 B + a ~73 KB closure script
≈ **2.74 MB** total evidence+landing footprint, against round-37's 3 082 296 B. Both rounds stay under
4 MiB; the round-38 wave is smaller than round-37's despite 73 seats vs 64, because round-37 carried
`wave1-plan.out` (473 KB) and a 326 KB build-results file that round 38 has not produced yet.

### 1.3 Files over 1 MiB

```
$ find .ufo/waves/round-37 -type f -size +1M   -> (none)
$ find .ufo/waves/round-38 -type f -size +1M   -> (none)
$ find . -path ./.git -prune -o -type f -size +1M -printf '%s %p\n'
1479694 ./corpus/source-snapshots/round-35/S052.txt
1470121 ./.ufo/waves/round-29/wave1/assimilation/fetch/S069.pdf
```

Both are named, both tracked, neither is in a wave dir of this round. Naming quality differs:

- `S052.txt` — bound: `git ls-files --error-unmatch` succeeds and
  `corpus/source-snapshots/round-35/manifest.json` carries `"id": "S052"` with the path/sha. **Named and bound.**
- `S069.pdf` — `git ls-files -s` → `100644 ef4367706c… .ufo/waves/round-29/wave1/assimilation/fetch/S069.pdf`.
  It is named by size only in prose (`corpus/lessons/round-35.md:124` — "`-k` fetch 200, 1,470,121 B PDF"),
  and it is **not** bound: `corpus/source-snapshots/round-29/manifest.json` holds only
  `S043`, `S044`, `S045`, and `grep -n 'S069' corpus/SOURCES.md` returns nothing. So it satisfies
  "named" by the letter of the item (byte count named in one lesson row) but not by the binding rule the
  other snapshots follow. Minimal action: none this round (deleting it would destroy the only bytes behind
  the r35/r37 `present-and-located` S069 verdict); record the gap, do not move files.

### 1.4 S055 capture

| metric | value |
|---|---|
| path landed | `corpus/source-snapshots/round-38/S055.txt` (dir absent at read time; deliverable copy `wave1/ExecC2Capture.S055.txt`) |
| bytes / lines | **272 441 / 5 146** (0.26 MiB — well under the 1 MiB line) |
| sha256 | `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` |
| source fetch | `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`, HTTP 200, `text/html`, no redirect, `fetched_bytes=414858`, fetched `2026-10-26T18:25:51Z`, UA `kasegi-shokunin/1.0` |
| raw sha256 | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| manifest | `wave1/ExecC2Capture.manifest.json`, 3 841 B (same directory) |

Size is in the same band as the r37 capture class and smaller than `S052.txt` (1.48 MB) and the r36
snapshots; no size objection to landing it.

---

## 2. Scratch leftovers — `/fast/scratch/hyaku/kasegi-r38`

Listed only, nothing deleted (other seats' trees). Two snapshots, seven minutes apart, showing the
delete-on-exit discipline working:

18:34Z — 34 entries, **1 128 680 602 B**; top: `ExecRefChecker` 467 702 769, `RevHarness` 363 902 527,
`ScribeLedgerFill` 141 075 588, `CritC1Export` 121 102 259, `ScribeFrontierBlocks` 17 585 841.

18:38:24Z — 31 entries, **2 543 423 211 B**; `ExecRefChecker` and `RevHarness` are gone (their seats
finished and removed their dirs between the two reads):

| bytes | dir | note |
|---:|---|---|
| 1 261 769 068 | `ScribeLedgerFill` | 7 × `mut-*` fixture trees at ~140 MB each (`mut-oxVl`, `mut-IYni`, `mut-9Shr`, `mut-zmEY`, `mut-XOca`, `mut-WNGD`, +1) — the single largest live consumer |
| 362 976 474 | `RevClaimsFreeze` | lane exports |
| 243 400 676 | `CritMotivation` | |
| 243 022 285 | `CritC1Export` | `arch/` 121 102 259 + `fxsh.PdH4wN` 121 827 614 |
| 134 623 421 | `ExecSuiteBuild` | |
| 122 298 417 | `CritC2Kill` | |
| 121 102 259 | `MutG1G2` | |
| 18 319 922 / 15 986 431 / 10 161 634 / 3 728 543 | `ConnC1C2`, `ScoutVexLeads`, `ExecQuarantine`, `ScribeGateLesson` | |
| ≤ 2 MB each | `L1`, `ExecSchemaCross`, `RevEntryF21`, `SimplReport`, `CritC2Ground`, `ConnPatterns`, `CritBoundary`, `CritJudgedHead`, `ScribeShonen`, `ScoutR37Evidence`, `SentSecrets`, `CritC1Kill`, `RevSelftestBar`, `RevNoHarm`, `RevSuiteDesign` | |
| 0 | `SentScope`, `RevPendingResolutions`, `MutG5G8`, `MutG3G4` | empty dirs, seats still live |

Free space is not at risk: `df -h /fast/scratch` → `804G 199G 605G 25%`.

Only the round-38 root exists — no `kasegi-r36`/`kasegi-r37` root, no `/tmp` residue
(`ls -d /tmp/*kasegi* /tmp/*r37* /tmp/*r38*` → nothing). The live total is transient by design
(each seat's dir is a working export); G6 measures the root at filing, not now.

---

## 3. `/tmp` use by lane instruments (prompt §7 rule 4)

Rule 4 forbids a committed tool that writes under `/tmp` *regardless of* `TMPDIR`/`--work`.

```
$ grep -rnE 'mkdtemp|mktemp|tempfile|TMPDIR|HYAKU_SCRATCH|KASEGI_SCRATCH' corpus/instruments --include='*.py' --include='*.sh'
```

Result: **zero non-compliant tools.** Three distinct shapes, all rule-4-clean:

1. **Scratch root with explicit precedence and a `--scratch`/`--work` argument** —
   `frontier-recheck-count.py:332`, `capture-binding-check.py:815`, `kill-rule-check.py:389`
   (`arg` → `$HYAKU_SCRATCH` → `$TMPDIR` → `/fast/scratch/hyaku` if present, else `tempfile.gettempdir()`),
   each passing the resolved root as `mkdtemp(dir=base)`.
2. **Plain `mktemp -d` / `mkdtemp()` with no `dir=`** — `r36-closure.sh:218` and `r37-closure.sh:287`
   use `mktemp -d -t r37-closure.XXXXXXXX` with an in-file comment "TMPDIR is honoured by mktemp itself;
   no path is hardcoded here"; same for `anchorcheck.py:299`, `mirror-containment-check.py:161`,
   `resolve-dispatch-check.py:214`, `capture-source.py:102`, `limb-mutation-check.py:260/599/619`,
   `score-gap.py:462`, `source-recheck.py:262`, `recheck-audit.py:201`. `tempfile` honours `TMPDIR`, so the
   seat's `TMPDIR=$S` binds them.
3. **Fallback-only `/tmp` in older shells** — `r-defect-closure.sh:461/750`
   (`${TMPDIR:-/tmp}` plus `SCRATCH_ARG`/`$HYAKU_SCRATCH`) and `r35-defect-closure.sh:114`
   (`${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}`). Both honour `TMPDIR` and accept a scratch argument, so they are
   compliant; `/tmp` is the last resort, not a hardcoded write root.

Literal `/tmp` strings elsewhere are **documentation or fixtures, never write roots**:
`density.py:6-7` and `resolve.py:10,43` cite historical `/tmp/kasegi-r13|r15` provenance in docstrings;
`citation-survival.tsv` rows record `/tmp/…` citations that are `GONE` (the survival evidence itself);
`recheck-audit.py:216` holds the string `"recheck: cd /tmp && python3 …"` as the `elsewhere.md`
selftest *fixture line* — the instrument only parses it and writes every fixture under its own
`TemporaryDirectory()`. No wave-1 deliverable hardcodes `/tmp` either: `ExecFenceWalk.sh:71` and
`ExecNoHarm.sh:107` both use `mktemp -d "${TMPDIR:-/tmp}/…"`, and this seat ran them with `TMPDIR=$S`.

---

## 4. Duplicate-content risk

### 4.1 The r37 scaffolding paste — quantified, still live in the tree

```
$ grep -n '```' PROVINCE.md        -> 81, 96, 124
$ wc -l PROVINCE.md corpus/README.md -> 152 / 454
$ sed -n '81,152p' PROVINCE.md | wc -c        -> 5645
$ sed -n '399,454p' corpus/README.md | wc -c  -> 4748
```

The pasted range `PROVINCE.md:81-152` is 72 lines / 5 645 B; **48 of its 58 non-blank lines are
byte-identical to lines already in `corpus/README.md`** (83 %), including the full receipt property
table and the "Harness on the same mirror" validation paragraph. The duplicate F20 row is exact:

```
PROVINCE.md:114 == corpus/README.md:416  ->  True   (both 1216 B)
```

So the r37 D-A defect is not just scaffolding noise: it is a **1 216 B frontier row stored twice and 48
duplicated lines across the two front-door files**, which is why a naive row counter on PROVINCE can
report a 21st frontier row. This seat found no new instance of the class in the round-38 landables.

### 4.2 Fence semantics — the one trap a duplication audit must not fall into

A naive toggle (`grep -c '^```'`, even = closed) gives the *wrong* answer on PROVINCE: 3 fence-ish
lines ⇒ odd ⇒ "open". Under CommonMark the ` ```text ` at L96 has an info string and cannot close the
block opened at L81, so L124 closes it and the walk ends **closed**. Measured independently with the
wave-1 walker (`bash wave1/ExecFenceWalk.sh <file>`, state only):

```
PROVINCE.md       -> closed
corpus/README.md  -> open      (single ``` at L426, no closer)
```

and over scratch copies with the round-38 blocks appended (the landing simulated in `$S/land/`):

```
$S/land/README.md   (486 lines) -> closed
$S/land/PROVINCE.md (156 lines) -> closed
grep -c '^| F21 |' $S/land/README.md -> 1     $S/land/PROVINCE.md -> 0
```

This agrees with `wave1/ExecFenceWalk.md` (which cross-checked with `cmark`: `cmark_blocks=[(81, 124)]`).
Consequence for G1: its "fence state closed at EOF" limb **must** specify the CommonMark closing-fence
rule (no info string on the closer); a grep-parity check would grade PROVINCE red for a defect it does
not have. No cleanup needed — a disclosure, so a later auditor does not "fix" a balanced file.

### 4.3 F21 row placement — no duplicate (checked because it is the r37 class)

`wave1/ScribeFrontierBlocks.readme-row.md` is byte-identical to line 23 of
`ScribeFrontierBlocks.readme-eof.md` (both 1 260 B for the row, `cmp`-equal per that seat's receipt);
the landing uses only the eof block, so after landing `corpus/README.md` carries exactly one `| F21 |`
row (verified above: 1) and `PROVINCE.md` none. Prior rounds also show zero F-row duplication
(`grep -oE '^\| F[0-9]+ ' corpus/README.md | sort | uniq -c` → no count >1; 20 rows; `SOURCES.md` 54 rows,
no duplicate id).

### 4.4 The real duplicate mass: spec/dispatch and committed fixture trees

**Spec ↔ dispatch.** The per-seat prompt text is stored twice, verbatim:

```
round-37: spec prompt bytes 430127 | dispatch task bytes 443382 | spec prompt present verbatim in dispatch task: 430127
round-38: spec prompt bytes 557146 | dispatch task bytes 572198 | spec prompt present verbatim in dispatch task: 557146
```

i.e. **97.4 % of every dispatch task is the spec prompt byte-for-byte** (dispatch adds only the
`/skill:godspeed` prefix and the item spec). That is 557 146 B duplicated inside round-38's own evidence
(1 183 621 B across the two files) and 430 127 B in round-37's. Both files are legitimate as artifacts
(spec authored, dispatch the validated form), but the payload is a copy. Cheapest fix is in the driver,
not the lane: `wave1-dispatch.json` carries `spec_sha256` + seat names, or `wave1-spec.json` carries the
prompt body and the dispatch carries `"prompt_ref": "<sha256>"`.

**Tracked byte-identical copies.** Hashing all 7355 tracked files, 422 groups ≥4 KiB are byte-identical,
i.e. **78 784 657 B redundant** (size×(n−1)). By the round that owns the extra copy:

| round | redundant bytes | class |
|---:|---:|---|
| 25 | 48 982 187 | committed fixture/mutation trees (`c1-controls/M1..M4`, `wave1/mut-audit/base`, `wave1/rev-independent/base-tree`, `mut-skip`, `c1-after-35`) |
| 26 | 24 252 333 | same class (`c1-controls/fixtures/*`, `wave2/b8/*`) |
| 0 (root) | 2 318 603 | root files copied by those fixture trees (`.ufo/rounds/…`, `LOG.md`, `SKILL.md`, `wave1-*spec/dispatch`) |
| 28 | 2 095 552 | `MutManifestC2/*`, `MutQuoteC2/work`, `ScribeEntryC2/scratch` snapshot copies |
| 29 | 504 913 | fetch copies |
| 31 | 345 870 | |
| 30 | 285 199 | |

**Rounds 37 and 38 contribute zero duplicate groups.** Worst single offender: one 249 789 B snapshot
(`round-24/S032.txt`) exists **×41**; `citation-survival.tsv` ×41; `round-24/S002.txt` ×41 — one
fixture tree's lane mirror stored per mutant. This is exactly the shape prompt §7 rule 3 forbids
("no mirror of the whole lane inside a wave `build/` dir"); those trees are committed history, so they
are a lane decision, not a seat's deletion. Per-round tracked wave totals for context:

```
round: files / bytes     23:104/1691701   24:82/1079812   25:3773/57513849  26:1535/26199699
27:10/10126  28:361/5705241  29:222/3881812  30:154/1798382  31:243/3412966  32:23/401010
33:147/1932368  34:110/2923280  35:110/2941009  36:80/2668477  37:83/3082296  38:7/1196158(tracked so far)
all waves: 116438186 B / 7044 files
```

**Capture copy on landing.** `wave1/ExecC2Capture.S055.txt` (272 441 B) + its manifest (3 841 B) are the
landable-byte copies and will also exist at `corpus/source-snapshots/round-38/`. No round-23..37 wave dir
holds a byte-identical copy of any snapshot (`sha256` join of `wave1/*` against
`corpus/source-snapshots/*/*.txt` → no match), so round 38 adds **276 282 B of intentional duplication**
mandated by the deliverable-beside-receipt rule. Accepted, but it is the second-largest duplicate after
spec/dispatch, and it is avoidable next round if the declared-blocks contract accepts
`sha256 + lines + path` instead of the bytes.

**r37 build-results.** `kasegi-r37-build-results.json` (326 389 B) holds 64 `results[].output` strings
totalling 304 912 B; **none** is embedded verbatim in its seat receipt (`output in receipt` → 0/64), so
it is a distinct artifact, not a copy of `wave1/*.md` (1 320 468 B) — no byte duplication there, only the
300 KB of a post-`complete` commit that D3 already flags.

---

## 5. Minimal cleanup list

Ranked; nothing here is a correctness gate. "Owner" is who can act without widening a seat's write scope.

| # | action | bytes at stake | owner | risk if skipped |
|---|---|---:|---|---|
| 1 | **Do not append `ScribeFrontierBlocks.readme-row.md` on its own.** It is byte-identical to line 23 of the eof block; a second append makes the frontier 22 rows and trips the C2 kill rule. | 0 (prevents +1 260 B of duplicate row) | L1 landing | C2 red for a duplicate row |
| 2 | At filing, remove `$HYAKU_SCRATCH/kasegi-r38` after the wave dir is copied in; expect `ScribeLedgerFill/mut-*` (≈980 MB, 7 trees) to be the last big survivor. | ~1.26 GB live now | L1 (seats already delete their own) | G6 red; disk-guard reaper churn |
| 3 | Driver: have `wave1-dispatch.json` reference the prompt by sha256 instead of embedding the 557 KB of spec prompt. | 557 146 B/round (r38), 430 127 B (r37) | L1 / dispatch generator | none functional; ~1.18 MB of round-38 evidence is one payload twice |
| 4 | Defer, lane decision: the round-25/26 committed fixture trees (3 773 + 1 535 files) hold 73 234 520 B of redundant lane mirrors — the §7-rule-3 class. Dropping them needs a gate-reproduction ruling (their hashes are cited by r25/r26 receipts). | 73 234 520 B | lane (single commit + lessons note) | none now; the repo carries 75 MiB of copies |
| 5 | Defer: deliver the capture once (land `S055.txt`/manifest, keep only `sha256+lines+path` in `wave1/`) if the declared-blocks contract allows. | 276 282 B/round | L1 / block contract | none functional |
| 6 | Record (no move): `S069.pdf` (1 470 121 B) is named only in `corpus/lessons/round-35.md:124` and unbound from any manifest, unlike `S052.txt`. Add the binding at the next round that touches the source ledger, or state the exemption. | 0 | scribe next round | an auditor re-derives "named?" from prose only |

Not on the list, deliberately: deleting the r37 paste lines (`PROVINCE.md:81-152`) — R6 append-only, and the
round-38 corrections already mark them misplaced; deleting `S069.pdf` — the only bytes behind an admitted
verdict; touching any other seat's scratch dir.

---

## 6. Preserved contract / non-findings

- Only file written: this receipt (`wave1/SimplHygiene.md`). No commit, no staging, no lane file edited.
- No file in either wave exceeds 1 MiB; the two lane files that do are named and tracked (§1.3).
- Committed instruments: 0 rule-4 violations (§3); the two `${TMPDIR:-/tmp}` fallbacks honour `TMPDIR`
  and accept a scratch argument.
- No `/tmp` residue and no `kasegi-r36`/`kasegi-r37` scratch root; the surviving `kasegi-r38` root is live
  round-38 seats, listed in §2 and not touched.
- Serialization check: round-38 `wave1-spec.json` and `wave1-dispatch.json` carry the same 73 seat names
  (`set(spec.items[].name) == set(dispatch.taskCall.tasks[].name)` → True; round-37 64/64 also True), so
  the duplication in §4.4 is a copy, not a desync.
- F21 does not exist in either front door before landing (`grep -c F21 PROVINCE.md corpus/README.md` → 0, 0)
  and exists once after it (simulated in §4.2).

## 7. Scratch removal

`S=/fast/scratch/hyaku/kasegi-r38/SimplHygiene` held only `land/` (two copies of the front-door files with
the round-38 blocks appended, used for the §4.2 landing simulation). It was removed after this receipt was
written; verification follows the removal command in the run log:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r38/SimplHygiene
$ ls -d /fast/scratch/hyaku/kasegi-r38/SimplHygiene 2>&1
ls: cannot access '/fast/scratch/hyaku/kasegi-r38/SimplHygiene': No such file or directory
```

Other seats' entries under `/fast/scratch/hyaku/kasegi-r38` were listed (§2) and left in place.
