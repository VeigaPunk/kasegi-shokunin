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

## Round-29 additions — open-defects ledger

| id | criterion | grounded in |
|---|---|---|
| R15 | A named open defect stays open only while its runnable closure check exits non-zero; every open-defect row carries its closure-check command (`bash -n`-parseable) and an evidence pointer. | considerthese/2026-10-25.md proposal 5 (2026-10-25) — routed still-open defects (D24-1, D24-4, D24-5, R25-1…R25-5) and carried debt (entry deletion shrinks the audited set while passing; `source-recheck.py --source` single-valued) are named without runnable closure checks, so nothing distinguishes open from closed; the proposal would run each closure check daily, read-only, and report flips. |

## Round-31 additions — closure checks and one-limb mutants

| id | criterion | grounded in |
|---|---|---|
| R16 | A result paragraph that states an open failure or an exit code carries its runnable closure check (`bash -n`-parseable) in the same record; when a later state change closes it, closure is an appended erratum that names that paragraph by its own wording and cites the corrected output, with the filed paragraph left byte-identical — a check that turns green because the stale sentence was reworded or deleted has closed nothing. The check exits non-zero while the statement stands un-errataed and zero once the naming erratum carrying the corrected output is present. | `corpus/lessons/round-31.md` § Mistakes M31-1 — stale premise; the round-30 paragraph at `SCORECARD.md:813` (stale reading on `:814`) still said `expect=present expected=43 missing=0 unexpected=0 exit=1` after `corpus/lessons/round-30.md` § Close-out erratum had corrected the audit to `strict pass=43/43`; routed by `corpus/lessons/round-30-verifier-spotcheck.md` §1 defect 3 and §5 item 4. Specimen `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` → `ExecErratumCheck-after.txt` on `SCORECARD.md` `cac64dbd…` → `5fa41aef…` (835 → 860 lines, append-only): red `file=SCORECARD.md stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0` / `erratum_closure=open`, `EXIT CODE: 1`; green `file=SCORECARD.md stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1` / `erratum_closure=closed`, `EXIT CODE: 0`, and the mutant that deletes the erratum block returns exit 1. Limit measured here: on the base bytes reworded once with no erratum the same check printed `erratum_closure=closed` and exited 0 (`stale_paragraphs=0`), so only the naming-erratum branch is closure under this criterion. |
| R17 | An instrument limb is claimed load-bearing only when a committed one-limb mutant makes that limb's kill command differ from the unmutated run: the mutant is an exact-once `find`/`replace` over the instrument's own bytes that still compiles (`py_compile`), and the replay `corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` prints one `LIMB <id>` line per limb and rejects all three degenerate controls (no-op patch, non-compiling patch, semantically equivalent patch). A limb no mutant can move is a survivor: the owning instrument's selftest is strengthened with a case that fails only on that limb, and a survivor is never relabelled killed. | R13; `corpus/lessons/round-31.md` § Mistakes (the round-31 survivor/limb entries); round-30 `corpus/lessons/round-30.md` § Mistakes M30-1 — the frozen B2 fixture declared `id=S045` with `path=B2.txt`, so the B1 stem limb exited first and the B2 mutant's flip was `NO` on the frozen bytes, i.e. that limb was never isolated. Specimen `.ufo/waves/round-31/wave1/ledger-fragments/ra.json` `RA-completeness`: “On the pre-round-31 bytes this was the one RA survivor (mutant compiled, find once, exit 0, stdout byte-identical to pristine)”, closed by the two `main()`-level fixtures `complete-empty` and `complete-missing-line` rather than by relabelling. |

## Round-31 wave-2 additions — byte-bound closure checks (append-only)

| id | criterion | grounded in |
|---|---|---|
| R18 | A closure check for a filed result paragraph binds three byte facts and has no count-zero escape: (i) the span the paragraph was filed at still hashes to the digest pinned when it was filed, so deleting it, or rewording it in place, leaves the item open; (ii) a naming erratum anchored on an `Errata`/`Erratum` line after the span quotes the paragraph's wording and cites its filed `FILE:start-end` address; (iii) the corrected-output citation is bound to the instrument bytes that print it — a `strict pass=` reading at or after the filed span carries, on its line or within the two lines above it, the value that instrument prints now, that instrument's 8-hex digest and the filed address, so a changed instrument re-opens the check until a labelling entry cites the new triple while a stale, fabricated or address-less pair stays open. For a missing-entry closure the entry is the file's own entry level (`## `): an `###` sub-section that only mentions the round does not close it. | supersedes R16 — R16 stated the rule but never bound its check to it: the shipped CHECK A closed on `[ "$n" -eq 0 ] \|\|`, its own disclosed `R-1` limit (`.ufo/waves/round-31/wave1/ExecErratumCheck.md` §1, §5), so the clause "a check that turns green because the stale sentence was reworded or deleted has closed nothing" (`corpus/QUALITY.md:95`) had no conforming specimen. Measured before the tightening: base bytes minus the filed paragraph, no erratum, printed `erratum_closure=closed` exit 0 (`.ufo/waves/round-31/wave2/CritMistakes.md` §2.1, `.ufo/waves/round-31/wave2/MutErratumCheck.md` §2 mutant (c)); the round-30 `##` entry relabeled `## Round 29` still closed through the `### Round-30 checks re-run` note (`MutErratumCheck.md` §2 mutant (d1), `CritMistakes.md` §3); and the erratum's `strict pass=43/43` is superseded by `strict pass=44/44` from `recheck-audit.py` `5d4842da…` while CHECK A required the historical literal (`CritMistakes.md` §4). Tightened matrix, 11 byte-states, in `.ufo/waves/round-31/wave2/ScribeQualityFix.md` §2–§3 and re-measured on drifted `SCORECARD.md` `4076091c…` in 13 byte-states under the address-bound window form (§8): landed `SCORECARD.md` `5fa41aef…` exits 1 on `live_citation_self_naming=0` and exits 0 once the labelling erratum is appended in a scratch copy; the five mutants the shipped check passed — paragraph deleted, `exit=1`→`exit=0` reword, unrelated r31 erratum quoting both phrases, phrase and erratum both removed, fabricated live-pair line — all exit 1; the erratum-deleted control, the base bytes, a wrong-digest label and a stale-value label stay exit 1. CHECK B' keeps landed `LOG.md` `864deb7d…` at exit 0 (`round30_h2_headings=1`) and flips the relabeled-heading, entry-body-deleted and h3-only-backfill shapes 0 → 1; the h3 tolerance `R-2` disclosed is withdrawn. |
| R19 | A specimen figure quoted inside a record row is either produced by a command the row cites or backed by a closure check that reproduces it; a literal the instrument never prints is a stale premise under R18 and is corrected by an appended row that names the stale literal and carries the command that computes the live figure — never by editing the filed row. | supersedes R13 — R13's specimen cites `selftest cases=4 failures=0 exit=0`, a summary shape `recheck-audit.py` has never printed: `grep -cE '^selftest cases='` on its output → 0, while the live `--selftest` prints 18 `selftest … ok` case lines at exit 0 (measured 2026-10-26T00:41Z on instrument `5d4842da…`); routed by `.ufo/waves/round-31/wave1/ScribeQuality.md` F1 and `.ufo/waves/round-31/wave2/CritMistakes.md` §6 (M31-4). Closure check below: pre-append bytes exit 1 (`supersedes_r13_rows=0`); a stub row naming R13 without a command also exits 1; this row and the two commands under R18 exit 0. R13's criterion text and its bite are unchanged and stay in force; only its specimen evidence is superseded. |

### R18 — runnable closure checks (`bash -n`-parseable, `cd`-prefixed, no lane write)

CHECK A' — `SCORECARD.md` `recheck-audit open item` paragraph. `$1` names the file under test
(default: the lane copy); a scratch copy is what the mutant controls run:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
f=${1:-SCORECARD.md}
pin=d6c6ea77c9450bfc6886bf75e5f5b48e9056e1bd9cd213febea31e25a206a7b1
d=$(sed -n '813,819p' "$f" | sha256sum | cut -d' ' -f1)
n=$(grep -c 'recheck-audit open item' "$f")
l=$(grep -nE '(([Rr]31)|([Rr]ound[- ]31))[[:space:]]+[Ee]rrata?' "$f" | head -1 | cut -d: -f1)
c=0
[ -n "$l" ] && tail -n +"$l" "$f" | grep -q 'recheck-audit open item' \
  && tail -n +"$l" "$f" | grep -q 'SCORECARD\.md:813-819' && c=1
live=$(python3 corpus/instruments/recheck-audit.py --quiet 2>&1 | grep -o 'strict pass=[0-9]*/[0-9]*' | head -1)
inst=$(sha256sum corpus/instruments/recheck-audit.py | cut -c1-8)
b=0
for k in $(awk 'NR>=813 && /strict pass=/ {print NR}' "$f"); do
  win=$(awk -v k="$k" 'NR>=k-2 && NR<=k' "$f")
  printf '%s\n' "$win" | grep -qF "$live" && printf '%s\n' "$win" | grep -qF "$inst" \
    && printf '%s\n' "$win" | grep -q 'SCORECARD\.md:813-819' && { b=1; break; }
done
printf 'file=%s filed_byte_identical=%s phrases=%s anchor=%s naming_erratum=%s live_citation_self_naming=%s live=%s instrument=%s\n' \
  "$f" "$([ "$d" = "$pin" ] && echo y || echo n)" "$n" "${l:-none}" "$c" "$b" "$live" "$inst"
[ "$d" = "$pin" ] && [ "$n" -ge 2 ] && [ "$c" -eq 1 ] && [ "$b" -eq 1 ] \
  && { echo "erratum_closure=closed"; exit 0; }
echo "erratum_closure=open"; exit 1
```

CHECK B' — round-30 `LOG.md` entry, gated on the entry level:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
f=${1:-LOG.md}
h2=$(awk '/^## /{ h=$0; sub(/^## */,"",h); if (match(h,/[Rr]ound[- ]?[0-9]+/)) { t=substr(h,RSTART,RLENGTH); gsub(/[^0-9]/,"",t); if (t+0==30) n++ } } END{print n+0}' "$f")
h23=$(awk '/^#{2,3} /{ h=$0; sub(/^#{2,3} */,"",h); if (match(h,/[Rr]ound[- ]?[0-9]+/)) { t=substr(h,RSTART,RLENGTH); gsub(/[^0-9]/,"",t); if (t+0==30) n++ } } END{print n+0}' "$f")
printf 'file=%s round30_h2_headings=%s round30_h2_or_h3_headings=%s\n' "$f" "$h2" "$h23"
if [ "$h2" -ge 1 ]; then echo "log_closure=closed"; exit 0; else echo "log_closure=open"; exit 1; fi
```

### R19 — closure check for the R13 specimen figure

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
q=${1:-corpus/QUALITY.md}
live=$(python3 corpus/instruments/recheck-audit.py --selftest 2>&1 | grep -c '^selftest .* ok$')
sum=$(python3 corpus/instruments/recheck-audit.py --selftest 2>&1 | grep -cE '^selftest cases=[0-9]+ failures=[0-9]+')
sup=$(grep -cE '^\| R[0-9]+ \| .*supersedes R13 ' "$q")
cmd=$(grep -E '^\| R[0-9]+ \| .*supersedes R13 ' "$q" | grep -c -- '--selftest')
printf 'live_selftest_ok_lines=%s instrument_cases_summary_lines=%s supersedes_r13_rows=%s row_cites_selftest=%s\n' "$live" "$sum" "$sup" "$cmd"
[ "$sum" -ge 1 ] || { [ "$sup" -ge 1 ] && [ "$cmd" -ge 1 ]; } && { echo "r13_specimen_closure=closed"; exit 0; }
echo "r13_specimen_closure=open"; exit 1
```

## Round-33 additions — a capture snapshot ships with its manifest (append-only)

These two rows widen R13/R14 from instruments to captures: a round's capture evidence is
admissible only with the binding metadata that lets a later reader tell a real capture from a
fabricated one. They add no new Q/R bar to entries already admitted, and they supersede no
earlier row.

| id | criterion | grounded in |
|---|---|---|
| R20 | A capture snapshot directory ships its `manifest.json` in the same round and the same commit that adds its captured files. Every manifest record carries a `url` matching exactly one `corpus/SOURCES.md` registry-row URL and one fetch-provenance field: `fetched_utc` for a round-32-or-later capture, a declared `archival: true` for an older one whose exact fetch instant was not recorded. A snapshot dir with no manifest, or a record with neither `url` nor provenance, is a defect of the round that landed it, and it is repaired by appending that round's manifest and landing the checker in the same round — never by re-freezing the claim that reads manifests into a lower record count. | M33-1 (`corpus/lessons/round-33.md` § Mistakes; frozen statement `.ufo/waves/round-33/claims.json` → `non_claim_frontier_items.mistake`); `corpus/lessons/round-32-verifier-spotcheck.md:93` D5 — "are committed without a `round-32/manifest.json`" and "so the 38-record target is not silently moved" — plus the base measurement below: `manifest_records=38 with_url=0 with_fetched_utc=0 archival_true=0`, `snapshot_dirs_without_manifest=1` (`corpus/source-snapshots/round-32`, holding `S049.txt` and `S050.txt`), measured on base `690b69da…`. |
| R21 | A sourced claim's capture manifest carries the provenance that lets a re-verifier separate a fabricated capture from a real one: a `url` the registry row independently names, and a fetch instant the capture commit dates. A counter set that binds only local bytes and shape counts (entry count, registry-row count, `occurrences=1`) is not evidence that the capture is real; until the manifest carries those fields, the claim states that limit instead of reading the passing counters as a capture check. | `corpus/lessons/round-31.md:146` open item 4 — "manifest `url`/`fetched_utc` fields and a census URL↔capture comparison" — after `.ufo/waves/round-31/wave1/CritC2Kill.md:232` §6 item 2 — "No URL↔capture binding anywhere": that seat's junk construction (invented capture + manifest + entry + frontier and registry rows) passed all seven C2 counters; M33-1 (`corpus/lessons/round-33.md` § Mistakes). |

### R20 / R21 — the base measurement both rows rest on (read-only, replayable)

`$1` is the revision to measure; the default is the round-33 claims base. The command prints one
line, writes nothing, and needs only `git` and `python3`:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
rev=${1:-690b69dae23ab9f4ccf056ba2d619cadc2abb3c4}
python3 - "$rev" <<'PY'
import json, subprocess, sys
rev = sys.argv[1]
g = lambda *a: subprocess.run(['git', *a], capture_output=True, text=True).stdout
dirs = g('ls-tree', '--name-only', '-d', rev, 'corpus/source-snapshots/').split()
tot = u = fut = arch = 0
naked = []
for d in dirs:
    files = [f.rsplit('/', 1)[-1] for f in g('ls-tree', '--name-only', f'{rev}:{d}').split()]
    mans = [f for f in files if f.endswith('manifest.json')]
    if not mans and any(f.endswith('.txt') for f in files):
        naked.append(d)
    for m in mans:
        doc = json.loads(g('show', f'{rev}:{d}/{m}'))
        recs = doc.get('sources', []) if isinstance(doc, dict) else doc
        for r in recs:
            tot += 1; u += 'url' in r; fut += 'fetched_utc' in r; arch += r.get('archival') is True
print(f'dirs={len(dirs)} manifest_records={tot} with_url={u} with_fetched_utc={fut} '
      f'archival_true={arch} snapshot_dirs_without_manifest={len(naked)} names={",".join(sorted(naked))}')
PY
```

Base output (measured 2026-10-26 against `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`):

```
dirs=9 manifest_records=38 with_url=0 with_fetched_utc=0 archival_true=0 snapshot_dirs_without_manifest=1 names=corpus/source-snapshots/round-32
```

The R20 recheck on a landed round is that round's committed checker —
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py` —
whose rule A supplies the manifest clause, rule B the one-registry-row `url` clause and rule C the
provenance clause. At round-33 composition the checker was absent from the base
(`git cat-file -e 690b69da:corpus/instruments/capture-binding-check.py` → exit 128), so no landed
verdict is claimed by these rows; a later reader runs the command and reads its own output.

## Round-34 additions — pre-freeze satisfiability and reflection cadence (append-only)

R6 form: R20's row (line 169) and every earlier line stay byte-identical; the R20 note and the two
rows below are appended at the end of the file.

Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-id
reading — a URL shared by two different registry rows is informational `multi_row_url=N`, not a
failure (SCORECARD round-33 section, erratum 2).

| id | criterion | grounded in |
|---|---|---|
| R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. Grounded in: round-33 verifier R2; M34-2. | `corpus/lessons/round-33-verifier-spotcheck.md:167-169` (R2 — the frozen parenthetical that literally read `bound=38`); M34-2 at `.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.mistake` |
| R23 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. Grounded in: considerthese/2026-10-25.md proposal 6. | `considerthese/2026-10-25.md:76` proposal 6 (2026-10-25) |
| R24 | A counter's mutant kill rule is recorded and tightened: the selftest clause requires one `selftest case=<name>` verdict line per case with cases>=11, so a summary-only forgery (cases=0 failures=0) cannot satisfy it. | `corpus/lessons/round-33-verifier-spotcheck.md:174-176` (R4) and the round-34 erratum at `corpus/lessons/round-33.md:215-226` — the frozen rule **caught 3 of 4**, skip-selftest (M4) survived (`.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75,172`, finding F-5); M34-1 at `.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.mistake` (the 'all mutants killed' overstatement) |
| R25 | A frozen claim's literal constants are checked for satisfiability against base bytes **plus the round's declared after-adds** (a new registry row the claim itself adds, a manifest record it lands): a literal true at base but false at the declared after-state is fixed before data, never waived by a post-freeze erratum. Grounded in: M34-3 (`.ufo/waves/round-34/mistakes-erratum-1.md`). | M34-3 at `.ufo/waves/round-34/mistakes-erratum-1.md` (the C1 `records=40` literal was true at base and false at the declared after-state `records=41`) |
