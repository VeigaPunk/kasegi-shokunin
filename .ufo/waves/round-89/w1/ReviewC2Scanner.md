# ReviewC2Scanner — round 89 C2 code and source review

Reviewed at the frozen commits: base `090a46f8`, freeze `94573d25`, C1 `eb5f0df8`, C2 `c61c5586`.
Instrument and allowlist at the landing are byte-equal to `.ufo/waves/round-89/c2/candidate/*` (P2), the
C1→C2 diff is exactly the three declared paths (P3), and an independent `--rev` scan at `c61c5586`
prints `scanned=1530 hits=0 files=0 allowed=20 unused_allow=0 rc=0`. The base instrument at the same
rev prints `allowed=18 unused_allow=2`, so the two new rows are the only new consumers.
Receipts: `ReviewC2Scanner-receipts/c2-code-source-review-r89.txt`.

**Verdict: CHANGES-REQUESTED** — no finding requires a change to the frozen instrument (P1–P3 hold
under my own re-run, and the pattern does what the statement says on every falsifiable clause); the
changes are documentation/counter binding, routed to round 90.

## What holds (verified, so the L1 need not re-derive it)

- **Docstring ↔ code is exact on all eight falsifiable clauses**: 40-character floor (39 miss, 40 hit),
  url-safe class `[A-Za-z0-9_~-]` and the `+ → -`, `= → _`, `/ → ~` order of S128:206-211, `[A-Z0-9]{8,32}`,
  either order, `_SEP` = `&|&amp;|\u0026`, case sensitivity, the 20-intervening-parameter ceiling
  (20 hit, 21 miss — the Known-limits sentence is literally correct), and `X-Amz-Signature` never
  starting a match. The new docstring citations (S128:13, :70-78, :202-211; S130:14, :75-84, :163-165)
  all resolve to the claimed bytes.
- **Allowlist is correct and load-bearing**: the match in both snapshots is 209 bytes
  (`Signature=…&Key-Pair-Id=…`, sha256 `f8d573cb…`), recomputed independently and equal to both rows;
  the reason cell's two assertions hold. The rows are the reason the landing scan is clean.
- **r88 F1 is really fixed, with no regression**: the S127:605 order JSON-escaped (`sv` sixth) hits
  `azure-sas-signature` on the candidate and not on the base; `_LB`'s first alternative is the old
  `(?<![A-Za-z0-9_])` verbatim, so no previous match is lost. `%26` is reachable only for a
  partially percent-encoded URL (`?u=x%26sv=…&sig=…` hits; `?sv=…%26sig=…` does not).
- **No false positive found.** Clean on: `X-Amz-Signature` beside `Key-Pair-Id` (both orders),
  CloudFront cookie form as query string and as a `Cookie` header, `Signature=` without
  `Key-Pair-Id`, `Key-Pair-Id` without `Signature=`, Azure/GCS `Signature=` without `Key-Pair-Id`,
  the S128/S130 step-list prose, OAuth/XML/SAML `Signature=`.
- **Cost is safe**: 1530 captures in 1.42 s (base 1.06 s); six adversarial 1–3.5 MB blobs finish in
  ≤0.40 s with no superlinear growth; no `SyntaxWarning` from the docstring escapes.

## Findings

### F1 — HIGH (routed to r90): the capability's knowledge entry now contradicts the instrument, and
### 30 of its 43 line references resolve to unrelated bytes
`corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` at `c61c5586`.
Every one of these references resolved **correctly at base**; the C2 insertion (+18 docstring lines,
+7 pattern lines) moved them: 11 of its 16 `capture-secret-scan.py:N` refs point at unrelated bytes
(two more now truncate, three still resolve), and 18 of 27 bare `:N` refs are wrong — 29 of the
entry's 43 references (full table, with the correct landing target for each, in the receipt §7). Samples:
doc:86 cites `:87` for the Azure left boundary — landing line 87 is `import os`; doc:212/225 cite
`:84-87` for the two cloud patterns — landing 84-87 is `import argparse`; doc:83 cites `:235` for the
`gcs-doc-wrapped` case — landing 235 is `results, used, allowed = [], set(), 0`; doc:82 cites `:242`
for `azure-sig-without-sv` — landing 242 is blank (correct 270); doc:74 cites `:57-61`/`:182-194`/`:191`
for the output and `report()` — landing reads the CloudFront bullet, `if not rec:`, and a `cat-file`
comment.

Four of those citations also carry a statement that is now false, which is worse than a wrong line
number:
1. doc:78 — "**Named limits**, verbatim from `…:43-45`: GCS V2 `Signature=` and CloudFront
   `Signature=`/`Key-Pair-Id=` URLs … are not detected." Landing 43-45 is the round-89 Azure paragraph,
   the quoted words are no longer in the file, and CloudFront signed URLs *are* detected.
2. doc:86 — "the `\u0026` clause holds only when the matched `sv=` or `sig=` is the first query
   parameter … `%26` separators are never recognised." Both halves are false at the landing.
3. doc:213 — "the named limits … exclude GCS V2, CloudFront, percent-encoded parameter names and
   wrapped captures." CloudFront is no longer excluded.
4. doc:221 — "Two providers, one form each." Three shapes now.

**Fix (r90):** repoint the tables in receipt §7 and rewrite those four sentences (Known limits =
`:61-65`, `\u0026`/`%26` now matched, three providers). Note `presigned-url-…md:69`
("instrument lines 57-62" → 77-82) is the one C2-caused break in the second entry;
`presigned-url-…md:33-36` and `:44-45` were already wrong at base and belong in the same sweep.

### F2 — MEDIUM (routed to r90): the statement's `%26` limb has no K8 clause and no plant, and the
### SCORECARD row drops it
The frozen statement says the Azure shape "matches after a `\u0026` or `%26` separator in any parameter
position"; the docstring says the same (lines 43-46); `_LB` implements it (line 103). But `CLAUSES` in
`.ufo/waves/round-89/c2/capability-check.py` has ten entries, none mentioning `%26`, and every Azure
plant (`E3.json`, `live-c`, `live-g3`) uses `\u0026`. `SCORECARD.md`'s row states only "after a
JSON-escaped `\u0026` separator". So "K8 maps every statement clause to a plant" is false by one
clause — the r88 M88-2 class, recurring in miniature.
**Fix:** add one clause+plant (`?u=x%26sv=2022-11-02&sig=<40+>` hits; `?sv=…%26sig=…` misses) **or**
delete `%26` from the statement and the docstring and from `_LB` — do not leave the two saying
different things.

### F3 — MEDIUM: a `Key-Pair-Id` longer than 32 characters is a silent *total* miss, untested and
### unlisted
`Key-Pair-Id=[A-Z0-9]{8,32}(?![A-Za-z0-9_-])` (line 107). Verified: 8, 15, 20 and 32 hit; 33 does not
match at all — every shorter split fails the lookahead, so the URL is missed even though a valid
`Signature=` is present. The shape line states 8-32, but the Known-limits paragraph (61-65) does not
list the ceiling, the selftest has no `Key-Pair-Id` length case, `K7` draws ids of 13-21 characters
and `K4`'s plant is 15, so nothing can discover it. `[INFERENCE]` no documented CloudFront id length
in the frozen sources (S128 shows 15; the root-key-pair form is 20) — the risk is small, the silence
is not.
**Fix:** list the ceiling in Known limits and pin `cf-kpi-33` as not detected; decide explicitly
whether the lookahead's all-or-nothing semantics are wanted.

### F4 — LOW: three verified misses are absent from Known limits (the list is otherwise exact)
(a) a `Signature` value that retains base64 `+`, `/` or `=` (not url-safe-translated) — no match;
(b) a HAR/DevTools structured query array (`{"name":"Signature","value":…}`) — no match, a real
capture shape for this lane; (c) a percent-encoded signature *value* (`%2B`, `%2F`) — no match.
Separately, the CloudFront paragraph omits that its own left boundary also admits a preceding `%26`
(line 104); only the Azure paragraph documents that.
**Fix:** three lines in Known limits (plus the `%26` note for the CloudFront shape), or one clause each
in a later round.

### F5 — LOW: registry drift on S130
`corpus/SOURCES.md` at the landing: S128 `mined` (used-by = the instrument + the knowledge entry),
S130 `queued` with used-by `—`, although the instrument now implements S130's shape. The round-88
landing flipped S126/S127 to `mined`; P3 forbade the edit here.
**Fix:** flip S130 to `mined`, used-by = `corpus/instruments/capture-secret-scan.py` (+ the knowledge
entry once F1 lands).

## Residual risk and verification gaps

- No live URL was exercised (lane prohibition): the S128/S130 documented example is the only
  real-shaped CloudFront URL available, so nothing here measures a URL that a signer actually emitted.
  An ECDSA-signed URL (~88-character signature) is inferred to pass the 40-floor; no sample exists.
- The allowlist row binds the whole 209-byte span, not just the signature value: a future capture of
  the same AWS page with `Signature` and `Key-Pair-Id` reordered, or with `Hash-Algorithm` moved
  between them, produces a different digest and a new HIT. That is the designed behaviour
  (one exact matched byte string per path), but it means a re-capture is not automatically quiet.
- The `%26` reachability conclusion is fixture reasoning; no capture in the corpus uses `%26` as a
  query separator, so F2's plant would be synthetic by construction.
- I did not run the full C2 counter (its controls take ~12 min): I re-ran P2, P3, the landing scan,
  the selftest and the allowlist consumption directly. `K6`'s "base instrument misses the additions"
  is a by-construction limb, as the claims file already records.
- Nothing here re-scores C2; coverage is 8 held at the landing, and F1–F5 are routed defects.
