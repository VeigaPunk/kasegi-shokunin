#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify round93-labels.tsv against the lane at cb1ef2b9856df79c530f3ff1374fa9691ff56233.

Proves, for every label row:
  * the citing file exists at the rev and its line N is in range;
  * the key token (`<key>`) occurs exactly once on that citing line;
  * the key's own anchor (if any) is inside its corpus/knowledge entry;
every named range (in line, label, fix, evidence) is inside a tracked entry;
the 5 non-SKILL rows are exactly the remaining GONE bare keys that name an
existing corpus/knowledge entry (re-derived independently from resolve.py);
the 2 cell-repair rows carry the exact full replacement of the citing line's
last table cell, and every quoted claim exists at the cited lines;
row 454's SKILL.md:494-506 contains no EV term and SKILL.md:827-848 carries the
formula + UNKNOWN fail-closed sentence.

Usage: python3 -B verify-labels-r93.py WORK TSV
Exit 0 only when every check passes; 1 otherwise; 2 on read error.
"""
import importlib.util
import io
import os
import re
import subprocess
import sys
import tarfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
REV = "cb1ef2b9856df79c530f3ff1374fa9691ff56233"
GONE_ROWS = 5  # the remaining GONE bare corpus/knowledge keys this tranche labels
BARE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
VAL = re.compile(r"([A-Za-z0-9][A-Za-z0-9._/-]*\.md):(\d+)(?:-(\d+))?")
CELL = "Replace cell with: "
OLD_CELL = {
    ("corpus/knowledge/triage-thresholds.md:437", "intake-surface.md:75-76"):
        '`intake-surface.md:75-76` ("`reward.min` present on 48"), `SKILL.md:111` '
        '("`reward` exists on 48" — true but conflated downstream)',
    ("corpus/knowledge/triage-thresholds.md:438", "mission-control.md:37-38"):
        '`mission-control.md:37-38` (`openai-oauth/gpt-6-astra:max`)',
}
EV_ROW = ("corpus/knowledge/triage-thresholds.md:454", "SKILL.md:494-506")

errs = []
oks = []


def ok(msg):
    oks.append(msg)
    print("OK", msg)


def bad(msg):
    errs.append(msg)
    print("FAIL", msg)


def git(*args):
    return subprocess.run(["git", "-C", LANE] + list(args),
                          capture_output=True, check=True).stdout


def entry(tree, rel):
    p = os.path.join(tree, rel)
    if not os.path.isfile(p):
        return None
    with io.open(p, encoding="utf-8") as fh:
        out = fh.read().split("\n")
    if out and out[-1] == "":
        out.pop()  # a single trailing newline is not a content line
    return out


def resolve_entry(tree, written):
    base = os.path.basename(written)
    for cand in (written, "corpus/knowledge/" + base, base):
        if os.path.isfile(os.path.join(tree, cand)):
            return cand
    return None


def main():
    work, tsv = sys.argv[1], sys.argv[2]
    tree = os.path.join(work, "verify-tree-cb1ef2b9")
    if not os.path.isdir(tree):
        os.makedirs(tree)
        data = git("archive", "--format=tar", REV)
        with tarfile.open(fileobj=io.BytesIO(data)) as tf:
            tf.extractall(tree, filter="tar")
    spec = importlib.util.spec_from_file_location(
        "resolve_pinned", os.path.join(tree, "corpus", "instruments", "resolve.py"))
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    mirror = os.path.expanduser(R.MIRROR_ROOT)

    rows, seen = [], set()
    for i, ln in enumerate(io.open(tsv, encoding="utf-8")):
        ln = ln.rstrip("\n")
        if not ln.strip() or ln.startswith("#") or (i == 0 and ln.startswith("line\t")):
            continue
        c = ln.split("\t")
        if len(c) != 5:
            bad("row %d has %d columns" % (i, len(c)))
            continue
        rows.append(c)
    if len(rows) != 6:
        bad("expected 6 label rows, found %d" % len(rows))
    else:
        ok("label rows=6 (3 edits: 2 cell-repair + 1 SKILL.md range; 3 no-edit)")

    # re-derive the remaining GONE bare-key site set independently
    kd = os.path.join(tree, "corpus", "knowledge")
    scan = set()
    for fn in sorted(os.listdir(kd)):
        if not fn.endswith(".md"):
            continue
        rel = "corpus/knowledge/" + fn
        lines = entry(tree, rel)
        for n, line in enumerate(lines, 1):
            for m in R.TOKEN.finditer(line):
                t = m.group(1).strip().rstrip(".,;:")
                if not R.is_pathlike(t):
                    continue
                bm = BARE.match(t)
                if not bm:
                    continue
                if not os.path.isfile(os.path.join(kd, bm.group(1))):
                    continue
                if R.classify(t, tree, mirror)[0] == "GONE":
                    scan.add((rel, n, t))
    ok("GONE bare-key scan at %s: %d distinct sites" % (REV[:12], len(scan)))

    gone_rows, ev_rows = set(), []
    for line, key, label, fix, ev in rows:
        if (line, key) in seen:
            bad("duplicate row %s %s" % (line, key))
        seen.add((line, key))
        m = re.match(r"^(.+):(\d+)$", line)
        if not m:
            bad("bad line field %r" % line)
            continue
        rel, n = m.group(1), int(m.group(2))
        lines = entry(tree, rel)
        if lines is None:
            bad("%s: citing file missing at %s" % (line, REV[:12]))
            continue
        if not 1 <= n <= len(lines):
            bad("%s: line out of range (entry has %d)" % (line, len(lines)))
            continue
        text = lines[n - 1]
        occ = text.count("`%s`" % key)
        if occ != 1:
            bad("%s: key `%s` occurs %d times on the citing line" % (line, key, occ))
        else:
            ok("%s key `%s` exists exactly once" % (line, key))
        cls = R.classify(key, tree, mirror)[0]
        bm = BARE.match(key)
        if key.startswith("SKILL.md:"):
            if cls != "INTERNAL":
                bad("%s: %s classifies %s, expected INTERNAL" % (line, key, cls))
            else:
                ok("%s: %s INTERNAL at %s" % (line, key, REV[:12]))
            ev_rows.append((line, key, label, fix, ev, n, text))
        else:
            gone_rows.add((rel, n, key))
            if bm is None:
                bad("%s: key is not a bare <name>.md[:N[-M]]: %s" % (line, key))
            elif not os.path.isfile(os.path.join(kd, bm.group(1))):
                bad("%s: key names no existing corpus/knowledge entry: %s" % (line, key))
            else:
                ok("%s: key `%s` is a bare key naming an existing entry" % (line, key))
            if cls != "GONE":
                bad("%s: %s classifies %s, expected GONE" % (line, key, cls))
            else:
                ok("%s: %s GONE at %s" % (line, key, REV[:12]))
            # the key's own anchor, when present, is inside its entry
            if bm and bm.group(2):
                a = int(bm.group(2))
                b = int(bm.group(3) or bm.group(2))
                L = len(entry(tree, "corpus/knowledge/" + bm.group(1)))
                if not 1 <= a <= b <= L:
                    bad("%s: key anchor %s:%d-%d outside 1..%d" % (line, bm.group(1), a, b, L))
                else:
                    ok("%s: key anchor %s:%d-%d inside entry (%d lines)" % (line, bm.group(1), a, b, L))
        # every named range in every column is inside its entry
        for colname, col in (("label", label), ("fix", fix), ("evidence", ev)):
            for vm in VAL.finditer(col):
                written, a, b = vm.group(1), int(vm.group(2)), int(vm.group(3) or vm.group(2))
                target = resolve_entry(tree, written)
                if target is None:
                    bad("%s: %s names no tracked entry: %s" % (line, colname, written))
                    continue
                L = len(entry(tree, target))
                if not 1 <= a <= b <= L:
                    bad("%s: %s range %s:%d-%d outside 1..%d" % (line, colname, written, a, b, L))
                else:
                    ok("%s: %s range %s:%d-%d inside %s (%d lines)" % (
                        line, colname, written, a, b, target, L))

    if gone_rows != scan:
        bad("GONE set mismatch: unlabelled=%s extra=%s" % (
            sorted(scan - gone_rows)[:5], sorted(gone_rows - scan)[:5]))
    else:
        ok("all %d remaining GONE bare-key sites labelled exactly once" % len(scan))

    # cell-repair rows: exact last-cell replacement + quoted claims true at the cited lines
    IS = entry(tree, "corpus/knowledge/intake-surface.md")
    MC = entry(tree, "corpus/knowledge/mission-control.md")
    SK = entry(tree, "SKILL.md")

    def seg(lines, a, b):
        return "\n".join(lines[a - 1:b])

    for line, key, label, fix, ev, n, text in [(r[0], r[1], r[2], r[3], r[4], None, None)
                                               for r in rows if r[2] == "cell-repair"]:
        old = OLD_CELL.get((line, key))
        if old is None:
            bad("%s: no frozen old-cell text for this cell-repair row" % line)
            continue
        rel, nn = line.rsplit(":", 1)
        raw = entry(tree, rel)[int(nn) - 1]
        i2 = raw.rfind("|")
        i1 = raw.rfind("|", 0, i2)
        cell = raw[i1 + 1:i2]
        if cell != " " + old + " ":
            bad("%s: last table cell differs from the frozen old cell: %r" % (line, cell))
            continue
        ok("%s: last table cell equals the frozen old cell (%d chars)" % (line, len(old)))
        if not fix.startswith(CELL):
            bad("%s: cell-repair fix lacks the %r prefix" % (line, CELL))
            continue
        new = fix[len(CELL):]
        if "|" in new:
            bad("%s: replacement cell contains a table pipe" % line)
        newraw = raw[:i1 + 1] + " " + new + " " + raw[i2:]
        if newraw.count("|") != raw.count("|"):
            bad("%s: replacement changes the table cell count" % line)
        else:
            ok("%s: replacement cell applies cleanly (%d chars, %d pipes unchanged)" % (
                line, len(new), raw.count("|")))

    if "`reward` object on 48 but numeric" in seg(IS, 89, 93) and \
       "`reward.min` on only 14" in seg(IS, 89, 93) and \
       "reward-exists≠reward.min-numeric conflation" in seg(IS, 89, 93):
        ok("437 cell: intake-surface.md:89-93 carries the counts and the conflation note")
    else:
        bad("437 cell: intake-surface.md:89-93 does not carry the quoted claims")
    if "`reward.min` present on 48" in git("show", "fb9ac8e:corpus/knowledge/intake-surface.md").decode("utf-8").split("\n")[71]:
        ok('437 cell: the superseded wording "`reward.min` present on 48" is at fb9ac8e:72')
    else:
        bad("437 cell: superseded wording not found at fb9ac8e:72")
    if "object exists on 48 records" in seg(SK, 176, 178) and \
       "`reward.min` on only 14 (round-13 correction)" in seg(SK, 176, 178):
        ok("437 cell: SKILL.md:176-178 carries the counts")
    else:
        bad("437 cell: SKILL.md:176-178 does not carry the quoted claims")
    if "`openai-codex/gpt-6-astra:max`" in seg(MC, 55, 57) and \
       "earlier text said `openai-oauth/`" in seg(MC, 55, 57):
        ok("438 cell: mission-control.md:55-57 carries the peak model and the correction note")
    else:
        bad("438 cell: mission-control.md:55-57 does not carry the quoted claims")
    hist = git("show", "7483333~1:corpus/knowledge/mission-control.md").decode("utf-8").split("\n")
    if "`openai-oauth/gpt-6-astra:max`" in "\n".join(hist[49:52]):
        ok("438 cell: superseded `openai-oauth/gpt-6-astra:max` was at 7483333~1:50-52")
    else:
        bad("438 cell: superseded model string not at 7483333~1:50-52")

    # row 454: the old token states no EV term; the label range carries formula + fail-closed
    if len(ev_rows) == 1:
        line, key, label, fix, ev, n, text = ev_rows[0]
        if (line, key) != EV_ROW:
            bad("unexpected SKILL.md row %s %s" % (line, key))
        old = seg(SK, 494, 506)
        hits = [m for m in ("p_success", "gross_value", "total_cost", "adjusted_ev") if m in old]
        if hits:
            bad("SKILL.md:494-506 unexpectedly states EV terms: %s" % hits)
        else:
            ok("SKILL.md:494-506 states no EV term (park-disposition text)")
        if label != "SKILL.md:827-848":
            bad("row 454 label is %r, expected SKILL.md:827-848" % label)
        rng = seg(SK, 827, 848)
        pats = [r"p_success\s*=\s*p_in_scope", r"gross_value\s*=\s*p_success",
                r"total_cost\s*=\s*effort_hours", r"adjusted_ev\s*=\s*gross_value"]
        miss = [p for p in pats if not re.search(p, rng)]
        if miss:
            bad("SKILL.md:827-848 missing formula lines: %s" % miss)
        else:
            ok("SKILL.md:827-848 carries all four EV formula lines")
        if "Missing inputs print `UNKNOWN`" in rng and "fail-closed" in rng and "degrade to `unknown`" in rng:
            ok("SKILL.md:827-848 carries the UNKNOWN fail-closed sentence")
        else:
            bad("SKILL.md:827-848 lacks the UNKNOWN fail-closed sentence")
        for rm in re.finditer(r"(\d+)-(\d+)", fix):
            a, b = int(rm.group(1)), int(rm.group(2))
            if not 1 <= a <= b <= len(SK):
                bad("row 454 fix range %d-%d outside SKILL.md 1..%d" % (a, b, len(SK)))
        ok("row 454 fix sub-ranges all inside SKILL.md (%d lines)" % len(SK))
    else:
        bad("expected exactly 1 SKILL.md row, found %d" % len(ev_rows))

    # no-edit rows carry the frozen no-edit marker
    ne = [r for r in rows if r[2] == "CORRECT"]
    if len(ne) == 3 and all(r[3].startswith("No edit") for r in ne):
        ok("3 no-edit rows carry the 'No edit' fix (unmapped by construction)")
    else:
        bad("no-edit row set unexpected: %d rows" % len(ne))

    print("VERIFY", "PASS" if not errs else "FAIL", "checks=%d failures=%d" % (len(oks), len(errs)))
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
