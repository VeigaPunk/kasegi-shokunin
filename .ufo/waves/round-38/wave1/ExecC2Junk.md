# ExecC2Junk — C2 junk twin: four fabricated CSAF/VEX claims are rejected and refuted (round 38, C2 / coverage)

Seat: `ExecC2Junk` (leaf, executor). Item: build the C2 junk twin for F21 (OASIS CSAF v2.0) — deliver
`c2-controls/junk-f21.md` content and prove each fabricated sentence is (a) rejected by the pinned-source
recheck and (b) substantively false against the standard.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only git; `HEAD=700153593eb586c70a6499c8ca225ee4d673bc9b`
at run time — other round-38 seats are landing concurrently; this seat wrote only its two wave1 files).
Write scope honoured: the only lane writes are
`.ufo/waves/round-38/wave1/ExecC2Junk.junk-f21.md` (deliverable) and this receipt. Every work copy, fetch and
transcript lived under `/fast/scratch/hyaku/kasegi-r38/ExecC2Junk/` (removed before yield, §8). No mutating git
command was run; no tool was installed.

Result in one line: the delivered twin's four sentences each occur **0** times in the pinned S055 capture,
`source-recheck.py` prints `MISMATCH reason=quote-not-found` ×4 with `exit=1` on both the scratch copy and the
committed instrument, the same manifest shape with genuine spec sentences is `OK occurrences=1` ×4 `exit=0`, and
each claim is contradicted by a named line of the OASIS Standard.

---

## 1. Pin identity — the capture the junk was tested against

Fetched with `curl` (recorded per the round's network rule) **and** normalized with the lane's own instrument, so
the normalization is exactly the one `source-recheck.py` compares with.

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o raw-S055.html \
    -w 'http_status=%{http_code} bytes=%{size_download} content_type=%{content_type} time_total=%{time_total}\n' \
    https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
http_status=200 bytes=414858 content_type=text/html time_total=0.055315
utc=2026-10-26T18:27:30Z
fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b  raw-S055.html
```

```
$ python3 corpus/instruments/capture-source.py --id S055 \
    --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html \
    --out $S/S055.txt --kind html
S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 \
     sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:27:34Z out=…/S055.txt
exit=0
  5146 272441 S055.txt
```

| fetch | channel | http | raw bytes | raw sha256 | normalized bytes | normalized sha256 |
|---|---|---|---|---|---|---|
| 1 | `curl` 18:27:30Z | 200 | 414858 | `fad0c60d…20cd66b` | 272441 | `63c8ad52…e11cd42` |
| 2 | `capture-source.py` (urllib) 18:27:34Z | 200 | 415225 | `0fbc5857…2d339ba` | 272441 | `63c8ad52…e11cd42` |
| 3 | `curl` 18:29:35Z | 200 | 414858 | `fad0c60d…20cd66b` | 272441 | `63c8ad52…e11cd42` |

Determinism note (measured, not assumed): the two `curl` fetches are byte-identical, the urllib body differs by
367 bytes, and the single difference is an injected analytics block
`<script type="module" src="https://static.cloudflareinsights.…` immediately before `</body>` (curl `<script>` tags
= 0, urllib = 1). `capture-source.py`'s `SCRIPT_RE` strips `<script>…</script>` before extraction, so **all three
fetches normalize to the identical 272441-byte snapshot, sha256 `63c8ad52…e11cd42`**. The junk red below therefore
does not depend on which fetch is committed.

Instrument used, copied byte-for-byte into scratch for the primary run:
`corpus/instruments/source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
(repo copy and scratch copy hashes equal). Python 3.14.8, Linux 7.2.11-arch1-1.

Line numbers cited in §4 are lines of the capture with sha256 `63c8ad52…e11cd42`; a capture with different bytes
re-pins them (the §5 replay re-derives the verdict from whatever capture is committed).

## 2. Deliverable — the junk twin

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/ExecC2Junk.junk-f21.md`
(landing target named by the frozen C2 claim: `.ufo/waves/round-38/c2-controls/junk-f21.md`).

- lines: **23**, bytes: **983**, sha256: **`6742705ec69537cfd949b1a7df506fe8446267c712aaec8b7e714d6cbdaa1630`**
- the file is the landable body only (front matter, four `## Claim n` sections, four blockquotes); no validation
  table, no notes — every table in this receipt is outside the deliverable.

Why it is a *plausible* impostor rather than a self-labelled joke: it mirrors an admitted entry's shape
(`# title`, `source: S055 — <url> — capture corpus/source-snapshots/round-38/S055.txt`, `ground: F21`), and its four
sentences are exactly what an unaudited summarizer emits — three of them are true statements about *neighbouring*
artifacts (CVSS scores as a concept, FIRST as CVSS/TLP owner, SSVC as a decision model) transplanted onto CSAF.
The `control: negative` line is the only self-identification, and it does **not** produce the rejection: the tested
manifest contains only the four blockquoted sentences (parsed with `^> "(.*)"$`, banner and front matter excluded).

```
$ python3 - <<'PY'   # quote equality, delivered file vs tested manifest
claims = re.findall(r'^> "(.*)"$', junk-f21.md, re.M); tested = [q["quote"] for q in manifest...]
print("identical to tested manifest quotes:", claims == tested, "| count:", len(claims))
PY
identical to tested manifest quotes: True | count: 4
```

## 3. Rejection transcripts (verbatim, `exit` captured per run)

### 3.1 Primary run — scratch copy of `source-recheck.py`, twin-derived manifest

Manifest `junk-manifest.json` was built by parsing the **delivered file** (four blockquotes, `id=J1..J4`),
`path=S055.txt`, `sha256=63c8ad52…e11cd42`.

```
=== run: junk manifest (4 fabricated sentences) ===
S055:sha256 OK
S055:J1 MISMATCH reason=quote-not-found
S055:J2 MISMATCH reason=quote-not-found
S055:J3 MISMATCH reason=quote-not-found
S055:J4 MISMATCH reason=quote-not-found
exit=1
```

### 3.2 Parity — the committed lane instrument on the same manifest

```
$ python3 corpus/instruments/source-recheck.py --manifest $S/junk-manifest.json
S055:sha256 OK
S055:J1 MISMATCH reason=quote-not-found
S055:J2 MISMATCH reason=quote-not-found
S055:J3 MISMATCH reason=quote-not-found
S055:J4 MISMATCH reason=quote-not-found
exit=1
```

Scratch copy and repo instrument agree line-for-line, so the red is the committed instrument's behaviour.

### 3.3 Positive control — genuine spec sentences, same manifest shape

```
=== positive control: genuine spec sentences ===
S055:sha256 OK
S055:G1 OK occurrences=1
S055:G2 OK occurrences=1
S055:G3 OK occurrences=1
S055:G4 OK occurrences=1
S055:G5 OK occurrences=1
exit=0
```

### 3.4 Isolation control — same ids `J1..J4`, same path, same sha256, genuine sentences substituted

```
=== isolation control: same ids/paths/sha, genuine sentences substituted ===
S055:sha256 OK
S055:J1 OK occurrences=1
S055:J2 OK occurrences=1
S055:J3 OK occurrences=1
S055:J4 OK occurrences=1
exit=0
```

Red vs green is decided by the quote text alone: the two manifests differ only in the `quote` strings (same
`schema_version`, `id=S055`, `path=S055.txt`, `sha256`, same four ids, no anchors). The discriminator is two-sided,
not a blanket rejecter.

### 3.5 Near-miss paraphrases of true statements

```
=== near-miss paraphrase ===
S055:sha256 OK
S055:N1 MISMATCH reason=quote-not-found
S055:N2 MISMATCH reason=quote-not-found
exit=1
```

- `N1` = the real conformance sentence 6.1.27.9 with `impact statement` → `impact note`.
- `N2` = the twin's J1 with the version corrected to `CVSS v3.1` — still false as written (no CVSS score is
  required at all, §4.1), and absent from the capture, so it reds too. A "less wrong" fabrication is not
  rescued by being closer to the truth.

### 3.6 Selection control — the other rejection mode

```
=== selection control: --source S056 on junk manifest ===
S056:source UNAVAILABLE reason=not-listed
exit=2
```

### 3.7 Instrument selftest (the scratch copy is the committed instrument)

```
SELFTEST clean PASS expected-exit=0 observed-exit=0 …
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 …
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 …
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 …
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 …
SELFTEST double-occurrence PASS expected-exit=1 observed-exit=1 …
SELFTEST double-occurrence-anchored PASS expected-exit=0 observed-exit=0 …
SELFTEST double-occurrence-out-of-range PASS expected-exit=1 observed-exit=1 …
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 …
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 …
selftest cases=10 failures=0
exit=0
```

### 3.8 Absence counts (the recheck's own comparison)

Occurrences are `source-recheck.py`'s `normalize()` (`" ".join(text.split())`, `<u>` markup dropped) and
`str.count` over the whole normalized snapshot — the exact comparison the manifest recheck performs.

| id | normalized chars | raw occurrences | normalized occurrences | verdict line emitted |
|---|---|---|---|---|
| J1 | 56 | **0** | **0** | `S055:J1 MISMATCH reason=quote-not-found` |
| J2 | 57 | **0** | **0** | `S055:J2 MISMATCH reason=quote-not-found` |
| J3 | 28 | **0** | **0** | `S055:J3 MISMATCH reason=quote-not-found` |
| J4 | 40 | **0** | **0** | `S055:J4 MISMATCH reason=quote-not-found` |

Every sentence is ≥ 28 normalized characters, so none can pass through `MIN_QUOTE_CHARS = 12` and none is rejected
for a different reason (empty, too-short, invalid id, duplicate id, stem mismatch, sha mismatch — all ruled out by
the `S055:sha256 OK` line and the ids in the output).

## 4. Substantive falsity — each claim against the standard

Counter greps over the whole capture (`S055.txt`, 5146 lines, 272441 bytes):

```
ssvc(ci)=0            decision point(ci)=0      cvss v4(ci)=0
4.0(all)=1            first.org(ci)=13          maintained(ci)=6        oasis(ci)=48
```

### 4.1 J1 "CSAF requires every advisory to carry a CVSS v4.0 score." — false twice over

No score is required at all, and CVSS v4.0 is not a version the standard knows.

- **L2080-L2094** — the mandatory element list of profile "CSAF Base" (which every other profile extends, L2071,
  L2104, L2114, L2126, L2138) is: `/document/category`, `/document/csaf_version`, `/document/publisher/category`,
  `/document/publisher/name`, `/document/publisher/namespace`, `/document/title`,
  `/document/tracking/{current_release_date,id,initial_release_date,status,version}`,
  `/document/tracking/revision_history[]/{date,number,summary}`. **`scores` is not in it**, and neither is any CVSS
  element.
- **L1645** — "Any vulnerability MAY provide the optional properties Acknowledgments (acknowledgments), …,
  Scores (scores), Threats (threats), and Title (title)." `scores` is **optional**.
- **L2012** — "Value type of every such Score item is object with the mandatory property products and the optional
  properties cvss_v2 and cvss_v3 …" — even inside an optional score object, the CVSS fields are optional.
- **L2026 / L2027** — the only CVSS versions named: `cvss_v2` "abiding by the schema at
  https://www.first.org/cvss/cvss-v2.0.json"; `cvss_v3` "abiding by one of the schemas at
  https://www.first.org/cvss/cvss-v3.0.json or https://www.first.org/cvss/cvss-v3.1.json". No v4.0.
- **L739** — the capture's only `4.0` is a *product version* example: `V3.0, V4.0, V4.1, V4.2`, listed at L740 as
  an invalid version range under `product_version`. It is not a CVSS version.

### 4.2 J2 "The VEX status known_not_affected needs no justification." — exactly inverted

- **L2152** — "For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement **SHALL**
  exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in
  /vulnerabilities[]/threats. For the latter one, the category value for such a statement MUST be impact and the
  details field SHALL contain a a description why the vulnerability cannot be exploited."
- **L2155** — "This implies that all products with the status known_not_affected **MUST** have an impact statement
  and all products with the status known_affected MUST have additional product specific information regardless of
  whether that is referenced through the Product ID or a Product Group ID."
- **L2877** — conformance test 6.1.27.9 Impact Statement: "For each item in
  /vulnerabilities[]/product_status/known_not_affected it **MUST be tested** that a corresponding impact statement
  exist in /vulnerabilities[]/flags or /vulnerabilities[]/threats."
- The machine-readable justifications are the five flag labels at **L1757-L1761** (`component_not_present`,
  `inline_mitigations_already_exist`, `vulnerable_code_cannot_be_controlled_by_adversary`,
  `vulnerable_code_not_in_execute_path`, `vulnerable_code_not_present`), which **L1762** ties to VEX: "The given
  values reflect the VEX not affected justifications." The standard's whole point is that the justification is
  machine-readable — the claim removes the very field.

### 4.3 J3 "CSAF is maintained by FIRST." — false; CSAF is an OASIS Standard

- **L3** — `OASIS Standard`; **L17-L18** — "Technical Committee: OASIS Common Security Advisory Framework (CSAF) TC";
  **L44** — "This document was last revised or approved by the membership of OASIS on the above date.";
  **L53** — "Copyright © OASIS Open 2022. All Rights Reserved."; **L46** — issued under "the OASIS IPR Policy".
- All 13 `first.org` occurrences are references to *CVSS* artefacts or the TLP definition, never to CSAF:
  **L433** (`First.org, Inc.` as publisher of the CVSS v2.0 guide), **L435** and **L437** (`FIRST.Org, Inc.` as
  publisher of the CVSS v3.0/v3.1 specification documents), **L523/L525/L527** and **L2026/L2027** (CVSS JSON
  schemas), **L533/L1306** (`https://www.first.org/tlp/`).
- None of the 6 `maintain*` hits (L393, L503, L1352, L1476, L3797, L4206) describes who maintains CSAF; they
  describe vendors/maintainers of *products*, the issuing authority of an ID, and a TLS transport rule.

### 4.4 J4 "CSAF v2.0 mandates SSVC decision points." — false; the term does not occur

- `ssvc` (case-insensitive): **0** occurrences in 272441 bytes; `decision point`: **0**.
- The two `decision` hits are unrelated: **L1889** — "…making a risk-based decision to patch or apply
  defense-in-depth measures" (prose addressed to the *consumer*, not a mandated data element), and **L4283** — the
  CVRF converter's namespace "decision".
- The VEX profile's complete mandatory set is **L2136-L2156** and names no SSVC construct: base-profile elements,
  `/product_tree`, `/vulnerabilities`, at least one of `fixed`/`known_affected`/`known_not_affected`/
  `under_investigation`, at least one of `cve`/`ids`/`notes`, the impact statement for `known_not_affected`
  (L2152), the action statement for `known_affected` (L2153), and **L2156** "The value of /document/category SHALL
  be csaf_vex."
- What the standard actually mandates as machine-readable decision content is the VEX not-affected justification
  flags (L1756-L1769) — a different model from SSVC, which this capture never mentions.

## 5. Replay against the committed capture (for the integrator / verifier)

The round-38 capture `corpus/source-snapshots/round-38/S055.txt` did not exist in the lane at the time of this seat
(seat owning the capture is separate), so every run above binds this seat's own fetch. Once it lands, this
reproduces the red from repo bytes without touching the repo:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
S=$(mktemp -d)
cp corpus/source-snapshots/round-38/S055.txt "$S/S055.txt"
python3 - "$S" <<'PY'
import hashlib, json, pathlib, re, sys
s = pathlib.Path(sys.argv[1]); cap = s / "S055.txt"
claims = re.findall(r'^> "(.*)"$', pathlib.Path(".ufo/waves/round-38/c2-controls/junk-f21.md").read_text(encoding="utf-8"), re.M)
doc = {"schema_version": 1, "sources": [{"id": "S055", "path": "S055.txt",
       "sha256": hashlib.sha256(cap.read_bytes()).hexdigest(),
       "quotes": [{"id": "J%d" % (i + 1), "quote": q} for i, q in enumerate(claims)]}]}
(s / "manifest.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print("claims parsed:", len(claims))
PY
python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json"; echo "exit=$?"   # expect 4x quote-not-found, exit=1
```

Recipe exercised here with the two repo inputs substituted by their scratch equivalents (the capture and the
landed twin do not exist yet): `claims parsed: 4` → `S055:J1..J4 MISMATCH reason=quote-not-found`, `exit=1`.

## 6. What is proven, and what is not

Proven by the transcripts above:

1. The delivered twin's four sentences are **rejected** — 4× `MISMATCH reason=quote-not-found`, `exit=1` — by the
   committed `source-recheck.py` (byte-identical scratch copy) against a capture made with the committed
   `capture-source.py` from the registry URL.
2. The rejection is **content-specific**: identical manifest shape with genuine spec sentences is `OK`/`exit=0`;
   the same four ids with genuine text are `OK`; two near-miss paraphrases (one word swapped; the J1 sentence with
   the version corrected) are red.
3. The rejection is **fetch-invariant**: three fetches (two `curl`, one urllib, one of them carrying an injected
   analytics script) normalize to the same snapshot sha256.
4. Each claim is **substantively false**, not merely unquotable: §4 cites the contradicting mandatory-element list,
   SHALL/MUST clauses, conformance test, committee/copyright lines and the zero-occurrence greps.

Not claimed by this receipt: that the admission harness or `recheck-audit.py` rejects the twin *structurally* (that
is harness/C1 territory and a `c2-controls/` file is outside `corpus/knowledge/*.md`); that the committed capture
equals this seat's fetch (it does not exist yet — §5 re-pins the sha); that the standard is stable upstream (drift
can change surrounding prose, but not the absence of invented claims, and not L2080-L2094, L2152, L2155, L2156).

## 7. Risks and blockers

- **Landing dependency (not a blocker for the evidence):** the twin content is delivered as
  `wave1/ExecC2Junk.junk-f21.md`; the frozen C2 claim checks `c2-controls/junk-f21.md`, so the integrator must land
  the file verbatim at that path (23 lines, 983 bytes, sha256 `6742705e…daa1630`). If it is landed with edits, the
  four blockquotes must stay byte-identical or the red no longer describes the landed file.
- **Capture binding:** every run binds sha256 `63c8ad52…e11cd42` (this seat's 18:27:34Z fetch). If the committed
  capture is a different fetch with different bytes, §5 rebuilds the manifest from the committed file, so the red
  survives a different capture sha.
- **Fabricated-sentence drift:** if the standard ever adopted one of these sentences the control would go stale;
  J1-J4 are checked against the 2026-10-26 capture and are absent from it (0 occurrences, raw and normalized).
- **Substantive-refutation staleness:** §4 cites line numbers of this capture; a different capture shifts line
  numbers but not the quoted text, which is also greppable by content.
- No tool was installed or upgraded in this seat (nothing was needed; `python3` 3.14.8 and `curl` sufficed).

## 8. Scratch

`S=/fast/scratch/hyaku/kasegi-r38/ExecC2Junk/` was created with `mkdir -p`, held `S055.txt`, three raw fetches,
four manifests, the instrument copy and `cites.txt`, and was removed before yield (`rm -rf -- "$S"`), after the
deliverable and this receipt were copied into `.ufo/waves/round-38/wave1/`.
