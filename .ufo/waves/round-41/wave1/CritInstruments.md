# CritInstruments — round-41 wave-1 receipt: instrument-assumption attack on C2

Seat: CritInstruments (leaf, receipt-only). Item: attack the instrument
assumptions behind the C2 gate chain (`source-recheck.py`,
`capture-binding-check.py`, `frontier-recheck-count.py`) for the F24/S063
(RFC 9116) admission. Method: full read of both instruments plus the harness,
three executable probes run in my scratch dir against the real committed
instruments, a network-use inventory of `corpus/instruments/`, and one live
fetch of the RFC 9116 primary text as an external anchor. No lane file was
written or modified; the round-41 `corpus/source-snapshots/round-41/` tree does
not exist yet in the working tree at attack time (wave-1 siblings still
building), so the attack targets the instruments and the claim language, not
sibling bytes.

## A. source-recheck.py — what `quote-not-found` / `occurrences` actually check

Full read of `corpus/instruments/source-recheck.py` (415 lines). The check is
three internal consistencies, nothing else:

1. record shape: `path` stem == record `id` (B1), `sha256` is 64 lowercase hex,
   quotes are non-empty, normalized quote >= 12 chars (`check_source`, lines
   113-148);
2. capture bytes sha256 == the manifest record's declared sha256 (lines
   181-185) — both sides of this equality are lane-authored artifacts;
3. quote search: `occurrences = normalized_source.count(normalize(quote))`
   (line 193) over the lane capture text only. `occurrences == 0` prints
   `reason=quote-not-found` and exits 1 (lines 208-211); `occurrences > 1`
   requires a verifying `anchor` line (B2, lines 108-134); `occurrences == 1`
   prints `OK occurrences=1`.

The record's `url` and `fetched_utc` fields are **never read** by this
instrument — they are inert here. There is no network code anywhere in the
file. The docstring states the scope itself (line 8-9): "This instrument reads
only local files; a successful check verifies captured bytes, not current
upstream availability or freshness."

**Probe A (run 1) — a lane-planted quote passes.** Fixture in scratch
(`/fast/scratch/hyaku/kasegi-r41/CritInstruments/probeA/`): a capture typed
inside the lane, opening line literally "LANE-AUTHORED CAPTURE — NO URL WAS
EVER FETCHED FOR THIS FILE", with the sentence "Per RFC 9116 a security.txt
file MUST be placed under the /.well-known/ path of the domain." planted in it;
manifest record with `url: https://www.rfc-editor.org/rfc/rfc9116.txt`,
`fetched_utc: 2026-10-27T09:30:00Z`, correct sha256 of my capture, and that
sentence as quote Q1. Real instrument, real invocation:

    $ python3 corpus/instruments/source-recheck.py --manifest .../probeA/manifest.json --source S063
    S063:sha256 OK
    S063:Q1 OK normalized=markup-whitespace occurrences=1
    exit=0

A 100% fabricated capture passes cleanly. The check is self-referential: the
quote is matched against the same lane file that the lane wrote.

**Probe A (run 2) — the instrument rejects the truth against a fabricated
capture.** Same capture, but Q1 is a genuine quote from the real RFC 9116
abstract ("defines a format to help organizations describe their vulnerability
disclosure process"):

    S063:sha256 OK
    S063:Q1 MISMATCH reason=quote-not-found
    exit=1

So the instrument's discrimination boundary is exactly "planted quote ∈ lane
capture". It accepts the fabrication when the quote is planted, and rejects the
authentic text when the capture is fake. It cannot tell the difference because
it has no channel to the URL.

## B. capture-binding-check.py — binding only, never content

Full read (892 lines). Four rule groups: A manifest-presence/per-file binding
by **file name**; B id→registry-row binding where the record `url` must equal
byte-for-byte the single `https://` token of the row's source cell (B1-B5);
C provenance shape (`fetched_utc` strict UTC or archival exemption); D
duplicate detection. `check()` (line 351+) opens `manifest.json` and
`SOURCES.md`; **no code path ever opens a capture file's bytes** (they are
`os.path.isfile`/`os.listdir`-ed only), and there is no network code. The
docstring's own "Known limits" admits it: "a record whose id names a row but
whose capture bytes came from a different document is bound by this instrument
and would only be caught by `source-recheck.py` (quote/sha256 pins) or a human
reader" — and per section A, source-recheck's pins are lane-authored on both
sides, so "caught" there means only quote-discipline, not truth.

**Probe B — a pancake recipe binds.** Minimal lane tree in scratch
(`probeB/`): registry row `| S063 | RFC 9116 security.txt —
https://www.rfc-editor.org/rfc/rfc9116.txt | spec | A | ... | mined | ... |`;
snapshot dir `round-41/` with manifest record (id S063, path S063.txt, url
byte-equal to the row token, `fetched_utc: 2026-10-27T09:35:00Z`, and a
deliberately wrong `"sha256": "ffff...ff"`) and a capture file that is a
pancake recipe stating in line 1 that no URL was fetched. Real instrument:

    $ python3 corpus/instruments/capture-binding-check.py --root .../probeB
    MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
    AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
    records=1 bound=1 unbound=0
    exit=0

`bound=1 unbound=0 exit=0` with content that manifestly does not match the URL,
and a sha256 field the checker never even reads. A lane-authored capture binds
fine by construction — the question in the seat spec is answered: only
manifest↔row↔file binding is verified; capture CONTENT vs URL is never
verified.

**Corollary on the C2 counting commands.** Every C2 gate number —
`records=55 bound=55 unbound=0`, source-recheck OK, `entries=27 pass=27` — is
computable entirely from lane-authored bytes. The frontier harness says so
itself (`frontier-recheck-count.py` lines 73-75): "This instrument measures
recheck coverage only: a passing entry proves its pinned captures still hold
its own assertions, not that the entry's claims are current upstream or that
the quotes assert what the entry says they assert."

## C. Network inventory of the instrument suite

Grep over `corpus/instruments/` for `urllib|requests|urlopen|curl |socket`:
the only network-capable file is `capture-source.py` (urllib, the
capture-production tool used at fetch time with UA
`kasegi-shokunin/1.0 (documentation capture; ...)`). No verification-time
instrument performs a fetch. Verification is deliberately network-free; the
real-world anchor is the fetch ledger recorded at capture time (HTTP status,
byte count, sha256, UTC instant) in the manifest/receipt.

## D. Is content-vs-URL verifiable at all? Live anchor for S063

Yes for this source, and cheaply. I fetched the canonical primary text twice:

    fetch 1: 2026-10-27T08:26:58Z  http_status=200 bytes=45129
             sha256 79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9
    fetch 2: 2026-10-27T08:27:00Z  http_status=200 bytes=45129  (same sha256)
    cmp: byte-identical

For `rfc-editor.org/rfc/rfc9116.txt` the raw digest IS stable across fetches
(contrast the S060 precedent: the Cloudflare-served CycloneDX page changed
3,936 bytes of `data-cfemail` tokens between two fetches, raw sha256 unstable
while normalized text was stable). Canonical cross-check strings present in
the live text: "Expires" field defined at L341-353
('The "Expires" field indicates the date and time after which the data'),
61 occurrences of `security.txt`, `/.well-known/security.txt` examples at
L268/283/284/416/479. Any committed S063 capture can therefore be compared
against an externally reproducible digest, and my independent fetch gives the
L1 a second ledger to cross-check the scout's S063 fetch record (HTTP status,
bytes, sha256, instant) without trusting any single lane member.

## E. Is the gap a QUALITY-criteria disclosure? — yes, already institutionalized

The disclosure the seat asks about exists and is load-bearing:

- **Q7** (`corpus/QUALITY.md` line 48): "Its successful output names what was
  checked: a pinned captured-source comparison is not a fresh network
  verification."
- **R21** (round-33 addition, line 170): "A counter set that binds only local
  bytes and shape counts (entry count, registry-row count, `occurrences=1`)
  is **not evidence that the capture is real**; until the manifest carries
  those fields, the claim states that limit instead of reading the passing
  counters as a capture check." This is exactly the S060 raw-digest-not-stable
  precedent generalized into criterion form.
- **R20** (line 169): manifest must carry `url` matching the registry row plus
  `fetched_utc` (round-32+) — the provenance fields that let a re-verifier
  separate a fabricated capture from a real one.
- **S060 precedent itself**: `corpus/source-snapshots/round-40/manifest.json`
  S063-precedent record carries `raw_sha256`, `raw_bytes`, an `http` block
  (status/content_type/date/server/user_agent) and a `reproducibility` field
  stating the raw digest is NOT stable across fetches while the normalized
  slice is; the S060 knowledge entry's `verified-at:` line repeats it. My
  section-D fetch shows the RFC 9116 mirror lacks that instability, so the S063
  record can and should state stability, not inherit the instability note.

## F. Verdicts

**V1 (lane-planted quote passes source-recheck): CONFIRMED.** Demonstrated
with the real instrument in probe A run 1 (exit 0). The capture check is
self-referential by design; the instrument's own docstring discloses the scope.

**V2 (capture-binding verifies manifest↔file binding only): CONFIRMED.**
Demonstrated in probe B (`records=1 bound=1 unbound=0 exit=0` for a pancake
recipe with a garbage sha256 field). A lane-authored capture binds fine. The
docstring's "Known limits" concedes it; per V1, source-recheck cannot close
the gap either.

**V3 (content-vs-URL unverifiable → QUALITY disclosure): PRESENT.** Q7 + R21 +
R20 + the S060 `reproducibility` precedent are the disclosure; for S063 the
content-vs-URL check is not only disclosable but externally reproducible
(section D: stable raw digest, byte-identical refetch).

**Fixable defect or tradeoff the judge must accept?** A tradeoff — not a
defect in the instruments, which do exactly what their contracts and docstrings
say, and not hidden, because Q7/R21 name it. The residual risk is
**over-reading the gate**: the C2 after-state (`bound=55/55`, `pass=27/27`,
source-recheck OK) is a claim about binding and pinned-quote discipline, not
about S063.txt being a true capture of RFC 9116. The strongest counterexample
available from local evidence is my probe A/B fixture class — a committed,
well-formed forged S063 (registry row + manifest with url/fetched_utc/quotes +
capture with planted quotes + knowledge entry with provenance trio) passes
every counting command in the C2 claim. The claim's "junk twin" kill (round-40
O4 class) covers a mined row *without* capture+entry+harness pass; it does not
cover a forged capture *with* all of them. What actually anchors S063 to
reality is process evidence outside the instruments: the scout fetch ledger
(HTTP status, bytes, sha256, UTC) recorded in the round-41 receipt, cross-checkable
against my independent ledger in section D.

**Smallest safe correction for this round (no instrument change required):**
(1) the S063 manifest record must carry the full R20/R21 provenance block —
`url`, `fetched_utc`, `http.status`, fetched/raw byte counts, `raw_sha256`, and
a `reproducibility` note following the S060 precedent (for this mirror: raw
digest stable across two fetches, sha256 79d19ce7...c61f9, 45,129 bytes); (2)
the round-41 receipt and the F24/S063 entry text must state the Q7/R21 limit
in so many words — "passing source-recheck and capture-binding is a pinned
capture comparison, not a fresh network verification" — and must not read
`bound=55`/`pass=27` as capture-authenticity evidence; (3) the L1 should
cross-check the scout's S063 fetch ledger against my section-D digest before
filing. If any of (1)-(3) is missing, the gap stops being a disclosed
tradeoff and becomes an undisclosed verifiability defect on depth:verifiability.

**Impacted axes:** depth:verifiability (C2's instrument chain cannot detect a
committed forged capture; the counting commands are necessary but not
sufficient for capture truth) and coverage (F24's admission is sound only
under the stated disclosure). No harm to any axis from the correction; it makes
the round-41 evidence strictly stronger.

## Evidence inventory

- Instrument reads (full): `corpus/instruments/source-recheck.py` 415 lines;
  `corpus/instruments/capture-binding-check.py` 892 lines;
  `frontier-recheck-count.py` docstring lines 73-75.
- Probe A run 1 output: `S063:sha256 OK` / `S063:Q1 OK
  normalized=markup-whitespace occurrences=1` / exit 0 (fabricated capture,
  planted quote).
- Probe A run 2 output: `S063:Q1 MISMATCH reason=quote-not-found` / exit 1
  (real RFC 9116 quote vs fabricated capture).
- Probe B output: `records=1 bound=1 unbound=0` / exit 0 (pancake-recipe
  capture, wrong sha256 field, byte-equal url binding).
- Network grep: only `capture-source.py` matches urllib/urlopen.
- Live fetch: 2026-10-27T08:26:58Z and 08:27:00Z, HTTP 200, 45,129 bytes,
  sha256 79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9,
  byte-identical refetch, UA kasegi-shokunin/1.0.
- Disclosure texts: QUALITY.md Q7 (L48), R20/R21 (L169-170); round-40
  manifest S060 record `reproducibility` field; S060 entry `verified-at:` line.
- No tools installed; no lane/fleet files written; probes ran read-only
  against committed instruments from my scratch dir; scratch dir removed.
