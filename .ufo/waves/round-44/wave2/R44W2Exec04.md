# R44W2Exec04 — pinned-source receipt: corpus/source-snapshots/round-44/S069.txt at 8063547

seat: R44W2Exec04 (falsify, wave 2). Item: recompute sha256/bytes/lines of the pinned capture and check each manifest Q1–Q5 anchor against the pinned file. Tree under attack: commit `8063547d0ce647d6f9eafc3c8d0a502616685218` (`git rev-parse HEAD` on the lane = the same; `git status --porcelain` shows `corpus/source-snapshots/round-44/` clean — `git ls-files -m` → empty).

## 1. Digest / byte / line recomputation — all three recorded values MATCH

```
$ git show 8063547:corpus/source-snapshots/round-44/S069.txt > $S/S069.txt
$ sha256sum $S/S069.txt
0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2
$ wc -c -l $S/S069.txt
1132 45681   (newline count and byte count; file ends with '\n', 0 CR bytes, valid UTF-8)
$ file $S/S069.txt
Unicode text, UTF-8 text, with very long lines (433)
```

manifest record (`git show 8063547:corpus/source-snapshots/round-44/manifest.json`):
`sha256: 0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`, `bytes: 45681`, `snapshot_bytes: 45681`, `lines: 1132`, `path: S069.txt` (stem == id, B1 ok), `fetched_utc: 2026-10-28T18:53:38Z` (strict-Z), `http.status: 200`, `capture_url == http.final_url` (E3 ok). All three expected values reproduce exactly — **no falsification there**.

## 2. Provenance chain is reproducible from committed bytes

`git show 8063547:.ufo/waves/round-44/source-recon/S069.txt` is the raw article-API JSON (47136 bytes, keys `title, body, public, categories, documentId`). `jq -r '.body'` on it reproduces the pinned capture **byte-identically**:

```
$ git show 8063547:.ufo/waves/round-44/source-recon/S069.txt | jq -r '.body' | sha256sum
0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2   (== committed snapshot)
```

This supports the SOURCES row note "capture body extracted from preserved API JSON via `jq -r '.body'`".

## 3. Q1–Q5 anchor resolution — mixed result

Each manifest quote is a multi-line span in the hard-wrapped capture (no quote is a literal substring of the file; all five pass under `normalize=markup-whitespace`, each with `occurrences=1`). Reproducing `corpus/instruments/source-recheck.py`'s own verdicts on the committed manifest gives `anchor=N-ok` for all five — **but the mechanism has two gaps the receipt conceals**:

**Finding A (defect, minor): Q3's anchor is off by one.** The manifest names `Q3.anchor=70`, but the quote's first character is on line 71, not 70. Line 70 is `* **Ineligibility**: Even if you find a valid vulnerability in Google-managed` — the start of the enclosing bullet. The four other anchors all name the quote's first line:

| quote | manifest anchor | line holding quote's first char | strict match |
|---|---|---|---|
| Q1 | 61 | 61 | ✓ |
| Q2 | 62 | 62 (starts mid-line after "and services. ") | ✓ |
| Q3 | **70** | **71** (` infrastructure, the report is ineligible…`) | **✗** |
| Q4 | 76 | 76 (starts mid-line after " prohibited. ") | ✓ |
| Q5 | 10 | 10 | ✓ |

`python3 -c` check: `"the report is ineligible for a reward if" in line 70` → False; first found on line 71. Under the strict reading "the line the manifest names," Q3 does not resolve; it only passes because the instrument's window is `raw_lines[anchor-1:anchor+3]` (a 4-line window — anchors 69, 70, and 71 all print `-ok` for Q3). The four-vs-one split shows the lane's working convention is "quote's first line," which Q3 breaks by naming the sentence's first line instead. The packet's own range `reward ineligible … :70-72` is consistent with anchor=70 (it needs the bullet header's line), so this may be deliberate convention drift rather than an error — but it is an *undocumented* convention and weaker than S067's exact-line locators.

**Finding B (discipline gap): the anchors are never gated.** `source-recheck.py` only fails a broken anchor when `occurrences > 1` (QUALITY Q9/B2). All five S069 quotes have `occurrences=1`, so anchor verification is cosmetic: mutating the committed manifest to `Q3.anchor=999` still exits 0 and still prints `S069:Q3 OK`:

```
$ source-recheck.py --manifest mutant-Q3-anchor999.json --source S069
S069:Q3 OK normalized=markup-whitespace occurrences=1 anchor=999-BROKEN
exit=0
```

Likewise `Q1.anchor=58` prints `anchor=58-BROKEN` and exits 0. So `controls/S069-source-recheck.txt`'s `anchor=N-ok` lines are a non-binding note, not a check: no committed instrument can fail on a wrong S069 anchor. (This is a pre-existing Q9 scoping decision, not a round-44 regression — but the round's receipt presents `anchor=N-ok` as verified evidence.)

## 4. Field-semantics drift vs the S067 precedent (minor)

S067 recorded `bytes: 10455` (raw fetched size) + `snapshot_bytes: 3822` + `raw_sha256`. S069 records `bytes == snapshot_bytes == 45681` (the extracted text) and **no `raw_sha256`**, so the raw API JSON digest (47136 B, sha256 `7e2004ba30638ba8ce2a123d6385ade62685e148c661b46ffd93519db0bc4609`, committed at `.ufo/waves/round-44/source-recon/S069.txt`) is pinned only by its own path, not digest-bound in the manifest. No instrument checks `bytes`/`lines` — both fields are unverified prose; they happen to be correct (measured in §1), but a wrong `lines` or `bytes` would pass every committed gate.

## 5. Checks that did not falsify

- `capture-binding-check.py --root <export of 8063547>` → `MANIFEST round-44 records=1 … records=58 bound=58 unbound=0`, exit 0; S069's SOURCES row source cell carries exactly one `https://` token equal to `url`.
- `source-recheck.py` on the committed manifest → all five `OK`, exit 0 (verbatim control `.ufo/waves/round-44/controls/S069-source-recheck.txt` matches my replay).
- Word counts 13/12/18/21/16 — all ≤25, matching the r43 spot-check quote discipline.
- All five normalized quotes also occur exactly once in the live-drift body captured by the lane (`controls/S069-live-drift.txt`), so the pins remain locatable on the reformatted live page.
- SOURCES row's ranges "Q1–Q3 lines 61–72, Q4 lines 76–77, Q5 lines 9–11" all contain their quotes; nonauthor-spotcheck-packet's `S069.txt:61` for Q1 is the quote's first line.

## Verdict

The pinned digest, byte count and line count are **fully correct** (all three recomputed fields match). The anchor set **partially fails strict resolution**: Q3's anchor names the line before the quote begins (Finding A), and anchors are structurally non-gating for unique quotes (Finding B) — so the claim "each of the manifest's Q1–Q5 anchors resolves to the pinned file at the line the manifest names" holds only under the instrument's 4-line-window semantics, not under the line-precise semantics S067 demonstrated. Field-semantics drift (`bytes`, missing `raw_sha256`) is a smaller provenance weakening (§4).

## Limitations

- No live HTTP re-open was performed (no network); I checked quotes against the lane's own live-drift capture instead. `http.status: 200` and `fetched_utc` could not be independently verified.
- "Anchor" has no documented definition beyond the instrument's window rule; Finding A is an off-by-one under the dominant quote-start convention, and may be intentional bullet-start conventioning — the manifest documents neither.
- I could not check whether `bytes` is contractually defined anywhere; the S067→S069 drift is observational.

## Evidence retained

- `corpus/source-snapshots/round-44/S069.txt` @8063547 — sha256 `0932279c…`, 45681 B, 1132 newlines.
- `corpus/source-snapshots/round-44/manifest.json` @8063547 — record fields quoted in §1.
- `corpus/instruments/source-recheck.py` @8063547 — `anchor_verdict` window `raw_lines[max(0, anchor-1):anchor+3]`; B2 gated on `occurrences > 1`.
- `.ufo/waves/round-44/controls/S069-source-recheck.txt` @8063547 — the lane's receipt (replays identically).
- `.ufo/waves/round-44/source-recon/S069.txt` @8063547 — raw API JSON, `jq -r '.body'` ⇒ byte-identical pinned capture.
- Mutation receipts: Q3.anchor=999 → `OK … anchor=999-BROKEN` exit 0; Q1.anchor=58 → `anchor=58-BROKEN` exit 0; Q3 anchors 69/70/71 all print `-ok`.
- `corpus/SOURCES.md` @8063547 L75 — S069 row (single `https://` token; sha256 cited correctly).
- `.ufo/waves/round-44/nonauthor-spotcheck-packet.md` @8063547 — pinned-byte figures restated correctly; `:70-72` range for the Q3 bullet.

No tools installed; no edits outside this report. Scratch `$HYAKU_SCRATCH/kasegi-r44/R44W2Exec04/` removed at yield.

Report: .ufo/waves/round-44/wave2/R44W2Exec04.md
