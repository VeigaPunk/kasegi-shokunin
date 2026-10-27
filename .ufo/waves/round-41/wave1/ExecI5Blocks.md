# ExecI5Blocks — I5 declared-blocks validator (kasegi round-41, wave 1)

**Seat:** ExecI5Blocks (executor) · **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
· **Round:** 41 (run-10 fresh start) · **Axis:** depth:verifiability (C1 check I5)

## Deliverables

| File | Lines | sha256 |
|---|---|---|
| `.ufo/waves/round-41/wave1/ExecI5Blocks.sh` | 667 | `5f24333761619d1fd30643c88101944ad6e7428f7b31defb0cfee45bbc6bc720` |
| `.ufo/waves/round-41/wave1/ExecI5Blocks.transcript.txt` | 154 | `14a9faa5cbff89e6ceff4b1bf4d1c10122ea6f6bc00ff27192c6617a3fbec23a` |

Both are byte-identical to the copies built in scratch
(`/fast/scratch/hyaku/kasegi-r41/ExecI5Blocks/`), verified after the copy:

```
5f24333761619d1fd30643c88101944ad6e7428f7b31defb0cfee45bbc6bc720  ExecI5Blocks.sh
14a9faa5cbff89e6ceff4b1bf4d1c10122ea6f6bc00ff27192c6617a3fbec23a  ExecI5Blocks.transcript.txt
```

`ExecI5Blocks.sh` is the **landable bytes only** — the limb itself, with its
header contract. No validation table, no notes, no evidence is inside the
deliverable; the evidence is in the transcript and in this receipt.

---

## 1. Design

### 1.1 What a declared block is

A `declared-blocks.txt` holds one declaration per line:

```
<path> <lines> <sha256>
```

It asserts that the file at `<path>` ends with exactly `<lines>` appended
lines whose bytes hash to `<sha256>`, and that the commit range added exactly
those lines and deleted nothing. Round-40's H9 limb already graded three of
the four properties; the round-40 wave-2 attack **T7** showed the fourth was
missing.

### 1.2 The four clauses (the seat's spec, implemented verbatim)

| Clause | Name | Rule | Failure reason |
|---|---|---|---|
| (a) | path shape | no NUL byte, no absolute prefix, no `..` anywhere | `nul-byte`, `path-absolute`, `path-escape` |
| (b) | containment | `readlink`-canonicalized resolved path **must** remain under the canonical export root | `escapes-root` |
| (c) | tail digest | `tail -n <lines>` of the export file hashes to `<sha256>` | `tail-mismatch` |
| (d) | diff shape | `git diff --numstat <base> <ref> -- <path>` → exactly one record, `added == <lines>`, `deleted == 0` | `diff-mismatch`, `diff-deleted`, `diff-ABSENT`, `diff-MULTI`, `diff-BINARY`, `diff-ERR` |

Clause (b) is the round-40 T7 kill. The ordering matters and is deliberate:
**(b) runs before the existence and tail checks**, so an escaping symlink is
reported as an escape and its target is **never read**. The tail digest of an
escaping path would otherwise be computed from bytes outside the tree under
test — which is exactly the defect.

### 1.3 Three guards beyond the four clauses

Each is harmless to an honest declaration and each closes a way the check
could be green without saying what it claims:

- **(b2) the declared path must be a regular file, not a symlink** — git
  counts a symlink as a one-line blob (its target text), so a symlink can
  never be an appended text block; allowing one would let a declaration
  certify the bytes of a file the range never touched. Reason
  `symlink-declared`. This is the reason that fires for a symlink pointing
  *inside* the export (contained, but not an appendable block).
- **(c2) the export file must really carry at least `<lines>` lines** — else
  `tail -n <lines>` silently clips and the digest means something other than
  the declared tail. Reason `lines-exceed-file`.
- **(e) a declaration line that does not parse is a declared-but-invalid
  declaration, never a silently dropped one** — a gate must not be green with
  a declaration it could not read. Reason `malformed-line`, counted in the
  payload as `malformed=N`.

### 1.4 The NUL clause needs a byte-level scan

Bash's `read -r` **drops** NUL bytes, so a path carrying a NUL cannot be
detected by parsing the line. `i5_nul_scan` therefore finds the NUL-bearing
**line numbers** with `grep -a -nP '\x00'` and maps them onto the declaration
records, with a byte-count fallback (`tr -d '\000' | wc -c` against `wc -c`)
for a host without PCRE. The scan is per line, so a NUL in one declaration
does not redden the others.

### 1.5 The API

```
i5_declared_blocks_check EXPORT_ROOT LANE BASE_REF REF DECLARED_FILE
```
Prints one detail line per declaration (`I5-decl path=… lines=… verdict=… reason=…`;
stderr by default, stdout with `I5_DETAIL=1`) and a final summary line, which
is always the last stdout line:

```
I5 payload=declared=N,valid=N,tail=N,malformed=N,pure=1|0,paths=1|0,canon=1|0,nul=0|1,diff-read=ok|fail closed=0|1
```

Exit 0 only when `closed=1`; exit 1 on a defect; exit 2 on a harness error
(unreadable export, unreadable lane, unresolvable ref, unreadable declared
file, degenerate export root).

`i5_check_in_tree TREE REF` is the **suite-facing wrapper**, in the idiom of
the round-40 suite's `check_h9 TREE REF`: it reads the globals `LANE`,
`BASE_REF` and `DECLARED` and grades the declared file inside `TREE`. The
committed r41 suite can call it directly. Verified against the real lane:

```
I5 payload=declared=293,valid=293,tail=293,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok closed=1
wrapper-exit=0
```

The file is **sourceable**: sourcing it defines 19 `i5_*` functions and
changes nothing else (`sourced-ok` / `type -t i5_declared_blocks_check` →
`function`). Running it executes the CLI (`--check`, `--selftest`).

### 1.6 Read-only discipline

The limb never writes under the lane, the export or any tracked tree. Its only
writes are `mktemp -d` scratch dirs under `$TMPDIR`, removed on exit. All git
reads use `--no-optional-locks`. The lane was touched only with read-only
`git show` / `git archive` / `git diff` / `git rev-parse`.

---

## 2. Evidence — the transcripts

Full byte-exact output: `ExecI5Blocks.transcript.txt`. The load-bearing parts:

### 2.1 The required rejection — symlink `pwn -> /etc` declared

A scratch export contains `pwn -> /etc`; `declared-blocks.txt` declares it
with the digest of the *outside* file's last line.

```
$ bash ExecI5Blocks.sh --check --export-root …/export --lane …/fixture --base … --ref … --declared …/declared-blocks.txt
I5-decl path=pwn lines=1 verdict=fail reason=escapes-root
I5 payload=declared=1,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=0,nul=0,diff-read=ok closed=0
exit=1
```

### 2.2 The required green — an honest declared append

```
$ bash ExecI5Blocks.sh --check --export-root …/export --lane …/fixture --base … --ref … --declared …/declared-blocks.txt
I5-decl path=PROVINCE.md lines=3 verdict=pass reason=-
I5 payload=declared=1,valid=1,tail=1,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok closed=1
exit=0
```

### 2.3 The load-bearing comparison — the **verbatim** round-40 H9 limb

`path_safe` + `check_h9` were extracted byte-exactly from the committed
`corpus/instruments/r40-closure.sh` with `git show HEAD:corpus/instruments/r40-closure.sh`
and run against the *same* fixture with the same globals. The escape to a
**file** outside the export:

```
--- measure: symlink-to-file (declared symlink pwn -> /etc/passwd) ---
  readlink -f export/pwn = /etc/passwd
  r40 r40-h9 payload=declared=1,valid=1,tail=1,pure=1,paths=1,diff-read=ok
  r40 r40-h9 exit=0                      <-- GREEN under the round-40 rules
  i5   I5-decl path=pwn lines=1 verdict=fail reason=escapes-root
  i5   I5 payload=declared=1,valid=0,tail=0,malformed=0,pure=1,paths=1,canon=0,nul=0,diff-read=ok closed=0
```

This is the round-40 wave-2 **T7** defect, reproduced and measured: the
round-40 rule set certified bytes that live outside the tree under test. The
I5 limb reds it.

(The `pwn -> /etc` **directory** variant happens to be caught by round-40 too
— `path_safe` rejects nothing there, but `check_h9`'s `[ ! -f "$tree/$path" ]`
fails on a directory, so r40 reports `paths=0`. The load-bearing escape is
the symlink-to-**file** case, which is what the round-40 defeat record shows:
`numstat: 1 0 pwn`, `rc=0`. Both variants are in the transcript and I5 reds
both with `escapes-root`.)

### 2.4 Real lane data — no false reds

The **real** round-40 `declared-blocks.txt` (293 declarations), exported from
the round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd`:

```
I5 payload=declared=293,valid=293,tail=293,malformed=0,pure=1,paths=1,canon=1,nul=0,diff-read=ok closed=1
exit=0
```

The same export with a `pwn -> /etc` symlink declared on top:

```
I5-decl path=pwn lines=1 verdict=fail reason=escapes-root
I5 payload=declared=294,valid=293,tail=293,malformed=0,pure=1,paths=1,canon=0,nul=0,diff-read=ok closed=0
exit=1
```

So the containment clause costs nothing on the 293 real honest declarations
and reds the injected one.

### 2.5 The limb's own selftest — 14 cases, 0 failures

```
selftest case=I5 honest verdict=pass reason=-
selftest case=I5 t7-symlink-escape verdict=pass reason=escapes-root
selftest case=I5 symlink-to-directory verdict=pass reason=escapes-root
selftest case=I5 path-dotdot verdict=pass reason=path-escape
selftest case=I5 path-absolute verdict=pass reason=path-absolute
selftest case=I5 path-nul verdict=pass reason=nul-byte
selftest case=I5 tail-mismatch verdict=pass reason=tail-mismatch
selftest case=I5 diff-added-mismatch verdict=pass reason=diff-mismatch
selftest case=I5 diff-with-deletion verdict=pass reason=diff-deleted
selftest case=I5 lines-exceed-file verdict=pass reason=lines-exceed-file
selftest case=I5 path-absent verdict=pass reason=absent
selftest case=I5 inner-symlink verdict=pass reason=symlink-declared
selftest case=I5 malformed-line verdict=pass reason=malformed-line
selftest case=I5 malformed-line-2 verdict=pass reason=malformed-line
selftest legacy=round40-h9 case=t7-symlink-escape verdict=green
selftest cases=14 failures=0
selftest-exit=0
```

Each defeat case reds on the clause it exercises, not on an incidental one.
The `malformed-line` case is checked to red the **whole** check, not just its
own line: `declared=2,valid=1,tail=1,malformed=1,… closed=0`.

---

## 3. Commands run (and their actual results)

| Command | Result |
|---|---|
| `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | green — `/tmp` 3 %, `/var/tmp` 35 %, `/fast/scratch/hyaku` 24 % (all < SOFT_PCT 70) |
| `bash -n ExecI5Blocks.sh` | exit 0 (syntax clean) |
| `bash ExecI5Blocks.sh --selftest` | `selftest cases=14 failures=0`, exit 0 |
| `bash ExecI5Blocks.sh --check --export-root <real export> --lane $LANE --base a7af2ce6… --ref c7aea5ef… --declared .ufo/waves/round-40/declared-blocks.txt` | `declared=293,valid=293,… closed=1`, exit 0 |
| same with an injected `pwn -> /etc` declaration | `declared=294,valid=293,… closed=0`, exit 1 |
| `git show HEAD:corpus/instruments/r40-closure.sh` (extract `path_safe` + `check_h9`) | 1734 lines; the two functions extracted byte-exactly and run on the fixture |
| `git -C "$D" rev-parse --show-toplevel` (every fixture, before any commit) | equals the fixture dir — asserted, `toplevel-assert=ok` in the transcript |

No network fetch was performed by this seat. No tool was installed or
upgraded: the limb uses only bash, GNU coreutils, GNU grep (PCRE), awk and
git, all present on the host. No `pacman` transaction was run (host-wide
pause).

---

## 4. Fixture and host safety

- Scratch dir: `/fast/scratch/hyaku/kasegi-r41/ExecI5Blocks/` (all fixtures,
  exports and work trees bound here; `TMPDIR` forced to it). **Removed before
  yield.**
- Every git fixture: `git -C "$D" init -q` under scratch, with
  `git -C "$D" rev-parse --show-toplevel` asserted equal to the fixture dir
  before any commit. The assertion output is in the transcript.
- No throwaway git identity was written anywhere: every commit uses
  `git -c user.name=… -c user.email=…` on the command line, so no config
  file — global or local — is modified.
- No mutating git/jj command was run in the lane, the fleet root or anywhere
  else. Only `git show`, `git archive`, `git diff`, `git rev-parse`,
  `git cat-file` (all read-only) plus `git init`/`git add`/`git commit`
  inside scratch fixtures.
- Nothing was written to any PATH directory, `~/.omp/agent/config.yml`,
  `~/.omp/agent/mcp.json`, or any host service.
- The lane repo was not edited: the only lane writes are the two deliverable
  files and this receipt, all inside `.ufo/waves/round-41/wave1/`.

---

## 5. Risks and blockers

- **None blocking.** The limb is complete, self-tested and proven on both a
  synthetic fixture and the real lane data.
- **Integration note for the L1** (not a blocker): the r41 suite's I5 must
  call `i5_declared_blocks_check` (or the `i5_check_in_tree TREE REF`
  wrapper) and grade the **round-41** `.ufo/waves/round-41/declared-blocks.txt`
  — the round-40 file I used for the no-false-red measurement is the
  round-40 one, and the round-41 file does not exist yet. The limb's
  `--selftest` builds its own fixtures and does not depend on any lane file.
- **Scope note:** the seat spec asks for a `declared-blocks.txt` of
  `<path> <lines> <sha256>` lines; the limb grades exactly that. The
  round-38 `ExecDeclaredBlocks.gen.sh` limb (a *generator* for declarations,
  with a different `# base` guard syntax) is a different artefact and was not
  modified. The `i5` limb supersedes the round-40
  `ExecH9DeclaredBlocks.validator.sh` for the T7 property, which the
  round-40 wave-2 record shows it lacked.
- The `--selftest` mode's `i5_legacy_h9_check` control deliberately omits the
  containment clause. It is a **control**, never a validator: it prints a
  `legacy …` payload with a different key prefix, and the suite must not call
  it. It is documented as such in the limb header.

---

## 6. Report trailer

`Report: .ufo/waves/round-41/wave1/ExecI5Blocks.md` (this file, written last).
