#!/usr/bin/env python3
"""Independent S140-vs-instrument probe for round-96 C2 (critic seat)."""
import importlib.util
import os
import re
import sys

S = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


new = load(os.path.join(S, "inst-landing", "capture-secret-scan.py"), "new_instr")
base = load(os.path.join(S, "inst-base", "capture-secret-scan.py"), "base_instr")

NEW = {"gitlab-pat-versioned", "gitlab-pat-routable",
       "gitlab-runner-auth-token-versioned", "gitlab-deploy-token-versioned",
       "gitlab-agent-token-versioned", "gitlab-workspace-token-versioned",
       "gitlab-pipeline-trigger-token"}
OLD = {"github-token", "github-refresh-token", "gitlab-pat", "gitlab-jwt-token",
       "gitlab-runner-auth-token", "gitlab-deploy-token", "aws-access-key-id",
       "aws-sts-session-token", "gcs-signed-url-signature", "azure-sas-signature",
       "cloudfront-signed-url-signature", "cloudfront-signed-cookie-signature"}

# S140 published regexes, transcribed verbatim from
# corpus/source-snapshots/round-94/S140.txt (lines 30, 51, 73, 136, 324, 358, 375)
S140 = {
    "glpat_routable": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
    "glpat_versioned": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
    "glptt": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glptt-(?:[0-9a-zA-Z_\-]{20}|[0-9a-zA-Z_\-]{40}))(?:[^0-9a-zA-Z_\-]|$)"),
    "glrtr_versioned": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glrtr?-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
    "gldt_versioned": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?gldt-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
    "glagent_versioned": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
    "glwt_versioned": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glwt-[0-9a-zA-Z_\-]{27,300}\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7})\b"),
}

PATS_NEW = [(n, rx) for n, rx in new.patterns() if n in NEW | OLD]
PATS_BASE = [(n, rx) for n, rx in base.patterns() if n in NEW | OLD]


def shapes(mod_pats, data):
    got = set()
    for name, rx in mod_pats:
        if rx.search(data):
            got.add(name)
    return got


S140_MAP = {
    "glpat_routable": "gitlab-pat-routable",
    "glpat_versioned": "gitlab-pat-versioned",
    "glptt": "gitlab-pipeline-trigger-token",
    "glrtr_versioned": "gitlab-runner-auth-token-versioned",
    "gldt_versioned": "gitlab-deploy-token-versioned",
    "glagent_versioned": "gitlab-agent-token-versioned",
    "glwt_versioned": "gitlab-workspace-token-versioned",
}


def s140_hits(data):
    return {S140_MAP[k] for k, rx in S140.items() if rx.search(data)}


def rows():
    A = b"A"
    H = lambda n, c=A: c * n
    VER = b".ab.cd1234567"
    ROUT = b".ab" + b"cd12345"
    out = []

    def add(label, data, s140_expect, note=""):
        out.append((label, data, s140_expect, note))

    # --- glpat routable: head floor / ceiling / tail / case / boundary ---
    add("pat-rout-27", b"glpat-" + H(27) + ROUT, {"glpat_routable"})
    add("pat-rout-26", b"glpat-" + H(26) + ROUT, set())
    add("pat-rout-28", b"glpat-" + H(28) + ROUT, {"glpat_routable"})
    add("pat-rout-300", b"glpat-" + H(300) + ROUT, {"glpat_routable"})
    add("pat-rout-301", b"glpat-" + H(301) + ROUT, set())
    add("pat-rout-upper2", b"glpat-" + H(27) + b".AB" + b"cd12345", set())
    add("pat-rout-upper7", b"glpat-" + H(27) + b".ab" + b"CD12345", set())
    add("pat-rout-tail8", b"glpat-" + H(27) + b".ab" + b"cd1234567", set())
    add("pat-rout-tail6", b"glpat-" + H(27) + b".ab" + b"cd1234", set())
    add("pat-rout-rb-alnum", b"glpat-" + H(27) + ROUT + b"x", set())
    add("pat-rout-rb-underscore", b"glpat-" + H(27) + ROUT + b"_", set())
    add("pat-rout-rb-hyphen", b"glpat-" + H(27) + ROUT + b"-", {"glpat_routable"})
    add("pat-rout-rb-dot", b"glpat-" + H(27) + ROUT + b".", {"glpat_routable"})
    add("pat-rout-eos", b"glpat-" + H(27) + ROUT, {"glpat_routable"})
    add("pat-rout-prefix", b"acme-glpat-" + H(27) + ROUT, {"glpat_routable"})
    add("pat-rout-prefix20", b"a" * 20 + b"-glpat-" + H(27) + ROUT, {"glpat_routable"})
    add("pat-rout-prefix21", b"a" * 21 + b"-glpat-" + H(27) + ROUT, {"glpat_routable"})
    add("pat-rout-head-underscore", b"glpat-" + b"A_" * 13 + b"A" + ROUT, {"glpat_routable"})
    # plain 20-char family token must not be swallowed
    add("pat-plain-20", b"glpat-" + H(20), set())
    add("pat-plain-20-dot", b"glpat-" + H(20) + ROUT, set())
    add("pat-plain-20-then-hyphen", b"glpat-" + H(20) + b"-" + H(6) + ROUT, {"glpat_routable"})

    # --- glpat versioned ---
    add("pat-ver-27", b"glpat-" + H(27) + VER, {"glpat_versioned"})
    add("pat-ver-26", b"glpat-" + H(26) + VER, set())
    add("pat-ver-300", b"glpat-" + H(300) + VER, {"glpat_versioned"})
    add("pat-ver-301", b"glpat-" + H(301) + VER, set())
    add("pat-ver-mid1", b"glpat-" + H(27) + b".a.cd1234567", set())
    add("pat-ver-mid3", b"glpat-" + H(27) + b".abc.cd1234567", set())
    add("pat-ver-upper2", b"glpat-" + H(27) + b".AB.cd1234567", set())
    add("pat-ver-upper-mid", b"glpat-" + H(27) + b".ab.CD1234567", set())
    add("pat-ver-last6", b"glpat-" + H(27) + b".ab.cd123456", set())
    add("pat-ver-rb-alnum", b"glpat-" + H(27) + VER + b"x", set())
    add("pat-ver-rb-hyphen", b"glpat-" + H(27) + VER + b"-", {"glpat_versioned"})
    add("pat-ver-eos", b"glpat-" + H(27) + VER, {"glpat_versioned"})
    add("pat-ver-prefix", b"acme-glpat-" + H(27) + VER, {"glpat_versioned"})
    add("pat-ver-vs-rout", b"glpat-" + H(27) + VER, {"glpat_versioned"})

    # --- glrt / glrtr versioned ---
    add("glrtr-ver", b"glrtr-" + H(30) + VER, {"glrtr_versioned"})
    add("glrt-ver", b"glrt-" + H(30) + VER, {"glrtr_versioned"})
    add("glrtr-ver-prefix", b"acme-glrtr-" + H(30) + VER, {"glrtr_versioned"})
    add("glrtr-ver-nohyph", b"acmeglrtr-" + H(30) + VER, set())
    add("glrtr-ver-26", b"glrtr-" + H(26) + VER, set())
    add("glrtr-routable-tail", b"glrtr-" + H(30) + ROUT, set())
    add("glrtr-ver-upper", b"glrtr-" + H(30) + b".AB.cd1234567", set())

    # --- gldt / glagent / glwt versioned ---
    add("gldt-ver", b"gldt-" + H(30) + VER, {"gldt_versioned"})
    add("gldt-ver-prefix", b"acme-gldt-" + H(30) + VER, {"gldt_versioned"})
    add("gldt-ver-26", b"gldt-" + H(26) + VER, set())
    add("gldt-routable-tail", b"gldt-" + H(30) + ROUT, set())
    add("glagent-ver", b"glagent-" + H(30) + VER, {"glagent_versioned"})
    add("glagent-ver-prefix", b"acme-glagent-" + H(30) + VER, {"glagent_versioned"})
    add("glagent-ver-26", b"glagent-" + H(26) + VER, set())
    add("glwt-ver", b"glwt-" + H(30) + VER, {"glwt_versioned"})
    add("glwt-ver-prefix", b"acme-glwt-" + H(30) + VER, {"glwt_versioned"})
    add("glwt-ver-26", b"glwt-" + H(26) + VER, set())
    add("glwt-routable-tail", b"glwt-" + H(30) + ROUT, set())

    # --- glptt 20 / 40 / 39 ---
    add("glptt-20", b"glptt-" + H(20, b"G"), {"glptt"})
    add("glptt-40", b"glptt-" + H(40, b"G"), {"glptt"})
    add("glptt-19", b"glptt-" + H(19, b"G"), set())
    add("glptt-39", b"glptt-" + H(39, b"G"), set())
    add("glptt-41", b"glptt-" + H(41, b"G"), set())
    add("glptt-21", b"glptt-" + H(21, b"G"), set())
    add("glptt-20-rb-hyphen", b"glptt-" + H(20, b"G") + b"-", set())
    add("glptt-20-rb-underscore", b"glptt-" + H(20, b"G") + b"_", set())
    add("glptt-20-rb-alnum", b"glptt-" + H(20, b"G") + b"x", set())
    add("glptt-20-rb-dot", b"glptt-" + H(20, b"G") + b".", {"glptt"})
    add("glptt-20-eos", b"glptt-" + H(20, b"G"), {"glptt"})
    add("glptt-20-prefix", b"acme-glptt-" + H(20, b"G"), {"glptt"})
    add("glptt-40-prefix", b"acme-glptt-" + H(40, b"G"), {"glptt"})
    add("glptt-20-underscore-head", b"glptt-" + b"G_" * 10, {"glptt"})
    # --- swallow checks: a plain 20-char family token must not become a new shape ---
    add("plain-gldt-20", b"gldt-" + H(20), set())
    add("plain-gldt-20-dot", b"gldt-" + H(20) + VER, set())
    add("plain-glrt-20", b"glrt-" + H(20), set())
    add("plain-glrt-t1-20", b"glrt-t1_" + H(20), set())
    add("plain-glrtr-20-dot", b"glrtr-" + H(20) + VER, set())
    add("plain-pat-20-ver", b"glpat-" + H(20) + VER, set())
    add("plain-pat-20-rout", b"glpat-" + H(20) + ROUT, set())
    add("plain-pat-20-hyphen-ver", b"glpat-" + H(20) + b"-" + H(6) + VER, {"glpat_versioned"})
    add("glptt-20-hyphen-20", b"glptt-" + H(20, b"G") + b"-" + H(20, b"H"), set())
    add("glptt-20-hyphen-19", b"glptt-" + H(20, b"G") + b"-" + H(19, b"H"), {"glptt"})
    add("glptt-40-rb-hyphen", b"glptt-" + H(40, b"G") + b"-", set())
    return out


def old_plants():
    """One plant per earlier shape (round-95 tip vocabulary)."""
    jwt = b"eyJ" + b"a" * 20 + b".eyJ" + b"b" * 20 + b"." + b"c" * 20
    return {
        "github-token": b"ghp_" + b"1" * 36 + b" end",
        "github-refresh-token": b"ghr_" + b"2" * 76 + b" end",
        "gitlab-pat": b"glpat-" + b"3" * 20 + b" end",
        "gitlab-jwt-token": b"glcbt-" + jwt + b" end",
        "gitlab-runner-auth-token": b"glrt-" + b"4" * 20 + b" end",
        "gitlab-deploy-token": b"gldt-" + b"5" * 20 + b" end",
        "aws-access-key-id": b"AKIA" + b"ABCDEFGHIJKLMNOP" + b" end",
        "aws-sts-session-token": b"X-Amz-Security-Token=" + b"6" * 40 + b"&x=1",
        "gcs-signed-url-signature": b"X-Goog-Signature=" + b"a1" * 32 + b" end",
        "azure-sas-signature": b"?sv=2020-01-01&sig=" + b"Ab1" * 20 + b" end",
        "cloudfront-signed-url-signature": b"Signature=" + b"A" * 40 + b"&Key-Pair-Id=" + b"K" * 10 + b"&x=1",
        "cloudfront-signed-cookie-signature": b"CloudFront-Signature=" + b"B" * 40 + b" end",
    }


def main():
    bad = 0
    print("== S140 vs instrument: seven new shapes ==")
    print("%-26s %-8s %-8s %-8s %s" % ("case", "s140", "new", "agree", "shapes-new"))
    for label, data, want, _note in rows():
        s = s140_hits(data)
        n = shapes(PATS_NEW, data) & NEW
        want = {S140_MAP[k] for k in want}
        agree = (s == want) and (n == want)
        if not agree:
            bad += 1
        print("%-26s %-8s %-8s %-8s %s" % (
            label, ",".join(sorted(s)) or "-", ",".join(sorted(n)) or "-",
            "yes" if agree else "NO", ",".join(sorted(n)) or "-"))
        if not agree:
            print("    bytes=%r want=%s" % (data, sorted(want)))

    print("\n== earlier shapes: base vs new instrument ==")
    plants = old_plants()
    base_missing, new_missing, new_extra = [], [], []
    for name, data in plants.items():
        bs = shapes(PATS_BASE, data)
        ns = shapes(PATS_NEW, data)
        if name not in bs:
            base_missing.append((name, sorted(bs)))
        if name not in ns:
            new_missing.append((name, sorted(ns)))
        extra = ns - {name}
        if extra:
            new_extra.append((name, sorted(extra)))
        print("%-38s base=%-38s new=%s" % (name, ",".join(sorted(bs)) or "-", ",".join(sorted(ns)) or "-"))
    print("base_missing=%s" % (base_missing or "none"))
    print("new_missing=%s" % (new_missing or "none"))
    print("new_extra=%s" % (new_extra or "none"))
    if base_missing or new_missing or new_extra:
        bad += 1

    print("\n== shape-name inventory ==")
    bn = {n for n, _ in base.patterns()}
    nn = {n for n, _ in new.patterns()}
    print("base_shapes=%d new_shapes=%d" % (len(bn), len(nn)))
    print("lost=%s" % (sorted(bn - nn) or "none"))
    print("added=%s" % (sorted(nn - bn) or "none"))
    print("OLD subset of base=%s" % (OLD <= bn))
    print("OLD subset of new=%s" % (OLD <= nn))
    print("NEW in base=%s" % (sorted(NEW & bn) or "none"))
    print("\nPROBE-BAD=%d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
