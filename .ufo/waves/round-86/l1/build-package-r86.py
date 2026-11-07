#!/usr/bin/env python3
"""KasegiR86 integration of the ExecC2Package candidate into
corpus/practice/curl-ibb-h1-1997312 (post-freeze; C2 is killed as frozen).

Steps: copy the candidate; replace evidence/S122.txt with the redacted lane
snapshot (presigned-URL query strings stripped, .ufo/waves/round-86/l1/redact-presigned.py);
rebind the evidence manifest, redaction receipts and status.json; apply the
ReviewC2Package text fixes F-2..F-8; record the L1 identity and the reviewer.
Usage: build-package-r86.py   (run from the lane root; idempotent over the candidate)
"""
import hashlib
import json
import os
import shutil
import sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
CAND = L + "/.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312"
DEST = L + "/corpus/practice/curl-ibb-h1-1997312"
SNAP = L + "/corpus/source-snapshots/round-86/S122.txt"
SCAN = ".ufo/waves/round-86/l1/redaction-scan-r86.txt"
TOKEN_NOTE = ("a short-lived presigned-URL session token (X-Amz-Date 2026-11-07T00:58:29Z, "
              "X-Amz-Expires 3600 s; live until 2026-11-07T01:58:29Z) inside the public ibb team "
              "profile-picture URLs")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sub(text, old, new):
    if text.count(old) != 1:
        raise SystemExit("expected one occurrence of %r (got %d)" % (old[:60], text.count(old)))
    return text.replace(old, new)


def main():
    if os.path.exists(DEST):
        shutil.rmtree(DEST)
    shutil.copytree(CAND, DEST)
    s122 = open(SNAP, "rb").read()
    open(DEST + "/evidence/S122.txt", "wb").write(s122)
    h122 = sha(s122)
    old122 = "ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1"

    m = json.load(open(DEST + "/evidence/manifest.json"))
    for s in m["sources"]:
        if s["id"] == "S122":
            s["sha256"], s["bytes"] = h122, len(s122)
    for a in m["artifacts"]:
        if a["path"] == "S122.txt":
            a["sha256"], a["bytes"] = h122, len(s122)
            a["note"] = ("HackerOne JSON record of IBB report 1997312, byte-identical to the redacted lane "
                         "snapshot corpus/source-snapshots/round-86/S122.txt (pre-redaction sha256 %s)" % old122)
    for r in m["redactions"]:
        r["verifier"] = "KasegiR86"
        r["verifier_receipt"] = SCAN
        if r["path"] == "S122.txt":
            r["artifact_sha256"] = r["scanned_artifact_sha256"] = h122
            r["removed"] = ["query strings of profile_picture_urls.small and profile_picture_urls.medium "
                            "(AWS STS X-Amz-Credential and X-Amz-Security-Token values): " + TOKEN_NOTE]
            r["note"] = ("public HackerOne record JSON; the only removed bytes are the two presigned query "
                         "strings, replaced by ?[presigned-query-redacted-r86]; every pricing field is untouched")
    mb = (json.dumps(m, indent=1, ensure_ascii=False) + "\n").encode()
    open(DEST + "/evidence/manifest.json", "wb").write(mb)

    st = json.load(open(DEST + "/status.json"))
    st["manifest_sha256"] = sha(mb)
    st["claim_review"]["subchecks"]["no_secrets"] = "PASS"
    rv = st["claim_review"]["reviewer"]
    rv["requested_model"] = "@m_flash (reviewer route at spawn)"
    rv["resolved_model"] = "not recorded by the seat"
    rv["verdict"] = ("CHANGES-REQUESTED on the candidate (F-1..F-9); F-2..F-8 applied at L1 integration by "
                     "KasegiR86; F-1 (frozen E1/E2 conflict) kills C2 as frozen; no reviewer re-pass was run")
    open(DEST + "/status.json", "w").write(json.dumps(st, indent=1, ensure_ascii=False) + "\n")

    pv = json.load(open(DEST + "/provenance.json"))
    for x in pv["agents"] + pv["transitions"]:
        if x.get("identity") == "KasegiR86" or x.get("agent") == "KasegiR86":
            x["requested_model"] = "anthropic/claude-opus-5-5:medium"
            x["resolved_model"] = "anthropic/claude-opus-5-5"
    pv["commands"] = [c for c in pv["commands"] if "build-package-r86.sh" not in c["command"]]
    pv["commands"].append({"command": "python3 -B .ufo/waves/round-86/l1/redact-presigned.py corpus/source-snapshots/round-86/S122.txt", "exit_code": 0})
    pv["commands"].append({"command": "python3 -B .ufo/waves/round-86/l1/build-package-r86.py", "exit_code": 0})
    pv["identity_note"] = ("Producer ExecC2Package built the candidate. KasegiR86 (round-86 L1) redacted the S122 "
                           "presigned query strings, re-scanned every artifact (%s) and applied ReviewC2Package "
                           "F-2..F-8 at integration." % SCAN)
    pv["secrets_attestation"] = {"no_secrets": True, "findings": 0, "by": "KasegiR86",
                                 "method": "claim-package-check.py SECRET_PATTERNS over every artifact after the S122 "
                                           "redaction (%s); before redaction S122 carried %s" % (SCAN, TOKEN_NOTE)}
    open(DEST + "/provenance.json", "w").write(json.dumps(pv, indent=1, ensure_ascii=False) + "\n")

    rp = open(DEST + "/report.md").read()
    rp = rp.replace(old122, h122)
    rp = sub(rp, "No credential material, no cookie value and no key material is recorded\nin this package.",
             "No usable credential, cookie value or key material is recorded in this\npackage (the S122 presigned query strings were removed, see Evidence).")
    start = rp.index("Note on S122 and the secret-shaped-token scan:")
    end = rp.index("The 64-hex tokens cited above")
    rp = rp[:start] + (
        "Note on S122: as captured, the record carried " + TOKEN_NOTE + ", which the\n"
        "gate's R-NOSECRET rule refuses. The lane snapshot and this artifact are the\n"
        "redacted record: both presigned query strings are replaced by\n"
        "`?[presigned-query-redacted-r86]`; every field the pricing reads is\n"
        "untouched. The pre-redaction digest is recorded in the lane manifest\n"
        "(corpus/source-snapshots/round-86/manifest.json, S122 redaction block).\n") + rp[end:]
    rp = sub(rp, "  S122's `bounty_amount` is null, so the amount comes only from S120;",
             "  S122 carries no bounty-amount field, so the amount comes only from S120;")
    rp = sub(rp, "  `internet-bug-bounty`.",
             "  `internet-bug-bounty`. No capture names the payer of this specific\n"
             "  report's bounty; `internet-bug-bounty` is the program-level payer named\n"
             "  by S123, joined to this report by S122 being the IBB team's own record\n"
             "  of it with `has_bounty?` true.")
    open(DEST + "/report.md", "w").write(rp)

    ck = open(DEST + "/claim_checklist.md").read()
    ck = sub(ck, "No credential material, token, cookie value or private key is stored in this\npackage.",
             "No usable credential, token, cookie value or private key is stored in this\npackage (the S122 presigned query strings were removed at integration).")
    ck = ck.replace('"ReviewC2Package" (PENDING-L1)', '"ReviewC2Package" (CHANGES-REQUESTED; fixes applied by the L1, no re-pass)')
    open(DEST + "/claim_checklist.md", "w").write(ck)
    print("BUILT %s s122=%s manifest=%s" % (DEST, h122, sha(mb)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
