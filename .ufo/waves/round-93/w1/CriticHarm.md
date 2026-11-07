# CriticHarm — round 93 attempt 1 (attack seat): no-harm audit of both landings

Base `e15996bfd2f6eca4af39507a7c5973afbeca8347` · freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68` ·
C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b` · C2 landing `9225954a6e3f177af46bdb9d811c062a4353a552`
(tip = C2 landing = `HEAD`). Lane repo cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; every command
absolute-path and read-only against the lane's git/jj state. Findings and files only; the L1 commits.
Receipts: `.ufo/waves/round-93/w1/CriticHarm-receipts/`.

**Axes this seat can touch:** `depth:verifiability` (C1, via citation-class movement and anchor support)
and `coverage` (C2, via false positives, ReDoS cost, old capabilities, and the dependent intake gate).
Item 1 additionally measures the adjacent `depth:density` surface. Verdicts below are no-harm
re-derivations, not re-scores: each claim stands or falls on its own frozen predicate.

## Verdict

**NO HARM — items 1–6 all NO HARM.** No routed defect re-scores either frozen claim. Four
qualifiers (Q1–Q4) are recorded for the next label round/census; none is a regression introduced by
these landings, and none changes a claim predicate.

| # | Item | Axis | Verdict | Key observation |
|---|---|---|---|---|
| 1 | depth:density, SKILL.md base vs tip | depth:density (adjacent) | **NO HARM** | SKILL.md blob and sha256 identical at base and tip (`27f23a93…` blob, `7d082bfe…` sha); `density.py --label r93` output byte-identical on both (mean 273.2, 932 path cites, 38 blocks) |
| 2 | false positives of the landed scanner | coverage | **NO HARM** | `--rev 9225954`: `scanned=1957 hits=0 allowed=24 unused_allow=0 rc=0`; `--files` over all 286 knowledge+snapshot files: `hits=0`; differential over all 6,275 tracked `.md` (base vs landed scanner): identical 23-hit/18-file set, zero new shape hits |
| 3 | ReDoS on 1 MiB near-miss lines | coverage | **NO HARM** | Isolated regex flat at 16.9–46.7 µs/KiB across 1/2/4/8 MiB (ratio 8×: 0.81–1.18); end-to-end 0.37–0.63 s per 1 MiB line incl. interpreter start; fixed-width lookbehinds, linear |
| 4 | old capabilities: round-92 counter | coverage | **NO HARM** | Frozen round-92 counter (`3feed3b0…`) at tip: **K1–K8 all pass, rc=0**; `--selftest` `pass cases=90`; all 13 prior shapes still present |
| 5 | C1 citation-class movement | depth:verifiability | **NO HARM** | corpus/knowledge distinct: base `994 GONE / 1007 resolving / 2001 total` → landing `991 / 1009 / 2000` (exactly the meter's M0/M1); only 5 lines changed; **no citation site lost a resolving citation**; net resolving +2 |
| 6 | intake gate still refuses planted tokens | coverage | **NO HARM** | Planted `ghp_`+36 → rc 3 `shape=github-token line=1 written=no`; planted `glpat-`+20 → rc 3 `shape=gitlab-pat line=1 written=no`; clean text → rc 0 and written |

## Ground truth reproduced (independent of the landing receipts)

- C1 landing `ae53b3c` changes **exactly one** tracked path, `corpus/knowledge/triage-thresholds.md`
  (numstat 5/5; line count 487 → 487). C2 landing `9225954` changes **exactly two**:
  `SCORECARD.md` (1/1) and `corpus/instruments/capture-secret-scan.py` (46/5). The SCORECARD diff is
  one replaced row whose first cell is `capture-secret-scan`; the row keeps every prior shape name
  (`github-token`, `cloudfront-signed-cookie-signature`, `skdutid`, `cloudfront-signed-url-signature`,
  `gcs-signed-url-signature`, `azure-sas-signature`, `corpus/practice/*/evidence/`) and the
  first-working-round cell `87`, and adds `gitlab-pat`.
- The landed scanner sha256 is exactly the frozen candidate:
  `7d9d7309d5a5eddde59dbbb49767d71f43ec78667f1c3aa05bb1c76a45f683c5`. `capture-source.py` is
  unchanged (`0630d32b…`) and imports the scanner's `patterns()` (the only other consumer; no
  duplicated pattern authority). The round-93 frozen counter/map/labels/candidate are untouched by
  both landings (`git diff --stat 5bad9e5 9225954 -- .ufo/waves/round-93/c1 .ufo/waves/round-93/c2` ⇒ empty).
- The five C1 sites are exactly the label/map rows: 58 and 144 (`SKILL.md:117` → `SKILL.md:191`),
  437 and 438 (whole last cell replaced), 454 (`SKILL.md:494-506` → `SKILL.md:827-848`). Byte-level:
  lines 58/144/454 equal the base line after that one substitution; lines 437/438 differ only in pipe
  field index 4 (last cell, 6 fields both sides); no other one of the 487 lines differs.
- New anchor content was read: `SKILL.md:191` = the `attempts()≥2` telemetry statement; `:176-178` =
  reward object 48 / numeric `reward.min` 14 (round-13 correction); `:827-848` = the EV formula,
  six-decimal `fmt`, and the UNKNOWN fail-closed sentence; `intake-surface.md:89-93` = the same
  reward correction; `mission-control.md:55-57` = peak `openai-codex/gpt-6-astra:max` with the
  round-13 correction.

## Item details

### 1 — depth:density (adjacent axis)

`git rev-parse e15996b:SKILL.md 9225954:SKILL.md` returns the same blob `27f23a93848be29b76992ac35ce423ab9a23c269`;
`git show <rev>:SKILL.md | sha256sum` is `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552` at base,
at tip and for the working-tree file; `git diff --stat e15996b 9225954 -- SKILL.md` is empty (rc 0).
`density.py` run on the base bytes and on the working tree, both `--label r93`: identical output
(`diff` rc 0), `1251 lines, 38 blocks`, `mean dens 273.2`, `Total path-citation instances: 932`.
No SKILL.md path is touched by either landing, so this axis cannot move.

### 2 — false positives of the landed scanner

- Capture scope at the tip (`--rev 9225954`, tip allowlist): `scanned=1957 hits=0 files=0 allowed=24 unused_allow=0 rc=0`.
- Required file scope (`--files`, all 103 `corpus/knowledge` entries + all 183 `corpus/source-snapshots`
  files): `scanned=286 hits=0 files=0 allowed=9 unused_allow=14 rc=0`. `unused_allow=14` is
  scope-driven: the 23-row allowlist has 9 rows under those two subtrees (S078 1, S124 2, S128 1,
  S130 1, S139 4), all consumed (`9` allowed matches); the 14 unused rows are the round-85
  `ExecC1Hunt-receipts/*.json` rows, which are not in a knowledge/snapshot file list. The full-tree
  `--rev` scan consumes all 23 rows (24 allow-listed occurrences; one row binds two occurrences),
  `unused_allow=0`.
- Wider differential (attack, not required): all 6,275 tracked `.md` at tip, same file bytes, base
  scanner vs landed scanner — both exit 1 with the **identical** 23 hits in 18 pre-existing files
  (round-25..47 seat reports and `corpus/lessons/round-87-verifier-spotcheck.md:61,:67`). No
  `github-token`, no `gitlab-pat`, and no escape-boundary hit appears anywhere; the new shapes add
  zero false positives to the whole Markdown tree.
- The S139 snapshot (the round's own GitLab page) scans clean: its 4 allowlisted matches bind and no
  `gitlab-pat` HIT appears in it or in any other snapshot.

### 3 — ReDoS / cost on a 1 MiB near-miss line

Fixtures are single lines of exactly 1,048,576 bytes made of repeated near-miss units
(`glpat-`+19 chars, `ghp_`+35 chars, mixed, plus `\u0020`/`%20` storms); every run was asserted
`rc=0` with no `HIT` line. End-to-end (`python3 -B capture-secret-scan.py --files <fixture>`,
including interpreter start, 3 independent reps): glpat 0.3936–0.4261 s, ghp 0.4187–0.6278 s,
mixed 0.4867–0.5492 s — i.e. **≈394–628 ms per 1 MiB line** on a host shared with peer seats.
Scaling (landed, 1/2/4/8 MiB of the ghp near-miss unit): 0.585/1.661/2.961/4.400 s ⇒ 585/831/740/550
ms/MiB, flat within noise. Single-process `finditer` isolates the regexes: landed `github-token`
36.4 µs/KiB at 1 MiB (base 17.6) and `gitlab-pat` 37.7 µs/KiB, both flat to 8 MiB (ratio 0.81–1.18).
Paired base-vs-landed mins on the 1 MiB cases are 0.2839–0.3782 s vs 0.3733–0.4339 s (≈1.0–1.5×).
No nested quantifier and no super-linear term; the widened boundary costs a fixed per-position
constant (two fixed-width lookbehind alternatives instead of one).

### 4 — old capabilities: frozen round-92 C2 counter at the landed state

Counter extracted from `5bad9e5:.ufo/waves/round-92/c2/capability-check.py`
(sha256 `3feed3b073194179b5542f91d7bba80f8d1fba1a3c3a3ec3d4587ce1c6baa847`), run unpinned at
`--rev 9225954`, seed 3394888229:

```
LIMB K1 pass selftest_rc=0 instrument_sha256=7d9d7309… gate_sha256=8b6f8493…
LIMB K2 pass rc=1 sts_files=2 oracle=2 oracle_matches_expected=True
LIMB K3 pass rc=0 summary=scanned=1957,hits=0,files=0,allowed=24,unused_allow=0
LIMB K4 pass rc=1 missing=none extra=none sts_allow_rc=2 files_rc=1 files_hits=2 files_ok=True
LIMB K6 pass base_rc=1 base_hits=22 new_caught_by_base=none
LIMB K7 pass seed=3394888229 rc=1 missing=none extra=none
LIMB K8 pass clauses=29 failing=none
LIMB K5 pass rows=1
CAPABILITY-CHECK-RESULT pass rc=0
```

So the round-92 plant set is matched exactly (no extra and no missing hit from the widened boundary
or the new shape), the round-86 STS history still flags exactly the two oracle files, the clean tip
scan still consumes every allow row, and the round-91/92 clauses remain green. The landed
`--selftest` prints `SELFTEST-RESULT pass cases=90` (68 in round 92); the shape list grows from 13
to 14 with every prior name intact.

### 5 — C1 citation-class movement in corpus/knowledge

Method: every backticked path-like token in every file under `corpus/knowledge` at each extracted
base/landing tree (`git archive`), classified with the lane's own `resolve.py`
`classify(token, lane_root, mirror_root)`; mirror root absent (`~/Projects/the-bounty-hunter` does
not exist), so `MIRROR-EQUIVALENT` is unreachable for both sides.

| Rev | distinct tokens | occurrences | GONE | resolving | classes |
|---|---:|---:|---:|---:|---|
| base `e15996b` | 2001 | 3315 | 994 | 1007 | INTERNAL 984, RESOLVES 23 |
| landing `ae53b3c` | 2000 | 3316 | 991 | 1009 | INTERNAL 986, RESOLVES 23 |

These are exactly the frozen meter's M0 `1007/2001` and M1 `1009/2000`, re-derived without the
meter. Only `corpus/knowledge/triage-thresholds.md` differs between the two trees; the other 102
knowledge files are byte-identical.

Token-level: 6 distinct tokens leave, 5 enter. Leaving: `SKILL.md:111`, `SKILL.md:117`,
`SKILL.md:494-506` (all resolving) and `intake-surface.md:75-76`, `mission-control.md:37-38`,
`openai-oauth/gpt-6-astra:max` (all GONE). Entering: `SKILL.md:176-178`, `SKILL.md:191`,
`SKILL.md:827-848`, `corpus/knowledge/intake-surface.md:89-93`,
`corpus/knowledge/mission-control.md:55-57` (all resolving, INTERNAL). Site-level: exactly five lines
changed (58, 144, 437, 438, 454); each landing line carries at least one resolving token; the only
site with no resolving token at base (438) gains one. **No citation site lost a resolving citation**;
the three retired resolving strings are precisely the mispointed anchors this tranche was chartered
to replace (117 provenance text; 111 `reward`-exists conflation; 494-506 park-disposition text),
and each site carries its replacement. Net resolving +2, so the class movement is repair, not loss.
`openai-oauth/` enters as a GONE token because the corrected 9.6 cell records the superseded prefix;
that is a documented mention, and it is the only added GONE string.

### 6 — dependent intake gate at the tip

Local HTTP fixtures served to `capture-source.py` (unchanged `0630d32b…`) with the committed
allowlist passed explicitly; fabricated values, never printed:

| case | rc | gate output |
|---|---:|---|
| clean text | 0 | `status=200 … snapshot_bytes=20 sha256=6fe4afe6…`; file written |
| planted `ghp_`+36 | 3 | `INTAKE-REFUSED T93 shape=github-token line=1 … written=no`; no out file |
| planted `glpat-`+20 | 3 | `INTAKE-REFUSED T93 shape=gitlab-pat line=1 … written=no`; no out file |
| both lines | 3 | `shape=github-token line=1` and `shape=gitlab-pat line=2`; no out file |

The gate still refuses through the imported `patterns()` (fail-closed path unchanged); the new shape
propagates to capture intake with no code change, and clean text is still admitted.

## Routed qualifiers (no verdict change; none re-scores a claim)

- **Q1 (depth:verifiability, 454 MATCHES anchor is partial).** The repointed cell cites
  `SKILL.md:827-848`, which supports its headline relation (EV formula 827-833, six-decimal `fmt`
  843-844, UNKNOWN fail-closed 846-848). The cell's parenthetical also names 10-input print order,
  exit-2 paths and non-persistence; those are not stated inside the cited range — exit-2 paths are
  at 850-855, non-persistence at 807-811, and 827-848 ends at the fail-closed sentence. Same class
  as round-92 F2 (a partial `MATCHES`),
  but a net improvement: the base anchor 494-506 contains no EV term at all. Smallest safe
  correction: a round-94 label that narrows the parenthetical or cites the additional ranges; no
  post-landing edit under the frozen map.
- **Q2 (depth:verifiability, documented partial at 58/144).** The two ties now cite
  `SKILL.md:191`, which states the `attempts()≥2` threshold but not the literal constant name
  `MAX_ATTEMPTS` (0 occurrences in SKILL.md, as the label records). This is exactly the round-92 F1
  correction ("repoint to `SKILL.md:191` or drop the tie"); no in-tree anchor states the name.
  Recorded so the remaining partial is not mistaken for a new false-provenance defect.
- **Q3 (depth:verifiability, token-set reading).** A census that compares distinct token strings
  alone will report 3 resolving strings "lost" (`SKILL.md:111`, `:117`, `:494-506`). They are the
  intentionally replaced anchors; every site carries a resolving replacement, and the resolving
  count rises 1007 → 1009. Do not read that string delta as a lost citation.
- **Q4 (coverage, cost).** The widened `github-token` left boundary measures 17.6 → 36.4 µs/KiB on
  a pure near-miss line (≈2.1×), and a 1 MiB single-line scan costs 0.37–0.63 s end-to-end on this
  loaded host. It is linear (flat 1–8 MiB) and no ReDoS; noted for future capture sizes (the fetch
  cap is 32 MiB). No action required this round.

## Counterexamples tested and rejected

- *"The widened escape boundary or `gitlab-pat` flags ordinary docs."* No: 0 hits in all 286
  knowledge/snapshot files, 0 hits in 1,957 capture-scope blobs, and the base-vs-landed hit set over
  all 6,275 tracked `.md` is identical (23 pre-existing hits, none of the new shapes).
- *"The new left boundary backtracks quadratically."* No: single-process `us/KiB` is flat across
  1/2/4/8 MiB (ratio 0.81–1.18) for both shapes; lookbehinds are fixed width; end-to-end scaling is
  flat within host noise.
- *"A capability regressed under the round-92 counter."* No: K1–K8 pass at tip; K4 exact set
  (`missing=none extra=none`); K3 `hits=0 unused_allow=0`; K6 base still misses every new plant.
- *"The repair lost resolving citations."* No site-level loss: five changed lines, each with a
  resolving token after; resolving distinct tokens 1007 → 1009. The only retired resolving strings
  are the replaced anchors themselves.
- *"The intake gate silently admits a new-shape secret."* No: both planted families refuse with the
  correct shape names, rc 3, and no output file; clean text still writes.
- *"The landing smuggled other paths or a shape-name loss."* No: path sets are exactly one and two
  files; the SCORECARD row keeps all prior shape names and the first-working-round cell; freeze
  counter/map/labels/candidate bytes are untouched by both landings.

## Files written

- `.ufo/waves/round-93/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-93/w1/CriticHarm-receipts/density.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/false-positives.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/redos.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/old-capabilities.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/c1-class-diff.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/c1-sites.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/intake-gate.txt`
- `.ufo/waves/round-93/w1/CriticHarm-receipts/landings.txt`

No lane file outside `w1/` was written; no `git`/`jj` mutation was issued; no subagent was spawned;
no package manager or tool install ran (so no tool/version/channel entry is owed). Scratch
`/fast/scratch/hyaku/kasegi-r93/CriticHarm` is deleted; receipts carry paths, line numbers, digests
and summary/HIT lines only, never a matched credential value.

## Receipts

Each command ran with cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (or the stated scratch
directory) and absolute paths; `$S=/fast/scratch/hyaku/kasegi-r93/CriticHarm`;
`$R=.ufo/waves/round-93/w1/CriticHarm-receipts`. Full outputs are in `$R/`.

1. `git rev-parse e15996b 5bad9e5 ae53b3c 9225954` — rc 0; the four pinned commits; `HEAD` = `9225954…`.
2. `git diff-tree --no-commit-id --name-status -r ae53b3c` — rc 0; `M corpus/knowledge/triage-thresholds.md` (1 path).
3. `git diff-tree --no-commit-id --name-status -r 9225954` — rc 0; `M SCORECARD.md`, `M corpus/instruments/capture-secret-scan.py` (2 paths).
4. `git diff --numstat e15996b ae53b3c -- corpus/knowledge/triage-thresholds.md` — rc 0; `5 5`; line counts 487/487.
   `git diff --numstat e15996b 9225954 -- SCORECARD.md corpus/instruments/capture-secret-scan.py` — rc 0; `1 1`, `46 5`.
5. `git rev-parse e15996b:SKILL.md 9225954:SKILL.md` — rc 0; both `27f23a93848be29b76992ac35ce423ab9a23c269`.
   `git show <rev>:SKILL.md | sha256sum` — both `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552`.
6. `git diff --stat e15996b 9225954 -- SKILL.md` — rc 0; empty.
7. `python3 -B corpus/instruments/density.py <base-bytes> --label r93` and
   `python3 -B corpus/instruments/density.py SKILL.md --label r93` — both rc 0; outputs identical
   (`diff` rc 0), `1251 lines, 38 blocks`, mean 273.2, 932 path-citation instances.
8. `python3 -B corpus/instruments/capture-secret-scan.py --lane <lane> --rev 9225954 --allow <tip allowlist>` —
   rc 0; `scanned=1957 hits=0 files=0 allowed=24 unused_allow=0`.
9. `cd $S/tip && python3 -B corpus/instruments/capture-secret-scan.py --files $(cat $S/scope-files.txt)` —
   rc 0; 286 files, `hits=0 files=0 allowed=9 unused_allow=14`.
10. `cd $S/landing && python3 -B $S/base/corpus/instruments/capture-secret-scan.py --files $(cat $S/all-md.txt) --allow <tip allowlist>`
    and the same with the tip scanner — both rc 1; both `scanned=6275 hits=23 files=18`, identical HIT sets.
11. `python3 -B corpus/instruments/capture-secret-scan.py --selftest` — rc 0; `SELFTEST-RESULT pass cases=90`.
12. ReDoS: `python3 -B capture-secret-scan.py --files <1 MiB near-miss fixture>` ×3 per case — all rc 0,
    no HIT; glpat 0.3936–0.4261 s, ghp 0.4187–0.6278 s, mixed 0.4867–0.5492 s. Scaling 1/2/4/8 MiB:
    0.5847/1.6614/2.9610/4.3995 s (landed), base 0.3357/0.9957/1.4983/2.8905 s. Single-process
    `finditer`: landed github 36.4/39.0/40.8/39.0 µs/KiB, gitlab 37.7/39.9/38.3/37.9, base github
    17.6/17.2/16.9/18.0 (1/2/4/8 MiB), ratio_8x 0.81–1.18.
13. `python3 -B $S/r92/capability-check.py --lane <lane> --rev 9225954 --work $S/r92work` — rc 0; K1–K8 pass,
    seed 3394888229, K3 `scanned=1957,hits=0,files=0,allowed=24,unused_allow=0`, K4 `missing=none extra=none`,
    K8 `clauses=29 failing=none`.
14. C1 class differential (own script, `resolve.py` imported from the lane) — base classes
    `{GONE:994, INTERNAL:984, RESOLVES:23}`, landing `{GONE:991, INTERNAL:986, RESOLVES:23}`; 2001→2000
    distinct; 6 base-only/5 landing-only tokens; changed lines `[58,144,437,438,454]`; lost resolving
    sites `none`; only `triage-thresholds.md` differs among 103 knowledge files.
    Byte-level check: 58/144/454 equal after the single token substitution; 437/438 differ only in
    pipe field 4.
15. `python3 -B corpus/instruments/capture-source.py --id T93 --url http://127.0.0.1:<ephemeral>/<case>.txt --out $S/intake/out-<case>.txt --kind text --allow <committed allowlist>`
    — clean rc 0 and written; github rc 3 `INTAKE-REFUSED … shape=github-token line=1 … written=no`;
    gitlab rc 3 `shape=gitlab-pat line=1 … written=no`; both rc 3 with both lines; no out file on refusal.
16. `cd $S/landing && python3 -B <scanner> --files $(cat $S/all-md.txt)` — see #10.
