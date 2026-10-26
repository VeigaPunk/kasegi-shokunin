# CritC1Kill — falsification of C1 (depth:verifiability, held 4)

Seat: leaf critic, round 34 (hyaku run 8). Assignment: construct states that satisfy C1's
after-predicate while violating its kill rule — five named vectors — and say whether the
landed instruments catch each one (pass) or not (gap).

## Measurement window and digests

The tree is live: peers edited `kill-rule-check.py` while this review was running.
`corpus/instruments/kill-rule-check.py` mtime moved to `2026-10-26 02:43:37 -0300` and its
probe set grew from 3 to 6 (`unnamed-record-id`, `stale-orphan-declaration`,
`malformed-fetched-utc` added). Every finding below was **re-measured on the 6-probe bytes**;
the 3-probe copies I made earlier are discarded.

| file | sha256 measured |
|---|---|
| `corpus/instruments/r-defect-closure.sh` | `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d` (832 lines, with the self-report judge; supersedes the `2a635bf5…` 742-line and `0beafed2…` 655-line bytes measured earlier in this review — each was re-measured, not assumed) |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` (43138 B, 881 lines; supersedes the `7a20e724…` 37730 B / 6-probe bytes measured earlier in this review) |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` (supersedes `8a79010d…`; rule A still bidirectional — R9 in the current plain run reads `mirror=0 reverse=1`) |
| `SCORECARD.md` | `efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91` (supersedes `b8fc8c66…`; the R1 spelling re-test was run against these bytes) |
| `corpus/source-snapshots/round-32/manifest.json` | `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6` |
| `corpus/source-snapshots/round-26/manifest.json` | `33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa` |
| `.ufo/waves/round-34/c2-controls/junk-f17.md` | `2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026` |
| `.ufo/waves/round-34/c1-controls/fake-suite.sh` | `899416e3ffaced532009646bbc6b5c0c0a48825e67858fca0b2b200fa19900db` |
| `.ufo/waves/round-34/c1-controls/fake-killrule.py` | `7ca5d4fa97c6dadcb8f8b63a8f86f12a75d41335fdded8e46b1475a6cbb3b1af` |

## Report

### Baselines (all C1 counting commands reproduced on landed bytes)

```
$ bash corpus/instruments/r-defect-closure.sh
... R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
EXIT=0

$ bash corpus/instruments/r-defect-closure.sh --selftest
selftest case=R1..R9 live=pass fixture=rejected verdict=pass   (9 lines)
selftest cases=9 failures=0
EXIT=0

$ bash corpus/instruments/r-defect-closure.sh --root <git archive 014ee2d>
closed=0/9 exit=1
EXIT=1                                   # base bytes: all nine defects open, suite fails

$ python3 corpus/instruments/capture-binding-check.py --selftest
selftest cases=23 failures=0
EXIT=0

$ python3 corpus/instruments/capture-binding-check.py
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
EXIT=0

$ python3 corpus/instruments/kill-rule-check.py
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
probe punctuated-url-cell pristine=pass exit=0
probe malformed-orphan-declaration pristine=pass exit=2
probe nested-legacy-round pristine=pass exit=0
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
EXIT=0
```

Two literal-counter discrepancies against the frozen claim text:

- C1 `counting_commands`: `python3 .../capture-binding-check.py -> records=40 bound=40 unbound=0`.
  Measured **41/41** (digest above): `corpus/source-snapshots/round-34/manifest.json` holds one
  record (S051, C2's landing), `total records=41` over ten manifests. `unbound=0` and exit 0
  hold; the `40` figure is stale and reads as a mismatch to a verifier running it literally.
- `round-26` S040 binding is present and legitimately declared:
  `"orphans": [{"path": "S040-live.txt", ...}]` in
  `corpus/source-snapshots/round-26/manifest.json`, surfaced as `orphan=S040-live.txt`. R6 closes.

### Attack 1 — `r-defect-closure.sh` printing `closed=9/9` with vacuous checks

**1a. One vacuous check (R8 replaced with `return 0`), run in a lane-shaped tree**
(`…/e1/corpus/instruments/r-defect-closure.sh`, lane files symlinked; live root = real lane):

```
$ bash <mutated>/r-defect-closure.sh --root <lane>            # plain
R8 check=undescribed open=0
closed=9/9 exit=0                                             EXIT=0

$ bash <mutated>/r-defect-closure.sh --root <lane> --selftest
selftest case=R8 live=pass fixture=passed verdict=fail problems=fixture-not-rejected
selftest cases=9 failures=1                                   EXIT=1
```

**CAUGHT.** The `--selftest` discriminator is behavioural: it re-runs each check against a
fixture with that defect reintroduced and requires non-zero. `closed=9/9` alone is therefore
not sufficient to satisfy `--selftest cases=9 failures=0` when a check is inert.
Re-confirmed on the judged bytes `809aaf90…` in a lane-shaped tree:
`selftest case=R8 live=pass fixture=passed control=pass verdict=fail
problems=fixture-not-rejected`, `selftest cases=9 failures=1`, exit 1, while the plain run still
prints `closed=9/9 exit=0` — so the vacuity discrimination and the new self-report judge are
independent limbs.

**1b. Nine vacuous checks at once** (same tree, all `check_r1..r9` bodies → `return 0`):

```
$ bash <mutated>/r-defect-closure.sh --root <lane>            # plain
closed=9/9 exit=0                                             EXIT=0
$ bash <mutated>/r-defect-closure.sh --root <lane> --selftest
selftest case=R1..R9 live=pass fixture=passed verdict=fail    (9 lines, fixture-not-rejected)
selftest cases=9 failures=9                                   EXIT=1
```

**CAUGHT**, 9/9.

**1c. Summary-only suite** — the case loop replaced with
`printf 'cases=9 failures=0\n'; return 0` at the top of `run_selftest()`:

```
$ bash <mutated>/r-defect-closure.sh --root <lane> --selftest
cases=9 failures=0                                            EXIT=0
$ bash <mutated>/r-defect-closure.sh --root <lane>            # plain (unmodified)
closed=9/9 exit=0                                             EXIT=0
```

**WAS NOT CAUGHT at `0beafed2…` / `2a635bf5…` (GAP, narrow); CLOSED at `809aaf90…` (832
lines).** The earlier bytes had no structural self-report judge: a summary-only run printed the
exact strings C1's kill rule names (`cases=9 failures=0`, `closed=9/9`, both exit 0) while
performing zero checks. The committed control
`.ufo/waves/round-34/c1-controls/fake-suite.sh` does exactly this (digest above). Measured
here, not taken on report: the dispatcher now captures its own run and judges it
(`report_ok` / `plain_report_ok`): `--selftest` requires nine
`selftest case=R# live=pass fixture=rejected control=pass|absent verdict=pass` lines with
distinct ids R1..R9 and a matching summary; the plain run requires nine
`R# check=… open=[01]` lines plus the consistent `closed=K/9` line. Replayed forgeries:

```
A  summary-only --selftest   cases=9 failures=0 / judge=forged-summary rejected=1 /
                             selftest problem=self-report cases=0 expected=9          EXIT=1
B  summary-only plain run    closed=9/9 exit=0 / suite problem=self-report plain-lines=0 expected=9  EXIT=1
D  short report (8 lines)    selftest problem=self-report cases=8 expected=9           EXIT=1
```

Baselines on the same bytes: plain `closed=9/9 exit=0`, `--selftest cases=9 failures=0` with
`judge=forged-summary rejected=1`, `judge=short-report rejected=1`, `judge=complete-report
accepted=1`, base archive 014ee2d `closed=0/9 exit=1`.

**Stated bound, verified at its exact edge:** a *fabricated complete* report passes —
C2 (nine `selftest case=R# … control=pass verdict=pass` lines, no case loop) → EXIT 0;
E2 (nine `R# check=fabricated open=0` lines + `closed=9/9 exit=0`, no checks) → EXIT 0. This is
inherent to in-process self-judgement and is now symmetric with `capture-binding-check.py`'s
`judge_selftest_report` (whose `complete-selftest-report-accepted` case is the same property by
design). The discriminator for fabrication is the tree the run points at — the base archive must
read `closed=0/9`, measured — plus an external reader, not the suite's own judgement. Recorded
as a limit, not a gap. Impacted axis: depth:verifiability.

### Attack 2 — `capture-binding-check --selftest` with N>=19 trivial cases

Actual run: `selftest cases=23 failures=0`. Nine named cases are present exactly once each
(`per-file-orphan-detected`, `per-file-orphan-listed`, `nested-snapshot-dir`,
`fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`,
`double-https-row`, `rejected-row-anchor`, `summary-only-selftest-rejected`). Triviality was
tested by removing each limb and re-running the instrument's own selftest on the mutant copy:

| mutant (exactly-once patch) | selftest result |
|---|---|
| drop rule-A per-file orphan detection | `case=per-file-orphan-detected exit=0 want=1 verdict=fail`; `case=per-file-orphan-listed … verdict=fail`; `cases=23 failures=2`; EXIT=1 |
| `classify_fetched` accepts local offsets | `case=fetched-utc-local-offset-rejected exit=0 want=1 verdict=fail`; failures=1; EXIT=1 |
| `judge_selftest_report` returns `[]` | `case=summary-only-selftest-rejected exit=0 want=1 verdict=fail`; failures=1; EXIT=1 |
| `os.walk` made non-recursive | `case=nested-snapshot-dir … verdict=fail`; `case=nested-snapshot-missing-manifest … verdict=fail`; failures=2; EXIT=1 |

**CAUGHT (pass).** Cases assert exit status plus exact contract lines
(`judge_run`), and a green run requires `FAIL ` to be absent; the summary cannot be produced
without the case lines. No gap found for this vector.

### Attack 3 — `kill-rule-check.py` printing `survivors=0` while a mutant survives

**3a. Honest red aggregate (control that the tool is not an always-zero printer).**
A real, probe-invisible defect — `orphan_paths` accepting an empty `reason` (no selftest case,
no external probe covers it) — added through `--row-file`:

```
mutant-probe name=accept-orphan-without-reason probe=selftest-shape pristine=pass mutant=pass exit=0
mutant-probe name=accept-orphan-without-reason probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=accept-orphan-without-reason probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant=accept-orphan-without-reason killed=0
mutants=4 killed=3 survivors=1 invalid=0
gates=6 failed=1
survivors=1
EXIT=1
```

So the landed tool *can* report the red aggregate, and it refuses an instrument that already
carries a defect: `--instrument <drop-orphan-detection mutant>` →
`pristine selftest-refused reasons=exit=1;failures=2;case-verdict`, `survivors=1`, EXIT=1.

**3b. Forged false zero (bytes then current: `7a20e724…`, 6 probes).** Two exactly-once edits
to the counter:

1. the `accept-record-without-url` row's `find`/`replace` replaced by the real, probe-invisible
   `orphan_paths` defect (same patch as the survivor above);
2. the verdict line
   `result["verdict"] = "killed" if killed_by else "survivor"` →
   `… if (killed_by or row["name"] in ("skip-selftest-summary", "accept-record-without-url", "per-file-binding-removal")) …`.

```
$ python3 <forged>/kill-rule-check-forged.py --root <lane> \
      --instrument corpus/instruments/capture-binding-check.py \
      --fake .ufo/waves/round-34/c1-controls/fake-killrule.py
probe selftest-shape|record-without-url|per-file-orphan|unnamed-record-id|stale-orphan-declaration|malformed-fetched-utc pristine=pass
mutant-probe name=accept-record-without-url probe=selftest-shape           pristine=pass mutant=pass exit=0
mutant-probe name=accept-record-without-url probe=record-without-url       pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=per-file-orphan          pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=unnamed-record-id        pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=malformed-fetched-utc    pristine=pass mutant=pass exit=1
mutant=accept-record-without-url killed=1
mutants=3 killed=3 survivors=0 invalid=0
gates=6 failed=0
survivors=0
EXIT=0
```

**NOT CAUGHT at the counter I first measured (`7a20e7…`, 37730 B, 6 probes) → was a GAP; now
CLOSED at `c279d952…` (43138 B, 881 lines, 9 probes), re-verified here, not taken on report.**
`ExecKillRuleCheck` landed three defences (I re-ran each on the final bytes):

| forged variant | landed counter's response | exit |
|---|---|---|
| **A** my two edits above, pins intact | `mutant-invalid name=accept-record-without-url status=invalid:anchor-mismatch detail=find-or-patch-digest`; `GATE fail name=rows-valid`; `mutants=3 killed=2 survivors=0 invalid=1` | 1 |
| **B** A with the pin lookup replaced by `pinned = None` and the row swapped to a comment-only patch | `mutant-invalid … status=invalid:inconsistent-kill`; `GATE fail name=rows-valid`; `GATE fail name=controls` (unconditional forced kill also kills `CTL-equivalent`, so the survivor witness is lost) | 1 |
| **C** a named row renamed, pins intact | `mutants=3 killed=3 survivors=0 invalid=0` + **`GATE fail name=named-rows`** | 1 |

Note on A: with a *named-row-only* forced verdict (my original edit) only `rows-valid` fires;
the `controls` failure appears when the forced verdict is unconditional (B), i.e. the two gates
are genuinely independent, not duplicated. `ROW_PINS` (literal `find` and `find\0replace`
sha256, lines 195-205) catches the substitution in A before the guard is ever reached.

**Residual, by construction of the counter itself (`kill-rule-check.py:54-60` concedes it): an
edit that rewrites validation logic and the pins together.** D2 — substitute the row with a
probe-invisible weakening (`parse_round` returning `0` for unparsable directory names, i.e.
granting the archival exemption to non-round snapshot dirs), re-pin `ROW_PINS` to the new
digests, and exempt named rows from the `inconsistent-kill` guard:

```
honest control, unmodified counter + the same defect via --row-file:
  mutant=parse-round-legacy-for-unparsable killed=0 ; mutants=4 killed=3 survivors=1 ; gates=7 failed=1 ; survivors=1 ; EXIT=1

D2 (forged counter):
  mutant-probe name=accept-record-without-url … (9 probes, every line mutant=pass)
  mutant=accept-record-without-url killed=1
  mutants=3 killed=3 survivors=0 invalid=0
  gates=7 failed=0
  survivors=0
  EXIT=0
  counter_sha256=d9bc0c0b0ddfbb2b126e1fe4ed83a605afe58c2aee1ef7084a3db4488750e113
```

So `survivors=0` is still producible with a mutant alive — but only by bytes whose
`counter_sha256` differs from the pinned `c279d952…`. **Nothing in the tree pins that digest**:
`corpus/instruments/r-defect-closure.sh` never reads `kill-rule-check.py`, and
`.ufo/waves/round-34/claims.json` still names only `survivors=K`. The zero is therefore bound
to bytes by receipts, not by a gate. Correction: record the expected `counter_sha256` in the
frozen claims (or as an `R`-check constant) and compare it in the suite; make the kill rule
read exit code + `GATE`s + digest, never `survivors=` alone.

**Independently reproduced by `ExecKillRuleCheck` (§9b of its receipt):** the same
`parse_round` weakening via `--row-file` at the frozen bytes reads
`mutant=parse-round-nonround-dir-archival-exemption killed=0`, nine probes `mutant=pass`,
`survivors=1`, `GATE fail survivors-zero`, exit 1; and a dedicated fixture discriminates the
limb without touching the counter — `snapshots-x/` with one `"archival": true` record gives
pristine `FAIL rule=provenance-missing record=S001 dir=snapshots-x`, `records=1 bound=0
unbound=1`, exit 1 against the mutant's `records=1 bound=1 unbound=0`, exit 0. So this is a
**real coverage survivor**, not merely a forgery ingredient: neither the selftest table nor the
nine probes reach a non-round directory name. Correction: case
`non-round-dir-archival-rejected` (pristine must exit 1). Both seats agree it must not be landed
under review; it is routed to the L1.

The peer's concrete form of the byte binding, which I endorse: freeze
`test "$(sha256sum corpus/instruments/kill-rule-check.py | awk '{print $1}')" = c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`
in the claims or the suite — it needs no counter change. Verified by this seat that the digest
still reads `c279d952…` and that `claims.json` contains neither `counter_sha256` nor the digest
(`grep -c` → 0).

**3c. Trimmed row set (`MUTANTS = []`)** prints `mutants=0 killed=0 survivors=0 … survivors=0`
with `GATE fail name=controls` and EXIT=1. Here the `survivors=` line alone is insufficient,
but the tool's *exit code* is the discriminator — which C1's kill rule does not name.

### Attack 4 — strict-UTC regex satisfied by a value that is not a real fetch instant

**4a. Fabricated but well-formed instants pass both instruments.** Fixture tree with
registry rows S049/S050 and a round-32 manifest carrying
`"fetched_utc": "2026-10-25T04:16:06Z"` (wrong day) and `"2026-01-01T00:00:00Z"` (wrong
everything):

```
$ bash corpus/instruments/r-defect-closure.sh --root <fixture>
R8 check=round-32 manifest fetched_utc strict UTC (^YYYY-MM-DDTHH:MM:SSZ$), no '-' offset open=0

$ python3 corpus/instruments/capture-binding-check.py --root <fixture>
AUDIT records=2 with_url=2 with_fetched_utc=2 with_archival=0 … orphans=0
records=2 bound=2 unbound=0
EXIT=0
```

**4b. The suite's R8 was weaker than the instrument's rule C — CLOSED at suite digest
`2a635bf5…`.** On the earlier `0beafed…` bytes `"2026-10-25Tgarbage-not-a-timeZ"` read
`open=0` (closed) while rule C called it `detail=malformed`. On the landed bytes R8 now parses
the instants (`datetime.fromisoformat`, zero offset required, `+00:00` normalised to `Z`):

```
r8garbage     R8 that is not a strict-UTC instant  open=1     # rejected
r8fabricated  (2026-10-25T04:16:06Z)               open=0     # still accepted — see 4a
r8plus0       (2026-10-26T04:16:06+00:00)          open=0     # accepted, normalised
```

and its broken fixture is now the garbageZ form itself, so `--selftest` proves the parse limb
is load-bearing: `selftest case=R8 live=pass fixture=rejected verdict=pass`. The base tree still
reads `closed=0/9 exit=1` on the new bytes. Gap 4b: **no longer open**.

**4c. Calendar validation exists** — `2026-02-30T00:00:00Z` is rejected by
`capture-binding-check.py` (`detail=malformed`, `unbound=1`, EXIT=1). So the boundary is:
syntactic + calendar validity is checked; *provenance* is not.

**GAP (provenance limb only) → record.** The format half of this vector is now closed (§4b).
What remains: `fetched_utc` can be any real calendar instant; neither instrument ties it to a
fetch record. The landed values (`2026-10-26T04:16:06Z` / `04:16:16Z`)
are in fact provenance-backed — `corpus/lessons/round-33.md:31-32` records the live re-open
with HTTP 200 and 0 differing lines (`wave1/ScoutLiveDrift.md`) — so the landed bytes are
sound; the instruments merely cannot certify that property. R8 now agrees with rule C on the
accept set (`garbageZ` rejected by both), so this is one shared limitation, not a divergence.
Impacted axis: depth:verifiability.

### Attack 5 — per-file binding satisfied by listing every file as orphan

Fixture: one snapshot directory with three capture files, `"sources": []`, and all three
declared in `orphans` with reasons.

```
$ python3 corpus/instruments/capture-binding-check.py --root <fixture>
MANIFEST round-30 records=0 url_bound=0 fetched=0 archival=0
AUDIT records=0 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=3 orphan=S001.txt orphan=S002.txt orphan=S003.txt
records=0 bound=0 unbound=0
EXIT=0
```

**NOT CAUGHT by the instrument → GAP.** Rule A only asks that each capture be *declared*; a
directory can hold arbitrary captured bytes with zero provenance and still exit 0. The
`unbound = records - bound` invariant is trivially true at 0=0-0. The only discriminator is
C1's `records=40 bound=40` counting line (which would read `records=0`), and that line is
itself stale (measured 41/41, §Baselines). The `per-file-orphan-listed` case deliberately
admits a *single* declared orphan (correct), but there is no case or rule for the degenerate
all-orphan directory. Impacted axis: depth:verifiability.

### Additional states constructed (beyond the five)

**R1 spelling brittleness.** `SCORECARD.md` copy with placeholders respelled as `<LANE-HASH>`
and `{{LANE_HASH}}` appended:

```
$ grep -c '<LANE_HASH>' <fixture>/SCORECARD.md      -> 0
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
```

The landing defect class (unreplaced placeholder in a published table) is re-introducible in a
different spelling with R1 still green. Narrow gap; fix is a wider marker regex.

**Report-verifier limb is implemented but its own rejection is unproven by a case** (corroborates
`ExecCaptureBindingHarden`'s routed item; measured here on `3d9e5e0d…` by importing the module
and calling `judge_selftest_report` directly):

```
complete-23                 problems=[]                                        ACCEPTED
drop-one-keep-summary       problems=['case-line-count case=clean-all-pass count=0']          REJECTED
drop-one-honest-summary     problems=['case-line-count …', 'summary-cases=22 want=23']       REJECTED
dup-one-name                problems=['case-line-count … count=2', 'summary-cases=24 want=23'] REJECTED
extra-unknown-case          problems=['unexpected-case-line case=bogus-case', 'summary-cases=24 want=23'] REJECTED
```

`REPORT_CASES` (lines 806-810) pins only `summary-only-selftest-rejected` and
`complete-selftest-report-accepted`, so no case demonstrates the case-line-count limb failing.
Same class as 1c one level down: the guard works, its rejection is not self-witnessed. Fix: one
extra `forged_incomplete` report factory expecting `False` (a one-line addition, no behavioural
change to the instrument).

**Prose checks R1–R4/R6/R7 are presence tests.** Their `--selftest` fixtures prove each check
*can* fail when its block is removed (measured above), not that the appended text is truthful;
a keyword-bearing block satisfies them. This is inherent to prose closure and is not counted
as a separate gap, but it is why the discriminating weight must sit on the runnable
instruments (capture-binding, kill-rule, frontier rule A), not on the R-text checks.

### Impacted axes

- `depth:verifiability` (C1): gaps 4a (provenance), 5, R1 spelling, the attack-3 byte-binding
  residual (`counter_sha256` unpinned), and the `parse_round` coverage survivor; C1's
  after-predicate is satisfiable without the property it certifies on those routes.
  Closed at the digests in §Measurement window: 1c (self-report judge), 3b in-band guards,
  4b (R8 format).
- `coverage` (C2): unaffected by this seat. One interaction recorded: C2's round-34 record made
  C1's `records=40` counting command stale (41), so a verifier running C1's counter literally
  sees a mismatch that is not a defect in the tree.

### Smallest safe corrections (each deterministic, no redesign)

1. **Suite self-report judge** (gap 1c) — **landed** at `809aaf90…` and re-verified here:
   `report_ok`/`plain_report_ok` judge the captured run in both modes, `--selftest` proves the
   judgement on three forged reports first, and the summary-only forgeries now exit 1
   (`A`/`B`/`D` replays). Residual is the stated fabrication bound (`C2`/`E2`), inherent to
   self-judgement and symmetric with `capture-binding-check.py`.
2. **R8 full-instant validation** (gap 4b) — **landed** at suite digest `2a635bf5…` and
   re-verified here: full `datetime.fromisoformat` parse, zero offset required, `+00:00`
   normalised, and the broken fixture is now the `garbageZ` form so `--selftest` proves the
   limb load-bearing (`selftest case=R8 live=pass fixture=rejected verdict=pass`).
3. **Provenance cross-check** (gap 4a): require each `fetched_utc` to appear verbatim in a
   named evidence receipt (a manifest `fetch_receipt` field checked to exist and contain the
   instant, or `--receipts DIR`), plus a selftest case `fetched-utc-fabricated-no-receipt`
   expecting exit 1. The future-instant / round-window variant of this correction is
   **withdrawn**: `ExecCaptureBindingHarden` correctly objects that `now()` breaks the
   byte-identical determinism every lane instrument requires; a per-round legal interval
   declared as data (not a clock) is a round-35 design question, not a wave fix. What remains
   in-wave and clock-free is the receipt cross-check and R8 delegating to rule C.
   Independently reproduced by that seat on the same digest (`3d9e5e0d…`), including
   `2026-10-25Tgarbage-not-a-timeZ` → `detail=malformed` exit 1 under rule C.
4. **Degenerate-orphan rule** (gap 5): in `check()`, `FAIL rule=no-records dir=<dir>` when a
   manifest directory holds captures and `len(records) == 0` (and the same when no capture is
   named by any record); add case `all-captures-orphaned-rejected` expecting exit 1.
5. **Kill-decision consistency + row pin** (gap 3b) — **landed** at `c279d952…` and re-verified
   here: `invalid:inconsistent-kill`, `ROW_PINS` `invalid:anchor-mismatch`, and the
   `named-rows` gate. What is still missing is the byte binding: record the expected
   `counter_sha256` (`c279d952…`) in the frozen claims or as an `R`-check constant and have
   the suite compare it, so `survivors=0` from different bytes cannot read as evidence.
6. **R1 marker regex**: case-insensitive `<[^>]*lane[_-]?hash[^>]*>` and
   `\{\{[^}]*lane[_-]?hash[^}]*\}\}`, keeping the literal count line.
7. **Claim text**: restate the counting command as `records=41 bound=41 unbound=0 exit=0`
   (or `records==bound, unbound=0, exit 0`), and add exit codes / case-line requirements to
   C1's kill rule beside the bare `survivors=` and `cases=9 failures=0` strings.

### Verdict

C1's after-predicate **reproduces literally on the landed bytes**: `closed=9/9 exit=0`,
`selftest cases=9 failures=0`, base tree `closed=0/9`, `capture-binding --selftest
cases=23 failures=0`, `kill-rule-check survivors=0` with `mutants=3 killed=3 gates=7
failed=0`, 0 literal `<LANE_HASH>`, round-32 strict-UTC (Z-suffix, correct instants), S040
declared orphan. Nothing in the nine filed defects is still open on the tree I measured.

Falsifying the predicate, four of the five named vectors are now caught, three of them only
after this review's findings were fixed and re-measured:
- attack 1 (vacuous suite): inert checks caught by live/fixture discrimination; **summary-only
  caught at `809aaf90…`** in both modes (`A`/`B`/`D` replays exit 1), with the fabrication
  bound verified at its edge (`C2`/`E2` exit 0) and recorded as a limit;
- attack 2 (trivial cases): caught, four limb removals fail named cases;
- attack 3 (forged zero): caught in-band (`invalid:anchor-mismatch`, `invalid:inconsistent-kill`,
  `GATE fail named-rows`, all exit 1), residual = a consistent rewrite whose
  `counter_sha256=d9bc0c0b…` differs from `c279d952…`; no landed check binds that digest;
- attack 4: format half closed at `809aaf90…`/`2a635bf5…` (`garbageZ` rejected, fixture proves
  the limb);
- **two routes still satisfy the rule without the property**, both fixable and clock-free:
  (4a) a fabricated but calendar-valid instant (`2026-10-25T04:16:06Z`, wrong day) passes every
  instrument; (5) every capture declared orphan with zero records exits 0 with
  `bound=0 unbound=0`.

Auxiliary findings that remain open: R1's exact-spelling marker count, the unpinned
`counter_sha256`, the `parse_round` non-round-directory coverage survivor, and the stale
`records=40` counting command (measured 41/41).

These are **fixable defects, not a tradeoff the canonical judge must reject**: each remaining
gap has a deterministic, clock-free gate named above, and the honest red paths are intact
(`survivors=1` for a genuinely surviving extra row; a defective instrument is refused at the
pristine gate; the base archive reads `closed=0/9`). Because C1 is held at 4 and claims no
increase, the gaps do not falsify the round's stated movement; they do mean C1 must not be
cited as a verifiability *increase* until corrections 3–4, 6–7 and the digest binding land, and
the kill rule should be restated to require exit codes, per-case lines and a bound
`counter_sha256` rather than the bare summary strings.

Scratch: `/fast/scratch/hyaku/kasegi-r34/CritC1Kill/` removed at exit —
`ls -d /fast/scratch/hyaku/kasegi-r34/CritC1Kill` → `No such file or directory` (status 2).
No tool installs were needed; no writes outside the lane remain (one transient, see seat
hygiene below).

Seat hygiene (self-reported defect, corrected): the first write of this receipt resolved the
relative path against the session workspace root and landed at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-34/wave1/CritC1Kill.md` — the fleet root, which
is read-only to this seat. It was copied byte-identically (sha256
`ab80628cf39403dad34ef1e8f7f05b4b9512c29e97ef5d53b72ebd9a92a52ca6`) to this lane path and the
stray file was deleted; `ls` on the fleet-root path now reports
`No such file or directory`. Class: write-scope drift via relative-path resolution; captured-by
the assignment's absolute-path rule, which every later edit in this seat used.
