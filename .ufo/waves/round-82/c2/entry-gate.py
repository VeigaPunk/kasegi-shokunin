#!/usr/bin/env python3
"""entry-gate.py — round-82 C2 entry gate (B8): shape limbs G1-G4 plus content limb G5.

Successor of the round-81 B8 gate (.ufo/waves/round-81/c2/entry-gate.py). It reads the entry
against its manifest and snapshot:

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
  G5 content  (round 82; round-81 CriticClaims (d) and MutEntryGate: a labelled six-quote
              dump with empty rule lines passed G1-G4) in every Claim section the text after
              the `Falsifiable rule:` label and the text after the `Rejected
              over-generalization` label each has >= 8 words; the rule text cites a
              `(<SID>.txt:<n>)` location; and neither text is drawn from the source: it
              contains no manifest quote and is not a substring of any snapshot line. A
              Claim section failing any of these counts in `ruleless`.

Output: 'ENTRY-GATE sid=<SID> claims=<c> want=<w> spans=<s> mislocated=<m> overlong=<o>
claimless=<k> unpinned=<u> ruleless=<r> header=<ok|bad>' then 'ENTRY-GATE-RESULT pass|fail'.
Exit 0 on pass, 1 on fail, 2 on a usage or read error.

G5 checks that the rule text exists, is the entry's own words and points at the source; it
does not check that the rule is true or that it follows from the quote.

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
MIN_WORDS = 8


def label_text(body, label_re):
    """Text after the first line matching label_re (the rest of that line), or None."""
    m = re.search(label_re, body, re.M)
    if not m:
        return None
    return body[m.end():].split("\n", 1)[0].strip()


def drawn_from_source(text, quotes, snapshot_lines):
    if any(q in text for q in quotes):
        return True
    return any(text in line for line in snapshot_lines if line.strip())


def content_ok(body, sid, quotes, snapshot_lines):
    rule = label_text(body, r"^Falsifiable rule:")
    rej = label_text(body, r"^Rejected over-generalization[^\n:]*:?")
    if rule is None or rej is None:
        return False
    if len(rule.split()) < MIN_WORDS or len(rej.split()) < MIN_WORDS:
        return False
    if not re.search(r"\b%s\.txt:\d+" % re.escape(sid), rule):
        return False
    return not (drawn_from_source(rule, quotes, snapshot_lines)
                or drawn_from_source(rej, quotes, snapshot_lines))


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
    ruleless = 0
    claim_spans = []
    for body in claims:
        body = body.split("\n## ")[0]
        cs = span_re.findall(body)
        claim_spans.extend(t for t, _n in cs)
        if not (cs and re.search(r"(?m)^Falsifiable rule:", body)
                and re.search(r"(?m)^Rejected over-generalization", body)):
            claimless += 1
        if not content_ok(body, sid, quotes, snapshot_lines):
            ruleless += 1
    unpinned = sum(1 for q in quotes if not any(q in t for t in claim_spans))
    ok = (header and len(claims) == len(quotes) and spans and mislocated == 0 and overlong == 0
          and claimless == 0 and unpinned == 0 and ruleless == 0)
    line = ("ENTRY-GATE sid=%s claims=%d want=%d spans=%d mislocated=%d overlong=%d claimless=%d "
            "unpinned=%d ruleless=%d header=%s"
            % (sid, len(claims), len(quotes), len(spans), mislocated, overlong, claimless,
               unpinned, ruleless, "ok" if header else "bad"))
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
            fh.write("title\nThe sky is blue on clear days.\nWater boils at one hundred degrees.\n"
                     "Clouds are made of tiny water droplets suspended in the air above us.\n")
        man = {"sources": [{"id": "S9", "path": "S9.txt", "quotes": [
            {"quote": "The sky is blue on clear days.", "anchor": 2},
            {"quote": "Water boils at one hundred degrees.", "anchor": 3}]}]}
        mpath = os.path.join(sdir, "manifest.json")
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(man, fh)
        head = ("# t\n\nsource: S9 — u\nverified-at: 2026-11-06\nrecheck: cd %s && python3 "
                "corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/r/"
                "manifest.json --source S9\n\n" % d)
        rule = ("Falsifiable rule: a report that the sky is green on a clear day contradicts "
                "the page (S9.txt:%d).\n\n")
        rej = ("Rejected over-generalization, not a page sentence: the sky is blue at night "
               "and on every cloudy day too.\n\n")
        claim = '## Claim %d — c\n\n"%s" (S9.txt:%d). x\n\n' + rule + rej

        def mk(k, q, n, r=None, j=None):
            body = '## Claim %d — c\n\n"%s" (S9.txt:%d). x\n\n' % (k, q, n)
            return body + (r if r is not None else rule % n) + (j if j is not None else rej)

        q1, q2 = "The sky is blue on clear days.", "Water boils at one hundred degrees."
        good = head + mk(1, q1, 2) + mk(2, q2, 3)
        dump = head + '"%s" (S9.txt:2)\n"%s" (S9.txt:3)\n' % (q1, q2)
        moved = head + mk(1, q1, 3) + mk(2, q2, 3)
        norule = good.replace(rule % 2, "", 1)
        labelled = head + mk(1, q1, 2, "Falsifiable rule:\n\n", "Rejected over-generalization\n\n") \
            + mk(2, q2, 3, "Falsifiable rule:\n\n", "Rejected over-generalization\n\n")
        copied = head + mk(1, q1, 2, "Falsifiable rule: The sky is blue on clear days. (S9.txt:2)"
                           " and more words here\n\n") + mk(2, q2, 3)
        snapline = head + mk(1, q1, 2, "Falsifiable rule: tiny water droplets suspended in the "
                             "air above us\n\n") + mk(2, q2, 3)
        nocite = head + mk(1, q1, 2, "Falsifiable rule: a report that the sky is green on a "
                           "clear day contradicts the page.\n\n") + mk(2, q2, 3)
        shortrej = head + mk(1, q1, 2, None, "Rejected over-generalization: no.\n\n") + mk(2, q2, 3)
        cases = {"good": (good, True), "dump": (dump, False), "moved": (moved, False),
                 "norule": (norule, False), "labelled": (labelled, False),
                 "copied": (copied, False), "snapline": (snapline, False),
                 "nocite": (nocite, False), "shortrej": (shortrej, False)}
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
