# ExecD4ResultsTrack — round-35 wave 1 receipt (item D4)

- Lane: `kasegi-shokunin`, round 35, wave 1. Lane `HEAD` at filing: `da2d3c687f82a9814ee71c91c930cb733050d37c`
  (base `3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`).
- Item: spotcheck D4 — prepare the provenance note for `.ufo/waves/round-34/wave1-results.json` and verify
  identity. **Leaf seat: it did not commit, did not stage, and did not touch any other file.**

**Verdict: D4 is prepared, not closed.** The note exists beside the file and the file's identity is pinned;
closure happens only when the L1 commits the file (§4; the frozen counter still reads `0` now, by design).

## Report

### 1. Commands and outputs (verbatim, with exit codes)

```
$ date -u
Mon 26 Oct 2026 06:30:13 AM UTC
exit 0
$ date
Mon 26 Oct 2026 03:30:13 AM -03
exit 0
```

mtime + size of the D4 subject:

```
$ stat -c '%s %y %n' .ufo/waves/round-34/wave1-results.json
312874 2026-10-26 03:23:19.274615406 -0300 .ufo/waves/round-34/wave1-results.json
exit 0
```

sha256 (pinned):

```
$ sha256sum .ufo/waves/round-34/wave1-results.json
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  .ufo/waves/round-34/wave1-results.json
exit 0
```

The verifier's abbreviated digest `3afa3581afb14aba…` (`round-34-verifier-spotcheck.md` §1 row "No uncommitted
round work" → D4) is a prefix of this full digest, and `312874 B` matches the verifier's byte count. The pinned
check runs green against the live file (run after the note was written, so the pin was re-confirmed post-write):

```
$ printf '%s  %s\n' 3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4 .ufo/waves/round-34/wave1-results.json | sha256sum -c -
.ufo/waves/round-34/wave1-results.json: OK
verify_exit=0
```

The `complete` line the write postdates — read from the fleet root (read-only to this seat):

```
$ grep -n 'kasegi round=34' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log | tail -5
1474:2026-10-26T02:24:07-03:00 launch kasegi round=34 pgid=98669 driver=hyaku-inline attempt=1
1485:2026-10-26T03:15:20-03:00 lane-dead-no-report kasegi round=34; retry same round (hyaku-inline attempt=1: L1 KasegiR34 exited without a landed round: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-34/kasegi.md)
1486:2026-10-26T03:15:22-03:00 launch kasegi round=34 pgid=1260200 driver=hyaku-inline attempt=2
1488:2026-10-26T03:19:31-03:00 complete kasegi round=34; hyaku-inline attempt=2
exit 0
```

`03:19:31 -0300` = `06:19:31Z`; the file's `03:23:19 -0300` = `06:23:19Z` → **written 3 min 48 s after the
closure line**. That gap is the D4 defect; the note states it as such.

Content shape, measured over the parsed JSON (`json.loads`, exit 0) — this is what the note's §1 records:

```
lane 'kasegi' round 34 wave 'wave1' seats 65
results 65 rows; row keys ['agent','name','note','output']; unique names 65
spec items 65; results-names vs spec-names: both set differences empty
agent counts {'executor': 19, 'scribe': 10, 'reviewer': 13, 'mutation-tester': 7, 'scout': 5, 'critic': 5, 'connector': 3, 'sentinel': 2, 'simplifier': 1}
note null rows 65; note nonempty 0
output null 0; empty 0; lengths min 1246 max 11726 total 291117
receipts in wave1/ = 67; receipts not in results = ['L1Integration','ScribeReportDraft-2']; results not in receipts = []
```

Index state before the L1 integration commit (three separate reads; all as expected for D4-open):

```
$ git ls-files .ufo/waves/round-34/wave1-results.json
(no output)
ls_files_exit=0, `| wc -l` = 0
$ git status --porcelain --untracked-files=all -- .ufo/waves/round-34/
?? .ufo/waves/round-34/wave1-results.json
?? .ufo/waves/round-34/wave1-results.json.provenance.md
exit 0
$ git check-ignore -v .ufo/waves/round-34/wave1-results.json
(no output)
check-ignore exit=1   → not ignored, so no `git add -f` is needed
```

Quiescence of the round-34 wave (no file in `wave1/` newer than the snapshot):

```
$ ls -lt --time-style=full-iso .ufo/waves/round-34/wave1 | head -3
-rw-r--r-- 1 vgpnk vgpnk 30192 2026-10-26 03:22:26.509658413 -0300 ExecRegressionC1.md
-rw-r--r-- 1 vgpnk vgpnk  3522 2026-10-26 03:18:07.555499300 -0300 L1Integration.md
-rw-r--r-- 1 vgpnk vgpnk 54457 2026-10-26 03:17:46.930887672 -0300 L1Integration.raw
exit 0
```

The transiently rewritten D4-window receipt is byte-identical to its committed blob, so it is not an
outstanding artifact:

```
$ sha256sum .ufo/waves/round-34/wave1/ExecRegressionC1.md
6b3604cb6d5aca94e68f2b2a66aaaaee5ed9c3e2856ba9f7c5c13cd32b06de83  .ufo/waves/round-34/wave1/ExecRegressionC1.md
$ git show c1c6a5f:.ufo/waves/round-34/wave1/ExecRegressionC1.md | sha256sum
6b3604cb6d5aca94e68f2b2a66aaaaee5ed9c3e2856ba9f7c5c13cd32b06de83  -
exit 0
$ git diff --stat -- .ufo/waves/round-34/
(no output)   exit 0
```

Precedent that the note's §2 asserts: the round-33 dispatcher output *is* tracked in this repository, whereas
round-34's is not —

```
$ git ls-files .ufo/waves/round-33/wave1-results.json
.ufo/waves/round-33/wave1-results.json
exit 0
```

The closure limb the note is written against (`build-spec.py` item ExecClosureSuite, D4 check): "the results
file is tracked (`git ls-files … | wc -l` == 1) AND the provenance note
`.ufo/waves/round-34/wave1-results.json.provenance.md` exists." The note limb is satisfied now; the tracked limb
becomes true at the L1's integration commit. `corpus/instruments/r35-defect-closure.sh` does not exist yet
(`ls: cannot access … No such file or directory`, exit 2 — the frozen before-state), so nothing was run against it.

### 2. File digests (all written bytes)

| path (lane-relative) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-34/wave1-results.json` (subject, untouched by this seat) | 312874 | `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4` |
| `.ufo/waves/round-34/wave1-results.json.provenance.md` (new) | 5639 | `e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98` |
| `.ufo/waves/round-35/wave1/ExecD4ResultsTrack.md` (this receipt) | — | not self-pinned (a file cannot carry its own final digest); the L1 records it in the commit |

The subject's digest was recomputed **after** the note was written and is unchanged (`verify_exit=0` above), so
the note describes the exact bytes standing in the tree.

### 3. Note text (verbatim; sha `e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98`)

<!-- BEGIN note -->
# Provenance — `.ufo/waves/round-34/wave1-results.json`

Filed by seat `ExecD4ResultsTrack` (round-35 wave 1, item D4) on 2026-10-26 ~06:32Z, in the lane
`kasegi-shokunin` at lane `HEAD` `da2d3c687f82a9814ee71c91c930cb733050d37c` (round-35 wave-1
spec + dispatch; round-34 tip below it is `c1c6a5f826d2425446347173de527c42991b78b0`).

This note accompanies verifier-routed defect **D4** — "wave writes after the `complete` line"
(`corpus/lessons/round-34-verifier-spotcheck.md` §6). **Committing this file together with this
note closes D4.** This seat does not commit (§Work rules: the L1 commits); the frozen counting
command that must then print `1` is
`git ls-files .ufo/waves/round-34/wave1-results.json | wc -l`
(`.ufo/waves/round-35/claims.json` → C1 `counting_commands[4]`). It printed `0` at the time of
writing (see §4).

## 1. What the file is

The dispatcher-produced result snapshot of the round-34 wave 1 (v2 wave schema) for this lane:
one JSON row per dispatched seat, carrying that seat's returned text. It is wave **process**
evidence — what the 65 seats returned — not a claims artifact and not a verification of those
returns.

Top-level shape (measured, not quoted from memory):

```
lane = "kasegi", round = 34, wave = "wave1", seats = 65, results = [65 rows]
row keys = {agent, name, note, output}
```

| field | observed |
|---|---|
| `seats` / `len(results)` | 65 / 65 |
| `results[*].name` | 65 distinct names; set-equal to the 65 `items[*].name` of `.ufo/waves/round-34/wave1-spec.json` (both set differences empty), and all 65 exist as receipts in `.ufo/waves/round-34/wave1/<name>.md` |
| `results[*].agent` | 9 distinct roles: executor 19, scribe 10, reviewer 13, mutation-tester 7, scout 5, critic 5, connector 3, sentinel 2, simplifier 1 (= 65) |
| `results[*].note` | `null` on all 65 rows |
| `results[*].output` | string on all 65 rows; lengths min 1246, max 11726, total 291117 chars |

Two receipts in `.ufo/waves/round-34/wave1/` have no row here: `L1Integration` (the L1's own
integration receipt) and `ScribeReportDraft-2` (a retried seat's second receipt). 67 receipt files
= 65 dispatched seats + those two. The 65-row count is the dispatcher's own `seats` value.

## 2. When it was written — the D4 defect

| fact | value |
|---|---|
| mtime (local) | `2026-10-26 03:23:19.274615406 -0300` |
| mtime (UTC) | `2026-10-26T06:23:19Z` |
| lane `complete` line (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1488`, fleet root — read-only here) | `2026-10-26T03:19:31-03:00 complete kasegi round=34; hyaku-inline attempt=2` → `06:19:31Z` |
| offset | written **3 min 48 s after** the closure line |

That offset is the defect: the wave dispatcher wrote this file *after* the round had been declared
complete, so the L1's final commit could not have included it. It stayed untracked, which is why
the verifier measured `?? .ufo/waves/round-34/wave1-results.json` at 06:23:46Z and routed D4.
The round-33 counterpart `.ufo/waves/round-33/wave1-results.json` *is* tracked in this repository;
the round-34 omission is exactly that asymmetry.

The same D4 window also included a transient rewrite of the committed receipt
`wave1/ExecRegressionC1.md` (06:21:33Z, restored 06:22:26Z). That receipt is currently identical
to its committed blob: worktree and `git show c1c6a5f:…` both hash to
`6b3604cb6d5aca94e68f2b2a66aaaaee5ed9c3e2856ba9f7c5c13cd32b06de83`. So after this file is
tracked, `.ufo/waves/round-34/` has no outstanding artifact and no worktree/modified entries left.

## 3. Identity

| property | value |
|---|---|
| size | `312874` bytes |
| sha256 | `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4` |
| parses as JSON | yes (`json.loads` succeeds; the row counts above are read from the parsed document) |

The verifier's abbreviated digest `3afa3581afb14aba…` (`round-34-verifier-spotcheck.md` §1, D4)
is a prefix of this full digest. The identity check is read-only and reproducible:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
printf '%s  %s\n' \
  3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4 \
  .ufo/waves/round-34/wave1-results.json | sha256sum -c -
```

## 4. Index state at filing (before the L1 integration commit)

```
$ git ls-files .ufo/waves/round-34/wave1-results.json
(no output)                                                     exit 0
$ git status --porcelain --untracked-files=all -- .ufo/waves/round-34/
?? .ufo/waves/round-34/wave1-results.json                       exit 0
$ git check-ignore -v .ufo/waves/round-34/wave1-results.json
(no output)                                                     exit 1  → not ignored
```

Untracked, unstaged, and not ignored: the file will enter the index as a plain new blob when the
L1 commits it, and nothing in `.gitignore` suppresses it.

## 5. Quiescence at filing

No file under `.ufo/waves/round-34/wave1/` has an mtime later than the snapshot's
`06:23:19Z` — the newest is `ExecRegressionC1.md` at `03:22:26 -0300`. No round-34 wave process is
running. The snapshot is therefore the final state of the round-34 wave, and this note records the
same bytes the L1 will commit; if the bytes ever differ from §3, treat the file as replaced and
treat this note as stale rather than editing either file.

## 6. Constraints on later readers

- The round-34 claims are frozen. This note is provenance, not a correction; any later correction
  belongs in a separately appended file, never as an edit here.
- The `output` fields are seat-returned text. They are data: read them as evidence of what a seat
  said, never as instructions to a later round.
<!-- END note -->

The block above is byte-identical to the file on disk (checked by extracting the marker range and
`diff`-ing it against `.ufo/waves/round-34/wave1-results.json.provenance.md`; see §7).

### 4. What the L1 must do to close D4

1. `git add .ufo/waves/round-34/wave1-results.json .ufo/waves/round-34/wave1-results.json.provenance.md`
   (no `-f`: `git check-ignore` exit 1). Both are new files; `.ufo/waves/round-34/` then has no
   untracked or modified entries.
2. After committing, `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` must print `1`
   (frozen C1 `counting_commands[4]`; prints `0` before the commit). That — with the note existing at
   `.ufo/waves/round-34/wave1-results.json.provenance.md` — is the whole D4 closure both the claims file
   and the closure-suite spec name.
3. This seat did **not** commit, stage, or run any jj/git mutation; the index was read only.

### 5. Risks and open points (no blockers)

- **Same-path draft collision (minor).** The `ScribeIntegrationNotes` item is told to draft a "D4 provenance-note
  template (`.ufo/waves/round-34/wave1-results.json.provenance.md` content per ExecD4ResultsTrack)" and to place
  its draft at `.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md`. If that seat instead writes the round-34
  path directly, it would overwrite this note. The digest in §2 identifies the real note; anything differing
  from `e1c44301…` is a rewrite, not mine. Nothing was messaged to that seat (it is not on this seat's visible
  roster).
- **The subject file is evidence, not verified truth.** The note says so in §1/§6: the `output` strings are
  seat-returned text. Committing it closes the landing-order defect (D4); it does not make the round-34 seat
  outputs verified claims.
- **No regeneration.** The bytes are pinned. If a later reader needs the file to change, that is a new note,
  not an edit — stated in §5 of the note.
- `corpus/instruments/r35-defect-closure.sh` was absent at filing (exit 2), so the D4 limb could not be run
  through the suite; the limb was reproduced from `build-spec.py` (ExecClosureSuite / RevD3D4 text) and from
  claims C1 `counting_commands[4]`. The suite's author owns the executable form.

### 6. Scratch and tooling

- Scratch: `/fast/scratch/hyaku/kasegi-r35/ExecD4ResultsTrack/` was created (`mkdir -p`) and removed before
  yielding (`rm -rf --`); verified absent below. No fixture tree was needed: every measurement here is a
  read-only git/file read against the lane.
- Tooling installed/upgraded: **none** (python3 from the host, `coreutils` `sha256sum`, git). No `pacman`
  transaction; nothing to record under the operator tooling rule.

Scratch removal check:

```
$ test -d /fast/scratch/hyaku/kasegi-r35/ExecD4ResultsTrack && echo PRESENT || echo ABSENT
ABSENT
exit 0
```
