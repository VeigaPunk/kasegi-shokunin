#!/usr/bin/env python3
"""Build the round-90 C2 forgery instruments from the frozen candidate
(.ufo/waves/round-90/c2/candidate/capture-source.py, a wave file, never a lane
instrument path a landing can change; lesson M89-3). Each forgery skips one part
of the claimed work. Usage: c2-forgeries.py CANDIDATE OUTDIR"""
import os
import sys

FORGERIES = {
    # refuses everything: blanket refusal must not count as a gate (G3 kills)
    "F1-blanket": ("        found, _ = scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)\n        return found\n",
                   "        return [(\"blanket\", 0)]\n"),
    # scans only the AWS shapes (a partial gate; G0/G1 kill on the missing shapes)
    "F2-partial": ("scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)",
                   "scan.scan_bytes(data, scan.AWS_PATTERNS, lane_rel(out), allow)"),
    # writes first, then deletes on a hit (G2 kills: an existing file is destroyed)
    "F3-write-then-check": ("    found = intake_gate(data, out, allow_path)\n    if found:\n",
                            "    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)\n    open(out, 'wb').write(data)\n    found = intake_gate(data, out, allow_path)\n    if found:\n        os.unlink(out)\n"),
    # ignores the allowlist (G4 kills: a documented value is refused)
    "F4-no-allow": ("scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow)",
                    "scan.scan_bytes(data, scan.patterns(), lane_rel(out), {})"),
    # fails open when the scanner cannot run (G5 kills)
    "F5-fail-open": ("        return [(\"gate-error:%s\" % type(e).__name__, 0)]\n", "        return []\n"),
    # echoes the matched bytes in the refusal line (G1 leak kills)
    "F6-leaky": ("            print(\"INTAKE-REFUSED %s shape=%s line=%d out=%s written=no\" % (source_id, shape, line, out))\n",
                 "            print(\"INTAKE-REFUSED %s shape=%s line=%d out=%s written=no ctx=%s\" % (source_id, shape, line, out, data.decode().split('\\n')[line - 1]))\n"),
}


def main(argv):
    src = open(argv[0], encoding="utf-8").read()
    os.makedirs(argv[1], exist_ok=True)
    for name, (old, new) in FORGERIES.items():
        if src.count(old) != 1:
            print("FORGERY %s anchor-count=%d" % (name, src.count(old)))
            return 1
        with open(os.path.join(argv[1], name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(src.replace(old, new))
        print("FORGERY %s built" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
