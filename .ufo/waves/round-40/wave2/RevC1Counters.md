# RevC1Counters — round-40 FALSIFY wave 2 receipt (seat: attack the C1 counters)

Seat: RevC1Counters · Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` · Dispatch: L1 (KasegiR40), hyaku run 9
Base `a7af2ce63bce153757d39bf66b366a96caf30c13` · claims freeze `5e985b74075dd3813a63d7750966bf8abf693465`
Frozen claims: `.ufo/waves/round-40/claims.json` (read, not edited)

## Refs observed at dispatch

- Lane tip (HEAD, detached): `3074c7679d6f527ec3930d7748ccce1dbae4a58a` — history: `4766b9d` integrate wave1 → `bfca9ae` J2 → `8717b8b` J3 → `94abbff` J4 → `3074c76` J5.
- The receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (16 lines, `export-ref=3074c76…`) is **untracked** at the tip: `git ls-tree HEAD .ufo/waves/round-40/final-gates/` is empty and `git log --all -- <receipt>` lists no commit. So the claims' `Y = J + receipt` commit **does not exist yet**; the tip is J.
- Suite `corpus/instruments/r40-closure.sh` sha256 `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e` — working tree, `git show HEAD:` and the SKILL.md Gates & probes registry row (SKILL.md:1122, "round 40; sha256 bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e") **all agree**. Registry check: **reproduced**.

## Commanded commands — results

Byte-exact transcripts: `wave2/RevC1Counters.runs.txt` (R1–R7). Scratch transcripts were destroyed with the scratch dir at yield, per seat rules.

| # | Command | Required | Observed | Verdict |
|---|---|---|---|---|
| R1 | `--export-ref 3074c76…` (lane tip) `--work $S/w --lane <lane>` | `closed=10/10 exit=0` | `closed=9/10 exit=1`, H7 red (`receipt=0,sentinel=0,ref=,…`) | **contradicted at the tip** — see P1 |
| R2 | `--selftest --export-ref 3074c76…` | `selftest cases=10 failures=0`, 10 graded lines | `selftest cases=10 failures=1`; `case=H7 positive=fail mutants=6/6 verdict=fail`; the other 9 cases pass, all 33 mutants rejected, all 6 forged reports rejected | **contradicted at the tip** — same P1 cause |
| R3 | `--export-ref a7af2ce…` (base) | `closed<10/10 exit=1` | `closed=3/10 exit=1` | **reproduced** |
| R4 | `--export-ref 8371e7ac…` (r39 judged head) | `closed<10/10 exit=1` | `closed=2/10 exit=1` (H10 `deleted=1`: the r39 round deleted a tracked path) | **reproduced** |
| R5 | plain run (no `--export-ref`) | exit 2 | exit 2, `refusing to run against the live worktree` | **reproduced** |
| R6 | `--export-ref <Y′>` over a scratch fixture repo = tip + the byte-exact receipt committed (`git diff --name-only tip Y′` = the receipt path only) | `closed=10/10 exit=0` | `closed=10/10 exit=0`; transcript **byte-identical** (`cmp`) to the on-disk receipt | **reproduced at simulated Y′** |
| R7 | `--selftest --export-ref <Y′>` | `selftest cases=10 failures=0` | `selftest cases=10 failures=0`, ten graded `case=H<i> positive=pass mutants=k/k verdict=pass` lines (3,3,2,3,2,4,6,2,5,3 mutants), `selftest judge=own-report accepted=1`, six forgeries rejected | **reproduced at simulated Y′** |

### P1 — the commanded Y-state is not materialized (procedural, blocks R1/R2 verbatim)

claims.json `judged_head_rule` says the lane tip Y adds only the receipt (`git diff --name-only J Y` = the receipt). At dispatch the receipt is untracked, so the tip is J, and the suite — by its own documented green window — must print `closed=9/10 exit=1` at J (H7 fail-closed on the absent receipt). That is exactly what R1/R2 show. The green window itself is sound: committing the byte-exact receipt (scratch fixture Y′ `7d9a151e67bde125200a9c05e331ceb10babba66`) makes R6/R7 green and the plain transcript byte-identical to the receipt bytes, which is the claims' "after" line. **Action for the L1**: commit the on-disk receipt bytes as the single change on top of `3074c76…` (that commit is Y), then R1/R2 reproduce verbatim. No instrument change is needed. Related: the kill rule "lane working tree not clean at filing" is currently false — untracked `final-gates/`, `wave2/` and two `kasegi-r40-falsify.ready*` markers exist; they must be cleaned/committed at filing.

## Attack results (defeaters supplied in scratch; byte-exact transcripts in `wave2/RevC1Counters.defeats.txt`)

Method: full-suite runs over scratch fixture repos (clone of the lane; `git rev-parse --show-toplevel` asserted before any commit; fixture identity `r40-fixture@local`), plus sourced invocation of individual `check_*` functions on crafted trees.

### Defects found — check passes while its defect is present

- **D1 (moderate) — H2 accepts wrong receipt values by substring match.** `h2_scan` tests `index(s,"closed=7/8")` and `index(s,"failures=1")`. A record line carrying `closed=7/80` and `failures=10` (wrong values) scores `named=4,missing=0` → H2 **green** (defeat1.cap T2; honest control T1 green). A future round could "correct" the round-39 receipt with false values and pass. The real round-40 records carry the exact tokens (`closed=7/8` ×13, `failures=1` ×14, no longer variants — checked), so no live lie; this is a checker defect exploitable from round 41 on. Fix: match the tokens with a boundary (`closed=7/8` not followed by `[0-9]`, `failures=1` not followed by `[0-9]`).
- **D2 (low-moderate) — H3 has no fence awareness.** A QUALITY.md whose only `M39-2` table row sits inside a ``` code fence scores `mentions=1,rows=1` → H3 **green** (T4). The "criterion row" is not a rendered row. Fix: reuse H2's fence scanner in H3.
- **D3 (low-moderate) — H4 location token false-positives inside the URL.** The block scanner's location regex `:[0-9]+` matches `:7` inside `https://example.com/page:7`; a quote with no real location then scores `s056=1` (T5). Fix: exclude `://`-span matches or require the token outside the URL span.
- **D4 (low-moderate) — H4's ≤25-word cap is evaded by hyphen-joining.** `words()` splits on `[^ \t\n]+`, so 42 real words joined into 21 hyphen-joined tokens pass as a 21-word quote (T6, `s056=1`). Fix: count words after splitting on `-`/`/` too, or cap characters as well.
- **D5 (moderate) — H9 declaration reads outside the export via a symlink.** A committed symlink whose target is a host file, declared as `pwn 1 <sha256 of the host file's tail>`, validates (`declared=1,valid=1,tail=1,pure=1,paths=1` → **green**, T7): `tail -n` follows the symlink, so `got` is computed from bytes outside the export root, contradicting the suite's "every tree limb reads bytes only under that export root". `path_safe` rejects `..` but not symlinked components; `[ -f ]` follows links. Fix: `tail --` on a `readlink`-resolved path and require the resolved target to stay under the export, or reject non-regular declared paths. (Sibling RevC1Sandbox independently recorded symlink findings — consistent.)
- **D6 (low) — H6 name-family match is case- and separator-sensitive.** A leftover scratch entry named `Kasegi-R40-stray` or `kasegi_r40-stray` scores `strays=0` → H6 **green** (T14); the lowercase control reds (`strays=1`). The kill rule's glob (`kasegi-r39*|kasegi-r40*`) has the same blind spot by construction. Fix: case-insensitive match and both `-`/`_` separators.
- **D7 (low) — H6's recorded payload is not bound to the audited root.** A receipt produced with `--scratch-root <empty dir>` while a family stray existed elsewhere prints `strays=0,read=ok` and is **byte-identical** to the honest receipt (T11: `nothing to commit` on commit attempt) — the audited root leaves no fingerprint in the transcript, so the lie is unfalsifiable post-hoc. Mitigations that hold: the claims' counting commands use the default root, and any later plain run re-derives H6 live against the real root. Fix: print a root fingerprint (e.g. sha256 of the sorted top-level family entries) in the H6 payload.
- **D8 (low) — H1's registry-row regex accepts a row that merely mentions the instrument.** A SKILL.md row `| density.py notes (see r40-closure.sh for the gate that pins it) | doc | n/a |` scores `registry=1,registry-in=skill` → H1 **green** (T13). The seat-commanded sha256 check (which passes today) is the real binding; the row-shape check alone is weaker than the registry's purpose. Fix: require the instrument name in the first cell and a run-command cell containing `--export-ref`.

### Attacks that did NOT defeat a check (recorded green-run evidence)

- **H7 tree-binding holds.** Patching the export on top of Y — `corpus/SOURCES.md` (T8) or `SCORECARD.md` (T9) — reds H7 via `diff-clean=0` (T8 also shows H9 staying green: SOURCES.md/SCORECARD.md are not declared paths, so the receipt diff is the only guard for them at Y — by construction, since Y = J + receipt). T9 cascades: `payload-match=7` (H2's payload changed, and H5's `control` dropped to 7/8 because the export receipt's payloads no longer all match the recomputed PAYFILE).
- **Forged-env H8 receipt is caught twice.** Producing a receipt with `R40_NEG_BASE=8371e7ac…` (so H8's "base" slot actually re-runs the r39 head) prints `closed=8/10 exit=1` **at production** — H5 reds (`control=7/8`: the export's honest receipt disagrees with the forged PAYFILE) and H7 reds (`closed-0=2,closed-line=0`). Committing the forged receipt and re-running plain: `closed=8/10 exit=1`, H7 `payload-match=8` (recorded `base=2/10` vs recomputed `base=3/10`). The `R40_NEG_BASE`/`R40_NEG_R39` knobs cannot mint a green receipt.
- **Selftest judge holds.** All six forged reports (summary-only, case-lines-only, failed-cases, detail-free `mutants=0/0`, 9-case, no-verdict-field) rejected in both selftest runs; `judge=own-report accepted=1` only at Y′.
- **Negative controls are genuine.** Base prints `closed=3/10 exit=1` (H1/H2/H3/H4/H5/H7/H8/H9 red — the suite and round-40 artifacts are absent at base), r39 head prints `closed=2/10 exit=1` (additionally H10 `deleted=1`). Neither can be confused with green.
- **H2's fence model is sound in the pass direction.** A correction inside a CommonMark 4-backtick fence reds H2 (`missing=1,fences=open`, T3) rather than passing — the {0,3}-indent fence grammar errs red, not green.
- **Work-dir hygiene holds.** `--work` inside the lane refused; reused `--work` subdirs (`export/`, `mut/`, `neg-*`, `h5/`) cleared before use (code-verified; stale-bytes reuse would be caught by the clearing).

## Verdict

- The five claims.json C1 counting commands **reproduce** at the state the claims define (Y = J + receipt): verified at scratch fixture Y′ `7d9a151e…` with a byte-identical transcript; negative controls and the plain-run refusal reproduce verbatim at the real lane.
- **P1 (procedural, blocking R1/R2 verbatim at the tip):** Y is not committed — the receipt is untracked at `3074c76…`. The L1 should commit the receipt bytes as the single change on top of the tip; no instrument change needed.
- **8 checker-hardening defects (D1–D8)**, none of which invalidate the round-40 evidence at the real lane bytes (real records carry exact values; real declared paths are regular files; the real registry row pins the suite digest). D1/D5 are the ones I would route to a round-41 fix first.

## Residual risk & gaps

- H4's URL/date/quote truth (does the URL exist, does the quote appear at the cited location) is shape-only in C1; truth-level binding lives in C2's source-recheck, which this seat did not re-open (other seats own it).
- H6 is live by design: my `strays=0` payload is a statement about `/fast/scratch/hyaku` at run time (only `kasegi-r40`, which contained `--work`, existed — verified), not a property of the commit.
- The `--scratch-root`/`R40_NEG_*` knobs are caller-supplied by design; D7 records the residual indistinguishability.
- I did not fuzz H9's numstat parsing (renames, quoted paths) beyond the suite's own five mutants; quoted-path declarations are theoretically parseable differently (`set -- $line` word-splits).

Scratch `/fast/scratch/hyaku/kasegi-r40/RevC1Counters/` removed before yield (defeat fixtures and the Y′ clone lived only there; the byte-exact transcripts survive in `RevC1Counters.defeats.txt` / `RevC1Counters.runs.txt`).
