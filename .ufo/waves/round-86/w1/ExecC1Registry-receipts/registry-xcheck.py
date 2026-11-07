#!/usr/bin/env python3
"""Kasegi round-86 C1 map cross-check against the lane registry (corpus/SOURCES.md) at base rev.

For each of the 203 entries in the frozen repair map:
  (a) reads the S-id's row in corpus/SOURCES.md at REV and extracts the capture
      path named in the anchor cell (`capture corpus/source-snapshots/round-N/Sxxx.txt`)
      OR a bare `corpus/source-snapshots/round-N/Sxxx.txt` mention in that cell
      when the capture keyword is absent (two phrasings in the registry);
  (b) compares it with the map value's path;
  (c) for each knowledge file citing the key at REV (backticked token, resolve.py
      TOKEN/is_pathlike semantics), checks whether that file's front-matter
      (`source:` ids in the first 15 lines) includes that S-id;
  (d) for anchored values, prints the cited snapshot line(s) via plain line read
      (anchorcheck.py verifies `path:NN[-MM]` cites in markdown; here the value
      already names the snapshot, so the cited lines are read directly).

Output: one TSV row per key:
  key, value, registry_capture, registry_match(yes/no/absent), cited_by_files,
  file_cites_sid(yes/no), first 100 chars of the anchored line (anchored only).

Usage: python3 -B registry-xcheck.py --lane LANE --rev REV --map MAP --out TSV
"""
import argparse
import json
import re
import subprocess
import sys

REV_DEFAULT = "d7296645c2cd9f631329fa8e2f38328a4c9c89a5"
MAP_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/c1/repair-map.json"
LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"

TOKEN = re.compile(r"`([^`\n]+)`")
BARE_SNAP = re.compile(r"^(S\d{3,}\.txt)(?::(\d+)(?:-(\d+))?)?$")
CAPTURE_RE = re.compile(r"capture (corpus/source-snapshots/round-\d+/S\d{3,}\.txt)")
MENTION_RE = re.compile(r"(corpus/source-snapshots/round-\d+/S\d{3,}\.txt)")


def git_text(lane, spec):
    r = subprocess.run(["git", "-C", lane, "show", spec], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout


def registry_captures(lane, rev):
    text = git_text(lane, "%s:corpus/SOURCES.md" % rev)
    if text is None:
        raise SystemExit("cannot read corpus/SOURCES.md at %s" % rev)
    caps = {}
    for line in text.splitlines():
        m = re.match(r"\| (S\d+) \|", line)
        if not m:
            continue
        sid = m.group(1)
        # Anchor cell is column 7 (1-based table columns: id, source, kind,
        # tier, scope, anchor, teaches, status, opened, recheck, used-by).
        cells = [c.strip() for c in line.split("|")]
        anchor = cells[6] if len(cells) > 6 else ""
        mm = CAPTURE_RE.search(anchor)
        found = [mm.group(1)] if mm else None
        if found is None:
            found = sorted(set(MENTION_RE.findall(anchor)))
        caps[sid] = found if found else None
    return caps


def cited_by(lane, rev):
    names = [p for p in subprocess.run(
        ["git", "-C", lane, "ls-tree", "-r", "--name-only", rev, "corpus/knowledge/"],
        capture_output=True, text=True).stdout.split("\n")
        if p.endswith(".md")]
    out = {}
    front = {}
    for rel in sorted(names):
        t = git_text(lane, "%s:%s" % (rev, rel))
        if t is None:
            continue
        lines = t.splitlines()
        front[rel] = "\n".join(lines[:15])
        for line in lines:
            for m in TOKEN.finditer(line):
                x = m.group(1).strip().rstrip(".,;:")
                if BARE_SNAP.match(x):
                    out.setdefault(x, set()).add(rel)
    return out, front


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=LANE_DEFAULT)
    ap.add_argument("--rev", default=REV_DEFAULT)
    ap.add_argument("--map", default=MAP_DEFAULT)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rmap = json.load(open(a.map, encoding="utf-8"))
    reg = registry_captures(a.lane, a.rev)
    cites, front = cited_by(a.lane, a.rev)

    rows = []
    counts = {"yes": 0, "no": 0, "absent": 0, "sid_yes": 0, "sid_no": 0,
              "anchored_lines": 0, "keys": 0, "files_checked": 0}
    line_cache = {}
    for key in sorted(rmap):
        value = rmap[key]
        sid = key.split(".")[0]
        caps = reg.get(sid)
        if caps is None:
            regcap, match = "absent", "absent"
        else:
            # Map value is `corpus/source-snapshots/round-N/Sxxx.txt[:anchor]`;
            # strip the numeric anchor to get the value path.
            vpath = re.sub(r"(:\d+(?:-\d+)?)$", "", value) if re.search(r"\.txt:\d", value) else value
            regcap = ",".join(caps)
            match = "yes" if caps == [vpath] else "no"
            counts[match] += 1
        if caps is None:
            counts["absent"] += 1
        files = sorted(cites.get(key, set()))
        counts["files_checked"] += len(files)
        sid_ok = all(sid in front.get(f, "") for f in files) if files else False
        if files:
            counts["sid_yes" if sid_ok else "sid_no"] += 1
        # (d) anchored line(s): read from the lane working tree (frozen paths)
        km = BARE_SNAP.match(key)
        anchored = ""
        if km and km.group(2):
            lo = int(km.group(2))
            hi = int(km.group(3)) if km.group(3) else lo
            vpath = re.sub(r"(:\d+(?:-\d+)?)$", "", value)
            if vpath not in line_cache:
                with open("%s/%s" % (a.lane, vpath), encoding="utf-8") as fh:
                    line_cache[vpath] = fh.read().splitlines()
            lines = line_cache[vpath]
            seg = lines[lo - 1:hi] if 1 <= lo <= len(lines) else []
            anchored = " | ".join(s.strip() for s in seg)[:100]
            if anchored:
                counts["anchored_lines"] += 1
        counts["keys"] += 1
        rows.append("\t".join([
            key, value, regcap, match,
            ",".join(files) if files else "none",
            ("yes" if sid_ok else "no") if files else "n/a",
            anchored,
        ]))

    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("key\tvalue\tregistry_capture\tregistry_match\tcited_by_files\tfile_cites_sid\tanchored_line_first100\n")
        for r in rows:
            fh.write(r + "\n")
    print("keys=%d registry_yes=%d registry_no=%d registry_absent=%d files_sid_yes=%d files_sid_no=%d anchored_lines=%d files_checked=%d" % (
        counts["keys"], counts["yes"], counts["no"], counts["absent"],
        counts["sid_yes"], counts["sid_no"], counts["anchored_lines"], counts["files_checked"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
