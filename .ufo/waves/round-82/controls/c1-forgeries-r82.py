#!/usr/bin/env python3
"""c1-forgeries-r82.py — pre-freeze forgery controls for round-82 C1.

Builds three table-reading forgeries of the frozen r82 candidate. Each keeps the candidate's
bytes (so every row anchor occurs exactly once) and appends a block (it begins at the line
'_FG_TABLE = ', and every forgery reads only its own source before that line) that hijacks --selftest
before main(): no assertion of the candidate runs. The block embeds the frozen r82 table
(zlib+base64, so no anchor is duplicated in clear text) and prints
'selftest case=<k> FAIL not-asserted' for the kill_cases of the rows it believes applied,
then 'selftest cases=24 failures=<n>'.

  F6-selfdiff   round-81 CriticClaims (a) shape (w1/CriticClaims-receipts/forgery-selfdiff.py),
                strengthened: a row applied when the own-source count of its anchor or of its
                replacement differs from the count in the candidate (embedded _FG_BASE), so an
                insertion row whose replacement keeps the anchor (J1) is caught too.
  F7-wsnorm     F6 read through a normalization chosen per row: the first of (all whitespace
                and parentheses removed with single quotes read as double; quotes only; raw)
                under which the row's anchor and replacement differ (level and counts
                embedded). It survives the D1 unparse decoy's spacing/quote/paren changes.
  F8-astembed   embeds the original source too: passes when ast.dump(own) equals the
                original's; otherwise a row applied when ast.dump of the original with that
                row's replacement equals ast.dump(own). Declared in advance as the decoy
                limb's known limit (the decoy is AST-identical to the original).

Each forgery is scored under (a) the round-81 counter and (b) the round-82 counter, both over
the full 63-row r82 table with --expect-cases 24. Prints one FORGERY line per run.
Usage: c1-forgeries-r82.py --lane DIR --work DIR
"""
import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zlib

C1 = ".ufo/waves/round-82/c1"
MAIN_GUARD = 'if __name__ == "__main__":\n    sys.exit(main(sys.argv))\n'

COMMON = r'''
def _fg_rows():
    import base64 as _b, json as _j, zlib as _z
    return _j.loads(_z.decompress(_b.b64decode(_FG_TABLE)).decode("utf-8"))


def _fg_report(hit):
    for _c in sorted(set(hit)):
        print("selftest case=%s FAIL not-asserted" % _c)
    print("selftest cases=24 failures=%d" % (1 if hit else 0))
    return 1 if hit else 0


def _fg_norm(_s):
    import re as _re
    return _re.sub(r"[\s()]+", "", _s).replace("'", '"')


def _fg_own():
    with open(os.path.abspath(__file__), encoding="utf-8") as _fh:
        return _fh.read().split("\n_FG_TABLE = ", 1)[0]


def _fg_cnt(_t, _x):
    return _t.count(_x) if _x else 0
'''

BODY = {
    "F6-selfdiff": r'''
def _fg_selftest():
    _src = _fg_own()
    _hit = []
    for _r in _fg_rows():
        if _r["class"] == "neutral":
            continue
        _ba, _br = _FG_BASE[_r["id"]]
        if _fg_cnt(_src, _r["anchor"]) != _ba or _fg_cnt(_src, _r["replacement"]) != _br:
            _hit.extend(_r["kill_cases"])
    return _fg_report(_hit)
''',
    "F7-wsnorm": r'''
def _fg_selftest():
    _own = _fg_own()
    _views = [_fg_norm(_own), _own.replace("'", '"'), _own]
    _fs = [_fg_norm, lambda _x: _x.replace("'", '"'), lambda _x: _x]
    _hit = []
    for _r in _fg_rows():
        if _r["class"] == "neutral":
            continue
        _lv, _ba, _br = _FG_BASE[_r["id"]]
        _f, _src = _fs[_lv], _views[_lv]
        if (_fg_cnt(_src, _f(_r["anchor"])) != _ba
                or _fg_cnt(_src, _f(_r["replacement"])) != _br):
            _hit.extend(_r["kill_cases"])
    return _fg_report(_hit)
''',
    "F8-astembed": r'''
def _fg_selftest():
    import ast as _a, base64 as _b, zlib as _z
    _orig = _z.decompress(_b.b64decode(_FG_ORIG)).decode("utf-8")
    with open(os.path.abspath(__file__), encoding="utf-8") as _fh:
        _own = _a.dump(_a.parse(_fh.read().split("\n_FG_TABLE = ", 1)[0]))
    if _own == _a.dump(_a.parse(_orig)):
        return _fg_report([])
    _hit = []
    for _r in _fg_rows():
        if _r["class"] == "neutral" or _orig.count(_r["anchor"]) != 1:
            continue
        try:
            _m = _a.dump(_a.parse(_orig.replace(_r["anchor"], _r["replacement"], 1)))
        except SyntaxError:
            continue
        if _m == _own:
            _hit.extend(_r["kill_cases"])
    return _fg_report(_hit)
''',
}


def norm(s):
    return re.sub(r"[\s()]+", "", s).replace("'", '"')


def base_counts(src, rows, name):
    if name != "F7-wsnorm":
        c = lambda x: src.count(x) if x else 0
        return {r["id"]: [c(r["anchor"]), c(r["replacement"])]
                for r in rows if r["class"] != "neutral"}
    fs = [norm, lambda x: x.replace("'", '"'), lambda x: x]
    out = {}
    for r in rows:
        if r["class"] == "neutral":
            continue
        lv = next(i for i, f in enumerate(fs) if f(r["anchor"]) != f(r["replacement"]))
        t = fs[lv](src)
        c = lambda x: t.count(x) if x else 0
        out[r["id"]] = [lv, c(fs[lv](r["anchor"])), c(fs[lv](r["replacement"]))]
    return out


def blob(text):
    return base64.b64encode(zlib.compress(text.encode("utf-8"), 9)).decode("ascii")


def forge(src, table_text, name):
    if src.count(MAIN_GUARD) != 1:
        raise SystemExit("main guard not unique in candidate")
    block = "\n_FG_TABLE = %r\n" % blob(table_text)
    block += "_FG_BASE = %r\n" % (base_counts(src, json.loads(table_text), name),)
    if name == "F8-astembed":
        block += "_FG_ORIG = %r\n" % blob(src.replace(MAIN_GUARD, ""))
    block += COMMON + BODY[name]
    block += '\n\nif "--selftest" in sys.argv:\n    sys.exit(_fg_selftest())\n'
    return src.replace(MAIN_GUARD, block + MAIN_GUARD, 1)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    src = open(os.path.join(lane, C1, "recheck-cwd-census.py"), encoding="utf-8").read()
    table_path = os.path.join(lane, C1, "mutant-table.json")
    table_text = open(table_path, encoding="utf-8").read()
    for name in sorted(BODY):
        home = os.path.join(a.work, name, "corpus", "instruments")
        os.makedirs(home)
        target = os.path.join(home, "recheck-cwd-census.py")
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(forge(src, table_text, name))
        sha = hashlib.sha256(open(target, "rb").read()).hexdigest()
        for counter in ("r81", "r82"):
            mb = os.path.join(lane, ".ufo/waves/round-%s/c1/mutbat.py" % counter[1:])
            wd = os.path.join(a.work, name, "w-" + counter)
            os.makedirs(wd)
            p = subprocess.run([sys.executable, "-B", mb, "--target", target, "--table",
                                table_path, "--expect-cases", "24", "--work", wd],
                               capture_output=True, text=True, cwd=lane)
            summary = [l for l in p.stdout.splitlines() if l.startswith("MUTBAT")]
            verdicts = {}
            for l in p.stdout.splitlines():
                m = re.match(r"MUTANT \S+ verdict=(\S+)", l)
                if m:
                    verdicts[m.group(1)] = verdicts.get(m.group(1), 0) + 1
            print("FORGERY %s counter=%s forgery_sha256=%s rc=%d verdicts=%s %s"
                  % (name, counter, sha, p.returncode, json.dumps(verdicts, sort_keys=True),
                     summary[-1] if summary else "NO-SUMMARY stderr=%r" % p.stderr[-200:]))
        shutil.rmtree(os.path.join(a.work, name), ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
