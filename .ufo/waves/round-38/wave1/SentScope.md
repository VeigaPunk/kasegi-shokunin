# SentScope — round-38 wave1 receipt

Seat: `SentScope` (sentinel, leaf). Lane `kasegi-shokunin`; round 38; base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims freeze
`9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; lane HEAD during audit
`700153593eb586c70a6499c8ca225ee4d673bc9b` ("round-38: wave1 spec + validated dispatch (73 seats, v2)").
Audit window 2026-10-26T18:35:54Z–18:41Z (round launch was 18:11:39Z = 15:11:39 -03;
claims frozen 18:17:40Z; incident at 18:29:11Z = 15:29:11 -03).

Item: audit the round's write scope and forbidden surfaces, then run the misroot sweep
read-only. Receipt only; no deliverable file and no lane edit. Every command below was
read-only git (`status`, `log`, `diff`, `cat-file`) or `find`/`stat`/`sha256sum`/`grep`;
no mutating git/jj command was run, no fleet-root or sibling file was written.

## 1. Planned lane write set — all contained in the lane

Source: `claims.json` + the 73 prompts in `.ufo/waves/round-38/wave1-spec.json` (paths
extracted by regex over every prompt). Every plan path is lane-relative; no prompt names a
write target outside `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

| Planned path (lane-relative) | State at audit | Action | Contained |
|---|---|---|---|
| `.ufo/waves/round-38/wave1/<SEAT>.md`, `<SEAT>.<suffix>` | 68 entries, untracked, 18:37Z | receipts + byte-exact deliverables | yes; no symlinks (`find -type l` empty); names match `<SEAT>[.<suffix>]` except the L1's own `swarm-registry.json` |
| `.ufo/waves/round-38/{wave1.ready,wave1.ready.dispatched,wave1-spec.json,wave1-dispatch.json,wave1-run.err}` | present, untracked | L1 dispatch evidence | yes |
| `.ufo/waves/round-38/claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt` | present; committed at freeze (`claims.json`) | frozen inputs | yes |
| `corpus/instruments/r38-closure.sh` (+ `r38-fixtures` if used) | absent | new suite (C1) | yes |
| `corpus/knowledge/csaf-vex-product-status-and-justifications.md` | absent | new entry (C2) | yes |
| `corpus/source-snapshots/round-38/{S055.txt,manifest.json}` | absent | new capture | yes |
| `corpus/lessons/round-38.md` | absent | new lesson | yes |
| `corpus/knowledge/considerthese-proposals-ledger.md` | 43 lines; `## Round-37 dispositions (appended 2026-10-26, R31 home)` at `:37` is an empty heading (D-F) | append rows (G7) | yes |
| `corpus/lessons/round-37.md` | 335 lines | append pending-marker resolutions (G3) | yes |
| `PROVINCE.md` (152), `SCORECARD.md` (1509), `SHONEN.md` (178), `SKILL.md` (1113), `LOG.md` (1692) | unchanged at audit | append-only (G1/G2/G5) | yes |
| `corpus/README.md` (454), `corpus/SOURCES.md` (118), `corpus/QUALITY.md` (278) | unchanged at audit | append-only | yes |
| `corpus/instruments/knowledge-expected.txt` (51) | unchanged | knowledge 49→50 driver | yes |
| `.ufo/waves/round-38/declared-blocks.txt` | absent | new (G1) | yes |
| `.ufo/waves/round-38/final-gates/all-gates.txt` | absent | new receipt at Y (G2) | yes |
| `.ufo/waves/round-38/c2-controls/junk-f21.md` | absent (delivery is `wave1/ExecC2Junk.junk-f21.md`, 983 B) | rejected junk twin | yes |
| `.ufo/waves/round-38/*-dispatch.json` → `*-results.json` | results absent | new (G4/D3) | yes |

Verify-none applies: the lane's protected ten-path set shows no churn yet, as expected
before landing:

```
$ git -C kasegi-shokunin diff --stat a173b0c2b98c5ae39599fa9be76027fbbead0b9e 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b -- SKILL.md PROVINCE.md SCORECARD.md LOG.md SHONEN.md corpus/QUALITY.md corpus/SOURCES.md corpus/README.md corpus/knowledge/considerthese-proposals-ledger.md corpus/lessons/round-37.md
(no output)
```

Lane writes observed since launch (mtime ≥ 15:11, `.git`/`.jj` excluded) are exactly:
`claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`,
`wave1-spec.json`, `wave1-dispatch.json`, `wave1.ready`, `wave1.ready.dispatched`,
`wave1-run.err`, the `wave1/` entries, and `.jj/repo` metadata from the L1's own two
commits (`9a10b02`, `7001535`). **No corpus/ or top-level lane file was touched**, and no
lane path exists outside `.ufo/waves/round-38/`:

```
$ git -C kasegi-shokunin status --porcelain
?? .ufo/waves/round-38/wave1.ready
?? .ufo/waves/round-38/wave1.ready.dispatched
?? .ufo/waves/round-38/wave1/
```

Deliverable scripts were spot-audited for the ExecNoHarm failure shape (relative writes
before `cd`): `ExecDeclaredBlocks.gen.sh` binds every write under `mktemp -d` honouring
`TMPDIR` and only `cd`s into scratch; `ExecFenceWalk.sh` writes only `$dir` fixtures
(`rm -rf` on exit); `ExecRefChecker.py` refuses a `--work` inside the lane and writes only
under `--work`/scratch. A grep for out-of-lane write operators across all `*.sh`/`*.py`
deliverables (`>`, `>>`, `tee`, `cp`, `mv`, `install`, `mkdir`, `touch`, `rm` targeting
`/home/vgpnk/Projects/{shokunin,shokuknow}`) returned nothing outside `kasegi-shokunin`.

## 2. The one planned out-of-lane write: the fleet report

- Target: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md` — **absent** now
  (`ls` → `No such file or directory`); parent dir exists and is tracked in the fleet repo.
- Precedent shape: `.ufo/reports/round-37/kasegi.md`, 11070 B, committed by hyaku
  (`3aa4ed4d`, `c6635628`). The round-38 report is the L1's sole allowed fleet-root write;
  dispatch evidence `.ufo/prompts/kasegi-round-38.md` (50696 B) was committed by hyaku at
  `44942bbe` (15:11:36 -03), i.e. at launch, before claims freeze.
- `ScribePendingResolutions` and `SimplReport` only *read* report paths; no seat prompt
  instructs a seat to write the report.

## 3. Forbidden-surface audit (fleet root, siblings, system paths)

Fleet repo is `tracked-clean=yes`, `index-clean=yes`; its only porcelain entry is an
unrelated untracked report. All recent mtimes are attributed to the hyaku driver, not to a
kasegi seat:

| Surface | Observed | Attribution | Verdict |
|---|---|---|---|
| `MANIFEST.json` | mtime 15:19:38, sha256 `abe3d0a0…c227` **=** `HEAD:MANIFEST.json` blob | hyaku commit `2df7532d` "rounds ledger: mado r44 closure" | clean (byte-identical) |
| `LOG.md` | mtime 15:29 (incident repair), sha256 `9342284d…47ed` **=** `HEAD` blob | ExecNoHarm repair (§4); content equals HEAD | clean |
| `SCORECARD.md` | mtime 15:29, sha256 `3f370f87…88b7` **=** `HEAD` blob | same | clean |
| fleet top level otherwise | no new entries; `PROVINCE.md`, `SHONEN.md`, `SKILL.md`, `corpus/` **absent** | — | clean |
| `templates/` | mtime 2026-10-19 21:22 | untouched | clean |
| `scripts/` | dir 2026-10-19; `scripts/hyaku/inline-dispatcher.py` 15:33:59 | hyaku commit `717d28da` (host-guard fix) | clean for lane; driver-owned change |
| `.ufo/state/` | `kasegi.report-baseline` 68 B, mtime 15:11:36 (pre-freeze); `disk-guard.log`/`inline-dispatcher.log` are live driver logs | hyaku driver (owner) | no seat write |
| `.ufo/watchdog.log` | mtime 15:20:26; kasegi entries end at `launch kasegi round=38` 15:11:39 | hyaku driver | no seat write |
| `.scratch/` | only `goal-20261026-hyaku-run9.md` 15:34:27 | hyaku commit `717d28da` | clean for lane |
| fleet `.ufo/waves/*kasegi*` | none | — | no misroot wave dir |
| `~/Projects/shokuknow` | newest file 2026-10-25 13:35; dirty tree is its own campaign, no file ≥ 15:11 | untouched by round 38 | clean |
| `~/Projects/*` outside shokunin | no kasegi/round-38/r38-named entry ≥ 15:11 | — | clean |
| `~/.omp/agent/{config.yml,mcp.json}` | 2026-10-26 00:50 / 2026-10-25 02:32 | operator-owned, untouched | clean |
| PATH dir `~/.local/bin` | no entry ≥ 15:11 | — | clean |
| sibling lane repos (`*/` with `.git`) | 9 dirty repos, 38 dirty entries at 18:39Z (kaidoku 3, kengaku 4, mado 2, souji 9, tabi 7, tameshi 7, tsukuroi 6; recount 18:44Z: 44 as sibling seats write live); content scan of every dirty file for `kasegi` matched only this lane's own `wave1.ready` | other lanes' rounds | clean |
| fleet `.ufo/waves/*/*-scratch/` | none created ≥ 15:11 | — | clean |

Read-only cross-surface execution: claim C2's census command runs
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … kasegi`.
`validate` emits to stdout (`emit()` writes a file only with `--out`, which the claim does
not pass; selftest is the only mode that touches `mktemp -d`), so this is a read-only touch
of a forbidden-surface script, not a write.

## 4. Misroot sweep (read-only, as instructed)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
?? .ufo/reports/round-48/tameshi.md
```

That is the complete untracked list at 18:39Z. Its content does **not** name kasegi round
38 — and it is another lane's in-flight round-48 report (mtime 14:23:39, before this round
launched):

```
$ grep -qiE 'kasegi|round[- ]38|r38' .ufo/reports/round-48/tameshi.md; echo $?
1
```

No other untracked file exists in the fleet root, so the answer to "any untracked file
whose content names kasegi round 38" is: **none** (report-only; nothing to move).

Caveat that makes this sweep insufficient on its own: the fleet `.gitignore` hides
`*-shokunin/`, `.ufo/state/*`, `.ufo/watchdog.log`, `.tower/` and `.ufo/waves/*/*-scratch/`,
so lane-clone and ignored-surface writes are invisible to that porcelain. I compensated by
(a) `git status` in every sibling lane repo, (b) a content grep of all 38 dirty sibling
files present at 18:39Z (the count drifts as other lanes write), (c) mtime attribution above, (d) a `find` for `*kasegi*|*round-38*|*r38*` files under
`/home/vgpnk/Projects` since 15:11 (only `kasegi-shokunin`'s own `wave1/` and the expected
fleet `.ufo/prompts/kasegi-round-38.md`, `.ufo/state/kasegi.report-baseline`; one
`kaidoku-shokunin/.ufo/waves/round-40/…/r38-c2-counter-at-base.json` is kaidoku's own
round-38 counter artifact and names no kasegi path).

## 5. Incident: the round's one real write-scope breach (already contained)

**Severity: medium-high, transient** — two tracked fleet ledgers truncated, eight fleet
paths created, fully repaired; no lane bytes lost; a conformance fix landed.

**Exploit path.** Seat `ExecNoHarm`'s fixture driver helper wrote relative paths *before*
`cd` into its scratch fixture, with the process cwd inherited as
`/home/vgpnk/Projects/shokunin`. At **15:29:11 -03 (18:29:11Z)** it truncated fleet
`LOG.md` (to 22 B) and `SCORECARD.md` (to 51 B) and created fleet
`PROVINCE.md`, `SHONEN.md`, `SKILL.md` and
`corpus/{QUALITY.md,SOURCES.md,README.md,knowledge/considerthese-proposals-ledger.md,lessons/round-37.md}`.
That is exactly the delivery shape the round is fixing (D-A pastes plus unguarded cwd), and
it reproduced it one level up: a seat trusted its own cwd instead of asserting the toplevel
before writing.

**Evidence.** Self-reported in `wave1/ExecNoHarm.md` §"Incident" (lines 224–246); fleet
dispatcher incident record in `.scratch/goal-20261026-hyaku-run9.md` (commit `717d28da`,
15:34:36, "append host guard to every seat prompt (kasegi r38 ExecNoHarm fleet-root
write …)"). Repair verified independently by me, not taken on the seat's word:

```
$ for p in PROVINCE.md SHONEN.md SKILL.md corpus corpus/instruments; do [ -e "$p" ] && echo PRESENT || echo absent; done
absent (×5)
$ sha256sum LOG.md SCORECARD.md MANIFEST.json vs git cat-file blob HEAD:<p>
LOG.md         file=9342284d26a56e17cd09a15c17d14432d11c2a2ac2eeec882d79311ba6ae47ed head=9342284d…47ed
SCORECARD.md   file=3f370f8705fe52f190263a5d0bb005b4766888cf3352c0f364186953056388b7 head=3f370f87…88b7
MANIFEST.json  file=abe3d0a0b5a4cf3b5440fed14275a083c097c874fbd9b392732078c934d1c227 head=abe3d0a0…c227
$ git -C /home/vgpnk/Projects/shokunin diff --quiet HEAD && echo tracked-clean=yes
tracked-clean=yes
```

The last fleet ledger commit before the incident, `2df7532d` (15:19:38), predates 15:29:11,
and the tree is byte-identical to HEAD, so no committed ledger bytes were lost.

**Impact.** If unrepaired, the fleet front door (`LOG.md`/`SCORECARD.md`, tracked and
read by every lane's front-door gates) would be corrupted in the shared repo, and eight
stray front-door-shaped files would make a fleet-level `corpus/` look plausible to the next
round's gates. Contained: repaired within ~3 minutes, no lane bytes affected, the incident
did not weaken any round-38 claim (the lane's ten protected files are still byte-identical
across base→freeze, §1).

**Residual risk (unverifiable, stated as such).** Any *uncommitted* fleet `LOG.md`/
`SCORECARD.md` bytes present at 15:29:11 are unrecoverable; both files now equal their HEAD
blobs exactly and HEAD's commit predates the write, so the loss window is empty for
committed history only. Writes that a seat performed and deleted elsewhere, and writes into
`.gitignore`d sibling surfaces, leave no trace and are outside what any local sweep can
prove.

**Smallest remediation (landed; no further edit needed from this seat).** The dispatcher
now appends a host guard to every seat prompt (commit `717d28da`): cwd is the fleet root →
`cd` to scratch before any command that writes a relative path; assert
`git rev-parse --show-toplevel` in fixtures before mutations; no PATH-dir writes; no
fleet-root tracked-file writes. The guard is present verbatim in this seat's own prompt
("Host guard (orchestrator; applies to every seat)"). Closure should cite `717d28da` as the
conformance evidence; a future seat prompt without the guard would be the regression to
test for.

## 6. Findings summary

| # | Severity | Finding | Status |
|---|---|---|---|
| F1 | medium-high (contained) | `ExecNoHarm` fixture driver wrote relative paths from cwd = fleet root: truncated `LOG.md`/`SCORECARD.md`, created 8 fleet paths at 18:29:11Z | repaired; verified byte-identical to HEAD; host guard landed `717d28da` |
| F2 | low (process) | Fleet-root porcelain cannot see lane-clone or `.gitignore`d writes, so the instructed sweep alone would miss a repeat of F1 | compensated here by per-repo status + content + mtime attribution; recommend the sweep be documented as one limb of three |
| F3 | informational | `ScribePendingResolutions`/`SimplReport` name report paths only as reads; the sole out-of-lane write is the L1's report, absent as expected | no action |
| F4 | informational | `.ufo/state/kasegi.report-baseline` (ignored, 68 B) predates the freeze and belongs to the hyaku driver; `.ufo/state` is forbidden to seats but invisible to porcelain | attribution by mtime/owner only |

No write-scope violation by any other seat: lane writes are confined to
`.ufo/waves/round-38/`, no corpus/top-level lane file changed, no sibling repo, shokuknow,
`~/.omp`, PATH dir or fleet surface holds a kasegi-round-38 write besides the repaired F1.

Tooling: none installed or upgraded (no pacman; nothing via uv/npx/`~/.local/bin`).
Scratch: `/fast/scratch/hyaku/kasegi-r38/SentScope/` was created per spec and removed after
this receipt was written (no work files were needed beyond the shell).
