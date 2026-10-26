#!/usr/bin/env python3
"""Replay C1's three named mutants and count the survivors.

Usage: python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH]
       [--root DIR] [--scratch DIR] [--row-file PATH] [--json PATH] [--selftest]

The round-34 C1 counter. Round 33 measured its mutant set under a kill rule that
accepted a `--selftest` run printing no per-case evidence: a mutant that replaced
the case loop with a forged summary `selftest cases=0 failures=0` exited 0 and was
recorded as caught (verifier defect R4, round-33 F-5), and a mutant that dropped
rule B's url-required limb altered no summary the frozen rule read. This counter
replays the three named mutants against a COPY of the landed instrument bytes and
applies a tightened rule with two independent oracles:

  1. OUTPUT SHAPE. A `--selftest` run is accepted only when it prints one
     `selftest case=<name> exit=N want=N verdict=pass` line for every case, plus
     one `selftest cases=N failures=0` summary whose N equals the number of case
     lines, whose case-name multiset equals the PRISTINE bytes' case-name multiset,
     and (for the pristine run only) whose N is at least `CASE_FLOOR`. A run whose
     stdout carries only the summary is rejected as `summary-only`; a forged
     `cases=0` summary is rejected by the floor and by the case-set comparison.

  2. EXTERNAL FIXTURES. Each mutant also runs against eight fixture lanes built
     from scratch, one per documented failure family, so the verdict does not
     depend on the mutant's own selftest:

       record-without-url          a record with no `url` is unbound
                                   (exit 1, `detail=absent`, `unbound=1`);
       per-file-orphan             a capture file with no manifest record fails
                                   (exit 1, `rule=orphan-capture`,
                                   `orphans=1 orphan=S009.txt`);
       unnamed-record-id           a record with no `id` is `rule=no-row
                                   record=<unnamed>` (exit 1, `unbound=1`);
       stale-orphan-declaration    a declared orphan that is absent fails
                                   (exit 1, `rule=orphan-declared-missing`);
       malformed-fetched-utc       both malformed stamp paths fail with
                                   `rule=fetched-utc detail=malformed` (exit 1):
                                   an impossible UTC-shaped stamp and an
                                   unparsable string;
       punctuated-url-cell         a registry cell URL ending in `.` still binds
                                   its clean record url (exit 0, `url_bound=1`);
       malformed-orphan-declaration a declared orphan without a `reason` is an
                                   unreadable manifest (exit 2,
                                   `reason=manifest-shape`);
       nested-legacy-round         a nested `round-31/inner` dir is legacy: an
                                   archival record passes (exit 0).

     The last three (and the malformed fixture's second record) were added after
     attack seats reported behaviour-bearing survivors at earlier generations —
     `url-token-normalization-removal`, the malformed-orphans exit-2 limb and
     `parse_round`'s first-component split. Every reported survivor of the round is
     pinned; see "Limits" for what stays outside the set.

A named row is also pinned by digest. `ROW_PINS` holds the literal `find` and
`find\0replace` sha256 of each of the three named rows, so replacing a named patch
with a probe-invisible defect is `invalid:anchor-mismatch` (exit 1) instead of a
false zero, and the `named-rows` gate requires all three names to be present
exactly once. A row whose verdict is `killed` while `killed_by` is empty is
`invalid:inconsistent-kill`. What none of this can defend against is an edit that
rewrites the summary line itself; the header prints `counter_sha256`, so bind the
counter bytes before trusting the zero.

A mutant is KILLED iff at least one probe the pristine bytes pass is failed by the
mutant bytes. Every row is an exactly-once textual patch (QUALITY R17): `find`
must occur exactly once, the patch must change bytes, and the mutant must compile
(`py_compile`) before any probe runs. A row that cannot be evaluated is
`invalid:<reason>` — it is never relabelled killed and never counted as a survivor.

Controls, all exercised on every run:

  CTL-noop        a `find`/`replace` pair that changes nothing: `invalid:noop`,
                  never a kill.
  CTL-nocompile   an exactly-once patch that breaks Python syntax: a mutant that
                  cannot compile is `invalid:nocompile`, never a kill.
  CTL-equivalent  a comment-only patch that compiles and changes bytes: no probe
                  can see it, so it is a `survivor` — the witness that this
                  counter reports survivors>0 (and aggregate exit 1) instead of
                  being an always-zero printer.
  CTL-fake        the do-nothing fake runner (newest
                  `.ufo/waves/round-*/c1-controls/fake-killrule.py`, overridable
                  with `--fake`): it prints `survivors=0` without replaying any
                  mutant. Its span carries no `mutant=` line, no patch digest and
                  no `mutants=` line (`verdict=opaque`), and it still prints
                  `survivors=0` on the survivor witness — the real tool must
                  differ on both counts (`differs=1`). A fake that produced a
                  full evidence span would be `evidential` and fail this control.

Output. One `KILL-RULE ...` header (instrument path, digest, bytes, floor), one
`probe <name> pristine=...` line per pristine probe, then per row a
`mutant-patch` line, one `mutant-probe` line per probe, and the claimed line
`mutant=<name> killed=0|1`; then one `control=<id> ... ok=0|1` line per control,
`controls=<n> rejected=<k>`, `mutants=<n> killed=<k> survivors=<k> invalid=<k>`,
`gates=<n> failed=<k>`, and finally `survivors=<K>`. Exit 0 iff survivors=0, no
row is invalid and every gate holds; 1 on any failed measurement or gate; 2 on a
usage or read error.

An attack seat can add its own rows without editing this file: `--row-file PATH`
takes `{"rows": [{"name": ..., "find": ..., "replace": ..., "note": ...}]}` (a bare
list is accepted too). Extra rows are measured by the same prepare/evaluate path,
printed as `mutant=<name> killed=0|1`, and counted in `survivors` — so a
deliberately surviving row makes the run print `survivors=1` and exit 1, which is
the sanctioned way to demonstrate the red aggregate. The three named rows always
run; a row file cannot remove or relabel them.

Limits (measured, not assumed):

- The instrument under test is a moving target: the patch anchors are bound to the
  bytes measured now, and `find`-count is enforced, so different instrument bytes
  produce `invalid:find-count` (exit 1) rather than a silent zero. The three named
  patches are additionally pinned by `ROW_PINS`, so a substituted named row is
  `invalid:anchor-mismatch`.
- The fixture probes assert the contract lines the instrument documents, not every
  line it prints. The set pins every limb an attack seat named this round plus the
  three named mutants' limbs; it is a bounded oracle, not an equivalence test, and
  a mutant that leaves every asserted line intact survives by construction.
- `killed` means "a probe the pristine bytes pass is failed by the mutant". It is
  not a claim that the mutated limb is the only cause of the difference.
- A kill can rest on the shape gate alone (mutant 1, a selftest-only defect); the
  counter never invents an external probe for it.
- The counter cannot defend against an edit that rewrites its own summary line. It
  refuses row substitutions and inconsistent verdicts, and prints `counter_sha256`,
  so the bytes must be bound before the zero is trusted.
- The fake control binds to the wave tree under the lane root. Later rounds that
  move `c1-controls/fake-killrule.py` make the control `absent` (ok=0) until the
  path is supplied with `--fake`; it is never silently skipped.

`--selftest` checks this counter's own verdict arithmetic (green, one survivor,
one invalid row), not the instrument: three internal scenarios, no subprocess.
"""
import argparse
import hashlib
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

LANE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_INSTRUMENT = "corpus/instruments/capture-binding-check.py"
CASE_FLOOR = 19          # frozen C1 conjunct: `--selftest` prints cases=N with N >= 19
TIMEOUT_SECONDS = 600

CASE_LINE_RE = re.compile(r"^selftest case=(\S+) exit=(-?\d+) want=(-?\d+) verdict=(\S+)$")
SUMMARY_RE = re.compile(r"^selftest cases=(\d+) failures=(\d+)$")
FAKE_ROUND_RE = re.compile(r"round-(\d+)\Z")

# --- rows: every patch is an exactly-once `find`/`replace` over the instrument bytes

MUTANTS = [
    {
        "name": "skip-selftest-summary",
        "note": "forges the round-33 F-5 report: the case loop is never reached, so "
                "`--selftest` prints `selftest cases=0 failures=0` and exits 0",
        "find": ("    base = scratch_base(scratch_arg)\n"
                 "    os.makedirs(base, exist_ok=True)\n"),
        "replace": ('    print("selftest cases=0 failures=0", file=out)\n'
                    "    return 0\n"
                    "    base = scratch_base(scratch_arg)\n"
                    "    os.makedirs(base, exist_ok=True)\n"),
    },
    {
        "name": "accept-record-without-url",
        "note": "drops rule B's url-required limb: a manifest record with no `url` "
                "binds (the round-33 plain-run survivor)",
        "find": ('    url = record.get("url")\n'
                 "    if not (isinstance(url, str) and url.strip()):\n"
                 '        return False, ["rule=url-mismatch record=%s detail=absent" '
                 "% record_id]\n"),
        "replace": ('    url = record.get("url")\n'
                    "    if not (isinstance(url, str) and url.strip()):\n"
                    "        return True, []\n"),
    },
    {
        "name": "per-file-binding-removal",
        "note": "drops rule A's per-file orphan detection: a capture file with no "
                "manifest record is neither listed nor failed",
        "find": ("            orphans.append((name, capture))\n"
                 "            if capture not in declared:\n"
                 '                failures.append("FAIL rule=orphan-capture file=%s '
                 'dir=%s" % (capture, name))\n'),
        "replace": ("            if capture not in declared:\n"
                    "                pass  # mutant: per-file orphan detection dropped\n"),
    },
]


# The three named rows are pinned by digest: `find` and `find\0replace` sha256 are
# literal constants, so substituting a different patch under a named row is
# `invalid:anchor-mismatch` and the run exits 1. `--row-file` rows are deliberately
# unpinned (an attack seat may test any patch), but they may not reuse a named row's
# name. Changing a named patch is therefore a visible edit to MUTANTS **and** ROW_PINS.
ROW_PINS = {
    "skip-selftest-summary": (
        "e6262244cffa1e1ecd5a1703c701356bf632b5413ca87be220d17b38211587d9",
        "c457083e5d99f9f0e3e6a2da8c3aa2381025925294b5a3131248a91902ad561a"),
    "accept-record-without-url": (
        "cbf461982c746e9dc27cded492b2dfa8ae6b11d140fd54f05b053bc68a939148",
        "83cbd622ad2fd1e26cfe2cedaf7e919be840f997084eb8f8f41ab06e61a98637"),
    "per-file-binding-removal": (
        "f1a44079b9477ef222bb422bcccc59f91127d96464ccc7b9979132c8b0ea9a80",
        "f872ef12408d9162e2386817b3904a197c5ca37f531e9386896dbc5c23838427"),
}


def control_rows():
    """The three patch-shape controls, bound to real anchors of the instrument."""
    return [
        {"id": "CTL-noop", "expect": "invalid:noop",
         "find": "SCHEMA_VERSION = 1",
         "replace": "SCHEMA_VERSION = 1"},
        {"id": "CTL-nocompile", "expect": "invalid:nocompile",
         "find": "def parse_round(dirname):",
         "replace": "def parse_round(dirname)"},
        {"id": "CTL-equivalent", "expect": "survivor",
         "find": "# --- selftest -------------------------------------------------------"
                 "----------",
         "replace": "# --- selftest (comment-only patch) ---------------------------"
                    "------------------"},
    ]


# --- fixtures: the instrument's own fixture shape, so the two cannot drift on
# --- how a registry row or a manifest is written

FIXTURE_HEADER = (
    "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|\n"
)
ALPHA = "https://example.invalid/alpha"
BETA = "https://example.invalid/beta"
STAMP = "2026-10-25T00:00:00Z"


def write_registry(root, rows):
    """Write a fixture registry: one table row per (id, source cell[, status])."""
    os.makedirs(os.path.join(root, "corpus"), exist_ok=True)
    lines = [FIXTURE_HEADER]
    for row in rows:
        row_id, cell = row[0], row[1]
        status = row[2] if len(row) > 2 else "mined"
        lines.append("| %s | Fixture source — %s | docs | A | scope | anchor | teaches | %s "
                     "| 2026-10-25 | 180d | — |\n" % (row_id, cell, status))
    with open(os.path.join(root, "corpus", "SOURCES.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(lines))


def write_manifest(root, dirname, records, orphans=None):
    """Write a fixture snapshot directory with its manifest and one capture per record."""
    path = os.path.join(root, "corpus", "source-snapshots", dirname)
    os.makedirs(path, exist_ok=True)
    for record in records:
        capture = record.get("path")
        if isinstance(capture, str):
            with open(os.path.join(path, capture), "w", encoding="utf-8") as fh:
                fh.write("fixture capture bytes for %s\n" % record.get("id", "?"))
    payload = {"schema_version": 1, "purpose": "kill-rule-check fixture",
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
    item = {"id": record_id, "path": "%s.txt" % (record_id or "unnamed"),
            "sha256": "0" * 64, "quotes": []}
    if url is not None:
        item["url"] = url
    if fetched is not None:
        item["fetched_utc"] = fetched
    if archival is not None:
        item["archival"] = archival
    return item


def build_url_less(root):
    """S001 binds; S002 carries no `url` at all (round-33's plain-run survivor)."""
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP),
                                      record("S002", archival=True)])


def build_per_file_orphan(root):
    """S009.txt sits in a manifest directory with no record naming it."""
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])
    write_capture_file(root, "round-30", "S009.txt")


def build_unnamed_record(root):
    """One manifest record carries no `id` (the `<unnamed>` diagnostic limb)."""
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record(None, url=ALPHA, fetched=STAMP)])


def build_stale_orphan(root):
    """The manifest declares an orphan file that is not in its directory."""
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)],
                   orphans=[{"path": "S077.txt", "reason": "fixture: listed, absent"}])


def build_malformed_fetched(root):
    """Two round-32 records carry malformed stamps: one impossible UTC-shaped, one garbage.

    The instrument has two `malformed` paths — a UTC-shaped stamp the datetime
    constructor rejects, and a string that matches neither stamp shape — so one
    record exercises each."""
    write_registry(root, [("S001", ALPHA), ("S002", BETA)])
    write_manifest(root, "round-32", [record("S001", url=ALPHA,
                                             fetched="2026-13-45T99:99:99Z"),
                                      record("S002", url=BETA, fetched="yesterday")])


def build_punctuated_url_cell(root):
    """The registry cell's URL ends in a period; row_tokens strips it, so the record binds."""
    write_registry(root, [("S001", ALPHA + ".")])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)])


def build_malformed_orphan_declaration(root):
    """A declared orphan object carries no `reason`: an unreadable manifest (exit 2)."""
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-30", [record("S001", url=ALPHA, fetched=STAMP)],
                   orphans=[{"path": "S009.txt"}])


def build_nested_legacy_round(root):
    """A nested directory's round is read from its first path component (`round-31/inner`)."""
    write_registry(root, [("S001", ALPHA)])
    write_manifest(root, "round-31/inner", [record("S001", url=ALPHA, archival=True)])


PROBES = [
    # name, kind, fixture builder, expected exit, expected stdout substrings
    {"name": "selftest-shape", "kind": "selftest"},
    {"name": "record-without-url", "kind": "fixture", "builder": build_url_less,
     "want_exit": 1, "want_lines": ("detail=absent", "unbound=1")},
    {"name": "per-file-orphan", "kind": "fixture", "builder": build_per_file_orphan,
     "want_exit": 1, "want_lines": ("rule=orphan-capture", "orphans=1 orphan=S009.txt")},
    {"name": "unnamed-record-id", "kind": "fixture", "builder": build_unnamed_record,
     "want_exit": 1, "want_lines": ("rule=no-row record=<unnamed>", "unbound=1")},
    {"name": "stale-orphan-declaration", "kind": "fixture", "builder": build_stale_orphan,
     "want_exit": 1, "want_lines": ("rule=orphan-declared-missing file=S077.txt", "orphans=0")},
    {"name": "malformed-fetched-utc", "kind": "fixture", "builder": build_malformed_fetched,
     "want_exit": 1, "want_lines": ("record=S001 dir=round-32 detail=malformed",
                                    "record=S002 dir=round-32 detail=malformed")},
    {"name": "punctuated-url-cell", "kind": "fixture", "builder": build_punctuated_url_cell,
     "want_exit": 0, "want_lines": ("MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0",
                                    "records=1 bound=1 unbound=0")},
    {"name": "malformed-orphan-declaration", "kind": "fixture",
     "builder": build_malformed_orphan_declaration,
     "want_exit": 2, "want_lines": ("reason=manifest-shape",)},
    {"name": "nested-legacy-round", "kind": "fixture", "builder": build_nested_legacy_round,
     "want_exit": 0, "want_lines": ("MANIFEST round-31/inner records=1 url_bound=1 fetched=0 archival=1",
                                    "records=1 bound=1 unbound=0")},
]


# --- measurement ---------------------------------------------------------------


def slug(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_text(text):
    return sha256_bytes(text.encode("utf-8"))


def scratch_base(arg=None):
    """Scratch root: explicit arg, else $HYAKU_SCRATCH, else $TMPDIR, else a default."""
    for candidate in (arg, os.environ.get("HYAKU_SCRATCH"), os.environ.get("TMPDIR")):
        if candidate:
            return candidate
    return "/fast/scratch/hyaku" if os.path.isdir("/fast/scratch") else tempfile.gettempdir()


def run_once(command, cwd, env):
    try:
        proc = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, timeout=TIMEOUT_SECONDS,
                              env=env)
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": "", "stderr": "", "timed_out": True}
    return {"exit": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
            "timed_out": False}


def run_twice(command, cwd, env):
    """Run twice; a run whose (exit, stdout) moves is not a measurement."""
    first = run_once(command, cwd, env)
    second = run_once(command, cwd, env)
    stable = (first["timed_out"] == second["timed_out"]
              and first["exit"] == second["exit"]
              and first["stdout"] == second["stdout"])
    return first, stable


def display_exit(run):
    return "timeout" if run["timed_out"] else str(run["exit"])


def probe_env(scratch):
    """Keep any tempfile the instrument creates inside this run's scratch tree."""
    env = dict(os.environ)
    env["TMPDIR"] = scratch
    env["HYAKU_SCRATCH"] = scratch
    return env


def accept_selftest(run, ref_names, floor):
    """Judge one `--selftest` span. Returns (ok, reasons, case names).

    `ref_names is None` is the pristine side, judged against `floor`; a mutant side
    is judged against the pristine case-name multiset, because the floor is the
    instrument's obligation (C1's `cases>=19` conjunct), not the mutant's."""
    reasons = []
    if run["timed_out"]:
        return False, ["timeout"], []
    if run["exit"] != 0:
        reasons.append("exit=%s" % display_exit(run))
    cases = [(m.group(1), m.group(4)) for m in
             (CASE_LINE_RE.match(line) for line in run["stdout"].splitlines()) if m]
    summaries = [m for m in (SUMMARY_RE.match(line) for line in
                             run["stdout"].splitlines()) if m]
    names = [name for name, _verdict in cases]
    if not cases:
        reasons.append("summary-only")
    if not summaries:
        reasons.append("no-summary")
    else:
        if len(summaries) != 1:
            reasons.append("summary-line-count=%d" % len(summaries))
        count, failures = int(summaries[0].group(1)), int(summaries[0].group(2))
        if failures != 0:
            reasons.append("failures=%d" % failures)
        if count != len(cases):
            reasons.append("cases=%d case-lines=%d" % (count, len(cases)))
        if ref_names is None:
            if count < floor:
                reasons.append("cases=%d<floor=%d" % (count, floor))
        elif sorted(names) != sorted(ref_names):
            reasons.append("case-set-mismatch")
    if any(verdict != "pass" for _name, verdict in cases):
        reasons.append("case-verdict")
    if len(set(names)) != len(names):
        reasons.append("dup-case")
    return (not reasons), reasons, names


def measure_probe(instrument_path, probe, scratch, fixtures, ref_names, floor, side):
    """Run one probe against one instrument copy. Returns dict(ok, stable, exit, reasons)."""
    if probe["kind"] == "selftest":
        probe_scratch = os.path.join(scratch, "selftest", side)
        os.makedirs(probe_scratch, exist_ok=True)
        command = [sys.executable, instrument_path, "--selftest", "--scratch", probe_scratch]
    else:
        command = [sys.executable, instrument_path, "--root", fixtures[probe["name"]]]
    run, stable = run_twice(command, scratch, probe_env(scratch))
    if probe["kind"] == "selftest":
        ok, reasons, names = accept_selftest(run, ref_names, floor)
    else:
        reasons = []
        if run["timed_out"]:
            reasons.append("timeout")
        elif run["exit"] != probe["want_exit"]:
            reasons.append("exit=%s want=%d" % (display_exit(run), probe["want_exit"]))
        for want in probe["want_lines"]:
            if want not in run["stdout"]:
                reasons.append("missing=%r" % want)
        ok, names = (not reasons), []
    if not stable:
        reasons.append("nondeterministic")
        ok = False
    return {"ok": ok, "stable": stable, "exit": run["exit"],
            "timed_out": run["timed_out"], "reasons": reasons, "names": names,
            "stdout": run["stdout"]}


def prepare_patch(row, pristine_bytes, scratch, base):
    """Apply the row's exactly-once patch. Returns (status, path, mutant_bytes, detail)."""
    find = row["find"].encode("utf-8")
    replace = row["replace"].encode("utf-8")
    count = pristine_bytes.count(find)
    if count != 1:
        return "invalid:find-count", None, None, "find-count=%d" % count
    mutant = pristine_bytes.replace(find, replace, 1)
    if mutant == pristine_bytes:
        return "invalid:noop", None, None, "bytes-unchanged"
    row_dir = os.path.join(scratch, "rows", slug(row["name"]))
    os.makedirs(row_dir, exist_ok=True)
    path = os.path.join(row_dir, base)
    with open(path, "wb") as fh:
        fh.write(mutant)
    try:
        py_compile.compile(path, cfile=os.path.join(row_dir, "compiled.pyc"), doraise=True)
    except py_compile.PyCompileError as exc:
        detail = str(exc).splitlines()[0] if str(exc) else "PyCompileError"
        return "invalid:nocompile", path, mutant, detail
    return "ok", path, mutant, None


def evaluate(row, pristine_bytes, pristine_probes, pristine_names, scratch, fixtures, base):
    """Replay one row. Returns a result dict; prints nothing."""
    find = row["find"].encode("utf-8")
    result = {
        "name": row["name"],
        "note": row.get("note", ""),
        "find_count": pristine_bytes.count(find),
        "patch_sha256": sha256_text(row["find"] + "\x00" + row["replace"]),
        "find_sha256": sha256_text(row["find"]),
    }
    pinned = ROW_PINS.get(row["name"])
    if pinned is not None and (result["find_sha256"], result["patch_sha256"]) != pinned:
        result.update({"status": "invalid:anchor-mismatch",
                       "detail": "find-or-patch-digest",
                       "verdict": "invalid:anchor-mismatch",
                       "probes": [], "killed_by": []})
        return result
    status, path, mutant, detail = prepare_patch(row, pristine_bytes, scratch, base)
    result["status"] = status
    if status != "ok":
        result.update({"verdict": status, "detail": detail, "probes": [], "killed_by": []})
        return result
    result["mutant_sha256"] = sha256_bytes(mutant)
    probe_rows, killed_by, unstable = [], [], False
    for probe in PROBES:
        side = measure_probe(path, probe, scratch, fixtures, pristine_names, None,
                             "row-" + slug(row["name"]))
        baseline = pristine_probes[probe["name"]]
        probe_rows.append({"probe": probe["name"], "pristine": "pass" if baseline["ok"] else "fail",
                           "mutant": "pass" if side["ok"] else "fail",
                           "reasons": side["reasons"], "exit": side["exit"]})
        if not side["stable"]:
            unstable = True
            continue
        if baseline["ok"] and not side["ok"]:
            killed_by.append(probe["name"])
    result["probes"] = probe_rows
    result["killed_by"] = killed_by
    if unstable:
        result["verdict"] = "invalid:nondeterministic"
    else:
        result["verdict"] = "killed" if killed_by else "survivor"
    if result["verdict"] == "killed" and not killed_by:
        result["verdict"] = "invalid:inconsistent-kill"
    return result


def summarise(verdicts):
    """(killed, survivors, invalid, exit) for one verdict vector."""
    killed = sum(1 for verdict in verdicts if verdict == "killed")
    survivors = sum(1 for verdict in verdicts if verdict == "survivor")
    invalid = sum(1 for verdict in verdicts if verdict.startswith("invalid:"))
    return killed, survivors, invalid, (1 if (survivors or invalid) else 0)


def load_extra_rows(paths):
    """Read `--row-file` rows: {"rows": [...]} (or a bare list) of patch rows."""
    rows = []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            payload = json.load(fh)
        entries = payload.get("rows") if isinstance(payload, dict) else payload
        if not isinstance(entries, list):
            raise ValueError("%s: no rows list" % path)
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise ValueError("%s: row %d is not an object" % (path, index))
            for field in ("name", "find", "replace"):
                if not (isinstance(entry.get(field), str) and entry[field]):
                    raise ValueError("%s: row %d has no %s" % (path, index, field))
            reserved = {row["name"] for row in MUTANTS}
            if entry["name"] in reserved or any(seen["name"] == entry["name"] for seen in rows):
                raise ValueError("%s: row %d reuses the name %r"
                                 % (path, index, entry["name"]))
            rows.append({"name": entry["name"], "find": entry["find"],
                         "replace": entry["replace"], "note": entry.get("note", "")})
    return rows


def default_fake(root):
    """The newest committed do-nothing fake runner under .ufo/waves/round-*/c1-controls/."""
    base = os.path.join(root, ".ufo", "waves")
    if not os.path.isdir(base):
        return None
    best = None
    for name in os.listdir(base):
        match = FAKE_ROUND_RE.match(name)
        if not match:
            continue
        path = os.path.join(base, name, "c1-controls", "fake-killrule.py")
        if os.path.isfile(path):
            key = int(match.group(1))
            if best is None or key > best[0]:
                best = (key, path)
    return best[1] if best else None


def fake_control(fake_path, expected_rows, witness_survivors, scratch, out):
    """Reject a runner that prints `survivors=0` without replaying anything."""
    if not fake_path:
        print("control=CTL-fake-killrule verdict=absent expect=opaque ok=0 "
              "reason=no-fake-under-.ufo/waves/round-*/c1-controls/", file=out)
        return {"ok": False, "verdict": "absent"}
    run, stable = run_twice([sys.executable, fake_path], scratch, probe_env(scratch))
    lines = [line.strip() for line in run["stdout"].splitlines()]
    mutant_lines = sum(1 for line in lines if line.startswith("mutant="))
    patch_digests = sum(1 for line in lines if "patch_sha256=" in line)
    mutants_line = sum(1 for line in lines if line.startswith("mutants="))
    survivors = None
    for line in lines:
        match = re.match(r"^survivors=(\d+)$", line)
        if match:
            survivors = int(match.group(1))
    evidential = (mutant_lines == expected_rows and patch_digests == expected_rows
                  and mutants_line == 1)
    verdict = "evidential" if evidential else "opaque"
    differs = int(mutant_lines == 0 and survivors == 0 and witness_survivors >= 1
                  and expected_rows >= 1)
    ok = verdict == "opaque" and differs == 1 and stable
    print("control=CTL-fake-killrule verdict=%s expect=opaque ok=%d fake=%s fake_exit=%s "
          "fake_mutant_lines=%d fake_patch_digests=%d fake_mutants_line=%d "
          "fake_survivors=%s real_mutant_lines=%d witness_survivors=%d differs=%d "
          "stable=%d"
          % (verdict, 1 if ok else 0, fake_path, display_exit(run), mutant_lines,
             patch_digests, mutants_line,
             "none" if survivors is None else survivors, expected_rows,
             witness_survivors, differs, 1 if stable else 0), file=out)
    return {"ok": ok, "verdict": verdict, "differs": differs}


# --- selftest: this counter's own verdict arithmetic ----------------------------


def selftest():
    """Three arithmetic scenarios for `summarise()`; no instrument, no subprocess."""
    scenarios = [
        ("all-killed", ["killed", "killed", "killed"], (3, 0, 0, 0)),
        ("one-survivor", ["killed", "survivor", "killed"], (2, 1, 0, 1)),
        ("one-invalid", ["killed", "invalid:find-count", "killed"], (2, 0, 1, 1)),
    ]
    failures = 0
    for name, verdicts, want in scenarios:
        got = summarise(verdicts)
        ok = got == want
        if not ok:
            failures += 1
        print("selftest case=%s got=%s want=%s verdict=%s"
              % (name, got, want, "pass" if ok else "fail"))
    print("selftest cases=%d failures=%d" % (len(scenarios), failures))
    return 0 if failures == 0 else 1


# --- main ----------------------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=LANE_ROOT,
                        help="lane root (default: three directories above this script)")
    parser.add_argument("--instrument", default=None,
                        help="instrument under test (default %s)" % DEFAULT_INSTRUMENT)
    parser.add_argument("--fake", default=None,
                        help="fake runner control (default: newest "
                             ".ufo/waves/round-*/c1-controls/fake-killrule.py)")
    parser.add_argument("--row-file", action="append", default=None,
                        help="extra mutant rows as JSON ({\"rows\": [...]}); repeatable, "
                             "measured and counted like the named rows")
    parser.add_argument("--scratch", default=None,
                        help="scratch root (default $HYAKU_SCRATCH, then $TMPDIR)")
    parser.add_argument("--json", default=None, help="write the measurement as JSON")
    parser.add_argument("--selftest", action="store_true",
                        help="check this counter's verdict arithmetic instead of the lane")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    out = sys.stdout
    root = os.path.abspath(args.root)
    instrument_ref = args.instrument or DEFAULT_INSTRUMENT
    instrument_path = (instrument_ref if os.path.isabs(instrument_ref)
                       else os.path.join(root, instrument_ref))
    base = os.path.basename(instrument_path)
    try:
        with open(instrument_path, "rb") as fh:
            pristine_bytes = fh.read()
    except OSError as exc:
        print("UNAVAILABLE reason=instrument %s" % exc, file=out)
        return 2
    if not instrument_path.startswith(root + os.sep):
        instrument_ref = instrument_path

    rows = list(MUTANTS)
    if args.row_file:
        try:
            rows.extend(load_extra_rows(args.row_file))
        except (OSError, ValueError) as exc:
            print("UNAVAILABLE reason=row-file %s" % exc, file=out)
            return 2

    scratch_root = scratch_base(args.scratch)
    os.makedirs(scratch_root, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="kill-rule-", dir=scratch_root)
    try:
        print("KILL-RULE instrument=%s sha256=%s bytes=%d lines=%d floor=%d counter_sha256=%s"
              % (instrument_ref, sha256_bytes(pristine_bytes), len(pristine_bytes),
                 pristine_bytes.count(b"\n"), CASE_FLOOR,
                 sha256_bytes(open(os.path.abspath(__file__), "rb").read())), file=out)

        pristine_dir = os.path.join(scratch, "pristine")
        os.makedirs(pristine_dir)
        pristine_path = os.path.join(pristine_dir, base)
        with open(pristine_path, "wb") as fh:
            fh.write(pristine_bytes)

        fixtures = {}
        fixture_root = os.path.join(scratch, "fixtures")
        for probe in PROBES:
            if probe["kind"] != "fixture":
                continue
            path = os.path.join(fixture_root, probe["name"])
            os.makedirs(path)
            probe["builder"](path)
            fixtures[probe["name"]] = path

        pristine_probes, pristine_names = {}, []
        for probe in PROBES:
            measured = measure_probe(pristine_path, probe, scratch, fixtures, None,
                                     CASE_FLOOR, "pristine")
            pristine_probes[probe["name"]] = measured
            if probe["kind"] == "selftest":
                pristine_names = measured["names"]
            print("probe %s pristine=%s exit=%s%s"
                  % (probe["name"], "pass" if measured["ok"] else "fail",
                     display_exit(measured),
                     "" if measured["ok"] else
                     " reasons=%s" % ";".join(measured["reasons"])), file=out)
        if pristine_probes["selftest-shape"]["ok"]:
            print("pristine selftest cases=%d case-lines=%d floor=%d floor_met=1"
                  % (len(pristine_names), len(pristine_names), CASE_FLOOR), file=out)
        else:
            print("pristine selftest-refused reasons=%s"
                  % ";".join(pristine_probes["selftest-shape"]["reasons"]), file=out)

        results = []
        for row in rows:
            result = evaluate(row, pristine_bytes, pristine_probes, pristine_names,
                              scratch, fixtures, base)
            results.append(result)
            print("mutant-patch name=%s patch_sha256=%s find_sha256=%s find_count=%d "
                  "status=%s%s"
                  % (row["name"], result["patch_sha256"][:16], result["find_sha256"][:16],
                     result["find_count"], result["status"],
                     "" if result["status"] == "ok" else
                     " detail=%s" % result.get("detail", "")), file=out)
            if result["status"] == "ok":
                print("mutant-bytes name=%s pristine_sha256=%s mutant_sha256=%s"
                      % (row["name"], sha256_bytes(pristine_bytes)[:16],
                         result["mutant_sha256"][:16]), file=out)
            for probe in result["probes"]:
                print("mutant-probe name=%s probe=%s pristine=%s mutant=%s exit=%s%s"
                      % (row["name"], probe["probe"], probe["pristine"], probe["mutant"],
                         probe["exit"],
                         "" if probe["mutant"] == "pass" else
                         " reasons=%s" % ";".join(probe["reasons"])), file=out)
            print("mutant=%s killed=%d"
                  % (row["name"], 1 if result["verdict"] == "killed" else 0), file=out)
            if result["verdict"].startswith("invalid:"):
                print("mutant-invalid name=%s status=%s detail=%s"
                      % (row["name"], result["verdict"], result.get("detail", "")), file=out)

        killed, survivors, invalid, _exit = summarise([r["verdict"] for r in results])

        controls, control_ok = [], True
        witness_survivors = 0
        for control in control_rows():
            row = {"name": control["id"], "find": control["find"],
                   "replace": control["replace"], "note": control["id"]}
            result = evaluate(row, pristine_bytes, pristine_probes, pristine_names,
                              scratch, fixtures, base)
            ok = result["verdict"] == control["expect"]
            control_ok = control_ok and ok
            controls.append({"id": control["id"], "expect": control["expect"],
                             "verdict": result["verdict"], "ok": ok})
            if result["verdict"] == "survivor":
                witness_survivors = summarise(["survivor"])[1]
            witness = ""
            if control["id"] == "CTL-equivalent":
                w_killed, w_survivors, w_invalid, w_exit = summarise([result["verdict"]])
                witness = (" witness_survivors=%d witness_exit=%d"
                           % (w_survivors, w_exit))
                witness_survivors = w_survivors
            print("control=%s verdict=%s expect=%s ok=%d%s"
                  % (control["id"], result["verdict"], control["expect"],
                     1 if ok else 0, witness), file=out)
            if not ok:
                print("control-detail=%s status=%s probes=%s"
                      % (control["id"], result.get("status"),
                         [(p["probe"], p["mutant"], p["reasons"])
                          for p in result.get("probes", [])]), file=out)

        fake = fake_control(args.fake or default_fake(root), len(results),
                            witness_survivors, scratch, out)
        control_ok = control_ok and fake["ok"]
        rejected = sum(1 for control in controls if control["ok"]) + (1 if fake["ok"] else 0)
        print("controls=%d rejected=%d" % (len(controls) + 1, rejected), file=out)

        named_counts = {name: sum(1 for seen in rows if seen["name"] == name)
                        for name in ROW_PINS}
        named_ok = (set(named_counts) == {row["name"] for row in MUTANTS}
                    and all(count == 1 for count in named_counts.values()))
        gates = [
            ("named-rows", named_ok),
            ("pristine-selftest", pristine_probes["selftest-shape"]["ok"]),
            ("pristine-fixtures", all(pristine_probes[p["name"]]["ok"] for p in PROBES
                                      if p["kind"] == "fixture")),
            ("pristine-determinism", all(pristine_probes[p["name"]]["stable"] for p in PROBES)),
            ("rows-valid", invalid == 0),
            ("controls", control_ok),
            ("survivors-zero", survivors == 0),
        ]
        failed = 0
        for name, ok in gates:
            if not ok:
                failed += 1
            print("GATE %s name=%s" % ("ok" if ok else "fail", name), file=out)

        print("mutants=%d killed=%d survivors=%d invalid=%d"
              % (len(results), killed, survivors, invalid), file=out)
        print("gates=%d failed=%d" % (len(gates), failed), file=out)
        print("survivors=%d" % survivors, file=out)

        if args.json:
            payload = {
                "schema": "kill-rule-check-v1",
                "instrument": instrument_ref,
                "instrument_sha256": sha256_bytes(pristine_bytes),
                "instrument_bytes": len(pristine_bytes),
                "case_floor": CASE_FLOOR,
                "pristine": {name: {"ok": value["ok"], "stable": value["stable"],
                                    "exit": value["exit"], "reasons": value["reasons"]}
                             for name, value in pristine_probes.items()},
                "pristine_case_names": pristine_names,
                "mutants": results,
                "controls": controls,
                "fake": fake,
                "killed": killed,
                "survivors": survivors,
                "invalid": invalid,
                "gates_failed": failed,
            }
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=1, sort_keys=True)
                fh.write("\n")

        return 0 if (survivors == 0 and invalid == 0 and failed == 0) else 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
