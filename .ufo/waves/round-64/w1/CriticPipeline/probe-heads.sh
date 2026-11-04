#!/usr/bin/bash
S=/fast/scratch/hyaku/kasegi-r64/CriticPipeline
cd "$S/work" || exit 9
echo "run_utc=$(date -u +%FT%TZ)"
for b in grep cat cut head tail ls sort sha256sum wc; do printf '%s -> %s\n' "$b" "$(readlink -f /usr/bin/$b)"; done
/usr/bin/grep --version | head -2
/usr/bin/cat --version | head -1
/usr/bin/ls --version | head -1
while IFS= read -r c; do
  /usr/bin/bash -c "$c" >/dev/null 2>"$S/work/err.txt"; rc=$?
  printf '%-40s rc=%-4s err=%s\n' "$c" "$rc" "$(head -c 100 "$S/work/err.txt" | tr '\n' ' ')"
done <<'CMDS'
/usr/bin/grep absent g.txt
/usr/bin/grep '[' g.txt
/usr/bin/grep 35 missing.txt
/usr/bin/grep -s 35 missing.txt
/usr/bin/grep 35 adir
/usr/bin/grep -q absent missing.txt
/usr/bin/grep 35 g.txt missing.txt
/usr/bin/grep -c absent g.txt
/usr/bin/grep -a x bin.dat
/usr/bin/grep -r absent nosuchdir
/usr/bin/grep -E '(' g.txt
/usr/bin/grep -P '(' g.txt
/usr/bin/cat missing.txt
/usr/bin/cat d_exist.txt missing.txt
/usr/bin/cat adir
/usr/bin/cut -d' ' -f1 missing.txt
/usr/bin/head missing.txt
/usr/bin/tail missing.txt
/usr/bin/ls missing.txt
/usr/bin/sort missing.txt
/usr/bin/sha256sum missing.txt
/usr/bin/wc -l missing.txt
/usr/bin/tr a b missing.txt
/usr/bin/git show refs/nonexistent-zz
CMDS
