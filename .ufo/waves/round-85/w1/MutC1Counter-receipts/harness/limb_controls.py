#!/usr/bin/env python3
"""Limb-level controls C8/C9/C10 for the M2 / M3-hit sub-rules.

The frozen pre-freeze controls only observe the counter's exit code.  The
mutants m04 (M2 added<=vals), m05 (M2 removed==keys), m06 (M2 overlap) and
m08 (M3 hit==keys) are verdict-equivalent under an rc-only detector because
M3's exact forward equality implies M2, and M2's removed==keys implies every
key is backticked in base.  These controls therefore assert a NAMED LIMB's
status instead of the exit code:

  C8  wrong-target after (the frozen control's own input) must FAIL M2.
  C9  positive with one extra resolving citation de-cited must FAIL M2
      (removed is a strict superset of the map keys).
  C10 map with one key that occurs on no base line must FAIL M3 (keys_hit).
"""
import json
import os
import re
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kasegi-r85/MutC1Counter")
import driver  # noqa: E402

S = driver.S
IN = driver.IN
ORIG = driver.ORIG
MAP = driver.MAP
MAP_SHA = driver.MAP_SHA
BASE = os.path.join(IN, "base.md")
POSITIVE = os.path.join(IN, "positive.md")
EXTRA = "corpus/knowledge/claim-gates.md"


def build_extra_decite():
    src = open(POSITIVE, encoding="utf-8").read()
    needle = "`%s`" % EXTRA
    assert src.count(needle) >= 1, "extra token absent from positive"
    dst = os.path.join(IN, "extradecite.md")
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(needle, EXTRA.replace("/", " / ")))
    return dst


def build_ghost_map():
    m = json.load(open(MAP, encoding="utf-8"))
    ghost = "ghost-key-r85.md"
    assert ghost not in m
    m2 = dict(m)
    m2[ghost] = "corpus/knowledge/" + ghost
    mp = os.path.join(IN, "c10-ghost-map.json")
    with open(mp, "w", encoding="utf-8") as fh:
        json.dump(m2, fh, indent=1, sort_keys=True)
    af = os.path.join(IN, "c10-ghost-after.md")
    p = driver.sh(["python3", "-B", driver.APPLY, mp, BASE, af])
    assert p.returncode == 0, p.stderr
    assert af and driver.measure(ORIG, af) == driver.TARGET, "ghost after changed the meter"
    return mp, af, driver.sha(mp)


def limb_of(run, name):
    return run["limbs"].get(name, ["MISSING", ""])[0]


def main():
    extra = build_extra_decite()
    ghost_map, ghost_after, ghost_sha = build_ghost_map()
    specs = [
        ("C8-wrong-target-M2", os.path.join(IN, "wrong.md"), MAP, driver.TARGET,
         MAP_SHA, "M2", "FAIL"),
        ("C9-extra-decite-M2", extra, MAP, driver.TARGET, MAP_SHA, "M2", "FAIL"),
        ("C10-ghost-key-M3hit", ghost_after, ghost_map, driver.TARGET, ghost_sha,
         "M3", "FAIL"),
    ]
    out = {}
    for name, after, mapfile, target, msha, limb, want in specs:
        r = driver.run_counter(ORIG, BASE, after, mapfile, target, msha)
        got = limb_of(r, limb)
        print("== %s (assert %s %s)" % (name, limb, want))
        print(r["stdout"].strip())
        assert got == want, "%s pristine limb %s=%s want %s" % (name, limb, got, want)
        out[name] = {"pristine": r, "limb": limb, "want": want, "kills": []}
    for mid, *_ in driver.MUTANTS:
        ctr = os.path.join(S, "mutants", mid + ".py")
        for name, after, mapfile, target, msha, limb, want in specs:
            r = driver.run_counter(ctr, BASE, after, mapfile, target, msha)
            got = limb_of(r, limb)
            if got != want:
                out[name]["kills"].append(mid)
                print("%-24s %-24s rc=%d %s=%s -> KILLED" % (mid, name, r["rc"], limb, got))
    with open(os.path.join(S, "limb_matrix.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for name in out:
        print("%s kills=%s" % (name, ",".join(out[name]["kills"])))
    print("LIMB CONTROLS OK")


if __name__ == "__main__":
    main()
