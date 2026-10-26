# Round-35 claims erratum — D5 (round-34 C2 frozen-predicate wording)

Filed: 2026-10-26, seat `ScribeErratumD5` (round 35, wave 1). This is an **appended
correction**, not an edit: `.ufo/waves/round-34/claims.json` and
`.ufo/waves/round-35/claims.json` are frozen and untouched by this file. The L1
commits it; the canonical judge remains the only authority that scores it.

It discharges the fix that D5 names
(`corpus/lessons/round-34-verifier-spotcheck.md:189-194`): the round-34 C2 predicate
carries one clause that has no executable form as written and one that is literally
false. Both are restated below with invocations that were run against committed
bytes. Every measurement quoted here, with its exit code and digest, is in
`.ufo/waves/round-35/wave1/ScribeErratumD5.md` §Report.

Tree read at `da2d3c687f82a9814ee71c91c930cb733050d37c` (round-35 wave-1 dispatch
commit), claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.

## 1. What the frozen text says

Round-34 `claims.json` (frozen in `29f606d`; the bytes below re-read at this
tree's HEAD) — C2's fields, plus the C1 closure line that states the same C2
control:

| location | frozen sentence |
|---|---|
| C2 `predicate` | "…source-recheck S051 prints every assertion occurrences=1, sha256 OK, exit 0; … the junk F17 twin (c2-controls/junk-f17.md) is rejected by the admission gate." |
| C2 `after[6]` | "junk twin rejected: source-recheck exit != 0 and non-author reviewer REFUSE on record" |
| **C1** `after[10]` | "junk-twin control committed under c2-controls/ and rejected by the admission gate (source-recheck exit != 0; reviewer REFUSE) (R9)" — a C1 closure item (R9) that states the C2 control, which is why D5 is routed as a C2 predicate defect even though this sentence lives in C1 |
| C2 `kill_rule` | "…source-recheck S051 exit != 0; … junk twin passes source-recheck or is admitted." |

D5's ruling is that the **wording** is the defect and the **fact** is intact:
`RevJunkTwin` proves the rejection by quote comparison; `CritOverclaim` F1 and
`CritC2Kill` G5 are right that the phrase as frozen has no discriminating
invocation, and Q9/Q17 make "every assertion occurrences=1" false. The lesson
records both readings verbatim and leaves the adjudication to the judge
(`corpus/lessons/round-34.md:195-227`). This erratum restates the clauses so either
reading can be tested by execution.

## 2. Clause 1 — why "source-recheck exit != 0" does not discriminate

The twin's `recheck:` line (`.ufo/waves/round-34/c2-controls/junk-f17.md:11`)
targets the same manifest and `--source S051` as the admitted entry's line
(`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:6`); the only
differences are the entry's `cd <lane-root> &&` prefix and its trailing comment:

```
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
```

so running it re-checks the **real** manifest, not the twin's content:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
…
S051:Q9 OK occurrences=2 anchor=77-ok
exit=0
```

The other available route — handing the instrument the twin file itself — exits 2,
and it does so for *any* non-manifest, so it cannot tell the twin from a blank file:

```
$ python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-34/c2-controls/junk-f17.md --source S051
manifest UNAVAILABLE reason=unreadable-or-invalid
exit=2
```

Neither route is a discriminating invocation. "source-recheck exit != 0 on the
twin" therefore has no executable form as frozen; what the round actually measured
(`RevJunkTwin` §3, `RevC2BeforeAfter` §8, `ExecDoNothingReject` §3) is the
quote-comparison route restated next.

## 3. Clause 1 — restated with a discriminating invocation

Restated: **the twin is rejected only by a discriminating invocation that pins the
twin's own fabricated quote against the committed capture — a manifest whose
assertion is that sentence, sha256-pinned to the captured bytes, prints
`MISMATCH reason=quote-not-found` and exits != 0 — while the same invocation shape
on an assertion the capture does hold exits 0.** The comparison, not the twin's
`recheck:` line, is the gate.

Reproduction from the lane root (the capture is the committed blob, so the run is
byte-stable):

```bash
S="$(mktemp -d)/S051"
mkdir -p "$S"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show HEAD:corpus/source-snapshots/round-34/S051.txt > "$S/S051.txt"
python3 - "$S" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); cap = root / "S051.txt"
doc = {"schema_version": 1, "sources": [{
    "id": "S051", "path": "S051.txt",
    "sha256": hashlib.sha256(cap.read_bytes()).hexdigest(),
    "url": "https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/",
    "fetched_utc": "2026-10-26T00:00:00Z",
    "quotes": [{"id": "J1", "quote": "five severity levels for smart-contract exploits"}]}]}
(root / "manifest.json").write_text(json.dumps(doc, sort_keys=True) + "\n")
PY
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json" --source S051; echo "exit=$?"
```

Measured:

```
S051:sha256 OK
S051:J1 MISMATCH reason=quote-not-found
exit=1
```

The control that makes it discriminating — the identical fixture with the quote
replaced by text the capture holds (`At Immunefi, we classify bugs on a simplified
5-level scale:`, anchor 46):

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
exit=0
```

Both runs use the committed capture `corpus/source-snapshots/round-34/S051.txt`
(sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`, equal
to the round-34 manifest pin). The `quote-not-found` verdict is the rejection the
frozen kill rule presupposes; the twin's own line never produces it.

The "reviewer REFUSE" half is not a `source-recheck` output at all and cannot be
phrased as one: it is a **receipt requirement** — a non-author reviewer receipt
naming the twin as refused, committed under `.ufo/waves/<round>/wave1/`, or the
`non-author reviewer REFUSE on record` clause is unmet. The round-34 record shows
that requirement was not met on disk at composition time (`CritOverclaim` F1,
`CritC2Kill` G5; lesson `round-34.md:216-217`), which is why it must be stated as a
deliverable rather than as a checker line.

## 4. Clause 2 — why "every assertion occurrences=1" is literally false

The committed round-34 manifest pins 18 assertions on S051. The instrument prints a
**per-id occurrences** line for each one, with the count it observed and the anchor
note it verified. Measured on the committed manifest:

```
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q9 OK occurrences=2 anchor=77-ok
S051:Q17 OK occurrences=2 anchor=96-ok
(16 assertions occurrences=1; Q9 and Q17 occurrences=2 anchored)
exit=0
```

"Every assertion occurrences=1" is therefore false for two of the eighteen, and it
is false in the ordinary case rather than by accident: a quote that recurs in a
long capture is legitimate when it names the line it is read at. QUALITY Q9 is the
rule (`corpus/QUALITY.md:64`): the quote is exactly-once **or** carries an `anchor`
line number the instrument verifies, and the check prints the count it observed.
The instrument's `anchor_verdict` docstring implements exactly that. The admitted
entry's own recheck comment already uses the honest wording
(`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:6`: "18 assertions
(Q1-Q18) on the pinned capture, each `occurrences=1` or anchored (Q9/Q17)"), so the
frozen predicate contradicts the entry it admits — which is why the correction is a
wording fix to the claim, not to the entry.

Restated: **the predicate is a per-id occurrences statement, not an
all-equal-to-one statement — every assertion must print `OK` with its own
`occurrences=N`; a unique quote needs no anchor; a non-unique quote passes only
with a verified `anchor=N-ok`; an unanchored or broken non-unique quote fails and
drives exit != 0.** The three fixture runs that prove the distinction, all against
the committed capture:

| fixture assertion | measured | exit |
|---|---|---|
| `Permanent freezing of funds`, `anchor: 77` (non-unique + verified anchor) | `S051:Q9 OK occurrences=2 anchor=77-ok` | 0 |
| `Permanent freezing of funds`, no anchor | `S051:Q9 MISMATCH reason=occurrence-not-unique` | 1 |
| `Permanent freezing of funds`, `anchor: 1` | `S051:Q9 MISMATCH reason=anchor-broken` | 1 |

The instrument's own spelling covers the same limbs (`python3
corpus/instruments/source-recheck.py --selftest` → `selftest cases=10 failures=0`,
exit 0, including `double-occurrence`, `double-occurrence-anchored`,
`double-occurrence-out-of-range`, `double-occurrence-broken`, `quote-absent`).

Ruled reading of the round-34 C2 predicate: the clause "source-recheck S051 prints
every assertion occurrences=1, sha256 OK, exit 0" is read as "source-recheck S051
prints a per-id occurrences line for every assertion, each `OK` — sixteen
`occurrences=1`, Q9 and Q17 `occurrences=2` with anchors 77/96 verified — `sha256
OK`, exit 0". The kill rule is unchanged and is not triggered by this: it keys on
`source-recheck S051 exit != 0`, and the measured exit is 0. The same substitution
applies to `after[3]` ("source-recheck S051 exit 0, every assertion occurrences=1,
sha256 OK").

## 5. Recurrence in the round-35 frozen C2 (disclosure, not an edit)

Round-35 `claims.json` C2 (frozen at `617496b9`) repeats the same phrasings
verbatim: `predicate` ends "…source-recheck S052 prints every assertion
occurrences=1, sha256 OK, exit 0…", `after[3]` reads "source-recheck S052 exit 0,
every assertion occurrences=1, sha256 OK", and `after[6]` reads "junk twin
rejected: source-recheck exit != 0 and non-author reviewer REFUSE on record". This
erratum's restatements apply to them by reference; the frozen file stays as frozen.

Round-35-shaped execution of the discriminating invocation, run at read time against
the working-tree capture (untracked at that moment — `git status` lists
`?? corpus/source-snapshots/round-35/`; `manifest.json` did not exist yet, so no
per-id occurrences run for S052 exists at read time):

```
S052 capture sha256 d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826
fixture assertion: "five exploited vulnerabilities to the catalog every Tuesday" (junk-f18's own sentence)
S052:sha256 OK
S052:J1 MISMATCH reason=quote-not-found
exit=1
```

So the clause is executable for round 35 in the same form once the capture is
committed. This erratum does **not** claim any round-35 after-state: `entries=21
pass=21`, the S052 per-id line set, and census are other seats' measurements.

## 6. Forward rule for twins

Future twins should carry only absent sentences. A twin exists to prove that the
gate rejects text the capture does not hold; a sentence the capture *does* hold
makes the control mixed and lets a reader argue the twin was rejected for the wrong
reason. Measured, normalized (whitespace-collapsed, `<u>`/`</u>` stripped, the
instrument's own `normalize`):

- Round-34 `junk-f17.md`: `Direct theft of any user funds` → **1** occurrence (real
  text), `five severity levels for smart-contract exploits` → **0**. Mixed control,
  as `ScoutDatawalk` F-1b found.
- Round-35 `junk-f18.md`: `five exploited vulnerabilities to the catalog every
  Tuesday` → **0**, `scores each entry with a CVSS v4 vector rather than a due-date`
  → **0**. Both absent at read time — conforms.

A twin must also declare no manifest record of its own (both do), so its only
executable route is the quote comparison above.

## 7. Verification of this erratum's own literals

Run from the lane root; the C1 after-state requires both to be at least 1:

```
$ grep -c 'discriminating invocation' .ufo/waves/round-35/claims-erratum-d5.md
5
$ grep -c 'per-id occurrences' .ufo/waves/round-35/claims-erratum-d5.md
5
```

Measured on this file; both counts satisfy the `>= 1` requirement. The
pre-citation read of the round-34 defect lives at
`corpus/lessons/round-34-verifier-spotcheck.md:189-194`, which is the D5 entry
this file closes. (This file's own digest is recorded in
`.ufo/waves/round-35/wave1/ScribeErratumD5.md` §Report, not here: a digest written
inside the file it measures is stale the moment it is typed.)

## 8. Scope and non-effects

- Does not edit either frozen `claims.json`; corrections land as this appended file
  only.
- Does not change any score: C2 stays held 7, C1 unaffected, and the round-34
  dispute's facts remain as recorded.
- Does not assert round-34's `refuse` receipt existed, nor any round-35 after-state
  (`entries=21 pass=21`, S052 per-id lines, census). Those are gate measurements
  owned elsewhere.
- Does not adjudicate the readings in `corpus/lessons/round-34.md:195-227`; the
  canonical judge does, and this file only makes both readings executable.
