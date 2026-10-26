# ExecS040Orphan — round-34 (R6: round-26 `S040-live.txt` orphan)

Seat: leaf executor, L2 wave 1 of kasegi-shokunin round 34. Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `014ee2d7`, claims-freeze
`29f606db`. I wrote exactly one file in the lane:
`corpus/source-snapshots/round-26/manifest.json`. No git/jj mutation, no commit, no
other lane or campaign touched, no tool installs (nothing was needed; `python3 3.14.0`,
`sha256sum`, `sha256sum`-equivalent stdlib were already present).

## Report

### Decision: option (b), explicit orphan declaration — and why (a) was not landable

Option (a) was "add a `sources` record for `S040-live.txt`". Measured, it cannot pass both
checkers at once:

- `corpus/instruments/source-recheck.py:123-126` fails any record whose path stem differs
  from its id:
  `if Path(path).stem != source_id: emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch"); return 1`.
  Path `S040-live.txt` has stem `S040-live`, so id `S040` → `MISMATCH reason=stem-mismatch`.
- Naming the record `S040-live` instead fails `capture-binding-check.py` rule B, because
  `corpus/SOURCES.md` has no `| S040-live |` row (`rule=no-row record=S040-live`), and the
  file's bytes are a live capture of the S040 *redirect target*
  (`https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`),
  while row S040's source cell carries only the canonical
  `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`
  (`corpus/SOURCES.md:46`, the only `https://` token in that cell).
- Renaming the committed capture to `S040.txt` would have satisfied both, but it silently
  rewrites the name every round-26 receipt and prose citation uses
  (`ScoutS040Probe.md:57`, `s040-probe.txt:47`, `ScribeScorecard.md:63`), and it makes the
  live probe byte-identical in name to the round-25 `S040.txt` capture — a worse trade than
  an explicit declaration.

So `S040-live.txt` is declared, not bound, and the instrument now audits the declaration
per file (round-33 `CritC1Kill.md` D7: "each capture file should be named by a record or by
an explicit `skipped` list (round-26's `S040-live.txt` is the lone orphan)").

Coordination, because the checker is not mine: `ExecCaptureBindingHarden` owns
`corpus/instruments/capture-binding-check.py` this round and told me the exact schema
(top-level `orphans`, object elements, non-empty `path` = exact basename + non-empty
`reason`; extra keys pass through; a bare string or missing/empty `path`/`reason` is
`UNAVAILABLE reason=manifest-shape`, exit 2). I did not edit the instrument. The landed
key is therefore `orphans` (plural) rather than the handoff's singular word "orphan"; the
instrument that reads it prints `orphan=S040-live.txt`.

### What landed in the manifest

`corpus/source-snapshots/round-26/manifest.json`, top-level keys now
`schema_version`, `purpose`, `orphans`, `sources`.

- `purpose` rewritten (the old text was false: it said `S040-live.txt` "was not present …
  so S040 is skipped this round"). It now names the two files the manifest actually covers,
  gives each one's size/lines/sha256, states that S041's record is `archival: true` because
  round-26 predates the round-32 strict-UTC rule and that its capture instant lives in
  `.ufo/waves/round-26/wave1/ExecCaptureS041.md:17` (`utc=2026-10-25T12:34:17Z`), and states
  that `S040-live.txt` cannot be a record because of `source-recheck.py` Q9 B1. It also says
  the declaration's `sha256`/`row`/`row_url`/`captured_url`/`fetched_utc` fields are
  informational to `capture-binding-check.py`, which validates only `path` and `reason`.
- `orphans`: one object —
  `path` `S040-live.txt`, non-empty `reason` (probe capture fetched after the manifest was
  built; no registry id `S040-live`), `sha256`
  `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`,
  `row` `S040`, `row_url` the canonical registry URL, `captured_url` the redirect target,
  `fetched_utc` `2026-10-25T12:34:27Z` (strict-UTC; from
  `.ufo/waves/round-26/wave1/ScoutS040Probe.md:57`).
- `sources` byte-identical to before: one S041 record, seven quotes, unchanged.

File digests (before → after, `sha256sum`):

```text
OLD corpus/source-snapshots/round-26/manifest.json
    1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247
NEW corpus/source-snapshots/round-26/manifest.json
    33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa
    corpus/source-snapshots/round-26/S040-live.txt
    b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c   (unchanged; equals the declared sha256)
    corpus/instruments/capture-binding-check.py
    3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa   (peer's rule-A landing; I did not edit it)
    corpus/SOURCES.md
    4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6   (S051 row appended by the C2 seat, not me)
```

Declared sha256 re-derived from the bytes rather than trusted from prose:

```text
$ python3 - <<'PY'
import json,hashlib
m=json.load(open('corpus/source-snapshots/round-26/manifest.json'))
o=m['orphans'][0]; b=open('corpus/source-snapshots/round-26/'+o['path'],'rb').read()
print('orphan_sha_matches=%s bytes=%d declared_ok=%s' % (hashlib.sha256(b).hexdigest()==o['sha256'], len(b), o['fetched_utc'].endswith('Z')))
PY
orphan_sha_matches=True bytes=33463 declared_ok=True
```
(`wc -l` on the file = 503 lines, matching the purpose text and `ScoutS040Probe.md:61`.)

### Verification on the landed tree (final run, after the S051 registry row landed)

```text
$ python3 -m json.tool corpus/source-snapshots/round-26/manifest.json > /dev/null
json_exit=0

$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
…
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
…
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
binding_exit=0
```

This is the assignment's gate: exit 0, `missing_manifest=0`, `unbound=0`, and the file is
shown bound-or-listed — the AUDIT line carries `orphans=1 orphan=S040-live.txt`, with no
`FAIL` line at all and the round-26 `MANIFEST` counters unchanged
(`records=1 url_bound=1 fetched=0 archival=1`), i.e. the declaration does not inflate
`records=`/`bound=`.

Source-recheck unaffected (the point of choosing the declaration over a record):

```text
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json
S041:sha256 OK
S041:Q1a OK occurrences=1
S041:Q1b OK occurrences=1
S041:Q2a OK occurrences=2 anchor=1874-ok
S041:Q2b OK occurrences=1
S041:Q3 OK occurrences=1
S041:Q4 OK occurrences=1
S041:Q5 OK occurrences=1
recheck_exit=0
```

`--manifest corpus/source-snapshots/round-25/manifest.json` also exits 0 (its own S040
record, quotes untouched by me).

### Controls (fixtures in scratch, not the lane)

Scratch tree `/fast/scratch/hyaku/kasegi-r34/ExecS040Orphan/lane`: a copy of the lane's
`corpus/SOURCES.md` + all ten `source-snapshots` dirs minus `round-34`, plus the peer's
instrument, so the round-34/S051 in-flight state could not mask a round-26 verdict.

New manifest (declaration present) → the declaration is accepted and changes nothing else:

```text
new_manifest_exit=0
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=40 bound=40 unbound=0
```

Old manifest (`1c913132…`, restored byte-for-byte from the pre-edit copy) → the same bytes
now fail, so the audit is not decorative:

```text
old_manifest_exit=1
AUDIT records=40 … missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=orphan-capture file=S040-live.txt dir=round-26
records=40 bound=40 unbound=0
```

The `orphans=1 orphan=S040-live.txt` token appears in both runs because the peer's token is
derived from the file walk; only the declared manifest suppresses the `FAIL` and the exit
status. So: declaration present → exit 0; declaration absent → `FAIL rule=orphan-capture`,
exit 1. Nothing else in the tree moves in either run.

Independent per-file coverage walk over every snapshot dir (my own walker, not the
instrument), on the final tree: no unlisted file anywhere, and round-26 is the only dir
with a declared orphan:

```text
round-23  files= 4 records= 4 covered= 4 orphan=0 unlisted=-
round-24  files=19 records=19 covered=19 orphan=0 unlisted=-
round-25  files= 5 records= 5 covered= 5 orphan=0 unlisted=-
round-26  files= 2 records= 1 covered= 1 orphan=1 unlisted=-
round-28  files= 2 records= 2 covered= 2 orphan=0 unlisted=-
round-29  files= 3 records= 3 covered= 3 orphan=0 unlisted=-
round-30  files= 3 records= 3 covered= 3 orphan=0 unlisted=-
round-31  files= 1 records= 1 covered= 1 orphan=0 unlisted=-
round-32  files= 2 records= 2 covered= 2 orphan=0 unlisted=-
round-34  files= 1 records= 1 covered= 1 orphan=0 unlisted=-
TOTAL files=42 covered=41 orphan=1 unlisted=0
```

### Timing note (measured, then cleared)

Between my manifest edit and the C2 land, the live-tree gate ran `binding_exit=1` on a
single unrelated failure, `FAIL rule=no-row record=S051 dir=round-34` (the `round-34/`
manifest landed at 02:35 with `S051.txt` before `SOURCES.md` carried the row). After the
S051 row landed (`corpus/SOURCES.md` now has one `^| S051` row; digest above), the same
command is `binding_exit=0` as quoted. No round-26 state depends on that ordering.

### Left deliberately alone (not mine, named so the L1 can route it)

- `corpus/instruments/capture-binding-check.py` and its docs — owned by
  `ExecCaptureBindingHarden`; I only consumed the schema it published.
- `corpus/instruments/README.md:552-563` still records the b4182665… live-run block whose
  `AUDIT` line lacks `orphans=`/`orphan=`; the peer said it is appending a round-34 section
  marking that block stale rather than rewriting it. My change keeps the round-26
  `MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1` line inside that block true.
- `QUALITY.md` R20 / errata / lessons / SCORECARD — the C1 items other seats own; R6's own
  record of the closed defect belongs to the L1's lesson/SCORECARD step, and this receipt is
  the evidence it can cite.
- Round-25's `S040` record and quotes: untouched (its own dir, its own binding).

## Risks and limits of this landing

1. The declaration is prose-adjacent by design: `capture-binding-check.py` asserts only
   `path` and `reason`. The orphan's sha256/url/UTC are checked by *me* here (recomputed
   above) and by any reader, not by a counter. A future round that wants them enforced needs
   a rule that validates orphan-element `sha256` against the bytes — peer's rule D territory,
   not added unilaterally.
2. The orphan's `captured_url` is the redirect target, not row S040's source-cell URL. That
   is a fact about the capture, not a registry mismatch: the instrument binds the file by
   declaration, not by URL, precisely because `S040-live` is no row id. A reader who expects
   every capture URL to equal a row URL will see a difference here; the `row_url` field and
   the purpose text make the relationship explicit.
3. `orphans` (plural) is the landed key; the handoff wrote "an `orphan` list". Any verifier
   grepping for an exact singular key would miss it — the checker's schema and the AUDIT
   token (`orphan=S040-live.txt`) are the binding facts.
4. I did not run the peer's `--selftest` as a gate on my file (their C1 item); my evidence is
   the live run plus the two scratch controls, which exercised their landed rule A directly.

## Scratch

All work trees lived under `/fast/scratch/hyaku/kasegi-r34/ExecS040Orphan/`
(`lane/`, `manifest-old.json`, `manifest-new.json`, `*.txt` run logs), all removed before
yield — the directory no longer exists. Receipt written before removal.
