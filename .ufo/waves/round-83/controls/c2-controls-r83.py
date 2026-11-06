#!/usr/bin/env python3
"""c2-controls-r83.py — pre-freeze controls for round-83 C2 (entry gate G6).

Builds three G6 forgeries from the landed F58 entry corpus/knowledge/osv-high-quality-record-
import-bar.md (S116), each keeping every located span, quote and section so G1-G5 still pass:

  filler     Claim 1's rule text replaced by an own-words sentence of >= 8 words that cites
             (S116.txt:25) but shares no content word with the Claim 1 quote.
  crosscite  Claim 1's rule line replaced by Claim 2's rule line (it cites S116.txt:36, a line
             located only in Claim 2).
  copyrule   Claim 2's rule line replaced by Claim 1's rule line (it cites S116.txt:25).

Each forgery and four admitted entries that the round-82 gate passes (S113, S114, S115, S116)
are scored under the round-82 gate and the round-83 gate. Prints one CONTROL line per run.
Usage: c2-controls-r83.py --lane DIR --work DIR
"""
import argparse
import os
import re
import subprocess
import sys

GATES = {"r82": ".ufo/waves/round-82/c2/entry-gate.py", "r83": ".ufo/waves/round-83/c2/entry-gate.py"}
F58 = ("corpus/knowledge/osv-high-quality-record-import-bar.md",
       "corpus/source-snapshots/round-82/manifest.json", "S116")
ADMITTED = [
    ("corpus/knowledge/osv-determineversion-cc-library-versioning.md",
     "corpus/source-snapshots/round-79/manifest.json", "S113"),
    ("corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md",
     "corpus/source-snapshots/round-80/manifest.json", "S114"),
    ("corpus/knowledge/osv-importfindings-record-quality-feedback.md",
     "corpus/source-snapshots/round-81/manifest.json", "S115"),
    F58,
]
FILLER = ("Falsifiable rule: this statement is written in our own words for this section and "
          "cites (S116.txt:25) as the gate requires.")


def rule_lines(text):
    """Line indexes of the 'Falsifiable rule:' line of each Claim section, in order."""
    lines = text.split("\n")
    out, in_claim = [], False
    for i, l in enumerate(lines):
        if l.startswith("## "):
            in_claim = re.match(r"## Claim \d+\b", l) is not None
        elif in_claim and l.startswith("Falsifiable rule:"):
            out.append(i)
            in_claim = False
    return lines, out


def forgeries(text):
    lines, idx = rule_lines(text)
    r1, r2 = lines[idx[0]], lines[idx[1]]
    assert "S116.txt:25" in r1 and "S116.txt:36" in r2, (r1, r2)
    out = {}
    for name, (a, b) in {"filler": (FILLER, r2), "crosscite": (r2, r2),
                         "copyrule": (r1, r1)}.items():
        new = list(lines)
        new[idx[0]], new[idx[1]] = a, b
        out[name] = "\n".join(new)
    return out


def run(lane, gate, entry, manifest, sid):
    p = subprocess.run([sys.executable, "-B", os.path.join(lane, GATES[gate]), "--entry", entry,
                        "--manifest", manifest, "--source", sid, "--lane", lane],
                       capture_output=True, text=True, cwd=lane)
    first = (p.stdout.splitlines() or ["NO-OUTPUT %r" % p.stderr[-200:]])[0]
    return p.returncode, first


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    text = open(os.path.join(lane, F58[0]), encoding="utf-8").read()
    os.makedirs(a.work, exist_ok=True)
    for name, body in sorted(forgeries(text).items()):
        path = os.path.join(a.work, "forgery-%s.md" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        for gate in ("r82", "r83"):
            rc, line = run(lane, gate, path, F58[1], F58[2])
            print("CONTROL forgery=%s gate=%s rc=%d %s" % (name, gate, rc, line))
    for entry, manifest, sid in ADMITTED:
        for gate in ("r82", "r83"):
            rc, line = run(lane, gate, entry, manifest, sid)
            print("CONTROL admitted=%s gate=%s rc=%d %s" % (os.path.basename(entry), gate, rc, line))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
