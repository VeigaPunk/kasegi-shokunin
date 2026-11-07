#!/usr/bin/env python3
"""Build the frozen r86 C1 control trees/maps in scratch, exactly as
.ufo/waves/round-86/controls/c1-controls-r86.sh builds them, plus extension
controls (tgt/prose/ghost/stale-anchor/uniq/key/mapsha-prefix/result-assert).
Writes controls.json for run_matrix.py. Read-only against the lane.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r86/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
B = "d7296645c2cd9f631329fa8e2f38328a4c9c89a5"
W = L + "/.ufo/waves/round-86/c1"
MAP = W + "/repair-map.json"
COUNTER = S + "/knowledge-meter.orig.py"
TREES = S + "/trees"
MAPS = S + "/maps"
WORK = S + "/w"


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s\n%s\n%s" % (cmd, r.stdout, r.stderr))
    return r.stdout


def sha(p):
    import hashlib
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def fresh(name):
    d = os.path.join(TREES, name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    sh(["git", "clone", "-q", "--shared", L, d])
    sh(["git", "-C", d, "checkout", "-q", B])
    if sh(["git", "-C", d, "rev-parse", "HEAD"]).strip() != B:
        raise SystemExit("checkout mismatch " + name)
    return d


def apply_map(root, mapfile):
    rmap = json.load(open(mapfile))
    d = os.path.join(root, "corpus", "knowledge")
    changed = 0
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if not (fn.endswith(".md") and os.path.isfile(p)):
            continue
        text = open(p, encoding="utf-8").read()
        out = []
        for line in text.split("\n"):
            for k, v in rmap.items():
                if "`%s`" % k in line:
                    line = line.replace("`%s`" % k, "`%s`" % v)
            out.append(line)
        new = "\n".join(out)
        if new != text:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


def meter(ctl):
    cmd = ["python3", "-B", COUNTER, "--lane", ctl["tree"], "--base-rev", B,
           "--map", ctl["map"], "--target", ctl["target"], "--map-sha256", ctl["sha"],
           "--work", WORK]
    r = subprocess.run(cmd, capture_output=True, text=True)
    limbs = {}
    for line in r.stdout.splitlines():
        if line.startswith("LIMB "):
            f = line.split()
            limbs[f[1]] = f[2]
    res = [l for l in r.stdout.splitlines() if l.startswith("KNOWLEDGE-METER-RESULT")]
    return {"rc": r.returncode, "limbs": limbs, "result_line": bool(res),
            "verdict": "pass" if r.returncode == 0 else "fail",
            "stderr_tail": r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""}


def main():
    os.makedirs(MAPS, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    rmap = json.load(open(MAP))
    fsha = sha(MAP)
    assert fsha == "dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12", fsha

    # ---- frozen map variants (byte-identical construction to the frozen script)
    order = sorted(rmap)
    half = {x: rmap[x] for x in order[: len(order) // 2]}
    half_p = MAPS + "/half.json"
    with open(half_p, "w") as fh:
        json.dump(half, fh)
    wrong = dict(rmap)
    assert "S071.txt:117" in wrong
    wrong["S071.txt:117"] = "corpus/source-snapshots/round-44/S069.txt:117"
    wrong_p = MAPS + "/wrongfile.json"
    with open(wrong_p, "w") as fh:
        json.dump(wrong, fh, indent=1, sort_keys=True)
    wsha = sha(wrong_p)
    assert wsha == "569b18fb06be07e10b7dcbf7ed6ee360ba3b4ba40b3847bff80fd35ba37dfce7", wsha

    # ---- frozen trees
    dn = fresh("dn")
    pos = fresh("pos")
    npos = apply_map(pos, MAP)
    half_t = fresh("half")
    apply_map(half_t, half_p)
    decite = fresh("decite")
    for fn in sorted(os.listdir(os.path.join(decite, "corpus", "knowledge"))):
        p = os.path.join(decite, "corpus", "knowledge", fn)
        t = open(p, encoding="utf-8").read()
        n = t
        for k in rmap:
            n = n.replace("`%s`" % k, k)
        if n != t:
            open(p, "w", encoding="utf-8").write(n)
    pad = fresh("pad")
    shutil.copytree(os.path.join(pos, "corpus", "knowledge"),
                    os.path.join(pad, "corpus", "knowledge"), dirs_exist_ok=True)
    with open(os.path.join(pad, "corpus", "knowledge", "claim-gates.md"), "a", encoding="utf-8") as fh:
        fh.write("\n`corpus/SOURCES.md`\n`corpus/instruments/resolve.py`\n")
    wrong_t = fresh("wrong")
    apply_map(wrong_t, wrong_p)

    # ---- extension: prose (M3 line equality only)
    prose = fresh("prose")
    apply_map(prose, MAP)
    pk = os.path.join(prose, "corpus", "knowledge", "ai-assisted-finding-validation.md")
    pt = open(pk, encoding="utf-8").read().split("\n")
    done = False
    for i, line in enumerate(pt):
        if " the " in line and "`" not in line:
            pt[i] = line.replace(" the ", " teh ", 1)
            done = True
            break
    assert done, "no prose line"
    open(pk, "w", encoding="utf-8").write("\n".join(pt))

    # ---- extension: ghost (M3 file set only)
    ghost = fresh("ghost")
    apply_map(ghost, MAP)
    with open(os.path.join(ghost, "corpus", "knowledge", "meter-ghost.md"), "w", encoding="utf-8") as fh:
        fh.write("meter ghost note without any citation or path\n")

    # ---- extension: stale-anchor truncations (M5 range only)
    stale_lo = fresh("stale-lo")
    apply_map(stale_lo, MAP)
    snap = os.path.join(stale_lo, "corpus", "source-snapshots", "round-45", "S071.txt")
    t = open(snap, encoding="utf-8").read().split("\n")
    open(snap, "w", encoding="utf-8").write("\n".join(t[:100]))
    stale_hi = fresh("stale-range")
    apply_map(stale_hi, MAP)
    snap2 = os.path.join(stale_hi, "corpus", "source-snapshots", "round-45", "S071.txt")
    t2 = open(snap2, encoding="utf-8").read().split("\n")
    open(snap2, "w", encoding="utf-8").write("\n".join(t2[:371]))

    # ---- extension maps: uniq (M4 uniqueness), keym (M4 KEY match)
    spec = importlib.util.spec_from_file_location("km", COUNTER)
    km = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(km)
    R = km.load_resolve(pos)
    bcls = km.classify_scope(R, pos, km.scope_files_rev(pos, B), WORK)
    base_tokens = set(bcls)
    bfiles = km.scope_files_rev(pos, B)
    base_text = "\n".join(bfiles.values())
    tracked = [p for p in km.git(pos, "ls-files").split("\n") if p]
    by = {}
    for p in tracked:
        by.setdefault(p.rsplit("/", 1)[-1], []).append(p)

    def nlines(p):
        return len(open(os.path.join(pos, p), encoding="utf-8").read().splitlines())

    # frozen key to drop: its value must not be a base token (keeps rate arithmetic intact)
    drop = [k for k in sorted(rmap) if rmap[k] not in base_tokens]
    assert drop, "no droppable key"
    K = drop[0]

    # uniqueness candidate: cited GONE token whose basename has >1 tracked copies,
    # anchor in range for a snapshot copy, value new, token backticked in base text.
    uniq_c = None
    for cit in sorted(bcls):
        if bcls[cit] != "GONE" or cit in rmap:
            continue
        m = km.KEY.match(cit)
        if not m or ":" not in cit:
            continue
        name, lo, hi = m.group(1), m.group(2), m.group(3)
        anchors = cit[len(name):]
        copies = [p for p in by.get(name, []) if p.startswith("corpus/source-snapshots/")]
        if len(by.get(name, [])) < 2 or not copies:
            continue
        hi_i = int(hi) if hi else int(lo)
        for p in copies:
            val = p + anchors
            if nlines(p) >= hi_i and val not in base_tokens and ("`%s`" % cit) in base_text:
                uniq_c = (cit, val, len(by[name]))
                break
        if uniq_c:
            break
    assert uniq_c, "no uniqueness candidate"
    uniq = dict(rmap)
    del uniq[K]
    uniq[uniq_c[0]] = uniq_c[1]
    assert len(uniq) == len(rmap)
    uniq_p = MAPS + "/uniq.json"
    with open(uniq_p, "w") as fh:
        json.dump(uniq, fh, indent=1, sort_keys=True)

    # non-KEY key: a cited GONE token that does not match KEY, value a resolving new token
    key_c = None
    for cand in ["corpus/knowledge/claim-gates.md", "corpus/knowledge/citation-bases.md",
                 "corpus/SOURCES.md", "corpus/knowledge/claim-package-contract.md"]:
        if cand in base_tokens:
            continue
        if not os.path.isfile(os.path.join(pos, cand)):
            continue
        if R.classify(cand, pos, os.path.expanduser(R.MIRROR_ROOT))[0] != "INTERNAL":
            continue
        key_c = cand
        break
    assert key_c, "no resolving new value token"
    nk = None
    for cit in sorted(bcls):
        if bcls[cit] != "GONE" or cit in rmap or km.KEY.match(cit):
            continue
        if ("`%s`" % cit) in base_text:
            nk = cit
            break
    assert nk, "no non-KEY GONE cited token"
    keym = dict(rmap)
    del keym[K]
    keym[nk] = key_c
    assert len(keym) == len(rmap)
    keym_p = MAPS + "/keym.json"
    with open(keym_p, "w") as fh:
        json.dump(keym, fh, indent=1, sort_keys=True)

    uniq_t = fresh("uniq")
    apply_map(uniq_t, uniq_p)
    keym_t = fresh("keym")
    apply_map(keym_t, keym_p)

    # ---- control definitions
    fake_sha = fsha[:8] + "0" * 56
    controls = [
        {"name": "do-nothing", "tree": dn, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "positive", "tree": pos, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "pass"},
        {"name": "partial", "tree": half_t, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "decite", "tree": decite, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "pad", "tree": pad, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "wrong-file", "tree": wrong_t, "map": wrong_p, "target": "596/1716", "sha": wsha, "expect": "fail"},
        {"name": "map-sha", "tree": pos, "map": MAP, "target": "596/1716",
         "sha": "0" * 64, "expect": "fail"},
        # extensions
        {"name": "tgt-den", "tree": pos, "map": MAP, "target": "596/1717", "sha": fsha, "expect": "fail"},
        {"name": "tgt-lo", "tree": pos, "map": MAP, "target": "595/1715", "sha": fsha, "expect": "fail"},
        {"name": "prose", "tree": prose, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "ghost", "tree": ghost, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "stale-lo", "tree": stale_lo, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "stale-range", "tree": stale_hi, "map": MAP, "target": "596/1716", "sha": fsha, "expect": "fail"},
        {"name": "uniq", "tree": uniq_t, "map": uniq_p, "target": "596/1716", "sha": sha(uniq_p), "expect": "fail"},
        {"name": "keym", "tree": keym_t, "map": keym_p, "target": "596/1716", "sha": sha(keym_p), "expect": "fail"},
        {"name": "mapsha-prefix", "tree": pos, "map": MAP, "target": "596/1716",
         "sha": fake_sha, "expect": "fail"},
        {"name": "result-assert", "tree": wrong_t, "map": wrong_p, "target": "596/1716",
         "sha": wsha, "expect": "fail", "assert_result": True},
    ]
    with open(S + "/controls.json", "w") as fh:
        json.dump({"base_rev": B, "counter": COUNTER, "controls": controls}, fh, indent=1)

    print("pos_knowledge_applied=%d" % npos)
    print("dropped_key=%s -> %s | uniq_token=%r value=%s copies=%d | nonkey=%r value=%s"
          % (K, rmap[K], uniq_c[0], uniq_c[1], uniq_c[2], nk, key_c))
    print("map_shas: frozen=%s half=%s wrong=%s uniq=%s keym=%s" % (
        fsha, sha(half_p), wsha, sha(uniq_p), sha(keym_p)))
    # pristine expectations for the extension controls must be exact
    for c in controls:
        r = meter(c)
        print("EXPECT %-13s verdict=%s limbs=%s result=%s %s" % (
            c["name"], r["verdict"], ",".join("%s:%s" % kv for kv in sorted(r["limbs"].items()) if kv[1] == "FAIL"),
            r["result_line"], c["expect"]))
        if r["verdict"] != c["expect"]:
            raise SystemExit("control %s pristine verdict %s != expected %s" % (c["name"], r["verdict"], c["expect"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
