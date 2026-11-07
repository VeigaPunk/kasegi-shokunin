#!/usr/bin/env python3
"""kasegi round-100 C2 frozen counter — the session-cookie separator, measured.

Stages the instrument at a named revision, then prints ONE summary line:

  C2-CHECK rev=<rev> regression_r98=<n> scanner_only=<n> mustfix=<n> rune=<n>
           agree_hit=<n> probe_mustfix=<n>/12 probe_negatives_extra=<n>
           selftest_cases=<n> instrument_sha256=<sha>

`regression_r98` counts matrix cells the round-98 instrument (pinned rev)
detected and this revision's instrument does not; `scanner_only` counts cells
this revision detects beyond S140's own regex; `mustfix`/`rune` count cells
S140 detects and this revision misses. The matrix is the round-99
SentinelCookie 192-cell matrix, unchanged, so the two rounds are comparable.

Usage:
  python3 -B .ufo/waves/round-100/c2/c2-check.py --lane . --rev <40-hex> \
      --r98-rev e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 --work <scratch>
"""
import argparse
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R98 = "e2caf4a1561b544a6ea684b0bcfa975f7e7f6061"
INSTR = "corpus/instruments/capture-secret-scan.py"
CLAIM = "corpus/instruments/claim-package-check.py"


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def stage(lane, rev, work, tag):
    d = os.path.join(work, "inst-" + tag)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, "capture-secret-scan.py")
    p = sh(["git", "-C", lane, "show", "%s:%s" % (rev, INSTR)])
    if p.returncode != 0:
        raise SystemExit("C2-CHECK error reason=bad-rev rc=2")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(p.stdout)
    src = os.path.join(lane, CLAIM)
    if os.path.isfile(src):
        shutil.copyfile(src, os.path.join(d, "claim-package-check.py"))
    return dst


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def matrix_module():
    spec = importlib.util.spec_from_file_location("r100_matrix", os.path.join(HERE, "matrix.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--file")
    ap.add_argument("--r98-rev", default=R98)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    if a.file:
        cand_path = os.path.abspath(a.file)
        tag = "file"
    else:
        if not a.rev:
            raise SystemExit("C2-CHECK error reason=usage rc=2")
        cand_path = stage(lane, a.rev, work, a.rev[:12])
        tag = a.rev
    r98_path = stage(lane, a.r98_rev, work, "r98")
    cand = load(cand_path, "cand")
    r98 = load(r98_path, "r98")
    mx = matrix_module()
    pats_c = cand.patterns()
    pats_9 = r98.patterns()
    counts = {"AGREE-HIT": 0, "AGREE-MISS": 0, "MUST-FIX": 0, "MUST-FIX-RUNE": 0,
              "REGRESSION-R98": 0, "SCANNER-ONLY": 0}
    for fam, pid, data in mx.build():
        got_c = {s for s, _ in cand.scan_bytes(data, pats_c)[0]}
        got_9 = {s for s, _ in r98.scan_bytes(data, pats_9)[0]}
        sb = bool(mx.S140_BYTES.search(data))
        try:
            sr = bool(mx.S140_RUNES.search(data.decode("utf-8")))
        except UnicodeDecodeError:
            sr = None
        if not got_c and sb:
            v = "MUST-FIX"
        elif not got_c and not sb and sr:
            v = "MUST-FIX-RUNE"
        elif not got_c and got_9:
            v = "REGRESSION-R98"
        elif got_c and not sb:
            v = "SCANNER-ONLY"
        elif got_c and sb:
            v = "AGREE-HIT"
        else:
            v = "AGREE-MISS"
        counts[v] += 1
    # probe: the twelve round-98 MUST-FIX payloads and the ten frozen negatives
    probe = sh([sys.executable, "-B", os.path.join(HERE, "session-cookie-probe.py"),
                "--lane", lane, "--instrument", cand_path, "--work", work])
    pm = pe = "?"
    for ln in probe.stdout.split("\n"):
        if ln.startswith("PROBE-RESULT"):
            for tok in ln.split():
                if tok.startswith("mustfix_hit="):
                    pm = tok.split("=", 1)[1]
                if tok.startswith("negatives_extra="):
                    pe = tok.split("=", 1)[1]
    st = sh([sys.executable, "-B", cand_path, "--selftest"])
    cases = "?"
    for ln in st.stdout.split("\n"):
        if ln.startswith("SELFTEST-RESULT"):
            for tok in ln.split():
                if tok.startswith("cases="):
                    cases = tok.split("=", 1)[1]
    with open(cand_path, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    print("C2-CHECK rev=%s regression_r98=%d scanner_only=%d mustfix=%d rune=%d "
          "agree_hit=%d probe_mustfix=%s probe_negatives_extra=%s selftest_cases=%s "
          "instrument_sha256=%s" % (
              tag, counts["REGRESSION-R98"], counts["SCANNER-ONLY"], counts["MUST-FIX"],
              counts["MUST-FIX-RUNE"], counts["AGREE-HIT"], pm, pe, cases, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
