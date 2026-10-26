# ScoutReopenS057 receipt (round 39, leaf scout; judged depth:verifiability, coverage)

Result: S057 re-opened live; page and PDF unchanged since round 38; normalized PDF text byte-identical to ExecFrontierCapture's capture.

| item | value |
|---|---|
| page | HTTP 200, 54453 B, sha256 4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d, fetched 2026-10-26T19:30:41Z |
| page publication date | `<time datetime="2023-11-06T12:00:00Z">November 06, 2023</time>` (Publish Date field); other datetimes (2026-10-22/16, 2026-09-16) are related-content cards |
| PDF | HTTP 200 application/pdf, 235270 B, sha256 cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99, fetched 2026-10-26T19:30:54Z, Last-Modified Mon, 06 Nov 2023 15:43:40 GMT |
| normalized text | capture-source.py pdf_to_text() imported read-only; 275 lines, 17971 B, sha256 11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f |
| compare | `cmp` vs .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt exit 0 (identical); vs ExecFrontierCapture scratch S057.txt also identical |
| committed capture | corpus/source-snapshots/round-39/S057.txt not present in the lane when checked (the L1 lands it); wave1 file used as stand-in; the L1 should re-run `cmp` or sha256 against the committed path |

Deliverable: .ufo/waves/round-39/wave1/ScoutReopenS057.reopen.txt (13 lines, 1653 bytes, sha256 278e76d64f20f579225c7c6ed8b88726bba5286d4fefa2a5c843e95f91ebbefa). No lane/fleet file other than my wave1 files was written; no tools installed; scratch removed.
