# Round 74 attempt 1 — CriticClaims (falsification of the frozen claims)

Seat: CriticClaims (leaf critic, read-only). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Freeze: 847b53792d2d29d161cad7d21a33c89df9e52e8d. Controls: 654d877f0bd4005fd139c46e5b889f4c1833ddda. Base: ccd6a54bf392922495c4860332665499582e3213.
State observed: HEAD = freeze commit (no implementation commit yet). No lane file was written by this seat. No live HTTP, no credentials, no packages installed.

## Verdicts

| Claim | Verdict | Named clause(s) |
|---|---|---|
| C1 recheck-cwd counter amendment (depth:verifiability 4) | **FALSIFIED** on the scope sentence `restoration-recheck: ... is out of the counted population by definition`; **WEAKENED** on `after_predicate.selftest` (a printed stub satisfies it), on `kill_rule (a)` (no frozen executor), and on the `tmpdir-parent` case (not observable by the frozen wording). | scope; after_predicate.selftest; kill_rule (a); selftest tmpdir-parent |
| C2 F52 Fuzzilli admission on S109 (coverage 8) | **WEAKENED** on `after_predicate.capture` ("each <=25 words, each located at its anchor line") and on `after_predicate.registry` ("every pre-existing row ... unchanged", "exactly one new row") because no frozen command measures them; numeric after-values are reachable by a hollow admission. Content loci all HOLD. | capture; registry; do_nothing reachability |

Axes: C1 is nominal under QUALITY R58 (see (e)); C2 is coverage, delta 0.

## Per-claim findings

### (1) Inputs read
- `.ufo/waves/round-74/claims.json` read in full (C2 target line 37 read raw). Predicates, kill rules, scope and non-claim lists quoted below as frozen.
- `.ufo/waves/round-74/controls/` read in full: `c1-base-census-r74.txt`, `c1-redbefore-mutant-survival-r74.txt`, `c2-base-counters-r74.txt`, `census-before-r74.txt`, `freeze-check-replay-r74.txt`.

### (a) Causal separability — HOLDS (with one overstated note)
- C1 bytes: `corpus/instruments/recheck-cwd-census.py` only.
- C2 bytes: new `corpus/source-snapshots/round-74/manifest.json`, new `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`, `corpus/SOURCES.md` (row S109), `corpus/README.md` (F52 row), `corpus/instruments/knowledge-expected.txt`. C2 does not require the counter to change; its recheck is measured by running the entry's own recheck from a foreign cwd.
- Coupling: C2's new entry enters C1's census population. The C1 census clause is shape-bound: claims.json line 24 reads "the printed entries equals ls corpus/knowledge/*.md | wc -l at that revision". That survives 89 -> 90 entries. Verified below.
- Overstatement: claims.json `notes[2]` says C2's landing "cannot falsify it". It can falsify the zero-clauses (`noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0`) if C2's entry is nonconformant. C2's own predicate (`recheck carries the lane-root cd prefix`, exit 0 from foreign cwd) is what prevents that. The shape binding holds; the note should say so.
- Measured: `python3 corpus/instruments/recheck-cwd-census.py --root <L> --lane <L>` -> `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, exit 0. Matches c1-base-census-r74.txt exactly. `ls corpus/knowledge/*.md | wc -l` = 89 (exit 0).

### (b) Do-nothing reachability — WEAKENED (C1), WEAKENED (C2)
C1:
- The unamended counter cannot reach `cases=5`: `python3 corpus/instruments/recheck-cwd-census.py --selftest` -> `selftest case=prefix-census ok ...`, `selftest cases=1 failures=0`, exit 0. Confirms the do-nothing receipt.
- A printed stub can satisfy the after-value. I built `STUB.py` in scratch: `selftest()` replaced by `print("selftest cases=5 failures=0"); return 0`, everything else unchanged. Measured: `--selftest` -> `selftest cases=5 failures=0`, exit 0; `--root L --lane L` -> the same census lines as above, `RECHECK-CWD-RESULT conformant`, exit 0. So the stub meets `after_predicate.selftest` (literal line + exit 0), `after_predicate.census` and `after_predicate.parity` simultaneously. Only kill rule (a) discriminates it, and kill rule (a) names no command or receipt path (see (c)).
- The frozen after-predicate also does not require the printed `selftest cases=5` to come from running the five cases. That is the weakening.
- Smallest safe correction (for the L1 to decide, not a rewording here): the amendment receipt must include the verbatim output and exit of the mutant battery run on the amended file, and the battery command must be named. `.ufo/waves/round-73/w1/K73MutateCounter-run.sh` exists (mode 755, 04:50) and is the natural runner.

C2:
- No-work tree reads (measured): `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108`, `entries=54 pass=54 exit=0`; registry grep = 108; knowledge = 89; knowledge-expected = 91 lines / 89 non-comment rows, sort-clean (`LC_ALL=C sort -c`, exit 0), set-equal to `ls corpus/knowledge/*.md` (`cmp`, exit 0). S109 and F52 absent (`grep -c`, exit 1 for the F52/S109 probes).
- A hollow admission reaches every numeric after-value without content: one knowledge entry with `recheck: cd <lane> && true`, a manifest of 10 quotes that exist in S109 at arbitrary anchors, and one registry row and one README row. The manifest check (see (c)) accepts wrong anchors and 40-word quotes (measured below). Count after-values cannot distinguish this from a real admission. Content is verified only by a reader; the frozen kill clause `if any content clause is contradicted by the capture` names no instrument. [INFERENCE: constructed from measured instrument behaviour; the hollow entry itself was not built in the lane.]

### (c) Universal-clause scan (fleet lesson §9) — WEAKENED (C1), WEAKENED (C2)
Command used for the scan: a Python walk over claims.json for `all|every|always|any|each|exactly|no|never` (exit 0). Hits and verdicts:

- C1 `selftest` "the five cases are exactly: ..." — enumerated, OK.
- C1 `selftest` "tmpdir-parent (every scratch directory the census creates resolves under TMPDIR)" — **WEAKENED**. Measured: with the M5 mutant (`dir="/tmp"` in run_foreign's mkdtemp), census output is identical to the base and nothing survives in TMPDIR or `/tmp/recheck-cwd-*` after the run (scratch is removed in `finally`). Command: M5 run with TMPDIR=<fixture>/tmp, exit 1 (same as base), `leftover-in-TMPDIR=0`, `leftover-in-/tmp=0`. So a leftover-check or output-check cannot observe the parent directory; only an in-process spy on `tempfile.mkdtemp` can. The frozen wording does not say how it is observed.
- C1 `selftest` "no scratch directory survives census()" — OK. Measured: M6 (`rmtree` removed) leaves `leftover-in-TMPDIR=2`.
- C1 `kill_rule` "ANY of: (a) any of the four mutant classes (M4..M7)" — enumerated set, consistent with `K73MutateCounter.md` rows M4..M7 (RC-1 = M4, RC-2 = M5+M6, RC-3 = M7). But the frozen text names no command that applies the four mutants to the amended file. **WEAKENED** (see (b)).
- C1 `kill_rule (d)` "adds a bash -c call site beyond run_foreign's single call ... checked by grep receipt" — the grep is not named. Baseline measured: `grep -n 'bash' corpus/instruments/recheck-cwd-census.py` -> exactly one code call (line 51, `subprocess.run(["bash", "-c", value], ...)`), plus the docstring mention on line 9. Baseline is 1 call; the check itself is unnamed.
- C1 `do_nothing_control` "all four mutants survive it" — verified (below).
- C2 `distinctness_screen.pre_freeze_quote_locus` "every content clause above is located" — verified (below), all HOLD.
- C2 `registry` "exactly one new SOURCES.md registry row" and "every pre-existing row's id/url/status/recheck/used-by cells unchanged" — **WEAKENED**: no command is named that compares rows. The count `grep -cE` = 109 measures only the count. A check must diff the pre-existing rows (e.g. `git diff ccd6a54 -- corpus/SOURCES.md` restricted to removed lines); none is frozen.
- C2 `capture` "each <=25 words, each located at its anchor line" — **WEAKENED**. Measured with `python3 corpus/instruments/source-recheck.py --manifest fx/manifest.json` on a scratch manifest (sha256 of S109 = c9a7adfb...568d486; copy of the lane capture), exit 0:
  - `U1-wrong-anchor` (anchor=1, quote from L151 at anchor 1): `OK occurrences=1 anchor=1-BROKEN`
  - `U2-oor-anchor` (anchor=99999): `OK occurrences=1 anchor=OUT-OF-RANGE`
  - `U3-no-anchor`: `OK occurrences=1`
  - `U4-long` (40-word quote, anchor=165): `OK occurrences=1 anchor=165-ok`
  Cause: `source-recheck.py` `anchor_verdict` only enforces the anchor when `occurrences > 1` (B2); a unique quote is accepted whatever its anchor. There is no word-count check anywhere in `source-recheck.py` (`grep -n -E '[Ww]ords?|25'` finds none). `capture-binding-check.py` does not read quotes (its quote handling is a comment, line 163). The frozen after-predicate names no quote instrument at all. So kill clauses "not located at its anchor" and "exceeds 25 words" have no measuring command.
- C2 `kill_rule` "if ANY after-value misses" — enumerated, OK.
- C2 `scope_limit` "any listed CVE" — scope, not a quantifier over an unenumerated set.

### (d) Freeze order — HOLDS
Commands and exits:
- `git log --format='%H %ci %s' -n 12` -> 847b5379 (committer 05:34:37 -0300), 654d877f (05:34:15), ccd6a54 (05:12:18), exit 0.
- `git merge-base --is-ancestor 654d877f 847b5379` -> exit 0; `git merge-base --is-ancestor 847b5379 HEAD` -> exit 0.
- `git log --format='%H parent=%P author=%ad committer=%cd' -n1 654d877f` -> parent = ccd6a54; author date 05:12:18 (copied), committer date 05:34:15. Ordering rests on ancestry, not on author timestamps.
- Implementation commit: none. `git log ccd6a54..HEAD` lists only 654d877f and 847b5379. Order "controls < freeze < implementation" is therefore true so far (implementation absent).
- Non-claim receipt not committed: `.ufo/waves/round-74/controls/freeze-check-replay-r74.txt` is untracked (`git status --short` -> `??`, exit 0; `git log -- <file>` empty). Its internal timestamp 08:35:12Z (05:35:12 -0300) is after the freeze commit (05:34:37 -0300). That is consistent with "before any candidate measurement" but the file is not in history. R73-V6 in the claims non-claim list says "already committed by the L1" — **not true at observation time**.
- Also in the controls commit: `c2-base-counters-r74.txt` records `capture-exit=0` from a command piped to `tail -1`, i.e., the tail's status. Standalone measurement shows the base capture-binding exit is 0 (see (c) and below). The freeze-check replay's own correction block (M74-2) records the same defect class; the base counter receipt was not corrected.

### (e) Score honesty — HOLDS
- C1 `axis_score_before=4`, `axis_score_after=4`, basis "nominal per QUALITY R58: the scored resolve.py citation census is not read by this gate". QUALITY.md line 415 defines R58: a claim that changes only a file the axis census never reads is labelled nominal and its score is held, with the non-moving metric named. C1 changes only the recheck counter; the basis names the metric. Consistent.
- C2 `axis_score_before=8`, `axis_score_after=8`, basis "the coverage denominator is operator-owned; the claim is the admission, not a score move". No sentence in claims.json claims a score increase. The non-claim list says "capability demonstration recorded", not a score.
- No sentence in claims.json, the freeze notes, or the controls claims more than delta 0.

### (f) Scope exclusion of restoration-recheck: lines — FALSIFIED (C1 scope sentence)
Frozen text (claims.json C1 `scope`): "the census reads the FIRST 'recheck:' line per corpus/knowledge/*.md file; 'restoration-recheck:' is a different header and is out of the counted population by definition".
- Docstring of `recheck-cwd-census.py` (lines 2-24): states "reads the FIRST `recheck:` line" (matches code: `line.startswith("recheck:")`, line 39). It does NOT mention `restoration-recheck:` anywhere. `grep -c -i restoration corpus/instruments/recheck-cwd-census.py` -> 0, exit 1. **Doc/counter mismatch: the exclusion lives only in claims.json.**
- Literal falsity: the restoration header is out of the recheck-value population, but a file that carries only `restoration-recheck:` is still in the counted population: `glob("*.md")` picks it up, `entries` is incremented, and `norecheck` is incremented. Measured with a scratch fixture (`r.md` with only `restoration-recheck: ...`, `p.md` with a `recheck:` line and a `restoration-recheck:` line), command `python3 corpus/instruments/recheck-cwd-census.py --root <fx> --lane <fx>`:
  - `NORECHECK r.md`
  - `RECHECK-CWD entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=0 exit1_foreign=1 exit_other=0 norecheck=1`
  - `RECHECK-CWD-RESULT conformant`, exit 0.
  So the census clause `norecheck=0` fails on such a tree while the RESULT line still says conformant. The RESULT line gates only `noprefix` and `exit2_foreign` (docstring line 15; code line 156).
- Current tree: no file lacks a `recheck:` line (`grep -l '^restoration-recheck:' corpus/knowledge/*.md` -> 2 files; the loop `grep -q '^recheck:'` over those two returned no missing file, exit 0). So the base census holds; the falsity is latent, not measured on the lane.
- Smallest safe correction (for the L1): record this as falsified-as-written in the round-74 lesson (precedent: RC-5/RC-6 in corpus/lessons/round-73.md), and add the docstring sentence as a documentation fix that does not change predicates. Do not rewrite claims.json here.

### C1 red-before (controls) — re-measured, verdict holds
Ran the four routed mutants built from the lane counter in scratch (M4 RESULT line forced to `conformant`; M5 `dir="/tmp"`; M6 `rmtree` removed; M7 last `recheck:` line). `python3 <mutant>.py --selftest` -> `selftest case=prefix-census ok ...`, `selftest cases=1 failures=0`, exit 0 for each. All four survive the base selftest, as the receipt states.
- Receipt caveat: `c1-redbefore-mutant-survival-r74.txt` records `selftest-stdout-tail=<selftest cases=1 failures=0>` with angle brackets, a paraphrase, not verbatim output. The exit codes and verdicts reproduce; the receipt should carry the raw tail.
- M7 kill check: a fixture entry with two `recheck:` lines (first `cd <lane> && true`, second `python3 corpus/instruments/missing.py`) gives base `noprefix=0 exit2_foreign=0 exit0_foreign=1` and M7 `noprefix=1 exit2_foreign=1 exit0_foreign=0` — the claimed first-line case discriminates M7. Holds.
- M4 kill check: the claimed result-main case discriminates M4 by running `main()` on a nonconformant fixture (base `main()` returns exit 1 with `RECHECK-CWD-RESULT nonconformant`; M4 would print `conformant`) — holds in design.

### C2 frozen loci and distinctness — HOLD
Measured: `sed -n` of the capture (sha256 `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`, `wc -l` = 375, `sha256sum` exit 0) at L151, L154, L155, L156, L165, L212, L214, L221, L226, L227, L230, L233, L236, L243 (exit 0). Each claimed clause matches: definition/FuzzIL (151), Targets/ patches and clang>=4.0 (154-156), semantic correctness versus try-catch wrappers (165), Swift/C split (212), MutationFuzzer/ScriptRunner/Corpus/Environment/Minimizer/Evaluator/Lifter (214-221), Storage and event-driven design (226-227), REPRL with state reset (230), tree hierarchy root + 16 + 256 (233, 236), NDSS 2023 paper (243). Note: the capture's component list includes `Environment` (L218), which the claim omits; this is a subset, not a contradiction.

Distinctness: `grep -rIil 'fuzzilli\|reprl' corpus --exclude-dir=source-snapshots` -> knowledge hit is only `project-zero-fuzzilli-vs-bigsleep-comparison.md` (S093/F41), consistent with the claim's screen.

Sources-census: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` -> six `W04` lines (S028, S029, S072, S076, S080, S085) and `kasegi ok`, exit 0. Matches the six inherited warnings.

### Capture-binding status at the freeze — finding
- `python3 corpus/instruments/capture-binding-check.py` at HEAD (847b5379) -> `FAIL rule=missing-manifest dir=round-74`, `records=87 bound=87 unbound=0`, exit 1. The freeze commit's S109.txt has no manifest yet, so the tree is red under this instrument until C2 lands. Expected; but the do-nothing receipt says exit 0.
- At ccd6a54 (archive export into scratch, `git archive ccd6a54... corpus | tar -x`): `records=87 bound=87 unbound=0`, exit 0. So the receipt's value is right at base, while its `capture-exit=0` field is the pipeline status.

## Base-state counter values (re-measured)
| Command | Output | Exit |
|---|---|---|
| `recheck-cwd-census.py --selftest` | `selftest cases=1 failures=0` | 0 |
| `recheck-cwd-census.py --root L --lane L` | `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0` / `RECHECK-CWD-RESULT conformant` | 0 |
| `frontier-recheck-count.py` | `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108` / `entries=54 pass=54 exit=0` | 0 |
| `capture-binding-check.py` (ccd6a54 archive) | `records=87 bound=87 unbound=0` | 0 |
| `capture-binding-check.py` (HEAD) | `FAIL rule=missing-manifest dir=round-74` / `records=87 bound=87 unbound=0` | 1 |
| `sources-census.sh validate --root <fleet> kasegi` | six W04 + `kasegi ok` | 0 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 108 | 0 |
| knowledge files (`ls corpus/knowledge/*.md \| wc -l`) | 89 | 0 |
| knowledge-expected (non-comment rows / lines) | 89 / 91; sort-clean; set-equal to ls (`cmp`) | 0 |

## Commands run and exits (summary)
- `git rev-parse --show-toplevel` -> lane path, exit 0
- `git log --format='%H %ci %s' -n 12`, `git log ccd6..HEAD`, `git show --stat` (both commits), `git merge-base --is-ancestor` x2, `git status --short`, `git log -- .ufo/waves/round-74/controls/freeze-check-replay-r74.txt` -> all exit 0
- `git -C <lane> archive ccd6a54... corpus | tar -x` (into scratch), `git cat-file`/`show ccd6a54:corpus/instruments/capture-binding-check.py | cmp -` -> exit 0 (identical)
- Counter/instrument runs listed above, with `PYTHONDONTWRITEBYTECODE=1` and TMPDIR in scratch
- Mutant and stub builds and runs (M4..M7, STUB) and fixtures (`fx/manifest.json`, two-line entry, restoration-only entry), all in scratch -> exits as stated above
- `sed -n` of S109.txt loci, exit 0
- `grep -c -i restoration corpus/instruments/recheck-cwd-census.py` -> 0, exit 1; `grep -n 'bash' ...` -> lines 9, 51
- Lane writes: none by this seat. Only this report was written.

## Recommended correction set (smallest safe; for the L1, not applied)
1. C1 scope: falsified-as-written; record in round-74 lesson (RC-5 precedent); add the restoration-only-population sentence to the counter docstring. No predicate rewording.
2. C1 selftest: the tmpdir-parent case must spy on `tempfile.mkdtemp` (argument `dir`) during census(); name the mutant battery command (`K73MutateCounter-run.sh` or equivalent) in the after-predicate's receipt; require the verbatim selftest output.
3. C1 kill (d): name the grep command and its expected output (one `bash -c` call site, line 51 at base).
4. C2 capture: name `source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json` as the measuring command for quotes; add a word-count check (<=25 words) as a named command; accept that unique-quote anchors are not enforced by source-recheck and record the gap in the entry's Limits (or name a separate anchor check).
5. C2 registry: name a diff of pre-existing SOURCES.md rows (e.g. `git diff ccd6a54 -- corpus/SOURCES.md`, removed-line count = 0, added-line count = 1).
6. Receipts: replace the `c2-base-counters` `capture-exit` value with the instrument's own exit (measured: base 0, HEAD 1); replace the angle-bracket placeholder in `c1-redbefore-mutant-survival-r74.txt` with raw output; commit `freeze-check-replay-r74.txt` or drop the claim that it is committed.

## Tools installed
None.

## Scratch
Created /fast/scratch/hyaku/kasegi-r74/CriticClaims; removed with `rm -rf -- <dir>`, exit 0; `ls -d` afterwards exit 2 (absent); no `/tmp/recheck-cwd-*` left.
