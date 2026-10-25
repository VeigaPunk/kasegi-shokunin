# CaptureTool — round-24 capture set: contract, instrument, receipts

Seat: L1Kasegi24.CaptureTool (executor, private clone `/tmp/kasegi-r24-CaptureTool`, clone HEAD
`c2480b143120364728b40397926ffcf30a7309c8` = lane `master`). Observed = a command I ran; anything
unrun is marked `[INFERENCE]`.

Files in the clone (nothing committed, nothing pushed, no lane file edited by this seat):

- `corpus/instruments/capture-source.py` (886 lines)
- `corpus/source-snapshots/round-24/capture-plan.json` (15 documents, 51 quotes)
- `corpus/source-snapshots/round-24/manifest.json` (19 records: S001-S015 repaired, S032-S035 byte-identical to the live manifest)

## 1. Findings first

**F-1 (depth:verifiability, live defect).** The live round-24 manifest carries three quote assertions
that fail the round's own contract (5-25 words, exactly once under `normalize()`):

| id:qid | live text | measured |
|---|---|---|
| `S015:Q2` | `Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')` | `AMBIGUOUS count=2` (table row + card on the same page) |
| `S009:Q1` | `Where should I start?` | 4 words |
| `S012:Q1` | `Published May 22, 2026` | 4 words |

Evidence: `python3 /tmp/kasegi-r24-CaptureTool/corpus/instruments/capture-source.py --manifest
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-24/manifest.json --verify`
→ `S009:Q1 SHORT words=4-outside-5-25`, `S012:Q1 SHORT words=4-outside-5-25`,
`S015:Q2 AMBIGUOUS count=2`, exit 1. `source-recheck.py` on the same bytes exits 0: containment-only
scoring cannot see either defect (see §4 control). All three are repaired in the candidate manifest;
digests and the other 48 assertions are untouched.

**F-2 (instrument gap, closed).** `source-recheck.py` accepts a quote that matches twice
(`assertion["quote"] in source_text`), and cannot see a one-token quote: `{"quote": " "}` passes. The
round-24 requirement "exactly-once under normalize()" therefore lives only in the capture instrument.
`capture-source.py --verify` now enforces it and the selftest proves the divergence
(`rechecker-accepts-ambiguous-quote` exit 0 vs `verify-quote-twice-fails` exit 1, same manifest).

**F-3 (metric, recorded not ticketed).** A whitespace word-count is meaningless for Japanese: one
sentence is one token. The live `S033`/`S034`/`S035` quotes measure 1 "word" each. They are *not*
defective on that basis; a CJK quote is now measured in CJK characters (10-120) instead, and all 29
S032-S035 quotes pass unchanged. Any reviewer re-deriving "quote too short" from a word count will
produce false positives on F09's evidence.

**F-4 (coverage).** F01-F05 entry `recheck:` lines already point at
`corpus/source-snapshots/round-24/manifest.json`; all five chains exit 0 on live lane bytes
(§5). Counter A is green today; this seat's change is depth, not liveness.

## 2. Manifest schema contract (read from the loader, then probed)

`source-recheck.py:43-145`. Two levels.

**Global (`load_manifest`), evaluated in order, any failure ⇒ exit 2 and *every* `--source` call
fails:** UTF-8 JSON object; `schema_version` is a JSON **int** `== 1` (`type(...) is int` rejects
`true`/`"1"`/`1.0`); `sources` is a **non-empty** list; each record is an object with an `id`
matching `[A-Za-z0-9][A-Za-z0-9._-]*\Z`; record ids unique.

**Per record (`check_source`), checked only when that record is selected or reached:** `path` str,
non-empty, not absolute, and after `resolve(strict=True)` still inside the manifest's own directory
(`os.path.commonpath == base`, so `../round-23/S018.txt` and symlinks out are `outside-manifest-directory`);
`sha256` matching `[0-9a-f]{64}\Z` (exactly 64 lowercase hex); `quotes` non-empty list; each quote an
object with an `id` (same RE, unique within the source) and a non-empty `quote` str.

Unknown keys are ignored at every level (`purpose`, `url`, `entry`, `captured`, `page`, `location`
are free). Field-level failure lines and exit codes: `{id}:manifest UNAVAILABLE reason=invalid-path |
invalid-sha256 | missing-quotes | duplicate-quote-id` → 2; `{id}:source UNAVAILABLE reason=missing |
not-utf8 | outside-manifest-directory` → 2; `{id}:sha256 MISMATCH expected=… actual=…` → 1;
`{id}:{qid} MISMATCH reason=quote-not-found` → 1. Quotes are checked `sorted` by id, so `Q10`
precedes `Q2`.

Skeleton (exact shape this seat emits via `--plan ... --skeleton`, one record shown, digest nulled):

```json
{
  "schema_version": 1,
  "round": 24,
  "purpose": "…",
  "ceiling": "…",
  "sources": [
    {
      "id": "S001",
      "url": "https://www.first.org/cvss/v4.0/user-guide",
      "entry": "corpus/knowledge/cvss-v4-severity-and-vector.md",
      "path": "S001.txt",
      "sha256": null,
      "captured": "2026-10-25",
      "quotes": [
        {"id": "Q1", "quote": "…5-25 words…", "location": "…"}
      ]
    }
  ]
}
```

`null` is deliberately not a valid `sha256`, so a skeleton rechecked with `--verify` exits 2
`reason=invalid-sha256` — it can never pass as captured bytes
(`SELFTEST skeleton-shape-and-fail-closed PASS`).

## 3. Instrument

`corpus/instruments/capture-source.py` — superset of the live per-document tool, same extractors
(`collapse`/`html_to_text`/`pdf_to_text`), same receipt line, so re-capture reproduces committed
bytes.

```
--id/--url/--out [--kind html|pdf|text]   capture one document, print sha256 receipt (unchanged CLI)
--plan P --capture                        fetch every plan document, extract, refuse the whole set if
                                          any quote is not exactly-once, then merge records into the
                                          manifest beside the plan (unnamed records preserved)
--plan P --check                          offline: re-hash snapshots vs manifest, re-count quotes
--plan P --skeleton                       manifest shape with null digests
--manifest M --verify                     offline: digest + exactly-once + length window (stricter
                                          than source-recheck.py)
--selftest                                offline controls over file:// URLs
```

Exit codes 0 / 1 (capture-or-verify mismatch) / 2 (malformed input). Fail-closed on refusal: nothing
is written when any source fails (`capture REFUSED failed-sources=N wrote=nothing`).

Selftest receipt (`python3 corpus/instruments/capture-source.py --selftest`, 17/17 PASS, exit 0):

```
SELFTEST normalize-deterministic PASS got='Alpha beta\ngamma\n'
SELFTEST capture-single-document PASS exit=0
SELFTEST capture-plan-and-merge PASS exit=0 ids=S901,S902,SA01
SELFTEST verify-clean PASS exit=0
SELFTEST rechecker-accepts-schema PASS exit=0
SELFTEST check-plan-offline PASS exit=0
SELFTEST verify-doctored-sha-fails PASS exit=1
SELFTEST verify-edited-body-fails PASS exit=1
SELFTEST capture-quote-twice-refused PASS exit=1
SELFTEST verify-quote-twice-fails PASS exit=1
SELFTEST rechecker-accepts-ambiguous-quote PASS exit=0
SELFTEST capture-quote-absent-refused PASS exit=1
SELFTEST capture-short-quote-rejected PASS exit=2
SELFTEST verify-missing-snapshot-fails PASS exit=1
SELFTEST verify-bad-schema-rejected PASS exit=2
SELFTEST verify-duplicate-id-rejected PASS exit=2
SELFTEST skeleton-shape-and-fail-closed PASS exit=0 verify-exit=2
```

The two required negatives are `verify-doctored-sha-fails` (one hex digit changed → `S901:sha256
MISMATCH`, exit 1) and `capture-quote-twice-refused` / `verify-quote-twice-fails` (`count=2` →
exit 1, and no snapshot or manifest written).

## 4. Control: the lane instrument accepts what the strict one refuses

Same manifest bytes, one field apart, both instruments run:

```
$ python3 corpus/instruments/source-recheck.py --manifest /tmp/r24-gap/manifest-ambiguous.json --source S015
S015:sha256 OK
S015:ambiguous-control OK normalized=markup-whitespace      ← quote occurs twice
exit=0

$ python3 corpus/instruments/capture-source.py --manifest /tmp/r24-gap/manifest-ambiguous.json --verify
S015:ambiguous-control AMBIGUOUS count=2
exit=1
```

The ambiguous quote is `CVEs in KEV: 7 Rank Last Year: 1`, which also matches CWE-94's
`Rank Last Year: 11` by prefix — the real failure mode, found by the capture gate on its first run.

## 5. Coverage table — 15 ids → URL → snapshot → assertions

Counts are the candidate manifest's; every quote measured `count=1` against the committed snapshot.

| id | URL captured | snapshot | quotes | backs |
|---|---|---|---|---|
| S001 | https://www.first.org/cvss/v4.0/user-guide | S001.txt | 4 | cvss-v4-severity-and-vector.md |
| S002 | https://www.first.org/cvss/v4.0/specification-document | S002.txt | 7 | cvss-v4-severity-and-vector.md |
| S003 | https://www.cisa.gov/sites/default/files/2026-07/joint-guide-establishing-a-cvd-program-to-work-with-security-researchers_508c.pdf (page: /resources-tools/resources/establishing-coordinated-vulnerability-disclosure-program-work-security-researchers) | S003.txt (PDF, `pdftotext -enc UTF-8`) | 3 | coordinated-disclosure-timelines.md |
| S004 | https://certcc.github.io/certcc_disclosure_policy/ | S004.txt | 3 | coordinated-disclosure-timelines.md |
| S005 | https://projectzero.google/vulnerability-disclosure-faq.html | S005.txt | 5 | coordinated-disclosure-timelines.md |
| S006 | https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | S006.txt | 3 | authorization-safe-harbor-and-scope.md |
| S007 | https://docs.bugcrowd.com/researchers/disclosure/disclose-io-and-safe-harbor/ | S007.txt | 3 | authorization-safe-harbor-and-scope.md |
| S008 | https://www.cisa.gov/vulnerability-disclosure-policy-template | S008.txt | 3 | authorization-safe-harbor-and-scope.md |
| S009 | https://www.ncsc.gov.uk/blogs/10-questions-ask-using-ai-models-find-vulnerabilities | S009.txt | 2 | ai-assisted-finding-validation.md |
| S010 | https://projectzero.google/2024/06/project-naptime.html | S010.txt | 3 | ai-assisted-finding-validation.md |
| S011 | https://blog.cloudflare.com/cyber-frontier-models/ | S011.txt | 2 | ai-assisted-finding-validation.md |
| S012 | https://www.anthropic.com/research/glasswing-initial-update | S012.txt | 3 | ai-assisted-finding-validation.md |
| S013 | https://cwe.mitre.org/top25/archive/2025/2025_methodology.html | S013.txt | 4 | cwe-top25-2025-methodology.md |
| S014 | https://cwe.mitre.org/top25/archive/2025/2025_key_insights.html | S014.txt | 4 | cwe-top25-2025-methodology.md |
| S015 | https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html | S015.txt | 2 | cwe-top25-2025-methodology.md |

Total 51 assertions over 15 snapshots (live set: same 51 ids, three of them repaired). S003's record
also carries the publication page as `page`, because the quoted material is in the linked 508c PDF,
not the page body.

## 6. Receipts

Candidate assembled at `/tmp/r24-final` (committed snapshots + candidate manifest + plan), lane root
untouched.

```
$ python3 capture-source.py --manifest /tmp/r24-final/manifest.json --verify
… 77 quote lines "OK count=1", 19 "…:sha256 OK" …                     exit=0
$ python3 capture-source.py --plan /tmp/r24-final/capture-plan.json --check
… 51 quote lines "OK count=1", 15 "…:sha256 OK" …                     exit=0
$ python3 corpus/instruments/source-recheck.py --manifest /tmp/r24-final/manifest.json
96 lines (19 sha256 + 77 quotes)                                      exit=0
$ for s in S001..S015; do source-recheck.py --manifest … --source $s; done
S001=0 S002=0 S003=0 S004=0 S005=0 S006=0 S007=0 S008=0 S009=0 S010=0
S011=0 S012=0 S013=0 S014=0 S015=0
```

Counter A on live lane bytes (entries already repointed to `round-24/manifest.json`):

```
$ for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines \
           authorization-safe-harbor-and-scope ai-assisted-finding-validation \
           cwe-top25-2025-methodology; do r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //'); \
  bash -c "$r" >/dev/null 2>&1; echo "$f $?"; done
cvss-v4-severity-and-vector 0
coordinated-disclosure-timelines 0
authorization-safe-harbor-and-scope 0
ai-assisted-finding-validation 0
cwe-top25-2025-methodology 0
```

Re-runnable capture, proven from upstream into an empty manifest copy (`/tmp/r24-repro`): all 15
plan sources re-fetched and re-extracted to the **committed digests, zero drift**; the four non-plan
records (`S032-S035`) came through the merge byte-identical
(`carried-unmodified: ['S032','S033','S034','S035']`, `digest-equal: 15`). Rechecker exit 0 on the
reproduced manifest as well.

## 7. What L1 has to integrate (this seat wrote only the three clone files)

1. Replace `corpus/source-snapshots/round-24/manifest.json` with the clone's, or apply the diff:
   `S009:Q1` → `You should also look for ways to verify the results, by using both AI and humans.`;
   `S012:Q1` → `90.6% (1,587) have proved to be valid true positives`;
   `S015:Q2` → `CWE-79 CVEs in KEV: 7 Rank Last Year: 1`; plus `url`/`entry`/`captured` (and
   `page` on S003) on S001-S015. No digest, path, or S032-S035 record changes.
2. Replace `corpus/instruments/capture-source.py` with the clone's (keeps the existing
   `--id/--url/--out` CLI and receipt line; adds `--plan --capture|--check|--skeleton`, `--manifest
   --verify`, and the 17-case `--selftest`). Copy `capture-plan.json` beside the manifest.
3. Regenerate `.ufo/waves/round-24/c1-counterA-manifest-receipt.txt`: its `occurrences=2 anchor=64-ok`
   line records the S015 ambiguity as accepted, and three quote texts change. After integration that
   receipt should read `occurrences=1` for all 77 assertions, or the integration lost a repair.
4. `S033`/`S034`/`S035` remain as found: 1-token Japanese quotes, exactly-once, 10+ CJK characters.
   Not this seat's scope; flagged so nobody "fixes" them into longer captions that no longer match.

## 8. Risks and limits

- **`S014` URL.** The live manifest has no `url`; the row above uses `2025_key_insights.html`
  (the page actually fetched and hashed). An earlier plan draft typo'd `2025_keyinsights.html`; the
  committed snapshot is unaffected, but do not copy the typo into `SOURCES.md`.
- **Digest ≠ freshness.** The pins bind captured bytes; a 2026-11 upstream edit drifts the digest and
  the gate fails closed, which is the intended behaviour, not a bug to paper over.
- **Location binding is human.** Uniqueness proves a sentence occurs once, not that it sits at the
  rule the entry names; `location` is a hint the instrument never reads.
- **`S003` needs `pdftotext`** (present at `/usr/bin/pdftotext`, poppler, already installed). No
  package was installed, upgraded, downgraded or removed by this seat; no `pacman` invocation ran.
- **Clone-only.** Nothing committed or pushed; no lane file, sibling lane, `.ufo/state`, `MANIFEST.json`
  or `/home/vgpnk/Projects/shokuknow` byte was written. Only `/tmp` scratch and this report.
