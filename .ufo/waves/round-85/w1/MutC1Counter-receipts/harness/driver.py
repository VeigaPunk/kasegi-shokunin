#!/usr/bin/env python3
"""Round-85 C1 counter mutation driver (MutC1Counter seat).

Rebuilds the exact pre-freeze control inputs of
  .ufo/waves/round-85/controls/c1-controls-r85.sh
in scratch, then runs the frozen control logic against single-point mutants of
.ufo/waves/round-85/c1/skill-meter.py.  The frozen target 167/732 and map
sha256 are held FIXED for every run (the oracle is not re-derived per mutant).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = L + "/.ufo/waves/round-85"
S = "/fast/scratch/hyaku/kasegi-r85/MutC1Counter"
IN = os.path.join(S, "inputs")
ORIG = os.path.join(S, "orig", "skill-meter.py")
MAP = os.path.join(IN, "repair-map.json")
APPLY = os.path.join(IN, "apply-map.py")
MAP_SHA = "b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944"
BASE_REV = "bc722e540c93b48ff159454b65a0f9f4630db1ed"
TARGET = "167/732"
ENV = dict(os.environ)
ENV["TMPDIR"] = S
ENV.pop("KASEGI_MIRROR", None)

PAD = ("\nPad: `corpus/knowledge/cisa-kev-catalog.md` `corpus/knowledge/claim-gates.md` "
       "`corpus/knowledge/claim-package-contract.md` `corpus/knowledge/cvss-v4-severity-and-vector.md` "
       "`corpus/knowledge/vdp-disclosure-packages.md` `corpus/instruments/density.py` "
       "`corpus/instruments/anchorcheck.py` `corpus/instruments/recheck-audit.py` "
       "`corpus/instruments/figure-audit.py` `corpus/instruments/wave-registry.py` "
       "`corpus/instruments/freeze-check.py` `corpus/instruments/gate-quote-audit.py` "
       "`corpus/instruments/census-freshness-check.py` `corpus/instruments/derive-head-census.py` "
       "`corpus/instruments/citation-ground-check.py` `corpus/instruments/mirror-containment-check.py` "
       "`corpus/instruments/recheck-cwd-census.py` `corpus/instruments/source-recheck.py`\n")

DELGONE = r'''import sys,os
sys.path.insert(0,os.path.join(sys.argv[3],'corpus','instruments'))
import resolve as R
t=open(sys.argv[1],encoding='utf-8').read(); n=0
mirror=os.path.expanduser(R.MIRROR_ROOT)
for line in t.split('\n'):
    for m in R.TOKEN.finditer(line):
        tok=m.group(1).strip().rstrip('.,;:')
        if n<18 and tok.startswith('~/Projects/bounties/') and R.is_pathlike(tok) and R.classify(tok,sys.argv[3],mirror)[0]=='GONE' and t.count('`%s`'%m.group(1))==1:
            t=t.replace('`%s`'%m.group(1), m.group(1).replace('/', ' / ')); n+=1
open(sys.argv[2],'w',encoding='utf-8').write(t); print('delete-gone de-cited', n)
'''

MUTANTS = [
    # id, old, new, note
    ("m01-m1-numerator-only",
     'limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))',
     'limbs.append(("M1", an == tn, "after=%d/%d" % (an, am)))',
     "M1 compares only numerator"),
    ("m02-m1-limb-dropped",
     '    limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))\n',
     '',
     "M1 limb never appended"),
    ("m03-m1-ge",
     '(an, am) == (tn, tm)',
     'an >= tn',
     "M1 accepts after >= target (numerator only, >=)"),
    ("m04-m2-drop-added",
     'm2 = removed == keys and added <= vals',
     'm2 = removed == keys',
     "M2 drops the added<=vals limb"),
    ("m05-m2-keys-subset",
     'm2 = removed == keys and added <= vals',
     'm2 = keys <= removed and added <= vals',
     "M2 uses issubset of keys instead of equality"),
    ("m06-m2-any-overlap",
     'm2 = removed == keys and added <= vals',
     'm2 = bool(removed & keys) and added <= vals',
     "M2 accepts any key/removal overlap"),
    ("m07-m3-skip-linecount",
     'm3 = len(base_lines) == len(after_lines)',
     'm3 = True',
     "M3 skips the equal-line-count requirement"),
    ("m08-m3-drop-hit",
     'm3 = bad == 0 and hit == keys',
     'm3 = bad == 0',
     "M3 hit==keys check removed"),
    ("m09-m3-self-replace",
     'fwd = fwd.replace("`%s`" % k, "`%s`" % v)',
     'fwd = fwd.replace("`%s`" % k, "`%s`" % k)',
     "M3 forward application replaces key with itself"),
    ("m10-m3-hit-from-after",
     'if "`%s`" % k in fwd:',
     'if "`%s`" % k in al:',
     "M3 looks for keys in the after line"),
    ("m11-m4-drop-ufo",
     'ok = (v in tracked and not v.startswith(".ufo/") and v.endswith("/" + k)',
     'ok = (v in tracked and v.endswith("/" + k)',
     "M4 drops the .ufo/ exclusion"),
    ("m12-m4-drop-endswith",
     'ok = (v in tracked and not v.startswith(".ufo/") and v.endswith("/" + k)',
     'ok = (v in tracked and not v.startswith(".ufo/")',
     "M4 drops the endswith('/'+key) rule"),
    ("m13-m4-drop-internal",
     'and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'and bcls.get(k) == "GONE")',
     "M4 drops the INTERNAL classification check"),
    ("m14-m4-drop-base-gone",
     'and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'and R.classify(v, lane, mirror)[0] == "INTERNAL")',
     "M4 drops the base-key-GONE check"),
    ("m15-m5-ignored",
     'if a.map_sha256:',
     'if False and a.map_sha256:',
     "M5 is ignored when --map-sha256 is given"),
    ("m16-m5-prefix",
     'limbs.append(("M5", got == a.map_sha256.lower(), "sha256=%s" % got))',
     'limbs.append(("M5", got[:8] == a.map_sha256.lower()[:8], "sha256=%s" % got))',
     "M5 compares only an 8-hex prefix"),
    ("m17-verdict-ignores-m4",
     'allok = all(ok for _, ok, _ in limbs)',
     'allok = all(ok for name, ok, _ in limbs if name != "M4")',
     "verdict ignores the M4 limb"),
    ("m18-verdict-ignores-m5",
     'allok = all(ok for _, ok, _ in limbs)',
     'allok = all(ok for name, ok, _ in limbs if name != "M5")',
     "verdict ignores the M5 limb"),
    ("m19-rc0-on-fail",
     'return 0 if allok else 1',
     'return 0',
     "exit code 0 even when a limb fails"),
    ("m20-m3-zip-swapped",
     'for bl, al in zip(base_lines, after_lines):',
     'for bl, al in zip(after_lines, base_lines):',
     "M3 walks after lines as the base side"),
]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, env=ENV, **kw)


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def measure(counter, skill, lane=L):
    p = sh(["python3", "-B", counter, "--lane", lane,
            "--work", os.path.join(S, "work"), "--measure", skill])
    m = re.search(r"rate=(\d+/\d+)", p.stdout)
    if not m:
        raise SystemExit("measure failed for %s: rc=%s %s %s" %
                         (counter, p.returncode, p.stdout, p.stderr))
    return m.group(1)


def build():
    base = os.path.join(IN, "base.md")
    assert sha(base) == "8df45d27e36e5dac62cdd7f56df6f6f2f85333d972be45fee0f751b8381b4104", "base sha"
    assert sha(MAP) == MAP_SHA, "map sha"
    positive = os.path.join(IN, "positive.md")
    p = sh(["python3", "-B", APPLY, MAP, base, positive])
    assert p.returncode == 0, p.stderr
    pad = os.path.join(IN, "pad.md")
    with open(pad, "wb") as fh:
        fh.write(open(base, "rb").read() + PAD.encode())
    dg = os.path.join(IN, "delgone.py")
    with open(dg, "w", encoding="utf-8") as fh:
        fh.write(DELGONE)
    delgone = os.path.join(IN, "delgone.md")
    p = sh(["python3", dg, base, delgone, L])
    assert p.returncode == 0, p.stderr
    wrong = os.path.join(IN, "wrong.md")
    p = sh(["python3", "-B", APPLY, MAP, base, wrong,
            "--swap", "resolve.py=corpus/instruments/density.py"])
    assert p.returncode == 0, p.stderr
    partial = os.path.join(IN, "partial.md")
    p = sh(["python3", "-B", APPLY, MAP, base, partial, "--only", "9"])
    assert p.returncode == 0, p.stderr
    rb, rp = measure(ORIG, base), measure(ORIG, positive)
    print("base=%s positive=%s target=%s delgone=%s pad=%s wrong=%s partial=%s" %
          (rb, rp, TARGET, measure(ORIG, delgone), measure(ORIG, pad),
           measure(ORIG, wrong), measure(ORIG, partial)))
    assert rb == "158/741", rb
    assert rp == TARGET, rp
    print("BUILD OK map_sha=%s base_sha=%s orig_sha=%s" % (MAP_SHA, sha(base), sha(ORIG)))


def mutants():
    src = open(ORIG, encoding="utf-8").read()
    outdir = os.path.join(S, "mutants")
    os.makedirs(outdir, exist_ok=True)
    for mid, old, new, note in MUTANTS:
        n = src.count(old)
        if n != 1:
            raise SystemExit("%s: old string occurs %d times: %r" % (mid, n, old[:60]))
        dst = os.path.join(outdir, mid + ".py")
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(src.replace(old, new, 1))
        d = subprocess.run(["diff", "-u", ORIG, dst], capture_output=True, text=True)
        with open(os.path.join(outdir, mid + ".diff"), "w", encoding="utf-8") as fh:
            fh.write(d.stdout)
        print("%s %s\n%s" % (mid, sha(dst)[:16], d.stdout.strip()))
    print("MUTANTS OK n=%d" % len(MUTANTS))


def run_counter(counter, base, after, mapfile, target, msha, lane=L):
    p = sh(["python3", "-B", counter, "--lane", lane,
            "--work", os.path.join(S, "work"),
            "--base", base, "--after", after, "--map", mapfile,
            "--target", target, "--map-sha256", msha])
    limbs = {}
    for ln in p.stdout.split("\n"):
        m = re.match(r"LIMB (\S+) (pass|FAIL) (.*)$", ln)
        if m:
            limbs[m.group(1)] = [m.group(2), m.group(3)]
    res = ""
    for ln in p.stdout.split("\n"):
        if ln.startswith("SKILL-METER-RESULT"):
            res = ln
    return {"rc": p.returncode, "limbs": limbs, "result": res,
            "stdout": p.stdout, "stderr": p.stderr}


def controls(counter, lane=L, tag=""):
    """Frozen six controls, expected outcomes per c1-controls-r85.sh."""
    base = os.path.join(IN, "base.md")
    specs = [
        ("donothing", os.path.join(IN, "base.md"), "fail"),
        ("pad-resolving-cites", os.path.join(IN, "pad.md"), "fail"),
        ("delete-gone-cites", os.path.join(IN, "delgone.md"), "fail"),
        ("wrong-target", os.path.join(IN, "wrong.md"), "fail"),
        ("partial-9-of-18", os.path.join(IN, "partial.md"), "fail"),
        ("positive", os.path.join(IN, "positive.md"), "pass"),
    ]
    out = {}
    for name, after, exp in specs:
        out[name] = run_counter(counter, base, after, MAP, TARGET, MAP_SHA, lane)
        out[name]["expected"] = exp
    return out


def is_killed(res):
    return (res["expected"] == "fail" and res["rc"] == 0) or \
           (res["expected"] == "pass" and res["rc"] != 0)


def matrix():
    os.makedirs(os.path.join(S, "logs"), exist_ok=True)
    results = {"pristine": {"sha256": sha(ORIG), "controls": controls(ORIG)}}
    for c, r in results["pristine"]["controls"].items():
        print("pristine %-22s rc=%d expected=%s killed=%s" % (c, r["rc"], r["expected"], is_killed(r)))
    for mid, *_ in MUTANTS:
        ctr = os.path.join(S, "mutants", mid + ".py")
        res = controls(ctr)
        results[mid] = {"sha256": sha(ctr), "controls": res}
        killed = [c for c, r in res.items() if is_killed(r)]
        print("%-24s killed_by=%s" % (mid, ",".join(killed) or "SURVIVED"))
    with open(os.path.join(S, "frozen_matrix.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print("MATRIX OK")


def proposed():
    base = os.path.join(IN, "base.md")
    positive = os.path.join(IN, "positive.md")
    specs = {}
    # C1 wrong-denominator target: numerator matches, denominator is off by 9.
    specs["C1-wrong-denominator-target"] = dict(
        after=positive, mapfile=MAP, target="167/741", msha=MAP_SHA, note="target=167/741")
    # C2 citation-free line appended to the accepted after.
    prompt = os.path.join(IN, "positive-blankline.md")
    with open(prompt, "wb") as fh:
        fh.write(open(positive, "rb").read() + b"\n")
    specs["C2-blank-line-appended"] = dict(
        after=prompt, mapfile=MAP, target=TARGET, msha=MAP_SHA, note="positive + one empty line")
    # C3 map sha with the last hex nibble corrupted (same 8-hex prefix).
    bad = MAP_SHA[:-1] + ("5" if MAP_SHA[-1] != "5" else "6")
    specs["C3-mapsha-tail-corrupt"] = dict(
        after=positive, mapfile=MAP, target=TARGET, msha=bad, note="sha tail flipped")
    # C4 forged map: value under .ufo/ (tracked copy of resolve.py).
    def forge(name, value):
        m = json.load(open(MAP, encoding="utf-8"))
        m2 = dict(m)
        m2["resolve.py"] = value
        mp = os.path.join(IN, name + "-map.json")
        with open(mp, "w", encoding="utf-8") as fh:
            json.dump(m2, fh, indent=1, sort_keys=True)
        af = os.path.join(IN, name + ".md")
        p = sh(["python3", "-B", APPLY, mp, base, af])
        assert p.returncode == 0, p.stderr
        return mp, af, measure(ORIG, af), sha(mp)
    mp4, af4, t4, s4 = forge(
        "c4-ufo-value", ".ufo/waves/round-25/c1-after-35/corpus/instruments/resolve.py")
    specs["C4-map-value-under-ufo"] = dict(
        after=af4, mapfile=mp4, target=t4, msha=s4, note="resolve.py -> tracked .ufo copy")
    mp5, af5, t5, s5 = forge(
        "c5-wrong-basename", "corpus/instruments/test_resolve.py")
    specs["C5-map-value-wrong-basename"] = dict(
        after=af5, mapfile=mp5, target=t5, msha=s5, note="resolve.py -> test_resolve.py")
    print("proposed targets:", {k: v["target"] for k, v in specs.items()},
          "shas:", {k: v["msha"][:12] for k, v in specs.items()})
    out = {}
    for name, sp in specs.items():
        r = run_counter(ORIG, base, sp["after"], sp["mapfile"], sp["target"], sp["msha"])
        r["expected"] = "fail"
        r["note"] = sp["note"]
        out[name] = r
        print("pristine %-28s rc=%d killed=%s %s" % (name, r["rc"], is_killed(r), r["result"]))
    for mid, *_ in MUTANTS:
        ctr = os.path.join(S, "mutants", mid + ".py")
        for name, sp in specs.items():
            r = run_counter(ctr, base, sp["after"], sp["mapfile"], sp["target"], sp["msha"])
            r["expected"] = "fail"
            out.setdefault(name, {})
            rk = is_killed(r)
            print("%-24s %-28s rc=%d new-killed=%s" % (mid, name, r["rc"], rk))
            out[name + "::" + mid] = r
    with open(os.path.join(S, "proposed_matrix.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("PROPOSED OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=["build", "mutants", "matrix", "proposed"])
    a = ap.parse_args()
    {"build": build, "mutants": mutants, "matrix": matrix, "proposed": proposed}[a.phase]()


if __name__ == "__main__":
    main()
