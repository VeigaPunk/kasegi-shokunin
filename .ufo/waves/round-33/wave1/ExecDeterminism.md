# ExecDeterminism — round-33 wave-1 determinism probe receipt

Seat: `ExecDeterminism` (leaf executor, hyaku run-8 inline spawn). Lane: `kasegi-shokunin`.
Lane write scope: this lane only. Fleet root and `shokuknow` untouched.
Measurement window: **2026-10-26T04:36:15Z – 04:38:00Z** (UTC stamps printed per run).
Lane HEAD at measurement: `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f` (working tree carried the
wave's uncommitted edits; every number below is bound to file digests, not to HEAD).
Runtime: `Python 3.14.8 (main, Oct 2 2026, 10:23:31) [GCC 16.2.1 20260810]`, Linux x64.
Model: this item does not depend on an answering model; no model was passed.

## 1. Method

Each command was executed twice, consecutively, on quiescent bytes, capturing the
command's **own** exit status plus sha256 of stdout and stderr:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
bash -c "$CMD" >out 2>err; rc=$?
printf 'exit=%s stdout_sha256=%s stdout_bytes=%s stderr_sha256=%s\n' \
  "$rc" "$(sha256sum <out|cut -d' ' -f1)" "$(stat -c %s out)" "$(sha256sum <err|cut -d' ' -f1)"
```

Quiescence gate: the 19 files the four probes read (four instruments, `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/instruments/knowledge-expected.txt`, the F16 knowledge entry,
all nine `corpus/source-snapshots/*/manifest.json`, `round-32/S049.txt`, `round-32/S050.txt`)
were hashed before the window, after the window, at 04:37:54Z, and once more at 04:39:49Z immediately before hand-off. The aggregate digest of
that digest list held at `6a5b48cf…` over the polls 04:36:15Z / 04:36:35Z / 04:36:55Z and the
before/after lists diff empty; all four probes therefore ran on one unchanged byte set.

Measured inputs (digest of record, identical at 04:37:03Z, 04:37:54Z and 04:39:49Z):

| Input | sha256 |
|---|---|
| `corpus/instruments/capture-binding-check.py` | `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` |
| `corpus/instruments/recheck-audit.py` | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/SOURCES.md` | `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b` |
| `corpus/README.md` | `3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932` |
| `corpus/instruments/knowledge-expected.txt` | `3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb` |
| `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` | `1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1` |
| `corpus/source-snapshots/round-32/manifest.json` | `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774` |
| `corpus/source-snapshots/round-23/manifest.json` | `1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70` |
| `corpus/source-snapshots/round-24/manifest.json` | `77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` |
| `corpus/source-snapshots/round-25/manifest.json` | `251cb5b2c1bacb5ba47758fb60e41aaf1e367ae11df05ed19886361b35f7aea2` |
| `corpus/source-snapshots/round-26/manifest.json` | `1c9131326106eca5860f5c650b2c9c4efa860da52a701b039b457aba619e3247` |
| `corpus/source-snapshots/round-28/manifest.json` | `89f51e052eaefcb56a880d48e6778ee88b46e55cafde1275c69992304e7ef75e` |
| `corpus/source-snapshots/round-29/manifest.json` | `b24a485ff3d2d03abe3ef2022e211c7092bcf7509f3913cfa44145216e2c8d15` |
| `corpus/source-snapshots/round-30/manifest.json` | `8aacf77cf2f3d9c7912eea419a05e10604959b2faacb4ae3b0e097f8ab81f94b` |
| `corpus/source-snapshots/round-31/manifest.json` | `5fa37fd7249d043af1e36f98a549ee4ac8d6181e29f5def78116d3c637cb50e8` |
| `corpus/source-snapshots/round-32/S049.txt` | `962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8` |
| `corpus/source-snapshots/round-32/S050.txt` | `2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888` |

## 2. The four probes — run 1 vs run 2

| # | Command (from the lane root) | run 1 sha256 | run 1 exit | run 2 sha256 | run 2 exit | Verdict |
|---|---|---|---|---|---|---|
| 1 | `python3 corpus/instruments/capture-binding-check.py` | `1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1` | 0 | `1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1` | 0 | byte-identical |
| 2 | `python3 corpus/instruments/recheck-audit.py --quiet` | `450a22c9a42f0973fda00ee3a45b74ebcc54b407db0124850494e01ad19bfd24` | 0 | `450a22c9a42f0973fda00ee3a45b74ebcc54b407db0124850494e01ad19bfd24` | 0 | byte-identical |
| 3 | `python3 corpus/instruments/frontier-recheck-count.py` | `18a19fef7ce4fef7f80adb5bae7424129fa2a9f6435297ff8f7fc794ff0e14d3` | 0 | `18a19fef7ce4fef7f80adb5bae7424129fa2a9f6435297ff8f7fc794ff0e14d3` | 0 | byte-identical |
| 4 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049` | `4ca1f549a0549e9ee92a236c37a866301e3eebfdd2ef6480d661373e64a50224` | 0 | `4ca1f549a0549e9ee92a236c37a866301e3eebfdd2ef6480d661373e64a50224` | 0 | byte-identical |

stdout sizes: 714 / 324 / 1898 / 215 bytes. stderr was empty on all eight runs
(`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, 0 bytes).
Timestamps (run 1 → run 2): #1 04:37:03Z/04:37:03Z · #2 04:37:03Z/04:37:06Z ·
#3 04:37:09Z/04:37:10Z · #4 04:37:11Z/04:37:11Z.

Outputs (verbatim, run 1 of each):

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
```

```
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=21 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
```

```
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
```

```
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
```

## 3. Temporal repeat — same bytes, 23–31 s later

Re-ran all four at 04:37:34Z–04:37:42Z; both repeats of every command reproduced the §2 digests:

| Probe | 04:37:03 window | repeat 1 | repeat 2 |
|---|---|---|---|
| binding | `1861fec8…` | `1861fec8…` | `1861fec8…` |
| audit | `450a22c9…` | `450a22c9…` | `450a22c9…` |
| harness | `18a19fef…` | `18a19fef…` | `18a19fef…` |
| recheck S049 | `4ca1f549…` | `4ca1f549…` | `4ca1f549…` |

cwd independence (supplementary): at 04:38:00Z run 1 of the binding check executed with
`pwd = /home/vgpnk/Projects/shokunin` (fleet root, outside the lane) and produced sha256
`1861fec8…`, exit 0 — identical to the lane-root run. The instrument's default root comes from
its own path, and its directory walk is ordered (`sorted(os.listdir(base))`,
`corpus/instruments/capture-binding-check.py:145`), so the ordering is not filesystem-dependent.

## 4. Scratch honouring — `TMPDIR` and `HYAKU_SCRATCH`

Window 2026-10-26T04:37:23Z–04:37:24Z. Instrument digest identical before and after
(`b4182665…`, `diff` empty). Two environments:

- A: `env -u HYAKU_SCRATCH TMPDIR=/tmp python3 corpus/instruments/capture-binding-check.py`
- B: `env -u TMPDIR HYAKU_SCRATCH=/fast/scratch/hyaku python3 corpus/instruments/capture-binding-check.py`

| Env | plain run sha256 (×2) | exit | `--selftest` sha256 (×2) | exit |
|---|---|---|---|---|
| A `TMPDIR=/tmp` | `1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1` | 0 | `9c61334e369b2a413af55bbdb91628d31cf94d1a34d368d75bd5f878f9de1b4a` | 0 |
| B `HYAKU_SCRATCH=/fast/scratch/hyaku` | `1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1` | 0 | `9c61334e369b2a413af55bbdb91628d31cf94d1a34d368d75bd5f878f9de1b4a` | 0 |

Within each env the two runs of a command matched each other; across envs the byte equality was
asserted with `cmp`, which printed nothing:

```
$ cmp plain_tmpdir.run1.out plain_hyaku.run1.out && echo "plain outputs byte-identical across env"
plain outputs byte-identical across env
$ cmp selftest_tmpdir.run1.out selftest_hyaku.run1.out && echo "selftest outputs byte-identical across env"
selftest outputs byte-identical across env
```

Plain-run output under both envs equals the lane-root run of §2 (`1861fec8…`): the non-selftest
path writes no scratch at all. The selftest (744 bytes, 11 cases, failures=0):

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
```

**Where the fixtures actually landed** — observed, not inferred. A `tempfile.mkdtemp` observer
wrapped the stdlib function for one run per env and ran the checker's own `main()` with
`--selftest` (checker bytes unmodified, digest-bound above):

```
$ env -u HYAKU_SCRATCH TMPDIR=/tmp python3 spy_scratch.py corpus/instruments/capture-binding-check.py
SPY mkdtemp dir='/tmp' path='/tmp/capture-binding-selftest-ca3wqtcy'
selftest cases=11 failures=0
SPY checker_exit=0
$ env -u TMPDIR HYAKU_SCRATCH=/fast/scratch/hyaku python3 spy_scratch.py corpus/instruments/capture-binding-check.py
SPY mkdtemp dir='/fast/scratch/hyaku' path='/fast/scratch/hyaku/capture-binding-selftest-sbtetawk'
selftest cases=11 failures=0
SPY checker_exit=0
```

Both scratch roots resolve as the code says they should
(`corpus/instruments/capture-binding-check.py:425-436`: `--scratch`, then `$HYAKU_SCRATCH`,
then `$TMPDIR`, then `/fast/scratch/hyaku` when `/fast/scratch` exists, else the platform temp),
`HYAKU_SCRATCH` winning over `TMPDIR` by precedence. Residue after all runs:

```
$ ls -d /tmp/capture-binding-selftest-* /fast/scratch/hyaku/capture-binding-selftest-* 2>/dev/null
none
```

Fixtures are removed at exit, so identical stdout is not identical stdout-with-leftovers.

## 5. Superseded first pass (recorded, not cited)

A first pass ran 04:31:43Z–04:33:42Z on the same instrument digests but on an **earlier F16
entry** (`53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48`). That entry was
rewritten to `1f7ac0a2…` at 04:33:57Z (ExecEntryF16's receipt lands 04:35:11Z), outside that
window, so the pass no longer described the tree and was re-measured as §1–§4 above. Recorded
facts about it, measured and not inferred:

- The superseded pass's own before/after lists were identical (it was quiescent too); a diff of
  its post-window list against §1's pre-window list shows **exactly one changed line**, the F16
  entry (one `<`/`>` pair, `diff` exit 1).
- All four probe stdout digests were **unchanged** by that entry revision
  (`1861fec8…` / `450a22c9…` / `18a19fef…` / `4ca1f549…` before and after) — consistent with these
  probes printing the entry's file name, ids and counts rather than its prose. That is an
  observation on two revisions, not a general guarantee.
- Two mid-wave smoke runs taken before the instrument settled are **non-comparative and not
  cited** (04:23:28Z printed `records=40 bound=38 unbound=2` with `FAIL rule=no-row record=S049`;
  04:27:33Z printed `records=40 bound=40 unbound=0`).

## 6. PRE-STATE baseline (non-comparative — do not read as an after column)

Labelled per bound 6. At the **base commit** `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`,
materialised with `git archive 690b69da | tar -x -C $HYAKU_SCRATCH/kasegi-r33/ExecDeterminism/base`
(no lane writes), each command ran twice; every pair was already identical:

| Probe at base | exit (both) | stdout sha256 (both) | bytes | Note |
|---|---|---|---|---|
| `capture-binding-check.py` | 2 | empty (`e3b0c442…`) | 0 | file absent at base; stderr 160 B `can't open file` |
| `recheck-audit.py --quiet` | 1 | `1c083fc648336eaf8ed3d042332d82f100909e18a03b45570ece044ae4c06951` | 324 | `strict pass=1/44`, `expected=44` |
| `frontier-recheck-count.py` | 0 | `fe8170ec16e6c3490dff4b26a0a1239cbf7d54edae5eae58086f70526a9eb68c` | 1795 | `entries=18 pass=18` |
| `source-recheck.py … --source S049` | 2 | `ed7d0ed1d12dda44f34cac21852240cebb0fbadcc7b81c3612361c0b5f0eb439` | 36 | `manifest UNAVAILABLE reason=missing` |

This column is **not** compared to §2: the base bytes lack the round-32 manifest, the F16 entry
and two registry rows, so every differing number (audit exit 1→0, harness 18→19, recheck S049
exit 2→0, binding absent→`bound=40`) is a landed-edit effect, not a determinism finding. Its
only use here is to show the three pre-existing instruments were deterministic before this wave,
so any in-wave nondeterminism would have been an edit regression rather than pre-existing noise.

## 7. Findings

1. **Determinism holds for all four commands.** Two consecutive runs each, plus two more runs
   23–31 s later, produced byte-identical stdout and identical exit codes (all 0) on one
   verified-unchanged input set (19 digests; aggregate `6a5b48cf…` unchanged
   04:36:15Z→04:39:49Z).
2. **Scratch honouring holds.** `--selftest` fixtures land in `$TMPDIR` when `HYAKU_SCRATCH` is
   unset and in `$HYAKU_SCRATCH` when it is set; both placements print the same 744 bytes and
   exit 0, both are removed at exit, and the non-selftest run writes nothing.
3. **No lane-state leakage into stdout.** Across all measured runs (lane root, both envs, base
   export) no probe printed an absolute path, a scratch/temp name, a timestamp or a PID; the
   base `source-recheck` failure printed `manifest UNAVAILABLE reason=missing` — a reason, not a
   path. The only path-shaped text is lane-relative (`knowledge/…` entry names), and the
   fleet-root cwd run reproduced the lane-root bytes, so the working directory does not change
   them.
4. **Context for the frozen claims** (C1/C2, not re-scored here): on these bytes
   `records=40 bound=40 unbound=0` exit 0, `multi_row_url=2` (the erratum-1 informational count
   for the S024/S029 and S006/S028 shared URLs), `entries=19 pass=19` including
   `PASS F16 … ids=S049,S050`, and `S049:Q1–Q8 OK occurrences=1`.

## 8. Limits, risks, re-run condition

- **Digest-bound, not commit-bound.** The measurement is valid for the §1 digests at HEAD
  `53bfa59` plus wave edits, not for any later revision. During this wave the instrument's
  digest moved three times (`5fa7868b…` → `4bc7aed3…` → `b4182665…`) and the F16 entry once.
  **Re-run condition:** any post-04:39:49Z change to one of the 19 inputs invalidates §2–§4 and
  the four commands must be run twice again on the new bytes.
- **Four commands, one host, one interpreter.** This is not a claim that the instruments are
  deterministic on another filesystem, locale or Python version. Ordering is `sorted()` at
  `corpus/instruments/capture-binding-check.py:145` and by record id in `source-recheck.py`, so
  the mechanism is not incidental, but only Python 3.14.8 was exercised.
- **Identical stdout is not identical behaviour.** §4's stdout equality across envs is
  corroborated by the `mkdtemp` observer; the observer is instrumentation around the same
  bytes, not a separate implementation.
- **The audit's exit flip (base 1 → landed 0) is a wave effect.** `recheck-audit --quiet` now
  reports `strict pass=45/45`; the strict limbs moved because the wave's own edits landed, not
  because of anything measured here. Determinism means both runs agree, not that the value is
  good.
- An early runner version appended `; echo "…_exit=$?"` to each command, so its recorded
  wrapper status was the echo's 0 while the instrument's status sat in stdout. Those runs (the
  base-commit pass taken before the runner captured the command's own status) were discarded;
  every number above is the command's own exit status.
- No tool was installed or upgraded; no pacman/uv/npm/cargo action. No network access, no live
  target contacted, no credential material read or written (QUALITY Q6). Writes were confined to
  this receipt; git use was read-only (`rev-parse`, `status`, `log`, `archive`). Scratch lived
  at `/fast/scratch/hyaku/kasegi-r33/ExecDeterminism/` and was removed after this file was
  written.
