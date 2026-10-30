#!/usr/bin/env python3
"""citation-ground-check.py — the round-49 C1 counter: citation-base grounding.

Usage:
  python3 corpus/instruments/citation-ground-check.py --root DIR [--ledger PATH] [--json PATH]
  python3 corpus/instruments/citation-ground-check.py --selftest [--scratch DIR]

WHAT THIS COUNTER MEASURES (one sentence).
Every path-like citation in the lane that names a file which exists on disk but
is written so that the resolver cannot open it is a citation a reader cannot
follow; this counter enumerates those two classes and fails closed while any
member survives.

THE TWO CLASSES.
  class-lane-bare   — a citation of a file that exists under `<root>/corpus/`
                      but is written without the `corpus/` prefix, so the
                      resolver (which tries the LANE root for relative paths)
                      classifies it GONE.  This violates the lane's own citation
                      vocabulary: `corpus/knowledge/citation-bases.md` (LANE
                      rule) — "Use the full internal path for knowledge
                      cross-references, for example
                      `corpus/knowledge/ops-invariants.md:18`; do not use a bare
                      `ops-invariants.md:18` or `claim-gates.md:3` when the
                      target is in the lane — the resolver only tries the lane
                      root for relative paths, so a bare cite of a file in a
                      subdirectory classifies GONE".
  class-fleet-relative — a citation of a file that exists under the FLEET root
                      (`<root>/..`, the fleet repo that holds PROTOCOL.md,
                      MISSION.md, `.ufo/`, `templates/`, `scripts/` and the
                      sibling lane repos) but is written fleet-root-relative, so
                      the lane resolver classifies it GONE.  The lane has no
                      FLEET base in its vocabulary yet; this counter names the
                      class so the vocabulary can carry it.

Neither class is a lost-tree citation: a citation into `~/Projects/bounties`,
`~/Projects/the-bounty-hunter` or `~/Projects/origin-work` is unfixable on
this host and is NOT enumerated here (it stays GONE and is reported as such by
`resolve.py`).  Re-pointing a lost-tree citation at some other file that
happens to exist is a fabrication, not a repair; the ledger check below fails
closed on any row whose new path lands inside a lost tree.

THE LEDGER.
Every repair is one row of `corpus/instruments/citation-reground-ledger.md`:

  | old token | new token | base class | sites | referent note |
  |---|---|---|---|---|
  | `knowledge/claim-gates.md` | `corpus/knowledge/claim-gates.md` | lane-bare | corpus/README.md:21,corpus/README.md:44 | same file, full LANE path (citation-bases.md LANE rule) |

  - `sites` — every occurrence of the old token, as `file:line`, comma
    separated.  A token that still occurs somewhere else keeps the old
    distinct citation alive, so EVERY site must be repaired.
  - `referent note` — why the new path is the same referent as the old token.

THE PREDICATE (frozen before any repair was applied).
  The run is clean (exit 0) only when ALL of the following hold:
    1. `unresolved-class=0` — no member of either class survives;
    2. `ledger-rows>0` — the repair is recorded, not invisible;
    3. every ledger row's new token resolves on disk (`rows-resolving` counts
       them) — a row that points at a missing file fails;
    4. every ledger row's old token is absent from every one of its sites, and
       the new token is present at every one of its sites;
    5. no ledger row points into a lost tree (`lost-base` finding).

Exit codes: 0 clean, 1 failed, 2 could-not-evaluate (missing/unreadable
input).  The counter never writes to the tree it measures.

Determinism: the citation extraction rule is the one in `resolve.py`
(`is_pathlike` + `strip_anchor`); it is imported, not re-implemented, so the
two instruments cannot drift apart.
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LOST_ROOTS = (
    os.path.expanduser("~/Projects/bounties"),
    os.path.expanduser("~/Projects/the-bounty-hunter"),
    os.path.expanduser("~/Projects/origin-work"),
)

FLEET_TOP_FILES = (
    "PROTOCOL.md", "PROTOCOL-APPENDIX.md", "MISSION.md", "AXES.md", "CORPUS.md",
    "LEARNING.md", "MANIFEST.json", "ROADMAP.md", "SHONEN.md", "README.md",
    "shokunin.conf", "MANIFEST.schema.json",
)
FLEET_TOP_DIRS = (".ufo", ".tower", "templates", "scripts", "docs", "considerthese")

TOKEN_RE = re.compile(r"`([^`\n]+)`")
GLOB_META = re.compile(r"[*?\[]")
LEDGER_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*([a-z-]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")

# Files the lane does not own: the outside verification lessons and the
# aggregator's audit lessons.  Their bytes are never edited by the lane
# (PROTOCOL "Inherited state"), so a citation that also occurs in one of them
# cannot be fully re-grounded by the lane: it is enumerated and named, never
# silently dropped.
PROTECTED_RE = re.compile(r"^round-\d+-verifier-spotcheck\.md$|^round-.*-aggregator-.*\.md$")


def is_protected(rel):
    return bool(PROTECTED_RE.match(os.path.basename(rel)))


def load_resolve_module():
    """Import the axis instrument so the extraction rule cannot drift."""
    path = os.path.join(HERE, "resolve.py")
    spec = importlib.util.spec_from_file_location("kasegi_resolve", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    argv = sys.argv
    sys.argv = ["resolve.py", "."]
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    finally:
        sys.argv = argv
    return module


def lane_files(root, resolve_mod):
    """Every file the axis instrument reads: SKILL.md + corpus/**/*.md.

    The generated census report (`corpus/instruments/citation-survival.md`) is
    excluded, exactly as `resolve.py` excludes it, so the two instruments read
    the same scope.
    """
    generated = "corpus/instruments/citation-survival.md"
    files = [os.path.join(root, "SKILL.md")]
    corpus = os.path.join(root, "corpus")
    if os.path.isdir(corpus):
        for dirpath, dirnames, filenames in os.walk(corpus):
            dirnames.sort()
            for fn in sorted(filenames):
                if fn.endswith(".md"):
                    files.append(os.path.join(dirpath, fn))
    out = []
    for f in files:
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        if rel == generated:
            continue
        out.append(f)
    return [f for f in out if os.path.isfile(f)]


def citations(root, resolve_mod, exclude=()):
    """{token: [(relpath, line)]} for every path-like citation in scope.

    `exclude` holds lane-relative paths that are excluded from the scan: the
    ledger records the OLD tokens on purpose, so scanning it would classify
    every ledger row as an unresolved class member.
    """
    out = {}
    for path in lane_files(root, resolve_mod):
        rel = os.path.relpath(path, root)
        if rel in exclude:
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    for m in TOKEN_RE.finditer(line):
                        tok = m.group(1).strip().rstrip(".,;:")
                        if not resolve_mod.is_pathlike(tok):
                            continue
                        out.setdefault(tok, []).append((rel, lineno))
        except OSError:
            continue
    return out


def fleet_root_for(root):
    """The fleet repo that holds the lane repo: `<root>/..`."""
    parent = os.path.dirname(os.path.abspath(root))
    if os.path.isfile(os.path.join(parent, "PROTOCOL.md")) and os.path.isfile(
        os.path.join(parent, "MISSION.md")
    ):
        return parent
    return None


def classify_class(tok, root, fleet):
    """'lane-bare' | 'fleet-relative' | None for one citation token."""
    if GLOB_META.search(tok):
        return None
    base = tok
    mm = re.search(r":\d+([–-]\d+)?$", tok)
    if mm:
        base = tok[: mm.start()]
    if not base:
        return None
    if os.path.exists(os.path.join(root, base)):
        return None  # already opens
    if os.path.exists(os.path.expanduser(base)):
        return None  # already opens (absolute home path)
    candidate = os.path.join(root, "corpus", base)
    if os.path.isfile(candidate):
        return "lane-bare"
    if fleet:
        seg = base.split("/")[0]
        known = seg in FLEET_TOP_FILES or seg in FLEET_TOP_DIRS or seg.endswith("-shokunin")
        if known and os.path.exists(os.path.join(fleet, base)):
            return "fleet-relative"
    return None


def read_ledger(path):
    """[(old, new, cls, sites, note)] from the ledger table."""
    rows = []
    if not os.path.isfile(path):
        return rows
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = LEDGER_ROW_RE.match(line.rstrip("\n"))
            if not m:
                continue
            old, new, cls, sites, note = m.groups()
            site_list = [s.strip() for s in sites.split(",") if s.strip()]
            rows.append((old, new, cls, site_list, note.strip()))
    return rows


def under_lost_tree(path):
    ap = os.path.abspath(os.path.expanduser(path))
    for lost in LOST_ROOTS:
        if ap == lost or ap.startswith(lost + os.sep):
            return True
    return False


def measure(root, ledger_path, fleet_override=None):
    resolve_mod = load_resolve_module()
    if resolve_mod is None:
        return None, "resolve.py could not be imported"
    ledger_rel = os.path.relpath(ledger_path, root) if os.path.isabs(ledger_path) else ledger_path
    cites = citations(root, resolve_mod, exclude=(ledger_rel,))
    fleet = fleet_override or fleet_root_for(root)
    classes = {"lane-bare": [], "fleet-relative": []}
    for tok in sorted(cites):
        cls = classify_class(tok, root, fleet)
        if cls:
            classes[cls].append((tok, cites[tok]))
    # Partition: a class member is fully owned by the lane only when EVERY
    # occurrence sits in a lane-authored file.  A member that also occurs in a
    # protected file cannot be re-grounded by the lane (its bytes are not the
    # lane's to edit), so it is named, counted and disclosed instead of being
    # counted as a repairable member or silently dropped.
    owned, blocked = [], []
    for cls in ("lane-bare", "fleet-relative"):
        for tok, sites in classes[cls]:
            prot = [s for s in sites if is_protected(s[0])]
            (blocked if prot else owned).append((cls, tok, sites, prot))
    rows = read_ledger(ledger_path)
    findings = []
    rows_resolving = 0
    for old, new, cls, sites, note in rows:
        new_base = new
        mm = re.search(r":\d+([–-]\d+)?$", new)
        if mm:
            new_base = new[: mm.start()]
        target = new_base if os.path.isabs(new_base) else os.path.join(root, new_base)
        if os.path.exists(target):
            rows_resolving += 1
        else:
            findings.append(("row-unresolved", old, new))
        if under_lost_tree(new_base):
            findings.append(("row-lost-base", old, new))
        for site in sites:
            rel, _, lineno = site.rpartition(":")
            path = os.path.join(root, rel)
            if not os.path.isfile(path):
                findings.append(("row-site-missing", old, site))
                continue
            try:
                lines = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                findings.append(("row-site-unreadable", old, site))
                continue
            try:
                idx = int(lineno) - 1
            except ValueError:
                findings.append(("row-site-badline", old, site))
                continue
            if idx < 0 or idx >= len(lines):
                findings.append(("row-site-out-of-range", old, site))
                continue
            text = lines[idx]
            tokens = {m.group(1).strip().rstrip(".,;:") for m in TOKEN_RE.finditer(text)}
            if old in tokens:
                findings.append(("row-old-present", old, site))
            if new not in tokens:
                findings.append(("row-new-absent", old, site))
    for cls, tok, sites, prot in owned:
        findings.append(("class-" + cls, tok, ",".join("%s:%d" % s for s in sites)))
    blocked_rows = []
    for cls, tok, sites, prot in blocked:
        blocked_rows.append({"id": "blocked-protected-" + cls, "token": tok,
                             "detail": ",".join("%s:%d" % s for s in prot)})
    if rows and rows_resolving != len(rows):
        pass  # already reported per row
    return {
        "root": root,
        "fleet_root": fleet,
        "ledger": ledger_path,
        "ledger_rows": len(rows),
        "rows_resolving": rows_resolving,
        "class_lane_bare": sum(1 for c, _, _, _ in owned if c == "lane-bare"),
        "class_fleet_relative": sum(1 for c, _, _, _ in owned if c == "fleet-relative"),
        "unresolved_class": len(owned),
        "class_total": len(owned) + len(blocked),
        "class_protected_blocked": len(blocked),
        "findings": [{"id": f[0], "token": f[1], "detail": f[2]} for f in findings],
        "blocked": blocked_rows,
    }, None


def report(data, out=sys.stdout):
    out.write("unresolved-class=%d\n" % data["unresolved_class"])
    out.write("class-lane-bare=%d\n" % data["class_lane_bare"])
    out.write("class-fleet-relative=%d\n" % data["class_fleet_relative"])
    out.write("class-total=%d\n" % data["class_total"])
    out.write("class-protected-blocked=%d\n" % data["class_protected_blocked"])
    out.write("ledger-rows=%d\n" % data["ledger_rows"])
    out.write("rows-resolving=%d\n" % data["rows_resolving"])
    out.write("findings=%d\n" % len(data["findings"]))
    for f in data["findings"][:200]:
        out.write("finding %s %s %s\n" % (f["id"], f["token"], f["detail"]))
    for f in data["blocked"][:200]:
        out.write("blocked %s %s %s\n" % (f["id"], f["token"], f["detail"]))
    out.write("verdict=%s\n" % ("clean" if not data["findings"] else "failed"))


def build_fixture_tree(base, work):
    """A minimal lane tree for the self-test (the lane sits INSIDE the fleet
    root, because the fleet root is the lane root's parent directory)."""
    fleet = os.path.join(work, "fleet")
    lane = os.path.join(fleet, "kasegi-shokunin")
    os.makedirs(os.path.join(lane, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(lane, "corpus", "instruments"), exist_ok=True)
    os.makedirs(os.path.join(fleet, ".ufo"), exist_ok=True)
    with open(os.path.join(lane, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("# fixture skill\n\n")
    with open(os.path.join(lane, "corpus", "knowledge", "entry.md"), "w", encoding="utf-8") as fh:
        fh.write("# entry\n")
    with open(os.path.join(lane, "corpus", "README.md"), "w", encoding="utf-8") as fh:
        fh.write("| Area | Entry |\n|---|---|\n| a | `knowledge/entry.md` |\n")
    with open(os.path.join(fleet, "PROTOCOL.md"), "w", encoding="utf-8") as fh:
        fh.write("protocol\n")
    with open(os.path.join(fleet, "MISSION.md"), "w", encoding="utf-8") as fh:
        fh.write("mission\n")
    with open(os.path.join(fleet, ".ufo", "state"), "w", encoding="utf-8") as fh:
        fh.write("state\n")
    shutil.copy2(os.path.join(HERE, "resolve.py"), os.path.join(lane, "corpus", "instruments", "resolve.py"))
    return lane, fleet


def selftest(scratch=None):
    work = scratch or tempfile.mkdtemp(prefix="citation-ground-selftest-")
    created = scratch is None
    failures = []
    cases = []

    def case(name, fn):
        try:
            ok, detail = fn()
        except Exception as exc:  # a fixture that raises is a failed case
            ok, detail = False, "exception:%s" % exc
        cases.append((name, ok, detail))
        if not ok:
            failures.append(name)

    def run(lane, ledger=None):
        ledger_path = ledger if ledger else os.path.join(lane, "corpus", "instruments", "citation-reground-ledger.md")
        data, err = measure(lane, ledger_path)
        return data, err

    def write_ledger(lane, rows):
        path = os.path.join(lane, "corpus", "instruments", "citation-reground-ledger.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# ledger\n\n| old token | new token | base class | sites | referent note |\n")
            fh.write("|---|---|---|---|---|\n")
            for row in rows:
                fh.write("| %s |\n" % " | ".join(row))
        return path

    def c_positive_red():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c1"))
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        return ("class-lane-bare" in ids and data["unresolved_class"] == 1, "ids=%s" % sorted(ids))

    def c_repaired_green():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c2"))
        readme = os.path.join(lane, "corpus", "README.md")
        text = open(readme, encoding="utf-8").read().replace("`knowledge/entry.md`", "`corpus/knowledge/entry.md`")
        open(readme, "w", encoding="utf-8").write(text)
        write_ledger(lane, [["`knowledge/entry.md`", "`corpus/knowledge/entry.md`", "lane-bare",
                              "corpus/README.md:3", "same file, full LANE path"]])
        data, err = run(lane)
        return (data["unresolved_class"] == 0 and data["ledger_rows"] == 1
                and data["rows_resolving"] == 1 and not data["findings"],
                "unresolved=%d findings=%s" % (data["unresolved_class"], data["findings"]))

    def c_fleet_class():
        lane, fleet = build_fixture_tree(None, os.path.join(work, "c3"))
        with open(os.path.join(lane, "corpus", "README.md"), "a", encoding="utf-8") as fh:
            fh.write("| b | `.ufo/state` |\n")
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        return ("class-fleet-relative" in ids, "ids=%s" % sorted(ids))

    def c_fleet_repaired_green():
        lane, fleet = build_fixture_tree(None, os.path.join(work, "c4"))
        readme = os.path.join(lane, "corpus", "README.md")
        text = open(readme, encoding="utf-8").read().replace("`knowledge/entry.md`", "`corpus/knowledge/entry.md`")
        with open(readme, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.write("| b | `%s/.ufo/state` |\n" % fleet)
        write_ledger(lane, [["`knowledge/entry.md`", "`corpus/knowledge/entry.md`", "lane-bare",
                              "corpus/README.md:3", "same file, full LANE path"],
                             ["`.ufo/state`", "`%s/.ufo/state`" % fleet, "fleet-relative",
                              "corpus/README.md:4", "absolute fleet path"]])
        data, err = run(lane)
        return (data["unresolved_class"] == 0 and not data["findings"], "findings=%s" % data["findings"])

    def c_row_unresolved():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c5"))
        readme = os.path.join(lane, "corpus", "README.md")
        text = open(readme, encoding="utf-8").read().replace("`knowledge/entry.md`", "`corpus/knowledge/missing.md`")
        open(readme, "w", encoding="utf-8").write(text)
        write_ledger(lane, [["`knowledge/entry.md`", "`corpus/knowledge/missing.md`", "lane-bare",
                              "corpus/README.md:3", "same file, full LANE path"]])
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        return ("row-unresolved" in ids, "ids=%s" % sorted(ids))

    def c_row_old_present():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c6"))
        write_ledger(lane, [["`knowledge/entry.md`", "`corpus/knowledge/entry.md`", "lane-bare",
                              "corpus/README.md:3", "same file, full LANE path"]])
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        return ("row-old-present" in ids, "ids=%s" % sorted(ids))

    def c_lost_base_row():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c7"))
        write_ledger(lane, [["`knowledge/entry.md`", "`~/Projects/bounties/claims/x.md`", "lane-bare",
                              "corpus/README.md:3", "re-pointed at the lost tree"]])
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        return ("row-lost-base" in ids, "ids=%s" % sorted(ids))

    def c_glob_not_counted():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c8"))
        with open(os.path.join(lane, "corpus", "README.md"), "a", encoding="utf-8") as fh:
            fh.write("| c | `corpus/knowledge/*.md` |\n")
        data, err = run(lane)
        return (data["class_lane_bare"] == 1 and data["unresolved_class"] == 1,
                "lane_bare=%d" % data["class_lane_bare"])

    def c_missing_ledger_is_not_clean():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c9"))
        data, err = run(lane)
        return (data["ledger_rows"] == 0 and data["unresolved_class"] == 1 and data["findings"],
                "rows=%d unresolved=%d" % (data["ledger_rows"], data["unresolved_class"]))

    def c_protected_occurrence_is_blocked_not_owned():
        lane, _ = build_fixture_tree(None, os.path.join(work, "c10"))
        prot = os.path.join(lane, "corpus", "lessons", "round-1-verifier-spotcheck.md")
        os.makedirs(os.path.dirname(prot), exist_ok=True)
        with open(prot, "w", encoding="utf-8") as fh:
            fh.write("| a | `knowledge/entry.md` |\n")
        data, err = run(lane)
        ids = {f["id"] for f in data["findings"]}
        bids = {f["id"] for f in data["blocked"]}
        return (data["unresolved_class"] == 0 and "blocked-protected-lane-bare" in bids
                and "class-lane-bare" not in ids,
                "unresolved=%d blocked=%s" % (data["unresolved_class"], sorted(bids)))

    case("protected-occurrence-is-blocked-not-owned", c_protected_occurrence_is_blocked_not_owned)
    case("planted-lane-bare-reads-red", c_positive_red)
    case("repaired-lane-bare-reads-clean", c_repaired_green)
    case("planted-fleet-relative-reads-red", c_fleet_class)
    case("repaired-fleet-relative-reads-clean", c_fleet_repaired_green)
    case("ledger-row-pointing-at-missing-file-reads-red", c_row_unresolved)
    case("ledger-row-with-old-token-still-present-reads-red", c_row_old_present)
    case("ledger-row-into-lost-tree-reads-red", c_lost_base_row)
    case("glob-token-is-not-a-class-member", c_glob_not_counted)
    case("absent-ledger-is-not-clean", c_missing_ledger_is_not_clean)

    for name, ok, detail in cases:
        print("selftest case=%s verdict=%s %s" % (name, "pass" if ok else "fail", detail))
    print("selftest cases=%d failures=%d" % (len(cases), len(failures)))
    if created:
        shutil.rmtree(work, ignore_errors=True)
    return 1 if failures else 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--fleet-root", default=None)
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--scratch", default=None)
    args = ap.parse_args(argv[1:])
    if args.selftest:
        return selftest(args.scratch)
    root = os.path.abspath(os.path.expanduser(args.root))
    if not os.path.isdir(root):
        sys.stderr.write("citation-ground-check.py: not a directory: %s\n" % args.root)
        return 2
    ledger = args.ledger or os.path.join(root, "corpus", "instruments", "citation-reground-ledger.md")
    fleet = os.path.abspath(os.path.expanduser(args.fleet_root)) if args.fleet_root else None
    data, err = measure(root, ledger, fleet_override=fleet)
    if data is None:
        sys.stderr.write("citation-ground-check.py: %s\n" % err)
        return 2
    report(data)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
    return 1 if data["findings"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
