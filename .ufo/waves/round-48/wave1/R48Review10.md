# R48Review10 — Sibling checklist conventions + province overlap scan (connector)

- Seat: R48Review10 (connector, lane `kasegi-shokunin`, round 48 wave 1; leaf, no dispatch)
- Axis: depth:verifiability (sole axis declared in `.ufo/waves/round-48/wave1-spec.json`)
- Frozen claim scanned: C1 (`claims.json` @ `3546f70`): SHONEN.md conforms to the canonical
  four-box author-assessment grammar with existing local evidence pointers — form validation,
  not promotion or evidence truth.
- Round-47 route context: `corpus/lessons/round-47-verifier-spotcheck.md:85` (R1 — SHONEN.md
  canonical-form drift, 13 blocks / 52 `[~]` lines) names this exact repair and offers three
  routes: (a) keep per-round assessments in reports, (b) restore SHONEN.md toward the canonical
  seed, (c) record the fleet-sanctioned convention explicitly. R2 (plain-target phrasing,
  `:86`) is not this seat's target; its lesson is applied to my own census patterns, which are
  all line-anchored (`^      Evidence: ` etc.) so prose cannot meet a target.
- No production edits. No git/jj mutation (read-only `git show`/`git log`/`git rev-parse` only).
  No tool installs — python3 3.14.8 at /usr/bin/python3 sufficed; nothing installed or upgraded;
  pacman untouched.
- Read-only scan: 21 sibling `SHONEN.md` files + kasegi's own (22 files). Contents were read
  for *convention shape only*; no sibling domain evidence was copied, paraphrased into kasegi
  artifacts, or absorbed.

## 1. Ground truth at scan time (2026-10-30T15:08:54Z)

The repair has landed: HEAD `3d7e042` ("round-48: restore canonical checklist and dispatch 64
probes"), freeze commit `3546f70`, base `903d47e1` (ancestor of HEAD, verified).

| artifact | sha256 | grade by frozen checker |
|---|---|---|
| production `SHONEN.md` @ HEAD (12 lines) | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | `canonical=1 finding=SF-CLEAN exit=0` |
| `controls/canonical-candidate.txt` (12 lines) | `b476c7aa3ff740e51e3f6020d278845f2fe85c7435ab4d71d2c38d34a4de4b8c` | `canonical=1 finding=SF-CLEAN exit=0` |
| `controls/shonen-before.txt` (356 lines, 52 `[~]`) | `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` | archive — matches kill-rule SHA |
| `git show 903d47e:SHONEN.md` | `596122c0…` (identical to `shonen-before.txt`) | history retains the drifted bytes |
| frozen checker `corpus/instruments/shonen-form.py` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | unmodified |

Production differs from the frozen candidate in evidence pointers and box-2 mark
(production: per-box pointers `SKILL.md`, `LOG.md`,
`corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md`; box 2 = `[ ]` with
"No new end-to-end domain task claimed"). Both grade `SF-CLEAN`; the claim's `after` line is
the grade, so the divergence is observed, not a defeat. Box 2 staying `[ ]` corroborates the
round-47 closure note that box 2 has no executed end-to-end item — the repair does not
overclaim (semantic review of the pointers is R48Review04's seat, not this one).

## 2. Sibling convention census (mechanical, anchored patterns)

Census script (anchored regex per R2), full table and per-file sha256 receipt:

- table: §4 receipt `sibling-census` (reprinted below)
- hashes: §4 receipt `sibling-hashes` (20 sibling files; kasegi excluded, hashed in §1)
- frozen at 2026-10-30T15:08:54Z; all patterns `^`-anchored.

```
sibling|lines|box_marks|evi_6space|evi_2space_capital|evi_2space_lower|evi_arrow|evi_assertion_word|evi_bare_backtick|other_style
audio|11|4|0|3|0|0|0|0|0
chousa|12|4|0|0|0|0|0|4|0
game-dev-2d|11|4|0|0|0|0|0|3|0
game-dev-3d|9|4|0|0|0|0|0|0|1
kagi|12|4|0|4|0|0|0|0|0
kaidoku|14|4|0|0|0|0|0|0|6
kake|8|4|0|0|0|0|0|0|0
kama|12|4|0|0|0|0|0|0|4
kasegi|12|4|4|0|0|0|0|0|0
kengaku|12|4|0|0|0|0|0|0|4
kotoba|12|4|0|0|4|0|0|0|0
kotodama|15|4|0|0|0|0|4|0|3
kumitate|8|4|0|0|0|0|0|0|0
lore|12|4|0|4|0|0|0|0|0
mado|12|4|0|0|0|0|4|0|0
mori|8|4|0|0|0|0|0|0|0
revenger|30|4|0|0|0|0|0|7|15
souji|12|4|0|0|0|0|0|0|4
tabi|12|4|0|0|0|0|0|4|0
tameshi|12|4|0|0|0|0|0|0|4
tsukuroi|12|4|0|0|0|0|4|0|0
```

Load-bearing files read in full (convention shape only): kagi, chousa, kaidoku, kotodama,
revenger, game-dev-3d, kake, mori, kumitate, kama (raw text in session transcript; each row
above is one `sha256sum` + one `cat` away from re-derivation).

Findings:

1. **No fleet-uniform evidence-line grammar.** At least 10 distinct per-box evidence styles
   across the 21 siblings: 2-space `Evidence: ` (audio, kagi, lore), 2-space lowercase
   `evidence: ` (kotoba), 2-space bare backtick/prose (chousa, kengaku, souji, tabi,
   game-dev-2d), 2-space markdown-link assertion (tameshi), 6-space `→ Author assertion: `
   (kama), `Historical assertion: ` (mado), `Author-side evidence: ` (tsukuroi), `asserted: `
   (kotodama), multi-line wrapped prose (revenger, 30 lines), inline-on-box-line after ` — `
   (mori). Three macro-shapes exist on top: canonical-seed-based (most), HTML-comment preamble
   above the seed (kaidoku, 6 lines), and a non-seed probation template (game-dev-3d,
   `# SHONEN — probation`, mint-era — never carried the canonical four labels, so it is a
   different template, not canonical drift). Bare canonical `[ ]` with no evidence lines:
   kake, kumitate.
2. **Kasegi's repaired grammar is fleet-unique and the strictest.** kasegi is the only file
   with 6-space `Evidence: ` (column `evi_6space`=4 for kasegi, 0 for all 21 siblings). No
   sibling file, taken as-is, would pass kasegi's frozen checker — its H1 hardcodes the kasegi
   name, and every sibling evidence style is non-6-space.
3. **Kasegi's pre-repair drift shape was unique in the fleet.** No sibling carries 13
   accumulated per-round assessment blocks: the drifted siblings differ in kind (revenger:
   multi-line wrapped prose; kotodama: appended `Marks:` legend; kaidoku: prepended HTML
   comment). Restoring canonical form therefore loses no fleet convention.

## 3. Province overlap verdict (both directions)

- **Reverse (does any sibling own checklist form?):** `grep -l "SHONEN|promotion checklist|
  shonen form" */PROVINCE.md` over the fleet root returns exactly one hit,
  `audio-shokunin/PROVINCE.md:31`, which concerns audio's own box-4 evidence boundary, not
  ownership of the form. The canonical seed is main-repo protocol-owned
  (`controls/protocol-source.txt`, "File contract per shokunin repo" + "The canonical
  `SHONEN.md` seed (verbatim)"). No sibling province claims SHONEN grammar; no contested scope.
- **Forward (does the repair emit anything siblings own?):** the repaired file's four evidence
  pointers (`SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`,
  `PROVINCE.md`) are all kasegi-local paths — no `../`, no sibling paths; the checker itself
  rejects absolute/`..` pointers (`SF-POINTER`, probed at R48Review17/18/19 seats). Sibling
  file *contents* (kagi's vault gate, tabi's journey loops, etc.) were read only as shape
  evidence and enter no kasegi artifact.
- **Verdict: no overlap; nothing absorbed; nothing routed.** The scan changes no sibling file
  and no kasegi production file.

## 4. Bounded probes — exact commands, expected vs observed

Frozen counter: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py`
(read-only; `--root /home/vgpnk/Projects/shokunin/kasegi-shokunin` for all runs).

| # | Case | Expected | Observed | Match |
|---|---|---|---|---|
| 1 | Live tree, HEAD `3d7e042` (repair landed) — `python3 …/shonen-form.py --root …/kasegi-shokunin` | `canonical=1 finding=SF-CLEAN exit=0` (claims.json `after`) | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, process exit 0 | yes |
| 2 | Do-nothing base — `git show 903d47e13058982460f0d90c1c2b9c7c02680646:SHONEN.md > …/R48Review10/SHONEN.base-903d47e.md`, then `--file` that path | `canonical=0 finding=SF-PREAMBLE exit=1` (`expect_before`, `controls/do-nothing.txt`) | `shonen-form canonical=0 finding=SF-PREAMBLE exit=1`, exit 1 | yes |
| 3 | Sibling-port mutant P3: production file with evidence lines re-indented 2-space `Evidence: ` (kagi/lore/audio style) | nonclean, stable SF finding | `canonical=0 finding=SF-EVIDENCE exit=1`, exit 1; re-run identical | yes |
| 4 | Sibling-port mutant P4: kaidoku-style HTML-comment preamble prepended | nonclean | `canonical=0 finding=SF-PREAMBLE exit=1` | yes |
| 5 | Sibling-port mutant P5: kotodama-style trailing `Marks:` legend appended | nonclean | `canonical=0 finding=SF-TRAILING exit=1` | yes |
| 6 | Sibling-port mutant P6: chousa-style bare 2-space backtick prose, `Evidence:` word removed | nonclean | `canonical=0 finding=SF-EVIDENCE exit=1` | yes |

Grammar readings (why the rejections are designed behavior, not fabricated defects): the frozen
checker accepts an optional evidence line **only** at exactly 6 spaces + `Evidence: ` with a
plain repo-relative file pointer; a `[~]` box whose next line is anything else falls into the
`elif mark != ' '` limb → `SF-EVIDENCE` (P3, P6); a preamble above the H1 breaks the expected
head lines → `SF-PREAMBLE` (P4); any bytes after box 4 → `SF-TRAILING` (P5). P3/P6 prove the
checker's grammar is **not portable to any sibling convention** — the mechanical half of the
route-(c) defeat.

Reproduction for P3 (fixture construction; all mutants lived only under
`/fast/scratch/hyaku/kasegi-r48/R48Review10/`):

```
$ python3 - <<'PY'
from pathlib import Path
prod = Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md').read_text()
Path('/fast/scratch/hyaku/kasegi-r48/R48Review10/SHONEN.sib-2space-evidence.md').write_text(
    prod.replace('      Evidence: ', '  Evidence: '))
PY
$ python3 …/shonen-form.py --root …/kasegi-shokunin --file …/R48Review10/SHONEN.sib-2space-evidence.md
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
```

## 5. The connector move (one, bounded)

**Affected axes:** depth:verifiability — improved; no other axis touched (coverage frontier
unchanged at 29 rows, no score claims, no promotion inference).

**Proposed move (for KasegiR48's integration record; proposed here, not written by this seat):**
land one durable sentence in the round-48 integration note recording, with this report as the
citable receipt:

> R1 closed via route (b) (restore toward canonical seed). Route (c) — "record the
> fleet-sanctioned convention explicitly" — has no unique target: a mechanical census of all
> 21 sibling SHONEN.md files (`wave1/R48Review10.md` §2) finds ≥10 distinct evidence-line
> styles and no fleet-uniform grammar; the frozen 6-space `Evidence: ` grammar is a kasegi-local
> pin, stricter than every sibling's and portable to none (probes P3–P6). No sibling province
> owns checklist form (protocol-owned template); zero sibling knowledge was absorbed in the
> repair (§3).

**Why it improves the axis without harming another:** two limbs of C1's boundary currently rest
on assertion — the kill rule's "tested hidden/commented/duplicate checklist" context and the
predicate's "author-side form only" scope. The census + P3–P6 make the "not a fleet convention,
not sibling knowledge, not portable" claims re-derivable by a non-author with one grep set and
one checker run each, and they pre-empt the R48Review03-class attack (overclaiming the repair
as fleet-level or promotion-relevant) with fleet-wide evidence rather than argument. It is a
record-only move: no file content changes, no score movement, so coverage and all other axes
are untouched.

**Synthesis note:** the move is compatible with R48Review16's migration rationale (historical
assessment blocks preserved in archive/reports) — §2 finding 3 supplies its fleet-side
justification (no sibling keeps per-round assessment blocks in SHONEN.md, so the migration
loses no convention) — and with R48Review01/05's seed-normalization reviews (both production
and candidate grade `SF-CLEAN`; the divergence between them is recorded in §1 for whoever
grades byte-equivalence).

**Risks and limits:**

1. Census classifier is regex-based over 22 small files; a mis-counted line would not change
   the conclusion, which rests on the *existence of multiple distinct styles* (directly
   observable in the §2 raw dumps), not on exact per-style tallies.
2. `game-dev-3d` is classified as a mint-era probation template, not canonical drift; counting
   it as drift would strengthen, not weaken, finding 1.
3. The census is frozen at 2026-10-30T15:08:54Z (hashes in §4 receipt); later sibling edits are
   new facts about a new date, not defects of this receipt.
4. No semantic truth is claimed anywhere here: sibling `[x]`/verifier names were read as shape
   only and are not endorsed; kasegi box marks remain author-side form.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review10/` held only the §4 fixtures/receipts
  (base snapshot, 4 sibling-port mutants, census table, hash list) and was removed after this
  report was saved. No `/tmp` clones; no background jobs; no installs (record: none — python3
  3.14.8 and coreutils sufficed; pacman untouched).
- Production tree, fleet root files, siblings, domain trees, git/jj index and state: read-only
  access only; nothing created, modified, or deleted outside this report and the named scratch.
