#!/usr/bin/env python3
"""CriticClaimsC2: independence attack on the round-98 C2 capability gate.

Loads the landing instrument and the gate, rebuilds the gate's plants from a
seed, then runs a matrix of wrong instruments over the same plants and over
targeted probes.  Prints one line per (variant, limb) with the observed set.
"""
import contextlib
import importlib.util
import io
import os
import re
import sys

S = "/fast/scratch/hyaku/kasegi-r98/CriticClaimsC2"
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gate = load(LANE + "/.ufo/waves/round-98/c2/capability-check.py", "gate")
inst = load(S + "/land/capture-secret-scan.py", "inst")
base = load(S + "/base/capture-secret-scan.py", "base")

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 777001
root, rev, expect = gate.build_plants(S + "/attack", SEED)
paths = [os.path.join(dp, f) for dp, _, fs in os.walk(root)
         for f in fs if "/.git/" not in os.path.join(dp, f)]
print("PLANTS root=%s rev=%s files=%d expect=%d" % (root, rev, len(paths), len(expect)))
for e in sorted(expect):
    print("EXPECT %s %s" % e)


def scan(pats, file_paths):
    hits = set()
    for p in file_paths:
        data = open(p, "rb").read()
        for name, rx in pats:
            if rx.search(data):
                hits.add((os.path.basename(p), name))
    return hits


def selftest(pats):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = inst.selftest(pats)
    out = buf.getvalue()
    m = re.search(r"SELFTEST-RESULT (\w+) cases=(\d+)", out)
    fails = [ln for ln in out.splitlines() if " FAIL " in ln]
    return rc, (m.group(1) if m else "none"), (m.group(2) if m else "?"), fails


def report(tag, pats, probes=(), do_selftest=True):
    hits = scan(pats, paths)
    missing = sorted(expect - hits)
    extra = sorted(hits - expect)
    k3 = "PASS" if hits == expect else "FAIL"
    if do_selftest:
        rc, st, cases, fails = selftest(pats)
        print("VARIANT %s K3=%s hits=%d missing=%s extra=%s | SELFTEST rc=%d %s cases=%s fails=%d" % (
            tag, k3, len(hits), missing or "none", extra or "none", rc, st, cases, len(fails)))
    else:
        print("VARIANT %s K3=%s hits=%d missing=%s extra=%s | SELFTEST skipped" % (
            tag, k3, len(hits), missing or "none", extra or "none"))
    for ln in (fails if do_selftest else [])[:6]:
        print("  SELFTEST-FAIL %s" % ln)
    for label, payload in probes:
        got = sorted({s for s, _ in inst.scan_bytes(payload, pats)[0]})
        want = sorted({s for s, _ in inst.scan_bytes(payload, inst.patterns())[0]})
        print("  PROBE %s payload=%r correct=%s variant=%s %s" % (
            label, payload, want or "none", got or "none",
            "DIVERGES" if got != want else "same"))
    return hits


LB = inst._GL_LB
print("LEFT-BOUNDARY %r" % LB)

# --- V0: the landing instrument itself ------------------------------------
report("V0-landing", inst.patterns())

# --- V1: literal-locked matcher (only the instrument's own selftest literals)
LITERALS = {
    "gitlab-ci-build-token": b"glcbt-Ab3_" + b"k" * 20,
    "gitlab-iam-refresh-token": b"gliamrt-" + b"A" * 43 + b"." + b"B" * 43,
    "gitlab-iam-authorization-code": b"gliamac-" + b"C" * 43 + b"." + b"D" * 43,
    "gitlab-session-cookie": b"_gitlab_session=" + b"0a" * 32,
    "gitlab-runner-registration-token": b"GR1348941" + b"A" * 20,
    "gitlab-feed-token": b"feed_token=" + b"B" * 20,
    "gitlab-oauth-app-secret": b"gloas-" + b"C" * 64,
    "gitlab-feed-token-v2": b"glft-" + b"D" * 20,
    "gitlab-scim-oauth-token": b"glsoat-" + b"F" * 20,
}
lit_pats = [(n, re.compile(re.escape(v))) for n, v in LITERALS.items()]
report("V1-literal-locked", lit_pats, do_selftest=False, probes=[
    ("selftest-literal", LITERALS["gitlab-ci-build-token"] + b" end"),
    ("plant-p1", b"glcbt-Zz9_" + b"Q" * 20 + b" end"),
])

# --- V2: session-cookie without the assignment context --------------------
v2 = [((n, re.compile(rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])"))
       if n == "gitlab-session-cookie" else (n, rx)) for n, rx in inst.patterns()]
print("V2TYPES", [(i,type(x),type(x[1])) for i,x in enumerate(v2) if not hasattr(x[1],"search")]); report("V2-session-nocontext", v2, probes=[
    ("bare-64-hex", b"x=" + b"0a" * 32 + b"\n"),
    ("bare-64-hex-upper", b"x=" + b"0A" * 32 + b"\n"),
])

# --- V3: keyword kept, geo/cell structure dropped -------------------------
v3 = [((n, re.compile(LB + rb"_gitlab_session[\s\"'=:;]+[0-9a-f]{64}(?![0-9a-f])"))
       if n == "gitlab-session-cookie" else (n, rx)) for n, rx in inst.patterns()]
report("V3-session-keyword-only", v3, probes=[
    ("geo", b"_gitlab_session_geo_" + b"0a" * 32 + b"=" + b"1b" * 32 + b"\n"),
    ("cell", b"_gitlab_session=" + b"cell-7-" + b"0a" * 32 + b"\n"),
])

# --- V4: ci-build-token keeps the round-97 strict right boundary ----------
v4 = [((n, re.compile(LB + rb"glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"))
       if n == "gitlab-ci-build-token" else (n, rx)) for n, rx in inst.patterns()]
report("V4-ci-build-strict-boundary", v4, probes=[
    ("token-then-underscore", b"glcbt-Ab3_" + b"k" * 20 + b"_x\n"),
    ("token-then-hyphen", b"glcbt-Ab3_" + b"k" * 20 + b"-x\n"),
])

# --- V5: ci-build-token prefix 0-5 instead of 1-5 -------------------------
v5 = [((n, re.compile(LB + rb"glcbt-[A-Za-z0-9]{0,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9])"))
       if n == "gitlab-ci-build-token" else (n, rx)) for n, rx in inst.patterns()]
report("V5-ci-build-zero-prefix", v5, probes=[
    ("zero-prefix", b"glcbt-_" + b"k" * 20 + b" end\n"),
])

# --- V6: iam second segment 43+ instead of exactly 43 ---------------------
v6 = []
for n, rx in inst.patterns():
    if n == "gitlab-iam-refresh-token":
        v6.append((n, re.compile(LB + rb"gliamrt-[A-Za-z0-9_-]{43}\.[A-Za-z0-9_-]{43,}(?![A-Za-z0-9_-])")))
    elif n == "gitlab-iam-authorization-code":
        v6.append((n, re.compile(LB + rb"gliamac-[A-Za-z0-9_-]{43}\.[A-Za-z0-9_-]{43,}(?![A-Za-z0-9_-])")))
    else:
        v6.append((n, rx))
report("V6-iam-second-43plus", v6, probes=[
    ("second-44", b"gliamrt-" + b"A" * 43 + b"." + b"B" * 44 + b" \n"),
    ("second-44-auth", b"gliamac-" + b"A" * 43 + b"." + b"B" * 44 + b" \n"),
])

# --- V7: widened shapes with no right boundary at all ---------------------
WIDENED = ["gitlab-runner-registration-token", "gitlab-feed-token",
           "gitlab-oauth-app-secret", "gitlab-feed-token-v2",
           "gitlab-scim-oauth-token"]
v7 = []
for n, rx in inst.patterns():
    if n in WIDENED:
        pat = rx.pattern
        assert pat.endswith(rb"(?![A-Za-z0-9])"), (n, pat)
        v7.append((n, re.compile(pat[:-len(rb"(?![A-Za-z0-9])")])))
    else:
        v7.append((n, rx))
report("V7-widened-no-boundary", v7, probes=[
    ("21-chars", b"GR1348941" + b"A" * 21 + b"\n"),
])

# --- V8: widened shapes keep the round-97 strict boundary -----------------
v8 = [(n, rx) for n, rx in inst.patterns() if n not in WIDENED]
v8 += [(n, rx) for n, rx in base.patterns() if n in WIDENED]
report("V8-widened-strict-boundary", v8, probes=[
    ("token-then-underscore", b"GR1348941" + b"A" * 20 + b"_x\n"),
])

# --- V7b: no boundary only for the three shapes whose negatives are short --
V7B = ["gitlab-feed-token", "gitlab-oauth-app-secret", "gitlab-scim-oauth-token"]
v7b = []
for n, rx in inst.patterns():
    if n in V7B:
        pat = rx.pattern
        assert pat.endswith(rb"(?![A-Za-z0-9])"), (n, pat)
        v7b.append((n, re.compile(pat[:-len(rb"(?![A-Za-z0-9])")])))
    else:
        v7b.append((n, rx))
report("V7b-no-boundary-three", v7b, probes=[
    ("feed-21", b"feed_token=" + b"B" * 21 + b"&\n"),
    ("oauth-65", b"gloas-" + b"C" * 65 + b" \n"),
    ("scim-21", b"glsoat-" + b"F" * 21 + b" \n"),
])

# --- V9: the do-nothing instrument (round-97 landing) ---------------------
report("V9-do-nothing-base", base.patterns())
