#!/usr/bin/env python3
"""Supplementary boundary probes for the round-96 SentinelShapes review."""
import importlib.util
import os
import re

S = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("landed", os.path.join(S, "scanner-7ef1d36.py"))
landed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(landed)
PATS = landed.patterns()
BY = dict(PATS)

VER = b".ab.cd1234567"
PATV = b"glpat-" + b"A" * 28 + b".de.fg1234567"
PATR = b"glpat-" + b"B" * 28 + b".defg12345"

cases = [
    ("runner glrt- (no r)", b"glrt-" + b"C" * 30 + VER, "gitlab-runner-auth-token-versioned"),
    ("runner glrtr-t2_ partition", b"glrtr-t2_" + b"C" * 27 + VER, "gitlab-runner-auth-token-versioned"),
    ("prefixed ACME-glpat- versioned", b"ACME-" + PATV, "gitlab-pat-versioned"),
    ("prefixed 21-char glpat- versioned", b"P" * 21 + b"-" + PATV, "gitlab-pat-versioned"),
    ("head min 27", b"glpat-" + b"A" * 27 + b".de.fg1234567", "gitlab-pat-versioned"),
    ("head max 300", b"glpat-" + b"A" * 300 + b".de.fg1234567", "gitlab-pat-versioned"),
    ("head 301", b"glpat-" + b"A" * 301 + b".de.fg1234567", "gitlab-pat-versioned"),
    ("routable head min 27", b"glpat-" + b"B" * 27 + b".defg12345", "gitlab-pat-routable"),
    ("routable head 26 (n1 control)", b"glpat-" + b"B" * 26 + b".defg12345", "gitlab-pat-routable"),
    ("versioned at EOF", PATV, "gitlab-pat-versioned"),
    ("routable at EOF", PATR, "gitlab-pat-routable"),
    ("glptt-20 at EOF", b"glptt-" + b"H" * 20, "gitlab-pipeline-trigger-token"),
    ("glptt-40 at EOF", b"glptt-" + b"G" * 40, "gitlab-pipeline-trigger-token"),
    ("glptt-20 then &", b"glptt-" + b"H" * 20 + b"&x=1", "gitlab-pipeline-trigger-token"),
    ("glptt-40 then %26", b"glptt-" + b"G" * 40 + b"%26x=1", "gitlab-pipeline-trigger-token"),
    ("versioned trailing dot", PATV + b".", "gitlab-pat-versioned"),
    ("versioned trailing hyphen", PATV + b"-", "gitlab-pat-versioned"),
    ("versioned trailing underscore", PATV + b"_", "gitlab-pat-versioned"),
    ("glptt-40 trailing hyphen", b"glptt-" + b"G" * 40 + b"-", "gitlab-pipeline-trigger-token"),
    ("versioned after \\u0026", b"q=a\\u0026" + PATV, "gitlab-pat-versioned"),
    ("versioned after %26", b"q=a%26" + PATV, "gitlab-pat-versioned"),
    ("versioned after %3D", b"q=a%3D" + PATV, "gitlab-pat-versioned"),
    ("versioned after &#x26;", b"q=a&#x26;" + PATV, "gitlab-pat-versioned"),
    ("versioned after &#x26 (no semi)", b"q=a&#x26" + PATV, "gitlab-pat-versioned"),
    ("versioned after &#38 (no semi)", b"q=a&#38" + PATV, "gitlab-pat-versioned"),
    ("versioned after \\x26", b"q=a\\x26" + PATV, "gitlab-pat-versioned"),
    ("URL query %2E both dots", b"https://h/p?private_token=" + PATV.replace(b".", b"%2E"), "gitlab-pat-versioned"),
    ("URL query %2e lower", b"https://h/p?private_token=" + PATV.replace(b".", b"%2e"), "gitlab-pat-versioned"),
    ("JSON value \\u002e", b'{"t":"' + PATV.replace(b".", b"\\u002e") + b'"}', "gitlab-pat-versioned"),
    ("HTML &#46;", b"<i>" + PATV.replace(b".", b"&#46;") + b"</i>", "gitlab-pat-versioned"),
    ("uppercase GLPAT-", b"GLPAT-" + b"A" * 28 + b".de.fg1234567", "gitlab-pat-versioned"),
]

print("%-40s %-5s %-5s %s" % ("case", "hit", "span", "shapes"))
for name, payload, want in cases:
    found = landed.scan_bytes(payload, PATS)[0]
    shapes = sorted({s for s, _ in found})
    m = BY[want].search(payload)
    span = "%d-%d" % (m.start(), m.end()) if m else "-"
    print("%-40s %-5s %-5s %s" % (name, "HIT" if want in shapes else "MISS", span, ",".join(shapes) or "-"))
