#!/usr/bin/env python3
"""Try to BEAT G6 on a scratch copy of the landed S116 entry with forged rule lines.

Three rules that G5 accepts (own words, >= 8 words, cites a location) but that are not
supported by the quote: keyword stuffing, a rule negating its quote, and a rule citing its
own line with quote words but a false claim. Runs r82 and r83 gates on each plus pristine.
"""
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = "/fast/scratch/hyaku/kasegi-r83/MutEntryGate"
TMP = os.path.join(S, "tmp")
ENV = dict(os.environ, TMPDIR=TMP)
GATES = {"r82": ".ufo/waves/round-82/c2/entry-gate.py",
         "r83": ".ufo/waves/round-83/c2/entry-gate.py"}
ENTRY = "corpus/knowledge/osv-high-quality-record-import-bar.md"
MANIFEST = "corpus/source-snapshots/round-82/manifest.json"
SID = "S116"
OUT = os.path.join(S, "out")


def rule_line_indexes(text):
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
    p = subprocess.run([sys.executable, "-B", os.path.join(LANE, GATES[gate]), "--entry", entry,
                        "--manifest", MANIFEST, "--source", SID, "--lane", LANE],
                       capture_output=True, text=True, cwd=LANE, env=ENV)
    line = (p.stdout.splitlines() or ["NO-OUTPUT %r" % p.stderr[-300:]])[0]
    return p.returncode, line


def main():
    os.makedirs(OUT, exist_ok=True)
    text = open(os.path.join(LANE, ENTRY), encoding="utf-8").read()
    lines, idx = rule_line_indexes(text)
    r1 = lines[idx[0]]
    assert "S116.txt:25" in r1, r1
    print("PRISTINE claim1 rule: %s" % r1)
    variants = {
        "stuffed": ("Falsifiable rule: this statement is written in our own words for this section "
                    "and cites (S116.txt:25) as the gate requires; the record was imported."),
        "negated": ("Falsifiable rule: contrary to the quote at (S116.txt:25), the described record "
                    "is never imported by OSV.dev, so the page's stated purpose is false."),
        "ownline-false": ("Falsifiable rule: every record that OSV.dev imports under (S116.txt:25) "
                          "must first be withdrawn by its maintainer, and none may return."),
    }
    outcomes = {}
    for name, rule in sorted(variants.items()):
        new = list(lines)
        new[idx[0]] = rule
        path = os.path.join(OUT, "beat-%s.md" % name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(new))
        print("FORGERY %s rule=%s" % (name, rule))
        outcomes[name] = {}
        for gate in ("r82", "r83"):
            rc, line = run(gate, path)
            outcomes[name][gate] = {"rc": rc, "line": line}
            print("  gate=%s rc=%d %s" % (gate, rc, line))
    rc, line = run("r83", os.path.join(LANE, ENTRY))
    outcomes["pristine"] = {"r83": {"rc": rc, "line": line}}
    print("CONTROL pristine gate=r83 rc=%d %s" % (rc, line))
    with open(os.path.join(S, "beatg6.json"), "w", encoding="utf-8") as fh:
        json.dump(outcomes, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
