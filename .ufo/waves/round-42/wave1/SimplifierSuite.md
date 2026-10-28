# SimplifierSuite — YAGNI review of the r42 J1–J13 design

Seat `SimplifierSuite`, round 42, lane `kasegi-shokunin`, lane HEAD `0566bd66e93d429b2df8b6751cf10cbdc391e79b`, base `5053a7f46de35784cff4b56756906e9014a38276`. Receipt-only seat: no lane/suite edit, no deliverable other than this file. Frozen claims read and not edited (`.ufo/waves/round-42/claims.json`).

Review basis: the suite `corpus/instruments/r42-closure.sh` does not exist yet (wave-1 executors are authoring it). The reviewable surface at freeze time is (a) the frozen C1 predicate, (b) the thirteen dispatched per-check specs in `.ufo/waves/round-42/wave1-spec.json` (items `ExecSuiteCore`, `ExecReplayHarness`, `ExecJ1Evidence`…`ExecJ12J13`), (c) the r41 harness the r42 suite is told to reuse verbatim (`corpus/instruments/r41-closure.sh`, 2209 lines), and (d) the committed defeat artifacts in `.ufo/waves/round-41/wave2/`. Every line citation below is to (c), because that is the code the r42 checks will be derived from; re-check R1/R2/R3/R7 once the suite lands.

## Verdict

The design is *mostly* already lean: the r41 harness has **no dead functions and no dead payload fields** (proved below), and the r42 split of r41's overloaded `I12` into `J12`/`J13` is the right decomposition. Four things are not lean and one thing cannot go green as written:

1. **J5 / J13 / J10 are one scratch scanner with three names.** J13's two limbs are the two limbs of J5 and J8. This is the overlap the seat asked about: **yes, J5 and J13 overlap, and J13 additionally duplicates J8's `diff-clean`.** Fix by composition, not by new code.
2. **J9's `closed<13/13` gate is vacuous.** Any recursive negative control that suppresses its own recursion satisfies `closed<N/N` by construction. The load-bearing clause is the *tree-dependent* red set, which the dispatch omits.
3. **J1's dispatch prose is over-broad and would red on the live corpus** (12 of 16 correction lines name none of the evidence). The frozen predicate is correct if scoped to the *overclaim-grading* correction subset.
4. **J11's dispatched rule is self-contradictory** (count==1 per body vs "green over a copy with only the marker appended"); the live duplication is real and append-only-safe only under a waiver rule.
5. **F-TOKEN is still open in the shared primitive**: r41 `value_present` accepts `closed=7/8/9` and `failures=1/2`. Tested patch in R2.

Net deletion available without any behavior loss: the `i2_fixture` twin block (17 lines), `check_i5`'s vestigial subshell (8 lines), `check_i1`'s union accumulator, two cross-case selftest mutants, and J13's clone. That is the whole delta this seat recommends — nothing is removed whose invariant is not still gated somewhere.

## Evidence (commands actually run, output as printed)

Scan/family reproduction (r41 primitives extracted verbatim, fixture built in seat scratch):

```
$ bash scan.sh
--- r41 family (kasegi-r41 literal):            strays=1,read=ok,scanned=1
--- r41 family over parent (outside-root):      strays=1,read=ok,scanned=1
--- r42 fixed family over root:                 strays=2,read=ok,scanned=2
--- r42 fixed family over parent (outside-root):strays=3,read=ok,scanned=3
```

Fixture was `root/kasegi-r41/SeatX`, `root/kasegi-r42-OtherSeat`, parent-level `kasegi_r42_outside_probe`. So r41's `family_match` (`^kasegi-r41`, lines 601–610) misses the r42 sibling *and* misses the undo-scored `kasegi_r42_outside_probe`; changing the match to `kasegi-r4[0-9]` (`family_name` already collapses `_` to `-`) finds both. This is the F-SCAN routed defect, reproduced at 1 line of fix.

F-TOKEN probe against r41 `value_present` (lines 443–461) and against the tightened class:

```
MATCH   closed=7/8 exit=1        MATCH   closed=7/8 exit=1
REJECT  closed=7/80 exit=1       REJECT  closed=7/80 exit=1
MATCH   closed=7/8/9     <--     REJECT  closed=7/8/9
MATCH   failures=1/2     <--     REJECT  failures=1/2
MATCH   failures=1               MATCH   failures=1
REJECT  failures=10              REJECT  failures=10
REJECT  xclosed=7/8              REJECT  xclosed=7/8
MATCH   | `closed=7/8` |         MATCH   | `closed=7/8` |
```

Left column = r41 as committed; right = same function with `before != "/"` and `after != "/"` added to the boundary test. The frozen J2 text ("bounded by non-digit, non-slash characters") is met by the right column and violated by the left. `/` is in `[[:punct:]]`, which is why the left column accepts it.

F-EVID union mutant (scratch copy of `SCORECARD.md` with the three evidence ids stripped from the *second* qualified correction, line 1607):

```
qualified lines at: [1602, 1607]
mutated line 1607 : Correction (round 41): round-40 C1 is not verified on the frozen counter (NOT verified), because the ...
union evidence=3/3 -> r41 verdict: GREEN-accepts-defeat
min per-correction evidence=0/3 -> r42 verdict: RED-rejects-defeat
```

Pristine corpus, same two computations: every qualified line is `ev=3/3`, so the per-correction rule is green on the live state and red only on the defeat. Qualified subset (r41 `qualified_corrections` filters, applied directly): `SCORECARD.md` 2 lines (1602, 1607 — the duplicate), `LOG.md` 1 (1736), `SHONEN.md` 1 (221). The other 12 `Correction (round …)` lines in those three files name **0/3** evidence ids, because they grade other overclaims (scores, selftest quotes, forward-looking statements).

J11 live duplication:

```
$ sed -n '1602,1605p' SCORECARD.md > a.txt; sed -n '1607,1610p' SCORECARD.md > b.txt
IDENTICAL (D-r41-1 persists at head);  sha256(a.txt)=95632a3fcce7e5bb5304b3e873e62ab579129d145ee16322c057c95eddbce4b5
```

Registry (J3) live defects, `SKILL.md`:

```
1119: | name | ... |            (header)
1120: |---|---|---|...|         (separator)
1121: (blank)                    <-- r40 D6: table split from its row
1122: | r40-closure.sh | ... |
1126: | name | ... |            (round-41 header)
1127: |---|---|---|...|
1128: | r40-closure.sh | ... |  <-- duplicate basename
1129: | r41-closure.sh | ... |
```

Strict-parser probe (proposed rule) over the two MutSkillTablePipes survivors, using the real separator (10 fields) and the real r41 row:

```
canonical                cells=10  sep=10  firstcell=[ r41-closure.sh ]   strict_ok=1
bare-internal-pipe       cells=11  sep=10  firstcell=[ r41-closure.sh ]   strict_ok=0
leading-whitespace-cell  cells=10  sep=10  firstcell=[  r41-closure.sh ]  strict_ok=0
```

J8 twin-block proof (`i2_fixture`, lines 1972–2014): the two emitted blocks are 18 lines each and identical at 17 of 18 positions; the only difference is `I2) printf 'I2 payload=pending closed=1\n'` vs `I2) printf 'I2 payload=%s,cmp=1,i2-line=1 closed=1\n' "$canon"`.

Density (J12 constant) verified, not assumed:

```
worktree corpus/instruments/density.py : ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710
base 5053a7f:corpus/instruments/density.py : ee803726...54710
r41 head 1f74646:corpus/instruments/density.py : ee803726...54710
```

Dead-code survey (all `^name()` defs, references counted; the only zero-ref hits were `check_i1..i12`, `selftest_case_i1..i12`, `i11_probe_f1..f8`, all reached indirectly via `run_check "check_${id,,}"`, `"selftest_case_${id,,}"`, `i11_probe_f${n}`). `payload_closed` used at 2025/2034/2078; `closed-0` used at 1263; `worktree_state` at 1500; `worktree_markers` at 1577; `pending_scan` at 1479/1519; `erratum_block` at 1026. **No dead function, no dead field. Nothing to delete at that layer.**

## Duplication map (one invariant, one authority)

| invariant | primary | second authority today | verdict |
|---|---|---|---|
| scratch namespace has no leftover | J5 (scan) | J13 (live scan) | **DUPLICATE** — must share `scan_scratch` |
| scratch gains no foreign entry during a run | J13 | J5 live limb | **DUPLICATE** — keep the scan in one place |
| per-case fixture isolation | J10 (before/after delta) | J5 (same walker) | **SHARED PRIMITIVE** — one `scratch_delta` |
| export equals the ref its receipt names | J8 (`ancestor`, `diff-clean`) | J13 ("clone of the exported ref is clean") | **DUPLICATE + vacuous** — delete the clone |
| declared-path validity / canonical root | J4 | — (r41 `I12` recomputed it; the split removed it) | **OK** — keep the split |
| no tracked corpus deletion | J12 | J4 (`pure=1` over declared tails) | distinct scopes; keep both, do not re-export `pure` into J12 |
| tally read as a bounded token | J2 | J9 (nested `closed=` parse) | **DUPLICATE parser** — one primitive |
| recorded payload equals re-derived payload | J8 (exact string compare) | J2 (token boundary) | distinct *if* J8 keeps exact equality |
| correction uniqueness | J11 | J1 (correction grading) | distinct predicates, same lines — see F1/F4 |
| registry table integrity | J3 | — | OK |
| negative control is red | J9 | — (r42 correctly dropped r41 `I12`'s `neg-red` re-read) | OK |

The r41 `I12` recomputation (`declared_blocks_check` again at 1533, `neg_accept` again, `payload_get I10` at 1585) is the duplication the r42 split already removes. Preserve that removal: **J12 must not re-read J4's payload or J9's verdict.**

## Recommendations (each states what is removed, the invariant that survives, and who still verifies it)

**R1 — J1: delete the union accumulator; scope to the overclaim-grading subset.** r41 `check_i1` (891–914) accumulates `seen` across lines (895, 903, 905) and gates on `ev=3` (911), so one correction can carry the evidence for another. Replace with: `qualified(f)` = the existing `qualified_corrections` filter (which is already correct); require `|qualified(f)| >= 1` per record, and for **each line** in `qualified(f)` require all `EVIDENCE` ids present. Delete `seen`, delete the cross-record `ev`. Payload: `records=3,lines=16,qualified=4,graded=4,evidence-min=3,missing=0`. *Survives:* the F-EVID defect is rejected (proved above, 3/3 union-green → 0/3 per-correction-red). *Do not* apply the test to every `Correction` line: 12 of 16 name no evidence and would red the live corpus (F1).

**R2 — J2/J9: one token primitive, slash excluded from the boundary class.** In `value_present` (443–461) change the two boundary predicates to `(before ~ /[[:space:][:punct:]]/ && before != "/")` and the same for `after`. Use it for J1's tally quotes, J2's record bodies, and J9's nested `closed=` parse; delete J9's ad-hoc `case $last in closed=*'/12'*` glob (r41 1366–1373), which also accepts `closed=10/12x`. *Survives:* every existing acceptance (canonical, backticked, sentence-embedded) — proved in the probe above; the two new rejections are exactly the frozen J2 text. This is a correctness fix, not a style preference: without it the kill rule's F-TOKEN limb fires on `closed=7/8/9`.

**R3 — J3: strict row identity, delete the trim and the cell-count tolerance.** `registry_row_state` (1156–1195) trims the first cell with `gsub` and accepts `nf >= 8`, which is why both MutSkillTablePipes survivors pass. Replace with (i) `nf == header_nf` (header_nf from the separator line) and (ii) literal first-cell equality against `" <name> "` or `` " `name` " ``. Delete the `gsub`. *Survives:* the canonical row; adds the two survivor rejections (proved). The blank-line and duplicate-basename limbs are separate and already correct.

**R4 — J4: one-line delegate; and implement "coverage" as changed-set ⊇ declared, not read interception.** `check_i5` (1118–1126) opens a subshell, `cd`s to the export, and then passes the absolute `$tree` to `declared_blocks_check`, which never uses the cwd. Delete the subshell and the `cd`: `check_j4() { declared_blocks_check "$1" "$2" "${R42_DECLARED:-$DECLARED}"; }`. Separately, the dispatch's "a read path not in the declaration is rejected" is not implementable without read interception; `CritDeclarationCoverage.md` §"Smallest safe correction" already names the implementable form: compare `git diff --name-only BASE REF` against the declared path set. Use that, with an explicit declared exclusion list (the declaration file itself — self-reference — the receipt path, the suite path, the wave dir). *Survives:* all of r41's `I5` validity clauses; adds the coverage gap CritDeclarationCoverage found.

**R5 — J5/J13: one scanner, three call sites; delete J13's clone.** Keep `scan_scratch` (636–675) as the only walker and call it in three places: J5 live (declared root, `$WORK` exempt), J5 fixture (materialized parent tree, outside-root stray), J13 post-run (declared root again — catches a *leak* that a pre-run scan cannot, which is J13's only distinct observable). J13's "no uncommitted changes in a clone of the exported ref" is vacuous — a fresh clone is clean by construction and the meaningful statement is J8's `diff-clean` (`git diff --name-only <receipt-ref> <export-ref>` names only the receipt) — so delete the clone (it also costs a full tree copy per run). If a live lane-side-effect limb is wanted, make it `find "$EXPORT" -newer <run-stamp>` (no writes into the export) plus `git status --porcelain` minus the declared `--receipt-out` path, and grade the planted-write fixture, not the structurally-clean clone. *Survives:* quiescence is still gated, on the side effects the run can actually cause. Note `family_match` must widen to `kasegi-r4[0-9]` (proved) or J5 ships the routed defect.

**R6 — J10: call `run_check`, not the suite entrypoint.** The dispatch says each case "invokes the suite entrypoint"; with 13 cases that is 13 full nested suite runs, each of which runs J9's two nested exports — cubic. r41's `st_pos`/`st_neg` (1622–1653) already call `run_check "$id" "$tree" "$ref"` on a private `fixture_tree` dir, and `st_neg`'s `[ "$out" != "$pos" ]` is the isolation assertion that a check reading shared state cannot pass. Keep that; J10's only addition is the per-case scratch delta, which is R5's primitive. *Survives:* per-case isolation, already structurally enforced, now with the leak assertion.

**R7 — J8: collapse the `i2_fixture` twin block into one parameterised emitter.** The two 18-line blocks (1972–2014) differ in exactly one line. `emit_receipt() { local i2=$1; … printf 'I2 payload=%s closed=1\n' "$i2"; … }` called as `emit_receipt pending` then `emit_receipt "$canon,cmp=1,i2-line=1"` produces byte-identical output. −17 lines, one convention instead of two.

**R8 — J9: report the tally, gate on the tree-dependent reds.** The nested run must suppress J9 to terminate, so its tally is at most 12/13 *whatever the tree contains*. `closed<13/13` therefore cannot fail. r41's `neg_accept` (1334–1348) is the actual safeguard: `k < N`, `exit==1`, and the tree-dependent checks red in the nested run. Carry that: J9's payload must carry the nested per-check lines and require the tree-dependent set red (J1 corrections, J4 declarations, J8 receipt) plus the distinct `ref-not-found` red. *Survives:* the kill rule's clause (that is an observable on the external run, not on a check ID) and the control becomes falsifiable.

**R9 — J11: waiver rule, no rewrite, count only the current round.** The dispatch asks for "count==1 per distinct body" *and* "green over a scratch copy with the dedup marker appended" while the duplicates remain — both cannot hold. Implement: `unwaived = duplicate bodies not named by the `Correction-dedup (round 42)` block`; closed = `unwaived == 0 && marker == 1 && the marker names every duplicate body`; payload `dups=<n>,dup-historical=<n>,dup-new=<n>,waived=<n>,unwaived=<n>,marker=1`. Name duplicates by content hash of the normalized body, never by line number (line numbers move on the next append). *Survives:* D-r41-1 stays visible and named in every payload; history is not rewritten; no new duplication can pass. The marker spelling `Correction-dedup (round 42)` deliberately does not match `^Correction \(round \d+\)`, so it never pollutes J1's correction set — keep that spelling.

**R10 — J12: carry only its own two limbs.** J12's frozen text is deletions + density. Do not inherit r41 `I12`'s `census`, `declared` (J4's), `neg-red` (J9's), `skill-del`/`province-del`, or its three-mutant selftest case (1899–1921). In particular **do not** add a no-deletion guard on `SKILL.md`: J3's repair deletes the blank line at 1121 and the duplicate row at 1128, so a `skill-del=0` limb would make J3 and J12 mutually unsatisfiable. `PROVINCE.md`'s F25 amendment is an append, so no conflict there.

## Falsifiers of the freeze (decide before the suite lands; each is a red at Y as designed)

- **F1 (J1 scope).** Dispatched prose "EACH correction individually must grade the named overclaim" is unsatisfiable: 12 of 16 live correction lines name 0/3 evidence ids. Use the frozen predicate's scoping (the overclaim-grading subset) per R1.
- **F2 (J11 contradiction).** `count==1` per body and "green with only the marker appended" cannot both hold while the 4 duplicated round-41 blocks remain (proved byte-identical). R9's waiver is the only append-only-compatible reading.
- **F3 (F-TOKEN residual).** `value_present` accepts `closed=7/8/9` and `failures=1/2` today. If J2 inherits it unchanged, the current suite bytes accept an in-family input and the C1 kill rule's F-TOKEN clause fires. R2's patch is one condition per side.
- **F4 (J9 vacuity).** `closed<13/13` is guaranteed by the recursion guard, independent of base-tree defects. The control's verification content is entirely in the tree-dependent reds; omit them and J9 gates nothing.
- **F5 (J13 vacuity/duplication).** A clone of an exported ref is clean by construction; the real statement (Y = J + receipt) is J8's `diff-clean`/`ancestor`. J13's remaining distinct content is the post-run leak scan (R5).
- **F6 (J10 cost).** Entrypoint-per-case nests the full suite 13×, each nesting J9's two exports. Use `run_check` (R6).
- **F7 (J3 ↔ SKILL.md deletions).** J3's repair *requires* deleting `SKILL.md` lines; any inherited `skill-del=0` limb reds J3. R10.
- **F8 (J4 read-path ambiguity).** "Every path a check reads" needs read interception or a declared exclusion list; use changed-set coverage with the self-reference exclusion (R4) or J4 will either be unimplementable or red on the declaration file itself.

## Do not simplify (load-bearing, keep exactly as is)

- `chain_clean`'s ancestor exemption (612–634) and the family-symlink rejection — the round-40 wave-2 F5 escape.
- The two-root scan split (live root vs materialized parent). Scanning the real parent at receipt time picks up sibling seats; scanning only the root misses the outside-root stray. Both roots, one function.
- `payload_match_ids`/`payload_match_count` exact-string comparison (746–825). Exact equality is why J8 does not need J2's token primitive.
- `st_neg`'s `[ "$out" != "$pos" ]` guard. It is the isolation proof; a case that ignores its fixture and reads shared state passes without it.
- J9's `neg_accept` probes (`12/12` rejected, `i1/i2/i7` red rejected, `3/12` accepted). That trio is what proves the acceptance predicate is killable — carry it, in J9 and in the r42 selftest.
- J12's density constant — verified `ee803726…54710` at worktree, base and r41 head.

## Weakest inherited defeat form (note, not a removal)

r41's failure-injection switches (`R41_ISOLATE_BREAK=1` at 769, `R41_NEG_WEAK=1` at 1339, `R41_FORGE_DISABLE`, `R41_I11_BREAK`) are defeats that prove a check honours its own break switch, not that it rejects a real artifact. The r42 REPLAY limbs fix this for J1–J7 (real committed artifacts); J8–J11 still inherit the switch style. Where a real fixture is cheap (J10's private-dir leak, J11's duplicated block) use the fixture; keep the switch only as a second probe.

## Attestation

Disk guard run before any probe: `/fast/scratch/hyaku` 27% use, 592.6G free (green). Tools installed: none. Network fetches: none. Mutating git/jj: none anywhere; no fixture repo was created (the one behavioural proof used plain files in seat scratch). Lane writes: none — `git status --porcelain` after the review shows only sibling seats' untracked wave-1 deliverables (`.ufo/waves/round-42/wave1/*`, `build-wave2-spec.py`, the two `kasegi-r42-build.ready*` markers); no tracked file is modified and no corpus path is touched. All scratch under `/fast/scratch/hyaku/kasegi-r42/SimplifierSuite/` was removed before filing.
