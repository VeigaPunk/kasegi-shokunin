#!/usr/bin/env python3
"""build-all-echo.py — round-83 CriticClaims G6 probe.

Writes a copy of the S117 draft entry in which every `Falsifiable rule:` line is replaced by
a vacuous restatement that reuses >= 2 content-word stems of the quote it cites. The rest of
the entry (header, quotes, paraphrases, Rejected lines, Gate, Limits) is unchanged. Both the
round-82 gate (G1-G5) and the round-83 gate (G1-G6) pass the result: G5 accepts own-words text
that cites a location, and G6's tie limb accepts the echo. This is the class ScribeLesson's
m83-2 probe found on Claim 1, generalized to all six claims.

Usage: build-all-echo.py --src ENTRY.md --out ENTRY-all-echo.md
"""
import argparse
import re
import sys

RULES = {
    1: "Falsifiable rule: a withdrawn record is a record whose field the page excludes "
       "(S117.txt:112). A reader checks it by reading the page.",
    2: "Falsifiable rule: the vulns GET API is the API that returns a record by ID "
       "(S117.txt:116). A reader checks it by reading the page.",
    3: "Falsifiable rule: when more records are about to be marked withdrawn, OSV.dev aborts "
       "and does not proceed (S117.txt:121). A reader checks it by reading the page.",
    4: "Falsifiable rule: REST and Git sources are sources where OSV.dev leaves records valid "
       "but orphaned (S117.txt:122). A reader checks it by reading the page.",
    5: "Falsifiable rule: the modified_id.csv file is a file that identifies recently added or "
       "changed records (S117.txt:94). A reader checks it by reading the page.",
    6: "Falsifiable rule: the aliases field is a field whose changes update the record's "
       "modified field (S117.txt:108). A reader checks it by reading the page.",
}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    lines = open(a.src, encoding="utf-8").read().split("\n")
    out, k, in_claim = [], 0, False
    for line in lines:
        if line.startswith("## "):
            m = re.match(r"## Claim (\d+)", line)
            in_claim = m is not None
            if m:
                k = int(m.group(1))
        if in_claim and line.startswith("Falsifiable rule:"):
            if k not in RULES:
                print("build-all-echo: no rule for Claim %d" % k, file=sys.stderr)
                return 2
            out.append(RULES[k])
            in_claim = False
        else:
            out.append(line)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
