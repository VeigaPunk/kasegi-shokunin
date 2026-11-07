#!/usr/bin/env python3
"""kasegi round-86 C2 counter: a subject-bound, payer-resolved priced claim package.

Usage:
  python3 e2e-check.py --lane LANE --pkg PKG_DIR
  python3 e2e-check.py --lane LANE --pricing-only REPORT_MD

Subject: HackerOne report 1997312 (team `ibb`, the Internet Bug Bounty record
for CVE-2023-28319). The package resolves the field the round-85 package left
open ("No captured record shows who paid it").

Inputs it trusts (committed lane bytes, read from LANE):
  corpus/source-snapshots/round-86/manifest.json   S122/S123 sha256 records
  corpus/source-snapshots/round-86/S122.txt        HackerOne JSON record, report 1997312
  corpus/source-snapshots/round-86/S123.txt        curl maintainer post, 2026-01-26
  corpus/source-snapshots/round-85/S120.txt        curl advisory CVE-2023-28319
  corpus/source-snapshots/round-85/S121.txt        curl vulnerability-disclosure policy
  corpus/source-snapshots/round-35/S052.txt        CISA KEV catalog capture (F18)
  corpus/instruments/claim-package-check.py        the r43 eight-rule package gate

report.md must carry exactly one `## Pricing` section whose machine lines are
`price-<field>: <value>`, each field at most once. Derivations:

  program               == S122 team.handle                          (`ibb`)
  payer                 == `internet-bug-bounty` iff S122 team.handle is `ibb`
                           AND S123 carries "Internet Bug Bounty project, which
                           has paid the bounties for us"
  severity              == S122 severity_rating == S120 `Severity: X` (case-insensitive)
  reward-at-disclosure  == the S120 `Bug bounty: ...` value, verbatim
  platform-bounty-flag  == S122 `has_bounty?` as `true`/`false`
  original-report       == the id N in S122's "The original submission can be
                           found here: https://hackerone.com/reports/N", and
                           S120 carries `Original report: https://hackerone.com/reports/N`
  reward-current-policy == `ended 2026-01-31` iff S123 carries "It officially
                           stops on January 31, 2026." AND S121 carries
                           "There is no bug bounty"
  kev                   starts `not-listed` iff the S122 CVE id occurs 0 times
                        in the S052 capture, else starts `listed`
  cve                   == S122 cve_ids[0]

Limbs (one LIMB line each, then E2E-RESULT):
  E0 subject   report.md line 1 is a `# ` heading naming `1997312` and the CVE;
               report.md names https://hackerone.com/reports/1997312; every
               hackerone.com/reports/<N> in report.md is 1997312 or the derived
               original-report id
  E1 gate      claim-package-check.py PKG exits 0 and prints verdict=WELL-FORMED
  E2 evidence  PKG/evidence/manifest.json lists artifacts whose bytes equal the
               committed S122.txt and S123.txt and whose recorded sha256 equals
               the round-86 manifest sha256 for that source
  E3 pricing   exactly one `## Pricing` heading; no price field repeated; every
               field above present and equal to its derivation
  E4 quotes    the Pricing section holds >= 3 lines starting `> `; each quote,
               whitespace-collapsed, is >= 20 characters and occurs in S120,
               S121, S122 or S123; at least one occurs in S123
  E5 logged    LOG.md and SHONEN.md in LANE both name PKG's lane-relative path

--pricing-only runs E0, E3 and E4 on one report.md. Exit 0 only when every limb
run holds; 1 on a failed limb; 2 on usage. Unreadable input fails its limb
closed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SUBJECT = "1997312"
FIELDS = ("program", "payer", "severity", "reward-at-disclosure", "platform-bounty-flag",
          "original-report", "reward-current-policy", "kev", "cve")
PAYER_LINE = "Internet Bug Bounty project, which has paid the bounties for us"
END_LINE = "It officially stops on January 31, 2026."
MIN_QUOTE = 20


def rd(p, mode="r"):
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def derive(lane):
    d = os.path.join(lane, "corpus", "source-snapshots")
    s122_raw = rd(os.path.join(d, "round-86", "S122.txt"))
    s122 = json.loads(s122_raw)
    s123 = rd(os.path.join(d, "round-86", "S123.txt"))
    s120 = rd(os.path.join(d, "round-85", "S120.txt"))
    s121 = rd(os.path.join(d, "round-85", "S121.txt"))
    kev = rd(os.path.join(d, "round-35", "S052.txt"))
    sev = re.search(r"^Severity: (\S+)\s*$", s120, re.M)
    bb = re.search(r"^Bug bounty: (.+?)\s*$", s120, re.M)
    orig = re.search(r"The original submission can be found here: https://hackerone\.com/reports/(\d+)",
                     s122.get("vulnerability_information", ""))
    orig_id = orig.group(1) if orig and ("Original report: https://hackerone.com/reports/%s" % orig.group(1)) in s120 else None
    handle = (s122.get("team") or {}).get("handle")
    cve = s122["cve_ids"][0]
    want = {
        "program": handle,
        "payer": "internet-bug-bounty" if handle == "ibb" and PAYER_LINE in s123 else None,
        "severity": s122["severity_rating"].lower() if sev and sev.group(1).lower() == s122["severity_rating"].lower() else None,
        "reward-at-disclosure": bb.group(1) if bb else None,
        "platform-bounty-flag": "true" if s122["has_bounty?"] is True else "false",
        "original-report": orig_id,
        "reward-current-policy": "ended 2026-01-31" if END_LINE in s123 and "There is no bug bounty" in s121 else None,
        "kev": "not-listed" if kev.count(cve) == 0 else "listed",
        "cve": cve,
    }
    return want, s122_raw, (s120, s121, s122_raw, s123)


def subject(lane, report):
    try:
        want, _, _ = derive(lane)
        text = rd(report)
    except Exception as e:
        return ("E0", False, "read:%s" % type(e).__name__)
    first = text.split("\n", 1)[0]
    head_ok = first.startswith("# ") and SUBJECT in first and want["cve"] in first
    url_ok = ("https://hackerone.com/reports/%s" % SUBJECT) in text
    ids = set(re.findall(r"hackerone\.com/reports/(\d+)", text))
    allowed = {SUBJECT, want["original-report"]}
    stray = sorted(ids - allowed)
    ok = head_ok and url_ok and not stray
    return ("E0", ok, "heading=%s url=%s stray=%s" % (head_ok, url_ok, ",".join(stray) or "none"))


def pricing(lane, report):
    out = []
    try:
        want, _, snaps = derive(lane)
        text = rd(report)
    except Exception as e:
        return [("E3", False, "read:%s" % type(e).__name__), ("E4", False, "read")]
    heads = re.findall(r"^## Pricing\s*$", text, re.M)
    m = re.search(r"^## Pricing\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    sec = m.group(1) if m else ""
    got, dup = {}, []
    for line in sec.split("\n"):
        mm = re.match(r"^price-([a-z-]+):\s*(.+?)\s*$", line)
        if mm:
            if mm.group(1) in got:
                dup.append(mm.group(1))
            got[mm.group(1)] = mm.group(2)
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
    ok = len(heads) == 1 and not dup and not bad
    out.append(("E3", ok, "sections=%d dup=%s bad=%s" % (len(heads), ",".join(sorted(set(dup))) or "none", ",".join(bad) or "none")))
    quotes = [norm(ln[2:]) for ln in sec.split("\n") if ln.startswith("> ")]
    pool = [norm(s) for s in snaps]
    short = [q for q in quotes if len(q) < MIN_QUOTE]
    miss = [q for q in quotes if not any(q in p for p in pool)]
    from_s123 = [q for q in quotes if len(q) >= MIN_QUOTE and q in pool[3]]
    ok4 = len(quotes) >= 3 and not short and not miss and bool(from_s123)
    out.append(("E4", ok4, "quotes=%d short=%d missing=%d s123=%d" % (len(quotes), len(short), len(miss), len(from_s123))))
    return out


def full(lane, pkg):
    limbs = [subject(lane, os.path.join(pkg, "report.md"))]
    gate = os.path.join(lane, "corpus", "instruments", "claim-package-check.py")
    try:
        p = subprocess.run([sys.executable, "-B", gate, pkg], capture_output=True, text=True, timeout=120)
        ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout
        limbs.append(("E1", ok, "gate_rc=%d" % p.returncode))
    except Exception as e:
        limbs.append(("E1", False, "gate:%s" % type(e).__name__))
    try:
        man = json.loads(rd(os.path.join(lane, "corpus", "source-snapshots", "round-86", "manifest.json")))
        rec = {s["id"]: s["sha256"] for s in man["sources"]}
        pm = json.loads(rd(os.path.join(pkg, "evidence", "manifest.json")))
        found = set()
        for art in pm.get("artifacts", []):
            ap = os.path.join(pkg, "evidence", art.get("path", ""))
            if not os.path.isfile(ap) or os.path.islink(ap):
                continue
            b = rd(ap, "rb")
            h = hashlib.sha256(b).hexdigest()
            for sid in ("S122", "S123"):
                snap = rd(os.path.join(lane, "corpus", "source-snapshots", "round-86", sid + ".txt"), "rb")
                if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:
                    found.add(sid)
        limbs.append(("E2", found == {"S122", "S123"}, "bound=%s" % (",".join(sorted(found)) or "none")))
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
    a = ap.parse_args(argv)
    lane = os.path.abspath(a.lane)
    if a.pricing_only:
        limbs = [subject(lane, a.pricing_only)] + pricing(lane, a.pricing_only)
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
