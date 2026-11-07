# MutC2Counter — attack on the C2 counter itself (round 92, attempt 1, wave w1)

Seat: mutation-tester (leaf). Subject: the frozen C2 counter
`.ufo/waves/round-92/c2/capability-check.py`, sha256
`3feed3b073194179b5542f91d7bba80f8d1fba1a3c3a3ec3d4587ce1c6baa847`
(= claims.json `C2.counter_sha256`). Question: **can a forged instrument pass
K1-K8 unpinned?**

## Verdict

**Yes.** Seven forged instruments pass every limb (K1-K8) at all three seeds
(9191, 1, and a printed os.urandom seed) when the counter is run **without**
`--instrument-sha256/--gate-sha256`. One more (F7) passes 2 of 3 seeds and is
killed only by K7's single random sample. The K6 probe shows K6 never looks at
the candidate.

With the frozen pins supplied, F2 — a 4.9 KB lookup table with no detection
logic — fails **K1 only**; K2-K8 all pass. The two sha256 pins are therefore the
sole barrier, and K1 accepts their absence. The frozen C2 predicate P1 does
supply both pins, so the landing is not re-scored; everything below is a routed
counter defect plus a qualifier for every unpinned run (this round's own control
log contains one: `candidate-unpinned` prints `CAPABILITY-CHECK-RESULT pass`).

## Method

- `git clone --shared` of the lane at base `ee830069` into scratch; one commit
  per forgery on top of that base. The lane was never written; every git call
  used `-C <scratch>/clone` and its `rev-parse --show-toplevel` was asserted.
- Counter run unpinned:
  `python3 -B .ufo/waves/round-92/c2/capability-check.py --lane <clone>
   --rev <forgery commit> --work <scratch> [--seed N]`
- Seeds: 9191, 1, and one run with no `--seed` (the counter prints the drawn
  seed). Forged bytes, run log and diffs: see receipts.
- F2's commit also adds `corpus/source-snapshots/round-99/S999.txt` to the
  clone (synthetic `ghp_`+36 fixture, sha256 `f5ce7eb2…`, scratch only) as the
  positive control at `--rev` that the counter never applies.

## Matrix (unpinned)

| forgery | category | mechanism / statement bound it breaks | 9191 | 1 | random | verdict |
|---|---|---|---|---|---|---|
| F1-harness-gated | (a) fixture structure | `github-token` patterns dropped unless the `--lane` path contains the counter's own `c2check-`/`plant-`/`gen-` mkdtemp names | pass | pass | pass (4210930336) | **PASS** |
| F2-pathkey | (a) fixture paths | whole-file lookup table on `PLANT_EXPECT ∪ generated(0)` paths; stub selftest; fabricated clean summary | pass | pass | pass (1156529028) | **PASS** |
| F3-n-exception | (b)/(c) U2 | JSON `\n` exception widened to any letter `n` (`(?<=n)`) | pass | pass | pass (183035764) | **PASS** |
| F4-tail-base64url | (b)/(c) U3 | 36-char tail alphabet base62 → `[A-Za-z0-9_-]` | pass | pass | pass (915020290) | **PASS** |
| F5-jwt-floor-4 | (c) U5 | stateless JWT segment floor 10 → 4 | pass | pass | pass (2416794357) | **PASS** |
| F6-appid-99 | (c) U4 | stateless app-id digits 1-20 → 1-99 | pass | pass | pass (4154201033) | **PASS** |
| F7-left-digit | (c) U1 | left boundary drops digits and `_` (`(?<![A-Za-z])`) | pass | **FAIL K7** | pass (659581612) | seed-dependent |
| F8-azure-floor-20 | (c) U6 | Azure SAS `sig` floor 40 → 20 | pass | pass | pass (327379453) | **PASS** |
| P0-no-gh | (d) K6 probe | landed instrument minus `github-token` and its selftest cases | K4/K7/K8 fail, **K6 pass** | same | same (3822447911) | K6 blind |

Seven of eight forgeries are accepted as `CAPABILITY-CHECK-RESULT pass rc=0`.
F7 fails at seed 1 only because `generated(1)` happens to draw a digit for K7's
`live-n11` prefix; at seed 9191 and at 659581612 it draws a letter and the
mutant survives. See defect D4.

## The passing forgeries (exact diffs)

All diffs apply to the landed instrument bytes
`04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e`; commit
shas and the full run log are in `counter-forgery-runs.txt`, and the exact
hunks in `forgery-diffs.txt`.

### F1-harness-gated — the counter's own tempdir names are the capability gate

```diff
--- a/corpus/instruments/capture-secret-scan.py
+++ b/corpus/instruments/capture-secret-scan.py
@@ -269,6 +269,8 @@ def report(mode, results, scanned, allowed=0, unused=0):
 
 
 def scan_rev(lane, rev, pats, allow):
+    if not any(t in lane for t in ("/c2check-", "/plant-", "/gen-")):
+        pats = tuple(p for p in pats if p[0] != "github-token")
     items = [(p, o) for p, o in tree_blobs(lane, rev) if is_capture_path(p)]
```

`K4`/`K7` run on `mkdtemp(prefix="c2check-", dir=--work)` + `plant-*`/`gen-*`
repos, so the new shape works there; `K3` (and every real lane) is a directory
that does not carry those names, so the claimed capability is **absent from
every real scan**. All limbs pass, including K8 (which reads K4's hits, where
the gate is open). K1's selftest never passes a lane, so it stays green.

### F2-pathkey — a lookup table with zero detection logic

Whole-file replacement (`forgery-F2-pathkey.py.txt`, sha256 `8fdddee7…`):
a `TABLE` of the 28 `PLANT_EXPECT` pairs plus the 9 `generated()` expected pairs
(keyed on the counter's literal fixture paths), a basename map for the `--files`
trio, a stub `SELFTEST-RESULT pass cases=0`, the two `HISTORY_EXPECTED` paths
hardcoded for K2, and a summary that reports `hits=0 allowed=1 unused_allow=0`
on any other rev. It scans no bytes at all. It passes K1-K8 at all three seeds,
and with the pins it fails K1 only:

```
LIMB K1 FAIL selftest_rc=0 instrument_sha256=8fdddee7…
LIMB K2 pass …  LIMB K3 pass …  LIMB K4 pass …  LIMB K6 pass …  LIMB K7 pass …
LIMB K8 pass clauses=29 failing=none  LIMB K5 pass
```

K7 randomises values, so a *literal*-keyed detector (controls F8) fails; it
does not randomise **paths**, so a path-keyed detector passes at every seed.

### F3/F4/F5/F6/F8 — one-line mutants in K8's blind bounds

```diff
-_GH_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=\\n))"      + _GH_LB = rb"(?:(?<![A-Za-z0-9_])|(?<=n))"        (F3)
-        _GH_LB + rb"(?:gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])|ghs_[0-9]{1,20}_"
+        _GH_LB + rb"(?:gh[pousr]_[A-Za-z0-9_-]{36}(?![A-Za-z0-9_])|ghs_[0-9]{1,20}_"               (F4)
-_JWT_SEG = rb"[A-Za-z0-9_-]{10,}"                 + _JWT_SEG = rb"[A-Za-z0-9_-]{4,}"               (F5)
-        … |ghs_[0-9]{1,20}_"                      +        … |ghs_[0-9]{1,99}_"                     (F6)
-_SIG = rb"sig=[A-Za-z0-9%+/]{40,}(?:=|%3D){0,2}" + _SIG = rb"sig=[A-Za-z0-9%+/]{20,}(?:=|%3D){0,2}" (F8)
```

Each breaks a bound the frozen statement states (base62 alphabet; the narrow
JSON-escape exception; segments of 10+; `<1-20 digits>`; "every round-91 shape
behaves as before" with the 40-character SAS floor) and each is accepted. F5 is
not even caught by the instrument's own `--selftest`: its only short-segment
case uses 3-character segments, so K1 passes untouched. F8 likewise survives
the landed selftest. K4/K7/K8 have no plant for any of these bounds (U1-U6 in
`clause-coverage.txt`).

### F7-left-digit — the seed-dependent one

`(?<![A-Za-z0-9_])` → `(?<![A-Za-z])` (digits and `_` may precede the prefix).
K8's only left-boundary plant is S032 (a letter). K7's `live-n11` prefix is
`r.choice(b62 + "_")` — **one** character out of 63 per seed. At seed 1 it is a
digit, so K7 reports `extra=g/x-receipts/live-n11.txt|github-token` and kills
the mutant; at 9191 and 659581612 it is a letter and the mutant survives.
Deterministic classification: 9191 → letter, 1 → digit.

## K3's "clean" limb has no positive control (demonstrated)

The counter never puts a secret in the tree at `--rev`; it only requires
`hits=0, allowed>=1, unused_allow=0`. F2's rev `5fcb8b85…` carries
`corpus/source-snapshots/round-99/S999.txt` (synthetic, sha256 `f5ce7eb2…`).
The **landed** instrument at that rev reports:

```
HIT shape=github-token path=corpus/source-snapshots/round-99/S999.txt line=1
CAPTURE-SECRET-SCAN mode=rev:5fcb8b85… scanned=1883 hits=1 files=1 allowed=20 unused_allow=0 rc=1
```

The frozen counter at the same rev with F2's instrument prints
`LIMB K3 pass rc=0 summary=scanned=17456,hits=0,files=0,allowed=1,unused_allow=0`
and passes all limbs one more time. K3 therefore certifies nothing about the
scanner's `--rev` path.

## K6 is candidate-blind

K6 runs **BASE_REV's** instrument over K4's fixture repo and never touches the
candidate's bytes. P0 (landed instrument minus `github-token`, GH selftest cases
neutralised so K1 stays green) gets `LIMB K6 pass base_rc=1 base_hits=22
new_caught_by_base=none` at all three seeds while K4/K7/K8 fail. The frozen
controls' no-work run shows the same: K6 pass, K4/K7/K8 fail. K6 is a one-time
base regression, not a discriminator; every forgery above gets it for free.

## K8 clause coverage gaps (details and per-clause table: clause-coverage.txt)

K8 has 29 keys (16 `github-token`). The statement bounds with **no K8 key and
no K4/K7 plant**:

1. **U1** left boundary "digit or `_`" — S032 plants a letter only; K7 samples
   one random char (~17.5% of seeds exercise the boundary).
2. **U2** the JSON-`\n` exception's narrowness — only the positive is planted;
   a token after a *plain* letter `n` is not a negative.
3. **U3** "base62" alphabet — no 36-tail containing `-`/`_`.
4. **U4** stateless `<1-20 digits>` — no 0-digit and no 21+-digit plant.
5. **U5** "segments of 10+" — S034 uses 3-char segments; 4-9 and exactly 10
   are unplanted (the landed selftest shares this).
6. **U6** round-91 floors ("behaves as before") — Azure sig 40 (no 20-39
   plant), CloudFront sig 40 (S013 is 12 chars), GCS 64 hex (S005's first run
   is 36), CloudFront `Key-Pair-Id` 8-32, the 2-7-letter param window, >20
   params.

## Routed counter defects (with re-runnable commands)

- **D1 (primary) — K1 treats the sha256 pins as optional.** Any instrument that
  prints `SELFTEST-RESULT pass` passes K1; the behavioural limbs then certify a
  zero-capability instrument (F2, pinned, fails K1 only). Fix: make
  `--instrument-sha256` and `--gate-sha256` `required=True` (or add a
  `pins=absent` FAIL), so unpinned runs exit 2 and can never print `pass`.
  Rerun: `python3 -B .ufo/waves/round-92/c2/capability-check.py --lane
  <clone> --rev 5fcb8b85… --work <scratch> --seed 9191` (unpinned → pass),
  then add the two pins → `K1 FAIL`, `K2-K8 pass`.
- **D2 — no positive test of the new shape outside the counter's own fixtures.**
  K4/K7 repos live under `mkdtemp(prefix="c2check-")/plant-*|gen-*` and every
  expected pair is a literal path. F1 (harness-name gate) and F2 (path table)
  pass. Fix: add a `github-token` positive to K4's `--files` trio with a
  *randomised* file name and a run-time value (defeats path keying), and scan
  one positive through a rev whose directory name the counter does not choose.
  Rerun: the F1/F2 rows above.
- **D3 — K3 has no positive control at `--rev`.** A synthetic commit in the
  counter's scratch clone (never the lane) adding one GH value in a capture path
  with a random name, requiring exactly one `github-token` hit, closes F1, F2
  and K3 self-attestation in one limb. Rerun: landed instrument at
  `5fcb8b85…` shows `hits=1 rc=1`; F2's K3 says `hits=0`.
- **D4 — K7's `live-n11` negative is one random character.** Emit three
  deterministic boundary negatives (letter, digit, `_`) instead of
  `r.choice(b62 + "_")`; otherwise a left-boundary mutant survives ~52/63 of
  seeds (F7: killed at 1, survived 9191 and 659581612).
- **D5 — K8 must map U1-U6.** Add plants at the exact bounds: 36-tail with one
  `-`/`_`; 21-digit app id; 4-9-char JWT segments; token after plain `n`, after
  a digit, after `_`; 20-39-char Azure sig; and floor negatives for the
  round-91 shapes. F3/F4/F5/F6/F8 are the reruns.
- **D6 — K6 is not a candidate limb.** Drop it from the pass/fail set (BASE_REV
  is already pinned) or compare candidate-vs-base on a repo the candidate cannot
  key on. Rerun: P0 gets `K6 pass` with `K4/K7/K8 FAIL`.

## Files written (all under `.ufo/waves/round-92/w1/`)

- `MutC2Counter.md` — this report.
- `MutC2Counter-receipts/counter-forgery-runs.txt` — every limb line for 27
  unpinned runs plus the pinned F2 control and the landed-instrument cross-check
  (sha256 `824f6995…`).
- `MutC2Counter-receipts/forgery-diffs.txt` — exact hunks for F1, F3-F8, P0
  (sha256 `b0ed7ebf…`).
- `MutC2Counter-receipts/forgery-F2-pathkey.py.txt` — the whole F2 instrument
  (sha256 `8fdddee7…`; its diff is a whole-file replacement).
- `MutC2Counter-receipts/clause-coverage.txt` — the statement-clause/K8 table
  and U1-U6.

Scratch `/fast/scratch/hyaku/kasegi-r92/MutC2Counter/` (clone, fixtures, poison,
forgeries, run outputs) is deleted before yield. No tool installed or upgraded.
The lane tree was read-only for this seat; no counter/instrument bytes were
modified.
