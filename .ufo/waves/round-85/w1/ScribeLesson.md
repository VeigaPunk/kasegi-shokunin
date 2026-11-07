# ScribeLesson — round-85 draft lesson, LOG entry and SOURCES bullets

Seat: ScribeLesson (scribe, leaf; godspeed). Scratch `S=/fast/scratch/hyaku/kasegi-r85/ScribeLesson`
(mkdir'd, not otherwise used; no files left). No tool installs, no network fetch (the S119–S121
captures are already committed), no lane-tree writes outside `.ufo/waves/round-85/w1/`, no git/jj
writes, no resolve.py census run.

## Behavior

Drafted, **not landed**, the round-85 text the L1 integrates:

1. `corpus/lessons/round-85.md` body — title, prefatory freeze/base line, `## Claims` (C1, C2
   restated from `.ufo/waves/round-85/claims.json`), `## Gate` with S119/S120/S121 blocks (URL,
   access date 2026-11-07, capture path + sha256 + bytes/lines + fetched_utc from
   `corpus/source-snapshots/round-85/manifest.json`, one located quote with snapshot line, row change
   `queued` → `mined`, used-by `corpus/practice/curl-h1-1913733`), a reused-input block for S052,
   Reject/deferred slots, considerthese (2026-10-26 proposal 2 adopted as C2) and assimilation slots,
   `## Mistakes` with M85-1 and M85-2, an r84 routed-defect disposition table (defects 1–6), routed
   slots, and the landing-values placeholder.
2. A `## Round 85` LOG.md entry draft (10 bullets, evidence pointer in each).
3. Three `corpus/SOURCES.md` `## Registry changes` bullets (S119, S120, S121; cell changes only,
   registry 121 → 121).

Every value that must be measured on the landing commit, or decided by the L1, is left as `<L1>`.

## Gates / checks actually run (read-only)

| Check | Result |
|---|---|
| 18 map entries; each basename occurs in base SKILL.md; M2/M3 forms | 18 keys, all present; candidate meter (executor receipt) `after=167/732`, M1–M5 pass |
| `.git` token class (M85-1) | `test -d .git` → 0; `git show bc722e5:SKILL.md \| grep -c 'excluding \`.git\`'` → 1; `git archive bc722e5 \| tar -t \| grep -c '^\.git/'` → 0 |
| Base-census split | `controls/census-of-record-base-r85.txt:1` extract 157/741; `controls/c1-controls-r85.txt:2` checkout 158/741; executor reproduced 157/741 → 166/732 over an extract (`w1/ExecC1Apply.md` §4) |
| M85-2 at r84 freeze `7f76b7eb` | `c1-candidate-r84.raw` → rc 128; `.txt` → rc 0; claims.json prints `.raw` |
| M85-2 at r85 freeze `4a2d34f2` | controls are an explicit 6-path list; named 6, missing 0 |
| Quote word counts / occurrence | S119 quote 7 words, 1 occurrence; S120 `Bug bounty: 2400 USD` 4 words, `S120.txt:81`; S121 quote 15 words, `S121.txt:43` |
| Derived pricing values | severity medium, 2400 USD, false, none, not-set-by-vendor, not-listed, CVE-2023-28319 (read from `c2/e2e-check.py:67-81`); `grep -c CVE-2023-28319 S052.txt` → 0 |
| Registry / collision counts | SOURCES rows 121; ConnectorOverlap receipts: 91 collisions S031–S121, guard collisions S001 and S052 |
| S052 sha256 | `d69349e8…8826`, matches the r35 record |

Receipt: `ScribeLesson-receipts/m85-check.txt` (M85-1 .git/archive presence, M85-2 control-path
resolution at both freezes, targeted rc values, committed controls listing).

## Findings

- **M85-1 `census-root-dependence`** — the resolve.py SKILL reading depends on the root class: a
  git-archive extract has no `.git`, so SKILL.md:464's `.git` token classifies GONE and base reads
  157/741; the checkout reads 158/741. Not a claim defect (C1 P1 is scoped to the checkout in
  `claims.json`), but a census-receipt defect: a receipt must name its root class. The draft gives a
  check that fails if the two roots ever print the same number.
- **M85-2 `claim-names-a-control-path-never-committed`** — mined from the r84 spot-check D-a
  (`corpus/lessons/round-84-verifier-spotcheck.md:27`, `:97`): at `7f76b7eb` claims.json names
  `c1-candidate-r84.raw` (absent), while `c1-candidate-r84.txt` is committed. Drafted fix is a
  pre-freeze resolver requiring `git cat-file -e <freeze>:<control path>`; it passes on the r85
  freeze's six explicit control paths and fails on r84's `.raw`.
- Observation for the L1: r84's `claims.controls` is a prose sentence, so the check needs a
  `controls/[^ ;),]+` token regex for prose blocks and verbatim entries for r85's list.

## Touched surfaces

Written only under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/`:

- `ScribeLesson-draft.md` — the three drafts.
- `ScribeLesson.md` — this report.
- `ScribeLesson-receipts/m85-check.txt` — the read-only evidence.

## Out of scope / not done

- Nothing landed: `corpus/lessons/round-85.md`, LOG.md and SOURCES.md are untouched; the L1 applies
  the drafts and fills `<L1>`.
- No landing measurement (C1 P1–P4, C2 P1–P6), no verdict wording, no QUALITY rule number.
- Externally attributed values are cited, not re-executed: the frozen control outputs, the executor's
  meter runs, and the connector's collision receipts.

## `<L1>` fill list

Claims/landing: landing commit; C1 landing receipt and P1–P4; C2 landing receipt and P1–P6;
depth:verifiability and coverage measured scores. Gate: the three independent re-opens; the
reject/deferred leads; the observation-not-a-source item. Mistakes: QUALITY `R<L1>`; M85-1 route.
Disposition table: rows 1, 4, 5 pointers. LOG: heading verdicts, wave attack-seat count and dead-seat
count, landing bullets, assimilation pointer. Routed-to-86 list.
