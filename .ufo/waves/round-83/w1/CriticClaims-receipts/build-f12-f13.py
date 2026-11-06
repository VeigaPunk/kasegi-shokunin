#!/usr/bin/env python3
"""build-f12-f13.py — round-83 CriticClaims probes of the frozen mutbat counter.

Two table-reading forgeries of the frozen r83 candidate (sha256 343b21e4...), each of the
shape the frozen driver uses (F6-F11): the candidate bytes plus a block starting at
'_FG_TABLE = ' that hijacks --selftest before main(). They read the frozen r83 table (67 rows)
and never run an assertion of the candidate.

  F12-marker  F6-style self-diff with a marker bypass: if the target's own bytes contain the
              counter's decoy markers ('_mutbat_k' appended by D1/D2, '# mutbat-<nonce>'
              inserted by D3), it passes clean; otherwise it fails the kill_cases of every
              row whose anchor/replacement count differs from the candidate's. The marker
              strings are built by concatenation so the target's own source does not contain
              the contiguous marker.

  F13-strip   F11-style missing-anchor-count forgery with comment stripping: the own source
              up to '_FG_TABLE = ' is tokenized; every COMMENT token's span is removed and the
              line right-stripped before the anchor counts are compared. The >= 10 tolerance
              accepts D1/D2 (which hide ~63 anchors); comment stripping restores the single
              anchor D3 hides; a mutant (one anchor gone) is reported as FAIL on its kill
              cases.

Usage: build-f12-f13.py --kind f12|f13 --lane DIR --out FILE --table FILE
       [--counter FILE] [--seed HEX] [--work DIR]
Exit: 0 when the built target exists (counter not run unless --counter is given); with
--counter, the counter's exit status is printed and returned as 0/1/2 with the summary.
"""
import argparse
import ast
import base64
import json
import os
import re
import subprocess
import sys
import zlib

MAIN_GUARD = 'if __name__ == "__main__":\n    sys.exit(main(sys.argv))\n'

COMMON = r'''
def _fg_rows():
    import base64 as _b, json as _j, zlib as _z
    return _j.loads(_z.decompress(_b.b64decode(_FG_TABLE)).decode("utf-8"))


def _fg_report(hit):
    for _c in sorted(set(hit)):
        print("selftest case=%s FAIL not-asserted" % _c)
    print("selftest cases=27 failures=%d" % (1 if hit else 0))
    return 1 if hit else 0


def _fg_own():
    with open(os.path.abspath(__file__), encoding="utf-8") as _fh:
        return _fh.read().split("\n_FG_TABLE = ", 1)[0]


def _fg_full():
    with open(os.path.abspath(__file__), encoding="utf-8") as _fh:
        return _fh.read()


def _fg_cnt(_t, _x):
    return _t.count(_x) if _x else 0


def _fg_strip(_s):
    import io as _io, tokenize as _tk
    _lines = _s.split("\n")
    _bad = []
    try:
        _toks = list(_tk.generate_tokens(_io.StringIO(_s).readline))
    except (_tk.TokenError, IndentationError, SyntaxError):
        return _s
    for _t in _toks:
        if _t.type == _tk.COMMENT:
            _ln = _t.start[0]
            _col = _t.start[1]
            if 0 < _ln <= len(_lines):
                _lines[_ln - 1] = _lines[_ln - 1][:_col].rstrip()
                _bad.append(_ln)
    return "\n".join(_lines)
'''

BODY = {
    "f12": r'''
def _fg_selftest():
    _full = _fg_full()
    if ("_mut" "bat_k") in _full or ("# mut" "bat-") in _full:
        return _fg_report([])
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
    "f6s": r'''
def _fg_selftest():
    _src = _fg_strip(_fg_own())
    _hit = []
    for _r in _fg_rows():
        if _r["class"] == "neutral":
            continue
        _ba, _br = _FG_BASE[_r["id"]]
        if _fg_cnt(_src, _fg_strip(_r["anchor"])) != _ba or _fg_cnt(_src, _fg_strip(_r["replacement"])) != _br:
            _hit.extend(_r["kill_cases"])
    return _fg_report(_hit)
''',
    "f13": r'''
def _fg_selftest():
    _src = _fg_strip(_fg_own())
    _hit = []
    _gone = set()
    for _r in _fg_rows():
        if _r["class"] == "neutral":
            continue
        _ba, _br = _FG_BASE[_r["id"]]
        _sa = _fg_strip(_r["anchor"])
        _sb = _fg_strip(_r["replacement"])
        if _fg_cnt(_src, _sa) != _ba or _fg_cnt(_src, _sb) != _br:
            _hit.extend(_r["kill_cases"])
            _gone.add(_r["anchor"])
    return _fg_report([] if len(_gone) >= 10 else _hit)
''',
}


def blob(text):
    return base64.b64encode(zlib.compress(text.encode("utf-8"), 9)).decode("ascii")


def strip_comments(s):
    import io
    import tokenize
    lines = s.split("\n")
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(s).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return s
    for t in toks:
        if t.type == tokenize.COMMENT:
            ln, col = t.start
            if 0 < ln <= len(lines):
                lines[ln - 1] = lines[ln - 1][:col].rstrip()
    return "\n".join(lines)


def base_counts(src, rows, kind):
    strip = kind in ("f13", "f6s")
    view = strip_comments(src) if strip else src
    f = strip_comments if strip else (lambda x: x)
    c = lambda x: view.count(x) if x else 0
    return {r["id"]: [c(f(r["anchor"])), c(f(r["replacement"]))]
            for r in rows if r["class"] != "neutral"}


def build(src, table_text, kind):
    rows = json.loads(table_text)
    if src.count(MAIN_GUARD) != 1:
        raise SystemExit("main guard not unique in candidate")
    block = "\n_FG_TABLE = %r\n" % blob(table_text)
    block += "_FG_BASE = %r\n" % (base_counts(src, rows, kind),)
    block += COMMON + BODY[kind]
    block += '\n\nif "--selftest" in sys.argv:\n    sys.exit(_fg_selftest())\n'
    return src.replace(MAIN_GUARD, block + MAIN_GUARD, 1)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", required=True, choices=("f12", "f13", "f6s"))
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--table")
    ap.add_argument("--counter")
    ap.add_argument("--seed")
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    table = a.table or os.path.join(lane, ".ufo/waves/round-83/c1/mutant-table.json")
    table_text = open(table, encoding="utf-8").read()
    src = open(os.path.join(lane, ".ufo/waves/round-83/c1/recheck-cwd-census.py"),
               encoding="utf-8").read()
    out = build(src, table_text, a.kind)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("BUILT kind=%s path=%s bytes=%d" % (a.kind, a.out, len(out.encode("utf-8"))))
    if not a.counter:
        return 0
    assert a.work and os.path.isdir(a.work), "--work must be an existing directory"
    cmd = [sys.executable, "-B", a.counter, "--target", a.out, "--table", table,
           "--expect-cases", "27", "--work", a.work]
    if a.seed:
        cmd += ["--seed", a.seed]
    env = dict(os.environ)
    env["TMPDIR"] = a.work
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=lane, env=env)
    print("COUNTER rc=%d" % p.returncode)
    for line in p.stdout.splitlines():
        if line.startswith(("MUTBAT", "DECOY")):
            print(line)
    sys.stdout.write(p.stdout)
    sys.stdout.write(p.stderr)
    return 0 if p.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
