# ConnectorOverlap — kasegi round 83, attempt 1

Scope: read-only cross-lane, assimilation-interface and cross-claim scan over the frozen round
bytes. Base `834bf78eaca70a69294f2ecfefa89b73c3fa85b8`, freeze `0cd499dbdfc0bf9ce3095681af9bc76588d76f31`
(= lane HEAD at scan time). The only commands run are the four phrase greps, the two id greps plus
`comm -12`, the quarantine `awk`, a read-only URL-level comparison of the two registries, and reads
(`sed`, `grep`, `python3 -c`, `git show`).
No counter, gate or lane suite was executed; no lane file was edited. Receipts:
`.ufo/waves/round-83/w1/ConnectorOverlap-receipts/` (`sibling-grep.txt`,
`assimilation/{reg-ids,staged-ids,collisions,quarantine-slice,doc-collisions.txt,assimilation-commands.txt}`).
No tool installs or updates.

## 1. Sibling overlap — does F59 duplicate held ground?

Phrase census over `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/` + each lane's `SOURCES.md`
(20 sibling lanes; kasegi excluded), exact literal match:

| phrase | sibling hits |
|---|---|
| `osv.dev/faq` | **0** in every sibling lane |
| `modified_id.csv` | **0** |
| `withdrawn field` | **0** |
| `orphaned` | **14 lines in 7 lanes**, all non-OSV (see below) |

`orphaned` hits in `corpus/knowledge/` + `SOURCES.md`, per lane (representative path:line):

- kaidoku ×3 — `corpus/knowledge/2026-10-13-pacman-packages.md:50` (orphaned pacman packages), `2026-10-13-r2-doctor-reverify-r2.md:56` (orphaned session dirs), `2026-10-13-r4-14-libsignal.md:79` (killed wrapper run)
- kake ×1 — `corpus/knowledge/fire-journal-codes.md:60` (a session that died)
- kotodama ×1 — `corpus/knowledge/culture-material/cuisine-food-lexicon.md:149` (a legend)
- mori ×3 — `corpus/knowledge/entry-claims-hardening-r60.md:1`, `watchdog-identity-r31.md:34,:47` (an orphaned child holding a flock fd)
- souji ×1 — `corpus/knowledge/git-grace-periods-and-expire-to.md:21`
- tameshi ×1 — `corpus/knowledge/guard-kill-closure.md:73` (orphaned process reparented to a subreaper)
- tsukuroi ×4 — `corpus/knowledge/foreign-provenance-r6.md:195,:287` (orphaned source db), `path-reconciliation-r23.md:18,:26`

(The wider `corpus/` scan adds fixture/transcript noise — game-dev-2d 2677, game-dev-3d 218, chousa
19 — none of it concerns OSV records. Broad `osv.dev` outside kasegi: only kaidoku
`kaidoku-shokunin/corpus/SOURCES.md:21` (S015, `https://api.osv.dev/v1/vulns/CVE-2025-55305`), its lesson
`kaidoku-shokunin/corpus/lessons/round-13.md:42`, and a registry JSON fixture `kaidoku-shokunin/corpus/evidence/round-30/c1/pypi-uv-0.13.0.json:1`.
kotodama's `OSV` is the Object–Subject–Verb word order in `linguistics/syntax-typology.md:32`, not the database.)

**Verdict: F59 duplicates no sibling's held ground.** The only sibling OSV row is kaidoku S015, one
CVE's API record (fields of CVE-2025-55305), a different document and a different proposition from
the OSV.dev FAQ's post-import lifecycle; kaidoku's Q142/Q143 (`kaidoku-shokunin/corpus/QUALITY.md:226,:228`) are
source-novelty criteria, not ground. No sibling holds any OSV.dev FAQ/record-lifecycle row, and no
sibling frontier row names it. F59's lane-internal distinctness (F51/F54/F55/F56/F57/F58) is not
widened here.

## 2. Assimilation id check (exact prompt commands, read-only on shokuknow)

`S=/home/vgpnk/Projects/shokuknow`, output under
`.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/`:

| measure | value |
|---|---|
| `reg-ids` (lane `corpus/SOURCES.md`) | **117** ids, S001..S117 |
| `staged-ids` (`merge/kasegi/SOURCES.append.md`) | **94** ids, S031..S124 |
| `comm -12` → `collisions` | **87** ids, a contiguous block **S031..S117** |
| `quarantine-slice` (data-row awk) | **7 lines** |

**Invariant (measured at three rounds): collisions = registry max − 30.** 112−30 = 82 (r77, `corpus/lessons/round-79.md:40`),
114−30 = 84 (r80, `round-80.md:16`), 116−30 = 86 (r82, `round-82.md`, ConnectorOverlap row),
117−30 = 87 (this round). Every id the lane mints above S030 converts one staged id into a
collision; this round mints S117, so the collision block now ends on the id the round lands. The
package's own basis line is stale — `merge/kasegi/MERGE-REPORT.md:9` still says "lane registry
currently holds **30** rows; first staged id is **S031**".

Document-level split (`doc-collisions.txt`): of the 87 colliding ids, **1 same URL (S042)** and
**86 different or URL-less** — the r82 reading (1 same-source pair, 85 different) holds; the r83
increment is exactly the new S117.

**The S117 twin is the non-obvious hazard.** `merge/kasegi/SOURCES.append.md:93` names staged S117
as "The canonical host's own attachment path and its file-name families — …/cert_upload_family_probe.txt"
(own-work, cert.org.cn directory probes), while lane `corpus/SOURCES.md:129` is the OSV FAQ
(`https://google.github.io/osv.dev/faq/`). The staged knowledge file that cites it is
`merge/kasegi/knowledge/corpus/knowledge/cnvd-bulletin-absence-by-directory-and-title.md:2` (again
`:21-25`). An adoption that carried citations unchanged would bind that CNVD-bulletin entry to the
OSV FAQ row **and pass the source census** (the id exists) — the exact failure mode the document-first
renumbering rule exists for. Nothing is appended while the r77 L0 question stays open
(`corpus/lessons/round-79.md:77`).

Freeze check: at `0cd499db`, `corpus/SOURCES.md` holds 117 rows and S117 is `queued` with `used-by —`;
the worktree already shows `mined` / `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` (L1
integration, see §6). The collision count is therefore identical at freeze and now — the id is taken
at freeze regardless of landing.

**Quarantine slice (7 rows, all quarantined).** 2 carry `payload-absent` (S037, S054); 5 carry the
register's unchecked-family prose "the cited source could not be fetched, so no quote was checked"
(S048, S065, S068, S069, S070) — unverifiable, not fabrication, pending a hand-fetch. Register
hygiene note: the 5 prose rows (`absent-defect-register.md:322-326`) put a trailing backtick inside
the id cell (`S048\``), so any exact-id join must normalize; the prompt's `awk` still emits them as
S-ids as required. Verdicts on these rows are the lane's to write; this seat did not fetch.

## 3. considerthese — latest file, one still-unimplemented proposal

Latest is `considerthese/2026-10-26.md` (mtime 2026-10-26 09:05). Files present, by date:
`2026-10-19.md`, `2026-10-20.md`, `2026-10-21.md`, `2026-10-22.md`, `2026-10-23.md`,
`2026-10-24.md`, `2026-10-25.md`, `2026-10-26.md`.
Dispositions: proposal 1 → `SCORECARD.md:1534` (landed r39); 3 → `corpus/instruments/r46-landing-gate.py:4-5`
("Adopts `considerthese/2026-10-26.md` proposal 3"); 5 → `PROVINCE.md:77` (F18 amendment appended r36);
7 → `corpus/knowledge/considerthese-proposals-ledger.md` (r30, with later appended flips); 6 is the
bot's own cadence (operator-owned, no lane instrument).

**Named: proposal 4, `considerthese/2026-10-26.md:32` — "Cap or externalise wave evidence."** It is
still unimplemented *as an instrument*: R14 (`corpus/QUALITY.md:83`) mints the policy from the
2026-10-25 file's same proposal, but no committed census command exists — 46 `.py` instruments and
`ls corpus/instruments | grep -iE 'size|growth|evidence'` prints only `wave-registry.py`; the file's
own measurements (96 % of files, ~95 % of bytes, 109 MB) have never been re-run. It fits a
recheck/instrument claim exactly, because R14's own sentence makes the predicate countable: per-round
repo growth from committed bytes (`git ls-tree`/`git cat-file` sums at two revisions).

Not named: proposal 2 (`:30`) is the only OSV-adjacent item, but it is a domain task, not a
recheck/instrument, and lane records contradict its status — `corpus/lessons/round-74.md:79` says the
trial was built and gated, while `round-79.md:40`, `round-80.md:16` and
`round-82-verifier-spotcheck.md:112` record SHONEN box 2 open and the proposal unimplemented.

## 4. Cross-claim pattern

**Both r83 limbs certify a look-alike at the right site, not the proposition that site is supposed to
carry.** Each closes a *positional* forgery class and leaves a *semantic* one:

- **C1** keys the environment — constant `mutbat-t-<nonce>` run dirs, nonce-keyed D1/D2, the D3
  single-anchor decoy, `extra` sites (`c1/mutbat.py:7-19`) — and scores kills by a `FAIL` line naming
  a declared case. The frozen limit is stated and receipted: an AST-embedding target that fails only
  on a known mutant image passes (`c1/mutbat.py:21-22`; `controls/c1-forgeries-r83.txt:8`, F8 rc=0
  under counter r83). The counter cannot separate "fails for the mutated semantics" from "fails
  because it recognises the mutant image".
- **C2** keys the site — the rule must cite a line holding a span in its own `## Claim` section and
  share ≥ 2 five-character stems with that span (`c2/entry-gate.py:85-98`, `TIE_WORDS = 2` at `:45`,
  `words()` at `:79-83`). Polarity cannot enter: `not`/`no` are filtered by the ≥4-letter rule, so a
  rule that reuses the quote's nouns and **negates** it ties. The converse is already in the frozen
  controls: the held S115 entry fails r83 with `untied=1` on a rule that is tied by deixis ("the
  audience the page names", `corpus/knowledge/osv-importfindings-record-quality-feedback.md:23`;
  `controls/c2-g6-controls-r83.txt:14`), recorded in `claims.json:7` as a finding against S115. G5
  states its own limit verbatim: "it does not check that the rule is true or that it follows from
  the quote" (`c2/entry-gate.py:29`).

Shared residual class: **token-at-site equivalence, symmetric under negation and paraphrase.** Both
limbs were built from the r82 routed defects 1-5 (`claims.json` history) and both moved the binding
into keys and positions; neither tests entailment.

## 5. Proposed move (one, bounded)

**Declare C2's G6 residual with a fourth control — the negate-tie forgery — and record the symmetric
limit beside C1's F8, instead of leaving G6's limit unstated.**

Specimen: take the landed F58 entry and replace Claim 1's rule
(`corpus/knowledge/osv-high-quality-record-import-bar.md:17`) with
`No record that OSV.dev will not import is described by the good enough properties this page names (S116.txt:25).`
Against the pinned quote `Describe the “good enough” OSV record that will be imported by OSV.dev`
(`corpus/source-snapshots/round-82/S116.txt:25`) the stems `descri, good, enough, recor, impor`
overlap ≥ 2; the text is ≥ 8 words, cites the line, and is not a snapshot substring — so G5 and G6
both pass it while it asserts the opposite of its quote. **[INFERENCE]** until run: gate r82 rc 0,
gate r83 rc 0 with `untied=0` (the forgery survives).

- **Affected axes:** depth:verifiability — the round's new limb gains its missing falsifier and a
  declared residual class, matching the practice that let C1's F8 limit survive review
  (`c1/mutbat.py:21-22`). Coverage unchanged (no frontier, registry or knowledge count moves). No
  harm to C1 (no frozen byte changes).
- **Why it is not a claim change:** B8 names only `filler`, `crosscite`, `copyrule`; the gate and the
  r83 controls stay frozen. The witness belongs in the round lesson's Gate block (and in the next
  round's control driver if G6 gets a successor).
- **Risks:** (a) a naive fix — a polarity filter — would reject held rules that legitimately negate
  (`osv-importfindings-record-quality-feedback.md:39` "the page does not name";
  `osv-faq-post-import-record-lifecycle.md:17` "has not ruled out", `:41` "is not proof"), so the move
  records a limit rather than tightening G6; (b) if G6 rejects the specimen (`untied=1`) the premise
  is falsified and no limit is owed — report flips; (c) the specimen must not be added to the frozen
  r83 controls (the kill rule freezes those bytes).
- **Verification (exact):**
  ```
  python3 -B .ufo/waves/round-83/c2/entry-gate.py --entry <scratch>/negate-s116.md \
    --manifest corpus/source-snapshots/round-82/manifest.json --source S116 --lane .
  python3 -B .ufo/waves/round-82/c2/entry-gate.py --entry <scratch>/negate-s116.md \
    --manifest corpus/source-snapshots/round-82/manifest.json --source S116 --lane .
  ```
  plus the frozen calibration pair `controls/c2-g6-controls-r83.txt:13-14` (S115 r82 rc0 / r83 rc1).

## 6. Routed observations (no claim verdict)

- **O1 (low, documentation of frozen bytes).** `c2/entry-gate.py:2` still reads "round-82 C2 entry
  gate (B8): shape limbs G1-G4 plus content limb G5" although G6 is implemented at `:85-98` and
  printed as `untied=` at `:122,:132-140`; a reader of the frozen gate's header alone would not know
  the round's new limb exists. Not a claim defect (B8 runs the file, not its header).
- **O2 (state, for closure).** HEAD = freeze `0cd499db`; the worktree carries 4 modified tracked files
  (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`)
  plus the untracked `corpus/knowledge/osv-faq-post-import-record-lifecycle.md`, mtimes 19:01–19:03 —
  the L1's integration in progress. R28's quiescence limb (`git status --porcelain` empty) must hold
  at closure; the frozen controls were taken pre-freeze (`controls/c2-prefreeze-r83.txt`, 21:57Z).
- **O3 (assimilation basis).** `MERGE-REPORT.md:9`'s "30 rows" basis is 87 rows out of date; the L0
  question on the staged package (`round-79.md:77`) remains the right place for the renumber ruling.

## Files written

- `.ufo/waves/round-83/w1/ConnectorOverlap.md` (this report)
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/sibling-grep.txt`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/reg-ids`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/staged-ids`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/collisions`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/quarantine-slice`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/doc-collisions.txt`
- `.ufo/waves/round-83/w1/ConnectorOverlap-receipts/assimilation/assimilation-commands.txt`
