# MutC1Tamper — round-99 C1 mutation probe (attempt 1, wave 1)

Seat: `MutC1Tamper` (leaf, read-only attacker). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Report path: `.ufo/waves/round-99/w1/MutC1Tamper.md`; receipts: `.ufo/waves/round-99/w1/MutC1Tamper-receipts/`.

## Pins and bytes

| item | value |
|---|---|
| base | `b9411a6b530e486180cf14c72fccc46668dcf5ee` |
| freeze | `6195db307c1cb101eba1d268f8cbfc1578d2caf7` |
| C2 landing | `a3db47e71fe292c03b00ba11f38cccbec45d3966` |
| C1 landing | `35e3ab6041ff8690b00d831f27b93d08101fd16a` |
| instrument at C1 landing | `corpus/instruments/census-at-rev.py` sha256 `6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041` |
| frozen harness | `.ufo/waves/round-99/c1/tamper.py` sha256 `1d0810a2a7a9b5179fba482df782f1ee98547d3a638b6b2ca09925dfbb5be220` |

The instrument and harness bytes were extracted with `git show <C1 landing>:<path>` into scratch; the
lane's tracked source tree was never edited (only the report and its receipts under
`.ufo/waves/round-99/w1/` were written). The harness was run from the scratch copy after the sha256
check above. Fixture clone: `git clone --shared` of the lane at `$S/clone`, `git -C "$S/clone" checkout -B
mut 35e3ab60…`; `git -C "$S/clone" rev-parse --show-toplevel` printed `$S/clone`; both
`a3db47e7…` and `b9411a6b…` are ancestors of `mut` (`merge-base --is-ancestor` rc=0 for both).

## Method

1. Baseline control: frozen harness vs the unmutated landing instrument.
2. Twelve single-point mutants: each is a byte copy of the landing instrument plus one limb edit
   (full diffs in `MutC1Tamper-receipts/mutants.diff`; each compiles with `python3 -m py_compile`).
3. Harness run per mutant, same command, same revs, fresh work dir:
   `python3 -B $S/harness/tamper.py --lane $S/clone --rev a3db47e7… --alt-rev b9411a6b… --instrument $S/mutants/mNN.py --work $S/work/mNN`
4. Targeted probe per mutant: the pristine landing instrument and the mutant run on the *same*
   tampered census/state, so a pass by the mutant is a concrete wrong acceptance, not merely an
   unexercised line. Driver: `MutC1Tamper-receipts/probe-driver.py`; full output
   `MutC1Tamper-receipts/probes.txt`.

## Controls

Baseline (`baseline.txt`), landing instrument `6d68d9…`:

```
TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 rc=0
```

Restored bytes after all twelve mutant runs (`restored.txt`), same file, same sha:

```
TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 rc=0
```

Pristine-byte check after the runs:

```
sha256sum $S/instrument-landing.py
6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041  …/instrument-landing.py
git -C <lane> show 35e3ab60…:corpus/instruments/census-at-rev.py | sha256sum
6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041  -
```

Baseline per-class reasons (condensed; the full lines in `baseline.txt` carry `CENSUS-CHECK fail reason=… rc=1`):

```
T01-pinned-edited        header-sha-mismatch
T02-measured-at-repointed header-sha-mismatch
T03-measured-at-short    no-measured-at
T04-measured-at-missing  no-measured-at
T05-body-edited          body-sha-mismatch
T06-host-line-removed    no-host-inclusive
T07-host-line-edited     header-sha-mismatch
T08-body-from-other-rev  body-sha-mismatch
T09-poisoned-cache       pinned-mismatch
T10-pinned-from-host     header-sha-mismatch
T11-host-owned-edited    header-sha-mismatch
T12-body-truncated       body-sha-mismatch
```

## Results

`killed=12` means the harness rejected all twelve classes (the mutant **survived**). `killed=11`
means one class was accepted (the mutant was **killed**).

| # | limb removed | harness | verdict | probe: pristine vs mutant |
|---|---|---|---|---|
| M01 | `..` confinement reclassification | 12/12, sha `d4a3af96…` | **SURVIVED** | rates shift; P2 kills |
| M02 | 40-hex `measured-at` length | 12/12, sha `1625ee4c…` | **SURVIVED** | 12-hex accepted |
| M03 | `measured-at` ancestor check | 12/12, sha `f314757b…` | **SURVIVED** | dangling commit accepted |
| M04 | header digest | 12/12, sha `68f186c5…` | **SURVIVED** | edited `home:` accepted |
| M05 | body digest | 12/12, sha `d6212093…` | **SURVIVED** | still rejected (body equality) |
| M06 | cache bypass in `--check` | 12/12, sha `86e1416b…` | **SURVIVED** | consistent poisoned cache accepted |
| M07 | full pinned-line compare (SKILL only) | 12/12, sha `e432a5c0…` | **SURVIVED** | lane denominator accepted |
| M08 | host-owned header line | **11/12**, sha `3e62722e…` | **KILLED** (T11) | committed census also fails |
| M09 | pinned-line presence | 12/12, sha `3ba3a156…` | **SURVIVED** | missing pinned line accepted |
| M10 | cache key (lane instead of rev+instrument) | 12/12, sha `133f4a34…` | **SURVIVED** | stale A measurement reused for B |
| M11 | `resolve.py` exit-code check | 12/12, sha `db2a63dd…` | **SURVIVED** | failed resolver's TSV accepted |
| M12 | `--write` ancestor check | 12/12, sha `52dab64f…` | **SURVIVED** | non-ancestor write accepted |

Eleven of twelve single-point mutants survive the frozen harness. Only M08 is killed.

## Per-mutant evidence

### M01 — drop the `..` confinement (SURVIVED)

Diff: the `if klass == "INTERNAL" and walkout(cit): …` reclassification block is removed; every
INTERNAL row stays INTERNAL. Harness: `killed=12 total=12`; no class asserts the pinned triple
against the census of record, and the harness writes its own pristine census with the mutant, so the
change is self-consistent.

Probe (`probes.txt`):

```
PROBE P01-m01-rev-rates pristine[rc=0 CENSUS … skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1]
                        mutant  [rc=0 CENSUS … skill=162/732 corpus=2570/7624 lane=2608/8026 host_owned=76 confined=0]
PROBE P01-m01-committed-census pristine[rc=0 CENSUS-CHECK pass … lane=2607/8026 … confined=1]
                               mutant  [rc=1 CENSUS-CHECK fail reason=pinned-mismatch rc=1]
```

The confinement limb is real: it moves the pinned numerator by one (and the corpus numerator by one).
The harness escapes it; P2 (`--check` of the committed census of record) kills it. **Routed gap:
harness-only, covered by P2.**

### M02 — accept a 12-hex `measured-at` (SURVIVED)

Diff: `^measured-at: ([0-9a-f]{40})$` → `^measured-at: ([0-9a-f]{12,40})$` in `check`. Harness:
`killed=12`; T03's reason changes from `no-measured-at` to `header-sha-mismatch` — the header digest,
not the length regex, rejects the harness's short measured-at.

Probe: 12-hex measured-at, header digest recomputed, body's `Lane root` line rewritten to the short
form:

```
PROBE P02-m02-short-measured-at pristine[rc=1 CENSUS-CHECK fail reason=no-measured-at rc=1]
                                mutant  [rc=0 CENSUS-CHECK pass rev=a3db47e71fe2 skill=162/732 corpus=2569/7624 lane=2607/8026 …]
```

**Routed gap: the 40-hex length limb is masked by the header digest; add a short-measured-at class
with a recomputed header digest.**

### M03 — drop the `measured-at` ancestor check (SURVIVED)

Diff: the `if not ancestor_of_tip(lane, rev): …` block in `check` is removed. Harness: `killed=12`;
T02 repoints to `b9411a6b…`, which *is* an ancestor, so the ancestor limb is never exercised.

Probe: a 40-hex dangling commit `7f9cfe911bc668cb57e9d26f739b9445d32c5cba` with the measured tree
(`ancestor_of_mut=1`), header digest and body recomputed:

```
PROBE P03-m03-non-ancestor pristine[rc=1 CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1]
                           mutant  [rc=0 CENSUS-CHECK pass rev=7f9cfe911bc668cb57e9d26f739b9445d32c5cba …]
```

**Routed gap: no non-ancestor 40-hex measured-at class; add one with a recomputed digest.**

### M04 — drop the header digest (SURVIVED)

Diff: `if False and digest("\n".join(hdr)) != stored_h.group(1):`. Harness: `killed=12`; the semantic
comparisons kill T01/T02/T07/T10 (`pinned-mismatch`/`host-mismatch`), T11 (`host-owned-mismatch`),
T05/T08/T12 (`body-sha-mismatch`), T03/T04 (length), T06 (field presence), T09 (measurement).

Probe: edit the `home:` line and keep the stored header digest:

```
PROBE P04-m04-home-line pristine[rc=1 CENSUS-CHECK fail reason=header-sha-mismatch rc=1]
                        mutant  [rc=0 CENSUS-CHECK pass rev=a3db47e7… skill=162/732 corpus=2569/7624 lane=2607/8026 …]
```

`check` collects `hdr[1]` (the `home:` line) but never compares it to `HOME_LINE`; the header digest
is its only binding. The harness has no home-line class. **Routed gap: the header digest's unique
contribution is untested; add T15-home-line-edited.**

### M05 — drop the body digest (SURVIVED)

Diff: `if False and digest(body) != stored_b.group(1):`. Harness: `killed=12`; T05/T08/T12 now fail
with `body-mismatch` instead of `body-sha-mismatch`.

Probe: a body edit with the stored body digest:

```
PROBE P05-m05-body-edit pristine[rc=1 CENSUS-CHECK fail reason=body-sha-mismatch rc=1]
                        mutant  [rc=1 CENSUS-CHECK fail reason=body-mismatch rc=1]
```

The mutant still rejects the tamper. On the accept/reject boundary the body digest is redundant with
`body != mbody`; it changes the failure reason, not the verdict. **Coverage redundancy, not a false
acceptance.** No routed gap beyond noting the body digest is not independently tested.

### M06 — read the cache in `--check` (SURVIVED)

Diff: `measure(lane, rev, work, cache_ok=False)` → `cache_ok=True`. Harness: `killed=12`; T09's
reason changes from `pinned-mismatch` to **`host-mismatch`**. The harness's T09 only edits the pinned
line, so the untouched host line catches the fake even when the cache is read. The harness cannot
distinguish a cache-reading instrument.

Probe: a fully self-consistent poisoned cache and census — every header line agrees with the fake
rates (`162/733`, `2569/7625`, `2607/8027`), the body is the fake body, both digests recomputed,
cache key `a3db47e7…-86e1416b83ca.json`:

```
PROBE P06-m06-cache-read pristine[rc=1 CENSUS-CHECK fail reason=pinned-mismatch rc=1]
                         mutant  [rc=0 CENSUS-CHECK pass rev=a3db47e7… skill=162/733 corpus=2569/7625 lane=2607/8027 …]
```

The mutant accepts a census whose numbers no measurement supports. **Routed gap: T09 does not
isolate the cache bypass; add a consistent-poisoned-cache class (all header lines + both digests
recomputed).** This is the most serious survivor: the claim "`--check` never reads the measurement
cache" is not established by the harness.

### M07 — compare only the SKILL segment (SURVIVED)

Diff: `if hdr[2] != pinned_line(rates):` → compare only the substring before ` | corpus`. Harness:
`killed=12`; T01 is killed by `header-sha-mismatch`, and T09 by `body-mismatch` (the fake body's
extra newline), so the lane segment is never compared semantically.

Probe: pinned line's lane denominator `8026` → `8027`, header digest recomputed, body unchanged:

```
PROBE P07-m07-skill-only pristine[rc=1 CENSUS-CHECK fail reason=pinned-mismatch rc=1]
                         mutant  [rc=0 CENSUS-CHECK pass rev=a3db47e7… skill=162/732 corpus=2569/7624 lane=2607/8026 …]
```

The accepted census's pinned line says `lane 2607/8027`; the measured line says `2607/8026`.
**Routed gap: add a pinned lane-segment class with a recomputed header digest.**

### M08 — drop the host-owned line from the header (KILLED)

Diff: `HOSTOWNED_PREFIX` removed from `HEADER_FIELDS`, `host_owned_line(rates)` removed from
`header_lines`, and the `hdr[4]` comparison removed. Harness: `killed=11 total=12`; T11 is accepted
(`rc=0`) because `OWNED_RE` finds no host-owned line, so the tamper is a no-op and the check passes
the unmodified census.

```
TAMPER T11-host-owned-edited rc=0 want=nonzero FAIL reason=CENSUS-CHECK pass rev=a3db47e7… skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
TAMPER-RESULT killed=11 total=12 evaluated=12 instrument_sha256=3e62722ed513544ac6b61d4682fca90a80c6c7fde73ba6e7d2c1b929f2b46702 rc=0
```

The committed census also fails (`header-sha-mismatch`, because the committed header has five lines
and the mutant collects four). **KILLED — the only mutant the harness rejects.**

### M09 — accept a missing pinned line (SURVIVED)

Diff: a missing `PINNED_PREFIX` field appends `"…: (absent)"` and continues; the pinned comparison is
skipped when the marker is present. Harness: `killed=12`; no class removes the pinned line.

Probe: pinned line removed, header digest computed over the placeholder join, body unchanged:

```
PROBE P09-m09-missing-pinned pristine[rc=1 CENSUS-CHECK fail reason=no-pinned rc=1]
                            mutant  [rc=0 CENSUS-CHECK pass rev=a3db47e7… skill=162/732 corpus=2569/7624 lane=2607/8026 …]
```

**Routed gap: add T18-pinned-removed (digest recomputed).**

### M10 — key the cache by lane (SURVIVED)

Diff: cache path `rev + "-" + instrument_digest() + ".json"` → `"lane-" + sha256(lane)[:12] + ".json"`.
Harness: `killed=12`; the harness uses separate work dirs for the pristine and alt writes, and
`--check` does not read the cache.

Probe: write `a3db47e7…` then `b9411a6b…` in one work dir:

```
PROBE P10-m10-cache-key mutant[rc=0 CENSUS-WRITE ok rev=b9411a6b… skill=162/732 lane=2607/8026 …]
                        pristine[rc=0 CENSUS-WRITE ok rev=b9411a6b… skill=162/732 lane=2607/8022 …]
PROBE P10-m10-outB pinned mutant[SKILL 162/732 … corpus 2569/7624 … lane 2607/8026 …]
                          pristine[SKILL 162/732 … corpus 2569/7620 … lane 2607/8022 …]
PROBE P10-m10-outB laneroot mutant[… extract of `a3db47e7…`]
                             pristine[… extract of `b9411a6b…`]
```

The mutant's B census carries A's rates and A's body (the `Lane root` line names A) while its
`measured-at` is B. **Routed gap: no cache-key collision class; add a two-revision single-work-dir
write.**

### M11 — ignore `resolve.py`'s exit code (SURVIVED)

Diff: the `if r.returncode != 0: return None, None, "resolve-rc%d"` block is removed. Harness:
`killed=12`; `resolve.py` succeeds in every harness run.

Probe: a fixture commit `db58b5e0b8a2b5bb54f0de30dfed446dcbf215b0` whose `resolve.py` writes a TSV
and exits 1:

```
PROBE P11-m11-resolve-rc pristine[rc=2 CENSUS error reason=resolve-rc1 rc=2]
                         mutant  [rc=0 CENSUS rev=db58b5e0… skill=1/1 corpus=0/0 lane=1/1 host_owned=0 confined=0]
```

The mutant publishes a measurement from a failed resolver. **Routed gap: no failing-resolve class;
add T20-resolve-rc-with-tsv.**

### M12 — accept a `--write` revision that is not an ancestor (SURVIVED)

Diff: the `if not ancestor_of_tip(lane, rev): … rev-not-ancestor` block in `write_census` is removed.
Harness: `killed=12`; the harness only writes at `a3db47e7…` and `b9411a6b…`, both ancestors.

Probe: the same dangling commit `7f9cfe91…`:

```
PROBE P12-m12-write-non-ancestor pristine[rc=2 CENSUS-WRITE error reason=rev-not-ancestor rc=2]
                                 mutant  [rc=0 CENSUS-WRITE ok rev=7f9cfe911bc668cb57e9d26f739b9445d32c5cba skill=162/732 lane=2607/8026 …]
```

**Routed gap: the control receipt has a write-not-ancestor control, but the frozen harness does not;
add T21-write-non-ancestor.**

## Harness limb map

The 12/12 is real for the 12 named classes, but the classes are not limb-independent:

- **Header digest** is the first rejection for T01, T02, T07, T10, T11; the semantic comparisons
  (`pinned-mismatch`, `host-mismatch`, `host-owned-mismatch`) are the second limb. Dropping the
  header digest (M04) still scores 12/12 because every harness header tamper leaves the digest stale
  and the semantic comparisons catch it. The digest's unique binding — the `home:` line — has no
  class.
- **Body digest** is the first rejection for T05, T08, T12; `body != mbody` is the second. Dropping
  the body digest (M05) still scores 12/12.
- **Length regex** rejects T03/T04, but T03 is also caught by the header digest if the digest is
  stale; a 12-hex measured-at with a recomputed digest passes M02.
- **Ancestor check** is never exercised: T02's alt rev is an ancestor; no class uses a 40-hex
  non-ancestor.
- **Cache bypass** is never isolated: T09 edits only the pinned line, so a cache-reading instrument
  is killed by `host-mismatch` (observed under M06), not by the cache bypass.
- **Confinement, cache key, resolve exit code, `--write` ancestor** have no class at all.

## Routed gaps

| id | gap | detector that would close it |
|---|---|---|
| G1 | harness does not assert the pinned triple against the census of record | P2 already covers it (M01 killed by P2); no harness change strictly required |
| G2 | short `measured-at` is masked by the header digest | T13: 12-hex measured-at + recomputed header digest |
| G3 | no non-ancestor 40-hex `measured-at` | T14: dangling commit + recomputed digests |
| G4 | `home:` line is bound only by the header digest and has no class | T15: home-line edit |
| G5 | body digest is redundant with body equality | note only; no acceptance gap |
| G6 | T09 does not isolate the cache bypass | T16: fully consistent poisoned cache (all header lines + both digests) |
| G7 | pinned lane segment is masked by the header digest | T17: pinned lane edit + recomputed header digest |
| G8 | no pinned-line removal | T18: pinned line removed + recomputed header digest |
| G9 | no cache-key collision | T19: write A then B in one work dir |
| G10 | no failing `resolve.py` | T20: failing resolver + TSV present |
| G11 | no non-ancestor `--write` | T21: `--write` at a dangling commit |

## Restoration and bounds

- The lane's tracked tree was not modified by this seat. The only writes are
  `.ufo/waves/round-99/w1/MutC1Tamper.md` and `.ufo/waves/round-99/w1/MutC1Tamper-receipts/`.
  During the wave the lane's tracked tree changed from a sibling (`corpus/lessons/round-98.md`
  modified at 19:24 → `corpus/lessons/round-99.md` modified at 19:34; lane HEAD moved from
  `29cd3058…` to `2c2124f2…`). My evidence uses `git show` at the pinned C1 landing, so it is
  unaffected.
- Scratch `$S=/fast/scratch/hyaku/kasegi-r99/MutC1Tamper` was removed after the receipts were
  copied into the report directory.
- No tools were installed or upgraded (existing `python3`, `git` only).
- The fixture clone was created with `git clone --shared`; every fixture commit used
  `git -C "$S/clone"` after asserting `rev-parse --show-toplevel` = `$S/clone`.

## Verdicts

VERDICT: M01 drop the `..` confinement — SURVIVED (12/12); the harness never asserts the pinned triple against the census of record; P2 kills it. Routed gap G1, covered by P2.
VERDICT: M02 accept a 12-hex `measured-at` — SURVIVED (12/12); T03 is killed by the header digest, not the length limb; a 12-hex measured-at with a recomputed digest passes. Routed gap G2.
VERDICT: M03 drop the `measured-at` ancestor check — SURVIVED (12/12); T02 uses an ancestor; a 40-hex dangling commit with a recomputed digest passes. Routed gap G3.
VERDICT: M04 drop the header digest — SURVIVED (12/12); the semantic comparisons are redundant for the harness's header tampers; an edited `home:` line passes. Routed gap G4.
VERDICT: M05 drop the body digest — SURVIVED (12/12); the body equality still rejects every body tamper; equivalent on the acceptance boundary, coverage redundancy only. Routed gap G5 (note only).
VERDICT: M06 read the cache in `--check` — SURVIVED (12/12); T09 is killed by `host-mismatch`, not the cache bypass; a fully consistent poisoned cache passes. Routed gap G6, the most serious survivor.
VERDICT: M07 compare only the SKILL segment — SURVIVED (12/12); T01 is killed by the header digest; a pinned lane denominator of 8027 with a recomputed digest passes. Routed gap G7.
VERDICT: M08 drop the host-owned header line — KILLED (11/12); T11 is accepted because the tamper becomes a no-op; the committed census also fails. No routed gap.
VERDICT: M09 accept a missing pinned line — SURVIVED (12/12); no class removes the pinned line; a census without it passes. Routed gap G8.
VERDICT: M10 key the cache by lane — SURVIVED (12/12); no cache-key collision class; a B write reuses A's rates and body. Routed gap G9.
VERDICT: M11 ignore `resolve.py`'s exit code — SURVIVED (12/12); no failing-resolve class; a failed resolver's TSV is published as a measurement. Routed gap G10.
VERDICT: M12 accept a non-ancestor `--write` revision — SURVIVED (12/12); the harness never writes at a non-ancestor; a dangling-revision census is written. Routed gap G11.
VERDICT: frozen 12-class harness — CONFIRMED 12/12 on the landing instrument (`6d68d9…`) and 12/12 on restored bytes, but NOT limb-independent: 11/12 single-point semantic mutants survive; the 12/12 is a lower bound on tamper coverage, not a proof of the five limbs.
