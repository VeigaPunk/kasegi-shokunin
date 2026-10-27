# ExecI4Fence — round-41, wave 1 — I4 fence-awareness limb

Seat: `ExecI4Fence` (executor). Lane: `kasegi-shokunin`.
Scope: build the I4 fence-awareness limb for the round-41 closure suite
(`corpus/instruments/r41-closure.sh`, check I4), prove it on a scratch fixture,
and hand the bytes to the L1.

## Deliverables

| file | lines | sha256 |
| --- | --- | --- |
| `.ufo/waves/round-41/wave1/ExecI4Fence.sh` | 332 | `ca1f4f372f8129b4a90036f6a1b2f9fc599c8559d455fcf9bc024b20a0132235` |
| `.ufo/waves/round-41/wave1/ExecI4Fence.transcript.txt` | 242 | `f64ac9cac52fd0291f645378aa5ddb5a75214d91e1a1c70e3c534e1a2bb10b14` |

`ExecI4Fence.sh` contains only the landable source of the limb (no validation
tables, no notes). This receipt holds the design and the evidence.

## Design

### What I4 needs and what the round-40 limb got wrong

Frozen check I4 (claims.json): *"fence awareness (fenced correction/criterion
lines do not satisfy line-anchored limbs; fence state CLOSED at EOF — T3/T4)"*.

The round-40 scanner (`corpus/instruments/r40-closure.sh`, `h2_scan`, lines
581–621) opens a fence on any line matching `/^ {0,3}```/` but closes it only on
`/^ {0,3}```[ \t]*$/` — **three backticks exactly**. A CommonMark four-backtick
fence therefore never closes. That is the wave-2 defeat fixture T3:

```
== T3 H2 4-backtick fence: correction inside a CommonMark 4-backtick fence
rc=1 payload=corrections=3,named=3,missing=1,fences=open
```

`fences=open` on a well-formed file: the round-40 scanner had no way to express
"this fence closed correctly". The r40 scanner also had no notion of fence
*length*, so it could not tell a ```` fence from a ``` fence, and no notion of
marker identity, so a tilde fence and a backtick fence were the same state.

### The state machine

The limb implements the CommonMark 0.30 §4.5 fenced-code-block rules:

- **Opener** — up to 3 leading spaces, then a run of ≥3 identical `` ` `` or `~`.
  For a backtick fence the info string may not contain a backtick; a tilde
  fence's info string may contain anything.
- **Closer** — up to 3 leading spaces, a run of the **same** marker character
  **at least as long as the opener's run**, and nothing but spaces/tabs after.
- **Different marker never closes.** A ``` inside a ```` fence is content; a
  ```` inside a ``` fence *does* close it (length ≥ opener).
- **Delimiter lines are inside.** The opening and the closing fence lines are
  reported INSIDE, so they are excluded from the outside set. This is
  deliberate and adversarial-facing: an attacker who writes the correction text
  onto the fence delimiter line must not satisfy a line-anchored limb.
- **Unclosed fence runs to EOF.** Remaining lines are INSIDE and the EOF state
  is `OPEN` — fail-closed, never silently "closed".

The scanner is a single awk pass (`FENCE_AWK_PROG`) over the file; every public
function is a pure function of the file bytes. No global state is written.

### Public API

| function | returns |
| --- | --- |
| `fence_scan FILE` | `<lineno>\t<OUTSIDE\|INSIDE>\t<CLOSED\|OPEN>` per line |
| `fence_report FILE` | human-readable per-line report + summary |
| `fence_outside_lines FILE` | outside line numbers, ascending, one per line |
| `fence_outside_set FILE` | the outside set on one line, space separated |
| `fence_outside_count FILE` | number of lines outside fences |
| `fence_outside_match FILE ERE` | `count=N lines=a b c` over outside lines matching ERE |
| `fence_eof_state FILE` | `CLOSED` \| `OPEN` |
| `fence_line_state FILE N` | `OUTSIDE` \| `INSIDE` for line N |
| `fence_audit FILE` | `outside=N inside=M eof=CLOSED` |
| `fence_payload FILE ERE` | `matches=N,fences=closed\|open` |
| `fence_selftest` | 7 graded cases; rc 0 only if all pass |

Sourcing defines functions and runs nothing (no `set -e`, no `set -u` side
effects on the caller). A standalone CLI (`--selftest`, `--report`, `--outside`,
`--eof`) sits behind the same `BASH_SOURCE` guard the round-40 suite uses.

The ERE argument is matched against the whole line; callers anchor it
themselves, e.g. `^Correction [(]round 41[)]` — bracket form, not escaped
parens, so the pattern survives both shell and awk quoting.

### Recommended I4 wiring (sent to `ExecSuiteCore`)

Count `fence_outside_match FILE '^Correction [(]round 41[)]'` over the four
records; require the count to be exactly 3 and `fence_eof_state` to be `CLOSED`
for each. The T3-style shape (one correction of four fenced) then yields
count=3 with eof=CLOSED — where the round-40 scanner said `fences=open`.

## Evidence — the four required proofs

Full transcript: `.ufo/waves/round-41/wave1/ExecI4Fence.transcript.txt`.
Fixtures were built in scratch under
`/fast/scratch/hyaku/kasegi-r41/ExecI4Fence/fx/` and removed before yield.

### (a) a `Correction (round 41)` line inside a 4-backtick fence is reported outside-set=empty

Fixture `a-fourbacktick-correction.md`:

`````markdown
# Round 41 ledger

````markdown
Correction (round 41): C1 is NOT verified on the frozen counter; the round-40
suite ran green (closed=10/10 exit=0) while its kill rule fired.
````

End of ledger.
`````

```
$ fence_report fx/a-fourbacktick-correction.md
fence-report file=fx/a-fourbacktick-correction.md
1	OUTSIDE	fence=CLOSED
2	OUTSIDE	fence=CLOSED
3	INSIDE	fence=OPEN
4	INSIDE	fence=OPEN
5	INSIDE	fence=OPEN
6	INSIDE	fence=CLOSED
7	OUTSIDE	fence=CLOSED
8	OUTSIDE	fence=CLOSED
outside=4 inside=4 eof=CLOSED
$ fence_outside_match fx/a-fourbacktick-correction.md '^Correction [(]round 41[)]'
count=0 lines=
$ fence_outside_set fx/a-fourbacktick-correction.md
1 2 7 8
$ fence_line_state fx/a-fourbacktick-correction.md 4   # the correction line
INSIDE
$ fence_eof_state fx/a-fourbacktick-correction.md
CLOSED
```

The correction line (4) is INSIDE; the outside set is `1 2 7 8` and contains no
correction line — `count=0`. The four-backtick fence opened at line 3 and closed
at line 6, so EOF state is `CLOSED`.

### (b) the T3-style case (one correction of four fenced) counts 3

Fixture `b-t3-style.md` — four correction lines, exactly one inside a
4-backtick fence:

```
$ fence_outside_match fx/b-t3-style.md '^Correction [(]round 41[)]'
count=3 lines=1 2 6
$ fence_outside_lines fx/b-t3-style.md
1
2
6
$ fence_report fx/b-t3-style.md
1	OUTSIDE	fence=CLOSED
2	OUTSIDE	fence=CLOSED
3	INSIDE	fence=OPEN
4	INSIDE	fence=OPEN
5	INSIDE	fence=CLOSED
6	OUTSIDE	fence=CLOSED
outside=3 inside=3 eof=CLOSED
$ fence_eof_state fx/b-t3-style.md
CLOSED
```

`count=3` — the fenced correction (line 4) is excluded. This is the T3 shape
the round-40 scanner mis-reported: same fixture, `h2_scan` gives `0 0 open`.

### (c) a fenced pseudo-table row containing `M39-2` is fenced

Fixture `c-fenced-pseudorow.md` (the round-40 T4 shape):

```
$ fence_outside_match fx/c-fenced-pseudorow.md 'M39-2'
count=0 lines=
$ fence_report fx/c-fenced-pseudorow.md
1	OUTSIDE	fence=CLOSED
2	OUTSIDE	fence=CLOSED
3	OUTSIDE	fence=CLOSED
4	OUTSIDE	fence=CLOSED
5	INSIDE	fence=OPEN
6	INSIDE	fence=OPEN
7	INSIDE	fence=CLOSED
8	OUTSIDE	fence=CLOSED
9	OUTSIDE	fence=CLOSED
outside=6 inside=3 eof=CLOSED
$ fence_line_state fx/c-fenced-pseudorow.md 5   # the M39-2 row
INSIDE
$ fence_eof_state fx/c-fenced-pseudorow.md
CLOSED
```

The pseudo-row `| M39-2 | pseudo row inside a fence |` is line 5, INSIDE, and
`M39-2` matches 0 outside lines.

### (d) fence state at EOF is CLOSED for a well-formed file

Fixture `d-wellformed.md` (3-backtick, 3-tilde and mixed fences, all closed):

```
$ fence_eof_state fx/d-wellformed.md
CLOSED
$ fence_audit fx/d-wellformed.md
outside=8 inside=10 eof=CLOSED
```

### Extras

- **Mixed markers and lengths** (`e-mixed.md`): a 4-backtick fence containing
  ``` lines, a 4-tilde fence containing ``` lines, and a tilde fence — all
  classified correctly, `eof=CLOSED`.
- **Unclosed fence** (`f-unclosed.md`): `fence_eof_state` → `OPEN` (fail-closed).
- **Round-40 baseline** on the same fixtures — `h2_scan` gives `0 0 open` for
  the well-formed `a-fourbacktick-correction.md` and for `b-t3-style.md`,
  i.e. the round-40 scanner cannot close a 4-backtick fence at all.

### Limb self-test (graded, 7 cases, rc 0)

```
$ fence_selftest
selftest case=A payload=outside=0,fences=CLOSED verdict=pass
selftest case=B payload=outside=3,fences=CLOSED verdict=pass
selftest case=C payload=outside=0,fences=CLOSED verdict=pass
selftest case=D payload=outside=1,fences=CLOSED verdict=pass
selftest case=E payload=outside=0/0,fences=CLOSED verdict=pass
selftest case=F payload=fences=OPEN verdict=pass
selftest case=G payload=outside=0,fences=CLOSED verdict=pass
selftest rc=0
```

A = 4-backtick correction is fenced · B = T3 shape counts 3 · C = fenced
`M39-2` row · D = well-formed file CLOSED at EOF · E = tilde fence honoured and
a different marker does not close a fence · F = unclosed fence reports OPEN ·
G = a shorter run of the same marker does not close a longer fence.

### Cross-check against a reference implementation

The INSIDE set was compared, line for line, against the CommonMark reference
parser (python `commonmark` 0.9.2) on 27 fixtures covering 3- and 4-backtick
fences, tilde fences, mixed markers, differing fence lengths, info strings
containing a backtick, closers with trailing text, unclosed fences, fences at
EOF, and indented fences:

```
$ uv run --with commonmark python diff_commonmark.py
plain                      OK  ref=- limb=-
three-backtick             OK  ref=[2, 3, 4, 5] limb=[2, 3, 4, 5]
three-backtick-info        OK  ref=[2, 3, 4] limb=[2, 3, 4]
four-backtick              OK  ref=[2, 3, 4, 5, 6] limb=[2, 3, 4, 5, 6]
four-backtick-nested-close OK  ref=[2, 3, 4, 5] limb=[2, 3, 4, 5]
tilde                      OK  ref=[2, 3, 4] limb=[2, 3, 4]
tilde-four                 OK  ref=[2, 3, 4, 5, 6] limb=[2, 3, 4, 5, 6]
tilde-inside-backtick      OK  ref=[2, 3, 4, 5, 6] limb=[2, 3, 4, 5, 6]
backtick-inside-tilde      OK  ref=[2, 3, 4, 5, 6] limb=[2, 3, 4, 5, 6]
unclosed                   OK  ref=[2, 3] limb=[2, 3]
unclosed-tilde             OK  ref=[2, 3] limb=[2, 3]
indented-3                 OK  ref=[2, 3, 4] limb=[2, 3, 4]
indented-4                 OK  ref=- limb=-
info-with-backtick         OK  ref=[4, 5] limb=[4, 5]
info-with-tilde-backtick   OK  ref=[2, 3, 4] limb=[2, 3, 4]
closer-with-trailing       OK  ref=[2, 3, 4] limb=[2, 3, 4]
closer-with-text           OK  ref=[2, 3, 4, 5] limb=[2, 3, 4, 5]
empty-fence                OK  ref=[2, 3] limb=[2, 3]
fence-after-paragraph      OK  ref=[3, 4, 5] limb=[3, 4, 5]
two-fences                 OK  ref=[1, 2, 3, 5, 6, 7] limb=[1, 2, 3, 5, 6, 7]
longer-closer              OK  ref=[2, 3, 4] limb=[2, 3, 4]
shorter-closer             OK  ref=[2, 3, 4, 5, 6] limb=[2, 3, 4, 5, 6]
tilde-longer-closer        OK  ref=[2, 3, 4] limb=[2, 3, 4]
blank-lines-inside         OK  ref=[1, 2, 3, 4, 5, 6] limb=[1, 2, 3, 4, 5, 6]
fence-at-eof               OK  ref=[2, 3, 4] limb=[2, 3, 4]
fence-at-eof-no-close      OK  ref=[2, 3] limb=[2, 3]
backtick-run-5             OK  ref=[2, 3, 4, 5] limb=[2, 3, 4, 5]
differential cases=27 diffs=0
differential rc=0
```

The reference parser's HTML output was used to confirm the ambiguous
`closer-with-text` case: both the reference parser and the limb treat
` ``` not a closer ` as content, not as a closer (the block runs to line 5).
The reference implementation was also checked against the `cmark` C binary from
the same package for that case, with identical HTML output.

### The limb applied to this receipt (self-application)

The limb was run against this very receipt after it was written, and it found a
real CommonMark error in it: proof (a) quoted the fixture — which contains a
four-backtick fence — inside a four-backtick display fence. Per CommonMark the
inner ` ```` ` closes the outer fence, so the outer fence re-opened and the
following three-backtick block could not close it, leaving the fence state
`OPEN` at EOF. The display fence was widened to five backticks, which is the
correct way to show a four-backtick fence inside another fence.

After the fix, run from the landed path:

```
$ bash -c '. ExecI4Fence.sh; fence_audit ExecI4Fence.md'
outside=253 inside=145 eof=CLOSED
$ fence_scan ExecI4Fence.md | awk -F'\t' '$2=="INSIDE" && $3=="CLOSED"'
33	INSIDE	CLOSED
111	INSIDE	CLOSED
133	INSIDE	CLOSED
161	INSIDE	CLOSED
188	INSIDE	CLOSED
202	INSIDE	CLOSED
226	INSIDE	CLOSED
272	INSIDE	CLOSED
306	INSIDE	CLOSED
325	INSIDE	CLOSED
```

Ten fences, ten closers, EOF `CLOSED`. The limb caught a real defect in its
own author's document — which is the strongest available evidence that it is
not a rubber stamp.

### Behaviour on the real lane corpus

The limb was run over the lane's own files (read-only) to confirm it neither
crashes nor mis-reports a well-formed document:

```
SCORECARD.md           lines=1600   audit=outside=1547 inside=53 eof=CLOSED corr41=count=0 lines=
LOG.md                 lines=1734   audit=outside=1734 inside=0  eof=CLOSED corr41=count=0 lines=
SHONEN.md              lines=219    audit=outside=219  inside=0  eof=CLOSED corr41=count=0 lines=
PROVINCE.md            lines=161    audit=outside=117  inside=44 eof=CLOSED corr41=count=0 lines=
SKILL.md               lines=1122   audit=outside=1104 inside=18 eof=CLOSED corr41=count=0 lines=
corpus/README.md       lines=543    audit=outside=513  inside=30 eof=CLOSED corr41=count=0 lines=
corpus/SOURCES.md      lines=135    audit=outside=135  inside=0  eof=CLOSED corr41=count=0 lines=
```

`corr41=count=0` is expected and correct: the `Correction (round 41)` blocks do
not exist in the lane yet — the sibling seats `ExecI1Blocks` / `ScribeCorrections`
own those bytes. When they land, this limb is the one that decides whether each
correction line is fenced.

### Robustness

- Runs clean under `set -uo pipefail` (the lane's suite setting): verified.
- Missing file → `fence_scan`/`fence_eof_state` return rc 1, no output, no crash.
- `fence_selftest` writes its fixtures under `$TMPDIR` and removes them on exit;
  verified no leftover directory.
- Pure POSIX-ish awk (`ENVIRON`, `substr`, `index`, `length`, POSIX character
  classes only) — no GNU-awk-only constructs.

## Limits (documented in the deliverable header too)

- Only **fenced** code blocks are modelled. Indented (4-space) code blocks,
  HTML blocks and setext headings are not fence state and are reported OUTSIDE.
- Indentation is counted in spaces only; a leading tab is treated as
  non-fence indentation.
- The `fence_outside_match` ERE is matched against the whole line; the caller
  anchors it.

## Tooling

- **Reference implementation used for the cross-check**: `commonmark` 0.9.2
  (official PyPI), the CommonMark 0.29 reference implementation. Reason: the
  I4 limb's fence state machine needed an independent oracle, so the INSIDE set
  is compared line-for-line against the reference parser rather than against
  my own expectations.
- **Install channel**: `uv run --with commonmark` (ephemeral environment,
  uv cache only). I first ran `uv tool install commonmark`, which wrote a
  `cmark` symlink into `~/.local/bin` — a PATH directory the seat host guard
  forbids writing to — so I removed it with `uv tool uninstall commonmark`
  immediately afterwards. `~/.local/bin/cmark` no longer exists and
  `~/.local/bin` is back to its prior state. The delivered cross-check
  reproduces without any PATH-directory install, because `uv run --with`
  builds an ephemeral environment and touches no PATH directory.
- **Reproduction**: the whole transcript reproduces byte-identically from the
  delivered limb and the scratch fixtures, modulo only the transcript's own
  `utc=` line. Verified by re-running the driver after the uninstall:
  `diff` of the two transcripts reports exactly one differing line, the
  timestamp.
- No pacman transaction was run (pacman is paused host-wide). No host service
  was restarted. No fleet-root tracked file was written.
- **Network fetch** (the one fetch performed for this seat):
  `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://pypi.org/pypi/commonmark/json`
  → `http_status=200`, `bytes=38477`, `utc_fetch=2026-10-27T08:26:45Z`.
  The package itself was then resolved by uv from the same PyPI index.

## Notes for the L1

- The limb is a **sourceable** file; the suite can either `.`-source it or
  inline the awk program. If it is inlined into `corpus/instruments/r41-closure.sh`,
  the function names `fence_*` are free of collision with the round-40 suite's
  `h1_*`–`h10_*` / `h2_scan` names.
- `ExecSuiteCore` was messaged the API and the recommended I4 wiring.
- The limb does **not** decide how many corrections are required (that is the
  suite's frozen predicate); it only decides, per line, whether the line is
  fenced, and reports the fence state at EOF. The I4 fixture the suite must
  red on is the T3 shape (four corrections, one fenced, eof CLOSED) — the
  limb gives count=3 there, which is the number the frozen predicate wants.

## Scope and hygiene

- Wrote only: this receipt, `.ufo/waves/round-41/wave1/ExecI4Fence.sh`,
  `.ufo/waves/round-41/wave1/ExecI4Fence.transcript.txt`, and scratch under
  `/fast/scratch/hyaku/kasegi-r41/ExecI4Fence/`.
- No lane file, fleet-root file, `SKILL.md`, `SCORECARD.md`, `LOG.md`,
  `SHONEN.md`, `PROVINCE.md`, `corpus/` file, or source tree was modified.
- No mutating git or jj command was run anywhere.
- Scratch directory removed before yield (verified absent).
