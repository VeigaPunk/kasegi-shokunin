# RevSourceRecheck — S054 source-recheck specification and pre-verification (round 37, C2 / coverage)

Seat: `RevSourceRecheck` (leaf, reviewer). Item: specify and pre-verify the S054 source-recheck —
instrument contract, the four planned quotes, a fresh live fetch into scratch, occurrence counting, and
a scratch `source-recheck` run against a scratch manifest (expect exit 0, each Q `occurrences=1`).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat except this receipt).
No lane/fleet/source-tree file written except this receipt; no mutating git command run; no installs.

## 1. Instruments under test (committed bytes)

Worktree `corpus/instruments/` is unmodified at lane head `b3620681` (git status shows no
`corpus/` entry), so these hashes are the committed instruments:

```
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18  corpus/instruments/capture-source.py
```

Both selftests pass on this host (transcripts in §5).

## 2. Invocation contract (the deliverable)

### 2.1 `source-recheck.py` — CLI and semantics

```
python3 corpus/instruments/source-recheck.py --manifest PATH [--source ID]
python3 corpus/instruments/source-recheck.py --selftest
```

- `--manifest PATH`: JSON, resolved strictly; record `path` values resolve **relative to the manifest's
  directory** and must stay inside it (`commonpath` check; `reason=outside-manifest-directory`).
- `--source ID`: check one source; unknown/invalid id → exit 2 (`reason=not-listed` / `invalid-source-id`).
- Exit codes: **0** all checks OK; **1** verification failure (MISMATCH); **2** unavailable/malformed
  (missing manifest, bad schema, bad sha field, missing capture, quote too short, …).
- Output lines: `manifest UNAVAILABLE reason=…`; `<ID>:sha256 OK|MISMATCH expected=<sha> actual=<sha>`;
  `<ID>:<QID> OK occurrences=N[ anchor=N-ok][ normalized=markup-whitespace]`;
  `<ID>:<QID> MISMATCH reason=quote-not-found|occurrence-not-unique|anchor-out-of-range|anchor-broken`.

Manifest schema (enforced, `schema_version` must be int `1`):

```json
{"schema_version": 1,
 "sources": [{"id": "S054",            // [A-Za-z0-9][A-Za-z0-9._-]*, unique
              "path": "S054.txt",      // relative, not absolute, stem MUST equal id (B1)
              "sha256": "<64 lowercase hex of the exact snapshot bytes>",
              "quotes": [{"id": "Q1",  // valid unique id
                          "quote": "…exact text…",
                          "location": "human note (free text)",
                          "anchor": 247}]}]}   // optional int, 1-based line
```

- Normalization for matching (`normalize()`): `" ".join(text.split())` with `<u>`/`</u>` dropped.
- A quote whose normalized length < 12 (`MIN_QUOTE_CHARS`) is refused (`reason=quote-too-short-to-be-evidence`).
- **B2 occurrence rule**: quote occurring >1 time passes only with a verifying `anchor`
  (`anchor_verdict`: the normalized quote must appear in `" ".join(raw_lines[anchor-1:anchor+3])` —
  the anchor line plus the 3 following lines); missing/out-of-range/broken anchors all fail exit 1.
- A unique quote needs no anchor; a quote absent from the capture fails `reason=quote-not-found`
  even if the sha matches (r31 MutSRExisting M5 pin; selftest `quote-absent` covers it).
- If the raw quote is not a literal substring but the normalized one is, the OK line carries
  `normalized=markup-whitespace` — legal, self-declared.

### 2.2 `capture-source.py` — how the pinned bytes are made

```
python3 corpus/instruments/capture-source.py --id S054 --url URL --out DIR/S054.txt [--kind html|pdf|text]
```

- HTML pipeline: `<script>/<style>` blocks removed → block tags (`p div li tr h1-h6 section article br`,
  `<br>`) to newlines → remaining tags stripped → `html.unescape` → per-line whitespace/NBSP collapse,
  blank lines dropped, UTF-8, trailing newline.
- Prints the binding line: `S054 status=200 fetched_bytes=N snapshot_bytes=N sha256=<sha> utc=<strict UTC> out=<path>`;
  the `sha256` is what the manifest record must carry. `--selftest` proves normalize+determinism.

### 2.3 Composed S054 invocation (what C2's `source-recheck S054 exit 0` is)

Manifest at `corpus/source-snapshots/round-37/manifest.json` with record `{"id":"S054","path":"S054.txt", …}`;
run `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054`
from the lane root. Expected output shape: `S054:sha256 OK` then four
`S054:Q<n> OK occurrences=1 anchor=<line>-ok` lines, exit 0.

## 3. Fresh live fetch + occurrence pre-check (this seat, scratch)

Scratch `/fast/scratch/hyaku/kasegi-r37/RevSourceRecheck/` (removed before yield). Fetched with the
lane's own `capture-source.py`, using the **erratum-1 URL**
`https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (claims-erratum-1.md, commit `b3620681`;
the frozen claims' `https://certcc.github.io/SSVC/` home page is superseded — it carries only the
definition sentence plus navigation):

```
S054 status=200 fetched_bytes=143053 snapshot_bytes=32623 sha256=ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21 utc=2026-10-26T17:13:12Z
```

The digest is byte-identical to the 17:02:11Z fetch recorded by sibling seat `ExecC2QuoteOnce` —
the page is stable across 11 minutes, and both pins are the same 518-line snapshot. Occurrence and
anchor measurement with the instrument's own `normalize()`/window semantics:

| id | occurrences (normalized) | raw | norm chars | earliest valid anchor | anchor line length |
|---|---|---|---|---|---|
| Q1 | 1 | 1 | 157 | 244 | 139 |
| Q2 | 1 | 1 | 90 | 256 | 4 |
| Q3 | 1 | 1 | 153 | 274 | 50 |
| Q4 | 1 | 1 | 103 | 364 | 24 |

All four planned quotes occur **exactly once** in the normalized snapshot — no anchor is even
required by B2; every declared anchor is belt-and-braces. Q2's anchor line is 4 chars because the
snapshot line-splitting breaks the sentence across lines — the 4-line anchor window is what makes a
multi-line quote verifiable, which is why declaring anchors anyway is worth it.

**Anchor non-uniqueness finding (spec clarification):** the 4-line window means several lines per
quote verify. Against this exact snapshot, both the receipt's anchors **247/259/277/367** and the
earliest-valid **244/256/274/364** return `anchor=N-ok` from the instrument's own `anchor_verdict`.
The committed manifest may carry either set; line numbers are valid **only for sha256
`ff3f3b2c…fdce21`** — a re-fetch that changes bytes must re-derive them.

## 4. Scratch manifest + source-recheck run (positive control)

Scratch manifest (exact bytes `{"schema_version": 1, "sources": [{"id": "S054", "path": "S054.txt",
"sha256": "ff3f3b2c…fdce21", "quotes": [Q1..Q4 with anchors 244/256/274/364 + location notes]}]}`)
written next to the scratch snapshot, then the canonical committed instrument run against it:

```
$ python3 corpus/instruments/source-recheck.py --manifest $S/manifest.json --source S054
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=244-ok
S054:Q2 OK occurrences=1 anchor=256-ok
S054:Q3 OK occurrences=1 anchor=274-ok
S054:Q4 OK occurrences=1 anchor=364-ok
source-recheck positive exit=0
```

Exactly the claimed shape: **exit 0, each Q `occurrences=1`**, sha256 bound.

## 5. Controls (instrument sanity + false-green guard)

`capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`, exit 0.
`source-recheck.py --selftest` → all 10 cases PASS (clean / corrupt / missing-source /
missing-manifest / stem-mismatch / double-occurrence / double-occurrence-anchored /
double-occurrence-out-of-range / double-occurrence-broken / quote-absent):
`selftest cases=10 failures=0`, exit 0.

Negative control (this seat): scratch manifest with Q3's page typo silently "corrected"
(`decisions point values` → `decision point values`) must NOT pass:

```
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=244-ok
S054:Q2 OK occurrences=1 anchor=256-ok
S054:Q3 MISMATCH reason=quote-not-found
S054:Q4 OK occurrences=1 anchor=364-ok
source-recheck negative exit=1
```

The harness genuinely binds: a corrected-typo quote is rejected, so the committed manifest must
quote the page's typo **verbatim**.

## 6. Risks / residual

1. Counts and anchors bind to `ff3f3b2c…fdce21` (both my 17:13:12Z fetch and the sibling's 17:02:11Z
   fetch). Any later page drift changes the digest; then the capture, sha256, and anchors must be
   re-derived together (the digest, not the URL, is the pin).
2. Q1 is a 22-word mid-sentence cut ending `or exploitability` (the full sentence is 40 words); do not
   "fix" it with an ellipsis — matching is literal.
3. Q3's `decisions point values` is the page's own typo; a corrected reading fails (§5 negative control).
4. The home page `https://certcc.github.io/SSVC/` (frozen-claims literal, superseded by erratum-1)
   contains **none** of the four quotes — if any manifest/capture still points there, recheck fails;
   erratum-1's overview URL is the only satisfiable binding.
5. `Carnegie Mellon` appears only in the site footer; attribution claims should not lean on S054 prose.

## 7. Verification summary

- Contract extracted from committed instrument bytes (§2), not from prose claims.
- Live satisfiability proven with a fresh fetch (§3): status 200, digest stable across seats.
- Positive control exit 0 with `occurrences=1` ×4 (§4); negative control exit 1 (§5); both instruments
  self-test clean (§5). The C2 `source-recheck S054 exit 0` claim is executable exactly as specified
  in §2.3 once the round-37 capture + manifest land.
- Tooling: none installed or upgraded (python3 stdlib + lane instruments only). Scratch removed.
