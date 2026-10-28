# ExecK15WaveNarrative — round 43, K15: wave-dispatch narrative vs results evidence

Seat: ExecK15WaveNarrative (leaf executor). Lane: `kasegi-shokunin` only. Base:
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Frozen claims read first
(`.ufo/waves/round-43/claims.json`, unedited): C1 K15 is "every sentence in LOG.md or
corpus/lessons asserting that a named `kasegi-rNN-*` wave was dispatched has
`.ufo/waves/round-NN/<wave>-results.json`, or is named never-true by a `Correction (round 43)`
line". Milestone: C1 K14-K19 narrative-evidence checks, attack share 23/73.

## Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecK15WaveNarrative.sh` | 450 | 17944 | `14a195b1eb7ec61550bf4938f62ae7856dbae0c1a49dc7aba078f7b97304e93a` |
| `.ufo/waves/round-43/w1/ExecK15WaveNarrative.transcript.txt` | 292 | 19259 | `b14ddcdfcc15fe103182bde6a7f5e093ae2daf1c1e6f47df7bd2f4704bf3b443` |

`ExecK15WaveNarrative.sh` is the landable limb: `source` it and call `check_k15 <export>`, or run
it as `bash ExecK15WaveNarrative.sh <export>`. It is read-only over the export and prints exactly
one stdout line `K15 payload=sentences=<n>,unbacked=<k>,superseded=<s>,mismatch=<m> closed=0|1`
(exit 0 closed / 1 open / 2 usage). Red detail lines go to stderr as
`K15 detail=<file>:<line> ...`; `K15_VERBOSE=1` also emits per-claim supersession lines on a green
run. The transcript is the unedited captured output of `evidence.sh` over the base export (its
commands are printed before each run, absolute paths included).

## Rule implemented

A sentence qualifies when it names a `kasegi-r<NN>-<word>` wave and, in the same sentence, either
predicates `dispatched` of it or gives a `round total` for it. Round and wave are taken from the
sentence: the named wave carries the round, the `wave N` label carries the wave; a label invokes
only the named wave written after it, so `wave 1 X ... wave 2` never borrows wave 1's name. The
named-wave-only form (`<name> N seats dispatched`, no label) is also a claim.

Evidence chain (first hit decides):
1. `.ufo/waves/round-<NN>/wave<label>-results.json`
2. `.ufo/waves/round-<NN>/<named-wave>-results.json`
3. the wave's seat-receipt corpus `.ufo/waves/round-<NN>/{wave<label>,w<label>,<word>}/` holding
   exactly the stated number of `*.md` receipts.

A results artifact must parse as a JSON object with integer `seats` == len(results) and, when the
`round` key is present, `round` == NN. Empty, corrupt or self-contradictory artifacts are
`mismatch`; a present-but-wrong artifact is never retired by prose. Absent evidence is retired
only by a later line in the same file whose stripped text starts with `Correction (round 43)`
(optional `- `/`* `/`**` prefix), carries `never-true` or `not taken`, and names the wave — the
named token, or `wave <label>` together with the round token. Correction blocks are skipped as
assertions (their quoted text cannot re-trigger), and the block ends at a blank line, heading or
new list item so a following LOG entry is never swallowed.

Quoted evidence is not narrative: Markdown table rows, fenced blocks, headings and inline-code
spans (for the `dispatched` predicate) are skipped; `wave1.ready.dispatched` is a filename, not an
assertion. A `round total` with no named wave in the sentence is out of scope by the rule (it
binds totals "for such a wave"), and is neither graded nor counted.

### Why the receipt-corpus limb exists (design decision)

Rounds 23 and 25 predate the `<wave>-results.json` convention. The committed statements

- `LOG.md:1147` — "wave 2 `kasegi-r23-falsify` (36 seats, 19 attack roles) … then dispatched"
- `LOG.md:1293` — "wave 2 `kasegi-r25-falsify`: 32 seats …, dispatched after wave 1"

are true and carry their seat receipts; measured at base:

```
ls .ufo/waves/round-23/falsify/*.md | wc -l   -> 36   (equals the stated 36)
ls .ufo/waves/round-25/wave2/*.md   | wc -l   -> 32   (equals the stated 32)
ls .ufo/waves/round-42/wave2/*.md   | wc -l   -> 0    (the round-42 wave-2 defect)
```

A strict artifact-only rule would red two true statements and force corrections calling them
never-true, i.e. a false correction. The fallback keeps them backed and still leaves round 42 open
(0 `.md`, no artifact).

## Measurements (command → real output; full transcript in the deliverable)

### Base export (the required red, naming every offending sentence)

```
$ bash ExecK15WaveNarrative.sh <scratch>/evidence/base
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
[exit=1]
```

The three reds are exactly RD42-2/RD42-3 (`LOG.md:1804`; `corpus/lessons/round-42.md:11,16`). The
`sentences=5` also counts the two backed round-23/25 sentences above.

### Green: corrections appended

Synthetic blocks (both files, EOF): `K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0
closed=1`, `[exit=0]`. `K15_VERBOSE=1` names the carriers:
`LOG.md:1804 … superseded-by=1808`, `corpus/lessons/round-42.md:11 … superseded-by=151`,
`:16 … superseded-by=151`. `bash limb tree 2>&1 | wc -l` → `1` (stdout stays one line).

The real blocks already drafted in this wave directory (`ScribeCorrections.log.txt` sha256
`7e8f7199…`, `ScribeCorrections.lesson42.txt` sha256 `37423d8b…`) were appended to a fresh copy of
the base export:

```
$ bash ExecK15WaveNarrative.sh <tree>      # base + real correction blocks
K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1
[exit=0]
```

### Round-43 LOG entry (as drafted) and its results artifact

`ScribeLogEntry.log-entry.md` (sha256 `b8a0897f…`) appended on top of the correction blocks:
`LOG.md:1934` reads "`kasegi-r43-hyaku`, 73 seats dispatched".

```
$ bash ExecK15WaveNarrative.sh <tree>      # before the artifact is committed
K15 detail=LOG.md:1934 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 payload=sentences=6,unbacked=1,superseded=3,mismatch=0 closed=0
[exit=1]
$ python3 -c "<write .ufo/waves/round-43/kasegi-r43-hyaku-results.json seats=73>"
$ bash ExecK15WaveNarrative.sh <tree>      # after
K15 payload=sentences=6,unbacked=0,superseded=3,mismatch=0 closed=1
[exit=0]
```

### Mutants

| case | observed |
|---|---|
| results file present, `seats` 35 vs 36 claimed | `mismatch=3 closed=0`, each line `mismatch=seats=35 path=.ufo/waves/round-42/wave2-results.json` |
| results file present, `seats` 36 | `sentences=5,unbacked=0,superseded=0,mismatch=0 closed=1` |
| empty results file | `mismatch=corrupt`, `mismatch=3 closed=0` |
| artifact `round` 41 in the round-42 path | `mismatch=artifact-round-mismatch`, `mismatch=3 closed=0` |
| name `kasegi-r41-falsify` 33 seats in a round-42 lesson | resolved as round 41, backed (`sentences=6`, three round-42 reds unchanged) |
| same name, 39 seats | `mismatch=seats=33 path=.ufo/waves/round-41/kasegi-r41-falsify-results.json` |
| name `kasegi-r42-falsify-2` (hyphen + number) 36 seats | `unbacked=4` (new claim named `kasegi-r42-falsify-2`) |
| `round total` sentence with no named wave | counters unchanged (`sentences=5`) — out of scope, see blind spots |
| fabricated historical lesson, past tense | `corpus/lessons/round-18-history.md:3 … unbacked`, `unbacked=4` |
| correction lacking `never-true`/`not taken` | not retired (`unbacked=3`) |
| correction above the sentence | not a follower (`unbacked=3`) |
| named wave + dispatched, no `wave N` label | `unbacked=4` |
| correction as `- **Correction (round 43)** …` | `superseded=1`, `unbacked=2` |
| correction block immediately followed by `## Round 43` entry | block ends, entry scanned: `LOG.md:1810 … unbacked`, `sentences=6` |

### Harness properties

```
read-only export (chmod -R a-w):            closed=0 (same as base), exit 1, no write attempted
two runs at base, diff:                     "runs identical"
source k15.sh; check_k15 <green tree>:      closed=1
plain run, no export arg:                   exit 2
tree without LOG.md:                        detail=LOG.md absent reason=no-export-tree, exit 1
```

Run time at base: `real 0m0.065s`.

## Integration precondition (L1 must hold for Y to close K15)

The round-43 entry as drafted asserts `73 seats dispatched` (`LOG.md:1934`). K15 stays green at Y
only if the L1 commits `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` with integer
`seats=73` and 73 `results` entries (as the entry itself promises at `LOG.md:1938`). Without that
artifact the entry is itself an RD42-2-class unbacked dispatch sentence and K15 reds at Y — by
design, and exactly as `ScribeLogEntry`'s own brief states ("never write a wave as dispatched
unless `<wave>-results.json` exists"). The correction blocks must keep the literal tokens
`never-true`/`not taken` and the wave name; the drafted bytes do.

## Blind spots (honest, per RevK15's attack list)

1. A `round total` sentence with no named wave at all is not graded: the rule binds totals "for
   such a wave" and there is none to resolve a round directory from. Case J shows the counters do
   not move and the limb does not pretend to pass it (it is not collected).
2. Dispatch synonyms (`sent`, `handed off`, `ran`, `started`) are invisible; only the token
   `dispatched` counts, and only outside inline code.
3. A wave written without the `kasegi-r<NN>-<word>` form (e.g. `kasegi-r42` alone, or
   `kasegi-r42-falsify-results.json` as the name) is not a wave name.
4. A bare `wave2` label (no space or hyphen) is not a label; `wave 2` / `wave-2` are.
5. Markdown table rows and fenced blocks are treated as quoted evidence, so a dispatch claim
   living only inside a table cell is not graded (this is what keeps
   `corpus/lessons/round-42-verifier-spotcheck.md:174`'s quotation from self-triggering).
6. Sentence splitting treats `[.!?]` not preceded by a digit as terminal; a period after an
   abbreviation (`e.g.`) in a claim sentence would split it. No current claim sentence does this.

## Scope and limits

Files written: the two deliverables above and this receipt, plus scratch under
`/fast/scratch/hyaku/kasegi-r43/ExecK15WaveNarrative/` (removed before yielding; nothing under the
fleet root, other lane files, or PATH directories was touched). Git use was read-only
(`rev-parse`, `archive`); no add/commit/checkout/reset/stash/worktree anywhere. No pacman,
no tool installs, no network fetches (no `curl`). No subagents were spawned. The base export was
produced with `git -C <lane> archive ab98fac9… | tar -x -C <scratch>/base` (8384 files, exit 0).

## Risks

- K15 grades every qualifying sentence in LOG.md and all `corpus/lessons/*.md`; a future record
  that states a dispatch without either artifact or the exact correction tokens stays red. That is
  the intended class, but it means the correction tokens are load-bearing (`never-true` /
  `not taken`, exact).
- The receipt fallback compares the `*.md` count exactly; extra non-receipt `.md` files in a wave
  directory would read as a count mismatch.
- Two corrections can both name a wave; the first later line wins and is reported in the verbose
  detail, so supersession accounting is deterministic.
