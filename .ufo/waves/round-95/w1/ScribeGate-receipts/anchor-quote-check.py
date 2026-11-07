#!/usr/bin/env python3
"""ScribeGate-2 anchor/quote checker for the round-95 knowledge entry.

Checks every quote the entry makes against the committed bytes it names, and
checks that the brief-mandated exact scanner regex is present.  Prints one
ANCHOR line per assertion and a greppable summary.  Reads only; prints no
credential-shaped value (the receipt's example token is truncated before the
tail).
"""
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
ENTRY = (sys.argv[1] if len(sys.argv) > 1
         else "corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md")
S142 = "corpus/source-snapshots/round-95/S142.txt"
S140 = "corpus/source-snapshots/round-94/S140.txt"
RCPT141 = ".ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt"
RCPT06 = ".ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt"
SCAN = "corpus/instruments/capture-secret-scan.py"

bad = 0
total = 0


def line_of(path, n):
    with open(os.path.join(LANE, path), "rb") as fh:
        lines = fh.read().split(b"\n")
    return lines[n - 1] if 0 < n <= len(lines) else None


def check(label, got, want):
    global bad, total
    total += 1
    ok = got == want
    bad += not ok
    short = (got or b"<missing>")[:120]
    if not ok:
        print("ANCHOR %-34s BAD got=%r want=%r" % (label, short, want[:120]))
    else:
        print("ANCHOR %-34s OK %r" % (label, short))


def check_contains(label, got, needle):
    global bad, total
    total += 1
    ok = got is not None and needle in got
    bad += not ok
    print("ANCHOR %-34s %s contains=%r" % (label, "OK" if ok else "BAD", needle[:100]))


def entry_text():
    path = ENTRY if os.path.isabs(ENTRY) else os.path.join(LANE, ENTRY)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---- capture anchors the entry quotes -------------------------------------
check_contains("S142:169 ghr_ sentence", line_of(S142, 169), b"The token starts with ghr_.")
check_contains("S142:169 field name", line_of(S142, 169), b"refresh_tokenstring")
check("S140:429 glcbt keyword", line_of(S140, 429), b'keywords = ["glcbt-"]')
check("S140:446 glsat keyword", line_of(S140, 446), b'keywords = ["glsat-"]')
check("S140:463 gliamat keyword", line_of(S140, 463), b'keywords = ["gliamat-"]')
check("S140:428 glcbt id", line_of(S140, 428), b'id = "gitlab_ci_build_token_jwt"')
check("S140:445 glsat id", line_of(S140, 445), b'id = "gitlab_stateless_access_token"')
check("S140:462 gliamat id", line_of(S140, 462), b'id = "gitlab_iam_access_token"')
check("S140:430 glcbt regex", line_of(S140, 430), (
    b"regex = '''\\b(?:[a-zA-Z0-9]{1,20}-)?glcbt-eyJ[0-9a-zA-Z_\\-]{10,1000}"
    b"\\.eyJ[0-9a-zA-Z_\\-]{10,1000}\\.[0-9a-zA-Z_\\-]{20,1000}'''"))
check("S140:447 glsat regex", line_of(S140, 447), (
    b"regex = '''\\b(?:[a-zA-Z0-9]{1,20}-)?glsat-eyJ[0-9a-zA-Z_\\-]{10,1000}"
    b"\\.eyJ[0-9a-zA-Z_\\-]{10,1000}\\.[0-9a-zA-Z_\\-]{20,1000}'''"))
check("S140:464 gliamat regex", line_of(S140, 464), (
    b"regex = '''\\bgliamat-eyJ[0-9a-zA-Z_\\-]{10,1000}"
    b"\\.eyJ[0-9a-zA-Z_\\-]{10,1000}\\.[0-9a-zA-Z_\\-]{20,1000}'''"))
check("S141-receipt:16 line 72", line_of(RCPT141, 16), b'72:regex = "ghr_[0-9a-zA-Z]{76}"')
r06 = line_of(RCPT06, 10)
check_contains("S141-receipt:06 measurement", r06, b"ghr          total= 80 tail= 76")

# ---- scanner anchors (the exact regex the entry is required to show) -------
check("scanner:188 _ESC_LB", line_of(SCAN, 188), (
    b'_ESC_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\[ntr])|(?<=\\\\u[0-9A-Fa-f]{4})|'
    b'(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"'))
check("scanner:189 _GH_LB", line_of(SCAN, 189), b"_GH_LB = _ESC_LB")
check("scanner:191 _GH_REFRESH", line_of(SCAN, 191),
      b'_GH_REFRESH = rb"ghr_[A-Za-z0-9]{76}(?![A-Za-z0-9_])"')
check("scanner:193 github-token", line_of(SCAN, 193).strip(),
      b'("github-token", re.compile(')
check("scanner:196 github-refresh row", line_of(SCAN, 196),
      b'    ("github-refresh-token", re.compile(_GH_LB + _GH_REFRESH)),')
check("scanner:198 _GL_LB", line_of(SCAN, 198), (
    b'_GL_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\\\[ntr])|(?<=\\\\u[0-9A-Fa-f]{4})|'
    b'(?<=%[0-9A-Fa-f]{2})|(?<=&#[0-9]{2};)|(?<=&#[xX][0-9A-Fa-f]{2};))"'))
check("scanner:199 _GL_PREFIX", line_of(SCAN, 199),
      b'_GL_PREFIX = rb"(?:[A-Za-z0-9]{1,20}-)?"')
check("scanner:200 _GJ_SEG", line_of(SCAN, 200),
      b'_GJ_SEG = rb"[A-Za-z0-9_-]{10,1000}"')
check("scanner:201 _GJ_TAIL", line_of(SCAN, 201),
      b'_GJ_TAIL = rb"[A-Za-z0-9_-]{20,1000}"')
check("scanner:202 _GJ_HEAD", line_of(SCAN, 202),
      b'_GJ_HEAD = _GL_LB + rb"(?:" + _GL_PREFIX + rb"(?:glcbt|glsat)|gliamat)-eyJ" + _GJ_SEG')
check("scanner:207 gitlab-jwt row", line_of(SCAN, 207),
      b'    ("gitlab-jwt-token", re.compile(')
check("scanner:208 gitlab-jwt tail", line_of(SCAN, 208),
      b'        _GJ_HEAD + rb"\\.eyJ" + _GJ_SEG + rb"\\." + _GJ_TAIL + rb"(?![A-Za-z0-9_-])")),')
for n, name in [(439, "gh-refresh-76"), (440, "gh-refresh-75"), (441, "gh-refresh-77"),
                (442, "gh-refresh-36-classic"), (443, "gh-refresh-escape-u0020"),
                (444, "gl-jwt-clcbt"), (445, "gl-jwt-clcbt-custom"), (446, "gl-jwt-glsat"),
                (447, "gl-jwt-gliamat"), (448, "gl-jwt-not-eyj"), (449, "gl-jwt-short-head"),
                (450, "gl-jwt-third-19-chars"), (451, "gl-jwt-letter-before"),
                (452, "gl-jwt-doc-placeholder")]:
    check_contains("scanner:%d case" % n, line_of(SCAN, n), name.encode())

# ---- the brief's required exact regex in the entry ------------------------
text = entry_text()
required = [
    ('_GH_REFRESH = rb"ghr_[A-Za-z0-9]{76}(?![A-Za-z0-9_])"',
     "GitHub refresh regex"),
    ('("github-refresh-token", re.compile(_GH_LB + _GH_REFRESH))',
     "GitHub refresh row"),
    ('_GL_PREFIX = rb"(?:[A-Za-z0-9]{1,20}-)?"', "GitLab prefix"),
    ('_GJ_SEG = rb"[A-Za-z0-9_-]{10,1000}"', "JWT segment"),
    ('_GJ_TAIL = rb"[A-Za-z0-9_-]{20,1000}"', "JWT tail"),
    ('("gitlab-jwt-token", re.compile(', "GitLab JWT row"),
    ('_GJ_HEAD + rb"\\.eyJ" + _GJ_SEG + rb"\\." + _GJ_TAIL + rb"(?![A-Za-z0-9_-])")', "JWT tail expr"),
]
missing = 0
for needle, label in required:
    ok = needle in text
    missing += not ok
    print("REQUIRED %-28s %s" % (label, "present" if ok else "MISSING"))

# ---- the entry's recheck line ---------------------------------------------
m = re.search(r"^recheck:[ \t]*(.*)$", text, re.M)
cmd = m.group(1) if m else ""
rc = subprocess.run(["bash", "-n", "-c", cmd], capture_output=True).returncode
print("RECHECK-PARSE rc=%d %s" % (rc, "ok" if rc == 0 else "NOT-A-COMMAND"))

print("ANCHOR-CHECK total=%d bad=%d" % (total, bad))
print("ENTRY-REQUIRED missing=%d" % missing)
