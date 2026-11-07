#!/usr/bin/env python3
"""Round-97 C1 controls: the frozen meter must pass on the candidate (rc=0,
pinned) and every negative fixture must fail on a DECLARED limb set only.

Each negative fixture isolates one rule: its FAIL set must equal the set declared
here (the named limb plus the counter's own code-level implications, one reason
per fixture). Two implications are structural: M5's condition includes M4 (an
unbound value cannot be range-checked), and a qualify-lane map that disagrees
with its label fails both M4 (value shape/target) and M9 (label agreement).

Every fixture clones the PINNED candidate revision (round-94 defect 1) and never
the mutable live lane. Fixture edits are chosen so the citation meter's rate is
unchanged: a fixture replaces a single-occurrence GONE token with a GONE token,
composes to the candidate's own line, or edits text that carries no path token.

Usage: c1-controls-r97.py CANDIDATE_CLONE FREEZE_REV R96_COUNTER WORK OUTDIR
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
C1 = LANE + "/.ufo/waves/round-97/c1"
BASE = "b06af5e07efbd961a8449f7de6b57eeea62c6bd3"
MAP = C1 + "/repair-map.tsv"
LABELS = C1 + "/labels.tsv"
LABELS_REL = ".ufo/waves/round-97/c1/labels.tsv"
MAP_REL = ".ufo/waves/round-97/c1/repair-map.tsv"
BASE_TARGET = "1040/2041"
TARGET = "1043/2035"
TRIAGE = "corpus/knowledge/triage-thresholds.md"
CITB = "corpus/knowledge/citation-bases.md"
LEDGER = "corpus/knowledge/considerthese-proposals-ledger.md"
BOD = "corpus/knowledge/cisa-bod-20-01-vdp-minimums.md"
GHPFX = "corpus/knowledge/github-prefixed-tokens-in-captured-evidence.md"
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
    cand, freeze, r96, work, outdir = argv
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

    def record(name, rc, want, out, declared=None):
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
    print("C1-CONTROLS candidate=%s base=%s freeze=%s r96=%s" % (cand_rev, BASE, freeze, r96))
    log.append("C1-CONTROLS candidate=%s base=%s freeze=%s r96=%s work=%s" % (
        cand_rev, BASE, freeze, r96, work))

    # 0. candidate: every limb passes, rc 0
    rc, out = run(meter, cand, cand_rev, freeze, MAP, TARGET, real_sha)
    record("candidate", rc, 0, out, declared=[])

    # 1. do-nothing: the after revision is the base (M1 rate, M3 33 lines)
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

    # 5. the round-96 counter (LABELS_PATH repointed only) on the same candidate:
    #    the 33 qualify-lane rows are unexpressible (unknown kind), so the
    #    successor is needed. M5 follows M4 by the counter's own condition.
    d = clone(cand, os.path.join(work, "fx-r96"))
    write(os.path.join(d, ".ufo/waves/round-97/c1/r96-counter.py"),
          read(r96).replace(".ufo/waves/round-96/c1/labels.tsv",
                            ".ufo/waves/round-97/c1/labels.tsv", 1))
    rev = commit(d)
    rc, out = run(os.path.join(d, ".ufo/waves/round-97/c1/r96-counter.py"),
                  d, rev, freeze, os.path.join(d, MAP_REL), TARGET, sha)
    record("r96-no-qualify-branch", rc, 1, out, declared=["M4", "M5", "M9", "M10"])

    # 6. qualify-lane target not tracked: a single-occurrence bare token is
    #    qualified to a path that is not in the after tree (GONE -> GONE, so the
    #    rate is unchanged); M4 rejects the value, M5 follows M4.
    lab = GHPFX + ":151\tquote-anchor-check.py\tcorpus/instruments/quote-anchor-check.py\t" \
                 "Qualify to corpus/instruments/quote-anchor-check.py\tevidence\n"
    mp = GHPFX + ":151\tquote-anchor-check.py\t`quote-anchor-check.py`\t`corpus/instruments/quote-anchor-check.py`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-target-missing"), label_append=lab,
                          map_append=mp,
                          edits=[(GHPFX, 151, "`quote-anchor-check.py`",
                                  "`corpus/instruments/quote-anchor-check.py`")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("qualify-target-missing", rc, 1, out, declared=["M4", "M5"])

    # 7. qualify-lane key not bare: the key carries a separator, so the binding
    #    refuses it (GONE -> GONE, rate unchanged); M5 follows M4.
    lab = LEDGER + ":154\tcontrols/plain-rows.sh\tcorpus/instruments/plain-rows.sh\t" \
                  "Qualify to corpus/instruments/plain-rows.sh\tevidence\n"
    mp = LEDGER + ":154\tcontrols/plain-rows.sh\t`controls/plain-rows.sh`\t`corpus/instruments/plain-rows.sh`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-key-slash"), label_append=lab,
                          map_append=mp,
                          edits=[(LEDGER, 154, "`controls/plain-rows.sh`",
                                  "`corpus/instruments/plain-rows.sh`")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("qualify-key-not-bare", rc, 1, out, declared=["M4", "M5"])

    # 8. map-not-label: the map's (old, new) composes to the candidate's own line
    #    but is not the pair the label names (M9; M4 because the qualify-lane
    #    binding requires old == `key`; M5 follows M4)
    mapt = read(MAP).replace(
        CITB + ":65\tresolve.py\t`resolve.py`\t`corpus/instruments/resolve.py`",
        CITB + ":65\tresolve.py\t`resolve.py`,\t`corpus/instruments/resolve.py`,")
    d, rev, sha = fixture(cand, os.path.join(work, "fx-m9"), map_text=mapt)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("map-not-label", rc, 1, out, declared=["M4", "M5", "M9"])

    # 9. unknown-kind-row: a label whose kind the counter cannot express, unmapped
    lab = BOD + ":159\tS021.txt\tweird-kind\tDo something else\tevidence\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-kind"), label_append=lab)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unknown-kind-row", rc, 1, out, declared=["M10"])

    # 10. unlabelled-only: a no-op map row with no label (M9 unbound + M10
    #     unlabelled; M3/M4/M5 stay green because the pair composes to the
    #     candidate line and the value is a valid knowledge citation)
    mp = (TRIAGE + ":57\tcorpus/knowledge/mission-control.md:20-24\t"
          "`corpus/knowledge/mission-control.md:20-24`\t`corpus/knowledge/mission-control.md:20-24`\n")
    d, rev, sha = fixture(cand, os.path.join(work, "fx-unlabelled"), map_append=mp)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unlabelled-only", rc, 1, out, declared=["M9", "M10"])

    # 11. unapplied-only: a label naming an edit that no map row applies
    lab = BOD + ":159\tS021.txt\tcorpus/source-snapshots/round-40/S021.txt\t" \
                "corpus/source-snapshots/round-40/S021.txt\tevidence\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-unapplied"), label_append=lab)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("unapplied-only", rc, 1, out, declared=["M10"])

    # 12. duplicate-row: the same (site, key) mapped twice (M3 dup_rows)
    mp = CITB + ":65\tresolve.py\t`resolve.py`\t`corpus/instruments/resolve.py`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-dup"), map_append=mp)
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("duplicate-row", rc, 1, out, declared=["M3"])

    # 13. snapshot-missing-only: a bare GONE capture token repointed to a missing
    #     snapshot directory (both GONE, so M1 holds); M4 fails on the missing
    #     file and M5 follows M4.
    lab = (BOD + ":159\tS021.txt\tcorpus/source-snapshots/round-31/S021.txt\t"
           "corpus/source-snapshots/round-31/S021.txt\tevidence\n")
    mp = BOD + ":159\tS021.txt\t`S021.txt`\t`corpus/source-snapshots/round-31/S021.txt`\n"
    d, rev, sha = fixture(cand, os.path.join(work, "fx-snap"), label_append=lab, map_append=mp,
                          edits=[(BOD, 159, "`S021.txt`", "`corpus/source-snapshots/round-31/S021.txt`")])
    rc, out = run(meter, d, rev, rev, os.path.join(d, MAP_REL), TARGET, sha)
    record("snapshot-missing-only", rc, 1, out, declared=["M4", "M5"])

    verdict = all(results)
    att_ok = all(attribution)
    print("ATTRIBUTION %s fixtures=%d" % ("pass" if att_ok else "fail", len(attribution)))
    print("C1-CONTROLS-RESULT %s controls=%d" % ("pass" if verdict else "fail", len(results)))
    write(os.path.join(outdir, "c1-controls-r97.txt"),
          "\n".join(log + ["ATTRIBUTION %s fixtures=%d" % ("pass" if att_ok else "fail", len(attribution)),
                           "C1-CONTROLS-RESULT %s controls=%d" % ("pass" if verdict else "fail", len(results))]) + "\n")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
