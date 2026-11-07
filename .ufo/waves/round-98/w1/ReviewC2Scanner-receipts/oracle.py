#!/usr/bin/env python3
"""Compare the landing instrument's nine round-98 GitLab shapes against
reference regexes transcribed literally from S140.txt."""
import importlib.util
import re
import sys

LAND = "/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner/landing/corpus/instruments/capture-secret-scan.py"
spec = importlib.util.spec_from_file_location("scan", LAND)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)
PATS = dict(scan.GITLAB_PATTERNS)

# POSIX classes translated from S140's own text.
PUNCT = rb"[!-/:-@\[-`{-~]"          # [[:punct:]]
SPACE = rb"[ \t\n\r\f\v]"            # [[:space:]] (blank is a subset)
B = rb"(?:" + PUNCT + rb"|" + SPACE + rb"|$)"

REF = {
    "gitlab-ci-build-token":
        rb"(?<![A-Za-z0-9_])(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20})" + B,
    "gitlab-runner-registration-token":
        rb"(?<![A-Za-z0-9_])(GR1348941[0-9a-zA-Z_\-]{20})" + B,
    "gitlab-feed-token":
        rb"(?<![A-Za-z0-9_])(feed_token=[0-9a-zA-Z_\-]{20})" + B,
    "gitlab-oauth-app-secret":
        rb"(?<![A-Za-z0-9_])(gloas-[0-9a-zA-Z_\-]{64})" + B,
    "gitlab-feed-token-v2":
        rb"(?<![A-Za-z0-9_])(glft-[0-9a-zA-Z_\-]{20})" + B,
    "gitlab-scim-oauth-token":
        rb"(?<![A-Za-z0-9_])(glsoat-[0-9a-zA-Z_\-]{20})" + B,
    "gitlab-iam-refresh-token":
        rb"(?<![A-Za-z0-9_])(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)",
    "gitlab-iam-authorization-code":
        rb"(?<![A-Za-z0-9_])(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:[^0-9a-zA-Z_\-]|$)",
}
REF = {k: re.compile(v, re.S) for k, v in REF.items()}

VALUE = {
    "gitlab-ci-build-token": b"glcbt-Ab3_" + b"k" * 20,
    "gitlab-runner-registration-token": b"GR1348941" + b"A" * 20,
    "gitlab-feed-token": b"feed_token=" + b"B" * 20,
    "gitlab-oauth-app-secret": b"gloas-" + b"C" * 64,
    "gitlab-feed-token-v2": b"glft-" + b"D" * 20,
    "gitlab-scim-oauth-token": b"glsoat-" + b"F" * 20,
    "gitlab-iam-refresh-token": b"gliamrt-" + b"A" * 43 + b"." + b"B" * 43,
    "gitlab-iam-authorization-code": b"gliamac-" + b"C" * 43 + b"." + b"D" * 43,
}

ours = lambda shape, data: bool(PATS[shape].search(data))


def main():
    print("== right-boundary sweep: every byte 0x00..0xff, plus EOL ==")
    diffs = {}
    for shape, val in VALUE.items():
        ref = REF[shape]
        d = []
        for b in range(256):
            data = val + bytes([b]) + b" end"
            o, r = ours(shape, data), bool(ref.search(data))
            if o != r:
                d.append((b, o, r))
        data = val
        if ours(shape, data) != bool(ref.search(data)):
            d.append(("EOL", ours(shape, data), bool(ref.search(data))))
        diffs[shape] = d
        kinds = {}
        for b, o, r in d:
            key = "ours-only" if (o and not r) else "ref-only"
            kinds.setdefault(key, []).append(b if isinstance(b, str) else "0x%02x" % b)
        print("%-40s diffs=%d %s" % (shape, len(d), {k: (len(v), v[:8]) for k, v in kinds.items()}))

    print()
    print("== left-boundary sweep (prefix byte) ==")
    for shape, val in VALUE.items():
        ref = REF[shape]
        d = []
        for b in range(256):
            data = bytes([b]) + val + b" end"
            o, r = ours(shape, data), bool(ref.search(data))
            if o != r:
                d.append((b, o, r))
        print("%-40s diffs=%d %s" % (shape, len(d),
              ["0x%02x:ours=%d ref=%d" % t for t in d[:6]]))

    print()
    print("== S140 grammar lengths, exact ==")
    for n in range(0, 8):
        data = b"glcbt-" + b"A" * n + b"_" + b"k" * 20 + b" "
        print("  ci-build prefix=%d ours=%-5s ref=%-5s" % (n, ours("gitlab-ci-build-token", data),
                                                           bool(REF["gitlab-ci-build-token"].search(data))))
    for n in (19, 20, 21):
        data = b"glcbt-Ab3_" + b"k" * n + b" "
        print("  ci-build tail=%d ours=%-5s ref=%-5s" % (n, ours("gitlab-ci-build-token", data),
                                                         bool(REF["gitlab-ci-build-token"].search(data))))
    for n in (42, 43, 44):
        data = b"gliamrt-" + b"A" * n + b"." + b"B" * 43 + b" "
        print("  iam-refresh a=%d ours=%-5s ref=%-5s" % (n, ours("gitlab-iam-refresh-token", data),
                                                         bool(REF["gitlab-iam-refresh-token"].search(data))))
    data = b"gliamrt-" + b"A" * 43 + b"B" * 43 + b" "
    print("  iam-refresh no-dot ours=%-5s ref=%-5s" % (ours("gitlab-iam-refresh-token", data),
                                                       bool(REF["gitlab-iam-refresh-token"].search(data))))

    print()
    print("== widening direction: token + `_` / `-` / alnum ==")
    for shape, val in VALUE.items():
        row = []
        for ch in (b"_", b"-", b"x", b"9", b" ", b"\n"):
            data = val + ch + b"x"
            row.append("%s:ours=%d ref=%d" % (ch.decode(), ours(shape, data),
                                              bool(REF[shape].search(data))))
        print("  %-40s %s" % (shape, " ".join(row)))


if __name__ == "__main__":
    main()
