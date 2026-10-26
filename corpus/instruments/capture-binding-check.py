#!/usr/bin/env python3
"""Bind every capture-manifest record to its registry row and to fetch provenance.

Usage: python3 corpus/instruments/capture-binding-check.py [--root DIR] [--selftest] [--scratch DIR]

The round-33 C1 counter. A capture directory can hold real bytes and still be
unauditable: nothing in `manifest.json` says which documented URL those bytes
came from, or when they were fetched. This instrument walks every
`corpus/source-snapshots/*/` directory under the root and applies three rules.

  A. MANIFEST PRESENCE. Every snapshot directory - a directory that holds a
     `manifest.json` or that holds any captured source file - must carry a
     `manifest.json`. A directory with captures and no manifest is a failure
     naming the directory (the round-32 S049/S050 state, routed defect D5).

  B. URL BINDING (claims-erratum-1, the L1's id-scoped ruling). Every manifest
     record must bind to its OWN `corpus/SOURCES.md` registry row:

       B1. the row `| <record id> | ... |` must exist - otherwise
           `FAIL rule=no-row record=<id>` (a fabricated id);
       B2. the row id must be unique in the registry - two rows with the same
           id are `FAIL rule=dup-id record=<id> rows=<n>`;
       B3. the record's `url` must equal, byte-for-byte, the `https://` token in
           that row's source cell (column 2) - otherwise
           `FAIL rule=url-mismatch record=<id>`. A record with no `url` field at
           all is `url-mismatch ... detail=absent`.

     A URL that also appears in a DIFFERENT row (the registry's S024/S029 and
     S006/S028 duplicate-URL rows) or in prose outside the registry table is
     NOT a failure: see the informational `multi_row_url=N` count on the AUDIT
     line. The frozen claim's predicate (erratum 1) keeps its `unbound=0`
     target under this reading, and the registry's pre-existing W04
     duplicate-URL warnings stay census facts outside this claim.

  C. PROVENANCE. Every record must carry either a non-empty `fetched_utc` or
     `"archival": true`. Records whose snapshot directory is `round-32` or a
     later round MUST carry `fetched_utc`: the archival exemption is closed for
     them, because their fetch instant is recorded. A directory name that does
     not parse as `round-<N>` is treated as a modern round (no archival
     exemption).

Output. One `AUDIT` header line, then one line per manifest directory

    MANIFEST <dirname> records=N url_bound=M fetched=K archival=L

(`url_bound` counts records passing rule B, `fetched` records carrying a
non-empty `fetched_utc`, `archival` records carrying `"archival": true`), then
one `FAIL` line per failure, then exactly one summary line

    records=<total> bound=<total> unbound=<U>

where `bound` counts records satisfying rules B **and** C, and `unbound` counts
records failing B or C, so the printed invariant is `unbound = records - bound`
(the same value the contract calls "<bound-failures>"). The AUDIT line reports
`records=<total> with_url=<records carrying a url field> with_fetched_utc=<...>
with_archival=<...> snapshot_dirs=<...> manifest_dirs=<...>
missing_manifest=<...> multi_row_url=<records whose URL text also occurs in
another registry row>`.

Exit 0 only when every rule passes; 1 on any failure; 2 on a usage or read
error (absent root, absent/unreadable SOURCES.md, unparsable manifest JSON,
malformed manifest shape). A passing summary is not the verdict - the exit
status is.

Known limits (measured, not assumed):

- Rule B binds a record by id, so the binding is only as good as the manifest's
  `id` field: a record whose id names a row but whose capture bytes came from a
  different document is bound by this instrument and would only be caught by
  `source-recheck.py` (quote/sha256 pins) or a human reader.
- The row's URL is the `https://` token found in the source cell with trailing
  `.,;:` stripped; byte-equality is then exact. A row that carries two URL
  tokens binds when the record's url is one of them.
- The registry is read as column 2 of every `| S0xx |` row, whatever the row's
  status (mined, queued, rejected). Duplicate ids are a failure, but duplicate
  URL *values* across different ids are not, per erratum 1.
- The instrument writes nothing outside its scratch directory, and only
  `--selftest` creates a scratch directory at all.

`--selftest` runs this file as a subprocess against eleven fixture lane trees, each
built in a fresh temporary directory (under `--scratch`, else `$HYAKU_SCRATCH`,
else `$TMPDIR`, else the platform temp dir; removed at exit), asserting the exit
status and the expected output lines per case. Prints
`selftest cases=N failures=F` and exits 0 only when F=0.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCHEMA_VERSION = 1
ROW_RE = re.compile(r"^\|\s*(S\d{3,})\s*\|")
URL_TOKEN = re.compile(r"https?://[^\s|]+")
ROUND_RE = re.compile(r"round-(\d+)\Z")
MODERN_ROUND = 32   # round-32+ records must carry fetched_utc; the archival exemption is closed
SCRIPT = os.path.abspath(__file__)


def parse_round(dirname):
    """Round number of a snapshot directory name, or None when it does not parse."""
    m = ROUND_RE.match(dirname)
    return int(m.group(1)) if m else None


def row_tokens(cell):
    """The `https://` tokens of a registry source cell, trailing `.,;:` stripped."""
    return [token.rstrip(".,;:") for token in URL_TOKEN.findall(cell)]


def load_registry(root):
    """Return (rows_by_id, cells) for every `| S0xx |` row in corpus/SOURCES.md.

    `rows_by_id` maps a row id to its list of source cells (a duplicate id is
    visible as a list longer than one); `cells` is every row's source cell in
    registry order, for the cross-row `multi_row_url` count."""
    path = os.path.join(root, "corpus", "SOURCES.md")
    rows_by_id, cells = {}, []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW_RE.match(line)
            if not m:
                continue
            parts = [cell.strip() for cell in line.rstrip("\n").strip().strip("|").split("|")]
            cell = parts[1] if len(parts) > 1 else ""
            rows_by_id.setdefault(m.group(1), []).append(cell)
            cells.append(cell)
    return rows_by_id, cells


def url_row_count(cells, url):
    """How many registry rows carry `url` text in their source cell."""
    return sum(1 for cell in cells if url in cell)


def snapshot_dirs(root):
    """Yield (dirname, path, has_manifest) for every directory under source-snapshots.

    A directory counts as a snapshot directory when it holds `manifest.json` or
    any captured source file; an empty directory is not a snapshot directory."""
    base = os.path.join(root, "corpus", "source-snapshots")
    for name in sorted(os.listdir(base)):
        path = os.path.join(base, name)
        if not os.path.isdir(path):
            continue
        if os.path.isfile(os.path.join(path, "manifest.json")):
            yield name, path, True
            continue
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if files:
            yield name, path, False


def provenance_ok(record, round_no):
    """Rule C for one record. Returns (ok, has_fetched, has_archival)."""
    fetched = record.get("fetched_utc")
    has_fetched = isinstance(fetched, str) and fetched.strip() != ""
    has_archival = record.get("archival") is True
    if round_no is None or round_no >= MODERN_ROUND:
        return has_fetched, has_fetched, has_archival
    return (has_fetched or has_archival), has_fetched, has_archival


def bind_record(record, rows_by_id):
    """Rule B for one record. Returns (bound, [FAIL line fragments])."""
    record_id = record.get("id")
    if not (isinstance(record_id, str) and record_id.strip()):
        return False, ["rule=no-row record=<unnamed>"]
    own = rows_by_id.get(record_id, [])
    if not own:
        return False, ["rule=no-row record=%s" % record_id]
    if len(own) > 1:
        return False, ["rule=dup-id record=%s rows=%d" % (record_id, len(own))]
    url = record.get("url")
    if not (isinstance(url, str) and url.strip()):
        return False, ["rule=url-mismatch record=%s detail=absent" % record_id]
    if url not in row_tokens(own[0]):
        return False, ["rule=url-mismatch record=%s row=%s" % (record_id, record_id)]
    return True, []


def check(root, out=sys.stdout):
    """Apply rules A-C. Returns exit status 0 (pass) / 1 (failure) / 2 (read error)."""
    try:
        rows_by_id, cells = load_registry(root)
        snapshot_list = list(snapshot_dirs(root))
    except OSError as exc:
        print("UNAVAILABLE reason=read-error %s" % exc, file=out)
        return 2

    manifests, missing, failures = [], [], []
    totals = {"records": 0, "with_url": 0, "with_fetched_utc": 0,
              "with_archival": 0, "bound": 0, "multi_row_url": 0}

    for name, path, has_manifest in snapshot_list:
        if not has_manifest:
            missing.append(name)
            failures.append("FAIL rule=missing-manifest dir=%s" % name)
            continue
        manifests.append((name, path))

    for name, path in manifests:
        manifest_path = os.path.join(path, "manifest.json")
        try:
            with open(manifest_path, encoding="utf-8") as fh:
                manifest = json.load(fh)
        except (OSError, ValueError) as exc:
            print("UNAVAILABLE reason=manifest-%s %s" % (type(exc).__name__, manifest_path), file=out)
            return 2
        records = manifest.get("sources") if isinstance(manifest, dict) else None
        if not isinstance(records, list):
            print("UNAVAILABLE reason=manifest-shape %s" % manifest_path, file=out)
            return 2

        round_no = parse_round(name)
        url_bound = fetched = archival = 0
        for record in records:
            if not isinstance(record, dict):
                print("UNAVAILABLE reason=record-shape %s" % manifest_path, file=out)
                return 2
            totals["records"] += 1
            url = record.get("url")
            if isinstance(url, str) and url.strip():
                totals["with_url"] += 1
                if url_row_count(cells, url) > 1:
                    totals["multi_row_url"] += 1

            url_ok, fragments = bind_record(record, rows_by_id)
            if url_ok:
                url_bound += 1
            else:
                failures.extend("FAIL %s dir=%s" % (fragment, name) for fragment in fragments)

            prov_ok, has_fetched, has_archival = provenance_ok(record, round_no)
            if has_fetched:
                fetched += 1
                totals["with_fetched_utc"] += 1
            if has_archival:
                archival += 1
                totals["with_archival"] += 1
            if not prov_ok:
                record_id = record.get("id")
                label = record_id if isinstance(record_id, str) and record_id.strip() else "<unnamed>"
                failures.append("FAIL rule=provenance-missing record=%s dir=%s" % (label, name))

            if url_ok and prov_ok:
                totals["bound"] += 1

        print("MANIFEST %s records=%d url_bound=%d fetched=%d archival=%d"
              % (name, len(records), url_bound, fetched, archival), file=out)

    print("AUDIT records=%d with_url=%d with_fetched_utc=%d with_archival=%d "
          "snapshot_dirs=%d manifest_dirs=%d missing_manifest=%d multi_row_url=%d"
          % (totals["records"], totals["with_url"], totals["with_fetched_utc"],
             totals["with_archival"], len(snapshot_list), len(manifests), len(missing),
             totals["multi_row_url"]),
          file=out)
    for line in failures:
        print(line, file=out)
    print("records=%d bound=%d unbound=%d"
          % (totals["records"], totals["bound"], totals["records"] - totals["bound"]),
          file=out)
    return 0 if not failures else 1


# --- selftest -----------------------------------------------------------------

FIXTURE_HEADER = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)


def write_registry(root, rows):
    """Write a fixture registry: one table row per (id, url) pair, URL in the source cell."""
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    lines = [FIXTURE_HEADER]
    for row_id, url in rows:
        lines.append("| %s | Fixture source — %s | docs | A | scope | anchor | teaches | mined "
                     "| 2026-10-25 | 180d | — |\n" % (row_id, url))
    with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(lines))


def write_manifest(root, dirname, records):
    """Write a fixture snapshot directory with its manifest and one capture per record."""
    path = os.path.join(root, "corpus", "source-snapshots", dirname)
    os.makedirs(path, exist_ok=True)
    for record in records:
        capture = record.get("path")
        if isinstance(capture, str):
            with open(os.path.join(path, capture), "w", encoding="utf-8") as fh:
                fh.write("fixture capture bytes for %s\n" % record.get("id", "?"))
    with open(os.path.join(path, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"schema_version": 1, "purpose": "capture-binding selftest fixture",
                   "sources": records}, fh, indent=2, sort_keys=True)
        fh.write("\n")


def record(record_id, url=None, fetched=None, archival=None):
    item = {"id": record_id, "path": "%s.txt" % (record_id or "unnamed"), "sha256": "0" * 64,
            "quotes": []}
    if url is not None:
        item["url"] = url
    if fetched is not None:
        item["fetched_utc"] = fetched
    if archival is not None:
        item["archival"] = archival
    return item


ALPHA = "https://example.invalid/alpha"
BETA = "https://example.invalid/beta"
GAMMA = "https://example.invalid/gamma"
STAMP = "2026-10-25T00:00:00Z"


def case_clean(root):
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP),
                                      record("S002", url=BETA, archival=True)])


def case_missing_manifest(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])
    path = os.path.join(root, "corpus", "source-snapshots", "round-31")
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "S009.txt"), "w", encoding="utf-8") as fh:
        fh.write("capture with no manifest\n")


def case_record_without_url(root):
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP),
                                      record("S002", archival=True)])


def case_duplicate_id_rows(root):
    """Erratum 1 rebuild of the old `url-matching-two-rows` case: same id, two rows."""
    write_registry(root, [("S001", ALPHA), ("S001", BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])


def case_url_mismatch(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url="https://example.invalid/unknown",
                                             fetched=STAMP)])


def case_no_row(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S009", url=ALPHA, fetched=STAMP)])


def case_shared_url_passes(root):
    """A URL carried by two DIFFERENT ids is informational, not a failure (erratum 1 §4)."""
    write_registry(root, [("S001", ALPHA), ("S024", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])


def case_modern_without_fetched(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-32", [record("S001", url=ALPHA, archival=True)])


def case_legacy_without_archival(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-31", [record("S001", url=ALPHA)])


def case_modern_with_fetched(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-32", [record("S001", url=ALPHA, fetched=STAMP)])


def case_legacy_archival(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-31", [record("S001", url=ALPHA, archival=True)])


CASES = [
    # name, builder, expected exit, expected stdout lines
    ("clean-all-pass", case_clean, 0,
     ["MANIFEST round-30 records=2 url_bound=2 fetched=1 archival=1",
      "records=2 bound=2 unbound=0"]),
    ("missing-manifest-dir", case_missing_manifest, 1,
     ["FAIL rule=missing-manifest dir=round-31",
      "MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
      "records=1 bound=1 unbound=0"]),
    ("record-without-url", case_record_without_url, 1,
     ["FAIL rule=url-mismatch record=S002 detail=absent dir=round-30",
      "records=2 bound=1 unbound=1"]),
    ("url-matching-two-rows", case_duplicate_id_rows, 1,
     ["FAIL rule=dup-id record=S001 rows=2 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("url-mismatch", case_url_mismatch, 1,
     ["FAIL rule=url-mismatch record=S001 row=S001 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("no-row", case_no_row, 1,
     ["FAIL rule=no-row record=S009 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("shared-url-not-a-failure", case_shared_url_passes, 0,
     ["MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
      "multi_row_url=1",
      "records=1 bound=1 unbound=0"]),
    ("round-32-record-without-fetched_utc", case_modern_without_fetched, 1,
     ["FAIL rule=provenance-missing record=S001 dir=round-32",
      "records=1 bound=0 unbound=1"]),
    ("pre-round-32-record-without-archival", case_legacy_without_archival, 1,
     ["FAIL rule=provenance-missing record=S001 dir=round-31",
      "records=1 bound=0 unbound=1"]),
    ("round-32-record-with-fetched_utc-passes", case_modern_with_fetched, 0,
     ["MANIFEST round-32 records=1 url_bound=1 fetched=1 archival=0",
      "records=1 bound=1 unbound=0"]),
    ("pre-round-32-archival-passes", case_legacy_archival, 0,
     ["MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1",
      "records=1 bound=1 unbound=0"]),
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
    scratch = tempfile.mkdtemp(prefix="capture-binding-selftest-", dir=base)
    failures = 0
    try:
        for name, build, want_exit, want_lines in CASES:
            root = os.path.join(scratch, name)
            os.makedirs(root)
            build(root)
            proc = subprocess.run(
                [sys.executable, SCRIPT, "--root", root],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            problems = []
            if proc.returncode != want_exit:
                problems.append("exit=%d want=%d" % (proc.returncode, want_exit))
            for line in want_lines:
                if line not in proc.stdout:
                    problems.append("missing=%r" % line)
            if want_exit == 0 and "FAIL " in proc.stdout:
                problems.append("unexpected-FAIL-line")
            verdict = "pass" if not problems else "fail"
            if problems:
                failures += 1
            print("selftest case=%s exit=%d want=%d verdict=%s"
                  % (name, proc.returncode, want_exit, verdict), file=out)
            if problems:
                for problem in problems:
                    print("selftest problem=%s case=%s" % (problem, name), file=out)
                print("selftest stdout case=%s\n%s" % (name, proc.stdout.rstrip()), file=out)
                if proc.stderr:
                    print("selftest stderr case=%s\n%s" % (name, proc.stderr.rstrip()), file=out)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    print("selftest cases=%d failures=%d" % (len(CASES), failures), file=out)
    return 0 if failures == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT))),
                        help="lane root holding corpus/SOURCES.md and corpus/source-snapshots/")
    parser.add_argument("--selftest", action="store_true",
                        help="run the fixture cases instead of checking the lane")
    parser.add_argument("--scratch", default=None,
                        help="scratch root for selftest fixtures (default $HYAKU_SCRATCH, then $TMPDIR)")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest(args.scratch)

    root = os.path.abspath(args.root)
    if not os.path.isdir(os.path.join(root, "corpus", "source-snapshots")):
        print("UNAVAILABLE reason=no-snapshot-tree %s" % root)
        return 2
    return check(root)


if __name__ == "__main__":
    sys.exit(main())
