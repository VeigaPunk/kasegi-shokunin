#!/usr/bin/env python3
"""Independent R67 review: real native pipelines and real gates, never a gate emulator.

Usage: python3 -B review.py --base ABS --candidate ABS --work ABS --out ABS
Writes fixtures only under --work; removes that tree in finally. Durable ledgers,
raw FIG output, native statuses, source comparison, and selftest output go to --out.
The main cases are reviewer-derived, not imported from the seat probe battery.
P1..P8 separately reproduce the exact r66 driver fixture and shape definitions.
"""
import argparse
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def native(stages, root, env, input_name=None, untruncated=False):
    procs, previous, files = [], None, []
    try:
        selected = stages[:1] if untruncated else stages
        for idx, argv in enumerate(selected):
            stdin = previous if previous is not None else subprocess.DEVNULL
            if idx == 0 and input_name:
                stdin = (root / input_name).open("rb")
                files.append(stdin)
            p = subprocess.Popen(argv, cwd=root, env=env, stdin=stdin,
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            procs.append(p)
            if previous is not None:
                previous.close()
            previous = p.stdout
        raw, _ = procs[-1].communicate(timeout=180)
        for p in procs[:-1]:
            p.wait(timeout=180)
        return [p.returncode for p in procs], raw.decode("utf-8", "replace")
    finally:
        for p in procs:
            if p.poll() is None:
                p.kill()
            p.wait()
            if p.stdout is not None:
                p.stdout.close()
        for f in files:
            f.close()


def source_units(path):
    source = path.read_text()
    tree = ast.parse(source)
    units = {}
    for node in tree.body:
        key = None
        if isinstance(node, ast.FunctionDef):
            key = node.name
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            key = "VAR:" + node.targets[0].id
        if key:
            units[key] = {"source": ast.get_source_segment(source, node),
                          "start": node.lineno, "end": node.end_lineno}
    return source, units


def main():
    ap = argparse.ArgumentParser()
    for name in ("base", "candidate", "work", "out"):
        ap.add_argument("--" + name, required=True)
    args = ap.parse_args()
    base, candidate, work, out = [Path(getattr(args, n)).resolve()
                                for n in ("base", "candidate", "work", "out")]
    allowed = Path("/fast/scratch/hyaku/kasegi-r67/ReviewMultiHead")
    if not work.is_relative_to(allowed) or work == allowed or work.exists():
        raise ValueError("work must be a new child of reviewer scratch")
    out.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True)
    env = dict(os.environ, TMPDIR=str(work / "tmp"), HYAKU_SCRATCH=str(work / "selftest"),
               PYTHONDONTWRITEBYTECODE="1")
    for name in ("tmp", "selftest"):
        (work / name).mkdir()
    hashes_before = {"base": digest(base.read_bytes()), "candidate": digest(candidate.read_bytes())}
    try:
        fx, small, r66, r66small = [work / n for n in ("fx", "small", "r66-big", "r66-small")]
        for root in (fx, small, r66, r66small):
            root.mkdir()
        # Exactly 4096 * 1024 + prefix bytes, thus genuinely >= 4 MiB.
        bodies = {"big.txt": "alpha\n" + ("x" * 1023 + "\n") * 4096,
                  "other.txt": "beta\n" + ("y" * 1023 + "\n") * 4096,
                  "xlines.txt": "xline\n" + ("x" * 1023 + "\n") * 4096}
        for name, body in bodies.items():
            (fx / name).write_text(body)
            assert (fx / name).stat().st_size >= 4 * 1024 * 1024
        (fx / "--").write_text(bodies["big.txt"])
        (fx / "g.txt").write_text("35\n")
        (fx / "list0").write_bytes(b"big.txt\0missing.txt\0")
        (fx / "many").mkdir()
        for n in range(20000):
            (fx / "many" / ("f%05d" % n)).touch()
        (fx / "check").mkdir()
        tiny_hash = digest(b"a")
        for n in range(32):
            (fx / "check" / ("c%05d" % n)).write_bytes(b"a")
        # First checked data file and the checksum-list operand both exceed 4 MiB.
        lines = [digest((fx / "big.txt").read_bytes()) + "  big.txt"]
        lines += [tiny_hash + "  check/c%05d" % (n % 32) for n in range(60000)]
        lines += [tiny_hash + "  check/missing.txt"]
        (fx / "biglist").write_text("\n".join(lines) + "\n")
        assert (fx / "biglist").stat().st_size >= 4 * 1024 * 1024
        for root in (small, r66small):
            (root / "big.txt").write_text("alpha\n")
            (root / "other.txt").write_text("beta\n")
        # Exact r66 frozen driver fixtures, including file literally named '--'.
        r66body = "alpha\n" + ("x" * 63 + "\n") * 66000
        for name in ("big.txt", "--"):
            (r66 / name).write_text(r66body)
        (r66 / "other.txt").write_text("beta\n")
        manifest = {}
        for root, names in ((fx, ["big.txt", "other.txt", "xlines.txt", "list0", "biglist"]),
                            (r66, ["big.txt", "--", "other.txt"]),
                            (r66small, ["big.txt", "other.txt"])):
            for name in names:
                data = (root / name).read_bytes()
                manifest[str((root / name).relative_to(work))] = {
                    "bytes": len(data), "newlines": data.count(b"\n"), "sha256": digest(data)}
        manifest["input_lists"] = {
            "list0": ["big.txt", "missing.txt"],
            "biglist": {"entries": len(lines), "first": "big.txt", "last": "check/missing.txt",
                        "middle": "60000 repetitions over 32 one-byte files"}}
        save_json(out / "fixtures.json", manifest)

        bs, bu = source_units(base)
        cs, cu = source_units(candidate)
        changed = {k: {"base_lines": [bu[k]["start"], bu[k]["end"]] if k in bu else None,
                       "candidate_lines": [cu[k]["start"], cu[k]["end"]] if k in cu else None}
                   for k in bu.keys() | cu.keys()
                   if k not in bu or k not in cu or bu[k]["source"] != cu[k]["source"]}
        same = [k for k in bu.keys() & cu.keys() if bu[k]["source"] == cu[k]["source"]]
        save_json(out / "source-comparison.json", {
            "hashes": hashes_before, "changed_units": changed, "unchanged_units": sorted(same),
            "cat_function_sha256": digest(cu["cat_sigpipe_exempt"]["source"].encode()),
            "candidate_units": {k: [v["start"], v["end"]] for k, v in cu.items()}})
        (out / "candidate.diff").write_text("".join(difflib.unified_diff(
            bs.splitlines(True), cs.splitlines(True), fromfile=str(base), tofile=str(candidate))))
        (out / "candidate-reviewed.py").write_bytes(candidate.read_bytes())

        cases = []
        def add(cid, producer, root=fx, stdin=None, want=None):
            argv = shlex.split(producer)
            derive = producer + (" < " + shlex.quote(stdin) if stdin else "") + " | head -n 1"
            cases.append((cid, root, derive, [argv, ["head", "-n", "1"]], stdin, want))
        for cid, producer, stdin in [
            ("cut0", "cut -f1 -d:", "big.txt"),
            ("cut1", "cut -f1 -d: big.txt", None),
            ("cut2", "cut -f1 -d: big.txt missing.txt", None),
            ("cut3", "cut -f1 -d: big.txt other.txt missing.txt", None),
            ("cut1detached", "cut -d : -f 1 big.txt", None),
            ("wc0", "wc -l", "big.txt"), ("wc1", "wc -l big.txt", None),
            ("wc2", "wc -l big.txt missing.txt", None),
            ("grep0", "grep x", "xlines.txt"), ("grep1", "grep x xlines.txt", None),
            ("grep2", "grep x xlines.txt missing.txt", None),
            ("grep3", "grep x xlines.txt other.txt missing.txt", None),
            ("grep_e_sep1", "grep -e x big.txt", None),
            ("grep_i_sep1", "grep -i x big.txt", None),
            ("grep_ex_attached2", "grep -ex big.txt missing.txt", None),
            ("grep_f_attached2", "grep -fbig.txt big.txt missing.txt", None),
            ("grep_e_sep2", "grep -e x big.txt missing.txt", None),
            ("grep_ee2", "grep -e x -e y big.txt missing.txt", None),
            ("grep_c1", "grep -c x big.txt", None),
            ("sort0", "sort", "big.txt"), ("sort1", "sort big.txt", None),
            ("sort2existing", "sort big.txt other.txt", None),
            ("sort2missing", "sort big.txt missing.txt", None),
            ("sort1detached", "sort -k 1 big.txt", None),
            ("head0attached", "head -c10000000", "big.txt"),
            ("head0detached", "head -c 10000000", "big.txt"),
            ("head1attached", "head -c10000000 big.txt", None),
            ("head1detached", "head -c 10000000 big.txt", None),
            ("head2bytes", "head -c10000000 big.txt missing.txt", None),
            ("head2lines", "head -n 5 big.txt missing.txt", None),
            ("tail0attached", "tail -c100000", "big.txt"),
            ("tail1attached", "tail -c100000 big.txt", None),
            ("tail1detached", "tail -c 100000 big.txt", None),
            ("tail2", "tail -c100000 big.txt missing.txt", None),
            ("sha0", "sha256sum", "big.txt"),
            ("sha1", "sha256sum big.txt", None),
            ("sha2", "sha256sum big.txt missing.txt", None),
            ("sha2existing", "sha256sum big.txt other.txt", None),
            ("tr0", "tr -d", "big.txt"),
            ("tr1", "tr -d y", "big.txt"),
            ("tr2", "tr a b", "big.txt"),
            ("ls1", "ls -l many", None), ("ls2", "ls -l many missing.txt", None),
            ("cat0", "cat", "big.txt"), ("cat1", "cat big.txt", None),
            ("cat2", "cat big.txt missing.txt", None),
            ("cat3", "cat big.txt other.txt missing.txt", None),
            ("cat1opt", "cat -n big.txt", None),
            ("catdashdash", "cat -- big.txt missing.txt", None),
            ("wc_files0", "wc -l --files0-from=list0", None),
            ("sha_check", "sha256sum -c biglist", None),
            ("sha_check_attached_setup", "sha256sum --check=biglist", None),
            ("sort_files0", "sort --files0-from=list0", None),
        ]:
            add(cid, producer, stdin=stdin)
        add("ls0", "ls -l", root=fx / "many")
        for cid, root, producer, inp, want in [
            ("R66-P1", r66, "cat big.txt missing.txt", None, "alpha"),
            ("R66-P2", r66, "cat big.txt other.txt", None, "alpha"),
            ("R66-P3", r66, "cat big.txt", None, "alpha"),
            ("R66-P4", r66, "cat", "big.txt", "alpha"),
            ("R66-P7", r66small, "cat big.txt other.txt", None, "alpha"),
            ("R66-P8", r66, "cat -- -- missing.txt", None, "alpha"),
        ]:
            add(cid, producer, root=root, stdin=inp, want=want)
        for cid, producer in (("R66-P5", ["cat", "missing.txt"]),
                              ("R66-P6", ["grep", "absent", "big.txt"])):
            cases.append((cid, r66, shlex.join(producer) + " | wc -l",
                          [producer, ["wc", "-l"]], None, "0"))

        results = []
        for cid, root, derive, stages, input_name, frozen_want in cases:
            statuses, text = native(stages, root, env, input_name)
            first = text.splitlines()[0].strip() if text else ""
            want = first if frozen_want is None else frozen_want
            full_status, _ = native(stages, root, env, input_name, untruncated=True)
            ledger = {"figures": [{"id": cid, "record": "review-fixture:1", "recorded": want,
                                    "derive": derive, "want": want}]}
            lp = out / "ledgers" / (cid + ".json")
            save_json(lp, ledger)
            row = {"id": cid, "root": str(root), "derive": derive,
                   "native_statuses": statuses, "untruncated_stage0": full_status[0],
                   "native_stdout": text, "want": want, "gates": {}}
            for label, gate in (("base", base), ("candidate", candidate)):
                p = subprocess.run([sys.executable, "-B", str(gate), "--ledger", str(lp),
                                    "--root", str(root)], cwd=work, env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
                stdout, stderr = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
                row["gates"][label] = {"exit": p.returncode, "stdout": stdout, "stderr": stderr}
                dest = out / label
                dest.mkdir(exist_ok=True)
                (dest / (cid + ".stdout")).write_text(stdout)
                (dest / (cid + ".stderr")).write_text(stderr)
            results.append(row)
        save_json(out / "results.json", results)
        summary = []
        for row in results:
            for label in ("base", "candidate"):
                p = row["gates"][label]
                fig = next((l for l in p["stdout"].splitlines() if l.startswith("FIG ")), "NO-FIG")
                verdict = "ok" if fig.endswith(" ok") else ("stale" if fig.endswith(" stale") else "SETUP")
                reason = fig.split("reason=")[1].split()[0] if "reason=" in fig else "-"
                summary.append("%s native=%s full=%s %s rc=%s verdict=%s reason=%s" %
                               (row["id"], row["native_statuses"], row["untruncated_stage0"],
                                label, p["exit"], verdict, reason))
        (out / "summary.txt").write_text("\n".join(summary) + "\n")

        repeats = []
        for cid in ("wc2", "wc_files0", "sha_check"):
            case = next(c for c in cases if c[0] == cid)
            _, root, derive, stages, inp, _ = case
            native_results = [native(stages, root, env, inp)[0] for _ in range(6)]
            repeats.append({"id": cid, "native_statuses": native_results})
        save_json(out / "native-repeats.json", repeats)
        p = subprocess.run([sys.executable, "-B", str(candidate), "--selftest"], cwd=work,
                           env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        (out / "selftest.stdout").write_bytes(p.stdout)
        (out / "selftest.stderr").write_bytes(p.stderr)
        versions = {name: subprocess.run([name, "--version"], cwd=work, env=env,
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
                    for name in ("head", "cut", "wc", "grep", "sort", "tail", "sha256sum", "tr", "ls", "cat")}
        save_json(out / "versions.json", versions)
        hashes_after = {"base": digest(base.read_bytes()), "candidate": digest(candidate.read_bytes())}
        save_json(out / "run.json", {"hashes_before": hashes_before, "hashes_after": hashes_after,
                                     "stable": hashes_before == hashes_after, "cases": len(results),
                                     "selftest_exit": p.returncode,
                                     "selftest_summary": p.stdout.decode().splitlines()[-1],
                                     "all_selftest_children_cleaned": not any((work / "selftest").iterdir()),
                                     "setup_note": "--check=FILE is an unsupported uutils form, not a killed mutant"})
        print("REVIEW cases=%s selftest_exit=%s stable=%s out=%s" %
              (len(results), p.returncode, hashes_before == hashes_after, out))
    finally:
        shutil.rmtree(work)


if __name__ == "__main__":
    main()
