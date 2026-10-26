# ExecArchiveNoHarmMirror — round-39 wave1 receipt

Seat `ExecArchiveNoHarmMirror` (executor, leaf; axis depth:verifiability). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `480b1a505a2dfc14a4f718d16d63808247214d0a`,
claims freeze `dcd31701720a6a4929a32471a62011ed87103421`). Writes: this receipt, the one named
deliverable, and `/fast/scratch/hyaku/kasegi-r39/ExecArchiveNoHarmMirror/` (removed before yield;
G6-clean). No lane, fleet, sibling-lane or source-tree file was written; no mutating git command ran
outside a scratch fixture; no tool was installed; no pacman transaction.

## 1. What the mirror is

`mirror = git archive 480b1a505a2dfc14a4f718d16d63808247214d0a` (7,421 files) + every byte-exact
wave1 deliverable present in `.ufo/waves/round-39/wave1/` at capture, mapped to its lane path by
`compose_mirror.py` (§6). Registration points used: the registry table after row `S055` (four rows in
id order), the search-log list after its last bullet, and end-of-file for every append.

| object | value |
|---|---|
| capture UTC | `2026-10-26T20:01:37Z` |
| wave1 files captured | 229 (`find . -type f`, excluding `swarm-registry.json` and this seat's own files) |
| wave1 capture manifest | scratch file `wave1_manifest_capture.txt` (sorted `path\tbytes`, removed with the scratch dir; recomputable from the wave dir at capture); sha256 `915aad790ae7224aef918d631f9c4563a38dded18b7c355ef6d582d4f2d600ad` |
| lane tip at capture | `1a139e0` (`round-39: wave1 integration (C1 suite + C2 F22/S057; corrections, criteria, ledger, distance block)`) |
| base export | 7,421 files |

Deliberately outside the mirror (not wave1 byte-exact deliverables): `.ufo/waves/round-39/declared-blocks.txt`,
`final-gates/all-gates.txt`, `*-dispatch.json`/`*-results.json`, `corpus/instruments/knowledge-expected.txt`
(the L1's recheck expected-list update), the assembled `corpus/lessons/round-39.md`, the `SCORECARD.md`
`## Round 39` section, the `LOG.md` round-39 entry and the `SKILL.md` `r39-closure.sh` row — all authored
by the L1 at landing (runbook B7/B8). `swarm-registry.json` and this seat's own artefacts are excluded.

## 2. Deliverable

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-39/wave1/ExecArchiveNoHarmMirror.no-harm.txt` | 536 | 53855 | `ed1f074642753bf93e3488e413dd40293a1fb2cdc2f161b0f2a575d9c58a1f18` |

It is the raw `verify.sh` transcript (commands printed with `$`, then results), no notes added.

## 3. The three required transcripts (full text in the deliverable)

### A — pure addition: every changed lane file only adds lines

`git diff --no-index --numstat base mirror` (symlinks compared as link blobs, so the export's 58
fixture symlinks cannot masquerade as content changes):

```
changed_files=9 added_files=233 added_lines=24114 removed_lines=0 deleted_files=0
```

Per-file lane verdicts (`ADD-ONLY <path> added=N removed=0`):

| path | added | removed | note |
|---|---|---|---|
| `LOG.md` | 1 | 0 | append; base bytes identical prefix |
| `PROVINCE.md` | 1 | 0 | append; base bytes identical prefix |
| `SCORECARD.md` | 28 | 0 | two appends (2 + 26); base bytes identical prefix |
| `SHONEN.md` | 72 | 0 | two appends (2 + 70); base bytes identical prefix |
| `corpus/QUALITY.md` | 16 | 0 | append; base bytes identical prefix |
| `corpus/README.md` | 28 | 0 | append; base bytes identical prefix |
| `corpus/SOURCES.md` | 9 | 0 | 4 registry rows + 1 search-log bullet inserted mid-file, 4 registry-change bullets appended; insert-only (removed=0), so not a byte prefix |
| `corpus/knowledge/considerthese-proposals-ledger.md` | 27 | 0 | append; base bytes identical prefix |
| `corpus/lessons/round-38.md` | 2 | 0 | append; base bytes identical prefix |

New files (pure addition by definition): `corpus/instruments/r39-closure.sh` 1793 lines,
`corpus/knowledge/cisa-when-to-issue-vex.md` 144 lines, `corpus/source-snapshots/round-39/S057.txt`
275 lines, `corpus/source-snapshots/round-39/manifest.json` 74 lines, plus 229 wave1 evidence files
(receipts, deliverables, fixture subtrees). `removed_lines=0 deleted_files=0`.

### B — suite syntax

```
$ bash -n mirror/corpus/instruments/r39-closure.sh
bash-n exit=0
1793 lines; sha256 2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b; mode -rwxr-xr-x
```

The landed copy at `1a139e0` is byte-identical (`2856a210…`) with mode 644; only the executable bit differs.

### C — declared blocks vs the mirror's appended tails

`.ufo/waves/round-39/declared-blocks.txt` appeared during this seat's run (L1 landing, sha256
`07e63e96c523871854bc675f2e105292afd2fb52fe551f4b79314c6e31f5cc5f`):

```
PROVINCE.md 2 fa2dd99f2791e022305fe1ee759a53ba514d7d4ef2e89a597cae8a41fe70d3d7
corpus/README.md 28 a59d42ccaea20fc78bc2ff2a55c5fead32ac43616df8c606c51c7ac8ebec2c8f
```

Raw cat-concat mirror tails: `PROVINCE.md` 1 line / `bd8dbc09…`, `corpus/README.md` 28 lines /
`a8aa90a2…`. The delta is exactly the landing convention: the L1 writes each append with one blank
separator line and no trailing blank line. Applying that convention to the same deliverable bytes
reproduces the declared numbers exactly, and the landed commit `1a139e0` carries exactly those bytes:

```
DECL-NORMALIZED PROVINCE.md declared_lines=2 block_lines=2 want_sha=fa2dd99f… block_sha=fa2dd99f… ok
DECL-NORMALIZED corpus/README.md declared_lines=28 block_lines=28 want_sha=a59d42cc… block_sha=a59d42cc… ok
LANDED PROVINCE.md declared_lines=2 added_lines=2 tail_sha=fa2dd99f… ok
LANDED corpus/README.md declared_lines=28 added_lines=28 tail_sha=a59d42cc… ok
```

So the declared whole tails equal the added-line counts and the last-N-line digests of the intended
after-state; the raw-concat one-line delta is the boundary blank, not a byte mispaste (D-A class clear).

## 4. Supplementary checks (beyond the item, same evidence stream)

1. **Landed integration is pure addition.** `git -C <lane> diff --numstat 480b1a5 1a139e0 -- . ':!.ufo'`
   → 14 paths, every row `<add>\t0\t<path>`, total deleted lines 0 (LOG 2, PROVINCE 2, SCORECARD 30,
   SHONEN 3, QUALITY 17, README 28, SOURCES 10, knowledge-expected 1, r39-closure 1793, F22 entry 144,
   ledger 28, lesson-38 2, S057 275, manifest 74).
2. **The landed suite's own G1 grades the mirror+declarations GREEN.** Fixture: scratch clone-shared of
   the lane checked out at base, mirror overlaid, `declared-blocks.txt` added, one commit, then
   `bash r39-closure.sh --export-ref HEAD --lane <fixture> --work <scratch> --scratch-root <empty>`
   (fixture toplevel asserted equal to the fixture dir before committing):

```
G1 payload=declared=2,valid=2,front-doors=2,tail-match=2,pure-append=1,paths=1,province-fence=closed,readme-fence=closed,corrections-outside=0,corrections-inside=0,corrections-declared=1,diff-read=ok closed=1
G3 payload=added-quotes=0,covered=0,uncovered=0,report-only=0,diff-read=ok closed=1
G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1
G7 payload=section=1,after-round38=1,correction=1,rows=7,proposal-1=1,proposal-3=1 closed=1
G8 payload=pin-ref=2387dcf6ccfefcfb703783387b9aade8fc82abfa,pinned-sha=1,export-copy=1,r37-copy=1,r37-closed=1,r37-exit=0 closed=1
closed=5/8 exit=1
```

   G2/G4/G5 are red only because a wave1-only mirror lacks the L1-authored receipt, dispatch/results and
   `## Round 39` SCORECARD section (observed payloads: `receipt=0`, `dispatches=0`, `round39-section=0`);
   that is scope, not a defect in the mirror. Note `corrections-outside=0` is *accepted* by the landed G1:
   the check reds only a correction inside an open fence or outside the declared tail.
3. **Reference-model divergence, cleared.** The wave1 fixture `ExecWholeTailFixture.fixtures/g1-check.sh`
   requires >= 1 outside `Correction (round 39)` line per front door; claims C1 and the landed suite
   require none (`corr_decl` stays 1 with zero corrections). Both real front doors carry 0 corrections
   (`fence-model=backtick+tilde state=closed outside=0 inside=0` on each). A suite copying the fixture's
   stricter rule would red G1 at the real head; the landed suite does not, and its G1 is green above.
4. **Mirror vs landed commit (editorial only).** `git diff --no-index mirror <export of 1a139e0>` names
   10 paths, all non-.ufo: PROVINCE +1, LOG +1, QUALITY +1, ledger +1 (blank separator), README +1/-1
   (trailing blank moved to the separator), SCORECARD +3/-1 (blank-line reflow around the correction),
   SOURCES +3/-2 (row/search-log blank placement), SHONEN +1/-70 (HEAD predates `ScribeShonen`'s append and
   reformats the correction block boundary),
   `knowledge-expected.txt` +1 (L1 list update), `r39-closure.sh` 0/0 (mode only). No base line is lost.

## 5. Findings for the L1

1. **Generate `declared-blocks.txt` after the final front-door state** (runbook B7 already does): the
   declared numbers describe the *landed* tails (blank separator, no trailing blank), not raw
   `cat block >> file` concatenation — a declaration copied from the raw blocks would lose PROVINCE's
   separator line and the README digest. Verified equal to `1a139e0` and to the normalized blocks.
2. **Commit `ScribeShonen.shonen.append.md`**: it landed after `1a139e0`; HEAD's `SHONEN.md` carries 3
   added lines where the mirror carries 72. Re-run the no-harm pass after that commit.
3. **Wave1-only mirror cannot satisfy G2/G4/G5**: the L1's landing must supply the receipt,
   dispatch/results and `## Round 39` section, and the `SKILL.md` `r39-closure.sh` row (mirror has no
   `SKILL.md` change because no wave1 seat delivers its bytes). The L1's own no-harm run must include
   `SKILL.md` and `knowledge-expected.txt`.
4. The landed suite is invoked with `bash`, so its 644 landing mode is safe; the wave1 deliverable is 755.

## 6. Deliverable → lane path mapping used (§1), with digest

| deliverable | lane path | action | lines | sha256 |
|---|---|---|---|---|
| `ExecFrontierCapture.S057.txt` | `corpus/source-snapshots/round-39/S057.txt` | new | 275 | `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f` |
| `ExecFrontierCapture.manifest.json` | `corpus/source-snapshots/round-39/manifest.json` | new | 74 | `432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659` |
| `ScribeEntryF22.entry.md` | `corpus/knowledge/cisa-when-to-issue-vex.md` | new | 144 | `5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29` |
| `ExecSuiteBuild.r39-closure.sh` | `corpus/instruments/r39-closure.sh` | new (755) | 1793 | `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` |
| `ScribeProvinceF22.province.append.md` | `PROVINCE.md` | append | 1 | `bd8dbc096b1a7190811a52ec1a78171524af436d448bcc85c8f3208540dcfc7d` |
| `ScribeFrontierF22.readme.append.md` | `corpus/README.md` | append | 28 | `a8aa90a29215c1ef73e76e7beec8e9dee7b96d3d6f3f00afd4d84a7625b22d25` |
| `ExecQualityCriteria.quality.append.md` | `corpus/QUALITY.md` | append | 16 | `a89eaa2de29dde8068ba4ab2b41ab9b9c2f0d17c718cdaa622ec7738742b368d` |
| `ExecCorrectionsR2.round38-lesson.append.md` | `corpus/lessons/round-38.md` | append | 2 | `895547931464ba115bae0620a771766dab35fb36daa329435e7310b1b5e83474` |
| `ExecCorrectionsR2.log.append.md` | `LOG.md` | append | 1 | `b9cee1ecfa138ec8f9da8a1e2401ae4e588dfb4c74181bb036e57ebddc4e2b3e` |
| `ExecCorrectionsR2.scorecard.append.md` | `SCORECARD.md` | append | 2 | `0251af27d9336fe1b93db705dacc38ab0a77df09331ed9a0ae7761df14bada55` |
| `ExecConsiderthese.scorecard.append.md` | `SCORECARD.md` | append | 26 | `a8c7af5293dc801a35fe46443f4f5b1bb6c757f2826d544b35db62f39398d707` |
| `ExecCorrectionsR2.shonen.append.md` | `SHONEN.md` | append | 2 | `79890f628869257df313f97aafd7359d4e6f9dc07af3de2eea5b756326deb23d` |
| `ScribeShonen.shonen.append.md` | `SHONEN.md` | append | 70 | `fa252112b97fd5d012d77c61d11d9489609b0d948459ca265b68924a0ae12666` |
| `ExecConsidertheseLedger.ledger.append.md` | `corpus/knowledge/considerthese-proposals-ledger.md` | append | 27 | `8becfdf77c472af27234fb783f7612ad1a7b767140ff0270175bb2eac3fe3c70` |
| `ScribeRowsRejected.registry-changes.md` | `corpus/SOURCES.md` | append | 4 | `86c4ab729473481226184e197c77919432836e5c8367960bca4ac30f9b39488c` |
| `ScribeRowS057.row.md` | `corpus/SOURCES.md` | insert after S055 | 1 | `176762ea6a22ecffcd28e926ae026044bbbf59c40c530cf53a00c741e5d3c8d9` |
| `ScribeRowsRejected.S056.row.md` | `corpus/SOURCES.md` | insert after S055 | 1 | `e3b789f2f7c249c82a71b498ef498cdf8afa43407a3eae59895ad0da86a69ceb` |
| `ScribeRowsRejected.S058.row.md` | `corpus/SOURCES.md` | insert after S055 | 1 | `57f1ab24f58bc512301226d7fe8e8e48ca4bd759474db249c90d6909ea3f87bb` |
| `ScribeRowsRejected.S059.row.md` | `corpus/SOURCES.md` | insert after S055 | 1 | `faf60f0194690c91a6db77d8c6523e4f71034e886426619059ff3b0b80d5cb47` |
| `ScribeSearchLog.searchlog.append.md` | `corpus/SOURCES.md` | insert at end of Search log | 1 | `400d393392d0dfb9e155acd5885a8714ab4269661119380ec270cb8a2b74222e` |

All wave1 receipts and evidence files are copied byte-for-byte into `mirror/.ufo/waves/round-39/wave1/`
(229 files at capture).

## 7. Reproduction

```
S=/fast/scratch/hyaku/kasegi-r39/ExecArchiveNoHarmMirror
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive \
  480b1a505a2dfc14a4f718d16d63808247214d0a | tar -x -C $S/base
python3 $S/compose_mirror.py     # prints ACTION/SKIP; skips absent deliverables, never invents
bash $S/verify.sh                # A/A2/A3 pure addition, B bash -n, C declared tails, C2 landed+normalized
```

`verify.sh` exits 0 with `no-harm-mirror: OK` on the capture in §1; the transcript is the deliverable.

## 8. Housekeeping

- Disk guard green before the pass (`/fast/scratch/hyaku` 610.5G free, 24% used); no heavy pass under a red guard.
- Scratch `/fast/scratch/hyaku/kasegi-r39/ExecArchiveNoHarmMirror/` (base export, mirror, fixture clone,
  work dirs) removed before yield — no kasegi-r39 scratch entry from this seat survives (G6). The capture
  manifest named in §1 was scratch-resident; its digest is recorded above, and the per-file line counts are
  in the deliverable's transcript A.
- Only read-only git: `archive`, `rev-parse`, `log`, `diff`, `cat-file`, `merge-base` (inside the landed-suite
  fixture). The one fixture (`fixture-head`) asserted `git rev-parse --show-toplevel` == its own dir before
  `checkout`/`add`/`commit`, and used per-command `-c user.name/-c user.email` only.
- No installs, no PATH writes, no pacman, no host-service restart, no `agent://all` message, no subagents.
