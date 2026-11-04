#!/bin/sh
# ScoutCommands r64 native exit-code recon. One invocation per receipt.
# Receipt = run-utc line + exact argv line + raw output/stderr + rc line.
set -u
S=/fast/scratch/hyaku/kasegi-r64/ScoutCommands
OUT=$S/receipts
mkdir -p "$OUT"
cd "$S"
printf '35\n' > g.txt
: > empty.txt
mkdir -p repo/.git/objects repo/.git/refs/heads
printf 'ref: refs/heads/main\n' > repo/.git/HEAD

receipt() {
  name=$1; shift
  {
    printf 'run-utc='; date -u '+%Y-%m-%dT%H:%M:%SZ'
    printf '$'; for a in "$@"; do printf ' %s' "$a"; done; printf '\n'
    "$@"
    printf 'rc=%d\n' "$?"
  } >"$OUT/$name.txt" 2>&1
}
pipe() {
  name=$1; script=$2
  {
    printf 'run-utc='; date -u '+%Y-%m-%dT%H:%M:%SZ'
    printf '$ /bin/sh -c %s\n' "$script"
    /bin/sh -c "$script"
    printf 'rc=%d\n' "$?"
  } >"$OUT/$name.txt" 2>&1
}

{
  date -u '+run-utc=%Y-%m-%dT%H:%M:%SZ'
  /usr/bin/cat --version | /usr/bin/head -1
  /usr/bin/git --version
  /usr/bin/python3 --version
  printf '/bin/sh -> %s\n' "$(readlink -f /bin/sh)"
  /bin/sh -c 'echo sh-version-ok'
  for t in cat cut head tail ls sort tr wc sha256sum grep git python3 date; do
    printf '%s=%s\n' "$t" "$(command -v "$t")"
  done
  if command -v dash >/dev/null 2>&1; then
    dash -c 'set -o pipefail; true | false' >/dev/null 2>&1; printf 'dash-pipefail-rc=%d\n' "$?"
  else
    printf 'dash=absent\n'
  fi
} >"$OUT/tools.txt" 2>&1

receipt cat-missing        /usr/bin/cat missing
receipt cat-partial        /usr/bin/cat g.txt missing
receipt cat-partial-first  /usr/bin/cat missing g.txt
receipt cut-missing        /usr/bin/cut -d : -f1 missing
receipt cut-partial        /usr/bin/cut -d : -f1 g.txt missing
receipt head-missing       /usr/bin/head missing
receipt head-partial       /usr/bin/head g.txt missing
receipt tail-missing       /usr/bin/tail missing
receipt ls-missing         /usr/bin/ls missing
receipt sort-missing       /usr/bin/sort missing
receipt sha256sum-missing  /usr/bin/sha256sum missing
receipt tr-missing         /usr/bin/tr a b missing
receipt wc-missing         /usr/bin/wc missing
receipt grep-no-match      /usr/bin/grep absent g.txt
receipt grep-match         /usr/bin/grep 35 g.txt
receipt grep-missing-file  /usr/bin/grep absent missing
receipt grep-invalid-regex /usr/bin/grep '[' g.txt
receipt git-show-missing-ref    /usr/bin/git -C "$S/repo" show refs/heads/figure-audit-nonexistent
receipt git-cat-file-e-missing  /usr/bin/git -C "$S/repo" cat-file -e 0123456789012345678901234567890123456789
receipt python-exit1       /usr/bin/python3 -c 'import sys; sys.exit(1)'
receipt python-exit2       /usr/bin/python3 -c 'import sys; sys.exit(2)'
receipt sort-c-disordered  /usr/bin/sort -c empty.txt
receipt sort-c-ok          /usr/bin/sort -c g.txt

pipe pipe-cat-missing-wc      'cat missing | wc -l'
pipe pipe-cat-partial-wc      'cat g.txt missing | wc -l'
pipe pipe-cut-missing-wc      'cut -d: -f1 missing | wc -l'
pipe pipe-head-missing-wc     'head missing | wc -l'
pipe pipe-tail-missing-wc     'tail missing | wc -l'
pipe pipe-ls-missing-wc       'ls missing | wc -l'
pipe pipe-sort-missing-wc     'sort missing | wc -l'
pipe pipe-sha256sum-missing-wc 'sha256sum missing | wc -l'
pipe pipe-tr-missing-wc       'tr a b missing | wc -l'
pipe pipe-grep-no-match-wc    'grep absent g.txt | wc -l'
pipe pipe-success-pipeline    'cat g.txt | wc -l'
pipe pipe-and-chain-ok        'cat g.txt && grep 35 g.txt'
pipe pipe-and-chain-grepfail  'cat g.txt && grep absent g.txt'
pipe pipe-and-chain-fail      'cat missing && echo no'
pipe pipefail-sha256sum-wc    'set -o pipefail; sha256sum missing | wc -l'
pipe pipefail-ls-wc           'set -o pipefail; ls missing | wc -l'
pipe pipefail-sort-wc         'set -o pipefail; sort missing | wc -l'
pipe pipefail-grep-wc         'set -o pipefail; grep absent g.txt | wc -l'
pipe pipefail-two-fails       'set -o pipefail; ls missing | cat missing2 | wc -l'
pipe pipe-signal-upstream     'yes | head -1'
pipe pipe-signal-pipestatus   'yes | head -1 > /dev/null; echo pipestatus=${PIPESTATUS[*]}'

# PIPESTATUS is bash-only; run that one receipt under /bin/bash explicitly.
{
  printf 'run-utc='; date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf '$ /bin/bash -c %s\n' "'yes | head -1 > /dev/null; echo pipestatus=\${PIPESTATUS[*]}'"
  /bin/bash -c 'yes | head -1 > /dev/null; echo pipestatus=${PIPESTATUS[*]}'
  printf 'rc=%d\n' "$?"
} >"$OUT/pipe-signal-pipestatus-bash.txt" 2>&1

echo DONE
