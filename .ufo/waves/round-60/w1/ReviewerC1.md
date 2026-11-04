VERIFIED

Seat ReviewerC1 · kasegi round 60 · wave w1 · claim **C1** (`depth:verifiability`, nominal per QUALITY R58).

Verdict scope: **VERIFIED on the frozen C1 predicate.** `claims.json` C1 is explicitly probe-set-scoped
("refuses every escape-aware and in-program/write-flag derive **in the committed probe set Q1-Q7**",
and SKILL.md:1227 "the round's frozen claim covers only the shell-chaining probe set"). Every frozen
number and both frozen digests reproduce exactly on the landed bytes. The kill rule enumerates only
probe-set conditions; none fires.

One material finding outside that probe set, **F1**: the write-flag screen compares *undecoded* option
tokens, so the same two flags the claim refuses as literals are admitted when spelled as a quoted token,
a backslash-escaped token, a clustered short option, or an abbreviated long option — seven such derives
are admitted and each writes its `MARK-*` file (evidence 5). F2–F4 are the wording/coverage consequences.
None of F1–F4 is a kill; they are routed as findings because the frozen sentence does not claim the class.

L = `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only, never written). S = `/fast/scratch/hyaku/kasegi-r60/ReviewerC1`
(removed at the end of this seat). Clone: `$S/clone`, pinned to `7f7dd267`, with
`git -C $S/clone rev-parse --show-toplevel` asserted equal to `$S/clone` before any later git call.
Lane HEAD at review time is `b8c77fb9fa13710f46d8f564a00af640de5108cd`, one wave-dispatch commit after the
implementation; it adds only four `.ufo/waves/round-60/` spec files (evidence 3.2), so the measured
instrument bytes are still the lane's. No tool was installed or upgraded this seat (channel: none).
Versions used: python 3.14.8, GNU bash 5.3.20(1)-release, git 2.56.0, GNU coreutils `sort` 9.12,
kernel 7.2.11-arch1-1 (evidence 0.1). The audit's own `shutil.which("bash")` is `/usr/bin/bash`,
so every derive below executes under **GNU sort 9.12**, not the omp session's builtin `sort` (0.8.0).

---

## 0. Setup and environment

### 0.1 Clone pinned to the implementation commit

```
$ S=/fast/scratch/hyaku/kasegi-r60/ReviewerC1; mkdir -p "$S"; export TMPDIR=$S
$ git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/clone"
$ D=$S/clone; TO=$(git -C "$D" rev-parse --show-toplevel); [ "$TO" = "$D" ] && echo TOPLEVEL-OK
TOPLEVEL-OK
$ git -C "$D" checkout -q 7f7dd267283d2a16ca38d4cb05bed92165cb35cd && echo CHECKOUT-OK
CHECKOUT-OK
$ git -C "$D" rev-parse HEAD
7f7dd267283d2a16ca38d4cb05bed92165cb35cd                       # exit=0
```

The clone's default HEAD was the lane tip `b8c77fb`; it was pinned to `7f7dd267` because the seat
names that commit. `git -C L log --oneline -3` shows `b8c77fb` (wave-1 dispatch) on top of `7f7dd26`,
so the implementation commit is intact history, not a rewritten tip.

### 0.2 Tool versions actually used (all `exit=0`)

```
$ python3 -V            -> Python 3.14.8
$ /usr/bin/bash --version | head -1 -> GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
$ git --version         -> git version 2.56.0
$ /usr/bin/sort --version | head -1 -> sort (GNU coreutils) 9.12
$ uname -sr             -> Linux 7.2.11-arch1-1
$ python3 -c 'import shutil;print(shutil.which("bash"))' -> /usr/bin/bash     # exit=0
```

`which -a sort` -> `/usr/bin/sort`; `/usr/bin/bash -c 'type -a sort'` -> `sort is /usr/bin/sort`
(the omp session shell additionally carries a builtin `sort 0.8.0`, which is *not* what the audit's
`/usr/bin/bash -c` derives execute). All bypass forms in evidence 5 were therefore re-confirmed
against GNU sort 9.12 directly (evidence 5.3).

---

## 1. Frozen digests, selftest, mutbat, ledger, red fixture, R74 limb (seat step 1)

Run from `$S/clone` at `7f7dd267`:

```
$ sha256sum corpus/instruments/figure-audit.py corpus/instruments/figure-audit-ledger.json
35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  corpus/instruments/figure-audit.py
28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b  corpus/instruments/figure-audit-ledger.json
                                                                         # exit=0
$ python3 corpus/instruments/figure-audit.py --selftest | tail -1
selftest cases=20 failures=0                                    # pipeline-exit=0
$ python3 corpus/instruments/figure-audit-mutbat.py | tail -1
mutbat killed=2/2 survivors=0 controls=pass                     # pipeline-exit=0
$ python3 corpus/instruments/figure-audit.py | tail -1
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0                    # pipeline-exit=0
$ python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json 2>&1 | grep d53-1
FIG d53-1-trailer recorded=34 derived=33 want=34 stale          # pipeline-exit=1
$ sed -n '1,40p' corpus/instruments/figure-audit.py | grep -c 'allow-list:.*head'
1                                                               # grep-exit=0
```

All eight frozen C1 counting commands' `want` values reproduce: instrument sha `35f7bcd3…2cb49ce2`,
ledger sha `28ad7fef…e81a753b`, `selftest cases=20 failures=0`, `mutbat killed=2/2 survivors=0
controls=pass`, `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, the red fixture line, the R74 limb `1`,
and the probe-runner want (evidence 2). The same two sha256 values are produced by the **lane working
tree** at `b8c77fb` (`sha256sum L/corpus/instruments/figure-audit.py …`, exit=0), so the landed bytes
equal the bytes measured in the clone.

Frozen sub-sentences also checked, all reproduced:

```
$ git -C L diff 66e6241 7f7dd267 -- corpus/instruments/figure-audit-ledger.json | grep -c '^[-+].*"derive"'
10                                                              # exit=0  -> 5 removed + 5 added derive lines
$ grep -c '"derive": "\(awk\|sed\)' L/corpus/instruments/figure-audit-ledger.json
0                                                               # exit=1 (zero matches, as intended)
$ grep -c 'run_case("\(escape-single-quote\|escape-double-quote\|sed-head\|awk-head\|sort-output-flag\|git-show-output-flag\)-refused"' L/corpus/instruments/figure-audit.py
6                                                               # exit=0
$ grep -n '"tr "' L/corpus/instruments/figure-audit.py
52:    "sha256sum", "cat ", "cut ", "sort ", "tr ", "head ", "tail ", "python ", "python3 ",
```

That is the frozen sentence's "the five awk derives are re-expressed in allow-listed heads" (exactly
5 derive pairs changed; 0 derives now open with awk or sed), its "six new cases" (count 6), and its
"tr joins the allow-list" (line 52).

## 2. Probe runner, Q1–Q7, controls, residual (seat step 2)

Command (clone root; the runner resolves the instrument absolute before its per-probe `cd`, so the
relative path runs literally — R77):

```
$ bash .ufo/waves/round-60/controls/c1-probe-run-r60.sh corpus/instruments/figure-audit.py "$S/probes"
instrument=/fast/scratch/hyaku/kasegi-r60/ReviewerC1/clone/corpus/instruments/figure-audit.py sha256=35f7bcd3e673b81b
run-utc=2026-11-04T13:39:19Z host=plazir27
probe=Q1-escape-single derive=cat g.txt \'; touch MARK-Q1; \' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q1-escape-single
probe=Q2-escape-double derive=cat g.txt \"; touch MARK-Q2; \" exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q2-escape-double
probe=Q3-sed-in-program derive=sed -n '1e touch MARK-Q3' g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q3-sed-in-program
probe=Q4-awk-system derive=awk 'BEGIN{system("touch MARK-Q4")}' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q4-awk-system
probe=Q5-sort-output-flag derive=sort -o MARK-Q5 g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q5-sort-output-flag
probe=Q6-git-show-output derive=git show --output=MARK-Q6 HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q6-git-show-output
probe=Q7-git-show-ext-diff derive=git show --ext-diff HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q7-git-show-ext-diff
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
probe=RESIDUAL-python-traversal derive=python3 corpus/instruments/../../../above-evil.py exit=1 markers=0 :: FIG RESIDUAL-python-traversal recorded=35 derived=UNAVAILABLE reason=derive-exit-2 stale
RUNNER-EXIT=0
```

Every C1 probe condition holds: Q1–Q7 `exit=2 markers=0` with `reason=derive-not-read-only`;
CTRL-quoted-semicolon `exit=0 derived=35`; CTRL-plain-count `exit=0 derived=1`;
RESIDUAL-python-traversal is **admitted** (`exit=1`, `reason=derive-exit-2`, i.e. *not*
`derive-not-read-only`), exactly the named-open state the kill rule requires. The probe block matches the
committed receipt `.ufo/waves/round-60/controls/c1-lane-after-r60.txt` line for line (differs only in
`run-utc`/`host`), including its `sha256=35f7bcd3e673b81b` header.

## 3. Commit scope audit (seat step 3)

### 3.1 Changed files

```
$ git -C L show --stat --format= 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
 .ufo/waves/round-60/claims-erratum-1.md            | 19 +++++++
 .ufo/waves/round-60/controls/c1-lane-after-r60.txt | 31 +++++++++++
 .ufo/waves/round-60/controls/c2-lane-after-r60.txt | 37 +++++++++++++
 PROVINCE.md                                        |  2 +
 SKILL.md                                           |  2 +-
 corpus/QUALITY.md                                  |  1 +
 corpus/README.md                                   | 21 ++++++++
 corpus/SOURCES.md                                  |  7 ++-
 corpus/instruments/figure-audit-ledger.json        | 14 ++---
 corpus/instruments/figure-audit.py                 | 63 +++++++++++++++++++---
 corpus/instruments/knowledge-expected.txt          |  1 +
 …project-zero-fuzzilli-vs-bigsleep-comparison.md   | 43 +++++++++++++++
 12 files changed, 224 insertions(+), 17 deletions(-)                      # exit=0
$ git -C L diff --name-status 66e6241 7f7dd267
A .ufo/waves/round-60/claims-erratum-1.md
A .ufo/waves/round-60/controls/c1-lane-after-r60.txt
A .ufo/waves/round-60/controls/c2-lane-after-r60.txt
M PROVINCE.md
M SKILL.md
M corpus/QUALITY.md
M corpus/README.md
M corpus/SOURCES.md
M corpus/instruments/figure-audit-ledger.json
M corpus/instruments/figure-audit.py
M corpus/instruments/knowledge-expected.txt
A corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md  # exit=0
```

**Out-of-scope files: none.** All 12 paths fall inside the declared change set (the nine named paths
plus `.ufo/waves/round-60/*`). No other file changed. `claims.json` is not in the diff.

### 3.2 Lane tip is one benign commit ahead

```
$ git -C L rev-parse HEAD
b8c77fb9fa13710f46d8f564a00af640de5108cd                       # exit=0
$ git -C L diff --stat 7f7dd267 b8c77fb
 .ufo/waves/round-60/build-spec.py    | 207 +++++++++++++++++++++++++++++
 .ufo/waves/round-60/w1-dispatch.json | 251 +++++++++++++++++++++++++++++++++++
 .ufo/waves/round-60/w1-plan.json     |  67 ++++++++++++++++++
 .ufo/waves/round-60/w1-spec.json     |  78 +++++++++++++++++++             # exit=0
```

No instrument, knowledge, README, SOURCES, PROVINCE or QUALITY byte moved after `7f7dd267`.

### 3.3 Frozen file untouched

```
$ for r in 66e6241 7f7dd267 b8c77fb; do git -C L rev-parse "$r:.ufo/waves/round-60/claims.json"; done
975f84c6634d5cb238fe11f5117bd5a47f7be051
975f84c6634d5cb238fe11f5117bd5a47f7be051
975f84c6634d5cb238fe11f5117bd5a47f7be051                       # exit=0 each
$ sha256sum L/.ufo/waves/round-60/claims.json
1ca06a10f5d2c7e9eeb695a23507381e4ce6f0c15c283cd7d7999bf5e9ec27c5  # exit=0
```

The same blob at the freeze commit, the implementation commit and the lane tip: the frozen claims and
the erratum are intact, and the erratum's `want: 2` correction is the only declared supersession.

## 4. Scope judgment (seat step 4)

The C1 frozen sentence is a **probe-set predicate**: "refuses every … derive **in the committed probe
set Q1-Q7**", and the row itself states "the round's frozen claim covers only the shell-chaining probe
set" (SKILL.md:1227). Measured against its receipts, no frozen sentence exceeds what the commands show:
Q1–Q7, both controls, the residual naming, the ledger, the selftest pin, the mutbat, the red fixture,
the R74 limb and both digests all reproduce (evidence 1–2), and the "five awk derives re-expressed" /
"six new cases" / "tr joins the allow-list" clauses reproduce numerically (evidence 1.1).

What **does** exceed its receipt is the same round's *class-level* wording in the registry row and the
instrument docstring (F2), and the residual list was not updated for the two classes the same round
closed (F2). The frozen sentence itself is not the place that claim is made; that is why this verdict
is VERIFIED while F1/F2 are reported.

---

## 5. Findings

### F1 — MAJOR (unclaimed class, outside the frozen probe set): the write-flag screen is defeated by token spelling; 7 derives are admitted and each writes its `MARK-*` file

Mechanism. `split_segments` (corpus/instruments/figure-audit.py:88–153) is escape-aware for *quoting*
(R72), but `denied_flag` (:156–167) receives the segment's raw text and compares `head.split()` tokens
literally:

- :163 `if tok == f or tok.startswith(f + "=")` — exact token or exact long-option spelling only;
- :164 `if f == "-o" and tok.startswith("-o") and tok != "-o"` — only a token that *begins* with `-o`.

Bash de-quotes and de-escapes tokens, and `sort`/`git` parse the decoded argv, so four spellings pass
the screen while the real command receives the refused flag. (The escape case is the same blind spot the
round added for quotes: `split_segments` appends the backslash and the escaped character verbatim, so
`-\o` reaches `denied_flag` as the three-character token `-\o`, while bash hands `sort` the token `-o`.)

Reproduction (self-contained; `$INSTR` is the clone's instrument; each probe gets a fresh root holding
`g.txt` = `35`, a one-figure ledger, and a `MARK-` count taken over the root):

```
B=$S/gateprobe
probe() { id=$1; derive=$2; inrepo=$3; r="$B/r-$id"; mkdir -p "$r"; printf '35\n' > "$r/g.txt"
  if [ "$inrepo" = repo ]; then mkdir -p "$r/repo"; git -C "$r/repo" init -q
    git -C "$r/repo" -c user.email=t@t -c user.name=t commit -q --allow-empty -m fixture
    [ "$(git -C "$r/repo" rev-parse --show-toplevel)" = "$r/repo" ] || echo ROOTMISMATCH; R="$r/repo"; else R="$r"; fi
  python3 -c 'import json,sys; json.dump({"figures":[{"id":sys.argv[1],"record":"probe","recorded":"35","derive":sys.argv[2],"want":"35"}]}, open(sys.argv[3],"w"))' "$id" "$derive" "$r/one.json"
  ( cd "$R" && python3 "$INSTR" --ledger "$r/one.json" --root "$R" > "$r/out.txt" 2>&1; echo "$?" > "$r/rc" )
  m=$(ls "$R" | grep -c '^MARK-')
  printf 'probe=%-24s exit=%s markers=%s :: %s\n' "$id" "$(cat "$r/rc")" "$m" "$(head -1 "$r/out.txt")"; }
```

```
probe G1-sort-o-control      'sort -o MARK-G1 g.txt'
probe G2-sort-cluster-ro     'sort -ro MARK-G2 g.txt'
probe G3-sort-abbrev-outp    'sort --outp=MARK-G3 g.txt'
probe G4-sort-quoted-flag    'sort "-o" MARK-G4 g.txt'
probe G5-sort-escaped-flag   'sort -\o MARK-G5 g.txt'
probe G6-sort-escaped-long   'sort --\output=MARK-G6 g.txt'
probe G7-sort-attached-quote 'sort -o"MARK-G7" g.txt'
probe G8-git-output-control  'git show --output=MARK-G8 HEAD'   repo
probe G9-git-quoted-flag     'git show "--output=MARK-G9" HEAD' repo
probe G10-git-escaped-flag   'git show --\output=MARK-G10 HEAD' repo
```

Printed output (exit codes and marker counts are the decisive columns):

```
probe=G1-sort-o-control        exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=G1-sort-o-control
probe=G2-sort-cluster-ro       exit=1 markers=1 :: FIG G2-sort-cluster-ro recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G3-sort-abbrev-outp      exit=1 markers=1 :: FIG G3-sort-abbrev-outp recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G4-sort-quoted-flag      exit=1 markers=1 :: FIG G4-sort-quoted-flag recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G5-sort-escaped-flag     exit=1 markers=1 :: FIG G5-sort-escaped-flag recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G6-sort-escaped-long     exit=1 markers=1 :: FIG G6-sort-escaped-long recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G7-sort-attached-quote   exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=G7-sort-attached-quote
probe=G8-git-output-control    exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=G8-git-output-control
probe=G9-git-quoted-flag       exit=1 markers=1 :: FIG G9-git-quoted-flag recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=G10-git-escaped-flag     exit=1 markers=1 :: FIG G10-git-escaped-flag recorded=35 derived=UNAVAILABLE reason=derive-empty stale
```

Seven derives are admitted and create their marker (`exit=1 markers=1` — the audit ran the derive and
then read empty stdout because `-o`/`--output` redirected it; the side effect already happened):
G2 clustered `-ro`; G3 abbreviated `--outp=`; G4 quoted `"-o"`; G5 escaped `-\o`; G6 escaped
`--\output=`; G9 quoted `"--output=…"`; G10 escaped `--\output=…`. The two literal controls G1 and G8,
and the attached form G7 (`-o"MARK"`, caught because the token starts with `-o`), stay refused
(`exit=2 markers=0`), which isolates the cause to token spelling rather than to the flags themselves.

Q7's flag has the same hole:

```
probe G11 'git show --ext-\diff HEAD'   repo
{"figures": [{"id": "G11", ... "derive": "git show --ext-\\diff HEAD", "want": "35"}]}
FIG G11 recorded=35 derived=commit ccefeb2d3fffb3767263eaf7a5831592fea18263
    (audit exit=1 — the derive was admitted and executed)
```

Whether this is "already named" depends on how the residual list's item (c) is read; F2 records why the
same registry row cannot be read both as stating the class refused (Q5–Q7) and as leaving it open.

### F1.1 — Same forms against GNU sort directly (rules out the omp builtin as the cause)

```
$ cd $S/soc; printf '35\n' > g.txt
$ /usr/bin/bash -c 'type -a sort; sort --version | head -1'
sort is /usr/bin/sort
sort (GNU coreutils) 9.12
$ /usr/bin/sort -ro G2 g.txt; echo "G2=$?"          -> G2=0
$ /usr/bin/sort --outp=G3 g.txt; echo "G3=$?"       -> G3=0
$ /usr/bin/sort "-o" G4 g.txt; echo "G4=$?"         -> G4=0
$ /usr/bin/sort -\o G5 g.txt; echo "G5=$?"          -> G5=0
$ /usr/bin/sort --\output=G6 g.txt; echo "G6=$?"    -> G6=0
$ ls G2 G3 G4 G5 G6 -> G2 G3 G4 G5 G6              all five files created
$ ( cd r && git show --output=M8 HEAD; echo $? )            -> 0, M8 created
$ ( cd r && git show "--output=M9" HEAD; echo $? )          -> 0, M9 created
$ ( cd r && git show --\output=M10 HEAD; echo $? )          -> 0, M10 created
$ ( cd r && git show --outp=M11 HEAD; echo $? )             -> 128, M11 absent  (git rejects the ambiguous abbreviation)
```

So the class is a property of the options, not of one sort implementation, and it needs no ANSI-C
(`$'…'`) quoting, no `#` comment and no `..` traversal — the three forms the lead already records as
out of scope or open.

### F2 — MEDIUM (R75-bound wording): the registry row and docstring state the write-flag class as refused, and the residual list still lists the same forms as open

- `SKILL.md:1224` (write-scope cell, edited by `7f7dd267`): "… and, since round 60, the escaped-quote,
  in-program (awk and sed heads removed) and write-flag (`sort -o`, `git show --output/--ext-diff`)
  **classes Q1-Q7** (`controls/c1-lane-after-r60.txt`); the python-head traversal
  (RESIDUAL-python-traversal) and the remaining classes listed below stay open".
  The receipt it cites supports only the literal spellings; the four spellings in F1 are neither refused
  nor listed in "the remaining classes below".
- `SKILL.md:1227` still lists, as open, "(b) in-program writes or execution by an allow-listed
  interpreter (`sed -n '1e …'`, `awk …`, `sed -n -i`, `awk -i inplace`)" and "(c) flag-level writes on
  allow-listed heads (`sort -o`, `git show --output=… HEAD`)" — i.e. exactly the two classes whose named
  forms round 60 closed (Q3/Q4 and Q5/Q6). Its receipts are the round-59 probes.
- `corpus/instruments/figure-audit.py:25` "the audit never runs a mutating command" and `:28`
  "sort without -o/--output" are falsified by F1's seven admitted derives. The R74 limb checks only that
  the docstring *names* the allow-list (`grep -c 'allow-list:.*head'` = 1, exit=0), not that the name is
  enforced, so the limb passes while the sentence is no longer true.

QUALITY R75 requires a row's write-scope sentence to be bound to a receipt per class it names and not to
exceed the receipts. Either the residual list needs an entry for token-spelling variants of flag-level
writes (and (b)/(c) need re-scoping to the forms that still work, e.g. `python3 corpus/instruments/*.py`),
or the row's class words need narrowing to "the literal Q5–Q7 spellings". Reported as text only, per the
seat contract; the lane files were not edited.

### F3 — LOW (coverage): the mutant battery and selftest cannot detect a screen that matches only literal tokens

`corpus/instruments/figure-audit-mutbat.py:23–28` has exactly two mutants (`m4-drop-stale-literal-case`,
`m6-readonly-gate-off`) and one control (`:29–31`); neither mutant targets `denied_flag`/`DENIED_FLAGS`.
The two new flag cases (`corpus/instruments/figure-audit.py:303–304`) use the literal spellings
`sort -o out.txt g.txt` and `git show --output=out.txt HEAD` only. `killed=2/2 survivors=0 controls=pass`
is true and reproducible (evidence 1); the gap is that `killed=2/2` cannot speak to the screen's
completeness, and a future mutant that narrows `denied_flag` further would survive.

### F4 — LOW (code reading, not reproduced as a write): an allow-listed head can spawn an arbitrary program through `--compress-program`

`sort` is allow-listed and only `-o`/`--output` are screened (`figure-audit.py:57–60`, `:156–167`).
GNU sort also honours `--compress-program=PROG`, which it executes (`PROG` for compression, `PROG -d` for
decompression). Reproduced that the program is spawned on a forced spill:

```
$ head -c 3000000 /dev/zero | tr '\0' '\n' | /usr/bin/sort -S 1K --compress-program=/bin/false >/dev/null
sort: '/bin/false' [-d] terminated abnormally                  # sort exit=2
$ head -c 3000000 /dev/zero | tr '\0' '\n' | /usr/bin/sort -S 1K >/dev/null
                                                               # exit=0 (control, no spill failure)
```

That is an execution channel on an allow-listed head, contradicting the docstring's own rationale for
removing awk/sed (`:30–32`: "an interpreted program can execute … whatever its head"). I did **not**
demonstrate a file write from it: a ledger-only derive must feed sort attacker-influenced data through
another allow-listed head, and I did not construct that. Stated as a gap, not as a reproduced escape.
(For completeness: the session shell's builtin `sort 0.8.0` also documents `--compress-program <PROG>`
in its own `--help`; the behaviour above was measured with `/usr/bin/sort` directly, which is what the
audit's `/usr/bin/bash -c` resolves — `shutil.which("bash")` = `/usr/bin/bash`, evidence 0.2.)

### F5 — INFORMATIONAL: the committed lane receipt labels a working-tree measurement with the freeze tip

`.ufo/waves/round-60/controls/c1-lane-after-r60.txt` header reads
`lane-tip=66e6241cd7afd6184273ce7df1dcd5328c187367 (working-tree bytes measured)` while its digest block
prints the post-implementation `35f7bcd3…`. The qualifier is present, and my in-commit measurement at
`7f7dd267` reproduces both digests, so no number is wrong; a reader who takes `lane-tip` as the measured
revision would be misled, because the tip's *committed* instrument at `66e6241` is the base. Recording
it only so the integrator can decide whether the header convention wants tightening.

---

## 6. Residual risk and verification gaps

- F1 is a live escape class against the instrument's stated contract, not against C1's frozen predicate.
  The instrument's consumers (the ledger's 35 figures) are all re-derived through the same gate; a ledger
  author who controls the `derive` string can write any lane-relative path with `sort "-o" <path>` or
  `git show "--output=<path>" HEAD`, and the audit reports only `derive-empty`/`stale`.
- I did not test every allow-listed head for write or exec flags (I read all of them:
  `git show`/`git cat-file`/`git ls-tree`/`grep`/`wc`/`ls`/`sha256sum`/`cat`/`cut`/`sort`/`tr`/`head`/
  `tail`/`python`/`python3`). Beyond `sort`/`git show` (F1) and `python3 corpus/instruments/*.py`
  (already-named residual (d)/(e)), the rest have no output-writing flag in GNU coreutils/git that I know
  of; that is a reading, not a probe, and is stated as such.
- The python-head traversal (`..` through `corpus/instruments/`) and `$'…'`/`#` were left alone per the
  seat's "already recorded / not claimed" list; I did not re-report them as new.
- Evidence was gathered at `7f7dd267` from a fresh clone; the lane tip advanced to `b8c77fb` (wave spec
  only), so the numbers here remain true for the lane tree unless a later round changes the instrument.
- Scratch: `/fast/scratch/hyaku/kasegi-r60/ReviewerC1` is removed at the end of this seat; no leftover
  files outside it were produced. Nothing under L was written except this evidence file. No credential
  material was read or written. No lane file, ledger, claim, erratum, SOURCES/README/PROVINCE/QUALITY,
  knowledge entry or instrument was edited.

## 7. Seat checklist against the item

| item | result |
|---|---|
| 1. clone at `7f7dd267`; instrument sha `35f7bcd3…`; ledger sha `28ad7fef…`; selftest last line; mutbat; ledger; red fixture `stale`; R74 limb `1` | all reproduced, evidence 0.1/1 |
| 2. `c1-probe-run-r60.sh` with the clone's instrument and `$S/probes`; Q1–Q7 exit 2 markers 0; controls exit 0 derived 35/1; residual admitted `reason=derive-exit-2` | all reproduced, evidence 2 |
| 3. `git show --stat --format= 7f7dd267…`: any file outside the declared set | none; all 12 paths declared, evidence 3.1 |
| 4. honest scope judgment: does any frozen sentence exceed the receipts | no for the probe-set sentences; F2 records the class-level overstatement in the SKILL row/docstring; F1 records the unclaimed class |
