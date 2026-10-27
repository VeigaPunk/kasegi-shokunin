# ScoutDefeatsSpec — round-41 wave-1 receipt

Seat: `ScoutDefeatsSpec` (scout, leaf — no subagents dispatched). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (write scope: this receipt +
`ScoutDefeatsSpec.txt` only). Frozen claims read first:
`.ufo/waves/round-41/claims.json` (authoritative; C1 I1–I12 text read in full
from the raw JSON lines).

## Assignment

Read `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` FULLY (D1–D8),
`MutH1H5.md`, `MutH6H10.md`; extract the defeat-fixture table the r41 suite
must kill (id | target r40 check | exact bytes/recipe | expected red payload |
inheriting r41 check I3–I10); cross-check against claims.json I3–I11; flag any
defeat fixture NOT mapped to an r41 check.

## Sources read (all in the lane repo, read-only)

- `.ufo/waves/round-41/claims.json` — full C1 predicate + kill_rule (raw lines;
  I1–I12 mapping is quoted in the table rows below).
- `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` — full file, D1–D8.
- `.ufo/waves/round-40/wave2/MutH1H5.md` — full (patches M-H1..M-H5, verdicts,
  H4 survivor, observations 1–2).
- `.ufo/waves/round-40/wave2/MutH6H10.md` — full (patches M-H6a..M-H10b +
  inert control, defects D1–D2, fixtures).
- `.ufo/waves/round-40/wave2/CritKillRule.md` — full (escape states F1–F8;
  needed for the I11 cross-check).
- `corpus/lessons/round-40-verifier-spotcheck.md` §5 (routed defects D1–D7).

## Verification commands run (actual output)

```
$ wc -l .ufo/waves/round-40/wave2/MutH1H5.md .ufo/waves/round-40/wave2/MutH6H10.md
  (read in full via the file reader; byte counts confirmed: MutH1H5.md 12K class,
   MutH6H10.md 13K class)
$ wc -c .ufo/waves/round-40/wave2/MutH1H5.h4-nodate.txt \
        .ufo/waves/round-40/wave2/MutH6H10.h7-reorder-receipt.txt
  723  .../MutH1H5.h4-nodate.txt
  1062 .../MutH6H10.h7-reorder-receipt.txt
$ sha256sum .../MutH1H5.h4-nodate.txt .../MutH6H10.h7-reorder-receipt.txt
  c362572072d465fd9c0ec807dcaf4e33004ac3648f5a9351480c19a9dc5bc00a  h4-nodate.txt
  0951033b91d4461d8e3a2021584f9582ec0d688d2fcf25ffc8f58ef0b0a9e1f6  h7-reorder-receipt.txt
```

Both committed probe fixtures exist on disk with the sha256 values recorded in
the two mutation receipts — the r41 suite can bind them by hash.

## Deliverable

`ScoutDefeatsSpec.txt` — 19 lines (1 header + 1 separator + 17 fixture rows),
8199 bytes, sha256 `dd0689f3ee10d837f536d7bdb802b7890734e3dd79ee72477e9980410dba56be`.
The file is the table only (landable bytes; no notes, no validation content).

## The table (verbatim from the deliverable)

| id | target r40 check | exact fixture bytes / construction recipe | expected red payload with fixture present | r41 check inheriting |
|---|---|---|---|---|
| T2 | H2 | correction lines whose named values are the superstrings `closed=7/80` and `failures=10` (substring-embed the real round-39 receipt values `closed=7/8`, `failures=1`) | I3 token-boundary value limb rejects both: `I3 payload=... closed=0` (r40 dialect `corrections=4,named=2,missing=2,fences=closed`; r40 observed GREEN `corrections=4,named=4,missing=0,fences=closed`); graded selftest `case=I3 positive=fail` if either is accepted | I3 |
| T4 | H3 | the criterion row (round-39 lesson table row) placed inside a CommonMark ``` fence; every other fence in the file CLOSED at EOF | I4 fence awareness: fenced criterion line satisfies no line-anchored limb, `I4 payload=... closed=0` (r40 dialect `mentions=1,rows=0`; r40 observed GREEN `mentions=1,rows=1`) | I4 |
| T7 | H9 | a declared-block path whose entry in the exported tree is a symlink resolving OUTSIDE the export root, so the declaration's bytes are read from outside the export (r40 evidence: numstat `1 0 pwn`) | I5 readlink-canonicalizes every declared path and requires resolution under the export root: `I5 payload=... closed=0`, the escaping path counted invalid and no out-of-export content in the diff (r40 observed GREEN `declared=1,valid=1,tail=1,pure=1,paths=1,diff-read=ok`) | I5 |
| T13 | H1 | a SKILL.md line that merely mentions the suite name without being a well-formed Markdown registry table row with structured cells | I7 mention-only rejected: `I7 payload=... closed=0` with registry=0 (r40 observed GREEN `suite=1,digest=1,registry=1,registry-in=skill` from a non-row mention) | I7 |
| T14 | H6 | scratch-root strays named `Kasegi-R40-stray` (case-upper) and `kasegi_r40_stray` (underscore separator); r41 family `kasegi-r41` analogous variants | I6 case/separator-insensitive family match: `I6 payload=strays=2,read=ok closed=0` (r40 observed GREEN `strays=0,read=ok` for both; r40 caught lower `kasegi-r40-stray` and suffix-case `kasegi-r40-STRAY` with `strays=1`) | I6 |
| M-H1 | H1 | suite mutation: replace `r40-closure\.sh` with `r40-closure-renamed\.sh` in the two registry-row EREs (r40 `check_h1` lines 569/571); mutant sha256 `845176ba601d43c3bc1b3a4298ff3b6d8af86360f5a1febbb92ac045d033bdf5` | graded selftest `case=I7 positive=fail` — registry=0 is the patch signal (r40 dialect `suite=1,digest=0,registry=0,registry-in=none`; digest=0 is mode collateral, attribution by case isolation) | I7 |
| M-H2 | H2 | suite mutation: `if (index(s, "closed=7/8") > 0 && index(s, "failures=1") > 0) named++` replaced by bare `named++` (r40 `h2_scan` line 594); mutant sha256 `529b31ba29ec32afdb3799f2add7563d2b423bdb408fcb32a10b334e03097e6f` | graded selftest `case=I3 positive=fail` — bad-values fixture accepted (`rejected=0 rc=0`); run payload inflates (`named=8` vs baseline `named=5`) while the limb stays green = defect present | I3 |
| M-H3 | H3 | suite mutation: `'M39-2'` replaced by `''` (empty -F pattern) in both `check_h3` greps (r40 lines 631/632); mutant sha256 `225d4f58671dc8b4f9027761ddaa3890f6cbc6e37397485d282d0522053e0841` | graded selftest criterion-case positive=fail — `row-absent-at-all` and `mention-without-criterion-row` accepted (r40 dialect `mentions=5,rows=3` and `mentions=6,rows=2`) | I4 (partial — see flag F2) |
| M-H4 | H4 | suite mutation: drop the `date` conjunct from both quote inhabit conditionals (r40 `h4_code` lines 662/670); mutant sha256 `bd5dffa2e2c6d9d4a432ce4fff3a00bc50a9fb6c781e4e0f0db1c51d96ee6c05`; probe fixture = committed `.ufo/waves/round-40/wave2/MutH1H5.h4-nodate.txt` (723 bytes, sha256 `c362572072d465fd9c0ec807dcaf4e33004ac3648f5a9351480c19a9dc5bc00a`): round-39 S056 Gate block with URL + located quote + location token but NO access date | graded selftest fixture `quote-date-absent` must red its case: pristine rc=1 `payload=s056=0,s058=1,s059=1,oversize=0` vs mutant rc=0 green; r40 SURVIVOR (selftest coverage gap on quote/date conjuncts) | NONE — unmapped (flag F1) |
| M-H5 | H5 | suite mutation: `payload_matches` reduced to presence-counting `if [ -n "$rec" ]; then n=$((n + 1)); fi` (r40 line 428); mutant sha256 `af761976a168aad61974e3a07c6738a680b5a7a6525679f206ac25e8205f6164` | graded selftest `case=I8 positive=fail` — `recorded-payload-contradicts-export` accepted (`rejected=0 rc=0`); run payload `forged-payload=accepted` instead of `rejected` (patch also blinds the shared value comparison → couples to I9) | I8 (+I9) |
| M-H6a | H6 | suite mutation: `local root=$SCRATCH_ROOT` replaced by `local root=$WORK` — scan the wrong root (r40 line 761); mutant sha256 `793198e0ddadf4e36c0589fc36d20ccab0b21406f5a70f1483811fd63f2bb6e5` | graded selftest `case=I6 positive=fail` — all four limbs flipped: empty-sibling-family, prior-round-family, current-family, unreadable-root all `rejected=0 rc=0 payload=strays=0,read=ok` with the defect present | I6 |
| M-H6b | H6 | suite mutation: family tolerance `kasegi-r39*\|kasegi-r40*) ;;` reduced to `kasegi-r40*) ;;` — prior-round family invisible (r40 line 779); mutant sha256 `97ca87b4463dfa280334ea46537d0a71c3489e05bd6216dc8c013bcf59aaba0f` | graded selftest `case=I6 positive=fail` — empty-sibling-family and prior-round-family fixtures accepted (`rejected=0 rc=0 payload=strays=0,read=ok`) | I6 |
| M-H7a | H7 | suite mutation: delete `cmp -s -- "$rebuild" "$f" \|\| ok=0` — skip the re-run byte-comparison (r40 line 849); mutant sha256 `c722da207693a2a37407334d901d666417e9be6dc034256050609cf7248505dc`; probe fixture = committed `.ufo/waves/round-40/wave2/MutH6H10.h7-reorder-receipt.txt` (1062 bytes, sha256 `0951033b91d4461d8e3a2021584f9582ec0d688d2fcf25ffc8f58ef0b0a9e1f6`): the real receipt bytes with the H2 and H3 payload lines swapped, every computed field green (`...payload-match=9,h7-line=1`) | the reorder fixture must be rejected with an all-green payload string (pristine rc=1 — `cmp` was the only rejecting clause; mutant rc=0 = r40 SURVIVOR, defect D1); graded selftest must isolate it: `case=I9 positive=fail` when the comparison clause is absent; receipt byte-identity enforced at Y (`I2`) | I9 (+I2) |
| M-H8a | H8 | suite mutation: `[ "$b" -lt 10 ]` replaced by `[ "$b" -le 10 ]` on the negative-control base comparison (r40 line 886); mutant sha256 `d17760b3d09dc0658d57c51a3c0ff217599b0438863a5ab246b311d435389c6f`; equivalent on r40 reachable inputs because leaf mode caps any nested tally below 10; pristine already accepts a leaf-capped green base: `H8 payload=base=7/10,base-exit=1,r39=2/10,r39-exit=1 closed=1` | the negative-control acceptance predicate must be killable by a real numeric comparison: a green base floored at the leaf cap must NOT satisfy the limb; graded selftest `case=I10 positive=fail` for the accepting mutation (r40 SURVIVOR, defect D2) | I10 |
| M-H9a | H9 | suite mutation: remove `[ "$add" = "$lines" ] \|\| continue` — skip whole-tail added-line equality (r40 line 929); mutant sha256 `0dbe96621a6ab61d9329d02cc032b45794dc4fd04b795218b13559a8b9689302` | graded selftest `case=I12 positive=fail` — `declared-short-of-added` accepted: `rejected=0 rc=0 payload=declared=2,valid=2,tail=2,pure=1,paths=1,diff-read=ok` (a declaration one line short of the added block) | I12 |
| M-H10a | H10 | suite mutation: drop the tracked-path deletion guard, `&& [ "$dens" -eq 1 ] && [ "$deleted" -eq 0 ] && exit 0` reduced to `&& [ "$dens" -eq 1 ] && exit 0` (r40 line 973); mutant sha256 `bcc237dda8378d00985ce22a18888f4e0536797864625e546b6514064c7b39bf` | graded selftest `case=I12 positive=fail` — `tracked-path-deleted` accepted: `rejected=0 rc=0 payload=skill-del=0,province-del=0,density=1,deleted=1,diff-read=ok` | I12 |
| M-H10b | H10 | suite mutation: drop the append-only guard (r40 lines 972-973), removing `[ "$skdel" -eq 0 ] && [ "$pvdel" -eq 0 ]` from the exit chain; mutant sha256 `2b39280daa3d55146a496e0d31923cc75e391c2190cd3629aa0c98fc0d654ce8` | graded selftest `case=I12 positive=fail` — `skill-line-deleted` accepted: `rejected=0 rc=0 payload=skill-del=1,province-del=0,density=1,deleted=0,diff-read=ok` | I12 |

## Cross-check against claims.json I3–I11

Claims.json C1 predicate maps, verbatim: I3 ← "the round-40 substring defeat
fixtures `closed=7/80` and `failures=10`"; I4 ← fence awareness "(T3/T4)";
I5 ← declared-block readlink-canonicalization; I6 ← "T14 + CritKillRule";
I7 ← mention-only registry row (T13); I8 ← MutH1H5 per-variant forgery flags
"not count-relative"; I9 ← graded selftest payload-value isolation; I10 ←
"the MutH6H10 M-H8a class"; I11 ← the seven CritKillRule escape states. I12
carries the structural limbs (negative controls red, whole-tail appends,
append-only, zero deletions, density byte-identical, census exit 0).

Result: T2→I3, T4→I4, T7→I5, T13→I7, T14→I6, M-H8a→I10 are **named**
mappings — confirmed. M-H6a/M-H6b→I6, M-H9a/M-H10a/M-H10b→I12 map by defect
class (claims name T14+CritKillRule under I6 and the structural clauses under
I12; the MutH6H10 kill-rule line names the leaf-capped green base and the
count-relative forgery explicitly). M-H1→I7, M-H2→I3, M-H5→I8(+I9), M-H7a→I9
map by class to the r41 successors of their r40 limbs (r41 has no H1..H10
limbs; I7 is the registry-row successor, I3 the value-matching successor, I8
the forgery-flagging successor, I9 the isolation successor).

## Unmapped / partially-mapped defeat fixtures (findings)

**F1 — M-H4 (H4 quote/date conjuncts) is NOT mapped to any r41 check.**
MutH1H5's surviving mutant drops the `date` conjunct from both quote
conditionals and nothing observable changes; the committed probe fixture
`MutH1H5.h4-nodate.txt` (sha256 `c3625720…`, verified on disk) reopens the
class on the pristine suite (pristine rc=1 reds it, a date-conjunct-dropped
suite goes green). The r41 claim set I1–I12 contains no successor of the r40
H4 provenance-block check (URL/location/access-date/quote conjuncts for the
S056/S058/S059-style Gate blocks) — claims.json names only "MutH1H5.md" at
file level under I8, and I8's six variants are receipt-forgery classes, not
the H4 selftest-coverage class. If the r41 suite carries any H4-analog limb, it
must add graded `quote-date-absent` (and ideally `quote-absent`) fixtures; if
it does not, the carry should be recorded so the gap is not silently lost.
**This is the one hard unmapped fixture in the required id set.**

**F2 — M-H3 (criterion-row token content) is only partially mapped.**
Claims name T3/T4 (fence awareness) under I4; M-H3's class is content-token
(the criterion row must cite the lesson token — r40 required `M39-2`; r41's
analog is the evidence-naming content now living in I1's correction lines and
the round-40 lesson table). No r41 check is explicitly charged with "a
criterion/lesson-table row must cite the named firing evidence, not merely
exist unfenced". Recommend the I4 builder confirm the criterion-row limb pins
content (cites `RevC1Counters.defeats.txt` / `CritKillRule.md` /
`MutH6H10.md`), not just fence-state and row shape.

**F3 — T5/T6 (H4 URL-colon location, hyphen-joining) have no r41 successor**
but were already RED in r40 (`rc=1 payload=s056=1,s058=0,s059=0,oversize=0`
for both) — caught defeats, not kill-rule exposures. They inherit only the
same hypothetical H4-analog limb as F1; otherwise record as retired-with-H4.

**F4 — T11 (lying `--scratch-root`: strays=0 unfalsifiable post-hoc) is
partially mapped at best.** Claims charge I6 with "case/separator-insensitive,
recursive, dot-inclusive, fail-closed" + T14 + CritKillRule; T11's distinct
class is root-integrity — the scan must cover the real scratch state and the
produced `strays=0` must remain falsifiable after the run (r40 evidence: a
re-run on the clean default root went `closed=10/10 exit=0` green with the
produced `strays=0`). The r41 export-mode suite runs with `--work` under the
caller scratch, so the class is live; I6's fail-closed/recursive scan limbs
are the nearest inheritance but no claim text names T11. Flag for the I6
builder: bind the scan root to a real, verified directory and keep the
scan-audit trail in the receipt (I2's teed transcript is the natural carrier).

**F5 — CritKillRule "seven" vs the eight labeled states F1–F8.** Claims I11
says "the seven committed CritKillRule escape states"; CritKillRule.md's
verdict header says "7 distinct escape states" but its body labels F1–F8
(F1 nested-depth, F2 container geometry, F3 dotfile, F4 case/Unicode
separator, F5 ancestor-prefix tolerance, F6 fail-open nonexistent root, F7
pending-marker spelling, F8 git-status blindness). The I11 builder must pin
the exact committed set (fixtures: `CritKillRule.h6-escapes.sh`,
`CritKillRule.pending-variants.md`, `CritKillRule.worktree-clean.sh`) and
reconcile the count — presumably F1/F2 count as one depth/geometry class —
before writing "seven" into the graded selftest.

Non-findings (recorded for completeness, all caught or positive in r40, so not
kill-rule exposures): T1 honest-values control → I3 positive limb (must accept
real `closed=7/8`,`failures=1`); T3 4-backtick fence → I4 (caught in r40;
keep a 4-backtick variant so the fence parser is not merely ```-aware); T8/T9
tree-binding patches → caught in r40, class inherited by I12's whole-tail
append-only limbs; T10 forged-env production+re-run → caught, class inherited
by I8's per-variant flags; D5/D6/D7/D8 byte-exact transcripts → evidence for
T10/T8/T9, no new fixture classes; M-inert → control proving byte-identity
collateral, not a seat patch.

## Hygiene

- Writes: this receipt + `ScoutDefeatsSpec.txt` only (both in
  `.ufo/waves/round-41/wave1/`). No lane tracked file, no fleet-root file, no
  source-tree write, no PATH-dir write, no `~/.omp` write.
- Git: read-only only (no mutating git/jj anywhere; no fixture repo built).
- Tools: none installed/upgraded (none needed); pacman untouched (paused
  host-wide per operator directive); no network fetches.
- Disk guard: not needed for this read-and-write pass (no heavy pass run).
- Scratch `S=/fast/scratch/hyaku/kasegi-r41/ScoutDefeatsSpec`: created at
  start, used as cwd for verification commands, **removed before yield**
  (`rm -rf` executed after the deliverable/receipt landed in the wave dir) —
  no `kasegi-r41*` scratch sibling survives from this seat at filing.

Report: `.ufo/waves/round-41/wave1/ScoutDefeatsSpec.md` (this file).
Deliverable: `.ufo/waves/round-41/wave1/ScoutDefeatsSpec.txt`.
