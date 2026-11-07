#!/usr/bin/env python3
"""kasegi round-99 C1 instrument — the citation census of record, measured at a
named revision and confined to the measured tree.

Round 98 made the census a reading of a named revision, but its check verified
only the pinned line, its `../` citations resolved against the verifier's
scratch parent (the same revision measured 2589/7961 in a clean work dir and
2591/7961 in a contaminated one), and resolve.py inherited the real HOME — a
`~/Projects/**` recursive glob that earlyoom killed at 2-3.5 GiB. Round 99:

  * CONFINEMENT (R157): an INTERNAL row whose citation walks out with a `..`
    segment and whose resolved path is not under the extract is reclassified
    `HOST-OWNED` and leaves the pinned numerator; it stays in the denominator,
    so the pinned rate is a function of the revision alone.
  * CONFINED HOME: resolve.py runs with HOME=<work>/home, whose `Projects/`
    tree is empty, so no host tree is globbed and the measurement is
    reproducible on any host. `--home real` restores the host reading for an
    ad-hoc host-inclusive number; the census of record always uses `confined`
    and says so in its `home:` line.
  * DIGESTS (R159): the five header lines are bound by `header-sha256` and the
    body by `body-sha256`, so a hand-edited pinned line, host line, host-owned
    count or body fails `--check` even when the pinned line still matches.
  * `--check` never reads the measurement cache: a poisoned cache cannot vouch
    for a census.
  * `--check` requires `measured-at` to be exactly 40 hex and an ancestor of a
    local branch tip; `--write` refuses a revision that is not an ancestor.

Exit: 0 pass, 1 fail, 2 could-not-evaluate (missing input, bad revision,
resolve.py error, no citations).

Usage:
  python3 -B corpus/instruments/census-at-rev.py --lane . --rev <hash> --work <scratch>
  python3 -B corpus/instruments/census-at-rev.py --lane . --write corpus/instruments/citation-survival.md --work <scratch>
  python3 -B corpus/instruments/census-at-rev.py --lane . --check corpus/instruments/citation-survival.md --work <scratch>
"""
import argparse
import hashlib
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

HOME_LINE = "home: confined (empty Projects tree; no host roots)"
PINNED_PREFIX = "pinned rate (INTERNAL only; revision-stable):"
HOST_PREFIX = "host-inclusive rate (resolve.py's definition, confined HOME):"
HOSTOWNED_PREFIX = "host-owned inputs:"
HEADER_FIELDS = ("measured-at:", HOME_LINE.split(":")[0] + ":", PINNED_PREFIX,
                 HOST_PREFIX, HOSTOWNED_PREFIX)
SEPARATOR = "\n---\n\n"


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def pct(n, m):
    return "%.2f%%" % (100.0 * n / m) if m else "n/a"


def home_dir(work):
    h = os.path.join(work, "home")
    os.makedirs(os.path.join(h, "Projects"), exist_ok=True)
    return h


def extract(lane, rev, work):
    # The extract lives under a private parent that holds only the extract, so
    # a `../` walk-out in a citation resolves to an absent path on every host
    # and the body is layout-stable (R157's body half).
    d = os.path.join(work, "extract-" + rev[:12], "tree")
    if os.path.isfile(os.path.join(d, RESOLVE)):
        return d, None
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    p = subprocess.run(["git", "-C", lane, "archive", rev], capture_output=True)
    if p.returncode != 0:
        return None, "bad-revision"
    tf = os.path.join(work, "extract-" + rev[:12] + ".tar")
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


def walkout(citation):
    """True when the citation carries a `..` path segment (a tree walk-out)."""
    return any(seg == ".." for seg in citation.replace("\\", "/").split("/"))


def instrument_digest():
    with open(os.path.abspath(__file__), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def measure(lane, rev, work, cache_ok=True):
    """Return (rates, body, error). Cached per revision + instrument under work/cache."""
    cache = os.path.join(work, "cache", rev + "-" + instrument_digest() + ".json")
    if cache_ok and os.path.isfile(cache):
        with open(cache, encoding="utf-8") as fh:
            c = json.load(fh)
        return c["rates"], c["body"], None
    d, err = extract(lane, rev, work)
    if err:
        return None, None, err
    env = dict(os.environ)
    env["HOME"] = home_dir(work)
    r = sh([sys.executable, "-B", os.path.join(d, RESOLVE), d], env=env)
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
            rows.append((cells[0], cells[-7], cells[-6], cells[-1]))
    if not rows:
        return None, None, "no-rows"

    # R157 confinement: a `..` walk-out that resolves outside the extract is
    # host-dependent, never INTERNAL. It stays in the denominator.
    root = os.path.realpath(d)
    confined = 0
    fixed = []
    for cit, klass, resolved, scopes in rows:
        if klass == "INTERNAL" and walkout(cit):
            rp = os.path.realpath(resolved) if resolved else ""
            if not (rp == root or rp.startswith(root + os.sep)):
                klass = "HOST-OWNED"
                confined += 1
        fixed.append((cit, klass, scopes))
    rows = fixed

    def rate(scope):
        sel = [k for _, k, sc in rows if scope == "ALL" or scope in sc]
        num = [k for k in sel if k == "INTERNAL"]
        return len(num), len(sel)

    def host_incl(scope):
        sel = [k for _, k, sc in rows if scope == "ALL" or scope in sc]
        num = [k for k in sel if k in ("INTERNAL", "RESOLVES", "MIRROR-EQUIVALENT")]
        return len(num), len(sel)

    host_owned = sum(1 for _, k, _ in rows if k in ("RESOLVES", "MIRROR-EQUIVALENT"))
    out = {"rev": rev, "rows": len(rows), "host_owned": host_owned, "confined": confined}
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
    # A host-owned row's occurrence count is a property of the host's file, not
    # of the revision (the watchdog log grows every round), so it is normalised
    # to `-`; the pinned and host-inclusive rates are unaffected (R161).
    norm = []
    for ln in body.split("\n"):
        cells = ln.split("|")
        if len(cells) == 8 and cells[2].strip() in ("RESOLVES", "MIRROR-EQUIVALENT"):
            cells[5] = " - "
            ln = "|".join(cells)
        norm.append(ln)
    body = "\n".join(norm)
    # Neither the extract nor the confined HOME is evidence: both are scratch
    # paths, so the body names a stable token for each (M98-1 class).
    body = body.replace(home_dir(work) + "/", "<confined-home>/")
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
    return ("%s SKILL %d/%d = %s | corpus %d/%d = %s | lane %d/%d = %s" % (
        PINNED_PREFIX,
        rates["skill"][0], rates["skill"][1], pct(*rates["skill"]),
        rates["corpus"][0], rates["corpus"][1], pct(*rates["corpus"]),
        rates["lane"][0], rates["lane"][1], pct(*rates["lane"])))


def host_line(rates):
    return ("%s SKILL %d/%d = %s | corpus %d/%d = %s | lane %d/%d = %s" % (
        HOST_PREFIX,
        rates["skill_host"][0], rates["skill_host"][1], pct(*rates["skill_host"]),
        rates["corpus_host"][0], rates["corpus_host"][1], pct(*rates["corpus_host"]),
        rates["lane_host"][0], rates["lane_host"][1], pct(*rates["lane_host"])))


def host_owned_line(rates):
    return ("%s %d absolute-path citations resolve outside the lane "
            "(reported separately; not revision-stable)" % (HOSTOWNED_PREFIX, rates["host_owned"]))


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def header_lines(rates, rev):
    return ["measured-at: %s" % rev,
            HOME_LINE,
            pinned_line(rates),
            host_line(rates),
            host_owned_line(rates)]


def ancestor_of_tip(lane, rev):
    tips = set()
    p = sh(["git", "-C", lane, "rev-parse", "HEAD"])
    if p.returncode == 0 and p.stdout.strip():
        tips.add(p.stdout.strip())
    p = sh(["git", "-C", lane, "for-each-ref", "--format=%(objectname)", "refs/heads"])
    tips.update(x for x in p.stdout.split() if x)
    for t in tips:
        if sh(["git", "-C", lane, "merge-base", "--is-ancestor", rev, t]).returncode == 0:
            return True
    return False


def write_census(lane, rev, work, out):
    if not ancestor_of_tip(lane, rev):
        print("CENSUS-WRITE error reason=rev-not-ancestor rc=2")
        return 2
    rates, body, err = measure(lane, rev, work)
    if err:
        print("CENSUS-WRITE error reason=%s rc=2" % err)
        return 2
    head = [HEAD, "",
            "Census of record — regenerated in round 99 at the revision below.",
            ""]
    head += header_lines(rates, rev)
    hdr = header_lines(rates, rev)
    head.append("header-sha256: %s" % digest("\n".join(hdr)))
    head.append("body-sha256: %s" % digest(body))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(head) + SEPARATOR + body)
    print("CENSUS-WRITE ok rev=%s skill=%d/%d lane=%d/%d host_owned=%d confined=%d" % (
        rev, rates["skill"][0], rates["skill"][1], rates["lane"][0], rates["lane"][1],
        rates["host_owned"], rates["confined"]))
    return 0


def split_body(text):
    i = text.find(SEPARATOR)
    if i < 0:
        return None
    return text[i + len(SEPARATOR):]


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
    if not ancestor_of_tip(lane, rev):
        print("CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1")
        return 1
    hdr = []
    for field in HEADER_FIELDS:
        mm = re.search(r"^" + re.escape(field) + r"(.+)$", text, re.M)
        if not mm:
            print("CENSUS-CHECK fail reason=no-%s rc=1" % field.rstrip(":").split(" ")[0])
            return 1
        hdr.append(field + mm.group(1))
    stored_h = re.search(r"^header-sha256: ([0-9a-f]{64})$", text, re.M)
    if not stored_h:
        print("CENSUS-CHECK fail reason=no-header-sha rc=1")
        return 1
    if digest("\n".join(hdr)) != stored_h.group(1):
        print("CENSUS-CHECK fail reason=header-sha-mismatch rc=1")
        return 1
    stored_b = re.search(r"^body-sha256: ([0-9a-f]{64})$", text, re.M)
    if not stored_b:
        print("CENSUS-CHECK fail reason=no-body-sha rc=1")
        return 1
    body = split_body(text)
    if body is None:
        print("CENSUS-CHECK fail reason=no-body rc=1")
        return 1
    if digest(body) != stored_b.group(1):
        print("CENSUS-CHECK fail reason=body-sha-mismatch rc=1")
        return 1
    rates, mbody, err = measure(lane, rev, work, cache_ok=False)
    if err:
        print("CENSUS-CHECK fail reason=%s rc=2" % err)
        return 2
    if hdr[2] != pinned_line(rates):
        print("CENSUS-CHECK fail reason=pinned-mismatch rc=1")
        print("  file: %s" % hdr[2])
        print("  rev : %s" % pinned_line(rates))
        return 1
    if hdr[3] != host_line(rates):
        print("CENSUS-CHECK fail reason=host-mismatch rc=1")
        return 1
    if hdr[4] != host_owned_line(rates):
        print("CENSUS-CHECK fail reason=host-owned-mismatch rc=1")
        return 1
    if body != mbody:
        print("CENSUS-CHECK fail reason=body-mismatch rc=1")
        return 1
    print("CENSUS-CHECK pass rev=%s skill=%d/%d corpus=%d/%d lane=%d/%d host_owned=%d confined=%d" % (
        rev, rates["skill"][0], rates["skill"][1], rates["corpus"][0], rates["corpus"][1],
        rates["lane"][0], rates["lane"][1], rates["host_owned"], rates["confined"]))
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
        if not re.fullmatch(r"[0-9a-f]{40}", a.rev):
            print("CENSUS error reason=bad-revision rc=2")
            return 2
        rates, body, err = measure(lane, a.rev, work)
        if err:
            print("CENSUS error reason=%s rc=2" % err)
            return 2
        print("CENSUS rev=%s skill=%d/%d corpus=%d/%d lane=%d/%d host_owned=%d confined=%d" % (
            a.rev, rates["skill"][0], rates["skill"][1], rates["corpus"][0],
            rates["corpus"][1], rates["lane"][0], rates["lane"][1], rates["host_owned"],
            rates["confined"]))
        return 0
    print("CENSUS error reason=usage rc=2")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
