# FirstTimes — S018 timelines-negotiation sentence and section

- Seat: `KasegiR23.FirstTimes-5`, read-only (no production edit, no subagent dispatch, no admission claim).
- Source: S018 `https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1`
- Opened live: 2026-10-20T21:42:40Z (server `date:` header); body read and raw HTML captured 2026-10-20T21:44Z.
- Axes served: `depth:verifiability` (byte-locatable quote, version discrepancy, recheck that fails closed) and `coverage` F06 (load-bearing timeline quote for S018).
- Question answered: is the timelines-negotiation sentence and its section exactly as attributed, and does the S018 row hold? **Yes, with two recorded traps.**

## 1. Answer — exact located quote

Verbatim sentence in the page body (12 words, ≤25):

> All parties should clearly and securely communicate and negotiate expectations and timelines.

Location (heading chain, verified by byte order in the live HTML, not by memory):

`Guiding Concepts and Best Current Practices` (H2) → `Maintain clear and consistent communications` (H3) → `Prior to disclosure` (bold sub-label) → **first bullet of that list**.

Heading-tag nuance: `<h2…>Guiding Concepts and Best Current Practices</h2>` occurs exactly once, but the bare phrase occurs twice — the second is prose in the Use Case 2 introduction (`…collected into the concluding section: Guiding Concepts and Best Current Practices.`). An assertion on the bare H2 phrase therefore matches 2; assert the heading tag.

Byte anchor in the raw capture: the sentence is the `<li>` immediately after `<p><strong>Prior to disclosure</strong></p>\n<ul>\n<li>` and is terminated by `</li>`; the next `<li>` is "Vendors should provide currently accepted contact mechanisms…".

## 2. Date / version

- Body banner: `Version 1.1` and `Released Spring, 2020` (two lines, immediately under the H1). The URL slug is `guidelines-v1.1`.
- **No ISO release day is stated anywhere on the page.** A `YYYY-MM-DD` scan (`grep -o -E "20[0-9]{2}-[0-9]{2}-[0-9]{2}"`) returns no match, and `grep -oE "[^<>]{0,60}2020[^<>]{0,60}"` returns exactly one line: `Released Spring, 2020`. Do not invent a month/day.
- HTTP `last-modified: Mon, 26 Jan 2026 14:43:46 GMT` — page modification, **not** the release date. `content-length: 94680`; no `ETag` header observed.
- **Trap:** `<title>` and `og:title` both say `… - version 1.0` (2 occurrences of `version 1.0` versus 1 of `Version 1.1`). A recheck that greps the HTML title records the wrong version. The authoritative marker is the body H1 block, not metadata.

## 3. S018 row verdict (existing row, `corpus/SOURCES.md:24`)

Row anchor: `Guiding Concepts and Best Current Practices; version 1.1, released Spring 2020`. **Confirmed correct** as section and version; it is the exact H2 that contains the quote.

Row `teaches`: `…clear contacts, negotiated timelines and shared disclosure expectations.` — **the string `negotiated timelines` occurs 0 times in the document.** This is a summary, not a quotation; it must never be presented as a verbatim quote. The verbatim support for the timelines point is the sentence in §1.

The `opened` field says `2026-10-19`; this seat re-opened the page `2026-10-20`, one day later. That is a re-open date, not a contradiction.

## 4. Detector caveat — the phrase is not unique, the sentence is

`negotiate expectations and timelines` occurs **twice**:

| Full sentence (verbatim) | Location | Selected |
|---|---|---|
| All parties should clearly and securely communicate and negotiate expectations and timelines. | H2 Guiding Concepts… → H3 Maintain clear and consistent communications → Prior to disclosure, bullet 1 | **yes** |
| Both parties (vendor and finder) should clearly communicate and negotiate expectations and timelines and acknowledge receipt of each communication. | Use Case 2 → Variant 5: Vendor does not remediate a reported vulnerability → Prevention, last bullet (the `Prevention` label is emitted malformed inside the last Causes `<li>`: `…vulnerability.\nPrevention</li>`) | no |
| Vendor should negotiate an agreed time frame with affected stakeholders prior to vulnerability disclosure. | Use Case 2 → Variant 3: Missing communication between upstream and downstream vendors → Response | no |
| Vendor should negotiate and try to meet timelines and be responsive. | Use Case 2 → Variant 7: Coordinator makes vulnerability details public prior to remediation → Prevention | no |

A substring assertion on `negotiate expectations and timelines` passes at two sites. A manifest/quote assertion must use the **full 12-word sentence** (count = 1 in raw HTML) or the site pair.

## 5. Recheck — executable now, fails closed

Local pinned snapshot `corpus/source-snapshots/round-23/S018.txt`:
- sha256 `d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4`, 8372 bytes, 86 lines — matches `.ufo/waves/round-23/opened-source-snapshots.json` (declared kind: `normalized public-doc reader excerpt; not raw HTTP bytes`).
- Line 36 is exactly `- All parties should clearly and securely communicate and negotiate expectations and timelines.` (`exact_match True`).
- It **starts at `## Definitions`** and ends at `### Use coordinators when appropriate`; it carries **neither** the `Version 1.1` / `Released Spring, 2020` banner **nor** the Use Case 2/3 sections. So a snapshot-only recheck cannot verify the version/date claim, and cannot see the near-duplicate sentence.
- It is **untracked** at frozen base `922a4dde90b60b465e2b8b241d1fe363f1f27e98` (`git status --short` → `?? corpus/source-snapshots/round-23/`). A frozen-base anchor cannot open it.

Canonical recheck — stdlib only, embedded here so it survives scratch loss (`/fast/scratch/kasegi-r23-firsttimes/s018_recheck.py`, copied verbatim):

```python
#!/usr/bin/env python3
"""S018 timeline-negotiation quote recheck. Exit 0 clean, 1 mismatch, 2 unavailable.

--file PATH  verify a captured page body against the pinned sha256 and assertions.
(no args)     fetch the official URL and run the same content assertions.
"""
import argparse
import hashlib
import sys
import urllib.request

URL = "https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1"
Q = "All parties should clearly and securely communicate and negotiate expectations and timelines."
PIN = "94febe95b8182ff362508a68f1939cead6499e02e042cb593099bfbf954ff5bb"


def load(path):
    if path:
        try:
            raw = open(path, "rb").read()
        except OSError as exc:
            print("UNAVAILABLE", exc)
            sys.exit(2)
        digest = hashlib.sha256(raw).hexdigest()
        if digest != PIN:
            print("MISMATCH sha256", digest)
            sys.exit(1)
        print("PASS sha256_pin")
        return raw.decode("utf-8", "replace")
    try:
        return urllib.request.urlopen(URL, timeout=30).read().decode("utf-8", "replace")
    except Exception as exc:  # network failure is unavailable, never clean
        print("UNAVAILABLE", exc)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file")
    args = ap.parse_args()
    b = load(args.file)
    h3 = b.find("Maintain clear and consistent communications</h3>")
    label = b.find("<strong>Prior to disclosure</strong>")
    q = b.find(Q)
    checks = {
        "quote_once": b.count(Q) == 1,
        "phrase_twice": b.count("negotiate expectations and timelines") == 2,
        "h3_unique": b.count("Maintain clear and consistent communications</h3>") == 1,
        "order_h3_label_quote": -1 < h3 < label < q,
        "quote_first_li": "<p><strong>Prior to disclosure</strong></p>\n<ul>\n<li>" + Q in b,
        "version_v1_1": "Version 1.1" in b,
        "released_spring_2020": "Released Spring, 2020" in b,
        "title_says_v1_0": "version 1.0</title>" in b,
        "negotiated_timelines_absent": "negotiated timelines" not in b,
    }
    for name, ok in checks.items():
        print(("PASS" if ok else "FAIL"), name)
    ok = all(checks.values())
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
```

Observed runs, 2026-10-20T21:44–21:47Z:

| Mode | Result | Exit |
|---|---|---|
| live fetch | all nine `PASS`, `OK` | 0 |
| `--file /fast/scratch/kasegi-r23-firsttimes/first-s018.html` (sha256 `94febe95…f5bb`, 94680 bytes) | `PASS sha256_pin` + all nine `PASS`, `OK` | 0 |
| `--file /tmp/does-not-exist.html` | `UNAVAILABLE [Errno 2] No such file or directory` | 2 |
| `--file` a 1-byte corrupt file | `MISMATCH sha256 2d711642…4881` | 1 |

The absent and corrupt controls are the fail-closed evidence: a missing base never reports clean. `title_says_v1_0` is asserted deliberately — it pins the stale-metadata trap rather than hiding it; the version claim rests on the body assertions.

**Blocking caveat for the draft entry:** `corpus/knowledge/multiparty-vulnerability-coordination.md:4` declares
`recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018`.
At 2026-10-20T21:44Z `test -e` found both paths absent. On re-check at 2026-10-20T21:47:10Z the instrument is present (`corpus/instruments/source-recheck.py`, 9408 bytes, sha256 `f743942d9643c930453c415414fd4468486140049541e3f7babc935581ae888d`) but `corpus/source-snapshots/round-23/manifest.json` is still absent; running the declared command exits **2** with `manifest UNAVAILABLE reason=missing`. The fail-closed path works, but the draft entry cannot yet claim a clean recheck; until the manifest lands, the embedded `s018_recheck.py` above is the executable evidence for S018. Instrument ownership is the `RecheckSources` seat (`.ufo/waves/round-23/build-spec.json`); this seat made no edit to it.

## 6. Independent check of the sibling draft (not authored here)

`corpus/knowledge/multiparty-vulnerability-coordination.md` (untracked, mtime 18:42) already carries the §1 sentence in its Evidence table. The **quote text is verbatim and correct**, and the listed location `Maintain clear and consistent communications — Prior to disclosure` is accurate. It omits the parent H2; no other section in this document has this H3/sub-label pair, so it is unambiguous, but the full chain `Guiding Concepts and Best Current Practices → Maintain clear and consistent communications → Prior to disclosure` is the exact location for Q3. That file is sibling-owned; this seat records the check and makes no edit.

## 7. Falsifiable findings

1. The 12-word sentence occurs exactly once in the live HTML body; the 4-word phrase `negotiate expectations and timelines` occurs twice. Falsified by `grep -o '…' file | wc -l` returning anything else.
2. The sentence is the first `<li>` under `Prior to disclosure`, whose parent H3 is `Maintain clear and consistent communications` under H2 `Guiding Concepts and Best Current Practices`. Falsified by byte-position order failing or a different enclosing list.
3. The page states `Version 1.1` / `Released Spring, 2020` in the body while `<title>`/`og:title` state `version 1.0`. Falsified by the title reading 1.1 or the body reading 1.0.
4. `negotiated timelines` is absent from the document. Falsified by any occurrence.
5. The pinned S018 snapshot contains the sentence at line 36 but no version/date banner. Falsified by `grep -n "Version 1.1" corpus/source-snapshots/round-23/S018.txt` returning a line.
6. The draft entry's declared recheck command exits 2 at 2026-10-20T21:47:10Z because `manifest.json` is absent, while the instrument itself is present. Falsified by the command exiting 0.

## 8. Scope limits

- Read-only; this seat wrote only this report. No production, registry, entry, instrument or manifest edit; no git commit/push; no tool installs (nothing needed, so nothing recorded).
- Covers only the timelines-negotiation sentence/section and the S018 row's version/date attribution. It does **not** validate F06's role definitions, F06 admission, the other five quotes in the sibling draft, or S022/S024.
- `SOURCE` metadata (`version 1.0` title, `nginx`/`last-modified` 2026-01-26) is observed as served; whether FIRST ever published a v1.0 and forgot to update the title cannot be resolved from this page alone — remaining unknown, not inferred.
- Live-change monitoring after 2026-10-20T21:44Z is out of scope; the 180d cadence on S018 is the L1 decision.
