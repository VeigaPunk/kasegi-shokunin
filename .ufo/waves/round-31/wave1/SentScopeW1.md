# SentScopeW1 — scope, credential and live-target sweep (round 31, wave 1)

- **Seat:** sentinel, `SentScopeW1`; lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `b374febbb`, claims-freeze `738a779`, HEAD at sweep `8a8916c7043bd873d191b30dd1744b241b91f4d9`.
- **Answering model:** `devin/deepseek-v4-1-flash` (config route table; no model passed to any call).
- **Writes by this seat:** this receipt only. No git/jj mutation, no `git add`, no counter run of another seat's claim, no tooling installed (nothing to install — the sweep is coreutils + git + python3 stdlib + the `read`/`grep` tools).
- **Lane scratch:** none created. Two transient files were written to `/tmp` by an early pipeline (`/tmp/lane_paths.txt`); no lane or fleet path was touched outside this receipt. Nothing was deleted anywhere.

## Verdict

**No credential material, no session/private URL, no live bounty target contact, and no out-of-lane write by a round-31 seat.** Three scope-hygiene findings are reported (F1 fleet-root blindness, F2 126 unowned/scratch paths, F2 non-hermetic census fixture root), one provenance observation (F2), and one in-flight read anomaly (F2), each with the smallest remediation. Findings F1–F2 are **reported only** — this seat has no remediation scope this wave.

---

## Gate — receipt polling (item: ≥15 receipts, cap 40 min)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/wave1
deadline=$((SECONDS+2400))
while :; do n=$(ls -1 *.md 2>/dev/null | wc -l); ... [ "$n" -ge 15 ] && break; ... sleep 20; done
```

```text
t=151s receipts=5
t=191s receipts=6
t=211s receipts=7
t=251s receipts=10
t=271s receipts=11
t=291s receipts=12
t=411s receipts=13
t=511s receipts=15
=== final receipts (15) ===
ConnClaims.md ConnSibling.md ExecCapManifest.md MutFRExisting.md MutRAExisting.md
MutSRExisting.md RevClaimsFreeze.md RevSourceBar.md ScoutDatawalk.md ScoutF15Sweep.md
ScoutMSVR.md ScoutPackageThemes.md ScoutRALimbMap.md ScribeErratum.md ScribeLogR30.md
```

Gate met at t=511 s, well inside the 40-minute cap. The sweep then ran over the tree as it stood; by the end of the sweep `ls -1 *.md | wc -l` = **27**, so seats were still landing.

## Snapshot discipline (bound 6 — in-flight bytes are non-comparative)

The lane tree changed under every read. Consecutive `git status --porcelain -uall | wc -l`:

| read (UTC) | count | note |
|---|---:|---|
| ~23:32Z | 33 | first probe (before the ≥15-receipt gate) |
| ~23:36Z | 335 | seats mid-flight; `CritC2Kill-scratch/junk-root/…` held a full corpus copy (164 paths) |
| ~23:37Z | 337 | grew between two adjacent calls |
| ~23:38Z | 322 | `CritC2Kill` began cleaning its junk-root |
| 23:42:47Z | 178 | junk-root gone; `ExecCensusDry/validate` copy tree still present |
| 23:43:01Z | 180 | **classification snapshot below** |

Every number in §2 is that 23:43:01Z snapshot and nothing else. No PRE-STATE / after comparison is drawn anywhere in this receipt; where a claim counter moved during the sweep (SOURCES.md, F5) both reads are shown and labelled.

---

## 1. Fleet root — `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec)

```text
SWEEP_UTC=2026-10-25T23:38:17Z
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
?? .ufo/waves/round-30/
?? .ufo/waves/round-41/w1/ExecQuarantineSlice.md
=== fleet HEAD === 5bfdf50ba7bf480220a13576971a0623e69b2daf
```

`git status --porcelain -uall` expands the one untracked directory to a single file, so the seat-name filter (`kasegi|round-31|Exec|Scribe|Scout`) returns exactly three paths:

```text
 M .ufo/state/kasegi.report-baseline
?? .ufo/waves/round-30/wave1/ScribeLesson.md
?? .ufo/waves/round-41/w1/ExecQuarantineSlice.md
```

| path | mtime | round-31 seat write? | classification |
|---|---|---|---|
| `.ufo/state/kasegi.report-baseline` | 20:07:54 −0300 | **no** (pre-freeze 20:13:08) | orchestrator state; `.ufo/state/` is a forbidden write zone for seats (bound 1) — the orchestrator, not a seat, owns it |
| `.ufo/waves/round-30/wave1/ScribeLesson.md` | 15:58:07 −0300 | **no** (round 30) | round-30 seat report written at the **fleet root** instead of the lane — an out-of-lane write, but from round 30 and pre-freeze; already visible in the round-30 record |
| `.ufo/waves/round-41/w1/ExecQuarantineSlice.md` | 19:58:53 −0300 | **no** (round 41) | another lane's seat (`# ExecQuarantineSlice — seat report (w1, round 41)`), pre-freeze |

`.scratch/` was never read or written; only its directory mtime was taken (`2026-10-25 17:07:14 −0300`, pre-freeze). No deletion was performed anywhere.

### F1 — the fleet-root `git status` is structurally blind to every lane

```sh
git -C /home/vgpnk/Projects/shokunin check-ignore -v kasegi-shokunin
```

```text
.gitignore:1:*-shokunin/	kasegi-shokunin
```

`kasegi-shokunin` (and all 20 sibling `*-shokunin` lanes: `audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kengaku kotoba kotodama kumitate lore mado mori revenger souji tabi tameshi tsukuroi`) are gitignored at the fleet root, so **no lane write can appear in the fleet-root status at all** — including a write into a *sibling* lane, which is exactly what bound 1 forbids. The git-only check in item (1) therefore cannot fail for the failure it exists to catch. Complement run (read-only), two ways:

```sh
# (a) content- and path-level: any changed path in a sibling lane naming this round or lane
for d in *-shokunin; do [ "$d" = kasegi-shokunin ] && continue; git -C "$d" status --porcelain | grep -Ei 'round-31|kasegi'; done
# (b) fleet-wide mtime sweep for non-lane files newer than the claims freeze
find . -xdev -newer kasegi-shokunin/.ufo/waves/round-31/claims.json -type f \
  -not -path './.git/*' -not -path './.scratch/*' -not -path './kasegi-shokunin/*' \
  -not -path './.ufo/state/*' -not -path './.ufo/watchdog.log'
```

```text
(a) → (no output: no sibling lane holds a changed path naming round-31 or kasegi)
(b) → 2844 files; first lines:
    ./.ufo/reports/round-46/tameshi.md
    ./.ufo/reports/round-48/mori.md
    ./.ufo/reports/round-56/kake.md
    ./.ufo/prompts/closure/tameshi-round-46.md
    ./.ufo/prompts/closure/mori-round-48.md
    ./.ufo/prompts/closure/kake-round-56.md
    ./.ufo/prompts/tameshi-round-47.md  ./.ufo/prompts/mori-round-49.md  ./.ufo/prompts/kake-round-57.md
    ./kake-shokunin/.git/objects/…
```

The 2844 are other lanes' own concurrent rounds (`tameshi` r46/47, `mori` r48/49, `kake` r56/57 …) and their git object stores — not attributable to a kasegi seat, and none carries a kasegi/round-31/Exec/Scribe/Scout name. `find . -name '*round-31*' -path './kasegi-shokunin' -prune -o -print` returns only the orchestrator's `.ufo/reports/round-31/` (no `kasegi.md` there yet; nothing under it newer than the freeze) and per-lane `.ufo/prompts/closure/<lane>-round-31.md` closure prompts.

**Smallest remediation:** keep the two complement commands in the L1 close-out (they are one line each) — do not rely on the fleet-root status alone for bound 1.

---

## 2. Lane classification — `git status --porcelain -uall`, 23:43:01Z snapshot

Command: the porcelain stream was classified by an inline path→owner map built from the round-31 FILE OWNERSHIP list (exact paths, the two `limb-fixtures/{sr,fr}/**` prefixes, the three `ledger-fragments/{ra,sr,fr}.json`, and `wave1/<Seat>.md` → that seat's own receipt).

```text
TOTAL 180 | OWNED 54 | UNOWNED 126
```

### Owned (54) — every one resolves to a named seat, no orphan

| paths | owner |
|---:|---|
| 2 `corpus/source-snapshots/round-31/{S048.txt,manifest.json}` | ExecCapManifest |
| 1 `corpus/instruments/limb-mutation-check.py` | ExecCounter |
| 1 `corpus/knowledge/vendor-third-party-finding-coordination.md` | ExecEntryF15 |
| 1 `corpus/instruments/knowledge-expected.txt` | ExecExpectedList |
| 7 `corpus/instruments/frontier-recheck-count.py` + 6 `limb-fixtures/fr/**` | ExecFRLimbs |
| 1 `corpus/instruments/limb-ledger.json` | ExecLedgerMerge |
| 2 `corpus/instruments/recheck-audit.py` + `wave1/ledger-fragments/ra.json` | ExecRALimbs |
| 1 `corpus/SOURCES.md` | ExecRegistryAppend |
| 6 `corpus/instruments/source-recheck.py` + `limb-fixtures/sr/**` (4) + `ledger-fragments/sr.json` | ExecSRLimbs |
| 1 `corpus/instruments/score-gap.py` | ExecScoreGap |
| 1 `SCORECARD.md` | ScribeErratum |
| 1 `LOG.md` | ScribeLogR30 |
| 1 `PROVINCE.md` | ScribeProvince |
| 1 `corpus/QUALITY.md` | ScribeQuality |
| 1 `corpus/README.md` | ScribeReadmeF15 |
| 26 `wave1/<Seat>.md` receipts | each its own seat (ConnClaims, ConnOwnership, ConnSibling, CritC2Kill, ExecCapManifest, ExecCensusDry, ExecEntryF15, ExecErratumCheck, ExecFRLimbs, ExecRALimbs, ExecSRLimbs, ExecScoreGap, MutFRExisting, MutRAExisting, MutSRExisting, RevClaimsFreeze, RevSourceBar, ScoutDatawalk, ScoutF15Sweep, ScoutMSVR, ScoutPackageThemes, ScoutRALimbMap, ScribeErratum, ScribeLogR30, ScribeProvince, ScribeReadmeF15) |

Not yet changed at the snapshot (owners idle or in flight, not a defect): `SKILL.md` (ScribeSkillGate), `corpus/instruments/README.md` (ScribeInstrReadme), `corpus/knowledge/considerthese-proposals-ledger.md` (ScribeConsiderthese).

Byte-level check of the six ` M` entries — all six really differ from HEAD (no phantom `M`):

```text
corpus/SOURCES.md                       wt=9b906580c50c head=44920041fe1a DIFF diffnumstat=3/0
corpus/README.md                        wt=dc9c20771c30 head=be773ed1c0a0 DIFF diffnumstat=25/0
corpus/instruments/knowledge-expected.txt wt=9471c496fc34 head=566985d1dffa DIFF diffnumstat=1/0
PROVINCE.md                             wt=adf701525640 head=abace490277c DIFF diffnumstat=20/0
LOG.md                                  wt=5d466fc57636 head=b8d2bca16c33 DIFF diffnumstat=115/0
SCORECARD.md                            wt=39e7373e2a6d head=77856a9afc89 DIFF diffnumstat=25/0
corpus/instruments/recheck-audit.py     wt=14c6aaabf41c head=dbfcff579cad DIFF diffnumstat=45/6
corpus/instruments/source-recheck.py    wt=49a230b45104 head=b80172bc171a DIFF diffnumstat=13/1
```

Forbidden zones (bound 1) inside the lane are clean — `git status --porcelain | grep -E '\.ufo/state/|\.ufo/watchdog\.log|MANIFEST\.json|templates/|scripts/'` → `NONE`; `.git/index` mtime 20:28:12 (pre-sweep, from the dispatch export) and `git reflog` shows only `export from jj` entries with HEAD unchanged at `8a8916c`.

### F2 — UNOWNED (126 of 180): scratch, fixtures, inherited leftovers, L1 artifacts

No UNOWNED path is a corpus byte or a round-31 deliverable. Complete inventory (every path named; the 44 symlinked knowledge entries are collapsed to one counted selector because they are one homogeneous set):

```sh
git status --porcelain -uall | grep '^?? \.ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/knowledge/'   # → 44
```

| count | paths |
|---:|---|
| 22 | **inherited round-29/30 leftovers** (routed defect 1, pre-existing): `.ufo/waves/round-29/kasegi-r29-build-results.json`; `.ufo/waves/round-30/{c1-controls/c1-after.txt,kasegi-r30-build.ready,kasegi-r30-build.ready.dispatched,plan.err,run.err}`; `.ufo/waves/round-30/wave1/{ConnHarm.md,CritMeta.md,ExecControlC1.md,RevC1Controls.md,fetch-manifest.sha256,fetch/s037.html,fetch/s048.html,fetch/s054.pdf,fetch/s054.txt,fetch/s065.pdf,fetch/s065.txt,fetch/s068.html,mutant-b1/mutant-b1-source-recheck.py,mutant-b1/mutant-b1.diff,mutant-b1/source-recheck.py}` |
| 1 | ` M .ufo/waves/round-30/wave1/ExecRegistryAppend.md` — **tracked** round-30 receipt, +8 lines appended 20:37:04 −0300 by the round-30 seat of that name ("Post-handoff note — S048 belongs to round 31, not this seat"). Not a round-31 write; it is a round-30 receipt edited during round 31, so a round-31 commit would carry a round-30 file — the L1 should decide explicitly (see F2 note below). |
| 5 | L1 / harness: ` M .ufo/waves/round-31/build-spec.py`, `.ufo/waves/round-31/{wave1.ready,wave1.ready.dispatched,wave2-items.py}`, `.ufo/waves/round-31/wave1/swarm-registry.json` |
| 8 | `CritC1Kill-scratch/`: `build-ledgers.py`, `contract-literal-counter.py`, `degenerate-ledger.json`, `degenerate-ledger-controls.json`, `honest-survivor-ledger.json`, `one-degenerate-limb-ledger.json`, `prove-attacks.py`, `vacuous-signal-ledger.json` |
| 1 | `CritC2Kill-scratch/live.txt` |
| 61 | `ExecCensusDry/`: `validate/controls.py`, `validate/corpus/README.md`, `validate/corpus/SOURCES.md`, `validate/corpus/instruments` (dir symlink), **44 symlinked knowledge entries**, `validate/corpus/source-snapshots/round-31/S048.txt`, and the control roots `validate/{pre,ctl-dup-id,ctl-dup-url,ctl-dangling-usedby}/corpus/{SOURCES.md,instruments,knowledge}` (3+3+3+3) |
| 17 | `ExecCounter-fixtures/`: `{green,killed,survivor,controls,controls-mismatch,invalid-find-count,invalid-find-twice,invalid-live-baseline,invalid-nocompile,invalid-noop,invalid-timeout,smoke-real,integration-13}.json`, `integration-13.out`, `transcript-fast.txt`, `timeout-run.txt`, `lane/corpus/instruments/probe.py` |
| 2 | `ExecErratumCheck-before.txt`, `ExecErratumCheck-after.txt` |
| 7 | `ExecSRLimbs-scratch/`: `pristine.py`, `mutant-SR-stem-mismatch.py`, `mutant-SR-occurrence-not-unique.py`, `mutant-accept-not-found.py`, `kill-sim.txt`, `proof.txt`, `rechecks.txt` |
| 3 | `ScoutMSVR-scratch/`: `raw.html`, `S048.txt`, `S048b.txt` |

**Exploit path (commit hygiene, not a corpus defect):** a lane-wide `git add -A` would land ~100 scratch/fixture files in the round-31 commit — including three copies of the MSVR capture, the raw 81,802-byte MSVR HTML, 13 counter fixture ledgers, and 52 symlinks that point into `corpus/`. The census and the counters only scan `corpus/`, so the *claims* would still hold, but the commit would carry evidence blobs the round never argued for, and F4's per-request identifiers would enter the repo. **Smallest remediation:** commit by explicit path (the 54 owned paths above, which is also what the ownership table already implies), or have each seat delete its `*-scratch/`/`*-fixtures/` directory after its receipt cites it. `CritC2Kill` already did the latter for its 164-path junk-root during this sweep.

**Note on the tracked round-30 receipt:** its appended text is coordination-only and internally consistent with the landed bytes it cites (see F4). If the L1 does not want a round-30 file in the round-31 commit, the append must be dropped by its round-30 owner — not by a round-31 seat (this seat wrote nothing there).

### F3 — the census dry-run root is symlinked into the live corpus (fixture is not hermetic)

`ExecCensusDry`'s `validate/` roots are **not** copies of the knowledge/instruments trees — they are relative symlinks into the live lane corpus:

```text
$ find .ufo/waves/round-31/wave1 -type l | wc -l
52
$ find .ufo/waves/round-31/wave1 -type l -printf '%p -> %l\n' | grep -v '/corpus/knowledge/'
…/ExecCensusDry/validate/corpus/instruments              -> ../../../../../../../corpus/instruments
…/ExecCensusDry/validate/pre/corpus/knowledge            -> ../../corpus/knowledge
…/ExecCensusDry/validate/pre/corpus/instruments          -> ../../corpus/instruments
…/ExecCensusDry/validate/ctl-dup-id/corpus/knowledge     -> ../../corpus/knowledge
…/ExecCensusDry/validate/ctl-dup-id/corpus/instruments   -> ../../corpus/instruments
…/ExecCensusDry/validate/ctl-dup-url/corpus/knowledge    -> ../../corpus/knowledge
…/ExecCensusDry/validate/ctl-dup-url/corpus/instruments  -> ../../corpus/instruments
…/ExecCensusDry/validate/ctl-dangling-usedby/corpus/{knowledge,instruments} -> ../../corpus/{knowledge,instruments}
# plus 44 per-file links, e.g.
…/ExecCensusDry/validate/corpus/knowledge/ai-assisted-finding-validation.md -> ../../../../../../../../corpus/knowledge/ai-assisted-finding-validation.md
```

Containment check — every one of the 52 resolves **inside** the lane (no escape to the fleet root or the package):

```sh
find .ufo/waves/round-31/wave1 -type l -exec sh -c 'for l; do t=$(readlink -f "$l"); case "$t" in /home/vgpnk/Projects/shokunin/kasegi-shokunin/*) ;; *) echo "OUTSIDE: $l -> $t";; esac; done' sh {} +
# → (no output)
```

Only two files in the control roots are real: `validate/corpus/SOURCES.md` (differs from the lane's, as the control intends) and `validate/corpus/knowledge/vendor-third-party-finding-coordination.md` (a control entry). The consequence is a trust-boundary weakness, not a landed defect: (a) a tool that wrote under a `validate/` root would write **through** into the live corpus, and (b) the dry-run control tests control `SOURCES.md` against *live* knowledge bytes, so its independence is weaker than a copy-based fixture would be. No write-through occurred: the lane's 43 pre-existing knowledge files are unchanged in `git status`, and `corpus/instruments` shows no unexpected `M`. **Smallest remediation:** have the census tool refuse a root whose corpus tree contains symlinks (`os.walk(..., followlinks=False)` + an `lstat` guard on `corpus/knowledge`), or build the fixture from real copies. Do not commit the 52 links (F2).

---

## 3. Credential material and session/private URLs in the lane's new/changed bytes

Patterns (two passes, case-insensitive where it matters):

```text
A: (?i)(token|secret|api[_-]?key|apikey|password|passwd|credential)s?\s*[:=]\s*\S+ | Bearer\s+[A-Za-z0-9._~+/=-]{8,} | op://
B: op:// | -----BEGIN …PRIVATE KEY | sk-[A-Za-z0-9]{16,} | ghp_[A-Za-z0-9]{20,} | github_pat_ | xox[bpas]- | AKIA[0-9A-Z]{12,}
   | Bearer\s+[A-Za-z0-9._~+/-]{12,} | (api[_-]?key|secret|token|password)\s*[:=]\s*["'][A-Za-z0-9_./+-]{12,}
C: (?i)session=|sid=|auth=|access_token|op://|localhost|127\.0\.0\.1|192\.168\.|10\.[0-9]+\.[0-9]+\.[0-9]+|file://
   | hackerone\.com/reports/ | bugcrowd\.com/[a-z]+/submission | /home/vgpnk
```

Pass A over `.ufo/waves/round-31` (all 100+ seat files, receipts and scratch), pass B over `corpus/`, over `LOG.md SCORECARD.md PROVINCE.md`, and over the inherited `.ufo/waves/round-{29,30}` leftovers; pass C over `corpus/source-snapshots/round-31/S048.txt`, `corpus/source-snapshots/round-31/manifest.json`, `corpus/knowledge/vendor-third-party-finding-coordination.md`.

**Result: zero real credentials, zero session URLs, zero `op://` vault references, zero private report URLs.**

Every hit is one of three benign classes, each verified by reading the line:

1. **Pre-existing schematic mentions in files this round did not change** — `corpus/instruments/citation-survival.tsv:127,944,1237` (the strings `op://` and `sk-/ghp_/github_pat_/xox/AKIA/private-key` used as *sweep selectors*), `corpus/lessons/round-5-aggregator-audit.md:50`, `round-6-aggregator-audit.md:31`, `round-9-aggregator-corpus-verdict.md:18,40`. None is in `git status`.
2. **Spec/pattern text** — `round-30/wave1/SentSecretScan.md:7` reads `Patterns checked: common credential/token/private-key forms, assignment-style secret values, literal op://, URLs`; the round-30/31 `build-spec.py`, `*-spec.json`, `*-dispatch.json`, `plan.out`, `run.out` hits are the same pattern strings quoted in dispatch prose (this receipt's own item text is one of them).
3. **Code identifiers** — `TOKEN = re.compile(...)` in `density.py:52`, `resolve.py:102`; `tokens = path_tokens(line)` in `recheck-audit.py:129`; `"Bare marked trailer, not a token: "` in `anchorcheck.py:291`. Not values.

Session/private-URL pass C over the three new corpus files: the only match is the standard recheck line's own lane path —

> `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py …`
> — `corpus/knowledge/vendor-third-party-finding-coordination.md:4`

which is the lane's canonical recheck form (Q7), not a private URL. `PROVINCE.md`'s +20 appended lines and `SCORECARD.md`'s +25 appended lines contain no credential, no URL and no private path; `LOG.md`'s +115 lines reference the read-only campaign package once (`LOG.md`, added line: `read-only merge package /home/vgpnk/Projects/shokuknow/merge/kasegi/`), which is the package path this round is authorized to read.

### F4 — per-request identifiers in the capture (benign; a provenance fact, not a leak)

The committed snapshot carries one per-request identifier, which is why its digest is not reproducible by refetch:

```text
$ sed -n '2p' corpus/source-snapshots/round-31/S048.txt | cut -c1-24
This is the Trace Id: f9
$ sha256sum corpus/source-snapshots/round-31/S048.txt
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55   (97 lines, 3755 B)
$ diff corpus/source-snapshots/round-31/S048.txt .ufo/waves/round-31/wave1/ScoutMSVR-scratch/S048.txt
2c2   (only line 2 differs; differing-line count = 2)
$ sha256sum .ufo/waves/round-31/wave1/ScoutMSVR-scratch/{S048.txt,S048b.txt}
78dbb989f257db1f21dd6c8c5b67d20341d60bc8f8e71f52a9472b42259828f4   S048.txt
43b3737a32b62487ec78ed44161c70b3634e59bd42f831568dd9efe934481593   S048b.txt
```

The landed bytes match `corpus/source-snapshots/round-31/manifest.json`'s `sha256` (`2001ad77…`) exactly, so `source-recheck` is stable against the pin; the scout's and the second capture's digests differ **only** on line 2. A `Trace Id` is a per-request correlation id with no auth power, and the manifest already documents it as a quirk; the actionable rule is the one the seats already wrote: **never substitute a fresh recapture for the pinned bytes**.

The raw HTML scratch files carry Microsoft's public page telemetry — `CVToken: CASMicrosoftCV<hex>.<n>` (6 occurrences in `ScoutMSVR-scratch/raw.html`) and one `var expToken = { … "propertyToken": "8c1e142d-…" }` block. These are public experiment/correlation ids served to every visitor, not credentials or cookies; they exist only in untracked scratch, and `CritC2Kill` has already reduced its own copy to `live.txt` (one `Trace Id` line, no `CVToken`). See F2 for why they must not be committed.

---

## 4. Campaign package `/home/vgpnk/Projects/shokuknow` — read-only, untouched

```sh
git -C /home/vgpnk/Projects/shokuknow status --porcelain | wc -l          # 1918
find . -newer …/kasegi-shokunin/.ufo/waves/round-31/claims.json -not -path './.git/*'   # → ./.git  (1 entry, a directory)
find . -not -path './.git/*' -newermt '-6 hours' -type f | wc -l          # 0
```

- The 1918 modified paths are **pre-existing** (round10/11/12 lane material, `MANIFEST.json`, `audit-wave.py`, …); every one predates the claims freeze.
- **Zero files** newer than `claims.json`; **zero files** newer than six hours. No seat wrote there.
- The single `newer` hit is the `./.git` directory itself, whose mtime is refreshed by read-only `git status` (this seat's and other seats' status calls). No git object, ref or index content was written by this seat: only `status`/`find`/`ls` were run, and campaign tools were never invoked.

---

## 5. Live-target contact — receipts' `curl`/`wget` lines and their hosts

Every receipt, then every file under `.ufo/waves/round-31` (scratch included), was scanned for fetch commands:

```sh
grep -nE '(^|[^a-zA-Z])(curl|wget) ' *.md                       # receipts
grep -rnE '(^|[^a-zA-Z])(curl|wget) ' .ufo/waves/round-31        # incl. scratch + scripts
grep -nE '\b(urllib|requests\.|httpie|nc -|ssh |scp |ftp )' *.md  # other network tools → no match
```

| receipt | line | host | executed? | allowed? |
|---|---|---|---|---|
| `ScoutMSVR.md:5` | `## Fetch (curl -sSL, instrument UA)` | `https://www.microsoft.com` | **yes** (200, 81802 B) | yes — the MSVR page named by the item |
| `CritC2Kill.md:35,249` | `curl -sSL -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" …` | `https://www.microsoft.com` (`shokunin.invalid` is inside the UA string, not a target) | **yes** (live re-fetch for drift) | yes — same page |
| `ConnSibling.md:283` | quoted recheck cell `recheck: 180d — curl -sSL https://www.microsoft.com/en-us/msrc/msvr ...` | `https://www.microsoft.com` | no — a quote of the staged row | yes |
| `ExecCapManifest.md:7,10` | `## 1. Capture (lane instrument, no curl fallback)` + `python3 corpus/instruments/capture-source.py --id S048 --url https://www.microsoft.com/en-us/msrc/msvr` | `https://www.microsoft.com` | **yes**, via the lane instrument | yes |
| `ScoutPackageThemes.md:47,60,81` | staged `recheck:` payloads piped to `bash -n` (`curl … -o bili.pdf && pdftotext …`) | staged-package URLs (see table below) | no — parsed, not run | yes — staged-package URLs |
| `RevSourceBar.md:23` | UA string and `capture-source.py` normalization note | `shokunin.invalid` (UA) | **yes** (own live comparison) | yes |

**Hosts appearing anywhere in the 27 receipts, with provenance** (every one accounted for):

| host | count | where | contacted? |
|---|---:|---|---|
| `www.microsoft.com` | 25 | ScoutMSVR, CritC2Kill, ExecCapManifest, ConnSibling, RevSourceBar | **yes** (MSVR page only) |
| `example.invalid` | 3 | RevClaimsFreeze (placeholder in the frozen-claims quotes) | no |
| `zc.cnvd.org.cn` | 2 | ScoutPackageThemes (staged ids S034/S081) | no |
| `std.samr.gov.cn` | 2 | ScoutPackageThemes, ExecCensusDry (staged id S082 / a control copy) | no |
| `hackerone.com` | 2 | ExecCensusDry, ExecRegistryAppend, RevClaimsFreeze, ScoutDatawalk, ScoutPackageThemes, ScribeLogR30 (registry row S043/S028 citations) | no — never on a `curl`/`wget` line |
| `www.sac.gov.cn`, `www.cve.org`, `std.sacinfo.org.cn`, `openstd.samr.gov.cn`, `security.bilibili.com`, `security.360.cn` | 1 each | ScoutPackageThemes / ExecCensusDry — staged package ids S077, S079, S081, and the cn-crowd entries | no |
| `uhf.microsoft.com`, `learn.microsoft.com` | 1 each | RevSourceBar (HTML chrome / doc link cited from the capture) | no |
| `shokunin.invalid` | 1 | CritC2Kill, RevSourceBar (instrument UA) | no |

The five query-string URLs in receipts are document-id citations from the staged package, not session parameters:

```text
https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3
https://std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A5DFDD818E05397BE0A0AFD6C
https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=57CAF3B46207A7D43649E9BE15AEA0C0
https://std.sacinfo.org.cn/gnoc/queryInfo?id=E8261DDA41842E54E073557BFF2F9E7B
https://zc.cnvd.org.cn/news/info?id=133&newsTypeCode=100100
```

No bounty platform, no program scope host, no credential endpoint and no `op://` reference was contacted. One private-tree path appears in a receipt, as a **quotation of the lane's own PROVINCE text** — `ConnSibling.md:173`: `"Domain: bounty & security research — scopes ~/Projects/bounties, program rules, claim packages"`; it is a quote of an existing corpus line, adds no new private path, and this seat's `PROVINCE.md` diff (+20 lines) introduces none.

---

## 6. Corpus state observed at the end of the sweep (not this seat's claim, recorded for the L1)

Measured 23:46Z, in-flight: `frontier admitted rows` = 15; `^\| S048 \|` rows = 1; `^source: S048 ` entries = 1; registry rows = 48. Not compared to any frozen before-column.

### F5 — one contradictory in-flight read, recorded rather than smoothed over

At ~23:41Z, in adjacent calls, `git status --porcelain -uall -- corpus` reported ` M corpus/SOURCES.md` while `git diff -- corpus/SOURCES.md` printed **nothing** and `grep -cE '^\|\s*S048\s*\|'` returned **0**. At 23:46Z the same diff shows `3/0` added lines and the row count is 1. There is no `.gitattributes` in the lane (so no diff filter can explain it); the two reads straddle the append by `ExecRegistryAppend`. Both outputs are recorded above and **no conclusion in this receipt rests on the earlier read**. **Smallest remediation:** the L1 re-runs the C2 counters once on quiescent bytes before committing (bound 6 / M30-3).

---

## Limits of this sweep

- The lane was **not quiescent** at any point: 33 → 337 → 322 → 178 → 180 paths during the sweep, 15 → 27 receipts. §2 is a 23:43:01Z snapshot; a path written after that instant is not classified here.
- Credential scanning is pattern-based over text; it cannot detect a secret encoded in a form none of the three patterns names (e.g. a base64 blob with no keyword). No binary files under `corpus/` were decoded (the round-30 `fetch/*.pdf` are inherited leftovers and were not opened as text).
- Fleet-root attribution relies on path names plus each sibling lane's own `git status`; a kasegi seat writing a generically-named file into a sibling lane between two reads would not be attributed. The `find -newer` sweep bounds it to files newer than the freeze (2844, all traced to other lanes' rounds and git object stores).
- `Captures`: `ScoutMSVR.md` records the instrument-UA fetch (`code=200 … size=81802`); this seat did not re-fetch anything and asserts no live value of its own.
