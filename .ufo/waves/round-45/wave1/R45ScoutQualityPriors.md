VERDICT: INFO

Prior art for the four freeze-hygiene classes named in `corpus/lessons/round-44-verifier-spotcheck.md:80` (the three sentences the round-45 counter will require as R47, R48, R49 at `corpus/instruments/r45-routed-defects.py:16-21` and `:143-147`). Reading scope: `corpus/lessons/round-41.md`, `round-41-verifier-spotcheck.md`, `round-42.md`, `round-42-verifier-spotcheck.md`, `round-43.md`, `round-43-verifier-spotcheck.md`, `round-44.md`, `round-44-verifier-spotcheck.md`, and `corpus/QUALITY.md` R38–R46, plus the earlier rows and instruments those lessons cite. "Gate today" means a `SKILL.md` Gates & probes row under the exact basename (R29, `corpus/QUALITY.md:264`) whose instrument executes the property. A criterion sentence, a lesson practice, an `corpus/instruments/README.md` counter row, or a check that only greps for the criterion's words is not that.

No language server is mounted (`xd://lsp` is not a device). Citations below are file reads and the re-runs quoted in each section.

## (a) Frozen counters replayed at base

The class, as mined: the frozen counter string is re-executed on the base before data, and a string that cannot separate base from the after target is fixed then (`corpus/lessons/round-44.md:15` M44-3, `:107-115`, `:126` M44-8; `corpus/lessons/round-44-verifier-spotcheck.md:40`, `:47`, `:80`, `:82`).

Neighbours, not this class:

| id | path:line | what it actually requires | gate today |
|---|---|---|---|
| R22 | `corpus/QUALITY.md:226` | Every literal and regex in the frozen predicate is run against the base tree; an unsatisfiable literal is fixed before data. | No. The only check that names it is `check_r2` in `corpus/instruments/r-defect-closure.sh:160-179`, which greps the R22 row for `satisfiab` and `before freeze\|pre-freeze`. Registered at `SKILL.md:1098`. It does not run a counter. |
| R25 | `corpus/QUALITY.md:229` | A literal true at base and false at the declared after-adds is fixed before data. Grounding is `records=40` vs `records=41`, not a counter replay. | No instrument reads `claims.json` and runs its counter. `corpus/instruments/freeze-check.py` is the name `corpus/instruments/r45-routed-defects.py:210-222` calls; the file is absent (command below). |
| R26 | `corpus/QUALITY.md:249` | Corrects R22's grounded-in citation. The row says R22's criterion is unchanged. | Same as R22. |
| R34 | `corpus/QUALITY.md:307` | A frozen counting command is dry-run over a stand-in head (judged head plus the receipt) before freeze. | `corpus/instruments/r39-closure.sh` G2, registered at `SKILL.md:1116`. The object is the round-39 receipt-in-export paradox (`corpus/instruments/r39-closure.sh:58-69`), not an arbitrary counter on the base tree. |
| R38 | `corpus/QUALITY.md:337` | A grading record says verified only after the kill rule is re-derived, and a correction grades the claim not verified on the frozen counter. | `corpus/instruments/r41-closure.sh` I1, registered at `SKILL.md:1128`. This grades records after the fact. It does not replay the counter at base before freeze. |
| R43 | `corpus/QUALITY.md:369` | A frozen `before` cell's literal must be what its cited control printed. | K17, below under (b). It compares stored tokens. It does not execute the counter. |

`corpus/instruments/r44-frontier-count.py:5-21` and `:44-60` measures the declared predicate (status is the third cell). It does not run the frozen regex. `grep -c -F selftest` on that file printed `0`. It is absent from `SKILL.md` and from `corpus/instruments/README.md` (commands below). The spot-check already calls it a probe, not a gate (`corpus/lessons/round-44-verifier-spotcheck.md:47`).

Re-run of the frozen string `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` and of `r44-frontier-count.py --expect 26`, same predicate, two trees. Base is round-44 open `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` (`corpus/lessons/round-44.md:3`), extracted with `git show` of `corpus/README.md` only (that is the only file either command reads).

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --verify 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a^{commit}
5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a
=== frozen regex at round-44 base ===
0
base_grep_exit=1
=== r44-frontier-count --expect 26 at round-44 base ===
frontier rows=25 admitted=25
frontier expected=26 admitted=25 verdict=SHORT exit=1
base_frontier_exit=1
```

Current lane tree (the admission is already in it):

```
=== frozen C2 regex on current tree ===
0
grep_exit=1
=== r44-frontier-count on current tree ===
frontier rows=26 admitted=26
frontier_exit=0
```

The frozen string prints 0 on the base and 0 after the admission. The table-aware probe prints 25 then 26. R22's "run the regex at base" is satisfied by a command that exits having printed 0; that does not catch a string that also prints 0 after. The committed hand replay agrees (`.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt:1-11` records base `0/68/62` and worktree `0/70/63`, and the sentence "The F-count result is 0 in both states"). Nothing in `SKILL.md` fails a freeze for that pair.

```
ls -l .../corpus/instruments/freeze-check.py
ls: cannot access '/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/freeze-check.py': No such file or directory
grep -n -E 'r44-frontier-count\.py|r44-routed-defects\.py|freeze-check\.py' .../SKILL.md
exit=1
grep -n -E 'r44-frontier-count\.py|freeze-check\.py' .../corpus/instruments/README.md
exit=1
```

Gate today: no.

R47 must not be a restatement of R22, R25, R34, R38, or R43. The uncovered residue is: re-execute the frozen counter string on the do-nothing base and refuse the freeze when that same string already fails to reach the declared after target. `enforced-by` must not be `r-defect-closure.sh`, `r39-closure.sh`, `r41-closure.sh`, `r43-closure.sh`, or `r44-frontier-count.py`. `corpus/instruments/r45-routed-defects.py:172-177` accepts any `enforced-by` path that exists, so pointing at one of those files would pass limb R2 without adding this check. `freeze-check.py` is not prior art; it is absent.

## (b) Do-nothing controls

The string `do-nothing` occurs once in `corpus/QUALITY.md`:

```
grep -c -F 'do-nothing' .../corpus/QUALITY.md
1
grep -n -F 'do-nothing' .../corpus/QUALITY.md
369:| R43 | A committed record that reports a run — ...
```

That occurrence is the r43 mine inside R43: the before cell said `closed=10/12 exit=1` and `.ufo/waves/round-42/c1-controls/do-nothing.txt:16` printed `closed=8/12 exit=1` (`corpus/QUALITY.md:369`). R43 does not require a do-nothing control to exist.

The practice is lesson text, not a criterion: `corpus/lessons/round-41-verifier-spotcheck.md:54-57` (suite absent, exit 127), `corpus/lessons/round-41.md:23`, `corpus/lessons/round-43.md:26`, `:33`, `:44` (M43-1), `corpus/lessons/round-44.md:114-116` and `:126`.

K17 (`corpus/instruments/r43-limbs/k17-claims-before.sh:1-12`, `:28-49`) is the gate that touches controls. It is wired at `corpus/instruments/r43-closure.sh:285` and `:293` and registered at `SKILL.md:1143`. It grades `before` tokens of `closed=`, `failures=`, and `cases=` only when the claim cites a receipt (`:37-41`). `after` tokens are not graded (`:43-49`). A do-nothing receipt that prints `0` and a before cell that quotes `0` satisfies K17 while the frozen string still cannot reach the after target. That is the discrimination: K17 binds the quoted token to the file; it does not require the control to be a do-nothing tree, and it does not re-run the counter.

`corpus/instruments/kill-rule-check.py:79` and `:600` take the newest `.ufo/waves/round-*/c1-controls/` fake runner as `CTL-fake`. Registered at `SKILL.md:1099`. The default instrument under test is `capture-binding-check.py`. That is one probe's degenerate control, not a rule that every freeze ships a do-nothing replay.

`corpus/instruments/r44-frontier-count.py:19-21` says a do-nothing control cannot reach 26. The base re-run above printed `verdict=SHORT exit=1`. The file is not a SKILL gate (section (a)).

Gate today: partial, and only for K17's token binding when a receipt is cited. Nothing requires a do-nothing control before data, and nothing fails the freeze when the frozen string is green, or equally blind, on that control.

R47's "do-nothing" half must not be copied from K17 or from `kill-rule-check.py`. The residue is the control itself: the frozen string is run on a tree where the round's change is absent, and that run is red against the after target, before the claim is frozen.

## (c) Presence-only predicates

The class: a predicate greens on a marker, a denial, a stub, or a fabricated tree (`corpus/lessons/round-44.md:16` M44-4, `:125` M44-7, `:165-167`, `:189` M44-10; `corpus/lessons/round-44-verifier-spotcheck.md:80`).

```
grep -c -F 'presence-only' .../corpus/QUALITY.md
0
grep -c -F 'M44-' .../corpus/QUALITY.md
0
```

The spot-check's own count is the same shape: `grep -c M44 corpus/QUALITY.md` → 0 (`corpus/lessons/round-44-verifier-spotcheck.md:75`).

Neighbours, not this class:

| id | path:line | what it actually requires | gate today |
|---|---|---|---|
| R24 | `corpus/QUALITY.md:228` | One `selftest case=<name>` line per case, `cases>=11`, so a summary-only `cases=0 failures=0` cannot pass. | The row is the round-34 kill-rule tightening. It does not reject a denial string or a fabricated tree. |
| R40 | `corpus/QUALITY.md:352` | Evidence is per correction. A `grep -c` over the union of lines is not per-correction evidence. | `corpus/instruments/r42-closure.sh` J1 and J11, registered at `SKILL.md:1134`. Grades correction blocks. |
| R42 | `corpus/QUALITY.md:354` | The selftest mutant is the committed defeat shape, executed and rejected. A stand-in mutant leaves the check unrepaired. | Same suite's REPLAY limbs, `SKILL.md:1134`. The mutant has to be the filed defeat. A predicate that accepts the token "not planner=L1", or a fabricated file that contains the token, is a different shape. |

`corpus/instruments/r44-routed-defects.py:12-20` and `:22-55` is the instrument that rejects marker-only evidence, denials, and a `FABRICATED-ARTIFACTS` tree for the eight round-43 defects. `corpus/instruments/README.md:992` registers it as type `counter`. It is not in `SKILL.md` (the combined grep in section (a) exited 1). Under R29 (`corpus/QUALITY.md:264`) the registry home is `SKILL.md`. It covers those eight limbs. It does not scan a new predicate.

Limb R2 of the round-45 counter is itself presence-only about the new rows: `corpus/instruments/r45-routed-defects.py:150-177` requires the strings `do-nothing`, `before data`, `presence-only`, `capture method`, and `reject`, a grounding path, and an `enforced-by` path that exists on disk. It does not run that path.

Gate today: no, for any predicate outside the eight round-44 limbs.

R48 must not restate R24, R40, or R42, and `enforced-by` must not be `r44-routed-defects.py` or `r42-closure.sh`. Those paths exist, so limb R2 would accept them, and neither fails the next marker-only or denial predicate.

## (d) Capture-method parity

The class: the method used to open the admit is the method used to open the reject (`corpus/lessons/round-44-verifier-spotcheck.md:64-66`, `:75`, `:79-80`). S069 was pinned through the article API (`corpus/lessons/round-44.md:24`, `:130`). S070 was rejected because "the accessible body is a JavaScript shell" (`corpus/lessons/round-44.md:22`, `:131`; `corpus/SOURCES.md:76`).

```
grep -c -F 'capture method' .../corpus/QUALITY.md
0
```

Re-read of the round-44 manifest and the missing reject capture:

```
ids ['S069']
S069 url https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules
S069 capture_url https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules
S069 final_url https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules
equal_capture_final True
url_eq_capture False
ls .../corpus/source-snapshots/round-44/S070.txt
ls: cannot access '.../corpus/source-snapshots/round-44/S070.txt': No such file or directory
```

`url` is the HTML page. `capture_url` and `http.final_url` are the article API and they match each other. The manifest has no S070 record, and there is no `S070.txt`.

Neighbours, not this class:

| instrument | path:line | what it actually requires | gate today |
|---|---|---|---|
| capture-binding E3 | `corpus/instruments/capture-binding-check.py:119-125` | On one record, `capture_url` and `http.final_url` are byte-identical when both are present, and `final_url` is the record `url` or `capture_url`. | Yes. `SKILL.md:1077` (`gate\|probe`). S069 already passes E3 (`equal_capture_final True`) while the page URL and the capture URL differ. E3 never looks at a second source. |
| capture-binding B3 | `corpus/instruments/capture-binding-check.py:44-47` | A row whose status is `rejected` cannot anchor a manifest record (`FAIL rule=rejected-row-anchor`). | Same gate. A capture record bound to S070 would fail this check. |
| source-recheck | `SKILL.md:1055` | sha256 and located quotes inside a manifest record that exists. | Yes, for records that exist. S070 is not in the manifest, so the gate does not see the reject. |
| R20, R21 | `corpus/QUALITY.md:169`, `:170` | A snapshot ships a manifest; provenance separates a fabricated capture from a real one. | The binding gate above. Both rows are about an admitted capture's manifest, not about how a reject was opened. |

Rounds 42 and 43 did open their rejects and quote them (`corpus/lessons/round-42.md:118-122` S065; `corpus/lessons/round-43.md:110-125` S068). That is lesson practice. Neither lesson states a criterion that the reject's fetch method equals the admit's, and no instrument compares two sources' methods. Round 41's gate section (`corpus/lessons/round-41.md:39-70`) records the S063 admit and has no reject subsection before `## Wave-2 falsification` at `:72`.

Gate today: no.

R49 must not require a manifest record on the rejected row: B3 (`capture-binding-check.py:44-47`) forbids that anchor. It must not cite E3 or `source-recheck.py` as the enforcement. Those check one admitted record's internal URL agreement and its pinned quotes. The residue is the opening: the reject is read by the same method as the admit (here the article API that made S069 quotable, `corpus/lessons/round-44-verifier-spotcheck.md:66`), and the stated reason is about the body that method returned.

## What R47–R49 would duplicate if copied

The spot-check asked for three criteria (`corpus/lessons/round-44-verifier-spotcheck.md:80`). The counter splits the first sentence across the needles `do-nothing` and `before data` (R47) and keeps the other two as R48 and R49 (`corpus/instruments/r45-routed-defects.py:143-147`). None of the three classes is enforced by a gate today. Each has a neighbour that will look like coverage and will satisfy limb R2's path-exists check:

- R47 duplicates R22/R25/R34/R43 if it only says "run literals at base" or "the before cell matches the cited control." The gap those rows leave is the one the re-run shows: frozen regex `0` at base and `0` on the current tree, table-aware count `25` then `26`.
- R48 duplicates R40/R42/R24, or the round-44 counter, if it only restates per-correction evidence, defeat-shaped mutants, or the eight already-pinned limbs.
- R49 duplicates E3/B3/`source-recheck.py` if it only restates single-record URL agreement or asks for a capture bound to the rejected row.

`grep -c` on `corpus/QUALITY.md` printed `0` for `R47`, `R48`, and `R49`. The rows are not landed. This scout did not add them.

## Limitations

- K17, `check_r2`, `r39-closure.sh` G2, `r42-closure.sh`, and `capture-binding-check.py` were read, not executed. Their export-mode drivers can write a receipt; this seat does not write one. The "gate today" judgments are the source plus the `SKILL.md` row, not a live suite run.
- The base replay is `git show 5ab3a60:corpus/README.md` into a scratch directory, not a full `git archive` of that commit. Both commands read only that file (`corpus/instruments/r44-frontier-count.py:45`).
- The round-45 frozen base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` was not the replay target. The 0/0 defect is about the round-44 counter and the round-44 base named in `corpus/lessons/round-44.md:3`.
- `grep -c` exits 1 when the count is 0. The `0` lines above are the counts; `grep_exit=1` and `base_grep_exit=1` are that exit, not a second count.
- Scratch `/fast/scratch/hyaku/kasegi-r45/R45ScoutQualityPriors` held the README extract. The shell EXIT trap did not remove it. A later `rm -rf` of that directory did; `ls -d` of it then printed `No such file or directory` (exit 2). No other scratch path was created.
- No lsp server was available, so these are textual citations, not resolver results.
