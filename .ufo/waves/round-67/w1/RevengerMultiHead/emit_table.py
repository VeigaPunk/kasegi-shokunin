#!/usr/bin/env python3
"""Emit the human-readable receipt table from the probe JSONs."""
import hashlib
import json
import os
import sys

S = "/fast/scratch/hyaku/kasegi-r67/RevengerMultiHead"
probe = json.load(open(os.path.join(S, "probe.json")))
fup = json.load(open(os.path.join(S, "followup.json")))
st3 = json.load(open(os.path.join(S, "stage3.json")))
order = json.load(open(os.path.join(S, "order.json")))
out = []
w = out.append

w("# kasegi round-67 / RevengerMultiHead — native receipt table")
w("")
w("Every pipeline below was started with python subprocess argv lists; no shell was used.")
w("A stage0 status of -13 is SIGPIPE.  'miss' = stage0 stderr named the missing operand")
w("(positive proof the later operand WAS opened); 'miss=-' = stderr never named it.")
w("")
w("## host")
w("kernel            = Linux 7.2.11-arch1-1 x86_64")
w("python            = 3.14.8 (GCC 16.2.1)")
w("pipe capacity     = %s bytes (F_GETPIPE_SZ)" % probe["pipe_capacity"])
w("gate sha256       = %s" % st3["gate_sha256"])
w("tools             = cut/wc/sort/head/tail/sha256sum/tr/ls/cat 0.8.0 (uutils);"
  " grep = 'grep (pi-uu-grep) 0.2.0'")
w("")
w("## fixtures (deterministic, 1024-byte lines)")
w("line 1   = b'alpha:' + b'a'*1017 + b'\\n'   (grep alpha matches exactly this line)")
w("line 2..k= b'x'*1023 + b'\\n'                (grep x matches every line)")
w("file size= k*1024 exactly; missing.txt is never created.")
w("")
w("%-12s %-10s %-6s %s" % ("bytes", "KiB", "lines", "sha256"))
for k in sorted(probe["fixtures"], key=int):
    f = probe["fixtures"][k]
    w("%-12s %-10s %-6s %s" % (f["bytes"], f["bytes"] // 1024, f["lines"], f["sha256"]))
w("")
w("## exact argv (stage lists)")
w("  cat       : ['cat', F, (M)]                       | ['head','-n','1']")
w("  cut       : ['cut','-f1','-d:', F, (M)]           | ['head','-n','1']")
w("  wc        : ['wc','-l', F, (M)]                   | ['head','-n','1']")
w("  grep-many : ['grep','x', F, (M)]                  | ['head','-n','1']")
w("  grep-few  : ['grep','alpha', F, (M)]              | ['head','-n','1']")
w("  sort      : ['sort', F, (M)]                      | ['head','-n','1']")
w("  head-n5   : ['head','-n','5', F, (M)]             | ['head','-n','1']")
w("  head-all  : ['head','-n','100000', F, (M)]        | ['head','-n','1']")
w("  tail      : ['tail', F, (M)]                      | ['head','-n','1']")
w("  tail-all  : ['tail','-n','+1', F, (M)]            | ['head','-n','1']")
w("  sha256sum : ['sha256sum', F, (M)]                 | ['head','-n','1']")
w("  ls        : ['ls', F, (M)]                        | ['head','-n','1']")
w("  tr        : ['tr','a','b', F, (M)]  (tr takes no file operands) | ['head','-n','1']")
w("  cat|tr    : ['cat', F, M] | ['tr','a','b'] | ['head','-n','1']")
w("F = absolute fixture path, M = <work>/missing.txt (absent).")
w("")
w("## TABLE A — full table at 64 KiB / 1 MiB / 4 MiB (7 repeats each)")
w("%-26s %-10s %-14s %-8s %s" % ("shape", "size", "stage0 rc", "stage1", "miss"))
for r in probe["main"]:
    tag = r["tag"]
    size = tag.split()[0].split("=")[1]
    name = tag.split(" ", 1)[1]
    w("%-26s %-10s %-14s %-8s %s" % (name, size, r["stage0_rc"], r["stage1_rcs_seen"],
                                     r["stage0_stderr_mentions_missing"]))
w("")
w("## TABLE B — 4 MiB stability (40 repeats, shapes that carry a later operand)")
w("%-26s %-16s %s" % ("shape", "stage0 rc", "sigpipe"))
for r in st3["four_mib_stability"]:
    w("%-26s %-16s %s" % (r["tag"], r["rc0"], r["sigpipe_rate"]))
w("")
w("## TABLE C — size sweep, 2-operand shapes (15 repeats; 40 where marked)")
w("%-26s %-6s %-16s %-8s %s" % ("shape", "KiB", "stage0 rc", "miss", "reps"))
for key, reps in (("cat_threshold", 15), ("cut_threshold", 15), ("grep_threshold", 15),
                  ("headall_threshold", 15)):
    for r in fup[key]:
        kib = int(r["tag"].split()[0].split("=")[1]) // 1024
        w("%-26s %-6s %-16s %-8s %s" % (r["tag"].split(" ", 1)[1], kib, r["rc0_seen"],
                                        r["err_mentions_missing_any"], reps))
for r in st3["cat_bisect"]:
    kib = int(r["tag"].split()[-1]) // 1024
    w("%-26s %-6s %-16s %-8s %s" % ("cat+missing", kib, r["rc0"], "-", 40))
w("")
w("## TABLE D — premise falsifiers (later operand WAS read, status still -13)")
for r in fup["wc_falsifier"]:
    w("%-24s rc0=%-12s miss_all=%s" % (r["tag"], r["rc0_seen"], r["err_mentions_missing_all"]))
    w("    stdout=%r" % r["rows"][0]["out_head"])
    w("    stderr=%r" % r["rows"][0]["err"])
w("")
w("## TABLE E — rule fires on worlds where EVERY operand was read (7 repeats)")
for r in fup["rule_fires_on_read_world"]:
    w("%-26s rc0=%s stable=%s" % (r["tag"], r["rc0_seen"], r["rc0_stable"]))
w("")
w("## TABLE F — production gate, unchanged, read-only, over scratch ledgers")
w("(each ledger records exactly what the shape prints; base verdict printed below)")
for line in st3["gate_verdicts"]:
    if line.startswith("FIG "):
        w("  %s -> %s" % (line.split()[1], line.split()[-1]))
    else:
        w("  " + line)
w("  exit=%d" % st3["gate_exit"])
w("")
w("## TABLE G — reversed operand order (missing first, 4 MiB second; 10 repeats)")
for k, v in order.items():
    w("%-24s rcs=%s" % (k, v["rcs"]))
    w("    stderr=%r" % v["err"][0][:100])
w("")
w("## TABLE H — residuals")
w("python flood (200000 lines) | head -n 1 : stage0 rc = %s (BrokenPipeError -> exit 1, never -13)"
  % fup["python_residual"][0]["rc0_seen"])
w("git ls-files (20000 entries, 220000 B) | head -n 1 : stage0 rc = -13 (5/5)")
w("")
w("## strace openat evidence (observational layer; strace slows the child)")
for r in fup["strace_opens"]:
    w("%-22s rc=%-10s opens_first=%-6s opens_missing=%s" %
      (r["tag"], r["rcs"], r["opens_first"], r["opens_missing"]))
w("")
sys.stdout.write("\n".join(out) + "\n")
