VERDICT: BROKEN

Scope: `--selftest` of `corpus/instruments/r44-frontier-count.py` in export of commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd). Export made with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/export`. Attacked file sha256 = `2409d2402c65522f02dbbaad9b7c472aa625eda5a5847215f63af208dcc9f0d4` (356 lines), matching the expected digest.

Bottom line: the selftest rejects the 10 seam-level mutants it ships with, and it kills most source-level mutants, but **9 single-edit source mutants of the counting/verdict code survive** (selftest prints `failures=0`, exit 0). One of them is a false PASS on the exact shape the counter exists to catch (25 admitted of 26 rows with `--expect 26`). The round-44 false-pass class is therefore only partly guarded. A draft gate fix (below) kills all of them on re-run; it is NOT landed.

---

## 1. Survivors (unmodified export; each mutant = exact single replacement in the export file; each run `python3 <mutant> --selftest --work <dir>` with TMPDIR set)

All nine print `selftest cases=43 failures=0`, exit 0. Control on unmodified export: `selftest cases=43 failures=0`, exit 0.

**S1 (most serious) `--expect` compares the ROW count, not the admitted count.**
- Edit (line 131): `if expect is not None and is_short(admitted, expect):` -> `if expect is not None and is_short(rows, expect):`
- Fixture: 26 rows, row F26 `queued` (25 admitted), `--expect 26`, `--ids`.
- Unmodified: `frontier rows=26 admitted=25` / `frontier expected=26 admitted=25 verdict=SHORT exit=1`, rc=1.
- Mutant: `frontier rows=26 admitted=25`, rc=0 — **false PASS**.
- Reverse fixture (25 admitted of 26 rows, `--expect 25`): unmodified rc=0; mutant prints `verdict=SHORT`, rc=1. Both directions are wrong in the mutant, and no fixture in `_cases()` has rows != admitted together with `--expect`.

**S2 status matched by substring.**
- Edit (line 69): `return cells[2] == "admitted"` -> `return "admitted" in cells[2]`
- Fixture: F02 status `not admitted`. Unmodified `frontier rows=2 admitted=1`; mutant `frontier rows=2 admitted=2`. Survives: no fixture contains a status with `admitted` as a substring other than exact `admitted`.

**S3 status matched by prefix.**
- Edit (line 69): `return cells[2] == "admitted"` -> `return cells[2].startswith("admitted")`
- Fixture: F02 status `admitted (partial)`. Unmodified admitted=1; mutant admitted=2. Survives.

**S4 HTML-comment rows counted.**
- Edit (line 62): `ROW_RX = re.compile(r"^\| F\d+ \|")` -> `ROW_RX = re.compile(r"^(?:<!--\s*)?\| F\d+ \|")`
- Fixture line: `<!-- | F02 | topic 2 | admitted | knowledge/k2.md | S002 | note | -->`. Unmodified `frontier-ids=F01` / `rows=1 admitted=1`; mutant `frontier-ids=F01,<!--` / `rows=2 admitted=1`. Survives: no commented row in fixtures.

**S5 comments stripped then counted.**
- Edit (line 86-87): insert `line = re.sub(r"<!--|-->", "", line).lstrip()` as first statement of the `for line in lines:` body.
- Survives (same fixture family as S4; mutant counts the stripped comment row). Unmodified and mutant both emit `failures=0` on the old fixture set.

**S6 indented rows counted.**
- Edit (line 62): `ROW_RX = re.compile(r"^\| F\d+ \|")` -> `ROW_RX = re.compile(r"^\s*\| F\d+ \|")`
- Fixture: `  | F02 | ...` (two leading spaces). Unmodified `rows=1 admitted=1`; mutant `frontier-ids=F01,F02` / `rows=2 admitted=2`. Survives. (Design note: CommonMark tolerates up to 3 leading spaces, so the "correct" behaviour for indented rows is a policy choice that the selftest does not pin either way.)

**S7 minimum-cells guard raised.**
- Edit (line 90): `if len(cells) < 3:` -> `if len(cells) < 4:`
- Fixture: `| F02 | t | admitted |` (3 cells). Unmodified `rows=2 admitted=2`; mutant `rows=1 admitted=1`. Survives: all fixture rows have 6 cells.

**S8 `--ids` suppressed when duplicates exist.**
- Edit (line 121): `    if show_ids:` -> `    if show_ids and not any(ids.count(i) > 1 for i in ids):`  (keep the following `out.append` line)
- Fixture: two `| F01 |` rows, `--ids`. Unmodified prints `frontier-ids=F01,F01` then `frontier duplicate-ids=F01 verdict=DEFECT exit=1`; mutant prints only the DEFECT line. Survives: no fixture combines `--ids` with duplicates. (Minor; the DEFECT verdict is still correct.)

**S9 temp location hard-coded to /tmp (gate does not guard it).**
- Edit (line 278): `base = tempfile.mkdtemp(prefix="r44-frontier-selftest-") if own_tmp else work` -> `base = ("/tmp/r44-frontier-selftest-x" if own_tmp else work)`
- Unmodified tree does NOT do this (see §2); this mutant only shows the gate has no check that the default temp dir honours TMPDIR. Mutant ran with TMPDIR set to a scratch dir, printed `failures=0`, and removed its /tmp directory on exit (verified `none left in /tmp`).

Killed (for the record, all rc=1, failures>0 on unmodified base): status compared to `queued` (failures=20 in run 1), status from cell 1 (24), status from cell 3 (crash: `IndexError` in `_is_admitted` line 69; no summary line printed), header counted (30), duplicate check removed (4), duplicates deduped at count (4), duplicate threshold `>2` (4), `--expect` `>=` (7), `--expect` `<` only (2), exit 0 on SHORT (5), default readme path wrong (14), do-nothing `count_lines` (28), do-nothing `count_frontier` (14).

Do-nothing control: `count_lines` body replaced by `return 0, 0, []` -> selftest `failures=28`, rc=1. `count_frontier` replaced by `return 0, 0, []` -> `failures=14`, rc=1. Unmodified export -> `failures=0`, rc=0. So the gate discriminates the do-nothing case.

---

## 2. Required checks

- **No hard-coded /tmp in the export.** `grep -n "/tmp\|tmp" .../r44-frontier-count.py` printed only:
  `277: own_tmp = work is None`, `278: base = tempfile.mkdtemp(prefix="r44-frontier-selftest-") if own_tmp else work`, `326: if own_tmp:`. No literal `/tmp` path.
- **Honours TMPDIR (default).** Mutant `default-tmp-kept-printed` (only the final `shutil.rmtree` replaced by `print("KEPT", base)`), run with `TMPDIR=<S>/tmpx`, printed:
  `KEPT /fast/scratch/hyaku/kasegi-r45/R45W2RevFrontierSelftest/tmpx/r44-frontier-selftest-htrqprqd`
  and the default run of the unmodified file with the same TMPDIR left `ls -A tmpx | wc -l` = 0 (cleaned up).
- **Honours --work.** `TMPDIR=<S>/tmpx python3 r44-frontier-count.py --selftest --work <S>/work/explicit` -> `selftest cases=43 failures=0`, rc=0; `ls <S>/work/explicit | wc -l` = 18 fixture directories kept (the explicit DIR is kept, as the docstring says).
- **Default-temp cleanup.** Default run leaves nothing in TMPDIR (see above), and no `r44-frontier*` entries in `/tmp`.

---

## 3. Draft fix (NOT landed; scratch only; kills every survivor above)

Add these cases to `_cases()` before `dict(name="missing-readme-is-zero-rows"` (line 205):

```python
        dict(name="expect-counts-admitted-not-rows", text=_readme(rows26[:25] + [_row(26, status="queued")]),
             args=["--expect", "26"], rc=1,
             out=["frontier rows=26 admitted=25",
                  "frontier expected=26 admitted=25 verdict=SHORT exit=1"]),
        dict(name="expect-25-of-26-rows-passes", text=_readme(rows26[:25] + [_row(26, status="queued")]),
             args=["--expect", "25"], rc=0, out=["frontier rows=26 admitted=25"]),
        dict(name="status-substring-not-admitted", text=_readme([_row(1), _row(2, status="not admitted")]),
             args=[], rc=0, out=["frontier rows=2 admitted=1"]),
        dict(name="status-admitted-prefix-not-admitted", text=_readme([_row(1), _row(2, status="admitted (partial)")]),
             args=[], rc=0, out=["frontier rows=2 admitted=1"]),
        dict(name="html-comment-row-not-counted",
             text=_readme([_row(1)]).replace("\n## Other", "\n<!-- | F02 | topic 2 | admitted | k | S | n | -->\n## Other"),
             args=[], rc=0, out=["frontier rows=1 admitted=1"]),
        dict(name="three-cell-admitted-row-counted", text=_readme([_row(1), "| F02 | t | admitted |\n"]),
             args=[], rc=0, out=["frontier rows=2 admitted=2"]),
        dict(name="indented-row-not-counted", text=_readme([_row(1), "  " + _row(2)]),
             args=[], rc=0, out=["frontier rows=1 admitted=1"]),
        dict(name="ids-printed-on-duplicate-defect", text=_readme(dup), args=["--ids"], rc=1,
             out=["frontier-ids=" + ",".join([f"F{i:02d}" for i in range(1, 27)] + ["F05"]),
                  "frontier duplicate-ids=F05 verdict=DEFECT exit=1"]),
```

Add after the `check("memory/...")` loop, before `# 3. Mutants`, a temp-location check (only meaningful when `--work` is absent):

```python
        if work is None:
            real_base = os.path.realpath(base)
            check("temp/default-under-gettempdir",
                  real_base.startswith(os.path.realpath(tempfile.gettempdir()) + os.sep), f"base={real_base}")
```

Re-run result on the draft (scratch copy, `patched2.py`): unmodified draft `selftest cases=60 failures=0` rc=0; all nine survivors rc=1 with failures 2–4 (e.g. `expect-compares-row-count` -> `case cli/expect-counts-admitted-not-rows: FAIL`); `tmp-hardcoded` under default temp -> `case temp/default-under-gettempdir: FAIL base=/tmp/r44-frontier-selftest-x`, rc=1. Note: `tmp-hardcoded` with an explicit `--work` still passes by design (the check is skipped when `--work` is given).

The draft is not landed; the L1 owns the writer. Changing the case count from 43 to 60 also changes the number any landed doc quotes (`selftest cases=43`), which must be updated together.

---

## 4. Other observations (INFO)

- Integration tree real counts: `python3 corpus/instruments/r44-frontier-count.py --root <export> --ids` -> `frontier rows=27 admitted=27`; `--expect 27` -> `frontier rows=27 admitted=27`, rc=0; `--expect 26` -> `frontier expected=26 admitted=27 verdict=SHORT exit=1`, rc=1. The frozen round-44 target 26 therefore no longer matches the integration tree; the round-45 target should be confirmed by the L1 (C2 scope, not the selftest).
- Real `corpus/README.md` frontier status cells: all 27 rows are `admitted` (`awk` + `uniq -c` -> `27 admitted`); no real `<!--` lines and no indented `| F` rows. The real tree therefore does not exercise S2–S8; only fixtures can.
- Crash-kill: `status-read-from-cell-3` raises `IndexError` (traceback, no `selftest cases` line). Counted as killed (rc=1) but the gate does not report it as a case failure. Minor.

---

## 5. Limitations

- Attacked only the export of 6662a42 and copies of it. I did not run mutants against the moving lane working tree, and did not touch the fleet repo, sibling lanes, or any shared file.
- Mutants are single textual replacements, each asserted to match exactly once; they do not cover multi-edit or harness-level mutants (e.g. `check()` not incrementing `failures`, which would make the gate print `failures=0` regardless). That harness path is not tested here.
- The draft fix was verified only in scratch against these nine mutants and the unmodified export; no broader mutation sweep was run.
- No tools installed or upgraded. Python 3.14.8 (system). No pacman touched.
- Scratch directory `/fast/scratch/hyaku/kasegi-r45/R45W2RevFrontierSelftest/` removed on exit; nothing written under /tmp.
