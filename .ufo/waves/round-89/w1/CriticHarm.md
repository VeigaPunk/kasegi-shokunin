# CriticHarm — round 89 harm check (whole round so far)

Seat: CriticHarm (leaf, read-only). Base `090a46f8`, freeze `94573d25`, C1 landing `eb5f0df8`, C2 landing `c61c5586`, master read at `50e2632e`. Every number below is from a command in `CriticHarm-receipts/`; no claim is re-scored and no lane file is edited.

## Verdicts (axis / owned surface)

| surface | verdict | evidence |
|---|---|---|
| depth:verifiability — C1 repoint + meter | **NO HARM** | meter at the C1 landing: `777/1798 -> 785/1797`, M1–M9 pass, pins M6/M7 match; do-nothing (`--after-rev` = base) fails M1/M2/M3 (`receipts/c1-meter.txt`). The 5 re-anchors land on the gate text the review named (claim-gates.md:35 decision-digest regex, :36-37 three-way binding, :78-80 not-claimable heuristics, :81-85 prior-submission guard; claim-package-contract.md:52-53 hard gates); the 4 prefix repoints only qualify a path and keep the cited span; `git diff --numstat` is 9/9, so no line shifted inside `triage-thresholds.md` and no external `triage-thresholds.md:NN` citation breaks |
| coverage — C2 landing (scanner) | **NO HARM on the bytes; the counter under-binds the statement (F2)** | master scanner @ master `scanned=1530 hits=0 allowed=20`; @ base tree `hits=0 allowed=18 unused_allow=2` (no retroactive false positive on any committed capture); base scanner @ master misses both new shapes (K6 direction); pathological 166 KB query line scans in 0.19 s (no backtracking); r89 counter at master K1–K8 pass with the row's pins (seed 808664095) |
| depth:density — SKILL.md | **NO HARM** | `SKILL.md` is byte-identical base↔master (`7d082bfe…`); `density.py SKILL.md --label x` mean dens 273.2, 932 instances / 38 blocks |
| instruments (selftests, recheck, census) | **NO HARM** | `capture-secret-scan.py --selftest` pass cases=43; `claim-package-check.py --selftest` 10/10; `source-recheck.py` round-89 and round-88 manifests rc 0 (6 and 6 `OK` lines); `sources-census.sh validate` `kasegi ok` |
| SCORECARD r87/r88 commands in the capture-secret-scan row | **NO HARM** | both still pass at master unchanged: r87 K1–K5 `pass`, r88 K1–K6 `pass` (`receipts/counters-at-master.txt`); neither pins the instrument, so the r89 change does not invalidate them. The row's r89 command also passes with its `--instrument-sha256`/`--gate-sha256` |
| scope / deletions | **NO HARM** | `git diff --name-only --diff-filter=D base master` is empty; freeze→C1 = `{triage-thresholds.md}`, C1→C2 = `{SCORECARD.md, capture-secret-scan.py, capture-secret-allow.tsv}` exactly as claimed |
| provenance pins | **NO HARM** | all 15 `claims.json` instrument pins re-hash equal at master (bad=0), including the two snapshots and the r88 review used by `labels.tsv` |
| credential hygiene of `w1/` | **NO HARM** | master scanner `--files` over the current `w1/` tree: `hits=0` (34 files at check time); no scanner/counter/`S<digits>.txt` copy in `w1/` |

## F1 — HARM (depth:verifiability; routed defect): the C2 landing falsifies the knowledge entry that specifies the scanner

`corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` is unchanged since base and still says what the base instrument did:

- `:78` — "**Named limits**, verbatim from `corpus/instruments/capture-secret-scan.py:43-45`: … CloudFront `Signature=`/`Key-Pair-Id=` URLs … are not detected." At master, `:43-45` is the new round-89 `\u0026` paragraph, and the docstring's limits (`:61-65`) no longer list CloudFront URLs (only signed cookies). The statement is false at master: `SCORECARD.md:307` claims the class and the scanner detects it.
- `:213` (rejected over-generalization 3) repeats the same false sentence.
- `:86` — states the round-88 `\u0026` left-boundary limit as current; master's `_LB` (`capture-secret-scan.py:103`) admits a start after `\u0026`/`%26`, i.e. exactly the limit the entry says holds.
- Eight line citations that were correct at base now point at unrelated lines: `:49`→`:81`,`:86-87` (now report text and imports; base: `_SIG` and the azure regex), `:78`/`:107`/`:213`/`:221`→`:43-45`, `:212`/`:225`→`:84-87`, `:82`→`:242`, `:83`→`:235`, `:222`→`:233-240`, `:65`→`:1-62` (docstring now ends at 83). Base-vs-master line table: `receipts/knowledge-drift.txt`.
- The entry's own checks no longer reproduce: FC-5 records instrument `d7349536…`, master is `95f24a54…`; FC-3 records `unused_allow=17`, master prints 19 (allowlist data rows 17→19, which is correct).

Impact: the lane's only knowledge authority on cloud signed URLs contradicts the landed instrument on two statements and eight anchors; a reader using the entry would treat CloudFront URLs as uncovered and mis-locate the azure pattern. This is a *consequence* of the C2 landing (the claim's P3 confines the diff to three files, so the repair cannot be in C2) — a routed defect, not a predicate failure.

Smallest safe correction: integrate the already-drafted `w1/ScribeEntry-candidate/cloud-signed-url-credentials-in-captured-evidence.md`. I checked it against master: all 30 instrument citations point where it says (`:99` `_SEP`, `:100` `_PARAM`, `:101` `_SIG`, `:103` `_LB`, `:104` `_CF_LB`, `:106-107` `_CF_SIG`/`_CF_KPI`, `:116`/`:117` constants, `:263`/`:270`/`:272`-`:281` selftest cases), its CloudFront quotes verify verbatim at S128:56-59, 94-95, 206-211 and S130:66, 70-71, 77-78, 163, and its `unused_allow=19` note matches the row count. Integration must land it in the same commit stream; otherwise master keeps a falsified entry on the axis the round claims to improve. If integration declines it, the alternative smallest repair is a one-paragraph deprecation note in that entry pointing at `SCORECARD.md:307` and the new docstring — but the candidate is cheaper and already verified.

Related, same commit: flip S128/S130 in `corpus/SOURCES.md` from `queued`/used-by `—` to `mined`/used-by `corpus/instruments/capture-secret-scan.py` (the lesson's Gate section commits exactly this "at integration"). At master the registry contradicts the lesson and the protocol's `mined` ⇔ used-by invariant; that is a pending integration step, not new harm — but it is *only* harmless if it lands.

## F2 — HARM (coverage / verifiability of the frozen counter; routed defect): three statement details are unbound — a mutation survives K1–K8

The frozen C2 statement names, besides the shapes: `%26` as a separator for `azure-sas-signature`; `Key-Pair-Id=<8-32 upper-case alnum>`; "up to 20 other parameters between". `claims.json` says K8 "maps every statement clause to a plant". None of the three is planted:

- K8 `CLAUSES` has 10 entries, none for `%26`, none for the key-id width, none for the parameter window;
- K4 `PLANTS` has no `%26` case, no out-of-width `Key-Pair-Id`, no >20-parameter case;
- K7 `generated()` uses only `&` and `\u0026`, a 13-21-char key id and 0-4 leading parameters;
- the scanner selftest has no `%26` case, no key-id-width case, no window case.

Executed mutants (scratch clones, commits only inside the clone, toplevel asserted; `receipts/mutations.txt`):

1. `_LB` with `(?<=%26)` deleted — counter (no pins) `CAPABILITY-CHECK-RESULT pass rc=0`, K1/K4/K7/K8 all pass, fresh seed. The mutant is behaviourally different: on a scratch query whose `sv=` starts right after `%26`, master prints `hits=1`, the mutant `hits=0`. The `%26` half of the frozen clause can therefore regress with every limb green.
2. `_CF_PARAM` window `{0,20}→{0,40}` and `_CF_KPI` width `{8,32}→{1,64}` — counter pass rc=0, fresh seed 342995815.

So K8's "every statement clause" assertion is false for three spec details, and this is the same class as the r88 lesson **M88-2** that C2 claims to close ("K8 maps every statement clause to a plant"). It does not falsify P1 — the counter does pass at the landing, and the pin catches any byte change outside a pin update — but the pin only protects the landing bytes, not the clause: a later refactor that updates the pin and drops `%26` passes everything.

Impact: coverage (the counter's discriminating power is narrower than the claim says) and depth:verifiability (a stated closure that did not happen). Smallest safe correction, in a later commit (the counter is frozen): add three plants to K4 and three `CLAUSES` entries — a `%26`-start azure case whose span crosses `&`, a 7-char and a 33-char `Key-Pair-Id` (expected miss), and a 21-intervening-parameter case (expected miss) — plus the two scanner selftest cases; or, if the lane prefers, narrow the statement and K8's note to what is planted and keep the three as named limits. Do not re-freeze this round.

## Qualifiers (not harm)

1. **`%26` spans, not just starts.** `_SEP` is `&`/`&amp;`/`\u0026` (instrument `:99`), so a query whose parameters are *joined* by `%26` is not spanned past the first matched parameter; "in any parameter position" in the statement holds only for `\u0026`-joined queries. Corroborates ExecC2Corpus FN-3 and is part of F2's missing plant; wording, not behaviour, is the cheapest fix.
2. **Fixture literals in the frozen `c2/` files.** `--files` on the 24 tracked round-89 wave files prints 7 HITs (2 files: the candidate scanner and the C2 counter). This is the lane's pre-existing pattern — the r87 counter prints 4 and the r88 counter+candidate print 7 — because a behavioural counter must carry fake shapes, and the instrument skips only its own canonical path. Both paths are outside `--rev` scope and outside `w1/`, so no commit is blocked and the round adds no new class of exposure; recorded only so the L1 does not read the 7 lines as a new leak.
3. **SOURCES status flip** (see F1) and **the two new allowlist rows** are correct as landed: the matched bytes are identical (same digest) at two paths, both consumed (`allowed=20 unused_allow=0` at master), and neither row is for a session token.
4. **The r88 knowledge entry's `:37-38` citation into the allowlist section was already wrong at base** (base `:37-38` is azure shape text; the "Rows for aws-sts-session-token are refused" sentence is at base `:53`). Pre-existing r88 drift, not this round; not counted in F1.

## Counterexample tested (strongest available)

A committed knowledge entry that **contradicts the landed instrument** is worse than a stale comment: the entry is the artifact a later round reads before changing the scanner, and it says the class the SCORECARD claims does not exist. Second-strongest: the frozen counter cannot see the `%26`/width/window half of its own statement — the exact failure mode (M88-2) the round says it closed. Neither falsifies a predicate; both are routed defects with re-runnable commands in the receipts.

## Files written

- `.ufo/waves/round-89/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-89/w1/CriticHarm-receipts/surfaces.txt`
- `.ufo/waves/round-89/w1/CriticHarm-receipts/counters-at-master.txt`
- `.ufo/waves/round-89/w1/CriticHarm-receipts/c1-meter.txt`
- `.ufo/waves/round-89/w1/CriticHarm-receipts/scanner-matrix.txt`
- `.ufo/waves/round-89/w1/CriticHarm-receipts/knowledge-drift.txt`
- `.ufo/waves/round-89/w1/CriticHarm-receipts/mutations.txt`

Scratch `/fast/scratch/hyaku/kasegi-r89/CriticHarm/` held the two throwaway clones (commits made only inside them, after `git rev-parse --show-toplevel` matched), the archived base tree and the fixtures; it is deleted before yield. No credential-shaped value is in this report or the receipts (scanner summary lines and digests only). No tool installed or upgraded; no pacman transaction; read-only git/jj elsewhere.
