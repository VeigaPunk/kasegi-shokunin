# NoHarmDiff — identical-export baseline/current verdict diff (C1)

Seat: `L1Kasegi23.NoHarmDiff-2` (falsify wave, round 23).
Scope: C1 only (`depth:verifiability`). Read-only against the lane; all execution in
`/tmp/kasegi-r23-falsify-noharmdiff`. No subagents. No repo writes except this report.

## 1. Question and short answer

Target: export `922a4dde90b60b465e2b8b241d1fe363f1f27e98`, run the baseline resolver bytes
(`.ufo/waves/round-23/c1-baseline-resolver.py`) and the current `corpus/instruments/resolve.py`
over that identical export, and diff `citation -> class`.

**Result: `changed=0, added=0, dropped=0` is CONFIRMED for the identical export — for both the
receipted HEAD bytes and the live worktree bytes.** The two runs are byte-identical (TSV
`sha256:80ef1504…`, MD `sha256:b47d78b2…`), 1589 distinct citations each.

**But the confirmation is evidentially empty for the C1 guard on this host.** With
`~/Projects/the-bounty-hunter` and `~/Projects/origin-work/the-bounty-hunter` absent and
`KASEGI_MIRROR` unset, `under_mirror()` is invoked **0 times** for the whole census
(instrumented, both resolver revisions). `changed=0` is therefore guaranteed by construction, not
measured: the export contains no citation whose verdict the confinement fix can alter *on this
host*. The fix's guard is live only under an injected mirror (§5).

## 2. Pinned inputs

| Artifact | SHA-256 | Note |
|---|---|---|
| `922a4dd:corpus/instruments/resolve.py` (baseline, also `c1-baseline-resolver.py`) | `d6a3c3f1…d869f903` | matches `c1-baseline.json` |
| `HEAD:corpus/instruments/resolve.py` (= worktree at seat start, 03:27:44) | `ed9a9dae…02840e9` | matches `c1-fixed.json` as it stood at seat start |
| live worktree `corpus/instruments/resolve.py` (mtime 03:42:37) | `8dd45bc8…f3868848` | changed **during** this review; see F2 |
| `c1-baseline.json` at capture | `c8433656…6e3cfa5f` | |
| `c1-fixed.json` at capture (03:43:07) | `bf0ece35…4deebfc` | pins resolver `8dd45bc…`, matrix `5c64e014…`, 17 cases |
| `mirror-containment-fixtures.json` at seat start | `5e61a33e…5b5e76a9` | 13 cases |
| `mirror-containment-fixtures.json` live (03:43:01) | `4e39f65c…71c2400b` | 20 cases |
| `mirror-containment-check.py` live | `53742c8d…534bff5d1` | modified during the wave |

Host state: `~/Projects/the-bounty-hunter`, `~/Projects/origin-work/the-bounty-hunter`,
`~/Projects/bounties`, `~/Projects/bounties-legacy` all absent; `KASEGI_MIRROR` unset →
`MIRROR_ABSENT=True`, `mirror=0` in every census run.

## 3. Identical-export experiment (primary)

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 922a4dd… | tar -x -C $S/export
# 105 files, 74 *.md
cp .ufo/waves/round-23/c1-baseline-resolver.py   $S/baseline/tool/resolve.py   # d6a3c3f1…
cp corpus/instruments/resolve.py (HEAD ed9a9dae) $S/current/tool/resolve.py    # ed9a9dae…
python3 baseline/tool/resolve.py $S/export
python3 current/tool/resolve.py  $S/export
```

Both runs, identical stdout:

```
distinct=1589 resolves=11 mirror=0 internal=197 other=0 gone=1381 skill=39/513 corpus=192/1262 all=208/1589
```

```
80ef1504c3f232b359cf90d0a19b125cd4c939aa9f4001b7821f7039e6ccda21  baseline/tool/citation-survival.tsv
80ef1504c3f232b359cf90d0a19b125cd4c939aa9f4001b7821f7039e6ccda21  current/tool/citation-survival.tsv
b47d78b22147456a7f58aa677bef7ed78b53464b5ac705bf7d4c3474dfe9ba2b  baseline/tool/citation-survival.md
b47d78b22147456a7f58aa677bef7ed78b53464b5ac705bf7d4c3474dfe9ba2b  current/tool/citation-survival.md
```

`citation -> (class, domain)` comparator, baseline vs current on the export:

```
distinct A=1589 B=1589 changed=0 added=0 dropped=0
```

Every changed verdict: **none.**

The live worktree bytes `8dd45bc8…` were also run over the same export: same stdout, TSV
`sha256:80ef1504…` again, `changed=0 added=0 dropped=0`. So the no-harm observation is stable
across the mid-review mutation, on this host.

Re-running the same resolver twice over the same frozen export reproduced `80ef1504…`
(deterministic for frozen input).

Class/domain census of the export: `GONE|bounty 45`, `GONE|other 108`, `GONE|rel 1228`,
`INTERNAL|rel 197`, `RESOLVES|other 11`, `MIRROR-EQUIVALENT 0`.

## 4. Why the export run cannot observe the fix

### 4a. Guard never executes (mirror absent)

Instrumented copy (wrapper around `resolve.under_mirror`, counter) over the export:

```
rc=0 under_mirror_calls=0        # baseline d6a3c3f1…
rc=0 under_mirror_calls=0        # current  ed9a9dae…
rc=0 under_mirror_calls=0        # live    8dd45bc8…
```

With `MIRROR_ABSENT`, every `exists_any(os.path.join(mirror_root, suffix))` returns `None` before
the `if m and under_mirror(...)` predicate is reached. All 45 bounty-domain and all rel/other
mirror-fallback candidates short-circuit to `None`. **`mirror=0` makes the added guard vacuous on
this host for the corpus census.**

### 4b. Boundary fix has no export input

The only citation in the current corpus that exercises `bounty_suffix()`'s exact-root boundary is
`~/Projects/bounties-x` (prefix sibling, should be domain `other`). It is **absent from the
922a4dd export** (`grep -c 'bounties-x' export-tsv` → `0`; no export file contains it) and was
added by `953c278`, which is 7 commits after the export. In the export, no citation starts with
the bounty prefixes other than root+`/` (the non-slash `bounties` hits are shell/noise tokens
such as `find ~/Projects/bounties …`). So the export cannot exercise either half of the fix.

### 4c. Current-tree supplement (moving target, timestamped)

Two back-to-back runs over the live repo, 03:41:45 / 03:41:50 (`distinct=1623`):

- `citation -> class` diff: **0 rows**.
- Full TSV diff: 4 lines = 2 rows: (i) `~/Projects/bounties-x` `GONE|bounty -> GONE|other`
  (the boundary fix — class unchanged), (ii) `/tmp/kasegi-r23-*` `resolved_path` drift
  (`glob` picks a different sibling scratch dir between runs — not fix-caused).
- Generated MD `OTHER` bucket: `12 resolve / 121 gone` -> `12 resolve / 122 gone`.
- Live worktree bytes `8dd45bc8…` over the repo: same one changed row (domain only), class diff 0.

At 03:38 the same comparison over the then-tree (`distinct=1620`) gave the same shape
(`changed=1` domain-only, class diff 0, `OTHER` 120 -> 121). A 03:41 rerun 2 min later saw
`distinct=1623` because sibling seats edited `corpus/knowledge/{cna-…,cra-…,multiparty-…}.md`
and `corpus/source-snapshots/round-23/manifest.json` during the window; the newest snapshot was
stable over 12 s but the corpus is not frozen. This supplement is therefore a snapshot, not a
certificate for the final tree.

## 5. Non-vacuity under an injected mirror (what `changed=0` hides)

Scratch mirror `/tmp/kasegi-r23-falsify-noharmdiff/synth/mirror` containing two symlink escapes
(`ops/fleet-dispatch.mjs`, `bounty-map/schema.json` -> `../outside/secret.mjs`) and one confined
file (`ops/shared.mjs`); `KASEGI_MIRROR` points at it; same frozen export.

| resolver set | mirror class count | changed vs baseline | added | dropped |
|---|---|---|---|---|
| baseline `d6a3c3f1…` | 16 | — | — | — |
| receipted current `ed9a9dae…` | 8 | **8** | 0 | 0 |
| live worktree `8dd45bc8…` | 11 | **11** | 0 | 0 |

Every changed verdict, baseline -> `ed9a9dae…` (receipted bytes):

```
../../../.ufo/l0-questions.md                        MIRROR-EQUIVALENT/rel    -> GONE/rel
bounty-map/schema.json                               MIRROR-EQUIVALENT/rel    -> GONE/rel
ops/*.mjs                                            MIRROR-EQUIVALENT/rel    -> GONE/rel
ops/fleet-dispatch.mjs                               MIRROR-EQUIVALENT/rel    -> GONE/rel
~/Projects/bounties/bounty-map/schema.json           MIRROR-EQUIVALENT/bounty -> GONE/bounty
~/Projects/bounties/bounty-map/{schema.json,programs/*.json}  MIRROR-EQUIVALENT/bounty -> GONE/bounty
~/Projects/bounties/ops/fleet-dispatch.mjs           MIRROR-EQUIVALENT/bounty -> GONE/bounty
~/Projects/bounties/ops/{claim-check,ev-report,fleet-dispatch,shared}.mjs  MIRROR-EQUIVALENT/bounty -> GONE/bounty
```

`ed9a9dae…` -> live `8dd45bc8…` adds three more (see F3): `~/Projects/bounties`,
`/home/vgpnk/Projects/bounties`, `~/Projects/bounties/` all `GONE/bounty ->
MIRROR-EQUIVALENT/bounty` (resolved to the mirror root directory; 12/7/4 citing files,
16/9/5 occurrences). Confined controls `ops/shared.mjs` and `~/Projects/bounties/ops/shared.mjs`
stay `MIRROR-EQUIVALENT` under both revisions.

Matrix replay (checker's own isolated `HOME`+`KASEGI_MIRROR` per case, checker lines 82-91):

- fixtures `5e61a33…` (13 cases), 03:39: `ed9a9dae…` 13/13 PASS; baseline `d6a3c3f1…`
  7/13 PASS, 6 FAIL (`bounty-parent-traversal`, `bounty-parent-traversal-vault`,
  `relative-mirror-fallback-escape`, `bounty-fallback-symlink-escape`,
  `relative-fallback-symlink-escape`, `bounty-prefix-sibling-confusion`).
- fixtures `4e39f65c…` (20 cases), 03:43: live `8dd45bc8…` 20/20 PASS; baseline 12/20 PASS,
  8 FAIL.

## 6. Findings (severity order)

**F1 — Medium (verifiability). The mandated export experiment is structurally blind to C1.**
`mirror=0` and `under_mirror_calls=0` on this host (§4a), and the sole boundary-sensitive cite is
absent from `922a4dd` (§4b). `changed=0/added=0/dropped=0` on that export is a no-op guarantee,
not evidence that the confinement wiring behaves correctly on real data. The only evidence that
exercises the guard is the synthetic matrix (§5). A no-harm claim scoped to this export cannot be
read as a no-harm claim about the fix's behavior.

**F2 — Medium (artifact identity / verifiability). The C1 artifacts mutated during the falsify
window, and the live receipt no longer matches the live tree.**
Observed drift, all after this seat's initial read:
`resolve.py` `ed9a9dae…` (03:27) -> `9e0b5751…` (03:42:37) -> `8dd45bc8…` (03:42:37 mtime);
`mirror-containment-fixtures.json` `5e61a33…`(13 cases) -> `5c64e014…`(17) -> `4e39f65c…`(20);
`mirror-containment-check.py` modified; `c1-fixed.json` rewritten at 03:43:07 to pin matrix
`5c64e014…` while the live fixtures are `4e39f65c…`. Any `changed=0`/matrix-pass statement is
only meaningful against a named SHA; the receipt-to-byte binding was broken at capture time
(`c1-fixed.json` matrix SHA ≠ live fixtures SHA). This is the reproducibility defect: a verifier
arriving later cannot reconstruct which bytes produced the receipt.

**F3 — Low/Medium (coverage gap in live bytes). Empty-suffix bounty cites now credit the mirror
root, with no fixture pinning it.** Live `bounty_suffix`/`classify` changes
`suffix == ""` handling from `(None, None)` to `exists_any(mirror_root)`, so root-only and
trailing-slash citations (`~/Projects/bounties`, `/home/vgpnk/Projects/bounties`,
`~/Projects/bounties/`) become `MIRROR-EQUIVALENT` whenever a mirror exists. Three real corpus
citations change class in the injected-mirror run (§5), two of them heavily cited (12 and 7
files). The current 20-case matrix contains **no root-only bounty cite** (`root-only: []`), so
this behavior change is unpinned; on this host it is invisible (mirror absent). Whether a
directory-exists check on the mirror root is adequate evidence for a whole-tree citation is
undecided by anything in the matrix or receipts.

**F4 — Low (correctness edge, unchanged coverage). Escape-first multi-match over-rejection.**
`exists_any()` returns the first existing brace/glob match; the guard then rejects that single
path and never tries later candidates. Under the injected mirror `ops/*.mjs` and
`~/Projects/bounties/ops/{claim-check,ev-report,fleet-dispatch,shared}.mjs` classify `GONE` even
though the confined sibling `ops/shared.mjs` exists and is `MIRROR-EQUIVALENT` for its own token.
All 20 fixture cites are single-target; no matrix case covers a multi-match token. Defensible
under the documented "first match wins" rule, but the docstring does not say a rejected first
match suppresses confined alternatives.

**F5 — Info (scope of the claim).** `citation -> class` no-harm holds; the instrument's full
observable output does not. `~/Projects/bounties-x` keeps class `GONE` but changes domain
`bounty -> other`, and the generated MD `OTHER` bucket moves 121 -> 122 (03:41 snapshot). Also,
full-TSV equality across runs is environment-dependent: the exported citation `/tmp/kasegi-r23-*`
globs live scratch dirs and resolved to different siblings between two runs over unchanged
source bytes (two different `resolved_path` values, hence different TSV hashes at 03:38). This
is an environment race with concurrent seats, not caused by the C1 diff, but it weakens the
module docstring's "byte-identical across consecutive runs over unchanged source bytes" claim
whenever `/tmp/kasegi-r23-*` matches exist.

## 7. Vacuity verdict

**Yes — on this host, `mirror=0` makes the added confinement guard vacuous for the corpus
census.** Both `MIRROR_CANDIDATES` roots and `~/Projects/bounties` are absent, `KASEGI_MIRROR` is
unset, and instrumentation shows `under_mirror()` is called zero times for every revision tested
(baseline, receipted current, live worktree) over both the frozen export and the current tree.
The guard is not vacuous in general: with an injected mirror it changes 8 real-export citations
(receipted bytes) / 11 (live bytes). The honest statement is therefore "no class change on this
host because the branch is unreachable here", not "the fix changed nothing".

## 8. Scope limits

- C1 only. C2 (F06-F08), corpus prose, Q-bars, and any score movement were not examined.
- No admission, integration, or credit claimed; this is a recommendation only.
- The current-tree numbers are a timestamped snapshot of a corpus being edited by other seats;
  only the frozen `922a4dd` export is reproducible byte-for-byte.
- No source availability / attribution judgement; the matrix measures classification only.
- Host-level absence of bounty/mirror trees was observed, not explained.

## 9. Reproduction (scratch `/tmp/kasegi-r23-falsify-noharmdiff`)

```sh
S=/tmp/kasegi-r23-falsify-noharmdiff
mkdir -p "$S/export" "$S/baseline/tool" "$S/current/tool"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 922a4dde90b60b465e2b8b241d1fe363f1f27e98 \
  | tar -x -C "$S/export"
cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/c1-baseline-resolver.py \
   "$S/baseline/tool/resolve.py"                       # d6a3c3f1…
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 922a4dde…:corpus/instruments/resolve.py \
   | sha256sum                                          # same d6a3c3f1…
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show HEAD:corpus/instruments/resolve.py \
   > "$S/current/tool/resolve.py"                       # ed9a9dae… (seat-start bytes)
python3 "$S/baseline/tool/resolve.py" "$S/export"
python3 "$S/current/tool/resolve.py"  "$S/export"
python3 "$S/compare.py" "$S/baseline/tool/citation-survival.tsv" \
                        "$S/current/tool/citation-survival.tsv"
# under_mirror call counter:
python3 "$S/probe/patchprobe.py" "$S/current/tool/resolve.py" "$S/export"
# synthetic mirror:
mkdir -p "$S/synth/mirror/ops" "$S/synth/mirror/bounty-map" "$S/synth/outside"
ln -s "$S/synth/outside/secret.mjs" "$S/synth/mirror/ops/fleet-dispatch.mjs"
ln -s "$S/synth/outside/secret.mjs" "$S/synth/mirror/bounty-map/schema.json"
echo CONFINED > "$S/synth/mirror/ops/shared.mjs"
KASEGI_MIRROR="$S/synth/mirror" python3 "$S/baseline-synth/tool/resolve.py" "$S/export"
KASEGI_MIRROR="$S/synth/mirror" python3 "$S/current-synth/tool/resolve.py"  "$S/export"
python3 "$S/compare.py" "$S/baseline-synth/tool/citation-survival.tsv" \
                        "$S/current-synth/tool/citation-survival.tsv"
# matrix replay:
python3 corpus/instruments/mirror-containment-check.py \
  --resolver "$S/baseline/tool/resolve.py" --json "$S/matrix-base.json"
python3 corpus/instruments/mirror-containment-check.py \
  --resolver "$S/current/tool/resolve.py"  --json "$S/matrix-fixed.json"
```

Comparator (`compare.py`) compares `(class, domain)` per citation and prints
`distinct/changed/added/dropped` plus one `CHANGED|ADDED|DROPPED` line per citation.
