# QualityCriteria — round-25 admission-bar criteria (kasegi, wave 1)

Seat: `L1Kasegi25.QualityCriteria` (scribe). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Sole writer of `corpus/QUALITY.md`.
No VCS write performed (only read-only `git show` / `git diff` / `git grep` / `git status`).

## 1. Behavior delivered

`corpus/QUALITY.md` (77 lines after the edit) gained, appended after the R12 row:

```
## Round-25 additions — recheck-line form and vendor-policy admission

The vendor-policy surface is measured under C2 (frontier rows plus a source first
registered this round), not by a new criterion here; Q4 already forbids generalizing
a vendor's policy into a universal rule.

| id | criterion | grounded in |
|---|---|---|
| Q10 | ... |
| R13 | ... |
```

* **Q10** (entry bar, next free Q-id after Q9): a `recheck:` line is ONE executable command —
  parses under `bash -n`, carries its own `cd <lane-root> &&` prefix so it runs from any cwd,
  keeps a human note after `#`. Grounded in D24-5 (5 of 35 lines prefixed) and the round's
  measured 29/35 non-conforming (23 parse failures + 6 cwd-dependent), receipt
  `.ufo/waves/round-25/c1-before.json`.
* **R13** (record bar, next free R-id after R12): a counter's before/after come from one frozen
  instrument whose limbs are each shown load-bearing by an isolating fixture; a discrimination
  figure is a measurement, not a construction; an unchanged or vacuous instrument is never
  cited as the fix. Grounded in R11, D24-3, `corpus/lessons/round-23.md` M10, and the
  round-25 `recheck-audit.py --selftest` specimen (with its measured residual gap, §4 F1).
* **No third (vendor-policy) criterion minted.** Decision and measurements in §4 F3.
* Two rows added, so `grep -cE '^\| [QR][0-9]+ '` moved 21 → 23.

## 2. Acceptance gates

### (a) insertions only, 0 deletions — append step

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat -- corpus/QUALITY.md
 corpus/QUALITY.md | 11 +++++++++++
 1 file changed, 11 insertions(+)
$ git diff --numstat -- corpus/QUALITY.md
11	0	corpus/QUALITY.md
```

Measured immediately after the append and **before** the D24-3 correction the parent ordered
(§3). After that correction the same command reads:

```
 corpus/QUALITY.md | 13 ++++++++++++-
 1 file changed, 12 insertions(+), 1 deletion(-)
12	1	corpus/QUALITY.md
$ git diff -U0 -- corpus/QUALITY.md | grep -E '^@@'
@@ -65 +65 @@ These supplement rather than rewrite Q1–Q6 and R1–R6.
@@ -66,0 +67,11 @@ These supplement rather than rewrite Q1–Q6 and R1–R6.
```

i.e. exactly two hunks: one existing line replaced **in place** (line 65, R11 — R6 same-line
form, the row keeps its id and line number), and 11 lines appended after line 66. No line
moved: R11 is still line 65, R12 still 66, the new section starts at 68.

### (b) every cited path exists

```
$ for p in .ufo/waves/round-25/c1-before.json corpus/lessons/round-24-verifier-spotcheck.md \
           corpus/lessons/round-23.md corpus/instruments/recheck-audit.py \
           .ufo/waves/round-24/wave1/ResolverAttack.md; do test -e "$p" && echo "OK   $p" || echo "MISS $p"; done
OK   .ufo/waves/round-25/c1-before.json
OK   corpus/lessons/round-24-verifier-spotcheck.md
OK   corpus/lessons/round-23.md
OK   corpus/instruments/recheck-audit.py
OK   .ufo/waves/round-24/wave1/ResolverAttack.md
```

### (c) row count increased by exactly the rows added

```
$ grep -cE '^\| [QR][0-9]+ ' corpus/QUALITY.md
23
$ git show HEAD:corpus/QUALITY.md | grep -cE '^\| [QR][0-9]+ '
21
```

### (d) R6 — existing lines kept at their numbers

```
$ git show HEAD:corpus/QUALITY.md | diff - <(sed -n '1,66p' corpus/QUALITY.md) && echo 'first 66 lines byte-identical'
first 66 lines byte-identical          # ran before the D24-3 correction
```

After the correction, `git diff -U0` shows the only pre-existing line touched is 65 itself
(§2a), which is the correction the parent ordered.

## 3. D24-3 in-place correction (parent instruction, supersedes the append-only reading)

One existing cell changed at `corpus/QUALITY.md:65`, R11's grounding column:

* **before:** `bound-64→8 **8/8 and 24/24 unchanged**`
* **after:** `bound-64→8 **4/8 with a receipt byte-identical to the baseline** on the base
  `690153ad…` and **24/24** on the round-23 containment matrix
  (`.ufo/waves/round-24/wave1/ResolverAttack.md` §F4 M4; an `8/8` on the landed `db5e0767…`
  bytes is an inference, not a lane measurement)`

Row id, criterion sentence and the remaining clauses are untouched. The measured receipt this
rests on, read verbatim from `.ufo/waves/round-24/wave1/ResolverAttack.md:151`:

```
| M4 `mut-m4-bound8.py` | bound 64 → 8 | **4/8, identical receipt** | **24/24** | `many10/{a01…a09,zzz}/f.md`: `INTERNAL` → **GONE** | **survives the whole lane instrumentation while changing a verdict** |
```

R13's grounding sentence was aligned to the corrected row: it now says the `8/8` was stated as
measured in `README.md:159`, `SCORECARD.md:502` and the round-24 report, and that "R11 carried
the same overstatement until round 25 corrected it in place" — so the file no longer asserts a
false present-tense claim about itself.

The second clause the parent flagged ("no case in either matrix has more than four brace
alternatives") was **left unchanged because it is not wrong**: `ResolverAttack.md` §F3 item 1
states it verbatim ("No frozen case has more than four alternatives, so the matrix is blind to
*any* bound ≥ 2") and repeats it after the mutant table ("no case in either has more than four
brace alternatives"). Nothing else in the file was touched.

## 4. Findings (measured this seat)

**F1 — the round-25 specimen does not yet isolate every limb; the gap is now written into R13.**
`python3 corpus/instruments/recheck-audit.py --selftest` (exit 0) prints:

```
selftest good.md    want=True  got=True  limbs={'parse': True, 'cwd': True, 'paths': True} ok
selftest prose.md   want=False got=False limbs={'parse': False, 'cwd': True, 'paths': False} ok
selftest cwd.md     want=False got=False limbs={'parse': True, 'cwd': False, 'paths': True} ok
selftest ghost.md   want=False got=False limbs={'parse': True, 'cwd': True, 'paths': False} ok
selftest cases=4 failures=0 exit=0
```

`cwd.md` isolates `cwd`, `ghost.md` isolates `paths`, but `prose.md` fails `parse` **and**
`paths` together, so the frozen selftest has no `parse`-only fixture. An ad-hoc probe built on
the same `audit_entry()` (temp root, no lane write) shows such a fixture is constructible and
that all three limbs are individually load-bearing:

```
parseonly.md   limbs={'parse': False, 'cwd': True, 'paths': True} pass=False   # "cd <tmp> && test -e corpus/knowledge/target.md (fails closed today: base absent)"
pathsonly.md   limbs={'parse': True, 'cwd': True, 'paths': False} pass=False
cwdonly.md     limbs={'parse': True, 'cwd': False, 'paths': True} pass=False
```

**F2 — `bash -n` alone does not catch prose.** A metacharacter-free prose sentence parses:
`recheck: cd <tmp> && on-restoration — python3 corpus/instruments/tool.py corpus/knowledge/target.md`
scores `parse=True, cwd=True, paths=True, pass=True`. The corpus's 23 parse failures come from
parentheticals such as `(fails closed today: base absent since 2026-09-28)`, not from the prose
prefix itself. Q10 therefore states exactly the frozen C1 predicate (`bash -n`), and the prose
case is carried by the `paths`/`cwd` limbs and by Q7's semantic test; a verifier should not read
Q10 as "any prose line fails".

**F3 — why no vendor-policy criterion was minted.** Q4 already binds this ground: a vendor
policy "is stated as that party's position … never generalized into a universal rule". The two
round-25 admission drafts (read-only package `/home/vgpnk/Projects/shokuknow/merge/kasegi`,
no campaign tool run there) were measured for a defect that Q4 and R12 do not already cover:

```
$ cd /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge
$ grep -c '^source: ' japanese-vendor-disclosure-policies-2026-10-23.md
4
$ grep '^recheck: ' japanese-vendor-disclosure-policies-2026-10-23.md | grep -o 'https://[^`]*' | wc -l
1
$ grep -c '^source: ' vendor-cvd-policy-crosswalk-2026-10-23.md
1
$ grep -o 'Cisco\|Cybozu\|GMO Pepabo\|Hitachi' vendor-cvd-policy-crosswalk-2026-10-23.md | sort | uniq -c
      8 Cisco
```

So the crosswalk names only Cisco in its body (its "three Japanese vendor rows" sentence carries
no ids), and the Japanese-vendor draft re-opens 1 of its 4 header sources. Both are real, but
both are **unadmitted drafts being rewritten by live C2 seats this wave**, and the nearest bar
for each is already Q4 (attribution) or R12/Q7 (recheck coverage of the entry's own sources).
Minting a row against a moving draft would encode a target the round is still editing and would
duplicate existing rows, against this file's "thin by design" rule. The lane copies landed
untracked while this seat ran and already meet the existing bar without a new row:

```
$ for f in corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md \
           corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md; do
    grep -c '^source: ' "$f"; grep -o '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json' "$f" | wc -l; done
4
1
4
1
```

i.e. 4 header sources each, one cwd-prefixed `source-recheck.py --manifest` command each — Q10
(form) and R12 (own-source coverage) bind them as written. The section's lead sentence records
where the vendor surface is actually measured (C2) instead of asserting a negative.

**F4 — no effect on C1's surface.** `recheck-audit.py` globs `corpus/knowledge/*.md`;
`corpus/QUALITY.md` is outside it, so this edit changes no recheck line and no C1 counter value.
The audit was not re-run for decoration.

**F5 — tooling.** No tool installed or upgraded (nothing was needed); all commands used
`python3`, `git` (read-only) and coreutils already on the host.

## 5. Touched surfaces

* `corpus/QUALITY.md` — 2 appended rows + 3-line section lead + heading/table header; one
  in-place cell correction at line 65 (D24-3, parent-ordered).
* `.ufo/waves/round-25/wave1/QualityCriteria.md` — this report.

Nothing else written. No entry, instrument, lesson, scorecard, claims file, census, or VCS state
was modified; no background job or subagent was started.

## 6. Out of scope (not done, deliberately)

* Q11 (vendor-policy admission row) — see F3.
* `corpus/instruments/recheck-audit.py` — its missing `parse`-only fixture is reported, not
  edited (not this seat's write scope; a mutation/audit seat owns those limbs).
* R11's other clauses — re-measured only; changed only where D24-3 requires.
* Any fix of the 29 non-conforming `recheck:` lines — that is the C1 build work, not the bar.

## 7. Artifacts

* `corpus/QUALITY.md` (edited)
* `.ufo/waves/round-25/wave1/QualityCriteria.md` (this report)
* receipts read, unmodified: `.ufo/waves/round-25/c1-before.json`, `.ufo/waves/round-25/c1-before.txt`,
  `corpus/lessons/round-24-verifier-spotcheck.md`, `corpus/lessons/round-23.md`,
  `corpus/lessons/round-24.md`, `.ufo/waves/round-24/wave1/ResolverAttack.md`,
  `corpus/instruments/recheck-audit.py`
