#!/usr/bin/env python3
"""kasegi round-90 C2 counter: capability `capture-intake-gate` — capture-source.py
refuses, before writing, a snapshot whose bytes carry credential material.

Usage:
  python3 capability-check.py --lane LANE --rev REV --base-rev REV --work DIR
      [--instrument FILE] [--instrument-sha256 HEX] [--seed N]

The counter extracts corpus/instruments/ at REV (`git archive`, never the working
tree) into a scratch tree, optionally replaces capture-source.py with --instrument
(controls only; printed as override=), and drives the instrument as a subprocess
with inputs served by a loopback HTTP server it starts (127.0.0.1, no external network). Shapes come from the scanner at REV itself:
capture-secret-scan.patterns(), so a shape the scanner gains without a plant here
fails G0 (round-89 lesson M89-2: the case list is derived, not hand-claimed).
Plant values are drawn at run time from the printed seed.

Limbs (all must hold):
  G0 coverage  plant shapes == the scanner's pattern names at REV (no missing, no extra).
  G1 refuse    every plant: rc 3, --out not created, an INTAKE-REFUSED line names the
               plant's shape, and the drawn value appears in neither stdout nor stderr.
  G2 keep      a plant captured onto an existing --out: rc 3 and the file is byte-identical.
  G3 clean     6 clean inputs (3 synthetic HTML, 3 snapshot files read from REV with
               `git show`, captured as text): rc 0 and the written bytes equal the
               bytes BASE-REV's capture-source.py writes for the same input.
  G4 allow     a `credential` plant at path P with a scratch allowlist row for
               (P, credential, sha256 of the matched bytes): rc 0 and written; the same
               plant at another path: rc 3; an `aws-sts-session-token` allow row
               (never allowed): rc 3 (the bad allowlist refuses, fail closed).
  G5 closed    with capture-secret-scan.py removed from the tree, a clean input: rc 3,
               not written.
  G6 selftest  `capture-source.py --selftest` rc 0.
  P  pin       sha256 of the instrument under test equals --instrument-sha256 (when given).
Exit 0 only when every limb holds; 1 when a limb fails; 2 on usage/read error.
"""
import argparse
import functools
import http.server
import threading
import hashlib
import importlib.util
import io
import os
import random
import shutil
import string
import subprocess
import sys
import tarfile
import tempfile

SNAPSHOTS = ("corpus/source-snapshots/round-89/S128.txt",  # AWS doc example, allowlisted at this path
             "corpus/source-snapshots/round-88/S126.txt",
             "corpus/source-snapshots/round-23/S030.txt")


def git(lane, *args):
    return subprocess.run(["git", "-C", lane] + list(args), capture_output=True, check=True).stdout


def extract(lane, rev, dest):
    data = git(lane, "archive", "--format=tar", rev, "corpus/instruments")
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        tf.extractall(dest, filter="tar")
    return os.path.join(dest, "corpus", "instruments")


def rnd(rng, n, alphabet=string.ascii_letters + string.digits):
    return "".join(rng.choice(alphabet) for _ in range(n))


def plants(rng):
    """shape -> (html text, drawn secret value whose echo would be a leak)."""
    up = string.ascii_uppercase + string.digits
    hx = "0123456789abcdef"
    b64 = string.ascii_letters + string.digits
    d = {}
    k = rng.choice(["RSA", "EC", "OPENSSH"])
    d["private-key"] = ("-----BEGIN %s PRIVATE KEY-----" % k, None)
    x = "%s/%s/%s" % (rnd(rng, 6), rnd(rng, 6), rnd(rng, 6))
    d["op-ref"] = ("op://" + x, x)
    x = rnd(rng, 32)
    d["bearer"] = ("Bearer " + x, x)
    x = rnd(rng, 30)
    d["authorization"] = ("Authorization: " + x, x)
    x = rnd(rng, 28)
    d["credential"] = ("api_key=" + x, x)
    x = rnd(rng, 28)
    d["session-cookie"] = ("session_cookie=" + x, x)
    x = rnd(rng, 64)
    d["aws-sts-session-token"] = ("u?X-Amz-Security-Token=" + x + "&amp;X-Amz-Signature=1", x)
    x = rng.choice(["AKIA", "ASIA"]) + "".join(rng.choice(up) for _ in range(16))
    d["aws-access-key-id"] = ("key " + x + " here", x)
    x = "".join(rng.choice(hx) for _ in range(128))
    d["gcs-signed-url-signature"] = ("https://storage.googleapis.com/b/o?X-Goog-Expires=900&amp;X-Goog-Signature=" + x, x)
    x = rnd(rng, 44, b64)
    d["azure-sas-signature"] = ("https://a.blob.core.windows.net/c/b?sv=2022-11-02&amp;sr=b&amp;sig=" + x + "%3D", x)
    x = rnd(rng, 60, b64 + "_~-")
    d["cloudfront-signed-url-signature"] = ("https://d1.cloudfront.net/a.mp4?Expires=1767290400&amp;Signature=" + x
                                            + "&amp;Key-Pair-Id=K" + "".join(rng.choice(up) for _ in range(13)), x)
    return d


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve(directory):
    h = functools.partial(Quiet, directory=directory)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def run(py, inst_dir, args, cwd):
    p = subprocess.run([sys.executable, "-B", os.path.join(inst_dir, "capture-source.py")] + args,
                       capture_output=True, text=True, cwd=cwd, timeout=120)
    return p.returncode, p.stdout, p.stderr


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--instrument")
    ap.add_argument("--instrument-sha256")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2 ** 31)
    rng = random.Random(seed)
    os.makedirs(a.work, exist_ok=True)
    W = tempfile.mkdtemp(prefix="c2r90-", dir=a.work)
    try:
        try:
            T = os.path.join(W, "t")
            inst = extract(lane, a.rev, T)
            if a.instrument:
                shutil.copyfile(a.instrument, os.path.join(inst, "capture-source.py"))
            B = os.path.join(W, "b")
            binst = extract(lane, a.base_rev, B)
            ibytes = open(os.path.join(inst, "capture-source.py"), "rb").read()
            spec = importlib.util.spec_from_file_location("scan_at_rev", os.path.join(inst, "capture-secret-scan.py"))
            scan = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(scan)
            shapes = [n for n, _ in scan.patterns()]
            snaps = [(p, git(lane, "show", "%s:%s" % (a.rev, p))) for p in SNAPSHOTS]
        except Exception as e:
            print("CAPABILITY-CHECK-RESULT error reason=read:%s rc=2" % type(e).__name__)
            return 2
        print("CAPABILITY-CHECK rev=%s base=%s seed=%d override=%s instrument_sha256=%s" % (
            a.rev, a.base_rev, seed, a.instrument or "none", hashlib.sha256(ibytes).hexdigest()))
        inp = os.path.join(W, "in")
        os.makedirs(inp)
        srv = serve(inp)
        base_url = "http://127.0.0.1:%d/" % srv.server_address[1]
        P = plants(rng)
        limbs = []
        missing = sorted(set(shapes) - set(P))
        extra = sorted(set(P) - set(shapes))
        limbs.append(("G0", not missing and not extra, "shapes=%d missing=%s extra=%s" % (
            len(shapes), ",".join(missing) or "none", ",".join(extra) or "none")))
        g1bad = []
        for shape, (text, sec) in sorted(P.items()):
            f = os.path.join(inp, "plant-%s.html" % shape)
            with open(f, "w", encoding="utf-8") as fh:
                fh.write("<html><body><p>intro</p><p>%s</p></body></html>" % text)
            out = os.path.join(T, "corpus", "source-snapshots", "round-90", "P-%s.txt" % shape)
            rc, so, se = run(sys.executable, inst, ["--id", "P", "--url", base_url + os.path.basename(f), "--out", out], T)
            named = any(l.startswith("INTAKE-REFUSED") and ("shape=%s " % shape) in l + " " for l in so.splitlines())
            leak = bool(sec) and (sec in so or sec in se)
            ok = rc == 3 and not os.path.exists(out) and named and not leak
            if not ok:
                g1bad.append("%s(rc=%d,written=%s,named=%s,leak=%s)" % (shape, rc, os.path.exists(out), named, leak))
        limbs.append(("G1", not g1bad, "plants=%d bad=%s" % (len(P), ",".join(g1bad) or "none")))
        # G2
        f = os.path.join(inp, "plant-aws-sts-session-token.html")
        out = os.path.join(T, "corpus", "source-snapshots", "round-90", "existing.txt")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        prev = b"previous snapshot bytes\n"
        with open(out, "wb") as fh:
            fh.write(prev)
        rc, so, se = run(sys.executable, inst, ["--id", "P", "--url", base_url + os.path.basename(f), "--out", out], T)
        kept = os.path.exists(out) and open(out, "rb").read() == prev
        limbs.append(("G2", rc == 3 and kept, "rc=%d kept=%s" % (rc, kept)))
        # G3
        clean = []
        for i, body in enumerate(["<p>Alpha&nbsp; beta</p><u>gamma</u>",
                                  "<h1>Rules</h1><p>The session token is required when temporary credentials are used.</p>",
                                  "<p>Signature=short&amp;Key-Pair-Id=public key ID</p><p>%s</p>" % rnd(rng, 12)]):
            g = os.path.join(inp, "clean-%d.html" % i)
            with open(g, "w", encoding="utf-8") as fh:
                fh.write("<html><body>%s</body></html>" % body)
            clean.append((g, "html", "corpus/source-snapshots/round-90/C%d.txt" % i))
        for i, (p, data) in enumerate(snaps):
            g = os.path.join(inp, "snap-%d.txt" % i)
            with open(g, "wb") as fh:
                fh.write(data)
            clean.append((g, "text", p))
        g3bad = []
        for g, kind, rel in clean:
            o1 = os.path.join(T, rel)
            o2 = os.path.join(B, rel)
            if os.path.exists(o1):
                os.unlink(o1)
            if os.path.exists(o2):
                os.unlink(o2)
            r1, s1, _ = run(sys.executable, inst, ["--id", "C", "--url", base_url + os.path.basename(g), "--out", o1, "--kind", kind], T)
            r2, _, _ = run(sys.executable, binst, ["--id", "C", "--url", base_url + os.path.basename(g), "--out", o2, "--kind", kind], B)
            same = os.path.exists(o1) and os.path.exists(o2) and open(o1, "rb").read() == open(o2, "rb").read()
            if not (r1 == 0 and r2 == 0 and same):
                g3bad.append("%s(rc=%d,base_rc=%d,same=%s)" % (rel, r1, r2, same))
        limbs.append(("G3", not g3bad, "clean=%d bad=%s" % (len(clean), ",".join(g3bad) or "none")))
        # G4
        cf = os.path.join(inp, "plant-credential.html")
        rel = "corpus/source-snapshots/round-90/allowed.txt"
        m = dict(scan.patterns())["credential"].search(P["credential"][0].encode())
        dig = hashlib.sha256(m.group(0)).hexdigest()
        allow = os.path.join(W, "allow.tsv")
        with open(allow, "w") as fh:
            fh.write("%s\tcredential\t%s\tcounter fixture: documented value at one path\n" % (rel, dig))
        o = os.path.join(T, rel)
        ra, _, _ = run(sys.executable, inst, ["--id", "A", "--url", base_url + os.path.basename(cf), "--out", o, "--allow", allow], T)
        allowed_written = os.path.exists(o)
        o2 = os.path.join(T, "corpus/source-snapshots/round-90/other.txt")
        rb_, _, _ = run(sys.executable, inst, ["--id", "A", "--url", base_url + os.path.basename(cf), "--out", o2, "--allow", allow], T)
        bad_allow = os.path.join(W, "allow-sts.tsv")
        with open(bad_allow, "w") as fh:
            fh.write("%s\taws-sts-session-token\t%s\tnever allowed\n" % (rel, "0" * 64))
        o3 = os.path.join(T, "corpus/source-snapshots/round-90/sts.txt")
        rcs, _, _ = run(sys.executable, inst, ["--id", "A", "--url", base_url + "clean-0.html", "--out", o3, "--allow", bad_allow], T)
        g4 = ra == 0 and allowed_written and rb_ == 3 and not os.path.exists(o2) and rcs == 3 and not os.path.exists(o3)
        limbs.append(("G4", g4, "allowed_rc=%d written=%s other_path_rc=%d never_allowed_rc=%d" % (ra, allowed_written, rb_, rcs)))
        # G5
        T5 = os.path.join(W, "t5")
        shutil.copytree(os.path.join(T, "corpus", "instruments"), os.path.join(T5, "corpus", "instruments"))
        os.unlink(os.path.join(T5, "corpus", "instruments", "capture-secret-scan.py"))
        o5 = os.path.join(T5, "corpus/source-snapshots/round-90/C0.txt")
        r5, _, _ = run(sys.executable, os.path.join(T5, "corpus", "instruments"), ["--id", "C", "--url", base_url + os.path.basename(clean[0][0]), "--out", o5], T5)
        limbs.append(("G5", r5 == 3 and not os.path.exists(o5), "rc=%d written=%s" % (r5, os.path.exists(o5))))
        # G6
        r6, s6, _ = run(sys.executable, inst, ["--selftest"], T)
        limbs.append(("G6", r6 == 0, "rc=%d %s" % (r6, " ".join(s6.split())[:120])))
        if a.instrument_sha256:
            got = hashlib.sha256(ibytes).hexdigest()
            limbs.append(("P", got == a.instrument_sha256.lower(), "sha256=%s" % got))
        for name, ok, det in limbs:
            print("LIMB %s %s %s" % (name, "pass" if ok else "FAIL", det))
        allok = all(ok for _, ok, _ in limbs)
        print("CAPABILITY-CHECK-RESULT %s rc=%d" % ("pass" if allok else "fail", 0 if allok else 1))
        return 0 if allok else 1
    finally:
        shutil.rmtree(W, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
