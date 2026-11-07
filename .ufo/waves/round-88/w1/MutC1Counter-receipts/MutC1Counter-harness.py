#!/usr/bin/env python3
"""Mutation harness for the frozen round-88 C1 counter.

Reads the frozen counter READ-ONLY, writes mutants into scratch, and runs the
frozen control battery (replicated step-for-step from
.ufo/waves/round-88/controls/c1-controls-r88.sh) plus a set of isolating
controls, comparing LIMB verdict vectors per control.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = os.path.join(L, ".ufo/waves/round-88")
CNT = os.path.join(W, "c1/knowledge-meter.py")
MAP = os.path.join(W, "c1/repair-map.json")
APPLY = os.path.join(W, "c1/apply-map.py")
B = "6beead9148945fa695cf3139e8fc9d8e91cc5fd0"
S = "/fast/scratch/hyaku/kasegi-r88/MutC1Counter"
TREES = os.path.join(S, "trees")
MUT = os.path.join(S, "mut")
OUT = os.path.join(S, "out")
WORK = os.path.join(S, "work")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def clone(name):
    d = os.path.join(TREES, name)
    shutil.rmtree(d, ignore_errors=True)
    r = run(["git", "clone", "-q", "--shared", L, d])
    assert r.returncode == 0, r.stderr
    r = run(["git", "-C", d, "checkout", "-q", B])
    assert r.returncode == 0, r.stderr
    top = run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    return d


def apply_map(root, mp):
    r = run([sys.executable, "-B", APPLY, "--root", root, "--map", mp])
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def forge(name, key=None, val=None, base_map=MAP, extra=None):
    """Write a forged map into scratch; returns (path, sha)."""
    m = json.load(open(base_map))
    if key is not None:
        m[key] = val
    if extra:
        m.update(extra)
    p = os.path.join(S, name + ".json")
    json.dump(m, open(p, "w"), indent=1, sort_keys=True)
    return p, sha(p)


def meter(counter, tree, mp, msha, target, tag):
    args = [sys.executable, "-B", counter, "--lane", tree, "--base-rev", B,
            "--map", mp, "--target", target, "--map-sha256", msha, "--work", WORK]
    r = run(args, env=dict(os.environ, TMPDIR=S))
    limbs = {}
    res = ""
    for ln in r.stdout.splitlines():
        if ln.startswith("LIMB "):
            parts = ln.split()
            limbs[parts[1]] = parts[2]
        elif ln.startswith("KNOWLEDGE-METER-RESULT"):
            res = ln
    open(os.path.join(OUT, tag + ".txt"), "w").write(
        "$ " + " ".join(args) + "\n" + r.stdout + r.stderr + "[exit %d]\n" % r.returncode)
    return {"rc": r.returncode, "limbs": limbs, "res": res, "raw": r.stdout}


def build_controls():
    print("building trees", flush=True)
    for t in ("dn", "pos", "half", "pad", "drift", "notentry", "ufocopy", "dups", "trunc"):
        clone(t)
    d = os.path.join(TREES, "pos")
    print(apply_map(d, MAP), flush=True)
    half = os.path.join(S, "half.json")
    m = json.load(open(MAP))
    k = sorted(m)[: len(m) // 2]
    json.dump({x: m[x] for x in k}, open(half, "w"))
    print("half", apply_map(os.path.join(TREES, "half"), half), flush=True)
    # pad: pos knowledge copied, then two extra resolving cites appended
    shutil.copytree(os.path.join(TREES, "pos/corpus/knowledge"),
                    os.path.join(TREES, "pad/corpus/knowledge"), dirs_exist_ok=True)
    with open(os.path.join(TREES, "pad/corpus/knowledge/claim-gates.md"), "a") as fh:
        fh.write("\n`corpus/SOURCES.md`\n`corpus/instruments/resolve.py`\n")
    for nm, kk, vv in (
            ("drift", "mission-control.md:41-45", "corpus/knowledge/mission-control.md:41-45"),
            ("notentry", "SOURCES.md", "corpus/SOURCES.md"),
            ("ufocopy", "claim-gates.md:32-33",
             ".ufo/waves/round-25/c1-controls/base/corpus/knowledge/claim-gates.md:32-33"),
            ("singledrift", "claim-gates.md:3", "corpus/knowledge/claim-gates.md:3"),
            ("ghostkey", "claim-gates.md:200", "corpus/knowledge/claim-gates.md:200"),
            ("zeroanchor", "claim-gates.md:0-3", "corpus/knowledge/claim-gates.md:0-3"),
            ("biganchor", "claim-gates.md:1-99999", "corpus/knowledge/claim-gates.md:1-99999"),
            ("slashkey", "corpus/../claim-gates.md", "corpus/knowledge/corpus/../claim-gates.md"),
    ):
        forge(nm, kk, vv, base_map=MAP)
    for nm in ("drift", "notentry", "ufocopy"):
        print(nm, apply_map(os.path.join(TREES, nm), os.path.join(S, nm + ".json")), flush=True)
    # dups: a second tracked file with the basename claim-gates.md outside .ufo/
    d = os.path.join(TREES, "dups")
    os.makedirs(os.path.join(d, "corpus", "notes"), exist_ok=True)
    open(os.path.join(d, "corpus", "notes", "claim-gates.md"), "w").write("# decoy\n")
    r = run(["git", "-C", d, "add", "corpus/notes/claim-gates.md"])
    assert r.returncode == 0, r.stderr
    print(apply_map(d, MAP), flush=True)
    # trunc: pos tree with the last line of one entry dropped (line count differs)
    d = os.path.join(TREES, "trunc")
    shutil.copytree(os.path.join(TREES, "pos/corpus/knowledge"),
                    os.path.join(d, "corpus/knowledge"), dirs_exist_ok=True)
    p = os.path.join(d, "corpus/knowledge/citation-bases.md")
    txt = open(p).read().rstrip("\n").split("\n")
    open(p, "w").write("\n".join(txt[:-1]) + "\n")
    print("trunc dropped a line from citation-bases.md", flush=True)


def control_table():
    fs = sha(MAP)
    tgt = "742/1743"
    table = [
        ("do-nothing", "dn", MAP, fs, tgt),
        ("positive", "pos", MAP, fs, tgt),
        ("partial", "half", MAP, fs, tgt),
        ("pad", "pad", MAP, fs, tgt),
        ("drift-forge", "drift", os.path.join(S, "drift.json"), sha(os.path.join(S, "drift.json")), tgt),
        ("notentry-forge", "notentry", os.path.join(S, "notentry.json"), sha(os.path.join(S, "notentry.json")), tgt),
        ("ufo-copy", "ufocopy", os.path.join(S, "ufocopy.json"), sha(os.path.join(S, "ufocopy.json")), tgt),
        ("map-sha", "pos", MAP, "0" * 64, tgt),
        # isolating controls (N-series)
        ("N1-drift-target", "drift", os.path.join(S, "drift.json"), sha(os.path.join(S, "drift.json")), "743/1743"),
        ("N2-pos-denom", "pos", MAP, fs, "742/1742"),
        ("N3-dups", "dups", MAP, fs, tgt),
        ("N4-ghost-key", "pos", os.path.join(S, "ghostkey.json"), sha(os.path.join(S, "ghostkey.json")), tgt),
        ("N5-zero-anchor", "pos", os.path.join(S, "zeroanchor.json"), sha(os.path.join(S, "zeroanchor.json")), tgt),
        ("N6-big-anchor", "pos", os.path.join(S, "biganchor.json"), sha(os.path.join(S, "biganchor.json")), tgt),
        ("N7-single-drift", "pos", os.path.join(S, "singledrift.json"), sha(os.path.join(S, "singledrift.json")), tgt),
        ("N8-trunc", "trunc", MAP, fs, tgt),
        ("N9-slash-key", "pos", os.path.join(S, "slashkey.json"), sha(os.path.join(S, "slashkey.json")), tgt),
    ]
    return table


MUTANTS = [
    ("p00-pristine", None, None),
    # M1
    ("m01-m1-numerator-only", '    limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))',
     '    limbs.append(("M1", an == tn, "after=%d/%d" % (an, am)))'),
    ("m02-m1-always", '    limbs.append(("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am)))',
     '    limbs.append(("M1", True, "after=%d/%d" % (an, am)))'),
    ("m03-rate-only-internal", '    return sum(1 for c in cls.values() if c != "GONE"), len(cls)',
     '    return sum(1 for c in cls.values() if c == "INTERNAL"), len(cls)'),
    # M2
    ("m04-m2-drop-removed", 'removed == keys and added <= vals', 'added <= vals'),
    ("m05-m2-removed-subset", 'removed == keys and added <= vals', 'removed <= keys and added <= vals'),
    ("m06-m2-drop-added", 'removed == keys and added <= vals', 'removed == keys'),
    # M3
    ("m07-m3-no-replace", 'fwd = fwd.replace("`%s`" % k, "`%s`" % v)', 'pass'),
    ("m08-m3-drop-linecount", '            if len(bl) != len(al):', '            if False:'),
    ("m09-m3-drop-hitkeys", 'm3 = same_files and bad == 0 and hit == keys', 'm3 = same_files and bad == 0'),
    # M4
    ("m10-m4-drop-bybase", '              and bybase.get(name) == [path]', '              and True'),
    ("m11-m4-drop-gone", '              and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     '              and R.classify(v, lane, mirror)[0] == "INTERNAL")'),
    ("m12-m4-drop-internal", 'and R.classify(v, lane, mirror)[0] == "INTERNAL" and bcls.get(k) == "GONE")',
     'and bcls.get(k) == "GONE")'),
    ("m13-m4-no-anchor-strip",
     '        path = v[: len(v) - len(anchor)] if anchor and v.endswith(anchor) else (v if not anchor else None)',
     '        path = v'),
    # M5
    ("m14-m5-drop-lo", '                if not (1 <= lo_i <= hi_i <= nlines):', '                if not (lo_i <= hi_i <= nlines):'),
    ("m15-m5-drop-hi", '                if not (1 <= lo_i <= hi_i <= nlines):', '                if not (1 <= lo_i <= hi_i):'),
    ("m16-m5-ignore-m4", '    limbs.append(("M5", not m5bad and not m4bad,', '    limbs.append(("M5", not m5bad,'),
    # M6
    ("m17-m6-always", '        limbs.append(("M6", got == a.map_sha256.lower(), "sha256=%s" % got))',
     '        limbs.append(("M6", True, "sha256=%s" % got))'),
    ("m18-m6-no-lower", 'got == a.map_sha256.lower()', 'got == a.map_sha256'),
    # M8
    ("m19-m8-always", '    limbs.append(("M8", not m8bad, "no_shared_identifier=%s" % (",".join(m8bad) or "none")))',
     '    limbs.append(("M8", True, "no_shared_identifier=%s" % (",".join(m8bad) or "none")))'),
    ("m20-m8-all-not-any", '        if not cites or any(not (idents(ln) & tw) for ln in cites):',
     '        if not cites or all(not (idents(ln) & tw) for ln in cites):'),
    ("m21-m8-slice-offbyone", 'tw = set(WORD.findall("\\n".join(tgt.split("\\n")[lo_i - 1:hi_i])))',
     'tw = set(WORD.findall("\\n".join(tgt.split("\\n")[lo_i - 1:hi_i - 1])))'),
    ("m22-m8-word-3", 'WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")',
     'WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")'),
    ("m23-m8-word-6", 'WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{4,}")',
     'WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]{5,}")'),
    ("m24-m8-drop-pathlike", '        if PATHLIKE.match(sp.strip()):\n            continue',
     '        if False:\n            continue'),
    ("m25-m8-first-cite-only", '        cites = [ln for txt in bfiles.values() for ln in txt.split("\\n") if "`%s`" % k in ln]',
     '        cites = [ln for txt in bfiles.values() for ln in txt.split("\\n") if "`%s`" % k in ln][:1]'),
    ("m26-m8-skip-single-anchor", '        if not km or km.group(2) is None:', '        if not km or km.group(3) is None:'),
    ("m27-m8-drop-nocites", '        if not cites or any(not (idents(ln) & tw) for ln in cites):',
     '        if any(not (idents(ln) & tw) for ln in cites):'),
    # KEY / scope
    ("m28-key-no-anchor", 'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")',
     'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)$")'),
    ("m29-key-no-range", 'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")',
     'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)(?::(\\d+))?$")'),
    ("m30-key-allow-slash", 'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")',
     'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._/-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")'),
    ("m31-key-allow-leading-dot", 'KEY = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")',
     'KEY = re.compile(r"^([A-Za-z0-9.][A-Za-z0-9._-]*\\.md)(?::(\\d+)(?:-(\\d+))?)?$")'),
    ("m32-scope-count-ge", '             if p.endswith(".md") and p.count("/") == 2]',
     '             if p.endswith(".md") and p.count("/") >= 2]'),
    ("m33-scope-drop-md-filter", '             if p.endswith(".md") and p.count("/") == 2]',
     '             if p.count("/") == 2]'),
    ("m34-tree-drop-md-filter", '        if fn.endswith(".md") and os.path.isfile(p):', '        if os.path.isfile(p):'),
    ("m35-ufo-include", '        if not p.startswith(".ufo/"):', '        if True:'),
    ("m36-ufo-noslash", '        if not p.startswith(".ufo/"):', '        if not p.startswith(".ufo"):'),
]


def main():
    os.makedirs(MUT, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    before = sha(CNT)
    src = open(CNT, encoding="utf-8").read()
    if not os.path.isdir(os.path.join(TREES, "trunc")):
        build_controls()
    ctl = control_table()
    results = {}
    manifest = {"pristine_sha256_before": before, "controls": [c[0] for c in ctl], "mutants": {}}
    only = os.environ.get("ONLY")
    for name, old, new in MUTANTS:
        if only and name not in only.split(","):
            continue
        if old is None:
            path, msha = CNT, before
        else:
            assert src.count(old) == 1, (name, src.count(old))
            body = src.replace(old, new)
            path = os.path.join(MUT, name + ".py")
            open(path, "w", encoding="utf-8").write(body)
            msha = sha(path)
        row = {}
        for cname, tree, mp, ms, tgt in ctl:
            tag = "%s__%s" % (name, cname)
            r = meter(path, os.path.join(TREES, tree), mp, ms, tgt, tag)
            row[cname] = r
        results[name] = row
        manifest["mutants"][name] = {"sha256": msha, "mutated_from": old,
                                     "mutated_to": new}
        print("%-28s %s" % (name, " ".join("%s:%s%s" % (c, r["rc"], "".join(v[0] if v == "pass" else "F" for v in [])) for c, r in row.items())), flush=True)
    # verdict vectors vs pristine
    ref = results.get("p00-pristine") or {c[0]: meter(CNT, os.path.join(TREES, c[1]), c[2], c[3], c[4], "p00-pristine__" + c[0]) for c in ctl}
    results.setdefault("p00-pristine", ref)
    summary = {}
    for name, row in results.items():
        killed_by = [c for c in row if row[c]["limbs"] != ref[c]["limbs"]]
        rc_chg = [c for c in row if row[c]["rc"] != ref[c]["rc"]]
        summary[name] = {"killed_by": killed_by, "rc_changed_by": rc_chg,
                         "verdict": "killed" if (killed_by or rc_chg) else "SURVIVED"}
    manifest["summary"] = summary
    manifest["pristine_sha256_after"] = sha(CNT)
    manifest["pristine_limbs"] = {c: ref[c]["limbs"] for c in ref}
    manifest["pristine_rc"] = {c: ref[c]["rc"] for c in ref}
    json.dump(manifest, open(os.path.join(S, "manifest.json"), "w"), indent=1, sort_keys=True)
    for name, s in summary.items():
        print("%-28s %-9s killed_by=%s rc_by=%s" % (name, s["verdict"], ",".join(s["killed_by"]) or "-", ",".join(s["rc_changed_by"]) or "-"))
    print("pristine sha before=%s after=%s" % (before, manifest["pristine_sha256_after"]))
    for c in ref:
        print("PRISTINE %-18s rc=%d %s %s" % (c, ref[c]["rc"],
              " ".join("%s=%s" % (k, v) for k, v in sorted(ref[c]["limbs"].items())), ref[c]["res"]))


if __name__ == "__main__":
    main()
