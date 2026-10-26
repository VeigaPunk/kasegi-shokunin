# MutCtrUrlMismatch — C1 counter mutant attack (round-33 wave1)

Seat: MutCtrUrlMismatch (mutation tester, leaf; no subagent dispatch, no background jobs of my own —
the one long poll below is the bound-9 wait pattern). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Assignment: in a **scratch copy** of `corpus/instruments/capture-binding-check.py` apply ONE mutation —
accept a `url` that matches NO registry row (string-contains instead of exact row match) — run the
kill-rule detector (fixture with a non-registry URL; the kill rule requires `unbound>0 / exit 1`) on
pristine, mutated and restored bytes; report survivor or killed. Answering model (session route from
harness context; this item does not depend on it, recorded for the audit trail): `devin/glm-5-3-flash-1m`.
Tools installed/upgraded: none (stdlib python3 only).

## 0. Subject bytes and drift handling (bound 6)

Probe start (instrument present, ExecCaptureBinding receipt present):

```
$ git -C $L rev-parse HEAD && git -C $L status --porcelain -- corpus/instruments/capture-binding-check.py && sha256sum $L/corpus/instruments/capture-binding-check.py
53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
?? corpus/instruments/capture-binding-check.py
4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79  corpus/instruments/capture-binding-check.py
```

Drift: after the first probe was complete, the lane bytes changed `4bc7aed3…` → `b4182665…`
(mtime 01:23:14; the owner's receipt was re-finalised 01:23:51 and cites the new digest). The diff of
old vs new bytes is docstring-only (3 lines: summary-line wording and "ten"→"eleven" fixture trees);
`bind_record` is untouched. Per bound 6 the **whole probe was re-run on the current bytes**; the
citable run below is the `b4182665…` one, and the pre-drift `4bc7aed3…` run produced byte-identical
outputs (both retained in §2–§4 as `pristine`/`mutant` vs `pristine2`/`mutant2`).

## 1. Fixture (self-contained, under `$HYAKU_SCRATCH/kasegi-r33/MutCtrUrlMismatch/`, now removed)

Two fixture lane roots, each = `corpus/SOURCES.md` (byte copy of the lane registry at 48 rows,
sha256 `5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5`) +
`corpus/source-snapshots/round-32/{manifest.json,S001.txt,S002.txt}`:

- `fixture-sub` — **PRIMARY (prefix case)**: record `S002` clean (url byte-exact = its own row's URL
  token); record `S001` near-miss, url `https://www.first.org/cvss/v4.0/user-gu` — a proper prefix of
  S001's own row URL token, so it matches NO registry-row URL byte-for-byte, but it IS a substring of
  S001's source cell. Both records carry `fetched_utc`, so rule C passes and rule B is the only
  possible failure.
- `fixture-super` — bounding case: same clean `S002`; near-miss `S001` url
  `https://www.first.org/cvss/v4.0/user-guide?utm_source=x` (row URL + query suffix; matches no
  registry-row URL byte-for-byte and is NOT a substring of the cell).

Why existing registry ids: `claims-erratum-1` (commit `53bfa59`) makes rule B id-scoped — B1 the row
`| <record id> |` must exist, B2 dup-id, B3 the record `url` must equal the `https://` token of its
OWN row's source cell byte-for-byte. A fabricated id (S901/S902-style) dies at `no-row` and never
reaches the url comparison, so the near-miss record reuses real ids (S001/S002) with a byte-unequal url.

URL row-count evidence in the fixture registry snapshot:

```
$ grep -c 'user-guide?utm_source=x' fixture-super/corpus/SOURCES.md
0
$ grep -c 'v4\.0/user-gu' fixture-sub/corpus/SOURCES.md
1
$ grep -c 'https://www\.first\.org/cvss/v4\.0/user-guide' fixture-sub/corpus/SOURCES.md
1
$ grep -c 'https://www\.first\.org/cvss/v4\.0/specification-document' fixture-sub/corpus/SOURCES.md
1
$ grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|' fixture-sub/corpus/SOURCES.md
48
```

(The S006/S028 duplicate-URL rows exist in the snapshot; the clean record deliberately uses the
unique S002 URL — the HackerOne URL spans two rows and would fail rule B on its own.)

## 2. Baseline — pristine bytes (detector sound)

```
$ python3 pristine2.py --root fixture-sub          # sha256 b4182665… == lane bytes
MANIFEST round-32 records=2 url_bound=1 fetched=2 archival=0
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S001 row=S001 dir=round-32
records=2 bound=1 unbound=1
exit=1
$ python3 pristine2.py --root fixture-super
… identical MANIFEST/AUDIT/FAIL/summary …
exit=1
$ python3 pristine2.py --selftest --scratch selftest2
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

The kill-rule requirement (unbound>0 / exit 1 on a non-registry-URL fixture) is met by the pristine
bytes on both fixtures; baseline is sound, the probe may proceed. (The pre-drift `4bc7aed3…` snapshot
gave byte-identical baseline output on both fixtures and `selftest cases=11 failures=0` exit 0.)

## 3. The mutant (one line)

```
$ cp pristine2.py mutant2.py && sha256sum mutant2.py
5a4cd785e1b3a750763939994ba10e3810e102be132ea33ffd6405de02547576  mutant2.py
$ diff pristine2.py mutant2.py
180c180
<     if url not in row_tokens(own[0]):
---
>     if url not in own[0]:
```

`row_tokens(own[0])` is the list of the own row's `https://` tokens, and `url not in <list>` is
membership, i.e. byte-equality against the row URL (erratum-1 B3). The mutant unwraps the call, so the
record url is accepted when it is a **substring of the whole source cell** — string-contains instead
of exact row match. Exactly one line changed; no other logic touched.

## 4. Mutant runs — verdict

```
$ python3 mutant2.py --root fixture-sub          # PRIMARY (prefix case)
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
records=2 bound=2 unbound=0
exit=0
$ python3 mutant2.py --root fixture-super        # bounding (superstring case)
MANIFEST round-32 records=2 url_bound=1 fetched=2 archival=0
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S001 row=S001 dir=round-32
records=2 bound=1 unbound=1
exit=1
$ python3 mutant2.py --selftest --scratch selftest2
… all 11 cases verdict=pass …
selftest cases=11 failures=0
selftest_exit=0
```

**Verdict: KILLED.** On the primary fixture the mutant prints `records=2 bound=2 unbound=0` exit 0 —
it counts the url `https://www.first.org/cvss/v4.0/user-gu`, which matches NO registry-row URL
byte-for-byte, as **bound** — violating the kill rule's requirement (`unbound>0 / exit 1`). The kill
rule therefore catches the accept-url-not-in-registry counter mutant; per claims.json
`mutants_of_the_counter`, the mutant fails the kill rule. (Pre-drift `mutant` on `4bc7aed3…` bytes:
identical outputs, same verdict.)

Bounding observation: on the superstring fixture the same mutant still prints `unbound=1` exit 1 —
the contains-in-cell loosening does not accept row-URL-plus-suffix urls; the killed defect shape is
specifically the substring direction. A token-level superstring mutant (`row_url in record_url`) is a
different mutation and was not assigned to this seat.

## 5. Restoration evidence

The lane file was never written by this seat (all runs used scratch copies); the mutated bytes never
existed outside `$HYAKU_SCRATCH/kasegi-r33/MutCtrUrlMismatch/mutant*.py`:

```
$ sha256sum $L/corpus/instruments/capture-binding-check.py pristine2.py     # after all mutant runs
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  …/capture-binding-check.py
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  pristine2.py
$ python3 $L/corpus/instruments/capture-binding-check.py --root fixture-sub  # restored bytes re-run
MANIFEST round-32 records=2 url_bound=1 fetched=2 archival=0
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S001 row=S001 dir=round-32
records=2 bound=1 unbound=1
exit=1
$ git -C $L rev-parse HEAD && git -C $L status --porcelain -- corpus/instruments/capture-binding-check.py
53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f
?? corpus/instruments/capture-binding-check.py
```

Lane hash at probe start == hash after all runs (`b4182665…`); the restored bytes reproduce the
pristine baseline on the primary fixture.

## 6. Coverage note (finding, not a contract change)

The instrument's `--selftest` is **blind to this mutant**: with the mutation applied it still prints
`selftest cases=11 failures=0` exit 0. Its `url-mismatch` case exercises a fully unrelated URL
(`https://example.invalid/unknown` against row url `https://example.invalid/alpha`), which no
contains-loosening accepts, so the loophole world — a url that is a substring of its own row's source
cell but byte-unequal to the row URL — is never tested there. The kill rule's fixture probe (this
seat's) supplies that world and kills the mutant. If the L1 wants the selftest to carry this world,
that is a contract/erratum decision, not this seat's: a seventh case ("url is a proper prefix of its
own row's URL token → must fail") would close it.

## 7. Cleanup

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r33/MutCtrUrlMismatch; echo rm_exit=$?
rm_exit=0
$ ls /fast/scratch/hyaku/kasegi-r33/ | grep -c MutCtrUrlMismatch
0
```

Scratch tree removed before this receipt was finalised; no fixture, clone or mutant copy remains on
disk. No lane file other than this receipt was written by this seat.
