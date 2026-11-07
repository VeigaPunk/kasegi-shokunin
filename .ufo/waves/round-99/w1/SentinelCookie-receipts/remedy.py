#!/usr/bin/env python3
"""SentinelCookie round-99: price the smallest remediation, and the rune case.

Candidate A = round-98 SentinelShapes option 1 (the union, unbounded).
Candidate B = the union with the whitespace run bounded to 8 and newline
excluded, which is the smallest change that recovers the cookie-jar form
without re-admitting either frozen negative.
"""
import importlib.util
import os
import re
import shutil
import sys

H = b"0123456789abcdef" * 4
LB = (rb"(?:(?<![A-Za-z0-9_])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})"
      rb"|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))")
TAIL = rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])"
A = re.compile(LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
               rb"(?:[\s\"'=:;]+|.{0,8}[:=].{0,8})" + TAIL)
B = re.compile(LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
               rb"(?:[^\S\n\"'=:;]{1,8}|[^\n]{0,8}[:=][^\n]{0,8})" + TAIL)
S140 = re.compile(rb"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
                  rb"(?:cell-[0-9]+-)?[0-9a-f]{64}")
S140_R = re.compile(r"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
                    r"(?:cell-[0-9]+-)?[0-9a-f]{64}")

MUSTFIX = [
    b"_gitlab_session=cell--" + H + b"\n",
    b"_gitlab_session => " + H + b"\n",
    b"_gitlab_session%20=%20" + H + b"\n",
    b"_gitlab_session%20:%20" + H + b"\n",
    b"_gitlab_session=%20" + H + b"\n",
    b"_gitlab_session(=(" + H + b")\n",
    b"_gitlab_session ( = ) " + H + b"\n",
    b"_gitlab_session,=" + H + b"\n",
    b"_gitlab_session|=" + H + b"\n",
    b"_gitlab_session+=" + H + b"\n",
    b"_gitlab_session=> " + H + b"\n",
    b"_gitlab_session_geo_" + H + b"%20=%20" + H + b"\n",
]
NEGATIVES = [
    b"_gitlab_session=" + H[:63] + b"\n",
    b"_gitlab_session_geo_" + H[:63] + b"=" + H + b"\n",
    b"_gitlab_session=" + H.upper() + b"\n",
    b"session=" + H + b"\n",
    b"_other_session=" + H + b"\n",
    b"_gitlab_session=cell-abc-" + H + b"\n",
    b"_gitlab_session" + b" " * 9 + b"=" + H + b"\n",
    b"_gitlab_session=\n" + H + b"\n",
    b"_gitlab_session=" + H[:32] + b"-" + H[33:] + b"\n",
    b"x_gitlab_session=" + H + b"\n",
]
JAR = [
    ("jar-tab", b".gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t" + H + b"\n"),
    ("jar-space", b".gitlab.com TRUE / TRUE 0 _gitlab_session " + H + b"\n"),
    ("geo-space", b"_gitlab_session_geo_" + H + b" " + H + b"\n"),
    ("nl-before-eq", b"_gitlab_session\n=" + H + b"\n"),
    ("gap9", b"_gitlab_session" + b" " * 9 + b"=" + H + b"\n"),
]
CJK = [
    ("cjk-paren", "_gitlab_session（会话）=".encode() + H + b"\n"),
    ("cjk-space", "_gitlab_session　会话　=".encode() + H + b"\n"),
]


def load(path, lane, work, tag):
    stage = os.path.join(work, "inst-" + tag)
    os.makedirs(stage, exist_ok=True)
    dst = os.path.join(stage, "capture-secret-scan.py")
    shutil.copyfile(path, dst)
    shutil.copyfile(os.path.join(lane, "corpus", "instruments", "claim-package-check.py"),
                    os.path.join(stage, "claim-package-check.py"))
    spec = importlib.util.spec_from_file_location("scanner_" + tag, dst)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    lane, work = argv[1], argv[2]
    landed = load(os.path.join(lane, "corpus", "instruments", "capture-secret-scan.py"),
                  lane, work, "landed3")
    pats = landed.patterns()
    hit = lambda d: {s for s, _ in landed.scan_bytes(d, pats)[0]}
    for name, rx in (("A-union", A), ("B-bounded-union", B)):
        m = sum(bool(rx.search(d)) for d in MUSTFIX)
        n = sum(bool(rx.search(d)) for d in NEGATIVES)
        print("CAND %-16s mustfix=%d/12 negatives=%d/10" % (name, m, n))
        for pid, d in JAR:
            print("CAND %-16s %-14s hit=%s" % (name, pid, bool(rx.search(d))))
    for pid, d in CJK:
        print("RUNE %-12s landed=%s s140_bytes=%s s140_runes=%s"
              % (pid, ",".join(sorted(hit(d))) or "none",
                 bool(S140.search(d)), bool(S140_R.search(d.decode("utf-8")))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
