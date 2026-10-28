# R44Scout1 — F26 candidate recon

## Finding

Uncovered public primary, read 2026-10-28: Apple’s own Apple Security Bounty category page.

- URL: `https://security.apple.com/bounty/categories/` (canonical `link rel="canonical"`; request URL and final URL match; HTTP 200; `text/html`)
- Date: HTTP `Last-Modified: Wed, 16 Sep 2026 00:50:56 GMT`. The body has no publication or revision date. Footer text is `Copyright © 2026 Apple Inc. All rights reserved.` Access time is the response `Date: Wed, 28 Oct 2026 18:59:31 GMT`.
- Quote (11 words), exact, one occurrence in the raw HTML: `Obtaining a specific reward requires confirmation with Target Flags where indicated.`
- Locus: under the heading `Apple Security Bounty Categories`, the first sentence of the paragraph that begins immediately after `<br/><br/>`. Raw body character offset 11165. Instrument-style normalized text (`capture-source.py` `html_to_text`) line 11, first sentence. The same normalized line continues with a second sentence about bonus rewards; that second sentence is not the quote.

Fetch: `User-Agent: kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` (`corpus/instruments/capture-source.py:32`). Raw 130105 bytes, sha256 `b5f01af0b2f5207f22906e8226814a8c052e433b60fc3e50e6668bab1a0e228e`, etag `"6e6acf981c4ab94e7ac5b3f57d8ec0cc"`. Normalized text 190 lines, 10532 bytes, sha256 `b9a641a681e75f9883787d6207cb17f80b46e5c85529e06c7ed8a796c692ef0a`. The quote string count is 1 in the raw body and 1 in the normalized text.

This is a bounty-program rule on Apple’s own site. It is not a CVSS vector (F01), not the HackerOne policy set or Bugcrowd VRT (F13, S043–S045), and not Immunefi’s impact levels (F17, S051).

## Do-nothing

Committed HEAD `66314015122b9aa32dc40f2f1815df56624c26d1` (freeze `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` is an ancestor) still matches the frozen C2 baseline in `.ufo/waves/round-44/controls/do-nothing.txt:9-13`:

- `git grep -cE '^\| F[0-9]+ \| .* \| admitted \|' HEAD -- corpus/README.md` → `HEAD:corpus/README.md:25`
- `git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `68`
- `git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'` → `62`

`git grep -n -E 'security\.apple|…' HEAD -- corpus/SOURCES.md corpus/README.md` printed nothing (`HEAD_NEGATIVE_OK`). A do-nothing replay of those counters cannot emit this URL, this quote, or an F26 row. This seat did not add a frontier row, a registry row, or a knowledge entry.

## Worktree, not this candidate

At the same HEAD, the worktree is dirty: `git status --short` shows `M corpus/README.md` and `M corpus/SOURCES.md`. `git diff -U0 -- corpus/SOURCES.md` adds uncommitted S069 (Google Cloud VRP rules) and rejected S070 (Bug Hunters rules directory). `corpus/README.md:628` is an uncommitted row:

`| F26 | Google Cloud VRP's own program scope, customer-resource testing prohibition and reward-ineligibility boundary | admitted | … | S069 | … |`

`git diff -- corpus/SOURCES.md corpus/README.md | grep -c 'security.apple'` → `0`. A lane-wide search for `security.apple`, `Apple Security Bounty`, and `Target Flag` in `*.md`, `*.txt`, and `*.json` returned no matches. The open F26 draft is a different URL. This recon does not grade that draft.

`/home/vgpnk/Projects/shokuknow/merge/kasegi` has no `security.apple` match (read-only). Sibling lanes were not scanned.

## Limits

The normalized categories page repeats the payout grid three times; the quoted sentence does not. `/bounty/target-flags/` and `/terms-and-conditions/` were not opened. No committed snapshot of this page exists in the lane. No tool was installed (python3, git, and urllib were enough; pacman was not invoked). Scratch `/fast/scratch/hyaku/kasegi-r44/R44Scout1` was removed (`SCRATCH_REMOVED`). C1’s eight defects were not re-counted here.

Report: `.ufo/waves/round-44/wave1/R44Scout1.md`
