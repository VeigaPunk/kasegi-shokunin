# K73ScribeLesson — round-73 lesson draft (scribe seat)

Seat: `K73ScribeLesson` (scribe, leaf, no subagent dispatch). Item produced: the round-73 lesson draft. Items attacked: (1) M73-1's `captured-by` premise in the seat brief; (2) the C1 census as a duplicate of an existing detector; (3) the C2 provenance record (S108 manifest). Frozen claims read in full: `.ufo/waves/round-73/claims.json` (freeze `3b53ff83`, base `fdf17413`); predicates and kill rules were not reworded.

## Outputs

- Draft lesson: `.ufo/waves/round-73/w1/draft/round-73.md` (this seat's only lesson output; not filed, not in `corpus/lessons/`).
- Receipts: `.ufo/waves/round-73/w1/K73ScribeLesson-receipts.txt` (blocks R1–R15, each with command and exit code).
- This report: `.ufo/waves/round-73/w1/K73ScribeLesson.md`.
- Scratch `/fast/scratch/hyaku/kasegi-r73/K73ScribeLesson/` (archives of base and freeze, mutant copies, sweep script); removed after the receipts were copied.

## Mistakes table (compact; full cells in the draft)

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M73-1 | enforcement gap: Q10 prefix rule (round 25) not checked at admission; 11 first recheck lines prefix-less, 10 exit 2 from a foreign cwd; 10 admitted r50–r72, root-loss r19 | `c1-donothing-r73.txt` lines 89–90; ENTRY lines 6,12,13,40,57,58,60,63,67,68,73; admitting commits in draft | `recheck-audit.py` `cwd` limb (round 25): `cwd_fail=10` [R4]; feeds `score-gap.py` only. Brief's "captured-by: none" corrected | `recheck-cwd-census.py` (committed `3b53ff83`); prefix repair pending landing | R1 base replay exit 1 (`noprefix=11 exit2_foreign=10`); R2 selftest `failures=0` exit 0; R3 mut1 (prefix limb removed) and mut2 (foreign-run limb removed): each `failures=1` exit 1 |
| M73-2 | duplicate detector: the new census's foreign-cwd limb repeats `recheck-audit.py`'s `cwd` limb; freeze cites neither | `claims.json` C1 `counter`; `recheck-audit.py` docstring limb (b), lines 13–14 | `recheck-audit.py` `cwd` limb (existing) | none this round (claims kept); routed R-8 | R15: both sets = same 10 entries, `sets identical=True`; census adds root-loss only |
| M73-3 | provenance absent at draft: S108 capture untracked, no `manifest.json` (R20); fetch instant only in claims note | R14; QUALITY R20, R21; `claims.json` `source.note` | `capture-binding-check.py` rule A (not run at draft) | L1 writes manifest in landing commit | open; landing-time counter run pending |

## Gate block

- URL: `https://google.github.io/osv.dev/post-v1-query/`
- Access date: 2026-11-05. Fetch instant `2026-11-05T07:40:48Z` is from the claims note; no manifest yet (M73-3). HTTP 200 is claimed there and recorded nowhere else.
- Capture: `corpus/source-snapshots/round-73/S108.txt`, 150 lines, sha256 `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9` (R6: `sha256sum` and `wc -l`; both match the claims pin).
- Located quote, **capture line 148** (12 words; R6 `grep -n 'response size limit of 32MiB'`):
  "The API has a response size limit of 32MiB when using HTTP/1.1."
- Not claimed: the OSV overview page (`api/`); F31 scope stays as written.

## Sweep: cwd dependence in knowledge and lessons

Command (self-contained; reproduces the all-lines count):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -c 'import glob,os,sys
root=sys.argv[1]; pre="cd %s && "%root; n=0; bad=[]
for p in sorted(glob.glob(root+"/corpus/knowledge/*.md")):
    rl=[l for l in open(p,encoding="utf-8",errors="replace") if l.startswith("recheck:")]
    n+=len(rl); bad+=[os.path.basename(p) for l in rl if not l[len("recheck:"):].strip().startswith(pre)]
print("KNOWLEDGE-RECHECK-LINES total=%d noprefix_any=%d" % (n,len(bad)))' /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Output: `KNOWLEDGE-RECHECK-LINES total=88 noprefix_any=11`, exit 0 (also R10 with the non-first split: `noprefix_nonfirst=0`, `files_with_gt1=0`).

Requested sweep `grep -l 'recheck:' corpus/knowledge/*.md | wc -l` → `88`, exit 0 (R8). Knowledge files: 88 (R7).
`grep -c '^recheck:' corpus/knowledge/*.md | grep -v ':1$'` → no output, exit 1 (R9): every entry has exactly one recheck line.

Round 71 and 72 lessons and verifier spot-checks (R11, R12):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -nE 'recheck' corpus/lessons/round-71.md corpus/lessons/round-71-verifier-spotcheck.md corpus/lessons/round-72.md corpus/lessons/round-72-verifier-spotcheck.md | grep -E '(python3|bash|sh|grep|sha256sum|test|wc|cat|diff) +corpus/' | grep -v 'kasegi-shokunin && '
```

Output: `corpus/lessons/round-71.md:70: ... (N8: python3 corpus/instruments/frontier-recheck-count.py ...` — a prose command, not a recheck field, not a Q10 instance; unchanged. Second sweep `grep -nE 'cwd|foreign|from any|exit 2'` over the same four files: no match, exit 1.

## Census and sources commands, before (round 73)

- Census (claims counter), base replay on committed bytes: `RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0` / `RECHECK-CWD-RESULT nonconformant`, **exit 1** (R1). The receipt `c1-donothing-r73.txt` lines 89–90 print the same counts; its exit is not in the file (the claims state exit 1).
- Census selftest: `selftest cases=1 failures=0`, **exit 0** (R2).
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`, run from the fleet root: `kasegi ok`, **exit 0** (R5). The first attempt from the lane cwd gave `command not found`, exit 127; the script lives at the fleet root. Not a finding about the registry.
- After (landing): not measured. The lane HEAD is `3b53ff83`; `git status` shows only untracked round-73 files, no tracked change (read-only).

## Gate-side and registry counts (before, measured by this seat)

- Knowledge-expected: `lines=90`, `rows=88`; `LC_ALL=C sort -c` exit 0 (R7).
- Frontier registry at base: `registry=107` (`c2-donothing-r73.txt`, L1 receipt; not re-run).
- S108 row: absent from `corpus/SOURCES.md` at draft time.

## Registry changes (old → new, pending landing except where stated)

- S108: none → mined (lands with C2).
- S108 recheck: none → 90d (pending).
- S108 used-by: none → F51 entry path (pending; draft at `.ufo/waves/round-73/w1/draft/F51-entry.md` per the wave spec; final corpus path not named in claims).
- Knowledge-expected: list added; base 90/88 → after pending 91/89.

## Routed defects

Round-72 R-1 to R-7 and L72-2, L72-3, L72-8, L72-11: restated in the draft, open and unchanged. New: R-8 (M73-2: one instrument of record for the foreign-cwd limb; operator decision, next round).

## Process note (order as known; receipts carry no timestamps)

1. Base census and C2 do-nothing counters ran at base `fdf17413`. The L1 states the C1 census ran before freeze `3b53ff83` was written. Neither receipt has a timestamp or an instrument digest, so the wall-clock order against the freeze rests on that statement.
2. Freeze `3b53ff83` (`2026-11-05T04:43:44-03:00`, i.e. `07:43:44Z`) adds `claims.json`, both receipts and `recheck-cwd-census.py` (R13). Its diff against base touches no other knowledge or instrument file.
3. S108 was captured at `07:40:48Z`, about three minutes before the freeze; the capture precedes the frozen C2 target (the reverse of M72-5).
4. The capture is untracked and has no manifest at the freeze (R14).
5. This seat replayed the census using the committed bytes (scratch copy of base, recheck prefix rewritten to the scratch path) and reproduced the receipt counts exactly (R1). The counts do not depend on any census byte that was uncommitted at the base run.
6. The seat brief's premise "no counter reads recheck cwd" was not checked before the claim was frozen; `recheck-audit.py` had a `cwd` limb all along (M73-2).

## Commands run and exits (summary; outputs in the receipts file)

- Reads (`read`): claims.json, round-72 lesson, QUALITY.md, census source, S108 capture, c1 and c2 receipts, wave listing, round-72 and round-71 lesson listings, S108 quote check, `recheck-audit.py` docstring, w1-spec.json excerpts. Read-only.
- `git -C <lane> --no-optional-locks` `log`, `show --stat`, `status --porcelain`, `ls-files`, `cat-file -e`, `rev-parse`, `diff --name-only`, `log --diff-filter=A` per entry, `show -s`: read-only. All exited 0 (the `cat-file -e` check printed `base-present`).
- `git archive fdf17413` and `3b53ff83` into scratch (`tar -x`): read-only on the repo; exit 0.
- Census base replay (R1) exit 1; selftest (R2) exit 0; mutants (R3, `mut1`, `mut2`) selftest exit 1 each.
- `recheck-audit.py --root <base> --foreign / --quiet` (R4) exit 1; `--json` run (R15) exit 1.
- Sweep commands (R8–R12); `sources-census.sh` (R5) exit 0 from the fleet root.
- Receipts run: first pass had two exit-capture defects (R5 printed `EXIT=` blank because of `PIPESTATUS`; R12 printed `head`'s exit). Both blocks were patched in the scratch script (exact-once replace), the file was regenerated, and the file is the re-run output (`RECEIPT_EXIT=0`).
- Draft edits: one `edit` applied to `round-73.md` (M73-2 limb range, R-4 owner). A first attempt was refused because the anchor line had not been read in full; nothing was applied by it.

## Not run

- C1 after-state census (lane not yet repaired) and `recheck-audit.py` after-state.
- C2 counters: `frontier-recheck-count.py`, `capture-binding-check.py`, `entries`, knowledge-expected after, sources-census after. Pending landing.
- Live network access: none (no recheck command reaches a live host; the replay reads committed captures only).

## Installs and tooling

None. No package, tool or runtime was installed or updated; `~/.local/bin` untouched; no pacman transaction. `/home/vgpnk/.omp/agent/RULES.md` was not read because no installation was made.

## Writes

- `.ufo/waves/round-73/w1/draft/round-73.md` (draft lesson).
- `.ufo/waves/round-73/w1/K73ScribeLesson-receipts.txt` (receipts).
- `.ufo/waves/round-73/w1/K73ScribeLesson.md` (this report).
- Scratch under `/fast/scratch/hyaku/kasegi-r73/K73ScribeLesson/` only; removed after the receipts were copied. No git mutation, no lane file edited, no fleet-root file written.

## Findings the L1 must act on before landing

1. Write `corpus/source-snapshots/round-73/manifest.json` (url, fetched_utc) in the landing commit with `S108.txt` (M73-3, R20).
2. Decide the single instrument of record for the foreign-cwd limb (M73-2, R-8). Until decided, the new census and `recheck-audit.py` both report the same ten entries.
3. After the C1 prefix repair, both `recheck-cwd-census.py` (predicate: `noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22`) and `recheck-audit.py` (`cwd_fail=0`, expected by construction, not measured) should read clean on the landed bytes. Measure both there.

## Verdict

Draft lesson complete on the required sections and the requested checks, with two honest corrections recorded (captured-by, duplicate detector) and one pre-landing gap (manifest). Blockers for filing: landing of C1 and C2 and their after-measurements; these are the integrator's, not this seat's.
