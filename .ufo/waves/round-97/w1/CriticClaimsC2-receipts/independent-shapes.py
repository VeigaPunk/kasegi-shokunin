#!/usr/bin/env python3
"""Independent re-derivation of the ten round-97 GitLab shapes against the
S140 published regexes (corpus/source-snapshots/round-94/S140.txt lines 101,
160, 174, 190, 213, 229, 278, 341, 392, 412).

Compares, per case: S140's own regex (translated to Python bytes) vs the
instrument's compiled pattern for that shape, and records every other shape
the instrument fires on the same bytes (swallow / double-report check).
"""
import importlib.util
import re
import sys

NEW = "/fast/scratch/hyaku/kasegi-r97/CriticClaimsC2/work-7001/inst-rev/corpus/instruments/capture-secret-scan.py"
BASE = "/fast/scratch/hyaku/kasegi-r97/CriticClaimsC2/work-7001/inst-base/corpus/instruments/capture-secret-scan.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


new = load(NEW, "inst_new")
base = load(BASE, "inst_base")
newp = dict(new.patterns())
basep = dict(base.patterns())

# POSIX [[:punct:]] = ASCII punctuation; [[:space:]]/[[:blank:]] = whitespace.
PUNCT_OR_SPACE = rb"[!-/:-@\[-`{-~]|[ \t\n\r\f\v]"
S140 = {
    "gitlab-runner-registration-token": re.compile(
        rb"\b(GR1348941[0-9a-zA-Z_\-]{20})(?:" + PUNCT_OR_SPACE + rb"|$)"),
    "gitlab-feed-token": re.compile(
        rb"\b(feed_token=[0-9a-zA-Z_\-]{20})(?:" + PUNCT_OR_SPACE + rb"|$)"),
    "gitlab-oauth-app-secret": re.compile(
        rb"\b(gloas-[0-9a-zA-Z_\-]{64})(?:" + PUNCT_OR_SPACE + rb"|$)"),
    "gitlab-feed-token-v2": re.compile(
        rb"\b(glft-[0-9a-zA-Z_\-]{20})(?:" + PUNCT_OR_SPACE + rb"|$)"),
    "gitlab-kubernetes-agent-token": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{50})(?:[^0-9a-zA-Z_\-.]|\.[^0-9a-z]|\.$|$)"),
    "gitlab-incoming-email-token": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glimt-[0-9a-z]{20,25})(?:[^0-9a-zA-Z_\-]|$)"),
    "gitlab-scim-oauth-token": re.compile(
        rb"\b(glsoat-[0-9a-zA-Z_\-]{20})(?:" + PUNCT_OR_SPACE + rb"|$)"),
    "gitlab-deploy-token-in-url": re.compile(
        rb"gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@"),
    "gitlab-feature-flags-client-token": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glffct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)"),
    "gitlab-runner-controller-token": re.compile(
        rb"\b((?:[a-zA-Z0-9]{1,20}-)?glrct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)"),
}

A = b"A"
CASES = []


def add(shape, label, data):
    CASES.append((shape, label, data))


# --- registration: GR1348941 + exactly 20 --------------------------------
add("gitlab-runner-registration-token", "exact+space", b"GR1348941" + A * 20 + b" ")
add("gitlab-runner-registration-token", "exact+eos", b"GR1348941" + A * 20)
add("gitlab-runner-registration-token", "exact+dot", b"GR1348941" + A * 20 + b".")
add("gitlab-runner-registration-token", "exact+newline", b"GR1348941" + A * 20 + b"\n")
add("gitlab-runner-registration-token", "exact+quote", b'"GR1348941' + A * 20 + b'"')
add("gitlab-runner-registration-token", "exact+underscore", b"GR1348941" + A * 20 + b"_")
add("gitlab-runner-registration-token", "exact+hyphen", b"GR1348941" + A * 20 + b"-")
add("gitlab-runner-registration-token", "exact+letter", b"GR1348941" + A * 20 + b"Z")
add("gitlab-runner-registration-token", "exact+digit", b"GR1348941" + A * 20 + b"9")
add("gitlab-runner-registration-token", "exact+nonascii", b"GR1348941" + A * 20 + b"\xc3\xa9")
add("gitlab-runner-registration-token", "19chars", b"GR1348941" + A * 19 + b" ")
add("gitlab-runner-registration-token", "21chars", b"GR1348941" + A * 21 + b" ")
add("gitlab-runner-registration-token", "word-before", b"xGR1348941" + A * 20 + b" ")
add("gitlab-runner-registration-token", "space-before", b" GR1348941" + A * 20 + b" ")

# --- feed_token= ---------------------------------------------------------
add("gitlab-feed-token", "exact+amp", b"?feed_token=" + A * 20 + b"&page=1")
add("gitlab-feed-token", "exact+eos", b"feed_token=" + A * 20)
add("gitlab-feed-token", "exact+underscore", b"feed_token=" + A * 20 + b"_")
add("gitlab-feed-token", "exact+letter", b"feed_token=" + A * 20 + b"Z")
add("gitlab-feed-token", "19chars", b"feed_token=" + A * 19 + b"&")
add("gitlab-feed-token", "21chars", b"feed_token=" + A * 21 + b"&")
add("gitlab-feed-token", "64hex-value", b"feed_token=" + b"a" * 64 + b"&")

# --- gloas- + 64 ---------------------------------------------------------
add("gitlab-oauth-app-secret", "exact+space", b"gloas-" + A * 64 + b" ")
add("gitlab-oauth-app-secret", "exact+eos", b"gloas-" + A * 64)
add("gitlab-oauth-app-secret", "exact+dot", b"gloas-" + A * 64 + b".")
add("gitlab-oauth-app-secret", "63chars", b"gloas-" + A * 63 + b" ")
add("gitlab-oauth-app-secret", "65chars", b"gloas-" + A * 65 + b" ")
add("gitlab-oauth-app-secret", "exact+underscore", b"gloas-" + A * 64 + b"_")

# --- glft- + 20 ----------------------------------------------------------
add("gitlab-feed-token-v2", "exact+space", b"glft-" + A * 20 + b" ")
add("gitlab-feed-token-v2", "exact+eos", b"glft-" + A * 20)
add("gitlab-feed-token-v2", "19chars", b"glft-" + A * 19 + b" ")
add("gitlab-feed-token-v2", "21chars", b"glft-" + A * 21 + b" ")
add("gitlab-feed-token-v2", "knownlimit-64hex", b"glft-" + b"0123456789abcdef" * 4 + b" ")
add("gitlab-feed-token-v2", "prefix-20", b"acme-glft-" + A * 20 + b" ")

# --- glagent- + 50 (boundary is the delicate one) ------------------------
add("gitlab-kubernetes-agent-token", "exact+space", b"glagent-" + A * 50 + b" ")
add("gitlab-kubernetes-agent-token", "exact+eos", b"glagent-" + A * 50)
add("gitlab-kubernetes-agent-token", "exact+dot-eos", b"glagent-" + A * 50 + b".")
add("gitlab-kubernetes-agent-token", "exact+dot-lower", b"glagent-" + A * 50 + b".abc")
add("gitlab-kubernetes-agent-token", "exact+dot-digit", b"glagent-" + A * 50 + b".1")
add("gitlab-kubernetes-agent-token", "exact+dot-upper", b"glagent-" + A * 50 + b".Abc")
add("gitlab-kubernetes-agent-token", "exact+dot-underscore", b"glagent-" + A * 50 + b"._x")
add("gitlab-kubernetes-agent-token", "exact+hyphen", b"glagent-" + A * 50 + b"-")
add("gitlab-kubernetes-agent-token", "exact+underscore", b"glagent-" + A * 50 + b"_")
add("gitlab-kubernetes-agent-token", "exact+letter", b"glagent-" + A * 50 + b"Z")
add("gitlab-kubernetes-agent-token", "exact+slash", b"glagent-" + A * 50 + b"/x")
add("gitlab-kubernetes-agent-token", "49chars", b"glagent-" + A * 49 + b" ")
add("gitlab-kubernetes-agent-token", "51chars", b"glagent-" + A * 51 + b" ")
add("gitlab-kubernetes-agent-token", "prefix-acme", b"acme-glagent-" + A * 50 + b" ")
add("gitlab-kubernetes-agent-token", "prefix-21chars", b"a" * 21 + b"-glagent-" + A * 50 + b" ")
add("gitlab-kubernetes-agent-token", "versioned-50seg", b"glagent-" + A * 50 + b".ab.cd1234567 ")
add("gitlab-kubernetes-agent-token", "versioned-27seg", b"glagent-" + A * 27 + b".ab.cd1234567 ")
add("gitlab-kubernetes-agent-token", "versioned-60seg", b"glagent-" + A * 60 + b".ab.cd1234567 ")

# --- glimt- 20-25 lower-case --------------------------------------------
add("gitlab-incoming-email-token", "20+space", b"glimt-" + b"a" * 20 + b" ")
add("gitlab-incoming-email-token", "22+space", b"glimt-" + b"a" * 22 + b" ")
add("gitlab-incoming-email-token", "25+eos", b"glimt-" + b"a" * 25)
add("gitlab-incoming-email-token", "19+space", b"glimt-" + b"a" * 19 + b" ")
add("gitlab-incoming-email-token", "26+space", b"glimt-" + b"a" * 26 + b" ")
add("gitlab-incoming-email-token", "upper-tail", b"glimt-" + b"E" * 22 + b" ")
add("gitlab-incoming-email-token", "mixed-case-tail", b"glimt-" + b"a" * 21 + b"B ")
add("gitlab-incoming-email-token", "digits-tail", b"glimt-" + b"0123456789" * 2 + b" ")
add("gitlab-incoming-email-token", "prefix-acme", b"acme-glimt-" + b"a" * 22 + b" ")
add("gitlab-incoming-email-token", "prefix-hyphenated", b"my-org-glimt-" + b"a" * 22 + b" ")
add("gitlab-incoming-email-token", "prefix-21chars", b"a" * 21 + b"-glimt-" + b"a" * 22 + b" ")
add("gitlab-incoming-email-token", "25+hyphen", b"glimt-" + b"a" * 25 + b"-")
add("gitlab-incoming-email-token", "25+dot", b"glimt-" + b"a" * 25 + b".x")

# --- glsoat- + 20 --------------------------------------------------------
add("gitlab-scim-oauth-token", "exact+space", b"glsoat-" + A * 20 + b" ")
add("gitlab-scim-oauth-token", "exact+eos", b"glsoat-" + A * 20)
add("gitlab-scim-oauth-token", "19chars", b"glsoat-" + A * 19 + b" ")
add("gitlab-scim-oauth-token", "21chars", b"glsoat-" + A * 21 + b" ")
add("gitlab-scim-oauth-token", "exact+underscore", b"glsoat-" + A * 20 + b"_")

# --- gitlab+deploy-token-<N>:<20>@ --------------------------------------
add("gitlab-deploy-token-in-url", "exact", b"https://gitlab+deploy-token-7:" + A * 20 + b"@gitlab.com")
add("gitlab-deploy-token-in-url", "no-at", b"gitlab+deploy-token-7:" + A * 20 + b"/x")
add("gitlab-deploy-token-in-url", "19chars", b"gitlab+deploy-token-7:" + A * 19 + b"@x")
add("gitlab-deploy-token-in-url", "21chars", b"gitlab+deploy-token-7:" + A * 21 + b"@x")
add("gitlab-deploy-token-in-url", "no-digits", b"gitlab+deploy-token-:" + A * 20 + b"@x")
add("gitlab-deploy-token-in-url", "word-before", b"xgitlab+deploy-token-7:" + A * 20 + b"@x")
add("gitlab-deploy-token-in-url", "slash-before", b"/gitlab+deploy-token-7:" + A * 20 + b"@x")
add("gitlab-deploy-token-in-url", "quote-before", b'"gitlab+deploy-token-7:' + A * 20 + b'@x"')

# --- glffct- + 20 --------------------------------------------------------
add("gitlab-feature-flags-client-token", "exact+space", b"glffct-" + A * 20 + b" ")
add("gitlab-feature-flags-client-token", "exact+eos", b"glffct-" + A * 20)
add("gitlab-feature-flags-client-token", "19chars", b"glffct-" + A * 19 + b" ")
add("gitlab-feature-flags-client-token", "21chars", b"glffct-" + A * 21 + b" ")
add("gitlab-feature-flags-client-token", "prefix-acme", b"acme-glffct-" + A * 20 + b" ")
add("gitlab-feature-flags-client-token", "prefix-21chars", b"a" * 21 + b"-glffct-" + A * 20 + b" ")

# --- glrct- + 20 ---------------------------------------------------------
add("gitlab-runner-controller-token", "exact+space", b"glrct-" + A * 20 + b" ")
add("gitlab-runner-controller-token", "exact+eos", b"glrct-" + A * 20)
add("gitlab-runner-controller-token", "19chars", b"glrct-" + A * 19 + b" ")
add("gitlab-runner-controller-token", "21chars", b"glrct-" + A * 21 + b" ")
add("gitlab-runner-controller-token", "prefix-acme", b"acme-glrct-" + A * 20 + b" ")


def inst_shapes(pats, data):
    out = []
    for name, rx in pats.items():
        if rx.search(data):
            out.append(name)
    return sorted(out)


div = 0
swallow = 0
rows = []
for shape, label, data in CASES:
    s140 = bool(S140[shape].search(data))
    got = inst_shapes(newp, data)
    mine = shape in got
    others = [s for s in got if s != shape]
    same = (s140 == mine)
    if not same:
        div += 1
    if others:
        swallow += 1
    rows.append((shape, label, s140, mine, ",".join(others) or "-", "ok" if same else "DIVERGE"))

print("CASE  shape  label  s140  instrument  other-shapes  verdict")
for shape, label, s140, mine, others, verdict in rows:
    print("%-44s %-18s s140=%-5s inst=%-5s other=%-40s %s"
          % (shape, label, s140, mine, others, verdict))
print("INDEPENDENT-SHAPES cases=%d divergences=%d cross-fire=%d" % (len(rows), div, swallow))

# --- old-shape survival: base vs new pattern name sets -------------------
OLD = {"github-token", "github-refresh-token", "gitlab-pat", "gitlab-jwt-token",
       "gitlab-runner-auth-token", "gitlab-deploy-token", "aws-access-key-id",
       "aws-sts-session-token", "gcs-signed-url-signature", "azure-sas-signature",
       "cloudfront-signed-url-signature", "cloudfront-signed-cookie-signature",
       "gitlab-pat-versioned", "gitlab-pat-routable",
       "gitlab-runner-auth-token-versioned", "gitlab-deploy-token-versioned",
       "gitlab-agent-token-versioned", "gitlab-workspace-token-versioned",
       "gitlab-pipeline-trigger-token"}
lost = sorted(OLD - set(newp))
print("OLD-SHAPES present=%d/%d lost=%s" % (len(OLD) - len(lost), len(OLD), lost or "none"))
print("BASE-SHAPES count=%d NEW-SHAPES count=%d" % (len(basep), len(newp)))
base_new = sorted(set(newp) - set(basep))
print("SHAPES-ADDED %s" % ",".join(base_new))
sys.exit(0 if div == 0 and not lost else 1)
