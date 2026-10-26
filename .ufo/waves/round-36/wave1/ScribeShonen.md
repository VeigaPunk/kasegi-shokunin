# ScribeShonen — round-36 SHONEN.md box drafts (text only; the L1 integrates)

Seat: `ScribeShonen` (scribe, axis `calibration`). Sole writer of this receipt.
Round: kasegi-shokunin round 36, hyaku run 9. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`
(HEAD at this seat's read); frozen claims `.ufo/waves/round-36/claims.json`.

Writes: this receipt only, plus scratch under `/fast/scratch/hyaku/kasegi-r36/ScribeShonen/` (deleted before
yield). No lane file was edited; no mutating git command ran. Tooling authorization unused — nothing installed
or upgraded.

What this seat is, and what it is not: a wave seat **drafts** box text. All four boxes stay `[~]`. A wave seat
cannot write a checked box and has no authority to promote; the drafts below are paste-ready appends whose
every figure is bound in-clause to the receipt that measures it, and each one carries an explicit owed line
(non-author verification).

## 1. What this seat read (observed, at the instants named)

Read at `2026-10-26T15:36Z–15:41Z`, HEAD `b47f2cdf…`, worktree unmodified except the round-36 wave artifacts.

| surface | command | observed value |
|---|---|---|
| HEAD | `git rev-parse HEAD` | `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` |
| worktree | `git status --porcelain \| wc -l` / `… \| grep -v '^?? \.ufo/waves/round-36/' \| wc -l` | 9 / **0** — all nine entries are round-36 wave artifacts (`build-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`, `wave1-plan.{out,err}`, `wave1-run.err`, `wave1.ready{,.dispatched}`, `wave1/`) |
| `SKILL.md` | `sha256sum` / `wc -l` | `daeff71b…` / 1104 lines |
| registry literals | `grep -cF 'r35-defect-closure.sh' SKILL.md`; `grep -cF 'r36-closure.sh' SKILL.md` | **0** / **0** |
| `SCORECARD.md` | `sha256sum` / `wc -l` | `ed6e931f…` / 1404 lines |
| placeholder spellings | `grep -c 'filled by the L1' SCORECARD.md`; `grep -c '<LANE_HASH>' SCORECARD.md` | **0** / **0** |
| `PROVINCE.md` | `sha256sum` / `wc -l` / `grep -c F18` / `grep -c F19` | `b4bb5fee…` / 75 / **0** / **0** |
| `corpus/QUALITY.md` | `sha256sum` / `wc -l` | `d4f83bb1…` / 250 (R26/R27 supersede R22/R23 at `:249-250`) |
| `corpus/README.md` | `sha256sum` / `wc -l` / `grep -cE '^\| F[0-9]+ \|'` | `277f04ce…` / 396 / **18** frontier rows (F16/F17/F18 present) |
| `corpus/SOURCES.md` | `sha256sum` / `wc -l` / registry-row grep | `0f95a132…` / 112 / **52** rows |
| knowledge | `ls corpus/knowledge/*.md \| wc -l`; `grep -rl '^source: S052' corpus/knowledge \| wc -l` | **47** entries; 1 citing S052 |
| `knowledge-expected.txt` | `wc -l`; `grep -c '\.md$'` | 49 lines / **47** entry rows |
| `LOG.md` | `sha256sum` / `wc -l` / `grep -c '^## Round 36'` | `a576d58c…` / 1659 / **0** |
| `SHONEN.md` | `sha256sum` / `wc -l` | `90385026…` / 160 (round-35 paragraphs are the live evidence base) |
| r35 results + provenance | `ls .ufo/waves/round-35/wave1-results.json{,.provenance.md}`; `git ls-files` | `0d28a45c…` / 391 lines; **tracked**; provenance note present |
| `L1Integration.md` E6 | `grep -n 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md` | present at `:34` |
| `claims-erratum-d5.md` E5 | `ls .ufo/waves/round-35/claims-erratum-d5.md` | present |
| E9 limbs | `git status --porcelain`; `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d \| wc -l` | 9 entries (all wave artifacts); **49** seat scratch dirs |
| round-36 deliverables | `ls corpus/instruments/r36-closure.sh`, `ls corpus/knowledge/epss-exploit-prediction-scoring.md`, `ls corpus/source-snapshots/round-36`, `ls corpus/lessons/round-36.md` | **all absent** (each `ls` exit 2) — the C1 suite, the F19 entry, the S053 capture/manifest and the round-36 lesson were **not landed** at this read |

Sealed receipts read in full and cited below (all under `.ufo/waves/round-36/wave1/`):

- `ExecCensusReplay.md` — §2 two identical `validate` runs, exit 0, findings exactly `W04 S028` + `W04 S029`;
  §6 registry rows 52, knowledge 47, S053 row and EPSS entry absent.
- `ExecAncestry.md` — §3/§4: the final-lane-commit paragraph set is 8/8 exist + 8/8 ancestor of `master`; §6 F1:
  `SCORECARD.md:613` carries `94f387cbeb71…` (no such object; the real commit is `94f387cbee71…`) and the
  claim's literal `grep -oE '[0-9a-f]{40}'` finds 9 more non-ids, 8 of them the first 40 chars of a sha256.
- `ExecC2Capture.md` — §1/§2/§4: HTTP 200, 26,804 served bytes; normalized `S053.txt` 244 lines / 8,448 bytes,
  sha256 `4ec61c59…`; manifest 3,566 bytes, sha256 `f9590c2b…`; `source-recheck.py` on the scratch manifest
  exit 0 with `Q1..Q4 OK occurrences=1`.
- `ScoutF19Sibling.md` — verdict line `UNCONTESTED (neither contested nor ratified by any sibling)`; strict
  sweep over 20 sibling lanes + `/home/vgpnk/Projects/shokuknow` → 0 files.
- `ScribeQualityRows.md` — R28 (head closure / quiescence) and R29 (exact-basename registration) drafts, with
  the near-name evidence re-derived at the freeze (`r35-defect-closure.sh` exact-cell count 0).
- `ExecManifestChecks.md` — §0/§3/§4: real lane HEAD `records=42 bound=42 unbound=0 exit=0`,
  `--selftest cases=23 failures=0`; the drafted C2 manifest binds at `records=1 bound=1 unbound=0 exit=0`;
  the gate is blind to a missing capture, so `source-recheck --manifest` must run too.
- `ScribeMistakes.md` — §1 M36-1..M36-4 (landing/closure-order, stale-premise, counter-discrimination, landing)
  with anchors; `ScribeRowS053.md` — the 11-cell S053 row draft; `ScribeScorecard.md` — the round-36 scorecard
  section draft (its measurement-state template is the one my §7 paragraph sits beside, not on top of).
- `ScribeEntryF19.md` — the entry draft (262 lines / 17,267 bytes as drafted), its Q1–Q10 self-check, and the
  one `recheck:` line quoted verbatim; `RevSourceRecheck.md` — five criteria PASS on that line, fail-closed
  `exit 2` reproduced three ways, tampered bytes `rc=1`, happy path only on the round-35 positive control.

## 2. Integration rules for the L1 (read before pasting)

1. **Paste order.** §3→§6 append under the existing four `[~]` items in `SHONEN.md`; §7 appends after them.
   Every draft keeps `[~]`. Nothing in these drafts closes a box.
2. **Slots.** Text inside `⟨…⟩` is a slot only the integrating seat can fill: the final lane-head hash (from
   the `SCORECARD.md` `Final lane commit:` line), post-append `SKILL.md`/`PROVINCE.md` digests and line counts,
   and the sibling ruling sentence. Fill each from the named receipt; if the receipt is missing or disagrees,
   **delete the clause or restate it to what the receipt prints** — never leave a figure whose receipt does not
   carry it.
3. **E1 discipline.** Do not write the literal `filled by the L1` or `<LANE_HASH>` anywhere in `SCORECARD.md`;
   both counts read 0 at this seat's read and the round-36 suite's E1 re-reads them structurally. The
   `Final lane commit:` line must carry a 40-hex hash that `git cat-file -e` resolves **and** that
   `git merge-base --is-ancestor <hash> <exported-ref>` accepts (E1; `ExecC1SuiteBuild.md`, `ExecAncestry.md`).
   Scope the token scan to the label and classify by maximal run length — the file-wide
   `grep -oE '[0-9a-f]{40}'` reading is unsound on today's bytes for the reasons in §9 F-1.
   `ExecAncestry.md` §7 carries the exact three-command limb.
4. **Landing order.** The suite's own E9 is red until the wave is committed and every seat scratch dir is gone
   (`git status --porcelain` empty, `find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1` empty).
   File the boxes only on quiescent bytes, and run the suite with `--export-ref` on the commit you name, not on
   the worktree (routed defect 1 / M35-1).
5. **No promotion claim.** These drafts assert no box closure and no promotion signal; box 2 in particular has
   no new executed task and says so.

## 3. Draft — box 1 (SKILL.md: decision tables, error patterns, checklists, cited sources)

```markdown
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 36, base `cc69200`, freeze `b47f2cd`, final lane head `⟨FINAL⟩`): the Gates & probes
      registry now registers both closure instruments by **exact basename** — `r35-defect-closure.sh` (the
      round-35 suite, which the round-35 registry addition missed: the landed rows at `SKILL.md:1097-1098` name
      `r-defect-closure.sh` and `kill-rule-check.py`, near-names that satisfied the old literal) and this round's
      `r36-closure.sh` (`⟨sha256⟩`, `⟨n⟩` lines; receipt `ExecC1SuiteBuild.md`). Both literals read 0 on the
      pre-append blob — measured at the claims freeze on `SKILL.md` `daeff71b…` (1104 lines):
      `grep -cF 'r35-defect-closure.sh' SKILL.md` = 0, `grep -cF 'r36-closure.sh' SKILL.md` = 0 — so the two
      rows are this round's delta, and the appended file is `⟨post-append sha256⟩` / `⟨lines⟩` lines
      (`RevNoHarm.md`). The criterion travels with the literal: the round-36 lesson's M36-3 records the
      near-name defect (class counter-discrimination: a sibling basename satisfied the registry grep) and
      QUALITY's new R29 requires registration by exact basename (drafts `ScribeMistakes.md`,
      `ScribeQualityRows.md`), so the registry check (E3) and the written rule now test the same thing. No-harm:
      the change is an end-of-file append; `density.py` / `anchorcheck.py` over the appended bytes are
      `RevNoHarm.md`'s to file (`⟨base mean/blocks/cites → landed mean/blocks/cites⟩`), and no pre-existing
      `SKILL.md` line is deleted. Box stays `[~]`: **owed — no named non-author verifier has checked this box,
      a wave seat cannot write a checked box (round-35 precedent), and the density pair above must be read off
      `RevNoHarm.md`, not inferred from the append.**
```

## 4. Draft — box 2 (end-to-end domain task in LOG.md)

```markdown
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 36): **no new end-to-end domain task ran this round** — stated as the box's fact, not as
      a gap elsewhere. At the claims freeze `b47f2cd`, `grep -c '^## Round 36' LOG.md` = **0** on a 1659-line
      `LOG.md` (blob `a576d58c…`), and the round-36 entry the L1 is to append (draft `ScribeLOG.md`)
      logs instruments and one admission — the `r36-closure.sh` closure suite and the F19/S053 EPSS entry — not
      a hunt-to-claim task; the 64-seat wave spec (`.ufo/waves/round-36/wave1-spec.json`) carries **no
      domain-task seat**, its closest members being `ExecC2Capture` (one-document capture) and
      `ExecC1SuiteBuild` (instrument build). The strongest executed measurement this round is instrument
      closure: `r36-closure.sh --export-ref ⟨FINAL⟩` → `closed=9/9 exit=0` and `--selftest` →
      `cases=9 failures=0`, with the red arms `closed=0/9 exit=1` on the round-35 base export and
      `closed<9/9 exit=1` on its judged head (claim C1 `counting_commands`; receipts `ExecC1SuiteBuild.md`,
      `ExecC1Fixtures.md`, `ExecC1BaseFail.md`) — instrument work, not a domain task. The round-35 disclosures
      stand: the closest end-to-end measurement remains the capture-binding check, which on the claims freeze
      `b47f2cd` reads `records=42 bound=42 unbound=0 exit=0` with `--selftest cases=23 failures=0`
      (`ExecManifestChecks.md` §0/§3; the round-34 frozen `40` literal is superseded by
      `.ufo/waves/round-34/claims-erratum-1.md`) — still a registry-to-capture binding, not a domain task. Box
      stays `[~]`:
      **owed — one domain task executed end to end (read → claim → logged decision) and a named non-author
      verifier to check it; until then this box cannot move and the round carries no promotion signal.**
```

## 5. Draft — box 3 (instructions executable without oral context)

```markdown
- [~] Instructions executable by an agent without oral context
      — evidence (round 36, base `cc69200`, freeze `b47f2cd`): the F19 entry
      `corpus/knowledge/epss-exploit-prediction-scoring.md` becomes the 48th `corpus/knowledge/*.md` entry
      (262 lines / 17,267 bytes as drafted, `ScribeEntryF19.md` §1) and
      carries exactly one `recheck:` command (draft `ScribeEntryF19.md`; at the claims freeze `b47f2cd` the tree
      held 47 entries and the entry was absent), and `corpus/instruments/knowledge-expected.txt` is synced with it —
      47 entry rows before (`grep -c '\.md$'` = 47, 49 lines, `d2e99ca6…`) → 48 (`⟨post-sync sha256⟩`,
      `⟨lines⟩`), so `python3 corpus/instruments/recheck-audit.py` reads `strict pass=48/48 cdroot_fail=0
      instrument_fail=0 own_fail=0` with `expect=present expected=48 missing=0 unexpected=0 exit=0` (receipt
      `ExecC2Harness.md`). The counters run on the proposed tree, each in one command: `frontier-recheck-count.py`
      `entries=22 pass=22 exit=0` including `PASS F19 … ids=S053`; `source-recheck.py --manifest
      corpus/source-snapshots/round-36/manifest.json --source S053` exit 0; `capture-binding-check.py` exit 0
      (receipts `ExecC2Harness.md`, `ExecC2Capture.md`, `ExecManifestChecks.md`). The capture those commands
      read is pinned at this round's read: the page served HTTP 200 with 26,804 bytes, normalized to `S053.txt`
      — 244 lines, 8,448 bytes, sha256 `4ec61c59…` — with `manifest.json` 3,566 bytes, sha256 `f9590c2b…`, and a
      `source-recheck.py` run over the scratch manifest printing `Q1..Q4 OK occurrences=1` at exit 0
      (`ExecC2Capture.md` §1/§2/§4); the lane-path run and `capture-binding-check.py` remain the two receipts
      named above to file. The census is executable as
      printed and was replayed twice this round: `sources-census.sh validate --root … kasegi` exit 0 both times,
      findings exactly `W04 S028` and `W04 S029`, registry 52 rows before the S053 append (this seat read
      `ExecCensusReplay.md` §2/§6; same two lines in `.ufo/waves/round-36/census-before.txt`). The closure suite
      is executable end to end from a fresh export — `bash corpus/instruments/r36-closure.sh --export-ref
      ⟨FINAL⟩` → `closed=9/9 exit=0`, `--selftest` → `selftest cases=9 failures=0`, while the r35 base export
      `3266c993…` reads `closed=0/9 exit=1` and the r35 judged head `0aee0ef1…` reads `closed<9/9 exit=1`
      (claim C1; receipts `ExecC1SuiteBuild.md`, `ExecC1Fixtures.md`, `ExecC1BaseFail.md`). The audit trail is
      itself corrected this round: the round-36 lesson records the correction of the three false evidence lines
      the round-35 lesson carried at A (routed defect 5 → E8; draft `ScribeGateLesson.md`), so a later reader
      learns from the record that those lines were wrong instead of from oral context. Box stays `[~]`:
      **owed — every figure above must be read off its named receipt at integration (none of the round-36
      deliverables existed at this seat's read), and a named non-author verifier must check the box.**
```

## 6. Draft — box 4 (no cross-domain bleed; PROVINCE.md accurate)

```markdown
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 36, base `cc69200`, freeze `b47f2cd`): at this seat's read `PROVINCE.md` was
      `b4bb5fee…`, 75 lines, with `grep -c F18` = **0** and `grep -c F19` = **0** — the round-35 F18 amendment
      was still owed and the round-36 F19 amendment not yet applied. This round closes both by end-of-file
      append under R6, no existing line edited (prefix bytes unchanged; file `⟨post-append sha256⟩` /
      `⟨lines⟩`, append shape `⟨lines/sha256⟩` from the landing commit): F18 (CISA KEV — exploitation status as
      a prioritization signal) and F19 (FIRST EPSS — exploitation-likelihood scoring, distinct from CVSS
      severity and from KEV catalog status). Both sit inside the province's core
      "program rules, claim packages" paragraph on the F13/F16/F17 severity-scope precedent, so no re-scope is
      claimed and no sibling's ground is taken. The no-bleed claim is non-vacuous only through the sweep:
      `ScoutF19Sibling.md` rules `UNCONTESTED (neither contested nor ratified by any sibling)` — its strict
      sweep (`\bEPSS\b|…|first\.org/epss`) returns 0 files across 20 sibling lanes and 0 hits in
      `/home/vgpnk/Projects/shokuknow`, so nothing contradicts S053/F19 and nothing pre-ratifies it; admission
      rests on kasegi's own primary-source capture and the harness PASS, not on sibling corroboration. Box
      stays `[~]`: **owed — the PROVINCE append had not landed at this seat's read, `ConnSibling.md`'s ruling
      must be quoted alongside `ScoutF19Sibling.md`'s rather than paraphrased, and no named non-author
      verifier has checked this box.**
```

## 7. Draft — measurement-state paragraph (append after the four boxes)

```markdown
**Round-36 measurement state (ScribeShonen, 2026-10-26T15:37Z; pre-append read at the claims freeze
`b47f2cdf…`).** Live tree HEAD `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`, base `cc692008…`. Digests read at
this seat's measurement: `SKILL.md` `daeff71b…` (1104 lines, registry literals `r35-defect-closure.sh`/`r36-closure.sh`
= 0/0), `SCORECARD.md` `ed6e931f…` (1404 lines, placeholder spellings 0/0), `PROVINCE.md` `b4bb5fee…` (75 lines,
F18 0 / F19 0), `corpus/QUALITY.md` `d4f83bb1…` (250 lines), `corpus/README.md` `277f04ce…` (396 lines, 18 frontier
rows), `corpus/SOURCES.md` `0f95a132…` (112 lines, 52 registry rows), `corpus/knowledge` 47 entries,
`corpus/instruments/knowledge-expected.txt` 47 entry rows, `LOG.md` `a576d58c…` (1659 lines, 0 round-36 headings),
`SHONEN.md` `90385026…` (160 lines), `.ufo/waves/round-35/wave1-results.json` `0d28a45c…` (391 lines, tracked,
provenance note beside it). Absent at this read: `corpus/instruments/r36-closure.sh`,
`corpus/knowledge/epss-exploit-prediction-scoring.md`, `corpus/source-snapshots/round-36/`,
`corpus/lessons/round-36.md`. E9 limbs at this read: `git status --porcelain` 9 entries, **all** under
`.ufo/waves/round-36/` (0 outside), and 49 seat scratch dirs under `/fast/scratch/hyaku/kasegi-r36` — red on both
limbs, as expected mid-wave. Every post-append figure in the boxes above is its owning receipt's to file; this
paragraph is the baseline those figures must be diffed against.
```

## 8. Calibration ledger — every figure in the drafts, bound and marked

Legend: **OBS** = this seat executed the read and saw the value; **PEND** = the value is the frozen claim's
predicate or the owning seat's item, **not observed at this seat's read**; **SLOT** = the integrating seat must
supply it from the named receipt.

| figure used in §3–§7 | binding | status at this seat's read |
|---|---|---|
| `r36-closure.sh` plain run `closed=9/9 exit=0` on the final export | C1 `counting_commands[0]`; `ExecC1SuiteBuild.md` | **PEND** — suite absent (`ls` exit 2) |
| `--selftest cases=9 failures=0` | C1 `counting_commands[3]`; `ExecC1Fixtures.md` | **PEND** |
| base export `3266c993…` → `closed=0/9 exit=1` | C1 `counting_commands[1]`; `ExecC1BaseFail.md` | **PEND** |
| round-35 judged head `0aee0ef1…` → `closed<9/9 exit=1` | C1 `counting_commands[2]`; `ExecC1BaseFail.md` | **PEND** |
| `r35-defect-closure.sh` / `r36-closure.sh` registry literals | E3; `ExecC1SuiteBuild.md`, `RevC1Suite.md` | **OBS 0 / 0** on `daeff71b…` (1104 lines); post-append counts **SLOT** |
| post-append `SKILL.md`/`PROVINCE.md` digest, lines, density pair | `RevNoHarm.md` (executor `ExecRegressionBase`/reviewer `RevNoHarm`) | **SLOT**, no figure in this receipt |
| `frontier-recheck-count.py` `entries=22 pass=22 exit=0` incl. `PASS F19 … ids=S053` | C2 `counting_commands[3]`; `ExecC2Harness.md` | **PEND** — frozen before cell: `entries=21 pass=21` (claims.json C2 `before`); observed base 18 frontier rows / 47 entries is consistent, not equal, to that counter |
| `source-recheck.py … --source S053` exit 0 | C2 `counting_commands[4]`; `ExecC2Capture.md`/`ExecC2QuoteOnce.md`; `RevSourceRecheck.md` | **partly OBS**: `ExecC2Capture.md` §4 records `Q1..Q4 OK occurrences=1` exit 0 over the **scratch** manifest; `RevSourceRecheck.md` independently passes all five criteria on the drafted `recheck:` line, shows fail-closed `exit 2` three ways and a tampered-bytes `rc=1`, with the happy path proven only on the **round-35** control. The lane-path `corpus/source-snapshots/round-36/manifest.json` run is **PEND** (dir absent) |
| F19 entry draft (262 lines / 17,267 bytes; one `recheck:` line; `ground: F19`) | `ScribeEntryF19.md` §1; `RevEntryF19.md` for Q1–Q10 | **drafted**, not landed (`corpus/knowledge/*.md` = 47 at read) |
| `S053.txt` / `manifest.json` pins (8,448 and 3,566 bytes; `4ec61c59…` / `f9590c2b…`) | `ExecC2Capture.md` §2; payloads embedded verbatim in that receipt | **OBS** in the sealed receipt; not on disk at this read |
| `capture-binding-check.py` exit 0 | C2 `counting_commands[6]`; `ExecManifestChecks.md` | **partly OBS**: real lane HEAD `b47f2cd` → `records=42 bound=42 unbound=0 exit=0`; the drafted C2 manifest against a bare-URL S053 row → `records=1 bound=1 unbound=0 exit=0`; instrument `--selftest cases=23 failures=0`. The landed-manifest run is **PEND**. `ExecManifestChecks.md` §4 also measures that this gate is blind to a missing capture (`exit 0` with `S053.txt` absent), so both gates must run |
| `recheck-audit.py` `strict pass=48/48`, `expected=48`, exit 0 | `ExecC2Harness.md` | **PEND** — base sync is 47/47 (observed rows) |
| S053 row fields (tier `A`, scope = FIRST's own EPSS statements, `status mined`, `opened 2026-10-26`, `recheck 90d`, `used-by` the F19 entry, 11 cells) | `ScribeRowS053.md` §row/§checks | **drafted**, not landed — row **PEND** on disk (`SOURCES.md` 52 rows at read) |
| M36-1..M36-4 anchors (M36-1 `none (new)`; M36-2/3/4 captured-by R16 / R17-limb+R11 / R4) | `ScribeMistakes.md` §1 | **drafted**, not landed (`corpus/lessons/round-36.md` absent) |
| F19 sibling ruling (`UNCONTESTED …`) | `ScoutF19Sibling.md` | **OBS** (sealed receipt; strict sweep 0 files / 20 lanes) |
| E1 ancestry on the final-lane-commit set (8/8 exist + ancestor) | `ExecAncestry.md` §3/§4 | **OBS** at `b47f2cdf`; the round-36 label line does not exist yet (no `## Round 36` heading in `SCORECARD.md`) |
| SCORECARD:613 stale hex `94f387cbeb71…` (F1) and the 8 sha256-prefix tokens | `ExecAncestry.md` §6 | **OBS** — pre-existing; see §9 F-1 |
| knowledge 47 → 48; expected 47 → 48 rows | C2 `after`; `ScribeEntryF19.md`, `ExecC2Harness.md` | 47 / 47 **OBS**; 48 **PEND** |
| census exit 0 ×2, `W04 S028`+`W04 S029` only, 52 registry rows before | C2 `counting_commands[5]`; `ExecCensusReplay.md` §2/§6 | **OBS** via the sealed receipt plus `.ufo/waves/round-36/census-before.txt` (same two lines) |
| `PROVINCE.md` F18/F19 appends | C1 E-checks E3-adjacent scope claim; draft `ScribeLOG.md`/lesson | **OBS 0 / 0**; append **PEND** |
| `LOG.md` round-36 entry | draft `ScribeLOG.md` | **OBS 0 headings**; entry **PEND** |
| lesson E8 correction of the three false evidence lines | C1 E8; draft `ScribeGateLesson.md`, `ScribeMistakes.md` | **PEND** — `corpus/lessons/round-36.md` absent |
| E9 `git status --porcelain` empty, no scratch seat dirs | `ExecQuiescenceProbe.md`; C1 kill rule | **OBS red**: 9 entries all under `.ufo/waves/round-36/` (0 outside), 49 scratch dirs |
| `L1Integration.md` `Correction (round 35)`, `claims-erratum-d5.md`, r35 results tracked + provenance, QUALITY R26/R27 | C1 E4–E7 | **OBS present/tracked** at `b47f2cdf` |
| capture-binding figures `records=42 bound=42 unbound=0`, `selftest cases=23` | `ExecManifestChecks.md` §0/§3 at `b47f2cd` | **OBS** this round (round-34's `41/41` and its erratum `.ufo/waves/round-34/claims-erratum-1.md` are history, superseded by the live count) |

## 9. Findings this seat passes to the L1 (about the evidence, not about the boxes)

**F-1 — E1 must be label-scoped and length-classified, or it is red before round-36 work lands.**
`ExecAncestry.md` §6 measured the claim's literal `grep -oE '[0-9a-f]{40}' SCORECARD.md`: 31 unique tokens, 9
with no object behind them. Eight are the first 40 characters of a 64-hex sha256 digest (instrument, file and
claims digests, e.g. `95333e29…`, `5d4842da…`, `fe0dae89…`) — they can never satisfy `cat-file -e`. The ninth is
a genuine stale citation: `SCORECARD.md:613` cites the round-28 dispatch commit as `94f387cbeb71…` where every
round-28 receipt and the object DB carry `94f387cbee71…` (one inserted `e`, same length, invisible to a length
check). Under the label-scoped reading E1's ancestry clause is green: the four `Final lane commit:` blocks and
their three restatements hold 8/8 exist + 8/8 ancestor of `master`. **Consequence for box text:** nothing in §3–§6
may claim that every 40-hex token in `SCORECARD.md` resolves. The box text as drafted claims only the label line.
If the suite keeps the file-wide literal, the round-36 boxes must carry F-1 as a known-exempt citation and F-1
should be corrected by an appended scorecard erratum — a rewrite of `:613` would violate routed defect 4.

**F-2 — the near-name registry defect is real and already re-derived at the freeze.**
`ScribeQualityRows.md` G6/G9: `git show cc692008…:SKILL.md | grep -cF 'r35-defect-closure.sh'` = 0 and the same
at `b47f2cdf…`; exact-cell counts `^\| *r35-defect-closure\.sh *\|` and `… r36-closure\.sh …` are 0 and 0, while
`grep -cF 'r-defect-closure.sh' SKILL.md` = 3 (the row at `:1097` plus its notes at `:1102`/`:1104`). This is what
makes M36-3 (class counter-discrimination) and R29 non-vacuous, and it is why box 1's evidence sentence names
both basenames rather than "closure instruments".

**F-3 — E9 is red now, by construction, and must be re-run at filing.** At this seat's read the worktree held 9
entries, all under `.ufo/waves/round-36/` (0 outside), and `/fast/scratch/hyaku/kasegi-r36` held 49 seat dirs.
Any box text pasted before the wave is committed and the scratch tree is empty would be evidence for a state
that does not exist; the boxes must land on quiescent bytes (R28, routed defect 1).

## 10. What is still owed (explicit, per box)

1. **A named non-author verifier for each box.** No box can be checked by a wave seat (round-35 precedent,
   repeated in the round-35 paragraphs this receipt appends after). Four boxes, four checks owed, by someone
   other than the drafting seat and other than the L1 that pastes.
2. **Box 2 has no new executed task, and says so in its own text.** Its owed item is the task itself first,
   verification second; without it the round carries no promotion signal regardless of C1/C2.
3. **Figures, not adjectives.** Each `⟨…⟩` slot and each **PEND** row in §8 must be replaced by the value its
   receipt prints before the box text is appended; where a receipt is missing, the clause is dropped, not
   softened.
4. **Quiescence at filing.** E9 is red on both limbs now (§8); the boxes may only be appended on bytes where
   `git status --porcelain` is empty and no seat scratch dir remains — including this seat's, removed at yield.

## 11. Limits of this receipt

- This seat did not run the round-36 suite, the harness, `source-recheck`, `capture-binding-check`,
  `recheck-audit`, `density.py` or `anchorcheck.py`; nothing here is presented as a measurement of an artifact
  that did not exist at read.
- The census is cited from the sealed executor receipt I read in full (`ExecCensusReplay.md`), not re-run.
- Drafts quote claim predicates (C1/C2 `counting_commands`, `after`) as the intended evidence set; they are not
  evidence of their own satisfaction.
- `SHONEN.md` line anchors: the file was 160 lines at read; the four `[~]` items and the round-35 paragraphs are
  append-only territory, so §3–§7 append cleanly after `SHONEN.md:160`.
- Scratch `/fast/scratch/hyaku/kasegi-r36/ScribeShonen/` removed before yield; no tool was installed.
