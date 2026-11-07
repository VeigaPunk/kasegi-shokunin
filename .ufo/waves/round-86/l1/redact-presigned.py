#!/usr/bin/env python3
"""Round-86: strip presigned-URL query strings (AWS STS credential material) from
a one-line HackerOne JSON capture, in place.

Every JSON string value containing `X-Amz-` keeps its scheme/host/path and
loses its query string, replaced by `?[presigned-query-redacted-r86]`. Output is
compact JSON (separators ',' ':'), ASCII-escaped like the served body, one line
plus a trailing newline, so the manifest's quote strings (`"handle":"ibb"`,
`"has_bounty?":true`, ...) still occur once. Prints old/new sha256 and the
number of redacted strings.

Usage: redact-presigned.py FILE
"""
import hashlib
import json
import sys

MARK = "?[presigned-query-redacted-r86]"


def walk(v, n):
    if isinstance(v, dict):
        return {k: walk(x, n) for k, x in v.items()}
    if isinstance(v, list):
        return [walk(x, n) for x in v]
    if isinstance(v, str) and "X-Amz-" in v and "?" in v:
        n[0] += 1
        return v.split("?", 1)[0] + MARK
    return v


def main(argv):
    p = argv[1]
    raw = open(p, "rb").read()
    n = [0]
    out = json.dumps(walk(json.loads(raw), n), separators=(",", ":"), ensure_ascii=True) + "\n"
    out_b = out.encode()
    assert b"X-Amz-" not in out_b
    open(p, "wb").write(out_b)
    print("REDACT file=%s strings=%d old_sha256=%s new_sha256=%s bytes=%d" % (
        p, n[0], hashlib.sha256(raw).hexdigest(), hashlib.sha256(out_b).hexdigest(), len(out_b)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
