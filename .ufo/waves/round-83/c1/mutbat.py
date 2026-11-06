#!/usr/bin/env python3
"""mutbat.py — round-83 C1 mutant battery for corpus/instruments/recheck-cwd-census.py.

Round 83 (successor of the round-82 counter, .ufo/waves/round-82/c1/mutbat.py; every round-82
limb kept) closes three forgery classes the round-82 limbs accept:

  constant run dirs  every mutant and decoy runs from a directory named 'mutbat-t-<random>',
                     so a target cannot read its row id from its path (round-82 CriticClaims
                     F1, M82-2).
  keyed decoys       D1 and D2 each end with a module-level assignment of a per-run nonce
                     (os.urandom, or --seed), so a target cannot whitelist decoy hashes
                     (round-82 ReviewC1 Major 1).
  D3 single decoy    the original bytes with one trailing comment '# mutbat-<nonce>' at the
                     end of the first line of one nonce-chosen non-neutral row's anchor (a
                     line ending outside every string, not a continuation). It hides that one
                     anchor, as a mutant does, without changing behaviour, so a target that
                     passes whenever many anchors are missing breaks D3.
  extra sites        a row may carry "extra": [[anchor, replacement], ...] applied after the
                     primary site; each must occur exactly once, else NOT-DERIVED.

A 'DECOY keyed=<yes|no> nonce=<hex> d3_row=<id>' line precedes the MUTBAT line. Known limit
(unchanged): a target that compares its own AST (or comment-stripped tokens) against an
embedded original and fails only on a known mutant passes every decoy.

Round 82 text follows.

Successor of the round-80 counter (QUALITY R129 classifier kept: an exception FAIL is a FAIL
whose detail BEGINS with 'exception='). Round 81 makes the kill tally a limb that does not
lean on the candidate's byte pin (round-80 CriticClaims (a): location, self-hash, sibling and
baseline-limb forgeries reached killed=28/28 under the round-80 counter). Three limbs:

  case-matched kill  every non-neutral row declares `kill_cases`, the selftest case ids its
                     transform is meant to break; a row counts as killed only when a FAIL line
                     names one of them. A FAIL on any other case id (an integrity or location
                     guard, an unrelated check) scores MISKILLED, not killed.
  clean baseline     the unmutated target must exit 0, print the exact line
                     'selftest cases=<expect> failures=0', print no 'selftest case=... FAIL'
                     line and no 'Traceback'.
  neutral rows       rows of class "neutral" apply a semantics-preserving transform (a comment,
                     a local rename) and run, like every mutant, from a copy in a fresh
                     directory; each must pass exactly as the baseline does (NEUTRAL-OK). A
                     target that fails when moved, when its bytes change or when a sibling is
                     absent breaks its neutral rows (NEUTRAL-BROKEN).

  decoy (round 82)   the counter, not the table, builds two semantics-preserving rewrites of
                     the whole target and runs each from a fresh directory; each must pass
                     exactly as the baseline does, else decoy=broken.
                       D1 unparse  ast.unparse(ast.parse(target)): drops comments and
                                   redundant parentheses, normalizes spacing and quotes.
                       D2 rename   D1 after a consistent rename (suffix `_d`) of every
                                   function-local identifier (parameters, assigned names,
                                   except-as names) that is not bound at module level, not
                                   used as a call keyword, not a builtin and not declared
                                   global/nonlocal.
                     Many row anchors vanish from the decoys while behaviour does not change,
                     so a target whose FAIL lines key on its own source text (round-81
                     CriticClaims (a): a table-reading forgery that fails a row's kill_cases
                     when that row's anchor is missing from its own source, also after
                     whitespace/quote/parenthesis normalization) breaks a decoy.
                     decoy_hidden=<h>/<n> counts the non-neutral rows whose anchor is absent
                     from at least one decoy; the limb needs h >= 1. Known limit: a forgery
                     that compares its own AST against an embedded original and fails only on
                     an AST equal to a known mutant passes both decoys.

Table rows: {"id", "anchor", "replacement", "class": "assertion"|"exception"|"neutral",
"kill_cases": [...] (non-neutral rows), "expect": prose}. The anchor must occur exactly once in
the target, else NOT-DERIVED. Verdicts for non-neutral rows:

  KILLED          exit != 0, no 'Traceback', a FAIL line on a kill case whose detail does not
                  begin with 'exception='
  EXCEPTION-KILL  exit != 0, no 'Traceback', every FAIL line on a kill case begins
                  'exception=' (counts as killed only for rows whose class is "exception")
  MISKILLED       exit != 0, no 'Traceback', FAIL lines present but none on a kill case
  SURVIVED        exit 0
  DIRTY           exit != 0 without a FAIL line, or with a 'Traceback'

Output: one 'MUTANT <id> verdict=<v> rc=<n> fails=<k> failed_cases=<a,b> counted=<yes|no>'
line per row, then 'MUTBAT target_sha256=<h> baseline=<ok|bad> rows=<n> killed=<k>
survived=<s> miskilled=<m> dirty=<d> notderived=<x> neutral_ok=<o>/<t> decoy=<ok|broken>
decoy_hidden=<h>/<n>'. Exit 0 iff the baseline is ok, every non-neutral row counts as
killed, every neutral row is NEUTRAL-OK, the decoy is ok with h >= 1, and the table has at
least one row of each kind; exit 1 otherwise; exit 2 on a usage, table or read error.

Usage:
  python3 mutbat.py --target FILE --table TABLE.json --expect-cases N --work DIR [--keep DIR]
  python3 mutbat.py --selftest --work DIR
"""
import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FAIL_LINE_RE = re.compile(r"^selftest case=(\S+) FAIL(?: (.*))?$", re.M)


def run_selftest(path, work):
    tmp = tempfile.mkdtemp(prefix="mutbat-run-", dir=work)
    try:
        env = dict(os.environ)
        env["TMPDIR"] = tmp
        proc = subprocess.run([sys.executable, "-B", path, "--selftest"], env=env,
                              stdin=subprocess.DEVNULL, capture_output=True, text=True,
                              timeout=900)
        return proc.returncode, proc.stdout + proc.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def fail_lines(out):
    """[(case, is_exception_detail)] for every 'selftest case=<id> FAIL' line."""
    return [(m.group(1), (m.group(2) or "").startswith("exception="))
            for m in FAIL_LINE_RE.finditer(out)]


def clean_pass(rc, out, expect_cases):
    exact = re.search(r"^selftest cases=%d failures=0$" % expect_cases, out, re.M) is not None
    return rc == 0 and exact and not fail_lines(out) and "Traceback" not in out


def verdict(rc, out, kill_cases):
    fails = fail_lines(out)
    if rc == 0:
        return "SURVIVED", fails
    if "Traceback" in out or not fails:
        return "DIRTY", fails
    on_target = [exc for case, exc in fails if case in kill_cases]
    if not on_target:
        return "MISKILLED", fails
    if all(on_target):
        return "EXCEPTION-KILL", fails
    return "KILLED", fails


def validate_rows(rows):
    """None when the table is well formed, else a one-line reason."""
    if not isinstance(rows, list) or not rows:
        return "table is not a non-empty list"
    ids = set()
    for row in rows:
        if not isinstance(row, dict):
            return "row is not an object"
        for key in ("id", "anchor", "replacement", "class"):
            if not isinstance(row.get(key), str):
                return "row %r lacks string %s" % (row.get("id"), key)
        if row["id"] in ids:
            return "duplicate row id %s" % row["id"]
        ids.add(row["id"])
        if row["class"] not in ("assertion", "exception", "neutral"):
            return "row %s has class %r" % (row["id"], row["class"])
        if row["class"] != "neutral":
            kc = row.get("kill_cases")
            if not (isinstance(kc, list) and kc and all(isinstance(c, str) and c for c in kc)):
                return "row %s lacks kill_cases" % row["id"]
        extra = row.get("extra", [])
        if not (isinstance(extra, list) and all(
                isinstance(p, list) and len(p) == 2 and all(isinstance(s, str) and s for s in p)
                for p in extra)):
            return "row %s has a malformed extra" % row["id"]
    return None


def rename_locals(tree):
    """D2: rename function-local identifiers in place (see the module docstring)."""
    import builtins
    module_names = set()
    for node in tree.body:
        for sub in ast.walk(node) if not isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else [node]:
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                module_names.add(sub.name)
            elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                module_names.add(sub.id)
            elif isinstance(sub, ast.alias):
                module_names.add((sub.asname or sub.name).split(".")[0])
    keywords = {kw.arg for n in ast.walk(tree) if isinstance(n, ast.Call)
                for kw in n.keywords if kw.arg}
    declared = {name for n in ast.walk(tree) if isinstance(n, (ast.Global, ast.Nonlocal))
                for name in n.names}
    local = set()
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = fn.args
            for arg in a.posonlyargs + a.args + a.kwonlyargs + [a.vararg, a.kwarg]:
                if arg is not None:
                    local.add(arg.arg)
            for sub in ast.walk(fn):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    local.add(sub.id)
                elif isinstance(sub, ast.ExceptHandler) and sub.name:
                    local.add(sub.name)
    rename = local - module_names - keywords - declared - set(dir(builtins)) - {"__file__"}
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id in rename:
            n.id += "_d"
        elif isinstance(n, ast.arg) and n.arg in rename:
            n.arg += "_d"
        elif isinstance(n, ast.ExceptHandler) and n.name in rename:
            n.name += "_d"
    return tree


def comment_lines(src):
    """1-based line numbers where a trailing comment can be added without changing the
    program: the line ends outside every string token and is not a backslash continuation."""
    import io
    import tokenize
    lines = src.split("\n")
    inside = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.STRING or getattr(tokenize, "FSTRING_MIDDLE", -1) == tok.type:
                inside.update(range(tok.start[0], tok.end[0]))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return set()
    return {n for n in range(1, len(lines) + 1)
            if n not in inside and lines[n - 1].strip() and not lines[n - 1].endswith("\\")}


def single_decoy(src, rows, nonce):
    """D3 (round 83): the original bytes with one trailing comment carrying the nonce, added
    at the end of the first line of one keyed-random eligible non-neutral row's anchor. That
    row's anchor (and only anchors spanning that line end) vanishes; behaviour is unchanged.
    Returns (row id, source) or (None, None) when no row is eligible."""
    ok_lines = comment_lines(src)
    cands = []
    for r in rows:
        if r["class"] == "neutral" or src.count(r["anchor"]) != 1 or "\n" not in r["anchor"]:
            continue
        pos = src.index(r["anchor"]) + r["anchor"].index("\n")
        if src.count("\n", 0, pos) + 1 in ok_lines:
            cands.append((r["id"], pos))
    if not cands:
        return None, None
    rid, pos = cands[int(nonce, 16) % len(cands)]
    return rid, src[:pos] + "  # mutbat-%s" % nonce + src[pos:]


def run_decoy(src, target, expect_cases, work, rows=(), nonce=None):
    """(ok, [decoy sources], d3 row id): D1 and D2, each keyed with a module-level nonce
    assignment when nonce is given (round 83), plus D3 when nonce is given; each runs from
    a fresh directory with a constant prefix. nonce None is the round-82 limb."""
    try:
        d1 = ast.unparse(ast.parse(src)) + "\n"
        d2 = ast.unparse(rename_locals(ast.parse(src))) + "\n"
    except (SyntaxError, ValueError, RecursionError):
        return False, None, None
    decoys = [d1, d2]
    d3_id = None
    if nonce is not None:
        decoys = [d + "_mutbat_k = %r\n" % nonce for d in decoys]
        d3_id, d3 = single_decoy(src, rows, nonce)
        if d3 is None:
            return False, decoys, None
        decoys.append(d3)
    ok = True
    for decoy in decoys:
        ddir = tempfile.mkdtemp(prefix="mutbat-t-" if nonce is not None else "mutbat-decoy-",
                                dir=work)
        try:
            dpath = os.path.join(ddir, os.path.basename(target))
            with open(dpath, "w", encoding="utf-8") as fh:
                fh.write(decoy)
            rc, out = run_selftest(dpath, work)
        finally:
            shutil.rmtree(ddir, ignore_errors=True)
        ok = ok and clean_pass(rc, out, expect_cases)
    return ok, decoys, d3_id


def apply_row(src, row):
    """The mutant source, or None when an anchor (primary or extra) is not unique."""
    if src.count(row["anchor"]) != 1:
        return None
    out = src.replace(row["anchor"], row["replacement"], 1)
    for anchor, repl in row.get("extra", []):
        if out.count(anchor) != 1:
            return None
        out = out.replace(anchor, repl, 1)
    return out


def battery(target, rows, expect_cases, work, keep=None, nonce=None, legacy=False):
    """legacy=True runs the round-82 limbs (row-id run-directory prefixes, unkeyed D1/D2, no
    D3); the selftest uses it to show each round-83 forgery passing the old limbs."""
    with open(target, encoding="utf-8") as fh:
        src = fh.read()
    sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    rc0, out0 = run_selftest(target, work)
    baseline = clean_pass(rc0, out0, expect_cases)
    if not legacy and nonce is None:
        nonce = os.urandom(8).hex()
    decoy_ok, decoy_src, d3_id = run_decoy(src, target, expect_cases, work, rows,
                                           None if legacy else nonce)
    hidden = sum(1 for r in rows if r["class"] != "neutral"
                 and (decoy_src is None or any(d.count(r["anchor"]) == 0 for d in decoy_src[:2])))
    tally = {"killed": 0, "survived": 0, "miskilled": 0, "dirty": 0, "notderived": 0,
             "neutral_ok": 0}
    n_neutral = sum(1 for r in rows if r["class"] == "neutral")
    lines = []
    for row in rows:
        mutant = apply_row(src, row)
        if mutant is None:
            tally["notderived"] += 1
            lines.append("MUTANT %s verdict=NOT-DERIVED occurrences=%d counted=no"
                         % (row["id"], src.count(row["anchor"])))
            continue
        mdir = tempfile.mkdtemp(prefix=("mutbat-%s-" % row["id"]) if legacy else "mutbat-t-",
                                dir=work)
        mpath = os.path.join(mdir, os.path.basename(target))
        with open(mpath, "w", encoding="utf-8") as fh:
            fh.write(mutant)
        rc, out = run_selftest(mpath, work)
        if keep:
            os.makedirs(keep, exist_ok=True)
            with open(os.path.join(keep, "%s.out" % row["id"]), "w", encoding="utf-8") as fh:
                fh.write("rc=%d\n%s" % (rc, out))
        shutil.rmtree(mdir, ignore_errors=True)
        failed = ",".join(sorted({case for case, _exc in fail_lines(out)})) or "-"
        if row["class"] == "neutral":
            ok_n = clean_pass(rc, out, expect_cases)
            if ok_n:
                tally["neutral_ok"] += 1
            lines.append("MUTANT %s verdict=%s rc=%d fails=%d failed_cases=%s counted=%s"
                         % (row["id"], "NEUTRAL-OK" if ok_n else "NEUTRAL-BROKEN", rc,
                            len(fail_lines(out)), failed, "yes" if ok_n else "no"))
            continue
        v, fails = verdict(rc, out, row["kill_cases"])
        counts = v == "KILLED" or (v == "EXCEPTION-KILL" and row["class"] == "exception")
        if counts:
            tally["killed"] += 1
        elif v == "SURVIVED":
            tally["survived"] += 1
        elif v == "MISKILLED":
            tally["miskilled"] += 1
        else:
            tally["dirty"] += 1
        lines.append("MUTANT %s verdict=%s rc=%d fails=%d failed_cases=%s counted=%s"
                     % (row["id"], v, rc, len(fails), failed, "yes" if counts else "no"))
    n_kill = len(rows) - n_neutral
    lines.append("DECOY keyed=%s nonce=%s d3_row=%s"
                 % ("no" if legacy else "yes", nonce or "-", d3_id or "-"))
    lines.append("MUTBAT target_sha256=%s baseline=%s rows=%d killed=%d survived=%d miskilled=%d "
                 "dirty=%d notderived=%d neutral_ok=%d/%d decoy=%s decoy_hidden=%d/%d"
                 % (sha, "ok" if baseline else "bad", len(rows), tally["killed"],
                    tally["survived"], tally["miskilled"], tally["dirty"], tally["notderived"],
                    tally["neutral_ok"], n_neutral, "ok" if decoy_ok else "broken", hidden,
                    n_kill))
    ok = (baseline and n_kill > 0 and n_neutral > 0 and tally["killed"] == n_kill
          and tally["neutral_ok"] == n_neutral and decoy_ok and hidden >= 1)
    return ok, lines


TOY = '''import sys
def tested(x):
    return (x > 0)
def other(x):
    return x * 2
def untested(x):
    return x < 0
def selftest():
    rows = []
    try:
        ok = tested(1) is True and tested(-1) is False
        detail = "note=exception-free ret=%r" % (tested(1),)
    except Exception as exc:
        ok, detail = False, "exception=%r" % (exc,)
    rows.append(("a", ok, detail))
    rows.append(("b", other(2) == 4, "got=%r" % (other(2),)))
    fails = 0
    for case, ok_, det in rows:
        print("selftest case=%s %s %s" % (case, "ok" if ok_ else "FAIL", det))
        fails += 0 if ok_ else 1
    print("selftest cases=%d failures=%d" % (len(rows), fails))
    return 0 if fails == 0 else 1
if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
'''

# A location-guard forgery of TOY (round-80 CriticClaims F1 shape): no assertion runs; it
# passes in its home directory and prints an integrity FAIL anywhere else.
FORGERY_LOCATION = TOY.replace(
    "def selftest():\n",
    "def selftest():\n"
    "    import os\n"
    "    home = os.path.basename(os.path.dirname(os.path.abspath(__file__))) == 'home'\n"
    "    print('selftest case=a ok stub')\n"
    "    print('selftest case=b ok stub')\n"
    "    if not home:\n"
    "        print('selftest case=integrity FAIL moved')\n"
    "    print('selftest cases=2 failures=%d' % (0 if home else 1))\n"
    "    return 0 if home else 1\n"
    "def unused_selftest():\n", 1)

# A baseline-limb forgery (round-80 CriticClaims F4 shape): red on its own pristine bytes yet
# exit 0 with the expected summary line.
FORGERY_BASELINE = TOY.replace(
    "    fails = 0\n",
    "    print('selftest case=integrity FAIL always')\n    fails = 0\n", 1)

# A table-reading self-diff forgery (round-81 CriticClaims (a) shape, w1/CriticClaims-receipts/
# forgery-selfdiff.py): no assertion runs; it prints FAIL on a case whenever that case's row
# anchor is missing from its own source. The case-matched tally and the neutral rows accept
# it; the round-82 decoy (the anchor vanishes under ast.unparse) breaks it.
FORGERY_SELFDIFF = """import sys
ANCHORS = {"a": ["    return (x > 0)\\n"]}
def tested(x):
    return (x > 0)
def untested(x):
    return x < 0
def selftest():
    with open(__file__, encoding="utf-8") as fh:
        src = fh.read()
    fails = 0
    for case in ("a", "b"):
        missing = [t for t in ANCHORS.get(case, []) if t not in src]
        print("selftest case=%s %s" % (case, "FAIL not-asserted" if missing else "ok stub"))
        fails += 1 if missing else 0
    print("selftest cases=2 failures=%d" % fails)
    return 1 if fails else 0
if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
"""

# Round-83 forgeries, each accepted by the round-82 limbs (legacy=True) and rejected by the
# round-83 limbs. A path-label forgery (round-82 CriticClaims F1, w1/CriticClaims-receipts/
# forgery-path-table.py): it reads the row id from its run directory name.
FORGERY_PATH = FORGERY_SELFDIFF.replace(
    "        missing = [t for t in ANCHORS.get(case, []) if t not in src]\n",
    "        import os\n"
    "        run = os.path.basename(os.path.dirname(os.path.abspath(__file__)))\n"
    "        missing = case == 'a' and run.startswith(('mutbat-T-KILL-', 'mutbat-T-EXC-'))\n", 1)

# A missing-anchor-count forgery: two anchors, both hidden by D1/D2; it passes clean when two
# or more anchors are missing (a decoy) and fails the case of a single missing anchor (a
# mutant). The round-83 D3 decoy hides exactly one anchor.
FORGERY_COUNT = """import sys
ANCHORS = {"a": "    return (x > 0)\\n", "b": "    return (x * 2)\\n"}
def tested(x):
    return (x > 0)
def other(x):
    return (x * 2)
def untested(x):
    return x < 0
def selftest():
    with open(__file__, encoding="utf-8") as fh:
        src = fh.read()
    missing = [c for c, t in sorted(ANCHORS.items()) if t not in src]
    if len(missing) >= 2:
        missing = []
    for case in ("a", "b"):
        print("selftest case=%s %s" % (case, "FAIL not-asserted" if case in missing else "ok stub"))
    print("selftest cases=2 failures=%d" % len(missing))
    return 1 if missing else 0
if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
"""

# A hash-whitelisting forgery (round-82 ReviewC1 Major 1): FORGERY_SELFDIFF plus a whitelist
# of the sha256 of its own unkeyed D1/D2 decoys (the WL line removed before hashing); a
# whitelisted source passes clean. Keyed decoys carry a per-run nonce, so no hash matches.
FORGERY_HASHWL_BASE = FORGERY_SELFDIFF.replace(
    "    fails = 0\n",
    "    import hashlib, re\n"
    "    core = re.sub(r'(?m)^WL = .*\\n', '', src)\n"
    "    if hashlib.sha256(core.encode('utf-8')).hexdigest() in WL:\n"
    "        src = ''.join(sum(ANCHORS.values(), []))\n"
    "    fails = 0\n", 1)


def forgery_hashwl():
    base = FORGERY_HASHWL_BASE
    wl = {hashlib.sha256((ast.unparse(t) + "\n").encode("utf-8")).hexdigest()
          for t in (ast.parse(base), rename_locals(ast.parse(base)))}
    return base.replace("import sys\n", "import sys\nWL = %r\n" % (sorted(wl),), 1)


def selftest(work):
    d = tempfile.mkdtemp(prefix="mutbat-selftest-", dir=work)
    try:
        home = os.path.join(d, "home")
        os.makedirs(home)
        toy = os.path.join(home, "toy.py")
        with open(toy, "w", encoding="utf-8") as fh:
            fh.write(TOY)
        rows = [
            {"id": "T-KILL", "anchor": "    return (x > 0)\n", "replacement": "    return True\n",
             "class": "assertion", "kill_cases": ["a"]},
            {"id": "T-MIS", "anchor": "    return x * 2\n", "replacement": "    return x * 3\n",
             "class": "assertion", "kill_cases": ["a"]},
            {"id": "T-SURV", "anchor": "    return x < 0\n", "replacement": "    return True\n",
             "class": "assertion", "kill_cases": ["a"]},
            {"id": "T-ABSENT", "anchor": "no such text", "replacement": "", "class": "assertion",
             "kill_cases": ["a"]},
            {"id": "T-EXC", "anchor": "    return (x > 0)\n",
             "replacement": "    raise ValueError('boom')\n", "class": "exception",
             "kill_cases": ["a"]},
            {"id": "T-EXCA", "anchor": "    return (x > 0)\n",
             "replacement": "    raise ValueError('boom')\n", "class": "assertion",
             "kill_cases": ["a"]},
            {"id": "T-NEU", "anchor": "def untested(x):\n",
             "replacement": "# neutral comment\ndef untested(x):\n", "class": "neutral"},
            {"id": "T-NEUBAD", "anchor": "    return x * 2\n", "replacement": "    return x * 3\n",
             "class": "neutral"},
        ]
        ok, lines = battery(toy, rows, 2, d)
        want = {"T-KILL": "KILLED", "T-MIS": "MISKILLED", "T-SURV": "SURVIVED",
                "T-ABSENT": "NOT-DERIVED", "T-EXC": "EXCEPTION-KILL", "T-EXCA": "EXCEPTION-KILL",
                "T-NEU": "NEUTRAL-OK", "T-NEUBAD": "NEUTRAL-BROKEN"}
        got = {ln.split()[1]: ln.split()[2].split("=")[1] for ln in lines if ln.startswith("MUTANT")}
        counted = {ln.split()[1]: ln.rsplit("counted=", 1)[1] for ln in lines
                   if ln.startswith("MUTANT")}
        want_counted = {"T-KILL": "yes", "T-MIS": "no", "T-SURV": "no", "T-ABSENT": "no",
                        "T-EXC": "yes", "T-EXCA": "no", "T-NEU": "yes", "T-NEUBAD": "no"}
        good = [rows[0], rows[4], rows[6]]
        ok_good, _l = battery(toy, good, 2, d)
        with open(toy, "w", encoding="utf-8") as fh:
            fh.write(FORGERY_LOCATION)
        ok_loc, lines_loc = battery(toy, good, 2, d)
        with open(toy, "w", encoding="utf-8") as fh:
            fh.write(FORGERY_BASELINE)
        ok_base, lines_base = battery(toy, good, 2, d)
        with open(toy, "w", encoding="utf-8") as fh:
            fh.write(FORGERY_SELFDIFF)
        ok_sd, lines_sd = battery(toy, good, 2, d)
        # Round 83: each new forgery passes the round-82 limbs and fails the round-83 limbs.
        good2 = [{"id": "T2-A", "anchor": "    return (x > 0)\n", "replacement": "    return True\n",
                  "class": "assertion", "kill_cases": ["a"]},
                 {"id": "T2-B", "anchor": "    return (x * 2)\n", "replacement": "    return x * 3\n",
                  "class": "assertion", "kill_cases": ["b"]},
                 rows[6]]
        r83 = {}
        for name, text, table in (("path", FORGERY_PATH, good), ("count", FORGERY_COUNT, good2),
                                  ("hashwl", forgery_hashwl(), good)):
            with open(toy, "w", encoding="utf-8") as fh:
                fh.write(text)
            r83[name] = (battery(toy, table, 2, d, legacy=True),
                         battery(toy, table, 2, d, nonce="00000000000000a1"))
        r83_ok = all(old[0] and "baseline=ok" in old[1][-1] and not new[0]
                     for old, new in r83.values())
        r83_ok = (r83_ok and "killed=0" in r83["path"][1][1][-1]
                  and "decoy=broken" in r83["count"][1][1][-1]
                  and "decoy=broken" in r83["hashwl"][1][1][-1])
        bad_tables = [validate_rows([{"id": "x", "anchor": "a", "replacement": "b",
                                      "class": "assertion"}]),
                      validate_rows([{"id": "x", "anchor": "a", "replacement": "b",
                                      "class": "bogus", "kill_cases": ["a"]}]),
                      validate_rows([rows[0], rows[0]]),
                      validate_rows([dict(rows[0], extra=[["a"]])])]
        okk = ((not ok) and got == want and counted == want_counted
               and "baseline=ok" in lines[-1] and ok_good
               and (not ok_loc) and "baseline=ok" in lines_loc[-1]
               and "killed=0" in lines_loc[-1] and "miskilled=2" in lines_loc[-1]
               and "neutral_ok=0/1" in lines_loc[-1]
               and (not ok_base) and "baseline=bad" in lines_base[-1]
               and "decoy=ok decoy_hidden=2/2" in _l[-1]
               and (not ok_sd) and "baseline=ok" in lines_sd[-1] and "killed=2" in lines_sd[-1]
               and "neutral_ok=1/1" in lines_sd[-1] and "decoy=broken" in lines_sd[-1]
               and r83_ok
               and all(r is not None for r in bad_tables) and validate_rows(rows) is None)
        print("mutbat selftest %s got=%s counted=%s all_killed_exit=%s location_forgery_exit=%s "
              "baseline_forgery_exit=%s selfdiff_forgery_exit=%s r83_forgeries=%s bad_tables=%s"
              % ("ok" if okk else "FAIL", got, counted, ok_good, ok_loc, ok_base, ok_sd,
                 {k: (o[0], n[0]) for k, (o, n) in sorted(r83.items())},
                 [r is not None for r in bad_tables]))
        return 0 if okk else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target")
    ap.add_argument("--table")
    ap.add_argument("--expect-cases", type=int)
    ap.add_argument("--work", required=True)
    ap.add_argument("--keep")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", help="hex nonce for the keyed decoys (default: os.urandom)")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.work):
        print("mutbat: --work %s is not a directory" % a.work, file=sys.stderr)
        return 2
    if a.selftest:
        return selftest(a.work)
    if not (a.target and a.table and a.expect_cases is not None):
        print("mutbat: --target, --table and --expect-cases are required", file=sys.stderr)
        return 2
    try:
        with open(a.table, encoding="utf-8") as fh:
            rows = json.load(fh)
    except (OSError, ValueError) as exc:
        print("mutbat: cannot read table: %s" % exc, file=sys.stderr)
        return 2
    bad = validate_rows(rows)
    if bad is not None:
        print("mutbat: bad table: %s" % bad, file=sys.stderr)
        return 2
    try:
        if a.seed is not None and not re.fullmatch(r"[0-9a-f]{1,64}", a.seed):
            print("mutbat: --seed must be lowercase hex", file=sys.stderr)
            return 2
        ok, lines = battery(a.target, rows, a.expect_cases, a.work, a.keep, nonce=a.seed)
    except OSError as exc:
        print("mutbat: cannot read target: %s" % exc, file=sys.stderr)
        return 2
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
