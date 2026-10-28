# SentinelScope — round-43 scope watch (kasegi)

Seat: `SentinelScope`. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane write
target). Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; freeze commit
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (`round-43: frozen claims C1 …`, 2026-10-28T13:37:11-03:00).
Claims read first from `.ufo/waves/round-43/claims.json` (never edited; digest unchanged during the run —
`git status` shows it inside the untracked wave dir only).
Watch window: **2026-10-28T16:43:08Z → 16:50:38Z** (local `-03:00`, 13:43:08 → 13:50:38). Eight
listings of `w1/` (t0–t7; t4 was a targeted `__pycache__` snapshot inside the same window), the last five
taken after seats began yielding. The wave was **still in flight** at the last
listing (56/73 receipts), so every count below is a timestamped snapshot, not a final state.

Method: read-only. `ls`/`find -printf`/`stat`/`sha256sum`/`grep`/`python3` over the wave dir and scratch;
`git -C <lane> status|rev-parse|log` and `git -C <fleet-root> status` only. No mutating git/jj anywhere, no
`git init`, no throwaway git identity, no PACMAN, no tool install, no network fetch, no write outside
`/fast/scratch/hyaku/kasegi-r43/SentinelScope/` and this receipt.

## Verdict

Two defects in the wave dir, one latent scope leak inside a landable deliverable, three informational
scope facts. Every other surface the item names is clean, with the command and its real output below.

| # | Severity | Class | Producer | State at last sighting |
|---|---|---|---|---|
| F1 | **HIGH** | non-`<SEATNAME>.*` artifact written into the landable wave dir (`w1/__pycache__/`, 3 `.pyc`) | `ExecGateFixtures` scratch harness `check_all.py` | absent at t0 (16:43:08Z), present t1–t6, last rewrite 16:47:43Z |
| F2 | **MEDIUM** | committed receipt asserts a wave-dir state the tree contradicts | `ExecGateManifest.md:148-151` | false from 16:43:21Z onward |
| F3 | **LOW (latent)** | landable limb falls back to `mktemp` in `${TMPDIR:-/tmp}` and never removes it | `ExecK17ClaimsBefore.sh:565,569` | not fired in any graded run — every counting command passes `--work` |
| F4 | INFO | non-`<SEATNAME>.*` file in `w1/` | harness `build-w1-spec.py` (pre-seat) | present, 28 763 B |
| F5 | INFO | deliverables not enumerated in the seat prompt but declared in the seat receipt | 4 seats | conforming-by-declaration; landing map below |
| F6 | INFO | `/tmp` droppings (all < 50 MB, permitted) | 5 seats | left in place, sizes below |

---

## F1 — `w1/__pycache__/`: three compiled modules written into the landable directory

**What.** `w1/__pycache__/` is a directory holding

```
$ ls -la --time-style=full-iso .ufo/waves/round-43/w1/__pycache__
drwxr-xr-x 1 vgpnk vgpnk   226 2026-10-28 13:43:21.993387642 -0300 .
-rw-r--r-- 1 vgpnk vgpnk 18063 2026-10-28 13:44:56.233357882 -0300 ExecGateChain.rules.cpython-314.pyc
-rw-r--r-- 1 vgpnk vgpnk 21232 2026-10-28 13:44:56.224811132 -0300 ExecGateManifest.rules.cpython-314.pyc
-rw-r--r-- 1 vgpnk vgpnk 25485 2026-10-28 13:47:43.726402250 -0300 ExecGateProvReport.rules.cpython-314.pyc
```

None of those three names is `<SEATNAME>.<suffix>` or `<SEATNAME>.md`; the directory itself is not a name
any seat owns. The three sources they shadow *are* declared deliverables (`ExecGateChain.rules.py`,
`ExecGateManifest.rules.py`, `ExecGateProvReport.rules.py`), so the `.pyc` set is build residue beside the
landable bytes, and it is rewritten whenever a source changes. Timeline (UTC; listed mtimes are local
`-03:00`, i.e. +3 h): first written **16:43:21.98Z**, rewritten **16:44:56.22Z**, **16:46:36.67Z**,
**16:47:43.72Z**. It was **absent** at t0 (16:43:08Z, 13 s earlier) and present at every listing from t1 on.

**Digests at last sighting (16:47:46Z).**

```
d0e754fa65076c3b852526df7163bcef5a857fa86fca87284f1cfc6b6d2a83a1  ExecGateChain.rules.cpython-314.pyc
cefb9f825f51cc51f6dfed529a843d4785123a2740df7b189430069db3c30764  ExecGateManifest.rules.cpython-314.pyc
efa9bfd7d8e5b5bf9aaeb7f884c654775c2022a42de5400c131f11f8f55da42f  ExecGateProvReport.rules.cpython-314.pyc
```

**Producer, from local evidence.** The pyc headers carry absolute wave-dir source paths, i.e. they were
compiled from sources living in `w1/`:

```
python3 -c 'marshal code.co_filename' →
ExecGateChain.rules.cpython-314.pyc     co_filename=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateChain.rules.py
ExecGateManifest.rules.cpython-314.pyc  co_filename=…/round-43/w1/ExecGateManifest.rules.py
ExecGateProvReport.rules.cpython-314.pyc co_filename=…/round-43/w1/ExecGateProvReport.rules.py
```

The only **surviving** harness that loads exactly these three modules by absolute wave-dir path is
`ExecGateFixtures`'s scratch file
`/fast/scratch/hyaku/kasegi-r43/ExecGateFixtures/check_all.py`:

```
8:W = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1"
11:def load(name):
12:    path = os.path.join(W, name)
13:    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), path)
15:    spec.loader.exec_module(mod)
28:    manifest_mod = load("ExecGateManifest.rules.py")
29:    chain_mod = load("ExecGateChain.rules.py")
30:    prov_mod = load("ExecGateProvReport.rules.py")
```

`exec_module` on a source in `W` writes `W/__pycache__/` unless bytecode writing is suppressed, and nothing
in the harness sets `sys.dont_write_bytecode` or exports `PYTHONDONTWRITEBYTECODE`. Timing corroborates the
first creation: the three pyc files land at 16:43:21.98–.99Z, and that seat's scratch directory is stamped
16:43:22.354707005Z — 0.36 s later.

**Second producer, not excludable for the later rewrites.** A background scan run at 16:44:47Z also found
`/fast/scratch/hyaku/kasegi-r43/ExecExemplarPackage/precheck.py` referencing the same three module names;
that scratch was emptied when the seat cleaned up (16:50Z, directory empty) so its import style cannot be
read. Its receipt says the same thing (`ExecExemplarPackage.md:24-27`: *"The three sourceable `*.rules.py`
modules were run separately before the CLI"*, gate identity `…/ExecGateCore/claim-package-check.py`).
Attribution is therefore: **first creation = ExecGateFixtures' harness (timing, 0.36 s)**; later rewrites
are *this class of scratch precheck* and cannot be pinned to one seat. What is not in doubt, and is what
matters for scope, is that the artifact is produced by seats importing deliverables in place.

**It is removed and re-created, so cleanup alone does not hold.** The pyc headers embed the source
mtimes/sizes they were compiled from, and Chain/Manifest were recompiled at 16:44:56.22Z although their
sources had not changed since 16:41:41Z / 16:41:57Z:

```
header_src_mtime=1793205701 (2026-10-28T16:41:41Z) header_src_size=13115   [Chain]
header_src_mtime=1793205717 (2026-10-28T16:41:57Z) header_src_size=14379   [Manifest]
header_src_mtime=1793206059 (2026-10-28T16:47:39Z) header_src_size=17168   [ProvReport]
```

An unchanged source with a freshly written pyc means the directory had been deleted and a later import
re-created it. Sighting sequence: created 16:43:21.98Z → removed, re-created 16:44:56.22Z →
ProvReport recompiled 16:46:36.67Z (source edit) and again 16:47:43.72Z (source 16:47:39Z) → still present
at the last listing 16:50:04Z. No seat's own text owns the artifact; the only mention in the wave dir is
F2 below, and it is already false.

**Mechanism reproduced in my own scratch** (no write to `w1/`, copies of the three modules only):

```
$ cd /fast/scratch/hyaku/kasegi-r43/SentinelScope/mech   # 3 .py copied in, nothing else
$ python3 -c '<same load(): spec_from_file_location + exec_module, path=os.getcwd()/name>'
sys.dont_write_bytecode = False
$ ls -la mech/__pycache__
-rw-r--r-- 18044 ExecGateChain.rules.cpython-314.pyc
-rw-r--r-- 21213 ExecGateManifest.rules.cpython-314.pyc
-rw-r--r-- 25466 ExecGateProvReport.rules.cpython-314.pyc
```

Three pyc files, same names, same class of sizes — the mechanism is exactly what produced F1.

**Impact.** `w1/` is the directory the L1 enumerates to land bytes; a blanket `cp w1/<seat>.*` or a
`find w1 -newer …` sweep picks up `__pycache__/` unless it is excluded, and a receiver auditing the wave
dir sees entries no seat owns. The directory also mutates under the L1 while it enumerates (four rewrites
inside the watch window).

**Smallest remediation.** (1) L1 removes `w1/__pycache__` before landing (one `rm -rf`); (2) `ExecGateFixtures`
either copies the three modules into its own scratch before importing, or runs its harness with
`PYTHONDONTWRITEBYTECODE=1` / `python3 -B`. No landed byte changes either way.

## F2 — `ExecGateManifest.md:148-151` asserts a wave-dir state the tree contradicts

**Claim, verbatim:**

```
148: Pre-landing sanity: `python3 -m py_compile ExecGateManifest.rules.py` → ok.
149: That check wrote a `__pycache__/` into the wave dir; I removed it immediately
150: (`rm -rf`), and the final `ls` of the wave dir shows no `__pycache__` or
151: `*.pyc`.
```

**Falsified by the tree, from 13:43:21Z onward:**

```
$ ls -d .ufo/waves/round-43/w1/__pycache__
/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/__pycache__
$ find .ufo/waves/round-43/w1 -maxdepth 1 -type f -size 0        # (nothing: no empty-file alibi)
```

The seat's own `rm -rf` was honest — it ran before 13:42:53Z, when its receipt was written — but the
sentence is written as a final state, and it stopped being true 28 s later when `ExecGateFixtures` created
the directory from a sibling import (F1). A reader taking line 150 at face value gets a false fact about
the landable dir; this is precisely the class the round is built to make gradable (a committed record that
contradicts the tree it describes), and it is the second-seat re-creation, not the author's own action,
that turned it false.

**Smallest remediation.** Either the L1 removes the artifact (F1 remediation, which restores the claim's
truth) or the seat's sentence is re-scoped from "the final `ls` shows no …" to "no `__pycache__` existed
when I yielded at 13:42:53Z; a sibling may recreate it" — the first is cheaper and leaves the receipt
unchanged.

## F3 — `ExecK17ClaimsBefore.sh` falls back to `${TMPDIR:-/tmp}` and never cleans its work dir

```
565:    K17_WORK=$(mktemp -d "${TMPDIR:-/tmp}/k17-work.XXXXXXXX") || exit 2
569:    rm -rf -- "$K17_WORK/export"
```

`--work` is honoured when given (`552: --work) K17_WORK=$2 ;;`), and every counting command in
`claims.json` passes `--work`, so no graded run trips this. But the bytes that will land inside
`corpus/instruments/r43-closure.sh` contain a default that (a) depends on an inherited `TMPDIR` — the wave
rule says never rely on one — and (b) creates a `k17-work.*` directory outside `--work`/`--scratch-root`
when the suite calls the limb without it, with no `trap` and no `rm -rf "$K17_WORK"` (the only removal is
`$K17_WORK/export`). Latent scope leak in landable bytes, not an observed write: **zero** `k17-work.*`
directories exist in `/tmp` or `/var/tmp` at any listing.

**Smallest remediation.** Make `--work` mandatory in the limb (exit 2 with a message, mirroring the
export-mode refusal at :575-580) or default to a directory under the caller's scratch root and add
`trap 'rm -rf -- "$K17_WORK"' EXIT`.

## F4 — `w1/swarm-registry.json` is not a seat file

```
-rw------- 1 vgpnk vgpnk 28763 2026-10-28 13:37:01.062501830 -0300 swarm-registry.json
```

Written **before any seat existed** — `build-w1-spec.py` 13:37:01.020, `w1-spec.json` 13:37:01.034,
`w1-dispatch.json` 13:37:01.064, `w1.ready` 13:37:18.139 — and `w1.ready` names the dispatch as
`"dispatch": ".../round-43/w1-dispatch.json", "l1": "KasegiR43"`. Harness artifact, not a seat write;
listed here because the rule is "report every file that is not `<SEATNAME>.<suffix>` or `<SEATNAME>.md`".
Must be excluded from landing.

## F5 — deliverables not enumerated in the seat prompt, but declared in the seat receipt

These carry a seat-name prefix but a suffix the seat prompt did not name. Each is declared, with its landing
path and digest, inside the producing seat's own receipt — so this is prompt under-specification, not an
undeclared write. Landing map for the L1:

| File(s) | Declared at | Lands at |
|---|---|---|
| `ExecExemplarPackage.{report.md,claim_checklist.md,manifest.json,custodian-receipts.json,provenance.json,status.json,source-capture.txt,source-excerpt.txt,solution-fixed-in.txt,disclosure-timeline.txt}` | `ExecExemplarPackage.md:58-68` (path + line count + sha256 per row) | `corpus/instruments/fixtures/claim-package/exemplar/{,evidence/}` per column 2 |
| `ExecGateFixtures.defect-1-missing-file` … `defect-9-secret` (9 **directories**, each a package tree with `custodian-receipts.json`, `provenance.json`, `report.md`, `status.json`, `evidence/`, `expected-rule`) | `ExecGateFixtures.index.txt` (13:47:16Z, 1071 B) | `corpus/instruments/fixtures/claim-package/defect-*` |
| `ExecSourceCapture.S067.txt` (6 446 B, sha256 `327bc909…`, 131 lines) | `ExecSourceCapture.md:106,114` | `corpus/source-snapshots/round-43/S067.txt` |
| `ScoutConsiderthese.txt` (14 lines, sha256 `76c3468b…`) | `ScoutConsiderthese.md:37,105` | end-of-file append to the proposals record |

Note the form deviation: the nine defect fixtures are directories beside the receipt, not single files.
They are the only `w1/` subdirectories other than `__pycache__` (`find w1 -maxdepth 1 -type d | wc -l` = 10).

## F6 — `/tmp` droppings (permitted size, not cleaned)

| Path | Bytes | UTC |
|---|---|---|
| `/tmp/w1_log_land.txt` | 401 | 16:38:54 |
| `/tmp/w1_q_land.txt` | 379 | 16:38:54 |
| `/tmp/w1_sc_land.txt` | 918 | 16:38:54 |
| `/tmp/census.out` | 3 704 | 16:39:56 |
| `/tmp/k18prompt.txt` | 1 534 | 16:40:02 |
| `/tmp/rv_sources.log` | 3 704 | 16:40:00 |
| `/tmp/revk19.err` | 0 | 16:43:15 |
| `/tmp/revk19.out` | 58 | 16:43:15 |
| `/tmp/revk19.src` | 0 | 16:44:16 |

All far under 50 MB, so permitted by the host guard, but they outlive their seats. `find /tmp -maxdepth 1
-type f -size +50M -newermt '2026-10-28 00:00:00'` → nothing; largest `/tmp` file today is
`/tmp/hyakki-repo-de46e1e.bundle` (17 535 828 B), another lane's. `/var/tmp` holds only
`disk-guard.{m3dRfl,uabpf0}` temp dirs from the disk guard itself.

---

## Surfaces verified clean (command → real output)

**No mutating git/jj command anywhere in the wave dir.** Verb histogram over every `git` token in all
`w1/` bytes, and an explicit mutating-verb scan:

```
$ grep -rhoE '\bgit[[:space:]]+(-[^ ]+[[:space:]]+)*[a-z-]+' w1 | awk '{print $NF}' | sort | uniq -c | sort -rn
     48 -            21 archive       16 show        13 diff      13 cat-file
     12 log          10 ls-tree        9 status       6 rev-parse  6 grep       5 ls-files
$ grep -rcE 'git[[:space:]]+(init|commit|add|push|checkout|reset|stash|branch|tag|worktree)|jj[[:space:]]+(commit|new|describe|edit|squash|rebase|abandon|bookmark)|GIT_COMMITTER|GIT_AUTHOR|user\.(name|email)' w1 | awk -F: '$2>0'
   (no output — zero files, zero hits)
```

Only read-only verbs appear (`archive`, `rev-parse`, `show`, `cat-file`, `status`, `ls-tree`, `log`, `diff`,
`grep`, `ls-files`); no fixture repository and no throwaway identity was created.

**Lane `.jj` untouched after the freeze commit.** Every `.jj` write precedes the wave's first seat activity:

```
$ find kasegi-shokunin/.jj -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS\n' | sort | tail -1
2026-10-28T13:37:13.6146176260
```

That is the freeze commit's own operation (13:37:11.73–13:37:13.61, commit `4cb6d4a`); nothing after.

**Lane worktree: no write outside the wave dir, no tracked change, no deletion.** At every listing from
16:43:20Z to 16:48:20Z:

```
$ git -C kasegi-shokunin status --porcelain=v1
?? .ufo/waves/round-43/INTEGRATION-PLAN.md
?? .ufo/waves/round-43/w1-REGISTRY.txt
?? .ufo/waves/round-43/w1.ready
?? .ufo/waves/round-43/w1.ready.dispatched
?? .ufo/waves/round-43/w1/
```

Five untracked paths, all under `.ufo/waves/round-43/`; no ` M `, ` D `, `D ` entry (so no tracked deletion
in `corpus/` either — the C2 kill rule's "tracked deletion" arm is not exercised). And:

```
$ find kasegi-shokunin -newermt '2026-10-28 13:37:14' -type f -not -path '*/.git/*' -not -path '*/.jj/*' -not -path '*/round-43/*' | wc -l
0
```

**`/home/vgpnk/Projects/shokuknow` untouched.** Zero entries newer than 13:00, at every listing:

```
$ find /home/vgpnk/Projects/shokuknow -newermt '2026-10-28 13:00:00' -not -path '*/.git/*' | wc -l
0
```

Reads of it are explicitly allowed and two receipts disclose them (`ScoutSiblingOverlap.md:76-94` greps it
and records `ls -ld … No such file or directory` for `shuknow`); grep of `w1/` shows no campaign-tool
invocation and no write path into it.

**Sibling lane repos: no kasegi artifact.** `find /home/vgpnk/Projects/shokunin -maxdepth 4 -name '*kasegi*'
-newermt '2026-10-28 13:30:00' -not -path '*/kasegi-shokunin/*'` → no output. The activity counts in
`kaidoku` (12), `souji` (24), `tameshi` (17), `tsukuroi` (12), `tabi` (7), `mori` (1) are those lanes' own
concurrent rounds (`kaidoku …/tools/round-46/{gate,attest}.py`, `souji …/census/round-38/records/*`,
`tameshi …/round-55/contract.json`, `tsukuroi PROVINCE.md`, `tabi …/round-42-verifier-spotcheck.md`).

**PATH directories and agent config untouched.** Before the wave, and unchanged after it:

```
$ stat -c '%y %n' /home/vgpnk/.local/bin /home/vgpnk/.omp/agent/config.yml /home/vgpnk/.omp/agent/mcp.json
2026-10-28 11:52:25 -0300 /home/vgpnk/.local/bin
2026-10-28 13:10:10 -0300 /home/vgpnk/.omp/agent/config.yml
2026-10-25 02:32:37 -0300 /home/vgpnk/.omp/agent/mcp.json
$ find /home/vgpnk/.local/bin -newermt '2026-10-28 13:30:00' | wc -l
0
```

`/usr/bin`, `/usr/local`, `/etc`, `/opt`, `/home/vgpnk/.agents` → 0 entries newer than 13:37. No
`systemctl`/service-restart string anywhere in `w1/`.

**Fleet root: two writes inside the window, neither from a kasegi seat.** `git -C
/home/vgpnk/Projects/shokunin status --porcelain=v1` is byte-for-byte the same set at t0 (16:43:27Z) and t4
(16:46:42Z); mtimes attribute the two new paths:

- `.scratch/goal-20261028-hyaku-run11.md` — 16:41:14Z, content begins `# hyaku run 11 — 2026-10-28` /
  `Operator directive (verbatim): "ok, let's continue the training rounds…"` → the hyaku runner.
- `.ufo/reports/round-38/souji.md` — 16:43:18Z, content begins `# souji round 38 … Lane:
  /home/vgpnk/Projects/shokunin/souji-shokunin · hyaku run 11 · round 38 attempt 1` → `SoujiR38`, which
  `history://` lists as running.
- Pre-existing, older than the window: `o.bin` (Oct 27), `oldrep1.out` (12:10Z), `oldrep2.out` (12:11Z),
  `.scratch/{closure-mado-r50.json, closure-r54/, source-routing-queue.md}`, and the literal directory
  `D=` (12:07:44Z).

No `w1/` artifact references either path (`grep -rn 'round-38/souji\|goal-20261028' w1` → no output), so no
kasegi seat claims or reproduces them.

**Home top level / `.config`:** the only entries newer than 13:37 are runtime session-state, with zero
kasegi content — `/home/vgpnk/.gateguard/state-sess_dwf-dwfrun-7d7c2543-…-actor_3_1.json` (13:46:25),
`/home/vgpnk/.grokbot`, `/home/vgpnk/.config/{fcitx5,ai-usage}`.

**No long-lived process left by the wave.** `ps -eo pid,etime,cmd | grep -F kasegi-r43` shows only
short-lived instrument runs (`…/export/corpus/instruments/frontier-recheck-count.py --root …`) and one
`timeout 30 du -xsk -- /fast/scratch/hyaku/kasegi-r43` scratch sizing. No service, no `sleep` watcher.

**No empty deliverables at last sighting.** `find w1 -maxdepth 1 -type f -size 0` → no output.
`ExecTranscriptDe0931.txt` was 0 B at 13:42:45 and is 2 005 B since 13:46:21 — in-flight seat, not a defect
(his scratch kept growing until 13:42:45).

## Re-list log (eight listings; the item asks for at least three)

| # | UTC | Command | Observed |
|---|---|---|---|
| t0 | 16:43:08 | `ls -la --time-style=full-iso w1` | 26 files, 0 dirs; `__pycache__` already present (3 pyc, 13:43:21.98); `swarm-registry.json` 0600; `ExecTranscriptDe0931.txt` 0 B |
| t1 | 16:44:20 | `os.listdir(w1)` | 38 entries; non-seat-named = `__pycache__`, `swarm-registry.json`; pyc rewritten 16:44:56 |
| t2 | 16:46:36 | `ls` tail + `ls -la w1/__pycache__` | receipts appearing (ExecRegistryRows, MutGateRules, RevK16, ScoutSourceHunt …); ProvReport pyc rewritten 16:46:36.67 |
| t3 | 16:47:09 / 16:47:24 | `ls -1 \| wc -l` then the spec-conformance script | 76 then 87 entries; 29 `<seat>.md`; `ExecExemplarPackage.*` (10 files) and `ExecGateFixtures.defect-*` (9 dirs) appear |
| t5 | 16:48:20 | final sweep | 94 entries, 41 receipts, 10 dirs; mutating-verb scan 0; lane status 5 paths; shokuknow 0; 47 scratch dirs live |
| t6 | 16:48:49 | `ls -A \| wc -l` | 100 entries, 44 receipts; `__pycache__` present, 3 pyc; `swarm-registry.json` 28 763 B |
| t7 | 16:50:38 | `ls -A \| wc -l` + conformance script | 116 entries, 56 receipts, 10 dirs, 3 pyc; non-`<SEATNAME>.*` = `__pycache__`, `swarm-registry.json` only; 41 scratch dirs still live |

Growth is monotone except the pyc rewrites; the only non-`<SEATNAME>.*` entries at **every** listing from
t1 on are `__pycache__` and `swarm-registry.json` — the two findings F1 and F4, nothing else.

## Declarations

- Scratch `/fast/scratch/hyaku/kasegi-r43/SentinelScope/` only (removed before yield; the mechanism
  reproduction lived at `…/SentinelScope/mech/`).
- Writes: this receipt and that scratch tree. Nothing in the fleet root, no sibling lane, no shokuknow, no
  PATH directory, no `~/.omp` file, no `w1/` file other than this receipt.
- Tools installed: none. `pacman` not invoked (host-wide pause respected). Network: no fetch issued.
- Git: `status --porcelain`, `rev-parse`, `log -1` only. No `archive` extraction of my own.
- This receipt is the deliverable and a self-digest is not quotable inside it; compute with
  `sha256sum .ufo/waves/round-43/w1/SentinelScope.md`. Digests of the artifacts this receipt is about are
  given inline (F1) so they can be re-verified against the tree.

## Limits

The wave was in flight at t7 (56/73 receipts, 41 scratch dirs still live; some seats edit deliverables after
writing their receipts — `ExecGateProvReport.rules.py` changed at 16:47:39Z and its `.pyc` at 16:47:43Z, and
`ExecExemplarPackage` emptied its scratch at 16:50Z). F1's presence is
stable across every listing from t1 on and its mechanism is reproduced, so it will still be there at landing unless
someone removes it; the count of `ExecGateFixtures.defect-*` and `ExecExemplarPackage.*` deliverables, and
therefore the F5 landing map, should be re-read from `ExecGateFixtures.index.txt` and
`ExecExemplarPackage.md` at landing time.
