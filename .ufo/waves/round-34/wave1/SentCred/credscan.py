#!/usr/bin/env python3
"""Round-34 credential/secret scan (SentCred seat, read-only, stdlib only).

Enumerates every lane artifact new or modified against the round-34 lane base
(and every untracked file), then scans each byte stream for credential material:
cloud/API key formats, JWTs, PEM/SSH/PGP private keys, HTTP basic-auth blobs,
secret-manager references, connection strings carrying a password, auth/cookie
headers, bearer tokens, session-id/csrf/password/api-key assignments, e-mail
addresses, URLs with query strings, non-public hosts, 64-hex tokens (digests are
the normal case in this repo and are reported separately), login/member markers
and HTTP header/status lines.

Exit: 0 = no S1/S2 material; 1 = at least one S1/S2 hit; 2 = enumeration failed.
Usage: python3 credscan.py [--base COMMIT] [--root LANE_ROOT] [--list FILE] [--json OUT]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SELF_TREE = "SentCred/"  # this seat's attachments
SELF_RECEIPT = ".ufo/waves/round-34/wave1/SentCred.md"  # quotes the pattern tokens it searched for
DEFAULT_ROOT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
DEFAULT_BASE = "014ee2d7aa8c3c095ff57ae51097606a9906228c"

PATTERNS = [
    ("S1", "cloud/api key format", re.compile(r"\b(?:sk_live_[0-9A-Za-z]{10,}|sk_test_[0-9A-Za-z]{10,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[0-9A-Za-z-]{10,}|AGE-SECRET-KEY-[0-9A-Z]+)\b")),
    ("S1", "JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{4,}\b")),
    ("S1", "PEM private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("S1", "ssh key blob", re.compile(r"ssh-(?:rsa|ed25519|dss) AAAA[0-9A-Za-z+/]+")),
    ("S1", "PGP private key", re.compile(r"-----BEGIN PGP PRIVATE KEY BLOCK-----")),
    ("S1", "HTTP basic-auth blob", re.compile(r"(?i)\bbasic\s+[A-Za-z0-9+/=]{12,}")),
    ("S1", "secret-manager ref", re.compile(r"\b(?:op://[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+|vault://[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+|sops://[^\s\"'`]+|age1[0-9a-z]{20,})")),
    ("S4", "secret-manager scheme word (no path)", re.compile(r"\b(?:op|vault)://(?![/A-Za-z0-9_-])")),
    ("S1", "connection string with password", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s:/@]+:[^\s@/]+@")),
    ("S2", "auth header", re.compile(r"(?im)^\s*(?:authorization|proxy-authorization|cookie|set-cookie|x-api-key|x-csrf-token)\s*:")),
    ("S2", "bearer token value", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{12,}=*")),
    ("S2", "session/csrf assignment", re.compile(r"(?i)\b(?:sessionid|session_id|sessiontoken|session_token|csrftoken|csrf_token|jsessionid|phpsessid|connect\.sid)\b\s*[=:]\s*\S+")),
    ("S2", "password assignment", re.compile(r"(?i)\b(?:password|passwd|pwd|passphrase)\b\s*[=:]\s*[^\s\"'`]{3,}")),
    ("S2", "api key assignment", re.compile(r"(?i)\b(?:api[_-]?key|apikey|access[_-]?key|secret[_-]?key|private[_-]?key|client[_-]?secret)\b\s*[=:]\s*[^\s\"'`]{6,}")),
    ("S3", "email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("S3", "URL with query string", re.compile(r"https?://[^\s<>\"'\)\]]*\?[^\s<>\"'\)\]]*")),
    ("S3", "non-public host", re.compile(r"(?i)\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|[\w.-]+\.internal\b|intranet)\b")),
    ("S4", "64-hex token (may be a declared digest)", re.compile(r"(?i)\b(?:0x)?[0-9a-f]{64}\b")),
    ("S4", "login/member marker", re.compile(r"(?i)\b(?:log ?in|sign ?in|log ?out|join immunefi|member area|my account|dashboard|profile|wallet connect)\b")),
    ("S4", "credential word", re.compile(r"(?i)\b(?:password|passwd|passphrase|secret|api[_-]?key|access[_-]?key|private[_-]?key|credential|bearer|session|cookie|csrf|xss)\b")),
    ("S4", "http header/status line", re.compile(r"(?im)^\s*(?:HTTP/\d(?:\.\d)?\s+\d{3}|server:|location:|content-type:|x-powered-by:)")),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def enumerate_artifacts(root, base):
    diff = subprocess.run(["git", "-C", root, "diff", "--name-only", base, "--", "."],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if diff.returncode != 0:
        sys.stderr.write(diff.stderr)
        return None
    others = subprocess.run(["git", "-C", root, "ls-files", "--others", "--exclude-standard"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if others.returncode != 0:
        sys.stderr.write(others.stderr)
        return None
    names = {line.strip() for line in diff.stdout.splitlines() if line.strip()}
    names |= {line.strip() for line in others.stdout.splitlines() if line.strip()}
    # The scanner's own tree contains the pattern literals it searches for; declared, not hidden.
    names = {n for n in names
             if not n.startswith(".ufo/waves/round-34/wave1/" + SELF_TREE)
             and n != SELF_RECEIPT}
    return sorted(names)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("KASEGI_LANE_ROOT", DEFAULT_ROOT))
    ap.add_argument("--base", default=os.environ.get("KASEGI_BASE", DEFAULT_BASE))
    ap.add_argument("--list", help="file of lane-relative paths instead of git enumeration")
    ap.add_argument("--json", help="write the full JSON report to this path")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if args.list:
        with open(args.list) as fh:
            rels = [line.strip() for line in fh if line.strip()]
    else:
        rels = enumerate_artifacts(root, args.base)
        if rels is None:
            return 2

    report = {"lane_root": root, "base": args.base, "artifacts": [], "hits": [],
              "separate_hex": [], "missing": []}
    for rel in rels:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            report["missing"].append(rel)
            continue
        raw = open(path, "rb").read()
        text = raw.decode("utf-8", "replace")
        report["artifacts"].append({"path": rel, "bytes": len(raw),
                                    "sha256": sha256(path),
                                    "lines": text.count("\n") + 1})
        for lineno, line in enumerate(text.splitlines(), 1):
            for sev, name, rx in PATTERNS:
                for m in rx.finditer(line):
                    hit = {"sev": sev, "cat": name, "path": rel,
                           "line": lineno, "match": m.group(0)[:160]}
                    if name.startswith("64-hex"):
                        report["separate_hex"].append(hit)
                    else:
                        report["hits"].append(hit)

    report["counts"] = {}
    for h in report["hits"]:
        key = "%s/%s" % (h["sev"], h["cat"])
        report["counts"][key] = report["counts"].get(key, 0) + 1
    report["hex_tokens"] = len(report["separate_hex"])
    blocking = [h for h in report["hits"] if h["sev"] in ("S1", "S2")]
    report["blocking"] = blocking

    text = json.dumps(report, indent=1)
    if args.json:
        with open(args.json, "w") as fh:
            fh.write(text + "\n")
    print("artifacts=%d hits=%d hex_tokens=%d blocking=%d"
          % (len(report["artifacts"]), len(report["hits"]),
             report["hex_tokens"], len(blocking)))
    for key in sorted(report["counts"]):
        print("  %s=%d" % (key, report["counts"][key]))
    for h in blocking:
        print("BLOCKING %s:%d [%s] %r" % (h["path"], h["line"], h["cat"], h["match"]))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
