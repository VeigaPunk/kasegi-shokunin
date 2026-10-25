# CritPredicate — C1 (`depth:verifiability`, recheck-audit) attacked for vacuity

**ONE LINE, ACT BEFORE PUBLICATION:** publish C1 on `pass_strict=37/37` + `exit=0` and on **37/37**, never on `pass` alone and never as `lines=35` — `pass` is still satisfied by a degenerate line (`cd <lane> && true # corpus/knowledge/<own>.md` → frozen `111`, `pass=True`, `FROZEN-ONLY`), the frozen denominator moved 35 → 37 when C2's two entries landed (`C1.independent_of: C2` is false), and the instrument changed **seven times during this review** (`d07af435 → efbd18ee → 4475d2e6 → 6eb657c0 → 1ccee066 → 8ab4dff7 → 8c3771e1`), so the report must pin the sha it quotes.

**Verdicts:** A1 **BROKEN** (frozen limbs) / SOUND-at-exit-only · A2 **BROKEN** (label) / **WEAK** (pass accounting) · A3 **WEAK** · A4 **BROKEN** · A5 (unasked) **BROKEN**.

Every number below was re-verified at **08:45Z** against the bytes then on disk, sha256 `8ab4dff70b578268bb2ff625dff99168d17e24629856180c30f8b9f5204f1475`, 14145 B, `--selftest` **12 cases / 0 failures / exit 0**. The counter output is byte-identical across the last four revisions (`6eb657c0`, `1ccee066`, `8ab4dff7`, and `8c3771e1` observed at 08:50Z), so the churn is in the instrument's code, not in its verdict.

Line references below are to the revision measured (`8ab4dff7`, 08:45Z); siblings were still editing at 08:50Z, so line numbers shift by 1-3. The citations that matter are also named by code and are stable across every revision: `limbs["cwd"]`, `limbs["paths"]`, `pass = all(limbs.values())`, `"class": "passing" if lane_rc == 0 else "fail-closed"`, `ok = passed == len(entries) and complete and strict_passed == total`.

---

## 0. State and provenance

| artifact | state at 08:45Z |
|---|---|
| `corpus/instruments/recheck-audit.py` at freeze | `d07af435…b564d6` (recorded in `c1-instrument-digest.txt` at 05:16 local) |
| … used for `c1-before.json` (05:16 local) | `d07af435…` — schema has no `strict`/`total_knowledge_files` |
| … used for `c1-after.json` (05:39:19 local) | `6eb657c0…` — schema has `strict`, `pass_strict`, `complete` |
| … intermediate revisions this review observed | `efbd18ee` (05:33:22), `4475d2e6` (05:34:28, **selftest red: 11 cases / 4 failures**), `1ccee066` (05:39:56) |
| … **on disk now** (05:43:26 local) | `8ab4dff7…` — `c1-instrument-digest.txt` refreshed at 05:43:31 and **matches**; selftest green. By 08:50Z the file was `8c3771e1…` with byte-identical counter output |
| `c1-after.json` | `lines=37 total=37 complete=True pass=37 pass_strict=37 fail_closed=23`, `strict_failing_limbs` all 0 |
| live counter, current bytes | `strict pass=37/37 cdroot_fail=0 instrument_fail=0 artifact_fail=0 own_fail=0` / `lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` |
| do-nothing control, current bytes (`c1-controls/base`, `c1-controls/do-nothing`) | `lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 exit=1` — control preserved |

Two provenance points survive the convergence. (i) The **verdict rule changed between the two measurements**: `c1-before.json`'s `exit=1` came from `passed == len(entries)`, while `c1-after.json`'s `exit=0` additionally requires `complete` and `strict_passed == total` (`:236`). The delta 6 → 37 is nevertheless attributable to the corpus edit, not to the rule change: the frozen limbs (`:102-113`) are untouched and the current run computes `pass=37` from them, so the pre-fix rule would also print `pass=37 exit=0` on the fixed corpus. (ii) The receipt pair was produced by two different instrument revisions (`d07af435` / `6eb657c0`); the report must name them, because "same counter" is true only at the level of the frozen three limbs.

Live exit classes: **14** lines `lane_exit=0`, **23** `lane_exit=1` (restoration-gated), **0** `lane_exit=2`.

All runs were read-only: `source-recheck.py`'s only write is inside its own selftest; `anchorcheck.py` shells `git show`. No lane file was written except this report.

---

## 1. Limb (b): can it pass vacuously? Does limb (c) block it?

**Verdict: BROKEN for the frozen three limbs.** Limb (b) (`:106`) demands *equality* of exit status and digest across two cwds, not *success*; limb (c) (`:113`) demands only that a named `corpus/…` token *exists*; `pass` (`:142`) never consults `lane_rc`.

Witnesses against the current bytes (scratch roots `/tmp/crit25*`, each a real `corpus/knowledge/*.md`):

| recheck line | frozen | lane/foreign | `pass` | strict verdict |
|---|---|---|---|---|
| `false corpus/knowledge/alwaysfalse.md` | `111` | `1 / 1` | **True** | FROZEN-ONLY |
| `cd /home/…/kasegi-shokunin && true # corpus/knowledge/authorised-testing-rules-of-engagement.md` | `111` | `0 / 0` | **True** | FROZEN-ONLY |
| `cd /nonexistent-lane-path && test -e corpus/knowledge/deadcd.md` | `111` | `1 / 1` | **True** | FROZEN-ONLY |
| `frobnicate corpus/knowledge/unknowncmd.md` | `111` | `127 / 127` | **True** | FROZEN-ONLY |

On the pre-strict bytes a scratch run printed `lines=3 pass=3 fail-closed=2 … exit=0` — the audit exited 0 while every line failed. **Limb (c) blocks none of these**: it is satisfied by a trailing comment naming any existing corpus file, or by the entry's own path, which the instrument itself found by glob (`:150`) and therefore exists by construction. `cd … && true` *without* a path token is caught (`paths_fail=1`) — which is the only reason the lane's M4-degenerate mutant dies — but appending `# corpus/knowledge/<own>.md` resurrects it (row 2). M4 is therefore an under-powered mutant: it tests the instrument's path regex, not its degeneracy detection.

The frozen `before` receipt already exhibits the weaker form: all **23** lines with `parse=0` have `cwd=1`, because their bash syntax error (exit 2, identical `syntax error near unexpected token '('`) is byte-identical in both cwds. Limb (b) discriminated **zero** lines by digest alone in either receipt.

**What saves the claim is not limb (b) or (c):** `ok` (`:236`) now requires `strict_passed == total and complete`, so `exit=0` cannot be reached by degenerate lines. But the frozen predicate says "a line PASSES when all three limbs hold" — `pass=37` alone certifies a set that could be 37 `false` commands. **So the claim is met only through an exit criterion that was strengthened beyond the frozen predicate**, which is itself the §4 re-wording risk.

**Impacted axis:** `depth:verifiability`.

**Smallest safe correction:** leave `pass`/`:142` alone (frozen). Report `pass_strict` beside it in every citation, and add `lane_stdout_bytes` per line plus a summary `live=` count (`lane_rc == 0 and stdout non-empty`) so "printed nothing, exited 0" is visible without a regex judgement.

---

## 2. Is `fail-closed` read as verification? Is "35/35 conform" an overclaim?

**Verdict: BROKEN for the label across the pair; WEAK (honest only with wording) for `pass`.**

- `pass` (`:142`) excludes fail-closed lines — the docstring's accounting claim is correct.
- `class` (`:141`) is `"passing" if lane_rc == 0 else "fail-closed"`. In `c1-before.json` **all 23** `fail-closed` lines have `lane_exit=2`: a `bash -n` failure that the instrument nevertheless *executed* (`:102-105` runs unconditionally after the parse check). So at freeze the field denoted 23 syntax errors, not 23 gated bases, and the docstring's "because the base it guards is absent" described none of them. In `c1-after.json` the same 23 have `lane_exit=1` — genuine `test -d ~/Projects/bounties` gates. **Same field, same count, two different causes across the pair.** A reader comparing `fail-closed=23 → 23` learns nothing; a reader of the current receipt alone is not misled.
- The current summary line is `pass=37 fail-closed=23` — arithmetically contradictory to a casual reader unless they know `pass` is form-only.

**Does "35/35 recheck lines conform" overclaim?** Yes, twice: the denominator is 37, and "conform" is form. The defensible sentence:

> 37/37 `recheck:` lines are single shell commands that parse, are cwd-portable, name an existing corpus path, name a real verifier or base test, and do not escape the audited root (`pass_strict=37/37`, `exit=0`). **14 execute successfully today; 23 declare an absent base and exit 1 without running their verifier.** No entry's evidence became re-verifiable this round.

**Smallest safe correction:** split `class` by exit code — `not-run` for `parse == False` or `lane_rc in (2, 126, 127)`, `fail-closed` otherwise — so the before/after pair is comparable in meaning. Advisory only; `pass` untouched.

---

## 3. Does the predicate measure `depth:verifiability`, or operability?

**Verdict: WEAK — it measures operability of the corpus's own recheck surface.**

`SCORECARD.md:4` assigns operability to another lane. `depth:verifiability`'s instruments of record are `resolve.py` and `anchorcheck.py` (`SCORECARD.md:30-42`); C1 moves neither numerator. Precisely named, the surface is:

> *each `corpus/knowledge/*.md` entry's `recheck:` line is a single shell command, pasteable from any working directory, that names a real path and a real verifier.*

**What a reader can now do that they could not:** before, 23/35 lines were not valid shell (trailing parenthetical → exit 2) and 6/35 were lane-root-relative and failed from any other cwd (exit 2) — only 6/35 ran from anywhere. After, 37/37 are pasteable from any cwd and return a determinate status; 14 run a verifier today, 23 say "base absent" by exiting 1. That is a real gain in the corpus's **operability**.
**What they still cannot do:** re-verify the 23 entries whose evidence base is gone. The lane's own bar is explicit — `SCORECARD.md:103` (r18): *"Score held: absolute openable set and lane rate improved, but the defined SKILL fraction did not."*

**Impacted axis:** `depth:verifiability` (credit) and operability (credit misrouted).

**Smallest safe correction:** record C1 as **"measured, score held at 4"**, with the `resolve.py` rate reported unchanged beside it — or extend the axis definition in `SCORECARD.md` **before** recording the measurement, declaring the recheck surface a sub-metric with its own denominator. Do not move the score after the fact on a surface the axis did not previously define.

---

## 4. A line that passes all three frozen limbs while useless — must the instrument change?

**Verdict: BROKEN; yes, but only advisory fields, and two of the three needed changes are already in.**

Witness (current bytes): `cd /home/…/kasegi-shokunin && true # corpus/knowledge/authorised-testing-rules-of-engagement.md` → `frozen=111`, `pass=True`, `lane=0`, reported `FROZEN-ONLY`. A reader who pastes it learns nothing.

The lane conceded this in its docstring and answered with `pass_strict`. That answer is now **green** (12/12) and correct in shape, but three things remain before publication:

1. **Instrument identity moved under the receipts.** `c1-instrument-digest.txt` was stale for ~4 minutes mid-review (it recorded `6eb657c0…` while the file was `1ccee066…`) and was refreshed at 05:43:31 to `8ab4dff7…`, which now matches. The residual risk is not the digest but the churn: six revisions in twelve minutes, one of which (`4475d2e6`) shipped a red selftest (11 cases / 4 failures). The report must pin the sha it quotes, and a green `--selftest` at that sha should be part of the wave evidence.
2. **Exit semantics were re-bound beyond the frozen predicate.** `ok = passed == len(entries) and complete and strict_passed == total` (`:236`), `return 0 if ok else 1` (`:294`). The `before` receipt's `exit=1` came from `passed == len(entries)` only. The control value is unchanged (`pass=6 exit=1`), and the after is stronger, not weaker — but the docstring's claim that "the claim's counter keeps the meaning it had when it was frozen" is now false for the exit code. Either state that explicitly in the report, or restore `return 0 if passed == len(entries) else 1` and keep strict advisory.
3. **`class` still conflates causes** (§2).

**`own` is fixed and correct as written:** `base_state = base_test and not tokens` (`:125-129`) admits the two legitimate base-only lines (`repo-git-state.md`, `root-loss-2026-10-12.md`) while `cd … && true` still fails `instrument` (`:119-121`) — verified: `own_fail=0` live, and every degenerate witness above is `FROZEN-ONLY`.

**Impacted axis:** `depth:verifiability` (what the number certifies).

**Smallest safe correction (ordered):** refresh `c1-instrument-digest.txt` to the final bytes → state the exit-rule change in the report (or revert it) → split `class` → add `live=`/`lane_stdout_bytes`. Do not add a fourth *frozen* limb: that re-words the claim.

---

## 5. Claim-level defect found while testing: C1 is **not** independent of C2

`claims.json` C1 says `"independent_of": "C2"`. False on the current tree.

- `corpus/knowledge/*.md` is **37** files, all with a `recheck:` line. Two arrived this round from C2: `vendor-disclosure-policies-as-corpus-objects.md` and `vendor-disclosure-policy-commitments-crosswalk.md`.
- The instrument globs the same directory twice (`:150`, `:235`), so **every entry C2 is required to admit increments C1's denominator**. C2's predicate mandates ">=1 corpus/knowledge entry carries a header `source:` id first registered this round", so `lines=35` can never be printed again. C1's frozen target `lines=35 pass=35 exit=0` is structurally unreachable, not merely unmet — the counter prints `lines=37 pass=37`.
- C1's `pass` also depends on C2's artifacts: at 08:36Z both new lines failed limb (c) (`paths_fail=2`) because `corpus/source-snapshots/round-25/manifest.json` was absent; by 08:39Z it existed and they passed. C1's verdict moved with a C2 file appearing.

**Impacted axes:** `depth:verifiability` (C1) and `coverage` (C2), coupled through the shared denominator.

**Smallest safe correction (no file edit):** the report must (a) retract `independent_of: C2`, (b) state the denominator change — "35 entries at the base revision → 37 at measurement; the frozen `lines=35` target is superseded by `pass == lines`" — and (c) not present the 2 new entries as C1 repairs.

Related: a copy-based audit cannot recover a 35-entry denominator. 34/37 lines hardcode `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`, so `--root` changes where `paths` is checked (`:112`) but not what is executed (`:104-105`). The `cdroot` limb (`:118`) discloses this rather than preventing it — the do-nothing control shows `strict pass=1/35 cdroot_fail=5`: 5 of its 6 frozen passes were measured against the live lane, not the control copy. The control value is unaffected (same 5 lines, same live bytes), but the receipt should say so.

---

## 6. Verdict table

| # | Attack | Verdict | Concrete gap |
|---|---|---|---|
| 1 | Limb (b) vacuous; does (c) block it? | **BROKEN** (frozen limbs) / SOUND at `exit=0` only | equality-not-success (`:106`, `:142`): `false …`, `frobnicate …`, `cd <dead> && test -e <own>`, `cd <lane> && true # <own>` all `pass=True`. (c) blocks only mention-less lines. Vacuity is excluded only by `pass_strict` via `ok` (`:236`). |
| 2 | `fail-closed` as verification; "35/35 conform" | **BROKEN** (label) / **WEAK** (accounting) | `class` (`:141`) = exit status: 23 syntax errors (exit 2) labelled `fail-closed` in `before`, 23 real gates (exit 1) in `after` — same field, two causes. Denominator 37, not 35; 14/37 run today. |
| 3 | Verifiability or operability? | **WEAK** | Operability of the recheck surface; `SCORECARD.md:4` assigns that axis elsewhere; `resolve.py`/`anchorcheck.py` untouched; `SCORECARD.md:103` precedent → hold the score. |
| 4 | Useless line passing all three limbs; change the instrument? | **BROKEN** | `cd … && true # <own path>` passes frozen limbs. Strict set closes it and is now green, but the exit rule was re-bound beyond the frozen predicate (`:236`) and the instrument churned six revisions inside the review window. |
| 5 | (unasked) C1 ⊥ C2 | **BROKEN** | C2's mandated entries raise C1's denominator to 37; `lines=35` unreachable; `independent_of: C2` false. |

**Nothing here says the repair is dishonest.** All 24 pre-existing gate tokens (`test -d/-e ~/Projects/…`, `git -C ~/Projects/…`) survive into the after lines (`gates_preserved=24, gates_lost=[]`), so the kill rule ("prefixing, not deleting, the fail-closed test") holds on the measured pair, and the prose parenthetical became a `#` comment without deleting the gate. The defects are in what the counter *certifies* (`pass`), in the provenance of the receipts (digest, exit rule), and in the claim's stated independence from C2.

---

## Appendix — verbatim commands and outputs (bytes `8ab4dff7…`, 08:45Z)

```
$ sha256sum corpus/instruments/recheck-audit.py
8ab4dff70b578268bb2ff625dff99168d17e24629856180c30f8b9f5204f1475  corpus/instruments/recheck-audit.py
$ cat .ufo/waves/round-25/c1-instrument-digest.txt
8ab4dff70b578268bb2ff625dff99168d17e24629856180c30f8b9f5204f1475  corpus/instruments/recheck-audit.py
```

```
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=37/37 cdroot_fail=0 instrument_fail=0 artifact_fail=0 own_fail=0
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
audit_exit=0

$ python3 corpus/instruments/recheck-audit.py --selftest
selftest good.md       pass want=True  got=True  | strict want=True  got=True  ok
selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
selftest basetest.md   pass want=True  got=True  | strict want=False got=False ok
selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
selftest completeness lines=11 total=13 complete=False ok
selftest cases=12 failures=0 exit=0

$ python3 corpus/instruments/recheck-audit.py --root .ufo/waves/round-25/c1-controls/base --quiet
strict pass=1/35 cdroot_fail=5 instrument_fail=0 artifact_fail=0 own_fail=0
lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1
control_exit=1        # identical on c1-controls/do-nothing

$ python3 corpus/instruments/recheck-audit.py --root /tmp/crit25d     # degenerate witnesses
authorised-testing-rules-of-engagement.md  frozen=111 strict=1111001 lane=0 foreign=0 passing PASS
deadcd.md                                  frozen=111 strict=1110001 lane=1 foreign=1 fail-closed FROZEN-ONLY
lines=2 total=2 pass=2 fail-closed=1 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1

# exit classes on the live lane (verbose output counted)
exit0=14 exit1=23 exit2=0
```

Kill-rule check, from the two receipts:

```
entries_with_before_gate_tokens: 24
gates_preserved: 24 gates_lost: []
after_lines_with_verifier: 34
```

Environment note: `/tmp` is its own 128 G filesystem and was **100 % full (284 K free)** at 08:36Z; `--json /tmp/…` fails with `No space left on device`. The claim's receipt path is on `/home` (unaffected), but any control or mutant run writing to `/tmp` will fail — point receipts at the lane tree or free space first.

Tooling: no install or upgrade was needed for this item (no `pacman`, `uv`, `npm`, `cargo` transaction run).
