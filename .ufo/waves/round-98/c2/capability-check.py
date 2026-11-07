#!/usr/bin/env python3
"""kasegi round-98 C2 capability gate — capture-secret-scan, four further S140
rules and the five widened right boundaries.

Limbs (frozen in .ufo/waves/round-98/claims.json):
  K1 instrument  the three instrument files exist at REV; capture-secret-scan.py
                 sha256 equals the frozen pin and --selftest exits 0 with
                 cases>=170.
  K2 clean       run on --rev REV with REV's allowlist: exit 0, hits=0,
                 unused_allow=0, allowed>=1.
  K3 planted     a scratch git repository whose directory names and basenames
                 are nonce-derived; the (path, shape) HIT set equals PLANT_SPEC
                 exactly. Every positive value is GENERATED from the rule's own
                 alphabet and length by this gate (not copied from the
                 instrument's selftest literals), so a literal-locked matcher
                 cannot pass (round-97 spot-check defect 3).
  K4 base        the round-97 landing instrument at BASE_REV reports 0 of the
                 four new shapes on the same plants and misses none of the
                 earlier shapes.
  K5 scorecard   SCORECARD.md at REV has exactly one capture-secret-scan row,
                 names all nine round-98 shape ids, first-working-round 87.
  K6 history     on the round-86 freeze the new instrument still reports
                 aws-sts-session-token.
  K7 boundary    the five widened shapes HIT a real token followed by `_` or
                 `-` at REV and MISS it at BASE_REV (the measured round-97
                 defect), on the same generated payloads.

Verdict: 0 pass, 1 fail, 2 could-not-evaluate (instrument missing).
"""
import argparse
import hashlib
import importlib.util
import os
import random
import re
import shutil
import subprocess
import sys

INSTRUMENT = "corpus/instruments/capture-secret-scan.py"
GATE = "corpus/instruments/claim-package-check.py"
ALLOW = "corpus/instruments/capture-secret-allow.tsv"
BASE_REV = "a9a53608dce6aea07d298bb9d5133532078eb1dd"   # round-97 C2 landing
HISTORY_REV = "252df0c9"                                 # round-86 freeze
NEW_SHAPES = {"gitlab-ci-build-token", "gitlab-iam-refresh-token",
              "gitlab-iam-authorization-code", "gitlab-session-cookie"}
WIDENED = {"gitlab-runner-registration-token", "gitlab-feed-token",
           "gitlab-oauth-app-secret", "gitlab-feed-token-v2",
           "gitlab-scim-oauth-token"}
ALL_NEW = NEW_SHAPES | WIDENED
OLD_SHAPES = {"github-token", "github-refresh-token", "gitlab-pat", "gitlab-jwt-token",
              "gitlab-pat-versioned", "gitlab-pat-routable",
              "gitlab-runner-auth-token-versioned", "gitlab-deploy-token-versioned",
              "gitlab-agent-token-versioned", "gitlab-workspace-token-versioned",
              "gitlab-pipeline-trigger-token", "gitlab-runner-registration-token",
              "gitlab-feed-token", "gitlab-oauth-app-secret", "gitlab-feed-token-v2",
              "gitlab-incoming-email-token", "gitlab-scim-oauth-token",
              "gitlab-deploy-token-in-url", "gitlab-feature-flags-client-token",
              "gitlab-runner-controller-token", "gitlab-kubernetes-agent-token",
              "aws-sts-session-token", "aws-access-key-id", "private-key",
              "credential", "bearer", "authorization", "session-cookie",
              "gcs-signed-url-signature", "azure-sas-signature",
              "cloudfront-signed-url-signature", "cloudfront-signed-cookie-signature"}

ALNUM = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
ALNUMU = ALNUM + "_-"
HEX = "0123456789abcdef"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode) as fh:
        fh.write(data)


def git(d, *args):
    return sh(["git", "-C", d] + list(args))


def commit(d):
    git(d, "add", "-A")
    r = git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", "plant")
    if r.returncode != 0:
        raise SystemExit("plant commit failed: " + r.stderr)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("plant root mismatch")
    return git(d, "rev-parse", "HEAD").stdout.strip()


def extract(lane, rev, work, tag):
    d = os.path.join(work, "inst-" + tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for rel in (INSTRUMENT, GATE, ALLOW):
        r = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (rev, rel)],
                           capture_output=True)
        if r.returncode != 0:
            return None, None
        write(os.path.join(d, rel), r.stdout)
    return os.path.join(d, INSTRUMENT), d


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_instr(inst, *args):
    r = sh([sys.executable, "-B", inst] + list(args))
    out = r.stdout + r.stderr
    hits = set()
    counts = {}
    for m in re.finditer(r"HIT shape=([a-z0-9-]+) path=(\S+) line=(\d+)", out):
        hits.add((os.path.basename(m.group(2)), m.group(1)))
    for m in re.finditer(r"scanned=(\d+) hits=(\d+) files=(\d+) allowed=(\d+) unused_allow=(\d+)", out):
        counts = {"scanned": int(m.group(1)), "hits": int(m.group(2)),
                  "files": int(m.group(3)), "allowed": int(m.group(4)),
                  "unused": int(m.group(5))}
    return r.returncode, hits, counts, out


def gen(rnd, alphabet, n):
    return "".join(rnd.choice(alphabet) for _ in range(n)).encode()


# One table: each row is (basename, shape, payload builder). The expected HIT
# set is derived from this table, never from a second list (R152).
PLANT_SPEC = [
    # positives: the four new shapes
    ("p1.txt", "gitlab-ci-build-token",
     lambda r: b"t glcbt-" + gen(r, ALNUM, r.randint(1, 5)) + b"_" + gen(r, ALNUMU, 20) + b" end\n"),
    ("p2.txt", "gitlab-iam-refresh-token",
     lambda r: b"gliamrt-" + gen(r, ALNUMU, 43) + b"." + gen(r, ALNUMU, 43) + b"\n"),
    ("p3.html", "gitlab-iam-authorization-code",
     lambda r: b"<i>gliamac-" + gen(r, ALNUMU, 43) + b"." + gen(r, ALNUMU, 43) + b"</i>\n"),
    ("p4.txt", "gitlab-session-cookie",
     lambda r: b"Cookie: _gitlab_session=" + gen(r, HEX, 64) + b"; Path=/\n"),
    # positives: the five widened right boundaries (a real token + `_`/`-`)
    ("p5.txt", "gitlab-runner-registration-token",
     lambda r: b"GR1348941" + gen(r, ALNUMU, 20) + b"_x\n"),
    ("p6.txt", "gitlab-feed-token",
     lambda r: b"u?feed_token=" + gen(r, ALNUMU, 20) + b"-x&page=1\n"),
    ("p7.txt", "gitlab-oauth-app-secret",
     lambda r: b"gloas-" + gen(r, ALNUMU, 64) + b"_x\n"),
    ("p8.txt", "gitlab-feed-token-v2",
     lambda r: b"glft-" + gen(r, ALNUMU, 20) + b"-x\n"),
    ("p9.txt", "gitlab-scim-oauth-token",
     lambda r: b"glsoat-" + gen(r, ALNUMU, 20) + b"_x\n"),
    # negatives: one boundary defect per new shape
    ("n1.txt", None, lambda r: b"glcbt-" + gen(r, ALNUM, 6) + b"_" + gen(r, ALNUMU, 20) + b"\n"),
    ("n2.txt", None, lambda r: b"gliamrt-" + gen(r, ALNUMU, 42) + b"." + gen(r, ALNUMU, 43) + b"\n"),
    ("n3.txt", None, lambda r: b"gliamac-" + gen(r, ALNUMU, 43) + gen(r, ALNUMU, 43) + b"\n"),
    ("n4.txt", None, lambda r: b"_gitlab_session=" + gen(r, HEX, 63) + b"\n"),
    ("n5.txt", None, lambda r: b"GR1348941" + gen(r, ALNUMU, 21) + b"\n"),
    ("n6.txt", None, lambda r: b"feed_token=" + gen(r, ALNUMU, 19) + b"&page=1\n"),
    ("n7.txt", None, lambda r: b"gloas-" + gen(r, ALNUMU, 63) + b"\n"),
    ("n8.txt", None, lambda r: b"glft-" + gen(r, ALNUMU, 21) + b"\n"),
    ("n9.txt", None, lambda r: b"glsoat-" + gen(r, ALNUMU, 19) + b"\n"),
    ("n10.txt", None, lambda r: gen(r, HEX, 64) + b"\n"),
]


def build_plants(work, seed):
    rnd = random.Random(seed)
    nonce = "".join(rnd.choice("abcdefghijkmnpqrstuvwxyz0123456789") for _ in range(12))
    root = os.path.join(work, "plant-" + nonce)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    git(root, "init", "-q")
    expect = set()
    for name, shape, build in PLANT_SPEC:
        data = build(rnd)
        d = os.path.join(root, nonce + "-" + name.split(".")[0][-1])
        write(os.path.join(d, nonce + "-" + name), data)
        if shape:
            expect.add((nonce + "-" + name, shape))
    rev = commit(root)
    return root, rev, expect


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--instrument-sha256")
    ap.add_argument("--gate-sha256")
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    os.makedirs(a.work, exist_ok=True)
    seed = a.seed if a.seed is not None else random.randrange(1, 2 ** 31)
    limbs = []

    inst, idir = extract(lane, a.rev, a.work, "rev")
    if inst is None:
        print("CAPABILITY-CHECK-RESULT error reason=instrument-missing rc=2")
        return 2
    ok = True
    det = []
    got_i = sha256_file(inst)
    got_g = sha256_file(os.path.join(idir, GATE))
    if a.instrument_sha256:
        ok = ok and got_i == a.instrument_sha256.lower()
        det.append("inst_sha=%s" % ("pin-ok" if got_i == a.instrument_sha256.lower() else got_i))
    if a.gate_sha256:
        ok = ok and got_g == a.gate_sha256.lower()
        det.append("gate_sha=%s" % ("pin-ok" if got_g == a.gate_sha256.lower() else got_g))
    st = sh([sys.executable, "-B", inst, "--selftest"])
    m = re.search(r"SELFTEST-RESULT pass cases=(\d+)", st.stdout + st.stderr)
    ok = ok and st.returncode == 0 and bool(m) and int(m.group(1)) >= 170
    det.append("selftest=%s cases=%s" % ("pass" if st.returncode == 0 else "rc%d" % st.returncode,
                                         m.group(1) if m else "none"))
    limbs.append(("K1", ok, " ".join(det)))

    rc, hits, counts, out = run_instr(inst, "--lane", lane, "--rev", a.rev)
    ok = rc == 0 and counts.get("hits") == 0 and counts.get("unused") == 0 and counts.get("allowed", 0) >= 1
    limbs.append(("K2", ok, "rc=%d scanned=%s hits=%s allowed=%s unused_allow=%s" % (
        rc, counts.get("scanned"), counts.get("hits"), counts.get("allowed"), counts.get("unused"))))

    root, prev, expect = build_plants(a.work, seed)
    plant_paths = [os.path.join(dp, f) for dp, _, fs in os.walk(root)
                   for f in fs if "/.git/" not in os.path.join(dp, f)]
    rc, hits, counts, out = run_instr(inst, "--files", *plant_paths)
    ok = hits == expect
    limbs.append(("K3", ok, "rc=%d hits=%d missing=%s extra=%s" % (
        rc, len(hits), sorted(expect - hits) or "none", sorted(hits - expect) or "none")))

    binst, bdir = extract(lane, BASE_REV, a.work, "base")
    if binst is None:
        limbs.append(("K4", False, "base instrument missing"))
        limbs.append(("K7", False, "base instrument missing"))
    else:
        rc, bhits, bcounts, bout = run_instr(binst, "--files", *plant_paths)
        missed = {h for h in bhits if h[1] in NEW_SHAPES}
        spec = importlib.util.spec_from_file_location("base_instr", binst)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        base_shapes = {name for name, _ in mod.patterns()}
        old_missing = OLD_SHAPES - base_shapes
        ok = not missed and not old_missing
        limbs.append(("K4", ok, "base_new_shape_hits=%d old_shapes_missing=%s" % (
            len(missed), sorted(old_missing) or "none")))
        # K7: the five widened shapes' `_`/`-` payloads are the p5..p9 plants.
        widened_paths = [p for p in plant_paths
                         if os.path.basename(p).endswith(("p5.txt", "p6.txt", "p7.txt", "p8.txt", "p9.txt"))]
        rc, bhits, _, _ = run_instr(binst, "--files", *widened_paths)
        base_widened = {h for h in bhits if h[1] in WIDENED}
        landing_widened = {h for h in hits if h[1] in WIDENED}
        ok = not base_widened and len(landing_widened) == len(WIDENED)
        limbs.append(("K7", ok, "base_widened_hits=%d landing_widened_hits=%d missing=%s" % (
            len(base_widened), len(landing_widened),
            sorted(WIDENED - {h[1] for h in landing_widened}) or "none")))

    score = subprocess.run(["git", "-C", lane, "show", "%s:SCORECARD.md" % a.rev],
                           capture_output=True, text=True).stdout
    rows = [ln for ln in score.split("\n") if ln.startswith("| `capture-secret-scan`") or ln.startswith("| capture-secret-scan")]
    named = all(s in rows[0] for s in sorted(ALL_NEW)) if rows else False
    last = rows[0].rstrip().rstrip("|").split("|")[-1].strip() if rows else ""
    ok = len(rows) == 1 and named and last == "87"
    limbs.append(("K5", ok, "rows=%d last=%s named=%s" % (len(rows), last or "none", named)))

    rc, hhits, hcounts, hout = run_instr(inst, "--lane", lane, "--rev", HISTORY_REV)
    ok = rc == 1 and ("aws-sts-session-token" in {h[1] for h in hhits})
    limbs.append(("K6", ok, "rc=%d shapes=%s" % (rc, ",".join(sorted({h[1] for h in hhits})) or "none")))

    bad = [n for n, okk, _ in limbs if not okk]
    print("CAPABILITY-CHECK-REV rev=%s seed=%d" % (a.rev, seed))
    for n, okk, d in limbs:
        print("LIMB %s %s %s" % (n, "ok" if okk else "FAIL", d))
    print("CAPABILITY-CHECK-RESULT %s rc=%d" % ("pass" if not bad else "fail", 0 if not bad else 1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
