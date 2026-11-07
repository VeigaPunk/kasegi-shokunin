#!/usr/bin/env python3
"""kasegi round-99 C2 counter — the session-cookie separator probe.

The round-98 wave's sentinel (`.ufo/waves/round-98/w1/SentinelShapes.md`,
`-receipts/final-checks.txt`) measured twelve real 64-hex session values that
S140's `gitlab_session_cookie` rule detects and the round-98 scanner missed:
its separator model `[\\s"'=:;]+` refuses S140's `<keyword>.{0,8}[:=].{0,8}`
assignment-context class. This probe replays those twelve payloads (verbatim
from the receipt) plus ten boundary negatives against an instrument given by
path, and prints the hit count per class.

Usage:
  python3 -B .ufo/waves/round-99/c2/session-cookie-probe.py --instrument <path>
Exit: 0 when every case was evaluated, 2 on setup error.
"""
import argparse
import hashlib
import importlib.util
import os
import shutil
import sys

H = b"0123456789abcdef" * 4  # 64 lower-case hex

# Verbatim from .ufo/waves/round-98/w1/SentinelShapes-receipts/final-checks.txt
# lines 15-26 (the twelve MUST-FIX payloads).
MUSTFIX = [
    ("ck-len-cookie-cell0", b"_gitlab_session=cell--" + H + b"\n"),
    ("ck-ruby-hash-rocket", b"_gitlab_session => " + H + b"\n"),
    ("ck-pct20-eq", b"_gitlab_session%20=%20" + H + b"\n"),
    ("ck-pct20-colon", b"_gitlab_session%20:%20" + H + b"\n"),
    ("ck-pct20-after-eq", b"_gitlab_session=%20" + H + b"\n"),
    ("ck-paren-eq", b"_gitlab_session(=" + H + b")\n"),
    ("ck-paren-gap", b"_gitlab_session ( = ) " + H + b"\n"),
    ("ck-comma-eq", b"_gitlab_session,=" + H + b"\n"),
    ("ck-pipe-eq", b"_gitlab_session|=" + H + b"\n"),
    ("ck-plus-eq", b"_gitlab_session+=" + H + b"\n"),
    ("ck-rocket-nospace", b"_gitlab_session=> " + H + b"\n"),
    ("ck-geo-pct20", b"_gitlab_session_geo_" + H + b"%20=%20" + H + b"\n"),
]

# Boundary negatives: each must NOT produce a gitlab-session-cookie hit.
NEGATIVES = [
    ("n-63-hex", b"_gitlab_session=" + H[:63] + b"\n"),
    ("n-geo-short", b"_gitlab_session_geo_" + H[:63] + b"=" + H + b"\n"),
    ("n-upper-hex", b"_gitlab_session=" + H.upper() + b"\n"),
    ("n-no-keyword", b"session=" + H + b"\n"),
    ("n-other-keyword", b"_other_session=" + H + b"\n"),
    ("n-cell-nondigit", b"_gitlab_session=cell-abc-" + H + b"\n"),
    ("n-gap-9", b"_gitlab_session" + b" " * 9 + b"=" + H + b"\n"),
    ("n-gap-newline", b"_gitlab_session=\n" + H + b"\n"),
    ("n-value-hyphen", b"_gitlab_session=" + H[:32] + b"-" + H[33:] + b"\n"),
    ("n-left-word", b"x_gitlab_session=" + H + b"\n"),
]


def load(path, lane, work):
    # The scanner loads claim-package-check.py from its own directory (the gate
    # patterns are shared), so the instrument is staged beside a copy of it.
    stage = os.path.join(work, "inst")
    os.makedirs(stage, exist_ok=True)
    with open(path, "rb") as fh:
        data = fh.read()
    dst = os.path.join(stage, "capture-secret-scan.py")
    with open(dst, "wb") as fh:
        fh.write(data)
    src = os.path.join(lane, "corpus", "instruments", "claim-package-check.py")
    shutil.copyfile(src, os.path.join(stage, "claim-package-check.py"))
    spec = importlib.util.spec_from_file_location("scanner_under_test", dst)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", required=True)
    ap.add_argument("--lane", default=os.getcwd())
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    path = os.path.abspath(a.instrument)
    if not os.path.isfile(path):
        print("PROBE-RESULT error reason=missing-instrument rc=2")
        return 2
    with open(path, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    work = os.path.abspath(a.work) if a.work else os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "session-cookie-probe")
    mod = load(path, os.path.abspath(a.lane), work)
    pats = mod.patterns()
    hit = 0
    for name, payload in MUSTFIX:
        found = {s for s, _ in mod.scan_bytes(payload, pats)[0]}
        ok = "gitlab-session-cookie" in found
        hit += ok
        print("PROBE %s hit=%s want=True %s got=%s"
              % (name, ok, "PASS" if ok else "FAIL", ",".join(sorted(found)) or "none"))
    extra = 0
    for name, payload in NEGATIVES:
        found = {s for s, _ in mod.scan_bytes(payload, pats)[0]}
        ok = "gitlab-session-cookie" not in found
        extra += not ok
        print("PROBE %s hit=%s want=False %s got=%s"
              % (name, not ok, "PASS" if ok else "FAIL", ",".join(sorted(found)) or "none"))
    print("PROBE-RESULT mustfix_hit=%d/%d negatives_extra=%d negatives=%d instrument_sha256=%s rc=0"
          % (hit, len(MUSTFIX), extra, len(NEGATIVES), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
