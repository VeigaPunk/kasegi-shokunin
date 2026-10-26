# SentScopeFinal — final scope + credential + misroot sweep (round 33)

Seat: sentinel, leaf (no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`;
lane HEAD at sweep `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f`.
Gate met before measuring: `receipts_md=30` (poll `until [ "$(ls .ufo/waves/round-33/wave1/*.md | wc -l)" -ge 30 ]`, elapsed 640 s).
Sweep ran 01:29–01:34 local; 30 receipts at the gate, 39 at the classification pass, 43 by the time this
receipt was written — the wave was still in flight (see Bounds).
Model: not recorded — `wave1-dispatch.json` carries no model key for this seat and every check below is a
deterministic local read; no model-dependent judgment was made or needed.
Tools installed/upgraded: none (stdlib `python3`, `git` reads, `sha256sum`).

**Verdict lines**
- `F1 HIGH` frozen C1 predicate sentence is contradicted by the landed instrument's own disclosed counter.
- `F2 MEDIUM` 36 paths written since base are outside the FILE OWNERSHIP path set (1 L1 erratum + 35 seat evidence fragments in 3 new `wave1/<Seat>/` subdirectories).
- `F3 CLEAN` no credential, session or private-URL material in any new or changed file.
- `F4 CLEAN` no misroot: fleet root unchanged, `shokuknow` untouched, all seat scratch under its own `kasegi-r33/<Seat>/` dir, no yielded seat left a tree.
- `F5 CLEAN` frozen surface intact (claims.json, both controls, census, watchdog digest, assimilation guard, 9 read-only instruments), and every append-only owned file shows 0 deleted lines.

## 1. Fleet root (`/home/vgpnk/Projects/shokunin`), no pathspec

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | wc -l
25
$ git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -iE 'kasegi|round-33|Exec|Scribe|Scout|Rev|Crit|Mut'
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/revenger.report-baseline
```

The 25-path list is byte-identical at 01:16 (wave start) and 01:31 (sweep): 16 `.ufo/state/*.report-baseline`,
`.ufo/watchdog.log`, `scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md`, and untracked
`.scratch/goal-20261026-hyaku-run8.md`, `.tower/`, `.ufo/state/disk-guard.log`,
`.ufo/state/inline-dispatcher.log`, `.ufo/waves/round-30/`, `demo-cwd.txt`.

No seat-written path at the fleet root. The two "kasegi"/"revenger" hits are dispatcher state baselines
(`.ufo/state/`), not round-33 seat content; `.scratch/`, `.tower/`, `demo-cwd.txt` and `.ufo/waves/round-30/`
are dispatcher surfaces outside this round. Nothing deleted, nothing touched.

## 2. Lane classification against FILE OWNERSHIP

```
$ python3 $S/classify.py "$PWD" 690b69d   # changed-since-base ∪ untracked ∪ staged
total=116   OWNED=58   L1-OWNED=22   READONLY-EDIT=0   UNOWNED=36
```

- `READONLY-EDIT=0`: the nine read-only instruments are untouched —
  `for f in limb-mutation-check.py limb-ledger.json recheck-audit.py source-recheck.py frontier-recheck-count.py anchorcheck.py density.py resolve.py score-gap.py; sha256sum` vs `git show 690b69d:corpus/instruments/$f | sha256sum` → all nine `UNCHANGED`.
- `OWNED=58` = 39 `wave1/<Seat>.md` receipts (`SEAT-SELF`) + 19 declared content paths:
  `ExecManifestUpgrade` 8 (round-23/24/25/26/28/29/30/31 manifests), `ExecManifest32`
  (`corpus/source-snapshots/round-32/manifest.json`), `ExecCaptureBinding`
  (`corpus/instruments/capture-binding-check.py`), `ExecEntryF16`
  (`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`), `ExecRegistryAppend` (`corpus/SOURCES.md`),
  `ExecExpectedList`, `ScribeReadmeF16`, `ScribeProvince`, `ScribeSkillGate`, `ScribeQuality`, `ScribeInstrReadme`,
  `L1` (`LOG.md`). `ScribeScorecard`/`ScribeShonen`/`ScribeLesson` had not landed at sweep.
  Nothing was written at a path another seat owns.
- `L1-OWNED=22`: `claims.json`, `c1-controls/*` (3), `c2-controls/before.txt`, `census-before.txt`,
  `watchdog-digest.txt`, `assimilation/*` (5), `build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`,
  `wave1-plan.{out,err}`, `wave1-run.err`, `wave1.ready`, `wave1.ready.dispatched`, `l1-ref/sid-url.tsv`,
  `wave1/swarm-registry.json` — all match the "not yours this wave" surface; none edited by a seat (see §5 hashes).

### UNOWNED writes (36) — outside the declared single-writer path set

```
$ grep '^UNOWNED' $S/classify3.out | grep -v '/wave1/[A-Za-z]*/'
UNOWNED  -  .ufo/waves/round-33/claims-erratum-1.md
$ grep '^UNOWNED' … | grep -o '/wave1/[A-Za-z]*/' | sort | uniq -c
     16 /wave1/ExecCaptureBinding/
     11 /wave1/ScribeInstrReadme/
      8 /wave1/ScribeSkillGate/
```

(a) **35 evidence fragments in three new seat-named subdirectories under `wave1/`.** The ownership table grants
each seat exactly one path, `…/wave1/<YourName>.md`; `wave1/ExecCaptureBinding/`, `wave1/ScribeInstrReadme/` and
`wave1/ScribeSkillGate/` are not in the table, so every file inside them is a single-writer violation in shape.
Measured sizes: `ExecCaptureBinding 22430 B`, `ScribeInstrReadme 14937 B`, `ScribeSkillGate 85682 B`.
This is also the committed-byte growth the considerthese proposal 1 (wave-evidence bloat) tracks:
`du -sb .ufo/waves/round-33/wave1` = `629533` at 01:29 and `679705` at 01:33, of which 123 049 B is fragments.
Both `ExecCaptureBinding.md` and `ScribeInstrReadme.md` reference their subdirectory, so the fragments are
load-bearing receipt attachments rendered at a path no seat owns.
Smallest remediation: the L1 either declares `wave1/<Seat>/` in the ownership table for the next wave, or the
evidence-index seat folds fragments into `wave1/<Seat>.md`; no seat should re-write them now.

(b) **`.ufo/waves/round-33/claims-erratum-1.md`** — self-identified as L1-authored (`Filed 2026-10-26 by the L1
(KasegiR33) after ScoutManifestAudit surfaced a Rule B hazard at base`), mtime `01:18:23`, first recorded
ExecCaptureBinding run `01:20:15` — so it preceded that seat's measurement, consistent with its own "no seat had
scored when it was filed". The claims-freeze rule sanctions corrections as separate appended files, but the path
is absent from the FILE OWNERSHIP table; it is L1 surface by authorship, contract gap by declaration.
See F1 for what it changes.

## 3. Credential / session / private-URL sweep

```
$ python3 $S/credsweep.py "$PWD" 690b69d     # grep -niE 'op://|token|secret|api[_-]?key|bearer|password|账号|密码'
scanned_files=111  pattern_hits=131           # 111 files at 01:31; the changed set grew to 118 paths by 01:33
$ grep -o 'pattern=[a-z-]*' credsweep.out | sort | uniq -c
    102 pattern=token     13 pattern=password     10 pattern=secret
      4 pattern=op-scheme  1 pattern=bearer        1 pattern=cn-account
```

Every hit is a keyword in prose, not a value; each of the 13 `password`, 10 `secret`, 4 `op-scheme` and 1
`cn-account` hits was read through `maskctx.py` (which prints `[MASK:n]` in place of the match, never the match),
and the 102 `token` hits are the word "token" in `the https:// token in the row's source cell` and in the seat
contract's own pattern list. Categorised:

| hit class | example (masked window) | count | verdict |
|---|---|---|---|
| the rule's own wording | ``the `https://` [MASK:5] in that row's source cell`` | 102 `token` | benign |
| Q6 disclosure that the material exists | `the S049 page carries platform-issued tester VPN account/[MASK:8] acquisition instructions for testers` | 9 `password` (+1 at `knowledge:193` stating it is **not reproduced**) | benign, compliant |
| lost evidence-path name | `LOST-RECORDED md:128 [lost-tree] evidence/hackerone-1[MASK:63] (not checked)` — anchorcheck reporting a referenced path that no longer resolves; no such file exists in the tree | 3 `password` | benign |
| bare scheme only | `op://` with `match_chars=5` — no vault path, so not a vault-reference URI; all 4 are in the L1 spec/dispatch text that quotes QUALITY Q6 | 4 `op-scheme` | benign |
| lane-domain prose | `kagi — [MASK:7] and vault handling` (`PROVINCE.md:48`) | 1 `secret` (10 total in prose) | benign |
| grep pattern text | `$ grep -nE "[MASK:34]" corpus/source-snapshots/round-32/manifest.json` | 1 `cn-account` | benign (checker pattern) |
| bearer in prose | `Bearer …` in instructions text, not a header value | 1 `bearer` | benign |

Added-lines-only pass (excludes pre-existing prose in modified files):

```
$ git diff -U0 690b69d -- $(git diff --name-only 690b69d) | grep '^+' | grep -niE 'op://|token|secret|api[_-]?key|bearer|password|账号|密码'
→ 20 hits, all in the L1 spec/dispatch text (the seat contract quotes the grep pattern) and in
  corpus/instruments/README.md describing `url` = the `https://` token. Zero 账号 / 密码 / op://-with-path.
```

**Q6 quote check on the one new document** (`q6span.py`, whitespace- and wrap-insensitive):

```
S049 quotes_total=26 found_wrap_insensitive=10 on_credential_lines=0 capture_credential_lines=10
S050 quotes_total=26 found_wrap_insensitive=0  on_credential_lines=0 capture_credential_lines=7
$ blockquote resolution: S049 raw=7 / S050 raw=8 of 15  → all 15 resolve to their own capture
```

No quoted span in `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` lands on any of the
10 credential-bearing S049 lines or the 7 S050 lines. The entry's only two `password` lines disclose that the
material exists and say it is not reproduced: `That material is **not reproduced** here — no account, [MASK:9]`.
S050's `found=0` under the span search is a method bound (blockquote lines carry bracketed annotations and
elision marks; the 15 blockquote lines all resolve to S050 under punctuation-stripped prefix match), not a
finding.

Off-registry URLs in seat content (registry = 50 row URLs parsed from `corpus/SOURCES.md`):

```
URL=http://www.cnvd.org.cn/                       in_registry=False appears_in_captures=['S049']
URL=https://security.360.cn/Product/product       in_registry=False appears_in_captures=['S050']
```

Both are verbatim inside the captured document they are cited from — quoted, not invented; public
documentation hosts, no session or private URL. Whether a capture-internal link needs its own registry row is
the C2 verifier's call, not adjudicated here.

## 4. Misroot

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain   # §1: 25 paths, unchanged 01:16 → 01:31
$ find /home/vgpnk/Projects/shokuknow -type f -newermt '2026-10-26 00:30' | grep -v '/\.git/' | wc -l
0          # same command at wave start: 0  → the read-only package was not written
$ ls /fast/scratch/hyaku/kasegi-r33/            # depth-1 files:
(none)     # every entry is a directory named for a seat; no stray file at the scratch root
$ find /fast/scratch -maxdepth 1 -type d -newermt '2026-10-26 04:00'
(none)     # no new top-level scratch root
$ ls -l /tmp/kasegi-*.txt ; du -ch … | tail -1
24K total  # 6 message files, 329–393 B each → inside the "<50 MB in /tmp" allowance; no committed tool hardcodes /tmp
```

Scratch-dir accounting: 21 seat dirs sat under `/fast/scratch/hyaku/kasegi-r33/` at sweep
(`ConnOwnership CritMistakes ExecCensusAfter ExecDeterminism ExecGrowthMeasurement ExecNoHarmFinal
ExecRegistryAppend ExecRegressionC1 ExecScratchDiscipline ExecWaveEvidencePack MutEntryF16 RevC1BeforeAfter
RevC1Instrument RevEntryF16 RevGateSpot RevRowS050 ScribeLesson ScribeSkillGate SentCred SentScopeFinal
SimplifierCleanup`). Every one maps to a seat with **no landed receipt** — i.e. still in flight — and this seat's
own `SentScopeFinal` dir is among them (removed at yield, see Cleanup). Every seat
whose receipt had landed (`Scout*`, `ExecBeforeReceipts`, `ExecCaptureBinding`, `ExecManifestUpgrade`,
`ExecManifest32`, `ExecQuarantine`, `ExecCensusDry`, `RevNoHarm`, `RevClaimsFreeze`, `RevManifestUpgrade`,
`ScribeInstrReadme`, …) had already removed its tree. No yielded seat left a tree behind.

One observation, dispatcher surface not a seat: `/fast/scratch/kasegi-r33-l1/` (4350 B `report-draft.md`) sits
outside the prescribed `$HYAKU_SCRATCH/kasegi-r33/` root.

## 5. F1 — HIGH: frozen C1 predicate is contradicted by the landed instrument

Three texts disagree; the lane holds all three, so the graded sentence is currently unsatisfiable as written.

1. **Frozen claim** (`claims.json`, sha256 `978d86b2639f30794ce37798496e8d13e9fc32327283e621f21e2c7d348fd237`,
   byte-identical to freeze commit `6e55c8d`): `every manifest record has a url that matches exactly one
   corpus/SOURCES.md registry-row URL`.
2. **Erratum 1** (side file, `01:18:23`) redefines rule B to id-scoped binding, makes a duplicate-carried URL
   informational (`multi_row_url`), and asserts `Predicate sentence, kill rule, counters and the 40/40/0 target
   are unchanged`.
3. **Landed instrument** `corpus/instruments/capture-binding-check.py` implements the erratum — its header says
   `B. URL BINDING (claims-erratum-1, the L1's id-scoped ruling)` and `A URL that also appears in a DIFFERENT
   row … is NOT a failure`.
4. **Live output** in `wave1/ExecCaptureBinding.md:156-157`:
   `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9
   missing_manifest=0 multi_row_url=2` / `records=40 bound=40 unbound=0` (exit 0).

`multi_row_url=2` is the contradiction. Independent measurement from the registry, not from the erratum:

```
$ rows_with_url=50 ; duplicate groups:
DUPLICATE_URL ids=['S006', 'S028'] count=2
DUPLICATE_URL ids=['S024', 'S029'] count=2
```

Records `S029` (round-23) and `S006` (round-24) each carry a `url` that matches **two** registry-row URLs.
Under the frozen sentence they are not bound; the instrument counts them bound and exits 0. So
`records=40 bound=40 unbound=0` can be printed by a checker whose own AUDIT line reports the frozen clause false
for 2 of 40 records. A verifier scoring the predicate sentence literally must reject; one scoring the
instrument's exit code must admit. The dispatch contract I was handed encodes the frozen reading explicitly
(`0 or 2+ matches = failure, name the record id`), so any seat coding to the dispatched contract would instead
fail `S029`/`S006` — the two readings cannot both be right.

Why it matters beyond bookkeeping: the counter is the claim's evidenced surface, and the relaxed reading is
strictly weaker (a record may bind a URL that two registry rows claim). Nothing in the erratum's own text
amends the sentence it says is unchanged.

Smallest remediation, in order of preference: (1) the L1 appends erratum 2 that **amends the predicate sentence**
to the id-scoped reading and discloses `multi_row_url=2` (S029/S006) inside the claim, so the graded sentence
matches the instrument; or (2) the instrument keeps the frozen "exactly one row" reading and the C1 target drops
to `bound=38 unbound=2`, which makes the frozen `40/40/0` target false and must be reported as such. Do not edit
`claims.json` — the correction has to be an appended file before either claim is scored. Owners to read this:
`CritC1Kill`, `RevC1Instrument`, `RevClaimsFreeze`, and the L1.

Consistent with the erratum filing order for the one seat I can time: erratum `01:18:23` precedes the first
recorded ExecCaptureBinding run `01:20:15`. That bounds the claim "no seat had scored when it was filed" to this
seat only; other seats' first-run times were not checked.

## 6. F5 evidence — frozen surface and append-only integrity

```
$ git show 6e55c8d:.ufo/waves/round-33/claims.json | sha256sum ; sha256sum .ufo/waves/round-33/claims.json
978d86b2…348fd237  -        (both identical → claims not edited)
$ for f in c1-controls/{before.txt,fake-checker.py,fake-checker-receipt.txt} c2-controls/before.txt \
           census-before.txt watchdog-digest.txt assimilation/guard-proof.txt; hash vs 6e55c8d → 7/7 UNCHANGED
$ git diff --numstat 690b69d -- <append-only owned paths>
2 0 PROVINCE.md | 43 0 SKILL.md | 55 0 corpus/QUALITY.md | 26 0 corpus/README.md | 6 0 corpus/SOURCES.md
139 0 corpus/instruments/README.md | 1 0 corpus/instruments/knowledge-expected.txt
12 0 round-23 | 57 0 round-24 | 15 0 round-25 | 3 0 round-26 | 6 0 round-28 | 9 0 round-29 | 9 0 round-30 | 3 0 round-31
```

Zero deletions anywhere → append-only respected, no rewritten rule text, no rewritten registry row, no dropped
record. Manifest additions total `114 = 3 × 38` records, exactly the `url` + `archival` + line-break shape the
contract asks for. Registry row counts: `| S049 |` = 1, `| S050 |` = 1, total rows with URL = 50.

## Cleanup

Scratch `$S=/fast/scratch/hyaku/kasegi-r33/SentScopeFinal` held the four read-only probes below plus their
outputs. The outputs that matter are quoted inline in §1–§5; the probe sources were scratch-only helpers and are
not committed, so the method appendix below states each one completely enough to reconstruct in a few lines.
``` 
$ rm -rf -- "$S"; [ -e "$S" ] || echo scratch_exists=NO
scratch_exists=NO
```
Every probe took the lane root and base rev (and, for the sweeps, its own scratch dir) as arguments; none writes
outside the named scratch dir, none hardcodes `/tmp`, none is committed.

## Method appendix (reconstruct the probes)

- `classify.py <lane> <base>` — path set = `git diff --name-only <base>` ∪ `git ls-files --others
  --exclude-standard` ∪ `git diff --name-only --cached`; map to `OWNED` / `L1-OWNED` / `READONLY-EDIT` /
  `UNOWNED` by first matching regex over the FILE OWNERSHIP table (read-only instruments checked first, so an
  edit to one is `READONLY-EDIT` even though the file is listed elsewhere).
- `credsweep.py <lane> <base>` — same path set; skip files whose first 8 KiB contain NUL; scan every line with
  `op://|token|secret|api[_-]?key|bearer|password|账号|密码` case-insensitive; print `path:line pattern=<class>
  match_chars=<n> line_chars=<n>` and **never the matched text**.
- `maskctx.py <file> <line> [half]` — print `±half` chars around each match with the match replaced by
  `[MASK:<len>]` and any ≥6-digit run by `[MASK:digits]`, so a credential cannot be reproduced.
- `q6span.py <entry> <capture> <id>` — extract `"…"` / `“…”` spans ≥6 chars from the entry; search each in the
  capture both line-wise and whitespace-stripped (offset→line map built from the stripped lines); report spans
  whose hit lines intersect the capture's credential-keyword lines.
- append-only check: `git diff --numstat <base> -- <path>` and require the deleted count to be 0; frozen-surface
  check: `git show <freeze>:<path> | sha256sum` vs `sha256sum <path>`.

## Bounds on what this proves

- Two in-flight reads (`01:18`, `01:22`) were re-run on quiescent bytes after their subjects landed; this report
  cites only the final pass. The wave was still running at 01:34: 43 of 64 receipts existed, so `ScribeScorecard`,
  `ScribeShonen`, `ScribeLesson` and later seats' writes are **not covered** — a path classification taken at
  this instant is not a forecast. Re-run the classifier and the credential sweep on the final tree.
- The credential sweep is a **pattern** sweep (`token|secret|password|api-key|bearer|op://|账号|密码`). Material
  with no such keyword — a bare hostname in a `curl` line, a base64 blob, a numeric account id — would not match.
  The Q6 quote check closes that gap for the one new document by locating each quote in its capture; it does not
  cover paraphrases, and it cannot see text quoted with a quote style outside `"…"` / `“…”`.
- `credsweep.py` scans whole changed files, so hits inside a modified file may be pre-existing prose. The
  added-lines-only pass is reported separately for that reason.
- Authorship is inferred from paths, not from process evidence: the two `wave1/<Seat>/` directories are attributed
  by name and by their receipts referencing them; I did not read `/proc` or shell history.
- Fleet-root comparison assumes no seat wrote and then restored a file between the 01:16 and 01:31 reads.

