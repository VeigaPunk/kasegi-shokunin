#!/usr/bin/env python3
"""Independent round-89 C1 re-measurement (seat ExecC1Indep, kasegi r89 w1).

Recomputes the knowledge-scope meter from corpus/instruments/resolve.py
primitives (collect/classify) over the corpus/knowledge/*.md scope at two
revisions, both read with `git show` (the working tree is never read), WITHOUT
importing the frozen round-89 counter .ufo/waves/round-89/c1/knowledge-meter.py.

Prints:
  - non-GONE/distinct rate at base-rev and after-rev (claim: 777/1798 -> 785/1797)
  - removed and added token sets vs the frozen repair map
  - line-diff check: every changed line equals its base line under exactly the
    9 backticked map substitutions (chained AND single-pass regex)
  - M4/M5-style binding and range checks recomputed from the map
  - M9 re-check from an independent parse of labels.tsv against the round-88
    non-author review at --review-rev

Usage:
  python3 indep_meter.py --lane LANE --base-rev REV --after-rev REV \
      --map MAP.json --labels LABELS.tsv --work DIR [--review-rev REV] \
      [--expect-base N/D] [--expect-after N/D]
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

KEY_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$")
VAL_RE = re.compile(
    r"^corpus/knowledge/([A-Za-z0-9][A-Za-z0-9._-]*\.md)(?::(\d+)(?:-(\d+))?)?$"
)
ANCHOR_RE = re.compile(r":(\d+)(?:-(\d+))?$")
REVIEW_PATH = ".ufo/waves/round-88/w1/ReviewC1Semantics.md"
EXPECT_BASE = "777/1798"
EXPECT_AFTER = "785/1797"


def git_out(lane, *args, binary=False):
    r = subprocess.run(
        ["git", "-C", lane, *args], capture_output=True, check=False
    )
    if r.returncode != 0:
        sys.exit(
            "git -C %s %s failed rc=%d: %s"
            % (lane, " ".join(args), r.returncode, r.stderr.decode(errors="replace").strip())
        )
    return r.stdout if binary else r.stdout.decode("utf-8")


def scope_files(lane, rev):
    out = git_out(lane, "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge")
    return sorted(ln for ln in out.splitlines() if ln.endswith(".md"))


def materialize(lane, rev, dest):
    """Copy the corpus/knowledge/*.md scope of rev into dest via git show."""
    files = scope_files(lane, rev)
    for rel in files:
        blob = git_out(lane, "show", "%s:%s" % (rev, rel), binary=True)
        p = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(blob)
    return files


def load_resolve(path):
    spec = importlib.util.spec_from_file_location("resolve_indep", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify_all(resolve, tree, lane, mirror):
    """Return {token: class} for every distinct citation collect() finds in tree."""
    _, cites = resolve.collect(tree)
    out = {}
    for tok in sorted(cites):
        cls, _p, _m, _dom = resolve.classify(tok, lane, mirror)
        out[tok] = cls
    return out


def rate(cls_map):
    total = len(cls_map)
    gone = sum(1 for c in cls_map.values() if c == "GONE")
    return total - gone, total


def parse_map(path):
    with open(path, "r", encoding="utf-8") as fh:
        m = json.load(fh)
    assert isinstance(m, dict) and m, "map is not a non-empty object"
    for k, v in m.items():
        if not KEY_RE.match(k):
            sys.exit("map key malformed: %r" % k)
        if not VAL_RE.match(v):
            sys.exit("map value malformed: %r" % v)
    return m


def parse_labels(path):
    """Independent parse: key, value, review-line, class per row; # comments."""
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\n")
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) != 4:
                sys.exit("labels row does not have 4 tab fields: %r" % ln)
            rows.append(
                {
                    "key": parts[0].strip(),
                    "value": parts[1].strip(),
                    "review_line": int(parts[2].strip()),
                    "class": parts[3].strip(),
                }
            )
    return rows


def anchor_of(token):
    m = ANCHOR_RE.search(token)
    if not m:
        return None, None
    n = int(m.group(1))
    mm = int(m.group(2)) if m.group(2) else None
    return n, mm


def whole_token(line, tok):
    return re.search(r"(?<![0-9A-Za-z_/-])" + re.escape(tok) + r"(?![0-9A-Za-z_-])", line)


def check_m9(rows, map_, lane, review_rev):
    problems = []
    detail = []
    lpairs = {r["key"]: r["value"] for r in rows}
    if lpairs == map_:
        detail.append("map==labels: yes (%d pairs)" % len(lpairs))
    else:
        only_map = sorted(set(map_) - set(lpairs))
        only_lab = sorted(set(lpairs) - set(map_))
        val_diff = sorted(k for k in set(map_) & set(lpairs) if map_[k] != lpairs[k])
        problems.append(
            "map!=labels only_map=%s only_labels=%s value_diff=%s"
            % (only_map, only_lab, val_diff)
        )
    review = git_out(lane, "show", "%s:%s" % (review_rev, REVIEW_PATH)).splitlines()
    for r in rows:
        key, val, no, cls = r["key"], r["value"], r["review_line"], r["class"]
        if not (1 <= no <= len(review)):
            problems.append("%s: review line %d out of range (file has %d)" % (key, no, len(review)))
            continue
        line = review[no - 1]
        errs = []
        if ("| %s |" % key) not in line:
            errs.append("no cell | %s |" % key)
        if cls == "WRONG":
            if "**WRONG" not in line:
                errs.append("no **WRONG marker")
        elif cls == "FN":
            if "proxy false negative" not in line:
                errs.append("no 'proxy false negative' marker")
            kn, km = anchor_of(key)
            vn, vm = anchor_of(val)
            if (kn, km) != (vn, vm):
                errs.append("FN value anchor %s != key anchor %s" % ((vn, vm), (kn, km)))
        else:
            errs.append("unknown class %r" % cls)
        vn, vm = anchor_of(val)
        tok = ("L%d-%d" % (vn, vm)) if vm else ("L%d" % vn)
        if not whole_token(line, tok):
            errs.append("no whole token %s" % tok)
        detail.append(
            "L%-4d %-34s %-5s %s%s" % (no, key, cls, "OK" if not errs else "FAIL " + "; ".join(errs), "")
        )
        if errs:
            problems.append("%s: %s" % (key, "; ".join(errs)))
    return problems, detail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--after-rev", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--review-rev", default="d0d9f49241420456f2373f62e417f8fa56a0f7d5")
    ap.add_argument("--expect-base", default=EXPECT_BASE)
    ap.add_argument("--expect-after", default=EXPECT_AFTER)
    args = ap.parse_args()

    lane = os.path.abspath(args.lane)
    if not os.path.isdir(os.path.join(lane, ".git")):
        sys.exit("--lane must be a checkout with .git: %s" % lane)

    resolve_path = os.path.join(lane, "corpus", "instruments", "resolve.py")
    resolve = load_resolve(resolve_path)
    mirror = os.path.expanduser(getattr(resolve, "MIRROR_ROOT"))

    work = os.path.abspath(args.work)
    base_tree = os.path.join(work, "base")
    after_tree = os.path.join(work, "after")
    base_files = materialize(lane, args.base_rev, base_tree)
    after_files = materialize(lane, args.after_rev, after_tree)

    base_cls = classify_all(resolve, base_tree, lane, mirror)
    after_cls = classify_all(resolve, after_tree, lane, mirror)

    bn, bd = rate(base_cls)
    an, ad = rate(after_cls)
    exp_bn, exp_bd = (int(x) for x in args.expect_base.split("/"))
    exp_an, exp_ad = (int(x) for x in args.expect_after.split("/"))
    print("RATE base=%d/%d expect=%s %s" % (bn, bd, args.expect_base, "AGREE" if (bn, bd) == (exp_bn, exp_bd) else "DISAGREE"))
    print("RATE after=%d/%d expect=%s %s" % (an, ad, args.expect_after, "AGREE" if (an, ad) == (exp_an, exp_ad) else "DISAGREE"))

    map_ = parse_map(args.map)
    keys = set(map_)
    vals = set(map_.values())
    removed = set(base_cls) - set(after_cls)
    added = set(after_cls) - set(base_cls)
    print("TOKENS removed=%d %s" % (len(removed), "AGREE (== map keys)" if removed == keys else "DISAGREE"))
    if removed != keys:
        print("  removed-only:", sorted(removed - keys))
        print("  keys-not-removed:", sorted(keys - removed))
    print("TOKENS added=%d %s" % (len(added), "AGREE (subset of map values)" if added <= vals else "DISAGREE"))
    if not added <= vals:
        print("  stray added:", sorted(added - vals))
    print("TOKENS added-set:", json.dumps(sorted(added), ensure_ascii=False))
    unrepaired = {k for k in keys if k in after_cls}
    print("TOKENS unrepaired_keys_in_after=%d %s" % (len(unrepaired), "AGREE (0)" if not unrepaired else "DISAGREE"))

    # line-diff check (M3 semantics, recomputed)
    problems = []
    if base_files != after_files:
        problems.append("scope file sets differ")
    keys_by_len = sorted(keys, key=len, reverse=True)
    alt = "|".join(re.escape("`%s`" % k) for k in keys_by_len)
    single_re = re.compile(alt)
    keys_hit = {k: False for k in keys}
    files_compared = 0
    bad_lines = 0
    for rel in base_files:
        b = open(os.path.join(base_tree, rel), "r", encoding="utf-8").read().splitlines()
        a = open(os.path.join(after_tree, rel), "r", encoding="utf-8").read().splitlines()
        if len(b) != len(a):
            problems.append("%s: line count %d -> %d" % (rel, len(b), len(a)))
            continue
        files_compared += 1
        for i, (bl, al) in enumerate(zip(b, a), 1):
            for k in keys:
                if ("`%s`" % k) in bl:
                    keys_hit[k] = True
            chained = bl
            for k in keys_by_len:
                chained = chained.replace("`%s`" % k, "`%s`" % map_[k])
            single = single_re.sub(lambda m: "`%s`" % map_[m.group(0)[1:-1]], bl)
            if al != chained or al != single:
                bad_lines += 1
                if len(problems) < 10:
                    problems.append("%s:%d differs (chained=%s single=%s)" % (rel, i, al == chained, al == single))
    missed = sorted(k for k, hit in keys_hit.items() if not hit)
    print(
        "LINES files=%d bad_lines=%d keys_hit=%d/%d %s"
        % (files_compared, bad_lines, len(keys) - len(missed), len(keys), "AGREE (only the 9 substitutions)" if not problems and not missed and bad_lines == 0 else "DISAGREE")
    )
    for p in problems:
        print("  " + p)
    if missed:
        print("  keys never present in base scope:", missed)

    # M4-style binding + M5-style range checks
    m4 = []
    tracked = git_out(lane, "ls-tree", "-r", "--name-only", args.after_rev).splitlines()
    for k, v in sorted(map_.items()):
        if base_cls.get(k) != "GONE":
            m4.append("key %s not GONE in base scope (class=%s)" % (k, base_cls.get(k)))
        m = VAL_RE.match(v)
        name = m.group(1)
        cand = [t for t in tracked if os.path.basename(t) == name and not t.startswith(".ufo/")]
        if cand != ["corpus/knowledge/" + name]:
            m4.append("value %s: tracked basenames outside .ufo/ = %s" % (v, cand))
        if after_cls.get(v) != "INTERNAL":
            m4.append("value %s not INTERNAL in after scope (class=%s)" % (v, after_cls.get(v)))
        n, mm = anchor_of(v)
        if n is not None:
            lc = len(open(os.path.join(after_tree, "corpus/knowledge/" + name), "r", encoding="utf-8").read().splitlines())
            if not (1 <= n <= (mm or n) <= lc):
                m4.append("value %s range out of file (%d lines)" % (v, lc))
    print("BINDING problems=%d %s" % (len(m4), "AGREE" if not m4 else "DISAGREE"))
    for p in m4:
        print("  " + p)

    # M9 re-check
    rows = parse_labels(args.labels)
    m9p, m9d = check_m9(rows, map_, lane, args.review_rev)
    print("LABELS rows=%d %s" % (len(rows), "AGREE (9/9 bound)" if len(rows) == 9 and not m9p else "DISAGREE"))
    for d in m9d:
        print("  " + d)
    for p in m9p:
        print("  PROBLEM " + p)

    ok = (
        (bn, bd) == (exp_bn, exp_bd)
        and (an, ad) == (exp_an, exp_ad)
        and removed == keys
        and added <= vals
        and not unrepaired
        and not problems
        and not missed
        and bad_lines == 0
        and not m4
        and len(rows) == 9
        and not m9p
    )
    print("INDEP-METER-RESULT %s" % ("pass" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
