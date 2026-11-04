PASS — scoped regression: Q1–Q7 refused (exit 2, zero markers), controls admitted (35 and 1), traversal residual now refused; 192 base/pin direct-call pairs produce zero new admissions.

# ExecRegression — round 61 / w1

Axes: depth:verifiability (pinned identity, exact receipts) and coverage (prior named probes plus root-argument matrix). No C2 or complete C1 judgment is made.

## Identity and scope

Read operator rules and frozen claims before probes. Frozen claims retrieved with `git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json` (exit 0); base c33d24ddd11abf1ebdea0dccf7327e9069dd9104, pin 13c8060b343e002339ffd72da37ff74514f82765.

Only production write is this report. No commits, lane-state mutations, installations, suite, selftest, mutbat, C2 checks, or background agents. All probe subprocesses inherited TMPDIR=/fast/scratch/hyaku/kasegi-r61/ExecRegression. Tool: Python 3.14.8 (existing). Mounted device inventory exposes no LSP/semantic-symbol tool; textual inspection used, no refactor attempted.

Exact clone commands (each exit 0):

```sh
mkdir -p /fast/scratch/hyaku/kasegi-r61/ExecRegression
env TMPDIR=/fast/scratch/hyaku/kasegi-r61/ExecRegression git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo
git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo rev-parse --show-toplevel
git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo checkout --detach 13c8060b343e002339ffd72da37ff74514f82765
git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo rev-parse HEAD
git -C /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo diff c33d24ddd11abf1ebdea0dccf7327e9069dd9104 13c8060b343e002339ffd72da37ff74514f82765 -- corpus/instruments/figure-audit.py
```

The rev-parse root result was asserted equal to /fast/scratch/hyaku/kasegi-r61/ExecRegression/repo before checkout. Probe cwd was the exclusive scratch, not fleet root. SHA-256 of base source bytes: 35f7bcd3e673b81b19e431413dec80d7254ce7ab6a50c2c78b8175242cb49ce2. SHA-256 of tested pin source: 051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9, matching frozen claims.

## Round-60 runner

Executed committed round-60 runner from the pinned clone with ONE disclosed adaptation: omitted its fixture-only empty commit line to honor no-commit instruction. git init remains scratch-only; root assertion remains. Q6/Q7 are refused before run_derive, so no HEAD is consulted. This is not a byte-for-byte unmodified runner execution. Its normal exit trap removed Q fixtures. Runner exit 0 alone is not an assertion; the per-probe receipts below are decisive.

Exact execution via Python subprocess (environment TMPDIR as above, cwd=/fast/scratch/hyaku/kasegi-r61/ExecRegression):

```python
runner = Path('/fast/scratch/hyaku/kasegi-r61/ExecRegression/repo/.ufo/waves/round-60/controls/c1-probe-run-r60.sh').read_text()
commit = '  git -C "$r/repo" -c user.email=t@t -c user.name=t commit -q --allow-empty -m fixture\n'
assert commit in runner
runner = runner.replace(commit, '')
subprocess.run(['/usr/bin/bash', '-c', runner, 'round60-no-commit', '/fast/scratch/hyaku/kasegi-r61/ExecRegression/repo/corpus/instruments/figure-audit.py', '/fast/scratch/hyaku/kasegi-r61/ExecRegression/q-probes'], cwd='/fast/scratch/hyaku/kasegi-r61/ExecRegression', env=env, text=True, capture_output=True)
```

Verbatim stdout/stderr, exit 0:

```text
instrument=/fast/scratch/hyaku/kasegi-r61/ExecRegression/repo/corpus/instruments/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:41Z host=plazir27
probe=Q1-escape-single derive=cat g.txt \'; touch MARK-Q1; \' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q1-escape-single
probe=Q2-escape-double derive=cat g.txt \"; touch MARK-Q2; \" exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q2-escape-double
probe=Q3-sed-in-program derive=sed -n '1e touch MARK-Q3' g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q3-sed-in-program
probe=Q4-awk-system derive=awk 'BEGIN{system("touch MARK-Q4")}' exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q4-awk-system
probe=Q5-sort-output-flag derive=sort -o MARK-Q5 g.txt exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q5-sort-output-flag
probe=Q6-git-show-output derive=git show --output=MARK-Q6 HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q6-git-show-output
probe=Q7-git-show-ext-diff derive=git show --ext-diff HEAD exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=Q7-git-show-ext-diff
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
probe=RESIDUAL-python-traversal derive=python3 corpus/instruments/../../../above-evil.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=RESIDUAL-python-traversal

```

The traversal row intentionally changes from admission to refusal. No payload file was installed for this row; refusal is established by exit 2 / derive-not-read-only rather than by a failed interpreter.

## Root-argument comparison matrix

Command: `env TMPDIR=/fast/scratch/hyaku/kasegi-r61/ExecRegression PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kasegi-r61/ExecRegression/matrix.py`, cwd=/fast/scratch/hyaku/kasegi-r61/ExecRegression; exit 0. Actual invocation used the equivalent inherited env dictionary. Base and pin loaded in distinct dictionaries without invoking main. Base predicate receives command; pin predicate receives root and command. Six roots × 32 command strings; no derives executed. Absolute/relative/symlink roots address actual fixtures; dot/empty/None address scratch cwd (no instruments fixture there), intentionally exercising fallback behavior.

Retained complete driver (scratch removed after receipt capture):

```python
import importlib.util
import os
from pathlib import Path
import subprocess

S = Path('/fast/scratch/hyaku/kasegi-r61/ExecRegression')
R = S / 'repo'
os.environ['TMPDIR'] = str(S)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.chdir(S)
base_source = subprocess.check_output(['git', '-C', str(R), 'show', 'c33d24ddd11abf1ebdea0dccf7327e9069dd9104:corpus/instruments/figure-audit.py'], text=True)
base = {'__name__': 'base'}
exec(compile(base_source, 'base-figure-audit.py', 'exec'), base)
new = {'__name__': 'pinned'}
exec(compile((R / 'corpus/instruments/figure-audit.py').read_text(), 'pinned-figure-audit.py', 'exec'), new)
root = S / 'matrix-root'
instruments = root / 'corpus/instruments'
instruments.mkdir(parents=True)
(instruments / 'sub').mkdir()
(instruments / 'ok.py').write_text('print(35)\n')
(root / 'out.py').write_text('print(35)\n')
(instruments / 'link-out.py').symlink_to(root / 'out.py')
(instruments / 'link-in.py').symlink_to(instruments / 'ok.py')
(S / 'root-link').symlink_to(root, target_is_directory=True)
roots = [('absolute', str(root)), ('relative', 'matrix-root'), ('symlink', str(S / 'root-link')), ('dot', '.'), ('empty', ''), ('none', None)]
commands = [
    'cat g.txt', 'cat g.txt | wc -l', "cat g.txt | grep -e '35' -e ';'",
    'cat g.txt; touch MARK', 'cat g.txt && touch MARK',
    'sed -n 1p g.txt', "awk 'BEGIN{print 35}'", 'sort -o MARK g.txt',
    'git show --output=MARK HEAD', 'git show --ext-diff HEAD',
    'git show HEAD', 'git cat-file -p HEAD', 'git ls-tree HEAD',
    'cat g.txt | sh', 'echo 35', 'python3 -c print35',
    'python3 /outside.py', 'python3', 'python3 corpus/instruments/ok.py',
    'python corpus/instruments/ok.py', 'python3 corpus/instruments/sub/../ok.py',
    'python3 corpus/instruments/../../out.py',
    'python3 corpus/instruments/../../../above-evil.py',
    'python3 corpus/instruments/link-out.py', 'python3 corpus/instruments/link-in.py',
    'python3 corpus/instruments/..', 'python3 corpus/instruments/',
    'python3 corpus/instruments/missing.py',
    'python3 corpus/instruments/ok.py | wc -l',
    'cat g.txt && python3 corpus/instruments/../../out.py',
    "sort '--output=MARK' g.txt", "cat g.txt #'\ntouch MARK #'",
]
counts = {'same_admit': 0, 'same_refuse': 0, 'tightened': 0, 'new_admission': 0}
for root_id, root_arg in roots:
    for index, command in enumerate(commands, 1):
        old = base['check_read_only'](command)
        current = new['check_read_only'](root_arg, command)
        kind = ('same_admit' if old else 'new_admission') if current else ('tightened' if old else 'same_refuse')
        counts[kind] += 1
        print(f'root={root_id} case={index:02d} base={int(old)} pin={int(current)} class={kind} command={command!r}')
print(f'MATRIX roots={len(roots)} commands={len(commands)} calls={len(roots)*len(commands)} {counts}')
assert counts['new_admission'] == 0
print('MATRIX PASS no new admission; direct predicate calls only, no derives executed')

```

Verbatim matrix receipt, exit 0:

```text
root=absolute case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=absolute case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=absolute case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=absolute case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=absolute case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=absolute case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=absolute case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=absolute case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=absolute case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=absolute case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=absolute case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=absolute case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=absolute case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=absolute case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=absolute case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=absolute case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=absolute case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=absolute case=18 base=0 pin=0 class=same_refuse command='python3'
root=absolute case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=absolute case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=absolute case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=absolute case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=absolute case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=absolute case=24 base=1 pin=0 class=tightened command='python3 corpus/instruments/link-out.py'
root=absolute case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=absolute case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=absolute case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=absolute case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=absolute case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=absolute case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=absolute case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=absolute case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
root=relative case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=relative case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=relative case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=relative case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=relative case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=relative case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=relative case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=relative case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=relative case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=relative case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=relative case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=relative case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=relative case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=relative case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=relative case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=relative case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=relative case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=relative case=18 base=0 pin=0 class=same_refuse command='python3'
root=relative case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=relative case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=relative case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=relative case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=relative case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=relative case=24 base=1 pin=0 class=tightened command='python3 corpus/instruments/link-out.py'
root=relative case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=relative case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=relative case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=relative case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=relative case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=relative case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=relative case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=relative case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
root=symlink case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=symlink case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=symlink case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=symlink case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=symlink case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=symlink case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=symlink case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=symlink case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=symlink case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=symlink case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=symlink case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=symlink case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=symlink case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=symlink case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=symlink case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=symlink case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=symlink case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=symlink case=18 base=0 pin=0 class=same_refuse command='python3'
root=symlink case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=symlink case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=symlink case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=symlink case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=symlink case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=symlink case=24 base=1 pin=0 class=tightened command='python3 corpus/instruments/link-out.py'
root=symlink case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=symlink case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=symlink case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=symlink case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=symlink case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=symlink case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=symlink case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=symlink case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
root=dot case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=dot case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=dot case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=dot case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=dot case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=dot case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=dot case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=dot case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=dot case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=dot case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=dot case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=dot case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=dot case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=dot case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=dot case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=dot case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=dot case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=dot case=18 base=0 pin=0 class=same_refuse command='python3'
root=dot case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=dot case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=dot case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=dot case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=dot case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=dot case=24 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-out.py'
root=dot case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=dot case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=dot case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=dot case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=dot case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=dot case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=dot case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=dot case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
root=empty case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=empty case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=empty case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=empty case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=empty case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=empty case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=empty case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=empty case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=empty case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=empty case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=empty case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=empty case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=empty case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=empty case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=empty case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=empty case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=empty case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=empty case=18 base=0 pin=0 class=same_refuse command='python3'
root=empty case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=empty case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=empty case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=empty case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=empty case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=empty case=24 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-out.py'
root=empty case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=empty case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=empty case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=empty case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=empty case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=empty case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=empty case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=empty case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
root=none case=01 base=1 pin=1 class=same_admit command='cat g.txt'
root=none case=02 base=1 pin=1 class=same_admit command='cat g.txt | wc -l'
root=none case=03 base=1 pin=1 class=same_admit command="cat g.txt | grep -e '35' -e ';'"
root=none case=04 base=0 pin=0 class=same_refuse command='cat g.txt; touch MARK'
root=none case=05 base=0 pin=0 class=same_refuse command='cat g.txt && touch MARK'
root=none case=06 base=0 pin=0 class=same_refuse command='sed -n 1p g.txt'
root=none case=07 base=0 pin=0 class=same_refuse command="awk 'BEGIN{print 35}'"
root=none case=08 base=0 pin=0 class=same_refuse command='sort -o MARK g.txt'
root=none case=09 base=0 pin=0 class=same_refuse command='git show --output=MARK HEAD'
root=none case=10 base=0 pin=0 class=same_refuse command='git show --ext-diff HEAD'
root=none case=11 base=1 pin=1 class=same_admit command='git show HEAD'
root=none case=12 base=1 pin=1 class=same_admit command='git cat-file -p HEAD'
root=none case=13 base=1 pin=1 class=same_admit command='git ls-tree HEAD'
root=none case=14 base=0 pin=0 class=same_refuse command='cat g.txt | sh'
root=none case=15 base=0 pin=0 class=same_refuse command='echo 35'
root=none case=16 base=0 pin=0 class=same_refuse command='python3 -c print35'
root=none case=17 base=0 pin=0 class=same_refuse command='python3 /outside.py'
root=none case=18 base=0 pin=0 class=same_refuse command='python3'
root=none case=19 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py'
root=none case=20 base=1 pin=1 class=same_admit command='python corpus/instruments/ok.py'
root=none case=21 base=1 pin=1 class=same_admit command='python3 corpus/instruments/sub/../ok.py'
root=none case=22 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../out.py'
root=none case=23 base=1 pin=0 class=tightened command='python3 corpus/instruments/../../../above-evil.py'
root=none case=24 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-out.py'
root=none case=25 base=1 pin=1 class=same_admit command='python3 corpus/instruments/link-in.py'
root=none case=26 base=1 pin=0 class=tightened command='python3 corpus/instruments/..'
root=none case=27 base=1 pin=0 class=tightened command='python3 corpus/instruments/'
root=none case=28 base=1 pin=1 class=same_admit command='python3 corpus/instruments/missing.py'
root=none case=29 base=1 pin=1 class=same_admit command='python3 corpus/instruments/ok.py | wc -l'
root=none case=30 base=1 pin=0 class=tightened command='cat g.txt && python3 corpus/instruments/../../out.py'
root=none case=31 base=1 pin=1 class=same_admit command="sort '--output=MARK' g.txt"
root=none case=32 base=1 pin=1 class=same_admit command="cat g.txt #'\ntouch MARK #'"
MATRIX roots=6 commands=32 calls=192 {'same_admit': 87, 'same_refuse': 72, 'tightened': 33, 'new_admission': 0}
MATRIX PASS no new admission; direct predicate calls only, no derives executed

```

192 comparisons = 87 unchanged admissions + 72 unchanged refusals + 33 tightenings + 0 new admissions. The external-symlink case tightens for the three fixture roots; dot/empty/None do not resolve to that fixture and still accept the nonexistent prefixed script. This is consistent with no existence check, not a new admission.

## Path:line evidence at the implementation pin

- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/controls/c1-probe-run-r60.sh:48-59 — seven historical probes, controls, traversal residual.
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-60/controls/c1-probe-run-r60.sh:38-40 — fixture init/empty commit/root assertion; commit omitted only in executed in-memory runner.
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:172-187 — literal prefix, root-relative realpath, reject directory itself, separator-delimited containment.
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:190-203 — root threaded through segment and all-segments predicates; non-Python branch unchanged.
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:225-228 — refusal exits before run_derive.
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:353-361 — CLI default root and --root passed into audit.

These references were read in the pinned clone at corresponding absolute scratch paths; lane was not used as the executable source.

## Risks and limits

Bounded evidence only: 192 observations are not a universal sandbox proof. Missing prefixed scripts still pass this predicate. Known quoted-sort-flag and phantom-comment/newline cases remain admitted in both versions (matrix cases 31/32); no execution claim is made for this wave's direct calls. No complete C1 counting suite or C2 checks were assigned/run. The no-commit runner adaptation means the exact committed runner with a fixture HEAD was not run; pre-execution refusal makes HEAD irrelevant to the observed Q6/Q7 result.

## Cleanup and self-evaluation

Executed Python `shutil.rmtree("/fast/scratch/hyaku/kasegi-r61/ExecRegression")`; completed normally; observed `scratch_exists=False`. All scratch sources, fixtures and clone removed. Complete decisive receipts are retained in this report. No tools installed/updated.

Self-evaluation (1–5): accuracy 4 (explicit runner adaptation, not exact-byte runner); completeness 4 (bounded matrix, not exhaustive); clarity 4 (full receipt is long); actionability 5 (pins, commands, driver, outcomes retained); conciseness 4 (raw matrix retained for auditability). Mean 4.2. Improvements by impact: exact runner requires permission for fixture commits; broader root matrix belongs only to a separately assigned scope. User agreement expected because limitations are explicit.

Report: .ufo/waves/round-61/w1/ExecRegression.md
