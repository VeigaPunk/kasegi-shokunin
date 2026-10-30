# R47W2EraBoundary — round-46 era-bound instruments vs current round-47 predicates

Seat: R47W2EraBoundary (critic, wave 2). Axes: **depth:verifiability**, **coverage**.
Scope: final integrated review of the era-bound question only. No integration, judgment of admissions,
edit, fleet write, delegation, or `agent://all`. All paths below are relative to
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless prefixed `fleet:`.

Execution status: **static review; gate execution unrun.** The only executed operations are
read-only byte inspections (sha256sum, grep/wc/diff counts, `git show`/`git diff`/`git status`
reads, one JSON read of committed manifest bytes). No gate, counter, census, source-recheck,
selftest, mutant battery or live fetch was run. No tool was installed (RULES.md read; pacman
transactions untouched per pause). No scratch directory was created, so none remains to delete.

Tree state inspected: integrated revision `65e19bdb142c90a08103eb4b2af60c71218a920e` with dispatch
commit `f074bffb121134243a8c58878d7283fe8d2c6784` on top; working tree additionally holds
**untracked** `.ufo/waves/round-47/counter-errata.md` and `w2/` seat files (`git status --porcelain`).

## Answer to the seat question

**Do current docs clearly distinguish historical green receipts from current red predicates? PARTIAL.**

What distinguishes well (verified, executed reads):

- The corpus-level captions are good: `corpus/README.md:695-700` new section says the F29 row "is
  historical; its current entry now cites S076 while the S074 capture remains retained for round-46
  history"; `corpus/instruments/README.md:1023` says counters "remain byte-frozen at `308a2cb2`;
  their green values are mechanical, not admission"; `corpus/lessons/round-47.md:67` logs the single
  registry cell change old→new; `.ufo/waves/round-47/controls/capture-binding-before.txt:24-29`
  retains the honest red-before predicate (`records=63 bound=61 unbound=2`, `EXIT=1`, S075/S076
  `FAIL rule=no-row`); the historical F29 receipt self-stamps its era
  (`.ufo/waves/round-46/attempt2/controls/final-measure.txt:1` `measured-at-rev: c8641e7a…`, base
  `fixed=1/7` at :17, tip `fixed=7/7` at :27).
- No era gate was weakened: sha256 of `r46-f29-gate.py` (`dc9f8af7…`), `r46-c1-gate.py`
  (`95f2eb79…`), `r46-c2-gate.py` (`ad60a72c…`) are byte-identical at freeze `308a2cb2`, integrated
  tip `65e19bd`, and the working tree. `git diff 308a2cb..65e19bd -- corpus/instruments/` moves only
  `README.md` (+4) and `knowledge-expected.txt` (+1) — no instrument bytes.

What does **not** distinguish — findings F1–F7 below. The core defect: the landed era statement
under-names the old gate's expected red limbs, so the exact M46-6 trap ("an instrument reading red
that no receipt explains", `corpus/lessons/round-46.md:96`) survives the integration.

## F1 — Counterexample: the landed era statement predicts H2/H5 red, but the integrated tree also necessarily moves H3 and H6 red

`.ufo/waves/round-47/counter-errata.md:23` (untracked file): "Re-grounding the F29 entry to S076
intentionally changes its H2/H5 reading at the new tree." That is the only limb-level prediction
landed anywhere. Derived from the committed predicates (static, unrun), the old gate
`corpus/instruments/r46-f29-gate.py` at tip `65e19bd` reads:

| limb | predicted reading (unrun) | driver | predicate evidence |
|---|---|---|---|
| H1 | GREEN: `rows=29 admitted=29`; F29 row sources cell still `S074` (`corpus/README.md:691`); entry cell exact; parsers unperturbed | no F30 row landed | `r46-f29-gate.py:175-200` (29-pin :180); `frontier()` :141-149 needs `^\| F\d+ \|`, `frontier_anywhere()` :151-160 needs `\| *F\d+ *\|` — the new `README.md:696-697` table rows (`| F02 coordinator case: …`, `| F29 current capture provenance |`) match neither |
| H2 | RED by design (D7) | entry header/recheck re-anchored | needs `source: S074 — <URL>` (:204-206) and `RECHECK_LINE` = `--manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` (:91-93); landed entry `corpus/knowledge/github-repository-security-advisories.md:3` says `source: S076 …`, :5 recheck uses `round-47/manifest.json` + `S076` |
| H3 | RED, single reason: used-by | S074 used-by repointed | :273-274 `p not in row[10]`; `corpus/SOURCES.md:80` used-by cell is now `corpus/lessons/round-46.md` (base was the entry path; awk cell-11 diff executed); status stays `mined`, anchor/locator/sha cells byte-unchanged, so no other H3 cell is red |
| H4 | GREEN, live-dependent | S074 history preserved | :278-301 pins S074 snapshot/manifest/`source-recheck.py` bytes (:83-89); none moved in the integrated diff. Caveat: H4 executes a live re-fetch, so its reading is subject to page drift, not era |
| H5 | RED by design (D7) | citation grammar | :303-329 recognizes only `S074.txt:N` spans; executed `grep -n 'S074'` on the landed entry prints **zero** matches → `spans=0` < 4 |
| H6 | RED, driver is **not** F30 | 67th knowledge entry | :350 pins `len(names) == 66`; executed `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` = **67** (`zdi-disclosure-policy.md`, the retained F02 coordinator case per `README.md:696`); base-names/content digests (:337-345) also change |
| H7 | GREEN | census warnings only | :355+ needs census rc 0 + ok-line; `w1/R47CritCensus.md` receipt: 76 rows, 4 warning-only W04 (new S076/S074 shared URL), exit 0 on the assembled candidate with the entry present |

Predicted aggregate at the integrated tip: **`f29-gate fixed=3/7 exit=1`** (H2/H3/H5/H6 red). No
committed or landed doc states this set. `w1/R47SrErrata.md:19-22` predicted H1/H2/H5/H6 red under
the frozen assumption that F30 landed (30 rows); the actual C2-unmet landing makes H1 green and adds
H3 red via the used-by repoint. `w1/R47CritErrata.md:14-16` correctly flagged H3 ("its resulting red
must be explained separately") and H4, but the landed `counter-errata.md` dropped both
qualifications. Result: a closure reader who runs the retained old gate sees two red limbs (H3, H6)
that no landed sentence explains — the precise recurrence M46-6 forbids.

## F2 — No integrated-tip receipt of the old gate exists; the wave-1 receipt requirement is unmet

`.ufo/waves/round-47/controls/` holds only base/pre-freeze receipts (c1-base, c2-base,
freeze-check, capture-binding-before, …). `w1/R47ExecFreezeGates.md` and `w1/R47ExecGateReplay.md`
receipt the **new** counters on base/freeze-era working trees, never `r46-f29-gate.py`.
`w1/R47CritErrata.md:70-72` required the integrator to record the final revision, exact old
instrument bytes, command, explicit `--work`, **all seven limb lines**, summary and actual exit
code, with each red limb classified against its changed tree predicate. None of that exists at
`65e19bd`. My seat supplies the static prediction (F1) but does not manufacture the receipt.

## F3 — The era erratum itself is uncommitted and referenced by nothing

`.ufo/waves/round-47/counter-errata.md` is **untracked** at both `65e19bd` and `f074bff`
(`git status --porcelain`: `??`). Grep over committed docs finds zero references to
`.ufo/waves/round-47/counter-errata.md` (`corpus/lessons/round-47.md`, `corpus/README.md`,
`corpus/SOURCES.md`, `LOG.md` mention only the round-45/46 errata files). The fleet report
`fleet:.ufo/reports/round-47/` does not exist yet. As **committed** docs stand, the era-bound
distinction exists nowhere; it lives only in uncommitted working-tree bytes. The closure must
commit this file and point to it, or the distinction silently vanishes on any fresh export.

## F4 — The fleet round-46 report's bare live-root sentences remain uncorrected by any landed pointer

`fleet:.ufo/reports/round-46/kasegi.md:81` still asserts, without qualification, "`r46-f29-gate.py
--root .` = 7/7 … recheck-audit 66/66, census, binding 61/61"; :46 carries "After (tip `4cdcf7bd`):
`fixed=7/7`"; :55's "the S074 URL is unique" is no longer repeatable (S076 intentionally shares it —
`corpus/SOURCES.md:82`); :57's "one Search-log bullet + two Registry-changes bullets" described
fenced drafting bytes (D5). `w1/R47CritErrata.md:24-58` inventories every such sentence and
:59-67 supplies append-only erratum wording; **that wording was not landed** — the untracked
`counter-errata.md` states the general principle but names neither the report file nor one specific
sentence. A reader entering through the fleet report gets no marker that these are era measurements.
Smallest fix: land the :59-67 erratum block in the round-47 report/counter-errata; do not rewrite
the filed report.

## F5 — Frozen "intended repair" fixture is not byte-identical to the landed entry (one undisclosed line)

`corpus/instruments/entry29-fixed-bytes.md` (freeze-era fixture, consumed by
`corpus/instruments/r47-counters-selftest.py:206`) differs from the landed
`corpus/knowledge/github-repository-security-advisories.md` in exactly one hunk (`diff -u`: 1
`@@`): the Limits chrome enumeration says `S076.txt:562-566` in the fixture, `562-565` in the landed
entry (both at :88). Committed bytes `S076.txt:561-567` show 562-565 are TOC chrome and 566 is the
repeated article heading, so the landed line is the more accurate reading — but the divergence from
the freeze-named "intended repair bytes" is disclosed nowhere, and `w1/R47CritErrata.md:11` told
readers the repair *is* `entry29-fixed-bytes.md`. One sentence in the counter-errata (fixture is
synthetic selftest input, not a byte-pin of the landed entry, with this one-line delta) closes it.

## F6 — The repaired entry carries a pre-capture `verified-at` date

`corpus/knowledge/github-repository-security-advisories.md:4` (and the fixture :4) says
`verified-at: 2026-10-29`, while its own source header (:3) names S076, whose committed manifest
record has `fetched_utc: 2026-10-30T10:35:47Z` and whose SOURCES row shows opened `2026-10-30`
(`corpus/SOURCES.md:82`, awk cell read executed). The date is inherited from the S074-era entry and
is unexplained; as written the entry claims verification one day before its cited capture existed.
Safe to fix or footnote: old-gate H2 is already red via `ok_s`, so this cannot be read as
gate-shaping. Smallest fix: state that 2026-10-29 is the S074-era content verification whose
normalized text S076's capture matched, or correct the cell to 2026-10-30.

## F7 — `knowledge-expected.txt` is now an era file; historical replay discipline must name it

The integrated commit appends one sorted line (`corpus/knowledge/zdi-disclosure-policy.md`,
`corpus/instruments/knowledge-expected.txt:69`) to the expectation file consumed by
`corpus/instruments/recheck-audit.py:45-47,269,372`. Consequence: running **current** instruments
against an **era export** (the round-46a2 replay route) now mismatches on the 67th expected entry,
and the round-46 report's "recheck-audit 66/66" (:81) has no current meaning. The landed
counter-errata's era paragraph covers gates but not this input file. One line suffices: era exports
pair with era expectation files; mixed-era runs are not measurements.

## F8 — Stable predictions for the other retained round-46 instruments (static, unrun)

- `r46-c2-gate.py` v1.3: at the round-46a2 export it already read `5/7` (G1 28→29, G6 65→66 —
  M46-6, `corpus/lessons/round-46.md:96`). At `65e19bd`: rows stay 29 (G1 unchanged red), entries
  67 vs pin 65 (G6 still red), ledger floor 40,843 untouched, the two re-grounded entries untouched
  → predicted **same `5/7`, no new limb movement**. Nothing needs a new exemption story here, but a
  doc saying "already era-count-bound" (counter-errata) should keep G1/G6 named as the moving pair.
- `r46-c1-gate.py` v1.2: its gated/anchored surfaces (`claim-gates.md`, `claim-package-contract.md`,
  still-gated entries, baseline `914ca0b`) are untouched by the integrated diff; it has no
  knowledge-count pin. Predicted unchanged/green at the new tip; no era explanation owed unless a
  run says otherwise.

## Smallest safe correction (for the closure; not performed by this seat)

1. Extend `.ufo/waves/round-47/counter-errata.md:23` to the full per-limb set: H2+H5 red by the D7
   re-anchor, H3 red by the S074 used-by repoint, H6 red by the 67th (F02-enrichment) entry,
   H1/H7 expected green, H4 green modulo live drift — classified per limb, no blanket waiver.
2. Commit `counter-errata.md` and reference it from the round-47 report and a LOG line (F3).
3. At closure, receipt the actual seven-limb output of `r46-f29-gate.py` at the integrated export
   (revision, command, `--work`, all seven `gate H<n> pass=` lines, summary, exit code) and explain
   any limb deviating from F1's prediction individually — especially H4 live drift (F2).
4. Land the `w1/R47CritErrata.md:59-67` naming erratum so the fleet round-46 report's bare
   sentences (:46, :55, :81) are covered by pointer, not rewritten (F4).
5. Add the three one-line disclosures: fixture-vs-landed chrome-range delta (F5), the entry's
   pre-capture `verified-at` (F6), and the era-pairing note for `knowledge-expected.txt` (F7).

## Executed-check receipts (all read-only, this seat)

```
sha256sum corpus/instruments/r46-{f29,c1,c2}-gate.py == git show 308a2cb:… (3/3 identical)
  dc9f8af78ec9c52c1778472941bef72b8e51a07277c5e91e27d42f2a40f70053  r46-f29-gate.py
  95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  r46-c1-gate.py
  ad60a72cf76304aaf22634e9b319453769f874c90d80df3305191f8e147d70f2  r46-c2-gate.py
git diff --stat 308a2cb..65e19bd -- corpus/instruments/ = README.md +4, knowledge-expected.txt +1
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l            = 67
grep -cE '^\| F[0-9]+ \|' corpus/README.md                        = 29
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md = 76
grep -n 'S074' corpus/knowledge/github-repository-security-advisories.md = (no matches)
S074 used-by cell: base=entry path → tip=corpus/lessons/round-46.md (single-line row diff, awk)
diff -u corpus/instruments/entry29-fixed-bytes.md <landed entry> = 1 hunk (562-566 vs 562-565)
manifest.json round-47: S075 fetched 2026-10-30T10:35:37Z, S076 fetched 2026-10-30T10:35:47Z
git status: .ufo/waves/round-47/counter-errata.md = untracked (??)
```

Unrun items are labeled as static predicate derivations above; none is presented as a measurement.
No installs, no pacman transactions, no background jobs, no shared-production edits, no git/jj
mutations; scratch discipline satisfied vacuously (no scratch created).
