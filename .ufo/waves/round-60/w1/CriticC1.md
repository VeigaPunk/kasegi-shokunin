DEFEATED — the repaired derive gate admits 24 new write/execute derives (9 of them with the gate green, exit 0), none of them Q1-Q7; the recorded python-traversal residual is confirmed live as a control. C1's literal Q1-Q7 sentence still passes, so the claim's predicate is false as a property while its own probe set is intact.

Seat CriticC1, round 60 wave w1, lane kasegi. Adversarial review of C1 at implementation
`7f7dd267283d2a16ca38d4cb05bed92165cb35cd` (lane HEAD measured `228118a8cfba679c1d97841aa3af38e5ec83d84a`;
the gate file is byte-identical across that range — §1). All probes ran against a scratch copy
whose sha256 equals the lane file; no lane file was written, no lane suite was run.

## 0. Counterexample (shortest)

    derive : sort g.txt --outp=MARK            (single segment, head `sort` is allow-listed)
    gate   : exit 1  (FIG ... derived=UNAVAILABLE reason=derive-empty), MARK file created
    green  : cat g.txt && sort g.txt --outp=MARK   -> gate exit 0, FIG ... ok, MARK created

The deny screen (`denied_flag`, `corpus/instruments/figure-audit.py:156-168`) compares raw
whitespace tokens to `-o`, `-o*`, `--output`, `--output=*`. It never sees the argv bash will
execute, so every shell spelling change below walks past it. Q1-Q7 are all still refused.

## 1. Instrument bytes under test

    $ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
    228118a8cfba679c1d97841aa3af38e5ec83d84a
    $ git rev-parse 7f7dd267283d2a16ca38d4cb05bed92165cb35cd
    7f7dd267283d2a16ca38d4cb05bed92165cb35cd
    $ git show 7f7dd26:corpus/instruments/figure-audit.py | sha256sum
    35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  -
    $ git diff --stat 7f7dd267..HEAD -- corpus/instruments/figure-audit.py
    (empty: the gate did not change between the implementation commit and HEAD)
    $ sha256sum corpus/instruments/figure-audit.py
    35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2  corpus/instruments/figure-audit.py

## 2. Method

Driver: `/fast/scratch/hyaku/kasegi-r60/CriticC1/probe.py`, run as

    $ cd /fast/scratch/hyaku/kasegi-r60/CriticC1 && TMPDIR=$PWD python3 probe.py
    (driver-exit=0; 61 attempts)

Per attempt: a fresh root `/fast/scratch/hyaku/kasegi-r60/CriticC1/r-<id>/` holding
`g.txt` = `35\n`, a one-figure ledger `one.json` in that root, optional fixture setup
(git init + one commit with `git -C <root> rev-parse --show-toplevel` asserted equal to the
root; textconv/smudge/diff.external helpers whose absolute marker path is baked in; for A01
the `corpus/instruments/` traversal directories; for A38 a byte-copy of the committed
`gate-quote-audit.py`, sha256 `396d720efa93fb38a1637f02f6b22da9eb2a0db03a0383e9ded78da7657b6896`),
then exactly the lane runner's invocation with cwd = root and stdin = /dev/null:

    cd <root> && python3 <gate copy> --ledger <root>/one.json --root <root>

REFUSED = exit 2 with `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only` (the gate
refused before running the derive). WROTE = at least one `MARK-*` file in the root (the derive
ran and wrote; for the `--compress-program`/textconv/filter rows the marker is created by the
program the allow-listed head executed). `exit` is the gate's exit code.

Host tool resolution matters and the driver prints it: the tool shell resolves a *builtin*
`sort 0.8.0`, but every derive here runs through `bash -c` (the gate's own `run_derive`), which
resolves GNU coreutils 9.12; python 3.14.8; git 2.56.0. Driver header, verbatim:

    driver=CriticC1 round-60 probe
    gate-copy=/fast/scratch/hyaku/kasegi-r60/CriticC1/gate.py sha256=35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2
    lane-gate=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py sha256=35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2
    python=3.14.8
    bash-sort=sort (GNU coreutils) 9.12
    git=git version 2.56.0
    attempts=61
    

## 3. All 61 attempts (gate exit / MARK count)

Output of the command above, table section verbatim:

    attempt                                  setup    exit markers gate   derive
    A01-CTRL-residual-python-traversal       residual 0    1       WROTE  python3 corpus/instruments/../../../above-evil.py
    A02-CTRL-plain-count                     -        0    0       admitted cat g.txt | wc -l
    A03-Q5-replica-sort-o                    -        2    0       REFUSED sort -o MARK-A03 g.txt
    A04-Q6-replica-git-show-output           repo     2    0       REFUSED git show --output=MARK-A04 HEAD
    A05-Q7-replica-git-show-ext-diff         repo-ext 2    0       REFUSED git show --ext-diff HEAD
    A06-sort-output-eq                       -        2    0       REFUSED sort --output=MARK-A06 g.txt
    A07-sort-output-space                    -        2    0       REFUSED sort --output MARK-A07 g.txt
    A08-sort-abbrev-outp                     -        1    1       WROTE  sort g.txt --outp=MARK-A08
    A09-sort-abbrev-out                      -        1    1       WROTE  sort --out=MARK-A09 g.txt
    A10-sort-cluster-ro                      -        1    1       WROTE  sort -ro MARK-A10 g.txt
    A11-sort-cluster-no                      -        1    1       WROTE  sort -no MARK-A11 g.txt
    A12-sort-dquoted-o                       -        1    1       WROTE  sort "-o" MARK-A12 g.txt
    A13-sort-backslashed-o                   -        1    1       WROTE  sort \-o MARK-A13 g.txt
    A14-sort-ansic-o                         -        1    1       WROTE  sort $'-o' MARK-A14 g.txt
    A15-sort-linecont-o                      -        1    1       WROTE  sort -\<LF>o MARK-A15 g.txt
    A16-sort-squoted-output                  -        1    1       WROTE  sort '--output=MARK-A16' g.txt
    A17-sort-linecont-output                 -        1    1       WROTE  sort --out\<LF>put=MARK-A17 g.txt
    A18-sort-brace-expansion                 -        1    1       WROTE  sort {--output=MARK-A18,-u} g.txt
    A19-sort-ifs-expansion                   -        1    1       WROTE  sort ${IFS}--output=MARK-A19 g.txt
    A20-sort-green-composite                 -        0    1       WROTE  cat g.txt && sort g.txt --outp=MARK-A20
    A21-sort-compress-program-exec           sortm    0    1       WROTE  sort -m --batch-size 2 --compress-program=./cp.sh f1 f2 f3 f4 f5
    A22-git-show-dquoted-output              repo     0    1       WROTE  cat g.txt && git show "--output=MARK-A22" HEAD
    A23-git-show-splitquoted-output          repo     0    1       WROTE  cat g.txt && git show '--output'=MARK-A23 HEAD
    A24-git-show-linecont-output             repo     0    1       WROTE  cat g.txt && git show --out\<LF>put=MARK-A24 HEAD
    A25-git-show-ifs-output                  repo     0    1       WROTE  cat g.txt && git show ${IFS}--output=MARK-A25 HEAD
    A26-git-show-abbrev-outp                 repo     1    0       admitted git show --outp=MARK-A26 HEAD
    A27-git-show-abbrev-out                  repo     1    0       admitted git show --out=MARK-A27 HEAD
    A28-git-show-abbrev-ext-dif              repo-ext 1    0       admitted git show --ext-dif HEAD
    A29-git-show-linecont-ext-diff           repo-ext 1    1       WROTE  git show --ext\<LF>-diff HEAD
    A30-git-show-ifs-ext-diff                repo-ext 1    1       WROTE  git show ${IFS}--ext-diff HEAD
    A31-git-show-textconv-exec               repo-tc  0    2       WROTE  git show --textconv HEAD:g.txt
    A32-git-cat-file-filters-exec            repo-tc  0    1       WROTE  git cat-file --filters HEAD:g.txt
    A33-git-cat-file-textconv-exec           repo-tc  0    2       WROTE  git cat-file --textconv HEAD:g.txt
    A34-git-show-orderfile                   repo     1    0       admitted git show -Og.txt HEAD
    A35-git-show-order-file-long             repo     1    0       admitted git show --order-file=g.txt HEAD
    A36-git-show-output-indicator            repo     1    0       admitted git show --output-indicator-new=X HEAD
    A37-git-c-config-refused                 repo-ext 2    0       REFUSED git -c diff.external=./x.sh show HEAD
    A38-python-instrument-json-write         pyinst   1    1       WROTE  python3 corpus/instruments/gate-quote-audit.py --json MARK-A38 --min-quotes 0
    A39-head-lines                           -        0    0       admitted head -n1 g.txt
    A40-tail-lines                           -        0    0       admitted tail -n1 g.txt
    A41-ls-flags                             -        1    0       admitted ls -la g.txt
    A42-grep-f-file                          -        0    0       admitted grep -f g.txt g.txt
    A43-grep-include-recursive               -        1    0       admitted grep -r --include=g.txt 35 .
    A44-grep-quoted-gt                       -        0    0       admitted grep -e 35 -e '>' g.txt
    A45-wc-files0-from                       -        1    0       admitted wc --files0-from=g.txt
    A46-wc-herestring                        -        0    0       admitted wc -l <<< 35
    A47-procsubst-refused                    -        2    0       REFUSED cat <(printf 35)
    A48-exec-refused                         -        2    0       REFUSED exec cat g.txt
    A49-command-refused                      -        2    0       REFUSED command cat g.txt
    A50-xargs-refused                        -        2    0       REFUSED printf 35 | xargs echo
    A51-find-exec-refused                    -        2    0       REFUSED find . -name g.txt
    A52-comment-hides-semicolon-refused      -        2    0       REFUSED cat g.txt # ; touch MARK-A52
    A53-comment-hides-pipe-admitted          -        0    0       admitted cat g.txt #| wc -l
    A54-linecont-separator                   -        0    0       admitted cat g.txt \<LF>| wc -l
    A55-dquote-backslash-metachar            -        0    0       admitted grep "35\>" g.txt
    A56-tr-write-head-refused                -        2    0       REFUSED tr 35 XX < g.txt | sort -o MARK-A56
    A57-CTRL-quoted-semicolon                -        0    0       admitted cat g.txt | grep -e '35' -e ';'
    A58-Q1-replica-escape-single             -        2    0       REFUSED cat g.txt \'; touch MARK-A58; \'
    A59-Q2-replica-escape-double             -        2    0       REFUSED cat g.txt \"; touch MARK-A59; \"
    A60-Q3-replica-sed-in-program            -        2    0       REFUSED sed -n '1e touch MARK-A60' g.txt
    A61-Q4-replica-awk-system                -        2    0       REFUSED awk 'BEGIN{system("touch MARK-A61")}'

Counts, by command over the same output:

    $ awk '/^attempt /{f=1;next} f&&/^$/{exit} f{print $5}' probe-run.txt | sort | uniq -c
         19 admitted
         17 REFUSED
         25 WROTE
    $ awk '/^attempt /{f=1;next} f&&/^$/{exit} f&&$4>0'  probe-run.txt | wc -l   -> 25
    $ awk '/^attempt /{f=1;next} f&&/^$/{exit} f&&$4>0&&$3==0' probe-run.txt | wc -l -> 10
    $ awk '/^attempt /{f=1;next} f&&/^$/{exit} f&&$4>0&&$3==1' probe-run.txt | wc -l -> 15

The ten green-with-write rows: A01, A20, A21, A22, A23, A24, A25, A31, A32, A33.
(A01 is the already-recorded python-traversal residual, kept here as a control; the other
nine green rows and fifteen exit-1 rows are new. Of the 24 new rows, 17 need only the root
(A08-A20; A22-A25 additionally need a git repo, and the lane is one); A21 needs five input
files; A29-A33 need a repo whose config arms a textconv/filter/external-diff program; A38
needs the committed instrument present, which it is in the lane.)

## 4. Decisive per-attempt receipts (all write rows, the Q5-Q7 refusals, the controls,
the abbreviation negatives)

Every block below is verbatim from the same `probe.py` output (`derive-bytes` is the exact
Python repr of the derive string; `<LF>` in the table is a real newline).

    [A01-CTRL-residual-python-traversal]
      derive-bytes = 'python3 corpus/instruments/../../../above-evil.py'
      gate-exit    = 0  markers=1  marker-names=MARK-A01-CTRL-residual-python-traversal  gate-refusal=False
      firstline    = FIG A01-CTRL-residual-python-traversal recorded=35 derived=35 ok
    
    [A02-CTRL-plain-count]
      derive-bytes = 'cat g.txt | wc -l'
      gate-exit    = 0  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A02-CTRL-plain-count recorded=1 derived=1 ok
    
    [A03-Q5-replica-sort-o]
      derive-bytes = 'sort -o MARK-A03 g.txt'
      gate-exit    = 2  markers=0  marker-names=-  gate-refusal=True
      firstline    = FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=A03-Q5-replica-sort-o
    
    [A04-Q6-replica-git-show-output]
      derive-bytes = 'git show --output=MARK-A04 HEAD'
      gate-exit    = 2  markers=0  marker-names=-  gate-refusal=True
      firstline    = FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=A04-Q6-replica-git-show-output
    
    [A05-Q7-replica-git-show-ext-diff]
      derive-bytes = 'git show --ext-diff HEAD'
      gate-exit    = 2  markers=0  marker-names=-  gate-refusal=True
      firstline    = FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=A05-Q7-replica-git-show-ext-diff
    
    [A08-sort-abbrev-outp]
      derive-bytes = 'sort g.txt --outp=MARK-A08'
      gate-exit    = 1  markers=1  marker-names=MARK-A08  gate-refusal=False
      firstline    = FIG A08-sort-abbrev-outp recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A09-sort-abbrev-out]
      derive-bytes = 'sort --out=MARK-A09 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A09  gate-refusal=False
      firstline    = FIG A09-sort-abbrev-out recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A10-sort-cluster-ro]
      derive-bytes = 'sort -ro MARK-A10 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A10  gate-refusal=False
      firstline    = FIG A10-sort-cluster-ro recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A11-sort-cluster-no]
      derive-bytes = 'sort -no MARK-A11 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A11  gate-refusal=False
      firstline    = FIG A11-sort-cluster-no recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A12-sort-dquoted-o]
      derive-bytes = 'sort "-o" MARK-A12 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A12  gate-refusal=False
      firstline    = FIG A12-sort-dquoted-o recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A13-sort-backslashed-o]
      derive-bytes = 'sort \\-o MARK-A13 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A13  gate-refusal=False
      firstline    = FIG A13-sort-backslashed-o recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A14-sort-ansic-o]
      derive-bytes = "sort $'-o' MARK-A14 g.txt"
      gate-exit    = 1  markers=1  marker-names=MARK-A14  gate-refusal=False
      firstline    = FIG A14-sort-ansic-o recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A15-sort-linecont-o]
      derive-bytes = 'sort -\\\no MARK-A15 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A15  gate-refusal=False
      firstline    = FIG A15-sort-linecont-o recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A16-sort-squoted-output]
      derive-bytes = "sort '--output=MARK-A16' g.txt"
      gate-exit    = 1  markers=1  marker-names=MARK-A16  gate-refusal=False
      firstline    = FIG A16-sort-squoted-output recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A17-sort-linecont-output]
      derive-bytes = 'sort --out\\\nput=MARK-A17 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A17  gate-refusal=False
      firstline    = FIG A17-sort-linecont-output recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A18-sort-brace-expansion]
      derive-bytes = 'sort {--output=MARK-A18,-u} g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A18  gate-refusal=False
      firstline    = FIG A18-sort-brace-expansion recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A19-sort-ifs-expansion]
      derive-bytes = 'sort ${IFS}--output=MARK-A19 g.txt'
      gate-exit    = 1  markers=1  marker-names=MARK-A19  gate-refusal=False
      firstline    = FIG A19-sort-ifs-expansion recorded=35 derived=UNAVAILABLE reason=derive-empty stale
    
    [A20-sort-green-composite]
      derive-bytes = 'cat g.txt && sort g.txt --outp=MARK-A20'
      gate-exit    = 0  markers=1  marker-names=MARK-A20  gate-refusal=False
      firstline    = FIG A20-sort-green-composite recorded=35 derived=35 ok
    
    [A21-sort-compress-program-exec]
      derive-bytes = 'sort -m --batch-size 2 --compress-program=./cp.sh f1 f2 f3 f4 f5'
      gate-exit    = 0  markers=1  marker-names=MARK-A21-sort-compress-program-exec  gate-refusal=False
      firstline    = FIG A21-sort-compress-program-exec recorded=35
    
    [A22-git-show-dquoted-output]
      derive-bytes = 'cat g.txt && git show "--output=MARK-A22" HEAD'
      gate-exit    = 0  markers=1  marker-names=MARK-A22  gate-refusal=False
      firstline    = FIG A22-git-show-dquoted-output recorded=35 derived=35 ok
    
    [A23-git-show-splitquoted-output]
      derive-bytes = "cat g.txt && git show '--output'=MARK-A23 HEAD"
      gate-exit    = 0  markers=1  marker-names=MARK-A23  gate-refusal=False
      firstline    = FIG A23-git-show-splitquoted-output recorded=35 derived=35 ok
    
    [A24-git-show-linecont-output]
      derive-bytes = 'cat g.txt && git show --out\\\nput=MARK-A24 HEAD'
      gate-exit    = 0  markers=1  marker-names=MARK-A24  gate-refusal=False
      firstline    = FIG A24-git-show-linecont-output recorded=35 derived=35 ok
    
    [A25-git-show-ifs-output]
      derive-bytes = 'cat g.txt && git show ${IFS}--output=MARK-A25 HEAD'
      gate-exit    = 0  markers=1  marker-names=MARK-A25  gate-refusal=False
      firstline    = FIG A25-git-show-ifs-output recorded=35 derived=35 ok
    
    [A26-git-show-abbrev-outp]
      derive-bytes = 'git show --outp=MARK-A26 HEAD'
      gate-exit    = 1  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A26-git-show-abbrev-outp recorded=35 derived=UNAVAILABLE reason=derive-exit-128 stale
    
    [A27-git-show-abbrev-out]
      derive-bytes = 'git show --out=MARK-A27 HEAD'
      gate-exit    = 1  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A27-git-show-abbrev-out recorded=35 derived=UNAVAILABLE reason=derive-exit-128 stale
    
    [A28-git-show-abbrev-ext-dif]
      derive-bytes = 'git show --ext-dif HEAD'
      gate-exit    = 1  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A28-git-show-abbrev-ext-dif recorded=35 derived=UNAVAILABLE reason=derive-exit-128 stale
    
    [A29-git-show-linecont-ext-diff]
      derive-bytes = 'git show --ext\\\n-diff HEAD'
      gate-exit    = 1  markers=1  marker-names=MARK-A29-git-show-linecont-ext-diff  gate-refusal=False
      firstline    = FIG A29-git-show-linecont-ext-diff recorded=35 derived=commit 08406f85863fb4ae02c82bee9cc1abd88f8d7611
    
    [A30-git-show-ifs-ext-diff]
      derive-bytes = 'git show ${IFS}--ext-diff HEAD'
      gate-exit    = 1  markers=1  marker-names=MARK-A30-git-show-ifs-ext-diff  gate-refusal=False
      firstline    = FIG A30-git-show-ifs-ext-diff recorded=35 derived=commit 08406f85863fb4ae02c82bee9cc1abd88f8d7611
    
    [A31-git-show-textconv-exec]
      derive-bytes = 'git show --textconv HEAD:g.txt'
      gate-exit    = 0  markers=2  marker-names=MARK-A31-git-show-textconv-exec-sm,MARK-A31-git-show-textconv-exec-tc  gate-refusal=False
      firstline    = FIG A31-git-show-textconv-exec recorded=35 derived=35 ok
    
    [A32-git-cat-file-filters-exec]
      derive-bytes = 'git cat-file --filters HEAD:g.txt'
      gate-exit    = 0  markers=1  marker-names=MARK-A32-git-cat-file-filters-exec-sm  gate-refusal=False
      firstline    = FIG A32-git-cat-file-filters-exec recorded=35 derived=35 ok
    
    [A33-git-cat-file-textconv-exec]
      derive-bytes = 'git cat-file --textconv HEAD:g.txt'
      gate-exit    = 0  markers=2  marker-names=MARK-A33-git-cat-file-textconv-exec-sm,MARK-A33-git-cat-file-textconv-exec-tc  gate-refusal=False
      firstline    = FIG A33-git-cat-file-textconv-exec recorded=35 derived=35 ok
    
    [A34-git-show-orderfile]
      derive-bytes = 'git show -Og.txt HEAD'
      gate-exit    = 1  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A34-git-show-orderfile recorded=35 derived=commit 08406f85863fb4ae02c82bee9cc1abd88f8d7611
    
    [A36-git-show-output-indicator]
      derive-bytes = 'git show --output-indicator-new=X HEAD'
      gate-exit    = 1  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A36-git-show-output-indicator recorded=35 derived=commit 08406f85863fb4ae02c82bee9cc1abd88f8d7611
    
    [A38-python-instrument-json-write]
      derive-bytes = 'python3 corpus/instruments/gate-quote-audit.py --json MARK-A38 --min-quotes 0'
      gate-exit    = 1  markers=1  marker-names=MARK-A38  gate-refusal=False
      firstline    = FIG A38-python-instrument-json-write recorded=35 derived=GATE-QUOTE-AUDIT annotated=0 ok=0 erratum-on-record=0 failures=0 want=35 stale
    
    [A53-comment-hides-pipe-admitted]
      derive-bytes = 'cat g.txt #| wc -l'
      gate-exit    = 0  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A53-comment-hides-pipe-admitted recorded=35 derived=35 ok
    
    [A57-CTRL-quoted-semicolon]
      derive-bytes = "cat g.txt | grep -e '35' -e ';'"
      gate-exit    = 0  markers=0  marker-names=-  gate-refusal=False
      firstline    = FIG A57-CTRL-quoted-semicolon recorded=35 derived=35 ok
    

## 5. Mechanism: the screen and the scanner disagree about what bash runs

`mech.py` imports the scratch gate copy and prints the gate's own classifiers per derive:

    $ cd /fast/scratch/hyaku/kasegi-r60/CriticC1 && TMPDIR=$PWD python3 mech.py

    gate=/fast/scratch/hyaku/kasegi-r60/CriticC1/gate.py
    'sort -o MARK g.txt'                                                     check_read_only=False | head='sort -o MARK g.txt' denied_flag=True segment_ok=False
    'sort --output=MARK g.txt'                                               check_read_only=False | head='sort --output=MARK g.txt' denied_flag=True segment_ok=False
    'sort g.txt --outp=MARK'                                                 check_read_only=True | head='sort g.txt --outp=MARK' denied_flag=False segment_ok=True
    'sort "-o" MARK g.txt'                                                   check_read_only=True | head='sort "-o" MARK g.txt' denied_flag=False segment_ok=True
    'sort \\-o MARK g.txt'                                                   check_read_only=True | head='sort \\-o MARK g.txt' denied_flag=False segment_ok=True
    "sort $'-o' MARK g.txt"                                                  check_read_only=True | head="sort $'-o' MARK g.txt" denied_flag=False segment_ok=True
    'sort -ro MARK g.txt'                                                    check_read_only=True | head='sort -ro MARK g.txt' denied_flag=False segment_ok=True
    'sort {--output=MARK,-u} g.txt'                                          check_read_only=True | head='sort {--output=MARK,-u} g.txt' denied_flag=False segment_ok=True
    'sort ${IFS}--output=MARK g.txt'                                         check_read_only=True | head='sort ${IFS}--output=MARK g.txt' denied_flag=False segment_ok=True
    'sort -\\\no MARK g.txt'                                                 check_read_only=True | head='sort -\\\no MARK g.txt' denied_flag=False segment_ok=True
    'git show --output=MARK HEAD'                                            check_read_only=False | head='git show --output=MARK HEAD' denied_flag=True segment_ok=False
    'git show "--output=MARK" HEAD'                                          check_read_only=True | head='git show "--output=MARK" HEAD' denied_flag=False segment_ok=True
    "git show '--output'=MARK HEAD"                                          check_read_only=True | head="git show '--output'=MARK HEAD" denied_flag=False segment_ok=True
    'git show --outp=MARK HEAD'                                              check_read_only=True | head='git show --outp=MARK HEAD' denied_flag=False segment_ok=True
    'git show ${IFS}--output=MARK HEAD'                                      check_read_only=True | head='git show ${IFS}--output=MARK HEAD' denied_flag=False segment_ok=True
    'git show --ext-diff HEAD'                                               check_read_only=False | head='git show --ext-diff HEAD' denied_flag=True segment_ok=False
    'git show --ext\\\n-diff HEAD'                                           check_read_only=True | head='git show --ext\\\n-diff HEAD' denied_flag=False segment_ok=True
    'git show --textconv HEAD:g.txt'                                         check_read_only=True | head='git show --textconv HEAD:g.txt' denied_flag=False segment_ok=True
    'git cat-file --filters HEAD:g.txt'                                      check_read_only=True | head='git cat-file --filters HEAD:g.txt' denied_flag=False segment_ok=True
    'sort -m --batch-size 2 --compress-program=./cp.sh f1 f2 f3 f4 f5'       check_read_only=True | head='sort -m --batch-size 2 --compress-program=./cp.sh f1 f2 f3 f4 f5' denied_flag=False segment_ok=True
    'python3 corpus/instruments/gate-quote-audit.py --json MARK --min-quotes 0' check_read_only=True | head='python3 corpus/instruments/gate-quote-audit.py --json MARK --min-quotes 0' denied_flag=False segment_ok=True
    'python3 corpus/instruments/../../../above-evil.py'                      check_read_only=True | head='python3 corpus/instruments/../../../above-evil.py' denied_flag=False segment_ok=True
    'cat g.txt && sort g.txt --outp=MARK'                                    check_read_only=True | head='cat g.txt' denied_flag=False segment_ok=True ; head='sort g.txt --outp=MARK' denied_flag=False segment_ok=True

Read with `corpus/instruments/figure-audit.py`:

- `split_segments` (:88-153) models quotes/escapes well enough that no separator-class
  bypass survives my set: `;`, `&`, `||`, newline, backtick, `(`, `)` and `>` are refused
  unquoted, and Q1/Q2 are refused exactly as the claim says.
- `denied_flag` (:156-168) is a raw `head.split()` comparison. Every row with
  `denied_flag=False` above is a head whose *argv* is the denied flag, reached by
  dequoting (`"-o"`, `\-o`, `$'-o'`, `'--output=...'`), abbreviation (`--outp`, `--out`),
  getopt clustering (`-ro`, `-no`), line continuation (`-\<LF>o`, `--out<LF>put=`,
  `--ext<LF>-diff`), or expansion (`{...,...}`, `${IFS}`).
- `DENIED_FLAGS` (:57-60) names two flags. It does not name `sort --compress-program`
  (GNU sort executes PROG for temp files: the in-program class the claim removed sed/awk
  heads for), `git show --textconv`, or any `git cat-file` flag at all.
- The three git abbreviation rows (A26-A28) are *admitted by the gate* and stopped only
  by git's own parser (`unrecognized argument`, exit 128): that route is closed by git, not
  by the screen.
- `segment_ok` (:170-178) checks only `parts[1].startswith('corpus/instruments/')` for
  python heads: no committed-blob check and no argument inspection.

## 6. Predicate objections: the claim can be met without the property being met

6a. The frozen sentence quantifies over `the committed probe set Q1-Q7`, and C1's kill rule
names only those seven strings plus the controls. My run confirms all seven are refused
(A03/A04/A05, A58-A61: exit 2, markers 0) and both controls admitted (A02 derived=1, A57
derived=35). The sentence is therefore true, and the kill rule cannot fire on any §4 row.
What is false is the property the sentence is offered as evidence for — the docstring at
`figure-audit.py:25` says `the audit never runs a mutating command`, and :28 says `sort
without -o/--output`: the 24 new admitted derives say otherwise.

6b. The selftest pin is a count, not a case-identity check (`EXPECTED_CASES = 20`, :63;
`len(cases) != EXPECTED_CASES`, :311). Scratch-copy experiment (`predicate.py`, lane file
untouched): the six round-60 refusal cases are replaced by six vacuous admitted cases
(`run_case(..., 0, 'cat g.txt')`), and the selftest still passes:

    six round-60 cases replaced: 6
    gate.py          selftest-exit=0 last-line=selftest cases=20 failures=0
    gate-dup.py      selftest-exit=0 last-line=selftest cases=20 failures=0
    gate-del.py      selftest-exit=1 last-line=selftest cases=19 failures=1
    gate-dup-m6.py   selftest-exit=1 last-line=selftest cases=20 failures=2

So `selftest cases=20 failures=0` is satisfiable with the six round-60 limbs gutted;
deleting a case is caught (19/1), replacing one is not. Fair note: with the six gutted, the
mutbat's m6 edit is still killed (exit 1, failures=2) by the pre-existing `echo` and
`pipe-to-shell` cases, so `killed=2/2` is not fully vacuous — but it is only as strong as a
case list whose round-60 members are exact-spelling-only (:299-304: `sort -o`, `git show
--output=`, `sed ... 1e`, `awk BEGIN{system}`, and the two escaped quotes; none of the
spellings in §4 appears).

6c. The R74 docstring limb is a phrase match: the counted command
`sed -n '1,40p' corpus/instruments/figure-audit.py | grep -c 'allow-list:.*head'` prints `1`
(measured, exit 0) while the same docstring misstates enforcement in three ways (mutating
commits, `sort without -o/--output`, `a corpus/instruments/*.py counter`). A grep for
`allow-list:.*head` cannot distinguish a correct allow-list description from a wrong one.

## 7. What stands (re-measured, not quoted)

- Q1-Q7: refused, exit 2, markers 0 (A03, A04, A05, A58, A59, A60, A61).
- Controls: CTRL-plain-count exit 0 derived=1 (A02); CTRL-quoted-semicolon exit 0
  derived=35 (A57).
- Selftest on the scratch copy: `selftest cases=20 failures=0`, exit 0 (predicate.py row 1).
- R74 docstring limb: `1` (§6c command).
- Refusal classes that do hold: `;` chains, `&`, `||`, newlines, `$()`, backticks, `>`;
  process substitution, `exec`, `command`, `xargs`, `find`; `sort -o`/`--output`/`--output=`;
  `git show --output=`, `git show --ext-diff`; `git -c ... show` (head not allow-listed).
- Known residual (not re-reported as new): A01 confirms the python-head traversal is live —
  with the target script present it is admitted and executes (exit 0, marker), which is
  stronger than the lane's own residual probe (derive-exit-2, target absent).
- Not measured by this seat (out of item scope): the lane ledger 35/35, the mutbat run, the
  red fixture, and the lane-root runner. §6b reads the mutbat's mutants from source only.

## 8. Impacted axes

- `depth:verifiability` (C1's axis): the instrument's read-only property is not established
  by its receipts. The gate's write protection is a two-entry denylist (sort's `-o`/`--output`,
  git show's `--output`/`--ext-diff`) and its refusal evidence is the seven committed probe strings; the claim
  presents it as an escape-aware in-program/write-flag screen. Score delta should not be
  awarded for the property; if awarded, the receipts need the §4 rows as named residuals.
- `coverage`: untouched — no C2 file, registry row, README row, or PROVINCE text is
  implicated by anything here.
- Claim coherence: the docstring limb (R74) now certifies wording the code does not
  enforce (:25, :28, :30). That is a documentation/claim defect of the same axis, not a new
  instrument defect.

## 9. Smallest safe correction (text only; no lane edit made)

Do not grow the denylist first; fix the mismatch that makes any denylist walkable:

1. Decide on the argv, not the raw token. Dequote each segment head (quotes, backslash,
   ANSI-C `$'...'`, `${...}`/`$IFS` expansion, line continuations) before comparing, and
   refuse a `sort`/`git show`/`git cat-file` segment that contains any of `' " \\ $ { }`
   at all — the conservative posture the round already accepts for `$'...'`.
2. Deny by option grammar: for short bundles test the bundled characters (`-ro` and `-no`
   contain `o`); for long options deny any prefix of the denied name (`--out`, `--outp`),
   since `getopt_long` accepts unambiguous prefixes (GNU sort does; git's parser does not).
3. Extend the screen to the other execution surfaces of allow-listed heads:
   `sort --compress-program`, `git show --textconv`, `git cat-file --textconv|--filters`.
4. Bind the interpreter allowance to committed bytes: require the target to be a blob at
   `HEAD` of the lane repo, and refuse output-path arguments (`--json`, `--out`) — or drop
   the interpreter allowance for a dedicated read-only counter wrapper.
5. Replace the selftest count pin with a digest of the case list, and add the §4 spellings
   to the case list so `killed=2/2` and `cases=20` bind the semantics.

## 10. Hygiene

- No installs or upgrades; nothing written outside the scratch dir and this file.
- Scratch `/fast/scratch/hyaku/kasegi-r60/CriticC1` was removed at the end of the seat;
  the transcripts above are the receipts. The lane tree was read only (`git show`,
  `git rev-parse`, `git diff --stat`, `sha256sum`, `grep`, `sed -n`).
