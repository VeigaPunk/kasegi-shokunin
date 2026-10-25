#!/usr/bin/env python3
"""Assemble the canonical round-28 receipts at the landed digest (defect 4:
one canonical receipt index; run by the L1 after all production lands and
the wave evidence is committed)."""
import json, os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
R28 = ".ufo/waves/round-28"

def run(cmd, cwd=LANE):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return p.stdout + (p.stderr or ""), p.returncode

def main():
    lines = []
    def L(s=""):
        lines.append(s)
        print(s)

    digest = subprocess.run(["sha256sum", "corpus/instruments/anchorcheck.py"],
                            cwd=LANE, capture_output=True, text=True).stdout.split()[0]
    L("== round-28 canonical C1 receipt index (assembled at landed digest) ==")
    L(f"instrument_sha256={digest}")
    L("")
    out, rc = run("python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md")
    L("== counter (a) bad-fixture ==")
    L(out.strip())
    L(f"exit={rc}")
    L("")
    out, rc = run("python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null")
    n = out.count("BOUNTIES-ABSENT")
    L("== counter (b) bounties-fixture ==")
    L(out.strip())
    L(f"BOUNTIES-ABSENT_lines={n}")
    L(f"exit={rc}")
    L("")
    out, rc = run("python3 corpus/instruments/anchorcheck.py --selftest")
    L("== counter (c) --selftest ==")
    L(out.strip())
    L(f"exit={rc}")
    L("")
    out, rc = run("python3 corpus/instruments/anchorcheck.py SKILL.md")
    L("== counter (d) SKILL.md no-harm ==")
    L(next((line for line in out.splitlines() if line.startswith("== ")), "(summary missing)"))
    L(f"exit={rc}")
    L("")
    out, rc = run("python3 corpus/instruments/recheck-audit.py")
    L("== recheck-audit expected-list gate ==")
    L(out.strip())
    L(f"exit={rc}")
    L("")
    out, rc = run("awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md")
    L("== C2 frontier count =="); L(f"frontier_admitted={out.strip()}"); L(f"exit={rc}")
    out, rc = run("grep -lE '^source: S042 ' corpus/knowledge/*.md 2>/dev/null | wc -l")
    L("== C2 entries citing S042 =="); L(f"entries={out.strip()}"); L(f"exit={rc}")
    out, rc = run("grep -cE '^\\|[[:space:]]*S042[[:space:]]*\\|' corpus/SOURCES.md")
    L("== C2 S042 row =="); L(f"s042_rows={out.strip()}"); L(f"exit={rc}")
    out, rc = run("python3 corpus/instruments/frontier-recheck-count.py")
    L("== C2 harness =="); L(out.strip()); L(f"exit={rc}")
    out, rc = run("grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md")
    L("== registry rows =="); L(f"rows={out.strip()}"); L(f"exit={rc}")

    with open(os.path.join(LANE, R28, "c1-receipt-index.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
