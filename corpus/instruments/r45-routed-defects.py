#!/usr/bin/env python3
"""r45-routed-defects.py — round-45 C1 counter (depth:verifiability), v1.

WHAT IT MEASURES
    The five status-bearing routed defects of
    `corpus/lessons/round-44-verifier-spotcheck.md` §6 (items 1-5).  Item 6 (the
    round-44 L1 process defect) is self-reported, carries no lane-side artifact
    and is NOT counted: the counted set is exactly five, named R1..R5 below.

    R1  S070 reject reason: a NEW registry row S072 whose `teaches` opens
        `supersedes S070 —`, status `rejected`, a checkable `flip:` clause, a
        sha-pinned snapshot with located quotes (source-recheck exit 0), the
        readable-body size token (10029 characters), the S070 row byte-identical
        to the baseline, and an appended `Correction (round 45` line in
        corpus/lessons/round-44.md that cites S072 and the size token.
    R2  QUALITY.md criteria R47/R48/R49 (append-only), each grounded in
        `corpus/lessons/round-44.md`, each naming its class and an
        `enforced-by:` path that exists:
          R47 do-nothing control replayed before data   (do-nothing, before data)
          R48 presence-only predicates                  (presence-only)
          R49 capture method parity for admit and reject (capture method, reject)
    R3  r44-frontier-count.py is a registered gate: `--selftest` prints
        `selftest cases=N failures=0` with N >= 8; SKILL.md carries a
        `## Round-45 Gates & probes registry addition` table with eight-cell
        rows for r44-frontier-count.py, r44-routed-defects.py and
        wave-registry.py; corpus/instruments/README.md has a row for
        r44-frontier-count.py.
    R4  freeze hygiene: corpus/instruments/freeze-check.py `--selftest` prints
        `selftest cases=N failures=0` with N >= 6, and the round-45 claims file
        replays clean at the baseline (`freeze-check claims=2 base_ok=2`).
    R5  receipt wording: `.ufo/waves/round-44/controls/final-attempt3-refiled.txt`
        carries the selftest invocation without the failed bare call (no
        `usage:` / `error:` line, `selftest cases=20 failures=0`, `exit=0`), and
        the original `final-attempt3.txt` is byte-identical to the baseline.

    A limb counts only when the bound artifact bytes carry the content; every
    value is read as a whole token and printed.  READ-ONLY over --root and
    --baseline; never runs git.  Honors TMPDIR (no hardcoded /tmp).

USAGE
    python3 corpus/instruments/r45-routed-defects.py --root TREE --baseline TREE
OUTPUT
    one `limb R<n> fixed=0|1 read=<token>` line each, then
    `routed-defects total=5 fixed=<k> unresolved=<5-k> exit=0|1`
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys

CENSUS = os.environ.get("SOURCES_CENSUS", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")


def rd(root: str, rel: str) -> bytes | None:
    try:
        with open(os.path.join(root, rel), "rb") as fh:
            return fh.read()
    except OSError:
        return None


def txt(root: str, rel: str) -> str | None:
    b = rd(root, rel)
    return None if b is None else b.decode("utf-8", "replace")


def run(cmd: list[str], cwd: str, env_extra: dict | None = None, timeout: int = 300) -> tuple[int, str]:
    env = dict(os.environ)
    env.update(env_extra or {})
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    except (OSError, subprocess.SubprocessError) as exc:  # fail closed
        return 99, f"run-error {exc}"
    return p.returncode, p.stdout + p.stderr


def sources_rows(root: str) -> dict[str, list[str]]:
    t = txt(root, "corpus/SOURCES.md") or ""
    rows: dict[str, list[str]] = {}
    for line in t.splitlines():
        if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", line):
            cells = line.strip().strip("|").split("|")
            if len(cells) == 11:
                rows[cells[0].strip()] = [c.strip() for c in cells]
    return rows


def raw_row_line(root: str, sid: str) -> str | None:
    for line in (txt(root, "corpus/SOURCES.md") or "").splitlines():
        if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(sid), line):
            return line
    return None


def limb_r1(root: str, base: str) -> tuple[bool, str]:
    rows = sources_rows(root)
    row = rows.get("S072")
    if row is None:
        return False, "row-S072=absent"
    # columns: id source kind tier scope anchor teaches status opened recheck used-by
    teaches, status = row[6], row[7]
    if not teaches.startswith("supersedes S070 —"):
        return False, "teaches-not-supersedes"
    if status != "rejected":
        return False, f"status={status}"
    if not re.search(r"flip:\s*\S", teaches):
        return False, "flip-absent"
    if not re.search(r"(?<![0-9])10[ ,]?029(?![0-9])", teaches):
        return False, "size-token-absent"
    if not re.search(r"\breadable\b", teaches):
        return False, "readable-absent"
    old = raw_row_line(base, "S070")
    new = raw_row_line(root, "S070")
    if old is None or old != new:
        return False, "S070-row-changed-or-baseline-absent"
    man = "corpus/source-snapshots/round-45/manifest.json"
    if rd(root, man) is None:
        return False, "manifest-absent"
    rc, out = run([sys.executable, os.path.join(root, "corpus/instruments/source-recheck.py"), "--manifest",
                   os.path.join(root, man), "--source", "S072"], root)
    oks = len(re.findall(r"^S072:Q\d+ OK ", out, re.M))
    if rc != 0 or "S072:sha256 OK" not in out or oks < 2:
        return False, f"recheck-rc={rc}-quotes={oks}"
    snap = rd(root, "corpus/source-snapshots/round-45/S072.txt")
    if snap is None or hashlib.sha256(snap).hexdigest() not in row[5]:
        return False, "snapshot-sha-not-in-anchor"
    les = txt(root, "corpus/lessons/round-44.md") or ""
    les_b = txt(base, "corpus/lessons/round-44.md") or ""
    if not les.startswith(les_b) or not les_b:
        return False, "round-44-lesson-not-append-only"
    tail = les[len(les_b):]
    hit = [ln for ln in tail.splitlines() if ln.startswith("Correction (round 45") and "S072" in ln
           and re.search(r"(?<![0-9])10[ ,]?029(?![0-9])", ln)]
    if not hit:
        return False, "lesson-correction-absent"
    return True, f"S072=supersedes recheck-quotes={oks} corrections={len(hit)}"


CLASS_RX = {
    "R47": [r"do-nothing", r"before data"],
    "R48": [r"presence-only"],
    "R49": [r"capture method", r"reject"],
}


def limb_r2(root: str, base: str) -> tuple[bool, str]:
    q = rd(root, "corpus/QUALITY.md")
    qb = rd(base, "corpus/QUALITY.md")
    if q is None or qb is None or not q.startswith(qb) or q == qb:
        return False, "quality-not-append-only-or-unchanged"
    tail = q[len(qb):].decode("utf-8", "replace")
    if len(re.findall(r"^## Round-45 additions", tail, re.M)) != 1:
        return False, "round-45-heading!=1"
    seen = 0
    for rid, needles in CLASS_RX.items():
        lines = [ln for ln in tail.splitlines() if re.match(r"^\|\s*%s\s*\|" % rid, ln)]
        if len(lines) != 1:
            return False, f"{rid}-rows={len(lines)}"
        cells = lines[0].strip().strip("|").split("|")
        if len(cells) != 3:
            return False, f"{rid}-cells={len(cells)}"
        crit, ground = cells[1], cells[2]
        if "corpus/lessons/round-44.md" not in ground:
            return False, f"{rid}-ungrounded"
        for nd in needles:
            if not re.search(nd, crit, re.I):
                return False, f"{rid}-missing-{nd}"
        paths = re.findall(r"enforced-by:\s*`([^`]+)`", crit)
        if not paths:
            return False, f"{rid}-enforced-by-absent"
        for p in paths:
            if not os.path.exists(os.path.join(root, p.split(" ")[0])):
                return False, f"{rid}-enforced-by-missing-{p}"
        seen += 1
    return True, f"criteria={seen}"


def selftest_tokens(out: str) -> tuple[int, int] | None:
    m = re.search(r"^selftest cases=(\d+) failures=(\d+)\s*$", out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else None


def limb_r3(root: str, base: str) -> tuple[bool, str]:
    s = os.path.join(root, "corpus/instruments/r44-frontier-count.py")
    rc, out = run([sys.executable, s, "--selftest"], root)
    tk = selftest_tokens(out)
    if rc != 0 or tk is None or tk[1] != 0 or tk[0] < 8:
        return False, f"selftest-rc={rc}-tokens={tk}"
    sk = txt(root, "SKILL.md") or ""
    skb = txt(base, "SKILL.md") or ""
    if not sk.startswith(skb):
        return False, "SKILL-not-append-only"
    m = re.search(r"^## Round-45 Gates & probes registry addition.*?(?=^## |\Z)", sk[len(skb):], re.M | re.S)
    if not m:
        return False, "registry-section-absent"
    for name in ("r44-frontier-count.py", "r44-routed-defects.py", "wave-registry.py"):
        rows = [ln for ln in m.group(0).splitlines() if re.match(r"^\|\s*%s\s*\|" % re.escape(name), ln)]
        if len(rows) != 1 or len(rows[0].strip().strip("|").split("|")) != 8:
            return False, f"registry-row-{name}={len(rows)}"
    rd_ = txt(root, "corpus/instruments/README.md") or ""
    if not re.search(r"^\|\s*`?r44-frontier-count\.py`?\s*\|", rd_, re.M):
        return False, "readme-row-absent"
    return True, f"selftest-cases={tk[0]}"


def limb_r4(root: str, base: str) -> tuple[bool, str]:
    fc = os.path.join(root, "corpus/instruments/freeze-check.py")
    if not os.path.exists(fc):
        return False, "freeze-check-absent"
    rc, out = run([sys.executable, fc, "--selftest"], root)
    tk = selftest_tokens(out)
    if rc != 0 or tk is None or tk[1] != 0 or tk[0] < 6:
        return False, f"selftest-rc={rc}-tokens={tk}"
    claims = os.path.join(root, ".ufo/waves/round-45/claims.json")
    rc, out = run([sys.executable, fc, "--claims", claims, "--tool-root", root, "--base", base], root)
    if rc != 0 or not re.search(r"^freeze-check claims=2 base_ok=2\b", out, re.M):
        return False, f"replay-rc={rc}"
    return True, f"selftest-cases={tk[0]} replay=base_ok=2"


def limb_r5(root: str, base: str) -> tuple[bool, str]:
    rel = ".ufo/waves/round-44/controls/final-attempt3-refiled.txt"
    t = txt(root, rel)
    if t is None:
        return False, "refiled-absent"
    if re.search(r"^(usage:|.*error:)", t, re.M | re.I):
        return False, "usage-or-error-line-present"
    if not re.search(r"^selftest cases=20 failures=0\s*$", t, re.M):
        return False, "selftest-token-absent"
    if not re.search(r"(^|\s)exit=0\s*$", t, re.M):
        return False, "exit0-absent"
    if not re.search(r"--root \S+ --selftest --work \S+", t):
        return False, "invocation-absent"
    o = rd(base, ".ufo/waves/round-44/controls/final-attempt3.txt")
    n = rd(root, ".ufo/waves/round-44/controls/final-attempt3.txt")
    if o is None or o != n:
        return False, "original-receipt-changed"
    return True, "refiled=ok original=unchanged"


LIMBS = [("R1", limb_r1), ("R2", limb_r2), ("R3", limb_r3), ("R4", limb_r4), ("R5", limb_r5)]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--baseline", required=True)
    a = ap.parse_args(argv)
    for d in (a.root, a.baseline):
        if not os.path.isdir(d):
            print(f"r45-routed-defects: {d} is not a directory", file=sys.stderr)
            return 2
    fixed = 0
    for lid, fn in LIMBS:
        try:
            ok, read = fn(os.path.abspath(a.root), os.path.abspath(a.baseline))
        except Exception as exc:  # fail closed, print the reason
            ok, read = False, f"exception-{type(exc).__name__}"
        fixed += 1 if ok else 0
        print(f"limb {lid} fixed={1 if ok else 0} read={read}")
    unresolved = len(LIMBS) - fixed
    code = 0 if unresolved == 0 else 1
    print(f"routed-defects total={len(LIMBS)} fixed={fixed} unresolved={unresolved} exit={code}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
