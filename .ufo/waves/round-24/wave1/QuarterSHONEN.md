# QuarterSHONEN — SHONEN.md calibration audit (round 24, read-only)

Target: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md`
(sha256 `890223902c4c771a60ef454e8ccbe16546e88d5580cf0b3349036bda05025e18`, `git status --porcelain -- SHONEN.md` empty — not edited).
Lane state at audit: `git -C … rev-parse master` = `c2480b143120364728b40397926ffcf30a7309c8`; working tree carries L1's in-flight
`M corpus/instruments/resolve.py` + untracked `capture-source.py`, `resolve-dispatch-check.py`, `resolve-dispatch-fixtures.json`,
`corpus/source-snapshots/round-24/` — none touched by this seat except as disclosed in **Incident**.

Tags: `[verified]` = the box's assertion holds against bytes today; `[stale]` = assertion falsified by today's state;
`[unverifiable]` = the evidence the assertion needs is absent from the repo/host, so it cannot be scored either way.

## Verdict table

| # | Box assertion | Tag | One-line reason |
|---|---|---|---|
| 1 | SKILL.md contains real decision tables, error patterns, checklists, cited sources | **[verified]** | 2 named decision tables, defect-class + anti-pattern tables, 7 checklist boxes, 10 distinct SOURCE ids all present with URLs. Two qualifiers: one table is render-broken, and 5/8 frontier citations are not re-derivable from committed captures. |
| 2 | At least one end-to-end domain task executed and logged in LOG.md | **[stale]** | 27 LOG entries; none describes executing a bounty-domain work item. LOG itself records `no_submission_performed` as the norm and one ledger claim as `[INFERENCE, never executed]`. |
| 3 | Instructions executable by an agent without oral context | **[unverifiable]** (half verified) | The lane's own instrument invocations run cold and deterministically from a clean `git archive master` (5/5, exit 0). The domain pipeline they describe names 14 `ops/*` executables, all absent — root loss, not a doc defect. One new reproducible footgun found in `resolve.py`. |
| 4 | No cross-domain bleed (PROVINCE.md still accurate) | **[verified]** today | 8 README frontier rows, 8 admitted, matching `PROVINCE.md:38` "F01–F08"; three absent roots match its annotations; 4 adjacent lanes exist; 1 sibling-lane mention in all of `corpus/`+`SKILL.md` and it is a non-duplication disclaimer. **Expires when C2 admits F09.** |

## Box 1 — [verified], with two qualifiers

Commands and output:

```
$ grep -c '^|' /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md
76
$ grep -n 'decision table' …/SKILL.md
134:## Finding-triage decision table
1014:## Frontier decision table (round 22)
```

- Decision tables: `SKILL.md:134` (7 terminal classes with package-state + evidence per row), `SKILL.md:1014` (5 frontier situations with rule/entry/source). Both carry per-row file:line or `S###` evidence.
- Error patterns: `SKILL.md:565` "Disclosure anti-patterns (all observed in fleet wrap review)" and `SKILL.md:680` "Claim-hardening wave — the defect layer above the gates" (10-row class/signature/fix table).
- Checklists: 7 boxes at `SKILL.md:60,63,67,72,76,80,87` (program-rule snapshot checklist). All are `[ ]` templates — the box asserts the checklist exists, which it does; it does not claim they are completed.
- Cited sources: `grep -oE 'S[0-9]{3}' SKILL.md | sort -u` → S001,S002,S003,S005,S006,S008,S009,S012,S013,S015 (10). All 10 exist as rows in `corpus/SOURCES.md` (31 rows), and each row carries an `http` URL (per-id `grep -m1 -E "^\| *$id " corpus/SOURCES.md | grep -q http` → URL-OK ×10).

Qualifier A — **render defect in the primary decision table.** `SKILL.md:139-143`: header `:139`, separator `:140`, one row `:141`, blank `:142`, remaining six rows `:143-148`. Under GFM only header+1 row render as a table; the other six render as prose. Detector: scan for `blank line inside header+separator table` → `(139, 142, 143)`. The table is real as source text, broken as instruction.

Qualifier B — **"cited sources" is existential, not re-derivable.** From a clean copy (`git archive master | tar -x -C /tmp/kasegi-shonen`):

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json
… 24 assertions OK … rc=0
$ r=$(grep -m1 '^recheck: ' corpus/knowledge/cvss-v4-severity-and-vector.md | sed 's/^recheck: //'); bash -c "$r"
S001:source UNAVAILABLE reason=not-listed
rc=2
```

The round-23 manifest lists S018/S029/S030/S031 only; F01–F05's rows exist in `corpus/SOURCES.md` but their bytes are not in the repo (this is the frozen C1 counter-A before-state, 3/8). Box 1 asks only that sources be cited, so it holds — but no reader can re-derive five of the eight frontier entries from committed bytes.

## Box 2 — [stale]

- `LOG.md` holds 27 dated entries (`grep -c '^- 2026-\|^## ' LOG.md` = 27). Reading every entry: rounds 1–19 census/read the lost tree, rounds 20–23 build instruments and admit sources. No entry records executing a domain work item (scope → triage → claim package).
- `LOG.md:147`: "… `no_submission_performed` is the norm" — describing the lost fleet's DONE packages, not this lane's output.
- `LOG.md:622`: a ledger claim marked `[INFERENCE, never executed]`.
- `LOG.md:1044`: "no verdicts, no numbers, no round executed" (SCORECARD scaffold round).
- Nearest domain artifact, `corpus/knowledge/claim-anatomy-sample.md:1-12`, is a 20/280 `status.json` sampling census. Its selection script is `/tmp/kasegi-r14/select20.sh` — outside the repo and gone — so even the sampling is no longer reproducible, and sampling status files is not an end-to-end task.
- Prior grading agrees: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/reports/round-21/kasegi.md:176` marks this box `[ ]` with "a resolver fixture is not execution of a bounty-domain work item".

This is not closable by documentation: with all three roots absent (`ls -d ~/Projects/bounties ~/Projects/the-bounty-hunter ~/Projects/origin-work` → three "No such file or directory") and the operator re-scope still open (`.ufo/l0-questions.md:10`, kasegi round-15 row, unanswered), the box cannot be cleared from inside this lane this round. It should be reported `[ ]`, not `[~]`.

## Box 3 — [unverifiable] as written; half verified with a named break

Verified half — the lane's own documented invocations (the `run` column of `corpus/instruments/README.md:9-13`) execute cold, from a clean `git archive master` copy, with no oral context:

| command (cwd = copy root) | result |
|---|---|
| `python3 corpus/instruments/density.py SKILL.md --label X` | mean dens **154.0**, "Total path-citation instances: 652 across 19 blocks", rc 0 |
| `python3 corpus/instruments/resolve.py /tmp/kasegi-shonen` | `distinct=1669 resolves=14 mirror=0 internal=216 other=0 gone=1439 skill=39/513 corpus=215/1344 all=230/1669`, rc 0; two consecutive runs → identical `md5 0e42a403eec32b4cc7e2bf51197df930` (deterministic) |
| `python3 corpus/instruments/anchorcheck.py SKILL.md` | rc 0, `LOST-RECORDED` rows only |
| `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json` | 24 `OK`, rc 0 |
| `python3 corpus/instruments/source-recheck.py --selftest` | `manifest:selection UNAVAILABLE reason=selftest-takes-no-manifest-or-source`, rc 0 |

Lane-local pointer closure: every backticked `corpus/…`/`plans/…`/`considerthese/…`/`SCORECARD.md` token in `SKILL.md` resolves (37/37); the only 9 unresolved lane-local tokens are `~/Projects/bounties`-rooted `.ufo*` paths, i.e. lost-tree surface.

Unverifiable half — the instructions that describe the domain pipeline name 14 distinct executables (`grep -oE '`?(ops|bounty-map|bin)/[A-Za-z0-9.*-]+\.(mjs|sh|py)`?' SKILL.md`): `ops/{claim-check,claim-index,prepare-claims,ev-report,fleet-dispatch,park-disposition,rank,registry-check,reroute-drill,check-freshness,validate,shared,import-board,finalize-all}.mjs` + `ops/sighting*.sh`. Every probed path is ABSENT (`ops/claim-check.mjs`, `ops/rank.mjs`, `ops/ev-report.mjs`, `ops/fleet-dispatch.mjs`, `ops/park-disposition.mjs`, `ops/check-freshness.mjs` all "No such file or directory"). Round-9 precedent graded exactly this situation "provisional / could-not-evaluate" (`corpus/lessons/round-9-aggregator-corpus-verdict.md:20-24`), and the earlier cold run graded it `[~] partial` for documented-vs-live mismatches (`corpus/lessons/round-8-aggregator-box3-coldrun.md:54`).

Named break (new, reproducible) — `resolve.py` accepts any `argv[1]` as the lane root and overwrites the census of record:

```
$ python3 corpus/instruments/resolve.py --help
distinct=0 resolves=0 … all=0/0
wrote …/corpus/instruments/citation-survival.tsv
wrote …/corpus/instruments/citation-survival.md
rc=0
```

`--help` was taken as a root: the generated md recorded `Lane root: …/--help` and `Scope: … (0 files)`, the tsv was truncated to its header. `anchorcheck.py --help` and `density.py --help` raise tracebacks instead (both then exit non-zero on the argparse path). A cold agent following intuition, not the README `run` column, destroys the census of record. Fix belongs in `resolve.py`: reject a non-directory argv with a `usage:` line, and never write when the file set is empty. (Corroborates C1's dispatch-liveness item; this is a different axis of the same script.)

Second minor break — recheck commands are cwd-dependent. `corpus/knowledge/cvss-v4-severity-and-vector.md` `recheck:` is `python3 corpus/instruments/source-recheck.py …` (relative), while `multiparty-vulnerability-coordination.md` uses `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`. A cold agent in any other cwd gets exit 2 for a reason unrelated to the citation it is checking.

## Box 4 — [verified] today, two calibration caveats

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
8
$ grep -n 'Frontier' PROVINCE.md
35:## Frontier
38:under Frontier F01–F08.
$ ls -d ~/Projects/bounties ~/Projects/the-bounty-hunter ~/Projects/origin-work
… three × "No such file or directory"
$ ls -d ../chousa-shokunin ../kagi-shokunin ../kake-shokunin ../kengaku-shokunin
all four present
$ grep -rniE 'kengaku|chousa|kagi-shokunin|kake-shokunin' corpus/ SKILL.md
corpus/QUALITY.md:8:the research method is chousa's — this file duplicates neither.
```

Every PROVINCE assertion holds against today's bytes: 8 frontier rows / 8 admitted = "F01–F08"; the three roots are absent exactly as its round-15/round-19 annotations say; the four adjacent lanes exist; the sole sibling-lane mention is a non-duplication disclaimer, so no bleed. `corpus/knowledge/` holds 33 files, all inside the bounty/security-research domain or its ops layer.

Caveat 1 — **expiry inside this round.** C2 admits F09. `PROVINCE.md:38` hardcodes "F01–F08" and `PROVINCE.md` was last committed at `c8b719d` (2026-10-19); the F09 admission will falsify box 4 the moment C2 lands unless PROVINCE is edited in the same commit. Recommend the line become "under Frontier (see corpus/README.md; 9 admitted at r24)" or a pointer with no count.

Caveat 2 — **the line has a history of being true by arithmetic only.** At `c8b719d` PROVINCE already said "F01–F08" while `git show c8b719d:corpus/README.md` had F01–F05 admitted and F06–F08 **queued**. The sentence "General practice that governs every program is indexed" was then false for three of the eight rows. Any future check must count the **admitted** column, not the row count — which is what C2's counter A already does.

## Incident — census-of-record overwritten and restored (disclosed, not silent)

- What happened: the box-3 probe `python3 corpus/instruments/resolve.py --help` ran against the live lane. The script ignores unknown flags and wrote `corpus/instruments/citation-survival.md` + `.tsv` with a 0-row census (`git diff --stat` showed `citation-survival.tsv | 1480 --------`).
- Was it mine: both files' mtimes were `2026-10-25 04:14:44 -0300`, the second of my probe run; the working tree had no prior modification of those two paths.
- Restore: `git show master:corpus/instruments/citation-survival.tsv > corpus/instruments/citation-survival.tsv` and the same for `.md` (no `checkout`, no index/commit operation). Post-restore `sha256sum` = `793e0a4e456b0863cd4172dad3563de3cb4e26d3f941efc9658d3014901f1044` (tsv) and `795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d` (md), byte-identical to `git show master:… | sha256sum`. Both paths are gone from `git status --porcelain -- corpus/instruments/`.
- Exposure window: ~2 minutes (04:14:44 → restore). Any seat that read `citation-survival.md` in that window saw a 0-row census with `Lane root: /…/--help`. Everything else in my audit ran against `/tmp/kasegi-shonen` (`git archive master` copy) for this reason.
- Not mine, left alone: `M corpus/instruments/resolve.py`, untracked `capture-source.py`, `resolve-dispatch-check.py`, `resolve-dispatch-fixtures.json`, `corpus/source-snapshots/round-24/` (L1's in-flight C1 work, mtimes 04:14:11–04:15).

## Calibration axis — what these four boxes actually measure

- The checklist has no arming rule: it is a promotion gate whose boxes are checked by the lane's own SHONEN section each round (`templates/round-prompt.md:118-120`: `[x]` needs a named non-author verifier, `[~]` a resolvable pointer, `[ ]` untouched). Since no non-author verifier has ever been named for kasegi, `[x]` has never been available — so the checklist can only ever report partial. That is a property of the gate, not of the lane, and it should be stated in the round report rather than re-derived each round.
- Box 2 is the only box that can never be satisfied while the province has no live surface, and the reason is already filed as an open operator question (`.ufo/l0-questions.md:10`). Two rounds have now graded it `[ ]` for the same reason; recording it as `[~]` with a fixture pointer would be the calibration error.
- Boxes 1 and 4 are cheap to falsify and were both falsifiable today: box 1's table-render break and box 4's hardcoded frontier count are exactly the kind of drift a per-round mechanical check catches. Box 4's check command already exists (C2 counter A) — reuse it instead of re-reading PROVINCE by eye.

## Remaining unknowns

- Whether `corpus/instruments/density.py`'s 154.0 mean and `resolve.py`'s 230/1669 are *comparable* to the last recorded pair (SCORECARD r18/r19 recorded 46.12 % → 6.32 % SKILL under the r18 definition, vs 39/513 = 7.60 % from committed master today): the definition is the same but `resolve.py` is being edited in the working tree right now, so a today-vs-r18 delta is not attributable to content. UNVERIFIED — blocked by the in-flight `M resolve.py`.
- Whether the domain pipeline can be re-executed at all without operator re-scope. UNVERIFIED — blocked by the three absent roots and the unanswered L0 row.
- Whether `capture-source.py`'s S001–S015 captures (untracked, `corpus/source-snapshots/round-24/`) will make F01–F05 rechecks exit 0. Out of scope for this seat; C1's counter owns it.
