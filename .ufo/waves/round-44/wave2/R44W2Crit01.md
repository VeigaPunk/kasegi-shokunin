# R44W2Crit01 — claim-wording attack on the two frozen round-44 claims

Seat: R44W2Crit01 (critic, wave 2, falsify). Attacked tree: `8063547d0ce647d6f9eafc3c8d0a502616685218` (= lane HEAD; `git diff --stat 8063547d..HEAD` empty, so every worktree byte I cite is committed at the attacked tree). Frozen base: `5ab3a60` (`5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`). Read-only seat: no production file was edited; all experiments ran on `git archive` exports under scratch. Tooling: nothing installed (system `python3`/`git`/`grep`/`awk` sufficed).

Freeze integrity first: `git log -- .ufo/waves/round-44/claims.json` → exactly one commit (`6631401` "freeze claims"), and `git diff --stat 8063547d -- .ufo/waves/round-44/claims.json` is empty. The claims below are the unedited frozen bytes.

## Headline answer

Neither after-state is ONE concrete value re-derivable with ONE command over committed bytes. Each is a conjunction; the recorded commands cover only part of it.

| claim | conjuncts in `after` | command-backed? | verdict |
|---|---|---|---|
| C1 (claims.json:12) | (a) 0 of 8 unresolved; (b) all eight append-only; (c) ≥1 red-before control per changed gate | (a) yes; (b) no — counter never diffs root vs baseline; (c) no — "changed gate" set undefined | not one value |
| C2 (claims.json:21) | (a) 26 admitted frontier rows; (b) ≥1 newly opened tier-A row cited by a new knowledge entry; (c) 63 knowledge entries; (d) a recorded reject; (e) non-author spot-check; (f) SOURCES census exit 0 | (a) only via a successor instrument the frozen claim does not record (its own recorded counter prints 0 in both worlds); (b) no command recorded (relational join); (c) yes; (d) no command recorded; (e) **absent at the attacked tree**; (f) command lives outside the lane, unrecorded in the claim | not one value |

## C1 — depth:verifiability (claims.json:9-15)

### Conjunct (a): "0 of those same 8 frozen routed defects remain unresolved" — HOLDS, one command, both directions

Re-derived on scratch exports (`git archive 5ab3a60` → `base/`, `git archive 8063547d` → `after/`):

```
python3 after/corpus/instruments/r44-routed-defects.py --root after --baseline base
  → routed-defects total=8 fixed=8 unresolved=0 exit=0 ; baseline total=8 fixed=0 unresolved=8
python3 after/corpus/instruments/r44-routed-defects.py --root base --baseline base
  → total=8 fixed=0 unresolved=8 exit=1     (do-nothing replay cannot report 8 fixed)
```

Kill-rule clause 1 (claims.json:13) verified: base-vs-base exits 1 with all 8 unresolved. The instrument is fail-closed (limb exception → unresolved, `grade()`), and its selftest rejects the marker-only mutants: `--selftest --work <scratch>` → `selftest cases=11 failures=0`. The command enumerates exactly the frozen eight (`TOTAL = 8` hard-coded) — full set of the frozen list, and nothing beyond it by construction.

### Conjunct (b): "all eight have append-only fixes" — TRUE in fact, but NOT re-derivable by the recorded command

`main()` grades `--root` and `--baseline` **independently** and never compares them; no limb diffs the two trees. Append-only is bound in-tree for only 3 of 8 limbs: D1 (round-43 row must still carry `13/19`, correction must sit after it), D2 (K17 must still carry the `claims-erratum` escape), D3 (original "29-character prefix" sentences must survive). For D4–D8 an in-place rewrite of the old bytes would still grade `fixed=8 unresolved=0` — e.g. D6 checks only a trailing `\n\n` and ≥4 boxes in SHONEN.md; D8 never checks the erratum's round-43 bytes.

The property is nonetheless true of the round: `git diff --stat 5ab3a60 8063547d` → `112 files changed, 13952 insertions(+)` with **zero deletions anywhere**, and per-file probes (`git diff … | grep -c '^-[^-]'`) → 0 removed lines for LOG.md, SHONEN.md, SCORECARD.md, corpus/instruments/README.md, claims-erratum-6.md, round-43.md. But that re-derivation is a **second command over git history**, not the claim's counter. Word "proven" (claims.json:12) therefore overclaims: the counter proves conjunct (a) only.

### Conjunct (c): "at least one red-before control per changed gate" — UNFALSIFIABLE as worded

"Changed gate" is never enumerated — not in the claim, not in §6, not in the SCORECARD rows. No command enumerates the set, so the existential ("at least one … per …") has no denominator. Concrete anchors exist (`controls/c1-counter-baseline.txt` = the red-before receipt for the counter itself; `controls/recheck-before.txt`), but the claim does not bind to any enumeration of gates. Also `<frozen-base>` (claims.json:14) is an unbound placeholder — the hash `5ab3a60` is pinned only outside the claim (SCORECARD.md:1718, `c1-do-nothing.txt`), and kill-rule clause 2's "final lane revision" is a moving referent no command can pin at freeze time.

Unfalsifiable/overreaching words, C1 `after` (claims.json:12): **"proven"** (counter covers 1 of 3 conjuncts), **"all … append-only"** (delta property outside the command's reach for 5 of 8 limbs), **"per changed gate"** (undefined set), **"at least one"** (existential over that undefined set). Kill-rule (claims.json:13): **"final lane revision"** (unpinned). Benign: "all eight" as a count over the enumerated §6 list, "actionable" (decorative; §6 fixes the set at 8).

## C2 — coverage (claims.json:18-24)

### The claim's own recorded counter measures nothing (decisive)

claims.json:23 records `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` as the frontier command. Replayed on committed bytes: **0 (exit 1) at base, 0 (exit 1) at the round-44 tree**, while the true status-cell distribution is 25 → 26 admitted (third cell, not second). The claim cannot re-derive even its own before-value (25) with its own recorded command. The committed receipts say the same: `controls/c2-frozen-counter-replay.txt` ("The F-count result is 0 in both states"), `controls/c2-counter-audit.txt` (frozen 0/0; the do-nothing control's double-escaped variant prints whole-file line counts 612/632, not 25/26), `controls/c2-do-nothing.txt` ("Frozen counter in claims.json C2 is not a valid measure").

The successor instrument `corpus/instruments/r44-frontier-count.py` (committed at the attacked tree) does measure the same declared predicate: base → `frontier rows=25 admitted=25`, `--expect 26` → `verdict=SHORT exit=1` (kill-rule clause 1 verified); after → `rows=26 admitted=26 exit=0`; `--ids` → `F01…F26`, 26 distinct ids, all admitted, no duplicates today. But it is **not the command the frozen claim records**; the authoritative binding lives in SCORECARD.md:1719 and the instrument docstring. The claim's `counter` field is dead text, and a closure following claims.json literally gets 0 in both worlds — indistinguishable.

### Conjunct-by-conjunct

- **"26 admitted frontier rows"** — concrete; re-derivable only with the successor instrument above. Full set: the instrument counts every `^\| F\d+ \|` row across the main table (F01–F14) and the appended amendment tables (F15–F26) — the union is the frontier; caveat: it counts rows, not distinct ids, so a duplicated id would double-count silently (no dedup; `--ids` is opt-in).
- **"at least one newly opened tier-A source row cited by a new knowledge entry"** — no command recorded. Three undefined-in-claim qualifiers: "newly opened", "new" (twice), "tier-A" (a SOURCES column convention the claim never states). Referents verified present at the tree: S069 is a new row in the +7-line SOURCES diff, tier cell `A`, status cell `mined`, dated 2026-10-28 (SOURCES.md:75), cited by exactly one knowledge file, `knowledge/google-cloud-vrp-customer-resource-boundary.md`, itself new. Re-derivation needs ≥2 commands plus a cross-file join — none recorded in the claim.
- **"63 knowledge entries"** — HOLDS with the recorded command: `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → 62 at base, 63 after; the dir is flat (0 subdirectories), so the command enumerates the full set. Fragility note: it counts any top-level `.md`, so a future README would pollute it.
- **"a recorded reject"** — "recorded" unbound, no command. Referent present: S070 (SOURCES.md:76) status cell `rejected` with its flip. (The recorded SOURCES command — the second grep in claims.json:23 — works: 68 → 70 rows, verified both exports — but the after-state never states the after-value 70; SCORECARD.md:1713 does.)
- **"non-author admit/reject spot-check"** — **not true at the attacked tree**. `wave1/` holds 55 seat files and none is a non-author spot-check result; only the dispatch `nonauthor-spotcheck-packet.md` exists, and SCORECARD.md:1698 says "no independent nonauthor spot-check". The frozen after-state bundles a wave-2 act as if it were a committed byte. A closure at `8063547d` cannot re-derive this conjunct — the value does not exist there yet. Kill-rule clause "the non-author gate agrees" (claims.json:22) has the same defect: gate and standard unpinned.
- **"SOURCES census validates exit 0"** — the census is a **fleet-root** script, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`, not lane-committed bytes; the claim records no command for it. `controls/census-invocation-error.txt` shows the lane-rooted mis-invocation exits 2 ("config not found … shokunin.conf"), and `controls/sources-census-after.txt` shows exit 0 **with two W04 warning rows** (S028/S029 duplicate URLs) — so "validates" means census-ok-with-warnings, a semantics the claim does not state. A closure holding only the lane export cannot run it.

Unfalsifiable/underbound words, C2 `after` (claims.json:21): **"at least one"** (existential, no recorded enumeration), **"newly opened"**, **"new"** (×2, delta properties with no recorded base-compare command), **"tier-A"** (column convention unstated), **"a recorded reject"** ("recorded" unbound), **"non-author admit/reject spot-check"** (absent at tree), **"SOURCES census validates"** (external script, unrecorded command, exit-0-with-warnings semantics), **"validates"** itself. C2 `before` (claims.json:20): **"public-practice"** (unoperationalized — no recorded command filters for it), "one source-grounded frontier move is absent" (prose, not a value). Kill-rule (claims.json:22): **"the non-author gate agrees"** (unpinned gate, unpinned standard).

## Round-44 SCORECARD rows — three evidence-discipline defects found

1. **Dangling evidence pointer (SCORECARD.md:1712).** The C1 evidence cell cites `.ufo/waves/round-44/controls/c1-counter-at-commit-A.txt`; `git ls-tree -r 8063547d | grep at-commit` → **0 hits**. The receipt does not exist at the attacked tree. The existing receipts are `c1-counter-after.txt` / `c1-counter-baseline.txt`. This is the same class as routed §6.7/§6.8 (pointer/measure mismatch).
2. **Numeral slip (SCORECARD.md:1712).** "the counter's own selftest rejects eleven marker-only mutants, `selftest cases=11 failures=0`" — the run has **11 cases = 1 POSITIVE + 10 mutants** (build_mutants: D1, D2, D3, D4, D5×3, D6, D7, D8). Verified by execution: `selftest cases=11 failures=0`. Eleven mutants is wrong; ten is right. Exactly the prose-numeral class §6.3 routed in round 43.
3. **Fleet-root dependency unstated (SCORECARD.md:1713).** "source census exit 0" is presented as round evidence without noting the census runs from the fleet root with a fleet-root script, or that exit 0 carries two W04 warnings. A lane-export closure cannot reproduce it.

## Smallest safe corrections (wording-level; I edited nothing)

- C1 `after`: split the sentence — "(a) fixed=8/unresolved=0 by the counter; (b) append-only holds for the round diff (13952 insertions, 0 deletions — re-derive with `git diff --numstat 5ab3a60 <final>`), bound in-counter for D1/D2/D3; (c) red-before controls: name the receipts and the gate set they cover." Pin `<frozen-base>` = `5ab3a60a5cb…` and "final lane revision" = the commit hash the wave report will name.
- C2 `after`: state the after SOURCES value (70); bind "tier-A/new/newly/cited-by" to named bytes (S069 row, the knowledge file, base-absence via the SOURCES diff); either drop "non-author admit/reject spot-check" from the frozen after-state or mark it explicitly as a wave-2 completion condition, not an after-state byte; name the census command and its fleet-root cwd, and say exit 0 includes W04 warnings.
- SCORECARD: fix or commit `c1-counter-at-commit-A.txt`; "eleven marker-only mutants" → "ten marker-only mutants (eleven selftest cases incl. the positive)"; note the census's fleet-root basis.
- Keep as-is (verified sound): C1 conjunct (a) and both kill-rule do-nothing behaviors (base→exit 1 unresolved=8; frontier `--expect 26` at base→exit 1); claims.json freeze (one commit, unedited); the successor-instrument binding in SCORECARD.md:1718-1719.

## What I could not check

- Whether a wave-2 non-author spot-check receipt will land and satisfy C2's promissory conjunct (that is this wave's own output; my item is the freeze-time wording, which is defective regardless).
- The content correctness of the S069 source snapshot and knowledge entry beyond the S069 citation link (out of item scope).
- Fleet-root census script internals (read-only fleet scope; only its committed receipts were used).

Evidence commands are quoted inline above; all scratch under `/fast/scratch/hyaku/kasegi-r44/R44W2Crit01/` (removed before yield).

## Worktree drift observed at write time (postscript)

Between my measurement and this file's write, the lane worktree gained untracked in-flight artifacts (not mine): `.ufo/waves/round-44/controls/c1-counter-at-commit-A.txt`, `controls/sources-census-before.txt`, `wave2-dispatch.*`, `wave2.ready*`, and a modified `SCORECARD.md`. Defect 1 above is pinned to the committed tree `8063547d` (`git ls-tree -r` → 0 hits for `at-commit`); the untracked file suggests an in-flight repair, which does not change the finding at the attacked tree but may already resolve it at the final lane revision.
