# ExecI6Scan — round-41 wave-1 receipt (I6 scratch-scan limb)

Seat: `ExecI6Scan` (executor, leaf). Item: build the I6 scratch-scan limb — a sourceable bash
function that scans a scratch root for entries of the round-41 name family, case- and
separator-insensitively, recursively, dot-inclusively, excluding the canonicalized `--work` dir,
and fails closed on a scan error. Axis: **depth:verifiability** (primary), **coverage**.

**Verdict: PASS.** 16/16 graded selftest cases, 24/24 F1-F6 + item fixture assertions
(16 RED-OK + 8 GREEN-OK, 0 FAIL), 9/9 mutants killed.
Every assertion in the landed `.ufo/waves/round-41/wave1/ExecI11KillRule.fixtures.txt` F1-F6 block
reproduces with the exact payload values that file names.

No lane file, fleet file, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
`corpus/`, `templates/`, `scripts/`, `.ufo/state/` or `.scratch/` was written. No mutating
git/jj command was run anywhere. No subagent was spawned (leaf seat).

---

## 1. Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-41/wave1/ExecI6Scan.sh` | 510 | `e9341dcac5781e0ee41e004a53ab0c02f84f62932714222f7235abfca5bb2e25` |
| `.ufo/waves/round-41/wave1/ExecI6Scan.transcript.txt` | 207 | `0d89f5d87057202050be2f950d30c660cff2f18456389cc137f6c6c0c9bfc3c6` |

`ExecI6Scan.sh` contains only landable limb bytes: the sourceable functions, the hermetic probe,
and the header contract. No validation tables, notes or receipts inside it.
`ExecI6Scan.transcript.txt` carries the raw evidence (section 0-8 of the generator below).

### 1.1 API the suite calls

Sourcing `ExecI6Scan.sh` defines the following and executes nothing (`BASH_SOURCE[0] != $0` guard).
Direct execution runs `i6_main`.

```bash
i6_scan_scratch SCRATCH_ROOT WORK_DIR   # -> "strays=<n>,read=<ok|fail>" ; exit 0 green / 1 red
i6_scan_detail  SCRATCH_ROOT WORK_DIR   # -> "strays=,read=,scanned=,excluded=,tolerated=,error="
                                        #    + one "stray: <path>" line per stray
i6_scan_names                           # array I6_NAMES, newline-separated via this helper
i6_stray_count                          # integer I6_STRAYS
check_i6 / i6_check / i6_scan / check_i6_detail   # aliases -> same contract
```

`SCRATCH_ROOT` defaults to `$I6_SCRATCH_ROOT` (`/fast/scratch/hyaku`). `WORK_DIR` is **required**:
with no canonical work dir nothing can be excluded, so the limb fails closed (`read=fail`) rather
than printing a clean scan.

Knobs: `I6_FAMILY` (default `kasegi-r41`), `I6_SCRATCH_ROOT`, `I6_CHAIN` (`strict` default, or
`literal`).

CLI: `--check|--detail --scratch-root DIR --work DIR [--chain strict|literal]`,
`--self-test [--root DIR]`, `--help`. Exit 0 green / 1 red / 2 harness error.

### 1.2 Matching semantics (what I6 actually asserts)

- **Family**: `kasegi-r41` **and** `kasegi_r41`, in any letter case. Normalisation is
  one implementation (`i6_normalize_into`): strip **all** leading dots → lowercase →
  fold every separator character to `-` (`_`, U+00AD soft hyphen, U+2010 hyphen,
  U+2011 non-breaking hyphen, U+2012 figure dash, U+2013 en dash, U+2014 em dash,
  U+2015 horizontal bar, U+2212 minus sign, U+FE58 small em dash, U+FE63 small hyphen-minus,
  U+FF0D fullwidth hyphen-minus). The family token is normalised the same way, so
  `kasegi_r41` is matched without a second special case.
- **Prefix, not equality** (round-40 precedent): `kasegi-r41`, `kasegi-r41x`,
  `kasegi-r41-stray`, `.kasegi-r41-dot` all match; `kasegi-r40-*` and non-family names do not.
- **Recursive, any depth**: `find -mindepth 1` over the whole root (F1).
- **Every entry type**: directory, regular file, symlink (dangling included), dot-prefixed (F3,
  and the four D4 shapes below).
- **Exclusion**: only the canonicalized (`cd && pwd -P`) `--work` realpath and everything **inside**
  it are exempt. Entries are resolved with `realpath -m` (readlink-canonicalised), so a symlink
  named `kasegi-r41-link` that resolves directly to the work dir is tolerated (F5 control),
  while one resolving to an **ancestor** of the work dir is counted (F5 red), and any family-named
  entry inside `--work` is not counted (the "work dir inside the family container" case).
- **Clean-chain tolerance** (`I6_CHAIN=strict`, default): a family-named ancestor of `--work` is
  tolerated only if every level between it and `--work` holds exactly the next component and
  nothing else (`i6_chain_clean`). This is the round-40 wave-1 `ExecH6ScratchFixtures` contract and
  the CritKillRule §4 F5 fix direction. A contaminated chain reds (F2 red = 2, F5 variant = 1).
- **Fail-closed**: missing root, non-directory root, unresolvable `--work`, `find` non-zero exit,
  **or any non-empty `find` stderr** (a single unreadable entry anywhere under the root) every one
  yields `read=fail`, exit 1. The payload additionally names the offending path in `error=` so a
  red is diagnosable. There is no fail-open path (F6, F6 variant, chmod 000, mode 0311, unreadable
  nested entry).

### 1.3 Deviation from the item's literal wording, stated explicitly

The item says "count every match that is not the work dir itself nor inside it". Read literally,
the round's own container `/fast/scratch/hyaku/kasegi-r41` is a family match that is neither the
work dir nor inside it, so I6 could never be green on the live root and the frozen C1 after-state
(`closed=12/12` at Y) would be unreachable. The default therefore tolerates a family-named
**ancestor** of `--work` when, and only when, the chain down to it is clean — the round-40 wave-1
contract the wave-2 lab asked for — and the landed `ExecI11KillRule.fixtures.txt` F2 **honest
control** ("round container holding only the work dir is tolerated") requires exactly this.
`I6_CHAIN=literal` restores the literal counting verbatim:

```
# container holding only the work dir
strict (default)  -> strays=0,read=ok  rc=0     (tolerated=kasegi-r41-container)
I6_CHAIN=literal  -> strays=1,read=ok  rc=1     (the container is counted)
# work dir itself family-named, directly under the root
I6_CHAIN=literal  -> strays=0,read=ok  rc=0     (the work dir is still excluded)
# ...plus a real stray
I6_CHAIN=literal  -> strays=1,read=ok  rc=1
```

So `literal` differs from `strict` exactly on the ancestor case and nowhere else.

---

## 2. Required transcripts (verbatim from `ExecI6Scan.transcript.txt`)

### 2.1 The five required strays, in one sandbox

```
$ mkdir -p $SB/scratch/kasegi-r41-stray $SB/scratch/Kasegi_R41-stray $SB/scratch/kasegi_r41_stray \
           $SB/scratch/container/kasegi-r41-nested $SB/scratch/.kasegi-r41-dot
$ bash ExecI6Scan.sh --detail --scratch-root $SB/scratch --work $SB/work
strays=5,read=ok,scanned=5,excluded=none,tolerated=none,error=none
stray: kasegi-r41-stray
stray: Kasegi_R41-stray
stray: kasegi_r41_stray
stray: container/kasegi-r41-nested
stray: .kasegi-r41-dot
exit=1
```

### 2.2 Each stray reds exactly once (isolation)

```
-- solo: kasegi-r41-stray          -> strays=1,read=ok  exit=1
-- solo: Kasegi_R41-stray          -> strays=1,read=ok  exit=1
-- solo: kasegi_r41_stray          -> strays=1,read=ok  exit=1
-- solo: container/kasegi-r41-nested -> strays=1,read=ok  exit=1
-- solo: .kasegi-r41-dot           -> strays=1,read=ok  exit=1
```

### 2.3 Removing them greens the run

```
$ bash ExecI6Scan.sh --detail --scratch-root $SB/scratch --work $SB/work
strays=0,read=ok,scanned=0,excluded=none,tolerated=none,error=none
exit=0
```

### 2.4 The passed `--work` dir never reds

```
-- work dir is itself family-named and INSIDE the scanned root
   $ ... --scratch-root $SB/scratch --work $SB/scratch/kasegi-r41-work
   strays=0,read=ok,scanned=1,excluded=none,tolerated=kasegi-r41-work,error=none
   exit=0
-- work dir contents are family-named
   strays=0,read=ok,scanned=2,excluded=kasegi-r41-work/kasegi-r41-inner,tolerated=kasegi-r41-work
   exit=0
-- work dir on a CLEAN CHAIN under a family-named container
   $ ... --scratch-root $SB/scratch --work $SB/scratch/kasegi-r41-container/work
   strays=0,read=ok,scanned=1,excluded=none,tolerated=kasegi-r41-container,error=none
   exit=0
```

### 2.5 Fail-closed

```
-- chmod 000 root            -> strays=0,read=fail  exit=1
-- mode 0311 root (listable-failure)
                             -> strays=0,read=fail  exit=1  error=‘…/listed’:permission-denied
-- nonexistent root          -> strays=0,read=fail  exit=1
-- non-directory root        -> strays=0,read=fail  exit=1
-- unreadable entry in a readable root
                             -> strays=1,read=fail  exit=1  error=‘…/kasegi-r41-locked’:permission-denied
```

---

## 3. Kill-rule fixtures F1-F6 — exact match to the landed I11 spec

Driver: `fixtures.sh` in scratch, `fixture-failures=0`. Every RED and GREEN assertion in
`.ufo/waves/round-41/wave1/ExecI11KillRule.fixtures.txt` reproduces with the exact payload values
that file names (`strays=` counts included).

```
F1 nested-leftover                        strays=1,read=ok    rc=1  RED-OK
F1 control clean-root                     strays=0,read=ok    rc=0  GREEN-OK
F2 container+nested-leftover              strays=2,read=ok    rc=1  RED-OK
F2 control container-holds-only-work      strays=0,read=ok    rc=0  GREEN-OK
F3 dotfile-family                         strays=1,read=ok    rc=1  RED-OK
F3 control dotfile-nonfamily              strays=0,read=ok    rc=0  GREEN-OK
F3 counterpart no-dot-family              strays=1,read=ok    rc=1  RED-OK
F4 three-variants                         strays=3,read=ok    rc=1  RED-OK
F4 control r40-name-out-of-family         strays=0,read=ok    rc=0  GREEN-OK
F5 symlink-to-ancestor                    strays=1,read=ok    rc=1  RED-OK
F5 control symlink-directly-to-work       strays=0,read=ok    rc=0  GREEN-OK
F5 variant dir-holding-work-plus-junk     strays=1,read=ok    rc=1  RED-OK
F6 nonexistent-root                       strays=0,read=fail  rc=1  RED-OK
F6 variant non-directory-root             strays=0,read=fail  rc=1  RED-OK
F6 control existing-empty-root            strays=0,read=ok    rc=0  GREEN-OK
fixture-failures=0
```

F4 is `Kasegi-R41-Stray` + `kasegi_r41_stray` + `kasegi‑r41‑stray` (U+2011) → exactly `strays=3`,
the "partial catch is itself a defect" requirement.

---

## 4. Graded selftest (16 cases, 0 failures)

```
$ bash ExecI6Scan.sh --self-test --root $S/probe
selftest case=I6 clean-root-green              positive=pass verdict=pass
selftest case=I6 five-strays-red               positive=pass verdict=pass   (strays=5,read=ok)
selftest case=I6 strays-removed-green          positive=pass verdict=pass
selftest case=I6 work-dir-family-named-green   positive=pass verdict=pass   (tolerated=kasegi-r41-work)
selftest case=I6 work-dir-contents-green       positive=pass verdict=pass   (excluded=…/kasegi-r41-inner)
selftest case=I6 work-chain-clean-green        positive=pass verdict=pass   (tolerated=kasegi-r41-container)
selftest case=I6 work-chain-contaminated-red   positive=pass verdict=pass   (strays=1)
selftest case=I6 stray-regular-file-red        positive=pass verdict=pass   (strays=1)
selftest case=I6 stray-dangling-symlink-red    positive=pass verdict=pass   (strays=1)
selftest case=I6 unreadable-entry-red          positive=pass verdict=pass   (strays=1,read=fail)
selftest case=I6 listable-failure-root-red     positive=pass verdict=pass   (read=fail)
selftest case=I6 unreadable-root-red           positive=pass verdict=pass   (read=fail)
selftest case=I6 missing-root-red              positive=pass verdict=pass   (read=fail)
selftest case=I6 deep-nested-red               positive=pass verdict=pass   (strays=1 @ depth 3)
selftest case=I6 unicode-separator-red         positive=pass verdict=pass   (strays=1, U+2011)
selftest case=I6 out-of-family-green           positive=pass verdict=pass   (strays=0)
selftest cases=16 failures=0
selftest verdict=pass
exit=0
```

---

## 5. Eight-mutant coverage table

The item asks which mutant shapes the limb covers: **case, separator, nested, dotfile**, plus the
**four the round-40 H6 selftest missed**. `.ufo/waves/round-40/wave2/LabExportClean.md` §3.5 D4
names the missed fixture shapes: "no fixture covers **a non-directory entry**, **a dangling
symlink**, **an unreadable entry**, **a listable-failure root (0311)** or the dot-prefixed name" —
the dot-prefixed name is the limb's `dotfile` shape, so the four missed ones are the first four.
D4's own §4 mutant table records exactly those as the four survivors (M2 unreadable entry, M5
`find -type d` only, M9 `read=fail` no longer reds, M10 `find` failure ignored).

Each row below is a **real weakening applied to a copy of the delivered limb** in scratch, then the
copy's own graded selftest run. "killed" = the copy's selftest reports `failures>0`.

| # | shape | weakening applied | covered by selftest case(s) | verdict |
|---|---|---|---|---|
| M1 | **case** (item) | `n=${n,,}` deleted → match case-sensitive | `five-strays-red` (Kasegi_R41-stray) | killed |
| M2 | **separator** (item) | `_`→`-` and U+2011 folds deleted | `five-strays-red`, `unicode-separator-red` | killed |
| M3 | **nested** (item) | `-maxdepth 1` added → top-level-only scan (round-40 F1) | `five-strays-red`, `deep-nested-red`, `unreadable-entry-red` | killed |
| M4 | **dotfile** (item) | leading-dot strip deleted (round-40 F3) | `five-strays-red` (.kasegi-r41-dot) | killed |
| M5 | **non-directory entry** (D4 missed) | `-type d` added → files/symlinks invisible (D4 M5 survivor) | `stray-regular-file-red`, `stray-dangling-symlink-red` | killed |
| M6 | **dangling symlink** (D4 missed) | unresolvable entries `continue`d instead of counted | `stray-dangling-symlink-red` | killed |
| M7 | **unreadable entry** (D4 missed) | find rc/stderr check disabled → `read=fail` never set (D4 M2/M10 survivors) | `unreadable-entry-red`, `listable-failure-root-red` | killed |
| M8 | **listable-failure root** (D4 missed) | verdict no longer requires `read=ok` → `read=fail` stops redding (D4 M9 survivor) | `listable-failure-root-red` | killed |
| M9 | prefilter (added) | `-iname` → `-name` in the find prefilter (case-sensitivity reintroduced below the guard) | `five-strays-red` | killed |

`mutants=9 survived=0`.

M9 exists because the limb prefilters with `find -iname` for speed (the live root holds >1e6
entries; a per-entry bash normalisation forked once per entry and took >300 s, versus **2.1 s**
with the prefilter). The prefilter is only a **superset** filter — the authoritative check stays in
bash — and the superset property is proven separately:

```
$ names accepted by i6_is_family_raw but NOT printed by find -iname '*kasegi*r41*'
[empty]
$ names printed but not accepted (allowed: superset slack)
kasegiX-r41
```

---

## 6. Live-root behaviour (operational finding for the L1)

```
# as recorded in ExecI6Scan.transcript.txt section 8
$ bash ExecI6Scan.sh --detail --scratch-root /fast/scratch/hyaku --work $S/live-work
strays=1,read=ok,scanned=1,excluded=none,tolerated=none,error=none
stray: kasegi-r41
exit=1

# earlier in the same wave, with another seat's fixtures present under the container
strays=9,read=ok,scanned=9,excluded=none,tolerated=none,error=none
stray: kasegi-r41
stray: kasegi-r41/ExecSuiteCore/w/dbg/mut/i11/f1/scratch/container/kasegi-r41-stray
… (8 more, all under that seat's scratch)
exit=1
```

Two facts the L1 must design around:

1. **The round container is itself a family match.** On the live root, `kasegi-r41` is a hit unless
   `--work` sits on a clean chain inside it. This is the F2 geometry, and it is why the F2 honest
   control exists. The suite should either scan an isolated root (as the round-40 wave-1 reference
   limb did for its selftest) or place `--work` directly under the container with nothing else at
   that level.
2. **One unreadable directory anywhere under the root fails the whole scan.** Observed live
   during the wave: an unreadable dir in **another lane's** scratch (`tsukuroi-r47/C2SentTmp/ct2/d`)
   produced `read=fail` with `error=‘…/ct2/d’:permission-denied`; once that directory went away the
   scan returned `read=ok`. This is correct fail-closed behaviour, but it means the Y counting run
   needs a quiescent, fully-scannable root — an operational precondition, not a relaxation. The
   `error=` payload names the offending path so the cause is diagnosable without re-running.

---

## 7. Hygiene / controls

- Disk guard green throughout (`/fast/scratch/hyaku` 25%, 604.1G free at final check).
- **No tool installed or upgraded**; no `pacman`; no network fetch; nothing written to
  `~/.local/bin` or any PATH directory; `~/.omp/agent/{config.yml,mcp.json}` untouched.
- **No mutating git/jj command anywhere.** The limb reads no git state at all (it is a pure
  filesystem scan), so no fixture repo was needed and none was created.
- Writes were confined to the two deliverables, this receipt, and scratch
  `S=/fast/scratch/hyaku/kasegi-r41/ExecI6Scan` (`probe/`, `mut/`, `tmp/`, driver scripts).
  Nothing else under `kasegi-r41/` was ever removed by this seat: every `rm -rf` in the limb and
  in the drivers targets a path the seat itself created under `$S`, never `$S/..`.
- Scratch is removed before yield (`S` deleted after the receipt was written); no `kasegi-r41`
  sibling survives from this seat. **I6-class defect avoided.**
- Two host-level events happened during the wave that were **not mine**: at ~05:46
  `ExecI8Forge` removed the shared parent `/fast/scratch/hyaku/kasegi-r41` instead of only its own
  seat dir (acknowledged to me directly), and `MutC2Counters` reported a second sweep at ~08:34Z.
  My scratch was wiped once mid-run; every artifact above was regenerated afterwards and both
  deliverable hashes are from post-wipe runs. `MutC2Counters` was told (and confirmed) that this
  limb deletes nothing outside its own `$S`.
- L1 IRC alignment honoured: base literal corrected to the 40-char
  `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (only relevant to suites, not to this filesystem
  limb); I11 escape count is eight (F1-F8), of which **F1-F6 are my limb's** and F7/F8 belong to
  the pending-marker and worktree-clean limbs; out-of-family names stay green (`kasegi-r40-stray`
  is the F4 control and is verified green).

---

## 8. Risks / open items for the L1

1. **Adoption.** The suite (`ExecSuiteCore`) owns `corpus/instruments/r41-closure.sh`; it must
   source or inline `i6_scan_scratch` and print `I6 payload=<limb payload> closed=<0|1>`. Aliases
   (`check_i6`, `i6_check`, `i6_scan`) are provided so either naming works. The limb must be called
   in a non-fatal context (`out=$(i6_scan_scratch …) || rc=$?`) because it returns 1 on red.
2. **Live-root geometry** (section 6): the I6 check cannot be green on the raw live root unless
   `--work` is on a clean chain inside `kasegi-r41`, and it cannot be green at all while any
   unrelated lane leaves an unreadable directory under the root. Recommend the suite scan an
   isolated sandbox root for the graded case, and treat the live-root mode as the F1-F6 fixture
   driver.
3. **`--chain` default is `strict`.** If the suite wants the item's literal wording instead, pass
   `I6_CHAIN=literal`; the F2 honest control then reds, so `strict` is the mode consistent with the
   landed I11 fixture spec.
4. **Performance.** ~2.1 s for the live root (1.5e6 entries) with the `find -iname` prefilter; the
   fork-free normaliser is what makes that possible. Do not reintroduce `$(i6_normalize …)` in the
   scan loop — it forked once per entry and took >300 s.

Report: `.ufo/waves/round-41/wave1/ExecI6Scan.md`
