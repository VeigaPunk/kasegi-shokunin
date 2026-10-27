# CritReceiptUtc — attack on `time-basis=ref-commit` (receipt-only seat)

Seat: CritReceiptUtc (leaf, no subagents). Scope: attack the time-basis of the
round-40 receipt model that round-41 C1/I2 inherits. Lane repo read-only;
writes: this receipt + scratch (removed). Verdicts on all three limbs: the
attack FAILS — `time-basis=ref-commit` is sound as implemented. No fix needed.

All transcripts are real command output captured 2026-10-27 from the lane repo
(/home/vgpnk/Projects/shokunin/kasegi-shokunin). No network fetches, no tool
installs, no git mutations anywhere (read-only git only; the one fixture repo
was created under scratch with `git init`, committed, and deleted).

---

## Limb 1 — reproduce the suite's run-utc derivation for Y and compare to the receipt

The r40 suite derives the stamp from the **epoch**, never from a wall clock
(`corpus/instruments/r40-closure.sh` lines 371–377):

```
ref_utc() { # REF
  local e
  [ -n "${1:-}" ] || return 1
  e=$(git -C "$LANE" log -1 --format=%ct "$1" 2>/dev/null) || return 1
  case $e in ''|*[!0-9]*) return 1 ;; esac
  TZ=UTC date -u -d "@$e" +%Y-%m-%dT%H:%M:%SZ
}
```

Reproduction against the lane (commands + output):

```
$ git -C lane log -1 --format=%ct d0fe34d ; TZ=UTC date -u -d "@<epoch>" +%Y-%m-%dT%H:%M:%SZ
ref=d0fe34d   %ct=1793053987  suite-render=2026-10-26T22:33:07Z
ref=c7aea5e   %ct=1793053957  suite-render=2026-10-26T22:32:37Z

$ git -C lane show -s --format=%cI d0fe34d
2026-10-26T19:33:07-03:00
$ git -C lane show -s --format=%cI c7aea5e
2026-10-26T19:32:37-03:00

$ git -C lane show d0fe34d:.ufo/waves/round-40/final-gates/all-gates.txt | sed -n '1,5p'
all-gates v4
export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd
suite-sha256=bdbd18a3239c3467c79b5b487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T22:32:37Z
```

**Finding:** `ref_utc(Y=d0fe34d)` = `2026-10-26T22:33:07Z` ≠ receipt's
`run-utc=2026-10-26T22:32:37Z`. The receipt's stamp equals `ref_utc` of the
receipt's **named export-ref** `c7aea5e` (round-40 judged head J7). This is
not a mismatch: `time-basis=ref-commit` binds the stamp to the receipt's named
ref, not to the commit that happens to carry the receipt file. The receipt at
Y names J7 and is a transcript of the run at J7; Y adds only the receipt. The
r40 verifier spot-check records exactly this expectation
(`corpus/lessons/round-40-verifier-spotcheck.md` line 37: "run-utc=…22:32:37Z,
which equals J7's committer instant (19:32:37-03:00, time-basis=ref-commit)
and comes before Y (19:33:07) | conformant").

**Verdict limb 1: attack fails.** A naive reading ("run-utc must equal Y's
committer instant") misreads the contract; the suite's own H7 shape check
compares the recorded stamp against `ref_utc` of the receipt's `export-ref`
line (lines 462–472), which is J7.

## Limb 2 — chicken-egg: could the L1 produce the receipt BEFORE committing Y?

Yes — necessarily so, and it is the intended bootstrap, not a defect. The
receipt never references Y, so its content is fully determined once J7 exists:
run the suite at `--export-ref c7aea5e`, tee the transcript, then commit Y
adding only that file. Verified binding facts:

```
$ git -C lane merge-base --is-ancestor c7aea5ef97902f38289cbdc1cf267068876a62dd d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5 && echo ancestor=YES
ancestor=YES
$ git -C lane diff --name-only c7aea5e d0fe34d
.ufo/waves/round-40/final-gates/all-gates.txt
$ git -C lane show -s --format=%P d0fe34d
c7aea5ef97902f38289cbdc1cf267068876a62dd
```

The r40 H7 ancestor limb is precisely the guard that makes this sound
(`r40-closure.sh` lines 532–548): `ancestor=1` requires the receipt's named
ref to be an ancestor of the invoked ref, and `diff-clean=1` requires the
diff between them to be nothing but the receipt. The selftest wires the
counter-case: an `export-ref=000…0` fixture must grade `ancestor=0`
(lines 1491–1493). The hypothetical self-referential variant (a receipt
naming Y inside Y) would require pre-pinning `GIT_COMMITTER_DATE` — possible
with git but unnecessary here; the J7/Y split avoids that circularity
entirely, and the `not-future` limb (`iso_past`, ≤ clock+120s) still rejects
future stamps, exercised by the H7-future negative control (lines 1488–1490).

**Verdict limb 2: no chicken-egg problem.** Receipt-before-Y with matching
run-utc is the designed flow; provenance is carried by ancestor + diff-clean +
digest + payload-match, not by wall-clock ordering.

## Limb 3 — timezone: does cross-timezone comparison of committer instants break?

Fixture (scratch repo, same absolute instant committed under two offsets;
verified `git rev-parse --show-toplevel` == fixture dir before committing;
fixture deleted after):

```
commit=e9d20a9 (GIT_COMMITTER_DATE='2026-10-26T19:33:07 -03:00')
  %cI=2026-10-26T19:33:07-03:00   %ct=1793053987   suite=2026-10-26T22:33:07Z
commit=0038190b (GIT_COMMITTER_DATE='2026-10-26T15:33:07 -07:00')
  %cI=2026-10-26T15:33:07-07:00   %ct=1793053987   suite=2026-10-26T22:33:07Z
epoch identical: YES
```

`%ct` is the absolute epoch — identical for the same instant regardless of
the commit-recorded offset. `%cI` preserves the recorded offset and is NOT
moved by the local TZ env (checked TZ=UTC, Pacific/Kiritimati,
America/Santiago — all print the recorded `-03:00`). A **textual** comparison
of `%cI` against the receipt's `…Z` string therefore false-negatives on the
lane's own Y commit:

```
suite-render=2026-10-26T22:33:07Z
%cI          =2026-10-26T19:33:07-03:00
textual match: NO
```

The suite never makes that mistake: it reads `%ct` (epoch) and renders a
canonical UTC string, comparing like-for-like UTC renders. Comparing instants
across timezones holds; only a naive string compare of offset-bearing `%cI`
output would break, and no check does that.

**Verdict limb 3: attack fails.** `%ct`-based derivation is timezone-immune;
`%cI` is display-only and the suite does not depend on its text.

## Boundaries (honest limits, not defects)

- The committer instant is self-asserted by the commit author (git honors
  arbitrary `GIT_COMMITTER_DATE`); `iso_past` only rejects stamps more than
  120s in the future. The contract treats the ref's recorded committer
  instant as ground truth by definition — falsifying it means forging the
  commit object itself, at which point the whole ref is adversarial and no
  in-tree receipt can rescue the model. The real anti-forgery weight is
  carried by payload-match (9 recomputed payloads), suite digest, the
  ancestor limb, and diff-clean.
- The receipt proves binding and re-derivation against the export, not that a
  human ran a command at a specific wall instant.

## Conclusion

`time-basis=ref-commit` survives all three attacks. Limb 1's apparent
mismatch (Y's committer instant ≠ receipt run-utc) is the intended semantics:
the stamp binds to the receipt's named export-ref (J7), which the committed
r40 receipt names and the spot-check already grades conformant. Limb 2 is the
designed J7→Y bootstrap, guarded by H7's ancestor and diff-clean limbs.
Limb 3 is immune because the derivation is epoch-based. The round-41 I2
claim language ("run-utc = ref committer instant") is consistent with this
reading — no correction required for C1/r41-closure.sh.

Evidence integrity: lane at claims-freeze fbba3d96cdf8d37c1ea41304a1ba35691329684b
(read-only); r40 Y blob read via `git show d0fe34d:<path>` from the lane;
fixture lived only under /fast/scratch/hyaku/kasegi-r41/CritReceiptUtc and was
removed. No other files written.
