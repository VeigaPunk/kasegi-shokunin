# CriticClaims — round-75 attempt 1 falsification report

Seat: CriticClaims (critic, leaf; no subagents). Read-only on the lane; writes are this report, one evidence file (`CriticClaims-attack-rename.py`, the rename-attack variant of the base counter) and the seat's scratch (deleted before yield). No git/jj mutation. `claims.json` not edited.

Inputs read: `.ufo/waves/round-75/claims.json` in full (long target lines 21 and 45 read whole); `controls/c1-donothing-r75.txt`, `controls/c1-redbefore-restoration-r75.txt`, `controls/c2-base-counters-r75.txt`, `controls/assimilation-considerthese-r75.txt`. Lane HEAD = `748dfb666280adfb1e249fcf6a265c5d9951eefb` (matches freeze; `git -C <lane> rev-parse HEAD`, exit 0). Lane census worktree is byte-identical to base (`git show f9cc05b:corpus/instruments/recheck-cwd-census.py | cmp - <worktree copy>`, exit 0).

## Summary

| ID | Claim / clause | CLASS | Blocks verification? | Finding |
|---|---|---|---|---|
| F1 | C1 target (ii) | letter-gap, forged-implementation reachable | **BLOCKS** C1 as a verified claim on target (ii) | A relabel of the base counter (old behaviour, bucket renamed `restoration_only`) passes A1 (frozen case-6 expectations), A2, A4 and the frozen kill rule. It mis-buckets neither-header files. No clause binds the `norecheck` half of (ii). |
| F2 | C1 A1 case 6 / A3 | vacuity, forged-implementation | **BLOCKS** | The case-6 RESULT limb can be dropped. A3 requires only "at least two" of M-A/M-B/M-C, so the seat can skip M-B. M-A and M-C then fail, and A1–A4 all pass with a census-only case 6. |
| F3 | C1 A3 | letter-gap (no measuring command) | **BLOCKS** A3 as a predicate until L1 names the mutant harness | A3 gives no command or mutant location. "the unamended counter survives (before block)" is ambiguous as a criterion. |
| F4 | C1 `exec_surface`, notes | letter-gap; dangling reference | routed-as-observation | No command for "exactly one bash -c". "kill rule (d)" does not exist in claims.json. The notes say the kill rule "keeps the exec-surface count fixed"; the C1 kill_rule text does not. |
| F5 | C1 (i) docstring, scope rows | letter-gap | routed-as-observation | No command for the docstring sentence, the SKILL.md registry row or the README section. |
| F6 | C2 coverage ground | WEAKENED-as-written | **BLOCKS** the "comparison to other fuzzers" ground | An entry quoting only the abstract passes B1–B8 as written. No clause requires quotes from the comparison or evaluation text. |
| F7 | C2 B5 "every quote <= 25 words" | letter-gap (named command does not check its predicate) | **BLOCKS** B5 until an explicit word-count check runs | `source-recheck.py` enforces only a 12-character minimum (`MIN_QUOTE_CHARS`). There is no 25-word cap. |
| F8 | C2 B1 row fields | letter-gap | routed-as-observation | Only the row count (`grep -c` = 110) is measured. kind/tier/status/opened/recheck/used-by have no command. |
| F9 | C2 B3 set-equality | letter-gap; partial self-reference | routed-as-observation (independent comparator exists, unnamed) | No command for "set-equal". `recheck-audit.py` compares the list against the directory, so it is not circular, but B3 does not name it. |
| F10 | C2 B4/B5 provenance | letter-gap (false-provenance path) | routed-as-observation | The snapshot digest pins capture-tool output. No after-value pins the fetched PDF bytes (918189) or PDF digest. |
| F11 | C2 B8 distinctness | vacuity | **BLOCKS** B8 as a mechanical predicate | B8 is verdict-only. Its named sibling grep (`grep -ril fuzzilli revenger/corpus`) returns nothing, so it cannot discriminate. |

Do-nothing answers: C1 do-nothing fails A1 and A2 (not reachable). C2 do-nothing fails B1, B3, B4, B5, B6 (not reachable). Details below.

---

## C1 — recheck-cwd census amendment

### F1 (letter-gap, forged-implementation reachable): the bucket can be relabelled and still pass A1–A4

Attack: `CriticClaims-attack-rename.py` (in this wave dir) is the base counter with the norecheck bucket renamed to `restoration_only`, `norecheck` kept as a constant 0, and the gate extended with `and restoration_only == 0`. Behaviour is otherwise unchanged.

Run on two fixtures I built in scratch (`TMPDIR` under scratch; `--root`/`--lane` = fixture):

- F2-case6 (the frozen case-6 fixture: `r.md` = only `restoration-recheck: touch <fx>/restoration-ran`; `p.md` = `recheck: cd <fx> && true`):
  - base: `RECHECK-CWD entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=0 exit_other=0 norecheck=1` / `RECHECK-CWD-RESULT conformant`, exit 0. This reproduces `controls/c1-redbefore-restoration-r75.txt` exactly.
  - attack: `... norecheck=0 restoration_only=1` / `RECHECK-CWD-RESULT nonconformant`, exit 1. Marker `restoration-ran` absent (`ls` exit 2).
  - So the attack meets the frozen case-6 assertions exactly: `entries=2 restoration_only=1 norecheck=0 noprefix=0 exit2_foreign=0`, marker absent, nonconformant, exit 1.
- F1-neither (one file, no recognised header at all, body empty):
  - base: `norecheck=1`, conformant, exit 0 — the target (ii) behaviour ("norecheck = files carrying neither header").
  - attack: `norecheck=0 restoration_only=1`, nonconformant, exit 1. The neither-header file is mis-bucketed, and the verdict is only nonconformant because the gate is now wrong about that file.

The real tree cannot distinguish the two: base real-tree `norecheck=0` (`controls/c1-donothing-r75.txt`) means no real entry lacks a recheck header, so the attack's real-tree output equals the base's, and A2/A4 pass.

Frozen clauses that would have to catch it: A1 case 6 (no neither-header fixture), A2 (no neither-header file on the real tree), A4 (parity on base-equal fields). None does. Gap in the frozen text: (ii) states "norecheck = files carrying neither header" but no after-value or case asserts a neither-header file lands in `norecheck` and not in `restoration_only`. I did not reword the freeze; L1 must decide (add a case, or accept as a stated gap). Under the kill rule as written C1 would be VERIFIED with this implementation.

Also, the rename variant with `restoration_only` pinned to 0 (no relabel, no behaviour) fails A1: case 6 asserts `restoration_only=1`. So the crude variable-rename fake is caught; the faithful relabel (F1) is not.

### F2 (vacuity, forged-implementation): case 6's RESULT limb can be weakened, and A3 permits skipping the one mutant that catches it

The gate lives only in `main()` (base lines 231–234). `census()` returns counts independent of the gate. So a case-6 that asserts the census counts but not the RESULT line (or exit code) passes any counter whose gate ignores `restoration_only`. Derived from base code structure (not separately run; [INFERENCE] only in the sense that it is read directly from the base source).

Mutant M-B ("RESULT gate keeps only the old two clauses") is the only class that catches a census-only case 6. A3 says "at least two mutant classes" of M-A, M-B, M-C must each fail the new selftest. The seat can pick M-A (caught by the restoration_only=1 count assertion) and M-C (caught by the marker assertion), and never run M-B. Then: census-only case 6 + M-A + M-C killed + A1 `cases=6 failures=0` + A2 + A4 = all green, while the RESULT limb is untested. No frozen clause names M-B or the RESULT-limb assertion as mandatory. Exact gap: A3 "at least two" ⇒ M-B is optional, and the RESULT limb of case 6 has no independent check.

Note: the claim's case-6 text does say "prints RECHECK-CWD-RESULT nonconformant and exits 1", so the weakened case is a departure from the frozen case text. Nothing mechanical checks the case text against the frozen text; A3 is the only backstop.

### F3 (letter-gap): A3 has no measuring command

A3 says each of M-A, M-B, M-C "fail[s] the new selftest (print a failing case line and cases=6 failures=1, exit 1)". No command, harness or mutant location is named, and "at least two" lets the seat choose. "the unamended counter survives (before block)" reads as a red-before note, not a criterion; the wording is ambiguous. Routed to L1: name the mutant harness and the mandatory set, or record that A3 is judged, not measured.

### F4 (letter-gap; dangling reference): exec surface

- `exec_surface` says "the census keeps exactly one bash -c call site (run_foreign) before and after; SentinelCounter re-measures (kill rule (d) continuity)".
- `claims.json` contains no "(d)" kill rule: `grep -n -o '.\{0,60\}(d).\{0,40\}' claims.json` (exit 0) returns only the exec_surface line.
- The notes say "kill rule keeps the exec-surface count fixed". The C1 `kill_rule` text is "if any of A1-A4 fails ... C1 is NOT VERIFIED". Exec surface is not in it.
- Base count verified: `grep -c '"bash", "-c"' base-census.py` → 1; `subprocess` sites: lines 52–56 only.
- Attack: a second `bash -c` that runs something harmless would pass A1–A4 and the exec_surface sentence. No command catches it.
Routed: L1 should record `grep -c '"bash", "-c"'` = 1 as a named check, and drop or fix the "(d)" reference (not a reword of a predicate; a dangling pointer).

### F5 (letter-gap): docstring, registry row and README

Target (i) (docstring sentence stating the restoration-recheck exclusion) and the scope rows (SKILL.md gate-registry row, `corpus/instruments/README.md` section) have no measuring command. A variant with no docstring change passes A1–A4. Routed-as-observation: the docstring should be checked by reading or a named grep.

### C1 do-nothing (the unamended counter)

- A1: base `--selftest` prints `selftest cases=5 failures=0`, exit 0 (I ran it: `TMPDIR=<scratch> python3 base-census.py --selftest | tail -1` → `selftest cases=5 failures=0`, exit 0). A1 needs `cases=6` → fails.
- A2: base real-tree output (`controls/c1-donothing-r75.txt`) has no `restoration_only=0` field → literal A2 string fails.
- A4: base vs base has an empty stdout delta; A4 requires the delta to be exactly the inserted field → fails.
- Conclusion: do-nothing is not reachable under A1–A4. (Real-tree census not re-run by me: it executes 90 recheck values, some network-touching; L1's receipt is the evidence.)

Renaming-only answer (the first question): a constant-0 rename is caught by A1 (`restoration_only=1` in case 6). A faithful relabel with unchanged behaviour is not caught (F1).

---

## C2 — F53 admission on S110 (NDSS 2023 Fuzzilli paper)

### Pre-checks run (all read-only)

- Base registry: `grep -c` for `S110` in `corpus/SOURCES.md` → `0` (grep exit 1 on zero matches; the count is 0). Leads line 175 is the NDSS lead (`- NDSS Symposium 2023 paper on Fuzzilli ...`), and line 174 is the OSV overview lead the C2 kill rule names (`- OSV.dev overview page https://google.github.io/osv.dev/api/ — lead`). Both exist; the kill-rule reference is not dangling.
- Base knowledge: `grep -vc '^#' corpus/instruments/knowledge-expected.txt` → 90 rows (92 lines total; 2 comments). Consistent with `controls/c2-base-counters-r75.txt`.
- The paper: `curl -sS -L --max-time 60 -o ndss-f290.pdf -w 'http=%{http_code} type=%{content_type} bytes=%{size_download}'` → `http=200 type=application/pdf bytes=918189`, curl exit 0. Matches the freeze. sha256 `bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9` (recorded for L1; the freeze pins the byte count only). `pdftotext` exit 0.

### F6 (WEAKENED-as-written): an abstract-only entry passes B1–B8; the comparison ground is absent

Evidence from the paper (`pdftotext`, plain mode):
- Abstract span (plain-text lines 27–52, from "Abstract—" to "I. I NTRODUCTION" at line 53): contains design ("we present the design and implementation of an intermediate representation"), evaluation ("evaluated our fuzzer over a period of six months ... 17 confirmed security vulnerabilities"). `grep -n -i 'compar\|other fuzzer\|state-of-the-art\|evaluat\|superion\|sofi'` over lines 27–52 returns only "evaluated" (exit 0). No comparison term.
- Comparison to other fuzzers is in the introduction (plain lines ~139–155: "our fuzzer compares well with Superion, a state-of-the-art open-source fuzzer", "comprehensive comparison against modern ... Superion") and in the evaluation (plain lines ~1164–1430: "Comparison with SoFi", "Comparison with Superion").

So an entry built only from abstract quotes covers design and evaluation, and does not cover comparison. The target says the row is "tier A scoped to the paper's own statements: design, comparison to other fuzzers, evaluation results", and the B-clauses do not check that scope:
- B5 checks that each quote anchors in the snapshot and is ≥12 characters. Any abstract sentence passes.
- B6 counts entries and passes (`entries=56 pass=56`). Coverage-blind.
- B8 is a verdict about the paper's ground vs other rows (F11), not about the entry's quotes.
- B1 checks the row count only (F8).

Exact gap: no after-value requires that the entry's quotes or its `teaches` coverage include the comparison ground, or that the entry's quotes come from more than one section. This is WEAKENED-as-written. I did not reword; L1 must decide whether to add a per-ground quote requirement (a new predicate) or to record the comparison ground as unclaimed.

### F7 (letter-gap; named command does not check its predicate): B5 "≤ 25 words"

- B5: "source-recheck.py ... exits 0 with every quote anchor-ok and every quote <= 25 words".
- `grep -n "len(\|word" corpus/instruments/source-recheck.py` (exit 0): hits at lines 108 (anchor range), 151 (`if len(normalize(assertion["quote"])) < MIN_QUOTE_CHARS:`), 391 (selftest count). No word count, no upper bound.
- So B5's exit 0 does not establish the 25-word cap. A quote of 300 words passes. BLOCKS B5 as stated until an explicit word count runs (e.g., a named one-liner over the manifest's quotes). This is a missing check, not a reword.

### F8 (letter-gap): B1 row fields

B1 says the new S110 row is "kind=paper, tier A, status mined, opened 2026-11-05, recheck 90d, used-by the new entry". The only measurement is `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md = 110`. No field check exists. Also "lane registry S110 unused — collision re-check receipt assimilation-considerthese-r75.txt" is not evidenced by that receipt: it measures staged ids vs registry (`reg-ids=109 staged-ids=94 collisions=79`) and never names S110. The base `grep -c S110` = 0 (above) is the evidence that S110 is unused. Routed-as-observation: L1 should cite the base grep, and the row fields should be read at integration.

### F9 (letter-gap; partial self-reference): B3 set-equality

- B3 names `ls corpus/knowledge/*.md | wc -l = 91` and `LC_ALL=C sort -c ... ` (sort exit 0). The **set-equality** has no named command.
- Self-reference answer: the expected list is hand-maintained by the same round (`recheck-audit.py` header: "keep in sync with corpus/knowledge/"). Adding the entry and its list row in one commit passes the sort and the count. But the set-equality comparator is independent of authorship: `recheck-audit.py` `expected_mismatch(root, expected)` computes `wanted - actual` and `actual - wanted` against `glob(corpus/knowledge/*.md)`, and `main()` runs it by default whenever `corpus/instruments/knowledge-expected.txt` exists (lines 438–440). `recheck-audit.py` does not regenerate the list.
- So an independent binder exists (`recheck-audit.py`), but no B-clause names it, and it is not in the kill rule. Routed-as-observation: L1 should name `python3 corpus/instruments/recheck-audit.py` (exit code and `missing=`/`unexpected=` lines) as the set-equality check.

### F10 (letter-gap; provenance): the snapshot is not pinned to the PDF bytes

- `capture-source.py --kind pdf` fetches the URL and runs `pdf_to_text(raw)`; the digest recorded in the manifest is of the output text (lines 244, 272, 294). `source-recheck.py` "verifies captured bytes, not current upstream availability" (its docstring).
- No after-value pins the fetched PDF (918189 bytes, or any digest of it). B4 (`records=89 bound=89`) binds records to manifest rows; B5 checks quotes against local bytes. A hand-typed `S110.txt` with the right anchors passes B4 and B5.
- Routed-as-observation: the manifest should record `fetched_utc`, HTTP status and the PDF byte count and digest, as the round-74 S109 manifest does (`fetch_method`, `fetched_utc`, `http.status`). The freeze does not require it.

### F11 (vacuity): B8 distinctness screen

- B8 asserts the paper's ground is "distinct from S109, S093 and revenger's S117 / S396". No command produces a pass/fail; the verdict is recorded in the round lesson, written by the same round.
- Named sibling sweep: `grep -ril 'fuzzilli' revenger-shokunin/corpus` → empty output (no Fuzzilli text in revenger at all). `grep -ril 'ndss' revenger-shokunin/corpus` → `SOURCES.md` (rows S114, S341, S363 are NDSS papers, none about Fuzzilli), `round-73-re-resource-atlas.md`, `lessons/2026-10-29-re-resource-atlas.md`. A Fuzzilli grep cannot discriminate between a NDSS-Fuzzilli row and no row, because the sibling has no Fuzzilli text.
- In-lane sweep: `grep -n -i 'ndss\|fuzzilli' corpus/SOURCES.md` at base → S093 (line 100), S109 (line 121), Leads (lines 173, 175), and other lesson-text lines. No NDSS row.
- BLOCKS B8 as a mechanical predicate; it can only be satisfied by judgment. L1 must either record the verdicts as judged (not measured) or define a discriminating grep.

### C2 do-nothing (base)

Base receipts (`controls/c2-base-counters-r75.txt`): registry 109 (B1 needs 110), knowledge 90 (B3 needs 91), `records=88` (B4 needs 89), frontier `rows=52 ... entries=55` (B6 needs 53/56). B5 fails at base (no S110 manifest). B2 and B7 pass at base. So do-nothing fails B1, B3, B4, B5, B6. Not reachable.

### B3 self-reference, answered directly

The expected list is authored by the same round, so the list can be edited to match. The independent comparator is `recheck-audit.py`'s glob-based `expected_mismatch`, which is not authored by the round. The count "91" (`ls | wc -l`) is directory-derived and not self-referential. The gap is naming, not circularity: no B-clause or kill rule invokes the comparator (F9).

---

## Checked, not findings

- Lane census worktree == base census (cmp exit 0).
- Two real knowledge entries (`claim-gates.md`, `claim-package-contract.md`) carry both a `recheck:` line and a `restoration-recheck:` line (`grep -n '^recheck:\|^restoration-recheck:'`). The base reader takes the `recheck:` line, so the real-tree counts are unaffected. Implementation hazard, not a finding: an amendment that tests `"recheck:" in line` (substring) instead of `startswith` would misread `restoration-recheck:` as a recheck header.
- The base selftest runs its own five cases: `selftest cases=5 failures=0`, exit 0.
- Real-tree census not re-run by me (it executes 90 recheck values, some network-touching); the receipts are the evidence I cite.

## Commands and exit codes (this seat)

- `git -C <lane> rev-parse HEAD` → `748dfb6…`, exit 0.
- `git -C <lane> show f9cc05b…:corpus/instruments/recheck-cwd-census.py | cmp - <worktree>` → exit 0.
- `grep -l '^restoration-recheck:' corpus/knowledge/*.md` → 2 files, exit 0.
- `grep -c S110 corpus/SOURCES.md` → `0`.
- `grep -n -i 'ndss\|fuzzilli' corpus/SOURCES.md` → exit 0 (rows at lines 100, 121, 173, 175, and lesson text).
- `grep -n "len(\|word" corpus/instruments/source-recheck.py` → lines 108, 151, 391, exit 0.
- `grep -c '"bash", "-c"' base-census.py` → `1`.
- `curl -sS -L --max-time 60 ... ndss2023_f290_paper.pdf` → `http=200 type=application/pdf bytes=918189`, exit 0; `pdftotext` exit 0.
- `grep -n -i ... ndss-plain.txt` abstract span 27–52 → `evaluated` only, exit 0; boundary "NTRODUCTION" at 53.
- `base-census.py --root <fx-F1> --lane <fx-F1>` → `norecheck=1`, conformant, exit 0.
- `base-census.py --root <fx-F2> --lane <fx-F2>` → `norecheck=1`, conformant, exit 0 (matches receipt).
- `attack-rename.py --root <fx-F2>` → `norecheck=0 restoration_only=1`, nonconformant, exit 1; marker absent.
- `attack-rename.py --root <fx-F1>` → `norecheck=0 restoration_only=1`, nonconformant, exit 1.
- `attack-rename.py --selftest` → `selftest cases=5 failures=0`, exit 0 (the attack passes the base cases too).
- `base-census.py --selftest` → `selftest cases=5 failures=0`, exit 0.
- `grep -rln 'fuzzilli' revenger-shokunin/corpus` → empty; `grep -ril 'ndss' ...` → 3 files.

## Evidence files

- `.ufo/waves/round-75/w1/CriticClaims-attack-rename.py` (copy; `cmp` exit 0 against scratch original).

## Routing summary for L1

Blocking on the frozen text as written (decision needed; no rewording done by this seat): F1 (C1 target (ii) neither-header half unbound), F2 (case-6 RESULT limb not mandatory), F3 (A3 no measuring procedure), F6 (C2 comparison-ground coverage unbound), F7 (B5 25-word cap unchecked by its command), F11 (B8 verdict-only).

Routed-as-observation: F4 (exec-surface command; "(d)" dangling pointer; notes vs kill_rule mismatch), F5 (docstring/scope rows), F8 (B1 row fields), F9 (name `recheck-audit.py` for set-equality), F10 (PDF byte pin in manifest).
