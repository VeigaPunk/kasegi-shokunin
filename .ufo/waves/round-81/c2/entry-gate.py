#!/usr/bin/env python3
"""entry-gate.py — round-81 C2 entry-content limb (B8) for one knowledge entry.

Closes the round-79/80 CriticClaims carry-in (d): B0-B7 bind capture fidelity and admission
bookkeeping but never read the entry's claim prose, so a six-quote dump passed them. This
gate reads the entry against its manifest and snapshot:

  G1 header   the first lines carry `source: <SID> — `, `verified-at: ` and exactly
              `recheck: cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
              <manifest> --source <SID>`.
  G2 located  every quoted span written as "<text>" (<SID>.txt:<n>) has <= 25 words and
              occurs verbatim on snapshot line <n>.
  G3 claims   the entry has exactly as many `## Claim <k>` sections as the manifest has
              quotes for <SID>; every such section carries at least one located span, a line
              beginning `Falsifiable rule:` and a line beginning `Rejected over-generalization`.
  G4 pinned   every manifest quote for <SID> occurs verbatim inside some located span of a
              Claim section.

Output: 'ENTRY-GATE sid=<SID> claims=<c> want=<w> spans=<s> mislocated=<m> overlong=<o>
claimless=<k> unpinned=<u> header=<ok|bad>' then 'ENTRY-GATE-RESULT pass|fail'. Exit 0 on
pass, 1 on fail, 2 on a usage or read error.

Usage:
  entry-gate.py --entry FILE --manifest FILE --source SID --lane DIR
  entry-gate.py --selftest
"""
import argparse
import json
import os
import re
import sys
import tempfile

SPAN_RE = r'"([^"\n]+)" \(%s\.txt:(\d+)\)'


def gate(entry_text, manifest, sid, lane, snapshot_lines):
    src = next(s for s in manifest["sources"] if s["id"] == sid)
    quotes = [q["quote"] for q in src["quotes"]]
    span_re = re.compile(SPAN_RE % re.escape(sid))
    lines = entry_text.split("\n")
    head = lines[:8]
    recheck = ("recheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest %s "
               "--source %s" % (lane, manifest["_path"], sid))
    header = (any(l.startswith("source: %s — " % sid) for l in head)
              and any(l.startswith("verified-at: ") for l in head)
              and any(l == recheck for l in head))
    spans = span_re.findall(entry_text)
    mislocated = sum(1 for t, n in spans
                     if not (1 <= int(n) <= len(snapshot_lines) and t in snapshot_lines[int(n) - 1]))
    overlong = sum(1 for t, _n in spans if len(t.split()) > 25)
    sections = re.split(r"(?m)^## ", entry_text)
    claims = [s for s in sections if re.match(r"Claim \d+\b", s)]
    claimless = 0
    claim_spans = []
    for body in claims:
        body = body.split("\n## ")[0]
        cs = span_re.findall(body)
        claim_spans.extend(t for t, _n in cs)
        if not (cs and re.search(r"(?m)^Falsifiable rule:", body)
                and re.search(r"(?m)^Rejected over-generalization", body)):
            claimless += 1
    unpinned = sum(1 for q in quotes if not any(q in t for t in claim_spans))
    ok = (header and len(claims) == len(quotes) and spans and mislocated == 0 and overlong == 0
          and claimless == 0 and unpinned == 0)
    line = ("ENTRY-GATE sid=%s claims=%d want=%d spans=%d mislocated=%d overlong=%d claimless=%d "
            "unpinned=%d header=%s" % (sid, len(claims), len(quotes), len(spans), mislocated,
                                       overlong, claimless, unpinned, "ok" if header else "bad"))
    return ok, line


def load(entry, manifest_path, sid, lane):
    with open(entry, encoding="utf-8") as fh:
        text = fh.read()
    with open(manifest_path, encoding="utf-8") as fh:
        man = json.load(fh)
    man["_path"] = os.path.relpath(os.path.abspath(manifest_path), os.path.abspath(lane))
    src = next(s for s in man["sources"] if s["id"] == sid)
    snap = os.path.join(os.path.dirname(os.path.abspath(manifest_path)), src["path"])
    with open(snap, encoding="utf-8") as fh:
        snap_lines = fh.read().split("\n")
    return text, man, snap_lines


def selftest():
    d = tempfile.mkdtemp(prefix="entry-gate-selftest-", dir=os.environ.get("TMPDIR") or None)
    try:
        sdir = os.path.join(d, "corpus", "source-snapshots", "r")
        os.makedirs(sdir)
        with open(os.path.join(sdir, "S9.txt"), "w", encoding="utf-8") as fh:
            fh.write("title\nThe sky is blue on clear days.\nWater boils at one hundred degrees.\n")
        man = {"sources": [{"id": "S9", "path": "S9.txt", "quotes": [
            {"quote": "The sky is blue on clear days.", "anchor": 2},
            {"quote": "Water boils at one hundred degrees.", "anchor": 3}]}]}
        mpath = os.path.join(sdir, "manifest.json")
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(man, fh)
        head = ("# t\n\nsource: S9 — u\nverified-at: 2026-11-06\nrecheck: cd %s && python3 "
                "corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/r/"
                "manifest.json --source S9\n\n" % d)
        claim = ('## Claim %d — c\n\n"%s" (S9.txt:%d). x\n\nFalsifiable rule: y\n\n'
                 'Rejected over-generalization, not a page sentence: z\n\n')
        good = head + claim % (1, "The sky is blue on clear days.", 2) + claim % (
            2, "Water boils at one hundred degrees.", 3)
        dump = head + '"The sky is blue on clear days." (S9.txt:2)\n"Water boils at one hundred degrees." (S9.txt:3)\n'
        moved = head + claim % (1, "The sky is blue on clear days.", 3) + claim % (
            2, "Water boils at one hundred degrees.", 3)
        norule = good.replace("Falsifiable rule: y\n\nRejected", "Rejected", 1)
        cases = {"good": (good, True), "dump": (dump, False), "moved": (moved, False),
                 "norule": (norule, False)}
        got = {}
        for name, (text, _want) in cases.items():
            p = os.path.join(d, name + ".md")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
            t, m, s = load(p, mpath, "S9", d)
            got[name] = gate(t, m, "S9", d, s)[0]
        okk = all(got[n] is w for n, (_t, w) in cases.items())
        print("entry-gate selftest %s got=%s" % ("ok" if okk else "FAIL", got))
        return 0 if okk else 1
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry")
    ap.add_argument("--manifest")
    ap.add_argument("--source")
    ap.add_argument("--lane")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.entry and a.manifest and a.source and a.lane):
        print("entry-gate: --entry, --manifest, --source and --lane are required", file=sys.stderr)
        return 2
    try:
        text, man, snap = load(a.entry, a.manifest, a.source, a.lane)
    except (OSError, ValueError, StopIteration) as exc:
        print("entry-gate: cannot read inputs: %r" % (exc,), file=sys.stderr)
        return 2
    ok, line = gate(text, man, a.source, a.lane, snap)
    print(line)
    print("ENTRY-GATE-RESULT %s" % ("pass" if ok else "fail"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
