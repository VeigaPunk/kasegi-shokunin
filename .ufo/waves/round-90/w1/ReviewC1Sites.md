# ReviewC1Sites — round 90, attempt 1, C1 semantic review (v1 wave, 12 seats)

Seat: ReviewC1Sites (leaf, attack/review). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Revs read: base `6088c3eb0c29040415c69e7b5fb91e110480ab26`, freeze
`33f43db99c06e89bb9fb78c538313e9450da649f`, C1 landing
`4a7e676895d3fc74e18c853457c9b465ade2ddf5`; labels (round-89 non-author)
`02b6d88f1c059e2f881fd07c73834f502b4f212d`.

## Scope and method

I judged `git diff 33f43db 4a7e676 -- corpus/knowledge/triage-thresholds.md`
(1 file, 32 insertions / 32 deletions; zero-context diff shows pure token
replacement) against `corpus/knowledge/*.md` extracted at `4a7e676` with
`git archive`. The landing is **34 sites on 32 lines** (lines 261 and 270
each carry two tokens), all in `triage-thresholds.md`. I judged every site
against its new range, judged the 4 frozen exclusions, and labelled the 6
round-91 inputs. Verdicts here are routed qualifiers, not a re-score of the
frozen claims.

## Verdict summary

- **34/34 sites judged: 32 CORRECT (26 exact, 6 partial-support), 2 WRONG, 0 UNCLEAR.**
- WRONG: `triage-thresholds.md:158` and `:439`, both repointed to
  `mission-control.md:61-64` — Finding 1.
- Partial-support (the range states the rule the tie claims, but not the
  row's derived detail; tagged `partial:` in the reason column): lines 264,
  278, 90, 442, 147, 157 — Finding 2.
- Exclusions: **4/4 agree** with the frozen stale/unsupported judgment
  (249, 155, 438 are content-repair; 152 is a split — the 15-min half is
  supportable by L61, the 20000-char tail is not).
- Round-91 labels: 6 rows — **5 content-repair** (457, 141, 142, 226, 368),
  **1 repoint** (454 -> `ev-model.md:13-25`).

## Finding 1 (medium, routed defect): two repoints land a self-contradictory SUPERSEDES tie

Paths: `corpus/knowledge/triage-thresholds.md:158` and `:439` at `4a7e676`.

Evidence at the landing rev: `corpus/knowledge/mission-control.md:61-64`
reads "strict signatures — FOUR, round-13 correction (`usage limit has been
reached`, `usage_limit_reached`, `rate limit exceeded`, `429 Too Many`;
fleet-dispatch.mjs:272)". The landed rows now say:

- line 158: `SUPERSEDES: corpus/knowledge/mission-control.md:61-64 — that
  entry lists 3 signatures, omitting usage_limit_reached`
- line 439: `corpus/knowledge/mission-control.md:61-64 (three signatures)`

Both parentheticals are false at the cited range: L61-64 list four
signatures and include `usage_limit_reached`.

Why every frozen limb still passes: the round-89 label anchored the row's
main statement (four signatures) and returned `61-64` as the supported
range; it never tested the supersedes parenthetical. M4 binds the value to
the label, M9 binds the value to a WRONG label, and M5 checks only that the
range is in bounds — none reads the parenthetical against the cited text.
This is the same defect class the frozen selection used to exclude lines
155/438 ("the SUPERSEDES premise is stale"), but the labels for 158/439 did
not flag it, so the map selected them.

Routed fix (content-repair, not a repoint): strike the supersedes
parenthetical and cite as `MATCHES: corpus/knowledge/mission-control.md:61-64`
(the entry already carries its own round-13 correction), or reword to
"MATCHES ... (entry corrected in round 13; audit-time text said three)".

Re-runnable:
`git show 4a7e676:corpus/knowledge/mission-control.md | sed -n '61,64p'` and
`git show 4a7e676:corpus/knowledge/triage-thresholds.md | sed -n '158p;439p'`.

## Finding 2 (info, round-91 content candidates): partial-support ties

Not defects under the frozen predicate — the range states the rule the
`MATCHES` tie claims — but the row's derived detail is not restated in the
cited range. Candidates for a wording note, not a citation change:

| line | new range | stated | not stated |
|---|---|---|---|
| 264 | claim-gates.md:69 | run-time digest binding | `^[a-f0-9]{64}$` format limb |
| 278 | claim-gates.md:82-85 | global scan, slug / same-title >=16 lowercase | `resolve(dir,'..','..')` root, self-skip, unparseable-skip |
| 90 | intake-surface.md:83-85 | `is_live(1)` | `freshness?.label === 'live'` predicate (definition at intake-surface.md:64-67) |
| 442 | mission-control.md:40 | pane exit -> FAILED, "budget still counts it" | `attempts()` counting `mission_(parked\|failed)`, 2-attempt exhaustion (the row's own tie cell concedes this) |
| 147 | mission-control.md:59-60 | `--models-rr` / `--rr-until` mode | `Date.now() < RR_UNTIL` gate |
| 157 | mission-control.md:64-66 | family regex ANDed with signatures | exact alternation, token-plan branch |

## Exclusions (frozen, 4) — judged

| line | labelled range | judgment | reason / fix |
|---|---|---|---|
| 249 | claim-gates.md:42-47 | **agree** (content-repair) | `claim-gates.md:52-56` documents the blanket symlink ban as a round-13 addition, so the row's "new; regex-only" is stale. Fix: `MATCHES: corpus/knowledge/claim-gates.md:52-56`; drop the clause. |
| 155 | mission-control.md:37-38 | **agree** (content-repair) | `mission-control.md:55-57` already carries `openai-codex/gpt-6-astra:max` with the round-13 correction ("earlier text said `openai-oauth/`"); the SUPERSEDES premise is stale. Fix: `MATCHES: ...:55-57`; drop the supersedes clause. |
| 438 | mission-control.md:37-38 | **agree** (content-repair) | Same as 155 for §9.6. Fix: `:55-57` with the entry's own correction note; drop the `openai-oauth/` premise. |
| 152 | mission-control.md:40-45 | **agree as written** (content-repair) | L61 states the 15-min mtime window; "tail = last 20000 chars" is stated nowhere. A bare repoint cannot fix it. Fix: split — `MATCHES: ...:61` for the window, drop or mark the tail unstated. |

## Round-91 labels (non-author, pre-freeze)

| line | token | label | fix | evidence |
|---|---|---|---|---|
| 457 | `claim-package-contract.md:9-16, 28-38` | content-repair | Replace with `claim-package-contract.md:9-16` (six-file table: L9 header, L10 separator, L11-16 six rows). `28-38` starts on blank L28 and cuts the verdict bullet at L38; if the status.json observed semantics are intended, use `29-54`. | L28 blank; L29 heading; L31-34 state; L35-38 partial verdict bullet |
| 141 | `mission-control.md:13-14` | content-repair | Replace with `—` (no supporting range: the entry names `--max` only as a loop bound at L17, never its default 5). | `--max` occurs only at L17 |
| 142 | `mission-control.md:13-14` | content-repair | Replace with `—` (no supporting range: `STAGGER_S` / 20 s default not stated anywhere). | no STAGGER/stagger/20 s occurrence |
| 226 | `claim-gates.md:29-36` | content-repair | Replace with `—` (no supporting range: the custodian section L29-37 never states the unreadable-file precheck; `readJson` does not occur in the entry). | L29-37 = chain / per-decision / head binding only |
| 368 | `ev-model.md:21-23` | content-repair | Replace with `—` (no supporting range: L22-23 pin only `p_*` to [0,1]; the six cost inputs' `number, unbounded` is not stated; L49-51 names some cost fields, not their type/bounds). | L22-23 pins `p_*` only; L49-51 is a field-name list |
| 454 | `ev-model.md:6-20` | `corpus/knowledge/ev-model.md:13-25` | Repoint the first token to `13-25`: formula L13-19 plus the UNKNOWN fail-closed bullet L24-25; L6-11 is anchor-base prose. | L13-19 formula block; L24-25 UNKNOWN bullet |

## Verifiability checks performed

- Scope: `git diff --stat` = 1 file, 32 insertions / 32 deletions; the
  zero-context diff shows only token replacements on the changed lines.
- Map fidelity: labels at `02b6d88` have 46 rows, 40 WRONG, 2 with no range
  (141, 142), hence 38 WRONG-with-range; minus the 4 frozen exclusions =
  34. The map is exactly that multiset (sorted join equal); 32 distinct
  citing lines.
- Application: for all 34 rows, the new value is present and the old key is
  absent on the citing line at `4a7e676`; the meter's M3 forward
  substitution also passes with `bad_lines=0`.
- Pinned meter, run independently with `--work` in scratch:
  `base=812/1827 after=843/1829`, M0/M1/M3/M4/M5/M6/M9 all pass, map sha256
  `7c420856c3347d362bfc419030aa474cbc253975f3026bc13355b654055fb8b3`,
  rc=0, 11.8 s. Receipt `meter-r90.txt`.
- All 4 excluded sites re-read at landing; the frozen reasons hold as
  stated above.
- Credential pre-scan of the wave receipts with
  `corpus/instruments/capture-secret-scan.py --files`: 5 files, 0 hits,
  rc=0.

## Residual risk and verification gaps

- No live source tree (`lost-tree` / `lost-base`): I judged the corpus
  entries' prose at `4a7e676`, not the lost sources. Finding 1 does not
  depend on the lost tree — it is a contradiction between two landed files.
- The frozen limbs test anchoring, binding, range, map digest and label
  agreement, not whether a supersedes parenthetical is true of the cited
  text. Both WRONG rows pass every frozen limb; a round-91 predicate could
  bind SUPERSEDES parentheticals to the cited range.
- The exact/partial boundary is reviewer judgment; the frozen label rubric
  has no "partial" bucket. Partials are tagged explicitly in the reason
  column.
- Single reviewer, single pass; the labels are non-author but
  single-labeller.

## Files written

- `.ufo/waves/round-90/w1/ReviewC1Sites.md` (this report)
- `.ufo/waves/round-90/w1/ReviewC1Sites-receipts/sites-r90.tsv` (34 rows;
  sha256 `d26050c39f11369a3460ea7b0903fd15e34f0f54f2023fb940325cb847517755`)
- `.ufo/waves/round-90/w1/ReviewC1Sites-receipts/exclusions-r90.tsv` (4 rows;
  sha256 `8a62b5290fdd0955ec2330c9f894901c4a86b7704484fd8df4a62d4499d5e4c8`)
- `.ufo/waves/round-90/w1/ReviewC1Sites-receipts/round91-labels.tsv` (6 rows;
  sha256 `4f3ad6633ce3b24b5ee44e24e8e5d25a77d1b638b0eca7961227cfe27fe65506`)
- `.ufo/waves/round-90/w1/ReviewC1Sites-receipts/meter-r90.txt`
  (sha256 `6430206bf46c949154f670f846da38d85ff15267f4b4169508af21949f4723f2`)
- `.ufo/waves/round-90/w1/ReviewC1Sites-receipts/map-fidelity.txt`
  (sha256 `df977203ad12a6bc0fef0c2e05690fa9cfc865f18a8fd90fbfb48859e4afe084`)

Scratch `/fast/scratch/hyaku/kasegi-r90/ReviewC1Sites` was deleted with
`rm -rf` (trap on exit); it is gone. No tool installs or upgrades; no
network access; no lane/tree writes outside the paths above.
