DEFEATED — new bypass class N1: the admitted derive `git show --output=MARK-RECEIPT HEAD` writes a file into the audited root (`git show ` is allow-listed with no option filter), and `git show --output=../<path> HEAD` writes outside it; corroborated by `git show --ext-diff HEAD` executing a configured command. New bypass class N2: the admitted derive `python3 corpus/instruments/../../../above-evil.py` executes a non-instrument script outside the audited root (the python branch only checks the literal `corpus/instruments/` prefix). Neither derive uses any P1–P8 text; neither is in the recorded residual set. Predicate objection in §7: every frozen C1 number stays green in the presence of both bypasses.

## 0. Scope and identity
1. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `472737847ff31d1255bf1a0745822a5e878e9622` (lane HEAD, exit 0).
2. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain=v1 -- corpus/instruments/figure-audit.py` → empty (worktree clean for the file under test).
3. `sha256sum $S/figure-audit-candidate.py` → `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0` — equals the frozen pin in claims.json C1 counting_commands; the lane implementation is byte-identical to the frozen candidate. Scratch copy extracted with `git -C L show 472737847ff31d1255bf1a0745822a5e878e9622:corpus/instruments/figure-audit.py`.
4. Frozen claims read via `git -C L show 00b535758d2cfa4511cda7167b67cdc045b85fb4:.ufo/waves/round-59/claims.json`; probe set from `git -C L show 00b5357…:.ufo/waves/round-59/controls/c1-probe-run.sh`; mutant battery from lane HEAD `corpus/instruments/figure-audit-mutbat.py`.
5. L was never written except this evidence file; no git mutation was run against L (only rev-parse/status/show/diff, all read-only). All fixtures lived in S = `/fast/scratch/hyaku/kasegi-r59/CriticC1` (removed after this file was written; no leftovers).

## 1. Method
Per attempt (all in scratch): fresh root `<dir>/root` holding `g.txt` = `35\n`; one-figure ledger `<dir>/one.json` = `{"figures":[{"id":<id>,"record":"g.txt:1","recorded":"35","derive":<attempt text>,"want":"35"}]}`; then exactly `python3 $S/figure-audit-candidate.py --ledger <dir>/one.json --root <dir>/root` with `TMPDIR=$S`; the instrument exit code is recorded and the root is listed for marker files. Root kinds: `plain` (g.txt only), `git` (git init + g.txt committed; `git rev-parse --show-toplevel` asserted equal to the root), `pyesc` (root also has `corpus/instruments/`; evil script placed outside `corpus/instruments`), `gitextdiff` (git + committed `.gitattributes` `g.txt diff=evil` + repo config `diff.evil.command`). Fixture commits used per-commit flags `-c user.name=fixture -c user.email=fixture@invalid`; no throwaway identity elsewhere. Batch drivers: `$S/driver.py` (28 attempts), `$S/fix-driver.py` (3 corrected attempts), `$S/receipt.sh`/`$S/receipt2.sh` (standalone receipts, quoted verbatim in §4/§5).

## 2. Gate surface (path:line into the candidate copy)
1. `figure-audit-candidate.py:47-50` — `READ_ONLY_HEADS` includes `"git show "`, `"git cat-file "`, `"git ls-tree "`, `grep`, `wc `, `wc<`, `ls `, `ls*`, `sha256sum`, `cat `, `cut `, `sort `, `awk `, `"sed -n "`, `head `, `tail `, `python `, `python3 `. Nothing after the head token is inspected: no option filtering, no `--`/flag grammar.
2. `:78-128 split_segments` — refuses unquoted `;`, backtick, `(`, `)`, `\n`, `\r`, `>` (`:121`), a lone `&`, `||`, and backtick/`$(` inside double quotes (`:97`). Backslash is never an escape anywhere (the recorded B1/B2 root).
3. `:131-136 segment_ok` — python branch: `len(parts) >= 2 and parts[1].replace("\\","/").startswith("corpus/instruments/")` (`:135`); no `..` rejection, no existence or committed-ness check. Else `head.startswith(READ_ONLY_HEADS)` (`:136`).
4. `:139-142 check_read_only` — `split_segments` + per-segment `segment_ok` only. `audit` (`:157-197`) sends any admitted derive to `run_derive` → `bash -c <derive>` with `cwd=root`.
5. `mutbat.py:23-27` — exactly two mutants: `m4-drop-stale-literal-case` (selftest case count) and `m6-readonly-gate-off` (`return head.startswith(READ_ONLY_HEADS)` → `return True`, i.e. `:136` only).

## 3. Attempt table (31 rows; driver verbatim output lines `ATTEMPT id=… exit=… markers=… outside=…`; all 28 driver rows are reproduced by `python3 $S/driver.py`, the three fix rows by `python3 $S/fix-driver.py`)
| id | derive | root | instr exit | MARK in root | outside | class |
|---|---|---|---|---|---|---|
| A01-p1-sanity | `cat g.txt; touch MARK-A01` | plain | 2 | 0 | 0 | control: refused, `reason=derive-not-read-only` (P1 shape) |
| A02-p6-sanity | `cat g.txt \| tee MARK-A02` | plain | 2 | 0 | 0 | control: refused (P6 shape) |
| A03-benign | `cat g.txt` | plain | 0 | 0 | 0 | baseline admitted, `derived=35 ok` |
| A04-ctrl-quoted-sep | `cat g.txt \| awk 'BEGIN{x=1;y=2} {print}'` | plain | 0 | 0 | 0 | the claim's CTRL, exact text: admitted, `derived=35 ok` |
| A05-b1-esc-sq | `cat g.txt \'; touch MARK-A05; \'` | plain | 1 | 1 | 0 | recorded residual B1 reproduced |
| A06-b2-esc-dq | `cat g.txt \"; touch MARK-A06; \"` | plain | 1 | 1 | 0 | recorded residual B2 reproduced |
| A07-b3-sed-e | `sed -n '1e touch MARK-A07' g.txt` | plain | 1 | 1 | 0 | recorded residual B3 reproduced |
| A08-b4-awk-system | `awk 'BEGIN{system("touch MARK-A08")}' g.txt` | plain | 1 | 1 | 0 | recorded residual B4 reproduced |
| A09-b6-sort-o | `sort -o MARK-A09 g.txt` | plain | 1 | 1 | 0 | recorded residual B6 reproduced |
| A10-residual-awk-write | `cat g.txt \| awk 'BEGIN{print 1 > "MARK-A10"}{print}'` | plain | 0 | 1 | 0 | named-open probe: exit 0, markers=1 — byte-consistent with claims "RESIDUAL-awk-write exits 0 markers=1" |
| A11-sed-w | `sed -n 'w MARK-A11' g.txt` | plain | 1 | 1 | 0 | named open (sed `w`), non_claim_frontier_items |
| A12-b6-sort-output-long | `sort --output=MARK-A12 g.txt` | plain | 1 | 1 | 0 | B6 long form |
| A13-b4-family-awk-dq | `awk "BEGIN{system(\"touch MARK-A13\")}" g.txt` | plain | 1 | 1 | 0 | B4 family via double-quoted program (scanner exits the span at `\"` — mirror of B2 — execution is still awk-in-program) |
| A23-sed-sub-w | `sed -n 's/35/35/w MARK-A23' g.txt` | plain | 1 | 1 | 0 | sed `s///w` flag — sed-`w` family (named open) |
| A14-git-show-output | `git show --output=MARK-A14 HEAD` | git | 1 | 1 | 0 | **NEW N1** — admitted, `MARK-A14` created in the audited root |
| A15-git-show-o-short | `git show -o MARK-A15 HEAD` | git | 1 (derive exit 128) | 0 | 0 | short `-o` unsupported by `git show`; N1 needs the long form |
| A14b-git-show-output-above | `git show --output=../MARK-OUT-A14B HEAD` | git | 1 | 0 | 1 | **NEW N1** — file written OUTSIDE the audited root (content verified in fix-driver output) |
| A16-git-show-output-norepo | `git show --output=MARK-A16 HEAD` | plain (no repo) | 1 (derive exit 128) | 0 | 0 | scoping: needs a repo root; the production audit root IS the lane repo |
| A24-git-ls-tree-output | `git ls-tree --output=MARK-A24 HEAD` | git | 1 (derive exit 129) | 0 | 0 | survey: `ls-tree` rejects `--output` |
| A25-git-cat-file-output | `git cat-file --output=MARK-A25 HEAD` | git | 1 (derive exit 129) | 0 | 0 | survey: `cat-file` rejects `--output` |
| A27-git-show-extdiff | `git show --ext-diff HEAD` | gitextdiff (1 commit) | 1 | 0 | 0 | ext-diff did not fire on an empty-tree (root-commit) diff — retested as A27b |
| A27b-git-show-extdiff-twocommit | `git show --ext-diff HEAD` | gitextdiff (2 commits) | 1 | 1 | 0 | **NEW N1 corroboration** — external diff driver executed (`MARK-A27b` created); precondition: repo-local `.gitattributes` + `diff.<drv>.command` config |
| A17-py-traversal-outside (v1) | `python3 corpus/instruments/../../outside-evil.py` | pyesc | 1 (derive exit 2) | 0 | 0 | my fixture placed the script one level off (`corpus/instruments/../..` resolves to the root, not beside it) — re-run as A17fix |
| A18-py-traversal-above (v1) | `python3 corpus/instruments/../../../above-evil.py` | pyesc | 1 (derive exit 2) | 0 | 0 | same fixture miss — re-run as A18fix |
| A17fix-py-traversal-rootlevel | `python3 corpus/instruments/../../outside-evil.py` (script at `root/outside-evil.py`) | pyesc | 1 | 2 (`MARK-IN`, `MARK-OUT`) | 0 | **NEW N2 degree 1** — non-instrument script inside the root executed |
| A18fix-py-traversal-escapes-root | `python3 corpus/instruments/../../../above-evil.py` (script beside the root) | pyesc | 1 | 1 (`MARK-IN`) | 1 (`MARK-OUT`) | **NEW N2** — non-instrument script OUTSIDE the audited root executed |
| A19-nul-crash | `cat g.txt\x00` | plain | 1 (uncaught `ValueError: embedded null byte`) | 0 | 0 | robustness: admitted, then the harness crashes before any `FIGURE-AUDIT` summary; exit 1 masquerades as stale, not a clean exit-2 refusal |
| A20-backslash-in-word | `to\uch MARK-A20` | plain | 2 | 0 | 0 | safe direction: bash would run touch; the gate refuses (over-refusal) |
| A21-quoted-word | `"to"uch MARK-A21` | plain | 2 | 0 | 0 | safe direction: refused |
| A22-formfeed | `cat g.txt\x0ctouch MARK-A22` | plain | 1 (derive exit 1) | 0 | 0 | `\f` absent from the refuse set at `:121` but bash-inert — admitted, no effect |
| A26-sort-compress-program | `sort -S 1K --compress-program=touch g.txt` | plain | 0 | 0 | 0 | admitted; compress-program never invoked (3-byte input never spills) — unfiltered program-name flag, execution NOT demonstrated |

## 4. Receipt N1 (standalone; `$S/receipt.sh`, verbatim)
```bash
R1=$(mktemp -d -p "$S")
git -C "$R1" init -q
printf '35\n' > "$R1/g.txt"
git -C "$R1" add g.txt
git -C "$R1" -c user.name=fixture -c user.email=fixture@invalid commit -qm fixture
python3 -c 'import json,sys; json.dump({"figures":[{"id":"R14","record":"g.txt:1","recorded":"35","derive":"git show --output=MARK-RECEIPT HEAD","want":"35"}]}, open(sys.argv[1],"w"))' "$R1/one.json"
python3 "$FA" --ledger "$R1/one.json" --root "$R1"
```
Output (trimmed to the decisive lines), exit 1:
```
FIG R14 recorded=35 derived=UNAVAILABLE reason=derive-empty stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
root listing after: .git  g.txt  MARK-RECEIPT  one.json
```
The instrument did NOT refuse (no `reason=derive-not-read-only`, no exit 2); bash ran `git show --output=MARK-RECEIPT HEAD` with cwd=root and git wrote `MARK-RECEIPT`. The final exit 1 (stale, empty stdout) is the claims' own marker-vs-refusal convention: the probe runner counts EXECUTED by marker presence, REFUSED only by exit 2 before the derive runs.

## 5. Receipt N2 (standalone; `$S/receipt2.sh`, verbatim derive run)
```bash
R2="$S/receipt2"; mkdir -p "$R2/root/corpus/instruments"
printf '35\n' > "$R2/root/g.txt"
# $R2/above-evil.py — OUTSIDE the audited root — writes MARK-OUT beside itself and MARK-IN in cwd
python3 -c '…json.dump one-figure ledger with derive "python3 corpus/instruments/../../../above-evil.py"…' "$R2/root/one.json"
python3 "$FA" --ledger "$R2/root/one.json" --root "$R2/root"
```
Output, exit 1:
```
FIG R18 recorded=35 derived=UNAVAILABLE reason=derive-empty stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
audited root listing: corpus  g.txt  MARK-IN  one.json
outside the audited root: above-evil.py  MARK-OUT  root
MARK-OUT content: executed outside the audited root
```
(`corpus/instruments/../../../` resolves from cwd=root to the parent of the root; the gate admitted the derive because `:135` only checks the literal prefix.) The first receipt-2 run failed for a fixture reason only — a bash `printf` escaping bug produced a SyntaxError script (exit 1, no markers); it was re-run with the byte-identical script already proven in the A18fix row.

## 6. Why N1/N2 are new classes
1. P1–P8 texts (`c1-probe-run.sh`): `;`, `&&`, lone `&`, newline, `$()`, `| tee`, `>`, `||`. Neither N1 derive nor N2 derive contains any of those characters outside a word: `git show --output=MARK-A14 HEAD` and `python3 corpus/instruments/../../../above-evil.py` are single segments of allow-listed heads.
2. Recorded residuals (goal + claims.json non_claim_frontier_items): B1/B2 backslash-escaped quotes, B3 sed `e`, B4 awk `system()`, B6 `sort -o`, and awk/sed in-program writes (sed `w`). N1 is a shell-level write by an allow-listed head through a diff OPTION — no metacharacter, no program interpreter. N2 is a path-scope escape of the python branch — the docstring's "only against a committed instrument" (`:19`, enforced at `:135` as a textual prefix) is defeated by `..`.
3. Safe directions verified and NOT claimed: A15/A24/A25 (only `git show` carries `--output`), A16 (non-repo root refuses at git level), A20/A21 (bash-executable words the gate refuses), A22 (bash-inert char the gate admits), A27 v1 (ext-diff needs a preimage diff). N1's ext-diff variant (A27b) executes a command outside the allow-list but needs repo config control, so it is corroboration, not the primary defeat.

## 7. Predicate objection — the frozen C1 claim is met, vacuously, in the presence of N1/N2
1. The C1 kill_rule binds refusals only to P1–P8 + CTRL-quoted-separator + four counters (probe run, selftest cases=14 failures=0, mutbat killed=2/2 survivors=0, ledger figures=35 ok=35 stale=0). None of my bypass derives appears in any of those inputs: run today against lane HEAD, every frozen number still reproduces (A01/A02 reproduce the P1/P6 refusal shape; A04 is the exact CTRL text and admits with `derived=35 ok`; A10 reproduces the recorded RESIDUAL line exit 0 markers=1). All five frozen predicates hold while the gate admits live file writes and command execution.
2. The only generality instrument is structurally blind here: `mutbat.py:23-27` mutates the selftest case list (`m4`) and the `:136` head check (`m6`). No mutant touches `split_segments` (`:78-128`), the python branch (`:132-135`), or git-head option handling — so `killed=2/2` cannot catch N1 or N2 by construction.
3. The frozen sentence scopes the refusal assertion to "every shell-chaining derive in the committed probe set P1–P8" — the enumeration is explicit, so this is an honestly-scoped claim, not an accidental gap. But the claim's kind line ("instrument repair"; the gate "protects the lane's figure ledger") and the instrument's own docstring ("the audit never runs a mutating command", `:13-14`) assert a safety property that enumerated-probe satisfaction does not establish. As frozen, C1 is satisfiable by a gate that is materially unsafe on every input outside the eight probes; N1/N2 are concrete instances. Sharpening (already recorded, not claimed new): the R58 CriticC1 caveat that the selftest pin is count-only (cases run, not coverage).
4. Smallest safe correction to propose (instrument decision, not mine to land): filter git heads to explicit read-only subcommand+option grammars (`git show <obj>`, reject `--output*`/`--ext-diff`/`-o*`), and require the python branch's second token to contain no `..` and to exist under `root/corpus/instruments/` (or drop awk/sed/python from the allow-list). Also catch `ValueError` in `run_derive` for the NUL crash (A19) so refusals are uniform exit 2.

## 8. Bounds, tooling, scratch
1. Lane writes: only `.ufo/waves/round-59/w1/CriticC1.md`. No ledger, claims, SOURCES.md, README.md, PROVINCE.md, or instrument was edited; corrections are text-only in §7.4.
2. Tooling authorization not exercised: no installs (pacman untouched; only python3 and git used).
3. Scratch `S=/fast/scratch/hyaku/kasegi-r59/CriticC1` (driver.py, fix-driver.py, receipt.sh, receipt2.sh, extracted claims/probe-runner/mutbat/instrument copies, 31 attempt trees) was removed after this file was written; nothing was left behind and nothing was written under /tmp (TMPDIR=$S throughout).
