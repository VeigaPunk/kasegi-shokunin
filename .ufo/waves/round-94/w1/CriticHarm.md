# CriticHarm — round-94 attempt 1, ONE v1 wave, 13 seats

Base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485` · freeze `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3` ·
C1 landing `d51220aeb4a538b7b211bb2629e83210669cd56d` · C2 landing `996460861d4130ddb2da6b7554e905d3e47504a3`
(13 seats: the 13 `Report: .ufo/waves/round-94/w1/<seat>.md` paths in `.ufo/waves/round-94/w1-spec.json`, counted, no other number claimed.)

## Verdict

**One named harm; no claim-level verdict change.** The C2 landing renumbers
`corpus/instruments/capture-secret-scan.py` (+33 lines, 458 → 491) and thereby
mis-points **65 of the 102 full-path citations** that five `corpus/knowledge`
entries make into that file (**35 of 50 distinct cited lines**), including
unqualified verbatim quotes. Neither frozen predicate covers it (C2 P3 fixes the
changed-path set to the scanner plus one SCORECARD row; C1 P3 fixes C1 to the two
knowledge files), and the C1 meter is structurally blind to it — the rate is
**1009/2000 at the C2 tip too**, identical to the C1 landing. So this is a routed
defect on the verifiability surface, not a re-score of C1 or C2. It is already the
assigned target of seat `ReviewC2Scanner` in this wave's spec, so it is reported
here as corroborated harm with independent numbers, not as a duplicate verdict.

Everything else on the harm list re-derived clean.

| # | check | result |
|---|---|---|
| 1 | `git diff --name-only base..tip -- SKILL.md PROVINCE.md SHENEN corpus/README.md AGENTS.md` | **empty, rc 0** |
| 2 | `git rev-parse <rev>:SKILL.md` at base/freeze/C1/C2 | `27f23a93848be29b76992ac35ce423ab9a23c269` ×4 — bytes identical |
| 3 | full-path scanner citations in `corpus/knowledge`, `git grep -oE 'capture-secret-scan\.py:[0-9]+' <rev> -- corpus/knowledge \| wc -l` | **102 at all four revs** |
| 4 | out-of-range citations | **none**: 50 distinct cited lines, max 373, against 458 (base) / 491 (tip) |
| 5 | knowledge meter, own extractor (no counter code) | **1008/1999** base → **1009/2000** C1 landing → 1009/2000 at C2 tip |
| 6 | ten EXCLUDED rows at C1 | **10/10** line byte-identical to base, old key still present on the line |
| 7 | S140 SOURCES row | **11 cells = header's 11**; `tier=A`; `status=queued`; `used-by=—`; no cell dropped |
| 8 | S140 redaction | the redaction receipt lists only snapshot line numbers (85 lines, `rule=gitlab_*`); the SOURCES row keeps all 11 cells; anchors 4, 114, 255 keep their `regex = '''…'''` lines |
| 9 | 19 repoints vs SKILL.md text | **19/19** old anchor pointed at unrelated bytes, new anchor carries the row's literals (1 partial, Q3) |
| 10 | C1 commit path set | exactly the two knowledge files, 17/17 + 1/1 lines, no collateral line |
| 11 | C2 commit path set | exactly `SCORECARD.md` (1/1 line) + `corpus/instruments/capture-secret-scan.py` (46+/13−) |
| 12 | pins | scanner `22ba32d1…beaf`, gate `8b6f8493…c8e6`, candidate row `4f10e273…eed8` — all equal `claims.json` |

## The named harm (C2)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git grep -nE 'capture-secret-scan\.py:[0-9]' dff5a0a01e8aafe6be81f4ee61567745c3c4c485 -- corpus/knowledge
git show dff5a0a01e8aafe6be81f4ee61567745c3c4c485:corpus/instruments/capture-secret-scan.py   # 458 lines
git show 996460861d4130ddb2da6b7554e905d3e47504a3:corpus/instruments/capture-secret-scan.py   # 491 lines
# per cited N: base[N] == tip[N]?
```

Result: divergence starts at line 98 (the `gitlab-pat` docstring gains the round-94
custom-prefix sentence) and accumulates through later insertions, so the shift is
not a constant. 65 tokens / 35 lines now point at other text:

| entry | drifted tokens |
|---|---|
| `github-prefixed-tokens-in-captured-evidence.md` | 23 of 39 |
| `capture-intake-gate.md` | 15 of 20 |
| `cloud-signed-url-credentials-in-captured-evidence.md` | 15 of 24 |
| `cloud-signed-cookies-and-user-bound-sas.md` | 11 of 16 |
| `presigned-url-credentials-in-captured-evidence.md` | 1 of 3 |

Two concrete counterexamples (both clean at base, both false at tip):

- `capture-intake-gate.md:69,71` quote **unqualified** —
  `> "A row binds one exact matched value at one path…" — capture-secret-scan.py:122-123`
  and `> "Rows for aws-sts-session-token are refused" — …:123`. At base, lines
  122–123 are exactly those sentences; at tip they are 141–143, and 122–123 are
  the `Known limits` prose. No "round-NN text" marker on either quote.
- `github-prefixed-tokens-in-captured-evidence.md:106` quotes
  `> "Known limits: fine-grained github_pat_ tokens…"` at `:106`-derived anchors;
  base line 106 **is** the `Known limits:` line, tip line 106 is the new
  custom-prefix sentence and the limits list moved to 120.

Only **two blocks** in the whole set carry a round marker — `capture-intake-gate.md:107`
("`…:106-115`, round-93 text") and
`cloud-signed-url-credentials-in-captured-evidence.md:79` ("round-91 text") — which
keeps those two *interpretable* while leaving the range itself wrong for anyone
who re-checks it. The other three entries quote the scanner verbatim with **no
marker at all**, and every one of those quotes is now false:

- `github-prefixed-tokens-in-captured-evidence.md:106` → `:106-107` (tip: the new
  custom-prefix sentence)
- `github-prefixed-tokens-in-captured-evidence.md:100` → `:359-373` (round-92
  selftest; now 381-395)
- `presigned-url-credentials-in-captured-evidence.md:75` → `:123-124` (now 142-143)
- `cloud-signed-cookies-and-user-bound-sas.md:104` → "verbatim from `:106-115`"
  (now 120-133) and `:102` → `:349-358` (now 371-380)
- `capture-intake-gate.md:73` → `:186-201` (`load_allow`; now 208-223)

`git grep -n 'round-[0-9]* text' corpus/knowledge/{capture-intake-gate,cloud-signed-cookies-and-user-bound-sas,cloud-signed-url-credentials-in-captured-evidence,github-prefixed-tokens-in-captured-evidence,presigned-url-credentials-in-captured-evidence}.md`
returns exactly two lines.

Why the round's own instruments cannot see this: `resolve.py`'s class for
`corpus/instruments/capture-secret-scan.py:NNN` is resolved by **path existence**
only (anchor stripped, file present → `INTERNAL`), so the meter's rate is a token
count and never a line check. Confirmed: `meter.py` at the C2 tip still prints
`1009/2000`. The round-93 integration commit (`a3760ac`) set the lane's own
precedent by re-anchoring five scanner-citing entries in the same commit; the C2
landing did not.

## Token-by-token arithmetic: 1008/1999 → 1009/2000

Own extractor (`meter.py`, fresh implementation of the documented path-like rule
and the three resolution domains; no counter code imported). Base token set 1999,
after-C1 token set 2000; shared tokens: **0** changed class.

- **15 distinct tokens leave** (every one was live `INTERNAL`, because `SKILL.md`
  exists in the tree and the line number is never consulted):
  `:526` (rows 143+151, 2 occurrences = 1 token), `:14-15` (153), `:90-91` (220),
  `:94-95` (267), `:498` (310), `:499` (311), `:500-501` (312), `:502` (313),
  `:111-112` (374), `:525` (rows 390+394, 2 occurrences = 1 token), `:146` (397),
  `:246` (397), `:115` (446), `:113-117` (460), `:1163` (ledger 156).
- **16 distinct tokens enter**, all live: `:251-253`, `:264-266`, `:157-158`,
  `:161-162`, `:828`, `:829`, `:830-831`, `:832`, `:999`, `:910-913`, `:321-324`,
  `:340-346`, `:224-226`, `:331-335`, `:184-187`, `:1164`.
- 19 rows do not give 19 − 19 because four rows are token-neutral or shared:
  `:522` (row 355) survives at `triage-thresholds.md:356` (an EXCLUDED row), so it
  is neither removed nor added; `:191` (row 460) already exists at base
  (`triage-thresholds.md:144`), so the repoint adds no new token;
  `SKILL.md:146, 245-247` (row 459, old side) is not `pathlike` (space, no `/`), so
  its removal is invisible; and its replacement `SKILL.md:224-226,335-338` is also
  not `pathlike` (no space, no `/`, no trailing anchor), so it never enters.
- Therefore **1999 − 15 + 16 = 2000** and **1008 − 15 + 16 = 1009**. The movement
  is real token churn (16 new anchors replace 15 retired ones), and it is
  *not* evidence that 19 anchors became verifiable — the meter cannot tell a
  correct line from a wrong one (see Q1).

## Qualifiers (disclosed limits, not harm)

- **Q1 — the meter is line-blind by construction.** `SKILL.md:NNN` classifies
  `INTERNAL` on file existence; a repoint from a dead line to a correct one and a
  repoint from a dead line to another dead line score identically. The measured
  +1/+1 is a token-set delta, so C1's "verifiability" gain rests on the anchor
  re-derivation (check 9), not on the meter.
- **Q2 — S140 stays `queued`, `used-by=—` at HEAD** although the landed scanner
  mines it (docstring lines 4/114/255) and C2's claim is sourced to S140. The
  round-93 precedent flipped S139 to `mined` inside the integration commit; the
  round-94 bullet in `corpus/SOURCES.md` ("Registry 140 rows before the
  integration status …") describes that flip as pending, and the uncommitted
  integrator diff in the working tree currently adds S141 without flipping S140.
  Bookkeeping, outside both predicates — but it must land, or the registry claims
  the source is unmined while an instrument is mined from it.
- **Q3 — one repoint is only half-supported.** Row
  `triage-thresholds.md:151` ("grid/session `SESSION='ufo_sighting'`,
  `GRID='formation'`") now cites `SKILL.md:251-253`, which gives
  `ufo_sighting:fleet-grid` and 2 h leases — the session literal is supported, the
  window literal is `fleet-grid`, not `formation`. Strictly better than the dead
  `:526` anchor it replaced (park-disposition prose), not a full binding of the
  GRID half.
- **Q4 — this wave's working tree is live.** `corpus/SOURCES.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-94.md` and
  `.ufo/waves/round-94/controls/r145-*` are modified/untracked by siblings while
  this seat ran; every number here is pinned to the four commits above, not to the
  worktree.

## Smallest safe correction (for the integrator, not applied by this seat)

Re-anchor the five entries mechanically with `.ufo/waves/round-94/w1/CriticHarm-receipts/scanner-cite-drift.tsv`
(35 `old → new` pairs, each old line's content now at exactly one new line, no
ambiguity), and — since this is the second consecutive round in which a scanner
edit moved them — cite the `Known limits` block and the selftest block by name
instead of by line, so the next landing cannot rot them. Do not widen the C2
predicate for this; it is a knowledge-layer repair, not a claim limb.

## Receipts

`.ufo/waves/round-94/w1/CriticHarm-receipts/` (every command output cited above):

- `commands.txt` — the 18 commands, their observed rc/counts
- `governance-diff.txt` — empty diff for the governance set; SKILL.md blob ×4
- `scanner-cite-count.txt` — 102 citations at four revs; 458/491 line lengths; 50 distinct, max 373
- `per-file-drift.txt` — 65/102 tokens, 35/50 lines, per entry
- `scanner-cite-drift.tsv` — the 35 `base_line → tip_line` pairs with base-line content
- `meter-recount.txt` — own extractor: 1008/1999 and 1009/2000, 15 out / 16 in / 0 flips, token lists
- `meter-at-tip.txt` — 1009/2000 at the C2 landing (meter blind to the drift)
- `excluded-rows.txt` — 10/10 unchanged with old key present
- `sources-and-redaction.txt` — 11/11/11 cells, `tier=A status=queued used-by=—`, redaction receipt (85 lines), S140 anchors 4/114/255
- `anchor-repoint-verify.txt` — all 19 map rows, old-anchor text vs new-anchor text
- `c1-c2-scope.txt` — numstat/hunks for both landings; candidate-row digest
- `commit-file-sets.txt` — `--name-status` for freeze, C1, C2
- `sha-and-patterns.txt` — instrument/gate digests and `_GL_LB`/`_GL_PREFIX`/three pattern lines
- `round-markers.txt` — the two round markers in the five entries (`lines=2`)

No mutating git/jj command was run; no file outside this report, its receipts dir
and the seat scratch was written; no tool was installed; scratch removed on exit.
