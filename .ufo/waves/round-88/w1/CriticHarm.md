# CriticHarm — round 88 harm check, base `6beead91` → C2 landing `b43dc21` (attempt 1)

Seat: CriticHarm (attack). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scope: harm only —
no claim is re-scored; every finding below is a routed defect with a re-runnable command.

Revs (from `.ufo/waves/round-88/landing.json`): base `6beead9148945fa695cf3139e8fc9d8e91cc5fd0`,
freeze `7f2ebebf…`, C1 landing `fd33e1bf…`, C2 landing `b43dc2154bc09470da2209fb626021da3af3593e`.
Method: two `git clone --shared` clones in scratch (`base`, `land`), each checked out and `rev-parse
--show-toplevel` asserted; every probe ran there or on read-only `git show`/`git grep`. Scratch
`/fast/scratch/hyaku/kasegi-r88/CriticHarm`, deleted before yield.

## VERDICT: HARM (2 landed defects + 1 pending integration obligation)

No frozen predicate is broken by these findings: C1's counter measures `KNOWLEDGE-METER-RESULT pass
rc=0 after=742/1743` on the landing clone and every instrument/source pin in `claims.json` matches at
`b43dc215`; C2's landed bytes are byte-equal to the frozen candidates. The harm is collateral:
one knowledge line changed meaning, and one existing knowledge entry is now false in three sentences.

---

## 1. depth:density — NO HARM

`python3 corpus/instruments/density.py SKILL.md` at both revs: mean dens **273.2**, **932** path-citation
instances across **38** blocks, identical. `SKILL.md` untouched: sha256
`7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552` at base and landing.
Receipt: `CriticHarm-receipts/density.txt`.

## 2. Deletions — NONE

`git diff --name-only --diff-filter=D 6beead91 b43dc215` prints nothing (whole range, no file removed or
renamed away). Per-commit stats: freeze adds 20 files (+2823), C1 touches 8 knowledge files
(64 insertions / 64 deletions, no line-count change), C2 touches 2 files.

## 3. Gate continuity — NO HARM (one expected sha difference)

Selftests run from each clone's own bytes, `python3 -B`, `TMPDIR` in scratch, cwd in scratch:

| selftest | base | landing |
|---|---|---|
| `claim-package-selftest.py` | rc=0, `cases=10 failures=0` | rc=0, `cases=10 failures=0` |
| `capture-secret-scan.py --selftest` | rc=0, `SELFTEST-RESULT pass cases=19` | rc=0, `SELFTEST-RESULT pass cases=33` |
| `source-recheck.py --selftest` | rc=0, `cases=10 failures=0` | rc=0, `cases=10 failures=0` |
| `capture-source.py --selftest` | rc=0, `normalize=ok deterministic=ok` | rc=0, `normalize=ok deterministic=ok` |

r87 counter (`.ufo/waves/round-87/c2/capability-check.py`) at the r88 landing:

- **without pins: all limbs pass** — K1 pass (selftest_rc=0), K2 pass (`sts_files=2 oracle=2`), K3 pass
  (`scanned=1414,hits=0,allowed=18,unused_allow=0`), K4 pass (`missing=none extra=none`, STS allowlist row
  refused rc=2), K5 pass (`rows=1`; the row's round cell is still `87`). rc=0.
- **with the r87 pin `b2bf9d65…` (the base bytes): K1 FAIL only**, every other limb identical, rc=1 —
  exactly the expected sha difference, and no behavioural regression from the two new shapes
  (K4's planted HIT set is exact: the new patterns add no hit on the r87 plant).
Receipt: `CriticHarm-receipts/gate-continuity.txt`, `…/r87-counter-at-r88-landing.txt`.

## 4. The C1 repoint — HARM on 1 of 64 changed lines

All 64 changed lines insert exactly one prefix, `corpus/knowledge/`, before a backticked
`<name>.md[:N[-M]]`; 50 map keys, all hit (`M3 keys_hit=50`). 63 lines are meaning-preserving. Checked
against the strongest ambiguity the format allows (a name whose referent is a different tree):

- `authorised-testing-rules-of-engagement.md`, `pz-reporting-transparency-trial.md`,
  `iso-29147-…-crosswalk.md`: "this entry does not restate / separates this row from / the round-25 F10
  entry" — the referent is the lane entry. OK.
- `triage-thresholds.md` (54 lines): narrative-companion sentence and the 11 "Corpus tie" table cells
  (`MATCHES: corpus/knowledge/<entry>.md:N-M`). The column's value is a per-row corpus-tie verdict, not a
  quoted filename. OK.
- `root-loss-2026-10-12.md` (3 lines): `citation-bases.md` and the two `ufo-workspaces.md` occurrences read
  as the **lane entries that hold** the re-anchored ufo-fsd citations — confirmed by the same
  parenthetical's other member `ufo-archive-2026.md:31`, which `.ufo/waves/round-88/c1/excluded.json`
  itself records as a lane-entry key (`anchor-content-drift:no shared identifier on 1/1 citing lines`).
  OK.
- `claim-gates.md`: the sentence quotes the committed gate — ``(`corpus/instruments/claim-package-check.py:4-8`
  says it derives from `corpus/knowledge/claim-gates.md` ``. Verified **not** a misquote: the gate's
  docstring already wrote `corpus/knowledge/` paths at base (`git show 6beead91:corpus/instruments/claim-package-check.py`
  lines 4-5). The repoint makes the quotation match the file. OK (and a genuine improvement).
- `considerthese-proposals-ledger.md`: "written from this entry (`corpus/knowledge/claim-gates.md`)". OK.

### H1 — the counterexample

`corpus/knowledge/japanese-domestic-disclosure-workflow.md:7` (`ground:` front matter), base →

```
ground: F12 — adopts the staged package entry `japanese-domestic-disclosure-workflow.md`
        (`/home/vgpnk/Projects/shokuknow/merge/kasegi/`, read-only), re-grounded line by line …

ground: F12 — adopts the staged package entry `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
        (`/home/vgpnk/Projects/shokuknow/merge/kasegi/`, read-only), re-grounded line by line …
```

The backticked value is now a **lane-relative repo path attached to a foreign root**, in the entry's own
provenance record:

- `test -e /home/vgpnk/Projects/shokuknow/merge/kasegi/corpus/knowledge/japanese-domestic-disclosure-workflow.md`
  → ABSENT; the staged file that does exist is
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`
  (EXISTS).
- The two copies are not the same file, as the sentence's own next clause says ("re-grounded line by line …
  none copied from the package bytes"): sha256 `a1ccb8c7…1996` (lane) vs `ee667c2f…72ec` (staged).

So the line now calls a lane path "the staged package entry" while naming a root under which that path
does not exist. Meaning changed: the base form was a *label inside the named staging tree*; the new form
is a *repo path* that resolves to a different file.

**Why the map could not see it.** The key is **unanchored**, and `knowledge-meter.py`'s M8 exempts
unanchored keys ("Unanchored keys cite a whole entry and are exempt"). 13 of the 50 keys are unanchored
(`authorization-safe-harbor-and-scope`, `citation-bases`, `claim-gates`, `claim-package-contract`,
`ev-model`, `intake-surface`, `japanese-domestic-disclosure-workflow`, `mission-control`,
`ops-invariants`, `triage-thresholds`, `ufo-workspaces`, `vendor-disclosure-policies-as-corpus-objects`,
`vendor-disclosure-policy-commitments-crosswalk`), i.e. **26% of the tranche has no content check at
all** — the round's "new M8 content proxy" is silent exactly where whole-entry citations live. The other
map limbs cannot separate the classes either: M4's test is "the basename's only tracked non-`.ufo` file is
`corpus/knowledge/<name>.md`", and a staged copy in a read-only sibling repo is not tracked here.
A scan of every base citing line for external-root markers (`/home/`, `~/Projects`, `shokuknow`,
`origin-work`, `bounties`, `merge/kasegi`, `[lost-tree]`, `[lost-base]`) returns exactly three lines:
this one, `claim-gates.md:130` (a `restoration-recheck:` shell command, unchanged by the landing) and
`triage-thresholds.md:436` (the `[lost-base]` marker binds `fleet-dispatch.mjs`, not the repointed
`mission-control.md`). **One defect, one class gap.**
Receipt: `CriticHarm-receipts/H1-two-copies.txt`, `…/map-audit.txt`.

**Smallest safe correction — and its measured price.** The frozen map, counter, target and sha pin make
any fix a *later*-commit change (the kill rule already allows this: "a post-landing semantic finding is
reverted in a later commit and reported as a qualifier"):

- Reverting this one key on the landing clone reads `after=741/1743`, `M1/M2/M3 FAIL`, rc=1 — so a revert
  must move the key to `excluded.json` and re-freeze map + counter + target + map sha in r89.
- Preferred: keep the lane path (it is the useful citation) and rewrite the non-backticked prose so root
  and path agree, e.g. "adopts the staged package entry, lane copy `corpus/knowledge/<name>.md`, staged
  under `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/`, read-only". Same cost: M3 is an exact
  line comparison, so this also fails the frozen limbs until r89's re-freeze.
- Generator fix for r89: treat a citing line carrying an external-root parenthetical as out-of-class, and
  extend M8 to unanchored keys (require a token from the target entry's H1/title, not any shared word).

Receipt: `CriticHarm-receipts/meter-and-one-key-revert.txt`.

## 5. Other axes' owned surfaces — NO HARM (one pending registry state)

`git diff --name-only 6beead91 b43dc215 -- PROVINCE.md SHONEN.md LOG.md corpus/README.md corpus/QUALITY.md
MANIFEST.json` prints nothing: untouched.

- `SCORECARD.md`: exactly one row (the C2 `capture-secret-scan` row), which is C2's declared P3 surface;
  its last cell stays `87`, which both the r87 K5 and the r88 K5 require. The old row text is preserved
  inside the new one (round-87 clause kept, round-88 clauses appended) — no evidence statement lost.
- `corpus/SOURCES.md`: changed only at the **freeze** commit, additively (S126, S127 + two record
  bullets); no pre-existing row cell edited, so CORPUS rule 2 (only `status`/`recheck`/`used-by` in place)
  is respected. Census at the C2 landing: rows **127**, malformed **0**, duplicate ids **none**, status
  `mined=105 queued=3 rejected=19`.
- **Pending obligation (not yet a defect):** S126 and S127 are still `queued` with `used-by = —` while the
  landed scanner cites both (`S126` lines 423-424, `S127` lines 402-404/605/638-639) and the SCORECARD row
  names them. The r87 precedent flipped S124/S125 in the **integration** commit (`d788810`), not in the
  landing; the r88 integration commit must flip S126/S127 to `mined`, fill `used-by` with
  `corpus/instruments/capture-secret-scan.py`, add the `Registry 127 rows` record bullet — and see H2.
Receipt: `CriticHarm-receipts/sources-census.txt`.

## 6. C2 — NO behavioural harm; HARM in a knowledge entry it may not edit

Behaviour at the landing rev (summary lines only): base instrument `scanned=1405 hits=0 allowed=18
unused_allow=0 rc=0`; r88 instrument `scanned=1414 hits=0 allowed=18 unused_allow=0 rc=0` — the scope
addition brings exactly the **9** `corpus/practice/*/evidence/` files into scope and nothing hits; the r88
instrument over the **base** rev reads `scanned=1411 hits=0`, and the r86 STS oracle is still exact
(`sts_files=2`). No false positives, no lost coverage, exit codes and the summary format unchanged (the
diff touches only the docstring, `patterns()`, `is_capture_path()` and `selftest()`).
Receipt: `CriticHarm-receipts/scan-scope.txt`.

### H2 — `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` is now false in three places

C2's P3 forbids touching this file, so the landing leaves it stale. It describes the instrument in the
present tense, and the landing falsified it:

| line | statement at landing | re-run |
|---|---|---|
| 13 | "Its shape set is the gate's `SECRET_PATTERNS` … **plus two AWS shapes it adds (instrument lines 21-31)**" | the instrument now adds **four** shapes; the two new ones sit at lines 32-46 (`grep -n 'gcs-signed-url-signature\|azure-sas-signature'`) |
| 111 (FC-4) | "`… capture-secret-scan.py --selftest \| tail -1` prints `SELFTEST-RESULT pass cases=19` at rc 0" | prints `SELFTEST-RESULT pass cases=33` |
| 69 | "exits 0 when nothing matched, 1 …, 2 … (**instrument lines 41-46**)" | the block moved to lines 57/62 (`Output never prints…` 41→57, `Exit 0 when nothing matched…` 46→62) |

Control: the same entry's FC-6 command still reproduces exactly (`scanned=2 hits=0 files=0 allowed=2
unused_allow=15 rc=0`), so this is drift from the two new shapes and the docstring insertion, not a
wholesale staleness. Impacted axis: depth:verifiability (knowledge entries) — a corpus claim falsified by
the round's own change, which C2 does not claim to improve and must not silently damage.
Smallest safe correction: in the integration commit (outside C2's frozen P3 window) update lines 13, 69,
111 — shape set "plus two AWS shapes and two cloud signed-URL shapes", `cases=33`, and the exit-code
anchor to `instrument lines 57-62`. Receipt: `CriticHarm-receipts/H2-stale-entry.txt`.

## 7. Qualifiers (not harm, recorded for the integrator)

- Q1 The two new shapes are **scanner-only**: the gate's `R-NOSECRET` still does not refuse a GCS V4 or
  Azure SAS signature inside a claim package. The docstring's "the gate's patterns … plus" is accurate as
  written, but the pre-commit scan is now the sole authority for those two classes.
- Q2 A GCS signature **wrapped across a line** (the S126 documentation example) is a deliberate negative
  selftest case; that negative is what keeps K3 clean on `S126.txt`. A real line-wrapped signature evades —
  worth naming beside the other limits in a later docstring pass.
- Q3 The tranche leaves bare and path-qualified citations of the same target inside one table column
  (`triage-thresholds.md` rows for `mission-control.md:20-21/13-14/37-43` stay bare; the excluded 54
  anchors). Cosmetic inconsistency only; the claim routes those for manual re-anchoring.
- Q4 The r88 SCORECARD row's round cell remains `87` while the row documents round-88 capability. Both
  counters require/preserve it, and the row text labels each round, so it is a reading convention, not a
  false claim — but a future reader should not mistake `87` for "last exercised in r87".

## Routed defects

1. **D88-H1** (r89, verifiability): revert/re-anchor `japanese-domestic-disclosure-workflow.md:7`'s
   `ground:` citation; re-freeze map + counter (`741/1743` after revert). Class fix: out-of-class rule for
   external-root lines + M8 coverage for unanchored keys.
   Re-run: `python3 -B .ufo/waves/round-88/c1/knowledge-meter.py --lane <clone of fd33e1bf> --base-rev 6beead91 --map .ufo/waves/round-88/c1/repair-map.json --target 742/1743`
   after reverting line 7 → `KNOWLEDGE-METER-RESULT fail`, `after=741/1743`.
2. **D88-H2** (integration, verifiability): update `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`
   lines 13, 69, 111. Re-run: `python3 -B corpus/instruments/capture-secret-scan.py --selftest | tail -1`
   (→ `cases=33`) and the two greps in `CriticHarm-receipts/H2-stale-entry.txt`.
3. **D88-H3** (integration, sources-registry): flip S126/S127 to `mined` with `used-by`, add the
   `Registry 127 rows` record bullet. Re-run the CORPUS frozen-v1 census block in
   `CriticHarm-receipts/sources-census.txt`.

## Credential hygiene / tooling

No credential-shaped value was written under `w1/`: receipts carry sha256 digests, summary and `HIT`-free
lines only; fixtures never left scratch; no counter, scanner or `S<digits>.txt` snapshot was copied in.
The receipts dir was verified clean with the landing scanner:
`python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-88/w1/CriticHarm-receipts/*.txt`
→ `scanned=9 hits=0 allowed=0 unused_allow=17 rc=0`. No tool was installed or upgraded.

## Files written

- `.ufo/waves/round-88/w1/CriticHarm.md` (this report)
- `.ufo/waves/round-88/w1/CriticHarm-receipts/density.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/gate-continuity.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/r87-counter-at-r88-landing.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/meter-and-one-key-revert.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/scan-scope.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/map-audit.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/sources-census.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/H1-two-copies.txt`
- `.ufo/waves/round-88/w1/CriticHarm-receipts/H2-stale-entry.txt`
