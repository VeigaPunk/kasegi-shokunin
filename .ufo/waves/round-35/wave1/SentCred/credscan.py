#!/usr/bin/env python3
"""Round-35 seat SentCred — credential/secret scan of every artifact new in the round.

Scope: every path the lane reports as changed since the frozen base plus every
untracked path (`git diff --name-only <BASE>` + `git ls-files --others
--exclude-standard`), read as bytes from the lane root.

Classes (round-35 receipt §Method):
  S1 credential material  — a secret value that is usable as-is (provider key
                            shapes, private-key blocks, vault-reference URIs).
  S2 session/auth values  — a live auth value or a URL that carries one
                            (header values, bearer/basic payloads, userinfo
                            URLs, token/signature query parameters, netrc/ssh).
  S3 triage               — non-blocking observations: addresses, tracking
                            parameters, cleartext http URLs. Printed, never
                            counted as a hit (a public CVE feed legitimately
                            carries vendor links and mailing-list addresses).

Excluded from its own scan: `.ufo/waves/round-35/wave1/SentCred` (this file and
the receipt name the patterns, so they would match themselves). The exclusion is
by prefix and is reported in the summary line.

Exit: 0 = no S1/S2 hit; 3 = at least one S1/S2 hit. A missing path is exit 2.

Usage: python3 credscan.py [--root /path/to/lane] [--base <sha>]
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

BASE_DEFAULT = "3266c9937b03062d9bbc2f436e20820115ed179c"
EXCLUDE_PREFIX = ".ufo/waves/round-35/wave1/SentCred"

S1 = [
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA)[0-9A-Z]{16}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("slack_token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("stripe_key", re.compile(r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]{10,}\b")),
    # Anchored so a hyphenated slug ("risk-known-exploited-...") cannot match.
    ("openai_key", re.compile(r"(?:^|[^A-Za-z0-9_-])sk-(?:proj-|ant-)?[A-Za-z0-9]{32,}")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{8,}\b")),
    ("private_key_block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("ssh_public_key", re.compile(r"\bssh-(?:rsa|ed25519|dss)\s+AAAA[A-Za-z0-9+/=]{20,}")),
    ("vault_reference", re.compile(r"\bop://[^\s`\"'()]+")),
    ("age_secret", re.compile(r"\bAGE-SECRET-KEY-[0-9A-Z]{10,}")),
    ("gitlab_pat", re.compile(r"\bglpat-[A-Za-z0-9_-]{16,}\b")),
    ("sendgrid_key", re.compile(r"\bSG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\b")),
    ("docker_pat", re.compile(r"\bdckr_pat_[A-Za-z0-9_-]{10,}\b")),
    ("pypi_token", re.compile(r"pypi-AgEIcHlwaS5vcmc")),
    ("npmrc_auth", re.compile(r"_authToken\s*=")),
]

S2 = [
    ("auth_header", re.compile(r"(?i)\b(?:authorization|set-cookie|cookie)\s*:\s*(?:bearer|basic|digest|token|session)\b")),
    ("bearer_value", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{10,}")),
    ("basic_value", re.compile(r"(?i)\bbasic\s+[A-Za-z0-9+/=]{16,}")),
    ("credential_assignment", re.compile(
        r"(?i)\b(?:password|passwd|pwd|api[_-]?key|apikey|access[_-]?key|secret[_-]?key|"
        r"client[_-]?secret|session[_-]?id|csrf[_-]?token)\b\s*[=:]\s*[^\s\"'`]{4,}")),
    ("userinfo_url", re.compile(r"\bhttps?://[^\s/\"'@]+:[^\s/\"'@]{2,}@")),
    ("query_secret", re.compile(r"(?i)[?&](?:token|key|api_?key|sig|signature|access_?token|password|secret)=[^&\s]+")),
    ("netrc_ssh_paths", re.compile(r"(?i)(?:\.netrc|id_rsa|id_ed25519|\.ssh/|\.aws/credentials|\.config/gh)")),
    ("x_api_key_header", re.compile(r"(?i)\bx-api-key\s*:\s*\S+")),
]

S3 = [
    ("email_address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("tracking_param", re.compile(r"(?i)[?&](?:_ga|_gl|gclid|fbclid|msclkid|utm_)=[^&\s]+")),
    ("cleartext_http_url", re.compile(r"\bhttp://[^\s\"'<>)]+")),
    ("private_ip_literal", re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|"
        r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b")),
]


def enumerate_paths(root, base):
    diff = subprocess.run(
        ["git", "-C", root, "diff", "--name-only", base],
        capture_output=True, text=True, check=True).stdout.split()
    untracked = subprocess.run(
        ["git", "-C", root, "ls-files", "--others", "--exclude-standard"],
        capture_output=True, text=True, check=True).stdout.split()
    return sorted(set(diff) | set(untracked))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--show-s3", action="store_true", help="print triage class hits")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    paths = enumerate_paths(root, args.base)
    excluded = [p for p in paths if p.startswith(EXCLUDE_PREFIX)]
    scanned = [p for p in paths if not p.startswith(EXCLUDE_PREFIX)]

    hits = {"S1": [], "S2": [], "S3": []}
    total_bytes = 0
    for rel in scanned:
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            print("MISSING", rel)
            return 2
        blob = open(full, "rb").read()
        total_bytes += len(blob)
        text = blob.decode("utf-8", "replace")
        for klass, table in (("S1", S1), ("S2", S2), ("S3", S3)):
            for name, rx in table:
                for m in rx.finditer(text):
                    line = text.count("\n", 0, m.start()) + 1
                    hits[klass].append((name, rel, line, m.group(0)[:100]))

    blocking = len(hits["S1"]) + len(hits["S2"])
    print("scan root=%s base=%s" % (root, args.base))
    print("files=%d bytes=%d excluded_self=%d" % (len(scanned), total_bytes, len(excluded)))
    for klass in ("S1", "S2"):
        for name, rel, line, token in hits[klass]:
            print("%s %s %s:%d %r" % (klass, name, rel, line, token))
    if args.show_s3:
        for name, rel, line, token in hits["S3"]:
            print("S3 %s %s:%d %r" % (name, rel, line, token))
    print("s1=%d s2=%d s3=%d exit=%d" % (
        len(hits["S1"]), len(hits["S2"]), len(hits["S3"]), 3 if blocking else 0))
    sys.stdout.flush()

    # Digests of everything scanned, so a later reader can tell whether the tree
    # moved between this scan and theirs.
    for rel in scanned:
        blob = open(os.path.join(root, rel), "rb").read()
        print("sha256 %s %s" % (hashlib.sha256(blob).hexdigest(), rel), file=sys.stderr)
    return 3 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
