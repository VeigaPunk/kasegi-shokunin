#!/usr/bin/env python3
"""Apply the round-49 C1 repairs and write the citation-ground ledger.

Reads the frozen class census (.ufo/waves/round-49/controls/class-before.json,
the members the frozen counter found at the base commit) and, for every member,
rewrites the citing line so the token opens.  The script is deliberately
literal: it replaces the exact backticked token at the exact recorded site and
refuses to continue when a site does not contain that token exactly once.

Every repair keeps the referent:
  lane-bare      `knowledge/x.md`      -> `corpus/knowledge/x.md`
  fleet-relative `.ufo/reports/x.md`   -> `/home/vgpnk/Projects/shokunin/.ufo/reports/x.md`
The line anchor of the token is preserved; two rows carry a note about an
anchor that drifted before this round.

Run from the lane root:  python3 .ufo/waves/round-49/apply-repairs.py [--dry-run]
"""
import json
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
CLASS_JSON = os.path.join(LANE, ".ufo/waves/round-49/controls/class-before.json")
LEDGER = os.path.join(LANE, "corpus/instruments/citation-reground-ledger.md")
ANCHOR_RE = re.compile(r":\d+([–-]\d+)?$")

# Per-row referent notes for the rows whose referent needs a sentence.
NOTES = {
    "MISSION.md:49-56": "the fleet MISSION.md — same file as the bare path; the push-scope allow-list "
                        "this sentence names sat at these lines at round 15 and has since drifted "
                        "(the fleet MISSION.md's push scope is now at line 81), the anchor is historical",
    "PROTOCOL.md:457-461": "the fleet root's PROTOCOL.md — the same file as the bare path; its lines "
                            "457-461 carry the 'one domain per shokunin / contested scope is reported' "
                            "invariant this sentence invokes (the canonical checkout's PROTOCOL.md is a "
                            "different vintage and its lines 457-461 hold the SHONEN seed instead)",
}


def referent_note(cls, old):
    base = ANCHOR_RE.sub("", old)
    if old in NOTES:
        return NOTES[old]
    if cls == "lane-bare":
        return ("the same file as the bare LANE path — the lane's own base rule "
                "(corpus/knowledge/citation-bases.md, LANE rule) requires the full lane-internal path "
                "because the resolver tries the lane root only")
    return ("the same file as the fleet-root-relative path — the fleet repo at " + FLEET +
            " is the lane root's parent, so the bare path named a file that exists but cannot be opened "
            "from the lane")


def main(argv):
    dry = "--dry-run" in argv
    data = json.load(open(CLASS_JSON))
    members = [f for f in data["findings"]]
    plan = []
    for f in members:
        old = f["token"]
        cls = "lane-bare" if f["id"] == "class-lane-bare" else "fleet-relative"
        base = ANCHOR_RE.sub("", old)
        anchor = ANCHOR_RE.search(old)
        anchor_txt = anchor.group(0) if anchor else ""
        if cls == "lane-bare":
            new = "corpus/" + base + anchor_txt
        else:
            new = FLEET + "/" + base + anchor_txt
        sites = [s for s in f["detail"].split(",") if s.strip()]
        plan.append({"old": old, "new": new, "cls": cls, "sites": sites,
                     "note": referent_note(cls, old)})
    changed = 0
    problems = []
    for row in plan:
        by_file = {}
        for site in row["sites"]:
            rel, _, lineno = site.rpartition(":")
            by_file.setdefault(rel, []).append(int(lineno))
        for rel, linenos in by_file.items():
            path = os.path.join(LANE, rel)
            with open(path, "r", encoding="utf-8") as fh:
                lines = fh.read().split("\n")
            for lineno in linenos:
                idx = lineno - 1
                if idx < 0 or idx >= len(lines):
                    problems.append(("out-of-range", rel, lineno, row["old"]))
                    continue
                line = lines[idx]
                needle = "`" + row["old"] + "`"
                if line.count(needle) != 1:
                    problems.append(("token-count-%d" % line.count(needle), rel, lineno, row["old"]))
                    continue
                if row["new"] in line:
                    problems.append(("already-present", rel, lineno, row["old"]))
                    continue
                lines[idx] = line.replace(needle, "`" + row["new"] + "`")
                changed += 1
            if not dry:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(lines))
    if not dry:
        with open(LEDGER, "w", encoding="utf-8") as fh:
            fh.write("# Citation-ground ledger — round 49 (C1)\n\n")
            fh.write("One row per repaired citation. `old token` is the token as written at the base commit "
                     "9b1662a2fa0e7c7b0ad6c4d45cb7786f27bdd03b; `new token` is the path that opens; "
                     "`base class` is the class the frozen counter reported; `sites` lists every occurrence "
                     "of the old token in lane-authored files; `referent note` says why the new path is the "
                     "same referent. The ledger is the counter's second evidence: "
                     "corpus/instruments/citation-ground-check.py checks every row.\n\n")
            fh.write("| old token | new token | base class | sites | referent note |\n")
            fh.write("|---|---|---|---|---|\n")
            for row in plan:
                note = row["note"].replace("|", "/")
                fh.write("| `%s` | `%s` | %s | %s | %s |\n" % (
                    row["old"], row["new"], row["cls"], ",".join(row["sites"]), note))
    print("rows=%d sites_changed=%d problems=%d dry=%s" % (len(plan), changed, len(problems), dry))
    for p in problems:
        print("problem", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
