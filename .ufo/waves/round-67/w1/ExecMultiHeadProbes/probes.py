#!/usr/bin/env python3
"""kasegi round-67 multi-head SIGPIPE probe harness (seat ExecMultiHeadProbes).

Drives the REAL production gate (corpus/instruments/figure-audit.py, never a
reimplementation) over committed-shape single-figure JSON ledgers, one ledger per
probe, and reports per probe the gate's exit code plus an independently measured
native per-stage returncode vector (subprocess, no shell).

Frozen expectation matrices are derived from the production gate source at base
revision 8e2a8fe8eb92d7c824902a4b70aab027a9aacee0 (gate sha256
51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac), cross-checked
against L1's committed receipts controls/donothing-multihead-r67.txt and
controls/base-matrix-r67.txt, and confirmed by L1 (KasegiR67) 2026-11-04:

  base      P1,P2 stale derive-upstream-signal-13 (R66 cat repair is IN the base;
            the wave payload's "P1/P2 base rc0" text predates it), P5 stale
            derive-exit-1, P15 stale derive-upstream-exit-1, every other shape ok,
            P10 flaky (native stage0 races 1 vs -13).
  candidate P9,P11 join P1,P2 as stale derive-upstream-signal-13 (the frozen
            repairs: cut and grep multi-input SIGPIPE must refuse), P10 stale
            under both outcomes (reason not frozen), every other row keeps its
            base verdict, P8 stays rc0 in BOTH modes.

Deviations from the original wave payload, kept as reported (L1-owned, measured):
  PAYLOAD-DEV base      P1,P2: payload rc0 -> frozen rc1/derive-upstream-signal-13.
  PAYLOAD-DEV candidate P8:   payload rc1/derive-upstream-signal-13 -> frozen rc0
        (grep -c alpha big.txt emits one 2-byte write at EOF; native stage0 [0,0]
        on this host; the per-head rule fires only on -13, so no candidate can
        derive signal-13 for P8).

P18 `grep x big.txt | head -n 1` is a POSITIVE CONTROL (L1 ruling), expected rc0
in both modes: base exempts its SIGPIPE (head-blind benign rule) and the candidate
exempts it too (grep with exactly one input operand), proving the repaired rule
discriminates on operand count, not head name. It is never counted as a repair.

Output grammar (bound by ExecMultiHeadDriver):
  NATIVE <name> stage0=<n> stage1=<n|->              (per probe; P10 = repeat 1)
  PROBE <name> rc=<n> expected=<rc|-> reason=<reason|-> pass=<true|false>
  PROBES probes=20 failures=F mode=<base|candidate> instrument_sha256=<sha>
Non-contract extras: RUN/INSTRUMENT-SHA256/FIXTURE header lines, GATEFIG raw gate
lines, P10REPEAT lines, PAYLOAD-DEV notes, CONTROL-WEAK notes, and one
CONTROL CUTDASH ... line (the no-`--` differential control, outside probes=).
Exit: 0 iff failures=0 AND the CUTDASH control passes; 1 otherwise; 2 setup/harness
error (missing instrument, fixture digest mismatch, occupied work dir). A
setup-failed run is a failed setup, never a verdict.

Shared table for the mutation battery: probe_table(root, mode="candidate") returns
[(id, derive, ("ok", want) | ("stale", reason)), ...].  Faces are the frozen primary
verdicts; P10/P19/P20 are conditional rows whose real acceptance is reason any-of
(P10_REASON_SET / P1920_REASON_SET) — the battery must not treat those reasons as exact.

Scratch: everything is written under --work (pass it explicitly; TMPDIR for gate
children is set to <work>/tmp). Fixtures are byte-pinned:
  big.txt   sha256 3ed4e02bd97495bce0703d0f0def4174cc5458ce14875807646c14709709766c
  other.txt sha256 0c5c9015ad84de5f05d27c12726ed78175f4a9896697c932ca2abc9c1df7c28e
  xlines.txt sha256 83d10921e04da595d825e6e37aee5b31dffd9dd4763100fb2a816bdbdccf4749
missing.txt must be absent.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

EXPECTED_CASES = 20
P10_REASON_SET = ("derive-upstream-exit-1", "derive-upstream-signal-13")
# P19/P20 candidate acceptance: the repair must refuse under any of these faces (SIGPIPE
# refusal, or the stage reaching the absent operand: cut exits 1, grep exits 2).
P1920_REASON_SET = ("derive-upstream-signal-13", "derive-upstream-exit-1", "derive-upstream-exit-2")
P10_REPEATS = 5
BASE_REVISION = "8e2a8fe8eb92d7c824902a4b70aab027a9aacee0"
BASE_GATE_SHA256 = "51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac"
FIXTURE_PINS = {
    "big.txt": ("3ed4e02bd97495bce0703d0f0def4174cc5458ce14875807646c14709709766c", 4193286),
    "other.txt": ("0c5c9015ad84de5f05d27c12726ed78175f4a9896697c932ca2abc9c1df7c28e", 4193285),
    "xlines.txt": ("83d10921e04da595d825e6e37aee5b31dffd9dd4763100fb2a816bdbdccf4749", 400000),
}

# name -> (derive string, stages [(argv, stdin-file-or-None)], want or None to capture)
PROBES = {
    "P1": ("cat big.txt missing.txt | head -n 1",
           [(["cat", "big.txt", "missing.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P2": ("cat big.txt other.txt | head -n 1",
           [(["cat", "big.txt", "other.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P3": ("cat big.txt | head -n 1",
           [(["cat", "big.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P4": ("cat < big.txt | head -n 1",
           [(["cat"], "big.txt"), (["head", "-n", "1"], None)], "alpha"),
    "P5": ("cat missing.txt", [(["cat", "missing.txt"], None)], "alpha"),
    "P6": ("head -n 5 big.txt | head -n 1",
           [(["head", "-n", "5", "big.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P7": ("wc -l < big.txt | head -n 1",
           [(["wc", "-l"], "big.txt"), (["head", "-n", "1"], None)], "4096"),
    "P8": ("grep -c alpha big.txt | head -n 1",
           [(["grep", "-c", "alpha", "big.txt"], None), (["head", "-n", "1"], None)], "1"),
    "P9": ("cut -f1 -d: big.txt missing.txt | head -n 1",
           [(["cut", "-f1", "-d:", "big.txt", "missing.txt"], None), (["head", "-n", "1"], None)],
           "alpha"),
    "P10": ("wc -l big.txt missing.txt | head -n 1",
            [(["wc", "-l", "big.txt", "missing.txt"], None), (["head", "-n", "1"], None)],
            "4096 big.txt"),
    "P11": ("grep x xlines.txt missing.txt | head -n 1",
            [(["grep", "x", "xlines.txt", "missing.txt"], None), (["head", "-n", "1"], None)],
            "xlines.txt:x"),
    "P12": ("cut -f1 -d: big.txt | head -n 1",
            [(["cut", "-f1", "-d:", "big.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P13": ("wc -l big.txt | head -n 1",
            [(["wc", "-l", "big.txt"], None), (["head", "-n", "1"], None)], "4096 big.txt"),
    "P14": ("sha256sum big.txt | head -n 1",
            [(["sha256sum", "big.txt"], None), (["head", "-n", "1"], None)], None),
    "P15": ("head -n 5 big.txt missing.txt | head -n 1",
            [(["head", "-n", "5", "big.txt", "missing.txt"], None), (["head", "-n", "1"], None)],
            "alpha"),
    "P16": ("sort big.txt | head -n 1",
            [(["sort", "big.txt"], None), (["head", "-n", "1"], None)], "alpha"),
    "P17": ("ls big.txt | head -n 1",
            [(["ls", "big.txt"], None), (["head", "-n", "1"], None)], "big.txt"),
    "P18": ("grep x big.txt | head -n 1",
            [(["grep", "x", "big.txt"], None), (["head", "-n", "1"], None)], "x" * 1023),
    # P19/P20 (L1, from CriticMultiHead finding 1): a MID-ARGV "--" spelling makes the
    # following dash-token a file operand, which the frozen leading-only "--" handling
    # miscounts as an option — the masked multi-input shape survives.  Repair rows:
    # base masked green; candidate stale with any reason in P1920_REASON_SET.
    "P19": ("cut -f1 -d: big.txt -- -missing.txt | head -n 1",
            [(["cut", "-f1", "-d:", "big.txt", "--", "-missing.txt"], None),
             (["head", "-n", "1"], None)], "alpha"),
    "P20": ("grep x xlines.txt -- -missing.txt | head -n 1",
            [(["grep", "x", "xlines.txt", "--", "-missing.txt"], None),
             (["head", "-n", "1"], None)], "xlines.txt:x"),
}
# Differential control (never a repair, never counted in probes=): without the "--",
# cut rejects the dash-token as an unknown OPTION (stage0 exit 1), proving the token
# in P19 is a file operand only because of the separator.
CONTROL_CUTDASH = ("cut -f1 -d: big.txt -missing.txt | head -n 1",
                   [(["cut", "-f1", "-d:", "big.txt", "-missing.txt"], None),
                    (["head", "-n", "1"], None)])
PROBE_ORDER = tuple("P%d" % i for i in range(1, EXPECTED_CASES + 1))

# (expected gate rc, expected derive reason or None)
EXPECTED = {
    "base": {
        "P1": (1, "derive-upstream-signal-13"), "P2": (1, "derive-upstream-signal-13"),
        "P3": (0, None), "P4": (0, None), "P5": (1, "derive-exit-1"), "P6": (0, None),
        "P7": (0, None), "P8": (0, None), "P9": (0, None), "P11": (0, None),
        "P12": (0, None), "P13": (0, None), "P14": (0, None),
        "P15": (1, "derive-upstream-exit-1"), "P16": (0, None), "P17": (0, None),
        "P18": (0, None),  # positive control, never a repair
        "P19": (0, None), "P20": (0, None),  # masked green: mid-argv "--" shapes
    },
    "candidate": {
        "P1": (1, "derive-upstream-signal-13"), "P2": (1, "derive-upstream-signal-13"),
        "P3": (0, None), "P4": (0, None), "P5": (1, "derive-exit-1"), "P6": (0, None),
        "P7": (0, None), "P8": (0, None), "P9": (1, "derive-upstream-signal-13"),
        "P11": (1, "derive-upstream-signal-13"), "P12": (0, None), "P13": (0, None),
        "P14": (0, None), "P15": (1, "derive-upstream-exit-1"), "P16": (0, None),
        "P17": (0, None), "P18": (0, None),  # positive control, never a repair
        # P19/P20: repair rows (mid-argv "--" operand must be counted); stale under any
        # of P1920_REASON_SET, never a frozen single reason.
        "P19": (1, frozenset(P1920_REASON_SET)),
        "P20": (1, frozenset(P1920_REASON_SET)),
    },
}

PAYLOAD_DEV = {
    "base": (
        "PAYLOAD-DEV base P1,P2 payload=rc0 frozen=rc1/derive-upstream-signal-13 "
        "(R66 cat restriction is in the production base; controls/base-matrix-r67.txt)",
    ),
    "candidate": (
        "PAYLOAD-DEV candidate P8 payload=rc1/derive-upstream-signal-13 frozen=rc0 "
        "(grep -c writes once at EOF; native stage0 [0,0]; rule fires only on -13)",
    ),
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def setup_fail(msg):
    print("SETUP-FAIL %s" % msg)
    print("PROBES probes=0 failures=0 mode=setup-error instrument_sha256=-")
    return 2


def build_fixtures(work):
    for absent in ("missing.txt", "-missing.txt"):
        if os.path.exists(os.path.join(work, absent)):
            return "%s already exists in --work (fixtures must be the committed shape)" % absent
    fixtures = {
        "big.txt": b"alpha\n" + (b"x" * 1023 + b"\n") * 4095,
        "other.txt": b"beta\n" + (b"y" * 1023 + b"\n") * 4095,
        "xlines.txt": b"x\n" * 200000,
    }
    for name, blob in fixtures.items():
        with open(os.path.join(work, name), "wb") as f:
            f.write(blob)
    for name, blob in fixtures.items():
        digest, size = FIXTURE_PINS[name]
        real = sha256_file(os.path.join(work, name))
        if real != digest or os.path.getsize(os.path.join(work, name)) != size:
            return "fixture %s digest mismatch: got sha256=%s bytes=%d want sha256=%s bytes=%d" % (
                name, real, os.path.getsize(os.path.join(work, name)), digest, size)
        print("FIXTURE %s sha256=%s bytes=%d" % (name, real, size))
    print("FIXTURE missing.txt absent=true")
    print("FIXTURE -missing.txt absent=true (P19/P20 operand must stay absent)")
    return None


def capture_p14_want(work):
    p = subprocess.run(["sha256sum", "big.txt"], cwd=work, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=60)
    if p.returncode != 0:
        return "sha256sum big.txt failed rc=%d: %s" % (p.returncode, p.stderr.decode("utf-8", "replace"))
    want = p.stdout.decode("utf-8", "replace").splitlines()[0].strip()
    if not want:
        return "sha256sum big.txt printed nothing"
    return want


def native(stages, root):
    """Real per-stage returncodes of the same argv pipeline; no shell."""
    procs, opened, prev = [], [], None
    try:
        for argv, input_path in stages:
            if input_path is not None:
                f = open(os.path.join(root, input_path), "rb")
                opened.append(f)
                stdin = f
            elif prev is not None:
                stdin = prev
            else:
                stdin = subprocess.DEVNULL
            p = subprocess.Popen(argv, cwd=root, stdin=stdin, stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL)
            procs.append(p)
            if prev is not None:
                prev.close()
            prev = p.stdout
        procs[-1].communicate(timeout=90)
        for p in procs[:-1]:
            p.wait(timeout=90)
        return [p.returncode for p in procs]
    except subprocess.TimeoutExpired:
        for p in procs:
            if p.poll() is None:
                p.kill()
        for p in procs:
            p.wait()
        return None
    finally:
        for f in opened:
            f.close()
        for p in procs:
            if p.stdout is not None:
                p.stdout.close()


def gate_run(instrument, ledger_path, root, env):
    return subprocess.run([sys.executable, "-B", instrument, "--ledger", ledger_path,
                           "--root", root],
                          capture_output=True, text=True, timeout=120, cwd=root, env=env)


def parse_fig(stdout, fig_id):
    """Return (measured reason or None, raw FIG line or '')."""
    prefix = "FIG %s " % fig_id
    for line in stdout.splitlines():
        if line.startswith(prefix):
            if line.endswith(" ok"):
                return None, line
            m = re.search(r"reason=([A-Za-z0-9_-]+)", line)
            return (m.group(1) if m else None), line
    return "no-fig-line", ""


def run_one(name, probe, expected, instrument, work, env):
    """Returns True on pass. Prints NATIVE/GATEFIG/PROBE lines."""
    derive, stages, want = probe
    erc, ereason = expected
    ledger_path = os.path.join(work, "ledgers", "%s.json" % name)
    entry = {"id": name, "record": "ExecMultiHeadProbes/%s" % name,
             "recorded": want if want is not None else "<captured>", "derive": derive,
             "want": want}
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"figures": [entry]}, f)
        f.write("\n")

    nrc = native(stages, work)
    if nrc is None:
        print("NATIVE %s stage0=timeout stage1=timeout" % name)
        print("PROBE %s rc=- expected=%d reason=native-timeout pass=false" % (name, erc))
        return False
    print("NATIVE %s stage0=%d stage1=%s" % (name, nrc[0], str(nrc[1]) if len(nrc) > 1 else "-"))

    p = gate_run(instrument, ledger_path, work, env)
    mreason, figline = parse_fig(p.stdout, name)
    if figline:
        print("GATEFIG %s" % figline)
    if p.returncode == 2:
        print("GATE-SETUP-ERROR %s stderr=%s" % (name, p.stderr.strip().replace("\n", " | ")))

    ok = p.returncode == erc
    if erc == 0:
        ok = ok and mreason is None
    elif isinstance(ereason, str):
        ok = ok and mreason == ereason
    elif ereason is not None:
        ok = ok and mreason in ereason
    premise = True
    if ereason == "derive-upstream-signal-13":
        # A SIGPIPE-verdict expectation must really show -13 natively.  (Any-of sets —
        # P19/P20 — are face-conditional and get no hard native premise, like P10.)
        premise = nrc[0] == -13
        if not premise:
            print("NATIVE-MISMATCH %s expected-stage0=-13 got=%d" % (name, nrc[0]))
    print("PROBE %s rc=%d expected=%d reason=%s pass=%s"
          % (name, p.returncode, erc, mreason if mreason else "-", "true" if ok and premise else "false"))
    return ok and premise


def run_p10(probe, mode, instrument, work, env):
    """Flake probe: five repeats, native premise stage0 in {-13, 1}; base accepts
    rc0 or rc1 in the reason set per repeat; candidate requires rc1 in the set.
    No frozen single reason (dispatch-addendum-r67.md)."""
    derive, stages, want = probe
    ledger_path = os.path.join(work, "ledgers", "P10.json")
    entry = {"id": "P10", "record": "ExecMultiHeadProbes/P10", "recorded": want,
             "derive": derive, "want": want}
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"figures": [entry]}, f)
        f.write("\n")

    repeats = []
    for k in range(1, P10_REPEATS + 1):
        nrc = native(stages, work)
        if nrc is None:
            print("P10REPEAT %d stage0=timeout gate_rc=- reason=native-timeout" % k)
            repeats.append({"stage0": None, "gate_rc": None, "reason": "native-timeout", "ok": False})
            continue
        p = gate_run(instrument, ledger_path, work, env)
        mreason, figline = parse_fig(p.stdout, "P10")
        if figline and k == 1:
            print("GATEFIG %s" % figline)
        premise = nrc[0] in (-13, 1)
        if mode == "base":
            ok = premise and (p.returncode == 0 or
                              (p.returncode == 1 and mreason in P10_REASON_SET))
        else:
            ok = premise and p.returncode == 1 and mreason in P10_REASON_SET
        print("P10REPEAT %d stage0=%d gate_rc=%d reason=%s repeat_pass=%s"
              % (k, nrc[0], p.returncode, mreason if mreason else "-", "true" if ok else "false"))
        repeats.append({"stage0": nrc[0], "native": nrc, "gate_rc": p.returncode,
                        "reason": mreason, "ok": ok})

    first = repeats[0]
    print("NATIVE P10 stage0=%s stage1=%s"
          % (first["stage0"] if first["stage0"] is not None else "timeout",
             str(first["native"][1]) if first.get("native") and len(first["native"]) > 1 else "-"))
    exp = "-" if mode == "base" else "1"
    print("PROBE P10 rc=%s expected=%s reason=%s pass=%s repeats=%d"
          % (first["gate_rc"] if first["gate_rc"] is not None else "-",
             exp, first["reason"] if first["reason"] else "-",
             "true" if all(r["ok"] for r in repeats) else "false", P10_REPEATS))
    return all(r["ok"] for r in repeats)


def run_control(instrument, work, env):
    """Differential control (L1): the same dash-token WITHOUT the mid-argv `--` is an
    unknown OPTION to cut, so stage0 exits 1 immediately and the gate refuses the derive
    (derive-upstream-exit-1).  Proves the token in P19 is a file operand only because of
    the `--` separator.  Outside probes=; a control failure still fails the run."""
    derive, stages = CONTROL_CUTDASH
    ledger_path = os.path.join(work, "ledgers", "CUTDASH.json")
    entry = {"id": "CUTDASH", "record": "ExecMultiHeadProbes/CUTDASH", "recorded": "alpha",
             "derive": derive, "want": "alpha"}
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"figures": [entry]}, f)
        f.write("\n")
    nrc = native(stages, work)
    if nrc is None:
        print("CONTROL CUTDASH stage0=timeout gate_rc=- reason=native-timeout pass=false")
        return False
    p = gate_run(instrument, ledger_path, work, env)
    mreason, figline = parse_fig(p.stdout, "CUTDASH")
    if figline:
        print("GATEFIG %s" % figline)
    stage_ok = nrc[0] == 1
    gate_ok = p.returncode == 1 and mreason == "derive-upstream-exit-1"
    print("CONTROL CUTDASH stage0=%d gate_rc=%d reason=%s pass=%s"
          % (nrc[0], p.returncode, mreason if mreason else "-",
             "true" if stage_ok and gate_ok else "false"))
    if not stage_ok:
        print("CONTROL-FAIL CUTDASH native stage0=%d want=1 (without -- the dash-token "
              "must be an unknown option)" % nrc[0])
    if not gate_ok:
        print("CONTROL-FAIL CUTDASH gate rc=%d reason=%s want=rc1/derive-upstream-exit-1"
              % (p.returncode, mreason if mreason else "-"))
    return stage_ok and gate_ok


def _p14_want_lenient(root):
    """P14's want is host-shaped (sha256sum output padding); capture it, with a pinned
    digest fallback so probe_table stays usable without built fixtures."""
    try:
        p = subprocess.run(["sha256sum", "big.txt"], cwd=root, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL, timeout=60)
        if p.returncode == 0:
            line = p.stdout.decode("utf-8", "replace").splitlines()[0].strip()
            if line:
                return line
    except (OSError, subprocess.TimeoutExpired, IndexError):
        pass
    return FIXTURE_PINS["big.txt"][0] + "  big.txt"


def probe_table(root, mode="candidate"):
    """Shared probe table for multihead-mutbat.py's load_collector (ExecMultiHeadDriver
    request): [(id, derive, ("ok", want) | ("stale", reason)), ...].

    Faces are the frozen PRIMARY verdicts for the given mode.  Conditional rows are
    emitted at their primary face but their real acceptance is reason any-of:
      P10      base green/stale flake (candidate: stale any of P10_REASON_SET);
      P19/P20  candidate stale any of P1920_REASON_SET.
    The battery must not treat those three reasons as exact-match requirements.
    """
    if mode not in EXPECTED:
        raise ValueError("mode must be base or candidate")
    faces = EXPECTED[mode]
    table = []
    for name in PROBE_ORDER:
        derive = PROBES[name][0]
        if name == "P10":
            # No EXPECTED row: handled specially in run_p10.  Primary face here:
            # candidate stale (signal-13); base dominant face is green.
            if mode == "base":
                table.append((name, derive, ("ok", PROBES[name][2])))
            else:
                table.append((name, derive, ("stale", "derive-upstream-signal-13")))
            continue
        erc, ereason = faces[name]
        if erc == 0:
            want = PROBES[name][2]
            table.append((name, derive, ("ok", want if want is not None else _p14_want_lenient(root))))
        else:
            reason = ereason if isinstance(ereason, str) else "derive-upstream-signal-13"
            table.append((name, derive, ("stale", reason)))
    return table


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--instrument", required=True, help="path to the REAL gate to drive")
    ap.add_argument("--work", required=True, help="fixture/work directory (created)")
    ap.add_argument("--mode", required=True, choices=("base", "candidate"))
    args = ap.parse_args(argv)

    if not os.path.isfile(args.instrument):
        return setup_fail("instrument not found: %s" % args.instrument)
    instrument = os.path.abspath(args.instrument)
    instrument_sha = sha256_file(instrument)
    work = os.path.abspath(args.work)
    os.makedirs(os.path.join(work, "ledgers"), exist_ok=True)
    tmpdir = os.path.join(work, "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = tmpdir  # never rely on an inherited TMPDIR, for gate children either

    print("RUN mode=%s instrument=%s work=%s" % (args.mode, instrument, work))
    print("INSTRUMENT-SHA256 %s" % instrument_sha)
    if instrument_sha == BASE_GATE_SHA256:
        print("INSTRUMENT-IDENTITY production-base-gate base-revision=%s" % BASE_REVISION)
    print("BASE-REVISION-UNDER-TEST %s (binding pin is INSTRUMENT-SHA256; revision informational)" % BASE_REVISION)

    err = build_fixtures(work)
    if err:
        return setup_fail(err)
    want14 = capture_p14_want(work)
    if want14.startswith("sha256sum"):
        return setup_fail(want14)
    print("FIXTURE p14-want-from-host=%s" % want14)
    probes = dict(PROBES)
    probes["P14"] = (PROBES["P14"][0], PROBES["P14"][1], want14)
    for note in PAYLOAD_DEV[args.mode]:
        print(note)
    print("NOTE P18 is a positive control (expected rc0 in both modes), never a repair")
    print("NOTE P10 is the flake probe: %d repeats, native premise stage0 in {-13,1}, "
          "no frozen reason (controls/dispatch-addendum-r67.md)" % P10_REPEATS)
    print("NOTE P19/P20 are repair rows (mid-argv '--' operand); base masked green, "
          "candidate stale any of %s" % ",".join(P1920_REASON_SET))
    print("NOTE CUTDASH is the no-'--' differential control (stage0 exit 1 proves the "
          "token is an option without the separator); outside probes=, failure fails the run")

    failures = 0
    for name in PROBE_ORDER:
        if name == "P10":
            if not run_p10(probes[name], args.mode, instrument, work, env):
                failures += 1
            continue
        if not run_one(name, probes[name], EXPECTED[args.mode][name], instrument, work, env):
            failures += 1
        if name == "P18":
            nrc = native(probes[name][1], work)
            if nrc is not None and nrc[0] != -13:
                print("CONTROL-WEAK P18 positive-control native stage0=%d (wanted -13 so the "
                      "control actually exercises the exemption)" % nrc[0])
    control_ok = run_control(instrument, work, env)

    print("PROBES probes=%d failures=%d mode=%s instrument_sha256=%s"
          % (EXPECTED_CASES, failures, args.mode, instrument_sha))
    if not control_ok:
        print("RUN-FAIL reason=cutdash-control-failed (probes/failures counts above are "
              "unaffected; the control is an assertion outside the probe set)")
    return 0 if failures == 0 and control_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
