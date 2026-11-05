#!/usr/bin/env bash
# ExecC1Amend verification battery. Every command's exit code is recorded.
set -u
S=/fast/scratch/hyaku/kasegi-r74/ExecC1Amend
L=/home/vgpnk/Projects/shokunin/kasegi-shokunin
A="$S/lane/corpus/instruments/recheck-cwd-census.py"
O="$S/out"
mkdir -p "$O" "$S/tmp" "$S/tmp-unset-scratch"
cd "$S" || exit 9

# Rebuild mutants M4-M7 from the FINAL amended counter (python builder, exits nonzero on anchor miss).
python3 - "$S" <<'PY' || { echo "MUTANT-BUILD-FAILED"; exit 9; }
import pathlib, sys
S = pathlib.Path(sys.argv[1])
amended = (S / "lane/corpus/instruments/recheck-cwd-census.py").read_text()
def sub(text, old, new):
    assert text.count(old) == 1, (text.count(old), old[:60])
    return text.replace(old, new)
m4 = sub(amended,
  'print("RECHECK-CWD-RESULT %s" % ("conformant" if conform else "nonconformant"))',
  'print("RECHECK-CWD-RESULT %s" % "conformant")')
m5 = sub(amended,
  'scratch = tempfile.mkdtemp(prefix="recheck-cwd-", dir=env_tmp)',
  'scratch = tempfile.mkdtemp(prefix="recheck-cwd-", dir="/tmp")')
a = amended.index("def run_foreign"); b = amended.index("def census")
m6 = amended[:a] + sub(amended[a:b], "    finally:\n        shutil.rmtree(scratch, ignore_errors=True)",
                       "    finally:\n        pass") + amended[b:]
a = amended.index("def first_recheck"); b = amended.index("def run_foreign")
m7 = amended[:a] + sub(amended[a:b],
  '    with open(path, encoding="utf-8", errors="replace") as fh:\n'
  '        for line in fh:\n'
  '            if line.startswith("recheck:"):\n'
  '                return line[len("recheck:"):].strip()\n'
  '    return None',
  '    value = None\n'
  '    with open(path, encoding="utf-8", errors="replace") as fh:\n'
  '        for line in fh:\n'
  '            if line.startswith("recheck:"):\n'
  '                value = line[len("recheck:"):].strip()\n'
  '    return value') + amended[b:]
for mid, text in (("M4", m4), ("M5", m5), ("M6", m6), ("M7", m7)):
    (S / f"mut-{mid}.py").write_text(text)
print("mutants-built")
PY
echo "mutant-build-exit=$?"

echo "== (i) amended selftest (TMPDIR set)"
TMPDIR="$S/tmp" python3 "$A" --selftest > "$O/selftest.txt" 2>&1; echo "selftest-exit=$?" | tee -a "$O/selftest.txt"; cat "$O/selftest.txt"

echo "== (i-b) amended selftest (TMPDIR UNSET, run from scratch cwd)"
( cd "$S/tmp-unset-scratch" && env -u TMPDIR python3 "$A" --selftest > "$O/selftest-unset-tmpdir.txt" 2>&1; echo "selftest-unset-exit=$?" | tee -a "$O/selftest-unset-tmpdir.txt" ); cat "$O/selftest-unset-tmpdir.txt"

echo "== (ii) amended census on clone tree"
TMPDIR="$S/tmp" python3 "$A" --root "$S/lane" --lane "$L" > "$O/census-clone.txt" 2>&1; echo "census-clone-exit=$?" | tee -a "$O/census-clone.txt"; cat "$O/census-clone.txt"
echo "knowledge-files-on-clone=$(ls "$S/lane/corpus/knowledge"/*.md | wc -l)"

echo "== (iii) parity limb"
TMPDIR="$S/tmp" python3 "$S/orig.py" --root "$S/base/repo" --lane "$L" > "$O/parity-orig.txt" 2>&1; echo "parity-orig-exit=$?" | tee -a "$O/parity-orig.txt"
TMPDIR="$S/tmp" python3 "$A" --root "$S/base/repo" --lane "$L" > "$O/parity-amended.txt" 2>&1; echo "parity-amended-exit=$?" | tee -a "$O/parity-amended.txt"
cmp "$O/parity-orig.txt" "$O/parity-amended.txt"; echo "parity-cmp-exit=$?"
echo "--- parity-orig:"; cat "$O/parity-orig.txt"; echo "--- parity-amended:"; cat "$O/parity-amended.txt"

echo "== (iv) kill battery: amended selftest under each mutant (TMPDIR set)"
for m in M4 M5 M6 M7; do
  TMPDIR="$S/tmp" python3 "$S/mut-$m.py" --selftest > "$O/kill-$m-selftest.txt" 2>&1; echo "kill-$m-selftest-exit=$?" | tee -a "$O/kill-$m-selftest.txt"
done
echo "== (iv-b) kill battery under TMPDIR UNSET"
for m in M4 M5 M6 M7; do
  ( cd "$S/tmp-unset-scratch" && env -u TMPDIR python3 "$S/mut-$m.py" --selftest > "$O/kill-$m-selftest-unset.txt" 2>&1; echo "kill-$m-selftest-unset-exit=$?" | tee -a "$O/kill-$m-selftest-unset.txt" )
done
for m in M4 M5 M6 M7; do echo "--- $m (TMPDIR set):"; cat "$O/kill-$m-selftest.txt"; echo "--- $m (TMPDIR unset):"; cat "$O/kill-$m-selftest-unset.txt"; done

echo "== (iv-c) informational: each mutant census on base export vs orig"
for m in M4 M5 M6 M7; do
  rm -rf "$S/tmp-$m"; mkdir -p "$S/tmp-$m"
  TMPDIR="$S/tmp-$m" python3 "$S/mut-$m.py" --root "$S/base/repo" --lane "$L" > "$O/info-census-$m.txt" 2>&1; echo "info-census-$m-exit=$?" | tee -a "$O/info-census-$m.txt"
  echo "info-census-$m-leftover-recheck-dirs=$(ls -d "$S/tmp-$m"/recheck-cwd-* 2>/dev/null | wc -l)"
  cat "$O/info-census-$m.txt"
done

echo "== (v) leak check on amended counter (clean TMPDIR)"
rm -rf "$S/tmp-amended-leak"; mkdir -p "$S/tmp-amended-leak"
TMPDIR="$S/tmp-amended-leak" python3 "$A" --selftest > /dev/null 2>&1; echo "leak-selftest-exit=$?"
echo "leak-selftest-leftover=$(ls -d "$S/tmp-amended-leak"/recheck-cwd-* 2>/dev/null | wc -l)"
TMPDIR="$S/tmp-amended-leak" python3 "$A" --root "$S/base/repo" --lane "$L" > /dev/null 2>&1; echo "leak-census-exit=$?"
echo "leak-census-leftover=$(ls -d "$S/tmp-amended-leak"/recheck-cwd-* 2>/dev/null | wc -l)"

echo "== (vi) constraint greps"
echo "grep-bash-literal-call-orig=$(grep -c '\["bash", "-c"' "$S/orig.py")  amended=$(grep -c '\["bash", "-c"' "$A")"
echo "grep-bash-any-orig=$(grep -c 'bash' "$S/orig.py")  amended=$(grep -c 'bash' "$A")"
echo "grep-subprocess-orig=$(grep -c 'subprocess' "$S/orig.py")  amended=$(grep -c 'subprocess' "$A")"
echo "--- /tmp literal lines in amended:"; grep -n '/tmp' "$A"; echo "grep-tmp-exit=$?"
echo "--- bash lines in amended:"; grep -n 'bash' "$A"; echo "grep-bash-lines-exit=$?"
echo "--- --selftest/--root/--lane/--verbose usage preserved:"; grep -n -- '--selftest\|--root\|--lane\|--verbose' "$A" | head -n 20
echo "== (vii) git scope"
git -C "$S/lane" diff --stat ccd6a54bf392922495c4860332665499582e3213 -- corpus/instruments/recheck-cwd-census.py
git -C "$S/lane" diff --name-only
