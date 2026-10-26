# G1' fixture pack — round-39 whole-tail declarations

Five synthetic export trees that pin the round-39 G1 check (whole-tail
declarations). Each fixture is data; `g1-check.sh` is the reference model that
turns a fixture into the exact `G1 payload=... closed=` line the suite must
print. Built for lane `kasegi-shokunin`, round 39, axis `depth:verifiability`;
the fixtures close the four instrument-attack findings that
`corpus/lessons/round-38.md` §Instrument attack findings routed to this round:

| Finding (round 38) | Fixture |
|---|---|
| a declaration may cover only part of the appended tail | `02-partial-tail-red` |
| a `Correction (round 38)` line inside a fence still counts | `03-inside-fence-correction-red` |
| `~~~` fences are not modelled | `04-tilde-fence-green` |
| a declaration path is not confined to the export | `05-outside-path-red` |

## Fixture layout

```
<fixture>/
  base/PROVINCE.md              pre-change front door (commit 1 of the fixture repo)
  base/corpus/README.md
  head/PROVINCE.md              the export tree (commit 2)
  head/corpus/README.md
  head/.ufo/waves/round-39/declared-blocks.txt
  export/…                      the same head bytes as `git archive` extracts them
```

`head/` is the tree the fixture commits as the head; `export/` is that tree as
the suite sees it, so the fixture can be read without git. `g1-check.sh` builds
a throwaway repo from `base/` and `head/` (one commit each, `git rev-parse
--show-toplevel` asserted to be that repo), exports the head with `git archive`,
and prints `export-sync=1` only when the export equals `export/` byte for byte.

## The G1' model (what the suite must implement)

1. **Fence walk** over each whole front door, both fence characters: while
   closed, a line matching `^ {0,3}(`{3,}|~{3,})` with an info string opens a
   fence (a backtick fence's info string may not contain a backtick); while
   open, only a line of the same character with a run at least as long as the
   opener, followed by blanks, closes it. The walk must end `closed` at EOF.
2. **Corrections outside fences**: a line that BEGINS `Correction (round 39)`
   counts only while the fence is closed; inside a fence it is counted in
   `corrections-inside` and does not satisfy the clause. Each front door needs
   at least one outside correction. (The r39 claim states this as a
   fence-exclusion count; it adds no required token inside the line, so the
   fixtures use plain `Correction (round 39): …` text.)
3. **Whole-tail declarations**: every non-comment line of
   `.ufo/waves/round-39/declared-blocks.txt` is `<path> <lines> <sha256>` and
   must satisfy, against the export:
   (a) `<path>` exists in the export (`pending-paths=0`);
   (b) `tail -n <lines> <path> | sha256sum` equals `<sha256>`;
   (c) `<lines>` equals the added-line count of `git diff <base> <head> --
   <path>` (`git diff --numstat`, first field).
   `declared-blocks` counts declarations satisfying (a) and (b);
   `declared-ok=1` only when every line is well formed and (a)-(c) hold for
   every line, with at least one declaration per front door.

## Expected lines

Every line below is the actual stdout of

```
bash g1-check.sh --fixture <fixture> --work <dir outside the lane>
```

`closed=1` means exit 0; `closed=0` means exit 1.

### `01-full-tail-green` — GREEN

Declared lines equal added lines for both doors (PROVINCE 3, README 4), both
fences closed, both corrections outside. Full-tail positive.

```
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1
```

### `02-partial-tail-red` — RED (`declared-ok=0`, `tail=PROVINCE.md:2:3`)

The PROVINCE declaration covers the last 2 of 3 appended lines: the hash still
binds (byte check passes) but the declared count is short of the added-line
count. A partial-tail declaration must be RED.

```
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=0,tail=PROVINCE.md:2:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
```

Discriminating needle: `tail=PROVINCE.md:2:3` (also `declared-ok=0`).

### `03-inside-fence-correction-red` — RED (`province-correction=0`, `corrections-inside=1`)

The appended PROVINCE tail is

````
```text
Correction (round 39): …
```
````

so the fence is balanced and closed at EOF, the tail is whole (3/3), and the
only PROVINCE correction sits inside the fence: it must not count.

```
G1 payload=province-correction=0,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=1 closed=0
```

Discriminating needle: `province-correction=0` with `province-fence=closed`
(the fence is not the failing limb) and `corrections-inside=1`.

### `04-tilde-fence-green` — GREEN under the r39 walk; RED under the r38 walk

The appended PROVINCE tail is

```
~~~text
```bash
echo hi
~~~
Correction (round 39): …
```

A tilde fence opens at `~~~text`; the literal ```` ```bash ```` line inside it
is content. The r39 walk closes on `~~~`, ends `closed`, and counts the
correction (last line, outside the fence) — 5 declared, 5 added.

```
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:5:5,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1
```

The round-38 backtick-only walk is the false RED this fixture forbids: it
ignores `~~~text`, opens on ```` ```bash ````, finds no backtick closer, and
calls the door OPEN, so the correction "inside" the fence does not count:

```
G1 payload=province-correction=0,readme-correction=1,province-fence=open,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:5:5,corpus/README.md:4:4,fence-model=backtick,corrections-inside=1 closed=0
```

Reproduce the old verdict with
`bash g1-check.sh --fixture 04-tilde-fence-green --fence-model backtick`
(exit 1). A suite whose fence walk omits tilde fences fails this fixture the
wrong way: it rejects a door that is closed.

### `05-outside-path-red` — RED (`pending-paths=1`, `declared-ok=0`)

Both real declarations are whole-tail green, and a third declaration names
`corpus/knowledge/ghost.md`, which is not in the export (sha256 of the empty
stream). A declared path outside the export must be RED; the two door
declarations still count as valid (`declared-blocks=2` = declarations that pass
shape, path existence and byte binding; the ghost line fails path existence and
is counted in `pending-paths`).

```
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=1,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
```

## Payload contract

Key order is fixed; every key is `name=value`, comma-separated, and the line
ends ` closed=<0|1>` after one space. One key per clause, so a mutant reopens
exactly one limb:

```
G1 payload=province-correction,readme-correction,province-fence,readme-fence,
           declared-blocks,declared-ok,pending-paths,tail,fence-model,
           corrections-inside closed
```

`tail=` prints `PROVINCE.md:<declared>:<added>` then
`corpus/README.md:<declared>:<added>` in that order. `fence-model=` names the
walk that produced the verdict (`backtick+tilde` for the r39 model) so the
tilde demonstration cannot be mistaken for the graded run.

Closed equation: `province-correction>=1 AND readme-correction>=1 AND both
fences closed AND declared-ok=1 AND pending-paths=0 AND declared-blocks>=2 AND
export-sync=1`.

## Running

```
bash g1-check.sh --fixture 01-full-tail-green --work /path/outside/the/lane
```

`--work` is cleared before use and holds only the throwaway repo and export; the
fixture is never written. Without `--work` the script uses a `mktemp -d` under
`TMPDIR` and removes it on exit.

## Suite integration

The suite's G1 selftest limb can either (a) call this script on the exported
fixture and require the exact expected line and exit status, or (b) inline the
model and build the fixture repo the same way. In both cases the fixture's
`base/` is the diff base for clause 3 — not the lane's round-39 base — so the
fixture grades the clause, not the round's own diff. Both limbs must reject
`02`, `03`, `05` and accept `01`, `04`; `04` under a backtick-only model must
produce `province-fence=open`, which is the failure the fixture exists to catch.

## Fence-walk unit probes (`--walk`)

`--walk FILE` runs clause 1 and 2 alone and prints
`fence-model=<m> state=<closed|open> outside=<n> inside=<n>` (exit 0 only when
`closed`). The cases below are the walk's own contract, each one line of the
r39 model:

| probe file | content | r39 walk | r38 walk |
|---|---|---|---|
| `U1` | ```` ```` ```` opener, ```` ``` ```` mid, ```` ```` ```` closer | `closed` | `closed` |
| `U2` | fence indented four spaces | `closed` (not a fence) | `closed` |
| `U3` | `~~~` block holding a literal ```` ``` ```` line | `closed` | `open` |
| `U4` | ```` ```text ```` with no closer | `open` | `open` |
| `U5` | closer with trailing text (` ```` ``` x ````) | `open` | `open` |
| `U6` | `~~~` opener, ```` ``` ```` closer (character mismatch) | `open` | `open` |
| `U7` | one correction outside, one inside | `closed outside=1 inside=1` | same |

Probe outputs measured on the r39 model:

```
fence-model=backtick+tilde state=closed outside=0 inside=0
fence-model=backtick+tilde state=closed outside=0 inside=0
fence-model=backtick+tilde state=closed outside=0 inside=0
fence-model=backtick+tilde state=open outside=0 inside=0
fence-model=backtick+tilde state=open outside=0 inside=0
fence-model=backtick+tilde state=open outside=0 inside=0
fence-model=backtick+tilde state=closed outside=1 inside=1
```

`U3` under `--fence-model backtick` prints
`fence-model=backtick state=open outside=0 inside=0` (exit 1) — the same false
RED as `04`.

## Clause isolation (mutants of `01-full-tail-green`)

Each mutant changes one limb of the green tree, re-syncs `export/`, and must be
RED with the other keys unchanged:

| mutant | change | payload difference |
|---|---|---|
| `M1-hash-flip` | README declaration hash replaced by 64 zeros | `declared-blocks=1,declared-ok=0,tail=corpus/README.md:0:4` |
| `M2-no-correction` | `Correction (round 39)` → `Correcting (round 39)`, declaration re-hashed | `province-correction=0`, everything else green |
| `M3-door-undeclared` | README declaration line deleted | `declared-blocks=1,declared-ok=0,tail=corpus/README.md:0:4` |

Measured: `M1 closed=0`, `M2 closed=0`, `M3 closed=0`; `M2` leaves
`declared-ok=1` and `declared-blocks=2`, so the correction clause is graded on
its own.
