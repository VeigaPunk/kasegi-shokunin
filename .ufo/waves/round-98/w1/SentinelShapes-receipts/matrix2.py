#!/usr/bin/env python3
"""Round-98 SentinelShapes matrix v2: nine C2 shapes, S140_A vs S140_B separated.

S140_A = the generated assignment regex GitLab documents for
assignmentContext (MR !151: `<keywordGroup>.{0,8}[:=].{0,8}(<rhs>)`), with
the eight plain rules translated from their published regexes.
S140_B = loose sensitivity bound for the session cookie only: keyword then the
value anywhere on the same line (no operator).  B is NOT the contract.
"""
import importlib.util
import re
import sys
from collections import Counter

LANDING = "/fast/scratch/hyaku/kasegi-r98/SentinelShapes/landing"
spec = importlib.util.spec_from_file_location(
    "landing_scan", LANDING + "/corpus/instruments/capture-secret-scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

NINE = [
    "gitlab-ci-build-token", "gitlab-iam-refresh-token",
    "gitlab-iam-authorization-code", "gitlab-session-cookie",
    "gitlab-runner-registration-token", "gitlab-feed-token",
    "gitlab-oauth-app-secret", "gitlab-feed-token-v2",
    "gitlab-scim-oauth-token",
]
PREF8 = [s for s in NINE if s != "gitlab-session-cookie"]

PUNCT = r"[!-/:-@\[-`{-~]"
SPACE = r"[\t\n\v\f\r ]"
BOUND = r"(?=" + PUNCT + r"|" + SPACE + r"|$)"
LB = r"(?<![0-9A-Za-z_])"

S140_A = {
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
COOKIE_B = re.compile(
    r"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,40}?(?:cell-[0-9]+-)?[0-9a-f]{64}")

HEX64 = "0123456789abcdef" * 4
CI = "glcbt-Ab3_" + "kQ7z-9LmN0pR2sT4uV6w"
IAMR = "gliamrt-" + "A" * 43 + "." + "B" * 43
IAMA = "gliamac-" + "C" * 43 + "." + "D" * 43
REG = "GR1348941" + "E" * 20
FEED = "feed_token=" + "F" * 20
OAUTH = "gloas-" + "G" * 64
FEED2 = "glft-" + "H" * 20
SCIM = "glsoat-" + "I" * 20
TOK = {"gitlab-ci-build-token": CI, "gitlab-iam-refresh-token": IAMR,
       "gitlab-iam-authorization-code": IAMA,
       "gitlab-runner-registration-token": REG, "gitlab-feed-token": FEED,
       "gitlab-oauth-app-secret": OAUTH, "gitlab-feed-token-v2": FEED2,
       "gitlab-scim-oauth-token": SCIM}

SEPS = ["_", "-", ".", ";", "&", "%26", "\\u0026", "&#x26;", " ", "\n", "\t",
        '"', "'", ")", "]", "}", ",", ":", "=", "/", "?", "#", "%", "+", "|",
        "\r\n"]
CONTEXTS = [
    ("bare", lambda t: t),
    ("json", lambda t: '{"token":"%s"}' % t),
    ("header", lambda t: "Authorization: Bearer %s" % t),
    ("query", lambda t: "https://gitlab.example.com/x?token=%s&y=1" % t),
    ("md-cell", lambda t: "| token | %s |" % t),
    ("log", lambda t: "2026-11-07T00:00:00Z INFO token=%s" % t),
    ("git-remote", lambda t: "https://oauth2:%s@gitlab.example.com/x.git" % t),
    ("yaml", lambda t: "token: %s" % t),
]
LEFT = ["", "_", "A", "9", "-", ".", "%26", "\\u0026", "&#x26;", "&#38;",
        '"', "'", "(", "[", "{", "=", ":", "&", ";"]

cases = []


def add(cid, shape, payload, real, note=""):
    cases.append((cid, shape, payload, real, note))


for s, t in TOK.items():
    add("pos-%s" % s, s, t, s, "bare token, EOS")
add("pos-cookie", "gitlab-session-cookie", "_gitlab_session=" + HEX64,
    "gitlab-session-cookie", "cookie assignment")
for s, t in TOK.items():
    for i, sep in enumerate(SEPS):
        add("sep-%s-%02d" % (s, i), s, t + sep + "x", s, "sep=%r" % sep)
for s, t in TOK.items():
    for name, fn in CONTEXTS:
        add("ctx-%s-%s" % (s, name), s, fn(t), s, "context=%s" % name)

# length over/under
add("len-ci-mid0", "gitlab-ci-build-token", "glcbt-_" + "k" * 20, None, "middle 0")
add("len-ci-mid1", "gitlab-ci-build-token", "glcbt-A_" + "k" * 20, "gitlab-ci-build-token", "middle 1")
add("len-ci-mid5", "gitlab-ci-build-token", "glcbt-ABCDE_" + "k" * 20, "gitlab-ci-build-token", "middle 5")
add("len-ci-mid6", "gitlab-ci-build-token", "glcbt-ABCDEF_" + "k" * 20, None, "middle 6")
add("len-ci-tail19", "gitlab-ci-build-token", "glcbt-Ab3_" + "k" * 19 + " ", None, "tail 19")
add("len-ci-tail21", "gitlab-ci-build-token", "glcbt-Ab3_" + "k" * 21 + " ", None, "tail 21")
add("len-iamr-42", "gitlab-iam-refresh-token", "gliamrt-" + "A" * 42 + "." + "B" * 43 + " ", None, "seg1 42")
add("len-iamr-44", "gitlab-iam-refresh-token", "gliamrt-" + "A" * 44 + "." + "B" * 43 + " ", None, "seg1 44")
add("len-iamr-b42", "gitlab-iam-refresh-token", "gliamrt-" + "A" * 43 + "." + "B" * 42 + " ", None, "seg2 42")
add("len-iamr-nodot", "gitlab-iam-refresh-token", "gliamrt-" + "A" * 43 + "B" * 43 + " ", None, "no dot")
add("len-iama-42", "gitlab-iam-authorization-code", "gliamac-" + "C" * 42 + "." + "D" * 43 + " ", None, "seg1 42")
add("len-iama-44", "gitlab-iam-authorization-code", "gliamac-" + "C" * 44 + "." + "D" * 43 + " ", None, "seg1 44")
add("len-reg19", "gitlab-runner-registration-token", "GR1348941" + "E" * 19 + " ", None, "tail 19")
add("len-reg21", "gitlab-runner-registration-token", "GR1348941" + "E" * 21 + " ", None, "tail 21")
add("len-feed19", "gitlab-feed-token", "feed_token=" + "F" * 19 + "&", None, "tail 19")
add("len-feed21", "gitlab-feed-token", "feed_token=" + "F" * 21 + "&", None, "tail 21")
add("len-oauth63", "gitlab-oauth-app-secret", "gloas-" + "G" * 63 + " ", None, "tail 63")
add("len-oauth65", "gitlab-oauth-app-secret", "gloas-" + "G" * 65 + " ", None, "tail 65")
add("len-feed2-19", "gitlab-feed-token-v2", "glft-" + "H" * 19 + " ", None, "tail 19")
add("len-feed2-21", "gitlab-feed-token-v2", "glft-" + "H" * 21 + " ", None, "tail 21")
add("len-scim19", "gitlab-scim-oauth-token", "glsoat-" + "I" * 19 + " ", None, "tail 19")
add("len-scim21", "gitlab-scim-oauth-token", "glsoat-" + "I" * 21 + " ", None, "tail 21")
add("len-cookie63", "gitlab-session-cookie", "_gitlab_session=" + HEX64[:63] + "\n", None, "hex 63")
add("len-cookie65", "gitlab-session-cookie", "_gitlab_session=" + HEX64 + "a\n", None, "hex 65: S140 matches a 64-hex prefix")
add("len-cookie-cell0", "gitlab-session-cookie", "_gitlab_session=cell--" + HEX64 + "\n", "gitlab-session-cookie", "cell-- (gap consumes it)")
add("len-cookie-cell7", "gitlab-session-cookie", "_gitlab_session=cell-7-" + HEX64 + "\n", "gitlab-session-cookie", "cell-7-")
add("len-cookie-cell123", "gitlab-session-cookie", "_gitlab_session=cell-123-" + HEX64 + "\n", "gitlab-session-cookie", "cell-123-")
add("len-cookie-cellabc", "gitlab-session-cookie", "_gitlab_session=cell-abc-" + HEX64 + "\n", None, "cell-abc- (9-char gap, beyond 8)")

# case variants
add("case-ci-upper-prefix", "gitlab-ci-build-token", "GLCBT-Ab3_" + "k" * 20 + " ", None, "prefix upper")
add("case-ci-mixed", "gitlab-ci-build-token", "Glcbt-Ab3_" + "k" * 20 + " ", None, "prefix mixed")
add("case-iamr-upper", "gitlab-iam-refresh-token", "GLIAMRT-" + "A" * 43 + "." + "B" * 43 + " ", None, "prefix upper")
add("case-iama-upper", "gitlab-iam-authorization-code", "GLIAMAC-" + "C" * 43 + "." + "D" * 43 + " ", None, "prefix upper")
add("case-reg-lower", "gitlab-runner-registration-token", "gr1348941" + "E" * 20 + " ", None, "prefix lower")
add("case-feed-upper", "gitlab-feed-token", "FEED_TOKEN=" + "F" * 20 + " ", None, "literal upper")
add("case-oauth-upper", "gitlab-oauth-app-secret", "GLOAS-" + "G" * 64 + " ", None, "prefix upper")
add("case-feed2-upper", "gitlab-feed-token-v2", "GLFT-" + "H" * 20 + " ", None, "prefix upper")
add("case-scim-upper", "gitlab-scim-oauth-token", "GLSOAT-" + "I" * 20 + " ", None, "prefix upper")
add("case-cookie-upperhex", "gitlab-session-cookie", "_gitlab_session=" + HEX64.upper() + "\n", None, "upper-case hex")
add("case-cookie-upperhex-name", "gitlab-session-cookie", "_GITLAB_SESSION=" + HEX64 + "\n", None, "upper-case keyword")

# left boundary variants
for s in ("gitlab-ci-build-token", "gitlab-iam-refresh-token",
          "gitlab-runner-registration-token", "gitlab-oauth-app-secret"):
    t = TOK[s]
    for i, lb in enumerate(LEFT):
        add("lb-%s-%02d" % (s, i), s, lb + t + " ", s, "left=%r" % lb)

# session-cookie contexts
CK = [
    ("cookie-header", "Cookie: _gitlab_session=%s; Path=/\n", "gitlab-session-cookie"),
    ("set-cookie", "Set-Cookie: _gitlab_session=%s; path=/; secure\n", "gitlab-session-cookie"),
    ("json", '{"_gitlab_session":"%s"}', "gitlab-session-cookie"),
    ("line-start", "_gitlab_session=%s\n", "gitlab-session-cookie"),
    ("after-quote", '"_gitlab_session=%s"', "gitlab-session-cookie"),
    ("after-squote", "'_gitlab_session=%s'", "gitlab-session-cookie"),
    ("query", "?foo=1&_gitlab_session=%s&bar=2", "gitlab-session-cookie"),
    ("space-eq", "_gitlab_session = %s\n", "gitlab-session-cookie"),
    ("colon-space", "_gitlab_session: %s\n", "gitlab-session-cookie"),
    ("tab-eq", "_gitlab_session\t=\t%s\n", "gitlab-session-cookie"),
    ("ruby-hash-rocket", "_gitlab_session => %s\n", "gitlab-session-cookie"),
    ("go-declare", "_gitlab_session := %s\n", "gitlab-session-cookie"),
    ("pct20-eq", "_gitlab_session%%20=%%20%s\n", "gitlab-session-cookie"),
    ("pct20-colon", "_gitlab_session%%20:%%20%s\n", "gitlab-session-cookie"),
    ("pct20-after-eq", "_gitlab_session=%%20%s\n", "gitlab-session-cookie"),
    ("geo-eq", "_gitlab_session_geo_%s=%s\n", "gitlab-session-cookie"),
    ("geo-space-eq", "_gitlab_session_geo_%s = %s\n", "gitlab-session-cookie"),
    ("cell-eq", "_gitlab_session=cell-7-%s\n", "gitlab-session-cookie"),
    ("cell-space", "_gitlab_session cell-7-%s\n", "gitlab-session-cookie"),
    ("paren-eq", "_gitlab_session(=%s)\n", "gitlab-session-cookie"),
    ("paren-gap", "_gitlab_session ( = ) %s\n", "gitlab-session-cookie"),
    ("comma-eq", "_gitlab_session,=%s\n", "gitlab-session-cookie"),
    ("pipe-eq", "_gitlab_session|=%s\n", "gitlab-session-cookie"),
    ("plus-eq", "_gitlab_session+=%s\n", "gitlab-session-cookie"),
    ("newline-eq", "_gitlab_session\n=%s\n", "gitlab-session-cookie"),
    ("bare-hex", "%s\n", None),
    ("no-context", "x=%s\n", None),
    ("geo-alone", "_gitlab_session_geo_%s\n", None),
    ("geo-63", "_gitlab_session_geo_%s=%s\n", None),
    ("geo-65", "_gitlab_session_geo_%s=%s\n", None),
    ("word-prefixed", "x_gitlab_session=%s\n", None),
    ("double-underscore", "__gitlab_session=%s\n", None),
    ("hex-then-underscore", "_gitlab_session=%s_x\n", "gitlab-session-cookie"),
    ("hex-then-g", "_gitlab_session=%s g\n", "gitlab-session-cookie"),
    ("hex-then-hex", "_gitlab_session=%s0\n", None),
    ("semi-other-assign", "_gitlab_session; foo=%s\n", None),
    ("space-other-assign", "_gitlab_session x=%s\n", None),
    ("rocket-nospace", "_gitlab_session=> %s\n", "gitlab-session-cookie"),
    ("geo-pct20", "_gitlab_session_geo_%s%%20=%%20%s\n", "gitlab-session-cookie"),
    ("pct20-fully-encoded", "_gitlab_session%%20%%3D%%20%s\n", None),
    ("form-encoded-eq", "_gitlab_session%%3D%s\n", None),
]
for name, fmt, real in CK:
    if name in ("geo-eq", "geo-space-eq", "geo-pct20"):
        payload = fmt % (HEX64, HEX64)
    elif name == "geo-63":
        payload = fmt % (HEX64[:63], HEX64)
    elif name == "geo-65":
        payload = fmt % (HEX64 + "a", HEX64)
    else:
        payload = fmt % HEX64
    add("ck-%s" % name, "gitlab-session-cookie", payload, real, "cookie context=%s" % name)

# scanner boundary negatives / widened positives
add("neg-ci-6prefix", "gitlab-ci-build-token", "glcbt-Ab3cde_" + "k" * 20 + " ", None, "selftest neg")
add("neg-ci-no-underscore", "gitlab-ci-build-token", "glcbt-Ab3" + "k" * 20 + " ", None, "selftest neg")
add("neg-ci-right-alnum", "gitlab-ci-build-token", "glcbt-Ab3_" + "k" * 21, None, "selftest neg")
add("neg-iamr-short", "gitlab-iam-refresh-token", "gliamrt-" + "A" * 42 + "." + "B" * 43 + " ", None, "selftest neg")
add("neg-iama-44", "gitlab-iam-authorization-code", "gliamac-" + "C" * 44 + "." + "D" * 43 + " ", None, "selftest neg")
add("neg-cookie-63", "gitlab-session-cookie", "_gitlab_session=" + HEX64[:63] + "\n", None, "selftest neg")
add("neg-cookie-upper", "gitlab-session-cookie", "_gitlab_session=" + HEX64.upper() + "\n", None, "selftest neg")
add("pos-reg-underscore", "gitlab-runner-registration-token", "GR1348941" + "E" * 20 + "_x", "gitlab-runner-registration-token", "widened positive")
add("pos-reg-hyphen", "gitlab-runner-registration-token", "GR1348941" + "E" * 20 + "-x", "gitlab-runner-registration-token", "widened positive")
add("pos-feed-underscore", "gitlab-feed-token", "feed_token=" + "F" * 20 + "_x", "gitlab-feed-token", "widened positive")
add("pos-oauth-hyphen", "gitlab-oauth-app-secret", "gloas-" + "G" * 64 + "-x", "gitlab-oauth-app-secret", "widened positive")
add("pos-feed2-underscore", "gitlab-feed-token-v2", "glft-" + "H" * 20 + "_x", "gitlab-feed-token-v2", "widened positive")
add("pos-scim-hyphen", "gitlab-scim-oauth-token", "glsoat-" + "I" * 20 + "-x", "gitlab-scim-oauth-token", "widened positive")

# ---- run -------------------------------------------------------------------
def scan9(payload):
    data = payload.encode("utf-8", "surrogateescape")
    return {s for s, _ in mod.scan_bytes(data, mod.GITLAB_PATTERNS)[0]} & set(NINE)


def s140a(payload):
    hits = {s for s, rx in S140_A.items() if rx.search(payload)}
    if COOKIE_A.search(payload):
        hits.add("gitlab-session-cookie")
    return hits


def s140b(payload):
    return {"gitlab-session-cookie"} if COOKIE_B.search(payload) else set()


rows = []
for cid, shape, payload, real, note in cases:
    sc, sa, sb = scan9(payload), s140a(payload), s140b(payload)
    miss_a = sa - sc
    extra = sc - sa
    if miss_a:
        cls = "MUST-FIX" if real in miss_a else "QUAL-S140A-ONLY"
    elif extra:
        cls = "QUAL-SCANNER-ONLY"
    elif sc:
        cls = "AGREE-HIT"
    elif sb - sc:
        cls = "QUAL-MODEL-B"
    else:
        cls = "AGREE-MISS"
    rows.append(dict(cid=cid, shape=shape, payload=payload, real=real, note=note,
                     scan=",".join(sorted(sc)) or "-",
                     s140a=",".join(sorted(sa)) or "-",
                     s140b=",".join(sorted(sb)) or "-", cls=cls))

print("MATRIX cases=%d" % len(rows))
print("CLASSES " + " ".join("%s=%d" % (k, v) for k, v in sorted(Counter(r["cls"] for r in rows).items())))
print()
print("MUST-FIX rows (S140_A hits a full real token, scanner misses):")
for r in [x for x in rows if x["cls"] == "MUST-FIX"]:
    print("  %-26s %-24s scan=%-4s s140A=%-22s %r" % (r["cid"], r["shape"], r["scan"], r["s140a"], r["payload"]))
print()
print("QUAL-S140A-ONLY rows (S140_A hits, scanner misses, no full real token):")
for r in [x for x in rows if x["cls"] == "QUAL-S140A-ONLY"]:
    print("  %-26s %-24s scan=%-4s s140A=%-22s %r" % (r["cid"], r["shape"], r["scan"], r["s140a"], r["payload"]))
print()
print("QUAL-SCANNER-ONLY rows (scanner hits, S140_A misses):")
for r in [x for x in rows if x["cls"] == "QUAL-SCANNER-ONLY"]:
    print("  %-26s %-24s s140A=%-4s scan=%-22s %r" % (r["cid"], r["shape"], r["s140a"], r["scan"], r["payload"]))
print()
print("QUAL-MODEL-B rows (only the loose model B hits):")
for r in [x for x in rows if x["cls"] == "QUAL-MODEL-B"]:
    print("  %-26s %-24s %r" % (r["cid"], r["shape"], r["payload"]))
print()
bad = [r for r in rows if r["cls"] == "AGREE-MISS" and r["real"]]
print("AGREE-MISS with a full real token (both miss; S140's own grammar refuses): %d" % len(bad))
for r in bad:
    print("  %-26s %-24s %r" % (r["cid"], r["shape"], r["payload"]))
print()

# ---- sweeps ----------------------------------------------------------------
ASCII = [chr(c) for c in range(0x00, 0x80)]
SWEEPS = []
def sweep(name, shape, make, real):
    s140only, scanonly, both, neither = [], [], 0, 0
    for c in ASCII:
        p = make(c)
        sc = shape in scan9(p)
        sa = shape in s140a(p)
        if sa and not sc:
            s140only.append(c)
        elif sc and not sa:
            scanonly.append(c)
        elif sc and sa:
            both += 1
        else:
            neither += 1
    SWEEPS.append((name, shape, s140only, scanonly, both, neither))
    return s140only, scanonly

def esc(chars):
    return "".join("\\x%02x" % ord(c) if not (0x20 <= ord(c) < 0x7f) else c for c in chars)

for s in PREF8:
    t = TOK[s]
    sweep("pre-" + s, s, lambda c, t=t: c + t + " ", s)
    sweep("post-" + s, s, lambda c, t=t: t + c, s)

sweep("cookie-sep", "gitlab-session-cookie",
      lambda c: "_gitlab_session" + c + HEX64, "gitlab-session-cookie")
sweep("cookie-gap-before-op", "gitlab-session-cookie",
      lambda c: "_gitlab_session" + c + "=" + HEX64, "gitlab-session-cookie")
sweep("cookie-gap-after-op", "gitlab-session-cookie",
      lambda c: "_gitlab_session=" + c + HEX64, "gitlab-session-cookie")
sweep("cookie-value-right", "gitlab-session-cookie",
      lambda c: "_gitlab_session=" + HEX64 + c, "gitlab-session-cookie")
sweep("cookie-kw-left", "gitlab-session-cookie",
      lambda c: c + "_gitlab_session=" + HEX64, "gitlab-session-cookie")

print("SWEEPS (ASCII 0x00-0x7f), S140_A vs landed scanner:")
for name, shape, so, co, both, neither in SWEEPS:
    print("  %-34s s140A_only=%s" % (name, esc(so) or "-"))
    print("  %-34s scanner_only=%s both=%d neither=%d" % ("", esc(co) or "-", both, neither))
print()
pref_bad = [w for w in SWEEPS if w[0].startswith(("pre-", "post-")) and w[2]]
print("ASSERT prefixed-shape sweeps: S140_A-only cells = %d (expected 0)" % len(pref_bad))
for w in pref_bad:
    print("  FAIL %s s140A_only=%s" % (w[0], esc(w[2])))

with open("/fast/scratch/hyaku/kasegi-r98/SentinelShapes/receipts/matrix.tsv", "w") as fh:
    fh.write("cid\tshape\tclass\tscan\ts140a\ts140b\treal\tnote\tpayload\n")
    for r in rows:
        fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%r\n" % (
            r["cid"], r["shape"], r["cls"], r["scan"], r["s140a"], r["s140b"],
            r["real"] or "-", r["note"], r["payload"]))
with open("/fast/scratch/hyaku/kasegi-r98/SentinelShapes/receipts/sweeps.tsv", "w") as fh:
    fh.write("sweep\tshape\ts140a_only\tscanner_only\tboth\tneither\n")
    for name, shape, so, co, both, neither in SWEEPS:
        fh.write("%s\t%s\t%s\t%s\t%d\t%d\n" % (name, shape, esc(so), esc(co), both, neither))
print()
print("WROTE receipts/matrix.tsv rows=%d and receipts/sweeps.tsv rows=%d" % (len(rows), len(SWEEPS)))
