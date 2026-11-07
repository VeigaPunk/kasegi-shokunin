#!/usr/bin/env python3
"""ReviewWindow r89 probe: does the landed scanner miss documented-shape
Azure/CloudFront signed URLs because of the name class or the 20-param window?

Behavioral classification: every question is answered by running the landed
compiled regex over a fixture, never by re-reading the pattern text.
"""
import hashlib
import importlib.util
import os
import random
import sys

S = os.environ.get("RW_SCRATCH", "/fast/scratch/hyaku/kasegi-r89/ReviewWindow")
FIX = os.path.join(S, "fixtures")
SEED = 8901

spec = importlib.util.spec_from_file_location(
    "landed", os.path.join(S, "capture-secret-scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
PATS = dict(mod.patterns())
AZ = PATS["azure-sas-signature"]
CF = PATS["cloudfront-signed-url-signature"]

rnd = random.Random(SEED)
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
CFB64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~_"


def sig(alphabet, n=44):
    return "".join(rnd.choice(alphabet) for _ in range(n))


AZ_SIG = sig(B64)          # 44 base64 chars, no '='
AZ_SIG_PAD = AZ_SIG[:42] + "%3D%3D"
CF_SIG = "FAKE" + sig(CFB64, 60)
KPI = "K2JCJMDEHXQW5F"     # the doc's published example key pair id (S128 line 13/S130 line 75)
G = ["%08x-1111-2222-3333-444455556666" % rnd.getrandbits(32) for _ in range(6)]
BASE = "https://acct.blob.core.windows.net/sascontainer/blob1.txt"
CFBASE = "https://d111111abcdef8.cloudfront.net/image.jpg"

# Documented Azure SAS query parameter names, from the URI-parameters table of
# https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas
# (fetched 2026-11-07; each name also appears as a standalone line in
# userdeleg.txt at the line noted).
AZ_NAMES = [
    ("sv", 1087), ("sr", 1110), ("st", 1133), ("se", 1158), ("sp", 1183),
    ("sip", 1206), ("spr", 1235), ("skoid", 1258), ("sktid", 1283),
    ("skt", 1306), ("ske", 1333), ("skv", 1360), ("sks", 1385),
    ("saoid", 1408), ("suoid", 1431), ("scid", 1454), ("skdutid", 1477),
    ("sduoid", 1504), ("srh", 1527), ("srq", 1550), ("sdd", 1573),
    ("ses", 1600), ("tn", 1623), ("spk", 1654), ("srk", 1658),
    ("epk", 1695), ("erk", 1699), ("sig", 1728), ("rscc", 1751),
    ("rscd", 1776), ("rsce", 1801), ("rscl", 1826), ("rsct", 1851),
    ("bv", 1941), ("bs", 1957),
]
CF_NAMES = ["Policy", "Signature", "Key-Pair-Id", "Expires", "Hash-Algorithm"]

out = []


def say(*a):
    line = " ".join(str(x) for x in a)
    out.append(line)
    print(line)


def az_hit(b):
    found, _ = mod.scan_bytes(b, mod.patterns())
    return "azure-sas-signature" in {s for s, _ in found}


def cf_hit(b):
    found, _ = mod.scan_bytes(b, mod.patterns())
    return "cloudfront-signed-url-signature" in {s for s, _ in found}


def main():
    os.makedirs(FIX, exist_ok=True)
    say("PROBE seed=%d azsig_chars=%d azsig_pad=yes cfsig_chars=%d" % (SEED, len(AZ_SIG_PAD), len(CF_SIG)))

    # --- 1. name class, behaviorally: one documented name at a time -----------
    say("## AZURE documented-name class: URL = %s?sv=2025-07-05&<NAME>=x&sig=<44>" % BASE)
    az_in, az_out = [], []
    for name, ln in AZ_NAMES:
        if name in ("sv", "sig"):
            continue
        u = ("%s?sv=2025-07-05&%s=x&sig=%s" % (BASE, name, AZ_SIG_PAD)).encode()
        (az_in if az_hit(u) else az_out).append((name, ln))
    say("AZ name-class in: %d %s" % (len(az_in), ",".join(n for n, _ in az_in)))
    say("AZ name-class OUT: %d %s" % (len(az_out), ",".join("%s(doc line %d)" % (n, l) for n, l in az_out)))

    say("## CLOUDFRONT documented-name class: URL = %s?Signature=<60>&<NAME>=x&Key-Pair-Id=%s" % (CFBASE, KPI))
    cf_in, cf_out = [], []
    for name in CF_NAMES:
        if name in ("Signature", "Key-Pair-Id"):
            continue
        u = ("%s?Signature=%s&%s=x&Key-Pair-Id=%s" % (CFBASE, CF_SIG, name, KPI)).encode()
        (cf_in if cf_hit(u) else cf_out).append(name)
    say("CF name-class in: %d %s" % (len(cf_in), ",".join(cf_in)))
    say("CF name-class OUT: %d %s" % (len(cf_out), ",".join(cf_out) or "-"))

    # --- 2. window boundary, all names in class ------------------------------
    pick = [n for n, _ in AZ_NAMES if n not in ("sv", "sig", "skdutid", "tn", "spk", "srk", "epk", "erk")]
    say("## AZURE window: in-class filler names available=%d" % len(pick))
    for k in (19, 20, 21, 22):
        fill = pick[:k]
        u = ("%s?sv=2025-07-05&%s&sig=%s" % (BASE, "&".join("%s=x" % n for n in fill), AZ_SIG_PAD)).encode()
        say("AZ window between=%d hit=%s" % (k, az_hit(u)))
    for k in (19, 20, 21):
        u = ("%s?Signature=%s&%s&Key-Pair-Id=%s" % (
            CFBASE, CF_SIG, "&".join("p%d=x" % i for i in range(k)), KPI)).encode()
        say("CF window between=%d hit=%s" % (k, cf_hit(u)))

    # --- 3. fixtures ---------------------------------------------------------
    fixtures = {}
    fixtures["az_f1_skdutid_min"] = "%s?sv=2025-07-05&sduoid=%s&skdutid=%s&sig=%s" % (BASE, G[0], G[1], AZ_SIG_PAD)
    fixtures["az_f2_control_no_skdutid"] = "%s?sv=2025-07-05&sduoid=%s&sig=%s" % (BASE, G[0], AZ_SIG_PAD)
    fixtures["az_f3_skdutid_alone"] = "%s?sv=2025-07-05&skdutid=%s&sig=%s" % (BASE, G[1], AZ_SIG_PAD)
    fixtures["az_f4_ud_full"] = "%s?sv=2025-07-05&sr=b&st=2025-07-05T00:00:00Z&se=2025-07-06T00:00:00Z&sp=r&spr=https&skoid=%s&sktid=%s&skt=2025-07-05T00:00:00Z&ske=2025-07-06T00:00:00Z&sks=b&skv=2025-07-05&sduoid=%s&skdutid=%s&sig=%s" % (
        BASE, G[0], G[1], G[2], G[3], AZ_SIG_PAD)
    fixtures["az_f4b_ud_full_no_skdutid"] = "%s?sv=2025-07-05&sr=b&st=2025-07-05T00:00:00Z&se=2025-07-06T00:00:00Z&sp=r&spr=https&skoid=%s&sktid=%s&skt=2025-07-05T00:00:00Z&ske=2025-07-06T00:00:00Z&sks=b&skv=2025-07-05&sduoid=%s&sig=%s" % (
        BASE, G[0], G[1], G[2], AZ_SIG_PAD)
    fixtures["az_f5_doc_example_documented_order"] = "sp=rw&sv=2026-04-06&sr=b&srh=foo,bar&srq=operation,identifier&sig=%s&operation=update&identifier=abcd" % AZ_SIG_PAD
    fixtures["az_f6_doc_example_request_params_first"] = "%s?operation=update&identifier=abcd&sp=rw&sv=2026-04-06&sr=b&srh=foo,bar&srq=operation,identifier&sig=%s" % (BASE, AZ_SIG_PAD)
    fixtures["az_f7_skdutid_after_sig"] = "%s?sv=2025-07-05&sig=%s&skdutid=%s" % (BASE, AZ_SIG_PAD, G[1])
    fixtures["cf_f1_canned"] = "%s?color=red&size=medium&Expires=1767290400&Signature=%s&Key-Pair-Id=%s&Hash-Algorithm=SHA256" % (CFBASE, CF_SIG, KPI)
    fixtures["cf_f2_custom"] = "%s?color=red&size=medium&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kLm5ldC8qIn1dfQ__&Signature=%s&Key-Pair-Id=%s" % (CFBASE, CF_SIG, KPI)
    fixtures["cf_f3_kpi_then_sig"] = "%s?Key-Pair-Id=%s&Expires=1767290400&Signature=%s" % (CFBASE, KPI, CF_SIG)

    fixtures["cf_f4_underscore_user_param_between"] = "%s?Signature=%s&_ga=1&Key-Pair-Id=%s" % (CFBASE, CF_SIG, KPI)
    fixtures["cf_f5_dotted_user_param_between"] = "%s?Signature=%s&foo.bar=1&Key-Pair-Id=%s" % (CFBASE, CF_SIG, KPI)
    fixtures["cf_f6_21_user_params_between"] = "%s?Signature=%s&%s&Key-Pair-Id=%s" % (
        CFBASE, CF_SIG, "&".join("p%d=x" % i for i in range(21)), KPI)

    for name, body in fixtures.items():
        p = os.path.join(FIX, name + ".txt")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body + "\n")
    say("## fixtures written=%d dir=%s" % (len(fixtures), FIX))
    for name in sorted(fixtures):
        b = fixtures[name].encode()
        say("FIXTURE %-38s azure=%s cloudfront=%s sha256=%s" % (
            name, az_hit(b), cf_hit(b), hashlib.sha256(b).hexdigest()[:16]))

    # --- 4. counts for the report -------------------------------------------
    say("COUNT az_names_documented=%d az_names_out_of_class=%d az_names_in_class=%d"
        % (len(AZ_NAMES), len(az_out), len(az_in)))
    say("COUNT cf_names_documented=%d cf_names_out_of_class=%d" % (len(CF_NAMES), len(cf_out)))
    say("COUNT az_max_realistic_between_ud_blob=%d" % len(
        ["sr", "st", "se", "sp", "spr", "sip", "skoid", "sktid", "skt", "ske", "sks", "skv",
         "saoid", "suoid", "scid", "sduoid", "skdutid", "srh", "srq", "sdd", "ses",
         "rscc", "rscd", "rsce", "rscl", "rsct", "bv", "bs"]))

    with open(os.path.join(S, "probe-out.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


main()
