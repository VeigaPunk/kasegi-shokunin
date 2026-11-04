VERDICT: killed 5 of 13 one-limb mutants (m1, m4, m5, m7, m8); 8 SURVIVED (m2, m3, m6, m9, m10, m11, m12, m13). No survivor is behaviourally equivalent to the pristine instrument: m11 (admitted `$(...)` inside double quotes) and m13 (admitted `sort --output=`) execute a write while the figure verifies green or stale, and m6 runs a configured diff driver. The instrument's own selftest is exit-code-sensitive on 5 of 13 limbs and blind on the other 8.

Seat MutationC1, Kasegi round 60 wave w1. Instrument: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py` at landed commit `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`, sha256 `35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2` (equals C1 counting command 7's want in the frozen claims). All mutants, logs and fixtures lived only in scratch `S=/fast/scratch/hyaku/kasegi-r60/MutationC1`; S was deleted at seat end (§10). No tool was installed or upgraded; no pacman transaction was run.

## 1. Instrument identity and the 14 copies

```
$ wc -l /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py && git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD && sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
333 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
b8c77fb9fa13710f46d8f564a00af640de5108cd
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 7f7dd267283d2a16ca38d4cb05bed92165cb35cd:corpus/instruments/figure-audit.py | sha256sum
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  -
```
Lane HEAD moved during the seat (`b8c77fb` at start -> `228118a8` when re-read); the instrument bytes stayed `35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2` at `7f7dd26`, at the worktree, and at the later HEAD (§10). The committed target therefore is the file measured.

Copy command (13 mutants + pristine control); the `&&` chain printed all 14 hashes, so mkdir/cp completed:

```
$ S=/fast/scratch/hyaku/kasegi-r60/MutationC1; mkdir -p "$S/mut" && L=/home/vgpnk/Projects/shokunin/kasegi-shokunin && for n in 1 2 3 4 5 6 7 8 9 10 11 12 13; do cp "$L/corpus/instruments/figure-audit.py" "$S/mut/m$n.py"; done && cp "$L/corpus/instruments/figure-audit.py" "$S/mut/control.py" && sha256sum "$S/mut"/*.py | sort -k2
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/control.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m1.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m2.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m3.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m4.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m5.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m6.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m7.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m8.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m9.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m10.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m11.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m12.py
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m13.py
```

Each mutant then received exactly one exact-once string replacement (`edit` tool; every diff in §4 is one hunk). `python3 -m py_compile` on all 14 copies exited 0 (§3).

## 2. The mutation battery (exact command and raw output)

```
$ S=/fast/scratch/hyaku/kasegi-r60/MutationC1; cd "$S/mut" || exit 9; command -v python; for n in control m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12 m13; do echo "=== $n hunks=$(diff -u control.py $n.py | grep -c '^@@') changed_lines=$(diff -u control.py $n.py | grep -cE '^[+-][^+-]')"; python3 -m py_compile "$n.py" 2>&1; echo "py_compile_exit=$?"; TMPDIR=$S python3 "$n.py" --selftest >"$n.selftest.log" 2>&1; echo "selftest_exit=$?"; tail -1 "$n.selftest.log"; grep -c 'verdict=fail' "$n.selftest.log" | sed 's/^/fail_lines=/'; done
/usr/bin/python
=== control hunks=0 changed_lines=0
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m1 hunks=1 changed_lines=7
py_compile_exit=0
selftest_exit=1
selftest cases=20 failures=1
fail_lines=1
=== m2 hunks=1 changed_lines=5
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m3 hunks=1 changed_lines=4
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m4 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=1
selftest cases=20 failures=1
fail_lines=1
=== m5 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=1
selftest cases=20 failures=1
fail_lines=1
=== m6 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m7 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=1
selftest cases=20 failures=1
fail_lines=1
=== m8 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=1
selftest cases=20 failures=1
fail_lines=1
=== m9 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m10 hunks=1 changed_lines=5
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m11 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m12 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
=== m13 hunks=1 changed_lines=2
py_compile_exit=0
selftest_exit=0
selftest cases=20 failures=0
fail_lines=0
```

The driver loop ran to completion; its own shell status was not captured (the loop's last command is the fail-line count), so every number relied on is a per-mutant `py_compile_exit=`/`selftest_exit=` value printed above. Every run printed `cases=20`, so the `EXPECTED_CASES = 20` pin (`corpus/instruments/figure-audit.py:63`) never fired: all five kills are behavioural case failures, not a dropped-case pin.

Killed mutant's failing case (from `grep 'verdict=fail' mN.selftest.log`):

```
m1: selftest case=escape-single-quote-refused exit=1 want=2 verdict=fail
m4: selftest case=sort-output-flag-refused exit=1 want=2 verdict=fail
m5: selftest case=git-show-output-flag-refused exit=1 want=2 verdict=fail
m7: selftest case=awk-head-refused exit=1 want=2 verdict=fail
m8: selftest case=sed-head-refused exit=1 want=2 verdict=fail
```

## 3. The 13 changes (one exact-once replacement each; `diff -u control.py mN.py`)

```
--- m1   remove the outside-quote backslash-escape branch (pristine :120-126)
@@ -117,13 +117,6 @@
-        if c == "\\":
-            if i + 1 >= n:
-                return None  # trailing lone backslash: a continuation bash would swallow
-            cur.append(c)
-            cur.append(cmd[i + 1])
-            i += 2
-            continue
--- m2   remove the double-quote backslash escape (:108-112)
@@ -105,11 +105,6 @@
-            if c == "\\" and i + 1 < n and cmd[i + 1] in '$`"\\':
-                cur.append(c)
-                cur.append(cmd[i + 1])
-                i += 2
-                continue
--- m3   accept a trailing lone backslash instead of refusing it (:121-122)
@@ -119,7 +119,9 @@
-                return None  # trailing lone backslash: a continuation bash would swallow
+                cur.append(c)
+                i += 1
+                continue
--- m4   drop the sort -o deny (:58)
@@ -55,7 +55,7 @@
-    ("sort", ("-o", "--output")),
+    ("sort", ("--output",)),
--- m5   drop the git show --output deny (:59)
@@ -56,7 +56,7 @@
-    ("git show", ("--output", "--ext-diff")),
+    ("git show", ("--ext-diff",)),
--- m6   drop the git show --ext-diff deny (:59)
@@ -56,7 +56,7 @@
-    ("git show", ("--output", "--ext-diff")),
+    ("git show", ("--output",)),
--- m7   re-add 'awk ' to READ_ONLY_HEADS (:50-53)
@@ -49,7 +49,7 @@
-    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ",
+    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ", "awk ",
--- m8   re-add 'sed -n ' to READ_ONLY_HEADS (:50-53)
@@ -49,7 +49,7 @@
-    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ",
+    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ", "sed -n ",
--- m9   drop 'tr ' from READ_ONLY_HEADS (:50-53)
@@ -49,7 +49,7 @@
-    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ",
+    "sha256sum", "cat ", "cut ", "sort ", "head ", "tail ", "python ", "python3 ",
--- m10  accept a lone '&' as a separator instead of refusing it (:139-144)
@@ -137,11 +137,10 @@
-            if cmd[i + 1:i + 2] != "&":
-                return None
+            fused = cmd[i + 1:i + 2] == "&"
-            i += 2
+            i += 2 if fused else 1
--- m11  ignore '$(' inside double quotes (keep backtick refusal) (:115)
@@ -112,7 +112,7 @@
-            elif c == "`" or (c == "$" and cmd[i + 1:i + 2] == "("):
+            elif c == "`":
--- m12  remove the unterminated-quote refusal (:150-151)
@@ -147,8 +147,6 @@
-    if quote is not None:
-        return None
--- m13  drop the sort --output long flag only (:58)
@@ -55,7 +55,7 @@
-    ("sort", ("-o", "--output")),
+    ("sort", ("-o",)),
```

Line pointers are to the pristine instrument: `READ_ONLY_HEADS` :50-53, `DENIED_FLAGS` :57-60, double-quote model :107-117, outside-quote escape :120-126, `&` :139-144, unterminated quote :148-151; the docstring contract sentence "An unterminated quote or a trailing lone backslash is refused" is :97. m1's single edit removes the whole outside-quote branch, so that file also loses the trailing-backslash refusal; its probe row is `differing=2` (Q1 and B), but §3 shows one hunk at one site.

## 4. Equivalence probe (52 inputs: the 35 committed ledger derives + 17 probe strings)

Command, exit 0:

```
$ S=/fast/scratch/hyaku/kasegi-r60/MutationC1; cd "$S" && TMPDIR=$S python3 probe.py
```

The probe imports each mutant beside the pristine copy and compares `check_read_only`; it then runs 22 selected (instrument, derive) pairs end-to-end in throwaway roots holding `g.txt=35`, `f1.txt=340`, `g2.txt=x"y`. Full output:

```
== classification differences against pristine (cases=52: ledger derives + probe strings)
m1 differing=2
  case=Q1-escape-single pristine=False mutant=True derive=cat g.txt \'; touch MARK-Q1; \'
  case=B-m3-trailing-backslash pristine=False mutant=True derive=cat g.txt \
m2 differing=1
  case=A2-m2-valid-dq-escape pristine=True mutant=False derive=grep -c "x\"y" g2.txt
m3 differing=1
  case=B-m3-trailing-backslash pristine=False mutant=True derive=cat g.txt \
m4 differing=1
  case=Q5-sort-output-flag pristine=False mutant=True derive=sort -o MARK-Q5 g.txt
m5 differing=1
  case=Q6-git-show-output pristine=False mutant=True derive=git show --output=MARK-Q6 HEAD
m6 differing=1
  case=Q7-git-show-ext-diff pristine=False mutant=True derive=git show --ext-diff HEAD
m7 differing=1
  case=Q4-awk-system pristine=False mutant=True derive=awk 'BEGIN{system("touch MARK-Q4")}'
m8 differing=1
  case=Q3-sed-in-program pristine=False mutant=True derive=sed -n '1e touch MARK-Q3' g.txt
m9 differing=4
  case=ledger:entries-r54 pristine=True mutant=False derive=git show 5108584aab38a1919992c46d0224f6ec1cb59363:corpus/README.md | grep -E '^\| F[0-9]+ \|' | cut -d'|' -f5 | tr ',' '\n' | wc -l
  case=ledger:entries-r55 pristine=True mutant=False derive=git show 133c575394099abf28ddf1b0125c53aefde3e0fa:corpus/README.md | grep -E '^\| F[0-9]+ \|' | cut -d'|' -f5 | tr ',' '\n' | wc -l
  case=ledger:entries-r56 pristine=True mutant=False derive=git show 8a5d7538b0caa50300b1eee88442a230d9a433f2:corpus/README.md | grep -E '^\| F[0-9]+ \|' | cut -d'|' -f5 | tr ',' '\n' | wc -l
  case=D-m9-tr-pipeline pristine=True mutant=False derive=cat g.txt | tr ',' '\n' | wc -l
m10 differing=1
  case=E-m10-lone-amp pristine=False mutant=True derive=cat g.txt & cat f1.txt
m11 differing=1
  case=F-m11-dq-cmdsubst pristine=False mutant=True derive=cat "g.txt$(touch MARK-M11)"
m12 differing=1
  case=G-m12-unterminated-quote pristine=False mutant=True derive=cat g.txt 'unterminated
m13 differing=1
  case=H-m13-sort-long-output pristine=False mutant=True derive=sort --output=out.txt g.txt
== end-to-end runs (instrument exit, new files, first output line)
instrument=control probe=Q1 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q1
instrument=control probe=Q2 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q2
instrument=control probe=Q3 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q3
instrument=control probe=Q4 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q4
instrument=control probe=Q5 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q5
instrument=control probe=Q6 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q6
instrument=control probe=Q7 exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q7
instrument=control probe=CTRL-quoted-semicolon exit=0 new_files=- first=FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
instrument=control probe=CTRL-plain-count exit=0 new_files=- first=FIG CTRL-plain-count recorded=1 derived=1 ok
instrument=m1 probe=Q1-escape-single exit=1 new_files=MARK-Q1 first=FIG Q1-escape-single recorded=35 derived=UNAVAILABLE reason=derive-exit-127 stale
instrument=m2 probe=A2-m2-valid-dq-escape exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=A2-m2-valid-dq-escape
instrument=m3 probe=B-m3-trailing-backslash exit=1 new_files=- first=FIG B-m3-trailing-backslash recorded=x derived=UNAVAILABLE reason=derive-exit-1 stale
instrument=m4 probe=Q5-sort-output-flag exit=1 new_files=MARK-Q5 first=FIG Q5-sort-output-flag recorded=35 derived=UNAVAILABLE reason=derive-empty stale
instrument=m5 probe=Q6-git-show-output exit=1 new_files=- first=FIG Q6-git-show-output recorded=35 derived=UNAVAILABLE reason=derive-exit-128 stale
instrument=m6 probe=Q7-git-show-ext-diff exit=1 new_files=- first=FIG Q7-git-show-ext-diff recorded=35 derived=UNAVAILABLE reason=derive-exit-128 stale
instrument=m7 probe=Q4-awk-system exit=1 new_files=MARK-Q4 first=FIG Q4-awk-system recorded=35 derived=UNAVAILABLE reason=derive-empty stale
instrument=m8 probe=Q3-sed-in-program exit=1 new_files=MARK-Q3 first=FIG Q3-sed-in-program recorded=35 derived=UNAVAILABLE reason=derive-empty stale
instrument=m9 probe=D-m9-tr-pipeline exit=2 new_files=- first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=D-m9-tr-pipeline
instrument=m10 probe=E-m10-lone-amp exit=1 new_files=- first=FIG E-m10-lone-amp recorded=x derived=340
instrument=m11 probe=F-m11-dq-cmdsubst exit=0 new_files=MARK-M11 first=FIG F-m11-dq-cmdsubst recorded=35 derived=35 ok
instrument=m12 probe=G-m12-unterminated-quote exit=1 new_files=- first=FIG G-m12-unterminated-quote recorded=x derived=UNAVAILABLE reason=derive-exit-2 stale
instrument=m13 probe=H-m13-sort-long-output exit=1 new_files=out.txt first=FIG H-m13-sort-long-output recorded=x derived=UNAVAILABLE reason=derive-empty stale
```

Every mutant changes classification on at least one input (none is an equivalent mutant). The pristine control row is the detector's baseline: Q1-Q7 exit 2 / no files, both controls exit 0 with their stated derived values.

## 5. In-repo impact of the two git-show limbs (m5, m6)

`runfix.sh`, exit 0: a throwaway repo (`git init`; `rev-parse --show-toplevel` equals the fixture) with two commits, a committed `.gitattributes` (`* diff=ext`) and `diff.ext.command`; the instrument runs with `--root` = the repo.

```
fixture=/fast/scratch/hyaku/kasegi-r60/MutationC1/tmp.8W8tqBc91e
fixture-root-ok
driver-config=/fast/scratch/hyaku/kasegi-r60/MutationC1/tmp.8W8tqBc91e/ext.sh
plain_git_show_exit=0
plain_git_marker=1
id=control-output instrument=control exit=2 new_in_root=[] first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=control-output
id=m5-output instrument=m5 exit=1 new_in_root=[out.txt ] first=FIG m5-output recorded=x derived=UNAVAILABLE reason=derive-empty stale
id=control-extdiff instrument=control exit=2 new_in_root=[] first=FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=control-extdiff
id=m6-extdiff instrument=m6 exit=1 new_in_root=[MARK-EXT ] first=FIG m6-extdiff recorded=x derived=commit d683c080b8f3b1a7593344b0855cca6808e37947
final_root_markers=[MARK-EXT ]
fixture_removed=yes
```

`plain_git_marker=1` first proves `git show --ext-diff HEAD` executes the configured driver in this fixture (independent of the instrument). Pristine control refuses both derives with exit 2; m5 writes `out.txt`; m6 runs the external driver, creating `MARK-EXT`.

## 6. Two consequence checks: m9 against the committed ledger, m2's refused derive is legitimate

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 /fast/scratch/hyaku/kasegi-r60/MutationC1/mut/m9.py >/fast/scratch/hyaku/kasegi-r60/MutationC1/m9.ledger.out 2>&1; echo "m9_ledger_exit=$?"; grep -m1 'UNAVAILABLE' /fast/scratch/hyaku/kasegi-r60/MutationC1/m9.ledger.out; wc -l < /fast/scratch/hyaku/kasegi-r60/MutationC1/m9.ledger.out
m9_ledger_exit=2
FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=entries-r54
11
```
(10 earlier figures printed, then the refusal at the first `tr` figure; m9 makes the real 35-figure audit unusable.)

```
$ r=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r60/MutationC1); printf 'x"y\n' > "$r/g2.txt"; ( cd "$r" && bash -c 'grep -c "x\"y" g2.txt'; echo "bash_exit=$?" ); rm -rf -- "$r"
1
bash_exit=0
```
The derive m2 refuses is ordinary and green in bash (count 1, exit 0).

## 7. Survivor list with equivalence judgment

None of the eight survivors is behaviourally equivalent; each is a real limb loss the selftest cannot see.

- **m2** (double-quote escape removed): NOT equivalent — over-refuses `grep -c "x\"y" g2.txt` that pristine admits (§4 A2; bash exit 0). Root cause of the blindness: the selftest's only double-quote case (`:300`) writes both quotes escaped from *outside* (`cat g.txt \"; touch X; \"`), so the outside-quote branch consumes the quotes and the double-quote branch is never entered. No committed ledger derive changes classification under m2 (§4: `m2 differing=1`, the targeted A2 only), so no current figure breaks; hidden limb.
- **m3** (trailing lone backslash accepted): NOT equivalent — admits `cat g.txt \` that pristine and docstring `:97` refuse; bash then exits 1 (`reason=derive-exit-1`), so fail-closed with no write. Contract/coverage defect, not an escape hole.
- **m6** (`--ext-diff` deny removed): NOT equivalent — admits `git show --ext-diff HEAD`; in a repo with a diff driver it runs the configured command (`MARK-EXT`, §5) while pristine refuses exit 2. This is the execution class the `DENIED_FLAGS` comment names (`:56-57`); the selftest has no `--ext-diff` case (only the probe runner Q7, `controls/c1-probe-run-r60.sh:54`).
- **m9** (`tr` head removed): NOT equivalent — refuses `tr` pipelines. 3 of the 35 committed ledger derives (`entries-r54`, `entries-r55`, `entries-r56`) now fail closed, and the mutant exits 2 on the real ledger at `entries-r54` (§6). Over-refusal/availability, not a write.
- **m10** (lone `&` accepted): NOT equivalent — admits `cat g.txt & cat f1.txt` that pristine refuses; the foreground segment runs (`derived=340`). The selftest's `chain-background-refused` (`:292`) passes only because its second segment is `true`, which is not an allow-listed head — it is insensitive to the separator rule. Backgrounding an allow-listed head (including the python counter head, the known residual class) is therefore admitted.
- **m11** (`$(` inside double quotes ignored): NOT equivalent, and the most serious survivor — `cat "g.txt$(touch MARK-M11)"` is admitted, creates `MARK-M11`, and the figure still verifies green (`exit=0`, `derived=35 ok`, §4). The selftest's `chain-cmdsubst-refused` (`:294`) uses `$(` *outside* quotes, which the metacharacter set at `:148` (semicolon, backtick, parens, newline, CR, `>`) catches without touching the double-quote branch.
- **m12** (unterminated-quote refusal removed): NOT equivalent — admits `cat g.txt 'unterminated` that pristine and docstring `:97` refuse; bash rejects it (exit 2 -> stale), so fail-closed with no write. Same coverage gap as m3.
- **m13** (`sort --output` long flag removed): NOT equivalent — admits `sort --output=out.txt g.txt`; the file is written (`new_files=out.txt`) and the derive reads empty (stale). The selftest covers only `sort -o` (`:303`), so the long flag is a separate uncovered write limb.

## 8. Which selftest case guards which limb (R17 reading)

| mutant | guarding selftest case | result |
|---|---|---|
| m1 outside escape | `escape-single-quote-refused` :299 | killed (behavioural) |
| m2 dq escape | none (only :300, which never enters dq state) | survived |
| m3 trailing `\` | none (docstring :97 only) | survived |
| m4 sort `-o` | `sort-output-flag-refused` :303 | killed |
| m5 `git show --output` | `git-show-output-flag-refused` :304 | killed |
| m6 `--ext-diff` | none | survived |
| m7 awk head | `awk-head-refused` :302 | killed |
| m8 sed head | `sed-head-refused` :301 | killed |
| m9 `tr` head | none (and 3 ledger derives use it) | survived |
| m10 lone `&` | `chain-background-refused` :292 — passes for the wrong reason | survived |
| m11 dq `$(` | none (only `chain-cmdsubst-refused` :294, outside quotes) | survived |
| m12 unterminated quote | none (docstring :97 only) | survived |
| m13 sort `--output` | none (only `-o` at :303) | survived |

## 9. Observations for the lead (text only; no file changed)

- The selftest's double-quote escape case (`:300`) does not exercise the double-quote branch; an m2-class regression would pass it. A positive case like `grep -c "x\"y" g2.txt` (or any derive with `\"` inside dq) would cover the limb.
- `--ext-diff` (m6), `sort --output` (m13), the lone `&` separator rule (m10), dq `$(` (m11), trailing `\` (m3) and unterminated quotes (m12) have no behavioural case; m11/m13 are write/execute classes, so their absence is the largest coverage gap found.
- The mutant battery (13 limbs, 5 killed) is a coverage statement about the *selftest*, not about the gate runtime: Q1-Q7 are each refused by the pristine instrument (§4 control rows), so the landed C1 claim's probe results are unaffected by these survivors.

## 10. Hygiene, bounds, cleanup

- Lane writes: only this file (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/w1/MutationC1.md`). No `git add/commit/stash/checkout/switch/reset/pull/push` and no jj command against L; lane access was read-only (`rev-parse`, `show`, `log`, `cat-file -e`, `grep`, `sha256sum`, `ls`, `wc`) plus one read-only instrument run of m9 against the ledger (§6), which executes only committed read-only derives.
- Lane HEAD advanced during the seat (`b8c77fb` -> `228118a8`); the instrument's sha256 stayed `35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2` at `7f7dd26`, at the worktree and at the later HEAD; post-run `sha256sum` of the lane file still printed that value (§ final check below).
- Scratch: all copies, mutants, logs, the probe, the fixture repo and the impact root were under `S=/fast/scratch/hyaku/kasegi-r60/MutationC1`; every probe/runfix temp root was created under S and removed. At seat end:

```
$ S=/fast/scratch/hyaku/kasegi-r60/MutationC1; L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; echo "copy_files=$(ls "$S"/mut/*.py | wc -l)"; echo "distinct_copy_hashes=$(sha256sum "$S"/mut/*.py | awk '{print $1}' | sort -u | wc -l)"; sha256sum "$L/corpus/instruments/figure-audit.py"; echo "lane_instrument_sha_unchanged=$?"; echo "scratch_before=[$(ls "$S" | tr '\n' ' ')]"; rm -rf -- "$S"; test ! -e "$S"; echo "scratch_gone_exit=$?"; ls -d "$S" 2>&1 | grep -c 'No such file'
copy_files=14
distinct_copy_hashes=14
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
lane_instrument_sha_unchanged=0
scratch_before=[m9.ledger.out mut probe.out probe.py runfix.sh ]
scratch_gone_exit=0
1
```

Reading of that output: `distinct_copy_hashes=14` is the post-mutation state (control + 13 different mutants); before editing, all 14 copies hashed identically (§1), and §3 shows each mutant differs from pristine by exactly one hunk. `lane_instrument_sha_unchanged=0` is the `sha256sum` exit status, not a comparison; the hash printed beside it equals §1's value, so the lane instrument bytes are unchanged. `scratch_gone_exit=0` is `test ! -e`; the trailing `1` is `grep -c 'No such file'`. No leftover scratch; nothing outside S and this evidence file was created.
- Tools: none installed or upgraded (no `uv tool`, `npx`, binary download, cargo/npm or pacman transaction); `python3 -m py_compile` and the host `bash`/`git`/`python` were sufficient. `command -v python` printed `/usr/bin/python`, which is why the selftest's inner `python "%s"` subprocess works on this host.
- No credential material was read or written.

Report: .ufo/waves/round-60/w1/MutationC1.md
