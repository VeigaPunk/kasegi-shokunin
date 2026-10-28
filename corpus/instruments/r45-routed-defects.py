#!/usr/bin/env python3
"""r45-routed-defects.py — round-45 C1 counter (depth:verifiability), v1.1 (hardened after the wave-1 falsification).

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

VERSION 1.1 (erratum E1, predicate and limb names unchanged; v1 digest 82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee)
    Wave 1 falsified v1 (`.ufo/waves/round-45/wave1/R45Rev*`, `R45Mut*`, `R45ExecSelftestC1.md`): vacuous `flip: tbd`, a row inside a code fence,
    a stub freeze-check/selftest that prints the tokens, a weakened claims file replayed from the graded tree, a hand-typed receipt, directory
    `enforced-by` targets.  v1.1 binds CONTENT: the frozen source capture is pinned by sha256, code artifacts (r44-frontier-count.py, freeze-check.py,
    r44-routed-defects.py) are pinned by sha256 so a stub must reproduce the genuine bytes, the claims file replayed by R4 must equal the frozen
    claims sha, rows are read only from the real registry table (not fences/comments), the lesson correction must quote located S072 text, and the
    R5 receipt body must equal the pinned one-run output of the r44 selftest at c950fa3.  source-recheck.py and freeze-check.py run from THIS script's own lane
    (the grader's tool root), never from the graded tree.

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
import shutil
import subprocess
import sys
import tempfile

TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PINS = {
    "S072.txt": "364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025",
    "freeze-check.py": "6809c99cd9a491bd343365ed36548d8ae81cd55d1a29d47252f7aa898cab079c",
    "r44-frontier-count.py": "966da7739160a837f57f06e98079c3d7f04ab4975d97d53126a56a1df70cf93a",
    "r44-routed-defects.py": "d5438c67befaefadf46e44474330771d5d5b7b3b8f0c5ec3df11ef422ca7ba90",
    "refiled-body": "03fe3af53006dc7561b6080b5bd923312569a5a2b8ca3d7b6ad3722da9f226c0",
    "R1-row": "a81e05d28128cf1d76b9d7616ea955cbd4e4fecc2af60a9a8a149d0803b11b9c",
    "R1-corr": "1a7dbdefe50978a80353c2533027690c03c8608a844175ef4243499b7aa0c187",
    "R2-R47": "ab375d48780d09566806ce68ed47a60b06cc7e40891006cb5d5bc77d51263900",
    "R2-R48": "7255d97d7456b8ea8a3d22f04d64681a7054331efb55c0c5d55093b761135ef7",
    "R2-R49": "e1b43f7ae5401bcbf829968004ff80a0b624b3c282b0d96696c3a07399cfb9d4",
    "R3-skill-r44-frontier-count.py": "035d2e9feb9bdbb2558d4615222c8f6be696e3bd95b75dcc6f620aa6d7f9c02b",
    "R3-skill-r44-routed-defects.py": "bfbe33563f6b9e9a243302698d38aeb07d081ec3644f163f3afd3efa43b0efea",
    "R3-skill-wave-registry.py": "f6064805acfe0fe4309871216943f51a0b91962f16976c24303015aee5eb36c9",
    "R3-readme-r44-frontier-count.py": "035d2e9feb9bdbb2558d4615222c8f6be696e3bd95b75dcc6f620aa6d7f9c02b",
    "claims.json": "bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206",
}
if os.environ.get("R45_PINS_OVERRIDE"):  # selftests only: the grader's environment, never the graded tree's
    import json as _json
    PINS.update(_json.load(open(os.environ["R45_PINS_OVERRIDE"])))


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(s: str) -> str:
    s = re.sub(r"</?u>|\*\*|``", "", s)
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def live_lines(t: str) -> list[str]:
    """Lines outside HTML comments and fenced code blocks (``` and ~~~)."""
    t = re.sub(r"(?s)<!--.*?-->", "", t)
    out, fence = [], None
    for ln in t.splitlines():
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            mark = st[:3]
            fence = None if fence == mark else (fence or mark)
            continue
        if fence is None:
            out.append(ln)
    return out


def pinned(key: str, line: str) -> bool:
    if key in PINS and PINS[key] is None:  # grader-side override only (selftests): this one pin is disabled
        return True
    return sha(line.strip().encode("utf-8")) == PINS.get(key)


def registry_lines(root: str) -> list[str]:
    """Lines of the real registry table only: after `## Registry`, before the next `## `, outside fences and HTML comments."""
    out, inreg = [], False
    for ln in live_lines(txt(root, "corpus/SOURCES.md") or ""):
        if re.match(r"^ {0,3}## ", ln):
            inreg = bool(re.match(r"^ {0,3}## Registry\b", ln))
            continue
        if inreg:
            out.append(ln)
    return out


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
    rows: dict[str, list[str]] = {}
    for line in registry_lines(root):
        if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", line):
            cells = line.strip().strip("|").split("|")
            if len(cells) == 11:
                rows[cells[0].strip()] = [c.strip() for c in cells]
    return rows


def raw_row_line(root: str, sid: str) -> str | None:
    found = [ln for ln in registry_lines(root) if re.match(r"^ {0,3}\|\s*%s\s*\|" % re.escape(sid), ln)]
    return found[0] if len(found) == 1 else None


def limb_r1(root: str, base: str) -> tuple[bool, str]:
    rows = sources_rows(root)
    row = rows.get("S072")
    if row is None:
        return False, "row-S072=absent"
    # columns: id source kind tier scope anchor teaches status opened recheck used-by
    rowline = [ln for ln in registry_lines(root) if re.match(r"^ {0,3}\|\s*S072\s*\|", ln)][0]
    if not pinned("R1-row", rowline):
        return False, "S072-row-not-the-pinned-line"
    teaches, status = row[6], row[7]
    if not teaches.startswith("supersedes S070 —"):
        return False, "teaches-not-supersedes"
    if status != "rejected":
        return False, f"status={status}"
    if not re.search(r"flip:\s*(?:\S+\s+){7,}\S+", teaches):  # a checkable condition: at least eight words, not `tbd`
        return False, "flip-absent"
    if not re.search(r"(?<![0-9])10[ ,]?029(?![0-9])", teaches):
        return False, "size-token-absent"
    if not re.search(r"\breadable\b", teaches):
        return False, "readable-absent"
    old = raw_row_line(base, "S070")
    new = raw_row_line(root, "S070")
    if old is None or old != new:
        return False, "S070-row-changed-or-baseline-absent"
    man = ".ufo/waves/round-45/source-recon/S072.manifest.json"
    if rd(root, man) is None:
        return False, "manifest-absent"
    rc, out = run([sys.executable, "-I", os.path.join(TOOL_ROOT, "corpus/instruments/source-recheck.py"), "--manifest",
                   os.path.join(root, man), "--source", "S072"], root)
    oks = len(re.findall(r"^S072:Q\d+ OK ", out, re.M))
    if rc != 0 or "S072:sha256 OK" not in out or oks < 2:
        return False, f"recheck-rc={rc}-quotes={oks}"
    snap = rd(root, ".ufo/waves/round-45/source-recon/S072.txt")
    if snap is None or sha(snap) != PINS["S072.txt"] or PINS["S072.txt"] not in row[5]:
        return False, "snapshot-not-the-pinned-capture-or-not-in-anchor"
    snapnorm = norm(snap.decode("utf-8", "replace"))
    les = txt(root, "corpus/lessons/round-44.md") or ""
    les_b = txt(base, "corpus/lessons/round-44.md") or ""
    if not les.startswith(les_b) or not les_b:
        return False, "round-44-lesson-not-append-only"
    tail = les[len(les_b):]
    hit = []
    for ln in tail.splitlines():
        if ln.startswith("Correction (round 45") and "S072" in ln and re.search(r"(?<![0-9])10[ ,]?029(?![0-9])", ln):
            spans = re.findall("\u201c([^\u201d]{30,})\u201d", ln)
            if any(len(norm(sp).split()) >= 6 and norm(sp) in snapnorm for sp in spans) and pinned("R1-corr", ln):
                hit.append(ln)
    if not hit:
        return False, "lesson-correction-absent-or-quotes-no-located-S072-span"
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
    tail_raw = q[len(qb):].decode("utf-8", "replace")
    tail = "\n".join(live_lines(tail_raw))
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
        if not pinned("R2-" + rid, lines[0]):
            return False, f"{rid}-row-not-the-pinned-line"
        if "corpus/lessons/round-44.md" not in ground:
            return False, f"{rid}-ungrounded"
        for nd in needles:
            if not re.search(nd, crit, re.I):
                return False, f"{rid}-missing-{nd}"
        paths = re.findall(r"enforced-by:\s*`([^`]+)`", crit)
        if not paths:
            return False, f"{rid}-enforced-by-absent"
        for p in paths:
            if not os.path.isfile(os.path.join(root, p.split(" ")[0])):
                return False, f"{rid}-enforced-by-not-a-file-{p}"
        if len(crit) < 300:
            return False, f"{rid}-criterion-too-short"
        les_lines = len((txt(root, "corpus/lessons/round-44.md") or "").splitlines())
        refs = [int(n) for n in re.findall(r"corpus/lessons/round-44\.md:(\d+)", crit + " " + ground)]
        if not refs or any(r < 1 or r > les_lines for r in refs):
            return False, f"{rid}-line-refs-absent-or-out-of-range"
        seen += 1
    return True, f"criteria={seen}"


def selftest_tokens(out: str) -> tuple[int, int] | None:
    m = re.search(r"^selftest cases=(\d+) failures=(\d+)\s*$", out, re.M)
    return (int(m.group(1)), int(m.group(2))) if m else None


def limb_r3(root: str, base: str) -> tuple[bool, str]:
    s = os.path.join(root, "corpus/instruments/r44-frontier-count.py")
    b = rd(root, "corpus/instruments/r44-frontier-count.py")
    if b is None or sha(b) != PINS["r44-frontier-count.py"]:
        return False, "r44-frontier-count-not-the-pinned-bytes"
    rc, out = run([sys.executable, "-I", s, "--selftest"], root)
    tk = selftest_tokens(out)
    if rc != 0 or tk is None or tk[1] != 0 or tk[0] < 8:
        return False, f"selftest-rc={rc}-tokens={tk}"
    sk = txt(root, "SKILL.md") or ""
    skb = txt(base, "SKILL.md") or ""
    if not sk.startswith(skb):
        return False, "SKILL-not-append-only"
    m = re.search(r"^## Round-45 Gates & probes registry addition.*?(?=^## |\Z)", "\n".join(live_lines(sk[len(skb):])) + "\n", re.M | re.S)
    if not m:
        return False, "registry-section-absent"
    for name in ("r44-frontier-count.py", "r44-routed-defects.py", "wave-registry.py"):
        rows = [ln for ln in m.group(0).splitlines() if re.match(r"^\|\s*%s\s*\|" % re.escape(name), ln)]
        if len(rows) != 1 or len(rows[0].strip().strip("|").split("|")) != 8:
            return False, f"registry-row-{name}={len(rows)}"
        if not pinned("R3-skill-" + name, rows[0]):
            return False, f"registry-row-{name}-not-the-pinned-line"
    rd_rows = [ln for ln in live_lines(txt(root, "corpus/instruments/README.md") or "") if re.match(r"^\|\s*`?r44-frontier-count\.py`?\s*\|", ln)]
    if len(rd_rows) != 1 or not pinned("R3-readme-r44-frontier-count.py", rd_rows[0]):
        return False, "readme-row-absent-or-not-the-pinned-line"
    return True, f"selftest-cases={tk[0]}"


def limb_r4(root: str, base: str) -> tuple[bool, str]:
    fc = os.path.join(root, "corpus/instruments/freeze-check.py")
    if not os.path.exists(fc):
        return False, "freeze-check-absent"
    if sha(open(fc, "rb").read()) != PINS["freeze-check.py"]:
        return False, "freeze-check-not-the-pinned-bytes"
    rc, out = run([sys.executable, "-I", fc, "--selftest"], root)
    tk = selftest_tokens(out)
    if rc != 0 or tk is None or tk[1] != 0 or tk[0] < 6:
        return False, f"selftest-rc={rc}-tokens={tk}"
    claims = os.path.join(root, ".ufo/waves/round-45/claims.json")
    cb = rd(root, ".ufo/waves/round-45/claims.json")
    if cb is None or sha(cb) != PINS["claims.json"]:
        return False, "claims-not-the-frozen-bytes"
    rc, out = run([sys.executable, "-I", fc, "--claims", claims, "--tool-root", TOOL_ROOT, "--base", base], TOOL_ROOT)
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
    lines = t.splitlines()
    inv = [i for i, ln in enumerate(lines) if ln == "$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>"]
    if len(inv) != 1:
        return False, f"invocation-lines={len(inv)}"
    end = [i for i, ln in enumerate(lines) if ln == "exit=0"]
    if len(end) != 1 or end[0] <= inv[0]:
        return False, "exit0-line-absent"
    if inv[0] != 0 or end[0] != len(lines) - 1:  # QUALITY R37/R39: no hand-written header, nothing appended after the run
        return False, "receipt-has-lines-before-the-invocation-or-after-exit"
    body = lines[inv[0] + 1:end[0]]
    o = rd(base, ".ufo/waves/round-44/controls/final-attempt3.txt")
    n = rd(root, ".ufo/waves/round-44/controls/final-attempt3.txt")
    if o is None or o != n:
        return False, "original-receipt-changed"
    r44 = rd(root, "corpus/instruments/r44-routed-defects.py")
    if r44 is None or sha(r44) != PINS["r44-routed-defects.py"]:
        return False, "r44-counter-not-the-pinned-bytes"
    # The r44 selftest only passes on the round-44 tip export (c950fa3): at later lane trees its limb D4 reads unresolved
    # (recorded in SKILL.md, Round-45 registry row), so the body is bound by sha256 of the genuine one-run output instead of a re-run.
    if sha("\n".join(body).encode()) != PINS["refiled-body"] or not re.search(r"^selftest cases=20 failures=0$", "\n".join(body), re.M):
        return False, "receipt-body-not-the-pinned-run-output"
    return True, "refiled=pinned-run-output original=unchanged"


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
