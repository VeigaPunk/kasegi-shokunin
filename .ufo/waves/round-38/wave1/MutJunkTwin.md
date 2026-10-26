# MutJunkTwin — round-38 wave1 receipt (F21 junk twins vs source-recheck)

Seat: MutJunkTwin (leaf, mutation-tester) · Round: kasegi-shokunin 38 · Axis judged: coverage · Milestone: round-38
Item: generate adversarial junk variants for F21 (OASIS CSAF v2.0, source S055) that source-recheck.py must reject; fetch+normalize the v2.0 OS page with capture-source.py; build scratch manifests; run a scratch copy of source-recheck.py; record each verdict.

## Setup (all work in scratch, lane untouched)

- Scratch: `S=/fast/scratch/hyaku/kasegi-r38/MutJunkTwin/` (created `mkdir -p`; TMPDIR bound to $S for every python run; removed before yield — see Cleanup).
- Scratch copies of the lane instruments, byte-identical to the committed originals (sha256):
  - `source-recheck.py` `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` (lane == scratch)
  - `capture-source.py` `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` (lane == scratch)
- `python3 $S/capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`

## Fetch records

1. CSAF v2.0 OS capture (item-mandated instrument), run twice to prove determinism:
   - `python3 $S/capture-source.py --id S055 --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html --out $S/m/S055.txt`
     → `S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:38:28Z`
   - Re-run to `$S/m/S055-second.txt` at `utc=2026-10-26T18:40:10Z` → same sha256; `cmp` → `captures byte-identical`.
   - The lane's `corpus/source-snapshots/round-38/` did not exist yet at run time (C2 executors concurrent); this scratch capture is from the identical URL with the lane's own instrument, so the byte binding `63c8ad52…e1cd42` is reproducible against the committed capture once it lands.
2. CSAF v2.1 draft (for the version-drift junk), mandated curl form:
   - `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o $S/v21-csd03.html https://docs.oasis-open.org/csaf/csaf/v2.1/csd03/csaf-v2.1-csd03.html` → `HTTP=200 bytes=1121726 utc=2026-10-26T18:38:58Z`
   - Probe first: `v2.1/os/csaf-v2.1-os.html` → 404; `csd03`/`csd02`/`csd01` → 200. Used csd03 (latest draft served).

## Junk variants (exact quotes) and pre-verified occurrence counts

Occurrence counts computed with the detector's own `normalize()` against the scratch capture (v2.0) and the normalized v2.1 csd03 text:

| id | junk kind | quote (normalized-exact) | v2.0 occ | v2.1 occ |
|----|-----------|--------------------------|----------|----------|
| J1 | real CSAF words, fabricated obligation | `Publishers of CSAF documents MUST provide a machine readable justification code for every product listed in known_affected.` | 0 | 0 |
| J2 | sentence from CSAF v2.1 draft, absent from v2.0 | `Unknown (unknown) of value type Products (products_t) represents that it is not known whether these versions are or are not affected by the vulnerability.` | 0 | 1 |
| J3 | near-miss, one word changed | v2.0 sentence `For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status.` with `MUST`→`SHOULD` (difflib word diff: `['- MUST', '+ SHOULD']` — exactly one word) | 0 | 0 |
| J4 | quote occurring twice in v2.0 text (needs an anchor) | `Multiple Flags with VEX Justification Codes per Product` — occurs exactly 2× (TOC line 222 + body heading line 3095) | 2 | 2 |

Controls (pristine/restored legs, same detector):
- P0 genuine pin: `Every Flag item of value type object with the mandatory property Label (label) contains product specific information in regard to this vulnerability as a single machine readable flag.` (occ=1)
- P1 restored original: the unmodified J3 base sentence (occ=1)
- P2 anchored double-occurrence pin: J4 with `anchor: 3095` (the body-heading line; detector window = anchor line + next 3)

## Scratch manifests

Eight manifests in `$S/m/`, each `{"schema_version":1,"sources":[{"id":"S055","path":"S055.txt","sha256":"63c8ad52…e1cd42","quotes":[…]}]}` (B1 stem rule satisfied: path stem `S055` == id):

`m0-baseline` (P0) · `m1-fabricated-obligation` (J1) · `m2-v21-sentence` (J2) · `m3-near-miss` (J3) · `m3-ok-restored` (P1) · `m4-anchor-missing` (J4, no anchor) · `m5-anchor-broken` (J4, `anchor:2` — line 2 is `Common Security Advisory Framework Version 2.0`) · `m6-anchor-ok-control` (P2)

## Detector runs — actual commands, output, verdicts

Command per manifest: `TMPDIR=$S python3 $S/source-recheck.py --manifest $S/m/<name>.json --source S055`

```
== m0-baseline
S055:sha256 OK
S055:Q1 OK occurrences=1
exit=0
== m1-fabricated-obligation
S055:sha256 OK
S055:Q1 MISMATCH reason=quote-not-found
exit=1
== m2-v21-sentence
S055:sha256 OK
S055:Q1 MISMATCH reason=quote-not-found
exit=1
== m3-near-miss
S055:sha256 OK
S055:Q1 MISMATCH reason=quote-not-found
exit=1
== m3-ok-restored
S055:sha256 OK
S055:Q1 OK occurrences=1
exit=0
== m4-anchor-missing
S055:sha256 OK
S055:Q1 MISMATCH reason=occurrence-not-unique
exit=1
== m5-anchor-broken
S055:sha256 OK
S055:Q1 MISMATCH reason=anchor-broken
exit=1
== m6-anchor-ok-control
S055:sha256 OK
S055:Q1 OK occurrences=2 anchor=3095-ok
exit=0
```

## Verdicts

| probe | mutant | expected | observed | verdict |
|-------|--------|----------|----------|---------|
| J1 | fabricated MUST obligation in real CSAF vocabulary | MISMATCH quote-not-found, exit 1 | `MISMATCH reason=quote-not-found`, exit 1 | **killed** |
| J2 | genuine v2.1-csd03 sentence (`unknown` product status) pinned against the v2.0 capture | MISMATCH quote-not-found, exit 1 | `MISMATCH reason=quote-not-found`, exit 1 | **killed** |
| J3 | one-word near-miss (MUST→SHOULD) of a real v2.0 sentence | MISMATCH quote-not-found, exit 1 | `MISMATCH reason=quote-not-found`, exit 1 | **killed** |
| J4a | twice-occurring v2.0 phrase pinned without anchor | MISMATCH occurrence-not-unique, exit 1 | `MISMATCH reason=occurrence-not-unique`, exit 1 | **killed** |
| J4b | same phrase with wrong anchor (2) | MISMATCH anchor-broken, exit 1 | `MISMATCH reason=anchor-broken`, exit 1 | **killed** |
| P0 | pristine genuine pin (baseline) | OK, exit 0 | `OK occurrences=1`, exit 0 | pass (baseline healthy — rejections are conclusive, not inconclusive) |
| P1 | restored original of J3 | OK, exit 0 | `OK occurrences=1`, exit 0 | pass (restoration leg) |
| P2 | same twice-occurring phrase with correct anchor 3095 | OK anchor-ok, exit 0 | `OK occurrences=2 anchor=3095-ok`, exit 0 | pass (anchor machinery accepts correct pins) |

## Findings (coverage)

1. All four mandated junk kinds are rejected by source-recheck (exit 1) with the precise expected reasons; no junk survived. The F21 recheck surface catches: (a) fabricated obligations (absence in normalized capture), (b) version drift v2.1→v2.0, (c) single-word normative-strength edits, (d) unanchored or wrongly-anchored pins of non-unique phrases (B2/Q9).
2. The rejections are precise, not blunt: the pristine pin, the restored original, and the correctly-anchored double-occurrence pin all pass (exit 0). A junk twin only survives if it is a ≥12-normalized-char substring of the committed capture AND (when non-unique) carries a verifying anchor — i.e. only a genuinely-occurring, correctly-anchored v2.0 sentence passes.
3. Version-drift material for future junk rounds: CSAF v2.1 csd03 (v2.1 OS not yet served — 404 at probe time) renamed the path notation to JSONPath (`$.vulnerabilities[*]…` vs v2.0's `/vulnerabilities[]/…`), switched many MUSTs to SHALLs, and added the `unknown` product status — genuine-looking sentences that are absent from v2.0.
4. No tooling installed (stock python3 + curl only; no pacman, no uv/npm installs). No mutating git/jj command run; no subagent spawned; no writes outside scratch and this receipt.

## Restoration evidence

- No lane, fleet, or source-tree bytes were modified by this seat: all reads were read-only; every write (captures, manifests, run outputs) lived under `$S`. Nothing to restore; the only lane write is this receipt.
- Scratch instrument copies verified byte-identical to the lane originals before use (sha256 above), so the detector behavior observed is the committed detector's behavior.
- Scratch removed before yield: `rm -rf -- /fast/scratch/hyaku/kasegi-r38/MutJunkTwin` (confirmed absent afterward).
