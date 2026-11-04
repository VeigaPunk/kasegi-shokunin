# CriticC1 — round 68, C1 adversarial review

**Verdict: DEFEATED (as a repair of the program-execution class).** The frozen predicate itself passes on the C1 gate (`VERIFY measurements=8 failures=0`, exit 0, gate sha256 `10c87100…74fee8`), so this is not a kill under the frozen rule. But two shapes still execute a named program through allow-listed heads on the committed gate:

1. **`sort --compress-progra=PROG` and every other unique long-option prefix** (`--compress-p`, `--compress`, `--comp`, `--co`, and the space form `--compress-progr PROG`) ran the compressor **18288 times each** on the candidate gate — identical to base. The denial matches only the exact token `--compress-program` / `--compress-program=…`; the host `sort` (uutils 0.8.0, clap) accepts prefix abbreviations.
2. **Plain `git show <commit>` runs the config-declared textconv driver with no flag at all** (marker 2 on a non-merge commit, 3 on a merge, 5 for a two-commit range), identically at base and candidate. Textconv is git show's *default* for commit patches; `--textconv` only matters for blob form. Only `--no-textconv` (marker 0) or `--stat` (0) suppress it. So refusing the `--textconv` token closes the blob-form spelling the counter measures, not the class the claim's residual names ("`git show --textconv` really ran a config-declared driver"). Also still executing on both gates: `git cat-file --textconv REV:PATH` (TC 1), `git cat-file --filters REV:PATH` (smudge filter 1), `git show -c/--cc/-m/--first-parent/--diff-merges=… <merge>` (TC 2–4).

Pre-existing, unchanged by this commit (not blamed on it; paired base run shows the same): sort write spellings `sort -uo FILE`, `sort -ro FILE`, `sort --outp=FILE`, `sort --o=FILE` all **wrote the file** at base and candidate.

## What I ran (all in `/fast/scratch/hyaku/kasegi-r68/CriticC1`, TMPDIR there)

- Gate export: `git show 82b3b7d:corpus/instruments/figure-audit.py > gate-82b3b7d.py`; `sha256sum` → `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8` (matches pin). Base `controls/base-gate-d0f48405.py` → `8147350c…7ad247` (matches). Counter → `785e38fd…6b4b` (matches; not edited).
- Fixture: `run/fixture` (60000-line big.txt, g.txt) and `run/repo` (`git init`; toplevel asserted == `run/repo`; identity `fixture@shokunin.local`; config `diff.mydriver.textconv`, `filter.myfilter.smudge`, `diff.external`, `core.pager` all pointing at marker-writing scripts; `.gitattributes` `big.txt diff=mydriver`, `f.txt filter=myfilter`; commits one/two/side + merge). Driver: `probe-r68.py`, `probe2-r68.py` (copied beside this report). Each probe is a one-figure ledger run as `python3 <gate> --ledger L --root <fixture|repo>`; marker files and named output files are counted after each run.
- `python3 -B probe.py` → `01-probes-paired.txt`; `python3 -B probe2.py` → `02-probes-commit-form.txt` (literal SHAs: the tokenizer refuses `~`, so first-run `HEAD~1` probes were parse refusals, re-measured here).
- Frozen counter: `python3 -B .ufo/waves/round-68/controls/c1-probe-run-r68.py --gate gate-82b3b7d.py --work counter --mode candidate` → `03-counter-candidate.txt`.
- Selftest + mutants: `--selftest` on the candidate and three scratch mutants (drop `--compress-program`, drop `--textconv`, drop the exact/`=` match line) → `04-selftest-and-mutants.txt`; direct reason capture of the 4 new selftest derives → `05-selftest-derive-reasons.txt`.

## Observed (excerpts; full lines in receipts)

(a) Spellings, `gate=base` | `gate=cand`:

| probe | base | cand |
|---|---|---|
| `sort --compress-program=P -S 1K big.txt \| head -n 1` | rc=1 COMP=18288 | rc=2 derive-not-read-only, COMP=0 |
| `--compress-progra=P` | rc=1 COMP=18288 | **rc=1 derive-upstream-signal-13 COMP=18288** |
| `--compress-p=P` / `--compress=P` / `--comp=P` / `--co=P` | rc=1 COMP=18288 each | **rc=1 COMP=18288 each** |
| `--compress-progr P` (space) | rc=1 COMP=18288 | **rc=1 COMP=18288** |
| `"--compress-program=P"`, `--compress-'program'=P`, `--compress-progra\m=P` | rc=1 COMP=18288 | rc=2 derive-not-read-only COMP=0 |
| `$'--compress-program=P'` | rc=2 refused (tokenizer `$`) | rc=2 refused |
| `sort -S 1K -- big.txt --compress-program=P` | rc=1 derive-upstream-exit-2 COMP=0 (file operand) | rc=2 derive-not-read-only (over-refusal of a filename after `--`, harmless) |
| `sort -uo F g.txt` / `-ro F` / `--outp=F` / `--o=F` | rc=1, **F written** | rc=1, **F written** |
| `sort -S 1K -T DIR big.txt` | COMP=0, no file left | same |
| `git show --textconv HEAD:big.txt` | rc=1 TC=1 | rc=2 derive-not-read-only TC=0 |
| `git show --textcon` / `--textc` | rc=1 derive-upstream-exit-128 TC=0 (git rejects abbrev) | same |
| `git show --textconv=x HEAD:big.txt` | exit-129 TC=0 | rc=2 refused |
| `git show e501c93 \| grep -c y` (no flag) | **TC=2** | **TC=2** |
| `git show -p` / `--word-diff` / `--no-ext-diff` `e501c93` | TC=2 | TC=2 |
| `git show --no-textconv e501c93`, `git show --stat e501c93` | TC=0 | TC=0 |
| `git show c5ff8bb` (merge) / `-c` / `--cc` / `-m` / `--first-parent` / `--diff-merges=dense-combined` | TC=3/3/3/4/2/3 | identical |
| `git show e501c93 c5ff8bb` | TC=5 | TC=5 |
| `git cat-file --textconv HEAD:big.txt` | **TC=1** | **TC=1** |
| `git cat-file --filters HEAD:f.txt` | **SM=1** | **SM=1** |
| `git show --filters` | exit-128 (not a show option) | same |
| `git show --ext-diff e501c93` | rc=2 refused | rc=2 refused |
| `git show --ext-dif` / `--ext` | derive-exit-1 EXT=0 (diff.external not run) | same |
| `git show --outpu=F HEAD` | derive-exit-128, no file | same |
| `GIT_PAGER=cat git show`, `GIT_EXTERNAL_DIFF=… git show`, `git -c core.pager=cat show`, `git -p show` | rc=2 refused (head not allow-listed) | same |
| `ls`, `wc --files0-from`, `sha256sum -c`, `cut`, `tr`, `grep -r` | no marker, no write | same |

(b) False stales: `grep -c -- '--compress-program'` and `grep -c -- '--textconv'` over `corpus/instruments/figure-audit-ledger.json` → **0** and **0**; over all 256 tracked `*ledger*.json` files (`git ls-files | grep -i 'ledger.*\.json$' | wc -l` = 256) → files containing either string = 0; `grep -rl` over `corpus/` → `--compress-program` in 3 files (`figure-audit.py`, `lessons/round-60.md`, `lessons/round-68.md`), `--textconv` in 1 (`figure-audit.py`) — all prose/code, no derive. The lane ledger's 18 `git show` derives are all blob form `rev:path` (no textconv by default); lane has 0 `.gitattributes` files. Counter `real-ledger`: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`. **No false stale introduced.** One over-refusal shape: a file operand named `--compress-program=…` or a pathspec `--textconv` after `--` is now refused (rc=2) — theoretical only.

(c) Selftest cases: candidate `selftest cases=77 failures=0`; each of the 4 new cases `exit=2 want=2 verdict=pass`. Direct run of the same derives on the candidate: all 4 `stderr='FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only'`; on base the 3 sort derives are `rc=0 ok` and the git one `rc=1 derive-exit-128`. Mutants: drop `--compress-program` → `failures=3` (exactly the 3 sort cases, exit=0); drop `--textconv` → `failures=1` (git case, exit=1 reasons=derive-exit-128); drop the match line → `failures=9`. **They do not pass for the wrong reason.** Weakness: `run_case` checks only the exit code for exit-2 cases (never `reason=` on stderr), and the cases use `/bin/false` on a 3-byte file in a non-repo, so they pin parse refusal only, never non-execution. The counter's measurements 1/2/8 carry the execution evidence.

Frozen counter on candidate (`03-counter-candidate.txt`): all 8 `MEASURE … ok`, `VERIFY measurements=8 failures=0 gate_sha256=10c87100…`, rc=0.

## Residuals / disagreements (round-69 candidates)

1. **R69-a sort long-option prefixes** (`--co`…`--compress-progra`, `=`/space forms) still execute PROG — the same 18288 runs as base. Fix: match any `--` token that is a prefix of a denied long flag (length ≥ the shortest unique prefix, or simply `flag.startswith(tok.split("=")[0])` for tokens of length ≥3 beginning `--`), and do the same for `--output` (`--o=`, `--outp=` wrote files). Add selftest cases `--compress-progra=`, `--co=`, `--outp=`.
2. **R69-b sort bundled short `-o`** (`-uo F`, `-ro F`) writes F at base and candidate — the `-o` rule only checks tokens starting `-o`. Fix: refuse any single-dash bundle containing `o` for sort.
3. **R69-c git show default textconv**: `git show <commit>` (and `-p`, `--word-diff`, merge forms, ranges) runs the driver with no flag. Fix shape: either require `--no-textconv` on non-blob `git show` / admit only `rev:path` blob form, or inject `--no-textconv` into the executed argv (would change the "same decoded argv" rule — L1 call).
4. **R69-d git cat-file `--textconv` / `--filters`** execute the driver / smudge filter at both gates; cat-file has no DENIED_FLAGS entry. Add `("git cat-file", ("--textconv", "--filters"))` (git rejected abbreviations in my probes: `--textcon`/`--textc` → exit 128, so exact + `=` matching suffices for git).
5. Claim-text disagreement (not a kill): the claim's `target` names only "`sort --compress-program` (equals, space and quoted spellings) and `git show --textconv`", which the gate meets; the `residual` frames the *class* ("program-execution classes admitted through allow-listed heads"). Measured: the class survives (items 1, 3, 4). The score stays 4 either way (nominal per R58), so the honest summary is "the two measured spellings are refused; the class is not closed".
6. Counter docstring says "six legitimate read-only derives" for measurement 3; the list and the output have 5 (`controls=5 failed=0`). Cosmetic; counter is frozen.

## Tooling
No tools installed or upgraded. Host `sort`/`head`/`tail`/`wc`/`ls`/`cut`/`tr`/`sha256sum` are uutils 0.8.0, `grep` is pi-uu-grep 0.2.0, git 2.56.0 — every result above is specific to these PATH binaries.

Scratch `/fast/scratch/hyaku/kasegi-r68/CriticC1` removed before yield.
