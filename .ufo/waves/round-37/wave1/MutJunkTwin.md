# MutJunkTwin — C2 adversarial junk-twin set for F20 (SSVC): four construction classes, all rejected, one needed anchor identified (round 37, C2 / coverage)

Seat: `MutJunkTwin-2` (leaf, mutation-tester). Item: generate adversarial junk-twin **variants** for C2 that
must be rejected — (1) real SSVC words mixed with a fabricated guarantee; (2) a sentence attributed to SSVC
but only present on the GitHub README, not the docs capture; (3) a near-miss quote with one word changed;
(4) a quote that occurs twice in the page (needs anchor) — run `source-recheck` on scratch manifests against
the live page, expect rejection or identify the needed anchor; deliver the twin set + transcripts.

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(claims freeze `224df74d…`; claims-erratum 1 `b3620681` read, not edited). Write scope honoured: **no lane
file was written except this receipt**; all work copies and transcripts lived under
`/fast/scratch/hyaku/kasegi-r37/MutJunkTwin-2/` (removed before yield — quiescence E9 safe). Only read-only
git (`rev-parse`, `log`, `show --stat`, `ls-tree`, `status`) was run. No tool was installed or upgraded.

Result in one line: all four twin constructions are **rejected** by the committed
`corpus/instruments/source-recheck.py` (sha256 `fd2e01e8…b9c003`, scratch copy byte-identical) against live
fetches of the erratum-1 URL — three as `MISMATCH reason=quote-not-found`, the duplicate as
`MISMATCH reason=occurrence-not-unique` — and the needed anchor for the duplicate is **any line anchor in
296–299 (Supplier Utility table) or 386–389 (Deployer restatement)**, verified `anchor=N-ok` at 296, 299,
386, 389 and `anchor-broken` at 295 and 250.

---

## 1. Pins — live fetches the twins were tested against

Captured with the lane's own instrument so the normalization is exactly what `source-recheck.py` applies:

```
$ python3 <scratch>/instr/capture-source.py --id S054 --url https://certcc.github.io/SSVC/tutorials/ssvc_overview/ --out <scratch>/overview/S054.txt --kind html
S054 status=200 fetched_bytes=143053 snapshot_bytes=32623 sha256=ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21 utc=2026-10-26T17:15:32Z
$ python3 <scratch>/instr/capture-source.py --id S054 --url https://certcc.github.io/SSVC/ --out <scratch>/home/S054.txt --kind html
S054 status=200 fetched_bytes=105807 snapshot_bytes=7730 sha256=a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56 utc=2026-10-26T17:15:32Z
$ python3 <scratch>/instr/capture-source.py --id S054 --url https://raw.githubusercontent.com/CERTCC/SSVC/main/README.md --out <scratch>/readme/S054.txt --kind text
S054 status=200 fetched_bytes=6731 snapshot_bytes=6645 sha256=0e8ebdc1d962e537dc5a7531516d0b240cbf81518180f4e16f36188d0db14d89 utc=2026-10-26T17:15:32Z
```

| capture | url | snapshot_bytes | sha256 |
|---|---|---|---|
| primary pin (erratum 1 URL) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 32623 | `ff3f3b2c…5fdce21` |
| home-page control | `https://certcc.github.io/SSVC/` | 7730 | `a6613315…ce58bb56` |
| GitHub README (raw) | `https://raw.githubusercontent.com/CERTCC/SSVC/main/README.md` | 6645 | `0e8ebdc1…0db14d89` |

The overview fetch is **byte-identical** to seat `ExecC2JunkControl`'s 17:02:19Z fetch and seat
`ExecC2QuoteOnce`'s 17:02:11Z fetch (same `snapshot_bytes=32623`, same sha256) — three independent fetches
tonight, identical bytes; the page is stable and my twins are tested against the same bytes the round-37
manifest work pins. Each scratch manifest mirrors the committed round-36 manifest schema (`schema_version`,
`sources[]` with `id/path/url/fetched_utc/fetched_bytes/snapshot_bytes/lines/sha256/normalized/http/quotes[]`),
so `capture-binding-check.py`'s `url`/`fetched_utc` fields are present. Manifest sha256s:
`manifest-twins.json dd572659…186e2d`, `manifest-t4-anchor299.json 9e89dc03…4ce0d8`,
`manifest-genuine.json b8423a27…c1a105`, `manifest-twins-home.json 6824a2b9…25eb5`,
`manifest-readme.json 8560463c…5539c2b0`.

## 2. The twin set (delivered as content; this seat's write scope is receipt + scratch only)

All four quotes are ≥ 63 normalized characters, far above `MIN_QUOTE_CHARS = 12`, so none is rejected for
being too short to be evidence; every red below comes from the quote comparison itself.

### T1 — real SSVC words + fabricated guarantee (hybrid)

> "SSVC rates vulnerabilities on risk to the concerned stakeholder and guarantees remediation within 30 days for every scored vulnerability."

Construction: the **verbatim** overview-page clause (L247, normalized 63 chars, occurs exactly once — see
isolation control G1) with a fabricated guarantee spliced on. The fabricated half transplants EPSS/S053's
30-day window and a certainty SSVC never states: `guarantees` 0 hits, `guarantee` 0 hits,
`remediation within` 0 hits, `30 days` 0 hits, `within 30` 0 hits in **both** docs captures. What the page
actually says: L249 *"We encourage stakeholders to define to define their own decision points, timeframes of
actionability, and possibly, even their own roles."* and L259 *"These categories reflect the timeliness of
action to be taken."* — the clock belongs to the stakeholder, and nothing is guaranteed. Adversarial point:
a matcher that checked only the real prefix, or any fuzzy/prefix matcher, would pass this twin; the
instrument's full-substring comparison does not.

### T2 — real SSVC-project sentence, wrong artifact (README-only)

> "The Stakeholder-specific Vulnerability Categorization (SSVC) is a system for prioritizing actions during vulnerability management."

Construction: the GitHub README's own definitional sentence (README L3), attributed to the docs capture. It
is genuine CERTCC/SSVC project text — the README is the content repo for the very site captured — but it
occurs **0 times** in the overview capture, **0 times** in the home capture, and **1 time** in the README
bytes. The docs overview page words the idea differently (L261/L268 speak of suggested end-categories and
CVD-based coordinator advice; no "system for prioritizing actions" sentence exists there). Adversarial
point: this twin is not an invention — a verifier grepping the *project* rather than the *pinned capture*
would accept it. The pinned-capture check rejects it.

### T3 — near-miss quote, one word changed

> "Unlike other vulnerability scoring systems, SSVC measures risk to a particular stakeholder without imposing a one-size-fits-all approach."

Construction: overview L473 with `evaluates` → `measures` (a different sentence and a different swapped word
from the sibling control's `stakeholder`→`organization` near-miss, so the two controls do not duplicate each
other). The original occurs exactly once (isolation control G2, `OK occurrences=1`); the mutated sentence
occurs 0 times (`SSVC measures` 0 hits). Adversarial point: the sentence stays semantically almost true and
every other word is genuine — only the literal pin catches it.

### T4 — genuine sentence that occurs twice (needs anchor)

> "Automatable is a simple yes or no, can the attacker reliably automate all four steps (reconnaissance, weaponization, delivery, exploitation) of the kill chain? If the vulnerability allows remote code execution or command injection, the expected response should be 'yes.'"

Construction: a **genuine** overview-page sentence (normalized 270 chars) that appears **twice** — L299
inside the Supplier **Utility** decision-point table (after the Utility/Value Density rows, L296–298) and
L389 in the Deployer section, which restates it *"For easy reference, Automatable is…"* under the
Deployer's Automatable row (L387–388: *"Automatable is the same question as contained in the Supplier's
Utility decision point."*). Adversarial point: an unanchored manifest quoting it is **ambiguous between two
different decision-point tables** — exactly the case QUALITY Q9/B2's anchor rule exists for. This twin is
the one that must *not* be rejected as not-found; it must force an anchor.

## 3. Transcripts (verbatim; `exit` captured per run)

All runs: `python3 <scratch>/instr/source-recheck.py --manifest <manifest>` (scratch instrument copy,
sha256-verified equal to the repo copy).

### 3.1 Twin battery vs the overview pin (all four twins, no anchors)

```
### twin battery vs overview pin (T1-T4, no anchors) ###
S054:sha256 OK
S054:T1 MISMATCH reason=quote-not-found
S054:T2 MISMATCH reason=quote-not-found
S054:T3 MISMATCH reason=quote-not-found
S054:T4 MISMATCH reason=occurrence-not-unique
exit=1
```

T1–T3 rejected as absent; T4 rejected for the **right** reason — not `quote-not-found` but
`occurrence-not-unique` (the B2 non-unique rule), i.e. the instrument saw both occurrences and demanded an
anchor.

### 3.2 T4 anchor probes — the needed anchor, identified

```
### T4 anchor=299 (first occurrence line) ###      S054:T4 OK occurrences=2 anchor=299-ok   exit=0
### T4 anchor=389 (second occurrence line) ###     S054:T4 OK occurrences=2 anchor=389-ok   exit=0
### T4 anchor=296 (range boundary) ###             S054:T4 OK occurrences=2 anchor=296-ok   exit=0
### T4 anchor=386 (second-occurrence boundary) ### S054:T4 OK occurrences=2 anchor=386-ok   exit=0
### T4 anchor=295 (one line outside the range) ### S054:T4 MISMATCH reason=anchor-broken    exit=1
### T4 anchor=250 (unrelated line) ###             S054:T4 MISMATCH reason=anchor-broken    exit=1
```

**Needed anchor:** the anchor window is the 1-based lines `anchor..anchor+3`
(`anchor_verdict` joins `raw_lines[anchor-1:anchor+3]`), so for an occurrence on line *L* any anchor in
`L-3..L` verifies. Empirically: **296, 299** verify for the L299 occurrence and **386, 389** for the L389
occurrence; 295 and 250 are `anchor-broken`. Canonical choices: `anchor: 299` pins the Supplier Utility
table's definition; `anchor: 389` pins the Deployer restatement. A manifest quoting this sentence MUST carry
one of those anchors (or re-derive them if the committed capture bytes differ — they do not tonight: the
committed-candidate fetch is byte-identical, sha `ff3f3b2c…`).

### 3.3 Isolation controls — the reds are content-specific, not shape-specific

```
### isolation control: genuine prefix + genuine sentence ###
S054:sha256 OK
S054:G1 OK occurrences=1
S054:G2 OK occurrences=1
exit=0
```

G1 is T1's real prefix alone (`SSVC rates vulnerabilities on risk to the concerned stakeholder`, L247) and
G2 is T3's unmutated original (L473). Same manifest shape, same ids scheme, same capture sha as the twin
battery — green. So each twin's red is caused by exactly the mutation the twin adds.

### 3.4 URL robustness — the twins red under the pre-erratum home page too

```
### twin battery vs home pin (URL robustness) ###
S054:sha256 OK
S054:T1 MISMATCH reason=quote-not-found
S054:T2 MISMATCH reason=quote-not-found
S054:T3 MISMATCH reason=quote-not-found
S054:T4 MISMATCH reason=quote-not-found
exit=1
```

All four red on `https://certcc.github.io/SSVC/` as well. Honest difference: on the home page T4's rejection
mode is `quote-not-found` (the Automatable sentence is not on the home page at all), not
`occurrence-not-unique` — the anchor requirement is specific to the overview page the erratum pins.

### 3.5 T2 against the README pin — the sentence is real, the attribution is not

```
### T2 vs README pin (sentence is real README text) ###
S054:sha256 OK
S054:T2 OK occurrences=1
exit=0
```

Same quote, manifest re-pinned to the README bytes: green. This is the structural finding for T2: **no line
anchor can rescue it** (the quote is absent from the pinned docs capture, and a declared anchor cannot
rescue an absent quote — the sibling control's S2 case already showed that), so the *needed anchor* for a
README-sourced claim is a **separate captured source** — its own S-record with the README URL and sha —
never a reuse of the docs capture's S054.

### 3.6 Instrument selftest (scratch copy = committed bytes)

```
selftest cases=10 failures=0
exit=0
```

## 4. Replay against the committed capture (for the integrator / verifier)

`corpus/source-snapshots/round-37/S054.txt` did not exist in the lane at seat time (seat `ExecC2Capture`
owns it). Once the capture and the twin set are landed, this reproduces every red from repo bytes:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
S=$(mktemp -d)
cp corpus/source-snapshots/round-37/S054.txt "$S/S054.txt"
python3 - "$S" <<'PY'
import hashlib, json, pathlib, re, sys
s = pathlib.Path(sys.argv[1])
cap = s / "S054.txt"
twins = {
 "T1": "SSVC rates vulnerabilities on risk to the concerned stakeholder and guarantees remediation within 30 days for every scored vulnerability.",
 "T2": "The Stakeholder-specific Vulnerability Categorization (SSVC) is a system for prioritizing actions during vulnerability management.",
 "T3": "Unlike other vulnerability scoring systems, SSVC measures risk to a particular stakeholder without imposing a one-size-fits-all approach.",
 "T4": "Automatable is a simple yes or no, can the attacker reliably automate all four steps (reconnaissance, weaponization, delivery, exploitation) of the kill chain? If the vulnerability allows remote code execution or command injection, the expected response should be 'yes.'",
}
doc = {"schema_version": 1, "sources": [{"id": "S054", "path": "S054.txt",
       "url": "https://certcc.github.io/SSVC/tutorials/ssvc_overview/",
       "fetched_utc": "2026-10-26T17:15:32Z",
       "sha256": hashlib.sha256(cap.read_bytes()).hexdigest(),
       "quotes": [{"id": k, "quote": v} for k, v in twins.items()]}]}
(s / "manifest.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
PY
python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json"; echo "exit=$?"
# expect: T1/T2/T3 MISMATCH reason=quote-not-found; T4 MISMATCH reason=occurrence-not-unique; exit=1
```

Exercised in this seat with the repo inputs substituted by their scratch equivalents (the repo files do not
exist yet): identical output to §3.1. If the committed capture is the byte-identical overview fetch
(sha `ff3f3b2c…5fdce21`), the §3.2 anchor values hold as-is; otherwise re-derive them from the committed
bytes with the same probe pattern.

## 5. What is proven, and what is not

Proven by the transcripts above:

1. **All four twin construction classes are rejected** by the committed instrument against live fetches of
   the erratum-1 URL: hybrid real+fabricated (T1), README-only attribution (T2), one-word near-miss (T3),
   and unanchored duplicate (T4, `occurrence-not-unique`).
2. **The needed anchor for the duplicate is identified and verified**: anchors 296/299 (Supplier Utility
   table) and 386/389 (Deployer restatement) verify `anchor=N-ok`; 295/250 are `anchor-broken`; the valid
   range for an occurrence on line L is `L-3..L`.
3. **The reds are content-specific**: identical-shape manifests carrying the real prefix, the unmutated
   sentence, or the README-pinned quote are green (`OK occurrences=1`), so the discriminators reject the
   mutations, not the shape.
4. **The rejection is URL-insensitive** across both erratum candidate pages for T1–T3, and the T4 anchor
   requirement is pinned to the overview page the erratum names.
5. **T2's remedy is structural**: a README-sourced sentence needs its own captured S-record; no line anchor
   can substitute.

Not claimed by this receipt: that the admission harness or `recheck-audit.py` rejects the twins structurally
(`ExecC2Harness` / C1 territory; a twin set delivered in a receipt is outside `corpus/knowledge/*.md`);
that the committed round-37 capture equals this seat's fetch (replay §4 re-pins the sha); page stability
beyond the three identical fetches tonight (17:02:11Z, 17:02:19Z, 17:15:32Z).

## 6. Relationship to the sibling control (no overlap)

Seat `ExecC2JunkControl` delivered `c2-controls/junk-f20.md` (four whole-sentence fabrications J1–J4, plus a
`stakeholder`→`organization` near-miss, a stitched-fragments case, and an anchor-rescue case). This seat's
set is complementary and textually disjoint: T1 is a *hybrid* (real prefix + fabricated suffix) rather than
a whole-sentence invention; T2 attacks the **artifact boundary** (real project text, wrong capture) rather
than truth; T3 swaps a different word in a different sentence (`evaluates`→`measures`, L473); T4 is the only
twin that is **genuine** page text and is rejected for non-uniqueness, identifying the required anchor. If
the integrator wants the set landed alongside `junk-f20.md`, a suitable path is
`c2-controls/junk-f20-variants.md` carrying §2 verbatim with the same `control: negative` banner style —
that landing decision is the integrator's, not this seat's.

## 7. Tooling and environment record

- No tool installed or upgraded (nothing needed): host `python3` 3.14.8, Linux 7.2.11-arch1-1; lane
  instruments `source-recheck.py` (sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`)
  and `capture-source.py` (sha256 `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`) copied
  byte-for-byte into scratch, hashes verified equal to the repo copies before every run.
- Network: three live fetches via the committed `capture-source.py` (UA `kasegi-shokunin/1.0`, all
  `status=200`, `fetched_utc=2026-10-26T17:15:32Z` strict UTC). No other network access.
- Git: read-only only (`rev-parse`, `log --oneline`, `show --stat`, `ls-tree`, `status --porcelain`).
  No mutating git/jj command anywhere, including fixtures.
- Scratch: `/fast/scratch/hyaku/kasegi-r37/MutJunkTwin-2/` — created with `mkdir -p`, held every work copy
  and manifest, and is removed before this receipt's yield (verified absent afterwards; E9 quiescence safe).
