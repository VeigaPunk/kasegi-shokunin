# ExecC2Checks — round-76 wave-1 C2 pre-integration mechanical checks

Seat: ExecC2Checks (leaf, read-only over the lane tree). Date: 2026-11-05.
Scope: the committed S111 capture and manifest at the freeze commit 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e (base a788021675873a96e09e91aa033d8c26ac2fe212). Claims A1-A5 / B1-B7 read in full from .ufo/waves/round-76/claims.json; no predicate reworded.

## Run environment
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` -> `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` (rc=0): the lane worktree was exactly at the freeze commit during every check; all checked files were additionally hash-verified against their freeze blobs (r1, r5).
- Git usage strictly read-only: rev-parse, cat-file -t, show. No mutating git/jj anywhere; no writes into the lane tree except this report + the named receipts.
- No network access used; no tools installed (so the 2026-10-19 tooling authorization was not exercised; PACMAN pause untouched).
- Instrument invocations ran with `TMPDIR=/fast/scratch/hyaku/kasegi-r76/ExecC2Checks/tmp` (explicit scratch, created and deleted this session; receipts copied out first).

## Results

| # | Check | Expected | Actual | Verdict |
|---|-------|----------|--------|---------|
| 1 | sha256 + wc -l of S111.txt | 6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab, 48 lines | exact hash match; 48 lines; rc=0; worktree == freeze blob | PASS (r1) |
| 2 | source-recheck.py --manifest round-76/manifest.json --source S111 | sha256 OK, 13 quotes anchor-located, exit 0 | `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`, rc=2; sha256 emit never reached | **DEVIATION — blocks B5 as frozen** (r2, r7) |
| 3 | per-quote word counts (QUALITY R123 <=25) | max <= 25 | `max_words=19 over25=0`, rc=0 | PASS (r3) |
| 4 | capture-binding-check.py | exactly one `FAIL rule=no-row record=S111`, earlier records bound, exit 1 | exactly that FAIL; `records=90 bound=89 unbound=1`, rc=1 | EXPECTED-TRANSITIONAL (r4) |
| 5 | base knowledge-expected.txt sanity | 93 lines / 91 rows, sort clean | 93 wc -l = 91 rows + 2 `#` comment lines; `LC_ALL=C sort -c` rc=0; worktree == base blob d63446ec… | PASS (r5) |
| 6 | 32MiB/HTTP-2 cross-reference | S108 Q27/Q28 anchors 148; S111:38 carries same statements | S108.txt:148 and round-73 manifest Q27/Q28/Q29 anchor=148; S111.txt:38-39 identical statements | PASS (r6) |

## Finding (check 2) — Q01 is below the instrument's evidence floor; B5 cannot reproduce as frozen

Command + rc:
```
$ TMPDIR=/fast/scratch/hyaku/kasegi-r76/ExecC2Checks/tmp python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-76/manifest.json --source S111
S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence
rc=2
```

Facts, all measured:
1. `MIN_QUOTE_CHARS = 12` in corpus/instruments/source-recheck.py ("normalized minimum: a shorter 'quote' matches any capture"); the per-quote gate in check_source() runs before the capture is read/hashed and returns 2 on the first sub-floor quote. Documented at corpus/instruments/README.md:196-198.
2. Q01 `"API (1.0)"` normalizes to 9 characters (measured 9 < 12).
3. The anchors are NOT the problem: an independent per-quote sweep (quote substring-tested against S111.txt line[anchor-1]) reports located=13/13, rc=0.
4. Probe (r7): scratch manifest minus Q01 + byte-identical scratch copy of S111.txt (sha256 6f92e5b7… re-verified on the copy) -> `S111:sha256 OK` + 12 quotes `OK occurrences=1 anchor=N-ok`, rc=0. Q01 is the sole blocker; the remaining manifest is recheck-clean end-to-end.
5. Structural: capture line 21 is exactly `API (1.0)` (9 normalized chars) — no >=12-char substring of that line exists, so lengthening Q01 inside its anchor line cannot pass the gate.

Decision needed before integration (L1/operator; this seat changed nothing): with this manifest, frozen predicate B5 ("reports sha256 OK and all 13 quotes anchor-located, exit 0") fails with rc=2 at the quote gate. Options visible from the evidence: drop Q01 (12 quotes, anchors 22-39) or replace it with a longer quote on another line — both alter the frozen manifest description ("13 quotes, anchors S111.txt lines 21-39") and are therefore for the L1/operator to reconcile, not for a seat to apply.

## Check 4 notes (expected transitional state)
Verbatim output preserved in r4. Substance matches the declared freeze-commit intermediate state: exactly one `FAIL rule=no-row record=S111 dir=round-76`; `bound=89` (every earlier record stays bound); `unbound=1`; rc=1. Totals delta recorded: the spec parenthetical said "(records=89 bound=89)" while the actual totals line is `records=90 bound=89 unbound=1` — records=90 because the round-76 manifest itself contributes the S111 record (AUDIT `records=90` = 89 prior + 1 new). B4 re-measures at integration (expect `records=90 bound=90 unbound=0`, exit 0). Inherited AUDIT observations, out of scope: orphans=1 orphan=S040-live.txt; multi_row_url=7; digest_unpinned=0; missing_manifest=0.

## Deliverables
- .ufo/waves/round-76/w1/ExecC2Checks.md (this report)
- Receipts: ExecC2Checks-r1-capture-hash.txt, ExecC2Checks-r2-recheck-s111.txt, ExecC2Checks-r3-quote-word-counts.txt, ExecC2Checks-r4-binding-check.txt, ExecC2Checks-r5-expected-list.txt, ExecC2Checks-r6-crossref-32mib-http2.txt, ExecC2Checks-r7-q01-probe.txt

## Bounds compliance
Read-only git only (rev-parse / cat-file -t / show); no stash/checkout/reset/pull/commit; no writes into the lane working tree outside this wave-dir report + named receipts; scratch /fast/scratch/hyaku/kasegi-r76/ExecC2Checks deleted before yielding; no network; no installs; claims.json read in full, predicates untouched.

## Status addendum (2026-11-05, after delivery)

All measurements above are the **pre-repair state** at freeze 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e (this seat's checks ran with HEAD == the freeze; nothing in the lane tree was modified by this seat). Per the L1 (KasegiR76, message received after delivery): Q01 was replaced at integration with "How does the API work?" (S111.txt:27, 22 normalized chars) and source-recheck.py now prints `S111:sha256 OK` with 13/13 quotes anchor-ok, exit 0. That post-repair state is reported by the L1 and was NOT re-verified by this seat (leaf mandate; the working tree moved past the freeze after these checks). The receipts r1-r7 therefore evidence the freeze-commit bytes and the r2 finding should be read as the pre-repair snapshot.
