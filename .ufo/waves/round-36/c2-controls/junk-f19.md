# Exploit Prediction Scoring System (EPSS) — junk twin (do-nothing control for C2)

This file is a **fabricated fixture**, not a knowledge entry. It carries the
same *shape* as the claimed F19 admission (H1 header, `source:` line citing
S053, a `recheck:` line) but quotes a sentence that does **not** exist in the
pinned capture, and it declares no manifest record. It exists to prove the F19
admission gate rejects a construction the shape counters cannot see.

source: S053 — https://www.first.org/epss/ — capture corpus/source-snapshots/round-36/S053.txt (244 lines; sha256 4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9): model definition L216, probability/percentiles L217, maintenance L235
verified-at: 2026-10-26
ground: F19
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053   # fixture line: it names the real recheck of S053, so it cannot itself be the gate; the gate is the pinned comparison in the control receipt, which prints MISMATCH reason=quote-not-found on the sentence below

## What this adds

> "EPSS guarantees exploitation within 30 days for every scored CVE." — L216 (fabricated anchor)

The fabricated sentence replaces FIRST's probabilistic statement (L216:
"estimates the probability that a published CVE will be exploited in the wild
in the next 30 days") with a guarantee. The twin also claims that S053 "scores
CVSS severity rather than exploitation likelihood", which the capture does not
say anywhere.

[FABRICATED — the quoted strings above are fabrications, and the admission gate
must reject this entry. Per-string occurrence counts in the pinned capture are
measured and recorded in the control seat receipt
`.ufo/waves/round-36/wave1/ExecC2JunkControl.md`; this file asserts nothing
about them.]
