#!/usr/bin/env python3
"""Regenerate every ReviewC2Scanner fixture and re-run the frozen scanner on it.

Usage: python3 -B regen-fixtures.py <scratch-dir> <instrument-dir>

<instrument-dir> must hold the three C2 landing files, extracted read-only with:
  git -C <lane> show 132e16c5:corpus/instruments/capture-secret-scan.py    > <dir>/capture-secret-scan.py
  git -C <lane> show 132e16c5:corpus/instruments/claim-package-check.py    > <dir>/claim-package-check.py
  git -C <lane> show 132e16c5:corpus/instruments/capture-secret-allow.tsv  > <dir>/capture-secret-allow.tsv

No credential value is stored in this file or in the fixtures it drops: the fake session-token
value is assembled from parts at runtime and every fixture lives under <scratch-dir>.
"""
import base64, gzip, hashlib, os, shutil, subprocess, sys, tempfile

S = sys.argv[1]; INST = os.path.join(sys.argv[2], "capture-secret-scan.py")
TOK = "IQoJb3JpZ2luX2Vj" + "PLANTEDFIXTURE" + "0123456789abcdefABCDEF"
PRESIGNED = ("https://b.s3.amazonaws.com/p.png?X-Amz-Algorithm=AWS4-HMAC-SHA256"
             "&X-Amz-Credential=" + "ASIA" + "PLANTEDFIXTURE01" + "%2F20261107%2Fus-west-2%2Fs3%2Faws4_request"
             "&X-Amz-Date=20261107T000000Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host"
             "&X-Amz-Security-Token=" + TOK + "&X-Amz-Signature=deadbeef")
FX = os.path.join(S, "fx"); shutil.rmtree(FX, ignore_errors=True); os.makedirs(FX)
EMPTY = os.path.join(FX, "empty.tsv"); open(EMPTY, "w").close()

def w(name, data):
    p = os.path.join(FX, name); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(data if isinstance(data, bytes) else data.encode())
    return p

def run(label, path, argv=None):
    q = subprocess.run([sys.executable, "-B", INST] + (argv or ["--files", path, "--allow", EMPTY]),
                       capture_output=True, text=True)
    hits = [l.replace(os.path.join(FX, ""), "").replace(FX, "$FX") for l in q.stdout.splitlines() if l.startswith("HIT")]
    print("%-45s rc=%d %s" % (label, q.returncode, "; ".join(hits[:2]) if hits else "clean"))

print("== FN battery (--files mode; rc=1 means a hit was reported)")
w("urlenc_sep.txt", "see https://x.example/r?X-Amz-Security-Token%3D" + TOK + "&X-Amz-Signature=ab\n")
run("percent-encoded separator", os.path.join(FX, "urlenc_sep.txt"))
w("urlenc_sep2.txt", '{"redirect":"https%3A%2F%2Fx.example%2Fr%3FX-Amz-Security-Token%3D' + TOK + '%26X-Amz-Signature%3Dab"}\n')
run("double-encoded url", os.path.join(FX, "urlenc_sep2.txt"))
w("json_u0026.txt", '{"u":"' + PRESIGNED.replace("&", "\\u0026") + '"}\n')
run("json \\u0026 escapes", os.path.join(FX, "json_u0026.txt"))
early = TOK[:9] + "/" + TOK[9:]
w("json_slash_early.txt", '{"u":"https://x.example/r?X-Amz-Security-Token=' + early.replace("/", "\\/") + '\\u0026X-Amz-Signature=1"}\n')
run("json escaped slash at char 10", os.path.join(FX, "json_slash_early.txt"))
w("json_slash_late.txt", '{"u":"https://x.example/r?X-Amz-Security-Token=' + TOK[:16] + 'EA' + TOK[:1] + '\\/rest' + TOK[1:] + '\\u0026X-Amz-Signature=1"}\n')
run("json escaped slash after 20 chars", os.path.join(FX, "json_slash_late.txt"))
w("lower_header.txt", "x-amz-security-token: " + TOK + "\r\n")
run("lowercase header name", os.path.join(FX, "lower_header.txt"))
w("split_header.txt", "X-Amz-Security-Token:\r\n  " + TOK + "\r\n")
run("header name, value on next line", os.path.join(FX, "split_header.txt"))
w("split_eq.txt", "X-Amz-Security-Token=\n" + TOK + "\n")
run("query name, value on next line", os.path.join(FX, "split_eq.txt"))
w("har.json", '{"queryString":[{"name":"X-Amz-Security-Token","value":"' + TOK + '"}]}\n')
run("HAR name/value pair", os.path.join(FX, "har.json"))
w("har_pretty.json", '{\n  "name": "X-Amz-Security-Token",\n  "value": "' + TOK + '"\n}\n')
run("HAR pretty-printed name/value", os.path.join(FX, "har_pretty.json"))
w("utf16.txt", b"\xff\xfe" + (PRESIGNED + "\r\n").encode("utf-16-le"))
run("UTF-16LE capture", os.path.join(FX, "utf16.txt"))
w("gzip_capture.bin", gzip.compress((PRESIGNED + "\n").encode()))
run("gzip-compressed body", os.path.join(FX, "gzip_capture.bin"))
w("nul_sep.bin", b"X-Amz-Security-Token=\x00" + TOK.encode() + b"\x00")
run("binary with NUL separators", os.path.join(FX, "nul_sep.bin"))
w("b64_capture.txt", base64.b64encode((PRESIGNED + "\n").encode()) + b"\n")
run("base64-wrapped capture", os.path.join(FX, "b64_capture.txt"))
p = os.path.join(FX, "big33.txt")
with open(p, "wb") as fh:
    fh.write(b"# filler\n" * (33 * 1024 * 1024 // 9)); fh.write(PRESIGNED.encode() + b"\n")
run("33 MiB capture, value at end", p)
w("js.txt", 'var u = "https://x.example/r?X-Amz-Security-Token=' + TOK + '&X-Amz-Signature=1";\n')
run("plain query string (control)", os.path.join(FX, "js.txt"))

print("\n== scope battery (--rev mode on a fixture repo)")
D = os.path.join(S, "fxrepo"); shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
def g(*a): return subprocess.run(["git", "-C", D] + list(a), capture_output=True, check=True)
g("init", "-q")
assert os.path.realpath(g("rev-parse", "--show-toplevel").stdout.decode().strip()) == os.path.realpath(D)
BODY = "X-Amz-Security-Token=" + TOK + "\n"
paths = ["corpus/source-snapshots/round-1/S001.txt", "corpus/source-snapshots/round-1/sub/x.json",
         ".ufo/waves/round-87/w1/Seat-receipts/a.json", ".ufo/waves/round-87/w1/live-cap.json",
         "w/exec-receipt/x.json", "w/receipts/x.json", "corpus/practice/p/evidence/capture.json",
         "corpus/practice/p/evidence/S122.txt", ".ufo/waves/round-87/w1/Foo-evidence/x.json",
         "docs/snapshots/round-1/S1.txt", "w/live-not-here/x.json", "corpus/notes/capture-x.json"]
for rel in paths:
    p = os.path.join(D, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(BODY)
os.makedirs(os.path.join(D, "w", "receipts"), exist_ok=True)
open(os.path.join(D, "w", "receipts", "target.json"), "w").write(BODY)
os.symlink("../receipts/target.json", os.path.join(D, "corpus", "source-snapshots", "round-1", "link.txt"))
g("add", "-A"); g("-c", "user.name=f", "-c", "user.email=f@invalid", "commit", "-q", "-m", "fx")
q = subprocess.run([sys.executable, "-B", INST, "--lane", D, "--rev", "HEAD", "--allow", EMPTY], capture_output=True, text=True)
hit = set(l.split("path=")[1].split(" ")[0] for l in q.stdout.splitlines() if l.startswith("HIT"))
for rel in paths:
    print("  %-52s %s" % (rel, "HIT" if rel in hit else "clean"))
print("  symlink corpus/source-snapshots/round-1/link.txt      %s" % ("HIT" if "corpus/source-snapshots/round-1/link.txt" in hit else "skipped (mode 120000)"))
print("  " + [l for l in q.stdout.splitlines() if l.startswith("CAPTURE-SECRET-SCAN")][0])

print("\n== allowlist path form (--files; row keyed to the repo-relative path)")
D2 = os.path.join(S, "fx2"); shutil.rmtree(D2, ignore_errors=True)
rel = ".ufo/waves/round-87/w1/X-receipts/fp.json"; p = os.path.join(D2, rel)
key = "tok" + "en"
os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write('{"' + key + '": "authorization-envelope.json"}\n')
m = (key + '": "authorization-envelope').encode(); allow = os.path.join(S, "fx2-allow.tsv")
open(allow, "w").write("%s\tcredential\t%s\tfile name, not a secret\n" % (rel, hashlib.sha256(m).hexdigest()))
for arg, cwd, label in ((rel, D2, "repo-relative from repo root"), ("./" + rel, D2, "'./'-prefixed"),
                        (p, D2, "absolute path")):
    q = subprocess.run([sys.executable, "-B", INST, "--files", arg, "--allow", allow], capture_output=True, text=True, cwd=cwd)
    print("  %-28s rc=%d %s" % (label, q.returncode, q.stdout.strip().splitlines()[-1]))

print("\n== allowlist binding (matched bytes vs value)")
D3 = os.path.join(S, "fx4"); shutil.rmtree(D3, ignore_errors=True)
rel = "corpus/source-snapshots/round-87/S124.txt"; p = os.path.join(D3, rel)
os.makedirs(os.path.dirname(p), exist_ok=True)
m = b"Authorization" + b": AWS4-HMAC-SHA256"; allow = os.path.join(S, "fx4-allow.tsv")
open(allow, "w").write("%s\tauthorization\t%s\texample header\n" % (rel, hashlib.sha256(m).hexdigest()))
for label, body in (("documented example line", "Authorization" + ": AWS4-HMAC-SHA256\n" + "Credential=" + "AKIAIOSFODNN7EXAMPLE" + "/20220830/us-east-1/ec2/aws4_request,\n"),
                    ("other key id, same scheme", "Authorization" + ": AWS4-HMAC-SHA256 " + "Credential=" + "AKIA" + "ZZZZZZZZZZZZZZZZ" + "/20260101/us-east-1/s3/aws4_request,\n")):
    open(p, "w").write(body)
    q = subprocess.run([sys.executable, "-B", INST, "--files", rel, "--allow", allow], capture_output=True, text=True, cwd=D3)
    print("  %-28s rc=%d %s" % (label, q.returncode, " | ".join(q.stdout.strip().splitlines())))
