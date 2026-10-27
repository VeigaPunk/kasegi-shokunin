# ExecI3Token — I3 token-boundary value-matching limb (kasegi round 41, wave 1)

Seat: `ExecI3Token` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base commit `5b29ea1439450b712581edf5f0bf98dfb262ab`; claims-freeze `fbba3d96cdf8d37c1ea41304a1ba35691329684b`.
Frozen claims read from `.ufo/waves/round-41/claims.json` (not edited).

## Deliverables (byte-exact, written into the wave dir)

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-41/wave1/ExecI3Token.sh` | 293 | `9ea0adba6b11485eac794a04e54622e9f6a835ef4d17c73af3640523f72dcb4a` |
| `.ufo/waves/round-41/wave1/ExecI3Token.transcript.txt` | 135 | `ed460111efc4160e5da786aba8f3f830dc44e8065dea9b4b5d0fb7b96834b4b4` |

Both files are copies of the scratch originals; `cmp` reports them byte-identical
(`cmp` → "sh identical" / "transcript identical"). No other lane file was written;
`git status --porcelain` shows only my two wave-1 deliverables among my writes.

## What the limb is

`ExecI3Token.sh` is a **sourceable bash limb** (the round-40 suite's own
`if [ "${BASH_SOURCE[0]}" = "$0" ]` guard convention) exporting three functions:

- `i3_token_match FILE ROUND VALUE...` — the value limb. Reads `FILE`, considers
  **only** lines whose text begins in column 1 with `Correction (round ROUND)`
  (the closing parenthesis is part of the anchor), and requires each `VALUE` to
  appear in one of those lines **as a token**: the character immediately before
  and immediately after the occurrence must each be whitespace, punctuation, or
  the edge of the line. Letters and digits are word characters and never
  boundaries. Exit `0` green, `1` red, `2` fail-closed (file absent/unreadable),
  `64` usage error. Prints one payload line, house style
  (`corrections=…,named=…,missing=…,missing-values=…,values=…,mode=…`), i.e. the
  same `k=v,…` shape the round-40 suite's `H<n> payload=` lines use, so the
  I3 check can print `I3 payload=<this> closed=0|1` without a second format.
- `i3_token_match_same_line FILE ROUND VALUE...` — the same match, stricter:
  **one** considered line must carry every value (`named>=1`), not one value per
  line. This is the reading I1 wants ("the correction line names the values");
  the default `any` mode is the reading I3 wants ("the value appears").
- `i3_correction_lines FILE ROUND` — prints the considered lines, so a
  neighbouring limb (I1, or I4's fence scanner) can compose with the same
  line-anchor selection without re-deriving it.

**The value list is an argument, not a constant** — `i3_token_match "$f" 41 'closed=8/8' 'failures=0'`
— so I1 and I3 share one implementation, as the item requires. A CLI
(`--file/--round/--value/--same-line`, plus `--selftest`) exists for
transcript reproduction; it is inert when the file is sourced (proven in
transcript §13).

### Why the boundary is `[[:space:][:punct:]]` and not awk field equality

The round-40 records quote their values **in backticks** — e.g.
`` `closed=7/8 exit=1` `` — so a bare whitespace-field comparison against the
field `closed=7/8` would reject the honest record. The punctuation-bounded
form accepts the backtick as a boundary character and still rejects the
digit-extension defeat. This is the option the item offered ("PCRE
`[[:space:][:punct:]]`-bounded or awk field equality — your choice").

One judgement call, stated so the L1 can overrule it: POSIX `[[:punct:]]`
includes `_`, so by default `x_closed=7/8` **does** satisfy the value
`closed=7/8` (the `_` is a boundary). A documented environment knob
`I3_STRICT_UNDERSCORE=1` removes `_` from the boundary set so it does not.
Both behaviours are proven in transcript §12b. The default follows the spec's
literal boundary class; the strict knob is available if I1/I3 want
word-joining to block.

## Design notes

1. **Line anchor is a prefix of the whole line, not a substring search.**
   The round-40 `h2_scan` used `index(s, "Correction (round 40)") == 1`, which
   is prefix-only but did not verify the round boundary; `Correction (round 410)`
   would have satisfied a round-41 query. My regex is
   `^Correction \(round <N>\)` with the closing parenthesis inside the anchor,
   so a wrong round cannot leak in. Indented copies are excluded by the `^`
   (transcript §9: an indented copy and a `Correction (round 410)` line both
   leave `corrections=0`).
2. **Matching is a scan, not a single `index()`.** `hasval()` walks every
   occurrence of the value in the line and accepts the first occurrence whose
   left and right neighbours are both boundaries. A line carrying *both* the
   defeat token and the honest token therefore still matches the honest value
   (transcript §3) — the limb never lets a wrong value poison a right one and
   never lets a right value be masked by a wrong one.
3. **Values travel to awk through the environment**, not `-v`: `awk -v` would
   interpret backslash escapes inside a value. The separator is `\037`
   (US, unit separator), which cannot occur in a shell argument in practice;
   a value containing it is rejected with `error=bad-value` rather than
   silently mangled.
4. **One awk program, two modes.** `_i3_scan` takes the mode as a variable, so
   `any` and `same-line` cannot drift apart. The `I3_STRICT_UNDERSCORE` knob is
   read once in `BEGIN`, so it applies uniformly to every value.
5. **Fail closed.** A missing or unreadable file is `error=file-absent`, exit
   `2` — never a silent green. A non-numeric round is `error=bad-round`,
   exit `64`. An empty value list is `error=no-values`, exit `64`.
6. **No writes.** The limb only reads the file it is given; it writes nothing
   to the lane, the export root or the scratch. The `--selftest` mode creates
   its fixtures under `$TMPDIR` (default `/tmp`) and removes them before
   returning.

## Proof — both ways (full transcript in `ExecI3Token.transcript.txt`)

The scratch fixture file carries **both** required lines, byte-exactly as the
transcript shows:

```
--- fixture-defeat.md
Correction (round 40): the final round-39 receipt records `closed=7/80 and failures=10`.
--- fixture-honest.md
Correction (round 40): the final round-39 receipt records `closed=7/8 exit=1` and `selftest failures=1`.
--- fixture-both.md
Correction (round 40): the final round-39 receipt records `closed=7/80 and failures=10`.
Correction (round 40): the graded selftest records `closed=7/8 exit=1` and `selftest failures=1`.
```

**Honest → green** (transcript §1):

```
$ bash ExecI3Token.sh --file .../fixture-honest.md --round 40 --value closed=7/8 --value failures=1
corrections=1,named=1,missing=0,missing-values=-,values=2,mode=any
rc=0
```

**Round-40 T2 defeat → red** (transcript §2), the exact defeat line from
`.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` (`== T2 H2 substring
defeat: closed=7/80 and failures=10 (wrong values)`):

```
$ bash ExecI3Token.sh --file .../fixture-defeat.md --round 40 --value closed=7/8 --value failures=1
corrections=1,named=0,missing=2,missing-values=closed=7/8,failures=1,values=2,mode=any
rc=1
```

The contrast is explicit in transcript §4: the **round-40 matcher on the same
defeat file** is green on the lie —

```
$ grep -cF "closed=7/8" fixture-defeat.md
1
$ grep -cF "failures=1" fixture-defeat.md
1
```

— which is the round-40 wave-2 T2 finding (`RevC1Counters.md` D1: *"H2 accepts
wrong receipt values by substring match"*). Transcript §5 confirms the limb is
not simply always-red: the same defeat file queried with the **defeat** values
`closed=7/80`/`failures=10` matches exactly (`missing=0`, rc=0). §6 does the
same per value.

**Against the real lane records** (transcript §7/§8), the limb reads the
committed round-40 correction lines in all three records:

- `SCORECARD.md`, `LOG.md`, `SHONEN.md` with `closed=7/8` + `failures=1` →
  `missing=0`, rc=0 in each (the honest correction lines really do carry the
  values as tokens);
- the same three with `closed=7/80` + `failures=10` → `missing=2`, rc=1 in each.

**Selftest** (transcript §11) grades six cases, all `verdict=pass`: `honest`,
`defeat`, `unanchored` (values present but not on a `Correction (round N)`
line → red), `mixed` (both lines → green), `split-any` (values on two
different correction lines → green in `any` mode), `split-same-line` (the same
file → red in `same-line` mode).

**Other edges proven** (transcript §9/§12/§12b/§13): the line anchor rejects an
indented copy and a wrong-round line; a missing file fails closed with exit 2;
the underscore knob flips `x_closed=7/8` from green to red; sourcing the file
defines the three functions and executes no CLI.

**Integration smoke** (scratch, not a deliverable): sourced under
`set -uo pipefail` in a caller that captures `payload=$(i3_token_match …)` and
`rc=$?`, the limb prints its payload and returns 0/1 as expected, and
`i3_correction_lines` returns the two anchored `SCORECARD.md` lines. A caller
that wants the I1 reading uses `i3_token_match_same_line`; a caller that wants
the I3 reading uses `i3_token_match`. Both take the same value list, so
I1 and I3 share one implementation as specified.

## How this lands into the r41 suite (for `ExecSuiteCore` / the L1)

The suite can source this limb and call

```bash
i3_token_match "$tree/SCORECARD.md" 41 'closed=8/8' 'failures=0'
```

per record file, or call `i3_correction_lines` once per file to obtain the
candidate lines for the fence-aware check (I4) and the evidence-naming check
(I1). The payload line is already in the `k=v,…` house shape, so
`I3 payload=<payload> closed=<0|1>` needs no reformatting.

Two integration points the L1 should decide:

1. **Which mode is "I3".** The frozen predicate for I3 says the substring
   defeat fixtures `closed=7/80` and `failures=10` are rejected; both modes
   reject them. `any` is the default; `same-line` is available for I1.
2. **`I3_STRICT_UNDERSCORE`.** Off by default (POSIX `[[:punct:]]` includes
   `_`). Turn it on if the round-41 correction lines must not be satisfied by
   an underscore-joined variant.

## Risks, limits, and what this seat did NOT do

- **This limb is one clause of I3, not the whole check.** It does not verify
  that the correction lines *grade* round-40 C1 as not verified, nor that they
  *name the firing evidence* — that is I1's clause. The limb only proves the
  values appear as tokens on the anchored lines.
- **Fence awareness is not here.** A `Correction (round N)` line inside a
  CommonMark fence still satisfies this limb. The claims assign fence
  awareness to I4 (a separate seat, `ExecI4Fence`); this limb is the
  token-boundary half only. If I4's implementation filters fenced lines
  before the value match, the two compose; if I4 instead expects to receive
  pre-filtered candidate lines, `i3_correction_lines` is the seam.
- **The transcript's file paths are scratch paths** that no longer exist after
  this seat cleans up; the fixture bytes are reproduced verbatim in §0 of the
  transcript, so any reader can recreate them and re-run the commands.
- **No LSP tooling was used** — the item is a self-contained shell script with
  no host-language symbol graph; the round-40 suite's shell style was read
  directly instead (`corpus/instruments/r40-closure.sh`, 1734 lines, whose
  `h2_scan` is the defect this limb replaces).
- **No tool was installed** for this seat (the task needed only `bash`, `awk`
  (GNU Awk 5.4.1, pre-installed) and coreutils), so the operator's
  tooling-authorisation clause produced no installs to record.
- **Scratch hygiene**: all work ran under
  `/fast/scratch/hyaku/kasegi-r41/ExecI3Token/`; the driver removed its own
  `$WORK` subtree, and the seat's scratch directory is removed before the
  yield (verified after cleanup). `TMPDIR` was pinned to the scratch dir for
  the selftest; `/tmp` was used only by `mktemp` under the scratch `TMPDIR`.

## Commands actually run (with output)

Every command in the transcript was executed with its actual output; the
transcript is the raw log. The headline runs:

```
$ sha256sum ExecI3Token.sh
9ea0adba6b11485eac794a04e54622e9f6a835ef4d17c73af3640523f72dcb4a
$ wc -l ExecI3Token.sh
293 ExecI3Token.sh
$ bash -n ExecI3Token.sh            # syntax OK
$ bash ExecI3Token.sh --selftest    # 6/6 verdict=pass, rc=0
```

Disk guard was green before the work (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`:
`/fast/scratch/hyaku` 25% used, 610.2G free).
