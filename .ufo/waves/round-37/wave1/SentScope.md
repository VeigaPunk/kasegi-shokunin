# SentScope — round-37 write-scope audit + pre-filing guardrail checklist

Seat: SentScope (sentinel, leaf — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`;
claims-erratum-1 `b362068`; lane HEAD at measurement `b362068195d5489aa94b31e6ec8f880c367e0ba0`, detached).
Axes owned: depth:verifiability, coverage. Milestone: round-37.

Measurement window 2026-10-26T17:05–17:30Z (14:05–14:30 local, `-03:00`). Method: read-only
`git status/diff/show/ls-tree/ls-remote/reflog/worktree`, `sha256sum`, `stat`, `find`, `grep`, `strings` on
`.jj/repo/op_store`; no `jj` binary invocation (a bare `jj` call snapshots the working copy — see F-6), no
network fetch, no tool install/upgrade, no pacman. This seat wrote only this receipt and its scratch
(`/fast/scratch/hyaku/kasegi-r37/SentScope/`, removed before yielding). It did **not** repair the live
defects below: remediation belongs to the L1, and repairing them would itself be a lane write outside this
seat's scope.

## Verdict

The round's write plan is enumerable and bounded: **22 lane path classes + 1 fleet path**. Two of them are
already **red as measured**, both in the VCS-containment layer rather than in the claim content:

- **F-1 (HIGH, live) — frozen round-36 evidence was rewritten during round 37.**
  `.ufo/waves/round-36/wave1/ScribeConsiderthese.md` is `M` in the lane worktree: 198 → 236 lines,
  `sha256 840e25ef…` → `198fbdca…`, `+38 −0`, adding `## 8. Post-integration addendum (appended
  2026-10-26T17:13Z, read at lane head b362068)`. The file is frozen history (landed `e666d90`), and no
  round-37 seat spec authorises writing it: ScribeConsiderthese's item says *draft*
  `corpus/considerthese-ledger.md`, and the universal seat write scope is that seat's own round-37 receipt.
- **F-2 (HIGH, latent) — the lane helper's pathspec scope is coarser than the round's scope.** `jj-lane.sh`
  refuses `.git`, `.jj`, `.ufo` exactly, `.ufo/state*`, `.ufo/watchdog.log` (`scripts/hyaku/jj-lane.sh:506-517`)
  and then only requires that every changed path be covered by the requested pathspec
  (`:522-556`). A commit requested as `-- .ufo/waves` would therefore commit F-1's round-36 edit and pass
  validation.

The plan is otherwise sound, but five scope-precision gaps (F-3–F-7) would let a green filing sit beside a
false or unverifiable statement. §5 is the checklist the L1 must run before filing; G2 fails today.

## 1. Measured baseline (this seat, read-only, 17:05–17:30Z)

| # | quantity | measured value | command |
|---|---|---|---|
| 1 | lane HEAD / remote tip | `b362068195d5489aa94b31e6ec8f880c367e0ba0` = `refs/heads/master` @origin | `git rev-parse HEAD`; `git ls-remote origin refs/heads/master` |
| 2 | lane tracked tree | **1 dirty file** — the round-36 receipt in F-1 (`git status --porcelain -uall \| grep -v '^?? .ufo/waves/round-37/'` → exactly that one ` M` line) | `git status --porcelain -uall` |
| 3 | lane untracked | 60 entries, all under `.ufo/waves/round-37/` (50 `wave1/*.md` + `wave1/swarm-registry.json`, `assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}`, `wave1-plan.err`, `wave1-run.err`, `wave1.ready`, `wave1.ready.dispatched`) | `git status --porcelain -uall` |
| 4 | `claims.json` integrity | `sha256 570c1d2c3f50723d161387283d4e4100f8f76e5aef2f270b70ce59f51fa778a7`, **identical** to `224df74`'s blob | `sha256sum .ufo/waves/round-37/claims.json`; `git show 224df74:… \| sha256sum` |
| 5 | C2 before-state | frontier **19**, SOURCES rows **53**, `corpus/knowledge/*.md` **48**, `knowledge-expected.txt` 48 entries (50 lines = 2 comment + 48), harness `expected=48` | the claim's own counting commands |
| 6 | E13 target | `SKILL.md:1111` row `r36-closure.sh`, type cell literal `gate\|probe` | `grep -n 'r36-closure.sh' SKILL.md` |
| 7 | E12 trap | `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b` occurs at `SCORECARD.md:1492` (inside the **round-36** append) | `grep -rn e666d902 SCORECARD.md corpus/lessons/*.md` |
| 8 | D2 false path | `corpus/instruments/r36-fixtures/` absent: 0 tree entries, no directory on disk | `git ls-tree -r HEAD --name-only \| grep -c r36-fixtures`; `ls -d …` |
| 9 | scratch root | `/fast/scratch/hyaku/kasegi-r37/` holds **24** entries at 14:17: 22 seat dirs + `build-spec.py` (file, 56 599 B) + `l1prep/` (dir) | `ls -la /fast/scratch/hyaku/kasegi-r37` |
| 10 | jj state | 617 ops, **1** op head (`1c57bcbf…`, description `push bookmark master to git remote origin`); op descriptions are readable with `strings` | `ls .jj/repo/op_store/operations \| wc -l`; `strings …` |
| 11 | fleet worktree | 17:0x: `?? k2.tsv` `?? k2s.tsv` (248 B / 40 B, mtime 14:04, untracked, not ignored); 17:16: **both gone**, replaced by ` M .scratch/goal-20261026-hyaku-run9.md` (+18 −0) | `git -C /home/vgpnk/Projects/shokunin status --porcelain` |
| 12 | fleet forbidden digests | `MANIFEST.json ecc50774846781402e91255759fd46119e1e53807881ff7ef44f103d4345b598`; `templates/`+`scripts/` tree `465f4ae652f503b68d94f4fa27a0d049ff27215f142b5714788e4a79333ea4fa`; `.ufo/l0-questions.md 67b2ead708ded12ce8a5e17062b7e9030c2f77b3905d7c4cbb3c639950a91171` (178 lines) | `sha256sum`; `git ls-tree -r HEAD -- templates scripts \| sha256sum` |
| 13 | operator-owned config | `~/.omp/agent/config.yml e709890e…`; `~/.omp/agent/mcp.json 4e8746da…` | `sha256sum` |
| 14 | repo layout | 21 lane repos under the fleet root, **every** `rev-parse --show-toplevel` equals its own path (no misroot); 21 `.git`, 21 `.jj`; no other nested repo at depth ≤ 3 | §5 G1 |
| 15 | sibling dirt (concurrent, not round-37's) | kasegi 7 · kaidoku 18 · kengaku 8 · mado 4 · tabi 9 · tameshi 5 · tsukuroi 6 · others 0; shokuknow 1918 | per-repo `status --porcelain \| wc -l` |
| 16 | fleet dispatch artifacts (already landed, not this round's) | `.ufo/prompts/kasegi-round-37.md` @`041ed81d`; MANIFEST rounds entry @`238b93b9` (hyaku, **non-author**) | `git show --stat` |

## 2. Allowed write manifest

### 2.1 Lane repo `kasegi-shokunin` (the only lane a seat may write)

`N` = new file, `M` = modify existing. Every path is anchored in the frozen claim text or in the seat items;
anything not listed is out of scope by default.

| id | path | kind | anchor | lands at |
|---|---|---|---|---|
| A01 | `corpus/instruments/r37-closure.sh` | N | C1 predicate; E14 shape | L1 integration |
| A02 | `.ufo/waves/round-37/final-gates/all-gates.txt` | N | C1 E10 | L1 integration |
| A03 | `SKILL.md` | M | C1 E3 (append Round-37 registry section) + **E13** (edit `:1111` r36-closure.sh type cell + verdict map exit 2) | L1 integration |
| A04 | `LOG.md` | M | C1 E11 (`## Round 37` entry naming the false `corpus/instruments/r36-fixtures/` path) | L1 integration |
| A05 | `SCORECARD.md` | M | C1 D1/D2 placeholder replacement + E12 (`c20300df…` = `anchor ancestor`; no `e666d902` inside the round-37 section) | L1 integration |
| A06 | `corpus/lessons/round-37.md` | N | C1 E12, M37-1..M37-5, considerthese dispositions | L1 integration |
| A07 | `corpus/QUALITY.md` | M | C1 E7 (supersedes R22/R23 rows) + R30/R31 | L1 integration |
| A08 | `corpus/considerthese-ledger.md` | N | non-claim (proposal 7 → R31) — **path ambiguity, F-4** | L1 integration |
| A09 | `corpus/README.md` | M | C2 F20 frontier row 19→20 (frontier table `:389` region) | L1 integration |
| A10 | `corpus/SOURCES.md` | M | C2 S054 row (13 fields) | L1 integration |
| A11 | `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | N | C2 entry, cites `source: S054` | L1 integration |
| A12 | `corpus/instruments/knowledge-expected.txt` | M | C2 48→49 entries | L1 integration |
| A13 | `corpus/source-snapshots/round-37/S054.txt` | N | C2 capture | L1 integration |
| A14 | `corpus/source-snapshots/round-37/manifest.json` | N | C2 capture manifest (url per claims-erratum-1) | L1 integration |
| A15 | `PROVINCE.md` | M | C2 F20 amendment, end-of-file append | L1 integration |
| A16 | `SHONEN.md` | M | calibration record (L1 appends per ScribeShonen receipt) | L1 integration |
| A17 | `.ufo/waves/round-37/wave1/*.md` | N | 64 seat receipts (this file is one) | as seats yield |
| A18 | `.ufo/waves/round-37/wave1/swarm-registry.json` | N | wave bookkeeping | dispatcher |
| A19 | `.ufo/waves/round-37/claims-erratum-N.md` | N | claims rule: corrections are **appended files**, never edits to `claims.json` | L1 |
| A20 | `.ufo/waves/round-37/kasegi-r37-build-results.json` | N | wave results (r36 analog `kasegi-r36-build-results.json`) | L1 |
| A21 | `.ufo/waves/round-37/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` | N | non-claim evidence, already on disk | L1 |
| A22 | `.ufo/waves/round-37/{wave1-spec.json,wave1-dispatch.json,wave1-plan.out,wave1-plan.err,wave1-run.err,wave1.ready,wave1.ready.dispatched}` and `c2-controls/junk-f20.md` | N | wave evidence / C2 junk control | L1 |

Already committed and therefore **read-only**: `.ufo/waves/round-37/claims.json`,
`c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`, `claims-erratum-1.md`.

### 2.2 Fleet repo `/home/vgpnk/Projects/shokunin` (exactly one path, filed last)

| id | path | kind | anchor |
|---|---|---|---|
| B01 | `.ufo/reports/round-37/kasegi.md` | N | lane report convention (11 sibling reports tracked in `.ufo/reports/round-37/`; `kasegi.md` absent) |

The rounds ledger `MANIFEST.json` is **not** part of the round: admission is a non-author hyaku step
(`238b93b9` appended 38 lines for r36). An L1 write there would both violate the non-author rule and corrupt
the admission record.

## 3. Forbidden surfaces

| surface | why | verification |
|---|---|---|
| lane `.git/**`, `.jj/**` | repo internals; helper refuses them (`jj-lane.sh:508-510`) | G5 |
| lane `.ufo/state/**`, `.ufo/watchdog.log` | driver runtime; helper refuses them (`:513`) | G5/G10 |
| `.ufo/waves/round-37/claims.json` | frozen; corrections are new `claims-erratum-N.md` files | G6 |
| `.ufo/waves/round-36/**` and every earlier wave dir | frozen prior-round evidence — **currently violated (F-1)** | G2/G7 |
| `corpus/instruments/r36-fixtures/` | the *false* path D2/E11 corrects; creating it falsifies the correction | G13 |
| `corpus/instruments/{r36-closure.sh,r35-*,limb-*}` and their fixtures | matrix inputs; a "fix" here would move the reds the claim requires | G7 |
| `.ufo/waves/round-34/wave1/L1Integration.md`, `.ufo/waves/round-35/{claims-erratum-d5.md,wave1-results.json,wave1-results.provenance.md}` | carried-over checks E4/E5/E6; already green — editing risks the carried semantics | G2 |
| `corpus/lessons/round-36*.md` | E8 carried-over; already green | G2 |
| `corpus/knowledge/considerthese-proposals-ledger.md` | tracked durable ledger (`c354ca02…`, 35 lines) with a `score-gap.py` digest pin; the round's literal is the *new* shorthand (F-4) | G2 + G7 |
| fleet `MANIFEST.json`, `templates/**`, `scripts/**`, `.ufo/state/**`, `.ufo/watchdog.log`, `.ufo/waves/**`, `.ufo/l0-questions.md` (except an L1 append), other lanes' `.ufo/reports/**`, `.scratch/**`, fleet `.git/**`/`.jj/**` | fleet root is read-only to the round; driver/lane-owned | G10/G11 |
| all 20 sibling lane repos, kagi included | other lanes' rounds run concurrently (measured dirt in §1 #15); a kasegi write there is cross-lane contamination | G15 |
| `/home/vgpnk/Projects/shokuknow/**` | separate campaign; never write, never run its tools | G15 |
| `~/Projects/*` outside the fleet, `~/.omp/agent/{config.yml,mcp.json}` | operator-owned | G10 |
| `/fast/scratch/hyaku/**` outside `kasegi-r37/<SEATNAME>/` | shared scratch root | G8 |

## 4. Findings

### F-1 (HIGH, live) Frozen round-36 receipt rewritten during round 37

- **Evidence.** `git -C kasegi-shokunin status --porcelain` → ` M .ufo/waves/round-36/wave1/ScribeConsiderthese.md`;
  `git diff --numstat` → `38 0`; `git show HEAD:<file> | wc -l` = **198**, worktree = **236**;
  `sha256 840e25ef4c39fd9e07451d3e9b8e8c8c75530fb141b51d2bc744efb7bd381869` → `198fbdca46987ab0a0170258060502a776bbca37730782228c22a9bef6cfad23`;
  file mtime `2026-10-26 14:14:58 -0300` (17:14:58Z); last commit on the path `e666d90` (round 36).
  The added block is `## 8. Post-integration addendum (appended 2026-10-26T17:13Z, read at lane head b362068)`.
- **Exploit path.** A scribe re-reading round-36 evidence appends "what became observable after
  integration" to the *round-36* receipt instead of its own round-37 receipt. The round-36 receipt is the
  artifact `round-36-verifier-spotcheck.md` and every later reviewer read as frozen; a later round can
  rewrite its findings table at will. If committed, `git log -- .ufo/waves/round-36/…` shows a round-36 file
  changing under a round-37 message, and any future "round-36 receipts are byte-frozen" claim is false.
  Secondary: the appended text itself asserts "this receipt is committed" while the worktree copy is not —
  a self-refuting provenance sentence.
- **Impact.** Retro-editable prior-round evidence; E9's `status --porcelain` limb can never read clean while
  it exists; a `-- .ufo/waves` commit (F-2) would publish it.
- **Smallest remediation.** Before any commit: restore the file byte-for-byte from HEAD
  (`git show HEAD:.ufo/waves/round-36/wave1/ScribeConsiderthese.md` → overwrite; verify the sha returns to
  `840e25ef…`), rehome the §8 content in `ScribeConsiderthese-2`'s round-37 receipt (or a
  `claims-erratum-N.md`), and mint the incident in the round-37 lesson (`M37-6`: class scope-breach /
  frozen-evidence). Do **not** commit it as "late receipt".

### F-2 (HIGH, latent) Helper pathspec is coarser than the round's scope

- **Evidence.** `scripts/hyaku/jj-lane.sh:506-517` (`repo_path_allowed`) refuses only `.git*`, `.jj*`,
  `.ufo` exactly, `.ufo/state*`, `.ufo/watchdog.log`. `:522-556` (`validate_change_scope`) accepts a commit
  when every changed path is covered by the requested pathspec. Therefore `-- .ufo/waves` passes both checks
  and sweeps F-1's round-36 edit; `-- .ufo` alone is refused, which is the only accidental protection.
- **Exploit path.** L1 commits the wave in one call with a directory specifier to save keystrokes → the
  frozen round-36 file is published under a round-37 commit whose message says nothing about it.
- **Impact.** Silent rewrite of prior-round evidence inside an otherwise-green round; the commit's own
  `--name-status` is the only witness.
- **Smallest remediation.** Commit with **exact** round-37 paths (or `.ufo/waves/round-37` only), never an
  ancestor directory; after each commit run G4 and require the file list ⊆ §2.1.

### F-3 (MEDIUM) Scratch-root cleanup is weaker than E9's literal

- **Evidence.** `/fast/scratch/hyaku/kasegi-r37/` holds 24 entries: 22 seat dirs **plus** `build-spec.py`
  (56 599 B **file**) and `l1prep/` (dir). r36's E9 limb counts top-level **directories** only
  (`r36-closure.sh:474`: `find "$sroot" -mindepth 1 -maxdepth 1 -type d`) and skips the suite's own work dir
  (`:471-477`). A leftover *file* at the scratch root is invisible to that limb.
- **Impact.** A filing can read `scratch-seat-dirs=0` while `build-spec.py` (56 KB of L1 source) remains in
  the shared scratch root; the claim's "no leftover … seat dirs" literal is satisfied, the intent is not.
- **Smallest remediation.** Remove the whole `/fast/scratch/hyaku/kasegi-r37` tree, then assert
  `find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 | wc -l` = 0 for the parent path (dir absent also
  passes: `scratch-root=absent`). Do not rely on `-type d`.

### F-4 (MEDIUM) `corpus/considerthese-ledger.md` is a new path beside an existing tracked ledger

- **Evidence.** `git ls-files corpus/considerthese-ledger.md` → 0; `corpus/considerthese-ledger.md` absent on
  disk. The durable tracked ledger is `corpus/knowledge/considerthese-proposals-ledger.md`
  (`c354ca02…`, 35 lines, `score-gap.py`-digest pinned), and the round-36 receipt's own §8 records this.
- **Impact.** Two failure modes: (a) the L1 "helpfully" appends to the tracked ledger → breaks its pinned
  digest and creates two ledgers of record; (b) it lands the shorthand and the durable ledger stays at
  r31 flips → the proposal-7 entry points at a second, non-canonical ledger.
- **Smallest remediation.** Land the **new** file exactly as the claim literal
  (`corpus/considerthese-ledger.md`), cross-reference the tracked ledger inside it, and leave the tracked
  ledger byte-unchanged (G7). If the L1 concludes the tracked ledger is the right home, that is a claim-text
  change → `claims-erratum-N.md` + digest re-pin, never a silent rewrite.

### F-5 (LOW) E12's stale-label grep must be section-scoped

- **Evidence.** `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b` is present at
  `SCORECARD.md:1492` in the round-36 append; E12 bans it only inside the round-37 section.
- **Impact.** A whole-file `grep -c` returns 1 and false-reds a correct landing; a section-scoped grep is the
  only faithful check. Conversely, a landing that pastes the r36 block into the r37 section would pass a
  whole-file "absent" check only if the paste omitted the line.
- **Smallest remediation.** Scope the grep to the appended section (from the last `## Round 37` heading to
  EOF) in both the receipt and the report.

### F-6 (MEDIUM) E9 reads live host state, so the recorded run has an ordering constraint

- **Evidence.** E9 takes `--lane` and `--scratch-root` and reads the **live** worktree and scratch root
  (`r36-closure.sh:452-483`); it is not evaluable inside a `git archive` export. A mid-wave run at `b362068`
  read `status-dirty=6, scratch-seat-dirs=0, head-match=1, lane-root=1, scratch-root=present closed=0`
  (`ScribeConsiderthese.md` §8 disclosure) — i.e. red for round-37 dirt, not for a round-36 defect.
- **Impact.** A recorded `all-gates.txt` taken while any seat still holds an untracked path is red and, if
  committed, documents a failing run; a run taken after the L1's own `all-gates.txt` commit is clean but
  cannot contain its own resulting hash.
- **Smallest remediation.** Follow the order in G18. E10 binds only `suite-sha256=<digest of suite bytes>`
  plus the line counts — it does **not** require `export-ref` to equal the final head, so record the true
  `export-ref` of the run and do not back-fill the final hash into the file.

### F-7 (MEDIUM) The fleet worktree is not quiescent during the round

- **Evidence.** During this audit (17:0x → 17:16Z) the fleet root changed without any round-37 seat touching
  it: `?? k2.tsv` (248 B) and `?? k2s.tsv` (40 B) — both untracked, mtime 14:04, `git check-ignore` exit 1 —
  disappeared, and ` M .scratch/goal-20261026-hyaku-run9.md` (+18 −0) appeared. The driver also writes
  `.ufo/state/kasegi.report-baseline` (13:52) and `.ufo/watchdog.log`.
- **Impact.** Any gate of the form "fleet `git status` must be empty" is unusable and would either block
  filing or be quietly waived; a non-pathspec fleet commit would sweep `.scratch`. `k2.tsv`'s rows
  (`a/run.sh`, `space name.txt`, `var/lib/data.bin` + sha256 + size) show a tool was run with the fleet root
  as cwd and wrote relative outputs — the same misroot class G1 targets.
- **Smallest remediation.** Gate on **delta + attribution**, not emptiness: the only new kasegi-attributable
  fleet entry may be `.ufo/reports/round-37/kasegi.md`; commit it through
  `scripts/hyaku/fleet-commit.sh --as kasegi -m … -- .ufo/reports/round-37/kasegi.md` (pathspec-limited,
  refuses `.ufo/state/*` and `.ufo/watchdog.log`, `fleet-commit.sh:44-48,68-86`) and verify
  `git show --name-only`.

## 5. Pre-filing guardrail checklist (run in order; each is fail-closed)

`L=/home/vgpnk/Projects/shokunin/kasegi-shokunin` · `F=/home/vgpnk/Projects/shokunin`. Any command error,
non-zero exit where zero is expected, or ambiguous output is **RED** — never "clean".

**G1 — misroot sweep (fleet + 21 lanes).**
```bash
cd "$F"
[ "$(git rev-parse --show-toplevel)" = "$PWD" ] || echo RED-misroot-fleet
for d in */; do d=${d%/}; [ -d "$d/.git" ] || continue
  [ "$(git -C "$d" rev-parse --show-toplevel)" = "$PWD/$d" ] || echo "RED-misroot $d"
done
find . -maxdepth 3 -name .git -not -path './.git' | wc -l    # expect 21
```
Baseline: 21 OK lanes, 21 `.git`, 0 red. A `RED-misroot` means a status read would have reported another
tree's cleanliness — the failure mode E9's `lane-root` limb guards inside the suite.

**G2 — no lane tracked write outside the manifest.** `git -C "$L" status --porcelain --untracked-files=no`
must be **empty**. **Currently RED (F-1).** Diff every remaining line against §2.1; a prior-round path is a
RED even if "just an addendum".

**G3 — untracked write allowlist.** With `git -C "$L" status --porcelain -uall`, every `??` path must match
`^\.ufo/waves/round-37/`; nothing under `corpus/`, `SKILL.md`, `LOG.md`, `SCORECARD.md`, siblings or `/fast`.
A `??` outside the wave dir is a seat write outside its receipt (the exact class F-1 belongs to).

**G4 — commit containment and identity.** For each new commit:
`git show --name-status --format='%H %an <%ae> | %cn <%ce> | %s' <c>`. Require author **and** committer
`kasegi-shokunin <kasegi@shokunin.local>` (helper-enforced, `jj-lane.sh` `--as`), subject prefixed
`round-37:`, and the file list ⊆ §2.1. **Never** commit an ancestor directory such as `.ufo/waves` (F-2).

**G5 — VCS mutation audit.** `git -C "$L" reflog --date=iso` → every new entry reads `export from jj`
(a `commit:`/`reset:`/`checkout:`/`merge:` entry means a plain-git mutation). `git stash list` empty;
`git worktree list` single entry; `ls .git/index.lock` absent. jj-side witness:
`ls .jj/repo/op_store/operations | wc -l` delta vs. baseline **617**, and `strings` on each new op file —
descriptions must be ones the helper emits (`commit`, `describe`, `metaedit`, `file track`, `bookmark set`,
`git push`, `git import`, `new`, `rebase`). A `status`/`log`/`diff`/`show` op is a **seat running bare `jj`**,
which silently snapshots the working copy: RED. (Seats must use `--ignore-working-copy` if they inspect jj at
all; the safest rule is: nobody but the helper invokes `jj`.)

**G6 — claims integrity.** `sha256sum .ufo/waves/round-37/claims.json` =
`570c1d2c3f50723d161387283d4e4100f8f76e5aef2f270b70ce59f51fa778a7`;
`git diff --stat 224df74..HEAD -- .ufo/waves/round-37/claims.json` empty; corrections exist only as
`claims-erratum-N.md`.

**G7 — frozen-history containment.**
```bash
cd "$L"
git diff --name-only 224df74..HEAD | grep -E 'round-(2[0-9]|3[0-6])/' && echo RED-prior-round-touched
git diff --name-only 224df74..HEAD | grep -vE '^(corpus/|SKILL\.md|LOG\.md|SCORECARD\.md|SHONEN\.md|PROVINCE\.md|\.ufo/waves/round-37/)' && echo RED-outside-manifest
```
Both must print nothing. (G2 covers the uncommitted variant — that is where F-1 lives today.)

**G8 — scratch root fully removed.**
```bash
find /fast/scratch/hyaku/kasegi-r37 -mindepth 1 2>/dev/null | wc -l   # expect 0 (or path absent)
```
Not `-type d`: `build-spec.py` is a file (F-3). Run before the recorded suite run, because E9 reads it live.

**G9 — recorded run preconditions.** Only after G2 and G3 are clean at the current head:
`git -C "$L" rev-parse HEAD` == `git -C "$L" rev-parse --verify HEAD` == remote tip (G12), and the working
tree clean. Any dirt at run time makes E9 red by design (F-6), not by suite defect.

**G10 — forbidden-surface digests (fleet + operator).**
`MANIFEST.json ecc50774…`; `git ls-tree -r HEAD -- templates scripts | sha256sum` = `465f4ae6…`;
`.ufo/l0-questions.md` = `67b2ead7…` and lines 1–178 byte-identical (append-only, L1 only);
`~/.omp/agent/config.yml e709890e…`; `~/.omp/agent/mcp.json 4e8746da…`. **Do not** digest-gate
`.ufo/state/**` or `.ufo/watchdog.log`: the driver writes them continuously (measured
`kasegi.report-baseline` @13:52, watchdog `launch kasegi round=37` line) — gate them by "never committed"
(the helpers refuse those paths) and by "no kasegi-round artifact beyond the driver's own keys".

**G11 — fleet filing containment (single path).**
```bash
cd "$F" && git status --porcelain          # baseline, record it, do not assume empty (F-7)
git status --porcelain | grep -vE '^( M \.scratch/|\?\? \.ufo/reports/round-37/kasegi\.md$)' && echo RED-fleet-extra
bash scripts/hyaku/fleet-commit.sh --as kasegi -m "round-37: kasegi report" -- .ufo/reports/round-37/kasegi.md
git show --name-only --format='%h %s' HEAD   # exactly .ufo/reports/round-37/kasegi.md
```
Never name `MANIFEST.json` (admission is non-author hyaku), `templates/`, `scripts/`, `.ufo/state/`,
`.ufo/watchdog.log`, `.scratch/`, or another lane's report.

**G12 — report-last ordering and hash binding.** The fleet report cites the **final lane head**, and at the
moment of filing all three agree: `git -C "$L" rev-parse HEAD` = `git -C "$L" ls-remote origin
refs/heads/master` (measured `b362068…` before integration) = the hash printed in the report. Nothing is
committed to the lane after the report commit; if the lane moves, the report is stale and must be re-filed.

**G13 — placeholder / stale-literal / false-path greps.**
```bash
cd "$L"
grep -c 'filled by the L1' SCORECARD.md            # 0
grep -c '<LANE_HASH>' SCORECARD.md                 # 0
sed -n '/^## Round 37/,$p' SCORECARD.md | grep -c 'e666d902'   # 0 (section-scoped; whole-file is 1 at :1492)
grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh      # 0
git ls-tree -r HEAD --name-only | grep -c r36-fixtures         # 0, and the dir stays absent on disk
grep -c 'gate\\|probe' SKILL.md                     # only the r35 row remains; r36 row is single-choice
```

**G14 — C2 surface (before → after).** frontier `19 → 20`; `corpus/SOURCES.md` rows `53 → 54` and S054 has
**13** fields (`awk -F'|' '/^\|[[:space:]]*S054[[:space:]]*\|/{print NF-2}'` → 13);
`corpus/knowledge/*.md` `48 → 49`; `knowledge-expected.txt` non-comment entries `48 → 49` (do **not** use
`wc -l`, which counts 2 comment lines: 50 → 51); `corpus/source-snapshots/round-37/{S054.txt,manifest.json}`
present and bound (`capture-binding-check.py records=44 bound=44`); `recheck-audit.py` prints
`expected=49 missing=0 unexpected=0 exit=0`; junk twin rejected. Before-state measured in §1 #5.

**G15 — cross-tree non-interference.** Do not gate on sibling cleanliness — measured concurrent dirt
(§1 #15) makes that a flake. Instead: no path under any `*-shokunin/` other than `kasegi-shokunin` may
contain a round-37 kasegi artifact
(`grep -rl 'round-37' <sibling>/.ufo/waves/round-37 2>/dev/null` → nothing), and no file under
`/home/vgpnk/Projects/shokuknow` may change (`git -C … status` is *its* campaign's business; the kasegi
gate is "kasegi never opened it").

**G16 — no mutating VCS by seats.** G5 covers commits; additionally no seat may run `jj init/add/commit/
rebase/abandon/restore`, `git init/add/commit/reset/checkout/switch/push/fetch/stash`, or create a repo
anywhere. A fixture repo is legal only as `D=$(mktemp -d) && git -C "$D" init -q` with
`[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]` asserted first.

**G17 — tooling and operator files.** No `pacman` (host-wide pause); any install recorded in the receipt
(tool, version, channel, reason); `~/.omp/agent/{config.yml,mcp.json}` untouched (G10).

**G18 — landing order (the one sequence that satisfies E9 + E10 + G12).**
1. All seats yield; receipts committed (A17/A18/A19/A20/A21/A22 as applicable) with exact paths (G4).
2. Land carriers A01–A16; run the claim's counting commands; fix only within those paths.
3. Commit; `git status` clean (G2), scratch removed (G8).
4. Run `r37-closure.sh --export-ref <current head>` at the clean head; capture the transcript.
5. Commit `.ufo/waves/round-37/final-gates/all-gates.txt` (the transcript, digest header intact); verify
   `suite-sha256` equals `sha256sum corpus/instruments/r37-closure.sh` **as committed**
   (`git show HEAD:corpus/instruments/r37-closure.sh | sha256sum`).
6. Final verify run at the resulting head (clean tree, scratch absent) for `closed=14/14 exit=0`,
   `--selftest cases=14 failures=0`, and the two required reds (`cc692008…`, `a23dc478…` → `closed<14/14
   exit=1`). Re-run G2/G3/G5/G6/G7/G13 afterwards.
7. File the fleet report last (G11/G12), citing the lane head; then G11's post-commit check.

## 6. Scope self-audit

- Writes: this receipt only (plus scratch, removed). No lane/fleet/sibling/shokuknow file was created,
  edited, restored or deleted; in particular F-1 was **reported, not repaired**.
- VCS: read-only `status/diff/show/ls-tree/ls-files/ls-remote/reflog/worktree/log/rev-parse`, plus
  `git ls-tree -r HEAD -- templates scripts | sha256sum`. No `git`/`jj` mutating command; no `jj` invocation
  at all (op store read with `ls`/`strings`).
- Tooling: none installed or upgraded; no pacman.
- Network: none (the `ls-remote` read is a remote ref query against the lane's existing origin; no fetch).
- Blocking implications for the L1: **F-1 must be restored before the first commit**; **F-2 constrains the
  commit pathspec shape**; F-3/F-6 fix the recorded-run ordering; F-4 fixes one carrier's identity; F-5
  fixes one grep; F-7 fixes what "fleet status" is allowed to mean.
