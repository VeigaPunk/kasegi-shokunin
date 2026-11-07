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
capture-class paths: anything under corpus/source-snapshots/, anything under a
practice package's evidence directory `corpus/practice/<pkg>/evidence/` (round
88: practice packages keep copies of their captures there), any path with a
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
  gcs-signed-url-signature  (round 88) `X-Goog-Signature=<hex>` (query string)
                         or `X-Goog-Signature: <hex>` with 64+ hex digits: a Cloud
                         Storage V4 signed URL's signature; "Anyone in possession
                         of the signed URL can use it while it's active" (S126
                         lines 423-424; parameter, lines 487-488).
  azure-sas-signature    (round 88) a `sig=<value>` query parameter of 40+
                         base64/percent-encoded characters in the same query as
                         an `sv=YYYY-MM-DD` storage-version parameter, either
                         order, separated by `&`, `&amp;` or JSON `\\u0026`: an
                         Azure Storage SAS signature, an HMAC-SHA256 "encoded by
                         using Base64 encoding" (S127 lines 402-404, 605, 638-639).
                         Round 89: the match may start right after a `\\u0026`
                         or `%26` separator, so a JSON-escaped SAS whose first
                         matched parameter is not the query's first parameter
                         (S127 line 605's order, sv sixth) is detected.
  cloudfront-signed-url-signature  (round 89) a `Signature=<value>` query
                         parameter of 40+ CloudFront URL-safe base64 characters
                         (`A-Za-z0-9`, `-`, `_`, `~`: CloudFront replaces `+`,
                         `=`, `/` with `-`, `_`, `~`, S128 lines 202-211) in the
                         same query as a `Key-Pair-Id=<ID>` parameter (8-32
                         upper-case letters or digits), either order, separated
                         by `&`, `&amp;` or `\\u0026`, parameter names
                         case-sensitive, any other parameters (Expires, Policy,
                         Hash-Algorithm) between: an Amazon CloudFront signed URL,
                         canned or custom policy (S128 lines 13, 70-78; S130 lines
                         14, 75-84). "anyone with the signed URL can access" the
                         files its policy covers (S130 lines 163-165). A
                         `Signature=` preceded by `-` (`X-Amz-Signature=`) never
                         starts a match.
Known limits: GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed
cookies (`CloudFront-Signature`), percent-encoded parameter names or `=`
(a whole URL percent-encoded inside another URL's query), more than 20 other
parameters between the two matched ones, values soft-wrapped across lines,
and gzip/UTF-16/base64-wrapped captures are not detected.
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
_SEP = rb"(?:&amp;|&|\\u0026)"
_PARAM = rb"(?:" + _SEP + rb"[A-Za-z]{2,6}=[^&\s\"'<>\\]*){0,20}?"
_SIG = rb"sig=[A-Za-z0-9%+/]{40,}(?:=|%3D){0,2}"
_SV = rb"sv=\d{4}-\d{2}-\d{2}"
_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\u0026)|(?<=%26))"
_CF_LB = rb"(?:(?<![A-Za-z0-9_-])|(?<=\\u0026)|(?<=%26))"
_CF_PARAM = rb"(?:" + _SEP + rb"[A-Za-z][A-Za-z0-9_-]{0,31}=[^&\s\"'<>\\]*){0,20}?"
_CF_SIG = rb"Signature=[A-Za-z0-9_~-]{40,}"
_CF_KPI = rb"Key-Pair-Id=[A-Z0-9]{8,32}(?![A-Za-z0-9_-])"
CLOUD_PATTERNS = (
    ("gcs-signed-url-signature", re.compile(
        rb"(?i)X-Goog-Signature(?:=|\\?[\"']?\s*:\s*\\?[\"']?)[0-9a-f]{64,}")),
    ("azure-sas-signature", re.compile(
        rb"(?i)" + _LB + rb"(?:" + _SV + _PARAM + _SEP + _SIG + rb"|" + _SIG + _PARAM + _SEP + _SV + rb")")),
    ("cloudfront-signed-url-signature", re.compile(
        _CF_LB + rb"(?:" + _CF_SIG + _CF_PARAM + _SEP + _CF_KPI + rb"|" + _CF_KPI + _CF_PARAM + _SEP + _CF_SIG + rb")")),
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
    return gate_patterns() + AWS_PATTERNS + CLOUD_PATTERNS


def is_capture_path(rel):
    parts = rel.split("/")
    return (rel.startswith("corpus/source-snapshots/")
            or (len(parts) >= 5 and parts[:2] == ["corpus", "practice"] and parts[3] == "evidence")
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
    gsig = b"0123456789abcdef" * 8
    asig = b"FAKEsasSIGNATUREfake0123456789abcdefABCDEFG%3D"
    cfsig = b"FAKEcfSIGNATUREfake~0123456789-abcdefABCDEF_ghijklmnopqrstuvwxyz~XYZ"
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
        ("gcs-v4-query", b"https://storage.googleapis.com/b/o.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=svc%40p.iam.gserviceaccount.com%2F20261107%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20261107T000000Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=" + gsig + b'"', {"gcs-signed-url-signature"}),
        ("gcs-json-key", b'{"X-Goog-Signature": "' + gsig + b'"}', {"gcs-signed-url-signature"}),
        ("gcs-doc-wrapped", b"X-Goog-SignedHeaders=host&X-Goog-Signature=247a2aa45f16\n9edf4d187d54e7cc46e4731b1e6273242c4f4c39a1d2507a0e58706e25e3a85a7dbb891d62afa849", set()),
        ("gcs-short", b"X-Goog-Signature=0123456789abcdef0123456789abcdef", set()),
        ("azure-sv-first", b"https://a.blob.core.windows.net/c/b.txt?sp=r&st=2026-11-07T00:00:00Z&se=2026-11-08T00:00:00Z&spr=https&sv=2022-11-02&sr=b&sig=" + asig, {"azure-sas-signature"}),
        ("azure-sig-first", b"https://a.blob.core.windows.net/c/b.txt?sig=" + asig + b"&se=2026-11-08T00:00:00Z&sv=2022-11-02&sp=r", {"azure-sas-signature"}),
        ("azure-json-escaped", b'"https://a.blob.core.windows.net/c/b.txt?sv=2022-11-02\\u0026sr=b\\u0026sig=' + asig + b'"', {"azure-sas-signature"}),
        ("azure-html-amp", b'<a href="https://a.blob.core.windows.net/c/b.txt?sv=2022-11-02&amp;sr=b&amp;sig=' + asig + b'">', {"azure-sas-signature"}),
        ("azure-doc-placeholder", b"https://myaccount.blob.core.windows.net/sascontainer/blob1.txt?sp=rw&spr=https&sv=2022-11-02&sr=b&sig=<signature>", set()),
        ("azure-sig-without-sv", b"https://example.com/x?id=1&sig=" + asig, set()),
        ("azure-short-sig", b"https://a.blob.core.windows.net/c?sv=2022-11-02&sig=abcdEFGH1234", set()),
        ("azure-json-escaped-s127-order", b'"https://myaccount.blob.core.windows.net/sascontainer/blob1.txt?sp=rw\\u0026st=2026-11-07T00:00:00Z\\u0026se=2026-11-08T00:00:00Z\\u0026spr=https\\u0026sv=2022-11-02\\u0026sr=b\\u0026sig=' + asig + b'"', {"azure-sas-signature"}),
        ("cf-canned", b"https://d111111abcdef8.cloudfront.net/image.jpg?color=red&size=medium&Expires=1767290400&Signature=" + cfsig + b"&Key-Pair-Id=K2JCJMDEHXQW5F&Hash-Algorithm=SHA256", {"cloudfront-signed-url-signature"}),
        ("cf-custom", b"https://d111111abcdef8.cloudfront.net/image.jpg?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMTExMTExYWJjZGVmOC5jbG91ZGZyb250Lm5ldC8qIn1dfQ__&Signature=" + cfsig + b"&Key-Pair-Id=K2JCJMDEHXQW5F", {"cloudfront-signed-url-signature"}),
        ("cf-kpi-first-json", b'"https://d1.cloudfront.net/a.mp4?Key-Pair-Id=K2JCJMDEHXQW5F\\u0026Expires=1767290400\\u0026Signature=' + cfsig + b'"', {"cloudfront-signed-url-signature"}),
        ("cf-html-amp", b'<a href="https://d1.cloudfront.net/a.mp4?Expires=1767290400&amp;Signature=' + cfsig + b'&amp;Key-Pair-Id=K2JCJMDEHXQW5F">', {"cloudfront-signed-url-signature"}),
        ("cf-doc-placeholder", b"5. &Signature=hashed and signed version of the policy statement 6. &Key-Pair-Id=public key ID for the", set()),
        ("cf-sig-without-kpi", b"https://d1.cloudfront.net/a.mp4?Expires=1767290400&Signature=" + cfsig, set()),
        ("cf-amz-signature-beside-kpi", b"https://x.s3.amazonaws.com/a?X-Amz-Signature=" + b"ab" * 32 + b"&Key-Pair-Id=K2JCJMDEHXQW5F", set()),
        ("cf-short-sig", b"https://d1.cloudfront.net/a.mp4?Signature=abcDEF123~-_&Key-Pair-Id=K2JCJMDEHXQW5F", set()),
        ("cf-lowercase-names", b"https://d1.cloudfront.net/a.mp4?signature=" + cfsig + b"&key-pair-id=K2JCJMDEHXQW5F", set()),
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
             ("corpus/practice/curl-ibb-h1-1997312/evidence/S122.txt", True),
             ("corpus/practice/curl-ibb-h1-1997312/report.md", False),
             ("corpus/practice/evidence/x.txt", False),
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
