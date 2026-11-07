# Draft — round-98 correction sweep (147 → 147 vs 147 → 149; "S140's own class" vs "a superset")

Status: draft only. The lane was not edited. This is the focused sweep for the
round-98 spot-check's routed defect 5
(`corpus/lessons/round-98-verifier-spotcheck.md:39` and `:147`), as it applies
to `SCORECARD.md` and `corpus/lessons/round-98.md` at HEAD `2c2124f`.

## 1. Registry `147 → 147` versus the actual `147 → 149`

Measured with
`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3} \|'`:

| revision | role | rows |
|---|---|---|
| `2133f5bd` | round-98 base | 147 |
| `12bb2f98` | round-98 freeze | 147 |
| `e2caf4a1` | round-98 C2 landing | 147 |
| `e2d3de7b` | round-98 C1 landing | 147 |
| `2790774` | round-98 **integration** | **149** |
| `6195db3` | round-99 base / freeze | 149 |
| `2c2124f` | round-99 HEAD | 150 |

The two new rows are S148 (`docs`, tier A, `mined`) and S149 (`docs`, tier B,
`mined`), both introduced by `2790774`
(`git log --oneline -S '| S148 |' -- corpus/SOURCES.md` and the same for
`| S149 |` print only `2790774`).

**Target sentences.**

- `corpus/lessons/round-98.md:55` — `Registry 147 → 147 rows:` (the Gate's
  own count, measured before the integration).
- `SCORECARD.md:3405` — `- **Sources:** registry 147 → 147 (no new row); S140
  and S144 re-opened, `used-by` extended on both; ...`

**Correction (exact wording).** The landing commits were `147 → 147`; the
round's integration commit `2790774` added S148 and S149, so the round closed
at **149**. The SCORECARD bullet's parenthetical `(no new row)` is false at
the round's close; the lesson's `147 → 147` is true only for the landing and
must say so.

## 2. "S140's own class" versus "a superset"

**Target sentences.**

- `SCORECARD.md:3396` (round-98 C2 row) — `the five shapes widened to S140's
  punct/space/EOL class`.
- `corpus/lessons/round-98.md:75` (Learning) — `published shapes and restores
  S140's own right boundary on five shapes`.

**Erratum (verbatim, `.ufo/waves/round-98/claims.json`, C2 `erratum`).**

> The statement's clause "S140's own punct/space/EOL right boundary
> `(?![A-Za-z0-9])`" is false as an equality: `(?![A-Za-z0-9])` is a strict
> superset of S140's `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` — it also
> accepts every non-ASCII byte and every non-whitespace C0 control plus DEL
> (156 of 256 right-boundary bytes; ReviewC2Scanner F1, CriticClaimsC2 §6.1).
> The regex is kept because the superset never refuses a token S140 would
> report; the three committed sites that called it S140's class are reworded to
> "a superset of S140's punct/space/EOL class" in the post-landing corrections
> commit. No regex changed, so the landing instrument at `e2caf4a1` keeps the
> pinned sha256 `45f8d226…`; the tip's instrument differs only in docstrings
> and comments (the `\-` …).

Independent witness (Python, `re`): `(?![A-Za-z0-9])` matches `é`, `Ω`,
`\x00` and `中`, none of which S140's punct/space/blank/EOL class matches;
therefore the widened boundary is a strict superset, not the class. The regex
is unchanged; only the wording is corrected.

**Correction (exact wording).** Replace the equality wording with: "the five
shapes widened to a **superset** of S140's punct/space/EOL class
(`(?![A-Za-z0-9])`; the claim's C2 erratum records the strict-superset proof
and the 156/256 boundary-byte count)". The `## Learning` sentence becomes
"restores a **superset** of S140's own right boundary on five shapes".

## 3. The third sweep item — S140 `used-by`

**Target sentence.** `corpus/lessons/round-98.md:44-47` (Gate): the S140
`used-by` old→new records two added paths
(`gitlab-remaining-token-families.md`, `gitlab-iam-ci-build-and-session-token-shapes.md`).

**Measured cells.**

- `2133f5bd` (base): `corpus/instruments/capture-secret-scan.py`
- `e2caf4a1` (C2 landing): `corpus/instruments/capture-secret-scan.py`
- `2790774` (integration) and `2c2124f` (HEAD):
  `corpus/instruments/capture-secret-scan.py,
  corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md,
  corpus/knowledge/gitlab-remaining-token-families.md,
  corpus/knowledge/gitlab-routable-and-versioned-token-forms.md,
  corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md`

Four paths were added, not two:
`github-refresh-tokens-and-gitlab-jwt-tokens.md` (round-95 entry),
`gitlab-remaining-token-families.md` (round-97 entry),
`gitlab-routable-and-versioned-token-forms.md` (round-96 entry) and
`gitlab-iam-ci-build-and-session-token-shapes.md` (round-98 entry).

## 4. Additional correction found by this audit — the redaction count

The committed appended block's final paragraph says `53 synthetic session
values, one ... marker each`. Measured at HEAD:

- markers: `body-sweep.txt` 8, `final-checks.txt` 12, `matrix-run.txt` 18,
  `matrix.tsv` 19 → **57**;
- the addendum `a3db47e7` adds 57 marker lines and removes 64 64-hex values
  (some lines held two values; only the matched value was replaced);
- line counts are unchanged (23/23, 26/26, 109/109, 451/451);
- `.ufo/waves/round-99/controls/redaction-r99.txt` records **4** lines (the
  first matched line per file), not 57.

Correction: 57 matched values, 57 marker lines; the receipt covers 4 of 57
lines.
