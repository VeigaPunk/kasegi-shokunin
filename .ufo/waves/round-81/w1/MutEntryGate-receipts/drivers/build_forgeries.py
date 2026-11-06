#!/usr/bin/env python3
"""Build forged entries that satisfy B8's lexical limbs while carrying no verifiable
claim prose. Reads the frozen manifest for exact quote bytes; writes into $S/forgeries."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MAN = os.path.join(LANE, "corpus/source-snapshots/round-81/manifest.json")
GATE = os.path.join(S, "gate.py")
OUT = os.path.join(S, "forgeries")
os.makedirs(OUT, exist_ok=True)

man = json.load(open(MAN, encoding="utf-8"))
src = man["sources"][0]
qs = [(q["id"], q["quote"], q["anchor"]) for q in src["quotes"]]
Q = {i: qs[i-1][1] for i in range(1, len(qs)+1)}
A = {i: qs[i-1][2] for i in range(1, len(qs)+1)}
snap = open(os.path.join(os.path.dirname(MAN), src["path"]), encoding="utf-8").read().split("\n")

HEAD = (
    "# FORGED entry — passes B8\n\n"
    "source: S115 — https://example.invalid/definitely-not-the-osv-page\n"
    "verified-at: 1970-01-01\n"
    "recheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest "
    "corpus/source-snapshots/round-81/manifest.json --source S115\n\n" % LANE)


def span(text, line):
    return '"%s" (S115.txt:%d)' % (text, line)


def claim(n, body):
    return "## Claim %d — c\n\n%s\n" % (n, body)


MARKERS = "Falsifiable rule: x\n\nRejected over-generalization\n\nTODO: filler, no content.\n\n"

entries = {}


def W(name, text):
    p = os.path.join(OUT, name + ".md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    entries[name] = p


# F1 boilerplate: one pin per claim, markers present, prose is a fixed placeholder.
W("f1_boilerplate", HEAD + "".join(
    claim(i, "%s\n\nlorem ipsum dolor sit amet.\n\n%s" % (span(Q[i], A[i]), MARKERS))
    for i in range(1, 7)))

# F2 dump: all six pins crammed into Claim 1; Claims 2-6 are stubs with a one-word span.
W("f2_dump_stubclaims", HEAD + claim(1, "\n".join(span(Q[i], A[i]) for i in range(1, 7)) + "\n\n" + MARKERS) +
  "".join(claim(i, '%s\n\nnone\n\n%s' % (span("the", 36), MARKERS)) for i in range(2, 7)))

# F3 semantic inversion: pristine quoted bytes, claim prose asserts the opposite.
inv = {
    1: "The endpoint reports every record, whether it passes or fails the checks.",
    2: "Anyone may call this endpoint; it is the public vulnerability feed for scanners.",
    3: "Records below the quality bar are repaired and imported after review.",
    4: "The call takes a JSON body with package, version and source parameters.",
    5: "The source may be passed as a query-string parameter to the stable v1 prefix.",
    6: "The source value is the record-id prefix used by the source's advisories.",
}
W("f3_semantic_inversion", HEAD + "".join(
    claim(i, "%s\n\n%s\n\nFalsifiable rule: none — nothing here is checkable.\n\n"
             "Rejected over-generalization\n\n" % (span(Q[i], A[i]), inv[i]))
    for i in range(1, 7)))

# F4 truncated fragments: pins in Claim 1; Claims 2-6 quote <=25-word verbatim
# fragments that drop the subject or the modality of the sentence.
frag = {
    2: ("operators of home databases that OSV.dev imports from", 32),
    3: ("do not meet OSV.dev’s quality bar (and therefore have not been imported)", 34),
    4: ("in order to construct the URL", 36),
    5: ("https://api.osv.dev/v1experimental/importfindings/{source}", 37),
    6: ("the name value in source.yaml", 38),
}
W("f4_truncated_fragments", HEAD + claim(1, "\n".join(span(Q[i], A[i]) for i in (1, 2, 3, 4, 5, 6)) + "\n\n" + MARKERS) +
  "".join(claim(i, "%s\n\nunsupported assertion.\n\n%s" % (span(*frag[i]), MARKERS))
          for i in range(2, 7)))

# F5 anti-case: paraphrase cited on the right line.
W("f5_paraphrase_mislocated", HEAD + "".join(
    claim(i, '"Records that fail the checks are repaired and imported." (S115.txt:%d)\n\n%s'
          % (A[i], MARKERS)) for i in range(1, 7)))

# F6 anti-case: pristine quote cited on the wrong line.
W("f6_moved_line", HEAD + claim(1, "%s\n\n%s" % (span(Q[1], 34), MARKERS)) + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MARKERS)) for i in range(2, 7)))

# F7 duplicate numbering: six sections all titled Claim 1.
W("f7_duplicate_numbering", HEAD + "".join(
    claim(1, "%s\n\n%s" % (span(Q[i], A[i]), MARKERS)) for i in range(1, 7)))

# F8 empty markers: the required lines exist with no content at all.
W("f8_empty_markers", HEAD + "".join(
    claim(i, '%s\n\nFalsifiable rule:\n\nRejected over-generalization\n\n'
              % span(Q[i], A[i])) for i in range(1, 7)))

# F9 fabricated provenance: wrong URL, empty access date.
W("f9_fake_provenance", HEAD.replace("verified-at: 1970-01-01", "verified-at: ") + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MARKERS)) for i in range(1, 7)))

# F10 bare: no Attribution, Limits, Distinctness or Gate section at all; only the six
# pins and twelve marker lines.
W("f10_bare_no_prose", HEAD + "".join(
    claim(i, '%s\n\nFalsifiable rule:\n\nRejected over-generalization\n\n'
              % span(Q[i], A[i])) for i in range(1, 7)))

# F11 cross-clause permutation: each claim carries a different clause's pin.
perm = [4, 5, 6, 1, 2, 3]
W("f11_cross_clause", HEAD + "".join(
    claim(i, "%s\n\nClause %d is quoted here.\n\n%s" % (span(Q[perm[i - 1]], A[perm[i - 1]]), i, MARKERS))
    for i in range(1, 7)))

# F12 foreign-source citations are ignored wholesale.
W("f12_foreign_citations", HEAD + "".join(
    claim(i, '%s\n\n"%s" (S113.txt:999)\n\n%s' % (span(Q[i], A[i]), "fabricated", MARKERS))
    for i in range(1, 7)))

# F15 anti-case: a 26-word verbatim span on line 32 exceeds the cap.
words = snap[31].split()[:26]
over = " ".join(words)
assert over in snap[31]
W("f15_overlong_span", HEAD + claim(1, "%s\n\n%s" % (span(over, 32), MARKERS)) + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MARKERS)) for i in range(2, 7)))

# F16 anti-case: one pin quoted six times, five pins never inside a Claim section.
W("f16_repeat_one_pin", HEAD + "".join(
    claim(i, "%s\n\n%s" % (span(Q[1], A[1]), MARKERS)) for i in range(1, 7)))

# --- run the frozen gate on each ---
rows = []
for name, path in entries.items():
    r = subprocess.run([sys.executable, GATE, "--entry", path, "--manifest", MAN,
                        "--source", "S115", "--lane", LANE],
                       capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
    out = (r.stdout or "").strip().split("\n")
    print("%-26s rc=%d %s | %s" % (name, r.returncode,
                                   out[-1] if out else "",
                                   out[0] if out else (r.stderr or "").strip()[:200]))
    rows.append({"name": name, "rc": r.returncode, "verdict": out[-1] if out else "",
                 "line": out[0] if out else "", "stderr": (r.stderr or "").strip()})

# --- synthetic anchor cross-check: manifest anchor vs cited line ---
fx = os.path.join(S, "fixture")
os.makedirs(os.path.join(fx, "corpus/source-snapshots/r"), exist_ok=True)
with open(os.path.join(fx, "corpus/source-snapshots/r/S9.txt"), "w", encoding="utf-8") as fh:
    fh.write("title\nThe sky is blue on clear days.\nfiller\nmore\n"
             "The sky is blue on clear days.\n")
with open(os.path.join(fx, "corpus/source-snapshots/r/manifest.json"), "w", encoding="utf-8") as fh:
    json.dump({"sources": [{"id": "S9", "path": "S9.txt", "quotes": [
        {"quote": "The sky is blue on clear days.", "anchor": 2}]}]}, fh)
fxhead = ("# t\n\nsource: S9 — u\nverified-at: 2026-11-06\nrecheck: cd %s && python3 "
          "corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/r/"
          "manifest.json --source S9\n\n" % fx)
text = fxhead + claim(1, '"The sky is blue on clear days." (S9.txt:5)\n\nFalsifiable rule:\n\n'
                         'Rejected over-generalization\n')
p = os.path.join(fx, "anchor_off.md")
open(p, "w", encoding="utf-8").write(text)
r = subprocess.run([sys.executable, GATE, "--entry", p, "--manifest",
                    os.path.join(fx, "corpus/source-snapshots/r/manifest.json"),
                    "--source", "S9", "--lane", fx],
                   capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
print("%-26s rc=%d %s | %s" % ("f13_anchor_mismatch(syn)", r.returncode,
                               (r.stdout or "").strip().split("\n")[-1],
                               (r.stdout or "").strip().split("\n")[0]))
rows.append({"name": "f13_anchor_mismatch_synthetic", "rc": r.returncode,
             "verdict": (r.stdout or "").strip().split("\n")[-1],
             "line": (r.stdout or "").strip().split("\n")[0], "stderr": ""})
json.dump(rows, open(os.path.join(S, "forgeries.json"), "w"), indent=1)
