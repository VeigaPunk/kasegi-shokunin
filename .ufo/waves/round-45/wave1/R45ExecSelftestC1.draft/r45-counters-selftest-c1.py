#!/usr/bin/env python3
"""r45-counters-selftest-c1.py — mutation selftest for the frozen round-45 C1 counter
(corpus/instruments/r45-routed-defects.py).  DRAFT; the L1 integrates.  stdlib only.

WHAT IT DOES
  1. Builds in scratch a COMPLETE synthetic tree (GOOD) on top of an export of the
     frozen base: every artifact a limb R1..R5 binds is genuinely written
       R1  S072 row in corpus/SOURCES.md, corpus/source-snapshots/round-45/{S072.txt,
           S071.txt,manifest.json} copied byte-for-byte from the lane, an appended
           `Correction (round 45` line in corpus/lessons/round-44.md
       R2  an append-only `## Round-45 additions` block in corpus/QUALITY.md (R47/R48/R49)
       R3  a working r44-frontier-count.py WITH --selftest (8 real cases), the SKILL.md
           `## Round-45 Gates & probes registry addition` table, an instruments README row
       R4  a working freeze-check.py (own minimal implementation, 8 real cases, replays
           the claims file at the base) + the real claims.json + r45 counters
       R5  .ufo/waves/round-44/controls/final-attempt3-refiled.txt whose output comes from a
           REAL run of r44-routed-defects.py --selftest in the tree
     and asserts the frozen counter prints fixed=5 on it.
  2. Controls: do-nothing base (fixed=0), marker-only tree (fixed=0), a null mutant
     (unchanged clone; must stay fixed=5 so the harness cannot pass by flagging everything).
  3. MUTANTS: each is a hardlink clone of GOOD with ONE limb's bound artifact broken while
     the prose marker stays.  A mutant is REJECTED when the targeted limb reads fixed=0, the
     total drops by exactly one and no other limb changes.  Anything else is a failure:
     FALSE-GREEN (target limb still fixed=1: the counter did not reject) or COLLATERAL.
  Output: one `case ...` line per case, `FALSE-GREEN ...` recipes, then
          `selftest cases=<N> failures=<F>` (exit 0 only when F=0).

USAGE
  python3 r45-counters-selftest-c1.py [--lane DIR] [--base DIR] [--counter PATH] [--only ID,ID] [--keep]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "/fast/scratch/hyaku/kasegi-r45/L1/pure"
SNAP = "corpus/source-snapshots/round-45"
LIMB_RX = re.compile(r"^limb (R\d) fixed=([01]) read=(.*)$", re.M)
TOT_RX = re.compile(r"^routed-defects total=(\d+) fixed=(\d+) unresolved=(\d+) exit=([01])$", re.M)

# ----------------------------------------------------------------------------------------
# Own working minimal freeze-check.py (NOT a stub: it replays claims and has a real selftest)
# ----------------------------------------------------------------------------------------
FREEZE_CHECK_SRC = r'''#!/usr/bin/env python3
"""freeze-check.py — replay frozen claim counters on the base (minimal implementation)."""
import argparse, json, os, shlex, subprocess, sys, tempfile

FIELDS = ("counter_cmd", "expect_before", "expect_after")
SELF = os.path.abspath(__file__)


def replay_claim(c, tool_root, base):
    for f in FIELDS:
        if not isinstance(c.get(f), str) or not c[f].strip():
            return False, "missing-" + f, "fields"
    cmd = c["counter_cmd"].replace("{tool}", tool_root).replace("{tree}", base).replace("{base}", base)
    env = dict(os.environ)
    env["R45_FREEZE_CHECK"] = "1"
    try:
        p = subprocess.run(shlex.split(cmd), cwd=tool_root, capture_output=True, text=True, timeout=300, env=env)
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        return False, "run-error", type(exc).__name__
    lines = [ln.strip() for ln in (p.stdout + p.stderr).splitlines() if ln.strip()]
    if not lines:
        return False, "no-output", "(no output)"
    if c["expect_after"].strip() in lines:
        return False, "already-green", c["expect_after"].strip()
    if c["expect_before"].strip() in lines:
        return True, "ok", c["expect_before"].strip()
    return False, "base-mismatch", lines[-1]


def run_claims(path, tool_root, base):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        claims = data["claims"]
    except (OSError, ValueError, KeyError, TypeError):
        print("freeze-check claims=0 base_ok=0 exit=1")
        return 1
    ok = 0
    for c in claims:
        good, fid, read = replay_claim(c, tool_root, base)
        ok += 1 if good else 0
        print("claim %s base_read=%s verdict=%s finding=%s" % (c.get("id", "?"), read, "ok" if good else "FAIL", fid))
    code = 0 if ok == len(claims) and claims else 1
    print("freeze-check claims=%d base_ok=%d exit=%d" % (len(claims), ok, code))
    return code


COUNTER = (
    "import sys\n"
    "m = sys.argv[1]\n"
    "if m == 'red': print('x fixed=0 exit=1'); sys.exit(1)\n"
    "if m == 'green': print('x fixed=5 exit=0'); sys.exit(0)\n"
    "if m == 'sub': print('x fixed=0x exit=1'); sys.exit(1)\n"
    "if m == 'suffix': print('x fixed=0 exit=1 trailing'); sys.exit(1)\n"
    "raise RuntimeError('boom')\n"
)


def selftest(work):
    work = work or tempfile.mkdtemp(prefix="freeze-selftest-", dir=os.environ.get("TMPDIR"))
    os.makedirs(work, exist_ok=True)
    with open(os.path.join(work, "counter.py"), "w") as fh:
        fh.write(COUNTER)
    with open(os.path.join(work, "README.md"), "w") as fh:
        fh.write("| id | title | status | k |\n|---|---|---|---|\n" +
                 "".join("| F%02d | t | admitted | k |\n" % i for i in range(1, 26)))
    red = "python3 {tool}/counter.py %s"
    good = {"id": "G", "counter_cmd": red % "red", "expect_before": "x fixed=0 exit=1", "expect_after": "x fixed=5 exit=0"}
    cases = [
        ("good-claim", good, 0, "ok"),
        ("r44-frozen-regex-prints-0-not-25", {"id": "D", "counter_cmd": "grep -cE '^\\| F[0-9]+ \\| admitted \\|' {tree}/README.md",
                                              "expect_before": "25", "expect_after": "26"}, 1, "base-mismatch"),
        ("do-nothing-green-at-base", dict(good, counter_cmd=red % "green"), 1, "already-green"),
        ("missing-expect_before", {k: v for k, v in good.items() if k != "expect_before"}, 1, "missing-expect_before"),
        ("counter-crash-no-match", dict(good, counter_cmd=red % "crash"), 1, "base-mismatch"),
        ("substring-fixed=0x", dict(good, counter_cmd=red % "sub"), 1, "base-mismatch"),
        ("trailing-text-not-whole-line", dict(good, counter_cmd=red % "suffix"), 1, "base-mismatch"),
        ("unrunnable-command", dict(good, counter_cmd="/nonexistent/binary-r45"), 1, "run-error"),
    ][:__LIMIT__]
    fails = 0
    for i, (name, claim, want_rc, want_id) in enumerate(cases):
        if i == 0:
            want_id = "__EXP1__"
        cj = os.path.join(work, "claims-%d.json" % i)
        with open(cj, "w") as fh:
            json.dump({"claims": [claim]}, fh)
        p = subprocess.run([sys.executable, SELF, "--claims", cj, "--tool-root", work, "--base", work],
                           capture_output=True, text=True)
        got = "finding=%s" % want_id in p.stdout and p.returncode == want_rc
        fails += 0 if got else 1
        print("selftest case=%s rc=%d want_rc=%d want=%s verdict=%s" % (name, p.returncode, want_rc, want_id, "pass" if got else "fail"))
    print("selftest cases=%d failures=%d" % (len(cases), fails))
    return 1 if fails else 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--claims")
    ap.add_argument("--tool-root")
    ap.add_argument("--base")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.work)
    if not (a.claims and a.tool_root and a.base):
        ap.error("--claims, --tool-root and --base are required")
    return run_claims(a.claims, os.path.abspath(a.tool_root), os.path.abspath(a.base))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''

# ----------------------------------------------------------------------------------------
# r44-frontier-count.py gets a real --selftest patched into the frozen base source
# ----------------------------------------------------------------------------------------
FRONTIER_SELFTEST = r'''
def _readme(rows):
    out = ["| id | frontier | status | knowledge |", "|---|---|---|---|"]
    out += rows
    return "\n".join(out) + "\n"


def selftest(work):
    import subprocess
    import tempfile
    work = work or tempfile.mkdtemp(prefix="frontier-selftest-", dir=os.environ.get("TMPDIR"))
    adm = ["| F%02d | t | admitted | k | s | n |" % i for i in range(1, 27)]

    def fixture(name, lines):
        d = os.path.join(work, name)
        os.makedirs(os.path.join(d, "corpus"), exist_ok=True)
        if lines is not None:
            with open(os.path.join(d, "corpus", "README.md"), "w", encoding="utf-8") as fh:
                fh.write(_readme(lines))
        return d

    def cli(d, *extra):
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "--root", d, *extra], capture_output=True, text=True)
        return p.returncode, p.stdout

    cases = []
    d = fixture("c1", adm)
    r, o = cli(d)
    cases.append(("26-rows-26-admitted", r == 0 and "frontier rows=26 admitted=__EXP_ADMIT__\n" in o))
    d = fixture("c2", adm + ["| F27 | t | admitted | k | s | n |"])
    r, o = cli(d, "--expect", "27")
    cases.append(("plus-one-admitted-expect-27", r == 0 and "frontier rows=27 admitted=27" in o))
    d = fixture("c3", adm)
    r, o = cli(d, "--expect", "27")
    cases.append(("expect-27-on-26-SHORT", r == 1 and "verdict=SHORT" in o))
    d = fixture("c4", adm + ["| F26 | dup | admitted | k | s | n |"])
    r, o = cli(d)
    cases.append(("duplicate-id-DEFECT", r == 1 and "verdict=DEFECT" in o))
    d = fixture("c5", adm[:25] + ["| F26 | t | queued | k | s | n |"])
    r, o = cli(d)
    cases.append(("queued-is-row-not-admitted", r == 0 and "frontier rows=26 admitted=25" in o))
    d = fixture("c6", adm[:3])
    r, o = cli(d)
    cases.append(("header-and-separator-not-counted", r == 0 and "frontier rows=3 admitted=3" in o))
    d = fixture("c7", ["| F01 | admitted | t | k | s | n |"])
    r, o = cli(d)
    cases.append(("status-in-second-cell-not-admitted", r == 0 and "frontier rows=1 admitted=0" in o))
    d = fixture("c8", None)
    r, o = cli(d)
    cases.append(("missing-readme-zero-rows", r == 0 and "frontier rows=0 admitted=0" in o))
    cases = cases[:__LIMIT__]
    fails = 0
    for name, good in cases:
        fails += 0 if good else 1
        print("selftest case=%s verdict=%s" % (name, "pass" if good else "fail"))
    print("selftest cases=%d failures=%d" % (len(cases), fails))
    return 1 if fails else 0

'''


def frontier_src(base_src: str, limit: int = 8, exp_admit: int = 26) -> str:
    s = base_src
    def once(old, new):
        nonlocal s
        assert s.count(old) == 1, old
        s = s.replace(old, new)
    once('    ap.add_argument("--root", required=True)\n',
         '    ap.add_argument("--root", default=None)\n    ap.add_argument("--selftest", action="store_true")\n'
         '    ap.add_argument("--work", default=None)\n')
    once("    args = ap.parse_args(argv)\n",
         '    args = ap.parse_args(argv)\n    if args.selftest:\n        return selftest(args.work)\n'
         '    if args.root is None:\n        ap.error("--root is required")\n')
    once("def main(argv: list[str]) -> int:\n", FRONTIER_SELFTEST.lstrip("\n") + "\ndef main(argv: list[str]) -> int:\n")
    s = s.replace("__LIMIT__", str(limit)).replace("__EXP_ADMIT__", str(exp_admit))
    return s


def freeze_src(limit: int = 8, exp1: str = "ok") -> str:
    return FREEZE_CHECK_SRC.replace("__LIMIT__", str(limit)).replace("__EXP1__", exp1)


STUB_SELFTEST = ('#!/usr/bin/env python3\nimport sys\n'
                 'if "--selftest" in sys.argv:\n    print("selftest cases=8 failures=0")\n    sys.exit(0)\n'
                 'print("claim C1 base_ok=2")\nprint("freeze-check claims=2 base_ok=2 exit=0")\n')


# ----------------------------------------------------------------------------------------
# tree helpers (hardlink clones; every write unlinks first so shared inodes are never touched)
# ----------------------------------------------------------------------------------------
def p(root, rel):
    return os.path.join(root, rel)


def rb(root, rel):
    with open(p(root, rel), "rb") as fh:
        return fh.read()


def rt(root, rel):
    return rb(root, rel).decode("utf-8")


def wb(root, rel, data, mode=None):
    path = p(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.lexists(path):
        os.unlink(path)
    with open(path, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))
    if mode:
        os.chmod(path, mode)


def wt(root, rel, text):
    wb(root, rel, text)


def sub(root, rel, old, new, count=1):
    t = rt(root, rel)
    assert t.count(old) >= 1, f"mutation anchor absent in {rel}: {old!r}"
    wt(root, rel, t.replace(old, new, count))


def clone(src, dst):
    r = subprocess.run(["cp", "-al", src, dst], capture_output=True, text=True)
    if r.returncode != 0:  # cross-device or permissions: fall back to a real copy
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst, symlinks=True)


# ----------------------------------------------------------------------------------------
# GOOD tree
# ----------------------------------------------------------------------------------------
def s072_row(sha: str, teaches: str | None = None) -> str:
    teaches = teaches or ("supersedes S070 — the S070 reject reason (a JavaScript shell) was read with the wrong capture method: "
                          "the same page is readable through the article API, whose body is 10029 readable characters; "
                          "the directory still supplies no program-specific rule beyond the linked policy text; "
                          "flip: the readable body exposes a located, program-specific rule absent from the linked policy text.")
    cells = ["S072", "Google Bug Hunters rules article API — https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section",
             "docs", "A", "Whether the rules directory, read through its article API, supplies operative scope rules beyond navigation",
             f"snapshot corpus/source-snapshots/round-45/S072.txt sha256 {sha}; quotes Q1 line 148, Q2 line 1 (manifest.json)",
             teaches, "rejected", "2026-10-28", "180d", "—"]
    assert all("|" not in c for c in cells)
    return "| " + " | ".join(cells) + " |"


LESSON_CORRECTION = ("Correction (round 45): the round-44 reject reason for S070 read a JavaScript shell; S072 captures the same "
                     "page through the article API (10029 readable characters) with located quotes, so the reject stays but "
                     "its reason is superseded by S072.")

QUALITY_APPEND = """
## Round-45 additions — do-nothing replay, presence-only predicates and capture-method parity (append-only)

| id | criterion | grounded in |
|---|---|---|
| R47 | A do-nothing control is replayed on the frozen counter string before data: the counter prints its expect_before line on the base before any seat is scored. enforced-by: `corpus/instruments/freeze-check.py` | grounded in `corpus/lessons/round-44.md` (the dead frozen regex that read 0 in both worlds) |
| R48 | A presence-only predicate (a marker, heading or token whose bytes are not bound to a located artifact) is never a verification limb. enforced-by: `corpus/instruments/r45-routed-defects.py` | grounded in `corpus/lessons/round-44.md` (marker-only receipts) |
| R49 | The capture method used to admit a source is also used to reject one: a reject reason read from a shell page is void. enforced-by: `corpus/instruments/source-recheck.py` | grounded in `corpus/lessons/round-44.md` (the S070 shell page) |
"""

REG_NAMES = ["r44-frontier-count.py", "r44-routed-defects.py", "wave-registry.py", "freeze-check.py", "r45-routed-defects.py", "r45-c2-gate.py"]
REG_HEAD = ("\n## Round-45 Gates & probes registry addition (appended 2026-10-28)\n\n"
            "| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n")


def reg_row(name: str) -> str:
    return (f"| {name} | gate | `python3 corpus/instruments/{name} ...` | 0 clean / 1 failed | "
            f"`python3 corpus/instruments/{name} --selftest` | base `dc5bb8c` | read-only | kasegi |\n")


def build_good(root: str, lane: str, base: str, tmp: str, counter_dir_src: str) -> None:
    # R1 ------------------------------------------------------------------------------
    for f in ("S071.txt", "S072.txt", "manifest.json"):
        wb(root, f"{SNAP}/{f}", open(p(lane, f"{SNAP}/{f}"), "rb").read())
    sha = hashlib.sha256(rb(root, f"{SNAP}/S072.txt")).hexdigest()
    sub(root, "corpus/SOURCES.md", "\n\n- Round 44 source/frontier addition:",
        "\n" + s072_row(sha) + "\n\n- Round 44 source/frontier addition:")
    lt = rt(root, "corpus/lessons/round-44.md")
    wt(root, "corpus/lessons/round-44.md", lt + "\n" + LESSON_CORRECTION + "\n")
    # R2 ------------------------------------------------------------------------------
    wt(root, "corpus/QUALITY.md", rt(root, "corpus/QUALITY.md") + QUALITY_APPEND)
    # R3 ------------------------------------------------------------------------------
    wt(root, "corpus/instruments/r44-frontier-count.py", frontier_src(rt(base, "corpus/instruments/r44-frontier-count.py")))
    os.chmod(p(root, "corpus/instruments/r44-frontier-count.py"), 0o755)
    wt(root, "SKILL.md", rt(root, "SKILL.md") + REG_HEAD + "".join(reg_row(n) for n in REG_NAMES))
    wt(root, "corpus/instruments/README.md", rt(root, "corpus/instruments/README.md") +
       "\n## Round-45 additions\n\n| script | what it measures | run |\n|---|---|---|\n"
       "| `r44-frontier-count.py` | frontier rows and admitted rows of corpus/README.md; `--selftest` grades eight fixture cases | "
       "`python3 corpus/instruments/r44-frontier-count.py --root TREE [--expect N]` |\n")
    # R4 ------------------------------------------------------------------------------
    wt(root, "corpus/instruments/freeze-check.py", freeze_src())
    os.chmod(p(root, "corpus/instruments/freeze-check.py"), 0o755)
    for f in ("r45-routed-defects.py", "r45-c2-gate.py"):
        wb(root, f"corpus/instruments/{f}", open(p(counter_dir_src, f), "rb").read(), 0o755)
    wb(root, ".ufo/waves/round-45/claims.json", open(p(lane, ".ufo/waves/round-45/claims.json"), "rb").read())
    # R5: the lane's own refiled receipt (a recorded real run at the round-44 tip export c950fa3).  A fresh run of
    # r44-routed-defects.py --selftest inside THIS base-derived tree prints failures=1 (R44-D4: the base LOG lacks the
    # planner=L1 mapping), so a re-run here cannot honestly mint the receipt; the recorded one is bound instead.
    wb(root, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt",
       open(p(lane, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"), "rb").read())


def run_counter(counter: str, root: str, baseline: str, tmp: str):
    env = dict(os.environ, TMPDIR=tmp, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, counter, "--root", root, "--baseline", baseline],
                       capture_output=True, text=True, env=env, timeout=900, cwd=tmp)
    out = r.stdout + r.stderr
    limbs = {m.group(1): (int(m.group(2)), m.group(3)) for m in LIMB_RX.finditer(out)}
    t = TOT_RX.search(out)
    return limbs, (int(t.group(2)) if t else -1), out


# ----------------------------------------------------------------------------------------
# mutants: (id, limb, expectation-note, fn(root, ctx))
# ----------------------------------------------------------------------------------------
WATCH = ["corpus/SOURCES.md", "corpus/QUALITY.md", "SKILL.md", "corpus/lessons/round-44.md", "corpus/instruments/README.md",
         "corpus/instruments/r44-frontier-count.py", "corpus/instruments/freeze-check.py", ".ufo/waves/round-45/claims.json",
         f"{SNAP}/S072.txt", f"{SNAP}/manifest.json", ".ufo/waves/round-44/controls/final-attempt3.txt",
         ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"]


def changed_files(a, b):
    def g(root, rel):
        try:
            return rb(root, rel)
        except OSError:
            return None
    return [rel for rel in WATCH if g(a, rel) != g(b, rel)]


def M(mid, limb, desc, fn, coupled=()):
    return {"id": mid, "limb": limb, "desc": desc, "fn": fn, "coupled": tuple(coupled)}


def _flip_byte(root, ctx):
    b = bytearray(rb(root, f"{SNAP}/S072.txt"))
    b[200] = b[200] ^ 0x01 if b[200] not in (0x0A,) else b[200]
    wb(root, f"{SNAP}/S072.txt", bytes(b))


def _drop_q2(root, ctx):
    m = json.loads(rt(root, f"{SNAP}/manifest.json"))
    for s in m["sources"]:
        if s["id"] == "S072":
            s["quotes"] = s["quotes"][:1]
    wt(root, f"{SNAP}/manifest.json", json.dumps(m, indent=2) + "\n")


def _forged_snapshot(root, ctx):
    forged = ("Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data\n"
              "an overview of the different vulnerability reward programs Google maintains\n")
    wt(root, f"{SNAP}/S072.txt", forged)
    sha = hashlib.sha256(forged.encode()).hexdigest()
    old = hashlib.sha256(rb(ctx["lane"], f"{SNAP}/S072.txt")).hexdigest()
    m = json.loads(rt(root, f"{SNAP}/manifest.json"))
    for s in m["sources"]:
        if s["id"] == "S072":
            s.update(sha256=sha, bytes=len(forged), snapshot_bytes=len(forged), lines=2)
            s["quotes"][0]["anchor"] = 1
            s["quotes"][1]["anchor"] = 2
    wt(root, f"{SNAP}/manifest.json", json.dumps(m, indent=2) + "\n")
    sub(root, "corpus/SOURCES.md", old, sha)


def _row_in_fence(root, ctx):
    t = rt(root, "corpus/SOURCES.md")
    line = [ln for ln in t.splitlines() if ln.startswith("| S072 |")][0]
    t = t.replace(line + "\n", "", 1)
    wt(root, "corpus/SOURCES.md", t + "\n```\n" + line + "\n```\n")


def _quality_edit_prefix(root, ctx):
    sub(root, "corpus/QUALITY.md", "# ", "## ", 1)


def _skill_edit_prefix(root, ctx):
    t = rt(root, "SKILL.md")
    wt(root, "SKILL.md", t.replace("\n", "\n ", 1))


def _reg_row_cells7(root, ctx):
    row = reg_row("wave-registry.py")
    sub(root, "SKILL.md", row, row.replace(" | kasegi |\n", " |\n"))


def _reg_row_dup(root, ctx):
    row = reg_row("r44-routed-defects.py")
    sub(root, "SKILL.md", row, row + row)


def _reg_row_gone(root, ctx):
    row = reg_row("wave-registry.py")
    sub(root, "SKILL.md", row, "wave-registry.py is registered in prose only (marker kept).\n")


def _readme_row_to_bullet(root, ctx):
    t = rt(root, "corpus/instruments/README.md")
    line = [ln for ln in t.splitlines() if ln.startswith("| `r44-frontier-count.py` |")][0]
    wt(root, "corpus/instruments/README.md", t.replace(line, "- r44-frontier-count.py counts frontier rows (prose, no table row)"))


def _claims_expect(root, ctx):
    sub(root, ".ufo/waves/round-45/claims.json", "c2-gate fixed=1/7 exit=1", "c2-gate fixed=2/7 exit=1")


def _claims_weakened(root, ctx):
    c = json.loads(rt(root, ".ufo/waves/round-45/claims.json"))
    for cl in c["claims"]:
        cl["counter_cmd"] = "echo '%s'" % cl["expect_before"]
    wt(root, ".ufo/waves/round-45/claims.json", json.dumps(c, indent=2) + "\n")


def _r4_claims_sub(root, ctx):
    pass


MUTANTS = [
    # ---- R1 -------------------------------------------------------------------------------
    M("r1-snapshot-byte-flipped", "R1", "S072.txt one byte flipped; manifest sha + anchor sha untouched", _flip_byte),
    M("r1-manifest-quote-dropped", "R1", "manifest keeps only S072:Q1 (valid JSON); snapshot and row untouched", _drop_q2),
    M("r1-s070-row-edited", "R1", "S070 row 'REJECTED:' -> 'Rejected:'",
      lambda r, c: sub(r, "corpus/SOURCES.md", "| REJECTED: the page's accessible body", "| Rejected: the page's accessible body")),
    M("r1-flip-clause-removed", "R1", "S072 teaches loses the 'flip:' clause; `supersedes S070 —`, readable, 10029 stay",
      lambda r, c: sub(r, "corpus/SOURCES.md", "flip: the readable body exposes", "if the readable body exposes")),
    M("r1-correction-wrong-size", "R1", "lesson Correction line cites S072 but size 10032 instead of 10029",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", "(10029 readable characters)", "(10032 readable characters)")),
    M("r1-anchor-sha-wrong", "R1", "S072 row anchor carries the S071.txt sha instead of S072.txt's",
      lambda r, c: sub(r, "corpus/SOURCES.md", hashlib.sha256(rb(c["lane"], f"{SNAP}/S072.txt")).hexdigest(),
                       hashlib.sha256(rb(c["lane"], f"{SNAP}/S071.txt")).hexdigest())),
    M("r1-row-outside-table", "R1", "PROBE: the S072 row is moved into a ``` fence at the end of SOURCES.md (not in the registry table)", _row_in_fence),
    M("r1-forged-snapshot-self-consistent", "R1",
      "PROBE: S072.txt replaced by a 2-line forgery holding only the two quotes; manifest sha/bytes/lines/anchors and the row anchor sha re-pinned to it", _forged_snapshot),
    M("r1-correction-content-free", "R1", "PROBE: lesson correction reduced to 'Correction (round 45): S072 10029' (cites tokens, corrects nothing)",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", LESSON_CORRECTION, "Correction (round 45): S072 10029")),
    # ---- R2 -------------------------------------------------------------------------------
    M("r2-enforced-by-missing", "R2", "R48 enforced-by path points at a file that does not exist",
      lambda r, c: sub(r, "corpus/QUALITY.md", "enforced-by: `corpus/instruments/r45-routed-defects.py`", "enforced-by: `corpus/instruments/does-not-exist.py`")),
    M("r2-quality-prefix-edited", "R2", "first byte-line of the baseline QUALITY.md changed (not append-only)", _quality_edit_prefix),
    M("r2-r49-ungrounded", "R2", "R49 grounded-in cell no longer names corpus/lessons/round-44.md",
      lambda r, c: sub(r, "corpus/QUALITY.md", "grounded in `corpus/lessons/round-44.md` (the S070 shell page)", "grounded in the S070 shell page")),
    M("r2-duplicate-heading", "R2", "the `## Round-45 additions` heading appears twice",
      lambda r, c: wt(r, "corpus/QUALITY.md", rt(r, "corpus/QUALITY.md") + "\n## Round-45 additions — stray second block\n")),
    M("r2-r47-lacks-before-data", "R2", "R47 criterion keeps `do-nothing` but loses `before data`",
      lambda r, c: sub(r, "corpus/QUALITY.md", "before data: the counter", "later: the counter")),
    M("r2-enforced-by-directory", "R2", "PROBE: R47 `enforced-by: `corpus`` (a directory; only os.path.exists is tested)",
      lambda r, c: sub(r, "corpus/QUALITY.md", "enforced-by: `corpus/instruments/freeze-check.py`", "enforced-by: `corpus`")),
    M("r2-vacuous-criterion", "R2", "PROBE: R48 criterion reduced to 'presence-only enforced-by: `LOG.md`' (keywords + any existing file)",
      lambda r, c: sub(r, "corpus/QUALITY.md",
                       "A presence-only predicate (a marker, heading or token whose bytes are not bound to a located artifact) is never a verification limb. enforced-by: `corpus/instruments/r45-routed-defects.py`",
                       "presence-only enforced-by: `LOG.md`")),
    # ---- R3 -------------------------------------------------------------------------------
    M("r3-selftest-7-cases", "R3", "r44-frontier-count.py really grades 7 cases (case 8 removed)",
      lambda r, c: wt(r, "corpus/instruments/r44-frontier-count.py", frontier_src(rt(c["base"], "corpus/instruments/r44-frontier-count.py"), limit=7))),
    M("r3-selftest-failure", "R3", "r44-frontier-count.py selftest case 1 expects admitted=99 -> failures=1",
      lambda r, c: wt(r, "corpus/instruments/r44-frontier-count.py", frontier_src(rt(c["base"], "corpus/instruments/r44-frontier-count.py"), exp_admit=99))),
    M("r3-stub-selftest", "R3", "PROBE: r44-frontier-count.py replaced by a 5-line stub that prints `selftest cases=8 failures=0`",
      lambda r, c: wt(r, "corpus/instruments/r44-frontier-count.py", STUB_SELFTEST)),
    M("r3-registry-row-7-cells", "R3", "wave-registry.py registry row has 7 cells", _reg_row_cells7),
    M("r3-registry-row-duplicated", "R3", "r44-routed-defects.py registry row appears twice", _reg_row_dup),
    M("r3-registry-row-prose-only", "R3", "wave-registry.py registry row replaced by a prose sentence (name marker kept)", _reg_row_gone),
    M("r3-readme-row-bullet", "R3", "instruments README table row for r44-frontier-count.py turned into a bullet (name kept)", _readme_row_to_bullet),
    M("r3-skill-not-append-only", "R3", "SKILL.md baseline portion edited (leading space on line 1)", _skill_edit_prefix),
    # ---- R4 -------------------------------------------------------------------------------
    M("r4-freeze-selftest-5-cases", "R4", "freeze-check.py really grades 5 cases",
      lambda r, c: wt(r, "corpus/instruments/freeze-check.py", freeze_src(limit=5))),
    M("r4-freeze-selftest-failure", "R4", "freeze-check.py selftest case 1 expects the wrong finding -> failures=1",
      lambda r, c: wt(r, "corpus/instruments/freeze-check.py", freeze_src(exp1="base-mismatch"))),
    M("r4-freeze-absent", "R4", "freeze-check.py deleted",
      lambda r, c: os.unlink(p(r, "corpus/instruments/freeze-check.py")), coupled=("R2",)),
    M("r4-claims-replay-short", "R4", "tree claims.json: C2 expect_before changed so the replay reads base_ok=1", _claims_expect),
    M("r4-stub-freeze-check", "R4", "PROBE: freeze-check.py replaced by a 5-line stub printing both tokens",
      lambda r, c: wt(r, "corpus/instruments/freeze-check.py", STUB_SELFTEST)),
    M("r4-claims-weakened", "R4", "PROBE: tree claims.json counter_cmd of both claims replaced by `echo '<expect_before>'`", _claims_weakened),
    # ---- R5 -------------------------------------------------------------------------------
    M("r5-usage-line", "R5", "refiled receipt carries a `usage:` line",
      lambda r, c: wt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt", "usage: r44-routed-defects.py [-h]\n" + rt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"))),
    M("r5-error-line-only", "R5", "refiled receipt carries only the argparse `error: the following arguments are required: --root` line (no `usage:`)",
      lambda r, c: wt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt", rt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt") + "r44-routed-defects.py: error: the following arguments are required: --root\n")),
    M("r5-original-changed", "R5", "original final-attempt3.txt gains one byte",
      lambda r, c: wt(r, ".ufo/waves/round-44/controls/final-attempt3.txt", rt(r, ".ufo/waves/round-44/controls/final-attempt3.txt") + " ")),
    M("r5-invocation-absent", "R5", "refiled receipt loses the `--root X --selftest --work Y` invocation (token lines stay)",
      lambda r, c: wt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt",
                      re.sub(r"--root \S+ --selftest --work \S+", "<invocation elided>", rt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt")))),
    M("r5-cases-19", "R5", "refiled receipt reads `selftest cases=19 failures=0`",
      lambda r, c: sub(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt", "selftest cases=20 failures=0", "selftest cases=19 failures=0")),
    M("r5-fabricated-receipt", "R5", "PROBE: refiled receipt is a 3-line hand-written text (comment carrying the invocation, the token, exit=0); nothing was run",
      lambda r, c: wt(r, ".ufo/waves/round-44/controls/final-attempt3-refiled.txt",
                      "# --root X --selftest --work Y\nselftest cases=20 failures=0\nexit=0\n")),
]


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--counter", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    counter = os.path.abspath(a.counter or p(a.lane, "corpus/instruments/r45-routed-defects.py"))
    scratch_root = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
    scratch = os.path.join(scratch_root, "kasegi-r45", "R45ExecSelftestC1")
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="run-", dir=scratch)
    tmp = os.path.join(work, "tmp")
    os.makedirs(tmp)
    cases = failures = 0
    false_green: list[str] = []
    try:
        good = os.path.join(work, "good")
        clone(a.base, good)
        build_good(good, a.lane, a.base, tmp, os.path.dirname(counter))
        ctx = {"lane": a.lane, "base": a.base}

        def grade(name, limbs, total, ok, note):
            nonlocal cases, failures
            cases += 1
            if not ok:
                failures += 1
            print(f"case {name} total_fixed={total} verdict={'ok' if ok else 'FAIL'} {note}")

        g_limbs, g_total, g_out = run_counter(counter, good, a.base, tmp)
        print("GOOD counter output:\n" + "".join("  " + ln + "\n" for ln in g_out.splitlines()))
        grade("control-good-tree", g_limbs, g_total, g_total == 5 and all(v[0] == 1 for v in g_limbs.values()),
              "expect fixed=5 " + " ".join(f"{k}={v[0]}" for k, v in sorted(g_limbs.items())))

        b_limbs, b_total, _ = run_counter(counter, a.base, a.base, tmp)
        grade("control-do-nothing-base", b_limbs, b_total, b_total == 0, "expect fixed=0")

        nul = os.path.join(work, "null")
        clone(good, nul)
        n_limbs, n_total, _ = run_counter(counter, nul, a.base, tmp)
        grade("control-null-mutant", n_limbs, n_total, n_total == 5, "unchanged clone must stay fixed=5 (harness does not flag everything)")

        mk = os.path.join(work, "marker")
        clone(a.base, mk)
        sub(mk, "corpus/lessons/round-44.md", "\n", "\n", 1)
        wt(mk, "corpus/lessons/round-44.md", rt(mk, "corpus/lessons/round-44.md") + "\n" + LESSON_CORRECTION + "\n")
        wt(mk, "corpus/QUALITY.md", rt(mk, "corpus/QUALITY.md") + "\n## Round-45 additions\nR47 do-nothing before data; R48 presence-only; R49 capture method reject\n")
        wt(mk, "SKILL.md", rt(mk, "SKILL.md") + "\n## Round-45 Gates & probes registry addition (appended 2026-10-28)\nr44-frontier-count.py r44-routed-defects.py wave-registry.py\n")
        m_limbs, m_total, _ = run_counter(counter, mk, a.base, tmp)
        grade("control-marker-only", m_limbs, m_total, m_total == 0, "prose markers only, no artifacts: expect fixed=0")

        only = set(a.only.split(",")) if a.only else None
        for mu in MUTANTS:
            if only and mu["id"] not in only:
                continue
            d = os.path.join(work, "m-" + mu["id"])
            clone(good, d)
            mu["fn"](d, ctx)
            ch = changed_files(good, d)
            limbs, total, out = run_counter(counter, d, a.base, tmp)
            tgt = limbs.get(mu["limb"], (None, "no-limb-line"))
            collateral = sorted(k for k, v in limbs.items() if k != mu["limb"] and k not in mu["coupled"] and v[0] != g_limbs[k][0])
            rejected = tgt[0] == 0 and total == g_total - 1 - len(mu["coupled"]) and not collateral and len(ch) == 1
            if rejected:
                verdict = "rejected"
            elif tgt[0] == 1:
                verdict = "FALSE-GREEN"
                false_green.append(f"FALSE-GREEN mutant={mu['id']} limb={mu['limb']} recipe: {mu['desc']} | counter read: limb {mu['limb']} fixed=1 read={tgt[1]} total={total}")
            else:
                verdict = "COLLATERAL-OR-HARNESS" + ("" if len(ch) == 1 else f"(changed={len(ch)})")
            cases += 1
            if not rejected:
                failures += 1
            print(f"case {mu['id']} limb={mu['limb']} target_fixed={tgt[0]} total_fixed={total} verdict={verdict} changed={','.join(ch)} read={tgt[1]}")
            shutil.rmtree(d, ignore_errors=True)
        for fg in false_green:
            print(fg)
        print(f"selftest cases={cases} failures={failures}")
        return 1 if failures else 0
    finally:
        if a.keep:
            print("kept scratch " + work, file=sys.stderr)
        else:
            shutil.rmtree(work, ignore_errors=True)
            try:
                os.rmdir(scratch)
            except OSError:
                pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
