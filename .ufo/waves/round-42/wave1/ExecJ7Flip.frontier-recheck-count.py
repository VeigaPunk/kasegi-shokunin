#!/usr/bin/env python3
"""Count Frontier entries whose own `recheck:` line re-verifies their own sources.

Usage: python3 corpus/instruments/frontier-recheck-count.py [--root DIR] [--json PATH]
       python3 corpus/instruments/frontier-recheck-count.py --selftest [--scratch DIR]

The round-24 C1 counter. A bare shell loop over `recheck:` lines measures
whatever the line happens to say: point every entry at one captured source, or
write `recheck: true`, and the loop reports 8/8 with no capture work done
(r24 wave-1 reviewers demonstrated four such routes). This harness binds the
line to the entry it belongs to before it runs it:

  A. the `--source` ids on the `recheck:` line must equal the entry's own
     declared source set, in BOTH directions — no dropped id (a declared
     source the line does not re-verify) and no undeclared id (a line that
     re-verifies a source the entry never declares, e.g. a line copied from
     another entry, or a source left credentialed by a bare prose mention after
     its declaration line was dropped);
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

Rule G — the frontier census — enumerates EVERY `| F<n> |` row of
`corpus/README.md`, whatever its status cell, so a row can never drop out of the
count unseen. A row fails the run when its status cell is not `admitted`
(`status-not-admitted`), when it is admitted but owns no PASS record
(`missing-pass-line`), and when it is bound to a source id the registry
`corpus/SOURCES.md` does not declare (`source-id-absent:<id>`); every row's
bound id set is its README `sources` cell plus the ids its entries declare. The
census prints one `FRONTIER-PASS <id> ids=<ids>` or `FRONTIER-FAIL <id>
status=<status> ids=<ids> problems=<...>` line per row BEFORE the per-entry
records, so the row set is auditable independently of the record count — the
round-41 status flip (one row's cell changed away from `admitted`, the row
silently vanished and the count self-consistently greened) is rejected here. A
row that is not admitted still contributes one FAIL record per entry cell, so
`entries=` counts the raw row set and never shrinks under a status flip. The
registry limb is skipped, and reported as `registry=absent`, when the root
carries no `corpus/SOURCES.md` (a miniature fixture lane) — a root WITH a
registry must declare every id its rows bind.

Rule A's two directions print different problem names so a receipt names the
limb that fired: `header-sources-not-rechecked` (a declared id missing from the
line's `--source` selections; the name is kept from the round-31 contract and
the limb now covers the whole declared set) and
`selection-not-declared-by-entry` (a `--source` id the entry never declares). A
selection that is not even mentioned in the entry text stays
`selection-not-cited-by-entry`.

The declared set is the union of the entry's two declaration shapes, both of
which the corpus uses: a header `source:` line per source (F09/F10/F13/F14) and
a per-source evidence list item that starts with the id, `- S002,
"Assessment": "…"` (the round-24 F01–F05 entries, whose single header line
declares the primary source and whose evidence list declares the rest). A
capture-path mention in prose or in a blockquote attribution (`S050.txt:70`) is
a reference, not a declaration. Measured residue of that shape rule: for the
five evidence-list entries a header `source:` line can be dropped without rule
A firing, because the id stays declared by its evidence bullets; those entries
lose only the header's URL/section provenance, not the entry↔source binding.

Exit 0 when every admitted Frontier entry passes, 1 otherwise (any failing
row, a missing entry, or a duplicate entry realpath), 2 on a harness/read
error.

`--selftest` runs this file as a subprocess against six fixture lanes — one per
limb of rule A, both declaration shapes, and the citation limb — and prints a
`selftest case=<name> exit=<N> want=<N> verdict=<pass|fail>` line per case plus
`selftest cases=N failures=F`; it exits 0 only when F=0. The fixtures carry
their own stub `source-recheck.py` and manifest, so the selftest measures the
harness's binding rules and never the lane. `bidirectional-holds` pins the pass
path; `selection-not-declared` is the reverse direction (an extra `--source`
mentioned in prose only must fail); `header-source-not-rechecked` is the
forward direction; `evidence-list-declares-selection` and
`evidence-declared-not-rechecked` cover the evidence-list declaration shape on
the pass and forward-fail sides; and
`selection-neither-declared-nor-mentioned` asserts both problems, in that
order. Scratch defaults to `$HYAKU_SCRATCH`, then `$TMPDIR`, then
`/fast/scratch/hyaku`, and is removed before exit.

This instrument measures recheck coverage only: a passing entry proves its
pinned captures still hold its own assertions, not that the entry's claims are
current upstream or that the quotes assert what the entry says they assert.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FRONTIER_ROW = re.compile(r"^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|")
FRONTIER_SOURCES = re.compile(r"^\|\s*(F\d+)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*([^|]*?)\s*\|")
REGISTRY_ROW = re.compile(r"^\|\s*(S\d{3,})\s*\|", re.MULTILINE)
SOURCE_LINE = re.compile(r"^source:\s*(S\d{3,})")
EVIDENCE_LINE = re.compile(r"^(?:[-*]|\d+[.)])\s+(S\d{3,})\b")
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


def read_frontier_sources(root):
    """Return {row id: sorted source ids its README `sources` cell names}."""
    cells = {}
    path = os.path.join(root, "corpus", "README.md")
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = FRONTIER_SOURCES.match(line)
            if m:
                cells[m.group(1)] = sorted(set(re.findall(r"S\d{3,}", m.group(2))))
    return cells


def read_registry_ids(root):
    """Return the source ids corpus/SOURCES.md registers, or None when the root
    carries no registry (a miniature fixture lane has none, and then the
    registry limb of rule G is not decidable and is reported, not applied)."""
    path = os.path.join(root, "corpus", "SOURCES.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return None
    return set(REGISTRY_ROW.findall(text))


def entry_contract(root, entry_path):
    """Return (declared ids, cited ids, recheck line, recheck ids, manifest,
    evidence ids).

    `declared` is the header `source:` id set; `evidence` is the subset of ids
    the entry declares in its own per-source evidence list (a list item that
    starts with an S-id, `- S002, "Assessment": "…"`). Together they are the
    entry's declared source set — the two declaration shapes the corpus uses
    (one header line per source, as F09/F10/F13/F14 do, or one evidence bullet
    per source, as the round-24 F01–F05 entries do). `cited` is the set of S-ids
    the entry mentions outside those declaration lines — prose, blockquote
    attributions and evidence items — so the recheck line's own `--source` ids
    cannot satisfy the citation limb by construction (M33-6 / R9).

    The recheck must select exactly the declared set (`declared ∪ evidence ==
    recheck_ids`, both directions: no dropped id, no undeclared id) and a
    subset of the cited ids (no cross-entry credit). A bare capture-path
    mention in prose or in a blockquote attribution (`S050.txt:70`) is a
    reference, not a declaration.

    Returns None when the entry file exists under neither candidate path
    (`root/<entry_path>` or the corpus-relative form); callers must treat None
    as a fail-closed missing-entry outcome."""
    full = os.path.join(root, entry_path)
    if not os.path.isfile(full):
        # README rows name entries relative to corpus/ (`knowledge/...`).
        full = os.path.join(root, "corpus", entry_path)
    if not os.path.isfile(full):
        return None
    declared, evidence, cited, recheck, manifest = [], [], set(), "", None
    with open(full, encoding="utf-8") as fh:
        for line in fh:
            m = SOURCE_LINE.match(line)
            if m:
                declared.append(m.group(1))
                continue
            m = EVIDENCE_LINE.match(line)
            if m:
                evidence.append(m.group(1))
            m = RECHECK_LINE.match(line)
            if m:
                if not recheck:
                    recheck = m.group(1).strip()
                continue
            # A declaration line is not evidence that the entry *cites* the
            # source: counting the recheck line's own `--source` ids as
            # citation made this limb vacuous by construction (M33-6 / R9).
            for sid in re.findall(r"S\d{3,}", line):
                cited.add(sid)
    recheck_ids = RECHECK_SOURCE.findall(recheck)
    m = RECHECK_MANIFEST.search(recheck)
    if m:
        manifest = m.group(1).strip("`'\"")
    return (sorted(declared), sorted(cited), recheck, sorted(recheck_ids), manifest,
            sorted(evidence))


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
            "evidence_declared_ids": [],
            "cited_ids": [],
            "recheck_ids": [],
            "manifest": None,
            "exit": None,
            "realpath": None,
            "problems": ["missing-entry"],
            "status": "FAIL",
        }
    declared, cited, recheck, recheck_ids, manifest, evidence = contract
    full = os.path.join(root, entry_path)
    if not os.path.isfile(full):
        full = os.path.join(root, "corpus", entry_path)
    realpath = os.path.realpath(full)
    declared_set = set(declared) | set(evidence)
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
    if declared_set and recheck_ids and not declared_set.issubset(set(recheck_ids)):
        problems.append("header-sources-not-rechecked")
    if declared_set and recheck_ids and not set(recheck_ids).issubset(declared_set):
        problems.append("selection-not-declared-by-entry")
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
        "evidence_declared_ids": evidence,
        "cited_ids": cited,
        "recheck_ids": recheck_ids,
        "manifest": manifest,
        "realpath": realpath,
        "exit": exit_code,
        "problems": problems,
        "status": "PASS" if not problems else "FAIL",
    }


def frontier_row_record(fid, entry, problems, declared_ids):
    """Return a FAIL record for a row that rule G refuses to score.

    A row whose status cell is not `admitted` is not evaluated (its entry may
    not exist yet), but it still contributes one record per entry cell so the
    `entries=` denominator counts the raw row set and cannot shrink under a
    status flip."""
    return {
        "entry": entry,
        "declared_ids": list(declared_ids),
        "evidence_declared_ids": [],
        "cited_ids": [],
        "recheck_ids": [],
        "manifest": None,
        "realpath": None,
        "exit": None,
        "problems": list(problems),
        "status": "FAIL",
        "frontier": fid,
    }


def frontier_census(rows, records, registry, sources):
    """Return (census lines, failed, summary) for rule G.

    Every README frontier row is enumerated. A row fails the run when its
    status cell is not `admitted` (`status-not-admitted`), when it is admitted
    but owns no PASS record (`missing-pass-line`), or when an id it binds — its
    README `sources` cell plus the ids its entries declare — has no row in
    `corpus/SOURCES.md` (`source-id-absent:<id>`). The registry limb is only
    applied when a registry exists; `registry=absent` says so in the summary
    instead of passing quietly."""
    by_row = {}
    for record in records:
        by_row.setdefault(record["frontier"], []).append(record)
    lines, failures = [], []
    admitted = closed = problem_rows = 0
    for fid, _title, status, _cell in rows:
        row_records = by_row.get(fid, [])
        bound = set(sources.get(fid, []))
        for record in row_records:
            bound.update(record["declared_ids"])
            bound.update(record["evidence_declared_ids"])
        problems = []
        if status != "admitted":
            problems.append("status-not-admitted")
        else:
            admitted += 1
            if not any(r["status"] == "PASS" for r in row_records):
                problems.append("missing-pass-line")
        if registry is not None:
            for sid in sorted(bound - registry):
                problems.append("source-id-absent:%s" % sid)
        ids = ",".join(sorted(bound)) or "-"
        if problems:
            problem_rows += 1
            failures.extend("%s %s" % (fid, problem) for problem in problems)
            lines.append("FRONTIER-FAIL %s status=%s ids=%s problems=%s" % (
                fid, status, ids, ",".join(problems)))
        else:
            closed += 1
            lines.append("FRONTIER-PASS %s ids=%s" % (fid, ids))
    lines.insert(0, "FRONTIER-CENSUS rows=%d admitted=%d closed=%d problem-rows=%d registry=%s" % (
        len(rows), admitted, closed, problem_rows,
        "absent" if registry is None else len(registry)))
    summary = {"rows": len(rows), "admitted": admitted, "closed": closed,
               "problem_rows": problem_rows,
               "registry": None if registry is None else len(registry),
               "failures": failures}
    return lines, bool(failures), summary


# --- selftest -----------------------------------------------------------------
#
# One case per limb of rule A, plus controls for the two declaration shapes and
# the citation limb. Each fixture root is a miniature lane: a Frontier table
# naming one entry, that entry's header + prose + evidence list + `recheck:`
# line, a schema-1 manifest, and a stub `corpus/instruments/source-recheck.py`
# that exits 0 — so a case failure can only come from the harness's own
# binding, never from a capture.

SELFTEST_README = (
    "| id | topic | status | entry | sources | note |\n"
    "|---|---|---|---|---|---|\n"
    "| F98 | fixture topic | admitted | knowledge/fixture.md | %s | selftest fixture |\n"
)

SELFTEST_ENTRY = (
    "# fixture entry\n"
    "\n"
    "%s"
    "\n"
    "%s"
    "\n"
    "%s"
    "\n"
    "recheck: python3 corpus/instruments/source-recheck.py "
    "--manifest corpus/source-snapshots/fixture/manifest.json %s\n"
)

SELFTEST_STUB = (
    '#!/usr/bin/env python3\n'
    '"""Selftest stub: the harness under test owns every binding rule."""\n'
    'import sys\n'
    "\n"
    "sys.exit(0)\n"
)


def build_fixture(root, header_ids, recheck_ids, prose_ids=(), evidence_ids=()):
    """Write one fixture lane. `prose_ids` are mentioned in a sentence only
    (a reference, not a declaration); `evidence_ids` get a per-source evidence
    list item (`- S002, "fixture section": "fixture quote"`)."""
    mentioned = sorted(set(header_ids) | set(prose_ids) | set(evidence_ids))
    manifest_ids_all = sorted(set(mentioned) | set(recheck_ids))
    for sub in (("corpus", "instruments"), ("corpus", "source-snapshots", "fixture"),
                ("knowledge",)):
        os.makedirs(os.path.join(root, *sub))
    with open(os.path.join(root, "corpus", "README.md"), "w", encoding="utf-8") as fh:
        fh.write(SELFTEST_README % ", ".join(header_ids))
    with open(os.path.join(root, "knowledge", "fixture.md"), "w", encoding="utf-8") as fh:
        fh.write(SELFTEST_ENTRY % (
            "".join("source: %s — selftest fixture header line\n" % sid for sid in header_ids),
            "Body mentions %s in prose only.\n" % ", ".join(mentioned),
            "".join('- %s, "fixture section": "fixture quote"\n' % sid
                    for sid in evidence_ids),
            " ".join("--source %s" % sid for sid in recheck_ids)))
    with open(os.path.join(root, "corpus", "source-snapshots", "fixture", "manifest.json"),
              "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "purpose": "frontier-recheck selftest fixture",
                   "sources": [{"id": sid, "path": "%s.txt" % sid}
                               for sid in manifest_ids_all]},
                  fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(root, "corpus", "instruments", "source-recheck.py"),
              "w", encoding="utf-8") as fh:
        fh.write(SELFTEST_STUB)


SELFTEST_CASES = [
    # name, header ids, recheck ids, prose-only ids, evidence ids,
    # expected exit, expected substrings
    ("bidirectional-holds", ("S001", "S002"), ("S001", "S002"), (), (), 0,
     ["PASS", "ids=S001,S002", "entries=1 pass=1 exit=0"]),
    ("selection-not-declared", ("S001", "S002"), ("S001", "S002", "S003"), ("S003",), (), 1,
     ["problems=selection-not-declared-by-entry", "entries=1 pass=0 exit=1"]),
    ("header-source-not-rechecked", ("S001", "S002"), ("S001",), (), (), 1,
     ["problems=header-sources-not-rechecked", "entries=1 pass=0 exit=1"]),
    ("evidence-list-declares-selection", ("S001",), ("S001", "S002"), (), ("S002",), 0,
     ["PASS", "ids=S001", "entries=1 pass=1 exit=0"]),
    ("evidence-declared-not-rechecked", ("S001",), ("S001",), (), ("S002",), 1,
     ["problems=header-sources-not-rechecked", "entries=1 pass=0 exit=1"]),
    ("selection-neither-declared-nor-mentioned", ("S001", "S002"),
     ("S001", "S002", "S003"), (), (), 1,
     ["problems=selection-not-declared-by-entry,selection-not-cited-by-entry",
      "entries=1 pass=0 exit=1"]),
]


def scratch_base(arg=None):
    """Scratch root: explicit arg, else $HYAKU_SCRATCH, else $TMPDIR, else a platform default."""
    for candidate in (arg, os.environ.get("HYAKU_SCRATCH"), os.environ.get("TMPDIR")):
        if candidate:
            return candidate
    return "/fast/scratch/hyaku" if os.path.isdir("/fast/scratch") else tempfile.gettempdir()


def selftest(scratch_arg=None, out=sys.stdout):
    base = scratch_base(scratch_arg)
    os.makedirs(base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="frontier-recheck-selftest-", dir=base)
    failures = 0
    try:
        for (name, header_ids, recheck_ids, prose_ids, evidence_ids,
             want_exit, want_lines) in SELFTEST_CASES:
            root = os.path.join(scratch, name)
            os.makedirs(root)
            build_fixture(root, header_ids, recheck_ids, prose_ids, evidence_ids)
            proc = subprocess.run(
                [sys.executable, os.path.abspath(__file__), "--root", root],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            problems = []
            if proc.returncode != want_exit:
                problems.append("exit=%d want=%d" % (proc.returncode, want_exit))
            for line in want_lines:
                if line not in proc.stdout:
                    problems.append("missing=%r" % line)
            if problems:
                failures += 1
            print("selftest case=%s exit=%d want=%d verdict=%s"
                  % (name, proc.returncode, want_exit, "fail" if problems else "pass"),
                  file=out)
            for problem in problems:
                print("selftest problem=%s case=%s" % (problem, name), file=out)
            if problems:
                print("selftest stdout case=%s\n%s" % (name, proc.stdout.rstrip()), file=out)
                if proc.stderr:
                    print("selftest stderr case=%s\n%s" % (name, proc.stderr.rstrip()), file=out)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    print("selftest cases=%d failures=%d" % (len(SELFTEST_CASES), failures), file=out)
    return 0 if failures == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    parser.add_argument("--json", default=None, help="write a JSON receipt here")
    parser.add_argument("--selftest", action="store_true",
                        help="run the fixture cases instead of checking the lane")
    parser.add_argument("--scratch", default=None,
                        help="scratch root for selftest fixtures (default $HYAKU_SCRATCH, then $TMPDIR)")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest(args.scratch)
    root = os.path.abspath(args.root)
    try:
        rows = read_frontier(root)
    except OSError as exc:
        print("harness UNAVAILABLE reason=read-error %s" % exc)
        return 2
    sources = read_frontier_sources(root)
    registry = read_registry_ids(root)
    records = []
    for fid, title, status, cell in rows:
        # A topic may govern more than one entry (`entry, entry` in one cell).
        entries = [part.strip() for part in cell.split(",") if part.strip()]
        for entry in entries or ["-"]:
            if status == "admitted":
                record = evaluate(root, entry)
            else:
                # Rule G: a row that is not admitted is never scored, but it
                # still occupies its entry cells in the count (see the docstring).
                record = frontier_row_record(fid, entry, ["status-not-admitted"],
                                             sources.get(fid, []))
            record["frontier"] = fid
            record["title"] = title
            records.append(record)
    census_lines, census_failed, census = frontier_census(rows, records, registry, sources)
    for line in census_lines:
        print(line)
    for record in records:
        print("%-8s %-4s %-52s ids=%-14s exit=%-4s%s" % (
            record["status"], record["frontier"], record["entry"],
            ",".join(record["declared_ids"]) or "-",
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
    if census_failed:
        fail_closed = True
    print("entries=%d pass=%d exit=%d" % (len(records), passed, 1 if fail_closed else 0))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"schema": "kasegi-frontier-recheck-receipt-v1", "root": root,
                       "entries": len(records), "pass": passed,
                       "duplicate_entry": duplicate[2] if duplicate else None,
                       "frontier_census": census,
                       "records": records},
                      fh, indent=2, sort_keys=True)
            fh.write("\n")
    return 1 if fail_closed else 0


if __name__ == "__main__":
    sys.exit(main())
