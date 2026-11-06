# ExecStatedOutput — round 83, attempt 1 (wave w1)

Seat: executor. Assignment: r82 routed defect 5 — the M82-3 stated-output check is the wave script
`.ufo/waves/round-82/l1/stated-output-check.py`, not a registered lane instrument; produce a
candidate lane instrument, a registry-row block, and shown-fail/shown-pass evidence.

Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. No lane file was edited. No git/jj
mutation. No delegation, no background jobs, no tool installs (host `python3` 3.14.8 sufficed; no
pacman transaction).

## Files written

- `.ufo/waves/round-83/w1/ExecStatedOutput-candidate-stated-output-check.py` — the candidate
  instrument (20012 bytes, 562 lines, sha256
  `3b086668e63956b916d540f7e21094d788d5cd8b77bd9ce62303630804441b31`).
- `.ufo/waves/round-83/w1/ExecStatedOutput-registry-rows.txt` — the exact SKILL.md and
  `corpus/instruments/README.md` append blocks (same 8-column row in both), plus insertion anchors,
  the README limits paragraph, and the receipts the rows rest on.
- `.ufo/waves/round-83/w1/ExecStatedOutput.md` — this report.
- `.ufo/waves/round-83/w1/ExecStatedOutput-receipts/stated-output-check-selftest.txt`
- `.ufo/waves/round-83/w1/ExecStatedOutput-receipts/stated-output-entries-r83.txt`
- `.ufo/waves/round-83/w1/ExecStatedOutput-receipts/stated-output-m823-replay.txt`
- `.ufo/waves/round-83/w1/ExecStatedOutput-receipts/stated-output-all-entries.txt`

## What the instrument is

`stated-output-check.py` checks the canonical claim shape

```
`<command>` prints <output> and exits <N>
```

by running the command with `bash -c` in `--root` (default cwd). Assertions: exit status equals N;
`nothing` means stdout is empty (stderr counted, not asserted); otherwise the phrase's single
backticked literal must start at least one stdout line, and a phrase saying "one … line" requires
exactly one stdout line. It keeps the round-82 script's "prints nothing and exits 1" limb and adds
the stated-literal and one-line limbs — the shape F58's landed Limits line actually uses.

Fail-closed refusal rules (never executed, counted as failure): a segment head outside the
read-only allow-list (grep egrep fgrep printf echo true false test [ wc sha256sum diff sort cut head
tail cat ls); a `python3` segment that does not name `corpus/instruments/<name>.py`; `>(`-class
writes — specifically `>`, a lone `&`, or `$(` anywhere. Segments split at unquoted `|`, `||`, `&&`,
`;`.

Exit map: 0 every matched output holds and refused=0; 1 mismatch or refusal; 2 usage/read error.
`--selftest` runs 21 cases (six fail-expecting: stdout-not-empty, rc mismatch, literal missing,
one-line limb, destructive-head refusal, timeout; plus redirect/pipeline/python3 refusals,
quoted-pipe admission, multi-command, outside-grammar, TMPDIR honoured/refusal, no hard-coded temp
path, missing-file exit 2, no-files exit 2, CLI exit mapping). Every temporary path comes from
`tempfile` with an explicit TMPDIR base; the source contains no hard-coded temp path (asserted by
the selftest).

## Evidence (pasted, with rc)

### 1. `--selftest` (receipt `stated-output-check-selftest.txt`)

```
$ TMPDIR=<scratch> python3 .ufo/waves/round-83/w1/ExecStatedOutput-candidate-stated-output-check.py --selftest
ok   pass-nothing
ok   fail-stdout-not-empty
ok   fail-rc-want-1-got-0
ok   pass-literal-one-line
ok   fail-literal-missing
ok   fail-one-line-limb
ok   refuse-destructive-head
ok   refuse-redirect
ok   refuse-second-segment-head
ok   refuse-python3-not-instrument
ok   pass-python3-instrument
ok   quoted-pipe-not-a-segment
ok   multi-two-commands
ok   outside-grammar-not-run
ok   timeout-is-a-failure
ok   tmpdir-honoured
stated-output-check: TMPDIR is not an existing directory: <scratch>/stated-output-check-*/absent
ok   tmpdir-refusal-exit-2
ok   no-hardcoded-temp-path
stated-output-check: <scratch>/stated-output-check-*/missing.md: [Errno 2] No such file or directory
ok   missing-file-exit-2
usage: stated-output-check.py [-h] [--root ROOT] [--timeout TIMEOUT] [--selftest] [files ...]
ok   no-files-exit-2
ok   cli-exit-map
selftest cases=21 failures=0
rc=0
```

### 2. On F58 `corpus/knowledge/osv-high-quality-record-import-bar.md` (receipt `stated-output-entries-r83.txt`)

```
$ TMPDIR=<scratch> python3 .ufo/waves/round-83/w1/ExecStatedOutput-candidate-stated-output-check.py corpus/knowledge/osv-high-quality-record-import-bar.md
FILE corpus/knowledge/osv-high-quality-record-import-bar.md commands=1 mismatches=0 refused=0
OK      rc=0 out_lines=1 err_lines=0  :: grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt
STATED-OUTPUT files=1 commands=1 mismatches=0 refused=0
rc=0
```

### 3. On the r83 draft `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` (same receipt)

```
$ TMPDIR=<scratch> python3 .ufo/waves/round-83/w1/ExecStatedOutput-candidate-stated-output-check.py corpus/knowledge/osv-faq-post-import-record-lifecycle.md
FILE corpus/knowledge/osv-faq-post-import-record-lifecycle.md commands=0 mismatches=0 refused=0
STATED-OUTPUT files=1 commands=0 mismatches=0 refused=0
rc=0
```

`commands=0` is a vacuous pass and is reported as such by design: the draft's only output-shaped
sentence is the recheck-receipt line ("the `recheck:` line above printed `S117:sha256 OK` … exit 0"),
whose subject is not a backticked command, and its Limits bullets state no command output. So the
M82-3 defect class is not present in the draft as far as this grammar can see; the recheck receipt
itself is covered by `source-recheck.py`, not by this instrument.

### 4. M82-3 replay and discrimination (receipt `stated-output-m823-replay.txt`)

A. The round-82 pre-review Limits sentence must fail:

```
FAIL    rc=0 out_lines=1 err_lines=0 rc-want-1-got-0 :: grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt
STATED-OUTPUT files=1 commands=1 mismatches=1 refused=0
rc=1
```

B. The round-82 wave script on the landed F58 entry matches nothing — the gap this instrument closes:

```
$ python3 .ufo/waves/round-82/l1/stated-output-check.py corpus/knowledge/osv-high-quality-record-import-bar.md $PWD
STATED-OUTPUT commands=0 mismatches=0
rc=0
```

C. The draft with two injected false stated outputs (scratch copy only) fails twice, with distinct
reasons — the instrument is shown able to fail on the draft's own bytes, not just on fixtures:

```
FAIL    rc=0 out_lines=1 err_lines=0 rc-want-1-got-0 :: grep -c 'withdrawn' corpus/source-snapshots/round-83/S117.txt
FAIL    rc=0 out_lines=1 err_lines=0 literal-missing:9: :: grep -n -i -E 'IMPORT_FINDING|finding' corpus/source-snapshots/round-82/S116.txt
STATED-OUTPUT files=1 commands=2 mismatches=2 refused=0
rc=1
```

D. Census over every knowledge entry stays green (receipt `all-entries`):

```
STATED-OUTPUT files=97 commands=20 mismatches=0 refused=0
rc=0
```

Files with matched commands: `fuzzilli-js-engine-fuzzing-framework.md` (2),
`osv-determineversion-cc-library-versioning.md` (6), `osv-high-quality-record-import-bar.md` (1),
`osv-importfindings-record-quality-feedback.md` (3), `osv-post-batch-query-contract.md` (3),
`osv-ubuntu-binary-to-source-mapping.md` (5). 91 entries contribute 0 matched commands.

## Registry rows

See `ExecStatedOutput-registry-rows.txt`: one appended `## Round-83 Gates & probes registry
addition (appended 2026-11-06)` block for `SKILL.md` (after the current last line, the r71
amendment) and one `## Round-83 instrument registry addition — stated-output-check.py` block for
`corpus/instruments/README.md` (after the round-50 section's last line), each with the same 8-column
row naming the committed path `corpus/instruments/stated-output-check.py`, the exit map, the
selftest line (`selftest cases=21 failures=0`), the pinned receipt path, the write scope and
`kasegi` as owner. The README block also carries a measured-limits paragraph.

## Risks and limits (routed, not hidden)

1. **The grammar is narrow by choice.** Claims without an inline backticked command are not checked
   — e.g. F58's Distinctness sweep ("… printed nothing for each") and the draft's "0 files each".
   Registering this instrument does not make those claims machine-checked. If the L1 wants them
   covered, the entries must state the command in the canonical shape (the sweep body contains a
   `<q>` placeholder, so today it is not runnable as written).
2. **Not a sandbox.** The allow-list refuses destructive heads and obvious write/substitution
   forms, but it is not a capability proof; the input is lane-authored markdown and is trusted.
   `python3` is admitted only for `corpus/instruments/*.py`, but an admitted instrument can still do
   whatever that instrument does.
3. **Environment inherited.** A stated output is checked against this host's command behaviour and
   these bytes, not against the author's run. `stderr` is counted but not asserted.
4. **Vacuous pass on zero matches.** `commands=0` is green on purpose (a file may make no
   stated-output claim); readers must read the count, as the registry row and docstring say.
5. **Timeout is a failure** and prints `timeout`; the default 60 s is per command.
6. The one-line limb is a lexical reading of "one … line" in the output phrase; a phrase worded
   differently is not held to it.

## Blockers

None. The candidate needs only the L1's integration (move to `corpus/instruments/`) and the two
registry appends; both blocks are in the rows file, and the evidence is re-runnable from the lane
root with the exact commands in each receipt header.

Scratch `/fast/scratch/hyaku/kasegi-r83/ExecStatedOutput` was removed before this yield; every
receipt cited here was copied into `.ufo/waves/round-83/w1/ExecStatedOutput-receipts/` first.
