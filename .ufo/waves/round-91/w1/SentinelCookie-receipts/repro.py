#!/usr/bin/env python3
"""Adversarial probe matrix for the landed round-91 capture-secret-scan shapes.

Re-runnable receipt for round-91 seat SentinelCookie. Every fixture value is
synthetic and assembled at run time, so this file holds no credential-shaped
literal. Output: one fixture per probe in --work/fixtures plus a TSV matrix
(PROBE FAMILY FORM REALISM CLASS OBSERVED FIXTURE_SHA256).

usage: python3 -B repro.py --work SCRATCH --scanner /path/to/capture-secret-scan.py
The scanner must be a copy of corpus/instruments/capture-secret-scan.py at
1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70 sitting beside that rev's
claim-package-check.py and capture-secret-allow.tsv.

Synthetic values only, assembled at run time so this file carries no
credential-shaped literal. Writes one fixture per probe, then runs the landed
scanner (a copy of corpus/instruments/capture-secret-scan.py at 1dd0723) with
--files over all of them and prints a TSV matrix.

usage: prober.py --work DIR --scanner PATH
"""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys

# --- synthetic shapes (assembled, never literal) ------------------------------
CF = "SMOKE" + "c" * 55 + "~_"          # 63 chars, [A-Za-z0-9_~-]
AZ = "Q" * 44 + "%2B" + "Z" * 8         # 55 chars, [A-Za-z0-9%+/]
AZB64URL = "A" * 8 + "-" + "B" * 47     # base64url alphabet
KPI = "K2JCJMDEHXQW5F"
SV = "2025-07-05"
DUT = "66666666-7777-8888-9999-000000000000"


def cf(name="CloudFront-Signature", val=CF):
    return name + "=" + val


def azq(pre, params, post=""):
    return "https://acct.blob.core.windows.net/c/b.txt?" + pre + "&".join(params) + post


P = []


def probe(pid, family, form, realism, docs, data):
    P.append(dict(id=pid, family=family, form=form, realism=realism, docs=docs, data=data))


# --- cloudfront signed cookie ------------------------------------------------
probe("cf01", "cf-cookie", "Set-Cookie baseline (doc S134 form)", "high", "contract",
      b"Set-Cookie: " + cf().encode() + b"; Domain=d111111abcdef8.cloudfront.net; Path=/; Secure; HttpOnly")
probe("cf02", "cf-cookie", "HAR name/value object", "high", "documented-limit",
      json.dumps({"name": "CloudFront-Signature", "value": CF}).encode())
probe("cf03", "cf-cookie", "HAR raw Set-Cookie header value", "high", "contract",
      json.dumps({"name": "Set-Cookie", "value": cf() + "; Path=/; Secure"}).encode())
probe("cf04", "cf-cookie", "HAR cookies array (browser HAR 'cookies' view)", "high", "documented-limit",
      json.dumps({"cookies": [{"name": "CloudFront-Key-Pair-Id", "value": KPI},
                              {"name": "CloudFront-Signature", "value": CF}]}).encode())
probe("cf05", "cf-cookie", "name and '=' percent-encoded as %3D", "high", "documented-limit",
      b"CloudFront-Signature%3D" + CF.encode())
probe("cf06", "cf-cookie", "whole Cookie header percent-encoded", "med", "documented-limit",
      b"Cookie%3A%20" + cf().replace("=", "%3D").encode() + b"%3B%20Path%3D%2F")
probe("cf07", "cf-cookie", "quoted cookie value (RFC 6265 cookie-value allows DQUOTE)", "med", "undocumented",
      b'Set-Cookie: CloudFront-Signature="' + CF.encode() + b'"; Path=/')
probe("cf08", "cf-cookie", "OWS around '=' (name = value)", "low", "undocumented",
      b"Set-Cookie: CloudFront-Signature = " + CF.encode())
probe("cf09", "cf-cookie", "';' separator, no space", "high", "contract",
      b"Cookie: CloudFront-Policy=x;CloudFront-Signature=" + CF.encode())
probe("cf10", "cf-cookie", "'; ' separator", "high", "contract",
      b"Cookie: CloudFront-Policy=x; CloudFront-Signature=" + CF.encode())
probe("cf11", "cf-cookie", "real CRLF between Set-Cookie headers", "high", "contract",
      b"Set-Cookie: CloudFront-Policy=x\r\nSet-Cookie: " + cf().encode() + b"\r\n")
probe("cf12", "cf-cookie", "obsolete line fold, continuation space", "low", "undocumented",
      b"Set-Cookie: CloudFront-Policy=x;\r\n " + cf().encode() + b"; Path=/")
probe("cf13", "cf-cookie", "HTML entity for '='", "low", "undocumented",
      b"CloudFront-Signature&#61;" + CF.encode())
probe("cf14", "cf-cookie", "JSON \\u003d for '='", "low", "undocumented",
      b'"CloudFront-Signature\\u003d' + CF.encode() + b'"')
probe("cf15", "cf-cookie", "python bytes repr of a header line", "high", "contract",
      b"b'CloudFront-Signature=" + CF.encode() + b"; Path=/; Secure'")
probe("cf16", "cf-cookie", "curl -b command line", "high", "contract",
      b"curl -b 'CloudFront-Policy=x; " + cf().encode() + b"; CloudFront-Key-Pair-Id=" + KPI.encode() + b"' https://d111111abcdef8.cloudfront.net/x")
probe("cf17", "cf-cookie", "python dict repr of a cookie jar", "high", "undocumented",
      repr({"CloudFront-Policy": "x", "CloudFront-Signature": CF, "CloudFront-Key-Pair-Id": KPI}).encode())
probe("cf18", "cf-cookie", "JS console object repr (name/value)", "med", "undocumented",
      b"{ name: 'CloudFront-Signature', value: '" + CF.encode() + b"' }")
probe("cf19", "cf-cookie", "Netscape cookies.txt jar (tab columns)", "med", "undocumented",
      b"#HttpOnly_d111111abcdef8.cloudfront.net\tFALSE\t/\tTRUE\t0\tCloudFront-Signature\t" + CF.encode())
probe("cf20", "cf-cookie", "JSON \\r\\n join of two Set-Cookie values", "med", "contract",
      b'{"set-cookie":"CloudFront-Policy=x\\r\\n' + cf().encode() + b'; Path=/"}')
probe("cf21", "cf-cookie", "JSON \\n join of two Set-Cookie values", "med", "contract",
      b'{"set-cookie":"CloudFront-Policy=x\\n' + cf().encode() + b'; Path=/"}')
probe("cf22", "cf-cookie", "value 39 chars (one under the floor)", "high", "documented-limit",
      b"Set-Cookie: CloudFront-Signature=" + CF[:39].encode())
probe("cf23", "cf-cookie", "value exactly 40 chars", "high", "contract",
      b"Set-Cookie: CloudFront-Signature=" + CF[:40].encode())
DOCEX = "dtKhpJ3aUYxq" "DIwepczPiDb9NXQ_"   # public AWS doc example, split so this file holds no
                                     # name=value-shaped 12+ char run (contract: no credential-shaped
                                     # literal in the wave dir)
probe("cf24", "cf-cookie", "doc example value (28 chars, S134 line 123)", "high", "claim-negative",
      b"Set-Cookie: " + cf("CloudFront-Signature", DOCEX).encode() + b"; Domain=example.org; Path=/")
probe("cf25", "cf-cookie", "doc prose placeholder (S134 line 40)", "high", "claim-negative",
      cf("CloudFront-Signature", "hashed and signed " "version of the policy statement").encode() + b";")
probe("cf26", "cf-cookie", "lower-case cookie name", "low", "claim-negative",
      b"Set-Cookie: cloudfront-signature=" + CF.encode())
probe("cf27", "cf-cookie", "prefixed name X-CloudFront-Signature", "low", "claim-negative",
      b"Set-Cookie: X-CloudFront-Signature=" + CF.encode())
probe("cf28", "cf-cookie", "value soft-wrapped across lines", "med", "documented-limit",
      b"Set-Cookie: CloudFront-Signature=" + CF[:30].encode() + b"\n" + CF[30:].encode())
probe("cf29", "cf-cookie", "cookie string with attributes first", "low", "contract",
      b"Domain=.cloudfront.net; Path=/; Secure; " + cf().encode())
probe("cf30", "cf-cookie", "XML name/value element", "low", "undocumented",
      b'<cookie name="CloudFront-Signature"><value>' + CF.encode() + b"</value></cookie>")

# --- azure sas window --------------------------------------------------------
probe("az01", "azure-sas", "sv..skdutid..sig baseline", "high", "contract",
      azq("", ["sv=" + SV, "skdutid=" + DUT, "sr=b", "sp=r", "sig=" + AZ]).encode())
probe("az02", "azure-sas", "sig before sv, skdutid between", "high", "contract",
      azq("", ["sig=" + AZ, "skdutid=" + DUT, "sv=" + SV]).encode())
LET = "abcdefghijklmnopqrstuvwxyz"
NAMES = ["p" + LET[i // 26] + LET[i % 26] for i in range(25)]


def named(names):
    return [nm + "=v" for nm in names]


def window(n):
    return azq("", ["sv=" + SV] + named(NAMES[:n]) + ["skdutid=x", "sig=" + AZ]).encode()


probe("az03", "azure-sas", "20 parameters between sv and sig (exact window bound)", "med", "contract",
      window(19))
probe("az04", "azure-sas", "21 parameters between sv and sig (one over)", "low", "documented-limit",
      window(20))
probe("az05", "azure-sas", "mixed-case parameter names", "med", "contract",
      azq("", ["SV=" + SV, "SkDuTiD=" + DUT, "SIG=" + AZ]).encode())
probe("az06", "azure-sas", "whole query joined by %26", "med", "documented-limit",
      ("https://a.blob.core.windows.net/c/b.txt?a=1%26sv=" + SV + "%26skdutid=x%26sig=" + AZ).encode())
probe("az07", "azure-sas", "%26 between sv and sig only", "low", "documented-limit",
      ("https://a.blob.core.windows.net/c/b.txt?sv=" + SV + "%26skdutid=x%26sig=" + AZ).encode())
probe("az08", "azure-sas", "HTML &amp; separators", "high", "contract",
      ("https://a.blob.core.windows.net/c/b.txt?sv=" + SV + "&amp;skdutid=x&amp;sr=b&amp;sig=" + AZ).encode())
probe("az09", "azure-sas", "HTML numeric entity &#38; separators", "low", "undocumented",
      ("https://a.blob.core.windows.net/c/b.txt?sv=" + SV + "&#38;skdutid=x&#38;sig=" + AZ).encode())
probe("az10", "azure-sas", "8-letter parameter between sv and sig", "low", "documented-limit",
      azq("", ["sv=" + SV, "abcdefgh=1", "sig=" + AZ]).encode())
probe("az11", "azure-sas", "8-letter name after skdutid", "low", "documented-limit",
      azq("", ["sv=" + SV, "skdutid=x", "abcdefgh=1", "sig=" + AZ]).encode())
probe("az12", "azure-sas", "base64url sig ('-' at offset 8)", "low", "undocumented",
      azq("", ["sv=" + SV, "sig=" + AZB64URL]).encode())
probe("az13", "azure-sas", "base64url sig ('-' after 60 chars)", "low", "undocumented",
      azq("", ["sv=" + SV, "sig=" + "A" * 60 + "-" + "B" * 8]).encode())
probe("az14", "azure-sas", "sig 39 chars", "high", "documented-limit",
      azq("", ["sv=" + SV, "sig=" + AZ[:39]]).encode())
probe("az15", "azure-sas", "empty parameter between (&&)", "low", "undocumented",
      ("https://a.blob.core.windows.net/c/b.txt?sv=" + SV + "&&sig=" + AZ).encode())
probe("az16", "azure-sas", "semicolon-separated SAS token", "low", "undocumented",
      ("sv=" + SV + ";skdutid=x;sig=" + AZ).encode())
probe("az17", "azure-sas", "python dict repr of query params", "med", "undocumented",
      repr({"sv": SV, "skdutid": "x", "sig": AZ}).encode())
probe("az18", "azure-sas", "realistic full SAS, skdutid last before sig", "high", "contract",
      azq("", ["sp=rw", "st=2026-11-07T00:00:00Z", "se=2026-11-08T00:00:00Z", "spr=https",
               "sv=" + SV, "sr=b", "skoid=11111111-2222-3333-4444-555555555555",
               "sktid=66666666-7777-8888-9999-000000000000", "sks=b", "skv=" + SV,
               "sduoid=" + DUT, "skdutid=" + DUT, "sig=" + AZ]).encode())
probe("az19", "azure-sas", "sig with %2B/%2F/%3D encoding", "high", "contract",
      azq("", ["sv=" + SV, "sig=" + "R" * 20 + "%2B%2F" + "S" * 20 + "%3D"]).encode())
probe("az20", "azure-sas", "JSON \\u0026 separators, sig last", "high", "contract",
      ('"https://a.blob.core.windows.net/c/b.txt?sv=' + SV + '\\u0026skdutid=x\\u0026sig=' + AZ + '"').encode())


probe("cf31", "cf-cookie", "JSON \\u0026 separator before the pair", "med", "contract",
      b'{"cookie":"CloudFront-Key-Pair-Id=' + KPI.encode() + b'\\u0026' + cf().encode() + b'"}')
probe("cf32", "cf-cookie", "%26 separator before the pair", "med", "contract",
      b"Cookie=CloudFront-Key-Pair-Id%3DK2JCJMDEHXQW5F%26" + cf().encode())
probe("cf33", "cf-cookie", "raw CRLF inside a JSON string value", "med", "contract",
      b'{"set-cookie":"CloudFront-Policy=x\r\n' + cf().encode() + b'; Path=/"}')
probe("cf34", "cf-cookie", "whole capture base64-wrapped", "low", "documented-limit",
      base64.b64encode(b"Set-Cookie: " + cf().encode() + b"; Path=/"))
probe("cf35", "cf-cookie", "mitmproxy-style request dump block", "med", "contract",
      b"GET /x HTTP/1.1\r\nHost: d111111abcdef8.cloudfront.net\r\nCookie: CloudFront-Policy=x; "
      + cf().encode() + b"\r\n\r\n")
probe("cf36", "cf-cookie", "value followed by a comma (comma-joined cookies)", "low", "contract",
      b"Cookie: " + cf().encode() + b", CloudFront-Key-Pair-Id=" + KPI.encode())

probe("az21", "azure-sas", "19 params then skdutid (last inside the window)", "med", "contract",
      azq("", ["sv=" + SV] + named(NAMES[:18]) + ["skdutid=x", "sig=" + AZ]).encode())
probe("az22", "azure-sas", "hyphenated name between sv and sig", "low", "undocumented",
      azq("", ["sv=" + SV, "x-ms-version=2020-10-02", "sig=" + AZ]).encode())
probe("az23", "azure-sas", "digit in a name between sv and sig", "low", "undocumented",
      azq("", ["sv=" + SV, "sp1=r", "sig=" + AZ]).encode())
probe("az24", "azure-sas", "parse_qs-style dict repr of the query", "high", "undocumented",
      repr({"sv": [SV], "skdutid": ["x"], "sig": [AZ]}).encode())
probe("az26", "azure-sas", "sig with raw '+' and '/' (unencoded base64)", "med", "contract",
      azq("", ["sv=" + SV, "sig=" + "R" * 20 + "+/" + "S" * 20]).encode())
probe("az27", "azure-sas", "sig ending in %3D%3D padding", "high", "contract",
      azq("", ["sv=" + SV, "sig=" + "T" * 44 + "%3D%3D"]).encode())
probe("cf40", "cf-cookie", "UTF-16LE encoded capture", "low", "documented-limit",
      ("Set-Cookie: " + cf() + "; Path=/").encode("utf-16-le"))
probe("cf41", "cf-cookie", "gzip-wrapped capture", "low", "documented-limit",
      __import__("gzip").compress(b"Set-Cookie: " + cf().encode() + b"; Path=/"))
probe("cf42", "cf-cookie", "selenium get_cookies() list of name/value dicts", "high", "documented-limit",
      repr([{"name": "CloudFront-Signature", "value": CF, "domain": ".cloudfront.net"}]).encode())
probe("az28", "azure-sas", "bare sig with no sv anywhere (shape design boundary)", "med", "claim-negative",
      ("sig=" + AZ).encode())
probe("az25", "azure-sas", "YAML block of query params", "med", "undocumented",
      ("sv: " + SV + "\nskdutid: x\nsig: " + AZ + "\n").encode())


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--scanner", required=True)
    a = ap.parse_args(argv)
    fx = os.path.join(a.work, "fixtures")
    os.makedirs(fx, exist_ok=True)
    paths = []
    for p in P:
        fp = os.path.join(fx, p["id"] + ".bin")
        with open(fp, "wb") as fh:
            fh.write(p["data"])
        p["path"] = fp
        p["sha"] = hashlib.sha256(p["data"]).hexdigest()
        paths.append(fp)
    proc = subprocess.run([sys.executable, "-B", a.scanner, "--files"] + paths,
                          capture_output=True)
    out = proc.stdout.decode()
    hits = {}
    for line in out.splitlines():
        if line.startswith("HIT "):
            f = dict(kv.split("=", 1) for kv in line.split()[1:])
            pid = os.path.basename(f["path"])[:-4]
            hits.setdefault(pid, []).append(f["shape"])
        else:
            print(line)
    print("scanner rc=%d" % proc.returncode)
    print("PROBE\tFAMILY\tFORM\tREALISM\tDOCS\tOBSERVED\tFIXTURE_SHA256")
    for p in P:
        got = ",".join(sorted(set(hits.get(p["id"], [])))) or "none"
        print("\t".join([p["id"], p["family"], p["form"], p["realism"], p["docs"], got, p["sha"]]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
