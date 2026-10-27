# ExecI9Isolate — receipt

Round 41, seat `ExecI9Isolate` (leaf executor; no subagents dispatched, no
labrat probe used). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; fleet root and
`/home/vgpnk/Projects/shokuknow` untouched; no mutating git/jj command run
anywhere; the only commits in existence are the lane's own (read-only
`git log`/`archive`/`show` used by this seat).

**Axis touched:** depth:verifiability (C1 limb I9). **Coverage:** not touched.
**Base commit:** `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (the 40-hex
literal in `.ufo/waves/round-41/claims.json`; the 38-hex
`5b29ea1439450b712581edf5f0bf98dfb262ab` in the seat prompt is a typo and
does not resolve — `git rev-parse --verify` on it returns
`fatal: Needed a single revision`, on the 40-hex form it resolves and is an
ancestor of `HEAD`).

## Files written

| path | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-41/wave1/ExecI9Isolate.notes.txt` (deliverable) | 214 | `21d8b2016338681b73c2653090ee583a71cd0f5a7dda005008095a16f2e10a4d` |
| `.ufo/waves/round-41/wave1/ExecI9Isolate.md` (this receipt) | — | — |

**No other file in the lane repo, the fleet repo, any sibling lane repo, or
any source tree was created, edited or deleted.** No file under `corpus/`,
`SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `PROVINCE.md`,
`MANIFEST.json`, `templates/`, `scripts/`, `.ufo/state/` or `.scratch/` was
touched. The r41 suite itself (`corpus/instruments/r41-closure.sh`) does not
exist yet and this seat did not create it — that is the suite core's
(`ExecSuiteCore`) file; this seat delivered the I9 specification and a
scratch prototype.

## What the item asked, and what was delivered

1. **The comparison contract (one paragraph)** — §1 of the deliverable, plus
   a six-point implementation checklist in §4.
2. **A scratch prototype demonstrating on one check**: honest payload → case
   pass; one-byte payload tamper → that case fails with `positive=fail`,
   other cases unaffected — §3 of the deliverable, transcript below.
3. **The exact output line format**
   `selftest case=I<n> <label> positive=pass|fail payload-match=1|0 verdict=pass|fail`
   — §2 of the deliverable, with the field table and the two judge rules
   that keep a summary-only or detail-free forgery from satisfying a case.

## Evidence: the r40 defect this closes (read-only, committed source)

Both halves of the I9 defect were confirmed against the **committed** r40
suite bytes (`git show HEAD:corpus/instruments/r40-closure.sh`, sha256
`bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`).

**Half one — the closed bit alone grades the positive limb.** `st_pos`,
lines 1287–1297:

```bash
st_pos() { # ID TREE REF
  local id=$1 tree=$2 ref=$3
  local out rc
  out=$(run_check "$id" "$tree" "$ref"); rc=$?
  if [ "$rc" -eq 0 ]; then
    printf 'selftest detail=%s positive=pass payload=%s\n' "$id" "$out"
    return 0
  fi
  printf 'selftest detail=%s positive=fail rc=%s payload=%s\n' "$id" "$rc" "$out"
  return 1
}
```

The payload is echoed into a detail line and **never compared** against the
values the fixture is supposed to produce.

**Half two — the value comparison is a shared, count-relative counter.**
`payload_matches`, lines 416–431:

```bash
# payload_matches FILE PAYFILE ID... — how many of the listed ids have a
# recorded `H<n> payload=` line in FILE equal to the canonical payload in
# PAYFILE. Pure: it compares bytes, it never runs a check.
payload_matches() { # FILE PAYFILE ID...
  local f=$1 pay=$2; shift 2
  local n=0 id rec want
  for id in "$@"; do
    rec=$(sed -n "s/^$id payload=\(.*\) closed=[01]\$/\1/p" -- "$f" 2>/dev/null | head -n 1)
    want=''
    if [ -n "$pay" ] && [ -f "$pay" ]; then
      want=$(awk -F'\t' -v id="$id" '$1 == id { print $2; exit }' "$pay")
    fi
    if [ -n "$rec" ] && [ -n "$want" ] && [ "$rec" = "$want" ]; then n=$((n + 1)); fi
  done
  printf '%s' "$n"
}
```

One number, over many ids — so one tampered payload moves a counter that
gates *other* checks (used by H5 at line 728/732 and H7 at line 546).

**The measured consequence** is recorded in the committed round-40 wave-2
report `.ufo/waves/round-40/wave2/MutH1H5.md` (its "Runs and verdicts"
table, mutant M-H3): a check reporting the **wrong payload values while still
exiting 0** (H3 payload `mentions=323,rows=83` instead of `mentions=1,rows=1`)
still graded `case=H3 positive=pass` — the mutant was killed only
*incidentally* by the mutant count falling to `0/2`. The same report's
observation 2 names the counter half: under the M-H5 patch the shared
`payload-match` reads `9` while two payload values contradict the receipt.

## Evidence: the prototype transcript

Prototype script (scratch only, **not** a deliverable, deleted with the
scratch dir): `/fast/scratch/hyaku/kasegi-r41/ExecI9Isolate/proto/i9-proto.sh`,
230 lines, sha256
`e80fcf28166b8c02f9879e0eaa1682c2028d163319317e81a42c1f10986b5f12`.
Transcript: `.../proto/transcript.txt`, 47 lines, sha256
`9aae32942055cea4d83ab7e0583526c0818abe6a466869a44cf7de6a34ac2b77`.

The prototype drives the **real committed r40 check functions**
(`check_h2`, `check_h3`, `check_h4`, sourced read-only from the lane) and the
**real lane export** obtained read-only via
`git -C <lane> archive <ref> | tar -x` into scratch. Export ref used:
`96dbd5f4276fcf8f93552fb97554485904cc0488` (lane `HEAD` at run time; pinned
in the transcript as `export-ref=`).

Verbatim transcript:

```
=== I9 payload-value isolation prototype ===

--- A. HONEST fixtures: every case payload equals its expected values
selftest detail=I1 positive=pass payload=corrections=4,named=4,missing=0,fences=closed
selftest detail=I1 mutant=correction-values-not-named rejected=1 payload=corrections=4,named=3,missing=1,fences=closed
selftest case=I1 corrections positive=pass payload-match=1 verdict=pass
selftest detail=I2 positive=pass payload=mentions=2,rows=1
selftest detail=I2 mutant=criterion-row-absent rejected=1 payload=mentions=1,rows=0
selftest case=I2 criterion-row positive=pass payload-match=1 verdict=pass
selftest detail=I3 positive=pass payload=s056=1,s058=1,s059=1,oversize=0
selftest detail=I3 mutant=s059-block-absent rejected=1 payload=s056=1,s058=1,s059=0,oversize=0
selftest case=I3 located-quotes positive=pass payload-match=1 verdict=pass
selftest cases=3 failures=0

--- B. LIVE EXPORT at a pinned ref, per-case expected map pinned
export-ref=96dbd5f4276fcf8f93552fb97554485904cc0488
export I1 payload=corrections=9,named=5,missing=0,fences=closed expected=corrections=9,named=5,missing=0,fences=closed payload-match=1
export I2 payload=mentions=1,rows=1 expected=mentions=1,rows=1 payload-match=1
export I3 payload=s056=1,s058=1,s059=1,oversize=0 expected=s056=1,s058=1,s059=1,oversize=0 payload-match=1

--- C. ONE-BYTE PAYLOAD TAMPER: export copy gets one extra prose mention
tampered I1 payload=corrections=9,named=5,missing=0,fences=closed rc=0 payload-match=1
tampered I2 payload=mentions=2,rows=1 rc=0 payload-match=0
tampered I3 payload=s056=1,s058=1,s059=1,oversize=0 rc=0 payload-match=1
honest  I2 payload=mentions=1,rows=1
tamper byte-diff: 1 byte(s) differ
--- C2. graded cases over the tampered export (per-case isolation)
selftest detail=I1 positive=pass payload=corrections=9,named=5,missing=0,fences=closed
selftest case=I1 corrections positive=pass payload-match=1 verdict=pass
selftest detail=I2 positive=fail rc=0 payload=mentions=2,rows=1
selftest case=I2 criterion-row positive=fail payload-match=0 verdict=fail
selftest detail=I3 positive=pass payload=s056=1,s058=1,s059=1,oversize=0
selftest case=I3 located-quotes positive=pass payload-match=1 verdict=pass
selftest cases=6 failures=1

--- D. r40-style grading on the same tampered fixture (contrast)
r40-style I2 positive=pass (exit code only; payload echoed, never compared)
r40-style I2 needle rows=1 accepted=1  exact payload-match=0

--- E. shared counter (r40 payload_matches style) vs per-case isolation
shared-counter control=2/3 (one counter gates every case)
per-case I1=1 I2=0 I3=1 (only I2 moved; no sibling gate moved)

--- F. MUTANT THAT EXITS NON-ZERO BUT REPORTS THE WRONG PAYLOAD
wrong-payload mutant actual=mentions=2,rows=0 rc=1 declared-expected=mentions=1,rows=0 exact-match=0

=== prototype done ===
```

### What the transcript establishes, property by property

| property the item asked for | where | measured result |
|---|---|---|
| honest payload → case pass | section A | all three cases `positive=pass payload-match=1 verdict=pass`; `selftest cases=3 failures=0` |
| one-byte payload tamper → that case `positive=fail` | section C | the I2 payload went `mentions=1,rows=1` → `mentions=2,rows=1`; `cmp -l` measures **1 byte** differing; the check's **exit code stayed 0** |
| other cases unaffected | section C2 | `selftest case=I2 criterion-row positive=fail payload-match=0 verdict=fail` while I1 and I3 stay `positive=pass payload-match=1 verdict=pass` |
| the closed bit alone would have passed it | section D | the r40-style exit-code-only grading of the same fixture reads `positive=pass`; a needle test also accepts it (`rows=1 accepted=1`) — so only the exact value comparison reds it (`exact payload-match=0`) |
| no sibling case reds through a shared counter | section E | shared counter `control=2/3` (moved by the tamper); per-case `I1=1 I2=0 I3=1` (only the tampered case moved) |
| a rejection for the wrong reason is caught | section F | mutant exits 1 but reports `mentions=2,rows=0` where `mentions=1,rows=0` was declared → `exact-match=0` |

The tamper is a **content** tamper on the export copy
(`corpus/QUALITY.md` gains one prose mention of `M39-2`), not a hand-edited
payload string: the check itself produces the drifted value, and the grader
catches it. The prototypes' expected payload maps for the synthetic fixtures
are ground truth **by construction of the fixture** (the fixture builder knows
what it planted), not values copied from a run.

## Format compatibility with the frozen claim

The r41 C1 predicate requires `--selftest` to print twelve graded
`selftest case=I<n> ... positive=pass ... verdict=pass` lines and
`selftest cases=12 failures=0`. The specified format satisfies that verbatim
(`positive=pass` present, `verdict=pass` last) and additionally exposes the
value comparison on the graded line as `payload-match=1|0`. Deliverable §2
also states the fallback for a suite core that prefers to keep r40's
`mutants=<ok>/<n>` field: it must not replace `payload-match=`, and the judge
must still require `payload-match=1`.

## Risks and open items (the L1's call, not this seat's)

- **The r41 suite does not exist yet.** The contract is a specification; the
  suite core must build the per-case expected payload maps, the parser, the
  per-key comparator, the judge and a committed one-byte tamper fixture into
  `corpus/instruments/r41-closure.sh`. This seat proves the contract is
  implementable against the real r40 check functions and the real export; it
  does **not** claim the r41 suite implements it.
- **The live-export expected payload maps must be measured at the verification
  ref Y**, not copied from any earlier ref: the corrections check's
  `corrections=<n>,named=<n>` counts depend on how many
  `Correction (round 41)` lines the L1 lands (zero such lines exist at
  `96dbd5f`; verified by `grep -c 'Correction (round 41)'` over
  `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-40.md` — all
  0). A map pinned at the wrong ref would red the whole selftest, so the
  suite must pin at Y or derive the map from the export it is grading
  **without** re-running the check under test (a self-comparison proves
  nothing).
- **The one-byte tamper fixture must be committed** (not built only in
  scratch) or the graded selftest cannot demonstrate the isolation property
  to the verifier; §4 item 6 of the deliverable states this.
- **Base-hash typo in the seat prompt** (§ above) is recorded here because the
  C1 counting commands name that ref; the 40-hex form in `claims.json`
  resolves.

## Hygiene

- Scratch: `/fast/scratch/hyaku/kasegi-r41/ExecI9Isolate/` (prototype,
  transcript, synthetic fixtures, export copies). **Removed before this
  receipt was finalized** — no `kasegi-r41/ExecI9Isolate` entry survives
  under the real scratch root.
- Scratch was wiped once mid-run by a sibling seat (`ExecI8Forge`, which
  reported the over-removal of the shared `kasegi-r41` parent); this seat
  recreated its scratch and **re-ran every step after that point**, so all
  evidence above is from the final run. The final prototype script sha256
  (`e80fcf28…`) is the one whose transcript is quoted.
- `TMPDIR` was set to the seat's own scratch (`$S/tmp`) for every run; `/tmp`
  was used only for small scratch shell fragments (< 1 MB each).
- Disk guard was checked before the pass
  (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
  `/fast/scratch/hyaku` 25 % used, 608.1 G free; `/tmp` 3 %; `/var/tmp` 35 %)
  and was green throughout.
- No tool was installed or upgraded by this seat (none was needed; **pacman
  was not run** — host-wide transactions are paused; no network fetch was
  made).
- No `git add`/`commit`/`push`/`checkout`/`reset`/`stash` and no `jj`
  mutation ran anywhere. The lane's tracked files are unmodified
  (`git status --short` shows only untracked `.ufo/waves/round-41/wave1/*`
  deliverables from this and other seats).
