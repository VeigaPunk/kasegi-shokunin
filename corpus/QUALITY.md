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
