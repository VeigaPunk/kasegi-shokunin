# RevC1Selftest — round-36 wave1 receipt (reviewer, depth:verifiability)

Item: run the drafted C1 suite's `--selftest` from scratch and verify (a) >=9 case lines each printing a `selftest case=<name>` verdict line, (b) `failures=0` + exit 0, (c) a summary-only forgery (`cases=0 failures=0`) is rejected — proven by constructing a forgery that prints only the summary.

**Verdict: PASS** — all three criteria hold on the final draft bytes.

## Target binding

Drafted suite by ExecC1SuiteBuild, live at `/fast/scratch/hyaku/kasegi-r36/ExecC1SuiteBuild/r36-closure.sh`. The draft moved during my run (I verified three identities):

| digest | lines | my action |
|---|---|---|
| `ff616adc045a8938c7ca69b3693565ef0f676a0d1d67df293b1b6c4a82da4720` | 737 | intermediate; baseline + green + forgery battery run |
| `76273416f7a6668a702eadf5a6c03b80ae87ad4793f652880303fcb7f8230323` | 817 | declared frozen; full battery re-run (green fixture needed an E3 row-format fix — see discrimination note) |
| `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` | 894 | **FINAL; all findings below bind to this copy** (sha re-verified on my copy before every run; author declared no edits after final) |

`bash -n` exit 0 on all three. The final bytes self-identify: the run/selftest header prints `suite-sha256=4db1ae70…`, so any `closed=9/9` / `cases=9 failures=0` line can be bound to the instrument that produced it.

## (a)+(b) Selftest — 9 case verdict lines, failures=0, exit 0

Green-path invocation, all writes bound under my scratch:

```
bash <copy> --selftest --export-ref 630c272d999dcceac8b4d305b1e0e939e49e44a4 \
  --lane <my-scratch>/fix --work <my-scratch>/w-green4 --scratch-root <my-scratch>/sroot-green4
```

Green tree: a scratch fixture repo (clone of the lane at b47f2cd — full history preserved so E1's `cat-file`/`merge-base` limbs resolve — plus the landings that are still pending at the freeze head, committed in two commits, `git add`/`commit` run only inside the verified-toplevel fixture):
- SKILL.md `## Round-36 Gates & probes registry addition` with registry rows `| r35-defect-closure.sh |` and `| r36-closure.sh |` (exact basenames, first column);
- `.ufo/waves/round-35/wave1-results.json.provenance.md`;
- `corpus/lessons/round-36.md` with M36-1..M36-4, naming the corrected `source-recheck` line;
- `## Round-36 closure` SCORECARD section with `**Final lane commit: 6d98bcf…**` (the landing commit; exists and is ancestor of the exported head `630c272d…`).

Measured output (verbatim counts):

- exactly 9 `selftest case=` lines, each `selftest case=E<i> positive=pass mutants=<ok>/<n> verdict=pass`; mutants 4/4, 3/3, 5/5, 1/1, 1/1, 1/1, 2/2, 4/4, 4/4 — every mutant rejected with a payload naming the reopened limb;
- `selftest cases=9 failures=0`; **exit 0**; `selftest judge=own-report accepted=1`; all four `selftest judge=forged-* rejected=1`;
- header: `selftest export-ref=630c272d… lane=<fixture> suite-sha256=4db1ae70…` and an honest `deviation=non-default --lane` line.

Honest baseline (real lane, author-contract invocation `--export-ref b47f2cd --lane <lane>`): 9 case lines; `selftest cases=9 failures=5` (E1/E3/E4/E8/E9 positives red — exactly the five landings still pending at the freeze head; E1 red because the freeze SCORECARD's `Final lane commit:` lines live in historical round blocks, not a Round-36 section); exit 1; `judge=own-report accepted=0`. The suite does not fake green while the round is unclosed, and the mutant limb stays fully exercised (4/3/5/1/1/1/2/4/4, all rejected) even on a red tree.

## (c) Summary-only forgery rejected — proven by construction

I built the forgeries myself (scratch scripts, exit 0, printing only the summary) and proved rejection three independent ways:

| forged output | my case-line gate (>=9 verdict lines) | extracted `judge_selftest_report` (verbatim from final bytes) |
|---|---|---|
| `selftest cases=0 failures=0` only (the item's forgery) | 0 case lines → REJECT | VERDICT=rejected |
| bare `selftest cases=9 failures=0` (bolder lie) | 0 case lines → REJECT | VERDICT=rejected |
| 8 pass-case lines + green summary (short) | 8 → REJECT | VERDICT=rejected |
| 9 lines, duplicate E1, E9 missing | 9 but ids broken → REJECT | VERDICT=rejected |
| 9 × `mutants=0/0 verdict=pass`, no detail lines | shape-complete → checked | VERDICT=rejected |
| control: real green-v4 report | 9 pass lines → PASS | VERDICT=accepted |

The judge's acceptance predicate (read from the final bytes): exactly 9 `^selftest case=` lines, all 9 `verdict=pass`, exactly one `selftest cases=9 failures=0` summary, all nine distinct ids present, and (new in final) each case's `mutants=ok/n` cross-checked against `selftest detail=E<i> mutant=` lines. The suite's own green run independently prints `forged-summary / forged-caselines / forged-failed-cases / forged-detail-free` all `rejected=1`, agreeing with my extracted-judge results.

## Discrimination evidence (observed, not injected)

- My first green fixture used path-prefixed registry cells (`| \`corpus/instruments/r36-closure.sh\` |`): E3 read `registry-r36-closure=0` and failed; after reformatting to exact basenames it passed. The section-scoped exact-basename clause rejects mentions/prefixed cells, closing round-35's "grep satisfied by a mention" defect class.
- At the final digest the baseline E1 is red on b47f2cd purely because the bound hashes sit in historical round blocks — a history-only closure no longer satisfies E1.

## Process notes

- Tooling installed: none (none needed).
- Writes: my scratch dir only, plus this receipt. Lane repo untouched (read-only git: log/show/ls-tree/ls-files/status/rev-parse; `git clone --no-hardlinks` read the lane source; all fixture commits inside a toplevel-verified scratch clone).
- One reviewer-harness artifact, diagnosed and fixed: my first direct-judge test rejected the real green report because I had extracted `CHECK_IDS` by line number from a draft the author then overwrote (the line had become a comment, leaving the ids unset). Redone from an immutable copy by pattern. Not a suite defect.
- Provenance: the author's published receipt was briefly stale (pinned ff616adc while the frozen bytes were 76273416); I flagged it and the author updated it to pin 4db1ae70 with verbatim text ("no edits after this message"). My copy's sha was re-checked against the live file immediately before the final battery.

## Residual risk / gaps

- The frozen claim binds `cases=9 failures=0` to the **round-36 final lane head**. I proved the green path on a scratch fixture (freeze tree + shape-compatible landings), because the final head does not exist at seat time. The integrator must re-run `--selftest --export-ref <final-head>` on the landed tree; my fixture landings are stand-ins, not the real content (the real round-36 lesson, registry rows and bound Final-lane-commit hash must be the L1's).
- `closed=0/9` on r35 base 3266c993 and `<9/9` on r35 judged head 0aee0ef are other seats' items; I did not re-measure them (the author reports 0/9 and 3/9 at the final digest).
- The suite's E4 index limb reads the `--lane` repo's index; in my green run that is the fixture's index. On the real lane post-integration (everything committed) the limb reads the lane's own index — consistent, but the integrator run is the binding measurement.

Report: .ufo/waves/round-36/wave1/RevC1Selftest.md
