#!/usr/bin/env python3
"""Build the round-58 S091 manifest from the committed capture bytes."""
import hashlib, json, re, sys

SNAP = "corpus/source-snapshots/round-58/S091.txt"
URL = "https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing"

raw = open(SNAP, "rb").read()
text = raw.decode("utf-8")
lines = text.splitlines()
norm = lambda s: re.sub(r"\s+", " ", s)
full = norm(text)

QUOTES = [
    ("Q1", 1,  "How fast is autonomous AI cyber capability advancing? | AISI Work"),
    ("Q2", 14, "already an acceleration from our November 2025 estimate of 8 months"),
    ("Q3", 21, "We deliberately constrain our setup to only 2.5M tokens per task to make results comparable over time."),
    ("Q4", 23, "This is an imperfect model, and is not a future prediction, nor a fixed law."),
    ("Q5", 25, "had doubled every 4.7 months since reasoning models emerged in late 2024"),
    ("Q6", 30, "Any single omission only shifts the pre-Mythos doubling time estimate to a minimum of 4.1 months, and a maximum of 5.0 months."),
    ("Q7", 34, "solving the range \u201cThe Last Ones\u201d in 6 of 10 attempts and the previously unsolved \u201cCooling Tower\u201d in 3 of 10 attempts"),
    ("Q8", 45, "The AI Security Institute is a research organisation within the Department of Science, Innovation and Technology."),
    ("Q9", 14, "It is unclear whether this represents a new, faster trend."),
]

fail = 0
for qid, anchor, quote in QUOTES:
    if norm(quote) not in norm(lines[anchor - 1]):
        print(f"{qid}: NOT-AT-ANCHOR {anchor}"); fail += 1
    n = full.count(norm(quote))
    w = len(quote.split())
    print(f"{qid}: occurrences={n} words={w} anchor={anchor}")
    if n != 1 or w > 25:
        fail += 1
if fail:
    sys.exit("manifest assertions failed")

manifest = {
    "schema_version": 1,
    "note": ("Round 58 (2026-11-03). S091 = the UK AI Security Institute's own blog report "
             "'How fast is autonomous AI cyber capability advancing?' (May 13, 2026) - the "
             "first-party measurement record of the rate of autonomous AI cyber capability "
             "progress: the 4.7-month 80%-reliability cyber time-horizon doubling estimate "
             "(February 2026, accelerated from the November 2025 estimate of 8 months), the "
             "bounded measurement method (narrow cyber suite, expert-time baselines, 80% "
             "threshold, 2.5M token cap for comparability that understates capability), the "
             "stated uncertainty band, and the cyber-range results (first completion of both "
             "ranges). First admission of the recorded AISI lead (corpus/SOURCES.md Leads, "
             "named in the round-52 through round-57 SCORECARD planned rows). Capture method: "
             "the committed instrument capture-source.py opened the page directly "
             "(status=200; no fallback needed, R66 not triggered)."),
    "sources": [
        {
            "id": "S091",
            "url": URL,
            "capture_url": URL,
            "http": {"status": 200, "final_url": URL},
            "kind": "html",
            "fetch_method": ("capture-source.py default urllib open, status=200 at this host "
                             "(the iso.org Cloudflare block of round 57 does not apply here); "
                             "two same-sha opens recorded (probe 20:35:32Z, recorded + "
                             "verification re-open 20:35:59Z)"),
            "fetched_utc": "2026-11-03T20:35:59Z",
            "path": "S091.txt",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "snapshot_bytes": len(raw),
            "lines": len(lines),
            "body_lines": [1, len(lines)],
            "quotes": [
                {"id": qid, "anchor": anchor, "quote": quote}
                for qid, anchor, quote in QUOTES
            ],
        }
    ],
}
out = "corpus/source-snapshots/round-58/manifest.json"
with open(out, "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print("wrote", out, "sha256", hashlib.sha256(raw).hexdigest(), "bytes", len(raw), "lines", len(lines))
