# RevSourceRecheck — round-38 S055 source-recheck pre-verification

Seat: RevSourceRecheck (leaf, reviewer). Item: pre-verify the S055 source-recheck — read
`corpus/instruments/source-recheck.py`, fetch+normalize the CSAF v2.0 URL, build a scratch
manifest with 4 quotes, run source-recheck (expect exit 0, `occurrences=1` each), then run it
on the raw (un-normalized) HTML and report whether the sha check catches the substitution.
Receipt only; no deliverable file. Manifest source: `ExecC2Capture.manifest.json` was already
present in the wave dir (first check) — the 3-checks-5-min-apart fallback was not needed; all
4 quotes (Q1–Q4) were taken from it verbatim.

## Verdict

Pre-verification **passes**. `source-recheck.py --manifest <scratch manifest>` exits 0 with
`S055:sha256 OK` and all four quotes `OK occurrences=1` (anchors 2135/2844/2151/1767 all
`-ok`). The raw-HTML substitution **is caught by the sha check**: exit 1 with
`S055:sha256 MISMATCH expected=63c8ad… actual=fad0c6…`, emitted before any quote is
evaluated, so zero quote verdicts appear in that run. The manifest's `raw_sha256` field is
ignored by the instrument (only `sha256` is read), so the substitution cannot slip through.

## Environment

- Instrument: `corpus/instruments/source-recheck.py` (415 lines, read in full 1–415; also read
  `corpus/instruments/capture-source.py:40-123` for the `html_to_text` normalizer the manifest
  declares).
- Scratch: `S=/fast/scratch/hyaku/kasegi-r38/RevSourceRecheck/` (TMPDIR bound there; removed
  before yield — verified `exists: False`).
- Tooling: no installs or updates (pacman untouched; stock `python3` and `curl` sufficed).

## Step 1 — fetch + normalize (mandated curl, same normalizer as the capture)

```
curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o $S/S055.raw.html -w '<fmt>' \
  https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
```

Actual: `rc=0`, `200 414858 0 https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`,
UTC fetch time `2026-10-26T18:35:58Z`. Raw bytes 414858, sha256
`fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` — equals the manifest's
declared `raw_sha256`.

Normalized by importing `capture-source.py:html_to_text` and running the fetched bytes through
it: 272441 bytes, 5146 lines, sha256
`63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` — equals the manifest's
declared `sha256` and is byte-identical to the sibling capture
(`ExecC2Capture.S055.txt`, 272441 bytes, same digest, `identical_to_mine=True`). The captured
snapshot is independently reproducible from upstream as of 18:35:58Z.

## Step 2 — instrument selftest (pre-verification of the instrument itself)

`python3 corpus/instruments/source-recheck.py --selftest` → exit 0:
`selftest cases=10 failures=0` (clean, corrupt, missing-source, missing-manifest, stem-mismatch,
double-occurrence ×4 anchor limbs, quote-absent — all PASS).

## Step 3 — clean run (manifest copy + my freshly normalized snapshot beside it)

`python3 corpus/instruments/source-recheck.py --manifest $S/manifest.json` (cwd = lane repo) →
**exit 0**, stdout exactly:

```
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
```

Each quote `occurrences=1` as required; all four declared anchors verify against the raw
snapshot lines. stderr empty in every run below.

## Step 4 — substitution: raw (un-normalized) HTML in place of the normalized snapshot

Overwrote `$S/S055.txt` with the fetched raw HTML (sha256
`fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b`), manifest unchanged (still
pins the normalized `63c8ad…`), re-ran the instrument → **exit 1**, stdout exactly:

```
S055:sha256 MISMATCH expected=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 actual=fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b
```

**Yes — the sha check catches the substitution.** `check_source()` hashes the snapshot bytes
and compares against the manifest `sha256` before any quote matching, so the substitution is
rejected at the digest layer with both digests named, and no quote verdicts are produced. The
manifest's `raw_sha256` key is dead weight to the instrument (never read), so a raw snapshot
cannot pass as the normalized capture.

## Step 5 — secondary observation: sha re-pinned to the raw HTML (what the quote layer alone says)

With `sha256` re-pinned to the raw digest (scratch `manifest-repinned.json`, `raw_sha256`
dropped), the instrument → **exit 1**:

```
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-BROKEN
S055:Q2 MISMATCH reason=quote-not-found
S055:Q3 MISMATCH reason=quote-not-found
S055:Q4 MISMATCH reason=quote-not-found
```

Q2/Q3/Q4 contain inline markup in the raw HTML (`<code>` spans), so even markup/whitespace
normalization cannot find them — the quote layer independently rejects the raw document. Q1's
sentence survives tag-free in one text node, so it still reports `occurrences=1`, and its
declared anchor (line 2135 of the normalized file) no longer holds at line 2135 of the raw
file, giving the note `anchor=2135-BROKEN` alongside verdict `OK`. Per the instrument's
documented contract (B2 makes anchor verdicts fatal only for non-unique quotes, docstring at
`source-recheck.py:71-84`), that OK-with-BROKEN-note combination on a unique quote is
by-design non-fatal, and it is unreachable in the round-38 configuration because the sha gate
fires first. Noted here for honesty; not a defect against the documented contract, no action
routed.

## Residual risk / verification gaps

- Upstream was stable between the sibling's 18:25:51Z fetch and mine at 18:35:58Z (identical
  digests); I did not re-check later — a future upstream edit would be caught at recheck time
  by the same sha gate demonstrated above.
- All runs used scratch copies; the checked-in capture and manifest were only read, never
  modified.
- Scratch dir removed before yield (verified absent); no files written in the lane beyond this
  receipt.
