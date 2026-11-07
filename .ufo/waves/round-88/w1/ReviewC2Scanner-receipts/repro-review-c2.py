#!/usr/bin/env python3
"""Re-runnable fixtures for the round-88 C2 review (capture-secret-scan extension).

Every value is generated here (repeated hex, base64 of range(32), repeated
letters); no planted or real credential is used. Fixtures are written under the
WORK argument only, never in the wave directory, and the output prints case
name, rc, detected shape names and a 16-hex digest of the fixture text, never a
matched value.

Usage:
  python3 -B repro-review-c2.py WORK [--only SUBSTR]

The instrument under test is read from the lane with `git show` (read-only) at
the C2 landing commit; nothing in the lane is written.
"""
import base64
import hashlib
import importlib.util
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "b43dc2154bc09470da2209fb626021da3af3593e"
FILES = ("capture-secret-scan.py", "claim-package-check.py", "capture-secret-allow.tsv")

HEX128 = "deadbeef" * 16
HEXU = "DEADBEEF" * 16
B64 = base64.b64encode(bytes(range(32))).decode()          # 44 chars, one '=' pad
B64_PCT = B64.replace("+", "%2B").replace("/", "%2F").replace("=", "%3D")
AZ = "https://a.blob.core.windows.net/c/b.txt"
S127_ORDER = ("?sp=rw&st=2026-11-07T00:00:00Z&se=2026-11-08T00:00:00Z"
              "&sip=198.51.100.10-198.51.100.20&spr=https&sv=2022-11-02&sr=b")


def cases():
    """(name, text, want) with want a shape set, or None to only observe."""
    c = [
        # GCS: claim-implied behaviour
        ("gcs_hex128_hit", "X-Goog-Signature=" + HEX128, {"gcs-signed-url-signature"}),
        ("gcs_hex128_upper_hit", "X-Goog-Signature=" + HEXU, {"gcs-signed-url-signature"}),
        ("gcs_hex63_miss", "X-Goog-Signature=" + HEX128[:63], set()),
        ("gcs_header_colon_hit", "X-Goog-Signature: " + HEX128, {"gcs-signed-url-signature"}),
        ("gcs_json_key_hit", '{"X-Goog-Signature": "' + HEX128 + '"}', {"gcs-signed-url-signature"}),
        # GCS: named limits and observations
        ("gcs_pct_name_miss", "X%2DGoog-Signature=" + HEX128, set()),
        ("gcs_wrapped_newline_miss", "X-Goog-Signature=" + HEX128[:12] + "\n" + HEX128[12:], None),
        ("gcs_json_escaped_newline_miss", '{"X-Goog-Signature": "' + HEX128[:60] + '\\n' + HEX128[60:] + '"}', None),
        ("gcs_base64_miss", "X-Goog-Signature=" + base64.b64encode(bytes(range(64))).decode(), None),
        ("gcs_prefixed_name_fp", "Not-X-Goog-Signature=" + HEX128, None),
        # Azure: claim-implied behaviour that holds
        ("az_sv_first_amp_hit", AZ + "?sp=r&se=2026-11-08T00:00:00Z&sv=2022-11-02&sr=b&sig=" + B64, {"azure-sas-signature"}),
        ("az_doc_order_amp_hit", AZ + S127_ORDER + "&sig=" + B64, {"azure-sas-signature"}),
        ("az_doc_order_ampamp_hit", AZ + S127_ORDER.replace("&", "&amp;") + "&amp;sig=" + B64, {"azure-sas-signature"}),
        ("az_sig_first_amp_mid_hit", AZ + "?sp=r&amp;sig=" + B64 + "&amp;sv=2022-11-02", {"azure-sas-signature"}),
        ("az_sv_first_u0026_first_param_hit", AZ + "?sv=2022-11-02\\u0026sr=b\\u0026sig=" + B64, {"azure-sas-signature"}),
        ("az_sig_first_u0026_first_param_hit", AZ + "?sig=" + B64 + "\\u0026sv=2022-11-02", {"azure-sas-signature"}),
        ("az_sig_40_hit", AZ + "?sv=2022-11-02&sig=" + ("Q" * 39) + "z", {"azure-sas-signature"}),
        ("az_sig_44_hit", AZ + "?sv=2022-11-02&sr=b&sig=" + B64, {"azure-sas-signature"}),
        ("az_sig_pct_encoded_hit", AZ + "?sv=2022-11-02&sr=b&sig=" + B64_PCT, {"azure-sas-signature"}),
        ("az_sig_39_miss", AZ + "?sv=2022-11-02&sig=" + ("Q" * 38) + "z", set()),
        ("az_no_sv_miss", AZ + "?sp=r&sig=" + B64, set()),
        ("az_placeholder_miss", AZ + S127_ORDER + "&sig=<signature>", set()),
        # Azure: the frozen statement says "either order, &/&amp;/\u0026 separators"
        ("az_doc_order_u0026_f1", AZ + S127_ORDER.replace("&", "\\u0026") + "\\u0026sig=" + B64, {"azure-sas-signature"}),
        ("az_sig_first_u0026_mid_f1", AZ + "?sp=r\\u0026sig=" + B64 + "\\u0026sv=2022-11-02", {"azure-sas-signature"}),
        # Azure: "in the same query" limits
        ("az_20_params_hit", AZ + "?sv=2022-11-02" + "".join("&ab%s=x" % chr(97 + i) for i in range(20)) + "&sig=" + B64, {"azure-sas-signature"}),
        ("az_21_params_miss", AZ + "?sv=2022-11-02" + "".join("&ab%s=x" % chr(97 + i) for i in range(21)) + "&sig=" + B64, {"azure-sas-signature"}),
        ("az_longname_between_miss", AZ + "?sv=2022-11-02&x-ms-version=2020-08-04&sig=" + B64, {"azure-sas-signature"}),
        # Azure: adjacent encodings / false-positive surface
        ("az_sv_first_pct26_miss", AZ + "?sp=r%26se=2026-11-08%26sv=2022-11-02%26sr=b%26sig=" + B64, None),
        ("az_nonazure_sv_sig_fp", "https://example.com/x?sv=2026-11-07&sig=" + ("Q" * 39) + "z", None),
    ]
    return c


def extract(work):
    d = os.path.join(work, "inst")
    os.makedirs(d, exist_ok=True)
    for f in FILES:
        out = subprocess.run(["git", "-C", LANE, "show", REV + ":corpus/instruments/" + f],
                             capture_output=True, check=True).stdout
        with open(os.path.join(d, f), "wb") as fh:
            fh.write(out)
    return d


def main(argv):
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
    work = argv[0]
    inst = extract(work)
    fxd = os.path.join(work, "fx")
    os.makedirs(fxd, exist_ok=True)
    bad = 0
    total = 0
    for name, text, want in cases():
        if only and only not in name:
            continue
        p = os.path.join(fxd, name + ".txt")
        with open(p, "wb") as fh:
            fh.write(text.encode() + b"\n")
        r = subprocess.run([sys.executable, "-B", os.path.join(inst, FILES[0]), "--files", p],
                           capture_output=True, text=True)
        got = {ln.split("shape=")[1].split()[0] for ln in r.stdout.splitlines() if ln.startswith("HIT ")}
        if want is None:
            verdict = "observe"
        else:
            total += 1
            ok = got == want
            bad += not ok
            verdict = "ok" if ok else "MISMATCH"
        print("%-36s rc=%d shapes=%-30s digest=%s %s"
              % (name, r.returncode, ",".join(sorted(got)) or "none",
                 hashlib.sha256(text.encode()).hexdigest()[:16], verdict))
    spec = importlib.util.spec_from_file_location("c2scan", os.path.join(inst, FILES[0]))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    scope = [
        ("corpus/practice/pkg/evidence/a.txt", True),
        ("corpus/practice/pkg/evidence/sub/dir/a.txt", True),
        ("corpus/practice/evidence/a.txt", False),
        ("corpus/practice/pkg/report.md", False),
        ("corpus/practice/pkg/evidenceX/a.txt", False),
        (".ufo/waves/round-88/w1/ReviewC2Scanner.md", False),
        (".ufo/waves/round-88/w1/ReviewC2Scanner-receipts/x.json", True),
    ]
    for p, want in scope:
        got = mod.is_capture_path(p)
        ok = got == want
        bad += not ok
        print("SCOPE %-56s want=%-5s got=%-5s %s" % (p, want, got, "ok" if ok else "MISMATCH"))
    print("REPRO-RESULT mismatches=%d claimed_cases=%d" % (bad, total))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
