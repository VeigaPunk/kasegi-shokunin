#!/usr/bin/env python3
"""Bind every capture-manifest record to its registry row and to fetch provenance.

Usage: python3 corpus/instruments/capture-binding-check.py [--root DIR] [--selftest] [--scratch DIR]

The round-33 C1 counter, hardened in round 34. A capture directory can hold real
bytes and still be unauditable: nothing in `manifest.json` says which documented
URL those bytes came from, when they were fetched, or whether a file in the
directory is accounted for at all. This instrument walks every snapshot
directory under `corpus/source-snapshots/` - recursively - and applies the
rules below.

  A. MANIFEST PRESENCE AND PER-FILE BINDING. Every snapshot directory - a
     directory that holds a `manifest.json` or that holds any captured source
     file of its own - must carry a `manifest.json`; a directory with captures
     and no manifest is `FAIL rule=missing-manifest dir=<dir>`. Inside a
     manifest directory, every capture file must be accounted for:

       A1. it is named by the `path` of at least one `sources[]` record; or
       A2. the manifest's top-level `orphans` list declares it, as an object
           `{"path": "<file name in this directory>", "reason": "<non-empty>"}`.
           A declared orphan keeps the exit status at 0 and is still printed as
           `orphan=<file>` on the AUDIT line - the listing is the record that
           the file is known and unbound, not a silent pass;
       otherwise `FAIL rule=orphan-capture file=<file> dir=<dir>`.
     A declaration whose file is absent is `FAIL rule=orphan-declared-missing`
     (a stale listing), and a malformed `orphans` list is a manifest-shape
     error (exit 2). Orphans never change `records=`/`bound=`/`unbound=`, so a
     declaration cannot be used to inflate the binding counts.

     Nested snapshot directories are audited in their own right: the walk
     descends whether or not the parent is a snapshot directory, and a nested
     directory is named by its path below `corpus/source-snapshots/`
     (`round-30/inner`). A parent's per-file check considers only its own direct
     files, because a nested directory's files are that directory's subject.

  B. URL BINDING (claims-erratum-1, the L1's id-scoped ruling). Every manifest
     record must bind to its OWN `corpus/SOURCES.md` registry row:

       B1. the row `| <record id> | ... |` must exist - otherwise
           `FAIL rule=no-row record=<id>` (a fabricated id);
       B2. the row id must be unique in the registry - two rows with the same
           id are `FAIL rule=dup-id record=<id> rows=<n>`;
       B3. a row whose `status` cell is `rejected` cannot anchor a record:
           `FAIL rule=rejected-row-anchor record=<id> row=<id>`. A rejected row
           is a documented refusal, so a capture claiming it is bound to a
           source the lane has refused;
       B4. the row's source cell must carry exactly one `https://` token. A row
           with two or more is `FAIL rule=double-https-row row=<id> n=<n>` and
           cannot unambiguously bind anything - the record pointing at it is
           `FAIL rule=url-ambiguous record=<id> row=<id> tokens=<n>`;
       B5. the record's `url` must equal, byte-for-byte, the `https://` token in
           that row's source cell (column 2) - otherwise
           `FAIL rule=url-mismatch record=<id>`. A record with no `url` field at
           all is `url-mismatch ... detail=absent`.

     A URL that also appears in a DIFFERENT row (the registry's S024/S029 and
     S006/S028 duplicate-URL rows) or in prose outside the registry table is
     NOT a failure: see the informational `multi_row_url=N` count on the AUDIT
     line. The frozen claim's predicate (erratum 1) keeps its `unbound=0`
     target under this reading, and the registry's pre-existing W04
     duplicate-URL warnings stay census facts outside this claim.

  C. PROVENANCE. Every record must carry either a strict-UTC `fetched_utc` or
     `"archival": true`. A `fetched_utc` value is strict UTC only when it is an
     ISO-8601 timestamp whose suffix is `Z` or `+00:00` and whose fields are a
     real calendar instant, e.g. `2026-10-26T04:16:06Z`:

       - a placeholder (`pending`, `tbd`, `unknown`, `none`, ...) is
         `FAIL rule=fetched-utc ... detail=pending`;
       - a local or non-zero offset (`2026-10-25T23:14:00-03:00`, the round-32
         R8 field) is `FAIL rule=fetched-utc ... detail=local-offset`;
       - anything else unparsable (`2026-13-01T00:00:00Z`, a bare date) is
         `FAIL rule=fetched-utc ... detail=malformed`;
       - an absent value is `FAIL rule=provenance-missing` when the record has
         no archival exemption, `detail=absent` folded into that line.

     Records whose snapshot directory is `round-32` or a later round MUST carry
     a strict-UTC `fetched_utc`: the archival exemption is closed for them,
     because their fetch instant is recorded. A directory name that does not
     parse as `round-<N>` is treated as a modern round (no archival exemption).
     A present-but-invalid `fetched_utc` fails in every round, including the
     legacy rounds - the field is an assertion whether or not the round requires
     it.

  D. MANIFEST INTEGRITY. Duplicate records inside one manifest fail: two
     records in the same directory carrying the same `id` is
     `FAIL rule=dup-record field=id value=<id> count=<n>`, and two records
     naming the same capture `path` is the `field=path` form. A duplicated
     record means the manifest's record count overstates the captures it
     documents.

  E. CAPTURE-BYTES BINDING (round-42, the wave-2 F-BIND defect). Rules A-D bind
     a record to a file NAME, a registry URL and a fetch stamp; they never read
     the capture. A manifest could therefore name a file that is absent, or pin
     a digest no file satisfies, and still print `bound=records`. For every
     `sources[]` record:

       E1. its `path` must resolve inside its own snapshot directory and name a
           regular file there - otherwise
           `FAIL rule=capture-missing record=<id> path=<path>`. A path that
           climbs out of the directory (`../S999.txt`) is the same line: the
           record names bytes outside the directory that is being audited;
       E2. the record's `sha256` - the digest of the capture bytes - must equal
           the file's sha256, otherwise `FAIL rule=digest-mismatch
           record=<id> sha256=<pinned>`. A value that is not 64 lowercase hex
           digits is `FAIL rule=digest-invalid`. A record that pins nothing
           (field absent, empty, or the `"0"*64` fixture sentinel) is
           `FAIL rule=digest-missing` in round-32 and later, and an
           informational, printed exemption (`digest_unpinned=N` on the AUDIT
           line) in the legacy rounds - the declared-exemption shape rule C
           already uses for `archival`. The other two digest fields of a record
           are pinned the same way where they can be: `snapshot_sha256`, the
           same assertion under the round-39+ name, must equal the file digest
           (`FAIL rule=digest-mismatch field=snapshot_sha256 ...`), while
           `full_text_sha256` pins the extracted document text, which is not the
           snapshot bytes (S060's full text is not its HTML capture), so only
           its shape - 64 lowercase hex digits - is checked;
       E3. the two fetched-URL fields agree: `capture_url` and
           `http.final_url` must be byte-identical when both are present, and a
           `http.final_url` must be the record's `url` or its `capture_url` -
           otherwise `FAIL rule=capture-url-mismatch record=<id>`. A redirect
           is a legal difference between `url` and `capture_url` (S057, S025
           capture the PDF behind the advisory); a disagreement between the
           fields describing one fetch is not.

     Rule E changes `bound`: a record failing E is `unbound` exactly as a
     record failing B or C is, so a manifest whose captures are absent or
     tampered can no longer print `bound=records`.

Output. One `MANIFEST` line per manifest directory

    MANIFEST <dir> records=N url_bound=M fetched=K archival=L

(`url_bound` counts records passing rule B, `fetched` records carrying a
strict-UTC `fetched_utc`, `archival` records carrying `"archival": true`), then
one `FAIL` line per failure, then exactly one summary line

    records=<total> bound=<total> unbound=<U>

where `bound` counts records satisfying rules B, C **and** E, and `unbound`
counts records failing B, C or E, so the printed invariant is
`unbound = records - bound` (the same value the contract calls
"<bound-failures>"). The AUDIT line reports
`records=<total> with_url=<records carrying a url field> with_fetched_utc=<...>
with_archival=<...> snapshot_dirs=<...> manifest_dirs=<...>
missing_manifest=<...> multi_row_url=<records whose URL text also occurs in
another registry row> digest_unpinned=<legacy-round records pinning no digest>
orphans=<capture files no record names>` followed by one `orphan=<file>` token
per such file.

Exit 0 only when every rule passes; 1 on any failure; 2 on a usage or read
error (absent root, absent/unreadable SOURCES.md, unparsable manifest JSON,
malformed manifest shape, malformed `orphans` declaration). A passing summary is
not the verdict - the exit status is, and an orphan or a duplicate row is a
failure that leaves `records=`/`bound=`/`unbound=` unchanged.

Known limits (measured, not assumed):

- Rule B binds a record by id, so the binding is only as good as the manifest's
  `id` field: a record whose id names a row but whose capture bytes came from a
  different document is bound by this instrument and would only be caught by
  `source-recheck.py` (quote/sha256 pins) or a human reader.
- Rule A binds captures to records by file name, not by content, and rule E2
  binds them by the digest the manifest itself declares: a capture whose bytes
  were copied from a different document still passes when the manifest pins the
  copied bytes' digest. What rule E removes is the silent case - a capture named
  but absent, a path leaving the directory, and a stale digest are failures, not
  absences.
- The row's URL is the `https://` token found in the source cell with trailing
  `.,;:` stripped; byte-equality is then exact. A row carrying two or more
  tokens is now a failure (rule B4) rather than a lenient match.
- The registry is read as column 2 of every `| S0xx |` row, whatever the row's
  status; rule B3 is the one status that changes a verdict. Duplicate URL
  *values* across different ids are not a failure, per erratum 1.
- The instrument writes nothing outside its scratch directory, and only
  `--selftest` creates a scratch directory at all.

`--selftest` runs this file as a subprocess against one fixture lane tree per
case, each built in a fresh temporary directory (under `--scratch`, else
`$HYAKU_SCRATCH`, else `$TMPDIR`, else the platform temp dir; removed at exit),
asserting the exit status and the expected output lines per case; it then runs
two report-verifier cases, which feed a forged `--selftest` report to the report
checker itself. A summary-only report (`selftest cases=N failures=0` with no
`selftest case=` verdict line) is a failure, not a pass: a mutant that skips
every fixture can print the summary without running a case. Prints
`selftest cases=N failures=F` and exits 0 only when F=0.
"""
import argparse
import datetime
import hashlib
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
UTC_STAMP_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?(?:Z|\+00:00)\Z")
OFFSET_STAMP_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.\d{1,9})?[+-]\d{2}:?\d{2}\Z")
PENDING_VALUES = frozenset({"pending", "tbd", "todo", "unknown", "none", "null", "n/a", "na", "unset"})
MODERN_ROUND = 32   # round-32+ records must carry fetched_utc; the archival exemption is closed
ZERO_DIGEST = "0" * 64   # the lane's fixture convention for "no digest declared"
DIGEST_RE = re.compile(r"^[0-9a-f]{64}\Z")
STATUS_REJECTED = "rejected"
STATUS_COLUMN = 7   # | id | source | kind | tier | scope | anchor | teaches | status | ...
SCRIPT = os.path.abspath(__file__)


def parse_round(dirname):
    """Round number of a snapshot directory name, or None when it does not parse.

    A nested directory is named by its path below source-snapshots, so the round
    is read from the first path component (`round-30/inner` is round 30)."""
    m = ROUND_RE.match(dirname.split("/", 1)[0])
    return int(m.group(1)) if m else None


def row_tokens(cell):
    """The `https://` tokens of a registry source cell, trailing `.,;:` stripped."""
    return [token.rstrip(".,;:") for token in URL_TOKEN.findall(cell)]


def load_registry(root):
    """Return (rows_by_id, cells) for every `| S0xx |` row in corpus/SOURCES.md.

    `rows_by_id` maps a row id to its list of (source cell, status) pairs (a
    duplicate id is visible as a list longer than one); `cells` is every row's
    source cell in registry order, for the cross-row `multi_row_url` count."""
    path = os.path.join(root, "corpus", "SOURCES.md")
    rows_by_id, cells = {}, []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW_RE.match(line)
            if not m:
                continue
            parts = [cell.strip() for cell in line.rstrip("\n").strip().strip("|").split("|")]
            cell = parts[1] if len(parts) > 1 else ""
            status = parts[STATUS_COLUMN] if len(parts) > STATUS_COLUMN else ""
            rows_by_id.setdefault(m.group(1), []).append((cell, status))
            cells.append(cell)
    return rows_by_id, cells


def double_https_rows(rows_by_id):
    """Rows whose source cell carries two or more `https://` tokens.

    A two-token cell cannot say which document the row names, so it can bind
    nothing: the row is a failure and every record pointing at it is ambiguous."""
    offenders = []
    for row_id in sorted(rows_by_id):
        for cell, _status in rows_by_id[row_id]:
            tokens = row_tokens(cell)
            if len(tokens) > 1:
                offenders.append((row_id, len(tokens)))
    return offenders


def url_row_count(cells, url):
    """How many registry rows carry `url` text in their source cell."""
    return sum(1 for cell in cells if url in cell)


def snapshot_dirs(root):
    """Yield (relname, path, has_manifest) for every snapshot directory, parents first.

    A directory is a snapshot directory when it holds `manifest.json` or any
    captured source file of its own; subdirectories are walked whether or not
    their parent is a snapshot directory, so a nested capture directory is
    audited in its own right under the name `<parent>/<child>`."""
    base = os.path.join(root, "corpus", "source-snapshots")
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        relname = os.path.relpath(dirpath, base)
        if relname == os.curdir:
            continue
        files = sorted(name for name in filenames
                       if os.path.isfile(os.path.join(dirpath, name)))
        if "manifest.json" in files:
            yield relname, dirpath, True
            continue
        if files:
            yield relname, dirpath, False


def classify_fetched(value):
    """Classify a `fetched_utc` value. Returns (ok, detail)."""
    if not isinstance(value, str) or not value.strip():
        return False, "malformed"
    text = value.strip()
    if text.lower() in PENDING_VALUES:
        return False, "pending"
    m = UTC_STAMP_RE.match(text)
    if m:
        try:
            datetime.datetime(*(int(part) for part in m.groups()))
        except ValueError:
            return False, "malformed"
        return True, None
    if OFFSET_STAMP_RE.match(text):
        return False, "local-offset"
    return False, "malformed"


def provenance_ok(record, round_no):
    """Rule C for one record. Returns (ok, has_fetched, has_archival, detail)."""
    has_archival = record.get("archival") is True
    modern = round_no is None or round_no >= MODERN_ROUND
    raw = record.get("fetched_utc")
    if raw is None:
        if modern:
            return False, False, has_archival, "absent"
        return has_archival, False, has_archival, (None if has_archival else "absent")
    stamp_ok, detail = classify_fetched(raw)
    if stamp_ok:
        return True, True, has_archival, None
    return False, False, has_archival, detail


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
    cell, status = own[0]
    if status == STATUS_REJECTED:
        return False, ["rule=rejected-row-anchor record=%s row=%s" % (record_id, record_id)]
    tokens = row_tokens(cell)
    url = record.get("url")
    if not (isinstance(url, str) and url.strip()):
        return False, ["rule=url-mismatch record=%s detail=absent" % record_id]
    if len(tokens) > 1:
        return False, ["rule=url-ambiguous record=%s row=%s tokens=%d"
                       % (record_id, record_id, len(tokens))]
    if url not in tokens:
        return False, ["rule=url-mismatch record=%s row=%s" % (record_id, record_id)]
    return True, []


def orphan_paths(manifest):
    """The declared orphan file names of a manifest, or None when malformed.

    The declaration is the manifest's top-level `orphans` list, one object per
    file: `{"path": "<name in this directory>", "reason": "<non-empty>"}`."""
    declared = manifest.get("orphans", [])
    if not isinstance(declared, list):
        return None
    paths = []
    for entry in declared:
        if not isinstance(entry, dict):
            return None
        path = entry.get("path")
        reason = entry.get("reason")
        if not (isinstance(path, str) and path.strip()):
            return None
        if not (isinstance(reason, str) and reason.strip()):
            return None
        paths.append(path.strip())
    return paths


def capture_files(path):
    """The capture files a snapshot directory holds directly (manifest excluded)."""
    return sorted(name for name in os.listdir(path)
                  if name != "manifest.json" and os.path.isfile(os.path.join(path, name)))


def duplicate_records(records):
    """Duplicate (field, value, count) triples inside one manifest's records."""
    duplicates = []
    for field in ("id", "path"):
        seen = {}
        for record in records:
            value = record.get(field)
            if isinstance(value, str) and value.strip():
                seen[value] = seen.get(value, 0) + 1
        for value in sorted(seen):
            if seen[value] > 1:
                duplicates.append((field, value, seen[value]))
    return duplicates


def capture_binding(record, dirpath, round_no):
    """Rule E for one record. Returns ([FAIL line fragments], digest_unpinned).

    E1 resolves the record's `path` against its own snapshot directory and
    requires a regular file there; E2 compares the record's capture-bytes pins
    (`sha256`, and `snapshot_sha256` when present) with the capture bytes (a
    `sha256` pin is mandatory from round-32 on; the round<=31 all-zero sentinel
    stays a printed exemption) and requires the document-text pin
    (`full_text_sha256`) to be a digest at all; E3 requires the record's
    fetched-URL fields to agree with each other. A path that escapes the
    directory through `..` is reported as E1: the record names bytes outside its
    own capture directory, which is exactly what a manifest may not do."""
    record_id = record.get("id")
    label = record_id if isinstance(record_id, str) and record_id.strip() else "<unnamed>"
    fragments = []
    unpinned = False
    raw = record.get("path")
    if not (isinstance(raw, str) and raw.strip()):
        return ["rule=capture-missing record=%s path=<absent>" % label], unpinned
    base = os.path.realpath(dirpath)
    target = os.path.realpath(os.path.join(base, raw))
    if os.path.commonpath([base, target]) != base or not os.path.isfile(target):
        return ["rule=capture-missing record=%s path=%s" % (label, raw)], unpinned

    with open(target, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()

    pinned = record.get("sha256")
    if pinned is None:
        value = ""
    elif isinstance(pinned, str):
        value = pinned.strip()
    else:
        value = None
    if value is None or (value and not DIGEST_RE.match(value)):
        fragments.append("rule=digest-invalid record=%s" % label)
    elif not value or value == ZERO_DIGEST:
        if round_no is None or round_no >= MODERN_ROUND:
            fragments.append("rule=digest-missing record=%s" % label)
        else:
            unpinned = True
    elif actual != value:
        fragments.append("rule=digest-mismatch record=%s sha256=%s" % (label, value))

    snapshot = record.get("snapshot_sha256")
    if isinstance(snapshot, str) and snapshot.strip() not in ("", ZERO_DIGEST):
        snapshot_value = snapshot.strip()
        if not DIGEST_RE.match(snapshot_value):
            fragments.append("rule=digest-invalid field=snapshot_sha256 record=%s" % label)
        elif snapshot_value != actual:
            fragments.append("rule=digest-mismatch field=snapshot_sha256 record=%s sha256=%s"
                             % (label, snapshot_value))
    full_text = record.get("full_text_sha256")
    if isinstance(full_text, str) and full_text.strip() and not DIGEST_RE.match(full_text.strip()):
        fragments.append("rule=digest-invalid field=full_text_sha256 record=%s" % label)

    url = record.get("url")
    capture_url = record.get("capture_url")
    http = record.get("http")
    final_url = http.get("final_url") if isinstance(http, dict) else None
    if isinstance(capture_url, str) and isinstance(final_url, str):
        if capture_url != final_url:
            fragments.append("rule=capture-url-mismatch record=%s capture_url=%s final_url=%s"
                             % (label, capture_url, final_url))
    elif isinstance(final_url, str):
        documented = [value for value in (url, capture_url) if isinstance(value, str)]
        if documented and final_url not in documented:
            fragments.append("rule=capture-url-mismatch record=%s final_url=%s"
                             % (label, final_url))
    return fragments, unpinned


def check(root, out=sys.stdout):
    """Apply rules A-E. Returns exit status 0 (pass) / 1 (failure) / 2 (read error)."""
    try:
        rows_by_id, cells = load_registry(root)
        snapshot_list = list(snapshot_dirs(root))
    except OSError as exc:
        print("UNAVAILABLE reason=read-error %s" % exc, file=out)
        return 2

    manifests, missing, failures = [], [], []
    totals = {"records": 0, "with_url": 0, "with_fetched_utc": 0,
              "with_archival": 0, "bound": 0, "multi_row_url": 0, "digest_unpinned": 0}
    orphans = []

    for row_id, count in double_https_rows(rows_by_id):
        failures.append("FAIL rule=double-https-row row=%s n=%d" % (row_id, count))

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
        declared = orphan_paths(manifest)
        if declared is None:
            print("UNAVAILABLE reason=manifest-shape %s orphans" % manifest_path, file=out)
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

            prov_ok, has_fetched, has_archival, detail = provenance_ok(record, round_no)
            if has_fetched:
                fetched += 1
                totals["with_fetched_utc"] += 1
            if has_archival:
                archival += 1
                totals["with_archival"] += 1
            if not prov_ok:
                record_id = record.get("id")
                label = record_id if isinstance(record_id, str) and record_id.strip() else "<unnamed>"
                if detail == "absent":
                    failures.append("FAIL rule=provenance-missing record=%s dir=%s" % (label, name))
                else:
                    failures.append("FAIL rule=fetched-utc record=%s dir=%s detail=%s"
                                    % (label, name, detail))

            capture_fragments, digest_unpinned = capture_binding(record, path, round_no)
            if digest_unpinned:
                totals["digest_unpinned"] += 1
            failures.extend("FAIL %s dir=%s" % (fragment, name)
                            for fragment in capture_fragments)

            if url_ok and prov_ok and not capture_fragments:
                totals["bound"] += 1

        for field, value, count in duplicate_records(records):
            failures.append("FAIL rule=dup-record field=%s value=%s count=%d dir=%s"
                            % (field, value, count, name))

        captures = capture_files(path)
        bound_paths = set(record.get("path") for record in records
                          if isinstance(record.get("path"), str))
        for capture in captures:
            if capture in bound_paths:
                continue
            orphans.append((name, capture))
            if capture not in declared:
                failures.append("FAIL rule=orphan-capture file=%s dir=%s" % (capture, name))
        for stale in sorted(set(declared) - set(captures)):
            failures.append("FAIL rule=orphan-declared-missing file=%s dir=%s" % (stale, name))

        print("MANIFEST %s records=%d url_bound=%d fetched=%d archival=%d"
              % (name, len(records), url_bound, fetched, archival), file=out)

    audit = ("AUDIT records=%d with_url=%d with_fetched_utc=%d with_archival=%d "
             "snapshot_dirs=%d manifest_dirs=%d missing_manifest=%d multi_row_url=%d "
             "digest_unpinned=%d orphans=%d"
             % (totals["records"], totals["with_url"], totals["with_fetched_utc"],
                totals["with_archival"], len(snapshot_list), len(manifests), len(missing),
                totals["multi_row_url"], totals["digest_unpinned"], len(orphans)))
    audit += "".join(" orphan=%s" % capture for _name, capture in orphans)
    print(audit, file=out)
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
    """Write a fixture registry: one table row per (id, source cell[, status]).

    The cell is the body after the ` — ` separator, so a row can carry one URL
    (the ordinary fixture) or several (the double-token case); `status` defaults
    to `mined`."""
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    lines = [FIXTURE_HEADER]
    for row in rows:
        row_id, cell = row[0], row[1]
        status = row[2] if len(row) > 2 else "mined"
        lines.append("| %s | Fixture source — %s | docs | A | scope | anchor | teaches | %s "
                     "| 2026-10-25 | 180d | — |\n" % (row_id, cell, status))
    with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(lines))


def write_manifest(root, dirname, records, orphans=None, pin_digests=True):
    """Write a fixture snapshot directory with its manifest and one capture per record.

    `dirname` may carry a slash, which builds a nested snapshot directory. Unless
    `pin_digests` is false, every record that leaves `sha256` unset (or at the
    `ZERO_DIGEST` sentinel) is pinned to the sha256 of the bytes just written for
    it, computed AFTER every capture is in place so a record naming a shared path
    pins the file that survives."""
    path = os.path.join(root, "corpus", "source-snapshots", dirname)
    os.makedirs(path, exist_ok=True)
    for record in records:
        capture = record.get("path")
        if isinstance(capture, str):
            with open(os.path.join(path, capture), "w", encoding="utf-8") as fh:
                fh.write("fixture capture bytes for %s\n" % record.get("id", "?"))
    if pin_digests:
        for record in records:
            capture = record.get("path")
            if not isinstance(capture, str) or record.get("sha256") not in (None, "", ZERO_DIGEST):
                continue
            target = os.path.join(path, capture)
            if os.path.isfile(target):
                with open(target, "rb") as fh:
                    record["sha256"] = hashlib.sha256(fh.read()).hexdigest()
    payload = {"schema_version": 1, "purpose": "capture-binding selftest fixture",
               "sources": records}
    if orphans is not None:
        payload["orphans"] = orphans
    with open(os.path.join(path, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")


def write_capture_file(root, dirname, filename):
    """Write one extra capture file into a fixture snapshot directory."""
    path = os.path.join(root, "corpus", "source-snapshots", dirname)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), "w", encoding="utf-8") as fh:
        fh.write("fixture capture bytes for %s\n" % filename)


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


def case_shared_url_two_records(root):
    """Two records sharing one URL across distinct rows: informational, not dup-id."""
    write_registry(root, [("S001", ALPHA), ("S024", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP),
                                      record("S024", url=ALPHA, fetched=STAMP)])


def case_duplicate_id_rows(root):
    """Two registry rows with the same id (renamed from the mismatched r33 name)."""
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


def case_fetched_pending(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-32", [record("S001", url=ALPHA, fetched="pending")])


def case_fetched_local_offset(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-32", [record("S001", url=ALPHA, fetched="2026-10-25T23:14:00-03:00")])


def case_per_file_orphan_detected(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])
    write_capture_file(root, "round-30", "S009.txt")


def case_per_file_orphan_listed(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)],
                   orphans=[{"path": "S009.txt",
                             "reason": "fixture: capture landed with no registry row yet"}])
    write_capture_file(root, "round-30", "S009.txt")


def case_nested_snapshot(root):
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])
    write_manifest(root, "round-30/inner", [record("S002", url=BETA, fetched=STAMP)])


def case_nested_missing_manifest(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-31", [record("S001", url=ALPHA, fetched=STAMP)])
    write_capture_file(root, "round-31/inner", "S009.txt")


def case_dup_record(root):
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    first = record("S001", url=ALPHA, fetched=STAMP)
    second = record("S001", url=ALPHA, fetched=STAMP)
    second["path"] = "S001-copy.txt"
    third = record("S002", url=BETA, fetched=STAMP)
    third["path"] = "S001.txt"
    write_manifest(root, "round-30", [first, second, third])


def case_double_https_row(root):
    write_registry(root, [("S001", ALPHA + " and " + BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])


def case_rejected_row_anchor(root):
    write_registry(root, [("S026", ALPHA, "rejected")])
    write_manifest(root, "round-30", [record("S026", url=ALPHA, fetched=STAMP)])


def case_capture_missing(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])
    os.remove(os.path.join(root, "corpus", "source-snapshots", "round-30", "S001.txt"))


def case_capture_escape(root):
    write_registry(root, [("S001", ALPHA)])
    escaping = record("S001", url=ALPHA, fetched=STAMP)
    escaping["path"] = "../S999.txt"
    write_manifest(root, "round-30", [escaping])


def case_digest_mismatch(root):
    write_registry(root, [("S001", ALPHA)])
    pinned = record("S001", url=ALPHA, fetched=STAMP)
    pinned["sha256"] = "f" * 64
    write_manifest(root, "round-30", [pinned], pin_digests=False)


def case_digest_invalid(root):
    write_registry(root, [("S001", ALPHA)])
    pinned = record("S001", url=ALPHA, fetched=STAMP)
    pinned["sha256"] = "not-a-digest"
    write_manifest(root, "round-30", [pinned], pin_digests=False)


def case_digest_unpinned_modern(root):
    write_registry(root, [("S001", ALPHA)])
    unpinned = record("S001", url=ALPHA, fetched=STAMP)
    unpinned["sha256"] = ZERO_DIGEST
    write_manifest(root, "round-32", [unpinned], pin_digests=False)


def case_digest_unpinned_legacy(root):
    write_registry(root, [("S001", ALPHA)])
    unpinned = record("S001", url=ALPHA, fetched=STAMP)
    unpinned["sha256"] = ZERO_DIGEST
    write_manifest(root, "round-30", [unpinned], pin_digests=False)


def case_capture_url_mismatch(root):
    write_registry(root, [("S001", ALPHA)])
    redirected = record("S001", url=ALPHA, fetched=STAMP)
    redirected["capture_url"] = BETA
    redirected["http"] = {"status": 200, "final_url": ALPHA}
    write_manifest(root, "round-30", [redirected])


def case_url_trailing_slash(root):
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA + "/", fetched=STAMP)])


def case_snapshot_digest_mismatch(root):
    write_registry(root, [("S001", ALPHA)])
    pinned = record("S001", url=ALPHA, fetched=STAMP)
    pinned["snapshot_sha256"] = "f" * 64
    write_manifest(root, "round-32", [pinned])


def case_snapshot_digest_matches(root):
    write_registry(root, [("S001", ALPHA)])
    pinned = record("S001", url=ALPHA, fetched=STAMP)
    write_manifest(root, "round-32", [pinned])
    with open(os.path.join(root, "corpus", "source-snapshots", "round-32", "S001.txt"),
              "rb") as fh:
        pinned["snapshot_sha256"] = hashlib.sha256(fh.read()).hexdigest()
    write_manifest(root, "round-32", [pinned])


CASES = [
    # name, builder, expected exit, expected stdout lines
    ("clean-all-pass", case_clean, 0,
     ["MANIFEST round-30 records=2 url_bound=2 fetched=1 archival=1",
      "orphans=0",
      "records=2 bound=2 unbound=0"]),
    ("missing-manifest-dir", case_missing_manifest, 1,
     ["FAIL rule=missing-manifest dir=round-31",
      "MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
      "records=1 bound=1 unbound=0"]),
    ("record-without-url", case_record_without_url, 1,
     ["FAIL rule=url-mismatch record=S002 detail=absent dir=round-30",
      "records=2 bound=1 unbound=1"]),
    ("shared-url-between-two-records", case_shared_url_two_records, 0,
     ["MANIFEST round-30 records=2 url_bound=2 fetched=2 archival=0",
      "multi_row_url=2",
      "records=2 bound=2 unbound=0"]),
    ("duplicate-id-rows", case_duplicate_id_rows, 1,
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
    ("fetched-utc-pending-rejected", case_fetched_pending, 1,
     ["FAIL rule=fetched-utc record=S001 dir=round-32 detail=pending",
      "MANIFEST round-32 records=1 url_bound=1 fetched=0 archival=0",
      "records=1 bound=0 unbound=1"]),
    ("fetched-utc-local-offset-rejected", case_fetched_local_offset, 1,
     ["FAIL rule=fetched-utc record=S001 dir=round-32 detail=local-offset",
      "records=1 bound=0 unbound=1"]),
    ("per-file-orphan-detected", case_per_file_orphan_detected, 1,
     ["FAIL rule=orphan-capture file=S009.txt dir=round-30",
      "orphans=1 orphan=S009.txt",
      "records=1 bound=1 unbound=0"]),
    ("per-file-orphan-listed", case_per_file_orphan_listed, 0,
     ["orphans=1 orphan=S009.txt",
      "records=1 bound=1 unbound=0"]),
    ("nested-snapshot-dir", case_nested_snapshot, 0,
     ["MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
      "MANIFEST round-30/inner records=1 url_bound=1 fetched=1 archival=0",
      "snapshot_dirs=2 manifest_dirs=2 missing_manifest=0",
      "records=2 bound=2 unbound=0"]),
    ("nested-snapshot-missing-manifest", case_nested_missing_manifest, 1,
     ["FAIL rule=missing-manifest dir=round-31/inner",
      "snapshot_dirs=2 manifest_dirs=1 missing_manifest=1",
      "records=1 bound=1 unbound=0"]),
    ("dup-record-in-manifest", case_dup_record, 1,
     ["FAIL rule=dup-record field=id value=S001 count=2 dir=round-30",
      "FAIL rule=dup-record field=path value=S001.txt count=2 dir=round-30",
      "records=3 bound=3 unbound=0"]),
    ("double-https-row", case_double_https_row, 1,
     ["FAIL rule=double-https-row row=S001 n=2",
      "FAIL rule=url-ambiguous record=S001 row=S001 tokens=2 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("rejected-row-anchor", case_rejected_row_anchor, 1,
     ["FAIL rule=rejected-row-anchor record=S026 row=S026 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("capture-path-missing-rejected", case_capture_missing, 1,
     ["FAIL rule=capture-missing record=S001 path=S001.txt dir=round-30",
      "MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
      "records=1 bound=0 unbound=1"]),
    ("capture-path-escape-rejected", case_capture_escape, 1,
     ["FAIL rule=capture-missing record=S001 path=../S999.txt dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("digest-mismatch-rejected", case_digest_mismatch, 1,
     ["FAIL rule=digest-mismatch record=S001 sha256=",
      "records=1 bound=0 unbound=1"]),
    ("digest-invalid-rejected", case_digest_invalid, 1,
     ["FAIL rule=digest-invalid record=S001 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("digest-unpinned-modern-rejected", case_digest_unpinned_modern, 1,
     ["FAIL rule=digest-missing record=S001 dir=round-32",
      "records=1 bound=0 unbound=1"]),
    ("digest-unpinned-legacy-listed", case_digest_unpinned_legacy, 0,
     ["digest_unpinned=1",
      "records=1 bound=1 unbound=0"]),
    ("capture-url-mismatch-rejected", case_capture_url_mismatch, 1,
     ["FAIL rule=capture-url-mismatch record=S001 capture_url=",
      "records=1 bound=0 unbound=1"]),
    ("url-trailing-slash-rejected", case_url_trailing_slash, 1,
     ["FAIL rule=url-mismatch record=S001 row=S001 dir=round-30",
      "records=1 bound=0 unbound=1"]),
    ("snapshot-digest-mismatch-rejected", case_snapshot_digest_mismatch, 1,
     ["FAIL rule=digest-mismatch field=snapshot_sha256 record=S001 sha256=",
      "records=1 bound=0 unbound=1"]),
    ("snapshot-digest-matches", case_snapshot_digest_matches, 0,
     ["records=1 bound=1 unbound=0"]),
]


CASE_LINE_RE = re.compile(r"^selftest case=(\S+) exit=(-?\d+) want=(-?\d+) verdict=(\S+)$")
SUMMARY_RE = re.compile(r"^selftest cases=(\d+) failures=(\d+)$")


def judge_run(exit_code, stdout, want_exit, want_lines):
    """Problems with one fixture run: exit status, expected lines, no surprise FAIL."""
    problems = []
    if exit_code != want_exit:
        problems.append("exit=%d want=%d" % (exit_code, want_exit))
    for line in want_lines:
        if line not in stdout:
            problems.append("missing=%r" % line)
    if want_exit == 0 and "FAIL " in stdout:
        problems.append("unexpected-FAIL-line")
    return problems


def judge_selftest_report(text, expected_names):
    """Problems with a `--selftest` report: one case line per case plus a true summary.

    A report that prints only the summary is a failure, not a pass: a mutant that
    skips every fixture can print `selftest cases=N failures=0` without running a
    single case (round-33 F-5), so the summary is never sufficient evidence."""
    problems = []
    lines = [line.rstrip() for line in text.splitlines()]
    case_lines = [m for m in (CASE_LINE_RE.match(line) for line in lines) if m]
    if not case_lines:
        problems.append("summary-only-report")
    seen = {}
    for m in case_lines:
        name, code, want, verdict = m.group(1), m.group(2), m.group(3), m.group(4)
        seen[name] = seen.get(name, 0) + 1
        if verdict != "pass":
            problems.append("case-failed case=%s" % name)
        if code != want:
            problems.append("case-exit-mismatch case=%s exit=%s want=%s" % (name, code, want))
    for name in expected_names:
        if seen.get(name, 0) != 1:
            problems.append("case-line-count case=%s count=%d" % (name, seen.get(name, 0)))
    for name in sorted(seen):
        if name not in expected_names:
            problems.append("unexpected-case-line case=%s" % name)
    summaries = [m for m in (SUMMARY_RE.match(line) for line in lines) if m]
    if len(summaries) != 1:
        problems.append("summary-line-count count=%d" % len(summaries))
        return problems
    if int(summaries[0].group(1)) != len(expected_names):
        problems.append("summary-cases=%s want=%d" % (summaries[0].group(1), len(expected_names)))
    if int(summaries[0].group(2)) != 0:
        problems.append("summary-failures=%s" % summaries[0].group(2))
    return problems


def forged_summary_only(expected_names):
    """The round-33 F-5 mutant's report: a summary, no case lines."""
    return "selftest cases=%d failures=0\n" % len(expected_names)


def forged_complete(expected_names):
    """A well-formed report, to prove the report checker is not an always-reject limb."""
    return ("".join("selftest case=%s exit=0 want=0 verdict=pass\n" % name
                    for name in expected_names)
            + "selftest cases=%d failures=0\n" % len(expected_names))


REPORT_CASES = [
    # name, report factory, whether the report checker must accept it
    ("summary-only-selftest-rejected", forged_summary_only, False),
    ("complete-selftest-report-accepted", forged_complete, True),
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
    expected = ([name for name, _build, _want_exit, _want_lines in CASES]
                + [name for name, _factory, _expect_ok in REPORT_CASES])
    report, failures = [], 0
    try:
        for name, build, want_exit, want_lines in CASES:
            root = os.path.join(scratch, name)
            os.makedirs(root)
            build(root)
            proc = subprocess.run(
                [sys.executable, SCRIPT, "--root", root],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            problems = judge_run(proc.returncode, proc.stdout, want_exit, want_lines)
            if problems:
                failures += 1
            report.append("selftest case=%s exit=%d want=%d verdict=%s"
                          % (name, proc.returncode, want_exit, "pass" if not problems else "fail"))
            if problems:
                for problem in problems:
                    report.append("selftest problem=%s case=%s" % (problem, name))
                report.append("selftest stdout case=%s\n%s" % (name, proc.stdout.rstrip()))
                if proc.stderr:
                    report.append("selftest stderr case=%s\n%s" % (name, proc.stderr.rstrip()))
        for name, factory, expect_ok in REPORT_CASES:
            problems = judge_selftest_report(factory(expected), expected)
            observed, want = (0 if not problems else 1), (0 if expect_ok else 1)
            ok = (not problems) == expect_ok
            if not ok:
                failures += 1
            report.append("selftest case=%s exit=%d want=%d verdict=%s"
                          % (name, observed, want, "pass" if ok else "fail"))
            if not ok:
                report.append("selftest problem=report-verifier case=%s problems=%s"
                              % (name, problems))
        report.append("selftest cases=%d failures=%d" % (len(expected), failures))
        for line in report:
            print(line, file=out)
        if failures == 0:
            structural = judge_selftest_report("\n".join(report) + "\n", expected)
            if structural:
                print("selftest problem=self-report problems=%s" % structural, file=out)
                return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
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
