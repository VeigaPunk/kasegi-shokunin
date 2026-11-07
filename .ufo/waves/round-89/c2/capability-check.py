#!/usr/bin/env python3
"""kasegi round-89 C2 counter (successor of round 88's): capability `capture-secret-scan`
gains the Amazon CloudFront signed-URL shape and detects Azure SAS signatures after a
JSON-escaped separator in any parameter position, measured at one revision.

Usage:
  python3 capability-check.py --lane LANE --rev REV --work DIR \
      [--instrument-sha256 HEX] [--gate-sha256 HEX] [--seed N]

Every limb reads committed bytes at REV (git show), never the working tree. The
instrument under test is the lane's corpus/instruments/capture-secret-scan.py at
REV, run from a scratch copy beside REV's claim-package-check.py and
capture-secret-allow.tsv (the instrument imports the gate's SECRET_PATTERNS from
its own directory and reads the allowlist from there by default).

Limbs (all must hold; one LIMB line each, then the verdict line):
  K1 instrument  the three instrument files exist at REV; capture-secret-scan.py
                 sha256 == --instrument-sha256 and claim-package-check.py sha256
                 == --gate-sha256 (when given); `--selftest` exits 0 and prints
                 `SELFTEST-RESULT pass`.
  K2 history     run on --rev HISTORY_REV (round-86 freeze 252df0c9, which pushed
                 the S122 STS token): exit 1, and the set of paths with a
                 `HIT shape=aws-sts-session-token` line equals the ORACLE set
                 (`git grep -l -E ORACLE_RE` over HISTORY_REV), which must itself
                 equal HISTORY_EXPECTED.
  K3 clean       run on --rev REV with REV's allowlist: exit 0, hits=0,
                 unused_allow=0 (no stale allowlist row), allowed>=1.
  K4 planted     a scratch git repository with planted files (built here, not by
                 the instrument): the HIT (path, shape) set equals PLANT_EXPECT
                 exactly (round 89 adds CloudFront canned/custom/JSON-escaped/
                 HTML-escaped signed URLs, the Azure SAS in S127 line 605's
                 parameter order JSON-escaped, and look-alike negatives); an
                 allowlist holding an aws-sts-session-token row makes the
                 instrument exit 2; `--files` over three planted working-tree
                 files (one Azure SAS, one CloudFront URL, one documentation
                 placeholder) exits 1 with exactly the two expected hits.
  K5 table       SCORECARD.md at REV has exactly one `## Capabilities` table row
                 whose first cell is `capture-secret-scan`; its last cell is `87`
                 and the row names `cloudfront-signed-url-signature`,
                 `gcs-signed-url-signature`, `azure-sas-signature` and
                 `corpus/practice/*/evidence/`.
  K6 discrim     the BASE instrument (corpus/instruments/capture-secret-scan.py
                 at BASE_REV, the round-89 base, run beside BASE_REV's gate) over
                 the same planted repository finds NONE of NEW_EXPECT (the round-89
                 additions to PLANT_EXPECT) and only PLANT_EXPECT members.
  K7 generated   (round 89, r88 CriticClaims D4) a second scratch repository whose
                 signature, key-pair-id and SAS values are drawn at run time from
                 `random.Random(seed)` (seed = --seed, default from os.urandom; the
                 seed is printed): every positive plant is found with its shape and
                 every generated negative (same values, companion parameter
                 removed or name lower-cased) is not; a detector keyed on the
                 fixture literals of K4 fails here.
  K8 clauses     (round 89, lesson M88-2) every clause of the frozen C2 statement
                 named in CLAUSES maps to one K4 plant in the position its source
                 documents, and that (path, shape) is in K4's hit set (positive
                 clauses) or absent from it (negative clauses).

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read error.
"""
import argparse
import base64
import hashlib
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile

HISTORY_REV = "252df0c90c066d83d229e3107811a6bc05e8feed"
HISTORY_EXPECTED = frozenset({
    ".ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json",
    "corpus/source-snapshots/round-86/S122.txt",
})
ORACLE_RE = r"X-Amz-Security-Token=[A-Za-z0-9%/+=_-]{20,}"
BASE_REV = "090a46f89932324787e00ca20b1007f893934c9a"
FILES = ("capture-secret-scan.py", "claim-package-check.py", "capture-secret-allow.tsv")
HIT = re.compile(r"^HIT shape=(\S+) path=(\S+) line=\d+$")
SUMMARY = re.compile(r"^CAPTURE-SECRET-SCAN mode=\S+ scanned=(\d+) hits=(\d+) files=(\d+) allowed=(\d+) unused_allow=(\d+) rc=(\d+)$")
CF = "cloudfront-signed-url-signature"
AZ = "azure-sas-signature"

TOKEN = "IQoJb3JpZ2luX2VjPLANTEDFIXTURESESSIONTOKEN0123456789abcdefABCDEFxyz"
GSIG = "fedcba9876543210" * 8
ASIG = "PLANTEDsasSIGNATUREfixture0123456789abcdefAB%3D"
CFSIG = "PLANTEDcfSIGNATURE~fixture-0123456789_abcdefABCDEF~ghijklmnopqrstuvwxyzQRS"
KPI = "K2PLANTEDFIXT9"
PLANTS = {
    "corpus/source-snapshots/round-1/S001.txt":
        '{"u":"https://b.s3.amazonaws.com/p.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAPLANTEDFIXTURE01%%2F20261107%%2Fus-west-2%%2Fs3%%2Faws4_request&X-Amz-Security-Token=%s&X-Amz-Signature=00"}\n' % TOKEN,
    "w/x-receipts/live-a.json": '{"k":"ASIAZZZZYYYYXXXXWWWW"}\n',
    "w/live-b.html": "<pre>-----BEGIN RSA PRIVATE KEY-----</pre>\n",
    "w/y-receipts/fp.json": '{"token": "authorization-envelope.json"}\n',
    "w/y-receipts/fp-other.json": '{"token": "authorization-envelope2.json"}\n',
    "corpus/knowledge/k.md": "X-Amz-Security-Token=%s\n" % TOKEN,
    "corpus/source-snapshots/round-1/S002.txt": '{"u":"https://b.s3.amazonaws.com/p.png?[presigned-query-redacted-r86]"}\n',
    "corpus/source-snapshots/round-1/S003.txt": "X-Amz-Credential=AKIAIOSFODNN7EXAMPLE/20220830/us-east-1/ec2/aws4_request&\n",
    "corpus/source-snapshots/round-1/S004.txt":
        "https://storage.googleapis.com/b/o.png?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=svc%%40p.iam.gserviceaccount.com%%2F20261107%%2Fauto%%2Fstorage%%2Fgoog4_request&X-Goog-Date=20261107T000000Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=%s\n" % GSIG,
    "corpus/source-snapshots/round-1/S005.txt":
        "X-Goog-SignedHeaders=host&X-Goog-Signature=247a2aa45f16\n9edf4d187d54e7cc46e4731b1e6273242c4f4c39a1d2507a0e58706e25e3a85a7dbb891d62afa849\n",
    "corpus/source-snapshots/round-1/S006.txt":
        "https://myaccount.blob.core.windows.net/sascontainer/blob1.txt?sp=rw&spr=https&sv=2022-11-02&sr=b&sig=<signature>\n",
    "corpus/source-snapshots/round-1/S007.txt": "https://example.com/x?id=1&sig=%s\n" % ASIG,
    "corpus/practice/p/evidence/E1.txt":
        "https://a.blob.core.windows.net/c/b.txt?sp=r&se=2026-11-08T00:00:00Z&spr=https&sv=2022-11-02&sr=b&sig=%s\n" % ASIG,
    "corpus/practice/p/evidence/E2.json": '{"u":"https://b.s3.amazonaws.com/p.png?X-Amz-Security-Token=%s"}\n' % TOKEN,
    "corpus/practice/p/report.md": "https://a.blob.core.windows.net/c/b.txt?sv=2022-11-02&sig=%s\n" % ASIG,
    "w/z-receipts/live-c.json": '{"url":"https://a.blob.core.windows.net/c/b.txt?sig=%s\\u0026sv=2022-11-02"}\n' % ASIG,
    # round 89 plants
    "corpus/source-snapshots/round-1/S008.txt":
        "https://d111111abcdef8.cloudfront.net/image.jpg?color=red&size=medium&Expires=1767290400&Signature=%s&Key-Pair-Id=%s&Hash-Algorithm=SHA256\n" % (CFSIG, KPI),
    "corpus/source-snapshots/round-1/S009.txt":
        "https://d111111abcdef8.cloudfront.net/image.jpg?color=red&size=medium&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMTExMTExYWJjZGVmOC5jbG91ZGZyb250Lm5ldC8qIn1dfQ__&Signature=%s&Key-Pair-Id=%s\n" % (CFSIG, KPI),
    "w/q-receipts/live-d.json":
        '{"url":"https://d1.cloudfront.net/v.mp4?Key-Pair-Id=%s\\u0026Expires=1767290400\\u0026Signature=%s"}\n' % (KPI, CFSIG),
    "w/live-e.html":
        '<a href="https://d1.cloudfront.net/v.mp4?Expires=1767290400&amp;Signature=%s&amp;Key-Pair-Id=%s">v</a>\n' % (CFSIG, KPI),
    "corpus/practice/p/evidence/E3.json":
        '{"u":"https://myaccount.blob.core.windows.net/sascontainer/blob1.txt?sp=rw\\u0026st=2026-11-07T00:00:00Z\\u0026se=2026-11-08T00:00:00Z\\u0026spr=https\\u0026sv=2022-11-02\\u0026sr=b\\u0026sig=%s"}\n' % ASIG,
    "corpus/source-snapshots/round-1/S010.txt":
        "5. &Signature=hashed and signed version of the policy statement\n6. &Key-Pair-Id=public key ID for the CloudFront public key\n",
    "corpus/source-snapshots/round-1/S011.txt":
        "https://b.s3.amazonaws.com/p.png?X-Amz-Signature=%s&Key-Pair-Id=%s\n" % ("ab" * 32, KPI),
    "corpus/source-snapshots/round-1/S012.txt":
        "https://d1.cloudfront.net/v.mp4?Expires=1767290400&Signature=%s\n" % CFSIG,
    "corpus/source-snapshots/round-1/S013.txt":
        "https://d1.cloudfront.net/v.mp4?Signature=abcDEF123~-_&Key-Pair-Id=%s\n" % KPI,
    "corpus/practice/p/report2.md":
        "https://d1.cloudfront.net/v.mp4?Expires=1767290400&Signature=%s&Key-Pair-Id=%s\n" % (CFSIG, KPI),
}
PLANT_EXPECT = frozenset({
    ("corpus/source-snapshots/round-1/S001.txt", "aws-sts-session-token"),
    ("corpus/source-snapshots/round-1/S001.txt", "aws-access-key-id"),
    ("corpus/source-snapshots/round-1/S001.txt", "credential"),
    ("w/x-receipts/live-a.json", "aws-access-key-id"),
    ("w/live-b.html", "private-key"),
    ("w/y-receipts/fp-other.json", "credential"),
    ("corpus/source-snapshots/round-1/S004.txt", "gcs-signed-url-signature"),
    ("corpus/practice/p/evidence/E1.txt", AZ),
    ("corpus/practice/p/evidence/E2.json", "aws-sts-session-token"),
    ("corpus/practice/p/evidence/E2.json", "credential"),
    ("w/z-receipts/live-c.json", AZ),
})
NEW_EXPECT = frozenset({
    ("corpus/source-snapshots/round-1/S008.txt", CF),
    ("corpus/source-snapshots/round-1/S009.txt", CF),
    ("w/q-receipts/live-d.json", CF),
    ("w/live-e.html", CF),
    ("corpus/practice/p/evidence/E3.json", AZ),
})
PLANT_EXPECT = PLANT_EXPECT | NEW_EXPECT
FP_MATCH = b'token": "authorization-envelope'
# clause of the frozen C2 statement -> (plant path, shape, expected present)
CLAUSES = {
    "cf: Signature then Key-Pair-Id, canned policy (S128 line 13 order)": ("corpus/source-snapshots/round-1/S008.txt", CF, True),
    "cf: Policy, Signature, Key-Pair-Id, custom policy (S130 line 14 order)": ("corpus/source-snapshots/round-1/S009.txt", CF, True),
    "cf: either order, \\u0026 separator (Key-Pair-Id first, JSON-escaped)": ("w/q-receipts/live-d.json", CF, True),
    "cf: &amp; separator": ("w/live-e.html", CF, True),
    "cf: documentation placeholder is not a hit (S128 lines 70-74)": ("corpus/source-snapshots/round-1/S010.txt", CF, False),
    "cf: X-Amz-Signature beside Key-Pair-Id never starts a match": ("corpus/source-snapshots/round-1/S011.txt", CF, False),
    "cf: Signature without Key-Pair-Id is not a hit": ("corpus/source-snapshots/round-1/S012.txt", CF, False),
    "cf: 40-character floor": ("corpus/source-snapshots/round-1/S013.txt", CF, False),
    "cf: capture scope only (practice report is not a capture)": ("corpus/practice/p/report2.md", CF, False),
    "azure: \\u0026 separator, sv sixth (S127 line 605 order), JSON-escaped": ("corpus/practice/p/evidence/E3.json", AZ, True),
}
URLSAFE = string.ascii_letters + string.digits + "-_~"
UPPER = string.ascii_uppercase + string.digits


def git(lane, *args, **kw):
    return subprocess.run(["git", "-C", lane] + list(args), capture_output=True, check=True, **kw).stdout


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_instr(d, *args):
    p = subprocess.run([sys.executable, "-B", os.path.join(d, FILES[0])] + list(args),
                       capture_output=True, text=True)
    hits = set()
    summ = None
    for line in p.stdout.splitlines():
        m = HIT.match(line)
        if m:
            hits.add((m.group(2), m.group(1)))
        s = SUMMARY.match(line)
        if s:
            summ = tuple(int(x) for x in s.groups())
    return p.returncode, hits, summ, p.stdout


def make_repo(work, prefix, plants):
    d = tempfile.mkdtemp(prefix=prefix, dir=work)
    git(d, "init", "-q")
    if os.path.realpath(git(d, "rev-parse", "--show-toplevel", text=True).strip()) != os.path.realpath(d):
        raise OSError("fixture toplevel")
    for rel, text in plants.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "plant")
    return d


def generated(seed):
    """Return (plants, expected hit set) with values drawn from random.Random(seed)."""
    r = random.Random(seed)
    cfsig = "".join(r.choice(URLSAFE) for _ in range(r.randint(172, 344)))
    kpi = "K" + "".join(r.choice(UPPER) for _ in range(r.randint(12, 20)))
    asig = base64.b64encode(bytes(r.getrandbits(8) for _ in range(32))).decode().replace("=", "%3D")
    exp = str(r.randint(1767000000, 1799999999))
    host = "d%s.cloudfront.net" % "".join(r.choice(string.ascii_lowercase + string.digits) for _ in range(13))
    pre = "&".join("%s=%d" % (r.choice(["color", "size", "w", "h", "v"]) + str(i), r.randint(0, 999)) for i in range(r.randint(0, 4)))
    pre = (pre + "&") if pre else ""
    plants = {
        "g/x-receipts/live-g1.txt": "https://%s/a.jpg?%sExpires=%s&Signature=%s&Key-Pair-Id=%s\n" % (host, pre, exp, cfsig, kpi),
        "g/x-receipts/live-g2.json": '{"u":"https://%s/a.mp4?%sKey-Pair-Id=%s\\u0026Expires=%s\\u0026Signature=%s"}\n' % (host, pre.replace("&", "\\u0026"), kpi, exp, cfsig),
        "g/x-receipts/live-g3.json": '{"u":"https://acct.blob.core.windows.net/c/b.txt?sp=rw\\u0026st=2026-11-07T00:00:00Z\\u0026se=2026-11-08T00:00:00Z\\u0026spr=https\\u0026sv=2022-11-02\\u0026sr=b\\u0026sig=%s"}\n' % asig,
        "g/x-receipts/live-n1.txt": "https://%s/a.jpg?%sExpires=%s&Signature=%s\n" % (host, pre, exp, cfsig),
        "g/x-receipts/live-n2.txt": "https://%s/a.jpg?expires=%s&signature=%s&key-pair-id=%s\n" % (host, exp, cfsig, kpi),
        "g/x-receipts/live-n3.txt": "https://acct.blob.core.windows.net/c/b.txt?sp=rw\\u0026sr=b\\u0026sig=%s\n" % asig,
    }
    expect = {("g/x-receipts/live-g1.txt", CF), ("g/x-receipts/live-g2.json", CF), ("g/x-receipts/live-g3.json", AZ)}
    return plants, expect


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--instrument-sha256")
    ap.add_argument("--gate-sha256")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2check-", dir=a.work)
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(4), "big")
    limbs = []
    try:
        try:
            rev = git(lane, "rev-parse", "--verify", a.rev + "^{commit}", text=True).strip()
            blobs = {}
            for f in FILES:
                try:
                    blobs[f] = git(lane, "show", "%s:corpus/instruments/%s" % (rev, f))
                except subprocess.CalledProcessError:
                    blobs[f] = None
            scorecard = git(lane, "show", "%s:SCORECARD.md" % rev).decode("utf-8")
            oracle = set(x.split(":", 1)[1] for x in git(
                lane, "grep", "-l", "-E", ORACLE_RE, HISTORY_REV, "--", text=True).split("\n") if x)
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError) as e:
            print("CAPABILITY-CHECK-RESULT error reason=read:%s rc=2" % type(e).__name__)
            return 2
        inst = os.path.join(work, "inst")
        os.makedirs(inst)
        present = all(blobs[f] is not None for f in FILES)
        if present:
            for f in FILES:
                with open(os.path.join(inst, f), "wb") as fh:
                    fh.write(blobs[f])
        print("CAPABILITY-CHECK rev=%s instrument_present=%s seed=%d" % (rev, present, seed))
        # K1
        det = "missing=%s" % ",".join(f for f in FILES if blobs[f] is None) if not present else ""
        ok = present
        if present:
            isha, gsha = sha(blobs[FILES[0]]), sha(blobs[FILES[1]])
            rc, _, _, out = run_instr(inst, "--selftest")
            ok = (rc == 0 and "SELFTEST-RESULT pass" in out
                  and (not a.instrument_sha256 or isha == a.instrument_sha256.lower())
                  and (not a.gate_sha256 or gsha == a.gate_sha256.lower()))
            det = "selftest_rc=%d instrument_sha256=%s gate_sha256=%s" % (rc, isha, gsha)
        limbs.append(("K1", ok, det))
        # K2
        ok, det = False, "instrument-absent"
        if present:
            rc, hits, _, _ = run_instr(inst, "--lane", lane, "--rev", HISTORY_REV)
            sts = set(p for p, s in hits if s == "aws-sts-session-token")
            ok = rc == 1 and oracle == set(HISTORY_EXPECTED) and sts == oracle
            det = "rc=%d sts_files=%d oracle=%d oracle_matches_expected=%s" % (rc, len(sts), len(oracle), oracle == set(HISTORY_EXPECTED))
        limbs.append(("K2", ok, det))
        # K3
        ok, det = False, "instrument-absent"
        if present:
            rc, hits, summ, _ = run_instr(inst, "--lane", lane, "--rev", rev)
            ok = bool(rc == 0 and summ and summ[1] == 0 and summ[4] == 0 and summ[3] >= 1 and not hits)
            det = "rc=%d summary=%s" % (rc, "scanned=%d,hits=%d,files=%d,allowed=%d,unused_allow=%d" % summ[:5] if summ else "none")
        limbs.append(("K3", ok, det))
        # K4
        ok, det, hits = False, "instrument-absent", set()
        if present:
            d = make_repo(work, "plant-", PLANTS)
            fp_sha = sha(FP_MATCH)
            allow = os.path.join(work, "plant-allow.tsv")
            with open(allow, "w") as fh:
                fh.write("w/y-receipts/fp.json\tcredential\t%s\tfile name, not a secret\n" % fp_sha)
                fh.write("w/y-receipts/fp-other.json\tcredential\t%s\tbinds the other file's value only\n" % fp_sha)
            rc, hits, _, _ = run_instr(inst, "--lane", d, "--rev", "HEAD", "--allow", allow)
            bad_allow = os.path.join(work, "plant-allow-sts.tsv")
            with open(bad_allow, "w") as fh:
                fh.write("corpus/source-snapshots/round-1/S001.txt\taws-sts-session-token\t%s\tforged\n" % ("0" * 64))
            rc2, _, _, _ = run_instr(inst, "--lane", d, "--rev", "HEAD", "--allow", bad_allow)
            f1 = os.path.join(d, "corpus/practice/p/evidence/E1.txt")
            f2 = os.path.join(d, "corpus/source-snapshots/round-1/S006.txt")
            f3 = os.path.join(d, "corpus/practice/p/report2.md")
            rc3, fhits, _, _ = run_instr(inst, "--files", f1, f2, f3, "--allow", allow)
            fok = rc3 == 1 and fhits == {(f1, AZ), (f3, CF)}
            ok = rc == 1 and hits == set(PLANT_EXPECT) and rc2 == 2 and fok
            det = "rc=%d missing=%s extra=%s sts_allow_rc=%d files_rc=%d files_hits=%d files_ok=%s" % (
                rc, ",".join(sorted("%s|%s" % x for x in set(PLANT_EXPECT) - hits)) or "none",
                ",".join(sorted("%s|%s" % x for x in hits - set(PLANT_EXPECT))) or "none", rc2, rc3, len(fhits), fok)
        limbs.append(("K4", ok, det))
        # K6
        ok, det = False, "instrument-absent"
        if present:
            binst = os.path.join(work, "base-inst")
            os.makedirs(binst)
            for f in FILES[:2]:
                with open(os.path.join(binst, f), "wb") as fh:
                    fh.write(git(lane, "show", "%s:corpus/instruments/%s" % (BASE_REV, f)))
            rcb, bhits, _, _ = run_instr(binst, "--lane", d, "--rev", "HEAD", "--allow", allow)
            caught = bhits & set(NEW_EXPECT)
            ok = rcb == 1 and not caught and bhits <= set(PLANT_EXPECT)
            det = "base_rc=%d base_hits=%d new_caught_by_base=%s" % (
                rcb, len(bhits), ",".join(sorted("%s|%s" % x for x in caught)) or "none")
        limbs.append(("K6", ok, det))
        # K7
        ok, det = False, "instrument-absent"
        if present:
            gplants, gexpect = generated(seed)
            gd = make_repo(work, "gen-", gplants)
            rcg, ghits, _, _ = run_instr(inst, "--lane", gd, "--rev", "HEAD", "--allow", os.devnull)
            ok = rcg == 1 and ghits == gexpect
            det = "seed=%d rc=%d missing=%s extra=%s" % (
                seed, rcg, ",".join(sorted("%s|%s" % x for x in gexpect - ghits)) or "none",
                ",".join(sorted("%s|%s" % x for x in ghits - gexpect)) or "none")
        limbs.append(("K7", ok, det))
        # K8
        ok, det = False, "instrument-absent"
        if present:
            badc = [c for c, (p, s, want) in sorted(CLAUSES.items())
                    if p not in PLANTS or ((p, s) in hits) != want]
            ok = not badc
            det = "clauses=%d failing=%s" % (len(CLAUSES), ";".join(badc) or "none")
        limbs.append(("K8", ok, det))
        # K5
        sec = scorecard.split("\n## Capabilities\n", 1)
        rows = []
        if len(sec) == 2:
            for line in sec[1].split("\n## ", 1)[0].splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if line.startswith("|") and cells and cells[0] == "capture-secret-scan":
                    rows.append(cells)
        need = (CF, "gcs-signed-url-signature", AZ, "corpus/practice/*/evidence/")
        ok = len(rows) == 1 and rows[0][-1] == "87" and all(n in " ".join(rows[0]) for n in need)
        limbs.append(("K5", ok, "rows=%d" % len(rows)))
    except (subprocess.CalledProcessError, OSError) as e:
        print("CAPABILITY-CHECK-RESULT error reason=run:%s rc=2" % type(e).__name__)
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)
    for name, ok, det in limbs:
        print("LIMB %s %s %s" % (name, "pass" if ok else "FAIL", det))
    allok = all(ok for _, ok, _ in limbs)
    print("CAPABILITY-CHECK-RESULT %s rc=%d" % ("pass" if allok else "fail", 0 if allok else 1))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
