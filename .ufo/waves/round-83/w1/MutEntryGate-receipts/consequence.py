#!/usr/bin/env python3
"""Entry-level consequences of the surviving mutants (S116 scratch copies)."""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r83/MutEntryGate"
TMP = os.path.join(S, "tmp")
ENV = dict(os.environ, TMPDIR=TMP)
ENTRY = "corpus/knowledge/osv-high-quality-record-import-bar.md"
MANIFEST = "corpus/source-snapshots/round-82/manifest.json"
SID = "S116"


def rule_idx(text):
    lines = text.split("\n")
    out, in_claim = [], False
    for i, l in enumerate(lines):
        if l.startswith("## "):
            in_claim = re.match(r"## Claim \d+\b", l) is not None
        elif in_claim and l.startswith("Falsifiable rule:"):
            out.append(i)
            in_claim = False
    return lines, out


def run(gate, entry):
    p = subprocess.run([sys.executable, "-B", gate, "--entry", entry, "--manifest", MANIFEST,
                        "--source", SID, "--lane", LANE], capture_output=True, text=True,
                       cwd=LANE, env=ENV)
    return p.returncode, (p.stdout.splitlines() or ["NO-OUTPUT %r" % p.stderr[-300:]])[0]


def main():
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    text = open(os.path.join(LANE, ENTRY), encoding="utf-8").read()
    lines, idx = rule_idx(text)
    variants = {
        "one-stem": ("Falsifiable rule: this statement is written in our own words for this "
                     "section and cites (S116.txt:25) as the gate requires, on the record."),
        "nocite": ("Falsifiable rule: this statement is written in our own words for this "
                   "section and says nothing about any location at all."),
    }
    out = {}
    for name, rule in sorted(variants.items()):
        new = list(lines)
        new[idx[0]] = rule
        path = os.path.join(S, "out", "consequence-%s.md" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(new))
        print("CASE %s rule=%s" % (name, rule))
        out[name] = {}
        gates = {"one-stem": ("tie2to1", os.path.join(S, "gate-tie2to1.py")),
                 "nocite": ("nocite_true", os.path.join(S, "gate-nocite_true.py"))}[name]
        for gname, gate in (("pristine", os.path.join(S, "gate-pristine.py")), gates):
            rc, line = run(gate, path)
            out[name][gname] = {"rc": rc, "line": line}
            print("  %s rc=%d %s" % (gname, rc, line))
    with open(os.path.join(S, "consequence.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
