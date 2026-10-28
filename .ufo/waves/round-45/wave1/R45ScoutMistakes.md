VERDICT: BROKEN

Mistake-mining scout for `corpus/lessons/round-45.md` `## Mistakes`. Ranked by how cheap the red-before command is. Do-nothing control is the freeze commit `8cf62c879e6e6b031e67412f8fac1fba0bd378cf` exported with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 8cf62c879e6e6b031e67412f8fac1fba0bd378cf | tar -x -C /fast/scratch/hyaku/kasegi-r45/R45ScoutMistakes/freeze-8cf62c87` (baseline export `/fast/scratch/hyaku/kasegi-r45/L1/pure`, base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`). On that export the C1 counter matches the freeze control. The C2 count does not.

```
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1
c1-freeze-exit:1
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=0 read=F27-rows=0
gate G6 pass=0 read=knowledge=63
gate G7 pass=1 read=census-rc=0
c2-gate fixed=2/7 exit=1
c2-freeze-exit:1
```

Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r45-routed-defects.py --root /fast/scratch/hyaku/kasegi-r45/R45ScoutMistakes/freeze-8cf62c87 --baseline /fast/scratch/hyaku/kasegi-r45/L1/pure` and the same `--root` for `r45-c2-gate.py`. A second worktree run of `r45-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` printed the same `c2-gate fixed=2/7 exit=1`.

Recorded control (`.ufo/waves/round-45/controls/freeze-controls.txt:1-2`) and `claims.json:26`:

```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
```

`expect_before` for C2 is `c2-gate fixed=1/7 exit=1`. The re-run prints `fixed=2/7`.

## Candidates

### 1. landing · captured-by none

Ten M44 rows landed no QUALITY criterion, and the three classes §6.2 asks for are absent: do-nothing replay before data, presence-only predicates, capture-method parity for admit and reject.

Evidence: `corpus/lessons/round-44-verifier-spotcheck.md:75` (`grep -c M44 corpus/QUALITY.md` → 0; M44-2, M44-5, M44-9 name no catching criterion) and `:80`. Precedent for the grep shape is the R37 grounding at `corpus/QUALITY.md:323` (M39-2, `grep -c` → 0).

Command:

```
grep -c M44 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md
grep -cE '^\| R4[789] \|' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md
grep -nE 'presence-only|capture method' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md
```

Printed:

```
0
grep-c-M44-exit:1
0
grep-c-R47-exit:1
no-presence-only-or-capture-method
```

`grep -c` exits 1 when the count is 0. Freeze-export limb: `limb R2 fixed=0 read=quality-not-append-only-or-unchanged`.

Fix that fails: append `R47`/`R48`/`R49` grounded in `corpus/lessons/round-44.md` with an `enforced-by:` path (`corpus/instruments/r45-routed-defects.py:143-178`). Copying R22 (`corpus/QUALITY.md:226`) as R47 fails to name the round-44 shape. R22 requires each frozen regex to be run on the base tree. It does not require the base reading and the after reading to differ. The round-44 frozen command still prints 0 while the table-aware count prints 26:

```
grep -cE '^\| F[0-9]+ \| admitted \|' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md
0
frozen-grep-exit:1
python3 .../r44-frontier-count.py --root <lane>
frontier rows=26 admitted=26
frontier-count-exit:0
```

That both-worlds zero is already M44-8 (`corpus/lessons/round-44.md:126`). A new criterion that only restates R22 leaves it unnamed. M44-2's captured-by cell (`corpus/lessons/round-44.md:14`) cites a Q5 review; the recheck-form criterion is Q10 (`corpus/QUALITY.md:76`). That recheck was already moved, so it is not an open red.

### 2. reference-drift · captured-by R29

`corpus/QUALITY.md:264` (R29): an instrument is registered in `SKILL.md` § Gates & probes under its exact basename. `r44-frontier-count.py`, `r44-routed-defects.py` and `wave-registry.py` have no such row. `corpus/lessons/round-44-verifier-spotcheck.md:82`. Round-43 had the same pointer miss at `corpus/lessons/round-43-verifier-spotcheck.md:107` (defect 7). R42 (`corpus/QUALITY.md:354`) is the additional criterion for the missing selftest: a repaired check's selftest contains the committed defeat. `r44-frontier-count.py` has no `--selftest`. The duplicate-id branch at `corpus/instruments/r44-frontier-count.py:81-87` is an ungraded limb, not an R17 survivor: a repeated id returns exit 1, so the limb moves when the input changes. No selftest grades that move.

Command:

```
grep -cE '^\| *(r44-frontier-count\.py|r44-routed-defects\.py|wave-registry\.py) *\|' SKILL.md
grep -cF r44-frontier-count.py SKILL.md
grep -nE '^\| (r43-closure\.sh|claim-package-check\.py|r44-frontier-count\.py|r44-routed-defects\.py|wave-registry\.py) \|' corpus/instruments/README.md
python3 corpus/instruments/r44-frontier-count.py --selftest
```

Printed:

```
0
skill-row-exit:1
0
skill-fc-exit:1
990:| r43-closure.sh |
991:| claim-package-check.py |
992:| r44-routed-defects.py |
993:| wave-registry.py |
usage: r44-frontier-count.py [-h] --root ROOT [--expect EXPECT] [--ids]
r44-frontier-count.py: error: the following arguments are required: --root
frontier-selftest-exit:2
```

`r44-frontier-count.py` is absent from `corpus/instruments/README.md` as well (the four-row grep above has no line for it). Freeze-export limb: `limb R3 fixed=0 read=selftest-rc=2-tokens=None`.

Fix that fails: a README row alone leaves the R29 exact-basename grep at 0. A SKILL row without `--selftest` still exits 2 and fails R3 (`selftest-rc=2`).

Same commit `8063547d0ce647d6f9eafc3c8d0a502616685218` (2026-10-28 16:58:53 -0300) also planted a stale-premise sentence. `SKILL.md:1138`:

```
The round-43 report incorrectly named `corpus/instruments/README.md` as the registry for these instruments; that file exists but contains no matching rows.
```

`grep -cF r43-closure.sh corpus/instruments/README.md` printed `1` and `grep -cF claim-package-check.py` printed `1` (rows at `:990` and `:991`). `git log -1 -S` for the sentence and for `| r43-closure.sh |` is the same hash. Captured-by for that sentence: none (R29 requires the SKILL row; it does not grade this prose). A Round-45 registry section appended under R3 leaves line 1138 in place. `grep -n 'matching rows' SKILL.md` hits only `:1138`.

### 3. vacuous · captured-by none

The lesson's S070 flip is already true of the committed capture, and the JavaScript-shell reason is false of that same file. No QUALITY row requires the admit capture channel to be used for the reject (candidate 1). `corpus/lessons/round-44-verifier-spotcheck.md:66` and `:79`.

`corpus/lessons/round-44.md:131`:

```
the accessible body is a JavaScript shell and the metadata is a directory welcome with no quotable rule. Flip condition: a readable, dated copy of the rules directory that carries a quotable rule text.
```

The same shell sentence is at `corpus/lessons/round-44.md:22` and in `corpus/SOURCES.md:76` cell 6 (`REJECTED: the page's accessible body is a JavaScript shell...`). Cell 6's own flip is a different sentence: `flip: the page itself exposes a located, program-specific rule absent from the linked policy text.`

Committed capture `corpus/source-snapshots/round-45/S072.txt` (tracked; `git ls-files` lists it), manifest `fetched_utc` `2026-10-28T20:53:00Z`, `bytes` 10032, sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025` (`corpus/source-snapshots/round-45/manifest.json:57-59`). File lines 1-5 are prose (`Welcome to the VRP rules section!...`). Lines 148-149:

```
Security issues affecting any Google Cloud product or web service that
handles reasonably sensitive user data
```

`corpus/source-snapshots/round-44/S069.txt:10-11` already has `product or web service that handles reasonably sensitive user data is intended / to be in scope.` There is no `S070.txt` under `corpus/source-snapshots/round-44/` (`test -e` exit 1; directory listing is `S069.txt` and `manifest.json`). `grep -cE '^\| S072 \|' corpus/SOURCES.md` printed `0` (`s072-row-exit:1`). Freeze-export limb: `limb R1 fixed=0 read=row-S072=absent`.

Fix that fails: copying the lesson flip into a new row does not change a condition. S072.txt is already a readable dated copy with a quotable sentence, so that flip cannot go from false to true. Putting `wc -c` into the teaches cell also fails the counter: the limb requires the token `10 029` / `10029` / `10,029` (`corpus/instruments/r45-routed-defects.py:112`). Measured on `S072.txt`:

```
endswith_newline=True chars=10030 chars_rstrip_one=10029 bytes=10032
```

`wc -c` prints `10032`. The spotcheck's `10 029-char` figure matches the character length with the trailing newline removed. A cell that quotes only the byte count fails the token check. Rewriting the S070 row in place fails the same limb's byte-identical compare (`r45-routed-defects.py:116-119`). The row's own flip (a program-specific rule absent from the linked policy) is the checkable one; the lesson flip is the vacuous one.

### 4. attribution · captured-by R39

`corpus/QUALITY.md:351` (R39): a file cited as the output of a run is the unedited tee of that run, and a value the instrument did not emit is not a receipt. The round-43 precedent is `corpus/lessons/round-43-verifier-spotcheck.md:108` (defect 8: `127` was not the cited control's `exit=2`). Spot-check route: `corpus/lessons/round-44-verifier-spotcheck.md:32` and `:84`.

`/.ufo/waves/round-44/controls/final-attempt3.txt:14-18`:

```
$ python3 corpus/instruments/r44-routed-defects.py --selftest
usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]
                             [--selftest] [--work WORK]
r44-routed-defects.py: error: the following arguments are required: --root
exit=0
```

Re-run:

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r44-routed-defects.py --selftest
usage: r44-routed-defects.py [-h] --root ROOT [--baseline BASELINE]
                             [--selftest] [--work WORK]
r44-routed-defects.py: error: the following arguments are required: --root
bare-routed-exit:2
```

The bare command exits 2. The receipt attributes `exit=0` to it.

Fix that fails: an untracked worktree file `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` (this seat did not write it) makes the worktree counter print `limb R5 fixed=1 read=refiled=ok` and `routed-defects total=5 fixed=1 unresolved=4 exit=1`. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-files --error-unmatch .ufo/waves/round-44/controls/final-attempt3-refiled.txt` printed `did not match any file(s) known to git` and `ls-files-refiled:1`. The file's invocation line is `python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>`. Those brackets are placeholders, not a path this seat executed. On the freeze export, which has no such file, the limb is `R5 fixed=0 read=refiled-absent`. Editing `final-attempt3.txt` in place would also fail the limb's baseline byte compare (`r45-routed-defects.py:238-241`). This seat did not re-run `--selftest --work`, so the refiled case lines are not a tee this seat observed.

### 5. number-drift · captured-by R39

The frozen C2 before-count is `fixed=1/7`. Three runs of the committed counter on the committed tree printed `c2-gate fixed=2/7 exit=1` (two on the worktree, one on the freeze export). The green gates are G4 (`recheck-rc=0 quotes-ok=5`) and G7 (`census-rc=0`). G1 stays `rows=26 admitted=26`. Round-42's routed class for a record that quotes a tally the receipt does not print is RD42-1 (`corpus/lessons/round-42-verifier-spotcheck.md:173`). R43 (`corpus/QUALITY.md:369`) binds a before-cell to the control it cites; here `claims.json:26` and `freeze-controls.txt:2` agree with each other and disagree with the command. The control therefore carries a tally the instrument does not emit (R39).

Fix that fails: filing the lesson or the score from `fixed=1/7` fails the next run of `python3 corpus/instruments/r45-c2-gate.py --root <freeze-export>`. The direction stays red (`exit=1`, five gates still fail), so this is a wrong count, not a vacuous pass. Census binary used for G7: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`.

## Discriminated, not ranked

- C1 do-nothing on the freeze export matches `freeze-controls.txt:1` (`fixed=0 unresolved=5 exit=1`). The worktree's `fixed=1` is the untracked refile in candidate 4.
- `corpus/instruments/freeze-check.py` is absent (`test -e` exit 1; limb R4 `freeze-check-absent`). That is the unstarted §6.4 repair (`corpus/lessons/round-44-verifier-spotcheck.md:83`), and the C1 replay itself was red at freeze. Not a second mistake beyond candidate 5's count.
- Frontier status column: `corpus/README.md:200` header is `id | topic | status | entry | sources | next`. First data row `:202` has 6 content cells and 7 pipe characters. `admitted` is content cell 3 and pipe-field 4. `corpus/lessons/round-44.md` "third cell" and the spot-check's "fourth `|`-delimited field" (`round-44-verifier-spotcheck.md:46`) name one column.
- §6 item 6 (two L1 attempts, no report) has no lane artifact (`corpus/lessons/round-44-verifier-spotcheck.md:84`). Not mined.
- M44-8's frozen grep still prints 0 (quoted under candidate 1). Already a lesson row.

## Limitations

- No live fetch. The JavaScript-shell sentence is contradicted by committed `S072.txt`, not by a new HTTP call. The spot-check's `10 029-char` figure matches `len(text)-1` on that file (trailing newline removed), and `wc -c` is 10032.
- G7 shells out to the fleet `sources-census.sh` named above. A different census binary could move that one gate. G4 is `source-recheck.py` on the pinned manifest and did not change between the two worktree runs and the freeze export.
- Scratch `/fast/scratch/hyaku/kasegi-r45/R45ScoutMistakes` held the freeze export and two selftest stdout files. Removed before yield. The untracked refile under `.ufo/waves/round-44/controls/` was left in place.
