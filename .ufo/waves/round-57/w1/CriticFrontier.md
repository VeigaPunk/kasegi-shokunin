VERDICT: YES — a degenerate entry passes the frozen C2 kill rule: probe (a2), a one-line-stub entry (all 4 falsifiable claims, distinctness and limits removed; only "S089" and "S090" named in prose) still prints `FRONTIER-PASS F38 ids=S089,S090` + `entries=41 pass=41 exit=0`. Probes (a1), (b), (c), (d) fail as designed — (a2) is the only passing probe. All three checked anchors verify. The tokens all/every/complete/no occur 0 times as words in the C2 entry; the quantifier load sits on "any"×3 and "each"×5, which the counters do enumerate. A do-nothing tree cannot reach the after-state.

Tooling record: no tool installed or upgraded (system python3 and git sufficient; pacman paused, nothing needed).

Throughout: L = /home/vgpnk/Projects/shokunin/kasegi-shokunin, W = L/.ufo/waves/round-57/w1, S = /fast/scratch/hyaku/kasegi-r57/CriticFrontier. The lane was never written; all mutations were in S/probe (copies).

## 1. Frozen C2 entry read

- File: L/.ufo/waves/round-57/claims.json:28-52 (entry id C2 at :29; axis coverage, kind frontier-admission; frozen_sentence :34; before :35; after :36; kill_rule :37; counting_commands :38-50). Freeze commit 6343e2c3882a96b1af86e1ecf4c9deba33361719 per the round contract; claims.json untouched.
- Kill rule (claims.json:37), decisive limbs for this attack: counter must print `FRONTIER-PASS F38 ids=S089,S090`, rows=38, registry=90, entries=41, pass=41, exit=0; source-recheck exits 0 with occurrences=1 per Q line; capture-binding records=73 bound=73; sha pins; sort -c; README/PROVINCE/SOURCES diffs "show any modified or deleted pre-existing line (pure additions and inserts only)"; ISO lead-line bytes/exact-line sha unchanged.
- Note: the knowledge entry corpus/knowledge/iso-29147-30111-standard-records.md is a NEW file this round (do-nothing control reads knowledge files 75 at base, after-state 76), so a stub body modifies no pre-existing README/PROVINCE/SOURCES line and cannot trip the diff limb.

## 2. Probe tree and baseline

Commands:
- `S=/fast/scratch/hyaku/kasegi-r57/CriticFrontier; rm -rf "$S"; mkdir -p "$S/probe" && cp -r L/corpus "$S/probe/corpus" && cp L/PROVINCE.md "$S/probe/PROVINCE.md" && cp L/SKILL.md "$S/probe/SKILL.md"` → exit 0 (12M copied).
- `python3 corpus/instruments/frontier-recheck-count.py --help` → real root flag is `--root ROOT` (also --json, --selftest, --scratch); exit 0. `source-recheck.py --help` → `--manifest`, `--source`, `--selftest`; exit 0.
- Baseline: `cd "$S/probe" && TMPDIR="$S" python3 corpus/instruments/frontier-recheck-count.py --root "$S/probe"` →
  ```
  FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90
  FRONTIER-PASS F38 ids=S089,S090
  PASS     F38  knowledge/iso-29147-30111-standard-records.md  ids=S089,S090  exit=0
  entries=41 pass=41 exit=0
  ```
  exit=0. The probe copy reproduces the after-state exactly, so probes isolate the mutation.

Counter internals (L/corpus/instruments/frontier-recheck-count.py): shape rules at :250-261 (`not-a-recheck-invocation` when the line lacks `source-recheck.py` or contains `--selftest`, :250-251; `header-sources-not-rechecked` :256-257; `selection-not-declared-by-entry` :258-259; `selection-not-cited-by-entry` :260-261 — recheck ids must be mentioned SOMEWHERE in non-declaration entry text); execution `subprocess.run(["bash","-c",recheck], cwd=root, ...)` :269-271 (the entry's own `cd L && ...` prefix pins execution to the lane root even in a probe tree); registry limb `source-id-absent:<id>` :339-340; entry_contract :151 reads ONLY `source:`/`recheck:` lines, evidence bullets, and bare S-id tokens (:24-32 regexes) — it never parses the entry's prose substance. That last fact is what the probes below exercise.

## 3. Degenerate-entry probes (each: restore pristine, mutate, run the counter; exit codes printed)

Mutant files built byte-exactly from `$S/pristine/knowledge.md` (copy of the lane file; header = lines 1-7: title, blank, `source: S089` :3, `source: S090` :4, `verified-at:` :5, `ground: F38` :6, `recheck:` :7) and `$S/pristine/SOURCES.md` (S089 row :96, S090 row :97). Counter command each time: `cd "$S/probe" && TMPDIR="$S" python3 corpus/instruments/frontier-recheck-count.py --root "$S/probe"`.

(a1) Body replaced by ONE stub line with no S-id:
`{ head -n 7 "$S/pristine/knowledge.md"; printf '%s\n' '(stub body: CriticFrontier probe a1 - the four falsifiable claims, the distinctness notes and the limits of this entry are removed)'; } > "$K"`
→ `FAIL F38 ... problems=selection-not-cited-by-entry`; `FRONTIER-FAIL F38 status=admitted ... problems=missing-pass-line`; `entries=41 pass=40 exit=1`; exit=1. FAILS (citation limb holds when the ids are not even mentioned).

(a2) Body replaced by ONE stub line naming the ids in prose:
`{ head -n 7 "$S/pristine/knowledge.md"; printf '%s\n' '(stub body: CriticFrontier probe a2 - the four falsifiable claims, the distinctness notes and the limits are removed; only the sources S089 and S090 are named here)'; } > "$K"`
Mutant proven a stub: `wc -l` = 8; `##` headings = 0; body lines after header = 1 (the printed stub line).
→ `FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90`; `FRONTIER-PASS F38 ids=S089,S090`; `PASS F38 knowledge/iso-29147-30111-standard-records.md ids=S089,S090 exit=0`; `entries=41 pass=41 exit=0`; exit=0. **PASSES — degenerate.** The counter's only substance signal for the body is that the two ids appear once each in prose; zero claims, zero anchors, zero limits survive. (The PASS record's `exit=0` is the recheck line executing against the lane captures via its absolute `cd` prefix — the entry↔capture binding still holds; what passes degenerately is the ENTRY BODY. No other C2 counting command reads the entry body either: source-recheck reads manifest+snapshots only; capture-binding-check binds manifest records to SOURCES.md rows and fetch provenance per its docstring (capture-binding-check.py:1-9); the knowledge-expected command counts path lines; sha/wc read capture bytes. So the whole C2 kill rule is satisfiable with this stub [the non-counter limbs from documented inputs; the counter limb probe-demonstrated].)

(b) Delete only the `source: S090` header line (knowledge :4):
`{ head -n 3 "$S/pristine/knowledge.md"; tail -n +5 "$S/pristine/knowledge.md"; } > "$K"`
→ `FAIL F38 ... ids=S089 problems=selection-not-declared-by-entry` (the recheck line still selects S090; reverse direction of rule A fires); `FRONTIER-FAIL F38 ... problems=missing-pass-line`; `entries=41 pass=40 exit=1`; exit=1. FAILS.

(c) Recheck line points at --selftest (header :7 replaced, everything else original):
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --selftest   # probe c: recheck points at --selftest, binds nothing`
→ `FAIL F38 ... problems=not-a-recheck-invocation,no-source-selection` (rule C :250-253 rejects --selftest and the missing --source explicitly); `FRONTIER-FAIL F38 ... problems=missing-pass-line`; `entries=41 pass=40 exit=1`; exit=1. FAILS. A recheck that binds nothing cannot green an entry.

(d) Delete the S090 registry row (SOURCES.md :97):
`{ head -n 96 "$S/pristine/SOURCES.md"; tail -n +98 "$S/pristine/SOURCES.md"; } > "$S/probe/corpus/SOURCES.md"`
→ `FRONTIER-CENSUS rows=38 admitted=38 closed=37 problem-rows=1 registry=89`; `FRONTIER-FAIL F38 status=admitted ids=S089,S090 problems=source-id-absent:S090` (registry limb :339-340; note the per-entry record still PASSes — the row-level registry limb is what fails); `entries=41 pass=41 exit=1`; exit=1. FAILS (exit!=0 and registry=89≠90 both trip the kill rule).

Restore check after probes: pristine tree re-run → `entries=41 pass=41 exit=0`; exit=0 (probe tree unharmed).

Probes that pass: (a2) only.

## 4. Anchor check (Claims 1-3 anchors, lane snapshots, read-only)

- `sed -n '84p' L/corpus/source-snapshots/round-57/S089.txt` → `This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services. ...` — matches the entry's Claim 1/3 anchor `S089.txt:84 Q2` (abstract scope sentence). EXIT 0. VERIFIED.
- `sed -n '204p' L/corpus/source-snapshots/round-57/S089.txt` → `ISO/IEC AWI 29147` — matches Claim 2 anchor `S089.txt:204 Q7` (successor work). EXIT 0. VERIFIED.
- `sed -n '197p' L/corpus/source-snapshots/round-57/S090.txt` → `ISO/IEC WD 30111.2` — matches Claim 2 anchor `S090.txt:197 Q6` (successor work). EXIT 0. VERIFIED.
All three expected word sets sit exactly on the cited lines; the anchors are not dangling.

## 5. Universal clauses (case-insensitive, C2 entry lines claims.json:28-52)

| token | word-form hits | substring artifacts | counter enumerates the coverage? |
|---|---|---|---|
| `all` | 0 | `LC_ALL=C` (claims.json:36,37,47 — sort env var, not a clause); `paywalled` (:34) | n/a — no `all`-clause exists |
| `every` | 0 | none | n/a |
| `complete` | 0 | none | n/a |
| `no ` | 0 | none (`\bno\b` count 0; negations are phrased "lacks", "differs", "!= 0") | n/a |
| (actual quantifiers) | `any` ×3 — all in kill_rule (:37): "if any of", "any Q line lacks occurrences=1", "any modified or deleted pre-existing line" | `each` ×5 — :34 ×2 ("each standard", "7+7 Q assertions each occurrences=1"), :3/:4 ("7 assertions Q1-Q7, each occurrences=1"), :36 ("each exit 0 with 7 Q-OK lines") | yes for both: rule G prints one FRONTIER-PASS/FAIL line per README F-row whatever its status (counter :334-343, docstring :37-49); source-recheck emits one sha256-OK + one Q-OK line per pinned quote with occurrences= and exits 1 if any Q line lacks occurrences=1 (probe executions exited 0; per-line print is the instrument's documented output); the README/PROVINCE/SOURCES limb is a byte diff over every pre-existing line; capture-binding walks every snapshot file and manifest record (:1-9 docstring) |
Command: `sed -n '28,52p' claims.json | grep -o -i -E '\b(any|each|every|all|complete|no)\b' | sort | uniq -c` → `3 any`, `5 each`, nothing else. The C2 frozen sentence carries no all/every/complete/no-universal that a counter could silently under-enumerate; the binding quantifiers are any/each and they are enumerated line-by-line by the instruments.

## 6. Do-nothing reach (L/.ufo/waves/round-57/controls/do-nothing-c2-r57.txt, rev 2)

No — a do-nothing tree cannot reach the C2 after-state. The control records the base bytes (commit eae1d614…) printing `FRONTIER-CENSUS rows=37 admitted=37 closed=37 problem-rows=0 registry=88` + `entries=40 pass=40 exit=0`, F38 rows 0, knowledge files 75, expected 75, capture-binding over a pure base export `records=71 bound=71 unbound=0`. The after-state demands rows=38, registry=90, `FRONTIER-PASS F38 ids=S089,S090`, entries=41 pass=41, capture-binding records=73 bound=73, knowledge files 76/expected 76 — every one of those is a live read of tree bytes that must contain, at minimum, the F38 README row (probe README.md:938), the two S089/S090 registry rows (SOURCES.md:96-97), the 41st entry file, the two capture files plus manifest, and the 76th knowledge file with its expected-path line. None exists at base (zero F38 rows, 75 files, 71 records), and the rule-G census enumerates every README row whatever its status, so no status or visibility trick can hide the missing row; the very first counting command already fires the kill rule on rows=37≠38, registry=88≠90 and the absent `FRONTIER-PASS F38` line. The only degenerate route this seat found is not do-nothing but do-less: the after-state's file set present with stub content (probe a2).

## 7. Smallest safe correction (report only — nothing edited, per contract)

The hole is the citation limb (:260-261): `recheck_ids ⊆ cited`, where `cited` is any bare `S\d{3,}` token in non-declaration text — so a single prose mention of each declared id substitutes for substance (probe a2). Smallest correction: require each rechecked id to be anchored by a declaration-shape or capture-anchor form — i.e. compute `cited` from evidence bullets and `<id>.txt:<line>` capture-path mentions (the regex the docstring already names at :69-70) instead of any S-token, or add a rule-A limb `selection-only-prose-mentioned` firing when an id appears in `cited` but in neither `declared` nor `evidence` nor a capture-path mention. The selftest already has the fixture vocabulary for this (`evidence-list-declares-selection`, :436-437; prose-only mention case :432-433), so the change is one limb plus one case. Everything else in the C2 counter held under attack: bidirectional rule A ((a1),(b)), rule C's --selftest rejection ((c)), the registry limb ((d)), and rule G's per-row enumeration. This is a fixable defect of the counter, not a tradeoff: the frozen kill rule's intent (an entry with "4 falsifiable claims") is not machine-checked for even one of the four.

Scratch: S was deleted before yield (`rm -rf -- "$S"`); no leftovers outside W/CriticFrontier.md. No credential material anywhere in this file.
