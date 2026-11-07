#!/usr/bin/env python3
"""kasegi round-98 C1 instrument — the citation census of record, measured at a
named revision.

Round 19 regenerated `corpus/instruments/citation-survival.md` against the live
working tree and recorded no revision; every later round inherited it, so the
"census of record" has been a reading of an unnamed tree (SCORECARD r92-r97
carry it as `132/701`, not regenerated). This wrapper makes the census a
reading of a revision:

  * `git archive REV` is extracted into --work (never the live lane), the
    extract's own `corpus/instruments/resolve.py` is run there, and the
    generated `citation-survival.tsv` is read back;
  * two rates are reported. The PINNED rate counts INTERNAL citations only
    (lane-relative, revision-stable). The HOST-INCLUSIVE rate is resolve.py's
    own definition (RESOLVES + MIRROR-EQUIVALENT + INTERNAL) and depends on
    host-owned absolute paths, which are reported on their own line (R142);
  * `--write FILE` writes the census of record: a header naming the revision
    and both rates, then resolve.py's generated body;
  * `--check FILE` re-measures the revision the file's `measured-at:` line
    names and compares the file's `pinned rate` line with that measurement.

A measurement is cached per revision under --work/cache (the measurement is
deterministic for a revision), so a control set that checks the same revision
eight times runs resolve.py once.

Exit: 0 pass, 1 fail, 2 could-not-evaluate (missing input, bad revision,
resolve.py error, no citations).

Usage:
  python3 -B corpus/instruments/census-at-rev.py --lane . --rev <hash> --work <scratch>
  python3 -B corpus/instruments/census-at-rev.py --lane . --write corpus/instruments/citation-survival.md --work <scratch>
  python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <scratch>
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile

RESOLVE = "corpus/instruments/resolve.py"
TSV = "corpus/instruments/citation-survival.tsv"
CENSUS = "corpus/instruments/citation-survival.md"
HEAD = "# citation-survival census — kasegi lane"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pct(n, m):
    return "%.2f%%" % (100.0 * n / m) if m else "n/a"


def extract(lane, rev, work):
    d = os.path.join(work, "tree-" + rev[:12])
    if os.path.isfile(os.path.join(d, RESOLVE)):
        return d, None
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    p = subprocess.run(["git", "-C", lane, "archive", rev], capture_output=True)
    if p.returncode != 0:
        return None, "bad-revision"
    tf = os.path.join(work, "tree-" + rev[:12] + ".tar")
    with open(tf, "wb") as fh:
        fh.write(p.stdout)
    with tarfile.open(tf) as tar:
        # The source is this lane's own committed tree; a committed absolute
        # symlink under .ufo/ (round-25 assimilation rows) is outside the
        # resolver's scope, so the extract is trusted as-is.
        try:
            tar.extractall(d, filter="fully_trusted")
        except TypeError:
            tar.extractall(d)
    os.unlink(tf)
    if not os.path.isfile(os.path.join(d, RESOLVE)):
        return None, "no-resolve"
    return d, None


def measure(lane, rev, work):
    """Return (rates, body, error). Cached per revision under work/cache."""
    cache = os.path.join(work, "cache", rev + ".json")
    if os.path.isfile(cache):
        with open(cache, encoding="utf-8") as fh:
            c = json.load(fh)
        return c["rates"], c["body"], None
    d, err = extract(lane, rev, work)
    if err:
        return None, None, err
    r = sh([sys.executable, "-B", os.path.join(d, RESOLVE), d])
    if r.returncode != 0:
        return None, None, "resolve-rc%d" % r.returncode
    tsv = os.path.join(d, TSV)
    if not os.path.isfile(tsv):
        return None, None, "no-tsv"
    rows = []
    with open(tsv, encoding="utf-8") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        if head[:2] != ["citation", "class"]:
            return None, None, "bad-tsv"
        for line in fh:
            cells = line.rstrip("\n").split("\t")
            if len(cells) < 8:
                continue
            # A citation may itself contain tabs; the trailing seven fields are
            # fixed, so class is cells[-7] and scopes is the last cell.
            rows.append((cells[-7], cells[-1]))
    if not rows:
        return None, None, "no-rows"

    def rate(scope):
        sel = [c for c, sc in rows if scope == "ALL" or scope in sc]
        num = [c for c in sel if c == "INTERNAL"]
        return len(num), len(sel)

    def host_incl(scope):
        sel = [c for c, sc in rows if scope == "ALL" or scope in sc]
        num = [c for c in sel if c in ("INTERNAL", "RESOLVES", "MIRROR-EQUIVALENT")]
        return len(num), len(sel)

    host_owned = sum(1 for c, _ in rows if c in ("RESOLVES", "MIRROR-EQUIVALENT"))
    out = {"rev": rev, "rows": len(rows), "host_owned": host_owned}
    for tag, scope in (("skill", "SKILL"), ("corpus", "+CORPUS"), ("lane", "ALL")):
        n, m = rate(scope)
        hn, hm = host_incl(scope)
        out[tag] = [n, m]
        out[tag + "_host"] = [hn, hm]
    p = os.path.join(d, CENSUS)
    if not os.path.isfile(p):
        return None, None, "no-census"
    with open(p, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if lines and lines[0].startswith(HEAD):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines.pop(0)
    # The extract path is scratch, never evidence: every resolved path in the
    # body names the lane root (the extract is a byte-identical copy of the
    # revision's tree), and the Lane root line names the revision (R142).
    body = "\n".join(lines)
    body = body.replace(d + "/./", lane + "/").replace(d + "/", lane + "/")
    lines = body.split("\n")
    for i, ln in enumerate(lines):
        if ln.startswith("Lane root: `"):
            lines[i] = "Lane root: `%s` (measured from the git-archive extract of `%s`)" % (lane, rev)
            break
    body = "\n".join(lines)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "w", encoding="utf-8") as fh:
        json.dump({"rates": out, "body": body}, fh)
    return out, body, None


def pinned_line(rates):
    return ("pinned rate (INTERNAL only; revision-stable): "
            "SKILL %d/%d = %s | corpus %d/%d = %s | lane %d/%d = %s" % (
                rates["skill"][0], rates["skill"][1], pct(*rates["skill"]),
                rates["corpus"][0], rates["corpus"][1], pct(*rates["corpus"]),
                rates["lane"][0], rates["lane"][1], pct(*rates["lane"])))


def host_line(rates):
    return ("host-inclusive rate (resolve.py's definition): "
            "SKILL %d/%d = %s | corpus %d/%d = %s | lane %d/%d = %s" % (
                rates["skill_host"][0], rates["skill_host"][1], pct(*rates["skill_host"]),
                rates["corpus_host"][0], rates["corpus_host"][1], pct(*rates["corpus_host"]),
                rates["lane_host"][0], rates["lane_host"][1], pct(*rates["lane_host"])))


def write_census(lane, rev, work, out):
    rates, body, err = measure(lane, rev, work)
    if err:
        print("CENSUS-WRITE error reason=%s rc=2" % err)
        return 2
    head = [
        HEAD,
        "",
        "Census of record — regenerated in round 98 at the revision below.",
        "",
        "measured-at: %s" % rev,
        pinned_line(rates),
        host_line(rates),
        "host-owned inputs: %d absolute-path citations resolve outside the lane "
        "(reported separately; not revision-stable)" % rates["host_owned"],
        "",
        "---",
        "",
        "",
    ]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(head) + body)
    print("CENSUS-WRITE ok rev=%s skill=%d/%d lane=%d/%d host_owned=%d" % (
        rev, rates["skill"][0], rates["skill"][1], rates["lane"][0], rates["lane"][1],
        rates["host_owned"]))
    return 0


def check(lane, path, work):
    if not os.path.isfile(path):
        print("CENSUS-CHECK fail reason=missing-file rc=2")
        return 2
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"^measured-at: ([0-9a-f]{40})$", text, re.M)
    if not m:
        print("CENSUS-CHECK fail reason=no-measured-at rc=1")
        return 1
    rev = m.group(1)
    p = re.search(r"^pinned rate \(INTERNAL only; revision-stable\): (.+)$", text, re.M)
    if not p:
        print("CENSUS-CHECK fail reason=no-pinned-line rc=1")
        return 1
    rates, body, err = measure(lane, rev, work)
    if err:
        print("CENSUS-CHECK fail reason=%s rc=2" % err)
        return 2
    want = pinned_line(rates)
    got = "pinned rate (INTERNAL only; revision-stable): " + p.group(1)
    if got != want:
        print("CENSUS-CHECK fail reason=pinned-mismatch rc=1")
        print("  file: %s" % got)
        print("  rev : %s" % want)
        return 1
    print("CENSUS-CHECK pass rev=%s skill=%d/%d corpus=%d/%d lane=%d/%d host_owned=%d" % (
        rev, rates["skill"][0], rates["skill"][1], rates["corpus"][0], rates["corpus"][1],
        rates["lane"][0], rates["lane"][1], rates["host_owned"]))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--write")
    ap.add_argument("--check")
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    work = os.path.abspath(a.work) if a.work else os.path.join(
        os.environ.get("TMPDIR", "/tmp"), "census-at-rev")
    os.makedirs(work, exist_ok=True)
    if a.check:
        return check(lane, a.check, work)
    if a.write:
        rev = a.rev or sh(["git", "-C", lane, "rev-parse", "HEAD"]).stdout.strip()
        if not re.fullmatch(r"[0-9a-f]{40}", rev or ""):
            print("CENSUS-WRITE error reason=bad-revision rc=2")
            return 2
        return write_census(lane, rev, work, a.write)
    if a.rev:
        rates, body, err = measure(lane, a.rev, work)
        if err:
            print("CENSUS error reason=%s rc=2" % err)
            return 2
        print("CENSUS rev=%s skill=%d/%d corpus=%d/%d lane=%d/%d host_owned=%d" % (
            a.rev, rates["skill"][0], rates["skill"][1], rates["corpus"][0],
            rates["corpus"][1], rates["lane"][0], rates["lane"][1], rates["host_owned"]))
        return 0
    print("CENSUS error reason=usage rc=2")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
