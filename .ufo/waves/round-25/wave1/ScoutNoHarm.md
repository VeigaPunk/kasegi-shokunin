# Round 25 wave 1 — no-harm baseline (ScoutNoHarm)

Seat: `L1Kasegi25.ScoutNoHarm` · read-only · lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Lane base revision: `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
Captured: 2026-10-25, before any round-25 fix landed. All commands run from the lane root
(`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`) unless stated. No file in the lane was edited by
this seat; the only output is this receipt.

---

## 1. `python3 corpus/instruments/density.py SKILL.md --label r25-before`

Exit code: **0**

```
# Density census — r25-before (1023 lines, 19 blocks)
# ev = path-cites + concrete-tbl-rows + numerics + signatures; dens = ev*100/nb
# num: unique numeric tokens (no bare years, no letter-adjacent fragments, no
#      enumeration markers, no date/time stamps; letter-free code spans count);
# sig: unique ALL-CAPS parts >=5 chars incl. non-path-like code spans, minus
#      GENERIC_SIG (full rules: see density.py docstring)

| # | block | lines | nb | cites | tbl | num | sig | ev | dens |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Pipeline (observed, not invented) | 18 | 15 | 1 | 0 | 0 | 1 | 2 | 13.3 |
| 2 | Program-rule checklist (step 1 of any mission) | 70 | 65 | 22 | 0 | 44 | 0 | 66 | 101.5 |
| 3 | Policy access playbook (fleet-learned) | 10 | 8 | 24 | 5 | 8 | 0 | 37 | 462.5 |
| 4 | Finding-triage decision table | 37 | 32 | 24 | 7 | 15 | 4 | 50 | 156.2 |
| 5 | Intake surface — the map is decorative, ingestion is hidden | 51 | 47 | 15 | 0 | 30 | 4 | 49 | 104.3 |
| 6 | Mission ledger & audit store | 27 | 24 | 21 | 0 | 16 | 6 | 43 | 179.2 |
| 7 | Mission control plane | 28 | 26 | 17 | 0 | 14 | 2 | 33 | 126.9 |
| 8 | UFO runtime workspaces — the untracked `.ufo/` layer + `.omp/` | 42 | 38 | 25 | 0 | 30 | 4 | 59 | 155.3 |
| 9 | Ops integrity layer — invariants, intake, finalize | 130 | 122 | 103 | 0 | 20 | 14 | 137 | 112.3 |
| 10 | VDP disclosure packages (sibling format) | 26 | 23 | 18 | 0 | 8 | 1 | 27 | 117.4 |
| 11 | Retirement lane — autopsies & the detail regex | 62 | 57 | 30 | 0 | 19 | 4 | 53 | 93.0 |
| 12 | Evidence-package anatomy | 28 | 24 | 20 | 6 | 13 | 3 | 42 | 175.0 |
| 13 | Disclosure anti-patterns (all observed in fleet wrap review) | 115 | 110 | 68 | 10 | 47 | 3 | 128 | 116.4 |
| 14 | Claim-hardening wave — the defect layer above the gates | 35 | 30 | 22 | 10 | 21 | 9 | 62 | 206.7 |
| 15 | Submitted-state registry — the do-not-refile set | 50 | 46 | 25 | 0 | 20 | 5 | 50 | 108.7 |
| 16 | Operator queue — live audit | 40 | 36 | 18 | 0 | 16 | 1 | 35 | 97.2 |
| 17 | Triage economics | 171 | 156 | 126 | 18 | 46 | 15 | 205 | 131.4 |
| 18 | Cited paths (verified 2026-09-28 against the then-live tree; round-13 full-set re-audit 705/708 resolved — **and as of round 15 the `~/Projects/bounties` root itself is gone**, so every path below is `[lost-tree]`; **round-19 re-census (2026-10-14): the mirror and origin-work roots that used to carry the exceptions are also gone**, so there are no live exceptions left — the previous clause "unless it has a mirror equivalent in `~/Projects/the-bounty-hunter` or lives under `~/Projects/origin-work/open-bug-bounties`" is historical. Resolvability is measured, not assumed: `corpus/instruments/resolve.py`, census of record `corpus/instruments/citation-survival.md` — SKILL.md 47/289 = 16.26 % before the round-15 re-anchor, 222/486 = 45.68 % at round-15 close, re-censused at round 19; this header is itself inside the measured file, so the figure is a fixed point only to ±1 token) | 38 | 36 | 66 | 0 | 41 | 6 | 113 | 313.9 |
| 19 | Frontier decision table (round 22) | 10 | 9 | 7 | 5 | 2 | 0 | 14 | 155.6 |
| | **mean dens** | | | | | | | | **154.0** |

Total path-citation instances: 652 across 19 blocks.
```

Aggregates for the diff (exact strings emitted):

| metric | value |
|---|---|
| file lines | `1023` |
| block count | `19` |
| file mean dens | `154.0` |
| total path-citation instances | `652` |
| output sha256 (stdout+stderr) | `d1708ba3a28d4356e60aae1e29a13bcc87fab74f5e2ef3c3680eb1b9cd2cba56` |

The fenced block above is the complete 31-line output, reproduced verbatim — verified byte-identical to the
live run (3209 bytes, sha256 `d1708ba3a28d4356e60aae1e29a13bcc87fab74f5e2ef3c3680eb1b9cd2cba56`).

---

## 2. `python3 corpus/instruments/anchorcheck.py SKILL.md`

Exit code: **0**

Header line (verbatim):

```
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

Counters:

| counter | value |
|---|---|
| in-range cite instances | `7` |
| bad | `0` |
| distinct anchors | `7` |
| LOST-RECORDED | `306` |
| PIN-BROKEN | `0` |
| ORIGIN | `0` |
| OUTSIDE-BASE | `0` |
| BASE-ABSENT | `0` |
| `OK md:` lines | `7` |
| total output lines | `315` |
| output sha256 (stdout+stderr) | `61abb8f6ab3b8749465eb5094ba430a37cdba4e8929ed20fef4608bf2d858464` |

The 7 `OK md:` (resolved) anchors, verbatim, truncated to 200 columns for this table:

```
OK md:120 corpus/knowledge/program-quirks.md:10  [- **$100 submission deposit** — the claimability gate is a read-only]
OK md:132 corpus/knowledge/policy-access-playbook.md:13  [| Terms-gated policy | SIX Group: reading Program Rules requires terms acceptance | Terms acceptance]
OK md:338 corpus/knowledge/ops-invariants.md:24  [| `gitMutationBlocker` | fail-closed preflight | refuses when rebase-merge/rebase-apply/MERGE_HEAD/C]
OK md:416 corpus/knowledge/intake-and-finalize.md:78-92  [For every `claims/<id>/<slug>/status.json` it then: ⏎  ⏎ 1. **Filters**: skip `state !== 'DONE'`; skip verdict matching ⏎ `/not.claimabl
OK md:696 corpus/knowledge/ufo-archive-2026.md:150-154  [14. Claims marked "verified" but never executed (coinbase vectors 3-4 + ⏎ path-form boundary); overclaims contradicted by the package's own �
OK md:697 corpus/knowledge/ufo-archive-2026.md:145-149  [13. Stale file:line citations — the single most common narrative defect ⏎ (metamask :161→:162, elastic :604→:605 check + api.search.go
OK md:821 corpus/knowledge/mission-control.md:3  [Source: `~/Projects/bounties/ops/fleet-dispatch.mjs` (read in full, 427]
```

The output is 315 lines: a leading blank line, the `==` header (line 2), then 306 `LOST-RECORDED md:<line>
[lost-tree|lost-base] <path>:<range> (not checked)` lines and 7 `OK` lines in emission order. The
LOST-RECORDED lines are not reproduced here because the command regenerates them byte-identically (digest
above); their `md:` line numbers span 57–989.

---

## 3. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain` and `rev-parse master`

Exit code: **0** (both)

```
?? .ufo/waves/round-25/
?? corpus/instruments/recheck-audit.py
?? corpus/source-snapshots/round-25/
```

```
b49948f1164ef65106b2c4cbee3f53e8a44b8c41
```

- Working tree was clean apart from three untracked paths at capture time: the round-25 wave directory, the
  C1 instrument `corpus/instruments/recheck-audit.py`, and the C2 source snapshots directory. No tracked file
  was modified or staged.
- `rev-parse master` = `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` — identical to the lane base revision named
  in the round brief, so `master` was at base when this baseline was taken.

---

## 4. sha256 at `b49948f` — files the round has not touched

Command shape: `git show b49948f1164ef65106b2c4cbee3f53e8a44b8c41:<path> | sha256sum` for each path.

| path | sha256 at b49948f | sha256 in working tree at capture | same? |
|---|---|---|---|
| `corpus/instruments/resolve.py` | `db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667` | `db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667` | yes |
| `SKILL.md` | `f74a9f3334688f8ef62b233c1173f5583f7edf3d03e8159be0787320677324af` | `f74a9f3334688f8ef62b233c1173f5583f7edf3d03e8159be0787320677324af` | yes |
| `corpus/README.md` | `88081296345bf31d679874975314b44602d5649b336cdaa9f8263fb5b7d7f7cc` | `88081296345bf31d679874975314b44602d5649b336cdaa9f8263fb5b7d7f7cc` | yes |
| `SCORECARD.md` | `8129f35e9cdc65858de5ce663a6223c7d46fdf605ec9eb2f765604a2eaa91dff` | `8129f35e9cdc65858de5ce663a6223c7d46fdf605ec9eb2f765604a2eaa91dff` | yes |

All four files matched their base blob byte-for-byte at capture time, i.e. the round had not yet touched any
of them when the baseline was taken. A post-round re-hash that still equals the `b49948f` column proves the
round did not touch that file; any difference is a round-caused change.

---

## 4b. Post-capture drift (informational — not part of the baseline)

Wave 1 siblings began landing edits after this seat's capture. Re-check at `2026-10-25T05:31:39-03:00`:

- `git status --porcelain` now lists **31 modified tracked files** — `corpus/QUALITY.md`,
  `corpus/instruments/README.md`, and 29 `corpus/knowledge/*.md` entries — plus the same three untracked paths
  as at capture. At capture time (section 3) there were **zero** modified tracked files, so the baseline above
  is genuinely the pre-fix state.
- The four protected files were still byte-identical to `b49948f` at that timestamp: `resolve.py`,
  `SKILL.md`, `corpus/README.md`, `SCORECARD.md` all unchanged (same digests as the table above).
- Because `SKILL.md` is unchanged, both instrument baselines in sections 1–2 remain reproducible right now;
  the L1's post-round diff of those two commands measures SKILL.md only, and any change is attributable to
  round-25 edits to that file.

Use the `sha256 at b49948f` column as the fixed reference for the protected-file check; the
"working tree at capture" column records the same values only because the tree had not yet moved.

---

## Determinism check (so the L1's post-round diff is meaningful)

Each instrument was run twice in the same conditions; both runs produced byte-identical output:

| instrument | run 1 exit | run 2 exit | distinct output digests across the two runs |
|---|---|---|---|
| `density.py SKILL.md --label r25-before` | 0 | 0 | 1 (`d1708ba3…cba56`) |
| `anchorcheck.py SKILL.md` | 0 | 0 | 1 (`61abb8f6…858464`) |

Both are pure reads of the tree plus the base revision; neither writes to the repo.

## Baseline summary for the no-harm gate

| proxy | baseline value |
|---|---|
| density: file mean dens | **154.0** |
| density: path-citation instances | **652** |
| density: block count / file lines | **19 / 1023** |
| anchorcheck: bad | **0** |
| anchorcheck: LOST-RECORDED | **306** |
| anchorcheck: in-range cites / distinct anchors | **7 / 7** |
| git: base revision | **b49948f1164ef65106b2c4cbee3f53e8a44b8c41** |
| git: dirty tracked files | **none** (3 untracked paths only) |
| four protected files vs base | **all identical** |

No-harm rule the L1 can apply after the round: file mean dens must not fall below `154.0`, path-citation
instances must not fall below `652` (or any fall must be justified as duplicate-removal, not evidence loss),
anchorcheck `bad` must stay `0`, LOST-RECORDED must not grow past `306`, and the four hashes above must be
unchanged unless a round item explicitly owns that file.

Tooling: no tool was installed or upgraded for this seat (only `python3`, `git`, `sha256sum` already present
were used).
