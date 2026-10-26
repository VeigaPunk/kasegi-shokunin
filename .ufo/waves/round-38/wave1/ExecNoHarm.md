# ExecNoHarm — round-38 wave1 receipt

Seat: `ExecNoHarm` (executor, leaf). Lane `kasegi-shokunin`; round 38; base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims freeze
`9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`.

Deliverable: `.ufo/waves/round-38/wave1/ExecNoHarm.sh`
- 228 lines, 8273 bytes, mode 0755
- sha256 `afbb87d2e87fe91d3cdf802277748f21a12d15e3e7274539a96839aa49a4de83`
- `bash -n` clean (syntax-ok)

The L1 runs it after integration as `bash .ufo/waves/round-38/wave1/ExecNoHarm.sh
<base> <ref>`; the deliverable's bytes are the whole artifact (no embedded tables).

## What the checker does

Two independent limbs per protected file, over a resolved commit range:

1. **Line budget.** `git diff --numstat <base> <ref> -- <10 paths>`. Every protected
   path must report `N	0	<path>`. git omits unchanged paths; the checker prints them
   as `0	0	<path>` in a normalized table and also echoes git's raw numstat block.
   `-` (binary) and any unexpected numstat path (rename/copy `old => new`) are
   failures, because neither can be shown to be append-only.
2. **Byte prefix.** The bytes at `<base>:<path>` must be a byte prefix of the bytes
   at `<ref>:<path>`, using the item's named comparison
   `git show <ref>:<path> | head -n $(git show <base>:<path> | wc -l) | cmp - <(git show <base>:<path>)`,
   with both blobs materialized in a private mktemp dir first (no SIGPIPE, no
   process-substitution race). A base blob with no trailing newline is compared as a
   `<base-bytes>` prefix instead, since `head -n` would otherwise invent the newline;
   for newline-terminated base blobs (all ten at this base) the two forms are
   byte-identical.

Protected list (fixed, in this order): `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`,
`LOG.md`, `SHONEN.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/README.md`,
`corpus/knowledge/considerthese-proposals-ledger.md`, `corpus/lessons/round-37.md`.

Exit codes: `0` append-only; `1` any deletion / binary change / unexpected numstat
path / absent-at-ref / prefix mismatch; `2` could not evaluate (usage, bad revision,
protected path absent at base, repo not a worktree root, mktemp failure).

Repo resolution: the worktree containing the script, else the worktree of the cwd;
`--repo DIR` overrides (needed only when the script is run against a fixture).
Read-only: the only git subcommands are `rev-parse`, `cat-file`, `diff`; writes are
confined to the mktemp dir, removed on exit. Verified: after every run below
`git -C <lane> diff --stat` is empty.

## Validation evidence

### V1 — base → freeze (required positive), exit 0

```
$ bash .ufo/waves/round-38/wave1/ExecNoHarm.sh a173b0c2b98c5ae39599fa9be76027fbbead0b9e 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b
no-harm v1
repo=/home/vgpnk/Projects/shokunin/kasegi-shokunin
base=a173b0c2b98c5ae39599fa9be76027fbbead0b9e
ref=9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b
-- limb 1: git diff --numstat a173b0c2b98c5ae39599fa9be76027fbbead0b9e 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b -- <protected paths> --
(no numstat lines: all protected files byte-identical)
-- normalized numstat: adds<TAB>deletes<TAB>path (unchanged shown as 0/0) --
0	0	SKILL.md
0	0	PROVINCE.md
0	0	SCORECARD.md
0	0	LOG.md
0	0	SHONEN.md
0	0	corpus/QUALITY.md
0	0	corpus/SOURCES.md
0	0	corpus/README.md
0	0	corpus/knowledge/considerthese-proposals-ledger.md
0	0	corpus/lessons/round-37.md
numstat files=10 deletions=0 violations=0
-- limb 2: bytes at <base> must prefix bytes at <ref> --
SKILL.md                                             base-lines=1113   ref-lines=1113   prefix=identical
PROVINCE.md                                          base-lines=152    ref-lines=152    prefix=identical
SCORECARD.md                                         base-lines=1509   ref-lines=1509   prefix=identical
LOG.md                                               base-lines=1692   ref-lines=1692   prefix=identical
SHONEN.md                                            base-lines=178    ref-lines=178    prefix=identical
corpus/QUALITY.md                                    base-lines=278    ref-lines=278    prefix=identical
corpus/SOURCES.md                                    base-lines=118    ref-lines=118    prefix=identical
corpus/README.md                                     base-lines=454    ref-lines=454    prefix=identical
corpus/knowledge/considerthese-proposals-ledger.md   base-lines=43     ref-lines=43     prefix=identical
corpus/lessons/round-37.md                           base-lines=335    ref-lines=335    prefix=identical
prefix files=10 mismatched=0
no-harm: OK
EXIT=0
```

Freeze independently leaves all ten blobs byte-identical: per-file sha256 of
`git show 9a10b02:<path>` equals `git show a173b0c:<path>` (10/10 `same`).

### V2 — base → current lane HEAD `70015359`, exit 0

```
$ bash …/ExecNoHarm.sh a173b0c2… HEAD   → EXIT=0
prefix files=10 mismatched=0
no-harm: OK
```

(The wave-1 spec commit also leaves the ten blobs untouched, so both limbs are
trivially green; the meaningful run is the L1's post-integration run.)

### V3 — the item's literal prefix pipeline agrees, 10/10

```
$ for f in <10 paths>; do
    git -C "$L" show 9a10b02:$f | head -n $(git -C "$L" show a173b0c:$f | wc -l) | cmp - <(git -C "$L" show a173b0c:$f)
  done
literal-cmp identical SKILL.md
literal-cmp identical PROVINCE.md
literal-cmp identical SCORECARD.md
literal-cmp identical LOG.md
literal-cmp identical SHONEN.md
literal-cmp identical corpus/QUALITY.md
literal-cmp identical corpus/SOURCES.md
literal-cmp identical corpus/README.md
literal-cmp identical corpus/knowledge/considerthese-proposals-ledger.md
literal-cmp identical corpus/lessons/round-37.md
mismatches=0
```

The same literal pipeline reports `MISMATCH SCORECARD.md` on the fixture's in-place
edit (`- /dev/fd/63 differ: char 34, line 2`), matching the checker's verdict below.

### V4 — fixture, append-only round (required positive), exit 0

Fixture repo `$S/fixture` (toplevel verified equal to itself), V1→V2 adds one line to
`LOG.md`:

```
-- limb 1 … --
1	0	LOG.md
…
LOG.md                                               base-lines=2      ref-lines=3      prefix=identical
numstat files=10 deletions=0 violations=0
prefix files=10 mismatched=0
no-harm: OK
EXIT=0
```

### V5 — fixture, one in-place edit (required negative), exit 1

`SCORECARD.md` line 2 rewritten in place (V1→V3):

```
-- limb 1 … --
1	0	LOG.md
1	1	SCORECARD.md
numstat files=10 deletions=1 violations=1
-- limb 2 … --
SCORECARD.md                                         base-lines=3      ref-lines=3      prefix=MISMATCH
prefix files=10 mismatched=1
HARM deletions=1 path=SCORECARD.md
HARM prefix-mismatch path=SCORECARD.md
no-harm: HARM
EXIT=1
```

### V6 — fixture, protected file deleted, exit 1

```
0	2	SHONEN.md
numstat files=10 deletions=3 violations=2
SHONEN.md                                            prefix=ABSENT-AT-REF (deleted)
prefix files=10 mismatched=2
HARM deletions=1 path=SCORECARD.md
HARM deletions=2 path=SHONEN.md
HARM prefix-mismatch path=SCORECARD.md
HARM absent-at-ref path=SHONEN.md
no-harm: HARM
EXIT=1
```

### V7 — cannot-evaluate paths, exit 2

```
$ bash …/ExecNoHarm.sh --repo /nonexistent a173b0c 9a10b02
no-harm: cannot evaluate: --repo is not a directory: /nonexistent         exit=2
$ bash …/ExecNoHarm.sh --repo <lane>/corpus a173b0c 9a10b02
no-harm: cannot evaluate: --repo is a subdirectory of the worktree …; pass the worktree root   exit=2
$ bash …/ExecNoHarm.sh a173b0c2… deadbeef
no-harm: cannot evaluate: ref revision does not resolve to a commit: deadbeef   exit=2
$ bash …/ExecNoHarm.sh                       (no operands)
(usage error on stderr)                                                   exit=2
$ fixture base v4 (SHONEN.md deleted) → v1
no-harm: cannot evaluate: protected path absent at base ef4a82f1…: SHONEN.md    exit=2
```

Note: base preflight runs before any limb-2 row is printed, so a base that lacks a
protected path never emits a partial verdict.

### V8 — real lane, backwards/reverse range, exit 1

`base a173b0c → older r37 base b56a416` (this removes the r37 appends):

```
numstat files=10 deletions=531 violations=10
prefix files=10 mismatched=10
HARM deletions=2 path=SKILL.md
HARM deletions=74 path=PROVINCE.md
HARM deletions=15 path=SCORECARD.md
HARM deletions=17 path=LOG.md
HARM deletions=9 path=SHONEN.md
HARM deletions=14 path=corpus/QUALITY.md
HARM deletions=1 path=corpus/SOURCES.md
HARM deletions=56 path=corpus/README.md
HARM deletions=8 path=corpus/knowledge/considerthese-proposals-ledger.md
HARM deletions=335 path=corpus/lessons/round-37.md
HARM prefix-mismatch path=<all ten>
no-harm: HARM
EXIT=1
```

### V9 — r37 base → r37 judged head, exit 2 (documents the preflight)

```
$ bash …/ExecNoHarm.sh b56a4168… 2387dcf6…
no-harm: cannot evaluate: protected path absent at base b56a4168…: corpus/lessons/round-37.md
EXIT=2
```

`corpus/lessons/round-37.md` did not exist at the round-37 base: the ten-path set is
round-38's protection set, and its base must be a commit where all ten exist
(`a173b0c` is). This is intentional fail-closed behaviour, not a false green.

## Incident: accidental writes to the fleet root, repaired

While building the fixture test, the driver's `mk` helper wrote relative paths before
changing directory, so the fixture files landed in the fleet root instead of scratch:

- wrote/truncated at `2026-10-26 15:29:11 -03` in `/home/vgpnk/Projects/shokunin`:
  `LOG.md` (truncated to 22 B) and `SCORECARD.md` (truncated to 51 B) — both tracked
  there; created `PROVINCE.md`, `SHONEN.md`, `SKILL.md` and
  `corpus/{QUALITY.md,SOURCES.md,README.md,knowledge/considerthese-proposals-ledger.md,lessons/round-37.md}`.
- repaired with plain writes from the fleet repo's own HEAD blobs (no git mutation):
  `git show HEAD:LOG.md > LOG.md` → sha256 `9342284d…` equals `git show HEAD:LOG.md |
  sha256sum` `9342284d…`; `git show HEAD:SCORECARD.md > SCORECARD.md` → `3f370f87…`
  equals HEAD `3f370f87…`.
- removed the eight created paths and the then-empty `corpus/knowledge`,
  `corpus/lessons`, `corpus` directories.
- post-repair `git -C /home/vgpnk/Projects/shokunin status --porcelain`:
  ` M .scratch/goal-20261026-hyaku-run9.md` and `?? .ufo/reports/round-48/tameshi.md`
  only — both pre-existing entries belonging to other agents, untouched by me.
- residual risk: if the fleet root's `LOG.md`/`SCORECARD.md` held uncommitted edits
  before 15:29:11, those bytes are unrecoverable; both files now equal their HEAD
  blobs exactly. The fixture driver was fixed to bind every write under `$S` and
  re-run; all fixture evidence above comes from the fixed driver whose repo toplevel
  was verified equal to the scratch fixture.

Scratch: no writes were made to `kasegi-shokunin` outside this wave directory
(`git -C <lane> status --porcelain` shows only the pre-existing untracked
`.ufo/waves/round-38/wave1*` entries created by the L1 before this seat ran; no
tracked file modified).

## Notes, limits, risks

- The ten-path list is fixed for round 38. A post-integration run with `<base> =
  a173b0c` is green iff every round-38 landing is append-only in these files, which
  is exactly claim G1's append-only requirement.
- Limb 2 is deliberately redundant at line level (a rewritten line always yields a
  deletion count): it is the fail-closed backstop for binary numstat (`-`), numstat
  path rewrites, an absent file at `<ref>`, and any parsing hole in limb 1. Both limbs
  were shown to fire independently as rows on the same fixture edit.
- The checker does not judge *content* of appended lines (D-A scaffolding pastes are
  G1's declared-blocks job); it judges only that nothing old was removed or rewritten.
- No network fetches, no tool installs or upgrades, no package-manager transactions.
- Scratch `/fast/scratch/hyaku/kasegi-r38/ExecNoHarm/` (fixture repo, captured
  outputs, temp dir) is removed after this receipt is written.
