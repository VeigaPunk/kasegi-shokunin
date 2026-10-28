#!/usr/bin/env python3
"""freeze-check.py — replay every frozen claim counter at the BASE before freeze, v1.

WHY THIS INSTRUMENT EXISTS
    Round 44 froze a C2 counter string,

        grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md

    whose regex had the wrong shape (the frontier status is the THIRD cell), so it
    printed 0 at the base while the claim's `expect_before` said 25.  Nobody ran the
    string on the base before freeze (`corpus/lessons/round-44-verifier-spotcheck.md`
    section 6 item 4).  This tool is that run: for every claim of a
    `kasegi-round-claims-v2` file it renders the counter command with tree=base,
    runs it, and requires the BASE reading to be exactly the frozen `expect_before`
    and NOT the frozen `expect_after`.

PASS RULE (per claim; all must hold, else verdict=FAIL)
    1. the claim carries all three fields `counter_cmd`, `expect_before`,
       `expect_after` (non-empty single-line strings) and an `id`;
    2. some output line (stdout+stderr merged) equals `expect_before` AS A WHOLE
       LINE (surrounding whitespace ignored) — `fixed=0` never matches `fixed=0x`,
       `xfixed=0`, or `total=5 fixed=0 unresolved=5` (R41: whole token, both ends);
    3. NO output line equals `expect_after` (a counter already green at the base is
       a do-nothing pass: the claim is not a measurement).
    A nonzero counter exit is NOT a failure by itself: counters are red at base.
    A timeout, a crash with no matching line, or a missing counter file is rule 2
    failing (or `timeout`/`spawn-error`), not a pass.

USAGE
    python3 freeze-check.py --claims PATH --tool-root DIR --base DIR [--work DIR] [--timeout S]
    python3 freeze-check.py --selftest [--work DIR]

    {tool} -> --tool-root (also the child's cwd), {tree} and {base} -> --base.
    The child env gets R45_FREEZE_CHECK=1 and PYTHONDONTWRITEBYTECODE=1; TMPDIR is
    inherited (no hardcoded /tmp).  Default timeout 300 s per claim.  --work is the
    scratch root for --selftest only.  READ-ONLY over --tool-root and --base.

OUTPUT
    claim <id> base_read=<matched line | last output line> verdict=ok|FAIL
    finding <id> <code> <detail>            (FAIL only; codes below)
    freeze-check claims=<n> base_ok=<k> exit=0|1
    --selftest ends with: selftest cases=<N> failures=<F>

FINDING CODES
    bad-claims-file  unreadable / not JSON / not an object / claims not a list
    bad-schema       schema is not kasegi-round-claims-v2
    no-claims        the file holds zero claims
    missing-field    id / counter_cmd / expect_before / expect_after absent or empty
    multiline-expect an expect_* value spans lines (a line match is undefined)
    spawn-error      the command could not be started
    timeout          the counter exceeded the timeout (process group killed)
    before-mismatch  no output line equals expect_before
    after-at-base    an output line equals expect_after (do-nothing green)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile

SCHEMA = "kasegi-round-claims-v2"
FIELDS = ("counter_cmd", "expect_before", "expect_after")
DEFAULT_TIMEOUT = 300
PURE_README = "/fast/scratch/hyaku/kasegi-r45/L1/pure/corpus/README.md"
SUMMARY_RE = re.compile(r"^freeze-check claims=(\d+) base_ok=(\d+) exit=([01])$")


# --------------------------------------------------------------------------- core
def render(cmd: str, tool: str, base: str) -> str:
    """Replace the three placeholders literally (str.replace: awk/shell braces survive)."""
    return (cmd.replace("{tool}", shlex.quote(tool))
               .replace("{tree}", shlex.quote(base))
               .replace("{base}", shlex.quote(base)))


def run_counter(cmd: str, cwd: str, timeout: float) -> tuple[str, int | None, str | None]:
    """Run `cmd` in a shell in cwd.  Returns (output, exit_code, error_code)."""
    env = dict(os.environ)
    env["R45_FREEZE_CHECK"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.Popen(["/bin/sh", "-c", cmd], cwd=cwd, env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, start_new_session=True)
    except OSError as exc:
        return f"{type(exc).__name__}: {exc}", None, "spawn-error"
    try:
        out, _ = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
        out, _ = proc.communicate()
        return out.decode("utf-8", "replace"), None, "timeout"
    return out.decode("utf-8", "replace"), proc.returncode, None


def one_line(text: str, limit: int = 200) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + "..."


def whole_line_match(lines: list[str], expect: str) -> str | None:
    want = expect.strip()
    for line in lines:
        if line.strip() == want:
            return line.strip()
    return None


def check_claim(claim: dict, index: int, tool: str, base: str, timeout: float):
    """Return (id, base_read, findings[(code, detail)])."""
    cid = claim.get("id") if isinstance(claim.get("id"), str) and claim.get("id").strip() else None
    label = cid or f"#{index}"
    findings: list[tuple[str, str]] = []
    missing = (["id"] if cid is None else []) + [
        f for f in FIELDS if not (isinstance(claim.get(f), str) and claim[f].strip())]
    if missing:
        findings.append(("missing-field", "absent or empty: " + ",".join(missing)))
        return label, "<not-run>", findings
    for f in ("expect_before", "expect_after"):
        if "\n" in claim[f].strip():
            findings.append(("multiline-expect", f"{f} spans lines"))
    if findings:
        return label, "<not-run>", findings

    out, code, err = run_counter(render(claim["counter_cmd"], tool, base), tool, timeout)
    lines = out.splitlines()
    last = next((l.strip() for l in reversed(lines) if l.strip()), "<no-output>")
    if err:
        findings.append((err, f"counter {err} after {timeout:g}s limit" if err == "timeout"
                         else one_line(out)))
        return label, one_line(last), findings
    hit = whole_line_match(lines, claim["expect_before"])
    if hit is None:
        findings.append(("before-mismatch",
                         f"no output line equals expect_before {claim['expect_before']!r}; "
                         f"exit={code}"))
    bad = whole_line_match(lines, claim["expect_after"])
    if bad is not None:
        findings.append(("after-at-base",
                         f"base already prints expect_after {claim['expect_after']!r}"))
    return label, one_line(hit if hit is not None else last), findings


def run(claims_path: str, tool: str, base: str, timeout: float, out=sys.stdout) -> int:
    def finish(n: int, ok: int) -> int:
        code = 0 if n > 0 and ok == n else 1
        print(f"freeze-check claims={n} base_ok={ok} exit={code}", file=out)
        return code

    try:
        with open(claims_path, "rb") as fh:
            doc = json.loads(fh.read().decode("utf-8"))
    except (OSError, ValueError) as exc:
        print(f"finding - bad-claims-file {one_line(str(exc))}", file=out)
        return finish(0, 0)
    if not isinstance(doc, dict) or not isinstance(doc.get("claims"), list):
        print("finding - bad-claims-file top level is not an object with a claims list", file=out)
        return finish(0, 0)
    if doc.get("schema") != SCHEMA:
        print(f"finding - bad-schema schema={doc.get('schema')!r} want {SCHEMA}", file=out)
        return finish(0, 0)
    claims = doc["claims"]
    if not claims:
        print("finding - no-claims the claims list is empty", file=out)
        return finish(0, 0)

    ok = 0
    for i, claim in enumerate(claims, 1):
        if not isinstance(claim, dict):
            label, read, findings = f"#{i}", "<not-run>", [("missing-field", "claim is not an object")]
        else:
            label, read, findings = check_claim(claim, i, tool, base, timeout)
        verdict = "FAIL" if findings else "ok"
        ok += not findings
        print(f"claim {label} base_read={read} verdict={verdict}", file=out)
        for code, detail in findings:
            print(f"finding {label} {code} {one_line(detail)}", file=out)
    return finish(len(claims), ok)


# ----------------------------------------------------------------------- selftest
class Fix:
    """One isolated fixture: tool/ base/ dirs and a claims.json under work/<name>."""

    def __init__(self, work: str, name: str):
        self.dir = os.path.join(work, name)
        self.tool = os.path.join(self.dir, "tool")
        self.base = os.path.join(self.dir, "base")
        self.claims = os.path.join(self.dir, "claims.json")
        os.makedirs(self.tool)
        os.makedirs(self.base)

    def counter(self, body: str, name: str = "c.py") -> str:
        with open(os.path.join(self.tool, name), "w", encoding="utf-8") as fh:
            fh.write(body)
        return name

    def write_claims(self, claims: list, schema: str = SCHEMA) -> None:
        with open(self.claims, "w", encoding="utf-8") as fh:
            json.dump({"schema": schema, "lane": "fixture", "round": 0, "claims": claims}, fh)


def drive(fx: Fix, extra: list[str] | None = None, env_extra: dict | None = None,
          tool: str | None = None, base: str | None = None) -> dict:
    env = dict(os.environ)
    env.update(env_extra or {})
    cmd = [sys.executable, os.path.abspath(__file__), "--claims", fx.claims,
           "--tool-root", tool or fx.tool, "--base", base or fx.base] + (extra or [])
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
                       timeout=120, check=False)
    text = p.stdout.decode("utf-8", "replace")
    lines = text.splitlines()
    m = next((SUMMARY_RE.match(l) for l in reversed(lines) if SUMMARY_RE.match(l)), None)
    return {
        "rc": p.returncode,
        "text": text,
        "summary": m,
        "claims": {l.split()[1]: l for l in lines if l.startswith("claim ")},
        "findings": [tuple(l.split(" ", 3)[1:3]) for l in lines if l.startswith("finding ")],
    }


def readme_source() -> str | None:
    for cand in (os.environ.get("R45_PURE_README"), PURE_README,
                 os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "README.md")):
        if cand and os.path.isfile(cand):
            return cand
    return None


def admitted_rows(path: str) -> int:
    pat = re.compile(r"^\|\s*F\d+\s*\|[^|]*\|\s*admitted\s*\|")
    with open(path, encoding="utf-8") as fh:
        return sum(1 for l in fh if pat.match(l))


def selftest(work_arg: str | None) -> int:
    created = work_arg is None
    work = work_arg or tempfile.mkdtemp(prefix="freeze-check-st-")
    os.makedirs(work, exist_ok=True)
    work = os.path.abspath(work)
    results: list[tuple[str, bool, str]] = []

    def case(name: str, fx: Fix, res: dict, *, rc: int, ok: int, n: int,
             findings: list[tuple[str, str]], reads: dict | None = None,
             verdicts: dict | None = None, absent: tuple = ()) -> None:
        why = []
        if res["rc"] != rc:
            why.append(f"rc={res['rc']} want {rc}")
        s = res["summary"]
        if s is None:
            why.append("no summary line")
        else:
            if (int(s.group(1)), int(s.group(2)), int(s.group(3))) != (n, ok, rc):
                why.append(f"summary {s.group(0)!r} want claims={n} base_ok={ok} exit={rc}")
        got = list(res["findings"])
        for f in findings:
            if f not in got:
                why.append(f"finding {f} missing from {got}")
        for code in absent:
            if any(c == code for _, c in got):
                why.append(f"unexpected finding {code} in {got}")
        for cid, v in (verdicts or {}).items():
            line = res["claims"].get(cid, "")
            if not line.endswith(f"verdict={v}"):
                why.append(f"claim {cid} line {line!r} want verdict={v}")
        for cid, frag in (reads or {}).items():
            line = res["claims"].get(cid, "")
            if f"base_read={frag} verdict=" not in line:
                why.append(f"claim {cid} line {line!r} lacks base_read={frag!r}")
        results.append((name, not why, "; ".join(why) or "as expected"))

    try:
        # (1) good claim: noise lines, counter exits 1 (red at base) -> ok, rc 0
        fx = Fix(work, "c1-good")
        fx.counter("import sys\nprint('noise line')\n"
                   "print('widget total=5 fixed=0 unresolved=5 exit=1')\nsys.exit(1)\n")
        fx.write_claims([{"id": "G1", "counter_cmd": "python3 {tool}/c.py --root {tree}",
                          "expect_before": "widget total=5 fixed=0 unresolved=5 exit=1",
                          "expect_after": "widget total=5 fixed=5 unresolved=0 exit=0"}])
        case("1 good claim, red counter exit 1", fx, drive(fx), rc=0, ok=1, n=1, findings=[],
             verdicts={"G1": "ok"}, reads={"G1": "widget total=5 fixed=0 unresolved=5 exit=1"})

        # (2) round-44 defect shape: frozen grep string vs the real README
        src = readme_source()
        fx = Fix(work, "c2-r44-shape")
        if src is None:
            results.append(("2 round-44 frozen-string shape", False, "no README source found"))
        else:
            os.makedirs(os.path.join(fx.base, "corpus"))
            shutil.copyfile(src, os.path.join(fx.base, "corpus", "README.md"))
            real = admitted_rows(src)
            frozen = r"grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md"
            fixed = r"grep -cE '^\| F[0-9]+ \| [^|]* \| admitted \|' {tree}/corpus/README.md"
            fx.write_claims([
                {"id": "R44", "counter_cmd": frozen, "expect_before": str(real),
                 "expect_after": str(real + 1)},
            ])
            # tool-root == base == the fixture holding only the copied README
            case(f"2 round-44 frozen string prints 0, expect_before {real} -> FAIL", fx,
                 drive(fx, tool=fx.base), rc=1, ok=0, n=1,
                 findings=[("R44", "before-mismatch")], verdicts={"R44": "FAIL"},
                 reads={"R44": "0"}, absent=("after-at-base",))
            fx.write_claims([{"id": "R44fix", "counter_cmd": fixed, "expect_before": str(real),
                              "expect_after": str(real + 1)}])
            case(f"2b table-aware string prints {real} -> ok (tool is not fail-always)", fx,
                 drive(fx, tool=fx.base), rc=0, ok=1, n=1, findings=[],
                 verdicts={"R44fix": "ok"}, reads={"R44fix": str(real)})

        # (3) do-nothing green: base already satisfies expect_after
        fx = Fix(work, "c3-do-nothing")
        fx.counter("print('widget fixed=5 exit=0')\n")
        fx.write_claims([{"id": "DN", "counter_cmd": "python3 {tool}/c.py",
                          "expect_before": "widget fixed=0 exit=1",
                          "expect_after": "widget fixed=5 exit=0"}])
        case("3 do-nothing green (prints expect_after at base) -> FAIL", fx, drive(fx), rc=1,
             ok=0, n=1, findings=[("DN", "after-at-base")], verdicts={"DN": "FAIL"})
        fx = Fix(work, "c3b-both-lines")
        fx.counter("print('widget fixed=0 exit=1')\nprint('widget fixed=5 exit=0')\n")
        fx.write_claims([{"id": "DB", "counter_cmd": "python3 {tool}/c.py",
                          "expect_before": "widget fixed=0 exit=1",
                          "expect_after": "widget fixed=5 exit=0"}])
        case("3b before line present AND after line present -> FAIL after-at-base only", fx,
             drive(fx), rc=1, ok=0, n=1, findings=[("DB", "after-at-base")],
             verdicts={"DB": "FAIL"}, absent=("before-mismatch",))

        # (4) claim without expect_before (also: without expect_after, counter_cmd, id)
        fx = Fix(work, "c4-missing-field")
        fx.counter("print('widget fixed=0 exit=1')\n")
        fx.write_claims([
            {"id": "NB", "counter_cmd": "python3 {tool}/c.py", "expect_after": "widget fixed=5"},
            {"id": "NA", "counter_cmd": "python3 {tool}/c.py", "expect_before": "widget fixed=0 exit=1"},
            {"id": "NC", "expect_before": "widget fixed=0 exit=1", "expect_after": "x"},
            {"counter_cmd": "python3 {tool}/c.py", "expect_before": "widget fixed=0 exit=1",
             "expect_after": "x"},
            {"id": "EB", "counter_cmd": "python3 {tool}/c.py", "expect_before": "  ",
             "expect_after": "x"},
        ])
        case("4 claims missing expect_before/expect_after/counter_cmd/id/blank -> FAIL", fx,
             drive(fx), rc=1, ok=0, n=5,
             findings=[("NB", "missing-field"), ("NA", "missing-field"), ("NC", "missing-field"),
                       ("#4", "missing-field"), ("EB", "missing-field")],
             verdicts={"NB": "FAIL", "NA": "FAIL", "NC": "FAIL", "EB": "FAIL"})

        # (5) crash with no matching line (traceback; also command-not-found and absent file)
        fx = Fix(work, "c5-crash")
        fx.counter("raise RuntimeError('boom')\n")
        fx.write_claims([
            {"id": "CR", "counter_cmd": "python3 {tool}/c.py", "expect_before": "widget fixed=0 exit=1",
             "expect_after": "widget fixed=5 exit=0"},
            {"id": "NF", "counter_cmd": "definitely-not-a-command-xyz {tree}",
             "expect_before": "widget fixed=0 exit=1", "expect_after": "widget fixed=5 exit=0"},
            {"id": "AF", "counter_cmd": "python3 {tool}/absent.py",
             "expect_before": "widget fixed=0 exit=1", "expect_after": "widget fixed=5 exit=0"},
        ])
        case("5 crash / command-not-found / absent counter, no matching line -> FAIL", fx,
             drive(fx), rc=1, ok=0, n=3,
             findings=[("CR", "before-mismatch"), ("NF", "before-mismatch"), ("AF", "before-mismatch")],
             verdicts={"CR": "FAIL", "NF": "FAIL", "AF": "FAIL"}, reads={"CR": "RuntimeError: boom"})

        # (6) token only as a substring (R41): fixed=0x, xfixed=0, longer line, 0 vs 05
        fx = Fix(work, "c6-substring")
        fx.counter("print('fixed=0x')\n", "a.py")
        fx.counter("print('xfixed=0')\n", "b.py")
        fx.counter("print('routed total=5 fixed=0 unresolved=5')\n", "c.py")
        fx.counter("print('closed=7/80')\n", "d.py")
        fx.write_claims([
            {"id": "S1", "counter_cmd": "python3 {tool}/a.py", "expect_before": "fixed=0",
             "expect_after": "fixed=1"},
            {"id": "S2", "counter_cmd": "python3 {tool}/b.py", "expect_before": "fixed=0",
             "expect_after": "fixed=1"},
            {"id": "S3", "counter_cmd": "python3 {tool}/c.py", "expect_before": "fixed=0",
             "expect_after": "fixed=1"},
            {"id": "S4", "counter_cmd": "python3 {tool}/d.py", "expect_before": "closed=7/8",
             "expect_after": "closed=8/8"},
        ])
        case("6 token only as substring (fixed=0x, xfixed=0, mid-line, closed=7/80) -> FAIL", fx,
             drive(fx), rc=1, ok=0, n=4,
             findings=[("S1", "before-mismatch"), ("S2", "before-mismatch"),
                       ("S3", "before-mismatch"), ("S4", "before-mismatch")],
             verdicts={"S1": "FAIL", "S2": "FAIL", "S3": "FAIL", "S4": "FAIL"},
             reads={"S1": "fixed=0x"})

        # (7) timeout kills the process group and fails
        fx = Fix(work, "c7-timeout")
        fx.counter("import time\ntime.sleep(60)\n")
        fx.write_claims([{"id": "TO", "counter_cmd": "python3 {tool}/c.py",
                          "expect_before": "x", "expect_after": "y"}])
        case("7 counter exceeding --timeout 2 -> FAIL timeout", fx, drive(fx, ["--timeout", "2"]),
             rc=1, ok=0, n=1, findings=[("TO", "timeout")], verdicts={"TO": "FAIL"})

        # (8) child env + cwd + placeholders: tree=base, cwd=tool-root, TMPDIR honored
        fx = Fix(work, "c8-env")
        tmpd = os.path.join(fx.dir, "tmpd")
        os.makedirs(tmpd)
        fx.counter("import os, sys\n"
                   "print('env=%s tmp=%s cwd=%s' % (os.environ.get('R45_FREEZE_CHECK'),"
                   " os.environ.get('TMPDIR'), os.getcwd()))\n"
                   "print('args=%s' % ' '.join(sys.argv[1:]))\n")
        want_env = f"env=1 tmp={tmpd} cwd={os.path.realpath(fx.tool)}"
        want_args = f"args=--root {fx.base} --baseline {fx.base}"
        fx.write_claims([
            {"id": "EV", "counter_cmd": "python3 {tool}/c.py --root {tree} --baseline {base}",
             "expect_before": want_env, "expect_after": "never"},
            {"id": "AR", "counter_cmd": "python3 {tool}/c.py --root {tree} --baseline {base}",
             "expect_before": want_args, "expect_after": "never"},
        ])
        case("8 child env R45_FREEZE_CHECK=1, TMPDIR passthrough, cwd=tool-root, tree=base", fx,
             drive(fx, env_extra={"TMPDIR": tmpd}), rc=0, ok=2, n=2, findings=[],
             verdicts={"EV": "ok", "AR": "ok"})

        # (9) mixed file: one good, one bad -> exit 1, base_ok=1 (no partial pass)
        fx = Fix(work, "c9-mixed")
        fx.counter("print('widget fixed=0 exit=1')\n")
        fx.write_claims([
            {"id": "M1", "counter_cmd": "python3 {tool}/c.py", "expect_before": "widget fixed=0 exit=1",
             "expect_after": "widget fixed=5 exit=0"},
            {"id": "M2", "counter_cmd": "python3 {tool}/c.py", "expect_before": "widget fixed=0",
             "expect_after": "widget fixed=5 exit=0"},
        ])
        case("9 mixed good+bad claim -> exit 1, base_ok=1", fx, drive(fx), rc=1, ok=1, n=2,
             findings=[("M2", "before-mismatch")], verdicts={"M1": "ok", "M2": "FAIL"})

        # (10) file-level defects: wrong schema, empty claims, unreadable, multi-line expect
        fx = Fix(work, "c10-file-level")
        fx.write_claims([], schema=SCHEMA)
        r_empty = drive(fx)
        fx.write_claims([{"id": "X"}], schema="kasegi-round-claims-v1")
        r_schema = drive(fx)
        with open(fx.claims, "w", encoding="utf-8") as fh:
            fh.write("{not json")
        r_bad = drive(fx)
        fx.counter("print('a')\nprint('b')\n")
        fx.write_claims([{"id": "ML", "counter_cmd": "python3 {tool}/c.py",
                          "expect_before": "a\nb", "expect_after": "z"}])
        r_ml = drive(fx)
        case("10a empty claims list -> FAIL no-claims", fx, r_empty, rc=1, ok=0, n=0,
             findings=[("-", "no-claims")])
        case("10b wrong schema -> FAIL bad-schema", fx, r_schema, rc=1, ok=0, n=0,
             findings=[("-", "bad-schema")])
        case("10c unreadable JSON -> FAIL bad-claims-file", fx, r_bad, rc=1, ok=0, n=0,
             findings=[("-", "bad-claims-file")])
        case("10d multi-line expect_before -> FAIL multiline-expect", fx, r_ml, rc=1, ok=0, n=1,
             findings=[("ML", "multiline-expect")], verdicts={"ML": "FAIL"})
    finally:
        for name, passed, why in results:
            print(f"case {'PASS' if passed else 'FAIL'}: {name} [{why}]")
        failures = sum(1 for _, p, _ in results if not p)
        print(f"selftest cases={len(results)} failures={failures}")
        for sub in os.listdir(work) if os.path.isdir(work) else ():
            if sub.startswith("c") and sub[1:2].isdigit():
                shutil.rmtree(os.path.join(work, sub), ignore_errors=True)
        if created:
            shutil.rmtree(work, ignore_errors=True)
    return 0 if failures == 0 and results else 1


# ---------------------------------------------------------------------------- CLI
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Replay frozen claim counters at the base.")
    ap.add_argument("--claims")
    ap.add_argument("--tool-root")
    ap.add_argument("--base")
    ap.add_argument("--work")
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.work)
    if not (a.claims and a.tool_root and a.base):
        ap.error("--claims, --tool-root and --base are required (or use --selftest)")
    return run(a.claims, os.path.abspath(a.tool_root), os.path.abspath(a.base), a.timeout)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
