#!/usr/bin/env python3
"""Round-93 C1 controls: every do-nothing / forgery variant must fail the frozen
round-93 knowledge meter (rc=1, or rc=2 on a missing read), and the candidate must
pass (rc=0). Run before the freeze; the receipt is committed with the freeze.

Usage: c1-controls-r93.py CANDIDATE_LANE BASE_REV AFTER_REV METER MAP LABELS WORK OUTDIR

CANDIDATE_LANE is a scratch clone whose AFTER_REV holds the five edits and the
labels file at .ufo/waves/round-93/c1/labels.tsv; BASE_REV is the lane base.
"""
import os
import shutil
import subprocess
import sys
import tempfile

MAP = "repair-map.tsv"
LAB = "labels.tsv"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def run(meter, lane, base, after, map_path, labels_rev, work, extra=()):
    cmd = [sys.executable, "-B", meter, "--lane", lane, "--base-rev", base,
           "--after-rev", after, "--map", map_path, "--labels-rev", labels_rev,
           "--base-target", "1007/2001", "--target", "1009/2000", "--work", work] + list(extra)
    p = sh(cmd)
    return p.returncode, p.stdout + p.stderr


def label_lines(labels_path):
    return open(labels_path, encoding="utf-8").read().rstrip("\n").split("\n")


def write_labels(path, lines):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def clone(lane, dest):
    sh(["git", "clone", "-q", "--shared", lane, dest])
    return dest


def commit(repo, msg):
    sh(["git", "-C", repo, "add", "-A"])
    p = sh(["git", "-C", repo, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
            "commit", "-q", "-m", msg])
    if p.returncode != 0:
        raise SystemExit("commit failed: %s" % p.stderr)
    return sh(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()


def main(argv):
    cand, base, after, meter, map_in, labels_in, work, outdir = argv
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    results = []

    def record(name, rc, want, out):
        ok = rc == want
        results.append(ok)
        print("CONTROL %s rc=%d want=%d %s" % (name, rc, want, "PASS" if ok else "FAIL"))
        for line in out.splitlines():
            if line.startswith(("KNOWLEDGE-METER ", "LIMB ", "KNOWLEDGE-METER-RESULT")):
                print("  " + line)

    # 0. positive control: the candidate passes.
    rc, out = run(meter, cand, base, after, map_in, after, work)
    record("candidate", rc, 0, out)

    # 1. do-nothing: the after rev is the base rev.
    rc, out = run(meter, cand, base, base, map_in, after, work)
    record("do-nothing", rc, 1, out)

    # 2. partial map: row 437 removed (the edit stays unmapped in the after rev).
    d = tempfile.mkdtemp(prefix="c1ctl-", dir=work)
    rows = [l for l in open(map_in).read().rstrip("\n").split("\n") if l]
    partial = os.path.join(d, MAP)
    with open(partial, "w") as fh:
        fh.write("\n".join(r for r in rows if not r.startswith("corpus/knowledge/triage-thresholds.md:437\t")) + "\n")
    rc, out = run(meter, cand, base, after, partial, after, work)
    record("partial-437-unmapped", rc, 1, out)

    # 3. map claims no edit at 454 (old == new).
    bad = os.path.join(d, "map-454-noop.tsv")
    with open(bad, "w") as fh:
        for r in rows:
            c = r.split("\t")
            if c[0] == "corpus/knowledge/triage-thresholds.md:454":
                c[3] = c[2]
            fh.write("\t".join(c) + "\n")
    rc, out = run(meter, cand, base, after, bad, after, work)
    record("map-454-noop", rc, 1, out)

    # 4. a no-edit CORRECT pair mapped as an edit (unlabelled map row).
    bad = os.path.join(d, MAP)
    with open(bad, "w") as fh:
        fh.write("\n".join(rows) + "\n")
        fh.write("corpus/knowledge/citation-bases.md:14\tclaim-gates.md:3\t`claim-gates.md:3`\t`corpus/knowledge/claim-gates.md:3`\n")
    rc, out = run(meter, cand, base, after, bad, after, work)
    record("no-edit-pair-mapped", rc, 1, out)

    # 5. cell-repair row claims a replacement with the old cell (no edit).
    bad = os.path.join(d, MAP)
    with open(bad, "w") as fh:
        for r in rows:
            c = r.split("\t")
            if c[0].endswith(":437"):
                c[3] = c[2]
            fh.write("\t".join(c) + "\n")
    rc, out = run(meter, cand, base, after, bad, after, work)
    record("cell-437-noop", rc, 1, out)

    # 6. duplicate map row (two rows for 437).
    bad = os.path.join(d, MAP)
    with open(bad, "w") as fh:
        fh.write("\n".join(rows) + "\n")
        fh.write([r for r in rows if r.startswith("corpus/knowledge/triage-thresholds.md:437\t")][0] + "\n")
    rc, out = run(meter, cand, base, after, bad, after, work)
    record("duplicate-map-row", rc, 1, out)

    # 7. wrong key column: 454's key renamed so no label pair matches.
    bad = os.path.join(d, MAP)
    with open(bad, "w") as fh:
        for r in rows:
            c = r.split("\t")
            if c[0].endswith(":454"):
                c[1] = "SKILL.md:111"
            fh.write("\t".join(c) + "\n")
    rc, out = run(meter, cand, base, after, bad, after, work)
    record("wrong-key-454", rc, 1, out)

    # 8. missing labels at the labels rev (base has no labels file).
    rc, out = run(meter, cand, base, after, map_in, base, work)
    record("missing-labels", rc, 2, out)

    # 9. wrong map sha256.
    rc, out = run(meter, cand, base, after, map_in, after, work, ["--map-sha256", "0" * 64])
    record("wrong-map-sha", rc, 1, out)

    # 10. M3 covers a retained label on a non-knowledge file: a control clone
    #     changes SKILL.md line 191 while its label says "No edit".
    d = tempfile.mkdtemp(prefix="c1ctl-scope-", dir=work)
    ctl = clone(cand, os.path.join(d, "lane"))
    with open(os.path.join(ctl, "SKILL.md"), encoding="utf-8") as fh:
        sk = fh.read().split("\n")
    sk[190] = sk[190] + " (control edit)"
    with open(os.path.join(ctl, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sk))
    lab = label_lines(os.path.join(ctl, ".ufo/waves/round-93/c1/labels.tsv"))
    lab.append("SKILL.md:191\tSKILL.md:191\tCORRECT\tNo edit: control fixture for the M3 labelled-file scope.\tcontrol")
    write_labels(os.path.join(ctl, ".ufo/waves/round-93/c1/labels.tsv"), lab)
    # The map and knowledge edits stay as in the candidate.
    shr = os.path.join(ctl, ".ufo/waves/round-93/c1/repair-map.tsv")
    shutil.copy(map_in, shr)
    scope_rev = commit(ctl, "scope control")
    rc, out = run(os.path.join(ctl, ".ufo/waves/round-93/c1/knowledge-meter.py"), ctl,
                  base, scope_rev, os.path.join(ctl, ".ufo/waves/round-93/c1/repair-map.tsv"),
                  scope_rev, work)
    record("m3-labelled-file-scope", rc, 1, out)

    print("C1-CONTROLS-RESULT %s controls=%d" % ("pass" if all(results) else "fail", len(results)))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
