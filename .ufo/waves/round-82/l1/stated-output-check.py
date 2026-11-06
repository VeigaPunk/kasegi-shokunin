import re, subprocess, sys
# Run every backticked command an entry says "prints nothing and exits 1"; report mismatches.
txt = open(sys.argv[1], encoding="utf-8").read()
bad = 0; n = 0
for m in re.finditer(r"`([^`]+)` prints nothing and exits 1", txt):
    n += 1
    p = subprocess.run(["bash", "-c", m.group(1)], capture_output=True, text=True, cwd=sys.argv[2])
    ok = p.returncode == 1 and p.stdout == ""
    bad += 0 if ok else 1
    print("%s rc=%d out_lines=%d :: %s" % ("OK  " if ok else "FAIL", p.returncode, len(p.stdout.splitlines()), m.group(1)[:90]))
print("STATED-OUTPUT commands=%d mismatches=%d" % (n, bad))
sys.exit(1 if bad else 0)
