#!/usr/bin/env python3
"""Re-run the three intake-gate bypass forms found by SentinelGate (r90) against
corpus/instruments/capture-source.py at 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2.

Writes nothing outside its own scratch dir (removed at the end) and never into the lane.
Synthetic values are generated here; none is a real credential.

  python3 -B repro-bypass-r90.sh        (the file is a Python script despite the .sh name)
"""
import functools
import hashlib
import http.server
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import threading

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
INST = os.path.join(LANE, "corpus", "instruments")
REV = "643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2"
S = tempfile.mkdtemp(prefix="sentinelgate-repro-", dir="/fast/scratch/hyaku/kasegi-r90")
os.makedirs(os.path.join(S, "srv"))
os.makedirs(os.path.join(S, "out"))
V = "FAKEfakeSYNTHETICVALUE0123456789abcdef"     # synthetic, generated, never a credential

spec = importlib.util.spec_from_file_location("scan", os.path.join(INST, "capture-secret-scan.py"))
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)
PATS = scan.patterns()


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=os.path.join(S, "srv")))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = "http://127.0.0.1:%d/" % srv.server_address[1]

CASES = [
    ("control-plain-sts", "<p>X-Amz-Security-Token=%s</p>" % V),
    ("V1-entity-separator", "<p>https://a.blob.core.windows.net/c/b?sv=2022-11-02&amp;#x26;sr=b&amp;#x26;sig=%s</p>" % V),
    ("V2-percent-separator", "<p>https://a.blob.core.windows.net/c/b?sv=2022-11-02%%26sr=b%%26sig=%s</p>" % V),
    ("V3-intra-value-tab", "<p>X-Amz-Security-Token=%s&#9;%s</p>" % (V[:10], V[10:])),
]
try:
    for name, body in CASES:
        fn = name + ".html"
        with open(os.path.join(S, "srv", fn), "w", encoding="utf-8") as fh:
            fh.write("<html><body>%s</body></html>" % body)
        out = os.path.join(S, "out", name + ".txt")
        p = subprocess.run([sys.executable, "-B", os.path.join(INST, "capture-source.py"), "--id", "REPRO",
                            "--url", BASE + fn, "--out", out],
                           capture_output=True, text=True, env=dict(os.environ, TMPDIR=S))
        wrote = os.path.exists(out)
        shapes = ",".join(sorted({l.split("shape=")[1].split(" ")[0]
                                  for l in p.stdout.splitlines() if l.startswith("INTAKE-REFUSED")})) or "none"
        verdict = "-"
        if wrote:
            verdict = "scanner-clean" if not scan.scan_bytes(open(out, "rb").read(), PATS)[0] else "scanner-HIT"
        print("%-24s rc=%d written=%-3s shapes=%-10s written_file=%s sha16=%s" % (
            name, p.returncode, "yes" if wrote else "no", shapes, verdict,
            hashlib.sha256(open(out, "rb").read()).hexdigest()[:16] if wrote else "-"))
    print("REPRO instrument_sha256=%s" % hashlib.sha256(open(os.path.join(INST, "capture-source.py"), "rb").read()).hexdigest())
finally:
    srv.shutdown()
    shutil.rmtree(S, ignore_errors=True)
    print("scratch removed:", not os.path.exists(S))
