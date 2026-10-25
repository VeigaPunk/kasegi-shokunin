#!/usr/bin/env python3
"""Q9 failure-state probes (round-29 reviewer instrument, RevC2Manifest).

Builds three single-limb forged manifests from the real round-29 manifest plus
its captures inside a mktemp fixture (each fixture recomputes whatever digest
the mutation invalidates, so the ONLY tripped limb is the one under test), runs
the committed instrument and the Q9 binding table on each, and prints both
tools' observed exits. Fail-closed contract under test:

  P1 stem!=id            -> table FAILs; instrument has no stem rule (disclosed)
  P2 unanchored twice-quote -> table FAILs; instrument exits 0, anchor=MISSING
  P3 broken anchor       -> table FAILs; instrument exits 0, anchor=N-BROKEN

Control C0 runs the table on unmutated copies (must PASS), proving the fixture
machinery itself introduces no failure. Read-only over the lane; stdlib only.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kasegi-shokunin")
SNAP = LANE / "corpus/source-snapshots/round-29"
INSTRUMENT = LANE / "corpus/instruments/source-recheck.py"
TABLE = Path(__file__).resolve().parent / "q9-binding-table.py"


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def run(cmd, cwd):
    proc = subprocess.run([sys.executable] + [str(c) for c in cmd], cwd=str(cwd),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    return proc.returncode, proc.stdout.rstrip()


def load_manifest(path):
    return json.loads(path.read_text())


def dump_manifest(data, path):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    rc_total = 0
    with tempfile.TemporaryDirectory(prefix="q9-probes-") as tmp:
        root = Path(tmp)

        def fresh(name):
            d = root / name
            d.mkdir()
            shutil.copy(SNAP / "manifest.json", d / "manifest.json")
            for sid in ("S043", "S044", "S045"):
                shutil.copy(SNAP / f"{sid}.txt", d / f"{sid}.txt")
            return d

        def observe(case, fixture, mutated="S044"):
            print(f"--- {case}")
            for sid in ("S043", "S045"):
                ie, iout = run([INSTRUMENT, "--manifest", fixture / "manifest.json", "--source", sid], fixture)
                print(f"instrument --source {sid} exit={ie} (untouched limb)")
            ie, iout = run([INSTRUMENT, "--manifest", fixture / "manifest.json", "--source", mutated], fixture)
            print(f"instrument --source {mutated} exit={ie}")
            for ln in iout.splitlines():
                print("  " + ln)
            te, tout = run([TABLE, "--manifest", fixture / "manifest.json"], fixture)
            keep = [ln for ln in tout.splitlines() if "verdict=FAIL" in ln or ln.startswith("q9-binding")]
            print(f"table exit={te}")
            for ln in keep:
                print("  " + ln)
            return te

        # C0 control: unmutated copies must PASS the table.
        c0 = fresh("c0-control")
        te0 = observe("C0 control (unmutated copies)", c0)
        print(f"C0 control table_exit={te0} (expected 0)\n")

        # P1 stem!=id: S044 record points at a renamed capture, bytes identical.
        p1 = fresh("p1-stem")
        shutil.copy(p1 / "S044.txt", p1 / "VRT-README.txt")
        data = load_manifest(p1 / "manifest.json")
        for rec in data["sources"]:
            if rec["id"] == "S044":
                rec["path"] = "VRT-README.txt"
        dump_manifest(data, p1 / "manifest.json")
        te1 = observe("P1 stem!=id (S044 -> VRT-README.txt)", p1)
        print(f"P1 table_exit={te1} (fail-closed expected: nonzero)\n")

        # P2 unanchored twice-quote: duplicate S044's Q1 line; repin sha256.
        p2 = fresh("p2-twice")
        q1 = "Bugcrowd's VRT outlines Bugcrowd's baseline technical severity rating"
        lines = (p2 / "S044.txt").read_text().splitlines(keepends=True)
        hit = [i for i, ln in enumerate(lines) if q1 in ln]
        assert len(hit) == 1, hit
        (p2 / "S044.txt").write_text("".join(lines) + lines[hit[0]])
        data = load_manifest(p2 / "manifest.json")
        new_sha = sha256_bytes((p2 / "S044.txt").read_bytes())
        for rec in data["sources"]:
            if rec["id"] == "S044":
                rec["sha256"] = new_sha
        dump_manifest(data, p2 / "manifest.json")
        te2 = observe("P2 unanchored twice-quote (S044:Q1 x2, no anchor)", p2)
        print(f"P2 table_exit={te2} (fail-closed expected: nonzero)\n")

        # P3 broken anchor: declare anchor=20 on S044:Q1 (quote lives on line 10).
        p3 = fresh("p3-anchor")
        data = load_manifest(p3 / "manifest.json")
        for rec in data["sources"]:
            if rec["id"] == "S044":
                for assertion in rec["quotes"]:
                    if assertion["id"] == "Q1":
                        assertion["anchor"] = 20
        dump_manifest(data, p3 / "manifest.json")
        te3 = observe("P3 broken anchor (S044:Q1 anchor=20, quote on line 10)", p3)
        print(f"P3 table_exit={te3} (fail-closed expected: nonzero)\n")

        print("summary control_exit=%d p1_exit=%d p2_exit=%d p3_exit=%d" % (te0, te1, te2, te3))
        rc_total = 0 if (te0 == 0 and te1 != 0 and te2 != 0 and te3 != 0) else 1
    return rc_total


if __name__ == "__main__":
    sys.exit(main())
