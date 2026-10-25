# QUALITY — kasegi admission bar (round 22, first mint)

Thin by design: every criterion exists because the lane already failed it once.
Each cites the mined mistake in `corpus/lessons/round-22.md` § Mistakes
(ids M1–M16 from the kaika W1 STATE dossier §4, A1–A10 from the lane's own
`SKILL.md` disclosure anti-patterns) and, where one exists, the earlier lesson
that recorded it. Source tiers are defined in `corpus/SOURCES.md` (contract v1);
the research method is chousa's — this file duplicates neither.

## Entry criteria — a corpus/knowledge entry is admitted only if all hold

| id | criterion | grounded in |
|---|---|---|
| Q1 | Opens, directly under its H1 title, with three header lines: `source:` (an `S###` row id, its URL or own-work path, and an exact anchor), `verified-at:` (ISO date the author re-opened it), `recheck:` (date or cadence plus the runnable command or URL anchor that re-verifies it, failing closed when the base is absent). | M16 — provenance fields never written, 0/25 entries |
| Q2 | Every load-bearing claim rests on ≥1 tier-A or tier-B row for that claim's scope, opened in the admitting round; a tier-C row is never sole support. | M16; A5 — historical tags treated as current authority |
| Q3 | Each load-bearing claim carries a verbatim quote of ≤25 words with its exact location (section heading, page, or line plus revision). Numbers are copied from the source, never retyped from memory. | M6 — 480/1506 published, 451/1506 re-derived; M3 — a rejection names its exact location |
| Q4 | Attribution is kept: a policy, vendor report or single-program rule is stated as that party's position ("Project Zero's policy", "Anthropic reports"), never generalized into a universal rule; self-reported results are labelled first-party. | A7 — claiming safe harbor a program does not grant; A6 — an empty in_scope_assets observation overclaimed as "no scope" |
| Q5 | States at least one falsifiable rule a reader can check against a report or package, and at least one rejected over-generalization with its reason. | M3 — critic falsification rejected only with evidence and sweep; A8 — manufactured findings |
| Q6 | Documentation-only: never instructs probing, scanning, logging in to, or submitting against any target; carries no credential material, session or private URL, or vault-reference URI (the op-scheme form). | A3 — an absolute "no live host contacted" claim contradicted by recorded GET/HEAD; `PROVINCE.md` refuses out-of-scope action |

Legacy entries (the 25 admitted before round 22) carry the same three header lines
as provenance disclosure, not re-admission, in an appended `## Provenance (round-22
correction, appended)` block at the end of the file — never inserted at the top, so
every existing line anchor into them stays valid. Their `source:` names the lost-tree
or lane base in plain text, and `recheck:` is a fail-closed command that cannot pass
until the base is restored.

An entry failing any of Q1–Q6 is **rejected**, and the rejection is kept in
that round's lesson with the failing criterion — a rejection is evidence of taste.

## Record criteria — ledgers, lessons, instruments and reports

| id | criterion | grounded in |
|---|---|---|
| R1 | A sentence asserting a tree, path or service is live carries an as-of date and its `test -e` result; absent bases are marked `[lost-base]` or historical. | M10 — `corpus/lessons/round-20-recensus.md` audit erratum: 22 live dead-path lines |
| R2 | Self-description is a claim: a rate cites its census file, a `$VARIABLE` cites the code that reads it, a deletion count cites the command. | M11 — `corpus/lessons/round-20-recensus.md` (stale rates, unread `$UFO_SRC`, unreproducible 50) |
| R3 | An instrument verdict names its matcher and definition; "frozen" names both byte inputs and the filesystem definition, and replays publish every divergent definition. | M7 — resolver ingested its own census; M13 — `corpus/lessons/round-21-routing-blocked.md` (32/506 vs 33/506 vs 31/506) |
| R4 | A round counts only with a resolvable work commit (`git cat-file -e`) and a before→after measurement; a rendered wave is not execution and a marker is not a round. | M1 — 273 B r16 marker; M2 — dead hash, report-before-commit; M12 — `corpus/lessons/round-21-routing-blocked.md` (0 of 32 dispatched) |
| R5 | A round without a lesson is recorded as a named omission in the next lesson. | M14 — no lessons for rounds 2, 16, 18, 19 |
| R6 | An edit to a file that other files cite by line number keeps every existing line at its number (append at the end, or a same-line suffix); anchorcheck before/after prints the same cited source lines. | M17 — r22 inserted provenance headers at line 2 of 25 legacy entries, shifting ~160 path:line anchors (e.g. SKILL.md:821) by +3 until L1 caught it pre-commit |

## Round-23 verifier-disagreement criteria

These supplement rather than rewrite Q1–Q6 and R1–R6.

| id | criterion | grounded in |
|---|---|---|
| Q7 | An executable recheck field contains a command, not prose beginning “On each”. Its successful output names what was checked: a pinned captured-source comparison is not a fresh network verification. At least one missing/corrupted-source control must fail. | `corpus/lessons/round-23.md` M2; the r22 verifier found five admitted entries' prose rechecks exit 2. |
| R7 | Freeze an axis claim against its registered detector before implementation. A provenance/header count cannot stand in for citation resolution; instrument-correctness claims must change and exercise the actual detector, report semantic before→after cases, and disclose unchanged source-availability scores. | `corpus/lessons/round-23.md` M1; r22 C1 rejected because `resolve.py` and `anchorcheck.py` were unchanged. |
| R8 | Source rows' immutable fields stay immutable: a corrected anchor or broadened scope in a registry row is a new row beginning “supersedes S### —”. A wrong quote location in a filed lesson is instead an appended R9 erratum, not duplicate source authority. Log every status/recheck/used-by old→new change. | `corpus/lessons/round-23.md` M5; S006's row and entry were already correct, but its r22 Gate location was wrong. |
| R9 | A numerical erratum names its base and changed-file scope; line pointers are re-opened against the cited revision. Append the correction to historical lessons/logs rather than silently rewriting their filed assertions. | `corpus/lessons/round-23.md` M3/M4; r22 stale lesson pointers and deletion tally 22 versus 32. |

## Round-23 additions — captured-source comparison

| id | criterion | grounded in |
|---|---|---|
| Q8 | A captured-source assertion is compared under a declared normalization (capture markup such as `<u>…</u>` stripped, whitespace collapsed) and the receipt names the transformation it applied (`normalized=markup-whitespace`); an entry never has to quote converter markup to pass, and an unnormalized substring match is not the only binding. | `considerthese/2026-10-24.md` proposals 1 and 2 (2026-10-24); `corpus/lessons/round-23.md` M8 and M15 — the `<u>` case passed only while the entry quoted tags, and a non-unique phrase passed an incident-only capture. |
| R10 | A fixture matrix is evidence only for the bytes it actually exercises: an escape class reached by a code path the matrix never enters (an absolute spelling, an expansion branch, a bare-root citation) is unpinned, and the matrix note must say which spellings it does and does not cover. | `corpus/lessons/round-23.md` M17; falsify seats `AddHocAbsForm` (absolute arm) and `MatrixFreezeOrder` (expansion branch) — both mutants passed the 13-case matrix unchanged. |

## Round-24 additions — assertion binding and counter discrimination

| id | criterion | grounded in |
|---|---|---|
| Q9 | A captured-source assertion binds three things: the record's `path` stem equals its `id`, the quote is exactly-once in the capture (or carries an `anchor` line number the instrument verifies), and the check prints the occurrence count it observed. `location` is documentation the instrument does not read, so a quote that occurs twice must carry the anchor. | `considerthese/2026-10-24.md` proposal 1's unlanded conjunct; r24 wave-1 mutant seats forged an S001 record pointing at `S018.txt` with a `" "` quote (exit 0) and a `location: page 99, rule 99.9.9` that no code reads — both filed as controls in `corpus/lessons/round-24.md` § Mistakes. |
| R11 | A counter's instrument is part of the claim: the round publishes its discrimination against degenerate and mutated instruments, not only its pass count. A matrix that a bound-8 brace mutant passes identically to the real fix proves the matrix does not exercise that bound — say so in the receipt. | r24 `ResolverAttack` measured always-GONE 1/8 and always-RESOLVES 0/8; bound-64→8 scored 4/8 on baseline bytes `690153ad…` (receipt `ResolverAttack.md` §F4 M4), and round 25 re-measured the landed-byte mutant `88122e10…` at 8/8 dispatch, 24/24 containment (`.ufo/waves/round-25/d24-3/receipt.txt`). No case in either matrix has more than four brace alternatives; source-recheck semantics changed mid-round under its own before-receipt. |
| R12 | A recheck line is measured against the entry that owns it: its `--source` ids must cover the entry's header `source:` ids and be cited by the entry, and the named manifest must list them. A line pointing at another entry's capture, at `true`, or at `--selftest` is not a recheck. | r24 wave-1 reviewers reached 3/8 → 8/8 by pointing all eight Frontier entries at `--source S018` with no new capture; the harness `corpus/instruments/frontier-recheck-count.py` is the fix and carries the four controls as code. |

## Round-25 additions — recheck-line form and vendor-policy admission

The vendor-policy surface is measured under C2 (frontier rows plus a source first
registered this round), not by a new criterion here; Q4 already forbids generalizing
a vendor's policy into a universal rule.

| id | criterion | grounded in |
|---|---|---|
| Q10 | A `recheck:` line is one executable command: it parses under `bash -n`, carries its own `cd <lane-root> &&` prefix so it runs from any cwd, and keeps any human note after a `#`. A prose sentence with a command appended, or a command that only resolves from the lane root, is not a recheck. | D24-5 — 5 of 35 lines carried the prefix, so a cold run from another cwd still exits 2 (`corpus/lessons/round-24-verifier-spotcheck.md` §6); round-25 measured 29/35 non-conforming — 23 prose+command hybrids fail `bash -n` and 6 are cwd-dependent (lane exit 0, foreign exit 2) — `.ufo/waves/round-25/c1-before.json` (`lines=35 pass=6 fail-closed=23`, `failing_limbs parse=23 cwd=6`). |
| R13 | A counter's before and after are produced by one frozen instrument whose limbs are each shown load-bearing by an isolating fixture — a fixture that fails exactly that limb and no other. A discrimination figure (a mutant's score) is a measurement, not a construction: if it was not run on the landed bytes, the receipt says so. An unchanged or vacuous instrument is never cited as the fix. | R11; `corpus/lessons/round-24-verifier-spotcheck.md` §6 D24-3 — the bound-64→8 mutant's `8/8` was stated as measured in `README.md:159`, `SCORECARD.md:502` and the round-24 report while only the baseline `4/8` was measured (R11 carried the same overstatement until round 25 corrected it in place); `corpus/lessons/round-23.md` M10 — a `mirror=0` host left the guard's verdict structurally incapable of changing. Specimen: `python3 corpus/instruments/recheck-audit.py --selftest` → `selftest cases=4 failures=0 exit=0`, where `cwd.md` isolates `cwd` and `ghost.md` isolates `paths`; `prose.md` fails `parse` and `paths` together, so a `parse`-only fixture (a syntax error that still names an existing `corpus/` path) is the selftest's remaining gap. |

## Round-28 additions — wave-evidence economy

| id | criterion | grounded in |
|---|---|---|
| R14 | Wave evidence is receipts and digests in git: a control/fixture tree larger than a few hundred kilobytes is committed as one content-addressed tarball (sha256 in the receipt) or regenerated from `git archive <rev>` plus a named mutation script, never as a full corpus copy; per-round repo growth is measurable from committed bytes. | considerthese/2026-10-25.md proposal 1 (2026-10-25); round-25 verifier spotcheck §bloat finding (98261eb +850,085 lines; ~65 MB under .ufo/waves/round-25/) |
