# ExecManifest — round-28 wave 1 (coverage / C2)

Scope: built `corpus/source-snapshots/round-28/manifest.json` only. The captures landed while this seat
prepared; the full `source-recheck.py` run on the landed bytes exits 0 with every assertion
`OK occurrences=1`. One fix was needed and is logged in the receipt.

## Deliverable
- `corpus/source-snapshots/round-28/manifest.json`, sha256 `e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`
  (5038 B), schema_version 1, purpose, sources[S041, S042].
- Pins: S041.txt `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (byte-identical to the
  round-26 capture), S042.txt `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`.
- Both records have path stem == id; `location` stays documentation, no `anchor` needed because all 12
  quotes are exactly-once raw and normalized.

## Required assertions present
- S042 Q1 (L145), the step-5 起算日の連絡 body sentence: JPCERT/CC reports the 起算日 and detail-contact
  date to IPA, and IPA relays both dates to the finder.
- S041 Q1 (L340), footnote-4 definition of 起算日 as the date the first contact attempt under Ⅳ．４．2)
  was made; S041 Q2/Q3 (L212/L249), the 図１ flow statement and its caption.

## Evidence
Full run and per-id runs are pasted verbatim in `.ufo/waves/round-28/receipts/ExecManifest.txt`
(exit=0; `--source S041` exit 0; `--source S042` exit 0). A separate Q9 audit outside the instrument
re-derived stems, pins, raw/normalized counts and word counts for all 12 quotes.

## Fix log
First build digest `fa1f366f…` failed with `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`
(the pinned heading normalized to 8 characters, below MIN_QUOTE_CHARS=12; ExecHarnessC2 reported the same
independently). Replaced that quote with the verbatim L145 line; landed digest `e62ddad1…` passes.

## Residual risk
If the capture owner rewrites S041.txt/S042.txt after this pin, the digest line goes MISMATCH; the L1's
re-run command in the receipt detects it. No other production file was touched.
