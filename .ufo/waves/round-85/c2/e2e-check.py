#!/usr/bin/env python3
"""kasegi round-85 C2 counter: one end-to-end priced claim package.

Usage:
  python3 e2e-check.py --lane LANE --pkg PKG_DIR [--work DIR]
  python3 e2e-check.py --lane LANE --pricing-only REPORT_MD

Inputs it trusts (committed lane bytes, read from LANE):
  corpus/source-snapshots/round-85/manifest.json   S119/S120/S121 sha256 records
  corpus/source-snapshots/round-85/S119.txt        HackerOne JSON record, report 1913733
  corpus/source-snapshots/round-85/S120.txt        curl advisory CVE-2023-28319
  corpus/source-snapshots/round-85/S121.txt        curl vulnerability-disclosure policy
  corpus/source-snapshots/round-35/S052.txt        CISA KEV catalog capture (F18)
  corpus/instruments/claim-package-check.py        the r43 eight-rule package gate

The package's report.md must carry a `## Pricing` section whose machine lines
are `price-<field>: <value>` (one per line). The counter re-derives every value
from the snapshots above and compares:

  severity               == S119 severity_rating == the S120 `Severity: X` value
                           (case-insensitive)
  reward-at-disclosure   == the S120 `Bug bounty: ...` value, verbatim
  platform-bounty-flag   == S119 `has_bounty?` as `true`/`false`
  reward-current-policy  == `none` iff S121 says "There is no bug bounty"
  cvss                   == `not-set-by-vendor` iff S121 says "We do not support CVSS"
  kev                    starts `not-listed` iff the S119 CVE id occurs 0 times
                         in the S052 capture, else starts `listed`
  cve                    == S119 cve_ids[0]

Limbs (one LIMB line each, then E2E-RESULT):
  E1 gate      claim-package-check.py PKG exits 0 and prints verdict=WELL-FORMED
  E2 evidence  PKG/evidence/manifest.json lists artifacts whose bytes equal the
               committed S119.txt and S120.txt and whose recorded sha256 equals
               the round-85 manifest sha256 for that source
  E3 pricing   every field above present and equal to its derivation
  E4 quotes    report.md `## Pricing` holds >= 3 lines starting `> `; each quote
               (whitespace-collapsed) occurs in S119, S120 or S121
  E5 logged    LOG.md and SHONEN.md in LANE both name PKG's lane-relative path

--pricing-only runs E3 and E4 on one report.md (the pre-freeze forgery
controls use it). Exit 0 only when every limb run holds; 1 on a failed limb;
2 on usage. Unreadable input fails its limb closed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

FIELDS = ("severity", "reward-at-disclosure", "platform-bounty-flag",
          "reward-current-policy", "cvss", "kev", "cve")


def rd(p, mode="r"):
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def derive(lane):
    d = os.path.join(lane, "corpus", "source-snapshots")
    s119 = json.loads(rd(os.path.join(d, "round-85", "S119.txt")))
    s120 = rd(os.path.join(d, "round-85", "S120.txt"))
    s121 = rd(os.path.join(d, "round-85", "S121.txt"))
    kev = rd(os.path.join(d, "round-35", "S052.txt"))
    sev = re.search(r"^Severity: (\S+)\s*$", s120, re.M)
    bb = re.search(r"^Bug bounty: (.+?)\s*$", s120, re.M)
    cve = s119["cve_ids"][0]
    return {
        "severity": s119["severity_rating"].lower() if sev and sev.group(1).lower() == s119["severity_rating"].lower() else None,
        "reward-at-disclosure": bb.group(1) if bb else None,
        "platform-bounty-flag": "true" if s119["has_bounty?"] is True else "false",
        "reward-current-policy": "none" if "There is no bug bounty" in s121 else "SOME",
        "cvss": "not-set-by-vendor" if "We do not support CVSS" in s121 else "SET",
        "kev": "not-listed" if kev.count(cve) == 0 else "listed",
        "cve": cve,
    }, (json.dumps(s119), s120, s121)


def pricing(lane, report):
    out = []
    try:
        want, snaps = derive(lane)
        text = rd(report)
    except Exception as e:
        return [("E3", False, "read:%s" % type(e).__name__), ("E4", False, "read")]
    m = re.search(r"^## Pricing\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    sec = m.group(1) if m else ""
    got = {}
    for line in sec.split("\n"):
        mm = re.match(r"^price-([a-z-]+):\s*(.+?)\s*$", line)
        if mm:
            got.setdefault(mm.group(1), mm.group(2))
    bad = []
    for f in FIELDS:
        g, w = got.get(f), want[f]
        if g is None or w is None:
            bad.append(f)
        elif f == "kev":
            if not g.startswith(w) or (w == "listed" and g.startswith("not-listed")):
                bad.append(f)
        elif f == "severity":
            if g.lower() != w:
                bad.append(f)
        elif g != w:
            bad.append(f)
    out.append(("E3", m is not None and not bad, "section=%s bad=%s" % (m is not None, ",".join(bad) or "none")))
    quotes = [ln[2:] for ln in sec.split("\n") if ln.startswith("> ")]
    pool = [norm(s) for s in snaps]
    miss = [q for q in quotes if not any(norm(q) in p for p in pool)]
    out.append(("E4", len(quotes) >= 3 and not miss, "quotes=%d missing=%d" % (len(quotes), len(miss))))
    return out


def full(lane, pkg):
    limbs = []
    gate = os.path.join(lane, "corpus", "instruments", "claim-package-check.py")
    try:
        p = subprocess.run([sys.executable, "-B", gate, pkg], capture_output=True, text=True, timeout=120)
        ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout
        limbs.append(("E1", ok, "gate_rc=%d" % p.returncode))
    except Exception as e:
        limbs.append(("E1", False, "gate:%s" % type(e).__name__))
    try:
        man = json.loads(rd(os.path.join(lane, "corpus", "source-snapshots", "round-85", "manifest.json")))
        rec = {s["id"]: s["sha256"] for s in man["sources"]}
        pm = json.loads(rd(os.path.join(pkg, "evidence", "manifest.json")))
        found = set()
        for art in pm.get("artifacts", []):
            ap = os.path.join(pkg, "evidence", art.get("path", ""))
            if not os.path.isfile(ap) or os.path.islink(ap):
                continue
            b = rd(ap, "rb")
            h = hashlib.sha256(b).hexdigest()
            for sid in ("S119", "S120"):
                snap = rd(os.path.join(lane, "corpus", "source-snapshots", "round-85", sid + ".txt"), "rb")
                if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:
                    found.add(sid)
        limbs.append(("E2", found == {"S119", "S120"}, "bound=%s" % (",".join(sorted(found)) or "none")))
    except Exception as e:
        limbs.append(("E2", False, "read:%s" % type(e).__name__))
    limbs += pricing(lane, os.path.join(pkg, "report.md"))
    try:
        rel = os.path.relpath(os.path.realpath(pkg), os.path.realpath(lane))
        log = rd(os.path.join(lane, "LOG.md"))
        sh = rd(os.path.join(lane, "SHONEN.md"))
        ok = not rel.startswith("..") and rel in log and rel in sh
        limbs.append(("E5", ok, "rel=%s log=%s shonen=%s" % (rel, rel in log, rel in sh)))
    except Exception as e:
        limbs.append(("E5", False, "read:%s" % type(e).__name__))
    return limbs


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--pkg")
    ap.add_argument("--pricing-only")
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    if a.pricing_only:
        limbs = pricing(lane, a.pricing_only)
    elif a.pkg:
        limbs = full(lane, os.path.abspath(a.pkg))
    else:
        print("E2E-RESULT error reason=usage rc=2")
        return 2
    for n, ok, det in limbs:
        print("LIMB %s %s %s" % (n, "pass" if ok else "FAIL", det))
    allok = all(ok for _, ok, _ in limbs)
    print("E2E-RESULT %s limbs=%d rc=%d" % ("pass" if allok else "fail", len(limbs), 0 if allok else 1))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
