# RevPendingResolutions — round-38 receipt

Seat: RevPendingResolutions-2 (reviewer, leaf). Milestone: round-38. Judged on `depth:verifiability`.
Item: independently verify the round-37 pending-marker resolutions for L10, L85, L90, L95, L216, L265,
L300, L320 of `corpus/lessons/round-37.md` from committed bytes, then grade each row of
`.ufo/waves/round-38/wave1/ScribePendingResolutions.block.md` agree/disagree. Receipt only.

## 0. Method, scope, timeline

- Evidence anchored to committed bytes: r37 base `b56a4168…`, judged head `2387dcf6…`, lane tip
  `83975acc…`, gate receipt `.ufo/waves/round-37/final-gates/all-gates.txt` at `83975acc`, r37 seat
  receipts under `.ufo/waves/round-37/wave1/` at `83975acc`, the r37 report
  `.ufo/reports/round-37/kasegi.md` (fleet repo, read-only), and
  `corpus/lessons/round-37-verifier-spotcheck.md`. Marker inventory at the tip:
  `git show 83975acc:corpus/lessons/round-37.md | grep -c '⟨pending'` → **7** (lines 10, 90, 95, 216,
  265, 300, 320); L85 carries no marker token — it is the "…but is **not landed**" sentence the
  spot-check §5 D-C names alongside the seven.
- Scribe block found on the **first** check (2026-10-26 15:30 local; checks 2–3 not needed):
  14 lines, 5,052 B, `sha256sum` →
  `baf6c6b25933f5c1edc7b2e2b2bf68df4574ab8050339500f183db76e31b1a0b`; 8 data rows
  (`grep -cE '^\| L[0-9]+ \|'` → 8); zero `⟨`/`⟩` characters.
- Instruments were executed only over a scratch export (`git -C <lane> archive 2387dcf6 | tar -x`),
  never against the lane worktree. All git was read-only with `-C <lane>`.
- In-flight note: while this seat worked, the round-38 landing moved the working tree
  (`corpus/lessons/round-37.md` +15 lines with `## Pending-marker resolutions (round 38)` at working
  line 337; the ledger +24 lines; PROVINCE/SCORECARD/SKILL/QUALITY/README/SOURCES also modified).
  The landed append is the scribe's block plus exactly one blank separator line
  (`diff block landed-tail` → only `0a1` blank), so this grading covers the landed section bytes too.
  Every graded fact below is commit-anchored.

## 1. Independent resolution values (committed bytes, this seat's measurements)

| line | true resolved value | evidence (commands run, output observed) |
|---|---|---|
| **L10** | The **final lane commit of round 37 is `83975acc83df4bd8d5eaf463182ae615f2b64546`** (lane tip, `WAVE-DONE results`, the round's last commit). `2387dcf6…` is the **judged head** (report: "Lane HEAD at filing: `2387dcf6…`"; WAVE-DONE addendum: "`83975acc…` — a post-measurement lane commit (claim measurements stand at `2387dcf6…`)"). The wrongly-bound "final lane head" is `aa88877b…` (D-B target): the F3 diff replaces `<r37-final-lane-hash>` with `aa88877bf921…` in SHONEN `:172`/`:176` and `<r37-final-head>` with `aa88877b…` in the SCORECARD "Measured after" line. SCORECARD `:1509` reads `Final lane commit: f3246559… (round-37 wave-evidence ancestor; …)` — the D-D defect. `git diff --numstat 2387dcf6 83975acc` → `392 0 .ufo/waves/round-37/kasegi-r37-build-results.json` only. | `git log --oneline b56a4168..83975acc` (10 commits, tip = WAVE-DONE); report § SHONEN + WAVE-DONE addendum; `git diff 9492c776 2387dcf6 -- SHONEN.md SCORECARD.md` (binding lines quoted); spotcheck `:8-9` |
| **L85** | The F20 entry **landed, but not verbatim**: the L1 applied the F1 pin alignment at landing. Landed blob at `2387dcf6`/`83975acc`: 84 lines, sha256 `aedd27d3b96eba125a61244fbd08e962ea20badc14cad052512137c15bd9410f`; `source: S054` `:3`, `verified-at: 2026-10-26` `:4`, `ground: F20` `:5`, executable `recheck:` `:6`. Draft bytes (committed receipt `ScribeEntryF20.md` `:35`, `:38` at `83975acc`) differ from landed `:3`/`:6`: draft `recheck:` comment pins `anchor=247-ok … anchor=367-ok`, landed pins `anchor=259-ok … anchor=68-ok`; draft source line says `supplier/deployer example L246` and `nav rows EPSS L90-L94, CVSS L69-L71 and L156-L159, CISA-based nav L150-L153`, landed says `example L245-L246` and `navigation rows … CVSS L69-L71/L156-L159, CISA-based L150-L153`. The r37 lesson's own addendum (F1) records exactly this alignment. | `git show 83975acc:corpus/knowledge/ssvc-….md \| sed -n '3p;6p'`; `git show 83975acc:.ufo/waves/round-37/wave1/ScribeEntryF20.md \| sed -n '35p;38p'` |
| **L90** | Entry present at the integrated head, untouched after landing. `git ls-tree 83975acc -- <entry>` → present; `… \| wc -l` → 84; add-commit `0acffc8`; `git log 0acffc82..83975acc -- <entry>` → **0 commits**. | commands as cited |
| **L95** | `all-gates.txt` carries **no C2 limb** (E1–E14 are the C1 suite). The committed transcript is the seat's **mirror** run at `ExecC2Harness.md:225-230`: `S054:sha256 OK`, Q1 `anchor=6-ok`, Q2 `anchor=7-ok`, Q3 `anchor=14-ok`, `EXIT=0` (planned-draft anchors). At the integrated head the landed manifest re-derives over committed bytes — **reproduced by this seat** on the `2387dcf6` export: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` → `S054:sha256 OK`, `Q1 OK occurrences=1 anchor=259-ok`, `Q2 … 277-ok`, `Q3 … 473-ok`, `Q4 … 68-ok`, **exit=0**. | mirror receipt read at `83975acc`; fresh export run quoted above |
| **L216** | Fully closed by bytes. `all-gates.txt` at `83975acc`: 121 lines; `:1` `all-gates v1`; `:2` `export-ref=9492c776…`; `:3` `suite-sha256=0da98e37…` — equal to `git cat-file blob 2387dcf6:corpus/instruments/r37-closure.sh \| sha256sum` (recomputed, equal); 14 `payload=… closed=1` lines (`:8-21`); exactly one `closed=14/14 exit=0` (`:22`); 14 `selftest case=` lines (first at `:31`); exactly one `selftest cases=14 failures=0` (`:114`). Byte-identical `aa88877b → 83975acc` (`git diff --name-only … -- <gates>` → empty). `ExecGateReviewPrep.md` tracked since `0acffc8`. | counts via `grep -cE` on the blob; digest recomputed |
| **L265** | The lesson-named path `corpus/considerthese-ledger.md` is in **no** r37 tree; the landing is an **8-line append** to the tracked `corpus/knowledge/considerthese-proposals-ledger.md` (`0acffc8`, `8 ++++++++`): heading `## Round-37 dispositions (appended 2026-10-26, R31 home)` at `:37` followed by blank lines — **0 rows** (awk section scan); `## Re-pin note` at `:41` landed. The byte-exact 18-row block exists only inside the seat receipt (`ScribeConsiderthese.md:56`: "9184 bytes, sha256 `7c23298319a5…43706`"), while the r37 report claims "round-37 18-row disposition table + re-pin note" — the table half is false at the tip. This is L1-found defect **D-F**; the round-38 fill (+24 lines in the working tree at read time) is its closure. | `git diff b56a4168 83975acc -- <ledger>` (full hunk quoted); `git cat-file blob 83975acc:<ledger> \| awk …` → 0 |
| **L300** | Census at the integrated head: **exit 0, `W04 S028` and `W04 S029` only** — **reproduced by this seat** on the `2387dcf6` export (`sources-census.sh validate --root <scratch-root> kasegi`): `W04 S028 duplicate url docs.hackerone.com/…`, `W04 S029 duplicate url eur-lex.europa.eu/…`, `ok`, **exit=0**. Matches spotcheck `:98`/`:142-143` (measured at A) and the report's assertion. No L1-committed census transcript exists in the lane; the resolved value rests on these re-derivations. | fresh export run quoted above |
| **L320** | No-harm measurement: `git diff --numstat b56a4168 2387dcf6 -- SKILL.md PROVINCE.md` → `74 0 PROVINCE.md`, `2 0 SKILL.md`; deletion-line count in both diffs → **0**; hunks `@@ -78,0 +79,74 @@` (base PROVINCE.md = 78 lines → EOF append) and `@@ -1111,0 +1112,2 @@` (base SKILL.md = 1111 lines → EOF append). `density.py` not re-run; no density move claimed; density 9 unchanged (spotcheck `:105-111` consistent). The 74-line PROVINCE append is itself D-A (scaffolding), corrected this round — append-only discipline still held. | commands as cited |

## 2. Grading of `ScribePendingResolutions.block.md` (8 rows)

| row | grade | basis |
|---|---|---|
| L10 | **disagree** | Primary value inverts the line's own noun: the line reads "round-37 **final lane commit**", and the true final lane commit is the tip `83975acc…`; the row resolves it to the judged head `2387dcf6…` and demotes the tip to a parenthetical. Naming a non-final commit under a final-commit label is the exact M37-3/D-D class the lane spent rounds 36–37 correcting. The row is otherwise transparent (it names the tip, and names the `aa88877b` binding as the D-B correction target), and its "392 lines" numstat claim is correct. Additionally, its evidence pointer "`2387dcf6:SCORECARD.md` § Round 37, `Final lane commit` line" is misdirected: that line (`:1509`) names `f3246559…`, not `2387dcf6` — it cannot evidence the resolved value (the artifact that binds `2387dcf6` is the report). Recommended landed text: name `83975acc…` as the final lane commit, keep `2387dcf6…` under the judged-head label, cite the report. |
| L85 | **disagree (contained)** | "Landed **verbatim**" is false: the landed `:3`/`:6` bytes differ from the committed draft (`ScribeEntryF20.md:35,38`) — recheck-comment anchors `247/367` → `259/68` (the F1 alignment) and source-line locator edits (`example L246` → `example L245-L246`; `nav rows … and L156-L159, CISA-based nav` → `navigation rows … /L156-L159, CISA-based`). The row's substantive claims (landed at `0acffc8`; 84 lines; `source: S054` `:3`; `verified-at` `:4`; executable `recheck:` `:6`) are all correct; only the "verbatim" characterization is wrong. |
| L90 | **agree** | Present at `83975acc`, 84 lines, untouched `0acffc82..83975acc` — independently reproduced (log → 0 commits). |
| L95 | **agree** | Gates file correctly reported as C1-only; mirror transcript exists at the cited lines with the cited anchors; landed-anchored instrument run re-derived by this seat (259/277/473/68, occurrences=1, exit 0). Honest about the absence of a committed integrated-head C2 transcript. |
| L216 | **agree** | Every counter, line number, digest binding and the byte-identity claim verified exactly (121 lines; `:1-3`; 14+14 lines; unique `:22` and `:114` summaries; digest equals the suite blob at the judged head; `aa88877b→tip` diff empty; prep receipt tracked since `0acffc8`). |
| L265 | **agree** | Path absence, receipt-only block (full sha matches `ScribeConsiderthese.md:56`), empty `:37` section, and the D-F routing all verified from bytes; reporting the landing as not-what-the-lesson-claimed rather than smoothing it is the correct treatment. |
| L300 | **agree** | Value reproduced by this seat on the judged-head export (exit 0, W04 S028/S029 only, no E-codes); consistent with the committed spot-check and report. |
| L320 | **agree** | SKILL/PROVINCE numstat, zero-deletion and EOF-hunk positions re-derived exactly; generalization to the other files is consistent with the committed spotcheck §2 numstat; D-A cross-reference is correct and properly kept separate from the no-harm claim. |

Net: **6 agree, 2 disagree** (L10 substantive; L85 one-word overclaim with correct substance).

## 3. Findings

1. **[medium] L10 resolved value/label mismatch + misdirected evidence pointer** (detail in §2). The
   landed section (byte-identical to the block) now records the r37 "final lane commit" as the judged
   head. Practical exposure is bounded — the row discloses the tip, the judged head, and the
   `aa88877b` D-B target — but a future reader following the landed primary value will repeat the
   three-heads drift (report `2387dcf6` / SHONEN+SCORECARD binding `aa88877b` / receipt `9492c776`)
   that §5 D-B routed. Fix is a one-line append or erratum naming `83975acc…` as the final lane commit.
2. **[low] L85 "verbatim" is contradicted by committed bytes** (detail in §2). Cosmetic but it is a
   checkable claim in a landed lesson section, and it is false; "landed with the F1 pin alignment"
   would have been exact.
3. **[info] L265's closure clause is forward-looking.** "…closed by the round-38 ledger deliverable"
   was true only as intent at block-write time; at this seat's last read the round-38 fill
   (+24 ledger lines) sat modified in the working tree, not yet committed to the tip. If the landing
   stalls, the clause overstates. No action needed if the round lands.
4. **[info] Landing discipline held.** The landed append is the delivered block plus one blank
   separator, byte-identical otherwise; the seven marker lines above it are untouched (append-only).
5. **[info] Timeline note, no defect.** The scribe receipt's "working-tree sha `8f5e49e7…` equals the
   blob at `83975acc`" was true at its read; the working tree has since moved (round-38 landing), so
   that equality no longer holds at receipt-write time.

## 4. Residual risk and verification gaps

- L320's whole-file "zero deletions" generalization was re-derived by this seat only for SKILL.md and
  PROVINCE.md (hunk positions + deletion count); the remaining files' numstat rows are cited from the
  committed spot-check §2, which this seat read and found consistent, but did not re-run file-by-file.
- L216 was verified at byte level (counters, digest binding, ancestry) per the spot-check's method;
  the r37 suite itself was not executed by this seat — a redundant execution of the L1's own gate run.
- The L10 grade rests on a labeling judgment (tip = final lane commit vs closure-time head = judged
  head). It is grounded in the line's own noun, the report's WAVE-DONE addendum wording, and the lane's
  M37-3/D-D history; both hashes are disclosed either way, so residual risk is limited to the primary
  value a future reader quotes.
- The census reproduction needed a scratch root with `shokunin.conf` copied from the fleet root
  (read-only source); the instrument is read-only by its own header and wrote only stdout.

## 5. Bounds

Writes: this receipt only. No lane, fleet, sibling-lane, or `shokuknow` file was edited; no mutating
git/jj command (all `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin` read-only subcommands);
no subagents; no `agent://all`; no tooling installs, no pacman, no network fetches (no `curl` needed —
every value came from committed bytes or a local instrument over an export). Scratch
`/fast/scratch/hyaku/kasegi-r38/RevPendingResolutions/` (judged-head export, fake census root, block
comparisons) was removed before yield.
