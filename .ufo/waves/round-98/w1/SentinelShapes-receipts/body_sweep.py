#!/usr/bin/env python3
"""Body-grammar sweep: vary every length field around its published value and
compare the landed scanner with the S140_A translation.  Any cell where
S140_A hits and the scanner misses is a body-grammar divergence (MUST-FIX if
the payload is a real token)."""
import importlib.util
import re

LANDING = "/fast/scratch/hyaku/kasegi-r98/SentinelShapes/landing"
spec = importlib.util.spec_from_file_location(
    "landing_scan", LANDING + "/corpus/instruments/capture-secret-scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

PUNCT = r"[!-/:-@\[-`{-~]"
SPACE = r"[\t\n\v\f\r ]"
BOUND = r"(?=" + PUNCT + r"|" + SPACE + r"|$)"
LB = r"(?<![0-9A-Za-z_])"
RX = {
    "gitlab-ci-build-token": re.compile(
        LB + r"(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20})" + BOUND),
    "gitlab-iam-refresh-token": re.compile(
        LB + r"(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?=[^0-9a-zA-Z_\-]|$)"),
    "gitlab-iam-authorization-code": re.compile(
        LB + r"(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?=[^0-9a-zA-Z_\-]|$)"),
    "gitlab-runner-registration-token": re.compile(
        LB + r"(GR1348941[0-9a-zA-Z_\-]{20})" + BOUND),
    "gitlab-feed-token": re.compile(
        LB + r"(feed_token=[0-9a-zA-Z_\-]{20})" + BOUND),
    "gitlab-oauth-app-secret": re.compile(
        LB + r"(gloas-[0-9a-zA-Z_\-]{64})" + BOUND),
    "gitlab-feed-token-v2": re.compile(
        LB + r"(glft-[0-9a-zA-Z_\-]{20})" + BOUND),
    "gitlab-scim-oauth-token": re.compile(
        LB + r"(glsoat-[0-9a-zA-Z_\-]{20})" + BOUND),
}
COOKIE_A = re.compile(
    r"(?:_gitlab_session(?:_geo_[0-9a-f]{64})?).{0,8}[:=].{0,8}(?:cell-[0-9]+-)?[0-9a-f]{64}")


def scan_hit(payload, shape):
    data = payload.encode("utf-8", "surrogateescape")
    return shape in {s for s, _ in mod.scan_bytes(data, mod.GITLAB_PATTERNS)[0]}


def s140_hit(payload, shape):
    if shape == "gitlab-session-cookie":
        return bool(COOKIE_A.search(payload))
    return bool(RX[shape].search(payload))


def sweep(label, shape, gen, n):
    s140only, scanonly, both, neither = [], [], 0, 0
    for i in range(n):
        p = gen(i)
        sc, sa = scan_hit(p, shape), s140_hit(p, shape)
        if sa and not sc:
            s140only.append(p)
        elif sc and not sa:
            scanonly.append(p)
        elif sc and sa:
            both += 1
        else:
            neither += 1
    print("%-38s s140A_only=%d scanner_only=%d both=%d neither=%d" % (
        label, len(s140only), len(scanonly), both, neither))
    for p in s140only[:6]:
        print("    S140A-ONLY %r" % p)
    for p in scanonly[:6]:
        print("    SCANNER-ONLY %r" % p)


# ci-build: middle 0..7 x tail 0..25
sweep("ci-build middle", "gitlab-ci-build-token",
      lambda i: "glcbt-" + "A" * (i % 8) + "_" + "k" * (i // 8) + " ", 8 * 26)
# IAM: seg1 38..48 x seg2 38..48
sweep("iam-refresh segs", "gitlab-iam-refresh-token",
      lambda i: "gliamrt-" + "A" * (38 + i % 11) + "." + "B" * (38 + i // 11) + " ", 11 * 11)
sweep("iam-auth segs", "gitlab-iam-authorization-code",
      lambda i: "gliamac-" + "C" * (38 + i % 11) + "." + "D" * (38 + i // 11) + " ", 11 * 11)
# fixed-tail shapes: tail 15..25
for shape, head in (("gitlab-runner-registration-token", "GR1348941"),
                    ("gitlab-feed-token", "feed_token="),
                    ("gitlab-feed-token-v2", "glft-"),
                    ("gitlab-scim-oauth-token", "glsoat-")):
    sweep(shape + " tail", shape, lambda i, h=head: h + "E" * (15 + i) + " ", 11)
sweep("oauth tail", "gitlab-oauth-app-secret",
      lambda i: "gloas-" + "G" * (59 + i) + " ", 11)
# session hex length 60..68, with and without cell prefix
sweep("cookie hex len", "gitlab-session-cookie",
      lambda i: "_gitlab_session=" + ("0123456789abcdef" * 5)[:60 + i] + "\n", 9)
sweep("cookie cell hex len", "gitlab-session-cookie",
      lambda i: "_gitlab_session=cell-7-" + ("0123456789abcdef" * 5)[:60 + i] + "\n", 9)
# cell digit count 0..4
sweep("cookie cell digits", "gitlab-session-cookie",
      lambda i: "_gitlab_session=cell-" + "7" * i + "-" + "0123456789abcdef" * 4 + "\n", 5)
# geo suffix hex length 62..66
sweep("cookie geo len", "gitlab-session-cookie",
      lambda i: "_gitlab_session_geo_" + ("0123456789abcdef" * 5)[:62 + i] + "=" + "0123456789abcdef" * 4 + "\n", 5)
