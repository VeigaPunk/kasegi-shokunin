#!/usr/bin/env python3
"""kasegi round-87 C2 counter: capability `capture-secret-scan` enters, measured at one revision.

Usage:
  python3 capability-check.py --lane LANE --rev REV --work DIR \
      [--instrument-sha256 HEX] [--gate-sha256 HEX]

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
                 `HIT shape=aws-sts-session-token` line equals the ORACLE set:
                 `git grep -l -E 'X-Amz-Security-Token=[A-Za-z0-9%/+=_-]{20,}'`
                 over HISTORY_REV, which must itself equal HISTORY_EXPECTED.
  K3 clean       run on --rev REV with REV's allowlist: exit 0, hits=0,
                 unused_allow=0 (no stale allowlist row), allowed>=1.
  K4 planted     a scratch git repository with planted files (built here, not
                 by the instrument): the HIT (path, shape) set equals PLANT_EXPECT
                 exactly; and an allowlist holding an aws-sts-session-token row
                 makes the instrument exit 2.
  K5 table       SCORECARD.md at REV has a `## Capabilities` table row whose
                 first cell is `capture-secret-scan` and whose last cell is `87`.

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read error.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HISTORY_REV = "252df0c90c066d83d229e3107811a6bc05e8feed"
HISTORY_EXPECTED = frozenset({
    ".ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json",
    "corpus/source-snapshots/round-86/S122.txt",
})
ORACLE_RE = r"X-Amz-Security-Token=[A-Za-z0-9%/+=_-]{20,}"
FILES = ("capture-secret-scan.py", "claim-package-check.py", "capture-secret-allow.tsv")
HIT = re.compile(r"^HIT shape=(\S+) path=(\S+) line=\d+$")
SUMMARY = re.compile(r"^CAPTURE-SECRET-SCAN mode=\S+ scanned=(\d+) hits=(\d+) files=(\d+) allowed=(\d+) unused_allow=(\d+) rc=(\d+)$")

TOKEN = "IQoJb3JpZ2luX2VjPLANTEDFIXTURESESSIONTOKEN0123456789abcdefABCDEFxyz"
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
}
PLANT_EXPECT = frozenset({
    ("corpus/source-snapshots/round-1/S001.txt", "aws-sts-session-token"),
    ("corpus/source-snapshots/round-1/S001.txt", "aws-access-key-id"),
    ("corpus/source-snapshots/round-1/S001.txt", "credential"),
    ("w/x-receipts/live-a.json", "aws-access-key-id"),
    ("w/live-b.html", "private-key"),
    ("w/y-receipts/fp-other.json", "credential"),
})
FP_MATCH = b'token": "authorization-envelope'


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


def plant_repo(work):
    d = tempfile.mkdtemp(prefix="plant-", dir=work)
    git(d, "init", "-q")
    if os.path.realpath(git(d, "rev-parse", "--show-toplevel", text=True).strip()) != os.path.realpath(d):
        raise OSError("fixture toplevel")
    for rel, text in PLANTS.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "plant")
    return d


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--instrument-sha256")
    ap.add_argument("--gate-sha256")
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2check-", dir=a.work)
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
        print("CAPABILITY-CHECK rev=%s instrument_present=%s" % (rev, present))
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
        ok, det = False, "instrument-absent"
        if present:
            d = plant_repo(work)
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
            ok = rc == 1 and hits == set(PLANT_EXPECT) and rc2 == 2
            det = "rc=%d missing=%s extra=%s sts_allow_rc=%d" % (
                rc, ",".join(sorted("%s|%s" % x for x in set(PLANT_EXPECT) - hits)) or "none",
                ",".join(sorted("%s|%s" % x for x in hits - set(PLANT_EXPECT))) or "none", rc2)
        limbs.append(("K4", ok, det))
        # K5
        sec = scorecard.split("\n## Capabilities\n", 1)
        rows = []
        if len(sec) == 2:
            for line in sec[1].split("\n## ", 1)[0].splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if line.startswith("|") and cells and cells[0] == "capture-secret-scan":
                    rows.append(cells)
        ok = len(rows) == 1 and rows[0][-1] == "87"
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
