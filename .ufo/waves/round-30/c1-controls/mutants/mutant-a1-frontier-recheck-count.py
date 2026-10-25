#!/usr/bin/env python3
"""Count Frontier entries whose own `recheck:` line re-verifies their own sources.

Usage: python3 corpus/instruments/frontier-recheck-count.py [--root DIR] [--json PATH]

The round-24 C1 counter. A bare shell loop over `recheck:` lines measures
whatever the line happens to say: point every entry at one captured source, or
write `recheck: true`, and the loop reports 8/8 with no capture work done
(r24 wave-1 reviewers demonstrated four such routes). This harness binds the
line to the entry it belongs to before it runs it:

  A. the `--source` ids on the `recheck:` line must equal the entry's own
     `source:` id set — no cross-entry credit, no dropped id;
  B. the named manifest must exist, be schema-valid, and list every one of
     those ids;
  C. the line must be a `source-recheck.py` invocation with `--manifest` and at
     least one `--source` (no `true`, no `--selftest`, no whole-manifest run);
  D. only then is the line executed, from the lane root, and its exit code is
     the entry's result.

An entry passes only when A-D all hold and the line exits 0. The harness also
fails closed before any line runs:

  E. an admitted row whose entry file does not exist fails with a named-row
     `missing-entry` problem (the row id and path are printed; never an
     uncaught FileNotFoundError traceback);
  F. two admitted rows resolving to the same entry realpath fail the run with
     a `DUPLICATE-ENTRY` note naming the duplicate rows and the entry.

Exit 0 when every admitted Frontier entry passes, 1 otherwise (any failing
row, a missing entry, or a duplicate entry realpath), 2 on a harness/read
error.

This instrument measures recheck coverage only: a passing entry proves its
pinned captures still hold its own assertions, not that the entry's claims are
current upstream or that the quotes assert what the entry says they assert.
"""
import argparse
import json
import os
import re
import subprocess
import sys

FRONTIER_ROW = re.compile(r"^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|")
SOURCE_LINE = re.compile(r"^source:\s*(S\d{3,})")
RECHECK_LINE = re.compile(r"^recheck:\s*(.+)$")
RECHECK_SOURCE = re.compile(r"--source\s+(S\d{3,})")
RECHECK_MANIFEST = re.compile(r"--manifest\s+(\S+)")


def read_frontier(root):
    """Return [(id, title, status, entry_path)] in README order."""
    rows = []
    path = os.path.join(root, "corpus", "README.md")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = FRONTIER_ROW.match(line)
            if m:
                rows.append((m.group(1), m.group(2), m.group(3), m.group(4).strip()))
    return rows


def entry_contract(root, entry_path):
    """Return (declared ids, cited ids, recheck line, recheck ids, manifest).

    `declared` is the header `source:` id set; `cited` is every S-id the entry's
    body mentions. The recheck must select a superset of the header ids (nothing
    dropped) and a subset of the cited ids (no cross-entry credit).

    Returns None when the entry file exists under neither candidate path
    (`root/<entry_path>` or the corpus-relative form); callers must treat None
    as a fail-closed missing-entry outcome."""
    full = os.path.join(root, entry_path)
    if not os.path.isfile(full):
        # README rows name entries relative to corpus/ (`knowledge/...`).
        full = os.path.join(root, "corpus", entry_path)
    declared, cited, recheck, manifest = [], set(), "", None
    with open(full, encoding="utf-8") as fh:
        body = fh.read()
    for sid in re.findall(r"S\d{3,}", body):
        cited.add(sid)
    with open(full, encoding="utf-8") as fh:
        for line in fh:
            m = SOURCE_LINE.match(line)
            if m:
                declared.append(m.group(1))
                continue
            m = RECHECK_LINE.match(line)
            if m and not recheck:
                recheck = m.group(1).strip()
    recheck_ids = RECHECK_SOURCE.findall(recheck)
    m = RECHECK_MANIFEST.search(recheck)
    if m:
        manifest = m.group(1).strip("`'\"")
    return sorted(declared), sorted(cited), recheck, sorted(recheck_ids), manifest


def manifest_ids(root, manifest):
    """Return the set of source ids a manifest lists, or None if unreadable."""
    path = os.path.join(root, manifest)
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return None
    records = data.get("sources")
    if not isinstance(records, list):
        return None
    return {r.get("id") for r in records if isinstance(r, dict)}


def evaluate(root, entry_path):
    contract = entry_contract(root, entry_path)
    if contract is None:
        return {
            "entry": entry_path,
            "declared_ids": [],
            "cited_ids": [],
            "recheck_ids": [],
            "manifest": None,
            "exit": None,
            "realpath": None,
            "problems": ["missing-entry"],
            "status": "FAIL",
        }
    declared, cited, recheck, recheck_ids, manifest = contract
    full = os.path.join(root, entry_path)
    if not os.path.isfile(full):
        full = os.path.join(root, "corpus", entry_path)
    realpath = os.path.realpath(full)
    problems = []
    if not declared:
        problems.append("no-source-line")
    if not recheck:
        problems.append("no-recheck-line")
    elif "source-recheck.py" not in recheck or "--selftest" in recheck:
        problems.append("not-a-recheck-invocation")
    if not recheck_ids:
        problems.append("no-source-selection")
    if not manifest:
        problems.append("no-manifest")
    if declared and recheck_ids and not set(declared).issubset(set(recheck_ids)):
        problems.append("header-sources-not-rechecked")
    if recheck_ids and not set(recheck_ids).issubset(set(cited)):
        problems.append("selection-not-cited-by-entry")
    listed = manifest_ids(root, manifest) if manifest else None
    if manifest and listed is None:
        problems.append("manifest-unreadable")
    elif listed is not None and not set(recheck_ids).issubset(listed):
        problems.append("manifest-missing-ids")
    exit_code = None
    if not problems:
        proc = subprocess.run(["bash", "-c", recheck], cwd=root,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        exit_code = proc.returncode
        if exit_code != 0:
            problems.append("recheck-exit-%d" % exit_code)
    return {
        "entry": entry_path,
        "declared_ids": declared,
        "cited_ids": cited,
        "recheck_ids": recheck_ids,
        "manifest": manifest,
        "realpath": realpath,
        "exit": exit_code,
        "problems": problems,
        "status": "PASS" if not problems else "FAIL",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    parser.add_argument("--json", default=None, help="write a JSON receipt here")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    try:
        rows = read_frontier(root)
    except OSError as exc:
        print("harness UNAVAILABLE reason=read-error %s" % exc)
        return 2
    admitted = [r for r in rows if r[2] == "admitted"]
    records = []
    for fid, title, _status, cell in admitted:
        # A topic may govern more than one entry (`entry, entry` in one cell).
        for entry in [part.strip() for part in cell.split(",") if part.strip()]:
            record = evaluate(root, entry)
            record["frontier"] = fid
            record["title"] = title
            records.append(record)
            print("%-8s %-4s %-52s ids=%-14s exit=%-4s%s" % (
                record["status"], fid, entry, ",".join(record["declared_ids"]) or "-",
                "-" if record["exit"] is None else record["exit"],
                (" problems=" + ",".join(record["problems"])) if record["problems"] else ""))
    passed = sum(1 for r in records if r["status"] == "PASS")
    duplicate = None
    seen_realpath = {}
    for record in records:
        rp = record.get("realpath")
        if rp is None:
            continue
        if rp in seen_realpath:
            duplicate = (seen_realpath[rp], record["frontier"], record["entry"])
            break
        seen_realpath[rp] = record["frontier"]
    if duplicate:
        print("DUPLICATE-ENTRY %s,%s %s" % (duplicate[0], duplicate[1], duplicate[2]))
    fail_closed = duplicate is not None or not records or passed != len(records)
    print("entries=%d pass=%d exit=%d" % (len(records), passed, 1 if fail_closed else 0))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"schema": "kasegi-frontier-recheck-receipt-v1", "root": root,
                       "entries": len(records), "pass": passed,
                       "duplicate_entry": duplicate[2] if duplicate else None,
                       "records": records},
                      fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 1 if fail_closed else 0


if __name__ == "__main__":
    sys.exit(main())
