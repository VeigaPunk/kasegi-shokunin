# RevOrphan — R6 orphan resolution review (round 34, wave 1)

Item: review the R6 orphan resolution — round-26 manifest record (or explicit orphan list) for
`S040-live.txt`; record sha256 matches file bytes; manifest purpose text truthful;
`capture-binding-check` exit 0 with `missing_manifest=0`.

## Verdict

**PASS.** R6 (`corpus/lessons/round-33-verifier-spotcheck.md:178-180`) is resolved by the
second of its two named remedies — "or record the orphan" — plus the per-file binding it asked
to land: `capture-binding-check.py` now implements top-level `orphans` declarations
(rule A2, `capture-binding-check.py:20-26`), with selftest cases `per-file-orphan-detected`
(exit 1) and `per-file-orphan-listed` (exit 0) both passing. The round-26 manifest declares the
orphan, every factual claim in its amended `purpose` text checked out against committed bytes
and receipts, and the plain binding run is green on the settled tree.

## Report

### 1. Manifest has an explicit orphan record for S040-live.txt

`corpus/source-snapshots/round-26/manifest.json` (digest `33ac33c3…eacefa`, full below) carries a
top-level `orphans` list with one entry: `path=S040-live.txt`, `reason` (non-empty; see §3),
`sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`, `row=S040`,
`row_url=https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`,
`captured_url=https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`,
`fetched_utc=2026-10-25T12:34:27Z` (strict-UTC form).

Before-state: `git show 014ee2d7aa8c3c095ff57ae51097606a9906228c:corpus/source-snapshots/round-26/manifest.json`
→ JSON has no `orphans` key (`False` from `'orphans' in m`), and the old purpose opened
"S040-live.txt was not present in corpus/source-snapshots/round-26/ at manifest build time" —
the text R6 declared false once the file was committed into the directory without a record.

### 2. Record sha256 matches the file bytes

```
$ sha256sum corpus/source-snapshots/round-26/S040-live.txt
b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c  …  exit=0
$ wc -lc corpus/source-snapshots/round-26/S040-live.txt
 503  33463 …                                                        exit=0
```

Matches the orphan entry's `sha256` exactly; size 33463 B and 503 lines match the purpose text.
The same sha256 appears verbatim in the producing receipt log line
`.ufo/waves/round-26/wave1/ScoutS040Probe.md:57`:
`S040 status=200 fetched_bytes=94027 snapshot_bytes=33463 sha256=b7f7b5…286c utc=2026-10-25T12:34:27Z out=…/round-26/S040-live.txt`.
Sibling S041 record also re-verified: `sha256sum` → `e18acbf9…5ab47`, `wc -l` → 2354 — both as
stated in the purpose.

### 3. Manifest purpose text is truthful (claim by claim)

1. "accounts for exactly the two files committed in this directory" — `ls` shows exactly
   `S041.txt`, `S040-live.txt`, `manifest.json`. TRUE.
2. "no registry row id `S040-live` exists" — `grep -c 'S040-live' corpus/SOURCES.md` → `0`
   (exit 1). TRUE. S040 row itself is SOURCES.md:46 with the same `row_url` as the orphan entry.
3. "source-recheck.py Q9 B1 requires a record `path` stem to equal its registry id" —
   `corpus/instruments/source-recheck.py:11-12` ("B1: every record's `path` stem must equal its
   `id`") and `:123-125` (emits `reason=stem-mismatch`). TRUE — so `S040-live.txt` cannot be a
   `sources` record, and the orphan listing is the correct R6 remedy.
4. "fetched 2026-10-25T12:34:27Z by ScoutS040Probe through capture-source.py" — receipt
   `ScoutS040Probe.md:57` (verbatim log line quoted in §2), command at the same receipt shows
   `--id S040 --url https://sec.cloudapps.cisco.com/… --out …/round-26/S040-live.txt`. TRUE.
5. "2 redirects, instrument UA required" — receipt: "instrument UA → 301 → 302 → 200",
   `final=… code=200 num_redirects=2`. TRUE. `captured_url` = that final URL; `row_url` = the
   canonical registry URL. TRUE.
6. "The `orphans` entry's … fields are informational only: that checker validates `path` and
   `reason` and asserts neither field" — `capture-binding-check.py:308-326` (`orphan_paths`)
   validates only that each entry is a dict with non-empty string `path` and `reason`; the audit
   compares declared vs actual capture files and prints `orphan=<file>`, asserting no sha/URL/
   timestamp fields. TRUE (and the disclosed sha256/fetched_utc are themselves accurate, §2).

### 4. capture-binding-check exit 0 with missing_manifest=0

```
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 … / round-26 records=1 url_bound=1 fetched=0 archival=1 / …
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
exit=0
```

`missing_manifest=0`, `orphans=1 orphan=S040-live.txt` listed on the AUDIT line with no FAIL and
no exit-status impact (rule A2 as documented). Selftest: `selftest cases=23 failures=0`, exit 0,
including `per-file-orphan-detected` (want 1, got 1) and `per-file-orphan-listed` (want 0, got 0).
Closure suite: `bash corpus/instruments/r-defect-closure.sh` → `R6 check=round-26 manifest binds
S040-live.txt (record or orphan list) + purpose corrected open=0` and `closed=9/9 exit=0`.

### 5. Observation (not an R6 defect) — mid-flight transients during review

Two gates were red on my first run and green on re-run minutes later, because sibling seats were
still landing C1/C2 artifacts in the shared working copy:

- First plain binding run: `FAIL rule=no-row record=S051 dir=round-34`, `records=41 bound=40
  unbound=1`, exit=1 — `corpus/SOURCES.md` then had 50 rows and no S051; the `+| S051 |` row
  (and "Registry 50 rows pre-append → 51 post-append") appeared in `git diff corpus/SOURCES.md`
  minutes later; re-run then gave `records=41 bound=41 unbound=0` exit=0.
- First closure-suite run: `R4 … open=1`, `closed=8/9 exit=1`; re-run `closed=9/9 exit=0`.

Consequence for the L1: the C1 counting-command baseline (`records=40 bound=40 unbound=0
exit=0`) is now `records=41` on any tree that includes the round-34 manifest — the frozen
baseline number is stale once S051 lands; the exit-0/unbound=0 property holds. All reviewed
artifacts are uncommitted working-copy state on top of `206e510` (base `014ee2d` held the
pre-amendment manifest), consistent with L1-owned commits.

### 6. File digests (sha256)

```
33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa  corpus/source-snapshots/round-26/manifest.json
b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c  corpus/source-snapshots/round-26/S040-live.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-26/S041.txt
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
c79c903f4bcfc9f46efaa4f1a1a03a0e661b73c715794b2bc31b5bc9886071ba  .ufo/waves/round-26/wave1/ScoutS040Probe.md
```

### 7. Scratch / tooling

No scratch directory created (all commands ran read-only in the lane; the only write is this
receipt) — nothing to clean, no tree left on disk. No tools installed; no `pacman` use; no git
add/commit/push, no jj mutations. Write scope respected: lane repo only.
