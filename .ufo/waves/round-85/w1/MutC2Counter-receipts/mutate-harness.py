#!/usr/bin/env python3
"""Round-85 C2 mutation probe: single-point mutants of c2/e2e-check.py scored
against the frozen pre-freeze controls (controls/c2-controls-r85.sh) and a set
of new positive/negative probes that exercise the success paths the frozen
controls leave untested.  Read-only over the lane; every write is under SCRATCH.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r85/MutC2Counter"
FROZEN = os.path.join(LANE, ".ufo/waves/round-85/c2/e2e-check.py")
FROZEN_SHA = "a6f238022d0d263403b46221fa9ca959b91c8941157c3275eb0ae5ae76a6814d"
SNAP = os.path.join(LANE, "corpus/source-snapshots")
MAN = json.load(open(os.path.join(SNAP, "round-85/manifest.json")))
REC = {s["id"]: s["sha256"] for s in MAN["sources"]}
S119B = open(os.path.join(SNAP, "round-85/S119.txt"), "rb").read()
S120B = open(os.path.join(SNAP, "round-85/S120.txt"), "rb").read()
S121B = open(os.path.join(SNAP, "round-85/S121.txt"), "rb").read()
S052B = open(os.path.join(SNAP, "round-35/S052.txt"), "rb").read()


def w(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        fh.write(data)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(counter, args, cwd=LANE):
    p = subprocess.run([sys.executable, "-B", counter] + args, cwd=cwd,
                       capture_output=True, text=True, timeout=120)
    limbs = []
    result = None
    for ln in p.stdout.splitlines():
        if ln.startswith("LIMB "):
            _, name, status = ln.split()[:3]
            limbs.append((name, status))
        elif ln.startswith("E2E-RESULT "):
            result = ln.split()[1]
    return {"rc": p.returncode, "limbs": limbs, "result": result,
            "out": p.stdout.strip().splitlines(), "err": p.stderr.strip()}


# ---------------------------------------------------------------- frozen controls
def pricing_report(name, sev="Medium", rwd="2400 USD", flg="false",
                   pol="none", cvs="not-set-by-vendor",
                   kev="not-listed (CVE id absent from the round-35 S052 capture)",
                   cve="CVE-2023-28319",
                   q3="There is no bug bounty and the curl project never offers "
                      "rewards for reported vulnerabilities."):
    return ("# pricing control %s\n## Pricing\n"
            "price-program: curl\n"
            "price-severity: %s\n"
            "price-reward-at-disclosure: %s\n"
            "price-platform-bounty-flag: %s\n"
            "price-reward-current-policy: %s\n"
            "price-cvss: %s\n"
            "price-kev: %s\n"
            "price-cve: %s\n"
            "> Severity: Medium\n> Bug bounty: 2400 USD\n> %s\n## Next\n"
            % (name, sev, rwd, flg, pol, cvs, kev, cve, q3))


CONTROLS = [
    ("donothing", ("pkg", os.path.join(LANE, "corpus/practice/curl-h1-1913733"))),
    ("exemplar-copy", ("pkg", os.path.join(S, "fx/exemplar"))),
    ("positive-pricing", ("pricing", pricing_report("positive-pricing"))),
    ("forged-severity", ("pricing", pricing_report("forged-severity", sev="High"))),
    ("forged-reward-exemplar", ("pricing", pricing_report("forged-reward-exemplar", rwd="505 USD"))),
    ("forged-platform-flag", ("pricing", pricing_report("forged-platform-flag", flg="true"))),
    ("forged-current-policy", ("pricing", pricing_report("forged-current-policy", pol="500 USD"))),
    ("forged-cvss", ("pricing", pricing_report("forged-cvss", cvs="6.3"))),
    ("forged-kev", ("pricing", pricing_report("forged-kev", kev="listed"))),
    ("forged-cve", ("pricing", pricing_report("forged-cve", cve="CVE-2025-9086"))),
    ("forged-quote", ("pricing", pricing_report(
        "forged-quote", q3="The curl project pays 2400 USD for every Medium report."))),
]

EXPECT = {
    "donothing": {"rc": 1, "result": "fail",
                  "limbs": [("E1", "FAIL"), ("E2", "FAIL"), ("E3", "FAIL"),
                            ("E4", "FAIL"), ("E5", "FAIL")]},
    "exemplar-copy": {"rc": 1, "result": "fail",
                      "limbs": [("E1", "pass"), ("E2", "FAIL"), ("E3", "FAIL"),
                                ("E4", "FAIL"), ("E5", "FAIL")]},
    "positive-pricing": {"rc": 0, "result": "pass",
                         "limbs": [("E3", "pass"), ("E4", "pass")]},
    "forged-severity": {"rc": 1, "result": "fail",
                        "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-reward-exemplar": {"rc": 1, "result": "fail",
                               "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-platform-flag": {"rc": 1, "result": "fail",
                             "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-current-policy": {"rc": 1, "result": "fail",
                              "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-cvss": {"rc": 1, "result": "fail",
                    "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-kev": {"rc": 1, "result": "fail",
                   "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-cve": {"rc": 1, "result": "fail",
                   "limbs": [("E3", "FAIL"), ("E4", "pass")]},
    "forged-quote": {"rc": 1, "result": "fail",
                     "limbs": [("E3", "pass"), ("E4", "FAIL")]},
}


def control_args(ctl):
    kind, payload = ctl
    if kind == "pkg":
        return ["--lane", LANE, "--pkg", payload]
    path = os.path.join(S, "fx", "pricing-%s.md" % payload.split("\n")[0].split()[-1])
    w(path, payload)
    return ["--lane", LANE, "--pricing-only", path]


def score(counter):
    out = {}
    for name, ctl in CONTROLS:
        out[name] = run(counter, control_args(ctl))
    return out


def sig(res):
    return (res["rc"], tuple(res["limbs"]))


# ---------------------------------------------------------------- mutants
MUTANTS = [
    # id, old, new, expectation note
    ("sev_case_sensitive",
     "            if g.lower() != w:", "            if g != w:",
     "E3 severity compared without lowercasing"),
    ("fields_drop_cve",
     '"reward-current-policy", "cvss", "kev", "cve")',
     '"reward-current-policy", "cvss", "kev")',
     "cve dropped from FIELDS"),
    ("flag_always_true",
     '"platform-bounty-flag": "true" if s119["has_bounty?"] is True else "false",',
     '"platform-bounty-flag": "true",',
     "platform flag hardwired true"),
    ("kev_reverse_prefix",
     'if not g.startswith(w) or (w == "listed" and g.startswith("not-listed")):',
     "if not w.startswith(g):",
     "kev comparison reversed"),
    ("e4_ignore_missing",
     'out.append(("E4", len(quotes) >= 3 and not miss,',
     'out.append(("E4", len(quotes) >= 3,',
     "E4 ignores quotes absent from the snapshots"),
    ("e4_pool_s119_only",
     "    }, (json.dumps(s119), s120, s121)",
     "    }, (json.dumps(s119),)",
     "quote pool loses S120/S121"),
    ("e1_rc_only",
     'ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout',
     "ok = p.returncode == 0",
     "E1 drops the verdict token"),
    ("e1_verdict_only",
     'ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout',
     'ok = "verdict=WELL-FORMED" in p.stdout',
     "E1 drops the gate exit code"),
    ("e2_drop_recorded_sha",
     'if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:',
     "if b == snap and h == rec[sid]:",
     "E2 drops the package-recorded sha256"),
    ("e2_drop_manifest_binding",
     'if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:',
     'if b == snap and str(art.get("sha256", "")).lower() == h:',
     "E2 drops the round-85 manifest sha256 binding"),
    ("e2_one_source",
     'limbs.append(("E2", found == {"S119", "S120"}, "bound=%s" % (",".join(sorted(found)) or "none")))',
     'limbs.append(("E2", "S119" in found, "bound=%s" % (",".join(sorted(found)) or "none")))',
     "E2 needs only S119"),
    ("e2_symlink_evidence",
     "            if not os.path.isfile(ap) or os.path.islink(ap):",
     "            if not os.path.isfile(ap):",
     "E2 follows symlinked evidence"),
    ("sev_ignore_s120",
     '"severity": s119["severity_rating"].lower() if sev and sev.group(1).lower() == s119["severity_rating"].lower() else None,',
     '"severity": s119["severity_rating"].lower(),',
     "severity derived from S119 without the S120 agreement"),
    ("reward_case_insensitive",
     "        elif g != w:\n            bad.append(f)",
     '        elif f == "reward-at-disclosure":\n'
     "            if g.lower() != w.lower():\n"
     "                bad.append(f)\n"
     "        elif g != w:\n            bad.append(f)",
     "reward compared case-insensitively"),
    ("e4_threshold_1",
     'out.append(("E4", len(quotes) >= 3 and not miss,',
     'out.append(("E4", len(quotes) >= 1 and not miss,',
     "E4 quote threshold 3 -> 1"),
    ("e4_raw_no_norm",
     'miss = [q for q in quotes if not any(norm(q) in p for p in pool)]',
     'miss = [q for q in quotes if not any(q in s for s in snaps)]',
     "E4 compares raw text (no whitespace collapse)"),
    ("e4_pool_includes_kev",
     "    pool = [norm(s) for s in snaps]",
     '    pool = [norm(s) for s in snaps + (rd(os.path.join(lane, "corpus", "source-snapshots", "round-35", "S052.txt")),)]',
     "E4 pool gains the S052 KEV capture"),
    ("e5_or",
     'ok = not rel.startswith("..") and rel in log and rel in sh',
     'ok = not rel.startswith("..") and (rel in log or rel in sh)',
     "E5 accepts either LOG.md or SHONEN.md"),
    ("allok_ignores_e1",
     "    allok = all(ok for _, ok, _ in limbs)",
     '    allok = all(ok for n, ok, _ in limbs if n != "E1")',
     "overall verdict ignores limb E1"),
    ("kev_dead_guard",
     'if not g.startswith(w) or (w == "listed" and g.startswith("not-listed")):',
     "if not g.startswith(w):",
     "removes the second kev conjunct"),
]


def make_mutant(mid, old, new):
    base = open(FROZEN, encoding="utf-8").read()
    n = base.count(old)
    assert n == 1, "%s: old string occurs %d times" % (mid, n)
    body = base.replace(old, new)
    assert body != base
    path = os.path.join(S, "mut", mid + ".py")
    w(path, body)
    return path


# ---------------------------------------------------------------- probes
def build_lane_stub(dst, gate_src, s120=None, manifest_sha=None):
    os.makedirs(os.path.join(dst, "corpus/source-snapshots/round-85"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus/source-snapshots/round-35"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus/instruments"), exist_ok=True)
    w(os.path.join(dst, "corpus/source-snapshots/round-85/S119.txt"), S119B)
    w(os.path.join(dst, "corpus/source-snapshots/round-85/S120.txt"),
      s120 if s120 is not None else S120B)
    w(os.path.join(dst, "corpus/source-snapshots/round-85/S121.txt"), S121B)
    w(os.path.join(dst, "corpus/source-snapshots/round-35/S052.txt"), S052B)
    man = json.loads(json.dumps(MAN))
    if manifest_sha:
        for s in man["sources"]:
            if s["id"] == manifest_sha[0]:
                s["sha256"] = manifest_sha[1]
    w(os.path.join(dst, "corpus/source-snapshots/round-85/manifest.json"),
      json.dumps(man, indent=1))
    shutil.copyfile(gate_src, os.path.join(dst, "corpus/instruments/claim-package-check.py"))
    w(os.path.join(dst, "LOG.md"), "# stub log\n")
    w(os.path.join(dst, "SHONEN.md"), "# stub shonen\n")


def gate_stub(name, code_and_out):
    p = os.path.join(S, "gate-stubs", name + ".py")
    w(p, code_and_out)
    return p


GATE_RC0_BAD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=0 fail=8 verdict=DEFECT exit=0")\nsys.exit(0)\n'
GATE_RC3_GOOD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=3")\nsys.exit(3)\n'
GATE_RC1_BAD = '#!/usr/bin/env python3\nimport sys\nprint("package=x rules=8 pass=7 fail=1 verdict=DEFECT exit=1")\nsys.exit(1)\n'

VALID_PRICE = pricing_report("probe")


def valid_pkg(dst, artifacts=("S119", "S120"), recorded=None, manifest_entries=None):
    """A package whose evidence bytes are the committed snapshots."""
    os.makedirs(os.path.join(dst, "evidence"), exist_ok=True)
    entries = []
    payload = {"S119": (S119B, "S119.txt"), "S120": (S120B, "S120.txt")}
    for sid in artifacts:
        blob, nm = payload[sid]
        w(os.path.join(dst, "evidence", nm), blob)
        entries.append({"path": nm,
                        "sha256": (recorded or {}).get(sid, REC[sid])})
    w(os.path.join(dst, "report.md"), VALID_PRICE)
    w(os.path.join(dst, "evidence/manifest.json"),
      json.dumps({"schema_version": "evidence-manifest/v1", "artifacts": entries}, indent=1))
    return dst


def build_probes():
    P = os.path.join(S, "pr")
    pkg = valid_pkg(os.path.join(P, "pkg-valid"))
    # gate stubs
    g0 = gate_stub("rc0_bad", GATE_RC0_BAD)
    g3 = gate_stub("rc3_good", GATE_RC3_GOOD)
    g1 = gate_stub("rc1_bad", GATE_RC1_BAD)
    # E1 probes: lane with a stub gate; pkg exists but other limbs may fail.
    lane_e1a = os.path.join(P, "lane-e1-rc0bad")
    build_lane_stub(lane_e1a, g0)
    lane_e1b = os.path.join(P, "lane-e1-rc3good")
    build_lane_stub(lane_e1b, g3)
    # E2 probes
    pkg_bogus = valid_pkg(os.path.join(P, "pkg-bogus-recorded"),
                          recorded={"S119": "0" * 64, "S120": "0" * 64})
    pkg_one = valid_pkg(os.path.join(P, "pkg-one-source"), artifacts=("S119",))
    pkg_sym = os.path.join(P, "pkg-symlink")
    valid_pkg(pkg_sym)
    os.remove(os.path.join(pkg_sym, "evidence", "S119.txt"))
    os.symlink(os.path.join(SNAP, "round-85/S119.txt"),
               os.path.join(pkg_sym, "evidence", "S119.txt"))
    lane_lie = os.path.join(P, "lane-manifest-lie")
    build_lane_stub(lane_lie, g1, manifest_sha=("S119", "f" * 64))
    pkg_lie = valid_pkg(os.path.join(P, "pkg-manifest-lie"))
    # E3 severity probe: synthetic S120 that disagrees with S119
    s120_hi = S120B.replace(b"Severity: Medium", b"Severity: High")
    assert s120_hi != S120B
    lane_sev = os.path.join(P, "lane-s120-high")
    build_lane_stub(lane_sev, g1, s120=s120_hi)
    # E3 reward probes / E4 probes: real lane, pricing-only
    rep_reward_case = pricing_report("probe-reward-case", rwd="2400 usd")
    rep_reward_cur = pricing_report("probe-reward-eur", rwd="2400 EUR")
    rep_two = ("# probe\n## Pricing\nprice-program: curl\nprice-severity: Medium\n"
               "price-reward-at-disclosure: 2400 USD\nprice-platform-bounty-flag: false\n"
               "price-reward-current-policy: none\nprice-cvss: not-set-by-vendor\n"
               'price-kev: not-listed (CVE id absent from the round-35 S052 capture)\n'
               "price-cve: CVE-2023-28319\n> Severity: Medium\n> Bug bounty: 2400 USD\n## Next\n")
    rep_ws = (VALID_PRICE.replace("> Severity: Medium", "> Severity:  Medium")
              .replace("> Bug bounty: 2400 USD",
                       "> Bug bounty:  2400 USD"))
    rep_kev = (VALID_PRICE.replace(
        "> Bug bounty: 2400 USD",
        '> Bug bounty: 2400 USD\n> "vendorProject": "Arista",'))
    assert S052B.find(b'"vendorProject": "Arista"') >= 0
    assert S119B.find(b'"vendorProject": "Arista"') < 0
    assert S120B.find(b'"vendorProject": "Arista"') < 0
    assert S121B.find(b'"vendorProject": "Arista"') < 0
    paths = {}
    for name, text in (("reward-case", rep_reward_case), ("reward-eur", rep_reward_cur),
                       ("two-quotes", rep_two), ("ws-quote", rep_ws), ("kev-quote", rep_kev)):
        paths[name] = os.path.join(P, "rep-" + name + ".md")
        w(paths[name], text)
    # E5 probes: lane stubs that name the package in only one file / outside lane
    lane_log_only = os.path.join(P, "lane-log-only")
    build_lane_stub(lane_log_only, g1)
    dst = os.path.join(lane_log_only, "corpus/practice/curl-h1-1913733")
    shutil.copytree(pkg, dst)
    w(os.path.join(lane_log_only, "LOG.md"),
      "# stub log\n- task: corpus/practice/curl-h1-1913733\n")
    lane_outside = os.path.join(P, "lane-outside")
    build_lane_stub(lane_outside, g1)
    outside_pkg = valid_pkg(os.path.join(P, "outside-pkg"))
    rel = os.path.relpath(os.path.realpath(outside_pkg), os.path.realpath(lane_outside))
    assert rel.startswith("..")
    w(os.path.join(lane_outside, "LOG.md"), "# stub log\n- task: %s\n" % rel)
    w(os.path.join(lane_outside, "SHONEN.md"), "# stub shonen\n- %s\n" % rel)
    # only-E1-fails probe: every limb passes except the gate
    lane_e1only = os.path.join(P, "lane-e1only")
    build_lane_stub(lane_e1only, g1)
    dst2 = os.path.join(lane_e1only, "corpus/practice/curl-h1-1913733")
    shutil.copytree(pkg, dst2)
    w(os.path.join(lane_e1only, "LOG.md"),
      "# stub log\n- task: corpus/practice/curl-h1-1913733\n")
    w(os.path.join(lane_e1only, "SHONEN.md"),
      "# stub shonen\n- corpus/practice/curl-h1-1913733\n")
    return {
        "gate_rc0_bad": (["--lane", lane_e1a, "--pkg", pkg], "E1"),
        "gate_rc3_good": (["--lane", lane_e1b, "--pkg", pkg], "E1"),
        "bogus_recorded_sha": (["--lane", LANE, "--pkg", pkg_bogus], "E2"),
        "manifest_lie": (["--lane", lane_lie, "--pkg", pkg_lie], "E2"),
        "one_source": (["--lane", LANE, "--pkg", pkg_one], "E2"),
        "symlink_evidence": (["--lane", LANE, "--pkg", pkg_sym], "E2"),
        "s120_disagrees": (["--lane", lane_sev, "--pricing-only", paths["two-quotes"]], "E3"),
        "reward_case": (["--lane", LANE, "--pricing-only", paths["reward-case"]], "E3"),
        "reward_currency": (["--lane", LANE, "--pricing-only", paths["reward-eur"]], "E3"),
        "two_quotes": (["--lane", LANE, "--pricing-only", paths["two-quotes"]], "E4"),
        "ws_quote": (["--lane", LANE, "--pricing-only", paths["ws-quote"]], "E4"),
        "kev_quote": (["--lane", LANE, "--pricing-only", paths["kev-quote"]], "E4"),
        "log_only": (["--lane", lane_log_only, "--pkg", dst], "E5"),
        "outside_lane": (["--lane", lane_outside, "--pkg", outside_pkg], "E5"),
        "only_e1_fails": (["--lane", lane_e1only, "--pkg", dst2], "RESULT"),
    }


PROBE_FOR = {
    "e1_rc_only": "gate_rc0_bad",
    "e1_verdict_only": "gate_rc3_good",
    "e2_drop_recorded_sha": "bogus_recorded_sha",
    "e2_drop_manifest_binding": "manifest_lie",
    "e2_one_source": "one_source",
    "e2_symlink_evidence": "symlink_evidence",
    "sev_ignore_s120": "s120_disagrees",
    "reward_case_insensitive": "reward_case",
    "e4_threshold_1": "two_quotes",
    "e4_raw_no_norm": "ws_quote",
    "e4_pool_includes_kev": "kev_quote",
    "e5_or": "log_only",
    "allok_ignores_e1": "only_e1_fails",
}

# expectations for a probe: the pristine outcome the probe was designed for
PROBE_EXPECT = {
    "gate_rc0_bad": ("E1", "FAIL", "pass"),
    "gate_rc3_good": ("E1", "FAIL", "pass"),
    "bogus_recorded_sha": ("E2", "FAIL", "pass"),
    "manifest_lie": ("E2", "FAIL", "pass"),
    "one_source": ("E2", "FAIL", "pass"),
    "symlink_evidence": ("E2", "FAIL", "pass"),
    "s120_disagrees": ("E3", "FAIL", "pass"),
    "reward_case": ("E3", "FAIL", "pass"),
    "reward_currency": ("E3", "FAIL", "pass"),
    "two_quotes": ("E4", "FAIL", "pass"),
    "ws_quote": ("E4", "pass", "FAIL"),
    "kev_quote": ("E4", "FAIL", "pass"),
    "log_only": ("E5", "FAIL", "pass"),
    "outside_lane": ("E5", "FAIL", "pass"),
    "only_e1_fails": ("RESULT", "fail", "pass"),
}


def limb(res, name):
    if name == "RESULT":
        return res["result"]
    for n, s in res["limbs"]:
        if n == name:
            return s
    return None


def main():
    os.makedirs(os.path.join(S, "fx"), exist_ok=True)
    shutil.rmtree(os.path.join(S, "fx/exemplar"), ignore_errors=True)
    shutil.copytree(os.path.join(
        LANE, "corpus/instruments/fixtures/claim-package/exemplar"),
        os.path.join(S, "fx/exemplar"))
    base = os.path.join(S, "base.py")
    frozen = open(FROZEN, "rb").read()
    w(base, frozen)
    assert sha(frozen) == FROZEN_SHA, "frozen counter sha drift"
    pristine = score(base)
    for name, exp in EXPECT.items():
        got = pristine[name]
        assert sig(got) == (exp["rc"], tuple(exp["limbs"])), (
            "pristine control %s mismatch: %s vs %s" % (name, sig(got), exp))
    print("pristine: %d/%d controls match frozen c2-controls-r85.txt"
          % (len(EXPECT), len(CONTROLS)))

    probes = build_probes()
    probe_pristine = {k: run(base, a) for k, (a, _) in probes.items()}

    results = {"frozen_sha256": sha(frozen), "mutants": {}, "probes": {}}
    for mid, old, new, note in MUTANTS:
        mpath = make_mutant(mid, old, new)
        mres = score(mpath)
        flips = []
        for cname in EXPECT:
            if sig(mres[cname]) != sig(pristine[cname]):
                flips.append({"control": cname,
                              "pristine": {"rc": pristine[cname]["rc"],
                                           "limbs": pristine[cname]["limbs"]},
                              "mutant": {"rc": mres[cname]["rc"],
                                         "limbs": mres[cname]["limbs"]}})
        probe = PROBE_FOR.get(mid)
        probe_row = None
        if probe:
            args, limbname = probes[probe]
            pm = run(mpath, args)
            pp = probe_pristine[probe]
            exp = PROBE_EXPECT[probe]
            probe_row = {
                "probe": probe,
                "limb": exp[0],
                "pristine": limb(pp, exp[0]),
                "mutant": limb(pm, exp[0]),
                "designed": [exp[1], exp[2]],
                "detects": limb(pp, exp[0]) == exp[1] and limb(pm, exp[0]) == exp[2],
                "pristine_full": pp["out"],
                "mutant_full": pm["out"],
                "pristine_rc": pp["rc"], "mutant_rc": pm["rc"],
            }
        verdict = "killed" if flips else "survived"
        results["mutants"][mid] = {
            "note": note, "sha256": sha(open(mpath, "rb").read()),
            "frozen_control_flips": flips, "verdict": verdict,
            "new_control": probe_row,
        }
        print("%-26s %-8s control_flips=%d probe=%s detects=%s"
              % (mid, verdict, len(flips), probe,
                 (probe_row or {}).get("detects")))

    # kev dead-guard equivalence: exhaustive truth table over plausible tokens
    def old_pred(g, w):
        return not g.startswith(w) or (w == "listed" and g.startswith("not-listed"))
    def new_pred(g, w):
        return not g.startswith(w)
    pairs = [(g, w) for g in ("listed", "listed (KEV)", "listed CVE", "not-listed",
                              "not-listed (CVE id absent)", "unlisted", "", "Listed")
             for w in ("listed", "not-listed")]
    diffs = [(g, w) for g, w in pairs if old_pred(g, w) != new_pred(g, w)]
    results["probes"]["kev_dead_guard_equivalence"] = {
        "pairs": len(pairs), "differing": diffs,
        "equivalent": not diffs,
        "proof": "when w=='listed', not g.startswith('listed') is already true for "
                 "g starting 'not-listed'; the second conjunct can never change the value",
    }

    # candidate package (as it stands) against pristine and every mutant
    cand = os.path.join(LANE, ".ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733")
    results["candidate"] = {"path": cand, "present": os.path.isdir(cand)}
    if os.path.isdir(cand):
        results["candidate"]["files"] = sorted(
            os.path.relpath(os.path.join(dp, f), cand)
            for dp, _, fs in os.walk(cand) for f in fs)
        args = ["--lane", LANE, "--pkg", cand]
        cp = run(base, args)
        results["candidate"]["pristine"] = {"rc": cp["rc"], "limbs": cp["limbs"],
                                            "result": cp["result"], "out": cp["out"]}
        cflips = {}
        for mid in results["mutants"]:
            cm = run(os.path.join(S, "mut", mid + ".py"), args)
            if sig(cm) != sig(cp):
                cflips[mid] = {"rc": cm["rc"], "limbs": cm["limbs"]}
        results["candidate"]["mutant_flips"] = cflips
        print("candidate: pristine %s; mutants flipping it: %s"
              % (sig(cp), ",".join(cflips) or "none"))

    w(os.path.join(S, "results.json"), json.dumps(results, indent=1))
    print("wrote", os.path.join(S, "results.json"))


if __name__ == "__main__":
    main()
