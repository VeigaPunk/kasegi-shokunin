#!/usr/bin/env python3
"""freeze-check.py - replay a kasegi-round-claims-v2 file against the frozen base.

Round-44 defect it closes: a counter frozen as
    grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md
printed 0 at the base AND after landing, because the status is the third table
cell, so the frozen claim could never go green.  The claim text was never replayed
at the freeze commit.  This tool replays every claim's counter_cmd at the base
tree and refuses the freeze unless the counter reads exactly what the claim says.

Usage
  freeze-check.py --claims PATH --tool-root DIR --base DIR [--work DIR] [--timeout S]
  freeze-check.py --selftest [--work DIR] [--base DIR]

For each claim: counter_cmd is rendered with {tool}=tool-root, {tree}={base}=base
(each shell-quoted), run with `bash -c` in tool-root (stdout+stderr merged, child
env R45_FREEZE_CHECK=1, TMPDIR explicit, default timeout 300 s).  A nonzero counter
exit is NOT a failure (counters are red at the base).  The claim is ok only when:
  * it carries non-empty counter_cmd, expect_before, expect_after;
  * some output line, stripped, EQUALS expect_before (whole line, never a substring:
    `fixed=0` does not match `fixed=0x` or `xfixed=0`, R41);
  * no output line contains expect_after (a counter already green at the base is a
    do-nothing pass);
  * expect_before != expect_after, counter_cmd mentions {tree} or {base}, ids are
    unique, and the counter left the base tree byte-for-byte untouched (counters are
    read-only; checked as relative path + size + mtime_ns).
Findings (stable ids, printed as `finding <claim> <ID> <detail>`):
  FC-SCHEMA FC-NO-CLAIMS FC-DUP-ID FC-MISSING-FIELD FC-BEFORE-EQ-AFTER FC-NO-TREE
  FC-NO-MATCH FC-AFTER-AT-BASE FC-TIMEOUT FC-BASE-MUTATED
Exit 0 only when claims>0, every claim is ok and there is no file-level finding.
--work: scratch root; as a check it becomes the children's TMPDIR (created if
missing, otherwise TMPDIR is inherited); in --selftest it holds the fixtures.
"""
import argparse
import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile

SCHEMA = "kasegi-round-claims-v2"
REQUIRED = ("counter_cmd", "expect_before", "expect_after")
DEFAULT_TIMEOUT = 300
PURE_DEFAULT = "/fast/scratch/hyaku/kasegi-r45/L1/pure"
FROZEN_BASE_REV = "dc5bb8c6e31efc4a6650819df85e79b72fd64bcd"


def snapshot(base):
    """Relative path -> (size, mtime_ns) for files, None for dirs."""
    snap = {}
    for root, dirs, files in os.walk(base):
        for name in dirs:
            p = os.path.join(root, name)
            snap[os.path.relpath(p, base) + "/"] = None
        for name in files:
            p = os.path.join(root, name)
            try:
                st = os.lstat(p)
                snap[os.path.relpath(p, base)] = (st.st_size, st.st_mtime_ns)
            except OSError:
                snap[os.path.relpath(p, base)] = ("gone", 0)
    return snap


def run_counter(cmd, tool_root, tmpdir, timeout):
    """-> (rc|None, lines, timed_out)."""
    env = dict(os.environ)
    env["R45_FREEZE_CHECK"] = "1"
    env["TMPDIR"] = tmpdir
    p = subprocess.Popen(
        ["bash", "-c", cmd], cwd=tool_root, env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        rc, timed_out = p.returncode, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
        rc, timed_out = None, True
    text = (out or b"").decode("utf-8", "replace")
    return rc, text.splitlines(), timed_out


def render(cmd, tool_root, base):
    return (cmd.replace("{tool}", shlex.quote(tool_root))
               .replace("{tree}", shlex.quote(base))
               .replace("{base}", shlex.quote(base)))


def clip(s, n=200):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 3] + "..."


def check(claims_path, tool_root, base, work=None, timeout=DEFAULT_TIMEOUT):
    """-> (output_lines, exit_code, findings[(claim_id, finding_id, detail)])."""
    out, findings = [], []
    tool_root, base = os.path.abspath(tool_root), os.path.abspath(base)
    if work:
        os.makedirs(work, exist_ok=True)
        tmpdir = os.path.abspath(work)
    else:
        tmpdir = os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        with open(claims_path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        findings.append(("-", "FC-SCHEMA", "claims file unreadable: %s" % clip(str(exc))))
        doc = {}
    if not isinstance(doc, dict):
        findings.append(("-", "FC-SCHEMA", "top level is not an object"))
        doc = {}
    elif doc and doc.get("schema") != SCHEMA:
        findings.append(("-", "FC-SCHEMA", "schema=%r, want %r" % (doc.get("schema"), SCHEMA)))
    claims = doc.get("claims") if isinstance(doc.get("claims"), list) else []
    if not claims:
        findings.append(("-", "FC-NO-CLAIMS", "no claims to replay"))
    file_level = len(findings)
    for f in findings:
        out.append("finding %s %s %s" % f)

    base_ok, seen = 0, set()
    for idx, claim in enumerate(claims):
        if not isinstance(claim, dict):
            claim = {}
        cid = claim.get("id") if isinstance(claim.get("id"), str) and claim.get("id") else "#%d" % (idx + 1)
        local = []
        if cid in seen:
            local.append(("FC-DUP-ID", "id %s appears more than once" % cid))
        seen.add(cid)
        vals = {k: claim.get(k) for k in REQUIRED}
        missing = [k for k in REQUIRED if not (isinstance(vals[k], str) and vals[k].strip())]
        if missing:
            local.append(("FC-MISSING-FIELD", "absent or empty: " + ",".join(missing)))
        eb = vals["expect_before"].strip() if "expect_before" not in missing else None
        ea = vals["expect_after"].strip() if "expect_after" not in missing else None
        cmd = vals["counter_cmd"] if "counter_cmd" not in missing else None
        if eb is not None and ea is not None and eb == ea:
            local.append(("FC-BEFORE-EQ-AFTER", "expect_before equals expect_after: %s" % clip(eb)))
        if cmd is not None and "{tree}" not in cmd and "{base}" not in cmd:
            local.append(("FC-NO-TREE", "counter_cmd reads neither {tree} nor {base}"))

        read = "n/a"
        if cmd is not None:
            before_snap = snapshot(base) if os.path.isdir(base) else {}
            rc, lines, timed_out = run_counter(render(cmd, tool_root, base), tool_root, tmpdir, timeout)
            after_snap = snapshot(base) if os.path.isdir(base) else {}
            stripped = [ln.strip() for ln in lines]
            nonempty = [ln for ln in stripped if ln]
            if timed_out:
                local.append(("FC-TIMEOUT", "counter exceeded %s s" % timeout))
            if before_snap != after_snap:
                changed = sorted(set(before_snap) ^ set(after_snap) |
                                 {k for k in before_snap if k in after_snap and before_snap[k] != after_snap[k]})
                local.append(("FC-BASE-MUTATED", "counter changed the base tree: %s" % clip(",".join(changed[:5]))))
            matched = None
            if eb is not None:
                matched = next((ln for ln in stripped if ln == eb), None)
                if matched is None and not timed_out:
                    local.append(("FC-NO-MATCH", "no output line equals expect_before %r; rc=%s" % (clip(eb), rc)))
            if ea is not None and any(ea in ln for ln in stripped):
                local.append(("FC-AFTER-AT-BASE", "counter output already contains expect_after %r" % clip(ea)))
            read = matched if matched is not None else (nonempty[-1] if nonempty else "<no-output>")
        verdict = "ok" if not local else "FAIL"
        if not local:
            base_ok += 1
        out.append("claim %s base_read=%s verdict=%s" % (cid, clip(read), verdict))
        for fid, detail in local:
            out.append("finding %s %s %s" % (cid, fid, detail))
            findings.append((cid, fid, detail))
    code = 0 if (claims and base_ok == len(claims) and file_level == 0) else 1
    out.append("freeze-check claims=%d base_ok=%d exit=%d" % (len(claims), base_ok, code))
    return out, code, findings


# ----------------------------------------------------------------------------- selftest

def locate_readme(base_arg):
    """Real base README bytes: --base, the L1 pure export, or git show of the frozen base."""
    cands = [p for p in (base_arg, PURE_DEFAULT) if p]
    for root in cands:
        p = os.path.join(root, "corpus", "README.md")
        if os.path.isfile(p):
            return open(p, "rb").read(), p
    here = os.path.dirname(os.path.abspath(__file__))
    for top in (os.path.dirname(os.path.dirname(here)), os.getcwd()):
        try:
            data = subprocess.run(
                ["git", "-C", top, "show", "%s:corpus/README.md" % FROZEN_BASE_REV],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True).stdout
            return data, "git:%s:%s" % (top, FROZEN_BASE_REV)
        except (OSError, subprocess.CalledProcessError):
            continue
    return None, None


def admitted_rows(readme_bytes):
    """Table-aware count: row whose 1st cell is F<n> and 3rd cell is `admitted`."""
    n = 0
    for ln in readme_bytes.decode("utf-8", "replace").splitlines():
        cells = [c.strip() for c in ln.split("|")]
        if len(cells) > 4 and cells[0] == "" and cells[1].startswith("F") and cells[1][1:].isdigit() \
                and cells[3] == "admitted":
            n += 1
    return n


def selftest(work=None, base_arg=None, timeout=DEFAULT_TIMEOUT):
    own = work is None
    root = tempfile.mkdtemp(prefix="freeze-check-selftest-", dir=None if own else (os.makedirs(work, exist_ok=True) or work))
    root = os.path.abspath(root)
    tool_root = os.path.join(root, "tool")
    os.makedirs(tool_root)
    results = []  # (name, ok, note)
    counter = [0]

    def mkbase(files=None):
        counter[0] += 1
        d = os.path.join(root, "base%d" % counter[0])
        os.makedirs(d)
        for rel, data in (files or {"marker.txt": b"x\n"}).items():
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as fh:
                fh.write(data)
        return d

    def claim(cid="C", cmd="echo 'T fixed=0 exit=1'", eb="T fixed=0 exit=1", ea="T fixed=1 exit=0", raw=False):
        if cmd is not None and not raw and "{tree}" not in cmd:
            cmd = ": {tree}; " + cmd
        c = {"id": cid, "counter_cmd": cmd, "expect_before": eb, "expect_after": ea}
        return {k: v for k, v in c.items() if v is not None}

    def case(name, claims, want_code, want_ids, base=None, schema=SCHEMA, tmo=timeout, extra=None):
        base = base or mkbase()
        counter[0] += 1
        cp = os.path.join(root, "claims%d.json" % counter[0])
        doc = {"schema": schema, "claims": claims}
        with open(cp, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        tmp = os.path.join(root, "tmp")
        out, code, _ = check(cp, tool_root, base, work=tmp, timeout=tmo)
        got = sorted({ln.split()[2] for ln in out if ln.startswith("finding ")})
        ok = code == want_code and got == sorted(want_ids)
        note = "exit want=%d got=%d ids want=%s got=%s" % (want_code, code, sorted(want_ids), got)
        if ok and extra is not None:
            ok, why = extra(out)
            note += " " + why
        results.append((name, ok, note + " | " + clip(" // ".join(l for l in out if l.startswith("claim ")), 160)))
        return out

    # 1 good claim; counter exits 1 (red at base) and that is not a failure
    case("1-good-claim-red-counter-exit1", [claim(cmd="echo 'T fixed=0 exit=1'; exit 1")], 0, [],
         extra=lambda o: ("verdict=ok" in "\n".join(o) and "base_ok=1 exit=0" in o[-1], "verdict=ok"))

    # 2 round-44 defect shape against the real base README (copy of that one file)
    data, src = locate_readme(base_arg)
    if data is None:
        results.append(("2-round44-frozen-grep-real-readme", False, "real base README not found"))
    else:
        n = admitted_rows(data)
        b = mkbase({"corpus/README.md": data})
        frozen = "cd {tree} && grep -cE '^\\| F[0-9]+ \\| admitted \\|' corpus/README.md"
        case("2-round44-frozen-grep-real-readme",
             [claim(cmd=frozen, eb=str(n), ea=str(n + 1))], 1, ["FC-NO-MATCH"], base=b,
             extra=lambda o, n=n, src=src: ("base_read=0 verdict=FAIL" in "\n".join(o),
                                              "table-aware admitted=%d, frozen grep read 0 (readme %s)" % (n, src)))

    # 3 do-nothing green: counter prints only the after line at base
    case("3-do-nothing-green-only-after-line",
         [claim(cmd="echo 'T fixed=1 exit=0'")], 1, ["FC-AFTER-AT-BASE", "FC-NO-MATCH"])
    # 3b counter prints both lines at base
    case("3b-after-line-present-beside-before-line",
         [claim(cmd="echo 'T fixed=0 exit=1'; echo 'T fixed=1 exit=0'")], 1, ["FC-AFTER-AT-BASE"])

    # 4 missing / empty expect fields and counter_cmd
    case("4-missing-expect_before", [claim(eb=None)], 1, ["FC-MISSING-FIELD"])
    case("4b-empty-expect_before", [claim(eb="  ")], 1, ["FC-MISSING-FIELD"])
    case("4c-missing-expect_after", [claim(ea=None)], 1, ["FC-MISSING-FIELD"])
    case("4d-missing-counter_cmd", [claim(cmd=None)], 1, ["FC-MISSING-FIELD"])

    # 5 crashing counter, no matching line
    case("5-counter-crash-no-matching-line",
         [claim(cmd="python3 -c \"raise RuntimeError('boom')\"")], 1, ["FC-NO-MATCH"],
         extra=lambda o: ("base_read=RuntimeError: boom" in "\n".join(o), "base_read=last line"))

    # 6 token only as a substring (R41): suffix and prefix
    case("6-substring-suffix-fixed=0x",
         [claim(cmd="echo 'fixed=0x'", eb="fixed=0", ea="fixed=1")], 1, ["FC-NO-MATCH"])
    case("6b-substring-prefix-xfixed=0",
         [claim(cmd="echo 'xfixed=0'", eb="fixed=0", ea="fixed=1")], 1, ["FC-NO-MATCH"])

    # 7 expect_before == expect_after (the claim can never be told apart before/after)
    case("7-before-equals-after", [claim(cmd="echo 'T 0'", eb="T 0", ea="T 0")], 1,
         ["FC-AFTER-AT-BASE", "FC-BEFORE-EQ-AFTER"])

    # 8 hung counter -> timeout kills the process group
    case("8-counter-timeout", [claim(cmd="sleep 30")], 1, ["FC-TIMEOUT"], tmo=1)

    # 9 duplicate id
    case("9-duplicate-claim-id", [claim("C1"), claim("C1")], 1, ["FC-DUP-ID"])

    # 10 counter ignores the tree: a counter that cannot read the base proves nothing about it
    case("10-counter-reads-no-tree-placeholder",
         [claim(cmd="echo 'T fixed=0 exit=1'", raw=True)], 1, ["FC-NO-TREE"])

    # 11 wrong schema / no claims
    case("11-wrong-schema", [claim()], 1, ["FC-SCHEMA"], schema="kasegi-round-claims-v1")
    case("11b-no-claims", [], 1, ["FC-NO-CLAIMS"])

    # 12 counter mutates the base tree
    case("12-counter-mutates-base",
         [claim(cmd="touch {tree}/new.txt; echo 'T fixed=0 exit=1'")], 1, ["FC-BASE-MUTATED"])

    # 13 env contract: R45_FREEZE_CHECK=1, TMPDIR is the one passed in, cwd=tool-root, {tree} substituted
    exp_tmp = os.path.join(root, "tmp")
    b13 = mkbase()
    case("13-env-tmpdir-cwd-contract",
         [claim(cmd="echo \"env=$R45_FREEZE_CHECK tmp=$TMPDIR cwd=$(pwd) tree={tree}\"",
                eb="env=1 tmp=%s cwd=%s tree=%s" % (exp_tmp, tool_root, b13))], 0, [], base=b13)

    # 14 mixed file: one ok, one FAIL -> base_ok=1 of 2, exit 1
    case("14-mixed-ok-and-fail",
         [claim("A", cmd="echo 'T fixed=0 exit=1'; : {tree}"), claim("B", cmd="echo 'nope'; : {tree}")], 1,
         ["FC-NO-MATCH"], extra=lambda o: ("claims=2 base_ok=1 exit=1" == o[-1].replace("freeze-check ", ""), "claims=2 base_ok=1"))

    failures = 0
    lines = []
    for name, ok, note in results:
        lines.append("case %s %s %s" % (name, "PASS" if ok else "FAIL", note))
        failures += 0 if ok else 1
    lines.append("selftest cases=%d failures=%d" % (len(results), failures))
    shutil.rmtree(root, ignore_errors=True)
    return lines, failures


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--claims")
    ap.add_argument("--tool-root")
    ap.add_argument("--base")
    ap.add_argument("--work")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        lines, failures = selftest(a.work, a.base, a.timeout)
        print("\n".join(lines))
        return 1 if failures else 0
    if not (a.claims and a.tool_root and a.base):
        ap.error("--claims, --tool-root and --base are required (or use --selftest)")
    lines, code, _ = check(a.claims, a.tool_root, a.base, a.work, a.timeout)
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
