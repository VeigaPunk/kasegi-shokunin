# ExecC2JunkControl — C2 junk twin: fabricated SSVC claims are rejected by the quote discriminators (round 37, C2 / coverage)

Seat: `ExecC2JunkControl` (leaf, executor). Item: build the C2 junk twin control for F20 — deliver the
`c2-controls/junk-f20.md` content and prove the discriminators reject it.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(claims freeze `224df74d…`, claims-erratum 1 `b3620681` read, not edited).
Write scope honoured: **no lane file was written except this receipt**; every work copy and transcript lived
under `/fast/scratch/hyaku/kasegi-r37/ExecC2JunkControl/` (removed before yield). No git command was mutating
(read-only `status`/`rev-parse`/`log` only). No tool was installed.

Result in one line: the four fabricated sentences each occur **0** times in the pinned S054 capture of both
candidate URLs, and `source-recheck.py` returns `MISMATCH reason=quote-not-found` for all four with `exit=1`,
while an identical-shape manifest carrying genuine page sentences returns `OK occurrences=1` ×4 with `exit=0`.

---

## 1. Pin identity — the capture the junk was tested against

Captured with the lane's own instrument, so the normalization is the one `source-recheck.py` applies:

```
$ python3 corpus/instruments/capture-source.py --id S054 \
    --url https://certcc.github.io/SSVC/tutorials/ssvc_overview/ --out <scratch>/S054.txt --kind html
S054 status=200 fetched_bytes=143053 snapshot_bytes=32623 \
     sha256=ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21 utc=2026-10-26T17:02:19Z out=…
```

| page | url | status | fetched_bytes | snapshot_bytes | lines | sha256 |
|---|---|---|---|---|---|---|
| primary pin (erratum 1 URL) | `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` | 200 | 143053 | 32623 | 518 | `ff3f3b2c…5fdce21` |
| home-page control | `https://certcc.github.io/SSVC/` | 200 | 105807 | 7730 | 286 | `a6613315…58bb56` |

Instrument used, copied byte-for-byte into scratch for every run below:
`corpus/instruments/source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
(repo copy and scratch copy hashes equal; Python 3.14.8, Linux 7.2.11-arch1-1).
Independent corroboration: seat `ExecC2QuoteOnce` fetched the same overview page at `17:02:11Z` and reports the
same `snapshot_bytes=32623` / `sha256=ff3f3b2c…5fdce21`, so this seat's pin is byte-identical to the quote-pin
capture used by the manifest work — two independent fetches, identical bytes.

## 2. The junk twin content (`c2-controls/junk-f20.md`)

Landed here as content only (this seat's write scope is receipt + scratch). Byte-exact file body, 991 bytes,
sha256 `22ec0dd965913ff8fe83eb880b5033f9757ebcc6ee3d089345d04d2304cbb945`:

```markdown
# SSVC — negative control twin for F20: fabricated claims that MUST fail the pinned-source check

control: negative — every quoted sentence below is invented; none of the four occurs in the S054 capture
source: S054 — https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — capture corpus/source-snapshots/round-37/S054.txt
forged-at: 2026-10-26 (kasegi-shokunin round 37, seat ExecC2JunkControl)
ground: F20 (adversarial twin — must NOT be admitted in place of the real entry)
expected: source-recheck.py over S054 prints one `MISMATCH reason=quote-not-found` line per claim and exits 1

## Claim 1 — a fixed remediation clock

> "SSVC guarantees a fixed remediation deadline for every vulnerability."

## Claim 2 — a replacement for severity scoring

> "SSVC replaces CVSS severity scoring."

## Claim 3 — maintained by FIRST

> "SSVC is maintained by FIRST."

## Claim 4 — a numeric exploitability score

> "SSVC assigns each vulnerability a 0-1 exploitability score."
```

Design notes, so the control carries weight rather than merely announcing itself:

- The file is shaped like an admitted entry (`# title`, `source: S054 — <url> — capture …`, `ground: F20`) so
  it is a *plausible* impostor for the admission harness, while the `control: negative` line keeps it from
  being mistaken for evidence by a reader.
- The rejection is **not** produced by that banner. The manifests below contain only the four blockquoted
  sentences (parsed out of the delivered file, `^> "(.*)"$`), no banner, no front matter — so the red verdict
  comes from the quote comparison alone. Verified: the four parsed blockquotes compare equal to the four
  quotes in the hand-built junk manifest (`identical to tested manifest quotes: True`).
- The twin deliberately carries no `recheck:` line: it is a specimen, not an admitted entry, and printing a
  `recheck:` line that resolves to nothing would turn the red into a missing-file red (the wrong reason).

### 2.1 Why each sentence is fabricated (not merely unlikely)

| id | claim | what the page actually says (pinned lines) |
|---|---|---|
| J1 | "SSVC guarantees a fixed remediation deadline for every vulnerability." | No deadline exists anywhere in the capture (`deadline` 0 hits, `fixed` 0 hits). The page hands the clock to the stakeholder: L249 *"We encourage stakeholders to define to define their own decision points, timeframes of actionability, and possibly, even their own roles."*; L259 *"These categories reflect the timeliness of action to be taken."* `remediat*` appears only as artefacts of remediation (L252 "providing remediations (patches)", L253 "apply the remediations or mitigations"), never as a clock. |
| J2 | "SSVC replaces CVSS severity scoring." | `replaces` 0 hits. The page states the opposite relation: L247 *"Unlike other vulnerability categorization systems that rate on technical severity (how bad it could be if the vulnerability were exploited) or exploitability (how likely it is that there will be an exploit), SSVC rates vulnerabilities on risk to the concerned stakeholder."*; L473 *"Unlike other vulnerability scoring systems, SSVC evaluates risk to a particular stakeholder without imposing a one-size-fits-all approach."* The site's own navigation (L155-L175) exposes `CVSS-based decision points` / `CVSS Decision Points` / `Base Metrics` / `Threat Metrics` as SSVC decision points — CVSS is an input to SSVC models, not something SSVC displaces. |
| J3 | "SSVC is maintained by FIRST." | Uppercase `FIRST` 0 hits (`first` occurs only inside prose, L449 *"The first two questions…"*, L465 *"…was first described…"*). The capture is the `CERTCC/SSVC` docs site (L6, L17), the practice is described as CERT/CC's (L268, L448 *"modeled on CERT/CC Coordinated Vulnerability Disclosure (CVD) practice"*, L449-L457), and L505-L507 carry *"Copyright © Carnegie Mellon University … CERT®, Carnegie Mellon® and CERT Coordination Center® are registered in the U.S. Patent and Trademark Office by Carnegie Mellon University."* The claim transplants FIRST's EPSS ownership (S053) onto SSVC. |
| J4 | "SSVC assigns each vulnerability a 0-1 exploitability score." | `0-1` and `0–1` both 0 hits. SSVC's Exploitation is categorical, not numeric: L281 *"Exploitation refers to how much evidence currently exists that the vulnerability is being exploited."* with the values `None` (L287), `Public PoC` (L290), `Active` (L293) and their definitions (L289, L292). The 0–1 probability is a *different* artifact the page only consumes as input (L93 *"EPSS Probability as input to Exploitation"*) — that is EPSS/S053-F19, not SSVC. |

## 3. Pinned comparison output, per junk sentence

Occurrences are `source-recheck.py`'s own `normalize()` (`" ".join(text.split())`, `<u>` markup dropped) and
`str.count` over the whole normalized snapshot — i.e. the exact comparison the manifest recheck performs.

| id | normalized chars | occurrences (overview pin) | occurrences (home control) | nearest real line | verdict line emitted |
|---|---|---|---|---|---|
| J1 | 69 | **0** | **0** | L249 / L259 (timeframes are stakeholder-defined) | `S054:J1 MISMATCH reason=quote-not-found` |
| J2 | 36 | **0** | **0** | L247 / L473 (SSVC *unlike* severity/exploitability systems); L155-L175 (CVSS decision points) | `S054:J2 MISMATCH reason=quote-not-found` |
| J3 | 28 | **0** | **0** | L6/L17 `CERTCC/SSVC`; L268/L448 CERT/CC; L505-L507 Carnegie Mellon copyright | `S054:J3 MISMATCH reason=quote-not-found` |
| J4 | 59 | **0** | **0** | L281 + L287/L290/L293 (categorical Exploitation); L93 (EPSS probability is an input) | `S054:J4 MISMATCH reason=quote-not-found` |

Each sentence is ≥ 28 normalized characters, so none can pass through the `MIN_QUOTE_CHARS = 12`
short-quote floor or be rejected for the wrong reason; none is rejected as empty or invalid either.

## 4. Rejection transcripts (verbatim, `exit` captured per run)

### 4.1 Junk manifest — the four fabricated sentences

```
### junk (4 fabricated sentences) ###
S054:sha256 OK
S054:J1 MISMATCH reason=quote-not-found
S054:J2 MISMATCH reason=quote-not-found
S054:J3 MISMATCH reason=quote-not-found
S054:J4 MISMATCH reason=quote-not-found
exit=1
```

### 4.2 Delivered twin content, parsed back out of `c2-controls/junk-f20.md`

```
### twin-parsed: the delivered c2-controls/junk-f20.md claims, exactly ###
S054:sha256 OK
S054:C1 MISMATCH reason=quote-not-found
S054:C2 MISMATCH reason=quote-not-found
S054:C3 MISMATCH reason=quote-not-found
S054:C4 MISMATCH reason=quote-not-found
exit=1
```

### 4.3 Positive control — two genuine page sentences with anchors

```
### genuine positive control (2 real page sentences) ###
S054:sha256 OK
S054:G1 OK occurrences=1 anchor=247-ok
S054:G2 OK occurrences=1 anchor=278-ok
exit=0
```

### 4.4 Isolation control — same ids, same paths, same capture sha, genuine sentences substituted

```
### same ids/paths/sha, genuine sentences substituted ###
S054:sha256 OK
S054:C1 OK occurrences=1
S054:C2 OK occurrences=1
S054:C3 OK occurrences=1
S054:C4 OK occurrences=1
exit=0
```

Manifest `twin-parsed-manifest.json` (junk) and `twin-shape-genuine-manifest.json` (genuine) differ only in
the `quote` strings and `location` notes: same `schema_version`, `id=S054`, `path=S054.txt`, `url`,
`fetched_utc`, `sha256`, same four quote ids `C1..C4`, no anchors in either. Red vs green is therefore decided
by the quote text alone — the discriminator is two-sided, not a blanket rejecter.

### 4.5 Near-miss paraphrase — one word swapped in a genuine sentence

```
### near-miss paraphrase (one word swapped: stakeholder -> organization) ###
S054:sha256 OK
S054:N1 MISMATCH reason=quote-not-found
exit=1
```

`SSVC rates vulnerabilities on risk to the concerned organization` vs the page's `…concerned stakeholder`
(L247): the pin is literal, so a plausible paraphrase of a *true* sentence is rejected exactly like an
invention.

### 4.6 Adversarial fabrication routes the twin could try

```
### adversarial: stitched fabrication + fabricated-with-valid-anchor ###
S054:sha256 OK
S054:S1 MISMATCH reason=quote-not-found
S054:S2 MISMATCH reason=quote-not-found
exit=1
```

- `S1` is built only from genuine fragments — L244 *"Risk exists on a continuum, and different stakeholders
  have different threat models and risk appetites."* concatenated with L247 *"SSVC rates vulnerabilities on
  risk to the concerned stakeholder"* across the L245-L246 gap. Normalization collapses whitespace but not
  intervening text, so the false adjacency does not match: stitching real bytes into a fake adjacency still
  reds.
- `S2` is fabricated J1 carrying a **valid** anchor (`anchor: 247`, a line that really holds a genuine
  sentence). It still reds, because a declared anchor cannot rescue an absent quote — the anchor path only
  arbitrates *non-unique* quotes.

### 4.7 Selection control — the other rejection mode named in the item

```
### selection control: --source S055 on junk manifest (unlisted id) ###
S055:source UNAVAILABLE reason=not-listed
exit=2
```

### 4.8 URL-robustness — the junk reds under the pre-erratum home page too

```
### junk sentences vs HOME page capture (URL-robustness) ###
S054:sha256 OK
S054:J1 MISMATCH reason=quote-not-found
S054:J2 MISMATCH reason=quote-not-found
S054:J3 MISMATCH reason=quote-not-found
S054:J4 MISMATCH reason=quote-not-found
exit=1
```

So the rejection does not depend on which of the two erratum candidates is captured: the four claims are
absent from `https://certcc.github.io/SSVC/` as well. Only the manifest `sha256` has to be pointed at whichever
capture is committed.

### 4.9 Instrument selftest (the scratch copy is the committed instrument)

```
selftest cases=10 failures=0
exit=0
```

## 5. Replay against the committed capture (for the integrator / verifier)

The round-37 capture `corpus/source-snapshots/round-37/S054.txt` did not exist in the lane at the time of this
seat (seat `ExecC2Capture` owns it), so every run above binds this seat's own fetch of the erratum URL. Once the
capture and the twin are landed, this reproduces the red from repo bytes without touching the repo:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
S=$(mktemp -d)
cp corpus/source-snapshots/round-37/S054.txt "$S/S054.txt"
python3 - "$S" <<'PY'
import hashlib, json, pathlib, re, sys
s = pathlib.Path(sys.argv[1])
cap = s / "S054.txt"
claims = re.findall(r'^> "(.*)"$', pathlib.Path("c2-controls/junk-f20.md").read_text(encoding="utf-8"), re.M)
doc = {"schema_version": 1, "sources": [{"id": "S054", "path": "S054.txt",
       "sha256": hashlib.sha256(cap.read_bytes()).hexdigest(),
       "quotes": [{"id": "C%d" % (i+1), "quote": q} for i, q in enumerate(claims)]}]}
(s / "manifest.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print("claims parsed:", len(claims))
PY
python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json"; echo "exit=$?"   # expect 4x quote-not-found, exit=1
```

Recipe exercised in this seat with the two repo inputs substituted by their scratch equivalents (neither repo
file exists yet): `claims parsed: 4` →
`S054:C1..C4 MISMATCH reason=quote-not-found`, `exit=1`.

## 6. What is proven, and what is not

Proven by the transcripts above:

1. The delivered `c2-controls/junk-f20.md` claims are **rejected** — 4× `MISMATCH reason=quote-not-found`,
   `exit=1` — by the committed `source-recheck.py` (sha256-pinned copy) against a capture made with the
   committed `capture-source.py` from the erratum URL.
2. The rejection is **content-specific**: identical manifest shape with genuine sentences is `OK`/`exit=0`;
   a one-word paraphrase of a true sentence is red; stitched genuine fragments and an anchor-rescue attempt
   are red.
3. The rejection is **URL-insensitive** across both erratum candidates, and the alternative rejection mode
   `--source S055` gives `UNAVAILABLE reason=not-listed exit=2`.
4. The twin is a *plausible* impostor: it mirrors the admitted-entry front matter, and its four sentences are
   the kind of claim an unaudited summarizer produces (fixed deadline, "replaces CVSS", "maintained by
   FIRST", "0-1 exploitability score") — three of which are truths about neighbouring artifacts (KEV
   deadlines, CVSS, EPSS/S053) transplanted onto SSVC.

Not claimed by this receipt: that the admission harness or `recheck-audit.py` rejects the twin structurally
(that is `ExecC2Harness`/C1 territory, and a `c2-controls/` file is outside `corpus/knowledge/*.md`); that
the committed round-37 capture equals this seat's fetch (it does not exist yet — replay §5 re-pins the sha);
that the page is stable (drift can change surrounding prose, but not the absence of invented claims).

## 7. Risks and blockers

- **Landing dependency (not a blocker for the evidence):** `c2-controls/junk-f20.md` content is delivered here,
  not written into the lane, because this seat's write scope is receipt + scratch only. The integrator must
  land the §2 block verbatim (991 bytes, sha256 `22ec0dd9…cbb945`) for the frozen C2 claim's "junk twin
  c2-controls/junk-f20.md rejected" to be checkable from repo bytes.
- **Capture binding:** the scratch manifest binds `sha256 ff3f3b2c…5fdce21` (this seat's 17:02:19Z fetch). The
  committed capture may be a later fetch; §5 rebuilds the manifest from the committed file, so the red
  survives a different capture sha.
- **Fabricated-sentence drift:** if the SSVC site ever adopted one of these sentences verbatim the control
  would go stale; J1-J4 are checked against both current captures and are absent from both.
- No tool was installed or upgraded in this seat (nothing was needed; `python3` 3.14.8 sufficed).
