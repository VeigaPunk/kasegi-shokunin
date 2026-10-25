#!/usr/bin/env python3
"""Independent re-derivation of the C1 `recheck:` predicate, round 25.

Written from the frozen predicate text in .ufo/waves/round-25/claims.json, not
from corpus/instruments/recheck-audit.py (which is deliberately not read by
this script). Throwaway verification artefact; no production effect.

Predicate re-derived here:
  Every `recheck:` line of every corpus/knowledge/*.md entry is one shell
  command that
    (a) parses under `bash -n`,
    (b) yields the same exit status AND the same combined stdout+stderr digest
        when run from the lane root and from a foreign cwd (/),
    (c) names at least one lane-relative `corpus/` path or a `~/Projects/`
        base test, and every `corpus/` path it names exists under the lane root.

Usage:
  independent-recheck.py --base <rev> --scratch <dir> [--json <out>] [--root DIR]
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
FOREIGN = "/"
KNOWLEDGE = "corpus/knowledge"
TIMEOUT = 300

# A `corpus/...` path token, at a token boundary. Trailing sentence punctuation is
# stripped after the match (prose lines end with "(fails closed today: ...)").
CORPUS_TOKEN = re.compile(r"(?<![A-Za-z0-9._/%-])corpus/[A-Za-z0-9._%+-][A-Za-z0-9._%+/-]*")
PROJECTS_TOKEN = re.compile(r"(?<![A-Za-z0-9._/%-])~/Projects/[A-Za-z0-9._%+-][A-Za-z0-9._%+/-]*")
TRAILING = ".,;:)]}\"'"


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, **kw)


def base_entries(root, rev):
    out = sh(["git", "-C", root, "ls-tree", "--name-only", rev, KNOWLEDGE + "/"])
    if out.returncode != 0:
        sys.exit("git ls-tree failed: " + out.stderr.decode("utf-8", "replace"))
    # ls-tree with a pathspec prints repo-root-relative paths.
    return sorted(os.path.basename(n) for n in out.stdout.decode().split("\n")
                  if n.endswith(".md"))


def export_base(root, rev, scratch):
    """Export base corpus/knowledge/*.md into scratch/base/corpus/knowledge."""
    dest = os.path.join(scratch, "base", KNOWLEDGE)
    os.makedirs(dest, exist_ok=True)
    for name in base_entries(root, rev):
        blob = sh(["git", "-C", root, "show", f"{rev}:{KNOWLEDGE}/{name}"])
        if blob.returncode != 0:
            sys.exit(f"git show failed for {name}")
        with open(os.path.join(dest, name), "wb") as fh:
            fh.write(blob.stdout)
    return dest


def recheck_command(path):
    """First line matching ^recheck: in the entry; text after the marker."""
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            m = re.match(r"\s*recheck:[ \t]?(.*)$", line.rstrip("\n"))
            if m:
                return m.group(1).strip()
    return None


def combined_digest(stdout, stderr):
    h = hashlib.sha256()
    h.update(b"OUT\0")
    h.update(stdout)
    h.update(b"\0ERR\0")
    h.update(stderr)
    return h.hexdigest()


def run(cmd, cwd):
    try:
        p = subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True,
                           timeout=TIMEOUT)
        return p.returncode, p.stdout, p.stderr, None
    except subprocess.TimeoutExpired:
        return None, b"", b"", "timeout"


def path_limb(cmd, root):
    named = []
    for m in CORPUS_TOKEN.finditer(cmd):
        tok = m.group(0).rstrip(TRAILING)
        if tok not in named:
            named.append(tok)
    missing = [t for t in named if not os.path.exists(os.path.join(root, t))]
    projects = [m.group(0).rstrip(TRAILING) for m in PROJECTS_TOKEN.finditer(cmd)]
    has_base_test = bool(projects)
    # (c): at least one lane-relative corpus/ path OR a ~/Projects/ base test,
    #      and every named corpus/ path exists.
    ok = (bool(named) or has_base_test) and not missing
    return ok, named, missing, projects


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--json")
    ap.add_argument("--root", default=LANE, help="root the commands run from")
    ap.add_argument("--git-root", default=LANE, help="repo the base blobs are read from")
    ap.add_argument("--foreign", default=FOREIGN)
    args = ap.parse_args()

    os.makedirs(args.scratch, exist_ok=True)
    base_dir = export_base(args.git_root, args.base, args.scratch)
    names = sorted(os.listdir(base_dir))

    rows = []
    for name in names:
        cmd = recheck_command(os.path.join(base_dir, name))
        row = {"entry": name, "command": cmd}
        if cmd is None or cmd == "":
            row.update({"limbs": {"parse": False, "cwd": False, "paths": False},
                        "pass": False, "class": "missing-recheck"})
            rows.append(row)
            continue

        parse = sh(["bash", "-n", "-c", cmd]).returncode == 0

        lane_exit, lane_out, lane_err, lane_errkind = run(cmd, args.root)
        foreign_exit, f_out, f_err, f_errkind = run(cmd, args.foreign)
        lane_digest = combined_digest(lane_out, lane_err)
        foreign_digest = combined_digest(f_out, f_err)
        cwd_ok = (lane_errkind is None and f_errkind is None
                  and lane_exit == foreign_exit and lane_digest == foreign_digest)

        paths_ok, named, missing, projects = path_limb(cmd, args.root)

        ok = parse and cwd_ok and paths_ok
        limbs = {"parse": parse, "cwd": cwd_ok, "paths": paths_ok}
        row.update({
            "limbs": limbs,
            "missing_paths": missing,
            "corpus_paths": named,
            "projects_paths": projects,
            "lane_exit": lane_exit,
            "foreign_exit": foreign_exit,
            "lane_output_sha256": lane_digest,
            "foreign_output_sha256": foreign_digest,
            "error": lane_errkind or f_errkind,
            "pass": ok,
            "class": "passing" if ok else "failing",
        })
        rows.append(row)

    passed = [r for r in rows if r["pass"]]
    failing = [r for r in rows if not r["pass"]]
    doc = {
        "root": args.root,
        "foreign_cwd": args.foreign,
        "base_revision": args.base,
        "lines": len(rows),
        "pass": len(passed),
        "fail_closed": len(failing),
        "failing_limbs": {
            "parse": sum(1 for r in rows if not r["limbs"]["parse"]),
            "cwd": sum(1 for r in rows if r["limbs"]["parse"] and not r["limbs"]["cwd"]),
            "paths": sum(1 for r in rows if not r["limbs"]["paths"]),
        },
        "entries": rows,
    }
    text = json.dumps(doc, indent=1, sort_keys=True)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(f"lines={doc['lines']} pass={doc['pass']} fail-closed={doc['fail_closed']}")
    for r in rows:
        if not r["pass"]:
            limb = "+".join(k for k, v in r["limbs"].items() if not v) or "?"
            print(f"  FAIL {r['entry']} limb={limb} "
                  f"exit(lane={r.get('lane_exit')},foreign={r.get('foreign_exit')}) "
                  f"missing={r.get('missing_paths')}")
    return 0 if doc["pass"] == doc["lines"] else 1


if __name__ == "__main__":
    sys.exit(main())
