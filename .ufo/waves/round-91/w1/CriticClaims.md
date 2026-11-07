# CriticClaims — round 91, attempt 1 (wave kasegi-r91-w1, 13 seats)

Seat: attack/verify critic (L1 KasegiR91 holds the planner seat). Scope: the two landed claims,
judged only on their frozen predicates at the landing commits; findings below are routed defects
and qualifiers, never re-scoring.

## Verdicts

| Claim | Verdict | Predicate evidence |
|---|---|---|
| C1 depth:verifiability (tranche 6, score 4, not claimed to move) | **VERIFIED** | P1 pass rc=0 (all limbs M0,M1,M3,M4,M5,M6,M9,M10) from committed bytes at 8a1a00c6; P2 counter `be7a100b…` and map `55d50b66…` equal claims.json; P3 `git diff-tree -r 8a1a00c6` prints exactly `corpus/knowledge/triage-thresholds.md` |
| C2 coverage (score 8 held; capture-secret-scan S133/S134) | **VERIFIED** | P1 pass rc=0 (K1–K8) with both sha pins at seeds 424242 (own), 9191, 1; P2 landed instrument sha = `89e283c6…` = frozen candidate; P3 `git diff-tree -r 1dd0723f` prints exactly `SCORECARD.md` + `corpus/instruments/capture-secret-scan.py` |

Chain checks: base bb4309ff is an ancestor of freeze 53ab692a (freeze touches no `corpus/knowledge/`
path); C1 8a1a00c6 parent = freeze; C2 1dd0723f parent = C1; receipts commit bcbfbde6 adds only the
two l1 receipts. Labels rev e993fd18 (round-90, author kasegi-shokunin, 04:34) **predates** base
(04:44), so the labels cannot have been back-fitted to the landing. The landed SCORECARD row is
byte-identical to `.ufo/waves/round-91/c2/candidate/scorecard-row.txt` (`cmp` → ROW_IDENTICAL).
No limb failed at any seed, so neither kill rule fires.

Receipts: `CriticClaims-receipts/` (`c1-frozen-rerun.txt`, `c2-frozen-3seeds.txt`,
`p2-p3-evidence.txt`, plus the attack receipts named below).

## C1 — attacks

**Not do-nothing-reachable.** M3 forces the after bytes to base + exactly the six map edits, M6 pins
the map sha, M9 binds each row to its label's named edit, M10 forces set equality with the labels;
the no-work control (after=base) fails M1 and M3, and the after file's content is fully determined
by frozen inputs. Nothing else reaches 891/1880.

**Routed defect C1-F1 (counter, M10 — completeness is site-set, not row-set).** A label row whose
site is already mapped but whose key is not in the map is never checked: `load_labels` keys by
`(site,key)` but M10 compares `{site}` sets, and M9 only looks up the map row's own key. Counterexample
(scratch clone, frozen lane untouched): frozen 6 rows + one extra row at site 368 with a different
key → header prints `labels=7`, M10 prints `labelled=6 mapped=6 unapplied=none` and **passes**
(`c1-m10-hole.txt`). The landing is unaffected (the frozen labels file has exactly 6 rows, 6 distinct
sites, 6 distinct keys), so this is the residual half of the round-90 closure's routed defect 1.
Smallest safe correction: `labelled = set(labels)` where `labels` is keyed by `(site, key)` and
`mapped = {(f"{f}:{n}", key_of(old))}`, compared as sets.

**Qualifier C1-Q1 (what the meter's move is).** Independent re-derivation with the pinned resolve.py
(`c1-attribution.txt`): numerator +1 is *solely* site 454 (`ev-model.md:6-20` GONE → absolute
`corpus/knowledge/ev-model.md:13-25` INTERNAL — a path-form normalisation of the same target);
denominator −3 is the removal of three distinct GONE tokens (`mission-control.md:13-14`,
`claim-gates.md:29-36`, `ev-model.md:21-23`). The 457 composite was never counted before (it is not
path-like: `` `` `claim-package-contract.md:9-16, 28-38` `` `` fails `is_pathlike`), and its new
absolute token already existed elsewhere in scope. So 890/1883 → 891/1880 is the exact token
arithmetic of these six edits, and is no evidence by itself that four citations became verifiable.
The claim does not assert a score move, so this is a qualifier, not a defect.

**Qualifier C1-Q2 (a statement clause no limb binds).** "no range of the cited entry supports" is
checked by no limb (M5 only asserts the repointed anchor lies *inside* the entry). Independently
verified at base (`c1-truth-check.txt`): (141) mission-control.md states `--max` only as a loop bound
(L17) and never its default 5; (142) no `STAGGER`/`stagger`/20 s occurrence in that entry; (226) the
custodian section L29-37 has no unreadable-file precheck and `readJson` is absent; (368) L21-23 pins
only `p_*`, and L49-51 is a field-name list without types/bounds. Both repoints hold: ev-model.md
L13-19 is the formula fence and L24-25 the UNKNOWN fail-closed bullet; claim-package-contract.md
L9-16 is the header, separator and six rows, while L28 (start of the dropped 28-38 span) is blank.
The statement's assertion is true; the counter just cannot check it.

## C2 — attacks

**Counter coverage is the weak half, not the instrument.** The landed scanner implements every
clause I can construct: `%26`-separator cookie hit, digit-prefixed name miss, 2-letter Azure window
hit, 1-letter miss, `skdutid` hit (`c2-forgery-behaviour.txt`, matrix block). Four forgeries that
each violate a literal clause of the frozen statement pass **all** K limbs (K1–K8) unpinned at seed
9191 and are rejected only by the sha pin:

| Forgery | One-line change | Behaviour at the statement's boundary |
|---|---|---|
| FC1 | `_CK_LB` drops `(?<=\u0026)`, `(?<=%26)` | misses a name right after a JSON `\u0026` separator |
| FC2 | `_CK_LB` rejects only `[_-]` | false-positive on `xCloudFront-Signature=` |
| FC3 | `\n` join keyed to `(?<=Path=/\n)` | misses a generic JSON `\n` join |
| FC4 | Azure `_PARAM` `{2,7}` → `{1,7}` | accepts a 1-letter name the statement excludes |

All four print `CAPABILITY-CHECK-RESULT pass rc=0` (`c2-forgeries.txt`), and each deviates from the
statement at the fixture shown in `c2-forgery-behaviour.txt` (diffs: `c2-forgery-diffs.txt`).

**Routed defect C2-F1 (K8 clause map omits three statement clauses and one half-clause).** Missing
from `CLAUSES`/plants: (i) the `\u0026`/`%26` cookie left-boundary exception (no plant, no clause;
the `%26` form is untested too); (ii) rejection of a preceding letter, digit or `_` (only `-` is
tested, S020/K7-n5); (iii) the generic JSON `\n` join (K4's E4 only fixes the `Path=/` context and
K7 has no generated `\n`-join cookie positive, so FC3 survives); (iv) the Azure window's lower bound
of 2 letters (no 1-letter negative). K8's own wording ("every clause … named in CLAUSES") is
self-scoped, so these gaps are invisible to it. Smallest safe correction: four K4 plants + three K7
generated plants + four `CLAUSES` rows, mirrored in the instrument's own selftest, then re-freeze.

**Qualifier C2-Q1 (coverage, not re-scoring).** The SCORECARD row's last column is
"First-working round" (= 87), unchanged and pinned by K5 — it is row identity, not a score. The axis
score (8) is held explicitly. Weight of the coverage claim rests on (a), a genuinely new shape; (b)
is detection completeness (a false-negative repair) inside the existing `azure-sas-signature` shape,
so "new edge classes" is one new shape plus one widened field window.

**Bounded observation C2-Q2 (cross-capability).** `capture-source.py` imports the scanner's
`patterns()`/`scan_bytes`, so the intake gate inherits the new cookie shape with no code change. No
regression is observed: K3 scans 1734 lane files at the landing with 0 hits, and the round-90 gate
counter contains no cookie fixture (grep). That counter was not re-run (out of this claim's surface).

## Files written

- `.ufo/waves/round-91/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c1-frozen-rerun.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c2-frozen-3seeds.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/p2-p3-evidence.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c1-attribution.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c1-m10-hole.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c1-truth-check.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c2-forgeries.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c2-forgery-behaviour.txt`
- `.ufo/waves/round-91/w1/CriticClaims-receipts/c2-forgery-diffs.txt`

Receipts carry digests, seeds, LIMB/HIT/summary lines only — no fixture bytes and no
credential-shaped values. Fixtures, the forgery clone and all counter `--work` trees lived under
`/fast/scratch/hyaku/kasegi-r91/CriticClaims/`, which is deleted. No git/jj write touched the lane
(read-only `show`/`archive`/`diff-tree`/`ls-tree` only; forgery commits are in the scratch clone).
No tool was installed or upgraded. Lane tree, frozen c1/c2/controls/l1 bytes and instruments were
never edited.
