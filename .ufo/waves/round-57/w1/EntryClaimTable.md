VERDICT: ok / admitted — 53 of 53 claim-bearing rows verify against the committed snapshots (yes=53, no=0); 0 quotes over 25 words; 2 anchor-precision findings reported as text only (the entry was NOT edited).

# EntryClaimTable — F38 claim-versus-source table (round 57, wave 1)

Seat: EntryClaimTable (leaf member; no subagent dispatch).
Lane: kasegi. Frozen claims: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/claims.json` (read-only; never edited).
Subject under test (read-only): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/iso-29147-30111-standard-records.md` — the F38 entry, Claims 1 to 4 at entry lines 17-70.
Sources checked (committed, read-only): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57/S089.txt`, `.../S090.txt`, `.../manifest.json`.
Scratch: `/fast/scratch/hyaku/kasegi-r57/EntryClaimTable` (created with `mkdir -p`; deleted on yield — see §7).

No tooling was installed or upgraded for this seat, so no tool/channel/version/reason row is owed under the operator tooling directive (`/home/vgpn/.omp/agent/RULES.md` was read; it is install-only and no install was needed — every command here is coreutils `grep`/`wc`/`sed`/`awk`/`python3` already present on the host).

## 0. Provenance and scope of the checked bytes

1. Command:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse --show-toplevel && git status --porcelain && git rev-parse HEAD`
   Output (decisive lines):
   ```
   /home/vgpnk/Projects/shokunin/kasegi-shokunin
    M LOG.md
    M SCORECARD.md
   cd3029876eac7189aaff0d32b26031c0defa35aa
   ```
   Exit code 0. The two modified files (LOG.md, SCORECARD.md) are fleet-root lane files owned by other seats — NOT touched by this seat. The subject entry and the snapshot dir are clean at HEAD (shown in command 2), so the bytes checked below are the committed bytes.

2. Command:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff --stat HEAD -- corpus/source-snapshots/round-57/ && git diff --stat HEAD -- corpus/knowledge/iso-29147-30111-standard-records.md && git ls-files corpus/source-snapshots/round-57/ corpus/knowledge/iso-29147-30111-standard-records.md`
   Output: both `git diff --stat` invocations printed nothing (empty = worktree identical to HEAD); `git ls-files` printed:
   ```
   corpus/source-snapshots/round-57/S089.txt
   corpus/source-snapshots/round-57/S090.txt
   corpus/source-snapshots/round-57/manifest.json
   corpus/knowledge/iso-29147-30111-standard-records.md
   ```
   Exit code 0. All three capture files and the entry are tracked and unmodified.

3. Command (worktree vs HEAD digest identity):
   `for f in S089 S090; do git show HEAD:corpus/source-snapshots/round-57/$f.txt | sha256sum; sha256sum corpus/source-snapshots/round-57/$f.txt; done`
   Output:
   ```
   17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  S089 HEAD=
   17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  S089 WORK=
   2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  S090 HEAD=
   2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  S090 WORK=
   ```
   Exit code 0. Both committed snapshots hash to the digests the frozen claim C2 pins (claims.json `sha256sum of S089.txt differs from 17ee9c41…` / `2074d3a1…`), so the capture bytes this seat verified are the bytes the frozen kill rule names.

4. Command:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57 && wc -c S089.txt S090.txt && wc -l S089.txt S090.txt && sha256sum S089.txt S090.txt`
   Output:
   ```
    6647 S089.txt
    5598 S090.txt
   12245 total
     268 S089.txt
     261 S090.txt
    529 total
   17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  S089.txt
   2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  S090.txt
   ```
   Exit code 0. Snapshot byte counts 6647 / 5598 match the entry header (`corpus/knowledge/iso-29147-30111-standard-records.md:3-4`) and the frozen claim C2 `after` field; line counts 268 / 261 match manifest `lines`.

5. Command:
   `python3 -c "import json;d=json.load(open('.../manifest.json'));[print(s['id'],'bytes=',s['bytes'],'snapshot_bytes=',s['snapshot_bytes'],'lines=',s['lines'],'nquotes=',len(s['quotes']),'fetched=',s['fetched_utc'],'http=',s['http']) for s in d['sources']]"`
   Output:
   ```
   S089 bytes= 88964 snapshot_bytes= 6647 lines= 268 nquotes= 7 fetched= 2026-11-03T18:04:24Z http= {'status': 200, 'final_url': 'https://www.iso.org/standard/72311.html'}
   S090 bytes= 87845 snapshot_bytes= 5598 lines= 261 nquotes= 7 fetched= 2026-11-03T18:04:24Z http= {'status': 200, 'final_url': 'https://www.iso.org/standard/69725.html'}
   ```
   Exit code 0. The entry header's `88964 fetched` / `87845 fetched`, `6647 snapshot bytes` / `5598 snapshot bytes`, `recorded fetch 2026-11-03T18:04:24Z, HTTP 200` and `manifest … (7 assertions Q1-Q7…)` assertions all agree with the manifest.

## 1. The claim-versus-source table (Claims 1 to 4)

Every row's line number was taken from `grep -n` output over the committed snapshot (never from memory); every quote was copied exactly from the snapshot text; every `occ` count is `grep -c -F` (or an exact Python `str.count` over the whole file, equivalent for these fixed strings) and every anchor cell is the entry's own inline citation.

Command that produced the row data (one script, exit code 0):
```
python3 - <<'PY'   # reads SNAP/S089.txt, SNAP/S090.txt line arrays; for each row it
                   # computes the grep -n line list of the exact quote, the whole-file
                   # occurrence count, and whether the entry's cited anchor line
                   # contains the quoted words
PY
```
The snapshot path used throughout: `SNAP=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57`.

Legend for `anchor carries quote`: whether the entry's own inline anchor line contains the quoted words (the item-5 check).

### Claim 1 — identity and edition (entry lines 19-29)

| row | asserted fact | quote copied exactly from the snapshot | snapshot line no. (grep -n) | occ | match | anchor carries quote |
|---|---|---|---|---|---|---|
| R01 | 29147 identity string `ISO/IEC 29147:2018` | `ISO/IEC 29147:2018` | S089: 49,52,58,60,66,67,115,212 (+1,82) | 10 | yes | anchor `S089.txt:54` -> **no** (see F1) |
| R02 | 29147 title `Information technology — Security techniques — Vulnerability disclosure` | `Information technology — Security techniques — Vulnerability disclosure` | S089: 1, 53, 61 | 3 | yes | anchor `S089.txt:54` -> **no** (see F1) |
| R03 | 29147 edition 2 | `Edition 2` | S089: 54, 63 | 2 | yes | yes (`:54` = `Edition 2`) |
| R04 | 29147 publication date 2018-10 | `2018-10` | S089: 55, 97, 164, 169, 172 | 5 | yes | yes (`:97` = `: 2018-10`) |
| R05 | 29147 reference 72311 | `72311` | S089: 59, 68 | 2 | yes | yes (`:59` = `72311`) |
| R06 | 29147 32 pages | `: 32` (label `Number of pages` at :102) | S089: 103 | 1 | yes | yes (`:103` = `: 32`) |
| R07 | 29147 abstract scope sentence (manifest Q2) | `This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services.` | S089: 84 | 1 | yes | yes (`:84`) |
| R08 | 29147 -> 30111 cross-reference (manifest Q3) | `Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111.` | S089: 91 | 1 | yes | yes (`:91`) |
| R09 | 30111 identity string `ISO/IEC 30111:2019` | `ISO/IEC 30111:2019` | S090: 49,52,58,60,66,67,108,205 (+1,82) | 10 | yes | anchor `S090.txt:54` -> **no** (see F1) |
| R10 | 30111 title `Information technology — Security techniques — Vulnerability handling processes` | `Information technology — Security techniques — Vulnerability handling processes` | S090: 1, 53, 61 | 3 | yes | anchor `S090.txt:54` -> **no** (see F1) |
| R11 | 30111 edition 2 | `Edition 2` | S090: 54, 63 | 2 | yes | yes (`:54` = `Edition 2`) |
| R12 | 30111 publication date 2019-10 | `2019-10` | S090: 55, 90, 165 | 3 | yes | yes (`:90` = `: 2019-10`) |
| R13 | 30111 reference 69725 | `69725` | S090: 59, 68 | 2 | yes | yes (`:59` = `69725`) |
| R14 | 30111 13 pages | `: 13` (label `Number of pages` at :95) | S090: 96 | 1 | yes | yes (`:96` = `: 13`) |
| R15 | 30111 abstract scope sentence (manifest Q2) | `This document provides requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service.` | S090: 84 | 1 | yes | yes (`:84`) |
| R16 | 29147 technical committee `ISO/IEC JTC 1/SC 27` | `ISO/IEC JTC 1/SC 27` | S089: 105 | 1 | yes | yes (`:105`) |
| R17 | 30111 technical committee `ISO/IEC JTC 1/SC 27` | `ISO/IEC JTC 1/SC 27` | S090: 98 | 1 | yes | yes (`:98`) |
| R18 | 29147 ICS `35.030` | `35.030` | S089: 107, 211 | 2 | yes | yes (`:107`) |
| R19 | 30111 ICS `35.030` | `35.030` | S090: 100, 204 | 2 | yes | yes (`:100`) |
| R20 | review cadence `A standard is reviewed every 5 years` (manifest Q7 for S090) | `A standard is reviewed every 5 years` | S090: 109 | 1 | yes | yes (`:109`) |
| R21 | negative: counter-example edition `29147:2022` absent from both snapshots | `29147:2022` | (absent from S089 and S090) | 0 | yes (absence confirmed) | n/a |
| R22 | site copyright chrome `© ISO 2026` | `© ISO 2026` | S089: 50 | 1 | yes | yes (`:50`) |
| R23 | site copyright chrome `© ISO 2026` | `© ISO 2026` | S090: 50 | 1 | yes | yes (`:50`) |
| R24 | CHF price 179 (store state) | `179` | S089: 78 | 1 | yes | yes (`:78`) |
| R25 | CHF price 135 (store state) | `135` | S090: 78 | 1 | yes | yes (`:78`) |
| R26 | life-cycle table present (earlier stage dates are history) | `Life cycle` | S089: 109 | 1 | yes | yes (`:109`) |
| R27 | life-cycle table present (earlier stage dates are history) | `Life cycle` | S090: 102 | 1 | yes | yes (`:102`) |

### Claim 2 — Published + current + stage "to be revised" + named successors (entry lines 31-43)

| row | asserted fact | quote copied exactly from the snapshot | snapshot line no. (grep -n) | occ | match | anchor carries quote |
|---|---|---|---|---|---|---|
| R28 | 29147 publisher status label `Status` | `Status` | S089: 94 | 1 | yes | yes (`:94`) |
| R29 | 29147 publisher status value `: Published` | `: Published` | S089: 95 | 1 | yes | yes (`:95`) |
| R30 | 30111 publisher status label `Status` | `Status` | S090: 87 | 1 | yes | yes (`:87`) |
| R31 | 30111 publisher status value `: Published` | `: Published` | S090: 88 | 1 | yes | yes (`:88`) |
| R32 | 29147 stage `International Standard to be revised [90.92]` (manifest Q5) | `International Standard to be revised [90.92]` | S089: 99 | 1 | yes | yes (`:99` = `: International Standard to be revised [90.92]`) |
| R33 | 30111 stage `International Standard to be revised [90.92]` (manifest Q4) | `International Standard to be revised [90.92]` | S090: 92 | 1 | yes | yes (`:92` = `: International Standard to be revised [90.92]`) |
| R34 | 29147 currency `This publication was last reviewed and confirmed in 2024.` (manifest Q6) | `This publication was last reviewed and confirmed in 2024.` | S089: 64 | 1 | yes | yes (`:64`) |
| R35 | 30111 currency `This publication was last reviewed and confirmed in 2025.` (manifest Q5; entry renders the tail `... in 2025.`) | `This publication was last reviewed and confirmed in 2025.` | S090: 64 | 1 | yes | yes on the full sentence (`:64`); the entry's abbreviated form `... in 2025.` is a tail of it, not the whole line |
| R36 | 29147 `Therefore this version remains current.` | `Therefore this version remains current.` | S089: 65 | 1 | yes | n/a (derived from the currency block, not separately cited) |
| R37 | 30111 `Therefore this version remains current.` | `Therefore this version remains current.` | S090: 65 | 1 | yes | n/a (derived from the currency block, not separately cited) |
| R38 | 29147 successor block label `Will be replaced by` | `Will be replaced by` | S089: 202 | 1 | yes | yes (`:202`) |
| R39 | 29147 successor block label `Under development` | `Under development` | S089: 203 | 1 | yes | yes (`:203`) |
| R40 | 29147 successor named `ISO/IEC AWI 29147` (manifest Q7) | `ISO/IEC AWI 29147` | S089: 204 | 1 | yes | yes (`:204`) |
| R41 | 30111 successor block label `Will be replaced by` | `Will be replaced by` | S090: 195 | 1 | yes | yes (`:195`) |
| R42 | 30111 successor block label `Under development` | `Under development` | S090: 196 | 1 | yes | yes (`:196`) |
| R43 | 30111 successor named `ISO/IEC WD 30111.2` (manifest Q6) | `ISO/IEC WD 30111.2` | S090: 197 | 1 | yes | yes (`:197`) |
| R44 | stage-code gloss `90.92 (To be revised)` | `90.92 (To be revised)` | S089: 117 | 1 | yes | yes (`:117` = `Stage: 90.92 (To be revised)`) |
| R45 | stage-code gloss `90.92 (To be revised)` | `90.92 (To be revised)` | S090: 110 | 1 | yes | yes (`:110` = `Stage: 90.92 (To be revised)`) |

### Claim 3 — the publisher's division-of-labour sentence (entry lines 45-58)

| row | asserted fact | quote copied exactly from the snapshot | snapshot line no. (grep -n) | occ | match | anchor carries quote |
|---|---|---|---|---|---|---|
| R46 | 29147 abstract scope fragment as quoted in the entry | `requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services` | S089: 84 | 1 | yes | yes (`:84`) |
| R47 | division-of-labour sentence (manifest Q3) | `Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111.` | S089: 91 | 1 | yes | yes (`:91`) |
| R48 | 30111 abstract scope fragment as quoted in the entry | `requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service` | S090: 84 | 1 | yes | yes (`:84`) |

### Claim 4 — vendor-side applicability; "choose" is 29147's own verb (entry lines 60-70)

| row | asserted fact | quote copied exactly from the snapshot | snapshot line no. (grep -n) | occ | match | anchor carries quote |
|---|---|---|---|---|---|---|
| R49 | 29147 applicability (manifest Q4) | `This document is applicable to vendors who choose to practice vulnerability disclosure to reduce risk to users of vendors' products and services.` | S089: 92 | 1 | yes | yes (`:92`) |
| R50 | 30111 applicability (manifest Q3) | `This document is applicable to vendors involved in handling vulnerabilities.` | S090: 85 | 1 | yes | yes (`:85`) |
| R51 | 29147 applicability carries the verb `choose` | `choose` | S089: 92 | 1 | yes | yes (`:92`) |
| R52 | negative: rejected over-generalization `vendors must follow ISO/IEC 29147` absent | `vendors must follow ISO/IEC 29147` | (absent from S089 and S090) | 0 | yes (absence confirmed) | n/a |
| R53 | `vendors who choose to practice` (the record's own wording) | `vendors who choose to practice` | S089: 92 | 1 | yes | yes (`:92`) |

### Counts

- Rows: **53** total.
- `match = yes`: **53**. `match = no`: **0**.
- Negative rows (assertion is an ABSENCE, so "yes" means the absence was confirmed): 2 (R21, R52) — `grep -c -F` returned 0 for both in both snapshots.
- Rows whose entry anchor line carries the quoted words: **51 of 53**. The 2 exceptions are R01/R02 (S089) and R09/R10 (S090) grouped into finding F1 below; plus R35, whose quoted form in the entry is an explicit tail-abbreviation of the anchored full sentence (`... in 2025.`), which resolves to S090.txt:64 in full (finding F2, informational, not a mismatch).

**Therefore: zero rows are proposed for replacement.** The "propose the exact replacement text" step of the seat spec produces no text, because no asserted fact failed against the snapshot. The two findings in §3 are anchor-precision/quoting-style notes about how the entry cites its own true facts, not fact failures; no edit is proposed for either and no file was edited.

### Supporting commands (every number above traces to one of these)

Command A — occurrence + line lists for every quote used above:
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-57 && \
for q in "ISO/IEC 29147:2018" "Information technology — Security techniques — Vulnerability disclosure" \
         "Edition 2" "2018-10" "72311" ": 32" "Number of pages" \
         "ISO/IEC 30111:2019" "Information technology — Security techniques — Vulnerability handling processes" \
         "2019-10" "69725" ": 13" "ISO/IEC JTC 1/SC 27" "35.030" \
         "A standard is reviewed every 5 years" "© ISO 2026" "179" "135" "Life cycle" \
         "Status" ": Published" "International Standard to be revised [90.92]" \
         "This publication was last reviewed and confirmed in 2024." \
         "This publication was last reviewed and confirmed in 2025." "in 2025." \
         "Therefore this version remains current." "Will be replaced by" "Under development" \
         "ISO/IEC AWI 29147" "ISO/IEC WD 30111.2" "Stage: 90.92 (To be revised)" \
         "This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services." \
         "Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111." \
         "This document provides requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service." \
         "This document is applicable to vendors who choose to practice vulnerability disclosure to reduce risk to users of vendors' products and services." \
         "This document is applicable to vendors involved in handling vulnerabilities." "choose" \
         "vendors who choose to practice" "29147:2022" "vendors must follow ISO/IEC 29147" ; do
  printf '=== %s\n' "$q"; grep -n -F -- "$q" S089.txt || echo "NO-MATCH"; done
```
Exit code 0 (the `29147:2022` / `vendors must follow …` arms print `NO-MATCH` in both files; the identical loop over S090.txt was run and gave the same shape). Decisive output lines are quoted in the table above; e.g. `grep -n -F "A standard is reviewed every 5 years"` printed `S089.txt:116` and `S090.txt:109`; `grep -n -F "ISO/IEC AWI 29147"` printed `S089.txt:204`; `grep -n -F "ISO/IEC WD 30111.2"` printed `S090.txt:197`.

Command B — the 14 manifest assertions, occurrence count and anchor, cross-checked against the entry's inline `Qn` labels:
```
python3 -c "import json; d=json.load(open('.../manifest.json')); [print(s['id'], q['id'], q['anchor'], q['quote']) for s in d['sources'] for q in s['quotes']]"
```
Exit code 0. Output (14 lines):
```
S089 Q1 1 ISO/IEC 29147:2018 - Information technology — Security techniques — Vulnerability disclosure
S089 Q2 84 This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services.
S089 Q3 91 Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111.
S089 Q4 92 This document is applicable to vendors who choose to practice vulnerability disclosure to reduce risk to users of vendors' products and services.
S089 Q5 99 International Standard to be revised [90.92]
S089 Q6 64 This publication was last reviewed and confirmed in 2024.
S089 Q7 204 ISO/IEC AWI 29147
S090 Q1 1 ISO/IEC 30111:2019 - Information technology — Security techniques — Vulnerability handling processes
S090 Q2 84 This document provides requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service.
S090 Q3 85 This document is applicable to vendors involved in handling vulnerabilities.
S090 Q4 92 International Standard to be revised [90.92]
S090 Q5 64 This publication was last reviewed and confirmed in 2025.
S090 Q6 197 ISO/IEC WD 30111.2
S090 Q7 109 A standard is reviewed every 5 years
```
Then, per quote, `grep -c -F -- "<quote>" <src>.txt` printed `occurrences=1` for all 14 (e.g. `S089 Q1 occurrences=1 anchor=1`, `S090 Q7 occurrences=1 anchor=109`), and a Python check that the quoted string is a substring of the anchor line printed `anchor_contains_quote=True` for all 14. Exit code 0.

Command C — the entry's inline `Sxxx.txt:NN Qn` citations vs the manifest anchor for the same Q-id:
```
python3 - <<'PY'   # regex over the entry body for (S0\d\d)\.txt:(\d+)\s+Q(\d); prints
                   # manifest anchor for the same Q-id and whether the line numbers agree
PY
```
Exit code 0. Output (all 14 citations, all line-agreed):
```
S089.txt:84 2 -> manifest anchor=84 LINE-AGREES
S089.txt:91 3 -> manifest anchor=91 LINE-AGREES
S090.txt:84 2 -> manifest anchor=84 LINE-AGREES
S090.txt:109 7 -> manifest anchor=109 LINE-AGREES
S089.txt:99 5 -> manifest anchor=99 LINE-AGREES
S090.txt:92 4 -> manifest anchor=92 LINE-AGREES
S089.txt:64 6 -> manifest anchor=64 LINE-AGREES
S090.txt:64 5 -> manifest anchor=64 LINE-AGREES
S089.txt:204 7 -> manifest anchor=204 LINE-AGREES
S090.txt:197 6 -> manifest anchor=197 LINE-AGREES
S089.txt:84 2 -> manifest anchor=84 LINE-AGREES
S089.txt:91 3 -> manifest anchor=91 LINE-AGREES
S090.txt:84 2 -> manifest anchor=84 LINE-AGREES
S089.txt:92 4 -> manifest anchor=92 LINE-AGREES
S090.txt:85 3 -> manifest anchor=85 LINE-AGREES
```
Every `Qn` label the entry prints points at the manifest assertion with the same quote text AND the same anchor line. No mislabelled or mis-anchored manifest reference.

## 2. Word-count measurement of every quote in the table (task item 4)

Method required by the seat spec: write the quote to a file, run `wc -w` on that file. Command (run over a TSV of id + quote, one file per quote, in scratch):
```
cd /fast/scratch/hyaku/kasegi-r57/EntryClaimTable/final && \
while IFS=$'\t' read -r id q; do printf '%s' "$q" > "f_$id.txt"; n=$(wc -w < "f_$id.txt"); \
  printf '%s|%s|%s\n' "$id" "$n" "$q"; done < q.tsv
```
Exit code 0. Output (every table quote, one `wc -w` per quote file):

| row id | wc -w | quote |
|---|---|---|
| C1.a | 2 | `ISO/IEC 29147:2018` |
| C1.b | 8 | `Information technology — Security techniques — Vulnerability disclosure` |
| C1.c | 2 | `Edition 2` |
| C1.d | 1 | `2018-10` |
| C1.e | 1 | `72311` |
| C1.f | 1 | `32` (the `: 32` value line) |
| C1.g | 2 | `ISO/IEC 30111:2019` |
| C1.h | 9 | `Information technology — Security techniques — Vulnerability handling processes` |
| C1.i | 2 | `Edition 2` |
| C1.j | 1 | `2019-10` |
| C1.k | 1 | `69725` |
| C1.l | 1 | `13` (the `: 13` value line) |
| C1.m | 4 | `ISO/IEC JTC 1/SC 27` |
| C1.n | 1 | `35.030` |
| C1.o | 7 | `A standard is reviewed every 5 years` |
| C1.p | 3 | `© ISO 2026` |
| C1.q | 1 | `179` |
| C1.r | 1 | `135` |
| C2.a | 1 | `Published` |
| C2.b | 6 | `International Standard to be revised [90.92]` |
| C2.c | 9 | `This publication was last reviewed and confirmed in 2024.` |
| C2.d | 9 | `This publication was last reviewed and confirmed in 2025.` |
| C2.e | 3 | `ISO/IEC AWI 29147` |
| C2.f | 3 | `ISO/IEC WD 30111.2` |
| C2.g | 4 | `90.92 (To be revised)` |
| C3.a | 17 | `This document provides requirements and recommendations to vendors on the disclosure of vulnerabilities in products and services.` |
| C3.b | 17 | `Other related activities that take place between receiving and disclosing vulnerability reports are described in ISO/IEC 30111.` |
| C3.c | 20 | `This document provides requirements and recommendations for how to process and remediate reported potential vulnerabilities in a product or service.` |
| C4.a | 22 | `This document is applicable to vendors who choose to practice vulnerability disclosure to reduce risk to users of vendors' products and services.` |
| C4.b | 10 | `This document is applicable to vendors involved in handling vulnerabilities.` |

**Quotes over 25 words: NONE (expected none — confirmed).** The maximum is C4.a at 22 words. The over-25 check command was the same loop with `if [ "$n" -gt 25 ]` and printed no lines.

Same measurement run over the 14 manifest quotes (one file per manifest quote), command:
```
cd /fast/scratch/hyaku/kasegi-r57/EntryClaimTable/mq && for f in *.txt; do printf '%s|' "$f"; wc -w < "$f"; done
```
Exit code 0. Output:
```
S089_Q1.txt|11   S089_Q2.txt|17   S089_Q3.txt|17   S089_Q4.txt|22   S089_Q5.txt|6   S089_Q6.txt|9   S089_Q7.txt|3
S090_Q1.txt|12   S090_Q2.txt|20   S090_Q3.txt|10   S090_Q4.txt|6   S090_Q5.txt|9   S090_Q6.txt|3   S090_Q7.txt|7
```
Over-25 check on the same 14 files printed no lines: **no manifest quote exceeds 25 words either** (max 22, S089 Q4).

Two boundary observations for the record (both are quote-selection facts, not failures):
- The full S089.txt:84 abstract line is 76 words (`sed -n '84p' S089.txt | wc -w` -> `76`); the entry deliberately quotes only its first sentence (17 words) as manifest Q2 and only the 14-word scope fragment in Claim 3. The unquoted remainder of that line (from `enables users to perform technical vulnerability management as specified in ISO/IEC 27002:2013, 12.6.1[1]` onward) is not relied on by any claim.
- S089.txt:91 (17 words) and S089.txt:92 (22 words) are the two longest quoted lines; S090.txt:84 (20 words) is the longest on the 30111 side. None is over 25.

## 3. Findings — anchor precision and quoting style (text only; the entry was NOT edited)

F1 (anchor precision, informational — the facts are true and correctly cited by their own Q-ids): the entry's inline citation `S089.txt:54` / `S090.txt:54` (entry lines 19-21) is attached to the sentence fragment that asserts identity + title + edition, but the cited line carries only `Edition 2`; the identity strings and titles live at S089:49/52/58/60/66/67/115/212 and S089:53/61 (and S090:49/52/58/60/66/67/108/205 and S090:53/61). The entry's own `source:` header (entry lines 3-4) already records the correct anchors for these facts — `title L1` for both sources, and manifest Q1 anchors at line 1 for both — so the reference resolves; the residue is that a reader following only the inline `S089.txt:54` pointer sees `Edition 2` and must consult the header or the manifest for the title's line. Note the title is also present at :1 (the document's own title line, which is exactly what manifest Q1 pins), at :53 and at :61. No fact is wrong; the pointer is coarser than the sentence it sits in.

F2 (quoting style, informational — the anchor is correct): the entry renders the S090 currency statement as `"... in 2025."` (entry line 36) while anchoring it `S090.txt:64 Q5`. The anchored line reads in full `This publication was last reviewed and confirmed in 2025.`; the entry's quoted form is an explicit leading-ellipsis abbreviation of that same line (the full sentence is what manifest Q5 pins, occurrences=1). The `... in 2025.` tail is present on S090.txt:64 (`grep -n -F "in 2025." S090.txt` -> `64`), so the citation resolves exactly; the parallel S089 citation at entry line 35 quotes the 2024 sentence in full, so the two citations are stylistically asymmetric but both resolve. No replacement proposed.

F3 (composite label, informational — the two component labels are each exact): the entry renders the life-cycle block label as `"Will be replaced by / Under development"` (entry line 36). The snapshot prints these as two separate lines, `Will be replaced by` (S089:202 / S090:195) and `Under development` (S089:203 / S090:196); the `/` is the entry's own joining punctuation, not snapshot text. Each component is verbatim at the lines shown and the successor names they introduce are pinned as manifest Q7 (:204) and Q6 (:197). Likewise the entry's `"Status : Published"` (entry line 33) is the entry's one-line rendering of the two adjacent snapshot lines `Status` (S089:94 / S090:87) and `: Published` (S089:95 / S090:88). Both components are exact and each is at the line shown; the composite is a presentation join, not a snapshot quotation. For the record, `grep -F "Will be replaced by / Under development"` returns NO-MATCH in both files while `grep -F "Will be replaced by"` and `grep -F "Under development"` each return exactly one line per file.

F4 (rejected over-generalization, confirmed sound): the entry's two negative assertions — that no `29147:2022` edition is on the page and that no `vendors must follow ISO/IEC 29147` mandate appears — are confirmed absences (`grep -c -F` -> 0 in both snapshots for both strings). The `choose` verb claim (R51) and the `vendors who choose to practice` wording (R53) are both confirmed at S089.txt:92, so the entry's "choosing is 29147's own verb" reading is the publisher's wording, not the lane's paraphrase.

F5 (stage-code ladder gloss, confirmed sound): the entry's rejected over-generalization "the rest of the numeric ladder is shown only as life-cycle labels" holds. Command:
```
awk 'NR>=109 && NR<=204 && /\(/ {print NR": "$0}' S089.txt
awk 'NR>=102 && NR<=197 && /\(/ {print NR": "$0}' S090.txt
```
Exit code 0. Output:
```
S089: 117: Stage: 90.92 (To be revised)
S089: 131: Committee draft (CD) registered
S090: 110: Stage: 90.92 (To be revised)
S090: 124: Committee draft (CD) registered
```
Only one parenthetical gloss of a stage code exists per file (the `90.92 (To be revised)` the entry quotes); the other hit is the `(CD)` abbreviation on the CD-registration event label, not a stage-code gloss. The remaining ladder codes (`00`, `10`, `20`, `30`, `40`, `50`, `60`, `90`, `95`, `90.92`, `90.93`, `90.99`, `95.99`) are bare numeric codes with plain labels, and the `90.93`/`90.99`/`95`/`95.99` rows carry no date (S089:194,196,198,200; S090:187,189,191,193) while the `90.92` row does (`2025-09-26`, S089:192 / S090:185), so the entry's "earlier stage dates are history, not the current state" and "the successor drafts are named, not opened" cautions are exactly on the snapshot's own structure.

## 4. Out of scope for this seat (not checked here, not claimed)

- The C1 limb (figure-audit ledger 27 -> 35, host-portable derive repair). Not this seat's item; the ledger and the round-56 receipts were not opened. This seat's evidence speaks only to C2's F38 entry prose versus its two committed captures.
- The other C2 kill-rule clauses (frontier census counters, capture-binding counts, the ISO lead line's exact-line sha, knowledge-expected sorting) — those are other seats' counting commands. This seat independently confirmed the two snapshot digests, byte counts, line counts, and the 14 manifest assertions' anchors and occurrence counts, which are the capture-side subset of C2.
- The `recheck:` command line in the entry (source-recheck.py) was NOT executed: the seat spec says to run only the commands this item names, and this item names grep -n / wc -w / snapshot reads. The manifest-quote anchor and occurrence facts it would print (sha256 OK + 7 Q-OK per source) were re-derived here independently via grep -c -F and the anchor-substring check (Command B), which is what this table's `occ` and `anchor carries quote` columns rest on.
- No credential material was written to this file or to any file this seat produced. The only URLs reproduced are the two public iso.org catalog URLs already committed in the manifest.

## 5. Files touched by this seat

- Written: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/w1/EntryClaimTable.md` (this file) — the only path under the lane that this seat created.
- Scratch (created and removed): `/fast/scratch/hyaku/kasegi-r57/EntryClaimTable/` with subdirs `quotes/`, `table/`, `final/`, `entryq/`, `mq/`, plus `rows.json`.
- No file under `corpus/` was created, edited, deleted or renamed. No `git add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push` or `jj` command was run against the lane; only read-only git (`rev-parse`, `status`, `diff`, `ls-files`, `show`) was used.

## 6. Verdict

`ok / admitted`. Every load-bearing fact asserted by the F38 entry's Claims 1 to 4 that is checkable against the committed round-57 snapshots reproduces exactly: 53 rows, 53 matches, 0 mismatches, 0 proposed replacements. All 14 manifest assertions (Q1-Q7 per source) are occurrences=1 at their anchors, every `Qn` label in the entry maps to the manifest assertion with the same quote and the same anchor line, and no quoted string exceeds 25 words. Two anchor-precision notes (F1, F2) and one composite-label note (F3) are reported as text only; they do not falsify any claim and no edit is proposed or made.

## 7. Leftovers

None. `/fast/scratch/hyaku/kasegi-r57/EntryClaimTable` was deleted before this yield (`rm -rf -- /fast/scratch/hyaku/kasegi-r57/EntryClaimTable`); the temporary `/tmp/mq.txt`, `/tmp/qlist.txt` and `/tmp/spans.txt` helper files were removed. No file outside this seat's scratch and its own evidence path was created.
