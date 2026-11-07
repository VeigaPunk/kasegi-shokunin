import hashlib, json, os, subprocess, sys
S = "/fast/scratch/hyaku/kasegi-r92/MutC1Counter"
L = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C = S + "/c1clone"
BASE = "0628fd247914555838a42c02ba5d4ac08b7e095d"
LANDING = "cb1ef2b9856df79c530f3ff1374fa9691ff56233"
LAB = "d0bd4758a41919b2c86c079f3a1a2dfb392dcd8d"
LABPATH = ".ufo/waves/round-91/w1/ReviewC1Labels-receipts/round92-labels.tsv"
FROZEN = S + "/W/c1/repair-map.tsv"
FMAP = open(FROZEN, encoding="utf-8").read()
MAPSHA = "6d87cafaec99961a15c00967d30c2bb164ed480d8b3fbaeadccd55b048d9b772"
TRIAGE = "corpus/knowledge/triage-thresholds.md"

def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, check=True, **kw).stdout

def fresh(rev, cwd=C):
    subprocess.run(["git", "-C", cwd, "checkout", "-q", "-f", "--detach", rev], check=True)
    subprocess.run(["git", "-C", cwd, "clean", "-fdq"], check=True)

def commit(msg, cwd=C):
    subprocess.run(["git", "-C", cwd, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "commit", "-q", "--allow-empty", "-am", msg], check=True)
    return sh(["git", "-C", cwd, "rev-parse", "HEAD"]).strip()

def write(p, text):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)

def add_all(cwd=C):
    subprocess.run(["git", "-C", cwd, "add", "-A"], check=True)

def mapfile(name, text):
    p = S + "/" + name
    write(p, text)
    return p

def mapsha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def frozen_rows():
    return [ln for ln in FMAP.split("\n") if ln.strip() and not ln.startswith("#")]

def rowmap(repl):
    """repl: dict site -> (key, old, new) replacement for that row (key match required)."""
    out = []
    for ln in frozen_rows():
        site, key, old, new = ln.split("\t")
        if site in repl and repl[site][0] == key:
            _, old, new = repl[site]
        out.append("\t".join([site, key, old, new]))
    return "\n".join(out) + "\n"

def apply_map(root, mappath):
    sh(["python3", "-B", S + "/W/c1/apply-map.py", "--root", root, "--map", mappath])

def run(tag, script, lane, base, after, mp, labels, base_target, target, msha, *_extra):
    work = S + "/work/pc-" + tag
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-B", script, "--lane", lane, "--base-rev", base,
           "--after-rev", after, "--map", mp, "--labels-rev", labels,
           "--base-target", base_target, "--target", target,
           "--map-sha256", msha, "--work", work]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    lines = [x for x in (r.stdout + r.stderr).splitlines() if x.strip()]
    res = next((x for x in reversed(lines) if x.startswith("KNOWLEDGE-METER-RESULT")), "NO-RESULT")
    limbs = {}
    for x in lines:
        if x.startswith("LIMB "):
            p = x.split()
            limbs[p[1]] = (p[2], " ".join(p[3:]))
    write(S + "/out/pc-%s.log" % tag, "\n".join(lines) + "\n")
    return res, limbs

def build(rev_for_labels=None):
    out = {}
    # PC-F: labels rev with EXCLUDED row 437 removed
    fresh(LAB)
    lp = os.path.join(C, LABPATH)
    text = open(lp, encoding="utf-8").read()
    kept = [ln for ln in text.split("\n")
            if not ln.startswith("corpus/knowledge/triage-thresholds.md:437\t")]
    assert len(kept) == len(text.split("\n")) - 1
    write(lp, "\n".join(kept))
    out["F"] = {"labels": commit("fixture: labels minus 437"), "after": LANDING,
                "map": FROZEN, "sha": MAPSHA, "target": "960/1944"}
    # PC-L: labels row 59 qualifies to a different key anchor
    fresh(LAB)
    text = open(lp, encoding="utf-8").read()
    lines = text.split("\n")
    hit = 0
    for i, ln in enumerate(lines):
        c = ln.split("\t")
        if len(c) == 5 and c[0] == "corpus/knowledge/triage-thresholds.md:59":
            assert c[1] == "mission-control.md:20-21"
            c[3] = c[3].replace("corpus/knowledge/mission-control.md:20-21",
                                "corpus/knowledge/mission-control.md:19-21", 1)
            lines[i] = "\t".join(c); hit += 1
    assert hit == 1
    write(lp, "\n".join(lines))
    out["L"] = {"labels": commit("fixture: row 59 qualify cross-key"), "after": LANDING,
                "map": FROZEN, "sha": MAPSHA, "target": "960/1944"}
    # PC-M: labels row 90 repoints to an overlong anchor
    fresh(LAB)
    text = open(lp, encoding="utf-8").read(); lines = text.split("\n"); hit = 0
    for i, ln in enumerate(lines):
        c = ln.split("\t")
        if len(c) == 5 and c[0] == "corpus/knowledge/triage-thresholds.md:90":
            assert c[1] == "mission-control.md:20-21"
            c[2] = "corpus/knowledge/mission-control.md:1-9999"
            c[3] = "Repoint to 1-9999 (fixture: overlong anchor)."
            lines[i] = "\t".join(c); hit += 1
    assert hit == 1
    write(lp, "\n".join(lines))
    out["M"] = {"labels": commit("fixture: row 90 overlong anchor"), "after": LANDING,
                "target": "960/1944"}
    mpm = mapfile("pc-M-map.tsv", rowmap({TRIAGE + ":90": ("mission-control.md:20-21",
                                                         "`mission-control.md:20-21`",
                                                         "`corpus/knowledge/mission-control.md:1-9999`")}))
    fresh(BASE); apply_map(C, mpm)
    out["M"]["after"] = commit("fixture: row 90 overlong edit"); out["M"]["map"] = mpm
    out["M"]["sha"] = mapsha(mpm)
    # PC-K: labels row for (437, mission-control.md:37-38) named-cell; after replaces 437's last cell
    fresh(LAB)
    text = open(lp, encoding="utf-8").read()
    base_line = sh(["git", "-C", C, "show", BASE + ":" + TRIAGE]).split("\n")[436]
    cells = base_line.rstrip().split("|")
    cell = cells[-2].strip()
    assert cell and "mission-control.md:37-38" not in cell
    row = "\t".join(["corpus/knowledge/triage-thresholds.md:437", "mission-control.md:37-38",
                     "content-repair",
                     "Replace with mission-control.md:56-57 (fixture: drop the stale clause).",
                     "fixture"])
    write(lp, text.rstrip("\n") + "\n" + row + "\n")
    out["K"] = {"labels": commit("fixture: named-cell row on 437"), "target": None}
    mapp = mapfile("pc-K-map.tsv", FMAP.rstrip("\n") + "\n" + "\t".join(
        ["corpus/knowledge/triage-thresholds.md:437", "mission-control.md:37-38", cell,
         "MATCHES: `corpus/knowledge/mission-control.md:56-57`"]) + "\n")
    fresh(BASE); apply_map(C, FROZEN)
    tp = os.path.join(C, TRIAGE); tl = open(tp, encoding="utf-8").read().split("\n")
    assert tl[436].count(cell) == 1
    tl[436] = tl[436].replace(cell, "MATCHES: `corpus/knowledge/mission-control.md:56-57`", 1)
    write(tp, "\n".join(tl))
    out["K"]["after"] = commit("fixture: 437 last-cell named"); out["K"]["map"] = mapp
    out["K"]["sha"] = mapsha(mapp)
    # PC-G: candidate edits + an extra non-scope file sharing a target basename
    fresh(BASE); apply_map(C, FROZEN)
    write(os.path.join(C, "corpus/other/mission-control.md"), "fixture basename collision\n")
    add_all()
    out["G"] = {"labels": LAB, "after": commit("fixture: extra basename"), "map": FROZEN,
                "sha": MAPSHA, "target": "960/1944"}
    # PC-I: candidate edits + an extra (uncited) scope file
    fresh(BASE); apply_map(C, FROZEN)
    write(os.path.join(C, "corpus/knowledge/zz-extra.md"), "fixture extra scope file\n")
    add_all()
    out["I"] = {"labels": LAB, "after": commit("fixture: extra scope file"), "map": FROZEN,
                "sha": MAPSHA, "target": "960/1944"}
    # PC-J: widened old, label-correct new
    fresh(BASE)
    tm = S + "/pc-J-apply.tsv"
    rows = [ln for ln in frozen_rows() if not ln.startswith(TRIAGE + ":86\t")]
    write(tm, "\n".join(rows) + "\n")
    apply_map(C, tm)
    tp = os.path.join(C, TRIAGE); tl = open(tp, encoding="utf-8").read().split("\n")
    old86 = "MATCHES: `intake-surface.md:71`,"
    new86 = "`corpus/knowledge/intake-surface.md:83-88`"
    assert tl[85].count(old86) == 1
    tl[85] = tl[85].replace(old86, new86, 1)
    write(tp, "\n".join(tl))
    mj = mapfile("pc-J-map.tsv", rowmap({TRIAGE + ":86": ("intake-surface.md:71", old86, new86)}))
    out["J"] = {"labels": LAB, "after": commit("fixture: widened old 86"), "map": mj,
                "sha": mapsha(mj), "target": "960/1944"}
    # PC-H: duplicate map row over the candidate tree
    dup = FMAP.rstrip("\n") + "\n" + \
        "\t".join([TRIAGE + ":86", "intake-surface.md:71", "`intake-surface.md:71`",
                   "`corpus/knowledge/intake-surface.md:83-88`"]) + "\n"
    mh = mapfile("pc-H-map.tsv", dup)
    out["H"] = {"labels": LAB, "after": "a7766f406342f6b3df1bd723661060a8df2ce34f",
                "map": mh, "sha": mapsha(mh), "target": "960/1944"}
    fresh(BASE)
    return out

def synthetic(tag, line3, label_row, mrow, after_line, base_target, target):
    D = S + "/fix-" + tag
    subprocess.run(["rm", "-rf", D], check=True)
    os.makedirs(D)
    sh(["git", "-C", D, "init", "-q"])
    assert sh(["git", "-C", D, "rev-parse", "--show-toplevel"]).strip() == D
    write(os.path.join(D, "corpus/instruments/resolve.py"),
          sh(["git", "-C", L, "show", BASE + ":corpus/instruments/resolve.py"]))
    xmd = "# x\n\n" + line3 + "\n"
    write(os.path.join(D, "corpus/knowledge/x.md"), xmd)
    ex1 = "\t".join(["corpus/knowledge/triage-thresholds.md:437", "intake-surface.md:75-76", "content-repair",
                     "Replace with intake-surface.md:89-90 (fixture).", "fixture"])
    ex2 = "\t".join(["corpus/knowledge/triage-thresholds.md:438", "mission-control.md:37-38", "content-repair",
                     "Replace with mission-control.md:56-57 (fixture).", "fixture"])
    labels = "line\tkey\tlabel\tfix\tevidence\n" + label_row + "\n" + ex1 + "\n" + ex2 + "\n"
    write(os.path.join(D, LABPATH), labels)
    subprocess.run(["git", "-C", D, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "add", "-A"], check=True)
    base = commit("fixture base", cwd=D)
    write(os.path.join(D, "corpus/knowledge/x.md"), "# x\n\n" + after_line + "\n")
    subprocess.run(["git", "-C", D, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "add", "-A"], check=True)
    after = commit("fixture after", cwd=D)
    mp = mapfile("pc-%s-map.tsv" % tag, mrow + "\n")
    return {"lane": D, "base": base, "after": after, "map": mp, "sha": mapsha(mp),
            "labels": base, "target": target, "base_target": base_target}

if __name__ == "__main__":
    real = build()
    import re as _re
    for _pc in ("K", "M"):
        run(_pc + "pre", S + "/W/c1/knowledge-meter.py", C, BASE, real[_pc]["after"],
            real[_pc]["map"], real[_pc]["labels"], "947/1947", "0/0", real[_pc]["sha"])
        _log = open(S + "/out/pc-%spre.log" % _pc, encoding="utf-8").read()
        _m = _re.search(r"base=(\d+/\d+) after=(\d+/\d+)", _log)
        assert _m
        real[_pc]["target"] = _m.group(2)
        print("PC-%s after rate:" % _pc, _m.group(2))
    json.dump(real, open(S + "/pc-fixtures.json", "w"), indent=1, sort_keys=True)
    # PC-N: named-cell on a line with pipes but no trailing pipe
    nrow = "\t".join(["corpus/knowledge/x.md:3", "x.md:1", "content-repair",
                      "Replace with x.md:2 (fixture: drop the stale clause).", "fixture"])
    nmap = "\t".join(["corpus/knowledge/x.md:3", "x.md:1", "b `x.md:1`",
                      "MATCHES: `corpus/knowledge/x.md:2`"])
    PCN = synthetic("n", "a | b `x.md:1` | tail", nrow, nmap,
                    "a | MATCHES: `corpus/knowledge/x.md:2` | tail", "0/1", "1/1")
    # PC-O: duplicate old token on the base line
    orow = "\t".join(["corpus/knowledge/x.md:3", "x.md:1", "corpus/knowledge/x.md:1",
                      "Repoint (fixture: duplicate old).", "fixture"])
    omap = "\t".join(["corpus/knowledge/x.md:3", "x.md:1", "`x.md:1`", "`corpus/knowledge/x.md:1`"])
    PCO = synthetic("o", "`x.md:1` and `x.md:1` again", orow, omap,
                    "`corpus/knowledge/x.md:1` and `x.md:1` again", "0/1", "1/2")
    # PC-RU2: labels with an unknown-kind pair
    fresh(LAB)
    lp = os.path.join(C, LABPATH)
    text = open(lp, encoding="utf-8").read()
    urow = "\t".join([TRIAGE + ":58", "claim-gates.md:99-100", "content-repair",
                      "Repoint later.", "fixture"])
    write(lp, text.rstrip("\n") + "\n" + urow + "\n")
    revU = commit("fixture: unknown-kind label")
    fresh(BASE)
    pc = {k: v for k, v in real.items()}
    # run pristine and targeted mutants
    PR = S + "/W/c1/knowledge-meter.py"
    def mut(n): return S + "/mut/" + n + ".py"
    jobs = []
    def add(tag, script, lane, base, after, mp, labels, base_target, target, msha, pcid):
        jobs.append((tag, script, lane, base, after, mp, labels, base_target, target, msha, pcid))
    def add_real(pcid, mutant=None):
        v = real[pcid]
        tgt = v["target"]
        msha = v["sha"]
        # if target unknown, probe with 0/0 to read the after rate from a pristine run
        add(pcid, PR, C, BASE, v["after"], v["map"], v["labels"], "947/1947", tgt or "0/0", msha, pcid)
        if mutant:
            add(pcid + "-" + mutant, mut(mutant), C, BASE, v["after"], v["map"], v["labels"],
                "947/1947", tgt or "0/0", msha, pcid)
    # A/B/C: argument controls on the landing tree
    add("A", PR, L, BASE, LANDING, FROZEN, LAB, "947/1947", "960/1944", "0" * 64, "A")
    add("B", PR, L, BASE, LANDING, FROZEN, LAB, "948/1947", "960/1944", MAPSHA, "B")
    add("C", PR, L, BASE, LANDING, FROZEN, LAB, "947/1947", "961/1944", MAPSHA, "C")
    # D/E: existing control variants with their own map sha and matching target
    add_real_d = None
    jobs.append(("D", PR, C, BASE, "5a6463cc5e7ace19085c91a949163bfd51a4985d",
                 S + "/map-excluded437.tsv", LAB, "947/1947", "961/1944",
                 mapsha(S + "/map-excluded437.tsv"), "D"))
    jobs.append(("D-m12", mut("m12_m10_unlabelled_off"), C, BASE,
                 "5a6463cc5e7ace19085c91a949163bfd51a4985d", S + "/map-excluded437.tsv", LAB,
                 "947/1947", "961/1944", mapsha(S + "/map-excluded437.tsv"), "D"))
    jobs.append(("E", PR, C, BASE, "68a09d7c63bd1e0266d4660b6ba0203bf951f285",
                 S + "/map-partial.tsv", LAB, "947/1947", "959/1944",
                 mapsha(S + "/map-partial.tsv"), "E"))
    jobs.append(("E-m13", mut("m13_m10_unapplied_off"), C, BASE,
                 "68a09d7c63bd1e0266d4660b6ba0203bf951f285", S + "/map-partial.tsv", LAB,
                 "947/1947", "959/1944", mapsha(S + "/map-partial.tsv"), "E"))
    for pcid, mname in [("F", "m15_m10_excluded_subset_off"), ("L", "m01_qualify_key_equality"),
                        ("M", "m27_m5_hi_off"), ("M", "m28_m5_off"), ("K", "m20_m4_key_in_old_off"),
                        ("G", "m19_m4_bybase_member"), ("I", "m23_m3_samefiles_true"),
                        ("J", "m11_m9_new_only"), ("H", "m22_m3_dup_off")]:
        add_real(pcid, mname)
    for pcid in ("F", "L", "M", "K", "G", "I", "J", "H"):
        add_real(pcid, None)
    for tag, pc in (("N", PCN), ("O", PCO)):
        jobs.append((tag, PR, pc["lane"], pc["base"], pc["after"], pc["map"], pc["labels"],
                     pc["base_target"], pc["target"], pc["sha"], tag))
        jobs.append((tag + "-m" + ("05" if tag == "N" else "21"), 
                     mut("m05_lastcell_guard" if tag == "N" else "m21_m3_oldcount_zero"),
                     pc["lane"], pc["base"], pc["after"], pc["map"], pc["labels"],
                     pc["base_target"], pc["target"], pc["sha"], tag))
    # redundancy probes
    jobs.append(("RU-m10", mut("m10_m9_excluded_off"), C, BASE,
                 "5a6463cc5e7ace19085c91a949163bfd51a4985d", S + "/map-excluded437.tsv", LAB,
                 "947/1947", "961/1944", mapsha(S + "/map-excluded437.tsv"), "RU"))
    jobs.append(("RU2", PR, C, BASE, LANDING, FROZEN, revU, "947/1947", "960/1944", MAPSHA, "RU2"))
    jobs.append(("RU2-m14", mut("m14_m10_unknown_off"), C, BASE, LANDING, FROZEN, revU,
                 "947/1947", "960/1944", MAPSHA, "RU2"))
    import concurrent.futures
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        fut = {ex.submit(run, *j): j[0] for j in jobs}
        for f in concurrent.futures.as_completed(fut):
            tag = fut[f]
            out[tag] = f.result()
    json.dump({k: [v[0], v[1]] for k, v in out.items()}, open(S + "/pc-results.json", "w"), indent=1, sort_keys=True)
    for tag in sorted(out):
        res, limbs = out[tag]
        fails = ",".join("%s" % k for k, (st, _) in limbs.items() if st == "FAIL")
        print("%-12s %-45s fails=%s" % (tag, res, fails or "-"))
