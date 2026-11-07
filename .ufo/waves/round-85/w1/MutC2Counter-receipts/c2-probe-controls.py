#!/usr/bin/env python3
"""Round-85 C2 probe controls (addendum to controls/c2-controls-r85.sh).

The frozen controls exercise only pricing forgeries plus one shape-valid but
pricing-empty exemplar: they never present the counter with a package that
satisfies a limb, so every loosening inside the E1/E2/E5 success paths (and the
E3/E4 success comparisons) is invisible to them. This suite adds one positive
anchor plus 15 negative probes, each designed so the frozen counter's limb
verdict is the correct, unique outcome. It is an oracle, not a mutant: run it
against the landing counter and it must print PROBE-RESULT exit=0; run it
against a suspected loosening and the named probe goes red.

Usage:
  python3 -B c2-probe-controls.py --lane LANE --counter COUNTER --scratch DIR
Exit: 0 every probe matches its oracle; 1 any probe mismatched; 2 usage.
Writes only under --scratch.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys


def sha(b):
    return hashlib.sha256(b).hexdigest()


def w(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        fh.write(data)


def run(counter, args, cwd):
    p = subprocess.run([sys.executable, "-B", counter] + args, cwd=cwd,
                       capture_output=True, text=True, timeout=120)
    limbs = {}
    result = None
    for ln in p.stdout.splitlines():
        if ln.startswith("LIMB "):
            _, name, status = ln.split()[:3]
            limbs[name] = status
        elif ln.startswith("E2E-RESULT "):
            result = ln.split()[1]
    return {"rc": p.returncode, "limbs": limbs, "result": result,
            "out": p.stdout.strip()}


GATE_RC0_BAD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=0 fail=8 verdict=DEFECT exit=0")\nsys.exit(0)\n'
GATE_RC3_GOOD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=3")\nsys.exit(3)\n'
GATE_RC1_BAD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=7 fail=1 verdict=DEFECT exit=1")\nsys.exit(1)\n'
GATE_RC0_GOOD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0")\nsys.exit(0)\n'

PRICE = ("# probe\n## Pricing\nprice-program: curl\nprice-severity: Medium\n"
         "price-reward-at-disclosure: 2400 USD\nprice-platform-bounty-flag: false\n"
         "price-reward-current-policy: none\nprice-cvss: not-set-by-vendor\n"
         'price-kev: not-listed (CVE id absent from the round-35 S052 capture)\n'
         "price-cve: CVE-2023-28319\n"
         "> Severity: Medium\n> Bug bounty: 2400 USD\n"
         "> There is no bug bounty and the curl project never offers rewards for "
         "reported vulnerabilities.\n## Next\n")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    counter = os.path.abspath(a.counter)
    S = os.path.abspath(a.scratch)
    os.makedirs(S, exist_ok=True)
    SNAP = os.path.join(lane, "corpus/source-snapshots")
    man = json.load(open(os.path.join(SNAP, "round-85/manifest.json")))
    REC = {s["id"]: s["sha256"] for s in man["sources"]}
    blob = {"S119": open(os.path.join(SNAP, "round-85/S119.txt"), "rb").read(),
            "S120": open(os.path.join(SNAP, "round-85/S120.txt"), "rb").read(),
            "S121": open(os.path.join(SNAP, "round-85/S121.txt"), "rb").read()}
    kev = open(os.path.join(SNAP, "round-35/S052.txt"), "rb").read()

    def stub(name, text):
        p = os.path.join(S, "gate-stubs", name + ".py")
        w(p, text)
        return p

    def lane_stub(name, gate, s120=None, manifest_sha=None):
        d = os.path.join(S, "lanes", name)
        for sid, b in blob.items():
            w(os.path.join(d, "corpus/source-snapshots/round-85", sid + ".txt"),
              s120 if (sid == "S120" and s120) else b)
        w(os.path.join(d, "corpus/source-snapshots/round-35/S052.txt"), kev)
        m = json.loads(json.dumps(man))
        if manifest_sha:
            for s in m["sources"]:
                if s["id"] == manifest_sha[0]:
                    s["sha256"] = manifest_sha[1]
        w(os.path.join(d, "corpus/source-snapshots/round-85/manifest.json"),
          json.dumps(m, indent=1))
        os.makedirs(os.path.join(d, "corpus/instruments"), exist_ok=True)
        shutil.copyfile(gate, os.path.join(d, "corpus/instruments/claim-package-check.py"))
        w(os.path.join(d, "LOG.md"), "# stub log\n")
        w(os.path.join(d, "SHONEN.md"), "# stub shonen\n")
        return d

    def pkg_at(d, artifacts=("S119", "S120"), recorded=None, symlink_sid=None):
        os.makedirs(os.path.join(d, "evidence"), exist_ok=True)
        ents = []
        for sid in artifacts:
            nm = sid + ".txt"
            target = os.path.join(d, "evidence", nm)
            if symlink_sid == sid:
                os.symlink(os.path.join(SNAP, "round-85", nm), target)
            else:
                w(target, blob[sid])
            ents.append({"path": nm, "sha256": (recorded or {}).get(sid, REC[sid])})
        w(os.path.join(d, "report.md"), PRICE)
        w(os.path.join(d, "evidence/manifest.json"),
          json.dumps({"schema_version": "evidence-manifest/v1",
                      "artifacts": ents}, indent=1))
        return d

    g0bad = stub("rc0_bad", GATE_RC0_BAD)
    g3good = stub("rc3_good", GATE_RC3_GOOD)
    g1bad = stub("rc1_bad", GATE_RC1_BAD)
    g0good = stub("rc0_good", GATE_RC0_GOOD)
    l_e1a = lane_stub("e1-rc0bad", g0bad)
    l_e1b = lane_stub("e1-rc3good", g3good)
    l_lie = lane_stub("manifest-lie", g1bad, manifest_sha=("S119", "f" * 64))
    hi = blob["S120"].replace(b"Severity: Medium", b"Severity: High")
    assert hi != blob["S120"]
    l_sev = lane_stub("s120-high", g1bad, s120=hi)
    l_log = lane_stub("log-only", g1bad)
    l_out = lane_stub("outside", g1bad)
    l_e1only = lane_stub("e1only", g1bad)
    l_pos = lane_stub("positive", g0good)

    p = os.path.join(S, "pkgs")
    v = pkg_at(os.path.join(p, "valid"))
    bogus = pkg_at(os.path.join(p, "bogus-recorded"),
                   recorded={"S119": "0" * 64, "S120": "0" * 64})
    one = pkg_at(os.path.join(p, "one-source"), artifacts=("S119",))
    sym = pkg_at(os.path.join(p, "symlink"), symlink_sid="S119")
    lie = pkg_at(os.path.join(p, "manifest-lie"))
    for name, d in (
            ("log-only", os.path.join(l_log, "corpus/practice/curl-h1-1913733")),
            ("e1only", os.path.join(l_e1only, "corpus/practice/curl-h1-1913733")),
            ("positive", os.path.join(l_pos, "corpus/practice/curl-h1-1913733"))):
        shutil.copytree(v, d)
    w(os.path.join(l_log, "LOG.md"), "# stub log\n- task: corpus/practice/curl-h1-1913733\n")
    w(os.path.join(l_e1only, "LOG.md"), "# stub log\n- corpus/practice/curl-h1-1913733\n")
    w(os.path.join(l_e1only, "SHONEN.md"), "# shonen\n- corpus/practice/curl-h1-1913733\n")
    w(os.path.join(l_pos, "LOG.md"), "# stub log\n- corpus/practice/curl-h1-1913733\n")
    w(os.path.join(l_pos, "SHONEN.md"), "# shonen\n- corpus/practice/curl-h1-1913733\n")
    out_pkg = pkg_at(os.path.join(S, "outside-pkg"))
    rel = os.path.relpath(os.path.realpath(out_pkg), os.path.realpath(l_out))
    assert rel.startswith("..")
    w(os.path.join(l_out, "LOG.md"), "# stub log\n- %s\n" % rel)
    w(os.path.join(l_out, "SHONEN.md"), "# shonen\n- %s\n" % rel)

    reps = {}
    for name, text in (
            ("reward-case", PRICE.replace("price-reward-at-disclosure: 2400 USD",
                                          "price-reward-at-disclosure: 2400 usd")),
            ("reward-eur", PRICE.replace("price-reward-at-disclosure: 2400 USD",
                                         "price-reward-at-disclosure: 2400 EUR")),
            ("two-quotes", "# probe\n## Pricing\nprice-program: curl\n"
             "price-severity: Medium\nprice-reward-at-disclosure: 2400 USD\n"
             "price-platform-bounty-flag: false\nprice-reward-current-policy: none\n"
             "price-cvss: not-set-by-vendor\n"
             'price-kev: not-listed (CVE id absent from the round-35 S052 capture)\n'
             "price-cve: CVE-2023-28319\n> Severity: Medium\n"
             "> Bug bounty: 2400 USD\n## Next\n"),
            ("ws-quote", PRICE.replace("> Severity: Medium", "> Severity:  Medium")
             .replace("> Bug bounty: 2400 USD", "> Bug bounty:  2400 USD")),
            ("kev-quote", PRICE.replace("> Bug bounty: 2400 USD",
                                        '> Bug bounty: 2400 USD\n> "vendorProject": "Arista",'))):
        reps[name] = os.path.join(S, "reports", name + ".md")
        w(reps[name], text)
    assert kev.find(b'"vendorProject": "Arista"') >= 0
    for sid in blob:
        assert blob[sid].find(b'"vendorProject": "Arista"') < 0

    probes = [
        ("gate_rc0_bad", ["--lane", l_e1a, "--pkg", v], "E1", "FAIL"),
        ("gate_rc3_good", ["--lane", l_e1b, "--pkg", v], "E1", "FAIL"),
        ("bogus_recorded_sha", ["--lane", lane, "--pkg", bogus], "E2", "FAIL"),
        ("manifest_lie", ["--lane", l_lie, "--pkg", lie], "E2", "FAIL"),
        ("one_source", ["--lane", lane, "--pkg", one], "E2", "FAIL"),
        ("symlink_evidence", ["--lane", lane, "--pkg", sym], "E2", "FAIL"),
        ("s120_disagrees", ["--lane", l_sev, "--pricing-only", reps["two-quotes"]], "E3", "FAIL"),
        ("reward_case", ["--lane", lane, "--pricing-only", reps["reward-case"]], "E3", "FAIL"),
        ("reward_currency", ["--lane", lane, "--pricing-only", reps["reward-eur"]], "E3", "FAIL"),
        ("two_quotes", ["--lane", lane, "--pricing-only", reps["two-quotes"]], "E4", "FAIL"),
        ("ws_quote", ["--lane", lane, "--pricing-only", reps["ws-quote"]], "E4", "pass"),
        ("kev_quote", ["--lane", lane, "--pricing-only", reps["kev-quote"]], "E4", "FAIL"),
        ("log_only", ["--lane", l_log, "--pkg", os.path.join(l_log, "corpus/practice/curl-h1-1913733")], "E5", "FAIL"),
        ("outside_lane", ["--lane", l_out, "--pkg", out_pkg], "E5", "FAIL"),
        ("only_e1_fails", ["--lane", l_e1only, "--pkg", os.path.join(l_e1only, "corpus/practice/curl-h1-1913733")], "RESULT", "fail"),
        ("positive_full", ["--lane", l_pos, "--pkg", os.path.join(l_pos, "corpus/practice/curl-h1-1913733")], "RESULT", "pass"),
    ]
    bad = 0
    for name, args, limb, want in probes:
        r = run(counter, args, lane)
        got = r["result"] if limb == "RESULT" else r["limbs"].get(limb)
        ok = got == want and (want != "pass" or r["rc"] == 0)
        bad += 0 if ok else 1
        print("PROBE %s %s limb=%s expected=%s got=%s rc=%d"
              % (name, "pass" if ok else "FAIL", limb, want, got, r["rc"]))
        if not ok:
            print("  transcript: " + " | ".join(r["out"].splitlines()))
    print("PROBE-RESULT pass=%d/%d exit=%d" % (len(probes) - bad, len(probes), 0 if not bad else 1))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
