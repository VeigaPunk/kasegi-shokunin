#!/usr/bin/env python3
"""Round-96 C1 controls: the frozen meter must pass on the candidate (rc=0,
pinned) and every negative fixture must fail on a DECLARED limb set only.

Round-95 defect (MutC1Counter, 10 of 18 mutants survived): the shipped negative
fixtures were multi-defect, so a verdict could not be attributed to the rule
under test. Each round-96 negative fixture isolates one limb: its FAIL set must
equal the set declared here (the named limb plus the counter's own code-level
implications, one reason per fixture).

Every fixture clones the PINNED candidate revision (round-94 defect 1) and never
the mutable live lane. Fixture edits are chosen so the citation meter's rate is
unchanged: a fixture replaces a GONE token with a GONE token, composes to the
candidate's own line, or edits text that carries no path token.

Usage: c1-controls-r96.py CANDIDATE_CLONE FREEZE_REV R95_COUNTER WORK OUTDIR
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C1 = LANE + "/.ufo/waves/round-96/c1"
BASE = "d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6"
MAP = C1 + "/repair-map.tsv"
LABELS = C1 + "/labels.tsv"
LABELS_REL = ".ufo/waves/round-96/c1/labels.tsv"
MAP_REL = ".ufo/waves/round-96/c1/repair-map.tsv"
BASE_TARGET = "1030/2027"
TARGET = "1032/2028"
TRIAGE = "corpus/knowledge/triage-thresholds.md"
ISO = "corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md"
DOJ = "corpus/knowledge/doj-vdp-framework-scope-and-authorization.md"
LIMB = re.compile(r"^LIMB (M\d+) (pass|FAIL)", re.M)


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def commit(d):
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
        "commit", "-q", "-m", "fixture"])
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    if top != os.path.realpath(d):
        raise SystemExit("fixture root mismatch at " + d)
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def clone(src, dest):
    shutil.rmtree(dest, ignore_errors=True)
    r = sh(["git", "clone", "-q", "--shared", src, dest])
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return dest


def fixture(cand, dest, edits=None, map_text=None, map_append=None, label_append=None,
            new_files=None, drop_labels=False):
    d = clone(cand, dest)
    if drop_labels:
        os.unlink(os.path.join(d, LABELS_REL))
    if label_append:
        write(os.path.join(d, LABELS_REL), read(os.path.join(d, LABELS_REL)) + label_append)
    if map_text is not None:
        write(os.path.join(d, MAP_REL), map_text)
    elif map_append:
        write(os.path.join(d, MAP_REL), read(os.path.join(d, MAP_REL)) + map_append)
    for rel, text in (new_files or {}).items():
        write(os.path.join(d, rel), text)
    files = {}
    for rel, n, old, new in (edits or []):
        if rel not in files:
            files[rel] = read(os.path.join(d, rel)).split("\n")
        if files[rel][n - 1].count(old) != 1:
            raise SystemExit("edit anchor not unique at %s:%d" % (rel, n))
        files[rel][n - 1] = files[rel][n - 1].replace(old, new)
    for rel, lines in files.items():
        write(os.path.join(d, rel), "\n".join(lines))
    rev = commit(d)
    sha = sh(["sha256sum", os.path.join(d, MAP_REL)]).stdout.split()[0]
    return d, rev, sha


def main(argv):
    cand, freeze, r95, work, outdir = argv
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    results, log, attribution = [], [], []

    def run(counter, lane, after, labels_pin, map_path, target, map_sha=None):
        wd = os.path.join(work, "w")
        os.makedirs(wd, exist_ok=True)
        cmd = [sys.executable, "-B", counter, "--lane", lane, "--base-rev", BASE,
               "--after-rev", after, "--map", map_path, "--labels-rev", labels_pin,
               "--base-target", BASE_TARGET, "--target", target, "--work", wd]
        if map_sha:
            cmd += ["--map-sha256", map_sha]
        p = sh(cmd)
        return p.returncode, p.stdout + p.stderr

    def record(name, rc, want, out, limbs=None, declared=None):
        got = sorted(set(LIMB.findall(out)))
        fails = {m for m, v in got if v == "FAIL"}
        ok = rc == want
        att = ""
        if declared is None:
            declared = []
        else:
            ok = ok and fails == set(declared)
            att = " attribution=%s" % ("PASS" if fails == set(declared) else "FAIL")
            attribution.append(fails == set(declared))
        results.append(ok)
        line = "CONTROL %s rc=%d want=%d %s limbs=%s declared=%s%s" % (
            name, rc, want, "PASS" if ok else "FAIL",
            ",".join(sorted(fails)) or "none", ",".join(sorted(declared)) or "-", att)
        print(line)
        log.append(line)
        for ln in out.splitlines():
            if ln.startswith(("KNOWLEDGE-METER ", "LIMB ", "KNOWLEDGE-METER-RESULT")) or "Traceback" in ln:
                print("  " + ln)
                log.append("  " + ln)

    meter = C1 + "/knowledge-meter.py"
    real_sha = sh(["sha256sum", MAP]).stdout.split()[0]
    cand_rev = sh(["git", "-C", cand, "rev-parse", "HEAD"]).stdout.strip()
    print("C1-CONTROLS candidate=%s base=%s freeze=%s r95=%s" % (cand_rev, BASE, freeze, r95))
    log.append("C1-CONTROLS candidate=%s base=%s freeze=%s r95=%s work=%s" % (
        cand_rev, BASE, freeze, r95, work))

    # 0. candidate: every limb passes, rc 0
    rc, out = run(meter, cand, cand_rev, freeze, MAP, TARGET, real_sha)
    record("candidate", rc, 0, out, declared=[])

    # 1. do-nothing: the after revision is the base (M1 rate, M3 five lines)
    rc, out = run(meter, cand, BASE, freeze, MAP, TARGET, real_sha)
    record("do-nothing", rc, 1, out, declared=["M1", "M3"])

    # 2. missing labels file at the pinned path (rc 2)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-nolabels"), drop_labels=True)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("missing-labels", rc, 2, out)

    # 3. wrong map sha (M6 only)
    rc, out = run(meter, cand, cand_rev, freeze, MAP, TARGET, "0" * 64)
    record("wrong-map-sha", rc, 1, out, declared=["M6"])

    # 4. extra unlisted edit: a text change the map does not name (M3 only;
    #    the edited text carries no path token, so the rate is unchanged)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-extra"),
                          edits=[(TRIAGE, 143, "MATCHES:", "MATCHES :")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("extra-unlisted-edit", rc, 1, out, declared=["M3"])

    # 5. the round-95 counter (LABELS_PATH repointed only) on the same candidate:
    #    the two prose-pointer rows are unbound (M4), so the successor is needed
    d = clone(cand, os.path.join(work, "fx-r95"))
    write(os.path.join(d, ".ufo/waves/round-96/c1/r95-counter.py"),
          read(r95).replace(".ufo/waves/round-95/c1/labels.tsv",
                            ".ufo/waves/round-96/c1/labels.tsv", 1))
    rev = commit(d)
    rc, out = run(os.path.join(d, ".ufo/waves/round-96/c1/r95-counter.py"),
                  d, rev, freeze, os.path.join(d, MAP_REL), TARGET, sha)
    record("r95-no-prose-branch", rc, 1, out, declared=["M4", "M5"])

    # 6. row-old-absent-only: a prose part row whose old is not on its line
    #    (M3's old_not_once); M4/M9/M10 stay green.
    lab = ISO + ":36\t(L1819)\tpart-repair\tReplace part: (L1819) => (L1820)\tevidence\n"
    mp = ISO + ":36\t(L1819)\t(L1819)\t(L1820)\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-old-absent"),
                          label_append=lab, map_append=mp)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("row-old-absent-only", rc, 1, out, declared=["M3"])

    # 7. map-not-label: the map's (old, new) composes to the candidate's own line
    #    but is not the pair the label names (M9 only).
    mapt = read(MAP).replace(
        TRIAGE + ":88\tSKILL.md:182-184\t`SKILL.md:182-184`\t`SKILL.md:182-185`",
        TRIAGE + ":88\tSKILL.md:182-184\t`SKILL.md:182-184` (round-13\t`SKILL.md:182-185` (round-13", 1)
    d, rev, sha = fixture(cand, os.path.join(work, "fx-m9"), map_text=mapt)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("map-not-label", rc, 1, out, declared=["M9"])

    # 8. snapshot-missing-only: a bare GONE capture token repointed to a missing
    #    snapshot directory (both GONE, so M1 holds); M4 fails, M5 is implied.
    lab = (DOJ + ":136\tS020.txt\tcorpus/source-snapshots/round-31/S020.txt\t"
           "corpus/source-snapshots/round-31/S020.txt\tevidence\n")
    mp = DOJ + ":136\tS020.txt\t`S020.txt`\t`corpus/source-snapshots/round-31/S020.txt`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-snap"), label_append=lab, map_append=mp,
                          edits=[(DOJ, 136, "`S020.txt`", "`corpus/source-snapshots/round-31/S020.txt`")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("snapshot-missing-only", rc, 1, out, declared=["M4", "M5"])

    # 9. unknown-kind-row: a label whose kind the counter cannot express, unmapped
    lab = ISO + ":36\t(L1819)\tweird-kind\tDo something else\tevidence\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-kind"), label_append=lab)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unknown-kind-row", rc, 1, out, declared=["M10"])

    # 10. unlabelled-only: a map row with no label (M9 unbound + M10 unlabelled;
    #     M3/M4/M5 stay green because the pair composes to the candidate line)
    mp = (TRIAGE + ":89\tSKILL.md:182-184\t`SKILL.md:182-184`\t`SKILL.md:182-184`\n")
    d, rev, sha = fixture(cand, os.path.join(work, "fx-unlabelled"), map_append=mp)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unlabelled-only", rc, 1, out, declared=["M9", "M10"])

    # 11. unapplied-only: a label naming an edit that no map row applies
    lab = ISO + ":36\t(L1819)\tpart-repair\tReplace part: (L1819) => (L1820)\tevidence\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-unapplied"), label_append=lab)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unapplied-only", rc, 1, out, declared=["M10"])

    verdict = all(results)
    att_ok = all(attribution)
    print("ATTRIBUTION %s fixtures=%d" % ("pass" if att_ok else "fail", len(attribution)))
    print("C1-CONTROLS-RESULT %s controls=%d" % ("pass" if verdict else "fail", len(results)))
    write(os.path.join(outdir, "c1-controls-r96.txt"),
          "\n".join(log + ["ATTRIBUTION %s fixtures=%d" % ("pass" if att_ok else "fail", len(attribution)),
                           "C1-CONTROLS-RESULT %s controls=%d" % ("pass" if verdict else "fail", len(results))]) + "\n")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
