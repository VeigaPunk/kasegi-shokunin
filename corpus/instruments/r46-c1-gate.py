#!/usr/bin/env python3
"""r46-c1-gate.py — round-46 C1 counter (depth:verifiability), v1.2 (hardened after the wave-1 and wave-2 falsification; errata E1 and E2, see .ufo/waves/round-46/counter-errata.md; v1 sha256 b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294).

WHAT IT MEASURES
    How many of the lane's `recheck:` lines are *gated* (run, then fail closed on a
    lost base) — `recheck-audit.py` calls that `gated`; `score-gap.py` prints it as the
    distance to depth:verifiability 5 — and whether a line stopped being gated because
    the entry was re-grounded on committed bytes, never because the line was
    softened.  A re-grounded entry carries, appended at its end, a section

        ## Re-ground (round 46)
        | id | current claim | committed anchor | token |
        | G1 | <the claim, in the entry's words> | `corpus/instruments/x.py:51` | `a substring` |

    and a recheck line `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry
    corpus/knowledge/<entry>.md` that exits 0 only while every row's token is found in
    the anchored committed lines.  Lines outside that section stay what they were
    (historical observations of a lost tree), and the section says so.

TWO MODES
    --entry corpus/knowledge/X.md [--root TREE]     per-entry re-ground check (the recheck line)
        one `row G<n> ok=0|1 read=<token>` line each, then
        `reground entry=X rows=<n> ok=<k> files=<f> distinct=0|1 exit=0|1`
        PASS needs: section present once, >= 6 rows with unique ids, every anchor a
        regular non-symlink file under corpus/instruments/ or corpus/source-snapshots/
        inside TREE (never the entry itself), a <= 40-line range inside the file, and the
        token (>= 8 chars, whitespace-normalised) inside those lines; >= 2 distinct anchor files; no repeated (anchor, range) or token.
    --root TREE --baseline BASE                      aggregate counter, seven limbs
        L1  gated lines at TREE <= 22, broken = 0, lines >= base lines
        L2  regrounded set R = gated(BASE) - gated(TREE): |R| >= 2 and gated(TREE) = gated(BASE) - |R|
        L3  every entry of R: exactly one `recheck:` line, and it is `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<itself>.md` (optional trailing ` # comment`), no ~/ or $HOME path
        L4  every entry of R: per-entry mode (this script's own bytes, not the tree's) exits 0 at TREE and every anchored file is byte-identical to BASE's
        L5  every entry of R: append-only — every BASE line except the recheck line is, in order, a prefix of TREE's, and the BASE recheck command survives verbatim as one `restoration-recheck:` line
        L6  every entry of R: each row is load-bearing — after an unmutated scratch copy reads green, blanking that row's token
            inside its anchored lines turns per-entry mode red on exactly that row (all rows of all entries of R)
        L7  entries gated at BASE and still gated at TREE are byte-identical to BASE
    Rechecks run with the leading `cd <path> &&` stripped and cwd = TREE (an export root measures itself, not the live lane), under the
    grader's own environment: BASE and TREE are read under the same HOME, so a host change moves both readings and L2 (the regrounded set)
    stays 0; only allow-listed line shapes are executed (see allowed(): `test`, `set -o pipefail`, `git -C <dir> rev-parse HEAD`, `python3 corpus/instruments/<x>.py`
    run from THIS lane's instruments, a minimal environment); gated = allow-listed, parses and exits non-zero; broken = does not parse or is not allow-listed.

    READ-ONLY on TREE and BASE; scratch under --work / TMPDIR; never runs git; stdlib only.
OUTPUT
    `gate L<n> pass=0|1 read=<token>` lines, then `c1-gate fixed=<k>/7 exit=0|1` (the gated count is on the L1 line)
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

SECTION = "## Re-ground (round 46)"
TARGET_GATED = 22
MIN_ROWS = 6
MIN_TOKEN = 8
LANE_CD = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MIN_REGROUNDED = 2
ANCHOR_DIRS = ("corpus/instruments/", "corpus/source-snapshots/")
SELF = os.path.abspath(__file__)
RECHECK_RE = re.compile(r"^recheck:[ \t]*(.*)$")
CD_RE = re.compile(r"^cd[ \t]+[^&;]+?[ \t]*&&[ \t]*")
HOME_RE = re.compile(r"(?:~/|\$HOME|\$\{HOME\}|/home/)")
RESTORE_RE = re.compile(r"^restoration-recheck:[ \t]*(.*)$")


def exact_line(entry_name: str) -> re.Pattern:
    return re.compile(r"^cd " + re.escape(LANE_CD) + r" && python3 corpus/instruments/r46-c1-gate\.py --entry corpus/knowledge/"
                      + re.escape(entry_name) + r"(?:[ \t]+#.*)?$")


TOOL_LANE = os.path.dirname(os.path.dirname(os.path.dirname(SELF)))
SEG_TEST = re.compile(r"^test (?:! )?-[defs] [~A-Za-z0-9_./-]+$")
SEG_GIT = re.compile(r"^git -C [~A-Za-z0-9_./-]+ rev-parse HEAD$")
SEG_PY = re.compile(r"^python3 corpus/instruments/(?:anchorcheck|source-recheck|claim-package-check|density|r46-c1-gate)\.py(?: (?:[A-Za-z0-9_./~=:,+-]+|'[^'$`\\]*'))*(?: \| grep -x '[^'$`\\]*')?$")


def allowed(cmd: str) -> bool:
    """Only the line shapes the lane's 64 rechecks actually use are ever executed: `&&`-joined `test`, `set -o pipefail`,
    `git -C <dir> rev-parse HEAD` and `python3 corpus/instruments/<name>.py <plain args> [| grep -x '<literal>']` for the five instruments the lane's rechecks use
    (anchorcheck, source-recheck, claim-package-check, density, r46-c1-gate).
    Anything else is `broken` (never run), so a hostile or careless line turns L1 red instead of running."""
    segs = cmd.split(" && ")
    return all(SEG_TEST.match(x) or x == "set -o pipefail" or SEG_GIT.match(x) or SEG_PY.match(x) for x in segs)


def grader_env() -> dict:
    """Minimal environment: no tokens, agent sockets or other host secrets reach a tree-supplied line. HOME is kept (the
    lines test ~/Projects/...); BASE and TREE are read under the same one, so a host change moves both readings."""
    return {k: os.environ[k] for k in ("HOME", "PATH", "TMPDIR") if k in os.environ} | {"LANG": "C"}


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def read(path: str) -> str | None:
    try:
        with open(path, "r", encoding="utf-8", newline="") as fh:  # newline="": CRLF/CR/LF are never translated, so byte edits stay visible
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


def lines_of(text: str) -> list[str]:
    return text.split("\n")  # exact: U+2028, \r and \x0b are not line breaks here


def live_lines(text: str) -> list[str]:
    """Lines outside HTML comments and fenced code blocks (what a renderer shows as prose and tables)."""
    text = re.sub(r"(?s)<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text)
    out, fence = [], None
    for ln in lines_of(text):
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            mark = st[:3]
            fence = None if fence == mark else (fence or mark)
            out.append("")
            continue
        out.append("" if fence else ln)
    return out


def recheck_line(text: str) -> str | None:
    for ln in lines_of(text):
        m = RECHECK_RE.match(ln)
        if m:
            return m.group(1).strip()
    return None


def section_rows(text: str) -> tuple[list[list[str]] | None, str]:
    """Rows of the single `## Re-ground (round 46)` section; None when it is absent or repeated."""
    raw = [i for i, ln in enumerate(lines_of(text)) if ln.strip() == SECTION]
    lines = live_lines(text)
    starts = [i for i, ln in enumerate(lines) if ln.strip() == SECTION]
    if len(starts) != 1 or len(raw) != 1:
        return None, "section-count=live%d/raw%d" % (len(starts), len(raw))
    rows, stray = [], 0
    for ln in lines[starts[0] + 1:]:
        if re.match(r"^#{1,6} ", ln):
            break
        if not re.match(r"^\s*\|", ln):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if re.match(r"^\|\s*G\d+\s*\|", ln):
            rows.append(cells)
        elif cells and (cells[0].lower() == "id" or set(cells[0]) <= set("-: ")):
            continue  # header and separator rows
        else:
            stray += 1
    if stray:
        return None, "stray-table-rows=%d (indented, lowercase-id or non-G rows are not read, so they fail the entry)" % stray
    return rows, "rows=%d" % len(rows)


def check_row(root: str, entry_rel: str, row: list[str]) -> tuple[bool, str, str | None, tuple | None]:
    if len(row) != 4:
        return False, "cells=%d" % len(row), None, None
    m = re.fullmatch(r"`([A-Za-z0-9_./-]+):(\d+)(?:-(\d+))?`", row[2])
    t = re.fullmatch(r"`([^`]+)`", row[3])
    if not m or not t:
        return False, "anchor-or-token-not-backticked", None, None
    rel, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    tok = norm(t.group(1))
    if not rel.startswith(ANCHOR_DIRS) or ".." in rel.split("/") or rel == entry_rel or rel.endswith("r46-c1-gate.py"):
        return False, "anchor-dir-or-self", rel, None
    fp = os.path.join(root, rel)
    if os.path.islink(fp) or not os.path.isfile(fp) or not os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep):
        return False, "anchor-not-a-regular-file-in-tree", rel, None
    if len(tok) < MIN_TOKEN or sum(c.isalnum() for c in tok) < 6 or a < 1 or b < a or b - a > 39:
        return False, "token-or-range-bad", rel, None
    raw = read(fp)
    lines = lines_of(raw or "")
    if raw is None or b > len(lines) or "\r" in "".join(lines[a - 1:b]) or "\u2028" in "".join(lines[a - 1:b]):
        return False, "range-past-eof-or-unusual-line-breaks", rel, None
    window = norm(" ".join(lines[a - 1:b]))
    if tok not in window:
        return False, "token-not-in-lines", rel, None
    return True, "token-located", rel, (rel, a, b, tok)


def entry_mode(root: str, entry: str) -> int:
    rel = os.path.relpath(os.path.abspath(os.path.join(root, entry)), root) if not os.path.isabs(entry) else os.path.relpath(entry, root)
    name = os.path.basename(rel)
    text = read(os.path.join(root, rel))
    if text is None:
        print("reground entry=%s rows=0 ok=0 exit=1 read=entry-absent" % name)
        return 1
    rows, why = section_rows(text)
    if rows is None:
        print("reground entry=%s rows=0 ok=0 exit=1 read=%s" % (name, why))
        return 1
    ok, files, keys, digests = 0, set(), [], set()
    ids = [r[0] for r in rows if r]
    for r in rows:
        good, read_, f, key = check_row(root, rel, r)
        print("row %s ok=%d read=%s" % (r[0] if r else "?", int(good), read_))
        ok += int(good)
        if good and f:
            files.add(f)
            digests.add(hashlib.sha256((read(os.path.join(root, f)) or "").encode("utf-8")).hexdigest())
        if key:
            keys.append(key)
    distinct = len({(k[0], k[1], k[2]) for k in keys}) == len(keys) and len({k[3] for k in keys}) == len(keys)
    good = (bool(rows) and ok == len(rows) and len(rows) >= MIN_ROWS and len(set(ids)) == len(ids) and len(files) >= 2 and len(digests) >= 2 and distinct)
    print("reground entry=%s rows=%d ok=%d files=%d distinct=%d exit=%d" % (name, len(rows), ok, len(files), int(distinct), 0 if good else 1))
    return 0 if good else 1


def classify(root: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    kd = os.path.join(root, "corpus/knowledge")
    if not os.path.isdir(kd):
        return out
    for fn in sorted(os.listdir(kd)):
        if not fn.endswith(".md"):
            continue
        text = read(os.path.join(kd, fn)) or ""
        n = sum(1 for ln in lines_of(text) if RECHECK_RE.match(ln))
        nl = sum(1 for ln in live_lines(text) if RECHECK_RE.match(ln))
        if nl != n:
            n = 99  # a recheck line hidden in a comment or a fence: never exactly one
        line = recheck_line(text)
        if line is None:
            continue
        if subprocess.run(["bash", "-n", "-c", line], capture_output=True).returncode != 0:
            out[fn] = {"line": line, "class": "broken", "n": n}
            continue
        cmd = CD_RE.sub("", line, count=1)
        cmd = re.sub(r"[ \t]+#.*$", "", cmd)
        if not allowed(cmd):
            out[fn] = {"line": line, "class": "broken", "n": n}
            continue
        # instruments run from the grader's own lane (cwd stays the tree): a tree cannot swap in its own instrument
        cmd = cmd.replace("python3 corpus/instruments/", "python3 " + TOOL_LANE + "/corpus/instruments/")
        try:
            rc = subprocess.run(["bash", "-c", cmd], cwd=root, capture_output=True, timeout=180, env=grader_env()).returncode
        except subprocess.TimeoutExpired:
            rc = 124
        out[fn] = {"line": line, "class": "executes" if rc == 0 else "gated", "n": n}
    return out


def entry_lines(root: str, e: str) -> list[str]:
    return lines_of(read(os.path.join(root, "corpus/knowledge", e)) or "")


def gate_list(root: str, base: str, work: str):
    cb, ct = classify(base), classify(root)
    gb = {k for k, v in cb.items() if v["class"] == "gated"}
    gt = {k for k, v in ct.items() if v["class"] == "gated"}
    broken = [k for k, v in ct.items() if v["class"] == "broken"]
    reg = sorted(gb - gt)
    res = []

    ok = len(gt) <= TARGET_GATED and not broken and len(ct) >= len(cb)
    res.append(("L1", ok, "gated=%d broken=%d lines=%d/base=%d" % (len(gt), len(broken), len(ct), len(cb))))
    ok = len(reg) >= MIN_REGROUNDED and len(gt) == len(gb) - len(reg) and not (gt - gb)
    res.append(("L2", ok, "base-gated=%d regrounded=%d %s" % (len(gb), len(reg), ",".join(reg))))
    bad3 = [e for e in reg if not exact_line(e).match(ct[e]["line"]) or ct[e]["n"] != 1
            or HOME_RE.search(CD_RE.sub("", ct[e]["line"], count=1))]
    res.append(("L3", bool(reg) and not bad3, "bad=%s" % ",".join(bad3) if bad3 else "recheck-lines-exact=%d" % len(reg)))
    bad4 = []
    for e in reg:
        p = subprocess.run([sys.executable, "-I", SELF, "--entry", "corpus/knowledge/" + e, "--root", root], capture_output=True, text=True, timeout=120)
        rows, _ = section_rows("\n".join(entry_lines(root, e)))
        planted = False
        for r in rows or []:
            m = re.fullmatch(r"`([A-Za-z0-9_./-]+):\d+(?:-\d+)?`", r[2]) if len(r) == 4 else None
            if not m:
                planted = True
                continue
            bp, tp = os.path.join(base, m.group(1)), os.path.join(root, m.group(1))
            if not (os.path.isfile(bp) and os.path.isfile(tp) and read(bp) == read(tp)):
                planted = True
        if p.returncode != 0 or planted:
            bad4.append(e)
    res.append(("L4", bool(reg) and not bad4, "bad=%s" % ",".join(bad4) if bad4 else "entry-mode-green-anchors-unchanged=%d" % len(reg)))
    bad5 = []
    for e in reg:
        bl = entry_lines(base, e)
        tl = entry_lines(root, e)
        base_re = [x for x in bl if RECHECK_RE.match(x)]
        live_tl = live_lines("\n".join(tl))
        rest_ok = [x for x in tl if RESTORE_RE.match(x)]
        if [x for x in live_tl if RESTORE_RE.match(x)] != rest_ok:
            rest_ok = ["hidden-restoration-line"]
        want = "restoration-recheck: " + base_re[0][len("recheck:"):].strip() if base_re else None
        b = [x for x in bl if not RECHECK_RE.match(x)]
        t = [x for x in tl if not RECHECK_RE.match(x) and not RESTORE_RE.match(x)]
        if t[:len(b)] != b or len(t) == len(b) or len(base_re) != 1 or rest_ok != [want]:
            bad5.append(e)
    res.append(("L5", bool(reg) and not bad5, "bad=%s" % ",".join(bad5) if bad5 else "append-only-restoration-kept=%d" % len(reg)))
    # L6: each row load-bearing, in a scratch copy of corpus/, with an unmutated green control first
    survivors, mutants = [], 0
    for e in reg:
        rows, _ = section_rows("\n".join(entry_lines(root, e)))
        sc0 = tempfile.mkdtemp(prefix="r46c1c-", dir=work)
        try:
            shutil.copytree(os.path.join(root, "corpus"), os.path.join(sc0, "corpus"), symlinks=True, ignore=shutil.ignore_patterns("lessons", "__pycache__"))
            c = subprocess.run([sys.executable, "-I", SELF, "--entry", "corpus/knowledge/" + e, "--root", sc0], capture_output=True, text=True, timeout=120)
            if c.returncode != 0:
                survivors.append("%s:unmutated-copy-not-green" % e)
                continue
        finally:
            shutil.rmtree(sc0, ignore_errors=True)
        for r in rows or []:
            m = re.fullmatch(r"`([A-Za-z0-9_./-]+):(\d+)(?:-(\d+))?`", r[2]) if len(r) == 4 else None
            t = re.fullmatch(r"`([^`]+)`", r[3]) if len(r) == 4 else None
            if not m or not t:
                survivors.append("%s:%s:unparsed" % (e, r[0] if r else "?"))
                continue
            sc = tempfile.mkdtemp(prefix="r46c1-", dir=work)
            try:
                shutil.copytree(os.path.join(root, "corpus"), os.path.join(sc, "corpus"), symlinks=True, ignore=shutil.ignore_patterns("lessons", "__pycache__"))
                fp = os.path.join(sc, m.group(1))
                ls = open(fp, "r", encoding="utf-8").read().split("\n")
                a, b = int(m.group(2)), int(m.group(3) or m.group(2))
                tok = t.group(1)
                hit = [i for i in range(a - 1, min(b, len(ls))) if tok in ls[i]]
                if hit:
                    for i in hit:
                        ls[i] = ls[i].replace(tok, "#" * len(tok))
                else:  # the token only matches after whitespace normalisation (it spans lines): blank the whole range
                    for i in range(a - 1, min(b, len(ls))):
                        ls[i] = "#" * len(ls[i])
                open(fp, "w", encoding="utf-8").write("\n".join(ls))
                mutants += 1
                p = subprocess.run([sys.executable, "-I", SELF, "--entry", "corpus/knowledge/" + e, "--root", sc], capture_output=True, text=True, timeout=120)
                red = [ln.split()[1] for ln in p.stdout.splitlines() if ln.startswith("row ") and " ok=0 " in ln]
                if p.returncode == 0 or red != [r[0]]:
                    survivors.append("%s:%s" % (e, r[0]))
            finally:
                shutil.rmtree(sc, ignore_errors=True)
    res.append(("L6", bool(reg) and mutants >= MIN_ROWS * len(reg) and not survivors,
                "mutants=%d survivors=%s" % (mutants, ",".join(survivors) or "none")))
    still = sorted(gb & gt)
    bad7 = [e for e in still if (read(os.path.join(base, "corpus/knowledge", e)) or "") != (read(os.path.join(root, "corpus/knowledge", e)) or "")]
    res.append(("L7", not bad7, "still-gated=%d changed=%s" % (len(still), ",".join(bad7) or "none")))
    return res, len(gt)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--entry")
    ap.add_argument("--root", default=".")
    ap.add_argument("--baseline")
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("r46-c1-gate: %s is not a directory" % a.root, file=sys.stderr)
        return 2
    if a.entry:
        return entry_mode(root, a.entry)
    if not a.baseline or not os.path.isdir(a.baseline):
        print("r46-c1-gate: aggregate mode needs --baseline <dir>", file=sys.stderr)
        return 2
    work = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    os.makedirs(work, exist_ok=True)
    fixed, gt = 0, -1
    try:
        res, gt = gate_list(root, os.path.abspath(a.baseline), work)
    except Exception as exc:  # fail closed, say why
        res = [("L%d" % i, False, "exception-%s" % type(exc).__name__) for i in range(1, 8)]
    for gid, ok, rd in res:
        fixed += int(ok)
        print("gate %s pass=%d read=%s" % (gid, int(ok), rd))
    code = 0 if fixed == 7 else 1
    print("c1-gate fixed=%d/7 exit=%d" % (fixed, code))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
