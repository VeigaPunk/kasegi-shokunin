#!/usr/bin/env python3
"""round-58 implementation builder (scratch). Builds the C1 + C2 after-state bytes in a shared clone
of the lane (HEAD 1e5c8f2 + the round-58 capture/manifest), runs the frozen after-counting commands
there (stand-in dry run), and writes the stand-in receipts into the lane's controls directory.
The same file bytes are then copied into the lane and cmp-verified (see land-impl.sh)."""
import os, re, shutil, subprocess, sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r58/standin"
K = "/fast/scratch/hyaku/kasegi-r58/pre-frozen/aisi-autonomous-cyber-capability-progress-rate.md"
CTL = os.path.join(L, ".ufo/waves/round-58/controls")
ENV = dict(os.environ, TMPDIR="/fast/scratch/hyaku/kasegi-r58/tmp")


def sh(cmd, cwd):
    p = subprocess.run(["bash", "-c", cmd], cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True, env=ENV)
    return p.stdout, p.returncode


def once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise SystemExit("exact-once failed for %s: count=%d" % (label, n))
    return text.replace(old, new)


# ---------- C1 implementation text ----------
FA_NEW_ROFIXTURE = '''SELFTEST_LEDGER_NOT_RO = {
    "figures": [
        {"id": "s-not-ro", "record": "g.txt:1", "recorded": "35", "derive": "echo 35", "want": "35"},
    ],
}
'''

MUTBAT = r'''#!/usr/bin/env python3
"""figure-audit-mutbat.py - R17 one-limb mutant battery for figure-audit.py's own selftest limbs.

Each mutant is an exact-once edit of the committed instrument bytes; the replay prints one
`MUT <id> ... killed=<0|1>` line per mutant. A mutant is KILLED when its own --selftest exits
nonzero. Two controls must NOT be killed: the pristine instrument (selftest exit 0) and an
equivalent patch (trailing whitespace only). A surviving mutant is a defect of the instrument.

Usage: python3 corpus/instruments/figure-audit-mutbat.py
Exit 0 only when every mutant is killed and both controls pass; 1 otherwise.
Scratch: honours TMPDIR (tempfile.mkdtemp), removed on exit.
"""
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INSTR = os.path.join(HERE, "figure-audit.py")

MUTANTS = [
    ("m4-drop-stale-literal-case",
     '    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)\n', ""),
    ("m6-readonly-gate-off",
     "return head.startswith(READ_ONLY_HEADS)", "return True"),
]
CONTROLS = [
    ("c-equivalent-trailing-space",
     "return head.startswith(READ_ONLY_HEADS)", "return head.startswith(READ_ONLY_HEADS)  "),
]


def selftest_exit(path, tmp):
    p = subprocess.run([sys.executable, path, "--selftest"], cwd=tmp,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
    tail = (p.stdout or "").strip().splitlines()
    return p.returncode, (tail[-1] if tail else "")


def main():
    with open(INSTR, "r", encoding="utf-8") as fh:
        pristine = fh.read()
    tmp = tempfile.mkdtemp(prefix="figure-audit-mutbat-")
    ok = True
    try:
        rc, last = selftest_exit(INSTR, tmp)
        print("PRISTINE selftest_exit=%d last=%r" % (rc, last))
        if rc != 0:
            ok = False
        for mid, old, new in CONTROLS:
            text = pristine.replace(old, new, 1) if pristine.count(old) == 1 else None
            if text is None:
                print("CONTROL %s sites=%d unusable" % (mid, pristine.count(old)))
                ok = False
                continue
            path = os.path.join(tmp, mid + ".py")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            rc, last = selftest_exit(path, tmp)
            held = rc == 0
            print("CONTROL %s selftest_exit=%d must_not_be_killed=%s last=%r" % (mid, rc, "held" if held else "KILLED", last))
            if not held:
                ok = False
        killed = survivors = 0
        for mid, old, new in MUTANTS:
            n = pristine.count(old)
            if n != 1:
                print("MUT %s sites=%d exact-once=fail" % (mid, n))
                ok = False
                continue
            text = pristine.replace(old, new, 1)
            path = os.path.join(tmp, mid + ".py")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            try:
                py_compile.compile(path, doraise=True)
                compiled = 0
            except py_compile.PyCompileError:
                compiled = 1
            if compiled:
                print("MUT %s sites=%d py_compile=fail killed=0 (not a valid mutant)" % (mid, n))
                ok = False
                continue
            rc, last = selftest_exit(path, tmp)
            k = 1 if rc != 0 else 0
            killed += k
            survivors += 1 - k
            print("MUT %s sites=%d py_compile=0 selftest_exit=%d killed=%d last=%r" % (mid, n, rc, k, last))
        print("mutbat killed=%d/%d survivors=%d controls=%s" % (
            killed, len(MUTANTS), survivors, "pass" if ok else "fail"))
        if survivors:
            ok = False
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
'''


def build_fa(text):
    text = once(text, "def eprint(*a):",
                "EXPECTED_CASES = 6  # R17 pin: a dropped selftest case turns the selftest red\n\n\ndef eprint(*a):",
                "EXPECTED_CASES")
    text = once(text, "\n\ndef selftest():", "\n\n" + FA_NEW_ROFIXTURE + "\ndef selftest():", "NOT_RO fixture")
    text = once(text, '    run_case("unreadable-ledger-exit-2", 2, None, broken=True)\n',
                '    run_case("unreadable-ledger-exit-2", 2, None, broken=True)\n'
                '    run_case("derive-not-read-only-refused", 2, SELFTEST_LEDGER_NOT_RO)\n', "new case")
    text = once(text, '    print("selftest cases=%d failures=%d" % (len(cases), failures))\n',
                '    if len(cases) != EXPECTED_CASES:\n'
                '        print("selftest pin cases=%d expected=%d verdict=fail" % (len(cases), EXPECTED_CASES))\n'
                '        failures += 1\n'
                '    print("selftest cases=%d failures=%d" % (len(cases), failures))\n', "pin")
    return text


def main():
    os.makedirs(S, exist_ok=True)
    os.makedirs(os.path.dirname(ENV["TMPDIR"]), exist_ok=True)
    os.makedirs(ENV["TMPDIR"], exist_ok=True)
    if os.path.exists(os.path.join(S, ".git")) or os.path.isdir(S):
        shutil.rmtree(S)
    out, rc = sh("git clone -q --shared %s %s" % (L, S), "/")
    if rc != 0:
        raise SystemExit("clone failed: " + out)
    # carry the round-58 untracked capture + manifest into the stand-in (declared after-adds)
    for rel in ["corpus/source-snapshots/round-58/S091.txt", "corpus/source-snapshots/round-58/manifest.json"]:
        os.makedirs(os.path.dirname(os.path.join(S, rel)), exist_ok=True)
        shutil.copyfile(os.path.join(L, rel), os.path.join(S, rel))
    # C1: figure-audit instrument + mutant battery + red fixture repoint
    fa = os.path.join(S, "corpus/instruments/figure-audit.py")
    with open(fa, encoding="utf-8") as fh:
        t = fh.read()
    with open(fa, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build_fa(t))
    with open(os.path.join(S, "corpus/instruments/figure-audit-mutbat.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(MUTBAT)
    red = os.path.join(S, ".ufo/waves/round-54/controls/red-d53-ledger.json")
    with open(red, encoding="utf-8") as fh:
        t = fh.read()
    old = "python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'"
    new = "grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2"
    with open(red, "w", encoding="utf-8", newline="") as fh:
        fh.write(once(t, old, new, "red fixture derive"))
    # C2: entry, registry row, README block, PROVINCE line, expected list, registry-change bullet
    ent_dst = os.path.join(S, "corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md")
    shutil.copyfile(K, ent_dst)
    sp = os.path.join(S, "corpus/SOURCES.md")
    with open(sp, encoding="utf-8") as fh:
        st = fh.read()
    s090 = [ln for ln in st.split("\n") if ln.startswith("| S090 |")]
    assert len(s090) == 1
    row = ("| S091 | UK AI Security Institute, How fast is autonomous AI cyber capability advancing? "
           "(blog, dated May 13, 2026) — https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing "
           "| docs | A | AISI's own measurement statements on the rate of autonomous AI cyber-task progress, scoped to its "
           "narrow cyber suite and its two cyber ranges, as the blog states them "
           "| capture corpus/source-snapshots/round-58/S091.txt: title L1, date L13, estimate and acceleration L14, "
           "method and threshold L19-L21, doubling L25, uncertainty L28-L30, cyber ranges L33-L35, publisher L45; "
           "dated May 13, 2026 "
           "| Read a dated, suite-bound doubling estimate with its stated method caps and uncertainty, not a universal "
           "rate of AI progress or a forecast | mined | 2026-11-03 | 90d "
           "| corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md |")
    assert row.count("|") == 12, row.count("|")
    st = st.replace(s090[0] + "\n", s090[0] + "\n" + row + "\n", 1)
    bullet = ("- S091 row added (round 58): new row (id `S091`, kind `docs`, tier A scoped to AISI's own statements on "
              "its narrow cyber suite and cyber ranges, status mined, opened 2026-11-03, recheck `90d`, used-by "
              "`corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md`), anchored to the round-58 capture "
              "`corpus/source-snapshots/round-58/S091.txt` (sha256 `d2ba7199…820618`, 67 lines). The lead line "
              "`UK AI Security Institute's report …` at `corpus/SOURCES.md:141` is byte-unchanged (exact-line sha256 "
              "`631364e0…627547` at base and tip) and is admitted as S091 by this bullet, not edited. Registry 90 rows "
              "pre-append → 91 post-append (R8); no pre-existing status, recheck or used-by cell changed.\n")
    st = st.rstrip("\n") + "\n\n" + bullet
    with open(sp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(st)
    rp = os.path.join(S, "corpus/README.md")
    with open(rp, encoding="utf-8") as fh:
        rt = fh.read()
    block = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "readme-block.md"), encoding="utf-8").read()
    with open(rp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(rt + block)
    pp = os.path.join(S, "PROVINCE.md")
    with open(pp, encoding="utf-8") as fh:
        pt = fh.read()
    pline = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "province-line.md"), encoding="utf-8").read()
    with open(pp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(pt + pline)
    ep = os.path.join(S, "corpus/instruments/knowledge-expected.txt")
    lines = open(ep, encoding="utf-8").read().split("\n")
    new_entry = "corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md"
    idx = [i for i, ln in enumerate(lines) if ln.startswith("corpus/knowledge/")]
    pos = next(i for i in idx if lines[i] > new_entry)
    lines.insert(pos, new_entry)
    with open(ep, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print("stand-in built at", S)


if __name__ == "__main__":
    main()
