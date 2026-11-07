# CriticClaims — hostile closure review of the two frozen claims

Round 87, attempt 1, wave 1. Review only: no edit, no commit, no push, no re-scoring. Every measurement
below was re-run by this seat on 2026-11-07 against committed bytes (`git show`/`git diff`) or a
`git clone --shared` under `/fast/scratch/hyaku/kasegi-r87/CriticClaims/` (cleaned after the run).
The frozen bytes read: `.ufo/waves/round-87/claims.json`, `.ufo/waves/round-87/landing.json`,
`.ufo/waves/round-87/controls/`, `.ufo/waves/round-87/c1/{knowledge-meter,apply-map,build-map}.py`,
`repair-map.json`, `excluded.json`, `.ufo/waves/round-87/c2/capability-check.py`,
`.ufo/waves/round-87/c2/candidate/{capture-secret-scan.py,capture-secret-allow.tsv}`,
`corpus/lessons/round-86-verifier-spotcheck.md`, `corpus/instruments/resolve.py`,
`corpus/instruments/claim-package-check.py`. Receipts: `w1/CriticClaims-receipts/`.

Base `cd1f568a`, freeze `afb13a88`, C1 landing `d87b1b55`, C2 landing `132e16c5` — all confirmed
ancestors of `master` (`git merge-base --is-ancestor`), and `freeze ⊂ C1 landing ⊂ C2 landing`.

## Verdicts on the frozen rules

| Claim | Frozen predicates | Verdict |
|---|---|---|
| C1 depth:verifiability | P1 (counter pass, M1–M7), P2 (13 sha pins), P3 (landing diff only `corpus/knowledge/`) | **NOT VERIFIED** — P1 reproduced, P2 13/13, **P3 false** (3 non-knowledge files at `d87b1b55`). Kill rule fires on its own terms. |
| C2 coverage (capability `capture-secret-scan`) | P1 (K1–K5 pass), P2 (landed instrument + allowlist byte-equal to the frozen candidates) | **VERIFIED** — K1–K5 pass at `132e16c5`, both landed sha256 equal the frozen pins. Qualifiers F6–F9 below, none defeats a predicate. |

Round-level consequence (AXES.md §"Working the axes"): a round is admitted only if **every** claim
verifies; C1 is the only claim on the lowest non-retired axis, so the lowest-axis obligation is unmet
until C1 lands on a commit that satisfies P3. This is a correction requirement, not a re-score: the
83-key repoint itself is mechanically sound (F11, F12).

## Answers to the assigned questions

**(a) Can a do-nothing or cheaper control meet either predicate? No.**
C1: the executed do-nothing (base knowledge as after) is `M1 FAIL 596/1720, rc 1`; the partial,
pad, `.ufo`-copy, S041-forge, quoted-forge and wrong-sha controls each fail at least one limb
(`controls/c1-controls-r87.txt`, copied as `cited-c1-controls-r87.txt`). M1+M2+M3 together bind
exactly the map's 83 backticked substitutions line-by-line, and M2 requires `removed == keys`; there
is no smaller edit that yields `678/1719`. C2: the do-nothing (base, instrument absent) fails K1–K5,
and the eight forgeries in the controls (always-clean, gate-patterns-only, path+shape allowlist,
scope widened to `corpus/`, whole-tree, allowlist refusal disabled, empty allowlist, stale row) each
fail ≥1 limb; a summary-printing stub additionally cannot pass K1 because the claim's invocation pins
`--instrument-sha256 b2bf9d65…` and `--gate-sha256 8b6f8493…`, and P2 requires the landed bytes to
equal the frozen candidate bytes.

**(b) Is C1 nominal in class, and is that honestly stated? Does M4 admit a wrong capture?**
Nominal: yes, and stated. `claims.json` C1 `axis_score` says in terms that the integer is not claimed
to move ("internal-citation repoint, r85/r86 CriticClaims qualifier"), and the uncommitted SCORECARD
row says "score 4 held". The scored `resolve.py` census of record (`corpus/instruments/citation-
survival.md`, 132/701) is not regenerated (the SCORECARD draft says so), so the axis is held, not
moved. M4 narrowing: tested on the strongest counterexample available and **it does not admit a wrong
capture for these 83 keys**. Basename uniqueness under `corpus/source-snapshots/` holds at base and at
the landing for S029/S040/S069/S100/S102 (one each); S029/S040/S100/S102 `.ufo` copies are
byte-identical to their corpus captures, so the narrowing changes nothing there. S069 is the one real
collision: three tracked files share the basename with three distinct digests — the corpus text
capture `round-44/S069.txt` (the map's target), the raw one-line API JSON
`.ufo/waves/round-44/source-recon/S069.txt`, and a **different source** (a Chinese national-standard
PDF) at `.ufo/waves/round-29/wave1/assimilation/fetch/S069.txt`. The cited anchors
(61-62, 78-86, 10-11, 70-72) match the corpus text capture exactly, and the knowledge entry itself
records the token collision and the resolve-by-URL+digest rule at
`corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:36`. So M4's scope is exactly what
makes the repoint correct; the `.ufo` exclusion is load-bearing but contractually sanctioned
("census-of-record root"). Qualifier F5: the numerator gain is 82, not 83 (see below).

**(c) Is C2 a real capability or bookkeeping; is the sourced-claim status valid; is a docstring
citation enough?** It is a real capability, not bookkeeping: the landed instrument implements generic
byte-pattern scanning, scopes capture-class paths, binds allowlist rows to path+shape+sha256 of the
matched bytes, refuses STS allowlist rows, and is exercised on three different trees (r86 freeze,
landing, planted repo) by limbs that fail on each forgery. It is not *enforced*: no tracked gate,
hook, script or SKILL.md rule invokes it before a commit (F6). Source validity: S124 lines 83-85 do
state that `X-Amz-Security-Token` carries the session token in header or query string, S125 lines
318-319/330-331 do give the `AKIA`/`ASIA` prefixes, and the two new shapes are exactly those two (the
`private-key`/`credential`/`authorization` shapes are inherited from the gate, and the docstring says
so). A docstring citation alone would not be the sourced-claim record; here it is backed by two tier-A
registry rows with manifest quotes and by the round lesson's §Gate entries. BUT at the landing commit
both rows are still `status: queued`, `used-by: —` (F7), so the source use is not yet recorded in
committed bytes.

**(d) Are C1 and C2 causally separable? Yes, both directions, measured.**
C1's meter passes M1–M7 on a knowledge-only commit on top of the freeze whose tree has **no**
`corpus/instruments/capture-secret-scan.py`, and all 13 P2 pins are freeze-commit artifacts (13/13 OK
there). C2's K1–K5 pass at a commit whose `corpus/knowledge/` is reverted to freeze bytes and whose C2
instruments are at the landing bytes. Receipts: `c1-separability.txt`, `c2-repro-separability.txt`.

**(e) Is the predicate sentence the same condition as the counter code and the receipt label?**
Substantially yes, with three disclosure gaps: (i) C1 `M5` is not an independent limb — its pass
condition is `not m5bad and not m4bad`, so it prints `LIMB M5 FAIL out_of_range=none` when the only
failure is M4 (F3); (ii) C2 P2's allowlist byte-equality is only in the L1 receipt, not in the frozen
counter, whose K1 hashes the instrument and the gate only (F8); (iii) C2 K2's "exactly the two files"
is true at file granularity (`files=2`), but the scanner emits 6 HITs (3 shapes × 2 files) and the
counter's detail line reports only `sts_files=2`, not total files (F9). C1 P1's "limbs M1–M7" is
exact (7 limbs; the receipt prints them in the order M1,M2,M3,M4,M7,M5,M6).

**(f) Does anything in the landing touch a frozen pin? No.**
At `d87b1b55` all 13 `instruments` pins match (also with the C2 landed files absent), and the
C2 landing commit itself (`d87b1b55→132e16c5`) is `SCORECARD.md` + the two instruments, none of which
is a pin. The P3 failure is a landing-scope violation (three wave-scaffold JSONs swept in), not a pin
change; `landing.json`'s note already records it.

## Findings

### F1 — C1 defeats itself on P3 (DEFEAT on the frozen rule; severity: critical to closure)
`git diff --name-only afb13a88 d87b1b55` lists 8 files, 3 outside `corpus/knowledge/`:
`.ufo/waves/round-87/w1-dispatch.json`, `.ufo/waves/round-87/w1-spec.json`,
`.ufo/waves/round-87/w1/swarm-registry.json`. claims.json C1 P3 requires "only corpus/knowledge/
files"; the kill rule says "any of P1-P3 false at the landing commit -> C1 NOT VERIFIED". The claim is
therefore NOT VERIFIED on its own rule. Re-runnable:

    cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
    git diff --name-only afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69 d87b1b55a51d78411438e962a9abbebdd17930cd
    git diff --name-only afb13a88 d87b1b55 | grep -vc '^corpus/knowledge/'   # 3

Do not repair this by editing `landing.json` or by re-labelling the commit: the landing is named in an
**untracked** file (F2), and moving it after the freeze would be a re-score. Smallest safe correction:
land the same five knowledge blobs on a commit whose parent is the freeze, and let that be the C1
landing. Proven in scratch: a knowledge-only commit on top of `afb13a88` has
`outside corpus/knowledge/: 0`, and the frozen counter reads `base=596/1720 after=678/1719` with
M1–M7 pass, rc 0 (`c1-p3-and-clean-landing.txt`). Whether a post-freeze re-land is admitted is the
L1's/planner's call; the r86 precedent (correction commit measured and reported, never re-scored)
applies.

### F2 — the claim→commit mapping and the P1/P3 evidence are not committed (qualifier; severity: high)
`.ufo/waves/round-87/landing.json`, `.ufo/waves/round-87/l1/` and `corpus/lessons/round-87.md` are
untracked in the lane working tree at review time (`git status --porcelain`), and the SCORECARD/
SOURCES/QUALITY/LOG round-87 edits are unstaged modifications. The r86 verifier read committed
receipts; at present a closure judge reads a mutable file for the landing identity. Re-runnable:

    cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git status --porcelain
    git ls-tree -r --name-only 132e16c5 .ufo/waves/round-87/l1/   # empty

Correction: commit `landing.json`, the L1 receipts and the round lesson before closure, and cite the
committed receipt shas in the round row.

### F3 — C1 `M5` is not an independent limb and mislabels its failure (qualifier; severity: medium)
`limbs.append(("M5", not m5bad and not m4bad, ...))` means an M4 failure prints
`LIMB M5 FAIL out_of_range=none`. Demonstrated by re-running the frozen counter with one map value
repointed at the `.ufo` copy (`c1-m5-and-root.txt`):

    cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
    # map variant: "S102.txt:101": ".ufo/waves/round-68/w1/ScoutS102/S102.txt:101"
    python3 -B .ufo/waves/round-87/c1/knowledge-meter.py --lane <clean clone at d87b1b55> \
      --base-rev cd1f568a --map <map variant> --target 678/1719 --work <scratch> | grep -E 'M4|M5'
    # LIMB M4 FAIL bad=S102.txt:101
    # LIMB M5 FAIL out_of_range=none

Does not defeat the positive run (all limbs pass there), but a receipt reader cannot tell an anchor
failure from a binding failure. Correction (round-88 counter): M5 = `not m5bad`.

### F4 — the C1 meter's base reading is not tree-bound (qualifier; severity: medium)
`classify_scope` resolves the base token set against the current `--lane` root, not against the base
commit's tree. Base token `../MISSION.md:49-56` reads `GONE` in the named scratch clone and `INTERNAL`
at the lane path (it walks into the fleet repo's `MISSION.md`), shifting both counts by one:
clean clone `596/1720 after=678/1719`, lane path `597/1720 after=679/1719` (`M1 FAIL`). The claim's
requirement to run under a `/fast/scratch/hyaku/kasegi-r87/` clone is therefore load-bearing, and the
counter has no cleanliness/location limb. Re-runnable:

    python3 -B .ufo/waves/round-87/c1/knowledge-meter.py --lane . --base-rev cd1f568a \
      --map .ufo/waves/round-87/c1/repair-map.json --target 678/1719 \
      --map-sha256 7db928c7... --work <scratch>     # M1 FAIL 679/1719

Correction (round-88): measure the after tree at a rev (`scope_files_rev(lane, rev)`) and/or confine
REL tokens to the lane root.

### F5 — "83 keys" is a key count, not the meter's gain (qualifier; severity: low)
The meter gains **82** distinct resolving citations, not 83: the map value
`corpus/source-snapshots/round-25/S040.txt` already occurs as a full-path token in base knowledge
(`corpus/knowledge/iso-29147-and-30111-division-of-labour.md`), so converting the bare `S040.txt`
removes one token and adds no new one (1720 → 1719, 596 → 678). Independent recomputation of the token
sets (`c1-repro.txt`, `delta.py`): `removed=83`, `added=82`, `values-not-added=1` (the S040 value),
`base already had value tokens: 1`. No predicate mismatch — the claim states the target, not +83 — but
the round report must not say "83 new citations". Re-runnable: import the clone's `resolve.py`,
`collect` on base-rev files vs the landing tree, diff the token sets.

### F6 — C2's "before commit" operation is not wired (qualifier; severity: medium)
The capability row says the scanner screens captures "before commit", and the document says to run it
on every capture before its first commit, but nothing tracked calls it: `git grep -l
capture-secret-scan 132e16c5 -- . ':!.ufo/waves/round-87'` returns only `SCORECARD.md`, the
allowlist, the instrument and the round-87 manifest. `claim-package-check.py` duplicates the generic
patterns but does not invoke the scanner, so a capture can still be committed unscanned. This is the
open half of r86 routed defect 1 (a pre-commit/pre-freeze step with a failing fixture); the landing
delivers the instrument and the failing fixture (K4) but not the step. Does not defeat K1–K5; the
capability is real and exercised. Correction (round 88): call it from the pre-freeze/gate path and
point the SCORECARD row at that caller.

### F7 — C2's sourced-claim registry state is not recorded at the landing (qualifier; severity: medium)
At `132e16c5`, both rows read `status=queued`, `used-by=—`
(`git show 132e16c5:corpus/SOURCES.md | sed -n '136,137p'`). The pending working-tree diff flips both
to `mined` with `used-by: corpus/instruments/capture-secret-scan.py` and logs the old→new change, but
(a) it is uncommitted, so the claim's sourced status is not in committed bytes at the landing, and
(b) CORPUS defines `used-by` as "repo-relative paths of the knowledge entries or lessons citing the
row"; the instrument is neither. The lesson `corpus/lessons/round-87.md` does cite both rows, so the
correction should name it (e.g. `corpus/lessons/round-87.md, corpus/instruments/capture-secret-scan.py`
or the lesson alone). Re-runnable:

    cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
    git show 132e16c5:corpus/SOURCES.md | sed -n '136,137p'    # queued / —
    git status --porcelain corpus/SOURCES.md                    # ' M'

### F8 — C2 P2's allowlist clause is receipt-only (qualifier; severity: low)
claims.json C2 P2 says both landed files are byte-equal to the frozen candidates, but the frozen
counter's K1 hashes only `FILES[0]` (instrument) and `FILES[1]` (gate) against the passed pins; the
allowlist is copied from the rev and used with its default path without being hashed. A re-runner of
the claim's counter command cannot reproduce the allowlist half of P2; only the L1's manual
`c2-landing-r87.txt` shows `EQUAL` (it does). Correction (round 88): add `--allow-sha256` and hash all
three files in K1.

### F9 — C2's K2 oracle shares the shape definition it checks (qualifier; severity: low)
`ORACLE_RE` matches the `X-Amz-Security-Token` key followed by an equals sign and at least 20
characters, query form only — the same literal prefix and the same 20-char threshold as the
scanner's STS pattern — so K2 is a consistency check against a second copy of the
same shape definition, not an independent oracle for recall: a scanner that dropped a token shorter
than 20 characters, or that only matched the query-string encoding, would still pass K2 at
`252df0c9`. The header/JSON-key encodings are exercised only by the instrument's own selftest
(self-graded). Verified at file granularity: `files=2`, `hits=6` (credential, STS, access-key-id per
file), `scanned=1070` at the r86 freeze (`c2-repro-separability.txt`). Correction (round 88): one
independent positive fixture per encoding, written from the source quote rather than from the
scanner's regex.

## What did NOT defeat the claims (tested negatives)

- **Wrong capture (b):** no. All five target basenames are unique under `corpus/source-snapshots/` at
  base and landing; the only distinct-copy case (S069) is decided correctly by the anchors and is
  documented in the entry itself. The corpus anchors reproduce the quoted text: S029:20 is
  Art. 14(4)(a), S069:61-62 is the Google-owned-scope sentence, S100:462-463 are the two PSIRT
  headings, S102:13-15 are the swagger description/title/version (`c1-wrong-capture-test.txt`).
- **Cheaper/do-nothing control (a):** no; see the controls battery and the pin argument above.
- **Causal separability (d):** holds in both directions (`c1-separability.txt`,
  `c2-repro-separability.txt`); all 13 P2 pins are freeze artifacts, not C2-landing artifacts.
- **Frozen pins (f):** untouched at both landings; P2 is 13/13 at `d87b1b55` even with the C2 landed
  files removed.
- **Bug-planting by C1's edit:** M3's line-for-line check is exact (`bad_lines=0`, `keys_hit=83`), the
  diff is 70 insertions/70 deletions in 5 files, and no line's prose changes; `corpus/instruments/
  citation-survival.md` is not touched by the landing.

## Smallest safe corrections, in order

1. Re-land C1 as a knowledge-only commit on the freeze (5 files); re-run the frozen counter on a clean
   clone; keep the map/counter/target bytes unchanged. Do not edit `landing.json` to move the identity.
2. Commit `landing.json`, the L1 receipts and the round lesson; cite receipt shas in the round row.
3. Commit the SOURCES flip for S124/S125 with `used-by` naming the round lesson (and the instrument if
   the lane reads the enumeration permissively); the change log entry is already drafted.
4. Round-88 counter defects (do not touch the frozen bytes now): M5 independent (`not m5bad`), rev-bound
   after-tree/base measurement, allowlist sha in K1, an independent oracle/fixture per STS encoding.
5. Wire `capture-secret-scan` into the pre-freeze/gate path before the SCORECARD row says "before
   commit"; until then the row is an available-tool claim, not an enforced-step claim.
