# ExecPinnedG8Fixture.fixtures — G8' pinned-bytes fixture set

Committed payloads for the round-39 closure suite's G8 limb
(`corpus/instruments/r39-closure.sh`, claim C1, `depth:verifiability`). G8 carries the
round-37 closure suite forward: the export's `corpus/instruments/r37-closure.sh` is trusted only
when its bytes hash to the bytes `git show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh`
returns **and** the run of those pinned bytes ends `closed=14/14 exit=0` with exit 0.

The run is always of the pinned bytes, never of the export copy. A copy that has been edited
supplies no verdict of its own.

## Pinned bytes

| field | value |
|---|---|
| commit | `2387dcf6ccfefcfb703783387b9aade8fc82abfa` (round-37 judged head) |
| path | `corpus/instruments/r37-closure.sh` |
| extract | `git -C <lane> show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh` |
| blob | `68ac41e8fdab46ba508800a377f396e663f2a436` |
| sha256 | `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d` |
| size | 73132 bytes, 1558 lines |

`pinned/r37-closure.sh` is that byte stream verbatim; `pinned/sha256.txt` is the same digest in
`sha256sum` format (`sha256sum -c pinned/sha256.txt` passes with cwd `pinned/`), `pinned/commit.txt`
and `pinned/path.txt` name the source of the bytes.

## Cases

Each case directory holds a `case.env` (`name`, `source`, `copy`, `run`, `run_exit`, `run_source`,
`mutation`, `note`) and, where a run exists, its transcript. `source=pinned` means the export copy is
the pinned byte stream, `source=copy` means the case carries its own copy under
`corpus/instruments/r37-closure.sh`, `source=absent` means the export has no copy at all.

| case | export copy sha256 | digest-match | run ends | expected |
|---|---|---|---|---|
| `positive/` | `0da98e37…42434d` (pinned) | 1 | `closed=14/14 exit=0`, exit 0 | GREEN |
| `negative-mutated/` | `4a5aea99…060483` (one byte off) | 0 | `closed=14/14 exit=0`, exit 0 | RED |
| `negative-open/` | `0da98e37…42434d` (pinned) | 1 | `closed=13/14 exit=1`, exit 1 | RED |
| `negative-absent/` | — | 0 | no run | RED |

The mutation in `negative-mutated/` is byte 78 (1-based): `1` → `2` inside the line-2 comment
`claim C1` → `claim C2`. The file keeps its 73132 bytes and 1558 lines, `cmp -l` reports exactly one
differing byte, and both files parse under `bash -n`. It is a comment byte, so no check reads it —
except the digest.

## Expected payload lines

`expected/expected.txt` is the contract, one line per case:

```
<case> -> G8 payload=<pinned-sha256>,<export-sha256>,<digest-match>,<r37-suite>,<r37-closed>,<r37-exit> closed=<0|1>
```

The full lines are in the file; the decision rule is

```
closed=1  iff  digest-match=1 AND r37-suite=1 AND r37-closed=1 AND r37-exit=0
r37-closed=1  iff  the transcript's last non-empty line is exactly `closed=14/14 exit=0`
```

## How to run the set

```
bash g8-pinned-check.sh                  # all four cases
bash g8-pinned-check.sh negative-mutated # one case
```

The harness materialises each case's export copy under a `mktemp -d` (honouring `TMPDIR`), hashes
it, reads the transcript, prints the `G8 payload=… closed=…` line the suite must print for that
state, compares it byte-exactly with `expected/expected.txt`, and exits 0 only when every case
matches. It reads no lane, no git object and no network, so it is safe to run from anywhere.

Measured at build time:

```
case=positive verdict=PASS
case=negative-mutated verdict=PASS
case=negative-open verdict=PASS
case=negative-absent verdict=PASS
g8p cases=4 failures=0
```

## Why the digest limb, and not just the run

Measured on the pinned bytes at `2387dcf6` (a lane whose HEAD is not that ref, so E9 is red):

| state | run |
|---|---|
| pinned bytes | `closed=13/14 exit=1` (E9 `head-match=0`, `status-dirty=7`) |
| the one-byte mutant | `closed=12/14 exit=1` — after normalising `suite-sha256`, the only difference from the pinned run is E10 (`digest-match=1` → `0`); E1–E9 and E11–E14 are byte-identical |

So the mutation is behaviour-neutral for every check except the digest read. And E10's digest read is
not enough on its own: rewrite the export's own receipt (`suite-sha256=` in
`.ufo/waves/round-37/final-gates/all-gates.txt`) to the mutant digest and E10, executing the mutant
copy, returns `digest-match=1 … rc=0` — the coordinated edit makes the tampered export look exactly
like the pinned one. G8' therefore pins the digest from the git object at `2387dcf6` (the bytes
`git show` returns), which no edit inside the export can move.

## Limits

- **These are payloads for the limb's decision, not a second suite.** The transcripts are recorded
  runs: `positive/` and `negative-mutated/` carry the committed round-37 receipt block
  (`.ufo/waves/round-37/final-gates/all-gates.txt` lines 8–22, whose `suite-sha256` is the pinned
  digest), and `negative-open/` carries this round's measured run at `2387dcf6`. A live
  `closed=14/14` needs a clean lane whose HEAD is the exported ref (E9's quiescence limbs are live);
  no fixture can supply that, and none claims to.
- **The harness models the limb; the suite is authoritative.** The payload keys above are the
  contract this set binds. If `r39-closure.sh` emits a different key set, the fixtures still hold
  their inputs and expected verdicts, but `expected/expected.txt` must be regenerated to the suite's
  spelling.
- **The mutation is a comment byte on purpose.** It proves the digest limb discriminates on a state
  whose checks all read the same; it does not prove the suite rejects a semantic edit, which is the
  selftest mutants' job.
