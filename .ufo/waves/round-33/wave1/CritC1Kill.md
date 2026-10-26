# CritC1Kill — attack review of C1's kill rule and `capture-binding-check.py` (round 33)

Seat: CritC1Kill (leaf; no dispatch). Axes: depth:verifiability (C1 primary), coverage (untouched).
Subject bytes measured, in this order:

- `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79` (21413 B, mtime 2026-10-26 01:19:52 -0300)
- `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` (21527 B) — the digest of record for every
  table below; the executor rewrote the docstring between my first matrix and its reply. Re-ran the whole matrix
  after the change: identical verdicts. Nothing else in the lane moved (manifest digests below).

Erratum read and applied: `.ufo/waves/round-33/claims-erratum-1.md` (per-id row binding, byte match,
`multi_row_url` informational). All fixtures ran under `$HYAKU_SCRATCH/kasegi-r33/CritC1Kill/`; nothing was
written into the lane except this receipt; scratch removed at yield. No tool installed (nothing needed).

## Verdict (what the canonical judge must decide)

1. **The counter is falsifiable and satisfies the kill rule's fake-checker clause.** On committed base bytes
   `690b69da` the real checker prints `records=38 bound=0 unbound=38`, exit 1, and names `round-32` as
   missing-manifest; the frozen fake prints `records=38 bound=38 unbound=0`, exit 0. The fake is rejected.
2. **The predicate is reachable only after `ExecRegistryAppend` lands.** Lane now: 48 registry rows, so
   S049/S050 are `no-row` → `records=40 bound=38 unbound=2`, exit 1 ("PRE-STATE", rule 6). With the two
   contract rows appended to a *fixture copy* the counter prints `records=40 bound=40 unbound=0`, exit 0.
   That fixture figure is **not** an after column; the verifier must re-run on the lane once the rows exist.
3. **The instrument implements erratum-1 correctly, and the erratum is load-bearing.** My independent probe
   of the landed manifests before reading the erratum: global "URL in exactly one row" → 36/40 (S029 and S006
   hit two rows each); id-scoped byte match → 38/40 (only S049/S050 absent). The kill text in `claims.json`
   still contains the global parenthetical ("0 or 2+ matches = failure"); read literally it would reject the
   correct instrument. The L1 must record that erratum-1 governs that clause (two rows per id = `dup-id`;
   a URL shared by two *different* ids is informational `multi_row_url=2`).
4. **The checker's A-C surface has seven measured blind spots (H1-H7), but the one I first judged material —
   capture bytes — is covered by the committed `source-recheck.py`, measured.** I ran `source-recheck.py` over
   all nine manifests: 40 `:sha256 OK` pins, exit 0 each; and its kill of my byte mutants (truncated capture,
   path traversal, missing capture) is sharp (`MISMATCH` exit 1, `stem-mismatch` exit 1, `UNAVAILABLE` exit 2).
   So C1's evidence chain is complete **only when the C1 verdict cites that run**; `capture-binding-check.py`
   alone proves string-level binding, not byte-level. That is a citation/evidence-map gap in the claim, not an
   unreachable predicate. The remaining blind spots (H4-H7) are spec-level or hardening.

## Correspondence with the executor (measured, not accepted on description)

`ExecCaptureBinding` replied twice: holes recorded for an L1 erratum, doc drift fixed, final digest `b4182665`;
and the rebuttal that (a)-(b) are "the byte-integrity gap `source-recheck.py` covers by design", (e) is the
contract's own one-level walk. Re-measured at `b4182665`:

- Byte-integrity rebuttal: **confirmed** — see Verdict 4 and the SR evidence block; 40/40 sha pins pass today.
- "The url-ambiguous class no longer exists, so any mutant built on it is stale": **not confirmed** as a rule.
  `bind_record` still accepts a record whose `url` is *one of several* `https://` tokens in its own row
  (`if url not in row_tokens(own[0])`, line 180). Fixture `x_m16_two_token_row` (row widened with a second
  token; record url = that token) prints `records=40 bound=40 unbound=0`, exit 0. What the executor measured is
  that **all 48 landed rows carry exactly one token** (true, re-measured) — a property of today's data, not of
  the checker. A later registry edit widens binding silently (H7).
- Doc drift I flagged was fixed in the same edit ("eleven fixture lane trees"; the `unbound` field's relation
  to the contract's `<bound-failures>` is now stated). No longer a finding.

## Measured matrix

Method: each row is a full copy of a post-append fixture lane (`corpus/SOURCES.md` with S049/S050 rows +
`corpus/source-snapshots/` from the working tree) with exactly one corruption, run as
`python3 corpus/instruments/capture-binding-check.py --root <fixture>` at `b4182665`.

| # | attack | fixture | observed | caught by |
|---|---|---|---|---|
| K1 | summary constant / count-every-record | single-record tree | `records=1 bound=1 unbound=0` exit 0 | recomputation, not constants |
| K2 | record without `url` | m4 | `FAIL rule=url-mismatch record=S048 detail=absent`, exit 1 | C B3 |
| K3 | url is a proper prefix of its own row URL (`…/msrc/`) | m5 | `url-mismatch`, exit 1 | C B3 (token equality, not substring) |
| K4 | url of a different row | m6 | `url-mismatch`, exit 1 | C B3 |
| K5 | lowercase id `s048` (zfill/loose match) | m11 | `FAIL rule=no-row record=s048`, exit 1 | C B1 (no normalization) |
| K6 | url with trailing space | m18 | `url-mismatch`, exit 1 | C B3 |
| K7 | round-32 record without `fetched_utc` | m2 | `FAIL rule=provenance-missing record=S049/S050`, exit 1 | C C |
| K8 | round-33 dir, archival-only | m3 | `provenance-missing … dir=round-33`, exit 1 | C C (`int(round)>=32`) |
| K9 | non-parsing dir `r33archive`, archival-only | m19 | `provenance-missing … dir=r33archive`, exit 1 | C C (parsed None → modern) |
| K10 | snapshot dir with captures, no manifest | m1 | `FAIL rule=missing-manifest dir=round-31`, exit 1 | A |
| K11 | two registry rows with the same id | m21 | `FAIL rule=dup-id record=S048 rows=2`, exit 1 | C B2 |
| K12 | no registry / absent root | m10, m23 | `UNAVAILABLE reason=read-error`, `reason=no-snapshot-tree`, exit 2 | exit contract |
| K13 | selftest forgeable? | live `--selftest` | 11 case lines `exit=/want=/verdict=`, `selftest cases=11 failures=0`, exit 0, scratch emptied | each case re-execs `SCRIPT --root fixture` |
| K14 | instrument writes into lane | source + run | no write path outside fixture builders; `--selftest` scratch list empty after run | contract |
| H1 | capture bytes unbound in C1's own rules: `S050.txt` truncated to 0 bytes (sha pin unchanged) | m8 | checker `records=40 bound=40 unbound=0` **exit 0**; `source-recheck.py` → `S050:sha256 MISMATCH`, exit 1 | SR, when cited |
| H2 | capture missing: `S049.txt` deleted | m17 | checker **exit 0**; SR → `S049:source UNAVAILABLE reason=missing`, exit 2 | SR, when cited |
| H3 | path traversal: record `path="../round-32/S050.txt"` | m12 | checker **exit 0**; SR → `S048:manifest MISMATCH reason=stem-mismatch`, exit 1 | SR, when cited |
| H4 | nested dir escapes A/B/C: `source-snapshots/nested/round-32/` | m14 | `records=38 bound=38 unbound=0` **exit 0** (2 records vanish) | — (contract's one-level glob) |
| H5 | `fetched_utc` presence-only: both = `"pending"` | m15 | `records=40 bound=40 unbound=0` **exit 0** | — (no format/range check) |
| H6 | duplicate record appended to one manifest | m9 | `records=41 bound=41 unbound=0` **exit 0** | — (dup check is registry-id only) |
| H7 | row with two https tokens; record binds the extra token | m16 | `records=40 bound=40 unbound=0` **exit 0** | — (line 180: membership, not one-token) |
| H8 | record bound to a `rejected` row (S099) | m22 | `records=41 bound=41 unbound=0` **exit 0** | — (status ignored) |

Root-level `source-snapshots/manifest.json` (m20) is silently skipped as a manifest, but its dir then trips
rule A (`missing-manifest dir=round-32`), so it is half-caught, not a silent pass.

## Smallest safe corrections (in priority order)

- **D1 (H1/H2/H3) cite the byte half, or inline it.** Cheapest: the C1 receipt/LOG cites
  `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/<round>/manifest.json` for
  all nine manifests (measured today: 40 `:sha256 OK`, exit 0 each) so "binds its capture" rests on committed
  bytes, not on string agreement. Optional code: rule D in the checker (path basename, exists, non-empty,
  `sha256 == record.sha256`) — a no-op on landed data (all 40 pins already match); if added, the selftest's
  own fixtures must compute real sha (today `record()` writes `"0"*64` over real fixture bytes, unread by the
  checker), otherwise all 11 cases regress. This is defence-in-depth, not a predicate fix.
- **D2 (H4) recursive scan**: `os.walk(corpus/source-snapshots)`; any `manifest.json` below the root is a
  snapshot manifest; a manifest whose relative path does not parse as `round-<N>` is a failure. Note the
  contract's own walk line (`source-snapshots/*/manifest.json`) is one level, so this is a spec change too.
- **D3 (H5) parse `fetched_utc`**: RFC3339 with an offset (`fromisoformat` after `Z`→`+00:00`), not later than
  run time; for `round-32`, exactly the two pinned values. Presence alone lets `"pending"` discharge rule C.
  Not covered by `source-recheck.py`; this one is a genuine provenance gap.
- **D4 (H6) per-manifest uniqueness**: duplicate `id` or duplicate `path` inside one manifest = failure.
  Today the exact-40 kill target catches the count, but the instrument cannot name the duplicate.
- **D5 (H7) row grammar**: the source cell must carry exactly one `https://` token; 0 or 2+ = failure
  (`rule=row-url-ambiguous`). Erratum 1 says "the URL = the https:// token", singular; the checker's docstring
  still reserves the either-token reading.
- **D6 (H8) anchor must be mined**: bound requires the row's status cell (`cells[7]`) to be `mined`. Verified
  safe: all 38 landed bound records name `mined` rows (only S049/S050 have no row yet); a `rejected` proposal
  row is not provenance for a capture.
- **D7 (H4-empty, not tabled separately) per-dir floor**: a snapshot dir holding capture files whose manifest
  lists 0 records currently audits as `records=39 bound=39 unbound=0` exit 0 (fixture m13); each capture file
  should be named by a record or by an explicit `skipped` list (round-26's `S040-live.txt` is the lone orphan).

## Evidence (commands and output, trimmed to verdict lines)

Lane PRE-STATE (registry 48 rows; label: PRE-STATE, do not compare to an after column):

```
$ python3 corpus/instruments/capture-binding-check.py --root <lane>
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
exit=1
```

Fixture simulation of the post-append state (two rows appended with exactly
`https://zc.cnvd.org.cn/news/helpList`, `https://security.360.cn/Reward/rules`):

```
$ python3 corpus/instruments/capture-binding-check.py --root <fixture app>
records=40 bound=40 unbound=0
exit=0
```

Base-bytes control (`git archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 | tar -x -C <scratch>`, read-only git):

```
$ python3 corpus/instruments/capture-binding-check.py --root <base tree>
FAIL rule=missing-manifest dir=round-32
FAIL rule=url-mismatch record=S018 detail=absent dir=round-23
AUDIT records=38 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=0
records=38 bound=0 unbound=38
exit=1
```

Selftest (explicit scratch, leftovers checked):

```
$ python3 corpus/instruments/capture-binding-check.py --selftest --scratch <scratch>
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
exit=0
scratch leftovers: []
```

Byte half (`source-recheck.py`, read-only this round) over every manifest:

```
$ for m in corpus/source-snapshots/*/manifest.json; do python3 corpus/instruments/source-recheck.py --manifest "$m"; echo "exit=$?"; done
round-23 exit 0 shaOK 4   round-24 exit 0 shaOK 19  round-25 exit 0 shaOK 5
round-26 exit 0 shaOK 1   round-28 exit 0 shaOK 2   round-29 exit 0 shaOK 3
round-30 exit 0 shaOK 3   round-31 exit 0 shaOK 1   round-32 exit 0 shaOK 2
total sha OK across manifests 40
```

and its kill of the byte mutants: `x_m8` → `S050:sha256 MISMATCH` exit 1; `x_m12` → `S048:manifest MISMATCH
reason=stem-mismatch` exit 1; `x_m17` → `S049:source UNAVAILABLE reason=missing` exit 2.

Manifest digests measured with the matrix (working-tree bytes, in-flight; labelled non-comparative):
`round-23 1f6d4fb50491 · round-24 77b158caac9a · round-25 251cb5b2c1ba · round-26 1c9131326106 ·
round-28 89f51e052eae · round-29 b24a485ff3d2 · round-30 8aacf77cf2f3 · round-31 5fa37fd7249d ·
round-32 6e4e719a76f1` (sha256 prefixes). Instrument digest at matrix time: `b4182665`.

Mutants were built from the post-append fixture as follows (each row above is one of these, run with `--root`):

```
m4  round-31 record[0].pop("url")
m5  round-31 record[0]["url"] = "https://www.microsoft.com/en-us/msrc/"          # prefix of its own row token
m6  round-31 record[0]["url"] = "https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf"
m8  truncate round-32/S050.txt to 0 bytes, sha pin unchanged
m9  round-31 sources.append(dict(record[0]))                                      # duplicate id
m11 round-31 record[0]["id"] = "s048"
m12 round-31 record[0]["path"] = "../round-32/S050.txt"
m13 round-31 sources.clear()                                                      # captures remain
m14 move source-snapshots/round-32 -> source-snapshots/nested/round-32
m15 round-32 both records fetched_utc="pending"
m16 append " or https://example.invalid/extra" to S048's source cell; record url = that token
m17 rm round-32/S049.txt
m18 round-31 record[0]["url"] += " "
m19 copy round-32 -> r33archive, drop fetched_utc, archival=true
m20 move round-32/manifest.json -> source-snapshots/manifest.json
m21 append S048 row with a different url (same id)
m22 append rejected row S099 + record S099 (archival) with its url
```

## Disclosures / limits that must not be over-read

- `records=40` is 40 manifest entries over **38 distinct ids**: S041 is re-captured in rounds 26, 28 and 30.
  The predicate counts entries, not distinct sources.
- `fetched_utc` is a commit timestamp, not a fetch instant; the round-32 manifest discloses it:
  "each record carries its registry `url` and its `fetched_utc` from the capture commit"
  (`corpus/source-snapshots/round-32/manifest.json` purpose field). C1's "fetch provenance" therefore means
  "recorded at capture commit", and D3's range check cannot create a real fetch instant.
- `multi_row_url=2` at landed bytes is exactly records S029 and S006 (S024/S029 and S006/S028 share URLs);
  the S048 URL's second occurrence is prose at `corpus/SOURCES.md:72`, not a row, and is correctly not counted.
- The instrument binds manifest metadata to registry text. Even with D1 it does **not** prove the bytes came
  from the documented URL (fetch log/UA and human reading remain the ceiling); say so where C1 is scored.

## Impacted axes

- depth:verifiability: C1's counters are discriminative (12 caught, 1 base control, 1 fake control); with
  `source-recheck.py` cited on all nine manifests the byte half is committed evidence. The residual delta is
  H4-H7 (spec-level walk, `fetched_utc` content, duplicate-record counting, two-token row ambiguity) and the
  rejected-row anchor (H8). No measured fact contradicts C1's predicate; the 40/40 line is pending the
  registry append and must be re-measured on quiescent lane bytes.
- coverage: no change claimed or measured by this seat.
