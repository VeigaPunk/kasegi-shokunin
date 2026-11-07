# ScribeEntry — round-89 knowledge-entry extension for the CloudFront shape

Seat: ScribeEntry (leaf). Round 89, attempt 1, wave w1. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Task: draft the full candidate replacement of `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` adding the Amazon CloudFront signed-URL section, and list the checks run. Not integrated: the L1 integrates.

## Deliverable

- `.ufo/waves/round-89/w1/ScribeEntry-candidate/cloud-signed-url-credentials-in-captured-evidence.md` — 336 lines, 50,267 bytes, sha256 `2533abb573160a09685dc9a91788be7c1c2a1bbfe342f34c57be49c95bf6d99c` (the current lane entry is 228 lines, 30,771 bytes, sha256 `6ba7e7ac…`; the candidate is a byte copy of it plus the edits below, so every unedited line is byte-identical).
- `.ufo/waves/round-89/w1/ScribeEntry-receipts/checks-r89.txt` — measured outputs of every check below.
- This report.

## Behaviour of the candidate

1. **Header.** `source:` now names S128 and S130 with URLs, anchors, capture size/line count, sha256 and the manifest quote ids/anchors (`occurrences=1` each). `verified-at:` keeps the round-88 re-open and appends the round-89 re-open (digests, `source-recheck` lines, scanner line). `recheck:` keeps the four round-88 commands and chains the two round-89 `--source` rechecks plus the round-89 `--files` scan; the whole line parses under `bash -n` and carries its own `cd` prefix.
2. **Title** names three providers and "all three shapes" (was "both shapes").
3. **Attribution** gains the AWS paragraph (S128/S130 are AWS's own pages, `corpus/SOURCES.md:140`, `:142`, tier A; CloudFront signed URLs only, not signed cookies or S3 presigned URLs) and the round-89 provider-count sentence.
4. **New `## Claim 7`** (inserted after Claim 6, so Claims 1–6 keep their numbers): the two parameter sets (canned `Expires`/`Signature`/`Key-Pair-Id`, custom `Policy`/`Signature`/`Key-Pair-Id`, optional `Hash-Algorithm`), the URL-safe replacement (`+`→`-`, `=`→`_`, `/`→`~`, S128:206-211), the bearer statement (S130:163) with its `Resource`-omission qualifier, the trust anchor (`Key-Pair-Id`, S128:82-83), the scanner shape `cloudfront-signed-url-signature` and seven named limits. Every quote cites `corpus/source-snapshots/round-89/S128.txt:<line>` or `S130.txt:<line>` and the source id; the vendor example signature is cited by line span only (`S128.txt:13`, `S130.txt:14`), never by value.
5. **Claim 5** gains the CloudFront shape bullet and the round-89 allowlist rows, and its instrument citations are repointed to the landed instrument (see "facts that moved").
6. **Two new check blocks**: FC-8 (15 CloudFront quote spans, `normalized=whitespace`) and FC-9 (the shape's four detected / five clean selftest cases, the two captures clean under their two allowlist rows, and the base control's `new_caught_by_base=none`).

## Facts that moved, and the existing text changed for them

Everything else in Claims 1–6 is byte-identical. The changed facts:

| fact | old | new | why |
|---|---|---|---|
| instrument line numbers | `:1-62`, `:14-19`, `:19-21`, `:23-45`, `:32-36`, `:37-42`, `:43-45`, `:46`, `:48-53`, `:53-55`, `:57-61`, `:62`, `:80-87`, `:81`, `:84-85`, `:84-87`, `:86-87`, `:87`, `:89`, `:90`, `:182-194`, `:191`, `:233-240`, `:235`, `:236`, `:241`, `:242`, `:243` | `:1-82`, `:14-21`, `:20-21`, `:23-60`, `:32-36`, `:37-46`, `:61-65`, `:66`, `:68-75`, `:73-75`, `:77-81`, `:82`, `:99`, `:100`, `:101`, `:103`, `:104`, `:106`, `:106-107`, `:106-114`, `:109-110`, `:111-112`, `:116`, `:117`, `:209-221`, `:218`, `:261-281`, `:263`, `:264`, `:269`, `:270`, `:271`, `:272`, `:273-276`, `:277`, `:278`, `:279`, `:280`, `:281` | the instrument grew at C2 landing `c61c5586`; every repointed line was read back and prints the cited text (receipt §12 and the resolution table in this seat's transcript) |
| named limits | "GCS V2 `Signature=` and CloudFront … not detected" | verbatim `:61-65`: GCS V2 `GoogleAccessId=`/`Signature=`, CloudFront signed cookies, percent-encoded names or `=`, >20 parameters, soft-wrapped values, gzip/UTF-16/base64 | CloudFront signed URLs are now detected; the limit set changed |
| Azure `\u0026` limit | "holds only when the match starts at the first query parameter; `%26` never recognised" | closed: `_LB` (`:103`) admits a match after `\u0026`/`%26`; selftest `azure-json-escaped-s127-order` (`:272`) pins S127's order; `%26` remains a left boundary only, not a separator | round-89 fix of the r88 F1 defect |
| shape count | two AWS + two cloud | two AWS + three cloud (adds `cloudfront-signed-url-signature`) | C2 capability extension |
| allowlist | 17 rows at r88 | 19 rows; the two round-89 rows bind AWS's CloudFront example at the two snapshot paths (`capture-secret-allow.tsv:21-22`) | C2 landing added two rows |
| `unused_allow` in FC-3/FC-7 | 17 | 19 | measured on the landed allowlist |
| instrument pin in FC-5 | `d7349536…` | `95f24a54…` (`c2-landing-r89.txt:4`) | C2 landing |
| provider scope | two providers | three providers; CloudFront signed cookies excluded | new sources |
| redaction blocks | r88 only | r88 and r89 both 0 (FC-6 extended) | new manifest |

Claims 1–4's quoted spans and prose are unchanged except Claim 3's pattern citation (`:81`, `:86-87` → `:101`, `:111-112`), which is the same fact at the new instrument offsets.

## Checks run (all from the lane root, `TMPDIR` in scratch)

| check | command | result |
|---|---|---|
| FC-1 (r88 quotes) | extracted from the candidate and run | `QUOTE-CHECK pass spans=11 bad=0`, rc 0 |
| FC-2 (missing/corrupt source) | extracted and run | `missing_rc=2`, `corrupt_rc=1` |
| FC-3 (r88 captures clean) | extracted and run | `scanned=2 hits=0 allowed=0 unused_allow=19 rc=0` |
| FC-5 (provider scope + pin) | extracted and run | the five counts in the entry and `95f24a54…` |
| FC-6 (redaction blocks) | extracted and run | `r88_redaction_blocks=0`, `r89_redaction_blocks=0` |
| FC-7 (wrapped GCS) | extracted and run | `HIT shape=gcs-signed-url-signature … rc=1`, `joined_rc=1` |
| FC-8 (15 CloudFront spans) | extracted from the candidate and run | `QUOTE-CHECK pass spans=15 bad=0`, rc 0 |
| FC-9 (shape load-bearing) | extracted and run | nine `SELFTEST cf-… ok`, `SELFTEST-RESULT pass cases=43`, `scanned=2 hits=0 allowed=2 unused_allow=17 rc=0` |
| candidate hygiene | scanner `--files` on the candidate and the receipt | `scanned=2 hits=0 … rc=0`; `Signature=` 12+, `sig=` 16+, AKIA/ASIA, private-key header, `token=`/`secret:` 16+ all 0 |
| recheck form (Q10) | `sed -n '5p'` → `bash -n` | rc 0 |
| line anchors (R6) | `awk 'NR==39'` | still the Claim 3 HMAC quote cited by `.ufo/waves/round-88/w1/ScoutSources.md:113`; lines 1–13 keep their numbers |
| source re-open | `source-recheck.py --manifest …round-89… --source S128` / `S130` | `sha256 OK` + 3 and 2 quote lines, rc 0 each |

Threshold/separator probes (scratch fixtures with generated values, deleted with the scratch dir; only HIT/summary lines recorded): 39-char signature not detected / 40 detected; `Key-Pair-Id` 7 not / 8 detected; 20 intervening parameters detected / 21 not; Azure `%26` left boundary with `&` inside detected, all-`%26` query not; CloudFront `\u0026` left boundary detected, `%26`-joined not.

## Findings routed (qualifiers, not re-scoring)

1. **The docstring's `%26` clause is narrower than it reads.** `%26` is a left boundary only (`_LB`/`_CF_LB` at `:103`/`:104`); `_SEP` (`:99`) is `&`, `&amp;`, `\u0026`. A query whose parameters are all `%26`-joined is not detected (measured). The candidate says this in Claim 5 and Claim 7 rather than repeating the docstring's broader wording.
2. **The CloudFront example is expired.** S128's own conversion dates `Expires=1767290400` at 2026-01-01 10:00 UTC, before the 2026-11-07 capture, so the documented example URL is outside its own window. This is a second, independent reason the allowlist row is safe.
3. **The two round-89 captures read clean only by allowlist** (`allowed=2`), because both carry AWS's documentation example signature. A capture of a real URL has no row and reads as a hit.
4. **CloudFront signed cookies are outside the shape** (`CloudFront-Signature`), as are `Signature=`-only fragments (no `Key-Pair-Id=`), lowercase parameter names, <40-char signatures and >20 intervening parameters — all pinned in the selftest.
5. **No lane file was edited outside the wave dir**; the candidate is a draft and the L1 integrates. No credential-shaped value is in any file written by this seat (scanner clean on both).

## Out of scope

No live target was contacted; no CloudFront signed-cookie capture, account SAS, user-delegation SAS or GCS V2 is covered; no HAR bytes are measured; the C2 counter and its controls script were not run (the landing receipt was read, not re-executed); no product code, judge, commit, push or deploy. No tool was installed or upgraded.

## Files written

- `.ufo/waves/round-89/w1/ScribeEntry-candidate/cloud-signed-url-credentials-in-captured-evidence.md`
- `.ufo/waves/round-89/w1/ScribeEntry-receipts/checks-r89.txt`
- `.ufo/waves/round-89/w1/ScribeEntry.md`

Scratch `/fast/scratch/hyaku/kasegi-r89/ScribeEntry/` is deleted before this report is filed (fixtures, extracted check blocks and the joined-S126 copy all lived there).
