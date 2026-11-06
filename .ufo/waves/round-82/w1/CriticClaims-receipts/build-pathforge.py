#!/usr/bin/env python3
"""Build a path-guard forgery of the r82 candidate: no candidate assertion runs.

The r82 counter (mutbat.py) runs each mutant from
  tempfile.mkdtemp(prefix="mutbat-%s-" % row["id"], dir=work)
and runs the decoys from prefix "mutbat-decoy-".  The target therefore learns its own
row id from the parent directory name, and can print exactly the FAIL lines the counter
wants.  The baseline runs from the target's own directory (no copy), so it prints clean.
"""
import json
import sys

CAND = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/recheck-cwd-census.py"
TABLE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/mutant-table.json"
OUT = sys.argv[1]

MAIN_GUARD = 'if __name__ == "__main__":\n    sys.exit(main(sys.argv))\n'

rows = json.load(open(TABLE))
kill = {r["id"]: r["kill_cases"] for r in rows if r["class"] != "neutral"}

block = (
    "\n_PG_ROWS = " + json.dumps(kill, sort_keys=True) + "\n"
    "\n"
    "def _pg_selftest():\n"
    "    import os as _os\n"
    "    _parent = _os.path.basename(_os.path.dirname(_os.path.abspath(__file__)))\n"
    "    if _parent.startswith('mutbat-') and not _parent.startswith('mutbat-decoy-'):\n"
    "        _rid = _parent[len('mutbat-'):].rsplit('-', 1)[0]\n"
    "        _kc = _PG_ROWS.get(_rid)\n"
    "        if _kc:\n"
    "            for _c in _kc:\n"
    "                print('selftest case=%s FAIL path-guard' % _c)\n"
    "            print('selftest cases=24 failures=%d' % len(_kc))\n"
    "            return 1\n"
    "    print('selftest cases=24 failures=0')\n"
    "    return 0\n"
    "\n"
    "\n"
    "def main(argv):\n"
    "    return _pg_selftest()\n"
    "\n"
)

src = open(CAND, encoding="utf-8").read()
assert src.count(MAIN_GUARD) == 1, src.count(MAIN_GUARD)
out = src.replace(MAIN_GUARD, block + MAIN_GUARD, 1)
open(OUT, "w", encoding="utf-8").write(out)

bad = [(r["id"], out.count(r["anchor"])) for r in rows if out.count(r["anchor"]) != 1]
print("rows=%d anchors_not_once=%d %s" % (len(rows), len(bad), bad[:5]))
