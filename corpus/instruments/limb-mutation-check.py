#!/usr/bin/env python3
"""Prove named instrument limbs load-bearing with a one-limb mutation ledger.

Usage:
  python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
  python3 corpus/instruments/limb-mutation-check.py --ledger PATH --root LANE_ROOT
  python3 corpus/instruments/limb-mutation-check.py --selftest

Ledger schema (round-31 C1 interface, frozen by the L1):

  {"version": 1,
   "limbs":    [LIMB...],
   "controls": [CONTROL...]}

  LIMB    = {"id","instrument","find","replace","kill","live_exit","signal","note"}
  CONTROL = LIMB + {"expect": "invalid:noop" | "invalid:nocompile" | "survivor"}

`instrument` is lane-relative. `find` must occur exactly once in the instrument's
current bytes; `replace` is the mutant text. `kill` is a shell command run with
`bash -c` from the scratch lane root, with `{inst}` replaced by the scratch copy
of the instrument and `{root}` by the scratch lane root. `signal` is a Python
regular expression (re.MULTILINE) that must match the run's stdout+stderr.
`live_exit` is the unmutated run's required exit status (1 is legitimate for a
fail-closed harness). An optional top-level `"copy"` list names extra
lane-relative files or directories a kill command needs beyond `corpus/`.

Per row, in this order: copy the lane's `corpus/` into a fresh temp scratch lane;
run `kill` twice on the unmutated scratch copy (both runs must exit `live_exit`
and match `signal`, and must agree with each other, else
`invalid:live-baseline`); check `find` occurs exactly once
(`invalid:find-count`); apply the one substitution (`invalid:noop` when the
bytes do not change); `py_compile` the mutated file (`invalid:nocompile`); exec
the mutant's module level in a subprocess (`invalid:import` when it raises
there, so a patch that never lets the limb run cannot be called killed); then
run `kill` twice on the mutated bytes in a SECOND fresh scratch copy (a
disagreement between those two runs is `invalid:mutant-baseline`). `killed` when
the mutant's exit differs from `live_exit` or its output no longer matches
`signal`; otherwise `survivor`. A run exceeding 120 s is `invalid:timeout` —
never `killed`. Nothing is written outside the scratch lanes (deleted at exit),
and no git command is run.

Before any ledger row, every run evaluates three guard fixtures on a throwaway
probe lane: a baseline that loses its declared signal must be
`invalid:live-baseline`, a `find` occurring twice must be `invalid:find-count`,
and a kill that never returns must be `invalid:timeout`. The committed ledger
trips none of those three gates, so a counter that silently dropped one of them
would still print the same summary; the guards close that route. They are not
limbs or controls and never enter the two summary counts.

Ledger validation (exit 2): `version` 1; unique ids; lane-relative instrument
paths; non-empty `find`; integer `live_exit`; a `signal` that is a valid regex
and does not match the empty string (a vacuous signal cannot discriminate); a
`kill` that runs the instrument as a program (`python3 [flags] {inst}`), so a
command that only reads the patched bytes cannot call a comment patch killed;
and the frozen control ids `CTL-noop`, `CTL-nocompile`, `CTL-equivalent` bound
to `invalid:noop`, `invalid:nocompile`, `survivor`.

Output grammar, one line per row (byte-exact):

  guard <name> verdict=<v> want=<w> ok=y|n
  LIMB <id> live=<exit>/<sig:y|n> mutant=<exit>/<sig:y|n> verdict=<verdict>
  CONTROL <id> verdict=<v> expected=<e> ok=y|n
  guard cases=<n> failures=<f>
  limbs=<n> killed=<k> survivors=<s>
  controls=<n> rejected=<r>

`<exit>` is the integer status, `timeout`, or `-` when that run did not happen;
`<verdict>` is `killed`, `survivor`, or `invalid:<reason>` with reason one of
`live-baseline`, `mutant-baseline`, `find-count`, `noop`, `nocompile`,
`import`, `timeout`. `rejected` counts
controls whose verdict equals their `expect`. Exit 0 iff n==k, survivors==0,
every limb verdict is `killed`, rejected==controls, and every guard fixture
holds; 1 otherwise; 2 on a usage, ledger, or lane-root error.

`--selftest` runs eleven internal fixtures (killed, survivor, one per
`invalid:*` reason — `live-baseline`, `mutant-baseline`, `find-count`, `noop`,
`nocompile`, `import`, `timeout` — plus a module level raising `SystemExit(0)`,
a nondeterministic baseline and a state-counting kill command), six
ledger-validation fixtures (vacuous signal, kill that only reads the
instrument, chained kill, mis-bound control id, bound control id, valid row),
then asserts both exit-code aggregates and the control-line verdict rule. It
writes nothing into the lane and uses a 1 s per-command timeout so the timeout
path is provable without a 120 s wait; the CLI always uses the frozen 120 s.
"""
import argparse
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile

TIMEOUT_SECONDS = 120
GUARD_TIMEOUT = 1
SIGNAL_FLAGS = re.MULTILINE
ROW_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]*\Z")
CONTROL_EXPECTS = ("invalid:noop", "invalid:nocompile", "survivor")
CONTROL_ID_EXPECTS = {
    "CTL-noop": "invalid:noop",
    "CTL-nocompile": "invalid:nocompile",
    "CTL-equivalent": "survivor",
}
ROW_KEYS = ("id", "instrument", "find", "replace", "kill", "live_exit", "signal")


class LedgerError(Exception):
    """The ledger or lane root cannot be evaluated; the counter exits 2."""


def lane_root_from_script():
    """The lane root is three directories above corpus/instruments/<this file>."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def safe_relative(value, label):
    """Return a normalized lane-relative path, refusing absolute or escaping paths."""
    if not isinstance(value, str) or not value:
        raise LedgerError("%s must be a non-empty lane-relative path" % label)
    if os.path.isabs(value):
        raise LedgerError("%s must be lane-relative, got an absolute path: %s" % (label, value))
    normalized = os.path.normpath(value)
    if normalized == os.pardir or normalized.startswith(os.pardir + os.sep):
        raise LedgerError("%s escapes the lane root: %s" % (label, value))
    return normalized


def validate_row(row, label, control):
    if not isinstance(row, dict):
        raise LedgerError("%s must be a JSON object" % label)
    for key in ROW_KEYS:
        if key not in row:
            raise LedgerError("%s is missing %r" % (label, key))
    row_id = row["id"]
    if not isinstance(row_id, str) or ROW_ID_RE.fullmatch(row_id) is None:
        raise LedgerError("%s.id must match [A-Za-z0-9][A-Za-z0-9._:-]*" % label)
    instrument = safe_relative(row["instrument"], label + ".instrument")
    for key in ("find", "replace", "kill", "signal"):
        if not isinstance(row[key], str):
            raise LedgerError("%s.%s must be a string" % (label, key))
    if not row["find"]:
        raise LedgerError("%s.find must be non-empty" % label)
    if not row["kill"].strip():
        raise LedgerError("%s.kill must be a non-empty command" % label)
    if type(row["live_exit"]) is not int:
        raise LedgerError("%s.live_exit must be an integer" % label)
    try:
        re.compile(row["signal"], SIGNAL_FLAGS)
    except re.error as exc:
        raise LedgerError("%s.signal is not a valid regular expression: %s" % (label, exc))
    expect = row.get("expect") if control else None
    if control and expect not in CONTROL_EXPECTS:
        raise LedgerError("%s.expect must be one of %s" % (label, ", ".join(CONTROL_EXPECTS)))
    # A signal that matches the empty string matches every run, so it cannot
    # discriminate the mutant from the baseline (`(?s).*` is the whole route).
    if re.search(row["signal"], "", SIGNAL_FLAGS) is not None:
        raise LedgerError("%s.signal matches the empty string and cannot discriminate a run" % label)
    # The kill must execute the instrument as a program: a command that only
    # reads the patched bytes (grep, wc, cmp) can call a comment patch "killed"
    # without the mutant ever running, and a bare `echo python3 {inst}` is not
    # an invocation either. The call must sit at a command boundary and the last
    # instrument invocation must end the command — a chain after it
    # (`python3 {inst} --selftest && grep ... {inst}`) can flip the exit on a
    # behavior-equivalent patch. Arguments and redirections may follow it.
    invocations = list(INVOCATION_RE.finditer(row["kill"]))
    if not invocations:
        raise LedgerError(
            "%s.kill must run the instrument as a program: expected `python3 [flags] {inst}` "
            "at a command boundary" % label
        )
    tail = REDIRECTION_RE.sub("", row["kill"][invocations[-1].end():])
    for separator in COMMAND_SEPARATORS:
        if separator in tail:
            raise LedgerError(
                "%s.kill must end at the instrument invocation; %r follows {inst}"
                % (label, separator)
            )
    if control:
        bound = CONTROL_ID_EXPECTS.get(row_id)
        if bound is not None and expect != bound:
            raise LedgerError("%s.expect must be %r for control id %s" % (label, bound, row_id))
    return {
        "id": row_id,
        "instrument": instrument,
        "find": row["find"],
        "replace": row["replace"],
        "kill": row["kill"],
        "live_exit": row["live_exit"],
        "signal": row["signal"],
        "expect": expect,
        "note": row.get("note", ""),
    }


def load_ledger(path):
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        raise LedgerError("cannot read ledger %s: %s" % (path, exc))
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LedgerError("ledger is not UTF-8 JSON: %s" % exc)
    if not isinstance(data, dict):
        raise LedgerError("ledger must be a JSON object")
    if type(data.get("version")) is not int or data["version"] != 1:
        raise LedgerError("unsupported ledger version: %r" % (data.get("version"),))
    limbs = data.get("limbs")
    controls = data.get("controls")
    if not isinstance(limbs, list):
        raise LedgerError("ledger.limbs must be a list")
    if not isinstance(controls, list):
        raise LedgerError("ledger.controls must be a list")
    extras = data.get("copy", [])
    if not isinstance(extras, list):
        raise LedgerError("ledger.copy must be a list of lane-relative paths")
    ledger = {
        "limbs": [validate_row(row, "limbs[%d]" % index, False) for index, row in enumerate(limbs)],
        "controls": [
            validate_row(row, "controls[%d]" % index, True) for index, row in enumerate(controls)
        ],
        "copy": [safe_relative(item, "copy[%d]" % index) for index, item in enumerate(extras)],
    }
    seen = set()
    for row in ledger["limbs"] + ledger["controls"]:
        if row["id"] in seen:
            raise LedgerError("duplicate ledger id: %s" % row["id"])
        seen.add(row["id"])
    return ledger


def load_pristine(root, rows):
    """Read every instrument named by the ledger once, before any scratch copy."""
    pristine = {}
    for row in rows:
        rel = row["instrument"]
        if rel in pristine:
            continue
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            raise LedgerError("instrument not found under the lane root: %s" % rel)
        with open(path, "rb") as handle:
            data = handle.read()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            raise LedgerError("instrument is not UTF-8: %s" % rel)
        pristine[rel] = data
    return pristine


def build_scratch(root, extras):
    """Copy corpus/ (and any declared extra) into a fresh temp lane; return its root."""
    corpus_src = os.path.join(root, "corpus")
    if not os.path.isdir(corpus_src):
        raise LedgerError("lane root has no corpus directory: %s" % root)
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    scratch = tempfile.mkdtemp(prefix="limb-mutation-")
    try:
        shutil.copytree(corpus_src, os.path.join(scratch, "corpus"), symlinks=True, ignore=ignore)
        for rel in extras:
            source = os.path.join(root, rel)
            target = os.path.join(scratch, rel)
            if os.path.isdir(source):
                shutil.copytree(source, target, symlinks=True, ignore=ignore)
            elif os.path.isfile(source):
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(source, target)
            else:
                raise LedgerError("ledger.copy names an absent path: %s" % rel)
    except BaseException:
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    return scratch


def write_bytes(path, data):
    with open(path, "wb") as handle:
        handle.write(data)


def drop_bytecode_cache(instrument_path):
    """Never let a cached .pyc stand in for the bytes under test."""
    shutil.rmtree(os.path.join(os.path.dirname(instrument_path), "__pycache__"), ignore_errors=True)


def run_kill(command, scratch, instrument_path, timeout):
    expanded = command.replace("{inst}", instrument_path).replace("{root}", scratch)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(
            ["bash", "-c", expanded],
            cwd=scratch,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"exit": None, "timed_out": True, "text": ""}
    except OSError as exc:
        raise LedgerError("cannot run a kill command: %s" % exc)
    text = proc.stdout.decode("utf-8", "replace") + "\n" + proc.stderr.decode("utf-8", "replace")
    return {"exit": proc.returncode, "timed_out": False, "text": text}


def display_exit(run):
    return "timeout" if run["timed_out"] else str(run["exit"])


def signal_matches(pattern, text):
    return re.search(pattern, text, SIGNAL_FLAGS) is not None


def yes_no(flag):
    return "y" if flag else "n"


def compiles(path, scratch):
    try:
        py_compile.compile(path, cfile=os.path.join(scratch, ".limb-compile-check.pyc"), doraise=True)
    except py_compile.PyCompileError:
        return False
    return True


IMPORT_GATE = (
    "import importlib.util, sys\n"
    "spec = importlib.util.spec_from_file_location('limb_mutant', sys.argv[1])\n"
    "module = importlib.util.module_from_spec(spec)\n"
    "spec.loader.exec_module(module)\n"
    "print('LIMB-IMPORT-OK')\n"
)
IMPORT_SENTINEL = b"LIMB-IMPORT-OK"
INVOCATION_RE = re.compile(
    r"(?:^|[;&|({]|\bthen\b|\belse\b|\bdo\b|\n)\s*python3(?:\.\d+)?(?:\s+-\S+)*\s+\{inst\}"
)
REDIRECTION_RE = re.compile(r"\d*>&\d*|&>\s*\S+|>\s*\S+|<\s*\S+")
COMMAND_SEPARATORS = (";", "&", "|", "\n", "`", "$(")


def import_verdict(path, scratch, timeout):
    """Exec the mutant's module level in a subprocess, main() not run.

    A patch that only compiles but raises at import (a module-level name bound
    to an undefined name, say) never lets the limb execute: the kill command
    would then differ for a reason the limb does not own. The gate requires both
    a zero exit AND the sentinel printed after `exec_module`, because a module
    level that raises `SystemExit(0)` exits zero without ever running the rest
    of the instrument. Returns "ok", "error", or "timeout"."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(
            [sys.executable, "-c", IMPORT_GATE, path],
            cwd=scratch,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    except OSError as exc:
        raise LedgerError("cannot run the import gate: %s" % exc)
    return "ok" if proc.returncode == 0 and IMPORT_SENTINEL in proc.stdout else "error"


def verdict_row(live_exit, live_signal, mutant_exit, mutant_signal, verdict):
    return {
        "live_exit": live_exit,
        "live_signal": live_signal,
        "mutant_exit": mutant_exit,
        "mutant_signal": mutant_signal,
        "verdict": verdict,
    }


def measure_runs(row, scratch, instrument_path, timeout):
    """Run the kill command twice on one scratch; require the same (exit, signal)."""
    runs = []
    for _ in range(2):
        run = run_kill(row["kill"], scratch, instrument_path, timeout)
        if run["timed_out"]:
            return {"token": "timeout", "exit": None, "display": "timeout", "signal": False}
        runs.append((run["exit"], signal_matches(row["signal"], run["text"])))
    if runs[0] != runs[1]:
        return {"token": "unstable", "exit": runs[0][0], "display": str(runs[0][0]), "signal": runs[0][1]}
    return {"token": "ok", "exit": runs[0][0], "display": str(runs[0][0]), "signal": runs[0][1]}


def measure_side(row, make_scratch, data, timeout):
    """Run one side of a row on its OWN fresh scratch copy of the lane.

    The baseline side and the mutant side never share a scratch, so a kill
    command that counts its own invocations cannot pass the two baseline runs
    and then misbehave on the mutant run (the three-state route)."""
    rel = row["instrument"]
    scratch = make_scratch()
    try:
        instrument_path = os.path.join(scratch, rel)
        if not os.path.isfile(instrument_path):
            raise LedgerError("scratch copy is missing the instrument: %s" % rel)
        write_bytes(instrument_path, data)
        drop_bytecode_cache(instrument_path)
        return measure_runs(row, scratch, instrument_path, timeout)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def evaluate_row(row, make_scratch, pristine, timeout):
    """Baseline side, the pre-mutant gates, then the mutant side.

    `make_scratch` returns a fresh scratch lane copy on every call: the
    baseline runs twice on one, the compile/import gates run on that same
    copy, and the mutant runs twice on a second, untouched copy."""
    rel = row["instrument"]
    original = pristine[rel]
    mutated = None
    scratch = make_scratch()
    try:
        instrument_path = os.path.join(scratch, rel)
        if not os.path.isfile(instrument_path):
            raise LedgerError("scratch copy is missing the instrument: %s" % rel)
        write_bytes(instrument_path, original)
        drop_bytecode_cache(instrument_path)
        live = measure_runs(row, scratch, instrument_path, timeout)
        live_exit = live["display"]
        if live["token"] == "timeout":
            return verdict_row(live_exit, "n", "-", "-", "invalid:timeout")
        if live["token"] == "unstable":
            return verdict_row(live_exit, yes_no(live["signal"]), "-", "-", "invalid:live-baseline")
        if live["exit"] != row["live_exit"] or not live["signal"]:
            return verdict_row(live_exit, yes_no(live["signal"]), "-", "-", "invalid:live-baseline")
        text = original.decode("utf-8")
        if text.count(row["find"]) != 1:
            return verdict_row(live_exit, "y", "-", "-", "invalid:find-count")
        mutated = text.replace(row["find"], row["replace"], 1).encode("utf-8")
        if mutated == original:
            return verdict_row(live_exit, "y", "-", "-", "invalid:noop")
        write_bytes(instrument_path, mutated)
        drop_bytecode_cache(instrument_path)
        if not compiles(instrument_path, scratch):
            return verdict_row(live_exit, "y", "-", "-", "invalid:nocompile")
        imported = import_verdict(instrument_path, scratch, timeout)
        if imported == "timeout":
            return verdict_row(live_exit, "y", "-", "-", "invalid:timeout")
        if imported != "ok":
            return verdict_row(live_exit, "y", "-", "-", "invalid:import")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    mutant = measure_side(row, make_scratch, mutated, timeout)
    if mutant["token"] == "timeout":
        return verdict_row(live_exit, "y", mutant["display"], "n", "invalid:timeout")
    if mutant["token"] == "unstable":
        return verdict_row(
            live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "invalid:mutant-baseline"
        )
    killed = mutant["exit"] != row["live_exit"] or not mutant["signal"]
    return verdict_row(
        live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "killed" if killed else "survivor"
    )


def limb_line(row_id, result):
    return "LIMB %s live=%s/%s mutant=%s/%s verdict=%s" % (
        row_id,
        result["live_exit"],
        result["live_signal"],
        result["mutant_exit"],
        result["mutant_signal"],
        result["verdict"],
    )


def control_line(row_id, result, expect):
    ok = "y" if result["verdict"] == expect else "n"
    return "CONTROL %s verdict=%s expected=%s ok=%s" % (row_id, result["verdict"], expect, ok)


def aggregate(limb_results, control_results, control_expects):
    count = len(limb_results)
    killed = sum(1 for result in limb_results if result["verdict"] == "killed")
    survivors = sum(1 for result in limb_results if result["verdict"] == "survivor")
    rejected = sum(
        1
        for result, expect in zip(control_results, control_expects)
        if result["verdict"] == expect
    )
    ok = (
        count == killed
        and survivors == 0
        and all(result["verdict"] == "killed" for result in limb_results)
        and rejected == len(control_results)
    )
    return (
        ok,
        "limbs=%d killed=%d survivors=%d" % (count, killed, survivors),
        "controls=%d rejected=%d" % (len(control_results), rejected),
    )


def run_ledger(ledger_path, root, timeout):
    ledger = load_ledger(ledger_path)
    guard_ok = run_guard()
    pristine = load_pristine(root, ledger["limbs"] + ledger["controls"])

    def make_scratch():
        return build_scratch(root, ledger["copy"])

    limb_results, control_results = [], []
    for row in ledger["limbs"]:
        result = evaluate_row(row, make_scratch, pristine, timeout)
        limb_results.append(result)
        print(limb_line(row["id"], result), flush=True)
    for row in ledger["controls"]:
        result = evaluate_row(row, make_scratch, pristine, timeout)
        control_results.append(result)
        print(control_line(row["id"], result, row["expect"]), flush=True)
    ok, limb_summary, control_summary = aggregate(
        limb_results, control_results, [row["expect"] for row in ledger["controls"]]
    )
    print(limb_summary)
    print(control_summary)
    return 0 if ok and guard_ok else 1


PROBE_SOURCE = '''#!/usr/bin/env python3
import sys

MODE = "pass"


def main():
    if MODE == "pass":
        print("probe ok")
        return 0
    print("probe fail")
    return 1


if __name__ == "__main__":
    sys.exit(main())
'''


def probe_lane(tmp):
    """Build a throwaway lane holding only the probe instrument."""
    root = os.path.join(tmp, "lane")
    os.makedirs(os.path.join(root, "corpus", "instruments"))
    os.makedirs(os.path.join(root, "corpus", "knowledge"))
    with open(os.path.join(root, "corpus", "instruments", "probe.py"), "w", encoding="utf-8") as handle:
        handle.write(PROBE_SOURCE)
    return root


def guard_rows():
    """The gates the committed ledger never trips, one fixture each."""
    pass_line = 'MODE = "pass"'
    base = {
        "instrument": "corpus/instruments/probe.py",
        "live_exit": 0,
        "signal": "^probe ok$",
        "kill": "python3 {inst}",
        "note": "guard fixture",
    }
    return [
        (
            "invalid-live-baseline",
            dict(base, id="guard-live", find=pass_line, replace='MODE = "fail"', signal="^probe never$"),
            "invalid:live-baseline",
        ),
        (
            "invalid-find-count",
            dict(base, id="guard-find", find='print("probe', replace='print("probe2'),
            "invalid:find-count",
        ),
        (
            "invalid-timeout",
            dict(
                base,
                id="guard-timeout",
                find=pass_line,
                replace='MODE = "fail"',
                kill='if grep -q \'MODE = "fail"\' {inst}; then sleep 5; fi; python3 {inst}',
            ),
            "invalid:timeout",
        ),
    ]


def run_guard():
    """Prove the unexercised verdict gates are still live, on every ledger run."""
    rows = guard_rows()
    failures = 0
    with tempfile.TemporaryDirectory(prefix="limb-guard-") as tmp:
        root = probe_lane(tmp)
        pristine = load_pristine(root, [row for _, row, _ in rows])
        for name, row, want in rows:
            result = evaluate_row(row, lambda: build_scratch(root, []), pristine, GUARD_TIMEOUT)
            ok = result["verdict"] == want
            failures += 0 if ok else 1
            print(
                "guard %-22s verdict=%-20s want=%-20s %s"
                % (name, result["verdict"], want, "ok" if ok else "FAIL"),
                flush=True,
            )
    print("guard cases=%d failures=%d" % (len(rows), failures))
    return failures == 0


def selftest():
    """One internal fixture per verdict path, then both exit-code aggregates."""
    failures = 0
    cases = 0
    with tempfile.TemporaryDirectory(prefix="limb-selftest-") as tmp:
        root = probe_lane(tmp)
        pass_line = 'MODE = "pass"'
        base = {
            "instrument": "corpus/instruments/probe.py",
            "live_exit": 0,
            "signal": "^probe ok$",
            "kill": "python3 {inst}",
            "note": "selftest fixture",
        }
        fixtures = [
            ("killed", dict(base, id="killed", find=pass_line, replace='MODE = "fail"'), "killed"),
            ("survivor", dict(base, id="survivor", find=pass_line, replace="MODE = 'pass'"), "survivor"),
            (
                "invalid-find-count",
                dict(base, id="find-count", find='MODE = "absent"', replace='MODE = "fail"'),
                "invalid:find-count",
            ),
            ("invalid-noop", dict(base, id="noop", find=pass_line, replace=pass_line), "invalid:noop"),
            (
                "invalid-nocompile",
                dict(base, id="nocompile", find="def main():", replace="def main(:"),
                "invalid:nocompile",
            ),
            (
                "invalid-import",
                dict(base, id="import", find=pass_line, replace="MODE = undefined_name"),
                "invalid:import",
            ),
            (
                "invalid-import-exit",
                dict(base, id="import-exit", find=pass_line, replace="raise SystemExit(0)"),
                "invalid:import",
            ),
            (
                "invalid-live-baseline",
                dict(base, id="live-baseline", find=pass_line, replace='MODE = "fail"', signal="^probe never$"),
                "invalid:live-baseline",
            ),
            (
                "invalid-timeout",
                dict(
                    base,
                    id="timeout",
                    find=pass_line,
                    replace='MODE = "fail"',
                    kill='if grep -q \'MODE = "fail"\' {inst}; then sleep 5; fi; python3 {inst}',
                ),
                "invalid:timeout",
            ),
            (
                "invalid-nondeterministic",
                dict(
                    base,
                    id="nondeterministic",
                    find=pass_line,
                    replace='MODE = "fail"',
                    kill='if [ -e {root}/marker ]; then python3 {inst} >/dev/null; exit 7; fi; touch {root}/marker; python3 {inst}',
                ),
                "invalid:live-baseline",
            ),
            (
                "invalid-mutant-baseline",
                dict(
                    base,
                    id="mutant-baseline",
                    find=pass_line,
                    replace="MODE = 'pass'",
                    kill='n=$(cat %s 2>/dev/null || echo 0); n=$((n+1)); printf %%s "$n" > %s; '
                    "if [ \"$n\" = 3 ]; then exit 9; fi; python3 {inst}"
                    % (os.path.join(tmp, "invocations"), os.path.join(tmp, "invocations")),
                ),
                "invalid:mutant-baseline",
            ),
        ]
        results = {}
        pristine = load_pristine(root, [row for _, row, _ in fixtures])
        for name, row, want in fixtures:
            result = evaluate_row(row, lambda: build_scratch(root, []), pristine, 1)
            results[name] = result
            cases += 1
            ok = result["verdict"] == want
            failures += 0 if ok else 1
            print(
                "selftest %-22s verdict=%-20s want=%-20s %s"
                % (name, result["verdict"], want, "ok" if ok else "FAIL")
            )

    validation = [
        (
            "validate-vacuous-signal",
            dict(base, id="vac", find=pass_line, replace='MODE = "fail"', signal="(?s).*"),
            False,
            True,
        ),
        (
            "validate-kill-reads-bytes",
            dict(base, id="grepkill", find=pass_line, replace='MODE = "fail"', kill="grep -q MODE {inst}"),
            False,
            True,
        ),
        (
            "validate-kill-chained",
            dict(
                base,
                id="chained",
                find=pass_line,
                replace='MODE = "fail"',
                kill="python3 {inst} --selftest && grep -q MODE {inst}",
            ),
            False,
            True,
        ),
        (
            "validate-control-misbound",
            dict(base, id="CTL-equivalent", find=pass_line, replace="MODE = 'pass'", expect="invalid:noop"),
            True,
            True,
        ),
        (
            "validate-control-bound",
            dict(base, id="CTL-equivalent", find=pass_line, replace="MODE = 'pass'", expect="survivor"),
            True,
            False,
        ),
        ("validate-valid-row", dict(base, id="valid", find=pass_line, replace='MODE = "fail"'), False, False),
    ]
    for name, row, control, must_raise in validation:
        try:
            validate_row(row, name, control)
            raised = False
        except LedgerError:
            raised = True
        cases += 1
        ok = raised == must_raise
        failures += 0 if ok else 1
        print(
            "selftest %-22s rejected=%-5s want=%-5s %s"
            % (name, raised, must_raise, "ok" if ok else "FAIL")
        )

    green_ok, green_limbs, green_controls = aggregate([results["killed"]], [], [])
    green_ok = green_ok and green_limbs == "limbs=1 killed=1 survivors=0" and green_controls == "controls=0 rejected=0"
    print("selftest aggregate-green       %s" % ("ok" if green_ok else "FAIL"))
    failures += 0 if green_ok else 1
    cases += 1

    red_ok, red_limbs, _ = aggregate([results["killed"], results["survivor"]], [], [])
    red_ok = (not red_ok) and red_limbs == "limbs=2 killed=1 survivors=1"
    print("selftest aggregate-survivor    %s" % ("ok" if red_ok else "FAIL"))
    failures += 0 if red_ok else 1
    cases += 1

    match_ok, _, match_controls = aggregate([], [results["invalid-noop"]], ["invalid:noop"])
    mismatch_ok, _, mismatch_controls = aggregate([], [results["invalid-noop"]], ["survivor"])
    control_ok = (
        match_ok
        and match_controls == "controls=1 rejected=1"
        and (not mismatch_ok)
        and mismatch_controls == "controls=1 rejected=0"
        and control_line("noop", results["invalid-noop"], "invalid:noop").endswith(" ok=y")
        and control_line("noop", results["invalid-noop"], "survivor").endswith(" ok=n")
    )
    print("selftest control-verdict-rule  %s" % ("ok" if control_ok else "FAIL"))
    failures += 0 if control_ok else 1
    cases += 1

    print("selftest cases=%d failures=%d" % (cases, failures))
    return 0 if failures == 0 else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ledger", help="path to the one-limb mutation ledger (JSON)")
    parser.add_argument("--root", help="lane root to copy (default: derived from this script's path)")
    parser.add_argument("--selftest", action="store_true", help="run the internal verdict fixtures")
    args = parser.parse_args(argv)
    if args.selftest:
        if args.ledger is not None or args.root is not None:
            print("limb-mutation-check: --selftest takes no --ledger or --root", file=sys.stderr)
            return 2
        return selftest()
    if args.ledger is None:
        parser.print_usage(sys.stderr)
        print("limb-mutation-check: --ledger is required", file=sys.stderr)
        return 2
    root = os.path.abspath(args.root) if args.root else lane_root_from_script()
    if not os.path.isdir(root):
        print("limb-mutation-check: lane root is not a directory: %s" % root, file=sys.stderr)
        return 2
    if not os.path.isfile(args.ledger):
        print("limb-mutation-check: ledger not found: %s" % args.ledger, file=sys.stderr)
        return 2
    try:
        return run_ledger(args.ledger, root, TIMEOUT_SECONDS)
    except LedgerError as exc:
        print("limb-mutation-check: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
