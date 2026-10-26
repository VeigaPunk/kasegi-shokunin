#!/usr/bin/env python3
"""score-gap.py — distance to the next depth:verifiability score (r31).

Implements considerthese/2026-10-25.md proposal 2 ("track distance to the next
score, not just improved, held"): a read-only reporter that prints, for
depth:verifiability, the four committed-byte measurements that decide whether a
score of 5 is reachable — each with the command it came from — and then one
COMPUTED `gap` line.

THIS IS NOT A CLAIM AND IT ASSERTS NO SCORE MOVE. It is a measurement of the
lane's own bytes; no field here is evidence for or against a score change, and a
green run does not mean a score is due. The reporter never writes: it opens
inputs read-only, runs the two audited instruments as subprocesses without their
--json/--receipt options, and does no scratch work outside --selftest (which
uses tempfile.mkdtemp and removes it).

Fields (root = the lane; every value is parsed from the instrument/file named):

 1. rechecks   `python3 corpus/instruments/recheck-audit.py --root <root> --quiet`
               -> lines/executes/gated/broken and its exit. `gated` is the
               instrument's own definition: the recheck line runs and fails
               closed on an absent base.
 2. anchors    `python3 corpus/instruments/anchorcheck.py SKILL.md` (cwd=root)
               -> the frozen summary buckets in-range/bad/LOST-RECORDED/ORIGIN/
               OUTSIDE-BASE/BASE-ABSENT and its fail-closed exit.
 3. census     corpus/instruments/citation-survival.md -> the committed lane and
               SKILL.md resolvability rates plus the file's own definition
               sentence (quoted, never retyped).
 4. threshold  SCORECARD.md -> the line naming the score-5 bar ("a non-author
               audit ... 0 unsupported current claims"): its line number and the
               quoted sentence.
 5. gap        `gap: <k> of <n> rechecks still gated on a lost base; score 5
               needs 0 gated unsupported claims`, k = field 1 `gated`,
               n = field 1 `lines`; computed, never typed.

Exit status: 0 on a complete read (even when the lane's own gates are red — the
reporter reports, it does not judge); 2 when an input file is missing/unreadable
or no longer yields its field.

Usage:
  python3 corpus/instruments/score-gap.py [--root <lane>]   # runs from any cwd
  python3 corpus/instruments/score-gap.py --selftest
"""

import argparse
import contextlib
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

RECHECK_REL = "corpus/instruments/recheck-audit.py"
ANCHOR_REL = "corpus/instruments/anchorcheck.py"
CENSUS_REL = "corpus/instruments/citation-survival.md"
SCORECARD_REL = "SCORECARD.md"
SKILL_REL = "SKILL.md"

RECHECK_FIELDS_RE = re.compile(r"executes=(\d+) gated=(\d+) broken=(\d+)")
RECHECK_LINES_RE = re.compile(r"^lines=(\d+) total=(\d+) ", re.M)
ANCHOR_SUMMARY_RE = re.compile(
    r"^== (?P<src>.+?): (?P<in_range>\d+) in-range cite instances, (?P<bad>\d+) bad; "
    r"(?P<anchors>\d+) distinct anchors; LOST-RECORDED=(?P<lost>\d+) PIN-BROKEN=(?P<pin>\d+) "
    r"ORIGIN=(?P<origin>\d+) OUTSIDE-BASE=(?P<outside>\d+) BASE-ABSENT=(?P<base_absent>\d+)$",
    re.M,
)
CENSUS_DEF_RE = re.compile(r"^Numerator = RESOLVES \+ MIRROR-EQUIVALENT \+ INTERNAL\..*$", re.M)
CENSUS_LANE_RE = re.compile(
    r"^- lane total \(SKILL\.md \+ corpus\): \*\*(\d+)/(\d+) = ([\d.]+)%\*\*$", re.M
)
CENSUS_SKILL_RE = re.compile(r"^- SKILL\.md alone: \*\*(\d+)/(\d+) = ([\d.]+)%\*\*$", re.M)
THRESHOLD_RE = re.compile(r"Threshold for 5: [^|]*?claims\.")

TIMEOUT = 600


class InputError(Exception):
    """An input file is missing/unreadable or no longer yields its field."""

    def __init__(self, message, path=None):
        Exception.__init__(self, message)
        self.path = path


def lane_root():
    """The lane this instrument lives in: <lane>/corpus/instruments/score-gap.py."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def read_text(path, rel):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        raise InputError("cannot read %s: %s" % (rel, exc.strerror or exc), path)


def run(cmd, cwd, env=None):
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InputError("cannot run %s: %s" % (os.path.basename(cmd[2] if len(cmd) > 2 else cmd[0]), exc))
    return proc.returncode, proc.stdout, proc.stderr


def field_recheck(root, env=None):
    rel = RECHECK_REL
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise InputError("missing input: %s" % rel, path)
    cmd = [sys.executable, "-B", path, "--root", root, "--quiet"]
    rc, out, err = run(cmd, root, env)
    text = out + err
    fields = RECHECK_FIELDS_RE.search(text)
    lines = RECHECK_LINES_RE.search(text)
    if not fields or not lines:
        raise InputError(
            "%s --quiet printed no executes/gated/broken summary (exit %d)" % (rel, rc), path
        )
    return {
        "lines": int(lines.group(1)),
        "total": int(lines.group(2)),
        "executes": int(fields.group(1)),
        "gated": int(fields.group(2)),
        "broken": int(fields.group(3)),
        "exit": rc,
        "cmd": "python3 %s --root %s --quiet" % (rel, root),
    }


def field_anchorcheck(root, env=None):
    rel = ANCHOR_REL
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise InputError("missing input: %s" % rel, path)
    if not os.path.isfile(os.path.join(root, SKILL_REL)):
        raise InputError("missing input: %s" % SKILL_REL, os.path.join(root, SKILL_REL))
    cmd = [sys.executable, "-B", path, SKILL_REL]
    rc, out, err = run(cmd, root, env)
    match = ANCHOR_SUMMARY_RE.search(out + err)
    if not match:
        raise InputError("%s printed no summary line for %s (exit %d)" % (rel, SKILL_REL, rc), path)
    return {
        "in_range": int(match.group("in_range")),
        "bad": int(match.group("bad")),
        "anchors": int(match.group("anchors")),
        "lost": int(match.group("lost")),
        "pin_broken": int(match.group("pin")),
        "origin": int(match.group("origin")),
        "outside": int(match.group("outside")),
        "base_absent": int(match.group("base_absent")),
        "exit": rc,
        "cmd": "python3 %s %s (cwd=%s)" % (rel, SKILL_REL, root),
    }


def field_census(root):
    path = os.path.join(root, CENSUS_REL)
    if not os.path.isfile(path):
        raise InputError("missing input: %s" % CENSUS_REL, path)
    text = read_text(path, CENSUS_REL)
    definition = CENSUS_DEF_RE.search(text)
    lane = CENSUS_LANE_RE.search(text)
    skill = CENSUS_SKILL_RE.search(text)
    if not definition:
        raise InputError("%s no longer states its resolvability definition" % CENSUS_REL, path)
    if not lane or not skill:
        raise InputError("%s no longer states both the lane and SKILL.md rates" % CENSUS_REL, path)
    return {
        "definition": definition.group(0).strip(),
        "lane": "%s/%s = %s%%" % (lane.group(1), lane.group(2), lane.group(3)),
        "skill": "%s/%s = %s%%" % (skill.group(1), skill.group(2), skill.group(3)),
        "cmd": "grep -nE '^Numerator = |^- (lane total|SKILL\\.md alone): ' %s" % CENSUS_REL,
    }


def field_threshold(root):
    path = os.path.join(root, SCORECARD_REL)
    if not os.path.isfile(path):
        raise InputError("missing input: %s" % SCORECARD_REL, path)
    text = read_text(path, SCORECARD_REL)
    found = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if "Threshold for 5" not in line or "unsupported current claims" not in line:
            continue
        quote = THRESHOLD_RE.search(line)
        if quote:
            found.append((lineno, quote.group(0).strip()))
    if not found:
        raise InputError(
            "%s no longer names the score-5 threshold (non-author audit, 0 unsupported current claims)"
            % SCORECARD_REL,
            path,
        )
    lineno, quote = found[0]
    return {
        "lineno": lineno,
        "quote": quote,
        "matches": len(found),
        "cmd": "grep -nE 'Threshold for 5:.*unsupported current claims' %s" % SCORECARD_REL,
    }


def gap_line(recheck):
    return (
        "gap: %d of %d rechecks still gated on a lost base; "
        "score 5 needs 0 gated unsupported claims" % (recheck["gated"], recheck["lines"])
    )


def report(root, env=None):
    """Return the report as a list of lines. Never writes. Raises InputError."""
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        raise InputError("root is not a directory", root)
    out = [
        "score-gap — depth:verifiability distance to score 5 "
        "(read-only; NOT a claim; asserts no score move)",
        "root: %s" % root,
    ]
    for rel in (RECHECK_REL, SKILL_REL, CENSUS_REL, SCORECARD_REL):
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            raise InputError("missing input: %s" % rel, path)
        out.append("source: %s sha256=%s" % (rel, sha256_file(path)))

    recheck = field_recheck(root, env)
    out.append("[1] rechecks")
    out.append("cmd: %s" % recheck["cmd"])
    out.append(
        "recheck: lines=%d executes=%d gated=%d broken=%d exit=%d"
        % (recheck["lines"], recheck["executes"], recheck["gated"], recheck["broken"], recheck["exit"])
    )

    anchor = field_anchorcheck(root, env)
    out.append("[2] anchors")
    out.append("cmd: %s" % anchor["cmd"])
    out.append(
        "anchorcheck: in-range=%d bad=%d lost-recorded=%d origin=%d outside-base=%d "
        "base-absent=%d exit=%d"
        % (
            anchor["in_range"],
            anchor["bad"],
            anchor["lost"],
            anchor["origin"],
            anchor["outside"],
            anchor["base_absent"],
            anchor["exit"],
        )
    )

    census = field_census(root)
    out.append("[3] citation-survival census (committed figures)")
    out.append("cmd: %s" % census["cmd"])
    out.append("census-definition: %s" % census["definition"])
    out.append("census-lane: %s" % census["lane"])
    out.append("census-skill: %s" % census["skill"])

    threshold = field_threshold(root)
    out.append("[4] score-5 threshold")
    out.append("cmd: %s" % threshold["cmd"])
    out.append(
        'threshold: %s:%d "%s"'
        % (SCORECARD_REL, threshold["lineno"], threshold["quote"])
    )
    if threshold["matches"] > 1:
        out.append("threshold-matches: %d (first line used)" % threshold["matches"])

    out.append("[5] gap")
    out.append(gap_line(recheck))
    return out


# ---------------------------------------------------------------- selftest ---

STUB_RECHECK = '''#!/usr/bin/env python3
"""score-gap.py --selftest stand-in for recheck-audit.py --quiet.

Used only when the real instrument cannot be copied-and-run inside the fixture
lane (it is under concurrent edit during the round). Emits the frozen summary
shape the reporter parses, with the numbers the fixture declares.
"""
import json
import os
import sys

data = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "recheck.json"),
                      encoding="utf-8"))
print("executes=%(executes)d gated=%(gated)d broken=%(broken)d  (selftest stub)" % data)
print("lines=%(lines)d total=%(total)d pass=%(pass)d fail-closed=%(fail_closed)d "
      "parse_fail=0 cwd_fail=0 paths_fail=0 exit=%(exit)d" % data)
sys.exit(data["exit"])
'''


def _write(path, text):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def _tree_digest(root):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = os.path.join(dirpath, name)
            rows.append("%s %s" % (os.path.relpath(path, root), sha256_file(path)))
    return "\n".join(rows)


VARIANTS = {
    "a": {
        "knowledge": [
            ("good.md", "recheck: cd {root} && python3 corpus/instruments/tool.py corpus/knowledge/good.md"),
            ("gated.md", "recheck: cd {root} && test -d ~/Projects/absent-base-score-gap"),
        ],
        "recheck": {"lines": 2, "total": 2, "executes": 1, "gated": 1, "broken": 0,
                    "pass": 1, "fail_closed": 1, "exit": 0},
        "skill": (
            "- in range `corpus/knowledge/good.md:3`\n"
            "- lost `[lost-tree] claims/x/status.json:2`\n"
            "- past eof `corpus/knowledge/good.md:99`\n"
            "- outside `~/Projects/bounties/../outside.md:1`\n"
            "- absent `corpus/knowledge/nope.md:4`\n"
        ),
        "census": (
            "## Resolvability rate\n\n"
            "Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct "
            "citations appearing in that scope (fixture A wording).\n\n"
            "- SKILL.md alone: **10/20 = 50.00%**\n"
            "- lane total (SKILL.md + corpus): **100/200 = 50.00%**\n"
        ),
        "scorecard": (
            "# scorecard fixture A\n"
            "\n"
            "| Axis | Before | After |\n"
            "|---|---:|---:|\n"
            "| depth:verifiability | 4 | 4 | Threshold for 5: a non-author audit passing "
            "25/25 source chains and 0 unsupported current claims. |\n"
        ),
    },
    "b": {
        "knowledge": [
            ("good.md", "recheck: cd {root} && python3 corpus/instruments/tool.py corpus/knowledge/good.md"),
            ("good2.md", "recheck: cd {root} && python3 corpus/instruments/tool.py corpus/knowledge/good2.md"),
            ("broken.md", "recheck: cd {root} && test -d ~/Projects/x (fails closed today)"),
        ],
        "recheck": {"lines": 3, "total": 3, "executes": 2, "gated": 0, "broken": 1,
                    "pass": 2, "fail_closed": 1, "exit": 1},
        "skill": (
            "- in range `corpus/knowledge/good.md:3`\n"
            "- origin `~/Projects/origin-work/open-bug-bounties/x.md:2`\n"
            "- lost `[lost-tree] claims/x/status.json:2`\n"
            "- lost `[lost-base] ops/shared.mjs:7`\n"
            "- lost `[lost-tree] docs/wrap-report.md:19`\n"
        ),
        "census": (
            "## Resolvability rate\n\n"
            "Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL. Denominator = all distinct "
            "citations appearing in that scope (fixture B wording, deliberately different).\n\n"
            "- SKILL.md alone: **3/8 = 37.50%**\n"
            "- lane total (SKILL.md + corpus): **3/4 = 75.00%**\n"
        ),
        "scorecard": (
            "# scorecard fixture B\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "\n"
            "| depth:verifiability | 4 | 4 | Threshold for 5: all source chains passing a "
            "non-author audit with 0 unsupported current claims. |\n"
        ),
    },
}


def _make_fixture(parent, variant, real_instruments, recheck_mode):
    root = os.path.join(parent, variant)
    spec = VARIANTS[variant]
    _write(os.path.join(root, "corpus/instruments/tool.py"), "")
    for name, line in spec["knowledge"]:
        _write(os.path.join(root, "corpus/knowledge", name), "# fixture\n\n%s\n" % line.format(root=root))
    _write(os.path.join(root, SKILL_REL), "# fixture SKILL\n\n" + spec["skill"])
    _write(os.path.join(root, CENSUS_REL), spec["census"])
    _write(os.path.join(root, SCORECARD_REL), spec["scorecard"])
    if recheck_mode == "real":
        shutil.copy(os.path.join(real_instruments, "recheck-audit.py"),
                    os.path.join(root, RECHECK_REL))
    else:
        _write(os.path.join(root, RECHECK_REL), STUB_RECHECK)
        _write(os.path.join(root, "corpus/instruments/recheck.json"),
               "".join('%s: %d,\n' % (k, v) for k, v in spec["recheck"].items()))
    shutil.copy(os.path.join(real_instruments, "anchorcheck.py"),
                os.path.join(root, ANCHOR_REL))
    # bases: bounties present in both (an escape is reachable), mirror/origin per variant
    os.makedirs(os.path.join(root, "bounties"), exist_ok=True)
    if variant == "a":
        mirror, origin = os.path.join(root, "mirror-absent"), os.path.join(root, "origin-absent")
    else:
        mirror, origin = os.path.join(root, "mirror"), os.path.join(root, "origin")
        os.makedirs(mirror, exist_ok=True)
        _write(os.path.join(origin, "x.md"), "line1\nline2\n")
    env = dict(
        os.environ,
        KASEGI_LANE_ROOT=root,
        KASEGI_MIRROR=mirror,
        KASEGI_ORIGIN_ROOT=origin,
        KASEGI_BOUNTIES=os.path.join(root, "bounties"),
    )
    return root, env


def _capture(argv, env):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = main(argv, env=env)
    return rc, out.getvalue(), err.getvalue()


def _values(lines):
    """Flatten a report into comparable fields (label -> value)."""
    fields = {}
    for line in lines:
        for prefix in ("recheck: ", "anchorcheck: ", "census-definition: ", "census-lane: ",
                       "census-skill: ", "threshold: ", "gap: "):
            if line.startswith(prefix):
                fields[prefix.rstrip(": ")] = line[len(prefix):]
    return fields


def _split_counts(value):
    return dict(part.split("=", 1) for part in value.split() if "=" in part)


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    failures = []

    def check(label, ok, detail):
        print("selftest %-28s %s %s" % (label, "ok" if ok else "FAIL", detail))
        if not ok:
            failures.append(label)

    with tempfile.TemporaryDirectory(prefix="score-gap-selftest-") as tmp:
        # pre-flight: can the real recheck-audit.py run inside a fixture lane?
        probe, probe_env = _make_fixture(tmp, "a", here, "real")
        mode, why = "real", ""
        try:
            field_recheck(probe, probe_env)
        except InputError as exc:
            mode, why = "stub", str(exc)
        print("selftest recheck-mode=%s%s" % (mode, (" reason=%s" % why) if why else ""))
        shutil.rmtree(probe)

        roots, envs, reports = {}, {}, {}
        for variant in ("a", "b"):
            roots[variant], envs[variant] = _make_fixture(tmp, variant, here, mode)
            before = _tree_digest(roots[variant])
            rc, out, err = _capture(["--root", roots[variant]], envs[variant])
            check("exit-%s" % variant, rc == 0, "rc=%d want=0 err=%r" % (rc, err.strip()[:120]))
            check("no-write-%s" % variant, _tree_digest(roots[variant]) == before,
                  "tree digest unchanged=%s" % (_tree_digest(roots[variant]) == before))
            reports[variant] = out.splitlines()

        a, b = _values(reports["a"]), _values(reports["b"])

        # every reported field must move when the fixture moves
        ra, rb = _split_counts(a["recheck"]), _split_counts(b["recheck"])
        for key in ("lines", "executes", "gated", "broken"):
            check("recheck.%s" % key, ra[key] != rb[key], "a=%s b=%s" % (ra[key], rb[key]))
        aa, ab = _split_counts(a["anchorcheck"]), _split_counts(b["anchorcheck"])
        for key in ("in-range", "bad", "lost-recorded", "origin", "outside-base",
                    "base-absent", "exit"):
            check("anchorcheck.%s" % key, aa[key] != ab[key], "a=%s b=%s" % (aa[key], ab[key]))
        for key in ("census-lane", "census-skill", "census-definition"):
            check(key, a[key] != b[key], "a=%r b=%r" % (a[key][:60], b[key][:60]))
        check("threshold", a["threshold"] != b["threshold"],
              "a=%r b=%r" % (a["threshold"][:60], b["threshold"][:60]))
        check("gap", a["gap"] != b["gap"], "a=%r b=%r" % (a["gap"], b["gap"]))

        # the gap line must be computed from field 1, not typed
        want = "%s of %s rechecks still gated on a lost base; " \
               "score 5 needs 0 gated unsupported claims" % (ra["gated"], ra["lines"])
        check("gap-computed", a["gap"] == want, "got=%r want=%r" % (a["gap"], want))

        # unreadable inputs exit 2 (never 0, never a traceback)
        for label, rel in (("missing-census", CENSUS_REL), ("missing-recheck", RECHECK_REL),
                           ("missing-scorecard", SCORECARD_REL)):
            broken = os.path.join(tmp, "broken-%s" % label)
            shutil.copytree(roots["a"], broken)
            os.unlink(os.path.join(broken, rel))
            env = dict(envs["a"], KASEGI_LANE_ROOT=broken)
            rc, out, err = _capture(["--root", broken], env)
            check("exit2-%s" % label, rc == 2, "rc=%d want=2 msg=%r" % (rc, err.strip()[:80]))
        no_threshold = os.path.join(tmp, "broken-no-threshold")
        shutil.copytree(roots["a"], no_threshold)
        _write(os.path.join(no_threshold, SCORECARD_REL), "# no threshold line here\n")
        rc, out, err = _capture(["--root", no_threshold],
                                dict(envs["a"], KASEGI_LANE_ROOT=no_threshold))
        check("exit2-no-threshold", rc == 2, "rc=%d want=2 msg=%r" % (rc, err.strip()[:80]))

        print("selftest fields=%d failures=%d" % (len(a), len(failures)))
        return 1 if failures else 0


def main(argv=None, env=None):
    parser = argparse.ArgumentParser(
        description="Read-only distance-to-score-5 reporter for depth:verifiability "
        "(NOT a claim; asserts no score move)."
    )
    parser.add_argument("--root", help="lane root; default: the lane this instrument lives in")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    root = os.path.abspath(args.root) if args.root else lane_root()
    try:
        lines = report(root, env)
    except InputError as exc:
        sys.stderr.write(
            "score-gap: INPUT-UNREADABLE %s%s\n"
            % (exc, (" (%s)" % exc.path) if exc.path else "")
        )
        return 2
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
