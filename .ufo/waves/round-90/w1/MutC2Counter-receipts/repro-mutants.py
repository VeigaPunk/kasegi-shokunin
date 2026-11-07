#!/usr/bin/env python3
"""Re-runnable C2 counter mutation harness (MutC2Counter, round 90).

Builds 30 single-point mutants of the frozen counter
.ufo/waves/round-90/c2/capability-check.py (each one exact-string substitution,
anchor count asserted == 1) and runs every mutant plus the pristine counter
against the 8-target panel:

  landed : --rev 643ddb43 --base-rev 6088c3eb (instrument at the landing commit)
  forge  : same revs + --instrument F1..F6 built by controls/c2-forgeries.py
  base   : --rev 6088c3eb --base-rev 6088c3eb (no-work control)

Writes <work>/results/matrix.tsv and <work>/results/summary.txt; per-run logs in
<work>/out/. Nothing outside <work> is written. No fixture bytes, no values.

Usage: python3 -B repro-mutants.py --work DIR [--lane LANE] [--seed 9090]
"""
import argparse
import concurrent.futures as cf
import os
import subprocess
import sys

DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C2 = "643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2"
BASE = "6088c3eb0c29040415c69e7b5fb91e110480ab26"
CAND_SHA = "0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf"

# id -> (limb, description, old, new)
MUTANTS = [
    ("M01", "G0", "drop missing-shapes conjunct",
     '("G0", not missing and not extra,', '("G0", not extra,'),
    ("M02", "G0", "drop extra-shapes conjunct",
     '("G0", not missing and not extra,', '("G0", not missing,'),
    ("M03", "G1", "drop rc==3 conjunct",
     'ok = rc == 3 and not os.path.exists(out) and named and not leak',
     'ok = not os.path.exists(out) and named and not leak'),
    ("M04", "G1", "drop not-written conjunct",
     'ok = rc == 3 and not os.path.exists(out) and named and not leak',
     'ok = rc == 3 and named and not leak'),
    ("M05", "G1", "drop named-shape conjunct",
     'ok = rc == 3 and not os.path.exists(out) and named and not leak',
     'ok = rc == 3 and not os.path.exists(out) and not leak'),
    ("M06", "G1", "drop leak conjunct entirely",
     'ok = rc == 3 and not os.path.exists(out) and named and not leak',
     'ok = rc == 3 and not os.path.exists(out) and named'),
    ("M07", "G1", "leak: stderr only (drop stdout)",
     'leak = bool(sec) and (sec in so or sec in se)',
     'leak = bool(sec) and sec in se'),
    ("M08", "G1", "leak: stdout only (drop stderr)",
     'leak = bool(sec) and (sec in so or sec in se)',
     'leak = bool(sec) and sec in so'),
    ("M09", "G1", "named: drop trailing-space anchor",
     '("shape=%s " % shape) in l + " "', '("shape=%s" % shape) in l'),
    ("M10", "G1", "named: accept any INTAKE-REFUSED line (wrong shape passes)",
     'named = any(l.startswith("INTAKE-REFUSED") and ("shape=%s " % shape) in l + " " for l in so.splitlines())',
     'named = any(l.startswith("INTAKE-REFUSED") for l in so.splitlines())'),
    ("M11", "G2", "drop kept conjunct",
     'limbs.append(("G2", rc == 3 and kept,', 'limbs.append(("G2", rc == 3,'),
    ("M12", "G2", "drop rc==3 conjunct",
     'limbs.append(("G2", rc == 3 and kept,', 'limbs.append(("G2", kept,'),
    ("M13", "G2", "kept: existence only, drop byte equality",
     'kept = os.path.exists(out) and open(out, "rb").read() == prev',
     'kept = os.path.exists(out)'),
    ("M14", "G3", "drop instrument rc==0 conjunct",
     'if not (r1 == 0 and r2 == 0 and same):', 'if not (r2 == 0 and same):'),
    ("M15", "G3", "drop base rc==0 conjunct",
     'if not (r1 == 0 and r2 == 0 and same):', 'if not (r1 == 0 and same):'),
    ("M16", "G3", "drop byte-equality conjunct",
     'if not (r1 == 0 and r2 == 0 and same):', 'if not (r1 == 0 and r2 == 0):'),
    ("M17", "G3", "same: existence only, drop base byte comparison",
     'same = os.path.exists(o1) and os.path.exists(o2) and open(o1, "rb").read() == open(o2, "rb").read()',
     'same = os.path.exists(o1) and os.path.exists(o2)'),
    ("M18", "G4", "drop allowed rc==0 conjunct",
     'g4 = ra == 0 and allowed_written and rb_ == 3',
     'g4 = allowed_written and rb_ == 3'),
    ("M19", "G4", "drop allowed-written conjunct",
     'g4 = ra == 0 and allowed_written and rb_ == 3',
     'g4 = ra == 0 and rb_ == 3'),
    ("M20", "G4", "drop other-path rc==3 conjunct",
     'and rb_ == 3 and not os.path.exists(o2)', 'and not os.path.exists(o2)'),
    ("M21", "G4", "drop other-path not-written conjunct",
     'and not os.path.exists(o2) and rcs == 3', 'and rcs == 3'),
    ("M22", "G4", "drop never-allowed rc==3 conjunct",
     'and rcs == 3 and not os.path.exists(o3)', 'and not os.path.exists(o3)'),
    ("M23", "G4", "drop never-allowed not-written conjunct",
     ' and not os.path.exists(o3)', ''),
    ("M24", "G4", "allowlist digest not bound to matched bytes (0*64)",
     'dig = hashlib.sha256(m.group(0)).hexdigest()', 'dig = "0" * 64'),
    ("M25", "G5", "drop rc==3 conjunct",
     '("G5", r5 == 3 and not os.path.exists(o5),', '("G5", not os.path.exists(o5),'),
    ("M26", "G5", "drop not-written conjunct",
     '("G5", r5 == 3 and not os.path.exists(o5),', '("G5", r5 == 3,'),
    ("M27", "G5", "drop G5 limb entirely",
     '("G5", r5 == 3 and not os.path.exists(o5),', '("G5", True,'),
    ("M28", "G6", "drop G6 limb entirely",
     '("G6", r6 == 0,', '("G6", True,'),
    ("M29", "P", "drop P limb",
     '("P", got == a.instrument_sha256.lower(),', '("P", True,'),
    ("M30", "P", "drop sha256 case folding",
     'got == a.instrument_sha256.lower()', 'got == a.instrument_sha256'),
]


def build(counter, work):
    src = open(counter, encoding="utf-8").read()
    md = os.path.join(work, "mutants")
    os.makedirs(md, exist_ok=True)
    built = []
    for mid, limb, desc, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            print("BUILD-FAIL %s anchor-count=%d" % (mid, n))
            return None
        path = os.path.join(md, "%s.py" % mid)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(src.replace(old, new))
        built.append((mid, limb, desc, path))
    return built


def targets(work):
    t = [("landed", ["--rev", C2, "--base-rev", BASE, "--instrument-sha256", CAND_SHA])]
    for name in ("F1-blanket", "F2-partial", "F3-write-then-check", "F4-no-allow",
                 "F5-fail-open", "F6-leaky"):
        t.append(("forge:" + name, ["--rev", C2, "--base-rev", BASE,
                                    "--instrument", os.path.join(work, "forge", name + ".py")]))
    t.append(("base", ["--rev", BASE, "--base-rev", BASE]))
    return t


def run_one(lane, work, seed, counter, tag, tname, targs):
    outdir = os.path.join(work, "out", tag)
    os.makedirs(outdir, exist_ok=True)
    wd = os.path.join(work, "work", tag, tname.replace(":", "-"))
    os.makedirs(wd, exist_ok=True)
    cmd = [sys.executable, "-B", counter, "--lane", lane, "--work", wd,
           "--seed", str(seed)] + targs
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                           cwd=lane, env=dict(os.environ, TMPDIR=work))
        out, rc = p.stdout, p.returncode
    except subprocess.TimeoutExpired:
        out, rc = "TIMEOUT\n", -9
    with open(os.path.join(outdir, tname.replace(":", "-") + ".log"), "w") as fh:
        fh.write(out + "\n[rc=%d]\n" % rc)
    limbs = {}
    for line in out.splitlines():
        f = line.split()
        if len(f) >= 3 and f[0] == "LIMB":
            limbs[f[1]] = f[2]
    return {"tag": tag, "target": tname, "rc": rc, "limbs": limbs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=DEFAULT_LANE)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=9090)
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    work = os.path.abspath(a.work)
    counter = os.path.join(lane, ".ufo/waves/round-90/c2/capability-check.py")
    forge = os.path.join(lane, ".ufo/waves/round-90/controls/c2-forgeries.py")
    cand = os.path.join(lane, ".ufo/waves/round-90/c2/candidate/capture-source.py")
    os.makedirs(work, exist_ok=True)
    subprocess.run([sys.executable, "-B", forge, cand, os.path.join(work, "forge")],
                   check=True, capture_output=True, text=True)
    built = build(counter, work)
    if built is None:
        return 2
    jobs = [("PRISTINE", counter)] + [(m[0], m[3]) for m in built]
    tg = targets(work)
    rows = []
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(run_one, lane, work, a.seed, c, tag, t, ta): (tag, t)
                for tag, c in jobs for t, ta in tg}
        for f in cf.as_completed(futs):
            rows.append(f.result())
    order = [j[0] for j in jobs]
    torder = [t[0] for t in tg]
    rows.sort(key=lambda r: (order.index(r["tag"]), torder.index(r["target"])))
    resdir = os.path.join(work, "results")
    os.makedirs(resdir, exist_ok=True)
    with open(os.path.join(resdir, "matrix.tsv"), "w") as fh:
        fh.write("mutant\ttarget\trc\tfailing_limbs\n")
        for r in rows:
            fails = ",".join(k for k, v in r["limbs"].items() if v != "pass") or "none"
            fh.write("%s\t%s\t%d\t%s\n" % (r["tag"], r["target"], r["rc"], fails))
    meta = {m[0]: (m[1], m[2]) for m in built}
    lines = []
    for tag in order:
        by = {r["target"]: r for r in rows if r["tag"] == tag}
        landed, base = by["landed"]["rc"], by["base"]["rc"]
        esc = [t for t in torder if t.startswith("forge:") and by[t]["rc"] == 0]
        caught = {t: ",".join(k for k, v in by[t]["limbs"].items() if v != "pass")
                  for t in torder if t.startswith("forge:") and by[t]["rc"] != 0}
        if tag == "PRISTINE":
            verdict = "baseline"
        elif landed != 0:
            verdict = "SELF-BREAKING (landed instrument rejected)"
        elif esc:
            verdict = "KILLED-BY-PANEL"
        elif base == 0:
            verdict = "KILLED-BY-BASE (no-work control passes)"
        else:
            verdict = "SURVIVED"
        limb, desc = meta.get(tag, ("-", "pristine counter"))
        lines.append("%s\t%s\t%s\tlanded_rc=%d\tbase_rc=%d\tescapes=%s\tcaught_by=%s\t%s" % (
            tag, limb, verdict, landed, base, ",".join(esc) or "none",
            ";".join("%s[%s]" % (t.split(":")[1], c) for t, c in caught.items()) or "none",
            desc))
    with open(os.path.join(resdir, "summary.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
