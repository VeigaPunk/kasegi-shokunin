#!/usr/bin/env python3
"""r45-counters-selftest-c1.py — mutation selftest for the round-45 C1 counter v1.1
(corpus/instruments/r45-routed-defects.py).  DRAFT; the L1 integrates.  stdlib only.

WHAT IT DOES
  1. Builds in scratch a COMPLETE synthetic tree (GOOD) on top of an export of the frozen
     base: every artifact a limb R1..R5 binds is genuinely written
       R1  S072 row inside the `## Registry` table of corpus/SOURCES.md, corpus/source-snapshots/
           round-45/{S071.txt,S072.txt,manifest.json} copied byte-for-byte from --lane, an
           appended `Correction (round 45` line in corpus/lessons/round-44.md that quotes a
           located S072 span
       R2  an append-only `## Round-45 additions` block in corpus/QUALITY.md (R47/R48/R49,
           >=300-char criteria, in-range corpus/lessons/round-44.md:<line> refs, enforced-by files)
       R3  a working r44-frontier-count.py WITH --selftest (8 real cases), the SKILL.md
           `## Round-45 Gates & probes registry addition` table, an instruments README row
       R4  a working freeze-check.py (own minimal implementation, 8 real cases, replays the
           claims file at the base) + the real claims.json + the r45 counters
       R5  .ufo/waves/round-44/controls/final-attempt3-refiled.txt (the lane's recorded run)
  2. v1.1 pins artifacts by sha256 (PINS dict of the counter).  The grader-side env var
     R45_PINS_OVERRIDE=<json file> carries pins COMPUTED FROM THE SYNTHETIC ARTIFACTS (keys
     S072.txt, freeze-check.py, r44-frontier-count.py, r44-routed-defects.py, claims.json,
     refiled-body); the real pins in the counter are never edited.  Mutants of the pinned
     artifacts keep the GOOD pins (the pin limb must reject them); mutants of BEHAVIOUR
     (selftest case count / failure) re-pin the mutated bytes so the selftest-token limb is
     tested in isolation.
  3. Controls: do-nothing base (fixed=0), marker-only tree (fixed=0), a null mutant
     (unchanged clone; must stay fixed=5 so the harness cannot pass by flagging everything),
     and the GOOD tree under the REAL pins (no override: pinned code limbs R3/R4 must reject).
  4. MUTANTS: each is a hardlink clone of GOOD with ONE limb's bound artifact broken while
     the prose marker stays.  A mutant is REJECTED when the targeted limb reads fixed=0 for
     the intended reason (`why` regex on the printed read= token), the total drops by exactly
     one (plus declared coupled limbs), no other limb changes, the counter exits 1 and the
     mutant really differs from GOOD.  Otherwise: FALSE-GREEN (target limb still fixed=1),
     WRONG-REASON, COLLATERAL or HARNESS-ERROR; each is a failure.  `info` mutants (beyond the
     literal predicate) print `info-accepted|info-rejected` and never count as failures.
  Output: one `case ...` line per case, `FALSE-GREEN ...` recipes, then
          `selftest cases=<N> failures=<F>` (exit 0 only when F=0).

USAGE
  python3 r45-counters-selftest-c1.py [--lane DIR] [--base DIR] [--counter PATH] [--only ID,ID] [--jobs N] [--keep]
  Scratch: $HYAKU_SCRATCH/kasegi-r45/selftest-c1 (HYAKU_SCRATCH defaults to /fast/scratch/hyaku);
  child processes get TMPDIR = the caller's TMPDIR if set, else a directory inside the scratch.
  --lane may be an export of the integration commit; the counter, snapshots, claims.json and the
  refiled receipt are read from it (default: the lane working tree).
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
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
BASE = "/fast/scratch/hyaku/kasegi-r45/L1/pure"
BASE_COMMIT = "dc5bb8c6e31efc4a6650819df85e79b72fd64bcd"
SNAP = "corpus/source-snapshots/round-45"
S72 = ".ufo/waves/round-45/source-recon"
REFILED = ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"
ORIGINAL = ".ufo/waves/round-44/controls/final-attempt3.txt"
CLAIMS = ".ufo/waves/round-45/claims.json"
FC = "corpus/instruments/freeze-check.py"
FR = "corpus/instruments/r44-frontier-count.py"
R44 = "corpus/instruments/r44-routed-defects.py"
INVOCATION = "$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>"
LINE_PINS = ("R1-row", "R1-corr", "R2-R47", "R2-R48", "R2-R49", "R3-skill-r44-frontier-count.py", "R3-skill-r44-routed-defects.py",
             "R3-skill-wave-registry.py", "R3-readme-r44-frontier-count.py")
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


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(s: str) -> str:
    """Mirror of the counter's norm() — used only to assert the GOOD quote is really located."""
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def receipt_body(text: str) -> bytes | None:
    """Pin of the receipt body, computed exactly as the counter does (lines between the invocation and `exit=0`)."""
    lines = text.splitlines()
    inv = [i for i, ln in enumerate(lines) if ln == INVOCATION]
    end = [i for i, ln in enumerate(lines) if ln == "exit=0"]
    if len(inv) != 1 or len(end) != 1 or end[0] <= inv[0]:
        return None
    return "\n".join(lines[inv[0] + 1:end[0]]).encode()


def compute_pins(tree: str, keys=None) -> dict:
    """Pins computed from the artifacts of TREE (missing artifact -> key omitted, so the real pin stays and rejects)."""
    spec = {"S072.txt": f"{S72}/S072.txt", "freeze-check.py": FC, "r44-frontier-count.py": FR,
            "r44-routed-defects.py": R44, "claims.json": CLAIMS}
    out = {}
    for k, rel in spec.items():
        if keys is not None and k not in keys:
            continue
        try:
            out[k] = sha(rb(tree, rel))
        except OSError:
            pass
    if keys is None or "refiled-body" in keys:
        try:
            body = receipt_body(rt(tree, REFILED))
        except OSError:
            body = None
        if body is not None:
            out["refiled-body"] = sha(body)
    return out


# ----------------------------------------------------------------------------------------
# GOOD tree
# ----------------------------------------------------------------------------------------
QUOTE = "Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data"
FLIP = ("flip: a fresh article-API capture states a program-specific scope or boundary rule that the program's linked rules "
        "page does not state")


def s072_row(sha256: str) -> str:
    teaches = ("supersedes S070 — REJECTED: the body is readable through the article API (10029 characters), so S070's no-body "
               "reason is corrected; it is a program, scope and where-to-report overview table that adds no operative rule; " + FLIP)
    cells = ["S072", "Google Bug Hunters Rules directory, readable article-API capture — https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section",
             "docs", "B", "Google's overview of which VRP program covers which product family; a secondary routing summary",
             f"capture .ufo/waves/round-45/source-recon/S072.txt (sha256 {sha256}, 10032 bytes, 312 lines); Cloud VRP scope line L148-L149",
             teaches, "rejected", "2026-10-28", "180d", "—"]
    assert all("|" not in c for c in cells)
    return "| " + " | ".join(cells) + " |"


LESSON_CORRECTION = ("Correction (round 45, appended 2026-10-28): the S070 reject reason was read from a JavaScript shell; S072 reads the "
                     "same page through the article API (10029 readable characters) and the directory's Cloud VRP row says "
                     f'\u201c{QUOTE}\u201d (located across a line break in .ufo/waves/round-45/source-recon/S072.txt), so the shell reason is '
                     "superseded by S072 and the reject stands on the corrected reason.")

R47_CRIT = ("A frozen counter is replayed on the cheapest do-nothing control (the unmodified base tree) and must print its declared "
            "before-value, never 0 for a nonzero before, before data is read and before any seat scores; a counter that prints 0 "
            "where the declared before is nonzero is unmeasurable, so the claim it grades stays unfrozen (the r44 mine: the frozen "
            "C2 grep printed 0 at base, `corpus/lessons/round-44.md:126`). enforced-by: `corpus/instruments/freeze-check.py`")
R47_GRD = "grounded in `corpus/lessons/round-44.md` (the dead frozen regex that read 0 in both worlds)"
R48_CRIT = ("A limb that grades a committed artifact is presence-only when it only checks that a file, heading, row or word exists, "
            "and a presence-only predicate accepts denials, stubs and fabricated trees, so every limb must bind content: pinned "
            "bytes by sha256, located quotes by exact anchor, whole-token values (the r44 mine: the v1 counter printed fixed=8 on a "
            "fully fabricated evidence tree, `corpus/lessons/round-44.md:189`). enforced-by: `corpus/instruments/r45-routed-defects.py`")
R48_GRD = "grounded in `corpus/lessons/round-44.md` (marker-only receipts)"
R49_CRIT = ("The capture method used to ADMIT a source is also the capture method used to REJECT one: a reject reason is graded only "
            "on text read through that same method, so a reject reason read from a shell page is void until the source is re-read "
            "through the admitting capture method (the r44 S070 mine: the plain page was read as a JavaScript shell, "
            "`corpus/lessons/round-44.md:131`). enforced-by: `corpus/instruments/source-recheck.py`")
R49_GRD = "grounded in `corpus/lessons/round-44.md` (the S070 shell page)"
for _c in (R47_CRIT, R48_CRIT, R49_CRIT):
    assert len(_c) >= 300 and "|" not in _c, len(_c)


def r_row(rid, crit, grd):
    return f"| {rid} | {crit} | {grd} |"


QUALITY_APPEND = ("\n## Round-45 additions — do-nothing replay, presence-only predicates and capture-method parity (append-only)\n\n"
                  "| id | criterion | grounded in |\n|---|---|---|\n"
                  + r_row("R47", R47_CRIT, R47_GRD) + "\n" + r_row("R48", R48_CRIT, R48_GRD) + "\n" + r_row("R49", R49_CRIT, R49_GRD) + "\n")

REG_NAMES = ["r44-frontier-count.py", "r44-routed-defects.py", "wave-registry.py", "freeze-check.py", "r45-routed-defects.py", "r45-c2-gate.py"]
REG_HEAD = ("\n## Round-45 Gates & probes registry addition (appended 2026-10-28)\n\n"
            "| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|---|\n")


def reg_row(name: str) -> str:
    return (f"| {name} | gate | `python3 corpus/instruments/{name} ...` | 0 clean / 1 failed | "
            f"`python3 corpus/instruments/{name} --selftest` | base `dc5bb8c` | read-only | kasegi |\n")


README_ROW = ("| `r44-frontier-count.py` | frontier rows and admitted rows of corpus/README.md; `--selftest` grades eight fixture cases | "
              "`python3 corpus/instruments/r44-frontier-count.py --root TREE [--expect N]` |")


def build_good(root: str, lane: str, base: str, counter_dir_src: str) -> None:
    # R1 ------------------------------------------------------------------------------
    for f in ("S071.txt", "manifest.json"):
        wb(root, f"{SNAP}/{f}", open(p(lane, f"{SNAP}/{f}"), "rb").read())
    for f in ("S072.txt", "S072.manifest.json"):
        wb(root, f"{S72}/{f}", open(p(lane, f"{S72}/{f}"), "rb").read())
    assert norm(QUOTE) in norm(rt(root, f"{S72}/S072.txt")), "GOOD quote is not located in the S072 snapshot"
    s_sha = sha(rb(root, f"{S72}/S072.txt"))
    t = rt(root, "corpus/SOURCES.md")
    s070 = [ln for ln in t.splitlines() if ln.startswith("| S070 |")]
    assert len(s070) == 1
    wt(root, "corpus/SOURCES.md", t.replace(s070[0] + "\n", s070[0] + "\n" + s072_row(s_sha) + "\n", 1))
    wt(root, "corpus/lessons/round-44.md", rt(root, "corpus/lessons/round-44.md") + "\n" + LESSON_CORRECTION + "\n")
    # R2 ------------------------------------------------------------------------------
    wt(root, "corpus/QUALITY.md", rt(root, "corpus/QUALITY.md") + QUALITY_APPEND)
    # R3 ------------------------------------------------------------------------------
    wt(root, FR, frontier_src(rt(base, FR)))
    os.chmod(p(root, FR), 0o755)
    wt(root, "SKILL.md", rt(root, "SKILL.md") + REG_HEAD + "".join(reg_row(n) for n in REG_NAMES))
    wt(root, "corpus/instruments/README.md", rt(root, "corpus/instruments/README.md") +
       "\n## Round-45 additions\n\n| script | what it measures | run |\n|---|---|---|\n" + README_ROW + "\n")
    # R4 ------------------------------------------------------------------------------
    wt(root, FC, freeze_src())
    os.chmod(p(root, FC), 0o755)
    for f in ("r45-routed-defects.py", "r45-c2-gate.py"):
        wb(root, f"corpus/instruments/{f}", open(p(counter_dir_src, f), "rb").read(), 0o755)
    wb(root, CLAIMS, open(p(lane, CLAIMS), "rb").read())
    # R5: the lane's own refiled receipt (a recorded real run at the round-44 tip export c950fa3).  A fresh run of
    # r44-routed-defects.py --selftest inside a base-derived tree prints failures=1 (R44-D4), so the recorded run is bound.
    wb(root, REFILED, open(p(lane, REFILED), "rb").read())


def run_counter(counter: str, root: str, baseline: str, tmpdir: str, pins_json: str | None):
    env = dict(os.environ, TMPDIR=tmpdir, PYTHONDONTWRITEBYTECODE="1")
    env.pop("R45_PINS_OVERRIDE", None)
    if pins_json:
        env["R45_PINS_OVERRIDE"] = pins_json
    r = subprocess.run([sys.executable, counter, "--root", root, "--baseline", baseline],
                       capture_output=True, text=True, env=env, timeout=900, cwd=tmpdir)
    out = r.stdout + r.stderr
    limbs = {m.group(1): (int(m.group(2)), m.group(3)) for m in LIMB_RX.finditer(out)}
    t = TOT_RX.search(out)
    return {"limbs": limbs, "total": int(t.group(2)) if t else -1, "rc": r.returncode, "out": out}


def changed_files(good: str, mut: str) -> list[str]:
    """Files that differ between GOOD and a hardlink clone: new inode AND different bytes (or created/deleted)."""
    out = []
    seen = set()
    for dp, _dn, fn in os.walk(mut):
        for f in fn:
            a = os.path.join(dp, f)
            rel = os.path.relpath(a, mut)
            seen.add(rel)
            b = os.path.join(good, rel)
            try:
                if os.path.samestat(os.lstat(a), os.lstat(b)):
                    continue
                if open(a, "rb").read() != open(b, "rb").read():
                    out.append(rel)
            except OSError:
                out.append(rel)
    for dp, _dn, fn in os.walk(good):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), good)
            if rel not in seen:
                out.append(rel)
    return sorted(out)


# ----------------------------------------------------------------------------------------
# mutants
# ----------------------------------------------------------------------------------------
def M(mid, limb, desc, fn, why, repin=(), coupled=(), info=False):
    return {"id": mid, "limb": limb, "desc": desc, "fn": fn, "why": why, "repin": tuple(repin), "coupled": tuple(coupled), "info": info}


def _s072_line(t):
    return [ln for ln in t.splitlines() if ln.startswith("| S072 |")][0]


def row_edit(fn):
    def f(r, c):
        t = rt(r, "corpus/SOURCES.md")
        line = _s072_line(t)
        wt(r, "corpus/SOURCES.md", t.replace(line, fn(line), 1))
    return f


def _row_to_paths(r, c):
    t = rt(r, "corpus/SOURCES.md")
    line = _s072_line(t)
    t = t.replace(line + "\n", "", 1)
    assert "## Paths\n" in t
    wt(r, "corpus/SOURCES.md", t.replace("## Paths\n", "## Paths\n" + line + "\n", 1))


def _flip_byte(r, c):
    b = bytearray(rb(r, f"{S72}/S072.txt"))
    assert b[200] != 0x0A
    b[200] ^= 0x01
    wb(r, f"{S72}/S072.txt", bytes(b))


def _drop_q2(r, c):
    m = json.loads(rt(r, f"{S72}/S072.manifest.json"))
    for s in m["sources"]:
        if s["id"] == "S072":
            s["quotes"] = s["quotes"][:1]
    wt(r, f"{S72}/S072.manifest.json", json.dumps(m, indent=2) + "\n")


def _forged_snapshot(r, c):
    forged = QUOTE + "\nan overview of the different vulnerability reward programs Google maintains\n"
    wt(r, f"{S72}/S072.txt", forged)
    new = sha(forged.encode())
    m = json.loads(rt(r, f"{S72}/S072.manifest.json"))
    for s in m["sources"]:
        if s["id"] == "S072":
            s.update(sha256=new, bytes=len(forged), snapshot_bytes=len(forged), lines=2)
            s["quotes"][0]["anchor"] = 1
            s["quotes"][1]["anchor"] = 2
    wt(r, f"{S72}/S072.manifest.json", json.dumps(m, indent=2) + "\n")
    sub(r, "corpus/SOURCES.md", c["gp"]["S072.txt"], new)


def _quality_row_sub(rid, fn):
    def f(r, c):
        t = rt(r, "corpus/QUALITY.md")
        line = [ln for ln in t.splitlines() if ln.startswith(f"| {rid} |")][0]
        wt(r, "corpus/QUALITY.md", t.replace(line, fn(line), 1))
    return f


def _quality_prefix(r, c):
    sub(r, "corpus/QUALITY.md", "# ", "## ", 1)


def _skill_prefix(r, c):
    wt(r, "SKILL.md", rt(r, "SKILL.md").replace("\n", "\n ", 1))


def _reg_sub(name, fn):
    def f(r, c):
        row = reg_row(name)
        sub(r, "SKILL.md", row, fn(row))
    return f


def _readme_row(fn):
    def f(r, c):
        sub(r, "corpus/instruments/README.md", README_ROW, fn(README_ROW))
    return f


def _claims_json(fn):
    def f(r, c):
        d = json.loads(rt(r, CLAIMS))
        fn(d)
        wt(r, CLAIMS, json.dumps(d, indent=2) + "\n")
    return f


def _claims_weaken(d):
    for cl in d["claims"]:
        cl["counter_cmd"] = "echo '%s'" % cl["expect_before"]


def _claims_expect(d):
    for cl in d["claims"]:
        if cl["id"] == "C2":
            cl["expect_before"] = "c2-gate fixed=2/7 exit=1"


def _refiled(fn):
    def f(r, c):
        wt(r, REFILED, fn(rt(r, REFILED)))
    return f


MUTANTS = [
    # ---- R1 -------------------------------------------------------------------------------
    M("r1-snapshot-byte-flipped", "R1", "S072.txt one byte flipped; manifest sha + row anchor untouched", _flip_byte, r"recheck-rc=[1-9]"),
    M("r1-manifest-quote-dropped", "R1", "manifest keeps only S072:Q1 (valid JSON); snapshot and row untouched", _drop_q2, r"quotes=1"),
    M("r1-forged-snapshot-self-consistent", "R1",
      "S072.txt replaced by a 2-line forgery holding only the quote; manifest sha/bytes/lines/anchors and the row anchor sha re-pinned to it (source-recheck passes; only the grader pin can catch it)",
      _forged_snapshot, r"snapshot-not-the-pinned-capture"),
    M("r1-anchor-sha-wrong", "R1", "S072 row anchor carries the S071.txt sha instead of S072.txt's",
      lambda r, c: sub(r, "corpus/SOURCES.md", c["gp"]["S072.txt"], sha(rb(r, f"{SNAP}/S071.txt"))), r"snapshot-not-the-pinned-capture-or-not-in-anchor"),
    M("r1-s070-row-edited", "R1", "S070 row 'REJECTED:' -> 'Rejected:'",
      lambda r, c: sub(r, "corpus/SOURCES.md", "| REJECTED: the page's accessible body", "| Rejected: the page's accessible body"), r"S070-row-changed"),
    M("r1-s070-row-duplicated", "R1", "S070 row appears twice in the registry",
      lambda r, c: sub(r, "corpus/SOURCES.md", [ln for ln in rt(r, "corpus/SOURCES.md").splitlines() if ln.startswith("| S070 |")][0] + "\n",
                       [ln for ln in rt(r, "corpus/SOURCES.md").splitlines() if ln.startswith("| S070 |")][0] + "\n"
                       + [ln for ln in rt(r, "corpus/SOURCES.md").splitlines() if ln.startswith("| S070 |")][0] + "\n"), r"S070-row-changed"),
    M("r1-teaches-not-supersedes", "R1", "S072 teaches opens `relates to S070 —`", row_edit(lambda ln: ln.replace("supersedes S070 —", "relates to S070 —", 1)), r"teaches-not-supersedes"),
    M("r1-status-admitted", "R1", "S072 status cell `admitted` instead of `rejected`", row_edit(lambda ln: ln.replace(" | rejected | ", " | admitted | ", 1)), r"status=admitted"),
    M("r1-flip-clause-removed", "R1", "S072 teaches loses the `flip:` clause (`supersedes S070 —`, readable, 10029 stay)",
      row_edit(lambda ln: ln.replace(FLIP, "if a fresh capture says more, revisit", 1)), r"flip-absent"),
    M("r1-flip-vacuous-tbd", "R1", "S072 flip clause reduced to the vacuous `flip: tbd` (wave-1 probe; predicate: a checkable flip clause)",
      row_edit(lambda ln: ln.replace(FLIP, "flip: tbd", 1)), r"flip-absent"),
    M("r1-flip-vacuous-colon-dot", "R1", "S072 flip clause reduced to `flip: .`", row_edit(lambda ln: ln.replace(FLIP, "flip: .", 1)), r"flip-absent"),
    M("r1-size-token-absent", "R1", "S072 teaches loses 10029", row_edit(lambda ln: ln.replace("(10029 characters)", "(some characters)", 1)), r"size-token-absent"),
    M("r1-row-in-code-fence", "R1", "S072 row wrapped in ``` fences in place (inside the registry)", row_edit(lambda ln: "```\n" + ln + "\n```"), r"row-S072=absent"),
    M("r1-row-in-html-comment", "R1", "S072 row wrapped in an HTML comment in place", row_edit(lambda ln: "<!--\n" + ln + "\n-->"), r"row-S072=absent"),
    M("r1-row-after-registry", "R1", "S072 row moved under `## Paths` (outside the registry table)", _row_to_paths, r"row-S072=absent"),
    M("r1-row-indented-code-block", "R1", "S072 row indented 4 spaces (markdown code block)", row_edit(lambda ln: "    " + ln), r"row-S072=absent"),
    M("r1-row-10-cells", "R1", "S072 row loses its last cell", row_edit(lambda ln: ln[:-len(" | — |")] + " |"), r"row-S072=absent"),
    M("r1-correction-wrong-size", "R1", "lesson Correction line cites S072 but size 10032 instead of 10029",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", "(10029 readable characters)", "(10032 readable characters)"), r"lesson-correction"),
    M("r1-correction-content-free", "R1", "lesson correction reduced to `Correction (round 45): S072 10029` (cites tokens, quotes nothing)",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", LESSON_CORRECTION, "Correction (round 45): S072 10029"), r"lesson-correction"),
    M("r1-correction-quote-unlocated", "R1", "lesson correction quotes a fabricated 14-word span that S072.txt does not contain",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", QUOTE, "Every Google program must publish a binding bounty schedule for each product family it names"), r"lesson-correction"),
    M("r1-correction-quote-absent", "R1", "lesson correction keeps S072 and 10029 but carries no quoted span",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", f'\u201c{QUOTE}\u201d', "the Cloud VRP row"), r"lesson-correction"),
    M("r1-correction-indented", "R1", "lesson correction line gets a leading space (no longer a `Correction (round 45` line)",
      lambda r, c: sub(r, "corpus/lessons/round-44.md", "\nCorrection (round 45", "\n Correction (round 45"), r"lesson-correction"),
    M("r1-lesson-not-append-only", "R1", "baseline portion of corpus/lessons/round-44.md edited (leading x)",
      lambda r, c: wt(r, "corpus/lessons/round-44.md", "x" + rt(r, "corpus/lessons/round-44.md")), r"round-44-lesson-not-append-only"),
    # ---- R2 -------------------------------------------------------------------------------
    M("r2-enforced-by-missing", "R2", "R48 enforced-by path points at a file that does not exist",
      lambda r, c: sub(r, "corpus/QUALITY.md", "enforced-by: `corpus/instruments/r45-routed-defects.py`", "enforced-by: `corpus/instruments/does-not-exist.py`"), r"R48-enforced-by-not-a-file"),
    M("r2-enforced-by-directory", "R2", "R47 `enforced-by: `corpus`` (a directory)",
      lambda r, c: sub(r, "corpus/QUALITY.md", "enforced-by: `corpus/instruments/freeze-check.py`", "enforced-by: `corpus`"), r"R47-enforced-by-not-a-file"),
    M("r2-enforced-by-absent", "R2", "R49 criterion loses its `enforced-by:` clause",
      lambda r, c: sub(r, "corpus/QUALITY.md", " enforced-by: `corpus/instruments/source-recheck.py`", ""), r"R49-enforced-by-absent"),
    M("r2-quality-prefix-edited", "R2", "baseline QUALITY.md edited (not append-only)", _quality_prefix, r"quality-not-append-only"),
    M("r2-r49-ungrounded", "R2", "R49 grounded-in cell no longer names corpus/lessons/round-44.md",
      lambda r, c: sub(r, "corpus/QUALITY.md", R49_GRD, "grounded in the S070 shell page"), r"R49-ungrounded"),
    M("r2-duplicate-heading", "R2", "the `## Round-45 additions` heading appears twice",
      lambda r, c: wt(r, "corpus/QUALITY.md", rt(r, "corpus/QUALITY.md") + "\n## Round-45 additions — stray second block\n"), r"round-45-heading!=1"),
    M("r2-r47-lacks-before-data", "R2", "R47 criterion keeps `do-nothing` but loses `before data`",
      lambda r, c: sub(r, "corpus/QUALITY.md", "before data is read", "later"), r"R47-missing-before data"),
    M("r2-r48-lacks-presence-only", "R2", "R48 criterion spells `presence only` (no hyphen)",
      _quality_row_sub("R48", lambda ln: ln.replace("presence-only", "presence only")), r"R48-missing-presence-only"),
    M("r2-row-duplicated", "R2", "R48 row appears twice", _quality_row_sub("R48", lambda ln: ln + "\n" + ln), r"R48-rows=2"),
    M("r2-criterion-too-short", "R2", "R47 criterion cut to <300 chars keeping do-nothing, before data, enforced-by and a line ref",
      _quality_row_sub("R47", lambda ln: r_row("R47", "do-nothing control before data, `corpus/lessons/round-44.md:126`. enforced-by: `corpus/instruments/freeze-check.py`", R47_GRD)), r"R47-criterion-too-short"),
    M("r2-line-ref-out-of-range", "R2", "R48 line refs point at line 9999 of corpus/lessons/round-44.md",
      _quality_row_sub("R48", lambda ln: ln.replace("round-44.md:189", "round-44.md:9999")), r"R48-line-refs-absent-or-out-of-range"),
    M("r2-line-ref-zero", "R2", "R48 line ref is :0", _quality_row_sub("R48", lambda ln: ln.replace("round-44.md:189", "round-44.md:0")), r"R48-line-refs-absent-or-out-of-range"),
    M("r2-line-ref-absent", "R2", "R49 carries no corpus/lessons/round-44.md:<line> ref at all",
      _quality_row_sub("R49", lambda ln: ln.replace("round-44.md:131", "round-44.md")), r"R49-line-refs-absent-or-out-of-range"),
    M("r2-vacuous-criterion", "R2", "R48 criterion reduced to 'presence-only enforced-by: `LOG.md`' (keywords + any existing file)",
      _quality_row_sub("R48", lambda ln: r_row("R48", "presence-only enforced-by: `LOG.md`", R48_GRD)), r"R48-criterion-too-short"),
    M("r2-row-in-code-fence", "R2", "R49 row wrapped in ``` fences inside the Round-45 block (a fenced line is not a criterion row)",
      _quality_row_sub("R49", lambda ln: "```\n" + ln + "\n```"), r"R49-rows=0"),
    M("r2-row-in-html-comment", "R2", "R49 row wrapped in an HTML comment inside the Round-45 block",
      _quality_row_sub("R49", lambda ln: "<!--\n" + ln + "\n-->"), r"R49-rows=0"),
    M("r2-padded-filler-criterion", "R2", "INFO: R48 criterion padded with 400 chars of filler to pass the length floor (class word + any file + a ref)",
      _quality_row_sub("R48", lambda ln: r_row("R48", "presence-only " + "lorem ipsum " * 34 + "`corpus/lessons/round-44.md:16` enforced-by: `LOG.md`", R48_GRD)),
      r"R48-", info=True),
    M("r2-enforced-by-unrelated-file", "R2", "INFO: R47 enforced-by names LOG.md (an existing file that enforces nothing); predicate as written asks only that the path exists",
      lambda r, c: sub(r, "corpus/QUALITY.md", "enforced-by: `corpus/instruments/freeze-check.py`", "enforced-by: `LOG.md`"), r"R47-", info=True),
    # ---- R3 -------------------------------------------------------------------------------
    M("r3-code-byte-flipped", "R3", "r44-frontier-count.py `def main(` -> `def  main(` (behaviour-identical, one byte); GOOD pin kept",
      lambda r, c: sub(r, FR, "def main(argv: list[str]) -> int:", "def  main(argv: list[str]) -> int:"), r"r44-frontier-count-not-the-pinned-bytes"),
    M("r3-code-trailing-newline", "R3", "r44-frontier-count.py gains one trailing newline; GOOD pin kept",
      lambda r, c: wt(r, FR, rt(r, FR) + "\n"), r"r44-frontier-count-not-the-pinned-bytes"),
    M("r3-frontier-absent", "R3", "r44-frontier-count.py deleted", lambda r, c: os.unlink(p(r, FR)), r"r44-frontier-count-not-the-pinned-bytes"),
    M("r3-stub-selftest", "R3", "r44-frontier-count.py replaced by a 5-line stub printing `selftest cases=8 failures=0`; GOOD pin kept",
      lambda r, c: wt(r, FR, STUB_SELFTEST), r"r44-frontier-count-not-the-pinned-bytes"),
    M("r3-selftest-7-cases", "R3", "r44-frontier-count.py really grades 7 cases (re-pinned so the token limb is tested alone)",
      lambda r, c: wt(r, FR, frontier_src(rt(c["base"], FR), limit=7)), r"selftest-rc=\d+-tokens=\(7, 0\)", repin=("r44-frontier-count.py",)),
    M("r3-selftest-failure", "R3", "r44-frontier-count.py selftest case 1 expects admitted=99 -> failures=1 (re-pinned)",
      lambda r, c: wt(r, FR, frontier_src(rt(c["base"], FR), exp_admit=99)), r"selftest-rc=1-tokens=\(8, 1\)", repin=("r44-frontier-count.py",)),
    M("r3-registry-row-7-cells", "R3", "wave-registry.py registry row has 7 cells", _reg_sub("wave-registry.py", lambda row: row.replace(" | kasegi |\n", " |\n")), r"registry-row-wave-registry.py=1"),
    M("r3-registry-row-duplicated", "R3", "r44-routed-defects.py registry row appears twice", _reg_sub("r44-routed-defects.py", lambda row: row + row), r"registry-row-r44-routed-defects.py=2"),
    M("r3-registry-row-prose-only", "R3", "wave-registry.py registry row replaced by a prose sentence (name marker kept)",
      _reg_sub("wave-registry.py", lambda row: "wave-registry.py is registered in prose only (marker kept).\n"), r"registry-row-wave-registry.py=0"),
    M("r3-registry-row-in-code-fence", "R3", "wave-registry.py registry row wrapped in ``` fences inside the section (a fenced line is not a table row)",
      _reg_sub("wave-registry.py", lambda row: "```\n" + row + "```\n"), r"registry-row-wave-registry.py"),
    M("r3-registry-row-in-html-comment", "R3", "wave-registry.py registry row wrapped in an HTML comment inside the section",
      _reg_sub("wave-registry.py", lambda row: "<!--\n" + row + "-->\n"), r"registry-row-wave-registry.py"),
    M("r3-registry-section-renamed", "R3", "SKILL.md section heading renamed `## Round-45 gates`",
      lambda r, c: sub(r, "SKILL.md", "## Round-45 Gates & probes registry addition", "## Round-45 gates"), r"registry-section-absent"),
    M("r3-readme-row-bullet", "R3", "instruments README table row for r44-frontier-count.py turned into a bullet (name kept)",
      _readme_row(lambda row: "- r44-frontier-count.py counts frontier rows (prose, no table row)"), r"readme-row-absent"),
    M("r3-readme-row-in-code-fence", "R3", "instruments README row for r44-frontier-count.py wrapped in ``` fences",
      _readme_row(lambda row: "```\n" + row + "\n```"), r"readme-row-absent"),
    M("r3-skill-not-append-only", "R3", "SKILL.md baseline portion edited (leading space on line 1)", _skill_prefix, r"SKILL-not-append-only"),
    # ---- R4 -------------------------------------------------------------------------------
    M("r4-code-byte-flipped", "R4", "freeze-check.py `def main(argv):` -> `def  main(argv):` (behaviour-identical, one byte); GOOD pin kept",
      lambda r, c: sub(r, FC, "def main(argv):", "def  main(argv):"), r"freeze-check-not-the-pinned-bytes"),
    M("r4-stub-freeze-check", "R4", "freeze-check.py replaced by a 5-line stub printing both tokens; GOOD pin kept",
      lambda r, c: wt(r, FC, STUB_SELFTEST), r"freeze-check-not-the-pinned-bytes"),
    M("r4-freeze-selftest-5-cases", "R4", "freeze-check.py really grades 5 cases (re-pinned)",
      lambda r, c: wt(r, FC, freeze_src(limit=5)), r"selftest-rc=\d+-tokens=\(5, 0\)", repin=("freeze-check.py",)),
    M("r4-freeze-selftest-failure", "R4", "freeze-check.py selftest case 1 expects the wrong finding -> failures=1 (re-pinned)",
      lambda r, c: wt(r, FC, freeze_src(exp1="base-mismatch")), r"selftest-rc=1-tokens=\(8, 1\)", repin=("freeze-check.py",)),
    M("r4-freeze-absent", "R4", "freeze-check.py deleted (R47 enforced-by then names a missing file: R2 coupled)",
      lambda r, c: os.unlink(p(r, FC)), r"freeze-check-absent", coupled=("R2",)),
    M("r4-claims-weakened", "R4", "tree claims.json: counter_cmd of both claims replaced by `echo '<expect_before>'`; frozen pin kept",
      _claims_json(_claims_weaken), r"claims-not-the-frozen-bytes"),
    M("r4-claims-expect-changed", "R4", "tree claims.json: C2 expect_before changed; frozen pin kept",
      _claims_json(_claims_expect), r"claims-not-the-frozen-bytes"),
    M("r4-claims-trailing-newline", "R4", "tree claims.json gains one trailing newline; frozen pin kept",
      lambda r, c: wt(r, CLAIMS, rt(r, CLAIMS) + "\n"), r"claims-not-the-frozen-bytes"),
    M("r4-claims-absent", "R4", "tree claims.json deleted", lambda r, c: os.unlink(p(r, CLAIMS)), r"claims-not-the-frozen-bytes"),
    M("r4-claims-replay-short", "R4", "tree claims.json: C2 expect_before changed AND claims.json re-pinned, so only the replay (base_ok=1) can reject",
      _claims_json(_claims_expect), r"replay-rc=1", repin=("claims.json",)),
    # ---- R5 -------------------------------------------------------------------------------
    M("r5-usage-line", "R5", "refiled receipt carries a `usage:` line",
      _refiled(lambda t: "usage: r44-routed-defects.py [-h]\n" + t), r"usage-or-error-line-present"),
    M("r5-error-line-only", "R5", "refiled receipt carries only the argparse `error: ... --root` line (no `usage:`)",
      _refiled(lambda t: t + "r44-routed-defects.py: error: the following arguments are required: --root\n"), r"usage-or-error-line-present"),
    M("r5-original-changed", "R5", "original final-attempt3.txt gains one byte",
      lambda r, c: wt(r, ORIGINAL, rt(r, ORIGINAL) + " "), r"original-receipt-changed"),
    M("r5-invocation-absent", "R5", "refiled receipt loses the `--root X --selftest --work Y` invocation (token lines stay)",
      _refiled(lambda t: re.sub(r"--root \S+ --selftest --work \S+", "<invocation elided>", t)), r"invocation-lines=0"),
    M("r5-invocation-twice", "R5", "refiled receipt carries the invocation line twice", _refiled(lambda t: t.replace(INVOCATION + "\n", INVOCATION + "\n" + INVOCATION + "\n", 1)), r"invocation-lines=2"),
    M("r5-exit-nonzero", "R5", "refiled receipt ends `exit=1`", _refiled(lambda t: t.replace("\nexit=0\n", "\nexit=1\n", 1)), r"exit0-line-absent"),
    M("r5-cases-19", "R5", "refiled receipt reads `selftest cases=19 failures=0` (body edited, GOOD body pin kept)",
      _refiled(lambda t: t.replace("selftest cases=20 failures=0", "selftest cases=19 failures=0", 1)), r"receipt-body-not-the-pinned-run-output"),
    M("r5-receipt-body-edited", "R5", "refiled receipt: one case line edited (`fixed=8` -> `fixed=7`), every token line intact; GOOD body pin kept",
      _refiled(lambda t: t.replace("verdict=pass fixed=8 unresolved=0", "verdict=pass fixed=7 unresolved=0", 1)), r"receipt-body-not-the-pinned-run-output"),
    M("r5-receipt-body-line-deleted", "R5", "refiled receipt: one case line deleted, tokens intact",
      _refiled(lambda t: "\n".join(ln for ln in t.split("\n") if not ln.startswith("selftest case=D8-no-receipt")) ), r"receipt-body-not-the-pinned-run-output"),
    M("r5-receipt-body-extra-line", "R5", "refiled receipt: one extra harmless line inserted in the body",
      _refiled(lambda t: t.replace("selftest cases=20 failures=0", "note: extra line\nselftest cases=20 failures=0", 1)), r"receipt-body-not-the-pinned-run-output"),
    M("r5-fabricated-receipt", "R5", "refiled receipt is hand-typed: exact invocation line, the token, exit=0 (nothing was run)",
      lambda r, c: wt(r, REFILED, INVOCATION + "\nselftest cases=20 failures=0\nexit=0\n"), r"receipt-body-not-the-pinned-run-output"),
    M("r5-fabricated-comment-invocation", "R5", "refiled receipt is hand-typed with the invocation only as a `#` comment",
      lambda r, c: wt(r, REFILED, "# --root X --selftest --work Y\nselftest cases=20 failures=0\nexit=0\n"), r"invocation-lines=0"),
    M("r5-r44-counter-edited", "R5", "corpus/instruments/r44-routed-defects.py gains a trailing comment; GOOD pin kept",
      lambda r, c: wt(r, R44, rt(r, R44) + "\n# edited\n"), r"r44-counter-not-the-pinned-bytes"),
    M("r5-refiled-absent", "R5", "refiled receipt deleted", lambda r, c: os.unlink(p(r, REFILED)), r"refiled-absent"),
]


def write_pins(path: str, pins: dict) -> str:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(pins, fh)
    return path


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=LANE)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--counter", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    a.lane = os.path.abspath(a.lane)
    a.base = os.path.abspath(a.base)
    counter = os.path.abspath(a.counter or p(a.lane, "corpus/instruments/r45-routed-defects.py"))
    for d in (a.lane, a.base):
        if not os.path.isdir(d):
            print(f"r45-counters-selftest-c1: {d} is not a directory", file=sys.stderr)
            return 2
    if not os.path.isfile(counter):
        print(f"r45-counters-selftest-c1: counter {counter} not found", file=sys.stderr)
        return 2
    scratch = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kasegi-r45", "selftest-c1")
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="run-", dir=scratch)
    ext_tmp = os.environ.get("TMPDIR")
    tmp = ext_tmp if ext_tmp and os.path.isdir(ext_tmp) else os.path.join(work, "tmp")
    os.makedirs(tmp, exist_ok=True)
    cases = failures = 0
    false_green: list[str] = []
    try:
        good = os.path.join(work, "good")
        clone(a.base, good)
        build_good(good, a.lane, a.base, os.path.dirname(counter))
        gp = compute_pins(good)
        assert set(gp) == {"S072.txt", "freeze-check.py", "r44-frontier-count.py", "r44-routed-defects.py", "claims.json", "refiled-body"}, sorted(gp)
        gp.update({k: None for k in LINE_PINS})
        gpj = write_pins(os.path.join(work, "pins-good.json"), gp)
        print("synthetic pins (R45_PINS_OVERRIDE): " + " ".join(f"{k}={str(v)[:12]}" for k, v in sorted(gp.items())))
        ctx = {"lane": a.lane, "base": a.base, "good": good, "gp": gp}

        def line_case(name, ok, note):
            nonlocal cases, failures
            cases += 1
            failures += 0 if ok else 1
            print(f"case {name} verdict={'ok' if ok else 'FAIL'} {note}")

        g = run_counter(counter, good, a.base, tmp, gpj)
        print("GOOD counter output:\n" + "".join("  " + ln + "\n" for ln in g["out"].splitlines()))
        g_limbs = g["limbs"]
        line_case("control-good-tree", g["total"] == 5 and g["rc"] == 0 and all(v[0] == 1 for v in g_limbs.values()) and len(g_limbs) == 5,
                  f"total_fixed={g['total']} rc={g['rc']} expect fixed=5 " + " ".join(f"{k}={v[0]}" for k, v in sorted(g_limbs.items())))

        b = run_counter(counter, a.base, a.base, tmp, gpj)
        line_case("control-do-nothing-base", b["total"] == 0 and b["rc"] == 1, f"total_fixed={b['total']} rc={b['rc']} expect fixed=0 (pins override active)")

        nul = os.path.join(work, "null")
        clone(good, nul)
        n = run_counter(counter, nul, a.base, tmp, gpj)
        line_case("control-null-mutant", n["total"] == 5 and n["rc"] == 0 and not changed_files(good, nul),
                  f"total_fixed={n['total']} unchanged clone must stay fixed=5 (harness does not flag everything)")

        mk = os.path.join(work, "marker")
        clone(a.base, mk)
        wt(mk, "corpus/lessons/round-44.md", rt(mk, "corpus/lessons/round-44.md") + "\n" + LESSON_CORRECTION + "\n")
        wt(mk, "corpus/QUALITY.md", rt(mk, "corpus/QUALITY.md") + "\n## Round-45 additions\nR47 do-nothing before data; R48 presence-only; R49 capture method reject\n")
        wt(mk, "SKILL.md", rt(mk, "SKILL.md") + "\n## Round-45 Gates & probes registry addition (appended 2026-10-28)\nr44-frontier-count.py r44-routed-defects.py wave-registry.py\n")
        m = run_counter(counter, mk, a.base, tmp, gpj)
        line_case("control-marker-only", m["total"] == 0 and m["rc"] == 1, f"total_fixed={m['total']} prose markers only, no artifacts: expect fixed=0")

        rp = run_counter(counter, good, a.base, tmp, None)
        rl = rp["limbs"]
        line_case("control-good-tree-under-real-pins", rl.get("R3", (1,))[0] == 0 and rl.get("R4", (1,))[0] == 0
                  and "not-the-pinned-bytes" in rl.get("R3", (0, ""))[1] and "not-the-pinned-bytes" in rl.get("R4", (0, ""))[1],
                  f"no override: the synthetic code must NOT satisfy the real pins; " + " ".join(f"{k}={v[0]}({v[1]})" for k, v in sorted(rl.items())))

        only = set(a.only.split(",")) if a.only else None
        todo = []
        for mu in MUTANTS:
            if only and mu["id"] not in only:
                continue
            d = os.path.join(work, "m-" + mu["id"])
            clone(good, d)
            err = None
            try:
                mu["fn"](d, ctx)
            except Exception as exc:  # builder broke: a harness error, never a pass
                err = f"{type(exc).__name__}: {exc}"
            pins = dict(gp)
            if mu["repin"]:
                pins.update(compute_pins(d, set(mu["repin"])))
            todo.append((mu, d, err, write_pins(os.path.join(work, f"pins-{mu['id']}.json"), pins)))

        def go(item):
            mu, d, err, pj = item
            if err:
                return None
            return run_counter(counter, d, a.base, tmp, pj)

        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            results = list(ex.map(go, todo))

        for (mu, d, err, _pj), res in zip(todo, results):
            cases += 1
            if res is None:
                failures += 1
                print(f"case {mu['id']} limb={mu['limb']} verdict=HARNESS-ERROR {err}")
                shutil.rmtree(d, ignore_errors=True)
                continue
            ch = changed_files(good, d)
            limbs, total = res["limbs"], res["total"]
            tgt = limbs.get(mu["limb"], (None, "no-limb-line"))
            collateral = sorted(k for k, v in limbs.items() if k != mu["limb"] and k not in mu["coupled"] and v[0] != g_limbs[k][0])
            coupled_ok = all(limbs.get(k, (1,))[0] == 0 for k in mu["coupled"])
            if tgt[0] == 1:
                verdict = "FALSE-GREEN"
            elif tgt[0] is None or not ch:
                verdict = "HARNESS-ERROR(no-limb-line-or-no-change)"
            elif collateral or not coupled_ok or total != 5 - 1 - len(mu["coupled"]) or res["rc"] != 1:
                verdict = "COLLATERAL"
            elif not re.search(mu["why"], tgt[1]):
                verdict = "WRONG-REASON"
            else:
                verdict = "rejected"
            if mu["info"]:
                verdict = "info-" + ("accepted" if tgt[0] == 1 else "rejected")
                ok = True
            else:
                ok = verdict == "rejected"
            if verdict == "FALSE-GREEN":
                false_green.append(f"FALSE-GREEN mutant={mu['id']} limb={mu['limb']} recipe: {mu['desc']} | counter read: limb {mu['limb']} fixed=1 read={tgt[1]} total={total}")
            if verdict.startswith("info-accepted"):
                false_green.append(f"INFO-ACCEPTED (not counted) mutant={mu['id']} limb={mu['limb']} recipe: {mu['desc']} | counter read: limb {mu['limb']} fixed=1 read={tgt[1]}")
            if not ok:
                failures += 1
            print(f"case {mu['id']} limb={mu['limb']} target_fixed={tgt[0]} total_fixed={total} rc={res['rc']} verdict={verdict} "
                  f"changed={','.join(ch)} read={tgt[1]}" + (f" collateral={collateral}" if collateral else "") + (f" want_why={mu['why']!r}" if verdict == "WRONG-REASON" else ""))
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
