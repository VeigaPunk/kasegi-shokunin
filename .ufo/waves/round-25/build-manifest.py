#!/usr/bin/env python3
"""Build corpus/source-snapshots/round-25/manifest.json from the round's capture set.

The quote lists are written by the two entry scribes
(.ufo/waves/round-25/wave1/quotes-vendor-jp.json, quotes-vendor-cisco.json); this
script binds each quote to the committed snapshot's sha256 so
corpus/instruments/source-recheck.py can assert them offline.

  python3 .ufo/waves/round-25/build-manifest.py [--write]

Without --write it prints the manifest to stdout for review.
"""
import hashlib
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
SNAP = os.path.join(LANE, "corpus/source-snapshots/round-25")
W1 = os.path.join(LANE, ".ufo/waves/round-25/wave1")
QUOTE_LISTS = ["quotes-vendor-jp.json", "quotes-vendor-cisco.json"]
PURPOSE = (
    "Round-25 captures for the F10 admission (vendor-side disclosure policies as corpus "
    "objects). Each snapshot is the text capture-source.py wrote on 2026-10-25T08:14Z; the "
    "sha256 binds those bytes and the quotes are asserted against them by "
    "corpus/instruments/source-recheck.py."
)


def sha256(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def main(argv):
    by_source = {}
    for name in QUOTE_LISTS:
        path = os.path.join(W1, name)
        if not os.path.exists(path):
            print("missing quote list: %s" % path, file=sys.stderr)
            return 2
        data = json.load(open(path, encoding="utf-8"))
        for record in data.get("records", []):
            source = record["source"]
            entry = by_source.setdefault(source, {"quotes": [], "entries": []})
            entry["entries"].append(data.get("entry", "?"))
            for quote in record.get("quotes", []):
                item = {"id": quote["id"], "quote": quote["quote"], "location": quote.get("location", "")}
                if quote.get("anchor") is not None:
                    item["anchor"] = quote["anchor"]
                entry["quotes"].append(item)

    sources = []
    for source in sorted(by_source):
        snapshot = os.path.join(SNAP, source + ".txt")
        if not os.path.exists(snapshot):
            print("missing snapshot for %s: %s" % (source, snapshot), file=sys.stderr)
            return 2
        sources.append(
            {
                "id": source,
                "path": source + ".txt",
                "sha256": sha256(snapshot),
                "quotes": by_source[source]["quotes"],
            }
        )
    manifest = {"schema_version": 1, "purpose": PURPOSE, "sources": sources}
    text = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    if "--write" in argv:
        target = os.path.join(SNAP, "manifest.json")
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)
        print("wrote %s sources=%d quotes=%d" % (target, len(sources), sum(len(s["quotes"]) for s in sources)))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
