#!/usr/bin/env python3
"""Round-97 structural redaction of credential-shaped fixture literals in the
round-96 wave receipts (R146 rule applied to wave evidence).

The round-97 C2 landing's clean-run limb (K2) found 56 (file, shape) hits in
`.ufo/waves/round-96/w1/**-receipts/`: the mutation campaign's mutant sources
(copies of the instrument, whose selftest table carries synthetic credential
literals) and the independent probe's generated fixtures. Each matched value is
replaced in place by `[<shape>-fixture-redacted-r97]`; line numbering is
preserved and a per-file, per-shape count is written to the receipt.

Usage: redact-r97.py LANE RECEIPT [ROOT]   (ROOT defaults to .ufo/waves)
"""
import hashlib
import importlib.util
import os
import sys

LANE = None


def load_scanner(lane):
    path = os.path.join(lane, "corpus", "instruments", "capture-secret-scan.py")
    spec = importlib.util.spec_from_file_location("scanner_r97_redact", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    lane, receipt = argv[:2]
    lane = os.path.abspath(lane)
    mod = load_scanner(lane)
    pats = mod.patterns()
    root = os.path.join(lane, argv[2]) if len(argv) > 2 else os.path.join(lane, ".ufo", "waves")
    targets = []
    for dp, dns, fns in os.walk(root):
        dns.sort()
        for fn in sorted(fns):
            rel = os.path.relpath(os.path.join(dp, fn), lane)
            if mod.is_capture_path(rel):
                targets.append(rel)
    lines = ["# round-97 redaction of wave receipts (structural, R146)",
             "root=%s files=%d" % (root, len(targets))]
    total = 0
    for rel in targets:
        p = os.path.join(lane, rel)
        before = open(p, "rb").read()
        data = before
        counts = []
        for name, pat in pats:
            n = 0

            def sub(m, name=name):
                nonlocal n
                n += 1
                return ("[%s-fixture-redacted-r97]" % name).encode()

            data = pat.sub(sub, data)
            if n:
                counts.append("%s=%d" % (name, n))
                total += n
        if data != before:
            open(p, "wb").write(data)
            lines.append("%s before=%s after=%s %s" % (
                rel, hashlib.sha256(before).hexdigest()[:16],
                hashlib.sha256(data).hexdigest()[:16], ",".join(counts)))
    lines.append("REDACTION-RESULT files=%d values=%d" % (len(targets), total))
    text = "\n".join(lines) + "\n"
    print(text, end="")
    if receipt:
        with open(receipt, "w", encoding="utf-8") as fh:
            fh.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
