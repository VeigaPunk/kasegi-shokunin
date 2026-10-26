# SentScopeFinal — final scope, ownership, credential and misroot sweep (round 31, wave 2)

- **Seat:** sentinel, `SentScopeFinal`; lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- **Revisions:** base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a77999a00efbca129cfccb28a481037f6241f`; lane HEAD at sweep `eecad59db166e0626ca2472e96ea48bc28a35153` ("round-31: wave-1 integration …, wave-2 spec", 2026-10-25 21:16:52 −0300).
- **Answering model actually run on:** `opencode-go/deepseek-v4.1-flash` (harness route; no model parameter passed by this seat).
- **Writes by this seat:** this receipt only. No git/jj mutation anywhere (read-only `status`/`log`/`ls-tree`/`diff`/`rev-parse`/`cat-file`/`show`); no counter run of another seat's claim; no lane instrument edited; nothing deleted; `.scratch/` never read or written.
- **Scratch:** the changed-path list and the classifier live in `/tmp/sentscope/` (`classify2.py`, `changed_final.txt`), outside the lane; both are reconstructible from §9, so nothing in this receipt depends on them surviving. No lane or fleet path was created by this seat except this receipt.
- **Tooling installed or upgraded:** none (`pacman` paused host-wide; no package transaction, no `uv`/`npx` install — the sweep is coreutils + git + python3 stdlib).

## Verdict

**No credential material, no session/private URL, no live bounty-target contact, no `op://` vault reference, and no out-of-lane write attributable to a round-31 seat.** Six findings are reported, all **report-only** (this seat has no remediation scope):

| # | Severity | Finding | Where |
|---|---|---|---|
| F1 | medium (verifiability) | The committed wave-1 tree carries **109 scratch/fixture files (52 of them symlinks), 512,027 B** — including the raw 81,802 B MSVR HTML with six `CVToken` values and one `expToken` block. Wave 1 **predicted** exactly this and recommended committing by explicit path; the commit took the scratch anyway. | §2.3 |
| F2 | medium (verifiability) | The same commit makes the census control fixture **non-hermetic in history**: its 52 committed symlinks resolve into the *live* `corpus/`, so what the fixture asserts can change without any byte of the fixture changing. | §2.4 |
| F3 | low (scope) | `demo-cwd.txt` (30 B, content = the fleet-root path) was written at the **fleet root** after the claims freeze and is claimed by no receipt. Unattributed out-of-lane litter; reported, never deleted. | §1.3 |
| F4 | low (instrument) | The item-1 command (`git status` at the fleet root) **cannot** detect a lane write at all: every `*-shokunin/` lane is gitignored at the fleet root. The complements must stay in the close-out. | §1.1 |
| F5 | low (provenance) | Response `Set-Cookie` values (`bStore=Y`, `CAS_PROGRAM=foxtrot`) and the `Cookie: bStore=N; CAS_PROGRAM=alpha` probe header are recorded verbatim in `RevSourceBar.md:30,82`. Non-auth preference/experiment flags, not credentials — but they are the only cookie **values** in the round. | §3.2 |
| F6 | low (provenance) | `.ufo/reports/round-30/kasegi.md` at the fleet root was written **during round 31** (mtime 2026-10-25 21:06 −0300) and is now tracked+clean in fleet HEAD. Orchestrator-attributed (commit `e7425c1e` "landed by orchestrator after fleet .git restore"), not a seat write. | §1.4 |

---

## 0. Gate and snapshot discipline (bound 6)

Gate: "after at least 20 wave-2 receipts exist or 45 minutes".

```sh
$ ls .ufo/waves/round-31/wave2/ | wc -l        # 00:30:57Z
23   # 22 receipts + swarm-registry.json
$ ls .ufo/waves/round-31/wave2/*.md | wc -l    # 00:36:58Z
31
```

Gate was met at 00:30:57Z (23 files ≥ 20). The lane was **not quiescent** at any point in the sweep — seats landed `corpus/lessons/round-31.md`, `M corpus/instruments/limb-mutation-check.py` (ExecCounterFix) and several receipts *while* the sweep ran. Therefore:

- Every lane number below is the **2026-10-26T00:36:48Z snapshot** and nothing else.
- No PRE-STATE/after comparison is drawn anywhere; no counter value is cited.
- Re-run on quiescent bytes before citing:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git status --porcelain -uall ; git diff --name-status b374febb HEAD
# then the §9 one-liner, which prints the UNOWNED set for the tree you are reading
```

Fleet-root reads are *also* non-comparable: fleet HEAD moved twice during the sweep (`e7425c1e` → `ebccb441` "round-64: hyaku closure dispatch for kumitate"), i.e. sibling rounds commit into the same repo concurrently.

---

## 1. Fleet root — `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec)

### 1.1 The command and its blindness (F4)

```text
$ 2026-10-26T00:33:41Z ; git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261025-hyaku-run7.md
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kotoba.report-baseline
 M .ufo/state/kotodama.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/revenger.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
?? .tower/
?? demo-cwd.txt
?? .ufo/waves/round-30/
=== fleet HEAD === e7425c1eb8779233b95542d361a9383f1de518f8
```

(The 00:36:58Z read of the same command additionally shows `?? .ufo/reports/round-41/mado.md` and HEAD `ebccb441…` — the repository is moving under the sweep.)

The status stream cannot show a lane write, by construction:

```text
$ git -C /home/vgpnk/Projects/shokunin check-ignore -v kasegi-shokunin
.gitignore:1:*-shokunin/	kasegi-shokunin
```

All 20 sibling `*-shokunin` lanes (21 lanes including this one) are ignored the same way, so a write into a **sibling lane** — the exact thing bound 1 forbids — is invisible to item (1). **Exploit path:** a seat that wrote, e.g., `../mori-shokunin/corpus/x.md` leaves no trace in this command; the sweep passes while the boundary is broken. **Smallest remediation:** keep the two complements in the close-out (each is one line):

```sh
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do [ "$d" = /home/vgpnk/Projects/shokunin/kasegi-shokunin ] && continue
  git -C "$d" status --porcelain | grep -Ei 'round-31|kasegi'; done      # (no output)
find /home/vgpnk/Projects/shokunin -xdev \
  -newer /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/claims.json -type f \
  -not -path '*/.git/*' -not -path '*/.jj/*' -not -path '*/.*scratch/*' -not -path '*/*-shokunin/*' \
  -not -path '*/.ufo/state/*' -not -path '*/.ufo/watchdog.log' -not -path '*/.tower/*'
```

### 1.2 Seat-named paths at the fleet root (tight filter)

Filter: path segment starting with `kasegi` / `round-31`, or a basename beginning `Exec|Scribe|Scout|Rev|Crit|Mut` (`review*` no longer matches).

```text
$ git -C . status --porcelain -uall | grep -E '(kasegi|round-31)|/(Exec|Scribe|Scout|Rev|Crit|Mut)[A-Za-z0-9._-]*'
 M .ufo/state/kasegi.report-baseline
?? .ufo/waves/round-30/wave1/ScribeLesson.md
```

| path | mtime (−0300) | round-31 seat write? | attribution |
|---|---|---|---|
| `.ufo/state/kasegi.report-baseline` | 2026-10-25 20:07:54 | **no** (pre-freeze 20:13:08) | orchestrator state; `.ufo/state/` is a forbidden seat zone (bound 1) |
| `.ufo/waves/round-30/wave1/ScribeLesson.md` | 2026-10-25 15:58:07 | **no** (round 30, pre-freeze) | round-30 seat report written at the fleet root — already recorded in round 30's record and in `SentScopeW1.md` §1 |

`find .ufo/waves/round-30 -newer …/claims.json -type f` → **0**: nothing under the untracked round-30 directory was touched after the freeze.

Two boundary notes for the item-1 reading:

- **`.scratch/`** appears once in the fleet status (`M .scratch/goal-20261025-hyaku-run7.md`). It was **never read or written** by this seat (bounds 1 and the item's "never touch .scratch/"); the `find` complement excludes it. It is the orchestrator's own goal file, outside every seat's scope.
- **`.tower/`** (untracked, 152 files under `-uall`) is a case-insensitive false positive for a naive `Rev|Crit|Mut` filter — its `comms/reviews/**` names contain "review". It is **pre-freeze** (newest entry 2026-10-24 19:00:13 −0300), belongs to the tower/round-18/round-100 review flow, and contains nothing kasegi/round-31.

### 1.3 F3 — `demo-cwd.txt`, the one post-freeze fleet-root file with no owner

```text
$ stat -c '%s bytes %y' demo-cwd.txt ; cat demo-cwd.txt
30 bytes 2026-10-25 20:54:49.629643125 -0300
/home/vgpnk/Projects/shokunin
$ grep -rn 'demo-cwd' kasegi-shokunin/.ufo/ kasegi-shokunin/corpus/     # → no match
```

30 bytes, no trailing newline, content is the fleet root: the shape of `pwd > demo-cwd.txt` run from the fleet root at 23:54:49Z, i.e. inside the wave-1 window. **No receipt claims it**, so it cannot be attributed to a named seat. It carries no credential and no path beyond the fleet root. **Report only — not deleted** (item: "report only, never delete"). **Smallest remediation:** the L1 adds `rm demo-cwd.txt` to its own close-out after deciding it is litter, or names the writing agent; do not leave it for the next round's sweep to re-discover.

### 1.4 F6 — the kasegi round-30 report landed at the fleet root during round 31

```text
$ stat -c '%y %n' .ufo/reports/round-30/kasegi.md
2026-10-25 21:06:19.089492837 -0300 .ufo/reports/round-30/kasegi.md
$ git -C . log --format='%h %ci %s' -- .ufo/reports/round-30/kasegi.md
e7425c1e 2026-10-25 21:12:37 -0300 round-30: kasegi report — late WAVE-DONE amendment (landed by orchestrator after fleet .git restore)
e959bfc6 2026-10-25 16:01:32 -0300 round-30: kasegi report
$ git -C . status --porcelain .ufo/reports/round-30/     # (empty: tracked and clean)
```

The file is **tracked and clean**, so it is not a pending scope violation, but a kasegi round-30 artifact was written to the fleet root *during* round 31 by the orchestrator (its own commit message says so) — outside any seat's write scope, and consistent with round 30's report having closed late. No seat receipt claims it. Recorded so the L1 does not mistake it for a round-31 seat write.

`.tower/` (untracked) is **pre-freeze**: newest file inside it is 2026-10-24 19:00:13 −0300. `.ufo/reports/round-31/` at the fleet root holds ten other lanes' reports and **no** `kasegi.md`, nothing newer than the freeze.

---

## 2. Lane classification — `git -C … status --porcelain -uall`

### 2.1 The ownership contract used (wave-1 FILE OWNERSHIP, de-truncated)

The wave-1 spec's ownership line is longer than a display line; extracted in full:

| target | wave-1 owner | wave-2 owner (this wave's grants) |
|---|---|---|
| `corpus/instruments/limb-mutation-check.py` | ExecCounter | **ExecCounterFix** |
| `corpus/instruments/limb-ledger.json` | ExecLedgerMerge | **ExecCounterFix** |
| `corpus/instruments/recheck-audit.py` | ExecRALimbs | — (read-only in wave 2) |
| `corpus/instruments/source-recheck.py` | ExecSRLimbs | — |
| `corpus/instruments/frontier-recheck-count.py` | ExecFRLimbs | — |
| `corpus/instruments/limb-fixtures/sr/**` | ExecSRLimbs | — |
| `corpus/instruments/limb-fixtures/fr/**` | ExecFRLimbs | — |
| `wave1/ledger-fragments/{ra,sr,fr}.json` | ExecRALimbs / ExecSRLimbs / ExecFRLimbs | — |
| `corpus/instruments/score-gap.py` | ExecScoreGap | — |
| `corpus/instruments/README.md` (append) | ScribeInstrReadme | — |
| `corpus/instruments/knowledge-expected.txt` | ExecExpectedList | — |
| `corpus/source-snapshots/round-31/{S048.txt,manifest.json}` | ExecCapManifest | — |
| `corpus/knowledge/vendor-third-party-finding-coordination.md` | ExecEntryF15 | — |
| `corpus/SOURCES.md` | ExecRegistryAppend | — |
| `corpus/README.md` (append) | ScribeReadmeF15 | — |
| `PROVINCE.md` (append) | ScribeProvince | — |
| `SKILL.md` (append, R6) | ScribeSkillGate | — |
| `corpus/QUALITY.md` (append) | ScribeQuality | **ScribeQualityFix** |
| `LOG.md` (append) | ScribeLogR30 | — |
| `SCORECARD.md` (append) | ScribeErratum | **ScribeScorecard** |
| `corpus/knowledge/considerthese-proposals-ledger.md` (append) | ScribeConsiderthese | — |
| `wave1/<YourName>.md` | its own seat | (wave 2 uses `wave2/<YourName>.md`) |
| — | — | **ScribeLesson** → `corpus/lessons/round-31.md`; **ScribeShonen** → `SHONEN.md` |

Everything else is unowned in this round. This seat's classifier was a path→owner map built from the table above plus the wave-2 grants, with every receipt basename matched against both specs' item names (so a receipt written under a non-seat name is flagged `UNOWNED`); §9 carries the equivalent commands so the classification is reproducible without this seat's scratch script.

### 2.2 Uncommitted — 00:36:48Z snapshot

```text
=== UNCOMMITTED (git status --porcelain -uall) ===
TOTAL 47 | OWNED 33 | UNOWNED 14
```

| count | paths | owner |
|---:|---|---|
| 1 | `M corpus/instruments/limb-mutation-check.py` | ExecCounterFix (wave-2 grant; wave-1 owner ExecCounter) |
| 1 | `corpus/lessons/round-31.md` | ScribeLesson (wave-2 grant) |
| 31 | `wave2/<SeatName>.md` | that seat (all 31 names resolve to a wave-2 item; none orphaned) |

**UNOWNED (14) — none is a corpus byte or a deliverable:**

| count | paths | class |
|---:|---|---|
| 9 | `.ufo/waves/round-29/kasegi-r29-build-results.json`; `.ufo/waves/round-30/{kasegi-r30-build.ready,.dispatched,plan.err,run.err}`; `.ufo/waves/round-30/wave1/fetch/s065.pdf`; `.ufo/waves/round-30/wave1/mutant-b1/{mutant-b1-source-recheck.py,mutant-b1.diff,source-recheck.py}` | inherited round-29/30 leftovers, pre-freeze |
| 4 | `.ufo/waves/round-31/{wave1.ready,wave1.ready.dispatched,wave2.ready,wave2.ready.dispatched}` | harness dispatch sentinels |
| 1 | `.ufo/waves/round-31/wave2/swarm-registry.json` | harness |

```text
$ 2026-10-26T00:39:06Z ; git -C . status --porcelain corpus/
 M corpus/instruments/limb-mutation-check.py     # ExecCounterFix (granted)
?? corpus/lessons/round-31.md                    # ScribeLesson (granted)
count: 2
```

Exactly the two wave-2 grants, and nothing else under `corpus/`: no wave-2 seat has touched a corpus byte outside its grant. (An earlier read during this sweep, before `ScribeLesson` landed, returned 0 paths — recorded here so the two reads are not confused.) No receipt was written to `wave1/`, to the lane root, or to a sibling lane.

### 2.3 Committed — `git diff --name-status b374febb HEAD` (221 paths) — F1

```text
=== COMMITTED base..HEAD ===
TOTAL 221 | OWNED 69 | UNOWNED 152
   14  inherited round-29/30 artifact (pre-freeze, newly committed)
   26  L1/harness round-31 artifact (specs, plans, dispatch, controls, claims, assimilation)
    2  seat capture: ExecErratumCheck-before/after.txt
   61  seat scratch/fixture tree: ExecCensusDry
   24  seat scratch/fixture tree: ExecCounter-fixtures
   13  seat scratch/fixture tree: CritC1Kill-scratch
    7  seat scratch/fixture tree: ExecSRLimbs-scratch
    3  seat scratch/fixture tree: ScoutMSVR-scratch
    1  seat scratch/fixture tree: CritC2Kill-scratch
    1  harness file: wave1/swarm-registry.json
```

Owned committed: **69** — every `corpus/` byte change plus the three ledger fragments and 38 wave-1 receipts. **No unowned corpus write exists in the commit**; the production surfaces all resolve to the seat the ownership list names.

The 152 unowned are evidence plumbing. Precisely:

```text
$ git ls-tree -r -l HEAD | awk '…wave1/(ExecCensusDry|ExecCounter-fixtures|CritC1Kill-scratch|ExecSRLimbs-scratch|ScoutMSVR-scratch|CritC2Kill-scratch)/…'
ExecCensusDry            61 files   246,045 B
ExecCounter-fixtures     24 files    31,453 B
CritC1Kill-scratch       13 files    68,226 B
ExecSRLimbs-scratch       7 files    73,236 B
ScoutMSVR-scratch         3 files    89,312 B
CritC2Kill-scratch        1 file      3,755 B
                          ----------------------
                          109 files  512,027 B   (52 of them symlinks)
+ ExecErratumCheck-*.txt  2 files    15,451 B
```

**This was predicted and did not have to happen.** Wave 1's gate draft, written before the commit, says at `ScribeGateDraft.md:351`:

> "A lane-wide `git add -A` would land ~100 scratch/fixture files in the round-31 commit"

and recommends the alternative in the same paragraph: commit by explicit path (the owned list), or have each seat delete its scratch after citing it. Commit `eecad59` is the failure case the draft describes: the six scratch trees are `A` (added) in `base..HEAD`, the raw `ScoutMSVR-scratch/raw.html` is in the commit at 81,802 B, and the 52 census symlinks are committed.

**Exploit path (verifiability, not secrets):** the round-31 commit is the permanent record the next round reads. Anyone recomputing the round's evidence from the commit now must first separate 109 fixture/scratch files from 69 owned deliverables; and the raw HTML in it carries per-request telemetry (§3.3) that no claim argues for. **Impact:** the commit's provenance is diluted and its size artificially inflated; no claim becomes false (`frontier-recheck-count.py`, `source-recheck.py`, `recheck-audit.py` read `corpus/` only). **Smallest remediation:** have the L1 drop the six scratch trees and the two `ExecErratumCheck-*.txt` captures from the round-31 commit (`git rm --cached` + `commit --amend` is the L1's call, not a seat's), or, if they must stay as evidence, move them under a single sha256-pinned tarball per R14 (`corpus/QUALITY.md:83`: "a control/fixture tree larger than a few hundred kilobytes is committed as one content-addressed tarball").

### 2.4 F2 — the committed census fixture is not hermetic

```text
$ git -C . ls-tree -r HEAD | awk '$1=="120000"' | wc -l
58            # 1 round-25 + 3 round-28 + 2 round-29 + 52 round-31
$ git -C . ls-tree -r HEAD | awk '$1=="120000" && $4 ~ /round-31/' | wc -l
52            # every one of them under ExecCensusDry/validate/
$ git -C . ls-tree -r HEAD .ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/instruments
120000 blob …  .ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/instruments
```

Each link resolves **inside** the lane and none is dangling (both measured on the committed tree, not assumed):

```text
$ find .ufo/waves/round-31 -type l ! -exec test -e {} \; -print | wc -l
0                                        # no broken link
$ find .ufo/waves/round-31 -type l -exec sh -c 'for l; do t=$(readlink -f "$l"); case "$t" in /home/vgpnk/Projects/shokunin/kasegi-shokunin/*) ;; *) echo "OUTSIDE: $l -> $t";; esac; done' sh {} +
(no output)                              # no escape
$ readlink -f .ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/knowledge/ai-assisted-finding-validation.md
/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ai-assisted-finding-validation.md
```

So nothing escapes the repository. But the targets are the **live** corpus, e.g. `validate/corpus/knowledge/<entry>.md -> ../../../../../../../corpus/knowledge/<entry>.md`. **Consequence:** the committed dry-run control is not a snapshot; a future round that edits any `corpus/knowledge/*.md` changes what the committed fixture asserts while the fixture's own bytes stay identical. **Exploit path:** a later reader runs the committed control, gets a pass, and concludes that *round 31's* bytes were validated, when what ran was the *current* corpus against a control list from round 31. **Smallest remediation:** commit the fixture as a real copy (or per R14, a tarball with its sha256 in the receipt) and assert the copy's digest, exactly as wave 1's sentinel recommended (`SentScopeW1.md` §F3).

---

## 3. Credential / session / private-URL sweep over new and changed bytes since the base

### 3.1 Command, file set, result

File set = `git diff --name-only b374febb HEAD` ∪ `git status --porcelain -uall`, deduped → **267 paths**; **215** are regular files (scanned), **52** are symlinks (content is corpus/instruments, in-set by target; containment checked separately).

```sh
PAT='(api[_-]?key|apikey|secret|password|passwd|credential)s?["'\'']?[[:space:]]*[:=]|op://|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_|xox[baprs]-|AKIA[0-9A-Z]{12,}|Bearer [A-Za-z0-9._~+/=-]{8,}|(session|sid|access_token|id_token|jwt|nonce)=[A-Za-z0-9%._~+-]{6,}|cookie:|file://|hackerone\.com/reports/|bugcrowd\.com/[a-z]+/submission'
while read -r p; do [ -f "$p" ] && [ ! -L "$p" ] && grep -ainE "$PAT" "$p"; done < changed.txt
```

```text
--- regular files scanned: 215 ; matching lines: 17
```

**17 matching lines in 8 files, zero credentials.** Every hit classified by reading it:

| hit | class | verdict |
|---|---|---|
| `build-spec.py:107`, `wave1-dispatch.json:645`, `wave1-plan.out:650`, `wave1-spec.json:390` | the sentinel item text itself ("grep … for credential material patterns (token/secret/api[_-]?key/Bearer/op://)") | pattern prose, no value |
| `RevSourceBar.md:99,:103` | its own rule-6 heading and its own searched-token list (`op://`, `token=`, `session`, …, `cookie:`) | pattern prose, no value |
| `SentScopeW1.md:246,247,249,255,259,260,348` | the predecessor's pattern definitions and its §F2/§F4 findings | pattern prose, no value |
| `RevEntryQ.md:138`, `RevRowS048.md:149` | each reviewer's own `grep -nE` selector | pattern prose, no value |
| `RevSourceBar.md:30,:82` | **response cookie values** — see §3.2 | non-auth flags (F5) |

No `Authorization:` header value appears anywhere in the changed bytes (the only `authorization:` token is the searched-word list at `RevSourceBar.md:103`). No `op://`, no `-----BEGIN … PRIVATE KEY`, no `sk-/ghp_/github_pat_/xox/AKIA` value, no `Bearer` value, no private report URL, no `hackerone.com/reports/…`, no `bugcrowd.com/…/submission`, no vault reference in any round-31 file.

### 3.2 F5 — cookie values recorded verbatim (benign, but the only values in the round)

```text
$ sed -n '30p' .ufo/waves/round-31/wave1/RevSourceBar.md
  Set-Cookie: ['bStore=Y; expires=…', 'CAS_PROGRAM=foxtrot; expires=…; path=/; secure; SameSite=None']
$ sed -n '82p' .ufo/waves/round-31/wave1/RevSourceBar.md
  … probing with `Cookie: bStore=N; CAS_PROGRAM=alpha` and `Accept-Language: ja-JP` …
```

The values are one-letter/bucket flags from Microsoft's public page (`bStore=Y` is the consent-store flag; `CAS_PROGRAM=foxtrot` an experiment bucket). They are not signed session tokens and carry no account binding — the receipt itself used them as a **probe input** (rewriting `bStore=N`, `CAS_PROGRAM=alpha`) and measured an identical body. **Exploit path:** none demonstrated — a reader cannot authenticate with `bStore`/`CAS_PROGRAM`. **Impact:** a cookie-shaped value now lives in a receipt; a future automated sweep will flag it again and spend review time. **Smallest remediation:** describe the probe as "the page's two preference cookies, values redacted" and keep the measured `no_trace_sha256`/`msvr_body_sha256` cells, which are what the claim actually rests on.

### 3.3 Telemetry identifiers in the committed raw HTML (F1 evidence)

```text
$ git -C . show HEAD:.ufo/waves/round-31/wave1/ScoutMSVR-scratch/raw.html | grep -c CVToken
6
$ … | grep -cE 'Trace Id|expToken|propertyToken'
4
$ git -C . cat-file -s $(git -C . rev-parse HEAD:.ufo/waves/round-31/wave1/ScoutMSVR-scratch/raw.html)
81802
```

Committed content includes `CVToken: CASMicrosoftCV33b0a016.{0,1,2}`, one `var expToken = { … "propertyToken": "8c1e142d-…", "visitorJsHash": …, "expJsHash": … }` block, and one `Trace Id`. These are public experiment/correlation identifiers served to every visitor — no auth power — but they are **per-request**, which is why wave 1's sentinel said they must not be committed (`SentScopeW1.md` §3.3: "See F2 for why they must not be committed"). They are now in the round-31 commit. Tracked under F1; the capture pin itself (`corpus/source-snapshots/round-31/S048.txt`, sha256 `2001ad77…e55`) is unaffected and remains the asserted artifact.

---

## 4. Campaign package `/home/vgpnk/Projects/shokuknow` — read-only, untouched

```text
$ 2026-10-26T00:34:23Z ; git -C /home/vgpnk/Projects/shokuknow status --porcelain | wc -l
1918
$ find /home/vgpnk/Projects/shokuknow -newer …/kasegi-shokunin/.ufo/waves/round-31/claims.json \
       -not -path '*/.git/*'
/home/vgpnk/Projects/shokuknow/.git          ← 1 entry, a directory
$ git -C /home/vgpnk/Projects/shokuknow status --porcelain | grep -i kasegi | wc -l
9       # merge/kasegi/{MERGE-REPORT.json,MERGE-REPORT.md,SOURCES.append.md} + ?? lanes/kasegi/round1{3..6}/ + 3 ?? merge/kasegi/knowledge/… — all pre-existing
```

**Zero files** newer than the freeze; **zero** content writes. The 1918 modified paths and the nine kasegi-named ones are pre-existing (every one predates `claims.json`; they are the package's own long-standing state). The single `.git` mtime refresh is caused by read-only `git status` (this seat's and every seat's), the same effect wave 1 recorded. Campaign tools were never invoked; nothing was fetched from that tree.

---

## 5. Live-target sweep — every fetch command in the round's receipts

Round-31 fetch lines were extracted mechanically (`curl|wget` on a line; plus `capture-source.py --url`, `urllib`, `requests`, `http.client`, `nc -`, `ssh`, `scp`, `ftp`):

```text
$ grep -rnE '(^|[^\w/.-])(curl|wget)\s' .ufo/waves/round-31          # 32 lines
$ python3 extract-hosts.py                                            # distinct hosts
  23  www.microsoft.com
   8  shokunin.invalid        # inside the instrument UA string, not a target
```

`urllib|requests|http.client|socket|nc -|ssh |scp |ftp` → the only line is `SentScopeW1.md:313`, which is the predecessor's own grep. **No second host is contacted by any round-31 seat.**

| receipt | executed fetch | host | allowed? |
|---|---|---|---|
| `wave1/ScoutMSVR.md:5,12` | `curl -sSL` + `capture-source.py` | `www.microsoft.com` | yes — the URL the item names |
| `wave1/ExecCapManifest.md:10,29` | 2 × `capture-source.py --url` | `www.microsoft.com` | yes |
| `wave1/CritC2Kill.md:35,41` | `curl` + `capture-source.py` | `www.microsoft.com` | yes |
| `wave1/RevSourceBar.md:23-40` | 7 recorded fetch/probe results (2 `fetch` lines, 2 baselines, `Accept-Language` ja/zh, cookie probe) | `www.microsoft.com` | yes |
| `wave2/ScoutLiveDrift.md:6-9` | `curl` + 2 × `capture-source.py` | `www.microsoft.com` | yes (its item: re-open the page) |
| `wave2/RevQuoteRoutes.md:32-42` | 2 independent GETs | `www.microsoft.com` | yes |
| `wave2/RevQuoteRoles.md:29-31` | 1 × `capture-source.py` | `www.microsoft.com` | yes |
| `wave2/RevRowS048.md:18,44` | 1 × `capture-source.py` + 1 `curl -D -` | `www.microsoft.com` | yes |

All eight seats fetched the **same public documentation path**, `https://www.microsoft.com/en-us/msrc/msvr`, GET only:

```text
$ grep -rnE 'curl[^|]*(-X *POST|--data|-d |--form|-F )|wget[^|]*--post' .ufo/waves/round-31 --include='*.md'
(no match)
$ grep -rnE '(curl|wget|capture-source\.py|urllib)[^\n]*msrc\.microsoft\.com' .ufo/waves/round-31 --include='*.md'
(no match)
```

No submission, no form body, no authenticated endpoint, no ticket/portal URL, no `hackerone.com/reports/` request. Non-executed hosts in the round's text are quotations: staged-package ids (`zc.cnvd.org.cn`, `std.samr.gov.cn`, `openstd.samr.gov.cn`, `std.sacinfo.org.cn`, `security.360.cn`, `security.bilibili.com`, `www.sac.gov.cn`), corpus citations (`www.cisa.gov`, `www.cve.org`, `www.first.org`, `www.ipa.go.jp`, `cwe.mitre.org`, `www.iso.org`, …), the instrument UA (`shokunin.invalid`), and page chrome inside the captured HTML (`bat.bing.com`, `www.clarity.ms`, `*.liveperson.net`, `cdnssl.clicktale.net`, …). Full census from the round tree: **76 distinct hosts in text; 1 ever fetched.**

**Rate observation, not a defect:** the same URL was fetched by eight seats in ~65 minutes (20 recorded `status=200` fetch/probe results) because each falsification seat re-opened it independently. That is what the wave asked for; if the fleet wants fewer identical fetches, the L1 can name one capture seat per wave and have reviewers verify against the pinned bytes.

---

## 6. R14 size check — new files over 300 KB under `.ufo/waves/round-31`

```text
$ find .ufo/waves/round-31 -type f -size +300k -printf '%s %p\n'
(no output)
$ find .ufo/waves/round-31 -type f -size +300k | wc -l
0
```

Zero files exceed 300 KB in the round tree. Largest (for scale): `wave2-dispatch.json` 88,600 B; `wave2-plan.out` 88,093 B; `wave1-dispatch.json` 83,509 B; `wave1-plan.out` 83,042 B; `ScoutMSVR-scratch/raw.html` 81,802 B; `wave2-spec.json` 70,846 B; `wave1-spec.json` 67,741 B.

The **aggregate** rule is a different question and it is breached by R14's own wording (see F1): a fixture tree "larger than a few hundred kilobytes" must be a tarball or regenerated — `ExecCensusDry` alone is **246,045 B / 61 files**, and all six scratch/fixture trees total **512,027 B / 109 files**. Repo growth is measurable, as R14 asks: tree size `b374febb` = 100,551,143 B → HEAD = 103,255,600 B (**+2,704,457 B**), of which round-31 wave-1 = 1,228,831 B, inherited round-30 wave-1 = 732,244 B (incl. a 513,648 B `s054.pdf`), then `corpus/` = 265,883 B; the four root markdown files' committed blob sizes are `LOG.md` 118,881 B, `SKILL.md` 96,028 B, `SCORECARD.md` 83,705 B, `PROVINCE.md` 4,007 B (sizes, not added bytes — their diffs are append-only per the ownership list).

One blob over 300 KB *was* newly committed by the round-31 commit, outside the item's scoped directory: `.ufo/waves/round-30/wave1/fetch/s054.pdf` (513,648 B), an inherited round-30 fetch artifact. It is pre-existing content, not a round-31 capture; noted so the size question is answered completely.

---

## 7. Findings, exploit paths, smallest remediation

| # | Sev | Exploit path | Impact | Smallest remediation |
|---|---|---|---|---|
| F1 | med | Read the round-31 commit as evidence: 109 fixture files, 52 symlinks and one 81,802 B raw page (6 `CVToken`, 1 `expToken` block) now sit beside 69 owned deliverables; a future reader must re-derive which bytes the round argued for. Wave 1 predicted this at `ScribeGateDraft.md:351` and the commit took the scratch anyway. | Provenance dilution, not a false claim: all counters read `corpus/` only. | L1 drops the six scratch trees + two `ExecErratumCheck-*.txt` captures from the round-31 commit (or folds them into one sha256-pinned tarball per R14). |
| F2 | med | Run the committed `ExecCensusDry` control after a future round edits `corpus/knowledge/*.md`: it passes against today's corpus while the receipt it backs describes round-31 bytes. | The committed control cannot be replayed against a fixed snapshot. | Replace the 52 symlinks with a real copy (or tarball + digest) and assert the copy's sha256. |
| F3 | low | `demo-cwd.txt` proves a process wrote at the fleet root after the freeze; no receipt claims it, so attribution fails and the file survives into the next round's sweep. | Litter at the fleet root; no credential. | L1 decides and removes it in its own close-out (not a seat write). |
| F4 | low | A seat writes into a sibling lane: fleet-root `git status` shows nothing because `.gitignore:1:*-shokunin/` hides every lane. | Item (1) cannot fail for the failure it exists to catch. | Keep the two complement commands (§1.1) in every close-out. |
| F5 | low | A future sweep re-flags `bStore`/`CAS_PROGRAM` in `RevSourceBar.md:30,82` and spends review time on non-auth flags. | Review noise; no auth value. | Describe the probe with values redacted; keep the measured digests. |
| F6 | low | A round-30 lane report written to the fleet root during round 31 could be mis-attributed to a wave-2 seat. | Attribution only; content is the orchestrator's own commit. | Record in the round-31 LOG/lesson that it is orchestrator-attributed (this receipt is the evidence). |

**Non-findings, verified rather than assumed:** no unowned `corpus/` byte in the commit (69/69 owned); no wave-2 seat wrote outside its grant (`corpus/` clean except the two granted files); no receipt written to `wave1/`, the lane root or a sibling lane; no placeholder left unexpanded in a wave-2 receipt (the 33 `{inst}` / 13 `{root}` matches are the counter contract's own kill-command placeholders, correctly quoted); no lane `git`/`jj` mutation by a seat (`.jj` newest write 21:16:54 −0300 = the L1's own commit; no receipt carries a `jj` command); `.git/index` mtime 21:18:35 −0300, 103 s *after* the L1's commit, i.e. not a seat write.

---

## 8. Limits of this sweep

- **Non-quiescent snapshot.** Wave 2 was still landing when the sweep ran (22 → 31 receipts during it; `limb-mutation-check.py` and `corpus/lessons/round-31.md` appeared mid-sweep). §2.2 is the 00:36:48Z count. A path written after that instant is not classified here; re-run `classify2.py` on quiescent bytes (bound 6).
- **Fleet-root attribution is by path name plus each sibling lane's own `git status`.** A kasegi seat writing a generically named file into a sibling lane between two reads would not be attributed; the `find -newer` complement bounds it to files newer than the freeze.
- **Credential scanning is pattern-based text scanning** over 215 regular files. It cannot see a secret in a shape no pattern names (e.g. an opaque base64 blob with no keyword). The 52 symlinks were not re-scanned by content (their targets are the lane's own `corpus/`), and the committed `s054.pdf` was not decoded as text.
- **I judged no claim and ran no counter.** C1/C2 truth is the other seats' subject; this receipt reports scope, ownership, credential posture and fetch discipline only.
- **No live value asserted.** Eight seats fetched `https://www.microsoft.com/en-us/msrc/msvr`; this seat fetched nothing and repeats none of their live results.

## 9. Reproduce

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git -C /home/vgpnk/Projects/shokunin status --porcelain                     # §1
git -C /home/vgpnk/Projects/shokunin check-ignore -v kasegi-shokunin        # §1.1
git -C . diff --name-status b374febbb33ccadade78a787279707fd5d2e6e1d HEAD    # §2.3
git -C . ls-tree -r -l HEAD | awk '$1=="120000"'                             # §2.4
git -C /home/vgpnk/Projects/shokuknow status --porcelain                     # §4 (read-only)
grep -rnE '(^|[^\w/.-])(curl|wget)\s' .ufo/waves/round-31                    # §5
find .ufo/waves/round-31 -type f -size +300k                                 # §6
```

The unowned list of §2.2 is reproducible without this seat's scratch script — the map of §2.1 is the whole classifier:

```sh
git status --porcelain -uall | sed 's/^...//; s/^"//; s/"$//' | grep -vE '^(corpus/instruments/(limb-mutation-check|limb-ledger|recheck-audit|source-recheck|frontier-recheck-count|score-gap)\.py|corpus/instruments/(README\.md|knowledge-expected\.txt)|corpus/instruments/limb-fixtures/(sr|fr)/|corpus/source-snapshots/round-31/(S048\.txt|manifest\.json)|corpus/knowledge/(vendor-third-party-finding-coordination|considerthese-proposals-ledger)\.md|corpus/(SOURCES|README|QUALITY)\.md|corpus/lessons/round-31\.md|PROVINCE\.md|SKILL\.md|LOG\.md|SCORECARD\.md|SHONEN\.md|\.ufo/waves/round-31/wave1/ledger-fragments/(ra|sr|fr)\.json|\.ufo/waves/round-31/wave(1|2)/[A-Za-z0-9_-]+\.md)$'
# → the 14 UNOWNED paths of §2.2 (run 00:36:48Z-equivalent tree); count check: 14
```

Caveat: that one-liner accepts **any** `wave1|wave2/*.md` as a receipt. This seat's classifier additionally matched every receipt basename against the wave-1 and wave-2 spec item names; **0** receipts were orphaned (all 31 resolve to a seat). To re-check that part:

```sh
python3 - <<'PY'
import json,re,os
lane='.'
names={i['name'].lower() for f in ('wave1-spec.json','wave2-spec.json') for i in json.load(open('.ufo/waves/round-31/'+f))['items']}
for w in ('wave1','wave2'):
    for f in os.listdir(f'.ufo/waves/round-31/{w}'):
        m=re.fullmatch(r'([A-Za-z0-9_-]+)\.md',f)
        if m and m.group(1).lower() not in names: print('ORPHAN',w,f)
print('orphan check done')
PY
```
