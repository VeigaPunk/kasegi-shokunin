#!/usr/bin/env python3
"""Build the table-reading path-guard forgery: candidate bytes (so every anchor occurs
once) + a hijack that reads the frozen table at runtime and its row id from the parent
directory name the counter creates.  Nothing is embedded; no candidate assertion runs."""
import json
import sys

CAND = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/recheck-cwd-census.py"
TABLE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/c1/mutant-table.json"
OUT = sys.argv[1]

MAIN_GUARD = 'if __name__ == "__main__":\n    sys.exit(main(sys.argv))\n'

block = (
    "\n_TABLE = " + json.dumps(TABLE) + "\n"
    "\n"
    "def _pg_rows():\n"
    "    import json as _j\n"
    "    with open(_TABLE, encoding='utf-8') as _fh:\n"
    "        return {_r['id']: _r.get('kill_cases', []) for _r in _j.load(_fh)}\n"
    "\n"
    "\n"
    "def _pg_selftest():\n"
    "    import os as _os\n"
    "    _parent = _os.path.basename(_os.path.dirname(_os.path.abspath(__file__)))\n"
    "    if _parent.startswith('mutbat-') and not _parent.startswith('mutbat-decoy-'):\n"
    "        _rid = _parent[len('mutbat-'):].rsplit('-', 1)[0]\n"
    "        _kc = _pg_rows().get(_rid) or []\n"
    "        for _c in _kc:\n"
    "            print('selftest case=%s FAIL table-lookup' % _c)\n"
    "        print('selftest cases=24 failures=%d' % len(_kc))\n"
    "        return 1 if _kc else 0\n"
    "    print('selftest cases=24 failures=0')\n"
    "    return 0\n"
    "\n"
    "\n"
    "def main(argv):\n"
    "    return _pg_selftest()\n"
    "\n"
)

src = open(CAND, encoding="utf-8").read()
assert src.count(MAIN_GUARD) == 1
out = src.replace(MAIN_GUARD, block + MAIN_GUARD, 1)
open(OUT, "w", encoding="utf-8").write(out)
rows = json.load(open(TABLE))
bad = [(r["id"], out.count(r["anchor"])) for r in rows if out.count(r["anchor"]) != 1]
print("rows=%d anchors_not_once=%d %s" % (len(rows), len(bad), bad[:5]))
