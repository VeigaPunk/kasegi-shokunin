#!/usr/bin/env python3
"""SentinelCookie round-99: ASCII sweeps around the landed session-cookie shape.

Four 128-cell sweeps (the byte before the keyword, the byte after the value,
the byte before the operator, the byte after the operator), plus a replay of
the twelve round-98 MUST-FIX payloads and the ten boundary negatives, plus a
candidate union separator to price the smallest remediation.
"""
import importlib.util
import os
import re
import shutil
import sys

H = b"0123456789abcdef" * 4
S140_BYTES = re.compile(
    rb"_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}"
    rb"(?:cell-[0-9]+-)?[0-9a-f]{64}")
# round-98 SentinelShapes remediation option 1: the union, keeps every
# round-98 detection and adds S140's assignment gap.
UNION = re.compile(
    rb"(?:(?<![A-Za-z0-9_])|(?<=\\[ntr])|(?<=\\u[0-9A-Fa-f]{4})|(?<=%[0-9A-Fa-f]{2})"
    rb"|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"
    rb"_gitlab_session(?:_geo_[0-9a-f]{64})?"
    rb"(?:[\s\"'=:;]+|.{0,8}[:=].{0,8})(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")


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


def classify(got, sb):
    if not got and sb:
        return "S140-ONLY"
    if got and not sb:
        return "SCANNER-ONLY"
    return "AGREE-HIT" if got else "AGREE-MISS"


def main(argv):
    lane, work = argv[1], argv[2]
    landed = load(os.path.join(lane, "corpus", "instruments", "capture-secret-scan.py"),
                  lane, work, "landed2")
    pats = landed.patterns()

    def hit(data):
        return {s for s, _ in landed.scan_bytes(data, pats)[0]}

    sweeps = {
        "pre-keyword": lambda c: bytes([c]) + b"_gitlab_session=" + H + b"\n",
        "post-value": lambda c: b"_gitlab_session=" + H + bytes([c]),
        "window-before-op": lambda c: b"_gitlab_session" + bytes([c]) + b"=" + H + b"\n",
        "window-after-op": lambda c: b"_gitlab_session=" + bytes([c]) + H + b"\n",
    }
    for name, fn in sweeps.items():
        counts = {}
        s140_only = []
        for c in range(128):
            data = fn(c)
            got = hit(data)
            sb = bool(S140_BYTES.search(data))
            v = classify(got, sb)
            counts[v] = counts.get(v, 0) + 1
            if v == "S140-ONLY":
                s140_only.append(c)
        print("SWEEP %-18s %s" % (name, " ".join("%s=%d" % (k, counts[k]) for k in sorted(counts))))
        if s140_only:
            print("SWEEP %-18s s140_only_bytes=%s" % (name, s140_only))

    # --- replay the twelve round-98 MUST-FIX payloads and the ten negatives
    mustfix = [
        ("M1", b"_gitlab_session=cell--" + H + b"\n"),
        ("M2", b"_gitlab_session => " + H + b"\n"),
        ("M3", b"_gitlab_session%20=%20" + H + b"\n"),
        ("M4", b"_gitlab_session%20:%20" + H + b"\n"),
        ("M5", b"_gitlab_session=%20" + H + b"\n"),
        ("M6", b"_gitlab_session(=(" + H + b")\n"),
        ("M7", b"_gitlab_session ( = ) " + H + b"\n"),
        ("M8", b"_gitlab_session,=" + H + b"\n"),
        ("M9", b"_gitlab_session|=" + H + b"\n"),
        ("M10", b"_gitlab_session+=" + H + b"\n"),
        ("M11", b"_gitlab_session=> " + H + b"\n"),
        ("M12", b"_gitlab_session_geo_" + H + b"%20=%20" + H + b"\n"),
    ]
    negatives = [
        ("N1", b"_gitlab_session=" + H[:63] + b"\n"),
        ("N2", b"_gitlab_session_geo_" + H[:63] + b"=" + H + b"\n"),
        ("N3", b"_gitlab_session=" + H.upper() + b"\n"),
        ("N4", b"session=" + H + b"\n"),
        ("N5", b"_other_session=" + H + b"\n"),
        ("N6", b"_gitlab_session=cell-abc-" + H + b"\n"),
        ("N7", b"_gitlab_session" + b" " * 9 + b"=" + H + b"\n"),
        ("N8", b"_gitlab_session=\n" + H + b"\n"),
        ("N9", b"_gitlab_session=" + H[:32] + b"-" + H[33:] + b"\n"),
        ("N10", b"x_gitlab_session=" + H + b"\n"),
    ]
    ok = 0
    for pid, data in mustfix:
        got = hit(data)
        ok += "gitlab-session-cookie" in got
        print("REPLAY %-4s mustfix hit=%s" % (pid, "gitlab-session-cookie" in got))
    print("REPLAY mustfix_hit=%d/12" % ok)
    bad = 0
    for pid, data in negatives:
        got = hit(data)
        bad += bool(got)
        print("REPLAY %-4s negative hit=%s" % (pid, ",".join(sorted(got)) or "none"))
    print("REPLAY negatives_hit=%d/10" % bad)

    # --- the regression payloads and the union candidate -------------------
    regress = [
        ("jar-tab", b".gitlab.com\tTRUE\t/\tTRUE\t0\t_gitlab_session\t" + H + b"\n"),
        ("jar-space", b".gitlab.com TRUE / TRUE 0 _gitlab_session " + H + b"\n"),
        ("nl-before-eq", b"_gitlab_session\n=" + H + b"\n"),
        ("nl-after-eq", b"_gitlab_session=\n" + H + b"\n"),
        ("gap9", b"_gitlab_session" + b" " * 9 + b"=" + H + b"\n"),
        ("geo-space", b"_gitlab_session_geo_" + H + b" " + H + b"\n"),
    ]
    for pid, data in regress:
        got = hit(data)
        print("REGRESS %-14s landed=%s union=%s s140=%s"
              % (pid, ",".join(sorted(got)) or "none",
                 bool(UNION.search(data)), bool(S140_BYTES.search(data))))
    # the union must not lose any of the twelve or gain any of the ten
    u_must = sum(bool(UNION.search(d)) for _, d in mustfix)
    u_neg = sum(bool(UNION.search(d)) for _, d in negatives)
    print("UNION mustfix=%d/12 negatives=%d/10" % (u_must, u_neg))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
