# InstrumentsCounts — D24-2 / D24-3 closure, kasegi round 25 (wave 1)

Seat: `L1Kasegi25.InstrumentsCounts` (writer of `corpus/instruments/README.md` only).
Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Claims touched: C1 (verifiability), C2 (coverage) — no
claim widened, no other file written. No tool installed or upgraded.

## a) The measured assertion count: **76** (README said 62)

Command (run from the lane root, exactly as now embedded in README):

```
python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"
```

Verbatim output: `76` (`rc=0`). The same string was extracted back out of the README line and re-run, so the
documented command is the executed command:

```
$ CMD=$(sed -n '183p' corpus/instruments/README.md | sed -E 's/^ *`(.*)`$/\1/') && bash -c "$CMD"
EXTRACTED: python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"
76
rc=0
```

Independent cross-check against the receipt (`.ufo/waves/round-24/c1-counterA-manifest-receipt.txt`), which
has 95 lines, every one an `OK` line:

```
$ awk '/:sha256 OK/{s++} /:Q[0-9]+ OK/{q++} END{print "sha256="s, "quote_assertions="q, "total="s+q}' .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
sha256=19 quote_assertions=76 total=95
$ wc -l .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
95 .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
```

19 `:sha256` lines + 76 quote assertions = the 95 `OK` lines, and `grep -c ':sha256 OK'` → `19`. The manifest
has `len(d['sources'])` = 19 records, so 76 is the count of committed quote assertions, not of records.

## b) The two edits (`corpus/instruments/README.md` only)

Edit 1 — the count. `62` → `76` on the manifest bullet, with the counting command and its receipt cross-check
appended to that same bullet (no other line of the bullet changed):

```
-- `corpus/source-snapshots/round-24/manifest.json` — 19 captured records, 62
+- `corpus/source-snapshots/round-24/manifest.json` — 19 captured records, 76
   assertions: S001–S015 (the five round-22 Frontier entries) and S032–S035 (the
   round-24 F09 admissions). Every assertion was measured exactly-once in its own
   capture; the checker now prints `occurrences=N` and verifies a declared `anchor`
-  line for non-unique quotes (QUALITY Q9).
+  line for non-unique quotes (QUALITY Q9). Count it from the lane root:
+  `python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"`
+  → `76`, and the round-24 receipt's 95 `OK` lines are 19 `:sha256` plus these 76.
```

Edit 2 — the bound-8 mutant, restated as what was measured (baseline bytes, `ResolverAttack.md:151`:
`| M4 mut-m4-bound8.py | bound 64 → 8 | **4/8, identical receipt** | **24/24** | … | **survives** …`):

```
   **Known limit (R11):** no case has more than four brace alternatives, so a
-  mutant that lowers `brace_expand`'s 64-combination bound to 8 scores 8/8 here and
-  24/24 on the round-23 matrix while flipping real verdicts. Reported, not hidden.
+  mutant that lowers `brace_expand`'s 64-combination bound to 8 flips real verdicts
+  without moving the pass count. Measured: on the **baseline** bytes
+  (`690153ad…`) that mutant scores 4/8 with an identical receipt and 24/24 on the
+  round-23 containment matrix (`ResolverAttack.md:151`); no lane file records it
+  against the landed `db5e0767…` bytes, so 8/8 there is an inference, not a
+  receipt. Reported, not hidden.
```

Byte hashes are the ones the round itself records: baseline
`690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d`
(`.ufo/waves/round-24/wave1/ResolverAttack.md:5,164`), landed `db5e0767…`
(`corpus/lessons/round-24.md:16`). Diff size: **10 insertions, 4 deletions, 2 hunks, 1 file** —
`git diff --numstat -- corpus/instruments/README.md` → `10	4	corpus/instruments/README.md`.

## c) Acceptance

**(a) Only the two edits.** `git diff -U2 -- corpus/instruments/README.md` produces exactly the two hunks
quoted in §b and nothing else (`@@ -157,6 +157,10 @@`, `@@ -172,9 +176,11 @@`).

**(b) The documented command reproduces the number.** `76`, `rc=0`, twice (§a: once standalone, once
extracted from the README line).

**(c) The wrong figures are gone.** Both greps return no lines and exit 1:

```
$ grep -n '62' corpus/instruments/README.md ; echo "exit=$?"
exit=1
$ grep -n '77' corpus/instruments/README.md ; echo "exit=$?"
exit=1
$ grep -c '62' corpus/instruments/README.md   # → 0
$ grep -c '77' corpus/instruments/README.md   # → 0
```

(The only surviving `76` in the file is the corrected count plus an unrelated pre-existing
`~76-col prose vs 150.0` in the density known-limit bullet at line 23, which is not an assertion count.)

## d) The same overstatement elsewhere — reported, not edited

- **`corpus/QUALITY.md:65` (R11) carries the same defect** — do NOT edit from this seat:
  `bound-64→8 **8/8 and 24/24 unchanged**`. The measured receipt is `4/8, identical receipt` + `24/24` on the
  baseline bytes (`ResolverAttack.md:151`). Suggested wording for the QUALITY owner: "bound-64→8 **4/8
  identical receipt and 24/24 on the baseline bytes** (`ResolverAttack.md:151`); 8/8 on the landed
  `db5e0767…` bytes is an inference, never measured."
- Same mutant overstatement, other owners: `SCORECARD.md:500` — "64-combination bound to 8 scores `8/8` on the
  dispatch matrix and `24/24` on the …"; `corpus/lessons/round-24.md:186-187` — "scores **8/8** on the dispatch
  matrix and **24/24** on the containment matrix".
- Same wrong count, other owners: `SCORECARD.md:510` — "(19 records, 77 assertions, exit 0)";
  `corpus/lessons/round-24.md:77` — "`source-recheck.py` exits 0 over 19 records / 77 assertions." Both should
  read 76; the round-24 verifier spotcheck already states the correct arithmetic at
  `corpus/lessons/round-24-verifier-spotcheck.md:65` — "95 `OK` lines = 19 `:sha256` + 76 assertions".
  `corpus/QUALITY.md` was unmodified in the worktree when checked (`git status --porcelain -- corpus/QUALITY.md`
  empty), so its R11 line is the committed text.

## Risks and limits

- **Residual cross-file disagreement.** `corpus/instruments/README.md` now says 76; `SCORECARD.md:510` and
  `corpus/lessons/round-24.md:77` still say 77, and `SCORECARD.md:500` / `QUALITY.md:65` /
  `corpus/lessons/round-24.md:186-187` still state the bound-8 mutant as measured 8/8. Those are other seats'
  paths; if they are not corrected this round the lane publishes a count split 76/77 across committed files.
- The `95 OK lines` figure is read from the receipt as committed (`grep -c OK` = 95 = total line count); I did
  not re-run the checker against the captures, so the receipt is quoted, not re-derived.
- Nothing installed (no pacman/uv/npx/cargo transaction). No VCS write; no background job; no spawn.
