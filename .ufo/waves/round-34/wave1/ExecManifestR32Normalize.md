# ExecManifestR32Normalize — R8: strict-UTC `fetched_utc` for the round-32 manifest

Seat: executor, leaf of the round-34 L2 wave. Write scope used:
`corpus/source-snapshots/round-32/manifest.json` (this receipt under
`.ufo/waves/round-34/wave1/`). No other lane file, no fleet file, no shokuknow
file, no git/jj mutation, no subagent.

## Report

### 1. Target and pre-state

Defect of record: `corpus/lessons/round-33-verifier-spotcheck.md:184-185` —
"**R8** Round-32 manifest `fetched_utc` holds `2026-10-25T23:14:00-03:00` — a
local-offset capture-commit time in a `_utc` field, not a fetch instant …
Normalize or rename the field." Frozen C1 clause: "round-32 manifest carries only
strict-UTC fetched_utc" (`.ufo/waves/round-34/claims.json`).

Pre-state, measured before any edit:

```
$ sha256sum corpus/source-snapshots/round-32/manifest.json
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
$ wc -lc corpus/source-snapshots/round-32/manifest.json
  94 5753 corpus/source-snapshots/round-32/manifest.json
$ python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-32/manifest.json'));print([(s['id'],s['fetched_utc']) for s in d['sources']])"
[('S049', '2026-10-25T23:14:00-03:00'), ('S050', '2026-10-25T23:14:00-03:00')]
```

Pre-state crawl-before bytes kept only until this receipt was written
(`/fast/scratch/hyaku/kasegi-r34/ExecManifestR32Normalize/manifest.before.json`,
digest above; the same bytes are recoverable from the lane's jj/git history at
HEAD `206e5108`).

Ground truth for the replacement instants (read, not retyped from the prompt) —
`.ufo/waves/round-33/wave1/ScoutLiveDrift.md`:

```
8:S049 status=200 fetched_bytes=56674 snapshot_bytes=20272 sha256=962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8 utc=2026-10-26T04:16:06Z
10:S050 status=200 fetched_bytes=427391 snapshot_bytes=31016 sha256=2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888 utc=2026-10-26T04:16:16Z
26:Fresh network read at 2026-10-26T04:16Z (S049) / 04:16:16Z (S050), ~2h02m after the capture commit 288ea9ac (author time 2026-10-25T23:14:00-03:00 = 02:14Z).
```

The differing-line count (`0`) is asserted in the same receipt's table and is what
the new `purpose` sentence states; this seat did not re-fetch the network.

### 2. Change — exactly three cells, nothing else

`corpus/source-snapshots/round-32/manifest.json`:

| location | before | after |
|---|---|---|
| `sources[0].fetched_utc` (`S049`, `path: S049.txt`, `url: https://zc.cnvd.org.cn/news/helpList`) | `2026-10-25T23:14:00-03:00` | `2026-10-26T04:16:06Z` |
| `sources[1].fetched_utc` (`S050`, `path: S050.txt`, `url: https://security.360.cn/Reward/rules`) | `2026-10-25T23:14:00-03:00` | `2026-10-26T04:16:16Z` |
| top-level `purpose` (one clause replaced, rest byte-identical) | "each record carries its registry `url` and its `fetched_utc` from the capture commit (C1 rule B/C)." | "each record carries its registry `url` and a strict-UTC (Z-suffix) `fetched_utc` that is a 2026-10-26 verification re-open instant of byte-equal content, not the original fetch: S049 2026-10-26T04:16:06Z and S050 2026-10-26T04:16:16Z, each HTTP 200 with 0 differing lines (round-33 lesson; `wave1/ScoutLiveDrift.md`). The capture commit's author time above (02:14Z) is a local-offset commit instant, not a measured HTTP fetch, and is recorded here as history rather than in a `_utc` field (R8)." |

No `id`, `path`, `sha256`, `url`, `quotes[].id`, `quotes[].quote`,
`quotes[].location` or `schema_version` cell was touched. Proof is a structural
walk of the two parsed trees, not a visual read:

```
$ python3 - <<'PY'   # walk(old, new) over json.load of before/after
...
CHANGED /purpose
CHANGED /sources[0]/fetched_utc
CHANGED /sources[1]/fetched_utc
total_changes= 3
quotes_unchanged= True
sha256_fields_unchanged= True
paths_urls_unchanged= True
```

Line-level diff (`git diff --numstat`): `3 3 corpus/source-snapshots/round-32/manifest.json`
— one `purpose:` line and the two `fetched_utc` lines, each replaced in place; no
line added or removed.

Post-state:

```
$ sha256sum corpus/source-snapshots/round-32/manifest.json
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
$ wc -lc corpus/source-snapshots/round-32/manifest.json
  94 6138 corpus/source-snapshots/round-32/manifest.json
$ python3 -c "...len(d['sources']), sum(len(s['quotes'])...)"
records= 2 quotes= 14
```

Captures untouched (the manifest's own sha256 pins, re-hashed):

```
$ sha256sum corpus/source-snapshots/round-32/S049.txt corpus/source-snapshots/round-32/S050.txt
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  corpus/source-snapshots/round-32/S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  corpus/source-snapshots/round-32/S050.txt
```

### 3. R8's own closure shape (strict UTC, no offset)

```
$ grep -oE '"fetched_utc": "[^"]+"' corpus/source-snapshots/round-32/manifest.json
"fetched_utc": "2026-10-26T04:16:06Z"
"fetched_utc": "2026-10-26T04:16:16Z"
$ grep -cE '"fetched_utc": "[^"]*[+-][0-9]{2}:[0-9]{2}"' corpus/source-snapshots/round-32/manifest.json
0        # grep exit 1 (no match) — the wanted result
$ python3 -c "...re.fullmatch(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$', v)..."
values= ['2026-10-26T04:16:06Z', '2026-10-26T04:16:16Z']
all_strict_utc= True
any_offset= False
records= 2
```

The exact R8 predicate frozen for `r-defect-closure.sh`
("`^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` and contain no '-' offset") holds for both
records.

### 4. Required verification runs (final bytes)

**4a. `source-recheck.py` per source** — every assertion, exit 0:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
recheck_S049_exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
recheck_S050_exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json   # both records
recheck_all_exit=0     # 14 assertion lines, 2 sha256 OK, 12 Q OK occurrences=1 (tail shown in §4a above)
```

Instrument of record for these runs:
`source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`.
The instrument never reads `fetched_utc`, so its verdict is unchanged by this edit
— which is why the clause needed its own check.

**4b. `capture-binding-check.py` live audit — record counts unchanged, exit
attributed to a sibling's in-flight dir (§5):**

```
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=10 manifest_dirs=9 missing_manifest=1 multi_row_url=2
FAIL rule=missing-manifest dir=round-34
records=40 bound=40 unbound=0
binding_exit=1
```

**4c. Same instrument, control root excluding the in-flight `round-34` directory
(`$S/ctrl` = copy of `corpus/SOURCES.md` + symlinks to `round-23…round-32`) —
the verdict this seat's change is responsible for:**

```
$ python3 corpus/instruments/capture-binding-check.py --root /fast/scratch/hyaku/kasegi-r34/ExecManifestR32Normalize/ctrl
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
ctrl_exit=0
```

**4d. `--selftest` on the same instrument bytes** (sha256
`b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, the round-33
landed bytes — the R9/H4–H8 hardening seat had not landed at run time):

```
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=url-matching-two-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
selftest_exit=0
```

### 5. Why the live `binding_exit=1` is not this seat's change

`corpus/source-snapshots/round-34/` is untracked and in flight at run time:

```
$ ls -la corpus/source-snapshots/round-34/
-rw-r--r-- 1 vgpnk vgpnk 8502 Oct 26 02:31 S051.txt
$ git status --porcelain corpus/source-snapshots/
?? corpus/source-snapshots/round-34/
```

`S051.txt` exists with no `manifest.json` yet, so rule A reports
`FAIL rule=missing-manifest dir=round-34` and the exit is 1. The three counters
this seat is judged on are unmoved: `records=40`, `bound=40`, `unbound=0`,
`with_fetched_utc=2`, `multi_row_url=2`. The control run in §4c removes only that
in-flight directory and exits 0. Attributed to the S051 landing seat (C2), not to
R8; the L1's post-integration run must re-measure after `round-34/manifest.json`
lands.

### 6. Cross-file references this edit makes stale (NOT edited — outside the assigned path)

Recorded for the L1, each with the line as it reads now:

1. `corpus/instruments/README.md:585` — the manifest-schema table still publishes
   the old value and the old semantics:
   `| \`fetched_utc\` | \`2026-10-25T23:14:00-03:00\`, the capture commit \`288ea9ac…\` author instant | 2 (round-32 S049/S050) |`
2. `corpus/instruments/README.md:627-629` — known-limit bullet: "**`fetched_utc` is
   the capture commit instant for the round-32 records, not a measured HTTP
   instant** … No independent fetch log exists for that round; drift is bounded
   only from the 2026-10-26T04:16Z live re-fetch onward".
3. `corpus/instruments/README.md:604` — the digest table row
   `| \`round-32\` | \`6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774\` |`;
   measured table state (this seat's check over all nine rows): eight `MATCH`,
   `round-32 STALE readme=6e4e719a76f1 actual=72ab4e6834b9`. New value:
   `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6`.
4. `SCORECARD.md:1045-1046` — "`fetched_utc` is the capture-commit timestamp
   (round-32 manifest `purpose`), not a fetch instant, and the instrument binds
   manifest metadata to registry text". The first clause is now false; the
   instrument-bound claim in the second clause is unchanged. (This file is
   another seat's write target this round — `M SCORECARD.md` at run time; left to
   that seat / the L1.)

   Note the same SCORECARD file's round-33 row `SCORECARD.md:1084` and the C1 row
   `:1001` cite `with_fetched_utc=2`, which still holds.
5. `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:290-291` —
   the entry binds the manifest by digest:
   "`corpus/source-snapshots/round-32/manifest.json` (sha256
   `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774`)". Stale after
   this edit; needs an appended correction carrying
   `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6`
   (QUALITY: corrections sweep every mention). Same file `:293` calls
   `2026-10-25T23:14:00-03:00` "the capture instant" — still true of the *capture
   commit*, but it is no longer the manifest's `fetched_utc`; re-word when the
   digest is corrected.

No other committed non-wave file carries the old digest (checked:
`grep -rn 6e4e719a… --include=*.md --include=*.json . | grep -v '^./.ufo/'` →
exactly the two rows above).

### 7. Notes and risks for integrating seats

- **R8's closure check must read `fetched_utc` values, not the whole file.** The
  `purpose` keeps one pre-existing `-03:00` literal — the capture-commit author
  time `(author time 2026-10-25T23:14:00-03:00)` in its first sentence, which this
  seat was told not to edit. `grep -o -- "-03:00" … | wc -l` → **1**. A whole-file
  "no offset anywhere" grep would therefore mark R8 open although the field is
  clean; the frozen wording ("`fetched_utc` values all match strict UTC … and
  contain no '-' offset") is the scoped reading that passes.
- **Strict-UTC acceptance of the hardened instrument.** The new values are
  `Z`-suffix, second-precision ISO-8601 (`2026-10-26T04:16:06Z`,
  `2026-10-26T04:16:16Z`) — the shape the C1 clause and the H4–H8 hardening
  (`+00:00` or `Z` only, offset rejected) require. The hardened checker was not on
  disk at run time (digest `b4182665…`, 11 cases, no strict-UTC limb), so that
  acceptance is asserted by shape here and must be re-run by the L1 after both
  landings.
- **The purpose note now carries a re-open claim** sourced to
  `ScoutLiveDrift.md` (HTTP 200, 0 differing lines, byte-equal post-conversion
  text). It does not claim the raw HTML/PDF bodies were compared — that limit is
  the drift seat's own wording and is untouched.
- No tool was installed or upgraded; the run used system `python3` and coreutils
  only, so there is no tooling entry to record.

### 8. Scratch

All work lived in `/fast/scratch/hyaku/kasegi-r34/ExecManifestR32Normalize/`
(pre-state copy, control root, captured outputs) and was removed before this
receipt was committed; `/tmp/r32-manifest-before.json` (pre-state bytes, 5753 B)
was also removed. Evidence needed beyond the quoted output above was copied into
this receipt. No scratch tree remains on disk.

### 9. Verdict for the L1

R8 is closed by this seat's edit on the assigned file: both `fetched_utc` values
are strict-UTC verification re-open instants, the purpose note says so and records
the capture commit's local-offset time as history, no other cell changed
(structural diff = 3 cells), and the two frozen assertions (`source-recheck` per
source, all `occurrences=1` + `sha256 OK`, exit 0) hold. Outstanding for the L1,
not for this seat: the five stale cross-file mentions in §6 and the in-flight
`round-34` directory that drives the live audit's exit 1 (§5).
