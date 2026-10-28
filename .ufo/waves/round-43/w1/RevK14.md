# RevK14 — attack review of the K14 correction-literal limb (RD42-1)

Seat `RevK14` (reviewer, leaf). Round 43, kasegi-shokunin. Base
`ab98fac9dce87130bc4f66de89e30650d63943dc`; claims-freeze commit
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. Axes: depth:verifiability, coverage.
Receipt-only item: no landable deliverable is produced by this seat.

Artifact under review (landed, stable for the whole pass):

```
$ sha256sum .ufo/waves/round-43/w1/ExecK14Corrections.sh
9fb97b4ce93a9d613e6508274517e4a9e4dc0b9e61b2639d966494d5eae238d3  .ufo/waves/round-43/w1/ExecK14Corrections.sh
$ stat -c '%s bytes %y' .ufo/waves/round-43/w1/ExecK14Corrections.sh
6787 bytes 2026-10-28 13:45:32 -0300
$ bash -n ExecK14Corrections.sh && echo "syntax ok"
syntax ok
```

Every run in §2-§3 is against a byte copy of that first landed revision (`sha256 9fb97b4c…`,
re-checked after the battery: identical). `check_k14` is called both as
`bash ExecK14Corrections.sh <export>` and, once, sourced
(`. ExecK14Corrections.sh; check_k14 <export>`) from `/` to prove the function form.

**Revision reviewed afterwards:** the executor revised the limb after §4 was filed; the revision
(`.ufo/waves/round-43/w1/ExecK14Corrections.sh`, 202 lines, `sha256
4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c`, `bash -n` clean) was
re-attacked with the same 22 fixtures plus six new ones and the same base/head/Y/r41 trees.
§9 carries that verification; §2-§8 are the record of the first revision.

## 1. How the limb was graded (independent reference)

I did not read the limb's rules as the oracle. Two independent artefacts were built first,
from the frozen claim + the seat spec only:

- `oracle_k14.py` — an independent implementation of the K14 predicates: correction ledger
  re-derived with the r42 `outside_lines`/`^Correction \(round (\d+)\)` semantics; literal
  regex `(?<![0-9A-Za-z_])(corrections|groups)=(\d+)(?![0-9])`; supersede = a later,
  same-file, outside-fence `Correction (round 43)` line naming the literal as a whole token;
  `mutant=`/`quarantined` lines skipped (R41), `payload=` lines counted when they are result
  claims. Two exclusion modes were implemented so the ambiguity in the instruction could be
  measured rather than assumed (§5).
- seventeen synthetic export trees, each with the three records plus a byte copy of
  `corpus/instruments/r42-closure.sh` (the limb's engine), each isolating one attack.

The limb and the oracle return the same `closed=` verdict on 14 of the 17 fixtures. The three
differences are `A3c` (limb green, oracle red — the F1 escape), `A11` (limb green, oracle red —
the limb exempts a fenced `payload=` transcript, which the instruction's `payload=` exclusion
authorises) and `A7` (limb red, oracle green — the limb grades a `live=` claim on its own marker
line, which its contract requires and my oracle does not). That agreement on the other fourteen
is what makes the divergences findings rather than taste.

## 2. The six assigned attacks — results

Each block below is that run's complete output: the `K14 <diagnostic>` lines are stderr, the
`K14 payload=…` line is the only stdout line (`2>/dev/null | wc -l` ⇒ `1`, measured).

| # | Attack | Correct verdict | Limb verdict | Holds? |
|---|---|---|---|---|
| 1 | stale literal inside a **fenced block** | red | `stale=1 … closed=0`, exit 1 | **yes** |
| 2 | **two `corrections=` literals in one line**, second stale | red | `literals=3,stale=1 … closed=0`, exit 1 | **yes** |
| 3a | literal inside **quoted defect evidence** (`mutant=`) | green (excluded) | `literals=2,stale=0 … closed=1`, exit 0 | **yes** |
| 3b | stale literal on a **`payload=` result quote** (`SCORECARD.md:1634` shape) | red (counted) | `literals=2,stale=1 … closed=0`, exit 1 | **yes** |
| 3c | same shape **plus the word `attack`** (my addition) | red | `literals=0,stale=0 … closed=1`, exit 0 | **NO — F1** |
| 4a | **near-token `corrections=330`** at live 33 | red | `stale=1 … corrections=330 live=33 closed=0`, exit 1 | **yes** |
| 4b | `corrections=330` at live 330 | green | `stale=0 … closed=1`, exit 0 | **yes** |
| 4c | near-token **cannot be excused by a marker naming `corrections=33`** | red | `stale=SCORECARD.md:34 corrections=330 live=34 … closed=0`, exit 1 | **yes** |
| 5 | correction **names the literal but not the live value** | green per frozen C1 text | `superseded=2 … closed=1`, exit 0 | **yes (coverage gap §6)** |
| 6 | **supersede marker in a DIFFERENT file** than the literal | red | `stale=SCORECARD.md:2 corrections=1 live=3 … closed=0`, exit 1 | **yes** |

Exact stdout:

```
### 1  fenced stale literal
$ bash ExecK14Corrections.sh fx/A1-fenced
K14 stale=SCORECARD.md:8 corrections=1 live=2
K14 payload=literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0
exit=1

### 2  two literals on one line (line: "…corrections=2,groups=0 while the older quote said corrections=1")
$ bash ExecK14Corrections.sh fx/A2-twoperline
K14 stale=SCORECARD.md:3 corrections=1 live=2
K14 payload=literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0
exit=1

### 3a quoted defect evidence: "defect evidence: mutant=`corrections=1,groups=0` was accepted by the r42 counter"
$ bash ExecK14Corrections.sh fx/A3a-defectevid
K14 payload=literals=2,stale=0,superseded=0,live=corrections=2,groups=0 closed=1
exit=0

### 3b payload= result quote (the SCORECARD.md:1634 shape)
$ bash ExecK14Corrections.sh fx/A3b-payloadquote
K14 stale=SCORECARD.md:3 corrections=1 live=3
K14 payload=literals=2,stale=1,superseded=0,live=corrections=3,groups=0 closed=0
exit=1

### 4a near-token at live 33
$ bash ExecK14Corrections.sh fx/A4a-neartoken
K14 stale=SCORECARD.md:34 corrections=330 live=33
K14 payload=literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0
exit=1

### 4b near-token equal to live
$ bash ExecK14Corrections.sh fx/A4b-live330
K14 payload=literals=2,stale=0,superseded=0,live=corrections=330,groups=0 closed=1
exit=0

### 4c marker names corrections=33 while the carrier says corrections=330
$ bash ExecK14Corrections.sh fx/A4c-near-excuse
K14 stale=SCORECARD.md:34 corrections=330 live=34
K14 superseded=SCORECARD.md:35 corrections=33 live=34
K14 payload=literals=3,stale=1,superseded=1,live=corrections=34,groups=0 closed=0
exit=1

### 5 correction names the literal, states no live value
###   line: "Correction (round 43): the older quote `corrections=1` is superseded."
$ bash ExecK14Corrections.sh fx/A5-nolivevalue
K14 superseded=SCORECARD.md:3 corrections=1 live=3
K14 superseded=SCORECARD.md:4 corrections=1 live=3
K14 payload=literals=2,stale=0,superseded=2,live=corrections=3,groups=0 closed=1
exit=0

### 6 marker in LOG.md for a literal carried by SCORECARD.md
$ bash ExecK14Corrections.sh fx/A6-crossfile
K14 stale=SCORECARD.md:2 corrections=1 live=3
K14 superseded=LOG.md:2 corrections=1 live=3
K14 superseded=LOG.md:2 corrections=2 live=3
K14 payload=literals=4,stale=1,superseded=2,live=corrections=3,groups=0 closed=0
exit=1
```

Four controls outside the six, all holding:

```
### 7 live= claim on a Correction (round 43) line is still graded
$ bash ExecK14Corrections.sh fx/A7-liveassert
K14 stale=SCORECARD.md:3 corrections=99 live=3
K14 payload=literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0
exit=1

### 8 marker BEFORE the carrier excuses nothing (strictly-later rule)
$ bash ExecK14Corrections.sh fx/A8-markbefore
K14 superseded=SCORECARD.md:1 corrections=1 live=3
K14 stale=SCORECARD.md:4 corrections=1 live=3
K14 payload=literals=3,stale=1,superseded=1,live=corrections=3,groups=0 closed=0
exit=1

### 9 marker line that also carries mutant= still excuses an earlier carrier
$ bash ExecK14Corrections.sh fx/A9-markevid
K14 superseded=SCORECARD.md:3 corrections=1 live=3
K14 payload=literals=1,stale=0,superseded=1,live=corrections=3,groups=0 closed=1
exit=0
```

`A10`, `A11`, `A12` are the extra probes referenced in §4 and §5.

## 3. Context measurements (the limb's own required states)

```
### base ab98fac9 (exact export; records byte-identical at 4cb6d4a: `git diff --stat ab98fac9 4cb6d4a -- SCORECARD.md LOG.md SHONEN.md` empty)
$ bash ExecK14Corrections.sh base
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
exit=1

### HEAD 4cb6d4a, independent export
$ bash ExecK14Corrections.sh head
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
exit=1

### intended Y tree = HEAD + the landed w1 correction blocks
###   (ScribeScorecardRound43.append.md + ScribeCorrections.scorecard.txt → SCORECARD.md;
###    ScribeCorrections.log.txt → LOG.md; three new `Correction (round 43)` lines)
$ bash ExecK14Corrections.sh y
K14 superseded=SCORECARD.md:1634 corrections=33 live=37
K14 superseded=SCORECARD.md:1691 corrections=33 live=37
K14 payload=literals=3,stale=0,superseded=2,live=corrections=37,groups=4 closed=1
exit=0

### round-41 judged head 1f74646 (zero `corrections=` literals in the three records there)
$ bash ExecK14Corrections.sh r41
K14 error=engine-unreadable path=corpus/instruments/r42-closure.sh
K14 payload=literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0
exit=1

### fail-closed probe: three records present, engine removed
$ bash ExecK14Corrections.sh fx/A0-noengine
K14 error=engine-unreadable path=corpus/instruments/r42-closure.sh
K14 payload=literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0
exit=1

### sourcing form from a foreign cwd
$ ( cd / && . <copy>/ExecK14Corrections.sh && check_k14 "$S/fx/A3a-defectevid" )
K14 payload=literals=2,stale=0,superseded=0,live=corrections=2,groups=0 closed=1
exit=0
```

Base red with the stale literal named on stderr, Y green at the exact landing shape
(`live=corrections=37,groups=4`), fail-closed on a missing engine, and one stdout line —
those are the four states the C1/K14 contract needs, and they hold.

**Landing check worth knowing (K14 alone):** the supersession must sit in `SCORECARD.md`
after line 1634 and must itself carry `corrections=33`; that occurrence is exempted only by
the self-naming rule. I measured the strict-later reading against the same Y tree with my
oracle (`STRICT_LATER=1`): `stale=1` on the marker's own quotation at `SCORECARD.md:1691`,
i.e. **without self-excuse the limb could never be green at Y**. The landed limb implements
self-excuse (lines 154-155) and is green, so this is a confirmation, not a finding.

## 4. Defects (first landed revision `9fb97b4c…`; both closed in revision `4a4945b0…`, verified in §9)

### F1 (high, escape) — `DEFECT_TOKENS` includes the lane's own role word `attack`, so a result line is silently discarded

Landed bytes, `ExecK14Corrections.sh:57` and `:135-139`:

```
57:  DEFECT_TOKENS = ("defeat", "rejected", "rejects", "attack")
135:            if "mutant=" in low or "quarantined" in low:
136:                continue
137:            if "payload=" in low:
138:                if fenced or any(t in low for t in DEFECT_TOKENS):
139:                    continue
```

The exclusion is a **whole-line substring test**. Any `payload=` line that merely mentions
`attack` — the lane's standard vocabulary (`attack share 23/73`, "attack roles") — is treated
as quoted defect evidence and drops out of the literal population entirely. Carrier bytes used
(`fx/A3c-attackword/SCORECARD.md:35`; live ledger 33 there):

```
the r43 suite at Y prints `K14 payload=literals=1,stale=0,superseded=0,live=corrections=31,groups=0 closed=1` for the 23/73 attack share
```

```
$ bash ExecK14Corrections.sh fx/A3c-attackword
K14 payload=literals=0,stale=0,superseded=0,live=corrections=33,groups=0 closed=1
exit=0
```

That is green against the frozen C1 predicate ("K14 every `corrections=<n>` literal in
SCORECARD.md/LOG.md/SHONEN.md equals the value the suite re-derives at the same export, or is
named superseded…"): the carrier's `corrections=31` is unequal to the live 33 and is not
named (`groups=0` happens to equal live groups=0, so it is not the stale one). Required
verdict: `literals=2,stale=1,closed=0`. My independent oracle on the same tree:
`K14 payload=literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0`. The limb's own
receipt (`ExecK14Corrections.md`, "Grading rules", item 3) states the rule that causes this:
"carries `payload=` together with `defeat` / `rejected` / `rejects` / `attack`".

Measured minimal fix (one line) — delete `"attack"`:

```
-DEFECT_TOKENS = ("defeat", "rejected", "rejects", "attack")
+DEFECT_TOKENS = ("defeat", "rejected", "rejects")
```

```
$ bash limb-patched.sh fx/A3c-attackword
K14 payload=literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0
K14 base: literals=2,stale=1,closed=0   Y: literals=3,stale=0,superseded=2,live=corrections=37,groups=4,closed=1
```

Base stays red and Y stays green under that patch. The residual heuristic risk is named in §7.

### F2 (medium, escape + self-contract violation) — a `live=` claim on an excluded line is not graded

The limb's header and receipt promise: "The one exception is a `live=<key>=<n>` assertion on
any line: a claimed live value is always graded against the re-derived value." The skip at `:135-139` runs **before** the
literal loop, so on any line carrying `mutant=`/`quarantined` (or `payload=`+defect word) the
`live=` claim is never read. Carrier bytes (`fx/A10-liveonevid/SCORECARD.md:4`; live 3):

```
defect evidence: mutant=`corrections=1` was rejected by the K14 mutant battery; live=corrections=99
```

```
$ bash ExecK14Corrections.sh fx/A10-liveonevid
K14 payload=literals=0,stale=0,superseded=0,live=corrections=3,groups=0 closed=1
exit=0
```

A false claim of the live value (`99` against 3) is reported as a clean tree, and the limb
contradicts its own documented rule 5. The same hole absorbs the F1 carrier: its
`live=corrections=31` was also invisible (`literals=0`).

Combined fix, measured (`limb-patch3.sh`) — replace `:135-139` with the block below
(`DEFECT_TOKENS` becomes unused and can be deleted; `payload=` is excluded only inside a
fence, so the base 1634 line stays counted and the `mutant=`/`quarantined` markers keep
their exclusion):

```
            live_claims = [(m.group(1), int(m.group(2)), m.start())
                           for m in LIT_RX.finditer(line)
                           if line[:m.start()].endswith("live=")]
            skip = ("mutant=" in low or "quarantined" in low or
                    ("payload=" in low and fenced))
            if skip:
                if not fenced:
                    for key, val, _pos in live_claims:
                        literals += 1
                        if val == live[key]:
                            continue
                        stale += 1
                        diag("stale-live=%s:%d %s=%d live=%d"
                             % (rec, lineno, key, val, live[key]))
                continue
```

Full battery under the patch (stdout, one line each; `exit` shown):

```
A1-fenced         literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0   exit=1
A2-twoperline     literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0   exit=1
A3a-defectevid    literals=2,stale=0,superseded=0,live=corrections=2,groups=0 closed=1   exit=0
A3b-payloadquote  literals=2,stale=1,superseded=0,live=corrections=3,groups=0 closed=0   exit=1
A3c-attackword    literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0  exit=1
A4a-neartoken     literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0  exit=1
A4b-live330       literals=2,stale=0,superseded=0,live=corrections=330,groups=0 closed=1  exit=0
A4c-near-excuse   literals=3,stale=1,superseded=1,live=corrections=34,groups=0 closed=0   exit=1
A5-nolivevalue    literals=2,stale=0,superseded=2,live=corrections=3,groups=0 closed=1    exit=0
A6-crossfile      literals=4,stale=1,superseded=2,live=corrections=3,groups=0 closed=0    exit=1
A7-liveassert     literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0    exit=1
A8-markbefore     literals=3,stale=1,superseded=1,live=corrections=3,groups=0 closed=0    exit=1
A9-markevid       literals=1,stale=0,superseded=1,live=corrections=3,groups=0 closed=1    exit=0
A10-liveonevid    literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0    exit=1
A11-fencedpayload literals=0,stale=0,superseded=0,live=corrections=2,groups=0 closed=1    exit=0
A12-quarantined   literals=0,stale=0,superseded=0,live=corrections=2,groups=0 closed=1    exit=0
A0-noengine       literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0    exit=1
base              literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0   exit=1
y                 literals=3,stale=0,superseded=2,live=corrections=37,groups=4 closed=1   exit=0
r41               literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0    exit=1
```

Both defects close, every one of the seventeen controls keeps its verdict, base stays red and Y
stays green. The fenced-payload transcript control (`A11`) still excludes, and its historical
`live=` quote is not graded — which is why the fix grades live claims only on **unfenced**
excluded lines.

Reproducer for F1 without my scratch tree (lane-only):

```
T=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r43)
mkdir -p "$T/corpus/instruments"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 4cb6d4a corpus/instruments/r42-closure.sh | tar -x -C "$T"
printf 'Correction (round 42): body 1.\nCorrection (round 42): body 2.\n' > "$T/SCORECARD.md"
: > "$T/LOG.md"; : > "$T/SHONEN.md"
printf 'the r43 suite at Y prints `K14 payload=literals=1,stale=0,superseded=0,live=corrections=1,groups=0 closed=1` for the 23/73 attack share\n' >> "$T/SCORECARD.md"
bash .ufo/waves/round-43/w1/ExecK14Corrections.sh "$T"        # landed: literals=0,stale=0,closed=1
```

(With live 2 and the carrier holding `corrections=1` (stale) and `groups=0` (= live 0), the
required verdict is `literals=2,stale=1,closed=0`.)

The table in §2 grades the first revision. In revision `4a4945b0…` every row still holds and
3c is red as required (§9).

## 5. Freeze-text risk (not a limb defect) — the instruction's `payload=` exclusion is unsatisfiable with its own base expectation

The seat instruction says: "Exclude literals that occur only inside quoted defect evidence: a
literal on a line whose own text also carries `payload=` or `mutant=` or `quarantined` is
evidence, never a result (R41)" — and then requires "At base ab98fac9: SCORECARD.md:1634
carries `corrections=33` while the live count is 34 -> stale=1 closed=0". The only
`corrections=` literal in the three records at base sits on that line **and that line carries
`payload=`**:

```
$ sed -n 1634p base/SCORECARD.md | cut -c1-140
Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,dups=4,exc
$ grep -c "corrections=" base/SCORECARD.md base/LOG.md base/SHONEN.md
base/SCORECARD.md:1
base/LOG.md:0
base/SHONEN.md:0
```

Measured with my independent oracle under the instruction's literal reading
(`spec-raw`: every line carrying `payload=` excluded, `Correction` status ignored):

```
$ python3 oracle_k14.py base spec-raw
K14 payload=literals=0,stale=0,superseded=0,live=corrections=34,groups=4 closed=1
exit=0
```

i.e. **the instruction as written makes K14 green at base**, which fires C1's kill rule ("a
K14-K19 check passes at base (a check that cannot see its own defect is not repaired)") and
contradicts the same instruction's `stale=1 closed=0` expectation. Three readings exist:

1. exclude every `payload=` line → base green → claim dies;
2. exclude nothing → the R41 quoted-evidence attack goes red → the seat's excluded-evidence
   case fails;
3. exclude defect evidence only (`mutant=`/`quarantined`, fenced payload transcripts) and
   count result-bearing `payload=` lines → base red **and** quoted defect evidence excluded.

The landed limb implements (3) and is the only one satisfying both requirements. The frozen
C1 predicate text ("every `corrections=<n>` literal … or is named superseded") also matches
(3) but names no exclusion at all, so a future reviewer reading only the claim can call every
exclusion an escape. **L1 action:** state the exclusion set (3) explicitly in the round
report and, if the round wants it durable, record it in the claims erratum channel; do not let
a later reviewer re-open K14 on reading 1 or on the claim's silence.

## 6. Receipt overstatement (low) and the coverage gap it papers over

`ExecK14Corrections.md`, "Blockers, risks, deviations": "The cost is that a round-43 correction
line could quote a stale value as narrative; K18/K19 grade that line's own narrative, and
`live=` claims stay graded here."

K18's scope in `claims.json` C1 is `closed=`/`selftest cases=` values quoted in round-42/43
lane records; K19 is freeze-record ordering. Neither reads `corrections=` narrative, so a
`Correction (round 43)` line quoting a stale `corrections=33` as prose is graded by **no**
check — and `live=` claims on that line are graded, but only as `live=` claims. That matters
because of attack 5: a correction that names the literal without stating the live value grades
**green** (measured above: `superseded=2, closed=1`), which is correct against the frozen C1
text but leaves nothing in the counter enforcing the "states the live value with the command
that re-derives it" duty that the correction-block spec imposes. This round's landed blocks do
state it (`ScribeCorrections.scorecard.txt` names 34/37 and the re-derivation command), so no
live gap; but the receipt's mitigation sentence should be corrected to "no check grades
`corrections=` narrative in a correction line", and the L1 should own it in the report rather
than let it disappear.

## 7. Residual risk and verification gaps

- **Heuristic exclusion remains heuristic.** Even after F1/F2, the rule decides a whole line's
  fate from substrings. A stale literal on a line that says `defeat`/`rejected`/`rejects` in a
  *result* sense (e.g. "the suite rejected 0 mutants and printed `payload=corrections=31`")
  is still invisible; conversely a defect-evidence line written as "the mutant produced
  `payload=corrections=31`" without the `mutant=` token is graded red. Both shapes are
  plausible prose. The lowering fix (marker-based exclusion only, fenced payloads exempt) was
  measured and keeps every control; the L1 decides.
- **Not tested by this seat:** the assembled `corpus/instruments/r43-closure.sh` (absent at
  HEAD — `ls corpus/instruments/r43*` ⇒ "No such file or directory"), so K14's integration
  inside the nineteen-check runner, its `--selftest` case grading, the receipt transcript, and
  the `K1-K13` carried limbs are out of my scope. My verdicts are for `check_k14` as a
  sourced limb, which is the interface the suite consumes.
- **My Y tree is assembled, not landed.** It is HEAD plus the three landed w1 correction
  blocks (`ScribeScorecardRound43.append.md`, `ScribeCorrections.scorecard.txt`,
  `ScribeCorrections.log.txt`). If the L1 lands different bytes, live and the supersede pairs
  move; `live=37` is a prediction for exactly those blocks, and the scorecard correction block
  agrees with it in its own text.
- **r41-head K14 red is infrastructural.** At `1f74646` the three records carry zero
  `corrections=` literals; the red comes from `error=engine-unreadable` (the r42 instrument did
  not exist there). That satisfies C1's "round-41 head red", but K14 contributes no
  content-borne red to that control — record it as such rather than as a literal defeat.
- **Diagnostics are stderr.** Any harness that captures `2>&1` will see two lines per red
  check; the suite must keep stdout only (`2>/dev/null | wc -l` ⇒ 1, measured).

## 8. Environment

- Scratch roots `S=/fast/scratch/hyaku/kasegi-r43/RevK14/` (first revision) and
  `S=/fast/scratch/hyaku/kasegi-r43/RevK14b/` (revision pass: exports `base`, `head`, `y`, `y36`,
  `r41`, 24 fixture trees, `limb2.sh`, `oracle_k14.py`, `mkfx.py`); both removed after the
  receipt was written (`rm -rf`, verified absent).
- Disk guard read before the pass: `scripts/hyaku/disk-guard.sh status` ⇒ `/fast/scratch/hyaku`
  25 % used, 603.8 G free; my exports and fixtures together stayed well under 100 MB.
- No git mutation anywhere: only `git -C <lane> archive`, `log`, `diff --stat`, `rev-parse`
  reads. No tool installed or upgraded; no pacman; nothing written outside this receipt and my
  scratch dir. The only lane write is this file.

## 9. Post-review verification — revision `4a4945b0…` closes F1 and F2

The executor revised the limb after §4 was filed (202 lines, `sha256
4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c`, `bash -n` clean). Source
changes verified by reading all three functions: `DEFECT_TOKENS` is deleted; `evidence_mode()`
returns `none` for a fenced `payload=` line, `live` for a line carrying `mutant=`/`quarantined`
and `all` otherwise; `is_live_claim()` scans back to whitespace/backtick/`;`/`(` and grades every
literal whose contiguous segment contains `live=` (so `live=corrections=<c>,groups=<g>` grades
both keys); self-exemption (`is_marker and not live_claim`) is unchanged. I re-ran the battery
and the trees on a byte copy of that file.

F1 closed:

```
$ bash ExecK14Corrections.sh fx/A3c-attackword      # 33 correction lines, live 33
K14 stale=SCORECARD.md:34 corrections=31 live=33
K14 payload=literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0
exit=1
```

F2 closed:

```
$ bash ExecK14Corrections.sh fx/A10-liveonevid      # live 3; mutant= line carrying live=corrections=99
K14 stale=SCORECARD.md:4 corrections=99 live=3
K14 payload=literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0
exit=1
```

Full battery on the revision (stdout + exit; stderr dropped; `2>/dev/null | wc -l` ⇒ 1 on a red
run):

```
A1-fenced            literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0      exit=1
A2-twoperline        literals=3,stale=1,superseded=0,live=corrections=2,groups=0 closed=0      exit=1
A3a-defectevid       literals=2,stale=0,superseded=0,live=corrections=2,groups=0 closed=1      exit=0
A3b-payloadquote     literals=2,stale=1,superseded=0,live=corrections=3,groups=0 closed=0      exit=1
A3c-attackword       literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0     exit=1
A4a-neartoken        literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0     exit=1
A4b-live330          literals=2,stale=0,superseded=0,live=corrections=330,groups=0 closed=1     exit=0
A4c-near-excuse      literals=3,stale=1,superseded=1,live=corrections=34,groups=0 closed=0      exit=1
A5-nolivevalue       literals=2,stale=0,superseded=2,live=corrections=3,groups=0 closed=1       exit=0
A6-crossfile         literals=4,stale=1,superseded=2,live=corrections=3,groups=0 closed=0       exit=1
A7-liveassert        literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0       exit=1
A8-markbefore        literals=3,stale=1,superseded=1,live=corrections=3,groups=0 closed=0       exit=1
A9-markevid          literals=1,stale=0,superseded=1,live=corrections=3,groups=0 closed=1       exit=0
A10-liveonevid       literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0       exit=1
A11-fencedpayload    literals=0,stale=0,superseded=0,live=corrections=2,groups=0 closed=1       exit=0
A12-quarantined      literals=0,stale=0,superseded=0,live=corrections=2,groups=0 closed=1       exit=0
A13-bothlive         literals=2,stale=2,superseded=0,live=corrections=4,groups=0 closed=0       exit=1
A14b-liveok          literals=2,stale=0,superseded=0,live=corrections=4,groups=0 closed=1       exit=0
A15-notlive          literals=1,stale=1,superseded=0,live=corrections=4,groups=0 closed=0       exit=1
A16-livespace        literals=1,stale=0,superseded=1,live=corrections=4,groups=0 closed=1       exit=0
A17-rejectedprose    literals=2,stale=1,superseded=0,live=corrections=2,groups=0 closed=0       exit=1
A18-liveword         literals=1,stale=0,superseded=1,live=corrections=4,groups=0 closed=1       exit=0
A0-noengine          literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0       exit=1
base                 literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0      exit=1
head                 literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0      exit=1
y                    literals=3,stale=0,superseded=2,live=corrections=37,groups=4 closed=1      exit=0
y36                  literals=3,stale=0,superseded=2,live=corrections=36,groups=4 closed=1      exit=0
r41                  literals=0,stale=0,superseded=0,live=corrections=0,groups=0 closed=0       exit=1
```

New probes in that battery:

- `A13` — `Correction (round 43): live=corrections=99,groups=99 is asserted.` at live 4 →
  `stale=2`: both keys of the `live=` segment are graded, as the revision documents (a marker
  line raises the live total itself, so a fixture's expected value must count its own marker).
- `A14b` — the same line with the correct `live=corrections=4,groups=0` → `stale=0, closed=1`:
  a correct live claim does not redden its own marker. (The superseded `A14-bothlive` fixture
  asserted `3` on a marker that makes the total 4; the revision's red there is correct.)
- `A15` — `notlive=corrections=99` → `stale=1`: the detector reads the whole contiguous segment,
  so a `notlive=` near-token is graded rather than exempted (the safe direction).
- `A17` — the deliberate behaviour change: `…payload=corrections=99…closed=0 is the rejected
  mutant output` (unfenced, word "rejected") → `literals=2,stale=1,closed=0`. My independent
  oracle grades it too. **Endorsed:** the word-based exemption is what produced F1, and a
  committed run quotation belongs in a fence, which stays exempt (`A11`).

Residual R1 (low, documented limitation, not a regression): the live-claim detector requires
`live=` inside the contiguous token, so two assertion forms are treated as narrative and
self-exempt on a marker line:

```
$ # A16: "Correction (round 43): live =corrections=99 is asserted."
K14 payload=literals=1,stale=0,superseded=1,live=corrections=4,groups=0 closed=1   exit=0
$ # A18: "Correction (round 43): the live corrections=99 is asserted."
K14 payload=literals=1,stale=0,superseded=1,live=corrections=4,groups=0 closed=1   exit=0
```

The revised contract says only `live=<key>=<n>` is graded, so this is behaving as documented; the
residual is that a live-value assertion written any other way is ungraded. It matters because of
the landing reconciliation below.

Landing reconciliation (medium, L1 action): the landing live total depends on which blocks land,
and K14 cannot arbitrate because the corrections state their live value as bare prose (`34`,
`37`): `grep -oE "(corrections|groups)=[0-9]+" ScribeCorrections.scorecard.txt` prints only
`corrections=33`, and a bare number is not a literal.

```
y   (ScribeScorecardRound43.append.md + ScribeCorrections.scorecard.txt + ScribeCorrections.log.txt) -> live=corrections=37, closed=1
y36 (the same minus ScribeScorecardRound43.append.md)                                               -> live=corrections=36, closed=1
```

The revision message quotes `36` for "the real scribe landing"; the scorecard correction block
asserts `37`. Both trees are green, so the counter will not arbitrate. Before the Y run the L1
must land exactly one set and make the report's live figure match it — this is the §6 gap made
concrete (the correction's stated live value is ungraded, and the "avoid the token" guidance is
what keeps it ungraded).

Agreement after the revision: the revised limb returns the required `closed=` verdict on all 23
battery fixtures and all 5 trees. The remaining differences from my independent oracle are my
oracle's own modelling gaps (it does not model `live=` claims: `A7`, `A10`, `A13`, `A14`, `A15`)
and the spec-authorised fenced-`payload=` exemption (`A11`); none is a limb defect.

### 9.1 Receipt-only follow-up (limb unchanged)

The executor folded R1 and the landing reconciliation into its receipt only; the graded bytes did
not move, re-hashed in the lane after the update:

```
ExecK14Corrections.sh           4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c  (unchanged)
ExecK14Corrections.transcript.txt 26810447af5ef6b3c6953dbbb273a1fdf0fad3834d4e93887d3e598a896c2405  (unchanged)
ExecK14Corrections.md (231 lines) 434eda9ca58b20970abf6cee9d8fe15cbfa7b1d040c3d93f2311dd4ac15c2135
```

So the §9 verification stands byte-for-byte. Two states are now recorded in the executor's
receipt and match my measurements: rule 5 names the contiguous `live=<key>=<n>` form as the only
graded live claim (R1 becomes a stated boundary, not an open residual), and the landing section
carries both `live=corrections=36,groups=4 closed=1` (the two blocks that touch graded records)
and `live=corrections=37,groups=4 closed=1` (2 SCORECARD + 1 LOG) with the non-arbitration
statement. Nothing in this follow-up changes a verdict; the L1 still owns landing exactly one
set and printing that number.
