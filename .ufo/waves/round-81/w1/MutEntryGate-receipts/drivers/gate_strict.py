#!/usr/bin/env python3
"""PROPOSAL SKETCH (not an instrument; never installed). A stricter B8' implementing the
tightenings found by the forgery battery:
  H1 source URL token == manifest url; verified-at date == manifest fetched_utc date.
  G2 every cited span verbatim on its line, no elision marker, <=25 words.
  G3 claim numbers exactly 1..N in order, N == pins; claim k holds exactly one span and it
     equals pin k (text and anchor); rule/rejected payloads >= 6 words.
  F  any (S*.txt:n) for another sid must resolve verbatim in that file beside the manifest.
Usage: entry-gate-strict.py --entry F --manifest F --source SID --lane DIR
"""
import argparse
import json
import os
import re
import sys

SPAN_ANY = re.compile(r'"([^"\n]+)" \(([A-Za-z0-9_.-]+)\.txt:(\d+)\)')


def gate(text, man, sid, lane, snap):
    src = next(s for s in man["sources"] if s["id"] == sid)
    pins = [(q["quote"], q["anchor"]) for q in src["quotes"]]
    lines = text.split("\n")
    head = lines[:8]
    url = src.get("url", "")
    date = (src.get("fetched_utc") or "")[:10]
    recheck = ("recheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest %s "
               "--source %s" % (lane, man["_path"], sid))
    src_line = next((l for l in head if l.startswith("source: %s \u2014 " % sid)), "")
    url_ok = src_line.split("\u2014 ", 1)[1].split()[0] == url if url else False
    ver_line = next((l for l in head if l.startswith("verified-at: ")), "")
    ver_ok = date and ver_line[len("verified-at: "):].strip() == date
    header = bool(url_ok and ver_ok and any(l == recheck for l in head))

    spans = SPAN_ANY.findall(text)
    own = [(t, int(n)) for t, s, n in spans if s == sid]
    foreign = [(t, s, int(n)) for t, s, n in spans if s != sid]
    bad_span = 0
    for t, n in own:
        if not (1 <= n <= len(snap) and t in snap[n - 1]) or len(t.split()) > 25 \
                or t.startswith("\u2026") or t.endswith("\u2026"):
            bad_span += 1
    bad_foreign = 0
    for t, s, n in foreign:
        p = os.path.join(os.path.dirname(man["_path_abs"]), s + ".txt")
        try:
            fl = open(p, encoding="utf-8").read().split("\n")
        except OSError:
            bad_foreign += 1
            continue
        if not (1 <= n <= len(fl) and t in fl[n - 1]):
            bad_foreign += 1

    sections = re.split(r"(?m)^## ", text)
    claims = [s for s in sections if re.match(r"Claim \d+\b", s)]
    nums = [int(re.match(r"Claim (\d+)\b", s).group(1)) for s in claims]
    order_ok = nums == list(range(1, len(pins) + 1))
    bad_claim = 0
    if order_ok:
        for k, body in enumerate(claims, 1):
            cs = [(t, int(n)) for t, n in re.findall(r'"([^"\n]+)" \(%s\.txt:(\d+)\)' % re.escape(sid), body)]
            if not (len(cs) == 1 and cs[0] == (pins[k - 1][0], pins[k - 1][1])):
                bad_claim += 1
    else:
        bad_claim = len(pins)
    bad_marker = 0
    for body in claims:
        m1 = re.search(r"(?m)^Falsifiable rule:(.*)$", body)
        m2 = re.search(r"(?m)^Rejected over-generalization(.*)$", body)
        ok1 = m1 and len(re.sub(r"^[\s:,\u2014-]+", "", m1.group(1)).split()) >= 6
        ok2 = m2 and len(re.sub(r"^[\s:,\u2014-]+", "", m2.group(1)).split()) >= 6
        if not (ok1 and ok2):
            bad_marker += 1
    ok = (header and order_ok and bad_claim == 0 and bad_marker == 0 and bad_span == 0
          and bad_foreign == 0 and bool(own))
    print("ENTRY-GATE-STRICT sid=%s pins=%d claims=%d order=%s url=%s date=%s bad_span=%d "
          "bad_foreign=%d bad_claim=%d bad_marker=%d header=%s" % (
              sid, len(pins), len(claims), order_ok, url_ok, bool(ver_ok), bad_span,
              bad_foreign, bad_claim, bad_marker, "ok" if header else "bad"))
    print("ENTRY-GATE-STRICT-RESULT %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


def main(argv):
    ap = argparse.ArgumentParser()
    for a in ("--entry", "--manifest", "--source", "--lane"):
        ap.add_argument(a)
    a = ap.parse_args(argv)
    man = json.load(open(a.manifest, encoding="utf-8"))
    man["_path"] = os.path.relpath(os.path.abspath(a.manifest), os.path.abspath(a.lane))
    man["_path_abs"] = os.path.abspath(a.manifest)
    src = next(s for s in man["sources"] if s["id"] == a.source)
    snap = open(os.path.join(os.path.dirname(os.path.abspath(a.manifest)), src["path"]),
                encoding="utf-8").read().split("\n")
    text = open(a.entry, encoding="utf-8").read()
    return gate(text, man, a.source, a.lane, snap)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
