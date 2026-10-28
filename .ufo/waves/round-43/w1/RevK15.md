# RevK15 — attack on ExecK15WaveNarrative (K15, RD42-2/RD42-3)

Seat: `RevK15` (reviewer, leaf). Lane: `kasegi-shokunin` @ base
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Frozen claims read first and never
edited: `.ufo/waves/round-43/claims.json` (C1 `depth:verifiability`). This is a
receipt-only item: no deliverable bytes beyond this file.

Reviewed artifact:
`.ufo/waves/round-43/w1/ExecK15WaveNarrative.sh`
sha256 `14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a`,
450 lines, mode 0755. The candidate in the executor's scratch changed three
times while I attacked it (`ff4a24ad…` → `b7c6d0d2…` → landed `14a195b1…`); the
prefix-handling fix landed before publication, so bullet/bold corrections are no
longer a finding. Every quote below is from the landed bytes above.

Verification base for the reviewer:
- export `base/` = `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x -C base`
  (152 MB, executed in `/fast/scratch/hyaku/kasegi-r43/RevK15`).
- 44 minimal export trees under `cases/<name>/` (LOG.md +
  corpus/lessons/round-42.md + selected `.ufo/waves/round-42/*` artifacts).
  Each fixture's artifact is the real shape
  `{"lane":"kasegi","round":42,"wave":"<name>","seats":N,"results":[…N…]}`.

Invocation (sourceable, same as the suite will use):
`bash <limb> cases/<name>`; stdout is the graded payload line, stderr is the
detail lines, rc is the closed status.

## Verdict

The limb is real: it parses the wave and round from the sentence, reds at base,
reds on empty/corrupt artifacts, catches past tense and line-wrapped sentences,
and refuses a correction placed before the claim or naming the wrong wave. It is
also not yet safe to call "seat count equals what the sentence states": five
silent-pass classes remain (F1–F5), the first directly reachable from ordinary
prose. Recommendation: repair F1–F3 before the suite is treated as
K15-closed; F4 and F5 are cheap same-file fixes.

At base the limb reds exactly the three routed sentences (the payload counts 5 qualifying sentences, 3 unbacked) and nothing else:

```
$ bash .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh base
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0   (rc=1)
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
```

That is the correct base red. What follows is what it cannot see.

## Findings, by severity

### F1 (high) — a seat-count mismatch is invisible when the count precedes the wave token

`SEATS` is only searched forward from the label (line 247,
`seats_after(lab['pos'], min(nxt, hi))`) or from the name (line 261,
`seats_after(n['pos'], hi)`). A sentence that states the count *before* the
wave says `stated=None`; `grade_claim` then treats a 35-seat artifact as
"backed" because it has no count to compare.

```
$ cat cases/seat-before-natural/LOG.md
36 seats were dispatched in wave 2 `kasegi-r42-falsify`.
$ python3 -c '<artifact round=42 wave=kasegi-r42-falsify seats=35 results=35 items>'
$ bash .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh cases/seat-before-natural
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1        (rc=0)

# same assertion, count after the name — the only difference is word order
$ cat cases/seat-after-natural/LOG.md
wave 2 `kasegi-r42-falsify` 36 seats were dispatched.
$ bash .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh cases/seat-after-natural
K15 detail=LOG.md:1 wave=kasegi-r42-falsify round=42 stated-seats=36 mismatch=seats=35 path=.ufo/waves/round-42/kasegi-r42-falsify-results.json
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=1 closed=0        (rc=1)
```

The same green appears for `36 seats in wave 2 … dispatched.` (case
`seat-before-label`, `closed=1`) and `36 seats: \`kasegi-r42-falsify\` dispatched.`
(case `seat-before-name`, `closed=1`), each against a 35-seat artifact. This is
K15's own required relation ("its seat count equals the count the sentence
states") evaded by prose order; a fabricated 36 over a 35-seat wave closes.

### F2 (high) — a correction line swallows the next plain paragraph

Lines 163–169: inside a correction block, only a blank line, a heading or a new
list item ends the block; every other line is `continue`d (skipped). The
executor's receipt says "so a following LOG entry is never swallowed" (line 46),
which holds only for list-item LOG entries; a plain paragraph is swallowed.

```
$ cat cases/swallow-mixed/LOG.md
wave 1 `kasegi-r42-build` 64 seats dispatched.
Correction (round 43): `kasegi-r42-other` never-true.
wave 2 `kasegi-r42-ghost` 36 seats dispatched.
$ bash .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh cases/swallow-mixed
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1        (rc=0)
```

The ghost dispatch (no `.ufo/waves/round-42/kasegi-r42-ghost-results.json`) is
never collected; only the backed wave-1 sentence is graded. `supersede-before`
shows the same mechanics from the other side: `Correction (round 43)` on line 1
followed by the false sentence on line 2 yields
`K15 payload=sentences=0,unbacked=0,superseded=0,mismatch=0 closed=0`
(`detail=. reason=no-qualifying-sentences`) — the false sentence disappears
instead of reding. A blank line after the correction restores the correct red /
supersession split (`correction-blank`, `superseded=1 closed=1`).

### F3 (medium-high) — evidence identity is not bound to the named wave

`read_artifact` (line 282 ff.) checks `round`, integer `seats`, list `results`
and `seats == len(results)`; it never checks the artifact's `wave` field, and the
evidence chain first tries `wave<label>-results.json` (line 315). Consequences,
each observed green:

```
# artifact at the expected path names a different wave
$ bash … cases/file-wave-mismatch     # .ufo/waves/round-42/kasegi-r42-falsify-results.json: "wave":"kasegi-r42-other"
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1

# only the label-chain file exists, and it is the build wave's
$ bash … cases/wave-label-mask        # .ufo/waves/round-42/wave2-results.json: "wave":"kasegi-r42-build", seats 36
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1

# a valid but empty run backs a dispatch claim that states no count
$ bash … cases/zero-seat              # .ufo/waves/round-42/kasegi-r42-falsify-results.json: "seats":0,"results":[]
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1
```

The label chain is a deliberate design decision for rounds 23/25 (receipt lines
53–60), but because the artifact's own `wave` is never compared, the chain also
lets a different wave's aggregate rescue a named-wave sentence, and a zero-seat
artifact rescue a count-less dispatch. A dispatch claim backed by 0 seats is
the RD42-2 defect shape one indirection away.

### F4 (medium) — a `round total` that names a wave is invisible unless it also says "dispatched" or carries a `wave N` label

`round_total` is consulted only in the label loop (line 236,
`if not (local_dispatch or round_total): continue`); the no-label loop requires
`dispatched` (line 259). The rule text covers "a `round total` for such a wave":

```
$ cat cases/round-total-named/LOG.md
The round total is 100 for `kasegi-r42-ghost`.
$ bash … cases/round-total-named
K15 detail=. reason=no-qualifying-sentences
K15 payload=sentences=0,unbacked=0,superseded=0,mismatch=0 closed=0        (rc=1)
```

The tree only reds because it has no other sentence. In a full export (any other
qualifying sentence) this false total is simply not counted. The declared blind
spot covers the *no-name* total; this one names a wave and is in scope.

### F5 (medium) — any `Correction (round N)` retires a claim, not only round 43

`CORRECTION = re.compile(r'^Correction \(round (\d+)\)')` (line 72) and
`superseded_by` never compares the captured round to 43.

```
$ bash … cases/corr-round42   # Correction (round 42): `kasegi-r42-falsify` never-true
K15 payload=sentences=1,unbacked=0,superseded=1,mismatch=0 closed=1
$ bash … cases/corr-round99   # Correction (round 99): …
K15 payload=sentences=1,unbacked=0,superseded=1,mismatch=0 closed=1
```

The spec requires a committed `Correction (round 43)` line. The other
supersession gates are sound: `corr-nokey` (no `never-true`/`not taken`) reds;
`supersede-wrongwave` reds; `supersede-before` does not supersede.

### F6 (low-medium, declared) — table rows are skipped even when they are narrative

```
$ cat cases/table-plus-backed/LOG.md
| wave | seats |
|---|---|
| `kasegi-r42-ghost` dispatched | 36 |
wave 1 `kasegi-r42-build` 64 seats dispatched.
$ bash … cases/table-plus-backed
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1
```

Declared at receipt line 172 and limb header ("quoted evidence is not
narrative"). The justification is real (`round-42-verifier-spotcheck.md:174`
quotes the false LOG sentence in a table), but this corpus also carries genuine
narrative in tables (`round-42-verifier-spotcheck.md:34` records the
"undispatched" finding there; `round-31.md:175` counts seats there), so the class
is a visibility hole even though declared.

### F7 (low) — headings and single-digit rounds are ungraded

`heading-claim` → `sentences=0`; `r9-singledigit` (`kasegi-r9-resolve`, three
mentions at base) → `sentences=0`, because `NAMED` requires `r(\d{2,3})`.
Headings are declared; the `r9` class is not.

### F8 (informational) — a cited path is never read; only the name's round is

```
# name says r41, cited path is round-42, evidence exists only under round-42
$ bash … cases/name-path-round
K15 detail=LOG.md:1 wave=kasegi-r41-falsify round=41 stated-seats=36 unbacked=no-evidence
K15 payload=sentences=1,unbacked=1,superseded=0,mismatch=0 closed=0

# same sentence, evidence under round-41; the wrong round-42 path in the sentence is ignored
$ bash … cases/path-round-green
K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1
```

This is the spec's "parse the round from the sentence itself" working as
specified, but the sentence's own path is never cross-checked: a path that
contradicts the wave name is invisible in both directions.

## The six requested attack classes, one row each

| requested class | fixture / command | limb stdout | honest? |
|---|---|---|---|
| wave name round ≠ cited path round | `cases/name-path-round` | `K15 payload=sentences=1,unbacked=1,superseded=0,mismatch=0 closed=0` | red as required (round from name), but path never read (F8) |
| same, with name-round evidence present | `cases/path-round-green` | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1` | cited wrong path invisible |
| wave name with hyphen + number (exact artifact) | `cases/hyphen-number-exact` (`kasegi-r42-falsify-2`) | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1` | correct; no truncation |
| hyphen + number, only the truncated prefix artifact | `cases/hyphen-number-trunc` (only `kasegi-r42-falsify-results.json`) | `K15 payload=sentences=1,unbacked=1,superseded=0,mismatch=0 closed=0` | correct (no truncation) |
| hyphen + number in the middle, exact | `cases/hyphen-mid-exact` (`kasegi-r42-wave2-falsify`) | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1` | correct |
| same, but only `wave2-results.json` (different wave) exists | `cases/hyphen-mid-labelmask` | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1` | **wrong** — F3 label mask |
| empty results file | `cases/empty-results` | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=1 closed=0` (detail `mismatch=corrupt`) | correct |
| corrupt results file | `cases/corrupt-results` | same as above (`mismatch=corrupt`) | correct |
| seat-count mismatch, canonical order | `cases/seat-mismatch` (36 stated, 35 seats) | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=1 closed=0` (detail `mismatch=seats=35`) | correct |
| seat-count mismatch, count before the wave | `cases/seat-before-natural` / `seat-before-label` / `seat-before-name` | `K15 payload=sentences=1,unbacked=0,superseded=0,mismatch=0 closed=1` | **wrong** — F1 |
| `seats`/`results` internally inconsistent | `cases/internal-inconsistent` (36 vs 35 results) | `mismatch=seats=36,results=35`, `closed=0` | correct |
| `round total`, no wave name | `cases/round-total-nowave` | `K15 payload=sentences=0,… closed=0`, `detail=. reason=no-qualifying-sentences` | declared out of scope (receipt limit 1); not a silent pass at tree level |
| `round total`, wave named, no label/verb | `cases/round-total-named` | `K15 payload=sentences=0,… closed=0` | **invisible in a mixed corpus** — F4 |
| past tense in a historical lesson | `cases/past-tense-with` (`was dispatched with 33 seats`) | `K15 payload=sentences=1,unbacked=1,superseded=0,mismatch=0 closed=0` | correct |
| past tense, no count | `cases/past-tense-nocount` (`the … wave was dispatched.`) | `K15 payload=sentences=1,unbacked=1,… closed=0` | correct |
| verb on the next line | `cases/wrapped` | `K15 payload=sentences=1,unbacked=1,… closed=0` | correct |

## Sentence classes the limb cannot see honestly (consolidated)

Undeclared (new in this review):
1. Count-before-wave order (`36 seats were dispatched in wave 2 …`) — F1.
2. Any plain paragraph immediately after a `Correction (round 43)` line with no
   blank/heading/list between them — F2.
3. A results artifact whose `wave` field names another wave; a label-chain
   `wave<label>-results.json` naming another wave; a valid zero-seat artifact —
   F3.
4. A `round total` tied to a named wave without "dispatched" or a `wave N` label
   — F4.
5. A correction with a round other than 43 — F5.
6. Single-digit round names (`kasegi-r9-*`) — F7.

Declared, and I confirmed the declaration is accurate:
7. `round total` with no wave name at all (receipt limit 1; tree cannot close on
   zero sentences, so it fails closed rather than open).
8. Dispatch synonyms (`sent`, `handed off`, `ran`) — only `dispatched` matches.
9. Bare `wave2` (no space/hyphen) is not a label.
10. Table rows and fenced blocks skipped — F6 (declaration accurate, but the
    "quoted evidence" rationale does not hold for this corpus; genuine narrative
    lives in tables).
11. A heading carrying a dispatch claim is skipped.

## Landing precondition for K15 at Y (measured, not inferred)

The r43 LOG entry (`w1/ScribeLogEntry.log-entry.md:127-130`) asserts
"one v2 wave `kasegi-r43-hyaku`, 73 seats dispatched" and the r43 lesson
(`w1/ScribeLessonDraft.round-43-lesson.md:12`) asserts
"wave 1 `kasegi-r43-hyaku` dispatched 73". I built the intended Y tree from the
base export + the three committed correction snippets + the scribe LOG entry +
the round-43 lesson + the round-43 wave directory:

```
$ bash … ysim                       # no .ufo/waves/round-43/kasegi-r43-hyaku-results.json
K15 detail=LOG.md:1934 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 detail=corpus/lessons/round-43.md:12 wave=kasegi-r43-hyaku round=43 stated-seats=73 mismatch=receipts=39 path=.ufo/waves/round-43/w1
K15 payload=sentences=7,unbacked=1,superseded=3,mismatch=1 closed=0      (rc=1)

$ python3 -c '<write .ufo/waves/round-43/kasegi-r43-hyaku-results.json round=43 wave=kasegi-r43-hyaku seats=73 73 results>'
$ bash … ysim
K15 payload=sentences=7,unbacked=0,superseded=3,mismatch=0 closed=1      (rc=0)
```

So the three corrections are accepted, and Y's K15 green depends on
`.ufo/waves/round-43/kasegi-r43-hyaku-results.json` with `round` 43, `wave`
`kasegi-r43-hyaku`, `seats` 73 and 73 `results` entries. The LOG sentence has
no `wave N` label, so the `w1/` receipt directory cannot back it (only `hyaku/`
or the results artifact can); the lesson's labeled claim can fall back to
`w1/`, but only if that directory contains exactly 73 `.md` files. The executor's
receipt names the same artifact in its "Integration precondition" section
(lines 154-157); this receipt records that the suite run at Y fails without it — treat the artifact as a landing precondition,
not an optional nicety.

## Residual risk and verification gaps

- The true Y does not exist yet. `ysim` uses the uncommitted scribe drafts and a
  snapshot of `.ufo/waves/round-43/` taken at 13:52Z (39 `.md` in `w1/` at copy
  time; live count 56), not committed bytes.
- I exercised the K15 limb only, not the assembled `r43-closure.sh` suite (not
  yet landed at review time), so I make no claim about K15's integration line
  number, its selftest case, or the suite's 19/19.
- Fixture trees are minimal exports (LOG.md + one lesson + targeted artifacts).
  The only full-tree runs are `base` and `ysim`.
- Findings F1–F5 are demonstrated with synthetic sentences that mirror the
  corpus grammar (`wave N`, backticked named wave, `N seats`, `dispatched`).
  They do not depend on any uncommitted lane byte.
- No finding here asserts a defect in the committed r42/r43 narrative contents;
  the r42 base reds are the intended ones.

## Hygiene

- Writes: this receipt and scratch under
  `/fast/scratch/hyaku/kasegi-r43/RevK15/` only. Scratch (including `base/`,
  `ysim/`, `cases/`, matrix logs) removed before yield.
- Git: read-only `archive` only; no add/commit/checkout/reset/stash/branch/tag/
  worktree anywhere, no fixture repo created.
- Tooling: nothing installed or upgraded (no pacman, no `uv`, no `npx`, no
  binary); no network fetch (no `curl`), so no HTTP status/byte/UTC record to
  report.
- No subagent spawn; no `agent://all` message.
- The receipt is the only delivered file, so it cannot carry its own sha256;
  the reviewed artifact's sha256 and line count are recorded above.
