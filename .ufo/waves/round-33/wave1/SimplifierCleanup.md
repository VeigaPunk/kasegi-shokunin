# SimplifierCleanup — wave-evidence leftover/duplicate scan (round 33, wave 1)

Seat `SimplifierCleanup` (simplifier, leaf — no subagent dispatch, no background job of its own).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`;
claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`.
Answering model: `opencode-go/deepseek-v4.1-flash` (route table decided; no model passed by this seat).
Tools installed or upgraded: **none** — no pacman transaction (host-wide pause respected), no `uv`/`npx`,
no official-binary download; `python3` stdlib + coreutils only. No git/jj mutation, no network fetch,
no write outside the lane. `/home/vgpnk/Projects/shokuknow` never touched.

Write scope exercised: this receipt plus its evidence directory
`.ufo/waves/round-33/wave1/SimplifierCleanup/` (`scan.py`, `scan.json`). The scan itself is read-only:
`{WD}` = `.ufo/waves/round-33` was never modified.

Scratch: `/fast/scratch/hyaku/kasegi-r33/SimplifierCleanup/` (`HYAKU_SCRATCH` unset → operator default),
removed before this receipt was finalised (§8 proves removal).

**Observation window and state label (bound 6).** Receipts were still landing while this seat ran
(45 receipts at 04:33Z, 62 at the 04:57:20Z scan; this receipt is the 63rd; `CritMistakes` had not
landed). Every count below is **PRE-STATE for receipt-set completeness**: it is the state of `{WD}`
at `2026-10-26T04:57:20Z`, not the wave's final content. Nothing here is compared to an "after" column.
Re-run command in §7.

## 0. Method

One committed scanner, `wave1/SimplifierCleanup/scan.py` (4,575 B, sha256
`5975091ccf1e68917e2d2106bc9efc58b53c6cf726a65fe7ff93a8453f22a6bd`), reads `{WD}` and reports sizes,
sha256 per file, digest groups, 0-byte files, scratch-token references, and a per-receipt evidence
census (fenced blocks, 4-space-indented code lines, `$` command lines). Its output is committed as
`wave1/SimplifierCleanup/scan.json` (51,365 B, sha256
`88230d950a80a1c5f1b568ddde547371cc3033c9d7dce43d0306fb88b6402f8d`); every number in §1–§6 is read
from that file or from the single-command checks quoted inline.

```
$ python3 /fast/scratch/hyaku/kasegi-r33/SimplifierCleanup/scan.py --root . --json > /fast/scratch/hyaku/kasegi-r33/SimplifierCleanup/scan-final.json
$ mv /fast/scratch/hyaku/kasegi-r33/SimplifierCleanup/scan-final.json wave1/SimplifierCleanup/scan.json
$ python3 -c 'import json;d=json.load(open("wave1/SimplifierCleanup/scan.json"));print(d["files"],d["bytes"],len(d["receipts"]))'
144 1604842 62
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T04:57:20Z
```

The output is written outside the tree first (a `>` redirect into a scanned file would truncate it before
the walk reads it). The 144-file total **includes this seat's two evidence files as they stood during
the scan** (`scan.py` 4,575 B, the previous `scan.json` 49,307 B); the committed `scan.json` is 51,365 B,
2,058 B larger than the copy that was counted, and this receipt adds its own size on top.

## 1. Files larger than 1 MB — none

`big=[]`: no file under `{WD}` exceeds 1,048,576 B. Largest five (bytes, sha256 truncated to 16 hex):

| bytes | sha256 (16) | path |
|---|---|---|
| 98,685 | `a2fcc8ea7a0268f7` | `wave1-dispatch.json` |
| 97,958 | `6dbf96f618c6164d` | `wave1-plan.out` |
| 72,624 | `5e61d0d0ddc1cd59` | `wave1-spec.json` |
| 65,308 | `d8eaa98761bc5e5c` | `build-spec.py` |
| 51,365 | `88230d950a80a1c5` | `wave1/SimplifierCleanup/scan.json` (this seat's evidence) |

Total at scan time: **144 files / 1,604,842 B**, of which `wave1/` holds 122 files / 1,243,697 B and the
four infra files (dispatch, plan, spec, generator) hold 334,575 B. The growth is driven by per-seat evidence directories, not by
single large files — the largest *receipt* is `wave1/ExecWaveEvidencePack.md` (34,389 B at scan time,
34,470 B at 05:00Z).
No single-file cleanup candidate exists on the >1 MB criterion.

## 2. Duplicate files (same sha256 under two or more names)

**Receipts (`.md`) are unique**: `sha256sum wave1/*.md | awk '{print $1}' | sort | uniq -d` → no output;
62 receipts carry 62 distinct digests. All duplicates are *side evidence* written by seats that re-ran
the same command and saved each run:

| sha256 (16) | copies | bytes each | paths |
|---|---|---|---|
| `1861fec846ca9a5c` | 9 | 714 | `wave1/ExecCaptureBinding/{live-postappend-run1,live-postappend-run2,live-recheck-current,live-recheck-current2}.txt`, `wave1/ExecRegressionC1/{bind-run1,bind-run2}.txt`, `wave1/ScribeSkillGate/{run1,run2,run3}.txt` — the same 9-line `MANIFEST …` inventory |
| `46bf84ca634c6431` | 3 | 879 | `wave1/ExecRegressionC1/{q1,q2,q3}.txt` — the same 4-file `sha256sum` block |
| `9c61334e369b2a41` | 2 | 744 | `wave1/ExecCaptureBinding/selftest-run2.txt`, `wave1/ScribeSkillGate/selftest-final.txt` — the same 9-case `selftest` table |
| `e3b0c44298fc1c14` | 2 | 0 | `wave1-plan.err`, `wave1-run.err` (see §4) |

Cleanup shape: each group collapses to one file plus a `sha256sum` citation in the seat's receipt; the
repeated copies add 7 × 714 + 2 × 879 + 1 × 744 = 7,500 B of redundant evidence and, more importantly,
make three seats' receipts cite different paths for identical bytes. This is a *presentation* defect,
not a fabrication: identical bytes across seats is cross-seat reproduction and should be named as such
in one place instead of stored nine times.

## 3. Scratch trees and `/tmp` paths embedded in evidence

Two different measurements, kept separate:

- **Receipts naming a scratch token** (`HYAKU_SCRATCH`, `/fast/scratch`, `/tmp/`): 50 of 62 receipts —
  this is the *sanctioned* scratch location and naming it is required by the round's scratch rule, so a
  token hit alone is not a defect.
- **Distinct scratch trees named**: 34 paths of the form `/fast/scratch/hyaku/kasegi-r33/<Seat>` across
  30 receipts. **No receipt embeds a copied tree**: no directory listing and no `find` output of a
  scratch root is pasted anywhere. Four receipts cite a *subpath they built inside their own* tree
  (`…/ExecCensusDry/validate/`, `…/ExecErratumCheck/baseroot/`, `…/ExecBeforeReceipts/root/`,
  `…/ScribeInstrReadme/e2/`), always as one output line naming that path; `wave1/` itself contains only
  four seat evidence directories (`ExecRegressionC1` 95,376 B / 22 files, `ScribeSkillGate` 85,682 B / 8,
  `ExecCaptureBinding` 22,430 B / 16, `ScribeInstrReadme` 14,937 B / 11) — all bounded command output,
  none a mirror of `corpus/`.
- **Absolute `/tmp` paths** appear in 4 receipts
  (`grep -rcE '(^|[^A-Za-z0-9._/-])/tmp/' wave1/*.md | grep -v ':0$'` →
  `ExecDeterminism.md:2`, `ExecNoHarmFinal.md:1`, `ExecScratchDiscipline.md:33`, `SentScopeFinal.md:1`):

| receipt | lines | verdict |
|---|---|---|
| `wave1/ExecScratchDiscipline.md` | 33 | residue inventory of `/tmp` (its own subject matter); paths are named as findings, not used as evidence |
| `wave1/ExecDeterminism.md` | 2 | a **deliberate precedence probe**, not an accidental fallback: `:172 SPY mkdtemp dir='/tmp' path='/tmp/capture-binding-selftest-ca3wqtcy'` runs under `env -u HYAKU_SCRATCH TMPDIR=/tmp`, and the same probe shows the `HYAKU_SCRATCH` branch resolving to `/fast/scratch/hyaku`. The `/tmp` path is a printed proof of the `$TMPDIR` branch and is not citable as the fixture root (bound 12); the citable root is the second run's |
| `wave1/SentScopeFinal.md` | 1 | `:159 $ ls -l /tmp/kasegi-*.txt` — a residue check, output shows no file |
| `wave1/ExecNoHarmFinal.md` | 1 | `:88` — the *pattern* `/fast/scratch\|/tmp/\|HYAKU_SCRATCH` inside a `git grep`, not a path |

Also note `wave1/ScribeInstrReadme/append-only.txt` matches `/tmp/` only as a substring of a quoted
citation (`.ufo/rounds/round-21/tmp/…`): **false positive**, not a scratch path.

- **Trees still on disk**: at the 04:57Z scan three existed — `CritMistakes` (seat then running),
  `ExecWaveEvidencePack`, and this seat's own `SimplifierCleanup`. At `2026-10-26T05:00:21Z` only
  `ExecWaveEvidencePack` remains, as a 45,654 B tree (`assemble.py`, `census.txt`, `hash-check.txt`,
  `index-wave.py`, `index.md`, `receipt-draft.md`, `render-index.py`, `role-coverage.txt`,
  `size-summary.txt`) whose receipt had already landed at 34,470 B. That is a leftover tree for
  `ExecScratchDiscipline` to rule on; this seat removed its own tree (§8) and does not judge the peer's.

## 4. Empty files (0 bytes) — 2, neither a receipt

`wave1-plan.err`, `wave1-run.err` — both `e3b0c44298fc1c14…` (the empty digest), committed in `a6a5023`.
They are *null* evidence: the plan/run emitted no stderr. **No receipt is 0 bytes.** A 0-byte file cannot
say what it means, so if the L1 keeps them the report should state "planner and runner stderr empty"
once; otherwise the two files are the only deletion candidates in this class (2 B of inode, 0 B of
information).

## 5. Prose-only receipts (no command output in block form) — 1

Criterion: zero fenced blocks **and** zero 4-space-indented code lines **and** zero `$` command lines.

| receipt | bytes | fences | indented | `$` |
|---|---|---|---|---|
| `wave1/ConnClaims.md` | 14,545 | 0 | 0 | 0 |

`ConnClaims.md` (226 lines, sha256 `9bff4afc112800d7…`) is a claim-pattern critique whose evidence is
quoted *inline* — e.g. `records=40 bound=38 unbound=2`, `selftest cases=9 failures=0`, and a numbered
"Commands exercised" list at `:201-214` — but no command is shown next to its verbatim output in a
block. Its content is not empty of evidence; it is unverifiable-by-copy-paste, which is exactly the
class this check is for. Fix (append-only, no rewrite): append one indented block holding the 12
`bash -n` exit codes and the three C1 counter emissions it paraphrases.

The other 61 receipts in the scanned set carry at least one fenced or indented command block. The only
other receipt with zero fenced blocks is `wave1/RevNoHarm.md` (9,776 B) and it carries 80 indented
command/output lines, so it is not prose-only; the smallest evidence-bearing receipt is
`wave1/ScoutLiveDrift.md` (2,761 B, one fenced block).

## 6. Supplementary duplication inside the infra files (beyond the five named checks)

Measured, because it is the largest redundant byte mass in `{WD}` and feeds the growth measurement:

- `wave1-plan.out` and `wave1-dispatch.json` hold **the same 64 task strings, 64/64 byte-identical**
  (63,625 B of task text in each file); the difference is wrapper keys only — the plan carries
  `priorRegistries` and `dispatch.calls`, the dispatch carries `taskCall` and `resumeSends`. Their total
  sizes differ by **727 B** (97,958 vs 98,685).
- `wave1-spec.json`'s 64 prompts are verbatim prefixes of the dispatch tasks (**64/64**, 50,553 B), so the
  unique task text in `{WD}` is 63,625 B stored as **177,803 B → 114,178 B redundant**.
- `build-spec.py` (65,308 B) holds the *pre-substitution* templates (`{LANE}`, `{WD}`): 0/64 spec prompts
  appear verbatim in it, so it is not a fourth literal copy but the generator. It is the reproducibility
  anchor for the three files above; **not** a deletion candidate.
- `l1-ref/sid-url.tsv` (7,738 B, untracked): 48 rows, and **48/48 URLs appear verbatim in
  `corpus/SOURCES.md`** — fully derived (id, url, title), no unique content. The L1's working reference;
  drop or keep, nothing is lost either way.
- The two ready markers `wave1.ready` (160 B) / `wave1.ready.dispatched` (20 B) are live coordination
  state at scan time — **not** cleanup candidates.

Per-round evidence bytes, same command on each round directory (context for the growth measurement;
older rounds are quiescent, this round is in flight):

| round | files | bytes |
|---|---|---|
| 23 | 104 | 1,691,701 |
| 24 | 83 | 1,126,754 |
| 25 | 3,808 | **58,378,746** (`wave1/mut-skip` 17.9 MB, `wave1/rev-independent` 5.7 MB, `wave1/mut-audit` 5.4 MB) |
| 26 | 1,587 | 27,519,789 |
| 27 | 10 | 10,126 |
| 28 | 363 | 5,843,408 |
| 29 | 221 | 3,883,677 |
| 30 | 157 | 1,863,229 |
| 31 | 196 | 3,132,387 |
| 32 | 23 | 401,010 |
| 33 (in flight) | 144 | 1,604,842 |

Round 33's `wave1/` carries no multi-MB seat directory, in contrast to rounds 25 and 26 where single
seat directories hold 17.9 MB (`round-25/wave1/mut-skip`) and 5.4 MB (`round-25/wave1/mut-audit`): the
2026-10-25 scratch rule moved those trees out of the lane. The remaining in-lane redundancy is the
triple-stored prompt text above and the 7,500 B of repeated evidence files (§2) — the growth
measurement's baseline should therefore read ~1.6 MB for this round *plus* the receipts that land after
04:57Z.

## 7. Re-run (on quiescent bytes)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-33
$ until [ "$(ls wave1/*.md | wc -l)" -ge 64 ]; do sleep 20; done    # or: L1 freezes the wave
$ python3 wave1/SimplifierCleanup/scan.py --root . --json > /fast/scratch/hyaku/r33-rescan.json
$ python3 -c 'import json;d=json.load(open("/fast/scratch/hyaku/r33-rescan.json"));
print(d["files"],d["bytes"],[r["path"] for r in d["big"]],d["empty"],
      {k[:16]:v for k,v in d["dups"].items()},
      [r["path"] for r in d["receipts"] if r["prose_only"]])'
```

Expected deltas after the last seats land: `files`/`bytes` grow; `big` stays empty; `dups` and `empty`
can only change if a late seat re-saves identical evidence; `prose_only` is recomputed over the full set.

## 8. Scratch removal proof

Evidence was copied into `wave1/SimplifierCleanup/` first (§0), then the tree was removed with the
literal command and output below (`$S` = `/fast/scratch/hyaku/kasegi-r33/SimplifierCleanup`):

```
$ S=/fast/scratch/hyaku/kasegi-r33/SimplifierCleanup; ls -d "$S" >/dev/null 2>&1 && echo "present_before=yes"; rm -rf -- "$S"; echo '--- after ---'; ls -d "$S" 2>&1; ls -d /fast/scratch/hyaku/kasegi-r33/* 2>/dev/null
present_before=yes
--- after ---
ls: cannot access '/fast/scratch/hyaku/kasegi-r33/SimplifierCleanup': No such file or directory
/fast/scratch/hyaku/kasegi-r33/CritMistakes
/fast/scratch/hyaku/kasegi-r33/ExecWaveEvidencePack
```

This seat ends with no tree on disk. The two remaining directories belong to other seats
(`CritMistakes` was still running; `ExecWaveEvidencePack` had already written its receipt) — reported
here as an observation for `ExecScratchDiscipline`, not ruled on by this seat.
