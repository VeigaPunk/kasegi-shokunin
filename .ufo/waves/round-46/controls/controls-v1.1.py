#!/usr/bin/env python3
"""Round-46 v1.1 control battery: one mutation per control on the GOOD tree (the committed tip), each expected RED.

usage: controls-v1.1.py --lane LANE --tip TIPREV --base BASEREV --freeze FREEZEREV --work SCRATCH

GOOD tree = `git archive TIPREV corpus` (counters 7/7 there; both counters run from LANE's own corpus/instruments,
never from a tree).  Every control is run twice:
  v1.1 column: LANE's counters (the integrated gates), on the tip tree + one mutation.
  v1   column: the FROZEN counters (`git show FREEZEREV:corpus/instruments/r46-c{1,2}-gate.py`) placed in a scratch
               tools dir that is a copy of LANE's instruments, on the same mutation.  Two v1-only adjustments, because v1
               could never read 7/7 on a tree that satisfies the other counter (counter-errata C2-E5): the v1 C1 trees
               carry the v1 gate file (the tree's own copy is what v1 executes), and the v1 C2 trees carry the two
               entries C1 re-grounds at BASE bytes (v1 byte-pinned all 64 base entries).
A control is RED when the counter exits non-zero AND (hostile-line control only) the benign scratch marker was never created; otherwise it is GREEN (false-green).
Output: one `== <control>` block per control (both columns, the counters' own gate lines, exit=<n>), then the v1
false-green list, `v1 total=.. red=.. green=..`, and last `controls total=N red=R green=G` (v1.1 reading).
Exit 0 iff the v1.1 green count is 0.  Stdlib only; read-only on LANE; the scratch work dir is removed on exit.
"""
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--lane", required=True)
ap.add_argument("--tip", required=True)
ap.add_argument("--base", required=True)
ap.add_argument("--freeze", required=True)
ap.add_argument("--work", required=True)
a = ap.parse_args()
lane, work = a.lane, os.path.abspath(a.work)
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work)
TMP = os.path.join(work, "tmp")
os.makedirs(TMP)
C1 = {"v1.1": os.path.join(lane, "corpus/instruments/r46-c1-gate.py")}
C2 = {"v1.1": os.path.join(lane, "corpus/instruments/r46-c2-gate.py")}
LANECD = "cd " + lane + " && "
SEC = "## Re-ground (round 46)"
ENT = ["claim-package-contract.md", "claim-gates.md"]
F28 = "corpus/knowledge/github-private-vulnerability-reporting.md"
COLS = ["v1.1", "v1"]


def sh(cmd, **kw):
    p = subprocess.run(cmd, shell=True, capture_output=True, **kw)
    assert p.returncode == 0, (cmd, p.stderr[-300:])
    return p.stdout


def rd(p): return open(p, encoding="utf-8").read()
def wr(p, t): open(p, "w", encoding="utf-8").write(t)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def export(rev, d):
    os.makedirs(d)
    sh("git -C %s archive %s corpus | tar -x -C %s" % (lane, rev, d))
    return d


# ---- inputs -----------------------------------------------------------------
tipx = export(a.tip, os.path.join(work, "tip-pristine"))
basex = export(a.base, os.path.join(work, "base"))
# v1 tools: a copy of the lane's instruments with the two frozen gates put back
v1root = os.path.join(work, "v1tools")
shutil.copytree(os.path.join(lane, "corpus/instruments"), os.path.join(v1root, "corpus/instruments"), ignore=shutil.ignore_patterns("__pycache__"))
V1GATE = {}
for n in ("r46-c1-gate.py", "r46-c2-gate.py"):
    b = sh("git -C %s show %s:corpus/instruments/%s" % (lane, a.freeze, n))
    p = os.path.join(v1root, "corpus/instruments", n)
    open(p, "wb").write(b)
    V1GATE[n] = p
C1["v1"], C2["v1"] = V1GATE["r46-c1-gate.py"], V1GATE["r46-c2-gate.py"]
HEADER = [
    "tip=%s base=%s freeze=%s" % (a.tip, a.base, a.freeze),
    "v1.1 tools (lane, == tip blobs: %s): c1 %s c2 %s" % (
        "yes" if all(sha(os.path.join(lane, "corpus/instruments", n)) == hashlib.sha256(sh("git -C %s show %s:corpus/instruments/%s" % (lane, a.tip, n))).hexdigest()
                     for n in ("r46-c1-gate.py", "r46-c2-gate.py")) else "NO",
        sha(C1["v1.1"])[:16], sha(C2["v1.1"])[:16]),
    "v1 tools (frozen, git show %s): c1 %s c2 %s" % (a.freeze[:12], sha(C1["v1"])[:16], sha(C2["v1"])[:16]),
]
fakehome = os.path.join(work, "fakehome")
for d in ("bounties", "the-bounty-hunter", "origin-work", "ufo-fsd-alpha"):
    os.makedirs(os.path.join(fakehome, "Projects", d))


def tree(col, name, kind):
    """kind c1: tip tree (+ v1 gate file for the v1 column). kind c2: tip tree (+ the two exempt entries at BASE bytes for v1)."""
    t = os.path.join(work, col, name)
    shutil.copytree(tipx, t, symlinks=True)
    if col == "v1":
        if kind == "c1":
            shutil.copy(C1["v1"], os.path.join(t, "corpus/instruments/r46-c1-gate.py"))
        else:
            for e in ENT:
                shutil.copy(os.path.join(basex, "corpus/knowledge", e), os.path.join(t, "corpus/knowledge", e))
    return t


def kp(t, e): return os.path.join(t, "corpus/knowledge", e)


def sub_recheck(t, e, fn):
    p = kp(t, e)
    wr(p, re.sub(r"^recheck:[ \t]*(.*)$", lambda m: "recheck: " + fn(m.group(1)), rd(p), count=1, flags=re.M))


GATE = lambda e: LANECD + "python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/%s" % e


def run(col, kind, t, env_extra=None):
    exe = (C1 if kind == "c1" else C2)[col]
    cmd = [sys.executable, exe, "--root", t] + (["--baseline", basex, "--work", os.path.join(work, "w-%s" % col)] if kind == "c1" else [])
    os.makedirs(os.path.join(work, "w-%s" % col), exist_ok=True)
    env = dict(os.environ, TMPDIR=TMP)
    env.update(env_extra or {})
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1500, env=env, cwd=work)
    lines = [l for l in (p.stdout + p.stderr).strip().splitlines() if l.startswith(("gate ", "c1-gate", "c2-gate", "r46-c"))]
    return p.returncode, lines


# ---- C1 mutators (on the tip tree) --------------------------------------------
def m_comment(t):
    for e in ENT:
        sub_recheck(t, e, lambda _l: LANECD + "true  # r46-c1-gate.py --entry corpus/knowledge/%s" % e)


def m_cdhome(t):
    for e in ENT:
        sub_recheck(t, e, lambda _l: "cd ~/Projects/bounties && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/%s" % e)


def m_shadow(t):
    for e in ENT:
        p = kp(t, e)
        wr(p, re.sub(r"^(recheck:)", lambda m: "recheck: true\n" + m.group(1), rd(p), count=1, flags=re.M))


def m_planted(t):
    cp = os.path.join(t, "corpus/instruments/claim-package-check.py")
    n0 = len(rd(cp).splitlines())
    wr(cp, rd(cp).rstrip("\n") + "\n# claim-check.mjs L22-24 requires report.md, claim_checklist.md, custodian-receipts.json\n")
    p = kp(t, "claim-package-contract.md")
    s = rd(p)
    i = s.index(SEC)
    head, sec = s[:i], s[i:]
    sec2, k = re.subn(r"^(\| G1 \|[^|]*\| )`corpus/instruments/claim-package-check\.py:[0-9-]+`( \| )`[^`]*`( \|)$",
                      lambda m: m.group(1) + "`corpus/instruments/claim-package-check.py:%d`" % (n0 + 1) + m.group(2) + "`claim-check.mjs L22-24 requires report.md`" + m.group(3),
                      sec, count=1, flags=re.M)
    assert k == 1, "G1 row of claim-package-contract.md not re-anchorable"
    wr(p, head + sec2)


def m_norestore(t):
    for e in ENT:
        p = kp(t, e)
        s, k = re.subn(r"^restoration-recheck:.*\n", "", rd(p), flags=re.M)
        assert k == 1
        wr(p, s)


def m_hollow(t):
    """Rows about the lost claim-check.mjs anchored to the committed gate: each row keeps a real, located, token-bearing anchor,
    but its claim cell is another row's claim (a cyclic shift), so no claim is what its anchor says."""
    for e in ENT:
        p = kp(t, e)
        s = rd(p)
        i = s.index(SEC)
        lines = s[i:].split("\n")
        idx = [j for j, l in enumerate(lines) if re.match(r"^\| G\d+ \|", l)]
        cells = [lines[j].strip().strip("|").split(" | ") for j in idx]
        assert all(len(c) == 4 for c in cells), e
        claims = [c[1] for c in cells]
        claims = claims[1:] + claims[:1]
        for j, c, cl in zip(idx, cells, claims):
            lines[j] = "| " + " | ".join([c[0], cl, c[2], c[3]]) + " |"
        wr(p, s[:i] + "\n".join(lines))


HOSTILE_MARK = os.path.join(work, "marker-hostile")


def m_hostile_for(col):
    mark = HOSTILE_MARK + "-" + col

    def m(t):
        sub_recheck(t, "citation-bases.md", lambda _l: "touch " + mark)
    return m, mark


# ---- C2 mutators ------------------------------------------------------------------
def entry_edit(fn):
    def m(t):
        p = os.path.join(t, F28)
        wr(p, fn(rd(p)))
    return m


def c2_wrongsrc(s):
    s2 = s.replace("--source S073 # 180d", "--source S0730 # 180d")
    assert s2 != s
    return s2


def c2_junkrow(s):
    ls = s.split("\n")
    n = 0
    for i, l in enumerate(ls):
        if re.match(r"^\| (Does the repository's security policy|What route applies|What does the reporter see)", l):
            ls[i] = "| - | - | - |"
            n += 1
    assert n == 3
    return "\n".join(ls)


def c2_emptylimits(s):
    i = s.index("## Limits")
    j = s.index("## Falsifiable package rule")
    return s[:i] + "## Limits\n\n" + s[j:]


def c2_range(s):
    s2 = s.replace("(`S073.txt:578`)", "(`S073.txt:1-589`)", 1)
    assert s2 != s
    return s2


def c2_comment(s):
    ls = s.split("\n")
    n = 0
    for i, l in enumerate(ls):
        if l.startswith("| Is the AI-assistance flag required?") and "I used AI assistance" in l:
            ls[i] = "<!-- " + l + " -->"
            n += 1
    assert n == 1
    return "\n".join(ls)


def m_c2_srcurl(t):
    p = os.path.join(t, "corpus/SOURCES.md")
    s = rd(p)
    u = "https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately"
    i = s.index("| S073 |")
    j = s.index("\n", i)
    row = s[i:j]
    row2 = row.replace(u, "https://evil.example/redirect?to=" + u, 1)
    assert row2 != row
    wr(p, s[:i] + row2 + s[j:])


def m_c2_extrafile(t):
    wr(os.path.join(t, "corpus/knowledge/notes.txt"), "stray non-md file\n")


# ---- control table -------------------------------------------------------------------
# (label, kind, mutator | "HOSTILE" | None, env_extra-fn(col)->dict | None, run on the base export instead of a mutated tip tree)
controls = []


def ctl(label, kind, mut, env=None, base_tree=False):
    controls.append((label, kind, mut, env, base_tree))


ctl("c1 do-nothing (tree = baseline = base export)", "c1", None, base_tree=True)
ctl("c1 comment-trick (`cd LANE && true  # r46-c1-gate.py --entry ...`, valid rows kept)", "c1", m_comment)
ctl("c1 cd-home (`cd ~/Projects/bounties && python3 corpus/instruments/r46-c1-gate.py --entry ...`)", "c1", m_cdhome)
ctl("c1 shadow-recheck (`recheck: true` line above the real gate line)", "c1", m_shadow)
ctl("c1 planted-anchor (comment appended to claim-package-check.py, contract G1 re-anchored on it)", "c1", m_planted)
ctl("c1 restoration-recheck removed (both entries)", "c1", m_norestore)
ctl("c1 hollow-rows (claim cells rotated: rows about the lost claim-check.mjs anchored to the committed gate)", "c1", m_hollow)
ctl("c1 hostile-line (`recheck: touch <scratch marker>` in unrelated citation-bases.md; marker must not be created)", "c1", "HOSTILE")
ctl("c1 home-override (do-nothing tree under a scratch HOME that holds ~/Projects/bounties)", "c1", None,
    env=lambda col: {"HOME": fakehome}, base_tree=True)
ctl("c2 do-nothing (base export)", "c2", None, base_tree=True)
ctl("c2 wrong-source recheck (`--source S0730`)", "c2", entry_edit(c2_wrongsrc))
ctl("c2 junk-table-rows (three real rows replaced by `| - | - | - |`)", "c2", entry_edit(c2_junkrow))
ctl("c2 emptied-Limits (heading kept, body deleted)", "c2", entry_edit(c2_emptylimits))
ctl("c2 source-cell URL wrapped in another host (SOURCES.md S073 row)", "c2", m_c2_srcurl)
ctl("c2 citation-range 1-589 (one cite widened to the whole capture)", "c2", entry_edit(c2_range))
ctl("c2 core-in-HTML-comment (the AI-assistance row wrapped in <!-- -->)", "c2", entry_edit(c2_comment))
ctl("c2 extra-non-md-file (corpus/knowledge/notes.txt)", "c2", m_c2_extrafile)

out = list(HEADER)

# ---- sanity (NOT controls): good tree must read 7/7 ---------------------------------
for kind in ("c1", "c2"):
    t = tree("v1.1", "good-" + kind, kind)
    rc, ls = run("v1.1", kind, t)
    out.append("-- good tip tree, v1.1 %s (sanity, not a control)" % kind)
    out.extend("   " + l for l in ls)
    out.append("   exit=%d" % rc)
    assert rc == 0, "good tree is not 7/7 under v1.1 %s" % kind
    tv = tree("v1", "good-" + kind, kind)
    rc, ls = run("v1", kind, tv)
    out.append("-- good tree for v1 %s (sanity, not a control)" % kind)
    out.extend("   " + l for l in ls)
    out.append("   exit=%d" % rc)
t = tree("v1.1", "tip-as-is-for-v1-c2", "c2")
rc, ls = run("v1", "c2", t)
out.append("-- info: v1 C2 on the UNMODIFIED tip tree (the two re-grounded entries differ from BASE; counter-errata C2-E5)")
out.extend("   " + l for l in ls)
out.append("   exit=%d" % rc)

# ---- controls -------------------------------------------------------------------------
res = {"v1.1": [0, 0], "v1": [0, 0]}  # red, green
v1_green, v11_green = [], []
out.append("")
for label, kind, mut, env, base_tree in controls:
    out.append("== " + label)
    reds = {}
    for col in COLS:
        if mut == "HOSTILE":
            m, mark = m_hostile_for(col)
            if os.path.exists(mark):
                os.remove(mark)
        else:
            m, mark = mut, None
        if base_tree:
            t = os.path.join(work, col, "do-nothing-" + kind + ("-env" if env else ""))
            shutil.copytree(basex, t, symlinks=True)
        else:
            t = tree(col, re.sub(r"\W+", "-", label)[:40], kind)
            m(t)
        rc, ls = run(col, kind, t, env(col) if env else None)
        ok_assert, aline = True, None
        if mark is not None:
            created = os.path.exists(mark)
            ok_assert, aline = (not created), "marker-created=%d" % int(created)
        red = rc != 0 and ok_assert
        reds[col] = red
        for l in ls:
            out.append("%-5s %s" % (col, l))
        if aline:
            out.append("%-5s %s" % (col, aline))
        out.append("%-5s exit=%d reads=%s" % (col, rc, "RED" if red else "GREEN"))
        res[col][0 if red else 1] += 1
    out.append("")
    short = label.split(" (")[0]
    if reds["v1.1"] and not reds["v1"]:
        v1_green.append(short)
    if not reds["v1.1"]:
        v11_green.append(short)

n = len(controls)
out.append("v1 false-greens (green under v1, red under v1.1; the red-before evidence for the errata): %s" %
           ("; ".join(v1_green) or "none"))
out.append("v1.1 greens (must be none): %s" % ("; ".join(v11_green) or "none"))
out.append("v1 total=%d red=%d green=%d" % (n, res["v1"][0], res["v1"][1]))
out.append("controls total=%d red=%d green=%d" % (n, res["v1.1"][0], res["v1.1"][1]))
print("\n".join(out))
shutil.rmtree(work, ignore_errors=True)
sys.exit(0 if res["v1.1"][1] == 0 else 1)
