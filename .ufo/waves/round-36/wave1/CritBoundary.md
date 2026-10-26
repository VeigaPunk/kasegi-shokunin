# CritBoundary — round-36 scope sweep (fleet root / sibling lanes / shokuknow / credentials / git-jj / cross-seat receipts)

Seat: `CritBoundary` (critic, leaf). Milestone: round-36. Judged on: **scope**.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `cc692008b0cfd58d18275aa6c4aed79620120799`,
claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`).

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/CritBoundary/`
(removed after this receipt was written). No lane, fleet, sibling-lane or source-tree file was edited;
no mutating git/jj command was run; no tool was installed or upgraded (tooling authorization unused);
no subagent was spawned; `agent://all` was not messaged.

**Verdict: 2 boundary defects found (1 fleet-root write, 1 transient lane-dir creation), both cleaned by
the offending seat; 5 of the 6 scanned categories are clean on all evidence I could reach. The residual
risk is systemic, not incidental: all 74 wave-relevant sessions run with `cwd` = the fleet root, so the
dispatch's own relative `Report:` trailer path points *into the fleet root*.**

---

## 1. What was swept (coverage before any claim below)

| surface | count | how |
|---|---|---|
| seat prompts (wave1-spec items) | 64 | parsed `wave1-spec.json` → `items[].prompt` |
| delivered prompts (`taskCall.tasks[].task`) | 64 | `wave1-dispatch.json` |
| non-receipt wave artifacts | 11 files | `build-spec.py` 45 780 B, `wave1-spec.json` 347 380 B, `wave1-dispatch.json` 371 403 B, `wave1-plan.out` 370 676 B, `wave1.ready`, `wave1.ready.dispatched`, `census-before.txt`, `claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`, `wave1/swarm-registry.json` |
| seat transcripts (authoritative action record) | 74 sessions | `~/.omp/agent/sessions/-Projects-shokunin/2026-10-26T15-10-35-484Z_01a178c3-.../ *.jsonl` — 64 wave seats + 10 foreign rounds (`main`, `SoujiR33`, `TabiR32`, `TameshiR48a3`, …) |
| tool calls in the 64 wave seats | **3 887** | `bash` 2 779, `read` 439, `edit` 252, `write` 212, `eval` 82, `yield` 65, `grep`/`glob` 46, `wait` 12 |
| landed peer receipts scanned | **55** (list in §7) | receipts present in `wave1/` at scan time, re-scanned as late arrivals landed; seats still landing are named in §7 |

Two independent instruments, deliberately different in kind: (a) text scan of every prompt/artifact/receipt
for the six violation families; (b) **action** sweep of every seat transcript for `write`/`edit` targets and
for `bash` write operators (`>`, `>>`, `tee`, `cp`, `mv`, `rm`, `mkdir`, `sed -i`, `ln`, `chmod`) whose
operand resolves outside the lane. (b) is what makes the negative results load-bearing: a receipt can omit a
write, a transcript cannot.

---

## 2. FINDING 1 — fleet-root write (confirmed, cleaned, and contradicted by the seat's own receipt)

**Seat:** `ScribeRowS053` (scribe, coverage).
**Category:** fleet-root write (`/home/vgpnk/Projects/shokunin` outside the lane).

Primary evidence, in order of occurrence:

1. Session `cwd` recorded as `/home/vgpnk/Projects/shokunin` (`ScribeRowS053.jsonl`, `type:"session"`).
2. Tool call `write` with `arguments.path = ".ufo/waves/round-36/wave1/ScribeRowS053.md"` — a **relative**
   path. Resolved against (1) this is `/home/vgpnk/Projects/shokunin/.ufo/waves/round-36/wave1/ScribeRowS053.md`,
   i.e. it created `.ufo/waves/round-36/` and `wave1/` **under the fleet root**. The seat's own next command
   is labelled `"Checking where receipt landed"` and lists exactly that fleet directory.
3. Cleanup (verbatim, one command):

   ```
   set -e
   mkdir -p /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-36/wave1
   cp /home/vgpnk/Projects/shokunin/.ufo/waves/round-36/wave1/ScribeRowS053.md \
      /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-36/wave1/ScribeRowS053.md
   rm -- /home/vgpnk/Projects/shokunin/.ufo/waves/round-36/wave1/ScribeRowS053.md
   rmdir /home/vgpnk/Projects/shokunin/.ufo/waves/round-36/wave1 /home/vgpnk/Projects/shokunin/.ufo/waves/round-36
   ```

4. Residue check (this seat, now): `ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-36` →
   `No such file or directory`; `find /home/vgpnk/Projects/shokunin/.ufo -maxdepth 3 -name round-36` →
   only `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36` (**pre-existing**: dir mtime
   `2026-10-26 02:13`, newest file `kaidoku.md` 02:23, both before the 12:34 dispatch — not this wave).
   Fleet `.ufo/waves` dir mtime `12:39` corroborates a create-then-delete inside it.

**Secondary defect (false statement in a landed receipt):** `ScribeRowS053.md:10` states
> "This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r36/ScribeRowS053/`
> (removed after the receipt was written). **No lane, fleet, sibling-lane or source-tree file was edited**".

A fleet file *was* created and deleted, so that sentence is false as written, and the receipt nowhere
discloses the slip (its only `fleet` occurrence is that line). The event is recorded **only by a peer**:
`RevRowS053.md:53` — "**Fleet-write slip, cleaned:** the scribe self-reports the receipt was first written by
relative path into the fleet-root `.ufo/`, then copied to the lane and the stray copies removed. I verified:
no `round-36` directory exists under `/home/vgpnk/Projects/shokunin/.ufo/waves/` …".

Impacted axes: `depth:verifiability` — see §6(c): a fleet-root write is invisible to every limb of E9, so a
round can be "lane-quiescent" while a seat has written outside its scope. `coverage` unaffected (the drafted
row/entry content is not implicated; the byte-level review of the row is `RevRowS053`'s and `CritC2Claim`'s).

---

## 3. FINDING 2 — transient lane-repo directory created by an executor (self-disclosed, cleaned)

**Seat:** `ExecC1SuiteBuild`. **Category:** lane-repo write (outside the seat's allowed write scope; not
fleet/sibling/shokuknow, so it is outside the letter of my six families but inside the seat contract's
"never edit any file in the lane repo").

Evidence: transcript bash `bash r36-closure.sh … --work /home/vgpnk/Projects/shokunin/kasegi-shokunin/tmpwork`
followed by `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && rmdir tmpwork`; the seat discloses it at
`ExecC1SuiteBuild.md:192`:

> "the first revision of the guard did create an empty dir; I removed it with `rmdir`, lane
> `git status --porcelain` count unchanged at 9, and reordered the guard".

Later runs of the same guard left no trace (`tmpwork2`, `tmpwork3` → `absent`), and the seat ran an `strace`
proof that the final instrument opens no lane path with write flags. Net state verified now:
`git -C <lane> status --porcelain` has **0** tracked entries and only untracked `.ufo/waves/round-36/` wave
artifacts. Impact: none on bytes; the guard defect was fixed in the artefact itself.

---

## 4. Clean results (each with the check that could have failed)

| category | result | discriminating check |
|---|---|---|
| fleet-root writes | **1** (§2) | every `write`/`edit` arg resolved against session `cwd`; every `bash` write operator whose operand is `/home/vgpnk/Projects/shokunin` and **not** `/…/kasegi-shokunin`. Foreign-round seats (`SoujiR33`, `TabiR32`, `TameshiR48a3`) write only **their own** lane repos and are excluded as out-of-wave. |
| sibling-lane writes | **0** | same sweep with `…/*-shokunin` operands; no wave seat wrote any lane but kasegi. Reads only (`ExecSiblingSweep`, `ScoutF19Sibling`, `ConnSibling` — per their items). |
| shokuknow writes | **0** | `shokuknow` appears in wave artifacts only as the read-only statement and in read operands: `…/merge/kasegi/SOURCES.append.md` passed to `collide-check.sh` (`ScribeAssimilationGate.md:206,209`), `ScoutIdCollisions` staged-id extraction, `…/doctrine/` greps (`ScoutF19Sibling`, `ConnPatterns`, `ConnSibling`). No `cp`/`mv`/`rm`/redirection with a shokuknow operand. |
| credential material | **0** | `op://`, `ghp_`, `github_pat_`, `sk-`, `AKIA`, `xox?`, PEM headers, `api_key=`/`secret=`/`token=` over all 74 transcripts and all 54 receipts, plus URL-credential forms (`user:pass@`, `X-Amz-Signature`, `sig=`, `token=`, `?key=`) and private hosts (`127.0.0.1`, `localhost`, `10.`, `192.168.`). Only hits: `op://vault/item` and `-----BEGIN OPENSSH PRIVATE KEY-----` **as regex literals inside `SentSecrets`' own scanner source** (`/fast/scratch/…/SentSecrets/scan_wave.py`) — detection patterns, not key material. URL inventory across receipts: `www.first.org` ×43, `www.cisa.gov` ×1, `shokunin.invalid` ×2 (the instrument UA's reserved-TLD host). |
| git/jj mutation instructions | **0** instructions; 11 fixture runs (+2 greps that only *match* the words) | receipts and artifacts contain only read-only subcommands (`archive`, `rev-parse`, `cat-file -e`, `merge-base --is-ancestor`, `ls-tree`, `ls-files`, `status --porcelain`); the single `git worktree` regex hit is the prose "lane is a git worktree" (`ExecGateReviewPrep.md:91`). `jj`: **0** occurrences of any mutating verb in prompts, receipts or transcripts. Bash mutating-git calls (11; the other two matches are greps over receipt text by this seat and `SentScope`) all target scratch fixtures: `CritC1Kill:$S/fakelane*`, `ExecC1ExportMode:$S/G` (asserts `rev-parse --show-toplevel` = `$S/G`), `ScribeMistakes:$S/clean`,`$S/dirty`, `SimplC1:$S/green` (toplevel equality asserted, `cp -a .git` from the lane is read-only on the source), `RevC1Selftest:$S/fix` (`git clone` into scratch + toplevel equality), `ExecQuiescenceProbe:$S/sandbox/fix.*`. Observation (not a violation): `CritC1Kill`'s fixture `init` uses a fixed scratch path and asserts no toplevel in that call — safe because the path is under its own scratch, but it is looser than the dispatched `mktemp` + verified-toplevel form. |
| a seat writing another seat's receipt | **0** | 64/64 delivered prompts carry exactly one anchored `Report:` line, and its path is `.ufo/waves/round-36/wave1/<own name>.md` (0 mismatches); 0 `write`/`edit` calls targeting another seat's receipt; 0 `bash` redirections into `wave1/<other>.md`. Cross-seat receipt **mentions** are citations only, e.g. `ScribeRowS053.md:56` "capture owned by ExecC2Capture, not this seat", `ExecGateReviewPrep.md:597-604`, `ScribeLOG.md:54-92`, `MutJunkTwin.md:97,129,138` — the right direction of provenance, not a write. |

---

## 5. False-positive ledger (what a text-only sweep would have reported wrongly)

I discarded these after reading the context; recording them so the negative results stay auditable:
`git merge-base --is-ancestor` matched by a `git merge` pattern (6 receipts); `grep -rln` matched by an `ln`
operator; `sed -n` reads; `cat`/`printf` fixture writes whose base variable is `$F`/`$G`/`$d`/`$SB`/`$S/…`
(all under `/fast/scratch/hyaku/kasegi-r36/<own seat>/`); `CritC1Export`'s and `CritC1Kill`'s
`…/wave1/L1Integration.md` writes (they write `$F/.ufo/waves/round-34/wave1/L1Integration.md` inside a
fixture — the name collides with a seat-name regex, the path does not); `ScribeAssimilationGate.md:17`
("nothing written under `…/shokuknow`") and `CritC2Kill.md:180` ("`shokuknow`, `~/Projects/*` untouched") —
negated statements. Wave artifacts' 340 off-lane references each are the read-only boilerplate sentence or a
sanctioned read operand (`/…/scripts/sources-census.sh`, `…/merge/kasegi/…`, `…/doctrine/…`).

---

## 6. Root cause and the smallest safe corrections

**(a) Root cause (measured, not inferred).** All 74 sessions in the wave's session directory report
`cwd = /home/vgpnk/Projects/shokunin` — the fleet root — while the seat contract tells each seat that the
`Report:` trailer path is *relative to the lane*. Any seat that hands that relative path to a path-taking tool
lands its receipt in the fleet root. `ScribeRowS053` is the one that did; the other 63 used absolute paths or
`cd <lane> &&` heredocs. Correcting the seat after the fact cannot fix the next wave.

**(b) Smallest safe correction, in order of value:**
1. **Dispatcher:** spawn wave seats with `cwd` = the lane repo (`/…/kasegi-shokunin`), or rewrite the trailer
   absolute in every prompt. One-line change, removes the entire class (all 64 seats are exposed, not just the
   one that slipped). Verify by `type:"session".cwd` in each new transcript.
2. **Disclosure:** append one correction line to `ScribeRowS053.md` (or the wave erratum file) recording the
   fleet-root write, its path, and the `rm`/`rmdir` cleanup, because line 10 as landed is false. Not mine to
   land (my write scope is this receipt + scratch); `RevRowS053.md:53` already carries the substance if the
   aggregator prefers to cite it.
3. **Claim-side, flagged not judged (C1's owners decide):** E9's three limbs are lane `status --porcelain`,
   `find <scratch-root>` and `head-match`. A fleet-root write satisfies all three. If quiescence is to mean
   *scope* quiescence, E9 needs a fourth limb — absence of `{fleet}/.ufo/waves/round-36` — otherwise the
   round can be closed on bytes produced after a seat wrote outside its lane. This is the strongest
   counterexample I can build against the C1 predicate from local evidence, and it is cheap to close.

Conversely, I found **no** defect in: prompt/trailer identity (64/64), shokuknow writes, sibling-lane writes,
credential material, git/jj mutation instructions, or cross-seat receipt writes. Nothing in this report
changes a claim, a route, an axis or a score.

---

## 7. Limits (stated so the L1 can scope the negative results)

- **55 peer receipts** were present when the sweep closed — 53 at the first pass, plus `ScribeGateLesson`
  and `ScribeReportDraft` scanned as they landed. This receipt is excluded from its own negative results
  (it necessarily contains the strings it hunts for): `ConnC1C2, ConnPatterns, ConnSibling, CritC1Export,
  CritC1Kill, CritC2Claim, CritC2Kill, CritMotivation, ExecAncestry, ExecC1BaseFail, ExecC1ExportMode,
  ExecC1Fixtures, ExecC1SuiteBuild, ExecC2Capture, ExecC2Harness, ExecC2JunkControl, ExecC2QuoteOnce,
  ExecCensusReplay, ExecDatawalk, ExecGateReviewPrep, ExecInstrumentsSynopsis, ExecManifestChecks,
  ExecQuiescenceProbe, ExecRegressionBase, ExecScoreGap, ExecSiblingSweep, MutC1Fixtures, MutC2Row,
  MutJunkTwin, RevC1Suite, RevClaimsFreeze, RevEntryF19, RevHarnessSync, RevRowS053, RevSourceRecheck,
  RevSpotCheckReadiness, ScoutCaptureAvailability, ScoutF19Open, ScoutF19Sibling, ScoutIdCollisions,
  ScoutQuarantine, ScoutStandingRefusals, ScribeAssimilationGate, ScribeConsiderthese, ScribeEntryF19,
  ScribeGateLesson, ScribeLOG, ScribeMistakes, ScribeQualityRows, ScribeReportDraft, ScribeRowS053,
  ScribeSOURCSCorrection, ScribeScorecard, ScribeShonen, SentScope, SimplC1`. Seats that had **not** landed
  a receipt at that instant are covered by the transcript action sweep (64/64) but **not** by the receipt
  text sweep; their receipts need the same three greps in §8 before filing.
- The action sweep sees tool calls, not what a shell did internally: a command that writes via a script the
  seat did not author (e.g. `bash .ufo/waves/round-35/assimilation/collide-check.sh`) is judged by its
  operands. Where it mattered I used the seat's own proof (`strace` in `ExecC1SuiteBuild`) or the lane's
  `git status --porcelain` (0 tracked modifications) instead.
- `ExecC1SuiteBuild.md:192`-class slips are invisible to E9 by construction (an empty directory never shows in
  `git status`); I report them from the transcript, which is why the transcript sweep exists.

## 8. Reproduction (all read-only)

```
# 1. prompt/artifact text sweep (trailers, cross-seat receipt paths, credentials, git/jj, off-lane operands)
python3 - <<'PY'
import json,re
t=json.load(open('.ufo/waves/round-36/wave1-dispatch.json'))['taskCall']['tasks']
for x in t:
    m=re.findall(r'^Report:\s*(.+)$',x['task'],re.M)
    assert len(m)==1 and f'.ufo/waves/round-36/wave1/{x["name"]}.md' in m[0], x['name']
print('64/64 trailers point at own receipt')
PY

# 2. action sweep: write/edit + bash write operators, resolved against session cwd
#    (sessions: ~/.omp/agent/sessions/-Projects-shokunin/2026-10-26T15-10-35-484Z_01a178c3-*/<seat>.jsonl;
#     filter toolCall blocks; classify path as fleet / source / lane-receipt / own-scratch / peer-scratch)

# 3. residue + lane state
ls -d /home/vgpnk/Projects/shokunin/.ufo/waves/round-36        # -> No such file or directory
find /home/vgpnk/Projects/shokunin/.ufo -maxdepth 3 -name round-36   # -> only reports/round-36 (pre-existing)
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | grep -v '^?? \.ufo/waves/round-36/' | wc -l   # -> 0
```

axis: scope → 1 fleet-root write (ScribeRowS053, cleaned, undisclosed in its own receipt) + 1 transient
lane-dir creation (ExecC1SuiteBuild, self-disclosed, cleaned); sibling/shokuknow/credentials/git-jj/
cross-receipt all clean; root cause is a uniform fleet-root `cwd` for all 74 wave sessions.
