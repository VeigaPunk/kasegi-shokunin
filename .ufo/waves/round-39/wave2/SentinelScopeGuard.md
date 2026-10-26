# Scope guard — round 39, wave 2 (SentinelScopeGuard)

Seat: `SentinelScopeGuard`, leaf attack seat. I authored none of the artifacts under attack (the C1
suite, the C2 artifacts, the claims and the errata are other seats' work); this seat wrote only this
receipt and its deliverable. Reading was read-only throughout; no git/jj mutation, no fixture, no clone.
Scan UTC 2026-10-26T20:14:09Z..20:20Z (local -03:00 17:14..17:20).
Anchors: fleet HEAD `d1e70ce65352cf95866842eb81e470eda7988e8e` (protocol-shokunin, 17:07:10 -03:00);
lane HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (Y); wave threshold `2026-10-26 16:20:00 -03:00`
(6m41s before the claims freeze `dcd3170` 16:26:41). Disk guard green at 20:17:17Z
(`ok /fast/scratch/hyaku use=25%`).

## 1. Verdict

| # | check | verdict | discriminator |
|---|---|---|---|
| a | fleet repo uncommitted writes | **PASS** | `git status --porcelain` and `-uall` → 0 lines |
| a′ | fleet repo *committed* writes during the wave | **PASS** | 31 commits, 19 orchestrator + 12 per-lane dispatch/report; 19 unique paths, none in a lane tree |
| a″ | `MANIFEST.json` mtime 17:06:10 | **cleared** | working-tree bytes == HEAD (`sha256 1d65a896…` both sides); rewrite is hyaku ledger append `f0505690` (kaidoku r40), by `scripts/hyaku/append-closure.py` |
| b | `~/.local/bin` + all PATH dirs | **PASS** for the round-39 window | no entry created/modified/renamed (`-newermt` and `-newerct` both empty across 20 dirs); no o+w, no foreign owner, no symlink into a repo/scratch; only PATH shadow is `jq` (real ELF, 2026-10-03) |
| b′ | host persistence surfaces | **PASS** | no systemd-user / autostart / shell-rc / crontab change |
| c | 20 sibling lane repos | **PASS** | 14 clean, 6 dirty only in their own round dirs; no kasegi identity author; no kasegi path, file or blob; S057 / "round-39" hits are lane-local |

FAIL count: **0**. Two findings, neither a numeric refutation of a frozen predicate: **F1** (medium,
latent, in the landed instrument) and **F2** (low, out-of-window host trace) — §3.

## 2. Evidence (commands with the output that decides)

Fleet root:
```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain            → (no output) rc=0
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | wc -l   → 0   (re-run 20:17:19Z → 0)
$ git -C … rev-list --count --since='2026-10-26T16:20:00-03:00' HEAD  → 31
$ git -C … log --since=… --format='%an' | sort | uniq -c
      2 kaidoku-shokunin / 1 kama-shokunin / 1 kasegi-shokunin / 2 kengaku-shokunin / 2 mado-shokunin
     19 protocol-shokunin / 1 souji-shokunin / 1 tabi-shokunin / 2 tameshi-shokunin
$ git -C … log --since=… --name-only --format='' | sort -u | wc -l    → 19
   all 19: MANIFEST.json, .scratch/goal-20261026-hyaku-run9.md, .ufo/prompts/{kaidoku-round-41,
   kama-round-46,kasegi-round-39,kengaku-round-42,mado-round-46,tabi-round-34,tameshi-round-49}.md,
   .ufo/prompts/closure/*.md (5), .ufo/reports/round-{33,40,41,45,48}/*.md
$ git -C … ls-files | grep -c '\-shokunin/'                           → 7
   (all synthetic: scripts/fixtures/sources-census/{injection,root/{a,b,c,z}}-shokunin/…)
$ sha256sum /home/vgpnk/Projects/shokunin/MANIFEST.json
   1d65a8969026d7944fb2173426c269a09495f26c797e9c19bd7e11f1883d42f9  (file)
$ git -C /home/vgpnk/Projects/shokunin show HEAD:MANIFEST.json | sha256sum
   1d65a8969026d7944fb2173426c269a09495f26c797e9c19bd7e11f1883d42f9  (HEAD blob)
$ git -C /home/vgpnk/Projects/shokunin diff --stat HEAD -- MANIFEST.json   → (empty)
$ git -C … log -1 --format='%h %cI %s' -- MANIFEST.json
   f0505690 2026-10-26T17:06:10-03:00 rounds ledger: kaidoku r40 closure (rejected-honest-stop) — hyaku, non-author
```

The one kasegi-named fleet file and its author. `edaa4fd1` is authored under the lane identity but is
the dispatcher's own prompt, and the same commit shape exists once for every lane dispatched in the
window (kama `87769f44`, mado `1a7a6925`, kengaku `e0551f18`, tameshi `77053a1b`, kaidoku `f51b1efc`,
tabi `0929a340`, kasegi `edaa4fd1`), i.e. orchestrator dispatch evidence, not a seat write:
```
$ git -C … log --since=… --format='%h %cI %an | %s' | grep -i kasegi
1e63da5d 16:28:38 protocol-shokunin | run9: goal ledger — kasegi r38 / tabi r33 closed … r39/r34 dispatched
edaa4fd1 16:22:59 kasegi-shokunin  | round-39: kasegi dispatch evidence (hyaku inline attempt 1)
97461c54 16:22:06 protocol-shokunin | rounds ledger: kasegi r38 closure (rejected-honest-stop) — hyaku, non-author
$ head -1 .ufo/prompts/kasegi-round-39.md
You are the kasegi L1, round 39. Working dir: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
```

Ignored paths (invisible to `git status`) written during the wave are all hyaku-run-9 state: `.jj/*`,
`.ufo/state/{disk-guard,inline-dispatcher}.log`, `.ufo/watchdog.log`, seven `*.report-baseline`,
the seven `.ufo/prompts/<lane>-round-N.md`, `.ufo/prompts/closure/*`, `.ufo/reports/round-{33,40,41,45,48}/`,
`.scratch/goal-20261026-hyaku-run9.md` (first line: `<!-- ORCHESTRATOR-OWNED run state (hyaku run 9) … -->`).
No `.ufo/reports/round-39/kasegi.md` exists yet (that dir holds `chousa.md` Oct 24 and `kaidoku.md` 14:57).

`~/.local/bin` (100 entries) and PATH (20 existing dirs):
```
$ find ~/.local/bin -maxdepth 1 -newermt "2026-10-26 16:20:00"   → (no output)
$ find ~/.local/bin -maxdepth 1 -newerct "2026-10-26 16:20:00"   → (no output)
   latest entry mtime 2026-10-26 10:50:01 (openbot) — 5h30m before the threshold
$ for p in $(echo "$PATH" | tr ':' '\n'); do [ -d "$p" ] && find "$p" -maxdepth 1 -newermt … ; done
   → (no output for every directory)
$ find ~/.local/bin -maxdepth 1 -type f -perm -o+w ; ! -user vgpnk       → (no output)
$ command -v git                                                          → /usr/bin/git
$ ls -la ~/.local/bin/git                                                 → No such file or directory
$ PATH symlinks resolved into shokunin|scratch|/fast                      → (none)
```

Siblings (each is its own repo; the fleet root is not a superproject):
```
audio0 chousa0 game-dev-2d0 game-dev-3d0 kagi0 kaidoku2 kake0 kama4 kasegi5 kengaku0 kotoba0 kotodama0
kumitate0 lore0 mado3 mori0 revenger0 souji0 tabi10 tameshi1 tsukuroi8      (dirty-line counts)
```
Every dirty path is the lane's own current round (kaidoku r41, kama r46, mado r45/r46, tabi r34,
tameshi r49, tsukuroi r42; mtimes 16:08–17:14). Commit identities since the wave are only
`<lane>@shokunin.local` and `protocol@shokunin.local`; no sibling commit is authored or committed by
`kasegi@shokunin.local`. Pickaxe (`-S'kasegi'`, `-S'round-39'`, `-S'r39-closure'`) over the window
surfaces only read-only cross-lane references by the owning lane: tabi's adjacency rows citing
`kasegi-shokunin` `SKILL.md:267` / `mission-control.md:119` / `ufo-workspaces.md:272` and its
`"kasegi": "d65d823e…"` sibling pin; tameshi's no-harm monitor hashing kasegi `.gitignore` +
`SCORECARD.md`; kengaku's own `plans/round-39-claims.md`; kama's own `round-39-{fleet-report,closure}.md`
("# kama round 39 fleet report / author: kama L1 / date: 2026-10-25"); mado's own
`.ufo/waves/round-39/w1/ExecEventqSnapshot/…`. Kasegi-only artifact names (`r39-closure.sh`,
`cisa-when-to-issue-vex*`, `claims-erratum-1.md`) exist in no sibling. `S057*` hits are lane-local
registry ids from earlier rounds (kake round 31 = a Render.com source; tabi round 18; tameshi round 45).

Positive control (the scan is not blind): the same `-newermt` filter returns the lane's own wave writes
(`16:26:21 c1-controls`, `16:26:35 claims.json`, `16:28:16 wave1-spec.json`, …) and the fleet's
`.scratch/goal-20261026-hyaku-run9.md` at 17:07:10. Negative control: 14 sibling repos read 0 under the
same filter, so the detector is not reporting noise.

Ignored-path gap closed: a write into a sibling's `.gitignore`d path never appears in `git status`, so
every sibling's `--ignored=matching` entries were checked too — only `.jj/{.gitignore,repo/,working_copy/}`
(the sibling's own VCS state, mtimes at its own commit times), `__pycache__/`, `.ruff_cache/` and pre-wave
scratch dirs of earlier rounds; none names kasegi and none was written inside the wave window. Bound of
the claim: a plant carrying zero `kasegi`/`round-39`/`r39-closure` token is not attributable by
name/content evidence; every sibling path, dirty or ignored, and every added line in every sibling commit
of the window was checked for those three tokens.

## 3. Findings

**F1 — medium, latent: the landed instrument resolves `git` through PATH.**
`corpus/instruments/r39-closure.sh` at HEAD (1793 lines) has 38 lines mentioning `git `, **29 executable**
invocations, and **0** `/usr/bin/git`. The judged-head export is bare-PATH (`:328 git -C "$LANE" archive
--format=tar "$REF_RESOLVED" | tar -xf - -C "$EXPORT"`), as are every lane-reading limb: `:323` rev-parse
--git-dir, `:325` rev-parse --verify, `:391` diff --numstat, `:692` cat-file, `:693` merge-base
--is-ancestor, `:696` diff --name-only, `:757` diff --no-color, `:956` `show "$PIN_REF:$suite"`, `:1315`
`show "$PIN_REF:…/r37-closure.sh"`. `/usr/bin` is PATH entry 12; eleven user-writable directories precede
it (six under `/home/vgpnk`, three under `/run/user/1000`), so a file named `git` in any of them wins for
every non-interactive script.
*Exploit path:* drop a `git` wrapper in a pre-`/usr/bin` directory → it is executed by the export limb and
by the diff/show limbs the gates compare against, so `closed=8/8` can be made to describe bytes that were
never committed. *Impact:* G1 (whole-tail declarations), G3 (added-line transcripts), G8 (pinned r37
bytes) and the judged-head export are trustworthy only if `command -v git` resolves to the system binary
at measurement time. *Smallest remediation:* resolve once at suite start (`GIT=$(command -v git)`; refuse
if it is not under `/usr/bin`/`/usr/local/bin` or if `readlink -f` lands in `$HOME`/`/fast/scratch`) and
invoke every limb as `"$GIT"`. No behaviour change on a clean host.

**F2 — low, out-of-window: a `git` path-shim existed in `~/.local/bin` during round 37.**
Two committed r37 receipts record it: `.ufo/waves/round-37/wave1/ExecC1JudgedHeadFail.md:97`
("`/home/vgpnk/.local/bin/git` (a 3526-byte Python wrapper, mtime 14:05 today, ahead of `/usr/bin/git` on
PATH) failed with `No such file or directory`…") and `.ufo/waves/round-37/wave1/ScribeMistakes.md:38`
("`/home/vgpnk/.local/bin/git` does not exist"). Host corroboration: `~/.local/bin` has directory mtime
`2026-10-26 14:05:53 -03:00` and no surviving entry with that mtime or ctime — the name existed
transiently at exactly the wrapper's stated mtime. Timeline: present 14:05:53 → observed 14:08:29 → gone
by 14:11:51, i.e. 2h14m before this wave's threshold. It is therefore **outside round 39 wave 2** and no
kasegi round-39 seat created or left one; but it proves the F1 class is real on this host, and whatever
suite limb ran bare-`git` inside that window ran through bytes nobody recorded. Remediation = F1.

## 4. Effect on the frozen claims (attack reading)

- C1: nothing in the eight gates' measured values is refuted here; `closed=8/8` at Y and the graded
  selftest are other seats' measurements, not mine. F1 is a trust-boundary caveat on *how* those numbers
  were produced — the instrument trusts PATH for the binary that produces the compared tree. Filed as
  remediation, not as a kill: the kill rule has no PATH clause, and no fixture shows a check passing while
  its defect is present.
- C2: unaffected — its counters are file counts and Python instruments over lane bytes, no `git`
  subprocess in the counted limbs.
- Do-nothing controls verified: an untouched fleet reads 0 and 14 untouched siblings read 0, while the
  same filter detects the wave's real writes; a lane that names kasegi is shown to be reading it, not
  writing it.

## 5. Files written (nothing else)

- `.ufo/waves/round-39/wave2/SentinelScopeGuard.md` — this receipt.
- `.ufo/waves/round-39/wave2/SentinelScopeGuard.scope.txt` — the deliverable: full commands and outputs.
- Scratch `/fast/scratch/hyaku/kasegi-r39/SentinelScopeGuard/` — removed before yielding.

## 6. Tooling, hygiene, scratch

No tool installed or upgraded (no pacman, no uv/npx/binary fetch) — nothing in this scan needed one.
No mutating git/jj command anywhere, no throwaway git identity, no fixture or clone created, no write to
any PATH directory, no fleet-root tracked file touched, no message to `agent://all`, no swarm.

Report: .ufo/waves/round-39/wave2/SentinelScopeGuard.md
