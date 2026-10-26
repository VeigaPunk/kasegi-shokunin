# ExecSuiteBuild — round-38 wave 1 (C1 depth:verifiability)

Leaf executor seat. Scope: build the complete instrument `corpus/instruments/r38-closure.sh` and
write it byte-exact beside this receipt. No lane, fleet, sibling-lane or source-tree file was
written by this seat; the only writes are this receipt, the deliverable beside it, and scratch under
`/fast/scratch/hyaku/kasegi-r38/ExecSuiteBuild/` (removed before yielding). No mutating git command
ran outside a `git init` fixture whose `rev-parse --show-toplevel` was verified equal to the fixture
path; all lane reads were read-only (`archive`, `cat-file`, `merge-base`, `diff`, `rev-list`,
`rev-parse`, `ls-tree`, `log`).

The instrument was revised three times before filing (two in-wave reviews, §8); the numbers below are
the final bytes.

## 0. Deliverable

| file | lines | bytes | sha256 | mode |
|---|---:|---:|---|---|
| `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh` | 1767 | 77726 | `09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42` | `-rwxr-xr-x` |

Landing path: `corpus/instruments/r38-closure.sh` (byte-identical; the L1 copies it unchanged).
8 `check_g<n>()` bodies and 8 `selftest_case_G<n>()` bodies are in the file.

## 1. What the suite does

Modelled on the committed `corpus/instruments/r37-closure.sh` (re-read in full: export/work-dir
guards, `suite_digest()`, cleanup trap, `mut_reset`/`mut_put`/`st_pos`/`st_neg`/`st_verdict`,
`judge_selftest_report`). Differences are the eight checks, the `--scratch-root` default
(`/fast/scratch/hyaku`), `BASE_REF=a173b0c2…` as a file constant, G6's live scratch rule, and the
G2 limbs the three review passes earned (§8).

Flags: `--export-ref <hash>` (required for a run), `--selftest [--export-ref <hash>]`, `--lane DIR`
(default the lane), `--work DIR` (realpath must be outside the lane; `export/` and `mut/` cleared
before use; a symlink into the lane is refused after `pwd -P`), `--scratch-root DIR`, `-h`.
Plain run → exit 2 with two stderr lines. Output: one header line
`export-ref=<hash> mode=export lane=<lane> suite-sha256=<digest>` (plus `deviation=` lines for a
non-default `--lane`/`--scratch-root`), one `G<n> payload=k=v,… closed=0|1` line per check, then
`closed=<k>/8 exit=<0|1>`; exit 0 only for 8/8. The self-report is re-counted before printing, so a
mangled run prints `suite problem=…` and `closed=0/8 exit=1`.

Checks, as implemented (each is fail-closed; the payload names the limb that reopened):

| id | defect | closes on |
|---|---|---|
| G1 | D-A | `Correction (round 38)` lines carrying `L79-L152` / `L399-L454`, the word `misplaced`, and sitting OUTSIDE every fenced block; two fence walks (the contract's backtick walk and a fuller CommonMark walk with tilde fences and opening/closing run lengths) must both end `closed`; `.ufo/waves/round-38/declared-blocks.txt` parsed as lane-relative `<path> <lines> <sha256>`, `tail -n <lines> <path> \| sha256sum` equal for every line, ≥1 line per front door, and each front-door tail carrying its round-38 correction |
| G2 | D-B | receipt `all-gates v2` (header read up to the first `== ` marker); one `export-ref=<40hex>` that IS a commit (`cat-file -t`), resolves and is ancestor-or-equal of REF; `git -c diff.renames=false diff --no-renames --name-status <export-ref> REF` showing only `A`/`M`/`R` at any path (renames off, so a `git mv` cannot collapse to the receipt); every commit in `export-ref..REF` changing only `A`/`M`/`R` rows (a file added and removed inside the range is invisible to the endpoint diff); one `suite-sha256=` equal to the executing digest; exactly 8 `G<n> payload=… closed=1` lines (ids G1-G8 once each) and NO `closed=0` line; one `closed=8/8 exit=0`; exactly 8 `selftest case=G<n> ` lines each claiming a real pass (`positive=pass`, `verdict=pass`, `mutants=<o>/<n>` with n≥1 and o==n); one `selftest cases=8 failures=0`; the recorded payload KEY SETS for G1,G3-G8 equal to this run's (G2 is exempt and is evaluated LAST); the SCORECARD `## Round 38` section and SHONEN carrying the literal `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt`; and zero lines in that section / among SHONEN's round-38 lines matching `(final (lane )?(head\|commit)\|judged head)[^\|]*[0-9a-f]{7,40}` (case-insensitive) |
| G3 | D-C | `## Pending-marker resolutions (round 38)` in `corpus/lessons/round-37.md` with table rows naming L10, L90, L95, L216, L265, L300, L320, L85 (8 distinct); 0 occurrences of `⟨pending`, `<fill>`, `filled by the L1`, `<LANE_HASH>`, `<r38-`, and 0 word-bounded `TBD`/`TODO`, on the `+` (not `+++`) lines of `git diff a173b0c2… <REF>` minus `.ufo`, the instrument and `corpus/instruments/r38-fixtures` |
| G4 | D3 | every `.ufo/waves/round-38/*-dispatch.json` in the export (≥1) has a `-results.json` sibling, or `<wave>-results.json`, that JSON-parses, reports the SAME `wave`, and whose seat-entry count (`results` list length, else `seats`) equals `len(taskCall.tasks)` (which must be ≥1) |
| G5 | D-D | `## Round 38` section has 0 `Final lane commit:` lines; SCORECARD has ≥1 line beginning `Correction (round 38)` containing `f3246559` and `anchor ancestor` |
| G6 | D-E | LIVE, fail-closed: `kasegi-r36`/`kasegi-r37` absent or 0 entries; `kasegi-r38` absent or only the canonical path of this run's `--work` (or its top-level parent under `kasegi-r38`, tolerated only through an empty chain of single components); every top-level entry counted, `find` rc read, unreadable ⇒ RED, tolerated entry printed |
| G7 | D-F | `## Round-37 dispositions — filled (round 38)` after `## Round-37 dispositions (appended 2026-10-26, R31 home)`, with a `Correction (round 38)` line and ≥7 table rows whose first cell IS a proposal number (`7` or `7. …`; `7x`/`7.5` do not count), all of 1-7 present |
| G8 | carry-over | the export's own `corpus/instruments/r37-closure.sh` run with `--export-ref REF --lane <lane> --work <work>/r37` ends `closed=14/14 exit=0` |

`--tree` was **not** added: the positives are proven with a scratch git fixture repo (`git init`
inside the verified fixture; its commits carry the overlay; the suite runs with `--lane "$D"`),
which is the item's documented alternative.

**G2's green window** (stated in the header): the receipt is read from the export, so a run at the
judged head J — the commit that by construction does NOT contain the receipt — reports G2 red
(`receipt=0`) and cannot reach 8/8. The 8/8 run is at the lane tip Y that adds the receipt, whose
`export-ref` names J. The verification command is therefore
`bash corpus/instruments/r38-closure.sh --export-ref <Y>`, and the report names J and Y.

## 2. Evidence — the contract's counting commands (delivered bytes)

All ran from the lane root with the delivered file.

```
$ bash -n .ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh
(silent)                                                   # exit 0
$ bash .ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh
r38-closure: refusing to run against the live worktree: this suite is export-mode only.
r38-closure: pass --export-ref <hash> (see --help) or --selftest.
                                                            # exit 2
$ bash … —export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e --work <scratch>/f2-base --scratch-root <scratch>/fakeroot
export-ref=a173b0c2b98c5ae39599fa9be76027fbbead0b9e mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42
deviation=non-default --scratch-root
G1 payload=province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-blocks=0,declared-ok=0 closed=0
G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=0,shonen-ref=0,head-token-lines=0,crossrun=0,history=0 closed=0
G3 payload=resolutions-section=0,line-tokens=0,added-pending=0,added-placeholders=0,diff-read=ok closed=0
G4 payload=dispatches=0,pairs=0,seats-ok=0,read=fail closed=0
G5 payload=round38-section=0,final-lane-commit-lines=0,correction=0,f3246559=1,anchor-ancestor=1 closed=0
G6 payload=r36=absent,r37=absent,r38=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=filled-section=0,correction=0,proposal-rows=0,missing=0 closed=0
G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=1/8 exit=1
$ bash … —export-ref 2387dcf6ccfefcfb703783387b9aade8fc82abfa --work <scratch>/f2-r37 --scratch-root <scratch>/fakeroot
export-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa mode=export lane=… suite-sha256=09d46673…
G1 …closed=0  G2 …closed=0  G3 …closed=0  G4 …closed=0  G5 …closed=0
G6 payload=r36=absent,r37=absent,r38=absent,work=outside,tolerated=none,read=ok closed=1
G7 …closed=0  G8 payload=r37-suite=1,r37-closed=0,r37-exit=1 closed=0
closed=1/8 exit=1
```

Both required red controls hold: base `a173b0c2` and the r37 judged head `2387dcf6` each print
`closed=1/8 exit=1` (`closed<8/8 exit=1`). G6 is green there only because a scratch root with no
`kasegi-r3x` entries was passed; G8 is red at both because the exported ref is not the lane HEAD
now (r37's E9 `head-match=0`, `status-dirty=3` when measured mid-wave), which is the staleness
guard working, not a suite defect. The live default-scratch run shows the environment as it is
mid-wave:

```
$ bash … —export-ref a173b0c2… --work <scratch>/fin-live            # default --scratch-root=/fast/scratch/hyaku
G6 payload=r36=absent,r37=absent,r38=present,work=inside,tolerated=none,read=ok closed=0
closed=0/8 exit=1
```

`kasegi-r38` held 17-26 live seat entries at measurement time, so G6 is red now by design; it can
only be green at the judged run, after the seats clean up (D-E).

`--selftest` at base (positives red is expected and reported honestly; every mutant still rejected):

```
$ bash … —selftest —export-ref a173b0c2… --work <scratch>/w-st5 --scratch-root <scratch>/fakeroot
selftest case=G1 positive=fail mutants=6/6 verdict=fail
selftest case=G2 positive=fail mutants=12/12 verdict=fail
selftest case=G3 positive=fail mutants=2/2 verdict=fail
selftest case=G4 positive=fail mutants=4/4 verdict=fail
selftest case=G5 positive=fail mutants=4/4 verdict=fail
selftest case=G6 positive=pass mutants=5/5 verdict=pass
selftest case=G7 positive=fail mutants=3/3 verdict=fail
selftest case=G8 positive=fail mutants=2/2 verdict=fail
selftest cases=8 failures=7
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
```

Guards, also measured: unknown argument → exit 2; `--work` inside the lane → `r38-closure: --work
must be outside the lane (it would write there): …` exit 2; a symlink to the lane → the same refusal
on the resolved path; an unresolvable `--export-ref` → `cannot resolve export ref …` exit 2.

## 3. Evidence — the positives go green (real deliverable blocks)

Fixture: a scratch repo (`git init` in `/fast/scratch/…/overlay-real`; `rev-parse --show-toplevel`
verified equal to it; `git fetch <lane> HEAD`, `update-ref refs/heads/base a173b0c2…`, checkout,
branch). Its parent IS the real base, so G3's `git diff BASE REF`, G2's ancestry limb and G2's
history limb are exercised against real history. Overlay = the actual wave-1 landable blocks:
`ScribeFrontierBlocks.province-eof.md` → `PROVINCE.md`; `ScribeFrontierBlocks.readme-eof.md` →
`corpus/README.md`; `ScribePendingResolutions.block.md` → `corpus/lessons/round-37.md`;
`ScribeLedgerFill.block.md` → the ledger; `ScribeScorecard.correction.md` **then**
`ScribeScorecard.section.md` → `SCORECARD.md`; `ScribeShonen.block.md` → `SHONEN.md`; a
`wave1-dispatch.json`/`wave1-results.json` pair (3 tasks / 3 results); the suite itself at
`corpus/instruments/r38-closure.sh`. `declared-blocks.txt` written as `PROVINCE.md 4 <sha>` and
`corpus/README.md 32 <sha>` from the blocks' own line counts.

Bootstrap (disclosed, the r37 shape): commit C1 carries the overlay; a draft receipt is committed;
a run's emitted payload lines (G2's own line forced closed=1 — G2 is exempt from the cross-run limb)
become the receipt's run block — that bootstrap run shows G2 red only on `crossrun=0`; the second
run is 8/8 and its selftest case lines are pasted in; that receipt is committed on C1 as C3.

```
$ bash <delivered file> --export-ref 7ef171351f569ccd86f3624b04aacd8cc9f50ac7 --lane <fixture> --work <scratch>/rrwork --scratch-root <scratch>/fakeroot
export-ref=7ef171351f569ccd86f3624b04aacd8cc9f50ac7 mode=export lane=/fast/scratch/hyaku/kasegi-r38/ExecSuiteBuild/overlay-real suite-sha256=09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1 closed=1
G2 payload=receipt=1,sentinel=1,export-ref=1,ancestor=1,diff-clean=1,digest-match=1,run-lines=1,closed-line=1,selftest-lines=1,selftest-summary=1,scorecard-ref=1,shonen-ref=1,head-token-lines=0,crossrun=1,history=1 closed=1
G3 payload=resolutions-section=1,line-tokens=8,added-pending=0,added-placeholders=0,diff-read=ok closed=1
G4 payload=dispatches=1,pairs=1,seats-ok=1,read=ok closed=1
G5 payload=round38-section=1,final-lane-commit-lines=0,correction=1,f3246559=2,anchor-ancestor=2 closed=1
G6 payload=r36=absent,r37=absent,r38=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=filled-section=1,correction=1,proposal-rows=7,missing=0 closed=1
G8 payload=r37-suite=1,r37-closed=1,r37-exit=0 closed=1
closed=8/8 exit=0
$ git -C <fixture> diff --name-status C1 C3
A	.ufo/waves/round-38/final-gates/all-gates.txt
$ git -C <fixture> status --porcelain
(empty)

$ bash <delivered file> --selftest --export-ref 7ef17135… --lane <fixture> --work <scratch>/rrwork --scratch-root <scratch>/fakeroot
selftest case=G1 positive=pass mutants=6/6 verdict=pass
selftest case=G2 positive=pass mutants=12/12 verdict=pass
selftest case=G3 positive=pass mutants=2/2 verdict=pass
selftest case=G4 positive=pass mutants=4/4 verdict=pass
selftest case=G5 positive=pass mutants=4/4 verdict=pass
selftest case=G6 positive=pass mutants=5/5 verdict=pass
selftest case=G7 positive=pass mutants=3/3 verdict=pass
selftest case=G8 positive=pass mutants=2/2 verdict=pass
selftest cases=8 failures=0
selftest judge=own-report accepted=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
```

G8 green in the same run is the carry-over evidence: **r37-closure.sh stays `closed=14/14 exit=0`
with the round-38 appends in the tree** (r37's E1 bound hashes, E12 round-37 section, E10 receipt and
E9 quiescence all still hold with `HEAD == the exported ref` and a clean worktree).

## 4. Evidence — declared-blocks cross-check

The peer generator `wave1/ExecDeclaredBlocks.gen.sh` (same `tail -n <lines> | sha256sum` contract)
accepts the fixture's declaration file, agreeing with G1's computation:

```
$ TMPDIR=<scratch> bash .ufo/waves/round-38/wave1/ExecDeclaredBlocks.gen.sh check .ufo/waves/round-38/declared-blocks.txt --root <fixture>
OK   PROVINCE.md lines=4 file_lines=156 sha256=797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf
OK   corpus/README.md lines=32 file_lines=486 sha256=f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
declared=2 ok=2 fail=0 base=0 exit=0
```

My parser is the item's literal rule plus the review hardening: lane-relative paths only, `>=1` line
per front door, every non-comment line valid, and each front-door declared tail must carry the
`Correction (round 38)` line. `#` comment lines are skipped, so the peer's optional
`# base <path> <pre_lines>` guard is tolerated (its `wc -l` limb is not implemented; the item names
only the suffix rule).

## 5. Selftest mutant inventory (38 mutants, all rejected; two accepted G6 controls)

| check | mutants (label → limb) |
|---|---|
| G1 | province-correction-absent → `province-correction=0`; readme-fence-open → `readme-fence=open`; declared-block-byte-flip (one byte flipped inside the declared block after declaring) → `declared-ok=0`; correction-inside-fence (a well-formed correction wrapped in its own fenced block) → `province-correction=0`; unpaired-tilde-fence (a `~~~` block never closed; the contract walk ignores it, the CommonMark walk does not) → `readme-fence=open`; declaration-path-escapes-export (`../PROVINCE.md`) → `declared-ok=0` |
| G2 | sentinel-v1 → `sentinel=0`; digest-mismatch → `digest-match=0`; final-head-hash-in-section → `head-token-lines=1`; correction-line-inside-section → `head-token-lines=1`; closed-zero-run-line → `run-lines=0`; selftest-case-not-a-pass (`positive=fail mutants=0/0`) → `selftest-lines=0`; crossrun-key-drift (an extra payload key) → `crossrun=0`; export-ref-not-ancestor (sibling empty commit, same tree) → `ancestor=0`; post-receipt-diff-extra (a later commit touching a second file) → `diff-clean=0`; export-ref-is-tag-object (an annotated tag's own hash) → `ancestor=0`; history-added-then-removed (a secret committed then deleted before the receipt commit; the endpoint diff is receipt-only) → `history=0`; receipt-renamed-into-place (a receipt committed at another path and `git mv`'d into place) → `diff-clean=0` |
| G3 | added-placeholder-token (`TODO` in an added file, parent = the real base) → `added-placeholders=1`; missing-line-token (L265 row dropped) → `line-tokens=7` |
| G4 | results-absent → `pairs=0`; seat-count-short (2 results, 3 tasks) → `seats-ok=0`; results-for-another-wave → `pairs=0`; zero-task-dispatch (0 tasks, 0 results) → `pairs=0` |
| G5 | final-label-in-section → `final-lane-commit-lines=1`; correction-absent → `correction=0`; round38-section-absent → `round38-section=0`; correction-line-inside-section → `final-lane-commit-lines=1` |
| G6 | r36-leftover-file → `r36=present`; r37-leftover-file → `r37=present`; r38-residual-seat → `r38=present`; r38-parent-sibling-leftover (tolerated parent with a sibling) → `r38=present`; unreadable-root (`chmod 000`) → `r37=unreadable`. Controls accepted: own work dir under `kasegi-r38/<seat>/work`; a clean nested chain `<seat>/work/deep` |
| G7 | proposal-row-absent (row 4 dropped) → `missing=1`; correction-absent → `correction=0`; proposal-cell-not-a-number (`1x`) → `missing=1` |
| G8 | carry-over-red (an r37 suite whose last line is `closed=13/14 exit=1`) → `r37-closed=0`; carry-over-suite-absent → `r37-suite=0` |

## 6. Landing constraints the L1 must hold (measured, not assumed)

a. **The SCORECARD correction line must land OUTSIDE the `## Round 38` section.** The landed text
   (`ScribeScorecard.correction.md`, one line) begins `Correction (round 38): …` and quotes
   `` `Final lane commit: f3246559…` `` and the judged-head hash. Appended *after*
   `ScribeScorecard.section.md` it sits inside the section and reds two limbs at once (measured by
   the two dedicated mutants): G5 `final-lane-commit-lines=1`, G2 `head-token-lines=1`. Appended
   *before* the section heading (as in the fixture and in the live tree at measurement time)
   everything is green; G5's correction limb is file-wide, so placement before the heading satisfies
   it.
b. **Verification ref and filing gate.** Run the 8/8 command at the lane tip Y that carries the
   receipt (`--export-ref <Y>`); a run at J is 7/8 by construction (§1, green window). Filing gate
   (routed critic ask, kept as a filing line rather than a suite limb because the suite sees only an
   export): `git rev-parse HEAD master origin/master` all equal the filing head and
   `git status --porcelain` empty — otherwise "the lane tip Y adds only the receipt" is unverified
   and the round-37 post-complete commit recurs. Measured at work time: HEAD, master and
   origin/master all `700153593eb586c70a6499c8ca225ee4d673bc9b` (HEAD detached).
c. **Receipt = `J` + one file, and its payloads must be a REAL run's shapes.** `export-ref=` must
   name the judged head J (or an ancestor), and the endpoint diff plus every commit in `J..Y` must
   show only `A`/`M`/`R` rows (renames computed off). The `G<n> payload=…` lines are bound by key
   set to a live run: a hand-written receipt with invented payloads is red (`crossrun=0`).
   Bootstrap as the r37 round did: run once, take the emitted payload lines (G2's own line may be
   forced `closed=1`; G2 is exempt), commit the receipt, run again (8/8), then paste the measured
   selftest case lines. No `closed=0` line may appear in the receipt, and the header block (before
   the first `== ` marker) must carry exactly one `export-ref=` and one `suite-sha256=`.
d. **The digest must be the executing bytes.** Run the landed
   `corpus/instruments/r38-closure.sh`; its `suite-sha256=` header line is the value to record. The
   pasted run header (`export-ref=… mode=export …`) and `selftest export-ref=…` header sit after
   the header block and are not counted, so the r37 house format (verified against
   `.ufo/waves/round-37/final-gates/all-gates.txt`) is accepted unchanged.
e. **G6 needs the host clean.** At the judged run: `kasegi-r36` and `kasegi-r37` absent or empty;
   `kasegi-r38` empty, or pass `--work` as its sole top-level entry (or with only a single-component
   chain toward it), or keep `--work` outside the three roots. `tolerated=` names the entry used.
   A live seat dir (any file or symlink, not only directories) is RED, so the judged run must not
   share `kasegi-r38` with a running seat.
f. **G8 re-runs r37-closure.sh live.** It needs the lane worktree clean, `HEAD ==` the exported ref,
   and `kasegi-r37` empty (r37 E9). Run it at the tip, with the wave committed.
g. **G4 needs the results file.** `wave1-dispatch.json` (73 tasks) needs a 73-entry
   `wave1-results.json` (or `kasegi-r38-build-results.json`) with `wave: kasegi-r38-build` tracked
   at J; a missing, short, zero-task or wrong-wave results file is `pairs=0` / `seats-ok=0`.
h. G3's vocabulary is the six fixed strings plus word-bounded `TBD`/`TODO`; `[L1-MEASURE]` is safe
   and passes (verified: the real blocks carry it, `added-placeholders=0`).
i. G2's zero-token rule is literal: keep any 7+ hex token off a SCORECARD round-38 / SHONEN round-38
   line that also contains `final … head|commit` or `judged head`. The real section and SHONEN block
   pass as drafted (measured: 0 matching lines).

## 7. Known limits of the instrument (also in its header)

- G1 requires both fence walks. The contract walk closes only on a run of exactly three backticks,
  so a 4-backtick block that CommonMark would close still reads open (red) — the contract's closer
  is that strict, and the added CommonMark walk does not rescue it. A tilde block opened and closed
  within itself is closed under both.
- G1 validates every non-comment declaration line, requires one per front door, and requires each
  front-door declared tail to carry the correction; it does not require uniqueness per path.
- G2's cross-run limb compares key sets, not values (G6 is live by design) and exempts G2 itself; it
  cannot prove the recorded values were green at the ref the receipt names, and it does not require
  the receipt's selftest block to carry per-id `selftest detail=` lines (r37's E10 did — the case-line
  shape plus the cross-run key sets carry that weight).
- G2's green window is the tip that contains the receipt (see §1).
- G4 compares counts, not seat identities, and reads the first results file it finds under either
  accepted name.
- G6 does not audit the contents of `--work` itself (the caller's own space, cleared only of
  `export/` and `mut/`); the tolerated entry is always printed.
- G8 inherits r37's own live limbs; a dirty lane or stale HEAD reds it by design.

## 8. Review hardening (three passes, measured)

`RevSuiteDesign` (10 probes, then a re-run of all ten on the revised bytes) and `CritJudgedHead`
(5 probes, then a second pass) reported additive false greens. Adopted, with a mutant for each:

- G2: `closed=0` lines banned; recorded selftest case lines must claim a real pass; cross-run payload
  key sets for G1,G3-G8 with G2 evaluated last; `export-ref` must be a commit (`cat-file -t`); the
  endpoint diff read with renames off in `--name-status` form (A/M/R only), which closes the
  `git mv other <receipt>` collapse; every commit in `export-ref..REF` restricted to A/M/R rows,
  which closes the add-secret-then-delete-it history hole the endpoint diff cannot see (fixture:
  `history-added-then-removed`); the receipt header read only up to the first `== ` marker.
- G1: the correction must sit outside every fenced block; a second, fuller CommonMark walk (tilde
  fences, opening/closing run lengths) must also end closed; declaration paths must be relative and
  must not contain `..`; the declared front-door tail must carry the correction.
- G4: the results file's own `wave` must equal the dispatch's, and the dispatch must have ≥1 task.
- G7: the first cell must be a proposal number (`7`/`7. …`), not an awk-coerced `7x`.

Not adopted, with reasons:

- `CritJudgedHead`'s literal parent pin `rev-list --parents -n1 Y` = `Y J`: the frozen contract
  allows any ancestor with a receipt-only diff, and the r37 bootstrap commits the receipt twice
  (draft, measured); the A/M/R history limb adopted above covers what the pin was meant to cover
  without reding that bootstrap.
- Pinning `Y == HEAD == master == origin/master` inside the suite: it is export-mode only and must
  be reproducible over a named head; the pin is kept as the filing-gate line in §6b instead, where
  it was measured (HEAD/master/origin/master all at `70015359…`, tree otherwise dirty mid-wave).
- Replacing the literal label regex with a resolve-every-hex-token rule: measured counterexample —
  the drafted `ScribeScorecard.section.md` cites the claims-freeze commit
  `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`, which is a real commit and NOT an ancestor of base
  (`merge-base --is-ancestor` → not), so that rule would red the real section. The literal rule is
  kept, section-scoped; the "missing `## Round 38` heading" case the critic named is already red via
  `scorecard-ref=0` (G2) and `round38-section=0` (G5), and `round38-section-absent` is a mutant.

`RevSuiteDesign`'s residual list (no per-id detail-line requirement in the receipt, G4
counts-not-identities, G3's `.ufo` exclusion, G6 tolerated-contents) is accepted and restated in §7.
Their R1 — the counting command is only satisfiable at the tip Y — is now stated in the suite header
and in §1/§6b.

## 9. Blockers and errors

None. The suite could not be run green end-to-end on the *real* lane head J, because J does not
exist yet (the round-38 artifacts are uncommitted and the receipt is the commit the L1 will make);
that is the round's construction, not a blocker. The positives were proven on a fixture repo whose
parent is the real base, carrying the actual landable blocks (§3).

## 10. Live pre-integration preview (measured on the working tree while the L1 was landing)

The L1 landed the round-38 appends into the working tree (PROVINCE.md, corpus/README.md, SCORECARD
correction **then** the `## Round 38 result` section, ledger, lesson, SHONEN, SKILL/QUALITY/SOURCES
rows) and wrote `.ufo/waves/round-38/declared-blocks.txt`. The delivered suite's check bodies were
sourced and run read-only against the live tree (`check_<g> "$LANE" -`; no git mutation, nothing
written):

```
G1: province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1
G4: dispatches=1,pairs=0,seats-ok=0,read=ok
G5: round38-section=1,final-lane-commit-lines=0,correction=1,f3246559=2,anchor-ancestor=2
G7: filled-section=1,correction=1,proposal-rows=7,missing=0

G2 section limbs on the landed text: section-lines=18, phrase=1, head-token-lines=0
SHONEN round-38 lines: 4, shonen-ref=1, head-token=0

$ cat .ufo/waves/round-38/declared-blocks.txt
corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf
```

The declaration digests are byte-identical to the ones my fixture computed before the landing (§4),
and both declared tails carry their correction line, so G1 is green on the landed bytes under the
hardened rule, not just on a rehearsal. G5 and G7 are green on the landed ledger and section; the
G2 section/SHONEN limbs are green on the landed wording (phrase present, 0 head+hash lines). G4 is
red only because the results file is not tracked yet (`pairs=0`): `wave1-dispatch.json` is present
with its 73 tasks, so a 73-entry `wave1-results.json` is the outstanding landing item (§6g). G2's
receipt limbs, G3, G6 and G8 cannot be previewed from the working tree — they need the committed J
and the receipt (G2), the base..J diff (G3), a quiet scratch root (G6) and a clean `HEAD == REF`
lane (G8).

## 11. Tooling and scratch

No tool installed or upgraded: `bash 5.3.20`, GNU coreutils 9.12 (`tail`, `sha256sum`, `find`),
`git 2.56.0`, `python3 3.14.8` were already present and sufficient. No pacman, no `uv`, no npm.

Scratch was `/fast/scratch/hyaku/kasegi-r38/ExecSuiteBuild/` (export copies, the fixture repo,
selftest work dirs). It was removed with its contents before yielding; the deliverable and this
receipt are the only surviving artifacts.
