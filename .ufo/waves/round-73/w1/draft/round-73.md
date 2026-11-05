# Round 73 — lesson (kasegi, attempt 1) — DRAFT

Status: DRAFT by seat K73ScribeLesson. Not filed. Lane HEAD is `3b53ff83` (freeze); no C1 or C2 landing commit exists at draft time, and the tracked lane tree is clean. Every "after" value below is pending: the integrator measures it on the landed bytes. Frozen claims: `.ufo/waves/round-73/claims.json` (base `fdf17413`, freeze `3b53ff83`). Wave `w1`. Receipts for every value below: `.ufo/waves/round-73/w1/K73ScribeLesson-receipts.txt` (R-numbers cited as `[R#]`).

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M73-1 | enforcement gap: the Q10 recheck-prefix rule (`corpus/QUALITY.md` Q10, minted round 25) was not checked at admission. 11 entries carry a first `recheck:` line with no `cd <lane-root> && ` prefix; 10 of them exit 2 from a foreign cwd. Ten were admitted in rounds 50–72 after Q10 existed; `root-loss-2026-10-12` (round 19) predates it | `.ufo/waves/round-73/controls/c1-donothing-r73.txt` lines 89–90 (`noprefix=11 exit2_foreign=10 ... nonconformant`) and the ENTRY lines 6, 12, 13, 40, 57, 58, 60, 63, 67, 68, 73. First-adding commits: osv-affected-range-events `e1c3ef5` (r50); cisa-vulnrichment-adp-enrichment `85e1ea5` (r51); nvd-api-2.0-retrieval-interface `227d3ed` (r52); nvd-api-2.0-response-schema `3ffd663` (r53); openssf-scorecard-checks `ff5a1bf` (r54); github-repository-security-advisories-rest-api `d9d77ec` (r55); cisa-vulnrichment-record-list `8c2d9a4` (r56); project-zero-fuzzilli-vs-bigsleep-comparison `7f7dd26` (r60); project-zero-big-sleep-sqlite-variant-analysis `13c8060` (r61); bugzilla-rest-api-bug-endpoints `123796a` (r72); root-loss-2026-10-12 `d1e6e8f` (r19) | `corpus/instruments/recheck-audit.py` `cwd` limb (round 25): `cwd_fail=10` on base bytes [R4], the same ten entries as the census `exit2_foreign` set [R15]. It feeds `score-gap.py` only, not admission. The census's `noprefix` limb is the only detector for `root-loss-2026-10-12` (prefix-less, exit 0 from a foreign cwd). The seat brief's "captured-by: none" was wrong and is corrected here | C1 (claims): prefix the 11 first recheck lines; the new counter `corpus/instruments/recheck-cwd-census.py` (committed in `3b53ff83`) counts `noprefix` and foreign exit codes. Landing pending | base replay of the committed counter: `RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 ... nonconformant`, exit 1 [R1]; selftest green, `cases=1 failures=0`, exit 0 [R2]; one-limb mutant with the prefix limb removed: `selftest cases=1 failures=1`, exit 1 [R3 mut1]; mutant with the foreign-run limb removed: `failures=1`, exit 1 [R3 mut2]; `recheck-audit` base replay `cwd_fail=10 ... exit=1` [R4] |
| M73-2 | duplicate detector: C1 froze a new counter whose foreign-cwd limb compares exit codes only, repeating the `cwd` limb of `recheck-audit.py` (exit code plus output digest). The existing limb already flagged the same ten entries on base. Neither the claim nor the freeze cites it | `.ufo/waves/round-73/claims.json` C1 `counter` names only the new census; `corpus/instruments/recheck-audit.py` docstring limb (b), lines 13–14 | `recheck-audit.py` `cwd` limb (existing since round 25); the claim's counter did not read it | none this round: the frozen counter is kept and the claim text is not reworded. Routed as R-8 below: one instrument of record for the cwd limb | [R15]: on fresh runs both sets have 10 members and are identical (`sets identical=True`); the census adds one entry (root-loss) that the cwd limb cannot see, so the new counter duplicates ten of its eleven findings
| M73-3 | provenance record absent at draft: `corpus/source-snapshots/round-73/` holds `S108.txt` alone, untracked, with no `manifest.json`. R20 requires the manifest (a `url` and a `fetched_utc`) in the same commit as the capture. The fetch instant `2026-11-05T07:40:48Z` appears only in the claims note | [R14] (`git ls-files` prints nothing; `ls` lists `S108.txt` only); `corpus/QUALITY.md` R20 and R21; `.ufo/waves/round-73/claims.json` `source.note` | `capture-binding-check.py` rule A (R20): not run on round-73 at draft time | the L1 writes `corpus/source-snapshots/round-73/manifest.json` in the landing commit, with `url` and `fetched_utc` 2026-11-05T07:40:48Z | open. R20 calls a manifest-less snapshot dir a defect of the round that landed it; the landing-time `capture-binding-check.py` run (C2 counter) is the measurement and is pending |

Note on M73-1's "able to fail" fixture: the census `--selftest` builds three entries (`a-prefixed.md`, `b-relative.md`, `c-bare-pass.md`) and asserts `noprefix=2 exit2_foreign=1 exit0_foreign=2` (`corpus/instruments/recheck-cwd-census.py` lines 99–131). Two one-limb mutants of the committed bytes each turn it red.

## Gate

- Source S108: `https://google.github.io/osv.dev/post-v1-query/` (the OSV.dev `POST /v1/query` page).
- Access date: 2026-11-05.
- Fetch instant: `2026-11-05T07:40:48Z`, from `.ufo/waves/round-73/claims.json` (C2 `source.note`). No manifest records it yet (M73-3). The capture file's mtime, `2026-11-05 04:40:48 -0300` (= 07:40:48Z), agrees but is not a fetch record. "HTTP 200" is claimed in the same note and recorded nowhere else.
- Capture: `corpus/source-snapshots/round-73/S108.txt`, 150 lines [R6]; sha256 `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9` [R6], matching the claims pin.
- Located quote, capture line 148 (12 words; `grep -n 'response size limit of 32MiB'` [R6]):
  "The API has a response size limit of 32MiB when using HTTP/1.1."
  The same line continues "There is no limit when using HTTP/2." — not quoted here.
- The OSV overview page (`api/`) is not claimed. The F31 scope limit stays as written; F51 admits the service contract only.
- The remaining C2 quotes belong to the F51 entry (draft path in the wave spec: `.ufo/waves/round-73/w1/draft/F51-entry.md`); they are not verified by this seat.

## Routed defects

Round-72 items named for this lesson. None is repaired by round 73 (claims `non_claims`). Each is open, unchanged.

- **R-1** `--json` and `--root` are outside the census's write-class set (`derive-head-census.py`). Owner: next round.
- **R-2** `freeze-check.py` runs `bash -c` on the claims file's `counter_cmd` (sentinel row 33). Owner: next round.
- **R-3** `sort -T` / `--temporary-directory` create and unlink files outside the root (sentinel rows 14, 15, 18). Owner: next round.
- **R-4** the round-71 harm-count correction (19 / 23 / 43 / 26, by predicate), which the round-72 lesson routes to that round's SCORECARD section. Landing not verified by this seat. Owner: as routed in round 72.
- **R-5** a realpath-resolved alias to a census head is admitted under a non-census name. Owner: next round.
- **R-6** a regular file named like a fixture head is keyed by name (inference only). Owner: next round.
- **R-7** `capture-binding-check.py --root .` is admitted on base and candidate. Owner: next round.
- **L72-2** a gate mutant that drops the `derive-head-census.py` census entry survives the counter (the selftest case `python-census-covers-instruments` catches it). Owner: next round, a counter self-test.
- **L72-3** counter-internal mutants survive (C2 POSITIVE dropped; C3 forged alias). Owner: next round, a counter freeze amendment.
- **L72-8** a duplicated S107 registry row leaves `FRONTIER-CENSUS registry=107` exit 0; only `sources-census.sh` E12 catches it. Owner: next round.
- **L72-11** `probes()` in `derive-head-census.py` copies heads from `dirname(--gate)` by fixed name. Owner: next round, a counter amendment.

Round-73 routed item:

- **R-8** M73-2: one instrument of record for the foreign-cwd limb. Either `recheck-audit.py`'s `cwd` limb joins the admission path and the census is retired, or the census's `noprefix` limb is folded into `recheck-audit.py`. Owner: next round; the decision is the operator's. Measured inputs: [R4], [R15].

## Residuals

1. C1 after-values are pending the landing commit. Predicate (claims): `noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22`, census `conformant`, selftest green.
2. The census compares exit codes only; it does not compare outputs. `recheck-audit.py`'s cwd limb compares both. On base, the digest limb passes for all 78 entries outside its ten `cwd_fail` [R4].
3. `root-loss-2026-10-12` is a round-19 line that predates Q10. Its repair adds only the prefix; its foreign exit stays 0 (C1 predicate counts it in `exit0_foreign=66`).
4. The round-73 receipts carry no instrument digest and no timestamp (see Process note).
5. `corpus/lessons/round-71.md:70` names `python3 corpus/instruments/frontier-recheck-count.py` in prose (N8). It is not a recheck field and not a Q10 instance; it is left unchanged.
6. M73-3: the manifest is not yet written.
7. The C2 entry's corpus path is not named by `claims.json`. Its draft path is in the wave spec (see Gate).

## Registry changes (old → new)

- S108 (OSV.dev `POST /v1/query` service contract): **none → mined**. The row is not in `corpus/SOURCES.md` at draft time (frontier census `registry=107` at base [c2 receipt]). It lands with C2.
- S108 recheck: **none → 90d** (pending landing).
- S108 used-by: **none → the F51 entry path** (pending landing; corpus path named by the integrator; draft at `.ufo/waves/round-73/w1/draft/F51-entry.md`).
- Knowledge-expected: list added. Base: `lines=90 rows=88` [R7]; `LC_ALL=C sort -c` exit 0 [R7]. After (pending): 91 lines / 89 rows, sort clean.
- Knowledge files: 88 at base [R7]; after (pending): 89.
- Census, before: `TMPDIR=<scratch> python3 corpus/instruments/recheck-cwd-census.py --root .` → exit 1 [R1, replayed on base bytes]. After (pending): the claims predicate, exit 0.
- Census selftest, before: `selftest cases=1 failures=0`, exit 0 [R2].
- Sources census, before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` run from the fleet root → `kasegi ok ...`, exit 0 [R5], W04 duplicate-URL warnings inherited. After (pending): exit 0.

## Sourced claim

C2 rests on S108, captured this round (fetch instant in Gate; manifest pending, M73-3). The located quote is at capture line 148 (Gate). C1 rests on no external source: it reads `corpus/knowledge/*.md` and runs each entry's own recheck command.

## Sweep (cwd dependence, run this round)

Knowledge, all recheck lines (`cd` prefix against the lane root), run from the lane root:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -c 'import glob,os,sys
root=sys.argv[1]; pre="cd %s && "%root; n=0; bad=[]
for p in sorted(glob.glob(root+"/corpus/knowledge/*.md")):
    rl=[l for l in open(p,encoding="utf-8",errors="replace") if l.startswith("recheck:")]
    n+=len(rl); bad+=[os.path.basename(p) for l in rl if not l[len("recheck:"):].strip().startswith(pre)]
print("KNOWLEDGE-RECHECK-LINES total=%d noprefix_any=%d" % (n,len(bad)))' /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Output (verified at draft time): `KNOWLEDGE-RECHECK-LINES total=88 noprefix_any=11`, exit 0. Files with a count of recheck lines other than 1: none (`grep -c '^recheck:' corpus/knowledge/*.md | grep -v ':1$'` prints nothing, exit 1). Non-first prefix-less lines: 0 (no entry has a second recheck line).

Round 71 and 72 lessons and their verifier spot-checks:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -nE 'recheck' corpus/lessons/round-71.md corpus/lessons/round-71-verifier-spotcheck.md corpus/lessons/round-72.md corpus/lessons/round-72-verifier-spotcheck.md | grep -E '(python3|bash|sh|grep|sha256sum|test|wc|cat|diff) +corpus/' | grep -v 'kasegi-shokunin && '
```

Output: one line, `corpus/lessons/round-71.md:70` (prose, see Residual 5). `grep -nE 'cwd|foreign|from any|exit 2'` over the same four files: no match (exit 1).

## Process note (order of events, as known)

1. The base census (`c1-donothing-r73.txt`) and the C2 do-nothing counters (`c2-donothing-r73.txt`) were run at base `fdf17413`. Per the L1, the C1 census was run before freeze commit `3b53ff83` was written. Neither receipt carries a timestamp or an instrument digest, so the wall-clock order against the freeze cannot be read from the receipts. It rests on the L1's statement.
2. Freeze `3b53ff83` (`2026-11-05T04:43:44-03:00`, i.e. `07:43:44Z`) adds `claims.json`, both receipts and `corpus/instruments/recheck-cwd-census.py` [R13]. Its diff against base touches no other knowledge or instrument file, so base and freeze bytes agree on the census inputs [R13].
3. The S108 capture was written at `07:40:48Z`, about three minutes before the freeze. The capture therefore precedes the frozen C2 target. This is the reverse of M72-5, where the freeze preceded the capture.
4. The capture is not in the freeze commit (untracked; no manifest) [R14].
5. This seat replayed the census with the committed bytes (the `3b53ff83` census on base knowledge bytes, recheck prefix rewritten to a scratch copy of base). It reproduced the receipt counts exactly [R1]. The counts therefore do not depend on any byte of the census that was uncommitted when the base run was made.
6. The seat brief's premise, "no counter reads recheck cwd", was not checked before the claim was written. `recheck-audit.py` has had a `cwd` limb since round 25 (M73-2).

## Assimilation and considerthese

Not assessed by K73ScribeLesson. The integrator records `merge/kasegi/` and `considerthese/` dispositions at landing.
