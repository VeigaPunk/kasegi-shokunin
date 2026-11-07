#!/usr/bin/env python3
"""Round-99 C1 mutation probe driver (scratch only).

The frozen tamper harness scores 12/12 against the landing instrument; this
driver asks, for each single-point mutant the harness does NOT isolate, whether
a concrete wrong census/measurement is accepted.  Every probe runs the pristine
landing instrument and the mutant on the same bytes and prints both outcomes.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kasegi-r99/MutC1Tamper"
CLONE = os.path.join(S, "clone")
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
INST = os.path.join(S, "instrument-landing.py")
MUT = {i: os.path.join(S, "mutants", "m%s.py" % i) for i in
       ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")}
A = "a3db47e71fe292c03b00ba11f38cccbec45d3966"
B = "b9411a6b530e486180cf14c72fccc46668dcf5ee"
SEP = "\n---\n\n"
BASE = open(os.path.join(S, "work/baseline/pristine.md"), encoding="utf-8").read()
COMMITTED = os.path.join(S, "committed-census.md")

spec = importlib.util.spec_from_file_location("census_inst", INST)
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def split(text):
    i = text.find(SEP)
    return text[:i], text[i + len(SEP):]


OH, OB = split(BASE)
OL = OH.split("\n")
assert OL[4].startswith("measured-at: ") and OL[8].startswith("host-owned inputs: "), OL[4:9]
H5 = OL[4:9]
HSHA = OL[9].split(": ", 1)[1]
BSHA = OL[10].split(": ", 1)[1]


def build(h5, body, hsha=None, bsha=None):
    hs = hsha if hsha is not None else sha("\n".join(h5))
    bs = bsha if bsha is not None else sha(body)
    head = OL[:4] + list(h5) + ["header-sha256: " + hs, "body-sha256: " + bs]
    return "\n".join(head) + SEP + body


def env_for(work):
    env = dict(os.environ)
    env["HOME"] = os.path.join(work, "home")
    os.makedirs(os.path.join(env["HOME"], "Projects"), exist_ok=True)
    return env


def run(cmd, work, clear=True):
    if clear:
        shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    p = subprocess.run(cmd, capture_output=True, text=True, env=env_for(work))
    return p.returncode, (p.stdout + p.stderr).strip()


def check(inst, path, work, lane=CLONE, clear=True):
    return run([sys.executable, "-B", inst, "--lane", lane, "--check", path,
                "--work", work], work, clear)


def revrun(inst, rev, work):
    return run([sys.executable, "-B", inst, "--lane", CLONE, "--rev", rev,
                "--work", work], work)


def writerun(inst, rev, out, work, clear=True):
    return run([sys.executable, "-B", inst, "--lane", CLONE, "--write", out,
                "--rev", rev, "--work", work], work, clear)


def first(text):
    for ln in text.splitlines():
        if "CENSUS" in ln:
            return ln.strip()
    return text.splitlines()[-1].strip() if text else "(no output)"


def fmt(r):
    return "rc=%d %s" % (r[0], first(r[1]))


def emit(tag, pristine, mutant, verdict):
    print("PROBE %-30s pristine[%s] mutant[%s] => %s" % (tag, fmt(pristine), fmt(mutant), verdict))


def write_probe(name, text):
    d = os.path.join(S, "work", name)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "census.md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


def git(args, env=None):
    return subprocess.run(["git", "-C", CLONE] + args, capture_output=True,
                          text=True, env=env)


def main():
    top = git(["rev-parse", "--show-toplevel"]).stdout.strip()
    assert top == CLONE, (top, CLONE)

    # P01 — M01: drop the `..` confinement.  Detector: the committed census of
    # record (P2), not the harness.  Also show the raw rate shift.
    emit("P01-m01-rev-rates", revrun(INST, A, os.path.join(S, "work/p01a")),
         revrun(MUT["01"], A, os.path.join(S, "work/p01b")), "rate shift")
    emit("P01-m01-committed-census",
         check(INST, COMMITTED, os.path.join(S, "work/p01c"), lane=LANE),
         check(MUT["01"], COMMITTED, os.path.join(S, "work/p01d"), lane=LANE),
         "P2 detector")

    # P02 — M02: accept a 12-hex measured-at (digest recomputed, body rev
    # rewritten to the short form).
    h5 = list(H5)
    h5[0] = "measured-at: " + A[:12]
    p02 = write_probe("p02", build(h5, OB.replace(A, A[:12])))
    emit("P02-m02-short-measured-at",
         check(INST, p02, os.path.join(S, "work/p02p")),
         check(MUT["02"], p02, os.path.join(S, "work/p02m")), "length limb")

    # P03 — M03: drop the ancestor check.  measured-at is a 40-hex dangling
    # commit with the measured tree, so every rate matches.
    tree = git(["rev-parse", A + "^{tree}"]).stdout.strip()
    dangling = git(["commit-tree", tree, "-m", "dangling-probe-r99-driver"]).stdout.strip()
    print("PROBE dangling-commit %s ancestor_of_mut=%d" % (
        dangling, git(["merge-base", "--is-ancestor", dangling, "mut"]).returncode))
    h5 = list(H5)
    h5[0] = "measured-at: " + dangling
    p03 = write_probe("p03", build(h5, OB.replace(A, dangling)))
    emit("P03-m03-non-ancestor",
         check(INST, p03, os.path.join(S, "work/p03p")),
         check(MUT["03"], p03, os.path.join(S, "work/p03m")), "ancestor limb")

    # P04 — M04: drop the header digest.  The `home:` line is bound by nothing
    # else in `check`; edit it and keep the stored header digest.
    h5 = list(H5)
    h5[1] = "home: real (host reading)"
    p04 = write_probe("p04", build(h5, OB, hsha=HSHA, bsha=BSHA))
    emit("P04-m04-home-line",
         check(INST, p04, os.path.join(S, "work/p04p")),
         check(MUT["04"], p04, os.path.join(S, "work/p04m")), "header-digest limb")

    # P05 — M05: drop the body digest.  The body equality check is the second
    # limb; show whether the mutant still rejects a body edit.
    body = OB.replace("| GONE | 5342 |", "| GONE | 5343 |")
    assert body != OB
    p05 = write_probe("p05", build(H5, body, hsha=HSHA, bsha=BSHA))
    emit("P05-m05-body-edit",
         check(INST, p05, os.path.join(S, "work/p05p")),
         check(MUT["05"], p05, os.path.join(S, "work/p05m")), "body-digest limb")

    # P06 — M06: read the cache in --check.  Poison a fully self-consistent
    # cache + census (every header line agrees with the fake rates).
    fake = {"rev": A, "rows": 8027, "host_owned": 76, "confined": 1,
            "skill": [162, 733], "corpus": [2569, 7625], "lane": [2607, 8027],
            "skill_host": [165, 733], "corpus_host": [2645, 7625],
            "lane_host": [2683, 8027]}
    h5 = [H5[0], H5[1], ci.pinned_line(fake), ci.host_line(fake), ci.host_owned_line(fake)]
    fake_body = OB + "\n"
    p06 = write_probe("p06", build(h5, fake_body))
    w06 = os.path.join(S, "work/p06m")
    os.makedirs(os.path.join(w06, "cache"), exist_ok=True)
    key = A + "-" + hashlib.sha256(open(MUT["06"], "rb").read()).hexdigest()[:12] + ".json"
    with open(os.path.join(w06, "cache", key), "w", encoding="utf-8") as fh:
        json.dump({"rates": fake, "body": fake_body}, fh)
    emit("P06-m06-cache-read",
         check(INST, p06, os.path.join(S, "work/p06p")),
         check(MUT["06"], p06, w06, clear=False), "cache limb")

    # P07 — M07: compare only the SKILL segment of the pinned line.
    h5 = list(H5)
    h5[2] = h5[2].replace("lane 2607/8026", "lane 2607/8027")
    assert h5[2] != H5[2]
    p07 = write_probe("p07", build(h5, OB))
    emit("P07-m07-skill-only",
         check(INST, p07, os.path.join(S, "work/p07p")),
         check(MUT["07"], p07, os.path.join(S, "work/p07m")), "pinned limb")

    # P08 — M08: drop the host-owned line from the header (killed by T11 in the
    # harness; show the committed census also fails).
    emit("P08-m08-committed-census",
         check(INST, COMMITTED, os.path.join(S, "work/p08p"), lane=LANE),
         check(MUT["08"], COMMITTED, os.path.join(S, "work/p08m"), lane=LANE),
         "harness T11 + P2")

    # P09 — M09: accept a missing pinned line (digest over the placeholder).
    absent = [H5[0], H5[1], H5[3], H5[4]]
    stored = sha("\n".join([H5[0], H5[1], ci.PINNED_PREFIX + " (absent)", H5[3], H5[4]]))
    p09 = write_probe("p09", build(absent, OB, hsha=stored, bsha=BSHA))
    emit("P09-m09-missing-pinned",
         check(INST, p09, os.path.join(S, "work/p09p")),
         check(MUT["09"], p09, os.path.join(S, "work/p09m")), "pinned-present limb")

    # P10 — M10: key the cache by lane.  Write A then B in one work dir; the
    # second write must not reuse A's measurement.
    w10 = os.path.join(S, "work/p10w")
    outA = os.path.join(S, "work/p10/outA.md")
    outB = os.path.join(S, "work/p10/outB.md")
    writerun(MUT["10"], A, outA, w10, clear=True)
    r10 = writerun(MUT["10"], B, outB, w10, clear=False)
    w10b = os.path.join(S, "work/p10w2")
    outA2 = os.path.join(S, "work/p10/outA2.md")
    outB2 = os.path.join(S, "work/p10/outB2.md")
    writerun(INST, A, outA2, w10b, clear=True)
    r10b = writerun(INST, B, outB2, w10b, clear=False)

    def line_of(path, prefix):
        for ln in open(path, encoding="utf-8"):
            if ln.startswith(prefix):
                return ln.strip()
        return "(absent)"

    print("PROBE P10-m10-cache-key mutant[%s] pristine[%s]" % (fmt(r10), fmt(r10b)))
    print("PROBE P10-m10-outB pinned mutant[%s] pristine[%s]" % (
        line_of(outB, "pinned rate"), line_of(outB2, "pinned rate")))
    print("PROBE P10-m10-outB laneroot mutant[%s] pristine[%s]" % (
        line_of(outB, "Lane root:"), line_of(outB2, "Lane root:")))

    # P11 — M11: ignore resolve.py's exit code.  A fixture commit whose
    # resolve.py writes a TSV and exits 1.
    probe_resolve = (
        "#!/usr/bin/env python3\n"
        "import os, sys\n"
        "root = sys.argv[1]\n"
        "tsv = os.path.join(root, 'corpus/instruments/citation-survival.tsv')\n"
        "with open(tsv, 'w') as fh:\n"
        "    fh.write('citation\\tclass\\tresolved\\tp4\\tp5\\tp6\\tp7\\tscopes\\n')\n"
        "    fh.write('probe-citation\\tINTERNAL\\t/abs/probe\\tx\\tx\\tx\\tx\\tSKILL\\n')\n"
        "sys.exit(1)\n")
    tmp = os.path.join(S, "work/probe-resolve.py")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(probe_resolve)
    blob = git(["hash-object", "-w", tmp]).stdout.strip()
    idx = os.path.join(S, "work/probe-index")
    ienv = dict(os.environ)
    ienv["GIT_INDEX_FILE"] = idx
    base_tree = git(["rev-parse", A + "^{tree}"]).stdout.strip()
    subprocess.run(["git", "-C", CLONE, "read-tree", base_tree], env=ienv, check=True)
    subprocess.run(["git", "-C", CLONE, "update-index", "--add", "--cacheinfo",
                    "100644,%s,corpus/instruments/resolve.py" % blob], env=ienv, check=True)
    new_tree = subprocess.run(["git", "-C", CLONE, "write-tree"], env=ienv,
                              capture_output=True, text=True, check=True).stdout.strip()
    probe_commit = git(["commit-tree", new_tree, "-p", A, "-m",
                        "probe-m11-failing-resolve"]).stdout.strip()
    os.unlink(idx)
    print("PROBE probe-commit %s" % probe_commit)
    emit("P11-m11-resolve-rc",
         revrun(INST, probe_commit, os.path.join(S, "work/p11p")),
         revrun(MUT["11"], probe_commit, os.path.join(S, "work/p11m")), "resolve-rc limb")

    # P12 — M12: accept a --write revision that is not an ancestor.
    outP = os.path.join(S, "work/p12/outP.md")
    outM = os.path.join(S, "work/p12/outM.md")
    emit("P12-m12-write-non-ancestor",
         writerun(INST, dangling, outP, os.path.join(S, "work/p12p")),
         writerun(MUT["12"], dangling, outM, os.path.join(S, "work/p12m")),
         "write-ancestor limb")
    return 0


if __name__ == "__main__":
    sys.exit(main())
