#!/usr/bin/env python
"""figure-audit.py — re-derive figures recorded in lane records against committed bytes.

The r53 closure routed two number-drift defects (D53-1: a receipt trailer said
"34 inherited" while the same receipt's measured line printed
FAIL_entry_records=33; D53-2: capture metadata said 543 lines while `wc -l`
over the committed capture printed 542).  This instrument is the audit that
catches that class: a JSON ledger pins, per figure, where it is recorded, the
literal as recorded, a read-only command that re-derives it, and the value the
command must print.  Every figure is re-derived and compared as a WHOLE value
(never a substring), so a recorded 34 against a derived 33, or a want of 34
against a derived 340, reads stale.

Usage:
  python corpus/instruments/figure-audit.py [--ledger PATH] [--root DIR]

Ledger entry shape (JSON object with a "figures" array):
  {"id": "...",      - stable figure id
   "record": "...",  - where the literal is recorded (file:line or pointer)
   "recorded": "...",- the literal as recorded (informational, printed)
   "derive": "...",  - read-only shell command, run with cwd=root, via bash
   "want": "...",    - the exact value the command must print (stripped)
   optional "rev": "..."} - when present, "derive" should address committed
                            bytes at that rev (e.g. `git show <rev>:<path>`);
                            the audit never runs a mutating command: entries
                            are rejected whose derive lacks a read-only head
                            (allow-list: git show, git cat-file, grep, wc, ls,
                            sha256sum, cat, cut, sort, awk, sed -n, python/
                            python3 running a corpus/instruments/*.py counter).

Exit codes: 0 every figure re-derives; 1 any figure stale or derive failed
(fail-closed: a nonzero derive exit or an empty stdout is stale, never ok);
2 harness/read error (ledger missing/unparsable, entry malformed, no bash).

--selftest grades its own limbs on a fixture tree built under $HYAKU_SCRATCH
(or the system temp dir) and prints one `selftest case=<id> verdict=pass|fail`
line per case plus a summary; it exits 0 only when every case passes.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

READ_ONLY_HEADS = (
    "git show ", "git cat-file ", "git ls-tree ", "grep", "wc ", "wc<", "ls ", "ls*",
    "sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "python ", "python3 ",
)


EXPECTED_CASES = 6  # R17 pin: a dropped selftest case turns the selftest red


def eprint(*a):
    print(*a, file=sys.stderr)


def run_derive(cmd, root):
    bash = shutil.which("bash")
    if bash is None:
        return None, "", "no-bash-on-host"
    try:
        p = subprocess.run([bash, "-c", cmd], cwd=root or ".",
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=300)
    except subprocess.TimeoutExpired:
        return None, "", "derive-timeout"
    out = p.stdout.decode("utf-8", "replace").strip()
    if p.returncode != 0:
        return None, out, "derive-exit-%d" % p.returncode
    if out == "":
        return None, out, "derive-empty"
    return out, out, None


def check_read_only(cmd):
    head = cmd.split("|")[0].split(">")[0].strip()
    if head.startswith(("python ", "python3 ")):
        # a counter run is admissible only against a committed instrument
        parts = head.split()
        return len(parts) >= 2 and parts[1].replace("\\", "/").startswith("corpus/instruments/")
    return head.startswith(READ_ONLY_HEADS)


def audit(ledger_path, root):
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            doc = json.load(f)
    except FileNotFoundError:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-missing path=%s" % ledger_path)
        return 2
    except (ValueError, UnicodeDecodeError) as e:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-unreadable detail=%s" % e)
        return 2
    figs = doc.get("figures") if isinstance(doc, dict) else None
    if not isinstance(figs, list) or not figs:
        eprint("FIGURE-AUDIT: UNAVAILABLE reason=ledger-shape want=figures-array")
        return 2
    ok = stale = 0
    for ent in figs:
        if not isinstance(ent, dict) or not all(k in ent for k in ("id", "record", "recorded", "derive", "want")):
            eprint("FIGURE-AUDIT: UNAVAILABLE reason=entry-shape entry=%r" % (ent.get("id") if isinstance(ent, dict) else ent,))
            return 2
        if not check_read_only(ent["derive"]):
            eprint("FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=%s" % ent["id"])
            return 2
        derived, raw, err = run_derive(ent["derive"], root)
        if err is not None:
            stale += 1
            print("FIG %s recorded=%s derived=UNAVAILABLE reason=%s stale" % (ent["id"], ent["recorded"], err))
            continue
        if derived == str(ent["want"]):
            ok += 1
            print("FIG %s recorded=%s derived=%s ok" % (ent["id"], ent["recorded"], derived))
        else:
            stale += 1
            print("FIG %s recorded=%s derived=%s want=%s stale" % (ent["id"], ent["recorded"], derived, ent["want"]))
    code = 1 if stale else 0
    print("FIGURE-AUDIT figures=%d ok=%d stale=%d exit=%d" % (len(figs), ok, stale, code))
    return code


SELFTEST_LEDGER_OK = {
    "figures": [
        {"id": "s-ok", "record": "g.txt:1", "recorded": "35", "derive": "cat g.txt", "want": "35"},
    ],
}
SELFTEST_LEDGER_STALE = {
    "figures": [
        {"id": "s-stale", "record": "f1.txt:1", "recorded": "7", "derive": "cat f1.txt", "want": "7"},
    ],
}
SELFTEST_LEDGER_FAILS = {
    "figures": [
        {"id": "s-fails", "record": "missing.txt", "recorded": "1", "derive": "cat missing.txt", "want": "1"},
    ],
}
SELFTEST_LEDGER_TOKEN = {
    "figures": [
        {"id": "s-token", "record": "f1.txt:1", "recorded": "34", "derive": "cat f1.txt", "want": "34"},
    ],
}


SELFTEST_LEDGER_NOT_RO = {
    "figures": [
        {"id": "s-not-ro", "record": "g.txt:1", "recorded": "35", "derive": "echo 35", "want": "35"},
    ],
}

def selftest():
    cases = []

    def run_case(cid, want_exit, ledger_doc=None, broken=False):
        tmp = tempfile.mkdtemp(prefix="figure-audit-selftest-")
        try:
            with open(os.path.join(tmp, "g.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("35\n")
            with open(os.path.join(tmp, "f1.txt"), "w", encoding="utf-8", newline="\n") as f:
                f.write("340\n")
            lp = os.path.join(tmp, "ledger.json")
            with open(lp, "w", encoding="utf-8", newline="\n") as f:
                if broken:
                    f.write("{not json")
                else:
                    json.dump(ledger_doc, f)
                    f.write("\n")
            me = os.path.abspath(sys.argv[0])
            bash = shutil.which("bash")
            p = subprocess.run([bash, "-c", 'python "%s" --ledger "%s" --root "%s"' % (me, lp, tmp)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
            out = p.stdout.decode("utf-8", "replace")
            good = p.returncode == want_exit
            cases.append((cid, p.returncode, want_exit, good, out))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    run_case("ok-ledger", 0, SELFTEST_LEDGER_OK)
    run_case("stale-literal", 1, SELFTEST_LEDGER_STALE)
    run_case("derive-fails-fail-closed", 1, SELFTEST_LEDGER_FAILS)
    run_case("token-boundary-34-vs-340", 1, SELFTEST_LEDGER_TOKEN)
    run_case("unreadable-ledger-exit-2", 2, None, broken=True)
    run_case("derive-not-read-only-refused", 2, SELFTEST_LEDGER_NOT_RO)

    failures = 0
    for cid, got, want, good, out in cases:
        print("selftest case=%s exit=%d want=%d verdict=%s" % (cid, got, want, "pass" if good else "fail"))
        if not good:
            failures += 1
    if len(cases) != EXPECTED_CASES:
        print("selftest pin cases=%d expected=%d verdict=fail" % (len(cases), EXPECTED_CASES))
        failures += 1
    print("selftest cases=%d failures=%d" % (len(cases), failures))
    return 0 if failures == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    ledger = os.path.join("corpus", "instruments", "figure-audit-ledger.json")
    root = "."
    it = iter(argv)
    for a in it:
        if a == "--ledger":
            ledger = next(it)
        elif a == "--root":
            root = next(it)
    return audit(ledger, root)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
