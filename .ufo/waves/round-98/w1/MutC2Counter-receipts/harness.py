#!/usr/bin/env python3
"""Round-98 C2 mutation harness: selftest + gate-K3 plants on pristine/mutant bytes."""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r98/MutC2Counter"
LANE = os.path.join(S, "lane")
INST = os.path.join(LANE, "corpus/instruments/capture-secret-scan.py")
GATE = os.path.join(LANE, ".ufo/waves/round-98/c2/capability-check.py")
WORK = os.path.join(S, "work")
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20261107
RAW = os.path.join(S, "raw")

HIT_RE = re.compile(r"HIT shape=([a-z0-9-]+) path=(\S+) line=(\d+)")
ST_RE = re.compile(r"SELFTEST-RESULT (pass|fail) cases=(\d+)")
FAIL_RE = re.compile(r"^SELFTEST (\S+) FAIL got=(.*)$", re.M)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def load_gate():
    spec = importlib.util.spec_from_file_location("gate_mod", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_selftest(inst, tag=None):
    r = subprocess.run([sys.executable, "-B", inst, "--selftest"],
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    if tag:
        os.makedirs(RAW, exist_ok=True)
        open(os.path.join(RAW, tag + ".selftest.txt"), "w").write(out)
    m = ST_RE.search(out)
    fails = [{"case": a, "got": b} for a, b in FAIL_RE.findall(out)]
    return {"rc": r.returncode, "result": m.group(1) if m else "none",
            "cases": int(m.group(2)) if m else None, "fails": fails}


def run_k3(inst, plant_paths, expect, tag=None):
    r = subprocess.run([sys.executable, "-B", inst, "--files"] + plant_paths,
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    if tag:
        os.makedirs(RAW, exist_ok=True)
        open(os.path.join(RAW, tag + ".k3.txt"), "w").write(out)
    hits = {(os.path.basename(m.group(2)), m.group(1)) for m in HIT_RE.finditer(out)}
    return {"rc": r.returncode, "hits": len(hits),
            "missing": sorted("%s|%s" % h for h in (expect - hits)),
            "extra": sorted("%s|%s" % h for h in (hits - expect)),
            "ok": hits == expect}


# (name, kind, old, new) — every replacement must occur exactly once.
MUTANTS = [
    ("M01-drop-ci-build", "drop-shape",
     '    ("gitlab-ci-build-token", re.compile(\n'
     '        _GL_LB + rb"glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9])")),\n', ''),
    ("M02-drop-iam-refresh", "drop-shape",
     '    ("gitlab-iam-refresh-token", re.compile(\n'
     '        _GL_LB + rb"gliamrt-[A-Za-z0-9_-]{43}\\.[A-Za-z0-9_-]{43}(?![A-Za-z0-9_-])")),\n', ''),
    ("M03-drop-iam-auth-code", "drop-shape",
     '    ("gitlab-iam-authorization-code", re.compile(\n'
     '        _GL_LB + rb"gliamac-[A-Za-z0-9_-]{43}\\.[A-Za-z0-9_-]{43}(?![A-Za-z0-9_-])")),\n', ''),
    ("M04-drop-session-cookie", "drop-shape",
     '    ("gitlab-session-cookie", re.compile(\n'
     '        _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[\\s\\"\'=:;]+"\n'
     '        rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),\n', ''),
    ("M05-narrow-registration", "narrow-boundary",
     'GR1348941[A-Za-z0-9_-]{20}(?![A-Za-z0-9])', 'GR1348941[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])'),
    ("M06-narrow-feed-token", "narrow-boundary",
     'feed_token=[A-Za-z0-9_-]{20}(?![A-Za-z0-9])', 'feed_token=[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])'),
    ("M07-narrow-oauth-app", "narrow-boundary",
     'gloas-[A-Za-z0-9_-]{64}(?![A-Za-z0-9])', 'gloas-[A-Za-z0-9_-]{64}(?![A-Za-z0-9_-])'),
    ("M08-narrow-feed-v2", "narrow-boundary",
     'glft-[A-Za-z0-9_-]{20}(?![A-Za-z0-9])', 'glft-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])'),
    ("M09-narrow-scim", "narrow-boundary",
     'glsoat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9])', 'glsoat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])'),
    ("M10-drop-session-context", "context",
     '_GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[\\s\\"\'=:;]+"',
     '_GL_LB + rb"[\\s\\"\'=:;]+"'),
    ("M11-43-to-42-refresh", "length",
     'gliamrt-[A-Za-z0-9_-]{43}', 'gliamrt-[A-Za-z0-9_-]{42}'),
    ("M12-drop-ci-build-underscore", "grammar",
     'glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}', 'glcbt-[A-Za-z0-9]{1,5}[A-Za-z0-9_-]{20}'),
    ("M13-session-hex-uppercase", "class",
     '(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])', '(?:cell-[0-9]+-)?[0-9a-fA-F]{64}(?![0-9a-f])'),
    # supplementary probes (coverage questions, not on the required list)
    ("M14-narrow-ci-build-boundary", "narrow-boundary",
     'glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9])',
     'glcbt-[A-Za-z0-9]{1,5}_[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])'),
    ("M15-43-to-44-auth-code", "length",
     'gliamac-[A-Za-z0-9_-]{43}', 'gliamac-[A-Za-z0-9_-]{44}'),
    ("M16-optional-session-context", "context",
     '_GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[\\s\\"\'=:;]+"',
     '_GL_LB + rb"(?:_gitlab_session(?:_geo_[0-9a-f]{64})?)?[\\s\\"\'=:;]+"'),
    ("M17-registration-20-to-21", "length",
     'GR1348941[A-Za-z0-9_-]{20}(?![A-Za-z0-9])', 'GR1348941[A-Za-z0-9_-]{20,21}(?![A-Za-z0-9])'),
]


def main():
    os.makedirs(WORK, exist_ok=True)
    gate = load_gate()
    root, rev, expect = gate.build_plants(WORK, SEED)
    plant_paths = [os.path.join(dp, f) for dp, _, fs in os.walk(root)
                   for f in fs if "/.git/" not in os.path.join(dp, f)]
    plant_paths.sort()
    pristine = open(INST, "rb").read()
    psha = sha(INST)
    base_st = run_selftest(INST, "PRISTINE")
    base_k3 = run_k3(INST, plant_paths, expect, "PRISTINE")
    results = {"seed": SEED, "plant_root": root, "plant_rev": rev,
               "plant_files": len(plant_paths),
               "expect": sorted("%s|%s" % h for h in expect),
               "pristine_sha256": psha,
               "baseline": {"selftest": base_st, "k3": base_k3},
               "mutants": []}
    if base_st["rc"] != 0 or not base_k3["ok"]:
        print("BASELINE FAILED — inconclusive")
        print(json.dumps(results, indent=1))
        return 2
    for name, kind, old, new in MUTANTS:
        text = pristine.decode()
        n = text.count(old)
        if n != 1:
            results["mutants"].append({"name": name, "kind": kind, "apply": "FAIL count=%d" % n})
            continue
        mutated = text.replace(old, new).encode()
        with open(INST, "wb") as fh:
            fh.write(mutated)
        msha = sha(INST)
        st = run_selftest(INST, name)
        k3 = run_k3(INST, plant_paths, expect, name)
        # restore exact pristine bytes
        with open(INST, "wb") as fh:
            fh.write(pristine)
        rsha = sha(INST)
        killed_st = st["rc"] != 0
        killed_k3 = not k3["ok"]
        results["mutants"].append({
            "name": name, "kind": kind, "apply": "ok",
            "mutant_sha256": msha, "restored_sha256": rsha,
            "selftest": st, "k3": k3,
            "killed_by": [d for d, k in (("selftest", killed_st), ("k3", killed_k3)) if k],
            "verdict": ("killed" if (killed_st or killed_k3) else "SURVIVED"),
            "gap": (("selftest-only" if killed_st and not killed_k3 else
                     "k3-only" if killed_k3 and not killed_st else
                     "both" if killed_st and killed_k3 else "NEITHER")),
        })
        print("%-30s %-8s st=%s k3=%s" % (name, results["mutants"][-1]["verdict"],
                                          "kill" if killed_st else "survive",
                                          "kill" if killed_k3 else "survive"))
    results["final_sha256"] = sha(INST)
    with open(os.path.join(S, "results-%d.json" % SEED), "w") as fh:
        json.dump(results, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
