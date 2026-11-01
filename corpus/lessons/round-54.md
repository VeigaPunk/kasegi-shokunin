# Round 54 — the routed D53 figure corrections (non-claim, carry-in), the move-log figure audit (C1), and the OpenSSF Scorecard check documentation (C2)

Three commits after the freeze (`37fc40e`): the carry-in landed FIRST as a routed non-claim
(`cfdf059` — one appended corrections file for D53-1+D53-2, no filed byte edited; D53-3 routed
operator-side via the L0 channel), then C1 (`c9df68e` — the figure-audit capability on
depth:verifiability) and C2 (`ff5a1bf` — frontier F35, the OpenSSF Scorecard check documentation on
S086). Host unchanged from rounds 50-53 (Windows workspace, `python` 3.13.15, `python3` = Store
stub, no /home, no /fast). The freeze carried the S086 capture + manifest + the extended pre-freeze
screen + the do-nothing/stand-in receipts; every after-literal was dry-run against a stand-in tree
before the freeze, which caught two of this round's own mistakes before any data landed.

## Mistakes

Sweep that found them (paste, per contract): (a) the pre-freeze stand-in dry-runs — the frontier
counter over the base export and over the base+declared-adds stand-in, the `LC_ALL=C sort -c` on
the patched expected list, the recheck-audit expect limb, the source-recheck S086 run and the
capture-binding run (all in `.ufo/waves/round-54/controls/c2-standin-dryrun-r54.txt` and the
freeze commit's receipts); (b) the C1 receipts — the selftest, the red control over the r53
literals AS FILED, and the first green lane run, whose fail-closed read-only limb rejected ledger
entry `knowledge-files` (raw output quoted in the commit message and in the receipt history below);
(c) the routed-defect verification greps (`controls/d53-base-greps-r54.txt`). Six rows, two mined
from the routed carry-in and four caught this round (three before their data landed, one at the round-end census gate):

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| receipt trailer prose kept the draft-run figure (routed D53-1, mined from `corpus/lessons/round-53-verifier-spotcheck.md` §6) | `.ufo/waves/round-53/controls/c2-counter-final-r53.txt:9` says "the 34 inherited recheck-exit-1 entry records" while the same receipt's `:8` prints `FAIL_entry_records=33` (= 37−4; re-derived again this round: 33 at base, 38−5=33 after C2 — invariant) | the routed defect itself; now machine-caught by the round-54 figure-audit ledger entry `fail-entry-records` (want 33) and named in `.ufo/waves/round-54/controls/routed-d53-corrections.md` whose closure check prints `d53-corrections=closed` exit 0 | one appended corrections file superseding the literal (receipt bytes byte-identical, sha `be69ece7…` pinned); R9 class: corrections append, receipts are never rewritten |
| capture metadata figures hand-derived, not command-derived (routed D53-2, same source) | manifest `"lines": 543` + S085 row + F34 entry header vs `wc -l` = 542 over the committed capture (7590 bytes = 7589 content + 1 trailing newline); load-bearing sha/bytes correct | the routed defect; now machine-caught by figure-audit ledger entries `capture-lines-s085` (want 542) and `capture-bytes-s085` (want 7590) | same corrections file, three literals superseded by 542, the three files byte-identical (manifest is committed capture provenance, R20; the registry row is append-only, R8) |
| sorted-list insert positioned by eye, not by sort (own, pre-freeze) | first stand-in build inserted `openssf-scorecard-checks.md` AFTER `operator-queue.md`; `LC_ALL=C sort -c` rejected the position ("disorder: corpus/knowledge/openssf-scorecard-checks.md" — 'openssf' < 'operator' byte-wise); nothing was committed | the R25/R34 stand-in discipline itself — the pre-freeze literal dry-run the round-53 lesson mandated | insert moved BEFORE `operator-queue.md`, `sort -c` clean; rule going forward: a sorted-list insert is verified by `sort -c` on the patched bytes, never by reading the neighbors |
| manifest quote anchor written from memory, not from `grep -nF` (own, pre-freeze) | the S086 manifest's Q2 anchor was first written as 7 ("This page describes…" read as the 7th line); the dry-run `source-recheck` printed `S086:Q2 OK occurrences=1 anchor=7-BROKEN` (true line: 5); caught before any commit | `source-recheck.py`'s anchor limb, working as designed | anchor re-derived with `grep -nF` (→ 5), all 14 assertions then `anchor=N-ok`; rule: manifest anchors come from `grep -nF` output pasted verbatim, never from counting lines by eye |
| instrument read-only allow-list incomplete, so a legitimate derive was rejected (own, fail-closed direction) | first `figure-audit.py` green run exited 2: `FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=knowledge-files` — the ledger's `git ls-tree --name-only …` head was not in READ_ONLY_HEADS; the limb failed CLOSED on a legitimate read-only command, never open on a bad one | the instrument's own read-only limb on its first lane run, before the C1 commit | head `git ls-tree ` added to the allow-list; all three receipts (selftest 5/0, red 2-stale exit 1, green 9-ok exit 0) regenerated over the FIXED bytes; rule: an allow-list is enumerated from the ledger's actual command heads, not from a remembered set |
| registry row landed with the wrong cell count (12 vs the established 11-field row shape) | the round-end fleet census validate printed `kasegi E01 S086 fields=12` (exit 1) after the C2 commit; the S085 row prints 11 cells; the two extra cells (a separate not-covered cell and a screen cell) were merged into the scope and flip cells, landing the 11-field shape, validate exit 0 | the fleet census validator's E01 limb at the round-end gate - the one check that reads a SOURCES row's SHAPE rather than its content | cells merged in place (same line count, R6-safe; the row was this round's own new bytes, never line-cited by anything); rule: a new registry row is dry-run through `sources-census.sh validate` BEFORE landing, not only at round end |

## Gate

- S086 — https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md — access date
  2026-11-01; two opens this round, byte-identical (`sha256sum` fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f
  on both; the recorded one fetched 2026-11-01T08:17:52Z, HTTP 200, 46441 bytes); normalization
  declared strip-cr-tab = no-op (0 CR, 0 TAB observed), capture
  `corpus/source-snapshots/round-54/S086.txt` (731 lines, 46441 bytes); manifest with 14
  assertions Q1-Q14 each exactly-once at its pinned anchor; command:
  `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-54/manifest.json --source S086`
  → sha256 OK + 14 Q-OK lines, exit 0 (`controls/s086-recheck-r54.txt`). Located quote (12 words by
  `wc -w`, R56): "week during the previous 90 days, the project receives the highest score." at
  S086.txt:415.
- Rejections this round: none — the bounded hunt opened exactly the recorded lead (the round-53
  SCORECARD planned-for-53 candidate); the CISA ADP list page lead stays unopened (lead, not row —
  R64 does not apply to unopened surfaces).
- Extended pre-freeze screen (downstream-consumer sweep included), run at base BEFORE the freeze:
  `controls/neighbor-screen-r54.txt` — "scorecard" names zero held README/PROVINCE rows, only the
  SOURCES lead line, SCORECARD.md-filename mentions in three knowledge files and SKILL.md rows, and
  the OSV entry's OSSF-foundation naming; zero "scorecard" consumers across corpus/source-snapshots/
  (the only "ossf" snapshot hits are F31's own S080 capture).

## Limits

- The host-bound classes are unchanged and stay operator-owned (L0 kasegi round-50/46 unanswered,
  routed around): the 67 `cd /home/vgpnk/...` recheck lines (`strict pass=1/73 cdroot_fail=67`),
  the 3 cwd_fail lines, and the limb-mutation replay's `python3` dependency. The counter's overall
  exit 1 (30 problem-rows + 33 host-bound entry records) is the same disclosed class as r53; F35
  passes.
- S086 sits at a moving branch tip (`main`); the pinned sha256 is the round's authority and the 90d
  row recheck re-fails on change. The aggregate 0-10 score computation, risk weights, publisher/API
  and Prox are NOT in the document and are unasserted anywhere.
- capture-binding `multi_row_url=7` is the known informational class, unchanged 7 → 7 by this round
  (S086's URL is unique; verified against the base export).
- The round-54 capabilities row enters through the round section (the r43/R6-append practice): the
  main capabilities table sits mid-file in a line-anchored SCORECARD, so appending at EOF is the
  only R6-safe form.
- The pre-existing worktree condition (122 uncommitted paths at the base: staged NTFS deletions,
  untracked leftovers) is standing and untouched; commits landed only named paths through the
  plumbing helper.

## considerthese disposition (R23/R27 reflection cadence)

Burst/idle review for this round: the newest reflection file is `considerthese/2026-10-26.md` — an
idle stretch, no new reflection in the 2026-10-27 → 2026-11-01 window. Its seven proposals all
carry recorded dispositions (ledger `corpus/knowledge/considerthese-proposals-ledger.md` + rounds
36-39: distance-to-next-score → R26/`score-gap.py`; end-to-end domain task → open, SHONEN box 2
still open, out of this round's scope; quiescence gate → R28/R33; wave-evidence cap → R14; F18
province amendment → landed; cadence → R23/R27; status ledger → the ledger itself). Nothing new was
adopted this round (the one-per-round slot goes unspent): `Assimilation: none — shokuknow
unreachable`.

## Census of record at this round's tip

Quoted only from the final regeneration over the truly final tree (after the SCORECARD/LOG result
appends); the figures live in the SCORECARD round-54 section and the gate receipt
(`.ufo/waves/round-54/controls/c1-gate-final-r54.txt`). No corpus edit follows that receipt.
