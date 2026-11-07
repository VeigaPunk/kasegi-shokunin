#!/usr/bin/env python3
"""Scan captured evidence for credential material before it is committed.

Usage:
  python3 corpus/instruments/capture-secret-scan.py --lane LANE --rev REV [--allow TSV]
  python3 corpus/instruments/capture-secret-scan.py --files PATH... [--allow TSV]
  python3 corpus/instruments/capture-secret-scan.py --selftest

Why: round 86 committed and pushed a HackerOne report JSON whose presigned
profile-picture URLs carried a live AWS STS session token (lesson M86-2). The
claim-package gate's R-NOSECRET rule would have refused those bytes, but it
scans packages, and nothing scanned a capture before its first commit.

Scope. `--rev` reads the git tree at REV (no checkout) and scans only
capture-class paths: anything under corpus/source-snapshots/, any path with a
directory segment ending in `-receipts`, and any file whose name starts with
`live-` (the shapes captures and seat receipts take in this lane). `--files`
scans exactly the named working-tree files, whatever their path: run it on
every capture before the commit that first adds it.

Shapes. The claim-package gate's SECRET_PATTERNS (imported from
claim-package-check.py beside this file, so the two never drift), plus:
  aws-sts-session-token  `X-Amz-Security-Token=<value>` (query string) or
                         `X-Amz-Security-Token: <value>` (header, JSON key): SigV4 says that with
                         temporary credentials you "must add X-Amz-Security-Token
                         ... to hold the session token" (S124 lines 83-85).
  aws-access-key-id      `AKIA`/`ASIA` + 16 upper-case letters or digits: the IAM
                         unique-ID prefixes for an access key and a temporary
                         (AWS STS) access key (S125 lines 318-331).
The documented example key id AKIAIOSFODNN7EXAMPLE (S124 line 409) is allowed.

Allowlist. The gate's generic shapes also match non-secrets in captures (a
file name as a JSON "token" value, a spec's example "secret"). Each such match
is allowed only by a row of the allowlist (default capture-secret-allow.tsv
beside this file): `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason`.
A row binds one exact matched value at one path, so a different value at the
same path and shape is still a hit. Rows for aws-sts-session-token are refused
(a session token is never a false positive); a refused or malformed row is a
read error (exit 2).

Output never prints a matched value: `HIT shape=<s> path=<p> line=<n>` per
file and shape (first non-allowed match), then
`CAPTURE-SECRET-SCAN mode=<m> scanned=<n> hits=<h> files=<f> allowed=<a> unused_allow=<u> rc=<rc>`
(`allowed` counts allowlisted matches; `unused_allow` counts allowlist rows no
scanned match consumed — reported, not an error).
Exit 0 when nothing matched, 1 when anything matched, 2 on usage or read error.
"""
import argparse
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

AWS_PATTERNS = (
    ("aws-sts-session-token", re.compile(
        rb"(?i)X-Amz-Security-Token(?:=|\\?[\"']?\s*:\s*\\?[\"']?)[^&\s\"'<>\\]{20,}")),
    ("aws-access-key-id", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
)
ALLOWED_VALUES = frozenset({b"AKIAIOSFODNN7EXAMPLE"})
NEVER_ALLOWED = frozenset({"aws-sts-session-token"})
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def load_allow(path):
    """Return {(path, shape, sha256hex): reason}; raise OSError on a bad row."""
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            cells = line.split("\t")
            if (len(cells) != 4 or not cells[0] or cells[1] in NEVER_ALLOWED
                    or not HEX64.match(cells[2]) or not cells[3].strip()):
                raise OSError("allowlist row %d" % n)
            rows[(cells[0], cells[1], cells[2])] = cells[3]
    return rows


def gate_patterns():
    path = os.path.join(HERE, "claim-package-check.py")
    spec = importlib.util.spec_from_file_location("claim_package_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.SECRET_PATTERNS)


def patterns():
    return gate_patterns() + AWS_PATTERNS


def is_capture_path(rel):
    parts = rel.split("/")
    return (rel.startswith("corpus/source-snapshots/")
            or any(p.endswith("-receipts") for p in parts[:-1])
            or parts[-1].startswith("live-"))


def scan_bytes(data, pats, path="", allow=None, used=None):
    """Return ([(shape, line)] first non-allowed match per shape, allowed count)."""
    allow = allow or {}
    found, allowed = [], 0
    for name, rx in pats:
        for m in rx.finditer(data):
            if m.group(0) in ALLOWED_VALUES:
                continue
            key = (path, name, hashlib.sha256(m.group(0)).hexdigest())
            if key in allow:
                allowed += 1
                if used is not None:
                    used.add(key)
                continue
            found.append((name, data.count(b"\n", 0, m.start()) + 1))
            break
    return found, allowed


def tree_blobs(lane, rev):
    out = subprocess.run(["git", "-C", lane, "ls-tree", "-r", "-z", rev],
                         capture_output=True, check=True).stdout
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, oid = meta.split(b" ")
        if kind == b"blob" and mode != b"120000":
            yield path.decode("utf-8", "surrogateescape"), oid.decode()


def read_blobs(lane, oids):
    # One request, one response: writing every oid before reading deadlocks once
    # the request bytes exceed the pipe buffer (~1,560 oids; round-87 control).
    proc = subprocess.Popen(["git", "-C", lane, "cat-file", "--batch"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for oid in oids:
        proc.stdin.write(oid.encode() + b"\n")
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        if len(header) != 3:
            raise OSError("cat-file header for %s" % oid)
        data = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        yield data
    proc.stdin.close()
    if proc.wait() != 0:
        raise OSError("cat-file rc %d" % proc.returncode)


def report(mode, results, scanned, allowed=0, unused=0):
    files = 0
    hits = 0
    for path, found in results:
        if found:
            files += 1
        for shape, line in found:
            hits += 1
            print("HIT shape=%s path=%s line=%d" % (shape, path, line))
    rc = 1 if hits else 0
    print("CAPTURE-SECRET-SCAN mode=%s scanned=%d hits=%d files=%d allowed=%d unused_allow=%d rc=%d"
          % (mode, scanned, hits, files, allowed, unused, rc))
    return rc


def scan_rev(lane, rev, pats, allow):
    items = [(p, o) for p, o in tree_blobs(lane, rev) if is_capture_path(p)]
    results, used, allowed = [], set(), 0
    for (path, _), data in zip(items, read_blobs(lane, [o for _, o in items])):
        found, n = scan_bytes(data, pats, path, allow, used)
        allowed += n
        results.append((path, found))
    return report("rev:%s" % rev, results, len(items), allowed, len(set(allow) - used))


def scan_files(paths, pats, allow):
    results, used, allowed = [], set(), 0
    for p in paths:
        with open(p, "rb") as fh:
            found, n = scan_bytes(fh.read(), pats, p, allow, used)
        allowed += n
        results.append((p, found))
    return report("files", results, len(paths), allowed, len(set(allow) - used))


def selftest(pats):
    token = b"IQoJb3JpZ2luX2VjEXAMPLEFAKESESSIONTOKENVALUE0123456789abcdefABCDEF"
    cases = [
        ("presigned-sts", b'{"url":"https://x.s3.amazonaws.com/a.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQGYBPQ6EXAMPLE12%2F20261107%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Security-Token=' + token + b'&X-Amz-Signature=ab"}', {"aws-sts-session-token", "aws-access-key-id", "credential"}),
        ("json-escaped-sts", b'"X-Amz-Security-Token=' + token + b'\\u0026X-Amz-Signature=1"', {"aws-sts-session-token", "credential"}),
        ("header-sts", b"X-Amz-Security-Token: " + token + b"\r\n", {"aws-sts-session-token", "credential"}),
        ("json-key-sts", b'{"X-Amz-Security-Token": "' + token + b'"}', {"aws-sts-session-token", "credential"}),
        ("redacted", b'"https://x.s3.amazonaws.com/a.png?[presigned-query-redacted-r86]"', set()),
        ("short-token-field", b"X-Amz-Security-Token=abc", set()),
        ("aws-doc-example", b"X-Amz-Credential=AKIAIOSFODNN7EXAMPLE/20220830/us-east-1/ec2/aws4_request&", set()),
        ("real-shaped-akid", b"key AKIAZZZZZZZZZZZZZZZZ here", {"aws-access-key-id"}),
        ("akid-too-long", b"AKIAZZZZZZZZZZZZZZZZZ", set()),
        ("gate-private-key", b"-----BEGIN OPENSSH PRIVATE KEY-----", {"private-key"}),
        ("plain-prose", b"The session token is required when temporary credentials are used.", set()),
    ]
    bad = 0
    for name, data, want in cases:
        got = {s for s, _ in scan_bytes(data, pats)[0]}
        ok = got == want
        bad += not ok
        print("SELFTEST %s %s got=%s" % (name, "ok" if ok else "FAIL", ",".join(sorted(got)) or "none"))
    paths = [("corpus/source-snapshots/round-86/S122.txt", True),
             (".ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-x.json", True),
             (".ufo/waves/round-87/w1/live-capture.html", True),
             (".ufo/waves/round-43/w1/SentSecrets.md", False),
             ("corpus/knowledge/x.md", False)]
    for p, want in paths:
        ok = is_capture_path(p) == want
        bad += not ok
        print("SELFTEST scope %s %s" % (p, "ok" if ok else "FAIL"))
    fp = b'{"token": "authorization-envelope.json"}'
    cred = dict(pats)["credential"]
    digest = hashlib.sha256(cred.search(fp).group(0)).hexdigest()
    allow = {("r/x-receipts/a.json", "credential", digest): "file name, not a secret"}
    other = b'{"token": "authorization-envelope2.json"}'
    checks = [("allow-exact", scan_bytes(fp, pats, "r/x-receipts/a.json", allow), set(), 1),
              ("allow-other-value", scan_bytes(other, pats, "r/x-receipts/a.json", allow), {"credential"}, 0),
              ("allow-other-path", scan_bytes(fp, pats, "r/y-receipts/a.json", allow), {"credential"}, 0)]
    for name, (found, n), want, want_n in checks:
        got = {s for s, _ in found}
        ok = got == want and n == want_n
        bad += not ok
        print("SELFTEST %s %s got=%s allowed=%d" % (name, "ok" if ok else "FAIL", ",".join(sorted(got)) or "none", n))
    print("SELFTEST-RESULT %s cases=%d" % ("pass" if not bad else "fail", len(cases) + len(paths) + len(checks)))
    return 0 if not bad else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane")
    ap.add_argument("--rev")
    ap.add_argument("--files", nargs="+")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--allow", default=os.path.join(HERE, "capture-secret-allow.tsv"))
    a = ap.parse_args(argv)
    try:
        pats = patterns()
        if a.selftest:
            return selftest(pats)
        allow = load_allow(a.allow)
        if a.files:
            return scan_files(a.files, pats, allow)
        if a.lane and a.rev:
            return scan_rev(os.path.abspath(a.lane), a.rev, pats, allow)
    except (OSError, subprocess.CalledProcessError, AttributeError) as e:
        print("CAPTURE-SECRET-SCAN error reason=%s rc=2" % type(e).__name__)
        return 2
    print("CAPTURE-SECRET-SCAN error reason=usage rc=2")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
