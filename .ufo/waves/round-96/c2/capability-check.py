#!/usr/bin/env python3
"""kasegi round-96 C2 counter for the capability `capture-secret-scan`:
round 96 adds the routable and versioned-routable GitLab forms (`glpat-`,
`glrtr-`, `gldt-`, `glagent-`, `glwt-`; S140 lines 30, 51, 136, 324, 358, 375)
and the pipeline trigger token (`glptt-` 20 or 40; S140 line 73).

Usage:
  python3 capability-check.py --lane LANE --rev REV --work DIR \
      [--instrument-sha256 HEX] [--gate-sha256 HEX] [--seed N]

Limbs:
  K1 instrument  the three instrument files exist at REV; capture-secret-scan.py
                 sha256 == --instrument-sha256 and claim-package-check.py sha256
                 == --gate-sha256 (when given); `--selftest` exits 0 printing
                 `SELFTEST-RESULT pass` with cases >= 128.
  K2 clean       run on --rev REV with REV's allowlist: exit 0, hits=0,
                 unused_allow=0, allowed>=1.
  K3 planted     a scratch git repository whose directory names and basenames
                 are built from a run-time nonce: the (path, shape) HIT set
                 equals PLANT_SPEC exactly (seven positives, six negatives).
  K4 discrim     the BASE instrument (corpus/instruments/capture-secret-scan.py
                 at BASE_REV = the round-95 tip) over the same plants reports
                 none of the seven new shapes, and no earlier shape is missing.
  K5 table       SCORECARD.md at REV has exactly one `capture-secret-scan` row
                 in `## Capabilities`; its first-working-round cell is `87` and
                 the row names the round-96 shapes.
  K6 history     the new instrument on HISTORY_REV (round-86 freeze, which pushed
                 the S122 STS token) still reports `aws-sts-session-token`: no
                 shape lost.

Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage or read error.
"""
import argparse
import hashlib
import os
import random
import re
import shutil
import subprocess
import sys

BASE_REV = "d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6"
HISTORY_REV = "252df0c90c066d83d229e3107811a6bc05e8feed"
INSTRUMENT = "corpus/instruments/capture-secret-scan.py"
GATE = "corpus/instruments/claim-package-check.py"
ALLOW = "corpus/instruments/capture-secret-allow.tsv"

NEW_SHAPES = {"gitlab-pat-versioned", "gitlab-pat-routable",
              "gitlab-runner-auth-token-versioned", "gitlab-deploy-token-versioned",
              "gitlab-agent-token-versioned", "gitlab-workspace-token-versioned",
              "gitlab-pipeline-trigger-token"}
OLD_SHAPES = {"github-token", "github-refresh-token", "gitlab-pat", "gitlab-jwt-token",
              "gitlab-runner-auth-token", "gitlab-deploy-token", "aws-access-key-id",
              "aws-sts-session-token", "gcs-signed-url-signature", "azure-sas-signature",
              "cloudfront-signed-url-signature", "cloudfront-signed-cookie-signature"}

VER = b".ab.cd1234567"
ROUT = b".ab" + b"cd12345"


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
    r = git(d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "plant")
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
        r = subprocess.run(["git", "-C", lane, "show", "%s:%s" % (rev, rel)], capture_output=True)
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


PLANT_SPEC = [
    ("p1.txt", "gitlab-pat-versioned"),
    ("p2.txt", "gitlab-pat-routable"),
    ("p3.txt", "gitlab-runner-auth-token-versioned"),
    ("p4.txt", "gitlab-deploy-token-versioned"),
    ("p5.txt", "gitlab-agent-token-versioned"),
    ("p6.html", "gitlab-workspace-token-versioned"),
    ("p7.txt", "gitlab-pipeline-trigger-token"),
]


def build_plants(work, seed):
    rnd = random.Random(seed)
    nonce = "".join(rnd.choice("abcdefghijkmnpqrstuvwxyz0123456789") for _ in range(12))
    root = os.path.join(work, "plant-" + nonce)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    git(root, "init", "-q")
    files = {
        # positives
        "p1.txt": b"t glpat-" + b"A" * 28 + VER + b" end\n",
        "p2.txt": b'{"t":"glpat-' + b"B" * 28 + ROUT + b'"}\n',
        "p3.txt": b"q=glrtr-" + b"C" * 30 + VER + b"\n",
        "p4.txt": b"acme-gldt-" + b"D" * 30 + VER + b" prose\n",
        "p5.txt": b"glagent-" + b"E" * 30 + VER + b"\n",
        "p6.html": b"<i>glwt-" + b"F" * 30 + VER + b"</i>\n",
        "p7.txt": b"glptt-" + b"G" * 40 + b"\n",
        # negatives
        "n1.txt": b"glpat-" + b"A" * 26 + ROUT + b"\n",              # 26-char head
        "n2.txt": b"glpat-" + b"A" * 28 + b".AB" + b"cd12345\n",     # upper tail
        "n3.txt": b"glpat-" + b"A" * 28 + b".d.fg1234567\n",         # 1-char middle
        "n4.txt": b"glptt-" + b"G" * 39 + b"\n",                     # 39 chars
        "n5.txt": b"glwt-" + b"F" * 30 + b".ab.cd12345\n",           # short tail
        "n6.txt": b"glagent-" + b"E" * 30 + b".AB.cd1234567\n",      # upper middle
    }
    for name, data in files.items():
        d = os.path.join(root, nonce + "-" + name.split(".")[0][-1])
        write(os.path.join(d, nonce + "-" + name), data)
    rev = commit(root)
    expect = {(nonce + "-" + n, shape) for n, shape in PLANT_SPEC}
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
    ok = ok and st.returncode == 0 and bool(m) and int(m.group(1)) >= 128
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
    else:
        rc, bhits, bcounts, bout = run_instr(binst, "--files", *plant_paths)
        missed = {h for h in bhits if h[1] in NEW_SHAPES}
        import importlib.util
        spec = importlib.util.spec_from_file_location("base_instr", binst)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        base_shapes = {name for name, _ in mod.patterns()}
        old_missing = OLD_SHAPES - base_shapes
        ok = not missed and not old_missing
        limbs.append(("K4", ok, "base_new_shape_hits=%d old_shapes_missing=%s" % (
            len(missed), sorted(old_missing) or "none")))

    score = subprocess.run(["git", "-C", lane, "show", "%s:SCORECARD.md" % a.rev],
                           capture_output=True, text=True).stdout
    rows = [ln for ln in score.split("\n") if ln.startswith("| `capture-secret-scan`") or ln.startswith("| capture-secret-scan")]
    named = all(s in rows[0] for s in ("gitlab-pat-versioned", "gitlab-pat-routable",
                                       "gitlab-pipeline-trigger-token")) if rows else False
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
